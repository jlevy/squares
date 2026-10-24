import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Data.Real.Basic

namespace SquarePackingArchive

structure Point where
  x : ℝ
  y : ℝ

def Point.translate (horizontal vertical : ℝ) (point : Point) : Point :=
  ⟨point.x + horizontal, point.y + vertical⟩

def Point.swap (point : Point) : Point :=
  ⟨point.y, point.x⟩

def Point.reflectX (coordinateSum : ℝ) (point : Point) : Point :=
  ⟨coordinateSum - point.x, point.y⟩

def Point.reflectY (coordinateSum : ℝ) (point : Point) : Point :=
  ⟨point.x, coordinateSum - point.y⟩

@[simp] lemma Point.swap_swap (point : Point) :
    point.swap.swap = point := by
  rfl

lemma Point.swap_injective : Function.Injective Point.swap := by
  intro left right equality
  have := congrArg Point.swap equality
  simpa using this

@[simp] lemma Point.reflectX_reflectX (coordinateSum : ℝ) (point : Point) :
    (point.reflectX coordinateSum).reflectX coordinateSum = point := by
  cases point
  simp [Point.reflectX]

lemma Point.reflectX_injective (coordinateSum : ℝ) :
    Function.Injective (Point.reflectX coordinateSum) := by
  intro left right equality
  have := congrArg (Point.reflectX coordinateSum) equality
  simpa using this

@[simp] lemma Point.reflectY_reflectY (coordinateSum : ℝ) (point : Point) :
    (point.reflectY coordinateSum).reflectY coordinateSum = point := by
  cases point
  simp [Point.reflectY]

lemma Point.reflectY_injective (coordinateSum : ℝ) :
    Function.Injective (Point.reflectY coordinateSum) := by
  intro left right equality
  have := congrArg (Point.reflectY coordinateSum) equality
  simpa using this

structure Frame where
  cosine : ℝ
  sine : ℝ
  unit : cosine ^ 2 + sine ^ 2 = 1

lemma Frame.cosine_le_one (frame : Frame) (cosine_nonnegative : 0 ≤ frame.cosine) :
    frame.cosine ≤ 1 := by
  nlinarith [frame.unit, sq_nonneg frame.sine]

lemma Frame.sine_le_one (frame : Frame) (sine_nonnegative : 0 ≤ frame.sine) :
    frame.sine ≤ 1 := by
  nlinarith [frame.unit, sq_nonneg frame.cosine]

def Frame.swap (frame : Frame) : Frame where
  cosine := frame.sine
  sine := frame.cosine
  unit := by nlinarith [frame.unit]

def Frame.rotateQuarter (frame : Frame) : Frame where
  cosine := -frame.sine
  sine := frame.cosine
  unit := by nlinarith [frame.unit]

def Frame.reflectX (frame : Frame) : Frame where
  cosine := -frame.cosine
  sine := frame.sine
  unit := by nlinarith [frame.unit]

def Frame.reflectY (frame : Frame) : Frame where
  cosine := frame.cosine
  sine := -frame.sine
  unit := by nlinarith [frame.unit]

def Frame.place (frame : Frame) (localX localY : ℝ) : Point :=
  ⟨localX * frame.cosine - localY * frame.sine,
    localX * frame.sine + localY * frame.cosine⟩

structure PlacedSquare where
  center : Point
  frame : Frame

def PlacedSquare.translate
    (horizontal vertical : ℝ) (square : PlacedSquare) : PlacedSquare where
  center := square.center.translate horizontal vertical
  frame := square.frame

def PlacedSquare.swap (square : PlacedSquare) : PlacedSquare where
  center := square.center.swap
  frame := square.frame.swap

def PlacedSquare.rotateQuarter (square : PlacedSquare) : PlacedSquare where
  center := square.center
  frame := square.frame.rotateQuarter

def PlacedSquare.rotateHalf (square : PlacedSquare) : PlacedSquare :=
  square.rotateQuarter.rotateQuarter

