import Sqpack.LemmaELeaf
import Sqpack.CapK
import Sqpack.ZMTreeX

/-!
# The pose tree of the `EXACT` certificate

The semantics of a node: `CovT` — every admissible pose of the box with `u ∈ (u₀/R, u₁/R]` **and
`θ ≤ 45°`** (`u² + 2u ≤ 1`) captures mass `≥ W`.  The `45°` cap is all the D4 reduction needs
(`d4_reduction_measure` reduces every pose to `θ ∈ [0°, 45°]`), so the `SYM` leaves of `qx2_zm` (boxes
entirely past `45°`) hold vacuously; the open lower end matches Lemma E (`CovMPo.of_exact`), and the
face `θ = 0` is a separate Lemma Z grid.

Nodes: splits in `x`, `y`, `u` (at any point), `clip_bin` (`ZMTree.clipOk`), a change of the scales
`S` and `R` (leaves are checked at their own denominators), and leaves: `EXACT`, `LEB`, `EMPTY`
(`ZMTree.eOk`), `SYM`, and `u₁ = 0`.  The tree is not a data structure: a generator writes it as a
proof term of these lemmas over the leaf theorems.
-/

open MeasureTheory

namespace SquarePacking

namespace ZMTreeM

open BoxTree ZMTree

variable {D S Mq R W : ℕ} {pts : List (ℕ × ℕ × ℕ)} {segs : List SegE} {rects : List RectE}
  {x0 x1 y0 y1 u0 u1 : ℕ}

/-- **The node semantics**: open lower end in `u`, poses up to `45°`. -/
def CovT (D S Mq R W : ℕ) (pts : List (ℕ × ℕ × ℕ)) (segs : List SegE) (rects : List RectE)
    (x0 x1 y0 y1 u0 u1 : ℕ) : Prop :=
  ∀ (c : ℝ × ℝ) (u : ℝ),
    (x0 : ℝ) / (D * S) ≤ c.1 → c.1 ≤ (x1 : ℝ) / (D * S) →
    (y0 : ℝ) / (D * S) ≤ c.2 → c.2 ≤ (y1 : ℝ) / (D * S) →
    (u0 : ℝ) / R < u → u ≤ (u1 : ℝ) / R → u ^ 2 + 2 * u ≤ 1 →
    sq c (2 * Real.arctan u) 1 ⊆ box ((Mq : ℝ) / D) →
    (W : ℝ) ≤ ptMass D pts (sq c (2 * Real.arctan u) 1) + segMass D segs (sq c (2 * Real.arctan u) 1)
      + rectMass D rects (sq c (2 * Real.arctan u) 1)

theorem CovT.of_covMPo (h : CovMPo D S Mq R W pts segs rects x0 x1 y0 y1 u0 u1) :
    CovT D S Mq R W pts segs rects x0 x1 y0 y1 u0 u1 :=
  fun c u hx0 hx1 hy0 hy1 hu0 hu1 _ hsub => h c u hx0 hx1 hy0 hy1 hu0 hu1 hsub

theorem CovT.of_covMP (h : CovMP D S Mq R W pts segs rects x0 x1 y0 y1 u0 u1) :
    CovT D S Mq R W pts segs rects x0 x1 y0 y1 u0 u1 :=
  CovT.of_covMPo (CovMPo.of_covMP h)

theorem CovT.of_covM (h : CovM D S Mq R W pts segs x0 x1 y0 y1 u0 u1) :
    CovT D S Mq R W pts segs rects x0 x1 y0 y1 u0 u1 :=
  CovT.of_covMP (CovMP.of_covM h)

theorem CovT.splitX (m : ℕ) (h1 : CovT D S Mq R W pts segs rects x0 m y0 y1 u0 u1)
    (h2 : CovT D S Mq R W pts segs rects m x1 y0 y1 u0 u1) :
    CovT D S Mq R W pts segs rects x0 x1 y0 y1 u0 u1 := by
  intro c u hx0 hx1 hy0 hy1 hu0 hu1 h45 hsub
  rcases le_total c.1 ((m : ℝ) / (D * S)) with h | h
  · exact h1 c u hx0 h hy0 hy1 hu0 hu1 h45 hsub
  · exact h2 c u h hx1 hy0 hy1 hu0 hu1 h45 hsub

theorem CovT.splitY (m : ℕ) (h1 : CovT D S Mq R W pts segs rects x0 x1 y0 m u0 u1)
    (h2 : CovT D S Mq R W pts segs rects x0 x1 m y1 u0 u1) :
    CovT D S Mq R W pts segs rects x0 x1 y0 y1 u0 u1 := by
  intro c u hx0 hx1 hy0 hy1 hu0 hu1 h45 hsub
  rcases le_total c.2 ((m : ℝ) / (D * S)) with h | h
  · exact h1 c u hx0 hx1 hy0 h hu0 hu1 h45 hsub
  · exact h2 c u hx0 hx1 h hy1 hu0 hu1 h45 hsub

theorem CovT.splitU (m : ℕ) (h1 : CovT D S Mq R W pts segs rects x0 x1 y0 y1 u0 m)
    (h2 : CovT D S Mq R W pts segs rects x0 x1 y0 y1 m u1) :
    CovT D S Mq R W pts segs rects x0 x1 y0 y1 u0 u1 := by
  intro c u hx0 hx1 hy0 hy1 hu0 hu1 h45 hsub
  rcases le_or_gt u ((m : ℝ) / R) with h | h
  · exact h1 c u hx0 hx1 hy0 hy1 hu0 h h45 hsub
  · exact h2 c u hx0 hx1 hy0 hy1 h hu1 h45 hsub

/-- A bin with `u₁ = 0` has no pose with `u > u₀/R ≥ 0` (the `AXIS` leaves; `θ = 0` is Lemma Z). -/
theorem CovT.of_top_zero (hR : 0 < R) : CovT D S Mq R W pts segs rects x0 x1 y0 y1 u0 0 := by
  intro c u _ _ _ _ hu0 hu1 _ _
  have hRr : (0 : ℝ) < R := by exact_mod_cast hR
  have : (0 : ℝ) ≤ (u0 : ℝ) / R := div_nonneg (Nat.cast_nonneg _) hRr.le
  simp at hu1; linarith

