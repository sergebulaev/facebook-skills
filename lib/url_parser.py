"""Facebook Page URL parser.

Handles the common shapes for Page posts and Page profiles. Facebook URLs are
messier than most platforms: the same post is reachable through several formats,
and the share/pfbid tokens are opaque.

1. Page post (from "Copy link" on a Page post):
   https://www.facebook.com/PageName/posts/PFBID...
   https://www.facebook.com/PageName/posts/123456789012345
   https://www.facebook.com/PageName/posts/pfbid0xxxxxxx

2. Permalink form (older share links, includes the page id):
   https://www.facebook.com/permalink.php?story_fbid=123&id=456
   https://www.facebook.com/story.php?story_fbid=123&id=456

3. Photo, video, and watch posts:
   https://www.facebook.com/photo.php?fbid=123
   https://www.facebook.com/photo/?fbid=123
   https://www.facebook.com/watch/?v=123
   https://www.facebook.com/PageName/videos/123

4. Short share links (opaque token, page/post id not recoverable):
   https://www.facebook.com/share/p/abc123XYZ/
   https://www.facebook.com/share/v/abc123XYZ/
   https://fb.com/share/p/abc123XYZ/

5. Page profile:
   https://www.facebook.com/PageName
   https://www.facebook.com/profile.php?id=123456789   (numeric page)
   https://fb.com/PageName

Returns a normalized dict:
    {
      "page": "<page slug or numeric id>" | None,
      "post_id": "<story_fbid / fbid / pfbid / numeric>" | None,
      "share_token": "<opaque token>" | None,
      "url_type": "post" | "profile" | "share" | "unknown",
      "canonical_url": "https://www.facebook.com/..." | None,
    }

Note: fb.com is normalized to www.facebook.com. The bundle targets business
Pages, not personal profiles (Publora cannot post to personal profiles). A
"share/p" link hides the page and post ids behind an opaque token, so the parser
flags it as url_type "share" and asks the user to paste the post text.
"""
from __future__ import annotations
import re
from typing import Optional, TypedDict
from urllib.parse import urlparse, parse_qs


class ParsedFacebookUrl(TypedDict, total=False):
    page: Optional[str]
    post_id: Optional[str]
    share_token: Optional[str]
    url_type: str
    canonical_url: Optional[str]


_FB_HOSTS = {
    "facebook.com",
    "www.facebook.com",
    "m.facebook.com",
    "mobile.facebook.com",
    "web.facebook.com",
    "fb.com",
    "www.fb.com",
    "fb.me",
}

# Reserved first-path segments that are not Page slugs.
_RESERVED = {
    "permalink.php",
    "story.php",
    "photo.php",
    "photo",
    "watch",
    "share",
    "profile.php",
    "events",
    "groups",
    "marketplace",
    "gaming",
    "watch.php",
    "sharer",
    "sharer.php",
    "login",
    "login.php",
    "home.php",
    "pages",
    "pg",
}

# /PageName/posts/POSTID  (POSTID may be numeric or a pfbid token)
_PAGE_POST_RE = re.compile(
    r"facebook\.com/(?P<page>[A-Za-z0-9.\-]+)/(?:posts|videos)/(?P<post>[A-Za-z0-9]+)",
    re.IGNORECASE,
)


def _normalize_host(text: str) -> str:
    """Rewrite fb.com / fb.me / m.facebook.com to www.facebook.com so the
    regexes only have to match one host."""
    return re.sub(
        r"(?:https?://)?(?:www\.)?(?:m\.|mobile\.|web\.)?(?:fb\.com|fb\.me|facebook\.com)",
        "https://www.facebook.com",
        text.strip(),
        count=1,
        flags=re.IGNORECASE,
    )


