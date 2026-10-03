---
title: n17 Capture Feasibility by Local Radius
date: 2026-10-02
status: planning-review
---
# n17 Capture Feasibility by Local Radius

**Session:** 167, BC-406, lane D. **Baseline:** main after PR 265 and PR 269.
**Question:** what does the capture step of an n11-style optimality proof cost for n17,
as a function of the local theorem’s certified radius, and must the radius be enlarged
before any capture work?

The [route review](review-2026-10-01-n17-route-after-pr265.md) deferred capture until
the H-261 radius and an endpoint-adapted cover exist, and its stop condition says to
open interval enlargement along $\omega_{11}-\omega_{12}$ and $\omega_{16}$ if the
certified radius falls below $10^{-4}$. This review prices capture from the n11 record
and from two exploratory probes, and separates what is measured from what is modelled.
It changes no bound, verdict or frontier field.

## Summary

- **n11’s capture was cheap and reached radii of the n17 scale.** Its ten geometry nodes
  replay in about two CPU-hours.
  Its local rectangle had per-coordinate radii between $6.5\times10^{-4}$ and
  $6.8\times10^{-3}$, not $1/64$, and the captured state filled 50–99% of those radii.
  Its finest angle rows were $1.3\times10^{-4}$ wide in $t$, the resolution n17 needs.
  The n17 target of $3\times10^{-4}$ is between 1.5 and 16 times finer than what n11
  delivered, depending on the coordinate, not fifty.
- **Capture cost depends only weakly on the radius.** The engine contracts by rounds of
  angle-row pruning with one-sided position bounds; rounds grow like $\log(1/r)$ and
  per-update cost with the number of live rows.
  Going from $r=3\times10^{-3}$ to $3\times10^{-4}$ adds about 40% more rounds and about
  a factor two in rows.
  The cost drivers are the number of leaves and the contraction rate, neither of which
  the radius controls.
- **Interval enlargement is cheap but does not change the capture problem.** Enlarging
  two weak directions to $10^{-2}$ needs a few hundred centred LP boxes, but the other
  43 coordinates stay at $3\times10^{-4}$, so capture must still get there.
  Enlargement in all 45 coordinates is impossible by box covering at any radius.
- **The architecture that lifts the requirement is a widened conditional theorem.** The
  projection theorem eliminates positions along contact chains and needs only angles and
  forced features. Widened to angle offsets of about $10^{-2}$ it would make the capture
  target the feature-forcing region, radius about $2\times10^{-2}$, which is coarser
  than what n11 reached.
- **Recommendation.** Lane A2 should certify H-261 at the best radius the first-order
  ratio allows, about $3\times10^{-4}$, and stop there.
  The next capture item is a contraction-rate pilot on the endpoint’s own occupancy
  state (positive control), run beside a W3 slice that scopes the widened conditional
  theorem. Enlargement is not a precondition.

## 1. What n11’s Capture Did and Cost

Measured from the record; every number has a source.

**Mechanism.** The n11 capture is an ownership induction
([PROOF.md](../../../packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md),
section 5, lines 232–287): each owner keeps closed half-angle rows, each with residual
centre polygons, and an owned hull of points inside the square for every surviving pose.
An update intersects a row’s legal centre domain with the complement of the partners’
hull-minus-core regions and universal collision kernels, then promotes new owned points.
Rows whose residual empties die.
The tree branches only on closed predicates (PROOF.md, lines 498–513): $y_{15}\le5/4$,
$t_{13}\le147/512$, $t_2\le183/512$. Three far leaves end in contradictions; the near
leaf’s final state is enclosed in the local rectangle by convexity (lines 515–522).

**Shape.** Ten geometry nodes, depth four (root, r1, r11, r111, near), four leaves, 453
owner updates in all, 136 live rows and 1,542 vertices at the end
([census contract](review-2026-09-29-n11-optimality-census-contract.md), lines
2397–2421).