/-- A bin of width zero has no pose with `u₀/R < u ≤ u₀/R`. -/
theorem CovT.of_degen : CovT D S Mq R W pts segs rects x0 x1 y0 y1 u0 u0 := by
  intro c u _ _ _ _ hu0 hu1 _ _
  linarith

/-- **`SYM`**: a bin past `45°` (`U₀² + 2U₀R > R²`) has no pose with `θ ≤ 45°`. -/
theorem CovT.of_sym (hR : 0 < R) (h : Nat.blt (R * R) (u0 * u0 + 2 * u0 * R) = true) :
    CovT D S Mq R W pts segs rects x0 x1 y0 y1 u0 u1 := by
  intro c u _ _ _ _ hu0 _ h45 _
  exfalso
  have hRr : (0 : ℝ) < R := by exact_mod_cast hR
  simp only [Nat.blt_eq] at h
  have h' : (R : ℝ) * R < u0 * u0 + 2 * u0 * R := by exact_mod_cast h
  have hu : (u0 : ℝ) < u * R := by rw [div_lt_iff₀ hRr] at hu0; linarith
  have hu0' : (0 : ℝ) ≤ u0 := Nat.cast_nonneg _
  nlinarith [mul_pos hRr hRr]

/-- A change of the centre scale: the box over `D·(kS)` with coordinates `k·x`. -/
theorem CovT.scaleS {k : ℕ} (hk : 0 < k)
    (h : CovT D (S * k) Mq R W pts segs rects (x0 * k) (x1 * k) (y0 * k) (y1 * k) u0 u1) :
    CovT D S Mq R W pts segs rects x0 x1 y0 y1 u0 u1 := by
  have hkr : (k : ℝ) ≠ 0 := by exact_mod_cast hk.ne'
  have e : ∀ z : ℕ, ((z * k : ℕ) : ℝ) / (D * (S * k : ℕ)) = (z : ℝ) / (D * S) := by
    intro z; push_cast; field_simp
  intro c u hx0 hx1 hy0 hy1 hu0 hu1 h45 hsub
  exact h c u (by rw [e]; exact hx0) (by rw [e]; exact hx1) (by rw [e]; exact hy0)
    (by rw [e]; exact hy1) hu0 hu1 h45 hsub

/-- A change of the angle scale: the bin over `kR` with ends `k·u`. -/
theorem CovT.scaleR {k : ℕ} (hk : 0 < k)
    (h : CovT D S Mq (R * k) W pts segs rects x0 x1 y0 y1 (u0 * k) (u1 * k)) :
    CovT D S Mq R W pts segs rects x0 x1 y0 y1 u0 u1 := by
  have hkr : (k : ℝ) ≠ 0 := by exact_mod_cast hk.ne'
  have e : ∀ z : ℕ, ((z * k : ℕ) : ℝ) / ((R * k : ℕ) : ℝ) = (z : ℝ) / R := by
    intro z; push_cast; exact mul_div_mul_right _ _ hkr
  intro c u hx0 hx1 hy0 hy1 hu0 hu1 h45 hsub
  exact h c u hx0 hx1 hy0 hy1 (by rw [e]; exact hu0) (by rw [e]; exact hu1) h45 hsub

/-- The converse change of the centre scale. -/
theorem CovT.scaleS' {k : ℕ} (hk : 0 < k) (h : CovT D S Mq R W pts segs rects x0 x1 y0 y1 u0 u1) :
    CovT D (S * k) Mq R W pts segs rects (x0 * k) (x1 * k) (y0 * k) (y1 * k) u0 u1 := by
  have hkr : (k : ℝ) ≠ 0 := by exact_mod_cast hk.ne'
  have e : ∀ z : ℕ, ((z * k : ℕ) : ℝ) / (D * (S * k : ℕ)) = (z : ℝ) / (D * S) := by
    intro z; push_cast; field_simp
  intro c u hx0 hx1 hy0 hy1 hu0 hu1 h45 hsub
  rw [e] at hx0 hx1 hy0 hy1
  exact h c u hx0 hx1 hy0 hy1 hu0 hu1 h45 hsub

/-- The converse change of the angle scale. -/
theorem CovT.scaleR' {k : ℕ} (hk : 0 < k) (h : CovT D S Mq R W pts segs rects x0 x1 y0 y1 u0 u1) :
    CovT D S Mq (R * k) W pts segs rects x0 x1 y0 y1 (u0 * k) (u1 * k) := by
  have hkr : (k : ℝ) ≠ 0 := by exact_mod_cast hk.ne'
  have e : ∀ z : ℕ, ((z * k : ℕ) : ℝ) / ((R * k : ℕ) : ℝ) = (z : ℝ) / R := by
    intro z; push_cast; exact mul_div_mul_right _ _ hkr
  intro c u hx0 hx1 hy0 hy1 hu0 hu1 h45 hsub
  rw [e] at hu0 hu1
  exact h c u hx0 hx1 hy0 hy1 hu0 hu1 h45 hsub

