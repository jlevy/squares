import Sqpack.MixedMeasure
import Sqpack.S21Data

/-!
# `s(21) = 5`, from one computational hypothesis

The lower bound comes from a **mixed cover** of `[0,5]²` (`certificates/s21/FORMAT.md`,
`certificates/s21/s21_mixed_cover_5.txt`): 7,536 point masses and 1,872 segments carrying mass
uniformly by length, total `2089474919732 / 10¹¹ = 20.8947… < 21`.  Its measure `μ`
(`MixedCover.measure`) gives every closed unit square in `[0,5]²` mass `≥ 1`; the checker
`search/zm_mixed.py` establishes that on the D4 fundamental region.

* `S21Data.check_ok`, `S21Data.total_lt`, `S21Data.d4` — **proved in Lean** (kernel evaluation,
  `decide +kernel`, no `native_decide`) for the cover transcribed into `Sqpack/S21Data.lean`: its
  total is `< 21`, and its measure is invariant under `x ↦ 5 − x` and `x ↔ y`.
* `S21RegionCover` — **the one hypothesis**: every closed unit square in `[0,5]²` with centre in
  `[0,5/2]²` and angle in `[0, π/4]` gets mass `≥ 1` (points inside it, plus each segment's mass
  times the fraction of the segment inside it).  `S21CheckerCover` is the same over the checker's
  angle range `θ = 2 arctan u`, `u ∈ [0, 1/2]`; it is what the `zm_mixed.py` D4 run certifies.
* **`s21_eq_five`**, **`s21_eq_five_of_checker`** — `minSide 21 = 5`; `s21_packs` (the upper bound,
  5 × 5 grid) needs no hypothesis.
-/

open MeasureTheory Finset
open scoped ENNReal

namespace SquarePacking

namespace S21Data

/-! ## 1.  The cover -/

/-- The point entries `(X, Y, w)`. -/
def pentries : Finset (ℕ × ℕ × ℕ) := ptree.toList.toFinset

/-- The segment entries `(X0, Y0, X1, Y1, w)`. -/
def sentries : Finset SegE := stree.toList.toFinset

/-- The point of a point entry: `(X/1000, Y/1000)`. -/
noncomputable def pt (e : ℕ × ℕ × ℕ) : ℝ × ℝ := ((e.1 : ℝ) / 1000, (e.2.1 : ℝ) / 1000)

/-- The mass of a point entry: `w/10¹¹`. -/
noncomputable def pw (e : ℕ × ℕ × ℕ) : ℝ := (e.2.2 : ℝ) / 100000000000

/-- The endpoints of a segment entry: `(X0/1000, Y0/1000)` and `(X1/1000, Y1/1000)`. -/
noncomputable def sa (e : SegE) : ℝ × ℝ := ((e.1 : ℝ) / 1000, (e.2.1 : ℝ) / 1000)
noncomputable def sb (e : SegE) : ℝ × ℝ := ((e.2.2.1 : ℝ) / 1000, (e.2.2.2.1 : ℝ) / 1000)

/-- The mass of a segment entry: `w/10¹¹`. -/
noncomputable def sw (e : SegE) : ℝ := (e.2.2.2.2 : ℝ) / 100000000000

/-- The cover as a `MixedCover` (no polygons). -/
noncomputable def cover : MixedCover (ℕ × ℕ × ℕ) SegE Empty where
  pts := pentries
  pt := pt
  pw := pw
  segs := sentries
  sa := sa
  sb := sb
  sw := sw
  polys := ∅
  poly := fun _ => ∅
  gw := fun _ => 0

/-- **The measure of the cover.** -/
noncomputable def μ : Measure (ℝ × ℝ) := cover.measure

/-! ## 2.  Facts about the data, by kernel evaluation -/

/-- The integer images of entries under `x ↦ 5 − x` and `x ↔ y` (segments re-normalised). -/
def pX (e : ℕ × ℕ × ℕ) : ℕ × ℕ × ℕ := (5000 - e.1, e.2.1, e.2.2)
def pS (e : ℕ × ℕ × ℕ) : ℕ × ℕ × ℕ := (e.2.1, e.1, e.2.2)
def sX (e : SegE) : SegE := segNorm (5000 - e.1, e.2.1, 5000 - e.2.2.1, e.2.2.2.1, e.2.2.2.2)
def sS (e : SegE) : SegE := segNorm (e.2.1, e.1, e.2.2.2.1, e.2.2.1, e.2.2.2.2)

