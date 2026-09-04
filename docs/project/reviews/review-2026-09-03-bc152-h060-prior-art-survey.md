# H-060 prior-art survey — BC-152 W1/W2 (agenda 016)

## Provenance and installation

This document is the review deliverable of BC-152 W1/W2, the H-060 three-gap prior-art
survey, written on 2026-09-03 in the agenda-016 ten-hour run.
Its author wrote only to `scratchpad/bc152-novelty/` -- a container-local directory
outside the repository, which does not survive the session -- and modified no repository
file.
It is installed here so that the evidence the records cite outlives that directory.

The source was `588` lines with SHA-256
`860a29509c7a9c829319e2f17461ea5f0d1dae6d207b179ffeec27192bdca9d3`, and that hash names
the scratchpad source rather than this file.
The installation added this preface and the closing guidelines footer, and reformatted
the body to house Markdown conventions; it altered no classification, verdict, finding,
number, citation, recommendation or claim boundary, and none may be altered here.
References of the form `scratchpad/...` in the body below are the reviewer’s own record
of what was read and where it was written at review time, and are left as written.

* * *

**Question.** If a proof of H-060 (Goebel’s exact `n = 5` packing is locally rigid at
fixed side `2 + sqrt(2)/2`) is completed, may it be labelled `apparently-novel`, and at
what scope?

**Date / branch.** 2026-09-03, `claude/squares-pr76-overnight-run-tpc888`.

**Repository inputs read.** `packing/campaign/hypotheses/H-060-n5-local-rigidity.md`,
`packing/campaign/explorations/X-007-the-n5-optimum-flexes-once-and-that-once-is-shut.md`,
`packing/frontier/results.yaml` (T-012, lines 339–366), `packing/frontier/RESULTS.md`,
`packing/frontier/evidence.yaml` (E-n005-second-order-rigidity lines 502–532,
E-n040-first-order-flexibility gaps line 565–566, E-n005-gobel-proof lines 168–190),
`packing/frontier/n-005.md`, `packing/frontier/n-011.md`,
`packing/frontier/square-packing-case.schema.yaml` (lines 152–224),
`packing/devtools/assess_n5_rigidity.py` (docstring; `second_order_terms`, lines
742–795), `packing/campaign/hypotheses/H-026-trump-first-order-rigidity.md`,
`packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-013-h-026-trump-tangent.md`
(lines 108–128), `epistemics.md` (lines 91–118), `packing/resources/README.md`, and the
whole of `packing/resources/` by grep (see the search record at the end).

**External material retrieved** (text extracted with an ephemeral `pymupdf` into this
directory; nothing in the repository was touched):

| Source | Local extract | Retrieved from |
| --- | --- | --- |
| Goebel 1979, *Geometrical packing and covering problems*, Math. Centre Tracts 106, 179–199 | `goebel1979.txt` (21 pp., 25 623 chars) | `packing/resources/papers/gobel-1979-geometrical-packing-and-covering-problems.pdf` (the archive’s own PDF, previously untranscribed) |
| Connelly & Whiteley 1996, *Second-order rigidity and prestress stability for tensegrity frameworks*, SIAM J. Discrete Math. 9(3) 453–491 | `cw1996.txt` | `https://pi.math.cornell.edu/~connelly/pdf/10.1137_S0895480192229236.pdf` |
| Donev, Connelly, Stillinger, Torquato 2007, *Underconstrained jammed packings of nonspherical hard particles: ellipses and ellipsoids*, Phys. Rev. E 75, 051304 | `donev2007.txt` | `https://pi.math.cornell.edu/~connelly/pdf/10.1103_PhysRevE.75.051304.pdf` |
| Connelly, lecture notes *Packings of circles and spheres* (slides) | `connelly-packings-notes.txt` | `https://pi.math.cornell.edu/~connelly/PackingsIII.IV.pdf` |
| Kingbird, *Squares in Squares: Rigid packings* (live page) | quoted below (WebFetch, two independent extractions) | `https://kingbird.myphotos.cc/packing/squares_in_squares__rigid.html` |
| Kingbird, *Analytic Minimization of Underdetermined Nonlinear Systems* | quoted below | `https://kingbird.myphotos.cc/packing/squares_in_squares__analytic_minimization.html` |
| MathWorld *Square Packing* | quoted below | `https://mathworld.wolfram.com/SquarePacking.html` |
| Nocedal–Wright-form second-order sufficient conditions (course summary) | `ucla-273-summary.txt` | `https://www.math.ucla.edu/~lvese/273.1.06f/Summary.pdf` |

Not retrieved: Connelly 2008, *Rigidity of packings*, Europ.
J. Combin. 29, 1862–1871 (ScienceDirect returned 403). Its content relevant here is
carried by the Connelly lecture notes and by Donev et al.
2007 §V.B.2, both retrieved.

* * *

## Preliminaries: what T-012 and X-007 already establish, in the terms used below

At Goebel’s exact pose `x*` in the 15-coordinate chart `(c_k, theta_k)` (two centre
coordinates and one angle per square; the tool’s velocities `v_k` and spins `w_k` are
the tangent coordinates), T-012 verifies exactly over `Q(sqrt 2)`:

