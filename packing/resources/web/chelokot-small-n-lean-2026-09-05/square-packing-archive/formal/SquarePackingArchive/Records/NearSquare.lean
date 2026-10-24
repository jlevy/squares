import SquarePackingArchive.Records.SquareNumbers

namespace SquarePackingArchive

lemma max_abs_add_abs_sub (left right : ℝ) :
    max |left + right| |left - right| = |left| + |right| := by
  apply le_antisymm
  · rw [max_le_iff]
    constructor
    · exact abs_add_le left right
    · simpa only [sub_eq_add_neg, abs_neg] using abs_add_le left (-right)
  · rcases le_total 0 left with left_nonnegative | left_nonpositive <;>
      rcases le_total 0 right with right_nonnegative | right_nonpositive
    · calc
        |left| + |right| = |left + right| := by
          rw [abs_of_nonneg left_nonnegative, abs_of_nonneg right_nonnegative,
            abs_of_nonneg (add_nonneg left_nonnegative right_nonnegative)]
        _ ≤ max |left + right| |left - right| := le_max_left _ _
    · calc
        |left| + |right| = |left - right| := by
          rw [abs_of_nonneg left_nonnegative, abs_of_nonpos right_nonpositive,
            abs_of_nonneg (sub_nonneg.mpr (right_nonpositive.trans left_nonnegative))]
          ring
        _ ≤ max |left + right| |left - right| := le_max_right _ _
    ·
      have difference_nonpositive : left - right ≤ 0 := sub_nonpos.mpr
        (left_nonpositive.trans right_nonnegative)
      calc
        |left| + |right| = |left - right| := by
          rw [abs_of_nonpos left_nonpositive, abs_of_nonneg right_nonnegative,
            abs_of_nonpos difference_nonpositive]
          ring
        _ ≤ max |left + right| |left - right| := le_max_right _ _
    ·
      have sum_nonpositive : left + right ≤ 0 := add_nonpos left_nonpositive right_nonpositive
      calc
        |left| + |right| = |left + right| := by
          rw [abs_of_nonpos left_nonpositive, abs_of_nonpos right_nonpositive,
            abs_of_nonpos sum_nonpositive]
          ring
        _ ≤ max |left + right| |left - right| := le_max_left _ _

noncomputable def frameExtent (frame : Frame) : ℝ :=
  (|frame.cosine| + |frame.sine|) / 2

