---
title: n17 Local Half — Composition of the Local Theorem, the Slide Coverage and the Cover
date: 2026-10-02
status: planning-review
---
# n17 Local Half — Composition of the Local Theorem, the Slide Coverage and the Cover

**Session:** 168 (BC-418), lane R2. **Reviewed:**
`packing/devtools/check_n17_slider_coverage.py` at `05b078bd` (module sha256
`3f698035…`, the digest in lane H2’s `receipt-unique.json`);
`packing/devtools/check_n17_local_minimum.py` at `9c26793c` with
`--ratio --box 0 1/4 -1/2500 1/12 -1/8 1/16` (lane A3’s receipt: 14 checks, 93 cells,
worst ratio $0.925931$ at $-\omega_{11}$), whose only change since the
[instrument review](review-2026-10-02-n17-local-theorem-instrument.md) at `e91bd859` is
the declared box; the H-266 cover accepted in
[exp-247](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-247-h266-n17-unique-state-cover.md);
[H-261](../../../packing/campaign/hypotheses/H-261-n17-local-minimum-modulo-sliders.md)
and
[H-268](../../../packing/campaign/hypotheses/H-268-n17-local-theorem-slider-coverage.md)
as frozen. **Recomputation:** five scripts of my own (`geometry.py`, `lemma_test.py`,
`scan.py`, `witness_check.py`, `amax_fix.py`, with their logs), retained with a `.txt`
suffix under
[exp-248’s `audit/`](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-248-n17-local-half-composition/audit/),
which retype the H-254 layout from the accepted record, read the exp-237 and exp-238
certificates directly, and import nothing from the three instruments.

## Verdict

- **H-268: confirmed on its frozen criterion**, with one deviation to record at
  acceptance. The bounds $a\le\tfrac14$ and $z\ge-\tfrac18$ hold with strict margins
  ($a\le\tfrac{23}{200}$, $z\ge-\tfrac{49}{1000}$), $b\le\tfrac1{12}$ holds
  ($b\le\tfrac{37}{500}$), the controls are refused, and every face is exact or outward.
  The deviation: the claim’s consequence “$B_W$ contains its slider coordinates” is not
  established, because $b\ge0$ is not a consequence of the premises; the 9/11 lemma
  gives $b\ge b^\ast=-1.684957\,r$. The box the composition uses is therefore
  $B_W'=[0,\tfrac14]\times[-\tfrac1{2500},\tfrac1{12}]\times[-\tfrac18,\tfrac1{16}]$,
  and lane A3’s run of the local theorem on $B_W'$ must be recorded as an experiment at
  `9c26793c` before H-268 is marked confirmed.
- **H-261: stays unresolved.** Its claim quantifies over every physically feasible
  slider value of a 17-square packing.
  That domain contains packings outside $B_W'$ on which the certified theorem is silent,
  for instance the family with squares 5 and 6 exchanged ($a\in[1,1.0742]$, square 6 at
  the bottom-right corner, every non-slider coordinate exactly on the family).
  The composition is the capture-target theorem under H-268.
- **No blocking defect** in any of the three instruments or their receipts.
  The composition is sound once one frame is fixed: the packing’s lower-left corner at
  the family’s, $(\sigma,\sigma)$ with $\sigma=(U-S^\ast)/2$, in the cover frame.
  That is a stated obligation on the global half, not a defect in the local one.

## The Slide-Coverage Tool

**The separation lemma.** Two closed unit squares turned by $\omega_A,\omega_B\in[-r,r]$
from the frame $(u,v)$, $v=R(\pi/2)u$, with centre difference $d=Tu+Dv$. Their interiors
are disjoint only if some edge normal $n$ of one square has $n\cdot d\ge h_A(n)+h_B(n)$,
where $h$ is the support; the own square’s support is $\tfrac12$ and the other’s is at
least $\tfrac12$. The eight candidate normals are $\pm R(\omega)u$ and $\pm R(\omega)v$
for $\omega\in\{\omega_A,\omega_B\}$, and $d\cdot R(\omega)u=T\cos\omega+D\sin\omega$,
$d\cdot R(\omega)v=D\cos\omega-T\sin\omega$.

