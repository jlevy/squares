import Sq19Lean.Capture.S3438.P0

/-! State 3438 (representative pose s19/data/capture/poses/orbit3438_11to_side1-1.txt, census cells shifted by
-sigma, side side19 + 1e-12). One piece, no split: P0 is captured into `P0.targets`, the hull box H
(s19/data/capture/coarse/hull2_box.txt) in this state's frame (s19/tools/captarget.py, g = 0, owner matching of
s19/data/capture/match_S3438.txt, a relabel.awk output). -/
namespace Sq19.Capture.S3438
open Sq17.Propagation Sq17.Propagation.HalfPlaneState Sq17.Propagation.HalfPlaneState.CaptureSummary Sq19.Capture

def widthCheck : Bool := (List.range 19).all fun i => decide (halfPiUpper ≤ (base i).2 - (base i).1)

theorem width_checked : widthCheck = true := by native_decide

theorem base_width : ∀ i, i < 19 → Real.pi/2 ≤ ((base i).2:ℝ) - ((base i).1:ℝ) := by
  intro i hi
  have h := of_decide_eq_true (List.all_eq_true.mp width_checked i (List.mem_range.mpr hi))
  have := half_pi_le _ h
  push_cast at this
  exact this

/-- The one piece is the base window. -/
def tileCheck : Bool := decide (splitOwner = 12 ∧ (base 12).1 = P0.pieceLo ∧ P0.pieceHi = (base 12).2)

theorem tile_checked : tileCheck = true := by native_decide

/-- Every family of 19 unit squares of state 3438 inside the trace container has poses in the targets. -/
theorem capture (c u : ℕ → ℝ × ℝ)
    (hunit : ∀ i, i < 19 → (u i).1^2+(u i).2^2 = 1)
    (hcenter : ∀ i, i < 19 → c i ∈ convexHull ℝ (realPoint '' {v | v ∈ cells.getD i []}))
    (hd : ∀ i j, i < 19 → j < 19 → i ≠ j → Disjoint
      (interior (Sq17.sq (c i).1 (c i).2 (u i).1 (u i).2))
      (interior (Sq17.sq (c j).1 (c j).2 (u j).1 (u j).2)))
    (hfit : ∀ i, i < 19 → Sq17.sq (c i).1 (c i).2 (u i).1 (u i).2 ⊆ traceContainer side shift) :
    ∃ p : ℕ → AnglePose,
      (∀ i, i < 19 → (p i).center = c i ∧ (p i).square = Sq17.sq (c i).1 (c i).2 (u i).1 (u i).2) ∧
      ∀ i : Fin 19, (P0.targets[i.val]!).Holds (p i.val) := by
  obtain ⟨hso, hb0, hb1⟩ := of_decide_eq_true tile_checked
  obtain ⟨p, hp⟩ := config_poses 19 base base_width c u hunit
  have hpack : Packing 19 p := by
    intro i j hi hj hij
    rw [(hp i hi).2.2, (hp j hj).2.2]
    exact hd i j hi hj hij
  have hfit' : Fits 19 side shift p := by
    intro i hi
    rw [(hp i hi).2.2]
    exact hfit i hi
  refine ⟨p, fun i hi => ⟨(hp i hi).1, (hp i hi).2.2⟩, P0.captured p ⟨fun i hi => (hp i hi).1 ▸ hcenter i hi,
    fun i hi => ?_, hpack, hfit'⟩⟩
  unfold P0.windows setWindow
  split_ifs with h
  · have := (hp i hi).2.1
    rw [h, hso] at this ⊢
    rw [← hb0, hb1]
    exact this
  · exact (hp i hi).2.1

end Sq19.Capture.S3438

#print axioms Sq19.Capture.S3438.capture
