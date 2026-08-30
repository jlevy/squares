---
title: X-007 — the n = 5 optimum flexes in exactly one direction, and that direction curves shut
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-007
  title: The n = 5 optimum flexes in exactly one direction, and that direction curves shut
  date: '2026-08-30'
  author: Claude (agent), under BC-049 in agenda-005, run as phase 5 of session-045
  campaign: packing.squares
  brief: >-
    BC-049 asked whether the packings the source catalogue annotates "Rigid." are rigid on
    evidence of our own. At n = 5 the record carried two things and neither was an answer:
    a translation-escape screen that decides single-square translation and nothing else,
    and bc-063's numerical rank at the retained decimal witness, which declined its own
    promotion. This asks the question exactly, over Q(sqrt 2), for all five squares and all
    three degrees of freedom each. The cone of infinitesimal motions is exactly
    one-dimensional -- rotation of the middle square about its own centre -- with the other
    fourteen coordinates pinned by verified Farkas certificates. That one direction is then
    refused at second order by a verified non-negative self-stress. So the packing is
    second-order rigid, which is stronger than anything the record held and still weaker
    than local rigidity, and the report says exactly where the remaining gap is.
  sources:
  - packing/campaign/series/series-000-smoke-and-calibration/results/bc-049-n5-rigidity-certificates.json
  - packing/campaign/series/series-000-smoke-and-calibration/results/bc-063-n5-rigidity-evidence.json
  - packing/atlas/known-best/translation-escape-screen.json
  - packing/frontier/n-005.md
  - packing/frontier/evidence.yaml
  - packing/cases/gobel5/packing.py
  - defects.md
  proposes: []
---
# X-007 — The `n = 5` Optimum Flexes in Exactly One Direction, and That Direction Curves Shut

**Date:** 2026-08-30

**Status:** W6 research slice under `BC-049`, run as phase 5 of `session-045`. Delivers
the commitment’s **first** exit branch in substance and stops short of it in name: a
first-party certificate with a stated scope, where the scope is second-order rigidity
rather than local rigidity.

**Owns:** The argument.
`devtools/assess_n5_rigidity.py` owns the computation, `tests/test_n5_rigidity.py` pins
it, and the gate step `n=5 rigidity certificates still verify` replays it.

## What the Record Held, and Why Neither Half Was an Answer

Two objects addressed `n = 5` rigidity before this, and the interesting thing is that
both were correct and neither was sufficient.

The **translation-escape screen** finds that no square of the retained witness can be
translated at any tolerance screened.
Its own registered limitation says why that settles nothing: it exhibits single-square
axis translations only, so a miss rules out one motion family and is silent about
rotation and about anything coordinated.
[`evidence.yaml`](../../frontier/evidence.yaml) records this as sound in one direction
only, and the frontier record for `n = 5` correctly reads `undetermined`.

**`bc-063`** went further and got closer.
It measured a contact-Jacobian rank of 15 against 16 unknowns, identified the resulting
one-dimensional motion space as a rotation of the centre square, and found a
second-order obstruction along it with coefficient `-1/4`. Its own `claim_boundary` then
declined the promotion, in terms worth quoting because they were right:

> Both the rank and the walk are numerical, at the retained pose.
> …It is consistent with local rigidity and does not establish it.

Three things were missing, and each of them matters.

**The pose was wrong for the purpose.** The retained decimal witness puts the middle
square’s centre `2.4e-30` off the diagonal, which the escape screen itself records as a
`-6.9e-30` pair separation.
A rigidity certificate built on an infeasible configuration is worse than no
certificate: it certifies a packing that does not exist.
This work uses Göbel’s exact construction instead, where the side is `2 + sqrt(2)/2` and
every contact is decided by an exact sign in `Q(sqrt 2)`.

**A rank is not a certificate.** A numerical rank of 15 says a search found no sixteenth
independent row; it does not say no motion exists.
The difference is the difference between a failed search and a proof, and this
repository has recorded that confusion often enough to have a name for it.

**One sampled direction is not every direction.** `bc-063` walked the one direction it
had displayed and saw the gap turn back.
That is evidence about a curve, not about the whole tangent structure, and in particular
it says nothing about whether the other fourteen coordinates could conspire to rescue
the rotation.

