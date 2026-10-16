import Mathlib.Analysis.SpecialFunctions.Trigonometric.Bounds
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Sq19Lean.Basic
import Sq19Lean.Wedge.CaseBB

/-!
# The four owner cases of the wedge bound

`PhiCase pa qa a11 a13 a14 o1 o2` is `phi` of `s19/tools/wedge_cert.c`: on the P side (13-14) the
separating normal is 13's (`pa = true`, case "a") or 14's (`pa = false`, case "b"), likewise on the
Q side (13-11) with 11. In case "a" the side constant is
`1 / (2 cos d) + 1/2 + g(d) + tan d * o` with the tangential offset `o` (wedge_cert.c convention).
`PhiCase false false` is `PhiBB` by definition.
-/

namespace Sq19.Wedge

open Real

noncomputable def f1C (pa : Bool) (a13 a14 : ℝ) : ℝ := cond pa (π / 4 + a13) (π / 4 + a14)
noncomputable def f2C (qa : Bool) (a13 a11 : ℝ) : ℝ := cond qa (π / 4 + a13) (π / 4 + a11)

/-- Side constant in owner case "a": `u.(Z - c13) >= 1/(2 cos d) + 1/2 + g(d) + tan(d) o`. -/
noncomputable def ownerA (d o : ℝ) : ℝ := 1 / (2 * cos d) + 1 / 2 + gk d + tan d * o

noncomputable def A1C (pa : Bool) (a13 a14 o1 : ℝ) : ℝ :=
  cond pa (ownerA ((π / 4 + a14) - (π / 4 + a13)) o1) (1 + gk ((π / 4 + a14) - (π / 4 + a13)))
noncomputable def A2C (qa : Bool) (a13 a11 o2 : ℝ) : ℝ :=
  cond qa (ownerA ((π / 4 + a11) - (π / 4 + a13)) o2) (1 + gk ((π / 4 + a11) - (π / 4 + a13)))

noncomputable def coefC (pa qa : Bool) (a11 a13 a14 : ℝ) : ℝ :=
  sin (f1C pa a13 a14) * (cos (f2C qa a13 a11) + sin (f2C qa a13 a11))
    + cos (f2C qa a13 a11) * cos (f1C pa a13 a14)

noncomputable def restC (pa qa : Bool) (a11 a13 a14 o1 o2 : ℝ) : ℝ :=
  cos (f1C pa a13 a14 - f2C qa a13 a11) * (2 + (|cos (π / 4 + a13)| + |sin (π / 4 + a13)|) / 2)
    + sin (f1C pa a13 a14) * A2C qa a13 a11 o2
    + cos (f2C qa a13 a11) * (2 * sin (f1C pa a13 a14) + A1C pa a13 a14 o1)

/-- The wedge bound of one owner case (least `L`). -/
noncomputable def PhiCase (pa qa : Bool) (a11 a13 a14 o1 o2 : ℝ) : ℝ :=
  1 + restC pa qa a11 a13 a14 o1 o2 / coefC pa qa a11 a13 a14

theorem PhiCase_false_false (a11 a13 a14 o1 o2 : ℝ) :
    PhiCase false false a11 a13 a14 o1 o2 = PhiBB a11 a13 a14 := by
  simp only [PhiCase, PhiBB, restC, restBB, coefC, coefBB, A1C, A2C, f1C, f2C, Bool.cond_false]
  ring

/-- Trigonometric bounds on the capture box used by every case. -/
theorem capture_facts {a11 a13 a14 : ℝ}
    (h11l : -1661/10000 ≤ a11) (h11h : a11 ≤ 1140/10000)
    (h13l : -1377/10000 ≤ a13) (h13h : a13 ≤ 82/10000)
    (h14l : -2292/10000 ≤ a14) (h14h : a14 ≤ 82/10000) :
    (9905/10000 : ℝ) ≤ cos a13 ∧ (-1377/10000 : ℝ) ≤ sin a13 ∧ sin a13 ≤ 82/10000 ∧
    (9718/10000 : ℝ) ≤ cos (a14 - a13) ∧ (-2374/10000 : ℝ) ≤ sin (a14 - a13) ∧
      sin (a14 - a13) ≤ 1459/10000 ∧
    (9683/10000 : ℝ) ≤ cos (a11 - a13) ∧ (-1743/10000 : ℝ) ≤ sin (a11 - a13) ∧
      sin (a11 - a13) ≤ 2517/10000 ∧
    (97/100 : ℝ) ≤ cos a14 ∧ (-2292/10000 : ℝ) ≤ sin a14 ∧ sin a14 ≤ 82/10000 ∧
    (98/100 : ℝ) ≤ cos a11 ∧ (-1661/10000 : ℝ) ≤ sin a11 ∧ sin a11 ≤ 1140/10000 := by
  have hpi := pi_gt_three
  have hpl : (-2374/10000 : ℝ) ≤ a14 - a13 := by linarith
  have hph : a14 - a13 ≤ (1459/10000 : ℝ) := by linarith
  have hql : (-1743/10000 : ℝ) ≤ a11 - a13 := by linarith
  have hqh : a11 - a13 ≤ (2517/10000 : ℝ) := by linarith
  refine ⟨cos_lo h13l h13h (by norm_num) (by norm_num) (by norm_num) (by norm_num),
    sin_lo h13l (by norm_num) (by linarith) (by linarith),
    sin_hi h13h (by norm_num) (by linarith) (by linarith),
    cos_lo hpl hph (by norm_num) (by norm_num) (by norm_num) (by norm_num),
    sin_lo hpl (by norm_num) (by linarith) (by linarith),
    sin_hi hph (by norm_num) (by linarith) (by linarith),
    cos_lo hql hqh (by norm_num) (by norm_num) (by norm_num) (by norm_num),
    sin_lo hql (by norm_num) (by linarith) (by linarith),
    sin_hi hqh (by norm_num) (by linarith) (by linarith),
    cos_lo h14l h14h (by norm_num) (by norm_num) (by norm_num) (by norm_num),
    sin_lo h14l (by norm_num) (by linarith) (by linarith),
    sin_hi h14h (by norm_num) (by linarith) (by linarith),
    cos_lo h11l h11h (by norm_num) (by norm_num) (by norm_num) (by norm_num),
    sin_lo h11l (by norm_num) (by linarith) (by linarith),
    sin_hi h11h (by norm_num) (by linarith) (by linarith)⟩

theorem angle_add_facts (a11 a13 a14 : ℝ) :
    cos a14 = cos a13 * cos (a14 - a13) - sin a13 * sin (a14 - a13) ∧
    sin a14 = sin a13 * cos (a14 - a13) + cos a13 * sin (a14 - a13) ∧
    cos a11 = cos a13 * cos (a11 - a13) - sin a13 * sin (a11 - a13) ∧
    sin a11 = sin a13 * cos (a11 - a13) + cos a13 * sin (a11 - a13) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · rw [← cos_add]; ring_nf
  · rw [← sin_add]; ring_nf
  · rw [← cos_add]; ring_nf
  · rw [← sin_add]; ring_nf

end Sq19.Wedge