/-- The data checks: keys strictly increasing in both trees (no repeated entry); every point has
`X ≤ 5000` and its two reflections, with the same mass, are points; every segment is stored
normalised (first endpoint lexicographically smaller, so it is not degenerate), has `X0, X1 ≤ 5000`,
and its two reflections (normalised), with the same mass, are segments. -/
def check : Bool :=
  PTree.chainB ptree.toList && STree.chainB stree.toList &&
    ptree.all (fun e => Nat.ble e.1 5000 && ptree.mem (pX e) && ptree.mem (pS e)) &&
    stree.all (fun e => ptLt e.1 e.2.1 e.2.2.1 e.2.2.2.1 && Nat.ble e.1 5000 &&
      Nat.ble e.2.2.1 5000 && stree.mem (sX e) && stree.mem (sS e))

/-- **The data checks pass** (kernel evaluation). -/
theorem check_ok : check = true := by decide +kernel

/-- **The point and segment totals, as integers** (kernel evaluation). -/
theorem pwsum_tree : ptree.wsum = 350685505788 := by decide +kernel
theorem swsum_tree : stree.wsum = 1738789413944 := by decide +kernel

theorem check_parts : PTree.chainB ptree.toList = true ∧ STree.chainB stree.toList = true ∧
    ptree.all (fun e => Nat.ble e.1 5000 && ptree.mem (pX e) && ptree.mem (pS e)) = true ∧
    stree.all (fun e => ptLt e.1 e.2.1 e.2.2.1 e.2.2.2.1 && Nat.ble e.1 5000 &&
      Nat.ble e.2.2.1 5000 && stree.mem (sX e) && stree.mem (sS e)) = true := by
  have h := check_ok
  simp only [check, Bool.and_eq_true] at h
  exact ⟨h.1.1.1, h.1.1.2, h.1.2, h.2⟩

theorem pnodup : ptree.toList.Nodup := PTree.nodup_of_chainB _ check_parts.1
theorem snodup : stree.toList.Nodup := STree.nodup_of_chainB _ check_parts.2.1

/-- **7,536 point entries and 1,872 segment entries**, one per line of the file. -/
theorem card_pentries : pentries.card = 7536 := by
  have hl : ptree.toList.length = 7536 := by decide +kernel
  rw [pentries, List.toFinset_card_of_nodup pnodup, hl]

theorem card_sentries : sentries.card = 1872 := by
  have hl : stree.toList.length = 1872 := by decide +kernel
  rw [sentries, List.toFinset_card_of_nodup snodup, hl]

theorem pentry_ok (e : ℕ × ℕ × ℕ) (he : e ∈ pentries) :
    e.1 ≤ 5000 ∧ pX e ∈ pentries ∧ pS e ∈ pentries := by
  have h2 := (PTree.all_iff _ ptree).mp check_parts.2.2.1 e (List.mem_toFinset.mp he)
  simp only [Bool.and_eq_true, Nat.ble_eq] at h2
  exact ⟨h2.1.1, List.mem_toFinset.mpr (PTree.mem_sound _ _ h2.1.2),
    List.mem_toFinset.mpr (PTree.mem_sound _ _ h2.2)⟩

theorem sentry_ok (e : SegE) (he : e ∈ sentries) :
    ptLt e.1 e.2.1 e.2.2.1 e.2.2.2.1 = true ∧ e.1 ≤ 5000 ∧ e.2.2.1 ≤ 5000 ∧
      sX e ∈ sentries ∧ sS e ∈ sentries := by
  have h2 := (STree.all_iff _ stree).mp check_parts.2.2.2 e (List.mem_toFinset.mp he)
  simp only [Bool.and_eq_true, Nat.ble_eq] at h2
  exact ⟨h2.1.1.1.1, h2.1.1.1.2, h2.1.1.2, List.mem_toFinset.mpr (STree.mem_sound _ _ h2.1.2),
    List.mem_toFinset.mpr (STree.mem_sound _ _ h2.2)⟩

/-! ## 3.  Total, non-negativity, the measure of a square -/

/-- The masses are non-negative. -/
theorem nonneg : cover.Nonneg :=
  ⟨fun _ _ => by simp only [cover, pw]; positivity,
   fun _ _ => by simp only [cover, sw]; positivity,
   fun k _ => k.elim⟩

