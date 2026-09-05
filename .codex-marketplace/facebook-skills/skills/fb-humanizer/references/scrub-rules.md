# Scrub Rules (Facebook Page, V3, 2026-09)

Tiered catalogs the humanizer applies. Load this file when actually executing a
scrub. Two tiers: forensic (always on) and strict (default on), plus the
Facebook-format scrubs. V3: vocabulary is scored by **density per
paragraph**, not deleted per word. Em dashes are **capped** at about 1 per 100
words, not banned. Forced rhythm is a tell, not a fix. Facebook has no corpus
of its own yet; the calibration follows LinkedIn. See SKILL.md "What changed
in V3" for the evidence.

## Contents

- Density scoring (how every vocabulary rule is applied)
- FORENSIC tier (always on)
- STRICT tier (default on)
- Facebook-format scrubs (always apply)
- Pass 2 - Rhythm (anti-uniformity guard only)
- Pass 3 - Forbidden insertions (sincerity markers, hedges)
- Preserve these (Page voice, do not scrub)

---

## Density scoring (how every vocabulary rule is applied)

The cluster principle: readers spot AI text from clusters of markers, not from
any single word. One "notably" in a paragraph is English. "Notably",
"comprehensive" and a nominalisation in the same paragraph is a signature. A
short Page post is one paragraph.

```python
def score_paragraph(paragraph: str, markers: dict) -> dict:
    """Count marker hits per paragraph. Returns hits and the action to take."""
    hits = []
    for name, pattern in markers.items():
        for m in re.finditer(pattern, paragraph, flags=re.I):
            hits.append((name, m.group(0)))
    n = len(hits)
    always = [h for h in hits if h[0] in ("reveal_bridge", "neg_parallel", "sincerity_marker", "corporate_opener")]
    if n >= 3:
        action = "REWRITE_PARAGRAPH"   # 3+ markers = signal. Rewrite the paragraph, not word-by-word.
    elif always:
        action = "REPLACE"             # a reveal bridge / negative parallelism / sincerity marker / corporate opener is always scrubbed,
                                       # even when paired with one ordinary marker (checked BEFORE the density branch)
    elif n == 2:
        action = "FLAG_ONLY"           # 2 ordinary markers = borderline. Report it, leave the words: the audit allows 0-2 per unit.
    else:
        action = "LEAVE"               # a single common word is not a verdict
    return {"hits": hits, "count": n, "action": action}
```

Rules of application:
- Score forensic markers separately: one hit = delete, no density threshold.
- Post-level counts also matter for two patterns: triads (keep the first
  natural one, rewrite every later one, so a post ends with at most one) and
  standalone fragments (3+ per post = merge back, see Pass 2).
- Never replace a word with a synonym from the same list. "Leverage" to
  "harness" is not a fix.
- When you rewrite a paragraph, rewrite it in the Page's register (a warm
  bakery stays a warm bakery), not in "plain" register. Plainness at uniform
  temperature is itself a fingerprint.

---

## FORENSIC tier (always on)

Real model leakage no human types. Delete or flag on sight.

| Pattern | Action |
|---|---|
| `oaicite`, `contentReference`, `turn0search0`, `attached_file`, `grok_card` | delete the marker |
| "As of my last update", "As of my knowledge cutoff", "I cannot browse" | delete the disclaimer line |
| `[Your Name]`, `[Page Name]`, `[Company]`, `[insert X here]`, `YYYY-MM-DD` template blanks | flag, ask the user to fill |
| Em dashes above the cap (see below) | replace the excess with a comma, colon, parentheses, or a rewrite; never a period |

### Em dash cap (about 1 per 100 words)

The character is not a tell: GPT-5.4 emits 1.43 em dashes per 1,000 words,
below the human 3.23, and 23-29% of human posts on sibling platforms contain
one. Zero em dashes in a story post that wanted one is the tell of someone
trying to look human. What is still forensic is the old GPT-4 glue habit: 3+
in a short post.

