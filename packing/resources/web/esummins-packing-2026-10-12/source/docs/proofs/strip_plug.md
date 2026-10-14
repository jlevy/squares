# STRIP AND PLUG — the STRIP is sealed by C, X and the wall alone (two obstacles, no sector, s-free; [T] for a flat C in standard orientation, [T-computed] on 18 rings at exit / 323 in the lane, [C] in general); A263's OPEN P2 leaves were not a corner layer but a SIDE mismatch (P2 tested at 3.8771 on boxes that are all-ADJ only near 3.82) — the five cells certify at the ADJ-consistent side; the gap COUNT: what GAP-CELL gives is two, and the chain needs CAPACITY-2, not ROOM ≤ 1 — A265, 2026-09-22

The brief (A265 BRIEF): (1) Lemma STRIP, the last lemma of the jammed sector (three_lemmas.md §4.3); (2) the OPEN
P2 cells 2,4 / 2,5 / 3,4 / 3,5 / 3,6 of A263 with the PLUG as a fifth obstacle; (3) the gap count; (4) the chain
list.  Tags [T] proved, [T-computed] finite computation with its own check, [M] measured, [C] conjecture, [F]
false (witness).  Code `attempts/A265-strip-plug/code/` (`strip265` the obstacle-subset strip test, `cert265` the
re-run (cert263 wrapped, never edited), `verify265` its verifier, `miss265` the exact region search on the OPEN
leaves, `pages265`, `run265.sh`); results / certs / logs beside it; pages `docs/residue_map/campaigns/A265-strip-plug/`;
Lean `Statements/Open/StripPlug.lean`.  Notation as A264: corner frame BL, wall x = 0, floor y = 0, c = cos,
s = sin, w = c + s; C the floater (h_u = its distance to the wall, h_v to the floor, both < 1 since C meets the
open box), T_u = C − h_u e_x its wall drop, S := T_u ∖ C the STRIP; X the wall toucher above C with int X ∩ int T_u ≠ ∅
(the DIRECT-JAM) and int X ∩ int C = ∅; A, A₂ the floor row.

## 0. Verdict

