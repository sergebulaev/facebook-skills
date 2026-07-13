---
name: fb-repurposer
description: Repurpose existing content into a native Facebook Page post. Take a LinkedIn post, X thread, blog, or newsletter and rewrite it for a Page: warm the tone, lead with a standalone claim before the "See more" fold, move links to the first comment, strip off-platform artifacts (hashtag walls, "link in bio", @-handles), then humanize and publish via Publora on approval. Not for writing from scratch (use fb-post-writer), auditing a draft (use fb-humanizer), or comment replies (use fb-engagement-drafter).
---

# Facebook Repurposer

Turn something you already made into a Page post that reads like it was born on
Facebook. Repurposing is not copy-paste. A post that killed on LinkedIn will die
on a Facebook Page if you paste it: wrong tone (corporate press release vs warm
Page voice), wrong length, links that suppress reach, and artifacts (hashtag
walls, "link in bio", X @-handles) that scream off-platform.

This skill transforms, it does not generate. It reads your source, keeps the
idea, and rebuilds the delivery for a Facebook Page.

## When to use

- "Turn this LinkedIn post into a Facebook Page post"
- "Repurpose my blog post / newsletter / X thread for our Page"
- "This worked on Threads, adapt it for Facebook"
- "I have a rough idea in another format, make it native here"

Not for a blank-page draft (use `fb-post-writer`), not for reviewing an
already-Facebook draft (use `fb-humanizer --mode audit`), and not for replying to
comments on your Page (use `fb-engagement-drafter`).

## How it works

1. **Take the source.** Any format: a post, a paragraph, a script, a caption, a
   transcript, a bullet list, a link to read. Ask for the source and the goal
   (shares / comments / reactions) if not given.
2. **Extract the spine.** Strip the source platform's shell and pull out the one
   claim, the one story, or the one number worth keeping. Most repurposing fails
   because it keeps the words instead of the point.
3. **Choose the container.** One claim, number, or moment -> a short Page post
   (aim under 80 chars). A true narrative or a build -> a story post (FB8-FB10
   shapes). Match the source to a 2026 Facebook shape in
   `../../references/hook-formulas.md`, picked by the goal.
4. **Warm the tone for a Page.** A Page voice is warm and human, not a press
   release and not clickbait. Rewrite the source's hook: lead with a standalone
   claim that lands the whole point above the "See more" fold. Facebook folds
   longer posts, so line one must carry it alone.
5. **Refit the format.** Lead short. One idea per post, line breaks as beats. Cut
   the source's connective tissue and corporate throat-clearing. 0-2 hashtags,
   0-2 emoji, none on a serious take.
6. **Move links off the body.** External links suppress organic reach on a Page.
   If the source's whole point is a link, put the link in the first comment and
   let the post stand on its own claim.
7. **Strip off-platform artifacts.** Remove "link in bio", "smash subscribe",
   "read more below", hashtag walls, X @-handles that only exist elsewhere, and
   any "as I posted on LinkedIn" throat-clearing. A repurposed post should not
   admit it was repurposed.
8. **Humanizer pass.** Run `fb-humanizer` on the draft: em dashes, AI vocab,
   rule-of-three, "We are thrilled to announce", generic openers. Keep the user's
   real numbers and named entities from the source.
9. **Approval card.** Show: source -> Facebook mapping (what became what), the
   container (short post or story post), shape used, char count (flag if it
   crosses the 80-char sweet spot), whether a link moved to the first comment,
   primary goal.
10. **On approval.** Publish via `lib.publish(kind="post", draft_text=<approved>,
    target_url="https://www.facebook.com/YourPage",
    platforms=[<FACEBOOK_PLATFORM_ID>], scheduled_time=<iso_or_None>)`. For a
    deliberate long story post, pass `kind="story"`. The wrapper handles Publora /
    manual / diy routing.

## Native-fit rules (source -> Facebook)

- **LinkedIn post -> Facebook:** warm the corporate tone. LinkedIn tolerates a
  thought-leadership register; a Page wants a human talking to people. Drop the
  buzzwords, keep the insight.
- **X thread -> Facebook:** unroll into one short story post. A Page reads a
  numbered thread as noise, so stitch the beats into a single readable arc and
  cut the "1/", "2/" scaffolding and @-handles.
- **Blog / newsletter -> Facebook:** pick the one relatable angle, not a summary.
  Lead with the human moment or the single most useful line; let the link (if
  any) live in the first comment.
- **YouTube script -> Facebook:** lead with the payoff, not the intro. "Here is
  what we found" beats "In this video".
- **Instagram / TikTok caption -> Facebook:** strip emoji density and hashtag
  blocks; a Page reads them as clutter. Keep the one line that carries.

## Hard rules

Global voice rules: see root `SKILL.md` Voice rules. Additional skill-specific
rules:

- Keep the source's **claim and facts** intact. Repurposing changes the delivery,
  never the meaning or the numbers.
- The first line must land the whole point above the fold, on its own.
- Never paste the source verbatim and trim. Rebuild the hook and tone from the
  spine.
- One specific number where the source offers one. Keep it.
- Warm and human, never a press release and never "You won't BELIEVE" clickbait.
- No tag-bait ("tag 3 friends"). Earn the share with the post.
- Links move to the first comment. The body carries the claim.

## Anti-patterns (skill will refuse)

- Copy-pasting the source with light edits (that is not repurposing).
- Keeping the source platform's artifacts ("link in bio", "smash subscribe",
  hashtag walls, X @-handles, "1/ 2/" thread numbering).
- "You won't BELIEVE" clickbait or ALL CAPS for intensity.
- Engagement bait ("LIKE and SHARE if you agree", "tag 3 friends").
- Em dashes anywhere.
- Rule-of-three lists without specifics.
- "leverage", "fundamentally", "game-changer", "deep dive".
- A bare external link in the post body (move it to the first comment).
- Meta throat-clearing ("I originally posted this on...").

## Resources

- `../../references/hook-formulas.md` - the 10 Facebook shapes to re-hook with (FB1-FB7 short, FB8-FB10 story)
- `../../references/algorithm-heuristics.md` - 2026 Facebook Page ranking rules (the under-80 boost, link reach suppression, timing, limits)

## Related skills

- `fb-post-writer` - write a fresh Page post from scratch
- `fb-humanizer` - scrub AI tells, plus `--mode audit` to review the result
- `fb-hook-extractor` - reverse-engineer a hook from a Page post you admire
- `fb-engagement-drafter` - reply to the comments your post earns
