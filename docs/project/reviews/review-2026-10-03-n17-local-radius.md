---
title: n17 Local Theorem at a Larger Radius
date: 2026-10-03
status: planning-review
---
# n17 Local Theorem at a Larger Radius

**Session:** 168, lane L1. **Question:** can the n17 local theorem
([H-261](../../../packing/campaign/hypotheses/H-261-n17-local-minimum-modulo-sliders.md),
exp-244, and its composition with
[H-268](../../../packing/campaign/hypotheses/H-268-n17-local-theorem-slider-coverage.md),
exp-248) be proved at a radius larger than $1/5000$, and how much of capture would that
remove? The upstream precedent is n11’s two-radius local isolation (finding S2 of the
2026-10-03 n11 review integration, with
`packing/devtools/check_n11_optimality_local_two_radius.py`), which passes at $1/256$,
with $1/128$ for two squares’ angles.
**Method:** a new wrapper,
[`check_n17_local_radius.py`](../../../packing/devtools/check_n17_local_radius.py), that
calls the functions of `check_n17_local_minimum` and `check_n17_slider_coverage`
unchanged, with its test file and the receipts under
[`receipts/local-radius/`](../../../packing/campaign/explorations/X048-session-168-pilots/receipts/local-radius/).
Neither checker’s bytes changed, and neither refuses on a digest in the paths used.
The wrapper does not repeat `ratio_main`’s core-stress blob comparison (OR-16; Git keeps
that source) or the n11 replay control, which no radius or box changes.

## Verdict

- **At a uniform radius, no.** The ratio is linear in $r$: $0.9259$ at $1/5000$, $1.852$
  at $1/2500$, $4.52$ at $1/1024$, $9.05$ at $1/512$ and $18.1$ at $1/256$, with
  $-\omega_{11}$ binding throughout.
  By that linearity the uniform limit is about $1/4630$ for exp-248’s own certificates,
  and at most about $1/4391$ for any certificate of the recipe’s form (an exact floor).
- **Per coordinate, yes, at about five times the radius.** The softest direction,
  $-\omega_{11}$, draws its dual mass almost entirely from rows that do not touch square
  11, so widening $\omega_{11}$ alone divides its ratio.
  On $B_W'$ the recipe passes exactly with every one of the 45 coordinates at least
  $1/1024$ ($\omega_{11}$ at $\tfrac{11}{2}\cdot\tfrac1{1024}$, $u_{11}$ at
  $\tfrac2{1024}$, five others widened by 3 to 39 percent), worst ratio $0.99997$. No
  vector with every coordinate between $1/896$ and $1/14$ passes even the floating-point
  point test.
- **The composition closes at every coordinate at least $1/1216$.** The wider
  $\omega_{11}$ forces the slide coverage to run at $R=9/2048$, which pushes the slider
  box to $b\in[-0.00742,\,0.11]$, beyond $B_W'$. The recipe passes on the box that
  results,
  $[0,\tfrac4{25}]\times[-\tfrac1{128},\tfrac{11}{100}]\times[-\tfrac{13}{200},\tfrac1{30}]$,
  with every coordinate at least $1/1216$ (worst ratio $0.99932$), and also with every
  angle at least $1/1024$ and every position at least $1/3072$ (worst $0.99937$). At
  $1/1152$ the vector needs $\omega_{11}$ above the slide radius, so $1/1216$ is the
  largest floor found to close.
- **For capture, the angle target moves from $2\times10^{-4}$ to $8.2$ or
  $9.8\times10^{-4}$**, four to five times, and $\omega_{11}$’s to about
  $4\times10^{-3}$, so live rows can be four to five times wider: two fewer bisection
  rounds. The $1/1024$ pilot box is **not** already inside: its positions are $1.2$ to
  $3$ times the composed position floors, and its turns, after 128-row pilot 2, are $2$
  to $33$ times the new angle radii.
- **Keep it a component for now**, as upstream kept n11’s, and register it as a
  hypothesis with a frozen vector and box when a capture pilot adopts it as its target
  (section 6).

## 1. Where the Radius Enters

The ratio test (C9) is $\max_{\text{cells}} M_j/\bigl(2(r_j-\varepsilon_jR)\bigr)<1$
with $M_j=\sum_i\lambda_iK_i$ and $R=\max_kr_k$. The radius enters three times.

- **The curvature constants (C7)**, quadratic in the radii.
  A wall row has $K=r_\omega^2/\sqrt2$, a pair row
  $K=D\,r_{\omega,o}^2+2\rho\,r_{\omega,o}+(r_{\omega,o}+r_{\omega,p})^2/\sqrt2$ with
  $\rho$ the Euclidean bound of the two squares’ position radii and $D$ the largest
  centre separation plus $\rho$. At a uniform radius a pair row is about $9.7\,r^2$:
  $D\approx1.2$, $2\rho/r=4\sqrt2\approx5.66$ and $4/\sqrt2\approx2.83$, so the
  angle–position cross term is more than half of it.
