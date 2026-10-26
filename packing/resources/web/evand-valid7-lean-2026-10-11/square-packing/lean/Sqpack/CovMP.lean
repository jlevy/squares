import Sqpack.CovM
import Sqpack.SquareArea

/-!
# `CovMP`: mixed covers with Lebesgue rectangles (points + segments + area)

The mixed covers of `certificates/s21/FORMAT.md` may carry mass uniformly by area on polygons
(`MixedCover.poly`).  The covers of `certificates/k2m3/` use one: the Lebesgue square
`[9/5, 26/5]²` with mass = area (density 1).  This file adds **axis-parallel rectangles of constant
density** to `CovM`.

* A rectangle entry `(X0, Y0, X1, Y1, ρ)` is the closed rectangle `[X0/D, X1/D] × [Y0/D, Y1/D]`
  carrying density `ρ/W` (mass per unit area).  The mass a closed square `Q` captures from it is
  `ρ · |Q ∩ rect| / W` (`rectMass`).
* `CovMP` — `CovM` with the rectangle mass added; `CovMP.split{X,Y,U}`, `CovMP.of_covM`.
* **`lebOk`, `CovMP.of_leb`** — the `LEB` leaf (Lemma U of `search/QUADRANT_EXACT.md` §4.2): if every
  admissible square of the box lies inside a rectangle of density `≥ 1`, it captures mass `≥ 1` (its
  area is `1`, `SqArea.volume_sq`).  The test is in natural numbers: the half-width `w(θ)/2` of a
  square at angle `θ = 2 arctan u` is bounded on the bin by `widN/widD`; a side of the rectangle on
  or beyond the container wall needs no test (the square is inside the container).
-/

open MeasureTheory Finset
open scoped ENNReal

namespace SquarePacking

namespace ZMTreeM

open BoxTree

/-- A rectangle entry `(X0, Y0, X1, Y1, ρ)`. -/
abbrev RectE := ℕ × ℕ × ℕ × ℕ × ℕ

/-- The closed rectangle of an entry, over `D`. -/
def rectSet (D : ℕ) (e : RectE) : Set (ℝ × ℝ) :=
  Set.Icc ((e.1 : ℝ) / D) ((e.2.2.1 : ℝ) / D) ×ˢ Set.Icc ((e.2.1 : ℝ) / D) ((e.2.2.2.1 : ℝ) / D)

/-- The rectangle mass a closed square captures (not yet divided by `W`). -/
noncomputable def rectMass (D : ℕ) (rects : List RectE) (Qs : Set (ℝ × ℝ)) : ℝ :=
  ∑ e ∈ rects.toFinset, (e.2.2.2.2 : ℝ) * (volume (Qs ∩ rectSet D e)).toReal

lemma rectMass_nonneg (D : ℕ) (rects : List RectE) (Qs : Set (ℝ × ℝ)) : 0 ≤ rectMass D rects Qs :=
  Finset.sum_nonneg fun _ _ => mul_nonneg (Nat.cast_nonneg _) ENNReal.toReal_nonneg

lemma ptMass_nonneg (D : ℕ) (pts : List (ℕ × ℕ × ℕ)) (Qs : Set (ℝ × ℝ)) : 0 ≤ ptMass D pts Qs :=
  Finset.sum_nonneg fun _ _ => Nat.cast_nonneg _

/-- **What a box certifies, with rectangles**: every closed unit square inside `[0, Mq/D]²` with
centre in `[x0,x1]×[y0,y1]` (over `Q = D·S`) and angle `2 arctan u`, `u ∈ [u0/R, u1/R]`, captures
point, segment and rectangle mass `≥ W`. -/
def CovMP (D S Mq R W : ℕ) (pts : List (ℕ × ℕ × ℕ)) (segs : List SegE) (rects : List RectE)
    (x0 x1 y0 y1 u0 u1 : ℕ) : Prop :=
  ∀ (c : ℝ × ℝ) (u : ℝ),
    (x0 : ℝ) / (D * S) ≤ c.1 → c.1 ≤ (x1 : ℝ) / (D * S) →
    (y0 : ℝ) / (D * S) ≤ c.2 → c.2 ≤ (y1 : ℝ) / (D * S) →
    (u0 : ℝ) / R ≤ u → u ≤ (u1 : ℝ) / R →
    sq c (2 * Real.arctan u) 1 ⊆ box ((Mq : ℝ) / D) →
    (W : ℝ) ≤ ptMass D pts (sq c (2 * Real.arctan u) 1) + segMass D segs (sq c (2 * Real.arctan u) 1)
      + rectMass D rects (sq c (2 * Real.arctan u) 1)

