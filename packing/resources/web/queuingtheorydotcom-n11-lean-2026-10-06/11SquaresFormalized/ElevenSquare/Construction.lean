import ElevenSquare.ConstructionData
import ElevenSquare.BasicGeometry
import Mathlib.Tactic.FinCases

/-! The exact attaining construction, assembled from checked scalar certificates. -/
namespace ElevenSquare
noncomputable section
set_option maxHeartbeats 4000000

abbrev candidateSquare := constructionSquare

/-- The polynomial representative agrees with the rational half-angle formula. -/
theorem construction_cos_halfAngle : constructionCos = (1-u^2)/(1+u^2) := by
  apply (eq_div_iff (show (1+u^2 : ℝ) ≠ 0 by positivity)).mpr
  have hid : constructionCos * (1+u^2) - (1-u^2) =
      (u/20 - 1/40) * endpointPolynomial u := by
    dsimp only [constructionCos, endpointPolynomial]
    ring
  rw [u_polynomial, mul_zero] at hid
  linarith

/-- The polynomial representative agrees with the rational half-angle formula. -/
theorem construction_sin_halfAngle : constructionSin = (2*u)/(1+u^2) := by
  apply (eq_div_iff (show (1+u^2 : ℝ) ≠ 0 by positivity)).mpr
  have hid : constructionSin * (1+u^2) - (2*u) =
      (-u/40 - 1/20) * endpointPolynomial u := by
    dsimp only [constructionSin, endpointPolynomial]
    ring
  rw [u_polynomial, mul_zero] at hid
  linarith

theorem construction_halfWidth (i : Fin 11) :
    halfWidth (constructionSquare i) = constructionRadius i := by
  by_cases hi : i.val < 6
  · simp [constructionSquare, constructionAxis, halfWidth, constructionRadius, hi,
      show ¬6 ≤ i.val by omega]
  · simp [constructionSquare, constructionAxis, halfWidth, constructionRadius, hi,
      show 6 ≤ i.val by omega,
      abs_of_pos construction_cos_pos, abs_of_pos construction_sin_pos]

theorem construction_separator_unit (k : Fin 4) :
    normSq (constructionSeparator k) = 1 := by
  fin_cases k
  · norm_num [constructionSeparator, normSq, dot]
  · norm_num [constructionSeparator, normSq, dot]
  · simpa [constructionSeparator, normSq, dot, sq] using construction_cos_sq_add_sin_sq
  · simpa [constructionSeparator, normSq, dot, sq, add_comm] using construction_cos_sq_add_sin_sq