/-- **`clip_bin`** (`ZMTree.C_cov`): poses with `u > us/R` are inadmissible. -/
lemma clip_inadm (hD : 0 < D) (hS : 0 < S) (hR : 0 < R) {us : ℕ}
    (h : clipOk (D * S) R x1 y1 u0 u1 us = true) {c : ℝ × ℝ} {u : ℝ}
    (hx1 : c.1 ≤ (x1 : ℝ) / (D * S)) (hy1 : c.2 ≤ (y1 : ℝ) / (D * S))
    (hgt : (us : ℝ) / R < u) (hu1 : u ≤ (u1 : ℝ) / R) (hsub : sq c (2 * Real.arctan u) 1 ⊆ box ((Mq : ℝ) / D)) :
    False := by
  simp only [clipOk, Bool.and_eq_true, Nat.ble_eq, Nat.blt_eq] at h
  obtain ⟨⟨⟨_, hsU1⟩, hw⟩, hmono⟩ := h
  have hQ : 0 < D * S := Nat.mul_pos hD hS
  have hRr : (0 : ℝ) < R := by exact_mod_cast hR
  have hQc : ((D : ℝ) * S) = ((D * S : ℕ) : ℝ) := by push_cast; ring
  rw [hQc] at hx1 hy1
  simp only [nat_mul_eq, nat_add_eq] at hmono
  have hmr : ((R : ℝ) + us) * (R + u1) < 2 * (R * R) := by exact_mod_cast hmono
  have husR : us < R := by
    by_contra hh
    push_neg at hh
    have : (R : ℝ) ≤ us := by exact_mod_cast hh
    nlinarith [(Nat.cast_nonneg u1 : (0 : ℝ) ≤ u1)]
  have hus0 : (0 : ℝ) ≤ (us : ℝ) / R := div_nonneg (Nat.cast_nonneg _) hRr.le
  have hu0' : 0 ≤ u := le_trans hus0 hgt.le
  have hU1R : (u1 : ℝ) < R := by nlinarith [(Nat.cast_nonneg us : (0 : ℝ) ≤ us)]
  have hu1' : u ≤ 1 := le_trans hu1 ((div_le_one hRr).mpr hU1R.le)
  obtain ⟨wx, wy⟩ := adm_lo hsub
  rw [wid_two_arctan hu0' hu1'] at wx wy
  have hK := wge_sound hQ hR husR.le hw
  have hprod : 1 - ((us : ℝ) / R + u + (us : ℝ) / R * u) > 0 := by
    have hu1R : u * R ≤ u1 := by rw [le_div_iff₀ hRr] at hu1; linarith
    have e : 1 - ((us : ℝ) / R + u + (us : ℝ) / R * u)
        = (2 * (R * R) - (R + us) * (R + u * R)) / (R * R) := by field_simp; ring
    rw [e]
    apply div_pos _ (by positivity)
    nlinarith [(Nat.cast_nonneg us : (0 : ℝ) ≤ us)]
  have hinc : widU ((us : ℝ) / R) < widU u := by
    have := widU_sub ((us : ℝ) / R) u
    have hd : (0 : ℝ) < (1 + ((us : ℝ) / R) ^ 2) * (1 + u ^ 2) := by positivity
    have : 0 < widU u - widU ((us : ℝ) / R) := by
      rw [this]; exact div_pos (mul_pos (by linarith) hprod) hd
    linarith
  rcases min_choice x1 y1 with hm | hm <;> rw [hm] at hK
  · linarith
  · linarith

theorem CovT.clip (hD : 0 < D) (hS : 0 < S) (hR : 0 < R) {us : ℕ}
    (h : clipOk (D * S) R x1 y1 u0 u1 us = true)
    (hc : CovT D S Mq R W pts segs rects x0 x1 y0 y1 u0 us) :
    CovT D S Mq R W pts segs rects x0 x1 y0 y1 u0 u1 := by
  intro c u hx0 hx1 hy0 hy1 hu0 hu1 h45 hsub
  rcases le_or_gt u ((us : ℝ) / R) with hle | hgt
  · exact hc c u hx0 hx1 hy0 hy1 hu0 hle h45 hsub
  · exact (clip_inadm hD hS hR h hx1 hy1 hgt hu1 hsub).elim

/-- **`EMPTY`** (`ZMTree.eOk`): no admissible pose. -/
theorem CovT.of_empty (hD : 0 < D) (hS : 0 < S) (hR : 0 < R) (hu1R : u1 ≤ R)
    (h : eOk (D * S) R x1 y1 u0 u1 = true) : CovT D S Mq R W pts segs rects x0 x1 y0 y1 u0 u1 :=
  CovT.of_covM (CovM.of_cov (E_cov hD hS hR hu1R h))

/-- **`LEB`**. -/
theorem CovT.of_leb (hD : 0 < D) (hS : 0 < S) (hR : 0 < R) {e : RectE} (he : e ∈ rects)
    (h : lebOk D S Mq R W x0 x1 y0 y1 u0 u1 e = true) :
    CovT D S Mq R W pts segs rects x0 x1 y0 y1 u0 u1 :=
  CovT.of_covMP (CovMP.of_leb hD hS hR he h)

/-- **`EXACT`**. -/
theorem CovT.of_exact (hD : 0 < D) (hS : 0 < S) (hR : 0 < R) {lf : LemmaELeaf.ExLeaf}
    (h : LemmaELeaf.exOk D S R W x0 x1 y0 y1 u0 u1 segs rects lf = true) :
    CovT D S Mq R W pts segs rects x0 x1 y0 y1 u0 u1 :=
  CovT.of_covMPo (LemmaELeaf.CovMPo.of_exact hD hS hR h)

/-- A `CAP` leaf: Lemma K (`CapK.capOk_sound`). -/
theorem CovT.of_cap (hD : 0 < D) (hS : 0 < S) (hR : 0 < R) {k : CapK.CapC}
    (h : CapK.capOk D S R W x0 x1 y0 y1 u0 u1 segs rects k = true) :
    CovT D S Mq R W pts segs rects x0 x1 y0 y1 u0 u1 :=
  CovT.of_covMPo (CapK.capOk_sound hD hS hR h)

/-! ## The face `θ = 0` -/