def PlacedSquare.rotateThreeQuarter (square : PlacedSquare) : PlacedSquare :=
  square.rotateHalf.rotateQuarter

def PlacedSquare.reflectX (coordinateSum : ℝ) (square : PlacedSquare) : PlacedSquare where
  center := square.center.reflectX coordinateSum
  frame := square.frame.reflectX

def PlacedSquare.reflectY (coordinateSum : ℝ) (square : PlacedSquare) : PlacedSquare where
  center := square.center.reflectY coordinateSum
  frame := square.frame.reflectY

noncomputable def PlacedSquare.firstQuadrant (square : PlacedSquare) : PlacedSquare :=
  if 0 ≤ square.frame.cosine then
    if 0 ≤ square.frame.sine then square else square.rotateQuarter
  else if 0 ≤ square.frame.sine then square.rotateThreeQuarter else square.rotateHalf

lemma PlacedSquare.firstQuadrant_cosine_nonnegative (square : PlacedSquare) :
    0 ≤ square.firstQuadrant.frame.cosine := by
  simp only [PlacedSquare.firstQuadrant]
  split_ifs with cosine_nonnegative sine_nonnegative sine_nonnegative
  · exact cosine_nonnegative
  · simp [PlacedSquare.rotateQuarter, Frame.rotateQuarter]
    linarith
  · simp [PlacedSquare.rotateThreeQuarter, PlacedSquare.rotateHalf,
      PlacedSquare.rotateQuarter, Frame.rotateQuarter]
    exact sine_nonnegative
  · simp [PlacedSquare.rotateHalf, PlacedSquare.rotateQuarter, Frame.rotateQuarter]
    linarith

lemma PlacedSquare.firstQuadrant_sine_nonnegative (square : PlacedSquare) :
    0 ≤ square.firstQuadrant.frame.sine := by
  simp only [PlacedSquare.firstQuadrant]
  split_ifs with cosine_nonnegative sine_nonnegative sine_nonnegative
  · exact sine_nonnegative
  · simp [PlacedSquare.rotateQuarter, Frame.rotateQuarter]
    exact cosine_nonnegative
  · simp [PlacedSquare.rotateThreeQuarter, PlacedSquare.rotateHalf,
      PlacedSquare.rotateQuarter, Frame.rotateQuarter]
    linarith
  · simp [PlacedSquare.rotateHalf, PlacedSquare.rotateQuarter, Frame.rotateQuarter]
    linarith

@[simp] lemma PlacedSquare.firstQuadrant_center (square : PlacedSquare) :
    square.firstQuadrant.center = square.center := by
  simp only [PlacedSquare.firstQuadrant]
  split_ifs <;>
    rfl

def PlacedSquare.point (square : PlacedSquare) (localX localY : ℝ) : Point :=
  let offset := square.frame.place localX localY
  ⟨square.center.x + offset.x, square.center.y + offset.y⟩

def PlacedSquare.Contains (square : PlacedSquare) (point : Point) : Prop :=
  ∃ localX localY : ℝ,
    |localX| ≤ 1 / 2 ∧
      |localY| ≤ 1 / 2 ∧
        point = square.point localX localY

def PlacedSquare.InteriorContains (square : PlacedSquare) (point : Point) : Prop :=
  ∃ localX localY : ℝ,
    |localX| < 1 / 2 ∧
      |localY| < 1 / 2 ∧
        point = square.point localX localY

def PlacedSquare.localX (square : PlacedSquare) (point : Point) : ℝ :=
  (point.x - square.center.x) * square.frame.cosine +
    (point.y - square.center.y) * square.frame.sine

def PlacedSquare.localY (square : PlacedSquare) (point : Point) : ℝ :=
  -(point.x - square.center.x) * square.frame.sine +
    (point.y - square.center.y) * square.frame.cosine