theorem construction_projectionRadius (i : Fin 11) (k : Fin 4) :
    projectionRadius (constructionSquare i) (constructionSeparator k) =
      constructionSepRadius i k := by
  have hc := construction_cos_pos
  have hs := construction_sin_pos
  have hnorm : constructionCos * constructionCos + constructionSin * constructionSin = 1 := by
    simpa only [sq] using construction_cos_sq_add_sin_sq
  have hcross : -constructionSin * constructionCos + constructionCos * constructionSin = 0 := by ring
  have hcross' : constructionCos * -constructionSin + constructionSin * constructionCos = 0 := by ring
  by_cases hi : i.val < 6
  · have hge : ¬6 ≤ i.val := by omega
    fin_cases k <;>
      simp [projectionRadius, constructionSquare, constructionAxis, constructionSeparator,
        constructionSepRadius, dot, perp, hi, hge, abs_of_pos hc, abs_of_pos hs, add_comm, mul_comm]
  · have hge : 6 ≤ i.val := by omega
    fin_cases k <;>
      simp [projectionRadius, constructionSquare, constructionAxis, constructionSeparator,
        constructionSepRadius, dot, perp, hi, hge, abs_of_pos hc, abs_of_pos hs,
        hnorm, hcross, hcross', add_comm, mul_comm]

theorem construction_contained (i : Fin 11) :
    ∀ p, ClosedSquare (constructionSquare i) p → InContainer T p := by
  apply contained_of_center_bounds
  all_goals rw [construction_halfWidth]
  all_goals simp only [constructionSquare]
  all_goals try rw [← constructionSide_eq_T]

  · fin_cases i
    · exact sub_nonneg.mp construction_bound_0_0_0
    · exact sub_nonneg.mp construction_bound_1_0_0
    · exact sub_nonneg.mp construction_bound_2_0_0
    · exact sub_nonneg.mp construction_bound_3_0_0
    · exact sub_nonneg.mp construction_bound_4_0_0
    · exact sub_nonneg.mp construction_bound_5_0_0
    · exact sub_nonneg.mp construction_bound_6_0_0
    · exact sub_nonneg.mp construction_bound_7_0_0
    · exact sub_nonneg.mp construction_bound_8_0_0
    · exact sub_nonneg.mp construction_bound_9_0_0
    · exact sub_nonneg.mp construction_bound_10_0_0
  · fin_cases i
    · exact (le_sub_iff_add_le').mp (sub_nonneg.mp construction_bound_0_0_1)
    · exact (le_sub_iff_add_le').mp (sub_nonneg.mp construction_bound_1_0_1)
    · exact (le_sub_iff_add_le').mp (sub_nonneg.mp construction_bound_2_0_1)
    · exact (le_sub_iff_add_le').mp (sub_nonneg.mp construction_bound_3_0_1)
    · exact (le_sub_iff_add_le').mp (sub_nonneg.mp construction_bound_4_0_1)
    · exact (le_sub_iff_add_le').mp (sub_nonneg.mp construction_bound_5_0_1)
    · exact (le_sub_iff_add_le').mp (sub_nonneg.mp construction_bound_6_0_1)
    · exact (le_sub_iff_add_le').mp (sub_nonneg.mp construction_bound_7_0_1)
    · exact (le_sub_iff_add_le').mp (sub_nonneg.mp construction_bound_8_0_1)
    · exact (le_sub_iff_add_le').mp (sub_nonneg.mp construction_bound_9_0_1)
    · exact (le_sub_iff_add_le').mp (sub_nonneg.mp construction_bound_10_0_1)
  · fin_cases i
    · exact sub_nonneg.mp construction_bound_0_1_0
    · exact sub_nonneg.mp construction_bound_1_1_0
    · exact sub_nonneg.mp construction_bound_2_1_0
    · exact sub_nonneg.mp construction_bound_3_1_0
    · exact sub_nonneg.mp construction_bound_4_1_0
    · exact sub_nonneg.mp construction_bound_5_1_0
    · exact sub_nonneg.mp construction_bound_6_1_0
    · exact sub_nonneg.mp construction_bound_7_1_0
    · exact sub_nonneg.mp construction_bound_8_1_0
    · exact sub_nonneg.mp construction_bound_9_1_0
    · exact sub_nonneg.mp construction_bound_10_1_0
  · fin_cases i
    · exact (le_sub_iff_add_le').mp (sub_nonneg.mp construction_bound_0_1_1)
    · exact (le_sub_iff_add_le').mp (sub_nonneg.mp construction_bound_1_1_1)
    · exact (le_sub_iff_add_le').mp (sub_nonneg.mp construction_bound_2_1_1)
    · exact (le_sub_iff_add_le').mp (sub_nonneg.mp construction_bound_3_1_1)
    · exact (le_sub_iff_add_le').mp (sub_nonneg.mp construction_bound_4_1_1)
    · exact (le_sub_iff_add_le').mp (sub_nonneg.mp construction_bound_5_1_1)
    · exact (le_sub_iff_add_le').mp (sub_nonneg.mp construction_bound_6_1_1)
    · exact (le_sub_iff_add_le').mp (sub_nonneg.mp construction_bound_7_1_1)
    · exact (le_sub_iff_add_le').mp (sub_nonneg.mp construction_bound_8_1_1)
    · exact (le_sub_iff_add_le').mp (sub_nonneg.mp construction_bound_9_1_1)
    · exact (le_sub_iff_add_le').mp (sub_nonneg.mp construction_bound_10_1_1)

theorem construction_disjoint_0_1 :
    ∀ p, ¬ (OpenSquare (constructionSquare 0) p ∧ OpenSquare (constructionSquare 1) p) := by
  have hh := separated_interiors (constructionSquare 0) (constructionSquare 1)
    (constructionSeparator 0) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_0_1)
  exact hh

theorem construction_disjoint_0_2 :
    ∀ p, ¬ (OpenSquare (constructionSquare 0) p ∧ OpenSquare (constructionSquare 2) p) := by
  have hh := separated_interiors (constructionSquare 0) (constructionSquare 2)
    (constructionSeparator 0) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_0_2)
  exact hh

theorem construction_disjoint_0_3 :
    ∀ p, ¬ (OpenSquare (constructionSquare 0) p ∧ OpenSquare (constructionSquare 3) p) := by
  have hh := separated_interiors (constructionSquare 0) (constructionSquare 3)
    (constructionSeparator 1) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_0_3)
  exact hh

theorem construction_disjoint_0_4 :
    ∀ p, ¬ (OpenSquare (constructionSquare 0) p ∧ OpenSquare (constructionSquare 4) p) := by
  have hh := separated_interiors (constructionSquare 0) (constructionSquare 4)
    (constructionSeparator 1) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_0_4)
  exact hh

theorem construction_disjoint_0_5 :
    ∀ p, ¬ (OpenSquare (constructionSquare 0) p ∧ OpenSquare (constructionSquare 5) p) := by
  have hh := separated_interiors (constructionSquare 0) (constructionSquare 5)
    (constructionSeparator 1) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_0_5)
  exact hh

theorem construction_disjoint_0_6 :
    ∀ p, ¬ (OpenSquare (constructionSquare 0) p ∧ OpenSquare (constructionSquare 6) p) := by
  have hh := separated_interiors (constructionSquare 0) (constructionSquare 6)
    (constructionSeparator 2) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_0_6)
  exact hh

theorem construction_disjoint_0_7 :
    ∀ p, ¬ (OpenSquare (constructionSquare 0) p ∧ OpenSquare (constructionSquare 7) p) := by
  have hh := separated_interiors (constructionSquare 0) (constructionSquare 7)
    (constructionSeparator 0) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_0_7)
  exact hh

theorem construction_disjoint_0_8 :
    ∀ p, ¬ (OpenSquare (constructionSquare 0) p ∧ OpenSquare (constructionSquare 8) p) := by
  have hh := separated_interiors (constructionSquare 0) (constructionSquare 8)
    (constructionSeparator 0) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_0_8)
  exact hh

theorem construction_disjoint_0_9 :
    ∀ p, ¬ (OpenSquare (constructionSquare 0) p ∧ OpenSquare (constructionSquare 9) p) := by
  have hh := separated_interiors (constructionSquare 0) (constructionSquare 9)
    (constructionSeparator 0) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_0_9)
  exact hh

theorem construction_disjoint_0_10 :
    ∀ p, ¬ (OpenSquare (constructionSquare 0) p ∧ OpenSquare (constructionSquare 10) p) := by
  have hh := separated_interiors (constructionSquare 0) (constructionSquare 10)
    (constructionSeparator 0) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_0_10)
  exact hh

theorem construction_disjoint_1_2 :
    ∀ p, ¬ (OpenSquare (constructionSquare 1) p ∧ OpenSquare (constructionSquare 2) p) := by
  have hh := separated_interiors (constructionSquare 1) (constructionSquare 2)
    (constructionSeparator 1) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_1_2)
  exact hh

theorem construction_disjoint_1_3 :
    ∀ p, ¬ (OpenSquare (constructionSquare 1) p ∧ OpenSquare (constructionSquare 3) p) := by
  have hh := separated_interiors (constructionSquare 3) (constructionSquare 1)
    (constructionSeparator 0) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_1_3)
  intro p hp
  exact hh p ⟨hp.2, hp.1⟩

theorem construction_disjoint_1_4 :
    ∀ p, ¬ (OpenSquare (constructionSquare 1) p ∧ OpenSquare (constructionSquare 4) p) := by
  have hh := separated_interiors (constructionSquare 4) (constructionSquare 1)
    (constructionSeparator 0) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_1_4)
  intro p hp
  exact hh p ⟨hp.2, hp.1⟩

theorem construction_disjoint_1_5 :
    ∀ p, ¬ (OpenSquare (constructionSquare 1) p ∧ OpenSquare (constructionSquare 5) p) := by
  have hh := separated_interiors (constructionSquare 5) (constructionSquare 1)
    (constructionSeparator 0) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_1_5)
  intro p hp
  exact hh p ⟨hp.2, hp.1⟩

theorem construction_disjoint_1_6 :
    ∀ p, ¬ (OpenSquare (constructionSquare 1) p ∧ OpenSquare (constructionSquare 6) p) := by
  have hh := separated_interiors (constructionSquare 6) (constructionSquare 1)
    (constructionSeparator 0) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_1_6)
  intro p hp
  exact hh p ⟨hp.2, hp.1⟩

theorem construction_disjoint_1_7 :
    ∀ p, ¬ (OpenSquare (constructionSquare 1) p ∧ OpenSquare (constructionSquare 7) p) := by
  have hh := separated_interiors (constructionSquare 7) (constructionSquare 1)
    (constructionSeparator 0) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_1_7)
  intro p hp
  exact hh p ⟨hp.2, hp.1⟩

theorem construction_disjoint_1_8 :
    ∀ p, ¬ (OpenSquare (constructionSquare 1) p ∧ OpenSquare (constructionSquare 8) p) := by
  have hh := separated_interiors (constructionSquare 8) (constructionSquare 1)
    (constructionSeparator 0) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_1_8)
  intro p hp
  exact hh p ⟨hp.2, hp.1⟩

theorem construction_disjoint_1_9 :
    ∀ p, ¬ (OpenSquare (constructionSquare 1) p ∧ OpenSquare (constructionSquare 9) p) := by
  have hh := separated_interiors (constructionSquare 1) (constructionSquare 9)
    (constructionSeparator 3) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_1_9)
  exact hh

theorem construction_disjoint_1_10 :
    ∀ p, ¬ (OpenSquare (constructionSquare 1) p ∧ OpenSquare (constructionSquare 10) p) := by
  have hh := separated_interiors (constructionSquare 1) (constructionSquare 10)
    (constructionSeparator 1) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_1_10)
  exact hh

theorem construction_disjoint_2_3 :
    ∀ p, ¬ (OpenSquare (constructionSquare 2) p ∧ OpenSquare (constructionSquare 3) p) := by
  have hh := separated_interiors (constructionSquare 3) (constructionSquare 2)
    (constructionSeparator 0) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_2_3)
  intro p hp
  exact hh p ⟨hp.2, hp.1⟩

theorem construction_disjoint_2_4 :
    ∀ p, ¬ (OpenSquare (constructionSquare 2) p ∧ OpenSquare (constructionSquare 4) p) := by
  have hh := separated_interiors (constructionSquare 4) (constructionSquare 2)
    (constructionSeparator 0) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_2_4)
  intro p hp
  exact hh p ⟨hp.2, hp.1⟩

theorem construction_disjoint_2_5 :
    ∀ p, ¬ (OpenSquare (constructionSquare 2) p ∧ OpenSquare (constructionSquare 5) p) := by
  have hh := separated_interiors (constructionSquare 5) (constructionSquare 2)
    (constructionSeparator 0) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_2_5)
  intro p hp
  exact hh p ⟨hp.2, hp.1⟩

theorem construction_disjoint_2_6 :
    ∀ p, ¬ (OpenSquare (constructionSquare 2) p ∧ OpenSquare (constructionSquare 6) p) := by
  have hh := separated_interiors (constructionSquare 6) (constructionSquare 2)
    (constructionSeparator 0) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_2_6)
  intro p hp
  exact hh p ⟨hp.2, hp.1⟩