/-- At `θ = 0` an admissible centre has `c₁ ≥ 1/2`: the face box may start at any `m ≤ Q/2`. -/
theorem CovMP.face_wallX {m : ℕ} (hD : 0 < D) (hS : 0 < S) (hm : 2 * m ≤ D * S)
    (h : CovMP D S Mq R W pts segs rects m x1 y0 y1 0 0) :
    CovMP D S Mq R W pts segs rects x0 x1 y0 y1 0 0 := by
  intro c u _ hx1 hy0 hy1 hu0 hu1 hsub
  have hRu : u = 0 := by
    simp only [Nat.cast_zero, zero_div] at hu0 hu1; linarith
  subst hRu
  obtain ⟨wx, _⟩ := adm_lo hsub
  rw [Real.arctan_zero, mul_zero] at wx
  simp only [wid, Real.cos_zero, Real.sin_zero, abs_one, abs_zero, add_zero] at wx
  refine h c 0 ?_ hx1 hy0 hy1 hu0 hu1 hsub
  have hQ : (0 : ℝ) < D * S := by positivity
  have hmr : (2 * m : ℝ) ≤ D * S := by exact_mod_cast hm
  rw [div_le_iff₀ hQ]; nlinarith

theorem CovMP.face_wallY {m : ℕ} (hD : 0 < D) (hS : 0 < S) (hm : 2 * m ≤ D * S)
    (h : CovMP D S Mq R W pts segs rects x0 x1 m y1 0 0) :
    CovMP D S Mq R W pts segs rects x0 x1 y0 y1 0 0 := by
  intro c u hx0 hx1 _ hy1 hu0 hu1 hsub
  have hRu : u = 0 := by
    simp only [Nat.cast_zero, zero_div] at hu0 hu1; linarith
  subst hRu
  obtain ⟨_, wy⟩ := adm_lo hsub
  rw [Real.arctan_zero, mul_zero] at wy
  simp only [wid, Real.cos_zero, Real.sin_zero, abs_one, abs_zero, add_zero] at wy
  refine h c 0 hx0 hx1 ?_ hy1 hu0 hu1 hsub
  have hQ : (0 : ℝ) < D * S := by positivity
  have hmr : (2 * m : ℝ) ≤ D * S := by exact_mod_cast hm
  rw [div_le_iff₀ hQ]; nlinarith

/-! ## The end-to-end lower bound from the pose tree -/

/-- `θ ∈ [0, π/4]` is `2 arctan u` with `u ≥ 0`, `70u ≤ 29` and `u² + 2u ≤ 1`. -/
lemma exists_u_of_theta45 {θ : ℝ} (hθ : θ ∈ Set.Icc 0 (Real.pi / 4)) :
    ∃ u : ℝ, 0 ≤ u ∧ 70 * u ≤ 29 ∧ u ^ 2 + 2 * u ≤ 1 ∧ 2 * Real.arctan u = θ := by
  obtain ⟨h0, h1⟩ := hθ
  have hpi := Real.pi_pos
  set u := Real.tan (θ / 2) with hu
  have he : 2 * Real.arctan u = θ := by
    rw [hu, Real.arctan_tan (by linarith) (by linarith)]; ring
  have hu0 : 0 ≤ u := Real.tan_nonneg_of_nonneg_of_le_pi_div_two (by linarith) (by linarith)
  have hs : Real.sin θ ≤ Real.sin (Real.pi / 4) :=
    Real.sin_le_sin_of_le_of_le_pi_div_two (by linarith) (by linarith) h1
  have hc : Real.cos (Real.pi / 4) ≤ Real.cos θ :=
    Real.cos_le_cos_of_nonneg_of_le_pi h0 (by linarith) h1
  rw [Real.sin_pi_div_four] at hs
  rw [Real.cos_pi_div_four] at hc
  rw [← he, sin_two_arctan] at hs
  rw [← he, cos_two_arctan] at hc
  have hN : (0 : ℝ) < 1 + u ^ 2 := by positivity
  have key : 2 * u ≤ 1 - u ^ 2 := by
    have := le_trans hs hc
    rwa [div_le_div_iff_of_pos_right hN] at this
  exact ⟨u, hu0, by nlinarith, by linarith, he⟩

