import SquarePackingArchive.Unavoidable
import SquarePackingArchive.Triangle

namespace SquarePackingArchive

lemma Frame.height_add_gap_product_le_sum_of_gap_le_four_fifths
    (frame : Frame) {height gap : ℝ}
    (cosine_nonnegative : 0 ≤ frame.cosine)
    (sine_nonnegative : 0 ≤ frame.sine)
    (height_upper : height ≤ 1)
    (gap_upper : gap ≤ 4 / 5) :
    height + gap * (frame.cosine * frame.sine) ≤
      frame.cosine + frame.sine := by
  have component_product_nonnegative :
      0 ≤ frame.cosine * frame.sine :=
    mul_nonneg cosine_nonnegative sine_nonnegative
  have component_sum_at_least_one :
      1 ≤ frame.cosine + frame.sine := by
    nlinarith [frame.unit]
  have component_sum_at_most_three_halves :
      frame.cosine + frame.sine ≤ 3 / 2 := by
    have sum_sq_at_most_two :
        (frame.cosine + frame.sine) ^ 2 ≤ 2 := by
      nlinarith [frame.unit, sq_nonneg (frame.cosine - frame.sine)]
    nlinarith
  have rational_component_product_bound :
      4 / 5 * (frame.cosine * frame.sine) ≤
        frame.cosine + frame.sine - 1 := by
    have product_nonpositive :
        (frame.cosine + frame.sine - 1) *
            (2 * (frame.cosine + frame.sine) - 3) ≤ 0 :=
      mul_nonpos_of_nonneg_of_nonpos (by linarith) (by linarith)
    nlinarith [frame.unit]
  have gap_component_product_bound :
      gap * (frame.cosine * frame.sine) ≤
        frame.cosine + frame.sine - 1 :=
    (mul_le_mul_of_nonneg_right gap_upper component_product_nonnegative).trans
      rational_component_product_bound
  linarith

