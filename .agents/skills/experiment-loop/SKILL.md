---
name: experiment-loop
description: >-
  Run a hypothesis-driven research or optimization campaign with a durable
  soft-schema experiment record: a registry of falsifiable hypotheses, an
  iteration loop measured against a control or a standing best, verdicts under
  a pre-declared accept rule, and a ledger/report generated from the record.
  Supports unattended overnight runs and several agents working one registry in
  parallel. Use whenever the user wants to make something measurably better or
  explore a solution space systematically — performance or load-time tuning,
  comparing algorithms or strategies, optimal-packing or proof-search campaigns,
  prompt or retrieval quality loops — and whenever they mention an experiment
  ledger, research log, hypothesis registry, benchmark campaign, recording
  negative results, pre-registration, sweeping a parameter, or resuming,
  paralleling, or merging experimental work. Also use when asked to set up "the
  experiment loop", "the performance loop", or an iterative-improvement
  methodology for any subject.
---
# The Experiment Loop

A method for making a system measurably better — or searching a solution space — without
fooling yourself, and for leaving a record that outlives the sessions that produced it.

It was distilled from two independent implementations by the same author: **fdu**’s
performance loop (64 committed experiment artifacts, paired statistics, generated
reports with a drift gate) and **metabrowser**’s exploration loop (the same method
rebuilt at 1/12th the weight for a full-stack web app).
Everything both kept is the core; everywhere they differ is a knob.
Your job is not to reproduce either implementation.
It is to build the *lightest* loop that answers your problem’s question, on top of the
invariants below.

## When to use this

Use it when work is a **campaign**: several competing hypotheses or strategies, each
needing a fair test, where “did anyone try this and what happened?”
must stay answerable months later — by a different person, agent, or model.

Skip it for a one-off question you can answer and forget.
And keep it out of CI: an exploration answers a question once; a benchmark defends an
answer forever; only the second belongs in a release gate.

## Reading protocol

This file is the map.
Load a reference when its action arrives, not before.

| Reference | Load it when |
| --- | --- |
| `references/contract.md` | setting up a campaign, adding a result shape, or writing any artifact |
| `references/statistics.md` | writing the accept rule, or judging a result |
| `references/unattended.md` | running rounds without a human watching, or with more than one agent |
| `references/traps.md` | at setup (skim), and whenever a result surprises you |
| `references/worked-examples.md` | choosing which of four domain templates is nearest |

Copyable starting points live in `assets/`: the four schemas, the idea-board template,
and a starter ledger generator that also runs the whole-set invariant checks.
Copy them into the campaign directory and cut them down; do not import them.

## Session startup and time slices

Before multi-hour work starts, write a bounded plan through the next coherent
integration checkpoint.
Unless the user declares another cadence, target that checkpoint within about four hours
and divide the path into slices no longer than 30 minutes, including validation and
finalization.

Identify independent read-only or disjoint-write work that available sub-agents can run
in parallel. One coordinator owns shared records, integration, scientific judgment,
commits, and external updates.
When the queue and runtime capacity permit, keep three to five sub-agents on concrete,
bounded work rather than serializing independent source, implementation, and audit
lanes. Do not manufacture duplicate or speculative tasks just to fill a slot.

Treat long CI as asynchronous evidence, not as a work phase.
After dispatch, record the run and continue with independent local work; check CI only
at a declared integration or finalization boundary, and never spend an iteration slice
polling an unchanged run.

At each slice boundary, compare measured command, coordinator, and delegated elapsed
time with the original estimates and the remaining critical path.
Shorten, split, reorder, or defer only future slices; never move a declared deadline or
alter a frozen hypothesis, criterion, regime, or scientific budget after seeing results.

## What a finished campaign leaves behind

Four things, all checked into the repo:

1. **The idea trail** — the idea board, which is the whole idea space on one page, and
   the exploration reports behind it, kept whole.
   Codifying an idea into a registry entry compresses it; the report is where the
   discarded reasoning survives, and the board is what makes it findable.
2. **A full research log** — one artifact per experiment (including every failure), the
   hypothesis registry, and the raw run data (or a pointer to where it lives, when too
   large to commit).
