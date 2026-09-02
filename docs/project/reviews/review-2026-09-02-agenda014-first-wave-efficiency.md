# Review: Agenda 014 First-Wave Efficiency

**Date:** 2026-09-02

**Author:** Claude, for the project maintainers

**Status:** Complete BC-127 W5 receipt; decision is `no-change`

This is agenda-014’s mandatory W5 `efficiency-loop` slice between the first wave and the
routing checkpoint. It measures the four first-wave blocks at the frozen evidence
revision `1e175108`, applies the predeclared change-admission rule, and routes what
fails it. It changes no scientific instrument, result, criterion or review flag.

The slice ran on a resumed wall.
The owner paused the six-hour run at `02:16Z` after every lane had terminalized, and
this review opened at `04:10Z` on a fresh container from the pushed checkpoint, so the
“remaining wall” in the repayment test is the resumed session’s own budget, not the
original six hours.

## Verdict

Record **`no-change`**.

One candidate was measured well enough to test: the local push tier selected the whole
suite, 1,302 tests, because the new `benchmarks/` root is outside the map that
`reachable_tests` uses to narrow it.
The earlier waves selected 245 and 301 tests for their changes.
That candidate has a frozen input, a completed pre-change run and a configuration-only
rollback seam, but no fixed-input equivalence receipt showing the mapped selection
equals the reachable set, and no positive repayment inside this session, which runs
focused suites during review and the push tier once at close.
Two guards fail; agenda-014 requires all of them.
It becomes a W7 entry rather than a change made during review.

The dominant measured costs are not code hot paths.
They are waiting on delegated agents, one exact serial arm whose paired candidate was
contaminated by host load the lane could not control, and rework found by different-lane
review after author-side tests had passed.
Each of those is a process contract, and each is routed below.

## Measurement Contract

The baseline follows the two agenda-013 W5 reviews, with one addition: the table is
rendered by
[`devtools.render_wave_efficiency`](../../../packing/devtools/render_wave_efficiency.py)
from the AgentSessions and their `CodexTaskTreeDelta/v1` receipts, so every figure is a
field lookup or a count rather than a transcription.
Its controls are
[`tests/test_render_wave_efficiency.py`](../../../packing/tests/test_render_wave_efficiency.py).

- a **cell** is one recorded workflow phase;
- an **output** is one path in `session.outputs`; a **substantive output** excludes the
  session’s own record and every resource receipt;
- **agent-active**, command, agent-wait, model-stream, first-token and compaction time
  are the receipt’s `delta` block;
- a **defect group** is one finding named by a lane record, the coordinator’s checkpoint
  or a preflight card, not an inferred bug count.

The coordinator receipt is a recursive task tree that contains the three lane subtrees,
so it is shown beside the lanes and never added to them.
Two lane receipts and the coordinator receipt were cut while a task was still live and
are lower bounds. Different lane outcomes make output rates descriptive, not causal.

## First-Wave Baseline

| Lane | Terminal state / cells | Agent-active | Command | Agent wait | Timed model stream | First-token wait | Compaction | Responses | Outputs / substantive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| session-073 | stopped / 8 | 6,515.000 s (lower bound) | 2,833.502 s | 1,024.216 s | 889.789 s | 0.000 s | 132.684 s | 279 | 8 / 6 |
| session-074 | completed / 7 | 5,686.517 s (lower bound) | 95.913 s | 1,908.372 s | 1,380.309 s | 6.247 s | 139.895 s | 272 | 8 / 6 |
| session-075 | completed / 7 | 5,093.446 s | 804.037 s | 2,104.759 s | 630.437 s | 11.559 s | 123.167 s | 212 | 8 / 6 |
| **Lane total** | **22 cells** | **17,294.963 s** (lower bound) | **3,733.452 s** | **5,037.347 s** | **2,900.535 s** | **17.806 s** | **395.746 s** | **763** | **24 / 18** |
| session-072 (coordinator, contains the lanes) | stopped / 2 | 31,104.632 s (lower bound) | 6,976.823 s | 8,166.253 s | 5,094.383 s | 75.013 s | 876.717 s | 1467 | 15 / 10 |

Lane totals: 4.996 declared output paths and 3.747 substantive paths per recursive
agent-active hour. Coordinator residual after removing the lane receipts: 8,156.718 s
agent-active (approximate: the cutoffs differ and a lower-bound lane receipt understates
its lane).

