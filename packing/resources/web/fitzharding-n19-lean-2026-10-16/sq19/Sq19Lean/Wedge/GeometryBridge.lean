import Sq19Lean.Wedge.CaseOffsets

/-!
# From the three axis-zero rows to the wedge bound

These are the P, Q and floor rows after the six axis-square angles are set to
zero. The anchor corners are `(2, L-1)` and `(L-1, L-1)` and the floor is at
height 2. Multiplying the rows by `cos f2`, `sin f1`, and `cos (f1-f2)` eliminates
the centre of square 13. This proves that the expression bounded by the wedge
certificates is exactly the required geometric lower bound, in all four owner
cases. The hypotheses are genuine half-plane constraints, not `PhiCase ≤ L`.

Deriving these rows from a packing, and relating nonzero axis angles to zero,
remain separate geometric and monotonicity obligations.
-/

namespace Sq19.Wedge
open Real

/-- The three axis-zero half-planes for the centre of square 13. -/
def ZeroAxisRows (pa qa : Bool) (a11 a13 a14 o1 o2 x y L : ℝ) : Prop :=
  (-sin (f1C pa a13 a14) * x + cos (f1C pa a13 a14) * y ≤
    cos (f1C pa a13 a14) * (L - 1) - 2 * sin (f1C pa a13 a14) - A1C pa a13 a14 o1) ∧
  (cos (f2C qa a13 a11) * x + sin (f2C qa a13 a11) * y ≤
    (cos (f2C qa a13 a11) + sin (f2C qa a13 a11)) * (L - 1) - A2C qa a13 a11 o2) ∧
  (2 + (|cos (π / 4 + a13)| + |sin (π / 4 + a13)|) / 2 ≤ y)

/-- Algebraic elimination of the centre; owner choices are arbitrary. -/
theorem PhiCase_le_of_zeroAxisRows (pa qa : Bool) {a11 a13 a14 o1 o2 x y L : ℝ}
    (hrows : ZeroAxisRows pa qa a11 a13 a14 o1 o2 x y L)
    (hP : 0 ≤ cos (f2C qa a13 a11))
    (hQ : 0 ≤ sin (f1C pa a13 a14))
    (hF : 0 ≤ cos (f1C pa a13 a14 - f2C qa a13 a11))
    (hcoef : 0 < coefC pa qa a11 a13 a14) :
    PhiCase pa qa a11 a13 a14 o1 o2 ≤ L := by
  obtain ⟨hp, hq, hf⟩ := hrows
  have mp := mul_le_mul_of_nonneg_left hp hP
  have mq := mul_le_mul_of_nonneg_left hq hQ
  have mf := mul_le_mul_of_nonneg_left hf hF
  have hbound : restC pa qa a11 a13 a14 o1 o2 ≤ coefC pa qa a11 a13 a14 * (L - 1) := by
    simp only [restC, coefC, cos_sub] at mf ⊢
    nlinarith only [mp, mq, mf]
  have hdiv : restC pa qa a11 a13 a14 o1 o2 / coefC pa qa a11 a13 a14 ≤ L - 1 := by
    apply (div_le_iff₀ hcoef).2
    nlinarith only [hbound]
  unfold PhiCase
  linarith only [hdiv]

/-- Both components of a tilted face normal are positive throughout the hull. -/
theorem tilted_normal_pos {a : ℝ} (ha : |a| ≤ 82/10000) :
    0 < cos (π / 4 + a) ∧ 0 < sin (π / 4 + a) := by
  obtain ⟨hal, hah⟩ := abs_le.mp ha
  have hpi := pi_gt_three
  exact ⟨cos_pos_of_mem_Ioo ⟨by linarith, by linarith⟩,
    sin_pos_of_pos_of_lt_pi (by linarith) (by linarith)⟩

