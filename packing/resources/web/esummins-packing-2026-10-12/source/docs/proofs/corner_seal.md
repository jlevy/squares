# The corner seal — Lemma SEAL, Lemma WEDGE, the slab certificate — A199, 2026-09-10

The PI's reading of `k5_16_interior_Y0491` (13:15): a free square that reaches into the slot ABOVE a pinned corner
from the side of the slot BESIDE it must be rotated, and its chord on the pin's top line then seals the slot beside
the pin except a wedge at the pin's corner that no unit square can use.  Stated here n-general, at the rigour of
`forced_corners.md` / `sideband.md`.  Tags: [T] proved here, [S] supported, [M] measured, [F] false, [C] Lean or
certificate obligation.  Code: `attempts/A199-corner-seal/code/seal199*.py`; certificates `results/seal199*.jsonl`.

## 0. Setting (the local frame)

A unit square P (the PIN) sits at a corner of the container with walls on two sides.  Put the pin's free corner
c at the origin, the pin at P = [0, 1] × [−1, 0], the wall through its far side at x = 1 and the floor at y = −1,
so the container lies in {x ≤ 1, y ≥ −1}.  The two slots beside the pin are

    B := (0, 1) × (0, 1)   (along the wall, above P),      A := (−1, 0) × (−1, 0)   (along the floor, beside P).

For `k5_16`'s BR corner: c = (s0 − 1, 1), B = BR(0,1), A = BR(1,0) (x_local = 1 − u, y_local = v − 1 in BR's frame);
the mirror orientation swaps u and v.  Every unit square of the packing other than P is interior-disjoint from P and
lies in the container.  A unit square F **reaches around the corner from A's side** if

    int F ∩ int P = ∅,   F ⊂ {x ≤ 1, y ≥ −1},   int F ∩ B ≠ ∅,   F ∩ {y < 0} ≠ ∅.

(Theorem FC supplies a FREE such F on a page: B is forced, and A178's reach test shows on Y0491 that every free
meeter of B dips below y = 0 — §4.)  Notation: for a unit square not axis-parallel, its RIGHTMOST vertex is unique;
write it q = (q_x, q_y), and φ ∈ (0°, 90°) for the angle between the downward vertical and the edge of F descending
from q; that edge has direction (−sin φ, −cos φ), its far end b = q − (sin φ, cos φ) is F's lowest vertex, the
other two vertices are l = b + (−cos φ, sin φ) (leftmost) and t = q + (−cos φ, sin φ) (highest).  L_F denotes the
line through q and b: x = x_r + y tan φ with x_r := q_x − q_y tan φ.

## 1. [T] Lemma SEAL (the forced rotation and the sealed edge)

Let F reach around the corner from A's side.  Then:

(a) **Half-plane.**  There is m ∈ (0, ∞) with F ⊂ {y ≥ m x}: F lies on the far side of a line of POSITIVE finite
    slope through the pin's corner.

(b) **Forced rotation.**  F is not axis-parallel; its rightmost vertex satisfies 0 < q_x ≤ 1, 0 < q_y < cos φ,
    the edge descending from q crosses the pin's top line y = 0 at x_r = q_x − q_y tan φ ∈ (−sin φ, 0], hence
    tan φ ≥ q_x / q_y > 0 (the tilt is bounded below by the poke ratio: the further q pokes past the corner
    relative to its height, the more F must be rotated), q_x < sin φ, and F ⊂ {x ≤ x_r + y tan φ} (F lies on the
    A-side of L_F).

(c) **The seal.**  F ∩ {y = 0} = [x_l, x_r] × {0} with

        x_r − x_l = 1 / cos φ                            if q_y < cos φ − sin φ   (the DEEP regime: l is below y = 0),
        x_r − x_l = (cos φ − q_y) / (sin φ cos φ) ≤ 1/cos φ   otherwise.

    In the deep regime x_l < −1: F's chord covers A's whole top edge except the SLIVER (x_r, 0) × {0} of width
    |x_r| = q_y tan φ − q_x < sin φ at the pin's corner.

(d) **F is itself a meeter of A**: b ∈ A and int F ∩ A ≠ ∅.

