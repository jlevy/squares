import Sqpack.Bentz

/-!
# Unit segments of the `1/10`-grid

The grid-dependent pieces of `Bentz.lean` (written there for the `1/5`-grid), for the `1/10`-grid:
segment endpoints, the index range of `[0,k]`, the index shift by an integer vector, and the
periodic sum.  The grid-independent pieces (`SegIx`, `convPoly`, `fileIx`, `wid_lt_two`,
`mem_sq_sub`, `exists_of_segFrac_ne`) are reused from `Bentz`.
-/

open MeasureTheory Finset
open scoped ENNReal

namespace SquarePacking
namespace Grid10

open Bentz (SegIx)

/-- The endpoints of a unit segment of the `1/10`-grid. -/
noncomputable def segA (s : SegIx) : ℝ × ℝ := ((s.2.1 : ℝ) / 10, (s.2.2 : ℝ) / 10)
noncomputable def segB (s : SegIx) : ℝ × ℝ :=
  if s.1 then ((s.2.1 : ℝ) / 10, ((s.2.2 : ℝ) + 1) / 10)
  else (((s.2.1 : ℝ) + 1) / 10, (s.2.2 : ℝ) / 10)

/-- `{0, …, 10k} ⊆ ℤ`. -/
def idx (k : ℕ) : Finset ℤ := (range (10 * k + 1)).map ⟨Nat.cast, Nat.cast_injective⟩

lemma mem_idx {k : ℕ} {x : ℤ} : x ∈ idx k ↔ 0 ≤ x ∧ x ≤ 10 * (k : ℤ) := by
  simp only [idx, mem_map, mem_range, Function.Embedding.coeFn_mk]
  constructor
  · rintro ⟨n, hn, rfl⟩; omega
  · rintro ⟨h0, h1⟩; exact ⟨x.toNat, by omega, by omega⟩

/-- The index shift by `(-10 nx, -10 ny)`. -/
def shiftIx (nx ny : ℤ) (s : SegIx) : SegIx := (s.1, s.2.1 - 10 * nx, s.2.2 - 10 * ny)

lemma segPt_shift (nx ny : ℤ) (s : SegIx) (t : ℝ) :
    segPt (segA (shiftIx nx ny s)) (segB (shiftIx nx ny s)) t + ((nx : ℝ), (ny : ℝ))
      = segPt (segA s) (segB s) t := by
  obtain ⟨o, i, j⟩ := s
  cases o <;> simp only [shiftIx, segA, segB, segPt, Bool.false_eq_true, if_false, if_true,
    Prod.mk_add_mk] <;> push_cast <;> ext <;> ring

lemma segFrac_shift (nx ny : ℤ) (s : SegIx) (c : ℝ × ℝ) (θ : ℝ) :
    segFrac (segA (shiftIx nx ny s)) (segB (shiftIx nx ny s))
        (sq (c - ((nx : ℝ), (ny : ℝ))) θ 1) = segFrac (segA s) (segB s) (sq c θ 1) := by
  unfold segFrac
  congr 3
  ext t
  simp only [Set.mem_preimage, Bentz.mem_sq_sub, segPt_shift]

lemma sum_range_mod (m : ℕ) (G : ℕ → ℕ) :
    ∑ x ∈ range (10 * m), G (x % 10) = m * ∑ p ∈ range 10, G p := by
  induction m with
  | zero => simp
  | succ m ih =>
    rw [show 10 * (m + 1) = 10 * m + 10 by ring, sum_range_add, ih, add_mul, one_mul]
    congr 1
    refine sum_congr rfl fun y hy => ?_
    rw [mem_range] at hy
    congr 1; omega

end Grid10
end SquarePacking
