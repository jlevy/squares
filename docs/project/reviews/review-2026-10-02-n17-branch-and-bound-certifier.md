---
title: n17 Branch-and-Bound Certifier Review
date: 2026-10-02
status: planning-review
---
# n17 Branch-and-Bound Certifier Review

**Session:** 168, BC-418, lane R4 (independent adversarial reviewer).
**Reviewed:** `packing/devtools/pilot_n17_subpattern_bb.py` at commit `0bc6a03b4`
(SHA-256 `7b77c4fd…`, the bytes whose line numbers are cited below) and the same tool at
`a4a6b29a3` (SHA-256 `f8da95e8…`), which adds a passive certificate recorder and is what
produced the saved certificate; the receipts
`scratchpad/lanes/p2/target-a6-0-A-split025.json` (the first A run, module `715a2766…`,
uncommitted bytes) and
`packing/campaign/explorations/X048-session-168-pilots/receipts/bb-A-certified.json`
(the committed-bytes reproduction, manifest `340492bd…`); and the certificate directory
`scratchpad/lanes/p2/cert-A/` (84 chunks, 53 MB). **Question:** can the second certified
n17 sub-pattern exclusion, pattern A = {interior-SW, interior-NW, interior-W,
interior-S, interior-N, interior-SE} at cap $U = 1169/250$, be admitted to the census on
the strength of this tool?
**Method:** every number below was produced by scripts of my own under the session
scratchpad `lanes/r4/`: `transfer_count.py` (states and orbits), `a_search.py` (a float
placement search), `make_mutants.py` and `run_mutants.sh` (sixteen deliberately unsound
variants of the committed module, each run against the tool’s own witness-path controls
and its committed tests), `wt_mut_run.py` (the same variants made to write certificates,
so the certificate check’s sensitivity could be measured), `corrupt_cert.py` (nine
doctored certificates), and `verify_cert.py`, an exact-rational verifier that imports
nothing from the pilot module and nothing from HiGHS: π by Machin’s formula, sine and
cosine by Taylor series with Lagrange remainders in integer fixed point, exact clipping,
exact Farkas sums. Nothing in the repository was edited except this document.

## Summary

- **Verdict: no blocking defect found.** All nine rules (a) to (i) are sound as written;
  the inequality each rests on is stated in section 2 with the line that enforces it.
  Two are sound with a remark rather than a repair: the wall rule (g) is never active
  for pattern A, whose cells sit more than $0.7$ outside every wall band, and the
  certificate README’s phrase “any vector would do” for the plane normal overstates what
  the charge covers (the recorded normal does lie inside its enclosure, which is what
  the charge needs).
- **The witness-path controls cannot see second-order errors; the certificate check
  can.** Of sixteen unsound mutants, the three witness paths caught four (the midpoint
  wall bound, a dropped normal, a false disc rule, a lost child) and the committed tests
  caught eight. Dropping the chord’s error term, dropping the chord plane altogether,
  overstating the gap by $10^{-6}$, shrinking the pair box by $10^{-6}$ and rounding the
  dual bound inward all passed every witness path and every test.
  Fed through the recorder, every one of those produced a certificate my verifier
  rejected at the right check.
  The witness path only sees an outright closure or a box loss, and a relaxation error
  that vanishes quadratically with the angle width has nothing to show at the resolution
  floor. The certificate check, not the controls, is the admission gate.
- **Transfer count, reproduced:** 8 distinct D4 images of A, 110,448 of the 346,104
  capacity-one states, 13,897 of the 43,593 orbits, by direct enumeration and by
  inclusion–exclusion; the selector’s own `removes` for A is 110,448. The endpoint’s
  state contains no image of A, so this exclusion does not touch the endpoint.
- **The geometry is tight.** My float search (two seeds, 120 restarts) places the six
  squares with worst violation $8.79\times10^{-3}$ and $8.78\times10^{-3}$, below the
  selector’s reported best penetration of $1.49\times10^{-2}$; that number is not a
  lower bound. The best poses are the near-lattice the module docstring describes: all
  six squares at $49.6°$. No placement was found.
