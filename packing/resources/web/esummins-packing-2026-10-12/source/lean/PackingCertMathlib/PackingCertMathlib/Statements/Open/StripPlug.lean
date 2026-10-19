import PackingCertMathlib.Statements.Open.ThreeLemmas

/-!
# -- OPEN: STRIP and the PLUG — the ADJ-consistent side of a box certificate, the graded plug, the reduced STRIP,
# the gap count — A265

`docs/proofs/strip_plug.md`.

**What is a theorem here.**
* `adj_side_bound` [T]: a box of A263's P2 family (offsets `b, a'`, tilt widths `w(φ_W), w(φ₁')`) carries an all-ADJ
  ring at side `s` only if `s ≤ s_eff := min(SMAX, hi_b + w_hi + 2, hi_a' + w'_hi + 2)`; `p2_of_adj_side` [T]: with
  the corner-frame monotonicity of A259 §2.3 / A263 `clip_mono` as the hypothesis `hmono`, a certificate of the
  box at `s_eff` is a certificate at every side of the family.  This is why A263's OPEN P2 leaves (checked at 3.8771,
  ADJ-feasible only near 3.82) certify in `cert265`.
* `plug_graded` [T]: Lemma PLUG (locked_wall.md §4) for any `ρ ≤ 1/4`: with `a' ∈ (0.354 + ρ, 1)` the START
  square's lowest vertex `(cos φ', a')` lies in the open kernel `(w/2 + ρ − 1/(2w), w/2 + 1/(2w))²` of every unit
  square (width `w ∈ [1, √2]`) that reaches within `ρ` of the corner — from `plug_kernel`.
