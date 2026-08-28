# Feature: The Interval Certification Bridge

**Date:** 2026-08-28

**Author:** Claude (agent), from a planning session with the repository owner

**Status:** Draft

## Overview

Build the checker that turns a high-precision numerical root into a `verified` result,
so a reported value can be certified without first recovering an exact algebraic form.

This is the missing half of TUTORIAL §5’s step six.
It is not a smaller version of the exact route — it is the *other* route, and it is the
one that is tractable with near-certainty.

The distinction matters for planning.
The exact route
([plan-2026-08-28-promotion-pipeline-implementation](plan-2026-08-28-promotion-pipeline-implementation.md))
recovers a minimal polynomial and discharges it by exact substitution.
That is strictly stronger, and it may not terminate: a sweep recorded in
[X-004](../../../../campaign/explorations/X-004-n29-exact-promotion.md) found no integer
relation through degree twenty with coefficients below `10^22`, so `s(29)`'s minimal
polynomial is large, and Gröbner elimination in six unknowns may not finish.
Interval certification does not need the polynomial at all.

`n = 29` is the target.
Certifying its reported value moves this repository’s `verified_upper_bound` from the
Schadt rational `5.93388579981302587863645209` to Kingbird’s `5.93383346267692`, closing
a `5.23e-5` gap that no amount of better sourcing can close because no public
certificate exists.

## Goals

- Prove existence and uniqueness of a root of a declared contact system inside an
  outward-rounded box, by a Krawczyk or interval-Newton operator.
- Propagate that box through the layout map to outward-rounded square poses, and verify
  separation and containment on intervals rather than on floats.
- Emit a `Witness/v1` record whose `method` is `interval-certified` and which the
  existing witness pipeline accepts as `verified` rather than refusing with
  `checker-not-built`.
- Calibrate at sizes where the answer is already known, so the checker can be caught
  being wrong before it is trusted at `n = 29`.

## Non-Goals

- **Any optimality claim.** Certifying an upper bound leaves the `n = 29` bound gap of
  about `0.46` untouched.
  A matching lower bound is separate mathematics.
- **Any record improvement.** This certifies an existing construction.
- **Replacing the exact route.** Where an exact algebraic form is recoverable it remains
  preferred, because exact substitution is stronger than an enclosure.
  The two routes are complements, and this spec does not deprecate the other.
- **Generic contact inference.** The system and the layout map are inputs here, not
  things this feature derives.

## Background

### What already exists, and it is more than it looks

The witness contract **already names this method**.
[`sqpack.assurance`](../../../../src/sqpack/assurance.py) lists `interval-certified`
among the methods that may carry `verified`, and
[`sqpack.witness`](../../../../src/sqpack/witness.py) enforces that `verified` assurance
requires `exact-algebraic` or `interval-certified`. The only thing missing is the
checker itself: `exact_verify` raises

```
WitnessError("checker-not-built",
  "Witness/v1 can describe interval evidence, but the generic interval "
  "certificate checker is not built")
```

So this feature fills a socket that was deliberately left open, rather than inventing a
new contract.

[`sqpack.field`](../../../../src/sqpack/field.py) already does rigorous interval work:
it isolates a real root by bisecting until the enclosure excludes zero, narrows an
isolating interval below a requested precision, and returns rigorous enclosures of a
polynomial over an interval.
That is the arithmetic core, applied to one univariate polynomial.
What is absent is the multivariate operator and everything downstream of it.

[`sqpack.verify`](../../../../src/sqpack/verify.py) checks separating-axis validity with
an injected `sign` callable, which is the seam this feature needs: an interval `sign`
that returns a definite sign only when the enclosure excludes zero, and otherwise
refuses.

### What is missing

| Piece | State |
| --- | --- |
| Multivariate interval arithmetic with directed rounding | unbuilt |
| Krawczyk / interval-Newton existence-and-uniqueness operator | unbuilt |
| Outward-rounded layout map, pose box to square boxes | unbuilt |
| Interval `sign` that refuses rather than guesses | unbuilt |
| `scalar.kind` for an enclosure | **absent from the schema** |
| `exact_verify` branch for `interval-certified` | raises `checker-not-built` |

The schema gap is real and needs a deliberate decision.
[`witness.schema.yaml`](../../../../witnesses/witness.schema.yaml) declares
`kind: {enum: [decimal, rational, algebraic-number-field]}`. An enclosure is none of
those. Adding a fourth kind is a contract change, and it must be made as one.