3. **The backing work** — the code each experiment built, referenced by commit and entry
   point from the artifact that measured it.
4. **A final report** — the ledger and any charts, generated from the artifacts, never
   edited by hand.

Because all of it is in git and the schema is validated, the campaign can be revisited
at any time: continue the loop, point a different agent or model at the same hypotheses
to see if it does better, or run branches in parallel and merge the records.

## The invariant core

Both implementations converged on these independently.
Keep them in every domain:

1. **One soft-schema artifact per experiment.** YAML frontmatter carries what a tool
   reads; the Markdown body carries the reasoning no schema can hold.
   Promote a value into YAML only when something consumes it.
2. **Record every experiment, failures most of all.** Negative results are the most
   reusable output of a campaign — they stop the next agent re-running a dead end.
   In fdu’s record, 28 of 64 artifacts are rejections, and that is why its queue is
   trustworthy.
3. **Name the criterion before measuring.** The hypothesis states which metric or
   determination will show it, and in which direction.
   Measuring, missing, and finding another metric that passes is never an accept.
4. **A number without its spread is not a result.** Median with range at minimum;
   confidence interval when claiming.
   Overlapping ranges mean “no detectable effect”, never “a small win”.
5. **The verdict is arithmetic plus exactly one judgment.** The accept rule’s clauses
   are computed; whether the change is worth its complexity is written down as the
   judgment it is.
6. **Views are generated, never edited.** The ledger and report rebuild from validated
   artifacts, so the record cannot be edited into a better story.
7. **Record the regime with the number.** Platform, cache state, scan state, load —
   whatever decides what the result is evidence *about*. Never extrapolate across
   regimes.
8. **Ids are stable and never reused.** Experiments (`exp-NNN`), hypotheses (`H-NNN`)
   and exploration reports (`X-NNN`) each number independently and monotonically, so no
   id ever means two things.
9. **Provenance is captured at the source, never retyped.** Commit, dirty flag, binary
   hash, command line, environment — filled by the recording step, not by whoever
   remembers.
10. **An independent check that the result is real, before it may be good.** Identical
    output before timing; a validity oracle; a solution checker; a proof kernel.
    A run failing it is *invalid*, not merely rejected — refuse it at record time.
11. **The record is corrected, not rewritten.** A defective artifact gets an annotation
    explaining what stands and what does not.
12. **The instrument must prove it was measuring something.** Six metabrowser runs were
    taken in a 0×0 browser pane and produced plausible timings measured against nothing.
    Guard the instrument, and refuse runs the guard rejects.
13. **A check that did not run is not a check that passed.** Gates degrade to skips — a
    missing optional dependency, an absent toolchain, an unreachable store — and a
    summary line that says everything passed while its strongest check was skipped is
    worse than no gate, because it is trusted.
    Count the skips, name them in the summary, print the unqualified pass only at zero,
    and give the gate a strict mode that unattended runs use.

## Three roles, and why they are separate

A campaign that scales past one session separates idea generation from codification from
execution. The same agent may wear all three hats in a small campaign, but the
*artifacts* stay distinct, because each role’s failure mode is different.

| Role | Produces | Optimizes for | Must not |
| --- | --- | --- | --- |
| **Explorer** | `explorations/X-NNN-*.md` — free-form reports proposing ideas | breadth, novelty, reading widely | narrow itself to what is easy to measure |
| **Codifier** | `ideas.md` rows and `hypotheses/H-NNN-*.md` — the board and the registry | falsifiability, one claim each | invent claims the report did not make |
| **Runner** | `experiments/exp-NNN-*.md` — one per round | fidelity to the runbook | change the accept rule, or skip a negative result |

The explorer is *deliberately unconstrained*: its report is prose, may propose twenty
ideas of wildly varying quality, and is judged on how much the codifier can mine from
it. Constraining it to schema-shaped output at the point of generation is the main way
campaigns go stale — you get the ideas that were easy to formalize, not the good ones.

The codifier is the schema boundary.
It reads reports and emits one registry artifact per falsifiable claim, each citing the
report and paragraph it came from (`derived_from`). One report legitimately yields many
hypotheses, or none.
An idea that cannot be stated so it could be wrong is recorded in the registry as
`kind: open_question` rather than being forced into a criterion it does not have.

