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

Build the reusable evidence and annotation layers that a constructive proposer needs,
then price the next layer before implementing it.
The first checkpoint is now complete: all known-best constructions for `n = 1..100` have
retained provenance, normalized `Witness/v2` geometry, numerical or exact receipts, and
deterministic house renderings.

The remaining overnight objective is a deterministic chunk-partition contract and its
controls, a contact-assembly grammar that fits the observed non-grid corpus, and a
measured enumeration-feasibility map.
The session’s success condition is **corpus and instruments that pass their own
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
| 1 | **W7** `pipeline-improvement` | Corpus importer, partition certificates, detector, overlays, and enumeration accounting. The bulk of the night | ~60% |
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

The autonomous loop advances one bounded slice per continuation and writes a durable
checkpoint before selecting the next slice.
The order below is by dependency; a later continuation resumes at the first incomplete
item rather than repeating completed work.

**Checkpoint A — known-best corpus and first descriptive census: complete.** `BC-023` /
`think-osm7` now covers all `n = 1..100`: 64 canonical exact grids, 34 attributed
Kingbird-derived numerical fact records with no retained raw SVG in this source
inventory, and two explicitly rendering-derived UnitSquare normalizations.
Every case has a witness, receipt, source record, frontier link, and house rendering.
The first census keeps a narrow maximal-lattice view separate from a broader same-angle
contact-assembly view.

**Checkpoint B — factual disposition of PR #44: complete.** The retained review accepts
the proposer/refiner split and grammar-freeze principle, but identifies the
chunk-count/angle-count conflation, the missing minimal-partition objective, the
now-inspected calibration corpus, and conditional rather than automatic enumeration
completeness.

**Checkpoint C — bounded lattice partition: complete as a calibration control.**
`BC-019` now has an exact-cover splitter over contiguous bars, filled rectangles, and
corner Ls inside maximal lattice components.
It evaluates every allowed exact free-square count `F`, prefers a certificate inside the
six-chunk budget, then minimizes `F` and chunk count `C`. Deterministic residual and
minimum-remaining-values traversal ties select the certificate, and state-cap and
candidate-universe limits remain typed.
An earlier capped `F` slice does not erase a later existence certificate, but it leaves
the retained certificate’s `F`/`C` minimality explicitly indeterminate.
For an out-of-budget retained certificate, any capped `F` slice also leaves budget
selection and `F`/`C` minimality indeterminate.
It certifies all 64 grid-derived cases and 3 of 36 non-grid cases inside the
six-chunk/two-free budget.
Two non-grid cases are conclusively outside that budget, 23 have no partition in this
universe, and eight are search-capped and therefore indeterminate after the 10,000-state
limit. No H-044 verdict is emitted.

The broader non-grid contact components retain 859 internal slide degrees under their
normal equalities before overlap intervals and wall contacts are applied.
That is the next design constraint: connectedness alone does not buy a rigid or
low-dimensional enumeration object.

**Checkpoint D — contact-assembly grammar and finite labels: complete and factually
accepted.** The draft grammar now charges internal slide degrees so one giant connected
component cannot make coverage vacuous, while the lattice splitter remains an
independent strict control.
The first geometry-free implementation canonicalizes signed contact normals, wall
colors, and caller-normalized semantic colors under square relabeling and all eight D4
symmetries for scaffolds of at most five squares.
It retains replayable orbit witnesses and typed candidate, emitted-label, and
orbit-image caps. Exhaustive controls distinguish ordinary topology counts from the
deliberately richer signed-contact quotient.

The acceptance pass proved D4 composition and endpoint reversal independently, rather
than relying only on self-consistent orbit labels.
It also exposed two branch-level portability defects: the new handoff bypassed the
renderer gallery, and retained census trigonometry depended on platform `libm` rounding.
Both repairs preserve the registered census semantics and passed complete Linux and
macOS validation before the later PR review.

**Checkpoint E — bounded local contact realization: complete and factually accepted.**
The target-free assembly-frame prefilter fixes translation, enforces signed unit normal
equalities and a declared positive tangential-overlap margin, canonicalizes and
deduplicates labels before solving, distinguishes infeasible from solver-indeterminate,
and stops at a typed LP-solve cap.
It rejects wall-bearing labels and mixed fitted-angle classes before solving and makes
no statement about non-edge separation, container fit, whole-packing feasibility, or
optimality.

The independent pass accepted those boundaries after mutating gauge, normal signs,
overlap, wall and non-edge exclusions, solver statuses, duplicate labels, and solve-cap
accounting. A concrete overlapping-non-edge counterexample confirms that a local receipt
cannot be promoted to packing feasibility.