/-- The multiplier and denominator signs follow from the hull's angle box. -/
theorem zeroAxis_multiplier_pos (pa qa : Bool) {a11 a13 a14 : ℝ}
    (h11 : |a11| ≤ 82/10000) (h13 : |a13| ≤ 82/10000) (h14 : |a14| ≤ 82/10000) :
    0 < cos (f2C qa a13 a11) ∧ 0 < sin (f1C pa a13 a14) ∧
    0 < cos (f1C pa a13 a14 - f2C qa a13 a11) ∧
    0 < coefC pa qa a11 a13 a14 := by
  have hf1 : 0 < cos (f1C pa a13 a14) ∧ 0 < sin (f1C pa a13 a14) := by
    cases pa
    · exact tilted_normal_pos h14
    · exact tilted_normal_pos h13
  have hf2 : 0 < cos (f2C qa a13 a11) ∧ 0 < sin (f2C qa a13 a11) := by
    cases qa
    · exact tilted_normal_pos h11
    · exact tilted_normal_pos h13
  refine ⟨hf2.1, hf1.2, ?_, ?_⟩
  · rw [cos_sub]
    exact add_pos (mul_pos hf1.1 hf2.1) (mul_pos hf1.2 hf2.2)
  · unfold coefC
    exact add_pos (mul_pos hf1.2 (add_pos hf2.1 hf2.2)) (mul_pos hf2.1 hf1.1)

/-- No multiplier-sign assumptions remain on the actual hull angle range. -/
theorem PhiCase_le_of_zeroAxisRows_hull (pa qa : Bool) {a11 a13 a14 o1 o2 x y L : ℝ}
    (h11 : |a11| ≤ 82/10000) (h13 : |a13| ≤ 82/10000) (h14 : |a14| ≤ 82/10000)
    (hrows : ZeroAxisRows pa qa a11 a13 a14 o1 o2 x y L) :
    PhiCase pa qa a11 a13 a14 o1 o2 ≤ L := by
  obtain ⟨hP, hQ, hF, hcoef⟩ := zeroAxis_multiplier_pos pa qa h11 h13 h14
  exact PhiCase_le_of_zeroAxisRows pa qa hrows hP.le hQ.le hF.le hcoef

/-- The three axis-zero rows, with hull angles and offsets, force the endpoint. -/
theorem side19_le_of_zeroAxisRows_hull (pa qa : Bool) {a11 a13 a14 o1 o2 x y L : ℝ}
    (h11 : |a11| ≤ 82/10000) (h13 : |a13| ≤ 82/10000) (h14 : |a14| ≤ 82/10000)
    (ho1l : 1589/10000 ≤ o1) (ho1h : o1 ≤ 2893/10000)
    (ho2l : -1322/10000 ≤ o2) (ho2h : o2 ≤ 365/10000)
    (hrows : ZeroAxisRows pa qa a11 a13 a14 o1 o2 x y L) : side19 ≤ L := by
  exact (wedge_hull pa qa h11 h13 h14 ho1l ho1h ho2l ho2h).trans
    (PhiCase_le_of_zeroAxisRows_hull pa qa h11 h13 h14 hrows)

/-- Positive control: at the record the row system has an exact solution, for
all four owner choices. Offsets drop out when the relative tilted angles vanish. -/
theorem zeroAxisRows_record (pa qa : Bool) (o1 o2 : ℝ) :
    ZeroAxisRows pa qa 0 0 0 o1 o2 (2 + 2 * √2 / 3) (2 + √2 / 2) side19 := by
  have hs : √2 ^ 2 = 2 := sq_sqrt (by norm_num)
  have hn : 0 ≤ √2 / 2 := by positivity
  cases pa <;> cases qa <;>
    norm_num [ZeroAxisRows, f1C, f2C, A1C, A2C, ownerA, gk, side19,
      cos_pi_div_four, sin_pi_div_four, abs_of_nonneg hn] <;>
    (try constructor) <;> nlinarith only [hs]

end Sq19.Wedge

#print axioms Sq19.Wedge.PhiCase_le_of_zeroAxisRows
#print axioms Sq19.Wedge.zeroAxis_multiplier_pos
#print axioms Sq19.Wedge.side19_le_of_zeroAxisRows_hull

#print axioms Sq19.Wedge.zeroAxisRows_record
