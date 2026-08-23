# The `s(n)` search campaign — runbook

An [experiment loop](../../../.agents/skills/experiment-loop/SKILL.md) aimed at the
search side of square packing.
This file is the contract every round is run under: the question, the metric vector, the
accept rule, and the budget.
It is frozen while rounds are running — see
[what a runner may not do](#what-a-runner-may-not-do).

## The campaign question

**What is the structure of the `s(n)` landscape — how many basins, how rare is the
record’s, and which proposers reach which — with records as corollaries rather than the
objective?**

This is the
[search-philosophy report’s](../docs/project/research/research-2026-08-23-search-philosophy-and-landscape-cartography.md)
framing, adopted here: **the map is the deliverable.** The campaign’s original question
— which strategies reach the standing best — is the special case that asks about one
basin only, and it remains a sub-question rather than the goal.

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
| 10 | **positive control** (machinery only) | `3 + 1/√2 = 3.70710678…`, proved | Known answer, and *not* the grid. But its mechanism is a 45° tilt, so passing it proves the machinery and says nothing about finding an oblique record — see the caveat below. |
| 11 | **target** | `3.87708359002281…`, Trump 1979 | The smallest open case, smallest open gap with a non-trivial record, degree-8 and rigid. |
| 12 | **negative control** | `4`, the trivial grid | The 4×4 grid is almost certainly optimal. A run that “beats” it has found a bug, not a packing. |
| 17 | **mechanism-matched calibration** | `4.67553009360455`, Bidwell 1998, still open | The nearest case whose record uses genuinely *oblique* structure — the corpus records tilts of `0°` and `±40°`, so two non-trivial orientations against a grid frame. The only cell here that speaks to record-*finding* rather than machinery. |

**The first three cells calibrate machinery, not strategy.** Both proved cases in the
ladder are 45°-tilt mechanisms, symmetric and reachable by blind search; `n = 11` needs
an oblique core at `≈ 40.182°`, a mechanism **no proved case exercises**. An engine can
ace `n = 5` and `n = 10` and remain structurally blind to what the target demands.

That is why `n = 17` joins the standing sweep rather than waiting: it is cheap to carry,
and rediscovering an oblique record is the only calibration that speaks to
record-finding. The other two mechanism-matched targets — `n = 11` at inflated `δ`, and
basin-entry tests — are registered separately.

Standing bests are read from [`../frontier/`](../frontier/README.md) — `n-010.md`,
`n-011.md`, `n-012.md` — never retyped into a round.
The frontier artifacts are the campaign’s source of truth for what is already known, and
a round that moved the frontier would edit one file.

## Who owns a hypothesis

A hypothesis can exist in three forms — prose in the
[standing review’s register](../docs/project/reviews/review-2026-08-23-toolkit-docs-and-first-experiments.md#the-hypothesis-register),
a codified artifact under `hypotheses/`, and a bead.
One rule settles which is true:

> **Once codified, the registry artifact is canonical.** The review’s register entry
> becomes historical. Beads track build work, never scientific claims.

So a claim’s criterion, tier, kill condition and status are read from the artifact and
nowhere else; a bead may say “build the instrument for H-002” but never “H-002 is
confirmed”. The eleven uncodified entries (`H-003`–`H-010`, `H-013`–`H-015`) are still
prose, their ids reserved and enforced, until someone codifies them.

## The three tiers

A number’s tier is recorded as `subject.precision`, and it decides what the number may
claim.

| Tier | What it is | May claim |
| --- | --- | --- |
| `f64_screen` | [`sqsearch`](../sqsearch/) — annealing that minimises the enclosing side, ~40M moves/s | a candidate was proposed |
| `polished` | **LP-in-cell quench** ([H-002](hypotheses/H-002-lp-in-cell-polish.md)) — fix angles and axis assignment, solve the cell’s linear program | a numerical endpoint candidate valued to solver precision; a candidate worth classifying and certifying |
| `exact` | [`sqpack`](../README.md#exact-verification) — separating-axis over the packing’s own algebraic number field | **validity, and only here: a record** |

The middle tier is numerical polish, not exact certification.
For fixed angles and a fixed separating-axis assignment, minimising `s` is a **linear
program**, so the quench can reproduce the cell optimum to the floating-point solver’s
precision. Exact value and terminal-component identity require separate evidence.
That is what turns “where the annealer stopped” into “which cell this is” — the
difference between a tolerance-dependent artifact of the cooling schedule and a
discrete, nameable, exactly-valued object.
Basin identity, the census, the atlas and every descriptor depend on it, which is why it
is the registry’s top priority and not yet built.

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
| `pair_tests` | cost | **the budget currency**; tiers S/M/L = `1e9`/`1e11`/`1e13`. Machine-independent, unlike wall clock |
| `moves`, `seconds` | cost | engine summary; reported alongside as a courtesy |
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
4. **Guards.** The `n=10` positive control lands within `1e-2`; every stored pose passes
   an independent geometry check; and deliberately invalid fixtures are rejected in the
   same instrument build.
   `n=12` is an open research case, not a negative control: a valid side below `4` would
   require exact promotion, not automatic rejection.
5. **And the complexity is worth carrying** — a judgment, written as one sentence in
   `verdict.reason`.

Clauses 1–4 are arithmetic.
Clause 5 is not, and an unattended runner may apply it only in the conservative
direction: it may decline a marginal win and must not accept one.

**Equal budget or no comparison.** Two proposers compared at different budgets have not
been compared. The currency is **pair-tests**, not wall clock and not moves: it is
machine-independent and comparable across proposers whose move semantics differ, which
matters as soon as δ-continuation and archive-based search sit beside annealing.
`sqsearch` currently reports moves only; emitting a pair-test counter is a tracked work
item.

## Budget and stop conditions

| Budget | Value |
| --- | --- |
| Per round | tier S = `1e9` pair-tests; tier M = `1e11`; tier L = `1e13` |
| Per session | 8 hours, or 40 rounds |
| Per hypothesis | 3 rounds, then it must be `abandoned` with `reopen_when` |
| Per round, wall clock | declare a `timebox` before starting; stopping when it expires is an outcome, not a failure |

Stop, do not adapt, on: budget exhausted; queue empty; three consecutive guard refusals
or crashes; a control cell breaching; any invariant check failing; or a decision that
needs a human. Exit non-zero on an abnormal stop.

### Effort, and how a round ends

Every terminal round carries an `effort` block, and the gate refuses one without it.
It exists so the record can answer two questions months later that no verdict can: *what
did this cost*, and *is the question still open?*

| Field | What it carries |
| --- | --- |
| `timebox` | the give-up bound, declared **before** the round starts |
| `wall_seconds` | compute time, lifted from the run data |
| `agent_minutes` | operator time — building, analysing, writing up |
| `pair_tests` | the machine-independent budget currency |
| `stopped_by` | why the round ended: `criterion`, `timebox`, `saturation`, `guard`, `error`, `dependency` |

`stopped_by` is the field that matters.
A round that stopped on its `criterion` answered its question, whichever way it fell.
A round that stopped on its `timebox` did not — the question is still open, the budget
is already spent, and the round must say in `verdict.resume_from` where a successor
picks it up.
The gate enforces exactly that, so a timeboxed round cannot quietly become a
dead end.

Three terminal states are distinct on purpose, and the difference is what a future agent
should do:

- **`rejected`** — the criterion was measured and missed.
  The claim is refuted *for this cell and regime*; a different regime may still say
  otherwise.
- **`abandoned`** — the budget ran out with no determination.
  Not refuted, out of promise for now: `budget_spent`, `best_reached`, `reopen_when`.
  Resumable, and listed in the ledger’s **Resumable** section.
- **`exhausted`** — the stronger claim: re-running under this regime would add nothing.
  Requires `reopen_when` naming a *change of instrument or regime*, not merely more
  budget. This is how a line of work is closed without pretending it was refuted.

The ledger derives cumulative effort per hypothesis and totals it, so “how much has gone
into this claim” is a generated number rather than an impression.

## Running one round

Two ways, and the difference is who is watching.

### With the harness — [`runner.py`](runner.py)

Each step does one thing, the same way, always.
An agent drives them; nothing here needs a human awake.

```bash
cd explorations/packing
./test.sh --strict                                   # must be clean before a night starts
uv run python campaign/runner.py status              # queue, in-progress, last session
uv run python campaign/runner.py preflight           # fire every guard and report

uv run python campaign/runner.py claim H-020         # -> exp-011
uv run python campaign/runner.py execute exp-011     # run the declared command, archive it
uv run python campaign/runner.py record  exp-011     # decide, write the round, commit

uv run python campaign/runner.py run --session-hours 8   # the middle three, over the queue
```

**State lives on disk, never between steps.** `claim` writes the stub, `execute` appends
to the archive beside it, `record` reads that archive back.
So a step that fails loses nothing: fix what it named and re-run *that step*, not the
session. `execute` truncates its archive first, so re-running it never double-counts.

`runner.py release exp-011 --why "..."` gives up a round that died, recording it as
`unresolved` rather than deleting it, and returns its hypothesis to the queue.

Two refusals worth knowing, because they are structural rather than advisory:

- **The harness cannot write the accepting verdict.** Clause 5 is a judgment, and an
  unwatched runner may apply it only in the conservative direction.
  A round passing clauses 1–4 is recorded `unresolved` with `needs_review: true` and
  waits for you. There is no code path that does otherwise, and `preflight` checks that
  there is not.
- **A hypothesis without a `runner` recipe is never run.** `instrument` is prose for a
  human; `runner.command` is the machine-readable form.
  A hypothesis carrying only the former is reported as needing an operator, never
  improvised into a command.

#### The experiment contract

The harness holds no experiment code and an experiment holds no harness code.
An experiment is a **command** declared in its hypothesis, run once per `{n}` and
`{seed}`, which must print JSON Lines carrying `best_side` and an `overlap` of exactly
zero on every result line, and exit 0. The seed’s result is the *minimum* `best_side`
over its lines, so nothing has to agree about which line is the summary.

Adding an experiment therefore never edits `runner.py`. Writing new experiment code is
expected; writing new harness code per round is the error-prone step this removes,
because it is code that runs once, at 3am, having never been exercised.

#### Before the first night on a new machine

```bash
uv run python campaign/runner.py preflight
```

**The regime is part of the result.** `moves` is the budget unit and the engine is
deterministic in its seed, so `best_side` reproduces across machines; wall clock does
not. Measured 2026-08-23: ~40M moves/s on the M1 Pro of the recorded regime, ~14.9M on a
4-core cloud container at `n = 11` and ~9.9M at `n = 17`. Size a timebox against the
machine you are actually on.

### Watched — by hand

```bash
./sqsearch/target/release/sqsearch --selftest   # gate; refuse to record if it fails
./run_baseline.sh <archive.jsonl>               # or a strategy's own invocation
./test.sh                                       # engine gate + record invariants + drift
```

Then write the artifact into `series/<current>/experiments/`, lifting every number from
the JSONL in `results/` rather than retyping it, and commit artifact, raw runs and
regenerated views together.

This is still the right path for any round whose analysis is the work — a new refiner, a
new probe, anything the recipe vocabulary cannot express.
Ten of the eleven rounds so far went this way, at **275 agent-minutes against 16.4
cpu-minutes**: this campaign’s cost has never been the compute, and the runner does not
change that.
It removes the *waiting* from the rounds that are pure engine time, which is
a smaller claim than it sounds and still the difference between one round a night and a
queue draining while nobody is up.

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

## Series

The series map 1:1 onto the
[standing review’s plan](../docs/project/reviews/review-2026-08-23-toolkit-docs-and-first-experiments.md#series-and-priorities):
`series-000` is S0, `series-001` is S1, and so on through S6.

| Series | Purpose | State |
| --- | --- | --- |
| `series-000` (S0) | smoke and calibration; every baseline metric’s first point | **open** |
| `series-001` (S1) | `n = 11` baseline campaign with canonical basins in place | not opened |
| `series-002` (S2) | `n = 12`, seeding and the LP-dual probe | not opened |
| `series-003` (S3) | opportunistic `m² − 3` slot | not opened |
| `series-004` (S4) | proof lane, after PoseBox | not opened |
| `series-005` (S5) | structured search: angle-class engine | not opened |
| `series-006` (S6) | landscape cartography — the atlas, the premise, the ladders | not opened |

S6 *interleaves* with S1 rather than following it: S1’s basin byproducts are the
census’s inputs.

## Where this sits

The campaign is the *experiment record*; the toolkit that produces the numbers is
specified in
[plan-2026-08-22-minimal-packing-toolkit.md](../docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md),
whose Phase 2 (the quench spine) is what makes basins nameable and this record’s
`polished` tier real.
The hypothesis registry here is the codified form of the
[standing review’s register](../docs/project/reviews/review-2026-08-23-toolkit-docs-and-first-experiments.md#the-hypothesis-register);
`H-001`–`H-015` are its ids, reserved even where not yet codified, and this campaign’s
own claims start at `H-016`.

## Layout

```
campaign/
  README.md              this runbook, spans every series
  ideas.md               the idea board: the whole idea space on one page
  schemas/               the four contracts, specialised from the skill's assets
  explorations/          X-NNN idea reports, free-form
  hypotheses/            H-NNN registry, spans every series
  series/series-000-smoke-and-calibration/   S0: reproductions and machinery gates
    README.md            the series artifact: goal, instrument, why it exists
    experiments/         exp-NNN, one per round
    results/             raw JSONL from the engine
  runner.py              harness steps: status, preflight, claim, execute, record, run
  ledger.py              regenerates ledger.md and runs the whole-set checks
  ledger.md              generated; never hand-edited
  session-report.md      generated by runner.py, one per unattended session
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
