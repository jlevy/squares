import SquarePackingArchive.Geometry

namespace SquarePackingArchive

private def RightRegion (horizontal vertical : ℝ) : Prop :=
  vertical ≤ horizontal ∧ -horizontal ≤ vertical

private def LeftRegion (horizontal vertical : ℝ) : Prop :=
  horizontal ≤ vertical ∧ vertical ≤ -horizontal

private def TopRegion (horizontal vertical : ℝ) : Prop :=
  horizontal ≤ vertical ∧ -vertical ≤ horizontal

private def BottomRegion (horizontal vertical : ℝ) : Prop :=
  vertical ≤ horizontal ∧ horizontal ≤ -vertical

private lemma weighted_not_all_positive
    {first second third firstWeight secondWeight thirdWeight : ℝ}
    (first_weight_nonnegative : 0 ≤ firstWeight)
    (second_weight_nonnegative : 0 ≤ secondWeight)
    (third_weight_nonnegative : 0 ≤ thirdWeight)
    (weight_sum : firstWeight + secondWeight + thirdWeight = 1)
    (balance : firstWeight * first + secondWeight * second + thirdWeight * third = 0) :
    ¬ (0 < first ∧ 0 < second ∧ 0 < third) := by
  rintro ⟨first_positive, second_positive, third_positive⟩
  have first_product_nonnegative : 0 ≤ firstWeight * first :=
    mul_nonneg first_weight_nonnegative first_positive.le
  have second_product_nonnegative : 0 ≤ secondWeight * second :=
    mul_nonneg second_weight_nonnegative second_positive.le
  have third_product_nonnegative : 0 ≤ thirdWeight * third :=
    mul_nonneg third_weight_nonnegative third_positive.le
  have a_weight_positive : 0 < firstWeight ∨ 0 < secondWeight ∨ 0 < thirdWeight := by
    rcases eq_or_lt_of_le first_weight_nonnegative with first_zero | first_positive
    · rcases eq_or_lt_of_le second_weight_nonnegative with second_zero | second_positive
      · right
        right
        linarith
      · exact Or.inr (Or.inl second_positive)
    · exact Or.inl first_positive
  rcases a_weight_positive with first_weight_positive |
      second_weight_positive | third_weight_positive
  · have := mul_pos first_weight_positive first_positive
    linarith
  · have := mul_pos second_weight_positive second_positive
    linarith
  · have := mul_pos third_weight_positive third_positive
    linarith

