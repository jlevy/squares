import Mathlib.Topology.MetricSpace.Contracting
import Mathlib.Tactic

/-! Finite rational bivariate coefficient certificates for Banach's theorem.
The coefficient tests are sufficient conditions, evaluated in the Lean kernel. -/
namespace Sq17.PolynomialBox

structure Term where
  xDegree : ℕ
  yDegree : ℕ
  coeff : ℚ
  deriving DecidableEq

noncomputable def Term.eval (t : Term) (p : ℝ × ℝ) : ℝ :=
  t.coeff*p.1^t.xDegree*p.2^t.yDegree
noncomputable def eval : List Term → (ℝ × ℝ) → ℝ
  | [], _ => 0
  | t::ts,p => t.eval p+eval ts p

def mass : List Term → ℚ
  | [] => 0
  | t::ts => |t.coeff|+mass ts

def slope : List Term → ℚ
  | [] => 0
  | t::ts => |t.coeff| *(t.xDegree+t.yDegree)+slope ts

def box : Set (ℝ × ℝ) := {p | |p.1| ≤ 1 ∧ |p.2| ≤ 1}

theorem pow_bound (x : ℝ) (hx : |x| ≤ 1) (n : ℕ) : |x^n| ≤ 1 := by
  rw [abs_pow]
  exact pow_le_one₀ (abs_nonneg x) hx

theorem pow_difference (x y : ℝ) (hx : |x| ≤ 1) (hy : |y| ≤ 1) (n : ℕ) :
    |x^n-y^n| ≤ n*|x-y| := by
  have h := abs_pow_sub_pow_le x y n
  have hp : max |x| |y| ^ (n-1) ≤ 1 :=
    pow_le_one₀ (le_max_of_le_left (abs_nonneg x)) (max_le hx hy)
  have hmul := mul_le_mul_of_nonneg_left hp (mul_nonneg (abs_nonneg (x-y)) (Nat.cast_nonneg n))
  nlinarith only [h,hmul]

theorem term_bound (t : Term) (p : ℝ × ℝ) (hp : p ∈ box) :
    |t.eval p| ≤ |(t.coeff : ℝ)| := by
  unfold Term.eval
  rw [abs_mul,abs_mul]
  have hx := pow_bound p.1 hp.1 t.xDegree
  have hy := pow_bound p.2 hp.2 t.yDegree
  calc
    _ ≤ |(t.coeff : ℝ)| *1*1 := mul_le_mul
      (mul_le_mul_of_nonneg_left hx (abs_nonneg _)) hy (abs_nonneg _) (by positivity)
    _ = _ := by ring

theorem term_difference (t : Term) (p q : ℝ × ℝ) (hp : p ∈ box) (hq : q ∈ box) :
    |t.eval p-t.eval q| ≤ (|(t.coeff : ℝ)| *(t.xDegree+t.yDegree))*dist p q := by
  let D := dist p q
  have hxD : |p.1-q.1| ≤ D := le_max_left _ _
  have hyD : |p.2-q.2| ≤ D := le_max_right _ _
  have hx := pow_difference p.1 q.1 hp.1 hq.1 t.xDegree
  have hy := pow_difference p.2 q.2 hp.2 hq.2 t.yDegree
  have hx' : |p.1^t.xDegree-q.1^t.xDegree| ≤ t.xDegree*D :=
    hx.trans (mul_le_mul_of_nonneg_left hxD (Nat.cast_nonneg _))
  have hy' : |p.2^t.yDegree-q.2^t.yDegree| ≤ t.yDegree*D :=
    hy.trans (mul_le_mul_of_nonneg_left hyD (Nat.cast_nonneg _))
  have hpY := pow_bound p.2 hp.2 t.yDegree
  have hqX := pow_bound q.1 hq.1 t.xDegree
  have hprod : |p.1^t.xDegree*p.2^t.yDegree-q.1^t.xDegree*q.2^t.yDegree| ≤
      (t.xDegree+t.yDegree)*D := by
    have he : p.1^t.xDegree*p.2^t.yDegree-q.1^t.xDegree*q.2^t.yDegree =
        (p.1^t.xDegree-q.1^t.xDegree)*p.2^t.yDegree+
        q.1^t.xDegree*(p.2^t.yDegree-q.2^t.yDegree) := by ring
    rw [he]
    have ht := abs_add_le ((p.1^t.xDegree-q.1^t.xDegree)*p.2^t.yDegree)
      (q.1^t.xDegree*(p.2^t.yDegree-q.2^t.yDegree))
    rw [abs_mul,abs_mul] at ht
    have h1 := mul_le_mul hx' hpY (abs_nonneg _) (by positivity : (0:ℝ) ≤ t.xDegree*D)
    have h2 := mul_le_mul hqX hy' (abs_nonneg _) (by norm_num : (0:ℝ) ≤ 1)
    nlinarith only [ht,h1,h2]
  have h := mul_le_mul_of_nonneg_left hprod (abs_nonneg (t.coeff : ℝ))
  have he : t.eval p-t.eval q = (t.coeff : ℝ)*
      (p.1^t.xDegree*p.2^t.yDegree-q.1^t.xDegree*q.2^t.yDegree) := by unfold Term.eval; ring
  rw [he,abs_mul]
  nlinarith only [h]

