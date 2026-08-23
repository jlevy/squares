# The `s(n)` search campaign — runbook

An [experiment loop](../../../.agents/skills/experiment-loop/SKILL.md) aimed at the
search side of square packing.
This file is the contract every round is run under: the question, the metric vector, the
accept rule, and the budget.
It is frozen while rounds are running — see
[what a runner may not do](#what-a-runner-may-not-do).

## The campaign question

**Which search strategies reach the standing best for `s(n)` within a declared move
budget, and what do the ones that fail find instead?**

Note what this does *not* say.
It does not say “beat Trump’s 1979 packing”.
That record has stood for 47 years against purpose-built programs, and a campaign whose
only success condition is breaking it would record nothing for weeks.
The answerable question is about the *methods*: which of them recover a known optimum,
how much budget that costs, and where they land when they fail.
That question has never been asked of this problem — the
[research program](../docs/project/research/research-2026-08-22-packing-11-unit-squares.md#a-research-program)
notes that the modern evolutionary-search stack has never been aimed at
squares-in-squares, and that “success would be informative; failure would be more
informative”.

## Subject, and the instance axis

The **subject** is the instrument and the precision the numbers were taken at.
Never extrapolate across it: an `f64_screen` number and an `exact` number are different
kinds of fact.

The **instance axis is `n`**, and the first three cells each have a different job:

| `n` | role | standing best | why this cell |
| --- | --- | --- | --- |
| 10 | **positive control** | `3 + 1/√2 = 3.70710678…`, proved | Known answer, and *not* the grid — it needs a genuine 45° tilted family. A searcher that cannot recover it has not earned an opinion about an open case. |
| 11 | **target** | `3.87708359002281…`, Trump 1979 | The smallest open case, smallest open gap with a non-trivial record, degree-8 and rigid. |
| 12 | **negative control** | `4`, the trivial grid | The 4×4 grid is almost certainly optimal. A run that “beats” it has found a bug, not a packing. |

Standing bests are read from [`../frontier/`](../frontier/README.md) — `n-010.md`,
`n-011.md`, `n-012.md` — never retyped into a round.
The frontier artifacts are the campaign’s source of truth for what is already known, and
a round that moved the frontier would edit one file.

## The three tiers

A number’s tier is recorded as `subject.precision`, and it decides what the number may
claim.

| Tier | What it is | May claim |
| --- | --- | --- |
| `f64_screen` | [`sqsearch`](../sqsearch/) — annealing that minimises the enclosing side, ~40M moves/s | a basin was found; a strategy comparison |
| `polished` | numerical refinement of one basin to ~1e-12 | a candidate worth certifying |
| `exact` | [`sqpack`](../README.md#exact-verification) — separating-axis over the packing’s own algebraic number field | **validity, and only here: a record** |

The tier boundary is not bureaucracy.
A record packing has pairs touching at *exactly* zero separation — 14 of the 55 pairs in
Trump’s — and no floating-point check can decide those: a tolerance loose enough to
accept true contact is loose enough to accept a small overlap.
That is the whole reason `sqpack` exists, and it is why `beat_record: true` may only be
written at `precision: exact`.

## The metric vector

Fixed for the campaign.
Recorded on every round; the role says what each may conclude.

| Metric | Role | Source |
| --- | --- | --- |
| `best_side` | **outcome** | smallest valid side found, `record` shape against the frontier’s standing best |
| `outcome` | **outcome** | `determination`: `beat_record`, `reached_basin`, `near_miss`, `no_progress`, `invalid` |
| `moves`, `seconds` | cost | engine summary |
| `overlap` | **guard** | total penetration depth of the reported packing; a non-zero value at screen tier invalidates the run |
| `selftest_passed` | **guard** | `sqsearch --selftest` before any run is recorded |
| control cells | **guard** | `n=10` must land within `1e-2`; `n=12` must not go below `4` |
| `restarts`, `accepted`, `moves_per_sec` | mechanism | engine summary |
| spread of `best_side` across seeds | mechanism | five seeds per cell, always |

`reached_basin` means `best_side − standing_best < 1e-4`. That is a **numerical proxy**
for “found the right combinatorial class”, not a proof of it; confirming the class means
comparing the contact graph, which is tier-2 work.
Rounds that claim `reached_basin` should say which they mean.

## The accept rule

Written before the first measurement, and not changed while rounds are running.
A candidate strategy is **accepted** when all of:

1. **Outcome.** Its median `best_side` across ≥5 seeds is below the control’s median,
   and the two seed ranges do not overlap — or it reaches `reached_basin` on a cell
   where the control does not.
2. **Evidence.** Five seeds per cell minimum, median and min–max range both reported.
   Overlapping ranges mean *no detectable effect*, never “a small win”.
3. **Validity.** Every reported configuration has `overlap == 0` at screen tier, and the
   engine selftest passed in the same invocation.
4. **Guards.** The `n=10` positive control lands within `1e-2` and the `n=12` negative
   control does not go below `4`, in the same round.
   A breach rejects regardless of the outcome, and means the instrument is wrong rather
   than the strategy good.
5. **And the complexity is worth carrying** — a judgment, written as one sentence in
   `verdict.reason`.

Clauses 1–4 are arithmetic.
Clause 5 is not, and an unattended runner may apply it only in the conservative
direction: it may decline a marginal win and must not accept one.

**Equal budget or no comparison.** Two strategies compared at different `--budget-moves`
have not been compared.
The budget is moves, not wall time, so results are portable across machines.

## Budget and stop conditions

| Budget | Value |
| --- | --- |
| Per round | 5 seeds × 8 chains × 100M moves per cell (~40 s per cell on 8 cores) |
| Per session | 8 hours, or 40 rounds |
| Per hypothesis | 3 rounds, then it must be `abandoned` with `reopen_when` |

Stop, do not adapt, on: budget exhausted; queue empty; three consecutive guard refusals
or crashes; a control cell breaching; any invariant check failing; or a decision that
needs a human. Exit non-zero on an abnormal stop.

## Running one round

```bash
cd explorations/packing
./sqsearch/target/release/sqsearch --selftest   # gate; refuse to record if it fails
./run_baseline.sh                               # or a strategy's own invocation
./test.sh                                       # engine gate + record invariants + drift
```

Then write the artifact into `series/<current>/experiments/`, lifting every number from
the JSONL in `results/` rather than retyping it, and commit artifact, raw runs and
regenerated views together.

`ledger.py` needs PyYAML. `test.sh` picks an interpreter that has it, falling back to a
pinned `uv run --with pyyaml==6.0.3 --with jsonschema==4.26.0 python3`; run it the same
way if invoking `ledger.py` directly.

## What a runner may not do

The full list is in
[`unattended.md`](../../../.agents/skills/experiment-loop/references/unattended.md).
The ones specific to this campaign:

- Do not change the accept rule, the tolerances, the metric vector, or the control
  cells.
- Do not record `beat_record: true` at any precision below `exact`.
- Do not edit `../frontier/` to match a search result.
  The frontier records the literature; a genuine improvement is a separate, deliberate,
  human-reviewed change.
- Do not compare strategies at unequal `--budget-moves`.
- Do not delete a run that came out badly.
  Negative results are the point.

## Layout

```
campaign/
  README.md              this runbook, spans every series
  ideas.md               the idea board: the whole idea space on one page
  schemas/               the four contracts, specialised from the skill's assets
  explorations/          X-NNN idea reports, free-form
  hypotheses/            H-NNN registry, spans every series
  series/001-smoke-n11/  the first pass: reproductions and obvious hypotheses
    README.md            the series artifact: goal, instrument, why it exists
    experiments/         exp-NNN, one per round
    results/             raw JSONL from the engine
  ledger.py              regenerates ledger.md and runs the whole-set checks
  ledger.md              generated; never hand-edited
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
