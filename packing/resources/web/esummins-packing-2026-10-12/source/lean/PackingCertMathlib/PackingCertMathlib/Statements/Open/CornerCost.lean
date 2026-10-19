import PackingCertMathlib.Statements.Open.CornerChase
import PackingCertMathlib.Statements.Open.TypeTChase

/-!
# -- OPEN: CORNER COST -- the two corner classes F / T, their wall roles, and the f-table (A281)

`docs/proofs/corner_cost.md` (parts in `attempts/A281-corner-cost/notes/`).  On the k0 window
every corner
box is doubly met with at most one toucher per wall; the PAIR corner's two touchers are either one
FLAT +
one POKER (class F) or both TILTED (class T).  Each corner puts one meeter on each of its two
walls, so a
corner is `T`, `Ff` (flat on its outgoing wall, poker on its incoming wall) or `Fw` (the mirror),
and every
wall carries a PAIR of roles from {Phi, Pi, tau}.  The finite bookkeeping below is decided by
`decide` over
the 81 assignments (case split + `decide`); the geometry enters through two named hypotheses on
the predicate `Realised`
("some k0 packing of eleven squares at a side in [3.82, ŝ] has these four corner classes"):

* `no_PiPi_window` [T-prose from `two_pokers_window`]: a realised assignment has no wall of type
Pi-Pi
  (TWO-POKERS, s* = 3.9342 > ŝ).
* `notches_le_three` [M, SEPARATE-NOTCHES]: on a Phi-Pi wall the poker's slot needs a FREE square
(the
  flat cannot meet it, FLAT-ABOVE; no other meeter can, PROJECTION / SAME-WALL), one free square
  serves at
  most one poker notch, and there are three free squares.

Consequences (theorems): `allF_is_pinwheel` (four F corners without a Pi-Pi wall have four Phi-Pi
walls),
`realised_has_T` (every realised skeleton has a T corner), `notches_of_noPiPi` (the count never
exceeds
four and the pinwheel is the only assignment reaching it).  The [T]-only layer of the f-table (the
room
count with PROJECTION sharing, which kills nothing) is `count281.py`; it is not formalised.
-/

namespace PackingCert.S11.OpenLemmas

/-- the class of a PAIR corner: both tilted / flat on the outgoing wall / flat on the incoming
wall. -/
inductive Role | T | Ff | Fw
  deriving DecidableEq, Repr

/-- the role a corner's meeter plays on a wall. -/
inductive WallRole | Phi | Pi | tau
  deriving DecidableEq, Repr

open Role WallRole

def outRole : Role → WallRole
  | Ff => Phi
  | Fw => Pi
  | T => tau

def inRole : Role → WallRole
  | Ff => Pi
  | Fw => Phi
  | T => tau

/-- the four corner classes, ccw from BL. -/
structure Assign where
  c0 : Role
  c1 : Role
  c2 : Role
  c3 : Role
  deriving DecidableEq, Repr

namespace Assign

def corner (a : Assign) : Fin 4 → Role
  | 0 => a.c0
  | 1 => a.c1
  | 2 => a.c2
  | 3 => a.c3

/-- wall `w` joins corner `w` (outgoing) and corner `w + 1` (incoming). -/
def wall (a : Assign) (w : Fin 4) : WallRole × WallRole :=
  (outRole (a.corner w), inRole (a.corner (w + 1)))

def isPiPi (p : WallRole × WallRole) : Bool := p.1 == Pi && p.2 == Pi

def isPhiPi (p : WallRole × WallRole) : Bool :=
  (p.1 == Phi && p.2 == Pi) || (p.1 == Pi && p.2 == Phi)

def hasPiPi (a : Assign) : Bool := (List.finRange 4).any fun w => isPiPi (a.wall w)

/-- the number of F corners. -/
def f (a : Assign) : Nat := (List.finRange 4).countP fun c => a.corner c != T

/-- the number of Phi-Pi walls = poker notches that need a free square. -/
def notches (a : Assign) : Nat := (List.finRange 4).countP fun w => isPhiPi (a.wall w)

def hasT (a : Assign) : Bool := (List.finRange 4).any fun c => a.corner c == T

end Assign

/-- **PINWHEEL** [T]: four F corners with no Pi-Pi wall put a flat and a poker on every wall. -/
theorem allF_is_pinwheel : ∀ a : Assign, a.f = 4 → a.hasPiPi = false → a.notches = 4 := by
  rintro ⟨c0, c1, c2, c3⟩
  cases c0 <;> cases c1 <;> cases c2 <;> cases c3 <;> decide

/-- **NOTCH COUNT** [T]: without a Pi-Pi wall, the number of poker notches is `4` only for the
all-F pinwheel; every other assignment has at most `2`. -/
theorem notches_of_noPiPi :
    ∀ a : Assign, a.hasPiPi = false → a.notches ≤ 2 ∨ (a.f = 4 ∧ a.notches = 4) := by
  rintro ⟨c0, c1, c2, c3⟩
  cases c0 <;> cases c1 <;> cases c2 <;> cases c3 <;> decide

/-- **T OR PINWHEEL** [T]: without a Pi-Pi wall, either some corner is class T or all four are F
in the
pinwheel arrangement. -/
theorem hasT_or_pinwheel :
    ∀ a : Assign, a.hasPiPi = false → a.hasT = true ∨ a.notches = 4 := by
  rintro ⟨c0, c1, c2, c3⟩
  cases c0 <;> cases c1 <;> cases c2 <;> cases c3 <;> decide

/-- "some k0_00 packing of eleven unit squares at a side in `[3.82, ŝ]` has its four PAIR corners of
these classes" -- the bridge from the geometry to the bookkeeping; opaque here. -/
axiom Realised : Assign → Prop

/-- **NO Pi-Pi WALL** [T-prose] (`corner_cost.md` part 2, from `two_pokers_window`): two pokers on
one
wall need side `≥ s* = 3.9342370 > ŝ`, so a realised assignment has no Pi-Pi wall. -/
axiom no_PiPi_window (a : Assign) (h : Realised a) : a.hasPiPi = false

/-- **NOTCHES ≤ 3** [M] (`corner_chase.md` §3.3 SEPARATE-NOTCHES, sup margin −0.003 at ŝ): each
Phi-Pi
wall's poker slot is met by a free square of its own (FLAT-ABOVE + PROJECTION [T]; one free square
per
notch [M]), and a realised eleven-square packing has three free squares. -/
axiom notches_le_three (a : Assign) (h : Realised a) : a.notches ≤ 3

/-- **EVERY REALISED SKELETON HAS A T CORNER** [T given the two hypotheses]. -/
theorem realised_has_T (a : Assign) (h : Realised a) : a.hasT = true := by
  rcases hasT_or_pinwheel a (no_PiPi_window a h) with hT | h4
  · exact hT
  · have := notches_le_three a h
    omega

/-- **NO ALL-F SKELETON ON THE WINDOW** [T given the two hypotheses] (A248's corollary in role
form).
-/
theorem no_allF_realised (a : Assign) (h : Realised a) : a.f ≠ 4 := by
  intro h4
  have := allF_is_pinwheel a h4 (no_PiPi_window a h)
  have := notches_le_three a h
  omega

end PackingCert.S11.OpenLemmas