lemma PlacedSquare.center_bounds
    {square : PlacedSquare} {side : ℝ} (fits : square.Fits side) :
    frameExtent square.frame ≤ square.center.x ∧
      square.center.x + frameExtent square.frame ≤ side ∧
        frameExtent square.frame ≤ square.center.y ∧
          square.center.y + frameExtent square.frame ≤ side := by
  have firstCorner := fits (point := square.point (1 / 2) (1 / 2)) (by
    refine ⟨1 / 2, 1 / 2, ?_, ?_, rfl⟩ <;> norm_num)
  have oppositeFirstCorner := fits (point := square.point (-1 / 2) (-1 / 2)) (by
    refine ⟨-1 / 2, -1 / 2, ?_, ?_, rfl⟩ <;> norm_num)
  have secondCorner := fits (point := square.point (1 / 2) (-1 / 2)) (by
    refine ⟨1 / 2, -1 / 2, ?_, ?_, rfl⟩ <;> norm_num)
  have oppositeSecondCorner := fits (point := square.point (-1 / 2) (1 / 2)) (by
    refine ⟨-1 / 2, 1 / 2, ?_, ?_, rfl⟩ <;> norm_num)
  simp only [PlacedSquare.point, Frame.place] at firstCorner oppositeFirstCorner secondCorner oppositeSecondCorner
  have cosine_sub_sine_left :
      |square.frame.cosine - square.frame.sine| ≤ 2 * square.center.x := by
    rw [abs_le]
    constructor <;> nlinarith [firstCorner.1, oppositeFirstCorner.1]
  have cosine_add_sine_left :
      |square.frame.cosine + square.frame.sine| ≤ 2 * square.center.x := by
    rw [abs_le]
    constructor <;> nlinarith [secondCorner.1, oppositeSecondCorner.1]
  have cosine_sub_sine_right :
      |square.frame.cosine - square.frame.sine| ≤ 2 * (side - square.center.x) := by
    rw [abs_le]
    constructor <;> nlinarith [firstCorner.2.1, oppositeFirstCorner.2.1]
  have cosine_add_sine_right :
      |square.frame.cosine + square.frame.sine| ≤ 2 * (side - square.center.x) := by
    rw [abs_le]
    constructor <;> nlinarith [secondCorner.2.1, oppositeSecondCorner.2.1]
  have sine_add_cosine_bottom :
      |square.frame.sine + square.frame.cosine| ≤ 2 * square.center.y := by
    rw [abs_le]
    constructor <;> nlinarith [firstCorner.2.2.1, oppositeFirstCorner.2.2.1]
  have sine_sub_cosine_bottom :
      |square.frame.sine - square.frame.cosine| ≤ 2 * square.center.y := by
    rw [abs_le]
    constructor <;> nlinarith [secondCorner.2.2.1, oppositeSecondCorner.2.2.1]
  have sine_add_cosine_top :
      |square.frame.sine + square.frame.cosine| ≤ 2 * (side - square.center.y) := by
    rw [abs_le]
    constructor <;> nlinarith [firstCorner.2.2.2, oppositeFirstCorner.2.2.2]
  have sine_sub_cosine_top :
      |square.frame.sine - square.frame.cosine| ≤ 2 * (side - square.center.y) := by
    rw [abs_le]
    constructor <;> nlinarith [secondCorner.2.2.2, oppositeSecondCorner.2.2.2]
  have horizontal_left := max_le cosine_add_sine_left cosine_sub_sine_left
  have horizontal_right := max_le cosine_add_sine_right cosine_sub_sine_right
  have vertical_bottom := max_le sine_add_cosine_bottom sine_sub_cosine_bottom
  have vertical_top := max_le sine_add_cosine_top sine_sub_cosine_top
  rw [max_abs_add_abs_sub] at horizontal_left horizontal_right vertical_bottom vertical_top
  constructor
  · unfold frameExtent
    linarith
  · constructor
    · unfold frameExtent
      linarith
    · constructor
      · unfold frameExtent
        linarith
      · unfold frameExtent
        linarith

lemma Frame.one_le_abs_cosine_add_abs_sine (frame : Frame) :
    1 ≤ |frame.cosine| + |frame.sine| := by
  let total := |frame.cosine| + |frame.sine|
  have total_nonnegative : 0 ≤ total := add_nonneg (abs_nonneg _) (abs_nonneg _)
  have total_sq : 1 ≤ total ^ 2 := by
    dsimp [total]
    rw [add_sq, sq_abs, sq_abs]
    nlinarith [frame.unit,
      mul_nonneg (abs_nonneg frame.cosine) (abs_nonneg frame.sine)]
  by_contra not_at_least_one
  have total_lt_one : total < 1 := lt_of_not_ge not_at_least_one
  have product_positive : 0 < (1 - total) * (1 + total) :=
    mul_pos (sub_pos.mpr total_lt_one) (by linarith)
  nlinarith [product_positive]

lemma PlacedSquare.center_deviation_bounds
    {square : PlacedSquare} {side : ℝ} (fits : square.Fits side) :
    |side / 2 - square.center.x| ≤
        (side - (|square.frame.cosine| + |square.frame.sine|)) / 2 ∧
      |side / 2 - square.center.y| ≤
        (side - (|square.frame.cosine| + |square.frame.sine|)) / 2 := by
  rcases center_bounds fits with
    ⟨x_lower, x_upper, y_lower, y_upper⟩
  constructor <;> rw [abs_le] <;> constructor <;>
    unfold frameExtent at * <;> linarith