/-- **The total is `2089474919732 / 10¹¹ = 20.8947… < 21`** (proved). -/
theorem total_eq : cover.total = (2089474919732 : ℝ) / 100000000000 := by
  have hp : ∑ e ∈ pentries, pw e = (350685505788 : ℝ) / 100000000000 := by
    have hn : ∑ e ∈ pentries, e.2.2 = 350685505788 := by
      rw [pentries, List.sum_toFinset _ pnodup, ← PTree.wsum_eq, pwsum_tree]
    have hr : ∑ e ∈ pentries, (e.2.2 : ℝ) = 350685505788 := by
      rw [← Nat.cast_sum, hn]; norm_num
    unfold pw
    rw [← Finset.sum_div, hr]
  have hs : ∑ e ∈ sentries, sw e = (1738789413944 : ℝ) / 100000000000 := by
    have hn : ∑ e ∈ sentries, e.2.2.2.2 = 1738789413944 := by
      rw [sentries, List.sum_toFinset _ snodup, ← STree.wsum_eq, swsum_tree]
    have hr : ∑ e ∈ sentries, (e.2.2.2.2 : ℝ) = 1738789413944 := by
      rw [← Nat.cast_sum, hn]; norm_num
    unfold sw
    rw [← Finset.sum_div, hr]
  simp only [MixedCover.total, cover, Finset.sum_empty, add_zero]
  rw [hp, hs]
  norm_num

theorem total_lt : cover.total < 21 := by
  rw [total_eq]; norm_num

/-- The measure of all of `[0,5]²` is `< 21`. -/
theorem mu_box_lt : μ (box 5) < 21 := by
  have h1 : μ (box 5) ≤ ENNReal.ofReal cover.total :=
    (measure_mono (Set.subset_univ _)).trans (cover.measure_univ_le nonneg)
  have h2 : ENNReal.ofReal cover.total < 21 := by
    rw [show (21 : ℝ≥0∞) = ENNReal.ofReal 21 by norm_num]
    exact (ENNReal.ofReal_lt_ofReal_iff (by norm_num)).mpr total_lt
  exact h1.trans_lt h2

open Classical in
/-- **The measure of a closed square is the explicit mass**: the point masses in it, plus each
segment's mass times the fraction of the segment in it. -/
theorem mu_sq (c : ℝ × ℝ) (θ : ℝ) :
    μ (sq c θ 1) = ENNReal.ofReal (∑ e ∈ pentries.filter (fun e => pt e ∈ sq c θ 1), pw e
      + ∑ e ∈ sentries, sw e * segFrac (sa e) (sb e) (sq c θ 1)) := by
  rw [μ, cover.measure_apply nonneg (measurableSet_sq _ _ _)]
  simp only [MixedCover.mass, cover, Finset.sum_empty, add_zero]
  rfl

/-! ## 4.  D4 invariance -/

lemma sX_eq (e : SegE) (h : ptLt e.1 e.2.1 e.2.2.1 e.2.2.2.1 = true) (ha : e.1 ≤ 5000)
    (hc : e.2.2.1 ≤ 5000) :
    sX (sX e) = e ∧ sw (sX e) = sw e ∧
      ((sa (sX e) = reflX 5 (sa e) ∧ sb (sX e) = reflX 5 (sb e)) ∨
        (sa (sX e) = reflX 5 (sb e) ∧ sb (sX e) = reflX 5 (sa e))) := by
  obtain ⟨a, b, c, d, w⟩ := e
  simp only [ptLt_iff] at h
  simp only at ha hc
  have hA : ((5000 - a : ℕ) : ℝ) = 5000 - a := by rw [Nat.cast_sub ha]; norm_num
  have hC : ((5000 - c : ℕ) : ℝ) = 5000 - c := by rw [Nat.cast_sub hc]; norm_num
  by_cases h1 : ptLt (5000 - a) b (5000 - c) d = true
  · have e1 : sX (a, b, c, d, w) = (5000 - a, b, 5000 - c, d, w) := by
      simp only [sX, segNorm, h1, if_true]
    have e2 : sX (5000 - a, b, 5000 - c, d, w) = (a, b, c, d, w) := by
      have h2 : ptLt (5000 - (5000 - a)) b (5000 - (5000 - c)) d = true := by
        rw [ptLt_iff]; omega
      simp only [sX, segNorm, h2, if_true]
      ext <;> simp <;> omega
    refine ⟨by rw [e1, e2], by rw [e1]; rfl, Or.inl ⟨?_, ?_⟩⟩
    · rw [e1]; simp only [sa, reflX, hA]; ext <;> simp; ring
    · rw [e1]; simp only [sb, reflX, hC]; ext <;> simp; ring
  · have e1 : sX (a, b, c, d, w) = (5000 - c, d, 5000 - a, b, w) := by
      simp only [sX, segNorm, h1, if_false, Bool.false_eq_true]
    have e2 : sX (5000 - c, d, 5000 - a, b, w) = (a, b, c, d, w) := by
      have h2 : ¬ ptLt (5000 - (5000 - c)) d (5000 - (5000 - a)) b = true := by
        rw [ptLt_iff]; omega
      simp only [sX, segNorm, h2, if_false, Bool.false_eq_true]
      ext <;> simp <;> omega
    refine ⟨by rw [e1, e2], by rw [e1]; rfl, Or.inr ⟨?_, ?_⟩⟩
    · rw [e1]; simp only [sa, sb, reflX, hC]; ext <;> simp; ring
    · rw [e1]; simp only [sa, sb, reflX, hA]; ext <;> simp; ring

