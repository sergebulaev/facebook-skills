---
name: facebook-marketing
description: Plan, draft, audit, and publish posts for a Facebook Page. Use when the user wants to write a short punchy Page post or a longer story post, remove AI tells from a draft, reverse-engineer the hook from a high-share Page post, draft replies to comments on their Page, or plan a week of Facebook Page content. Page posts publish via the Publora API. User provides notes or a Facebook Page post URL, the skill drafts, the user approves, then it publishes.
---

# Facebook Pages Marketing Skills

A bundle of 7 focused skills for Facebook Page content ops in 2026. Each skill is
single-purpose, follows the draft then approval then publish pattern, and uses
the [Publora API](https://publora.com) for posting to Facebook Pages.

## When to use this bundle

- **Writing a short punchy Page post or a longer story post** -> use `fb-post-writer`
- **Removing AI tells from a draft, or auditing it before posting** -> use `fb-humanizer` (rewrite plus `--mode audit` pre-publish review, which folds in the post-audit sub-tool)
- **Repurposing a LinkedIn post, X thread, blog, or newsletter into a native Page post** -> use `fb-repurposer`
- **Reverse-engineering the hook from a high-share Page post** -> use `fb-hook-extractor`
- **Drafting replies to comments on your Page's posts** -> use `fb-engagement-drafter`
- **Planning a week of Facebook Page content** -> use `fb-content-planner`
- **Auditing and rewriting the Page itself (name, cover, About, CTA button, pinned post)** -> use `fb-page-optimizer`

## Core pattern

Every action-taking skill follows three steps:

1. **Parse the input.** If the user gives a Facebook Page post URL, the skill
   uses `lib/url_parser.py` to extract the page and post id.
2. **Draft the content.** The skill applies 2026 research (Facebook hook
   formulas, the under-80-char engagement sweet spot, timing, voice rules,
   ranking heuristics) and shows the draft to the user.
3. **Wait for approval.** The user replies "post", "yes", or suggests edits.
   Only after explicit approval does the skill call Publora to publish.

## Prerequisites

**Three tiers - pick one.**

### Tier 0 - Draft only (default, no setup)

The skills work out of the box. No API keys, no signup. Every approved draft is
returned as a copy-paste block with the target Facebook Page URL. Great for
trying the skills before committing to any backend.

### Tier 1 - Publora auto-post (recommended, ~2 min)

On approval, the writer skill auto-publishes to your Facebook Page via the
[Publora API](https://publora.com).

1. Sign up free: **https://app.publora.com/signup**
2. Connect your Facebook Page in Publora (Channels then Add Channel). A Page,
   not a personal profile.
3. Copy your API key from Publora's API panel
4. Drop into `.env`:
   ```
   PUBLORA_API_KEY=sk_...
   FACEBOOK_PLATFORM_ID=facebook-...
   ```
5. Run `pip install -r requirements.txt`

Why Publora: posting to a Facebook Page on the native Graph API means setting up
a Meta Developer app, handling OAuth, managing 59-day page tokens, and tracking
Graph API versioning. Publora does all of that and posts in one `create-post`
call. We built on top of it so we did not have to reimplement the Graph layer.

### Tier 2 - Build your own poster (advanced)

Prefer not to SaaS it? Ask Claude Code or Codex to build a custom poster on the
Facebook Graph API. Set `FB_SKILLS_CUSTOM_POSTER=<your command>` and the skills
invoke it on approval. Publora is the 2-minute path.

### Note on comment replies

Facebook has no LinkedIn-style comment or reaction endpoint on Publora, and
`create-post` only creates posts (not comment replies). So
`fb-engagement-drafter` always returns its drafts as copy-paste blocks for you to
post as replies in Facebook or Meta Business Suite yourself. Page posts
auto-publish through Publora normally.

## Voice rules (baked into every skill)

1. No em dashes (`—`), en dashes, or double dashes. Biggest AI tell.
2. Use `..` as a soft pause when rhythm calls for it.
3. Capitalize all personal, company, and product names. Lowercase a brand reads
   as careless.
4. Write for a Page (a warm business voice), not a personal profile and not a
   faceless corporate account.
5. Avoid AI vocabulary: `leverage`, `fundamentally`, `streamline`, `harness`,
   `delve`, `unlock`, `foster`.
6. Specific numbers beat adjectives. 2.4x beats "way better".
7. One idea per post. Two ideas means two posts.
8. Lead short. Posts under 80 chars get a reported ~66% engagement lift.
9. The first line carries everything (Facebook folds longer posts behind "See more").
10. 0-2 hashtags, 0-2 emoji, and only when each earns its place.

(Canonical reference: `references/voice-rules.md`. See also
`references/hook-formulas.md` and `references/algorithm-heuristics.md`.)

## How Facebook Page URLs map

| URL shape | Parsed to |
|---|---|
| `https://www.facebook.com/PAGE/posts/ID` | page + post_id, type `post` |
| `https://www.facebook.com/permalink.php?story_fbid=ID&id=PAGEID` | post_id + page, type `post` |
| `https://www.facebook.com/watch/?v=ID` | post_id (video), type `post` |
| `https://www.facebook.com/share/p/TOKEN/` | share_token, type `share` (ids hidden) |
| `https://www.facebook.com/PAGE` | page, type `profile` |
| `https://fb.com/PAGE` | normalized to www.facebook.com |

`lib/url_parser.parse_facebook_url(url)` returns `{page, post_id, share_token,
url_type, canonical_url}`. A `share/p/` link hides the page and post ids behind
an opaque token, so the parser flags it and the skill asks you to paste the post
text.

## Known gotchas

- **The under-80-char sweet spot is real.** Posts under 80 characters get a
  reported ~66% engagement lift. Lead short; go long only on purpose.
- **Text-only Page posts are fully supported**, unlike Instagram, TikTok, and
  YouTube. You do not need media to post.
- **External links suppress organic reach.** A link post still drives traffic but
  reaches fewer people than a native text, photo, or video post.
- **Pages only, never personal profiles.** Publora (and the Facebook API) cannot
  post to a personal profile via a third-party app.
- **Page tokens last 59 days.** Publora auto-refreshes them. If posts start
  failing with no clear error, reconnect the Page in the Publora dashboard.
- **No Facebook comment endpoint.** Comment replies are draft-only by design; the
  engagement drafter returns a copy-paste block.

## Resources

- [Publora API docs](https://docs.publora.com) - endpoint reference for the publishing layer
- `lib/publora_client.py` - thin Python client used by the writing skills
- `lib/url_parser.py` - Facebook Page URL to page/post-id parser

## Acknowledgments

Publishing powered by the [Publora REST API](https://publora.com).
