import Sq19Lean.Endgame.Combine
import Sq19Lean.Endgame.ExactRowsOnH
import Sq19Lean.Wedge.GeometryBridge

/-!
# Algebraic identification of the axis-zero row quotient

Separate row scalings cancel from the three-row Farkas quotient. The canonical
axis-zero P/Q/floor rows give exactly `Wedge.PhiCase`, with no assumptions about
existence of a centre satisfying the rows. This identity is the interface needed
when reducing a symbolic certificate to the wedge theorem.
-/
namespace Sq19.Endgame
open Real Sq19.Milp

structure RealRow where
  ax : ℝ
  ay : ℝ
  b0 : ℝ
  b1 : ℝ

@[ext] theorem RealRow.ext {r s : RealRow}
    (hx : r.ax = s.ax) (hy : r.ay = s.ay) (hb : r.b0 = s.b0) (hc : r.b1 = s.b1) : r = s := by
  cases r; cases s; simp_all

noncomputable def RowE.at (r : RowE) (θ : ℕ → ℝ) : RealRow :=
  ⟨r.ax.real θ, r.ay.real θ, r.b0.real θ, r.b1.real θ⟩
noncomputable def RealRow.scale (t : ℝ) (r : RealRow) : RealRow :=
  ⟨t*r.ax,t*r.ay,t*r.b0,t*r.b1⟩
noncomputable def rowS0 (p q f : RealRow) : ℝ :=
  -cross q.ax q.ay f.ax f.ay * p.b0 - cross f.ax f.ay p.ax p.ay * q.b0 -
    cross p.ax p.ay q.ax q.ay * f.b0
noncomputable def rowS1 (p q f : RealRow) : ℝ :=
  -cross q.ax q.ay f.ax f.ay * p.b1 - cross f.ax f.ay p.ax p.ay * q.b1 -
    cross p.ax p.ay q.ax q.ay * f.b1
noncomputable def rowQuotient (p q f : RealRow) : ℝ := -rowS0 p q f / rowS1 p q f

theorem rowS0_scale (p q f : RealRow) (u v w : ℝ) :
    rowS0 (p.scale u) (q.scale v) (f.scale w) = u*v*w*rowS0 p q f := by
  unfold rowS0 RealRow.scale cross; ring

theorem rowS1_scale (p q f : RealRow) (u v w : ℝ) :
    rowS1 (p.scale u) (q.scale v) (f.scale w) = u*v*w*rowS1 p q f := by
  unfold rowS1 RealRow.scale cross; ring

theorem rowQuotient_scale (p q f : RealRow) {u v w : ℝ}
    (hu : u ≠ 0) (hv : v ≠ 0) (hw : w ≠ 0) :
    rowQuotient (p.scale u) (q.scale v) (f.scale w) = rowQuotient p q f := by
  unfold rowQuotient
  rw [rowS0_scale, rowS1_scale, neg_mul_eq_mul_neg]
  exact mul_div_mul_left _ _ (mul_ne_zero (mul_ne_zero hu hv) hw)

theorem rowQuotient_at (p q f : RowE) (θ : ℕ → ℝ) :
    rowQuotient (p.at θ) (q.at θ) (f.at θ) = -(S0E p q f).real θ / (S1E p q f).real θ := by
  unfold rowQuotient rowS0 rowS1 RowE.at S0E S1E lam1 lam2 lam3 crossE cross
  simp only [Sq19.Milp.Ex.real]
  congr 1 <;> ring

noncomputable def zeroP (pa : Bool) (a13 a14 o1 : ℝ) : RealRow :=
  let f := Wedge.f1C pa a13 a14
  ⟨-sin f, cos f, -cos f - 2*sin f - Wedge.A1C pa a13 a14 o1, cos f⟩
noncomputable def zeroQ (qa : Bool) (a13 a11 o2 : ℝ) : RealRow :=
  let f := Wedge.f2C qa a13 a11
  ⟨cos f, sin f, -cos f - sin f - Wedge.A2C qa a13 a11 o2, cos f + sin f⟩
