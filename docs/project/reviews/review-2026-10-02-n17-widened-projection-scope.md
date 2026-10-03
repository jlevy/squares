---
title: n17 Widened Projection Theorem, Scope and Instrument
date: 2026-10-02
status: planning-review
---
# n17 Widened Projection Theorem, Scope and Instrument

**Session:** 167, BC-406, lane E. **Baseline:** main after PR 265 and PR 269.
**Question:** can the
[conditional projection theorem](review-2026-10-01-n17-projection-branches.md) be
widened into a near-terminal theorem whose hypotheses a capture step can deliver: every
packing whose 17 angles lie within $\rho_a$ of their endpoint values and whose contact
features are the endpoint’s has $S\ge S^{\ast}$, with equality only on the endpoint
family?

The [capture feasibility review](review-2026-10-02-n17-capture-feasibility.md) named
this theorem as the architecture that lifts the capture target from the H-261 radius
($3\times10^{-4}$) to the feature-forcing region ($\sim10^{-2}$). This review scopes it.
Its numbers come from an exploratory floating-point probe in the session scratchpad
(`scratchpad/lanes/e/lp_probe*.py` and `.out`); none is an admitted result.
It changes no bound, verdict or frontier field.

## Summary

- **The theorem is a parametric linear program, not three scalar functions.** At fixed
  angles and fixed owner normals, nonoverlap along a forced feature and containment are
  linear in the centres and the side.
  The projection theorem’s chains are one hand dual of this LP at common orientation,
  and its row set is exactly the positive row set of the H-258 stress.
  Widening means certifying $S_{\rm LP}(\psi)\ge S^{\ast}$ over an angle box, with the
  centres eliminated by the LP rather than by Taylor bounds.
- **The slider domain is a premise, not a nuisance.** With the three sliding squares
  unconstrained, the LP has five flat directions and one negative one ($+\omega_{14}$,
  slope $-0.011$), reached by sliding square 5 by $3.7$ and square 11 by $1.8$. With the
  H256 slider domain plus a $10^{-2}$ margin as rows, every one of the 32 coordinate
  directions has positive slope; the softest is $0.0155$ per radian ($\beta$
  increasing), the next $0.088$ ($-\omega_{11}$).
- **The value function is conical out to $3\times10^{-2}$.** Slopes along coordinate
  directions are constant to three digits from $10^{-5}$ to $3\times10^{-2}$ radians, so
  the sheet curvature is of order $0.3$ per squared radian, against the n11-recipe
  constant of $33$ that fixes the H-261 radius.
  The theorem appears true on an angle box of radius $10^{-2}$ and probably
  $3\times10^{-2}$; feature forcing, not the LP, caps the radius at about $10^{-2}$.
- **Side range and the $15\parallel16$ branch disappear.** A dual bound carries no side,
  so the premise $S\in[4.675,4.676]$ was an artefact of the hand proof.
  The co-orientation of square 15 with 16 sits $0.64$ radians from the box and is a
  different feature set, excluded by the global step rather than by this theorem.
- **Verdict.** Plausible at $\rho_a\approx5\times10^{-3}$ to $10^{-2}$ in angles with
  centres within $10^{-2}$ of the family.
  The instrument is an interval certificate of dual sheets over direction patches in
  seven backbone angles; it reuses H-261’s exact duals and should nest inside H-261’s
  bead rather than replace it until it certifies.

## 1. The Chain Argument as a Linear Program

**Where common orientation enters.** The projection theorem uses the common basis $u,v$
of squares 9, 10, 11, 12 and 14 in four places: the telescoping sums along $u$
($9\to10\to15$, $3\to11\to12$, $2\to13\to14\to17$) and along $w$
($4\to10\to12\to14\to7$); the unit supports $H_i(u)=H_{12}(u)=1/2$; the bridge
identities $p\cdot r=(d/c)(u\cdot r)-(\gamma/c)y$ and
$p\cdot r=(\gamma/s)x-(e/s)(u\cdot r)$; and $H_{16}(u)=(\alpha+\gamma)/2$ in $12\to16$.
With individual angles each chain can be rewritten along its last owner’s normal
($u_{10}$, $u_{12}$, $u_{14}$), and the bridge identities hold with $(c,s)$ replaced by
that owner’s cosine and sine.
A parallel-face link whose owner is the other square then projects with a loss
$|\varepsilon|\,|\tau|$ and a gain $\tfrac12|\sin\varepsilon|$ from the support, so with
$|\tau|<1/2$ it still contributes at least $1$; all nine offsets satisfy
$|\tau^{\ast}|\le0.276$.