The runner never reopens either.
If a round wants a criterion the registry does not carry, the runner registers a new
hypothesis first and says so — see `references/unattended.md` for what an unwatched
runner may and may not decide.

## The idea board

One page, `ideas.md`, carrying the **whole idea space** — every idea anyone has had
about the campaign, one line each, whether or not it has been formalized, tried, or
killed. It is the first thing an arriving agent reads, and usually the only thing it
needs before picking up work.

It exists because the two artifact stores either side of it are the wrong shape for
orientation. The exploration reports are deep and many: reading them all to learn what
has been considered costs more context than the work does.
The registry is strict and narrow: it holds only what survived formalization, so an idea
that was thought of and not yet shaped is invisible there — and gets proposed again.
The board is the wide, shallow middle, and it is the piece that makes a campaign cheap
to join.

A row is one line, with a status (`raw`, `shaped`, `registered`, `parked`, `dead`), a
link to the exploration report behind it, and the crux in a clause.
Once a row reaches `registered` it names its `H-NNN` and stops carrying outcome — the
ledger owns that from then on, which is what stops the board becoming a second, drifting
record. Dead ideas are moved to a section, never deleted; an idea deleted for tidiness
gets reproposed within the month.

**The board is the one hand-written link in the chain, and the only one.** It is an
input, not a view, because grouping ideas and saying why they matter is judgment.
What is mechanical is its *referential integrity*, and that is checked both ways: every
`H-NNN` the board names must exist in the registry, and every registered hypothesis must
appear on the board.
Start from `assets/ideas-template.md`.

## Setting up a campaign

Read `references/contract.md` first — it has the artifact contract, the result shapes,
and the design choices below spelled out.
Then:

1. **Write the campaign question.** One sentence, falsifiable, in the runbook.
   “Which search strategies reach the standing best for this instance within a four-hour
   budget, and what do the ones that fail find instead?”
   is a campaign question.
   “Improve packing” is not.
2. **Declare the subject and the instance axis.** The subject is what decides what a
   result *means* (host and cache regime; corpus and viewport; problem instance and its
   constraints). Separate out the **instance axis** — the dimension you may hold fixed
   now and sweep later (`n`, corpus size, model, dataset).
   Every result records its point on that axis, so a later sweep merges into the same
   record instead of starting a new one.
3. **Declare the metric vector — multidimensional, fixed, with roles.** A small set of
   metrics recorded on *every* experiment, each with a role: `outcome` (the accept rule
   scores it), `cost` (qualifies the win), `guard` (independent limit; a breach rejects
   regardless of outcome), `mechanism` (explains, never decides).
   Fixing the set is what prevents metric-shopping; multiple benchmarks per run are
   normal — record them all, and let the roles say which may conclude what.
4. **Choose comparison shape(s)**: `paired` (control vs candidate), `conditions`
   (labeled arms, median + range), `record` (score against a standing best),
   `determination` (categorical pass/fail or proved/refuted).
   A campaign may use more than one — a packing round typically carries a `record` score
   *and* a `determination` on whether it beat the record.
5. **Choose the evidence tier** (`exploratory` or `confirmatory`) and write the accept
   rule down — see `references/statistics.md`. Do this before the first measurement.
6. **Write the runbook** (`README.md` in the campaign directory): the campaign question,
   the loop steps for this subject, how to produce one valid run, the accept rule, and
   the budget and stop conditions.
   Test it against the **resume rule**: everything needed to pick the loop up mid-stream
   lives in three places — the registry (what to try next and why), the record and its
   views (what has been tried), and the runbook (how to run one round).
   Nothing needed is only in someone’s head.
7. **Seed the idea board and the registry** — commission one or more exploration
   reports, land their ideas on `ideas.md`, codify the ones that can be stated so they
   could be wrong, and only then start measuring.
   A hypothesis whose instrument does not exist yet is `blocked`, not measured badly.
   Status is *generated* from the experiments that reference it.
8. **Run a baseline round first** (`decision: baseline`) so later experiments have
   numbers to be measured against.
   Where the subject has a *known* answer at some point of the instance axis, make that
   the baseline: a searcher that cannot recover a solved case has not earned an opinion
   about an open one.