theorem construction_disjoint_2_7 :
    ∀ p, ¬ (OpenSquare (constructionSquare 2) p ∧ OpenSquare (constructionSquare 7) p) := by
  have hh := separated_interiors (constructionSquare 7) (constructionSquare 2)
    (constructionSeparator 1) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_2_7)
  intro p hp
  exact hh p ⟨hp.2, hp.1⟩

theorem construction_disjoint_2_8 :
    ∀ p, ¬ (OpenSquare (constructionSquare 2) p ∧ OpenSquare (constructionSquare 8) p) := by
  have hh := separated_interiors (constructionSquare 8) (constructionSquare 2)
    (constructionSeparator 2) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_2_8)
  intro p hp
  exact hh p ⟨hp.2, hp.1⟩

theorem construction_disjoint_2_9 :
    ∀ p, ¬ (OpenSquare (constructionSquare 2) p ∧ OpenSquare (constructionSquare 9) p) := by
  have hh := separated_interiors (constructionSquare 9) (constructionSquare 2)
    (constructionSeparator 1) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_2_9)
  intro p hp
  exact hh p ⟨hp.2, hp.1⟩

theorem construction_disjoint_2_10 :
    ∀ p, ¬ (OpenSquare (constructionSquare 2) p ∧ OpenSquare (constructionSquare 10) p) := by
  have hh := separated_interiors (constructionSquare 10) (constructionSquare 2)
    (constructionSeparator 3) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_2_10)
  intro p hp
  exact hh p ⟨hp.2, hp.1⟩

