# CONSTRUCT TOWARDS a 12-stuck ring: the propagation rules, the supplier patterns, and why they do not yet close below 4 — A246, 2026-09-16

The PI (21:30): *"is there not a way we can try and construct towards a ring, and show that it's not possible with
s < 4?"*  The statement is **STUCK-EXIST(11)**: no packing of 11 unit squares at side s < 4 has all twelve border
cells (four corner boxes c00, eight wall slots c01 / c10; A243 `wall_slot243.md`) doubly met.  Pure existence: no
locks, no forces, no minimiser.  This note writes the construction as a propagation around the perimeter — per
corner the two meeters' variables, per wall slot its second supplier — proves each propagation rule from the cited
lemmas (two of them new: SQUARE-IN-TRIANGLE and NOT-SELF-SUFFICIENT, closing A244's O-NO-SELF-SUFFICIENT), tests every
rule on the corpus, composes them per supplier pattern, and says plainly what closes.  Tags: [T] proved here,
[S] proof route with a gap, [M] measured, [F] fails, [C] obligation.  Code `attempts/A246-construct-towards/code/`
(`geom246`, `check246`, `interval246`, `slotmet246`, `test246`, `pages246`, `run246.sh`), results
`results/construct246.{md,jsonl}`, `results/slotmet246_<eta>.json`, pages
`docs/residue_map/campaigns/A246-construct-towards/{corner_propagation,tight_case}.svg`, Lean
`Statements/Open/StuckExist.lean`.  Sources: A244 `twelve244.md`, A243 `wall_slot243.md`, A239 `rings_below_4.md`,
`pocket_waste.md` (TILT-MIN, DEPTH-BUDGET), `wedged_seal.md` (Cor. B1), `ring_capacity.md` (Lemma TWO).

## 0. Verdict

> **[T] The propagation rules, all n-general** (§2): TWO-CORNERS (no square meets two corner boxes; so 8 distinct
> meeters and f = n − 8 = 3 free squares at n = 11), MAX-FIVE (one square meets ≤ 5 cells, only as its own corner's
> triple + the far slot of each of its walls; a free square ≤ 4; cells of opposite walls never), SQUARE-IN-TRIANGLE
> (a unit square inside the right triangle with legs a, b forces 1/a + 1/b ≤ 1), **NOT-SELF-SUFFICIENT** (two disjoint
> squares cannot both meet all three cells of one corner — proved by the separating line, which must cross all three
> cells, hence descend, hence cut a triangle with 1/u₀ + 1/v₀ > 1 that holds no unit square), TYPE-F-OWN (a corner
> with a flat meeter on a wall supplies exactly 4 of its 6 incidences: the flat meeter never meets the wall slot, the
> partner never meets the floor slot, and the partner's reach R′ = w(θ) − (δ − sin θ) tan θ ≥ 1 puts its top at height
> ≥ 2), ADJ-REACH (an adjacent-corner supplier has extent > s − 3 along the shared wall — vacuous below 4, dead above
> 3 + √2), and Lemma TWO on the centre.  **[T] CAP-REDUCTION** for SLOT-MET (each square of a counterexample has
> exactly its leftmost vertex left of u = 1, in the box) and **[T-computed] SLOT-MET(η)**: for meetings of depth ≥ η
> the claim is certified by interval branch-and-bound, η = 0.05, 10⁻³, 10⁻⁴, 10⁻⁵, 10⁻⁶, 10⁻⁷ in about a second each (191 525 …
> 649 243 boxes, guard 10⁻⁹, `results/slotmet246_*.json`); the depth-free limit stays [S].
>
> **[M] Every rule holds on the corpus** (§4): 282 corpus 12-stuck crowds, 34 certified candidates: 0 violations
> of any lemma; the sub-4 attempts (A244's 304 near-4 poses, two fresh ones at ŝ and 3.95) break NOT-SELF-SUFFICIENT
> and TYPE-F-OWN — the rules are exactly what an overlapping candidate cheats on.
>
> **[F] The composition does not force s ≥ 4** (§3): the rules bound COUNTS (outside demand ≥ 4 incidences, ≥ 8 when
> all corners are type F; ADJ supply ≤ one incidence per flat meeter, none from a partner; free supply ≤ 4 per free
> square) and the counts are satisfiable with f = 3 at every side; the only rules carrying s (ADJ-REACH, the flat
> ADJ condition δ > s − 3, Lemma TWO) are satisfiable below 4 too — a wall with two flat meeters at offsets
> δ, δ′ > s − 3 is a packing for s < 4 (δ + δ′ ≤ s − 2 ⟺ possible iff s < 4 once δ, δ′ > s − 3).  So every wall pattern
> is LOCALLY feasible below 4 and the obstruction A244 measures (residual 1.4·10⁻² at ŝ) is GLOBAL: it is the room for
> the partners on the side walls once the flat meeters are deep, i.e. POCKET(11) again.  **STUCK-EXIST(11) is NOT
> closed below 4.**  What is closed: the propagation is now a set of proved rules with a per-pattern reduction (§3.4)
> whose smallest open instance is 8 poses + s — the same object A242/A243 could not certify, with a sharper hypothesis.

## 1. Setting, variables, suppliers

Container [0, s]², 2 + √2 < s < 4.  Corner c has frame (u, v) (distances to its two walls); cells c00 = (0,1)²,
c01 = (0,1)×(1,2) up its wall, c10 = (1,2)×(0,1) along its floor (open; a square MEETS a cell iff their interiors
overlap).  M_c := the squares meeting c00, |M_c| ≥ 2.  **Per corner** the two meeters' variables: for a meeter lying
on a wall of c (a FLAT meeter, tilt 0 mod 90°, touching that wall) its offset δ from the other wall; for a tilted
meeter its tilt θ (the angle of the edge leaving its lowest vertex, in the frame whose floor is the other meeter's
wall) and lowest vertex (x_v, y_v).  A corner is **type F** (one flat meeter on one of its walls; by ONE-TILTED and
WEDGED-SEAL the other is tilted and touches at most the other wall) or **type T** (both tilted).  **Per slot** the
SECOND supplier (SLOT-MET gives one own meeter): OWN (the corner's other meeter), ADJ (a meeter of the adjacent corner
along that wall), FREE (a square meeting no corner box); FAR (a meeter of a non-adjacent corner) is impossible (§2 B).
The 12-cell condition asks 24 incidences; the propagation is: place M_c, read off which of c's four slot incidences
are own, demand the rest from the wall (ADJ) or the pocket (FREE), and go round.

## 2. The propagation rules

**A. TWO-CORNERS [T].**  Two corner boxes differ by > s − 2 > √2 in a coordinate and a unit square has extent ≤ √2 in
every direction, so no square meets two boxes: the M_c are disjoint, Σ|M_c| ≤ n, and f := n − Σ|M_c| ≤ n − 8 free
squares (3 at n = 11).  Same computation: a square meeting cells of two OPPOSITE walls has extent > s − 2.  ∎

**B. MAX-FIVE [T].**  A square meets cells of at most two adjacent walls (A); on one wall the cells' along-wall
intervals are [0,1], [1,2], [s−2, s−1], [s−1, s], and meeting all four needs extent > s − 2: ≤ 3 per wall, and 3 only
as {c00, c10, c′10} or {c10, c′10, c′00} (extent > s − 3).  On two adjacent walls (floor of c, wall of c) the far
boxes c′00 (x > s − 1) and c″00 (y > s − 1) are out — a point of either with a point of a cell of the other wall is
> s − 2 away in a coordinate — so the cells available are c00, c10, c′10, c01, c″01: **five**, and a square meeting
no box meets ≤ 4.  [M] A244's grid: 5 at ŝ with exactly this witness.  ∎

**C. SQUARE-IN-TRIANGLE [T] (any tilt).**  Let a unit square Q lie in T = {u ≥ 0, v ≥ 0, u/a + v/b ≤ 1}, a, b > 0.
Then 1/a + 1/b ≤ 1.  *Proof.*  Tilt φ ∈ [0, 90°), centre (c_u, c_v), edge directions e₀ = (cos φ, sin φ),
e₁ = (−sin φ, cos φ), w = cos φ + sin φ.  Q ⊆ {u ≥ 0}, {v ≥ 0} give c_u, c_v ≥ w/2; Q ⊆ {αu + βv ≤ 1} (α = 1/a,
β = 1/b) gives α c_u + β c_v + h ≤ 1 with h = (|α cos φ + β sin φ| + |β cos φ − α sin φ|)/2 the half-width of Q in
direction (α, β).  So (α + β) w/2 + h ≤ 1, and it suffices that h ≥ (α + β)(1 − w/2).  Case β cos φ ≥ α sin φ:
2h = (α + β) cos φ + (β − α) sin φ and the claim is β sin φ ≥ (α + β)(1 − cos φ); its worst case α = β cot φ reads
sin²φ ≥ (sin φ + cos φ)(1 − cos φ) ⟺ (1 − sin φ)(1 − cos φ) ≥ 0.  Case β cos φ < α sin φ: 2h = α(cos φ + sin φ) +
β(sin φ − cos φ) and the claim is α(cos φ + sin φ − 1) ≥ β(1 − sin φ); with β < α tan φ it suffices that
cos φ (cos φ + sin φ − 1) ≥ sin φ (1 − sin φ) ⟺ (1 − sin φ)(1 − cos φ) ≥ 0.  ∎  (Equivalently: the largest
axis-aligned inscribed square ab/(a + b) is at least as large as any tilted one.)  [M] `test246`: the inequality on a
721 × 60 × 60 grid, slack ≥ −9·10⁻¹⁶; 20 000 random squares.

**D. NOT-SELF-SUFFICIENT [T] (any n, any side).**  Two interior-disjoint unit squares A, B in the closed quadrant
cannot both meet c00, c01 and c10.  *Proof.*  int A, int B are disjoint open convex sets, so a line ℓ separates them:
A ⊆ H⁻, B ⊆ H⁺ (closed half-planes), int A, int B in the open ones.  Each open cell contains an interior point of A
and one of B, hence (convexity) a point of ℓ: ℓ meets (0,1)×(1,2) and (1,2)×(0,1), so it is neither vertical nor of
slope ≥ 0 (a point with u < 1, v > 1 and one with u > 1, v < 1 lie on it): **ℓ descends**, crossing the axes at
u₀, v₀ > 0, ℓ = {u/u₀ + v/v₀ = 1}.  ℓ meets the open box iff 1/u₀ + 1/v₀ > 1 (the box's values of u/u₀ + v/v₀ fill
(0, 1/u₀ + 1/v₀)).  The square on the lower-left side lies in {u ≥ 0, v ≥ 0, u/u₀ + v/v₀ ≤ 1}, a right triangle with
legs u₀, v₀ — impossible by C.  ∎  Corollary (OUTSIDE-SUPPLY): a corner with |M_c| = 2 gets at most **3** of its 4
slot incidences from its own meeters; ≥ 1 comes from ADJ or FREE.  [M] 1500 + 200 000 restarts (A244, `test246`), the
example A = [0.1, 1.1]×[0.85, 1.85], B tilted 70° with leftmost vertex (0.95, 0.342) shows two squares CAN share c00
and c10 (B misses c01): the lemma is sharp in its hypothesis.

**E. TYPE-F-OWN [T].**  Corner c of type F: flat meeter A = [δ, 1 + δ] × [0, 1] on the floor (0 < δ < 1), partner B
of tilt θ with lowest vertex (x_v, y_v), sin θ ≤ x_v ≤ δ, y_v ≥ 1 − (δ − x_v) tan θ (TILT-MIN).  Then (i) A meets c00
and c10 and not c01 (A ⊆ {v ≤ 1}); (ii) B meets c00 and c01 and not c10: B ∩ {v < 1} lies under the edge leaving
(x_v, y_v) to the right, whose abscissa at height v is x_v + (v − y_v) cot θ ≤ x_v + (δ − x_v) = δ < 1, so no point of B
has u > 1 and v < 1; and B's leftmost vertex (x_v − sin θ, y_v + cos θ) has height > 1 (cos θ > (δ − sin θ) tan θ
⟺ 1 > δ sin θ) and < 2, u ∈ [0, 1): B meets c01.  So the corner supplies **exactly 4** of its 6 incidences: both
slots need an outside supplier.  (iii) **R′ ≥ 1**: the partner's extent above height y_v is w(θ), and w(θ) −
(δ − sin θ) tan θ ≥ 1 for sin θ ≤ δ ≤ 1: R′ decreases in δ, and cos θ · (R′(θ, 1) − 1) = cos²θ + sin θ cos θ −
sin θ (1 − sin θ) − cos θ = (1 − sin θ)(1 − cos θ) ≥ 0 (grid check on 4000 × 50 points, slack ≥ 5·10⁻⁹, `test246`);
so the crowd occupies [0, ≥ 2] along the partner's wall and [0, 1 + δ] along the flat meeter's, with equality only
as θ → 0 or 90°.  ∎  Consequence for ADJ: a **partner never
supplies the adjacent corner's floor slot** (its part below height 1 has u ≤ δ < 1 < s − 2), and a **flat meeter
supplies the far slot of its wall iff 1 + δ > s − 2, i.e. δ > s − 3**.

**F. ADJ-REACH [T]** (A244 CROSS-CORNER-REACH): an ADJ supplier of c′10 from M_c has a point with u < 1 (the box) and
one with u > s − 2: extent > s − 3 along the wall — vacuous for s < 3 + √2 unless the supplier is flat (E).  **Lemma
TWO [T]** (`ring_capacity.md` §2.5): at most one square lies inside the centre (1, s − 1)² (side < 2), so ≥ 2 of the 3
free squares meet a border cell that is already doubly met or supply one.

**G. SLOT-MET: CAP-REDUCTION [T] and the certificate [T-computed].**  Suppose A, B disjoint in the quadrant, both meet
the box, both avoid the slot Q₂ = (0,1)×(1,2).  (1) A convex body disjoint from the open quadrant {u < 1, v > 1} with
a point in the box lies below a line of slope ≥ 0 through (1,1), so A ∩ {u ≤ 1} ⊆ [0,1]² (A243 §2 (1)); A ⊄ [0,1]²
(the flush square is lonely, Cor. B1), so A crosses u = 1 with a chord ⊆ [0,1].  (2) The separating line ℓ of A, B
crosses the box; it is not vertical (the left square would sit in a strip of width < 1), not horizontal (the lower
one in a strip of height < 1), and not descending (D's triangle); so ℓ ascends, A above it, B below, and the chords
on u = 1 are [a₁, a₂] ⊆ [v_ℓ, 1], [b₁, b₂] ⊆ [0, v_ℓ] with v_ℓ = ℓ(1) ∈ (0, 1) — each of length < 1, so u = 1 cuts a
CORNER CAP (one vertex on one side).  (3) The cap is on the LEFT: three vertices left of u = 1 lie in [0,1]² and span
the full v-extent w(θ) ≥ 1, forcing the flush square.  Hence each square is W + {a e₀ + b e₁}, W = (1 − a, v) its
leftmost vertex, 0 < a ≤ min(sin θ, cos θ), v ≥ cos θ (lowest vertex above the floor), v cos θ + a sin θ ≤ cos θ (the
chord's top ≤ 1), and WLOG v_A ≥ v_B.  ∎  The B&B (`slotmet246`) bisects the 6-box (θ, a, v)², discards a box only
when an interval enclosure shows every pose in it violates a constraint or has SAT overlap depth > 0 (guard 10⁻⁹,
`interval246`, soundness-tested on 15 000 samples), and certifies: **no pair with both box depths ≥ η is disjoint**
— η = 0.05 (191 525 boxes), 10⁻³ (345 941), 10⁻⁴ (397 321), 10⁻⁵ (476 943, box floor 10⁻⁷), 10⁻⁶ (566 843),
10⁻⁷ (649 243, floor 10⁻⁹), each in about a second.  The margin
degenerates as η → 0 (a flush A and a B of depth ε overlap by ≈ ε), so the depth-free claim is exactly the [S] left.

## 3. The supplier patterns and the composed inequalities

**3.1 Per corner.**  Own slot incidences k_c ∈ {2, 3} (D; k_c = 2 exactly for type F by E), outside demand
o_c = 4 − k_c ∈ {1, 2}.  With |M_c| ≥ 3 a corner can be self-sufficient (A meets all three, B, C one slot each) at the
price f ≤ 2.  **3.2 Per wall** (corners c, c′; slots c10, c′10): supply letters per slot.  ADJ into c′10 comes from a
FLAT meeter of c on that wall with δ > s − 3 (E) or from a tilted meeter of c with w(θ) > s − 3 that reaches u > s − 2
below height 1 (F; alive below 4: a 45° BL meeter centred (1.3, 0.8) reaches BR10 at ŝ).  FREE into c10: a free square
with a point in (1 + δ, 2)×(0,1) beside the flat meeter (if c is type F with A on this wall), i.e. a third wall member
that JUTS when the floor gap is < 1 (A239 §1: R ≥ 1 leaves s − 2 − R < 1... in the contact family), or in the notch
above a partner's edge.  **3.3 Around the perimeter**, with A_w the ADJ incidences on wall w and F_w the free ones:
    Σ_c o_c ≤ Σ_w (A_w + F_w),   A_w ≤ #{flat meeters on w with δ > s − 3} + #{tilted meeters on w with reach},
    Σ_w F_w ≤ 4 f,   f = 11 − Σ|M_c| ≤ 3,   and ≥ 2 free squares meet the border (Lemma TWO).
All-type-F ring: Σ o_c = 8, Σ A_w ≤ 4 (one far slot per flat meeter), so **F ≥ 4 free incidences, f ≥ 1**; with
partners never crossing corners, a wall carrying two partners has F_w = 2.  Mixed rings: Σ o_c ≥ 4 + #F-corners.

**3.4 Where the s-dependence sits, pattern by pattern.**  (a) *All ADJ, type F everywhere* (no free square meets a
cell): dead by the count above [T].  (b) *Two flat meeters on one wall, mutual ADJ* (letters AO/AO): needs
δ, δ′ > s − 3 and disjointness 1 + δ ≤ s − 1 − δ′, i.e. 2(s − 3) < δ + δ′ ≤ s − 2 — feasible iff **s < 4** [T]: the
wall closes exactly at 4 (equality structure: δ = δ′ = 1, the grid's flush row), and below 4 it is a packing, so no
wall-local rule kills it; what it costs is on the SIDE walls: both partners then have sin θ ≤ δ but depth
d_B ≤ (δ − sin θ) tan θ, their tops at ≥ 2 (E iii), and the two side walls each carry a partner from below and a
crowd from above in s < 4 — the room statement.  (c) *Alternating* (flat meeter on the floor at c, partner on the
floor at c′): c10's second supplier is FREE (the partner cannot cross, E), c′10's is A iff δ > s − 3 or FREE — one
free square can serve both if it spans (1 + δ, 2) to (s − 2, ·) inside the strip: it is a third floor member, and
with the floor gap s − 2 − δ − (partner's reach ≥ 1 along the floor... ) < 1 it juts (A239 §2.4).  (d) *Type T
corners*: k_c ∈ {2, 3}; the ADJ reach of a tilted meeter is w(θ) > s − 3 [T, vacuous]; nothing local.  **In every
pattern the composed inequality is a count plus (b)'s δ + δ′ ≤ s − 2, and the count is satisfiable with f = 3.**  The
missing rule is the room for the free squares and the partners together — a statement about 8 poses + s, which no
bounded search in "the few remaining variables" reaches: the smallest reduction (all four corners type F in mode (a),
free squares only supplying) has 8 continuous parameters plus the three free poses.  Recorded, not run.

## 4. Tests [M] (`results/construct246.md`)

The 282 corpus crowds (sides 4.002–4.391; 145 of them 12-stuck at meeting depth > 10⁻⁵, the rest doubly met only by
touches), the 34 certified (4.000022–4.015): **0 violations** of A, B, D, E, F, TWO and of the counts; corner types
TTTT 93 / mixed 188 / FFFF 1 in the corpus, TTTT 32 of 34 certified; f = 3 always; max cells 3–4 (never 5 above 4,
as B predicts: 5 needs s ≤ ŝ's reach); slot letters OO 696, FO 690, AO 297, AFO 229, O 172, FOO 83, …; ADJ
incidences 0–5, outside demand 4–8.  The 304 A244 near-4 attempts (residual < 10⁻³) and the two fresh fixed-side
attempts (ŝ: residual 2.8·10⁻², 3.95: 1.2·10⁻², 6 restarts each) violate D (20 corners) and E (9) — an overlapping
candidate makes a corner self-sufficient — and satisfy every count; their supply pattern (AO 720, FOO 464, AOO 311
of 2432 slots) leans on ADJ and on free triples, exactly the mutual-service and jut suppliers of §3.

## 5. What is proved, what remains, n-generality

* **[T]** A, B, C, D, E, F (+ Lemma TWO), CAP-REDUCTION; O-NO-SELF-SUFFICIENT closed.  **[T-computed]** SLOT-MET(η)
  for every η ≥ 10⁻⁷; **[S]** SLOT-MET as η → 0.
* **[F]** as a proof of STUCK-EXIST(11): the rules compose to counts and to (b)'s wall inequality, satisfiable below 4.
* **[C]** STUCK-EXIST(11) — with WALL-SLOT and K0-FREE it closes k0_00 without locks (`no_packing_of_stuck_exist`);
  the honest residue is the 8-pose room statement of §3.4, i.e. POCKET(11) under the sharper 12-stuck + propagation
  hypotheses.  **Not closed below 4.**
* **n-general**: A–G and the pattern counts hold for every n and s ∈ (2 + √2, 4]; only f = n − 8 = 3 uses n = 11
  (through Lemma TWO's "at most one in the centre" it gives ≥ 2 free squares on the border).
* Lean `Statements/Open/StuckExist.lean`: `stuck_exist_eleven` (axiom [C]), `wall_slot_link` (axiom, WALL-SLOT +
  K0-FREE given SLOT-MET), theorems `stuck4_unlocked_of_stuck_exist`, `no_packing_of_stuck_exist`,
  `no_twelve_stuck_of_stuck_exist`, `stuck_exist_of_unlocked`; build + audit, no sorry.  Obligations: O-SLOT-MET-LIMIT
  (η → 0), O-SQUARE-IN-TRIANGLE / O-NSS in Lean over `IsUnitSquare` (routine).
* Resume: `bash attempts/A246-construct-towards/code/run246.sh test|check|slotmet|pages` (nothing left running; the
  ladder is seconds; `logs/STOP` + checkpoints `logs/slotmet_<eta>.npz` if a finer η is ever wanted).