set_option maxHeartbeats 1000000 in
lemma PlacedSquare.contains_bottomPairWith_of_nonnegative_frame
    {square : PlacedSquare} {side left targetHeight gap : ℝ}
    (fits : square.Fits side)
    (target_height_upper : targetHeight ≤ 1)
    (gap_positive : 0 < gap)
    (gap_upper : gap ≤ 1)
    (cosine_nonnegative : 0 ≤ square.frame.cosine)
    (sine_nonnegative : 0 ≤ square.frame.sine)
    (weighted_bound :
      targetHeight + gap * (square.frame.cosine * square.frame.sine) ≤
        square.frame.cosine + square.frame.sine)
    (center_x_lower : left ≤ square.center.x)
    (center_x_upper : square.center.x ≤ left + gap)
    (center_y_upper : square.center.y ≤ targetHeight) :
    square.Contains ⟨left, targetHeight⟩ ∨
      square.Contains ⟨left + gap, targetHeight⟩ := by
  have lower_corner_bounds := fits
    (point := square.point (-1 / 2) (-1 / 2))
    ⟨-1 / 2, -1 / 2, by norm_num, by norm_num, rfl⟩
  have center_y_lower :
      (square.frame.cosine + square.frame.sine) / 2 ≤ square.center.y := by
    have := lower_corner_bounds.2.2.1
    simp [PlacedSquare.point, Frame.place] at this
    linarith
  let horizontalOffset := square.center.x - left
  let verticalOffset := targetHeight - square.center.y
  let leftLocalX :=
    -horizontalOffset * square.frame.cosine +
      verticalOffset * square.frame.sine
  let leftLocalY :=
    horizontalOffset * square.frame.sine +
      verticalOffset * square.frame.cosine
  let rightLocalX :=
    (gap - horizontalOffset) * square.frame.cosine +
      verticalOffset * square.frame.sine
  let rightLocalY :=
    -(gap - horizontalOffset) * square.frame.sine +
      verticalOffset * square.frame.cosine
  have horizontal_offset_nonnegative : 0 ≤ horizontalOffset := by
    dsimp [horizontalOffset]
    linarith
  have horizontal_offset_upper : horizontalOffset ≤ gap := by
    dsimp [horizontalOffset]
    linarith
  have vertical_offset_nonnegative : 0 ≤ verticalOffset := by
    dsimp [verticalOffset]
    linarith
  have vertical_offset_weighted_upper :
      verticalOffset ≤
        targetHeight -
          (square.frame.cosine + square.frame.sine) / 2 := by
    dsimp [verticalOffset]
    linarith
  have vertical_offset_upper :
      verticalOffset ≤
        1 - (square.frame.cosine + square.frame.sine) / 2 := by
    dsimp [verticalOffset]
    linarith
  have cosine_at_most_one :=
    square.frame.cosine_le_one cosine_nonnegative
  have sine_at_most_one :=
    square.frame.sine_le_one sine_nonnegative
  have vertical_sine_upper :
      verticalOffset * square.frame.sine ≤
        (1 - (square.frame.cosine + square.frame.sine) / 2) *
          square.frame.sine :=
    mul_le_mul_of_nonneg_right vertical_offset_upper sine_nonnegative
  have vertical_cosine_upper :
      verticalOffset * square.frame.cosine ≤
        (1 - (square.frame.cosine + square.frame.sine) / 2) *
          square.frame.cosine :=
    mul_le_mul_of_nonneg_right vertical_offset_upper cosine_nonnegative
  have left_local_x_upper : leftLocalX ≤ 1 / 2 := by
    have first_term_nonpositive :
        -horizontalOffset * square.frame.cosine ≤ 0 := by
      exact mul_nonpos_of_nonpos_of_nonneg
        (neg_nonpos.mpr horizontal_offset_nonnegative) cosine_nonnegative
    have vertical_term_upper :
        (1 - (square.frame.cosine + square.frame.sine) / 2) *
            square.frame.sine ≤ 1 / 2 := by
      nlinarith [square.frame.unit,
        sq_nonneg (1 - square.frame.sine)]
    dsimp [leftLocalX]
    linarith
  have left_local_y_nonnegative : 0 ≤ leftLocalY := by
    dsimp [leftLocalY]
    positivity
  have right_local_x_nonnegative : 0 ≤ rightLocalX := by
    dsimp [rightLocalX]
    positivity
  have right_local_y_upper : rightLocalY ≤ 1 / 2 := by
    have first_term_nonpositive :
        -(gap - horizontalOffset) * square.frame.sine ≤ 0 := by
      have : 0 ≤ gap - horizontalOffset := by linarith
      exact mul_nonpos_of_nonpos_of_nonneg (neg_nonpos.mpr this)
        sine_nonnegative
    have vertical_term_upper :
        (1 - (square.frame.cosine + square.frame.sine) / 2) *
            square.frame.cosine ≤ 1 / 2 := by
      nlinarith [square.frame.unit,
        sq_nonneg (1 - square.frame.cosine)]
    dsimp [rightLocalY]
    linarith
  have left_local_x_eq :
      square.localX ⟨left, targetHeight⟩ = leftLocalX := by
    dsimp [PlacedSquare.localX, leftLocalX, horizontalOffset, verticalOffset]
    ring
  have left_local_y_eq :
      square.localY ⟨left, targetHeight⟩ = leftLocalY := by
    dsimp [PlacedSquare.localY, leftLocalY, horizontalOffset, verticalOffset]
    ring
  have right_local_x_eq :
      square.localX ⟨left + gap, targetHeight⟩ = rightLocalX := by
    dsimp [PlacedSquare.localX, rightLocalX, horizontalOffset, verticalOffset]
    ring
  have right_local_y_eq :
      square.localY ⟨left + gap, targetHeight⟩ = rightLocalY := by
    dsimp [PlacedSquare.localY, rightLocalY, horizontalOffset, verticalOffset]
    ring
  by_contra neither_point
  push Not at neither_point
  have left_miss : leftLocalX < -1 / 2 ∨ 1 / 2 < leftLocalY := by
    by_contra coordinates_inside
    push Not at coordinates_inside
    apply neither_point.1
    rw [square.contains_iff_localCoordinates, left_local_x_eq,
      left_local_y_eq]
    exact ⟨abs_le.mpr ⟨by linarith [coordinates_inside.1], left_local_x_upper⟩,
      abs_le.mpr ⟨by linarith, coordinates_inside.2⟩⟩
  have right_miss : 1 / 2 < rightLocalX ∨ rightLocalY < -1 / 2 := by
    by_contra coordinates_inside
    push Not at coordinates_inside
    apply neither_point.2
    rw [square.contains_iff_localCoordinates, right_local_x_eq,
      right_local_y_eq]
    exact ⟨abs_le.mpr ⟨by linarith, coordinates_inside.1⟩,
      abs_le.mpr ⟨by linarith [coordinates_inside.2], right_local_y_upper⟩⟩
  rcases left_miss with left_x_low | left_y_high
  · rcases right_miss with right_x_high | right_y_low
    · have gap_cosine_gt_one : 1 < gap * square.frame.cosine := by
        dsimp [leftLocalX, rightLocalX] at left_x_low right_x_high
        linarith
      have gap_cosine_le_gap : gap * square.frame.cosine ≤ gap :=
        mul_le_of_le_one_right gap_positive.le cosine_at_most_one
      linarith
    · have horizontal_offset_gt_half : 1 / 2 < horizontalOffset := by
        have offset_cosine_gt_half :
            1 / 2 < horizontalOffset * square.frame.cosine := by
          dsimp [leftLocalX] at left_x_low
          have vertical_term_nonnegative :
              0 ≤ verticalOffset * square.frame.sine := by positivity
          linarith
        have offset_cosine_le_offset :
            horizontalOffset * square.frame.cosine ≤ horizontalOffset :=
          mul_le_of_le_one_right horizontal_offset_nonnegative
            cosine_at_most_one
        linarith
      have remaining_offset_gt_half :
          1 / 2 < gap - horizontalOffset := by
        have remaining_sine_gt_half :
            1 / 2 < (gap - horizontalOffset) * square.frame.sine := by
          dsimp [rightLocalY] at right_y_low
          have vertical_term_nonnegative :
              0 ≤ verticalOffset * square.frame.cosine := by positivity
          linarith
        have remaining_nonnegative : 0 ≤ gap - horizontalOffset := by
          linarith
        have remaining_sine_le_remaining :
            (gap - horizontalOffset) * square.frame.sine ≤
              gap - horizontalOffset :=
          mul_le_of_le_one_right remaining_nonnegative sine_at_most_one
        linarith
      linarith
  · rcases right_miss with right_x_high | right_y_low
    · have weighted_coordinates_gt :
          (square.frame.cosine + square.frame.sine) / 2 <
            leftLocalY * square.frame.cosine +
              rightLocalX * square.frame.sine := by
        by_cases cosine_zero : square.frame.cosine = 0
        · have sine_one : square.frame.sine = 1 := by
            nlinarith [square.frame.unit]
          dsimp [rightLocalX] at right_x_high
          nlinarith
        · have cosine_positive : 0 < square.frame.cosine :=
            lt_of_le_of_ne cosine_nonnegative (Ne.symm cosine_zero)
          have left_weighted_gt :=
            mul_lt_mul_of_pos_right left_y_high cosine_positive
          have right_weighted_le :=
            mul_le_mul_of_nonneg_right right_x_high.le sine_nonnegative
          linarith
      have weighted_coordinates_eq :
          leftLocalY * square.frame.cosine +
              rightLocalX * square.frame.sine =
            verticalOffset +
              gap * (square.frame.cosine * square.frame.sine) := by
        dsimp [leftLocalY, rightLocalX]
        calc
          _ = verticalOffset *
                (square.frame.cosine ^ 2 + square.frame.sine ^ 2) +
              gap * (square.frame.cosine * square.frame.sine) := by ring
          _ = _ := by rw [square.frame.unit]; ring
      have weighted_coordinates_upper :
          verticalOffset +
              gap * (square.frame.cosine * square.frame.sine) ≤
            (square.frame.cosine + square.frame.sine) / 2 := by
        linarith [vertical_offset_weighted_upper, weighted_bound]
      rw [weighted_coordinates_eq] at weighted_coordinates_gt
      linarith
    · have gap_sine_gt_one : 1 < gap * square.frame.sine := by
        dsimp [leftLocalY, rightLocalY] at left_y_high right_y_low
        linarith
      have gap_sine_le_gap : gap * square.frame.sine ≤ gap :=
        mul_le_of_le_one_right gap_positive.le sine_at_most_one
      linarith