- **The certificate re-checks.** The tree covers the root box: all 41,598 nodes
  reachable from the root, every open node split into exactly the children its record
  names, every closed node childless, 21,215 closed leaves (10,032 disc, 6,679 pair,
  4,504 LP). All 378 trig enclosures hold against my Taylor bounds.
  A sample of 3,553 nodes was verified in full — the 50 deepest closures (depth 31), 200
  random LP closures, 200 random disc and pair closures, and every ancestor of each: 205
  Farkas closures, 67,623 bound tightenings, 165,531 cut right sides, 730 pair splits
  and 2,374 angle splits, box inheritance along every chain — with zero failures in 236
  s. The verifier rejects all nine kinds of doctored certificate.
  The full-tree run then verified every one of the 41,598 nodes in full — 4,504 Farkas
  closures, 10,032 disc and 6,679 pair closures, 639,609 bound tightenings, 1,652,060
  cut right sides, 17,349 angle and 3,034 pair splits — with zero failures in 1,531 s.
- **Bottom line: admissible, under the conditions in section 5.** The record must bind
  the committed receipt and manifest rather than the first (uncommitted-bytes) receipt,
  retain the certificate and an independent full re-check, and record that the exclusion
  rests on the certificate check and not on the witness controls.

## 1. What the Tool Claims and How It Argues

A sub-pattern $G$ of $k$ closed cells is forbidden when $k$ unit squares, square $i$
centred in cell $i$, at any angles, all inside $[0,U]^2$, cannot have pairwise disjoint
interiors. The tool branches on the $k$ angles, each in one closed period
$[\theta_0, \theta_0+\pi/2]$ with $\theta_0 = 0.4$, and on each angle box decides the
centres by a linear program whose rows are the cells’ edges, per-pair *hull cuts* and
the centre boxes.
Two squares are disjoint iff $n\cdot d \ge g$ for one of eight directed
normals $n(\theta_i + k\pi/2)$, $n(\theta_j + k\pi/2)$, with $d = c_j - c_i$ and
$g = \tfrac12 + h(\theta_j-\theta_i)$, $h(a) = (|\cos a|+|\sin a|)/2$. Each normal
family gives a *piece*, an interval of normal angles; a piece narrower than $\pi/2$ is
covered by three half-planes (its two end normals and a chord), a wider one by a single
relaxed row. The union of a pair’s half-planes within the pair’s box of differences $d$
is bounded by the facets of its convex hull, each facet’s right side made valid by an
exact Lagrangian bound.
HiGHS proposes multipliers; a closure or a tightened box is accepted only when the
multipliers’ combination, evaluated with interval floats rounded outward, proves it.
A node closes by `cell` (box misses its cell or walls), `disc` ($|d| < 1$ throughout),
`pair` (no half-plane of any piece can meet the box), `lp` (Farkas) or `obbt` (a
tightened bound crosses); otherwise it is split, by the most violated undecided pair’s
options or by bisecting an angle.
A run that stops at the resolution floor or the depth cap is unresolved, never
certified.

The reasoning is a chain of “every feasible pose of this node satisfies …” statements,
each derived from earlier ones, so there is no circularity; what must be checked is that
each link is an implication for *every* pose in the node, not a statement about the LP
point.

## 2. Soundness of the Pruning Rules

Line numbers are those of commit `0bc6a03b4`. The `a4a6b29a3` diff adds the recorder’s
hooks, replaces the `functools.cache` on `cos_sin` with a module dictionary the
certificate writes out, records each pair’s pieces, and rewrites the bound-improvement
test in `tighten` as an equivalent `improved` flag; I read the whole diff and found no
change to what the search computes.

### (a) The disjointness condition: sound