lemma PlacedSquare.contains_iff_localCoordinates
    (square : PlacedSquare) (point : Point) :
    square.Contains point ↔
      |square.localX point| ≤ 1 / 2 ∧
        |square.localY point| ≤ 1 / 2 := by
  constructor
  · rintro ⟨localX, localY, localX_le, localY_le, rfl⟩
    have recovered_localX :
        square.localX (square.point localX localY) = localX := by
      dsimp [PlacedSquare.localX, PlacedSquare.point, Frame.place]
      linear_combination localX * square.frame.unit
    have recovered_localY :
        square.localY (square.point localX localY) = localY := by
      dsimp [PlacedSquare.localY, PlacedSquare.point, Frame.place]
      linear_combination localY * square.frame.unit
    rw [recovered_localX, recovered_localY]
    exact ⟨localX_le, localY_le⟩
  · rintro ⟨localX_le, localY_le⟩
    refine ⟨square.localX point, square.localY point,
      localX_le, localY_le, ?_⟩
    rw [Point.mk.injEq]
    constructor
    · dsimp [PlacedSquare.localX, PlacedSquare.localY,
        PlacedSquare.point, Frame.place]
      linear_combination
        -(point.x - square.center.x) * square.frame.unit
    · dsimp [PlacedSquare.localX, PlacedSquare.localY,
        PlacedSquare.point, Frame.place]
      linear_combination
        -(point.y - square.center.y) * square.frame.unit

@[simp] lemma PlacedSquare.translate_contains_iff
    (square : PlacedSquare) (horizontal vertical : ℝ) (point : Point) :
    (square.translate horizontal vertical).Contains
        (point.translate horizontal vertical) ↔
      square.Contains point := by
  rw [(square.translate horizontal vertical).contains_iff_localCoordinates,
    square.contains_iff_localCoordinates]
  constructor <;> intro coordinates <;> convert coordinates using 1 <;>
    simp [PlacedSquare.translate, Point.translate, PlacedSquare.localX,
      PlacedSquare.localY]

@[simp] lemma PlacedSquare.swap_contains_iff
    (square : PlacedSquare) (point : Point) :
    square.swap.Contains point.swap ↔ square.Contains point := by
  constructor
  · rintro ⟨localX, localY, localX_le, localY_le, point_eq⟩
    refine ⟨localX, -localY, localX_le, by simpa using localY_le, ?_⟩
    apply Point.swap_injective
    rw [point_eq, Point.mk.injEq]
    constructor
    · simp [PlacedSquare.swap, PlacedSquare.point, Frame.swap,
        Frame.place, Point.swap]
      ring
    · simp [PlacedSquare.swap, PlacedSquare.point, Frame.swap,
        Frame.place, Point.swap]
  · rintro ⟨localX, localY, localX_le, localY_le, point_eq⟩
    refine ⟨localX, -localY, localX_le, by simpa using localY_le, ?_⟩
    rw [point_eq, Point.mk.injEq]
    constructor
    · simp [PlacedSquare.swap, PlacedSquare.point, Frame.swap,
        Frame.place, Point.swap]
    · simp [PlacedSquare.swap, PlacedSquare.point, Frame.swap,
        Frame.place, Point.swap]
      ring

@[simp] lemma PlacedSquare.reflectX_contains_iff
    (square : PlacedSquare) (coordinateSum : ℝ) (point : Point) :
    (square.reflectX coordinateSum).Contains (point.reflectX coordinateSum) ↔
      square.Contains point := by
  constructor
  · rintro ⟨localX, localY, localX_le, localY_le, point_eq⟩
    refine ⟨localX, -localY, localX_le, by simpa using localY_le, ?_⟩
    apply Point.reflectX_injective coordinateSum
    rw [point_eq, Point.mk.injEq]
    constructor
    · simp [PlacedSquare.reflectX, PlacedSquare.point,
        Frame.reflectX, Frame.place, Point.reflectX]
      ring
    · simp [PlacedSquare.reflectX, PlacedSquare.point,
        Frame.reflectX, Frame.place, Point.reflectX]
  · rintro ⟨localX, localY, localX_le, localY_le, point_eq⟩
    refine ⟨localX, -localY, localX_le, by simpa using localY_le, ?_⟩
    rw [point_eq, Point.mk.injEq]
    constructor
    · simp [PlacedSquare.reflectX, PlacedSquare.point,
        Frame.reflectX, Frame.place, Point.reflectX]
      ring
    · simp [PlacedSquare.reflectX, PlacedSquare.point,
        Frame.reflectX, Frame.place, Point.reflectX]

