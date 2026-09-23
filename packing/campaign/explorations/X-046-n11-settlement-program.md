---
title: X-046 — an n11 settlement program, priced
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-046
  title: An N11 Settlement Program, Priced
  date: '2026-09-23'
  author: Claude Fable 5.1 at max reasoning, W3 key-insight lane; not yet reviewed by the coordinator
  campaign: packing.squares
  brief: >-
    Owner goal for the session: find what would significantly push n11 forward or
    conclusively settle it. Asked whether any provable route beats a verified global
    search over the 33 pose coordinates; to design the H-112 milestone concretely
    with its generalization ladder; to attack the whole program adversarially; and
    to rank three overnight lanes. Generate freely, certify nothing, keep exploratory
    compute under about twenty minutes.
  sources:
  - operating-rules.md
  - packing/frontier/n-011.md
  - packing/cases/trump11/isolation-theorem.md
  - packing/cases/trump11/packing.py
  - packing/cases/trump11/independent_lp_cell.py
  - packing/campaign/explorations/X-045-n11-global-capture-and-exact-optimality.md
  - packing/campaign/explorations/X-043-new-lower-bound-proof-directions.md
  - packing/campaign/explorations/X-018-hybrid-strength-and-angular-release.md
  - packing/campaign/hypotheses/H-112-six-axis-five-common-angle-optimum.md
  - packing/campaign/hypotheses/H-113-at-most-two-angle-optimum.md
  - packing/campaign/hypotheses/H-120-rank-nine-release-exclusion.md
  - packing/campaign/hypotheses/H-121-axis-plus-one-minimizer.md
  - packing/campaign/hypotheses/H-131-near-axis-counts-at-q.md
  - docs/project/reviews/review-2026-09-10-n11-structural-normal-forms.md
  - docs/project/reviews/review-2026-09-07-n11-hybrid-strategy.md
  - docs/project/reviews/review-2026-09-22-kleddamag-n11-mathematics.md
  - packing/resources/papers/stromquist-2003-packing-10-or-11-unit-squares.md
  - packing/resources/web/external-square-certificates-2026-09-22/kleddamag-11/global-certificate.json
  - packing/campaign/agent-sessions/session-153-native-full.json
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-204-basin-hopping.md
  - packing/src/sqpack/fractional/parent_core.py
  - packing/src/sqpack/fractional/parent_core_interval.py
  - packing/src/sqpack/uniform_cell.py
  - packing/src/sqpack/exact_lp.py
  - packing/src/sqpack/research/quench.py
  - packing/devtools/run_basin_hopping.py
  - attic/x046/probe_a_growth_cone.py (gitignored scratch, this block)
  - attic/x046/probe_b_rows_at_u.py (gitignored scratch, this block)
  - attic/x046/probe_c_census.py (gitignored scratch, this block)
  - attic/x046/probe_d_path_back.py (gitignored scratch, this block)
  proposes: [H-236, H-237, H-238, H-239]
---
# X-046: An N11 Settlement Program, Priced

No dimension-reduction lemma examined here is both provable with current tools and
strong enough to remove angle dimensions.
The angle-merging normal form (H-121) is the conjecture in another form, not a lemma on
the way to it. What can be proved is a **ladder of restricted-family theorems** in one
and then two angle parameters, each a strengthening of Stromquist’s 0°/45° theorem, and
each rung’s cost is set by the fixed-angle cell enumeration rather than by the angle
dimension. Settling $s(11)=U$ outright needs the far region of the 11-dimensional angle
space closed as well, and whether that is a one-week computation or an impossible one
turns on two measurable constants named below, not on anything now in the record.

Four bounded float probes were run in gitignored scratch.
They measured the first-order angular growth of the fixed-angle optimum at Trump
(flattest coordinate direction 0.066 per radian, square 10 turning clockwise), read
Kleddamag’s certificate at container side $U$ (the per-row minimum charge collapses by
68% at the axis angle and by 1–2% at Trump’s tilt, so the certificate carries no
transferable slack), and quenched 59 perturbed Trump poses.
Every three-orientation endpoint the quench reported within $0.005$ of $U$ lies on a
monotone descent path back to Trump, so the census instrument over-reports local minima
and the only minima observed within $U+0.0085$ are Trump’s orbit and Stromquist’s 45°
family, at Stromquist’s value $2+4\sqrt2/3$ to nine decimals.

