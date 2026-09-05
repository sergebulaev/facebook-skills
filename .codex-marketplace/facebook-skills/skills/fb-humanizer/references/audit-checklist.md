# Pre-Publish Audit Checklist (Facebook Page)

The thresholds the `--mode audit` pass applies. Mirror of the root
`references/algorithm-heuristics.md` checklist, with the humanizer's blocker
distinctions. V3 (2026-09): AI tells are scored by density per paragraph; em
dashes are capped at about 1 per 100 words, not banned; forced rhythm is a
tell.

## Blockers (auto-fail)

- [ ] Em dashes (`—`) at or under about 1 per 100 words (0-1 in a short post,
      1-2 in a story post). A single em dash is not a blocker. No en dash (`–`)
      between clauses, no double dash (`--`).
- [ ] No "We are thrilled / excited / delighted to announce" or equivalent
      corporate opener.
- [ ] No engagement bait ("LIKE and SHARE if you agree", "comment YES", "tag 3
      friends").
- [ ] No "What do you think?" / "Thoughts?" / "Let us know in the comments
      below!" / "Let that sink in." dead closer (a specific question that earns
      a real comment is fine and wanted).
- [ ] No reveal-bridge opener ("Here's what", "Stop X, start Y") and no
      sincerity announcement opener ("let me be honest", "we'll be real with
      you", "real talk").
- [ ] No paragraph with 3+ vocabulary / grammar markers (one marker per
      paragraph is fine); no "It's not X, it's Y" negative parallelism; no
      "The result?" reveal bridge.
- [ ] First line stands alone as a hook (everything above the "See more" fold).
- [ ] No bare external link with zero framing text.

## Warnings (flag with fix)

- [ ] Leads short. If the point fits under 80 chars, the short version is offered
      (the under-80 sweet spot is ~66% more engagement, reported).
- [ ] 0-2 hashtags, at the end.
- [ ] 0-2 emoji, none on a serious post.
- [ ] No story paragraph reads machine-flat (4+ sentences all the same length,
      no clause doing work). Flag that paragraph only; never suggest adding
      variance as a tactic. A short post has no rhythm to flag.
- [ ] No staccato stacks ("Short. Punchy. Done.", "No X. No Y. Just Z."), no
      one-word paragraphs for drama, at most 2 standalone fragments in the
      post, no long/short/long/short seesaw.
- [ ] At least one odd-precision number WITH a named referent where the claim
      allows (a bare number does not clear this).
- [ ] At least one named entity.
- [ ] At most one natural rule-of-three; no stacked or perfectly parallel
      triads, no hollow triads without concrete items, never 3+ in a post.
- [ ] No hedging stack ("perhaps", "it seems", "we might be wrong but") and no
      framed confession ("We'll be honest, this was hard: ..."). A flat dated
      fact is fine.
- [ ] Rewrite audits only (original in hand to compare against): not
      over-scrubbed, i.e. the Page's tone, reactions, one em dash, one natural
      triad and a deliberate story post's length survived the rewrite. A fresh
      draft that never had an em dash or a triad is not over-scrubbed; never
      add one to clear this.
- [ ] One clear primary goal (shares / comments / reactions).
- [ ] Designed for a share or a comment, not just a passive Like.
- [ ] One idea per post.
- [ ] If it is a link post, the user knows it reaches fewer people organically.

## Thresholds quick reference

| Metric | Value |
|---|---|
| Engagement sweet spot | under 80 chars |
| Native post limit | 63,206 chars |
| Story-post guidance | under ~500 chars of substance |
| Hashtags | 0-2 |
| Emoji per post | 0-2 |
| Em dashes | about 1 per 100 words (0-1 short post, 1-2 story post) |
| Vocabulary / grammar markers per paragraph | 0-2 |
| Standalone fragments | 2 per post |
| Comment text limit | 8,000 chars |

## Scoring

- Any blocker -> **FAIL**, return fixes, offer auto-rewrite via `fb-humanizer`.
- No blockers, any warnings -> **PASS with warnings**, list each with a fix.
- Clean -> **PASS**, add the timing note and a short-vs-story sanity check.
- Report per-paragraph tell density (markers, em dashes per 100 words,
  fragments, triads). Do not estimate a detector score: on post-length text
  those are noise and this skill does not promise to beat them.
