# THREE LEMMAS — the near-flat cube is a THEOREM (both mixed corners force offsets to 1, margin 0.10 in the offset at ŝ, for every side < 3.981); the JAMMED SECTOR needs A and C only, X is a domain condition, and C is dominated by its own wall drop (pair3 + a STRIP lemma); the NON-SERVING GAP: what P1⁺ / BLOCKER-SIDE / STRIP-LANDING give and what is still open — A264, 2026-09-22

The brief (A264 BRIEF): the three lemmas left by A262 (N1 the BL sector of a JAM ring) and A263 (O3 the non-ADJ
gap, O4 the all-near-flat cube).  Tags [T] proved, [T-computed] finite computation with its own check, [M] measured,
[C] conjecture, [F] false (witness).  Code `attempts/A264-three-lemmas/code/` (`corner264` exact corner forms + SAT,
`cube264` the cube constants + LP scan, `sub264` obstacle subsets on the JAM rings, `cmp264` the drop-cell comparison
and the strip test, `pages264`); results beside it; pages `docs/residue_map/campaigns/A264-three-lemmas/`; Lean
`Statements/Open/ThreeLemmas.lean`.  Notation: corner frame with the corner at the origin, floor y = 0 (x = distance
from the corner), wall x = 0; c = cos, g = sin, w = c + g; A = the wall's START square (offset a, tilt α), B = the
floor's END square (offset b, tilt β), offsets as in A258 (a_w + b_w = s − sec φ_w − w(φ_w) on every wall, both senses).

## 0. Verdict