private lemma opposite_regions_of_weighted_center
    {firstX firstY secondX secondY thirdX thirdY
      firstWeight secondWeight thirdWeight : ℝ}
    (first_weight_nonnegative : 0 ≤ firstWeight)
    (second_weight_nonnegative : 0 ≤ secondWeight)
    (third_weight_nonnegative : 0 ≤ thirdWeight)
    (weight_sum : firstWeight + secondWeight + thirdWeight = 1)
    (horizontal_balance :
      firstWeight * firstX + secondWeight * secondX + thirdWeight * thirdX = 0)
    (vertical_balance :
      firstWeight * firstY + secondWeight * secondY + thirdWeight * thirdY = 0) :
    ((RightRegion firstX firstY ∨ RightRegion secondX secondY ∨ RightRegion thirdX thirdY) ∧
      (LeftRegion firstX firstY ∨ LeftRegion secondX secondY ∨ LeftRegion thirdX thirdY)) ∨
    ((TopRegion firstX firstY ∨ TopRegion secondX secondY ∨ TopRegion thirdX thirdY) ∧
      (BottomRegion firstX firstY ∨ BottomRegion secondX secondY ∨ BottomRegion thirdX thirdY)) := by
  by_contra no_opposite_regions
  have no_horizontal_opposites :
      ¬ (RightRegion firstX firstY ∨ RightRegion secondX secondY ∨
        RightRegion thirdX thirdY) ∨
      ¬ (LeftRegion firstX firstY ∨ LeftRegion secondX secondY ∨
        LeftRegion thirdX thirdY) := by
    by_cases has_right : RightRegion firstX firstY ∨ RightRegion secondX secondY ∨
        RightRegion thirdX thirdY
    · exact Or.inr (by
        intro has_left
        exact no_opposite_regions (Or.inl ⟨has_right, has_left⟩))
    · exact Or.inl has_right
  have no_vertical_opposites :
      ¬ (TopRegion firstX firstY ∨ TopRegion secondX secondY ∨
        TopRegion thirdX thirdY) ∨
      ¬ (BottomRegion firstX firstY ∨ BottomRegion secondX secondY ∨
        BottomRegion thirdX thirdY) := by
    by_cases has_top : TopRegion firstX firstY ∨ TopRegion secondX secondY ∨
        TopRegion thirdX thirdY
    · exact Or.inr (by
        intro has_bottom
        exact no_opposite_regions (Or.inr ⟨has_top, has_bottom⟩))
    · exact Or.inl has_top
  rcases no_horizontal_opposites with no_right | no_left <;>
    rcases no_vertical_opposites with no_top | no_bottom
  · apply weighted_not_all_positive first_weight_nonnegative second_weight_nonnegative
      third_weight_nonnegative weight_sum
      (first := -(firstX + firstY)) (second := -(secondX + secondY))
      (third := -(thirdX + thirdY)) (by nlinarith)
    push Not at no_right no_top
    constructor
    · by_contra
      rcases le_total firstX firstY with first_x_le_y | first_y_le_x
      · exact no_top.1 ⟨first_x_le_y, by linarith⟩
      · exact no_right.1 ⟨first_y_le_x, by linarith⟩
    constructor
    · by_contra
      rcases le_total secondX secondY with second_x_le_y | second_y_le_x
      · exact no_top.2.1 ⟨second_x_le_y, by linarith⟩
      · exact no_right.2.1 ⟨second_y_le_x, by linarith⟩
    · by_contra
      rcases le_total thirdX thirdY with third_x_le_y | third_y_le_x
      · exact no_top.2.2 ⟨third_x_le_y, by linarith⟩
      · exact no_right.2.2 ⟨third_y_le_x, by linarith⟩
  · apply weighted_not_all_positive first_weight_nonnegative second_weight_nonnegative
      third_weight_nonnegative weight_sum
      (first := -(firstX - firstY)) (second := -(secondX - secondY))
      (third := -(thirdX - thirdY)) (by nlinarith)
    push Not at no_right no_bottom
    constructor
    · by_contra
      rcases le_total firstX (-firstY) with first_x_le | first_neg_y_le
      · exact no_bottom.1 ⟨by linarith, first_x_le⟩
      · exact no_right.1 ⟨by linarith, by linarith⟩
    constructor
    · by_contra
      rcases le_total secondX (-secondY) with second_x_le | second_neg_y_le
      · exact no_bottom.2.1 ⟨by linarith, second_x_le⟩
      · exact no_right.2.1 ⟨by linarith, by linarith⟩
    · by_contra
      rcases le_total thirdX (-thirdY) with third_x_le | third_neg_y_le
      · exact no_bottom.2.2 ⟨by linarith, third_x_le⟩
      · exact no_right.2.2 ⟨by linarith, by linarith⟩
  · apply weighted_not_all_positive first_weight_nonnegative second_weight_nonnegative
      third_weight_nonnegative weight_sum
      (first := firstX - firstY) (second := secondX - secondY)
      (third := thirdX - thirdY) (by nlinarith)
    push Not at no_left no_top
    constructor
    · by_contra
      rcases le_total firstY (-firstX) with first_y_le | first_neg_x_le
      · exact no_left.1 ⟨by linarith, first_y_le⟩
      · exact no_top.1 ⟨by linarith, by linarith⟩
    constructor
    · by_contra
      rcases le_total secondY (-secondX) with second_y_le | second_neg_x_le
      · exact no_left.2.1 ⟨by linarith, second_y_le⟩
      · exact no_top.2.1 ⟨by linarith, by linarith⟩
    · by_contra
      rcases le_total thirdY (-thirdX) with third_y_le | third_neg_x_le
      · exact no_left.2.2 ⟨by linarith, third_y_le⟩
      · exact no_top.2.2 ⟨by linarith, by linarith⟩
  · apply weighted_not_all_positive first_weight_nonnegative second_weight_nonnegative
      third_weight_nonnegative weight_sum
      (first := firstX + firstY) (second := secondX + secondY)
      (third := thirdX + thirdY) (by nlinarith)
    push Not at no_left no_bottom
    constructor
    · by_contra
      rcases le_total firstY firstX with first_y_le_x | first_x_le_y
      · exact no_bottom.1 ⟨first_y_le_x, by linarith⟩
      · exact no_left.1 ⟨first_x_le_y, by linarith⟩
    constructor
    · by_contra
      rcases le_total secondY secondX with second_y_le_x | second_x_le_y
      · exact no_bottom.2.1 ⟨second_y_le_x, by linarith⟩
      · exact no_left.2.1 ⟨second_x_le_y, by linarith⟩
    · by_contra
      rcases le_total thirdY thirdX with third_y_le_x | third_x_le_y
      · exact no_bottom.2.2 ⟨third_y_le_x, by linarith⟩
      · exact no_left.2.2 ⟨third_x_le_y, by linarith⟩

