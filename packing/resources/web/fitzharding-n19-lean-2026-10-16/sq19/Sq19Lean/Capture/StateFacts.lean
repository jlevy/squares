import Sq19Lean.Capture.CensusLink
import Sq19Lean.Capture.S3442.Common
import Sq19Lean.Capture.S3435.Common
import Sq19Lean.Capture.S3438.Common

/-! Finite facts linking each capture state to its census mask (inputs of `census_to_capture`): the roster is
injective, the capture cells are the census vertices shifted by `-sigma`, the frame inequalities hold, and the
symmetry 1 (x reflection, an involution) maps the roster into census mask 3435, 3438, 3442 respectively, the
census orbit representatives of these states. -/
namespace Sq19.Capture
open Sq17.Propagation

def rosterOf (l : List ℕ) (j : Fin 19) : Fin 25 := ⟨l.getD j 0 % 25, Nat.mod_lt _ (by norm_num)⟩

theorem perm1_invol : ∀ x : Fin 25, Sq19.Cover.perm 1 (Sq19.Cover.perm 1 x) = x := by decide

/-- From the census assignment of mask `m` to the roster: every roster cell is the image of an assigned cell. -/
theorem img_of_mask (r : Fin 19 → Fin 25) (m : ℕ) (hm : ∀ j, m.testBit (Sq19.Cover.perm 1 (r j)) = true)
    (c : Fin 19 → Fin 25) (himg : Finset.univ.image c = Sq19.Cover.ofMask m) :
    ∀ j, ∃ i, Sq19.Cover.perm 1 (c i) = r j := by
  intro j
  have : Sq19.Cover.perm 1 (r j) ∈ Finset.univ.image c := by
    rw [himg]; simp [Sq19.Cover.ofMask, hm j]
  obtain ⟨i, -, hi⟩ := Finset.mem_image.mp this
  exact ⟨i, by rw [hi, perm1_invol]⟩

namespace S3442
theorem roster_inj : Function.Injective (rosterOf rosterNat) := by decide
theorem cells_ok : ∀ j : Fin 19, cells.getD j [] = (Sq19.Census.vertices (rosterOf rosterNat j)).map (shiftVertex sigma) := by
  native_decide
theorem frame_lo : (2443/500 : ℝ) - 2 * (sigma:ℝ) ≤ side + 2 * shift := by norm_num [side, sigma, shift]
theorem frame_hi : (side : ℝ) ≤ 2443/500 - 2 * sigma + 2 * shift := by norm_num [side, sigma, shift]
theorem mask_ok : ∀ j, (Sq19.Cover.censusMasks.getD 3442 0).testBit (Sq19.Cover.perm 1 (rosterOf rosterNat j)) = true := by
  native_decide
end S3442

namespace S3435
theorem roster_inj : Function.Injective (rosterOf rosterNat) := by decide
theorem cells_ok : ∀ j : Fin 19, cells.getD j [] = (Sq19.Census.vertices (rosterOf rosterNat j)).map (shiftVertex sigma) := by
  native_decide
theorem frame_lo : (2443/500 : ℝ) - 2 * (sigma:ℝ) ≤ side + 2 * shift := by norm_num [side, sigma, shift]
theorem frame_hi : (side : ℝ) ≤ 2443/500 - 2 * sigma + 2 * shift := by norm_num [side, sigma, shift]
theorem mask_ok : ∀ j, (Sq19.Cover.censusMasks.getD 3435 0).testBit (Sq19.Cover.perm 1 (rosterOf rosterNat j)) = true := by
  native_decide
end S3435

namespace S3438
theorem roster_inj : Function.Injective (rosterOf rosterNat) := by decide
theorem cells_ok : ∀ j : Fin 19, cells.getD j [] = (Sq19.Census.vertices (rosterOf rosterNat j)).map (shiftVertex sigma) := by
  native_decide
theorem frame_lo : (2443/500 : ℝ) - 2 * (sigma:ℝ) ≤ side + 2 * shift := by norm_num [side, sigma, shift]
theorem frame_hi : (side : ℝ) ≤ 2443/500 - 2 * sigma + 2 * shift := by norm_num [side, sigma, shift]
theorem mask_ok : ∀ j, (Sq19.Cover.censusMasks.getD 3438 0).testBit (Sq19.Cover.perm 1 (rosterOf rosterNat j)) = true := by
  native_decide
end S3438

end Sq19.Capture

#print axioms Sq19.Capture.S3442.cells_ok
#print axioms Sq19.Capture.S3438.mask_ok
