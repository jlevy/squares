# Research Loop Logbook

This logbook gives a new reader one ground-up synopsis for each bounded research-loop
run. An entry may summarize several agent sessions when a recovery session continues the
same user-level clock and objective.

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
9. `Defect Logbook`
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
- **experiments** count scientific rounds with their own criteria and verdicts.

An early evidence checkpoint may open another phase without adding wall time.
Never report phase count as elapsed cycles.
When a known phase-cap defect forces an explicit continuation, preserve both session
records and cite the defect.

`packing-ledger check` validates each entry, verifies the rollup against its source
sessions and experiments, checks defect and file references, requires every section, and
rejects one session being summarized by two logbook entries.
The generated campaign ledger links every entry.

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
