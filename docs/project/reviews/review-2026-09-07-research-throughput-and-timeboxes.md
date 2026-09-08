# Research Throughput and Time-Box Review

The coordinator preserved Session097’s scientific limits but allowed successive
operational follow-ups to displace the next experiment.
The research direction still matches the selected agenda.
Execution has delivered fewer mathematical decisions than the investment warrants.

This is a W4 process review under `think-muns`, requested after PR116’s checkpoint.
The bounded diagnostic pass began at 00:22:27 UTC on September 8 and must stop by
00:37:27 UTC. Its output is this review and two follow-up beads, not a new scheduler,
experimental allocation, or change to existing acceptance rules.
The preceding cost audit is included below.

## What the Investment Bought

The eight nonoverlapping retained Codex intervals for Sessions088, 089, 090, 091, 093,
094, 095 and 097 contain 48.88 aggregate agent-hours and 18.63 hours during which at
least one agent was active.
They report 3,704,727 output tokens, including 1,463,273 reasoning-output tokens;
reasoning is not an additional chargeable count here.
Input totals are 38,221,360 uncached tokens and 773,885,952 cached tokens.
These are usage figures, not an invoice or a dollar estimate.

The retained timings include 21.21 aggregate hours of model streaming, 3.27 hours of
context compaction across 94 events, and 9.10 hours of command-tool time.
These timing categories are not established as a mutually exclusive partition.
About 93% of recorded model-stream time used max or xhigh reasoning.
The receipts do not identify how many of those tokens bought mathematics versus
bookkeeping, so an exact waste percentage would be invented.