Projecting square $i$ onto a unit vector at angle $\phi$ gives an interval of half-width
$(|\cos(\phi-\theta_i)| + |\sin(\phi-\theta_i)|)/2$. On $i$’s own edge normals this is
$\tfrac12$; on $j$’s it is $h(\theta_i-\theta_j) = h(\theta_j-\theta_i)$ because $h$ is
even with period $\pi/2$. The two half-widths sum to the same $g$ on all eight axes, so
the separating-axis theorem reads $n\cdot d \ge g$ for some directed normal, the eight
directed normals covering both signs of each axis.
The comparison is non-strict, which is right for closed squares with open interiors
(lines 13–18, and the lower bound `gap_lower`, lines 281–290). `gap_lower` returns $1$,
the minimum of $g$, whenever the two angle intervals overlap or the difference range may
contain a multiple of $\pi/2$ (the test `contains_half_pi_multiple`, lines 251–255, is
conservative: it uses the outward enclosures of $k\pi/2$ and declares any interval at
least $\pi/2$ wide a hit); otherwise $h$ is concave on the open interval between
consecutive multiples, so its minimum is at an endpoint, and both endpoints are
evaluated through the difference formulas on enclosures (line 274–278) so that no
rounded angle is ever formed.
`disc` (line 797) uses the strict $|d|^2_{\max} < 1$: open discs of radius $\tfrac12$
inside the squares overlap.
`separated` (line 795) uses $|d|^2_{\min} \ge 2$: the circumscribed discs are then
disjoint.

### (b) Three half-planes per option: sound

The lemma (lines 507–521): if $n(\phi)\cdot d \ge g$ for some $\phi \in [a,b]$ with
$b - a < \pi/2$, then $n(a)\cdot d \ge g$, or $n(b)\cdot d \ge g$, or $n(m)\cdot d \ge
g\cos x$ with $x = \max(m-a, b-m)$. Proof: write $d = \rho\,n(\psi)$ and take the
representative of $\psi$ with $\psi - \phi \in (-\pi/2, \pi/2)$, which exists since
$\rho\cos(\psi-\phi) \ge g > 0$. Then $\psi \in (a - \pi/2, b + \pi/2)$, an interval of
length below $2\pi$, so exactly one of three cases holds.
If $\psi \in [a,b]$ then $|\psi - m| \le x$ and
$n(m)\cdot d = \rho\cos(\psi-m) \ge \rho\cos x \ge g\cos x$, using
$\rho \ge \rho\cos(\psi-\phi) \ge g$. If $\psi > b$ then $0 < \psi - b \le \psi - \phi <
\pi/2$ and cosine decreases there, so $n(b)\cdot d \ge n(\phi)\cdot d \ge g$; the case
$\psi < a$ is symmetric.
This is an exact statement, not an approximation; “second-order loss” in the docstring
describes only how far the chord row sits below the true boundary.
The code then uses $\cos x \ge 1 - x^2/2$, true for all real $x$, with $x$ rounded up
and the product rounded down (line 520), and replaces $g$ by the lower bound $g_{lo}$,
valid because $1 - x^2/2 > 0$ for $x < \pi/4$. The width guard
`up(hi - lo) >= HALF_PI[0]` (line 516) sends anything that might be $\pi/2$ wide to the
single-row fallback.
The midpoint $m$ is a snapped float checked to lie in $[a,b]$ (line 486). Each float
normal $\bar n$ is the rounded midpoint of its enclosure, hence inside it, so
$|\bar n_x - \cos\phi| \le$ the enclosure’s width, which is the `eps` charged against
$|d|_1$ (lines 529–534). The fallback row (lines 489–499) rests on
$n(\phi) - n(m) = 2\sin\tfrac{\phi-m}{2}\,n_\perp(\tfrac{\phi+m}{2})$ and
$|n_\perp(\tfrac{\phi+m}{2}) - n_\perp(m)| \le \tfrac{|\phi-m|}{2}$, giving
$n(m)\cdot d \ge g - 2\tau(S + \tau D)$ with $\tau \ge |\phi-m|/2$,
$S \ge |n_\perp(m)\cdot d|$ and $D \ge |d|$, all rounded outward.