- the 20 active contact gap functions `g_j` (16 corner-on-wall, 4 corner-on-edge of the
  middle square), with gradient rows `a_j = grad g_j(x*)` forming `A` (up to declared
  positive row scalings);
- the first-order cone `K = {d : A d >= 0}` is the line `R u`, `u` the unit spin of the
  middle square, the other 14 coordinates pinned by two-sided Farkas certificates (X-007
  §"First Order");
- the second-order coefficients `q_j = u^T H_j u` with `H_j = Hess g_j(x*)`
  (`second_order_terms` docstring: “`u . H_j . u` for every contact, exactly, along the
  straight line `x(t) = t u`”): `q_j = -1/2` at the four pair contacts, `0` at the
  walls;
- a non-negative self-stress `w` with `w A = 0` and `w . q = -1/2 < 0` (weights `1/2` on
  two pair rows and four wall rows; X-007 table).

X-007 §"What This Establishes" states the remaining gap as: an arc whose derivative
vanishes at the pose is excluded by nothing above, and proposes a semialgebraic
curve-selection plus Puiseux coefficient induction through order `2m`. H-060 makes that
route its instrument (`prereqs`: “sourced semialgebraic curve-selection theorem with
hypotheses matched to the pose chart”).

The registered novelty basis of T-012 (`evidence.yaml` line 523) names the three gaps
this survey was asked to close:

> Kingbird’s own ‘Rigid packings’ page, which defines the annotation it applies, was
> never archived, so what the catalogue means by ‘Rigid.’
> is unknown here. [Goebel 1979] is a PDF with no transcription.
> Trump’s personal site is not retained.
> The structural rigidity literature (Connelly, Whiteley and successors) is absent from
> this corpus entirely -- it is the body of work a refutation would most plausibly come
> from, and it is the largest known hole.

All three are addressed below with the primary texts in hand.

* * *

## Gap 1 — Structural rigidity / tensegrity / jamming prior art

### 1.1 What the repository corpus holds

Nothing. `grep -rli` over `packing/resources/` for `connelly`, `whiteley`, `tensegrity`,
`prestress`, `second-order rigid`, `jamm`, `torquato`, `donev`, `stillinger` matches
only through unrelated tokens (Roth–Vaughan 1978; “rigid motion” in Martin 2000; a
bibliography line in Alvarado et al.
2025). The only rigidity *claims* in the archive are catalogue annotations (Kingbird
“Rigid.” at `n = 5, 11, 28, 40`; Friedman DS7 “The packing for n = 40 is rigid” and, of
Trump’s `n = 11`, “This packing is also rigid”; Trump 2023: “The geometrical object is
absolutely rigid, no unit square can be rotated or translated”). None defines the term
or argues it. This confirms the T-012 basis statement; it does not settle the gap, which
needs the external literature.

### 1.2 Candidate theorems, their hypotheses, and where the square system falls outside

#### (a) Connelly–Whiteley 1996 (tensegrity frameworks)

Constraint class (Definition 2.1.1, `cw1996.txt` p. 457): “A tensegrity framework in
d-space G(p) is a signed graph (V; E_-, E_0, E_+), and an assignment p in R^{dv} such
that each p_i in R^d corresponds to a vertex of G … The members in E_- are cables, the
members in E_0 are bars, and the members in E_+ are struts.”
Domination (Definition 2.1.2) compares `|p_i - p_j|` with `|q_i - q_j|` member by
member. Rigidity is modulo congruence and is stated in three equivalent forms, the third
being “(c) for every analytic path, or analytic flex, p(t) ... p is congruent to p(t)”,
with the equivalence cited to [9] and [29].

Relevant results, quoted:

- Theorem 3.1.1 (energy principle, p. 460): “If such an H* has a local minimum at p
  which is strict up to congruence in some neighborhood of p in R^{dv}, then the
  framework G(p) is rigid.
  Proof. Any nearby q with G(q) <= G(p) will have f_ij(|q_i - q_j|^2) <= f_ij(|p_i -
  p_j|^2) for all members.
  Since this makes H*(q) <= H*(p), we conclude that q is congruent to p.”
- Definition 3.3.1 (prestress stability, p. 463): a proper self stress `w` and stiffness
  coefficients such that the quadratic form
  `sum w_ij (p'_i - p'_j)^2 + sum c_ij [(p_i - p_j).(p'_i - p'_j)]^2` is positive
  semidefinite with only trivial flexes in its kernel.
- Proposition 3.3.2 (p. 464): “If a tensegrity framework G(p) is prestress stable for a
  self stress w, then G(p) is rigid.
  Proof. The positive definite property of H guarantees a strict local minimum modulo
  trivial first-order flexes of p … Thus the energy principle applies to show G(p) is
  rigid.” Remark 3.3.2: “We will see, by Theorem 4.4.1, that if G(p) is prestress stable,
  then G(p) is second-order rigid and, by Theorem 4.3.1, G(p) is rigid.
  However, the present proof is much simpler since it is a direct application of the
  energy principle.”
- Definition 4.1.1 (second-order flex): for a strut, “either
  `(p_i - p_j).(p’_i - p’_j) > 0` or `(p_i - p_j).(p’_i - p’_j) = 0` and
  `|p’_i - p’_j|^2 + (p_i - p_j).(p''_i - p''_j) >= 0`”.
