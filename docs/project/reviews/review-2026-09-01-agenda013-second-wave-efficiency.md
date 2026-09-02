# Review: Agenda 013 Second-Wave Efficiency

**Date:** 2026-09-01

**Author:** Codex, for the project maintainers

**Status:** Complete BC-119 W5 receipt; decision is `no-change`

This is agenda-013’s mandatory second W5 `efficiency-loop` slice.
It compares the three second-wave lanes with the first-wave BC-122 baseline and records
the agent, tool and process bottlenecks that should shape the next agenda.
It does not run an experiment, repair a frozen artifact or decide a packing claim.

## Verdict

Record **`no-change`** for the remaining agenda-013 wall.

The second wave retained more useful evidence per recorded agent-active hour, but the
tasks, branches and artifact sizes differ, so the comparison is descriptive.
No candidate optimization has a profiled hot path, completed before-and-after target
replay, fixed-input equivalence result, rollback seam and demonstrated repayment inside
the remaining review wall.

Three process corrections are nevertheless strong enough to carry forward:

1. A side-effect-free replay of the **literal preregistered command**, including its
   production adapter and output-path refusal, becomes a W7 admission guard before a W6
   target wall opens.
2. A result manifest binds every executable that can choose its outcome, including the
   producer runner, and uses an injected stage sentinel when refusal ordering matters.
3. A target expected to exceed one 15--30 minute cell must checkpoint first and emit a
   per-unit timing sample before a long target round is registered.

These are future entry conditions, not code changes to the frozen second-wave evidence.

## Measurement Contract

The baseline follows the first-wave review:

- a **cell** is one recorded workflow phase;
- an **output** is one declared `session.outputs` path;
- a **substantive output** excludes the AgentSession and resource receipts; and
- **agent-active**, command, model-stream, first-token and compaction time come from
  complete `CodexTaskTreeDelta/v1` receipts.

Session-070’s independent closure review is a disjoint receipt and is added once to the
n = 50 lane. Receipt intervals are not wall-clock durations and must not be summed into
campaign elapsed time.
Output rates compare unlike work products and therefore cannot establish a causal
improvement.

## Second-Wave Baseline

| Lane | Terminal state / cells | Agent-active | Command | Timed model stream | Outputs / substantive |
| --- | ---: | ---: | ---: | ---: | ---: |
| BC-116, n = 17 | completed / 8 | 6,837.693 s | 2,858.936 s | 1,079.508 s | 8 / 6 |
| BC-117, n = 68 | stopped / 6 | 2,878.896 s | 43.250 s | 1,065.387 s | 6 / 4 |
| BC-118, n = 50, including disjoint review | completed / 7 | 2,311.580 s | 32.103 s | 922.067 s | 13 / 10 |
| **Total** | **21 cells** | **12,028.169 s** | **2,934.289 s** | **3,066.962 s** | **27 / 20** |

The total is 200m28.169s of recorded agent-active time.
It corresponds to 8.081 output paths and 5.986 substantive paths per agent-active hour.
The first wave recorded 151m42.895s, 6.328 output paths and 3.955 substantive paths per
agent-active hour. The second-wave rates are therefore 27.7% and 51.4% higher,
respectively, but the additional tests, drivers and checkpoint files make the
denominator and numerator non-comparable enough that no causal credit is assigned.

The main three lane receipts, excluding the disjoint n = 50 closure review, total
11,602.427 agent-active seconds, 2,926.504 command-seconds, 2,848.592 model-stream
seconds, 136.720 recorded first-token seconds and 240.473 compaction-seconds.
The separate review adds 425.742 active seconds, 7.785 command-seconds, 218.370
model-stream seconds and 12.029 first-token seconds, with no compaction event.
Every receipt reports `snapshot_incomplete: false`.

The source records are
[session-068](../../../packing/campaign/agent-sessions/session-068-bc116-n17-resumability.md),
[session-069](../../../packing/campaign/agent-sessions/session-069-bc117-n68-refusal-localization.md),
[session-070](../../../packing/campaign/agent-sessions/session-070-bc118-n50-source-semantics.md),
and their [resource receipts](../../../packing/campaign/resource-usage/).

## Lane Findings

### n = 17: durable progress, unchanged scientific speed

The sole exp-052 process ran for 4,456 seconds and retained 33 contiguous paired rows.
That is 135.030 seconds per completed row, or 0.444 rows per minute.
A straight-line projection is 6.789 hours for all 181 rows and 5.551 hours for the
remaining 148. The projection assumes later directions cost like the first 33 and is not
a completion estimate.

The external checkpoint driver changed the value of a censored run: exp-049 retained no
canonical row after 3,920 target seconds, while exp-052 retained a validated restart at
ordinal 33. It did not demonstrate faster exact accumulation.
The n = 17 lane accounts for 97.4% of second-wave command time.
Its receipt also records 1,639.457 seconds of agent-wait time, consistent with the long
target process rather than a coordination gate.

The next registered n = 17 round should resume rather than replay and should record
per-direction timings or a function profile before a speed change is proposed.
A parallel design can be explored in W3, but it needs a deterministic merge and
identical row-hash boundary before receiving causal credit.

### n = 68: late discovery of command unreachability

The lane completed its proof, independent verifier, injected runner, 38-test suite and
normal/optimized self-tests.
It then invoked the exact registered `--record` command and exited 2 in argument parsing
because the CLI exposed no production adapter.
No network, parent, child or target access occurred.

