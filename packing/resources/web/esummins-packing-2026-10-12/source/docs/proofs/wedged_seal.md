# WEDGED-SEAL — a corner meeter touching both walls is alone: the PI's direct proof, the two-line proof from Lemma PUSH, and where it sits (= Cor. B1; not a corollary of NO-SECOND) — A239, 2026-09-16

The PI (11:00): *"take a square and push it into the corner so two of its corners touch the two adjacent walls: no
second meeter of the corner box is geometrically permitted, for any rotation."*  This file states the lemma for
every n and every side, gives (i) the PI's direct proof — the sealed triangle, the two wedges, the segment-crossing
computation with the small and the large tilts handled — and (ii) a two-line proof from Lemma PUSH (`k0_count.md`
§2), and says honestly where the statement sits in the lab: it IS Corollary B1 of `sideband.md` §4 ("pressed ⇒
lonely", A169, proved there from Theorem B's four clauses), it is NOT a corollary of A199's NO-SECOND (different
hypotheses, §4), and its mechanism is A199's WEDGE mechanism in the simplest setting.  What is new: two proofs that
use neither Theorem B nor the certificates, and the Lean theorem `wedged_seal` (its only non-standard dependence is
the `lemma_PUSH` axiom).  Tags: [T] proved here, [S] routine given cited items, [M] measured, [C] obligation.
Code `attempts/A239-rings-below-4/code/geom239.py` (`wedged_square`, `wedge_regions`, `f_alpha`, `b0star`,
`second_meeter_search`), `test239.py`; page `docs/residue_map/campaigns/A239-rings-below-4/wedged_seal.svg`; Lean
`Statements/Open/WedgedSeal.lean`.

## 0. Verdict