- Theorem 4.3.1 (p. 474): “If a tensegrity framework G(p) is second-order rigid, then it
  is rigid.” The preceding paragraph states the difficulty exactly as X-007 does: “The
  natural idea is to take the first and second derivatives of the analytic flex
  evaluated at the starting point.
  Unfortunately, this may not work because the first derivative of the analytic flex may
  be trivial, and we may have to wait for some higher derivative to be nontrivial.
  For cables and struts we use the principle that the first nonvanishing derivative of
  the member length squared has the correct sign.”
  The proof takes a nonrigid analytic flex (via Definition 2.1.2(c)), lets `k` be the
  first nontrivial derivative order, shows `p^{(k)}` is a first-order flex, and handles
  the orders `k+1 ... 2k-1` and the order-`2k` term with the sets `E_n` and a
  perturbation `r' = p^{(k)} + eps_1 p^{(k+1)} + ...` (pp.
  474–476). Remark 4.3.1: “The general outline for the above proof is the same as in
  [6]” ([6] = Connelly 1980, Adv.
  Math. 37).
- Theorem 4.4.1: prestress stable implies second-order rigid.
  Proposition 5.3.1 (p. 480): “If a tensegrity framework G(p) is second-order rigid with
  either a one-dimensional cone of equilibrium first-order flexes or a one-dimensional
  cone of proper self stresses, then G(p) is prestress stable.”

**Where the square system falls outside.** Every constraint in Definition 2.1.1 is a
comparison of a point-pair distance `|p_i - p_j|`. The `n = 5` system has none: a
corner-on-edge gap is `(p_A - c_B) . R(theta_B) n - 1/2`, a signed point-to-line
distance that is bilinear in the two bodies’ corner coordinates and depends on the
orientation of the host edge; a wall gap is a half-plane condition on a corner.
Neither is expressible as a cable, bar, or strut, and the sign structure differs in the
way that matters: a strut’s second-order term `|p'_i - p'_j|^2` is non-negative, whereas
the pair gaps here have `q_j = -1/2`. Rigidity in C–W is also modulo congruence with no
container, and the theorems are stated for point configurations, not rigid bodies.
So Theorem 4.3.1 and Proposition 3.3.2 **cannot be invoked as stated** — X-007’s own
caveat ("Adapting an argument is not the same as invoking a theorem") is correct.
What does transfer is the *proof* of Proposition 3.3.2, which uses nothing about
distances (see 1.3), and the *shape* of the proof of Theorem 4.3.1, which is exactly
X-007’s induction.

#### (b) Danzer / Connelly: packings of disks in a container (strut frameworks)

Connelly’s lecture notes (`connelly-packings-notes.txt`, slides 11–15): “Theorem (Danzer
1960): A packing P of circles (or spherical balls in 3-space) is collectively jammed in
a polygonal container C, if and only if the underlying strut tensegrity framework is
infinitesimally rigid.”
Proof idea: “let p' be the (non-zero) infinitesimal flex of G(p). Then for each i define
p_i(t) = p_i + t p’_i … The crucial calculation
|p_i(t) - p_j(t)|^2 = |p_i - p_j|^2 + 2t (p_i - p_j)(p’_i - p’_j) + t^2 |p’_i - p’_j|^2. So
|p_i(t) - p_j(t)| >= |p_i - p_j| for each pair of disks that touch”. (The published form
is Connelly 2008, Europ.
J. Combin. 29, 1862–1871; Donev et al.
2007 §V.B.2 “The stress matrix for hard spheres” gives the same argument.)
“Collectively jammed” (fixed container, all particles free) is the Torquato–Stillinger
term for exactly H-060’s fixed-side property.

**Where the square system falls outside.** The theorem is for disks; its proof depends
on the quadratic term of each constraint along a straight line being non-negative.
At `n = 5` that term is `q_j = -1/2` at every pair contact, which is why the packing is
first-order flexible yet not flexible.
Goebel’s `n = 5` is therefore a counterexample to any transfer of the disk equivalence
“rigid iff infinitesimally rigid” to squares with rotation, and this theorem family says
nothing about it beyond the (correct) necessary condition “jammed implies statically
rigid”.

#### (c) Donev–Connelly–Stillinger–Torquato 2007 (nonspherical particles, second-order jamming)

Scope (abstract): “we consider jamming in packings of smooth strictly convex
nonspherical hard particles.”
§V: “The discussion here is an adaptation of the theory of first-order, prestress, and
second-order rigidity developed for tensegrities in Ref.
[12]” ([12] = Connelly–Whiteley 1996). Under the analytic motion ansatz
`Q(t) = Q' t + Q'' t^2/2 + O(t^3)`, first-order flexes satisfy `A^T Q' >= 0`; §V.B: “we
want to look for accelerations Q'' that make the second-order term … non-negative, i.e.,
A^T Q'' >= -Q'^T H Q'. (17) If we cannot find such a Q'' for any first-order flex, then
the packing is second-order jammed.”
Dual (19): `min_f Q'^T H_f Q'` over `A f = 0, e^T f = 1, f >= 0`. “If Q'^T H Q' < 0 then
sigma* < 0 and therefore the first-order flex Q' cannot be extended into a second-order
flex. We say that the stress matrix blocks the flex.”
“If the matrix H_V is negative definite, than the packing is second-order jammed.
In Ref. [12] such packings are called prestress stable, since the self-stress f
rigidifies the packing.”
And the same higher-order caveat X-007 raises: “If for all first-order flexes Q' at
least one of the inequalities in Eq.
(17) has to be an equality, then we need to consider even third- or higher-order terms,
however, we will see that for sphere and ellipsoid packings this is not necessary.”