lemma PlacedSquare.contains_bottomPairWith
    {square : PlacedSquare} {side left targetHeight gap : ℝ}
    (fits : square.Fits side)
    (target_height_upper : targetHeight ≤ 1)
    (gap_positive : 0 < gap)
    (gap_upper : gap ≤ 1)
    (weighted_bound : ∀ frame : Frame,
      0 ≤ frame.cosine → 0 ≤ frame.sine →
        targetHeight + gap * (frame.cosine * frame.sine) ≤
          frame.cosine + frame.sine)
    (center_x_lower : left ≤ square.center.x)
    (center_x_upper : square.center.x ≤ left + gap)
    (center_y_upper : square.center.y ≤ targetHeight) :
    square.Contains ⟨left, targetHeight⟩ ∨
      square.Contains ⟨left + gap, targetHeight⟩ := by
  have normalized_result :=
    square.firstQuadrant.contains_bottomPairWith_of_nonnegative_frame
      ((square.firstQuadrant_fits_iff side).2 fits)
      target_height_upper gap_positive gap_upper
      square.firstQuadrant_cosine_nonnegative
      square.firstQuadrant_sine_nonnegative
      (weighted_bound square.firstQuadrant.frame
        square.firstQuadrant_cosine_nonnegative
        square.firstQuadrant_sine_nonnegative)
      (by simpa using center_x_lower)
      (by simpa using center_x_upper)
      (by simpa using center_y_upper)
  simpa using normalized_result

