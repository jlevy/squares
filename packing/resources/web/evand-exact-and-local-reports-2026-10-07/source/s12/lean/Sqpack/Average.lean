import Sqpack.MixedMeasure

/-!
# Averaging lemma: symmetry of the container is free for cover measures

`search/FRIEDMAN.md` §9.1.1.  If a measure `μ` captures `≥ 1` in every closed unit square of a
region `C`, so does the uniform average of its push-forwards `μ.map gᵢ` under finitely many maps
`gᵢ` that pull closed unit squares of `C` back to closed unit squares of `C`; if the `gᵢ` also
preserve `C`, the average has the same mass on `C`.

* `CoverValid C μ` — every closed unit square `S ⊆ C` has `1 ≤ μ S`.
* `SqGood C g` — `g` pulls every closed unit square of `C` back to one of `C`.
* `coverValid_avg`, `avgMap_apply_of_preimage` — the generic lemma (any finite index type).
* `d4map m : Fin 8 → (ℝ × ℝ → ℝ × ℝ)` — the symmetry group of `box m` as the eight words in
  `reflX m`, `swapXY`; composing with either generator permutes it (`reflX_comp_d4map`,
  `swapXY_comp_d4map`).
* **`exists_d4InvM_cover`** — every valid cover measure of `box m` has a D4-invariant valid cover
  measure of the same total mass.  So restricting certificates to D4-invariant ones (as all ours
  are) loses nothing, and `d4_reduction_measure` applies to the average.
-/

open MeasureTheory
open scoped ENNReal

namespace SquarePacking

/-! ## 1.  The generic averaging lemma -/

/-- `μ` is a valid cover of `C`: every closed unit square inside `C` has measure `≥ 1`. -/
def CoverValid (C : Set (ℝ × ℝ)) (μ : Measure (ℝ × ℝ)) : Prop :=
  ∀ (c : ℝ × ℝ) (θ : ℝ), sq c θ 1 ⊆ C → 1 ≤ μ (sq c θ 1)

/-- `g` pulls every closed unit square of `C` back to a closed unit square of `C`. -/
def SqGood (C : Set (ℝ × ℝ)) (g : ℝ × ℝ → ℝ × ℝ) : Prop :=
  ∀ (c : ℝ × ℝ) (θ : ℝ), sq c θ 1 ⊆ C →
    ∃ (c' : ℝ × ℝ) (θ' : ℝ), g ⁻¹' sq c θ 1 = sq c' θ' 1 ∧ sq c' θ' 1 ⊆ C

lemma sqGood_id (C : Set (ℝ × ℝ)) : SqGood C id :=
  fun c θ h => ⟨c, θ, rfl, h⟩

lemma SqGood.comp {C : Set (ℝ × ℝ)} {g h : ℝ × ℝ → ℝ × ℝ} (hg : SqGood C g) (hh : SqGood C h) :
    SqGood C (g ∘ h) := by
  intro c θ hS
  obtain ⟨c₁, θ₁, e₁, s₁⟩ := hg c θ hS
  obtain ⟨c₂, θ₂, e₂, s₂⟩ := hh c₁ θ₁ s₁
  exact ⟨c₂, θ₂, by rw [Set.preimage_comp, e₁, e₂], s₂⟩

/-- The uniform average of the push-forwards of `μ` under the maps `g i`. -/
noncomputable def avgMap {ι : Type*} [Fintype ι] (g : ι → ℝ × ℝ → ℝ × ℝ) (μ : Measure (ℝ × ℝ)) :
    Measure (ℝ × ℝ) :=
  (Fintype.card ι : ℝ≥0∞)⁻¹ • ∑ i, μ.map (g i)

