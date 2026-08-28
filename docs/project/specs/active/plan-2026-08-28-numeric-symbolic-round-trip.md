# Feature: The Numeric–Symbolic Round Trip

**Date:** 2026-08-28

**Author:** Claude (agent), from a design discussion with the repository owner

**Status:** Draft

## Overview

Complete the missing middle of the promotion route so a numerical packing can be carried
to a certified algebraic characterization, and close the loop by carrying it back and
re-verifying it. Two halves are missing and they fail differently: the **symbolic** half
cannot turn a contact structure into a polynomial, and the **numeric** half cannot
produce a pose precise enough for the symbolic half to trust.

`n = 11` is the calibration, because every stage has a published answer to be caught
being wrong against.
`n = 29` is the target, because its best known construction is a numerical root-find
with no public certificate.

## Goals

- Assemble, close, refine, and solve the contact system for a pose whose contact
  structure is known, recovering `n = 11`’s published minimal polynomial independently.
- Close the round trip: substitute the recovered polynomial back exactly, re-verify the
  packing, and compare the reconstructed side against the input pose.
- Execute the same chain end to end at `n = 29`, where no published answer exists.
- Replace the float LP’s `1e-11` noise floor with an exact LP over certified rational or
  algebraic coefficients, so the chain can consume poses this project generates rather
  than only poses someone else published at high precision.

## Non-Goals

- **Any optimality claim.** Certifying an upper bound leaves the `n = 29` bound gap of
  about `0.46` untouched.
  A matching lower bound is separate mathematics.
- **Any record improvement.** This certifies an existing construction; it does not
  search for a better one.
  That is the proposer layer, where H-002, H-016, H-018 and H-020 are all refuted.
- **Generic contact inference from arbitrary serialized geometry.** Where near-contacts
  are ambiguous, that must remain an explicit typed failure.
- **Resolving component identity.** `distinct_basins` counting endpoint keys is a real
  blocker for the atlas, but it is independent of this feature and neither unblocks the
  other.

## Background