theorem construction_disjoint_3_4 :
    ∀ p, ¬ (OpenSquare (constructionSquare 3) p ∧ OpenSquare (constructionSquare 4) p) := by
  have hh := separated_interiors (constructionSquare 3) (constructionSquare 4)
    (constructionSeparator 0) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_3_4)
  exact hh

theorem construction_disjoint_3_5 :
    ∀ p, ¬ (OpenSquare (constructionSquare 3) p ∧ OpenSquare (constructionSquare 5) p) := by
  have hh := separated_interiors (constructionSquare 5) (constructionSquare 3)
    (constructionSeparator 1) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_3_5)
  intro p hp
  exact hh p ⟨hp.2, hp.1⟩

theorem construction_disjoint_3_6 :
    ∀ p, ¬ (OpenSquare (constructionSquare 3) p ∧ OpenSquare (constructionSquare 6) p) := by
  have hh := separated_interiors (constructionSquare 6) (constructionSquare 3)
    (constructionSeparator 1) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_3_6)
  intro p hp
  exact hh p ⟨hp.2, hp.1⟩

theorem construction_disjoint_3_7 :
    ∀ p, ¬ (OpenSquare (constructionSquare 3) p ∧ OpenSquare (constructionSquare 7) p) := by
  have hh := separated_interiors (constructionSquare 3) (constructionSquare 7)
    (constructionSeparator 0) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_3_7)
  exact hh