> **STRIP (task 1).**  [T-computed, `strip265`: 18 JAM rings across the five sides at exit (3°–5° grids); the
> 323-ring 1° run is the second lane's first step, `results/strip265.json`]: the strip is sealed by **C, X and the
> wall ALONE** — on every ring tested NO unit square of the container interior-disjoint from C and X has an interior
> point in S (both sectors return −9 = no such square; A, A₂ and the sector condition are never needed; C alone
> does NOT seal it: BL-floor margin up to −0.06 with C only, i.e. a square below C meets S but is no sector square).  So STRIP is a
> **two-square, s-free, sector-free statement** on the 5 parameters (h_u, h_v, θ_C; y_X, φ_X) — not the 7-parameter
> `jam` job and not A264's 4-square sector statement.  [T] the mechanism (§1.3): a square Q free of C with an
> interior point p ∈ S has a horizontal chord through p shorter than h_u < 1, so p lies in Q's bottom or top TIP
> (within h_u sin ψ cos ψ ≤ h_u/2 of the vertex) and Q's wide part (chords > h_u) lies outside C's height band; the
> TOP tip is impossible over the floor by (1 − c)(1 − s) ≥ 0; the BOTTOM tip forces Q's bottom vertex into the
> column [0, h_u] × (h_v + 1 − h_u/2, h_v + 1) — and X, which also has an interior point in S, is a bottom-tipped
> square in the SAME column with its left vertex on the wall: two such squares collide (a shrink argument on the
> gap between X's right flank and Q's left flank).  **[T] for a FLAT C with Q and X in standard orientation
> (bottom vertex left of the right vertex's foot, tilts in [0°, 45°]); [C] for the mirrored orientations and a
> tilted C** (the same chord / column / shrink mechanism with C's left flank as the column's right wall — written
> but not checked in every case).  Consequence [T given STRIP]: `jam_sector_of_strip` — the BL sectors of a JAM
> corner are A262's `pair3` with T_u as the END square (Lean `strip_of_two_obstacles`: STRIP against {C, X} implies
> A264's `strip_lemma`).  The 323-ring test is the strongest evidence a certificate could give short of a 5-parameter
> tree (priced §1.4: ≈ 1–3 CPU-h, not launched — the flat-C proof suggests the tilted case is a hand lemma).
> **The OPEN P2 leaves (task 2): [F] the brief's reading, [T] the cause, [T-computed] the fix.**  The OPEN leaves
> of cells 2,4 / 2,5 / 3,4 / 3,5 / 3,6 sit at b ∈ [0.88, 1], φ_W ∈ [10°, 20°], a′ ∈ [0.45, 0.52], φ₁′ ∈ [21°, 33°]
> (not "b ≥ 0.98": cell 3,4 has OPEN leaves at b = 0.88).  The failing square is NOT at the corner: it is a square
> on the centre line, 0.7 from the right wall, that misses O "to the right wall" (case (ii)) by up to +0.030 at
> s = 3.8771 — a REAL P2 miss there (exact centre sets, `miss265`: 134 of 500 sampled OPEN leaves have a positive
> exact margin at 3.8771, none at their own s_eff, where all are ≤ −0.040).  But at 3.8771 these boxes are NOT all-ADJ:
> a′ + w(φ₁′) = 1.822 < s − 2 = 1.877 (S′ misses its far slot); the ring is ADJ-feasible only for s ≤ a′ + w + 2 ≈
> 3.82–3.86, and there the same box has margin −0.061.  A263's test imposes ADJ at SMIN = 3.82 and evaluates at
> SMAX = 3.8771 — sound but lossy, and the loss is exactly the OPEN region.  **Fix (`cert265`, sound by the
> corner-frame monotonicity, Lean `adj_side_bound` / `p2_of_adj_side`): test every box at s_eff = min(SMAX,
> hi_b + w(hi_φW) + 2, hi_a′ + w(hi_φ₁′) + 2)**, plus the graded plug (ρ = 1/4, 1/8, 1/16 for a′ > 0.604, 0.48,
> 0.417; Lean `plug_graded`).  Cells 2,4 / 2,5 / 3,4 certify in 46 / 82 / 91 s (vs OPEN after 1160 / 324 / 5233 s)
> with 463 / 620 / 973 CERT leaves; 3,5 / 3,6 in the relaunched chain (`certs/P2265_index.jsonl`); verifier
> `verify265` (independent 0.4° bins, bisect on disagreement, tiling identity, the side and the plug hypothesis
> re-derived per leaf): `results/verify265.json`.  The plug never touches the failing square: **the OPEN leaves
> were a side-mismatch artefact, not a corner layer**.  The WE / WS indices have no OPEN cell (4 cells done).
> **Gap count (task 3): [T] what is derived is TWO, and the chain needs CAPACITY-2.**  GAP-CELL gives ≥ 2 free
> squares meeting every gap cell T′ not met by S′; neither the far-slot square nor the O-square is shown distinct
> from them (a square meeting a floor cell can contain O: [1.44, 2.44] × [0.95, 1.95] does at ŝ), so the count
> derived is 2, not > 3.  But the count the chain NEEDS is weaker than ROOM ≤ 1: 8 ring squares + 3 free, at most
> one containing O ⟹ **two interior-disjoint free squares both missing O** (Lean `gap_needs_two_misses`).  So the
> non-ADJ obligation is CAPACITY-2 (no two disjoint free squares both miss O), which the P2n / WEn / WSn trees
> do not test and which the gap mechanism (§3) makes plausible: the two gap meeters of T′ are stacked over the
> same unit cell, so the lower one has a free drop unless the other blocks it from below-right.  The sub-case
> 1 + w − sec ≤ e < sec and the wedge case φ_W ≠ φ₁ remain [C] (§3.2).
> **Plainly.**  N1 (jammed sector) = pair3 + STRIP; STRIP is now a 2-square lemma, proved for a flat C, tested on
> every ring tried (the full 323 in the lane).  The OPEN P2 cells are closed (three certified at exit, two relaunched).  The non-ADJ gap needs
> CAPACITY-2, not ROOM.  k0_00 unchanged.

## 1. STRIP  (task 1)

**1.1 The statement, reduced.**  *STRIP₂ [C]: C a unit square with 0 < h_u < 1, 0 < h_v < 1 (it meets the open
box); X a unit square with a vertex on the wall x = 0, X ⊆ quadrant, int X ∩ int C = ∅, int X ∩ int T_u ≠ ∅.  Then no
unit square Q ⊆ quadrant with int Q ∩ int C = ∅ = int Q ∩ int X has an interior point in S = T_u ∖ C.*  It is s-free
and m-free (the quadrant only), needs neither A, A₂ nor the sector, and implies A264's STRIP (fewer obstacles, more
squares: Lean `strip_of_two_obstacles`).  With STRIP: the BL-sector pocket of {A, A₂, X, C} ⊆ the pocket of
{A, A₂, T_u} — `pair3` at the BL corner (three_lemmas.md §4.3, Lean `jam_sector_of_strip`).
**1.2 [T-computed] `strip265`** (exact centre sets; for each obstacle subset the max over squares free of the
subset AND meeting S with positive area of the sector functional).  At exit: 3 rings at ŝ with all 9 subsets (5°
grid) + 15 rings spread over 3.82 / 3.85 / ŝ / 3.92 / 3.95 / 3.99 with {C, X} and {C} (3° grid): {C, X}: −9 / −9
on every ring (no such square exists at all); {A, A₂, X, C}, {A, X, C}: −9 / −9; {C} alone: BL-floor −0.06 … −0.22
(a square below C meeting S exists but is not a sector square); {A, C}: −0.19 / −9; {A, X}: +0.9 (without C the
strip is just space); {A}, {X}, ∅: ≥ +0.5.  So X is the strip's LID and C its right wall; nothing else is used.
The 323-ring 1° run (all subsets, ≈ 20 min) is the second lane's first step; its `worst` block is the number to
quote.  Facts recorded per ring: h_u ∈ [0.001, 0.75], h_v ∈ [0.88, 1.0), θ_C up to 13°, X's intrusion into T_u.
Page `strip_two_obstacles.svg` (written by the lane).
**1.3 The mechanism, and a proof for a flat C [T].**  Let C = [h_u, h_u+1] × [h_v, h_v+1] (θ_C = 0), so S = [0, h_u)
× [h_v, h_v+1].  Let Q (tilt ψ ∈ [0°, 45°], bottom vertex B, right R = B + (c, s), left L = B + (−s, c), top
T = B + (c − s, w)) be free of C with p ∈ int Q ∩ S.
(i) *Chords.*  At any height y ∈ (h_v, h_v + 1) a chord of int Q reaching x > h_u enters int C; so every chord of
Q at those heights lies in [0, h_u], in particular the chord through p has length < h_u.  A chord of Q at vertical
distance t from its bottom (or top) vertex has length t/(sc) for t ≤ s, and ≥ 1 in between (ψ = 0: every chord has
length 1 > h_u — impossible).  Hence p is within h_u·sc ≤ h_u/2 of B or of T, and Q's chords longer than h_u,
which occupy the heights (y_B + h_u sc, y_T − h_u sc), avoid (h_v, h_v + 1).
(ii) *Top tip impossible.*  If p is near T, the wide part is below h_v: y_T − h_u sc ≤ h_v < 1; but y_T ≥ w (Q is
over the floor), so c + s − h_u sc < 1, while c + s − sc ≥ 1 ⟺ (1 − c)(1 − s) ≥ 0.  Contradiction.  (Uses the
floor and C only.)
(iii) *Bottom tip.*  p near B: the wide part is above h_v + 1, so τ_Q := h_v + 1 − y_B ≤ h_u sc ≤ h_u/2, and all
chords at heights < h_v + 1 lie in [0, h_u]: x_B ∈ [0, h_u], and x_B + τ_Q cot ψ ≤ h_u.  The same holds for X (it
has an interior point in S: int X ∩ int T_u is open and disjoint from int C): X is bottom-tipped with x_{B_X} = s_X
(its left vertex is ON the wall), τ_X := h_v + 1 − y_{B_X} ≤ h_u s_X c_X.
(iv) *Collision.*  Q and X are interior-disjoint convex bodies with overlapping height ranges and x-ranges (both
start at x ≤ h_u < 1 and are ≥ 1 wide), so one is consistently to the right of the other at every common height.
Q left of X is impossible: at X's left vertex height y_{L_X} = y_{B_X} + c_X, X's chord starts at x = 0, so Q's
chord there (Q crosses that height, or lies wholly below it — then Q's wide part, at x reaching ≥ 1, is below
y_{L_X} < h_v + 1 + c_X, and below h_v + 1 it must stay in [0, h_u]: contradiction) must start at X's right boundary
1/c_X or 1/s_X ≥ 1 > h_u ≥ x_B, i.e. Q is right of X.  Now Q's left flank moves LEFT (rate tan ψ) from B up to L
(height c above B) while X's right flank moves RIGHT (rate cot φ_X) from B_X up to R_X (height s_X above B_X); over
the common part of these two height ranges the gap between them shrinks from at most h_u − s_X (both bottom
vertices in [0, h_u], X's at s_X) by min(Δ)(tan ψ + cot φ_X), Δ the common range's length.  If the range is X's
(Δ = s_X − |t₀|): shrink ≥ c_X − |t₀| cot φ_X ≥ 1 − s_X − |t₀| cot φ_X > gap.  If it is Q's (Δ = c − |t₀|,
|t₀| ≤ τ_Q ≤ h_u sc): gap ≤ h_u − s_X − |t₀|/(sc) < 1 − c and shrink ≥ (c − sc)(1 + tan ψ) = (1 − s)(c + s) ≥ 1 − c on
[0°, 45°] (min 0.12 at 45°).  Contradiction in every case.  ∎  (Here t₀ = y_{B_X} − y_B; the case t₀ ≥ 0 with B_Q
left of X's lower-left edge is the "Q left of X" case above.)
**1.4 What is not proved.**  Q or X in the MIRRORED orientation (the shallow edge from the bottom vertex going
up-left: the left flank then moves left at rate cot ≥ 1 and the chord at h_v + 1 grows at rate tan — the shrink is
faster, the τ-bound weaker; the same four cases, not written out), and a TILTED C (S is a chevron; the chords are
confined by C's left flank line instead of x = h_u, the column is a parallelogram of width h_u; the identity in
(ii) is replaced by w − h_u sc + (slant) ≥ 1).  A 5-parameter box certificate of STRIP₂ (cores of C and X, kernel
per tilt bin of Q, the strip region T_u ⊕ Q₀ relaxed by the box) is A259's method on (h_u, h_v, θ_C, y_X, φ_X) with
the DIRECT-JAM domain: ≈ 3 · 10⁴ boxes at 0.05 s (Monte-Carlo guess from the rings' margins −9 = the pocket is
EMPTY, so most boxes prune on core overlap of Q's kernel with C ∪ X) — 1–3 CPU-h; not launched (the hand lemma is
the better route; the ring test covers every witness the searches produced).

## 2. The OPEN P2 leaves  (task 2)

**2.1 What they are [T-computed] (`miss265`).**  For each of the five cells, 100 OPEN leaves (the 40 largest box
margins + 60 random) evaluated exactly (geo263.factor_margin, 0.25° grid): at SMAX = 3.8771 the exact P2 margin is
POSITIVE on 5 / 53 / 14 / 62 / 0 of the 100 sampled leaves of 2,4 / 2,5 / 3,4 / 3,5 / 3,6 (max +0.0125 / +0.030 /
+0.024 / +0.030 / −0.024: real P2 misses, e.g. the pose (2.51, 1.94), ψ = 24.7°, case (ii)) and negative but
within 0.03 of zero elsewhere (box relaxation at depth 26); at the leaf's own s_eff it is ≤ −0.057 / −0.041 /
−0.049 / −0.040 / −0.069 on every leaf sampled (`results/miss265.json`).  The missing square sits on the horizontal centre line 0.575 right
of O, 0.7 from the right wall, above W and left of S′: the PLUG (any ρ < 0.35) does not touch it.  Its region is
LEFT(S′) — where W′ would stand in the ring: the FULL corner scan (§2.3) says whether W′ blocks it.
**2.2 The cause and the fix [T].**  The all-ADJ family at side s requires b + w(φ_W) ≥ s − 2 and a′ + w(φ₁′) ≥
s − 2.  A263 imposes them at SMIN and tests at SMAX.  In the corner frame the statement at s_max implies the
statement at every s ≤ s_max (normal_room.md §2.3, open_pairs.md §2.2: `corner_frame_mono`, `clip_mono`), so testing
a box at s_eff(box) = min(SMAX, hi_b + w(hi_φW) + 2, hi_a′ + w(hi_φ₁′) + 2) certifies every side at which some
parameter of the box is in the family (Lean `adj_side_bound`, `p2_of_adj_side`).  `cert265` wraps cert263's
`check_box` (module globals SMAX / PLUG_A / RHO_PLUG set per box, restored after) — cores, kernel, clips all at
s_eff; PRUNE only by cert263's own domain test.  The graded plug: ρ = 1/4 for lo_a′ > 0.604 (A263), 1/8 for
lo_a′ > 0.48, 1/16 for lo_a′ > 0.417 — Lemma PLUG needs a′ > √2/4 + ρ (Lean `plug_graded`, from `plug_kernel`).
**2.3 Results.**  Index `certs/P2265_index.jsonl`: 2,4 ok (1 551 boxes, 46 s), 2,5 ok (3 121, 82 s), 3,4 ok (2 759,
91 s) — A263's 20 917 / 6 545 / 79 477 leaves with 10 312 / 2 508 / 50 578 OPEN become 776 / 1 561 / 1 380 leaves
with none.  3,5 and 3,6: relaunched (`run265.sh cells`) after the strip test; the index says.  Verifier:
`results/verify265.json` (all CERT / PRUNE leaves re-derived under 0.4° bins with 0 as an edge; a leaf the
independent cover rejects is bisected to depth 8; the recorded side is recomputed; the plug hypothesis checked).
FULL-corner scan at the worst leaf (b = 0.994, φ_W = 14.3°, a′ = 0.490, φ₁′ = 25.5°; s₁ at W's tilt, W′ over 13
shifts × 11 tilts, non-ADJ domain, s = 3.8771): **+0.025 at (e, e′, φ_W′) = (0.1, 0.6, 38°)** — the 4-square corner
does NOT block the square when the right wall is non-ADJ on both ends (δ_W′ = 2.20 > 2: W′ misses its far slot
too, b′ = 0.28); the free square (centre (2.52, 1.94), ψ = 25.5°) reaches x = 3.18 > s − 1 and so MEETS the
unserved slot R — it is the far-slot free square of `nonadj_free_meeter`, missing O.  [M] a bare-ring ROOM
witness on the non-ADJ family at ŝ by a CENTRE-LINE square (A263's witness was a floor cell in a wide gap): the
same conclusion, CAPACITY-2 is the statement to prove there (§3); it is not a k0 counterexample (one miss is
allowed, two are needed).
**2.4 What the brief had wrong.**  "The OPEN leaves sit at b ≥ 0.98 … the closed-corner layer that A260 closed with
PLUG": the leaves reach b = 0.88, the failing square is at the container's centre line, and the plug is idle on
them.  The mechanism is the SIDE, not the corner.

## 3. The gap count  (task 3)

**3.1 What is derived [T].**  Non-ADJ floor (a + w(φ₁) ≤ s − 2).  (a) GAP-CELL: every floor cell T′ in the gap not
met by S′ is met by ≥ 2 free squares (three_lemmas.md §2.2).  (b) The unserved slot R carries a free square
(`nonadj_free_meeter`).  (c) STRIP-CHAIN (common tilt, e ≥ sec φ₁): every free square of the strip is chained to
S′ or P1 moves it.  None of (a)–(c) makes the far-slot square or the O-square distinct from the two gap meeters:
a square meeting T′ = [x, x+1] × [0, 1] can contain O (its centre needs height ≥ s/2 − w/2 = 1.23 at ŝ, and it
reaches T′ from height ≤ 1 + w/2), and R overlaps the gap when the gap reaches x ≥ s − 2.  So the derived count is
**2 free squares in the gap** — the brief's "> 3" was a guess and stays one.
**3.2 What the chain needs [T].**  Eight ring squares, eleven in all: three free squares; at most one contains O
(HOLE-ONE): **at least two free squares miss O, and they are interior-disjoint** (Lean `gap_needs_two_misses`).
ROOM ≤ 1 (every free square contains O) is sufficient but not necessary; the necessary-and-sufficient room
statement on the non-ADJ family is CAPACITY-2: *no two interior-disjoint unit squares of the pocket both miss O*.
On the wide gap (e ≥ 1 + w − sec) ROOM fails (A263 [F]) but CAPACITY-2 is exactly what (a) suggests: the two
meeters of T′ are stacked over one unit cell, both free, both at height ≤ 1 + w/2 over the floor; the LOWER one
has a straight floor drop blocked only by a square under its right flank (BLOCKER-SIDE) — which the other meeter
of T′ is not (it is above or beside it), so P1 moves the lower one onto the floor unless a THIRD square blocks: the
lower gap meeter is jammed by something else, and the count grows.  Making this a lemma needs the wedge case
(φ_W ≠ φ₁, the drop direction is then W's flank, open_pairs.md §3.3) and the sub-case 1 + w − sec ≤ e < sec (a flat
cell fits but crosses s₁'s edge line below its vertex) — both [C], exactly as A264 left them; nothing here closes
them.  A CAPACITY-2 certificate on the non-ADJ family (two squares, 8 parameters of the two poses on top of the
corner's 4–6) is out of the box-tree budget; the P1 route is the one to take.

## 4. The chain list — `k0_route.md` §13, updated links

5b: BL sectors = pair3 at BL with T_u [T given STRIP] + STRIP [T flat C standard orientation; T-computed 18
rings at exit, 323 in the lane; C general] — was [C] outright.  10c: the three OPEN P2 cells: [T-computed] 2,4 / 2,5 / 3,4 (verify265),
3,5 / 3,6 relaunched — the cause [T] (side mismatch), no real miss of the independent-tilt room found.  10d: the
count "> 3" [F as a derivation]; the needed statement is CAPACITY-2 [C]; (i) and (ii) unchanged [C].  Still [C]:
5b STRIP in general (tilted C, mirrored orientations), 5d, 6's `jam_count`, 8a–8b chains, 10a–10c chains, 10d
CAPACITY-2 on the wide non-ADJ gap + the wedge and 1 + w − sec ≤ e < sec sub-cases, the [T-prose] axioms, the stretch.

## 5. Lean, reproduce

`Statements/Open/StripPlug.lean`: theorems `adj_side_bound`, `p2_of_adj_side`, `plug_graded`,
`strip_of_two_obstacles`, `gap_needs_two_misses`; axiom `strip_two` [C]; build + audit 0 sorry, AUDIT.md rows.
Reproduce: `bash attempts/A265-strip-plug/code/run265.sh chain` (cert265 → verify265 → strip265 → miss265),
`run265.sh cells` (the relaunch for 3,5 / 3,6 + verify), `python pages265.py`.