A layout that has worked (adapt freely):

```
<campaign>/
  README.md                    # the runbook: question, loop, accept rule, budget
  ideas.md                     # the idea board: the whole idea space on one page
  schemas/                     # the contracts, copied from assets/ and cut down
  explorations/X-001-....md    # the idea trail, free-form
  hypotheses/H-001-....md      # the registry, one artifact per claim
  series/001-smoke-.../
    README.md                  # the series artifact: goal, instrument, why it exists
    experiments/exp-001-....md # the record, one artifact per round
    results/                   # raw runs (jsonl or per-run files)
  ledger.md                    # generated view — never hand-edited
```

## Series: running the loop more than once

A campaign that lives long enough will want to run its loop again — with a rewritten
engine, a different solver, a better instrument — and the old numbers will not be
comparable to the new ones.
A **series** is one full pass of the loop under one generation of tooling.

The split that makes this work:

| Spans the campaign | Belongs to a series |
| --- | --- |
| the idea board | the experiments |
| the hypothesis registry (`H-NNN`) | the raw run data |
| the schemas and the checker | the series’ own ledger view |

Hypotheses span series because a claim about the world does not become a different claim
when the engine improves — and because the most valuable question a long campaign can
answer is *what did series 001 and series 003 each conclude about H-007?* Experiments
belong to a series because their numbers were taken on one instrument, and invariant 7
says never to extrapolate across regimes.
A series is that invariant applied at campaign scale.

**Experiment ids stay globally monotonic across the whole campaign.** The series is a
directory and a field, not a namespace: `exp-042` means one round, forever, wherever it
lives. Numbering per series would make `exp-001` mean several things and break invariant
8 on the first merge.

```
<campaign>/
  ideas.md, hypotheses/, schemas/, ledger.py     # span every series
  series/
    001-smoke-<slice>/
      README.md            # the series artifact: goal, instrument, why it exists
      experiments/         # exp-001 .. exp-037
      results/
    002-<next>/
      README.md            # supersedes: series-001, carries_forward: [exp-012]
      experiments/         # exp-038 ..
```

The field that earns a series its existence is `opened_because`: what changed since the
last one. If nothing changed, the work belongs in the series already open.
The natural first series is a **smoke pass** — the obvious hypotheses, the reproductions
of known results, the cheap sweeps — run precisely to prove the loop itself works end to
end before anything subtle is attempted.
Its `carries_forward` is empty, and that is correct.

A later series may declare `carries_forward: [exp-012]` for rounds whose conclusions
survive the tooling change.
Listing one is a claim that its numbers still hold; leaving it out costs a re-run and is
the safer default. Start from `assets/series.schema.yaml`.

## Running one round

```
1. PICK      the top open hypothesis from the registry, and claim it.
2. PREDICT   restate its criterion, direction, regime, and instance. If you are
             about to measure something it did not predict, register that first.
3. BASELINE  measure the control (or confirm the standing best) under the runbook.
4. CHANGE    the smallest diff that tests the one hypothesis. Reference the code
             by commit and entry point.
5. MEASURE   the candidate the same way. Pair and interleave if the harness can;
             same corpus, same regime, same instance, recorded either way.
6. DECIDE    apply the accept rule mechanically; write the one judgment sentence.
7. RECORD    one artifact, validated, whatever the verdict. Lift every number
             from the run data — never retype. Then regenerate the views.
8. RE-SCREEN the queue: the change you landed may have eaten the next
             hypothesis's headroom, and two hypotheses can compete for one cost.
```

For search campaigns (packing, proofs, strategy portfolios), steps 4–5 become “spend the
declared budget exploring the approach”, and the verdict may be `abandoned`: budget
spent, best result reached, and what would justify reopening — distinct from `rejected`,
because the claim was not refuted; the search ran out of promise.

## Sweeps

A **sweep** runs one hypothesis across several points of the instance axis, or one
instance across several hypotheses.
Both are ordinary rounds; the sweep is a *view*, not a new artifact type.
That is the whole reason the instance is a declared field rather than prose.

- Fix the hypothesis, vary the instance: does the effect hold across `n`, or was it a
  property of the one case you tuned on?
