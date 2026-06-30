---
name: fb-engagement-drafter
description: Draft replies to comments on your Facebook Page's posts, in your Page voice. Use when the user pastes the comments under one of their Page posts and wants on-brand replies that earn more comments and shares. Drafts 1-3 variants per comment using proven templates (answer, thank plus add value, handle the complaint, turn it into a share). Publora has no Facebook comment endpoint, so every draft returns as a copy-paste block to post yourself. Not for writing top-level posts (use fb-post-writer).
---

# Facebook Page Engagement Drafter

Drafts replies to the comments on your Page's posts. Replying fast in the first
hour is a ranking action on Facebook, not just community management: a Page that
keeps the conversation alive gets more reach on that post. This skill drafts the
replies; you post them.

## The honest limitation

Publora has **no Facebook comment endpoint** (its comment and reaction endpoints
are LinkedIn-only), and `create-post` only creates new posts. So this skill
**cannot auto-post** a reply to a comment. Every draft comes back as a
copy-paste block for you to post in Facebook or Meta Business Suite by hand. This
is a documented limitation of the publish layer, not a missing feature here.

## When to use

- User pastes the comments under one of their Page posts and says "reply to these"
- A comment thread needs on-brand responses that keep the conversation going
- A complaint or question needs a careful, human reply

## Input

The Page post (for context) and the comments to reply to, pasted by the user,
since this bundle has no built-in Page reader. Optionally the Page post URL (for
the target link) and the Page's voice samples.

## Output

- 1-3 reply variants per comment, each in the Page's voice
- A short note on which template each variant uses and why
- An approval card. On approval, each reply is returned as a copy-paste block
  with the target post URL.

## Reply templates (`references/reply-templates.md`)

- **C1 Answer-the-Question** - they asked, you answer plainly plus one real detail
- **C2 Thank-Plus-Add-Value** - acknowledge, then add a useful extra (not a bare "thanks!")
- **C3 Handle-the-Complaint** - acknowledge, own it, offer the next step, take it to DM if needed
- **C4 Turn-It-Into-a-Share** - build on a positive comment so the thread itself becomes shareable
- **C5 Invite-the-Spotlight** - when a commenter shares a win, invite them to be featured (feeds FB10)

## Steps

1. **Parse the post URL** if given. `lib.url_parser.parse_facebook_url(url)`
   returns `page`, `post_id`, `canonical_url` for the target link.
2. **Read the context.** Ask the user to paste the post and the comments. Group
   the comments (questions, praise, complaints, wins).
3. **Pick a template per comment** using the table above.
4. **Draft 1-3 variants per comment.** Keep them short and human. Answer
   questions plainly with one real detail. For complaints, acknowledge first,
   never get defensive, offer a concrete next step.
5. **Humanizer pass.** Strip em dashes, AI vocab, canned "Thank you for your
   feedback!" corporate filler. Keep the Page voice.
6. **Approval card.** Show each comment, its drafted replies, the template used,
   and the target post URL.
7. **On approval.** Call `lib.publish(kind="comment", draft_text=<approved>,
   target_url=<canonical_url>)`. Because Publora has no Facebook comment
   endpoint, this always returns a copy-paste block. Paste each reply under the
   comment in Facebook or Meta Business Suite yourself.

## Hard rules

Global voice rules: see root `SKILL.md` Voice rules. Additional skill-specific
rules:

- Reply fast and human. The first hour matters for reach; a fast, real reply
  beats a slow, polished one.
- Never paste a canned "Thank you for your feedback!". Acknowledge with content
  or do not reply.
- On a complaint: acknowledge first, never argue in public, offer a next step,
  move details to DM. Comments are public and screenshot-able.
- Do not hard-sell in a reply. Help first; mention the product only if it
  genuinely answers the question.
- Keep replies under a few short lines. A Page reply is not a press release.

## Example

> User: "Reply to these comments on my post:
> https://www.facebook.com/MyBakery/posts/123. Comments: 'Are you open Sunday?'
> and 'Best sourdough in town!'"
>
> Skill: parses -> page MyBakery, post 123. Drafts a C1 Answer-the-Question reply
> to the first ("We are, 8 to 2 on Sundays. Come hungry.") and a C4
> Turn-It-Into-a-Share reply to the second ("That means a lot. The Saturday batch
> is the one to beat, ask for it warm."). Shows the approval card.
>
> User: "post both"
>
> Skill: returns each reply as a copy-paste block with the post URL, since
> Publora has no Facebook comment endpoint. User pastes them in Facebook.

## Files

- `SKILL.md` - this file
- `references/reply-templates.md` - 5 comment-reply templates with examples

## Related skills

- `fb-post-writer` - for a standalone Page post rather than a reply
- `fb-humanizer` - scrub a reply before posting
- `fb-content-planner` - sets the daily comment-reply target this skill executes
