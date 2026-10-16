import Sq19Lean.Capture.StateFacts
import Sq19Lean.Capture.S3442.State
import Sq19Lean.Capture.S3435.State
import Sq19Lean.Capture.S3438.State

/-! Census to capture, per state: a packing at L <= side whose census mask is 3442, 3435 or 3438
(`Sq19.Cover.packing_reaches_census`) has, after the x reflection, the relabelling into owner order and the
translation by `-(sigma, sigma)`, poses in the state's targets (the hull box H in the state's frame). Needs all
pieces of the three states built (the State modules). -/
namespace Sq19.Capture
open Sq17.Propagation Sq17.Propagation.HalfPlaneState Sq17.Propagation.HalfPlaneState.CaptureSummary

theorem S3442.census_capture (L : ℝ) (hL : L ≤ S3442.side) (q u : Fin 19 → ℝ × ℝ) (c : Fin 19 → Fin 25)
    (hu : ∀ i, (u i).1^2+(u i).2^2 = 1)
    (hf : ∀ i, Sq17.sq (q i).1 (q i).2 (u i).1 (u i).2 ⊆ Sq19.Cover.frameBox L)
    (hd : ∀ i j, i ≠ j → Disjoint
      (interior (Sq17.sq (q i).1 (q i).2 (u i).1 (u i).2))
      (interior (Sq17.sq (q j).1 (q j).2 (u j).1 (u j).2)))
    (hcell : ∀ i, q i ∈ Sq19.Cover.cell (c i))
    (himg : Finset.univ.image c = Sq19.Cover.ofMask (Sq19.Cover.censusMasks.getD 3442 0)) :
    ∃ π : Fin 19 → Fin 19, Function.Injective π ∧ ∃ p : ℕ → AnglePose,
      (∀ j : Fin 19, (p j.val).center = Sq19.Cover.actG 1 (q (π j)) + (-(S3442.sigma:ℝ), -(S3442.sigma:ℝ)) ∧
        (p j.val).square = Sq17.sq (Sq19.Cover.actG 1 (q (π j)) + (-(S3442.sigma:ℝ), -(S3442.sigma:ℝ))).1
          (Sq19.Cover.actG 1 (q (π j)) + (-(S3442.sigma:ℝ), -(S3442.sigma:ℝ))).2
          (Sq19.Cover.dirG 1 (u (π j))).1 (Sq19.Cover.dirG 1 (u (π j))).2) ∧
      (∀ i : Fin 19, (S3442.P2.targets[i.val]!).Holds (p i.val)) ∧
      (∀ j : Fin 19, (p j.val).square ⊆ boxA ((2443/500 - L)/2 - S3442.sigma) L) ∧
      (∀ i j : Fin 19, i ≠ j → Disjoint (interior (p i.val).square) (interior (p j.val).square)) :=
  census_to_capture (rosterOf S3442.rosterNat) S3442.roster_inj S3442.sigma S3442.side S3442.shift S3442.cells
    S3442.cells_ok S3442.frame_lo S3442.frame_hi _ (fun c' u' h1 h2 h3 h4 => S3442.capture c' u' h1 h2 h3 h4)
    L hL 1 q u c hu hf hd hcell (img_of_mask _ _ S3442.mask_ok c himg)

