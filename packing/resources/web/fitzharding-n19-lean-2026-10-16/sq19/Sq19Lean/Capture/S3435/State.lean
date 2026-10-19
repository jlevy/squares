import Sq19Lean.Capture.S3435.P0
import Sq19Lean.Capture.S3435.P1
import Sq19Lean.Capture.S3435.P2
import Sq19Lean.Capture.S3435.P3

/-! State 3435, the record's census state (pose s19/data/capture/poses/state3435.txt, census cells shifted by -sigma,
side side19 + 1e-12). Owner 12 (square 13) has the base window `base 12`, cut into four pieces at relative angles
-3.5, -0.5 and 0.5 degrees (dyadic cut points). P1 and P3 are excluded. P2 (|a13| <= 0.5 deg) is captured into
`P2.targets`, the hull box H (s19/data/capture/coarse/hull2_box.txt) in this state's frame (s19/tools/captarget.py,
g = 0); P0 (a13 <= -3.5 deg) into `P0.targets`, H through the anti-diagonal mirror (g = 5). -/
namespace Sq19.Capture.S3435
open Sq17.Propagation Sq17.Propagation.HalfPlaneState Sq17.Propagation.HalfPlaneState.CaptureSummary Sq19.Capture

def widthCheck : Bool := (List.range 19).all fun i => decide (halfPiUpper ≤ (base i).2 - (base i).1)

theorem width_checked : widthCheck = true := by native_decide

theorem base_width : ∀ i, i < 19 → Real.pi/2 ≤ ((base i).2:ℝ) - ((base i).1:ℝ) := by
  intro i hi
  have h := of_decide_eq_true (List.all_eq_true.mp width_checked i (List.mem_range.mpr hi))
  have := half_pi_le _ h
  push_cast at this
  exact this

/-- The pieces tile owner 12's base window. -/
def tileCheck : Bool :=
  decide (splitOwner = 12 ∧ (base 12).1 = P0.pieceLo ∧ P0.pieceHi = P1.pieceLo ∧ P1.pieceHi = P2.pieceLo ∧
    P2.pieceHi = P3.pieceLo ∧ P3.pieceHi = (base 12).2)

theorem tile_checked : tileCheck = true := by native_decide

/-- Every family of 19 unit squares of state 3435 inside the trace container has poses in one of the two targets. -/
theorem capture (c u : ℕ → ℝ × ℝ)
    (hunit : ∀ i, i < 19 → (u i).1^2+(u i).2^2 = 1)
    (hcenter : ∀ i, i < 19 → c i ∈ convexHull ℝ (realPoint '' {v | v ∈ cells.getD i []}))
    (hd : ∀ i j, i < 19 → j < 19 → i ≠ j → Disjoint
      (interior (Sq17.sq (c i).1 (c i).2 (u i).1 (u i).2))
      (interior (Sq17.sq (c j).1 (c j).2 (u j).1 (u j).2)))
    (hfit : ∀ i, i < 19 → Sq17.sq (c i).1 (c i).2 (u i).1 (u i).2 ⊆ traceContainer side shift) :
    ∃ p : ℕ → AnglePose,
      (∀ i, i < 19 → (p i).center = c i ∧ (p i).square = Sq17.sq (c i).1 (c i).2 (u i).1 (u i).2) ∧
      ((∀ i : Fin 19, (P0.targets[i.val]!).Holds (p i.val)) ∨
        ∀ i : Fin 19, (P2.targets[i.val]!).Holds (p i.val)) := by
  have ht := of_decide_eq_true tile_checked
  obtain ⟨hso, hb0, h01, h12, h23, hb3⟩ := ht
  obtain ⟨p, hp⟩ := config_poses 19 base base_width c u hunit
  have hpack : Packing 19 p := by
    intro i j hi hj hij
    rw [(hp i hi).2.2, (hp j hj).2.2]
    exact hd i j hi hj hij
  have hfit' : Fits 19 side shift p := by
    intro i hi
    rw [(hp i hi).2.2]
    exact hfit i hi
  have adm : ∀ a b : ℚ, (p 12).angle ∈ Set.Icc (a:ℝ) (b:ℝ) →
      Admissible 19 side shift (setWindow base splitOwner (a, b)) cells p := by
    intro a b hab
    refine ⟨fun i hi => (hp i hi).1 ▸ hcenter i hi, fun i hi => ?_, hpack, hfit'⟩
    unfold setWindow
    split_ifs with h
    · rw [h, hso]; exact hab
    · exact (hp i hi).2.1
  refine ⟨p, fun i hi => ⟨(hp i hi).1, (hp i hi).2.2⟩, ?_⟩
  obtain ⟨hlo, hhi⟩ := (hp 12 (by norm_num)).2.1
  rw [hb0] at hlo
  rw [← hb3] at hhi
  rcases le_total (p 12).angle (P0.pieceHi:ℝ) with g0 | g0
  · exact Or.inl (P0.captured p (adm _ _ ⟨hlo, g0⟩))
  rw [h01] at g0
  rcases le_total (p 12).angle (P1.pieceHi:ℝ) with g1 | g1
  · exact (P1.excluded_piece p (adm _ _ ⟨g0, g1⟩)).elim
  rw [h12] at g1
  rcases le_total (p 12).angle (P2.pieceHi:ℝ) with g2 | g2
  · exact Or.inr (P2.captured p (adm _ _ ⟨g1, g2⟩))
  rw [h23] at g2
  exact (P3.excluded_piece p (adm _ _ ⟨g2, hhi⟩)).elim

end Sq19.Capture.S3435

#print axioms Sq19.Capture.S3435.capture
