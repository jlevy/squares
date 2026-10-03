---
title: n17 Capture After the Pilot
date: 2026-10-02
status: planning-review
---
# n17 Capture After the Pilot

**Session:** 168, BC-418, lane R5. **Reviewed:** the capture pilot
`packing/devtools/pilot_n17_capture.py` (`e22ca457`) and its receipts under
[X048-session-168-pilots](../../../packing/campaign/explorations/X048-session-168-pilots/README.md)
(`receipts/capture-*.json`), at `cea300a4`. **Question:** the pilot met the
[capture feasibility review](review-2026-10-02-n17-capture-feasibility.md)’s falsifier,
position contraction $g=1.000$ at every scale.
Is that a property of n11’s ownership-induction architecture or of this producer, and if
the architecture is wrong, what replaces it?

**Recomputation:** one floating-point probe of my own, `lanes/r5/pairwise_probe.py` in
the session scratchpad with its logs, which runs an idealised pairwise propagation and
an LP on the first-order cones of n17 (the 58 H-258 rows from
`check_n17_core_stress.common_rows`) and of n11 (the 42 rows of branch 0 from
`cases.trump11.tangent_cones`). It is planning evidence, outside the record for the
usual reason: the lint floor admits no unlinted Python under `packing/`. This review
changes no bound, verdict or frontier field.

## Summary

- **The falsifier was met by the producer, not the architecture.** On the first-order
  cone, an idealised pairwise induction with the pilot’s row budget (24 live rows per
  owner) leaves every position at the box for 23 rounds, then crawls at $g=0.85$–$0.95$.
  With 48 live rows it contracts from round 15 at $g\approx0.82$, with 96 from round 12
  at $g\approx0.70$, and the rate is the bisection rate of the rows, not a property of
  the cone. The pilot ran 14 rounds at 24 rows.
  Its $g=1.000$ is what the model predicts for that budget.
- **Positions follow the angle rows, about ten rows to the position scale.** In the
  model, contraction begins when the widest live row is about a tenth of the position
  extent, and at the fixpoint for a given row width the extents are about 12 times the
  row width in position and 28 to 36 times in angle (square 11 is the worst).
  n11’s cone gives 20 to 33 and contracts at $g=0.50$ in the same model.
  The pilot’s rows never got below a quarter of the extent for axis squares, or below
  the extent itself for the tilted ones, at either box radius.
- **The soft slope $1/175.8$ sets the row width capture needs, not whether capture
  works.** Pinning $\omega_{11}$ to $r=1/5000$ needs rows about $r/36\approx5.6\times
  10^{-6}$ rad wide, close to lane C1’s $2^{-18}$. The model shows that rows that fine
  do pin it; the claim that even then $g\ge0.994$ is not supported.
- **Three producer losses are first order in the row width and add to the model’s own:**
  the envelope core (half the row’s half-width per core, in every direction), the
  16-vertex owned-hull cap, and the one-sided measurement.
  The eight-direction outer domain is harmless, because the producer’s partner covers
  use the exact residual hulls; self-hull cuts therefore change nothing in the model.
- **Of the alternative routes, none replaces the kernel; one shortens it.** The widened
  conditional theorem raises the angle target from $2\times10^{-4}$ to about
  $5\times10^{-3}$ and the position target to $10^{-2}$, which saves about five
  bisection rounds, and C1’s turn data does not yet reach its radius (three owners stall
  at $1.8$–$4.2\times10^{-2}$ rad).
  An LP per angle box with interval coefficients loses first order on the eleven
  corner-to-edge rows and closes a box only when its radius is about $D/3500$ of its
  distance $D$; the Taylor-at-centre form that fixes this is the dual-sheet instrument,
  so routes (a) and (b) are one route.
  A lower cap changes nothing the model does not already run at $\varepsilon=0$.
- **Recommendation:** a second capture pilot with the four producer fixes and a sharper
  falsifier: if, with every owner’s widest live row under a twentieth of its position
  extent for three rounds, no two-sided position extent falls by ten percent, the
  architecture is wrong.
  Beside it, the n11 case-438 state through the same producer, which the pilot never had
  as a contraction control.

## 1. What the Receipts Show

Read from `capture-main-box1024.json`, `capture-main-box64.json` and
`capture-control-U-box1024.json`; measured, in unit coordinates.

