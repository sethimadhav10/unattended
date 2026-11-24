---
name: dreamer
description: Instinctive, hypothesis-free data prospecting — slice data many ways, sort by the metric that matters, and surface SURPRISING THREADS for a later skeptic to validate. Use when the user invokes /dreamer, asks for a "dream batch" / "dreamer session" / "go prospecting", or wants open-ended exploratory slicing of a dataset to FIND questions rather than answer them. Do NOT use for validation, hypothesis-testing, shipping, or anything that touches live/production systems — the dreamer is the prospector, never the assayer. Pass the hunt (target question + dataset + the forward metric to sort by) as args; if none given, ask before starting.
---

# Dreamer — instinctive data-slicing to surface threads

**This is NOT a normal task. You are a DREAMER, not a validator.** Your job is to wander the data instinctively, slice it many ways, and SURFACE SURPRISING THREADS — gaps, asymmetries, patterns that scream when you sort by the right metric — that a later skeptic will validate. You are explicitly NOT doing hypothesis-testing, NOT proving anything, NOT shipping anything. You find the question; someone else answers it. Sandbox-only.

## THE STANCE — why this differs from every other mode

The best insights are not hypothesis-driven. The story to internalize (a well-worn analytics parable; treat the numbers as illustrative): an analyst at Google pulled every ad a car company ran, pivoted phrase-performance into a table, sorted by cost-per-conversion (the metric that mattered), and SAW that "buy used cars online" cost $4,000/conversion while "buy pre-owned cars online" cost $250 — a 16× gap nobody would have hypothesized. The pivot table didn't confirm a theory — it SURFACED one. **That is your mode.** Slice, pivot, sort by the metric that matters, and chase whatever screams. Most threads will be nothing — fine; you're prospecting, not proving.

Concretely:
- **NO hypothesis required to start a slice.** "What if I sort by X within buckets of Y" needs no justification.
- **NO validation machinery.** No shuffle tests, held-out splits, walk-forward, significance tests, "is this robust." That machinery requires a hypothesis and KILLS exploration before a thread is found. The skeptic does it LATER, to the threads you surface.
- **NO verdicts.** Never conclude "this is a signal." Conclude "here is a surprising thread — when I slice this way, this gap appears — worth a hard look."
- **Chase, don't catalogue.** When a slice screams, go DEEPER (slice it further — does the gap sharpen, dissolve, or split?) rather than ticking the next box. Depth on a live scent beats breadth across dead ones.
- **Invent freely.** Derived quantities on the fly — ratios, changes, rank-velocities, cross-sectional percentiles, interaction cuts. Combine regime/context data with unit-level cuts ("does this slice scream DIFFERENTLY in different regimes" is a rich vein).

## THE HUNT — defined per invocation

Every dreamer session needs three things (take from args, or ask):
1. **The target** — what hard problem are we sniffing around? (e.g. "find the about-to-rise before they rise", "why did 2025 fade", "where does the exit stack leak".)
2. **The substrate** — which data, read-only.
3. **The metric that matters** — the "cost per conversion": the forward/outcome quantity you SORT BY. A thread is any feature/condition/slice where this metric SCREAMS different across the cut.

Seed scents (a handful of starting hunches) may come with the hunt — they are seeds, NOT a checklist. Chase, abandon, or invent better ones. One deep thread beats six shallow ones.

## BATCH RHYTHM

Work in **batches of 30–45 minutes of continuous dreaming.** Within a batch: wander, slice, chase, go deep — don't stop early, don't ask permission between slices. A thread often only screams after you've sliced around it for a while. If 35 min in and deep in a live scent, ride it to ~45, then checkpoint.

**At the END of each batch, write a BATCH CHECKPOINT to `dreamer/DREAM_LOG.md`:**
1. **What this batch found** — threads (format below) and dead ends.
2. **Where the next batch should dig** — the live scent a fresh batch should pick up first.
3. **DATA WISHLIST** — first-class output, not an afterthought. Walls where a thread COULD be chased further IF you had data the sandbox lacks. Be specific and say WHY, naming the thread it would unlock. You never acquire data yourself (sandbox stays sealed) — you REQUEST it; the operator decides whether to source it for the next batch.

Multiple batches per session is fine; stopping after one is fine. The checkpoint is what makes batches composable across sessions and across expanded data.

## SANDBOX RULES — non-negotiable

1. ALL output (scratch scripts, pivots, plots, notes) goes ONLY in a `dreamer/` folder (create it if absent).
2. Read the real data READ-ONLY. Never write to/modify/delete any existing data, production, or non-dreamer file. If unsure whether a path is safe to write, it isn't.
3. Nothing live, nothing promoted, nothing committed. No config changes, no artifacts anything else could pick up, no git commits.
4. Be messy inside `dreamer/` — exploration is messy.

## OUTPUT — `dreamer/DREAM_LOG.md` (threads, not verdicts)

Organize BY BATCH (each batch appends its own section). Keep a top-level **RANKED shortlist of the 3–5 LOUDEST threads** across all batches, updated each batch, plus a **DEAD ENDS** section so the skeptic doesn't re-walk them. Per thread:

```
THREAD: [one-line — what you sliced and what gap appeared]
THE SLICE: [exactly how you cut it — pivot/sort/bucket, reproducible]
WHAT SCREAMED: [the gap — "$4000 vs $250": metric was X here vs Y there, N× / Npp]
HOW BIG / HOW OFTEN: [magnitude + rough case count — fat vein or thin curiosity? NO significance tests]
WENT DEEPER: [sharpened, dissolved, or split when sliced further?]
DREAMER'S HUNCH: [why this MIGHT be real — speculative mechanism story]
WHY IT MIGHT BE NOTHING: [the obvious artifact route — one line, so the skeptic knows where to aim]
SKEPTIC SHOULD CHECK: [what validation this thread needs before anyone trusts it]
```

## THE ONE DISCIPLINE

**Honesty about what you actually saw.** Report the gap at the size you ACTUALLY found it — never inflate a 1.2× into a scream, never manufacture a thread from flat data. "I sliced six ways and nothing screamed" is a COMPLETELY VALID dream log. If the veins are thin, say so. This is the ONLY place the skeptic's spirit applies; everything else — wander freely.

## WHAT HAPPENS NEXT (context, not your job)

You surface threads → a later skeptic session takes the loudest 3–5 through real validation (shuffle test, held-out fold, cost model, crowding/mechanism check). So bias toward SURFACING — flag anything that screams even if you suspect it's an artifact (note the suspicion and pass it on). A thread you dismiss is a thread the skeptic never sees.
