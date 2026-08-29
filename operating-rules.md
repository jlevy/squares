# Operating Rules

**How the work is done here**, as against `conventions.md`, which governs the shape of
what is produced. Each rule below is here because it was broken and cost something; the
citation is the argument.
[`AGENTS.md`](AGENTS.md) carries a generated one-line summary, since it is the only file
guaranteed to be in context before the first tool call.
Add a rule here, then run `devtools.render_operating_rules`.

## OR-1: Build the tool; never leave a measurement in one-off code

A `python -c`, a heredoc, or a throwaway script means the tool is missing.
Write it into `devtools/` with the guard that makes its answer refusable; if it needs a
design, open a [W7 pipeline-improvement](README.md#workflow-entry-points) session rather
than improvising inside a research slice.

The cost is wrong numbers, not untidiness.
A heredoc control in [D-023](defects.md) restored its mutation with `git checkout`,
discarding an uncommitted backfill and invalidating two probes.
A script in
[session-043](packing/campaign/agent-sessions/session-043-block9-degree-bound.md)
reported a Bézout bound of `12,690,480` where the answer is `1,039,500`, and it was said
out loud before the guarded tool that refused it existed.

Three shapes keep recurring, kept here as instances so a W7 session can generalise the
tool from them:

- **Anchored prose replacement:** swapping a multi-paragraph section of `AGENTS.md` for
  another, by `str.index` slicing inside a heredoc.
  An editor tool with a uniqueness guarantee does this directly.
- **Anchored insertion into a structured record:** putting `BC-076` before
  `- id: BC-075` in the agenda, and three control definitions before a named anchor in
  `controls.yaml`. `run_negative_controls` already has the guard this wants, since an
  anchor matching other than exactly once is a refusal rather than a mutation.
- **Coordinated edit under one invariant:** `operating-rules` had to reach the
  document-map schema enum, the map, and `ROLE_LABELS` together or the renderer raises,
  and `count:` in `defects.yaml` has to move with three aggregates in `SYNOPSIS.md`.
  Both were multi-file heredocs whose only check was a later gate step.

## OR-2: Run three to five sub-agents, at a thinking level matched to the task

Read-only investigation and disjoint writes parallelise; shared records, integration,
commits, and external updates stay with the coordinator.
Below three is usually serial work that could have been handed out; above five,
reconciliation costs more than it buys.

Pick the thinking level by difficulty: **extra** for anything carrying a proof
obligation, **max** for the hardest mathematics and review findings.

A sub-agent’s report is evidence, not a verdict.
One in
[session-044](packing/campaign/agent-sessions/session-044-agenda006-continuation.md)
reported that `contacts.py` does not parse; it parses under the project’s Python 3.14,
where [PEP 758](https://peps.python.org/pep-0758/) makes `except A, B:` valid.

## OR-3: Never wait on a gate with nothing else in flight

Launch it in the background and keep the next slice moving.
Never poll it, and never start one against a tree you are about to change: a gate whose
inputs move underneath it has to be run again, so it spends the eight minutes and buys
nothing.

Whether the gate should be that long is `BC-075`, not this rule.

## OR-4: Take the next slice from the handoff, not from the backlog

The [current handoff](SYNOPSIS.md#current-handoff) names the active agenda, the next
bounded slice, and the owning bead, and that agenda’s queue owns priority ordering.
`tbd ready` mixes in the historical backlog, so it informs a coordinator checkpoint but
is never the queue.

## OR-5: Declare the workflow entry point before beginning

Independently tracked work picks W1–W8 from
[`README.md`](README.md#workflow-entry-points) before the session or phase starts, with
`general-improvement` reserved for maintenance outside those workflows.
Bounded delegated work inherits the parent phase unless it opens its own tracked
session. [`SYNOPSIS.md`](SYNOPSIS.md#workflow-entry-contracts) owns the full contracts.

## OR-6: Plan multi-hour work in slices before starting it

Unless the user sets another cadence, target an integration checkpoint within about four
hours and cap each slice at 30 minutes, per the
[bounded research cycle](packing/campaign/README.md#the-bounded-research-cycle).
Thirty minutes is a ceiling, not a quota: close a slice as soon as its bounded output is
complete. Replan at each boundary from measured time, and only forward.

## OR-7: Run the documentation guidelines pass at block boundaries

A block that produced a new document, a substantial rewrite, or a long block comment
closes with a `pprose-common-edit` pass; `tbd guidelines common-doc-guidelines` is the
text it applies. The commit hook already handles formatting, so this is the structure,
footer, and de-slop pass, which is the one that never happens on its own.

Once per block, not per file: per file it re-reads the same guidelines for every edit
and churns text that was already conformant, and a block that only touched records or
code has nothing for it to do.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
