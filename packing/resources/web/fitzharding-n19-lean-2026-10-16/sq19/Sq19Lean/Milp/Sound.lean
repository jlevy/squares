import Sq19Lean.Milp.Tree

/-!
# Soundness of the certificate check

A configuration gives every square `q` an angle `angOf θ q = q.m π/4 + θ q.s` and a centre
`cenOf dx dy q = (q.rx + dx q.s, q.ry + dy q.s)`. `checkCert_sound`: if `checkCert P text = true`,
no configuration with relative angles and offsets in the boxes of `P`, every square inside
`[0, L]^2`, pairwise disjoint interiors and `L ≤ side19` exists.
-/
namespace Sq19.Milp
open Sq17.Propagation

noncomputable def angOf (θ : ℕ → ℝ) (q : Sq) : ℝ := q.m * Real.pi / 4 + θ q.s
noncomputable def cenOf (dx dy : ℕ → ℝ) (q : Sq) : ℝ × ℝ := (q.rx + dx q.s, q.ry + dy q.s)

theorem oxq_cast (j : Fin 4) : ((oxq j : ℚ) : ℝ) = ox j := by
  unfold oxq ox; split_ifs <;> norm_num
theorem oyq_cast (j : Fin 4) : ((oyq j : ℚ) : ℝ) = oy j := by
  unfold oyq oy; split_ifs <;> norm_num

theorem vxE_real (θ : ℕ → ℝ) (q : Sq) (j : Fin 4) : (vxE q j).real θ = vx (angOf θ q) j := by
  simp only [vxE, Ex.real, vx, angOf, oxq_cast, oyq_cast]; ring
theorem vyE_real (θ : ℕ → ℝ) (q : Sq) (j : Fin 4) : (vyE q j).real θ = vy (angOf θ q) j := by
  simp only [vyE, Ex.real, vy, angOf, oxq_cast, oyq_cast]; ring
theorem nxE_real (θ : ℕ → ℝ) (A : Sq) (k : ℕ) : (nxE A k).real θ = nx (angOf θ A) k := by
  simp only [nxE, Ex.real, nx, angOf]; congr 1; push_cast; ring
theorem nyE_real (θ : ℕ → ℝ) (A : Sq) (k : ℕ) : (nyE A k).real θ = ny (angOf θ A) k := by
  simp only [nyE, Ex.real, ny, angOf]; congr 1; push_cast; ring
theorem cs_real (θ : ℕ → ℝ) (B : Sq) : (Ex.cs B.s B.m).real θ = Real.cos (angOf θ B) := rfl
theorem sn_real (θ : ℕ → ℝ) (B : Sq) : (Ex.sn B.s B.m).real θ = Real.sin (angOf θ B) := rfl

/-- Angles inside a box of intervals. -/
def InAng (θ : ℕ → ℝ) (ang : ℕ → Iv) : Prop := ∀ k, Iv.mem (θ k) (ang k)

theorem boxH_bound {θ : ℕ → ℝ} {ang : ℕ → Iv} (h : InAng θ ang) (k : ℕ) :
    |θ k - (boxTrig ang).cen k| ≤ (boxH ang k : ℝ) := Iv.abs_sub_mid (h k)

theorem boxTrig_shift (θ : ℕ → ℝ) (ang : ℕ → Iv) :
    (fun s => ((boxTrig ang).cen s : ℝ) + (θ s - (boxTrig ang).cen s)) = θ := by
  funext s; ring

theorem boxTrig_valid (ang : ℕ → Iv) : (boxTrig ang).Valid := Trig.ofCentres_valid _ _

/-- Every expression lies in its Taylor range on the box. -/
theorem ex_mem_range {θ : ℕ → ℝ} {ang : ℕ → Iv} (h : InAng θ ang) (e : Ex) :
    Iv.mem (e.real θ) ((e.tf (boxTrig ang) (boxH ang)).range (boxH ang)) := by
  have hm := TF.mem_range (Ex.tf_encl (boxTrig_valid ang) (boxH ang) e)
    (fun k => θ k - (boxTrig ang).cen k) (boxH_bound h)
  rw [boxTrig_shift θ ang] at hm
  exact hm

theorem mem_dIv {rA rB : ℚ} {IA IB : Iv} {a b : ℝ} (ha : Iv.mem a IA) (hb : Iv.mem b IB) :
    Iv.mem ((rB + b) - (rA + a)) (dIv rA rB IA IB) := by
  simp only [Iv.mem, dIv]; push_cast
  exact ⟨by linarith [ha.2, hb.1], by linarith [ha.1, hb.2]⟩

/-- Offsets inside the position boxes. -/
def InPos (dx dy : ℕ → ℝ) (q : Sq) : Prop := Iv.mem (dx q.s) q.x ∧ Iv.mem (dy q.s) q.y