lemma PlacedSquare.contains_bottomPair
    {square : PlacedSquare} {side gap : ℝ}
    (fits : square.Fits side)
    (gap_positive : 0 < gap)
    (gap_sq : gap ^ 2 = 1 / 2)
    (center_x_lower : 1 ≤ square.center.x)
    (center_x_upper : square.center.x ≤ 1 + gap)
    (center_y_upper : square.center.y ≤ 1) :
    square.Contains ⟨1, 1⟩ ∨ square.Contains ⟨1 + gap, 1⟩ := by
  have gap_upper : gap ≤ 1 := by nlinarith [gap_sq]
  apply square.contains_bottomPairWith fits (by norm_num)
    gap_positive gap_upper
  · intro frame cosine_nonnegative sine_nonnegative
    have gap_at_most_three_quarters : gap ≤ 3 / 4 := by
      nlinarith [gap_sq]
    exact frame.height_add_gap_product_le_sum_of_gap_le_four_fifths
      cosine_nonnegative sine_nonnegative (by norm_num)
      (by linarith)
  · exact center_x_lower
  · exact center_x_upper
  · exact center_y_upper

lemma PlacedSquare.contains_topPair
    {square : PlacedSquare} {gap : ℝ}
    (fits : square.Fits (2 + gap))
    (gap_positive : 0 < gap)
    (gap_sq : gap ^ 2 = 1 / 2)
    (center_x_lower : 1 ≤ square.center.x)
    (center_x_upper : square.center.x ≤ 1 + gap)
    (center_y_lower : 1 + gap ≤ square.center.y) :
    square.Contains ⟨1, 1 + gap⟩ ∨
      square.Contains ⟨1 + gap, 1 + gap⟩ := by
  have reflected_result :=
    (square.reflectY (2 + gap)).contains_bottomPair
      ((square.reflectY_fits_iff (2 + gap)).2 fits)
      gap_positive gap_sq
      (by simpa [PlacedSquare.reflectY, Point.reflectY] using center_x_lower)
      (by simpa [PlacedSquare.reflectY, Point.reflectY] using center_x_upper)
      (by simp [PlacedSquare.reflectY, Point.reflectY]; linarith)
  rcases reflected_result with left_mem | right_mem
  · exact Or.inl ((square.reflectY_contains_iff (2 + gap)
      ⟨1, 1 + gap⟩).1 (by
        convert left_mem using 1
        all_goals norm_num [Point.reflectY]))
  · exact Or.inr ((square.reflectY_contains_iff (2 + gap)
      ⟨1 + gap, 1 + gap⟩).1 (by
        convert right_mem using 1
        all_goals norm_num [Point.reflectY]))