The source records are
[session-072](../../../packing/campaign/agent-sessions/session-072-agenda014-six-hour-first-wave.md),
[session-073](../../../packing/campaign/agent-sessions/session-073-bc123-n17-parent-bound-parallel-profile.md),
[session-074](../../../packing/campaign/agent-sessions/session-074-bc124-n68-production-adapter.md),
[session-075](../../../packing/campaign/agent-sessions/session-075-bc125-n50-producer-refusal-ordering.md)
and their [resource receipts](../../../packing/campaign/resource-usage/). BC-126 ran
inside the coordinator’s own tree and has no separate receipt; its three 15-minute cells
are in session-072’s cell log.

Removing the three lane receipts from the coordinator receipt leaves about 13,810 s of
agent-active time, about 3,243 s of command time and about 2,194 s of model-stream time
for the coordinator’s own work, which includes BC-126, four W2 readmission cards, two
packet preflights and the checkpoint publication.
Those residuals are approximate because the four cutoffs differ by up to 22 minutes and
one lane receipt is a lower bound.
The coordinator row was completed after this review was first written: commit `0b632c3e`
on the PR branch extended the session-072 receipt to its full interval, and the row and
residuals above are re-rendered from that receipt.
The three lane receipts and every lane figure are unchanged.

### Where the lane time went

| Lane | Agent wait | Command | Model stream | Compaction | Sum of four | Share of agent-active |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| BC-123, n = 17 | 1,024.216 s | 2,833.502 s | 889.789 s | 132.684 s | 4,880.191 s | 74.9% |
| BC-124, n = 68 | 1,908.372 s | 95.913 s | 1,380.309 s | 139.895 s | 3,524.489 s | 62.0% |
| BC-125, n = 50 | 2,104.759 s | 804.037 s | 630.437 s | 123.167 s | 3,662.400 s | 71.9% |

Agent wait is the largest single category in two of three lanes and 29.1% of the lane
total. Each of those two lanes spawned one delegate for its different-lane W2 admission
and waited on it; the wait is the price of the independence rule, not idle time to be
optimized away, but it is the first time the receipts make its size visible.

Command time is concentrated in the n = 17 lane: 75.9% of the lane command total.
Its one exact serial arm cost 524.743164166 s for three ordinals, with recorded
publication intervals of about 177, 181 and 166 s. The rest of that lane’s command time
is focused suites, four self-test rounds and the replay of the retained arm.
No function-level profile exists for the arm, and the receipt does not separate the
serial arm from the aborted candidate arm.

## Literal-Entry Failures

The second-wave correction held.
BC-124 executed the literal `--record` argv against injected dependencies at
`00:31:54Z`, seventeen minutes into its wall, and BC-125’s single registered command ran
once in 0.72 s at its authorized cell.
Neither lane discovered its command was unreachable late, which is the failure the
agenda-013 review named.

BC-123’s literal pair command first ran at `01:49:22Z`, 94 minutes in, after two W2
rounds. It then stopped on a guard the lane could observe but not enforce: unrelated
CPU-heavy work began during the candidate arm, the contamination kill fired, and arm B
was deleted. No paired sample exists.
The measured cost of that stop is the whole 738 s command wall plus the 15-minute
research cell; the retained value is one serial control that a later round cannot pair
with, because the records forbid pairing a stale control with a fresh candidate.

## Rework and Review Yield

| Lane | Defect groups | Found by | Recorded cost |
| --- | ---: | --- | --- |
| BC-123 | 2 | coordinator W2 (same-basename worker-root escape); second W2 (missing final-assembler controls, symlink and resolved-parent escapes) | 147 s for the first W2; one 15-minute repair cell; guard count 18 to 30 |
| BC-124 | 1 | coordinator manual prepublication diff review (selected-path marker recursed before its depth bound) | fresh different-lane W2 at 35 tests; no time recorded |
| BC-125 | 3 | coordinator publication preflight (order-dependent module state in the n = 50 tests; formatter drift in three content-addressed instrument files); coordinator (H-059 omitted from the launch ownership lists) | not recorded |
| BC-126 | 2 | different-lane packet preflight (no named negative control in the formula tool; retained 2009 HTML missing from its frozen-input table) | not recorded; cards are budgeted at 15--20 minutes |

Eight groups across four blocks, against thirteen in agenda-013’s first wave.
Every lane had at least one finding from a reviewer who did not write the code, and in
three of four the author-side suite and static checks had already passed.
The n = 68 finding is the sharpest case: 34 tests, twenty named mutations, Ruff,
BasedPyright and one independent W2 all passed with the guard in the wrong place, and a
human reading the diff caught it.
A declared bound with no mutation that exceeds it is a guard that has not been tested.