- Fix the instance, vary the hypothesis: which strategy wins *here*, which is the
  portfolio question.
- Fix both, vary the operator: does a different agent or model do better on the same
  claim? This is a replication, not a conflict — see `references/unattended.md`.

Declare the sweep’s points in the hypothesis (`sweep.axis`, `sweep.points`) so the
ledger can show which cells are filled and which are still open.
An unfilled cell is a queue item; a hypothesis “confirmed” on one cell of a declared
sweep is confirmed on that cell only, and the ledger should say so.

## Record both halves, and check both in

The frontmatter carries the structured half: every metric of the fixed vector with its
spread, the comparison against control or standing best, complexity, verdict.
The body is a **full research report** of the qualitative half: what the profile or
prior evidence suggested, what was actually built and how (commands, resources,
references, the code that ran — by commit, path, and entry point), what surprised you,
and **what the prediction got wrong** — “right about the component, wrong about the
wall” is a reusable lesson; “missed” is not.

Commit the artifacts, the registry, the exploration reports, the raw runs, the
regenerated views, and the backing code together.
A number nobody can trace is a number nobody can defend.

## Adapt the weight to the problem

| Knob | Light (metabrowser-scale) | Heavy (fdu-scale) | Choose by |
| --- | --- | --- | --- |
| Statistics | median + range overlap, n≥3 | paired bootstrap CI, n≥12 | evidence tier of the claim |
| Interleaving | sequential conditions | per-trial interleave | whether the harness is automated |
| Schema | hand-written YAML | compiled from a typed model | field count and churn |
| Drift gate | none | views re-derived in the check gate | record size and audience |
| Measurement | operator-carried paste, provenance auto-filled | fully automated harness | dependency policy |
| Coordination | one agent, one session | leases, budgets, morning report | whether rounds run unwatched |

Start light. Move a knob rightward when a claim needs defending, not before.

**Before building unattended operation, check that it buys anything.** Divide the effort
fields you have already recorded: agent-minutes against machine-minutes.
One campaign’s first ten rounds came to 275 agent-minutes against 16.4 cpu-minutes —
seventeen to one — and a runner removes only the second number.
An agent-bound loop gains close to nothing from a night of unattended execution and can
lose a week building it.
Where the ratio runs the other way, unattended operation is the whole game.
This is a measurement you already have; make it before writing the runner, not after.

## Tooling

The artifact format is **softschema** (validation, self-describing envelope, schema
compilation). Prefer a project-installed command; pin the zero-install fallback rather
than floating it, because an unpinned runner re-resolves on every invocation:

```bash
softschema validate <doc.md>                    # if installed
uvx softschema==0.6.2 validate <doc.md>         # pinned fallback
uvx softschema==0.6.2 docs spec                 # the exact artifact format
uvx softschema==0.6.2 skill --brief             # operating brief
```

Real implementations to crib from:

- **fdu** ([github.com/jlevy/fdu](https://github.com/jlevy/fdu)) — the heavy end:
  [the performance loop](https://github.com/jlevy/fdu/blob/main/docs/project/guides/performance-loop.md)
  (protocol and hypothesis registry),
  [the instrumentation playbook](https://github.com/jlevy/fdu/blob/main/docs/project/guides/performance-instrumentation-playbook.md)
  (the domain-neutral method — worth reading in full before any measurement campaign),
  [`experiment.py`](https://github.com/jlevy/fdu/blob/main/benchmarks/realtree/experiment.py)
  (typed contract), `docs/project/experiments/` (64 artifacts;
  [exp-051](https://github.com/jlevy/fdu/blob/main/docs/project/experiments/exp-051-memoize-the-parent-resolved-for-the-previous-upsert.md)
  is the gold standard), and
  [the generated ledger](https://github.com/jlevy/fdu/blob/main/docs/project/reports/report-2026-08-10-fdu-performance-experiments.md),
  which leads with its failures.
- **metabrowser** ([github.com/jlevy/metabrowser](https://github.com/jlevy/metabrowser))
  — the light end: `explorations/README.md` (runbook), `explorations/run.py` (772-line
  harness), `explorations/experiments/exp-003-*.md` (a full round in ~150 lines of
  file).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
