# The `s(n)` Research Campaign — W6 Runbook

An [experiment loop](../../../.agents/skills/experiment-loop/SKILL.md) for the durable
square-packing research program.
This file owns W6, `research-loop`: the contract every experiment round runs under—the
question, metric vector, accept rule, and budget.
The [synopsis](../SYNOPSIS.md#workflow-entry-contracts) owns the seven workflow entry
points and the distinction among campaign, series, session, experiment, round, and run.
It is frozen while rounds are running — see
[what a runner may not do](#what-a-runner-may-not-do).

The [research loop logbook](research-loop-logbook/README.md) gives each bounded
user-level run a reader-first synopsis.
Experiment artifacts remain the authoritative positive and negative scientific result
record, agent sessions retain phase history, and `defects.yaml` remains the separate
toolchain-defect log.
The logbook also separates new round results from prior retained results used by the
run; neither category implies the separate novelty assessment owned by
`frontier/evidence.yaml`.

## The Current Search Objective

**What is the structure of the `s(n)` landscape — how many basins, how rare is the
record’s, and which proposers reach which — with records as corollaries rather than the
objective?**

This is the
[search-philosophy report’s](../docs/project/research/research-2026-08-23-search-philosophy-and-landscape-cartography.md)
framing for the current search lane: **the map is the deliverable.** The campaign itself
is broader: it also contains exact proof, validation, local-geometry, construction, and
infrastructure questions under the same registry and evidence contract.
Its original search question—which strategies reach the standing best—is the special
case that asks about one basin only, and it remains a sub-question rather than the
search goal.

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

The **subject** records the instrument, assurance, method, actual precision, tolerance,
and arithmetic regime.
Never extrapolate from a numerical result to a formal claim, or from one numerical
regime to another.

The **instance axis is `n`**, and the standing cells have different jobs:

| `n` | role | standing best | why this cell |
| --- | --- | --- | --- |
| 10 | **positive control** (machinery only) | `3 + 1/√2 = 3.70710678…`, proved | Known answer, and *not* the grid. But its mechanism is a 45° tilt, so passing it proves the machinery and says nothing about finding an oblique record — see the caveat below. |
| 11 | **target** | `3.87708359002281…`, Trump 1979 | The smallest open case and a degree-8 side construction; exp-013 proves qualitative local isolation, while a radius and global optimality remain open. |
| 12 | **open-case calibration** | `4`, the trivial grid | The 4×4 grid is the standing best, not a proved optimum. A numerically lower side would be a candidate and must enter formal promotion before it changes the verified frontier. |
| 16 | **proved not-below control** | `4`, proved | A reported side below `4` is known to be invalid. This is the valid replacement for the old `n=12` guard. |
| 17 | **mechanism-matched calibration** | `4.67553009360455`, Bidwell 1998, still open | The nearest case whose record uses genuinely *oblique* structure — the primary SVG records `0°`, `+39.80496°`, and `−36.62379°`, so two unequal non-trivial orientations against a grid frame. The only cell here that speaks to record-*finding* rather than machinery. |

**The proved ladder cells calibrate machinery, not strategy.** Both proved cases are
45°-tilt mechanisms, symmetric and reachable by blind search; `n = 11` needs an oblique
core at `≈ 40.182°`, a mechanism **no proved case exercises**. An engine can ace `n = 5`
and `n = 10` and remain structurally blind to what the target demands.

That is why `n = 17` joins the standing sweep rather than waiting: it is cheap to carry,
and rediscovering an oblique record is the only calibration that speaks to
record-finding. The other two mechanism-matched targets — `n = 11` at inflated `δ`, and
basin-entry tests — are registered separately.

Standing bests are read from [`../frontier/`](../frontier/README.md)—`n-010.md`,
`n-011.md`, `n-012.md`, `n-016.md`, and `n-017.md`—never retyped into a round.
The frontier artifacts are the campaign’s source of truth for what is already known, and
a round that moved the frontier would edit one file.

## Who owns a hypothesis

A hypothesis can exist in three forms — prose in the
[standing review’s register](../docs/project/reviews/review-2026-08-23-toolkit-docs-and-first-experiments.md#the-hypothesis-register),
a codified artifact under `hypotheses/`, and a bead.
One rule settles which is true:

> **Once codified, the registry artifact is canonical.** The review’s register entry
> becomes historical. Beads track build work, never scientific claims.

So a claim’s criterion, required assurance, kill condition, and status are read from the
artifact and nowhere else; a bead may say “build the instrument for H-002” but never
“H-002 is confirmed”.
All fifteen entries from the standing review are now codified.
Later ids carry campaign-native claims and explicit open questions.

## The Bounded Research Cycle

The campaign keeps a broad portfolio, while one W6 round addresses one narrow registered
question at a time. Other workflows use the same discipline but leave different
artifacts; their contracts live in the synopsis rather than in this experiment runbook.
This distinction protects both creativity and completion: ideas are cheap to capture,
but only a preregistered slice may consume the current clock.
Routine work declares `research-loop`, its objective, expected artifact, and focused
check where the round is already tracked.
An escalated session phase also declares one primary focus from the packing program’s
[four operating focuses](../README.md#operating-principles).
A material focus change starts a new phase even when the workflow remains W6; a brief
change of emphasis does not.
The other three principles continue to constrain and contribute to the work.

The protocol is agent-neutral.
Its authoritative state is the repository: the hypothesis and idea board say what may be
tried, `tbd` owns dependencies and tracked work, the active launch agenda freezes the
executable portfolio when bead state is under reconciliation, and experiments, defects,
commits, and bead notes preserve what happened.
An [agent-session artifact](agent-sessions/README.md) records what the session is
trying, when it stops, and its outer-loop recovery state only when the escalation
criteria apply. Conversation history, a native goal, and a watchdog are useful
controllers, but none is the only copy of a decision or result.

### Supervision Defaults for Escalated Sessions

These clocks are defaults for long autonomous supervision, not requirements for a
routine round or mathematical accept rules.
An active agent-session artifact records one absolute start and deadline bounded by its
wall budget; a new phase cannot reset them.
Ordinary phases end before the finalization reserve, and one explicitly designated final
phase may use that reserve for reconciliation.
Choose a cadence proportional to command cost, recovery cost, and uncertainty before the
work starts. A checkpoint may change later supervision cadence prospectively when
retained evidence shows the original cadence is unsuitable; it may never change a
round’s hypothesis, criterion, regime, or scientific budget after seeing the result.
A long numerical or proof computation keeps its separately preregistered round timebox,
while the agent still checkpoints its supervision work on this cadence.
An escalated active phase records its expected output, validation command, stopping
condition, fallback, start, and deadline.
Outcome and evidence are recorded only when it closes.

| Clock | Default | Required outcome at the boundary |
| --- | ---: | --- |
| Orientation | 10 minutes | Confirm the workflow, question, owning artifact, focused check, and the fuller session fields when escalation applies |
| Evidence checkpoint | 20 minutes | Produce a passing check, minimized failure, retained measurement, source-bound derivation, or explicit blocked result; prose about continued investigation is not evidence |
| Active slice | Up to 30 minutes | Integrate a coherent checkpoint, or stop and preserve the partial work with its exact limitation; continuation requires a newly stated slice and clock |
| Finalization reserve | 15 minutes | Stop new work before the session deadline; reconcile artifacts, defects, beads, generated views, commits, pushes, and the next action |
| Research command | Declared per hypothesis | Terminate or return at its own wall-clock bound and retain its stopping reason and resumable state |

For multi-hour work, state the bounded slice plan through the next integration
checkpoint before acting.
Unless the user declares another cadence, place that checkpoint within about four hours.
Thirty minutes is the maximum allocation before an inventory, not the default duration.
Close a 5-, 10-, 15-, 20-, or 25-minute slice when its bounded output is complete; never
pad it to fill the clock.
Allocate another slice only after checking progress, dependency state, information
value, and the remaining finalization reserve.
At every slice boundary, compare measured command, coordinator, and delegation time with
the estimates, finalization start, and session deadline.
Shorten, split, reorder, or defer only future slices; never move a declared deadline or
alter a frozen scientific contract after seeing results.

A durable handoff must leave a coherent checkpoint.
Commit coherent work; when interruption makes that impossible, preserve the partial
state with its reproducer, limitation, and next decision in the owning bead or escalated
session record. Raw results that already answer a preregistered question are committed
even when the answer is negative or invalid.

### One Slice

1. **Select.** Re-screen the portfolio and choose the highest-information ready action,
   not merely the most recent idea.
2. **Declare.** Confirm the workflow, question, promised artifact, narrow validation,
   and scientific budget before acting.
   Add focus, outer clock, stopping condition, and fallback when the session escalation
   criteria apply.
3. **Execute.** Take the smallest action that can answer the question.
   Use available sub-agents or delegates for independent read-only or disjoint-write
   work under the same clock.
   The delegation inherits the coordinating phase unless it opens its own independently
   tracked session. One coordinator owns shared records, integration, commits, and
   external updates.
4. **Checkpoint.** At the declared evidence checkpoint, preserve concrete evidence.
   A result may be positive, negative, invalid, or blocked; each advances the record if
   its evidence is replayable.
5. **Stop or renew.** At the declared slice boundary, integrate, preserve, or abandon
   the slice. Compare measured elapsed time with the remaining plan and finalization
   reserve before selecting the next slice.
   Never extend it merely because the answer feels close.
   A successor slice must state what new fact makes another bounded attempt worthwhile.
6. **Record once.** Route an idea to the idea board or a new `H-NNN`, a measurement to
   raw data and `exp-NNN`, an implementation task to its bead and owning workflow, and
   an actual error to `defects.yaml` with its detector and regression.
7. **Commit and re-screen.** Regenerate owned views, run the narrowest sufficient gate,
   commit and push the checkpoint, then choose again from the now-current queue.

New tangents do not disappear and do not hijack the clock.
Record one as a bead, defect, exploration report, hypothesis, or open question according
to what it is; pursue it immediately only when it falsifies the active slice’s premise
or outranks the queue under an explicit re-screen.

### Workflow Checkpoints

At a slice boundary, either renew W6 under a newly stated question or close the phase.
A renewal closes the old phase and opens another with a changed objective, a new clock,
and the new evidence that earns another slice; workflow and focus may stay the same.
Close the active phase before changing purpose or material focus.
Record status, evidence, stop reason, and next action in the agent-session artifact when
one exists; otherwise use the experiment and owning bead without creating a duplicate
record.
A promoted, novel, disputed, or otherwise high-risk claim receives an independent
W2 audit. A routine guarded result whose preregistered criterion and independent replay
already decide its claim may proceed directly to W3 or another W6 slice.
Generating a successor hypothesis enters W3; reviewing a process failure enters W4;
optimizing a measured bottleneck enters W5; and building or repairing a reusable
packing-pipeline capability enters W7. A W6 phase may prepare an instrument specific to
its registered round, but measurement begins only after the hypothesis, criterion,
budget, and instrument are ready and frozen.
A missing cross-round capability or a material change to a shared trust boundary stops
W6 and hands off to W7, then W2 when independent review is required.

A user request may cause the same transition immediately, but it does not erase the
phase already performed.
The ordered phase history is the account of what the session actually did.

### Supervisors and Watchdogs

A supervisor and its default cadence are optional; the registered round contract is not.
When available, use a native long-running goal to maintain the session objective and a
periodic watchdog to inspect repository evidence.
The watchdog checks elapsed wall time, the latest experiment or commit, the active bead,
and the agent-session next action.
At the declared evidence checkpoint it requests concrete evidence; at the declared slice
boundary it requires the current slice to stop or be restated.
It never changes a hypothesis, criterion, threshold, or mathematical verdict.

An agent without native goal or watchdog support uses bounded command execution and the
smallest retained state needed for recovery.
A human, cron job, CI task, or small shell/Python supervisor may poll the same durable
state. This makes the safety property portable: replacing Codex with Claude, another
coding agent, or a human changes the driver, not the research contract.

## Campaign Agendas

A hypothesis registry is deliberately broad, while one agent session is deliberately
narrow.
A campaign agenda is the small coordination layer between them: an ordered set of
bounded commitments that can be reprioritized at a checkpoint or divided among agents
without changing a scientific claim.

The active [basin-map confidence ladder](agendas/agenda-001-basin-confidence-ladder.md)
separates three purposes:

- `tool_validation` tests whether this repository emits, retains, replays, and checks
  the evidence it says it does;
- `measurement_validation` tests whether the counted object or estimator agrees with
  mathematical ground truth; and
- `research` asks about the packing landscape itself and remains blocked until its
  validation dependencies pass.

The agenda frontmatter is a lightweight soft schema, not an executable scheduler.
It stores stable commitment IDs, priorities, budgets, prerequisites, beads, and promised
evidence; the body carries the rationale.
Hypotheses still own criteria, experiment artifacts still own measurements, `tbd` still
owns work dependencies, and the active session still owns the clock.
`packing-campaign` does not consume an agenda.

Update an agenda only at a checkpoint.
A completed item means its bounded question has a retained answer, not that a basin map
or hypothesis is complete.
The generated ledger shows agenda states alongside experiments so the next agent does
not need conversation history to find the next ready commitment.

## Assurance and Method

Every experiment records assurance separately from the method and arithmetic that
produced it.

| Assurance | What it means | May claim |
| --- | --- | --- |
| `numerically-checked` | A finite computation under the recorded method, precision, rounding, and tolerance | The scoped numerical outcome and a candidate for further work |
| `verified` | An exact check, rigorous certificate, or complete proof with discharged preconditions | The scoped formal conclusion; `beat_record: true` only when a verified feasible witness beats the comparator |

Source reports live in the frontier’s `reported` lane rather than experiment assurance.
Methods include `numerical-f64`, `numerical-multiprecision`, `interval-certified`,
`exact-algebraic`, and the proof methods defined in the synopsis.
A result records the precision actually used; neither a multiprecision library nor a
small tolerance makes a calculation verified.

**Polish is an operation, not an assurance class.** For fixed angles and a fixed
separating-axis assignment, minimizing `s` is a linear program, so the quench can
produce an endpoint candidate at the floating-point solver’s recorded precision.
Exact value and terminal-component identity require separate evidence.
That is what turns “where the annealer stopped” into “which cell this is” — the
difference between a tolerance-dependent artifact of the cooling schedule and a
discrete, nameable, exactly-valued object.
Basin identity, the census, the atlas and every descriptor depend on it, which is why it
is the registry’s top priority and not yet built.

The assurance boundary is mathematical, not administrative.
A record packing has pairs touching at *exactly* zero separation — 14 of the 55 pairs in
Trump’s — and no floating-point check can decide those: a tolerance loose enough to
accept true contact is loose enough to accept a small overlap.
That is the reason `sqpack` exists, and it is why `beat_record: true` requires
`assurance: verified`.

## The metric vector

Fixed for the campaign.
Recorded on every round; the role says what each may conclude.

| Metric | Role | Source |
| --- | --- | --- |
| `best_side` | **outcome** | smallest numerically accepted or formally verified side found, with assurance carried by the subject |
| `outcome` | **outcome** | `determination`: generic `criterion_met` / `criterion_missed`, or the search-specific `beat_record`, `reached_basin`, `near_miss`, `no_progress`, `invalid` |
| `pair_tests` | cost | **the budget currency**; tiers S/M/L = `1e9`/`1e11`/`1e13`. Machine-independent, unlike wall clock |
| `moves`, `seconds` | cost | engine summary; reported alongside as a courtesy |
| `overlap` | **guard** | numerical penetration depth under the declared screen arithmetic; a non-zero value invalidates the run but zero does not make it formal |
| `selftest_passed` | **guard** | `sqsearch --selftest` before any run is recorded |
| control cells | **guard** | `n=10` must land within `1e-2`; proved `n=16` must not go below `4` |
| `restarts`, `accepted`, `moves_per_sec` | mechanism | engine summary |
| spread of `best_side` across seeds | mechanism | five seeds per cell, always |

`reached_basin` means `best_side − standing_best < 1e-4`. That is a **numerical proxy**
for “found the right combinatorial class”, not a proof of it; confirming the class needs
a separately scoped structural check or formal certificate.
Rounds that claim `reached_basin` should say which they mean.

## The accept rule

Written before the first measurement, and not changed while rounds are running.
A candidate strategy is **accepted** when all of:

1. **Outcome.** Its median `best_side` across ≥5 seeds is below the control’s median,
   and the two seed ranges do not overlap — or it reaches `reached_basin` on a cell
   where the control does not.
2. **Evidence.** Five seeds per cell minimum, median and min–max range both reported.
   Overlapping ranges mean *no detectable effect*, never “a small win”.
3. **Numerical guard.** Every reported configuration has `overlap == 0` under the
   declared screen arithmetic, and the engine selftest passed in the same invocation.
   This decides whether the numerical round is usable; it does not verify feasibility.
4. **Guards.** The `n=10` positive control lands within `1e-2`; the proved `n=16`
   not-below control never reports a side under `4`; every stored pose passes an
   independent geometry check; and deliberately invalid fixtures are rejected in the
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
`sqsearch` now emits exact search-path `pair_tests` on every ordinary chain, basin-entry
trial, and summary. The count is one `pair_depth` evaluation of one unordered square
pair: one full scan per restart, both local scans per move, and one final
retained-configuration scan.
It excludes the basin-entry command’s one-time seed diagnostic and independent
verification work, which are setup and verifier receipts, not proposer budget.
Budget enforcement, campaign adapters, and cross-proposer comparisons are still
move-denominated, so no equal-pair-budget comparison is yet admissible.

## Budget and stop conditions

| Budget | Value |
| --- | --- |
| Per round | tier S = `1e9` pair-tests; tier M = `1e11`; tier L = `1e13` |
| Default per session | 8 hours, or 40 rounds |
| Per hypothesis | 3 rounds, then it must be `abandoned` with `reopen_when` |
| Per round, wall clock | declare a `timebox` before starting; stopping when it expires is an outcome, not a failure |

Stop, do not adapt, on: budget exhausted; queue empty; three consecutive guard refusals
or crashes; a control cell breaching; any invariant check failing; or a decision that
needs a human. Exit non-zero on an abnormal stop.

The per-session value is a default safety bound, not a hard research limit.
A longer user-level horizon may use multiple source sessions under one mutable agenda,
or an explicitly reviewed longer session when that has less coordination cost.
Reassess the pipeline, evidence quality, throughput, and remaining portfolio before
extending the clock.
Preserve a protected finalization reserve under either form.

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

### With the harness — [`packing-campaign`](../src/sqpack/campaign/runner.py)

Each step does one thing, the same way, always.
An agent drives them; nothing here needs a human awake.

**Current launch status: NO-GO for unattended numeric work.** The commands below are the
interface, not evidence that the queue is ready.
The only operational recipe projects to about 2.8 hours locally, and independent pose
validity, lifecycle recovery, durable reports, and per-cell queue pricing remain open.
Use the
[current readiness agenda](../docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md)
for the exact 8-hour and 24-hour gate.
The H-020/exp-011 identifiers below are a historical lifecycle example, not a
copy-pastable ready round; `status` and the confidence ladder own the live queue.

```shell
cd explorations/packing
uv run --frozen --group dev packing-validate --strict
uv run --frozen packing-campaign status
uv run --frozen packing-campaign preflight

uv run --frozen packing-campaign claim H-020
uv run --frozen packing-campaign execute exp-011
uv run --frozen packing-campaign record exp-011

uv run --frozen packing-campaign run --session-hours 8
```

**State lives on disk, never between steps.** `claim` writes the stub, `execute` appends
to the archive beside it, `record` reads that archive back.
So a step that fails loses nothing: fix what it named and re-run *that step*, not the
session. `execute` truncates its archive first, so re-running it never double-counts.

`packing-campaign release exp-011 --why "..."` gives up a round that died, recording it
as `unresolved` rather than deleting it, and returns its hypothesis to the queue.

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

#### The Experiment Contract

The harness holds no experiment-specific code, and an experiment holds no harness code.
An experiment is one durable `exp-NNN` record for one round.
Its executable recipe is a **command** declared in the hypothesis.
The harness invokes that command once per `{n}` and `{seed}`; each invocation is a run
inside the experiment.
It must print JSON Lines carrying `best_side` and an `overlap` of exactly zero on every
result line, and exit 0. The seed’s result is the *minimum* `best_side` over its lines,
so nothing has to agree about which line is the summary.

Adding an experiment therefore never edits the campaign runner.
Writing new experiment code is expected; writing new harness code per round is the
error-prone step this removes, because it is code that runs once, at 3am, having never
been exercised.

#### Before the first night on a new machine

```shell
uv run --frozen packing-campaign preflight
```

**The regime is part of the result.** `moves` is the budget unit and the engine is
deterministic in its seed, so `best_side` reproduces across machines; wall clock does
not. Measured 2026-08-23: ~40M moves/s on the M1 Pro of the recorded regime, ~14.9M on a
4-core cloud container at `n = 11` and ~9.9M at `n = 17`. Size a timebox against the
machine you are actually on.

### Watched — by hand

```shell
./sqsearch/target/release/sqsearch --selftest
uv run --frozen python -m cases.campaign_smoke.baseline_sweep <archive.jsonl>
uv run --frozen --group dev packing-validate
```

Then write the artifact into `series/<current>/experiments/`, lifting every number from
the JSONL in `results/` rather than retyping it, and commit artifact, raw runs and
regenerated views together.

This is still the right path for any round whose analysis is the work — a new refiner, a
new probe, anything the recipe vocabulary cannot express.
The first eleven search and quench rounds used this watched path; later corpus and exact
proof rounds use dedicated deterministic checkers.
The generated [ledger](ledger.md#effort) owns the cumulative effort total: this
campaign’s cost has so far been agent analysis rather than machine compute, and the
runner does not change that.
It removes the *waiting* from the rounds that are pure engine time, which is a smaller
claim than it sounds and still the difference between one round a night and a queue
draining while nobody is up.

Use `packing-ledger check` for a read-only campaign check and `packing-ledger render`
after a reviewed artifact change.
Both run in the locked uv environment and share the same invariant implementation.

## What a runner may not do

The full list is in
[`unattended.md`](../../../.agents/skills/experiment-loop/references/unattended.md).
The ones specific to this campaign:

- Do not change the accept rule, the tolerances, the metric vector, or the control
  cells.
- Do not record `beat_record: true` unless `assurance: verified`.
- Do not edit `../frontier/` to match a search result.
  The frontier records the literature; a genuine improvement is a separate, deliberate,
  human-reviewed change.
- Do not compare strategies at unequal `--budget-moves`.
- Do not delete a run that came out badly.
  Negative results are the point.

## Series

The standing review named topical stages S0–S6. Only S0 currently has a series artifact:
`series-000`. The remaining rows are historical planning labels, not current records and
not automatic reasons to open a new series.
A series is earned by a tooling or regime change that affects comparability, recorded in
`opened_because`; a topic change alone does not earn one.

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
numerical refinement record reproducible.
The hypothesis registry here is the codified form of the
[standing review’s register](../docs/project/reviews/review-2026-08-23-toolkit-docs-and-first-experiments.md#the-hypothesis-register);
`H-001`–`H-015` are its now-codified ids, and this campaign’s own claims start at
`H-016`.

## Layout

```
campaign/
  README.md              this runbook, spans every series
  ideas.md               the idea board: the whole idea space on one page
  schemas/               scientific contracts plus the small outer agent-session contract
  agent-sessions/        versioned outer-loop delegation and handoff records
  explorations/          X-NNN idea reports, free-form
  hypotheses/            H-NNN registry, spans every series
  series/series-000-smoke-and-calibration/   S0: reproductions and machinery gates
    README.md            the series artifact: goal, instrument, why it exists
    experiments/         exp-NNN, one per round
    results/             raw JSONL from the engine
  ledger.md              generated; never hand-edited
  session-report.md      generated numeric-runner batch handoff; historical filename,
                         not a versioned session-NNN agent-session artifact
```

The implementation lives in `src/sqpack/campaign/`; the durable campaign state stays in
this directory.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
