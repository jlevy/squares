import Sq19Lean.Endgame.AngleReduction
import Sq19Lean.Endgame.ExactRowsOnH

/-! Concrete row expressions and signed-prefix directions for the local endgame.
The five relevant axis angles are 1, 2, 5, 8, 10. Square 7 and the 7–8 owner do
not occur in the F1 bound. The 5–8 relative-angle sign is derived from the two
orthant bits and the magnitude order, rather than guessed independently.
-/
namespace Sq19.Endgame.Reduction
open Sq19.Milp

structure Case where
  pa : Bool
  qa : Bool
  owner12 : Bool
  owner58 : Bool
  b1 : Bool
  b2 : Bool
  b5 : Bool
  b8 : Bool
  b10 : Bool
  fiveLarger : Bool
  pd : Bool
  qd : Bool
  deriving Repr, DecidableEq

/-- Bit encoding of the 4096 expression/cone cases. Some encodings deliberately
repeat expressions when an irrelevant endpoint or ordering bit is ignored. -/
def Case.ofNat (n : ℕ) : Case :=
  let bit := fun k => (n / 2^k) % 2 == 1
  ⟨bit 0, bit 1, bit 2, bit 3, bit 4, bit 5,
   bit 6, bit 7, bit 8, bit 9, bit 10, bit 11⟩

/-- Sign of θ8−θ5 on this signed magnitude-order cone. -/
def Case.bd58 (c : Case) : Bool :=
  if c.b5 == c.b8 then (if c.fiveLarger then !c.b8 else c.b8) else c.b8

/-- The derived relative-angle sign is correct, including ties and zeros. -/
theorem Case.relative_sign (c : Case) {g5 g8 : ℝ}
    (h5 : 0 ≤ (sg c.b5 : ℝ) * g5) (h8 : 0 ≤ (sg c.b8 : ℝ) * g8)
    (horder : if c.fiveLarger then |g8| ≤ |g5| else |g5| ≤ |g8|) :
    0 ≤ (sg c.bd58 : ℝ) * (g8-g5) := by
  cases hb5 : c.b5 <;> cases hb8 : c.b8 <;> cases hord : c.fiveLarger <;>
    simp_all [Case.bd58, sg, abs_of_nonneg, abs_of_nonpos] <;> linarith

def Case.j12 (c : Case) : ℕ := if c.owner12 then 2 else 1
def Case.j58 (c : Case) : ℕ := if c.owner58 then 8 else 5
def Case.other58 (c : Case) : ℕ := if c.owner58 then 5 else 8

def Case.P (c : Case) : RowE :=
  let Y := if (if c.owner12 then c.b2 else c.b1) then dY12.hi else dY12.lo
  if c.pa then ProwA c.j12 Y (if c.pd then tightOffPIv.lo else tightOffPIv.hi) (σPa c.b1 c.b2)
  else ProwB c.j12 (if c.owner12 then 1 else 2) Y (σPb c.b1 c.b2)

def Case.Q (c : Case) : RowE :=
  if c.qa then QrowA (if c.qd then tightOffQIv.lo else tightOffQIv.hi) (σQa c.b10)
  else QrowB (σQb c.b10)

def Case.F (c : Case) : RowE :=
  if c.b8 then
    if c.owner58 then F1rowPos8 (absX 2).hi (sg c.b5, 1) (1, 1) (anchor58E c.bd58)
    else F1rowPos5 (if c.b5 then (absX 2).hi else (absX 2).lo)
      (if c.bd58 then (absX 4).hi else (absX 4).lo)
      (if c.bd58 == c.b5 then (absY 4).hi else (absY 4).lo)
      (sg c.b5, 1) (1, 1) (anchor58E c.bd58)
  else F1rowNeg c.j58 c.other58
    (if (if c.owner58 then c.b8 else c.b5) then dX58.lo else dX58.hi)
    dX813.hi (sg c.b5, 1) (1, 1) (anchor58E c.bd58)

def Case.margin (c : Case) : Ex := endpointMargin c.P c.Q c.F

/-- A single signed coordinate direction. -/
def coordinate (k : ℕ) (b : Bool) : ℕ → ℚ :=
  fun j => if j == k then sg b else 0

/-- Prefixes of the order |θ5| ≥ |θ8|, or its reverse. -/
def Case.directions (c : Case) : List (ℕ → ℚ) :=
  [coordinate 1 c.b1, coordinate 2 c.b2, coordinate 10 c.b10,
   if c.fiveLarger then coordinate 5 c.b5 else coordinate 8 c.b8,
   fun j => coordinate 5 c.b5 j + coordinate 8 c.b8 j]