private lemma horizontal_high_of_right
    {horizontal vertical : ℝ}
    (outside : ¬ (|horizontal| ≤ 1 / 2 ∧ |vertical| ≤ 1 / 2))
    (right : RightRegion horizontal vertical) :
    1 / 2 < horizontal := by
  by_contra horizontal_not_high
  apply outside
  rw [abs_le, abs_le]
  constructor <;> constructor <;> dsimp [RightRegion] at right <;> linarith

private lemma horizontal_low_of_left
    {horizontal vertical : ℝ}
    (outside : ¬ (|horizontal| ≤ 1 / 2 ∧ |vertical| ≤ 1 / 2))
    (left : LeftRegion horizontal vertical) :
    horizontal < -1 / 2 := by
  by_contra horizontal_not_low
  apply outside
  rw [abs_le, abs_le]
  constructor <;> constructor <;> dsimp [LeftRegion] at left <;> linarith

private lemma vertical_high_of_top
    {horizontal vertical : ℝ}
    (outside : ¬ (|horizontal| ≤ 1 / 2 ∧ |vertical| ≤ 1 / 2))
    (top : TopRegion horizontal vertical) :
    1 / 2 < vertical := by
  by_contra vertical_not_high
  apply outside
  rw [abs_le, abs_le]
  constructor <;> constructor <;> dsimp [TopRegion] at top <;> linarith

private lemma vertical_low_of_bottom
    {horizontal vertical : ℝ}
    (outside : ¬ (|horizontal| ≤ 1 / 2 ∧ |vertical| ≤ 1 / 2))
    (bottom : BottomRegion horizontal vertical) :
    vertical < -1 / 2 := by
  by_contra vertical_not_low
  apply outside
  rw [abs_le, abs_le]
  constructor <;> constructor <;> dsimp [BottomRegion] at bottom <;> linarith