> **Lemma 3 — NEAR-FLAT CUBE: [T], hand proof, explicit constants, on [3, 3.981) ⊃ [3.82, ŝ].**  At a MIXED corner
> of type (+,−) BOTH offsets exceed 1 − λ, λ = ε₀/2 + ε₀²/2 (§3.2); at a (−,+) corner ONE offset exceeds 1 − μ,
> μ = ε₀²/2 + tan ε₀ (1 + sin ε₀); at a one-sense (+,+) corner the END offset exceeds 1 − ε₀²/2 − a tan ε₀.  With the
> wall identity a_w + b_w ≤ s − 2 the three mixed patterns close in one to four steps (§3.3): + + + − and + − + −
> are infeasible for s < 4 − λ − ν = 3.9813, + + − − for s < 3.9814; at ŝ the contradiction margin is 0.104–0.106 in
> the offset (`cube264`: constants at 60 digits, 0 violations of the corner lemmas on 20 000 random near-flat
> corners against exact SAT, LP max-strictness = 0 at 200 tilt vectors × 16 axis choices).  ε₀ = 0.703° = π/256 is
> A261's TMIN; the lemma holds for any ε₀ with λ + ν(ε₀) < 4 − s.  `slab_cube` is no longer an axiom: Lean
> `cube_pppm`, `cube_pmpm`, `cube_ppmm` from the three corner lemmas (axioms [T-prose]) + `linarith`.  **The one-sense
> near-flat cube** needs nothing: A259 / A260 / A263's room certificates start at tilt 0 (D1 is 0 < φ, the trees
> cover [0°, 45°]), and exactly flat walls are A261's F0 / F02 jobs [T-computed].
> **Lemma 1 — JAMMED SECTOR: [M] + [C], reduced.**  On all 323 JAM rings of A262 (ring262 + search262, five sides):
> the BL-floor sector is decided by {A, C} alone and the BL-left sector by {A, A₂, C} (identical margins with and
> without X and A₂, `sub264`); **X is a DOMAIN condition (it jams C), never an obstacle of a low free square**.
> Candidate (i) tested as a monotone comparison: replacing C by its WALL DROP cell T_u = C − h_u e_x (a wall toucher
> at C's tilt, offset h_v < 1) keeps both sectors negative on every ring (worst −0.0123 / −0.0052 at 3.99, −0.061 /
> −0.064 on the window), and **no free square of the true pocket meets T_u ∖ C** (the strip between the wall and C's
> left flank; 323/323, `cmp264`).  So the BL sectors are A262's `pair3` (a row of two + ONE wall square, 4
> parameters, launched) at the BL corner with T_u as the wall square — exactly IF the STRIP lemma holds [C]: *a low
> free square avoiding A, C, X never enters the strip between the wall and C's left flank*.  The 7-parameter `jam`
> job is then unnecessary.  The worst rings are the NEAR-FLAT LIFTED-END jams (C within 0.001–0.13 of the wall, all
> tilts < 3°, the one-sense ring with an END square lifted off its wall): their sector margin is the flush value
> −(4 − s)/2, so no analytic sector lemma can beat A259's PAIR there — the comparison IS the lemma.  **N6 corrected
> [F → M]**: adjacent j = 2 JAM rings EXIST on the window (A262's chain2 `adv262`, t = 0.0071 at ŝ, 0.0010 at 3.82;
> capacity 1, pierce ≤ −0.081 at ŝ); j = 3 and j = 4 rings exist at 3.95 / 3.99 only (room 0), none on the window.
> The count reduction (no_jam.md §2.3) is per corner, so nothing changes: each JAM corner is its own sector job.
> N3, N5: `float262` / the indirect-jam search have not run (chain3 waits for search262, 399 rows, no witness).
> **Lemma 2 — NON-SERVING GAP: [T] pieces, [C] closure.**  (a) [T] the gap cells: a floor cell T in the gap between
> s₁ and W is met by no ring toucher except possibly the next wall's START square S′ (a sliver), so by P1⁺ it is met by
> S′ or by ≥ 2 free squares (§2.2).  (b) [T] BLOCKER-SIDE: s₁ never blocks the floor drop of a gap square (it is
> below-LEFT); W never blocks its slide along the notch.  (c) [T] STRIP-CHAIN, common tilt, e ≥ sec φ₁: the strip
> between s₁'s upper-right edge line and W's left flank line has width e cos φ₁ ≥ 1 and is free of s₁, W; a free
> square inside it slides along the flank direction to a floor cell met by nothing but itself unless a chain of
> free squares below-right of it ends at S′ — so every free square of the strip is chained to S′, or P1 is violated.
> On A263's drawn witness (2°, e = 1.06 > sec 2° = 1.0006) the flat square is in the strip with a free drop of 0.02:
> P1 kills it [T].  (d) [C] what is missing: the sub-case 1 + w − sec φ₁ ≤ e < sec φ₁ (a flat cell fits the gap but
> crosses s₁'s edge line below its vertex), the wedge case φ_W ≠ φ₁, and the count "chained to S′ ⟹ ≥ 4 free
> squares or a free square containing O" — the brief's "> 3 free squares" is not derived.  Room on the non-ADJ family
> is otherwise A263's P2n / WEn / WSn (queued), whose OPEN leaves are exactly the strip region.
> **Plainly.**  O4 closed [T].  N1 reduced to pair3 + STRIP [C].  O3 open with its mechanism [T].  k0_00 unchanged.

## 1. Corner geometry and the admissible forms  [T]  (`corner264`)

**1.1 Vertices** (from A258's Q1 = (a+g, 0), (a+w, g), (a+c, w), (a, c) in the wall frame and its mirror for sense −;
the floor is walked towards the corner, x = s − t):
A(+): (0, a+g), (g, a+w), (w, a+c), (c, a);  A(−): (0, a+c), (g, a), (w, a+g), (c, a+w);
B(+): (b+c, 0), (b, g), (b+g, w), (b+w, c);  B(−): (b+g, 0), (b+w, g), (b+c, w), (b, c).
Both senses: A's y-extent is [a, a + w], B's x-extent [b, b + w]; the box (0,1)² is met iff a < 1, resp. b < 1.
**1.2 Forms.**  Interior-disjointness is SAT over the four edge normals; the two normals in the open second quadrant
(A261 §3.1, PUSH) give, by direct computation of the extreme vertex on each side (the extreme vertex switches at
sin(α − β) = 0, hence the max terms):
(+,+): E_A = g_α a + c_α b − c_α² − g_α g_β − max(0, sin(α−β));  E_B = g_β a + c_β b − g_β² − c_β c_α − max(0, sin(α−β));
(+,−): E_A = g_α a + c_α b − c_α² − g_α c_β  (⟺ b ≥ c_α + tan α (c_β − a));  E_B = c_β a + g_β b − c_β² − g_β c_α  (⟺ a ≥ c_β + tan β (c_α − b));
(−,+): E_A = c_α a + g_α b − c_α w_β − g_α² + g_α g_β  (⟺ a ≥ w_β − tan α (b + g_β − g_α));  E_B = g_β a + c_β b − c_β w_α − g_β² + g_β g_α  (⟺ b ≥ w_α − tan β (a + g_α − g_β));
(−,−): the (+,+) forms with (a, α) ↔ (b, β).  Corner condition: max(E_A, E_B) ≥ 0.
[T-computed] the forms equal A261's `point_form` (cert261.py) to 6·10⁻¹⁶ and agree with exact SAT on 40 000 random
corners (a, b ∈ [0, 1), tilts up to 0.8 rad, all four sense pairs; 0 disagreements): **the two admissible axes decide
interior-disjointness exactly whenever both squares meet the open box** — A258's "[M] the other axis never decides" and
A261's admissible-axes lemma, re-derived and re-checked.  The flat limits are right: (+,−) at α = 0 reads b ≥ 1 or
a ≥ c_β + tan β (1 − b).

## 2. Lemma 2 — the non-serving gap  (O3)

**2.1 Setting** (open_pairs.md §3).  Floor wall with START toucher s₁ (a, φ₁) and END toucher W (b, φ_W); T = s₁ +
sec φ₁ e_x its normal cell, W = T + (e, 0) at common tilt (e ≥ 0 the SHIFT); W meets int T iff e < sec φ₁.  Non-ADJ:
a + w(φ₁) ≤ s − 2, and then [T, Lean `nonadj_free_meeter`] a FREE square F meets the far slot R = [s−2, s−1] × [0, 1].
A flat floor cell fits between s₁ and W iff e ≥ 1 + w(φ₁) − sec φ₁ (the cell [a+w, a+w+1] × [0,1] must clear s₁'s
vertex (a+w, g) and W's vertex (a + sec φ₁ + e, c)); a cell at s₁'s tilt (T itself) iff e ≥ sec φ₁.
**2.2 GAP-CELL [T].**  Let T′ be any unit cell touching the floor, inside the container, interior-disjoint from s₁ and
W.  Its ring meeters are ⊆ {S′} (the previous wall's END square lies at x ≤ w(φ) < a + w when a ≥ 0 — it cannot
reach past s₁; the opposite walls are > s − 2 > 1.8 away; A261 SAME-WALL: no second toucher of the floor exists).  By
P1⁺ (box_meeters.md §1.1) with Π = {T′}: **M(T′) ∋ S′, or |M(T′)| ≥ 2 and every square of M(T′) is free.**  This is
the brief's NO-GAP count; it says nothing about depth or O.
**2.3 BLOCKER-SIDE for the gap [T].**  A free square F in the gap (a point of F between s₁'s right flank and W's left
flank, above the floor) whose straight floor drop T_v(F) = F − h_v e_y is blocked: the blocker lies under F's RIGHT
flank, separated from F by a line of positive slope (box_meeters.md §1.2, s-free).  s₁ is below-LEFT of F (every
point of s₁ has x ≤ a + w and its supporting lines towards the gap have negative slope): **s₁ never blocks the drop**.
W can (its lower-left edge leans under the gap), as can a free square below-right.
**2.4 STRIP-CHAIN [T] (common tilt, e ≥ sec φ₁).**  The lines L₁ = s₁'s upper-right edge line and L_W = W's left flank
line are parallel (direction (−g, c)); the strip between them has width e c ≥ 1 in direction (c, g) (A260's slot),
and it is free of s₁ and W (each line supports its square).  Let F be free with F ⊆ strip.  The translates
F + λ (g, −c), λ ≥ 0, stay in the strip; the sweep ends on the floor at a cell touching the floor, met by nothing
but F unless a square G meets the swept region; G has a point in the strip, so G is free (2.2) and lies below-right
of F along (g, −c).  "Below-right along a fixed direction" is acyclic on disjoint convex sets, so the chain of
blockers ends at a square whose own sweep is unblocked — a floor cell met by one free square: P1 (TOUCH-CELL) raises
Φ₁ — or at a square not in the strip, i.e. at S′ (the only ring square that can poke into the strip near its
lower-right end, x ≥ s − w(φ′)).  **In the maximiser every free square of the strip is chained to S′.**
[T-computed on A263's witness] φ = 2°, e = 1.06 ≥ sec 2° = 1.0006, the flat Q of `nonadj_gap.svg` lies in the
strip (its width in direction (c, g) is w(2°) = 1.0343 < e c = 1.0594) with a free drop of 0.02: P1 kills it.
**2.5 What is open [C].**  (i) 1 + w − sec φ₁ ≤ e < sec φ₁: the flat gap cell crosses L₁ below s₁'s vertex; the sweep
must be replaced by a slide along W's flank with s₁'s lower-right edge as the second wall (a wedge, not a strip).
(ii) φ_W ≠ φ₁ (WEDGE-NOTCH geometry).  (iii) The count: a chain to S′ means the free squares of the gap are stacked
towards the BR corner under S′, and S′ itself is a box meeter; whether that forces a fourth free square, or forces
the chain's squares to contain O, is not derived — the brief's "> 3 free squares" is a conjecture.  The non-ADJ
certificates P2n / WEn / WSn (A263, queued) will return OPEN exactly on the strip region; 2.2–2.4 are what must be
argued there.

## 3. Lemma 3 — the near-flat cube  (O4)  [T]

**3.1 Setting.**  A ring of four rows of two with senses σ_w, tilts φ_w ∈ [0, ε₀], offsets a_w, b_w ∈ [0, 1) (both boxes
of every wall met, A258 (D2)), wall identity a_w + b_w = s − sec φ_w − w(φ_w) ≤ s − 2 − sin φ_w ≤ s − 2 (sec + cos ≥ 2).
Corner k has A = wall k's START (a_k, φ_k) and B = wall k−1's END (b_{k−1}, φ_{k−1}), condition max(E_A, E_B) ≥ 0 of §1.2
with (σ_A, σ_B) = (σ_k, σ_{k−1}).  Elementary bounds used: 1 − cos x ≤ x²/2, sin x ≤ x ≤ tan x, tan x ≤ x(1 + x²) on
[0, ε₀]; tan ε₀ = 0.0122724.
**3.2 The three corner lemmas.**
*MC(+,−).*  a, b ∈ [0, 1) and max(E_A, E_B) ≥ 0 ⟹ a > 1 − λ and b > 1 − λ, λ := ε₀/2 + ε₀²/2 = 0.0062112.
Proof.  If E_A ≥ 0: b ≥ c_α + tan α (c_β − a).  Were a ≤ 1 − λ, then c_β − a ≥ (1 − ε₀²/2) − (1 − λ) = ε₀/2, so
b ≥ c_α + α ε₀/2 ≥ 1 − α²/2 + α ε₀/2 ≥ 1 (α ≤ ε₀): impossible.  Hence a > 1 − λ, and b ≥ c_α − tan α (1 − c_β) ≥ 1 −
ε₀²/2 − tan ε₀ · ε₀²/2 > 1 − λ.  E_B ≥ 0 is the same with a ↔ b.  ∎
*MC(−,+).*  ⟹ a > 1 − μ or b > 1 − μ, μ := ε₀²/2 + tan ε₀ (1 + sin ε₀) = 0.0124984.  Proof.  E_A ≥ 0 and b < 1 give
a ≥ w_β − tan α (1 + g_β) ≥ (1 − ε₀²/2) − tan ε₀ (1 + sin ε₀); E_B symmetric.  ∎
*PC(+,+).*  ⟹ b > 1 − ε₀²/2 − a tan ε₀ =: 1 − ν(a).  Proof.  E_A ≥ 0: c_α b ≥ c_α² + (nonneg.) − g_α a, so b ≥ c_α −
a tan α; E_B ≥ 0: c_β b ≥ c_β c_α + (nonneg.) − g_β a, so b ≥ c_α − a tan β.  ∎  (The pinwheel corner pins the END
offset of the PREVIOUS wall, as the domino minimiser b_w = 1, a_w = s − 3 says.)
[T-computed] `cube264`: 20 000 random corners, tilts in [0, ε₀], SAT-disjoint ⟹ the bound, 0 violations, least
slack 0.0029 / 0.0013 / 0.0003.
**3.3 The chains** (S := s − 3; every "wall" step is a_w ≤ S + (1 − b_w) or b_w ≤ S + (1 − a_w)).
*+ + + − (walls 0, 1, 2 sense +, wall 3 sense −; corners 0 = (+,−), 3 = (−,+), 1, 2 = (+,+)).*  Corner 0: a₀, b₃ >
1 − λ.  Wall 3: a₃ < S + λ ≤ 0.8834 < 1 − μ, so corner 3 gives b₂ > 1 − μ.  Wall 2: a₂ < S + μ.  Corner 2: b₁ > 1 −
ν(S + μ).  Wall 1: a₁ < S + ν(S + μ).  Corner 1: b₀ > 1 − ν(S + ν(S + μ)) =: 1 − ν₁ (ν₁ = 0.010976 at ŝ).  Wall 0:
a₀ < S + ν₁ = 0.8881.  But a₀ > 1 − λ = 0.9938.  ∎  Infeasible for s < 4 − λ − ν₁ = 3.98128; margin 0.1057 at ŝ.
*+ − + − (corners 0, 2 = (+,−), 1, 3 = (−,+)).*  Corners 0, 2: a₀, b₃, a₂, b₁ > 1 − λ.  Wall 1: a₁ < S + λ < 1 − μ, so
corner 1 (A = wall 1, B = wall 0) gives b₀ > 1 − μ; wall 0: a₀ < S + μ = 0.8896 < 1 − λ.  ∎  s < 4 − λ − μ = 3.98129;
margin 0.1042.
*+ + − − (corner 0 = (+,−), corner 1 = (+,+)).*  a₀ > 1 − λ, so b₀ < S + λ; corner 1 needs b₀ > 1 − ν(1) = 0.98765.  ∎
s < 3.98144; margin 0.1043 (A263 measured ≥ 0.061 in the LP's τ*: consistent).
**3.4 What this settles.**  The all-near-flat cube [0, ε₀]⁴ of every mixed pattern is excluded on [3, 3.981) with no
certificate; the exactly flat walls are included (α = 0 is allowed in every bound).  Together with A261's M1–M3
certificates (tilts ≥ ε₀ on every wall) and A263's 492 slab jobs (at least one wall ≥ ε₀ — the boxes adjacent to the
cube may now use the cube's margin instead of h ∝ ε: their heavy tail (SM1_013 ≈ 3·10⁷ leaves) was the cube's
neighbourhood) the mixed pinwheels of rows of two are excluded on the window.  The one-sense near-flat family is
not excluded — it exists (A261 [F]) — and its room is A259 / A260 / A263 (tilt cells from 0°).  m-general: the
corner lemmas are s-free and m-free (two squares); the chain uses only a_w + b_w ≤ s − 2 and 3 < s < 4 − λ − ν, so for
m ≥ 5 the same chain reads (m − 3) sec φ + w in the identity and gives s < m − λ − ν for rows of m − 2.

## 4. Lemma 1 — the jammed sector  (N1, N3, N5, N6)

**4.1 [M] obstacle subsets** (`sub264`, 323 JAM rings: A262's 34 + search262's 289 with t > 0, sides 3.82 / 3.85 /
ŝ / 3.92 / 3.99; exact centre sets, 1° grid).  Worst sector margins on the window (204 rings) / on all 323:
{A, A₂, X, C}: BL-floor −0.0631 / −0.0123, BL-left −0.0640 / −0.0151;  {A, A₂, C}: −0.0631 / −0.0123, −0.0640 / −0.0092;
{A, C}: −0.0610 / −0.0123, +0.0009 / +0.0009 (BL-left needs A₂ on one ring: it leans over A's tooth);  {C, X}, {C}:
+0.94 / +0.80 (A is essential);  {A, A₂, X}: +0.11 / +1.0 (C is essential).  **BL-floor = {A, C}; BL-left = {A, A₂, C}.**
X never touches a sector square — it enters only through the DIRECT-JAM domain (X meets C's wall drop, X misses the
open box), which is what keeps C where it is.  The worst rings are at 3.99 (h_u = 0.003–0.13, near-flat, A at offset
0.98: the lifted-end jam) and on the window at ŝ with margin −0.063 ≈ −(4 − ŝ)/2 = −0.0615: the flush limit.
**4.2 [M] the comparison** (`cmp264`).  T_u := C − h_u e_x (C's wall drop: a wall-touching cell at C's tilt, offset
h_v < 1 — it meets the open box because C does).  With C replaced by T_u: BL-floor ≤ −0.0123, BL-left ≤ −0.0052 on all
323 rings (−0.0610 / −0.0641 on the window); with C replaced by its floor drop T_v the sectors FAIL (+0.11, +0.94):
the comparison obstacle is the WALL drop, not the floor drop.  Strip test: max over free squares Q of the true
pocket in the BL sectors of area(Q ∩ (T_u ∖ C)) = 0 on 323/323 rings.
**4.3 The reduction [T given STRIP].**  *STRIP [C]: in a JAM corner, a unit square interior-disjoint from A, C, X, inside
the container, with (q − O)·(−v) ≥ ½, q_x ≤ s/2 (or the BL-left form) has no interior point in T_u ∖ C.*  Given STRIP,
every free square of the BL sectors avoids T_u (it avoids C and T_u ∖ C), so the BL-sector pocket of {A, A₂, X, C} is
contained in the pocket of {A, A₂, T_u} — A262's `pair3` family at the BL corner (floor row (a, φ) + one wall square
(h_v, θ), 4 parameters, s eliminated as in A259 §2.3, domain h_v < 1, a < 1), whose certificate is running (chain3)
and whose verifier is `verify262`.  Monotonicity is in the right direction: the obstacles A, A₂, T_u are each inside
A ∪ A₂ ∪ C ∪ (the strip no sector square enters).  STRIP is a 3-square statement (A, C, X + Q) — the geometry: a
square entering the strip between the wall and C's left flank while low must pass under X (y_X ≥ 1 − c_X) and over A's
tooth (depth ≥ cos φ); on every ring the strip is narrower than the space this leaves.  Not proved.
**4.4 N6 corrected [F → M].**  no_jam.md §4 said "j = 2 ADJACENT: no ring found".  A262's own chain2 (`adv262`, 160
rows) finds adjacent JAM rings (corners 3, 0) at every side: t = 0.0010 (3.82), 0.0071 (ŝ), 0.0053 (3.95), 0.0082 (3.99),
capacity 1 (pierce ≤ −0.081 at ŝ, −0.155 at 3.82), and two rows at ŝ where ring + free square IS family-stuck (a
9-packing; harmless for the count).  j = 3 (corners 3, 0, 1): rings at 3.95 / 3.99 (room 0), none on the window
(best −0.0052 at ŝ); j = 4: at 3.95 (t = 0.0001) / 3.99, room 0.  Opposite j = 2: rings at all sides, room 0.
The room statement is per corner (no_jam.md §2.4), so the adjacent ring adds no new sector type: its BR corner is
the mirror JAM with the floor's single toucher A in X's role (A misses the BR box since a + w ≤ s − 2 + … there).
**4.5 N3, N5.**  Not run: `float262` and the indirect-jam scan are queued behind search262 (399 rows at exit, all
capacity ≤ 1, none family-stuck, no 11-witness).  Nothing here changes them.

## 5. What the brief had wrong

1. Lemma 3's "b ≥ 1 + ε(1 − a) − K ε² … side ≥ 3.9347 − K′ε₀²": the mechanism is not a single END offset pushed past 1
   but BOTH offsets of a (+,−) corner pushed to 1 − O(ε₀), and the closing side is 4 − O(ε₀), not 3.9347; no Taylor
   remainder and no interval certificate are needed — the forms are exact and the bounds are elementary.
2. Lemma 1 (i) "C's far vertex reaches ~1.94 toward O, C is a bigger obstacle than a toucher": C's far vertex reaches
   2.24–2.43 from the corner (`sub264`), but what matters is the WALL drop T_u, not the floor drop or the far vertex;
   and the fictitious toucher must be INSIDE C ∪ (an unreachable strip) for the comparison to be sound — hence STRIP.
3. N6 "adjacent j = 2: none found": false, they exist on the whole window (4.4).
4. Lemma 2 "the gap admits a unit cell ⟹ met by ≥ 2 non-toucher squares … > 3 free squares": the first half is P1⁺
   verbatim (2.2) and allows S′ as the single meeter; the count to 4 is not a consequence of anything proved here.

## 6. Lean, reproduce

`Statements/Open/ThreeLemmas.lean`: axioms [T-prose] `mixed_corner_pm`, `mixed_corner_mp`, `pinwheel_corner_pp` (the
corner lemmas §3.2 on the opaque corner predicates), theorems `cube_pppm`, `cube_pmpm`, `cube_ppmm` (§3.3 by
`linarith`), `slab_cube_264` (the three together, replacing A263's axiom `slab_cube` for rings of pairs); axiom [C]
`strip_lemma`; theorem `jam_sector_of_strip` (4.3, from `strip_lemma` and A262's `pair3` as a hypothesis); build +
audit 0 sorry.  Reproduce: `python attempts/A264-three-lemmas/code/cube264.py` (1 min), `sub264.py` (10 min),
`cmp264.py` (15 min), `pages264.py`.
