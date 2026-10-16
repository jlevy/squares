import Sq19Lean.Capture.Final
import Sq19Lean.Endgame.CertifiedHull

/-! The `hcap` hypothesis of `Sq19.Assembly.side19_le_of_routes`, per capture state: a packing below `side19`
whose census mask is the state's is impossible (census output, capture, the step into `Hull.prob`, then
`Sq19.Endgame.Reduction.side19_le_of_hull`). State 3435's piece P0 goes through the mirror (`S3435.mirror`). -/
namespace Sq19.Capture
open Sq17.Propagation Sq17.Propagation.HalfPlaneState Sq19.Milp

theorem S3442.hcap : ∀ L : ℝ, L < Sq19.side19 →
    ∀ (q u : Fin 19 → ℝ × ℝ) (c : Fin 19 → Fin 25),
    (∀ i, (u i).1^2+(u i).2^2 = 1) →
    (∀ i, Sq17.sq (q i).1 (q i).2 (u i).1 (u i).2 ⊆ Sq19.Cover.frameBox L) →
    (∀ i j, i ≠ j → Disjoint
      (interior (Sq17.sq (q i).1 (q i).2 (u i).1 (u i).2))
      (interior (Sq17.sq (q j).1 (q j).2 (u j).1 (u j).2))) →
    (∀ i, q i ∈ Sq19.Cover.cell (c i)) →
    Finset.univ.image c = Sq19.Cover.ofMask (Sq19.Cover.censusMasks.getD 3442 0) → False := by
  intro L hL q u c hu hf hd hcell himg
  obtain ⟨θ, dx, dy, hg⟩ := S3442.good L (le_trans hL.le side19_lt_side.le) ⟨q, u, c, hu, hf, hd, hcell, himg⟩
  exact absurd (Sq19.Endgame.Reduction.side19_le_of_hull hg) (not_le.mpr hL)

theorem S3438.hcap : ∀ L : ℝ, L < Sq19.side19 →
    ∀ (q u : Fin 19 → ℝ × ℝ) (c : Fin 19 → Fin 25),
    (∀ i, (u i).1^2+(u i).2^2 = 1) →
    (∀ i, Sq17.sq (q i).1 (q i).2 (u i).1 (u i).2 ⊆ Sq19.Cover.frameBox L) →
    (∀ i j, i ≠ j → Disjoint
      (interior (Sq17.sq (q i).1 (q i).2 (u i).1 (u i).2))
      (interior (Sq17.sq (q j).1 (q j).2 (u j).1 (u j).2))) →
    (∀ i, q i ∈ Sq19.Cover.cell (c i)) →
    Finset.univ.image c = Sq19.Cover.ofMask (Sq19.Cover.censusMasks.getD 3438 0) → False := by
  intro L hL q u c hu hf hd hcell himg
  obtain ⟨θ, dx, dy, hg⟩ := S3438.good L (by rw [sides_eq.2]; exact le_trans hL.le side19_lt_side.le)
    ⟨q, u, c, hu, hf, hd, hcell, himg⟩
  exact absurd (Sq19.Endgame.Reduction.side19_le_of_hull hg) (not_le.mpr hL)

theorem S3435.hcap_of_mirror
    (hmirror : ∀ (L : ℝ) (p : ℕ → AnglePose), (∀ i : Fin 19, (S3435.P0.targets[i.val]!).Holds (p i.val)) →
      (∀ j : Fin 19, (p j.val).square ⊆ boxA ((2443/500 - L)/2 - S3435.sigma) L) →
      (∀ i j : Fin 19, i ≠ j → Disjoint (interior (p i.val).square) (interior (p j.val).square)) →
      ∃ θ dx dy : ℕ → ℝ, Good Endgame.Hull.prob θ dx dy L) :
    ∀ L : ℝ, L < Sq19.side19 →
    ∀ (q u : Fin 19 → ℝ × ℝ) (c : Fin 19 → Fin 25),
    (∀ i, (u i).1^2+(u i).2^2 = 1) →
    (∀ i, Sq17.sq (q i).1 (q i).2 (u i).1 (u i).2 ⊆ Sq19.Cover.frameBox L) →
    (∀ i j, i ≠ j → Disjoint
      (interior (Sq17.sq (q i).1 (q i).2 (u i).1 (u i).2))
      (interior (Sq17.sq (q j).1 (q j).2 (u j).1 (u j).2))) →
    (∀ i, q i ∈ Sq19.Cover.cell (c i)) →
    Finset.univ.image c = Sq19.Cover.ofMask (Sq19.Cover.censusMasks.getD 3435 0) → False := by
  intro L hL q u c hu hf hd hcell himg
  obtain ⟨θ, dx, dy, hg⟩ := S3435.good L (by rw [sides_eq.1]; exact le_trans hL.le side19_lt_side.le)
    ⟨q, u, c, hu, hf, hd, hcell, himg⟩ (hmirror L)
  exact absurd (Sq19.Endgame.Reduction.side19_le_of_hull hg) (not_le.mpr hL)

theorem S3435.hcap : ∀ L : ℝ, L < Sq19.side19 →
    ∀ (q u : Fin 19 → ℝ × ℝ) (c : Fin 19 → Fin 25),
    (∀ i, (u i).1^2+(u i).2^2 = 1) →
    (∀ i, Sq17.sq (q i).1 (q i).2 (u i).1 (u i).2 ⊆ Sq19.Cover.frameBox L) →
    (∀ i j, i ≠ j → Disjoint
      (interior (Sq17.sq (q i).1 (q i).2 (u i).1 (u i).2))
      (interior (Sq17.sq (q j).1 (q j).2 (u j).1 (u j).2))) →
    (∀ i, q i ∈ Sq19.Cover.cell (c i)) →
    Finset.univ.image c = Sq19.Cover.ofMask (Sq19.Cover.censusMasks.getD 3435 0) → False := by
  intro L hL q u c hu hf hd hcell himg
  have hLs : L ≤ S3435.side := by rw [sides_eq.1]; exact le_trans hL.le side19_lt_side.le
  obtain ⟨θ, dx, dy, hg⟩ := S3435.good L hLs ⟨q, u, c, hu, hf, hd, hcell, himg⟩
    (fun p hT hbox hdis => S3435.mirror L hLs p hT hbox hdis)
  exact absurd (Sq19.Endgame.Reduction.side19_le_of_hull hg) (not_le.mpr hL)

end Sq19.Capture

#print axioms Sq19.Capture.S3442.hcap
#print axioms Sq19.Capture.S3438.hcap
#print axioms Sq19.Capture.S3435.hcap
