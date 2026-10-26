import S12.SquareFrame
import S12.ShortCluster

namespace S12
open S12Pilot
set_option maxHeartbeats 0

theorem weighted_positive_three (a b c x y z : ℝ)
    (ha : 0 ≤ a) (hb : 0 ≤ b) (hc : 0 ≤ c) (hs : a+b+c=1)
    (hx : 0<x) (hy : 0<y) (hz : 0<z) : 0<a*x+b*y+c*z := by
  have hax := mul_nonneg ha hx.le
  have hby := mul_nonneg hb hy.le
  have hcz := mul_nonneg hc hz.le
  by_cases ha' : 0<a
  · have := mul_pos ha' hx; linarith
  by_cases hb' : 0<b
  · have := mul_pos hb' hy; linarith
  have hc' : 0<c := by linarith
  have := mul_pos hc' hz
  linarith

/-- A box wider than one in both orthogonal coordinates cannot avoid a
short-diameter triangle whose barycenter is the origin. -/
theorem centered_triangle_cover (a u0 v0 u1 v1 u2 v2 w0 w1 w2 : ℝ)
    (ha : 1<a) (hw0 : 0≤w0) (hw1 : 0≤w1) (hw2 : 0≤w2)
    (hws : w0+w1+w2=1)
    (hu : w0*u0+w1*u1+w2*u2=0) (hv : w0*v0+w1*v1+w2*v2=0)
    (d01u0 : -1≤u0-u1) (d01u1 : u0-u1≤1)
    (d01v0 : -1≤v0-v1) (d01v1 : v0-v1≤1)
    (d02u0 : -1≤u0-u2) (d02u1 : u0-u2≤1)
    (d02v0 : -1≤v0-v2) (d02v1 : v0-v2≤1)
    (d12u0 : -1≤u1-u2) (d12u1 : u1-u2≤1)
    (d12v0 : -1≤v1-v2) (d12v1 : v1-v2≤1) :
    InBands (-a/2) (-a/2) a u0 v0 ∨ InBands (-a/2) (-a/2) a u1 v1 ∨
      InBands (-a/2) (-a/2) a u2 v2 := by
  have hsep : ∀ c s : ℝ, 0<c*u0+s*v0 → 0<c*u1+s*v1 → 0<c*u2+s*v2 → False := by
    intro c s h0 h1 h2
    have hp := weighted_positive_three w0 w1 w2 _ _ _ hw0 hw1 hw2 hws h0 h1 h2
    have he : w0*(c*u0+s*v0)+w1*(c*u1+s*v1)+w2*(c*u2+s*v2)=0 := by
      calc
        _ = c*(w0*u0+w1*u1+w2*u2)+s*(w0*v0+w1*v1+w2*v2) := by ring
        _ = 0 := by rw [hu,hv]; ring
    linarith
  by_contra he
  simp only [InBands,not_or,not_and_or,not_lt] at he
  rcases he with ⟨he0,he1,he2⟩
  rcases he0 with e0 | e0 | e0 | e0 <;>
    rcases he1 with e1 | e1 | e1 | e1 <;>
    rcases he2 with e2 | e2 | e2 | e2
  all_goals first
    | linarith
    | exact hsep 1 0 (by linarith) (by linarith) (by linarith)
    | exact hsep (-1) 0 (by linarith) (by linarith) (by linarith)
    | exact hsep 0 1 (by linarith) (by linarith) (by linarith)
    | exact hsep 0 (-1) (by linarith) (by linarith) (by linarith)
    | exact hsep 1 1 (by linarith) (by linarith) (by linarith)
    | exact hsep 1 (-1) (by linarith) (by linarith) (by linarith)
    | exact hsep (-1) 1 (by linarith) (by linarith) (by linarith)
    | exact hsep (-1) (-1) (by linarith) (by linarith) (by linarith)

theorem relative_short_bounds (q : OpenSquare) (x y x' y' : ℝ)
    (hd : (x-x')^2+(y-y')^2 ≤ 1) :
    -1≤relativeU q x y-relativeU q x' y' ∧ relativeU q x y-relativeU q x' y'≤1 ∧
    -1≤relativeV q x y-relativeV q x' y' ∧ relativeV q x y-relativeV q x' y'≤1 := by
  obtain ⟨h0,h1,h2,h3⟩ := short_projections q _ _ hd
  dsimp [relativeU,relativeV]
  refine ⟨?_,?_,?_,?_⟩ <;> linarith

/-- The triangle non-avoidance lemma, proved for arbitrary real vertices,
weights, square positions, and orientations, including boundary centers. -/
theorem triangle_nonavoidance (q : OpenSquare) (ha : 1<q.side)
    (x0 y0 x1 y1 x2 y2 w0 w1 w2 : ℝ)
    (hw0 : 0≤w0) (hw1 : 0≤w1) (hw2 : 0≤w2) (hws : w0+w1+w2=1)
    (hx : w0*x0+w1*x1+w2*x2=centerX q)
    (hy : w0*y0+w1*y1+w2*y2=centerY q)
    (hd01 : (x0-x1)^2+(y0-y1)^2≤1)
    (hd02 : (x0-x2)^2+(y0-y2)^2≤1)
    (hd12 : (x1-x2)^2+(y1-y2)^2≤1) :
    q.Inside x0 y0 ∨ q.Inside x1 y1 ∨ q.Inside x2 y2 := by
  obtain ⟨cc0,cc1⟩ := center_coordinates q
  have hu : w0*relativeU q x0 y0+w1*relativeU q x1 y1+w2*relativeU q x2 y2=0 := by
    calc
      _ = q.c*(w0*x0+w1*x1+w2*x2)+q.s*(w0*y0+w1*y1+w2*y2)-
        (q.loU+q.side/2)*(w0+w1+w2) := by dsimp [relativeU]; ring
      _ = 0 := by rw [hx,hy,hws,cc0]; ring
  have hv : w0*relativeV q x0 y0+w1*relativeV q x1 y1+w2*relativeV q x2 y2=0 := by
    calc
      _ = -q.s*(w0*x0+w1*x1+w2*x2)+q.c*(w0*y0+w1*y1+w2*y2)-
        (q.loV+q.side/2)*(w0+w1+w2) := by dsimp [relativeV]; ring
      _ = 0 := by rw [hx,hy,hws,cc1]; ring
  obtain ⟨d0,d1,d2,d3⟩ := relative_short_bounds q x0 y0 x1 y1 hd01
  obtain ⟨d4,d5,d6,d7⟩ := relative_short_bounds q x0 y0 x2 y2 hd02
  obtain ⟨d8,d9,d10,d11⟩ := relative_short_bounds q x1 y1 x2 y2 hd12
  have h := centered_triangle_cover q.side
    (relativeU q x0 y0) (relativeV q x0 y0) (relativeU q x1 y1) (relativeV q x1 y1)
    (relativeU q x2 y2) (relativeV q x2 y2) w0 w1 w2 ha hw0 hw1 hw2 hws hu hv
    d0 d1 d2 d3 d4 d5 d6 d7 d8 d9 d10 d11
  simpa only [relative_inside_iff] using h

#print axioms triangle_nonavoidance
end S12
