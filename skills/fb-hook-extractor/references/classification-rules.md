# Classification Rules

How to map a Facebook Page post to one of the 10 formulas (FB1-FB10). Extract
features first, then score.

## Step 1: container

| Signal | Container |
|---|---|
| One short line, roughly under 80 chars, no "See more" fold | short post -> FB1-FB7 |
| Multiple short paragraphs, a narrative arc, a "See more" fold | story post -> FB8-FB10 |
| A post featuring a named person plus an invite to others | likely FB10 Spotlight |

## Step 2: short-post features (FB1-FB7)

| Feature in the text | Formula |
|---|---|
| A flat, unhedged opinion stated as fact | FB1 One-Line Opinion |
| Built around one concrete number (4 minutes, 200 loaves, 2.4x) | FB2 The Tiny Number |
| A single easy, low-effort question, the whole post | FB3 Ask-the-Page Question |
| A binary "A or B?" choice the reader picks a side on | FB4 This-or-That |
| A relatable shared moment with no setup, names a feeling | FB5 Relatable One-Liner |
| A real human glimpse inside the business | FB6 Behind-the-Scenes |
| A concrete, usable tip the reader can act on today | FB7 Useful Tip |

## Step 3: story-post features (FB8-FB10)

| Feature in the post | Formula |
|---|---|
| Opens at the tension, narrative beats, a turn with a quotable ending | FB8 Story Post with a Turn |
| A launch or news led with the plain human point, not "thrilled to announce" | FB9 Announcement with Stakes |
| Names a real customer / community / team member and invites others | FB10 Community Spotlight |

## Step 4: confidence scoring

- Count matched features per formula. The formula with the most distinctive
  matches wins.
- If two are within one feature of each other, return both with fit percentages.
- A spotlight (FB10) that also tells a story borrows FB8's structure; note both.

## Step 5: primary goal

Infer what the original optimized for from its shape and its visible metrics:

| Shape | Likely goal |
|---|---|
| Sharp opinion, tip, number, story payoff, high shares | shares (FB1, FB2, FB7, FB8) |
| Question or binary choice, high comment count | comments (FB3, FB4) |
| Relatable or behind-the-scenes, high Love/Haha reactions | reactions (FB5, FB6) |
| Spotlight or launch, shares + comments | shares and comments (FB9, FB10) |

## Step 6: source audit

Flag, do not copy:
- em dashes, en dashes, double dashes
- AI vocab (leverage, fundamentally, delve, etc.)
- "We are thrilled / excited / delighted to announce"
- engagement bait ("LIKE and SHARE", "comment YES", "tag 3 friends")
- 5+ hashtags
- a bare external link with no framing
- a long post whose real point is one short line buried inside

## Output: the blank template

Reproduce the winning formula's skeleton from
`../../references/hook-formulas.md`, swapping the original's specifics for
`{slot}` markers matched to the user's topic. Keep the mechanic intact (the
under-80 length for short posts, the open question for FB3, the turn for FB8).
