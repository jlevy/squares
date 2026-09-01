# Review: Agenda 013 First-Wave Efficiency

**Date:** 2026-09-01

**Author:** Codex, for the project maintainers

**Status:** Complete BC-122 W5 receipt; decision is `no-change`

This is the mandatory W5 `efficiency-loop` review between agenda-013’s two research
waves. It measures the three first-wave lanes at their retained cutoffs and applies the
predeclared repayment rule.
It neither changes a scientific instrument nor decides any packing claim.

## Verdict

Record **`no-change`**.

The n = 17 exact target path is the dominant measured bottleneck.
Its one authorized run consumed 3,920 seconds, emitted no result or checkpoint, and
accounts for 95.473% of the three receipts’ command-category time.
The likely repeated exact-rational work is large enough to deserve a separate W7 repair,
but it is not admissible as an optimization inside BC-122 or BC-111: there is no
function profile, completed pre-change target output, target-scale equivalence replay,
rollback seam, or demonstrated repayment inside the remaining wall.
The likely BC-116 continuation also reads the same package, so the change is not
disjoint from the second wave.

BC-111 should route the n = 17 lane to BC-116 without calling the timebox a mathematical
disagreement or a premeasurement guard.
Before another target replay, that route needs a newly registered direction-sliced
checkpoint driver around the unchanged scientific kernels.
This is an observability and resumability prerequisite, not a speedup claim.

## Measurement Contract

The common baseline uses the three terminal AgentSessions and their complete task-tree
receipts:

- a **cell** is one recorded workflow phase;
- an **output** is one path in `session.outputs`, with a declared directory counted
  once;
- a **substantive output** excludes the session record and resource receipt;
- a **defect group** is one group named by the coordinator’s retained audit, not an
  inferred count of bugs; and
- **receipt wall** is the source-cutoff span.
  It is not additive agent time and is not the receipt’s `elapsed_envelope_seconds`
  field.

Task-tree deltas have no observed Git-branch field.
Their branch association is the AgentSession’s operator-recorded declaration.
Different lane outcomes make output rates descriptive rather than causal.

## First-Wave Baseline

| Lane | Terminal state / cells | Receipt wall | Agent-active | Outputs / substantive | Recorded defect groups |
| --- | ---: | ---: | ---: | ---: | ---: |
| BC-108, n = 17 | completed / 4 | 7,150.000 s | 6,271.211 s | 6 / 4 | 5 |
| BC-109, n = 68/69 | stopped / 2 | 3,987.000 s | 2,319.926 s | 7 / 5 | 5 |
| BC-110, n = 50 | stopped / 2 | 1,148.000 s | 511.758 s | 3 / 1 | 3 |
| **Total** | **8 cells** | — | **9,102.895 s** | **16 / 10** | **13** |

The totals are 151m42.895s of recursive agent-active time, 6.328 declared output paths
per active hour, and 3.955 substantive paths per active hour.
Those yield figures do not make a small refusal artifact commensurate with a tested
implementation.

The source records are
[session-065](../../../packing/campaign/agent-sessions/session-065-bc108-n17-certificate.md),
[session-066](../../../packing/campaign/agent-sessions/session-066-bc109-n68-n69-precision.md),
[session-067](../../../packing/campaign/agent-sessions/session-067-bc110-n50-exact-control.md),
and their [resource receipts](../../../packing/campaign/resource-usage/).

### Cost decomposition

| Lane | Command | Timed model stream | Recorded first-token wait | Compaction |
| --- | ---: | ---: | ---: | ---: |
| BC-108 | 3,910.842 s | 1,110.189 s | 34.281 s | 79.729 s |
| BC-109 | 181.925 s | 658.678 s | 27.904 s | 107.026 s |
| BC-110 | 3.531 s | 187.615 s | 9.422 s | 51.416 s |
| **Total** | **4,096.298 s** | **1,956.482 s** | **71.607 s** | **238.171 s** |

BC-108’s 3,920-second target timebox is 43.063% of total first-wave agent-active time.
Its receipt independently records 3,910.842 command-seconds.
That command category is 95.473% of the three-lane command total.
The agreement between those two clocks makes the target computation the dominant
measured tool cost, even though it does not locate a function-level hot path.

### Rework and handoff defects

BC-108’s five retained groups are missing source-defect controls, a vacuous optimized-
Python pytest because assertions were stripped, stale 150/130-minute accounting,
historical-versus-current digest ambiguity, and the absence of progress, partial-output,
checkpoint, or resume support.
Its independent readmission and runtime audits add 1,080 seconds of recorded coordinator
effort.

BC-109’s five groups are an unsound heuristic interval enclosure, an incomplete target
runner, omitted precision/tolerance metadata, malformed result/effort wall-time fields,
and a stopped phase initially labelled complete.
Its terminal audit records 360 seconds.

