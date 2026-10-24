import Mathlib

/-!
# Four unit squares in a rectangle: the two-angle inequalities

The one-square lemma for `R₄` (`Rect4.lean`) reduces, case by case, to inequalities in two frames
`(P, Q)` (the square) and `(C, S)` (the separating line): unit vectors with nonnegative entries,
`σ = SP - CQ = sin(t - θ)`.  In half-angle coordinates `u = tan(θ/2)`, `v = tan(t/2) ∈ [0, 1]` they factor:

* `polyD1 = 4uv(v - u) R₁ / ((1+u²)²(1+v²)²)`, `R₁ = u²(v² - 2v - 1) + 2uv + (v - 1)²` (`σ ≥ 0`, so `u ≤ v`);
* `polyD2 = 2(1 - u)(u - v)(1 - v) R₂ / ((1+u²)²(1+v²)²)`, `R₂ = u²(v² - 2v - 1) + 2uv(v + 1) + v² + 1`
  (`σ ≤ 0`, so `v ≤ u`).

`R₁`, `R₂` are concave in `u` and nonnegative at the ends of the range (chord identities).
-/

namespace SquarePacking

/-- The D-case inequality for `σ ≥ 0` (the frontier and upright bounds, mixed with weight `CQ/(SP)`). -/
def polyD1 (P Q C S : ℝ) : ℝ :=
  -C*P*S - C*Q^2*S + C*Q*S - C*Q + C*S + P*Q*S^2 - P*S^2 - Q*S^2 - Q*S + Q + S^2

/-- The D-case inequality for `σ ≤ 0`, at `H = 2`: `C γ (P + Q - 1) - P (C + S - 1)`. -/
def polyD2 (P Q C S : ℝ) : ℝ := C * (S * Q + C * P) * (P + Q - 1) - P * (C + S - 1)

/-- Half-angle coordinates of a unit vector with nonnegative entries. -/
lemma half_angle {P Q : ℝ} (hP : 0 ≤ P) (hQ : 0 ≤ Q) (hPQ : P ^ 2 + Q ^ 2 = 1) :
    ∃ u : ℝ, 0 ≤ u ∧ u ≤ 1 ∧ P = (1 - u ^ 2) / (1 + u ^ 2) ∧ Q = 2 * u / (1 + u ^ 2) := by
  have h1 : 0 < 1 + P := by linarith
  have hQ1 : Q ≤ 1 := by nlinarith
  refine ⟨Q / (1 + P), div_nonneg hQ h1.le, (div_le_one h1).2 (by linarith), ?_, ?_⟩
  · field_simp; nlinarith
  · field_simp; nlinarith

/-- The order of the half angles from the sign of `σ = SP - CQ`. -/
lemma half_order {u v : ℝ} (hu : 0 ≤ u) (hv : 0 ≤ v)
    (h : 0 ≤ 2 * v / (1 + v ^ 2) * ((1 - u ^ 2) / (1 + u ^ 2)) -
      (1 - v ^ 2) / (1 + v ^ 2) * (2 * u / (1 + u ^ 2))) : u ≤ v := by
  have e : 2 * v / (1 + v ^ 2) * ((1 - u ^ 2) / (1 + u ^ 2)) -
      (1 - v ^ 2) / (1 + v ^ 2) * (2 * u / (1 + u ^ 2)) =
      2 * (v - u) * (1 + u * v) / ((1 + u ^ 2) * (1 + v ^ 2)) := by field_simp; ring
  rw [e, div_nonneg_iff] at h
  rcases h with ⟨h1, -⟩ | ⟨-, h2⟩
  · nlinarith [mul_nonneg hu hv]
  · nlinarith [sq_nonneg u, sq_nonneg v, mul_nonneg (sq_nonneg u) (sq_nonneg v)]

/-- **D1** (`σ ≥ 0`). -/
theorem core_D1 {P Q C S : ℝ} (hP : 0 ≤ P) (hQ : 0 ≤ Q) (hC : 0 ≤ C) (hS : 0 ≤ S)
    (hPQ : P ^ 2 + Q ^ 2 = 1) (hCS : C ^ 2 + S ^ 2 = 1) (hsg : 0 ≤ S * P - C * Q) :
    0 ≤ polyD1 P Q C S := by
  obtain ⟨u, hu0, hu1, rfl, rfl⟩ := half_angle hP hQ hPQ
  obtain ⟨v, hv0, hv1, rfl, rfl⟩ := half_angle hC hS hCS
  have huv := half_order hu0 hv0 (by linarith)
  set R1 := u ^ 2 * (v ^ 2 - 2 * v - 1) + 2 * u * v + (v - 1) ^ 2
  have hR1 : 0 ≤ R1 := by
    rcases eq_or_lt_of_le hv0 with h | h
    · subst h; have : u = 0 := by linarith
      subst this; simp [R1]
    · have chord : v * R1 = (v - u) * (v - 1) ^ 2 + u * (v ^ 2 + 1) * (v - 1) ^ 2 +
          v * (1 + 2 * v - v ^ 2) * u * (v - u) := by simp only [R1]; ring
      have : 0 ≤ v * R1 := by
        rw [chord]
        have : 0 ≤ 1 + 2 * v - v ^ 2 := by nlinarith
        have := sub_nonneg.2 huv
        positivity
      exact (mul_nonneg_iff_of_pos_left h).1 this
  have e : polyD1 ((1 - u ^ 2) / (1 + u ^ 2)) (2 * u / (1 + u ^ 2)) ((1 - v ^ 2) / (1 + v ^ 2))
      (2 * v / (1 + v ^ 2)) = 4 * u * v * (v - u) * R1 / ((1 + u ^ 2) ^ 2 * (1 + v ^ 2) ^ 2) := by
    simp only [polyD1, R1]; field_simp; ring
  rw [e]
  have := sub_nonneg.2 huv
  positivity

