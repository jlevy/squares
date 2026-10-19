import Sq19Lean.Capture.Links
import Sq19Lean.Basic

/-! Final-assembly skeleton for the lower bound `side19 ≤ L`.

Proved here: the composition. Not proved here (named hypotheses of `lower_bound_of_parts`):
* `hcensus`: every packing at `L ≤ sideQ` has an isometric copy (a symmetry of the square and a relabelling)
  whose `σ`-translated centres lie in the census cells of one capture region (census, cover and branch trees);
* `htoH`: poses in a region's targets give, after that region's symmetry and relabelling, poses in the hull box H
  (s19/tools/mirror.awk, s19/tools/relabel.awk; not yet in Lean);
* `hlocal`: the local theorem on H (s19/LOCAL_THEOREM.md);
* `hside`: `side19 ≤ sideQ` and the frame inequalities (finite checks).
Each capture region is instantiated by a `State.capture` theorem (Sq19Lean/Capture/S*/State.lean), which needs
its pieces built. -/
namespace Sq19.Capture
open Sq17.Propagation Sq17.Propagation.HalfPlaneState

/-- Nineteen unit squares with pairwise disjoint interiors in `[0, L]^2`. -/
def Packing19 (L : ℝ) (c u : ℕ → ℝ × ℝ) : Prop :=
  (∀ i, i < 19 → (u i).1^2+(u i).2^2 = 1) ∧
  (∀ i j, i < 19 → j < 19 → i ≠ j → Disjoint
    (interior (Sq17.sq (c i).1 (c i).2 (u i).1 (u i).2))
    (interior (Sq17.sq (c j).1 (c j).2 (u j).1 (u j).2))) ∧
  (∀ i, i < 19 → Sq17.sq (c i).1 (c i).2 (u i).1 (u i).2 ⊆ containerBox L)

/-- Poses `p` describe the family `(c, u)`. -/
def Describes (c u : ℕ → ℝ × ℝ) (p : ℕ → AnglePose) : Prop :=
  ∀ i, i < 19 → (p i).center = c i ∧ (p i).square = Sq17.sq (c i).1 (c i).2 (u i).1 (u i).2

/-- A capture region: census cells (unshifted), the trace frame of its runs, and what its capture concludes. -/
structure Region where
  census : List (List (ℚ × ℚ))
  sigma : ℚ
  side : ℚ
  shift : ℚ
  holds : (ℕ → AnglePose) → Prop
  capture : ∀ c u : ℕ → ℝ × ℝ,
    (∀ i, i < 19 → (u i).1^2+(u i).2^2 = 1) →
    (∀ i, i < 19 → c i ∈ convexHull ℝ
      (realPoint '' {v | v ∈ (census.map (List.map (shiftVertex sigma))).getD i []})) →
    (∀ i j, i < 19 → j < 19 → i ≠ j → Disjoint
      (interior (Sq17.sq (c i).1 (c i).2 (u i).1 (u i).2))
      (interior (Sq17.sq (c j).1 (c j).2 (u j).1 (u j).2))) →
    (∀ i, i < 19 → Sq17.sq (c i).1 (c i).2 (u i).1 (u i).2 ⊆ traceContainer side shift) →
    ∃ p, Describes c u p ∧ holds p

theorem getD_map_shift (V : List (List (ℚ × ℚ))) (s : ℚ) (i : ℕ) :
    (V.map (List.map (shiftVertex s))).getD i [] = (V.getD i []).map (shiftVertex s) := by
  simp [List.getD_eq_getElem?_getD]
  cases V[i]? <;> simp

theorem lower_bound_of_parts (regions : List Region) (sideQ : ℚ) (InH : (ℕ → AnglePose) → Prop)
    (hside : side19 ≤ sideQ)
    (hframe : ∀ R ∈ regions, sideQ ≤ R.side ∧ 0 ≤ R.shift)
    (hcensus : ∀ (L : ℝ) c u, L ≤ sideQ → Packing19 L c u → ∃ R ∈ regions, ∃ c' u',
      Packing19 L c' u' ∧ ∀ i, i < 19 → c' i + ((R.sigma:ℝ), (R.sigma:ℝ)) ∈
        convexHull ℝ (realPoint '' {v | v ∈ R.census.getD i []}))
    (htoH : ∀ R ∈ regions, ∀ (L : ℝ) c u p, Packing19 L c u → Describes c u p → R.holds p →
      ∃ c' u' p', Packing19 L c' u' ∧ Describes c' u' p' ∧ InH p')
    (hlocal : ∀ (L : ℝ) c u p, Packing19 L c u → Describes c u p → InH p → side19 ≤ L)
    (L : ℝ) (c u : ℕ → ℝ × ℝ) (hP : Packing19 L c u) : side19 ≤ L := by
  by_cases hL : L ≤ sideQ
  · obtain ⟨R, hR, c', u', hP', hcell⟩ := hcensus L c u hL hP
    obtain ⟨hu, hd, hf⟩ := hP'
    obtain ⟨hsR, hsh⟩ := hframe R hR
    obtain ⟨p, hp, hh⟩ := R.capture c' u' hu (fun i hi => by
        rw [getD_map_shift]; exact hull_shift _ _ _ (hcell i hi)) hd
      (fun i hi => (hf i hi).trans (container_sub_trace L R.side R.shift
        (hL.trans (by exact_mod_cast hsR)) (by exact_mod_cast hsh)))
    obtain ⟨c'', u'', p'', hP'', hp'', hH⟩ := htoH R hR L c' u' p ⟨hu, hd, hf⟩ hp hh
    exact hlocal L c'' u'' p'' hP'' hp'' hH
  · exact hside.trans (le_of_lt (lt_of_not_ge hL))

end Sq19.Capture

#print axioms Sq19.Capture.lower_bound_of_parts