Two of the eight are repeats.
The agenda-013 second-wave review recorded that formatter normalization must precede a
hash freeze; exp-055 froze three files that then needed exclusions.
The n = 54 negative-control gap is the same shape as the agenda-013 finding that a
dependency had been mistaken for an instrument guard: a tool whose only tests are
positive cannot show it would refuse.

## Validation and CI

The local record gate ran in 11.6 s on the unchanged frozen tree at the start of this
session; soft-schema validation is 7.2 s of it.
The push tier at the checkpoint ran 33 named steps and 1,302 reachable tests with 25
exhaustive cases deselected, against 245 and 301 tests for the two agenda-013 waves,
because the validator selected the whole suite for the unmapped `benchmarks/` root.
Session-072 deferred that scope warning to this review.

Hosted checks on `1e175108`: Linux `validate` 779 s, `macos-portability` 50 s and the
required aggregator 2 s. Linux is above the earlier 744--752 s band by about 4%, which
is consistent with the larger selected suite but is end-to-end job time and does not
isolate it. CI was asynchronous and did not sit on the lane or checkpoint critical path.

## Change-Admission Test

The candidate is mapping `benchmarks/` and the new case roots into the reachable-tests
map so the push tier selects tests for a change there instead of running everything.

| Required guard | Evidence | Decision |
| --- | --- | --- |
| Profiled hot path | Step-level: 1,302 selected tests against 245 and 301 in prior waves; no per-step timing was retained | pass, at step level only |
| Frozen input | The checkpoint tree and its push-tier run are frozen at `1e175108` | pass |
| Completed pre-change replay | Session-072’s push tier completed and passed | pass |
| Fixed-input equivalence guard | No receipt shows the mapped selection equals the reachable set for the n = 17 change | fail |
| Rollback seam | The map is configuration in `reachable_tests`; reverting it restores whole-suite selection | pass |
| Positive remaining-wall repayment | This session runs focused suites during review and the push tier once at close; the saving is bounded by one run and the change costs a W7 cell now | fail |
| Disjoint from active lanes and frozen evidence | The validator is not under review and touches no evidence path | pass |

Two guards fail. The decision is `no-change`, and the candidate is routed to W7.

No other candidate reached the table.
The n = 17 arm has no function profile and no completed paired replay; agent wait is the
independence rule’s cost; the rework groups are contract corrections, not optimizations
of an unchanged implementation.

## Routed Work

Each entry below is a future W7 or process-contract item.
None is implemented here, and none touches exp-053, exp-054, exp-055 or the frozen
instrument bytes.

1. **Reachable-tests root map.** Add `benchmarks/` and the first-wave case roots to the
   map, with a control showing the selection for a benchmark-only change equals its
   reachable set. This is the one candidate that passed the frozen-input and rollback
   guards.
2. **Pre-freeze normalization check.** A record check that every file bound by a
   result’s instrument bindings is either formatter-clean or already in the exclusion
   list, run before the hash freeze rather than discovered at publication.
   The same defect has now been recorded in two consecutive agendas.
3. **Bound-exceeding mutations.** Every declared parser or recursion bound in an
   instrument needs a named mutation that exceeds it, listed in the admission receipt.
   The n = 68 depth guard passed 34 tests and an independent W2 without one.
4. **Quiet-host lease receipt.** A paired timing round needs a machine-checked host-load
   receipt before the control arm starts and at each arm boundary, so that a
   contaminated candidate arm stops before the control is spent.
   The kill guard worked; it fired after 524.743 s of control had already been paid.
5. **n = 54 negative control and frozen-input inventory.** Named by BC-126’s own
   next-evidence field; the packet cannot be frozen until they exist.

BC-128 should route from the lane exits as recorded, without treating this review as
having changed any of them: BC-123 earned no continuation, BC-124’s admission is
target-blind and instrument-level, and BC-126 retains its source refusal.

## Limitations

- Receipts are aggregate task-tree deltas, not function profiles; agent wait is not
  split by what was waited on.
- Session-073’s receipt records zero first-token wait, which the other three receipts do
  not; it is reported as read.
- Three of four receipts were cut with a live task and are lower bounds.
- BC-126 has no receipt of its own and no recorded elapsed time; its cost is inside the
  coordinator residual.
- Three elapsed figures coexist for BC-124: 6,843 s operator-reported in session-072,
  5,940 s in exp-054, and 5,686.517 s agent-active in the receipt.
  The table uses the receipt; the others are retained as reported.
- Output counts weigh heterogeneous files equally, and the four blocks differ in kind,
  so rates are descriptive.
- Hosted durations are end-to-end job times.

These limits weaken causal attribution.
They do not weaken the `no-change` decision, which follows from two named guards that
fail on the retained evidence alone.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
