# Lemma EPS — half-side entry: the wedges of a near-simple square's cell (A227, 2026-09-15; PI 00:40)

A unit square `F` sitting within `(δ, θ0)` of a cell's slot pose leaves uncovered only four thin WEDGES of the
cell, one along each side, each on the tilt-determined HALF of its side; any other square meeting the cell must
enter through one of them, and a wedge along a pin- or wall-backed side only through its open END at the cell's
corner.  Rule EPS replaces the option row "M meets C" by "M meets the wedges of (F, C)".  Tags: [T] proved, [S]
supported, [M] measured, [F] false as stated, [C] obligation.  Lean `Statements/Open/LemmaEps.lean`
(`not_mem_iff_four`, `wedge_right_depth`, `wedge_right_corner`, `coord_within_h`, `gate` — all theorems).  Code
`attempts/A227-lemma-eps/code/eps227.py` (exact rational wedge polygons, targets, the strike), `epsscan227.py` (the
replay), `integration227.diff` (the wiring); results `attempts/A227-lemma-eps/results/eps227.md`; pages
`docs/residue_map/campaigns/A227-lemma-eps/`.

## 0. Verdict

> **[T] Lemma EPS (any n, pure geometry).**  Let `C = [X0, X1] × [Y0, Y1]` be a cell (on a page: the widened slot
> box `B_p⁺`; at side `m`: the slot box) and `F` a unit square with centre `z` and tilt `θ ∈ [0°, 90°)`,
> `t = tan(θ/2)`.  Then
> (EPS-1) `C \ F = W_R ∪ W_L ∪ W_T ∪ W_B`, `W_R = C ∩ {(p − z)·e > ½}`, `W_L = C ∩ {(p − z)·e < −½}`,
> `W_T = C ∩ {(p − z)·e⊥ > ½}`, `W_B = C ∩ {(p − z)·e⊥ < −½}`, `e = (cos θ, sin θ)` — four convex polygons.
> (EPS-2) In the unit cell `[0,1]²` with `z = (½ + δx, ½ + δy)`:
> `W_R = {(x, y) ∈ C : x > 1 − w_R(y)}`, `w_R(y) = w_R − (1 − y)·2t/(1 − t²)`, **`w_R = t(1 − t − 2δy)/(1 − t²) − δx`**:
> the wedge lies along the right side, is deepest (`w_R`) at the corner `(1, 1)`, tapers linearly and vanishes at
> the crossing height **`y* = ½ + δy + t/2 + δx(1 − t²)/(2t)`**; its foot on the side is `{y > y*}`.  For a pure
> rotation (`δ = 0`) the feet are the PINWHEEL: right side upper half `(½ + t/2, 1]`, top side left half
> `[0, ½ − t/2)`, left side lower half, bottom side right half (mirror image for a clockwise tilt).  Depth bound:
> `w_σ ≤ w̄(δ, t0) := δ + t0(1 + 2δ)/(1 − t0²) ≈ δ + θ0/2` for every side.
> (EPS-3) A unit square `M` with `int M ∩ int F = ∅` and `int M ∩ int C ≠ ∅` has an interior point in one of the
> four open wedges: it enters `C` only through a wedge, i.e. within depth `w_σ` of one side, on that side's foot.
> (EPS-4, a BOX of poses) for `z ∈ [x0,x1] × [y0,y1]`, `t ∈ [t0,t1] ⊆ [0,1]`, the union of the wedges over the box
> is contained in four explicit unions of ≤ 4 convex polygons each (interval arithmetic in `cos, sin`, exact
> rationals), and `K' := C` minus them is inside every `F` of the box — the engine's certified core.
> (EPS-5, GATE) if a side of `C` is BACKED (a container wall, or a pin whose certified core reaches the side's
> line), a meeter of its wedge has an interior point in one of the wedge's END ZONES at the cell's corners
> (the open end where the backed side meets a free side, or the pin-gap sliver at a backed–backed corner).
> (EPS-6, poses) the squares of tilt `φ` whose interior meets a set `W` are exactly those with centre in
> `W ⊕ int Sq_φ` (Minkowski sum); for a rectangle `W = [a0,a1] × [b0,b1]` this is inside
> `(a0 − h_φ, a1 + h_φ) × (b0 − h_φ, b1 + h_φ)`, `h_φ = (cos φ + sin φ)/2 ∈ [½, 1/√2]`.
>
> **[T] Rule EPS.**  At a node where a role `F` is near-simple in a FORCED cell `C = B_p⁺` (Theorem FC: two
> distinct non-pin squares meet `int B_p⁺`), the second meeter must meet a TARGET of `(F, C)`: the bounding
> rectangle of a free-side wedge polygon, or an end zone of a backed side.  Every other non-pin role whose pose set
> misses every target EXACTLY (A161's separating-axis test, in `t`, hull box then pieces, and per piece of `F` —
> the actual `F` lies in one piece) is STRUCK; an anonymous square is struck unless an alive option-table cell of
> `p` lies within `1/√2` (ℓ∞) of a target.  No candidate left ⇒ **DEAD by FC+EPS**, the certificate being the
> target list and the miss certificates.  Otherwise the survivors and their reachable targets are the geometry for
> a Rule NS split of the survivor at the WEDGE rather than at the whole cell.
>
> **[M] Y0865 (`R.2.3.1.p1.1.2.2.1.1.1x`, F1 at BL(1,0), §5):** the four free roles are struck at the hull box
> already; `H` reaches exactly ONE target, the right-side wedge `[1.974, 2.0108] × [0, 1.0068]` (its edge crosses
> `x = 2` at `y = 0.992`), so the rule does not kill and hands Rule NS the wedge.  The full replay over every A211
> g1 node is `results/eps227.md` (detached; see the resume block there).