### (c) Hull cuts inside the pair’s d-box: sound

The box of differences is `difference_box` (lines 699–704), outward from the current
centre boxes, so it contains $d$ for every pose whose centres are in those boxes.
A cut $u\cdot d \ge v$ is valid when $v \le \min u\cdot d$ over the union of the pair’s
possible half-planes meet the box, because every feasible $d$ lies in that union (by
(b)) and in the box.
`hull_cuts` (lines 627–654) uses the float hull only to *choose* $u$; $v$ is the minimum
over planes of `plane_min` (lines 602–624), which is the Lagrangian bound
$\min_{\text{box}} (u - \lambda n)\cdot d + \lambda r$ for $\lambda \ge 0$, valid for
every nonnegative $\lambda$ since $\lambda(n\cdot d - r) \ge 0$ on the plane; the check
`not lam >= 0.0` (line 617) also rejects NaN. Planes the box cannot meet are dropped
before the hull (lines 546–559), which is valid because a feasible $d$ satisfying such a
plane would have to lie in the box.
The tightened boxes the children inherit are sound by induction: each bound in `tighten`
(lines 952–984) is a dual bound over the *current* box (`current`, line 967) with rows
valid on the round’s box, a superset, and `clip_to_box` (lines 356–372) clips the cell
exactly in rationals with closed half-planes, so a box that touches its cell at one
point survives.
The cells’ vertices come from `build_cover` in canonical counterclockwise
order, which Sutherland–Hodgman needs; I checked all 24.

### (d) Bound tightening from HiGHS multipliers: sound

`dual_bound` (lines 438–467) skips every multiplier that is not strictly positive (line
455), so HiGHS’s sign convention cannot make a bound invalid, only weak; `run` (line
927\) clips $y = \max(0, -\text{row\_dual})$ anyway.
With $y \ge 0$ and every row $a_r\cdot z \le b_r$ valid at every feasible pose,
$y\cdot(Az - b) \le 0$ there, so $\sigma z_c \ge (\sigma e_c + yA)\cdot z - y\cdot b$;
the right side is minimised over the box coordinate by coordinate with interval
coefficients, every operation stepping outward (`iadd`, `imul`, `dn`). The verified row
is the exact one (rational cell rows enclosed outward; cut rows with exact float
coefficients), and the LP row is it divided by `norm`, so the applied multiplier is
$y/\text{norm}$ (line 457). A sign $+1$ result raises the lower bound and a sign $-1$
result lowers the upper bound (lines 970–973); a crossing closes the node (line 976).

### (e) The Farkas closures: sound

The same combination with no cost term (line 941): a strictly positive minimum over the
box of $(yA)\cdot z - y\cdot b$ contradicts $y\cdot(Az-b) \le 0$. The LP’s own objective
$t^\ast$ is only a trigger (line 939); when the combination fails, the node is branched,
never closed (`farkas_failed`, line 950). A HiGHS status other than optimal is treated
the same way (lines 933–935).

### (f) `mpmath.iv` and the difference formulas: sound

`cos_sin` (lines 225–234) evaluates `iv.cos`, `iv.sin` at 120 bits at an exactly
representable float and rounds each end outward to a float (`_iv_float`, line 213).
`cos_sin_difference` (lines 274–278) encloses $\cos(p-q)$ and $\sin(p-q)$ for the exact
real difference by the addition formulas in interval arithmetic.
I confirmed all 378 enclosures the certificate uses against my own Taylor bounds
(section 4), and the committed test does the same at 300 random points.

### (g) The wall bound from $h$ at an interval endpoint: sound, with a remark