**Where the elimination stops closing by hand.** The $w$ chain has different owners at
its two ends (square 10 at $4\to10$, square 14 at $14\to7$). Written along $w_{12}$, a
split of square 10 from 12 relaxes it by up to $0.055|\varepsilon|$ (kink $0.224$
against rotating-normal loss $0.215$ and support change $0.064$) and a split of 14 from
12 by up to $0.18|\varepsilon|$ (offset $u\cdot(r_7-r_{14})=0.49$). $F_1$ alone can
therefore fall under a split; the $u$ chains must make it up through $F_2$ and $G_3$.
Three fixed scalar functions no longer carry the argument.
What does carry it is the LP: for fixed angles $\psi$ and forced owner normals,
feasibility in the 32 centre coordinates (square 6 absent) and $S$ is linear, and
$S_{\rm LP}(\psi)=\min S$ over it is a lower bound for every packing with those
features. At $\psi^{\ast}$ the probe reproduces $S_{\rm LP}=S^{\ast}$ to $10^{-15}$.

The rows are the 19 chain pairs, each along one of its endpoint owner normals (the nine
parallel faces as a disjunction of two owners), and all 64 containment rows.
This is the stress’s positive row set: its six zero-weight rows are the $5$-right and
$6$-bottom walls and the $9/11$ face, which the chains also omit.
So the first-order cone of the chain subsystem is the stress’s cone, and the chain
argument generalises exactly as far as the stress does.

## 2. The Angle Region

The probe evaluates $S_{\rm LP}(\psi)$ by enumerating the owner choices (up to $2^9$ LPs
per point) along every signed coordinate direction and along random directions, in three
variants: the bare chain rows (V0); with the slider domain as rows (V3:
$\xi_5\in[-0.11-\rho_p,\rho_p]$, square 11 along $-v$ up to $0.07+\rho_p$, square 13
along $\pm v$ within $0.036+\rho_p$ of the centroid, $\rho_p=10^{-2}$); and with a full
centre box of radius $\rho_p$ and a side box as well (V2).

| Direction | V0 slope | V3 slope at $10^{-5}$ | at $10^{-2}$ | at $3\times10^{-2}$ |
| --- | ---: | ---: | ---: | ---: |
| $-\omega_{16}$ ($\beta$ up) | $0.0155$ | $0.0154$ | $0.0172$ | $0.0207$ |
| $-\omega_{11}$ | $0$ | $0.0876$ | $0.0876$ | $0.0875$ |
| $+\omega_{13}$ | $0$ | $0.1019$ | $0.1033$ | $0.1061$ |
| $-\omega_{13}$ | $0$ | $0.1905$ | $0.1905$ | $0.1905$ |
| $+\omega_{14}$ | $-0.0108$ | $0.2632$ | $0.2631$ | $0.2630$ |
| $-\omega_5$, $-\omega_7$ | $0$ | $0.4800$ | $0.477$ | $0.473$ |
| $-\omega_9$ | $0.154$ | $0.154$ | $0.151$ | $0.145$ |
| $+\omega_{10}$ | $0.182$ | $0.182$ | $0.185$ | $0.190$ |
| $+\theta$ (9–14 together) | $0.101$ | — | $0.105$ | $0.112$ |
| $-\omega_{12}$ (steepest) | $0.710$ | $0.710$ | $0.707$ | $0.699$ |

Slopes are $(S_{\rm LP}-S^{\ast})/r$ in side units per radian.
All 32 coordinate directions are positive under V3 from $10^{-5}$ to $3\times10^{-2}$;
the remaining ones lie between $0.21$ and $0.66$. Random directions in all 16 angles
($\infty$-norm radius $r$) under V3 have slope at least $1.08$ at $r=10^{-4}$, $0.79$ at
$10^{-3}$ and $0.56$ at $10^{-2}$, with no negative value in 36 samples; under V2 at
$r=10^{-3}$ the least of 30 samples is $0.70$. V2 agrees with V3 wherever it is feasible
and becomes infeasible for most coordinate directions at $r=3\times10^{-2}$, where no
centre box of radius $10^{-2}$ can accommodate the rotation; that is vacuous truth, not
a failure.

