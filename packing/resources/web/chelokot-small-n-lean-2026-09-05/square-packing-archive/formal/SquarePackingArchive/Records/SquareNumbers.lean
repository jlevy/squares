import SquarePackingArchive.Area

namespace SquarePackingArchive.Records.SquareNumbers

lemma fin_cast_distance_ge_one
    {size : ℕ} {left right : Fin size} (different : left ≠ right) :
    1 ≤ |(left : ℝ) - (right : ℝ)| := by
  rcases lt_or_gt_of_ne different with before | after
  · have separated : (left : ℝ) + 1 ≤ right := by
      exact_mod_cast (Nat.succ_le_iff.mpr before)
    have ordered : (left : ℝ) - right ≤ 0 := by linarith
    rw [abs_of_nonpos ordered]
    linarith
  · have separated : (right : ℝ) + 1 ≤ left := by
      exact_mod_cast (Nat.succ_le_iff.mpr after)
    have ordered : 0 ≤ (left : ℝ) - right := by linarith
    rw [abs_of_nonneg ordered]
    linarith

noncomputable def gridSquare
    {size : ℕ} (column row : Fin size) : PlacedSquare where
  center := ⟨(column : ℝ) + 1 / 2, (row : ℝ) + 1 / 2⟩
  frame := { cosine := 1, sine := 0, unit := by norm_num }

lemma gridSquare_fits {size : ℕ} (column row : Fin size) :
    (gridSquare column row).Fits size := by
  intro point contains
  rcases contains with ⟨localX, localY, localX_le, localY_le, rfl⟩
  rcases abs_le.mp localX_le with ⟨localX_lower, localX_upper⟩
  rcases abs_le.mp localY_le with ⟨localY_lower, localY_upper⟩
  have column_upper : (column : ℝ) + 1 ≤ size := by
    exact_mod_cast column.isLt
  have row_upper : (row : ℝ) + 1 ≤ size := by
    exact_mod_cast row.isLt
  have column_nonnegative : (0 : ℝ) ≤ column := by positivity
  have row_nonnegative : (0 : ℝ) ≤ row := by positivity
  simp only [gridSquare, PlacedSquare.point, Frame.place, Container.Contains]
  constructor
  · norm_num
    linarith
  · constructor
    · norm_num
      linarith
    · constructor <;> norm_num <;> linarith

lemma gridSquare_horizontal_disjoint
    {size : ℕ} {leftColumn rightColumn leftRow rightRow : Fin size}
    (different : leftColumn ≠ rightColumn) :
    (gridSquare leftColumn leftRow).InteriorDisjoint
      (gridSquare rightColumn rightRow) := by
  apply PlacedSquare.separatedOn_interiorDisjoint (axisX := 1) (axisY := 0)
  · have distance := fin_cast_distance_ge_one different
    rw [abs_sub_comm] at distance
    norm_num [PlacedSquare.SeparatedOn, PlacedSquare.projectionRadius,
      gridSquare, dot]
    exact distance
  · exact Or.inl one_ne_zero

lemma gridSquare_vertical_disjoint
    {size : ℕ} {leftColumn rightColumn leftRow rightRow : Fin size}
    (different : leftRow ≠ rightRow) :
    (gridSquare leftColumn leftRow).InteriorDisjoint
      (gridSquare rightColumn rightRow) := by
  apply PlacedSquare.separatedOn_interiorDisjoint (axisX := 0) (axisY := 1)
  · have distance := fin_cast_distance_ge_one different
    rw [abs_sub_comm] at distance
    norm_num [PlacedSquare.SeparatedOn, PlacedSquare.projectionRadius,
      gridSquare, dot]
    exact distance
  · exact Or.inr one_ne_zero

noncomputable def gridPacking (size : ℕ) : Packing (size * size) size where
  squares := fun index =>
    let cell := finProdFinEquiv.symm index
    gridSquare cell.1 cell.2
  side_nonnegative := by positivity
  fits := by
    intro index
    exact gridSquare_fits _ _
  disjoint := by
    intro left right different
    let leftCell := finProdFinEquiv.symm left
    let rightCell := finProdFinEquiv.symm right
    have cells_different : leftCell ≠ rightCell := by
      intro cells_equal
      exact different (finProdFinEquiv.symm.injective cells_equal)
    by_cases columns_different : leftCell.1 ≠ rightCell.1
    · exact gridSquare_horizontal_disjoint columns_different
    · apply gridSquare_vertical_disjoint
      intro rows_equal
      apply cells_different
      exact Prod.ext (not_ne_iff.mp columns_different) rows_equal

theorem squareNumber_hasPacking (size : ℕ) :
    HasPacking (size * size) size :=
  ⟨gridPacking size⟩

theorem squareNumber_isMinimumSide (size : ℕ) :
    IsMinimumSide (size * size) size := by
  constructor
  · exact squareNumber_hasPacking size
  · intro candidateSide hasPacking
    rcases hasPacking with ⟨packing⟩
    have area_bound := packing.squareCount_le_side_sq
    have size_nonnegative : (0 : ℝ) ≤ size := by positivity
    have side_nonnegative := packing.side_nonnegative
    push_cast at area_bound
    nlinarith

theorem s1_eq_one : IsMinimumSide 1 1 := by
  simpa using squareNumber_isMinimumSide 1

theorem s4_eq_two : IsMinimumSide 4 2 := by
  simpa using squareNumber_isMinimumSide 2

theorem s9_eq_three : IsMinimumSide 9 3 := by
  simpa using squareNumber_isMinimumSide 3

theorem s16_eq_four : IsMinimumSide 16 4 := by
  simpa using squareNumber_isMinimumSide 4

theorem s25_eq_five : IsMinimumSide 25 5 := by
  simpa using squareNumber_isMinimumSide 5

theorem s36_eq_six : IsMinimumSide 36 6 := by
  simpa using squareNumber_isMinimumSide 6

theorem s49_eq_seven : IsMinimumSide 49 7 := by
  simpa using squareNumber_isMinimumSide 7

theorem s64_eq_eight : IsMinimumSide 64 8 := by
  simpa using squareNumber_isMinimumSide 8

theorem s81_eq_nine : IsMinimumSide 81 9 := by
  simpa using squareNumber_isMinimumSide 9

end SquarePackingArchive.Records.SquareNumbers
