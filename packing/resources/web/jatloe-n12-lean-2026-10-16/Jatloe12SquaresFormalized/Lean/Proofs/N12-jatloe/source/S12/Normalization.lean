import S12.To117

namespace S12
open S12Pilot

/-- The original problem: unit open squares with disjoint interiors in [0,L]^2.
Boundary contacts are allowed. -/
structure UnitPacking (L : ℝ) where
  square : Fin 12 → OpenSquare
  congruent : ∀ i,(square i).side=1
  contained : ∀ i x y,(square i).Inside x y → 0≤x ∧ x≤L ∧ 0≤y ∧ y≤L
  disjoint : ∀ i j,i≠j → ∀ x y,¬((square i).Inside x y ∧ (square j).Inside x y)

def scaleSquare (q : OpenSquare) (a : ℝ) (ha : 0<a) : OpenSquare where
  c := q.c
  s := q.s
  loU := a*q.loU
  loV := a*q.loV
  side := a*q.side
  unit_normal := q.unit_normal
  side_pos := mul_pos ha q.side_pos

theorem inside_scale (q : OpenSquare) (a : ℝ) (ha : 0<a) (x y : ℝ) :
    (scaleSquare q a ha).Inside (a*x) (a*y) ↔ q.Inside x y := by
  unfold OpenSquare.Inside scaleSquare InBands
  have hu : q.c*(a*x)+q.s*(a*y)=a*(q.c*x+q.s*y) := by ring
  have hv : -q.s*(a*x)+q.c*(a*y)=a*(-q.s*x+q.c*y) := by ring
  rw [hu,hv,←mul_add,←mul_add]
  simp only [mul_lt_mul_iff_right₀ ha]

theorem inside_scale_div (q : OpenSquare) (a : ℝ) (ha : 0<a) (x y : ℝ) :
    (scaleSquare q a ha).Inside x y ↔ q.Inside (x/a) (y/a) := by
  have hh := inside_scale q a ha (x/a) (y/a)
  simpa only [mul_div_cancel₀ _ (ne_of_gt ha)] using hh

noncomputable def scaleFactor (L : ℝ) : ℝ := min (4/L) (1001/1000)

theorem scaleFactor_bounds (L : ℝ) (hL : 0<L) (h4 : L<4) :
    1<scaleFactor L ∧ scaleFactor L≤1001/1000 ∧ scaleFactor L*L≤4 := by
  have hdiv : (1:ℝ)<4/L := (lt_div_iff₀ hL).mpr (by simpa using h4)
  refine ⟨lt_min hdiv (by norm_num),min_le_right _ _,?_⟩
  exact (le_div_iff₀ hL).mp (min_le_left _ _)

noncomputable def UnitPacking.normalize {L : ℝ} (p : UnitPacking L) (hL : 0<L)
    (h4 : L<4) : NormalizedPacking := by
  let a := scaleFactor L
  have hb := scaleFactor_bounds L hL h4
  have ha : 0<a := lt_trans (by norm_num) hb.1
  exact {
    square := fun i => scaleSquare (p.square i) a ha
    commonSide := a
    side_gt_one := hb.1
    side_le := hb.2.1
    congruent := by intro i; change a*(p.square i).side=a; rw [p.congruent,mul_one]
    contained := by
      intro i x y hi
      have ho := (inside_scale_div _ a ha x y).mp hi
      obtain ⟨hx0,hxL,hy0,hyL⟩ := p.contained i _ _ ho
      have hx := (div_le_iff₀ ha).mp hxL
      have hy := (div_le_iff₀ ha).mp hyL
      have hxpos : 0≤x := by have := mul_nonneg hx0 (le_of_lt ha); simpa [ne_of_gt ha] using this
      have hypos : 0≤y := by have := mul_nonneg hy0 (le_of_lt ha); simpa [ne_of_gt ha] using this
      refine ⟨hxpos,?_,hypos,?_⟩ <;> nlinarith [hb.2.2]
    disjoint := by
      intro i j hij x y hi
      exact p.disjoint i j hij (x/a) (y/a)
        ⟨(inside_scale_div _ a ha x y).mp hi.1,(inside_scale_div _ a ha x y).mp hi.2⟩ }

/-- The initial reduction applied directly to a hypothetical packing below 4. -/
theorem unit_packing_reduction_to_117 {L : ℝ} (p : UnitPacking L) (hL : 0<L) (h4 : L<4) :
    ∃ t∈allTransforms, ∃ r∈retainedRows,
      codedMarkerFamily (t.pullPacking (p.normalize hL h4))=r.groups :=
  packing_reduction_to_117 (p.normalize hL h4)

#print axioms unit_packing_reduction_to_117
end S12
