"""Approval gate helpers.

Every skill that posts to a Facebook Page MUST present a draft to the user and
wait for explicit approval before calling Publora. This file is a thin
conventions layer, not runtime enforcement. Skills call `render_approval_card`
to format the draft consistently and then stop until the user says go.
"""
from __future__ import annotations
from typing import Optional


def render_approval_card(
    *,
    kind: str,  # "post" | "story" | "comment"
    preview_text: str,
    target_url: Optional[str] = None,
    char_count: Optional[int] = None,
    goal: Optional[str] = None,
    extra_context: Optional[dict] = None,
) -> str:
    """Format a standardized approval card for the user to review.

    The card MUST contain:
    - What the action is (post / story / comment)
    - The full preview text
    - Char count, and a note when a short post crosses the 80-char sweet spot
    - Target URL if applicable (the Page, or the post a comment replies under)
    - The primary engagement goal (shares / comments / reactions)
    - A clear prompt: "reply post / yes to publish, or suggest edits"
    """
    lines = [f"## Draft ready for approval - {kind}", ""]
    if target_url:
        lines.append(f"**Target:** {target_url}")
    if char_count is None:
        char_count = len(preview_text)
    lines.append(f"**Chars:** {char_count}")
    if char_count >= 80 and kind == "post":
        lines.append(
            "**Note:** over the 80-char sweet spot. Posts under 80 chars get a "
            "reported ~66% engagement lift. Tighten if you can, or keep it as a "
            "deliberate story post."
        )
    if goal:
        lines.append(f"**Primary goal:** {goal}")
    lines.append("")
    lines.append("**Preview:**")
    lines.append("")
    for pl in preview_text.splitlines() or [""]:
        lines.append(f"> {pl}")
    lines.append("")
    if extra_context:
        lines.append("**Context:**")
        for k, v in extra_context.items():
            lines.append(f"- **{k}**: {v}")
        lines.append("")
    lines.append("Reply **post** / **yes** to publish, or suggest edits.")
    return "\n".join(lines)
