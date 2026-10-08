import ElevenSquare.Endpoint

/-! Exact inequalities linking the algebraic endpoint to the rational search cap. -/
namespace ElevenSquare

theorem U_pos : 0 < U := by norm_num [U]

theorem U_lt_four : U < 4 := by norm_num [U]

theorem T_lt_U : T < U := by
  unfold T
  apply (div_lt_iff₀ endpoint_denominator_pos).2
  have hhi : 0 < U * (1 + 2 * rootHi - rootHi^2) - (6 * rootHi + 4) := by
    norm_num [U, rootHi]
  have hm : 0 < U * (u + rootHi) + 6 - 2 * U := by
    have hu := u_broad_bounds.1
    norm_num [U, rootHi] at *
    linarith
  have hp := mul_pos (sub_pos.mpr u_bounds.2) hm
  nlinarith

theorem T_lt_four : T < 4 := lt_trans T_lt_U U_lt_four

theorem lower_search_bound_lt_T : (191 / 50 : ℝ) < T := by
  unfold T
  apply (lt_div_iff₀ endpoint_denominator_pos).2
  have hu := u_broad_bounds.1
  nlinarith [sq_nonneg (u - 9 / 25)]

end ElevenSquare