| Node | Updates | Rows checked | Collision inequalities | Wall s | Workers | Source |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Root, 14 rounds | 154 | 16,551 | — | 718 | 3 | round receipts; [optimality review](review-2026-09-29-n11-optimality.md) lines 53–74 |
| Root node, 14 steps | 14 | 2,402 | 31,570,192 | 1,083 | 1–3 | contract lines 1253–1276, 1514–1550 |
| r1 | 9 | — | — | 117 | 2 | contract lines 1695–1718 |
| far15 | 8 | 1,585 | 0 | 66 | 1 | contract lines 1943–1956 |
| r10 | 13 | 1,996 | 0 | 164 | 1 | contract lines 1958–1969 |
| near13 | 44 | 7,852 | 0 | 623 | 1 | contract lines 2046–2058 |
| far13 | 24 | 4,034 | 11,277,080 | 494 | 1 | contract lines 2127–2140 |
| r11 | 7 | 1,245 | 6,004,752 | 232 | 1 | contract lines 2210–2223 |
| far2 | 11 | 1,855 | 4,702,168 | 226 | 1 | contract lines 2267–2286 |
| r111 | 48 | 8,258 | 13,850,000 | 727 | 1 | contract lines 2307–2320 |
| near | 121 | 119,372 | 7,568,064 | 303 | 3 | contract lines 2399–2409 |

Wall times are the receipts’ `wall_seconds` under
[`receipts/`](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/).
Summing wall time times workers gives at most 7,300 CPU-seconds, about **two
CPU-hours**, in **1.3 hours of wall time**; several nodes did not measure process CPU.
That is the checker replay.
The producer’s discovery cost (choosing splits, orders and kernels) is not public (route
review, line 304), and it is the larger unknown.

**Radius reached.** The local rectangle’s radii, per owner $(r_x, r_y, r_\theta)$ in
unit coordinates and radians, come from the accepted
[pose-inclusion receipt](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/pose-inclusion/result.json):
positions from $6.5\times10^{-4}$ to $3.3\times10^{-3}$, angles from $1.5\times10^{-3}$
to $6.8\times10^{-3}$. PROOF.md line 425 says only that all lie within the $1/64$
working box. The near state’s achieved half-extents, read from the receipt’s derived
state (exploratory probe, part 1), are $4.3\times10^{-4}$ to $2.1\times10^{-3}$ in
position and, for the five slanted squares, $1.0$–$4.9\times10^{-3}$ in angle, filling
0.50–0.99 of the corresponding radius.
Its live rows are $1.3$–$5.1\times10^{-4}$ wide in $t$ over an adaptive partition of
674–1,052 rows per owner.
The capture stopped when inclusion held, not because it stalled; nothing in the record
says how much further it could have gone.

**Per-exclusion comparison.** A nonfield exclusion cost about 640 CPU-seconds (contract
lines 2376–2380); the whole capture cost about ten of those.

## 2. The n17 Target

Facts from the route review and the
[X-048 receipts](../../../packing/campaign/explorations/X048-route-review/README.md),
exploratory unless noted.

- The local theorem is on 45 non-slider coordinates, with square 6 entirely free and
  squares 5, 11 and 13 sliding over domains of $0.024$–$0.11$ (route review, lines
  218–239). The 52 positive rows have rank 45 and a 6-dimensional kernel; the probe
  reproduces this (part 2) and finds the slide direction of squares 11 and 13 to be
  $v=(0.640,-0.768)$ with a residual of $10^{-16}$.
- The n11-style ratio is $0.86$ at uniform radius $3\times10^{-4}$, $1.43$ at
  $5\times10^{-4}$, $2.86$ at $10^{-3}$, $8.6$ at $3\times10^{-3}$, binding at
  $-\omega_{11}$ with dual coefficient $175.8$ and $\lVert\lambda\rVert_1=921$
  (`endpoint-n17_radius.txt`). Anisotropy does not help much: $(r_{\rm pos},r_{\rm
  ang})=(10^{-3},3\times10^{-4})$ gives $1.99$. The ratio is linear in the radius, so
  the certifiable uniform radius is about $3.5\times10^{-4}$.
- The first-order conical slope is $\kappa_\infty=1/175.8=0.0057$ side per unit
  $\infty$-norm; n11’s is $0.0518$ (exp-227), nine times larger.