## What the Probes Measured

All four probes are exploratory `f64` computations in `attic/x046/`; none is a retained
measurement, and `OR-1` says which of them deserve a tool.

| Probe | Question | Result |
| --- | --- | --- |
| A, growth cone | One-sided rates $(f(\theta^*+hd)-U)/h$ per radian at $h=10^{-4}$; coordinate directions and the common tilt minimized over the 2,048 raw separating-axis cells containing Trump’s pose, the composite directions in the read cell only | Coordinate rates: sq0 0.139/0.164, sq1 0.458/0.542, sq2 0.411/0.194, sq3 0.458/0.458, sq4 0.458/0.542, sq5 0.230/0.273, sq6 0.238/0.299, sq7 0.312/0.301, sq8 0.674/0.210, sq9 0.402/0.301, sq10 0.134/**0.066**; common tilt 0.384/0.175 (H-019’s 0.3841/0.1747 reproduced); all six axis squares together 1.06/1.08 |
| B, certificate at $U$ | Kleddamag’s rows, sites, weights and cores unchanged; container enlarged from $191/50$ to $(764/775)\cdot3877084/10^6$, ratio $3.877084>U$; per-row minimum charge on 18 rows by the retained box search in enclose mode | Drop from the $999{,}962{,}528$ threshold: 68.2% at $u=0$; 22–39% for $u\le0.023$ (tilt $\le2.6°$); 5–12% for $u\in[0.06,0.15]$; 0.8–2.5% for $u\ge0.19$; 1.69% on the row adjacent to Trump’s half-tangent $0.365769$ |
| C, census | 59 `quench_bracket` runs from Trump: 15 single-square angle releases, 3 double releases, 40 random jolts of every centre and angle at scales 0.02–0.3 | 24 return to $U$ (13 of 16 jolts at scale $\le0.05$, then 2/8, 1/8, 1/8); Stromquist’s $3.885618083$ reached seven times; six endpoints at $U+0.0017$ to $U+0.0049$ with six axis squares, four at a common tilt $40.4°$–$40.9°$, and one square alone (square 10 five times, square 7 once) |
| D, descent check | From each of those six endpoints, walk the straight line in angle space to Trump’s angles in 24 steps, re-optimizing centres by the LP-in-cell fixed point | All six decrease monotonically to $U$ with zero rise; they are class-coordinate stalls of the quench, not local minima |

Probe A’s rates are upper bounds on the growth of the all-cell optimum, since only
Trump-containing cells were enumerated.
Probe B’s per-row values are exact charges at admissible witnesses and bound the
enlarged-container minimum from above on those rows only.
Probes C and D say nothing about regions the jolts did not reach; in `exp-204`, 200
refined optima from uniform scatter reached no side below $3.897$.

## Facts the Program Stands On

Proved or verified in the record:

- $31/8<s(11)\le U=3.87708359002281417\ldots$, the exact root of Trump’s degree-8
  polynomial; Kleddamag’s certificate replayed by two complete methods
  ([n-011](../../frontier/n-011.md)).
- All 128 derivative-distinct fixed-side tangent cones at Trump are zero, so Trump is
  locally isolated at fixed side and strictly locally side-optimal (exp-013,
  registered).
- The BC-240 packet quantifies this in the labelled anchored 33-coordinate sup-norm
  chart: radius $\rho_{\text{row}}=808514697/2\cdot10^{11}$ and, on the uniform pass,
  modulus $\kappa=0.011480\ldots$, remainder constant $K=4972105219/5\cdot10^8$ and
  radius $\rho_u=2\kappa/K=288616983/1.25\cdot10^{11}$
  ([isolation theorem](../../cases/trump11/isolation-theorem.md)), accepted at
  retained-record-dependent scope.
- Normal form S1: at any feasible side, every fixed-angle feasible component contains a
  representative whose contact components touch the left and bottom walls with a 22-row
  true-contact basis
  ([structural normal forms](../../../docs/project/reviews/review-2026-09-10-n11-structural-normal-forms.md)).
- Stromquist’s Theorem 3: eleven squares oriented only at 0° or 45° need side at least
  $2+4\sqrt2/3=3.885618\ldots=U+0.008534$
  ([source](../../resources/papers/stromquist-2003-packing-10-or-11-unit-squares.md)).
- Eleven axis-parallel unit squares need side at least 4 (the nine-mark argument in the
  [hybrid review](../../../docs/project/reviews/review-2026-09-07-n11-hybrid-strategy.md)),
  and the angular transfer inequality $f(\theta)\ge f(\alpha)/(\cos\delta+\sin\delta)$
  when every actual orientation is within $\delta$ of $\alpha$'s
  ([X-045](X-045-n11-global-capture-and-exact-optimality.md)).

Derived in this block from those facts, not reviewed:

- **Angular growth floor inside the ball.** For a feasible pose in the uniform-pass ball
  with displacement $v$ and side $U+\sigma$, the modulus supplies a row with
  $a_jv\le-\kappa\|v\|_\infty$ and the remainder bound gives
  $\sigma e_j\ge\kappa\|v\|_\infty-(K/2)\|v\|_\infty^2$; a row with $e_j=0$ is then
  infeasible outright, so
  $\sigma\ge(\kappa/2)\|v\|_\infty\ge0.0057\,\|\Delta\theta\|_\infty$ whenever
  $\|v\|_\infty\le\rho_u/2=0.00115$. In particular there is no first-order flat angle
  direction at Trump; probe A’s rates sit ten to a hundred times above this floor.
- **Free boundary strips for one-parameter families.** With every square within $\delta$
  of the axis, transfer from the axis floor 4 gives $f\ge4/(\cos\delta+\sin\delta)\ge U$
  for $\delta\le0.032228$ rad ($1.8465°$). With every square within $\delta$ of the
  0°/45° pattern, transfer from Stromquist gives $f\ge U$ for $\delta\le0.002204$ rad
  ($0.1263°$).

## Is There a Better Route Than a Thirty-Three-Dimensional Search?

Each mechanism below is stated with the lemma it would need, why it might hold, what
kills it, and the smallest test.

| Mechanism | Precise lemma | Why it might hold | Falsifier | Smallest test | Verdict |
| --- | --- | --- | --- | --- | --- |
| Angle vertex argument (S1 for angles) | Some global minimizer has every square either a rotational rattler or rotationally blocked in one direction at fixed centre | Rotate each square at fixed centre to the end of its feasible angular interval; compactness | None expected; it follows from compactness | Write the proof | True, useless for dimension: a vertex-edge point contact blocks rotation without equating angles, so no class merges |
| Angle merging (H-121) | Some global minimizer has at most one non-axis class | Fewest-classes selection plus a finite side-nonincreasing merging path | A rigid three-class local minimum on every candidate path | None that is cheaper than the theorem | Not a lemma: if $s(11)=U$ it holds with Trump; if not, it is a claim about an unknown optimum. Retire as a route, keep as a corollary |
| Rattler elimination | Some minimizer has no translational or rotational rattler | S1 plus rotational quenching | None | Proof | True, no reduction |
| Forced wall and corner structure below $U$ | At most three squares per wall, four distinct corner blockers, at least two squares more than $1.7°$ from the axes | Already proved in the record | — | — | Too weak: it fixes no angle class and no five-square block |
| Symmetry breaking | Quotient by $Z/2\times S_{11}$ on angles (rotations act trivially on angles modulo a quarter turn) and by $Z/4\times S_6\times S_5$ on the 6+5 family | Standard | — | — | Constant factors only: $2\cdot11!$ and $345{,}600$ |
| Counting-forced localization (X-045 mode A) | A certificate at side $U$ with excess $\varepsilon=M-11\Gamma$ forces every square into $\{q\le\Gamma+\varepsilon\}$ | The 31/8 certificate has relative excess $10^{-5}$ | A fractional packing of mass 11 supported off the Trump roles | Probe B and the localization LP below | Probe B says the retained certificate is wall-brittle and cannot be read at $U$; a $U$-targeted certificate needs an optimizer the repository does not have (the external search is not retained; in-repo column generation tops out near 3.827) |
| Rigid sub-assembly within 0.0021 of $U$ | Every packing with side $\le U$ contains six near-axis squares and a five-square block at a common tilt | Probes C and D found nothing else within $U+0.0085$ | A verified $\ge3$-class local minimum below $U+0.0085$ | Census with a descent filter (lane 2) | Plausible as a fact, unreachable as a theorem by one-body counting; it is the bridge statement, discussed below |
| Angle-profile certificates (candidate H-a) | For an angle set $B$, every packing with a square oriented in $B$ has side $>U$ | Stromquist’s Theorem 3 is exactly such a theorem for the profile “all squares in $\{0°,45°\}$”, and it beats $U$ | The profile LP’s dual: a fractional packing using $B$-oriented poses at side $U$ | Formulate the LP on the retained T-025 atoms at $191/50$ and read its dual | Open; the only known success is a profile with two exact angles |

Two conclusions follow.
First, nothing here removes an angle dimension by proof, so the exact-family ladder is
the only theorem-producing route available now.
Second, the far region can only be closed by counting-type profile theorems or by a
search whose relaxation is coarse enough, and neither has been priced.

### The Two Constants That Price a Full Search

A verified search over the angle box $[0,\pi/2)^{11}$ covers it with boxes and closes
each by a rigorous bound $f\ge U$ over the box.
Write $c$ for the side lost per radian of box width by the relaxation, and
$V(\varepsilon)$ for the volume of the sublevel set $\{f\le U+\varepsilon\}$ modulo
$Z/2\times S_{11}$. A box at a point where $f-U=\varepsilon$ needs width about
$\varepsilon/c$, so the box count is roughly
$\int V'(\varepsilon)\,(c/\varepsilon)^{11}\,d\varepsilon$: exponential in $c$, and
dominated by wherever $f$ is close to $U$.

- **Near Trump** the local theorem is the terminal leaf, and probe A gives the rates.
  With first-order relaxations the shells outside the ball cost about
  $\prod_i(c/\kappa_i)$ per shell; probe A’s minimum rates give
  $\prod_i1/\kappa_i\approx6\times10^6$ before the factor $c^{11}$. This is the cluster
  problem of global optimization (Du and Kearfott 1994; Wechsung, Schaber and Barton
  2014), and its known remedy is a second-order convergent bound: a fixed dual
  certificate from the box centre, with the centre coordinates also boxed, loses
  $O(w\cdot|\text{centre box}|)=O(w^2)$ near a vertex minimizer.
  With such bounds the shell sum converges and the near-Trump region costs on the order
  of its outermost shell, an estimated $10^5$ boxes.
- **Far from Trump** the cost is $V(\varepsilon)$ against $c$. A relaxation that treats
  each row independently over an angle window of width $w$ loses, by a rough count of
  corner displacements, around $3w$ to $4w$ in side, which at $f-U\approx0.2$ forces
  $w\approx0.05$ and about $4\times10^8$ boxes even before refinement.
  A better relaxation is exact: replace each square by its **rotational core**, the
  intersection of the square over its angle window, an octagon with corners cut to depth
  about $0.35w$. Every true square contains its core, so a packing at any angles in the
  box is a packing of the cores, and the core problem is a fixed-shape polygon packing
  whose cells are again exact LPs, with eight candidate separating axes per pair instead
  of four. The loss is first order; corner cuts of depth $0.35w$ propagating through
  contact chains of three or four squares suggest a constant near 1, unmeasured.
  If so, at $w\approx0.15$ the coarse cover is on the order of $10^3$ boxes.

Neither $c$ for the core relaxation nor $V(\varepsilon)$ has been measured.
Both are cheap: $c$ from the core LP at a few angle vectors and widths, $V$ from the
distribution of the fixed-angle optimum over random angle vectors.
Until they are, “settle by search” is priced between a week and never, and every lane
below is chosen to be worth running under either answer.

## The H-112 Milestone

**Statement.** Let $\mathcal F_{6,5}(\theta)$ be the packings of eleven unit squares in
which six have actual orientation $0$ and five share the actual orientation $\theta$,
modulo quarter turns, with centres and contacts free.
Then $\min\{S:P\in\mathcal F_{6,5}(\theta),\ \theta\in[0,\pi/4]\}=U$, attained only on
the $Z/4\times S_6\times S_5$ orbit of Trump’s pose at $\theta=\theta^*$. One reflection
of the container folds $\theta$ into $[0,\pi/4]$; the family at $\theta=0$ is the axis
family and at $\theta=\pi/4$ lies inside Stromquist’s class.
Comparisons with $U$ are decided exactly: every leaf bound is rational and $U$ is
irrational, so “bound $\ge U$” is the strict comparison through $U$'s isolating
interval.

**Domain.** Use the half-tangent chart $t=\tan(\theta/2)\in[0,\tan(\pi/8)]$, in which
corner coordinates are rational, matching the certificate machinery.
The strips $\theta\le1.8465°$ and $\theta\ge45°-0.1263°$ are closed by the transfer
corollaries above without any computation.

**Per-box decision.** For a box $[t_a,t_b]$, build each square’s rotational core (for
the axis squares this is the square itself), enumerate separating-axis cells by a
branch-and-bound that branches on the pair most violated by the current LP solution, and
close each leaf by an exact rational Farkas infeasibility certificate or an exact dual
bound above $U$, produced by `sqpack.exact_lp` and replayed by an independent reader in
the style of `uniform_cell_check`. The cores make the bound valid for every angle in the
box with no interval arithmetic inside the LP; only the core’s construction from the box
endpoints needs exact rational geometry, which `parent_core.validate_parent_core`
already does for square cores.
Symmetry-breaking rows order the axis squares by centre and fix the tilted block’s
centroid quadrant.

**The Trump box.** Cells containing a Trump image stay feasible at side $\le U$, so they
close only by the local theorem: refine the box containing $t^*$ until its angle width
and the LP’s centre enclosure at side $\le3877084/10^6$ both lie within $\rho$ of the
matched labelled Trump image.
Because the fixed-side feasible set at $t^*$ is the single point $z_*$ in each such
cell, the enclosure shrinks with the box; the growth floor above bounds the true
feasible set at side $U+4.1\times10^{-7}$ to sup-diameter $7\times10^{-5}$ inside the
half ball, and the relaxed enclosure exceeds that only by the box’s relaxation loss.
Boxes adjacent to the Trump box carry margins $0.175h$ and $0.384h$ at distance $h$ on
the two sides of $t^*$ (probe A, the family’s one parameter), so refinement toward $t^*$
is geometric and about 20 boxes deep on each side.

**What is automatic and what it costs.** Everything except the cell-tree driver exists:
exact LP with certificates, uniform cell descriptors and their reader, rational cores,
the exact witness and the local theorem.
The unknown is the cell-tree size per box.
BC-095’s $2\times10^8$ LP figure priced a different grammar and is not evidence here; an
eleven-body fixed-shape tree with violated-pair branching is expected at $10^3$ to
$10^5$ LPs per box.
With 200 to 2,000 boxes that is $10^5$ to $10^8$ LP solves plus exact
replay: CPU hours to days, and one to three weeks of engineering.

**First two-hour slice (Rung 0).** Build the cell-tree driver with float HiGHS proposals
and exact leaf certificates, control it on $n=5$ in the family “four axis squares and
one at $\theta$” at a box around $45°$ against the proved $s(5)=2+1/\sqrt2$, then run it
on the single box $t\in[t^*-10^{-6},t^*+10^{-6}]$ for $\mathcal F_{6,5}$. The
machine-checkable exit is a certificate file listing every leaf with its cell and its
exact Farkas or dual vector, accepted by the independent reader, together with the
Trump-degenerate leaves closed by the local theorem.
A bounded negative is equally valid output: the list of unresolved leaves with their
bounds and the node count.
Either way the slice prices the tree, which is the only unknown in the milestone.

**The ladder.**

| Rung | Family | Angle parameters | What it proves | Cost order |
| --- | --- | --- | --- | --- |
| 0 | $\mathcal F_{6,5}$ on one box around $t^*$ | 0 | Trump is globally optimal at its own angle: the first global optimality statement in any $n=11$ family | One cell tree |
| 1 | $\mathcal F_{6,5}$, all $\theta$ (H-112) | 1 | Any improvement on Trump has a different multiplicity or more classes | $10^2$–$10^3$ boxes |
| 2 | Axis plus one angle, $m=1..11$ tilted squares | 1 each | Any improvement uses two distinct non-axis orientations | 11 rungs like 1 |
| 3 | Two arbitrary orientations (H-113) | 2 | Any improvement has at least three orientations: Stromquist’s Theorem 3 with $\{0°,45°\}$ replaced by every pair | $10^4$–$10^5$ boxes per multiplicity |
| 4 | Three orientations | 3 | The first rung that meets the far region | Priced by $c$ and $V$ |

Each rung also yields **tubes**: wherever a box is closed with margin $\mu>0$, transfer
thickens the exclusion to every packing whose orientations are within $\delta$ of the
box’s exact pattern, $\cos\delta+\sin\delta\le1+\mu/U$. After rung 1 this gives the
first explicit exclusion region of positive 11-dimensional measure around the 6+5
family, with the ball covering the margin-zero end.

## Adversarial Check

- **A genuine three-class minimum near $U$.** The strongest threat to the profile and
  tube picture. Probe C produced six candidates within $U+0.005$ and probe D dissolved
  all six. The census only sampled jolts of size up to 0.3 about Trump; a distant
  three-class minimum below $U+0.0085$ would leave rungs 0–3 true but make rung 4
  mandatory and defeat one-body profile theorems at that sharpness.
  Lane 2 is the cheap falsifier, but only after the instrument is repaired:
  `quench_bracket` returns `converged=True` with reason “converged, 3 classes, free pass
  clean” at class-coordinate stationary points that are not local minima, which its
  docstring permits (cyclic coordinate search over classes) and which any census
  consumer must filter.
- **Stromquist’s class at $3.8856$.** It is a second local minimum of $\mathcal F_{6,5}$
  at $\theta=45°$, attained, with rotational rattlers (probe C reached the same side
  with an axis square at $1.5°$–$3.5°$, thirteen contacts, not converged).
  For rung 1 it is harmless: the margin $0.0085$ prunes boxes of width about $0.0085/c$
  there, and the transfer strip covers the endpoint.
  For a profile theorem it fixes the required sharpness: any one-body statement about
  “not Trump’s profile” must resolve $0.0085$.
- **Cell-tree explosion.** If rung 0’s single box needs more than $10^6$ nodes, the
  ladder is repriced or abandoned; nothing else in the program is at risk from this.
- **Centre enclosure conditioning.** The ball needs centre enclosures within
  $\rho=0.004$; if the LP’s enclosure over a box grows like $100w$, rung 1 needs boxes
  of width $4\times10^{-5}$ near $t^*$, still only logarithmically many in one
  dimension, but squared for rung 3.
- **Flat directions.** Excluded at first order by the zero cones; the floor derived
  above is quantitative but small ($0.0057$ per radian), and probe A’s measured rates
  are the operative numbers.
  Second-order flatness is ruled out with them.
- **Labelled matching.** The ball is stated for one labelled anchored chart; every
  Trump-degenerate leaf must be matched to one of the $4\cdot6!\cdot5!$ images by exact
  comparison, and the cover must be shown to reach each image’s leaf.
  Symmetry-breaking rows reduce this to a handful of leaves but the argument that they
  lose no packing is part of the theorem.

## Candidate Hypotheses

Local labels, not identifiers.

| Candidate | Claim | Smallest discriminator | Falsifier | Information |
| --- | --- | --- | --- | --- |
| H-a, angle-profile certificate | For an explicit angle set $B$ away from $\{0,\theta^*\}$, every packing with a square oriented in $B$ has side $>U$, by a counting certificate whose $B$-rows carry excess above the budget gap | Write the profile LP over the retained T-025 atoms at $191/50$ and read its optimal dual | A dual fractional packing using $B$ poses; or excess below the budget gap on every feasible certificate | Whether one-body counting can shape the far region at all |
| H-b, fixed-angle global optimality | Rung 0 holds on a box of half-width $10^{-6}$ in $t$ around $t^*$ | The cell-tree driver | A leaf with rational bound below $U$ that is not Trump-degenerate: a counterexample candidate | Prices every later rung |
| H-c, H-112 by one-parameter cell trees | Rung 1 closes with rotational cores and the ball | Run after H-b | An unresolved box away from $t^*$ after refinement to $10^{-4}$ | The first restricted-family theorem at $n=11$ |
| H-d, angular capture radius | The exact first-order growth cone $g(d)=\min_b\max_{\lambda\in Y_b^*}(-\lambda^\top\rho_b(d))$ over the 128 branches, with $\rho_b(d)$ the first-order change of branch $b$’s active rows along $d$ and $Y_b^*$ its stress cone normalized on the far-wall rows, together with the exact second-order remainder, certifies $f>U$ on an angular ball larger than $\rho$ | 2,816 small exact LPs from exp-013’s stresses and `research/exact_jets` | Radius no larger than $\rho$ | Whether the terminal leaf can be enlarged tenfold, which multiplies through every rung |
| H-e, no third class below $U+0.0085$ | Every descent-stable local minimum with side below Stromquist’s value is in Trump’s orbit | Census with a descent filter from jolted Trump and jolted Stromquist starts | A descent-stable $\ge3$-class minimum below $3.8856$ | The required sharpness of any profile theorem |
| H-f, core relaxation constant | Rotational-core LPs lose at most $1.5$ in side per radian of box width at generic angle vectors, and the fixed-angle optimum exceeds $U+0.2$ on most of angle space | Core LP at 20 random angle vectors and three widths; quench at frozen random angles | $c>3$ or median $f-U<0.1$ | Whether a full verified search is a one-week program or none |

## Lanes for a W6/W7 Loop

| Lane | Model | Question | Entry | First discriminator | Exit | Falsifier | Budget | Files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1, rung 0 instrument | Opus extra-high, Fable extra-high review of the certificate contract | Does a fixed-angle cell tree with exact leaf certificates close the box around $t^*$? | `exact_lp`, `uniform_cell_check`, `cases/trump11`, the $n=5$ control | The $n=5$ control closes | Certificate file plus reader verdict, or the unresolved-leaf list with node count | A non-degenerate leaf below $U$ | 4–6 h | new `packing/cases/trump11/fixed_angle_tree.py` and its reader; results in `attic/` until admitted |
| 2, census repair and landscape | Opus extra-high | Which descent-stable local minima exist below $U+0.02$, and how many orientation classes do they have? | `run_basin_hopping`, probes C and D | The descent filter rejects the six probe-C stalls and accepts Trump and Stromquist | A table of distinct minima with sides, class counts and multiplicities from 1,000 jolted starts | A descent-stable $\ge3$-class minimum below $3.8856$ | 3–4 h | `packing/devtools/run_basin_hopping.py` census mode, a descent-filter module beside `research/quench.py` |
| 3, capture radius and profile LP (high risk, high reward) | Fable extra-high | Can the exact stresses certify $f>U$ on an angular ball larger than $\rho$, and does the profile LP’s dual on retained atoms leave any $B$ excludable? | exp-013 record, `research/exact_jets`, `fractional/threshold` | $g(d)>0$ reproduced on all 22 coordinate faces from the stresses | A theorem-shaped statement with constants for H-d; a go or no-go on H-a from the dual’s support | Radius $\le\rho$; low-charge set covering most of pose space | 4–6 h | new module under `packing/cases/trump11/`, notes in `attic/` |

Lane 3 is the one that can change the shape of the program: a tenfold larger terminal
leaf shortens every rung, and a dead profile LP retires the counting bridge and leaves
H-f as the only route to the far region.
Lanes 1 and 2 are disjoint in files and share only read-only records.
The rotational rattlers of the Stromquist family do not touch rung 1’s equality clause,
since the family value there is above $U$.

## Corrections and Limits

On X-045 and the review of it:

- The review’s equivalence is right: with $s(11)>31/8$ in hand, “every local minimum in
  $[L,U]$ has side $U$” is $s(11)=U$. Its operational residue is the admissibility of
  descent leaves, and probe D is a first use of exactly that leaf type.
- The proposed “certificate side-slope at $U$” was measured (probe B) and is not a
  landscape: the certificate’s leverage sits on the lines of wall-flush parents at the
  exact side, and moving the walls out by $0.001$ removes up to 68% of a row’s charge.
  X-045’s unchanged-core ceiling $3.87501$ is the same brittleness seen from the core
  side.
- The proposed “basin-hopping census of verified local minima in $(U,U+0.02)$” cannot be
  run with the instrument as it stands: uniform starts do not reach the region (exp-204)
  and the quench’s convergence flag is not local minimality (probe D).
- H-112’s first slice should be rung 0, not a full angle interval; and its boundary
  strips are free.
- The rigidity packet’s modulus floor $0.0057$ per radian is a proved statement inside
  half the uniform ball, at the packet’s retained-record-dependent scope; probe A’s
  rates are measurements outside any theorem.

Limits of this block: every number from the probes is `f64` and unretained; probe A is
restricted to Trump-containing cells; probe B samples 18 of 12,028 rows; probes C and D
sample one neighbourhood; no hypothesis identifier is allocated and no bound changes.
Session 156 codified the candidates as H-236 to H-239 and retained probe C and D’s
purpose as a tool, the descent filter behind exp-228.

## Measured Against This Report

Session 156 ran three of the lanes above the same night, and three estimates here were
wrong in ways that change the plan:

- **The cell tree is about a thousand times larger than estimated.** Rung 0’s box needed
  more than $7.8\times10^7$ nodes before its last 79 of 256 subtrees, against the
  $10^3$–$10^5$ LPs per box estimated in “The H-112 Milestone”.
  Each added square multiplies the tree by roughly six or seven (the $n=5$ control
  closes in 229 nodes).
  Rung 1 is out of reach with this relaxation, and the lever is a stronger bound per
  node, not more boxes.
  The instrument itself held up: an independent reader accepted every certificate, and a
  [W2 review](../../../docs/project/reviews/review-2026-09-23-rung0-certificate-contract.md)
  found the contract sound.
- **Candidate H-d cannot beat $\rho$.**
  [exp-227](../series/series-000-smoke-and-calibration/experiments/exp-227-h237-trump-growth-cone-capture-radius.md)
  proves that any certificate bounding each row’s second-order remainder separately is
  capped by BC-199’s weighted modulus.
  The growth minimum over the whole sphere is $0.05177$, and along the binding direction
  36 of 42 rows keep decreasing at second order, so a second-order-exact isolation
  theorem is the route to a larger ball.
  The floor quoted above as $0.0057$ per radian used a far-row constant; the corrected
  uniform-ball floor is $\sigma\ge0.0111\,t$.
- **The census found no third class below Stromquist’s value, but did find two new
  minima within $U+0.02$.**
  [exp-228](../series/series-000-smoke-and-calibration/experiments/exp-228-h238-descent-filtered-census.md)
  filtered 1,000 jolted starts: every one of 85 apparent three-class minima below
  $3.885618$ descends.
  A two-orientation minimum at $3.8867460$ ($0°$ and $41.56°$) and a genuine
  three-orientation minimum at $3.8943219$ set the sharpness any profile theorem must
  reach.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