- $\pm R(\omega)u$: $|T\cos\omega+D\sin\omega|\le|T|+|D|\sin r<1\le h_A+h_B$. Excluded
  by the first hypothesis.
- $-R(\omega)v$: needs $T\sin\omega-D\cos\omega\ge1$. From $D>-1+|T|\sin r$ and
  $0<\cos\omega\le1$, $-D\cos\omega<1-|T|\sin r$, so the left side is below
  $|T|\sin r+1-|T|\sin r=1$. Excluded by the second hypothesis.
- $+R(\omega)v$: needs $D\cos\omega-T\sin\omega\ge1$, i.e.
  $D\ge f(\omega)=(1+T\sin\omega)/\cos\omega$.
  $f'(\omega)=(T+\sin\omega)/\cos^2\omega\le(T+\sin r)/\cos^2\omega\le0$ on $[-r,r]$ by
  the third hypothesis, so $f$ is nonincreasing and $D\ge f(r)=\sec r+T\tan r$.

So the lemma holds, and it is sharp: both squares turned by $+r$ and $D=\sec r+T\tan r$
touch along $R(r)v$. `lemma_test.py` samples 700,000 pairs $(T,D,\omega_A,\omega_B)$ in
the hypothesis region below the bound at $r=0.3$, $0.1$, $0.01$ and $1/5000$: every pair
overlaps, the sharp case separates by $0$ to $2\times10^{-16}$, and the least $D$ with
disjoint interiors over the turn corners equals $\sec r+T\tan r$ to twelve digits, at
turns $(+r,+r)$.

**Containment.** A point with nominal-frame coordinates bounded by $H=\tfrac12-2r$ has,
in the frame of the square displaced by $|\delta|\le r\sqrt2$ and turned by
$|\omega|\le r$, coordinate at most $H(|\cos\omega|+|\sin\omega|)+|\delta|\le
H(1+r)+r\sqrt2=\tfrac12-r(\tfrac32-\sqrt2)-2r^2$, which is $\tfrac12-1.72\times10^{-5}$
at $r=1/5000$. The shrunk nominal square lies inside the moved one; the rational inner
rectangle is checked vertex by vertex inside the exact shrunk square over the root box,
and a convex set containing the vertices contains the rectangle.
Strict overlap of two inner rectangles on all four edge normals is interior overlap of
two convex polygons, hence of the real squares.
The $\ell_\infty$ ball of radius $r$ on $(\xi,\eta)$ is inside the disc of radius
$r\sqrt2$; squares 11 and 13 move by $\varepsilon u$ with $|\varepsilon|\le r$, square 5
by $\eta_5$ only, and the slide itself is the rectangle’s offset, so the premise matches
the local theorem’s 45 coordinates.

**$a\ge0$.** $a=x_5^\ast-x_5$ exactly, $x_5^\ast+\tfrac12$ is the family’s right wall
(an identity of the layout, `(side - half, half)`), and the packing’s right wall is at
or left of it; square 5’s reach is $(|\cos\omega_5|+|\sin\omega_5|)/2\ge\tfrac12$. So
$a\ge\tfrac12-h(\omega_5)+(\text{wall gap})\ge0$. It holds in every embedding whose
right wall is at or left of the family’s.

**$b^\ast$ and $z^\ast$.** With $c_9-c_{11}=\tau_0u+D_0v+\delta_9+bv-\varepsilon_{11}u$
the lemma gives
$b\ge\sec r-D_0+\tau_0\tan r-\varepsilon_{11}\tan r+(\tan r\,u-v)\cdot\delta_9$, linear
in the perturbations, least at $\varepsilon_{11}=r$ and
$\delta_9=-r\,\mathrm{sign}(\tan r\,u-v)$: the tool’s formula.
For 11 over 13, $D'=D_1-b-z$ and the same lemma gives
$z\le D_1-b-\sec r-(\tau_1+\varepsilon_{11}-\varepsilon_{13})\tan r$; substituting the
9/11 bound for $-b$ cancels $\varepsilon_{11}$ and leaves the tool’s $z^\ast$. Both
lemma hypotheses hold on the ranges the receipt names (my check at 60 digits).
My layout gives $\tau_0=c(s-1)=-0.276426766820$, $D_0=1$ exactly,
$\tau_1=s-c=-0.128051926457$ and $D_1=1+T/3=1.023737743195$; then
$b^\ast=-3.36991338442\times10^{-4}$ ($b^\ast/r=-1.684956692$) and
$z^\ast=0.0241003249195$, both inside the receipt’s intervals, with $b^\ast$ above
$-\tfrac1{2500}$ by $6.30\times10^{-5}$.

