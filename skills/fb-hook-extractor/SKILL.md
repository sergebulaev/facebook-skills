---
name: fb-hook-extractor
description: Reverse-engineer the hook from a high-share Facebook Page post, from its URL or pasted text. Identifies which of the 10 canonical 2026 Facebook formulas it uses (one-line opinion, tiny number, ask-the-page question, this-or-that, behind-the-scenes, story post, announcement, spotlight), explains why it earned shares or comments, and returns a blank template mapped to your topic. Use to learn from a Page post you admire. Not for writing your own (use fb-post-writer).
---

# Facebook Page Hook Extractor

Paste a high-share Page post URL (or the text). Get back: which hook formula it
uses, the exact structure, why it worked, and a blank template you can fill with
your own voice.

## When to use

- User finds a high-share Page post they want to study
- User wants to replicate a specific Page's pattern
- Before `fb-post-writer`, to seed a draft with a proven shape

## Input

A Facebook Page post URL (any of the many shapes: `/posts/`, `permalink.php`,
`/watch/`, `share/p/`). For a `share/p/` link the page and post ids are hidden
behind an opaque token, so paste the post text. The bundle has no built-in Page
reader, so the user pastes the post text either way.

## Output

- **Formula identified** (FB1-FB10 from `../../references/hook-formulas.md`) with
  a confidence score
- **Container:** short post vs story post, and why that container fit the idea
- **Structural breakdown:**
  - The hook line (and for a story post, how the first line earns the "See more" tap)
  - Body architecture (the beats, for a longer post)
  - The close (what earns the share or the comment)
  - Interaction-triggering devices (numbers, named entities, the question, the turn)
- **Primary goal** the original chased (shares / comments / reactions)
- **Why it worked** psychologically and algorithmically (meaningful interactions)
- **Blank template** with `{slot}` markers matched to the original, ready for the
  user's topic
- **Cautions:** anything in the original that would fail a 2026 audit (em dashes,
  AI vocab, "We are thrilled to announce", engagement bait, 5+ hashtags)

## Steps

1. **Parse the URL.** `lib.url_parser.parse_facebook_url(url)` returns `page`,
   `post_id`, `share_token`, `url_type`. If `url_type` is "share", tell the user
   the ids are hidden and ask for the post text.
2. **Get the text.** This bundle has no built-in Page reader, so ask the user to
   paste the post (and any first comments, if relevant). If they later wire an
   Apify Page actor, read it automatically.
3. **Detect the container.** A short post (one line / under ~80 chars) or a
   longer story post.
4. **Classify against the 10 formulas** using features:
   - Short post: a flat opinion (FB1)? one hard number (FB2)? an easy question
     (FB3)? a binary this-or-that (FB4)? a relatable shared moment (FB5)? a
     behind-the-scenes glimpse (FB6)? a usable tip (FB7)?
   - Story post: a narrative with a turn (FB8)? a launch led human (FB9)? a named
     customer/team spotlight (FB10)?
5. **Score confidence.** If two formulas fit, return the top 2 with fit scores.
6. **Extract structure.** Label each part by its role. For a story post, map the
   first line (the "See more" tap), the beats, and the closer.
7. **Name the primary goal** the original optimized for (shares / comments /
   reactions).
8. **Generate a blank template** with `{slot}` markers matched to the original
   shape and the user's topic.
9. **Audit the source.** Flag any AI tells in the original so the user does not
   copy them.

## Example

See `references/examples.md` for worked teardowns.

## Formulas reference

See `../../references/hook-formulas.md` for the 10 canonical Facebook formulas
with full skeletons and goal tags.

## Files

- `SKILL.md` - this file
- `references/classification-rules.md` - feature extraction + scoring heuristics
- `references/examples.md` - worked teardowns (short post and story post)

## Related skills

- `fb-post-writer` - use the extracted template to draft your own
- `fb-humanizer` - audit your draft before shipping
- `fb-content-planner` - study competitors' Pages while planning