This is precisely T-012’s computation in their vocabulary: T-012’s `w` is their `f`,
`w . q` is `Q'^T H_f Q'`, and with a one-dimensional flex space `H_V` is the `1 x 1`
matrix `[-1/2]`, negative definite, so `n = 5` is “second-order jammed / prestress
stable” in their classification.

The paper also states the *mechanism* of `n = 5` qualitatively, for polygons, in §II
(Fig. 3 discussion): “Now imagine making the particles noncircular … making them
polygons, so that the point contacts between the disks become extended contacts between
flat sides of the polygons.
The floppy modes still remain, in the sense that rotations of the polygons, to first
order, simply lead to the two tangent planes at the points of contact sliding along each
other without leading to overlap.
However, it is clear that this is only a first-order approximation.
In reality, the polygons cannot be rotated because such rotation leads to overlap in the
extended region of contact around the point of contact.
To calculate the amount of overlap, one must use second-order terms … Low curvature,
that is, ‘flat’ contacts, block rotations of the particles.”
X-007’s “turning the line can therefore only bring it nearer” is this observation at a
corner-on-flat-edge contact.

§VIII states the energy route: “This gives a simple way to prove that a given packing is
jammed: Find a set of interparticle potentials that makes the configuration a stable
energy minimum [12,13]. ... It is well known that for smooth interactions a given
configuration is a stable energy minimum if the gradient of the energy is zero and the
Hessian is positive definite”.

**Where the square system falls outside.** The derivation is for smooth strictly convex
particles with a smooth overlap function; the implication “second-order jammed implies
jammed” is asserted by adaptation of [12] and by the energy argument, not stated as a
theorem with hypotheses; and the authors explicitly exclude polygons from what they
establish: “Future work should consider the mathematics of jamming for packings of hard
particles that are convex, but not necessarily smooth or strictly convex.
In particular, particles with sharp corners and/or flat edges are of interest, such as,
for example, tetrahedra [52], cylinders and cubes.”
No theorem here has hypotheses reduced to corner-on-edge contacts in a fixed container.

#### (d) Classical second-order sufficient optimality conditions (nonlinear programming)

This is the one stated theorem found whose hypotheses **do** reduce to the `n = 5` local
system. Standard statement (McCormick 1967, SIAM J. Appl.
Math. 15, 641–652; Fiacco & McCormick 1968, *Nonlinear Programming: SUMT*; Nocedal &
Wright, *Numerical Optimization* 2nd ed., Theorem 12.6 — the last two citations are from
memory of the printed texts and should be checked by the reviewer; the Nocedal–Wright
form as reproduced in the retrieved course summary `ucla-273-summary.txt` p. 2 reads):
“Suppose that at some feasible point x* there is a Lagrange multiplier lambda* such that
the KKT conditions are satisfied.
Then if the following condition is satisfied, then x* is a strict local minimizer: w^T
grad^2_xx L(x*, lambda*) w > 0 for all w in F(lambda*), w != 0”, where
`F(lambda*) = { w : grad c_i(x*)^T w = 0 for active i with lambda*_i > 0; grad c_i(x*)^T w >= 0 for active i with lambda*_i = 0 }`.
No constraint qualification is assumed for the sufficient direction; `f` and `c_i` twice
continuously differentiable near `x*`.

Reduction to H-060 (each step checkable against T-012’s receipts):

1. *Objective.* Take `f(x) = -|x - x*|^2`. Then `x*` is isolated in the feasible set `F`
   iff `x*` is a strict local minimizer of `f` on `F` (any other feasible point nearby
   has `f < 0 = f(x*)`).
2. *Constraint system.* Near `x*`, feasibility implies `g_j(x) >= 0` for the 20 active
   contacts (the necessity half of H-060’s neighborhood reduction, see 1.3; inactive
   constraints are strictly satisfied on a neighborhood and impose nothing).
   The `g_j` are `C^infinity` in the `(c, theta)` chart — the same chart in which
   T-012’s `A` and `q` are computed.
3. *KKT.* `grad f(x*) = 0`, so a multiplier is any `lambda >= 0` with
   `sum lambda_j grad g_j(x*) = 0`, i.e. a non-negative self-stress.
   Take `lambda = s w` for a scalar `s > 0` (still KKT).
4. *Critical cone.*
   `F(s w) = { d : a_j . d = 0 on supp w, a_j . d >= 0 on the other active rows }`. This
   is contained in `K = { A d >= 0 } = R u` (T-012), and contains `u` because no row has
   a nonzero entry in the middle square’s spin column.
   So `F(s w) = R u`.
5. *Second-order condition.*
   `u^T grad^2 L u = u^T grad^2 f u - s sum w_j u^T H_j u = -2|u|^2 - s (w . q) = -2|u|^2 + s/2 > 0`
   for `s > 4|u|^2` (with `|u| = 1`, any `s > 4`).
