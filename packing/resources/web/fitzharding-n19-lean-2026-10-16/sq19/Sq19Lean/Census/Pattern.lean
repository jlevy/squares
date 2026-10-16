import Sq19Lean.Census.Symmetry
import Sq17Lean.PropagationWallReplace

/-! Sub-pattern exclusion for the 19-square census.

`Packs pat` says: there are unit squares, one for each entry of the cell list `pat : Fin m → Fin 25`,
with centres in those closed cells, pairwise disjoint interiors, all inside `[0, 2443/500]^2`.

* `not_packs_of_trace` turns a half-plane certificate (the generic `case_excluded` form that
  `s19/tools/produce19k.py` writes) into `¬ Packs pat`.
* `not_packs_perm`: excluding a pattern excludes each of its eight images under the square symmetries.
* `not_packs_of_sub`: excluding a pattern excludes every family whose cells include it (subfamily).

No finite data is checked in this file. -/
namespace Sq19.Census
open Sq17.Propagation

def Packs {m : ℕ} (pat : Fin m → Fin 25) : Prop :=
  ∃ p u : Fin m → ℝ × ℝ,
    (∀ i, (u i).1 ^ 2 + (u i).2 ^ 2 = 1) ∧
    (∀ i, p i ∈ cell (pat i)) ∧
    (∀ i, Sq17.sq (p i).1 (p i).2 (u i).1 (u i).2 ⊆ containerBox (2443/500)) ∧
    (∀ i j, i ≠ j → Disjoint
      (interior (Sq17.sq (p i).1 (p i).2 (u i).1 (u i).2))
      (interior (Sq17.sq (p j).1 (p j).2 (u j).1 (u j).2)))

/-- A packing of the image pattern maps back to a packing of the pattern. -/
theorem packs_of_perm {m : ℕ} (pat : Fin m → Fin 25) (g : Fin 8)
    (h : Packs (fun i => perm g (pat i))) : Packs pat := by
  obtain ⟨p, u, hu, hc, hf, hd⟩ := h
  refine ⟨fun i => action (inv g) (p i), fun i => direction (inv g) (u i),
    fun i => direction_unit _ _ (hu i), fun i => ?_, fun i => action_square_fit _ _ _ (hf i),
    fun i j hij => action_square_disjoint _ _ _ _ _ (hd i j hij)⟩
  have := action_mem_cell (inv g) _ (hc i)
  rwa [perm_inverse] at this

theorem not_packs_perm {m : ℕ} (pat : Fin m → Fin 25) (h : ¬ Packs pat) (g : Fin 8) :
    ¬ Packs (fun i => perm g (pat i)) :=
  fun hp => h (packs_of_perm pat g hp)

/-- Subfamily: if every cell of an injective pattern is the cell of some square of the family,
a packing of the family contains a packing of the pattern. -/
theorem packs_of_sub {n m : ℕ} (assign : Fin n → Fin 25) (pat : Fin m → Fin 25)
    (hpat : Function.Injective pat) (hsub : ∀ i, ∃ j, assign j = pat i)
    (h : Packs assign) : Packs pat := by
  choose owner howner using hsub
  obtain ⟨p, u, hu, hc, hf, hd⟩ := h
  refine ⟨fun i => p (owner i), fun i => u (owner i), fun i => hu _, fun i => ?_,
    fun i => hf _, fun i j hij => hd _ _ ?_⟩
  · rw [← howner i]; exact hc _
  · intro he
    apply hij
    apply hpat
    rw [← howner i, ← howner j, he]

theorem not_packs_of_sub {n m : ℕ} (assign : Fin n → Fin 25) (pat : Fin m → Fin 25)
    (hpat : Function.Injective pat) (h : ¬ Packs pat) (hsub : ∀ i, ∃ j, assign j = pat i) :
    ¬ Packs assign :=
  fun hp => h (packs_of_sub assign pat hpat hsub hp)

theorem getD_ofFn {m : ℕ} (pat : Fin m → Fin 25) (i : Fin m) :
    (List.ofFn (fun j : Fin m => vertices (pat j))).getD i [] = vertices (pat i) := by
  simp [List.getD_eq_getElem?_getD, i.isLt]

