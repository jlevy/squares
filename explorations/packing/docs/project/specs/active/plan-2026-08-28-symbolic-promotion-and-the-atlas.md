# Plan: The Symbolic Promotion Gap, and What a Complete Atlas Would Need

**Date:** 2026-08-28

**Owns:** The top-down capability reading that decides which symbolic work is reachable
now, why `n = 11` is exact and `n = 29` is not, and the ranked gaps between the current
tooling and a complete atlas.

**Does not own:** The bounded commitments, which live in
[agenda-005](../../../../campaign/agendas/agenda-005-symbolic-promotion-and-identity.md);
the scientific claims, which live in the hypothesis registry; or the component-status
vocabulary, which [SYNOPSIS’s What Is Built](../../../../SYNOPSIS.md#what-is-built) owns
and this plan only reads.

## Objective

Decide what a symbolic survey can actually attempt with the tooling that exists, and
name the specific missing pieces rather than the general ambition.
The conclusion is that the front and back of the promotion pipeline are built and the
middle is not, so every exact entry in the atlas today was either derived by hand or
supplied by the literature.

## The reading, in one table

The six-step route from a float vector to a certified algebraic number is set out in
[TUTORIAL §5](../../../../TUTORIAL.md#from-a-numeric-solution-to-an-exact-one).
Against what is implemented:

| Step | State |
| --- | --- |
| 1. Numeric solve: propose, then quench | **built**; the proposer is the measured bottleneck |
| 2. Read off the contact structure | **unbuilt** — the project does not generically infer corner–edge incidences |
| 3. Write and reduce the contact equations | **unbuilt** |
| 4. Close the underdetermined system by Jacobian or Fritz-John conditions | **unbuilt** |
| 5. Solve exactly by elimination or integer relation | **unbuilt** — no Gröbner, resultant, PSLQ or LLL code exists |
| 6. Certify | **half built** — irreducibility and root isolation exist; interval-Newton, Krawczyk and the `PoseBox` scalar do not |

Steps two through five are the whole middle of the pipeline.
What exists is a search front end and an exact-arithmetic back end with no bridge
between them. SymPy appears in three files and none of them is a general promoter.

## Why `n = 11` is exact and `n = 29` is not

This difference is not about difficulty, and reading it as difficulty would misdirect
the next several sessions.

[`cases.trump11.derive_field`](../../../../cases/trump11/derive_field.py) states its
input plainly: it takes **only the published minimal polynomial** of the container side,
plus the tilted-block contact relation, and re-derives the minimal polynomial of
`u = tan(a/2)`. `n = 11` is exact because Trump published the degree-eight polynomial in
1979\. Steps two through five were carried out by a person, decades ago, and this
repository picks the work up at step six, where it is strong.

`n = 29` has no such publication, and the record is explicit that none exists anywhere.
`E-n029-kingbird-report` carries `replay_status: public-certificate-missing` with the
limitation that “the public SVG serializes a FindRoot result and supplies no formal
certificate”, and the blocker “no outward-rounded interval or exact algebraic
certificate is public”.
The repository’s own reconstruction reaches `numerically-checked` at 160 decimal digits
and tolerance `1e-80`, and stops there by design.

So the best known `n = 29` construction is a numerical root-find, and **no exact
constructive value for it exists in the literature or here**.

The contrast with `n = 5` and `n = 10` is the useful one, because those come from the
same catalogue yet reach `verified` and `exact-algebraic` in
[`cases.gobel5`](../../../../cases/gobel5/) and
[`cases.gobel10`](../../../../cases/gobel10/). The difference is that Göbel’s underlying
constructions are known in closed form.
At `n = 29` the construction *is* the numerical solve.

This changes what the symbolic pipeline would be doing at each size.
At `n = 11` it would reproduce a result published in 1979, which is a calibration with a
known answer. At `n = 29` it would produce a characterization **nobody has**, with no
published answer to check against — so step six stops being a formality and becomes the
entire guarantee.

It also means the `5.23e-5` reported-value gap cannot be closed by better sourcing.
There is no certificate to find; there is only one to derive.

## The number that should govern priorities

|  | verified minus reported | reading |
| --- | ---: | --- |
| `n = 11` | `4.18e-15` | the verified bound **is** the record |
| `n = 29` | `5.23e-05` | the verified bound is **weaker** than the record |

`n = 29`’s `reported_upper_bound` is Kingbird’s, a better construction than the Schadt
pose the repository can certify.
The certified bound sits about `5.23e-5` above the actual record, and that record is not
verified here at all.

Session 032 tightened the Schadt relaxation from `4.93e-11` to `4.93e-31`, a factor of
`1e20`. **The distance to the real record, `5.23e-5`, is about `1e6` times that entire
improvement** — and about `1e26` times the `4.93e-31` that remains.
An earlier draft of this line quoted the second ratio against the first quantity.
Either reading gives the same verdict: the tightening was correct, cheap, and irrelevant
to the frontier; it moved a quantity that does not bear on closing the gap.
Recording that here so the next session prices the two kinds of work differently.

## Two programs, not one

A complete atlas needs both, and they are independent.

**Exact entries** need steps two through five, plus the missing half of step six.
This is the symbolic survey proper, and `n = 29` is its natural first hard target
because a numerical pose already exists and the failure is purely one of promotion.

**A map that means something** needs the component-identity blocker resolved.
`distinct_basins` counts endpoint keys rather than connected terminal components, the
exact `n = 3` sliding family shows one connected optimal set producing many keys, and
until that is fixed the census cannot saturate and the rarity premise is untestable
rather than untested.

Neither program unblocks the other.
A perfect exact promoter would still leave the map counting keys; a resolved identity
relation would still leave `n = 29` uncertified.

## Ranked gaps

1. **Precision manufactured from the system.** Corrected by measurement after this plan
   was first written. Contact-structure inference was ranked first here on an ambiguity
   risk that does not apply at `n = 29`: the retained reconstruction separates contact
   from non-contact by about ninety-nine orders of magnitude, and the structure is
   already computed. The real first blocker is that the source carries about ninety-eight
   digits, which a probe in X-004 shows cannot identify a minimal polynomial.
   More digits require Newton refinement, and refinement requires the closed system —
   which at `n = 29` is published in the provenance SVG and already transcribed in
   [`cases.kingbird29.verify_svg`](../../../../cases/kingbird29/verify_svg.py), where it
   is evaluated but never solved.
   Precision at this size is available today; gaps 2 and 3 below are what generalize the
   route to sizes with no published system.
2. **Contact-equation assembly and closure**, including the determinant conditions that
   keep the problem root-finding rather than minimization.
   Root-finding reaches the precision step five needs; minimization does not.
3. **Exact solve.** Elimination or high-precision Newton followed by integer relation.
4. **Certified numerics.** Interval-Newton or Krawczyk, to discharge existence and
   uniqueness near a candidate root.
5. **Component identity.** Blocks the map half specifically, and nothing else.

## The two guesses this pipeline would introduce

Building steps two through five creates two new ways to be confidently wrong, and both
are already documented rather than hypothetical.

- **The contact structure is a guess.** Step two decides that a residual separation at
  the solver floor, `1e-11` and below, is exactly zero.
  It might not be, and nothing in steps three through five rechecks it.
- **The minimal polynomial is a guess.** Integer relation finds a relation, not a proof.
  A degree-eight relation holding to five hundred digits is overwhelming evidence and no
  proof at all.

This is why step six is not optional and why a promoter that skips it would produce
exactly the shape of the flattering soundness defects this repository already logs.

## What this plan does not authorize

- No claim that a promoted pose certifies a reported value until the claim is discharged
  — either by exact substitution into the recovered field, which is the stronger route
  and the pipeline’s own success path, or by interval certification where only a
  numerical enclosure is available.
- No treatment of the `4.93e-31` relaxation as progress toward the `n = 29` record.
- No atlas saturation, census completeness, or rarity claim while `distinct_basins`
  counts keys.
- No inference of a contact model from serialized geometry where near-contacts are
  ambiguous; that must remain an explicit typed failure.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