### Why `n = 29` is the natural target

Everything upstream is already published and already transcribed.
The provenance SVG carries nine slide scalars in closed form, six equations `f1 … f6` in
`{s, a, b, c, d, i}`, **and the layout map**: its `<use>` transforms are written
symbolically in those same names, for example
`translate(2 1) rotate(&a;) translate(0 -&r1;)`.
[`cases.kingbird29.verify_svg`](../../../../cases/kingbird29/verify_svg.py) transcribes
the system and parses the transforms.

So the two inputs this feature declares as prerequisites — a contact system and a layout
map — exist at `n = 29` today, with no assembler required.
That is why this can start immediately rather than queueing behind BC-042 and BC-043.

## Design

### The mathematical core

Given `F: R^m -> R^m` (the closed contact system) and an approximate root `x*`, the
**Krawczyk operator** on a box `X` containing `x*` is

```
K(X) = x* - C F(x*) + (I - C F'(X)) (X - x*)
```

where `C` is an approximate inverse of `F'(x*)`, evaluated in interval arithmetic with
directed rounding.

Two standard facts do the work, and the implementation must depend on nothing else:

- If `K(X)` is a subset of `X`, then `F` has **at least one** root in `X`.
- If additionally `K(X)` is in the *interior* of `X`, the root is **unique** in `X`.

The second condition is the one that matters, and the implementation must check interior
containment rather than containment, because the weaker check does not give uniqueness.

Interval-Newton is an acceptable alternative and has the same contract; Krawczyk is
preferred because it needs no interval matrix inversion.

### Approach

Four stages, each of which can refuse:

```
pose box  ->  Krawczyk certify  ->  layout map  ->  interval SAT  ->  witness
 (input)      (root exists,        (outward-      (separation and    (interval-
               is unique)           rounded)       containment)       certified)
```

Refusal is a first-class result at every stage.
A checker that cannot fail has not been tested, and a checker that silently widens until
it succeeds is worse than none.

### Components

| Component | Role |
| --- | --- |
| `promote/interval.py` | Interval scalars with directed rounding; `+ - * /`, `sin`, `cos`, comparison that refuses on straddling zero |
| `promote/krawczyk.py` | The operator, existence and uniqueness verdicts, and a typed refusal carrying the failing box |
| `promote/enclose.py` | Layout map from a certified pose box to outward-rounded square boxes |
| `promote/interval_verify.py` | `verify_packing` driven by an interval `sign` |
| `sqpack.witness` | New `interval-certified` branch replacing the `checker-not-built` raise |

Interval arithmetic is built on `mpmath.iv`, which supplies directed rounding and
interval transcendentals, rather than hand-rolled.
The reason to prefer it is narrow and worth stating: rounding-mode errors in
hand-written interval code fail *silently and in the unsafe direction*, producing
enclosures that are too tight and certificates that are wrong.

### Data shapes

```python
@dataclass(frozen=True)
class PoseBox:
    names: tuple[str, ...]  # unknown names, in a declared canonical order
    lo: tuple[str, ...]  # exact decimal strings, one per unknown
    hi: tuple[str, ...]
    radius: str  # max half-width, for reporting


@dataclass(frozen=True)
class CertifiedRoot:
    box: PoseBox
    exists: bool  # K(X) subset of X
    unique: bool  # K(X) in the interior of X
    operator: str  # "krawczyk" | "interval-newton"
    iterations: int
    working_precision: int
```

`unique` is the load-bearing field.
`exists` without `unique` may not be promoted, because a box holding two roots does not
identify which pose was certified.

### API changes

One schema change, made deliberately: `witness.schema.yaml` gains a fourth
`scalar.kind`, `interval-enclosure`, carrying the contact system, the certified pose
box, and the operator verdict.
This is a `Witness/v1` extension by enum addition; if the soft-schema policy treats enum
widening as breaking, it becomes `Witness/v2` and the existing writers are migrated in
the same change rather than left straddling two versions.

No change to `verify_packing`’s signature — it already accepts an injected `sign`.

## Implementation Plan

### Phase 1: Interval arithmetic and the operator

- [ ] `promote/interval.py` over `mpmath.iv`, with a `sign` that returns `0` only when
  it can prove the enclosure contains zero and otherwise **refuses** rather than
  guessing.
- [ ] `promote/krawczyk.py` implementing `K(X)`, returning `CertifiedRoot` with `exists`
  and `unique` reported separately.