*Proof.*  (a) Q′ := {x > 0, y < 0} is an open convex cone with apex c.  F ∩ Q′ = ∅: a point of F in Q′ has
x ∈ (0, 1], y ∈ [−1, 0) (container); if it is in int P we are done, and if it is on ∂P ∩ Q′ (the far edge x = 1 or
the bottom y = −1 of the pin) then, F being a convex body in {x ≤ 1, y ≥ −1}, the open segments from that point to
interior points of F pass through int P.  Separate the disjoint convex sets F and Q′ (Q′ open): there are n ≠ 0 and
k with n·z < k ≤ n·f for z ∈ Q′, f ∈ F.  Boundedness of n·z above on the cone forces n = (−a, b) with a, b ≥ 0,
and then sup_{Q′} n·z = 0 (approached at c), so k ≥ 0 and F ⊂ {b y ≥ a x}.  b = 0 gives F ⊂ {x ≤ 0}, against
int F ∩ B ≠ ∅; a = 0 gives F ⊂ {y ≥ 0}, against F ∩ {y < 0} ≠ ∅.  So a, b > 0 and m = a/b.
(b) Let U = F ∩ {y ≥ 0} (convex, compact) and q̃ a maximiser of x on U.  Points of U with y = 0 have x ≤ 0 by (a),
while int F ∩ B contains a point with x > 0; so q̃_x > 0 and q̃_y > 0.  If q̃ were interior to an edge of F, that
edge would be vertical (else moving along it increases x while staying in y ≥ 0), so F = [x0, x0+1] × [y0, y0+1]
with y0 < 0 (F ∩ {y<0} ≠ ∅) and x0 + 1 > 0, and the vertex (x0+1, y0) violates y ≥ m x.  Hence F is not
axis-parallel and q̃ is a vertex; it is F's rightmost vertex, for a vertex w with w_x > q̃_x would have w_y < 0 and
the segment q̃w ⊂ F would cross y = 0 at x > 0, against (a).  Put q = q̃.  Both edges at the rightmost vertex go
left; the descending one has direction (−sin φ, −cos φ), its end b is the lowest point of F, and F ∩ {y<0} ≠ ∅ gives
b_y = q_y − cos φ < 0.  The point (x_r, 0) of that edge lies in F, so x_r ≤ 0 by (a); q_x > 0 then gives
tan φ ≥ q_x/q_y, q_x ≤ q_y tan φ < sin φ, x_r > q_x − sin φ > −sin φ; and F is convex with an edge on L_F, so it
lies on one side of L_F — the side containing t, i.e. x ≤ x_r + y tan φ.
(c) The line y = 0 enters F through the edge qb at x_r.  If l_y = q_y − cos φ + sin φ < 0 it leaves through the
opposite edge lt, parallel to qb at distance 1: the horizontal separation of the two lines is 1/cos φ.  Otherwise
it leaves through the edge bl at the point b + ((−b_y)/sin φ)(−cos φ, sin φ), and the chord is
x_r − (b_x − (cos φ − q_y) cot φ) = (cos φ − q_y)/(sin φ cos φ).  In the deep regime x_l = x_r − 1/cos φ ≤ −1/cos φ < −1.
(d) b = (q_x − sin φ, q_y − cos φ) has −sin φ < b_x < 0 (by (b)) and −cos φ < b_y < 0, so b ∈ A, and int F meets
the open set A near b.  ∎

*What "clockwise" is.*  A square has no sense of rotation; the content of (b) is WHICH vertex pokes past the corner
(the rightmost one, not the top one) and the lower bound tan φ ≥ q_x/q_y on the tilt of the edge through the
corner region.  In the PI's picture the top-right corner of an upright square has been turned clockwise by φ so that
it became the rightmost vertex q and its right edge became the leaning edge qb.

## 2. [T] Lemma WEDGE (no second meeter of A on the wedge side)