@[simp] lemma PlacedSquare.reflectY_contains_iff
    (square : PlacedSquare) (coordinateSum : ℝ) (point : Point) :
    (square.reflectY coordinateSum).Contains (point.reflectY coordinateSum) ↔
      square.Contains point := by
  constructor
  · rintro ⟨localX, localY, localX_le, localY_le, point_eq⟩
    refine ⟨localX, -localY, localX_le, by simpa using localY_le, ?_⟩
    apply Point.reflectY_injective coordinateSum
    rw [point_eq, Point.mk.injEq]
    constructor
    · simp [PlacedSquare.reflectY, PlacedSquare.point,
        Frame.reflectY, Frame.place, Point.reflectY]
    · simp [PlacedSquare.reflectY, PlacedSquare.point,
        Frame.reflectY, Frame.place, Point.reflectY]
      ring
  · rintro ⟨localX, localY, localX_le, localY_le, point_eq⟩
    refine ⟨localX, -localY, localX_le, by simpa using localY_le, ?_⟩
    rw [point_eq, Point.mk.injEq]
    constructor
    · simp [PlacedSquare.reflectY, PlacedSquare.point,
        Frame.reflectY, Frame.place, Point.reflectY]
    · simp [PlacedSquare.reflectY, PlacedSquare.point,
        Frame.reflectY, Frame.place, Point.reflectY]
      ring

@[simp] lemma PlacedSquare.rotateQuarter_contains_iff
    (square : PlacedSquare) (point : Point) :
    square.rotateQuarter.Contains point ↔ square.Contains point := by
  constructor
  · rintro ⟨localX, localY, localX_le, localY_le, point_eq⟩
    refine ⟨-localY, localX, ?_, ?_, ?_⟩
    · simpa using localY_le
    · simpa using localX_le
    · rw [point_eq, Point.mk.injEq]
      constructor <;>
        simp [PlacedSquare.rotateQuarter, PlacedSquare.point,
          Frame.rotateQuarter, Frame.place] <;>
        ring
  · rintro ⟨localX, localY, localX_le, localY_le, point_eq⟩
    refine ⟨localY, -localX, ?_, ?_, ?_⟩
    · simpa using localY_le
    · simpa using localX_le
    · rw [point_eq, Point.mk.injEq]
      constructor <;>
        simp [PlacedSquare.rotateQuarter, PlacedSquare.point,
          Frame.rotateQuarter, Frame.place] <;>
        ring

@[simp] lemma PlacedSquare.firstQuadrant_contains_iff
    (square : PlacedSquare) (point : Point) :
    square.firstQuadrant.Contains point ↔ square.Contains point := by
  simp only [PlacedSquare.firstQuadrant]
  split_ifs <;>
    simp [PlacedSquare.rotateHalf, PlacedSquare.rotateThreeQuarter]

def Container.Contains (side : ℝ) (point : Point) : Prop :=
  0 ≤ point.x ∧ point.x ≤ side ∧ 0 ≤ point.y ∧ point.y ≤ side

@[simp] lemma Container.swap_contains_iff (side : ℝ) (point : Point) :
    Container.Contains side point.swap ↔ Container.Contains side point := by
  simp only [Container.Contains, Point.swap]
  tauto

@[simp] lemma Container.reflectX_contains_iff (side : ℝ) (point : Point) :
    Container.Contains side (point.reflectX side) ↔
      Container.Contains side point := by
  simp only [Container.Contains, Point.reflectX]
  constructor <;> rintro ⟨left, right, bottom, top⟩ <;>
    exact ⟨by linarith, by linarith, bottom, top⟩