/-- **Face test soundness.** A face that separates somewhere on the box passes the test. -/
theorem facePossible_sound {θ dx dy : ℕ → ℝ} {ang : ℕ → Iv} (hθ : InAng θ ang) (A B : Sq)
    (hA : InPos dx dy A) (hB : InPos dx dy B) (k : ℕ)
    (hsep : Sep (cenOf dx dy A) (angOf θ A) (cenOf dx dy B) (angOf θ B) k) :
    facePossible (boxTrig ang) (boxH ang) A B k = true := by
  have hs := sep_support _ _ _ _ k hsep
  simp only [cenOf] at hs
  set n1 := nx (angOf θ A) k
  set n2 := ny (angOf θ A) k
  set T := boxTrig ang
  set H := boxH ang
  -- the projection interval
  have hproj : Iv.mem (n1 * ((B.rx + dx B.s) - (A.rx + dx A.s)) + n2 * ((B.ry + dy B.s) - (A.ry + dy A.s)))
      (((((nxE A k).tf T H).range H).mul (dIv A.rx B.rx A.x B.x)).add
        ((((nyE A k).tf T H).range H).mul (dIv A.ry B.ry A.y B.y))) := by
    have h1 := ex_mem_range hθ (nxE A k)
    have h2 := ex_mem_range hθ (nyE A k)
    rw [nxE_real] at h1; rw [nyE_real] at h2
    exact Iv.mem_add (Iv.mem_mul h1 (mem_dIv hA.1 hB.1)) (Iv.mem_mul h2 (mem_dIv hA.2 hB.2))
  -- the support lower bound
  set Pr := n1 * Real.cos (angOf θ B) + n2 * Real.sin (angOf θ B)
  set Qr := -n1 * Real.sin (angOf θ B) + n2 * Real.cos (angOf θ B)
  have hunit : Pr^2 + Qr^2 = 1 := by
    have h1 := Real.sin_sq_add_cos_sq (angOf θ B)
    have h2 : n1^2 + n2^2 = 1 := by
      simp only [n1, n2, nx, ny]; rw [add_comm]; exact Real.sin_sq_add_cos_sq _
    simp only [Pr, Qr]; nlinarith [h1, h2]
  have hhalf : (1:ℝ) ≤ |Pr| + |Qr| := by
    have : (1:ℝ) ≤ (|Pr| + |Qr|)^2 := by
      nlinarith [sq_abs Pr, sq_abs Qr, abs_nonneg Pr, abs_nonneg Qr, mul_nonneg (abs_nonneg Pr) (abs_nonneg Qr)]
    nlinarith [abs_nonneg Pr, abs_nonneg Qr]
  unfold facePossible
  simp only [Bool.not_eq_true', decide_eq_false_iff_not, not_lt]
  set P : Ex := .add (.mul (nxE A k) (.cs B.s B.m)) (.mul (nyE A k) (.sn B.s B.m))
  set Q : Ex := .add (.neg (.mul (nxE A k) (.sn B.s B.m))) (.mul (nyE A k) (.cs B.s B.m))
  have ePr : P.real θ = Pr := by
    show (nxE A k).real θ * (Ex.cs B.s B.m).real θ + (nyE A k).real θ * (Ex.sn B.s B.m).real θ = Pr
    rw [nxE_real, nyE_real, cs_real, sn_real]
  have eQr : Q.real θ = Qr := by
    show -((nxE A k).real θ * (Ex.sn B.s B.m).real θ) + (nyE A k).real θ * (Ex.cs B.s B.m).real θ = Qr
    rw [nxE_real, nyE_real, cs_real, sn_real]; simp only [Qr]; ring
  set σ1 : ℚ := if 0 ≤ ((P.tf T H).range H).mid then 1 else -1
  set σ2 : ℚ := if 0 ≤ ((Q.tf T H).range H).mid then 1 else -1
  have hσ1 : (σ1 : ℝ) * Pr ≤ |Pr| := by
    simp only [σ1]; split_ifs
    · simp only [Rat.cast_one, one_mul]; exact le_abs_self _
    · simp only [Rat.cast_neg, Rat.cast_one, neg_mul, one_mul]; exact neg_le_abs _
  have hσ2 : (σ2 : ℝ) * Qr ≤ |Qr| := by
    simp only [σ2]; split_ifs
    · simp only [Rat.cast_one, one_mul]; exact le_abs_self _
    · simp only [Rat.cast_neg, Rat.cast_one, neg_mul, one_mul]; exact neg_le_abs _
  have hS := (ex_mem_range hθ (.add (.mul (.c σ1) P) (.mul (.c σ2) Q))).1
  simp only [Ex.real, ePr, eQr] at hS
  have hp := hproj.2
  have hlb : ((max (1/2) ((((Ex.add (.mul (.c σ1) P) (.mul (.c σ2) Q)).tf T H).range H).lo / 2) : ℚ) : ℝ)
      ≤ (|Pr| + |Qr|) / 2 := by
    push_cast
    apply max_le <;> linarith
  have : (1/2 : ℝ) + ((max (1/2) ((((Ex.add (.mul (.c σ1) P) (.mul (.c σ2) Q)).tf T H).range H).lo / 2) : ℚ) : ℝ)
      ≤ ((((((nxE A k).tf T H).range H).mul (dIv A.rx B.rx A.x B.x)).add
        ((((nyE A k).tf T H).range H).mul (dIv A.ry B.ry A.y B.y))).hi : ℝ) := by
    have e : (B.rx + dx B.s) - (A.rx + dx A.s) = (B.rx:ℝ) + dx B.s - (A.rx + dx A.s) := rfl
    linarith
  apply (Rat.cast_le (K := ℝ)).mp
  push_cast at this ⊢
  linarith

end Sq19.Milp
