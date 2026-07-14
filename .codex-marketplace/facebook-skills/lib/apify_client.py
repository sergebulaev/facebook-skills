"""Apify read client for the Facebook Pages Skills project.

The read layer: given a Facebook Page URL, pull the Page's public stats (title,
followers, likes, categories, intro) so a skill can size up a Page (yours or a
competitor's); and given a public Page-post URL, pull the commenters. Uses the
run-sync-get-dataset-items endpoint (one HTTP request, no polling).

Auth: APIFY_TOKEN env var (or constructor arg). Get one at
https://console.apify.com/account/integrations (free tier included).

Actors (both verified live 2026-07-13):
  - apify/facebook-pages-scraper: input {"startUrls":[{"url":"<page url>"}]}.
    Returns title, pageName, pageId, likes, followers, followings, categories,
    intro, websites, email, profilePictureUrl, coverPhotoUrl.
  - danek/facebook-comments-ppr: input {"post_id":"<post url or pfbid>",
    "max_comments":N}. Returns comments with author {name, id, profile_image},
    message, reactions_count, replies_count, created_time, depth.

What Facebook does NOT expose: the list of who REACTED to (liked) a post.
Facebook shows only reaction COUNTS, never a reactor roster. The engagement
signal here is COMMENTERS + Page stats, not a liker list. That is a platform
wall, not a client limitation. Be honest about it.

Caching: in-process LRU (256 entries, 6h TTL). force_refresh=True to bypass.
Retries transient 429/5xx (3 attempts, exponential backoff + jitter).
"""
from __future__ import annotations
import os
import random
import time
from collections import OrderedDict
from typing import Any, Optional

import requests

PAGES_ACTOR = "apify~facebook-pages-scraper"
COMMENTS_ACTOR = "danek~facebook-comments-ppr"
RUN_SYNC = "https://api.apify.com/v2/acts/{actor}/run-sync-get-dataset-items"
RETRYABLE_STATUSES = {429, 500, 502, 503, 504}
CACHE_MAX_ENTRIES = 256
CACHE_TTL_SECONDS = 6 * 60 * 60
SIGNUP_URL = "https://console.apify.com/account/integrations"


class ApifyError(RuntimeError):
    pass


class ApifyAuthError(ApifyError):
    """No token configured. Message explains the free path + paste fallback."""


def _retry(attempts: int = 3, base_delay: float = 0.6):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            last: Optional[Exception] = None
            for i in range(attempts):
                try:
                    return fn(*args, **kwargs)
                except ApifyError as e:
                    if getattr(e, "status", None) not in RETRYABLE_STATUSES or i == attempts - 1:
                        raise
                    last = e
                    time.sleep(base_delay * (2 ** i) + random.uniform(0, 0.3))
            if last:
                raise last
        return wrapper
    return decorator


def _page_stats(p: dict) -> dict:
    """Map one facebook-pages-scraper row to a clean dict."""
    return {
        "title": p.get("title") or p.get("pageName"),
        "page_name": p.get("pageName"),
        "page_id": p.get("pageId"),
        "page_url": p.get("pageUrl") or p.get("facebookUrl"),
        "likes": p.get("likes"),
        "followers": p.get("followers"),
        "followings": p.get("followings"),
        "categories": p.get("categories") or [],
        "intro": p.get("intro"),
        "websites": p.get("websites") or ([p["website"]] if p.get("website") else []),
        "email": p.get("email"),
        "profile_picture_url": p.get("profilePictureUrl"),
        "cover_photo_url": p.get("coverPhotoUrl"),
    }