/-- **D2** (`σ ≤ 0`). -/
theorem core_D2 {P Q C S : ℝ} (hP : 0 ≤ P) (hQ : 0 ≤ Q) (hC : 0 ≤ C) (hS : 0 ≤ S)
    (hPQ : P ^ 2 + Q ^ 2 = 1) (hCS : C ^ 2 + S ^ 2 = 1) (hsg : S * P - C * Q ≤ 0) :
    0 ≤ polyD2 P Q C S := by
  obtain ⟨u, hu0, hu1, rfl, rfl⟩ := half_angle hP hQ hPQ
  obtain ⟨v, hv0, hv1, rfl, rfl⟩ := half_angle hC hS hCS
  have hvu : v ≤ u := half_order hv0 hu0 (by
    have e : ∀ a b c d : ℝ, a * b - c * d = -(c * d - a * b) := fun _ _ _ _ => by ring
    nlinarith [e (2 * v / (1 + v ^ 2)) ((1 - u ^ 2) / (1 + u ^ 2)) ((1 - v ^ 2) / (1 + v ^ 2))
      (2 * u / (1 + u ^ 2))])
  set R2 := u ^ 2 * (v ^ 2 - 2 * v - 1) + 2 * u * v * (v + 1) + v ^ 2 + 1
  have hR2 : 0 ≤ R2 := by
    rcases eq_or_lt_of_le hv1 with h | h
    · subst h; have : u = 1 := by linarith
      subst this; norm_num [R2]
    · have chord : (1 - v) * R2 = (1 - u) * (v ^ 2 + 1) ^ 2 + (u - v) * (4 * v ^ 2) +
          (1 - v) * (1 + 2 * v - v ^ 2) * (u - v) * (1 - u) := by simp only [R2]; ring
      have : 0 ≤ (1 - v) * R2 := by
        rw [chord]
        have : 0 ≤ 1 + 2 * v - v ^ 2 := by nlinarith
        have := sub_nonneg.2 hvu; have := sub_nonneg.2 hu1; have := sub_nonneg.2 hv1
        positivity
      exact (mul_nonneg_iff_of_pos_left (by linarith)).1 this
  have e : polyD2 ((1 - u ^ 2) / (1 + u ^ 2)) (2 * u / (1 + u ^ 2)) ((1 - v ^ 2) / (1 + v ^ 2))
      (2 * v / (1 + v ^ 2)) =
      2 * (1 - u) * (u - v) * (1 - v) * R2 / ((1 + u ^ 2) ^ 2 * (1 + v ^ 2) ^ 2) := by
    simp only [polyD2, R2]; field_simp; ring
  rw [e]
  have := sub_nonneg.2 hvu; have := sub_nonneg.2 hu1; have := sub_nonneg.2 hv1
  positivity

/-- For the construction: `g(C, S) = S/2 + C - S² - 2C² + k(S² - CS + 2C²) ≥ 0`, `k = (C + S)/2`
(`= 2v(1 - v)(2v⁴ + v³ + v² - v + 1)/(1 + v²)³`). -/
theorem core_g {C S : ℝ} (hC : 0 ≤ C) (hS : 0 ≤ S) (hCS : C ^ 2 + S ^ 2 = 1) :
    0 ≤ S / 2 + C - S ^ 2 - 2 * C ^ 2 + (C + S) / 2 * (S ^ 2 - C * S + 2 * C ^ 2) := by
  obtain ⟨v, hv0, hv1, rfl, rfl⟩ := half_angle hC hS hCS
  have e : 2 * v / (1 + v ^ 2) / 2 + (1 - v ^ 2) / (1 + v ^ 2) - (2 * v / (1 + v ^ 2)) ^ 2 -
      2 * ((1 - v ^ 2) / (1 + v ^ 2)) ^ 2 + ((1 - v ^ 2) / (1 + v ^ 2) + 2 * v / (1 + v ^ 2)) / 2 *
        ((2 * v / (1 + v ^ 2)) ^ 2 - (1 - v ^ 2) / (1 + v ^ 2) * (2 * v / (1 + v ^ 2)) +
          2 * ((1 - v ^ 2) / (1 + v ^ 2)) ^ 2) =
      2 * v * (1 - v) * (2 * v ^ 4 + v ^ 3 + (v - 1 / 2) ^ 2 + 3 / 4) / (1 + v ^ 2) ^ 3 := by
    field_simp; ring
  rw [e]
  have := sub_nonneg.2 hv1
  positivity

end SquarePacking
