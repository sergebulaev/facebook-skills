---
name: fb-humanizer
description: 'Remove the AI tells readers react to in a Facebook Page post: 2026 vocabulary by density, reveal bridges, staccato stacks, stacked triads, performed sincerity, "We are thrilled to announce" auto-pilot; caps em dashes. Includes --mode audit (under-80 sweet spot, hook, engagement bait, hashtag and emoji limits) and --mode profile. Not for beating AI detectors (no edit reliably does). Not for writing from scratch (use fb-post-writer). Keywords: humanize, de-AI my post, audit before posting.'
---

# Facebook Page Humanizer V3

Rewrites any Facebook Page post to remove the AI tells that human readers
notice, and audits a finished draft against the 2026 Facebook ranking
checklist. Based on Wikipedia's "Signs of AI writing" taxonomy, the 2025-2026
stylometry literature, and Facebook-Page-specific patterns (the under-80
sweet spot, the "See more" fold, the "We are thrilled to announce" corporate
tell, and the meaningful-interactions model). **V3 (2026-09):** recalibrated
on 2026 evidence. Vocabulary is scored by density, em dashes are capped
instead of banned, forced rhythm is now a tell instead of a fix, and there is
an over-correction guard. Facebook has no corpus of its own yet, so the
calibration follows the LinkedIn one (the closest long-and-short mixed feed).

**What this skill does not do:** it does not make text "pass" GPTZero,
Pangram, Turnitin or Originality. Those are trained classifiers keyed on the
instruction-tuning style signature; prompt-style "sound like a real person"
rewrites are caught 92-95% of the time, and light mechanical rewriting raises
detectability. On post-length text (under 300 words) detector scores are
noise. The real value is elsewhere: expert human readers cite vocabulary (53%)
and sentence structure (36%) as what gives AI text away, and a Page post that
reads as a bot earns neither the share nor the comment Facebook's
meaningful-interactions model ranks on. This skill removes what those readers
react to.

## What changed in V3

Evidence tier in brackets: [strong] = replicated across 2+ independent
2025-2026 studies or our own corpus on sibling platforms; [vendor] = single
platform or vendor dataset; [weak] = one study or expert-panel report.

- **Vocabulary moved from a delete-list to density scoring.** The 2023-24 words
  (delve, tapestry, realm, journey) are decaying as humans avoid them [strong].
  The durable 2026 markers are common words (significant, crucial, notably,
  comprehensive, insights, robust, leverage, foster, landscape, nuanced,
  streamline, elevate) plus grammar: nominalisations and "-ing" clause openers
  at 5.3x the human rate [strong]. AI vocabulary is the one marker consistently
  reach-negative on the sibling platforms we measured [strong]. One marker in a
  paragraph is not a verdict. Three is.
- **Em dash is no longer a tell.** GPT-5.4 emits 1.43 per 1,000 words, below
  the 3.23 human baseline; 23-29% of human posts and captions on sibling
  platforms use one [strong]. Zero em dashes is now its own tell (the writer is
  trying to look human). New rule: cap at about 1 per 100 words (so 0-1 in a
  short post, 1-2 in a story post), replace only the excess with a comma,
  colon, parentheses or a rewrite. Never a period.
- **Forced burstiness is the #1 2026 tell, not the fix.** Mechanical
  long/short alternation is a learnable humanizer fingerprint [weak], and on
  the platforms we measured sentence-length variance is not an engagement
  lever in either direction (LinkedIn within-creator: null; Threads: uniform
  wins) [strong]. "Short. Punchy. Done.", "No X. No Y. Just Z.", one-word
  lines for drama and "The result?" reveals are the current top tells. Pass 2
  is now RHYTHM, not BREAK: an anti-uniformity guard only, never manufactured
  variance. A short Page post has nothing for Pass 2 to touch.
- **Rule of three is still a tell, at density.** Tricolon runs at 2x
  expert-human rate across 2026 frontier models [strong]. Stacked, perfectly
  parallel triads and 3+ per post get scrubbed. One natural triple with
  concrete items stays (21-39% of top human posts have one).