Only 43.250 receipt seconds were command time; 1,065.387 were model-stream time.
The dominant loss was therefore not slow computation.
It was guard latency: three W7 cells developed an instrument whose literal production
entry point was still unreachable.
A parser/adapter reachability check against the absent result path should be present
from the first executable skeleton and repeated at every W7 boundary.

This rule does not imply that the exact proof residue was wasted.
The residue is useful for a newly registered adapter round.
It means the lane was not ready to buy target time.

### n = 50: effective review, incomplete provenance binding

The lane retained a reason-3 `attribution-unbound` E1 result with zero cells, an exact
19-square control covering all 171 pairs and two rejecting mutations.
The separate closure review took 425.742 agent-active seconds and found the material
caveat: the immutable result and independent verifier bind four inputs but omit the
`source_semantics_runner.py` hash.
Current source checks the existing-result refusal before evaluation, but the durable
record cannot prove that ordering after an unbound runner mutation.

That short review had high leverage because it challenged the evidence boundary rather
than repeating the producer’s happy path.
Future result manifests must enumerate the whole decision-producing executable closure
before W6. Where ordering is itself a claim, an injected stage sentinel should prove
that the forbidden stage was never reached.

## Agent Behavior and Coordination

The three agents stayed within disjoint ownership and returned positive, negative and
blocked outcomes without substituting easier targets.
That prevented target contamination and made the protected checkpoint possible.
The receipts do not support a comparison between the n = 17 lane’s `max` reasoning
setting and the two `xhigh` lanes: the tasks, runtimes and artifact loads differ.

The most important behavior correction is to test the external contract earlier.
The n = 68 agent verified internal proof and runner properties before verifying that the
registered command could reach the runner.
By contrast, the independent n = 50 review looked directly for an omitted trust-boundary
input and found one quickly.
Future W7 review prompts should lead with the literal command, result-path behavior and
provenance closure before internal implementation detail.

Checkpointing eliminated the n = 17 lane’s zero-retention failure mode.
Regular 15--25-minute cell records also made every lane’s last trustworthy state
visible. They did not reduce the exact accumulator’s measured cost, and the records
should not claim that they did.

## Validation, CI and Artifact Lifecycle

The second-wave checkpoint passed the local push tier: 33 of 58 named steps, 301
reachable tests, all 151 document anchors, Ruff, BasedPyright, schemas, exact
verification, campaign-record checks and the tbd tree.
Checkpoint `529b6729` passed hosted Linux validation in 747 seconds, macOS portability
in 64 seconds and the required aggregator in 4 seconds.
Linux remains inside the earlier 744--752 second band.
Hosted CI is slow, but it neither regressed nor blocked lane execution or the W5 slice,
so no CI optimization is admitted here.

Two executed source files had to be narrowly excluded from Ruff formatting because the
immutable exp-050 and exp-052 records bind their exact bytes.
Both still lint and type-check, and their hashes were rechecked before and after
repository formatting.
This is a lifecycle warning: formatter and static-check normalization should precede the
hash freeze. An evidence-bound file that must remain byte-identical needs an explicit,
measured exclusion rather than a late rewrite.

## Change-Admission Test

| Required guard | Evidence | Decision |
| --- | --- | --- |
| Profiled hot path | Per-lane aggregates and n = 17 row rate only | fail |
| Frozen input | All three experiment inputs and retained outcomes are frozen | pass |
| Completed pre-change target replay | n = 17 is censored; n = 68 never reached target; n = 50 is a refusal | fail |
| Fixed-target equivalence replay | Synthetic controls, not an optimization replay | fail |
| Rollback seam | No proposed code change or versioned substitute exists | fail |
| Positive remaining-wall repayment | Remaining time is reserved for review and synthesis | fail |
| Disjoint from frozen review artifacts | Any runner or manifest repair changes evidence under review | fail |

Agenda-013 requires every guard.
The decision is `no-change`.

## Routed Bottlenecks

BC-119 should encode, but not implement, these requirements in the frozen packets:

- n = 17 review verifies checkpoint-chain integrity, absent canonical result and the
  distinction between resumability evidence and H-052 evidence;
- n = 68 review executes the literal command first, then a proof mutation, and treats
  the CLI refusal as the terminal result rather than repairing it; and
- n = 50 review verifies the immutable result and no-overwrite behavior, then treats the
  missing producer hash as a bounded provenance caveat rather than inferring that the
  recorded run evaluated geometry.

The next agenda should register separate work for n = 17 profiling/parallel merge
design, n = 68 production-adapter admission, and n = 50 manifest/sentinel repair.
None should mutate exp-050, exp-051 or exp-052 in place.

## Limitations

- Task-tree receipts are aggregate intervals, not function profiles.
- Output counts treat heterogeneous files equally.
- First- and second-wave tasks differ, so throughput deltas are descriptive.
- The n = 17 linear projection ignores direction-dependent event-cell counts.
- Completion-emitted token and first-token fields can be assigned wholly to the interval
  containing completion.
- Hosted CI is end-to-end checkpoint evidence and is not attributed to a lane.

These limits prevent an optimization claim.
They do not weaken the observed admission, provenance and lifecycle failures, each of
which is preserved by a direct artifact or literal command result.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
