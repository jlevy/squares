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
    and unambiguous, and the source publishes the closed system outright, so the blocker at
    this size is neither inference nor assembly but the exact solve at six unknowns. Mines candidate hypotheses for that program and states what such a result
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

## The first correction

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
| 3. Assemble and reduce the equations | **published by the source and already transcribed** — see the second correction below |
| 4. Close by determinant conditions | **published by the source and already transcribed** |
| 5. Solve exactly | **libraries exist and are unused** — SymPy carries `groebner` and `resultant`, mpmath carries `pslq` |
| 6. Certify | **half built** — irreducibility, root isolation and exact predicates exist; interval-Newton, Krawczyk and the `PoseBox` scalar do not |

“Unbuilt” in the synopsis means no code in this repository, which is not the same as no
capability. For a single case whose contact graph is known, the distance is considerably
shorter than a generic pipeline would suggest.

## The risk that remains is scale, not ambiguity

Fifteen of the twenty-nine squares are axis-aligned, and the reconstruction measures six
orientation classes with a minimum class gap of `0.296` degrees — the count that refuted
[H-042](../hypotheses/H-042-n29-numerical-angle-classes.md)’s three-class claim.

The six orientation classes **include** the axis class, which holds fifteen squares at
zero degrees, so there are five tilted classes.
After eliminating centres the system carries `s` plus those five angles: **six
unknowns**, against two at `n = 11` and three at `n = 17`. The source settles this
rather than leaving it an estimate — its own solve is a six-by-six system in
`{s, a, b, c, d, i}`. Gröbner basis cost is severe in the number of variables, so
elimination may still not terminate at six.

The integer-relation route avoids elimination entirely: it recognises a minimal
polynomial from digits.
With roughly ninety-nine digits already serialized, and more obtainable by
high-precision Newton from the same contact system, that route has unusually good
material. It is a parallel candidate rather than a fallback.

## The second correction, and the larger one

A first draft of this exploration closed the section below with the assertion that
**“there is no route to step five that avoids steps three and four”**, and concluded
that building the assembly infrastructure was therefore on the critical path for
`n = 29`.

That is false, and the artifact refuting it was already in this repository and is listed
in this document’s own `sources`.

The archived provenance SVG does not merely serialize a `FindRoot` result.
It publishes the **entire closed system**: nine slide scalars
`r1, r2, r3, r4, r5, r8, rB, rC, rD`, each given in closed form, and six equations
`f1 … f6` in the six unknowns `{s, a, b, c, d, i}`, followed by the `FindRoot` call over
them at `WorkingPrecision -> 200`. Its header credits David Ellsworth with an *exact
analytic solution* on 2025-12-10, and [`frontier/n-029.md`](../../frontier/n-029.md)
already records that phrase.

Steps three and four at `n = 29` were therefore never unbuilt work.
They were done by the source and published.

Worse for the original claim,
[`cases.kingbird29.verify_svg`](../../cases/kingbird29/verify_svg.py) had **already
transcribed all six equations and all nine slide scalars into this repository**. It uses
them only to evaluate residuals at the serialized pose, as a consistency check on the
serialization — it never solves them.
The distance between what existed and what was said to be missing was the difference
between evaluating that system and passing it to a root finder.

Re-solving the transcribed system directly confirms this:

| Quantity | Value |
| --- | --- |
| `s` at 60 digits | `5.93383346267692918968946061635201913843383418107788697463883` |
| Agreement with the reported record `5.93383346267692` | all 15 published digits |
| Max equation residual at 420 digits | `8.85e-421` |
| Wall-clock for a 420-digit solve | about 2 seconds |

Precision at `n = 29` is not a thing to be manufactured by new infrastructure.
It is available now, to any depth, from a system this repository transcribed months ago.

### The two halves of the source agree

The solve can be checked against something it cannot influence.
`verify_svg` derives the orientation classes from the SVG’s parsed `<use>` transforms —
the packing’s *geometry* — while `f1 … f6` are the packing’s *equations*. The two are
independent readings of the same source, and this repository had only ever run the
first.

| Unknown | Solved from the equations | Measured from the geometry | Class size |
| --- | --- | --- | ---: |
| — | (axis class) | `0.0` | 15 |
| `a` | `25.2586553084` | `25.2586553083514058513567614369` | 1 |
| `b` | `20.8001267627` | `20.8001267626996105663146232033` | 9 |
| `c` | `17.5062684757` | `-17.5062684757323675007868691576` | 1 |
| `d` | `24.9625879894` | `24.9625879894377186810714309248` | 2 |
| `i` | `24.3083584013` | `24.3083584013469067264676340473` | 1 |

They agree to every digit compared, and the class sizes total
`15 + 1 + 9 + 1 + 2 + 1 = 29`. The sign on `c` is the layout’s, not a discrepancy: the
class is recorded in the canonical `[-45, 45)` interval while the equations carry the
unsigned angle.

This also settles the unknown count by direct observation rather than by argument.
Six orientation classes, one of them the axis class, leave five tilted angles; with `s`
that is six unknowns, matching the source’s own six-by-six solve.

The measurement in the next section stands unchanged; only the inference drawn from it
was wrong.
Ninety-eight digits genuinely cannot identify the minimal polynomial — but the
remedy is to run the system that is already here, not to build the machinery that would
have produced it.

