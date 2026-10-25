import S12.WallCubicData
import Mathlib.Tactic.FieldSimp

namespace S12
set_option maxHeartbeats 0

/-- Rational parametrization of the entire closed first-quadrant unit arc,
including the two axis directions. -/
theorem first_quadrant_rational (c s : ℝ) (hc : 0≤c) (hs : 0≤s) (hn : c^2+s^2=1) :
    ∃ t : ℝ, 0≤t ∧ t≤1 ∧ c=2*t/(1+t^2) ∧ s=(1-t^2)/(1+t^2) := by
  let t := c/(1+s)
  have hden : 0<1+s := by linarith
  have hc1 : c≤1 := by nlinarith [sq_nonneg s,sq_nonneg (c-1)]
  have ht0 : 0≤t := div_nonneg hc hden.le
  have ht1 : t≤1 := (div_le_one hden).mpr (by linarith)
  have hct : t*(1+s)=c := div_mul_cancel₀ c hden.ne'
  have hct2 := congrArg (fun z : ℝ => z^2) hct
  have hfac : (1+s)*(s*(1+t^2)-(1-t^2))=0 := by nlinarith [hct2]
  have hsrel : s*(1+t^2)=1-t^2 := by
    have hh := (mul_eq_zero.mp hfac).resolve_left hden.ne'
    linarith
  have hsrel' : (1+s)*(1+t^2)=2 := by nlinarith only [hsrel]
  have hcrel : c*(1+t^2)=2*t := by
    calc
      _ = t*((1+s)*(1+t^2)) := by rw [← hct]; ring
      _ = 2*t := by rw [hsrel']; ring
  have hden' : 0<1+t^2 := by nlinarith [sq_nonneg t]
  exact ⟨t,ht0,ht1,(eq_div_iff hden'.ne').mpr hcrel,(eq_div_iff hden'.ne').mpr hsrel⟩

/-- A checked cubic bound implies the required inequality for every square
orientation; the parametrization and denominator signs are proved here. -/
theorem normal_bound_from_cubic (w delta : ℝ)
    (hp : ∀ t : ℝ, 0≤t → t≤1 → 0≤wallCubic w delta t)
    (c s : ℝ) (hc : 0≤c) (hs : 0≤s) (hn : c^2+s^2=1) :
    (1-delta)*c^2+s^2+w*c*s≤c+s := by
  obtain ⟨t,ht0,ht1,hct,hst⟩ := first_quadrant_rational c s hc hs hn
  have hden : 0<1+t^2 := by nlinarith [sq_nonneg t]
  have hid : (c+s-1+delta*c^2-w*c*s)*(1+t^2)^2 = 2*t*wallCubic w delta t := by
    rw [hct,hst]
    dsimp [wallCubic]
    field_simp
    <;> ring
  have hp' := mul_nonneg (show 0≤2*t by linarith) (hp t ht0 ht1)
  have hv : 0≤c+s-1+delta*c^2-w*c*s := by
    apply nonneg_of_mul_nonneg_left (b := (1+t^2)^2) _ (sq_pos_of_pos hden)
    rw [hid]
    exact hp'
  nlinarith only [hv,hn]

theorem normal_bound_088 (c s : ℝ) (hc : 0≤c) (hs : 0≤s) (hn : c^2+s^2=1) :
    c^2*(457/500)+s^2+(22/25)*c*s≤c+s := by
  have h := normal_bound_from_cubic (22/25) (43/500) wall088_nonnegative c s hc hs hn
  nlinarith only [h]
theorem normal_bound_0956 (c s : ℝ) (hc : 0≤c) (hs : 0≤s) (hn : c^2+s^2=1) :
    c^2*(19/25)+s^2+(239/250)*c*s≤c+s := by
  have h := normal_bound_from_cubic (239/250) (6/25) wall0956_nonnegative c s hc hs hn
  nlinarith only [h]

theorem normal_bound_small (w b d c s : ℝ) (hw : w≤413/500) (hb : b≤1) (hd : d≤1)
    (hc : 0≤c) (hs : 0≤s) (hn : c^2+s^2=1) :
    c^2*b+s^2*d+w*c*s≤c+s := by
  have ht1 : 1≤c+s := by nlinarith [mul_nonneg hc hs,sq_nonneg (c+s-1)]
  have ht2 : c+s≤99/70 := by nlinarith [sq_nonneg (c-s),sq_nonneg (c+s-99/70)]
  have hwidth := mul_nonneg (mul_nonneg hc hs) (sub_nonneg.mpr hw)
  have hb' := mul_nonneg (sq_nonneg c) (sub_nonneg.mpr hb)
  have hd' := mul_nonneg (sq_nonneg s) (sub_nonneg.mpr hd)
  have hpoly := mul_nonneg (show 0≤1-(413/1000)*(c+s+1) by linarith)
    (show 0≤c+s-1 by linarith)
  nlinarith only [hwidth,hb',hd',hpoly,hn]

#print axioms normal_bound_088
#print axioms normal_bound_0956
end S12