variable {D S Mq R W : ℕ} {pts : List (ℕ × ℕ × ℕ)} {segs : List SegE} {rects : List RectE}
  {x0 x1 y0 y1 u0 u1 : ℕ}

theorem CovMP.splitX (m : ℕ) (h1 : CovMP D S Mq R W pts segs rects x0 m y0 y1 u0 u1)
    (h2 : CovMP D S Mq R W pts segs rects m x1 y0 y1 u0 u1) :
    CovMP D S Mq R W pts segs rects x0 x1 y0 y1 u0 u1 := by
  intro c u hx0 hx1 hy0 hy1 hu0 hu1 hsub
  rcases le_total c.1 ((m : ℝ) / (D * S)) with h | h
  · exact h1 c u hx0 h hy0 hy1 hu0 hu1 hsub
  · exact h2 c u h hx1 hy0 hy1 hu0 hu1 hsub

theorem CovMP.splitY (m : ℕ) (h1 : CovMP D S Mq R W pts segs rects x0 x1 y0 m u0 u1)
    (h2 : CovMP D S Mq R W pts segs rects x0 x1 m y1 u0 u1) :
    CovMP D S Mq R W pts segs rects x0 x1 y0 y1 u0 u1 := by
  intro c u hx0 hx1 hy0 hy1 hu0 hu1 hsub
  rcases le_total c.2 ((m : ℝ) / (D * S)) with h | h
  · exact h1 c u hx0 hx1 hy0 h hu0 hu1 hsub
  · exact h2 c u hx0 hx1 h hy1 hu0 hu1 hsub

theorem CovMP.splitU (m : ℕ) (h1 : CovMP D S Mq R W pts segs rects x0 x1 y0 y1 u0 m)
    (h2 : CovMP D S Mq R W pts segs rects x0 x1 y0 y1 m u1) :
    CovMP D S Mq R W pts segs rects x0 x1 y0 y1 u0 u1 := by
  intro c u hx0 hx1 hy0 hy1 hu0 hu1 hsub
  rcases le_total u ((m : ℝ) / R) with h | h
  · exact h1 c u hx0 hx1 hy0 hy1 hu0 h hsub
  · exact h2 c u hx0 hx1 hy0 hy1 h hu1 hsub

/-- A points-and-segments certificate is a certificate with rectangles (their mass is `≥ 0`). -/
theorem CovMP.of_covM (h : CovM D S Mq R W pts segs x0 x1 y0 y1 u0 u1) :
    CovMP D S Mq R W pts segs rects x0 x1 y0 y1 u0 u1 := by
  intro c u hx0 hx1 hy0 hy1 hu0 hu1 hsub
  have := h c u hx0 hx1 hy0 hy1 hu0 hu1 hsub
  linarith [rectMass_nonneg D rects (sq c (2 * Real.arctan u) 1)]

/-! ## The `LEB` leaf (Lemma U) -/

/-- An upper bound of `w(θ) = cos θ + sin θ` on the bin `u ∈ [U0/R, U1/R] ⊆ [0, 1]`: the numerator
`1 − u² + 2u` is at most `1 − (U0/R)² + 2 U1/R`, the denominator `1 + u²` at least `1 + (U0/R)²`.
As the fraction `widN/widD` of naturals. -/
def widN (R U0 U1 : ℕ) : ℕ := R * R + 2 * U1 * R - U0 * U0
def widD (R U0 : ℕ) : ℕ := R * R + U0 * U0

