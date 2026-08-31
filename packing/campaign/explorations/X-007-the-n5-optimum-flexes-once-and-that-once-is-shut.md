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

    Extended on the same day to n = 40, which is where the instrument was found to carry
    three assumptions that n = 5 cannot distinguish from theorems: rational Farkas weights
    against mixed rows (D-388), corner incidences read as contacts (D-390), and a
    disjunctive tangent cone intersected (D-391). With all three corrected, n = 40 is
    infinitesimally FLEXIBLE -- its sixteen tilted squares turn together -- and seven such
    directions are now retained, each refused at second order by its own verified
    self-stress. Every one of them leaves all twenty-four frame squares fixed, and 52 of the
    frame's 72 coordinates are proved zero in every branch, so the flex looks like a block
    mechanism rather than a property of the packing at large -- twenty coordinates short of
    saying so outright. Nothing is promoted: an infinitesimal flex is not a motion, so both
    records stay undetermined.
  sources:
  - packing/campaign/series/series-000-smoke-and-calibration/results/bc-049-n5-rigidity-certificates.json
  - packing/campaign/series/series-000-smoke-and-calibration/results/bc-049-n40-rigidity-bracket.json
  - packing/campaign/series/series-000-smoke-and-calibration/results/bc-063-n5-rigidity-evidence.json
  - packing/atlas/known-best/translation-escape-screen.json
  - packing/frontier/n-005.md
  - packing/frontier/n-040.md
  - packing/frontier/evidence.yaml
  - packing/cases/gobel5/packing.py
  - packing/cases/gobel40/packing.py
  - defects.md
  proposes: []
---
# X-007 — The `n = 5` Optimum Flexes in Exactly One Direction, and That Direction Curves Shut

**Date:** 2026-08-30

**Status:** W6 research slice under `BC-049`, run as phase 5 of `session-045`. Delivers
the commitment’s **first** exit branch in substance and stops short of it in name: a
first-party certificate with a stated scope, where the scope is second-order rigidity
rather than local rigidity.

**Owns:** The argument, at `n = 5` and at `n = 40`. `devtools/assess_n5_rigidity.py`
owns the `n = 5` computation and the shared machinery, `devtools/assess_n40_rigidity.py`
the extension; `tests/test_n5_rigidity.py` and `tests/test_n40_rigidity.py` pin them,
and the gate steps `n=5 rigidity certificates still verify` and
`n=40 rigidity bracket still reproduces` replay them.

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

That rescaling turned out to be a special case rather than a trick, and finding its
limit took three defects.
It works here because every row is *wholly* rational or *wholly* irrational, and that
dichotomy is exhaustive at `n = 5` and nowhere else — Göbel’s `n = 40`, in the same
field, has 184 of its 400 contact rows carrying both parts, which no positive scalar
rationalizes ([`D-388`](../../../defects.md)). What answers those is a Farkas search
whose weights live in the ordered field: each row gets a weight `p + q sqrt 2` with both
parts free in sign and non-negativity imposed as the single inequality
`p + sqrt(2) q >= 0`. `certify` runs that alongside the cheaper restricted search and
verifies either result exactly, and it reproduces all fourteen certificates below
without the rescaling.

**Two further assumptions about contacts were wrong, and neither shows at `n = 5`.**
Both are recorded, both point the same way — toward reporting a pose *more* rigid than
it is — and the second is still open:

- [`D-390`](../../../defects.md): a corner lying on an edge’s **endpoint** is an
  incidence, not a contact.
  Two squares meeting edge-to-edge have exactly one separating axis, yet each one’s
  corners land on the endpoints of the other’s two perpendicular edges.
  Reading those as contacts asserts that a square free to move cannot.
  At `n = 40` that was 208 of 560 pair rows; at `n = 5`, none, because every contact
  here is a corner on the *interior* of an edge.
- [`D-391`](../../../defects.md): the tangent cone at a corner-to-corner touch is a
  **union** of half-spaces, not their intersection.
  “What This Establishes, and the One Step It Does Not”, below, is where this document
  argued that point in prose and then relied on it without checking it.

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
The set is semi-algebraic, and near this pose it is cut out by exactly these twenty
polynomial inequalities in the centres and in `(cos θ, sin θ)`. Two convex polygons are
disjoint when *some* axis separates them, so in general the condition is a maximum over
candidate axes rather than one inequality.
Here that maximum is attained at the contact normal and nowhere near it: along every
other candidate axis the two squares overlap in projection at this pose, strictly, and
therefore in a neighbourhood of it.

This paragraph was the only place in the repository where that distinction was written
down, and writing it down was not the same as checking it.
It is a claim about `n = 5`’s geometry, it is true, and the tool that depends on it went
on intersecting the half-spaces at every pose — which is [`D-391`](../../../defects.md).
`disjunctive_pairs` now decides the question from the pose, `assess` refuses any pose
that fails it, and `test_n5_has_no_disjunctive_pair` holds the exemption claimed here.
The cost of leaving it as prose was not hypothetical: at `n = 40`, 42 of 98 touching
pairs are corner-to-corner, and intersecting them reports that packing rigid when it is
not. So the curve selection lemma gives a semi-algebraic arc into the set, and Puiseux
gives `gamma(s) = p + sum_{k >= m} a_k s^k` with `a_m != 0`. Then:

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
sixteenth variable.

That caveat is load-bearing rather than formal, and the cheapest way to see it is to
drop it. Adding the side as a sixteenth variable takes the rank to 15 — the side appears
in no pair constraint — but the admissible cone opens to the full sixteen dimensions,
and the second-order refusal goes with it: `A y >= -q` becomes feasible, satisfied by
growing the side while translating two corner squares outward.
Every coordinate that is pinned above, the corner squares’ own rotations included, is
free once the box may grow.