lemma PlacedSquare.contains_leftPair
    {square : PlacedSquare} {side gap : ℝ}
    (fits : square.Fits side)
    (gap_positive : 0 < gap)
    (gap_sq : gap ^ 2 = 1 / 2)
    (center_x_upper : square.center.x ≤ 1)
    (center_y_lower : 1 ≤ square.center.y)
    (center_y_upper : square.center.y ≤ 1 + gap) :
    square.Contains ⟨1, 1⟩ ∨ square.Contains ⟨1, 1 + gap⟩ := by
  have swapped_result := square.swap.contains_bottomPair
    ((square.swap_fits_iff side).2 fits) gap_positive gap_sq
    (by simpa [PlacedSquare.swap, Point.swap] using center_y_lower)
    (by simpa [PlacedSquare.swap, Point.swap] using center_y_upper)
    (by simpa [PlacedSquare.swap, Point.swap] using center_x_upper)
  rcases swapped_result with bottom_mem | top_mem
  · exact Or.inl ((square.swap_contains_iff ⟨1, 1⟩).1
      (by simpa [Point.swap] using bottom_mem))
  · exact Or.inr ((square.swap_contains_iff ⟨1, 1 + gap⟩).1
      (by simpa [Point.swap] using top_mem))

lemma PlacedSquare.contains_rightPair
    {square : PlacedSquare} {gap : ℝ}
    (fits : square.Fits (2 + gap))
    (gap_positive : 0 < gap)
    (gap_sq : gap ^ 2 = 1 / 2)
    (center_x_lower : 1 + gap ≤ square.center.x)
    (center_y_lower : 1 ≤ square.center.y)
    (center_y_upper : square.center.y ≤ 1 + gap) :
    square.Contains ⟨1 + gap, 1⟩ ∨
      square.Contains ⟨1 + gap, 1 + gap⟩ := by
  have reflected_result :=
    (square.reflectX (2 + gap)).contains_leftPair
      ((square.reflectX_fits_iff (2 + gap)).2 fits)
      gap_positive gap_sq
      (by simp [PlacedSquare.reflectX, Point.reflectX]; linarith)
      (by simpa [PlacedSquare.reflectX, Point.reflectX] using center_y_lower)
      (by simpa [PlacedSquare.reflectX, Point.reflectX] using center_y_upper)
  rcases reflected_result with bottom_mem | top_mem
  · exact Or.inl ((square.reflectX_contains_iff (2 + gap)
      ⟨1 + gap, 1⟩).1 (by
        convert bottom_mem using 1
        all_goals norm_num [Point.reflectX]))
  · exact Or.inr ((square.reflectX_contains_iff (2 + gap)
      ⟨1 + gap, 1 + gap⟩).1 (by
        convert top_mem using 1
        all_goals norm_num [Point.reflectX]))