noncomputable def zeroF (a13 : ℝ) : RealRow :=
  ⟨0,-1,-(2+(|cos (π/4+a13)|+|sin (π/4+a13)|)/2),0⟩

theorem zeroRow_denominator (pa qa : Bool) (a11 a13 a14 o1 o2 : ℝ) :
    rowS1 (zeroP pa a13 a14 o1) (zeroQ qa a13 a11 o2) (zeroF a13) =
      Wedge.coefC pa qa a11 a13 a14 := by
  unfold rowS1 zeroP zeroQ zeroF cross Wedge.coefC; ring

theorem zeroRow_numerator (pa qa : Bool) (a11 a13 a14 o1 o2 : ℝ) :
    -rowS0 (zeroP pa a13 a14 o1) (zeroQ qa a13 a11 o2) (zeroF a13) =
      Wedge.coefC pa qa a11 a13 a14 + Wedge.restC pa qa a11 a13 a14 o1 o2 := by
  unfold rowS0 zeroP zeroQ zeroF cross Wedge.coefC Wedge.restC
  rw [cos_sub]; ring

/-- Canonical geometric quotient equals the expression checked by the wedge proof. -/
theorem zeroRow_quotient (pa qa : Bool) (a11 a13 a14 o1 o2 : ℝ)
    (hc : Wedge.coefC pa qa a11 a13 a14 ≠ 0) :
    rowQuotient (zeroP pa a13 a14 o1) (zeroQ qa a13 a11 o2) (zeroF a13) =
      Wedge.PhiCase pa qa a11 a13 a14 o1 o2 := by
  unfold rowQuotient
  rw [zeroRow_numerator, zeroRow_denominator]
  unfold Wedge.PhiCase
  rw [add_div, div_self hc]

private theorem cos_threequarter (a : ℝ) : cos (3*π/4+a) = -sin (π/4+a) := by
  rw [show 3*π/4+a = (π/4+a)+π/2 by ring, cos_add_pi_div_two]
private theorem sin_threequarter (a : ℝ) : sin (3*π/4+a) = cos (π/4+a) := by
  rw [show 3*π/4+a = (π/4+a)+π/2 by ring, sin_add_pi_div_two]

/-- The selected signed supports of P at zero axis angles. -/
private theorem zero_support_P {θ : ℕ → ℝ} (h0 : θ 0=0) (h1 : θ 1=0) (h2 : θ 2=0)
    (b1 b2 : Bool) (k : ℕ) :
    (suppE 1 (-sg b1) 0 0 1 0).real θ = 1/2 ∧
    (suppE (sg b2) 1 0 2 2 0).real θ = 1/2 ∧
    (suppE (-1) 1 k 3 2 0).real θ = (cos (π/4+θ k)+sin (π/4+θ k))/2 := by
  simp only [suppE, Ex.real, cosD_real, sinD_real, angE, h0,h1,h2]
  norm_num [cos_threequarter, sin_threequarter, show (2:ℝ)*π/4=π/2 by ring]
  ring

/-- P owned by the neighbouring tilted square: no row scaling remains at zero. -/
theorem ProwB_at_zero {θ : ℕ → ℝ} (h0 : θ 0=0) (h1 : θ 1=0) (h2 : θ 2=0)
    (j o : ℕ) (hj : θ j=0) (Y : ℚ) (b1 b2 : Bool) (o1 : ℝ) :
    (ProwB j o Y (σPb b1 b2)).at θ = zeroP false (θ 13) (θ 14) o1 := by
  obtain ⟨e1,e2,e3⟩ := zero_support_P h0 h1 h2 b1 b2 14
  have e4 := suppAbsE_real θ 14 3 13 1
  have ea : angE θ 14 3 = angE θ 14 1+π/2 := by simp [angE]; ring
  rw [ea, supp_quarter] at e4
  apply RealRow.ext <;>
    simp only [RowE.at, ProwB, σPb, Ex.real, e1,e2,e3,e4, zeroP,
      Wedge.f1C, Wedge.A1C, Bool.cond_false, angE, hj, supp, Wedge.gk] <;>
    norm_num [cos_threequarter,sin_threequarter] <;> ring

