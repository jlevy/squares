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
- an agent-session artifact records the overall goal, entry workflow, ordered phase
  history, budget, delegated work, evidence, stopping reason, and exact next action.

## Starting a Session

One session has one integration bead and one active workflow phase.
Before work starts, record:

- the overall session goal, wall budget, and stop conditions;
- `entry_workflow`, chosen from W1–W6 or the explicit `general-improvement` fallback;
- the phase’s workflow, focus, objective, promised evidence, and budget; and
- the next action if the phase succeeds, stops, or blocks.

The first phase uses `entered_by: session_start`, has no `switch_reason`, and must match
`entry_workflow`. Historical v1 sessions were migrated without invented precision:
`budget_minutes` is `null` only where a past phase allocation was never declared.

## Switching Phases

Start a new phase whenever the workflow or focus changes.
A focus-only change repeats the workflow name; it is a phase boundary, not a workflow
switch.
Later phases say whether they began at a planned checkpoint, evidence checkpoint,
or user request, and state the reason.
Close the prior phase first with an outcome, concrete evidence, stop reason, and next
action.

Only the final phase may be `in_progress`, and its status must equal the session status.
The checker enforces those rules.
The generated [ledger](../ledger.md#agent-sessions) shows each phase sequence and counts
both session entry workflows and phases, so a long autonomous session can report what
kinds of work it actually performed.

[Session 009](session-009-autonomous-basin-map.md) is the worked example.
It begins with W4 process review, enters W6 for admissible H-023 experiments, pauses for
a W2 factual review that catches instrument defects, resumes W6 for exp-035, uses W3 to
register the exp-036 obstruction, and returns to W6 for its exact result.
A later W4 phase isolates an unrelated strict-gate failure; the active
`general-improvement` phase now owns that bounded correctness repair without relabeling
it as research.

## Delegation and Control

The parent agent owns shared-file integration.
A delegated task should have a bounded, preferably disjoint write scope and return the
same compact contract represented in the frontmatter: outcome, evidence, files, checks,
uncertainty, next action, and elapsed wall time.

The controller may be a coding agent, a native long-running goal, an external watchdog,
or a human. The repository contract is portable across them: the session records the
objective, budget, slice clocks, stop conditions, evidence, and next action; `tbd` owns
the queue; and commits own integrated state.
A platform goal or watchdog should read and enforce this record rather than become a
second, private source of truth.
These documents are records, not schedulers.
[`runner.py`](../runner.py) remains the executor for preregistered numerical rounds.
The generated `session-report.md` is a numeric-runner batch handoff with a historical
filename; it is not a versioned `session-NNN` agent-session artifact.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
