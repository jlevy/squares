# Review Plan for Issue 1050 (s(18) = (7+√7)/2), Frozen Before Any Check Ran

Lane r1050, bead `think-5jr0`, 2026-11-20. This plan is written after reading the
source's prose and data only: `README.md`, `proof.md`, `verification.md`,
`replay/README.md`, `replay/stabs18-endpoint-window.json`, `replay/six-tilt18.json`,
`replay/SHA256SUMS`, and the key lists of the case JSON files. No program of the source
(`*.py`, `*.cpp`, `*.inc`) has been opened or run. Source: `Mira-Cult/math` at
`78bec6aacebf304d942a9225e16c2f18165778ff`, folder
`notes/geometry/unit-square-packing-18/`. For form only, I read this repository's
reviews of 2026-09-20 (n = 17, Mira's earlier certificate) and 2026-11-18 (issue 1018).
No earlier review of this result exists in the record.

## Notation

$H = (7+\sqrt7)/2$. $U = 4822876/10^6$ (the rack's `cap`). The rack $M$: the orbit
closure, under the eight symmetries of $[0,2000]^2$, of the lattice points (390,390),
(617,617), (797,359), (1000,716), (1000,1000), each scaled by $U/2000$. A tile is a
closed unit square with centre $c$ and angle $\theta$; $h = 1/2$;
$\lVert x \rVert_\theta = \lVert R(-\theta) x \rVert_\infty$. $\varepsilon = 1/100000$ (the
rack's `erosion`).

## Statements the Proof Needs

- **S0.** $U > H$, so a packing in a square of side $L < H$ translates into $[0,U]^2$
  with all tiles inside.
- **S1 (construction).** The 18 tiles of `six-tilt18.json`, with orientation bit 1 meaning
  axes $u = ((1+\sqrt7)/4, (\sqrt7-1)/4)$ and $Ju$, lie in $[0,H]^2$ and have pairwise
  disjoint interiors.
- **S2 (covering lemma, strong form).** For every $\theta$ and every $c$ with the tile
  inside $[0,U]^2$ there is $m \in M$ with $\lVert m - c \rVert_\theta < (1-\varepsilon)h$.
- **S3 (assignment).** Choosing for each tile a nearest mark in its own norm gives an
  injective map from tiles to marks; each chosen mark is interior to its tile, every
  other occupied mark lies outside the closed tile, and no mark is strictly nearer.
- **S4 (orbits).** The 1330 three-element sets of unoccupied marks fall into exactly 187
  orbits under the box's eight symmetries, and the source's 187 case keys are one per
  orbit.
- **S5 (refutations).** For 181 orbits no packing with that assignment exists in
  $[0,U]^2$. This rests on the soundness of each kernel operation (proof.md, “Which
  changes to a pose domain are safe?”): K1 nearest-mark removal only where another mark
  is strictly nearer throughout the angle interval; K2 the conic-interpolation lemma for
  linear inequalities in $(\cos\theta, \sin\theta)$ (valid for homogeneous forms, or with
  a non-positive constant term, over an interval shorter than $\pi$); K3 closed
  subdivisions on both sides; K4 Minkowski sums of inner shapes as forbidden centre
  differences, removing only centres forbidden for every choice of the partner; K5
  outward lattice rounding; K6 floating-point proposals admitted only after exact tests;
  K7 a valid terminal for every branch.
- **S6 (six tight cases).** T1 a line crossing a tile between opposite faces has chord
  $1/\lvert\cos\rvert \ge 1$; T2 the row support $aR_x + bR_y \ge a + pb$ from a probe of
  $p$ tiles; T3 the two-row combination $(Q-P)\cdot(a,b) \le (L-3)a + (L-4)b$; T4 the
  chord bound $\lvert Q-P \rvert \ge 2$, the two-face bound $u\cdot(Q-P) \ge 2$, and the
  perpendicular-probe corner support; T5 $2 \le \sqrt{(L-3)_+^2+(L-4)_+^2} \Rightarrow L
  \ge H$. Every hypothesis must be verified over the whole pose enclosure and for every
  direction $(a,b)$ the inequality is applied to.
- **S7 (cover).** In each case the terminal regions cover the root domain; case 82's
  reflection is a symmetry of that case.

## Checks, Methods and Expected Outcomes

Every program is this lane's own, imports nothing from the source or this repository,
and runs as `python -I` under the project interpreter. Exact means `fractions.Fraction`
or Python integers, with $\mathbb Q(\sqrt7)$ as pairs of rationals and signs decided by
comparing squares.

- **C1 (S0, S1)** `r1050_construction.py`: every wall inequality (72) and every pair (153)
  by the separating-axis test on the four edge normals, exactly; list the contacts.
  Expected: pass. Controls, each expected to fail: side $H - 10^{-30}$; each touching
  pair closed by $10^{-30}$ along its separating axis; each tilted tile's orientation bit
  flipped; a tile duplicated.
- **C2 (S2)** `r1050_rack.py`: an exact branch and bound over $t = \tan(\theta/2) \in
  [0, T]$, $T = 4143/10000 > \sqrt2 - 1$ (checked), and centres in the whole box
  $[0,U]^2$; the reduction to $\theta \in [0, \pi/4]$ uses only the diagonal reflection,
  which maps $M$ to itself (checked). A leaf is closed either by exact infeasibility of
  every centre in it (the wall half-width is concave in $\theta$, so its minimum is at a
  $t$-endpoint) or by one mark capturing every pose in it: each of the four inequalities
  is linear in the centre and a quadratic in $t$ after multiplying by $1+t^2$, so its
  maximum over the leaf is the maximum over the four corners of a quadratic on an
  interval, computed exactly. Floats only propose splits. Expected: pass at
  $\varepsilon$. Controls, each expected to fail with an exactly verified uncovered
  pose: the rack without (1000,1000); without (797,359); without (1000,716); without
  (390,390); and $\varepsilon = 1/2$. The largest passing $\varepsilon$ is measured for
  information only.
- **C3 (S4)** `r1050_orbits.py`: enumerate the 1330 sets, canonical form the smallest
  sorted tuple of lattice coordinates over the eight symmetries; confirm by Burnside's
  count. Expected: 187. After the freeze, with the source's mark order read from its
  code, every key must lie in a distinct orbit.
- **C4 (witnesses)** `r1050_orbits.py`: place the construction in $[0,U]^2$ at offsets in
  $\{0, (U-H)/2, U-H\}^2$, under all eight symmetries; compute each tile's nearest marks
  exactly, keep every tie, check each chosen mark is interior and the map injective, and
  record every orbit reached. Also move each tile that can move by $1/1000$ steps
  (validity checked exactly after each step, up to one unit) and record the orbits.
  Expected: every orbit reached is one of the source's six tight cases (53, 55, 82, 92,
  115, 137, mapped after the freeze). A witness in a refuted orbit would be blocking.
- **C5 (S5, sample)** `r1050_refute` (C++ with a Python driver): an independent
  refutation attempt. Each tile's angle range $[-\pi/4, \pi/4]$ is split into slices,
  each with a convex centre polygon. Rules: R1 the capture enclosure (mid-frame square of
  half-side $h(\cos\delta + \sin\delta)$ about the mark, $\delta$ the slice half-width);
  R2 the walls; R3 every other occupied mark as a point obstacle, removing centres whose
  inner square (half-side $h/(\cos\delta + \sin\delta)$) holds the mark; R4 pairs: a
  centre is removed only if, for every live slice of the partner and every vertex of its
  polygon, the difference lies in the open Minkowski sum of the two inner squares; R5
  the new domain is the convex hull of what remains. Branching splits a tile's slices or
  polygon into closed halves. Arithmetic is double precision, with every computed domain
  padded outward and every forbidden region shrunk by $\eta = 10^{-9}$, so a refutation
  here is independent evidence, not an exact certificate. Sample: the 187 canonical forms
  sorted ascending, minus the witness orbits of C4, then
  `random.Random(1050).sample(..., 6)`; one CPU-hour per case. Expected: refuted;
  “undecided” is reported as such and is not evidence against the source. Controls:
  synthetic instances (two tiles in a box of side 19/10 and four in 199/100 must be
  refuted; two in 2001/1000 and four in 2001/1000 must not be) and every witness orbit at
  $U$ must not be refuted.
- **C6 (S6)** The review re-derives T1 to T5 by hand. After the freeze it reads the three
  guards and checks that each hypothesis is tested over the whole enclosure and for every
  direction used, and it locates the construction in its case's cut tree: its terminal
  must be a guard terminal met with equality, not `empty`.
- **C7 (replay)** After the checker freeze, the source's own command runs from a copy of
  the folder (read before it runs). Mutated inputs, each expected to be refused: a
  construction coordinate changed; a rack point moved; a case key deleted from the base
  cover; a tight-case terminal relabelled `empty`; a cut threshold moved so the cuts no
  longer meet.
- **C8 (S5, S7)** After the freeze, a read of the kernel and the cover code against K1 to
  K7 and S7, citing file and line.

## Order

1. This plan is committed and pushed, its SHA-256 and time in
   `frozen/plan-frozen-digest.txt`.
2. C1 to C4 are written, run on synthetic data only, and frozen (checker freeze 1); then
   they run on the source's data.
3. C5 is written, tested on synthetic instances, and frozen (checker freeze 2); then it
   runs on the sample.
4. Only then is any source program opened (C6, C8) or run (C7).
5. The findings are frozen before the record at n = 18 is compared.

Budget: the owner's 40 CPU-hours for this item; the plan expects under 15.
