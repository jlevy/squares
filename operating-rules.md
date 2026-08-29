# Operating Rules

**How work is done here.** `conventions.md` governs the *shape of what is produced*:
ids, artifacts, schemas, evidential status.
This page governs the *conduct of the work itself*, which is what to pick up, how to
spend a session, and which mistakes cost this project the most wall clock.

Read it before starting a slice, not after.
Every rule below was written because it was broken, and each one cites what it cost.

[`AGENTS.md`](AGENTS.md) carries a one-line summary of each rule, generated from the
headings below by `devtools.render_operating_rules`. Add a rule here, then run it;
`packing-validate` fails on drift.

## The rules

### OR-1: Build the tool; never leave a measurement in one-off code

An inline `python -c`, a heredoc, or a throwaway script is a signal that a tool is
missing, not evidence that one is unnecessary.
Write it into `devtools/` with the guard that makes its answer refusable, run it, and
check it in. When the tool is large enough to need a design, open a
[W7 pipeline-improvement](README.md#workflow-entry-points) session with a spec of what
has to be built, rather than improvising it inside a research slice.

The cost is not tidiness, it is wrong numbers.
[D-023](defects.md) records the first experiment session, whose negative controls were
heredocs; one restored its mutation with `git checkout` and silently discarded an
uncommitted backfill, invalidating two probes.
[session-043](packing/campaign/agent-sessions/session-043-block9-degree-bound.md)
repeated it: a throwaway script reported a Bézout bound of `12,690,480`, because
substituting only `sin(a)` and `cos(a)` leaves `cos(b − i)` standing as an opaque
generator. The number had already been said out loud before the tool existed.
The productionised tool’s rational-coefficient guard is what caught it, and the
corrected bound is `1,039,500`.

### OR-2: Run three to five sub-agents, at a thinking level matched to the task

Independent read-only investigation and disjoint writes parallelise; shared records,
integration, commits, and external updates stay with the coordinator.
Below three, the coordinator is usually doing serially what it could have handed out.
Above five, reconciliation costs more than the parallelism buys.

Choose the thinking level by difficulty rather than by habit: **high** for survey and
retrieval, **extra** for anything carrying a proof obligation, **max** for the hardest
mathematics and the hardest review findings.

A sub-agent’s report is evidence, not a verdict.
Verify anything surprising before acting on it.
In [session-044](packing/campaign/agent-sessions/session-044-agenda006-continuation.md)
a sub-agent reported that `contacts.py` does not parse, which reproduced under Python
3.11 and is simply wrong under the project’s Python 3.14, where
[PEP 758](https://peps.python.org/pep-0758/) makes `except A, B:` valid.

### OR-3: Never wait on a gate with nothing else in flight

Wall clock is the scarce resource in a timed session, and the fast gate takes about
eight minutes of it.
Start validation in the background, keep the next slice moving, and read the result when
it lands. Blocking on it converts a check into eight idle minutes of a four-hour budget,
repeatedly.

This rule is about the coordinator’s conduct; whether the gate itself should be that
long is a separate question, measured and retiered under `BC-075`. Both halves are
needed, because a faster gate that is still waited on synchronously wastes less time but
wastes it the same way.

### OR-4: Take the next slice from the handoff, not from the backlog

The entry point is the synopsis’s [current handoff](SYNOPSIS.md#current-handoff): it
names the active agenda, the exact next bounded slice, and the owning bead.
The active agenda’s session queue owns priority ordering.

`tbd ready` includes the historical backlog.
It is an input to a coordinator checkpoint, not the queue itself: do not pick work from
it directly while a handoff and an agenda exist.

### OR-5: Declare the workflow entry point before beginning

Independently tracked packing work chooses W1–W8 from
[`README.md`](README.md#workflow-entry-points) before a session or a genuine workflow
phase begins, with `general-improvement` reserved for repository maintenance outside
those workflows. Bounded delegated work (formatting, lint repair, extraction, a repeated
check) inherits the parent phase unless it opens its own tracked session.
Longer sessions record workflow and primary-focus changes as ordered phases;
[`SYNOPSIS.md`](SYNOPSIS.md#workflow-entry-contracts) owns the full contracts.

### OR-6: Plan multi-hour work in slices before starting it

Follow the
[bounded research cycle](packing/campaign/README.md#the-bounded-research-cycle) and the
[portable session guide](packing/campaign/agent-sessions/README.md#starting-a-portable-four-hour-session).
Unless the user sets another cadence, target a coherent integration checkpoint within
about four hours and cap each slice at 30 minutes.

Thirty minutes is a ceiling and a review point, not a quota: close a smaller process,
review, efficiency, or implementation slice as soon as its bounded output is complete.
At every boundary, compare measured command, coordinator, and sub-agent time against the
remaining plan, and replan only future slices.

## Why this is a separate page

These are the rules an agent needs *before* its first tool call, and they kept ending up
in places that are read too late: a defect entry is read during a review, the session
guide is read once a session is already open, and `conventions.md` is long and consulted
on demand.

`AGENTS.md` is the only file guaranteed to be in context before anything happens, which
makes it the right place for the summary and the wrong place for the reasoning.
So the reasoning lives here, the summary lives there, and a check keeps them the same.
Adding a rule means adding it here first.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