The six-step route from a float vector to a certified algebraic number is set out in
[TUTORIAL §5](../../../../TUTORIAL.md#from-a-numeric-solution-to-an-exact-one).
Step one and step six are built and sound.
Steps two through five are the gap.

Two things were corrected by measurement during planning, and both changed the design.

**Contact inference is not the blocker at `n = 29`.** It was first ranked first, on an
ambiguity risk imported from D-021’s `1e-11` float-LP floor.
That floor governs this project’s quench output, not a source carrying roughly
ninety-nine digits per coordinate.
The retained reconstruction separates contact from non-contact by about ninety-nine
orders of magnitude — worst touching margin `-4.05e-101` against smallest strict
separation `3.617e-02`, over 406 pairs — and the structure is already computed: 52 pair
contacts and 37 container contacts, 89 incidences.

**The serialized digits are not enough, but the system is already public.** Running
integer relation directly on the serialized side value returns relations at almost every
degree from eight to twenty-one, which is the signature of an under-determined search.
The degree-eight candidate has a relative residual of order `1e-90` against roughly a
hundred available digits, having consumed almost exactly the ninety it was permitted.
That first probe’s parameters were not recorded and it is not reproducible as written;
X-004 carries a fully parameterized replacement, which finds no relation at all through
degree sixteen at 700 digits.
Ninety-eight digits cannot identify the minimal polynomial, so precision has to be
manufactured from the closed system rather than read from the source.

That system, at `n = 29`, is published rather than pending: the provenance SVG carries
nine slide scalars and six equations in `{s, a, b, c, d, i}`, and
[`cases.kingbird29.verify_svg`](../../../../packing/cases/kingbird29/verify_svg.py)
already transcribes them for a residual check.
Solving that same transcription reaches 420 digits in about two seconds.
The assembler below is therefore about generalizing to sizes with no published system,
not about unblocking this one.
All three measurements are recorded in
[X-004](../../../../packing/campaign/explorations/X-004-n29-exact-promotion.md).

That is why the D-021 floor matters even though `n = 29` does not need it.
On a published high-precision pose the contact structure is unambiguous.
On a pose this project quenches, the floor is exactly the ambiguity that makes step two
a guess.

## Design

### Approach

Build the chain against the back end that already exists, so each new stage has
something that can catch it being wrong.
`sqpack.field` proves irreducibility and isolates a real root; `sqpack.verify` checks
separating-axis validity with exact predicates.

The chain is strictly ordered, and the ordering is forced rather than chosen: the solve
needs precision, precision needs refinement, refinement needs a closed system.

```
contact structure -> closed system -> refined solution -> minimal polynomial -> certificate
     (measured)        (unbuilt)        (unbuilt)           (unbuilt)            (built)
```

The numeric half is parallel to that chain, not upstream of it.
It does not gate the `n = 29` result; it gates whether the chain generalizes past
published sources.

### Components

| Component | State | Role |
| --- | --- | --- |
| Contact-structure artifact | measured, not retained | Freeze the 89 incidences and their separation as a durable record |
| Contact-system assembler | unbuilt | Equations from incidences; eliminate centres; close with Jacobian-determinant conditions |
| High-precision refiner | unbuilt | Newton from the closed system, seeded by the serialized pose |
| Exact solver | unbuilt; libraries present | Elimination, or integer relation with real margin |
| Exact LP | unbuilt | Removes the `1e-11` floor so this project’s own poses become promotable |
| `sqpack.field`, `sqpack.verify` | built and sound | Discharge the two guesses |

SymPy carries `groebner` and `resultant`, and mpmath carries `pslq`. Unbuilt here means
no code in this repository, which is not the same as no capability.

### API Changes

New devtools modules and one CLI surface; no change to `Witness/v2` or to the existing
verification API. A promoted result must enter the record through the same witness and
evidence contracts as any other certificate, so that assurance, method, precision and
novelty are recorded rather than asserted in prose.

## Implementation Plan

### Phase 1: The chain, calibrated then executed

- [ ] Freeze the `n = 29` contact structure as a retained artifact, and reproduce the
  known `n = 11` structure with the same extraction.
- [ ] Assemble the contact equations, eliminate centres, and close the system with
  Jacobian-determinant conditions; reproduce the known `n = 11` form.
- [ ] Refine to a declared precision well past the source, reporting a residual bound
  rather than assuming one.
- [ ] Recover a minimal polynomial by elimination or integer relation, with margin that
  the residual demonstrates rather than the tolerance permits.
- [ ] Close the round trip at `n = 11`: substitute back exactly, re-verify the packing,
  and compare the reconstructed side against the input.
- [ ] Run the same chain at `n = 29` and record whatever it returns, including a typed
  refusal.

### Phase 2: Remove the numeric floor

- [ ] Exact LP over certified rational or algebraic coefficients, replacing the float
  solver where a certified answer is required.
- [ ] Demonstrate that a pose quenched through the exact path has an unambiguous contact
  structure, which is the property the float path cannot supply.

## Testing Strategy

The calibration is the test.
At `n = 11` every stage has a published answer, so each is checked against something no
implementation can influence: the extraction against the known contact structure, the
assembly against the known system, the solve against Trump’s degree-eight polynomial,
and the round trip against `cases.trump11.packing`.

Two failure modes need different checks, and one is only partly covered.

- A **wrong minimal polynomial** is caught by exact back-substitution: it will not
  satisfy the system.
- A **wrong contact structure** is caught by re-verifying the reconstructed packing, but
  verification catches infeasibility and not a structure that yields a valid yet
  *suboptimal* packing.
  That failure appears as a reconstructed side strictly above the input pose, so the
  comparison must be against the input side and not merely against validity.

Every stage that can refuse must have a control proving it refuses, in the same style as
the existing negative controls.
A stage that cannot fail has not been tested.

## Rollout Plan

Each stage lands with its checks and its controls, behind the existing gate.
Nothing enters `frontier/` from this work without passing the witness and evidence
contracts, and a promoted `n = 29` certificate is a deliberate, reviewed change rather
than a search result written into the record.

An unattended runner may not accept a scientific verdict from this chain; that rule is
unchanged and applies here as it did to exp-045.

## Open Questions

- What is the degree of `s(29)`'s minimal polynomial?
  Unknown, and it decides whether integer relation is viable and at what precision.
  The probe bounds only what ninety-eight digits can reach, not the true degree.
- Does elimination terminate at six unknowns?
  `n = 11` reduces to two and `n = 17` to three; Gröbner cost is severe in variable
  count. Integer relation is a parallel candidate rather than a fallback for this reason.
- Do the five tilted orientation classes correspond to fewer exact algebraic relations,
  lowering the effective unknown count below six?
- Is the exact LP purely rational for the cells that matter, or does it need algebraic
  coefficients? SYNOPSIS notes it is rational only for rational-coefficient cells.

## References

- [X-004 — an exact algebraic characterization of the `n = 29` record](../../../../packing/campaign/explorations/X-004-n29-exact-promotion.md)
- [plan-2026-08-28 — the symbolic promotion gap](plan-2026-08-28-symbolic-promotion-and-the-atlas.md)
- [agenda-005](../../../../packing/campaign/agendas/agenda-005-symbolic-promotion-and-identity.md)
- [TUTORIAL §5 — from a numeric solution to an exact one](../../../../TUTORIAL.md#from-a-numeric-solution-to-an-exact-one)
- [SYNOPSIS — What Is Built](../../../../SYNOPSIS.md#what-is-built)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
