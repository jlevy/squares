/-
Basic data types and exact parsing for the s(17) >= 4.5705 certificate.

Design rule: parsing failures produce *poisoned* values that make every
downstream check return `false`. No malformed input can create a passing
configuration; it can only cause a failing one.
-/

namespace Square17

structure Atom where
  x : Int
  y : Int
  w : Int
deriving Repr, Inhabited

def parseNat? (s : String) : Option Nat :=
  if s.isEmpty || !s.all Char.isDigit then none
  else some (s.foldl (fun acc c => acc * 10 + (c.toNat - '0'.toNat)) 0)

/-- Poisoned integer parse: malformed input becomes `-1`, which violates the
nonnegativity constraints checked everywhere downstream. -/
def parseIntPoison (s : String) : Int :=
  match parseNat? s with
  | some n => (n : Int)
  | none => -1

def parseAtoms (raw : String) : Array Atom :=
  (raw.splitOn "\n").foldl (init := #[]) fun acc line =>
    if line.isEmpty then acc
    else
      match line.splitOn " " with
      | [a, b, c] => acc.push ⟨parseIntPoison a, parseIntPoison b, parseIntPoison c⟩
      | _ => acc.push ⟨-1, -1, -1⟩

/-- Parse "p q" sample lines; malformed lines poison to `(-1, -1)`, which the
sample-range preconditions reject. -/
def parseSamples (raw : String) : Array (Int × Int) :=
  (raw.splitOn "\n").foldl (init := #[]) fun acc line =>
    if line.isEmpty then acc
    else
      match line.splitOn " " with
      | [a, b] => acc.push (parseIntPoison a, parseIntPoison b)
      | _ => acc.push (-1, -1)

def intAbs (x : Int) : Int := if x < 0 then -x else x

/-- Sorted ascending, duplicates removed. -/
def sortedDedup (a : Array Int) : Array Int :=
  let s := a.qsort (· < ·)
  s.foldl (init := #[]) fun acc v =>
    if acc.isEmpty || acc.back! != v then acc.push v else acc

/-- Exact index of `v` in strictly sorted `xs`; `none` if absent. -/
def exactIdx (xs : Array Int) (v : Int) : Option Nat := Id.run do
  let mut lo : Nat := 0
  let mut hi : Nat := xs.size
  for _ in [0:64] do
    if lo < hi then
      let mid := (lo + hi) / 2
      if xs[mid]! < v then
        lo := mid + 1
      else
        hi := mid
  if lo < xs.size && xs[lo]! == v then return some lo
  return none

end Square17
