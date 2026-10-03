#!/usr/bin/env python3
"""Every skill that reads text a stranger wrote must carry the untrusted rule.

The read layer, and the user pasting someone else's post, both hand the model
text the user did not write, and the same agent can publish to their account.
The data-is-not-instructions rule has to travel with the skills that do the
reading, not live only in a reference nobody is pointed at.

Two triggers, because the two kinds of reading look different in the document:

* **REQUIRED** names the skills whose input is somebody else's content, pasted
  or fetched. Removing the section from one of these fails the check.
* **READ_CALLS** catches a skill that starts calling the read layer without
  anyone remembering to add the section.

Run from the repo root:

    python3 scripts/check_untrusted_rule.py
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = sorted(d for d in (ROOT / "skills").iterdir() if (d / "SKILL.md").is_file())
CANONICAL = ROOT / "references" / "untrusted-content.md"
SECTION = re.compile(r"^## Untrusted content\s*$", re.M)
CITES = "references/untrusted-content.md"

#: Skills whose input is content somebody else wrote.
REQUIRED = {
    "fb-audience-insights",
    "fb-hook-extractor",
    "fb-engagement-drafter",
}

#: Calls that return text somebody else wrote.
READ_CALLS = re.compile(r"fetch_page_stats|fetch_post_commenters")


def main() -> int:
    problems = []

    if not CANONICAL.is_file():
        problems.append(
            f"{CANONICAL.relative_to(ROOT)} is missing. Every skill that reads "
            f"other people's text points at it.")

    names = {s.name for s in SKILLS}
    for gone in sorted(REQUIRED - names):
        problems.append(
            f"REQUIRED lists {gone}, which is not a skill in this bundle. A rename "
            f"has to update this check too.")

    for skill in SKILLS:
        text = (skill / "SKILL.md").read_text(encoding="utf-8")
        has = bool(SECTION.search(text))
        if skill.name in REQUIRED and not has:
            problems.append(
                f"skills/{skill.name}/SKILL.md reads content somebody else wrote and "
                f"has no `## Untrusted content` section. The rule has to be in front "
                f"of the text, not only in references/.")
        elif READ_CALLS.search(text) and not has:
            problems.append(
                f"skills/{skill.name}/SKILL.md names a read-layer call but has no "
                f"`## Untrusted content` section. Add the section, and add the skill "
                f"to REQUIRED in this script.")
        if has and CITES not in text:
            problems.append(
                f"skills/{skill.name}/SKILL.md has the section but never cites "
                f"{CITES}, so the full rule is unreachable from it.")

    if problems:
        print("Untrusted-content rule:\n" + "\n".join("  " + p for p in problems))
        return 1

    print(f"OK: {len(REQUIRED)} skills read other people's text and all of them "
          f"carry the untrusted-content rule.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
