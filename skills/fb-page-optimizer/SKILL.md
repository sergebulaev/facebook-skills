---
name: fb-page-optimizer
description: Audit and rewrite a Facebook Page for 2026: Page name, username and vanity URL, profile picture and cover photo, Intro/About and category, the CTA button (Shop, Book, Sign Up, Contact matched to your goal), pinned post, tabs order, and contact/link fields. Triggers on "review my Facebook Page", "fix my Page about", "optimize my cover", "set my CTA button", "Page audit". Converts a default Page into one that turns a visitor into a follower or a lead. Not for writing Page posts (use fb-post-writer).
---

# Facebook Page Optimizer

Audit the parts of a Facebook Page that decide whether a first-time visitor
follows the Page or takes the action you want, then rewrite each part that needs
it. On a Page the decision happens fast on the top card: Page name, profile
picture, cover photo, and the CTA button. The button is the whole point of a
Page. It converts a visitor into a follower or a lead. That is what this fixes.

## When to use

- User pastes their Facebook Page URL or name and asks for an audit
- "Fix my Page about", "rewrite my Intro", "what category should I pick"
- "Optimize my cover", "set my CTA button", "which button for a bakery"
- User is starting to post seriously and wants the Page to match
- Any of: "review my Facebook Page", "Page audit", "vanity URL"

Not for writing Page posts (use `fb-post-writer`), planning a week of them
(use `fb-content-planner`), or replying to comments (use `fb-engagement-drafter`).

## Input

- Page URL / @username (or a screenshot of the top card and About tab)
- Goal: **grow followers** / **capture leads** / **drive sales** / **build a
  community** - the CTA button, pinned post, and About all change by goal
- Optional: their best-performing posts, to pick a pin

## Output

1. **Scorecard** (9 parts, pass / needs-work / fail)
2. **Priority fixes** ranked by impact (CTA button and Intro first, always)
3. **Before -> After** rewrites for each failing part
4. **Pinned-post pick** with the reason

## Steps

1. **Intake.** Collect the Page state + goal. Note whether the Page has a
   custom @username yet and which CTA button is currently set.
2. **Score the 9 parts** against the scorecard below.
3. **Fix the CTA button.** Match it to the goal: **Shop Now** for sales,
   **Book Now** for appointments, **Sign Up** for leads or a list, **Contact
   Us / Send Message** for community and enquiries. One button, one job. A Page
   with the default "Like" and no CTA leaks every visitor who was ready to act.
4. **Rewrite the Intro / About.** Formula: `who you serve + what you offer +
   one proof or specific`. Lead with the value, not the founding date. The short
   Intro shows on the card, so front-load it; the longer About can carry hours,
   story, and location.
5. **Set the category.** Pick the most specific accurate category (e.g. "Bakery"
   over "Business"). Category drives discovery and unlocks the right fields
   (menu, hours, booking).
6. **Fix the Page name.** Clear brand name + optionally a searchable keyword
   people type (e.g. "Rivera Bakery - Fresh Sourdough"). Keep it stable; frequent
   renames trip Facebook's name-change review.
7. **Set the username / vanity URL.** Claim `facebook.com/YourBrand`. Short,
   matches the handle you use elsewhere, no numbers if avoidable. A raw numeric
   URL reads as unclaimed.
8. **Pick the pinned post.** Their single best proof of what a new follower
   gets: a top-performing post or a clear offer matched to the goal. No pin
   leaves the most valuable slot on the Page empty.
9. **Rewrite the cover photo brief.** One line of value prop, readable on mobile,
   not a busy collage. It reinforces the Intro, it does not repeat it. Note the
   safe zone so text is not cropped on phones.
10. **Profile picture check.** Logo or clear face, fills the frame, high contrast,
    recognizable at a small size. It appears next to every post the Page makes.
11. **Order the tabs / sections.** Surface the sections that serve the goal
    (Shop, Services, Reviews, Menu) near the top; bury the ones that do not.
12. **Fill contact + link fields.** Website, hours, address, phone, email as the
    category allows. One link matched to the goal; a link-hub if several are
    needed. Blank contact fields read as inactive.
13. **Deliver the before/after diff** + the two-second test: read only the Page
    name, Intro, and CTA button, and ask "would a stranger follow or click from
    this alone?"

## Nine-part scorecard

| # | Part | Pass criteria (2026) |
|---|------|----------------------|
| 1 | **CTA button** | Present and matched to the goal (Shop / Book / Sign Up / Contact), not the default with no action |
| 2 | **Intro / About** | Value + offer + proof; front-loaded Intro; longer About carries hours, story, location |
| 3 | **Category** | Most specific accurate category, unlocking the right fields (menu, hours, booking) |
| 4 | **Page name** | Clear brand + optional searchable keyword; stable, not recently renamed |
| 5 | **Username / vanity URL** | Custom `facebook.com/Brand` claimed, short, no avoidable numbers |
| 6 | **Pinned post** | Present, and it is their best proof matched to the goal, not a random recent post |
| 7 | **Cover photo** | One readable value-prop line, mobile-safe safe zone, reinforces (not repeats) the Intro |
| 8 | **Profile picture** | Logo or clear face, fills the frame, high contrast, recognizable small |
| 9 | **Tabs / sections + contact** | Goal-serving sections ordered up top; website, hours, address, and one goal-matched link filled |

## Hard rules

Global voice rules: see root `SKILL.md` Voice rules. Additional skill-specific rules:

- The Page must pass the two-second test: a stranger reading only Page name +
  Intro + CTA button should know who it is for and want to follow or click.
- The CTA button is chosen by the goal, never left on the default. One button,
  one job.
- Lead the Intro with the visitor's benefit, not the founding date or a mission
  statement.
- One specific or one number in the Intro where it fits.
- Keep every rewrite inside Facebook's limits. Never ship a truncated Intro.
- No em dashes. No "leverage", "fundamentally", "we are thrilled to announce".

## Related skills

- `fb-post-writer` - write the Page posts the optimized Page will host
- `fb-hook-extractor` - find a pin-worthy hook in a post that already worked
- `fb-content-planner` - plan the cadence that fills the Page
- `fb-engagement-drafter` - reply to the comments the Page earns