None of that is surprising and none of it is a weakness: a container with slack in it is
not the object here.
It is worth measuring precisely because “rigid” said without a container condition would
be false, and the distance between the two readings is the whole sixteen dimensions.

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

`n = 40` then did the same thing later the same day, for the opposite finding: it is
infinitesimally *flexible*, its property still reads `undetermined` because a flex is
not a motion, and it left the assessed bucket on evidence
`E-n040-first-order-flexibility`. Three assessed and three left to a stronger argument.
That a record can leave for a stronger argument in *either* direction is the part worth
noticing — the bucket is about how much is known, not about which way the answer went.

Two things follow, and both are deliberate.

**[`D-354`](../../../defects.md) is untouched.** The catalogue’s bare “Rigid.”
stays in `reported_upper_bound.catalogue_rigid` and never becomes our finding.
The guard in `test_frontier_rigidity_assessment.py` that asserts `undetermined` for
`n = 5, 28, 40` stays green without being edited, and so does the one forbidding a
rigidity claim on screen-miss evidence.
That was the test this change was held to: a guard you have to weaken to land a result
is a guard that was telling you something.

**`n = 28` is not covered, and `n = 40` now is.** They were in the same `undetermined`
group and this section originally said nothing about either, on the ground that neither
had an exact construction retained.
That was true of the repository and false of the mathematics
([`D-389`](../../../defects.md)): Göbel’s family is published, `a = 3, b = 4` gives
exactly forty squares in side `4 + 2 sqrt(2)`, and `cases/gobel40` now builds it
exactly. What the extension found there is in the next section.
`n = 28` still retains only decimals and is untouched by any of this.

## What Extending It Cost, and What `n = 40` Turned Out to Be

This section predicted the wrong price, and the way it was wrong is the useful part.

It said the instrument was general in shape and specific in inputs — that
`assess_n5_rigidity.py` takes any pose in `Q(sqrt 2)` and does the rest without knowing
anything about `n = 5` — and that the only obstacle was the pose.
The pose was the smaller half.
Given an exact `n = 40`, the tool ran and produced an answer, and the answer was wrong
in three separate ways before it was right: rational weights against mixed rows
([`D-388`](../../../defects.md)), incidences read as contacts
([`D-390`](../../../defects.md)), and a union of half-spaces intersected
([`D-391`](../../../defects.md)). Each is invisible at `n = 5`, each points toward
reporting a pose *more* rigid than it is, and the third inverts the answer outright.

**`n = 40` is infinitesimally flexible.** All sixteen squares of the tilted central
block turn together, each about its own centre at the same rate, with translations that
hold every contact surviving in all branches at exactly zero gap rate; the twenty-four
frame squares do not move.
The witness is a vector in `Q(sqrt 2)^120`. The mechanism is visible in a single pair:
for two block squares sharing a full edge, the moving corner’s rotation contributes
`+1/2` to the gap rate and the host normal’s rotation contributes `-1/2`, and they
cancel. That is why the block can turn in place at first order, and why no instrument
that ignores the host’s rotation could have found it.

Finding it did not need the `2^42` branch enumeration the disjunction seems to demand.
Candidates come from the null space of the rows every branch carries — exact, so no
rounding can push a candidate out of the cone it came from, which is what defeated a
search over linear-programming vertices.
A candidate is a motion exactly when every corner-touching pair still has an axis that
separates along it, and that choice *names* an admitting branch instead of searching for
one.

**And it is refused at second order**, by the same argument as `n = 5` one scale up: 104
of the 283 tight contacts curve into the obstacle, and a verified non-negative
self-stress with `w . A = 0` and `w . q < 0` rules out every second-order correction at
once.

**The cone is wider than that one direction, and it is confined to the block.** Inside
the subspace where every all-branch contact stays tight, the admissible set is exactly a
line — of the 3124 nonzero integer combinations in `[-2, 2]^5` of the null basis, four
extend to a branch and all four are multiples of one vector.
Outside it there is more: six further motions are retained, each opening between four
and eight all-branch contacts strictly, each admissible at all 42 corner pairs, together
spanning rank five.
Every one of the seven is refused at second order by its own verified
self-stress. And every one of the seven — found by two unrelated routes — turns squares
of the tilted block and leaves all twenty-four axis-aligned squares exactly where they
are.

**The frame is mostly held, and the “mostly” is the honest part.** Fifty-two of its
seventy-two coordinates are *proved* zero in every branch: every branch’s cone sits
inside the relaxed one, so a coordinate the all-branch rows pin is pinned however the
disjunctions resolve, and each of the fifty-two carries a Farkas certificate verified in
the field. The other twenty are not proved.
Forty targeted searches over them reached twenty-four directions in the relaxed cone and
found none admissible, which is coverage rather than a proof — the same limitation the
translation-escape screen carries and is registered for.
So “the block is the mechanism” is a sharper statement than “`n = 40` flexes” and it is
not yet a theorem; twenty coordinates stand between.

So the shape of the two results is identical — flexible at first order, shut at second —
and the strength is not.
`n = 5` has a one-dimensional cone and that one direction is refused, which is what
earns the phrase *second-order rigid*. At `n = 40` seven directions are refused and the
cone is not bounded, so the phrase is not available.
Bounding it is the open question, and the machinery for the refusals is already written.

The real price of extending this, then, was not the pose.
It was that a tool validated on one pose had three assumptions in it that the pose could
not distinguish from theorems.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