**Wall sides are pinned exactly, and nothing else arrives.** At $U'$ the wall-touching
coordinates sit at $-2.24\times10^{-13}=-(U'-S^{\ast})/2$ from the family in every
round: the centred clipping of the kernel spec’s section 4.1 is implemented as
specified. At the exclusion cap $U$ the same sides sit at $-2.35\times10^{-4}=-\sigma$,
the family’s offset from the container wall, so the two frames differ exactly as they
should; the README’s “positions identical” refers to the deviation measure, which is the
same because it takes the larger of the two sides.

| Owner | Round 0 low, high in $x$ (or $u$) | Round 14 | Turn at 14 | Widest row ($t$) |
| --- | --- | --- | ---: | ---: |
| corner-SW (1) | $[-2\times10^{-13},\ 9.77\times10^{-4}]$ | unchanged | $2.2\times10^{-3}$ | $2.44\times10^{-4}$ |
| side-S0 (2) | $[-9.77\times10^{-4},\ 9.77\times10^{-4}]$ | $[-2.77\times10^{-4},\ 9.77\times10^{-4}]$ | $2.2\times10^{-3}$ | $2.44\times10^{-4}$ |
| side-W2 (9) | $[-9.77\times10^{-4},\ 9.77\times10^{-4}]$ | $[-5.48\times10^{-4},\ 9.77\times10^{-4}]$ | $1.77\times10^{-2}$ | $9.77\times10^{-4}$ |
| side-N2 (16) | $[-9.77\times10^{-4},\ 9.77\times10^{-4}]$ | unchanged | $4.21\times10^{-2}$ | $1.95\times10^{-3}$ |

Three readings follow.

- **Lower bounds propagate one link from the walls, with the envelope core’s loss.**
  Square 2’s lower side moved from $-9.77\times10^{-4}$ to $-2.77\times10^{-4}$ over 14
  rounds, still falling.
  The envelope core of a row of half-width $\delta$ in angle has side
  $1/(\cos\delta+\sin\delta)\approx1-\delta$ (`counting.row_envelope`), so each core
  loses $\delta/2$ in half-width in every direction, and a link uses two cores: at the
  final row width of $4.9\times10^{-4}$ rad that is $2.4\times10^{-4}$, which is what
  arrived at square 2.
- **No upper bound reaches any non-wall side.** Every high side off a wall stays at
  $+9.77\times10^{-4}$. The chains that would carry one (for square 2, the right wall
  through 17, 14 and 13 along $u$) pass through tilted squares, whose rows are
  $9.77\times10^{-4}$ to $1.95\times10^{-3}$ wide in $t$ at the live-row cap of 24.
  Since the deviation is $\max(|{\rm low}|,|{\rm high}|)$, one-sided progress never
  registers as $g<1$.
- **Turns stall where the wall meets the box.** For an axis square at a wall,
  $h(\theta)-\tfrac12\approx\theta/2$ must fit the box’s $\rho$, so turns stop at
  $2\rho$: $2.2\times10^{-3}$ at $\rho=1/1024$ and $3.5\times10^{-2}$ at $1/64$, as
  measured. A tilted square at a wall has $h'(\theta^{\ast})=(\cos-\sin)/2=0.064$, so its
  turn stops near $\rho/0.064=16\rho$: side-W2 at $1.77\times10^{-2}$. Angles and
  positions limit each other at the same scale, which is why the stall looks the same at
  both radii.

## 2. The Probe

The question is whether a pairwise induction can contract at all here, so the probe
models the best one possible and asks what it does.

**Model.** Each owner holds angle slabs, each slab a convex centre polygon, starting
from a box of radius $P=10^{-3}$ and slabs over $[-W,W]$, $W=0.05$ rad.
Each first-order row $a\cdot z\ge-a_\sigma\varepsilon$ is enforced between one owner’s
slab and the partner’s whole pose set: the owner’s polygon is cut by the halfplane that
holds for *some* angle in the slab and *some* partner pose, which is the kernel’s row
residual (an outer bound on the union over the row).
Tied row pairs (W$\mp$, E$\mp$) are enforced jointly, so wall bounds on a slab
containing the endpoint angle are lossless, as `wall_lines` makes them.
The partner side uses the exact polygon, as `producer.partner_cover` uses the exact
residual hull. The owner’s next input is its eight-direction outer domain
(`SUPPORT_NORMALS`), optionally kept tight along the owner’s own axes, which is what
self-hull cuts do. Rows are bisected up to a live-row cap, as the pilot’s `refine` does.
Square 6 is coarse and never updated.
Everything is homogeneous, so the scale $P$ is immaterial and $\varepsilon=0$ is the
hardest case. Pairwise ownership induction can do no better than this: every one of its
rules (forbidden regions from owned hulls, universal collision, self-hull cuts) bounds
one owner’s poses from one partner’s pose set.

| System | Live rows per owner | Owner input | Outcome |
| --- | ---: | --- | --- |
| n17 | 8 or 64 fixed slabs, no refinement | exact | stall: $g=1.000$ in position and angle from round 2 |
| n17 | 24, refined | 8-direction and self cuts | positions at the box for 23 rounds, then $g=0.85$–$0.95$ (round 40: $3.4\times10^{-4}$) |
| n17 | 48, refined | exact | contraction from round 15, $g\approx0.82$; $2.7\times10^{-6}$ at round 39 |
| n17 | 96, refined | exact, or 8-direction with or without self cuts | contraction from round 12 at $g\approx0.70$, identical in all three; $8.5\times10^{-8}$ at round 40 |
| n17 | 400, refined | 8-direction and self cuts | contraction from round 12 at $g=0.61$–$0.68$; $1.75\times10^{-7}$ at round 30 |
| n17 | 96, refined, $\varepsilon=4.49\times10^{-13}$ | 8-direction and self cuts | as at $\varepsilon=0$ to the probe’s row-width floor ($5.5\times10^{-8}$ at round 60); the cap slack is invisible at these scales |
| n17 | 96, refined | 8-direction rounding applied to the partner side too | stall at the box |
| n11 | 96, refined | any of the three | contraction from round 8 at $g=0.50$ |
| n11 | 24, refined | exact | contraction from round 8 at $g=0.50$ |

Four things the table says.

1. **There is no fixpoint above zero for either system.** Contraction continues as long
   as rows are refined, down to the probe’s floor of $10^{-9}$ rad.
   The rate is the refinement rate: $0.50$ when every live row splits each round (n11,
   where about 25 rows per owner are live), $0.71=\sqrt{1/2}$ when the cap lets half of
   them split (n17 at 96, where about 65 are live), and $0.61$–$0.68$ at 400 rows, where
   the rows that die at the edges of the live range each round are what limits the
   halving.
2. **Positions wait for the rows.** The n17 extents at a given row width settle at about
   12 times the widest live row in position and 28 to 36 in angle (square 11, the
   softest, is 36); n11’s are 20 to 33. Contraction begins once the widest row is about
   a tenth of the position extent.
   At 24 rows that condition is reached only at round 24, at 96 rows at round 12.
3. **The owner-side rounding costs nothing; partner-side rounding is fatal.** The
   eight-support outer domain inflates a sliver’s support along $u^{\ast}$ (at
   $39.8^{\circ}$, between axis and diagonal) by about 18 percent of its length, a
   scale-free loss. Applied to the owner’s own input it is re-cut each round and has no
   effect; applied to what partners see it stops everything.
   The producer keeps partners exact, so this is not the pilot’s problem, and self-hull
   cuts, which carry an owner’s own-axis supports through the rounding, are not the
   missing ingredient.
4. **The LP pins everything at once.** With $\varepsilon=0$ the LP on the same rows
   gives zero extent for every non-slider coordinate, angles in a box of any radius; the
   induction needs rows to get there.
   That is the architectural gap, and it is a cost, not a wall.

**Why the dual-norm argument overstates the row width.** C1’s reading is that a contact
cycle gains $\delta/176$ against per-link losses, so rows must be about $2^{-18}$ wide.
The dual with $\lVert\lambda\rVert_1=921$ bounds what uniform row losses $\ell$ allow:
$|\omega_{11}|\le921\,\ell$. The probe’s losses are one-sided and correlated along
chains, and the measured constant is 36 rather than 230; pinning $\omega_{11}$ to
$r=2\times10^{-4}$ needs rows of about $5.6\times10^{-6}$ rad, which is $2^{-17.5}$. The
width is right; the conclusion that fine rows still give $g\ge0.994$ is not what the
model shows, because at that width the extents are that small.

**What the model leaves out, and which way each item points.** It is first order; at
$P\le10^{-2}$ the quadratic terms are below $10^{-4}$ of the linear ones.
Its cores are ideal, where the pilot’s envelope core loses $\delta/2$ per core and its
owned hulls are capped at 16 vertices; both are first order in the row width, so they
raise the constants (perhaps by two to four) without creating a fixpoint.
The calibration is n11: the record’s $g\approx0.84$ against the model’s $0.50$ says the
real kernel, with its real producer, is about four times slower in log-rate.
The same factor on n17’s $0.70$ gives $g\approx0.91$, under the falsifier’s $0.95$ but
not by much, and the figure is an extrapolation.

## 3. Verdict on the Falsifier

**Producer-limited, with moderate-to-high confidence in the mechanism and moderate
confidence in the rate.** The four questions of the brief:

- **Can positions contract when owned hulls come only from what the cell certifies?**
  Yes. The hulls are not the limit: by round 1 every owner’s hull has area $0.99$, the
  unit square shrunk by $\rho$. The limit is the row width relative to the position
  extent, which the live-row cap fixes at a quarter (axis squares) to one (tilted
  squares) in both pilot runs, where the model needs a tenth.
- **What would self-hull cuts, branch predicates, finer rows and uncapped live rows
  change?** Self-hull cuts: nothing, in the model (section 2, item 3). Branch
  predicates: nothing for contraction; they are for bimodal residuals, and no residual
  in the receipts has two components.
  Finer rows and more live rows: everything.
  The minimum width $2^{-16}$ in $t$ was never reached; the cap of 24 was binding for
  every owner in every round.
- **Is the box seed a fair stand-in for post-split states?** Yes, and conservative.
  The centred box is the hardest start, since walls cut only one side of it and the
  model is homogeneous; a post-split child is asymmetric and inherits one-sided bounds.
  One correction to the measurement: the deviation should be reported per side, since
  the pilot’s lower sides moved and the metric could not show it.
- **Are the $U'$ frame and the wall clipping right?** Yes, by the wall-side values in
  section 1, and the $U$ control differs from $U'$ by exactly $\sigma$ on those sides.
  The cell-seed runs (`capture-try-b32-g64.json`) contracted nothing because 13 of 17
  owners owned no point and all 544 rows stayed live; that is the reach problem the
  sub-pattern lanes already met, not a capture result.

What is not shown: that the exact kernel, with the producer fixed, reaches $g<0.95$. The
n11 calibration says it should, at about $0.9$, and only the next pilot measures it.

## 4. Alternative Routes

Each route is assessed on soundness, on the measurement that decides it, on cost, and on
how it composes with the capture-target theorem’s three obligations from the
[composition review](review-2026-10-02-n17-local-half-composition.md): the frame
(embedding A, the packing’s corner at $(\sigma,\sigma)$), the cap ($U'$ within
$10^{-12}$ of $S^{\ast}$), and the charging of $u^{\ast}$'s enclosure to its own radius
rather than to $r$.

### (a) The Widened Conditional Theorem

**Statement.** Every packing in the endpoint’s feature set with angles within $\rho_a$
of the endpoint’s and centres within $10^{-2}$ has $S\ge S^{\ast}$
([widened projection scope](review-2026-10-02-n17-widened-projection-scope.md), verdict:
plausible at $\rho_a=5\times10^{-3}$ to $10^{-2}$).

**Does it close the gap?** It moves the target, it does not remove capture.
Capture must still deliver angles within $\rho_a$ and centres within $10^{-2}$ for every
packing of side at most $U'$ in the state, from the cells.
The angle target is 25 times coarser than $r$, which by the model’s constant of 36 means
rows of $1.4\times10^{-4}$ rather than $5.6\times10^{-6}$ rad: about five fewer
bisection rounds, in line with the feasibility review’s “logarithmic in the radius”.
C1’s turn data does not yet support the radius: at $\rho=1/1024$ the turns of side-N2,
side-N0 and side-W2 stall at $4.2$, $1.9$ and $1.8\times10^{-2}$ rad, above $10^{-2}$,
and at $1/64$ at $0.23$–$0.26$. Those stalls are the row-cap stalls of section 2, so the
data neither supports nor refutes the radius; it is silent.

**Composition.** The theorem is a dual bound and carries no side, so the cap obligation
is unchanged: capture runs at $U'$ in embedding A, and the state’s packings of side at
most $U'$ must land in the angle box and the $10^{-2}$ centre box.
The angle box is around the exact root’s angles, so the $u^{\ast}$ enclosure is charged
as before. The feature-forcing premise adds a fourth obligation: the capture state must
show every one of the 135 unavailable options still negative, which at $10^{-2}$ the
H-257 margins give but which must be re-verified along the slider family (the scope
review’s caution).

**What decides it.** The patch count of the dual-sheet instrument; the scope review puts
the run at minutes to a CPU-day once built and the build at one slice plus review.
Worth doing for its own sake, since it supersedes H-261’s radius, but it does not change
whether the kernel route works.

### (b) LP-Based Contraction over Angle Boxes

**Two forms, with different losses.** Branch on the angles, decide the centres by one LP
per box, close a box when the LP is infeasible at cap $U'$.

- *Interval coefficients*, as `pilot_n17_subpattern_bb.py` does: every row’s support is
  replaced by its least value over the box.
  On the nine parallel-face pairs the loss is second order, as the tool’s docstring
  says. On the eleven corner-to-edge rows (`smooth` in the stress receipt) the support
  $(|\cos a|+|\sin a|)/2$ moves at $0.064$ per radian, a first-order loss.
  A box of radius $\rho$ at distance $D$ along $-\omega_{11}$ gains $D/176$ in side and
  loses about $\sum_{\rm smooth}\lambda_r\cdot0.064\rho\approx20\rho$ against the H-261
  dual, so it closes only when $\rho\lesssim D/3500$. In sixteen angle dimensions the
  shell at distance $D$ then needs of order $(3500)^{15}$ boxes.
  This is not a capture method for the endpoint state; it certified pattern A because
  A’s margin is $1.5\times10^{-2}$ and collective, not $1/176$ and soft.
- *Taylor at the box centre*: linearise the supports at the centre, so the first-order
  term is exact and the loss is the second-order remainder, about $33\rho^2$ side per
  squared radius (`endpoint-n17_radius.txt`, the stress remainder).
  A box closes when $D/176>33\rho^2$, that is $\rho<\sqrt{D/5800}$, which at
  $D=2\times10^{-4}$ allows $\rho\approx D$. Boxes of radius comparable to their
  distance cover a shell with $O(2^{16})$ boxes, and about ten dyadic shells run from
  the cell scale to $r$. That is the dual-sheet certificate of the scope review with the
  patches chosen by subdivision rather than by direction, and it meets the same obstacle
  the scope review names: a subdivision scaled to the distance from the apex does not
  terminate at the apex, which is why the apex is handled by H-261’s ratio test instead.

So route (b) in its sound form is route (a)'s instrument extended outward, plus the
option disjunctions the branch-and-bound already handles.
Its soundness is the branch-and-bound pilot’s (Farkas multipliers checked with outward
rounding), its composition is (a)'s, and what decides it is a Knuth estimate of the tree
under the Taylor relaxation, which the pilot’s `--estimate` can give once the relaxation
is swapped. **Cost to find out:** a few days of build on the existing tool, then an
estimate run of minutes.
It does not reuse the n11 checkers, so admission would need its own review.

### (c) A Lower or Second Cap, and Far Leaves

The model already runs at $\varepsilon=0$, the hardest cap, and contracts; the cap is
not the obstacle. The residue process review’s far leaves (section 5.5) are the same
engine on asymmetric seeds, which the model says contract faster than the centred box.
Their count is lane Q1’s to measure; their cost per leaf is the near leaf’s. Not a
route; a part of the kernel route’s policy, and the right home for branch predicates if
a residual ever goes bimodal.

### (d) Other Candidates

- **An LP cut inside the kernel:** add, per owner per round, the halfplane the LP gives
  on its centre over all partners’ live ranges, certified by Farkas multipliers as a new
  region kind. Rejected: with angles as whole live ranges the interval-coefficient loss
  is about 20 times the range, worse than the kernel’s own row-wise treatment, and the
  row-slab structure is what makes the kernel’s loss local.
- **Rows as adaptive partitions with no cap**, which is what n11’s near state had (674
  to 1,052 rows per owner, `pose-inclusion/result.json`). This is not an alternative to
  the kernel; it is the kernel used as n11 used it, and the recommendation.

## 5. Recommendation: The Next Capture Pilot

**Slice: capture pilot 2, the producer fixed and the control added.** One lane, two to
three days, runs under a wall ceiling.

1. **Rows.** Raise `--max-live` to 128 and 256, bisect every live row wider than the
   floor rather than only up to the cap, and lower the floor to $2^{-22}$ in $t$. Report
   per owner the widest live row over the position extent, the ratio the model says must
   fall below about $1/10$ before positions move.
2. **Cores.** Replace the envelope square by the intersection of the two end-angle
   squares of the row (an octagon, strictly inside both and inside every angle between
   by convexity of the support), still passed through `strict_core`; the loss along each
   face normal becomes second order in the row width.
   Keep the envelope as a `--core envelope` option so the two can be compared on the
   same seed.
3. **Hulls.** Raise `--hull-limit` to 48 or drop it, and record the area lost by
   `bounded_vertices` per step.
4. **Measurement.** Report low and high per coordinate and per owner, and define $g$ on
   the two-sided extent and on each side separately.
   Keep the endpoint control and the replay.
5. **Control.** Run the same producer on n11’s case-438 state from its cells in the
   `n11` frame, which the pilot lacks as a contraction control, and compare its $g$ with
   the record’s $0.84$ and with the model’s $0.50$. That ratio calibrates the model’s
   n17 constants to the real kernel.

**Runs.** The $\rho=1/1024$ box at $U'$ at 128 and 256 rows, and the n11 control, each
under a three-hour ceiling; the $1/64$ box if time allows.
At the pilot’s 3.5 s per update with 24 rows and cost growing with rows times partner
rows, 128 rows is about 25 times slower, 90 s per update, so three hours buys about
seven rounds of sixteen owners: enough to pass the one-tenth threshold, which the model
puts at round 12 from $W=0.05$ with 96 rows and earlier from the pilot’s already
contracted turns.

**Falsifier.** If, for three consecutive rounds, every contracting owner’s widest live
row is under a twentieth of its position extent and no owner’s two-sided position extent
falls by ten percent, the architecture is wrong and the widened-theorem instrument
becomes the route. If positions contract, record $g$ per round after the threshold and
the extent-to-row ratio at which they started; the model’s figures to beat are $0.70$
and $1/10$, and the calibrated expectation is about $0.9$.

**What the cost model becomes if it passes.** Rounds: about $\log_2$ of the ratio of the
starting angle width to the final row width, $5.6\times10^{-6}$ rad, from the cells’
$\pi/4$: about 17 bisections, at $g$ per round once the rows are fine.
Rows: about twice the angle-to-row constant, 60 to 100 live per owner at the end, which
is below n11’s. Per update: n11’s near-stage 7 to 15 CPU-seconds at those row counts,
times about three for the pair count, so 20 to 50 CPU-seconds; 16 owners, 40 to 60
rounds, one occupancy state: 4 to 13 CPU-hours per leaf, inside the feasibility review’s
100 to 400 CPU-hours with room for leaves.

## Evidence Status

| Kind | Items |
| --- | --- |
| Measured, from the receipts | Wall-side values at $U'$ and $U$; per-owner ranges, turns, widest rows and live-row counts; hull areas; the one-link lower-bound propagation |
| Derived here, from the record | The envelope core’s $\delta/2$ loss and its match to square 2’s lower side; the $2\rho$ and $16\rho$ turn stalls; the $\sigma$ difference between the two caps |
| Exploratory, from the probe | Every entry of the section 2 table; the constants 12, 28 to 36 (n17) and 20 to 33 (n11); the one-tenth threshold; the partner-side rounding result; the LP’s zero extent |
| Derived, needing review | That pairwise induction can do no better than the probe’s model; the $D/3500$ and $\sqrt{D/5800}$ box conditions; the identification of route (b)'s sound form with the dual-sheet instrument |
| Extrapolated | The real kernel’s $g\approx0.9$ for n17 from the n11 ratio $0.84/0.50$; the cost model of section 5 |
| Open | Whether the exact kernel with the fixed producer contracts; the widened theorem’s patch count; the far-leaf count (lane Q1) |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
