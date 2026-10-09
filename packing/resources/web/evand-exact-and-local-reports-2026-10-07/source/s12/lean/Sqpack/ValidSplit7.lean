import Sqpack.ValidSplit
import Sqpack.ValidSplitData

/-!
# `Valid7` split: D4 and Lemma Z in Lean, `ValidTilt7` left to the Python run

`Valid7` (`Bentz.lean`) is reduced to `ValidTilt7`, exactly the pose region that `qx2_zm.py`'s run
V3 certifies (centres in `[0, 7/2]²`, `u = tan(θ/2) > 0`, `θ ≤ 45°`, admissible squares):

* `box7_grid` — the box file's measure is a grid cover (`ValidSplit.gridCover`, weights the packed
  table `box7Packed`, Lebesgue on `[9/5, 26/5]²`); kernel checks `out7`, `fit7` tie the packed table
  to the family weights `wN 7`, hence (`box7Cover_measure`) to the file.
* `d4_box7` — it is D4-invariant (kernel check `sym7`).
* **`validAxis7`** — Lemma Z: every axis-parallel closed unit square in `[0,7]²` has mass `≥ 1`
  (kernel check `axis7`: 3,600 corner limits, the whole box, no symmetry used).
* **`valid7_of_tilt`** — `ValidTilt7 → Valid7`, and **`bentz_of_validTilt7`** — `ValidTilt7 → ∀ k ≥
  6, minSide (k² − 3) = k`.

`notes/lean-valid-split.md`.
-/

open MeasureTheory

namespace SquarePacking
namespace Bentz

open ValidSplit

/-! ## Kernel checks -/

/-- The family weights vanish outside `[0,7]²`. -/
theorem out7 : outOK 7 (wN 7) = true := by decide +kernel

/-- The packed table is the family's weights on the whole grid. -/
theorem fit7 : fitOK (5 * 7) (wN 7) box7Packed = true := by decide +kernel

/-- The weights are D4-invariant. -/
theorem sym7 : symOKP (5 * 7) box7Packed = true := by decide +kernel

/-- Lemma Z: every corner limit of every cell has mass `≥ 1`. -/
theorem axis7 : axisOKP 7 9 1000000000000 box7Packed = true := by decide +kernel

/-! ## The box file is a grid cover -/

lemma lebSq7 : lebSq 7 = BentzFam.lebSq 9 7 := by
  ext p
  simp only [lebSq, BentzFam.lebSq, Set.mem_prod, Set.mem_Icc]
  norm_num

/-- `μ₇` (the box file `L4_k02_box7.txt`) as a grid cover. -/
theorem box7_grid :
    box7Cover.measure = (gridCover 7 9 1000000000000 (wP box7Packed (5 * 7))).measure := by
  rw [box7Cover_measure, ← gridCover_fit fit7]
  refine measure_eq_gridCover (famCover 7) 7 9 1000000000000 (wN 7) rfl rfl rfl rfl (fun s => ?_)
    rfl (fun _ => lebSq7) (fun _ => ?_) out7
  · simp only [famCover]; norm_num
  · simp only [famCover]; norm_num

/-! ## The split -/

/-- **`ValidTilt7`: what run V3 of `qx2_zm.py` certifies** — every admissible closed unit square
with centre in `[0, 7/2]²` and angle `θ = 2 arctan u`, `u > 0`, `u² + 2u ≤ 1` (`0 < θ ≤ 45°`), has
mass `≥ 1` under the box file `L4_k02_box7.txt`. -/
def ValidTilt7 : Prop := ValidTilt 7 box7Cover.measure

/-- **`ValidAxis7`** (Lemma Z): every axis-parallel closed unit square in `[0,7]²` has mass
`≥ 1`. -/
def ValidAxis7 : Prop := ValidAxis 7 box7Cover.measure

/-- The box cover is D4-invariant. -/
theorem d4_box7 : D4InvM 7 box7Cover.measure := by
  rw [box7_grid]
  simpa only [Nat.cast_ofNat] using d4InvM_packed (K := 7) (A := 9) (den := 1000000000000) sym7

/-- `ValidTilt7 → ValidAxis7 → Valid7` (the D4 reduction). -/
theorem valid7_of_tilt_axis (ht : ValidTilt7) (ha : ValidAxis7) : Valid7 :=
  valid_of_tilt_axis d4_box7 ht ha

/-- **Lemma Z for `μ₇`, in Lean.** -/
theorem validAxis7 : ValidAxis7 := by
  unfold ValidAxis7
  rw [box7_grid]
  simpa only [Nat.cast_ofNat] using validAxis_packed (K := 7) (A := 9) (den := 1000000000000)
    (by norm_num) (by norm_num) (by norm_num) axis7

/-- **`ValidTilt7 → Valid7`.** -/
theorem valid7_of_tilt (ht : ValidTilt7) : Valid7 := valid7_of_tilt_axis ht validAxis7

/-- **`s(k² − 3) = k` for all `k ≥ 6`, from `ValidTilt7`** (the tilted run's region only). -/
theorem bentz_of_validTilt7 (ht : ValidTilt7) : ∀ k : ℕ, 6 ≤ k → minSide (k ^ 2 - 3) = k :=
  bentz_of_valid7 (valid7_of_tilt ht)

end Bentz
end SquarePacking