/-- **The covering statement from a pose tree**: every closed unit square in `[0, Mq/D]²` captures
mass `≥ 1` of the mixed cover (`mcoverP`), from a `CovT` root and the face `θ = 0`. -/
theorem cover_of_tree (D S Mq R Um W : ℕ) (pts : PTree) (segs : STree) (rects : List RectE)
    (hD : 0 < D) (hS : 0 < S) (hR : 0 < R) (hUm : R ≤ 2 * Um) (hnd : pts.toList.Nodup)
    (hrnd : rects.Nodup) (hsym : d4Check Mq pts = true) (hssym : segD4Check Mq segs = true)
    (hrsym : rectD4Check Mq rects = true)
    (hcov0 : CovMP D S Mq R W pts.toList segs.toList rects 0 (Mq * S - Mq * S / 2) 0
      (Mq * S - Mq * S / 2) 0 0)
    (hcov : CovT D S Mq R W pts.toList segs.toList rects 0 (Mq * S - Mq * S / 2) 0
      (Mq * S - Mq * S / 2) 0 Um)
    (hW : 0 < W) :
    ∀ (c : ℝ × ℝ) (θ : ℝ), sq c θ 1 ⊆ box ((Mq : ℝ) / D) →
      1 ≤ (mcoverP D W pts segs rects).measure (sq c θ 1) := by
  classical
  set m : ℝ := (Mq : ℝ) / D with hm
  set M := mcoverP D W pts segs rects with hMdef
  have hWr : (0 : ℝ) < W := by exact_mod_cast hW
  have hDr : (0 : ℝ) < D := by exact_mod_cast hD
  have hSr : (0 : ℝ) < S := by exact_mod_cast hS
  have hRr : (0 : ℝ) < R := by exact_mod_cast hR
  -- the data facts
  simp only [segD4Check, Bool.and_eq_true] at hssym
  obtain ⟨hschain, hsall⟩ := hssym
  have hsnd : segs.toList.Nodup := STree.nodup_of_chainB _ hschain
  have pentry_ok : ∀ e ∈ pts.toList.toFinset,
      e.1 ≤ Mq ∧ (Mq - e.1, e.2.1, e.2.2) ∈ pts.toList.toFinset ∧
        (e.2.1, e.1, e.2.2) ∈ pts.toList.toFinset := by
    intro e he
    have h2 := (PTree.all_iff _ pts).mp hsym e (List.mem_toFinset.mp he)
    simp only [Bool.and_eq_true, Nat.ble_eq] at h2
    exact ⟨h2.1.1, List.mem_toFinset.mpr (PTree.mem_sound _ _ h2.1.2),
      List.mem_toFinset.mpr (PTree.mem_sound _ _ h2.2)⟩
  have sentry_ok : ∀ e ∈ segs.toList.toFinset,
      ptLt e.1 e.2.1 e.2.2.1 e.2.2.2.1 = true ∧ e.1 ≤ Mq ∧ e.2.2.1 ≤ Mq ∧
        sXg Mq e ∈ segs.toList.toFinset ∧ sSg e ∈ segs.toList.toFinset := by
    intro e he
    have h2 := (STree.all_iff _ segs).mp hsall e (List.mem_toFinset.mp he)
    simp only [Bool.and_eq_true, Nat.ble_eq] at h2
    exact ⟨h2.1.1.1.1, h2.1.1.1.2, h2.1.1.2, List.mem_toFinset.mpr (STree.mem_sound _ _ h2.1.2),
      List.mem_toFinset.mpr (STree.mem_sound _ _ h2.2)⟩
  have rentry_ok : ∀ e ∈ rects.toFinset,
      e.1 ≤ e.2.2.1 ∧ e.2.1 ≤ e.2.2.2.1 ∧ e.2.2.1 ≤ Mq ∧ rXg Mq e ∈ rects.toFinset ∧
        rSg e ∈ rects.toFinset := by
    intro e he
    simp only [rectD4Check, List.all_eq_true] at hrsym
    have h2 := hrsym e (List.mem_toFinset.mp he)
    simp only [Bool.and_eq_true, Nat.ble_eq, List.contains_iff_mem] at h2
    exact ⟨h2.1.1.1.1, h2.1.1.1.2, h2.1.1.2, List.mem_toFinset.mpr h2.1.2,
      List.mem_toFinset.mpr h2.2⟩
  have hnonneg : M.Nonneg :=
    ⟨fun _ _ => by simp only [hMdef, mcoverP]; positivity,
     fun _ _ => by simp only [hMdef, mcoverP]; positivity,
     fun _ _ => by simp only [hMdef, mcoverP]; positivity⟩
  have hvolX : ∀ e ∈ rects.toFinset, volume (rectSet D (rXg Mq e)) = volume (rectSet D e) := by
    intro e he
    obtain ⟨h1, _, h3, _, _⟩ := rentry_ok e he
    rw [rectSet_rXg Mq D hD e h1 h3]
    exact (measurePreserving_reflX m).measure_preimage (measurableSet_rectSet D e).nullMeasurableSet
  have hvolS : ∀ e, volume (rectSet D (rSg e)) = volume (rectSet D e) := by
    intro e
    rw [rectSet_rSg]
    exact measurePreserving_swapXY.measure_preimage (measurableSet_rectSet D e).nullMeasurableSet
  -- D4 invariance of the measure
  have hinv : D4InvM m M.measure := by
    refine M.d4InvM m (fun e _ => measurableSet_rectSet D e) (fun e => (Mq - e.1, e.2.1, e.2.2))
      (fun e => (e.2.1, e.1, e.2.2)) (sXg Mq) sSg (rXg Mq) rSg ?_ ?_ ?_ ?_ ?_ ?_
    · intro e he
      obtain ⟨hx, hpX, _⟩ := pentry_ok e he
      refine ⟨hpX, ?_, rfl, ?_⟩
      · change ptR D (Mq - e.1, e.2.1, e.2.2) = reflX m (ptR D e)
        simp only [ptR, reflX, hm, Nat.cast_sub hx]
        ext
        · simp only; field_simp
        · simp
      · obtain ⟨a, b, c⟩ := e
        simp only at hx ⊢
        ext <;> simp; omega
    · intro e he
      obtain ⟨h, ha, hc, hsX, _⟩ := sentry_ok e he
      obtain ⟨h1, h2, h3⟩ := sXg_eq Mq D e h ha hc
      refine ⟨hsX, ?_, h1, h3⟩
      change ((sXg Mq e).2.2.2.2 : ℝ) / W = (e.2.2.2.2 : ℝ) / W
      rw [h2]
    · intro e he
      obtain ⟨h1, _, h3, hrX, _⟩ := rentry_ok e he
      refine ⟨hrX, ?_, ?_, rectSet_rXg Mq D hD e h1 h3⟩
      · change ((rXg Mq e).2.2.2.2 : ℝ) * (volume (rectSet D (rXg Mq e))).toReal / W =
          (e.2.2.2.2 : ℝ) * (volume (rectSet D e)).toReal / W
        rw [hvolX e he]; rfl
      · obtain ⟨a, b, c, d, w⟩ := e
        simp only [rXg] at h1 h3 ⊢
        ext <;> simp <;> omega
    · intro e he
      exact ⟨(pentry_ok e he).2.2, rfl, rfl, rfl⟩
    · intro e he
      obtain ⟨h, _, _, _, hsS⟩ := sentry_ok e he
      obtain ⟨h1, h2, h3⟩ := sSg_eq D e h
      refine ⟨hsS, ?_, h1, h3⟩
      change ((sSg e).2.2.2.2 : ℝ) / W = (e.2.2.2.2 : ℝ) / W
      rw [h2]
    · intro e he
      obtain ⟨_, _, _, _, hrS⟩ := rentry_ok e he
      refine ⟨hrS, ?_, rfl, rectSet_rSg D e⟩
      change ((rSg e).2.2.2.2 : ℝ) * (volume (rectSet D (rSg e))).toReal / W =
        (e.2.2.2.2 : ℝ) * (volume (rectSet D e)).toReal / W
      rw [hvolS e]; rfl
  -- the measure of a square is the mass
  have hmass : ∀ (Qs : Set (ℝ × ℝ)), MeasurableSet Qs →
      M.measure Qs = ENNReal.ofReal
        ((ptMass D pts.toList Qs + segMass D segs.toList Qs + rectMass D rects Qs) / W) := by
    intro Qs hQs
    rw [M.measure_apply hnonneg hQs]
    congr 1
    simp only [MixedCover.mass, hMdef, mcoverP, ptMass, segMass, rectMass, gw_areaFrac]
    rw [add_div, add_div, Finset.sum_div, Finset.sum_div, Finset.sum_div]
    congr 1
    · congr 1
      refine Finset.sum_congr rfl fun e _ => ?_
      ring
  -- the region statement, from the tree
  have hcover : ∀ (c : ℝ × ℝ) (θ : ℝ), sq c θ 1 ⊆ box m → 1 ≤ M.measure (sq c θ 1) := by
    refine d4_reduction_measure m M.measure hinv fun c θ h1 h2 hθ hsub0 => ?_
    obtain ⟨u, hu0, hu1, h45, rfl⟩ := exists_u_of_theta45 hθ
    have hsub := hsub0
    have hu : u ∈ Set.Icc (0 : ℝ) (1 / 2) := ⟨hu0, by linarith⟩
    rw [hmass _ (measurableSet_sq _ _ _), ← ENNReal.ofReal_one]
    apply ENNReal.ofReal_le_ofReal
    have hhalf : m / 2 ≤ (((Mq * S - Mq * S / 2 : ℕ) : ℝ)) / (D * S) := by
      have h2 : Mq * S ≤ 2 * (Mq * S - Mq * S / 2) := by omega
      have h2r : ((Mq * S : ℕ) : ℝ) ≤ 2 * ((Mq * S - Mq * S / 2 : ℕ) : ℝ) := by exact_mod_cast h2
      rw [hm, div_div, div_le_div_iff₀ (by positivity) (by positivity)]
      push_cast at h2r
      nlinarith
    have hU : ((0 : ℕ) : ℝ) / R ≤ u := by simpa using hu.1
    have hU1 : u ≤ (Um : ℝ) / R := by
      rw [le_div_iff₀ hRr]
      have : (R : ℝ) ≤ 2 * Um := by exact_mod_cast hUm
      nlinarith [hu.2]
    rw [le_div_iff₀ hWr, one_mul]
    rcases eq_or_lt_of_le hu0 with h0 | h0
    · subst h0
      exact hcov0 c 0 (by simpa using h1.1) (le_trans h1.2 hhalf) (by simpa using h2.1)
        (le_trans h2.2 hhalf) hU (by simp) hsub
    · exact hcov c u (by simpa using h1.1) (le_trans h1.2 hhalf) (by simpa using h2.1)
        (le_trans h2.2 hhalf) (by simpa using h0) hU1 h45 hsub
  exact hcover