## The Instrument

An **infinitesimal motion** assigns each square a velocity and an angular velocity so
that to first order no contact is violated.
Writing `a_j` for the gradient of the `j`-th contact gap, those motions are exactly the
polyhedral cone `{x : Ax >= 0}`, and the packing is infinitesimally rigid precisely when
that cone is the origin.

The pose has 20 active contacts — 16 corners on walls, 4 corners of corner squares on
edges of the middle square — against 15 variables, and the middle square touches no
wall. That last fact is worth checking rather than assuming: its extreme coordinate is
`s/2 + sqrt(2)/2 ≈ 2.06` inside a container of side `≈ 2.71`.

Two things make the computation exact rather than approximate.

Contacts are found by **exact sign**, not by tolerance.
A tight packing is one whose squares touch exactly; a tolerance test on it either
invents contacts or misses the ones holding it together, and either way the constraint
matrix describes a different packing.

Pinning is established by **Farkas certificates**, not by rank.
Non-negative row weights `w` with `w . A = e_k` prove `x_k >= 0` for every admissible
motion, since `x_k = w . (Ax)` is a non-negative combination of non-negative numbers;
the same for `-e_k` pins the coordinate to zero.
The weights are proposed by a linear program in floating point and then **re-checked in
the field**, which is what makes them evidence.
A proposal that survives exact verification is a proof; the search that produced it is
not.

One implementation detail is load-bearing.
The four pair rows have entries that are pure multiples of `sqrt 2`, because the middle
square’s edge normals are `(sqrt(2)/2)(±1, ±1)`, so rational weights cannot cancel them
against the rational wall rows.
Scaling each such row by `sqrt 2` — a positive constant, which leaves the cone unchanged
— makes every row rational and the certificates ordinary.
Written without that step, the search returns nothing at all, which is how it was first
written.

## First Order: One Free Direction, Fourteen Certificates

The cone is a **line**. Fourteen of the fifteen coordinates are pinned, each with a
verified certificate in both directions; none is left uncertified.
The fifteenth, the middle square’s rotation, is free — and free in the strong sense that
**no row mentions it at all**, which is a two-sided degree of freedom rather than the
weaker one-sided slack a single inequality would leave.

So the `n = 5` optimum is **not infinitesimally rigid**.

The reason is a coincidence of this packing’s geometry, and it is checkable in one line.
Each corner square’s inner corner rests at the **midpoint** of the middle square’s edge,
which is the foot of the perpendicular from that square’s centre.
The rotation enters a pair constraint only through `(p - c) . n_perp`, and at the foot
of the perpendicular `p - c` is parallel to `n`, so that term is identically zero.
Four contacts, four zeros, and a rotation nothing can see.

This already strictly dominates both prior objects.
It covers rotation, which the screen does not; it covers all five squares at once, which
the screen does not; it is exact, which `bc-063` is not; and it certifies rather than
observes, which neither is.

## Second Order: The Same Geometry, the Other Way Round

A nonzero first-order direction is not a motion.
The question is whether some feasible arc realizes it, and the next term decides.

For a twice-differentiable arc `x(t)` through the pose with `u = x'(0)` and
`y = x''(0)`,

```
g_j(t) = t (a_j . u) + (t^2 / 2) ( u . H_j . u + a_j . y ) + O(t^3).
```

Here the first-order term vanishes for every contact, so feasibility at second order
needs `A y >= -q` where `q_j := u . H_j . u`.

Along the rotation the curvature is immediate, and it is the same geometric fact seen
from the other side.
Turning the middle square rotates each edge **line** about the centre, which leaves the
line’s distance from that centre unchanged.
The resting corner sits at the point of the line nearest the centre.
Turning the line can therefore only bring it *nearer* to a fixed point at that distance,
never further — so the gap is exactly `(1/2) cos(t) - 1/2`, curving into the obstacle at
both signs of `t`. The computation confirms `q_j = -1/2` at each of the four pair
contacts and `0` at all sixteen wall contacts.