lemma wid_le_widHat {R U0 U1 : ℕ} (hR : 0 < R) (hU1 : U1 ≤ R) {u : ℝ} (hu0 : (U0 : ℝ) / R ≤ u)
    (hu1 : u ≤ (U1 : ℝ) / R) :
    wid (2 * Real.arctan u) ≤ (widN R U0 U1 : ℝ) / widD R U0 := by
  have hRr : (0 : ℝ) < R := by exact_mod_cast hR
  have h0u : 0 ≤ u := le_trans (by positivity) hu0
  have hu0' : (U0 : ℝ) ≤ R * u := by rw [div_le_iff₀ hRr] at hu0; linarith
  have hu1' : R * u ≤ (U1 : ℝ) := by rw [le_div_iff₀ hRr] at hu1; linarith
  have hU1r : (U1 : ℝ) ≤ R := by exact_mod_cast hU1
  have hu1'' : u ≤ 1 := by nlinarith
  have hUU : U0 * U0 ≤ R * R + 2 * U1 * R := by
    have : (U0 : ℝ) ≤ U1 := le_trans hu0' hu1'
    have h2 : U0 ≤ U1 := by exact_mod_cast this
    nlinarith
  rw [wid_two_arctan h0u hu1'', widU, widN, widD, Nat.cast_sub hUU]
  push_cast
  have hD : (0 : ℝ) < (R : ℝ) * R + U0 * U0 := by positivity
  rw [div_le_div_iff₀ (by positivity) hD]
  -- `(1 − u² + 2u)(R² + U0²) ≤ (R² + 2 U1 R − U0²)(1 + u²)`
  have hU0 : (0 : ℝ) ≤ U0 := Nat.cast_nonneg _
  nlinarith [mul_nonneg hU0 hU0, mul_nonneg h0u h0u, mul_nonneg hU0 h0u,
    mul_le_mul_of_nonneg_left hu0' hU0, mul_le_mul_of_nonneg_left hu1' hRr.le,
    mul_le_mul_of_nonneg_left hu0' h0u, mul_nonneg (sub_nonneg.mpr hu1') (mul_nonneg h0u h0u),
    mul_nonneg (sub_nonneg.mpr hu1') hRr.le, mul_nonneg (sub_nonneg.mpr hu0') (sub_nonneg.mpr hu0')]

/-- The natural-number test of `LEB`: the bin is in `[0, 1]`, the density is `≥ W`, and the box of
centres widened by `widHat/2` on every side lies in the rectangle. -/
def lebOk (D S Mq R W x0 x1 y0 y1 u0 u1 : ℕ) (e : RectE) : Bool :=
  Nat.ble u1 R && Nat.ble u0 u1 && Nat.ble W e.2.2.2.2 &&
    (e.1 == 0 || Nat.ble (2 * e.1 * S * widD R u0 + D * S * widN R u0 u1) (2 * x0 * widD R u0)) &&
    (Nat.ble Mq e.2.2.1 ||
      Nat.ble (2 * x1 * widD R u0 + D * S * widN R u0 u1) (2 * e.2.2.1 * S * widD R u0)) &&
    (e.2.1 == 0 || Nat.ble (2 * e.2.1 * S * widD R u0 + D * S * widN R u0 u1) (2 * y0 * widD R u0)) &&
    (Nat.ble Mq e.2.2.2.1 ||
      Nat.ble (2 * y1 * widD R u0 + D * S * widN R u0 u1) (2 * e.2.2.2.1 * S * widD R u0))

lemma half_add_le {A x D S Wn Wd : ℕ} (hD : 0 < D) (hS : 0 < S) (hWd : 0 < Wd)
    (h : 2 * A * S * Wd + D * S * Wn ≤ 2 * x * Wd) :
    (A : ℝ) / D + (Wn : ℝ) / Wd / 2 ≤ (x : ℝ) / (D * S) := by
  have hDr : (0 : ℝ) < D := by exact_mod_cast hD
  have hSr : (0 : ℝ) < S := by exact_mod_cast hS
  have hWr : (0 : ℝ) < Wd := by exact_mod_cast hWd
  have hr : ((2 * A * S * Wd + D * S * Wn : ℕ) : ℝ) ≤ ((2 * x * Wd : ℕ) : ℝ) := by exact_mod_cast h
  push_cast at hr
  have e1 : (A : ℝ) / D + (Wn : ℝ) / Wd / 2 =
      (2 * A * S * Wd + D * S * Wn) / (2 * D * S * Wd) := by field_simp
  have e2 : (x : ℝ) / (D * S) = (2 * x * Wd) / (2 * D * S * Wd) := by field_simp
  rw [e1, e2]
  exact div_le_div_of_nonneg_right hr (by positivity)

lemma add_half_le {A x D S Wn Wd : ℕ} (hD : 0 < D) (hS : 0 < S) (hWd : 0 < Wd)
    (h : 2 * x * Wd + D * S * Wn ≤ 2 * A * S * Wd) :
    (x : ℝ) / (D * S) + (Wn : ℝ) / Wd / 2 ≤ (A : ℝ) / D := by
  have hDr : (0 : ℝ) < D := by exact_mod_cast hD
  have hSr : (0 : ℝ) < S := by exact_mod_cast hS
  have hWr : (0 : ℝ) < Wd := by exact_mod_cast hWd
  have hr : ((2 * x * Wd + D * S * Wn : ℕ) : ℝ) ≤ ((2 * A * S * Wd : ℕ) : ℝ) := by exact_mod_cast h
  push_cast at hr
  have e1 : (x : ℝ) / (D * S) + (Wn : ℝ) / Wd / 2 =
      (2 * x * Wd + D * S * Wn) / (2 * D * S * Wd) := by field_simp
  have e2 : (A : ℝ) / D = (2 * A * S * Wd) / (2 * D * S * Wd) := by field_simp
  rw [e1, e2]
  exact div_le_div_of_nonneg_right hr (by positivity)

/-- A closed unit square inside a rectangle of `rects` captures its density. -/
lemma rectMass_ge_of_subset {e : RectE} (he : e ∈ rects) {Qs : Set (ℝ × ℝ)} {c : ℝ × ℝ} {θ : ℝ}
    (hQ : Qs = sq c θ 1) (hsub : Qs ⊆ rectSet D e) :
    (e.2.2.2.2 : ℝ) ≤ rectMass D rects Qs := by
  have hvol : (volume (Qs ∩ rectSet D e)).toReal = 1 := by
    rw [Set.inter_eq_left.mpr hsub, hQ, SqArea.volume_sq]; simp
  have := Finset.single_le_sum (f := fun e => (e.2.2.2.2 : ℝ) * (volume (Qs ∩ rectSet D e)).toReal)
    (fun _ _ => mul_nonneg (Nat.cast_nonneg _) ENNReal.toReal_nonneg) (List.mem_toFinset.mpr he)
  simp only [hvol, mul_one] at this
  exact this

/-- **Soundness of the `LEB` leaf.** -/
theorem CovMP.of_leb (hD : 0 < D) (hS : 0 < S) (hR : 0 < R) {e : RectE} (he : e ∈ rects)
    (h : lebOk D S Mq R W x0 x1 y0 y1 u0 u1 e = true) :
    CovMP D S Mq R W pts segs rects x0 x1 y0 y1 u0 u1 := by
  simp only [lebOk, Bool.and_eq_true, Bool.or_eq_true, Nat.ble_eq, beq_iff_eq] at h
  obtain ⟨⟨⟨⟨⟨⟨hu1R, hu01⟩, hW⟩, hX0⟩, hX1⟩, hY0⟩, hY1⟩ := h
  intro c u hx0 hx1 hy0 hy1 hu0 hu1 hbox
  have hwd : 0 < widD R u0 := by unfold widD; have : 0 < R * R := Nat.mul_pos hR hR; omega
  have hw := wid_le_widHat hR hu1R hu0 hu1
  have hDr : (0 : ℝ) < D := by exact_mod_cast hD
  have hsub : sq c (2 * Real.arctan u) 1 ⊆ rectSet D e := by
    intro p hp
    obtain ⟨h1, h2⟩ := abs_sub_le_wid hp
    obtain ⟨b1, b2, b3, b4⟩ := hbox hp
    rw [abs_le] at h1 h2
    refine ⟨⟨?_, ?_⟩, ⟨?_, ?_⟩⟩
    · rcases hX0 with h | h
      · rw [h, Nat.cast_zero, zero_div]; exact b1
      · linarith [half_add_le hD hS hwd h]
    · rcases hX1 with h | h
      · have : (Mq : ℝ) / D ≤ (e.2.2.1 : ℝ) / D :=
          div_le_div_of_nonneg_right (by exact_mod_cast h) hDr.le
        linarith
      · linarith [add_half_le hD hS hwd h]
    · rcases hY0 with h | h
      · rw [h, Nat.cast_zero, zero_div]; exact b3
      · linarith [half_add_le hD hS hwd h]
    · rcases hY1 with h | h
      · have : (Mq : ℝ) / D ≤ (e.2.2.2.1 : ℝ) / D :=
          div_le_div_of_nonneg_right (by exact_mod_cast h) hDr.le
        linarith
      · linarith [add_half_le hD hS hwd h]
  have hr := rectMass_ge_of_subset (D := D) he rfl hsub
  have hWr : (W : ℝ) ≤ e.2.2.2.2 := by exact_mod_cast hW
  linarith [ptMass_nonneg D pts (sq c (2 * Real.arctan u) 1),
    segMass_nonneg D segs (sq c (2 * Real.arctan u) 1)]

/-! ## The D4 data check for rectangles, and the measure of the data -/

/-- The images of a rectangle entry under `x ↦ Mq − x` and `x ↔ y`. -/
def rXg (Mq : ℕ) (e : RectE) : RectE := (Mq - e.2.2.1, e.2.1, Mq - e.1, e.2.2.2.1, e.2.2.2.2)
def rSg (e : RectE) : RectE := (e.2.1, e.1, e.2.2.2.1, e.2.2.1, e.2.2.2.2)

/-- Every entry has `X0 ≤ X1 ≤ Mq`, `Y0 ≤ Y1`, and its two reflections are entries. -/
def rectD4Check (Mq : ℕ) (rects : List RectE) : Bool :=
  rects.all fun e => Nat.ble e.1 e.2.2.1 && Nat.ble e.2.1 e.2.2.2.1 && Nat.ble e.2.2.1 Mq &&
    rects.contains (rXg Mq e) && rects.contains (rSg e)

/-- `Σ ρ (X1 − X0)(Y1 − Y0)`: the rectangle mass, times `D²` (natural numbers). -/
def rectsW (rects : List RectE) : ℕ :=
  (rects.map fun e => e.2.2.2.2 * ((e.2.2.1 - e.1) * (e.2.2.2.1 - e.2.1))).sum

lemma measurableSet_rectSet (D : ℕ) (e : RectE) : MeasurableSet (rectSet D e) :=
  measurableSet_Icc.prod measurableSet_Icc

lemma volume_rectSet_ne_top (D : ℕ) (e : RectE) : volume (rectSet D e) ≠ ⊤ := by
  rw [rectSet, Measure.volume_eq_prod, Measure.prod_prod, Real.volume_Icc, Real.volume_Icc]
  exact ENNReal.mul_ne_top ENNReal.ofReal_ne_top ENNReal.ofReal_ne_top

lemma volume_rectSet_toReal (D : ℕ) (hD : 0 < D) (e : RectE) (h1 : e.1 ≤ e.2.2.1)
    (h2 : e.2.1 ≤ e.2.2.2.1) :
    (volume (rectSet D e)).toReal =
      (((e.2.2.1 - e.1) * (e.2.2.2.1 - e.2.1) : ℕ) : ℝ) / ((D : ℝ) * D) := by
  have hDr : (0 : ℝ) < D := by exact_mod_cast hD
  rw [rectSet, Measure.volume_eq_prod, Measure.prod_prod, Real.volume_Icc, Real.volume_Icc,
    ENNReal.toReal_mul, ENNReal.toReal_ofReal, ENNReal.toReal_ofReal, Nat.cast_mul,
    Nat.cast_sub h1, Nat.cast_sub h2]
  · field_simp
  · rw [sub_nonneg]; exact div_le_div_of_nonneg_right (by exact_mod_cast h2) hDr.le
  · rw [sub_nonneg]; exact div_le_div_of_nonneg_right (by exact_mod_cast h1) hDr.le

lemma rectSet_rXg (Mq D : ℕ) (hD : 0 < D) (e : RectE) (h1 : e.1 ≤ e.2.2.1) (h3 : e.2.2.1 ≤ Mq) :
    rectSet D (rXg Mq e) = reflX ((Mq : ℝ) / D) ⁻¹' rectSet D e := by
  have hDr : (0 : ℝ) < D := by exact_mod_cast hD
  ext p
  simp only [rectSet, rXg, reflX, Set.mem_preimage, Set.mem_prod, Set.mem_Icc,
    Nat.cast_sub h3, Nat.cast_sub (h1.trans h3), sub_div]
  constructor <;> rintro ⟨⟨a, b⟩, c, d⟩ <;> exact ⟨⟨by linarith, by linarith⟩, c, d⟩

lemma rectSet_rSg (D : ℕ) (e : RectE) : rectSet D (rSg e) = swapXY ⁻¹' rectSet D e := by
  ext p
  simp only [rectSet, rSg, swapXY, Set.mem_preimage, Set.mem_prod]
  exact and_comm

/-- The mixed cover of the data, with the rectangles as polygons: the polygon weight is
`ρ · area / W`, so that its mass in `Q` is `ρ |Q ∩ rect| / W`. -/
noncomputable def mcoverP (D W : ℕ) (pts : PTree) (segs : STree) (rects : List RectE) :
    MixedCover (ℕ × ℕ × ℕ) SegE RectE where
  pts := pts.toList.toFinset
  pt := ptR D
  pw := fun e => (e.2.2 : ℝ) / W
  segs := segs.toList.toFinset
  sa := segA D
  sb := segB D
  sw := fun e => (e.2.2.2.2 : ℝ) / W
  polys := rects.toFinset
  poly := rectSet D
  gw := fun e => (e.2.2.2.2 : ℝ) * (volume (rectSet D e)).toReal / W

lemma gw_areaFrac (D W : ℕ) (e : RectE) (Qs : Set (ℝ × ℝ)) :
    (e.2.2.2.2 : ℝ) * (volume (rectSet D e)).toReal / W * areaFrac (rectSet D e) Qs =
      (e.2.2.2.2 : ℝ) * (volume (Qs ∩ rectSet D e)).toReal / W := by
  rw [areaFrac_eq]
  by_cases h0 : (volume (rectSet D e)).toReal = 0
  · have : (volume (Qs ∩ rectSet D e)).toReal = 0 := by
      rcases (ENNReal.toReal_eq_zero_iff _).mp h0 with h | h
      · rw [measure_mono_null Set.inter_subset_right h]; simp
      · exact absurd h (volume_rectSet_ne_top D e)
    rw [h0, this]; simp
  · field_simp

/-- **The generic lower bound from a mixed cover with Lebesgue rectangles.** -/
theorem le_minSide_mixedP (D S Mq R Um W : ℕ) (pts : PTree) (segs : STree) (rects : List RectE)
    (hD : 0 < D) (hS : 0 < S) (hR : 0 < R) (hUm : R ≤ 2 * Um) (hnd : pts.toList.Nodup)
    (hrnd : rects.Nodup) (hsym : d4Check Mq pts = true) (hssym : segD4Check Mq segs = true)
    (hrsym : rectD4Check Mq rects = true)
    (hcov : CovMP D S Mq R W pts.toList segs.toList rects 0 (Mq * S - Mq * S / 2) 0
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
    refine d4_reduction_measure_u m M.measure hinv fun c u h1 h2 hu hsub => ?_
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
    have hc := hcov c u (by simpa using h1.1) (le_trans h1.2 hhalf) (by simpa using h2.1)
      (le_trans h2.2 hhalf) hU hU1 hsub
    rw [le_div_iff₀ hWr, one_mul]
    exact hc
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

/-! ## Boxes open at the lower end of the angle bin -/

/-- `CovMP` for the angles `u ∈ (u0/R, u1/R]` (open at `u0`; Lemma E's leaves). -/
def CovMPo (D S Mq R W : ℕ) (pts : List (ℕ × ℕ × ℕ)) (segs : List SegE) (rects : List RectE)
    (x0 x1 y0 y1 u0 u1 : ℕ) : Prop :=
  ∀ (c : ℝ × ℝ) (u : ℝ),
    (x0 : ℝ) / (D * S) ≤ c.1 → c.1 ≤ (x1 : ℝ) / (D * S) →
    (y0 : ℝ) / (D * S) ≤ c.2 → c.2 ≤ (y1 : ℝ) / (D * S) →
    (u0 : ℝ) / R < u → u ≤ (u1 : ℝ) / R →
    sq c (2 * Real.arctan u) 1 ⊆ box ((Mq : ℝ) / D) →
    (W : ℝ) ≤ ptMass D pts (sq c (2 * Real.arctan u) 1) + segMass D segs (sq c (2 * Real.arctan u) 1)
      + rectMass D rects (sq c (2 * Real.arctan u) 1)

theorem CovMPo.of_covMP (h : CovMP D S Mq R W pts segs rects x0 x1 y0 y1 u0 u1) :
    CovMPo D S Mq R W pts segs rects x0 x1 y0 y1 u0 u1 :=
  fun c u hx0 hx1 hy0 hy1 hu0 hu1 hsub => h c u hx0 hx1 hy0 hy1 hu0.le hu1 hsub

theorem CovMPo.splitX (m : ℕ) (h1 : CovMPo D S Mq R W pts segs rects x0 m y0 y1 u0 u1)
    (h2 : CovMPo D S Mq R W pts segs rects m x1 y0 y1 u0 u1) :
    CovMPo D S Mq R W pts segs rects x0 x1 y0 y1 u0 u1 := by
  intro c u hx0 hx1 hy0 hy1 hu0 hu1 hsub
  rcases le_total c.1 ((m : ℝ) / (D * S)) with h | h
  · exact h1 c u hx0 h hy0 hy1 hu0 hu1 hsub
  · exact h2 c u h hx1 hy0 hy1 hu0 hu1 hsub

theorem CovMPo.splitY (m : ℕ) (h1 : CovMPo D S Mq R W pts segs rects x0 x1 y0 m u0 u1)
    (h2 : CovMPo D S Mq R W pts segs rects x0 x1 m y1 u0 u1) :
    CovMPo D S Mq R W pts segs rects x0 x1 y0 y1 u0 u1 := by
  intro c u hx0 hx1 hy0 hy1 hu0 hu1 hsub
  rcases le_total c.2 ((m : ℝ) / (D * S)) with h | h
  · exact h1 c u hx0 hx1 hy0 h hu0 hu1 hsub
  · exact h2 c u hx0 hx1 h hy1 hu0 hu1 hsub

theorem CovMPo.splitU (m : ℕ) (h1 : CovMPo D S Mq R W pts segs rects x0 x1 y0 y1 u0 m)
    (h2 : CovMPo D S Mq R W pts segs rects x0 x1 y0 y1 m u1) :
    CovMPo D S Mq R W pts segs rects x0 x1 y0 y1 u0 u1 := by
  intro c u hx0 hx1 hy0 hy1 hu0 hu1 hsub
  rcases le_or_gt u ((m : ℝ) / R) with h | h
  · exact h1 c u hx0 hx1 hy0 hy1 hu0 h hsub
  · exact h2 c u hx0 hx1 hy0 hy1 h hu1 hsub

/-- The closed face `u = u0/R` and the open rest give the closed bin. -/
theorem CovMP.of_face (h0 : CovMP D S Mq R W pts segs rects x0 x1 y0 y1 u0 u0)
    (h1 : CovMPo D S Mq R W pts segs rects x0 x1 y0 y1 u0 u1) :
    CovMP D S Mq R W pts segs rects x0 x1 y0 y1 u0 u1 := by
  intro c u hx0 hx1 hy0 hy1 hu0 hu1 hsub
  rcases eq_or_lt_of_le hu0 with h | h
  · exact h0 c u hx0 hx1 hy0 hy1 hu0 h.symm.le hsub
  · exact h1 c u hx0 hx1 hy0 hy1 h hu1 hsub

end ZMTreeM

end SquarePacking
