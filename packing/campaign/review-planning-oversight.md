# W10 Review, Planning, and Oversight

W10 is the terminal reconciliation and planning workflow.
It turns an executed agenda into an honest account of results, gives every unfinished
block an actionable disposition, reviews the documents readers rely on, and selects one
next entry point. It does not execute that successor.

## Entry Contract

Enter after every writer and long-running process in the source agenda is terminal.
Bring the frozen agenda, experiment and session records, validation receipts, current
SYNOPSIS, generated views, live tbd state, and any operator direction received at the
boundary.

Classify the smallest declared scope that has one answer.
A partially successful agenda item may therefore have more than one outcome row.

| Classification | What the evidence permits | Required disposition |
| --- | --- | --- |
| `achieved` | Valid work met its frozen exit at the stated scope | `retire-success` |
| `bounded-negative` | A valid search exhausted its declared domain or budget without a qualifying object | `retire-negative` |
| `time-limited` | Valid work began, but an external wall arrived before completion | `continue` |
| `guard-refused` | A correct admission, provenance, validity, or safety guard rejected the stage | `defer-dependency` |
| `technical-failure` | A crash, checker defect, malformed control, or instrument failure prevented valid completion | `fix-and-rerun` |
| `never-opened` | An upstream route never authorized execution | `defer-dependency` |
| `inconclusive` | The full valid protocol ran, but its frozen criterion did not discriminate | `continue` |

Decision precedence prevents a convenient label from hiding what happened: never opened,
then correct guard refusal, then unintended technical failure, then unfinished at the
wall, and only then achieved, bounded-negative, or inconclusive under the frozen
criterion. A negative result must name the completed search space and budget.
A partial prefix, refused run, or unopened route is not a negative result.

## Required Closeout

1. Freeze the evidence and verify that every agenda item is `complete` or `stopped`.
2. Record one or more outcome rows for every item, including result, evidence,
   classification, disposition, and follow-up bead where work remains.
3. Regenerate the ledger, agenda map, session-close report, synopsis views, and document
   map from their owning records.
4. Reconcile `SYNOPSIS.md`, then review `README.md`, `TUTORIAL.md`, `conventions.md`,
   `development.md`, and `operating-rules.md`; mark each updated, checked current, or
   not applicable with a reason.
5. Reconcile live tbd: close settled work, preserve deferred work, add newly exposed
   repairs, and rank the surviving candidates.
6. Ask the operator to confirm the closeout and offer reprioritizations or new ideas
   when an operator is available.
   Record `confirmed`, `revised`, or `unavailable`. An unavailable operator does not
   stall an autonomous mandate: keep the frozen ranking and use the declared fallback.
7. Select exactly one next bead and workflow, state why it outranks the alternatives,
   update the current handoff, and only then authorize a candidate agenda to execute.
8. Publish a pull-request description that leads with measured cost and then reports
   actual results, stop reasons, dispositions, grouped file changes, validation, and the
   next boundary.

For a terminal agenda with a versioned session, run from `packing/`:

```shell
uv run --frozen --all-extras --group dev python -m devtools.close_session \
  --render --session session-NNN --agenda agenda-NNN
```

The command performs the mechanical regeneration and prints the repository-owned PR
description.
The judgment fields must already be present in the agenda closeout; the tool
refuses to invent outcomes, dispositions, document decisions, or priorities.

## Boundary with Other Workflows

W8 performs a substantive documentation reconciliation when reader-facing prose has
drifted materially. W10 always performs the lighter impact review and routes to W8 when
that review finds work it cannot settle safely.
W9 executes defect-remediation waves selected here.
W1–W7 continue to own research, review, experimentation, measurement, and
implementation.

W10 may edit records and reader-facing summaries to reconcile established evidence.
It may not change a frozen scientific criterion, reinterpret a stopped run as a result,
fix the defects it discovers, or begin the next agenda in the same phase.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