theorem construction_disjoint_3_8 :
    ∀ p, ¬ (OpenSquare (constructionSquare 3) p ∧ OpenSquare (constructionSquare 8) p) := by
  have hh := separated_interiors (constructionSquare 3) (constructionSquare 8)
    (constructionSeparator 0) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_3_8)
  exact hh

theorem construction_disjoint_3_9 :
    ∀ p, ¬ (OpenSquare (constructionSquare 3) p ∧ OpenSquare (constructionSquare 9) p) := by
  have hh := separated_interiors (constructionSquare 3) (constructionSquare 9)
    (constructionSeparator 0) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_3_9)
  exact hh

theorem construction_disjoint_3_10 :
    ∀ p, ¬ (OpenSquare (constructionSquare 3) p ∧ OpenSquare (constructionSquare 10) p) := by
  have hh := separated_interiors (constructionSquare 3) (constructionSquare 10)
    (constructionSeparator 0) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_3_10)
  exact hh

theorem construction_disjoint_4_5 :
    ∀ p, ¬ (OpenSquare (constructionSquare 4) p ∧ OpenSquare (constructionSquare 5) p) := by
  have hh := separated_interiors (constructionSquare 5) (constructionSquare 4)
    (constructionSeparator 0) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_4_5)
  intro p hp
  exact hh p ⟨hp.2, hp.1⟩

theorem construction_disjoint_4_6 :
    ∀ p, ¬ (OpenSquare (constructionSquare 4) p ∧ OpenSquare (constructionSquare 6) p) := by
  have hh := separated_interiors (constructionSquare 6) (constructionSquare 4)
    (constructionSeparator 1) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_4_6)
  intro p hp
  exact hh p ⟨hp.2, hp.1⟩

theorem construction_disjoint_4_7 :
    ∀ p, ¬ (OpenSquare (constructionSquare 4) p ∧ OpenSquare (constructionSquare 7) p) := by
  have hh := separated_interiors (constructionSquare 7) (constructionSquare 4)
    (constructionSeparator 1) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_4_7)
  intro p hp
  exact hh p ⟨hp.2, hp.1⟩