The remaining question is whether the other fourteen coordinates can absorb that, and it
is answered by Farkas again, in its affine form: `{y : A y >= -q}` is empty exactly when
some `w >= 0` has `w . A = 0` and `w . q < 0`. Such a `w` is a **self-stress** — a
non-negative combination of the constraint rows that cancels identically — and here one
exists, verified in the field:

| Contact | Weight |
| --- | ---: |
| square 1 corner 0 on the bottom wall | 1/2 |
| square 1 corner 2 on the right wall | 1/2 |
| square 1 corner 3 on square 4 edge 0 | 1/2 |
| square 2 corner 0 on the left wall | 1/2 |
| square 2 corner 1 on square 4 edge 2 | 1/2 |
| square 2 corner 2 on the top wall | 1/2 |

The certificate reads as the picture it describes.
Squares 1 and 2 sit at opposite corners; each is boxed by two walls behind it and the
middle square in front.
The rotation drives the middle square into both of them, and the walls have nowhere to
give. Because `q` is quadratic in the direction, `q(-u) = q(u)` and the same certificate
refuses the reverse turn; a line’s two ends are not two questions here.

So every first-order flex is obstructed at second order.
The `n = 5` optimum is **second-order rigid**.

There is an independent check on the coefficient, and it is worth naming because it
comes from an entirely different method.
`bc-063` walked this direction numerically and measured contact overlaps of `-2.5e-7`,
`-2.5e-9` and `-2.5e-11` at steps of `1e-3`, `1e-4` and `1e-5` — a hundredfold per
decade, so `-t^2/4`, symmetric in both signs.
The exact gap `(1/2) cos(t) - 1/2` expands to `-t^2/4 + O(t^4)`. A sampled walk at a
slightly infeasible decimal pose and an exact expansion at the true pose agree to the
digit, which is the kind of agreement worth having between two methods that share no
code.

## What This Establishes, and the One Step It Does Not

Established, exactly, at the exact fixed-side pose: the cone of infinitesimal motions is
the line spanned by the middle square’s rotation; the other fourteen coordinates are
pinned by verified certificates; along that line every pair gap has curvature `-1/2` and
every wall gap curvature `0`; and a verified self-stress admits no second-order
correction. Together: **no twice-differentiable feasible arc leaves this pose with a
nonzero derivative.**

Not established by the computation: **local rigidity itself.** An arc whose derivative
vanishes at the pose — one that starts off like `s^2` rather than like `s` — is excluded
by nothing above.

There is an argument that closes it, it is short, and it is worth writing down precisely
because the obvious version of it is wrong.

The **wrong** version, which was the first thing written here: the feasible set is
semi-algebraic, so a nontrivial motion yields an analytic arc, which reparametrizes to
have nonzero derivative, and the above applies.
The last clause is false.
Puiseux gives `gamma(s) = p + a_m s^m + …` with `a_m != 0`, and when `m >= 2` no
analytic — indeed no `C^2` — reparametrization makes the first derivative nonzero.
Substituting `sigma = s^m` does it, but `sigma^(1/m)` is not twice differentiable, so
the second-order analysis no longer applies to the thing being analysed.

The **correct** version needs no reparametrization at all; it runs the same argument
inductively on the arc’s own coefficients.
Suppose the pose is not isolated in the feasible set.
The set is semi-algebraic — near this pose the non-overlap condition reduces to exactly
these twenty polynomial inequalities in the centres and in `(cos θ, sin θ)`, because
every other separating axis is strictly separating here and stays so nearby — so the
curve selection lemma gives a semi-algebraic arc into it, and Puiseux gives
`gamma(s) = p + sum_{k >= m} a_k s^k` with `a_m != 0`. Then:

- The `s^m` coefficient of `g_j(gamma(s))` is `a_j . a_m`, so feasibility forces
  `a_j . a_m >= 0` for every `j`: `a_m` lies in the first-order cone, hence
  `a_m = lambda e_{w4}` with `lambda != 0`, and `A a_m = 0`.
- Inductively, for `m < k < 2m` the quadratic part has not started yet, so the `s^k`
  coefficient is `a_j . a_k` and the same argument puts every `a_k` in `ker A`.