set_option maxHeartbeats 1000000 in
lemma PlacedSquare.contains_lowerRightTriangle_of_nonnegative_frame
    {square : PlacedSquare} {gap : ℝ}
    (gap_positive : 0 < gap)
    (gap_sq : gap ^ 2 = 1 / 2)
    (cosine_nonnegative : 0 ≤ square.frame.cosine)
    (sine_nonnegative : 0 ≤ square.frame.sine)
    (center_x_lower : 1 ≤ square.center.x)
    (center_x_upper : square.center.x ≤ 1 + gap)
    (center_y_lower : 1 ≤ square.center.y)
    (center_y_below_diagonal : square.center.y ≤ square.center.x) :
    square.Contains ⟨1, 1⟩ ∨
      square.Contains ⟨1 + gap, 1⟩ ∨
        square.Contains ⟨1 + gap, 1 + gap⟩ := by
  let horizontalOffset := square.center.x - 1
  let verticalOffset := square.center.y - 1
  let bottomLeftLocalX :=
    -horizontalOffset * square.frame.cosine -
      verticalOffset * square.frame.sine
  let bottomLeftLocalY :=
    horizontalOffset * square.frame.sine -
      verticalOffset * square.frame.cosine
  let bottomRightLocalX :=
    (gap - horizontalOffset) * square.frame.cosine -
      verticalOffset * square.frame.sine
  let bottomRightLocalY :=
    -(gap - horizontalOffset) * square.frame.sine -
      verticalOffset * square.frame.cosine
  let topRightLocalX :=
    (gap - horizontalOffset) * square.frame.cosine +
      (gap - verticalOffset) * square.frame.sine
  let topRightLocalY :=
    -(gap - horizontalOffset) * square.frame.sine +
      (gap - verticalOffset) * square.frame.cosine
  have horizontal_offset_nonnegative : 0 ≤ horizontalOffset := by
    dsimp [horizontalOffset]
    linarith
  have horizontal_offset_upper : horizontalOffset ≤ gap := by
    dsimp [horizontalOffset]
    linarith
  have vertical_offset_nonnegative : 0 ≤ verticalOffset := by
    dsimp [verticalOffset]
    linarith
  have vertical_offset_le_horizontal : verticalOffset ≤ horizontalOffset := by
    dsimp [horizontalOffset, verticalOffset]
    linarith
  have cosine_at_most_one :=
    square.frame.cosine_le_one cosine_nonnegative
  have sine_at_most_one :=
    square.frame.sine_le_one sine_nonnegative
  have gap_lt_one : gap < 1 := by nlinarith [gap_sq]
  have component_sum_upper :
      square.frame.cosine + square.frame.sine ≤ 2 * gap := by
    nlinarith [square.frame.unit, gap_sq,
      sq_nonneg (square.frame.cosine - square.frame.sine)]
  have diagonal_projection_upper :
      gap * (square.frame.cosine + square.frame.sine) ≤ 1 := by
    have scaled := mul_le_mul_of_nonneg_left component_sum_upper
      gap_positive.le
    nlinarith [gap_sq]
  have horizontal_projection_upper :
      gap * square.frame.cosine < 1 := by
    have := mul_le_mul_of_nonneg_left cosine_at_most_one gap_positive.le
    linarith
  have vertical_projection_upper :
      gap * square.frame.sine < 1 := by
    have := mul_le_mul_of_nonneg_left sine_at_most_one gap_positive.le
    linarith
  have bottom_left_x_nonpositive : bottomLeftLocalX ≤ 0 := by
    dsimp [bottomLeftLocalX]
    have horizontal_product_nonnegative :
        0 ≤ horizontalOffset * square.frame.cosine := by positivity
    have vertical_product_nonnegative :
        0 ≤ verticalOffset * square.frame.sine := by positivity
    linarith
  have bottom_right_y_nonpositive : bottomRightLocalY ≤ 0 := by
    dsimp [bottomRightLocalY]
    have remaining_horizontal_nonnegative : 0 ≤ gap - horizontalOffset := by
      linarith
    have horizontal_product_nonnegative :
        0 ≤ (gap - horizontalOffset) * square.frame.sine := by positivity
    have vertical_product_nonnegative :
        0 ≤ verticalOffset * square.frame.cosine := by positivity
    linarith
  have top_right_x_nonnegative : 0 ≤ topRightLocalX := by
    dsimp [topRightLocalX]
    have remaining_horizontal_nonnegative : 0 ≤ gap - horizontalOffset := by
      linarith
    have remaining_vertical_nonnegative : 0 ≤ gap - verticalOffset := by
      linarith
    positivity
  have bottom_left_local_x_eq :
      square.localX ⟨1, 1⟩ = bottomLeftLocalX := by
    dsimp [PlacedSquare.localX, bottomLeftLocalX, horizontalOffset,
      verticalOffset]
    ring
  have bottom_left_local_y_eq :
      square.localY ⟨1, 1⟩ = bottomLeftLocalY := by
    dsimp [PlacedSquare.localY, bottomLeftLocalY, horizontalOffset,
      verticalOffset]
    ring
  have bottom_right_local_x_eq :
      square.localX ⟨1 + gap, 1⟩ = bottomRightLocalX := by
    dsimp [PlacedSquare.localX, bottomRightLocalX, horizontalOffset,
      verticalOffset]
    ring
  have bottom_right_local_y_eq :
      square.localY ⟨1 + gap, 1⟩ = bottomRightLocalY := by
    dsimp [PlacedSquare.localY, bottomRightLocalY, horizontalOffset,
      verticalOffset]
    ring
  have top_right_local_x_eq :
      square.localX ⟨1 + gap, 1 + gap⟩ = topRightLocalX := by
    dsimp [PlacedSquare.localX, topRightLocalX, horizontalOffset,
      verticalOffset]
    ring
  have top_right_local_y_eq :
      square.localY ⟨1 + gap, 1 + gap⟩ = topRightLocalY := by
    dsimp [PlacedSquare.localY, topRightLocalY, horizontalOffset,
      verticalOffset]
    ring
  by_contra no_vertex
  push Not at no_vertex
  have bottom_left_miss :
      bottomLeftLocalX < -1 / 2 ∨
        bottomLeftLocalY < -1 / 2 ∨ 1 / 2 < bottomLeftLocalY := by
    by_contra coordinates_inside
    push Not at coordinates_inside
    apply no_vertex.1
    rw [square.contains_iff_localCoordinates, bottom_left_local_x_eq,
      bottom_left_local_y_eq]
    exact ⟨abs_le.mpr ⟨by linarith, by linarith⟩,
      abs_le.mpr ⟨by linarith [coordinates_inside.2.1],
        coordinates_inside.2.2⟩⟩
  have bottom_right_miss :
      bottomRightLocalX < -1 / 2 ∨ 1 / 2 < bottomRightLocalX ∨
        bottomRightLocalY < -1 / 2 := by
    by_contra coordinates_inside
    push Not at coordinates_inside
    apply no_vertex.2.1
    rw [square.contains_iff_localCoordinates, bottom_right_local_x_eq,
      bottom_right_local_y_eq]
    exact ⟨abs_le.mpr ⟨by linarith [coordinates_inside.1],
        coordinates_inside.2.1⟩,
      abs_le.mpr ⟨by linarith [coordinates_inside.2.2],
        by linarith⟩⟩
  have top_right_miss :
      1 / 2 < topRightLocalX ∨ topRightLocalY < -1 / 2 ∨
        1 / 2 < topRightLocalY := by
    by_contra coordinates_inside
    push Not at coordinates_inside
    apply no_vertex.2.2
    rw [square.contains_iff_localCoordinates, top_right_local_x_eq,
      top_right_local_y_eq]
    exact ⟨abs_le.mpr ⟨by linarith, coordinates_inside.1⟩,
      abs_le.mpr ⟨by linarith [coordinates_inside.2.1],
        coordinates_inside.2.2⟩⟩
  rcases bottom_left_miss with bottom_left_x_low |
      bottom_left_y_low | bottom_left_y_high <;>
    rcases bottom_right_miss with bottom_right_x_low |
      bottom_right_x_high | bottom_right_y_low <;>
    rcases top_right_miss with top_right_x_high |
      top_right_y_low | top_right_y_high
  all_goals
    dsimp [bottomLeftLocalX, bottomLeftLocalY, bottomRightLocalX,
      bottomRightLocalY, topRightLocalX, topRightLocalY] at *
    nlinarith

