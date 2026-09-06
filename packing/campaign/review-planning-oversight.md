# W10 Review, Planning, and Oversight

W10 is the planning workflow at launch, at a research checkpoint, and at terminal
closeout. A planning block assesses the mathematical questions and the evidence for
spending effort on them, then updates the existing research queue.
It selects the next coordinating entry point, which may dispatch several independent
commitments in parallel.
It does not execute those successors.

## Entry Contract

Declare the planning scope and its owning bead.
For a multi-lane portfolio decision, use a BC item in the active agenda with
`workflows: [review-planning-oversight]`. A short routine re-screen can stay in its
existing bead or session phase.
Bring the source reviews, idea board, H-items, negative results, agenda, retained
experiment and session records, validation receipts, and live tbd state.

At a checkpoint, only the evidence being assessed must be stable.
Name any continuing process and preserve its frozen contract; do not mark its work
terminal or change its criterion, regime, or scientific budget.
Terminal closeout additionally requires every writer and long-running process in the
source agenda to have ended.
Assessment can overlap disjoint continuing work.
Shared-record integration, commits, and repository-wide validation wait until their
writers stop at the existing
[session integration boundary](agent-sessions/README.md#starting-a-session).

## One Planning Block

1. **Assess the questions.** Read both strategic proposals and adversarial reviews.
   For each direction, state the mechanism, supporting and contrary evidence, scope
   limits, plausible payoff, cheapest useful discriminator, and what would change its
   priority. Separate proved results, numerical observations, and speculation.
   Delegate independent mathematical assessments; one coordinator reconciles them.
2. **Map the hypotheses.** Reuse an H-item only when its claim and regime match.
   Register a distinct claim before testing it; preserve a broader direction as
   `kind: open_question` when its criterion or domain is not yet defined.
   Keep its source on the idea board and link the H-item from the relevant BC’s
   `hypotheses`. Build, review, planning, and publication tasks need no invented
   mathematical H-item.
3. **Select bounded work.** Update the owning agenda’s items, priorities, real
   prerequisites, and parallel groups.
   Price the next discriminator and integration, not the entire speculative program.
   State a stop or reconsideration condition for each selected commitment; keep later
   allocations conditional.
   A ready item is takeable, not automatically funded.
4. **Assign execution.** Give each selected BC one accountable bead and disjoint worker
   deliverables. Record the next checkpoint and available capacity in the agenda; record
   actual clocks and recovery in the session when escalation applies.
   One selected coordinator can dispatch several ready BCs.
   Scientific or write dependencies serialize work; membership in one manager group does
   not.
5. **Distill and check.** A tbd plan document may retain the assessment, alternatives,
   source coverage, and design decisions.
   Link it from the planning BC and its bead.
   Before closing the block, put claims in H-items, operational commitments in the
   agenda, and ownership in beads.
   Regenerate the existing views and check references, readiness, prerequisites, and
   frozen criteria. Publish the checkpoint and name its next entry.
   Do not create an experiment just to count planning as research.

These steps use the existing [work units](../../SYNOPSIS.md#work-units-and-records) and
[control records](../../SYNOPSIS.md#identifiers-and-control-records).
Programs and parallel groups are labels on BC items; they need no separate registry.
The plan supplies rationale, not another live queue.
Sessions record execution, not a second copy of the agenda.
A new session or agent does not create a new hypothesis.

Bounded assessment and codification of supplied ideas belong in this planning block.
A substantial new derivation or exploration enters W3; a missing source enters W1; a
requested framework correction enters W4; an actual test enters W6 after registration.
The planning BC may link those sub-beads without pretending they are one experiment.

At exit, every selected research direction has an H-item and every selected action has
an agenda commitment and bead.
Unshaped directions remain visible as open questions; deferred work says what would
justify selection. A future agent can dispatch from the agenda and follow its links
without reconstructing the conversation or reading the full assessment first.

## Terminal Closeout

The additional reconciliation below applies to a terminal agenda.
A session may close while its agenda remains active; follow the
[session close procedure](agent-sessions/README.md#closing-a-session) for that narrower
boundary. Neither session closure nor checkpoint planning closes an unfinished agenda.

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

### Required Closeout

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
7. Select exactly one next coordinating bead and workflow, state why it outranks the
   alternatives, and update the current handoff.
   That entry may dispatch the agenda’s independent BC items concurrently; it is not a
   one-worker limit. Only then authorize a candidate agenda to execute.
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

W10 may edit planning records and reader-facing summaries to reconcile established
evidence.
It may not change a frozen scientific criterion, reinterpret a stopped run as a
result, fix the defects it discovers, or begin the next agenda in the same phase.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
