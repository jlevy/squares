---
title: X-004 — an exact algebraic characterization of the n = 29 record
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-004
  title: An exact algebraic characterization of the n = 29 record
  date: '2026-08-28'
  author: Claude (agent), from a design discussion with the repository owner
  campaign: packing.squares
  brief: >-
    Record a 2026-08-28 discussion that measured how far the repository actually is from
    an exact characterization of the best known n = 29 packing, and corrected a claim made
    earlier in the same discussion. The contact structure at n = 29 is already computed
    and unambiguous, so the blocker is not inference but the reduction and solve at seven
    unknowns. Mines candidate hypotheses for that program and states what such a result
    would and would not be.
  sources:
  - SYNOPSIS.md
  - TUTORIAL.md
  - cases/kingbird29/verify_svg.py
  - cases/trump11/derive_field.py
  - frontier/evidence.yaml
  - frontier/n-029.md
  - resources/papers/kingbird-square-29-provenance.svg
  - campaign/series/series-000-smoke-and-calibration/experiments/exp-037-h-042-n29-numerical-angle-classes.md
---
# X-004 — An Exact Algebraic Characterization of the `n = 29` Record

This report records a design discussion and its measurements.
It spends no experiment budget and asserts no scientific verdict.
Its purpose is to state, with numbers, how far the repository is from an exact `n = 29`
characterization — and to correct a claim made earlier in the same discussion, because
the correction is the most useful thing in it.

## What the best known `n = 29` packing actually is

A numerical root-find, serialized.
[`E-n029-kingbird-report`](../../frontier/evidence.yaml) carries
`replay_status: public-certificate-missing`, the limitation that “the public SVG
serializes a FindRoot result and supplies no formal certificate”, and the blocker “no
outward-rounded interval or exact algebraic certificate is public”.

So **no exact constructive value for `n = 29` exists in the literature or here.** The
contrast with `n = 5` and `n = 10` is the instructive one: those come from the same
catalogue yet reach `verified` and `exact-algebraic`, because Göbel’s constructions are
known in closed form.
At `n = 29` the construction *is* the numerical solve.

`n = 11` is exact for the same kind of reason and not by any capability of this
repository’s pipeline.
[`cases.trump11.derive_field`](../../cases/trump11/derive_field.py) takes “only the
published minimal polynomial” and re-derives `u = tan(a/2)` from it.
Trump did steps two through five by hand in 1979; this repository picks the work up at
step six, where it is strong.

## The correction

Earlier in this discussion the agent asserted that contact-structure inference was “the
single thing standing between exact at `n = 11` and exact at `n = 29`”, and scoped a
commitment around calibrating that inference.

That was wrong, and the measurement says so plainly.
Running the retained reconstruction:

| Quantity | Value |
| --- | ---: |
| Pairs tested | 406 |
| Touching pairs within tolerance | 52 |
| Strict, separated pairs | 354 |
| Container contacts | 37 |
| Worst touching margin | `-4.05e-101` |
| Smallest strict pair separation | `3.617e-02` |

**The gap between “in contact” and “not in contact” is about ninety-nine orders of
magnitude.** There is no ambiguity to resolve, and the contact structure — 89 incidences
in total — is already computed today.

The error was applying the wrong instrument’s error budget.
The ambiguity concern came from [D-021](../../defects.md), the roughly `1e-11` noise
floor of *this project’s float LP solver*. The Kingbird SVG is not that solver’s output;
it carries roughly ninety-nine decimal digits per coordinate.
A floor that governs a quench endpoint says nothing about a published high-precision
serialization.

## What is therefore left

For this one case, with its contact graph in hand:

| Step | State at `n = 29` |
| --- | --- |
| 2. Contact structure | **done**, 89 unambiguous incidences |
| 3. Assemble and reduce the equations | real work, mechanical from a known graph |
| 4. Close by determinant conditions | real work |
| 5. Solve exactly | **libraries exist and are unused** — SymPy carries `groebner` and `resultant`, mpmath carries `pslq` |
| 6. Certify | **built and sound** |

“Unbuilt” in the synopsis means no code in this repository, which is not the same as no
capability. For a single case whose contact graph is known, the distance is considerably
shorter than a generic pipeline would suggest.

## The risk that remains is scale, not ambiguity

Fifteen of the twenty-nine squares are axis-aligned, and the reconstruction measures six
orientation classes with a minimum class gap of `0.296` degrees — the count that refuted
[H-042](../hypotheses/H-042-n29-numerical-angle-classes.md)’s three-class claim.

