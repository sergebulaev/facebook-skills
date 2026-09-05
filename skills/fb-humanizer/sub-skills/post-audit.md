# Facebook Page Post Audit

Run any Page-post draft through the 2026 Facebook ranking checklist. Catches AI
tells, corporate auto-pilot, engagement bait, the missed under-80 sweet spot,
link-post reach issues, and structural weaknesses before publishing. This is the
`fb-humanizer --mode audit` workflow: detection only, no rewrite.

## When to use

- Before publishing a hand-written or AI-drafted Page post
- When `fb-post-writer` finishes a draft (auto-invoked)
- When a recent post underperformed and the user wants a post-mortem

## Input

- A Page post (short or story)
- Optional: target audience, scheduled time, whether it is a link/photo/video post

## Output

- **Pass / Fail** header
- **Blockers** (must fix before publishing): em dash density over the cap,
  paragraphs at 3+ AI markers, corporate openers, reveal bridges, engagement
  bait, bare links
- **Warnings** (ship-risky): staccato stacks, sincerity markers, missing
  referenced numbers, generic close, missed short version
- **Suggested fixes** for each issue
- **Per-paragraph tell density** (markers, em dashes per 100 words,
  fragments, triads). No detector score: on post-length text those are noise
  and the skill does not promise to beat them
- **Timing recommendation** given the audience

## Checks

### Blockers (auto-fail)

1. Em dash density above about 1 per 100 words (more than 1 in a short post,
   more than 2 in a story post); en dash between clauses; double dash. A
   single em dash is not a blocker.
2. Opens with "We are thrilled / excited / delighted to announce" or equivalent,
   a reveal bridge ("Here's what", "Stop X, start Y"), or a sincerity
   announcement ("let me be honest", "we'll be real with you", "real talk").
3. Engagement bait ("LIKE and SHARE if you agree", "comment YES", "tag 3 friends").
4. Ends with "What do you think?", "Thoughts?", "Let us know in the comments
   below!", or "Let that sink in." (a specific question is fine).
5. Any paragraph with 3+ vocabulary / grammar markers, or any
   negative-parallelism / "The result?" reveal bridge (see
   `../references/scrub-rules.md`).
6. First line does not stand alone (it needs line 2, but Facebook folds the rest
   behind "See more").
7. A bare external link with no framing text.

### Warnings (flag with a suggested fix)

8. Did not try the under-80-char short version when the point would fit. That is
   the engagement sweet spot (~66% lift, reported).
9. 3 or more hashtags, or a hashtag mid-sentence.
10. 3 or more emoji, or any emoji on a serious post.
11. A story paragraph that reads machine-flat (4+ sentences all the same
    length, no clause doing work). Flag that paragraph only; never suggest
    adding variance as a tactic. A short post has no rhythm to flag.
11a. Staccato stacks ("Short. Punchy. Done.", "No X. No Y. Just Z."), one-word
    paragraphs for drama, more than 2 standalone fragments, or a long/short/
    long/short seesaw.
12. No odd-precision number with a named referent anywhere the claim would
    allow one (a bare number does not clear this).
13. No named entity (person, business, place, tool).
14. Stacked or perfectly parallel rule-of-three, a hollow triad without
    concrete items, or 3+ triads in the post (one natural triad passes).
14a. Hedging stack ("perhaps", "it seems") or a framed confession ("We'll be
    honest, this was hard: ..."). A flat dated fact is fine.
14b. Over-scrubbed (rewrite audits only, with the original in hand to compare
    against; a fresh draft that never had an em dash or a triad is not
    over-scrubbed, and nothing is added to clear this): uniformly flat tone,
    every em dash and triad gone from a story post, a deliberate story post
    shrunk to a one-liner, no reaction or opinion anywhere.
15. No clear primary goal: the draft chases shares, comments, and reactions all
    at once. Pick one (see `../../../references/hook-formulas.md`
    "Engagement-goal split").
16. Designed only for a passive Like, not a share or a comment.
17. A single post trying to carry two ideas (should be two posts).
18. A link post the user may not realize reaches fewer people organically.

### Info (neutral notes)

19. Suggested posting window given the audience (Facebook often peaks early
    weekday afternoons).
20. Short-post vs story-post recommendation given the material.
21. Share-bait opportunity: if the draft is an opinion, tip, or number, note that
    shares are the reach multiplier on a Page and the post should be built to be
    passed on.

## Steps

1. Detect the container: short post or story post.
2. Count chars, flag against the 80-char sweet spot and the 63,206 ceiling;
   count em dashes per 100 words.
3. Run the blocker checks. If any, return **FAIL** with specific fixes;
   optionally offer to hand off to `fb-humanizer` for an auto-rewrite.
4. If no blockers, run the warnings.
5. Report per-paragraph tell density. Do not estimate a detector score.
6. Return the structured report with a timing note.

## Related

- `fb-humanizer` - proportional rewrite if the audit fails
- `fb-post-writer` - regenerate using a proven formula
