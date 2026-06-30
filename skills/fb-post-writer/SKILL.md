---
name: fb-post-writer
description: Draft a short punchy Facebook Page post, or a longer story post, using a 2026 Facebook hook formula (one-line opinion, tiny number, ask-the-page question, this-or-that, useful tip, story post) picked by goal (shares, comments, reactions). Favors the under-80-character engagement sweet spot, runs the humanizer pass, and publishes via Publora on approval. Use to write a Page post from notes. Not for replying to comments (use fb-engagement-drafter) or auditing a draft (use fb-humanizer).
---

# Facebook Page Post Writer

Ship a short punchy Page post, or a longer story post when the material earns it,
using hook shapes that actually travel on a Facebook Page in 2026. The single
highest-engagement move on a Page is the short post: posts under 80 characters
get a reported ~66% engagement lift, so this skill leads short and only goes long
on purpose.

## When to use

- User says "write me a Facebook Page post about X"
- User has a topic or a rough line and wants a sharper, shorter hook
- User wants to pick a proven Page-post shape and fill in their voice
- User wants a quick draft that auto-publishes on approval

## Formulas this skill uses

| Code | Formula | Primary goal | Best for |
|---|---|---|---|
| FB1 | One-Line Opinion | shares | a sharp, defensible take in one short line |
| FB2 | The Tiny Number | shares | one concrete number that reframes a thing |
| FB3 | Ask-the-Page Question | comments | an easy, fun question the audience answers |
| FB4 | This-or-That | comments | a friendly binary choice readers pick a side on |
| FB5 | Relatable One-Liner | reactions | a specific shared moment, no setup |
| FB6 | Behind-the-Scenes | reactions | a real human moment inside the business |
| FB7 | Useful Tip | shares | one usable tip the reader passes on |
| FB8 | Story Post with a Turn | shares | a longer true story with a quotable turn |
| FB9 | Announcement with Stakes | shares | a launch or news, led human not corporate |
| FB10 | Community Spotlight | shares | featuring a real customer or team member |

Full skeletons in `../../references/hook-formulas.md`. FB1-FB7 are short-post
shapes (lead here). FB8-FB10 are longer story shapes (use on purpose).

### Pick by goal first

| Goal | Reach for |
|---|---|
| Shares | FB1, FB2, FB7, FB8, FB9, FB10 |
| Comments | FB3, FB4, FB8 |
| Reactions | FB5, FB6 |

## Steps

1. **Gather inputs.** Topic, angle, any rough draft, target audience (B2C / B2B /
   local / community), and the goal (shares / comments / reactions).
2. **Pick the container.** Default to a short post (aim under 80 chars). If it is
   one opinion, number, question, or moment, it stays short. Only escalate to a
   story post (FB8-FB10) if the idea is a true narrative, a real launch, or a
   spotlight that needs room.
3. **Pick the formula.** Use the goal table to shortlist, then suggest 2-3 that
   also fit the topic and let the user choose.
4. **Draft the post.** Fill the skeleton in the user's voice. Respect the 2026
   Facebook rules:
   - Lead short. Try to land the whole point under 80 chars.
   - First line carries the post (Facebook folds longer posts behind "See more").
   - One idea per post. Line breaks as beats.
   - 0-2 hashtags, 0-2 emoji, none on a serious take.
   - If the post includes a link, write framing text above it (Facebook builds a
     preview card) and warn that link posts reach fewer people organically.
5. **Humanizer pass.** Strip em dashes, AI vocab, "We are thrilled to announce",
   rule-of-three, corporate auto-pilot. Add a specific number or named entity
   where the claim allows it.
6. **Optional audit.** Invoke `fb-humanizer --mode audit` for a pass-fail check.
7. **Approval card.** Show: formula used, full draft, char count (flag if it
   crosses the 80-char sweet spot), suggested posting window, primary goal.
8. **On approval.** Call `lib.publish(kind="post", draft_text=<approved>,
   target_url="https://www.facebook.com/YourPage", platforms=[<FACEBOOK_PLATFORM_ID>],
   scheduled_time=<iso_or_None>)`. For a deliberate long story post, pass
   `kind="story"`. The wrapper handles Publora / manual / diy routing.

## Hard rules

Global voice rules: see root `SKILL.md` Voice rules. Additional skill-specific
rules:

- Lead short. Default to under 80 chars; that is the engagement sweet spot. A
  long post is a deliberate choice for a story, not the fallback.
- The first line must carry the post on its own (everything above the "See more"
  fold).
- One specific number where the claim allows it. "4 minutes" beats "fast".
- Never open with "We are thrilled / excited / delighted to announce".
- Do not beg for engagement. Earn the share or comment with the post itself.

## Anti-patterns (skill will refuse)

- "We are thrilled to announce.." and every variant.
- Engagement bait ("LIKE and SHARE if you agree", "comment YES", "tag 3 friends").
- Em dashes anywhere.
- Padding a one-line idea into five paragraphs.
- Rule-of-three lists without specifics.
- "leverage", "fundamentally", "game-changer", "deep dive".
- A bare external link with no framing text.
- 5+ hashtags stuffed at the bottom.

## Resources

- `../../references/hook-formulas.md` - all 10 Facebook formula skeletons (FB1-FB7 short, FB8-FB10 story)
- `../../references/algorithm-heuristics.md` - 2026 Facebook Page ranking rules (signals, the under-80 boost, timing, limits)
- `references/short-post-checklist.md` - the per-post scrub and the under-80 fit check

## Related skills

- `fb-humanizer` - aggressive AI-tell scrubber, plus `--mode audit` for review
- `fb-hook-extractor` - reverse-engineer a hook from a Page post you admire
- `fb-content-planner` - plan a week of these posts
- `fb-engagement-drafter` - reply to the comments your post earns