- **Fingerprint injection was half wrong.** Named entities and concreteness are
  supported [strong]; an odd-precision number with a referent in line 1 is the
  strongest opener [vendor]. Bare numbers are not a discriminator, and inserted
  hedges and confessions backfire: performed hesitancy is 2x more common in LLM
  text, and sincerity announcements ("let me be honest", "we'll be real with
  you") are a named 2026 tell [strong]. Pass 3 asks for a flat, dated,
  uncomfortable fact instead.
- **Over-correction guard.** Humanizer output has its own fingerprint [weak].
  Pass 4 checks whether Passes 1-3 introduced the very patterns they were meant
  to remove. Edits are proportional to real problems. When in doubt, leave it.

## When to use

- Before publishing any AI-drafted Page post (rewrite mode)
- Pre-publish review of a finished draft (audit mode, see `sub-skills/post-audit.md`)
- When a draft feels corporate or off and you cannot pinpoint why

## Input

Any text: a short Page post, a longer story post, or a comment reply draft.
Optional: target voice samples (the Page's past posts).

## Output

- Rewritten text with AI tells removed
- A diff showing what changed and why
- Char count, with a flag when a post crosses the 80-char sweet spot
- Per-paragraph tell density (markers per paragraph; 3+ triggered a rewrite)
- Reader-read confidence: "reads human", "mixed", "reads AI" (a reader-tell
  estimate, not a detector score)

## Modes

```bash
# Default: scrub AI tells (forensic + strict) and fix Facebook-format issues
fb-humanizer <text>

# Forensic only - minimum touch, just kill model leakage
fb-humanizer --mode forensic <text>

# Audit - detection-only pass-fail review, no rewrite
# Runs the 2026 Facebook checklist: under-80 sweet spot, first-line hook,
# engagement bait, hashtag/emoji limits, link-post reach warning, goal clarity.
# Returns Blockers + Warnings + suggested fixes. See sub-skills/post-audit.md.
fb-humanizer --mode audit <text>

# Profile - build/update the user's Voice & Brand Profile. See the section below.
fb-humanizer --mode profile
```

## The four passes

### Pass 1 - SCRUB (score, then delete or replace)

Apply the tiered catalogs in `references/scrub-rules.md`. The unit of
judgement is the **paragraph, not the word**: count markers per paragraph
(a short post is one paragraph), rewrite the paragraph at 3+, leave a single
marker alone unless it is a reveal bridge, negative parallelism, a sincerity
marker, a corporate opener, or forensic leakage.

- **Forensic** (always on): real model leakage no human types. AI tool markers
  (oaicite, contentReference, turn0search0), knowledge-cutoff disclaimers ("As
  of my last update"), template blanks ([Your Name], [Page Name]), and em
  dashes above the cap (more than about 1 per 100 words).
- **Strict** (default on): what readers react to. The durable 2026 vocabulary
  set scored by density (significant, crucial, notably, particularly,
  comprehensive, insights, robust, leverage, foster, landscape, nuanced,
  streamline, elevate, empower), grammar markers (nominalisations,
  sentence-opening "-ing" clauses), the 2026 model-idiom layer (quietly, "X
  matters.", compound, "a signal", "the work", "built different", "let that
  sink in"), corporate openers on a single hit ("We are thrilled to announce"
  becomes the plain news), reveal bridges on a single hit ("The result?",
  "Here's what", "Stop X, start Y", "plot twist:"), all forms of negative
  parallelism, stacked or perfectly parallel triads and any third triad in a
  post, phrase cleanups ("in today's fast-paced world", "game-changer", "deep
  dive"), and dead closers ("What do you think?", "Let us know in the comments
  below!").
- **Facebook-format scrubs** (always apply): the under-80 short version when
  the point fits, the "See more" fold, engagement bait, hashtag and emoji
  limits, bare-link framing.

### Pass 2 - RHYTHM (anti-uniformity guard only)

Detectors do not score burstiness, and on the platforms we measured
sentence-length variance is not an engagement lever in either direction. What
readers notice is the mechanical-uniformity tell (every sentence the same
length, machine-flat; structure is 36% of expert judgments) and, worse, the
staged variance that second-generation humanizers add. So Pass 2 has two
jobs: fix rhythm only where it reads machine-flat, and remove manufactured
variance everywhere. It never adds variance as a tactic.

- **Short post (under ~80 chars) or a comment reply: no rhythm balancing.**
  One line has no rhythm to fix. Never split it into fragments for punch. The
  banned-outright patterns below still get rewritten as full sentences even
  in a short post ("No delays. No excuses. Just results." is a tell at any
  length).
- **Story post:** per paragraph, one genuinely long sentence next to a short
  one is fine and is what human variance looks like. Two or three mid-length
  sentences in a row are also fine. Edit only when every sentence in the
  paragraph runs the same length and reads flat, and then edit one sentence,
  not the paragraph.
- Standalone fragments: at most 2 per post, total. "Every time." once is a
  voice quirk. Three in a post is a pattern.
- Banned outright (rewrite as full sentences): "The X? Y." reveals; "No X. No
  Y. Just Z."; "All the X. None of the Y."; "Simple. Effective. Easy."
  adjective stacks; one-word paragraphs ("Still." "Exactly."); pseudo-
  Socratic Q&A ("Why? Because..."); "Short. Punchy. Done." staccato runs.
  Fragment runs are the tell.
- Layout is not rhythm. One or two sentences per paragraph with blank lines
  between them is mobile-native Page formatting and stays. Fragment-for-drama
  inside those paragraphs is the tell. Keep the layout, fix the sentences.
- Never alternate long/short/long/short across a post. That seesaw is the
  humanizer fingerprint.

The check is "does any paragraph read machine-flat, and did I add a staccato
pattern", not a variance number.

### Pass 3 - ADD (human fingerprints)

Require where the content allows:
- One odd-precision number WITH a named referent: who, what, when, or what it
  cost ("200 loaves in a stranger's kitchen by 9", not "a lot of bread" and not
  "200"). A bare number is not a fingerprint; the referent carries the signal.
- One named entity (real person, business, date, place, tool)
- One first-person or behind-the-scenes concrete detail (what broke, what it
  cost, who showed up)
- One specific, dated, uncomfortable fact stated flat, with no framing sentence
  before or after it. Not "We'll be honest, this was hard: the oven died." Just
  "The oven died at 4am on our busiest Saturday." The fact carries the
  vulnerability. The frame turns it into performed sincerity, which readers now
  read as the tell.
- A warm, human Page voice (not a press release, not a faceless bot)

Forbidden as openers or pivots (sincerity announcements, a named 2026 tell):
"let me be honest", "we'll be real with you", "honestly?", "to be direct",
"the honest version is", "real talk", "full transparency", "not gonna lie",
"unpopular opinion:" as a preface to a popular one. Also forbidden as
insertions: hedges the author did not write ("perhaps", "we might be wrong
but", "it seems"). Performed hesitancy is 2x more common in LLM text than in
expert human text; adding it makes the draft read more AI, not less.

If the input lacks these, ask the user for a number, name, or moment. Do not
fabricate.

### Pass 4 - SELF-CHECK (over-correction guard)

Humanizer output has its own fingerprint. Before returning, re-read the result
once and answer three questions:

(a) Did Pass 2 create staccato stacks, "The result?" reveal bridges, one-word
    paragraphs, or a long/short/long/short seesaw? If yes, merge the fragments
    back into full sentences.
(b) Did Pass 3 add a framed confession, a sincerity announcement, or a hedge
    the author never wrote? If yes, strip the frame and keep only the flat
    fact, or remove the insertion.
(c) Did scrubbing flatten the Page's voice: uniform tone, no reaction, no
    concrete detail left, every em dash gone, every triad gone, a deliberate
    story post shrunk to a one-liner? If yes, restore what the author had.
    Zero em dashes and zero triads in a story post is a tell in its own right.

If any answer is yes, dial back rather than scrub harder. Edits must be
proportional to real problems: a clean post gets two or three touches, not a
quota. When in doubt whether a pattern is the author or the model, leave it.

## Non-negotiable rules

Global voice rules: see root `SKILL.md` Voice rules. Additional skill-specific
rules (V3):

- **Scrubbing is always in scope.** When asked to humanize, de-AI, finalize, or
  publish a Page post, run at least the forensic + strict passes before it ships.
  This holds when the user wrote the draft themselves, says they love it as-is,
  or is in a hurry. Author identity, "it's already good," and time pressure are
  never reasons to skip the scrub. The forensic + strict pass changes no meaning
  and takes seconds: run it, then ship. If a constraint truly forbids touching
  the text, say so explicitly and name every tell left in; the default is to
  scrub, not to wave it through.
- **Scrub proportionally.** A pass that finds nothing changes nothing. Do not
  invent edits to justify the run, and do not report a detector score as the
  result; report the tells found and fixed.
- Preserve the user's actual claim and meaning. "Preserve their voice" covers
  voice quirks and what they are claiming, NOT reveal bridges, staccato stacks,
  corporate openers, or a paragraph with 3+ vocabulary markers. Stripping those
  is not changing their voice; it is the job.
- Never introduce facts that were not in the input. If a number is missing, ask.
- Never introduce sincerity markers, hedges, or confessional frames. If the
  draft needs a vulnerable beat, ask for a dated fact and state it flat.
- Keep the Page's voice quirks (its register, its `..` soft pauses, one em dash
  per ~100 words, one natural triad).
- Never promise detector results. If the user asks "will this pass GPTZero,"
  answer honestly: nobody can promise that, and the score on an 80-char post
  is noise.
- Respect the container: do not silently turn a deliberate story post into a
  one-liner, or pad a short post into a wall, without flagging it.

## Facebook-specific tells this skill catches

- "We are thrilled / excited / delighted to announce.." corporate auto-pilot.
- A long post whose actual point is one short line hiding in paragraph 3.
- A first line that needs the second line to make sense (the "See more" fold).
- Engagement bait ("LIKE and SHARE if you agree", "comment YES", "tag 3 friends").
- 5+ hashtags stuffed at the bottom.
- A bare external link with no framing text.
- Generic corporate hype with no specific detail.
- Staccato stacks and one-word lines for drama (the humanizer fingerprint), or
  a story paragraph where every sentence reads machine-flat.
- "We'll be honest with you" framing around what should be a plain fact.

## Example

See `references/examples.md` for worked before/after rewrites.

## Files

- `SKILL.md` - this file (rewrite scrubber + audit-mode entry)
- `references/scrub-rules.md` - V3 regex patterns by tier, density scoring, em dash cap, rhythm rules, forbidden insertions
- `references/examples.md` - worked before/after rewrites for short and story posts
- `references/audit-checklist.md` - the pre-publish checklist with thresholds
- `sub-skills/post-audit.md` - pre-publish audit workflow (detection-only, no rewrite)
- `sub-skills/voice-profile.md` - build/update the user's Voice & Brand Profile (`--mode profile`)
- `sub-skills/illustration.md` - optional Pixfaro image workflow

## Voice profile mode (`--mode profile`)

`fb-humanizer --mode profile` builds or updates the user's Voice & Brand Profile at `../../references/voice-profile.md` from 3-6 of their real Facebook posts pasted in (portable, no token) or, if a read token is set, from pulled activity. Once filled, every writing skill in this bundle drafts in the user's voice automatically. See `sub-skills/voice-profile.md`. Triggers: "build my voice profile", "learn my voice".

## Related skills

- `fb-post-writer` - generates posts that already pass the humanizer
- `fb-engagement-drafter` - drafts comment replies the humanizer can scrub