def _comment(c: dict) -> dict:
    """Map one facebook-comments-ppr row to a clean dict."""
    au = c.get("author") or {}
    reactions = c.get("reactions_count")
    try:
        reactions = int(reactions) if reactions is not None else 0
    except (TypeError, ValueError):
        reactions = 0
    return {
        "comment_id": c.get("legacy_comment_id") or c.get("comment_id"),
        "author": au.get("name"),
        "author_id": au.get("id"),
        "author_url": au.get("url"),
        "author_profile_image": au.get("profile_image"),
        "message": c.get("message"),
        "reactions": reactions,
        "replies": c.get("replies_count", 0),
        "depth": c.get("depth", 0),
        "is_reply": bool(c.get("parent_comment_id")),
        "created_time": c.get("created_time"),
    }


class ApifyClient:
    def __init__(self, token: Optional[str] = None, timeout: int = 180):
        self.token = token or os.environ.get("APIFY_TOKEN")
        self.timeout = timeout
        self._cache: "OrderedDict[str, tuple[float, Any]]" = OrderedDict()

    def _require(self) -> str:
        if not self.token:
            raise ApifyAuthError(
                "No APIFY_TOKEN set. Get one free at "
                f"{SIGNUP_URL}. Or paste the Page stats or comments you already "
                "have and the skill will run the same analysis on them."
            )
        return self.token

    def _cget(self, k):
        h = self._cache.get(k)
        if h and (time.time() - h[0]) < CACHE_TTL_SECONDS:
            self._cache.move_to_end(k)
            return h[1]
        return None

    def _cput(self, k, v):
        self._cache[k] = (time.time(), v)
        self._cache.move_to_end(k)
        while len(self._cache) > CACHE_MAX_ENTRIES:
            self._cache.popitem(last=False)

    @_retry()
    def _run(self, actor: str, payload: dict) -> list[dict]:
        try:
            r = requests.post(RUN_SYNC.format(actor=actor),
                              params={"token": self._require()}, json=payload,
                              timeout=self.timeout)
        except requests.RequestException as e:
            err = ApifyError(f"network error: {e}"); err.status = 503; raise err
        if r.status_code >= 400:
            err = ApifyError(f"actor returned {r.status_code}: {r.text[:200]}")
            err.status = r.status_code; raise err
        data = r.json()
        if isinstance(data, dict) and data.get("error"):
            raise ApifyError(f"actor error: {str(data['error'])[:200]}")
        if not isinstance(data, list):
            raise ApifyError(f"unexpected response shape: {str(data)[:150]}")
        return data

    # ---- public read methods ----
    def fetch_page_stats(self, page_url: str,
                         force_refresh: bool = False) -> Optional[dict]:
        """Public stats for a Facebook Page (self or competitor): title,
        followers, likes, categories, intro, websites. Verified path.

        Returns a clean dict, or None if the Page could not be read.
        """
        ck = f"page:{page_url}"
        if not force_refresh and (c := self._cget(ck)) is not None:
            return c
        rows = self._run(PAGES_ACTOR, {"startUrls": [{"url": page_url}]})
        out = None
        for row in rows:
            if isinstance(row, dict) and (row.get("title") or row.get("pageName")):
                out = _page_stats(row)
                break
        self._cput(ck, out)
        return out

    def fetch_post_commenters(self, post_url: str, max_comments: int = 25,
                              force_refresh: bool = False) -> list[dict]:
        """Commenters on a public Page post (the Facebook engagement signal,
        since Facebook hides the reactor/liker roster and shows counts only).

        `post_url` may be a full Page-post URL or a bare pfbid post id.
        Verified path.
        """
        ck = f"comments:{post_url}:{max_comments}"
        if not force_refresh and (c := self._cget(ck)) is not None:
            return c
        rows = self._run(COMMENTS_ACTOR,
                         {"post_id": post_url, "max_comments": max_comments})
        out = [_comment(c) for c in rows
               if isinstance(c, dict) and (c.get("author") or c.get("message"))]
        self._cput(ck, out)
        return out


if __name__ == "__main__":
    import json as _json
    print(_json.dumps(ApifyClient().fetch_page_stats(
        "https://www.facebook.com/nasa"), indent=2))
