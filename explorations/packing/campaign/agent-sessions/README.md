# Agent Sessions

These are the durable handoffs for the outer autonomous work loop.
An agent session is one bounded interval of orchestrated work, not a campaign, series,
experiment, or solver run.
The [synopsis](../../SYNOPSIS.md#work-units-and-records) owns those definitions; the
[workflow contracts](../../SYNOPSIS.md#workflow-entry-contracts) own W1–W6.

Session records complement, and do not replace, the scientific record:

- `tbd` owns the work queue and dependencies;
- exploration reports, hypothesis artifacts, and experiment artifacts own mathematical
  ideas and measurements;
- `defects.yaml` owns actual mistakes; and
- an agent-session artifact records the overall goal, ordered phase history, budget,
  delegated work, evidence, stopping reason, and exact next action; its entry workflow
  is derived from the first phase.

## Starting a Session

Each independently tracked session has one integration bead and one active workflow
phase. Several sessions may exist concurrently; each keeps its own phase and clock.
Before work starts, record:

- the overall session goal, wall budget, and stop conditions;
- the first phase’s workflow, chosen from W1–W6, with `general-improvement` reserved for
  genuine repository maintenance outside those workflows;
- the phase’s primary focus, objective, expected output, validation command, kill
  condition, fallback, start, and deadline; and
- the next action if the phase succeeds, stops, or blocks.

Implementation is not a separate implied handoff.
A bounded correction, checker repair, probe, optimization, or research instrument stays
inside W1–W6 according to the durable result it serves.
The phase records actual outcome and evidence only when it closes.

The first phase uses `entered_by: session_start`, has no `switch_reason`, and defines
the derived entry workflow.
Sessions 001–008 predate the workflow vocabulary.
Their v2 rows are retrospective reconstructions from durable evidence, not proof that
the workflow, focus, clock, or transition was declared at the time.
Missing historical phase timing remains unknown rather than receiving invented
precision.

## Switching Phases

Start a new phase whenever the workflow or focus changes.
A focus-only change repeats the workflow name; it is a phase boundary, not a workflow
switch.
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
A delegated task should have a bounded, preferably disjoint write scope and return the
same compact contract represented in the frontmatter: outcome, evidence, files, checks,
uncertainty, next action, and elapsed wall time.
Formatting, lint repair, extraction, and repeated checks inherit the coordinating phase;
a delegate declares another workflow only when it opens its own independently tracked
session.

The controller may be a coding agent, a native long-running goal, an external watchdog,
or a human. The repository contract is portable across them: the session records the
objective, expected output, validation, kill condition, fallback, start, deadline,
terminal evidence, and next action; `tbd` owns the queue; and commits own integrated
state.
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