6. *Conclusion.* `x*` is a strict local minimizer of `-|x - x*|^2` on `F`, hence
   isolated in `F`: fixed-side local rigidity.

Positive row scalings between T-012’s stored rows and the true gradients are harmless:
scaling row `j` by `s_j > 0` scales `a_j` and `q_j` identically and `w_j` by `1/s_j`.

### 1.3 The closing step, written out (so that the verdict does not rest on a citation)

The specialization of the SOSC proof to this case is short enough to state in full; it
is also the proof of Connelly–Whiteley’s Proposition 3.3.2 with `sum w_j g_j` in the
role of the energy, and Donev et al.'s “find potentials that make the configuration a
stable energy minimum”.
It uses no semialgebraicity, no polynomial chart, no curve selection, and no Puiseux
expansion.

*Hypotheses.* (N) There is a neighborhood `U` of `x*` such that every fixed-side
feasible pose `x in U` satisfies `g_j(x) >= 0` for the 20 active contacts, each `g_j`
being `C^2` on `U`. (K) `{ d : A d >= 0 } = R u`, where `A` has rows
`a_j = grad g_j(x*)`. (S) There is `w >= 0` with `sum_j w_j a_j = 0` and
`sum_j w_j u^T H_j u < 0`, `H_j = Hess g_j(x*)`.

*Claim.* `x*` is isolated in the fixed-side feasible set.

*Proof.* Suppose feasible `x_k -> x*`, `x_k != x*`. Set `d_k = (x_k - x*)/|x_k - x*|`
and pass to a subsequence with `d_k -> d`, `|d| = 1`. For each active `j`,
`0 <= g_j(x_k) = a_j . (x_k - x*) + O(|x_k - x*|^2)` by (N), so `a_j . d >= 0` and by
(K) `d = +-u/|u|`. Let `Phi = sum_j w_j g_j`. By (N) and `w >= 0`, `Phi(x_k) >= 0`. By
(S), `Phi(x*) = 0` and `grad Phi(x*) = sum w_j a_j = 0`, so Taylor’s theorem gives
`Phi(x_k) = (1/2)|x_k - x*|^2 ( d_k^T Hess Phi(x*) d_k + o(1) )`, and the bracket tends
to `d^T (sum w_j H_j) d = (sum w_j u^T H_j u)/|u|^2 < 0`. Hence `Phi(x_k) < 0` for large
`k`, a contradiction.
∎