theorem construction_disjoint_4_8 :
    ∀ p, ¬ (OpenSquare (constructionSquare 4) p ∧ OpenSquare (constructionSquare 8) p) := by
  have hh := separated_interiors (constructionSquare 8) (constructionSquare 4)
    (constructionSeparator 3) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_4_8)
  intro p hp
  exact hh p ⟨hp.2, hp.1⟩

theorem construction_disjoint_4_9 :
    ∀ p, ¬ (OpenSquare (constructionSquare 4) p ∧ OpenSquare (constructionSquare 9) p) := by
  have hh := separated_interiors (constructionSquare 9) (constructionSquare 4)
    (constructionSeparator 1) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_4_9)
  intro p hp
  exact hh p ⟨hp.2, hp.1⟩

theorem construction_disjoint_4_10 :
    ∀ p, ¬ (OpenSquare (constructionSquare 4) p ∧ OpenSquare (constructionSquare 10) p) := by
  have hh := separated_interiors (constructionSquare 4) (constructionSquare 10)
    (constructionSeparator 0) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_4_10)
  exact hh

theorem construction_disjoint_5_6 :
    ∀ p, ¬ (OpenSquare (constructionSquare 5) p ∧ OpenSquare (constructionSquare 6) p) := by
  have hh := separated_interiors (constructionSquare 6) (constructionSquare 5)
    (constructionSeparator 3) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_5_6)
  intro p hp
  exact hh p ⟨hp.2, hp.1⟩

theorem construction_disjoint_5_7 :
    ∀ p, ¬ (OpenSquare (constructionSquare 5) p ∧ OpenSquare (constructionSquare 7) p) := by
  have hh := separated_interiors (constructionSquare 5) (constructionSquare 7)
    (constructionSeparator 0) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_5_7)
  exact hh

theorem construction_disjoint_5_8 :
    ∀ p, ¬ (OpenSquare (constructionSquare 5) p ∧ OpenSquare (constructionSquare 8) p) := by
  have hh := separated_interiors (constructionSquare 5) (constructionSquare 8)
    (constructionSeparator 0) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_5_8)
  exact hh

theorem construction_disjoint_5_9 :
    ∀ p, ¬ (OpenSquare (constructionSquare 5) p ∧ OpenSquare (constructionSquare 9) p) := by
  have hh := separated_interiors (constructionSquare 5) (constructionSquare 9)
    (constructionSeparator 0) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_5_9)
  exact hh

theorem construction_disjoint_5_10 :
    ∀ p, ¬ (OpenSquare (constructionSquare 5) p ∧ OpenSquare (constructionSquare 10) p) := by
  have hh := separated_interiors (constructionSquare 5) (constructionSquare 10)
    (constructionSeparator 0) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_5_10)
  exact hh

theorem construction_disjoint_6_7 :
    ∀ p, ¬ (OpenSquare (constructionSquare 6) p ∧ OpenSquare (constructionSquare 7) p) := by
  have hh := separated_interiors (constructionSquare 7) (constructionSquare 6)
    (constructionSeparator 3) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_6_7)
  intro p hp
  exact hh p ⟨hp.2, hp.1⟩

theorem construction_disjoint_6_8 :
    ∀ p, ¬ (OpenSquare (constructionSquare 6) p ∧ OpenSquare (constructionSquare 8) p) := by
  have hh := separated_interiors (constructionSquare 6) (constructionSquare 8)
    (constructionSeparator 2) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_6_8)
  exact hh

theorem construction_disjoint_6_9 :
    ∀ p, ¬ (OpenSquare (constructionSquare 6) p ∧ OpenSquare (constructionSquare 9) p) := by
  have hh := separated_interiors (constructionSquare 6) (constructionSquare 9)
    (constructionSeparator 2) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_6_9)
  exact hh

theorem construction_disjoint_6_10 :
    ∀ p, ¬ (OpenSquare (constructionSquare 6) p ∧ OpenSquare (constructionSquare 10) p) := by
  have hh := separated_interiors (constructionSquare 6) (constructionSquare 10)
    (constructionSeparator 0) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_6_10)
  exact hh