**Branch and bound.** The $(a,z)$ domain is the physical range rounded outward to
$2^{-10}$; every box ends in the target, in a pair closure or in a closure of square 6,
or the run fails (node limit, or a box narrower than $2^{-12}$ that nothing closes).
Square 6 ranges over $\tau=\tan(\phi/2)\in[0,1]$, which is every orientation by the
square’s symmetry, with $\cos\phi$ and $\sin\phi$ monotone and rounded outward to
$2^{-40}$; `six_overlaps` uses lower bounds on both supports and an upper bound on the
projected centre distance, so it only ever under-claims overlap; `six_leaves` uses a
lower bound on the reach.
Square 11 is absent from square 6’s obstacles (conservative, it is far away); squares 5
and 13 keep the face that squeezes 6 whatever the interval width, as the docstring says.
The $(b,z)$ covers are complete over $[b_{\max},b_{\rm hi}]\times[z_{\min},z_{\rm hi}]$.
The chain
$a_z\Rightarrow z\ge-\tfrac1{20}\Rightarrow b\le\tfrac3{40}\Rightarrow b\ge b^\ast
\Rightarrow z\le z^\ast\Rightarrow$ tight $a_z$ with $z\le z^\ast$, $a\ge0\Rightarrow
b\le\tfrac{37}{500}$ has no cycle: each premise is proved for every packing in the
hypotheses before it is used.
The whole-box, no-13 and no-9 controls are refused.

**Independent witnesses.** With the sixteen other squares exactly on the family
(`amax_fix.py`, full 17-square separating-axis check, touching allowed):

| Quantity | Certified | Unperturbed family extreme | Where |
| --- | ---: | ---: | --- |
| $\sup a$ | $\tfrac{23}{200}=0.115$ | $T/s=0.111240$ at $z=T/3$ | square 6 axis-parallel on the bottom wall at the left end of its family box; no tilted pose does better |
| $\inf z$ | $-\tfrac{49}{1000}=-0.049$ | $-0.047475$ at $a=0$ | square 6 on the wall against 5, 13 slid along $-v$ onto it; no tilted pose does better |
| $\sup z$ | $0.0241003$ | $T/3=0.0237377$ | 11/13 contact; the $3.6\times10^{-4}$ is the perturbation allowance |
| $\inf b$ | $-3.3699\times10^{-4}$ | $0$ | 9/11 contact; the allowance is $-1.685\,r$ |

The certified bounds sit $18.8\,r$ and $7.6\,r$ outside the unperturbed extremes, as
they should: the tool lets the sixteen squares move by $r$ and turn by $r$. Along the
family $\sup a$ falls linearly with $z$ ($0.074160$ at $z=0$, $0.000743$ at $z=-0.047$)
and $\inf z$ rises with $a$ ($0$ at $a=0.1$), so the two faces are one
6-between-5-and-13 constraint seen from both ends.

## The Local Theorem on $B_W'$

The diff `e91bd859..9c26793c` adds `--box`, refuses a box that leaves a declared $\tau$
branch before any dual is sought, and allows $b<0$. On $B_W'$ every face stays in its
branch (`c3`: $\tau_{11,12}\in[0.0564,0.1402]$, $\tau_{13,14}\in[0.0181,0.2056]$,
$\tau_{5,7}\in[-\tfrac14,0]$), the 125 option margins stay negative (least $-0.055273$,
at $b=-\tfrac1{2500}$), the stress stays nonnegative, and the ratio test passes on the
same 93 cells, worst $0.925931$ against $0.925818$ on $B_W$. The argument for $b<0$ is
right: the 9/11 face is not a retained row, its offset does not depend on $b$, the
retained rows are tight along $x^\ast(w)$ by C2 as identities in the sliders, and the
curvature constants are bounds over the box.
At $b<0$ the conclusion $x=x^\ast(w(x))$ is vacuous, since the base point overlaps 9 and
11, which agrees with $b\ge b^\ast$. Nothing in the instrument review is disturbed by
the box change.