The [session cost table](../../../SYNOPSIS.md#sessions-conducted) links the intervals.
The totals above sum their `rollup.delta` fields, never their cumulative `before` or
`after` snapshots. All eight receipts are live lower bounds with completion-attributed
tokens. They exclude gaps, other task trees, and later work; they are not campaign
totals. The [receipt semantics](../../../packing/campaign/resource-usage/README.md)
explain the distinction.

Session097 alone records 5.92 aggregate agent-hours and 416,285 output tokens through
23:38:23 UTC, across a 2.69-hour interval.
Its useful mathematical result is the exact cubic center-feature obstruction.
The independently implemented proposer and exact reader passed 75 source-free controls,
but those controls provide no evidence about H125’s target.
The target never ran.
See its
[cost receipt](../../../packing/campaign/resource-usage/codex-task-tree-session-097.yaml)
and
[session record](../../../packing/campaign/agent-sessions/session-097-kernel-contract-and-feature-pricing.md).

Earlier work established an exact optimum of eleven on one fixed support and a density
calibrated on that support.
These are useful exclusions and controls, not improvements to the global packing bound.
Further investment must buy a new mathematical distinction, not another representation
of those results.

## What the Logs Show

The review inspected timestamp-selected visible messages, tool calls and tool outputs
from this task’s native log, restricted to September 7, 21:45–23:40 UTC. It did not
inspect other conversations or retain private reasoning or raw transcripts.
The durable counterparts are Session097’s operational receipts and
[exp129](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-129-h125-finite-kernel-obstruction.md).
Times below are UTC on September 7.

| Time | Observed event | Consequence |
| --- | --- | --- |
| 22:04:22 | Protocol patch fixes launch by 22:20 and science completion by 22:27 | Limits existed before the attempted admission |
| 22:18:07 | Tool output rejects a mutation anchor expecting “There are 84 rounds”; the synopsis correctly contains 85 | Documentation consistency prevents admission |
| 22:29:34 | Disposition records non-invocation and zero scientific execution | The expired scientific allowance was not extended |
| 22:47:49 | Formatting-hook repair is allocated | Operational work continues around the stopped research |
| 22:55:04 | A closing check reports 550.25 seconds and handoff/certification failures | Another repair and validation cycle follows |
| 23:12:22 | Another push check reports 177.01 seconds | The certification declaration remains a blocker |
| 23:14:22 | Full check reports 3,616.36 seconds and four failed steps | Its failures require separate evidence; they do not prove a kernel defect |
| 23:23:03 | Bead update declares a new 23:21:36–23:51:36 operational allocation | A fresh local limit does not bound cumulative recovery cost |
| 23:38:43 | Cost receipt is refreshed to include post-freeze repairs | Accounting retains the expense, but only after the agenda has lost that time |

The gate durations overlap and must not be added as elapsed delay.
The log does not support blaming all failures on host contention or calling every repair
unnecessary. In particular, borrowing an old documentation-only pass to certify later
scientific code would have been wrong; the independent reviewer correctly rejected it.

## Why Time Boxing Did Not Protect Throughput

**Local limits worked.** Exp129 declares one producer and one conditional reader, each
with a 60-second TERM deadline and two-second KILL grace.
Neither child ran because the launch prerequisite failed.
Research-phase and session deadlines also remained fixed.
Those are important protections against an unbounded search or an invented result.

**The coordinator did not bound cumulative recovery.** Formatting, generated views,
publication, certification and diagnostic work received additional allocations after the
research session stopped.
The inspected log contains no common recovery-time or token allowance across that
sequence. Relabeling work as operational preserves its scientific meaning, but does not
make its cost disappear.

**Readiness depended on too much surrounding state.** A stale documentation test stopped
a numerical attempt whose two child envelopes total at most 124 seconds, plus
supervision overhead.
The original guard had to be obeyed once frozen.
Its placement still deserves prospective review: documentation correctness, scientific
validity and merge assurance are related requirements with different consequences.

**Checks detect some clock errors without scheduling useful work.** A validator refusing
an expired active phase is an audit, not a runtime supervisor that selects the next
mathematical task. Passing that audit cannot establish that the agenda received enough
attention. A local phase cap also cannot limit the sum of separately allocated repairs.
The [clock checker](../../../packing/devtools/check_session_clocks.py) explicitly
reports elapsed-versus-budget rather than refusing it.
The stronger [ledger check](../../../packing/src/sqpack/campaign/ledger.py) rejects an
expired active phase against
[HEAD’s committer date](../../../packing/src/sqpack/campaign/commit_clock.py), so its
verdict is reproducible.
Neither mechanism interrupts live agent work.

The policy also permits continuation: OR-6 bounds individual slices and OR-8 directs an
open-ended run to plan its next slice when an estimate expires.
That supports persistence, but leaves the coordinator responsible for making further
maintenance compete with research.
The existing `certification_pending` correction now allows an honest stopped checkpoint;
rebuilding that escape would duplicate work.

**The schedule counted many intermediate completions.** Design, admission,
implementation, code review, protocol review and disposition each produced an artifact.
Independent proof and instrument checks had value, but their completion was not a
substitute for the target result.
More occupied agent slots would not by itself have fixed this.

## Smallest Proposed Corrections

These are recommendations for the next allocation, not retroactive changes to exp129.

1. **Budget the complete research decision.** Put preparation, author and reviewer work,
   active validation handling, repair and publication under one owner-level allowance.
   Report aggregate agent time separately from active elapsed time; exclude genuine
   interruptions, not active maintenance.
   Declare a small recovery allowance inside it.
   When recovery consumes that allowance, preserve the blocker and redirect to eligible
   independent work. Any additional repair allocation must state what research it
   displaces and why it is worth doing.
   This is a decision boundary within an open-ended mandate, not permission to abandon
   the mandate. `think-ycuo` owns this correction.
2. **Separate launch prerequisites from publication prerequisites.** Map every check to
   the claim it protects before changing its placement.
   Preserve fixed inputs and criteria, known-answer controls, sound instruments,
   independent exact acceptance, and final merge coverage.
   Full validation is already allowed to run asynchronously; do not invent a
   full-before-every-target requirement.
   Review whether unrelated documentation drift should block future exploratory
   execution or only promotion and publication.
   `think-6l2l` owns that review; no check is waived here.
3. **Judge a checkpoint by its decision.** Record what was proved, refuted, or left
   unresolved by an actual attempt, and how that changes the next choice.
   Keep readiness and repair outcomes visible but separate.
   A missed launch calls for reprioritization, not automatic renewal of the same chain
   of preparation tasks.
4. **Spend parallel reasoning on distinct questions.** Use max for mathematical judgment
   and independent proof review; high or xhigh for mechanical work.
   Give delegates compact evidence packets and bounded outputs.
   Reuse unchanged reviews and controls; reopen them when their assumptions or source
   change. Avoid repeated broad handoff reviews and extra management layers without
   independent work for them to coordinate.

These changes can use the existing bead, experiment, agenda and cost records.
No additional identifier family, clock schema or token dashboard is justified by this
review. Any accepted checker implementation belongs in the existing
[validation-efficiency plan](../specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md).

## Next Mathematical Decision

One first H125 invocation remains the cheapest prepared discriminator, subject to its
specific fresh admission requirements.
Its marginal cost, not the sunk implementation cost, earns that priority.
An exact obstruction retires only the certified family.
An inconclusive outer LP does not earn a continuum verifier, a larger feature family, or
an automatic retry.

H101 is a conditional alternative, not an automatic second funded lane.
The record has no exact candidate square avoiding the common occupied region and no
completed certificate for that candidate.
A short candidate search may earn further work; an implementation project cannot
substitute for the missing candidate.
The
[Agenda027 handoff](../../../packing/campaign/agendas/agenda-027-compatibility-and-restricted-families.md#session095-selection-and-parallel-handoff)
retains the other directions and external BC261/273 ownership.

The next checkpoint should contain one such mathematical decision or a concise blocker
and a selected independent next action, together with the total effort it consumed.
It should not require another pipeline review to discover that no target ran.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
