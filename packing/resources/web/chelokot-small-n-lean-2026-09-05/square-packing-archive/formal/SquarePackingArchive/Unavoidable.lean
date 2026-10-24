import Mathlib.Data.Fintype.Pigeonhole
import SquarePackingArchive.Area

namespace SquarePackingArchive

def InteriorUnavoidable
    {pointCount : ℕ} (points : Fin pointCount → Point) (side : ℝ) : Prop :=
  ∀ square : PlacedSquare, square.Fits side →
    ∃ index, square.InteriorContains (points index)

def Unavoidable
    {pointCount : ℕ} (points : Fin pointCount → Point) (side : ℝ) : Prop :=
  ∀ square : PlacedSquare, square.Fits side →
    ∃ index, square.Contains (points index)

def Point.scale (factor : ℝ) (point : Point) : Point :=
  ⟨factor * point.x, factor * point.y⟩

def PlacedSquare.scaleCenter
    (factor : ℝ) (square : PlacedSquare) : PlacedSquare where
  center := square.center.scale factor
  frame := square.frame

@[simp] lemma Point.scale_x (factor : ℝ) (point : Point) :
    (point.scale factor).x = factor * point.x := rfl

@[simp] lemma Point.scale_y (factor : ℝ) (point : Point) :
    (point.scale factor).y = factor * point.y := rfl

lemma PlacedSquare.scaleCenter_point
    (square : PlacedSquare) (factor localX localY : ℝ) :
    (square.scaleCenter factor).point (factor * localX) (factor * localY) =
      (square.point localX localY).scale factor := by
  rw [Point.mk.injEq]
  constructor <;>
    simp [PlacedSquare.scaleCenter, PlacedSquare.point, Point.scale,
      Frame.place] <;>
    ring

lemma PlacedSquare.scaleCenter_fits
    {square : PlacedSquare} {side factor : ℝ}
    (fits : square.Fits side)
    (factor_at_least_one : 1 ≤ factor) :
    (square.scaleCenter factor).Fits (factor * side) := by
  have factor_positive : 0 < factor := zero_lt_one.trans_le factor_at_least_one
  intro point point_mem
  rcases point_mem with ⟨localX, localY, localX_le, localY_le, rfl⟩
  have scaled_localX_le : |localX / factor| ≤ 1 / 2 := by
    rw [abs_div, abs_of_pos factor_positive]
    exact (div_le_iff₀ factor_positive).2 (by
      nlinarith [localX_le])
  have scaled_localY_le : |localY / factor| ≤ 1 / 2 := by
    rw [abs_div, abs_of_pos factor_positive]
    exact (div_le_iff₀ factor_positive).2 (by
      nlinarith [localY_le])
  have source_point_mem :
      square.Contains (square.point (localX / factor) (localY / factor)) :=
    ⟨localX / factor, localY / factor, scaled_localX_le, scaled_localY_le, rfl⟩
  have source_bounds := fits source_point_mem
  have point_identity :
      (square.scaleCenter factor).point localX localY =
        (square.point (localX / factor) (localY / factor)).scale factor := by
    convert square.scaleCenter_point factor (localX / factor) (localY / factor) using 1
    all_goals field_simp
  rw [point_identity]
  exact ⟨mul_nonneg factor_positive.le source_bounds.1,
    (mul_le_mul_of_nonneg_left source_bounds.2.1 factor_positive.le),
    mul_nonneg factor_positive.le source_bounds.2.2.1,
    (mul_le_mul_of_nonneg_left source_bounds.2.2.2 factor_positive.le)⟩

lemma PlacedSquare.interiorContains_scaled_of_scaleCenter_contains
    {square : PlacedSquare} {factor : ℝ} {point : Point}
    (factor_gt_one : 1 < factor)
    (point_mem : (square.scaleCenter factor).Contains point) :
    square.InteriorContains (point.scale (1 / factor)) := by
  have factor_positive : 0 < factor := zero_lt_one.trans factor_gt_one
  rcases point_mem with
    ⟨localX, localY, localX_le, localY_le, point_eq⟩
  refine ⟨localX / factor, localY / factor, ?_, ?_, ?_⟩
  · rw [abs_div, abs_of_pos factor_positive]
    exact (div_lt_iff₀ factor_positive).2 (by
      nlinarith [localX_le])
  · rw [abs_div, abs_of_pos factor_positive]
    exact (div_lt_iff₀ factor_positive).2 (by
      nlinarith [localY_le])
  · subst point
    rw [Point.mk.injEq]
    constructor <;>
      simp [PlacedSquare.scaleCenter, PlacedSquare.point, Point.scale,
        Frame.place] <;>
      field_simp

theorem Unavoidable.interior_scaled
    {pointCount : ℕ} {points : Fin pointCount → Point}
    {side factor : ℝ}
    (unavoidable : Unavoidable points (factor * side))
    (factor_gt_one : 1 < factor) :
    InteriorUnavoidable
      (fun index => (points index).scale (1 / factor)) side := by
  intro square fits
  have scaled_fits := square.scaleCenter_fits fits factor_gt_one.le
  obtain ⟨index, point_mem⟩ := unavoidable
    (square.scaleCenter factor) scaled_fits
  exact ⟨index,
    square.interiorContains_scaled_of_scaleCenter_contains
      factor_gt_one point_mem⟩