lemma sS_eq (e : SegE) (h : ptLt e.1 e.2.1 e.2.2.1 e.2.2.2.1 = true) :
    sS (sS e) = e ∧ sw (sS e) = sw e ∧
      ((sa (sS e) = swapXY (sa e) ∧ sb (sS e) = swapXY (sb e)) ∨
        (sa (sS e) = swapXY (sb e) ∧ sb (sS e) = swapXY (sa e))) := by
  obtain ⟨a, b, c, d, w⟩ := e
  simp only [ptLt_iff] at h
  by_cases h1 : ptLt b a d c = true
  · have e1 : sS (a, b, c, d, w) = (b, a, d, c, w) := by
      simp only [sS, segNorm, h1, if_true]
    have e2 : sS (b, a, d, c, w) = (a, b, c, d, w) := by
      have h2 : ptLt a b c d = true := by rw [ptLt_iff]; omega
      simp only [sS, segNorm, h2, if_true]
    exact ⟨by rw [e1, e2], by rw [e1]; rfl, Or.inl ⟨by rw [e1]; rfl, by rw [e1]; rfl⟩⟩
  · have e1 : sS (a, b, c, d, w) = (d, c, b, a, w) := by
      simp only [sS, segNorm, h1, if_false, Bool.false_eq_true]
    have e2 : sS (d, c, b, a, w) = (a, b, c, d, w) := by
      have h2 : ¬ ptLt c d a b = true := by rw [ptLt_iff]; omega
      simp only [sS, segNorm, h2, if_false, Bool.false_eq_true]
    exact ⟨by rw [e1, e2], by rw [e1]; rfl, Or.inr ⟨by rw [e1]; rfl, by rw [e1]; rfl⟩⟩

/-- **The measure is D4-invariant** (proved). -/
theorem d4 : D4InvM 5 μ := by
  refine cover.d4InvM 5 (fun k => k.elim) pX pS sX sS id id ?_ ?_ (fun k => k.elim) ?_ ?_
    fun k => k.elim
  · intro e he
    obtain ⟨hx, hpX, _⟩ := pentry_ok e he
    refine ⟨hpX, ?_, rfl, ?_⟩
    · change pt (pX e) = reflX 5 (pt e)
      simp only [pt, pX, reflX, Nat.cast_sub hx]
      ext
      · simp; ring
      · simp
    · obtain ⟨a, b, c⟩ := e
      simp only [pX] at hx ⊢
      ext <;> simp; omega
  · intro e he
    obtain ⟨h, ha, hc, hsX, _⟩ := sentry_ok e he
    obtain ⟨h1, h2, h3⟩ := sX_eq e h ha hc
    exact ⟨hsX, h2, h1, h3⟩
  · intro e he
    exact ⟨(pentry_ok e he).2.2, rfl, rfl, rfl⟩
  · intro e he
    obtain ⟨h, _, _, _, hsS⟩ := sentry_ok e he
    obtain ⟨h1, h2, h3⟩ := sS_eq e h
    exact ⟨hsS, h2, h1, h3⟩

end S21Data

open S21Data