## The Composition

**Frames.** The local theorem lives in the H-258 frame: the container $[0,S^\ast]^2$
with its lower-left corner fixed, a packing of side $S\le S^\ast$ placed with its own
lower-left corner there.
The slide-coverage tool works in the cover frame $[0,U]^2$, $U=\tfrac{1169}{250}$, with
the family embedded concentrically, so its corner is at $(\sigma,\sigma)$,
$\sigma=(U-S^\ast)/2=2.3495\times10^{-4}$, and it takes the packing’s corner to be the
same point: its container bound is $[\sigma,U-\sigma]$ and $x_5^\ast+\tfrac12=U-\sigma$
is what `a_floor` checks.
Call this embedding A. Under A the two neighbourhoods coincide (both are translates by
$(\sigma,\sigma)$ of the same set), the slides are the same functions of the packing,
and the cell premise is stated in the frame in which the state is read.
Every packing of side $S\le S^\ast$ can be so embedded, since
$[\sigma,\sigma+S]^2\subset[\sigma,U-\sigma]^2$. Two other embeddings are tempting and
neither works unchanged: the concentric one, $(U-S)/2$, moves the packing by
$(S^\ast-S)/2$ relative to the family, so closeness within $r$ there is closeness within
$2r$ in the local theorem’s frame, beyond the certified radius; the origin one,
$[0,S]^2$, is offset from A by $\sigma=1.17\,r$. The obligation on the global half is
therefore to read the occupancy state with the packing’s lower-left corner at
$(\sigma,\sigma)$, or to re-run the slide coverage with square 6’s cell enlarged by the
offset it uses. Only $a\ge0$ is immune, needing just that the packing’s right wall is at
or left of the family’s.

**Root box.** The exp-237 certificate’s `box.midpoint` and `inclusion_bounds` are
byte-for-byte the exp-238 `geometry.box` midpoint and bounds (`geometry.py`): one root
box, radii $9.9\times10^{-24}$ and $6.5\times10^{-23}$, widened to $10^{-40}$ by the
cover tool. The local theorem folds the box into its residual (C8(i)) and the slide
coverage encloses every endpoint quantity over it, so both theorems are about the family
at the exact root, in the exact root’s frame $u^\ast$, as the recipe requires.

**Angles and labels.** Both tools take each angle as the H254 lift modulo $\pi/2$ within
$r$ of the family’s, so a square geometrically within $r$ but labelled a quarter turn
off is outside both neighbourhoods, consistently.
Square 6 is checked at every turn.
The labelling of a packing in the endpoint’s state is forced: each of the seventeen
occupied cells holds exactly one centre, and the label is the family square assigned to
that cell (square 6 is the square in `side-S2`, square 13 the one in `side-S1`). The
cover’s uniqueness of the family’s state is not used by the composition itself; it
matters to the global half, so that no point of the family sits in a second state that
would need its own capture.