lemma PlacedSquare.contains_lowerRightTriangle
    {square : PlacedSquare} {gap : ℝ}
    (gap_positive : 0 < gap)
    (gap_sq : gap ^ 2 = 1 / 2)
    (center_x_lower : 1 ≤ square.center.x)
    (center_x_upper : square.center.x ≤ 1 + gap)
    (center_y_lower : 1 ≤ square.center.y)
    (center_y_below_diagonal : square.center.y ≤ square.center.x) :
    square.Contains ⟨1, 1⟩ ∨
      square.Contains ⟨1 + gap, 1⟩ ∨
        square.Contains ⟨1 + gap, 1 + gap⟩ := by
  have normalized_result :=
    square.firstQuadrant.contains_lowerRightTriangle_of_nonnegative_frame
      gap_positive gap_sq square.firstQuadrant_cosine_nonnegative
      square.firstQuadrant_sine_nonnegative
      (by simpa using center_x_lower)
      (by simpa using center_x_upper)
      (by simpa using center_y_lower)
      (by simpa using center_y_below_diagonal)
  simpa using normalized_result

lemma PlacedSquare.contains_upperLeftTriangle
    {square : PlacedSquare} {gap : ℝ}
    (gap_positive : 0 < gap)
    (gap_sq : gap ^ 2 = 1 / 2)
    (center_x_lower : 1 ≤ square.center.x)
    (center_y_lower : 1 ≤ square.center.y)
    (center_y_upper : square.center.y ≤ 1 + gap)
    (center_x_below_diagonal : square.center.x ≤ square.center.y) :
    square.Contains ⟨1, 1⟩ ∨
      square.Contains ⟨1, 1 + gap⟩ ∨
        square.Contains ⟨1 + gap, 1 + gap⟩ := by
  have swapped_result := square.swap.contains_lowerRightTriangle
    gap_positive gap_sq
    (by simpa [PlacedSquare.swap, Point.swap] using center_y_lower)
    (by simpa [PlacedSquare.swap, Point.swap] using center_y_upper)
    (by simpa [PlacedSquare.swap, Point.swap] using center_x_lower)
    (by simpa [PlacedSquare.swap, Point.swap] using center_x_below_diagonal)
  rcases swapped_result with bottom_left_mem | bottom_right_mem | top_right_mem
  · exact Or.inl ((square.swap_contains_iff ⟨1, 1⟩).1
      (by simpa [Point.swap] using bottom_left_mem))
  · exact Or.inr (Or.inl ((square.swap_contains_iff ⟨1, 1 + gap⟩).1
      (by simpa [Point.swap] using bottom_right_mem)))
  · exact Or.inr (Or.inr ((square.swap_contains_iff
      ⟨1 + gap, 1 + gap⟩).1 (by simpa [Point.swap] using top_right_mem)))