/-! ## 5.  The hypothesis and the theorem -/

open Classical in
/-- **The computational hypothesis.**  Every closed unit square inside `[0,5]²` whose centre lies
in `[0,5/2]²` and whose angle lies in `[0, π/4]` gets mass `≥ 1` from the cover
`certificates/s21/s21_mixed_cover_5.txt`: the masses of the points in it, plus, for each segment,
its mass times the fraction of the segment lying in it (`segFrac`: the Lebesgue measure of the
parameters `t ∈ [0,1]` with `a + t(b − a)` in the square). -/
def S21RegionCover : Prop :=
  ∀ (c : ℝ × ℝ) (θ : ℝ), c.1 ∈ Set.Icc 0 (5 / 2) → c.2 ∈ Set.Icc 0 (5 / 2) →
    θ ∈ Set.Icc 0 (Real.pi / 4) → sq c θ 1 ⊆ box 5 →
      1 ≤ ∑ e ∈ pentries.filter (fun e => pt e ∈ sq c θ 1), pw e
        + ∑ e ∈ sentries, sw e * segFrac (sa e) (sb e) (sq c θ 1)

open Classical in
/-- **The hypothesis in the checker's coordinates**: the root domain `[0,5/2]² × u ∈ [0, 1/2]` with
`θ = 2 arctan u`, which `zm_mixed.py --d4` covers by its 40,000 roots. -/
def S21CheckerCover : Prop :=
  ∀ (c : ℝ × ℝ) (u : ℝ), c.1 ∈ Set.Icc 0 (5 / 2) → c.2 ∈ Set.Icc 0 (5 / 2) →
    u ∈ Set.Icc 0 (1 / 2) → sq c (2 * Real.arctan u) 1 ⊆ box 5 →
      1 ≤ ∑ e ∈ pentries.filter (fun e => pt e ∈ sq c (2 * Real.arctan u) 1), pw e
        + ∑ e ∈ sentries, sw e * segFrac (sa e) (sb e) (sq c (2 * Real.arctan u) 1)

/-- The checker's statement implies the region statement (its angle range is larger). -/
theorem S21CheckerCover.region (h : S21CheckerCover) : S21RegionCover := by
  intro c θ h1 h2 hθ hsub
  obtain ⟨u, hu, rfl⟩ := exists_u_of_theta hθ
  exact h c u h1 h2 hu hsub

/-- From the region to every closed unit square in `[0,5]²` (the D4 reduction for measures). -/
theorem s21_cover_all (h : S21RegionCover) :
    ∀ (c : ℝ × ℝ) (θ : ℝ), sq c θ 1 ⊆ box 5 → 1 ≤ μ (sq c θ 1) := by
  refine d4_reduction_measure 5 μ d4 fun c θ h1 h2 hθ hsub => ?_
  rw [mu_sq, ← ENNReal.ofReal_one]
  exact ENNReal.ofReal_le_ofReal (h c θ h1 h2 hθ hsub)

/-- **Lower bound**: under the hypothesis, 21 unit squares do not fit in a square of side `< 5`. -/
theorem s21_not_packs (h : S21RegionCover) {s : ℝ} (hs : s < 5) : ¬ Packs 21 s :=
  not_packs_of_measure 5 μ (s21_cover_all h) 21 (by exact_mod_cast mu_box_lt) hs

/-- **Upper bound**: 21 unit squares fit in `[0,5]²` (the 5 × 5 grid minus 4). -/
theorem s21_packs : Packs 21 5 := by
  have h := packs_grid 5 21 (by norm_num)
  simpa using h

/-- Under the hypothesis, `5` is the least side of a square holding 21 unit squares. -/
theorem s21_isLeast (h : S21RegionCover) : IsLeast {s | Packs 21 s} 5 :=
  ⟨s21_packs, fun _ hs => not_lt.mp fun hlt => s21_not_packs h hlt hs⟩

/-- **`s(21) = 5`**, from the single computational hypothesis `S21RegionCover`. -/
theorem s21_eq_five (h : S21RegionCover) : minSide 21 = 5 :=
  (s21_isLeast h).csInf_eq

/-- **`s(21) = 5`**, from the statement the `zm_mixed.py` D4 run certifies. -/
theorem s21_eq_five_of_checker (h : S21CheckerCover) : minSide 21 = 5 :=
  s21_eq_five h.region

end SquarePacking
