import Mathlib

/-!
# Unit squares in the plane, and the facts the 19-square endpoint needs

`sq` and `IsUnitSquare` are copied from the 17 project (`Sq17Lean/SquareBase.lean`, tag v1.0.0) into the
`Sq19` namespace. The remaining lemmas are support bounds for squares at angle 0 and 45 degrees and a
half-plane separation lemma for interiors.
-/

namespace Sq19

/-- The closed unit square with centre `(cx, cy)` whose sides are parallel to `(ux, uy)` and
`(-uy, ux)`: the points whose two coordinates in that frame are at most 1/2 in absolute value.
It is a genuine unit square exactly when `(ux, uy)` is a unit vector. -/
def sq (cx cy ux uy : ℝ) : Set (ℝ × ℝ) :=
  {p | |(p.1 - cx) * ux + (p.2 - cy) * uy| ≤ 1/2 ∧ |(p.2 - cy) * ux - (p.1 - cx) * uy| ≤ 1/2}

/-- A set is a unit square if it is `sq` of some centre and some unit direction. -/
def IsUnitSquare (S : Set (ℝ × ℝ)) : Prop :=
  ∃ cx cy ux uy : ℝ, ux ^ 2 + uy ^ 2 = 1 ∧ S = sq cx cy ux uy

theorem sqrt2_sq : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)

theorem sqrt2_lo : (1414 : ℝ) / 1000 < Real.sqrt 2 := by
  rw [Real.lt_sqrt (by norm_num)]; norm_num

theorem sqrt2_hi : Real.sqrt 2 < (1415 : ℝ) / 1000 := by
  rw [Real.sqrt_lt' (by norm_num)]; norm_num

theorem diag_unit : (Real.sqrt 2 / 2) ^ 2 + (Real.sqrt 2 / 2) ^ 2 = 1 := by
  have h := sqrt2_sq; nlinarith

/-- Every point of the axis-parallel square satisfies `a z₁ + b z₂ ≤ a cx + b cy + (|a| + |b|)/2`. -/
theorem axis_le (a b cx cy : ℝ) (z : ℝ × ℝ) (hz : z ∈ sq cx cy 1 0) :
    a * z.1 + b * z.2 ≤ a * cx + b * cy + (|a| + |b|) / 2 := by
  obtain ⟨h1, h2⟩ := hz
  simp only [mul_one, mul_zero, add_zero, sub_zero] at h1 h2
  have e1 : a * (z.1 - cx) ≤ |a| * (1/2) := by
    calc a * (z.1 - cx) ≤ |a * (z.1 - cx)| := le_abs_self _
      _ = |a| * |z.1 - cx| := abs_mul _ _
      _ ≤ |a| * (1/2) := mul_le_mul_of_nonneg_left h1 (abs_nonneg a)
  have e2 : b * (z.2 - cy) ≤ |b| * (1/2) := by
    calc b * (z.2 - cy) ≤ |b * (z.2 - cy)| := le_abs_self _
      _ = |b| * |z.2 - cy| := abs_mul _ _
      _ ≤ |b| * (1/2) := mul_le_mul_of_nonneg_left h2 (abs_nonneg b)
  nlinarith

/-- Every point of the square at 45 degrees satisfies
`a z₁ + b z₂ ≤ a cx + b cy + (|a + b| + |b - a|) √2 / 4`. -/
theorem diag_le (a b cx cy : ℝ) (z : ℝ × ℝ)
    (hz : z ∈ sq cx cy (Real.sqrt 2 / 2) (Real.sqrt 2 / 2)) :
    a * z.1 + b * z.2 ≤ a * cx + b * cy + (|a + b| + |b - a|) * Real.sqrt 2 / 4 := by
  obtain ⟨h1, h2⟩ := hz
  have hs := sqrt2_sq
  have hpos : 0 < Real.sqrt 2 := by positivity
  set s := Real.sqrt 2
  set u := (z.1 - cx) + (z.2 - cy)
  set v := (z.2 - cy) - (z.1 - cx)
  have hu : |u| ≤ s / 2 := by
    have e : (z.1 - cx) * (s / 2) + (z.2 - cy) * (s / 2) = u * (s / 2) := by ring
    rw [e, abs_mul, abs_of_pos (by positivity : 0 < s / 2)] at h1
    have : |u| * s ≤ 1 := by linarith
    nlinarith [abs_nonneg u]
  have hv : |v| ≤ s / 2 := by
    have e : (z.2 - cy) * (s / 2) - (z.1 - cx) * (s / 2) = v * (s / 2) := by ring
    rw [e, abs_mul, abs_of_pos (by positivity : 0 < s / 2)] at h2
    have : |v| * s ≤ 1 := by linarith
    nlinarith [abs_nonneg v]
  have key : a * z.1 + b * z.2 = a * cx + b * cy + ((a + b) * u + (b - a) * v) / 2 := by
    simp only [u, v]; ring
  have e1 : (a + b) * u ≤ |a + b| * (s / 2) := by
    calc (a + b) * u ≤ |(a + b) * u| := le_abs_self _
      _ = |a + b| * |u| := abs_mul _ _
      _ ≤ |a + b| * (s / 2) := mul_le_mul_of_nonneg_left hu (abs_nonneg _)
  have e2 : (b - a) * v ≤ |b - a| * (s / 2) := by
    calc (b - a) * v ≤ |(b - a) * v| := le_abs_self _
      _ = |b - a| * |v| := abs_mul _ _
      _ ≤ |b - a| * (s / 2) := mul_le_mul_of_nonneg_left hv (abs_nonneg _)
  rw [key]; nlinarith

/-- If a nonzero linear functional is at most `c` on `A` and at least `c` on `B`, the interiors of
`A` and `B` are disjoint. Boundary contact is allowed. -/
theorem halfplane_disjoint (A B : Set (ℝ × ℝ)) (a b c : ℝ) (hab : a ^ 2 + b ^ 2 ≠ 0)
    (hA : ∀ z ∈ A, a * z.1 + b * z.2 ≤ c) (hB : ∀ z ∈ B, c ≤ a * z.1 + b * z.2) :
    Disjoint (interior A) (interior B) := by
  let f : (ℝ × ℝ) →L[ℝ] ℝ := a • ContinuousLinearMap.fst ℝ ℝ ℝ + b • ContinuousLinearMap.snd ℝ ℝ ℝ
  have hf_apply : ∀ z : ℝ × ℝ, f z = a * z.1 + b * z.2 := fun z => rfl
  have hsurj : Function.Surjective f := by
    intro t
    refine ⟨(a * t / (a ^ 2 + b ^ 2), b * t / (a ^ 2 + b ^ 2)), ?_⟩
    rw [hf_apply]; field_simp
  have hA' : A ⊆ f ⁻¹' Set.Iic c := fun z hz => by simp [hf_apply, hA z hz]
  have hB' : B ⊆ f ⁻¹' Set.Ici c := fun z hz => by simp [hf_apply, hB z hz]
  apply Set.disjoint_left.mpr
  intro z hzA hzB
  have h1 := interior_mono hA' hzA
  have h2 := interior_mono hB' hzB
  rw [f.interior_preimage hsurj, interior_Iic] at h1
  rw [f.interior_preimage hsurj, interior_Ici] at h2
  simp only [Set.mem_preimage, Set.mem_Iio, Set.mem_Ioi] at h1 h2
  linarith

end Sq19

#print axioms Sq19.halfplane_disjoint
#print axioms Sq19.diag_le