lemma PlacedSquare.contains_bottomRightCorner
    {square : PlacedSquare} {gap : ℝ}
    (fits : square.Fits (2 + gap))
    (center_x_lower : 1 + gap ≤ square.center.x)
    (center_y_upper : square.center.y ≤ 1) :
    square.Contains ⟨1 + gap, 1⟩ := by
  have reflected_mem := (square.reflectX (2 + gap)).contains_unitCorner
    ((square.reflectX_fits_iff (2 + gap)).2 fits)
    (by simp [PlacedSquare.reflectX, Point.reflectX]; linarith)
    (by simpa [PlacedSquare.reflectX, Point.reflectX] using center_y_upper)
  exact (square.reflectX_contains_iff (2 + gap) ⟨1 + gap, 1⟩).1 (by
    convert reflected_mem using 1
    all_goals norm_num [Point.reflectX])

lemma PlacedSquare.contains_topLeftCorner
    {square : PlacedSquare} {gap : ℝ}
    (fits : square.Fits (2 + gap))
    (center_x_upper : square.center.x ≤ 1)
    (center_y_lower : 1 + gap ≤ square.center.y) :
    square.Contains ⟨1, 1 + gap⟩ := by
  have reflected_mem := (square.reflectY (2 + gap)).contains_unitCorner
    ((square.reflectY_fits_iff (2 + gap)).2 fits)
    (by simpa [PlacedSquare.reflectY, Point.reflectY] using center_x_upper)
    (by simp [PlacedSquare.reflectY, Point.reflectY]; linarith)
  exact (square.reflectY_contains_iff (2 + gap) ⟨1, 1 + gap⟩).1 (by
    convert reflected_mem using 1
    all_goals norm_num [Point.reflectY])

lemma PlacedSquare.contains_topRightCorner
    {square : PlacedSquare} {gap : ℝ}
    (fits : square.Fits (2 + gap))
    (center_x_lower : 1 + gap ≤ square.center.x)
    (center_y_lower : 1 + gap ≤ square.center.y) :
    square.Contains ⟨1 + gap, 1 + gap⟩ := by
  have reflected_mem := (square.reflectX (2 + gap)).contains_topLeftCorner
    ((square.reflectX_fits_iff (2 + gap)).2 fits)
    (by simp [PlacedSquare.reflectX, Point.reflectX]; linarith)
    (by simpa [PlacedSquare.reflectX, Point.reflectX] using center_y_lower)
  exact (square.reflectX_contains_iff (2 + gap)
    ⟨1 + gap, 1 + gap⟩).1 (by
      convert reflected_mem using 1
      all_goals norm_num [Point.reflectX])

lemma PlacedSquare.contains_bottomBoundaryPair
    {square : PlacedSquare} {side left gap : ℝ}
    (fits : square.Fits side)
    (gap_positive : 0 < gap)
    (gap_upper : gap ≤ 4 / 5)
    (center_x_lower : left ≤ square.center.x)
    (center_x_upper : square.center.x ≤ left + gap)
    (center_y_upper : square.center.y ≤ 1) :
    square.Contains ⟨left, 1⟩ ∨ square.Contains ⟨left + gap, 1⟩ := by
  apply square.contains_bottomPairWith fits (by norm_num)
    gap_positive (by linarith)
  · intro frame cosine_nonnegative sine_nonnegative
    exact frame.height_add_gap_product_le_sum_of_gap_le_four_fifths
      cosine_nonnegative sine_nonnegative (by norm_num) gap_upper
  · exact center_x_lower
  · exact center_x_upper
  · exact center_y_upper

end SquarePackingArchive
