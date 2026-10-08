import Mathlib.Data.Real.Basic
import Mathlib.Algebra.Group.Prod

/-!
# Actual geometric objects used in the eleven-square problem

The square is described by its centre and an arbitrary real unit axis.
`Packing` assumes only containment and disjoint open interiors. In particular,
centre separation and cell occupancy are theorems, not extra assumptions.
-/

namespace ElevenSquare

abbrev Point := ℝ × ℝ

def dot (p q : Point) : ℝ := p.1 * q.1 + p.2 * q.2
def normSq (p : Point) : ℝ := dot p p
def perp (p : Point) : Point := (-p.2, p.1)

structure UnitSquare where
  center : Point
  axis : Point
  axis_unit : normSq axis = 1

def localX (q : UnitSquare) (p : Point) : ℝ := dot (p - q.center) q.axis
def localY (q : UnitSquare) (p : Point) : ℝ := dot (p - q.center) (perp q.axis)

def ClosedSquare (q : UnitSquare) (p : Point) : Prop :=
  |localX q p| ≤ 1 / 2 ∧ |localY q p| ≤ 1 / 2

def OpenSquare (q : UnitSquare) (p : Point) : Prop :=
  |localX q p| < 1 / 2 ∧ |localY q p| < 1 / 2

def InContainer (S : ℝ) (p : Point) : Prop :=
  0 ≤ p.1 ∧ p.1 ≤ S ∧ 0 ≤ p.2 ∧ p.2 ≤ S

structure Packing (n : ℕ) (S : ℝ) where
  squares : Fin n → UnitSquare
  side_nonneg : 0 ≤ S
  contained : ∀ i p, ClosedSquare (squares i) p → InContainer S p
  interior_disjoint : ∀ i j, i ≠ j → ∀ p,
    ¬ (OpenSquare (squares i) p ∧ OpenSquare (squares j) p)

def Packable (n : ℕ) (S : ℝ) : Prop := Nonempty (Packing n S)

def translatedSquare (q : UnitSquare) (v : Point) : UnitSquare :=
  ⟨q.center + v, q.axis, q.axis_unit⟩

end ElevenSquare
