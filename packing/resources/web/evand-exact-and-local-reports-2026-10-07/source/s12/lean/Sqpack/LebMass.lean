import Sqpack.ValidSplit

/-!
# Uniform-area (Lebesgue) mass: Lemma U (LEB) and Lemma K (CAP) as leaf tests

`search/QUADRANT_EXACT.md` §4.2; the tests as run: `search/qx2_zm.py` `cert_leb`, `cert_cap`.
Design: `notes/lean-leb-mass.md`.

* `CovT m μ x0 x1 y0 y1 u0 u1` — what a pose box certifies for a measure `μ`, in exactly the pose region
  of `ValidTilt` (`ValidSplit.lean`): admissible squares, `θ = 2 arctan u`, `0 < u`, `u² + 2u ≤ 1`.
  Gluing `CovT.splitX/Y/U`; root `validTilt_of_covT`.
* `PBox` — a leaf box with rational corners; `whi` — the upper bound `ŵ` of `w(θ) = cos θ + sin θ`
  on the bin (`widU_le_whi`).
* `volume_sq` — a closed unit square at any angle has area `1`.
* **Lemma U** (`leb_sound`): if every square of the box lies in `[a,b]²` and `μ ≥ λ` on `[a,b]²`, then
  `μ(Q) ≥ 1`.  `gridCover_vol_le`: a grid cover is `≥ λ` on its Lebesgue square.
* **Lemma K** (`cap_sound`): see §4.
-/

open MeasureTheory Finset
open scoped ENNReal

namespace SquarePacking
namespace LebMass

open ValidSplit
open Bentz (SegIx)

/-! ## 1.  The box predicate -/

