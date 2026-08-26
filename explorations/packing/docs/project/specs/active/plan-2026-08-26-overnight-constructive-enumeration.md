# Overnight Run: Constructive Enumeration Groundwork

**Date:** 2026-08-26

**Owns:** The handoff contract for one bounded overnight session on the constructive
proposer lane: what to do, in what order, under which workflow, and what may not be
claimed.

**Does not own:** The scientific claims, which live in
[H-044 through H-048](../../../../campaign/ideas.md); the cell order, which lives in
[agenda-002](../../../../campaign/agendas/agenda-002-constructive-enumeration-groundwork.md);
or the design rationale, which lives in
[X-003](../../../../campaign/explorations/X-003-stratified-chunk-enumeration.md).

## Objective

Build the tooling for stratified chunk enumeration on foundations that can carry its
results, and import the record-geometry corpus every chunk measurement reads.
The session’s success condition is **instruments and corpus that pass their own
controls**, not a scientific verdict and emphatically not a record.

## Read First, in This Order

1. [X-003](../../../../campaign/explorations/X-003-stratified-chunk-enumeration.md) —
   the design, its grading against the archive, and its known risks.
2. [agenda-002](../../../../campaign/agendas/agenda-002-constructive-enumeration-groundwork.md)
   — the cell order and why it is that order.
3. [H-044](../../../../campaign/hypotheses/H-044-chunk-expressibility-of-records.md) and
   [H-047](../../../../campaign/hypotheses/H-047-chunk-regular-predecessors.md) — the
   two claims whose instruments this session builds.