- **The denominator** $2(r_j-\varepsilon_jR)$, linear; the residual term is negligible
  here.
- **The option margins (C6)**, $g+\sum_j\lvert\partial_jg\rvert r_j+K/2<0$. They are not
  what binds: all 125 stay negative to $1/256$, least $-0.0454$ there against $-0.0553$
  at $1/5000$.

So at a uniform radius $M\propto r^2$ and the ratio is linear in $r$, which is exactly
what the receipts show.

**These are already n11’s finer bounds.** `pair_curvature` and `wall_curvature` are the
per-pair constants of n11’s isolation checker (the formula of its PROOF.md section 7),
and C12 replays n11’s focused receipt through them.
The “six coarse constants” of n11’s review S2 are the coarser alternative.
Anything finer is a new lemma.
`check_n17_local_radius bounds` models two, in floating point and without third-order
terms:

| Direction, radii | Checker constants | Each row’s second-order part, with its sign | Weighted sum, rows allowed to cancel |
| --- | ---: | ---: | ---: |
| $-\omega_{11}$, uniform $1/5000$ | $0.878$ | $0.567$ | $0.465$ |
| $+\xi_3$, the $B_W'$ vector at $1/1024$ | $0.951$ | $0.547$ | $0.451$ |
| $-u_{11}$, the same vector | $0.950$ | $0.537$ | $0.441$ |

The signed row bound drops the owner’s $-\tfrac12w_o^2$ (concave) and uses the
tangential component of the displacement rather than its norm; it is about $1.6$ to $2$
times smaller per row, and $1.5$ to $1.8$ times smaller in the ratio.
Letting rows cancel gains about $2$. **A finer lemma would buy a factor of about two,
not the eighteen that a uniform $1/256$ needs.** The gap to n11 is the dual: the
$-\omega_{11}$ certificate has $\lVert\lambda\rVert_1=1{,}439$, the $1/175.8$ soft
slope, and no curvature bound fixes that.

## 2. Uniform Radii

`scan` on $B_W'$, every number exact.
The second column is exp-248’s own 93 certificates evaluated at the larger radius.
The floor is the dual of the point program at the box’s vertices and centre: a rational
$z$ with $A_N(w)z\le K$ row by row, so $\sum_i\lambda_iK_i\ge-s\,z_j$ for every
$\lambda\ge0$ with $\lambda^{\mathsf T}A_N(w)=-s\,e_j$, and no certificate of the
recipe’s form does better than the floor at any cell containing $w$ (less
$\lVert z\rVert_\infty\varepsilon$ for a residual $\varepsilon$).

| $r$ | exp-248 certificates | Floor | Binding | Directions with floor $\ge1$ | C6 least margin |
| --- | ---: | ---: | --- | ---: | ---: |
| $1/5000$ | $0.925931$ | $0.878153$ | $-\omega_{11}$ | 0 | $-0.0553$ |
| $1/2500$ | $1.85196$ | $1.75640$ | $-\omega_{11}$ | 1 | $-0.0547$ |
| $1/1024$ | $4.52212$ | $4.28879$ | $-\omega_{11}$ | 5 | $-0.0532$ |
| $1/512$ | $9.04669$ | $8.57991$ | $-\omega_{11}$ | 13 | $-0.0506$ |
| $1/256$ | $18.1032$ | $17.1691$ | $-\omega_{11}$ | 26 | $-0.0454$ |

At $1/1024$ the next directions after $-\omega_{11}$ are $-u_{11}$ ($1.52$),
$-\omega_{16}$ ($1.16$), $-\omega_8$ and $-\xi_8$ ($1.08$).

## 3. Per-Coordinate Radii

**Why $\omega_{11}$ can be wide.** Square 11’s only retained rows are $3/11$ and
$11/12\,E_\pm$; the $9/11$ face is dropped.
At the worst vertex at $1/5000$ the $-\omega_{11}$ dual has
$\lVert\lambda\rVert_1=1{,}439$ and puts $98.6$ percent of its mass on rows that do not
touch square 11, the largest being $10/15$, $16/17$, $15/16$, $14/17$ and $2/13$ at 8 to
9 percent each (`bounds-5000-omega11.json`). So its $M$ hardly depends on
$r_{\omega_{11}}$, and $M/(2r_{\omega_{11}})$ falls as $1/r_{\omega_{11}}$. The cost is
that $3/11$ and $11/12$ grow as $r_{\omega_{11}}^2$, and other duals load them: at the
$1/1024$ vector 15 percent of the $-u_{11}$ mass sits on square 11’s rows.
The vector widens $u_{11}$, $\xi_3$ and the square-8 and square-16 coordinates to absorb
that. This is n11’s two-radius pattern, a soft square given a wider angle.

