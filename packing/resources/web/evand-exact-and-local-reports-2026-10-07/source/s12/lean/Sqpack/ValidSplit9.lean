import Sqpack.ValidSplit
import Sqpack.ValidSplitData

/-!
# `Valid9` split: D4 and Lemma Z in Lean, `ValidTilt9` left to the Python run

`Valid9` (`Bentz4.lean`) is reduced to `ValidTilt9`, exactly the pose region that `qx2_zm.py`'s run
`qx2_k4x_k008/qxzm_full` certifies (centres in `[0, 9/2]²`, `u = tan(θ/2) > 0`, `θ ≤ 45°`,
admissible squares):

* `box9_grid` — the box file's measure is a grid cover (`ValidSplit.gridCover`, weights the packed
  table `box9Packed`, Lebesgue on `[14/5, 31/5]²`); kernel checks `out9`, `fit9` tie the packed
  table to the family weights `famW fam4 9` (both layers), hence (`box9Cover_measure`) to the file.
* `d4_box9` — it is D4-invariant (kernel check `sym9`).
* **`validAxis9`** — Lemma Z: every axis-parallel closed unit square in `[0,9]²` has mass `≥ 1`
  (kernel check `axis9`: 6,400 corner limits, the whole box, no symmetry used).
* **`valid9_of_tilt`** — `ValidTilt9 → Valid9`, and **`bentz4_of_validTilt9`** — `ValidTilt9 → ∀ k ≥
  8, minSide (k² − 4) = k`.

`notes/lean-valid-split.md`.
-/

open MeasureTheory

namespace SquarePacking
namespace Bentz4

open ValidSplit BentzFam

/-! ## Kernel checks -/

/-- The family weights vanish outside `[0,9]²`. -/
theorem out9 : outOK 9 (famW fam4 9) = true := by decide +kernel

/-- The packed table is the family's weights (both layers) on the whole grid. -/
theorem fit9 : fitOK (5 * 9) (famW fam4 9) box9Packed = true := by decide +kernel

/-- The weights are D4-invariant. -/
theorem sym9 : symOKP (5 * 9) box9Packed = true := by decide +kernel

/-- Lemma Z: every corner limit of every cell has mass `≥ 1`. -/
theorem axis9 : axisOKP 9 14 2000000000000 box9Packed = true := by decide +kernel

/-! ## The box file is a grid cover -/

/-- `μ₉` (the box file `K4_k008_box9.txt`) as a grid cover. -/
theorem box9_grid :
    box9Cover.measure = (gridCover 9 14 2000000000000 (wP box9Packed (5 * 9))).measure :=
  (box9Cover_measure.trans (famCover_measure_eq fam4 9 out9)).trans (gridCover_fit fit9)

/-! ## The split -/

/-- **`ValidTilt9`: what `qx2_zm.py`'s run `qx2_k4x_k008/qxzm_full` certifies** — every admissible
closed unit square with centre in `[0, 9/2]²` and angle `θ = 2 arctan u`, `u > 0`, `u² + 2u ≤ 1`
(`0 < θ ≤ 45°`), has mass `≥ 1` under the box file `K4_k008_box9.txt`. -/
def ValidTilt9 : Prop := ValidTilt 9 box9Cover.measure

/-- **`ValidAxis9`** (Lemma Z): every axis-parallel closed unit square in `[0,9]²` has mass
`≥ 1`. -/
def ValidAxis9 : Prop := ValidAxis 9 box9Cover.measure

/-- The box cover is D4-invariant. -/
theorem d4_box9 : D4InvM 9 box9Cover.measure := by
  rw [box9_grid]
  simpa only [Nat.cast_ofNat] using d4InvM_packed (K := 9) (A := 14) (den := 2000000000000) sym9

/-- `ValidTilt9 → ValidAxis9 → Valid9` (the D4 reduction). -/
theorem valid9_of_tilt_axis (ht : ValidTilt9) (ha : ValidAxis9) : Valid9 :=
  valid_of_tilt_axis d4_box9 ht ha

/-- **Lemma Z for `μ₉`, in Lean.** -/
theorem validAxis9 : ValidAxis9 := by
  unfold ValidAxis9
  rw [box9_grid]
  simpa only [Nat.cast_ofNat] using validAxis_packed (K := 9) (A := 14) (den := 2000000000000)
    (by norm_num) (by norm_num) (by norm_num) axis9

/-- **`ValidTilt9 → Valid9`.** -/
theorem valid9_of_tilt (ht : ValidTilt9) : Valid9 := valid9_of_tilt_axis ht validAxis9

/-- **`s(k² − 4) = k` for all `k ≥ 8`, from `ValidTilt9`** (the tilted run's region only). -/
theorem bentz4_of_validTilt9 (ht : ValidTilt9) : ∀ k : ℕ, 8 ≤ k → minSide (k ^ 2 - 4) = k :=
  bentz4_of_valid9 (valid9_of_tilt ht)

end Bentz4
end SquarePacking