```python
def em_dash_excess(text: str) -> int:
    """Return how many em dashes exceed the cap (~1 per 100 words, floor 1, ceiling 2 per post).
    0 = leave every em dash alone. A short post (under 80 chars) rarely needs one; the cap is still 1."""
    words = len(text.split())
    cap = max(1, min(2, round(words / 100)))
    return max(0, text.count("—") - cap)

# Replacement order for the EXCESS ones (keep the one doing the most work, usually the first):
#   1. comma            if the dash joins a clause to the main sentence
#   2. colon            if the dash introduces a reveal, a list, or a consequence
#   3. parentheses      if the dash pair wraps an aside
#   4. rewrite          if none of the above reads naturally
# NEVER a period. "X. Y." from a split dash creates fragment stacking, which is a worse tell than the dash.
```

---

## STRICT tier (default on)

What expert human readers cite when they spot AI text (vocabulary 53%,
sentence structure 36%). All vocabulary and grammar lists go through
`score_paragraph()`; reveal bridges, negative parallelism, sincerity markers
and corporate openers are scrubbed on a single hit.

### Punctuation

- Curly quotes -> straight quotes.
- `--` -> a comma or a rewrite (not a period: a period here stacks fragments).
- En dash (`–`) between clauses -> a comma. Number ranges (7-9) stay.
- Em dashes are handled by `em_dash_excess()` above, not stripped.

### Vocabulary: durable 2026 markers (density-scored)

The 2023-24 list (delve, tapestry, realm) is decaying because humans now avoid
those words. The durable markers are common words LLMs over-select at 2-5x the
human rate across 2026 frontier models. They are ordinary English, so one per
paragraph is fine. Three in a paragraph is a signature.

| Marker | Preferred replacement when the paragraph is over threshold |
|---|---|
| significant | a number ("31% more orders", not "significant growth"; ask if none exists) |
| crucial | delete, or "the" |
| notably, particularly | delete |
| comprehensive, holistic | full |
| insight(s) | say what was learned |
| robust | solid (keep if a term of art) |
| leverage | use |
| foster | build |
| landscape | field |
| nuanced | specific |
| multifaceted | delete |
| streamline | simplify |
| elevate | improve |
| empower | let |
| utilize, harness | use |
| facilitate | help |
| unlock | open up |
| navigate (figurative) | handle |
| seamless | smooth |
| ecosystem | space |

Filler adverbs (each counts as one marker; delete when over threshold):
fundamentally, essentially, ultimately, crucially, notably, particularly,
arguably, certainly, definitely, undoubtedly.

### Grammar markers (density-scored; the 2026 structural signature)

```python
GRAMMAR_MARKERS = {
    # Present-participial clause openers: 5.3x the human rate.
    # "Leveraging our data, we..." / "Building on this, ..."
    "ing_opener": r"(?m)^[\s>*\-]*[A-Z][a-z]+ing\b[^.]{0,60},",
    # Nominalisations: verb-turned-noun that hides the actor. "the implementation of"
    "nominalisation": r"\bthe (\w+(?:tion|sion|ment|ance|ence|ization|isation)) of\b",
    # Stacked abstract nouns
    "abstract_stack": r"\b(alignment|transformation|optimization|innovation|efficiency|scalability|synergy)\b.{0,40}\b(alignment|transformation|optimization|innovation|efficiency|scalability|synergy)\b",
}
# Fix for ing_opener: put the actor first. "Leveraging our data, we cut wait times" -> "We cut wait times with our data."
# Fix for nominalisation: use the verb. "the implementation of the new menu" -> "when we launched the new menu"
```

### 2026 model-idiom layer (density-scored)

Phrases that were human idiom in 2024 and are model idiom in 2026. Each counts
as one marker; "let that sink in" and "that's the real story" are scrubbed on
a single hit as closers.

```python
IDIOM_LAYER_2026 = [
    r"\bquietly\b",                          # "quietly shipped"
    r"(?m)^\w+ matters\.$",                  # "community matters." as a line
    r"\bcompound(s|ing)?\b",
    r"\ba signal\b|\bthe signal\b",
    r"\bthe work\b",
    r"\bbuilt different\b",
    r"\bload-bearing\b",
    r"\bdoing the heavy lifting\b",
    r"\blet that sink in\b",
    r"\bthat's the real story\b",
]
```

### Corporate openers (single hit = rewrite to the plain news)

```python
CORPORATE_OPENERS = [
    r"(?im)^we (are|'re) (thrilled|excited|delighted|proud|honou?red|pleased) to (announce|share|introduce|reveal)\b[^.!\n]*[.!:]?\s*",
    r"(?im)^it is with great (pleasure|excitement|pride) that\b[^.!\n]*[.!:]?\s*",
    r"(?im)^without further ado[,:]?\s*",
    r"(?im)^(big|exciting) news[!:]\s*",
]
# Fix: state the news the way you would text a friend. "We are thrilled to announce our new menu" -> "New menu drops Friday."
```

