import Sqpack.S32

/-!
# Lower bounds from measures, and mixed covers (points + segments + polygons)

`packing_le_weight` (`Basic.lean`) bounds a packing by the total weight of a finite weighted point
set that every closed unit square of the container captures with weight `≥ 1`.  The mixed covers
of `certificates/s21/FORMAT.md` also carry mass **uniformly on segments** (by length) and
**uniformly on convex polygons** (by area).  This file does the reduction once for *any* measure,
then specialises.

* `packing_le_measure` — if `μ` is any measure on the plane with `μ(Q) ≥ 1` for every closed unit
  square `Q ⊆ C`, a packing of `n` squares of side `L > 1` in `C` has `n ≤ μ(C)`: the concentric
  closed unit squares are pairwise disjoint (closed) subsets of `C`.
* `not_packs_of_measure` — with the scaling argument: `μ(box m) < n` excludes packing `n` unit
  squares in `box s`, `s < m`.
* `D4InvM`, **`d4_reduction_measure`**, `d4_reduction_measure_u` — the D4 reduction for a measure
  invariant under `x ↦ m − x` and `x ↔ y` (the analogue of `D4.lean` for point sets).
* `MixedCover`, `MixedCover.measure` — the measure of a mixed cover: `∑ w·δ_p` over the points,
  `∑ w·(uniform probability on [a,b])` over the segments (the push-forward of Lebesgue measure on
  `[0,1]` by `t ↦ a + t(b − a)`), `∑ w·(uniform probability on P)` over the polygons (normalised
  restricted Lebesgue measure).  Polygons are arbitrary measurable sets here.
* `MixedCover.measure_apply` — on a measurable set `S` the measure is `ofReal (M.mass S)`, where
  `M.mass S` is the explicit real number: point weights in `S`, plus each segment's weight times the
  fraction of its parameter interval `[0,1]` mapped into `S`, plus each polygon's weight times the
  fraction of its area in `S`.  So a checker's statement "`mass(Q) ≥ 1`" is `μ(Q) ≥ 1`.
* `MixedCover.measure_univ_le` — the total mass is at most the file's total `M.total`
  (with equality, `measure_univ_eq`, when no polygon has zero or infinite area).
* `MixedCover.d4InvM` — D4 invariance of the measure from the entry-level invariance (points and
  weights mapped onto points, segments onto segments in either orientation, polygons onto polygons).
-/

open MeasureTheory Finset
open scoped ENNReal

namespace SquarePacking

/-! ## 1.  Closed squares are measurable -/

lemma continuous_coord (c : ℝ × ℝ) (θ : ℝ) : Continuous (coord c θ) := by
  unfold coord; fun_prop

lemma isClosed_sq (c : ℝ × ℝ) (θ L : ℝ) : IsClosed (sq c θ L) := by
  have h1 : Continuous fun p => |(coord c θ p).1| := (continuous_coord c θ).fst.abs
  have h2 : Continuous fun p => |(coord c θ p).2| := (continuous_coord c θ).snd.abs
  have e : sq c θ L = {p | |(coord c θ p).1| ≤ L / 2} ∩ {p | |(coord c θ p).2| ≤ L / 2} := rfl
  rw [e]
  exact (isClosed_le h1 continuous_const).inter (isClosed_le h2 continuous_const)

lemma measurableSet_sq (c : ℝ × ℝ) (θ L : ℝ) : MeasurableSet (sq c θ L) :=
  (isClosed_sq c θ L).measurableSet

/-! ## 2.  The reduction for measures -/