lemma PlacedSquare.containerCenter_interior
    {square : PlacedSquare} {side : ℝ}
    (fits : square.Fits side) (side_lt_two : side < 2) :
    square.InteriorContains ⟨side / 2, side / 2⟩ := by
  let cosine := square.frame.cosine
  let sine := square.frame.sine
  let total := |cosine| + |sine|
  let horizontalDelta := side / 2 - square.center.x
  let verticalDelta := side / 2 - square.center.y
  let localX := horizontalDelta * cosine + verticalDelta * sine
  let localY := -horizontalDelta * sine + verticalDelta * cosine
  have total_at_least_one : 1 ≤ total := by
    exact square.frame.one_le_abs_cosine_add_abs_sine
  have total_positive : 0 < total := lt_of_lt_of_le zero_lt_one total_at_least_one
  have deviation_bounds := center_deviation_bounds fits
  have horizontal_bound : |horizontalDelta| ≤ (side - total) / 2 := by
    exact deviation_bounds.1
  have vertical_bound : |verticalDelta| ≤ (side - total) / 2 := by
    exact deviation_bounds.2
  have gap_nonnegative : 0 ≤ side - total := by
    rcases center_bounds fits with ⟨x_lower, x_upper, _, _⟩
    unfold frameExtent at x_lower x_upper
    dsimp [total, cosine, sine]
    linarith
  have product_lt_one : total * (side - total) < 1 := by
    have scaled_side_lt : total * side < total * 2 :=
      mul_lt_mul_of_pos_left side_lt_two total_positive
    nlinarith [sq_nonneg (total - 1)]
  have localX_lt : |localX| < 1 / 2 := by
    calc
      |localX| ≤ |horizontalDelta * cosine| + |verticalDelta * sine| := by
        exact abs_add_le _ _
      _ = |horizontalDelta| * |cosine| + |verticalDelta| * |sine| := by
        rw [abs_mul, abs_mul]
      _ ≤ ((side - total) / 2) * |cosine| +
          ((side - total) / 2) * |sine| := by
        gcongr
      _ = total * (side - total) / 2 := by
        dsimp [total]
        ring
      _ < 1 / 2 := by linarith
  have localY_lt : |localY| < 1 / 2 := by
    calc
      |localY| ≤ |-horizontalDelta * sine| + |verticalDelta * cosine| := by
        exact abs_add_le _ _
      _ = |horizontalDelta| * |sine| + |verticalDelta| * |cosine| := by
        rw [abs_mul, abs_mul, abs_neg]
      _ ≤ ((side - total) / 2) * |sine| +
          ((side - total) / 2) * |cosine| := by
        gcongr
      _ = total * (side - total) / 2 := by
        dsimp [total]
        ring
      _ < 1 / 2 := by linarith
  refine ⟨localX, localY, localX_lt, localY_lt, ?_⟩
  simp only [PlacedSquare.point, Frame.place, Point.mk.injEq]
  constructor
  · dsimp [localX, localY, horizontalDelta, verticalDelta, cosine, sine]
    linear_combination
      -(side / 2 - square.center.x) * square.frame.unit
  · dsimp [localX, localY, horizontalDelta, verticalDelta, cosine, sine]
    linear_combination
      -(side / 2 - square.center.y) * square.frame.unit

end SquarePackingArchive

namespace SquarePackingArchive.Records.NearSquare

open SquareNumbers

theorem nearSquare_hasPacking (size removed : ℕ) :
    HasPacking (size * size - removed) size :=
  (squareNumber_hasPacking size).mono (Nat.sub_le (size * size) removed)

theorem squareMinusOne_hasPacking (size : ℕ) :
    HasPacking (size * size - 1) size :=
  nearSquare_hasPacking size 1

theorem squareMinusTwo_hasPacking (size : ℕ) :
    HasPacking (size * size - 2) size :=
  nearSquare_hasPacking size 2

lemma two_squares_side_ge_two {side : ℝ} (packing : Packing 2 side) :
    2 ≤ side := by
  by_contra side_too_small
  have side_lt_two : side < 2 := lt_of_not_ge side_too_small
  have first_contains := (packing.squares 0).containerCenter_interior
    (packing.fits 0) side_lt_two
  have second_contains := (packing.squares 1).containerCenter_interior
    (packing.fits 1) side_lt_two
  exact packing.disjoint 0 1 (by decide) ⟨side / 2, side / 2⟩
    ⟨first_contains, second_contains⟩

theorem s2_eq_two : IsMinimumSide 2 2 := by
  constructor
  · simpa using squareMinusTwo_hasPacking 2
  · intro side hasPacking
    exact two_squares_side_ge_two hasPacking.some

theorem s3_eq_two : IsMinimumSide 3 2 := by
  constructor
  · simpa using squareMinusOne_hasPacking 2
  · intro side hasPacking
    let twoPacking := hasPacking.some.reindex (Fin.castLEEmb (by norm_num : 2 ≤ 3))
    exact two_squares_side_ge_two twoPacking

end SquarePackingArchive.Records.NearSquare