- The 135 unavailable owner options have margins of at least $0.056$
  (`endpoint-n17_more.txt`), so the H257 feature set is forced on a neighbourhood of
  radius roughly $10^{-2}$ to $3\times10^{-2}$, far larger than the local radius.
- Square 9’s centre is $0.0012$ below an H259 seam (route review, lines 164–170), so on
  that grid the endpoint family straddles two occupancy states.

**Correction to the brief.** The comparison “n11 near $1/64$, n17 near $3\times10^{-4}$,
fifty times smaller” compares n11’s analytic working box with n17’s certified radius.
Measured extent to required radius, n17 needs angles 3–16 times finer and positions
1.5–7 times finer than what n11 captured, and the same row resolution n11 already used.

## 3. A Cost Model for n17 Capture

**Where the contraction comes from.** The probe (part 2 and 3) ran hull consistency on
the linearised cones, $Ah\ge0$ on a symmetric box: 52 positive rows for n17 and the 42
rows of n11’s branch 0 (built from `cases.trump11.tangent_cones`). Neither contracts at
all; the box is a fixed point after one sweep, while an LP on the same cone pins every
coordinate to zero. So the n11 engine’s power is not per-row linear propagation.
It is the combination of one-sided bounds (walls, and chains from them), exact hull
geometry, and above all the angle rows: inside a row of width $w$ the angle contributes
$w/2$ rather than the whole domain, positions then contract to that scale, and rows die.
The angle width of an owner shrinks only through its partners’ widths, by a geometric
factor $g$ per round; the splits are what to do when a domain is bimodal.
Capture is therefore a branch-and-prune over angles with cheap propagation in positions,
and its cost is

$$
\text{cost}\approx L\cdot N_{\rm rounds}\cdot n_{\rm owners}\cdot c_{\rm update},
\qquad N_{\rm rounds}\approx\frac{\ln(w_0/r_\theta)}{\ln(1/g)},
$$

with
$c_{\rm update}\propto(\text{live rows})\times(\text{partner rows})\times(\text{facets})$.

**Calibration from n11.** $w_0=\pi/4$, final angle half-widths about $2\times10^{-3}$,
about 35 rounds along the near path: $g\approx0.84$ per round on average.
Near-stage updates cost 7–15 CPU-seconds (near, r111, near13), root-stage updates up to
75\.

**n17 entries.** Owners: 16, since square 6 appears in no positive row and can keep a
coarse angle partition; its three coordinates and the slides of 5, 11 and 13 are
quotiented by the product form of the theorem.
Pairs: about 40 contact-adjacent pairs against n11’s 14, so $c_{\rm update}$ is taken as
three times n11’s at equal rows.
Row resolution: $r_\theta=3\times10^{-4}$ rad is $1.5\times10^{-4}$ in $t$, about
$1/8192$, the width of n11’s finest rows; n11’s partition was already adaptive
(674–1,052 rows per owner rather than the 8,000 a uniform partition would need), so the
row count per update is taken as one to two times n11’s. Leaves: two occupancy states on
the H259 grid (one if H-263 picks a cover that holds the family), times the angle
splits; n11 needed three splits and four leaves with 11 squares, so 4–16 leaves per
occupancy state is assumed.
D4 is handled before capture by the bridge, as in n11.

| Radius $r$ | $t$ resolution | Rounds | $c_{\rm update}$ (CPU-s) | Per leaf (CPU-h) | 8–32 leaves (CPU-h) |
| --- | --- | ---: | ---: | ---: | ---: |
| $3\times10^{-4}$ | 1/8192 | 45 | 60 | 12 | 100–400 |
| $10^{-3}$ | 1/2048 | 38 | 45 | 8 | 60–240 |
| $3\times10^{-3}$ | 1/1024 | 32 | 30 | 4 | 35–140 |
| $10^{-2}$ | 1/256 | 25 | 30 | 3 | 27–110 |

Each factor is uncertain by about three times, so the totals are order-of-magnitude.
If the engine could not keep the partition adaptive and had to carry 8,000 rows per
owner at the finest radius, the first row would grow by roughly twenty times.
Three things the table does not contain:

1. **Stall.** If $g$ approaches one in a soft mode, rounds grow without bound and the
   capture stops above $r$. n17’s slope $\kappa_\infty$ is nine times smaller than
   n11’s, which is the reason to expect slower contraction, but the probe shows the
   linear cone does not predict $g$; only a pilot measures it.
2. **Producer cost.** Discovery of splits and orders is unpriced for n11.
3. **Seam cost.** A second occupancy state doubles everything above it; the H-263 cover
   removes the doubling.

The radius enters only through rounds and rows.
From $3\times10^{-3}$ to $3\times10^{-4}$ it adds 40% to the rounds and about a factor
two to the rows; the whole span of the table is a factor four per leaf.
Leaves and $g$ dominate.

## 4. Radius Target and the Enlargement Question

**Where enlargement is cheap.** A sub-box centred at distance $d$ from the family along
a non-slider direction is excluded by an LP at its centre when $\kappa_\infty d$ exceeds
the stress remainder $C_\sigma\rho^2$, with $C_\sigma\approx33$ side units per squared
$\infty$-norm radius, read from `endpoint-n17_radius.txt` (the “stress remainder” column
divided by $r^2$). That gives a lateral box radius $\rho<0.013\sqrt d$. Enlarging $k$
coordinates from $r$ to $R$ then needs about $(76\sqrt R)^k$ boxes per shell: for $k=2$
and $R=10^{-2}$ about 60 per shell and a few hundred in all, each an exact LP on 52
variables and 58 rows.
For $k=45$ it is $(2.4)^{45}\approx10^{17}$ already at $R=10^{-3}$. Enlargement is
affordable only in a handful of directions.

**Why it does not relieve capture.** The ratio test couples every coordinate: the
curvature term of the $-\omega_{11}$ certificate sums over rows touching most squares,
so the box must stay near $3\times10^{-4}$ in all 45 coordinates for that certificate to
hold. Enlarging $\omega_{11}-\omega_{12}$ and $\omega_{16}$ to $10^{-2}$ leaves 43
coordinates where capture must still reach $3\times10^{-4}$. Since capture cost is
logarithmic in the radius and the engine refines angle rows adaptively anyway, a
two-direction enlargement buys at most the two softest coordinates’ last few rounds.
It becomes valuable only if a pilot shows the contraction stalling specifically in those
directions, which is the one case where it unblocks capture at low cost.

**Affordability threshold.** Under the model, capture is under $10^3$ CPU-hours at every
radius in the table, with a margin of about two at $3\times10^{-4}$ and of about seven
at $3\times10^{-3}$ against the stated uncertainty.
The threshold is therefore not a radius; it is $g<0.9$ and at most a few dozen leaves.
If a pilot finds $g>0.95$ at the $10^{-3}$ scale, the n11 architecture is the wrong
engine for n17 regardless of $r$.

**Radius target.** Lane A2 should certify at the largest rational radius vector with
ratio below one, about $3\times10^{-4}$ uniform or slightly anisotropic (angles
$2.5\times10^{-4}$, positions $4\times10^{-4}$), and not spend effort pushing beyond.
The slider domain of the theorem should be the capture’s expected enclosure of the H256
triangle plus margin, since $A(w)$ is affine in the slider parameters.

## 5. Alternative Architectures

