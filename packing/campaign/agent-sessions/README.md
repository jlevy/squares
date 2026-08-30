# Agent Sessions

These are escalation artifacts for the outer autonomous work loop.
An agent session is one bounded interval of orchestrated work, not a campaign, series,
experiment, or solver run.
The [synopsis](../../../SYNOPSIS.md#work-units-and-records) owns those definitions; the
[workflow contracts](../../../SYNOPSIS.md#workflow-entry-contracts) own W1–W8.

Session records complement, and do not replace, the scientific record:

- `tbd` owns the work queue and dependencies;
- exploration reports, hypothesis artifacts, and experiment artifacts own mathematical
  ideas and measurements;
- `defects.yaml` owns actual mistakes; and
- an agent-session artifact records the overall goal, ordered phase history, budget,
  delegated work, evidence, stopping reason, and exact next action; its entry workflow
  is derived from the first phase.

After all source sessions for one user-level run become terminal, the
[research loop logbook](../research-loop-logbook/README.md) joins their checked counts,
scientific results, relevant defect ids, pipeline changes, validation, and next action
into one ground-up synopsis.
The source sessions remain authoritative for phase detail.

Do not open a session record for a routine single-purpose edit, a short review, or one
registered round whose hypothesis, experiment, result, and bead already provide the
needed state.
In those cases, declare the workflow, bounded objective, intended artifact,
and focused check in the place already tracking the work.

## Starting a Session

Read [`operating-rules.md`](../../../operating-rules.md) first: OR-4 decides what the
session picks up, OR-5 what workflow it declares.

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
- the first phase’s workflow, chosen from W1–W8, with `general-improvement` reserved for
  genuine repository maintenance outside those workflows;
- the phase’s primary focus, objective, clock role, expected output, validation command,
  kill condition, fallback, start, and deadline; and
- the next action if the phase succeeds, stops, or blocks.

In a clocked session, ordinary `work` phases must end before the finalization reserve.
The final phase may instead declare `clock_role: finalization` and use that reserve for
records, checks, commits, and handoff.
An active session leaves `progress.after` null; the checker requires the completed value
when the session closes.

### Starting a Portable Four-Hour Session

A four-hour session uses repository state as its complete control plane.
A native goal, scheduled wakeup, or chat history may resume the work, but the session
must remain runnable without any of them.

Before opening the first phase, read the synopsis’s
[current handoff](../../../SYNOPSIS.md#current-handoff), the active campaign agenda, the
owning hypothesis, and its bead.
From the repository root, establish the baseline:

```shell
tbd prime
uv run --directory packing --frozen packing-ledger check
uv run --directory packing --frozen --all-extras --group dev \
  packing-validate --fast --jobs 2 --inner-jobs 1
uv run --directory packing --frozen packing-campaign status
```

Create the next sequential `session-NNN` artifact before target work starts.
Record one absolute 240-minute deadline, at most eight 30-minute wall-clock cycle slots,
ten minutes for orientation, a twenty-minute evidence checkpoint, up to thirty minutes
per work phase, and at least fifteen minutes of protected finalization.
No work, validation, publication/CI, or terminal-reconciliation slot may exceed 30
minutes. If the finalization reserve is longer, split it into bounded slots inside the
final workflow phase.
The cap is an inventory point, not a quota.
Close a short phase as soon as its bounded output is complete, and grant another slice
only after re-screening measured progress and remaining value.
Cycle slots account for wall time; workflow phases account for material changes of
purpose or focus.
An early evidence-triggered phase switch does not create more wall time
or consume an extra cycle slot.
Record the current slot and phase together in the session body whenever their numbers
differ. The last phase is `clock_role: finalization`; it reconciles artifacts, generated
views, defects, beads, commits, and the next action rather than opening new research.

Before target work, write a bounded slot plan through finalization.
Each proposed slot names its objective, dependency or parallel lane, expected evidence,
representative command cost, and defer or kill rule.
Only the active slice is frozen; later slices are maximum allocations that must be
revised from measured elapsed time at each boundary.
Apply the same boundary review to validation and finalization slots even when a shared
purpose lets them remain inside one workflow phase.

For each work phase:

1. Declare the workflow, focus, bounded objective, expected artifact, exact validation
   command, kill condition, fallback, start, and deadline.
2. Give read-only or disjoint implementation work to available sub-agents or delegates
   under the same clock.
   One coordinator owns shared records, experiment IDs, mathematical judgment, and
   integration.
3. Preserve a checkable result by minute twenty and stop or renew at minute thirty.
   At the boundary, compare measured coordinator, command, and delegation time with the
   remaining slots, finalization start, and session deadline.
   A renewal needs new retained evidence and a new phase contract.
4. Update the owning scientific or engineering artifact, render and check generated
   views, and record every negative, invalid, blocked, or partial result.

On resume, compare the current offset-aware time with the active phase deadline,
finalization start, and session deadline before writing:

| Clock state | Required action |
| --- | --- |
| Before the active phase deadline | Continue only its frozen objective and guards. |
| At or after the active phase deadline, before finalization | Terminalize that phase from retained evidence before opening a successor; never extend its lease or criterion retroactively. |
| At or after finalization start, before the session deadline | Open or continue only a `finalization` phase; do not start new research. |
| At or after the session deadline | Terminalize the session from existing evidence, validate, commit, push, sync the bead, and leave an exact next action; do not perform more target work. |

Each session’s fresh-agent section records its live branch and durable checkpoint.
A portable checkpoint runs the session’s exact focused validation and then, from the
repository root, uses this sequence:

```shell
uvx --from flowmark-rs==0.3.2 flowmark --auto <edited-markdown-files>
uv run --directory packing --frozen --all-extras --group dev \
  packing-validate --only "soft-schema"
uv run --directory packing --frozen packing-ledger render
uv run --directory packing --frozen packing-ledger check
uv run --directory packing --frozen python -m devtools.check_synopsis
git diff --check
git status --short --branch
git add <explicit-reviewed-files>
git commit -m "<conventional-commit-message>"
git push
tbd update <owning-bead> --notes "<checkpoint evidence and exact next action>"
tbd sync
```

Do not use `git add -A` in a shared checkout.

## Closing a Session

The checkpoint sequence above is per-phase.
Bringing a whole session to a terminal state adds one step, and it is not optional:

```shell
# From packing/. One record per log: the outer agent's, and every sub-agent it spawned.
uv run --frozen python -m devtools.log_rollup <session-log>.jsonl --out campaign/resource-usage
uv run --frozen python -m devtools.log_rollup <sub-agent-log>.jsonl --out campaign/resource-usage
```

Then list what those wrote in the session record’s `resource_rollups`,
repository-relative.

**Why this is a required field and a gate step rather than a line in a checklist.**
Session-045 ran twenty-three phases without the rollup being written once, and nothing
noticed: no field was empty, no check failed, and the session closed clean.
The omission was invisible because there was no link at all between a session and its
usage — rollups are named by harness log id, sessions by their own sequence number, and
nothing joined the two.
`OR-1` says the answer to a recurring measurement gap is a tool rather than a better
memory, so `devtools.check_session_rollups` refuses a terminal session that declares
none and the gate step `terminal sessions name what they cost` runs it in `--records`.

Three things worth knowing when you do it:

- **The rollup is regenerated, not appended.** A record is a function of the log it
  names, so re-running the command on a session that has since grown replaces the
  record. Run it at the end, not part-way through, or run it again if you do.

- **Sub-agent transcripts are where the delegated cost lives**, and they are separate
  logs. Session-045’s sixteen of them carry work that does not appear in the outer log at
  all. Attribute them by comparing each rollup’s `span` against the session’s window
  rather than by memory; the outer log may span more than one session, in which case
  each names it.

- **Sessions numbered below `session-045` predate the field** and the checker lists them
  as grandfathered rather than skipping them silently.

- **The reverse direction is reported, not refused.** `check_session_rollups` asks
  whether every declared rollup exists; `close_session` also asks whether every rollup
  on disk is declared by some session.
  Ten currently are not, and all ten are legitimate — their spans fall in sessions that
  closed before the field existed.
  That is why it prints them with their dates rather than failing: an unattributed cost
  is worth seeing and is not by itself a defect.

- **`close_session --render` is what closing a session produces**, and it writes two
  views of one join: [`session-close-report.yaml`](../session-close-report.yaml), one
  validated entry per session, and the generated block under `## Sessions Conducted` in
  [`SYNOPSIS.md`](../../../SYNOPSIS.md).
  `--check` refuses either having drifted and runs in `--records`; `--update`
  regenerates rollups from logs and is the whole of backfill, since a retained log
  turning up needs a run rather than a code change.

- **Never total by adding sessions.** Sessions share harness logs — four declare the
  current one in full, which is correct of each of them — so adding their figures counts
  a shared log once per claimant.
  Measured on 2026-08-30: 117.9 hours for a campaign that had spent 43.7. Every total in
  the report is over *distinct* rollups, and the shared log is shown on its own row so
  the per-session column still adds up.
  The tool infers no owner for an unclaimed rollup, which is a different question from
  the span comparison above: use spans to decide what *your* session declares, and let
  the unclaimed ones stay counted separately rather than assigned to whichever window
  happens to contain them.

  The coordinator substitutes the phase’s recorded validation command for
  `<focused-validation>` before the sequence and inspects every staged path before
  committing. A session checkpoint is durable only when its commit is on the recorded
  remote branch and the session’s next action identifies any remaining work.

Do not infer that the generic numerical runner is admissible because
`packing-campaign preflight` passes.
The synopsis and launch agenda own the scientific go/no-go decision.
When they say **NO-GO**, run supervised exact or source-bound slices only; never fill
the clock with an executable recipe whose validity, budget, or evidence contract remains
blocked.

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

### What May End a Run

The rollup above is what a session does when it legitimately ends.
This is when that is.

Under an open-ended mandate — “don’t stop”, “through the night”, “until it’s done” —
three things end a run: the user says so, an external blocker makes progress impossible,
or the agenda is exhausted.
A plan running out is not one of them.
The plan is an estimate the run wrote for itself, and its end is a cue to plan the next
slice.
`OR-8` in [`operating-rules.md`](../../../operating-rules.md) is the rule; this is
the mechanism it needs.

**Take the hourly floor even though an hour is too coarse.** The recurring-trigger
interval is floored at one hour, and the run that produced `D-395` read that refusal as
*cron is unusable here* and fell back to a chain of one-shots alone.
It says one hour is the *floor*, which is what a floor is for: arm the hourly recurring
trigger and layer the finer ping on top of it.
Declining the coarse device because it is coarse leaves nothing underneath the fine one.

**Arm a recurring trigger, not a chain of one-shots.** `send_later` fires once, so a
chain of them is exactly as long as the first turn that concludes the work is finished —
and that turn has no successor to reconsider it.
A recurring trigger fires on its own schedule regardless of what the last turn decided.
Keep the one-shot as the fine-grained ping if it helps; the recurring one is the floor
under it, and it is the floor precisely because no single judgement can remove it.

**Deleting the recurring trigger needs the user to ask for it.** Every other bad call in
the loop gets another firing to be corrected.
This one does not, which puts it with the irreversible actions rather than the routine
ones.

[`D-395`](../../../defects.md) is what this costs when it is left to memory: a run with
eleven and three-quarter hours of unbroken twenty-minute pings, every one re-armed by
hand, that then wrote itself a note reading “the wall budget is spent … do not start new
work” and deleted it.
The clocks were accurate — that was [`D-358`](../../../defects.md)’s failure, not this
one. What went wrong is that a budget the run invented was allowed to outrank an
instruction the user gave in words, and “budget spent” went into the record looking like
a constraint that had been met.

### Cycle Time Is Reported, Not Tolerated

Efficiency is one of the four operating principles, and its goal is iteration *as fast
as possible*. A phase that verifies a change by running materially more than that change
can reach has violated it, and the violation is a reportable finding rather than a cost
of doing business.

Each phase already declares a `validation_command`. Two obligations come with it:

- **Choose it against the change, not from habit.** `packing-validate` states the ladder
  in its own help — `--fast` while editing, `--only TEXT` for one named surface, the
  default before a commit, `--strict` before an unattended session or a merge.
  The full gate belongs at block boundaries and before commits, not after every edit.
- **Record the measured cost, and report an overrun.** When a phase spends materially
  longer verifying than the affected surface requires, that is logged like any other
  defect, with the two numbers side by side.
  [D-355](../../../defects.md) is the worked example: `979.79s` spent against `12.06s`
  of affected steps, an 82x overrun, found only because a session measured its own cycle
  time instead of accepting it.

The tension between coverage and cycle time is real, and resolving it is the design’s
job rather than the operator’s discretion.
The standing asymmetry decides the direction: efficiency may simplify process but never
weaken the assurance a claim requires, so a narrower command is admissible only when the
steps it drops provably cannot fail on this change.
Running less than that is a coverage gap; running more than that, by reflex, is the
defect above.

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