lemma avgMap_apply {ι : Type*} [Fintype ι] {g : ι → ℝ × ℝ → ℝ × ℝ} (hg : ∀ i, Measurable (g i))
    (μ : Measure (ℝ × ℝ)) {S : Set (ℝ × ℝ)} (hS : MeasurableSet S) :
    avgMap g μ S = (Fintype.card ι : ℝ≥0∞)⁻¹ * ∑ i, μ (g i ⁻¹' S) := by
  simp only [avgMap, Measure.smul_apply, smul_eq_mul, Measure.coe_finsetSum, Finset.sum_apply,
    Measure.map_apply (hg _) hS]

/-- **Averaging lemma.**  Averaging over square-good maps preserves validity. -/
theorem coverValid_avg {ι : Type*} [Fintype ι] [Nonempty ι] {C : Set (ℝ × ℝ)}
    {g : ι → ℝ × ℝ → ℝ × ℝ} (hg : ∀ i, Measurable (g i)) (hgood : ∀ i, SqGood C (g i))
    {μ : Measure (ℝ × ℝ)} (hμ : CoverValid C μ) : CoverValid C (avgMap g μ) := by
  intro c θ hS
  rw [avgMap_apply hg μ (measurableSet_sq c θ 1)]
  have hsum : (Fintype.card ι : ℝ≥0∞) ≤ ∑ i, μ (g i ⁻¹' sq c θ 1) := by
    have : ∑ _i : ι, (1 : ℝ≥0∞) ≤ ∑ i, μ (g i ⁻¹' sq c θ 1) := by
      refine Finset.sum_le_sum fun i _ => ?_
      obtain ⟨c', θ', e, s⟩ := hgood i c θ hS
      rw [e]; exact hμ c' θ' s
    simpa using this
  have hn0 : (Fintype.card ι : ℝ≥0∞) ≠ 0 := by simp [Fintype.card_ne_zero]
  have hnt : (Fintype.card ι : ℝ≥0∞) ≠ ⊤ := ENNReal.natCast_ne_top _
  calc (1 : ℝ≥0∞) = (Fintype.card ι : ℝ≥0∞)⁻¹ * (Fintype.card ι : ℝ≥0∞) :=
        (ENNReal.inv_mul_cancel hn0 hnt).symm
    _ ≤ _ := by gcongr

/-- If every map preserves `C` (as a preimage), the average has the same mass on `C`. -/
theorem avgMap_apply_of_preimage {ι : Type*} [Fintype ι] [Nonempty ι] {C : Set (ℝ × ℝ)}
    (hC : MeasurableSet C) {g : ι → ℝ × ℝ → ℝ × ℝ} (hg : ∀ i, Measurable (g i))
    (hpre : ∀ i, g i ⁻¹' C = C) (μ : Measure (ℝ × ℝ)) : avgMap g μ C = μ C := by
  rw [avgMap_apply hg μ hC]
  simp only [hpre, Finset.sum_const, Finset.card_univ, nsmul_eq_mul]
  have hn0 : (Fintype.card ι : ℝ≥0∞) ≠ 0 := by simp [Fintype.card_ne_zero]
  have hnt : (Fintype.card ι : ℝ≥0∞) ≠ ⊤ := ENNReal.natCast_ne_top _
  rw [← mul_assoc, ENNReal.inv_mul_cancel hn0 hnt, one_mul]

/-- Reindexing: if `h ∘ g i = g (σ i)` for a permutation `σ`, the average is `h`-invariant. -/
theorem avgMap_preimage_eq {ι : Type*} [Fintype ι] {g : ι → ℝ × ℝ → ℝ × ℝ}
    (hg : ∀ i, Measurable (g i)) {h : ℝ × ℝ → ℝ × ℝ} (hh : Measurable h) (σ : ι ≃ ι)
    (hσ : ∀ i, h ∘ g i = g (σ i)) (μ : Measure (ℝ × ℝ)) {S : Set (ℝ × ℝ)} (hS : MeasurableSet S) :
    avgMap g μ (h ⁻¹' S) = avgMap g μ S := by
  rw [avgMap_apply hg μ (hh hS), avgMap_apply hg μ hS]
  congr 1
  calc ∑ i, μ (g i ⁻¹' (h ⁻¹' S)) = ∑ i, μ (g (σ i) ⁻¹' S) := by
        refine Finset.sum_congr rfl fun i _ => ?_
        rw [← Set.preimage_comp, hσ i]
    _ = ∑ i, μ (g i ⁻¹' S) := Equiv.sum_comp σ (fun i => μ (g i ⁻¹' S))

/-! ## 2.  The symmetry group of `box m` -/

lemma measurable_reflX (m : ℝ) : Measurable (reflX m) := by
  unfold reflX; fun_prop

lemma measurable_swapXY : Measurable swapXY := by
  unfold swapXY; fun_prop

lemma sqGood_reflX (m : ℝ) : SqGood (box m) (reflX m) := by
  intro c θ hS
  refine ⟨reflX m c, -θ, ?_, (sq_subset_box_reflX_iff m c θ).mpr hS⟩
  have := preimage_sq_reflX m (reflX m c) (-θ)
  rwa [reflX_reflX, neg_neg] at this

lemma sqGood_swapXY (m : ℝ) : SqGood (box m) swapXY := by
  intro c θ hS
  refine ⟨swapXY c, -θ, ?_, (sq_subset_box_swapXY_iff m c θ).mpr hS⟩
  have := preimage_sq_swapXY (swapXY c) (-θ)
  rwa [swapXY_swapXY, neg_neg] at this

lemma preimage_box_reflX (m : ℝ) : reflX m ⁻¹' box m = box m := by
  ext p; simp only [Set.mem_preimage, box, reflX, Set.mem_ofPred_eq]
  constructor <;> rintro ⟨h1, h2, h3, h4⟩ <;> refine ⟨?_, ?_, h3, h4⟩ <;> linarith

lemma preimage_box_swapXY (m : ℝ) : swapXY ⁻¹' box m = box m := by
  ext p; simp only [Set.mem_preimage, box, swapXY, Set.mem_ofPred_eq]
  constructor <;> rintro ⟨h1, h2, h3, h4⟩ <;> exact ⟨h3, h4, h1, h2⟩

/-- The eight elements of the symmetry group of `box m`, as words in `r = reflX m`, `s = swapXY`:
`e, r, s, rs, sr, rsr, srs, rsrs`. -/
def d4map (m : ℝ) : Fin 8 → ℝ × ℝ → ℝ × ℝ
  | 0 => id
  | 1 => reflX m
  | 2 => swapXY
  | 3 => reflX m ∘ swapXY
  | 4 => swapXY ∘ reflX m
  | 5 => reflX m ∘ swapXY ∘ reflX m
  | 6 => swapXY ∘ reflX m ∘ swapXY
  | 7 => reflX m ∘ swapXY ∘ reflX m ∘ swapXY

lemma measurable_d4map (m : ℝ) (i : Fin 8) : Measurable (d4map m i) := by
  have hr := measurable_reflX m; have hs := measurable_swapXY
  fin_cases i <;> simp only [d4map] <;> first | exact measurable_id | fun_prop

lemma sqGood_d4map (m : ℝ) (i : Fin 8) : SqGood (box m) (d4map m i) := by
  have hr := sqGood_reflX m; have hs := sqGood_swapXY m
  fin_cases i <;> simp only [d4map]
  · exact sqGood_id _
  · exact hr
  · exact hs
  · exact hr.comp hs
  · exact hs.comp hr
  · exact hr.comp (hs.comp hr)
  · exact hs.comp (hr.comp hs)
  · exact hr.comp (hs.comp (hr.comp hs))

lemma preimage_box_d4map (m : ℝ) (i : Fin 8) : d4map m i ⁻¹' box m = box m := by
  have hr := preimage_box_reflX m; have hs := preimage_box_swapXY m
  fin_cases i <;> simp only [d4map, Set.preimage_id, Set.preimage_comp, hr, hs]

/-- Left multiplication by `r`: `e ↔ r, s ↔ rs, sr ↔ rsr, srs ↔ rsrs` (an involution). -/
def permR : Fin 8 → Fin 8 := ![1, 0, 3, 2, 5, 4, 7, 6]
/-- Left multiplication by `s`: `e ↔ s, r ↔ sr, rs ↔ srs, rsr ↔ rsrs` (uses `srsr = rsrs`). -/
def permS : Fin 8 → Fin 8 := ![2, 4, 0, 6, 1, 7, 3, 5]

lemma permR_invol : Function.Involutive permR := by
  intro i; revert i; decide
lemma permS_invol : Function.Involutive permS := by
  intro i; revert i; decide

lemma reflX_comp_d4map (m : ℝ) (i : Fin 8) : reflX m ∘ d4map m i = d4map m (permR i) := by
  fin_cases i <;> funext p <;>
    simp [d4map, permR, reflX, swapXY, Function.comp]

lemma swapXY_comp_d4map (m : ℝ) (i : Fin 8) : swapXY ∘ d4map m i = d4map m (permS i) := by
  fin_cases i <;> funext p <;>
    simp [d4map, permS, reflX, swapXY, Function.comp]

/-! ## 3.  D4 symmetrisation is free -/

/-- **Symmetrisation is free.**  Every valid cover measure of `box m` has a D4-invariant valid cover
measure of the same total mass (the average of its eight images). -/
theorem exists_d4InvM_cover (m : ℝ) (μ : Measure (ℝ × ℝ)) (hμ : CoverValid (box m) μ) :
    ∃ ν : Measure (ℝ × ℝ), D4InvM m ν ∧ CoverValid (box m) ν ∧ ν (box m) = μ (box m) := by
  have hg := measurable_d4map m
  refine ⟨avgMap (d4map m) μ, ?_, coverValid_avg hg (sqGood_d4map m) hμ, ?_⟩
  · intro S hS
    exact ⟨avgMap_preimage_eq hg (measurable_reflX m) (permR_invol.toPerm _)
        (reflX_comp_d4map m) μ hS,
      avgMap_preimage_eq hg measurable_swapXY (permS_invol.toPerm _) (swapXY_comp_d4map m) μ hS⟩
  · have hbox : MeasurableSet (box m) := by
      unfold box
      exact (measurableSet_le measurable_const measurable_fst).inter
        ((measurableSet_le measurable_fst measurable_const).inter
          ((measurableSet_le measurable_const measurable_snd).inter
            (measurableSet_le measurable_snd measurable_const)))
    exact avgMap_apply_of_preimage hbox hg (preimage_box_d4map m) μ

end SquarePacking