/-- **Main reduction, for measures.**  If every closed unit square inside `C` has `μ`-measure
`≥ 1`, then any family of `n` squares of side `L > 1` inside `C` with pairwise disjoint interiors
has `n ≤ μ(C)`.  (`packing_le_weight` is the case of a finite sum of weighted Dirac masses.) -/
theorem packing_le_measure (μ : Measure (ℝ × ℝ)) (C : Set (ℝ × ℝ))
    (hcover : ∀ (c : ℝ × ℝ) (θ : ℝ), sq c θ 1 ⊆ C → 1 ≤ μ (sq c θ 1))
    (n : ℕ) (L : ℝ) (hL : 1 < L) (ctr : Fin n → ℝ × ℝ) (ang : Fin n → ℝ)
    (hin : ∀ i, sq (ctr i) (ang i) L ⊆ C)
    (hdisj : ∀ i j, i ≠ j → Disjoint (sqInt (ctr i) (ang i) L) (sqInt (ctr j) (ang j) L)) :
    (n : ℝ≥0∞) ≤ μ C := by
  have hIntSub : ∀ (c : ℝ × ℝ) (θ : ℝ), sqInt c θ L ⊆ sq c θ L := by
    rintro c θ p ⟨h1, h2⟩; exact ⟨le_of_lt h1, le_of_lt h2⟩
  have hU : ∀ i, sq (ctr i) (ang i) 1 ⊆ C := fun i =>
    subset_trans (subset_trans (unit_subset_interior hL) (hIntSub _ _)) (hin i)
  set S : Fin n → Set (ℝ × ℝ) := fun i => sq (ctr i) (ang i) 1 with hSdef
  have hSdisj : ((univ : Finset (Fin n)) : Set (Fin n)).PairwiseDisjoint S := by
    intro i _ j _ hij
    exact Set.disjoint_of_subset (unit_subset_interior hL) (unit_subset_interior hL)
      (hdisj i j hij)
  calc (n : ℝ≥0∞) = ∑ _i : Fin n, (1 : ℝ≥0∞) := by simp
    _ ≤ ∑ i : Fin n, μ (S i) := Finset.sum_le_sum fun i _ => hcover _ _ (hU i)
    _ = μ (⋃ i ∈ (univ : Finset (Fin n)), S i) :=
        (measure_biUnion_finset hSdisj fun i _ => measurableSet_sq _ _ _).symm
    _ ≤ μ C := measure_mono (Set.iUnion₂_subset fun i _ => hU i)

/-- **Lower bounds from a measure.**  If every closed unit square inside `box m` has `μ`-measure
`≥ 1` and `μ(box m) < n`, then `n` unit squares cannot be packed in `box s` for any `s < m`
(scale such a packing by `m/s > 1` and apply `packing_le_measure`). -/
theorem not_packs_of_measure (m : ℝ) (μ : Measure (ℝ × ℝ))
    (hcover : ∀ (c : ℝ × ℝ) (θ : ℝ), sq c θ 1 ⊆ box m → 1 ≤ μ (sq c θ 1))
    (n : ℕ) (htot : μ (box m) < n) {s : ℝ} (hs : s < m) : ¬ Packs n s := by
  rintro ⟨ctr, ang, hin, hdisj⟩
  rcases Nat.eq_zero_or_pos n with rfl | hn
  · simp at htot
  have hs1 : 1 ≤ s := by
    obtain ⟨h1, h2, _, _⟩ := (sq_subset_box_iff s _ _).mp (hin ⟨0, hn⟩)
    linarith [one_le_wid (ang ⟨0, hn⟩)]
  have hs0 : 0 < s := by linarith
  set k := m / s with hkdef
  have hk : 1 < k := (one_lt_div hs0).mpr hs
  have hk0 : 0 < k := by linarith
  have hks : k * s = m := by rw [hkdef]; field_simp
  have h := packing_le_measure μ (box m) hcover n k hk
    (fun i => (k * (ctr i).1, k * (ctr i).2)) ang ?_ ?_
  · exact absurd h (not_le.mpr htot)
  · intro i q hq
    rw [mem_sq_scale_iff hk0] at hq
    obtain ⟨h1, h2, h3, h4⟩ := hin i hq
    simp only at h1 h2 h3 h4
    have e1 : q.1 = k * (q.1 / k) := by field_simp
    have e2 : q.2 = k * (q.2 / k) := by field_simp
    refine ⟨?_, ?_, ?_, ?_⟩
    · rw [e1]; positivity
    · rw [e1, ← hks]; exact mul_le_mul_of_nonneg_left h2 hk0.le
    · rw [e2]; positivity
    · rw [e2, ← hks]; exact mul_le_mul_of_nonneg_left h4 hk0.le
  · intro i j hij
    rw [Set.disjoint_left]
    intro q hqi hqj
    rw [mem_sqInt_scale_iff hk0] at hqi hqj
    exact Set.disjoint_left.mp (hdisj i j hij) hqi hqj

/-! ## 3.  The D4 reduction for measures -/

/-- **D4 invariance of a measure**, on the two generators `x ↦ m − x` and `x ↔ y` of the symmetry
group of `box m`. -/
def D4InvM (m : ℝ) (μ : Measure (ℝ × ℝ)) : Prop :=
  ∀ s : Set (ℝ × ℝ), MeasurableSet s → μ (reflX m ⁻¹' s) = μ s ∧ μ (swapXY ⁻¹' s) = μ s

lemma preimage_sq_reflX (m : ℝ) (c : ℝ × ℝ) (θ : ℝ) :
    reflX m ⁻¹' sq (reflX m c) (-θ) 1 = sq c θ 1 := by
  ext p; exact mem_sq_reflX m c θ p

lemma preimage_sq_swapXY (c : ℝ × ℝ) (θ : ℝ) :
    swapXY ⁻¹' sq (swapXY c) (-θ) 1 = sq c θ 1 := by
  ext p; exact mem_sq_swapXY c θ p