Three readings, all exploratory:

- **The derivative signs hold on the whole box.** Slopes change by less than $3$% over
  three decades of radius, so each dual sheet is nearly linear and its curvature is of
  order $0.3$ per squared radian.
  The ratio of softest slope to curvature, $0.0155/0.3$, is about $5\times10^{-2}$,
  which is why a $10^{-2}$ box is within reach and the H-261 ratio ($0.0057/33$) is not.
- **The sliders are not harmless; their domain is.** In every optimum the sliders sit at
  the far end of their domain, so the slider bound rows are active and the theorem must
  state the domain explicitly: the H256 triangle plus the capture margin.
  Square 6 is absent and harmless.
- **Squares 1–8, 15 and 17 are one-sided.** Their directions have slopes $0.21$ to
  $0.55$ from the wall supports, which is the universal support bound in LP form.
  Square 13 no longer needs two fixed-direction premises: its own normal owns $2\to13$.

One discrepancy to resolve: the X-048 receipt gives $-\omega_{11}$ the slope $1/175.8$
on its 58-row cone, while the LP with the slider domain gives $0.088$ and without it
gives $0$. The models differ in how the slides are treated, and the owner of the exact
duals (lane A2) should say which cone the terminal theorem uses.

*Coordinator’s note, 2026-10-02:* the two numbers measure different things, so they are
not in conflict.
The dual optimum $175.8$ from H-261 bounds the coordinate $-\omega_{11}$
along *every* perturbation, with all other non-slider coordinates free: the side grows
at least like $\lvert h_{\omega_{11}}\rvert/175.8$. The LP slope here is the side’s
growth along the single axis $-\omega_{11}$, with the other angles held fixed and only
the centres re-optimised.
It can only be larger.
H-261’s terminal statement uses the full box in all 45 non-slider coordinates, so its
cone is the first. Lane A2’s instrument certifies it over the slider box
$B_W=[0,\tfrac14]\times[0,\tfrac1{12}]\times[-\tfrac18,\tfrac1{16}]$.

## 3. The Premises

**Fixed separating directions follow from feature forcing.** Nonoverlap of two squares
is separation along one of the eight owner-axis options.
If the 135 unavailable options stay negative, each of the 21 contact pairs is separated
along an endpoint zero option, which is the forced-feature premise; the contact need not
be tight. An option’s gap moves by at most $2\sqrt2\,\rho_p$ in the centres, about
$1.41\rho_a$ in the two supports and about $1.5\rho_a$ from the owner’s rotating normal,
so the least margin $0.0558$ (pairs 14/17 and 7/14) survives when
$2.83\rho_p+2.9\rho_a\le0.0558$: uniformly $\rho\le9.7\times10^{-3}$, or
$\rho_p\le1.4\times10^{-2}$ at $\rho_a=5\times10^{-3}$. Two cautions: the H-257 margins
are at the centroid, and the slide of square 11 moves the 3/11 option by up to $0.045$
against its margin $0.147$, so the margins must be re-verified along the family; and the
three axis-aligned faces 1/2, 1/3 and 5/7 need the same owner treatment as the slanted
ones.

**The parallel-face disjunction becomes one row.** Separation along either owner normal,
with the tangential offset bounded by $\tau_{\max}<1/2$ from the centre box, implies
separation along one owner’s normal with support sum at least
$1+(\tfrac12-\tau_{\max})|\varepsilon|-O(\varepsilon^2)$. This is the first-order
review’s two-row reduction at finite radius and removes the $2^9$ enumeration.

**The $15\parallel16$ branch is outside the theorem.** $W_{15}\ge cd+\gamma$ fails only
near $\phi_{15}=-36.6^\circ$, $0.64$ radians from the box.
Within $\rho_a$ the 15/16 pair is separated along $p_{16}$ by feature forcing.
The co-oriented configuration is a different feature set that the global cover and
exclusion step must handle; it is not a case the capture delivers to this theorem.

