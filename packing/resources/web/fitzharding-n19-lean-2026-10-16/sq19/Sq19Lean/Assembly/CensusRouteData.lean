import Sq19Lean.Cover.OrbitData

/-! Small finite data for connecting the generated census exclusion to the final assembly.
The definitions `popc`, `count`, `survivorImages`, `isSurvivor`, and `exceptions` have
the same values as `gen_census_complete.py` emits for the complete census. They do
not import that large generated proof. Applying its `census_excluded` theorem to
the interface in `CensusRoute.lean` checks this agreement by definitional equality.
-/
namespace Sq19.Assembly.CensusRoute

def popc : ℕ → ℕ → ℕ
  | 0, _ => 0
  | k + 1, m => m % 2 + popc k (m / 2)

def count (m : ℕ) : ℕ := popc 25 m

/-- All 38 symmetry images of the seven census survivors. -/
def survivorImages : List ℕ := [
  0x00f7fff, 0x00fbfff, 0x00fdfff, 0x00fefff, 0x00ff7ff, 0x00ffbff,
  0x00ffdff, 0x00ffeff, 0x00fff7f, 0x00fffbf, 0x00fffdf, 0x00fffef,
  0x0f15fff, 0x0f17bff, 0x0f17fbf, 0x0f1ddff, 0x0f1dfdf, 0x0f29fff,
  0x0f2b7ff, 0x0f2bf7f, 0x0f2deff, 0x0f2dfef, 0x0f46fff, 0x0f47eff,
  0x0f47fef, 0x0f4e7ff, 0x0f4ef7f, 0x0f8afff, 0x0f8bdff, 0x0f8bfdf,
  0x0f8ebff, 0x0f8efbf, 0x103ffff, 0x105ffff, 0x10affff, 0x10cffff,
  0x10ffff6, 0x10ffff9]

def isSurvivor (m : ℕ) : Bool := survivorImages.contains m

/-- The empty exception encoding emitted by the complete census generator. -/
def exceptionsRaw : String := ""

/-- Retain the generator's parser expression so its theorem plugs in directly. -/
def exceptions : List ℕ := (exceptionsRaw.splitOn " ").filterMap String.toNat?

/-- The precise hypotheses under which the complete census excludes a mask. -/
abbrev Excluded (m : ℕ) : Prop :=
  m < 2 ^ 25 ∧ count m = 19 ∧ isSurvivor m = false ∧ m ∉ exceptions

/-- The capture representatives, in state-number order 3435, 3438, 3442. -/
def captureMasks : List ℕ := [0x0f15fff, 0x0f17bff, 0x0f17fbf]

/-- This literal list is definitionally equal to `Survivors.treeMasks`. -/
def treeMasks : List ℕ := [0x00f7fff, 0x00ff7ff, 0x103ffff, 0x10ffff6]

def routeCheck : Bool := Sq19.Cover.censusMasks.all fun m =>
  decide (Excluded m) || treeMasks.contains m || captureMasks.contains m

/-- One finite native check over the 22,475 census representatives. -/
theorem route_checked : routeCheck = true := by native_decide

theorem route (m : ℕ) (hm : m ∈ Sq19.Cover.censusMasks) :
    Excluded m ∨ m ∈ treeMasks ∨ m ∈ captureMasks := by
  have h := List.all_eq_true.mp route_checked m hm
  simpa only [Bool.or_eq_true, decide_eq_true_eq, List.contains_iff_mem, or_assoc] using h

/-- Pin the three names to their actual indices, rather than relying on comments. -/
theorem capture_indices :
    Sq19.Cover.censusMasks[3435]? = some 0x0f15fff ∧
    Sq19.Cover.censusMasks[3438]? = some 0x0f17bff ∧
    Sq19.Cover.censusMasks[3442]? = some 0x0f17fbf := by native_decide

end Sq19.Assembly.CensusRoute