Containment is $h(\theta) \le x, y \le U - h(\theta)$; $h \ge \tfrac12$ with equality at
multiples of $\pi/2$ and concave between consecutive ones, so on an interval meeting no
multiple the least value is at an endpoint, and `h_lower` (lines 263–271) returns
$\max(\tfrac12, \min(h(a), h(b)))$ with each $h$ a lower bound from enclosures, or
$\tfrac12$ when the interval may meet a multiple.
`contract` (lines 771–783) then takes $[h_{lo}, U - h_{lo}]$ with $U$ rounded up.
The remark: pattern A’s six cells lie in $x, y \in [1.411, 3.265]$, while
$h \le \sqrt2/2 \approx 0.707$ and $U - h \ge 3.969$, so the wall clip never bites for
A. Rule (g) is sound but carries no weight in this certificate; the mutation study bears
this out (section 3).

### (h) The seam at $\theta_0 = 0.4$: sound

A square is invariant under quarter turns and its four edge normals are
$\theta + k\pi/2$, so restricting each $\theta_i$ independently to one period loses no
pose. The root interval is $[\theta_0, \text{up}(\theta_0 + \text{HALF\_PI}[1])]$ (line
763), closed and at least $\pi/2$ wide, so every orientation is represented at least
once; the two endpoints represent the same square, which costs a factor of two in the
seam’s regime and no soundness.
The constructor’s check $\theta_0 \in [-\pi, \pi]$ (lines 735–737) keeps every angle,
difference and shifted piece inside the range $[-2\pi, 4\pi]$ of the enclosed multiples.
Windows: a normal angle $\phi$ lies in $[\theta_0, \theta_0 + 2\pi + \varepsilon]$ and a
window in $[\theta_0 - \varepsilon, \theta_0 + 2\pi + \varepsilon]$, so $\phi + 2\pi t$
can lie in a window only for $t \in \{-1, 0, 1\}$, which is exactly what `in_window`
tries (lines 667–681), with each shift rounded outward.

### (i) Coverage of the root box: sound

Angle bisection yields the closed halves $[a, m]$ and $[m, b]$ (lines 1029–1031), which
overlap at $m$. A pair branch yields one child per merged option (lines 1005–1020);
every feasible pose has a separating normal $\phi$ in some piece, $d$ satisfies one of
that piece’s half-planes by (b), that half-plane is then possible on the box, so the
piece is alive and lies in some option, and the child with that window holds the pose.
Windows and tightened boxes are inherited, both valid on the subset.
The driver (lines 1302–1358) pops every node and either closes it, pushes all its
children, or stops with an unresolved verdict at the floor, the depth cap or the budget;
`certified-infeasible` survives only if the stack empties.
The certificate makes this checkable rather than argued, and section 4 checks it over
every node.

### What I looked for and did not find

Strictness mismatches between closed cells and open interiors; an LP point used as a
fact about the node (none: the point only chooses branches); a tightened bound evaluated
over the round’s box instead of the current one (it is evaluated over `current`); a cut
computed on a box smaller than the one the children inherit (cuts come from the round’s
box, children get the tightened subset); a piece intersected with its window on the
wrong turn; a `relax` row used on a piece wider than $\pi$ (pieces are at most $\pi/2$
plus a few ulp); a half-plane dropped as impossible by a test that was not an upper
bound; a dual bound with a negative multiplier; a `clip` that drops boundary contacts; a
cell polygon in non-boundary order; an overflow or NaN path into `imul` (`not lam >= 0`
guards the one division).
A nit in the certificate README, not the code: P3 says of the recorded normal “any
vector would do: the check charges its distance to the enclosure”, but the charge is the
enclosure’s width, which covers a normal *inside* the enclosure; the recorded normals
are, and my verifier checks that they are.

## 3. Mutation Tests