Let F reach around the corner from A's side, and let G be a unit square with int G ∩ int F = ∅, int G ∩ int P = ∅,
G ⊂ {x ≤ 1, y ≥ −1} (G does not cross A's far side — the floor here), and int G ∩ A ≠ ∅.  Then

    G has a point (x, y) with y < 0 and x < x_r + y tan φ,

i.e. G is NOT contained in the closed region R := {y ≥ 0} ∪ {y < 0, x ≥ x_r + y tan φ} on the wedge side of F's
leaning edge.  In particular, for EVERY φ ∈ (0°, 90°) and every admissible q, no unit square dips into A with a
vertex whose two edges both cross the line y = 0 inside the sliver [x_r, 0] (the PI's "a vertex cannot use the
wedge"): such a square would lie in R.

*Proof.*  Suppose G ⊂ R.  G has a point with y < 0 (it meets A), and every point of G with y < 0 has x ≤ 0
(int P, as in SEAL (a)).  The open chord (x_l, x_r) × {0} of F lies in int F (the line y = 0 crosses F), so G's
chord [g_l, g_r] × {0} on that line is disjoint from it and its interior points have x ≤ 0; being a segment it lies
in [x_r, 0] or in (−∞, x_l].  In the second case g_r ≤ x_l < x_r, and the points (g_r − ε′, −ε) ∈ int G (small ε, ε′)
are left of L_F below y = 0 — G ⊄ R.  So assume the chord lies in [x_r, 0] (length ≤ |x_r| < sin φ < 1).
*Upright G* = [x0, x0+1] × [y0, y0+1] with y0 < 0: its bottom edge lies in {x ≤ 0}, so x0 ≤ −1 < x_r, and its left side
at heights y ↑ 0 has x0 < x_r + y tan φ — G ⊄ R.  *Tilted G*: let v be its lowest vertex (v_y < 0) and ψ ∈ (0°, 90°)
the angle above the horizontal of the edge leaving v to the left, direction (−cos ψ, sin ψ); the other edge at v has
direction (sin ψ, cos ψ).  The vertices of G above v are at heights v_y + cos ψ, v_y + sin ψ, v_y + cos ψ + sin ψ.
*Case A (only v below y = 0).*  The chord has length |v_y|(tan ψ + cot ψ) ≤ |x_r|, so |v_y| ≤ |x_r| sin ψ cos ψ,
and its right end v_x + |v_y| tan ψ ≤ 0.  Put w := v_x − x_r + |v_y| tan φ ≥ 0 (v ∈ R).  Along the left edge the
horizontal gap to L_F is w − t (cos ψ + sin ψ tan φ) at edge parameter t, and it vanishes at t* = w/(cos ψ + sin ψ tan φ),
at height y* = v_y + w/(cot ψ + tan φ).  Since v_x ≤ −|v_y| tan ψ: w ≤ |x_r| − |v_y|(tan ψ − tan φ); if
tan ψ ≥ tan φ this gives w ≤ |x_r| < sin φ ≤ cos(ψ − φ)/cos φ = cos ψ + sin ψ tan φ (as sin φ cos φ ≤ min(sin φ, cos φ) ≤ cos(ψ − φ)), and if
tan ψ < tan φ it gives w ≤ |x_r|(1 + sin ψ cos ψ (tan φ − tan ψ)) = |x_r| cos ψ (cos ψ + sin ψ tan φ); either way
t* < 1, so the crossing lies on G's edge.  Also |x_r| < q_y tan φ gives w < (q_y + |v_y|) tan φ and so y* < q_y.
If y* < 0 the edge has points below y = 0 left of L_F — G ⊄ R.  If 0 ≤ y* < q_y the crossing point lies on the OPEN
edge qb of F (b_y < 0 ≤ y* < q_y) and the edge of G continues into int F — impossible.
*Case B (exactly one of the two side vertices below y = 0).*  The line y = 0 then cuts G between two PARALLEL edges
at horizontal distance 1/sin ψ or 1/cos ψ ≥ 1 > |x_r|: the chord cannot lie in [x_r, 0].
*Case C (v and both side vertices below y = 0, the top vertex t_G = (t_x, t_y) above).*  Then the right side vertex
(t_x + cos ψ, t_y − sin ψ) has x ≤ 0, so t_x ≤ −cos ψ; the chord's left end t_x − t_y tan ψ ≥ x_r; and the floor
gives v_y = t_y − cos ψ − sin ψ ≥ −1.  Hence |x_r| ≥ cos ψ + (cos ψ + sin ψ − 1) tan ψ = tan(45° − ψ/2) + sin ψ ≥ 1
(equality only at ψ ∈ {0°, 90°}), against |x_r| < 1.  ∎

**[F] Two stronger readings that are false (the counter-configurations).**  (i) "No second meeter of A has a point in
the wedge {y < 0, x > x_r + y tan φ}": false — F with φ = 45°, q = (0.1, 0.6) (x_r = −0.5, b = (−0.607, −0.107))
and G the 45°-square with vertices (−1.128, −1), (−0.42, −0.293), (−1.128, 0.414), (−1.835, −0.293) are
interior-disjoint (G ⊂ {x + y ≤ −0.714} ⊂ the far side of F's bottom edge), G meets A and contains (−0.6, −0.4),
which is in the wedge; G passes UNDER F and crosses A's left side — consistent with WEDGE (it has (−1.5, −0.5) left of
L_F).  (ii) Without the far-side hypothesis G ⊂ {y ≥ −1} the conclusion fails: F with φ = 60°, q = (0.05, 0.45)
(x_r = −0.729, b_y = −0.05) and the 60°-square G with top vertex (−0.53, 0.1), other vertices (−1.396, −0.4),
(−0.03, −0.766), (−0.896, −1.266) satisfy G ⊂ R (G pokes its top vertex UP through the sliver from below A's
bottom line).  So the sharp statement is exactly Lemma WEDGE: for every φ, with A's far side closed (the floor, or
any obstacle G cannot cross).

## 3. [T] Corollary SIDES and Lemma NO-SECOND (A has no second meeter at all)

Let F reach around the corner from A's side in the DEEP regime (q_y < cos φ − sin φ, so φ < 45°, b_y < −sin φ,
l_y < 0, x_l < −1) and let G be any unit square with int G ∩ int F = ∅ = int G ∩ int P, G ⊂ {x ≤ 1, y ≥ −1},
int G ∩ A ≠ ∅.  Write y_bl := b_y + (b_x + 1) tan φ for the height at which F's lower-left edge bl crosses A's left
side x = −1 (F occupies that side from y_bl up to a height > 0, since the far edge lt crosses y = 0 at x_l < −1).