def parse_facebook_url(url: str) -> ParsedFacebookUrl:
    """Parse any Facebook Page post or profile URL into structured fields.

    >>> p = parse_facebook_url("https://www.facebook.com/Stripe/posts/123456789")
    >>> p["page"], p["post_id"], p["url_type"]
    ('Stripe', '123456789', 'post')
    >>> q = parse_facebook_url("https://www.facebook.com/permalink.php?story_fbid=99&id=42")
    >>> q["post_id"], q["page"], q["url_type"]
    ('99', '42', 'post')
    """
    out: ParsedFacebookUrl = {
        "page": None,
        "post_id": None,
        "share_token": None,
        "url_type": "unknown",
        "canonical_url": None,
    }
    if not url:
        return out

    text = _normalize_host(url)
    parsed = urlparse(text)

    # Reject non-Facebook hosts before any profile fallback. Without this, a
    # single-segment path on any host (twitter.com/elon, example.com/SomePage)
    # would be misread as a fake FB Page profile, and a bare string with no
    # host ("not a url") would be misread as a page slug.
    host = (parsed.netloc or "").lower().split(":", 1)[0]
    host = re.sub(r"^(?:www\.|m\.|mobile\.|web\.)+", "", host)
    if host not in _FB_HOSTS:
        return out

    path = parsed.path or ""
    qs = parse_qs(parsed.query or "")

    # 1. permalink.php / story.php  ->  story_fbid + id
    if path.lower().rstrip("/").endswith(("permalink.php", "story.php")):
        story = (qs.get("story_fbid") or [None])[0]
        page_id = (qs.get("id") or [None])[0]
        out["post_id"] = story
        out["page"] = page_id
        # Only call it a post if at least one id was actually recovered; a bare
        # /permalink.php with no query params is unknown (ask for a paste).
        if story or page_id:
            out["url_type"] = "post"
        if story and page_id:
            out["canonical_url"] = (
                f"https://www.facebook.com/permalink.php?story_fbid={story}&id={page_id}"
            )
        return out

    # 2. photo / watch  ->  fbid or v
    # Match on the FINAL path segment only. Using endswith over the whole path
    # would misclassify Page slugs like /BestWatch or /MyPhoto as dropped posts.
    low = path.lower().rstrip("/")
    segs = [p for p in low.split("/") if p]
    last_seg = segs[-1] if segs else ""
    if last_seg in {"photo.php", "photo"}:
        fbid = (qs.get("fbid") or [None])[0]
        if fbid:
            out["post_id"] = fbid
            out["url_type"] = "post"
            out["canonical_url"] = f"https://www.facebook.com/photo.php?fbid={fbid}"
        return out
    if last_seg == "watch":
        vid = (qs.get("v") or [None])[0]
        if vid:
            out["post_id"] = vid
            out["url_type"] = "post"
            out["canonical_url"] = f"https://www.facebook.com/watch/?v={vid}"
        return out

    # 3. /share/p/TOKEN/ or /share/v/TOKEN/  (opaque, ids not recoverable)
    m_share = re.search(r"/share/(?P<kind>p|v|r)/(?P<token>[A-Za-z0-9_-]+)", path, re.IGNORECASE)
    if m_share:
        kind = m_share.group("kind").lower()
        out["share_token"] = m_share.group("token")
        out["url_type"] = "share"
        out["canonical_url"] = (
            f"https://www.facebook.com/share/{kind}/{m_share.group('token')}/"
        )
        return out

    # 4. profile.php?id=NUMERIC  (numeric Page id, treated as a profile target)
    if low.endswith("profile.php"):
        page_id = (qs.get("id") or [None])[0]
        if page_id:
            out["page"] = page_id
            out["url_type"] = "profile"
            out["canonical_url"] = f"https://www.facebook.com/profile.php?id={page_id}"
        return out

    # 5. /PageName/posts/ID or /PageName/videos/ID
    m_post = _PAGE_POST_RE.search(text)
    if m_post:
        page = m_post.group("page")
        post = m_post.group("post")
        out["page"] = page
        out["post_id"] = post
        out["url_type"] = "post"
        out["canonical_url"] = f"https://www.facebook.com/{page}/posts/{post}"
        return out

    # 6. Page profile: /PageName  (single path segment, not reserved)
    seg = [p for p in path.split("/") if p]
    if len(seg) == 1 and seg[0].lower() not in _RESERVED:
        out["page"] = seg[0]
        out["url_type"] = "profile"
        out["canonical_url"] = f"https://www.facebook.com/{seg[0]}"
        return out

    return out


def build_post_url(page: str, post_id: str) -> str:
    """Format a canonical Page post URL from a page slug and a post id."""
    page = page.strip("/")
    return f"https://www.facebook.com/{page}/posts/{post_id}"


if __name__ == "__main__":
    import json
    import sys

    examples = sys.argv[1:] or [
        "https://www.facebook.com/Stripe/posts/123456789012345",
        "https://www.facebook.com/permalink.php?story_fbid=99887766&id=4455",
        "https://www.facebook.com/share/p/abc123XYZ/",
        "https://www.facebook.com/watch/?v=778899",
        "https://fb.com/Notion",
        "https://www.facebook.com/profile.php?id=100064123456789",
    ]
    for u in examples:
        print(u)
        print(json.dumps(parse_facebook_url(u), indent=2))
        print()