**How the vector is found.** `shape` iterates $r\leftarrow\max(T,F(r)/\theta)$ from
$r=T$, with $F_j$ half the largest point-program mass of coordinate $j$ at the box’s
vertices and centre.
$F$ is monotone, so the iterates rise to the least vector above $T$ that passes the
point test with factor $\theta$, and grow without bound when there is none.
The settled vector is rounded up to multiples of $T/64$, and `ratio` then runs every
recipe item at it, exactly.

| Box | Floor | Widened coordinates (multiples of the floor) | Outcome |
| --- | --- | --- | --- |
| $B_W'$ | $1/1024$ | $\omega_{11}$ $\tfrac{11}2$, $u_{11}$ 2, $\omega_{16}$ $\tfrac{21}{16}$, $\omega_8$ and $\xi_8$ $\tfrac{89}{64}$, $\xi_3$ $\tfrac{67}{64}$, $\eta_8$ $\tfrac{33}{32}$ | **exact pass**, 138 cells, worst $+\xi_3$ $0.999973$ |
| $B_W'$ | $1/896$, $\theta=1$ | none settles | point test fails at every vector in $[T,64T]$ |
| $B_W'$ | $1/512$, $\theta=1$ | none settles | fails within four steps |

The $1/1024$ receipt passes all thirteen checks it runs (C1, the slide half of C2, C3,
C4 and its symbolic form, C6, C8 with the root-box residual, C9, C10, C11, the tiling,
the replay from the certificates, the controls), and all six controls are refused, among
them the vector scaled by two.
The worst ratios sit just under one because the cell bisection stops at the first
passing dual; the point test at the same vector is $0.95$.

## 4. The Composition

**The slide coverage at the vector’s largest radius.** H-268’s tool takes one radius for
all 45 coordinates, so it runs at $R\ge\max_jr_j$, which is conservative.
Its premise, square 6 in `side-S2` and the other squares within $R$, is then implied by
the vector’s. With the $B_W'$ vector, $R=\tfrac{11}{2048}$ gives a box that leaves
$B_W'$ (`slide-11-2048.json`): the $b$ floor is $-1.688R=-0.0091$ and $b$ reaches
$0.143$, against $B_W'$’s $[-1/2500,1/12]$. The cap on $b$ comes from the $11/13$ pair
cover, and in these runs it sits near $0.0237-z_{\min}+4R$, so it grows with both $R$
and $\lvert z_{\min}\rvert$.

**The run that closes.** At $R=9/2048$ with thresholds $a\le\tfrac25$,
$z\ge-\tfrac1{10}$, $b\le\tfrac3{20}$ and tight ones $\tfrac4{25}$, $-\tfrac{13}{200}$,
$\tfrac{11}{100}$, the unchanged `run` passes all seven checks, controls refused, and
certifies

$$
a\in[0,\tfrac4{25}],\quad b\in[-0.0074162,\ \tfrac{11}{100}],\quad z\in[-\tfrac{13}{200},\ 0.0314109].
$$

The main $a$ threshold must be loose, since only the tight cover has $z$ capped.
In trial runs not kept as receipts, a main threshold of $\tfrac6{25}$ at $R=11/2048$
left a box near $a=0.262$, $z=0.102$ open, and tighter thresholds failed: $z\ge-0.056$
and $b\le0.095$ at $R=11/3072$, and $b\le0.105$ at $9/2048$.

**The local theorem on that box.** On
$B_c=[0,\tfrac4{25}]\times[-\tfrac1{128},\tfrac{11}{100}]\times[-\tfrac{13}{200},\tfrac1{30}]$,
which contains the certified box:

| Vector | Widened | Largest radius | Cells | Worst |
| --- | --- | ---: | ---: | --- |
| every coordinate $\ge1/1216$ | $\omega_{11}$ $\tfrac{85}{16}$, $u_{11}$ $\tfrac{33}{16}$, $\omega_8$ and $\xi_8$ $\tfrac{71}{64}$, $\omega_{16}$ $\tfrac{67}{64}$ | $85/19456=0.004369\le9/2048$ | 109 | $-\omega_8$ $0.999317$ |
| angles $\ge1/1024$, positions $\ge1/3072$ | $\omega_{11}$ $\tfrac{249}{64}$, $u_{11}$ $\tfrac{97}{64}$, $\xi_8$ $\tfrac{13}{16}$, $\xi_3$ and $\eta_8$ $\tfrac{39}{64}$ (of $1/1024$) | $0.003799\le9/2048$ | 117 | $-\xi_8$ $0.999368$ |