theorem construction_disjoint_7_8 :
    ∀ p, ¬ (OpenSquare (constructionSquare 7) p ∧ OpenSquare (constructionSquare 8) p) := by
  have hh := separated_interiors (constructionSquare 7) (constructionSquare 8)
    (constructionSeparator 1) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_7_8)
  exact hh

theorem construction_disjoint_7_9 :
    ∀ p, ¬ (OpenSquare (constructionSquare 7) p ∧ OpenSquare (constructionSquare 9) p) := by
  have hh := separated_interiors (constructionSquare 7) (constructionSquare 9)
    (constructionSeparator 2) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_7_9)
  exact hh

theorem construction_disjoint_7_10 :
    ∀ p, ¬ (OpenSquare (constructionSquare 7) p ∧ OpenSquare (constructionSquare 10) p) := by
  have hh := separated_interiors (constructionSquare 7) (constructionSquare 10)
    (constructionSeparator 1) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_7_10)
  exact hh

theorem construction_disjoint_8_9 :
    ∀ p, ¬ (OpenSquare (constructionSquare 8) p ∧ OpenSquare (constructionSquare 9) p) := by
  have hh := separated_interiors (constructionSquare 9) (constructionSquare 8)
    (constructionSeparator 3) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_8_9)
  intro p hp
  exact hh p ⟨hp.2, hp.1⟩

theorem construction_disjoint_8_10 :
    ∀ p, ¬ (OpenSquare (constructionSquare 8) p ∧ OpenSquare (constructionSquare 10) p) := by
  have hh := separated_interiors (constructionSquare 8) (constructionSquare 10)
    (constructionSeparator 2) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_8_10)
  exact hh

theorem construction_disjoint_9_10 :
    ∀ p, ¬ (OpenSquare (constructionSquare 9) p ∧ OpenSquare (constructionSquare 10) p) := by
  have hh := separated_interiors (constructionSquare 9) (constructionSquare 10)
    (constructionSeparator 2) (by rw [construction_separator_unit]; norm_num)
    (by rw [construction_projectionRadius, construction_projectionRadius]
        exact sub_nonneg.mp construction_gap_9_10)
  exact hh