/-- **The lower bound from a pose tree** (`le_minSide_mixedP` with the tree semantics `CovT` for
`u > 0` and the face `θ = 0` separately). -/
theorem le_minSide_mixedT (D S Mq R Um W : ℕ) (pts : PTree) (segs : STree) (rects : List RectE)
    (hD : 0 < D) (hS : 0 < S) (hR : 0 < R) (hUm : R ≤ 2 * Um) (hnd : pts.toList.Nodup)
    (hrnd : rects.Nodup) (hsym : d4Check Mq pts = true) (hssym : segD4Check Mq segs = true)
    (hrsym : rectD4Check Mq rects = true)
    (hcov0 : CovMP D S Mq R W pts.toList segs.toList rects 0 (Mq * S - Mq * S / 2) 0
      (Mq * S - Mq * S / 2) 0 0)
    (hcov : CovT D S Mq R W pts.toList segs.toList rects 0 (Mq * S - Mq * S / 2) 0
      (Mq * S - Mq * S / 2) 0 Um)
    (n k : ℕ) (hn : (pts.wsum + segs.wsum) * (D * D) + rectsW rects < n * W * (D * D))
    (hk : n ≤ k * k) :
    (Mq : ℝ) / D ≤ minSide n := by
  classical
  set m : ℝ := (Mq : ℝ) / D with hm
  set M := mcoverP D W pts segs rects with hMdef
  have hW : 0 < W := by
    rcases Nat.eq_zero_or_pos W with h | h
    · rw [h] at hn; simp at hn
    · exact h
  have hWr : (0 : ℝ) < W := by exact_mod_cast hW
  have hDr : (0 : ℝ) < D := by exact_mod_cast hD
  have hSr : (0 : ℝ) < S := by exact_mod_cast hS
  have hRr : (0 : ℝ) < R := by exact_mod_cast hR
  -- the data facts
  simp only [segD4Check, Bool.and_eq_true] at hssym
  obtain ⟨hschain, hsall⟩ := hssym
  have hsnd : segs.toList.Nodup := STree.nodup_of_chainB _ hschain
  have pentry_ok : ∀ e ∈ pts.toList.toFinset,
      e.1 ≤ Mq ∧ (Mq - e.1, e.2.1, e.2.2) ∈ pts.toList.toFinset ∧
        (e.2.1, e.1, e.2.2) ∈ pts.toList.toFinset := by
    intro e he
    have h2 := (PTree.all_iff _ pts).mp hsym e (List.mem_toFinset.mp he)
    simp only [Bool.and_eq_true, Nat.ble_eq] at h2
    exact ⟨h2.1.1, List.mem_toFinset.mpr (PTree.mem_sound _ _ h2.1.2),
      List.mem_toFinset.mpr (PTree.mem_sound _ _ h2.2)⟩
  have sentry_ok : ∀ e ∈ segs.toList.toFinset,
      ptLt e.1 e.2.1 e.2.2.1 e.2.2.2.1 = true ∧ e.1 ≤ Mq ∧ e.2.2.1 ≤ Mq ∧
        sXg Mq e ∈ segs.toList.toFinset ∧ sSg e ∈ segs.toList.toFinset := by
    intro e he
    have h2 := (STree.all_iff _ segs).mp hsall e (List.mem_toFinset.mp he)
    simp only [Bool.and_eq_true, Nat.ble_eq] at h2
    exact ⟨h2.1.1.1.1, h2.1.1.1.2, h2.1.1.2, List.mem_toFinset.mpr (STree.mem_sound _ _ h2.1.2),
      List.mem_toFinset.mpr (STree.mem_sound _ _ h2.2)⟩
  have rentry_ok : ∀ e ∈ rects.toFinset,
      e.1 ≤ e.2.2.1 ∧ e.2.1 ≤ e.2.2.2.1 ∧ e.2.2.1 ≤ Mq ∧ rXg Mq e ∈ rects.toFinset ∧
        rSg e ∈ rects.toFinset := by
    intro e he
    simp only [rectD4Check, List.all_eq_true] at hrsym
    have h2 := hrsym e (List.mem_toFinset.mp he)
    simp only [Bool.and_eq_true, Nat.ble_eq, List.contains_iff_mem] at h2
    exact ⟨h2.1.1.1.1, h2.1.1.1.2, h2.1.1.2, List.mem_toFinset.mpr h2.1.2,
      List.mem_toFinset.mpr h2.2⟩
  have hnonneg : M.Nonneg :=
    ⟨fun _ _ => by simp only [hMdef, mcoverP]; positivity,
     fun _ _ => by simp only [hMdef, mcoverP]; positivity,
     fun _ _ => by simp only [hMdef, mcoverP]; positivity⟩
  have hvolX : ∀ e ∈ rects.toFinset, volume (rectSet D (rXg Mq e)) = volume (rectSet D e) := by
    intro e he
    obtain ⟨h1, _, h3, _, _⟩ := rentry_ok e he
    rw [rectSet_rXg Mq D hD e h1 h3]
    exact (measurePreserving_reflX m).measure_preimage (measurableSet_rectSet D e).nullMeasurableSet
  have hvolS : ∀ e, volume (rectSet D (rSg e)) = volume (rectSet D e) := by
    intro e
    rw [rectSet_rSg]
    exact measurePreserving_swapXY.measure_preimage (measurableSet_rectSet D e).nullMeasurableSet
  -- D4 invariance of the measure
  have hinv : D4InvM m M.measure := by
    refine M.d4InvM m (fun e _ => measurableSet_rectSet D e) (fun e => (Mq - e.1, e.2.1, e.2.2))
      (fun e => (e.2.1, e.1, e.2.2)) (sXg Mq) sSg (rXg Mq) rSg ?_ ?_ ?_ ?_ ?_ ?_
    · intro e he
      obtain ⟨hx, hpX, _⟩ := pentry_ok e he
      refine ⟨hpX, ?_, rfl, ?_⟩
      · change ptR D (Mq - e.1, e.2.1, e.2.2) = reflX m (ptR D e)
        simp only [ptR, reflX, hm, Nat.cast_sub hx]
        ext
        · simp only; field_simp
        · simp
      · obtain ⟨a, b, c⟩ := e
        simp only at hx ⊢
        ext <;> simp; omega
    · intro e he
      obtain ⟨h, ha, hc, hsX, _⟩ := sentry_ok e he
      obtain ⟨h1, h2, h3⟩ := sXg_eq Mq D e h ha hc
      refine ⟨hsX, ?_, h1, h3⟩
      change ((sXg Mq e).2.2.2.2 : ℝ) / W = (e.2.2.2.2 : ℝ) / W
      rw [h2]
    · intro e he
      obtain ⟨h1, _, h3, hrX, _⟩ := rentry_ok e he
      refine ⟨hrX, ?_, ?_, rectSet_rXg Mq D hD e h1 h3⟩
      · change ((rXg Mq e).2.2.2.2 : ℝ) * (volume (rectSet D (rXg Mq e))).toReal / W =
          (e.2.2.2.2 : ℝ) * (volume (rectSet D e)).toReal / W
        rw [hvolX e he]; rfl
      · obtain ⟨a, b, c, d, w⟩ := e
        simp only [rXg] at h1 h3 ⊢
        ext <;> simp <;> omega
    · intro e he
      exact ⟨(pentry_ok e he).2.2, rfl, rfl, rfl⟩
    · intro e he
      obtain ⟨h, _, _, _, hsS⟩ := sentry_ok e he
      obtain ⟨h1, h2, h3⟩ := sSg_eq D e h
      refine ⟨hsS, ?_, h1, h3⟩
      change ((sSg e).2.2.2.2 : ℝ) / W = (e.2.2.2.2 : ℝ) / W
      rw [h2]
    · intro e he
      obtain ⟨_, _, _, _, hrS⟩ := rentry_ok e he
      refine ⟨hrS, ?_, rfl, rectSet_rSg D e⟩
      change ((rSg e).2.2.2.2 : ℝ) * (volume (rectSet D (rSg e))).toReal / W =
        (e.2.2.2.2 : ℝ) * (volume (rectSet D e)).toReal / W
      rw [hvolS e]; rfl
  -- the measure of a square is the mass
  have hmass : ∀ (Qs : Set (ℝ × ℝ)), MeasurableSet Qs →
      M.measure Qs = ENNReal.ofReal
        ((ptMass D pts.toList Qs + segMass D segs.toList Qs + rectMass D rects Qs) / W) := by
    intro Qs hQs
    rw [M.measure_apply hnonneg hQs]
    congr 1
    simp only [MixedCover.mass, hMdef, mcoverP, ptMass, segMass, rectMass, gw_areaFrac]
    rw [add_div, add_div, Finset.sum_div, Finset.sum_div, Finset.sum_div]
    congr 1
    · congr 1
      refine Finset.sum_congr rfl fun e _ => ?_
      ring
  -- the region statement, from the tree
  have hcover : ∀ (c : ℝ × ℝ) (θ : ℝ), sq c θ 1 ⊆ box m → 1 ≤ M.measure (sq c θ 1) := by
    refine d4_reduction_measure m M.measure hinv fun c θ h1 h2 hθ hsub0 => ?_
    obtain ⟨u, hu0, hu1, h45, rfl⟩ := exists_u_of_theta45 hθ
    have hsub := hsub0
    have hu : u ∈ Set.Icc (0 : ℝ) (1 / 2) := ⟨hu0, by linarith⟩
    rw [hmass _ (measurableSet_sq _ _ _), ← ENNReal.ofReal_one]
    apply ENNReal.ofReal_le_ofReal
    have hhalf : m / 2 ≤ (((Mq * S - Mq * S / 2 : ℕ) : ℝ)) / (D * S) := by
      have h2 : Mq * S ≤ 2 * (Mq * S - Mq * S / 2) := by omega
      have h2r : ((Mq * S : ℕ) : ℝ) ≤ 2 * ((Mq * S - Mq * S / 2 : ℕ) : ℝ) := by exact_mod_cast h2
      rw [hm, div_div, div_le_div_iff₀ (by positivity) (by positivity)]
      push_cast at h2r
      nlinarith
    have hU : ((0 : ℕ) : ℝ) / R ≤ u := by simpa using hu.1
    have hU1 : u ≤ (Um : ℝ) / R := by
      rw [le_div_iff₀ hRr]
      have : (R : ℝ) ≤ 2 * Um := by exact_mod_cast hUm
      nlinarith [hu.2]
    rw [le_div_iff₀ hWr, one_mul]
    rcases eq_or_lt_of_le hu0 with h0 | h0
    · subst h0
      exact hcov0 c 0 (by simpa using h1.1) (le_trans h1.2 hhalf) (by simpa using h2.1)
        (le_trans h2.2 hhalf) hU (by simp) hsub
    · exact hcov c u (by simpa using h1.1) (le_trans h1.2 hhalf) (by simpa using h2.1)
        (le_trans h2.2 hhalf) (by simpa using h0) hU1 h45 hsub
  -- the total
  have htot : M.measure (box m) < n := by
    have h1 : M.measure (box m) ≤ ENNReal.ofReal M.total :=
      (measure_mono (Set.subset_univ _)).trans (M.measure_univ_le hnonneg)
    have hp : ∑ e ∈ pts.toList.toFinset, (e.2.2 : ℝ) = pts.wsum := by
      have : ∑ e ∈ pts.toList.toFinset, e.2.2 = pts.wsum := by
        rw [List.sum_toFinset _ hnd, PTree.wsum_eq]
      rw [← this]; push_cast; rfl
    have hs : ∑ e ∈ segs.toList.toFinset, (e.2.2.2.2 : ℝ) = segs.wsum := by
      have : ∑ e ∈ segs.toList.toFinset, e.2.2.2.2 = segs.wsum := by
        rw [List.sum_toFinset _ hsnd, STree.wsum_eq]
      rw [← this]; push_cast; rfl
    have hr : ∑ e ∈ rects.toFinset, (e.2.2.2.2 : ℝ) * (volume (rectSet D e)).toReal =
        (rectsW rects : ℝ) / ((D : ℝ) * D) := by
      have e1 : ∑ e ∈ rects.toFinset, (e.2.2.2.2 : ℝ) * (volume (rectSet D e)).toReal =
          ∑ e ∈ rects.toFinset,
            ((e.2.2.2.2 * ((e.2.2.1 - e.1) * (e.2.2.2.1 - e.2.1)) : ℕ) : ℝ) / ((D : ℝ) * D) := by
        refine Finset.sum_congr rfl fun e he => ?_
        rw [volume_rectSet_toReal D hD e (rentry_ok e he).1 (rentry_ok e he).2.1, Nat.cast_mul
          e.2.2.2.2]
        ring
      rw [e1, ← Finset.sum_div, ← Nat.cast_sum, rectsW, List.sum_toFinset _ hrnd]
    have hsum : M.total = ((pts.wsum : ℝ) + segs.wsum + (rectsW rects : ℝ) / ((D : ℝ) * D)) / W := by
      simp only [MixedCover.total, hMdef, mcoverP]
      rw [← Finset.sum_div, ← Finset.sum_div, ← Finset.sum_div, hp, hs, hr]
      ring
    have h2 : ENNReal.ofReal M.total < n := by
      rw [hsum]
      have hDD : (0 : ℝ) < D * D := by positivity
      have hlt : ((pts.wsum : ℝ) + segs.wsum) * (D * D) + rectsW rects < n * W * (D * D) := by
        exact_mod_cast hn
      have e2 : (pts.wsum : ℝ) + segs.wsum + (rectsW rects : ℝ) / ((D : ℝ) * D) =
          (((pts.wsum : ℝ) + segs.wsum) * (D * D) + rectsW rects) / (D * D) := by
        field_simp
      have h3 : (pts.wsum : ℝ) + segs.wsum + (rectsW rects : ℝ) / ((D : ℝ) * D) < n * W := by
        rw [e2, div_lt_iff₀ hDD]; linarith
      have h4 : ((pts.wsum : ℝ) + segs.wsum + (rectsW rects : ℝ) / ((D : ℝ) * D)) / W < n := by
        rw [div_lt_iff₀ hWr]; exact h3
      have hn0 : (0 : ℝ) < n := lt_of_le_of_lt (by positivity) h4
      calc ENNReal.ofReal (((pts.wsum : ℝ) + segs.wsum + (rectsW rects : ℝ) / ((D : ℝ) * D)) / W)
          < ENNReal.ofReal n := (ENNReal.ofReal_lt_ofReal_iff hn0).mpr h4
        _ = n := ENNReal.ofReal_natCast n
    exact h1.trans_lt h2
  -- `s(n)`
  have hne : ({s | Packs n s} : Set ℝ).Nonempty := ⟨k, packs_grid k n hk⟩
  refine le_csInf hne fun s hs => ?_
  by_contra hlt
  exact not_packs_of_measure m M.measure hcover n htot (not_le.mp hlt) hs

end ZMTreeM

end SquarePacking