theorem S3435.census_capture (L : ℝ) (hL : L ≤ S3435.side) (q u : Fin 19 → ℝ × ℝ) (c : Fin 19 → Fin 25)
    (hu : ∀ i, (u i).1^2+(u i).2^2 = 1)
    (hf : ∀ i, Sq17.sq (q i).1 (q i).2 (u i).1 (u i).2 ⊆ Sq19.Cover.frameBox L)
    (hd : ∀ i j, i ≠ j → Disjoint
      (interior (Sq17.sq (q i).1 (q i).2 (u i).1 (u i).2))
      (interior (Sq17.sq (q j).1 (q j).2 (u j).1 (u j).2)))
    (hcell : ∀ i, q i ∈ Sq19.Cover.cell (c i))
    (himg : Finset.univ.image c = Sq19.Cover.ofMask (Sq19.Cover.censusMasks.getD 3435 0)) :
    ∃ π : Fin 19 → Fin 19, Function.Injective π ∧ ∃ p : ℕ → AnglePose,
      (∀ j : Fin 19, (p j.val).center = Sq19.Cover.actG 1 (q (π j)) + (-(S3435.sigma:ℝ), -(S3435.sigma:ℝ)) ∧
        (p j.val).square = Sq17.sq (Sq19.Cover.actG 1 (q (π j)) + (-(S3435.sigma:ℝ), -(S3435.sigma:ℝ))).1
          (Sq19.Cover.actG 1 (q (π j)) + (-(S3435.sigma:ℝ), -(S3435.sigma:ℝ))).2
          (Sq19.Cover.dirG 1 (u (π j))).1 (Sq19.Cover.dirG 1 (u (π j))).2) ∧
      ((∀ i : Fin 19, (S3435.P0.targets[i.val]!).Holds (p i.val)) ∨ ∀ i : Fin 19, (S3435.P2.targets[i.val]!).Holds (p i.val)) ∧
      (∀ j : Fin 19, (p j.val).square ⊆ boxA ((2443/500 - L)/2 - S3435.sigma) L) ∧
      (∀ i j : Fin 19, i ≠ j → Disjoint (interior (p i.val).square) (interior (p j.val).square)) :=
  census_to_capture (rosterOf S3435.rosterNat) S3435.roster_inj S3435.sigma S3435.side S3435.shift S3435.cells
    S3435.cells_ok S3435.frame_lo S3435.frame_hi _ (fun c' u' h1 h2 h3 h4 => S3435.capture c' u' h1 h2 h3 h4)
    L hL 1 q u c hu hf hd hcell (img_of_mask _ _ S3435.mask_ok c himg)

theorem S3438.census_capture (L : ℝ) (hL : L ≤ S3438.side) (q u : Fin 19 → ℝ × ℝ) (c : Fin 19 → Fin 25)
    (hu : ∀ i, (u i).1^2+(u i).2^2 = 1)
    (hf : ∀ i, Sq17.sq (q i).1 (q i).2 (u i).1 (u i).2 ⊆ Sq19.Cover.frameBox L)
    (hd : ∀ i j, i ≠ j → Disjoint
      (interior (Sq17.sq (q i).1 (q i).2 (u i).1 (u i).2))
      (interior (Sq17.sq (q j).1 (q j).2 (u j).1 (u j).2)))
    (hcell : ∀ i, q i ∈ Sq19.Cover.cell (c i))
    (himg : Finset.univ.image c = Sq19.Cover.ofMask (Sq19.Cover.censusMasks.getD 3438 0)) :
    ∃ π : Fin 19 → Fin 19, Function.Injective π ∧ ∃ p : ℕ → AnglePose,
      (∀ j : Fin 19, (p j.val).center = Sq19.Cover.actG 1 (q (π j)) + (-(S3438.sigma:ℝ), -(S3438.sigma:ℝ)) ∧
        (p j.val).square = Sq17.sq (Sq19.Cover.actG 1 (q (π j)) + (-(S3438.sigma:ℝ), -(S3438.sigma:ℝ))).1
          (Sq19.Cover.actG 1 (q (π j)) + (-(S3438.sigma:ℝ), -(S3438.sigma:ℝ))).2
          (Sq19.Cover.dirG 1 (u (π j))).1 (Sq19.Cover.dirG 1 (u (π j))).2) ∧
      (∀ i : Fin 19, (S3438.P0.targets[i.val]!).Holds (p i.val)) ∧
      (∀ j : Fin 19, (p j.val).square ⊆ boxA ((2443/500 - L)/2 - S3438.sigma) L) ∧
      (∀ i j : Fin 19, i ≠ j → Disjoint (interior (p i.val).square) (interior (p j.val).square)) :=
  census_to_capture (rosterOf S3438.rosterNat) S3438.roster_inj S3438.sigma S3438.side S3438.shift S3438.cells
    S3438.cells_ok S3438.frame_lo S3438.frame_hi _ (fun c' u' h1 h2 h3 h4 => S3438.capture c' u' h1 h2 h3 h4)
    L hL 1 q u c hu hf hd hcell (img_of_mask _ _ S3438.mask_ok c himg)

end Sq19.Capture

#print axioms Sq19.Capture.S3442.census_capture
#print axioms Sq19.Capture.S3435.census_capture
#print axioms Sq19.Capture.S3438.census_capture
