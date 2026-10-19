import PackingCertMathlib.Statements.Open.StripJam

/-!
# -- OPEN: STRIP₂ on the near-flat corner by hand (X flat, and θ, φ ≤ 5°) — A276

`docs/proofs/flat_x.md` (derivation in `attempts/A276-flat-x/notes/flatx276_part0..6.md`).  Corner frame as in
`StripJam.lean`: `C` the floater (`h_u`, `θ`, `c = cos θ`, `s = sin θ`, `k = tan θ`, top vertex `T = (T_x, C_top)`,
`T_x = h_u + c`, `w0 = T_x − 1`), `T_u = C − h_u e_x` with top vertex `T′ = (c, C_top)`, `X` the wall toucher (tilt
`φ`, flat when `φ = 0`), `D = C_top − X_low`, `Q` the free square (lowest vertex `V`, tilt `ω`, left vertex `W_L`).

**What is a theorem here (the arithmetic cores).**
* `dip_window` [T] (part 1 (1.1)): X's flat bottom edge above C's upper-left edge at `x = 1` gives
  `D ≤ (h_u + c − 1) tan θ`.
* `near_miss_pos` [T] (part 1 (1.4)): the corner `(1, C_top)` is at distance `(1 − c) c > 0` from `T_u`
  (the foot of the perpendicular is on T_u's upper-right edge, `(P − T′)·(c, s) = (1 − c) c`).
* `lemma_a_dv` [T] (part 2 (2.1)): the chord at `C_top` has right end `V_x + d_V cot ω ≤ T_x` and `V_x ≥ 1 + sin ω`,
  so `d_V cot ω ≤ w0 − sin ω`.
* `clearance_core` [T] (part 4, Lemma A*): `1 − c > w0 tan²θ / 4` whenever `1/3 ≤ c < 1`, `0 ≤ w0 < c`: the cap of a
  square right of `x = 1` (left boundary on the edge `V W_L` at `C_top`) stays right of T_u's upper-right edge line.
* `a2_core` [T] (part 6 §6.1): a centre with `q_x ≥ w_φ + 0.468` (disc chord at `X_low*` right of R_X, `w_φ ≥ 1`)
  and `q_x + 0.218 < h_u + s ≤ 1.09` (disc chord 0.45 below the centre left of C's lower-left edge) is impossible.
* `delta_core` [T] (part 5 §5.2, case φ > θ): `cos²ω + (w_φ − 1) sin ω > sin φ cos ω` when `sin ω ≥ 0.707`,
  `w_φ − 1 ≥ 0.95 sin φ`, `0 < sin φ ≤ 0.0875` — the AM–GM step that kills the case `W_L` under X's bottom vertex.
* `strip_two_in_ring_of_corner` [T from the axiom]: the BL sectors of a JAM corner reduce to `pair3` under
  `JamCorner ∧ CornerTilts` — A271/A272's bridge with the disc lemma replaced by the corner hypothesis.

**What is not.**
* `FlatXTilt`, `CornerTilts` are opaque propositions ("`φ = 0` and `0 < θ ≤ 30°`", "`0 ≤ θ, φ ≤ 5°`", tilts of C and X in a
  JAM corner): the tilts are not fields of A271's opaque `JamCorner`.
* `strip_two_in_jam_flat_x`, `strip_two_in_jam_corner` [T-prose]: Theorems FLAT-X (flat_x.md §0, parts 2–3) and CORNER
  (parts 4–6) — the case split by the height of Q's left vertex against X (Lemma A / A*, cases B, C, β, γ, δ, A1, A2),
  each case a chord/pin inequality whose arithmetic core is one of the theorems above or a numeric bound stated with
  its slack in the parts (A1 at φ > 0: a grid check, `check276b`).  These are the axioms of this file.
-/

namespace PackingCert.S11.OpenLemmas.FlatX

open PackingCert.S11.OpenLemmas.RingDomain

/-- **The dip window at X flat** [T]: `X_low ≥ y1 = L_h + (1 − h_u) k`, `C_top = L_h + s`, `s = c k`, `D = C_top − X_low`
give `D ≤ (h_u + c − 1) k`. -/
theorem dip_window (hu c s k Lh Xlow Ctop D : ℝ) (hy : Lh + (1 - hu) * k ≤ Xlow) (hC : Ctop = Lh + s)
    (hs : s = c * k) (hD : D = Ctop - Xlow) : D ≤ (hu + c - 1) * k := by
  subst hC hs hD; nlinarith

/-- **The near-miss distance is positive** [T]: `0 < c < 1` gives `0 < (1 − c) c`. -/
theorem near_miss_pos (c : ℝ) (h0 : 0 < c) (h1 : c < 1) : 0 < (1 - c) * c := by
  nlinarith

/-- **Lemma A, (2.1)** [T]: `V_x + d_V k' ≤ 1 + w0` and `1 + sω ≤ V_x` give `d_V k' ≤ w0 − sω`. -/
theorem lemma_a_dv (Vx dV k' w0 som : ℝ) (h : Vx + dV * k' ≤ 1 + w0) (hV : 1 + som ≤ Vx) :
    dV * k' ≤ w0 - som := by
  linarith

/-- **Lemma A\*, the constant** [T]: `c² + s² = 1`, `s = c k`, `1/3 ≤ c < 1`, `0 ≤ w0 < c` give `w0 k² / 4 < 1 − c`. -/
theorem clearance_core (c s k w0 : ℝ) (h1 : c ^ 2 + s ^ 2 = 1) (hs : s = c * k) (hc0 : 1 / 3 ≤ c)
    (hc1 : c < 1) (hw0 : 0 ≤ w0) (hw : w0 < c) : w0 * k ^ 2 / 4 < 1 - c := by
  subst hs
  have hpos : 0 < 1 + c := by linarith
  have hc : 0 < c := by linarith
  have key : (1 - c) * (1 + c) = c ^ 2 * k ^ 2 := by nlinarith
  have hck : 0 < c ^ 2 * k ^ 2 := by rw [← key]; exact mul_pos (by linarith) hpos
  have hc2 : c ^ 2 ≤ 1 := by nlinarith
  have hk : 0 < k ^ 2 := by nlinarith [sq_nonneg k, mul_nonneg (sub_nonneg.2 hc2) (sq_nonneg k)]
  have h4 : w0 * (1 + c) < 4 * c ^ 2 := by
    nlinarith [mul_lt_mul_of_pos_right hw hpos, mul_le_mul_of_nonneg_left hc0 hc.le]
  have h5 : 0 < k ^ 2 * (4 * c ^ 2 - w0 * (1 + c)) := mul_pos hk (by linarith)
  nlinarith [h5, key, hpos]

/-- **A2, the two pins** [T]: `w + 0.468 ≤ q_x`, `q_x + 0.218 < h`, `1 ≤ w`, `h ≤ 1.09` are inconsistent. -/
theorem a2_core (qx w h : ℝ) (hw : 1 ≤ w) (hq : w + 0.468 ≤ qx) (hh : qx + 0.218 < h) (hh1 : h ≤ 1.09) :
    False := by
  linarith

/-- **Case δ, φ > θ: the AM–GM step** [T]: `c_ω² + s_ω² = 1`, `0.707 ≤ s_ω`, `0 < c_ω`, `0.95 p ≤ w1`, `0 < p ≤ 0.0875`
give `p c_ω < c_ω² + w1 s_ω` (i.e. `cos ω + (w_φ − 1) tan ω > sin φ`). -/
theorem delta_core (com som w1 p : ℝ) (h1 : com ^ 2 + som ^ 2 = 1) (hs : 0.707 ≤ som) (hc : 0 < com)
    (hw : 0.95 * p ≤ w1) (hp0 : 0 < p) (hp1 : p ≤ 0.0875) : p * com < com ^ 2 + w1 * som := by
  have hsom0 : (0:ℝ) ≤ som := by linarith
  have hA : 0.95 * p * som ≤ w1 * som := mul_le_mul_of_nonneg_right hw hsom0
  have hB : p * 0.707 ≤ p * som := mul_le_mul_of_nonneg_left hs hp0.le
  have hC : 0 < p * (0.672 - p / 4) := mul_pos hp0 (by linarith)
  nlinarith [hA, hB, hC, sq_nonneg (com - p / 2)]

/-- "X flat and `0 < θ ≤ 30°`" in a JAM corner (tilts are not fields of the opaque `JamCorner`): opaque. -/
opaque FlatXTilt : Prop

/-- "`0 ≤ θ ≤ 5°` and `0 ≤ φ ≤ 5°`" in a JAM corner: opaque. -/
opaque CornerTilts : Prop

/-- **Theorem FLAT-X** [T-prose] (flat_x.md §0, §3): under H1–H3 with X flat and `θ ≤ 30°`, no unit square of the
quadrant interior-disjoint from `C` and `X` has an interior point in `T_u ∖ C`. -/
axiom strip_two_in_jam_flat_x (hjam : JamCorner) (hflat : FlatXTilt) (Q : Set RP)
    (h : PackingCert.S11.OpenLemmas.StripPlug.TwoFree Q) :
    ¬ PackingCert.S11.OpenLemmas.ThreeLemmas.InStrip Q

/-- **Theorem CORNER** [T-prose] (flat_x.md §0, §4): the same on `0 ≤ θ, φ ≤ 5°` — A273's open layer. -/
axiom strip_two_in_jam_corner (hjam : JamCorner) (hcorner : CornerTilts) (Q : Set RP)
    (h : PackingCert.S11.OpenLemmas.StripPlug.TwoFree Q) :
    ¬ PackingCert.S11.OpenLemmas.ThreeLemmas.InStrip Q

/-- **The BL sectors of a JAM corner reduce to `pair3`** [T from `strip_two_in_jam_corner`] on the corner. -/
theorem strip_two_in_ring_of_corner (hjam : JamCorner) (hcorner : CornerTilts)
    (hsub : ∀ Q, PackingCert.S11.OpenLemmas.ThreeLemmas.JamSectorFree Q →
      PackingCert.S11.OpenLemmas.StripPlug.TwoFree Q)
    (hcover : ∀ Q, PackingCert.S11.OpenLemmas.ThreeLemmas.JamSectorFree Q →
      ¬ PackingCert.S11.OpenLemmas.ThreeLemmas.InStrip Q →
      PackingCert.S11.OpenLemmas.ThreeLemmas.Pair3Free Q)
    (hpair3 : ∀ Q, ¬ PackingCert.S11.OpenLemmas.ThreeLemmas.Pair3Free Q) (Q : Set RP) :
    ¬ PackingCert.S11.OpenLemmas.ThreeLemmas.JamSectorFree Q :=
  fun h => hpair3 Q (hcover Q h (strip_two_in_jam_corner hjam hcorner Q (hsub Q h)))

#print axioms dip_window
#print axioms near_miss_pos
#print axioms lemma_a_dv
#print axioms clearance_core
#print axioms a2_core
#print axioms delta_core
#print axioms strip_two_in_ring_of_corner

end PackingCert.S11.OpenLemmas.FlatX