Both pass every check and refuse every control.
At floor $1/1152$ on $B_c$ the vector settles with $\omega_{11}$ at
$\tfrac{373}{64}T=0.00506>9/2048$, outside the slide radius, and a larger slide radius
widens $b$ again. So $1/1216$ is the largest floor found to close, and $1/1152$ does not
close at this slide radius.

**The capture-target theorem at the new radius.** As in the
[composition review](review-2026-10-02-n17-local-half-composition.md), with $r^\ast$
either vector above: a packing of side $S\le S^\ast$, in embedding A, whose occupancy
state is the endpoint’s and whose 45 non-slider coordinates are within $r^\ast_j$ of the
family at the exact root, has $w\in B_c$, sixteen squares exactly on the family, and
$S=S^\ast$. The frame, cap and $u^\ast$-enclosure obligations are unchanged.

## 5. What It Changes for Capture

**The contraction target.** From $2\times10^{-4}$ in every coordinate to the vector:
$8.2\times10^{-4}$ in most coordinates and $4.4\times10^{-3}$ in $\omega_{11}$ (cube
form), or $9.8\times10^{-4}$ in every angle, $3.3\times10^{-4}$ in most positions and
$3.8\times10^{-3}$ in $\omega_{11}$ (capture form).

**Rows, by the capture-after-pilot rule** that extents settle at about 36 row widths in
angle (square 11) and 28 to 36 elsewhere, and 12 in position:

| Target | Binding coordinate | Row width | Rounds from $\pi/4$ |
| --- | --- | ---: | ---: |
| $1/5000$ uniform (now) | $\omega_{11}$, $r/36$ | $5.6\times10^{-6}$ | 17.1 |
| composed, cube form | the other angles, $r/36$ | $2.3\times10^{-5}$ | 15.1 |
| composed, capture form | the other angles and the positions | $2.7\times10^{-5}$ | 14.8 |

Rows can be four to five times wider, which removes about two bisection rounds.
$\omega_{11}$ stops binding: its target is now 4 to 5 times the other angles’.

**The $1/1024$ pilot box is not inside.** The local theorem alone on $B_W'$ does contain
its positions, but that box does not compose, since its slide coverage needs $B_c$. The
composed floors are $1/1216$ (cube) and $1/3072$ (capture form) in position, below the
seed’s $1/1024$. The turns are further out.
After pilot 2’s 128-row run they span $\pm2.0\times10^{-3}$ for the axis owners (2 to
$2.4$ times the new radii), $[-5.4,4.0]\times10^{-3}$ for square 11 (just over its $3.8$
to $4.4\times10^{-3}$), $4.9$ to $7.0\times10^{-3}$ for squares 12, 13, 14, $1.5$ to
$1.6\times10^{-2}$ for 9 and 10, and $2.8\times10^{-2}$ for 16 (about 33 times).
Capture still has to contract every angle by 2 to 33 times from that state, against 10
to 140 times before.

## 6. Hypothesis or Component

**A component now.** Upstream kept n11’s two-radius box beside the accepted rectangle
because nothing downstream used it.
Here nothing does yet either.
Two further reasons: the vector and the slide thresholds were found by searching against
these results, so a hypothesis registered now would be retuned after the fact; and the
worst ratios sit within $10^{-3}$ of one, which is sound in exact arithmetic but leaves
no room to change the vector or the box without a re-run.

**A hypothesis when capture adopts it.** Once a capture pilot is designed against the
vector, the composed theorem is load-bearing.
Register it then, freezing the vector (one of the two above, or a shaved copy), the box
$B_c$, the slide radius and thresholds, and the accept rule “both receipts pass, from a
clean worktree”. Then run it as an experiment, as exp-248 was.
H-261 stays unresolved and H-268 confirmed as recorded; this review changes neither.

## Evidence Status

| Kind | Items |
| --- | --- |
| Exact, by the unchanged recipe functions (planning evidence of exp-244’s kind; the recipe’s lemmas are hand proofs) | The $B_W'$ pass at floor $1/1024$; the two passes on $B_c$; their controls; C6 at every radius scanned |
| Exact, by the unchanged H-268 `run` | The slide coverage at $R=9/2048$ and its certified box |
| Exact floors | The uniform-radius floors and exp-248’s certificates evaluated at each radius (section 2) |
| Floating-point model | Every `shape` proposal; “no vector at $1/896$ or $1/512$”; the $1/1152$ step; the finer-bound factors (third-order terms dropped) |
| Derived from a model | The capture row widths and rounds, through the capture-after-pilot review’s exploratory 12/28/36 constants |
| Read from receipts | Pilot 2’s turn and position extents |
| Not done | A per-square slide coverage, which would shrink $b$’s range and let the floor rise; a finer curvature lemma; the $1/1152$ composition at a larger slide radius |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