## 1. Setting

`F = {p : |u(p)| ≤ ½, |v(p)| ≤ ½}` with `u = (p − z)·e`, `v = (p − z)·e⊥`, `e⊥ = (−sin θ, cos θ)` (Lean
`Parametrize.mem_set_iff_uv`); in `t`: `cos θ = (1 − t²)/(1 + t²)`, `sin θ = 2t/(1 + t²)`.  Tilts `θ` and `θ − 90°`
give the same square, so "within `θ0` of alignment" means `t ≤ t0 = tan(θ0/2)` after relabelling `e ↦ e⊥`.  NEAR-
SIMPLE in `C`: `|z − centre(C)|_∞ ≤ δ` and `t ≤ t0` (A224's filter: `δ = 0.06`, `θ0 = 3°`, `t0 = 0.02619`).  All
squares are closed; "meets" is interior-to-interior; the container is `[0, s]²`.

## 2. [T] EPS-1 and EPS-2 — the four wedges, exactly

*EPS-1.*  `p ∉ F ⟺ |u| > ½ ∨ |v| > ½ ⟺ u > ½ ∨ u < −½ ∨ v > ½ ∨ v < −½` (Lean `not_mem_iff_four`).  Each clause
cuts `C` by an open half-plane: a convex polygon (possibly empty).  ∎

*EPS-2.*  `u > ½ ⟺ (x − zx) cos θ + (y − zy) sin θ > ½ ⟺ x > zx + (½ − (y − zy) sin θ)/cos θ` since `cos θ > 0`
(Lean `wedge_right_depth`).  Put `zx = ½ + δx`, `zy = ½ + δy`, `1/cos θ = (1 + t²)/(1 − t²)`, `tan θ = 2t/(1 − t²)`:
`1 − x_line(y) = ½ − δx − (1 + t²)/(2(1 − t²)) + (y − ½ − δy)·2t/(1 − t²)`; at `y = 1` the bracket is
`[(1 − t²) − (1 + t²) + 2t(1 − 2δy)]/(2(1 − t²)) = t(1 − t − 2δy)/(1 − t²)`, which is `w_R`; the slope in `y` is
`2t/(1 − t²)` (Lean `wedge_right_corner`, the identity multiplied out).  `w_R(y)` is increasing in `y`, so the depth
is maximal at the corner `(1, 1)`, and `w_R(y*) = 0` at `y* = 1 − w_R(1 − t²)/(2t) = ½ + δy + t/2 + δx(1 − t²)/(2t)`.
The other three sides follow by the symmetries of `C`: `x ↦ 1 − x` sends `(θ, δx) ↦ (−θ, −δx)`; the quarter turn
sends `e ↦ e⊥`, i.e. `(u, v) ↦ (v, −u)`.  For `θ = 0` the wedge is the rectangle `C ∩ {x > 1 + δx}` (empty when
`δx ≥ 0`, of width `−δx` and no taper when `δx < 0`: the formula's `y* → −∞`).  ∎

*The half side.*  `y* ≥ ½ + t/2 + δy` whenever `δx ≥ 0`: an offset TOWARD the side (`F` pushed against it) keeps
the foot strictly inside the upper half; an offset AWAY from the side (`δx < 0`) lengthens it by `|δx|(1 − t²)/(2t)`,
and once `|δx| ≥ (½ + t/2 + δy)·2t/(1 − t²)` the wedge is a full strip (page `eps227_pinwheel.svg`, panel C).  So "half side" is exact for the pure rotation and a bound `y* ≥ ½ + t/2 − |δy| − |δx|(1 − t²)/(2t)`
in general — the engine uses the exact polygons, not the half.

*The constant.*  `w_R ≤ t(1 + 2|δy|)/(1 − t²) + |δx| ≤ w̄(δ, t0) = δ + t0(1 + 2δ)/(1 − t0²)`; A224's filter gives
`w̄ = 0.0894`; to first order `w̄ ≈ δ + θ0/2`.  The same bound holds on every side by symmetry.  ∎

*Pinwheel table (`δ = 0`, `θ > 0`).*  On `y = 1`: `v > ½ ⟺ −(x − ½) sin θ + ½ cos θ > ½ ⟺ x < ½ − t/2`; on `x = 0`:
`u < −½ ⟺ y < ½ − t/2`; on `y = 0`: `v < −½ ⟺ x > ½ + t/2`.  Right-upper, top-left, left-lower, bottom-right. ∎

## 3. [T] EPS-3 and EPS-4 — meeters enter through a wedge; a box of poses

*EPS-3.*  `U := int M ∩ int C` is open and non-empty and `U ∩ int F = ∅`, so `U ∩ F ⊆ ∂F`, a union of four segments
with empty interior; hence `U \ F ≠ ∅`, and any of its points lies in an open wedge of EPS-1 (strict inequalities)
and in `int C`.  ∎  (i) of the brief follows: the entry is within `w_σ` of side `σ`, on the foot `{y > y*}`.

*EPS-4.*  For a fixed unit normal `ν` (one of `e, −e, e⊥, −e⊥`) `sup_{z ∈ box} (p − z)·ν = (p − z_ν)·ν` at the box
corner `z_ν` minimising `z·ν`; for `θ ∈ [0°, 90°]` this corner is `(x0, y0)` for `ν = e`, `(x1, y1)` for `−e`,
`(x1, y0)` for `e⊥`, `(x0, y1)` for `−e⊥`.  Over the tilt bin, `c = cos θ ∈ [c1, c0]` and `s = sin θ ∈ [s0, s1]`
(`cos` decreasing, `sin` increasing in `t`), and for `ν = e`
`(p − z)·e = (x − x0)c + (y − y0)s ≤ V_e⁺(p) := max((x − x0)c0, (x − x0)c1) + max((y − y0)s1, (y − y0)s0)`,
likewise `V_{−e}⁺` with `(x1 − x, y1 − y)`, `V_{e⊥}⁺ = max((x1 − x)s0, (x1 − x)s1) + max((y − y0)c0, (y − y0)c1)`,
`V_{−e⊥}⁺` with `(x − x0, y1 − y)`.  Hence `⋃_{box} (C \ F) ⊆ ⋃_ν {p ∈ C : V_ν⁺(p) > ½} =: 𝒲(box)`; each `V_ν⁺` is
the maximum of four linear functions (one per sign quadrant of the offset), so each piece is a union of ≤ 4 convex
polygons `C ∩ {quadrant} ∩ {linear > ½}`, computed exactly by clipping the rectangle (Fractions).  A non-empty
piece touches `∂C` (the linear function is monotone in the quadrant's directions), so every polygon is assigned to
the side(s) of `C` its bounding box reaches.  `K' := C \ 𝒲(box)` satisfies `V_ν(p; pose) ≤ V_ν⁺(p) ≤ ½` for all
`ν` and poses, i.e. `K' ⊆ ⋂_{box} F`.  The relaxation `(c, s) ∈ [c1,c0] × [s0,s1]` loses the coupling `c² + s² = 1`,
a second-order loss (`0.0014` at a `3°` bin, nil at the pieces' `0.6°` bins).  ∎

## 4. [T] EPS-5 — GATE: a backed wedge is reachable only through its ends

**Lemma GATE (Lean `gate`).**  `M` a unit square; `R` a closed set with `int M ∩ int R ≠ ∅` and `int M ⊄ R`; `O`
an open set with `int M ∩ O = ∅` (the union of the obstacles' interiors); `E` a set such that every point of
`∂R \ E` lies in `closure O`.  Then `int M ∩ E ≠ ∅`.
*Proof.*  `int M` is convex, so the segment from `a ∈ int M ∩ int R` to `b ∈ int M \ R` lies in `int M`; it is
connected and meets both `R` and its complement, so it meets `∂R` at some `q ∈ int M`.  If `q ∉ E` then `q ∈
closure O`, and the open neighbourhood `int M` of `q` meets `O` — contradiction.  ∎

**Corollary EPS-5 (backed sides).**  On a page the obstacles are: the container's exterior `{x < 0} ∪ … ∪ {y > s}`;
each pin's CORE `K_P = [x1 − h, x0 + h] × [y1 − h, y0 + h]` for a pin box `[x0,x1] × [y0,y1]`, tilt `t ≤ t_P`, with
`h = 1/(2(cos + sin)) = (1 + t_P²)/(2(1 + 2t_P − t_P²))` (a unit square of tilt `φ` contains the axis-aligned square
of half-width `1/(2(cos φ + sin φ))` about its centre: `|(p − z)·e| ≤ h(|cos| + |sin|) = ½`); and `int F` itself,
which contains `int K'`.  A side `σ` of `C` is WALL-backed when it lies on `∂[0, s]²` and PIN-backed when a pin core
reaches the side's line from outside (`x0 + h ≥ X0` for the left side), its blocked span being the core's open
extent along the side; the complementary GAP slivers of the side (of length `≤ ½ − h + δ_pin`, `0.01` on A57 pages,
`3·10⁻⁸` on A60's) are exits.  Let `w_σ` be the depth of the polygons of `𝒲(box)` assigned to `σ`, `S_σ` the strip
of depth `w_σ` along `σ`, `K'_rect := C \ ⋃_σ S_σ ⊆ K'`, and `R := ⋃_{backed σ} S_σ` (area `< 1` whenever `w̄ < 1/8`,
so `int M ⊄ R`).  Every point of `∂R` is blocked or lies in a CORNER ZONE: on a backed side, by the wall or the pin
core except on the gap slivers; on a strip's inner side, by `int K'_rect ⊆ int F` except within the adjacent
strips' depths of the corners; a strip's end on a free adjacent side is an exit.  So `E ⊆ ⋃ Z_κ` over the corners
`κ` of `C`, `Z_κ` = the rectangle at `κ` spanned by the two adjacent depths, extended over any gap sliver at `κ`;
`Z_κ` is empty at a wall–wall corner or a backed–backed corner without gap.  A meeter of a backed wedge (⊆ R)
therefore has an interior point in some `Z_κ` — SNAP-DIAG's "point": a vertex poking in from the adjacent open
side.  ∎  On Y0865's BL(1,0) (left = pin BL(0,0), bottom = wall) the zones are `Z_(1,1)`, `Z_(2,0)` and the
`0.01`-gap sliver zone at `(1, 0)`; the free sides' wedges (right, top) are targets in full.

## 5. [T] EPS-6 and Rule EPS — the certificate

*EPS-6.*  `int M ∋ p ⟺ z_M ∈ p + int Sq_φ` (`Sq_φ` symmetric), so `{z_M : int M ∩ W ≠ ∅} = W ⊕ int Sq_φ`; for a
rectangle `W` the box bound is Lean `coord_within_h` (`|p.1 − cx| ≤ (|cos φ| + |sin φ|)/2`).  For a square of
UNKNOWN tilt the ℓ∞ dilation by `1/√2` (fact (F1) of `sideband.md`).  ∎

*Rule EPS (`eps227.py`).*  Inputs: the node's role boxes and pieces, the class's forced cells with their widened
boxes `wb` (A178), the pins' boxes.  For each near-simple pair `(F, p)` (A224's filter, heuristic only):
(a) `targets(F, C)` from `F`'s hull box: the bounding rectangles of the free-side polygons and the corner zones of
the backed sides, all inside `C` (the zones inside `R ⊆ C`); (b) a role `M ≠ F` (including `H`) is STRUCK when
A161's exact miss test (`snap224.misses_t`, the bin taken in `t`) separates every pose of `M` from every target —
hull box first, then every piece of `M`; and when that fails, per PIECE `π` of `F`: `M` is struck iff for every
`π`, `M` misses every target of `(π, C)` (the true `F` lies in some `π`, and the targets of `π` are a subset of the
hull's); (c) anonymous squares: none at a fully named node; else the FRESH option row `single[p]` (A198's reach of
a free square into `B_p⁺` clipped by every role's `K'`, Lemma CT's proviso as for rule CC) filtered to the cells
whose centre rectangle meets some target dilated by `1/√2`; (d) DEAD iff no named survivor and no anonymous cell.
*Soundness.*  Theorem FC gives two distinct non-pin meeters `Q1, Q2` of `int B_p⁺` on the page (all dilates, a
packing at `s0`).  At most one of them is `F`.  The other, `M`, is interior-disjoint from `F`, so by EPS-3 it has
an interior point in a wedge of the ACTUAL pose of `F`, which lies in `𝒲(π)` for the piece `π` containing that pose
(EPS-4); on a free side that point is in the polygon's rectangle, on a backed side EPS-5 gives an interior point
of `M` in a zone.  A struck `M` has no pose with an interior point in any target: contradiction.  Pins are not
candidates (the cell is UNCLIPPED for the class, `classes178.clipped_by_pin`, exactly as Rule SNAP's clause (b)).
An anonymous meeter's centre lies in an alive cell of `single[p]` (it meets `B_p⁺`) and within `1/√2` of the target
it meets (EPS-6).  ∎  Where it does not kill, each survivor's reachable targets are recorded: Rule NS on `(M, T)`
("M meets T" / "M misses T", the miss certified by the same test) is the split the wedge geometry suggests.

*Transfer.*  Nothing beyond Theorem FC is transferred from side `m`: the wedge argument runs on the page's own
squares (dilates are interior-disjoint, `closed_disjoint_bridge.md`), with `C = B_p⁺` and the pins' cores as they
are on the page.  At side `m` itself (exact pins, `g = 0`) the same statements hold with the raw slot box.

## 6. [M] What the rule measures — see `attempts/A227-lemma-eps/results/eps227.md`

The replay `epsscan227.py ALL --run g1_page` puts every recorded node of every A211 g1 certificate through the
rule on its own snapshot (padded outward, as `snapscan224` does).  Per node it records the candidates, the struck
roles, the survivors with their reachable targets, the anonymous cells kept, and the verdict; the report tabulates
kills by FC+EPS, nodes where a candidate lost a meeter without dying, and the surviving blockers.  The live wiring
(`integration227.diff`: leaf rule (0′) beside SNAP in `leaves211.py` / `tree211.py`, flag `A227_EPS=1`, default OFF)
is benchmarked on Y0402 g1 and on the closed page Y0865 g1 in isolated cert dirs.

## 7. [C] Obligations and levers

1. **[T] The polygon strike — DISCHARGED (A230, `attempts/A230-eps-branch/code/eps230.py` `misses_poly_t`).**  The
   strike now tests the wedge POLYGON as well as its bounding rectangle: axes = the polygon's edge normals (support
   radius of the square in an unnormalised direction `w = (a, b)` bounded by interval arithmetic in `(cos, sin)` over
   the tilt bin, the same relaxation as EPS-4) + the square's own two normals at radius `½`, both over the Minkowski
   difference `D = {box corner} − {polygon vertex}` (its extreme points).  Sound a fortiori: wedge ⊆ polygon ⊆ bbox.
   Flag `A230_TAPER` (on with the rule); the count of strikes it adds is in `attempts/A230-eps-branch/results/bench230.md`.
2. **[C] The tilt-coupled wedge.**  EPS-4 relaxes `(cos, sin)` to a box; the exact union over a bin is bounded by a
   circular arc, not a line — negligible at piece bins.
3. **[T] Rule NS at the wedge — DISCHARGED (A230, `attempts/A230-eps-branch/code/epsns230.py`, notes/eps230.md s.3).**
   Where exactly ONE named role `M` survives a candidate and the anonymous clause is CERTIFIED empty, `M` *is*
   Theorem FC's second meeter, so "`M` meets `W`" / "`M` misses `W`" (`W` = the union of the hull-box targets `M`
   can still reach) is exhaustive: the MISSES child is DEAD at once by FC+EPS (certificate = the target list + the
   struck roles' miss certificates; no cascade is run), and the MEETS child carries `M`'s pieces clipped exactly to
   the poses reaching `W` — a piece separated from every target is dropped, the rest are intersected with `W`'s
   bounding box dilated by `h = (cos + sin)/2` over their own bin (EPS-6).  Branch kinds `epsns-meets` /
   `epsns-misses` in `tree211.py`; depth-cap accounting as Rule NS's, and the split is capped per `(slot, role)`
   along a path (`A230_WEDGE_CAP`, default 1) because it otherwise recurs on the same pair at every depth.
4. **[T] n-general.**  Nothing uses `n = 11`: EPS-1…6 are about one cell, one near-simple square and its neighbours;
   Rule EPS consumes only Theorem FC (any forced cell of any class) and the node's pose sets.
