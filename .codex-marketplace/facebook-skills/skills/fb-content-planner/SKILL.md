---
name: fb-content-planner
description: Generate a weekly Facebook Page content plan from a theme, audience, and content pillars. Produces per-day picks (short post vs story post, hook formula, angle, posting time, primary goal), a short-to-story post mix, a daily comment-reply target, and a share-optimized goal-mix balance check across shares, comments, and reactions. Use when the user wants to plan a week of Page content. Not for drafting one post (use fb-post-writer) or replying to comments (use fb-engagement-drafter).
---

# Facebook Page Content Planner

Produce a weekly Page plan built around a pillar discipline, a healthy short-to-
story post mix, and a share-optimized goal balance. Facebook rewards meaningful
interactions (comments and shares) over reactions, and short posts over long, so
the plan leads with short and designs for shares.

## When to use

- User asks "plan my week on Facebook" or "what should my Page post this week"
- User wants to escape ad-hoc posting and establish a rhythm
- Before a launch week (the plan aligns a product pillar)

## Input

- **Theme** (optional): e.g. "new spring menu launch"
- **Audience description:** e.g. "local families, weekend brunch crowd"
- **Pillar mix** (optional): defaults to 40% Value / 30% Community / 20%
  Behind-the-Scenes / 10% Promotion
- **Posting cadence** (optional): defaults to 1 post/day, 5-7 a week
- **Voice samples** (optional): past Page posts for voice calibration

## Output

A markdown plan with:

### 7-day calendar

| Day | Type | Pillar | Formula | 1-line angle | Goal | Time |
|---|---|---|---|---|---|---|
| Mon | short | Value | FB7 Useful Tip | "protect your first 90 minutes" | shares | 1:00 PM |
| Tue | short | Community | FB3 Ask-the-Page | "your weekend ritual?" | comments | 12:30 PM |
| Wed | story | Behind-the-Scenes | FB6 Behind-the-Scenes | "the 4am oven story" | reactions | 1:00 PM |
| Thu | short | Value | FB2 Tiny Number | "every message in 4 minutes" | shares | 1:30 PM |
| Fri | short | Community | FB4 This-or-That | "sweet or savory brunch?" | comments | 12:00 PM |
| Sat | story | Community | FB10 Spotlight | "Maria's launch story" | shares | 10:00 AM |
| Sun | short | Promotion | FB9 Announcement | "spring menu drops Monday" | shares | 11:00 AM |

(The skill fills real angles from the theme. Lead with short posts; story posts
are the exception, not the default.)

### Daily comment-reply target

For each day:
- **Reply to every comment in the first hour** where possible. On Facebook,
  replying fast is a ranking action, not just community management.
- **Template to apply** (C1 answer, C2 thank-plus-value, C3 handle-complaint, C4
  turn-into-share, C5 invite-spotlight) via `fb-engagement-drafter`.
- **Target:** clear the comment queue daily; prioritize questions and complaints
  first, then build on the positive ones (C4) to make threads shareable.

### Weekly balance check

- [ ] Short-to-story mix roughly 70/30 (lead short; the under-80 sweet spot is
      the engagement workhorse)
- [ ] At least 2 share-goal posts (shares are the reach multiplier on a Page)
- [ ] At least 1 comment-goal post (an easy question or this-or-that)
- [ ] At least 1 behind-the-scenes or community post (the human face)
- [ ] No pillar over 60% of the week's posts
- [ ] No formula repeated more than twice in the week
- [ ] Promotion pillar at most 1-2 posts
- [ ] Goal mix spread (see below): not every post chases the same signal

## Goal mix (balance the week)

Every formula earns a primary signal. A week that is all share-bait or all
question-bait reads as engineered. Spread the goals, but weight shares (the reach
multiplier):

| Goal | Formulas | Weekly target |
|---|---|---|
| Shares | FB1, FB2, FB7, FB8, FB9, FB10 | at least 2 (the reach multiplier) |
| Comments | FB3, FB4, FB8 | at least 1 |
| Reactions | FB5, FB6 | at least 1 |

## Rules

- **1 strong post a day, or 5-7 a week, beats burst posting.** Quality and
  meaningful interactions gate reach more than raw frequency.
- **Short-to-story mix ~70/30.** Short posts (under 80 chars) are the engagement
  workhorse; story posts are deliberate, for a launch, a real story, or a
  spotlight.
- **Comment replies are a content type, not an afterthought.** Block reply time
  daily; replying fast in the first hour lifts the post's reach.
- **Facebook often peaks early weekday afternoons.** Lunch and the 1-3 PM window
  are reliable; weekends suit community and relatable content.
- **Promotion pillar max 1-2 posts/week.** Overuse kills trust and reach.
- **Design for shares.** A share re-injects the post into a new network, the only
  organic way a Page exceeds its follower count.

## Formula -> pillar mapping

| Pillar | Preferred formulas |
|---|---|
| Value | FB1 One-Line Opinion, FB2 Tiny Number, FB7 Useful Tip |
| Community | FB3 Ask-the-Page, FB4 This-or-That, FB10 Spotlight |
| Behind-the-Scenes | FB5 Relatable, FB6 Behind-the-Scenes, FB8 Story Post |
| Promotion | FB9 Announcement, FB2 (your own data), FB10 (results that imply the product) |

## Steps

1. Gather inputs. Ask for theme, audience, pillar preferences if not provided.
2. Validate the pillar mix sums to 100%; warn if any pillar is over 60%.
3. For each day, pick: type (short/story), pillar, formula (do not over-repeat),
   angle, posting time (audience timezone), goal.
4. Add the daily comment-reply target with a suggested template.
5. Run the weekly balance check and the goal-mix check; flag anything missing.
6. Return as markdown, plus optional JSON for import.

## Example

See `references/example-week.md` for a filled-in 7-day plan.

## Files

- `SKILL.md` - this file
- `references/example-week.md` - worked 7-day plan
- `references/pillars-framework.md` - the Facebook Page pillar discipline explained

## Related skills

- `fb-post-writer` - draft each post from the plan
- `fb-engagement-drafter` - execute the daily comment-reply target
- `fb-hook-extractor` - study competitors' Pages while planning
- `fb-humanizer` - scrub each draft before it ships