set_option maxHeartbeats 2000000 in
lemma triangle_coordinate_core
    {firstX firstY secondX secondY thirdX thirdY
      firstWeight secondWeight thirdWeight : ℝ}
    (first_weight_nonnegative : 0 ≤ firstWeight)
    (second_weight_nonnegative : 0 ≤ secondWeight)
    (third_weight_nonnegative : 0 ≤ thirdWeight)
    (weight_sum : firstWeight + secondWeight + thirdWeight = 1)
    (horizontal_balance :
      firstWeight * firstX + secondWeight * secondX + thirdWeight * thirdX = 0)
    (vertical_balance :
      firstWeight * firstY + secondWeight * secondY + thirdWeight * thirdY = 0)
    (first_second_distance :
      (firstX - secondX) ^ 2 + (firstY - secondY) ^ 2 ≤ 1)
    (first_third_distance :
      (firstX - thirdX) ^ 2 + (firstY - thirdY) ^ 2 ≤ 1)
    (second_third_distance :
      (secondX - thirdX) ^ 2 + (secondY - thirdY) ^ 2 ≤ 1) :
    (|firstX| ≤ 1 / 2 ∧ |firstY| ≤ 1 / 2) ∨
      (|secondX| ≤ 1 / 2 ∧ |secondY| ≤ 1 / 2) ∨
        (|thirdX| ≤ 1 / 2 ∧ |thirdY| ≤ 1 / 2) := by
  by_contra no_vertex
  have first_outside : ¬ (|firstX| ≤ 1 / 2 ∧ |firstY| ≤ 1 / 2) := by
    intro inside
    exact no_vertex (Or.inl inside)
  have second_outside : ¬ (|secondX| ≤ 1 / 2 ∧ |secondY| ≤ 1 / 2) := by
    intro inside
    exact no_vertex (Or.inr (Or.inl inside))
  have third_outside : ¬ (|thirdX| ≤ 1 / 2 ∧ |thirdY| ≤ 1 / 2) := by
    intro inside
    exact no_vertex (Or.inr (Or.inr inside))
  have opposite_regions := opposite_regions_of_weighted_center
    first_weight_nonnegative second_weight_nonnegative third_weight_nonnegative
    weight_sum horizontal_balance vertical_balance
  rcases opposite_regions with ⟨right, left⟩ | ⟨top, bottom⟩
  · have right_high : 1 / 2 < firstX ∨ 1 / 2 < secondX ∨ 1 / 2 < thirdX := by
      rcases right with first_right | second_right | third_right
      · exact Or.inl (horizontal_high_of_right first_outside first_right)
      · exact Or.inr (Or.inl (horizontal_high_of_right second_outside second_right))
      · exact Or.inr (Or.inr (horizontal_high_of_right third_outside third_right))
    have left_low : firstX < -1 / 2 ∨ secondX < -1 / 2 ∨ thirdX < -1 / 2 := by
      rcases left with first_left | second_left | third_left
      · exact Or.inl (horizontal_low_of_left first_outside first_left)
      · exact Or.inr (Or.inl (horizontal_low_of_left second_outside second_left))
      · exact Or.inr (Or.inr (horizontal_low_of_left third_outside third_left))
    rcases right_high with first_high | second_high | third_high <;>
      rcases left_low with first_low | second_low | third_low <;>
      nlinarith
  · have top_high : 1 / 2 < firstY ∨ 1 / 2 < secondY ∨ 1 / 2 < thirdY := by
      rcases top with first_top | second_top | third_top
      · exact Or.inl (vertical_high_of_top first_outside first_top)
      · exact Or.inr (Or.inl (vertical_high_of_top second_outside second_top))
      · exact Or.inr (Or.inr (vertical_high_of_top third_outside third_top))
    have bottom_low : firstY < -1 / 2 ∨ secondY < -1 / 2 ∨ thirdY < -1 / 2 := by
      rcases bottom with first_bottom | second_bottom | third_bottom
      · exact Or.inl (vertical_low_of_bottom first_outside first_bottom)
      · exact Or.inr (Or.inl (vertical_low_of_bottom second_outside second_bottom))
      · exact Or.inr (Or.inr (vertical_low_of_bottom third_outside third_bottom))
    rcases top_high with first_high | second_high | third_high <;>
      rcases bottom_low with first_low | second_low | third_low <;>
      nlinarith