* `strip_of_two_obstacles` [T]: STRIP against the two obstacles `C, X` (the strip's own walls) implies STRIP
  against `A, A₂, X, C` (fewer obstacles = more squares); the two-obstacle statement is `strip_two` [C].
* `gap_needs_two_misses` [T]: eight ring squares and eleven in all leave three free squares, at most one containing
  `O`: at least TWO free squares miss `O`.  So the room statement the chain needs on the non-ADJ family is
  CAPACITY-2 (no two interior-disjoint free squares both miss `O`), weaker than ROOM ≤ 1 (strip_plug.md §3).

**What is not.**
* `strip_two` [C]: STRIP against `{C, X}` alone — [T-computed] on 18 of A264's 323 JAM rings at exit, the rest in
  the lane (`strip265`): no unit square of the corner quadrant interior-disjoint from `C` and `X` has an interior
  point in `T_u ∖ C` (−9 on every ring tested: such a square does not exist, sector condition unused); a hand proof
  is written for a flat `C` only (strip_plug.md §1.3).
-/

namespace PackingCert.S11.OpenLemmas.StripPlug

/-- **ADJ-SIDE** [T]: the all-ADJ family at side `s` has `b + w(φ_W) ≥ s − 2` and `a' + w(φ₁') ≥ s − 2`; over a box
with upper corners `hb, hw, ha, hw'` this bounds the side. -/
theorem adj_side_bound (s b w a w' hb hw ha hw' smax : ℝ) (hs : s ≤ smax)
    (hW : s - 2 ≤ b + w) (hS : s - 2 ≤ a + w') (h1 : b ≤ hb) (h2 : w ≤ hw) (h3 : a ≤ ha) (h4 : w' ≤ hw') :
    s ≤ min smax (min (hb + hw + 2) (ha + hw' + 2)) := by
  refine le_min hs (le_min ?_ ?_) <;> linarith

/-- **The certificate at `s_eff` transfers** [T]: `P2` is any side-indexed statement that is monotone downward in
the side (A259 §2.3 corner-frame monotonicity + A263 `clip_mono`, taken as `hmono`). -/
theorem p2_of_adj_side (P2 : ℝ → Prop) (hmono : ∀ s t : ℝ, s ≤ t → P2 t → P2 s)
    (s b w a w' hb hw ha hw' smax : ℝ) (hs : s ≤ smax)
    (hW : s - 2 ≤ b + w) (hS : s - 2 ≤ a + w') (h1 : b ≤ hb) (h2 : w ≤ hw) (h3 : a ≤ ha) (h4 : w' ≤ hw')
    (hcert : P2 (min smax (min (hb + hw + 2) (ha + hw' + 2)))) : P2 s :=
  hmono _ _ (adj_side_bound s b w a w' hb hw ha hw' smax hs hW hS h1 h2 h3 h4) hcert

/-- **PLUG, graded** [T]: for `0 ≤ ρ ≤ 1/4`, `w ∈ [1, √2]`, `0.354 + ρ < a' < 1`, `0.707 ≤ c < 1` the point
`(c, a')` lies strictly inside `(w/2 + ρ − 1/(2w), w/2 + 1/(2w))²` — cleared of the denominator `2w`:
`w² − 1 + 2wρ < 2w·a' < w² + 1` and the same for `c`.  With `c = cos φ'` this is `V' ∈ int Q` (locked_wall.md §4). -/
theorem plug_graded (w ρ a c : ℝ) (h1 : 1 ≤ w) (h2 : w * w ≤ 2) (hρ0 : 0 ≤ ρ) (hρ : ρ ≤ 1 / 4)
    (ha : (354 : ℝ) / 1000 + ρ < a) (ha1 : a < 1) (hc : (707 : ℝ) / 1000 ≤ c) (hc1 : c < 1) :
    (w * w - 1 + 2 * w * ρ < 2 * w * a ∧ 2 * w * a < w * w + 1) ∧
    (w * w - 1 + 2 * w * ρ < 2 * w * c ∧ 2 * w * c < w * w + 1) := by
  obtain ⟨k1, k2⟩ := PackingCert.S11.OpenLemmas.LockedWall.plug_kernel w h1 h2
  have hw : 0 < w := by linarith
  refine ⟨⟨?_, ?_⟩, ?_, ?_⟩
  · nlinarith [mul_lt_mul_of_pos_left ha hw]
  · nlinarith [mul_lt_mul_of_pos_left ha1 hw]
  · nlinarith [mul_le_mul_of_nonneg_left hc hw.le, mul_le_mul_of_nonneg_left hρ hw.le]
  · nlinarith [mul_lt_mul_of_pos_left hc1 hw]

/-- A unit square of the corner quadrant avoiding `C` and `X` (opaque); avoiding also `A, A₂` is a special case. -/
opaque TwoFree (Q : Set RP) : Prop

/-- **STRIP against `{C, X}`** [C] (strip_plug.md §1): no unit square of the quadrant interior-disjoint from `C`
and `X` has an interior point in `T_u ∖ C`.  [T-computed] on 18 JAM rings at exit, 323 in the lane (`strip265`). -/
axiom strip_two (Q : Set RP) (h : TwoFree Q) :
    ¬ PackingCert.S11.OpenLemmas.ThreeLemmas.InStrip Q

/-- **Monotonicity** [T]: A264's `strip_lemma` (against `A, A₂, X, C` in the sector) follows from `strip_two`,
given that a sector square avoiding the four squares avoids `C, X` (`hsub`). -/
theorem strip_of_two_obstacles
    (hsub : ∀ Q, PackingCert.S11.OpenLemmas.ThreeLemmas.JamSectorFree Q → TwoFree Q) (Q : Set RP)
    (h : PackingCert.S11.OpenLemmas.ThreeLemmas.JamSectorFree Q) :
    ¬ PackingCert.S11.OpenLemmas.ThreeLemmas.InStrip Q :=
  strip_two Q (hsub Q h)

/-- **The count the non-ADJ family needs** [T] (strip_plug.md §3): `8 + F = 11` free squares, of which `nO ≤ 1`
contain `O` (HOLE-ONE) and the rest miss it: at least two free squares miss `O`.  ROOM ≤ 1 (every free square
contains `O`) is therefore more than the chain needs; CAPACITY-2 suffices. -/
theorem gap_needs_two_misses (F nO nMiss : ℕ) (hF : 8 + F = 11) (hO : nO ≤ 1) (h : nO + nMiss = F) :
    2 ≤ nMiss := by omega

#print axioms adj_side_bound
#print axioms p2_of_adj_side
#print axioms plug_graded
#print axioms strip_of_two_obstacles
#print axioms gap_needs_two_misses

end PackingCert.S11.OpenLemmas.StripPlug