BC-110’s three groups are a missing non-scientific readiness determination, a dependency
mistaken for an instrument guard, and drift in BC-118’s E1--E5 refusal taxonomy.
Its closure audit records 300 seconds.
The coordinator checkpoint separately repaired one invalid combined
engine-commit/source-hash field; it is not safely attributable to one lane.

These defects support earlier readiness and record guards.
They do not yet supply a repeatable fixed-input benchmark or a positive within-wall
repayment case for new shared tooling.

## Dominant Tool Bottleneck

The n = 17 runner finishes the source-faithful manifest before entering the independent
Cartesian path. In the independent path, each direction is reduced to feasible event
cells; every cell constructs a fixture and invokes an accumulator that reprojects and
rescans all 168 atoms.
With 181 directions, 168 atoms and an average of C event cells, the direct work is
Theta(D × A × C). Each axis has at most 2A + 2 events, so the static worst-case envelope
is Theta(D × A^3), roughly 3.45 billion atom-cell examinations.

This is a code-derived complexity bound, not a profile.
The interrupted run retained one localization sample inside the independent accumulator,
no per-direction time, no partial row and no canonical output.
It cannot distinguish projection, exact-fraction membership sums, fixture validation, or
another operation as the true hot function.

The relevant implementation is
[`run.py`](../../../packing/cases/n17_weighted_certificate/run.py),
[`target_independent.py`](../../../packing/cases/n17_weighted_certificate/target_independent.py),
[`independent.py`](../../../packing/cases/n17_weighted_certificate/independent.py), and
[`model.py`](../../../packing/cases/n17_weighted_certificate/model.py).
The censored run is retained in
[exp-049](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-049-h-052-n17-independent-certificate-agreement.md).

## Validation and CI

The successful first-wave local record gate reported 9.55 seconds of wall time.
After a provenance field repair, the local push tier reported 36.97 seconds and 245
selected tests. Focused W5 probes took 0.141 seconds for the n = 17 self-test and 0.388
seconds for the n = 17 and UnitSquare test files together.
Those fast controls do not stand in for the fixed target replay.

The earlier published revision `d7c94590` gives the first hosted baseline: Linux
validate 752 seconds, macOS portability 66 seconds, and the required aggregator 2
seconds. Checkpoint `5572cbf2` then passed Linux validate in 744 seconds, macOS
portability in 65 seconds, and the required aggregator in 3 seconds.
Hosted validation is slow, but it is asynchronous and was not on the remaining W6
critical path. Reworking CI inside this 15-minute slice would have neither a frozen
equivalence benchmark nor a demonstrated second-wave repayment case.

## Change-Admission Test

| Required guard | Evidence | Decision |
| --- | --- | --- |
| Profiled hot path | Static complexity and one interrupt location only | fail |
| Frozen input | exp-049 fixture and package hashes are frozen | pass |
| Completed pre-change replay | The 3,920-second run is right-censored with no output | fail |
| Fixed-target equivalence guard | Small synthetic controls only | fail |
| Rollback seam | The runner hard-codes the adapter and H-052 binds the package manifest | fail |
| Positive remaining-wall repayment | Baseline already exceeded 65 minutes; candidate cost and savings are unmeasured | fail |
| Disjoint from active lanes | BC-116 would reuse the same n = 17 package | fail |

Agenda-013 requires every guard, not a majority.
The only admissible decision is `no-change`. This preserves the frozen exp-049 evidence
boundary and keeps BC-111 on schedule.

## Routed Efficiency Work

The smallest safe future seam is an external direction-sliced execution driver around
the unchanged source-faithful and independent kernels.
For each direction it should:

1. retain a non-scientific start marker;
2. atomically write a paired canonical row after both implementations return;
3. bind the package, fixture, direction, ordinal and previous-row hashes;
4. resume only a contiguous, hash-valid prefix; and
5. assemble all 181 rows into an output byte-identical to the existing canonical record.

Synthetic interrupted, resumed and uninterrupted runs must agree before a new target
round is registered.
This design would make another timebox informative and resumable, but it earns no
speedup or mathematical claim here.

BC-111 should therefore select BC-116, stop BC-112, and amend the launch wording only as
needed to preserve the actual **midmeasurement timebox with no checkpoint**. It must not
relabel that outcome as a discrepancy, cannot-reproduce result, or premeasurement guard.
H-052 remains unresolved and review-pending, with no consequence for n = 18 or n = 19.

## Limitations

- Receipts are aggregate task-tree deltas, not function profiles.
- Cross-lane concurrency is not represented by each receipt’s zero internal parallel
  overlap.
- Session-066’s cutoff includes terminal repair after its scientific stop; session-067’s
  receipt excludes its separate closure audit.
- Artifact paths are heterogeneous, so output rates are descriptive only.
- Completion-emitted token and first-token fields can be assigned wholly to the interval
  containing completion.
- Current hosted durations are end-to-end job durations; they do not isolate setup,
  dependency synchronization or individual validation steps.

These limitations weaken causal attribution, not the no-change decision: the proposed
shared-path optimization fails the predeclared admission rule even under the most
favourable reading of the available timings.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
