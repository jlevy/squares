import Sqpack.Spec
import Sqpack.S32
import Sqpack.S12WLower

/-!
# Bridge: this project's definitions agree with the common specification `Sqpack/Spec.lean`

* `sq_one_eq`, `sqInt_one_eq`, `box_eq` — `SquarePacking.sq c θ 1`, `SquarePacking.sqInt c θ 1`
  and `SquarePacking.box s` are `unitSq c θ`, its interior, and `container s`;
* `packs_iff`, `minSide_eq` — hence `Packs` and `minSide` agree;
* `lower_of_le_minSide`, `isLeast_of_le_minSide` — a bound `a ≤ minSide n` (`n ≥ 1`) gives the
  canonical lower-bound shape `∀ s, Packs n s → a ≤ s`, and with `Packs n a` the exact shape.

Then the results in the default build, restated in the canonical shapes: `s12_lower_3920_997`
and, under its one computational hypothesis, `s32_isLeast_of_checker`.  The headline results,
whose data is opt-in, are restated in `Sqpack/SpecHeadline.lean` (also opt-in).

(`Sqpack/Attain.lean` proves that `minSide n` is attained, `isLeast_minSide`; with `packs_iff`
and `minSide_eq` that transfers to `UnitSquarePacking` verbatim.)
-/

namespace UnitSquarePacking

open Set

/-! ## The definitions agree -/

theorem sq_one_eq (c : ℝ × ℝ) (θ : ℝ) : SquarePacking.sq c θ 1 = unitSq c θ := by
  rw [unitSq_eq_setOf]; rfl

theorem sqInt_one_eq (c : ℝ × ℝ) (θ : ℝ) :
    SquarePacking.sqInt c θ 1 = interior (unitSq c θ) := by
  rw [interior_unitSq]; rfl

theorem box_eq (s : ℝ) : SquarePacking.box s = container s := by
  ext p
  simp only [SquarePacking.box, container, mem_prod, mem_Icc, mem_ofPred_eq]
  tauto

theorem packs_iff {n : ℕ} {s : ℝ} : SquarePacking.Packs n s ↔ Packs n s := by
  simp only [SquarePacking.Packs, Packs, sq_one_eq, sqInt_one_eq, box_eq]
  rfl

theorem minSide_eq (n : ℕ) : SquarePacking.minSide n = minSide n := by
  simp only [SquarePacking.minSide, minSide, packs_iff]

/-! ## From `a ≤ minSide n` to the canonical shapes -/

/-- A container holding at least one unit square has side `≥ 0` (the centre lies in it). -/
lemma nonneg_of_packs {n : ℕ} {s : ℝ} (hn : 1 ≤ n) (h : Packs n s) : 0 ≤ s := by
  obtain ⟨c, θ, hin, -⟩ := h
  have hc : c ⟨0, hn⟩ ∈ unitSq (c ⟨0, hn⟩) (θ ⟨0, hn⟩) :=
    ⟨0, ⟨⟨by norm_num, by norm_num⟩, by norm_num, by norm_num⟩, by simp [rot]⟩
  obtain ⟨⟨h1, h2⟩, -⟩ := hin _ hc
  linarith

lemma bddBelow_packs {n : ℕ} (hn : 1 ≤ n) : BddBelow {s | Packs n s} :=
  ⟨0, fun _ hs => nonneg_of_packs hn hs⟩

theorem lower_of_le_minSide {n : ℕ} {a : ℝ} (hn : 1 ≤ n) (h : a ≤ minSide n) :
    ∀ s, Packs n s → a ≤ s :=
  fun _ hs => h.trans (csInf_le (bddBelow_packs hn) hs)

theorem isLeast_of_le_minSide {n : ℕ} {a : ℝ} (hn : 1 ≤ n) (h : a ≤ minSide n)
    (hp : Packs n a) : IsLeast {s | Packs n s} a :=
  ⟨hp, lower_of_le_minSide hn h⟩

/-- The `m × m` grid packs any `k ≤ m²` unit squares in `[0, m]²`. -/
theorem packs_grid (m k : ℕ) (hk : k ≤ m * m) : Packs k m :=
  packs_iff.mp (SquarePacking.packs_grid m k hk)

/-! ## Results in the default build, in the canonical shapes -/

/-- `s(12) ≥ 3920/997 = 3.9318…` (`SquarePacking.s12_ge_3920_997`). -/
theorem s12_lower_3920_997 : ∀ s, Packs 12 s → (3920 / 997 : ℝ) ≤ s :=
  lower_of_le_minSide (by norm_num) (minSide_eq 12 ▸ SquarePacking.s12_ge_3920_997)

/-- `s(32) = 6` from the statement the `zeromargin.py` D4 run certifies
(`SquarePacking.s32_isLeast`).  The unconditional version is in `Sqpack/SpecHeadline.lean`'s
comment (its data, `S32Z`, is opt-in). -/
theorem s32_isLeast_of_checker (h : SquarePacking.S32CheckerCover) :
    IsLeast {s | Packs 32 s} 6 := by
  simpa only [packs_iff] using SquarePacking.s32_isLeast h.region

end UnitSquarePacking