/-- **What a pose box certifies** (the tilted run's region): every admissible closed unit square
with centre in `[x0,x1] × [y0,y1]` and angle `θ = 2 arctan u`, `u ∈ [u0,u1]`, `u > 0`,
`u² + 2u ≤ 1`, has `μ`-mass `≥ 1`. -/
def CovT (m : ℝ) (μ : Measure (ℝ × ℝ)) (x0 x1 y0 y1 u0 u1 : ℝ) : Prop :=
  ∀ (c : ℝ × ℝ) (u : ℝ), x0 ≤ c.1 → c.1 ≤ x1 → y0 ≤ c.2 → c.2 ≤ y1 → u0 ≤ u → u ≤ u1 →
    0 < u → u ^ 2 + 2 * u ≤ 1 → sq c (2 * Real.arctan u) 1 ⊆ box m →
      1 ≤ μ (sq c (2 * Real.arctan u) 1)

variable {m : ℝ} {μ : Measure (ℝ × ℝ)} {x0 x1 y0 y1 u0 u1 : ℝ}

theorem CovT.splitX (t : ℝ) (h1 : CovT m μ x0 t y0 y1 u0 u1) (h2 : CovT m μ t x1 y0 y1 u0 u1) :
    CovT m μ x0 x1 y0 y1 u0 u1 := by
  intro c u hx0 hx1 hy0 hy1 hu0 hu1 hu hu' hsub
  rcases le_total c.1 t with h | h
  · exact h1 c u hx0 h hy0 hy1 hu0 hu1 hu hu' hsub
  · exact h2 c u h hx1 hy0 hy1 hu0 hu1 hu hu' hsub

theorem CovT.splitY (t : ℝ) (h1 : CovT m μ x0 x1 y0 t u0 u1) (h2 : CovT m μ x0 x1 t y1 u0 u1) :
    CovT m μ x0 x1 y0 y1 u0 u1 := by
  intro c u hx0 hx1 hy0 hy1 hu0 hu1 hu hu' hsub
  rcases le_total c.2 t with h | h
  · exact h1 c u hx0 hx1 hy0 h hu0 hu1 hu hu' hsub
  · exact h2 c u hx0 hx1 h hy1 hu0 hu1 hu hu' hsub

theorem CovT.splitU (t : ℝ) (h1 : CovT m μ x0 x1 y0 y1 u0 t) (h2 : CovT m μ x0 x1 y0 y1 t u1) :
    CovT m μ x0 x1 y0 y1 u0 u1 := by
  intro c u hx0 hx1 hy0 hy1 hu0 hu1 hu hu' hsub
  rcases le_total u t with h | h
  · exact h1 c u hx0 hx1 hy0 hy1 hu0 h hu hu' hsub
  · exact h2 c u hx0 hx1 hy0 hy1 h hu1 hu hu' hsub

/-- **The root.**  The D4 root box `[0, m/2]² × [0, 1/2]` is `ValidTilt` (`u² + 2u ≤ 1 ⇒ u ≤ 1/2`). -/
theorem validTilt_of_covT (h : CovT m μ 0 (m / 2) 0 (m / 2) 0 (1 / 2)) : ValidTilt m μ := by
  intro c u hc1 hc2 hu hu' hsub
  exact h c u hc1.1 hc1.2 hc2.1 hc2.2 hu.le (by nlinarith) hu hu' hsub

/-! ## 2.  Rational leaf boxes and the width bound `ŵ` -/

/-- A leaf box `[x0,x1] × [y0,y1] × [u0,u1]` with rational corners. -/
structure PBox where
  x0 : ℚ
  x1 : ℚ
  y0 : ℚ
  y1 : ℚ
  u0 : ℚ
  u1 : ℚ

/-- `CovT` of a rational box. -/
def PBox.Cov (m : ℝ) (μ : Measure (ℝ × ℝ)) (B : PBox) : Prop :=
  CovT m μ B.x0 B.x1 B.y0 B.y1 B.u0 B.u1

/-- `ŵ`: an upper bound of `w = cos θ + sin θ` for `0 < u ≤ u1`, `u² + 2u ≤ 1` (zeromargin's
`bin_data` `whi`: `w(u1)` below 45°, else `14143/10000 > √2`). -/
def whi (u1 : ℚ) : ℚ :=
  if u1 * u1 + 2 * u1 ≤ 1 then (1 - u1 * u1 + 2 * u1) / (1 + u1 * u1) else 14143 / 10000

lemma widU_le_whi {u : ℝ} {u1 : ℚ} (_hu : 0 ≤ u) (hu1 : u ≤ u1) (hu' : u ^ 2 + 2 * u ≤ 1) :
    widU u ≤ (whi u1 : ℝ) := by
  have hN : (0 : ℝ) < 1 + u ^ 2 := by positivity
  unfold whi
  split_ifs with h
  · have h' : (u1 : ℝ) * u1 + 2 * u1 ≤ 1 := by exact_mod_cast h
    push_cast
    have hN1 : (0 : ℝ) < 1 + (u1 : ℝ) * u1 := by nlinarith
    rw [widU, div_le_div_iff₀ hN hN1]
    nlinarith [mul_nonneg (sub_nonneg.mpr hu1)
      (show (0 : ℝ) ≤ 1 - u - u1 - u * u1 by nlinarith)]
  · push_cast
    rw [widU, div_le_iff₀ hN]
    nlinarith [sq_nonneg (u - 1), sq_nonneg (1 - u ^ 2 + 2 * u - 14143 / 10000 * (1 + u ^ 2)),
      sq_nonneg (u ^ 2 - 2 * u - 1)]

/-- Every point of the square is within `ŵ/2` of the centre in each axis. -/
lemma abs_sub_le_whi {c p : ℝ × ℝ} {u : ℝ} {u1 : ℚ} (hu : 0 ≤ u) (hu1 : u ≤ u1)
    (hu' : u ^ 2 + 2 * u ≤ 1) (hp : p ∈ sq c (2 * Real.arctan u) 1) :
    |p.1 - c.1| ≤ (whi u1 : ℝ) / 2 ∧ |p.2 - c.2| ≤ (whi u1 : ℝ) / 2 := by
  have hw := widU_le_whi hu hu1 hu'
  rw [← wid_two_arctan hu (by nlinarith)] at hw
  obtain ⟨h1, h2⟩ := abs_sub_le_wid hp
  exact ⟨by linarith, by linarith⟩

/-! ## 3.  Area of a unit square; Lemma U -/

/-- The linear part of `coord c θ`. -/
noncomputable def rotL (θ : ℝ) : (ℝ × ℝ) →ₗ[ℝ] (ℝ × ℝ) :=
  Matrix.toLin (Module.Basis.finTwoProd ℝ) (Module.Basis.finTwoProd ℝ)
    !![Real.cos θ, Real.sin θ; -Real.sin θ, Real.cos θ]

lemma rotL_apply (θ : ℝ) (p : ℝ × ℝ) :
    rotL θ p = (p.1 * Real.cos θ + p.2 * Real.sin θ, -p.1 * Real.sin θ + p.2 * Real.cos θ) := by
  rw [rotL, Matrix.toLin_apply]
  simp [Matrix.mulVec, dotProduct, Fin.sum_univ_two]
  constructor <;> ring

lemma rotL_det (θ : ℝ) : LinearMap.det (rotL θ) = 1 := by
  rw [rotL, LinearMap.det_toLin, Matrix.det_fin_two_of]
  nlinarith [Real.cos_sq_add_sin_sq θ]

/-- **A closed unit square has area `1`**, at any angle. -/
theorem volume_sq (c : ℝ × ℝ) (θ : ℝ) : volume (sq c θ 1) = 1 := by
  have e : sq c θ 1 = (fun p => p + (-c)) ⁻¹' (rotL θ ⁻¹'
      (Set.Icc (-(1/2 : ℝ)) (1/2) ×ˢ Set.Icc (-(1/2 : ℝ)) (1/2))) := by
    ext p
    simp only [sq, coord, Set.mem_ofPred_eq, Set.mem_preimage, rotL_apply, Set.mem_prod,
      Set.mem_Icc, abs_le, Prod.fst_add, Prod.snd_add, Prod.fst_neg, Prod.snd_neg]
    constructor <;> rintro ⟨⟨h1, h2⟩, h3, h4⟩ <;> refine ⟨⟨?_, ?_⟩, ?_, ?_⟩ <;> linarith
  rw [e, measure_preimage_add_right,
    Measure.addHaar_preimage_linearMap _ (by rw [rotL_det]; norm_num), rotL_det,
    Measure.volume_eq_prod, Measure.prod_prod, Real.volume_Icc]
  norm_num

/-- The Lebesgue square `[a,b]²`. -/
def lsq (a b : ℝ) : Set (ℝ × ℝ) := Set.Icc a b ×ˢ Set.Icc a b

/-- The LEB test: every square of the box lies in `[a,b]²` (`cert_leb`). -/
def lebOK (a b : ℚ) (B : PBox) : Bool :=
  decide (a + whi B.u1 / 2 ≤ B.x0 ∧ a + whi B.u1 / 2 ≤ B.y0 ∧ B.x1 + whi B.u1 / 2 ≤ b ∧
    B.y1 + whi B.u1 / 2 ≤ b)

/-- **Lemma U.**  If `μ ≥ λ` on `[a,b]²` and the LEB test passes, every square of the box has
`μ`-mass `≥ λ(Q) = 1`. -/
theorem leb_sound {a b : ℚ} (hμ : ∀ S, MeasurableSet S → volume (S ∩ lsq a b) ≤ μ S)
    {B : PBox} (h : lebOK a b B = true) : B.Cov m μ := by
  simp only [lebOK, decide_eq_true_eq] at h
  obtain ⟨h1, h2, h3, h4⟩ := h
  have h1' : (a : ℝ) + (whi B.u1 : ℝ) / 2 ≤ B.x0 := by exact_mod_cast h1
  have h2' : (a : ℝ) + (whi B.u1 : ℝ) / 2 ≤ B.y0 := by exact_mod_cast h2
  have h3' : (B.x1 : ℝ) + (whi B.u1 : ℝ) / 2 ≤ b := by exact_mod_cast h3
  have h4' : (B.y1 : ℝ) + (whi B.u1 : ℝ) / 2 ≤ b := by exact_mod_cast h4
  intro c u hx0 hx1 hy0 hy1 _ hu1 hu hu' _
  have hsub : sq c (2 * Real.arctan u) 1 ⊆ lsq a b := by
    intro p hp
    obtain ⟨e1, e2⟩ := abs_sub_le_whi hu.le hu1 hu' hp
    rw [abs_le] at e1 e2
    exact ⟨⟨by linarith [e1.1], by linarith [e1.2]⟩, by linarith [e2.1], by linarith [e2.2]⟩
  calc (1 : ℝ≥0∞) = volume (sq c (2 * Real.arctan u) 1 ∩ lsq a b) := by
        rw [Set.inter_eq_left.mpr hsub, volume_sq]
    _ ≤ μ _ := hμ _ (measurableSet_sq _ _ _)

/-- The Lebesgue square of a grid cover. -/
lemma lebSq_eq (A K : ℕ) :
    BentzFam.lebSq A K = lsq (((A : ℚ) / 5 : ℚ) : ℝ) (((K : ℚ) - A / 5 : ℚ) : ℝ) := by
  simp only [BentzFam.lebSq, lsq]; push_cast; rfl

lemma volume_lebSq (A K : ℕ) (hA : 2 * A ≤ 5 * K) :
    volume (BentzFam.lebSq A K) = ENNReal.ofReal (((K : ℝ) - 2 * A / 5) ^ 2) := by
  have hA' : (2 * A : ℝ) ≤ 5 * K := by exact_mod_cast hA
  rw [BentzFam.lebSq, Measure.volume_eq_prod, Measure.prod_prod, Real.volume_Icc,
    ← ENNReal.ofReal_mul (by linarith), pow_two]
  congr 1; ring

/-- **A grid cover is at least Lebesgue measure on its Lebesgue square.** -/
theorem gridCover_vol_le {K A den : ℕ} {w : SegIx → ℕ} (hA : 2 * A < 5 * K) (S : Set (ℝ × ℝ))
    (hS : MeasurableSet S) :
    volume (S ∩ BentzFam.lebSq A K) ≤ (gridCover K A den w).measure S := by
  have hA' : (2 * A : ℝ) < 5 * K := by exact_mod_cast hA
  have hv := volume_lebSq A K hA.le
  have h0 : volume (BentzFam.lebSq A K) ≠ 0 := by
    rw [hv]; simp only [ne_eq, ENNReal.ofReal_eq_zero, not_le]; nlinarith
  have htop : volume (BentzFam.lebSq A K) ≠ ⊤ := by rw [hv]; exact ENNReal.ofReal_ne_top
  rw [MixedCover.measure_apply']
  refine le_trans ?_ le_add_self
  simp only [gridCover, Finset.univ_unique, Finset.sum_singleton]
  rw [areaMeasure_apply _ hS, ← hv, ← mul_assoc, ENNReal.mul_inv_cancel h0 htop, one_mul]

/-- Lemma U for a grid cover, with `a = A/5`, `b = K − A/5`. -/
theorem leb_sound_grid {K A den : ℕ} {w : SegIx → ℕ} (hA : 2 * A < 5 * K) {B : PBox}
    (h : lebOK ((A : ℚ) / 5) ((K : ℚ) - A / 5) B = true) :
    B.Cov m (gridCover K A den w).measure :=
  leb_sound (fun S hS => by rw [← lebSq_eq]; exact gridCover_vol_le hA S hS) h

/-! ## 4.  Lemma K: the width lemma (slices of a centrally symmetric convex body) -/

/-- The horizontal slice `{x | (x, y) ∈ Q}`. -/
def hsl (Q : Set (ℝ × ℝ)) (y : ℝ) : Set ℝ := {x | (x, y) ∈ Q}

/-- **Width lemma.**  For a compact convex set symmetric about `c`, slices below the centre grow
towards it: `y ≤ a ≤ c.2 ⇒ λ(Q_y) ≤ λ(Q_a)`. -/
theorem vol_hsl_le {Q : Set (ℝ × ℝ)} {c : ℝ × ℝ} (hconv : Convex ℝ Q) (hcomp : IsCompact Q)
    (hsym : ∀ p ∈ Q, (2 * c.1 - p.1, 2 * c.2 - p.2) ∈ Q) {y a : ℝ} (hya : y ≤ a) (hac : a ≤ c.2) :
    volume (hsl Q y) ≤ volume (hsl Q a) := by
  rcases eq_or_lt_of_le hya with rfl | hya'
  · exact le_rfl
  rcases (hsl Q y).eq_empty_or_nonempty with he | hne
  · rw [he, measure_empty]; exact zero_le
  have hcl : IsClosed (hsl Q y) :=
    hcomp.isClosed.preimage (continuous_id.prodMk continuous_const)
  have hbd : Bornology.IsBounded (hsl Q y) := by
    obtain ⟨R, hR⟩ := hcomp.isBounded.subset_closedBall (0 : ℝ × ℝ)
    refine (Metric.isBounded_closedBall (x := (0 : ℝ)) (r := R)).subset fun x hx => ?_
    have := hR hx
    simp only [Metric.mem_closedBall, dist_zero_right] at this ⊢
    exact le_trans (by simp [Prod.norm_def]) this
  have hK : IsCompact (hsl Q y) := Metric.isCompact_of_isClosed_isBounded hcl hbd
  set l := sInf (hsl Q y)
  set r := sSup (hsl Q y)
  have hl : (l, y) ∈ Q := hK.sInf_mem hne
  have hr : (r, y) ∈ Q := hK.sSup_mem hne
  have hsub : hsl Q y ⊆ Set.Icc l r := fun x hx =>
    ⟨csInf_le hK.bddBelow hx, le_csSup hK.bddAbove hx⟩
  have hlr : l ≤ r := (hsub hne.some_mem).1.trans (hsub hne.some_mem).2
  -- the convex weight `λ` with `λ y + (1 − λ)(2 c₂ − y) = a`
  have hcy : y < c.2 := lt_of_lt_of_le hya' hac
  set t : ℝ := (a - y) / (2 * (c.2 - y))
  have ht0 : 0 ≤ t := div_nonneg (by linarith) (by linarith)
  have ht1 : t ≤ 1 := by rw [div_le_one (by linarith)]; linarith
  have hr' := hsym _ hr
  have hl' := hsym _ hl
  have hyt : (1 - t) * y + t * (2 * c.2 - y) = a := by
    have : t * (2 * (c.2 - y)) = a - y := div_mul_cancel₀ _ (by linarith)
    linear_combination this
  have hP : ((1 - t) * l + t * (2 * c.1 - r), a) ∈ Q := by
    have := hconv hl hr' (by linarith : (0:ℝ) ≤ 1 - t) ht0 (by ring)
    simp only [Prod.smul_mk, Prod.mk_add_mk, smul_eq_mul] at this
    rwa [hyt] at this
  have hR : ((1 - t) * r + t * (2 * c.1 - l), a) ∈ Q := by
    have := hconv hr hl' (by linarith : (0:ℝ) ≤ 1 - t) ht0 (by ring)
    simp only [Prod.smul_mk, Prod.mk_add_mk, smul_eq_mul] at this
    rwa [hyt] at this
  have hseg : Set.Icc ((1 - t) * l + t * (2 * c.1 - r)) ((1 - t) * r + t * (2 * c.1 - l))
      ⊆ hsl Q a := by
    intro x hx
    set x1 := (1 - t) * l + t * (2 * c.1 - r)
    set x2 := (1 - t) * r + t * (2 * c.1 - l)
    rcases eq_or_lt_of_le (hx.1.trans hx.2) with he | hlt
    · have : x = x1 := le_antisymm (he ▸ hx.2) hx.1
      rw [this]; exact hP
    · set s := (x - x1) / (x2 - x1)
      have hs0 : 0 ≤ s := div_nonneg (by linarith [hx.1]) (by linarith)
      have hs1 : s ≤ 1 := by rw [div_le_one (by linarith)]; linarith [hx.2]
      have := hconv hP hR (by linarith : (0:ℝ) ≤ 1 - s) hs0 (by ring)
      simp only [Prod.smul_mk, Prod.mk_add_mk, smul_eq_mul] at this
      have e1 : (1 - s) * x1 + s * x2 = x := by simp only [s]; field_simp; ring
      have e2 : (1 - s) * a + s * a = a := by ring
      rw [e1, e2] at this
      exact this
  calc volume (hsl Q y) ≤ volume (Set.Icc l r) := measure_mono hsub
    _ = ENNReal.ofReal (r - l) := Real.volume_Icc
    _ = volume (Set.Icc ((1 - t) * l + t * (2 * c.1 - r)) ((1 - t) * r + t * (2 * c.1 - l))) := by
        rw [Real.volume_Icc]; congr 1; ring
    _ ≤ volume (hsl Q a) := measure_mono hseg

/-- **The cap below a line** (Fubini): if every slice below `a` is at most the slice at `a`, and
`Q ⊆ {y ≥ a − d}`, then `λ(Q ∩ {y < a}) ≤ d · λ₁(Q_a)`. -/
theorem vol_below_le {Q : Set (ℝ × ℝ)} (hQ : MeasurableSet Q) {a d : ℝ}
    (hb : ∀ p ∈ Q, a - d ≤ p.2) (hmono : ∀ y ≤ a, volume (hsl Q y) ≤ volume (hsl Q a)) :
    volume (Q ∩ {p | p.2 < a}) ≤ ENNReal.ofReal d * volume (hsl Q a) := by
  have hm : MeasurableSet (Q ∩ {p : ℝ × ℝ | p.2 < a}) :=
    hQ.inter (measurableSet_lt measurable_snd measurable_const)
  rw [Measure.volume_eq_prod, Measure.prod_apply_symm hm]
  calc ∫⁻ y, volume ((fun x => (x, y)) ⁻¹' (Q ∩ {p : ℝ × ℝ | p.2 < a}))
      ≤ ∫⁻ y, (Set.Ico (a - d) a).indicator (fun _ => volume (hsl Q a)) y := by
        refine lintegral_mono fun y => ?_
        by_cases hy : y ∈ Set.Ico (a - d) a
        · rw [Set.indicator_of_mem hy]
          refine le_trans (measure_mono fun x hx => hx.1) (hmono y hy.2.le)
        · rw [Set.indicator_of_notMem hy]
          have : (fun x => (x, y)) ⁻¹' (Q ∩ {p : ℝ × ℝ | p.2 < a}) = ∅ := by
            ext x
            simp only [Set.mem_preimage, Set.mem_inter_iff, Set.mem_ofPred_eq,
              Set.mem_empty_iff_false, iff_false, not_and]
            intro hx hlt
            exact hy ⟨hb _ hx, hlt⟩
          rw [this, measure_empty]
    _ = volume (hsl Q a) * volume (Set.Ico (a - d) a) := lintegral_indicator_const measurableSet_Ico _
    _ = ENNReal.ofReal d * volume (hsl Q a) := by
        rw [Real.volume_Ico, mul_comm]; congr 2; ring

/-! ### The unit square is compact, convex and symmetric -/

lemma convex_sq (c : ℝ × ℝ) (θ : ℝ) : Convex ℝ (sq c θ 1) := by
  intro p hp q hq s t hs ht hst
  obtain ⟨hp1, hp2⟩ := hp
  obtain ⟨hq1, hq2⟩ := hq
  have e1 : (coord c θ (s • p + t • q)).1 = s * (coord c θ p).1 + t * (coord c θ q).1 := by
    simp only [coord, Prod.smul_fst, Prod.smul_snd, Prod.fst_add, Prod.snd_add, smul_eq_mul]
    linear_combination (c.1 * Real.cos θ + c.2 * Real.sin θ) * hst
  have e2 : (coord c θ (s • p + t • q)).2 = s * (coord c θ p).2 + t * (coord c θ q).2 := by
    simp only [coord, Prod.smul_fst, Prod.smul_snd, Prod.fst_add, Prod.snd_add, smul_eq_mul]
    linear_combination (c.2 * Real.cos θ - c.1 * Real.sin θ) * hst
  rw [abs_le] at hp1 hp2 hq1 hq2
  refine ⟨?_, ?_⟩
  · rw [e1, abs_le]; constructor <;> nlinarith
  · rw [e2, abs_le]; constructor <;> nlinarith

lemma sq_sym (c : ℝ × ℝ) (θ : ℝ) (p : ℝ × ℝ) (hp : p ∈ sq c θ 1) :
    (2 * c.1 - p.1, 2 * c.2 - p.2) ∈ sq c θ 1 := by
  obtain ⟨h1, h2⟩ := hp
  refine ⟨?_, ?_⟩
  · have : (coord c θ (2 * c.1 - p.1, 2 * c.2 - p.2)).1 = -(coord c θ p).1 := by
      simp only [coord]; ring
    rw [this, abs_neg]; exact h1
  · have : (coord c θ (2 * c.1 - p.1, 2 * c.2 - p.2)).2 = -(coord c θ p).2 := by
      simp only [coord]; ring
    rw [this, abs_neg]; exact h2

lemma isCompact_sq (c : ℝ × ℝ) (θ : ℝ) : IsCompact (sq c θ 1) := by
  refine Metric.isCompact_of_isClosed_isBounded (isClosed_sq c θ 1) ?_
  refine (Metric.isBounded_closedBall (x := c) (r := 2)).subset fun p hp => ?_
  obtain ⟨h1, h2⟩ := abs_sub_le_wid hp
  have hw : wid θ ≤ 2 := by
    simp only [wid]; linarith [Real.abs_cos_le_one θ, Real.abs_sin_le_one θ]
  rw [Metric.mem_closedBall, Prod.dist_eq, Real.dist_eq, Real.dist_eq]
  exact max_le (by linarith) (by linarith)

/-- The swapped square `{p | swap p ∈ Q}` is again compact, convex and symmetric (about `swap c`). -/
lemma swap_props (c : ℝ × ℝ) (θ : ℝ) :
    Convex ℝ (swapXY ⁻¹' sq c θ 1) ∧ IsCompact (swapXY ⁻¹' sq c θ 1) ∧
      ∀ p ∈ swapXY ⁻¹' sq c θ 1, (2 * c.2 - p.1, 2 * c.1 - p.2) ∈ swapXY ⁻¹' sq c θ 1 := by
  have hl : IsLinearMap ℝ swapXY := ⟨fun _ _ => rfl, fun _ _ => rfl⟩
  have he : swapXY ⁻¹' sq c θ 1 = swapXY '' sq c θ 1 := by
    ext p; simp only [Set.mem_preimage, Set.mem_image]
    exact ⟨fun h => ⟨swapXY p, h, rfl⟩, fun ⟨q, hq, e⟩ => by rw [← e]; exact hq⟩
  refine ⟨(convex_sq c θ).is_linear_preimage hl, ?_, fun p hp => ?_⟩
  · rw [he]; exact (isCompact_sq c θ).image (by unfold swapXY; fun_prop)
  · exact sq_sym c θ _ hp

/-- **The cap below `y = a`** of a unit square: `λ(Q ∩ {y < a}) ≤ d · λ₁(Q ∩ {y = a})` when the
centre is above the line and `Q ⊆ {y ≥ a − d}`. -/
theorem sq_below_le (c : ℝ × ℝ) (θ : ℝ) {a d : ℝ} (hac : a ≤ c.2)
    (hb : ∀ p ∈ sq c θ 1, a - d ≤ p.2) :
    volume (sq c θ 1 ∩ {p | p.2 < a}) ≤ ENNReal.ofReal d * volume (hsl (sq c θ 1) a) :=
  vol_below_le (measurableSet_sq c θ 1) hb fun _ hy =>
    vol_hsl_le (convex_sq c θ) (isCompact_sq c θ) (sq_sym c θ) hy hac

/-- The vertical slice `{y | (x, y) ∈ Q}`. -/
def vsl (Q : Set (ℝ × ℝ)) (x : ℝ) : Set ℝ := {y | (x, y) ∈ Q}

/-- **The cap left of `x = a`**, by the diagonal reflection. -/
theorem sq_left_le (c : ℝ × ℝ) (θ : ℝ) {a d : ℝ} (hac : a ≤ c.1)
    (hb : ∀ p ∈ sq c θ 1, a - d ≤ p.1) :
    volume (sq c θ 1 ∩ {p | p.1 < a}) ≤ ENNReal.ofReal d * volume (vsl (sq c θ 1) a) := by
  obtain ⟨hcv, hcp, hsy⟩ := swap_props c θ
  have hmeas : MeasurableSet (swapXY ⁻¹' sq c θ 1) :=
    (by unfold swapXY; fun_prop : Measurable swapXY) (measurableSet_sq c θ 1)
  have h := vol_below_le (Q := swapXY ⁻¹' sq c θ 1) hmeas (a := a) (d := d)
    (fun p hp => hb _ hp) fun _ hy =>
      vol_hsl_le (c := (c.2, c.1)) hcv hcp hsy hy hac
  have e : swapXY ⁻¹' (sq c θ 1 ∩ {p | p.1 < a}) = swapXY ⁻¹' sq c θ 1 ∩ {p | p.2 < a} := rfl
  rw [← measurePreserving_swapXY.measure_preimage
    ((measurableSet_sq c θ 1).inter (measurableSet_lt measurable_fst measurable_const)).nullMeasurableSet, e]
  exact h

/-! ## 5.  Lemma K: the boundary lines' segments -/

open Bentz (segA segB) in
/-- A horizontal unit segment `(false, i, j)` captures `5 λ₁(Q_{j/5} ∩ [i/5, (i+1)/5])`. -/
lemma segMeasure_h (i j : ℤ) {S : Set (ℝ × ℝ)} (hS : MeasurableSet S) :
    segMeasure (segA (false, i, j)) (segB (false, i, j)) S =
      5 * volume (hsl S ((j : ℝ) / 5) ∩ Set.Icc ((i : ℝ) / 5) (((i : ℝ) + 1) / 5)) := by
  rw [segMeasure_apply _ _ hS]
  have e : segPt (segA (false, i, j)) (segB (false, i, j)) ⁻¹' S ∩ Set.Icc 0 1 =
      (fun t : ℝ => (1 / 5 : ℝ) * t) ⁻¹' ((fun x => x + (i : ℝ) / 5) ⁻¹'
        (hsl S ((j : ℝ) / 5) ∩ Set.Icc ((i : ℝ) / 5) (((i : ℝ) + 1) / 5))) := by
    ext t
    simp only [segPt, segA, segB, Set.mem_inter_iff, Set.mem_preimage, Set.mem_Icc, hsl,
      Set.mem_ofPred_eq, Bool.false_eq_true, if_false]
    have e1 : ((i : ℝ) / 5 + t * (((i : ℝ) + 1) / 5 - (i : ℝ) / 5), (j : ℝ) / 5 + t * ((j : ℝ) / 5 - (j : ℝ) / 5))
        = (1 / 5 * t + (i : ℝ) / 5, (j : ℝ) / 5) := by ext <;> ring
    rw [e1]
    constructor
    · rintro ⟨h1, h2, h3⟩; exact ⟨h1, by linarith, by linarith⟩
    · rintro ⟨h1, h2, h3⟩; exact ⟨h1, by linarith, by linarith⟩
  rw [e, Real.volume_preimage_mul_left (by norm_num), measure_preimage_add_right]
  norm_num

open Bentz (segA segB) in
/-- A vertical unit segment `(true, i, j)` captures `5 λ₁(Q^{i/5} ∩ [j/5, (j+1)/5])`. -/
lemma segMeasure_v (i j : ℤ) {S : Set (ℝ × ℝ)} (hS : MeasurableSet S) :
    segMeasure (segA (true, i, j)) (segB (true, i, j)) S =
      5 * volume (vsl S ((i : ℝ) / 5) ∩ Set.Icc ((j : ℝ) / 5) (((j : ℝ) + 1) / 5)) := by
  rw [segMeasure_apply _ _ hS]
  have e : segPt (segA (true, i, j)) (segB (true, i, j)) ⁻¹' S ∩ Set.Icc 0 1 =
      (fun t : ℝ => (1 / 5 : ℝ) * t) ⁻¹' ((fun x => x + (j : ℝ) / 5) ⁻¹'
        (vsl S ((i : ℝ) / 5) ∩ Set.Icc ((j : ℝ) / 5) (((j : ℝ) + 1) / 5))) := by
    ext t
    simp only [segPt, segA, segB, Set.mem_inter_iff, Set.mem_preimage, Set.mem_Icc, vsl,
      Set.mem_ofPred_eq, if_true]
    have e1 : ((i : ℝ) / 5 + t * ((i : ℝ) / 5 - (i : ℝ) / 5), (j : ℝ) / 5 + t * (((j : ℝ) + 1) / 5 - (j : ℝ) / 5))
        = ((i : ℝ) / 5, 1 / 5 * t + (j : ℝ) / 5) := by ext <;> ring
    rw [e1]
    constructor
    · rintro ⟨h1, h2, h3⟩; exact ⟨h1, by linarith, by linarith⟩
    · rintro ⟨h1, h2, h3⟩; exact ⟨h1, by linarith, by linarith⟩
  rw [e, Real.volume_preimage_mul_left (by norm_num), measure_preimage_add_right]
  norm_num

/-- A set of the line inside `[i0/5, i1/5]` is covered by the cells `[i/5, (i+1)/5]`, `i0 ≤ i < i1`. -/
lemma vol_le_sum_cells {T : Set ℝ} {i0 i1 : ℕ} (h : T ⊆ Set.Icc ((i0 : ℝ) / 5) ((i1 : ℝ) / 5)) :
    volume T ≤ ∑ i ∈ Finset.Ico i0 i1, volume (T ∩ Set.Icc ((i : ℝ) / 5) (((i : ℝ) + 1) / 5)) := by
  have hsub : T ⊆ {(i0 : ℝ) / 5} ∪ ⋃ i ∈ Finset.Ico i0 i1,
      (T ∩ Set.Icc ((i : ℝ) / 5) (((i : ℝ) + 1) / 5)) := by
    intro x hx
    obtain ⟨hx0, hx1⟩ := h hx
    rcases eq_or_lt_of_le hx0 with he | hlt
    · exact Or.inl he.symm
    right
    have h5 : (0 : ℝ) ≤ 5 * x := by have := (Nat.cast_nonneg (α := ℝ) i0); linarith
    set k := ⌈5 * x⌉₊ with hk
    have hk1 : i0 < k := by rw [hk, Nat.lt_ceil]; linarith
    have hk2 : k ≤ i1 := by rw [hk, Nat.ceil_le]; linarith
    have hk3 : (k : ℝ) < 5 * x + 1 := Nat.ceil_lt_add_one h5
    have hk4 : 5 * x ≤ k := Nat.le_ceil _
    simp only [Set.mem_iUnion, Finset.mem_Ico]
    refine ⟨k - 1, ⟨by omega, by omega⟩, hx, ?_, ?_⟩
    · rw [Nat.cast_sub (by omega)]; push_cast; linarith
    · rw [Nat.cast_sub (by omega)]; push_cast; linarith
  calc volume T ≤ volume ({(i0 : ℝ) / 5} ∪ ⋃ i ∈ Finset.Ico i0 i1,
        (T ∩ Set.Icc ((i : ℝ) / 5) (((i : ℝ) + 1) / 5))) := measure_mono hsub
    _ ≤ volume {(i0 : ℝ) / 5} + volume (⋃ i ∈ Finset.Ico i0 i1,
        (T ∩ Set.Icc ((i : ℝ) / 5) (((i : ℝ) + 1) / 5))) := measure_union_le _ _
    _ ≤ _ := by rw [Real.volume_singleton, zero_add]; exact measure_biUnion_finset_le _ _

/-- **The line bound**: if the slice lies in the cells `i0 ≤ i < i1` and each cell's density is
`≥ d`, the cells' segments carry `≥ d · λ₁(slice)`. -/
lemma line_mass_ge {T : Set ℝ} {i0 i1 : ℕ} (h : T ⊆ Set.Icc ((i0 : ℝ) / 5) ((i1 : ℝ) / 5))
    {d : ℝ} {wl : ℕ → ℝ} (hw : ∀ i ∈ Finset.Ico i0 i1, d ≤ 5 * wl i) :
    ENNReal.ofReal d * volume T ≤
      ∑ i ∈ Finset.Ico i0 i1, ENNReal.ofReal (wl i) *
        (5 * volume (T ∩ Set.Icc ((i : ℝ) / 5) (((i : ℝ) + 1) / 5))) := by
  calc ENNReal.ofReal d * volume T
      ≤ ENNReal.ofReal d * ∑ i ∈ Finset.Ico i0 i1,
          volume (T ∩ Set.Icc ((i : ℝ) / 5) (((i : ℝ) + 1) / 5)) :=
        mul_le_mul_right (vol_le_sum_cells h) _
    _ = ∑ i ∈ Finset.Ico i0 i1, ENNReal.ofReal d *
          volume (T ∩ Set.Icc ((i : ℝ) / 5) (((i : ℝ) + 1) / 5)) := Finset.mul_sum _ _ _
    _ ≤ _ := by
        refine Finset.sum_le_sum fun i hi => ?_
        rw [← mul_assoc]
        refine mul_le_mul_left ?_ _
        calc ENNReal.ofReal d ≤ ENNReal.ofReal (5 * wl i) := ENNReal.ofReal_le_ofReal (hw i hi)
          _ ≤ ENNReal.ofReal (wl i) * 5 := by
              rw [mul_comm, ENNReal.ofReal_mul' (by norm_num)]; simp

/-! ## 6.  Lemma K: the tangent cap and the chord ranges -/

/-- `cos θ − sin θ`, `tan θ`, `cot θ` at `θ = 2 arctan u`. -/
def csQ (u : ℚ) : ℚ := (1 - u * u - 2 * u) / (1 + u * u)
def tqQ (u : ℚ) : ℚ := 2 * u / (1 - u * u)
def ctQ (u : ℚ) : ℚ := (1 - u * u) / (2 * u)

lemma cs_anti {u v : ℝ} (hu : 0 ≤ u) (huv : u ≤ v) (hv : v ≤ 1) :
    (1 - v * v - 2 * v) / (1 + v * v) ≤ (1 - u * u - 2 * u) / (1 + u * u) := by
  rw [div_le_div_iff₀ (by nlinarith) (by nlinarith)]
  nlinarith [mul_nonneg (sub_nonneg.mpr huv)
    (show 0 ≤ u + v + 1 - u * v by nlinarith [mul_le_mul_of_nonneg_left hv hu])]

lemma tq_mono {u v : ℝ} (hu : 0 ≤ u) (huv : u ≤ v) (hv : v < 1) :
    2 * u / (1 - u * u) ≤ 2 * v / (1 - v * v) := by
  rw [div_le_div_iff₀ (by nlinarith) (by nlinarith)]
  nlinarith [mul_nonneg (sub_nonneg.mpr huv) (show 0 ≤ 1 + u * v by nlinarith)]

lemma ct_anti {u v : ℝ} (hu : 0 < u) (huv : u ≤ v) :
    (1 - v * v) / (2 * v) ≤ (1 - u * u) / (2 * u) := by
  rw [div_le_div_iff₀ (by linarith) (by linarith)]
  nlinarith [mul_nonneg (sub_nonneg.mpr huv) (show 0 ≤ 1 + u * v by nlinarith)]

/-- **The cone at the lowest vertex** `BL = c + ((S − C)/2, −(C + S)/2)`: every point of the square
has `C (p₁ − x_BL) + S (p₂ − y_BL) ≥ 0` and `S (p₁ − x_BL) − C (p₂ − y_BL) ≤ 0`. -/
lemma cone_BL {c p : ℝ × ℝ} {θ : ℝ} (hp : p ∈ sq c θ 1) :
    0 ≤ Real.cos θ * (p.1 - (c.1 - (Real.cos θ - Real.sin θ) / 2)) +
        Real.sin θ * (p.2 - (c.2 - (Real.cos θ + Real.sin θ) / 2)) ∧
    Real.sin θ * (p.1 - (c.1 - (Real.cos θ - Real.sin θ) / 2)) -
        Real.cos θ * (p.2 - (c.2 - (Real.cos θ + Real.sin θ) / 2)) ≤ 0 := by
  obtain ⟨hX, hY⟩ := hp
  obtain ⟨e1, e2⟩ := sub_eq_of_coord c θ p
  have hCS := Real.cos_sq_add_sin_sq θ
  rw [abs_le] at hX hY
  set X := (coord c θ p).1
  set Y := (coord c θ p).2
  constructor
  · have : Real.cos θ * (p.1 - (c.1 - (Real.cos θ - Real.sin θ) / 2)) +
        Real.sin θ * (p.2 - (c.2 - (Real.cos θ + Real.sin θ) / 2)) = X + 1 / 2 := by
      linear_combination Real.cos θ * e1 + Real.sin θ * e2 + (X + 1 / 2) * hCS
    linarith
  · have : Real.sin θ * (p.1 - (c.1 - (Real.cos θ - Real.sin θ) / 2)) -
        Real.cos θ * (p.2 - (c.2 - (Real.cos θ + Real.sin θ) / 2)) = -Y - 1 / 2 := by
      linear_combination Real.sin θ * e1 - Real.cos θ * e2 + (-Y - 1 / 2) * hCS
    linarith

/-- **The cone at the leftmost vertex** `TL = c + (−(C + S)/2, (C − S)/2)`. -/
lemma cone_TL {c p : ℝ × ℝ} {θ : ℝ} (hp : p ∈ sq c θ 1) :
    0 ≤ Real.sin θ * (p.2 - (c.2 + (Real.cos θ - Real.sin θ) / 2)) +
        Real.cos θ * (p.1 - (c.1 - (Real.cos θ + Real.sin θ) / 2)) ∧
    Real.cos θ * (p.2 - (c.2 + (Real.cos θ - Real.sin θ) / 2)) -
        Real.sin θ * (p.1 - (c.1 - (Real.cos θ + Real.sin θ) / 2)) ≤ 0 := by
  obtain ⟨hX, hY⟩ := hp
  obtain ⟨e1, e2⟩ := sub_eq_of_coord c θ p
  have hCS := Real.cos_sq_add_sin_sq θ
  rw [abs_le] at hX hY
  set X := (coord c θ p).1
  set Y := (coord c θ p).2
  constructor
  · have : Real.sin θ * (p.2 - (c.2 + (Real.cos θ - Real.sin θ) / 2)) +
        Real.cos θ * (p.1 - (c.1 - (Real.cos θ + Real.sin θ) / 2)) = X + 1 / 2 := by
      linear_combination Real.sin θ * e2 + Real.cos θ * e1 + (X + 1 / 2) * hCS
    linarith
  · have : Real.cos θ * (p.2 - (c.2 + (Real.cos θ - Real.sin θ) / 2)) -
        Real.sin θ * (p.1 - (c.1 - (Real.cos θ + Real.sin θ) / 2)) = Y - 1 / 2 := by
      linear_combination Real.cos θ * e2 - Real.sin θ * e1 + (Y - 1 / 2) * hCS
    linarith

/-! ## 7.  Lemma K: the CAP test and its soundness -/

/-- The tangent-cap refinement is used when `0 < u0` and `u1 < 1`. -/
def tang (B : PBox) : Prop := 0 < B.u0 ∧ B.u1 < 1

instance (B : PBox) : Decidable (tang B) := inferInstanceAs (Decidable (_ ∧ _))

/-- A range containing the chord `Q ∩ {y = a}` (parameter `x`), cap depth `≤ d`. -/
def loY (B : PBox) (d : ℚ) : ℚ :=
  if tang B then max (B.x0 - whi B.u1 / 2) (B.x0 - csQ B.u0 / 2 - tqQ B.u1 * d)
  else B.x0 - whi B.u1 / 2
def hiY (B : PBox) (d : ℚ) : ℚ :=
  if tang B then min (B.x1 + whi B.u1 / 2) (B.x1 - csQ B.u1 / 2 + ctQ B.u0 * d)
  else B.x1 + whi B.u1 / 2
/-- A range containing the chord `Q ∩ {x = a}` (parameter `y`), cap depth `≤ d`. -/
def loX (B : PBox) (d : ℚ) : ℚ :=
  if tang B then max (B.y0 - whi B.u1 / 2) (B.y0 + csQ B.u1 / 2 - ctQ B.u0 * d)
  else B.y0 - whi B.u1 / 2
def hiX (B : PBox) (d : ℚ) : ℚ :=
  if tang B then min (B.y1 + whi B.u1 / 2) (B.y1 + csQ B.u0 / 2 + tqQ B.u1 * d)
  else B.y1 + whi B.u1 / 2

/-- The first and one-past-last cell (of the `1/5`-grid) meeting a range. -/
def cellLo (lo : ℚ) : ℕ := (⌊5 * lo⌋).toNat
def cellHi (K : ℕ) (hi : ℚ) : ℕ := min (5 * K) (⌈5 * hi⌉).toNat

/-- Every cell `i0 ≤ i < i1` of the line has density `5 wl i / den ≥ d`. -/
def lineOK (den : ℕ) (wl : ℕ → ℕ) (d : ℚ) (i0 i1 : ℕ) : Bool :=
  (List.range' i0 (i1 - i0)).all fun i => decide (d * den ≤ 5 * (wl i : ℚ))

/-- **The CAP test** (`cert_cap`), for a grid cover with Lebesgue square `[a, K − a]²`, `a = A/5`:
the squares stay below `y, x ≤ K − a`; for each of the lines `y = a`, `x = a` either no square of
the box crosses it, or the centres are on `U`'s side and the cap depth `d` is at most the density
of every grid cell of the line meeting the chord range. -/
def capOK (K A den : ℕ) (w : SegIx → ℕ) (B : PBox) : Bool :=
  let a : ℚ := A / 5
  let h := whi B.u1 / 2
  let dy := a - B.y0 + h
  let dx := a - B.x0 + h
  decide (B.x1 + h ≤ K - a ∧ B.y1 + h ≤ K - a) &&
  (decide (dy ≤ 0) || (decide (a ≤ B.y0) &&
     lineOK den (fun i => w (false, i, A)) dy (cellLo (loY B dy)) (cellHi K (hiY B dy)))) &&
  (decide (dx ≤ 0) || (decide (a ≤ B.x0) &&
     lineOK den (fun j => w (true, A, j)) dx (cellLo (loX B dx)) (cellHi K (hiX B dx))))

lemma lineOK_spec {den : ℕ} {wl : ℕ → ℕ} {d : ℚ} {i0 i1 : ℕ} (hden : 0 < den)
    (h : lineOK den wl d i0 i1 = true) :
    ∀ i ∈ Finset.Ico i0 i1, (d : ℝ) ≤ 5 * ((wl i : ℝ) / den) := by
  intro i hi
  rw [Finset.mem_Ico] at hi
  simp only [lineOK, List.all_eq_true, List.mem_range'_1, decide_eq_true_eq] at h
  have h1 := h i ⟨hi.1, by omega⟩
  have h2 : (d : ℝ) * den ≤ 5 * (wl i : ℝ) := by exact_mod_cast h1
  have hd : (0 : ℝ) < den := by exact_mod_cast hden
  rw [mul_div_assoc', le_div_iff₀ hd]; exact h2

lemma cell_range {x : ℝ} {lo hi : ℚ} {K : ℕ} (h0 : 0 ≤ x) (hK : x ≤ K) (hlo : (lo : ℝ) ≤ x)
    (hhi : x ≤ hi) : x ∈ Set.Icc ((cellLo lo : ℝ) / 5) ((cellHi K hi : ℝ) / 5) := by
  constructor
  · simp only [cellLo]
    rcases le_total ⌊5 * lo⌋ 0 with hz | hz
    · rw [Int.toNat_eq_zero.mpr hz]; simpa using h0
    · have e : (((⌊5 * lo⌋).toNat : ℕ) : ℝ) = ((⌊5 * lo⌋ : ℤ) : ℝ) := by
        rw [← Int.cast_natCast, Int.toNat_of_nonneg hz]
      have hf : ((⌊5 * lo⌋ : ℤ) : ℝ) ≤ 5 * (lo : ℝ) := by
        have := Int.floor_le (5 * lo); exact_mod_cast this
      rw [e]; linarith
  · simp only [cellHi, Nat.cast_min]
    rw [le_div_iff₀ (by norm_num)]
    refine le_min (by push_cast; linarith) ?_
    have e : ((⌈5 * hi⌉ : ℤ) : ℝ) ≤ (((⌈5 * hi⌉).toNat : ℕ) : ℝ) := by
      rw [← Int.cast_natCast]; exact_mod_cast Int.self_le_toNat _
    have hc : 5 * (hi : ℝ) ≤ ((⌈5 * hi⌉ : ℤ) : ℝ) := by
      have := Int.le_ceil (5 * hi); exact_mod_cast this
    linarith

lemma cast_csQ (u : ℚ) : (csQ u : ℝ) = (1 - (u : ℝ) * u - 2 * u) / (1 + (u : ℝ) * u) := by
  simp [csQ]
lemma cast_tqQ (u : ℚ) : (tqQ u : ℝ) = 2 * (u : ℝ) / (1 - (u : ℝ) * u) := by
  simp [tqQ]
lemma cast_ctQ (u : ℚ) : (ctQ u : ℝ) = (1 - (u : ℝ) * u) / (2 * u) := by
  simp [ctQ]

/-- The pose facts at `θ = 2 arctan u` used by the tangent cap. -/
lemma trig_facts {u : ℝ} (hu : 0 < u) (hu1 : u < 1) :
    let C := Real.cos (2 * Real.arctan u)
    let S := Real.sin (2 * Real.arctan u)
    0 < C ∧ 0 < S ∧ S = 2 * u / (1 - u * u) * C ∧ C = (1 - u * u) / (2 * u) * S ∧
      C - S = (1 - u * u - 2 * u) / (1 + u * u) ∧ C + S = widU u := by
  intro C S
  have hN : (0 : ℝ) < 1 + u ^ 2 := by positivity
  have hC : C = (1 - u * u) / (1 + u * u) := by simp only [C]; rw [cos_two_arctan]; ring_nf
  have hS : S = 2 * u / (1 + u * u) := by simp only [S]; rw [sin_two_arctan]; ring_nf
  have h1 : (0 : ℝ) < 1 - u * u := by nlinarith
  have h1' : (1 : ℝ) - u * u ≠ 0 := h1.ne'
  have hN' : (1 : ℝ) + u * u ≠ 0 := by nlinarith
  have hu0 : u ≠ 0 := hu.ne'
  refine ⟨by rw [hC]; apply div_pos h1; nlinarith, by rw [hS]; positivity, ?_, ?_, ?_, ?_⟩
  · rw [hC, hS, div_mul_div_comm, mul_comm (1 - u * u), ← div_mul_div_comm, div_self h1', mul_one]
  · rw [hC, hS, div_mul_div_comm, mul_comm (2 * u), ← div_mul_div_comm,
      div_self (mul_ne_zero two_ne_zero hu0), mul_one]
  · rw [hC, hS]; ring
  · rw [hC, hS, widU]; ring

/-- **The chord on `y = a` lies in `[loY, hiY]`.** -/
lemma chordY {B : PBox} {c : ℝ × ℝ} {u : ℝ} (hx0 : (B.x0 : ℝ) ≤ c.1) (hx1 : c.1 ≤ B.x1)
    (hy0 : (B.y0 : ℝ) ≤ c.2) (hu0 : (B.u0 : ℝ) ≤ u) (hu1 : u ≤ B.u1) (hu : 0 < u)
    (hu' : u ^ 2 + 2 * u ≤ 1) {a : ℝ} {d : ℚ} (hd : (d : ℝ) = a - B.y0 + whi B.u1 / 2)
    (hd0 : 0 ≤ (d : ℝ)) {x : ℝ} (hp : (x, a) ∈ sq c (2 * Real.arctan u) 1) :
    (loY B d : ℝ) ≤ x ∧ x ≤ hiY B d := by
  obtain ⟨e1, _⟩ := abs_sub_le_whi hu.le hu1 hu' hp
  rw [abs_le] at e1
  have hlo : (B.x0 : ℝ) - whi B.u1 / 2 ≤ x := by linarith [e1.1]
  have hhi : x ≤ (B.x1 : ℝ) + whi B.u1 / 2 := by linarith [e1.2]
  by_cases ht : tang B
  · obtain ⟨ht0, ht1⟩ := ht
    have ht0' : (0 : ℝ) < B.u0 := by exact_mod_cast ht0
    have ht1' : (B.u1 : ℝ) < 1 := by exact_mod_cast ht1
    have hult : u < 1 := by linarith
    obtain ⟨hC, hS, eS, eC, eCS, eW⟩ := trig_facts hu hult
    obtain ⟨k1, k2⟩ := cone_BL (c := c) (p := (x, a)) hp
    simp only at k1 k2
    set C := Real.cos (2 * Real.arctan u)
    set S := Real.sin (2 * Real.arctan u)
    have hw := widU_le_whi hu.le hu1 hu'
    set t := a - (c.2 - (C + S) / 2)
    have htd : t ≤ d := by rw [hd]; simp only [t]; linarith
    set τ := 2 * u / (1 - u * u)
    set κ := (1 - u * u) / (2 * u)
    have hτ : 0 ≤ τ := div_nonneg (by linarith) (by nlinarith)
    have hκ : 0 ≤ κ := div_nonneg (by nlinarith) (by linarith)
    have hτ1 : τ ≤ tqQ B.u1 := by rw [cast_tqQ]; exact tq_mono hu.le hu1 ht1'
    have hκ0 : κ ≤ ctQ B.u0 := by rw [cast_ctQ]; exact ct_anti ht0' hu0
    have hcs0 : C - S ≤ csQ B.u0 := by
      rw [cast_csQ, eCS]; exact cs_anti ht0'.le hu0 hult.le
    have hcs1 : (csQ B.u1 : ℝ) ≤ C - S := by
      rw [cast_csQ, eCS]; exact cs_anti hu.le hu1 ht1'.le
    have hL : 0 ≤ x - (c.1 - (C - S) / 2) + τ * t := by
      have e : C * (x - (c.1 - (C - S) / 2) + τ * t) =
          C * (x - (c.1 - (C - S) / 2)) + S * t := by rw [eS]; ring
      by_contra hneg; push Not at hneg; nlinarith [mul_pos hC (neg_pos.mpr hneg)]
    have hU : x - (c.1 - (C - S) / 2) - κ * t ≤ 0 := by
      have e : S * (x - (c.1 - (C - S) / 2) - κ * t) =
          S * (x - (c.1 - (C - S) / 2)) - C * t := by rw [eC]; ring
      by_contra hpos; push Not at hpos; nlinarith [mul_pos hS hpos]
    have hτd : τ * t ≤ tqQ B.u1 * d := by
      calc τ * t ≤ τ * d := mul_le_mul_of_nonneg_left htd hτ
        _ ≤ tqQ B.u1 * d := mul_le_mul_of_nonneg_right hτ1 hd0
    have hκd : κ * t ≤ ctQ B.u0 * d := by
      calc κ * t ≤ κ * d := mul_le_mul_of_nonneg_left htd hκ
        _ ≤ ctQ B.u0 * d := mul_le_mul_of_nonneg_right hκ0 hd0
    simp only [loY, hiY, if_pos (show tang B from ⟨ht0, ht1⟩)]
    push_cast
    exact ⟨max_le hlo (by linarith), le_min hhi (by linarith)⟩
  · simp only [loY, hiY, if_neg ht]
    push_cast
    exact ⟨hlo, hhi⟩

/-- **The chord on `x = a` lies in `[loX, hiX]`.** -/
lemma chordX {B : PBox} {c : ℝ × ℝ} {u : ℝ} (hx0 : (B.x0 : ℝ) ≤ c.1)
    (hy0 : (B.y0 : ℝ) ≤ c.2) (hy1 : c.2 ≤ B.y1) (hu0 : (B.u0 : ℝ) ≤ u) (hu1 : u ≤ B.u1) (hu : 0 < u)
    (hu' : u ^ 2 + 2 * u ≤ 1) {a : ℝ} {d : ℚ} (hd : (d : ℝ) = a - B.x0 + whi B.u1 / 2)
    (hd0 : 0 ≤ (d : ℝ)) {y : ℝ} (hp : (a, y) ∈ sq c (2 * Real.arctan u) 1) :
    (loX B d : ℝ) ≤ y ∧ y ≤ hiX B d := by
  obtain ⟨_, e2⟩ := abs_sub_le_whi hu.le hu1 hu' hp
  rw [abs_le] at e2
  have hlo : (B.y0 : ℝ) - whi B.u1 / 2 ≤ y := by linarith [e2.1]
  have hhi : y ≤ (B.y1 : ℝ) + whi B.u1 / 2 := by linarith [e2.2]
  by_cases ht : tang B
  · obtain ⟨ht0, ht1⟩ := ht
    have ht0' : (0 : ℝ) < B.u0 := by exact_mod_cast ht0
    have ht1' : (B.u1 : ℝ) < 1 := by exact_mod_cast ht1
    have hult : u < 1 := by linarith
    obtain ⟨hC, hS, eS, eC, eCS, eW⟩ := trig_facts hu hult
    obtain ⟨k1, k2⟩ := cone_TL (c := c) (p := (a, y)) hp
    simp only at k1 k2
    set C := Real.cos (2 * Real.arctan u)
    set S := Real.sin (2 * Real.arctan u)
    have hw := widU_le_whi hu.le hu1 hu'
    set t := a - (c.1 - (C + S) / 2)
    have htd : t ≤ d := by rw [hd]; simp only [t]; linarith
    set τ := 2 * u / (1 - u * u)
    set κ := (1 - u * u) / (2 * u)
    have hτ : 0 ≤ τ := div_nonneg (by linarith) (by nlinarith)
    have hκ : 0 ≤ κ := div_nonneg (by nlinarith) (by linarith)
    have hτ1 : τ ≤ tqQ B.u1 := by rw [cast_tqQ]; exact tq_mono hu.le hu1 ht1'
    have hκ0 : κ ≤ ctQ B.u0 := by rw [cast_ctQ]; exact ct_anti ht0' hu0
    have hcs0 : C - S ≤ csQ B.u0 := by
      rw [cast_csQ, eCS]; exact cs_anti ht0'.le hu0 hult.le
    have hcs1 : (csQ B.u1 : ℝ) ≤ C - S := by
      rw [cast_csQ, eCS]; exact cs_anti hu.le hu1 ht1'.le
    have hL : 0 ≤ y - (c.2 + (C - S) / 2) + κ * t := by
      have e : S * (y - (c.2 + (C - S) / 2) + κ * t) =
          S * (y - (c.2 + (C - S) / 2)) + C * t := by rw [eC]; ring
      by_contra hneg; push Not at hneg; nlinarith [mul_pos hS (neg_pos.mpr hneg)]
    have hU : y - (c.2 + (C - S) / 2) - τ * t ≤ 0 := by
      have e : C * (y - (c.2 + (C - S) / 2) - τ * t) =
          C * (y - (c.2 + (C - S) / 2)) - S * t := by rw [eS]; ring
      by_contra hpos; push Not at hpos; nlinarith [mul_pos hC hpos]
    have hτd : τ * t ≤ tqQ B.u1 * d := by
      calc τ * t ≤ τ * d := mul_le_mul_of_nonneg_left htd hτ
        _ ≤ tqQ B.u1 * d := mul_le_mul_of_nonneg_right hτ1 hd0
    have hκd : κ * t ≤ ctQ B.u0 * d := by
      calc κ * t ≤ κ * d := mul_le_mul_of_nonneg_left htd hκ
        _ ≤ ctQ B.u0 * d := mul_le_mul_of_nonneg_right hκ0 hd0
    simp only [loX, hiX, if_pos (show tang B from ⟨ht0, ht1⟩)]
    push_cast
    exact ⟨max_le hlo (by linarith), le_min hhi (by linarith)⟩
  · simp only [loX, hiX, if_neg ht]
    push_cast
    exact ⟨hlo, hhi⟩

open Bentz (segA segB) in
/-- **A grid cover's mass in `S`** is at least the Lebesgue part plus any horizontal unit segments
on `y = A/5` and vertical ones on `x = A/5` (each counted once). -/
lemma gridCover_ge {K A den : ℕ} {w : SegIx → ℕ} (hA : 2 * A < 5 * K) {S : Set (ℝ × ℝ)}
    (hS : MeasurableSet S) {I J : Finset ℕ} (hI : ∀ i ∈ I, i < 5 * K) (hJ : ∀ j ∈ J, j < 5 * K) :
    volume (S ∩ BentzFam.lebSq A K) +
      (∑ i ∈ I, ENNReal.ofReal ((w (false, i, A) : ℝ) / den) *
          segMeasure (segA (false, i, A)) (segB (false, i, A)) S +
        ∑ j ∈ J, ENNReal.ofReal ((w (true, A, j) : ℝ) / den) *
          segMeasure (segA (true, A, j)) (segB (true, A, j)) S) ≤
      (gridCover K A den w).measure S := by
  have hpoly : volume (S ∩ BentzFam.lebSq A K) =
      ∑ k ∈ (gridCover K A den w).polys, ENNReal.ofReal ((gridCover K A den w).gw k) *
        areaMeasure ((gridCover K A den w).poly k) S := by
    have hA' : (2 * A : ℝ) < 5 * K := by exact_mod_cast hA
    have hv := volume_lebSq A K hA.le
    have h0 : volume (BentzFam.lebSq A K) ≠ 0 := by
      rw [hv]; simp only [ne_eq, ENNReal.ofReal_eq_zero, not_le]; nlinarith
    have htop : volume (BentzFam.lebSq A K) ≠ ⊤ := by rw [hv]; exact ENNReal.ofReal_ne_top
    simp only [gridCover, Finset.univ_unique, Finset.sum_singleton]
    rw [areaMeasure_apply _ hS, ← hv, ← mul_assoc, ENNReal.mul_inv_cancel h0 htop, one_mul]
  set f : ℕ → SegIx := fun i => (false, (i : ℤ), (A : ℤ))
  set g : ℕ → SegIx := fun j => (true, (A : ℤ), (j : ℤ))
  set F : SegIx → ℝ≥0∞ := fun s => ENNReal.ofReal ((gridCover K A den w).sw s) *
    segMeasure ((gridCover K A den w).sa s) ((gridCover K A den w).sb s) S
  have hdisj : Disjoint (I.image f) (J.image g) := by
    rw [Finset.disjoint_left]
    intro s hs ht
    obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hs
    obtain ⟨j, _, hj⟩ := Finset.mem_image.mp ht
    simp [f, g] at hj
  have hsum : (∑ i ∈ I, ENNReal.ofReal ((w (false, i, A) : ℝ) / den) *
          segMeasure (segA (false, i, A)) (segB (false, i, A)) S +
        ∑ j ∈ J, ENNReal.ofReal ((w (true, A, j) : ℝ) / den) *
          segMeasure (segA (true, A, j)) (segB (true, A, j)) S) = ∑ s ∈ I.image f ∪ J.image g, F s := by
    rw [Finset.sum_union hdisj, Finset.sum_image (fun _ _ _ _ h => by simpa [f] using h),
      Finset.sum_image (fun _ _ _ _ h => by simpa [g] using h)]
    rfl
  have hsub : I.image f ∪ J.image g ⊆ (gridCover K A den w).segs := by
    intro s hs
    show s ∈ segsIn K
    rcases Finset.mem_union.mp hs with h | h
    · obtain ⟨i, hi, rfl⟩ := Finset.mem_image.mp h
      have := hI i hi
      rw [mem_segsIn]; refine ⟨⟨by omega, by omega⟩, ⟨by omega, by omega⟩, Or.inr ⟨rfl, by omega⟩⟩
    · obtain ⟨j, hj, rfl⟩ := Finset.mem_image.mp h
      have := hJ j hj
      rw [mem_segsIn]; refine ⟨⟨by omega, by omega⟩, ⟨by omega, by omega⟩, Or.inl ⟨rfl, by omega⟩⟩
  rw [MixedCover.measure_apply', hpoly, hsum, add_comm]
  refine add_le_add_left (le_trans (Finset.sum_le_sum_of_subset hsub) le_add_self) _

open Bentz (segA segB) in
/-- The line `y = A/5` pays for the cap below it. -/
lemma capY_claim {K A den : ℕ} {w : SegIx → ℕ} (hden : 0 < den) {B : PBox} {c : ℝ × ℝ} {u : ℝ}
    (hx0 : (B.x0 : ℝ) ≤ c.1) (hx1 : c.1 ≤ B.x1) (hy0 : (B.y0 : ℝ) ≤ c.2) (hu0 : (B.u0 : ℝ) ≤ u)
    (hu1 : u ≤ B.u1) (hu : 0 < u) (hu' : u ^ 2 + 2 * u ≤ 1)
    (hbox : sq c (2 * Real.arctan u) 1 ⊆ box K)
    (h : ((A : ℚ) / 5 - B.y0 + whi B.u1 / 2 ≤ 0) ∨ ((A : ℚ) / 5 ≤ B.y0 ∧
      lineOK den (fun i => w (false, i, A)) ((A : ℚ) / 5 - B.y0 + whi B.u1 / 2)
        (cellLo (loY B ((A : ℚ) / 5 - B.y0 + whi B.u1 / 2)))
        (cellHi K (hiY B ((A : ℚ) / 5 - B.y0 + whi B.u1 / 2))) = true)) :
    ∃ I : Finset ℕ, (∀ i ∈ I, i < 5 * K) ∧
      volume (sq c (2 * Real.arctan u) 1 ∩ {p | p.2 < (A : ℝ) / 5}) ≤
        ∑ i ∈ I, ENNReal.ofReal ((w (false, i, A) : ℝ) / den) *
          segMeasure (segA (false, i, A)) (segB (false, i, A)) (sq c (2 * Real.arctan u) 1) := by
  set Q := sq c (2 * Real.arctan u) 1
  set d : ℚ := (A : ℚ) / 5 - B.y0 + whi B.u1 / 2
  have hd : (d : ℝ) = (A : ℝ) / 5 - B.y0 + whi B.u1 / 2 := by simp only [d]; push_cast; ring
  have hlow : ∀ p ∈ Q, (A : ℝ) / 5 - d ≤ p.2 := by
    intro p hp
    obtain ⟨_, e2⟩ := abs_sub_le_whi hu.le hu1 hu' hp
    rw [abs_le] at e2; rw [hd]; linarith [e2.1]
  by_cases hd0 : d ≤ 0
  · refine ⟨∅, by simp, ?_⟩
    have : Q ∩ {p | p.2 < (A : ℝ) / 5} = ∅ := by
      ext p
      simp only [Set.mem_inter_iff, Set.mem_ofPred_eq, Set.mem_empty_iff_false, iff_false, not_and,
        not_lt]
      intro hp
      have := hlow p hp
      have : (d : ℝ) ≤ 0 := by exact_mod_cast hd0
      linarith
    rw [this, measure_empty]; exact zero_le
  rcases h with h | ⟨ha, hl⟩
  · exact absurd h hd0
  push Not at hd0
  have hd0' : (0 : ℝ) ≤ d := by exact_mod_cast hd0.le
  have ha' : (A : ℝ) / 5 ≤ B.y0 := by
    have h' : (((A : ℚ) / 5 : ℚ) : ℝ) ≤ (B.y0 : ℝ) := Rat.cast_le.mpr ha
    push_cast at h'; exact h'
  refine ⟨Finset.Ico (cellLo (loY B d)) (cellHi K (hiY B d)), fun i hi => ?_, ?_⟩
  · rw [Finset.mem_Ico] at hi; have := min_le_left (5 * K) (⌈5 * hiY B d⌉).toNat
    simp only [cellHi] at hi; omega
  have hT : hsl Q ((A : ℝ) / 5) ⊆
      Set.Icc ((cellLo (loY B d) : ℝ) / 5) ((cellHi K (hiY B d) : ℝ) / 5) := by
    intro x hx
    have hb := hbox hx
    obtain ⟨l1, l2⟩ := chordY hx0 hx1 hy0 hu0 hu1 hu hu' hd hd0' hx
    exact cell_range hb.1 hb.2.1 l1 l2
  have hseg : ∀ i : ℕ, segMeasure (segA (false, i, A)) (segB (false, i, A)) Q =
      5 * volume (hsl Q ((A : ℝ) / 5) ∩ Set.Icc ((i : ℝ) / 5) (((i : ℝ) + 1) / 5)) := by
    intro i
    have := segMeasure_h (i : ℤ) (A : ℤ) (measurableSet_sq c (2 * Real.arctan u) 1)
    simpa only [Int.cast_natCast] using this
  calc volume (Q ∩ {p | p.2 < (A : ℝ) / 5})
      ≤ ENNReal.ofReal d * volume (hsl Q ((A : ℝ) / 5)) :=
        sq_below_le c _ (le_trans ha' hy0) hlow
    _ ≤ _ := line_mass_ge hT (lineOK_spec hden hl)
    _ = _ := by simp only [hseg]

open Bentz (segA segB) in
/-- The line `x = A/5` pays for the cap left of it. -/
lemma capX_claim {K A den : ℕ} {w : SegIx → ℕ} (hden : 0 < den) {B : PBox} {c : ℝ × ℝ} {u : ℝ}
    (hx0 : (B.x0 : ℝ) ≤ c.1) (hy0 : (B.y0 : ℝ) ≤ c.2) (hy1 : c.2 ≤ B.y1) (hu0 : (B.u0 : ℝ) ≤ u)
    (hu1 : u ≤ B.u1) (hu : 0 < u) (hu' : u ^ 2 + 2 * u ≤ 1)
    (hbox : sq c (2 * Real.arctan u) 1 ⊆ box K)
    (h : ((A : ℚ) / 5 - B.x0 + whi B.u1 / 2 ≤ 0) ∨ ((A : ℚ) / 5 ≤ B.x0 ∧
      lineOK den (fun j => w (true, A, j)) ((A : ℚ) / 5 - B.x0 + whi B.u1 / 2)
        (cellLo (loX B ((A : ℚ) / 5 - B.x0 + whi B.u1 / 2)))
        (cellHi K (hiX B ((A : ℚ) / 5 - B.x0 + whi B.u1 / 2))) = true)) :
    ∃ J : Finset ℕ, (∀ j ∈ J, j < 5 * K) ∧
      volume (sq c (2 * Real.arctan u) 1 ∩ {p | p.1 < (A : ℝ) / 5}) ≤
        ∑ j ∈ J, ENNReal.ofReal ((w (true, A, j) : ℝ) / den) *
          segMeasure (segA (true, A, j)) (segB (true, A, j)) (sq c (2 * Real.arctan u) 1) := by
  set Q := sq c (2 * Real.arctan u) 1
  set d : ℚ := (A : ℚ) / 5 - B.x0 + whi B.u1 / 2
  have hd : (d : ℝ) = (A : ℝ) / 5 - B.x0 + whi B.u1 / 2 := by simp only [d]; push_cast; ring
  have hlow : ∀ p ∈ Q, (A : ℝ) / 5 - d ≤ p.1 := by
    intro p hp
    obtain ⟨e1, _⟩ := abs_sub_le_whi hu.le hu1 hu' hp
    rw [abs_le] at e1; rw [hd]; linarith [e1.1]
  by_cases hd0 : d ≤ 0
  · refine ⟨∅, by simp, ?_⟩
    have : Q ∩ {p | p.1 < (A : ℝ) / 5} = ∅ := by
      ext p
      simp only [Set.mem_inter_iff, Set.mem_ofPred_eq, Set.mem_empty_iff_false, iff_false, not_and,
        not_lt]
      intro hp
      have := hlow p hp
      have : (d : ℝ) ≤ 0 := by exact_mod_cast hd0
      linarith
    rw [this, measure_empty]; exact zero_le
  rcases h with h | ⟨ha, hl⟩
  · exact absurd h hd0
  push Not at hd0
  have hd0' : (0 : ℝ) ≤ d := by exact_mod_cast hd0.le
  have ha' : (A : ℝ) / 5 ≤ B.x0 := by
    have h' : (((A : ℚ) / 5 : ℚ) : ℝ) ≤ (B.x0 : ℝ) := Rat.cast_le.mpr ha
    push_cast at h'; exact h'
  refine ⟨Finset.Ico (cellLo (loX B d)) (cellHi K (hiX B d)), fun i hi => ?_, ?_⟩
  · rw [Finset.mem_Ico] at hi; have := min_le_left (5 * K) (⌈5 * hiX B d⌉).toNat
    simp only [cellHi] at hi; omega
  have hT : vsl Q ((A : ℝ) / 5) ⊆
      Set.Icc ((cellLo (loX B d) : ℝ) / 5) ((cellHi K (hiX B d) : ℝ) / 5) := by
    intro y hy
    have hb := hbox hy
    obtain ⟨l1, l2⟩ := chordX hx0 hy0 hy1 hu0 hu1 hu hu' hd hd0' hy
    exact cell_range hb.2.2.1 hb.2.2.2 l1 l2
  have hseg : ∀ j : ℕ, segMeasure (segA (true, A, j)) (segB (true, A, j)) Q =
      5 * volume (vsl Q ((A : ℝ) / 5) ∩ Set.Icc ((j : ℝ) / 5) (((j : ℝ) + 1) / 5)) := by
    intro j
    have := segMeasure_v (A : ℤ) (j : ℤ) (measurableSet_sq c (2 * Real.arctan u) 1)
    simpa only [Int.cast_natCast] using this
  calc volume (Q ∩ {p | p.1 < (A : ℝ) / 5})
      ≤ ENNReal.ofReal d * volume (vsl Q ((A : ℝ) / 5)) :=
        sq_left_le c _ (le_trans ha' hx0) hlow
    _ ≤ _ := line_mass_ge hT (lineOK_spec hden hl)
    _ = _ := by simp only [hseg]

/-- **Lemma K.**  If the CAP test passes, every square of the box has mass `≥ 1` under the grid
cover: `λ(Q ∩ U) + (caps' line mass) ≥ λ(Q ∩ U) + λ(Q ∩ {y < a}) + λ(Q ∩ {x < a}) ≥ λ(Q) = 1`. -/
theorem cap_sound {K A den : ℕ} {w : SegIx → ℕ} (hA : 2 * A < 5 * K) (hden : 0 < den) {B : PBox}
    (h : capOK K A den w B = true) : B.Cov K (gridCover K A den w).measure := by
  simp only [capOK, Bool.and_eq_true, Bool.or_eq_true, decide_eq_true_eq] at h
  obtain ⟨⟨⟨hb1, hb2⟩, hy⟩, hx⟩ := h
  intro c u hx0 hx1 hy0 hy1 hu0 hu1 hu hu' hbox
  obtain ⟨I, hI, hIy⟩ := capY_claim (w := w) hden hx0 hx1 hy0 hu0 hu1 hu hu' hbox hy
  obtain ⟨J, hJ, hJx⟩ := capX_claim (w := w) hden hx0 hy0 hy1 hu0 hu1 hu hu' hbox hx
  set Q := sq c (2 * Real.arctan u) 1
  have hb1' : (B.x1 : ℝ) + whi B.u1 / 2 ≤ K - A / 5 := by
    have h' : ((B.x1 + whi B.u1 / 2 : ℚ) : ℝ) ≤ (((K : ℚ) - A / 5 : ℚ) : ℝ) := Rat.cast_le.mpr hb1
    push_cast at h'; exact h'
  have hb2' : (B.y1 : ℝ) + whi B.u1 / 2 ≤ K - A / 5 := by
    have h' : ((B.y1 + whi B.u1 / 2 : ℚ) : ℝ) ≤ (((K : ℚ) - A / 5 : ℚ) : ℝ) := Rat.cast_le.mpr hb2
    push_cast at h'; exact h'
  have hcov : Q ⊆ (Q ∩ BentzFam.lebSq A K ∪ Q ∩ {p | p.2 < (A : ℝ) / 5}) ∪
      Q ∩ {p | p.1 < (A : ℝ) / 5} := by
    intro p hp
    obtain ⟨e1, e2⟩ := abs_sub_le_whi hu.le hu1 hu' hp
    rw [abs_le] at e1 e2
    by_cases h2 : p.2 < (A : ℝ) / 5
    · exact Or.inl (Or.inr ⟨hp, h2⟩)
    by_cases h1 : p.1 < (A : ℝ) / 5
    · exact Or.inr ⟨hp, h1⟩
    push Not at h1 h2
    exact Or.inl (Or.inl ⟨hp, ⟨h1, by linarith [e1.2]⟩, h2, by linarith [e2.2]⟩)
  calc (1 : ℝ≥0∞) = volume Q := (volume_sq c _).symm
    _ ≤ volume (Q ∩ BentzFam.lebSq A K) + volume (Q ∩ {p | p.2 < (A : ℝ) / 5}) +
          volume (Q ∩ {p | p.1 < (A : ℝ) / 5}) :=
        (measure_mono hcov).trans
          ((measure_union_le _ _).trans (by gcongr; exact measure_union_le _ _))
    _ ≤ volume (Q ∩ BentzFam.lebSq A K) + (_ + _) := by
        rw [add_assoc]; gcongr
    _ ≤ _ := gridCover_ge hA (measurableSet_sq c _ 1) hI hJ

end LebMass
end SquarePacking
