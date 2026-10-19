import Sq17Lean.HalfPlaneTree
import Sq17Lean.SquareSupportSeparation

/-! A feasible two-square control using the production table, named-cell seed,
state checker, roster wrapper and branch-tree wrapper. All finite checks use
kernel reduction. The centres are actual vertices of named cells 0 and 1. -/
namespace Sq17.Propagation.HalfPlaneState.PositiveControl
open HalfPlaneInt

set_option maxRecDepth 100000
set_option maxHeartbeats 0

def table : Array Entry := #[
  ⟨-1, 0, 1, -1, 1, 1, 4, 0⟩,
  ⟨0, 1, 1, 1, 1, 1, 4, 0⟩]

def atNeg : TrigBounds := ⟨1/2, 3/5, -9/10, -4/5⟩
def atZero : TrigBounds := ⟨1, 1, 0, 0⟩
def atPos : TrigBounds := ⟨1/2, 3/5, 4/5, 9/10⟩
def bounds : Array (TrigBounds × TrigBounds) := #[(atNeg, atZero), (atZero, atPos)]

def initial : HState := [[mkRow [] 0, mkRow [] 1], [mkRow [] 0, mkRow [] 1]]
def roster : Fin 2 → Fin 24 := ![0, 1]

theorem table_checked : tableOK 44 table bounds = true := by decide +kernel
theorem seed_checked : stateSeedOK table (-initialAngleRadius) initialAngleRadius
    (rosterCells 0 (List.ofFn roster)) initial = true := by decide +kernel

/-- Enforce the four legal centre walls of the side-5 box on every initial row. -/
def walls : List IC := [⟨-2, 0, -1⟩, ⟨2, 0, 9⟩, ⟨0, -2, -1⟩, ⟨0, 2, 9⟩]
def steps : List Step := [.wall 0 0 walls 0, .wall 0 1 walls 0,
  .wall 1 0 walls 0, .wall 1 1 walls 0]
def finalState : HState := (runAll table 5 0 initial steps).getD []

theorem walls_accepted : (runAll table 5 0 initial steps).isSome = true := by decide +kernel
theorem walls_do_not_exclude : excludes table 5 0 2 initial steps = false := by decide +kernel
theorem false_kill_rejected : ((Step.kill 0 0 1).run table 5 0 finalState).isNone = true := by
  decide +kernel
theorem false_dead_rejected : ((Step.dead 0 0).run table 5 0 finalState).isNone = true := by
  decide +kernel
theorem false_wall_rejected :
    ((Step.wall 0 0 [⟨1, 0, 0⟩] 0).run table 5 0 finalState).isNone = true := by
  decide +kernel
theorem self_kill_rejected : ((Step.kill 0 0 0).run table 5 0 finalState).isNone = true := by
  decide +kernel
theorem missing_partner_rejected : ((Step.kill 0 0 2).run table 5 0 finalState).isNone = true := by
  decide +kernel
theorem false_cut_rejected : ((Step.cut 0 0 1 ⟨1, 0, 0⟩ 0).run table 5 0 finalState).isNone = true := by
  decide +kernel
theorem missing_angle_coverage_rejected :
    ((Step.split 0 0 1 1).run table 5 0 finalState).isNone = true := by decide +kernel

def forgedBoxState : HState :=
  [[⟨[], ⟨some (-1, 1), none, none, none⟩, 0⟩, mkRow [] 1], [mkRow [] 0, mkRow [] 1]]
theorem forged_cache_seed_rejected : stateSeedOK table (-initialAngleRadius) initialAngleRadius
    (rosterCells 0 (List.ofFn roster)) forgedBoxState = false := by decide +kernel
theorem missing_entry_seed_rejected : stateSeedOK table (-initialAngleRadius) initialAngleRadius
    (rosterCells 0 (List.ofFn roster)) [[mkRow [] 99], [mkRow [] 99]] = false := by
  decide +kernel

/-- A deliberately misused raw Boolean can count an absent third owner as empty.
The production wrapper's `S.length = n` premise rules out exactly this misuse. -/
theorem raw_wrong_owner_count : excludes table 5 0 3 initial [] = true := by decide +kernel

noncomputable section
def centres : Fin 2 → ℝ × ℝ := ![(1/2, 1/2), (1693/500, 1/2)]
def directions : Fin 2 → ℝ × ℝ := fun _ => (1, 0)

theorem unit (i : Fin 2) : (directions i).1^2 + (directions i).2^2 = 1 := by
  norm_num [directions]

