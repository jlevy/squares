import SquarePackingArchive.Friedman

namespace SquarePackingArchive.Records.Square5

noncomputable def diagonal : ℝ := Real.sqrt 2 / 2

lemma diagonal_positive : 0 < diagonal := by
  have : 0 < Real.sqrt 2 := Real.sqrt_pos.2 (by norm_num)
  exact div_pos this (by norm_num)

lemma diagonal_sq : diagonal ^ 2 = 1 / 2 := by
  rw [diagonal, div_pow, Real.sq_sqrt (by norm_num)]
  norm_num

noncomputable def axisFrame : Frame where
  cosine := 1
  sine := 0
  unit := by norm_num

noncomputable def diagonalFrame : Frame where
  cosine := diagonal
  sine := diagonal
  unit := by nlinarith [diagonal_sq]

noncomputable def side : ℝ := 2 + diagonal

noncomputable def bottomLeft : PlacedSquare :=
  { center := ⟨1 / 2, 1 / 2⟩, frame := axisFrame }

noncomputable def bottomRight : PlacedSquare :=
  { center := ⟨side - 1 / 2, 1 / 2⟩, frame := axisFrame }

noncomputable def topLeft : PlacedSquare :=
  { center := ⟨1 / 2, side - 1 / 2⟩, frame := axisFrame }

noncomputable def topRight : PlacedSquare :=
  { center := ⟨side - 1 / 2, side - 1 / 2⟩, frame := axisFrame }

noncomputable def center : PlacedSquare :=
  { center := ⟨side / 2, side / 2⟩, frame := diagonalFrame }

noncomputable def squares : Fin 5 → PlacedSquare := ![
  bottomLeft, bottomRight, topLeft, topRight, center
]

@[simp] lemma squares_zero : squares 0 = bottomLeft := by rfl

@[simp] lemma squares_one : squares 1 = bottomRight := by rfl

@[simp] lemma squares_two : squares 2 = topLeft := by rfl

@[simp] lemma squares_three : squares 3 = topRight := by rfl

@[simp] lemma squares_four : squares 4 = center := by rfl

lemma square_fits (index : Fin 5) : (squares index).Fits side := by
  intro point point_mem
  rcases point_mem with ⟨localX, localY, localX_le, localY_le, rfl⟩
  rcases abs_le.mp localX_le with ⟨localX_lower, localX_upper⟩
  rcases abs_le.mp localY_le with ⟨localY_lower, localY_upper⟩
  have diagonal_nonnegative : 0 ≤ diagonal := diagonal_positive.le
  have diagonal_lt_one : diagonal < 1 := by
    nlinarith [diagonal_sq]
  fin_cases index <;>
    simp [bottomLeft, bottomRight, topLeft, topRight, center,
      PlacedSquare.point, Frame.place, axisFrame, diagonalFrame,
      Container.Contains, side] <;>
    exact ⟨by nlinarith [diagonal_sq], by nlinarith [diagonal_sq],
      by nlinarith [diagonal_sq], by nlinarith [diagonal_sq]⟩

