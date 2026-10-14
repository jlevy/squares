import Sq17Lean.EndpointRoot
import Sq17Lean.SquareBase

/-! Exact endpoint geometry in the canonical algebraic root. Indices are the
source labels minus one. Square 6 is the omitted bottom-row slider, fixed here
at its explicitly specified endpoint position. -/
namespace Sq17.EndpointGeometry
open Sq17.PolynomialBox
noncomputable section

def t : ℝ := EndpointRoot.coordinates.1
def beta : ℝ := EndpointRoot.coordinates.2
def c : ℝ := (1-t*t)/(1+t*t)
def s : ℝ := 2*t/(1+t*t)
def d : ℝ := (1-beta*beta)/(1+beta*beta)
def e : ℝ := 2*beta/(1+beta*beta)
def side : ℝ := (6+4*t)/(1+2*t-t*t)
def h : ℝ := (c+s)/2
def X : ℝ := 1/2+(2+c*s+3*s-s*side)/c
def Y : ℝ := 3/2+(2+3*c-c*side)/s
def A : ℝ := d*(X+1/2)-e*(side-1)+1/2
def B : ℝ := (d+e)*(side-1)-1/2
def u10 : ℝ := 3/2+c*s+2*s
def v10 : ℝ := c*(side-1)-s-1/2
def u11 : ℝ := c+2*s+1/2
def v11 : ℝ := 2*c+(c*c-s*s)/2-1
def u13 : ℝ := 2*c+s+1/2
def T : ℝ := c*(c+4-side)
def rotate (u v : ℝ) : ℝ × ℝ := (c*u-s*v,s*u+c*v)

def centres : Fin 17 → ℝ × ℝ := ![
  (1/2,1/2),(3/2,1/2),(1/2,3/2),(1/2,side-1/2),
  (side-1/2,1/2),(side-3/2-T/(3*s),1/2),(side-1/2,3/2),
  (side-1/2,side-1/2),(h,2+h),rotate u10 v10,rotate u11 v11,
  rotate (u11+1) (v10-1),rotate u13 (v11-1-T/3),
  rotate (u13+1) (v10-2),(X,side-1/2),(d*A+e*B,-e*A+d*B),(side-1/2,Y)]

def directions : Fin 17 → ℝ × ℝ := ![
  (1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),(1,0),
  (c,s),(c,s),(c,s),(c,s),(c,s),(c,s),(1,0),(d,-e),(1,0)]

def squares (i : Fin 17) : Set (ℝ × ℝ) :=
  Sq17.sq (centres i).1 (centres i).2 (directions i).1 (directions i).2

theorem root_bounds :
    |t-(EndpointRoot.midpoint.1:ℝ)| ≤ EndpointRoot.radius ∧
    |beta-(EndpointRoot.midpoint.2:ℝ)| ≤ EndpointRoot.radius := EndpointRoot.coordinates_spec.1

theorem t_bounds : (36/100:ℝ) ≤ t ∧ t ≤ 37/100 := by
  have h := abs_le.mp root_bounds.1
  norm_num [EndpointRoot.midpoint,EndpointRoot.radius] at h
  constructor <;> linarith

theorem beta_bounds : (33/100:ℝ) ≤ beta ∧ beta ≤ 34/100 := by
  have h := abs_le.mp root_bounds.2
  norm_num [EndpointRoot.midpoint,EndpointRoot.radius] at h
  constructor <;> linarith

theorem rational_direction_unit (x : ℝ) :
    ((1-x*x)/(1+x*x))^2+(2*x/(1+x*x))^2=1 := by
  have hx : 1+x*x ≠ 0 := by nlinarith [sq_nonneg x]
  field_simp
  <;> ring

theorem cs_unit : c^2+s^2=1 := rational_direction_unit t
theorem de_unit : d^2+e^2=1 := rational_direction_unit beta

theorem directions_unit (i : Fin 17) : (directions i).1^2+(directions i).2^2=1 := by
  fin_cases i <;> simp [directions,cs_unit,de_unit]

theorem squares_unit (i : Fin 17) : Sq17.IsUnitSquare (squares i) :=
  ⟨(centres i).1,(centres i).2,(directions i).1,(directions i).2,directions_unit i,rfl⟩

theorem denominator_positive : 0 < 1+t*t ∧ 0 < 1+beta*beta ∧ 0 < 1+2*t-t*t := by
  have ht := t_bounds
  refine ⟨by nlinarith [sq_nonneg t],by nlinarith [sq_nonneg beta],?_⟩
  nlinarith [mul_nonneg (sub_nonneg.mpr ht.2) (show 0 ≤ t by linarith)]

theorem cs_positive : 0 < c ∧ 0 < s := by
  have ht := t_bounds
  refine ⟨div_pos ?_ denominator_positive.1,div_pos (by linarith) denominator_positive.1⟩
  nlinarith [mul_nonneg (sub_nonneg.mpr ht.2) (show 0 ≤ t by linarith)]

theorem de_positive : 0 < d ∧ 0 < e := by
  have hb := beta_bounds
  refine ⟨div_pos ?_ denominator_positive.2.1,div_pos (by linarith) denominator_positive.2.1⟩
  nlinarith [mul_nonneg (sub_nonneg.mpr hb.2) (show 0 ≤ beta by linarith)]

theorem side_positive : 0 < side :=
  div_pos (by linarith [t_bounds.1]) denominator_positive.2.2

end
end Sq17.EndpointGeometry
#print axioms Sq17.EndpointGeometry.squares_unit
#print axioms Sq17.EndpointGeometry.cs_positive
#print axioms Sq17.EndpointGeometry.side_positive