lemma PlacedSquare.contains_cornerPoint_of_nonnegative_frame
    {square : PlacedSquare} {side targetX targetY : ℝ}
    (fits : square.Fits side)
    (cosine_nonnegative : 0 ≤ square.frame.cosine)
    (sine_nonnegative : 0 ≤ square.frame.sine)
    (target_x_upper : targetX ≤ 1)
    (target_y_upper : targetY ≤ 1)
    (center_x_upper : square.center.x ≤ targetX)
    (center_y_upper : square.center.y ≤ targetY) :
    square.Contains ⟨targetX, targetY⟩ := by
  have lower_x_corner := fits (point := square.point (-1 / 2) (1 / 2))
    ⟨-1 / 2, 1 / 2, by norm_num, by norm_num, rfl⟩
  have lower_y_corner := fits (point := square.point (-1 / 2) (-1 / 2))
    ⟨-1 / 2, -1 / 2, by norm_num, by norm_num, rfl⟩
  have center_x_lower :
      (square.frame.cosine + square.frame.sine) / 2 ≤ square.center.x := by
    have := lower_x_corner.1
    simp [PlacedSquare.point, Frame.place] at this
    linarith
  have center_y_lower :
      (square.frame.cosine + square.frame.sine) / 2 ≤ square.center.y := by
    have := lower_y_corner.2.2.1
    simp [PlacedSquare.point, Frame.place] at this
    linarith
  let horizontalDelta := targetX - square.center.x
  let verticalDelta := targetY - square.center.y
  let localX :=
    horizontalDelta * square.frame.cosine +
      verticalDelta * square.frame.sine
  let localY :=
    -horizontalDelta * square.frame.sine +
      verticalDelta * square.frame.cosine
  have horizontal_delta_nonnegative : 0 ≤ horizontalDelta := by
    dsimp [horizontalDelta]
    linarith
  have vertical_delta_nonnegative : 0 ≤ verticalDelta := by
    dsimp [verticalDelta]
    linarith
  have horizontal_delta_upper :
      horizontalDelta ≤
        1 - (square.frame.cosine + square.frame.sine) / 2 := by
    dsimp [horizontalDelta]
    linarith
  have vertical_delta_upper :
      verticalDelta ≤
        1 - (square.frame.cosine + square.frame.sine) / 2 := by
    dsimp [verticalDelta]
    linarith
  have component_product_nonnegative :
      0 ≤ square.frame.cosine * square.frame.sine :=
    mul_nonneg cosine_nonnegative sine_nonnegative
  have component_sum_at_least_one :
      1 ≤ square.frame.cosine + square.frame.sine := by
    nlinarith [square.frame.unit]
  have common_upper_at_most_half :
      (1 - (square.frame.cosine + square.frame.sine) / 2) *
          (square.frame.cosine + square.frame.sine) ≤
        1 / 2 := by
    nlinarith [sq_nonneg (square.frame.cosine + square.frame.sine - 1)]
  have localX_nonnegative : 0 ≤ localX := by
    dsimp [localX]
    positivity
  have localX_upper : localX ≤ 1 / 2 := by
    calc
      localX ≤
          (1 - (square.frame.cosine + square.frame.sine) / 2) *
              square.frame.cosine +
            (1 - (square.frame.cosine + square.frame.sine) / 2) *
              square.frame.sine := by
        dsimp [localX]
        exact add_le_add
          (mul_le_mul_of_nonneg_right horizontal_delta_upper
            cosine_nonnegative)
          (mul_le_mul_of_nonneg_right vertical_delta_upper sine_nonnegative)
      _ =
          (1 - (square.frame.cosine + square.frame.sine) / 2) *
            (square.frame.cosine + square.frame.sine) := by ring
      _ ≤ 1 / 2 := common_upper_at_most_half
  have localY_abs_upper : |localY| ≤ 1 / 2 := by
    calc
      |localY| ≤
          |-horizontalDelta * square.frame.sine| +
            |verticalDelta * square.frame.cosine| := by
        exact abs_add_le _ _
      _ =
          horizontalDelta * square.frame.sine +
            verticalDelta * square.frame.cosine := by
        rw [abs_mul, abs_mul, abs_neg,
          abs_of_nonneg horizontal_delta_nonnegative,
          abs_of_nonneg vertical_delta_nonnegative,
          abs_of_nonneg sine_nonnegative,
          abs_of_nonneg cosine_nonnegative]
      _ ≤
          (1 - (square.frame.cosine + square.frame.sine) / 2) *
              square.frame.sine +
            (1 - (square.frame.cosine + square.frame.sine) / 2) *
              square.frame.cosine := by
        exact add_le_add
          (mul_le_mul_of_nonneg_right horizontal_delta_upper sine_nonnegative)
          (mul_le_mul_of_nonneg_right vertical_delta_upper cosine_nonnegative)
      _ =
          (1 - (square.frame.cosine + square.frame.sine) / 2) *
            (square.frame.cosine + square.frame.sine) := by ring
      _ ≤ 1 / 2 := common_upper_at_most_half
  refine ⟨localX, localY, ?_, localY_abs_upper, ?_⟩
  · rw [abs_of_nonneg localX_nonnegative]
    exact localX_upper
  · rw [Point.mk.injEq]
    constructor
    · dsimp [localX, localY, horizontalDelta, verticalDelta,
        PlacedSquare.point, Frame.place]
      linear_combination
        -(targetX - square.center.x) * square.frame.unit
    · dsimp [localX, localY, horizontalDelta, verticalDelta,
        PlacedSquare.point, Frame.place]
      linear_combination
        -(targetY - square.center.y) * square.frame.unit

