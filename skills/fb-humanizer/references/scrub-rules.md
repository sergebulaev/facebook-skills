# Scrub Rules

Tiered catalogs the humanizer applies. Load this file when actually executing a
scrub. Two tiers: forensic (always on) and strict (default on).

## FORENSIC tier (always on)

Real model leakage no human types. Delete or flag on sight.

| Pattern | Action |
|---|---|
| `oaicite`, `contentReference`, `turn0search0`, `attached_file`, `grok_card` | delete the marker |
| "As of my last update", "As of my knowledge cutoff", "I cannot browse" | delete the disclaimer line |
| `[Your Name]`, `[Page Name]`, `[Company]`, `[insert X here]`, `YYYY-MM-DD` template blanks | flag, ask the user to fill |
| 3+ em dashes in a single post | replace each with `..`, a period, or a line break |

## STRICT tier (default on)

Bad Facebook Page style regardless of who wrote it.

### Punctuation

- Curly quotes -> straight quotes.
- `--` -> a period or a line break.
- Em dash (`—`) / en dash (`–`) -> `..`, a comma, or two sentences.

### Vocabulary swaps

| AI word | Swap to |
|---|---|
| leverage | use |
| utilize | use |
| facilitate | help |
| streamline | simplify |
| harness | use |
| foster | build |
| delve | look at |
| navigate (figurative) | handle |
| unlock | open up |
| robust | solid |
| seamless | smooth |
| cultivate | grow |

### Corporate openers (rewrite to the plain news)

- "We are thrilled to announce" -> just state the news the way you would text a friend
- "We are excited to share" -> the news, plainly
- "It is with great pleasure that" -> delete
- "Without further ado" -> delete

### Filler adverbs (delete)

fundamentally, essentially, ultimately, crucially, notably, simply, just (as a
hedge), really (as a hedge).

### Dead phrases (delete or rewrite)

- "in today's fast-paced world"
- "at the end of the day"
- "game-changer", "deep dive", "move the needle", "needle-mover"
- "it's not just X, it's Y"
- "the world of {thing}"

### Dead closers (rewrite to a landing or a specific ask)

- "What do you think?"
- "Thoughts?"
- "Let us know in the comments below!"
- "Tag someone who needs this."

## Facebook-format scrubs (always apply)

- A post that runs long when its point fits under 80 chars: surface the short
  version and offer it.
- A first line that needs line 2 to make sense (the "See more" fold): rewrite so
  it stands alone.
- Engagement bait ("LIKE and SHARE", "comment YES", "tag 3 friends"): delete. It
  is downranked, not rewarded.
- 3+ hashtags: cut to 0-2, move to the end.
- 3+ emoji, or any emoji on a serious post: cut.
- A bare external link with no framing: add framing text above it, and note that
  link posts reach fewer people organically.

## Negative parallelism

Strip the "not X, but Y" / "it isn't about X, it's about Y" constructions. They
are an AI rhythm tell. Rewrite to a direct claim.