**Checkpoint F — target-free enumeration price: complete through the bounded control.**
The exact connected four-edge-color labeled counts for sizes 1 through 5 are `1`, `4`,
`112`, `15,104`, and `9,684,224`. Exhaustive D4-by-relabeling canonicalization through
size 4 reduces those rows to `1`, `1`, `7`, and `124` local LP solves; `1`, `1`, `4`,
and `26` are locally feasible at the declared overlap margin, with no indeterminate
solves. The raw size-five path would inspect at most `9,296,855,040` orbit images, far
above its ten-million-image cap.
Its independently checked isomorph-free replacement reduces 1,533,696 topology colorings
to 11,013 abstract orbits and deliberately runs no size-five LP. These counts are
target-free engineering evidence, not atlas coverage or packing feasibility.

**Checkpoint G — descriptive contact overlays: complete and factually accepted.** The
registered 1–100 census already retains wall seating, contact-graph topology, internal
slide count, component membership, and edge residuals.
A new renderer feature keeps those tolerance-qualified graph edges separate from exact
certified contact loci.
Five deterministic structural strata (`n = 11`, `28`, `40`, `68`, and `89`) now have
house-rendered overlays with visible square IDs, centre-to-centre contact-graph edges,
and centre-to-wall seating edges.
The gallery is calibration evidence and emits no H-044 verdict.

The independent review now rejects mismatched witnesses, unchecked geometry,
over-tolerance residuals, invalid detector tolerances, and unstable feature order.
Every SVG visibly states both registered tolerances and that its dashed graph edges are
not exact contact geometry; all five representative renderings passed visual review.

**Later infrastructure slices — complete.** The prospective source map covers
`n = 101..324` without derived annotations or video coordinates.
Its admitted seed is limited to exact grids and the four UnitSquare cases covered by the
upstream dataset’s reuse terms; the Kingbird retention boundary is resolved separately
in the source policy.

The independently checked isomorph-free path reduces 1,533,696 size-five topology
colorings to 11,013 abstract contact-scaffold orbits.
The retained atlas contains no packing geometry, local-LP outcome, feasibility claim, or
H-044 verdict. CG-010 now supplies a separate literal target-free structural full-cell
control with a total wall inventory, an exhaustive pair partition, one frozen oriented
axis per pair, a joint D4-by-relabeling label, and separated candidate-domain and
executed-work prices.
Its control examines one selected raw cell through 48 orbit images and performs zero LP
solves. Numerical row compilation and realization remain unbuilt, and no target-sized
execution is authorized.

**Finalization reserve.** Reconcile generated views, run the proportionate gate, update
the session and research-loop records, commit, push, and leave the exact first
unfinished slice. Do not start new target work in the reserve.

Do **not** reach `BC-021` (the `n = 11` enumeration run) tonight.
The corpus has now been inspected while designing the detector, so a later `n = 11` run
is retrospective replay, not unseen rediscovery.
A confirmatory proposer claim needs a prospectively frozen target after the grammar,
split, and complexity controls are committed.

## The One Irreversible Decision

The annotation-contract freeze now precedes the grammar freeze.
After a freeze, no change to source selection, tolerances, candidate shapes, split
objective, symmetry rules, bounds, or enumeration order may be made without creating a
new version and invalidating the corresponding prospective evaluation.
Name every freeze commit in the session record.
An open grammar is a normal state; a silently adjusted one is a defect.

## Guardrails

- **A run that beats a standing record is suspect.** Replay it independently and require
  formal or interval verification before making a record claim; a numerical improvement
  alone does not update the frontier.
- **`beat_record: true` requires `verified` assurance.** Numerical results stay
  numerical at any precision.
- **The solver floor is about `1e-11` in the side** ([D-021](../../../../defects.md)).
  No comparison finer than that is admissible.
- **A stopped quench is not a certified local optimum**
  ([D-052](../../../../defects.md)).
- **Imported decimal geometry is `numerically-checked`, never `verified`.** Record the
  method, actual precision, rounding, and tolerance.
- **A source rendering is evidence at its displayed precision only.** It does not replay
  unavailable interval coordinates or another site’s assurance claim.
- **Videos are visual cross-checks, not coordinate sources**, while retained vector
  geometry exists. All project-facing atlas images use the house renderer.
- **Unattended numerical execution stays NO-GO.** Every cell here is a bounded,
  deterministic, supervised slice; none needs the numeric runner.
- **Do not start basin-frequency work**, and do not reinterpret the exp-035 through
  exp-042 chain as a connectivity proof.
- **`git commit --no-verify` is not for PRs.** The lefthook pre-commit hook formats the
  whole repository; do not narrow it to staged files, and do not format generated views
  by hand.

## Environment

Use the repository lock and the supported invocation from `development.md`:

```bash
cd explorations/packing
uv run --frozen --all-extras --group dev packing-validate --fast
```

If a provenance step fails, retain the exact failure and inspect repository history
before deciding whether the cause is environmental.
Do not mutate global tooling or assume every checkout is shallow from a plan written on
one host.

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