@[simp] lemma Container.reflectY_contains_iff (side : ℝ) (point : Point) :
    Container.Contains side (point.reflectY side) ↔
      Container.Contains side point := by
  simp only [Container.Contains, Point.reflectY]
  constructor <;> rintro ⟨left, right, bottom, top⟩ <;>
    exact ⟨left, right, by linarith, by linarith⟩

def PlacedSquare.Fits (square : PlacedSquare) (side : ℝ) : Prop :=
  ∀ ⦃point⦄, square.Contains point → Container.Contains side point

@[simp] lemma PlacedSquare.swap_fits_iff
    (square : PlacedSquare) (side : ℝ) :
    square.swap.Fits side ↔ square.Fits side := by
  constructor
  · intro fits point point_mem
    have swapped_bounds := fits
      ((square.swap_contains_iff point).2 point_mem)
    exact (Container.swap_contains_iff side point).1 swapped_bounds
  · intro fits point point_mem
    have source_mem := (square.swap_contains_iff point.swap).1 (by
      simpa using point_mem)
    have source_bounds := fits source_mem
    exact (Container.swap_contains_iff side point).1 source_bounds

@[simp] lemma PlacedSquare.reflectX_fits_iff
    (square : PlacedSquare) (side : ℝ) :
    (square.reflectX side).Fits side ↔ square.Fits side := by
  constructor
  · intro fits point point_mem
    have reflected_bounds := fits
      ((square.reflectX_contains_iff side point).2 point_mem)
    exact (Container.reflectX_contains_iff side point).1 reflected_bounds
  · intro fits point point_mem
    have source_mem := (square.reflectX_contains_iff side
      (point.reflectX side)).1 (by simpa using point_mem)
    have source_bounds := fits source_mem
    exact (Container.reflectX_contains_iff side point).1 source_bounds

@[simp] lemma PlacedSquare.reflectY_fits_iff
    (square : PlacedSquare) (side : ℝ) :
    (square.reflectY side).Fits side ↔ square.Fits side := by
  constructor
  · intro fits point point_mem
    have reflected_bounds := fits
      ((square.reflectY_contains_iff side point).2 point_mem)
    exact (Container.reflectY_contains_iff side point).1 reflected_bounds
  · intro fits point point_mem
    have source_mem := (square.reflectY_contains_iff side
      (point.reflectY side)).1 (by simpa using point_mem)
    have source_bounds := fits source_mem
    exact (Container.reflectY_contains_iff side point).1 source_bounds

@[simp] lemma PlacedSquare.firstQuadrant_fits_iff
    (square : PlacedSquare) (side : ℝ) :
    square.firstQuadrant.Fits side ↔ square.Fits side := by
  constructor
  · intro fits point point_mem
    exact fits ((square.firstQuadrant_contains_iff point).2 point_mem)
  · intro fits point point_mem
    exact fits ((square.firstQuadrant_contains_iff point).1 point_mem)

def PlacedSquare.InteriorDisjoint (left right : PlacedSquare) : Prop :=
  ∀ point, ¬(left.InteriorContains point ∧ right.InteriorContains point)

lemma PlacedSquare.InteriorDisjoint.symm
    {left right : PlacedSquare} (disjoint : left.InteriorDisjoint right) :
    right.InteriorDisjoint left := by
  intro point shared
  exact disjoint point ⟨shared.2, shared.1⟩

def dot (leftX leftY rightX rightY : ℝ) : ℝ :=
  leftX * rightX + leftY * rightY

noncomputable def PlacedSquare.projectionRadius
    (square : PlacedSquare) (axisX axisY : ℝ) : ℝ :=
  (|dot axisX axisY square.frame.cosine square.frame.sine| +
    |dot axisX axisY (-square.frame.sine) square.frame.cosine|) / 2

def PlacedSquare.SeparatedOn
    (left right : PlacedSquare) (axisX axisY : ℝ) : Prop :=
  left.projectionRadius axisX axisY + right.projectionRadius axisX axisY ≤
    |dot
      (right.center.x - left.center.x)
      (right.center.y - left.center.y)
      axisX axisY|

