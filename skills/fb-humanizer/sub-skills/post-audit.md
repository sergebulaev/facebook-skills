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
- **Blockers** (must fix before publishing)
- **Warnings** (ship-risky)
- **Suggested fixes** for each issue
- **Timing recommendation** given the audience

## Checks

### Blockers (auto-fail)

1. Em dash / en dash / double dash present.
2. Opens with "We are thrilled / excited / delighted to announce" or equivalent.
3. Engagement bait ("LIKE and SHARE if you agree", "comment YES", "tag 3 friends").
4. Ends with "What do you think?" / "Thoughts?".
5. Contains AI vocabulary blacklist words (see `../references/scrub-rules.md`).
6. First line does not stand alone (it needs line 2, but Facebook folds the rest
   behind "See more").
7. A bare external link with no framing text.

### Warnings (flag with a suggested fix)

8. Did not try the under-80-char short version when the point would fit. That is
   the engagement sweet spot (~66% lift, reported).
9. 3 or more hashtags, or a hashtag mid-sentence.
10. 3 or more emoji, or any emoji on a serious post.
11. No specific number anywhere the claim would allow one.
12. No named entity (person, company, tool).
13. Rule-of-three list without concrete items.
14. No clear primary goal: the draft chases shares, comments, and reactions all
    at once. Pick one (see `../../../references/hook-formulas.md`
    "Engagement-goal split").
15. Designed only for a passive Like, not a share or a comment.
16. A single post trying to carry two ideas (should be two posts).
17. A link post the user may not realize reaches fewer people organically.

### Info (neutral notes)

18. Suggested posting window given the audience (Facebook often peaks early
    weekday afternoons).
19. Short-post vs story-post recommendation given the material.
20. Share-bait opportunity: if the draft is an opinion, tip, or number, note that
    shares are the reach multiplier on a Page and the post should be built to be
    passed on.

## Steps

1. Detect the container: short post or story post.
2. Count chars, flag against the 80-char sweet spot and the 63,206 ceiling.
3. Run the blocker checks. If any, return **FAIL** with specific fixes;
   optionally offer to hand off to `fb-humanizer` for an auto-rewrite.
4. If no blockers, run the warnings.
5. Return the structured report with a timing note.

## Related

- `fb-humanizer` - aggressive rewrite if the audit fails
- `fb-post-writer` - regenerate using a proven formula
