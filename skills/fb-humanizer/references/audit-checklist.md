# Pre-Publish Audit Checklist (Facebook Page)

The thresholds the `--mode audit` pass applies. Mirror of the root
`references/algorithm-heuristics.md` checklist, with the humanizer's blocker
distinctions.

## Blockers (auto-fail)

- [ ] No em dash (`—`), en dash (`–`), or double dash (`--`).
- [ ] No "We are thrilled / excited / delighted to announce" or equivalent
      corporate opener.
- [ ] No engagement bait ("LIKE and SHARE if you agree", "comment YES", "tag 3
      friends").
- [ ] No "What do you think?" / "Thoughts?" dead closer.
- [ ] No AI vocabulary blacklist words.
- [ ] First line stands alone as a hook (everything above the "See more" fold).
- [ ] No bare external link with zero framing text.

## Warnings (flag with fix)

- [ ] Leads short. If the point fits under 80 chars, the short version is offered
      (the under-80 sweet spot is ~66% more engagement, reported).
- [ ] 0-2 hashtags, at the end.
- [ ] 0-2 emoji, none on a serious post.
- [ ] At least one specific number where the claim allows.
- [ ] At least one named entity.
- [ ] No rule-of-three list without concrete items.
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
| Comment text limit | 8,000 chars |

## Scoring

- Any blocker -> **FAIL**, return fixes, offer auto-rewrite via `fb-humanizer`.
- No blockers, any warnings -> **PASS with warnings**, list each with a fix.
- Clean -> **PASS**, add the timing note and a short-vs-story sanity check.