/-- Signed Q supports at zero axis angles. -/
private theorem zero_support_Q {θ : ℕ → ℝ} (h0 : θ 0=0) (h10 : θ 10=0)
    (b10 : Bool) (k : ℕ) :
    (suppE 1 (-sg b10) 0 0 10 0).real θ = 1/2 ∧
    (suppE (sg b10) 1 0 2 10 0).real θ = 1/2 ∧
    (suppE 1 1 k 1 10 0).real θ = (cos (π/4+θ k)+sin (π/4+θ k))/2 := by
  simp only [suppE, Ex.real, cosD_real, sinD_real, angE, h0,h10]
  norm_num [show (2:ℝ)*π/4=π/2 by ring]
  ring

/-- Q owned by the neighbouring tilted square: the canonical row exactly. -/
theorem QrowB_at_zero {θ : ℕ → ℝ} (h0 : θ 0=0) (h10 : θ 10=0)
    (b10 : Bool) (o2 : ℝ) :
    (QrowB (σQb b10)).at θ = zeroQ false (θ 13) (θ 11) o2 := by
  obtain ⟨e1,e2,e3⟩ := zero_support_Q h0 h10 b10 11
  have e4 := suppAbsE_real θ 11 1 13 1
  apply RealRow.ext <;>
    simp only [RowE.at, QrowB, σQb, Ex.real, e1,e2,e3,e4, zeroQ,
      Wedge.f2C, Wedge.A2C, Bool.cond_false, angE, supp, Wedge.gk] <;>
    norm_num <;> ring