- At `s^(2m)` the quadratic part contributes for the first time, and only through the
  pair `(m, m)`, so the coefficient is `a_j . a_{2m} + (lambda^2 / 2) q_j`. Feasibility
  needs `A a_{2m} >= -(lambda^2 / 2) q`, which is a positive rescaling of the very
  system the self-stress refutes: applying `w` gives
  `0 = w . A a_{2m} >= -(lambda^2/2) w . q > 0`.

So no such arc exists and the pose is isolated: the packing is locally rigid at fixed
side.

**That argument is not what this record claims**, and the distinction is deliberate.
Everything up to and including the self-stress is computed and verified in the field,
and `--check` replays it.
The induction above is prose: it rests on the curve selection lemma for semi-algebraic
sets and on the local reduction of non-overlap to these twenty inequalities, neither of
which any test here checks.
Promoting the frontier record on the strength of a paragraph is the shape of mistake
this repository keeps a defect log about, so the property stays `undetermined` and the
argument is offered for review rather than banked.

The related citation is worth getting right too.
Connelly and Whiteley prove that second-order rigidity implies rigidity, but they prove
it for *tensegrity frameworks* — constraints on pairwise squared distances — and these
are corner-on-line constraints, so the theorem does not apply as stated.
What transfers is the proof: smoothness, semi-algebraicity, curve selection, Taylor, the
Farkas alternative. Adapting an argument is not the same as invoking a theorem, and the
difference is exactly the kind that gets lost in a citation.

Also not established, and worth stating because it is easy to lose: everything here is
at **fixed side**. The container side is Göbel’s exact optimum and is a constant, not a
sixteenth variable. This is a statement about motion within the optimal container, not
about what happens as the container grows.

## What Moves in the Record, and What Deliberately Does Not

The frontier `rigidity` block for `n = 5` keeps `property: undetermined`, and everything
else about it changes.

The property stays because the schema’s vocabulary is
`[locally-rigid, semi-rigid, not-rigid, undetermined]` and this result is none of them:
the packing is not `not-rigid` (no motion has been exhibited), and it is not
`locally-rigid` (the last step is prose, per the section above).
`undetermined` is documented as *assessed and not settled*, which is exactly right —
what changed is the assessment behind it, not the verdict.

What changes is everything that says *why*. The block moves from
`assurance: numerically-checked` and `method: numerical-multiprecision` to `verified`
and `exact-algebraic`; its certificate moves from the translation-escape screen to this
work’s own record; and it cites a new first-party evidence id,
`E-n005-second-order-rigidity`, in place of the screen’s.

That last swap has a mechanical consequence worth naming, because it is the design
working as intended rather than a side effect.
`assess_frontier_rigidity` decides what it owns by evidence id: a record whose evidence
is not in its own owned set is left alone as belonging to a stronger argument.
So `n = 5` leaves the assessed bucket and joins `n = 11` there — four `undetermined`
records assessed rather than five, two left to a stronger argument rather than one.
A record can leave that bucket without its verdict moving at all, and this is what that
looks like.

Two things follow, and both are deliberate.

**[`D-354`](../../../defects.md) is untouched.** The catalogue’s bare “Rigid.”
stays in `reported_upper_bound.catalogue_rigid` and never becomes our finding.
The guard in `test_frontier_rigidity_assessment.py` that asserts `undetermined` for
`n = 5, 28, 40` stays green without being edited, and so does the one forbidding a
rigidity claim on screen-miss evidence.
That was the test this change was held to: a guard you have to weaken to land a result
is a guard that was telling you something.

**`n = 28` and `n = 40` are not covered.** They are in the same `undetermined` group and
this says nothing about them.
The pose used here is Göbel’s exact construction; neither of the others has an exact
construction retained, and building one is the cost of extending this.

## What This Costs to Extend

The instrument is general in shape and specific in inputs.
`assess_n5_rigidity.py` takes a pose in `Q(sqrt 2)` and does the rest — contact
enumeration, linearization, first-order certificates, second-order terms, self-stress —
without knowing anything about `n = 5` in particular.

What does not generalize is the pose.
The argument needs an **exact** configuration, and the retained witnesses are decimals
that are infeasible at the scale a certificate works at.
For `n = 28` and `n = 40` that means the work is not “run the tool”; it is “produce an
exact construction first”, and that is the real price.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
