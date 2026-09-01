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

**The rate is measured and nobody reads it.** `ClaudeEfficiencyRollup/v1` has always
counted `one_off_code`, and session-047 is the first to look: 954 of 3416 tool calls,
27.9%, three hours of wall time, 718 of them Python heredocs — in the session that wrote
this paragraph. That number is not a gate and should not become one.
The rule forbids *leaving* a measurement in one-off code, not exploring with it, and a
threshold on heredocs would fail the exploration this repository depends on while
catching none of the actual defect, which is a retained number whose tool does not
exist. It is here because a rule with a number attached is harder to feel exempt from
than one without, and because the rollup can answer this question for any session that
asks.

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

**That exact error recurred twice more**, in two independent sub-agents run at maximum
effort on unrelated tasks during
[session-045](packing/campaign/agent-sessions/session-045-agenda008-queue-and-identity.md).
One called it “a hard `SyntaxError` under Python 3.14”, the other “a `SyntaxError` on
every Python 3” across ten named files.
All ten parse. Three for three is not bad luck: `except A, B:` reads as a Python 2 tell
strongly enough to survive being checked, so verify a parse claim by parsing rather than
by reading. The same reports were otherwise excellent, which is the point — a report can
be right about five real defects and confidently wrong about a sixth.

## OR-3: Never wait on a gate with nothing else in flight

Launch it in the background and keep the next slice moving.
Never poll it, and never start one against a tree you are about to change: a gate whose
inputs move underneath it has to be run again, so it spends the eight minutes and buys
nothing.

**Run `packing-validate --records` before a push, and push before the slower checks
finish** so CI runs concurrently with them rather than after them.
The record checks take about four seconds and are the ones that break
([D-369](defects.md)); the behavioural tests take eight minutes and have never broken
here. Serialising local tests and CI pays the longer of the two costs twice.

Four seconds rather than the seventy this rule first recorded, since `BC-077` swapped
the schema validator and moved exact geometry out of the step named for schemas
([D-370](defects.md)). That changes how the rule reads: at seventy seconds running the
record checks was a judgement call, and at four there is no argument for skipping them.

**Use `--edit` while editing.** `BC-079` split it out of `--fast`, which had stopped
being fast at `499s` with one step 94% of it.
`--edit` is 33 seconds and runs everything except that step.
`--fast` is what a block boundary is for, and CI runs the full gate on every push
regardless, so the split moves feedback latency and not coverage.

**The waste this rule names is measured now, and it is the coordinator’s, not the
gate’s.** The evidence is the retained rollup
[`5cd11e53`](packing/campaign/resource-usage/5cd11e53-fb82-4a28-ab2a-0c26f16fe7e5.yaml),
quoted from its own fields: `345.1s` across **four** `.gate-running` polling calls, plus
`245.6s` across three that waited on a test run, against `3187.6s` of wall — **18.5%**
of the session spent watching a gate that was going to finish either way.
Twice the gate was started against a tree that then changed underneath it, and both runs
had to be discarded.

The first version of this paragraph said `233.6s` across three calls and “about 17%”,
read off the transcript rather than the rollup ([D-379](defects.md)). Understating the
waste in the rule that exists to stop it is the wrong direction to be wrong in, and the
rollup is one field lookup away.

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

## OR-8: A self-declared budget is not a stop condition

Under an open-ended mandate — “don’t stop”, “run through the night”, “until it is done”
— only three things end a run: the user says so, an external blocker makes progress
impossible, or the work is genuinely exhausted.
Reaching the end of a plan is none of these.
A plan is an estimate the run wrote for itself, and the end of an estimate means it is
time to plan the next slice, not time to stop.

Two devices keep this from being a matter of memory, because memory is what failed.

**The continuity trigger does not depend on being re-armed.** `send_later` is one-shot,
so a chain of re-arms is only as long as the first turn that decides the work is
finished. A recurring trigger fires on its own schedule regardless of what the previous
turn concluded, so a wrong “we are done” is corrected at the next firing rather than
being final. Keep the one-shot chain for fine-grained pings if it helps; the recurring
one is the floor under it.

**Deleting that trigger requires the user to ask.** It is the only irreversible action
in the loop — every other bad call gets another turn to be reconsidered, and this one
does not. Treat it the way any other irreversible action is treated here.

[D-395](defects.md) is a run that had eleven and three-quarter hours of unbroken
20-minute pings, wrote itself a reminder saying “the wall budget is spent … do not start
new work”, and then deleted it.
The clocks were right; the authority was wrong.
[D-358](defects.md) is the same stop, reached by a misread clock instead — which is why
the rule is about what may end a run, not about how to measure time.

## OR-9: A pull request leads with what the branch cost

The reviewer can see what changed.
Nothing on the page said what it took, though harness telemetry existed: Claude records
branch-aware per-log rollups, and Codex can now retain a privacy-reduced additive
task-tree interval declared by an AgentSession.
It was simply never put where the merge decision is made.

So the description of an end-to-end session’s pull request opens with that block, and it
is generated rather than written:

```shell
uv run --frozen --all-extras --group dev python -m devtools.render_pr_rollup
```

For Codex, pass `--session session-NNN`. Codex exposes no Git-branch field, so the
AgentSession declares the interval’s association with the PR and the renderer labels it
operator-recorded rather than harness-observed.
Never render a Codex receipt without that explicit declaration.

**Close the session first.** The block is a function of the rollups, so it is wrong
until they are written — which is why `close_session --render` prints it as its last act
rather than leaving it to a second command.
Close, then paste, then open.

**Never collapse it to one number.** In a Claude record, `turns.by_branch` is the only
branch-aware field, so a log that ran on more than one branch has an exact turn count
and no way to split its tokens or tool calls.
The block prints three columns — on-branch logs only, prorated by turn share, and every
log that touched the branch — of which the outer two are measurements and the middle is
the estimate to quote.
On the branch that introduced this rule the straddling logs carried 5,486 of 8,423
turns, so the interval is not a rounding matter and a single figure would be a guess
wearing a measurement’s clothes.
Codex intervals render in a separate section: their model responses are not Claude
turns, and adding the two harnesses could count the same work twice.
A live Codex snapshot is explicitly a lower bound.

**A multi-block session keeps the pull request current, not just open.** The owner
reviews as the work lands, so a session that runs more than one block opens the pull
request at its first completed block — with a mid-session rollup snapshot standing in
for the terminal one — and refreshes the description and cost block at each block
boundary rather than saving both for the end.
Added 2026-08-31 at the owner’s request, during the session that opened
[PR #64](https://github.com/jlevy/squares/pull/64) this way.

This is `OR-1` applied to the reviewer rather than to the researcher: a measurement that
exists and is not reported is the same waste as one taken and thrown away.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
