import Sq17Lean.CaptureSummaryFast

/-! Core-only, any number of owners: the 17 project's terminal summary check
(`Sq17Lean/CaptureSummaryFast.lean`, stated there for 17 owners), and a run followed by that check. -/
namespace Sq19.Capture
open Sq17.Propagation.HalfPlaneState Sq17.Propagation.HalfPlaneInt
open Sq17.Propagation.HalfPlaneState.CaptureSummary

/-- Every live row of every owner `i < n` lies inside `targets[i]` (angle interval and half-planes). -/
def summaryCheckN (n : Nat) (T : Array Entry) (S : HState) (targets : Array Target) : Bool :=
  decide (S.length = n ∧ targets.size = n) &&
    (List.range n).all fun i => (rowsOf S i).all (rowCheck T targets[i]!)

/-- The trace is accepted and its final state passes the summary check. -/
def runSummary (n : Nat) (T : Array Entry) (side shift : Rat) (S : HState) (steps : List Step)
    (targets : Array Target) : Bool :=
  match runAll T side shift S steps with
  | some E => summaryCheckN n T E targets
  | none => false

end Sq19.Capture