lemma PlacedSquare.contains_cornerPoint
    {square : PlacedSquare} {side targetX targetY : ℝ}
    (fits : square.Fits side)
    (target_x_upper : targetX ≤ 1)
    (target_y_upper : targetY ≤ 1)
    (center_x_upper : square.center.x ≤ targetX)
    (center_y_upper : square.center.y ≤ targetY) :
    square.Contains ⟨targetX, targetY⟩ := by
  have normalized_contains :=
    square.firstQuadrant.contains_cornerPoint_of_nonnegative_frame
      ((square.firstQuadrant_fits_iff side).2 fits)
      square.firstQuadrant_cosine_nonnegative
      square.firstQuadrant_sine_nonnegative target_x_upper target_y_upper
      (by simpa using center_x_upper)
      (by simpa using center_y_upper)
  exact (square.firstQuadrant_contains_iff ⟨targetX, targetY⟩).1
    normalized_contains

lemma PlacedSquare.contains_unitCorner
    {square : PlacedSquare} {side : ℝ}
    (fits : square.Fits side)
    (center_x_at_most_one : square.center.x ≤ 1)
    (center_y_at_most_one : square.center.y ≤ 1) :
    square.Contains ⟨1, 1⟩ := by
  exact square.contains_cornerPoint fits (by norm_num) (by norm_num)
    center_x_at_most_one center_y_at_most_one

theorem Packing.squareCount_le_of_interiorUnavoidable
    {squareCount pointCount : ℕ} {side : ℝ}
    (packing : Packing squareCount side)
    (points : Fin pointCount → Point)
    (unavoidable : InteriorUnavoidable points side) :
    squareCount ≤ pointCount := by
  by_contra count_too_large
  have point_count_lt_square_count : pointCount < squareCount :=
    Nat.lt_of_not_ge count_too_large
  have covered : ∀ squareIndex,
      ∃ pointIndex,
        (packing.squares squareIndex).InteriorContains (points pointIndex) := by
    intro squareIndex
    exact unavoidable (packing.squares squareIndex) (packing.fits squareIndex)
  let assignedPoint : Fin squareCount → Fin pointCount :=
    fun squareIndex => (covered squareIndex).choose
  have assigned_point_mem : ∀ squareIndex,
      (packing.squares squareIndex).InteriorContains
        (points (assignedPoint squareIndex)) := by
    intro squareIndex
    exact (covered squareIndex).choose_spec
  obtain ⟨left, right, different, same_point⟩ :=
    Fintype.exists_ne_map_eq_of_card_lt assignedPoint (by
      simpa using point_count_lt_square_count)
  apply packing.disjoint left right different
    (points (assignedPoint left))
  exact ⟨assigned_point_mem left, by
    rw [same_point]
    exact assigned_point_mem right⟩

theorem lowerBound_succ_of_interiorUnavoidable_below
    {pointCount : ℕ} {side : ℝ}
    (certificates : ∀ candidateSide, 0 < candidateSide → candidateSide < side →
      ∃ points : Fin pointCount → Point,
        InteriorUnavoidable points candidateSide) :
    IsLowerBound (pointCount + 1) side := by
  intro candidateSide hasPacking
  by_contra candidate_too_small
  have candidate_positive := hasPacking.some.side_positive (by omega)
  obtain ⟨points, unavoidable⟩ := certificates candidateSide candidate_positive
    (lt_of_not_ge candidate_too_small)
  have count_bound := hasPacking.some.squareCount_le_of_interiorUnavoidable
    points unavoidable
  omega

theorem lowerBound_succ_of_unavoidable
    {pointCount : ℕ} {points : Fin pointCount → Point} {side : ℝ}
    (unavoidable : Unavoidable points side) :
    IsLowerBound (pointCount + 1) side := by
  apply lowerBound_succ_of_interiorUnavoidable_below
  intro candidateSide candidate_positive candidate_lt_side
  let factor := side / candidateSide
  have factor_gt_one : 1 < factor := by
    dsimp [factor]
    exact (lt_div_iff₀ candidate_positive).2 (by
      simpa only [one_mul] using candidate_lt_side)
  have scaled_unavoidable :
      Unavoidable points (factor * candidateSide) := by
    simpa [factor, candidate_positive.ne'] using unavoidable
  exact ⟨fun index => (points index).scale (1 / factor),
    scaled_unavoidable.interior_scaled factor_gt_one⟩

end SquarePackingArchive
