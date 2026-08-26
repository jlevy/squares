# Research Loop Logbook

This logbook gives a new reader one ground-up synopsis for each escalated, bounded
user-level research run that has one or more durable agent-session records.
An entry may summarize several sessions when a recovery session continues the same
user-level clock and objective.
Routine single-round work that never opens an agent session remains fully recorded by
its experiment and does not require a logbook entry.

The logbook is a checked index, not a replacement for its sources:

- agent-session artifacts own the ordered phase history, clocks, delegations, and
  recovery state;
- experiment artifacts own scientific criteria, measurements, and verdicts;
- `defects.yaml` owns bugs, inefficiencies, and record defects in the toolchain; and
- a logbook entry joins those sources into a reader-facing account of what was
  attempted, achieved, stopped, changed, validated, and left next.

Rejected approaches and unresolved hypotheses are research results, not defects.
List them under Results or What Did Not Work.
Add an item to the defect log only when the toolchain, record, or process itself was
wrong, and cross-reference its `D-NNN` id here.

## Record Topology

Each durable fact has one owner.
Other records link to that owner instead of copying its mutable state.

| Question | Owning record | What summaries may repeat |
| --- | --- | --- |
| What might be worth trying? | `ideas.md`, `H-NNN`, and launch agendas | The selected question and why it was selected |
| What did one scientific round decide? | `exp-NNN` and its retained result | Its id, checked verdict, narrow result, and claim limit |
| What happened over time? | `session-NNN` | Checked phase and delegation counts plus a compressed history |
| What did one bounded user-level run accomplish? | `run-NNN` in this logbook | A ground-up synthesis linked to all of the records above |
| What was wrong with the machinery or record? | `defects.yaml`; `defects.md` is generated | New and relevant defect ids plus their effect on the run |
| What is currently believed? | `SYNOPSIS.md` and generated `ledger.md` | A link and the run’s effect on current state |
| Whose scientific result is a claim? | `frontier/evidence.yaml` and the synopsis novelty rollup | The owning evidence reference; never a chronology-based inference |
| What changed in the repository? | Git commits and the PR | A grouped pipeline summary, not a second change log |

An idea killed before a registered round belongs in the idea board’s Dead Ends section.
An approach tested under a registered round belongs in its experiment record and may be
cited by the run logbook.
The stage, not whether the result is negative, decides the owner.

The logbook separates **new scientific results from this run** from **prior retained
results used or rechecked by the run**. “New” is chronological: it says which experiment
outcomes belong to this run, whether accepted, rejected, unresolved, or otherwise.
The prior group cites earlier experiment records without copying or re-adjudicating
their verdicts.

Neither group states scientific novelty.
That is a separate, source-review-dependent axis: `common-knowledge`,
`previously-published`, `apparently-novel`, or the reserved `confirmed-novel`, as
defined in the [synopsis](../../SYNOPSIS.md#assurance-methods-and-claims).
A result produced in the current run may have no novelty assessment; a previously
published result may be rechecked in the current run.
Never infer one axis from the other.

## Entry Contract

Create the next sequential `run-NNN-YYYY-MM-DD-slug.md` after the source sessions reach
a terminal state. Use the enforced
[`ResearchLoopLogEntry/v1`](../schemas/research-loop-log-entry.schema.yaml) frontmatter
and these body sections, in this order:

1. `Context`
2. `Outcome`
3. `Run Rollup`
4. `Phase History`
5. `Results`
6. `What Worked`
7. `What Did Not Work`
8. `Pipeline Changes`
9. `Defects Affecting This Run`
10. `Validation`
11. `Claim Boundary and Next Action`

The opening Context assumes an intelligent reader with no project or conversation
history.
Define the mathematical question, the local objective, and the evidence boundary
before using internal names.

The machine-readable rollup separates four counts that are easy to conflate:

- **planned cycle slots** divide the user-level wall-clock target by the declared cycle
  length;
- **source sessions** count durable recovery records;
- **recorded phases** count material workflow, focus, or objective changes; and
- **new round results** count scientific rounds produced in this run, with their own
  criteria and verdicts.

An early evidence checkpoint may open another phase without adding wall time.
Never report phase count as elapsed cycles.
When a known phase-cap defect forces an explicit continuation, preserve both session
records and cite the defect.

Within Results, use `New Scientific Results From This Run` followed by
`Prior Retained Results Used or Rechecked`. “Rechecked” means the cited result’s own
criterion was replayed; using one formula or fixture makes it a prerequisite or control,
not a revalidation. A `rechecked` item must name the replay command or retained evidence
in `recheck_evidence`.

`packing-ledger check` validates each entry, verifies the rollup against its source
sessions, checks the cited new-round verdicts and prior-result ids, checks defect and
file references, requires every section, and rejects one session being summarized by two
logbook entries. The coordinator authors which experiments belong to a run; current
session records do not expose typed experiment membership, so the checker cannot infer
that relationship. The generated campaign ledger links every entry.

`source_commit` anchors the terminal research snapshot described by the entry.
The checker validates verdicts against the current canonical experiment records; it does
not read the historical Git tree.
Closed verdicts remain immutable under the repository’s correction policy, and later
corrections use a dated annotation or successor reference, not a silent rewrite of the
run entry.

## PR Descriptions

Use the logbook entry as the PR description source.
Link the entry, then carry over its Outcome, Run Rollup, Results, What Worked, What Did
Not Work, Pipeline Changes, Validation, and Next Action.
Keep the same counts and claim boundary; do not write a second, more flattering summary
for the PR.

From `explorations/packing`, validate a new entry with:

```shell
uv run --frozen softschema validate \
  campaign/research-loop-logbook/run-NNN-YYYY-MM-DD-slug.md
uv run --frozen packing-ledger render
uv run --frozen packing-ledger check
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