After eliminating centres the system carries roughly `s` plus six angles, so about seven
unknowns, against two at `n = 11` and three at `n = 17`. Gröbner basis cost is severe in
the number of variables, so elimination may not terminate at seven.

The integer-relation route avoids elimination entirely: it recognises a minimal
polynomial from digits.
With roughly ninety-nine digits already serialized, and more obtainable by
high-precision Newton from the same contact system, that route has unusually good
material. It is a parallel candidate rather than a fallback.

## A two-minute probe that bounds the shortcut

The obvious shortcut is to skip the system entirely and run integer relation directly on
the serialized side value.
That was tried during this discussion, as orientation and not as a registered round, and
it fails informatively.

`mpmath.pslq` over `s^0 .. s^d` returns relations at almost every degree from eight to
twenty-one. That pattern is the signature of an under-determined search rather than of
structure: the coefficient budget, not the mathematics, decides where relations appear.

The degree-eight candidate was then checked directly.
Its relative residual is `1.26e-90` against roughly ninety-eight available digits — it
consumed almost exactly the `(8 + 1) x 10 = 90` digits the search was allowed and
stopped there.
A genuine minimal polynomial would vanish to the full input precision, not
to the precision the search was permitted to spend.

**So ninety-eight digits cannot identify the minimal polynomial**, and the serialized
value alone will not yield one however it is processed.

That is a bound on the shortcut and not on the problem, and it forces the order of work:

- more digits require Newton refinement,
- refinement requires the contact *system*, not merely the contact *structure*,
- assembling that system is steps three and four.

The infrastructure is therefore on the critical path rather than beside it.
There is no route to step five that avoids steps three and four, which is worth knowing
before any budget is spent looking for one.

## Validation runs both directions, and the reverse half is already sound

The reverse direction is what makes the forward one worth attempting.
`sqpack.field` proves irreducibility and isolates the real root; `sqpack.verify` checks
separating-axis validity with exact predicates.
A derivation would be built against a back end that can catch it being wrong.

The two guesses are discharged differently, and one of them only partly:

- **A wrong minimal polynomial** is caught by exact back-substitution: it will not
  satisfy the system.
- **A wrong contact structure** is caught by re-verifying the reconstructed packing —
  but verification catches *infeasibility*, not a structure that yields a valid yet
  suboptimal packing. That failure appears as a reconstructed side strictly above the
  input pose, so the round trip must compare against the input side and not merely
  against validity.

At `n = 11` the loop closes against a value nobody can fudge: published polynomial,
independent derivation, exact back-substitution, comparison against
`cases.trump11.packing`.

## What such a result would and would not be

It would be a **certification, not an improvement**. Deriving the algebraic form proves
the already-claimed side is achievable; it does not produce a smaller square.
What moves is this repository’s own verified bound, from the Schadt-derived
`5.93388579981302587863645209` to Kingbird’s `5.93383346267692`, closing a gap of about
`5.23e-5`.

Beating the record is a different program in a different layer — the proposer lane,
where H-002, H-016, H-018 and H-020 are all refuted and the annealer demonstrably does
not reach records.

It would appear novel, with the repository’s standing qualification.
The blocker text says no public certificate exists, so a derived one would be new
relative to the reviewed sources.
That is `apparently-novel` rather than `novel`, because the archive README records that
a “not retrievable” verdict is a negative search result and that this archive “has now
been wrong about it eight times”.

It would say **nothing about optimality**. The verified lower bound at `n = 29` is
`5.472135955` from [`E-basic-area-lower`](../../frontier/evidence.yaml), which “uses
only area and is weaker than the recorded theorem for most cases”.
Against an upper bound near `5.9339` that leaves a bound gap of about `0.46`. Certifying
the upper bound does not narrow it.

## Candidate hypotheses, unregistered

Stated here as mineable candidates only.
None is registered, none has a criterion frozen, and none may be run from this document.

1. The `n = 29` contact system, closed by determinant conditions, admits elimination to
   a univariate minimal polynomial for `s` within a declared time and memory budget.
2. Integer relation on the serialized side value recovers a minimal polynomial whose
   degree is at most some declared `D`, and that polynomial survives irreducibility,
   root isolation, and exact back-substitution.
3. The six numerically observed orientation classes correspond to at most some smaller
   number of exact algebraic angle relations, so the effective unknown count is below
   seven.
4. The reconstructed side from an accepted contact structure equals the input pose’s
   side to within the serialization precision, which is the round-trip criterion that
   distinguishes a correct contact structure from a valid but suboptimal one.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