def table : Trig := boxTrig Hull.prob.rootAng
def radii : ℕ → ℚ := boxH Hull.prob.rootAng

def range (e : Ex) : Iv := (e.tf table radii).range radii

/-- Positive row-combination denominator and nonnegative Farkas weights. -/
def geometryCheck (c : Case) : Bool :=
  decide (0 ≤ (range (lam1 c.P c.Q c.F)).lo) &&
  decide (0 ≤ (range (lam2 c.P c.Q c.F)).lo) &&
  decide (0 ≤ (range (lam3 c.P c.Q c.F)).lo) &&
  decide (0 < (range (S1E c.P c.Q c.F)).lo)

/-- Every Taylor range used by the checker encloses its expression on H. -/
theorem mem_range (e : Ex) {θ : ℕ → ℝ}
    (hθ : InAng θ Hull.prob.rootAng) : Iv.mem (e.real θ) (range e) := by
  have h := TF.mem_range (Ex.tf_encl (boxTrig_valid Hull.prob.rootAng) radii e)
    (fun j => θ j - table.cen j) (boxH_bound hθ)
  have he : (fun s => ((boxTrig Hull.prob.rootAng).cen s : ℝ) + (θ s - table.cen s)) = θ := by
    funext s; dsimp [table]; ring
  rw [he] at h
  exact h

theorem geometry_sound (c : Case) (hcheck : geometryCheck c = true)
    {θ : ℕ → ℝ} (hθ : InAng θ Hull.prob.rootAng) :
    0 ≤ (lam1 c.P c.Q c.F).real θ ∧
    0 ≤ (lam2 c.P c.Q c.F).real θ ∧
    0 ≤ (lam3 c.P c.Q c.F).real θ ∧
    0 < (S1E c.P c.Q c.F).real θ := by
  simp only [geometryCheck, Bool.and_eq_true, decide_eq_true_eq] at hcheck
  rcases hcheck with ⟨⟨⟨h1, h2⟩, h3⟩, h4⟩
  have r1 : (0 : ℝ) ≤ ((range (lam1 c.P c.Q c.F)).lo : ℝ) := by exact_mod_cast h1
  have r2 : (0 : ℝ) ≤ ((range (lam2 c.P c.Q c.F)).lo : ℝ) := by exact_mod_cast h2
  have r3 : (0 : ℝ) ≤ ((range (lam3 c.P c.Q c.F)).lo : ℝ) := by exact_mod_cast h3
  have r4 : (0 : ℝ) < ((range (S1E c.P c.Q c.F)).lo : ℝ) := by exact_mod_cast h4
  exact ⟨r1.trans (mem_range _ hθ).1, r2.trans (mem_range _ hθ).1,
    r3.trans (mem_range _ hθ).1, r4.trans_le (mem_range _ hθ).1⟩

/-- Whole-H derivative check; a failed check calls for subdividing the box,
not for weakening the theorem. -/
def slopeCheck (c : Case) : Bool :=
  c.directions.all (fun v => c.margin.alongNonneg table radii v)

def check (c : Case) : Bool := geometryCheck c && slopeCheck c

def checkNat (n : ℕ) : Bool := check (Case.ofNat n)

/-- An accepted family member gives a sound increase on each listed prefix
whose endpoints stay in H. This theorem does not assume any numerical result. -/
theorem step_mono (c : Case) (h : slopeCheck c = true)
    (v : ℕ → ℚ) (hv : v ∈ c.directions) (θ : ℕ → ℝ) {u w : ℝ}
    (huw : u ≤ w)
    (hu : ∀ j, |angleLine θ v u j - table.cen j| ≤ radii j)
    (hw : ∀ j, |angleLine θ v w j - table.cen j| ≤ radii j) :
    c.margin.real (angleLine θ v u) ≤ c.margin.real (angleLine θ v w) := by
  have hc : c.margin.alongNonneg table radii v = true :=
    (List.all_eq_true.mp h) v hv
  exact Ex.along_step_mono (boxTrig_valid _) radii c.margin v θ hc huw
    (angleLine_box_of_endpoints θ v _ radii hu hw)

end Sq19.Endgame.Reduction

#print axioms Sq19.Endgame.Reduction.step_mono

#print axioms Sq19.Endgame.Reduction.geometry_sound