**(i) [T] G's chord on the line y = 0 lies in (−∞, x_l].**  G is not contained in {y < 0} (a unit square in
{x ≤ 0, −1 ≤ y ≤ 0} is upright with its top edge on y = 0, which must avoid F's open chord, so it lies left of x_l and
misses A), so G crosses y = 0 and its chord avoids F's open chord and has x ≤ 0; if it lay in [x_r, 0] then, as in
the proof of WEDGE, Case A would give a dip |v_y| ≤ |x_r| sin ψ cos ψ < sin φ/4 < |b_y|, hence a crossing height
y* > v_y > b_y on F's open edge qb — G enters int F; Cases B and C are impossible verbatim; an upright G has chord 1.
**(ii) [T] G ∩ {y ≥ b_y} lies on the far side of F** (x ≤ F's left boundary at that height): the slab {b_y ≤ y ≤ 0}
minus int F has two components (left of F, right of L_F), G ∩ slab is convex and contains the chord of (i).  Hence
**G ∩ {x > −1} ⊂ {−1 ≤ y < y_bl}** and every point of G right of x = −1 lies UNDER F's lower boundary: A's top edge
admits no second meeter, and a second meeter crosses A's left side below y_bl or lies under F (Cor. SIDES).
**(iii) [T] Lemma NO-SECOND.**  Put h := 1 + y_bl (require y_bl < 0), c := −1 − l_x (> 0), g := 1 + l_y (> 0).  If

        min_{ψ′ ∈ [arccos h, 90°)} ( cos ψ′ + c tan ψ′ )  >  g,     in particular if  c √(1 − h²) / h > g   or   2 √(c √(1 − h²)) > g,

then NO such G exists: A's only non-pin meeter is F itself.  *Proof.*  By (ii) every vertical chord of G at x > −1
has length < h < 1, so G is not upright (chord 1) and the line x = −1 meets G within h/2 of its rightmost or leftmost
vertex; the leftmost case is impossible (right of the line G has a vertical chord ≥ 1: at distance min(sin ψ, cos ψ)
from the leftmost vertex the chord is 1/cos ψ or 1/sin ψ, and if that lies left of x = −1 the chord AT the line is
already full).  So G's rightmost vertex v_R = (x_R, y_R) has x_R > −1 and lies under F's lower boundary; its two
edges go left, the upper one at angle ψ′ above the horizontal, the lower one dropping cos ψ′, so y_R ≥ −1 + cos ψ′,
and y_R < y_bl forces cos ψ′ < h.  The upper edge stays under F's lower boundary; it reaches x = l_x (if it ended
first, at a left vertex above l_x, G's top edge would rise from below l_y into the region right of l_x at heights
≥ l_y, which is inside or right of F's far edge — but G's points at height ≥ 0 lie left of x_l by (i), and the top
edge's x only increases: contradiction), where it must pass below l: y_R + (x_R − l_x) tan ψ′ ≤ l_y.  With
x_R − l_x > c this gives cos ψ′ + c tan ψ′ < g.  The two closed forms are the bounds c tan ψ′ ≥ c tan(arccos h) and
cos ψ′ + c tan ψ′ ≥ 2 √(c sin ψ′) ≥ 2 √(c √(1 − h²)) (AM–GM).  ∎

**(iv) [T] Vertex localisation (the fallback when (iii)'s margin vanishes, i.e. F within ≈ q_y²/4 radians of
upright).**  The proof of (iii) shows, before any inequality, that a second meeter's RIGHTMOST vertex lies in
(−1, −1 + h/2] × [−1, y_bl), so its centre lies in [−1 − 1/√2, −1 + h/2 − 1/2] × [−3/2, y_bl + 1/2]; on a page that
box is bisected against the pins' and H's K′ and the container (an exact reach test), and if nothing survives there
is no second meeter.  On k5_16 pages the box overlaps the BL pin column, and the test is empty.

Every quantity is an explicit function of (q_x, q_y, φ); on a piece of F's pose space the inequalities are checked at
their worst ends in exact rationals of t = tan(θ/2) (`seal199c.sealed`, with q_x ≤ q_y tan φ substituted for q_x's
upper end — sound for dipping poses by SEAL (b) — and the exact minimum of u + c√(1−u²)/u over u = cos ψ′ ∈ (0, h]:
at u = h when h²(1−h²) ≤ c², else ≥ √c (2 − h²)): that is the SEAL LEAF.  On Y0491's BR
corner (F's certified region: φ ≤ 23°, q_y ≤ 0.11) c ≈ 0.3, h ≈ 0.35, g ≈ 0.49: 2√(c√(1−h²)) ≈ 1.06 > 0.49.

## 4. The certificate on a page (what `seal199` runs; every step an exact test)

For a pinned corner c whose two neighbours B = c(0,1), A = c(1,0) are both forced (Theorem FC), at reference side s
with slab factor λ (§5; λ = 1, s = s0 at the top), **the SEAL leaf** (`seal199c`):
1. base node {pins, H} normalised (A171/A172 multibox; EmptyBox = the pair leaf);
2. B's meeter window bisected (4 tilt sub-bins, depth ≤ 16): a piece is DROPPED when provably dead — container clip,
   multibox's exact dead test against every role's K′, A161's exact miss test against B's box, or q_y < 0 at every
   pose (no pose meets int B clear of the pin, SEAL (b)); SEALED when Lemma NO-SECOND's inequalities hold at their
   worst ends (deep regime, l_x < −1, y_bl < 0, the exact minimum bound); otherwise SPLIT.  The unsealed survivors
   at the cap are the residue; if every residue piece is in the deep regime with y_bl < 0, the fallback (iv) runs one
   exact reach test on the second meeter's centre box (h = the residue's largest 1 + y_bl); **DEAD iff the residue is
   empty (or the fallback box is empty)**: then every free meeter F of B (Theorem FC gives one) leaves A with F as
   its only non-pin meeter, against FC(A).  On Y0491: 49 sealed pieces (vol 0.0023 of the window, smallest margin
   2.7·10⁻⁴), 74 dropped, residue = the near-upright sliver (tilt ≥ 89.5°, vol < 10⁻⁶) closed by the fallback with
   h = 0.101; 2,804 exact tests, 4 s [M].
Soundness: the pieces are a superset of the free meeters' poses; each drop is an exact test; each seal is Lemma
NO-SECOND on the whole piece.  [C: geometry, SEAL; the multibox invariant of A171 on the base node.]  The certificate
row records every piece's fate (dropped / sealed with its margin / residue with the failing inequality).
**The exact multibox chain** (`seal199b`, `--chain`: {pins, H, F-sub-box, G} with G a further free meeter of A,
then the (FH) miss tests) is ALSO run on Y0491 and does NOT kill (G survives in every F sub-box): the pair test sees
only F's K′ (the part present in EVERY pose of the sub-box), which is far smaller than any actual F, so it cannot see
the seal — the lemma is not a reading of that certificate but the leaf that replaces it.

## 5. The window: the slab certificate

A page's hypothesis is about F = Δ_{s0/m} P for every m ∈ [3.82, s0] (`forced_corners.md` §2); at s0 the FC boxes
carry the pad π_i = (λ − 1)(i + 1 + 1/√2), λ = s0/m, and at λ_max the two widened boxes B⁺, A⁺ OVERLAP in the
(π_0 × π_0) square at the pin's corner — the strip through which the sampled (F, H) pairs coexist [M, A198 notes].
A certificate run at s0 with pad π(λ) is valid for every m ∈ [s0/λ, s0] (the pad is monotone), so the threshold pad
π* — the largest at which the chain still kills — gives the top slab [s0/λ*, s0] and nothing below it: at the s0
reference the pad cannot be made smaller.  **The slab certificate moves the reference.**  For a slab [s_i, s_{i+1}]
run the chain AT SIDE s′ = s_{i+1} with λ′ = s′/s_i: container [0, s′]², pins at the s′-slots with slack
η′ = (λ′ − 1)/2 (Lemma B.0: the dilated pin's centre is (s′ − λ′/2, λ′/2)), the FC boxes with pads π_i(λ′), and H's
box CONTRACTED by μ = s′/s0 (Δ_μ ∘ Δ_{s0/m} = Δ_{s′/m}; tilts unchanged).  Theorem FC's proof (§2 there) is verbatim
with s′ in place of s0.  Composition: the slabs cover [3.82, s0] and each slab's certificate excludes every m in
it, so the page is dead on the window — the same finite disjunction over a cover of the window by which Corollary
B′ / Lemma M→E (`closed_disjoint_bridge.md` B.1, `instratum_bridge.md` E.2) compose the scoreboard's window rows
from per-slab certificates at sides above the slab.  Slab count: with the largest killing ratio λ′,
N = ⌈ln(s0/3.82) / ln λ′⌉; the cost is N runs of the chain.  [T] the composition; [C] the N runs.

## 6. Lean shape (obligations)

L1 `quadrant_halfplane`: a convex body disjoint from an open quadrant lies in a half-plane {b y ≥ a x}, a, b ≥ 0.
L2 `rightmost_vertex`: a non-axis-parallel unit square has a unique rightmost vertex with the explicit neighbours
b, t (formulas of §0).  L3 `seal_chord`: the two chord formulas of SEAL (c).  L4 `wedge`: the case analysis of §2 —
finitely many polynomial inequalities in (q_x, q_y, tan φ, v, tan ψ) per case, the trigonometric fact
tan(45° − ψ/2) + sin ψ ≥ 1, the parallel-edge chord bound; discharged by `nlinarith`/interval arithmetic.
L5 the transport of §5: `dilation_bridge` with reference side s′ (exists) + the pin-centre shift (λ′ − 1)/2.
L6 the certificate replay: multibox's exact dead test and A161's miss test are already the replayable objects of
A171/A161; the chain of §4 is a list of them plus the FC bookkeeping over `Fin 11`.