/-- The bridge from a certificate in the generic `case_excluded` form: cells listed in owner order as
exact vertex lists, a trace container `[-shift, side + shift]^2` containing `[0, 2443/500]^2`. -/
theorem not_packs_of_trace {m : ℕ} (pat : Fin m → Fin 25) (cells : List (List (ℚ × ℚ)))
    (side shift : ℚ) (hcells : ∀ i : Fin m, cells.getD i [] = vertices (pat i))
    (hside : (2443/500 : ℚ) ≤ side + shift) (hshift : 0 ≤ shift)
    (no_packing : ∀ (c u : ℕ → ℝ × ℝ),
      (∀ i, i < m → (u i).1^2+(u i).2^2 = 1) →
      (∀ i, i < m → c i ∈ convexHull ℝ (realPoint '' {v | v ∈ cells.getD i []})) →
      (∀ i j, i < m → j < m → i ≠ j → Disjoint
        (interior (Sq17.sq (c i).1 (c i).2 (u i).1 (u i).2))
        (interior (Sq17.sq (c j).1 (c j).2 (u j).1 (u j).2))) →
      (∀ i, i < m → Sq17.sq (c i).1 (c i).2 (u i).1 (u i).2 ⊆ traceContainer side shift) →
      False) :
    ¬ Packs pat := by
  rintro ⟨p, u, hu, hc, hf, hd⟩
  have hbox : containerBox (2443/500) ⊆ traceContainer (side : ℝ) (shift : ℝ) := by
    have h1 : ((2443/500 : ℚ) : ℝ) ≤ ((side + shift : ℚ) : ℝ) := by exact_mod_cast hside
    have h2 : ((0 : ℚ) : ℝ) ≤ ((shift : ℚ) : ℝ) := by exact_mod_cast hshift
    push_cast at h1 h2
    rintro z ⟨a, b, c, d⟩
    exact ⟨by linarith, by linarith, by linarith, by linarith⟩
  let c : ℕ → ℝ × ℝ := fun n => if h : n < m then p ⟨n, h⟩ else 0
  let v : ℕ → ℝ × ℝ := fun n => if h : n < m then u ⟨n, h⟩ else (1, 0)
  apply no_packing c v
  · intro i hi; simp only [v, dite_eq_left hi]; exact hu _
  · intro i hi
    simp only [c, dite_eq_left hi]
    have := hcells ⟨i, hi⟩
    simp only at this
    rw [this]; exact hc _
  · intro i j hi hj hij
    simp only [c, v, dite_eq_left hi, dite_eq_left hj]
    exact hd _ _ (fun h => hij (congrArg Fin.val h))
  · intro i hi
    simp only [c, v, dite_eq_left hi]
    exact (hf _).trans hbox

/-- A certified pattern: an injective cell list with `¬ Packs`. -/
structure Free where
  k : ℕ
  roster : Fin k → Fin 25
  inj : Function.Injective roster
  free : ¬ Packs roster

/-- If the cells of `mask` include the image of a certified pattern under the symmetry `h`, then every
family whose cells include the image of `mask` under any symmetry `g` has no packing. -/
theorem not_packs_of_witness (P : Free) (h g : Fin 8) (mask : ℕ)
    (hw : ∀ i, mask.testBit (perm h (P.roster i)) = true)
    {n : ℕ} (assign : Fin n → Fin 25)
    (hsub : ∀ c : Fin 25, mask.testBit c = true → ∃ j, assign j = perm g c) :
    ¬ Packs assign := by
  have hinj : Function.Injective (fun i => perm g (perm h (P.roster i))) :=
    (perm_injective g).comp ((perm_injective h).comp P.inj)
  exact not_packs_of_sub assign _ hinj
    (not_packs_perm _ (not_packs_perm _ P.free h) g) (fun i => hsub _ (hw i))

end Sq19.Census

#print axioms Sq19.Census.not_packs_of_witness
#print axioms Sq19.Census.not_packs_perm
#print axioms Sq19.Census.not_packs_of_sub
#print axioms Sq19.Census.not_packs_of_trace