lemma square_disjoint
    (left right : Fin 5) (different : left ≠ right) :
    (squares left).InteriorDisjoint (squares right) := by
  have diagonal_nonnegative : 0 ≤ diagonal := diagonal_positive.le
  have bottom_pair :
      (squares 0).InteriorDisjoint (squares 1) := by
    apply PlacedSquare.separatedOn_interiorDisjoint
      (axisX := 1) (axisY := 0)
    · norm_num [PlacedSquare.SeparatedOn, PlacedSquare.projectionRadius,
        bottomLeft, bottomRight, axisFrame, side, dot]
      rw [abs_of_nonneg] <;> nlinarith
    · exact Or.inl one_ne_zero
  have left_pair :
      (squares 0).InteriorDisjoint (squares 2) := by
    apply PlacedSquare.separatedOn_interiorDisjoint
      (axisX := 0) (axisY := 1)
    · norm_num [PlacedSquare.SeparatedOn, PlacedSquare.projectionRadius,
        bottomLeft, topLeft, axisFrame, side, dot]
      rw [abs_of_nonneg] <;> nlinarith
    · exact Or.inr one_ne_zero
  have opposite_pair :
      (squares 0).InteriorDisjoint (squares 3) := by
    apply PlacedSquare.separatedOn_interiorDisjoint
      (axisX := 1) (axisY := 0)
    · norm_num [PlacedSquare.SeparatedOn, PlacedSquare.projectionRadius,
        bottomLeft, topRight, axisFrame, side, dot]
      rw [abs_of_nonneg] <;> nlinarith
    · exact Or.inl one_ne_zero
  have bottom_left_center :
      (squares 0).InteriorDisjoint (squares 4) := by
    apply PlacedSquare.separatedOn_interiorDisjoint
      (axisX := diagonal) (axisY := diagonal)
    · norm_num [PlacedSquare.SeparatedOn, PlacedSquare.projectionRadius,
        bottomLeft, center, axisFrame, diagonalFrame, side, dot,
        abs_of_nonneg diagonal_nonnegative]
      repeat' rw [abs_of_nonneg (by nlinarith [diagonal_sq])]
      nlinarith [diagonal_sq]
    · exact Or.inl diagonal_positive.ne'
  have crossed_pair :
      (squares 1).InteriorDisjoint (squares 2) := by
    apply PlacedSquare.separatedOn_interiorDisjoint
      (axisX := 1) (axisY := 0)
    · norm_num [PlacedSquare.SeparatedOn, PlacedSquare.projectionRadius,
        bottomRight, topLeft, axisFrame, side, dot]
      rw [abs_of_nonpos] <;> nlinarith
    · exact Or.inl one_ne_zero
  have right_pair :
      (squares 1).InteriorDisjoint (squares 3) := by
    apply PlacedSquare.separatedOn_interiorDisjoint
      (axisX := 0) (axisY := 1)
    · norm_num [PlacedSquare.SeparatedOn, PlacedSquare.projectionRadius,
        bottomRight, topRight, axisFrame, side, dot]
      rw [abs_of_nonneg] <;> nlinarith
    · exact Or.inr one_ne_zero
  have bottom_right_center :
      (squares 1).InteriorDisjoint (squares 4) := by
    apply PlacedSquare.separatedOn_interiorDisjoint
      (axisX := -diagonal) (axisY := diagonal)
    · norm_num [PlacedSquare.SeparatedOn, PlacedSquare.projectionRadius,
        bottomRight, center, axisFrame, diagonalFrame, side, dot,
        abs_of_nonneg diagonal_nonnegative]
      have displacement_nonnegative :
          0 ≤
            -(((2 + diagonal) / 2 - (2 + diagonal - 1 / 2)) * diagonal) +
              ((2 + diagonal) / 2 - 1 / 2) * diagonal := by
        nlinarith [diagonal_sq]
      rw [abs_of_nonneg displacement_nonnegative]
      rw [abs_of_nonneg (by nlinarith [diagonal_sq] :
        0 ≤ diagonal * diagonal + diagonal * diagonal)]
      nlinarith [diagonal_sq]
    · exact Or.inl (neg_ne_zero.mpr diagonal_positive.ne')
  have top_pair :
      (squares 2).InteriorDisjoint (squares 3) := by
    apply PlacedSquare.separatedOn_interiorDisjoint
      (axisX := 1) (axisY := 0)
    · norm_num [PlacedSquare.SeparatedOn, PlacedSquare.projectionRadius,
        topLeft, topRight, axisFrame, side, dot]
      rw [abs_of_nonneg] <;> nlinarith
    · exact Or.inl one_ne_zero
  have top_left_center :
      (squares 2).InteriorDisjoint (squares 4) := by
    apply PlacedSquare.separatedOn_interiorDisjoint
      (axisX := diagonal) (axisY := -diagonal)
    · norm_num [PlacedSquare.SeparatedOn, PlacedSquare.projectionRadius,
        topLeft, center, axisFrame, diagonalFrame, side, dot,
        abs_of_nonneg diagonal_nonnegative]
      rw [abs_of_nonpos (by nlinarith [diagonal_sq] :
        -(diagonal * diagonal) + -(diagonal * diagonal) ≤ 0)]
      rw [abs_of_nonneg] <;> nlinarith [diagonal_sq]
    · exact Or.inl diagonal_positive.ne'
  have top_right_center :
      (squares 3).InteriorDisjoint (squares 4) := by
    apply PlacedSquare.separatedOn_interiorDisjoint
      (axisX := diagonal) (axisY := diagonal)
    · norm_num [PlacedSquare.SeparatedOn, PlacedSquare.projectionRadius,
        topRight, center, axisFrame, diagonalFrame, side, dot,
        abs_of_nonneg diagonal_nonnegative]
      rw [abs_of_nonneg (by nlinarith [diagonal_sq] :
        0 ≤ diagonal * diagonal + diagonal * diagonal)]
      rw [abs_of_nonpos] <;> nlinarith [diagonal_sq]
    · exact Or.inl diagonal_positive.ne'
  fin_cases left <;> fin_cases right <;> simp at different
  · exact bottom_pair
  · exact left_pair
  · exact opposite_pair
  · exact bottom_left_center
  · exact bottom_pair.symm
  · exact crossed_pair
  · exact right_pair
  · exact bottom_right_center
  · exact left_pair.symm
  · exact crossed_pair.symm
  · exact top_pair
  · exact top_left_center
  · exact opposite_pair.symm
  · exact right_pair.symm
  · exact top_pair.symm
  · exact top_right_center
  · exact bottom_left_center.symm
  · exact bottom_right_center.symm
  · exact top_left_center.symm
  · exact top_right_center.symm

noncomputable def packing : Packing 5 side where
  squares := squares
  side_nonnegative := by
    dsimp [side]
    nlinarith [diagonal_positive]
  fits := square_fits
  disjoint := square_disjoint

theorem s5_le_goebel : HasPacking 5 (2 + Real.sqrt 2 / 2) := by
  exact ⟨packing⟩

noncomputable def unavoidablePoints : Fin 4 → Point := ![
  ⟨1, 1⟩,
  ⟨1, 1 + diagonal⟩,
  ⟨1 + diagonal, 1⟩,
  ⟨1 + diagonal, 1 + diagonal⟩
]

@[simp] lemma unavoidablePoints_zero :
    unavoidablePoints 0 = ⟨1, 1⟩ := by rfl

@[simp] lemma unavoidablePoints_one :
    unavoidablePoints 1 = ⟨1, 1 + diagonal⟩ := by rfl

@[simp] lemma unavoidablePoints_two :
    unavoidablePoints 2 = ⟨1 + diagonal, 1⟩ := by rfl

@[simp] lemma unavoidablePoints_three :
    unavoidablePoints 3 = ⟨1 + diagonal, 1 + diagonal⟩ := by rfl

theorem unavoidable_points : Unavoidable unavoidablePoints side := by
  intro square fits
  change square.Fits (2 + diagonal) at fits
  by_cases center_x_left : square.center.x ≤ 1
  · by_cases center_y_bottom : square.center.y ≤ 1
    · exact ⟨0, by
        simpa using square.contains_unitCorner fits center_x_left center_y_bottom⟩
    · by_cases center_y_top : 1 + diagonal ≤ square.center.y
      · exact ⟨1, by
          simpa using square.contains_topLeftCorner fits center_x_left center_y_top⟩
      · have center_y_lower : 1 ≤ square.center.y := by linarith
        have center_y_upper : square.center.y ≤ 1 + diagonal := by linarith
        rcases square.contains_leftPair fits diagonal_positive diagonal_sq
            center_x_left center_y_lower center_y_upper with
          bottom_mem | top_mem
        · exact ⟨0, by simpa using bottom_mem⟩
        · exact ⟨1, by simpa using top_mem⟩
  · by_cases center_x_right : 1 + diagonal ≤ square.center.x
    · by_cases center_y_bottom : square.center.y ≤ 1
      · exact ⟨2, by
          simpa using square.contains_bottomRightCorner fits center_x_right
            center_y_bottom⟩
      · by_cases center_y_top : 1 + diagonal ≤ square.center.y
        · exact ⟨3, by
            simpa using square.contains_topRightCorner fits center_x_right
              center_y_top⟩
        · have center_y_lower : 1 ≤ square.center.y := by linarith
          have center_y_upper : square.center.y ≤ 1 + diagonal := by linarith
          rcases square.contains_rightPair fits diagonal_positive diagonal_sq
              center_x_right center_y_lower center_y_upper with
            bottom_mem | top_mem
          · exact ⟨2, by simpa using bottom_mem⟩
          · exact ⟨3, by simpa using top_mem⟩
    · have center_x_lower : 1 ≤ square.center.x := by linarith
      have center_x_upper : square.center.x ≤ 1 + diagonal := by linarith
      by_cases center_y_bottom : square.center.y ≤ 1
      · rcases square.contains_bottomPair fits diagonal_positive diagonal_sq
            center_x_lower center_x_upper center_y_bottom with
          left_mem | right_mem
        · exact ⟨0, by simpa using left_mem⟩
        · exact ⟨2, by simpa using right_mem⟩
      · by_cases center_y_top : 1 + diagonal ≤ square.center.y
        · rcases square.contains_topPair fits diagonal_positive diagonal_sq
              center_x_lower center_x_upper center_y_top with
            left_mem | right_mem
          · exact ⟨1, by simpa using left_mem⟩
          · exact ⟨3, by simpa using right_mem⟩
        · have center_y_lower : 1 ≤ square.center.y := by linarith
          have center_y_upper : square.center.y ≤ 1 + diagonal := by linarith
          by_cases below_diagonal : square.center.y ≤ square.center.x
          · rcases square.contains_lowerRightTriangle diagonal_positive
                diagonal_sq center_x_lower center_x_upper center_y_lower
                below_diagonal with
              bottom_left_mem | bottom_right_mem | top_right_mem
            · exact ⟨0, by simpa using bottom_left_mem⟩
            · exact ⟨2, by simpa using bottom_right_mem⟩
            · exact ⟨3, by simpa using top_right_mem⟩
          · have above_diagonal : square.center.x ≤ square.center.y := by
              linarith
            rcases square.contains_upperLeftTriangle diagonal_positive
                diagonal_sq center_x_lower center_y_lower center_y_upper
                above_diagonal with
              bottom_left_mem | top_left_mem | top_right_mem
            · exact ⟨0, by simpa using bottom_left_mem⟩
            · exact ⟨1, by simpa using top_left_mem⟩
            · exact ⟨3, by simpa using top_right_mem⟩

theorem s5_ge_goebel : IsLowerBound 5 (2 + Real.sqrt 2 / 2) := by
  simpa [side, diagonal] using lowerBound_succ_of_unavoidable unavoidable_points

theorem s5_eq_goebel : IsMinimumSide 5 (2 + Real.sqrt 2 / 2) :=
  ⟨s5_le_goebel, s5_ge_goebel⟩

end SquarePackingArchive.Records.Square5