lemma measure_sq_reflX {m : ℝ} {μ : Measure (ℝ × ℝ)} (h : D4InvM m μ) (c : ℝ × ℝ) (θ : ℝ) :
    μ (sq (reflX m c) (-θ) 1) = μ (sq c θ 1) := by
  rw [← (h _ (measurableSet_sq _ _ _)).1, preimage_sq_reflX]

lemma measure_sq_swapXY {m : ℝ} {μ : Measure (ℝ × ℝ)} (h : D4InvM m μ) (c : ℝ × ℝ) (θ : ℝ) :
    μ (sq (swapXY c) (-θ) 1) = μ (sq c θ 1) := by
  rw [← (h _ (measurableSet_sq _ _ _)).2, preimage_sq_swapXY]

/-- **D4 reduction for measures.**  If `μ` is invariant under `x ↦ m − x` and `x ↔ y`, and every
closed unit square inside `box m` with centre in `[0,m/2]²` and angle in `[0, π/4]` has measure
`≥ 1`, then every closed unit square inside `box m` has measure `≥ 1`. -/
theorem d4_reduction_measure (m : ℝ) (μ : Measure (ℝ × ℝ)) (hinv : D4InvM m μ)
    (hreg : ∀ (c : ℝ × ℝ) (θ : ℝ), c.1 ∈ Set.Icc 0 (m / 2) → c.2 ∈ Set.Icc 0 (m / 2) →
      θ ∈ Set.Icc 0 (Real.pi / 4) → sq c θ 1 ⊆ box m → 1 ≤ μ (sq c θ 1)) :
    ∀ (c : ℝ × ℝ) (θ : ℝ), sq c θ 1 ⊆ box m → 1 ≤ μ (sq c θ 1) := by
  let P : ℝ × ℝ → ℝ → Prop := fun c θ => sq c θ 1 ⊆ box m → 1 ≤ μ (sq c θ 1)
  have hP : ∀ c ∈ box m, ∀ θ, P c θ := by
    refine d4_reduce m P ?_ ?_ ?_ ?_
    · intro c θ
      simp only [P, sq_add_pi_div_two]
    · intro c θ h hsub
      rw [measure_sq_reflX hinv]
      exact h ((sq_subset_box_reflX_iff m c θ).mp hsub)
    · intro c θ h hsub
      rw [measure_sq_swapXY hinv]
      exact h ((sq_subset_box_swapXY_iff m c θ).mp hsub)
    · intro c θ h1 h2 h3 hsub
      exact hreg c θ h1 h2 h3 hsub
  intro c θ hsub
  exact hP c (hsub (mem_sq_self c θ)) θ hsub

/-- **D4 reduction for measures, in the checkers' coordinates** (`θ = 2 arctan u`,
`u ∈ [0, 1/2]`, a larger angle range than `[0, π/4]`). -/
theorem d4_reduction_measure_u (m : ℝ) (μ : Measure (ℝ × ℝ)) (hinv : D4InvM m μ)
    (hreg : ∀ (c : ℝ × ℝ) (u : ℝ), c.1 ∈ Set.Icc 0 (m / 2) → c.2 ∈ Set.Icc 0 (m / 2) →
      u ∈ Set.Icc 0 (1 / 2) → sq c (2 * Real.arctan u) 1 ⊆ box m →
        1 ≤ μ (sq c (2 * Real.arctan u) 1)) :
    ∀ (c : ℝ × ℝ) (θ : ℝ), sq c θ 1 ⊆ box m → 1 ≤ μ (sq c θ 1) := by
  refine d4_reduction_measure m μ hinv fun c θ h1 h2 hθ hsub => ?_
  obtain ⟨u, hu, rfl⟩ := exists_u_of_theta hθ
  exact hreg c u h1 h2 hu hsub

/-! ## 4.  Segments and regions -/

/-- The point of parameter `t` on the segment from `a` to `b`. -/
def segPt (a b : ℝ × ℝ) (t : ℝ) : ℝ × ℝ := (a.1 + t * (b.1 - a.1), a.2 + t * (b.2 - a.2))

lemma continuous_segPt (a b : ℝ × ℝ) : Continuous (segPt a b) := by
  unfold segPt; fun_prop

lemma measurable_segPt (a b : ℝ × ℝ) : Measurable (segPt a b) :=
  (continuous_segPt a b).measurable

/-- The uniform probability measure on the closed segment `[a, b]` (by length, when `a ≠ b`): the
push-forward of Lebesgue measure on `[0,1]` by `t ↦ a + t(b − a)`. -/
noncomputable def segMeasure (a b : ℝ × ℝ) : Measure (ℝ × ℝ) :=
  (volume.restrict (Set.Icc (0 : ℝ) 1)).map (segPt a b)