**The theorem the three receipts prove.** Let $P$ be a packing of 17 unit squares in
$[0,S]^2$ with $S\le S^\ast$, embedded in the cover frame with its lower-left corner at
$(\sigma,\sigma)$. Suppose (i) the occupancy state of $P$’s centres on
`ring-3-voronoi-8-tabbed-unique` is the endpoint’s, which labels $P$’s squares, and (ii)
in that labelling the 45 non-slider coordinates of $P$ (angles as H254 lifts; $\eta_5$,
$\omega_5$ for square 5; $u^\ast\!\cdot\delta r$, $\omega$ for 11 and 13;
$\xi,\eta,\omega$ for the other thirteen) are each within $1/5000$ of the family’s at
the exact root. Then $a\in[0,\tfrac{23}{200}]$, $b\in[b^\ast,\tfrac{37}{500}]$ and
$z\in[-\tfrac{49}{1000},0.0241004]$, so $w(P)\in B_W'$; hence the sixteen squares other
than 6 are exactly $x^\ast(w(P))$; the family touches all four walls of
$[\sigma,U-\sigma]^2$ at every $w$ (C10), so $S=S^\ast$ and $P$ lies on the family, with
square 6 somewhere in `side-S2` where it fits.
Nothing is said about packings in other states, about a packing in this state whose
coordinates are not within $r$, or about $S>S^\ast$; and the receipts that carry it are
lane H2’s `receipt-unique.json`, lane A3’s $B_W'$ receipt with its certificates, and
exp-247’s run, of which only the last is yet an experiment record.

**Missing links.** (1) The embedding above, to be fixed in the capture design.
(2) The $B_W'$ run recorded as an experiment at `9c26793c`, with the receipt and
certificate digests, and H-268’s acceptance text naming $B_W'$. (3) The capture step
must deliver closeness in the exact root’s frame; the rational enclosure of $u^\ast$ is
charged to its radius (recipe open question 4), not to $r$. None is a gap in what is
proved.

## H-261 As Worded

The claim has no occupancy premise and lets the sliders, square 6’s three coordinates
included, range over everything physically feasible.
The suggestion that square 6 is then confined to its own hole is false: exchange squares
5 and 6 in the family, placing 6 at the bottom-right corner and 5 in 6’s box.
`witness_check.py` verifies this is a packing of side exactly $S^\ast$ for every
$a\in[1,1.0742]$ (5 meets 13 at $a=1.074160$), with all 45 non-slider coordinates
exactly on the family and $b=z=0$. It satisfies every premise of H-261 and lies outside
$B_W'$, where the local theorem has no retained 5/7 face and square 7 would rest on the
dropped square 6. Square 13 retreating along $-v$ with 6 in its place is a second such
component, and a grid search (step $0.01$, $2°$) finds no room for square 6 anywhere for
$a\in[0.13,0.99]$ at $z=0$, which suggests the domain is disconnected.
Whether these packings are local minima modulo their own sliders is a different theorem,
with a different retained system, that no receipt addresses.
The frozen criterion also asks for every item “uniformly over the slider domain”, which
$B_W'$ is not. H-261 therefore stays unresolved, as exp-244 recorded, and the composed
theorem above, with its state premise, is the capture-target theorem under H-268.
Narrowing H-261 to $B_W'$ would be a retune after the result and is not proposed here.

## Blocking Defects

None in `check_n17_slider_coverage` at `05b078bd`, in `check_n17_local_minimum` at
`9c26793c` on $B_W'$, in the exp-247 cover, or in their composition.

Blocking for the record, not for the mathematics: H-268 cannot be accepted with “$B_W$”
in its consequence; the acceptance must name $B_W'$ and cite a recorded $B_W'$ run of
the local theorem.

## Notes

1. The cell `side-S2` in the receipt,
   $[\tfrac{4021}{1500},\tfrac{1693}{500}]\times[\tfrac12,\tfrac{1411}{1000}]$, is what
   the design parameters give (corner $\tfrac{79}{100}$, middle width
   $\tfrac{257}{375}$, depth $\tfrac{911}{1000}$), and the family’s square-6 box
   $[3.0645,3.1758]\times[0.5002,0.7502]$ lies inside it.
2. The receipt’s `margins` field reports the first thresholds against $B_W$
   ($\tfrac1{25}$, $\tfrac1{120}$, $\tfrac3{40}$); the margins of the tight box, which
   capture should cite, are $\tfrac{27}{200}$ in $a$, $\tfrac{19}{250}$ in $z$ and
   $\tfrac7{750}$ in $b$, and $6.3\times10^{-5}$ between $b^\ast$ and the $B_W'$ floor.
3. The H-268 Progress section still quotes the tabbed-design bounds
   ($a\le\tfrac{21}{100}$, $z\ge-\tfrac1{20}$, $b\le\tfrac3{40}$); the unique-design run
   supersedes them.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
