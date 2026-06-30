---
name: fb-humanizer
description: Scrub AI tells from any Facebook Page post draft, or audit a finished draft against the 2026 Facebook checklist. Strips em dashes, AI vocabulary (leverage, delve, harness), "We are thrilled to announce" openers, and corporate auto-pilot, then adds human fingerprints. Includes a --mode audit pre-publish check (under-80 sweet spot, hook, engagement bait, hashtag and emoji limits). Triggers on humanize, de-AI my post, audit before posting. Not for writing from scratch (use fb-post-writer).
---

# Facebook Page Humanizer

Rewrites any Facebook Page post to remove AI tells, and audits a finished draft
against the 2026 Facebook ranking checklist. Based on Wikipedia's "Signs of AI
writing" taxonomy plus Facebook-Page-specific patterns (the under-80 sweet spot,
the "See more" fold, the "We are thrilled to announce" corporate tell, and the
meaningful-interactions model).

## When to use

- Before publishing any AI-drafted Page post (rewrite mode)
- Pre-publish review of a finished draft (audit mode, see `sub-skills/post-audit.md`)
- When a draft feels corporate or off and you cannot pinpoint why

## Input

Any text: a short Page post, a longer story post, or a comment reply draft.
Optional: target voice samples (the Page's past posts).

## Output

- Rewritten text with AI tells removed
- A diff showing what changed and why
- Char count, with a flag when a post crosses the 80-char sweet spot
- Confidence: "human", "mixed", "AI-likely"

## Modes

```bash
# Default: scrub AI tells and fix Facebook-format issues
fb-humanizer <text>

# Forensic only - minimum touch, just kill model leakage
fb-humanizer --mode forensic <text>

# Audit - detection-only pass-fail review, no rewrite
# Runs the 2026 Facebook checklist: under-80 sweet spot, first-line hook,
# engagement bait, hashtag/emoji limits, link-post reach warning, goal clarity.
# Returns Blockers + Warnings + suggested fixes. See sub-skills/post-audit.md.
fb-humanizer --mode audit <text>
```

## The three passes

### Pass 1 - SCRUB (delete or replace)

Apply the tiered catalogs in `references/scrub-rules.md`:

- **Forensic** (always on): real model leakage no human types. AI tool markers
  (oaicite, contentReference, turn0search0), knowledge-cutoff disclaimers ("As
  of my last update"), template blanks ([Your Name], [Page Name]), and em dash
  overuse.
- **Strict** (default on): bad Page style regardless of origin. Vocabulary swaps
  (leverage -> use, delve -> look, harness -> use, foster -> build), filler
  adverbs (fundamentally, essentially, ultimately), corporate openers ("We are
  thrilled to announce" -> the plain news), phrase cleanups ("in today's
  fast-paced world", "game-changer", "deep dive"), and dead closers ("What do
  you think?").

### Pass 2 - BREAK (force burstiness)

- If the post is long, look for the short version hiding inside it. The
  under-80-char line often beats the paragraph.
- Add a sentence fragment where it fits ("Every time.").
- Break perfect parallel structures with one asymmetric line.

### Pass 3 - ADD (human fingerprints)

Require where the content allows:
- 1 specific number (replace "many", "a lot", "massive")
- 1 named entity (real person, company, tool)
- a warm, human Page voice (not a press release, not a faceless bot)
- 1 first-person or behind-the-scenes concrete detail

If the input lacks these, ask the user for a number or anecdote. Do not
fabricate.

## Non-negotiable rules

Global voice rules: see root `SKILL.md` Voice rules. Additional skill-specific
rules:

- Preserve the user's actual claim. Humanizing does not change meaning.
- Never introduce facts that were not in the input. If a number is missing, ask.
- Keep the Page's voice quirks (its register, its `..` soft pauses).
- Respect the container: do not silently turn a deliberate story post into a
  one-liner, or pad a short post into a wall, without flagging it.

## Facebook-specific tells this skill catches

- "We are thrilled / excited / delighted to announce.." corporate auto-pilot.
- A long post whose actual point is one short line hiding in paragraph 3.
- A first line that needs the second line to make sense (the "See more" fold).
- Engagement bait ("LIKE and SHARE if you agree", "comment YES", "tag 3 friends").
- 5+ hashtags stuffed at the bottom.
- A bare external link with no framing text.
- Generic corporate hype with no specific detail.

## Example

See `references/examples.md` for worked before/after rewrites.

## Files

- `SKILL.md` - this file (rewrite scrubber + audit-mode entry)
- `references/scrub-rules.md` - vocabulary swaps and regex by tier
- `references/examples.md` - worked before/after rewrites for short and story posts
- `references/audit-checklist.md` - the pre-publish checklist with thresholds
- `sub-skills/post-audit.md` - pre-publish audit workflow (detection-only, no rewrite)

## Related skills

- `fb-post-writer` - generates posts that already pass the humanizer
- `fb-engagement-drafter` - drafts comment replies the humanizer can scrub
