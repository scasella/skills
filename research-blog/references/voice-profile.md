# Voice profile

The writing register the skill ships. Internalise these rules before drafting prose; they're what differentiates the article from generic AI-blog output.

## The register in one sentence

A forensic mentor explaining a result: short declarative observations followed by longer subordinate clauses that do the technical unpacking.

## Ten rules with examples

### 1. Mechanism leads, numbers follow

Topic sentences open with what changed and why. The number lives downstream in the same sentence or the next one. This forces the reader to think about the causal story, not the headline.

- ❌ "Panel hill-climbs 14% → 29% on held-out, +15pp in 100 RL steps." *(Number first, mechanism implicit.)*
- ✅ "Panel sees gradient signal on 382 of 877 problems. Thinking sees it on 209. The 1.83× ratio is the cleanest first-order test of the diversity claim." *(Observation, observation, then the ratio with its interpretation.)*

### 2. Hedging via specificity, not modal verbs

Instead of "we believe", "could suggest", "may indicate", "we estimate" — name the constraint, the n, the seed, the noise floor.

- ❌ "The result suggests panel may be hill-climbing faster, though more seeds would help confirm this."
- ✅ "The +15 pp number is one seed. The curve's shape replicates across the per-source breakdown; the absolute number wants a second seed before its CI gets reported."

### 3. Italics only on defined concepts

`*variance band*`, `*Base*`, `*hybrid*`, `*Thinking-2507*`. Not for emphasis. Not for "the right kind of *different*". Use `<strong>` for emphasis instead, sparingly.

- ❌ "The wider search converts to *gradient signal* — that's the *real* finding."
- ✅ "Wider per-sample search shows up where it matters for RL." (No italics — emphasis lives in the sentence structure.)

### 4. Em-dashes are scarce

Reference articles in this genre use one or two per article. The dash is for an aside that genuinely interrupts; for everything else use a period or comma.

- ❌ "Panel — which has 1.83× more variance-band problems than thinking — climbs faster on held-out — and the gain scales with training-pool fraction — across all four sources."
- ✅ "Panel has 1.83× more variance-band problems than thinking. It climbs faster on held-out, and the gain scales with training-pool fraction across all four sources."

### 5. Forensic short → long rhythm

Open with a punchy declarative observation. Follow with a longer sentence that unpacks the mechanism. This pattern repeats throughout. Avoid uniform sentence length — it reads as either staccato (too short) or AI prose (too long-and-balanced).

- Pattern: `[6-12 word observation]. [25-40 word unpacker with one or two subordinate clauses].`
- Example: "RL is a known diversity-killer. The natural worry was that 100 steps of RLVR would collapse the policy distribution and quietly erase the property the scaffold was chosen for."

### 6. Topic-first paragraphs

The first sentence of each paragraph states the claim. The rest of the paragraph supports it. Avoid building up to the punch line — readers skim, and the first sentence is what they read.

- ❌ "We ran the experiment with G=8 samples per problem. We sorted them into three bands. The variance band is where group-relative RLVR generates non-zero gradient. Panel had 382 problems in this band, vs thinking's 209."
- ✅ "Panel sees gradient signal on 382 of 877 problems; thinking sees it on 209. We classified each problem by sampling G=8 times per arm at temperature 1.0 and sorting into all_zero, variance_band (1–7 of 8 correct), or all_one — the variance band is the only regime where group-relative RLVR generates non-zero gradient."

### 7. No hype words

Banned: *dramatically, massively, hugely, shocking, incredible, surprising, remarkable, profoundly, fundamentally, paradigm-shifting, game-changing, breakthrough.* Also banned: *interestingly, notably, importantly* as paragraph openers — they signal the writer trying to control the reader's reaction.

- ❌ "Surprisingly, panel hill-climbs dramatically faster than thinking, with a remarkable +15pp gain."
- ✅ "Panel hill-climbs from 14% to 29% in 100 RL steps. Per-source gains scale with training-pool representation."

### 8. No "AI tells"

Specific phrases that signal generated prose:

- *"the right kind of different"*
- *"load-bearing"* (when used as a flourish rather than a technical term)
- *"in a theater costume"*, *"sets on fire"*, *"wider set of angles"*, *"orbits that strategy"* — overwrought metaphor
- *"It's worth noting that"*, *"It's important to understand"* — meta-narration
- *"In essence,"*, *"Ultimately,"*, *"At its core,"* — generalization markers
- *"This is more than just X — it's Y"* — the X-not-Y construction
- Em-dash followed by a colon

Strip them.

### 9. Numbers carry significance, not adjectives

If the number is significant, write it. Don't write "highly significant" or "extremely large". Let `t = 5.91, p < 10⁻⁸` do the work.

- ❌ "An extremely strong, highly significant effect (+78.2%, p < 10⁻⁸)."
- ✅ "+78.2% further apart in mpnet-space on MATH500 (paired t = 5.91, p < 10⁻⁸)."

### 10. Section pivots via direct setup, not rhetorical flourish

Open new sections with the question being asked or the operation being performed. Skip the "let's now turn to" / "with that in mind" / "this raises the question" connectives.

- ❌ "With the diversity result established, we now turn our attention to a follow-up question that emerged from the data: does the property hold under RL?"
- ✅ "The follow-up went further than that. Instead of a pass@k re-replication on a new dataset, we asked whether the per-sample diversity converts into gradient signal under RLVR."

## Anti-checklist before shipping prose

Run through these before declaring a draft done:

- [ ] No paragraph leads with a headline number — every topic sentence is mechanism-first.
- [ ] No "interestingly", "notably", "importantly", "surprisingly", "fundamentally" as paragraph openers.
- [ ] No "the right kind of X", "load-bearing", "in a theater costume", "orbits that strategy".
- [ ] Em-dashes counted: ideally 0–6 per article. Anywhere with two or more in one sentence: rewrite.
- [ ] Italics only on defined concepts (named methods, model variants, technical terms being introduced). No italicized adjectives.
- [ ] Hedging done via specificity (n, seed, stderr, what-was-not-tested) not modal verbs (may, suggests, could indicate).
- [ ] Caveats section is present and states what was *not* tested, not just what was. Lead with "Does not say:" before "Does say:" if both are present.
- [ ] No promotional close. The closing two paragraphs restate what holds and what's still open. Don't say "this is exciting" or "we're proud of this work".

## Common rewrites

| AI register | Forensic register |
|---|---|
| "We're excited to share..." | (cut entirely; no preamble) |
| "Here's what we found..." | "The result:" or just state the finding |
| "It's worth noting that..." | (cut; or restate the underlying point as a fact) |
| "This is significant because..." | State the significance directly as the next claim |
| "Our results clearly demonstrate..." | "The data shows..." or just state the data |
| "More research is needed to confirm..." | Name what specifically is needed: "A second seed; a matched-thinking-arm RL." |
| "Surprisingly, X happened" | "X happened. We expected Y." (Two sentences, surprise emerges from contrast.) |