def constructionPacking : Packing 11 T where
  squares := constructionSquare
  side_nonneg := T_pos.le
  contained := construction_contained
  interior_disjoint := by
    intro i j hij
    fin_cases i <;> fin_cases j
    · exact (hij rfl).elim
    · exact construction_disjoint_0_1
    · exact construction_disjoint_0_2
    · exact construction_disjoint_0_3
    · exact construction_disjoint_0_4
    · exact construction_disjoint_0_5
    · exact construction_disjoint_0_6
    · exact construction_disjoint_0_7
    · exact construction_disjoint_0_8
    · exact construction_disjoint_0_9
    · exact construction_disjoint_0_10
    · intro p hp
      exact construction_disjoint_0_1 p ⟨hp.2, hp.1⟩
    · exact (hij rfl).elim
    · exact construction_disjoint_1_2
    · exact construction_disjoint_1_3
    · exact construction_disjoint_1_4
    · exact construction_disjoint_1_5
    · exact construction_disjoint_1_6
    · exact construction_disjoint_1_7
    · exact construction_disjoint_1_8
    · exact construction_disjoint_1_9
    · exact construction_disjoint_1_10
    · intro p hp
      exact construction_disjoint_0_2 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_1_2 p ⟨hp.2, hp.1⟩
    · exact (hij rfl).elim
    · exact construction_disjoint_2_3
    · exact construction_disjoint_2_4
    · exact construction_disjoint_2_5
    · exact construction_disjoint_2_6
    · exact construction_disjoint_2_7
    · exact construction_disjoint_2_8
    · exact construction_disjoint_2_9
    · exact construction_disjoint_2_10
    · intro p hp
      exact construction_disjoint_0_3 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_1_3 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_2_3 p ⟨hp.2, hp.1⟩
    · exact (hij rfl).elim
    · exact construction_disjoint_3_4
    · exact construction_disjoint_3_5
    · exact construction_disjoint_3_6
    · exact construction_disjoint_3_7
    · exact construction_disjoint_3_8
    · exact construction_disjoint_3_9
    · exact construction_disjoint_3_10
    · intro p hp
      exact construction_disjoint_0_4 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_1_4 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_2_4 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_3_4 p ⟨hp.2, hp.1⟩
    · exact (hij rfl).elim
    · exact construction_disjoint_4_5
    · exact construction_disjoint_4_6
    · exact construction_disjoint_4_7
    · exact construction_disjoint_4_8
    · exact construction_disjoint_4_9
    · exact construction_disjoint_4_10
    · intro p hp
      exact construction_disjoint_0_5 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_1_5 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_2_5 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_3_5 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_4_5 p ⟨hp.2, hp.1⟩
    · exact (hij rfl).elim
    · exact construction_disjoint_5_6
    · exact construction_disjoint_5_7
    · exact construction_disjoint_5_8
    · exact construction_disjoint_5_9
    · exact construction_disjoint_5_10
    · intro p hp
      exact construction_disjoint_0_6 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_1_6 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_2_6 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_3_6 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_4_6 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_5_6 p ⟨hp.2, hp.1⟩
    · exact (hij rfl).elim
    · exact construction_disjoint_6_7
    · exact construction_disjoint_6_8
    · exact construction_disjoint_6_9
    · exact construction_disjoint_6_10
    · intro p hp
      exact construction_disjoint_0_7 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_1_7 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_2_7 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_3_7 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_4_7 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_5_7 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_6_7 p ⟨hp.2, hp.1⟩
    · exact (hij rfl).elim
    · exact construction_disjoint_7_8
    · exact construction_disjoint_7_9
    · exact construction_disjoint_7_10
    · intro p hp
      exact construction_disjoint_0_8 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_1_8 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_2_8 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_3_8 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_4_8 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_5_8 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_6_8 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_7_8 p ⟨hp.2, hp.1⟩
    · exact (hij rfl).elim
    · exact construction_disjoint_8_9
    · exact construction_disjoint_8_10
    · intro p hp
      exact construction_disjoint_0_9 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_1_9 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_2_9 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_3_9 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_4_9 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_5_9 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_6_9 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_7_9 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_8_9 p ⟨hp.2, hp.1⟩
    · exact (hij rfl).elim
    · exact construction_disjoint_9_10
    · intro p hp
      exact construction_disjoint_0_10 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_1_10 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_2_10 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_3_10 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_4_10 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_5_10 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_6_10 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_7_10 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_8_10 p ⟨hp.2, hp.1⟩
    · intro p hp
      exact construction_disjoint_9_10 p ⟨hp.2, hp.1⟩
    · exact (hij rfl).elim

theorem construction_packable : Packable 11 T := ⟨constructionPacking⟩

/-- The construction attains the left wall and the bottom wall. -/
theorem construction_left_corner : ClosedSquare (constructionSquare 0) (0,0) := by
  have ha : (constructionSquare 0).axis = (1,0) := rfl
  simp only [ClosedSquare, localX, localY, ha, dot, perp]
  constructor <;> apply abs_le.mpr <;> constructor <;>
    norm_num [constructionSquare, constructionCenter]

/-- The construction attains the right wall. -/
theorem construction_right_corner : ClosedSquare (constructionSquare 1) (T,0) := by
  have ha : (constructionSquare 1).axis = (1,0) := rfl
  rw [← constructionSide_eq_T]
  simp only [ClosedSquare, localX, localY, ha, dot, perp]
  constructor <;> apply abs_le.mpr <;> constructor <;>
    norm_num [constructionSquare, constructionCenter, constructionSide]

/-- The construction attains the top wall. -/
theorem construction_top_corner : ClosedSquare (constructionSquare 3) (0,T) := by
  have ha : (constructionSquare 3).axis = (1,0) := rfl
  rw [← constructionSide_eq_T]
  simp only [ClosedSquare, localX, localY, ha, dot, perp]
  constructor <;> apply abs_le.mpr <;> constructor <;>
    norm_num [constructionSquare, constructionCenter, constructionSide]

/-- Any axis-parallel container holding these exact squares must have side at least T. -/
theorem construction_required_side {S : ℝ}
    (h : ∀ i p, ClosedSquare (constructionSquare i) p → InContainer S p) : T ≤ S := by
  exact (h 1 (T,0) construction_right_corner).2.1

end
end ElevenSquare