lemma PlacedSquare.local_coordinate_distance_sq
    (square : PlacedSquare) (first second : Point) :
    (square.localX first - square.localX second) ^ 2 +
        (square.localY first - square.localY second) ^ 2 =
      (first.x - second.x) ^ 2 + (first.y - second.y) ^ 2 := by
  dsimp [PlacedSquare.localX, PlacedSquare.localY]
  nlinarith [square.frame.unit]

lemma PlacedSquare.contains_triangleVertex
    (square : PlacedSquare) (first second third : Point)
    (firstWeight secondWeight thirdWeight : ℝ)
    (first_weight_nonnegative : 0 ≤ firstWeight)
    (second_weight_nonnegative : 0 ≤ secondWeight)
    (third_weight_nonnegative : 0 ≤ thirdWeight)
    (weight_sum : firstWeight + secondWeight + thirdWeight = 1)
    (center_x_eq : square.center.x =
      firstWeight * first.x + secondWeight * second.x + thirdWeight * third.x)
    (center_y_eq : square.center.y =
      firstWeight * first.y + secondWeight * second.y + thirdWeight * third.y)
    (first_second_distance :
      (first.x - second.x) ^ 2 + (first.y - second.y) ^ 2 ≤ 1)
    (first_third_distance :
      (first.x - third.x) ^ 2 + (first.y - third.y) ^ 2 ≤ 1)
    (second_third_distance :
      (second.x - third.x) ^ 2 + (second.y - third.y) ^ 2 ≤ 1) :
    square.Contains first ∨ square.Contains second ∨ square.Contains third := by
  have horizontal_balance :
      firstWeight * square.localX first +
          secondWeight * square.localX second +
          thirdWeight * square.localX third = 0 := by
    dsimp [PlacedSquare.localX]
    calc
      _ = (firstWeight * first.x + secondWeight * second.x + thirdWeight * third.x -
            (firstWeight + secondWeight + thirdWeight) * square.center.x) *
            square.frame.cosine +
          (firstWeight * first.y + secondWeight * second.y + thirdWeight * third.y -
            (firstWeight + secondWeight + thirdWeight) * square.center.y) *
            square.frame.sine := by ring
      _ = 0 := by rw [weight_sum, ← center_x_eq, ← center_y_eq]; ring
  have vertical_balance :
      firstWeight * square.localY first +
          secondWeight * square.localY second +
          thirdWeight * square.localY third = 0 := by
    dsimp [PlacedSquare.localY]
    calc
      _ = -(firstWeight * first.x + secondWeight * second.x + thirdWeight * third.x -
            (firstWeight + secondWeight + thirdWeight) * square.center.x) *
            square.frame.sine +
          (firstWeight * first.y + secondWeight * second.y + thirdWeight * third.y -
            (firstWeight + secondWeight + thirdWeight) * square.center.y) *
            square.frame.cosine := by ring
      _ = 0 := by rw [weight_sum, ← center_x_eq, ← center_y_eq]; ring
  have local_first_second_distance :
      (square.localX first - square.localX second) ^ 2 +
          (square.localY first - square.localY second) ^ 2 ≤ 1 := by
    rw [square.local_coordinate_distance_sq]
    exact first_second_distance
  have local_first_third_distance :
      (square.localX first - square.localX third) ^ 2 +
          (square.localY first - square.localY third) ^ 2 ≤ 1 := by
    rw [square.local_coordinate_distance_sq]
    exact first_third_distance
  have local_second_third_distance :
      (square.localX second - square.localX third) ^ 2 +
          (square.localY second - square.localY third) ^ 2 ≤ 1 := by
    rw [square.local_coordinate_distance_sq]
    exact second_third_distance
  have local_result := triangle_coordinate_core
    first_weight_nonnegative second_weight_nonnegative third_weight_nonnegative
    weight_sum horizontal_balance vertical_balance local_first_second_distance
    local_first_third_distance local_second_third_distance
  simpa only [square.contains_iff_localCoordinates] using local_result

end SquarePackingArchive
