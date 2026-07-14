---
name: fb-audience-insights
description: Read a Facebook Page and its audience from real data. Pull any Page's public stats (yours or a competitor's): followers, likes, categories, intro, websites. And pull the commenters on a public Page post, since Facebook hides the reactor and liker roster and shows counts only, so commenters are the signal. Powered by Apify, no login. Triggers on "analyze my Page", "competitor Page stats", "who is commenting", "read the comments", "audience insights". Not for writing Page posts (use fb-post-writer).
---

# Facebook Audience Insights

Turn real Facebook data into a read on a Page and its audience: how big it is, what it is about, and who is actually engaging in the comments. This is the read layer, so the skill sees actual numbers instead of guessing.

One honest limit: Facebook hides the roster of who **reacted** to (liked) a post. It shows reaction counts, never a reactor list. The engagement signal here is **commenters + Page stats**, which is where the real conversation lives anyway. This reads commenters, not likers, on purpose.

## When to use

- "Analyze my Page / how is my Page doing"
- "Pull the stats on this competitor Page"
- "Who is commenting on this post"
- "Read the comments on this Page post"
- "Size up [a Page] before I pitch / benchmark against it"

Not for writing a Page post (use `fb-post-writer`) or drafting comment replies (use `fb-engagement-drafter`).

## Setup (optional)

The read layer uses **Apify** (no login, no cookies). Get a free token at `https://console.apify.com/account/integrations` and set `APIFY_TOKEN`. No token? Paste the Page stats or the comments you already have and the skill runs the same analysis on them.

## Input

- A Facebook Page URL (yours or a competitor's), or
- A public Page-post URL (or a bare `pfbid` post id) to read its commenters

## Output

1. **Page read** - the Page's title, category, followers, likes, and intro, with a one-line take on positioning and size
2. **Commenter read** - who commented on a post, recurring questions or themes, commenters worth a reply or a follow
3. **Competitor read** - the same Page stats for a rival, so you can benchmark follower size, category, and how they describe themselves
4. **Action list** - what to write more of, whose comments to reply to, which Page angle to borrow

## Steps

1. **Pull the data.** For a Page: `lib.ApifyClient().fetch_page_stats(page_url)`. For a post's commenters: `fetch_post_commenters(post_url, max_comments=25)`. Falls back to pasted data if no token.
2. **Read the Page.** Report followers, likes, category, and intro. Compare a competitor's numbers to the user's own Page to size the gap honestly (a bigger follower count is context, not destiny).
3. **Read the commenters.** Cluster comments into questions, agreement, and pushback. Recurring questions are content ideas; commenters with substance are reply candidates. Sort by `reactions` and `replies` to surface the comments that themselves traveled.
4. **Be honest about the wall.** Facebook does not expose who reacted or liked. Never present a "top likers" list. If the user asks for likers, explain the platform limit and pivot to commenters.
5. **Build the action list.** Write-more-of (angles the audience responds to), engage (specific commenters to reply to), borrow (a competitor Page's positioning move). Route drafts to `fb-post-writer` / `fb-engagement-drafter`.
6. **Deliver the report** in the Output shape, with the raw Page stats and ranked comments attached.

## What the read layer exposes

| Method | Returns |
|---|---|
| `fetch_page_stats(page_url)` | Page stats: title, page_name, page_id, followers, likes, categories, intro, websites, email, profile/cover photo urls |
| `fetch_post_commenters(post_url, max_comments)` | commenters on a post: author, author_id, message, reactions, replies, depth, is_reply (the engagement signal, since reactors/likers are hidden) |

Both are verified live against `apify/facebook-pages-scraper` and `danek/facebook-comments-ppr`.

## Hard rules

Global voice rules: see root `SKILL.md` Voice rules. Additional skill-specific rules:

- Be honest that this reads **commenters, not likers** (Facebook hides the reactor roster). Never imply a full liker or reactor list exists.
- **Compare against the user's own Page** before calling a competitor "ahead" or "behind". Raw follower count without context misleads.
- Never invent a Page stat, a follower number, a comment, or a commenter name. If a Page or post returns nothing (private, comments off, share link that hides ids), say so and ask the user to paste.
- A theme is only a theme if it recurs across several comments, not one.
- Page stats are a public snapshot, not private Insights (no reach, no demographics). Do not present them as Meta Business Suite Insights.

## Related skills

- `fb-post-writer` - write more of what the read shows the audience responds to
- `fb-engagement-drafter` - reply to a commenter the read surfaced
- `fb-hook-extractor` - reverse-engineer a hook from a competitor's high-share post
- `fb-content-planner` - feed the winning angles into a weekly plan
- `fb-page-optimizer` - borrow a competitor Page's positioning into your own Page setup