Sixteen variants of the committed module, each one textual patch asserted to apply
exactly once (`make_mutants.py`), were run against the tool’s own controls —
`--witness-endpoint` on the endpoint’s west and north states, `--witness-selector 1` on
the placeable control {side-S1, interior-SW, interior-W, interior-S, interior-SE,
interior-E}, and the 13 committed tests — and, as recorder-capable copies, were made to
write certificates for three small patterns (a crowded row closed by Farkas prunes, the
same row with bound tightening, and a placeable row) plus a crowded row moved against
the west wall, each certificate then fed to `verify_cert.py`. The unmutated module
passes every control and every test, and its certificates verify.

| Mutation | Rule | Witness paths (W, N, placed) | Committed tests | Certificate check |
| --- | --- | --- | --- | --- |
| wall bound $+10^{-6}$ | g | pass, pass, pass | 13 pass | B1 rejects it on the wall row; not exercised on rows away from the walls |
| wall bound from the midpoint | g | **fail** (box lost, depth 11), pass, **fail** (depth 40) | 1 fail | rejects a false `cell` closure on the wall row |
| chord error term dropped | b | pass, pass, pass | 13 pass | rejected: cut right side above the exact minimum |
| chord plane dropped | b | pass, pass, pass | 13 pass | rejected: cut right side above the exact minimum |
| cut-row multipliers negated | d | pass, pass, pass (no closure at all) | 4 fail | fails safe: certifies nothing |
| raw HiGHS duals, no sign check | d | pass, pass, pass (no closure) | 4 fail | fails safe |
| dual bound rounded inward | e | pass, pass, pass | 13 pass | rejected on a bound tightening; the Farkas certificate it wrote is still valid |
| one of four normals dropped | a | **fail**, **fail**, **fail** | 4 fail | rejected (pieces do not cover); it falsely certified the placeable row, and the verifier caught that |
| gap bound $+10^{-6}$ | a | pass, pass, pass | 13 pass | rejected: cut right side |
| pair box shrunk by $10^{-6}$ | c | pass, pass, pass | 13 pass | rejected: cut right side |
| negative $\lambda$ admitted in `plane_min` | c | pass, pass, pass | 13 pass | not exercised: no negative candidate won on these rows |
| period short by $10^{-6}$ | h | pass, pass, pass | 1 fail | rejected: root interval narrower than $\pi/2$ |
| period short by $10^{-3}$ | h | pass, pass, pass | 1 fail | rejected: root interval |
| disc rule on the near corner | — | **fail** ×3 (closed at depth 0) | 6 fail | rejected: the far corner of the box has $d \cdot d \ge 1$ |
| lost child at bisection | i | **fail** ×3 | 2 fail | rejected: T2 children mismatch |
| float difference instead of the difference formulas | f | pass, pass, pass | 13 pass | not exercised: a $10^{-16}$ change produced no invalid record |

Reading: the witness paths see four of sixteen, the tests eight, and the certificate
check every mutation that actually produced an invalid record (twelve), including the
six that nothing else saw.
The reason is structural.
`witness_path` fails only when a node on the pose’s path closes, loses the pose from its
boxes, or has no child holding it; a cut that wrongly excludes the pose shrinks neither
the LP’s bounds nor the node while other relaxation points remain, and at the floor the
chord’s error $g(1 - \cos x) \approx g
x^2/2$ is $10^{-13}$, below any tolerance.
The two unsound sign mutations are the reassuring kind — they certify nothing — and the
two “not exercised” rows are a limit of the small patterns, not evidence of safety.

## 4. Geometry, Transfer Count and the Certificate

### The transfer

From the cover tool’s 24 cell polygons and its `d4_apply` on points, I built the eight
cell permutations (checked to form a group), the 8 distinct images of A, and enumerated
all $\binom{24}{17} = 346{,}104$ states: **110,448** contain an image of A (also by
inclusion–exclusion over the images), lying in **13,897** of the 43,593 D4 orbits
(Burnside reproduces 43,593). The selector receipt’s `removes` for A is 110,448. The
endpoint’s state {four corners, S0, N0, W0, E0, S1, N1, E1, S2, N2, W2, interior-W,
interior-N, interior-E} holds no image of A.