| Alternative | What it would prove | Soundness | Cost | Assessment |
| --- | --- | --- | --- | --- |
| **Intermediate theorem on the feature-forced region, certified by the H-258 stress** | $S\ge S^{\ast}$ wherever the H257 features are forced | A stress at a point is a KKT condition on the contact manifold only; off the family it certifies nothing without a remainder bound, which returns the Taylor radius. Along the family itself it is the right certificate (uniformity over sliders) | Small, but limited to the family | Not a route to a larger radius; keep as the slider-uniformity lemma inside H-261 |
| **Capture into the conditional projection theorem’s box, premises widened** | $S\ge S^{\ast}$ for packings whose features are forced and whose angles lie within $\delta$ of the endpoint angles, positions unconstrained | Sound if the chain inequalities are re-proved on a product of angle intervals rather than at exact common orientation, with the 15-parallel-16 branch recorded. Positions are eliminated by the chains, so no position radius is needed beyond feature forcing | An interval or monotonicity proof in about 17 angle variables on a box of radius $\delta$; derivative signs are constant on the current frozen box (projection review) and the exploratory scan grows linearly over all common orientations, so iterated monotonicity is plausible on $\delta\approx10^{-2}$ | **Most promising.** It raises the capture target to angles within $\sim10^{-2}$ and positions within the feature-forcing margin ($\sim2\times10^{-2}$), about $1/256$ in $t$, a resolution n11 passed early. The open risk is the widening proof itself |
| **Capture in the quotient by the slider family** | The same statement in 45 coordinates | Already the product form of H-261; the engine handles translational slides as segment residuals and square 6 as a coarse owner | None beyond stating the theorem that way | Necessary bookkeeping, not a cost change |
| **Interval enlargement along two weak directions** | H-261 on a box enlarged to $10^{-2}$ in $\omega_{11}-\omega_{12}$ and $\omega_{16}$ | Sound by centred LPs with remainder bounds | A few hundred exact LPs | Cheap insurance against a directional stall; not a precondition |

The widened conditional theorem is also the only alternative that reuses the n11
pipeline unchanged: capture to $1/256$ resolution is what n11’s root rounds already did
(777–2,036 rows across 11 owners).
Its deliverable is a theorem, so the route review’s deferred row “strengthen the
conditional theorem” should be selected on the ground it names: a capture step that
needs a wider target in angle directions.

## 6. Recommendation

1. **Lane A2 (H-261):** certify at about $3\times10^{-4}$, anisotropic if the exact
   duals allow, with uniformity over a slider domain equal to the H256 triangle plus a
   margin of the same order as the radius.
   Record the per-coordinate radius vector; it is the capture target if the conditional
   route fails.
2. **Next capture item, before any enlargement:** a contraction-rate pilot (OR-1) that
   adapts the n11 v9 kernel to one n17 occupancy state, the endpoint’s own, with square
   6 coarse and sliders as segment residuals, and measures per round the live-row count
   and angle width per owner, the per-update CPU, and the radius at which progress
   stops. Its falsifier: $g>0.95$ at the $10^{-3}$ scale, or more than 16 splits before
   reaching $10^{-3}$. This pilot is also the positive control for BC-410 and BC-411.
3. **In parallel, a W3 slice** that scopes the widened conditional theorem: list the
   chain inequalities as functions of all 17 angles, check derivative signs on an angle
   box of radius $10^{-2}$ around the endpoint, and decide between iterated monotonicity
   and an interval branch-and-bound.
   If the signs hold, the capture target becomes the feature-forcing region and the
   radius question closes.
4. **Open the two-direction enlargement only** if the pilot stalls in
   $\omega_{11}-\omega_{12}$ or $\omega_{16}$ specifically.

## Evidence Status

| Kind | Items |
| --- | --- |
| Measured from the n11 record | Node inventory, wall times, worker counts, update and row counts; the per-owner local radii; the 2,180-exclusion batch cost |
| Exploratory, from the probe in this session | n11 achieved half-extents and live-row widths; n17 kernel, slide direction and zero columns; the null contraction of linear hull consistency for both cases |
| Exploratory, from X-048 receipts | Ratio values, dual coefficients, $\kappa_\infty$, $C_\sigma$, unavailability margins |
| Derived here, needing review | The cost model and its table; the $(76\sqrt R)^k$ box count; the claim that the widened conditional theorem needs no position radius beyond feature forcing |
| Assumed | $g\approx0.84$ carries over from n11; 4–16 angle leaves per occupancy state; update cost three times n11’s at equal rows; D4 handled by a bridge as in n11 |

The probe script and its output are in the session scratchpad
(`scratchpad/lanes/d/capture_probe.py` and `capture_probe.out`), outside the record for
the same reason as the X-048 scripts: the lint floor admits no unlinted Python under
`packing/`. Every number from it is planning evidence until an admitted instrument
reproduces it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
