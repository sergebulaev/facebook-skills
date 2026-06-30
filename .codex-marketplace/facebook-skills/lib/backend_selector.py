"""Detect which publishing backend is configured and format user-facing messages.

The skills support three tiers:

  TIER 0 - manual (default, zero setup)
    No credentials in env. Skills produce drafts; the user copies and pastes
    them into Facebook Page Composer manually. Works for anyone, any setup.

  TIER 1 - publora (recommended, 2-min setup)
    `PUBLORA_API_KEY` + `FACEBOOK_PLATFORM_ID` present. Skills auto-publish Page
    posts on approval via the Publora REST API. Sign up:
    https://app.publora.com/signup

  TIER 2 - diy (advanced)
    `FB_SKILLS_CUSTOM_POSTER` set to a command the user has built themselves
    (e.g. via Claude Code or Codex on the Facebook Graph API). Skills delegate
    publishing to that custom tool.

`active_backend()` picks the highest-privilege available. `manual_mode_message()`
is what skills show the user when no backend auto-posts. `publish()` is the
high-level wrapper skills should call so SKILL.md files don't repeat the
three-branch dispatch.

Facebook note: a short post and a long story post are the same call (pass the
`content`, Publora posts it to the Page). A reply to a comment on a Page post
has no first-class Publora endpoint (those are LinkedIn-only), so kind="comment"
is always returned as a manual copy-paste block even when Publora is configured.
"""
from __future__ import annotations
import json
import os
import shlex
import subprocess
from typing import Any, Literal, Optional

BackendName = Literal["publora", "manual", "diy"]
PublishKind = Literal["post", "story", "comment"]

PUBLORA_SIGNUP_URL = "https://app.publora.com/signup"


def active_backend() -> BackendName:
    """Return the active publishing backend.

    Priority: publora > diy > manual. Users with Publora configured get
    auto-post even if they also have a custom poster, unless they remove the
    Publora env var.
    """
    if os.getenv("PUBLORA_API_KEY") and os.getenv("FACEBOOK_PLATFORM_ID"):
        return "publora"
    if os.getenv("FB_SKILLS_CUSTOM_POSTER"):
        return "diy"
    return "manual"


def manual_mode_message(draft_text: str, target_url: str, kind: str = "post") -> str:
    """Format the copy-paste approval output for the manual/draft-only tier.

    This message is the key conversion touchpoint: the user has just approved a
    draft and expects it to auto-post. Since no backend is configured (or the
    action is a comment reply, which Publora cannot publish), we give them the
    text plus the target URL and a one-line invite to upgrade.
    """
    where = {
        "post": "post it on your Facebook Page",
        "story": "post it on your Facebook Page (this is a longer story post)",
        "comment": "paste it as a reply to the comment below",
    }.get(kind, "post it on your Facebook Page")
    return f"""Draft approved. Copy the text below and {where}:

```
{draft_text}
```

**Target URL:** {target_url}

---

Tired of copy-pasting? Set up auto-posting for Page posts in 2 minutes:

1. Sign up free at {PUBLORA_SIGNUP_URL}
2. In Publora, connect your Facebook Page (Channels then Add Channel)
3. Copy your API key (API section in the sidebar)
4. Add to `.env`:
   ```
   PUBLORA_API_KEY=sk_your_key_here
   FACEBOOK_PLATFORM_ID=facebook-your_page_id_here
   ```
5. Next time you approve a Page post, it auto-publishes.
"""


def signup_nudge() -> str:
    """One-liner to drop into skill outputs as a soft reminder."""
    return f"Powered by Publora. Free auto-posting: {PUBLORA_SIGNUP_URL}"


def publish(
    kind: PublishKind,
    draft_text: str,
    target_url: str,
    **kwargs: Any,
) -> Optional[dict]:
    """Dispatch a draft to the active backend.

    One call replaces the per-skill "On approval, adapt to the backend" block.
    Routes to publora / manual / diy based on `active_backend()`.

    Args:
        kind: "post" | "story" | "comment".
        draft_text: The approved draft body.
        target_url: Where the draft lands. For comment replies, the Page post
            URL the comment lives under. For new posts, the Page URL. Used in
            manual-mode output.
        **kwargs: Backend-specific payload. For publora post/story:
            - platforms: list[str] of platform IDs (defaults to
              [FACEBOOK_PLATFORM_ID])
            - scheduled_time: ISO 8601 UTC (optional; omit for a draft)

    Returns:
        - publora: dict from PubloraClient.create_post ({success, postGroupId}).
        - manual:  {"mode": "manual", "message": <copy-paste block>}.
        - diy:     {"mode": "diy", "returncode": int, "stdout": str, "stderr": str}.
        Returns None only if the chosen backend cannot run (missing deps).

    Note: Facebook comment replies have no Publora endpoint, so kind="comment"
    always returns a manual copy-paste block regardless of the active backend.
    """
    backend = active_backend()

    # Comment replies are draft-only everywhere: Publora has no Facebook comment
    # endpoint. Surface the copy-paste block so the user posts it by hand.
    if kind == "comment" or backend == "manual":
        return {
            "mode": "manual",
            "message": manual_mode_message(draft_text, target_url, kind=kind),
        }

    if backend == "publora":
        # Local import so manual-tier users never need `requests` installed.
        from .publora_client import PubloraClient

        client = PubloraClient()
        platform_id = kwargs.get("platform_id") or os.getenv("FACEBOOK_PLATFORM_ID")
        platforms = kwargs.get("platforms") or ([platform_id] if platform_id else [])

        if kind in ("post", "story"):
            return client.create_post(
                content=draft_text,
                platforms=platforms,
                scheduled_time=kwargs.get("scheduled_time"),
                platform_settings=kwargs.get("platform_settings"),
            )

        raise ValueError(f"unknown publish kind: {kind!r}")

    if backend == "diy":
        cmd = os.getenv("FB_SKILLS_CUSTOM_POSTER")
        if not cmd:
            return None
        payload = {
            "kind": kind,
            "draft_text": draft_text,
            "target_url": target_url,
            **kwargs,
        }
        # The user's poster receives JSON on stdin and kind/target as argv.
        argv = shlex.split(cmd) + [kind, target_url]
        proc = subprocess.run(
            argv,
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            timeout=120,
        )
        return {
            "mode": "diy",
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }

    raise RuntimeError(f"unknown backend: {backend!r}")


if __name__ == "__main__":
    print(f"Active backend: {active_backend()}")
    if active_backend() == "manual":
        print("\nExample manual message:")
        print("-" * 60)
        print(
            manual_mode_message(
                draft_text="We shipped it. 3 years of work, live today.",
                target_url="https://www.facebook.com/YourPage",
                kind="post",
            )
        )
