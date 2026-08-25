# Agent Sessions

These are escalation artifacts for the outer autonomous work loop.
An agent session is one bounded interval of orchestrated work, not a campaign, series,
experiment, or solver run.
The [synopsis](../../SYNOPSIS.md#work-units-and-records) owns those definitions; the
[workflow contracts](../../SYNOPSIS.md#workflow-entry-contracts) own W1–W7.

Session records complement, and do not replace, the scientific record:

- `tbd` owns the work queue and dependencies;
- exploration reports, hypothesis artifacts, and experiment artifacts own mathematical
  ideas and measurements;
- `defects.yaml` owns actual mistakes; and
- an agent-session artifact records the overall goal, ordered phase history, budget,
  delegated work, evidence, stopping reason, and exact next action; its entry workflow
  is derived from the first phase.

Do not open a session record for a routine single-purpose edit, a short review, or one
registered round whose hypothesis, experiment, result, and bead already provide the
needed state.
In those cases, declare the workflow, bounded objective, intended artifact,
and focused check in the place already tracking the work.

## Starting a Session

Open a versioned session when at least one of these conditions holds:

- the work will cross multiple workflow or material-focus phases;
- it will run autonomously beyond an ordinary checkpoint;
- it coordinates delegates that need independently recoverable state;
- it supervises an expensive experiment or proof search; or
- interruption would otherwise lose a consequential decision or exact next action.

Each such session has one integration bead and one active workflow phase.
Several may exist concurrently; each keeps its own phase and clock.
Before escalated work starts, record:

- the overall session goal, offset-aware start and hard deadline, wall budget, cycle
  cap, finalization reserve, and stop conditions;
- the first phase’s workflow, chosen from W1–W7, with `general-improvement` reserved for
  genuine repository maintenance outside those workflows;
- the phase’s primary focus, objective, clock role, expected output, validation command,
  kill condition, fallback, start, and deadline; and
- the next action if the phase succeeds, stops, or blocks.

In a clocked session, ordinary `work` phases must end before the finalization reserve.
The final phase may instead declare `clock_role: finalization` and use that reserve for
records, checks, commits, and handoff.
An active session leaves `progress.after` null; the checker requires the completed value
when the session closes.

Implementation is not a separate implied handoff.
A bounded correction, checker repair, probe, optimization, or one-round research
instrument stays inside W1–W6 according to the durable result it serves.
W7 owns reusable packing-pipeline capabilities, targeted refactors, robustness,
visualization infrastructure, and cleanup for named research consumers.
The phase records actual outcome and evidence only when it closes.

The first phase uses `entered_by: session_start`, has no `switch_reason`, and defines
the derived entry workflow.
Sessions 001–008 predate the workflow vocabulary.
Their v2 rows are retrospective reconstructions from durable evidence, not proof that
the workflow, focus, clock, or transition was declared at the time.
Missing historical phase timing remains unknown rather than receiving invented
precision.

## Switching Phases

Start a new phase whenever the workflow, focus, or bounded slice objective changes.
A focus-only change repeats the workflow name; it is a phase boundary, not a workflow
switch. A renewed slice may repeat workflow and focus only after the prior phase closes,
and its changed objective and switch reason must state what new evidence earns another
clock. Momentary changes of emphasis do not create phases.
Focus is the primary quality emphasis; the other three operating principles still
constrain and may contribute to the phase.
Later phases say whether they began at a planned checkpoint, evidence checkpoint, or
user request, and state the reason.
Close the prior phase first with an outcome, concrete evidence, stop reason, and next
action.

Only the final phase may be `in_progress`, and its status must equal the session status.
The checker enforces those rules.
The generated [ledger](../ledger.md#agent-sessions) shows each session’s derived entry,
current phase, phase count, and recording provenance.
Its workflow summary separates contemporaneous declarations from retrospective
reconstructions; the linked source artifact retains the complete ordered history.
Historical reconstructed rows must be identified as reconstructions rather than counted
as contemporaneous declarations.

[Session 009](session-009-autonomous-basin-map.md) is the worked example.
It begins with W4 process review, enters W6 for admissible H-023 experiments, pauses for
a W2 factual review that catches instrument defects, resumes W6 for exp-035, uses W3 to
register the exp-036 obstruction, and returns to W6 for its exact result.
A later W4 phase isolates an unrelated strict-gate failure; a bounded W2 correctness
phase audits and implements D-199 without relabeling that repair as research.

## Delegation and Control

The parent agent owns shared-file integration.
A delegated task should have a bounded, preferably disjoint write scope.
A delegation that may cross a checkpoint or run a long or side-effecting command gets a
durable queued or active row before it runs.
That row records `recording: contemporaneous`, phase, wall budget, expected output,
validation command, kill condition, fallback, write scope, excluded long commands,
start, and deadline.
A short read-only or mechanical task that begins and returns inside one parent slice may
inherit the prompt’s scope and clock without a queued row; record its compact terminal
receipt when it returns.
Every terminal receipt retains recording provenance, owning phase, outcome, evidence,
files, checks, uncertainty, next action, and elapsed wall time.
The command itself becomes evidence only after its owning parent collects a terminal
receipt keyed by the command or session identifier.
Retain exact argv and any replay-relevant working directory or environment, offset-aware
start and end times, elapsed wall time, exit code or terminating signal, stdout and
stderr inline or at durable paths, the declared timeout result, and process cleanup or
reaping. These fields bind after success, failure, timeout, yielding, or delegation;
process disappearance is not a receipt.
Queued and active rows leave terminal outcome, evidence, uncertainty, and elapsed
quality null rather than inventing placeholders; the checker requires them when the row
closes. Use frozen dependency commands; a read-only assignment does not authorize a
lockfile or other tracked side effect.
Until the outer validation timeout and durable-receipt blockers close, the coordinator
retains every long command and delegates explicitly exclude strict or deep gates.
Formatting, lint repair, extraction, and repeated checks inherit the coordinating phase;
a delegate declares another workflow only when it opens its own independently tracked
session.

The controller may be a coding agent, a native long-running goal, an external watchdog,
or a human.
When escalation applies, the repository contract is portable across them: the
session records the objective, expected output, validation, kill condition, fallback,
start, deadline, terminal evidence, and next action; `tbd` owns the queue; and commits
own integrated state.
A platform goal or watchdog should read and enforce this record rather than become a
second, private source of truth.
These documents are records, not schedulers, and
[`packing-campaign`](../../src/sqpack/campaign/runner.py) remains the executor for
preregistered numerical rounds.
The generated `session-report.md` is a numeric-runner batch handoff with a historical
filename; it is not a versioned `session-NNN` agent-session artifact.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