Two remarks on (N). Only the direction “feasible implies the 20 inequalities” is used,
and it follows from exact strict margins at `x*` plus continuity: for each touching
pair, the three non-contact separating axes overlap strictly in projection at `x*`, the
resting corner is the unique support corner, and the far-side orientation is excluded,
so nearby non-overlap forces the contact-axis gap `g_j >= 0` (this is what X-007 argues
in prose and what H-060’s instrument is to certify).
No isolation radius, no polynomial chart, and no converse ("the 20 inequalities imply
feasibility") are needed for the isolation claim.
The argument is the second-order instance of the pattern the repository already used at
first order for Trump’s `n = 11` pose (exp-013, “Finite-branch local-isolation
corollary”: normalise displacements, pass to a convergent subsequence).

### 1.4 Other theorem families checked and why they do not apply

- Generic and combinatorial rigidity (Laman; body–bar; body-and-cad; slider-pinning):
  first-order and generic.
  Goebel’s pose is non-generic in the precise way that produces the flex (each inner
  corner at the midpoint of the middle square’s edge), and the question is second-order.
  Not applicable.
- Connelly–Servatius 1994 (Discrete Comput.
  Geom. 11, 193–199) and arXiv:2410.15541: a framework can be third-order rigid in the
  Taylor-coefficient sense yet flexible.
  Relevant as a warning for the Puiseux route: the order-`2m` induction must be carried
  out exactly as C–W do for `k ... 2k`, and must not be generalised to higher orders
  without their care. The sequence argument of 1.3 is not exposed to this.
- Alpert–Bauer–Kahle–MacPherson–Spendlove 2023 (in the archive): configuration spaces of
  axis-aligned hard squares; no rotations, and side `2.707` admits at most four
  axis-aligned unit squares, so it says nothing about this pose.

### 1.5 Hypothesis-failure table

| Prior result | Constraint class assumed | Failing hypothesis at `n = 5` | What survives |
| --- | --- | --- | --- |
| C–W 1996 Thm 4.3.1, Prop 3.3.2, Thm 4.4.1, Prop 5.3.1 | point-pair distance members (cables/bars/struts), rigidity modulo congruence, no container | gaps are signed point-to-line distances of rigid bodies, walls are half-planes; pair-gap curvature is negative | the energy-principle proof (constraint-agnostic); the analytic-flex induction shape |
| Danzer / Connelly 2008 | disks in a polygonal container (struts only) | particle shape; the straight-line push needs ` | p’_i - p’_j |
| Donev et al. 2007 §V | smooth strictly convex particles, analytic-motion ansatz | non-smooth particles explicitly deferred to future work; no theorem stated | the first/second-order LP–duality formalism; the flat-contact mechanism; the energy route |
| McCormick 1967 / Fiacco–McCormick 1968 / Nocedal–Wright Thm 12.6 | any `C^2` inequality system with a KKT point | none — hypotheses reduce to the local 20-inequality system given (N), (K), (S) | the whole closing inference |

### 1.6 Verdict — Gap 1

**CLOSED-NOT-NOVEL** for the inference “first-order cone `R u` plus a non-negative
self-stress with `w . q < 0` implies fixed-side local isolation”: it is the classical
second-order sufficient optimality condition (McCormick 1967; Fiacco–McCormick 1968;
Nocedal–Wright Theorem 12.6) applied to `min -|x - x*|^2` over the local contact system,
equivalently Connelly–Whiteley’s energy principle (Theorem 3.1.1 / Proposition 3.3.2)
and Donev et al. 2007 §VIII, and its hypotheses reduce to this system as itemised in
1.2(d).

Qualification that must accompany the verdict: **no theorem stated in the
structural-rigidity or jamming literature covers polygon contact systems** — C–W is for
distance constraints, Danzer/Connelly for disks (and its equivalence fails here), and
Donev et al. explicitly defer particles “with sharp corners and/or flat edges”.
The mechanism ("flat contacts block rotations at second order") is stated qualitatively
in Donev et al.
2007 §II. The case-specific content — the exact certificates of T-012 and
the exact local reduction (N) at Goebel’s pose — is not in any retrieved source.

Consequence for the proof lane: the curve-selection / Puiseux route in H-060 is a valid
but unnecessary detour; the sequence argument of 1.3 (or the SOSC theorem) proves the
same claim from strictly weaker hypotheses, in the tool’s existing smooth chart, and
with a sourced theorem whose hypotheses match.
If the Puiseux route is kept, it should be cited as the shape of Connelly 1980 /
Connelly–Whiteley 1996 Theorem 4.3.1, not as new.

* * *

## Gap 2 — Goebel 1979

### 2.1 What Goebel proved

The archive’s PDF
(`packing/resources/papers/gobel-1979-geometrical-packing-and-covering-problems.pdf`)
was not transcribed before; `goebel1979.txt` now holds the extracted text (21 pages; the
PDF has a text layer).
The `n = 5` content is all on printed pages 180–181:

> “The treatment is elementary; proofs are hardly given.
> The stress is on defining problem areas and pointing out open problems.”
> (p. 179)

> “The exact value of z*(n) is known only for n = 2,3,5 and the squares of integers.”
> (p. 180)

> “To demonstrate a technique for finding non-trivial lower bounds, we outline a proof
> of the following result (which implies z*(5) = 2 + ½√2). PROPOSITION 1. S’ :=
> S(2+½√2−ε) cannot be packed with 5 unit squares (ε > 0). OUTLINE OF PROOF. Take an S’
> and draw four lines in its interior, parallel to the sides and at a distance 1 − ε/3
> from the sides (see figure 2). It is sufficient to show that any unit square S(1) in
> S’ covers at least one of the points A, B, C, D. There are 3 cases.”
> (pp. 180–181)

That is the entire treatment: a lower-bound outline by four unavoidable points, plus the
packing in Table 1 as the matching upper bound.
The words `rigid`, `unique`, `move`, `wiggle` do not occur anywhere in the 21 extracted
pages (grep). Goebel states nothing about uniqueness of the optimal configuration,
nothing about continuous motion, and nothing about local rigidity.

The repository already records this correctly: `E-n005-gobel-proof` cites “Proposition
1, z*(5) = 2 + sqrt(2)/2 … Printed pages 180-181, Proposition 1, Figure 2, and its
three-case proof outline” as a lower-bound claim only.

### 2.2 The other optimality proof, and the uniqueness question

Friedman DS7 (`packing/resources/papers/friedman-ds7-packing-unit-squares-in-squares.md`
line 225–227): “**Theorem 2.** s(5) = 2 + 1/√2. *Proof:* The set P = {(1,1), (1, 1 +
1/√2), (1 + 1/√2, 1), (1 + 1/√2, 1 + 1/√2)} is unavoidable in [0, 2 + 1/√2]^2.” Again a
lower bound.
Friedman’s only rigidity remarks (lines 59, 71) concern `n = 40` and Trump’s
`n = 11`; `n = 5` is not annotated.
MathWorld’s *Square Packing* page: `n = 5` marked proven optimal; “The page contains no
sentences with the words ‘rigid’ or ‘unique’.” The archived Wikipedia page contains no
occurrence of “rigid”.

This matters because a published *uniqueness* theorem for the `n = 5` optimum (unique up
to the container’s symmetries) would make fixed-side rigidity a corollary — a continuous
flex through an optimal pose yields infinitely many distinct optimal packings.
No such theorem was found in the corpus or by web search ("five unit squares … unique /
uniqueness"; results are the surveys above, none claiming uniqueness).
The unavoidable-set proofs of Goebel and Friedman do not analyse the equality case, so
they do not yield uniqueness.
Kingbird’s “compared” page lists no alternative packing for `n = 5`, which is absence of
a record, not evidence.

### 2.3 The three claims, separated

| Claim | Status in the literature found |
| --- | --- |
| `s(5) = 2 + sqrt(2)/2` (optimality) | proved: Goebel 1979 (outline), Friedman DS7 Theorem 2 |
| the optimal packing is unique up to symmetry | not stated or proved in any source found |
| the optimal packing is locally rigid at fixed side / has no continuous flex | not stated by Goebel or Friedman; asserted by Kingbird (Gap 3) |

### 2.4 Verdict — Gap 2

**CLOSED-NOVEL** with respect to Goebel: Goebel 1979 proves (in outline) optimality
only, states no uniqueness or rigidity property, and H-060 is not a corollary of
anything in it. No uniqueness theorem for `n = 5` exists in the sources found, so no
“uniqueness implies rigidity” route pre-empts H-060 either.
The one source that would reverse this verdict is a published uniqueness proof for
`s(5)`; none was located.

* * *

## Gap 3 — Kingbird

### 3.1 What Kingbird defines

The “Rigid packings” page (`squares_in_squares__rigid.html`, live, retrieved 2026-09-03;
it was never archived, which T-012’s basis names as its first gap):

> “Squares in Squares: Rigid packings” — “This is a list of rigid packings.
> Most are the best known, but in cases where they are inoptimal, they are shown
> alongside the best known.”

> “A packing is rigid when it cannot be continuously transformed into any other valid
> packing without changing the size of its enclosing square.”

> “Where the word ‘alternative’ is used, this designates an alternative packing, which
> is enclosed within the same-sized bounding square as another packing, but cannot be
> reached by continuously translating and/or rotating the squares in that packing.”
> “When the packing can be reached by such continuous transformations, the word
> ‘rearrangement’ is used.”

> “The property of rigidity is rare among nontrivial best known packings.”

Entry for `n = 5` on that page: “5. [SVG] s = 2 + ½√2 = 2.70710678118654. Proved optimal
by Frits Göbel in early 1979.” On the archived main page
(`packing/resources/web/kingbird-squares-in-squares.md` line 44) the `n = 5` entry reads
“[Rigid.] Proved by Frits Göbel in early 1979.” The main page carries “Rigid.”
on exactly four packings at `n <= 100`: `n = 5, 11, 28, 40` (lines 44, 80, 163, 224),
consistent with the schema comment “all but four packings at n <= 100”.

How the annotation is decided: both extractions of the rigid page agree that “The page
contains no explicit sentences stating how rigidity was proven, verified, or conjectured
for individual entries.
No general methodology for determining rigidity is provided.”
The “Analytic Minimization of Underdetermined Nonlinear Systems” page does not use the
words rigid, semi-rigid, underdetermined, degrees of freedom, or discuss `n = 5`; it is
about minimising side length through contact equations and Jacobian determinants.
The `n = 11` provenance SVG
(`packing/resources/papers/kingbird-square-11-provenance.svg` line 21) says only “Is one
of the very few rigid packings.”
“Semi-rigid” is used on the rigid page for `n = 28` without a definition.

### 3.2 Overlap with H-060’s claim

Kingbird’s definition is: no nonconstant continuous path in the fixed-side feasible set
starting at the pose reaches a different packing — i.e. the pose’s path component is a
point. H-060’s claim is that the pose is isolated.
For a closed semialgebraic set these coincide (semialgebraic sets have finitely many
connected components, each semialgebraic and closed, and are locally path-connected; an
isolated point is its own component and conversely a one-point path component is
isolated because the finitely many other components are closed).
So Kingbird’s “Rigid.”
at `n = 5` is **the same proposition as H-060**, asserted without definition of method,
argument, or evidence.
It is a finite (not infinitesimal) notion, so it is not contradicted by T-012 ("not
infinitesimally rigid but second-order rigid") nor by T-013 (`n = 40` infinitesimally
flexible); the worry recorded in `E-n040-first-order-flexibility`’s gaps ("a catalogue
meaning ‘infinitesimally rigid’ would contradict this result outright") is now resolved
in the repository’s favour.

### 3.3 The Kingbird witness and case code

`packing/witnesses/kingbird-n029-2026-interval.yaml` (id `W-kingbird-n029-interval`) and
`cases/kingbird29/` concern `n = 29` only: a Krawczyk interval enclosure of the pose and
side from the six closing equations of the provenance SVG. Its `unique: true` is
root-uniqueness of that square system inside a pose box of radius `3.19e-62` — a
statement about a nonlinear solve, not about packing rigidity — and its `limitations`
say “Not the optimum, not an optimality result”.
It has no bearing on `n = 5` or on H-060’s notion.

### 3.4 Verdict — Gap 3

**CLOSED-NOT-NOVEL as a statement; CLOSED-NOVEL as a proof.** Kingbird asserts, under a
definition equivalent to H-060’s claim, that Goebel’s `n = 5` packing is rigid; it gives
no argument and no method anywhere on the site, and its rigidity page even drops the
annotation into a bare “Proved optimal” line for `n = 5`. Nothing in the Kingbird
material (page, article, SVGs, `n = 29` witness) proves or purports to prove the
property. Any registered result must therefore be worded as the first proof of a
catalogue-asserted property, not as a new claim.

* * *

## Overall recommendation

### Can an H-060 proof be registered as `apparently-novel`?

Yes, at one scope only:

> **Novel object.** A first-party, exact proof that Goebel’s `n = 5` optimal packing is
> locally rigid at fixed side `2 + sqrt(2)/2` (collectively jammed, in
> Torquato–Stillinger / Connelly terminology): the fixed-side feasible set is locally
> reduced to twenty smooth contact inequalities by certified exact margins, and the
> T-012 certificates then close by the classical second-order sufficient optimality
> condition (prestress stability).
> The property was asserted without proof or method by the Kingbird catalogue; it is not
> stated by Goebel 1979 or Friedman DS7; no uniqueness theorem implies it; and no
> theorem in the structural-rigidity or jamming literature is stated for polygon
> corner-on-edge contact systems (Donev et al.
> 2007 explicitly defer them).

What the label must **not** cover:

- the closing inference itself (SOSC / Connelly–Whiteley energy principle / Donev §VIII
  — `previously-published`);
- the mechanism (flat contacts block rotations at second order — Donev et al.
  2007 §II);
- the proof shape of the Puiseux route, if it is kept (Connelly 1980; Connelly–Whiteley
  1996 Theorem 4.3.1);
- global uniqueness, an isolation radius, or any `n != 5` statement.

Significance should be scored as a case result (`S3`), not a reusable technique (`S4`).
The `novelty_basis` should list the sources retrieved here (table at the top), the
searches that returned nothing (uniqueness for `n = 5`; rigidity theorems for hard
squares), and the one source not obtained in print (Connelly 2008).

### Course correction for the proof lane (BC-152) and reviewer (BC-153)

1. The closing step can be the sequence argument of 1.3 or a direct appeal to the SOSC
   theorem with the reduction of 1.2(d). Both need only: the necessity half of the
   neighborhood reduction (N), `C^2` gap functions in the tool’s existing `(c, theta)`
   chart, and T-012’s `A`, `w`, `q`. The half-angle chart, semialgebraicity, curve
   selection, and the order-`2m` induction are not needed for isolation.
   H-060’s pre-registered criterion names “a reviewed curve-selection and coefficient
   argument”; whether to amend that wording before evaluation or to run both routes is
   the coordinator’s decision — the SOSC route proves the same claim from weaker
   hypotheses, so it satisfies the criterion’s purpose, but not its letter.
2. If the Puiseux route is retained, cite Connelly–Whiteley 1996 Theorem 4.3.1 and
   Remark 4.3.1 for its shape and Connelly–Servatius 1994 for why the induction must
   stop at order `2m`; do not present it as an original argument.
3. BC-153’s instruction “do not invoke a tensegrity theorem whose hypotheses were not
   reduced to this system” stands; the SOSC theorem is not a tensegrity theorem and its
   hypotheses are reduced above, step by step.
4. Outside this survey’s write scope but worth a bead: the `gaps` fields of
   `E-n005-second-order-rigidity` and `E-n040-first-order-flexibility` can now be
   tightened (Kingbird’s definition is known and finite; Goebel is transcribed; the
   Connelly–Whiteley / Donev texts are retrieved), which strengthens T-012’s and T-013’s
   existing `apparently-novel` labels rather than weakening them.

### Residual OPEN items (none blocking)

- Connelly 2008 (Europ.
  J. Combin.) was not read in print; its relevant theorem is reproduced in the retrieved
  lecture notes and in Donev et al.
  §V.B.2. A copy would only confirm the disk-only scope already established.
- The Nocedal–Wright / Fiacco–McCormick theorem numbers are cited from memory and should
  be checked against the printed texts by the reviewer; the self-contained proof in 1.3
  does not depend on them.
- The Kingbird author’s method for “Rigid.”
  is unknown (not contacted); this cannot change the verdict because no argument is
  published either way.

* * *

## Search record

Repository (`packing/resources/`, all files, case-insensitive grep): `rigid` — hits only
in Friedman DS7 (`n = 40`, `n = 11`), Kingbird main page (`n = 5, 11, 28, 40`), Trump
2023 (`n = 11`), the `n = 11` provenance SVG, Stromquist 2003 ("the argument … is not
rigid", about a point set), Martin 2000 ("rigid motions"), one bibliography line in
Alvarado et al. 2025, and `prospective-packings/README.md` (a disclaimer).
`connelly`, `whiteley`, `tensegrity`, `prestress`, `second-order`, `infinitesimal`,
`farkas`, `self-stress`, `jamm`, `donev`, `torquato`, `stillinger`, `curve selection`,
`puiseux`, `milnor`, `bochnak`, `fiacco`, `mccormick`, `kkt` — no substantive hits in
the archive; in the campaign only X-007, H-060, bc-049’s JSON and agenda 016 mention
curve selection. Goebel PDF: `rigid`, `unique`, `move`, `wiggle` absent.

External: Connelly–Whiteley 1996 (full text); Donev et al.
2007 (full text); Connelly lecture notes (full text); Kingbird rigid page and
analytic-minimization page (live); MathWorld (live); web searches for a uniqueness proof
of the five-square optimum and for rigidity theorems on hard squares / polygons with
flat contacts (no relevant hits beyond the sources above).

Local extracts in this directory: `goebel1979.txt`, `cw1996.txt`, `donev2007.txt`,
`connelly-packings-notes.txt`, `ucla-273-summary.txt`, `stanford-msande311-lec06.txt`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