### Is A plausibly infeasible?

`a_search.py` minimises the worst of pair penetration, cell excursion and wall excursion
over the 18 pose variables with a log-sum-exp surrogate sharpened in four stages and a
Nelder–Mead polish, from 60 random starts per seed, half of them with a shared angle.
Best violations: $8.79\times10^{-3}$ (seed 1) and $8.78\times10^{-3}$ (seed 2); the
median start ends at $3.7\times10^{-2}$. Both best poses are the same near-lattice, all
six squares at $49.6°$ with interior-SW at $(1.402, 1.742)$, interior-W at
$(2.045, 2.497)$ and interior-SE at $(3.274, 2.005)$, which is the regime the module
docstring names. The selector’s $1.49\times10^{-2}$ is above both and should not be
quoted as a bound.
No placement was found; the certificate is what turns “not found” into
“none”.

### The certificate

`verify_cert.py` reads the manifest, the enclosure table and the 84 chunks, refusing any
file whose bytes do not hash to its name, and checks:

- **Header.** The six cells equal the design’s cells (vertex sets) and are strictly
  counterclockwise; the pairs are all fifteen; each root angle interval is wider than
  $\pi/2$ by my π; each root box contains its cell; each recorded multiple of $\pi/2$
  encloses mine.
- **Trig.** All 378 enclosures contain my Taylor enclosures (width about $2^{-158}$),
  and each recorded normal lies inside its own enclosure.
  The tree uses 24 distinct angle endpoints and 359 piece angles, all present in the
  table.
- **Tree (T1–T3), over every node.** One root with the root angles and no windows;
  41,598 nodes all reachable; every open node has a `split` and a `final`, an angle
  split point inside the interval, and children whose angles and windows are exactly the
  two halves or the one-per-window records; every closed node is childless;
  `summary.complete` is true.
  Closed leaves: 21,215 (10,032 disc, 6,679 pair, 4,504 LP); maximum depth 31.
- **Per node (B1, B2, P1–P4, C1–C5).** Round 0’s boxes contain the exact contraction of
  the parent’s `final` (walls from my `h_lower`, cell clipped in rationals); each later
  round’s boxes contain the previous round’s `next`, which contains the clipped
  tightened box; `final` contains the last `next`. For every pair a multiplier or a
  split touches: the eight normal sets, within the window modulo $2\pi$ on all three
  turns, lie in the union of the recorded pieces; the pieces’ planes are recomputed with
  my $g_{lo}$ and my enclosures (chord or fallback by the piece’s width against my
  $\pi/2$); each cut’s $v$ is at most the exact minimum of $u\cdot d$ over the possible
  planes meet the box, by exact 2-D clipping; each Farkas combination is strictly
  positive; each bound is at most its exact combination over the current box, applied in
  order; a `disc` closure has $\max|d|^2 < 1$ and a `pair` closure has no possible
  plane; a pair split covers every piece that has a possible plane.

**Sample run** (`--sample 200 --deepest 50 --seed 7`): 3,553 nodes verified in full —
the 50 deepest closed leaves (depth 31), 200 random LP closures, 200 random disc and
pair closures, and all their ancestors, so every box on every chain is derived from the
root — 205 LP closures, 118 pair closures, 126 disc closures, 165,531 cut right sides,
67,623 bound tightenings, 730 pair splits, 2,374 angle splits; **zero failures**, 236 s.

**Full run** (`--all --trig all`, report `lanes/r4/cert-A-full.json`): every one of the
41,598 nodes verified in full — 4,504 Farkas closures, 10,032 disc closures, 6,679 pair
closures, 639,609 bound tightenings (the count P2’s own re-check reports), 1,652,060 cut
right sides, 17,349 angle splits and 3,034 pair splits (the receipt’s branch counts
exactly), every round-0 box against its parent’s `final`, every later box against the
previous `next`; **zero failures**, 1,531 s. Six cuts were vacuous: on their pair no
plane was possible under my tighter bounds, so the node had no feasible pose and the cut
is trivially valid.
The whole certificate therefore derives, in exact arithmetic and from
my own lemmas and enclosures, that no pose of the root box survives.

