import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.Deriv.MeanValue
import Mathlib.Topology.Order.IntermediateValue
import Mathlib.Tactic.FunProp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Positivity

/-! Exact algebraic endpoint. No numerical oracle is part of these proofs. -/
namespace ElevenSquare
noncomputable section

def endpointPolynomial (x : ℝ) : ℝ := 5 * x^8 - 10 * x^7 - 2 * x^6 + 14 * x^5 + 12 * x^4 - 6 * x^3 + 2 * x^2 + 2 * x - 1
def endpointDerivative (x : ℝ) : ℝ := 40 * x^7 - 70 * x^6 - 12 * x^5 + 70 * x^4 + 48 * x^3 - 18 * x^2 + 4 * x + 2
def rootLo : ℝ := 365769307604677293388545018143 / 1000000000000000000000000000000
def rootHi : ℝ := 365769307604677293388545018144 / 1000000000000000000000000000000
def U : ℝ := 387708359002281417731 / 100000000000000000000

theorem endpointPolynomial_continuous : Continuous endpointPolynomial := by
  unfold endpointPolynomial
  fun_prop

theorem endpoint_hasDerivAt (x : ℝ) :
    HasDerivAt endpointPolynomial (endpointDerivative x) x := by
  convert ((((((((((hasDerivAt_id x).pow 8).const_mul 5).sub (((hasDerivAt_id x).pow 7).const_mul 10)).sub (((hasDerivAt_id x).pow 6).const_mul 2)).add (((hasDerivAt_id x).pow 5).const_mul 14)).add (((hasDerivAt_id x).pow 4).const_mul 12)).sub (((hasDerivAt_id x).pow 3).const_mul 6)).add (((hasDerivAt_id x).pow 2).const_mul 2)).add ((hasDerivAt_id x).const_mul 2)).sub_const 1 using 1 <;> (try funext y) <;> simp [endpointPolynomial, endpointDerivative] <;> ring

/-- A small-coefficient decomposition of the endpoint derivative. -/
theorem endpointDerivative_decomposition (x : ℝ) :
    endpointDerivative x = (2 - 9 * x^2) + x * (4 - 9 * x) +
      12 * x^3 * (4 - x^2) + 70 * x^4 * (1 - x^2) + 40 * x^7 := by
  unfold endpointDerivative
  ring

/-- Positivity holds on an interval wider than the root-isolation interval. -/
theorem endpointDerivative_pos_broad {x : ℝ}
    (hx : x ∈ Set.Icc (0 : ℝ) (2/5)) : 0 < endpointDerivative x := by
  have hx0 : 0 ≤ x := hx.1
  have hx_upper : x ≤ (2/5 : ℝ) := hx.2
  have hx_sq : x^2 ≤ (4/25 : ℝ) := by
    nlinarith [mul_nonneg hx0 (sub_nonneg.mpr hx_upper)]
  have hconstant : 0 < 2 - 9 * x^2 := by linarith
  have hlinear : 0 ≤ 4 - 9 * x := by linarith
  have hcubic : 0 ≤ 4 - x^2 := by linarith
  have hquartic : 0 ≤ 1 - x^2 := by linarith
  rw [endpointDerivative_decomposition]
  positivity

theorem endpointDerivative_pos {x : ℝ} (hx : x ∈ Set.Icc (9/25 : ℝ) (37/100)) :
    0 < endpointDerivative x := by
  apply endpointDerivative_pos_broad
  constructor <;> linarith [hx.1, hx.2]

theorem endpointPolynomial_strictMono :
    StrictMonoOn endpointPolynomial (Set.Icc (9/25 : ℝ) (37/100)) := by
  apply strictMonoOn_of_deriv_pos (convex_Icc _ _) endpointPolynomial_continuous.continuousOn
  intro x hx
  rw [(endpoint_hasDerivAt x).deriv]
  exact endpointDerivative_pos (Set.mem_of_mem_of_subset hx interior_subset)

theorem rootLo_lt_rootHi : rootLo < rootHi := by norm_num [rootLo, rootHi]
theorem rootLo_in_interval : (9/25 : ℝ) < rootLo := by norm_num [rootLo]
theorem rootHi_in_interval : rootHi < (37/100 : ℝ) := by norm_num [rootHi]
theorem endpoint_at_lo : endpointPolynomial rootLo < 0 := by
  norm_num [endpointPolynomial, rootLo]
theorem endpoint_at_hi : 0 < endpointPolynomial rootHi := by
  norm_num [endpointPolynomial, rootHi]

theorem endpoint_root_exists : ∃ x ∈ Set.Ioo rootLo rootHi, endpointPolynomial x = 0 := by
  obtain ⟨x, hx, hp⟩ := intermediate_value_Icc rootLo_lt_rootHi.le
    endpointPolynomial_continuous.continuousOn ⟨endpoint_at_lo.le, endpoint_at_hi.le⟩
  refine ⟨x, ⟨?_, ?_⟩, hp⟩
  · rcases hx.1.eq_or_lt with h | h
    · subst x
      linarith [endpoint_at_lo]
    · exact h
  · rcases hx.2.eq_or_lt with h | h
    · subst x
      linarith [endpoint_at_hi]
    · exact h

def u : ℝ := Classical.choose endpoint_root_exists
theorem u_bounds : u ∈ Set.Ioo rootLo rootHi :=
  (Classical.choose_spec endpoint_root_exists).1
theorem u_polynomial : endpointPolynomial u = 0 :=
  (Classical.choose_spec endpoint_root_exists).2
theorem u_broad_bounds : u ∈ Set.Ioo (9/25 : ℝ) (37/100) :=
  ⟨lt_trans rootLo_in_interval u_bounds.1, lt_trans u_bounds.2 rootHi_in_interval⟩
theorem u_unique {x : ℝ} (hx : x ∈ Set.Icc (9/25 : ℝ) (37/100))
    (hp : endpointPolynomial x = 0) : x = u := by
  apply endpointPolynomial_strictMono.injOn hx
    ⟨u_broad_bounds.1.le, u_broad_bounds.2.le⟩
  rw [hp, u_polynomial]

def T : ℝ := (6*u+4)/(1+2*u-u^2)

theorem endpoint_denominator_pos : 0 < 1 + 2*u - u^2 := by
  have hlo := u_broad_bounds.1
  have hhi := u_broad_bounds.2
  have hmul := mul_nonneg (show 0 ≤ u by linarith) (show 0 ≤ 37/100-u by linarith)
  nlinarith

theorem T_pos : 0 < T := by
  unfold T
  apply div_pos _ endpoint_denominator_pos
  have h := u_broad_bounds.1
  linarith

end
end ElevenSquare
