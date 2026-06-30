# 2026 Facebook Page Posting Heuristics

Synthesized from Meta's public statements on the Facebook feed ranking, the
"meaningful social interactions" (MSI) framework, and observed Page creator data.
Numbers marked "reported" are community-measured, not officially confirmed.

## Signal weights (relative reach impact)

Facebook's feed ranker scores predicted engagement, and the engagement types are
not equal. Reported relative weights for Page content:

| Signal | Relative weight | Note |
|---|---|---|
| **Share** (esp. to a feed, not just Messenger) | highest for reach | re-injects the post into a whole new network |
| **Comment** (esp. a real reply, and Page replying back) | highest "meaningful interaction" | a conversation is the strongest on-post signal |
| **Comment reply / thread depth** | high | back-and-forth tells the ranker the post sparked discussion |
| **Reaction: Love / Care / Haha / Wow / Angry / Sad** | medium | weighted above a plain Like since they take more intent |
| **Plain Like** | low | cheap affirmation, light reach |
| **Link click / dwell** | medium | counts, but link posts can suppress organic reach |
| **Negative: Hide post, "See fewer", unfollow, report** | heavy penalty | one hide outweighs many Likes |

Takeaway: optimize for **shares and comments** (the meaningful interactions), not
reactions. Reactions are social proof for the next reader but barely move
distribution. Shares are the reach multiplier.

## The short-post engagement boost

- **Posts under 80 characters get a reported ~66% more engagement** than longer
  posts. This is the single most actionable Page heuristic: lead with short.
- Short posts beat long ones because they read fully in the feed without a "See
  more" tap, and they are easier to react to and share on mobile.
- Long story posts still have a place (FB8 / FB9 / FB10), but they are a
  deliberate choice, not the default. When you go long, the first line still has
  to earn the "See more" tap.

## The first 60-90 minutes

- The opening window sets the trajectory. Early comments and shares tell the
  ranker to widen distribution.
- **Reply to early comments fast.** The Page replying back on a comment is a
  strong meaningful-interaction signal and pulls the conversation up.
- A handful of substantive comments in the first hour earns a second
  distribution test. A post that only collects silent Likes plateaus.

## Reach suppressors (avoid)

- **Engagement bait** ("LIKE and SHARE if you agree", "comment YES", "tag 3
  friends") is explicitly downranked by Meta, not rewarded.
- **External links** can suppress organic reach, because Facebook prefers to keep
  users in-feed. A link post still works for traffic, but expect lower organic
  reach than a native text, photo, or video post. Put the framing in the text;
  do not post a bare URL.
- **Repeated near-duplicate posts** (the same post reworded) trip a similarity
  penalty.
- **High hide/unfollow/report rate** collapses distribution fast and is slow to
  recover from.
- **Too many hashtags.** Zero to two is native on a Page; five or more reads as
  spam and does nothing for discovery.
- **"We are thrilled to announce" corporate auto-pilot** does not earn the
  meaningful interactions the ranker needs to push the post.

## Reach amplifiers

- **Native video** is favored, especially video that holds watch time. Upload
  directly to Facebook; do not link out to YouTube.
- **Photos and albums** out-reach bare link posts. A short text post with one
  strong image is a reliable Page workhorse.
- **Shares to feed** are the compounding lever. A post designed to be passed on
  (a clean opinion, a useful tip, a quotable number) reaches past your follower
  count.
- **Conversation the Page keeps alive** by replying compounds reach over hours.
- **Consistency.** Pages that post on a steady cadence get more reliable
  distribution than Pages that post in bursts.

## Character and media limits

| Item | Limit |
|---|---|
| Post text (native) | 63,206 characters |
| Engagement sweet spot | under 80 characters (~66% more engagement, reported) |
| Comment text | 8,000 characters |
| Images per post | up to 10 (carousel / album) |
| Image size (API) | 10 MB (PNG recommended under 1 MB to avoid pixelation) |
| Image formats | JPEG, PNG, GIF, BMP, TIFF (WebP auto-converted to JPEG) |
| Video duration (API) | 45 minutes (Facebook native allows up to 4 hours) |
| Video size | 2 GB via the API (Publora server limit is 512 MB; native is 4 GB) |
| Video formats | MP4, MOV |
| Reels (API) | up to 90 seconds, Pages only, 30 Reels/day/Page |

- A single post can contain **either images or a video, not both**. This is a
  Facebook limitation.
- If post text includes a URL, Facebook **auto-generates a link preview card**.
  Write the text to stand on its own above it.

## Post types

| Type | When to use | Reach note |
|---|---|---|
| **Text only** | quick opinions, questions, tips (allowed and common on Pages) | strong for short, conversational posts; the under-80 sweet spot lives here |
| **Photo / album** | a moment, a product, behind-the-scenes | reliably out-reaches a bare link post |
| **Native video / Reel** | demos, stories, anything that holds attention | favored by the ranker; keep the first 3 seconds strong |
| **Link post** | driving traffic off-platform | lower organic reach; frame it well in the text |

Unlike Instagram, TikTok, and YouTube, **a Facebook Page text-only post is fully
supported** and is often the best-performing shape. You do not need media to
post.

## Shares are the underrated lever

- A share re-injects the post into the sharer's network, which is the only
  organic way a Page post meaningfully exceeds its follower count.
- Shares are to a Facebook Page what saves are to Instagram: the high-intent
  signal that compounds reach. Design for them.
- Share-bait that works (not the begging kind): a clean opinion (FB1), a useful
  tip (FB7), a hard number (FB2), a quotable story ending (FB8), a generous
  spotlight (FB10).

## Timing

| Audience | Best windows (local) |
|---|---|
| General consumer / B2C Page | weekdays 9-11 AM and 1-3 PM; weekday lunch is strong |
| B2B / professional Page | Tue-Thu mid-morning |
| Broad / mixed | early afternoon on weekdays tends to peak on Facebook |

- Weekday early afternoon is a reliable Facebook peak for many Pages, which
  differs from X (mornings) and LinkedIn (early weekday AM).
- Weekends work for lighter, relatable, and community content (FB5, FB6, FB10).
- Posting cadence: 1 strong post a day, or 4-7 a week, beats burst posting.
  Quality and meaningful interactions gate reach more than raw frequency.

## Comments are publishing, not just engagement

- Replying to comments on your Page posts is a ranking action, not just
  community management. A Page that replies fast in the first hour gets more
  reach on that post.
- Publora has **no Facebook comment endpoint** (comment and reaction endpoints
  are LinkedIn-only). So the `fb-engagement-drafter` skill drafts comment
  replies and hands them back as a copy-paste block to post in Facebook or Meta
  Business Suite by hand. This is a documented limitation, not an oversight.

## Pre-publish checklist

- [ ] Leads short where possible (under 80 chars is the engagement sweet spot).
- [ ] First line carries the post (everything above the "See more" fold).
- [ ] No em dashes (`—`), en dashes (`–`), or double dashes (`--`).
- [ ] No AI vocabulary blacklist words (leverage, fundamentally, delve, etc.).
- [ ] No "We are thrilled to announce" or corporate auto-pilot opener.
- [ ] At least one specific number where the claim allows it.
- [ ] 0-2 hashtags, 0-2 emoji, and only where each earns its place.
- [ ] No engagement bait ("LIKE and SHARE", "comment YES", "tag 3 friends").
- [ ] A clear primary goal (shares / comments / reactions), not all at once.
- [ ] Designed for a share or a comment, not just a passive Like.
- [ ] Close is a landing or a specific question, not "What do you think?".