4. [The campaign runbook](../../../../campaign/README.md#the-bounded-research-cycle) —
   slice protocol, clocks, refusal rules.
5. [`development.md`](../../../../development.md) — code placement, validation loops,
   CLI policy.

Assume no memory of the design conversation.
Everything needed is in those five documents.

## Workflow Switching

Switch workflows as the work demands rather than forcing everything through one; declare
the switch at a checkpoint and record it as an ordered phase.
The [entry contracts](../../../../SYNOPSIS.md#workflow-entry-contracts) are
authoritative. Expected rough shape for this session:

| Priority | Workflow | Use it for | Expected share |
| --- | --- | --- | --- |
| 1 | **W7** `pipeline-improvement` | The enumerator, glued rows, sweep driver, detector, corpus importer. The bulk of the night | ~60% |
| 2 | **W5** `efficiency-loop` | Only if a measured bottleneck blocks iteration; bring a baseline and a profile, not a hunch | ~10% |
| 3 | **W2** `factual-review` | Before any instrument’s output is trusted, and before any claim touches a hypothesis artifact | ~10% |
| 4 | **W3** `insight-iteration` | Freeform chunk-and-quench exploration on the corpus once it exists; may implement bounded exploratory derivations and visualizations | ~15% |
| 5 | **W4** `process-review` | Only if the record itself is hard to reconstruct | ~5% |

**W6 is deliberately not on the list.** No preregistered experiment round should be run
tonight: every instrument here is new, and a round measured on an unreviewed instrument
is the shape of most soundness defects in this repository’s log.
The night ends with instruments that are *ready* for W6, and the first round is a
supervised decision.

Freeform W3 exploration is encouraged once the corpus exists, and its output is
candidate structure, notes, and idea-board rows.
It may not emit a verdict on H-044 through H-048; those need a frozen criterion and an
independent review pass first.

## Queue, in Order

Roughly eight hours of work, ordered by dependency.
Cells inside one bracket are independent and may be reordered or run in parallel.

**Hours 0-1 — start the corpus, it unblocks the most.** `BC-023` / `think-osm7`: import
standing-record geometry for `n <= 100` from the archived catalogue into `Witness/v1`,
with retained provenance and a numerical check per case.
Populate `tilt_angles_deg` and the derived angle-class count in each frontier case
artifact, replacing the nulls most of them carry.
Typed absent-or-ambiguous failures are a legitimate output; guessing a coordinate
convention is not.

**Hours 1-3 — the two foundations, independent of each other.**

- `BC-016` / `think-zt29`: the degenerate-cell differential.
  Aligned and glued strata are the most tie-rich linear programs this pipeline will ever
  solve, and [D-059](../../../../defects.md) says endpoint identity there can be
  toolchain-dependent.
  Measure it before any ranking is trusted.
  An instability finding blocks `BC-018` rather than being carried into it.
- `BC-017` / `think-u97a`: price a stratum in counted LP solves end to end, so results
  are comparable without reference to wall time ([D-126](../../../../defects.md)).

**Hours 3-6 — the instruments.**

- `BC-018` / `think-sfzh`, `think-vnm5`, `think-dh4b`: stage-1 enumerator, glued-chunk
  equality rows, coarse class-angle sweep driver.
  Calibrate against `n = 5` and `n = 10` proved optima and the `n = 16` not-below guard.
- The chunk-decomposition detector for `BC-019` / `BC-024`, with the two-band adjacency
  rule and free squares, per H-044.

**Hours 6-7.5 — first measurements and exploration.**

- `BC-024` / `think-kr1d`: the descriptive chunk taxonomy over the imported corpus.
  What chunk shapes, sizes, tilted-chunk counts, and wall seatings actually recur.
- W3 freeform: regularize a few poses, re-quench, watch what happens.
  Notes and idea rows, no verdicts.

**Hours 7.5-8 — finalization reserve.** Reconcile generated views, run the gate, write
the session artifact and handoff, commit and push.
Do not start new work in this window.

Do **not** reach `BC-021` (the `n = 11` enumeration run) tonight.
It is blocked on the grammar freeze and on the coverage measurement, and running it
early would make
[H-045](../../../../campaign/hypotheses/H-045-chunk-grammar-rediscovery.md)’s criterion
vacuous.

## The One Irreversible Decision

The grammar freeze at `BC-018` is the point after which no design change may be made
without invalidating H-045. If the night reaches that point, name the freeze commit in
the session record. If it does not, say so plainly and leave the grammar open; an
unfrozen grammar is a normal state, and a silently adjusted one is a defect.

## Guardrails

- **A run that beats a record has a bug** until an independent exact layer says
  otherwise. This pre-registered rule has already caught a critical defect here.
- **`beat_record: true` requires `verified` assurance.** Numerical results stay
  numerical at any precision.
- **The solver floor is about `1e-11` in the side** ([D-021](../../../../defects.md)).
  No comparison finer than that is admissible.
- **A stopped quench is not a certified local optimum**
  ([D-052](../../../../defects.md)).
- **Imported decimal geometry is `numerically-checked`, never `verified`.** Record the
  method, actual precision, rounding, and tolerance.
- **Unattended numerical execution stays NO-GO.** Every cell here is a bounded,
  deterministic, supervised slice; none needs the numeric runner.
- **Do not start basin-frequency work**, and do not reinterpret the exp-035 through
  exp-042 chain as a connectivity proof.
- **`git commit --no-verify` is not for PRs.** The lefthook pre-commit hook formats the
  whole repository; do not narrow it to staged files, and do not format generated views
  by hand.

## Environment

The pinned `uv` on this image cannot bootstrap CPython 3.14.7. Install a newer uv and
invoke it as a module:

```bash
pip install --upgrade 'uv>=0.12'
cd explorations/packing
python3 -m uv run --frozen --all-extras --group dev packing-validate --fast
```

The clone is shallow, so the provenance gate step fails on one unreachable historical
engine commit until `git fetch --unshallow` runs.
That failure is environmental and is not a defect in the tree.

## What the Session Owes at the End

An [agent-session artifact](../../../../campaign/agent-sessions/README.md) with the
ordered phase history, budget, evidence, stop reason, and a handoff naming the exact
next bounded slice; a green gate or a named reason it is not green; regenerated ledger
and defect views; new defects logged in `defects.yaml` with what caught them; and a
pushed branch with a draft pull request.

Any instrument built tonight that has not passed an independent review pass must say so
in its handoff, so the first W6 round knows what it is standing on.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
