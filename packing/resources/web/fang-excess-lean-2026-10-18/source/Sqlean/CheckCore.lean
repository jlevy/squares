/-!
# The certificate checker (core Lean only, no Mathlib)

A certificate square is `⟨X, Y, C, S, N⟩ : Sq`, all integers: centre `(X / D, Y / D)` for a global
denominator `D`, rotation `(cos θ, sin θ) = (C / N, S / N)` with `C² + S² = N²`, `N > 0`.  A rational
certificate line `x y t` becomes `C = q² − p², S = 2pq, N = q² + p²` for `t = p / q`, and
`X = x·D`, `Y = y·D`.

This file has no imports beyond Lean's prelude so that the files holding data and kernel checks
(`decide +kernel`) do not load Mathlib.  Soundness is in `Sqlean/Check.lean`.

* `unitOK`: `C² + S² = N²` and `N > 0`.
* `boxOK D Wn Hn Sd`: the four corners lie in `[0, Wn / Sd] × [0, Hn / Sd]`.
* `farOK D`: the centres are more than `√2` apart: `ΔX² + ΔY² > 2 D²`.
* `sepOK D i j k`: side `k` of square `i` has the four corners of `j` on its closed outer side,
  tested at once for all four corners: `Ni Nj D + D (|u| + |v|) ≤ 2 Nj (A ΔX + B ΔY)` where
  `(A, B)` is the integer normal of side `k` and `u, v` are its coordinates in the frame of `j`.
* `pairOK D i j = farOK ∨ some side of i ∨ some side of j`.
* `headsOK D k L`: `pairOK` for every pair whose first element is among the first `k` of `L`,
  except that a row stops at the first square more than `√2` to the right in `X` (`cutX`); with
  `sortedX L` every later square of the row is then far as well.
-/

namespace UnitSquarePacking.Cert

structure Sq where
  X : Int
  Y : Int
  C : Int
  S : Int
  N : Int

def unitOK (q : Sq) : Bool :=
  q.C * q.C + q.S * q.S == q.N * q.N && decide (0 < q.N)

/-- Corner `(ea / 2, eb / 2)` of `q` (local coordinates, `ea, eb = ±1`) lies in the box. -/
def cornerOK (D Wn Hn Sd : Int) (q : Sq) (ea eb : Int) : Bool :=
  let vx := 2 * q.N * q.X + D * (ea * q.C - eb * q.S)
  let vy := 2 * q.N * q.Y + D * (ea * q.S + eb * q.C)
  let M := 2 * q.N * D
  decide (0 ≤ vx) && decide (vx * Sd ≤ M * Wn) && decide (0 ≤ vy) && decide (vy * Sd ≤ M * Hn)

def boxOK (D Wn Hn Sd : Int) (q : Sq) : Bool :=
  cornerOK D Wn Hn Sd q 1 1 && cornerOK D Wn Hn Sd q 1 (-1) &&
  cornerOK D Wn Hn Sd q (-1) 1 && cornerOK D Wn Hn Sd q (-1) (-1)

/-- The integer outward normal of side `k` of a square with rotation `(C, S)`; matches `nrm`. -/
def nA (C S : Int) : Nat → Int
  | 0 => C
  | 1 => -S
  | 2 => -C
  | _ => S

def nB (C S : Int) : Nat → Int
  | 0 => S
  | 1 => C
  | 2 => -S
  | _ => -C

def farOK (D : Int) (i j : Sq) : Bool :=
  let dx := j.X - i.X
  let dy := j.Y - i.Y
  decide (2 * D * D < dx * dx + dy * dy)

def sepOK (D : Int) (i j : Sq) (k : Nat) : Bool :=
  let A := nA i.C i.S k
  let B := nB i.C i.S k
  let u := A * j.C + B * j.S
  let v := B * j.C - A * j.S
  decide (i.N * j.N * D + D * ((u.natAbs : Int) + (v.natAbs : Int)) ≤
    2 * j.N * (A * (j.X - i.X) + B * (j.Y - i.Y)))

def sepAny (D : Int) (i j : Sq) : Bool :=
  sepOK D i j 0 || sepOK D i j 1 || sepOK D i j 2 || sepOK D i j 3

def pairOK (D : Int) (i j : Sq) : Bool :=
  farOK D i j || sepAny D i j || sepAny D j i

/-- `r` is so far to the right of `q` that, in a list sorted by `X`, it and everything after it
is far from `q`. -/
def cutX (D : Int) (q r : Sq) : Bool :=
  decide (q.X ≤ r.X) && decide (2 * D * D < (r.X - q.X) * (r.X - q.X))

/-- `pairOK D q r` for every `r` in the list, stopping at the first `r` with `cutX`. -/
def rowOK (D : Int) (q : Sq) : List Sq → Bool
  | [] => true
  | r :: rs => cutX D q r || (pairOK D q r && rowOK D q rs)

def headsOK (D : Int) : Nat → List Sq → Bool
  | 0, _ => true
  | _, [] => true
  | k + 1, q :: rest => rowOK D q rest && headsOK D k rest

/-- The list is sorted by `X` (non-decreasing). -/
def sortedX : List Sq → Bool
  | [] => true
  | [_] => true
  | a :: b :: rest => decide (a.X ≤ b.X) && sortedX (b :: rest)

end UnitSquarePacking.Cert