> **[T] Lemma WEDGED-SEAL (any n, any side).**  Let Q be a unit square in the closed quadrant {u ≥ 0, v ≥ 0} of a
> corner with a vertex on the floor v = 0 and a vertex on the wall u = 0 (tilt θ ∈ [0°, 90°]; θ = 0 is the flush
> slot square).  Then no unit square G of the quadrant with int G ∩ int Q = ∅ has int G ∩ (0, 1)² ≠ ∅: **the open
> corner box has no second meeter, at any tilt.**  Two proofs: the direct one (§2: Q covers the box except a SEALED
> triangle of area sin θ cos θ / 2 and two WEDGES of apex angles θ and 90° − θ; a unit square cannot put a point into
> a wedge without crossing the wall or the bounding edge — the crossing computed on the SEGMENT, with the far
> quadrant at the edge's end excluded by a separation argument and the wedge case closed by Lemma B0*) and the
> short one (§3: the separating normal into Q has both components positive by PUSH (ii), the normal into G has a
> positive component by PUSH (i) — contradiction).  **Where it sits** (§4): the statement is `sideband.md` Cor. B1
> (A169) verbatim; NO-SECOND (A199) is about the slot BESIDE a pin and has hypotheses (a pin, a square reaching
> around it in the deep regime, an explicit inequality) that WEDGED-SEAL does not need, so WEDGED-SEAL is not its
> corollary; the "a vertex cannot use a wedge" mechanism is A199's Lemma WEDGE mechanism.  **Consequence** (§5): in
> a doubly-met open corner neither meeter touches both walls — one touches at most the floor, the other at most the
> wall (PUSH / HOLD's setting) — and a corner meeter touching both walls is ALONE, so K0-FREE teleports it.
> **Lean** (§6): `wedged_seal` is a theorem (via `sat_selection_thm` and `lemma_PUSH`); no new axiom.  [M] 5 × 20 000
> random meeters, 0 second meeters; the wedge inequality on a 0.05° grid.  k0_00 unchanged (a wedged meeter never
> occurs in a doubly-met corner: the lemma is a structural fact used by PUSH / HOLD, not a new kill).

## 1. Setting

Corner frame (u, v) = distances from the two walls; the quadrant {u ≥ 0, v ≥ 0}; the open corner box (0, 1)².  A
unit square MEETS the box iff its interior meets it.  Q WEDGED: a vertex on the floor and a vertex on the wall.
With b := cos θ, l := sin θ (θ the angle of the edge from the floor vertex to the wall vertex, measured from the
vertical; θ ∈ (0°, 90°), the flush case θ = 0 being Cor. B1's trivial case [0, 1]² = the slot square) the vertices
are L = (l, 0) (lowest), W = (0, b) (leftmost), R = L + (b, l) = (l + b, l) (rightmost), T = W + (b, l) =
(b, b + l) (highest); the centre is (w/2, w/2) with w = b + l ∈ [1, √2] — the PRESSED square of `sideband.md`.
Notation: t := (b, l) (the direction of the edge L → R), n := (−l, b) (its inward normal); ℓ := the line through
L and R.  Q = {x : 0 ≤ t·(x − L) ≤ 1, 0 ≤ n·(x − L) ≤ 1}.  w(φ) := |cos φ| + |sin φ|: a unit square of tilt ψ has
half-width w(φ − ψ)/2 in the unit direction at angle φ.

**Lemma B0\* (k0_count.md §1 = the mirror of sideband.md's Lemma B0).**  For ζ ∈ [0°, 90°] and every φ:
w(φ) + (cos ζ − sin ζ) w(φ + ζ) ≥ 2 cos² ζ.  [T there; checked on a 0.25° grid, min −4·10⁻¹⁶, `test239.py`.]

**What Q leaves uncovered in the box.**  The far vertices have u, v = b + l ≥ 1, so the box minus Q is: the SEALED
TRIANGLE Δ₀ = conv(0, L, W) (between the walls and the near edge W–L; area bl/2); the FLOOR WEDGE T_f = {l < u < 1,
0 < v < (u − l) tan θ} (between the floor and the edge L–R; apex L, angle θ; its top at u = 1 is (1 − l) tan θ ≤ l
< 1, so the wedge is cut by the box's far side u = 1, not by Q); and the WALL WEDGE T_w, the mirror (apex W, angle
90° − θ).  Nothing else: a point of the box with u ≥ l, v ≥ b... — precisely, a point of [0, 1)² not in Q lies below
ℓ (T_f or its closure), left of the edge W–T (T_w), or below the edge W–L (Δ₀), since the two far edges of Q pass
outside the box.

## 2. [T] The direct proof (the PI's sketch made exact)

**Step 0 (the sealed triangle).**  No unit square G of the quadrant interior-disjoint from Q meets int Δ₀.  Δ₀ has
diameter 1 (the hypotenuse |LW| = 1) while G contains a segment of length √2, so G ⊄ Δ₀; a point p ∈ int G ∩ int Δ₀
and a point q ∈ G ∖ Δ₀ are joined by [p, q) ⊂ int G (p interior, G convex), which crosses ∂Δ₀ at a point r ∈ int G;
r on the floor or the wall contradicts G ⊂ quadrant (int G would contain points with v < 0 or u < 0), r on the
open edge W–L is a boundary point of the convex body Q, whose every neighbourhood meets int Q — contradiction; r = L
or W likewise.  ∎  (The same argument shows every region bounded by walls and members' edges in which no unit
square fits is waste: `realign.md` §1.2, `pocket_waste.md` J2.)

**The wedge claim.**  No such G meets T_f (T_w is the mirror).  Suppose p ∈ int G ∩ T_f; write τ := t·(p − L) and
ν := n·(p − L) < 0; from u_p < 1 and v_p < (u_p − l) tan θ, 0 < τ < (1 − l)/b =: τ* < 1 (as 1 − l ≤ b) and
−τ tan θ < ν < 0.

**Step 1 (the strip).**  Let Σ̄ := {0 ≤ t·(x − L) ≤ 1} (the strip between the perpendiculars to ℓ through L and R)
and Δ := Σ̄ ∩ {n·(x − L) ≤ 0} ∩ {v ≥ 0} = the closed right triangle L, R, R′ with R′ = (l + 1/b, 0) (legs |LR| = 1
and |RR′| = tan θ, right angle at R).  Then **G ∩ Σ̄ ⊂ Δ**: a point q ∈ G ∩ Σ̄ with n·(q − L) > 0 gives, on [p, q),
points with n ∈ (0, ε) and t ∈ (0, 1) (t is a convex combination of τ ∈ (0, 1) and t_q ∈ [0, 1], strictly inside for
λ < 1) — points of int Q ∩ int G.  And G ⊂ {v ≥ 0}.
**Step 2 (nothing left of L).**  **G ⊂ {t·(x − L) ≥ 0}**: a point q with t_q < 0 gives on [p, q) ⊂ int G a point
with t = 0, which by Step 1 lies in Δ ∩ {t = 0} = {L}; so L ∈ int G, and L ∈ Q, so int G ∩ int Q ≠ ∅.
**Step 3 (G does not fit in the strip).**  A unit square contains a disc of radius ½; Δ's inradius is
(1 + tan θ − 1/cos θ)/2 < ½ (⟺ sin θ < 1).  So G ⊄ Σ̄, hence (Step 2) G has points with t·(x − L) > 1: **G leaves
the strip through the leg R–R′** and continues to the right of R.
**Step 4 (the forbidden quadrant).**  Let K := {t·(x − L) < 1, n·(x − L) > 0} (the open quadrant with apex R
opening to the upper left).  **G ∩ K = ∅**: a point of G ∩ K has t ∈ [0, 1) by Step 2, so it is in Σ̄, so in Δ
(Step 1), so n ≤ 0.  (This is the crossing computation "with the SEGMENT, not the line": G may cross the LINE ℓ,
but only beyond R, where Q has ended; crossing it on the segment L–R or reaching the region above the segment from
inside the strip is what K forbids.)
**Step 5 (separation).**  G is compact convex, K open convex, disjoint: a line separates them.  As in `corner_seal.md`
SEAL (a), a linear functional bounded above on the cone K = R + {−μ t + λ n : μ, λ > 0} has the form m = b′ t − a n
with a, b′ ≥ 0, (a, b′) ≠ 0, and sup_K m·x = m·R; so **G ⊂ {a n·(x − R) ≤ b′ t·(x − R)}**, the half-plane below the
line through R with direction a t + b′ n, i.e. at angle α := θ + arctan(b′/a) ∈ [θ, θ + 90°] above the horizontal.
The case α ≥ 90° (b′ cos θ ≥ a sin θ... precisely b′ sin θ ≥ a cos θ) is impossible: p has u_p < 1 ≤ u_R and v_p
< (1 − l) tan θ ≤ l = v_R (as 1 − l ≤ b), and m·(p − R) = (b′ b + a l)(u_p − u_R) + (b′ l − a b)(v_p − v_R) < 0
then, against p ∈ G.  So **α ∈ [θ, 90°)**, and G lies in the WEDGE with apex A₀ = (u_A, 0), u_A = l + b −
l cot α (where the line meets the floor), between the floor and the ray at angle α: {v ≥ 0} ∩ {(u − u_A) sin α −
v cos α ≥ 0}.  (α = θ, i.e. b′ = 0, is the wedge under ℓ itself with A₀ = L; α = 90°, i.e. a = 0, is excluded.)
**Step 6 (the wedge computation, Lemma B0\*).**  Let G have tilt ψ and centre c.  Above the floor: v_c ≥ w(ψ)/2.
Below the α-line: −sin α (u_c − u_A) + cos α v_c + w(ψ − α)/2 ≤ 0.  Hence sin α (u_c − u_A) ≥ [cos α w(ψ) +
w(ψ − α)]/2 and, with min_G u = u_c − w(ψ)/2,
    sin α (min_G u − u_A) ≥ [(cos α − sin α) w(ψ) + w(ψ − α)]/2 ≥ cos² α       (B0\* with ζ = α, φ = ψ − α),
so **min_G u ≥ f(α) := l + b − l cot α + cos² α / sin α** (this is `k0_count.md` PUSH (ii)'s computation
"min_A u ≥ u₀ + cos² α / sin α" with u₀ = u_A; it is sharp: G's edge along the line, its vertex on the floor).
**Step 7 (f(α) ≥ 1 on [θ, 90°)).**  f(α) − 1 = (l + b − 1) + cos α (cos α − l)/sin α.  Write x := cos α ∈ (0, b].
(i) If b ≥ l/2 (tan θ ≤ 2): x(x − l) ≥ −l²/4 and sin α ≥ l give f ≥ l + b − l/4 = ¾ sin θ + cos θ ≥ 1, since
¾ sin θ ≥ 1 − cos θ ⟺ tan(θ/2) ≤ ¾ ⟺ θ ≤ 73.7°, and tan θ ≤ 2 gives θ ≤ 63.5°.  (ii) If b < l/2: x(x − l) is
decreasing on [0, l/2] ⊃ [0, b], so x(x − l) ≥ b(b − l) (negative), and sin α ≥ l gives f ≥ l + b + b(b − l)/l =
1/sin θ ≥ 1.  In both cases min_G u ≥ 1, against u_p < 1.  ∎
**The small and the large tilts.**  θ → 0: the floor wedge T_f flattens (apex angle θ) and the wall wedge T_w
opens to a quadrant — f(θ) = 1/sin θ → ∞ on the floor side, while on the wall side the mirror computation gives
min_G v ≥ 1/cos θ → 1: a flush square beside the slot square just fails to meet the open box (equality at
θ = 0 is the closed-box touching, consistent with Cor. B1's open box).  θ → 90°: the roles swap.  Both bounds of
Step 7 are strict on (0°, 90°); the drawn minimum of f − 1 over α is ≥ 0.004 on [0.5°, 89.5°] (page (c)).

## 3. [T] The proof from Lemma PUSH (two lines)

Q and G are interior-disjoint convex bodies, so a line {n·x = β}, |n| = 1, weakly separates them: G ⊂ {n·x ≤ β},
Q ⊂ {n·x ≥ β} (the separating axis is an edge normal of G or of Q: Lemma SAT, `local_certificate.md` §1 — in Lean
`sat_selection_thm`).  Both squares are in the quadrant and both meet (0, 1)².  Lemma PUSH (ii) for the ordered
pair (G, Q): Q touches the floor, so n_u > 0; Q touches the wall, so n_v > 0.  Lemma PUSH (i) for the pair (Q, G)
with the normal −n pointing into G: (−n)_u > 0 or (−n)_v > 0.  Contradiction.  ∎  (PUSH itself is proved in
`k0_count.md` §2 from Lemma B0 / B0′ / B0\*; the direct proof of §2 uses only B0\*, Step 6 being PUSH (ii)'s own
inequality at the wedge.)

## 4. Where the lemma sits: Cor. B1, and A199's SEAL / WEDGE / NO-SECOND

* **[T] It is Corollary B1 of `sideband.md` §4 (A169)** — "the pressed square (centre (g, g), g = w(θ)/2, any tilt
  θ) admits no second meeter of (0, 1)²" — the wedged square IS the pressed square (its centre is (w/2, w/2)).  B1
  is proved there by Theorem B's exact second-meeter criterion: the four clauses (NE), (W), (S), (P) each fail for
  the pressed square (a sinusoid argument per clause).  `k0_count.md` §1 already uses it ("a meeter of a doubly-met
  corner touches at most one of c's walls (Cor. B1)").  **So the statement is not new; the two proofs of §2–3 are
  Theorem-B-free, and §6's Lean theorem is new** (B1 had no Lean form: Theorem B is `SecondMeeterCriterion` [C]
  in `Sideband.lean`).
* **Not a corollary of NO-SECOND.**  A199's setting (`corner_seal.md` §0) is a PIN P settled in the corner and a
  square F reaching around it into the slot A beside the pin from the slot B above it; Lemma SEAL forces F to lean
  and to cut A's top edge, Lemma WEDGE says no second meeter of A can sit in the region on the wedge side of F's
  leaning edge, Cor. SIDES / Lemma NO-SECOND say that in the DEEP regime, under an explicit inequality
  (c √(1 − h²)/h > g or 2√(c√(1 − h²)) > g) whose margin vanishes as F becomes upright, A has no second meeter at all.
  WEDGED-SEAL has no pin, no reaching square, no regime and no inequality: its hypotheses are two touched walls.
  Nothing in NO-SECOND's chain can be instantiated to yield it (there is no P and no F), and conversely NO-SECOND's
  conclusion is about a box (the slot A) whose two "walls" are the container floor and the pin's side — WEDGED-SEAL
  applied to A would need a square touching the pin's side and the floor with a vertex each, which F does not.
* **The same mechanism.**  Lemma WEDGE's content — "a unit square cannot place a vertex in a wedge of angle < 90°
  between an obstacle edge and a wall without crossing one of them" (the sliver [x_r, 0] at the pin's corner there;
  T_f, T_w here) — is exactly Steps 1–7; A199 does the crossing computation with F's edge as the obstacle and three
  cases on which vertices of G dip below the line, and here the obstacle is Q's edge with the far quadrant K
  taking the place of A199's Case C.  The two [F] readings of A199 §2 (a second meeter CAN have a point in the wedge
  beyond the obstacle's end; the far side must be closed) are both visible here: G may cross ℓ beyond R (Step 4
  allows it), and the floor must be a wall (Step 6 uses v ≥ 0; without it the mirror of A199's counter-configuration
  (ii) pokes a vertex up through T_f from below).

## 5. Consequences (any n)

**[T] In a doubly-met open corner neither meeter touches both walls.**  With Lemma A2 (`sideband.md`: two meeters
sit in distinct cells of the 2 × 2 grid at 1) and Cor. B1's cell reading: the meeter in the NW cell can touch only
the wall, the one in the SE cell only the floor, the NE cell neither.  This is the setting of Lemma PUSH (ii) / HOLD
(`k0_count.md` §2–3: the push away from the corner ALONG the touched wall, the holder along it) and of TILT-MIN
(`pocket_waste.md` §1: the flat meeter at offset δ > 0 from its second wall).  **[T] A corner meeter touching both
walls is alone**, so the corner is singly met and K0-FREE (`k0_route.md` §3, Lean `teleport_packing`) exchanges it
into the flush slot square at the same side: a wedged meeter is never an obstacle to settling its corner.  For the
rings of `attempts/A239-rings-below-4/notes/rings_below_4.md` this fixes the shape of every corner crowd: one
square on each wall, the corner triangle between them sealed by neither.

## 6. Lean (`Statements/Open/WedgedSeal.lean`)

`Wedged q` := (∃ p ∈ q.set, p.2 = 0) ∧ (∃ p ∈ q.set, p.1 = 0).  Theorems: `Separates.symm`;
`wedged_seal_of_separates` (q wedged, g a second meeter, both in the quadrant with t ∈ [0, 1], a `Separates n β g q`
witness ⟹ False: the two PUSH applications of §3; depends on the axiom `lemma_PUSH` only); `dot_decomp`,
`support_le` (|a·(p − c)| ≤ (|a·e| + |a·e⊥|)/2 for p in a square with edge direction e), `separates_of_axis`,
`separates_of_gsel` (a nonnegative selection row `gsel qw qo k eps` of Lemma SAT is a `Separates` witness with
normal eps·a_k(θ_w) and level eps a·c_w + ½); **`wedged_seal`** (the lemma with `Disjoint (interior g.set)
(interior q.set)` as hypothesis, via `sat_selection_thm`).  `lake build` + `lean/audit.py` exit 0, no sorry;
`#print axioms wedged_seal` = std + `lemma_PUSH`.  Obligation: none new (O-PUSH of `k0_count.md` §7 covers
`lemma_PUSH`; the direct proof of §2 would give a PUSH-free formalisation from B0\*, obligation O-WEDGE-DIRECT [S]).

## 7. Numerics and the page [M]

`test239.py`: for θ ∈ {5°, 20°, 45°, 70°, 85°} the wedged square is in the quadrant, touches both walls, meets the
box, its far vertices are at cos θ + sin θ ≥ 1; 20 000 random unit squares of the quadrant meeting the box per θ,
interior-disjoint from Q: 0 (the largest SAT gap −0.005 at 5° and 85°, −0.09 at 45°); min_{α ∈ [θ, 90°)} f(α) ≥ 1
on a 0.01° grid (1.081 / 1.252 / 1.280 / 1.064 / 1.004); Lemma B0\* on a 0.25° grid.  Page `wedged_seal.svg`:
(a) the wedged square at 30° with the sealed triangle hatched and the wedges shaded, (b) the proof objects (strip,
Δ, the forbidden quadrant K, the extremal square G\* with min u = 1/sin θ, the α-line and A₀), (c) f(α) − 1 and
the two bounds of Step 7, (d) the consequence at A237's window crowd with PUSH's normal; every panel geometry-
checked, note per panel with the time per step.