- [ ] Calibrate on a univariate case with a known answer, cross-checked against
  `sqpack.field`’s existing isolating-interval machinery, which is independent of this
  code path.
- [ ] Negative control: a box containing **two** roots must return
  `exists=True, unique=False`, never `unique=True`.
- [ ] Negative control: a box containing **no** root must return `exists=False`.

### Phase 2: The layout map and interval verification

- [ ] `promote/enclose.py`: propagate a certified `PoseBox` through the layout map to
  outward-rounded square corner boxes.
- [ ] `promote/interval_verify.py`: `verify_packing` under the interval `sign`, so a
  pair whose separation enclosure straddles zero is a refusal and not a pass.
- [ ] Negative control: shrink the container side below the packing and require refusal.
- [ ] Negative control: widen the pose box until separation is undecidable and require a
  typed refusal naming the pair — **not** a silent pass.

### Phase 3: Calibration where the answer is known

- [ ] Certify `n = 5` and `n = 10`, whose Göbel constructions are exact and already
  reach `verified` by the exact route.
  The interval verdict must agree with the exact one.
- [ ] Certify `n = 11` against Trump’s published polynomial: the certified box must
  contain the known algebraic root.
- [ ] Demonstrate the checker **refuses** on a pose that is numerically plausible but
  not actually feasible, since agreeing with the exact route on valid inputs proves
  nothing about discrimination.

### Phase 4: `n = 29`

- [ ] Drive the `cases.kingbird29` system and layout map from a BC-047 refinement.
- [ ] Certify, and record whatever comes back, including a typed refusal.
- [ ] On success, emit an `interval-certified` witness and move `verified_upper_bound`
  through the normal evidence contract — as a reviewed change, never as a search result
  written into the record.

## Testing Strategy

The calibration is the test, and it is stronger here than for the exact route because
`n = 5`, `n = 10` and `n = 11` all have answers this implementation cannot influence.

Two failure modes need different checks:

- **An unsound certificate** — claiming uniqueness that does not hold — is caught by the
  two-root and no-root controls in phase 1, and by disagreement with the exact route in
  phase 3.
- **A vacuous certificate** — a box so wide that verification is meaningless — is caught
  by requiring the reported `radius` to be recorded and by the phase-2 widening control.

Every stage that can refuse must have a control proving it refuses.

An unattended runner may not accept a scientific verdict from this chain.
A round that certifies `n = 29` is recorded `unresolved` with `needs_review: true`, and
a human makes the accept decision, exactly as for exp-045.

## Rollout Plan

Each stage lands with its controls, behind the existing gate.
Nothing enters `frontier/` without passing the witness and evidence contracts.

The bound move at `n = 29` is the last step and a deliberate one.
Until it happens, `verified_upper_bound` stays where it is, and no document may describe
the reported value as certified.

## Open Questions

- Is `mpmath.iv` sound enough for a certificate, given that it is not a formally
  verified library? The honest answer is that it is better than hand-rolled rounding and
  worse than a proof assistant; the assurance ladder should record `interval-certified`
  as below `proof-assistant-checked`, which it already does.
- How wide can the pose box be before interval separating-axis tests go undecidable?
  This is the practical limit and is unknown until measured; it decides how much
  precision BC-047 must supply.
- Does the `n = 29` contact system have a well-conditioned Jacobian at the root?
  Ill-conditioning would make the Krawczyk contraction fail even though the packing is
  fine, which is a checker limitation and must be reported as one rather than as a
  negative result about the packing.
- Does enum widening on `scalar.kind` count as breaking under the soft-schema policy?
  This decides `Witness/v1` extension versus `Witness/v2` migration.

## References

- [BC-045 in agenda-005](../../../../campaign/agendas/agenda-005-symbolic-promotion-and-identity.md)
- [plan-2026-08-28 — the promotion pipeline implementation](plan-2026-08-28-promotion-pipeline-implementation.md)
- [plan-2026-08-28 — the symbolic promotion gap](plan-2026-08-28-symbolic-promotion-and-the-atlas.md)
- [X-004 — an exact algebraic characterization of the `n = 29` record](../../../../campaign/explorations/X-004-n29-exact-promotion.md)
- [TUTORIAL §5 — from a numeric solution to an exact one](../../../../TUTORIAL.md#from-a-numeric-solution-to-an-exact-one)
- [SYNOPSIS — What Is Built](../../../../SYNOPSIS.md#what-is-built)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