structure Packing (squareCount : ℕ) (side : ℝ) where
  squares : Fin squareCount → PlacedSquare
  side_nonnegative : 0 ≤ side
  fits : ∀ index, (squares index).Fits side
  disjoint : ∀ left right, left ≠ right →
    (squares left).InteriorDisjoint (squares right)

def HasPacking (squareCount : ℕ) (side : ℝ) : Prop :=
  Nonempty (Packing squareCount side)

def IsLowerBound (squareCount : ℕ) (side : ℝ) : Prop :=
  ∀ candidateSide, HasPacking squareCount candidateSide → side ≤ candidateSide

def IsMinimumSide (squareCount : ℕ) (side : ℝ) : Prop :=
  HasPacking squareCount side ∧
    IsLowerBound squareCount side

def Packing.reindex
    {sourceCount targetCount : ℕ} {side : ℝ}
    (packing : Packing sourceCount side)
    (embedding : Fin targetCount ↪ Fin sourceCount) :
    Packing targetCount side where
  squares := packing.squares ∘ embedding
  side_nonnegative := packing.side_nonnegative
  fits := fun index => packing.fits (embedding index)
  disjoint := by
    intro left right different
    exact packing.disjoint (embedding left) (embedding right)
      fun equality => different (embedding.injective equality)

lemma HasPacking.mono
    {sourceCount targetCount : ℕ} {side : ℝ}
    (packing : HasPacking sourceCount side)
    (count_le : targetCount ≤ sourceCount) :
    HasPacking targetCount side := by
  rcases packing with ⟨source⟩
  exact ⟨source.reindex (Fin.castLEEmb count_le)⟩

def Packing.enlarge
    {squareCount : ℕ} {side largerSide : ℝ}
    (packing : Packing squareCount side) (side_le : side ≤ largerSide) :
    Packing squareCount largerSide where
  squares := packing.squares
  side_nonnegative := packing.side_nonnegative.trans side_le
  fits := by
    intro index point point_mem
    have contained := packing.fits index point_mem
    exact ⟨contained.1, contained.2.1.trans side_le,
      contained.2.2.1, contained.2.2.2.trans side_le⟩
  disjoint := packing.disjoint

lemma HasPacking.enlarge
    {squareCount : ℕ} {side largerSide : ℝ}
    (packing : HasPacking squareCount side) (side_le : side ≤ largerSide) :
    HasPacking squareCount largerSide :=
  ⟨packing.some.enlarge side_le⟩

lemma abs_linearCombination_le
    {localX localY coefficientX coefficientY : ℝ}
    (localX_le : |localX| ≤ 1 / 2)
    (localY_le : |localY| ≤ 1 / 2) :
    |localX * coefficientX + localY * coefficientY| ≤
      (|coefficientX| + |coefficientY|) / 2 := by
  calc
    |localX * coefficientX + localY * coefficientY| ≤
        |localX * coefficientX| + |localY * coefficientY| := abs_add_le _ _
    _ = |localX| * |coefficientX| + |localY| * |coefficientY| := by
      rw [abs_mul, abs_mul]
    _ ≤ (1 / 2) * |coefficientX| + (1 / 2) * |coefficientY| := by
      gcongr
    _ = (|coefficientX| + |coefficientY|) / 2 := by ring

lemma abs_linearCombination_lt
    {localX localY coefficientX coefficientY : ℝ}
    (localX_lt : |localX| < 1 / 2)
    (localY_lt : |localY| < 1 / 2)
    (coefficient_nonzero : coefficientX ≠ 0 ∨ coefficientY ≠ 0) :
    |localX * coefficientX + localY * coefficientY| <
      (|coefficientX| + |coefficientY|) / 2 := by
  calc
    |localX * coefficientX + localY * coefficientY| ≤
        |localX * coefficientX| + |localY * coefficientY| := abs_add_le _ _
    _ = |localX| * |coefficientX| + |localY| * |coefficientY| := by
      rw [abs_mul, abs_mul]
    _ < (1 / 2) * |coefficientX| + (1 / 2) * |coefficientY| := by
      rcases coefficient_nonzero with coefficientX_nonzero | coefficientY_nonzero
      · exact add_lt_add_of_lt_of_le
          (mul_lt_mul_of_pos_right localX_lt (abs_pos.mpr coefficientX_nonzero))
          (mul_le_mul_of_nonneg_right (le_of_lt localY_lt) (abs_nonneg _))
      · exact add_lt_add_of_le_of_lt
          (mul_le_mul_of_nonneg_right (le_of_lt localX_lt) (abs_nonneg _))
          (mul_lt_mul_of_pos_right localY_lt (abs_pos.mpr coefficientY_nonzero))
    _ = (|coefficientX| + |coefficientY|) / 2 := by ring