/-- The fraction of the segment `[a, b]` lying in `S`: the Lebesgue measure of the parameters
`t ∈ [0,1]` with `a + t(b − a) ∈ S`.  For a convex `S` (a closed square) and `a ≠ b` it is
`|[a,b] ∩ S| / |[a,b]|`, the checkers' "parametric fraction". -/
noncomputable def segFrac (a b : ℝ × ℝ) (S : Set (ℝ × ℝ)) : ℝ :=
  (volume (segPt a b ⁻¹' S ∩ Set.Icc (0 : ℝ) 1)).toReal

lemma volume_Icc01 : volume (Set.Icc (0 : ℝ) 1) = 1 := by simp [Real.volume_Icc]

lemma segMeasure_apply (a b : ℝ × ℝ) {S : Set (ℝ × ℝ)} (hS : MeasurableSet S) :
    segMeasure a b S = volume (segPt a b ⁻¹' S ∩ Set.Icc (0 : ℝ) 1) := by
  rw [segMeasure, Measure.map_apply (measurable_segPt a b) hS,
    Measure.restrict_apply (measurable_segPt a b hS)]

lemma segMeasure_univ (a b : ℝ × ℝ) : segMeasure a b Set.univ = 1 := by
  rw [segMeasure_apply a b MeasurableSet.univ, Set.preimage_univ, Set.univ_inter, volume_Icc01]

lemma segMeasure_le_one (a b : ℝ × ℝ) (S : Set (ℝ × ℝ)) : segMeasure a b S ≤ 1 :=
  (measure_mono (Set.subset_univ S)).trans (segMeasure_univ a b).le

lemma segMeasure_ne_top (a b : ℝ × ℝ) (S : Set (ℝ × ℝ)) : segMeasure a b S ≠ ⊤ :=
  ne_top_of_le_ne_top ENNReal.one_ne_top (segMeasure_le_one a b S)

lemma segMeasure_apply_eq (a b : ℝ × ℝ) {S : Set (ℝ × ℝ)} (hS : MeasurableSet S) :
    segMeasure a b S = ENNReal.ofReal (segFrac a b S) := by
  rw [segFrac, ← segMeasure_apply a b hS, ENNReal.ofReal_toReal (segMeasure_ne_top a b S)]

/-- The segment measure does not depend on the orientation. -/
lemma segMeasure_comm (a b : ℝ × ℝ) : segMeasure b a = segMeasure a b := by
  have hmp : MeasurePreserving (fun t : ℝ => 1 - t) volume volume :=
    Measure.measurePreserving_sub_left volume 1
  have hpre : (fun t : ℝ => 1 - t) ⁻¹' Set.Icc 0 1 = Set.Icc 0 1 := by
    ext t; simp only [Set.mem_preimage, Set.mem_Icc]; constructor <;> intro h <;> constructor <;>
      linarith [h.1, h.2]
  have hmp' := hmp.restrict_preimage (measurableSet_Icc (a := (0 : ℝ)) (b := 1))
  rw [hpre] at hmp'
  have e : segPt b a = segPt a b ∘ (fun t : ℝ => 1 - t) := by
    funext t; simp only [segPt, Function.comp]; ext <;> ring
  rw [segMeasure, segMeasure, e, ← Measure.map_map (measurable_segPt a b) hmp.measurable,
    hmp'.map_eq]

/-- `segFrac` does not depend on the orientation of the segment (for a measurable set). -/
lemma segFrac_comm (a b : ℝ × ℝ) {S : Set (ℝ × ℝ)} (hS : MeasurableSet S) :
    segFrac b a S = segFrac a b S := by
  rw [segFrac, segFrac, ← segMeasure_apply b a hS, ← segMeasure_apply a b hS, segMeasure_comm]

/-- The uniform probability measure on a region `P` (by area, when `0 < area P < ∞`). -/
noncomputable def areaMeasure (P : Set (ℝ × ℝ)) : Measure (ℝ × ℝ) :=
  (volume P)⁻¹ • volume.restrict P

/-- The fraction of the area of `P` lying in `S` (`0` if `P` has zero or infinite area). -/
noncomputable def areaFrac (P S : Set (ℝ × ℝ)) : ℝ :=
  ((volume P)⁻¹ * volume (S ∩ P)).toReal

lemma inv_mul_self_le_one (x : ℝ≥0∞) : x⁻¹ * x ≤ 1 := by
  have h := ENNReal.mul_div_le (a := x) (b := 1)
  rwa [one_div, mul_comm] at h

lemma areaMeasure_apply (P : Set (ℝ × ℝ)) {S : Set (ℝ × ℝ)} (hS : MeasurableSet S) :
    areaMeasure P S = (volume P)⁻¹ * volume (S ∩ P) := by
  rw [areaMeasure, Measure.smul_apply, Measure.restrict_apply hS, smul_eq_mul]

lemma areaMeasure_univ_le (P : Set (ℝ × ℝ)) : areaMeasure P Set.univ ≤ 1 := by
  rw [areaMeasure_apply P MeasurableSet.univ, Set.univ_inter]; exact inv_mul_self_le_one _

lemma areaMeasure_univ (P : Set (ℝ × ℝ)) (h0 : volume P ≠ 0) (htop : volume P ≠ ⊤) :
    areaMeasure P Set.univ = 1 := by
  rw [areaMeasure_apply P MeasurableSet.univ, Set.univ_inter, ENNReal.inv_mul_cancel h0 htop]

lemma areaMeasure_ne_top (P S : Set (ℝ × ℝ)) : areaMeasure P S ≠ ⊤ :=
  ne_top_of_le_ne_top ENNReal.one_ne_top
    ((measure_mono (Set.subset_univ S)).trans (areaMeasure_univ_le P))

lemma areaMeasure_apply_eq (P : Set (ℝ × ℝ)) {S : Set (ℝ × ℝ)} (hS : MeasurableSet S) :
    areaMeasure P S = ENNReal.ofReal (areaFrac P S) := by
  rw [areaFrac, ← areaMeasure_apply P hS, ENNReal.ofReal_toReal (areaMeasure_ne_top P S)]

/-- `areaFrac` is the area ratio (both sides are `0` for zero or infinite area). -/
lemma areaFrac_eq (P S : Set (ℝ × ℝ)) :
    areaFrac P S = (volume (S ∩ P)).toReal / (volume P).toReal := by
  rw [areaFrac, ENNReal.toReal_mul, ENNReal.toReal_inv, div_eq_inv_mul]

/-! ## 5.  Mixed covers -/

/-- A mixed cover (FORMAT.md v1, over the reals): finitely many weighted points, segments
`[sa j, sb j]` carrying mass `sw j` uniformly by length, and regions `poly k` (convex polygons in
the file) carrying mass `gw k` uniformly by area.  The index types are arbitrary. -/
structure MixedCover (ι κ ν : Type*) where
  /-- the point entries -/
  pts : Finset ι
  pt : ι → ℝ × ℝ
  pw : ι → ℝ
  /-- the segment entries -/
  segs : Finset κ
  sa : κ → ℝ × ℝ
  sb : κ → ℝ × ℝ
  sw : κ → ℝ
  /-- the polygon entries -/
  polys : Finset ν
  poly : ν → Set (ℝ × ℝ)
  gw : ν → ℝ

namespace MixedCover

variable {ι κ ν : Type*} (M : MixedCover ι κ ν)

/-- The measure of the cover. -/
noncomputable def measure : Measure (ℝ × ℝ) :=
  (∑ i ∈ M.pts, ENNReal.ofReal (M.pw i) • Measure.dirac (M.pt i))
    + (∑ j ∈ M.segs, ENNReal.ofReal (M.sw j) • segMeasure (M.sa j) (M.sb j))
    + (∑ k ∈ M.polys, ENNReal.ofReal (M.gw k) • areaMeasure (M.poly k))

/-- The file's total: the sum of all the masses. -/
noncomputable def total : ℝ :=
  (∑ i ∈ M.pts, M.pw i) + (∑ j ∈ M.segs, M.sw j) + ∑ k ∈ M.polys, M.gw k

open Classical in
/-- The mass in a set `S`, as an explicit real number. -/
noncomputable def mass (S : Set (ℝ × ℝ)) : ℝ :=
  (∑ i ∈ M.pts.filter (fun i => M.pt i ∈ S), M.pw i)
    + (∑ j ∈ M.segs, M.sw j * segFrac (M.sa j) (M.sb j) S)
    + ∑ k ∈ M.polys, M.gw k * areaFrac (M.poly k) S

/-- Non-negative masses. -/
def Nonneg : Prop :=
  (∀ i ∈ M.pts, 0 ≤ M.pw i) ∧ (∀ j ∈ M.segs, 0 ≤ M.sw j) ∧ (∀ k ∈ M.polys, 0 ≤ M.gw k)

lemma measure_apply' (S : Set (ℝ × ℝ)) :
    M.measure S = (∑ i ∈ M.pts, ENNReal.ofReal (M.pw i) * Measure.dirac (M.pt i) S)
      + (∑ j ∈ M.segs, ENNReal.ofReal (M.sw j) * segMeasure (M.sa j) (M.sb j) S)
      + ∑ k ∈ M.polys, ENNReal.ofReal (M.gw k) * areaMeasure (M.poly k) S := by
  simp only [measure, Measure.add_apply, Measure.finsetSum_apply, Measure.smul_apply, smul_eq_mul]

open Classical in
/-- **The measure of a measurable set is the explicit mass.** -/
theorem measure_apply (hM : M.Nonneg) {S : Set (ℝ × ℝ)} (hS : MeasurableSet S) :
    M.measure S = ENNReal.ofReal (M.mass S) := by
  obtain ⟨hp, hs, hg⟩ := hM
  rw [measure_apply', mass]
  have h1 : 0 ≤ ∑ i ∈ M.pts.filter (fun i => M.pt i ∈ S), M.pw i :=
    Finset.sum_nonneg fun i hi => hp i (Finset.mem_filter.mp hi).1
  have h2 : 0 ≤ ∑ j ∈ M.segs, M.sw j * segFrac (M.sa j) (M.sb j) S :=
    Finset.sum_nonneg fun j hj => mul_nonneg (hs j hj) ENNReal.toReal_nonneg
  have h3 : 0 ≤ ∑ k ∈ M.polys, M.gw k * areaFrac (M.poly k) S :=
    Finset.sum_nonneg fun k hk => mul_nonneg (hg k hk) ENNReal.toReal_nonneg
  rw [ENNReal.ofReal_add (add_nonneg h1 h2) h3, ENNReal.ofReal_add h1 h2,
    ENNReal.ofReal_sum_of_nonneg (fun i hi => hp i (Finset.mem_filter.mp hi).1),
    ENNReal.ofReal_sum_of_nonneg (f := fun j => M.sw j * segFrac (M.sa j) (M.sb j) S)
      (fun j hj => mul_nonneg (hs j hj) ENNReal.toReal_nonneg),
    ENNReal.ofReal_sum_of_nonneg (f := fun k => M.gw k * areaFrac (M.poly k) S)
      (fun k hk => mul_nonneg (hg k hk) ENNReal.toReal_nonneg)]
  refine congrArg₂ (· + ·) (congrArg₂ (· + ·) ?_ ?_) ?_
  · rw [Finset.sum_filter]
    refine Finset.sum_congr rfl fun i _ => ?_
    rw [Measure.dirac_apply' _ hS]
    by_cases h : M.pt i ∈ S <;> simp [h]
  · refine Finset.sum_congr rfl fun j hj => ?_
    rw [ENNReal.ofReal_mul (hs j hj), segMeasure_apply_eq _ _ hS]
  · refine Finset.sum_congr rfl fun k hk => ?_
    rw [ENNReal.ofReal_mul (hg k hk), areaMeasure_apply_eq _ hS]

/-- **The total mass is at most the file's total.** -/
theorem measure_univ_le (hM : M.Nonneg) : M.measure Set.univ ≤ ENNReal.ofReal M.total := by
  obtain ⟨hp, hs, hg⟩ := hM
  rw [measure_apply', total,
    ENNReal.ofReal_add (add_nonneg (Finset.sum_nonneg hp) (Finset.sum_nonneg hs))
      (Finset.sum_nonneg hg),
    ENNReal.ofReal_add (Finset.sum_nonneg hp) (Finset.sum_nonneg hs),
    ENNReal.ofReal_sum_of_nonneg hp, ENNReal.ofReal_sum_of_nonneg hs,
    ENNReal.ofReal_sum_of_nonneg hg]
  gcongr with i _ j _ k _
  · simp
  · simp [segMeasure_univ]
  · exact mul_le_of_le_one_right' (areaMeasure_univ_le _)

/-- With no degenerate polygon, the total mass *is* the file's total. -/
theorem measure_univ_eq (hM : M.Nonneg)
    (hpoly : ∀ k ∈ M.polys, volume (M.poly k) ≠ 0 ∧ volume (M.poly k) ≠ ⊤) :
    M.measure Set.univ = ENNReal.ofReal M.total := by
  obtain ⟨hp, hs, hg⟩ := hM
  rw [measure_apply', total,
    ENNReal.ofReal_add (add_nonneg (Finset.sum_nonneg hp) (Finset.sum_nonneg hs))
      (Finset.sum_nonneg hg),
    ENNReal.ofReal_add (Finset.sum_nonneg hp) (Finset.sum_nonneg hs),
    ENNReal.ofReal_sum_of_nonneg hp, ENNReal.ofReal_sum_of_nonneg hs,
    ENNReal.ofReal_sum_of_nonneg hg]
  congr 1
  · congr 1
    · refine Finset.sum_congr rfl fun i _ => ?_; simp
    · refine Finset.sum_congr rfl fun j _ => ?_; simp [segMeasure_univ]
  · refine Finset.sum_congr rfl fun k hk => ?_
    rw [areaMeasure_univ _ (hpoly k hk).1 (hpoly k hk).2, mul_one]

/-! ### Invariance under an involution of the plane -/

/-- The segment measure transported by a map that is affine on segments. -/
lemma segMeasure_preimage (g : ℝ × ℝ → ℝ × ℝ) (hg : Measurable g)
    (haff : ∀ a b t, g (segPt a b t) = segPt (g a) (g b) t) (a b : ℝ × ℝ)
    {s : Set (ℝ × ℝ)} (hs : MeasurableSet s) :
    segMeasure a b (g ⁻¹' s) = segMeasure (g a) (g b) s := by
  rw [segMeasure_apply _ _ (hg hs), segMeasure_apply _ _ hs, ← Set.preimage_comp]
  congr 3
  funext t
  exact haff a b t

/-- The area measure transported by a measure-preserving involution. -/
lemma areaMeasure_preimage (g : ℝ × ℝ → ℝ × ℝ) (hgg : ∀ p, g (g p) = p)
    (hmp : MeasurePreserving g volume volume) (P : Set (ℝ × ℝ)) (hP : MeasurableSet P)
    {s : Set (ℝ × ℝ)} (hs : MeasurableSet s) :
    areaMeasure P (g ⁻¹' s) = areaMeasure (g ⁻¹' P) s := by
  have hinvP : g ⁻¹' (g ⁻¹' P) = P := by ext p; simp [hgg]
  have hP' : MeasurableSet (g ⁻¹' P) := hmp.measurable hP
  rw [areaMeasure_apply _ (hmp.measurable hs), areaMeasure_apply _ hs]
  have e1 : volume (g ⁻¹' P) = volume P := hmp.measure_preimage hP.nullMeasurableSet
  have e2 : g ⁻¹' s ∩ P = g ⁻¹' (s ∩ g ⁻¹' P) := by
    rw [Set.preimage_inter, hinvP]
  rw [e1, e2, hmp.measure_preimage (hs.inter hP').nullMeasurableSet]

/-- **Invariance of the measure** under an involution `g` of the plane that is affine on segments
and preserves area, given entry-level involutions: `gp` maps points to points (with `g`, keeping
weights), `gs` maps segments to segments (endpoints moved by `g`, in either order, weights kept),
`gq` maps polygons to polygons (`poly (gq k) = g⁻¹' poly k = g '' poly k`, weights kept). -/
theorem measure_preimage_invol (g : ℝ × ℝ → ℝ × ℝ) (hgg : ∀ p, g (g p) = p)
    (haff : ∀ a b t, g (segPt a b t) = segPt (g a) (g b) t)
    (hmp : MeasurePreserving g volume volume)
    (hpolyM : ∀ k ∈ M.polys, MeasurableSet (M.poly k))
    (gp : ι → ι) (gs : κ → κ) (gq : ν → ν)
    (hp : ∀ i ∈ M.pts, gp i ∈ M.pts ∧ M.pt (gp i) = g (M.pt i) ∧ M.pw (gp i) = M.pw i ∧
      gp (gp i) = i)
    (hs : ∀ j ∈ M.segs, gs j ∈ M.segs ∧ M.sw (gs j) = M.sw j ∧ gs (gs j) = j ∧
      ((M.sa (gs j) = g (M.sa j) ∧ M.sb (gs j) = g (M.sb j)) ∨
        (M.sa (gs j) = g (M.sb j) ∧ M.sb (gs j) = g (M.sa j))))
    (hq : ∀ k ∈ M.polys, gq k ∈ M.polys ∧ M.gw (gq k) = M.gw k ∧ gq (gq k) = k ∧
      M.poly (gq k) = g ⁻¹' M.poly k)
    {s : Set (ℝ × ℝ)} (hsm : MeasurableSet s) :
    M.measure (g ⁻¹' s) = M.measure s := by
  have hg : Measurable g := hmp.measurable
  rw [measure_apply', measure_apply']
  refine congrArg₂ (· + ·) (congrArg₂ (· + ·) ?_ ?_) ?_
  · refine Finset.sum_nbij' gp gp (fun i hi => (hp i hi).1) (fun i hi => (hp i hi).1)
      (fun i hi => (hp i hi).2.2.2) (fun i hi => (hp i hi).2.2.2) fun i hi => ?_
    rw [(hp i hi).2.2.1, (hp i hi).2.1, ← Measure.map_apply hg hsm, Measure.map_dirac' hg]
  · refine Finset.sum_nbij' gs gs (fun j hj => (hs j hj).1) (fun j hj => (hs j hj).1)
      (fun j hj => (hs j hj).2.2.1) (fun j hj => (hs j hj).2.2.1) fun j hj => ?_
    rw [(hs j hj).2.1, segMeasure_preimage g hg haff _ _ hsm]
    rcases (hs j hj).2.2.2 with ⟨ha, hb⟩ | ⟨ha, hb⟩
    · rw [ha, hb]
    · rw [ha, hb, segMeasure_comm]
  · refine Finset.sum_nbij' gq gq (fun k hk => (hq k hk).1) (fun k hk => (hq k hk).1)
      (fun k hk => (hq k hk).2.2.1) (fun k hk => (hq k hk).2.2.1) fun k hk => ?_
    rw [(hq k hk).2.1, (hq k hk).2.2.2, areaMeasure_preimage g hgg hmp _ (hpolyM k hk) hsm]

end MixedCover

/-! ### The two generators of D4 -/

lemma measurePreserving_reflX (m : ℝ) : MeasurePreserving (reflX m) volume volume := by
  have h := (Measure.measurePreserving_sub_left (volume : Measure ℝ) m).prod
    (MeasurePreserving.id (volume : Measure ℝ))
  rw [← Measure.volume_eq_prod] at h
  exact h

lemma measurePreserving_swapXY : MeasurePreserving swapXY volume volume := by
  have h := Measure.measurePreserving_swap (μ := (volume : Measure ℝ)) (ν := (volume : Measure ℝ))
  rw [← Measure.volume_eq_prod] at h
  exact h

lemma reflX_segPt (m : ℝ) (a b : ℝ × ℝ) (t : ℝ) :
    reflX m (segPt a b t) = segPt (reflX m a) (reflX m b) t := by
  simp only [reflX, segPt]; ext
  · simp only; ring
  · simp only

lemma swapXY_segPt (a b : ℝ × ℝ) (t : ℝ) :
    swapXY (segPt a b t) = segPt (swapXY a) (swapXY b) t := rfl

namespace MixedCover

variable {ι κ ν : Type*} (M : MixedCover ι κ ν)

/-- **D4 invariance of a mixed cover's measure**, from entry-level invariance under `x ↦ m − x`
(`gpX`, `gsX`, `gqX`) and `x ↔ y` (`gpS`, `gsS`, `gqS`). -/
theorem d4InvM (m : ℝ) (hpolyM : ∀ k ∈ M.polys, MeasurableSet (M.poly k))
    (gpX gpS : ι → ι) (gsX gsS : κ → κ) (gqX gqS : ν → ν)
    (hpX : ∀ i ∈ M.pts, gpX i ∈ M.pts ∧ M.pt (gpX i) = reflX m (M.pt i) ∧ M.pw (gpX i) = M.pw i ∧
      gpX (gpX i) = i)
    (hsX : ∀ j ∈ M.segs, gsX j ∈ M.segs ∧ M.sw (gsX j) = M.sw j ∧ gsX (gsX j) = j ∧
      ((M.sa (gsX j) = reflX m (M.sa j) ∧ M.sb (gsX j) = reflX m (M.sb j)) ∨
        (M.sa (gsX j) = reflX m (M.sb j) ∧ M.sb (gsX j) = reflX m (M.sa j))))
    (hqX : ∀ k ∈ M.polys, gqX k ∈ M.polys ∧ M.gw (gqX k) = M.gw k ∧ gqX (gqX k) = k ∧
      M.poly (gqX k) = reflX m ⁻¹' M.poly k)
    (hpS : ∀ i ∈ M.pts, gpS i ∈ M.pts ∧ M.pt (gpS i) = swapXY (M.pt i) ∧ M.pw (gpS i) = M.pw i ∧
      gpS (gpS i) = i)
    (hsS : ∀ j ∈ M.segs, gsS j ∈ M.segs ∧ M.sw (gsS j) = M.sw j ∧ gsS (gsS j) = j ∧
      ((M.sa (gsS j) = swapXY (M.sa j) ∧ M.sb (gsS j) = swapXY (M.sb j)) ∨
        (M.sa (gsS j) = swapXY (M.sb j) ∧ M.sb (gsS j) = swapXY (M.sa j))))
    (hqS : ∀ k ∈ M.polys, gqS k ∈ M.polys ∧ M.gw (gqS k) = M.gw k ∧ gqS (gqS k) = k ∧
      M.poly (gqS k) = swapXY ⁻¹' M.poly k) :
    D4InvM m M.measure := fun _ hs =>
  ⟨M.measure_preimage_invol (reflX m) (reflX_reflX m) (reflX_segPt m) (measurePreserving_reflX m)
      hpolyM gpX gsX gqX hpX hsX hqX hs,
   M.measure_preimage_invol swapXY swapXY_swapXY swapXY_segPt measurePreserving_swapXY
      hpolyM gpS gsS gqS hpS hsS hqS hs⟩

end MixedCover

end SquarePacking