## A two-minute probe, and the inference that was drawn from it wrongly

The obvious shortcut is to skip the system entirely and run integer relation directly on
the serialized side value.
That was tried during this discussion, as orientation and not as a registered round, and
it fails informatively.

`mpmath.pslq` over `s^0 .. s^d` returns relations at almost every degree from eight to
twenty-one. That pattern is the signature of an under-determined search rather than of
structure: the coefficient budget, not the mathematics, decides where relations appear.

The degree-eight candidate was then checked directly, and its relative residual came out
around `1e-90` against roughly ninety-eight available digits — consuming almost exactly
the `(8 + 1) x 10 = 90` digits the search was allowed and stopping there.
A genuine minimal polynomial would vanish to the full input precision, not to the
precision the search was permitted to spend.

**The parameters of that first probe were not recorded, and it is therefore not
reproducible as originally written.** A reviewer re-running the same shape obtained
`1.19e-85` at `dps = 100` and `4.54e-84` at `dps = 98` rather than the figure first
noted, and the “ninety-eight digits” was never derived — the serialized side carries
exactly one hundred significant digits.
The order of magnitude and the qualitative reading survive; the specific figure does
not, and it is recorded here as approximate for that reason.

A reproducible replacement is recorded below with full parameters.

### The probe, restated reproducibly

Run against the system solved directly, rather than against the serialized digits:

| Parameter | Value |
| --- | --- |
| Source of `s` | the transcribed `f1 … f6` system, solved by `mpmath.findroot` |
| Ground-truth precision | `mp.dps = 1200`, max equation residual `1.11e-1200` |
| Search precision | `mp.dps = 700` |
| Basis | `s^0 … s^d` |
| `tol` | `1e-675`, that is `10^-(search - 25)` |
| `maxcoeff` | `10^22` |
| `maxsteps` | `50000` |
| Degrees swept | `2 … 20`, sweep complete |

At these parameters **no relation is returned at any degree from two through twenty** —
against the original probe’s relations at nearly every degree from eight to twenty-one.
That contrast is the cleanest available confirmation that the original relations were
artifacts of insufficient precision rather than structure, and it is the measurement the
margin rule in the implementation spec is written to enforce.

What this negative result bounds, stated exactly: there is **no integer relation among
`s^0 … s^d` for `d ≤ 20` whose coefficients are smaller than `10^22`**, given a value
carrying 700 reliable digits.
It does not bound the degree on its own, because degree and coefficient size trade off —
a degree-20 minimal polynomial with coefficients near `10^30` would need roughly
`21 x 30 = 630` digits and would sit inside this budget, but one with coefficients near
`10^40` would not. Pushing further is cheap in principle and expensive in practice: cost
grew from `0.3s` at degree four to `339s` at degree twenty, roughly a factor of `1.4`
per degree, so degree thirty at these settings is hours rather than minutes.
The useful conclusion is negative and bounded, and it is recorded that way.

That is a bound on the shortcut and not on the problem, and the first two links of the
chain it implies are sound:

- more digits require Newton refinement,
- refinement requires the contact *system*, not merely the contact *structure*.

The third link is where the first draft went wrong.
It concluded that assembling that system was steps three and four, and so put the
infrastructure on the critical path.
At `n = 29` the system does not have to be assembled, because the source published it
and this repository transcribed it.
The infrastructure is needed to *generalize* the route to sizes with no published system
— which is a real and separate reason to build it — but it does not gate this case.

## Validation runs both directions, and the reverse half is already sound

The reverse direction is what makes the forward one worth attempting.
`sqpack.field` proves irreducibility and isolates the real root; `sqpack.verify` checks
separating-axis validity with exact predicates.
A derivation would be built against a back end that can catch it being wrong.
That back end is sound for the route this exploration needs — exact substitution into
the recovered field — and it is the *other* half of step six, interval-Newton and
Krawczyk, that is absent; see the
[atlas plan](../../docs/project/specs/active/plan-2026-08-28-symbolic-promotion-and-the-atlas.md)
for the component-by-component reading.

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
`5.472135955` from [`E-nagamochi-lower`](../../frontier/evidence.yaml) — Theorem 2 of
[Nagamochi 2005], recorded in exact form as `sqrt(29 - 2*floor(sqrt(29)) + 1) + 1`, that
is `sqrt(20) + 1`. It is a published proof and strictly stronger than the area bound,
which would give only `sqrt(29)` — about `5.385`. Against an upper bound near `5.9339`
that leaves a bound gap of about `0.46`. Certifying the upper bound does not narrow it.

## Candidate hypotheses, unregistered

Stated here as mineable candidates only.
None is registered, none has a criterion frozen, and none may be run from this document.

1. The `n = 29` contact system, closed by determinant conditions, admits elimination to
   a univariate minimal polynomial for `s` within a declared time and memory budget.
2. Integer relation on the serialized side value recovers a minimal polynomial whose
   degree is at most some declared `D`, and that polynomial survives irreducibility,
   root isolation, and exact back-substitution.
3. The five tilted orientation classes correspond to at most some smaller number of
   exact algebraic angle relations, so the effective unknown count is below six.
4. The reconstructed side from an accepted contact structure equals the input pose’s
   side to within the serialization precision, which is the round-trip criterion that
   distinguishes a correct contact structure from a valid but suboptimal one.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