### Reveal bridges (single hit = replace)

```python
REVEAL_BRIDGES = [
    (r"(?im)^the (result|outcome|answer|lesson|catch|kicker|truth)\?\s*", ""),   # "The result?"
    (r"(?i)\bit'?s not \w[^,.]{0,40}, it'?s \b", None),                          # "It's not X, it's Y" (rewrite as paired declaratives)
    (r"(?i)^stop \w[^,.]{0,40}\. start \b|^stop \w[^,.]{0,40}, start \b", None),  # "Stop X, start Y"
    (r"(?im)^here'?s (what|how|why|the thing)\b[^:.\n]{0,40}[:.]\s*", ""),      # "Here's what/how"
    (r"(?im)^(plot twist|spoiler|the twist)[:?]\s*", ""),
]
# Fix: delete the bridge and let the next sentence stand. It was the point anyway.
# Named 2026 tells on every reader list; measured reach-negative on LinkedIn (vendor data).
```

### Negative parallelism (single hit = rewrite)

Strip the "not X, but Y" / "it isn't about X, it's about Y" constructions and
every sibling form ("The question isn't X, it's Y", "This isn't X. This is
Y."). Rewrite as paired declaratives, not by auto-substitution, and flag for
the user since meaning preservation needs judgement.

### Rule of three (strict at density; one natural triad is allowed)

Tricolon runs at 2x the expert-human rate across 2026 models. 21-39% of top
human posts on sibling platforms contain one, so the tell is the stacked or
perfectly parallel triad, the hollow one, and the repeat, not the form.

```python
def detect_triads(text: str) -> list:
    patterns = [
        r"(\w+), (\w+),? and (\w+)",                       # word triplets
        r"(\w+ \w+), (\w+ \w+),? and (\w+ \w+)",           # short-phrase triplets
        r"(?m)^(\w+)\. (\w+)\. (\w+)\.$",                  # "Simple. Effective. Easy." (also a Pass 2 staccato hit)
        r"\b(no \w+)[,.] (no \w+)[,.] (just|only) \w+",    # "No X. No Y. Just Z." (also a Pass 2 hit)
    ]
    return [m for p in patterns for m in re.finditer(p, text, flags=re.I)]

HOLLOW_ADJECTIVES = {"dynamic", "vibrant", "innovative", "faster", "cheaper", "better", "simple",
                     "effective", "easy", "bold", "clear", "focused", "scalable", "powerful"}
ABSTRACT_NOUNS = {"growth", "impact", "value", "alignment", "innovation", "efficiency", "results", "success",
                  "clarity", "freedom", "scale", "momentum", "consistency", "mindset", "strategy", "vision"}

def hollow(items) -> bool:
    """A triad is hollow when its items are interchangeable: every item is an abstract adjective or an
    abstract noun, and none carries a receipt (a proper name, a number, a $ or %). Equal word counts are
    NOT a tell on their own: "Stripe invoices, Vercel logs, and GitHub alerts" is a natural concrete triad."""
    def has_receipt(items) -> bool:
        for i, x in enumerate(items):
            for j, w in enumerate(x.split()):
                if re.search(r"[0-9$%]", w):
                    return True
                if w[:1].isupper() and not (i == 0 and j == 0):   # a sentence-initial capital is not a name
                    return True
        return False
    all_abstract = all(x.lower().strip() in HOLLOW_ADJECTIVES or x.lower().strip() in ABSTRACT_NOUNS
                       or x.lower().split()[-1] in ABSTRACT_NOUNS for x in items)
    return (not has_receipt(items)) and all_abstract

def triad_action(triads: list) -> list:
    """Call once per post with that post's triads. Scrub any hollow triad on sight. Of the natural
    (concrete, non-interchangeable) ones keep only the FIRST; every later triad in the same post is rewritten,
    so each post ends with at most one natural triad. Threads are not pooled: the threshold is per post."""
    actions = []
    kept_one = False
    for t in triads:
        items = t.groups()
        if hollow(items) or kept_one:
            actions.append((t, "REWRITE_AS_TWO_OR_FOUR"))   # 2 items, or 4 with one that breaks the pattern
        else:
            actions.append((t, "LEAVE"))
            kept_one = True
    return actions
```

### Dead phrases (delete or rewrite)

- "in today's fast-paced world", "in the age of AI"
- "at the end of the day"
- "game-changer", "deep dive", "move the needle", "needle-mover", "paradigm shift"
- "the world of {thing}"
- "the hard truth is" / "the uncomfortable reality is"
- "embark on this journey", "stay tuned for more updates"

### Dead closers (rewrite to a landing or a specific ask)

- "What do you think?"
- "Thoughts?"
- "Let us know in the comments below!"
- "Tag someone who needs this."
- "Let that sink in."
- A one-word closing line ("Still.")

A specific question that earns a real comment ("Which one are you trying
first?") is not a dead closer; it is what the meaningful-interactions model
rewards.

## Facebook-format scrubs (always apply)

- A post that runs long when its point fits under 80 chars: surface the short
  version and offer it. (This is a format choice, not a rhythm edit: the short
  version is the point stated once, not the paragraph chopped into fragments.)
- A first line that needs line 2 to make sense (the "See more" fold): rewrite so
  it stands alone.
- Engagement bait ("LIKE and SHARE", "comment YES", "tag 3 friends"): delete. It
  is downranked, not rewarded.
- 3+ hashtags: cut to 0-2, move to the end.
- 3+ emoji, or any emoji on a serious post: cut.
- A bare external link with no framing: add framing text above it, and note that
  link posts reach fewer people organically.

---

## Pass 2 - Rhythm (anti-uniformity guard only)

Replaces V2's "BREAK (force burstiness)". Detectors do not score burstiness
(GPTZero dropped it in 2023). On the platforms we measured, sentence-length
variance is not an engagement lever in either direction (LinkedIn
within-creator: null to slightly negative; Threads: uniform wins), and
mechanical long/short alternation is a learnable humanizer fingerprint. So:
fix rhythm only where a story paragraph reads machine-flat, remove
manufactured variance everywhere, never add variance as a tactic. A short
post has nothing for this pass to touch.

```python
STACCATO_TELLS = [
    r"(?m)^\w+\.$",                                              # one-word paragraph: "Still." "Exactly."
    r"(?m)^(\w+\. ){2,}\w+\.$",                                  # "Short. Punchy. Done." / "Simple. Effective. Easy."
    r"(?i)\bno \w+\. no \w+\. (just|only) \w+",                  # "No X. No Y. Just Z."
    r"(?i)\ball (of )?the \w+\. none of the \w+",                # "All the X. None of the Y."
    r"(?im)^the (result|outcome|answer|lesson|catch|kicker|truth)\?",  # "The result?" reveal (also a strict reveal bridge)
    r"(?i)\b(why|how|what happened)\? (because|simple|easy)\b",  # pseudo-Socratic Q&A
    r"(?i)\b(that's it|that's all|that's the post|full stop|period)\.$",
]

def restore_rhythm(text: str) -> str:
    """V3. Remove staged variance; un-flatten only what reads machine-flat. Never manufacture variance."""
    paragraphs = split_paragraphs(text)
    fragments_seen = 0

    for i, p in enumerate(paragraphs):
        # 1. Kill staged rhythm first, on EVERY post including a short one. Merge staccato runs into one
        #    full sentence with a real clause. "No delays. No excuses. Just results." is a tell at any length.
        for pat in STACCATO_TELLS:
            if re.search(pat, p):
                p = merge_into_sentence(p, pat)     # "No preservatives. No shortcuts. Just bread." -> "No preservatives and no shortcuts, just bread baked at 4am."

        # 1b. Short post (one paragraph under ~120 chars): staccato cleanup is the only rhythm edit.
        #     There is no rhythm to un-flatten and nothing may be fragmented for punch.
        if len(paragraphs) == 1 and len(text) < 120:
            return p

        sents = split_sentences(p)
        lengths = [len(s.split()) for s in sents]

        # 2. Cap standalone fragments (<4 words) at 2 per POST, not per paragraph.
        for j, n in enumerate(lengths):
            if n < 4:
                fragments_seen += 1
                if fragments_seen > 2:
                    sents[j] = attach_to_neighbor(sents, j)   # fold into the previous sentence with a comma or colon

        # 3. Un-flatten ONLY a machine-flat paragraph: 4+ sentences, every one within +-3 words of the
        #    mean, no subordinate clause anywhere. Then extend the ONE sentence that carries the most
        #    content by absorbing its natural neighbour with a clause that does work (because / which /
        #    when / after), not a comma splice. The absorbed neighbour is removed so nothing appears twice.
        #    Once per paragraph, and only if the result reads like the author.
        if len(sents) >= 4 and all(abs(n - mean(lengths)) <= 3 for n in lengths) and not any(has_working_clause(s) for s in sents):
            k = max(range(len(sents)), key=lambda j: lengths[j])
            j = k + 1 if k + 1 < len(sents) else k - 1
            sents[k] = join_with_clause(sents[k], sents[j])
            del sents[j]

        # 4. Never long/short/long/short. If the paragraph now alternates (4+ sentences flipping between
        #    short <8 words and long >=16 words), fold the SECOND short sentence into the sentence before it.
        #    The seesaw is the humanizer fingerprint.
        lengths = [len(s.split()) for s in sents]
        if len(lengths) >= 4 and all((lengths[k] < 8) != (lengths[k + 1] < 8) for k in range(len(lengths) - 1)) \
                and all(n < 8 or n >= 16 for n in lengths):
            k = [j for j, n in enumerate(lengths) if n < 8][1]
            sents[k - 1] = join_with_clause(sents[k - 1], sents[k])
            del sents[k]

        # 5. One-idea-per-line story posts (each paragraph one sentence): leave rhythm alone entirely.

        paragraphs[i] = rejoin_keeping_breaks(p, sents)   # re-attach the paragraph's own single line breaks; the pass edits sentences, never breaks

    return "\n\n".join(paragraphs)
```

Layout vs rhythm: 1-2 sentence paragraphs with blank lines between them are
mobile-native Page formatting and are **not** touched by this pass. "The oven
died at 4am on our busiest Saturday." on its own line is layout. "Still." on
its own line is fragment-for-drama. The pass edits sentences, never the blank
lines.

## Pass 3 - Forbidden insertions (sincerity markers, hedges)

Pass 3 adds concreteness only (a referenced odd-precision number, a named
entity, a flat dated fact). It never adds these, and Pass 1 strict removes them
when the draft already has them as an opener or pivot:

```python
SINCERITY_MARKERS = [
    r"(?im)^(let me be (honest|real|direct|clear)|we'?ll be (honest|real|direct)( with you)?|i'?ll be (honest|real|direct)|honestly\?|honest (caveat|version|answer)|the honest (version|answer|truth) is|to be (direct|honest|fair|transparent)|real talk|full transparency|can i be (honest|vulnerable)|not gonna lie|ngl|unpopular opinion)[:,.]?\s*",
    r"(?i)\b(i (might|may|could) be wrong,? but|we (might|may|could) be wrong,? but|perhaps|it seems (to me )?that|in my humble opinion|i think it'?s fair to say)\b",  # inserted hedges: only scrub if NOT in the author's voice samples
]
# Fix: delete the marker and keep the sentence that follows. If the sentence that follows is not
# a specific fact, the marker was doing the work of vulnerability. Ask the author for the fact.
# Evidence: performed hesitancy 2x more common in LLM than expert human text; "false vulnerability"
# is a named 2026 tell. A flat dated uncomfortable fact with no frame is reach-POSITIVE (vendor data).
```

## Preserve these (Page voice, do not scrub)

- The Page's register, whether warm-casual or plain-spoken
- `..` as a soft pause
- One or two sentence fragments used intentionally ("Every time.") - the cap
  is 2 per post, not 0
- One em dash per ~100 words. Do not push the count to zero; zero across a
  story post is below the human baseline
- One natural rule-of-three with concrete, non-interchangeable items
- One genuinely long sentence per paragraph in a story post, even if a style
  guide would split it
- A deliberate story post's length. Long is fine when every line earns it
- Contractions (don't, it's, you're)
- Specific numbers with referents and named entities (add MORE, never remove)
- Behind-the-scenes concrete details
- The Page's reactions and opinions, including a blunt one. Flat tone across
  a whole post is a humanizer fingerprint
- A single common-word marker in a paragraph ("notably", "robust" as a term
  of art). One is not a verdict
- The real story. Never invent a detail to make a post land