## 4. Side Range

A dual bound $S\ge\lambda\cdot b(\psi)$ contains no side.
The premise $S\in[4.675,4.676]$ served the hand monotonicity argument, whose signs the
receipts show holding on $S\in[4.66,4.676]$ as well.
In the LP form the side range is simply absent: every $S$ the capture state allows is
covered, and adding $S\le S^{\ast}+10^{-2}$ as a row (V2) changed no value.

## 5. Verdict and Plan

**Plausible, at $\rho_a$ between $5\times10^{-3}$ and $10^{-2}$**, with centres within
$10^{-2}$ of the family and sliders within their domain plus $10^{-2}$. The LP evidence
supports $3\times10^{-2}$; feature forcing sets the smaller figure.

**What an instrument certifies.** For each direction patch $D$ on the sphere of the
seven backbone angles (9, 10, 11, 12, 13, 14, 16), a dual basis $B$ of the LP and the
inequality $S_B(\psi^{\ast}+\rho d)\ge S^{\ast}+\rho\,g_B(d)-\rho^2C_B\ge S^{\ast}$ for
$d\in D$, $\rho\le\rho_a$, where $S_B(\psi)=\lambda_B(\psi)\cdot b_B(\psi)$ is the
sheet, $\lambda_B(\psi)=A_B(\psi)^{-\top}e_S$ the parametric dual, $g_B$ its slope and
$C_B$ an interval bound on its second derivative.
Nonnegativity of $\lambda_B(\psi)$ is checked on the same patch.
The nine other angles enter each sheet through one square’s supports and are handled by
a one-dimensional check that the wall weights dominate, as the universal support bound
does. This is the n11 focused-rectangle argument applied to the angle-only value
function, with the apex handled by the ratio test per patch instead of by subdivision; a
box subdivision would need cells scaled to their distance from $\psi^{\ast}$ and does
not terminate.

**Arithmetic and cost.** Each patch needs one $35\times35$ interval linear solve
(Krawczyk about a floating inverse) and a $7\times7$ interval Hessian of trigonometric
sums over at most 70 rows; exact rationals with outward rounding are affordable at under
a second per patch. The patch count is the uncertainty: the optimal dual face at
$\psi^{\ast}$ has dimension about 17, and the number of sheets that are optimal
somewhere near the apex is unknown.
With $10^3$ to $10^5$ patches the target run is minutes to a CPU-day on one worker, and
the build is one controlled slice plus review, comparable to H-261’s.

**Likely failure points.** The patch count exploding under dual degeneracy; the softest
patch ($\beta$ increasing, slope $0.0155$) having a curvature larger than the coordinate
probe shows; the centroid margins failing along the family; and the $-\omega_{11}$
discrepancy between the LP and the receipt, which would change the softest slope by a
factor of 15 in one direction.

**Interaction with H-261.** At radius $3\times10^{-4}$ the widened theorem’s conclusion
is H-261’s, so a certified widened theorem supersedes it.
Until then H-261 is the terminal theorem and the widened theorem should nest inside its
bead: lane A2’s exact kernel and 90 duals supply the dual bases, and its
slider-uniformity lemma supplies the domain rows.
If the widened theorem certifies, the capture target becomes the feature-forcing region
and the contraction-rate pilot measures against $10^{-2}$ rather than $3\times10^{-4}$;
if it fails on patch count, H-261 plus capture to $3\times10^{-4}$ remains the route and
the pilot is unchanged.

## Evidence Status

| Kind | Items |
| --- | --- |
| Derived here by hand | The LP formulation; the identification of the chain rows with the stress rows; the per-chain rewriting and the $w$-chain losses; the feature-forcing radius; the finite-radius disjunction reduction |
| Exploratory, floating point, this session | All slopes and their constancy in radius; the slider exploits; the random-direction minima; V2 agreeing with V3 |
| From the record | The 135 margins and $\kappa_\infty$ (X-048 receipts); the derivative-sign boxes (`route-endpoint.txt`); $W_{15}$ and $W_{17}$ windows (`route-derivs.txt`); offsets $\tau$ (first-order review) |
| Open | The $-\omega_{11}$ slope discrepancy; the patch count; margins along the family |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