**Sensitivity.** Nine doctored copies of a small certificate (a cut’s right side raised
by $10^{-9}$, a Farkas multiplier negated, a bound overstated by $10^{-9}$, a round box
shrunk by $10^{-9}$, a leaf removed, a piece narrowed by $10^{-9}$ at a lower end no
other piece covers, a disc-closed box widened, an angle split point moved outside its
interval) are each rejected at the intended check; the narrowed-piece corruption is
caught only when the narrowed end is not duplicated by another piece of the same pair,
which is the right behaviour.

### Custody

Three module hashes appear in this story.
The first A receipt (`target-a6-0-A-split025.json`, 14:01) names `715a2766…`, bytes
never committed.
The tool was committed at `0bc6a03b4` as `7b77c4fd…`, which no A receipt
names. The certificate and `bb-A-certified.json` come from `f8da95e8…`, committed as
`a4a6b29a3`, re-run from a worktree with an import digest list.
All three runs report 41,598 nodes, 21,215 leaves, depth 31 and the same prune counts,
so the search is deterministic across the recorder’s addition, and the diff between the
two committed versions changes nothing the search computes.
The admissible object is the `a4a6b29a3` receipt with its manifest `340492bd…`, not the
scratch receipt.

## 5. Bottom Line

Pattern A’s exclusion **can be admitted**, under these conditions:

1. **Bind the record to committed bytes and the manifest.** The census entry cites
   `bb-A-certified.json` (module `f8da95e8…` at `a4a6b29a3`, manifest `340492bd…`), not
   `target-a6-0-A-split025.json`. The certificate (53 MB) is retained with its
   hash-named files, outside the repository if size demands, and the receipt’s manifest
   hash is what ties them.
2. **Retain an independent re-check and name its extent.** This review’s sample
   verification (3,553 nodes with every ancestor, all 378 enclosures, the whole tree
   structure) and the full-tree run (all 41,598 nodes) should be filed beside P2’s own
   re-check, which left P2, P4, B1, B2 and the trig table to this review.
3. **State the controls’ limit in the record.** The witness paths and the committed
   tests are necessary controls but are blind to second-order relaxation errors; the
   claim rests on the certificate check.
   A future certificate from this tool should not be admitted on controls alone.
4. **Record the transfer and the non-placement as evidence, not proof.** 110,448 states
   and 13,897 orbits; the endpoint state untouched; the float search’s
   $8.8\times10^{-3}$ as a control that found no placement, with the selector’s
   $1.49\times10^{-2}$ not quoted as a bound.

Two non-blocking follow-ups for the tool: amend the certificate README’s P3 wording to
say the recorded normal must lie inside its enclosure (it does), and note in the module
docstring that `witness_path` cannot detect relaxation errors that vanish with the angle
width, so that nobody treats a passed witness path as a soundness result.

## Evidence Status

| Kind | Items |
| --- | --- |
| Measured, this review | The transfer and orbit counts; the endpoint’s survival; the placement search minima; the sixteen mutants against three controls, the tests and the certificate check; the nine doctored certificates; the certificate verification (header, trig, tree, the 3,553-node sample, then all 41,598 nodes) |
| Read from code, this review | The inequalities and enforcement lines of section 2; the `a4a6b29a3` diff |
| Taken from the record | The receipts’ node, leaf and depth counts; the selector’s best penetration and `removes`; the cover’s cells and `d4_apply` (from `check_n17_capacity_one_cover`) |
| Not checked here | HiGHS itself (nothing depends on it); `mpmath.iv` beyond the 378 enclosures the certificate uses; the selector’s search code |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