lemma Frame.projection_coefficients_nonzero
    (frame : Frame) {axisX axisY : ℝ}
    (axis_nonzero : axisX ≠ 0 ∨ axisY ≠ 0) :
    dot axisX axisY frame.cosine frame.sine ≠ 0 ∨
      dot axisX axisY (-frame.sine) frame.cosine ≠ 0 := by
  by_contra both_zero
  push Not at both_zero
  rcases both_zero with ⟨first_zero, second_zero⟩
  simp only [dot] at first_zero second_zero
  rcases axis_nonzero with axisX_nonzero | axisY_nonzero
  · have : axisX * (frame.cosine ^ 2 + frame.sine ^ 2) = 0 := by
      linear_combination frame.cosine * first_zero - frame.sine * second_zero
    rw [frame.unit, mul_one] at this
    exact axisX_nonzero this
  · have : axisY * (frame.cosine ^ 2 + frame.sine ^ 2) = 0 := by
      linear_combination frame.sine * first_zero + frame.cosine * second_zero
    rw [frame.unit, mul_one] at this
    exact axisY_nonzero this

lemma PlacedSquare.projection_lt_radius
    {square : PlacedSquare} {point : Point} {axisX axisY : ℝ}
    (point_interior : square.InteriorContains point)
    (axis_nonzero : axisX ≠ 0 ∨ axisY ≠ 0) :
    |dot
      (point.x - square.center.x)
      (point.y - square.center.y)
      axisX axisY| < square.projectionRadius axisX axisY := by
  rcases point_interior with ⟨localX, localY, localX_lt, localY_lt, point_eq⟩
  subst point
  have bound := abs_linearCombination_lt
    localX_lt localY_lt (square.frame.projection_coefficients_nonzero axis_nonzero)
  simp only [PlacedSquare.point, Frame.place, dot]
  rw [PlacedSquare.projectionRadius]
  convert bound using 1
  congr 1
  simp only [dot]
  ring

lemma PlacedSquare.separatedOn_interiorDisjoint
    {left right : PlacedSquare} {axisX axisY : ℝ}
    (separated : left.SeparatedOn right axisX axisY)
    (axis_nonzero : axisX ≠ 0 ∨ axisY ≠ 0) :
    left.InteriorDisjoint right := by
  intro point shared
  have left_projection := left.projection_lt_radius shared.1 axis_nonzero
  have right_projection := right.projection_lt_radius shared.2 axis_nonzero
  have triangle :
      |dot
        (right.center.x - left.center.x)
        (right.center.y - left.center.y)
        axisX axisY| ≤
        |dot
          (point.x - left.center.x)
          (point.y - left.center.y)
          axisX axisY| +
        |dot
          (point.x - right.center.x)
          (point.y - right.center.y)
          axisX axisY| := by
    calc
      |dot
        (right.center.x - left.center.x)
        (right.center.y - left.center.y)
        axisX axisY| =
          |dot
            (point.x - left.center.x)
            (point.y - left.center.y)
            axisX axisY -
          dot
            (point.x - right.center.x)
            (point.y - right.center.y)
            axisX axisY| := by
              congr 1
              simp only [dot]
              ring
      _ ≤ _ := abs_sub _ _
  exact (not_lt_of_ge separated) (lt_of_le_of_lt triangle (add_lt_add left_projection right_projection))

end SquarePackingArchive