/-- P owned by square 13 is the canonical row scaled by the positive relative cosine. -/
theorem ProwA_at_zero {θ : ℕ → ℝ} (h0 : θ 0=0) (h1 : θ 1=0) (h2 : θ 2=0)
    (j : ℕ) (hj : θ j=0) (Y O : ℚ) (b1 b2 : Bool)
    (hd : cos ((π/4+θ 14)-(π/4+θ 13)) ≠ 0) :
    (ProwA j Y O (σPa b1 b2)).at θ =
      (zeroP true (θ 13) (θ 14) O).scale (cos ((π/4+θ 14)-(π/4+θ 13))) := by
  have hd' : cos (θ 14-θ 13) ≠ 0 := by
    rwa [show (π/4+θ 14)-(π/4+θ 13) = θ 14-θ 13 by ring] at hd
  obtain ⟨e1,e2,e3⟩ := zero_support_P h0 h1 h2 b1 b2 13
  have e4 := suppAbsE_real θ 13 3 14 1
  have ea : angE θ 13 3 = angE θ 13 1+π/2 := by simp [angE]; ring
  rw [ea, supp_quarter, supp_symm] at e4
  apply RealRow.ext <;>
    simp only [RowE.at, ProwA, σPa, Ex.real, e1,e2,e3,e4, cosD_real,sinD_real,
      RealRow.scale, zeroP, Wedge.f1C, Wedge.A1C, Bool.cond_true,
      angE, hj, supp, Wedge.gk, Wedge.ownerA, tan_eq_sin_div_cos] <;>
    norm_num [cos_threequarter,sin_threequarter] <;>
    field_simp [hd'] <;> ring

/-- Q owned by square 13 has the corresponding relative-cosine scaling. -/
theorem QrowA_at_zero {θ : ℕ → ℝ} (h0 : θ 0=0) (h10 : θ 10=0)
    (O : ℚ) (b10 : Bool) (hd : cos ((π/4+θ 11)-(π/4+θ 13)) ≠ 0) :
    (QrowA O (σQa b10)).at θ =
      (zeroQ true (θ 13) (θ 11) O).scale (cos ((π/4+θ 11)-(π/4+θ 13))) := by
  have hd' : cos (θ 11-θ 13) ≠ 0 := by
    rwa [show (π/4+θ 11)-(π/4+θ 13) = θ 11-θ 13 by ring] at hd
  obtain ⟨e1,e2,e3⟩ := zero_support_Q h0 h10 b10 13
  have e4 := suppAbsE_real θ 13 1 11 1
  rw [supp_symm] at e4
  apply RealRow.ext <;>
    simp only [RowE.at, QrowA, σQa, Ex.real, e1,e2,e3,e4, cosD_real,sinD_real,
      RealRow.scale, zeroQ, Wedge.f2C, Wedge.A2C, Bool.cond_true,
      angE, supp, Wedge.gk, Wedge.ownerA, tan_eq_sin_div_cos] <;>
    norm_num <;> field_simp [hd'] <;> ring


private theorem zero_support_F {θ : ℕ → ℝ} (h0 : θ 0=0) (h5 : θ 5=0) (h8 : θ 8=0)
    (b5 bd : Bool) :
    (suppE (sg b5) 1 0 2 5 0).real θ = 1/2 ∧
    (anchor58E bd).real θ = 1/2 ∧
    (suppE 1 1 8 2 13 1).real θ = (cos (π/4+θ 13)+sin (π/4+θ 13))/2 := by
  simp only [suppE, anchor58E, Ex.real, cosD_real, sinD_real, angE, h0,h5,h8]
  norm_num [show (2:ℝ)*π/4=π/2 by ring, cos_pi_div_two_sub, sin_pi_div_two_sub]
  ring

/-- Every positive-8 exact floor row has the canonical axis-zero value. -/
theorem F1rowPos8_at_zero {θ : ℕ → ℝ} (h0 : θ 0=0) (h5 : θ 5=0) (h8 : θ 8=0)
    (X : ℚ) (b5 bd : Bool)
    (hc : 0 ≤ cos (π/4+θ 13)) (hs : 0 ≤ sin (π/4+θ 13)) :
    (F1rowPos8 X (sg b5,1) (1,1) (anchor58E bd)).at θ = zeroF (θ 13) := by
  obtain ⟨e1,e2,e3⟩ := zero_support_F h0 h5 h8 b5 bd
  apply RealRow.ext <;>
    simp only [RowE.at,F1rowPos8, Ex.real,e1,e2,e3,zeroF,angE,h8,
      abs_of_nonneg hc,abs_of_nonneg hs] <;>
    norm_num [show (2:ℝ)*π/4=π/2 by ring] <;> ring

/-- The owner-5 exact floor row has the same zero-axis value. -/
theorem F1rowPos5_at_zero {θ : ℕ → ℝ} (h0 : θ 0=0) (h5 : θ 5=0) (h8 : θ 8=0)
    (X Cx Cy : ℚ) (b5 bd : Bool)
    (hc : 0 ≤ cos (π/4+θ 13)) (hs : 0 ≤ sin (π/4+θ 13)) :
    (F1rowPos5 X Cx Cy (sg b5,1) (1,1) (anchor58E bd)).at θ = zeroF (θ 13) := by
  obtain ⟨e1,e2,e3⟩ := zero_support_F h0 h5 h8 b5 bd
  apply RealRow.ext <;>
    simp only [RowE.at,F1rowPos5, Ex.real,e1,e2,e3,cosD_real,sinD_real,zeroF,angE,h5,h8,
      abs_of_nonneg hc,abs_of_nonneg hs] <;>
    norm_num [show (2:ℝ)*π/4=π/2 by ring] <;> ring

/-- The negative-8 floor row, for either 5–8 owner, has the same canonical value. -/
theorem F1rowNeg_at_zero {θ : ℕ → ℝ} (h0 : θ 0=0) (h5 : θ 5=0) (h8 : θ 8=0)
    (j o : ℕ) (hj : θ j=0) (X Xh : ℚ) (b5 bd : Bool)
    (hc : 0 ≤ cos (π/4+θ 13)) (hs : 0 ≤ sin (π/4+θ 13)) :
    (F1rowNeg j o X Xh (sg b5,1) (1,1) (anchor58E bd)).at θ = zeroF (θ 13) := by
  obtain ⟨e1,e2,e3⟩ := zero_support_F h0 h5 h8 b5 bd
  apply RealRow.ext <;>
    simp only [RowE.at,F1rowNeg, Ex.real,e1,e2,e3,zeroF,angE,hj,h8,
      abs_of_nonneg hc,abs_of_nonneg hs] <;> norm_num <;> ring


/-- Any symbolic rows identified with scaled canonical rows inherit the wedge
bound at the zero-axis evaluation, without a packing at that evaluation. -/
theorem zero_rows_quotient_ge {P Q F : RowE} {θ : ℕ → ℝ}
    (pa qa : Bool) {a11 a13 a14 o1 o2 u v w : ℝ}
    (h11 : |a11| ≤ 82/10000) (h13 : |a13| ≤ 82/10000) (h14 : |a14| ≤ 82/10000)
    (ho1l : 1589/10000 ≤ o1) (ho1h : o1 ≤ 2893/10000)
    (ho2l : -1322/10000 ≤ o2) (ho2h : o2 ≤ 365/10000)
    (hp : P.at θ = (zeroP pa a13 a14 o1).scale u)
    (hq : Q.at θ = (zeroQ qa a13 a11 o2).scale v)
    (hf : F.at θ = (zeroF a13).scale w)
    (hu : u ≠ 0) (hv : v ≠ 0) (hw : w ≠ 0) :
    side19 ≤ -(S0E P Q F).real θ / (S1E P Q F).real θ := by
  rw [← rowQuotient_at, hp,hq,hf,rowQuotient_scale _ _ _ hu hv hw,
    zeroRow_quotient pa qa a11 a13 a14 o1 o2
      (Wedge.zeroAxis_multiplier_pos pa qa h11 h13 h14).2.2.2.ne']
  exact Wedge.wedge_hull pa qa h11 h13 h14 ho1l ho1h ho2l ho2h

/-- Division-free form of the algebraic base case, ready for endpoint-margin
monotonicity. Positivity of the denominator is certified by the geometry checks. -/
theorem zero_rows_margin_nonneg {P Q F : RowE} {θ : ℕ → ℝ}
    (pa qa : Bool) {a11 a13 a14 o1 o2 u v w : ℝ}
    (h11 : |a11| ≤ 82/10000) (h13 : |a13| ≤ 82/10000) (h14 : |a14| ≤ 82/10000)
    (ho1l : 1589/10000 ≤ o1) (ho1h : o1 ≤ 2893/10000)
    (ho2l : -1322/10000 ≤ o2) (ho2h : o2 ≤ 365/10000)
    (hp : P.at θ = (zeroP pa a13 a14 o1).scale u)
    (hq : Q.at θ = (zeroQ qa a13 a11 o2).scale v)
    (hf : F.at θ = (zeroF a13).scale w)
    (hu : u ≠ 0) (hv : v ≠ 0) (hw : w ≠ 0)
    (hS : 0 < (S1E P Q F).real θ) :
    0 ≤ -(S0E P Q F).real θ - side19*(S1E P Q F).real θ := by
  have h := zero_rows_quotient_ge pa qa h11 h13 h14 ho1l ho1h ho2l ho2h hp hq hf hu hv hw
  have := (le_div_iff₀ hS).mp h
  linarith

end Sq19.Endgame
#print axioms Sq19.Endgame.rowQuotient_scale
#print axioms Sq19.Endgame.zeroRow_quotient

#print axioms Sq19.Endgame.ProwA_at_zero
#print axioms Sq19.Endgame.ProwB_at_zero
#print axioms Sq19.Endgame.QrowA_at_zero
#print axioms Sq19.Endgame.QrowB_at_zero
#print axioms Sq19.Endgame.F1rowPos8_at_zero
#print axioms Sq19.Endgame.F1rowPos5_at_zero
#print axioms Sq19.Endgame.F1rowNeg_at_zero
#print axioms Sq19.Endgame.zero_rows_margin_nonneg