theorem eval_bound (ts : List Term) (p : ℝ × ℝ) (hp : p ∈ box) :
    |eval ts p| ≤ (mass ts : ℝ) := by
  induction ts with
  | nil => simp [eval,mass]
  | cons t ts ih =>
    have h := (abs_add_le (t.eval p) (eval ts p)).trans (add_le_add (term_bound t p hp) ih)
    simpa only [eval,mass,Rat.cast_add,Rat.cast_abs] using h

theorem eval_difference (ts : List Term) (p q : ℝ × ℝ) (hp : p ∈ box) (hq : q ∈ box) :
    |eval ts p-eval ts q| ≤ (slope ts : ℝ)*dist p q := by
  induction ts with
  | nil => simp [eval,slope]
  | cons t ts ih =>
    have he : eval (t::ts) p-eval (t::ts) q = (t.eval p-t.eval q)+(eval ts p-eval ts q) := by simp only [eval]; ring
    rw [he]
    have h := (abs_add_le _ _).trans (add_le_add (term_difference t p q hp hq) ih)
    simpa only [slope,Rat.cast_add,Rat.cast_mul,Rat.cast_abs,Rat.cast_natCast,add_mul] using h

def check (f g : List Term) : Bool := decide (mass f ≤ 1 ∧ mass g ≤ 1 ∧ slope f ≤ 1/2 ∧ slope g ≤ 1/2)

theorem check_unique_fixed (f g : List Term) (hc : check f g = true) :
    ∃! p : ℝ × ℝ, p ∈ box ∧ (eval f p,eval g p) = p := by
  have hq : mass f ≤ 1 ∧ mass g ≤ 1 ∧ slope f ≤ 1/2 ∧ slope g ≤ 1/2 := of_decide_eq_true hc
  have hr0 := (Rat.cast_le (K := ℝ)).mpr hq.2.2.1
  have hr1 := (Rat.cast_le (K := ℝ)).mpr hq.2.2.2
  norm_num only [Rat.cast_div,Rat.cast_ofNat] at hr0 hr1
  have hr : (mass f : ℝ) ≤ 1 ∧ (mass g : ℝ) ≤ 1 ∧ (slope f : ℝ) ≤ 1/2 ∧ (slope g : ℝ) ≤ 1/2 :=
    ⟨by exact_mod_cast hq.1,by exact_mod_cast hq.2.1,hr0,hr1⟩
  have hclosed : IsClosed box := by
    change IsClosed ({p : ℝ × ℝ | |p.1| ≤ 1} ∩ {p : ℝ × ℝ | |p.2| ≤ 1})
    exact (isClosed_le (by fun_prop) continuous_const).inter (isClosed_le (by fun_prop) continuous_const)
  letI : CompleteSpace box := hclosed.completeSpace_coe
  letI : Nonempty box := ⟨⟨(0,0),by norm_num [box]⟩⟩
  let F : box → box := fun p => ⟨(eval f p,eval g p),
    (eval_bound f p p.property).trans hr.1,(eval_bound g p p.property).trans hr.2.1⟩
  have hF : ContractingWith (1/2) F := by
    refine ⟨by norm_num,LipschitzWith.of_dist_le_mul ?_⟩
    intro p q
    change max |eval f p-eval f q| |eval g p-eval g q| ≤ (1/2:ℝ)*dist (p:ℝ×ℝ) q
    apply max_le
    · exact (eval_difference f p q p.property q.property).trans
        (mul_le_mul_of_nonneg_right hr.2.2.1 dist_nonneg)
    · exact (eval_difference g p q p.property q.property).trans
        (mul_le_mul_of_nonneg_right hr.2.2.2 dist_nonneg)
  refine ⟨(hF.fixedPoint F).val,⟨(hF.fixedPoint F).property,?_⟩,?_⟩
  · exact congrArg Subtype.val hF.fixedPoint_isFixedPt
  · intro q hq
    have hfix : Function.IsFixedPt F ⟨q,hq.1⟩ := Subtype.ext hq.2
    exact congrArg Subtype.val (hF.fixedPoint_unique hfix)

end Sq17.PolynomialBox
#print axioms Sq17.PolynomialBox.check_unique_fixed
