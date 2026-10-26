import S12.SquareFrame

namespace S12
open S12Pilot
set_option maxHeartbeats 0

/-- Re-index the four faces, without moving or reflecting the square. -/
noncomputable def turnFrame (q : OpenSquare) : OpenSquare where
  c := -q.s
  s := q.c
  loU := q.loV
  loV := -q.loU-q.side
  side := q.side
  unit_normal := by nlinarith [q.unit_normal]
  side_pos := q.side_pos

@[simp] theorem turnFrame_inside (q : OpenSquare) (x y : ℝ) :
    (turnFrame q).Inside x y ↔ q.Inside x y := by
  dsimp [turnFrame,OpenSquare.Inside,InBands]
  constructor <;> rintro ⟨h0,h1,h2,h3⟩ <;> refine ⟨?_,?_,?_,?_⟩ <;> linarith
@[simp] theorem turnFrame_side (q : OpenSquare) : (turnFrame q).side=q.side := rfl
@[simp] theorem turnFrame_centerX (q : OpenSquare) : centerX (turnFrame q)=centerX q := by
  dsimp [turnFrame,centerX,centerY]; ring
@[simp] theorem turnFrame_centerY (q : OpenSquare) : centerY (turnFrame q)=centerY q := by
  dsimp [turnFrame,centerX,centerY]; ring

/-- Every square admits nonnegative normal components, by re-indexing its
faces. No symmetry of an ownership branch is assumed here. -/
theorem exists_positive_frame (q : OpenSquare) :
    ∃ r : OpenSquare, 0≤r.c ∧ 0≤r.s ∧ r.side=q.side ∧
      centerX r=centerX q ∧ centerY r=centerY q ∧
      ∀ x y, r.Inside x y ↔ q.Inside x y := by
  by_cases hc : 0≤q.c
  · by_cases hs : 0≤q.s
    · exact ⟨q,hc,hs,rfl,rfl,rfl,by intros; rfl⟩
    · refine ⟨turnFrame q,?_,?_,by simp,by simp,by simp,by simp⟩
      · dsimp [turnFrame]; linarith
      · exact hc
  · by_cases hs : 0≤q.s
    · refine ⟨turnFrame (turnFrame (turnFrame q)),?_,?_,by simp,by simp,by simp,by simp⟩
      · dsimp [turnFrame]; linarith
      · dsimp [turnFrame]; linarith
    · refine ⟨turnFrame (turnFrame q),?_,?_,by simp,by simp,by simp,by simp⟩ <;>
        dsimp [turnFrame] <;> linarith

/-- Elementary closure of an affine inequality on a one-sided interval. -/
theorem affine_endpoint_nonnegative (a d v : ℝ) (ha : 0<a)
    (h : ∀ t, 0<t → t<a → 0≤v+d*t) : 0≤v := by
  by_contra hv
  have hv' : v<0 := lt_of_not_ge hv
  let t := min (a/2) ((-v)/(2*(|d|+1)))
  have hd : 0<2*(|d|+1) := by nlinarith [abs_nonneg d]
  have ht0 : 0<t := lt_min (by linarith) (div_pos (by linarith) hd)
  have ht1 : t<a := lt_of_le_of_lt (min_le_left _ _) (by linarith)
  have htm : t*(2*(|d|+1))≤-v :=
    (le_div_iff₀ hd).mp (min_le_right _ _)
  have hdt : d*t ≤ |d| * t := mul_le_mul_of_nonneg_right (le_abs_self d) ht0.le
  have hh := h t ht0 ht1
  nlinarith

/-- Wall containment of an open square implies the inequalities for its
extreme vertices. Boundary limits are proved, not numerically assumed. -/
theorem positive_frame_wall_bounds (q : OpenSquare) (hc : 0≤q.c) (hs : 0≤q.s)
    (hwall : ∀ x y, q.Inside x y → 0≤x ∧ 0≤y) :
    q.side*(q.c+q.s)/2 ≤ centerX q ∧ q.side*(q.c+q.s)/2 ≤ centerY q := by
  have hx : 0≤q.c*q.loU-q.s*(q.loV+q.side) := by
    apply affine_endpoint_nonnegative q.side (q.c+q.s) _ q.side_pos
    intro t ht0 ht1
    let u := q.loU+t
    let v := q.loV+q.side-t
    have hi : q.Inside (q.c*u-q.s*v) (q.s*u+q.c*v) := by
      apply (inside_iff_rotated_box q _ _).mpr
      refine ⟨u,v,?_,rfl,rfl⟩
      dsimp [u,v,InBands]; refine ⟨?_,?_,?_,?_⟩ <;> linarith
    have hh := (hwall _ _ hi).1
    dsimp [u,v] at hh
    nlinarith
  have hy : 0≤q.s*q.loU+q.c*q.loV := by
    apply affine_endpoint_nonnegative q.side (q.c+q.s) _ q.side_pos
    intro t ht0 ht1
    let u := q.loU+t
    let v := q.loV+t
    have hi : q.Inside (q.c*u-q.s*v) (q.s*u+q.c*v) := by
      apply (inside_iff_rotated_box q _ _).mpr
      refine ⟨u,v,?_,rfl,rfl⟩
      dsimp [u,v,InBands]; refine ⟨?_,?_,?_,?_⟩ <;> linarith
    have hh := (hwall _ _ hi).2
    dsimp [u,v] at hh
    nlinarith
  dsimp [centerX,centerY]
  constructor <;> nlinarith

#print axioms exists_positive_frame
#print axioms positive_frame_wall_bounds
end S12
