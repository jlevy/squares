# Verification Determinations for the Agenda-010 Overnight Run

**Date:** 2026-08-31.
**Session:** [session-060](../../../packing/campaign/agent-sessions/session-060-verification-review.md)
(`BC-106` under `think-ngf0`,
[agenda-011](../../../packing/campaign/agendas/agenda-011-verification-review.md)).
**Charge:** the owner's direction after the run closed — apply the repository's
own assurance rubric and make the verified/not-verified call per result instead
of deferring to owner review; where independence is insufficient, build the
independent verification; where the rubric is unclear, say so explicitly.
The owner reviews this PR as a whole afterward.

## The Rubric Applied

From [conventions.md §4](../../../conventions.md#4-evidence) and the
[frontier evidence contract](../../../packing/frontier/frontier-evidence.schema.yaml):

- **`verified`** means an exact check, rigorous certificate, or complete proof
  decides the claim *and its preconditions*. One sound exact check suffices for
  the label; nothing numerical, however tight, qualifies.
- **Verification origin is a separate recorded fact** — external proof,
  independent implementation, repository replay, and repository audit are
  distinguished on the evidence entry, never blurred into the assurance level.
- **Independence practice** (the witness precedent, and the soundness
  perimeter's "checked by code it does not share"): a claim adopted into a
  `verified_*` field should carry at least one verification mechanism
  independent of whatever generated the object. For results that audit a
  published proof, the published proof itself is the independent side of the
  comparison; for first-party novel claims, a second method or implementation
  is built.

## The Six Determinations

**1. Bentz 2010, Theorem 8 (`s(46) = 7` lower half) — VERIFIED, fully
machine-audited.** The printed 45-point system certifies exactly over
`Q(sqrt 2, sqrt 3)` (92 cells, three lemma kinds, the Lemma 5 threshold by a
rigorous rational subdivision bound), and 45 points against 46 boxes is
pigeonhole, so the machine check covers the whole lower-bound argument.
Independence: the published peer-reviewed proof on one side, this repository's
independent implementation of the Section 1 lemma hypotheses on the other, in
agreement. Recorded as `E-bentz46-theorem8-audit`, attached to `n-046`'s
`verified_lower_bound`.

**2. The Lemma 10 settlement — VERIFIED both ways, and now source-settled.**
The lemma as printed is *refuted* by an exact escape certificate (a box of side
`1001/1000` avoiding the printed replacement set entirely), and *certified*
under the corrected reading: all three corrected replacement covers are exact,
inside the paper's own Lemma 5 parameter families. The overnight caveat —
whether the transposition `(1, 1.74)` for `(1.74, 1)` was the paper's or the
extraction pipeline's — is discharged at the strongest layer available: the
published PDF's page 5, rendered as an image and read visually, prints the
transposed value, matching the byte-level text layer. The defect is the
journal's, erratum-level; both theorem statements stand, and the paper's own
downstream usage matches the corrected reading. Recorded as
`E-bentz13-figure2-audit` plus `external_review: defect-found` on
`E-bentz-2010-proof`; the transcription carries the settlement note beside the
printed text. The partial-audit boundary is explicit: Sections 3.1–3.2's case
analysis completing `s(13) = 4` is audited as prose only, so `n-013`'s
verified floor continues to rest on the published proof, now with the repaired
lemma machine-checked beside it.

**3. exp-046 / H-044 — hold RESOLVED; the hypothesis stays undisposed by its
own registration.** The measurement is verified computation: every
establishment re-derived from stored options, every miss a typed no-partition
result under the frozen contract, byte-identical replay. The criterion is
missed under *both* denominator readings the registered text supports (23/30
and 3/10, identically in both bands), so the near-threshold hold clause has
nothing left to adjudicate. The round cannot dispose H-044: the registered
2026-08-26 amendment types the corpus calibration-only, and the ledger derives
a hypothesis-level refutation from any `rejected` round regardless of tier —
recording `rejected` would mechanically report a disposition the registration
forbids. Decision stands `unresolved`, `needs_review: false`, `reopen_when`
naming the confirmatory successor and the two priced relaxations.

**4. `s(17)` / `s(18)` — VERIFIED and UPGRADED; frontier fields moved.** The
run's `17/4` was held partly because the claim was first-party with no
external derivation. The independence gap was closed by building
[`cases/green17/interval_audit.py`](../../../packing/cases/green17/interval_audit.py):
exhaustive branch-and-bound over the full pose space in exact fixed-scale
integer arithmetic, sharing the point data and nothing else with the
lemma-cell certificate. Its verdict did more than confirm: **`17/4` was the
cell plan's ceiling, not the set's.** The audit certified the same sixteen
points at `4.3`, `4.4`, and `4426213/1000000 = 4.426213`, refuted `4427/1000`
with an exact escaping pose, and the bracket has an exact explanation — the
top wall strips' Lemma 4 hypothesis `a + 2b <= 2 sqrt 2` becomes equality at
`t* = 753/250 + sqrt 2 = 4.42621356...`, squarely inside it, with the escape
at `4.427` sitting at `theta` near `pi/4` between two unit-spaced strip
points, exactly Lemma 4's tight case. The cell certificate was rebuilt at
`4.426213` (right-wall Lemma 4 rectangles replacing the margin band and
near-slabs), both methods certify, the falsifier saturates with negative
margin at the adopted side (and finds genuine escape candidates at `4.45` and
`4.5`, corroborating the ceiling from above), and
**`verified_lower_bound` at `n = 17` and `n = 18` moved to `4.426213`** on
`E-green17-sixteen-point-lower` (exact-algebraic) plus
`E-green17-interval-audit` (interval-certified, independent implementation).
Above Nagamochi's `4.1623`; `0.019` below Green's reported but sourceless
`(40 sqrt 2 + 19)/17`. Certifying at `t*` exactly needs `Q(sqrt 2)` arithmetic
in the shared certifier and is typed as follow-on on `think-iye2`.

**5. The `m = 8` sizing statement — stands as verified arithmetic.** Every
load-bearing comparison is an exact integer inequality (the pattern ceiling
via `18816 < 21025`; the lattice dilemma exact). The parking decision is a
plan decision, not a mathematical claim; nothing further to verify, nothing
pending.

**6. The τ* diagnostic — final status: uncertified exploratory, by
construction.** Float LP on restricted grids can never meet the `verified`
bar in either direction, and the pilot says so on every run. The
determination is that this is the *final* typing, not a pending review: no
claim enters the record, the certified two-sided instrument H-034 registered
remains the named gap, and the method reading (a pure eleven-point set at
`n = 12` has at most a `~0.04`-wide window) stands as an uncertified
diagnostic guiding the next agenda.

## What the Independent Instrument Taught

Two measured obstructions, both now cured inside the tool and worth keeping:

- **Naive pose-space interval certification provably cannot terminate on this
  claim family.** Where coverage hands off between two points closer than one
  apart, both sit exactly on the square boundary in the side-one limit, so
  every single-point bound is tight with zero margin along a curved manifold.
  The cure is the *pair-handoff rule*, sound by Cauchy–Schwarz with no angle
  refinement at all — which is Lemma 2's content rediscovered in pose space,
  derived independently of the paper.
- **Triple-tight wall pockets** (container fit, point on the square edge,
  `theta` at zero) stall the same way; the cure is substituting the fit
  constraint into the rotated component (*wall-tightened bounds*), closing
  exactly at the face by single-variable concavity.

One real bug was caught by the negative controls en route: the escape probe
computed the fit margin with signed sine and manufactured a false witness at
negative `theta` — the kind of failure the control discipline exists to catch.

## Rubric Gaps Surfaced (for the owner)

- **The ledger's `status_of` ignores round tier.** Any `rejected` round makes
  its hypothesis read `refuted`, so a calibration-only round can never record
  the schema-accurate `rejected` ("criterion measured and missed") without
  mechanically overriding its own registration. Worth either a tier-aware
  derivation or a written convention; tonight's resolution (decision
  `unresolved` with the reason carrying the review) is correct but indirect.
- **"Near the threshold" in hold clauses is undefined.** Resolved here by
  robustness-across-readings (a miss under every supportable reading is not
  near anything); worth codifying.
- **`relationship_to_generator` for hand-designed objects.** The green17 set
  was designed against the lemma-cell certifier, recorded as
  `same-implementation` on the cell-certificate entry with the independent leg
  on the audit entry; confirm that reading or name a better value.
- **`reported_lower_bound` at `n = 17` still carries Nagamochi**, not Green's
  stronger reported value, because Green has no recoverable primary source.
  That is a sourcing decision deliberately left standing; the review notes it
  rather than deciding it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