theorem centres_in_cells (i : Fin 2) :
    centres i ∈ CenteredOrbitFrame.shift (-(0:ℝ)) '' ExactCells.cell (roster i) := by
  refine ⟨centres i, ?_, by simp [CenteredOrbitFrame.shift]⟩
  change centres i ∈ convexHull ℝ (realPoint '' {v | v ∈ ExactCells.vertices (roster i)})
  apply subset_convexHull
  fin_cases i
  · refine ⟨((1/2:ℚ), (1/2:ℚ)), ?_, ?_⟩
    · simp [roster, ExactCells.vertices]
    · norm_num [centres, realPoint]
  · refine ⟨((1693/500:ℚ), (1/2:ℚ)), ?_, ?_⟩
    · simp [roster, ExactCells.vertices]
    · norm_num [centres, realPoint]

theorem separated : Disjoint
    (interior (Sq17.sq (centres 0).1 (centres 0).2 1 0))
    (interior (Sq17.sq (centres 1).1 (centres 1).2 1 0)) := by
  apply WallCapacity.support_gap_disjoint (centres 0) (centres 1) 1 0 1 0 1 0
  all_goals norm_num [centres, WallCapacity.squareSupport]

theorem disjoint (i j : Fin 2) (hij : i ≠ j) : Disjoint
    (interior (Sq17.sq (centres i).1 (centres i).2 (directions i).1 (directions i).2))
    (interior (Sq17.sq (centres j).1 (centres j).2 (directions j).1 (directions j).2)) := by
  fin_cases i <;> fin_cases j
  · exact (hij rfl).elim
  · exact separated
  · exact separated.symm
  · exact (hij rfl).elim

theorem fits (i : Fin 2) :
    Sq17.sq (centres i).1 (centres i).2 (directions i).1 (directions i).2 ⊆ traceContainer 5 0 := by
  change Sq17.sq (centres i).1 (centres i).2 1 0 ⊆ _
  have h := WallCapacity.support_walls_contained (centres i) 1 0 5
    (by norm_num) (by fin_cases i <;> norm_num [centres, WallCapacity.squareSupport])
    (by fin_cases i <;> norm_num [centres, WallCapacity.squareSupport])
    (by fin_cases i <;> norm_num [centres, WallCapacity.squareSupport])
    (by fin_cases i <;> norm_num [centres, WallCapacity.squareSupport])
  simpa only [traceContainer, neg_zero, add_zero] using h

theorem represented_packing : ∃ p : ℕ → AnglePose,
    Rep table initial p ∧ Packing 2 p ∧ Fits 2 5 0 p := by
  obtain ⟨p, hr, hs⟩ := roster_represented table 0 2 roster initial seed_checked rfl
    centres directions unit (by simpa using centres_in_cells)
  refine ⟨p, hr, ?_, ?_⟩
  · intro i j hi hj hij
    rw [hs ⟨i, hi⟩, hs ⟨j, hj⟩]
    exact disjoint _ _ (fun he => hij (congrArg Fin.val he))
  · intro i hi
    rw [hs ⟨i, hi⟩]
    simpa using fits ⟨i, hi⟩

/-- For this explicit feasible packing, *no* step list can yield accepted exclusion
through the production roster wrapper. This is stronger than testing one trace. -/
theorem no_false_exclusion (trace : List Step) : excludes table 5 0 2 initial trace = false := by
  cases h : excludes table 5 0 2 initial trace with
  | false => rfl
  | true =>
    exact (roster_excluded table bounds 5 0 0 2 roster initial trace table_checked
      seed_checked rfl h centres directions unit (by simpa using centres_in_cells)
      disjoint (by simpa using fits)).elim

/-- The same geometry prevents a branch-tree exclusion certificate. -/
theorem no_false_tree : ¬ BranchComposition.Excluded table initial 5 0 := by
  intro h
  exact tree_excluded table 5 0 0 2 roster initial seed_checked rfl h
    centres directions unit (by simpa using centres_in_cells) disjoint (by simpa using fits)

end
end Sq17.Propagation.HalfPlaneState.PositiveControl

#print axioms Sq17.Propagation.HalfPlaneState.PositiveControl.no_false_exclusion
#print axioms Sq17.Propagation.HalfPlaneState.PositiveControl.no_false_tree
#print axioms Sq17.Propagation.HalfPlaneState.PositiveControl.represented_packing
