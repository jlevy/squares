import S12.Markers

namespace S12
open S12Pilot

theorem inside_distance_bound (q : OpenSquare) (x y x' y' : ℝ)
    (hp : q.Inside x y) (hp' : q.Inside x' y') :
    (x-x')^2 + (y-y')^2 < 2*q.side^2 := by
  rcases hp with ⟨h0,h1,h2,h3⟩
  rcases hp' with ⟨h4,h5,h6,h7⟩
  let du := (q.c*x+q.s*y) - (q.c*x'+q.s*y')
  let dv := (-q.s*x+q.c*y) - (-q.s*x'+q.c*y')
  have hu0 : 0 < q.side-du := by dsimp [du]; linarith
  have hu1 : 0 < q.side+du := by dsimp [du]; linarith
  have hv0 : 0 < q.side-dv := by dsimp [dv]; linarith
  have hv1 : 0 < q.side+dv := by dsimp [dv]; linarith
  have hu := mul_pos hu0 hu1
  have hv := mul_pos hv0 hv1
  have hrot : du^2+dv^2 = (x-x')^2+(y-y')^2 := by
    calc
      _ = (q.c^2+q.s^2)*((x-x')^2+(y-y')^2) := by dsimp [du,dv]; ring
      _ = _ := by rw [q.unit_normal, one_mul]
  nlinarith

theorem normalized_diameter_bound (q : OpenSquare)
    (hsize : q.side ≤ 1001/1000) (x y x' y' : ℝ)
    (hp : q.Inside x y) (hp' : q.Inside x' y') :
    (x-x')^2+(y-y')^2 < (2000000/982081 : ℝ) := by
  have hd := inside_distance_bound q x y x' y' hp hp'
  have ha := q.side_pos
  have hh : q.side^2 ≤ (1001/1000 : ℝ)^2 := by nlinarith
  nlinarith

def Owns (q : OpenSquare) (i : Marker) : Prop :=
  q.Inside (marker i).1 (marker i).2


#print axioms inside_distance_bound
end S12
