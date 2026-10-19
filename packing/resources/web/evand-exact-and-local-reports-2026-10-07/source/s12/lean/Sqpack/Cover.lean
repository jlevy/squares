import Sqpack.D4

/-!
# Weighted covers given as integer data

A weighted cover in the certificate format of `verify/` and `search/zeromargin.py` is a list of
integer triples `(x, y, w)`, standing for the point `(x/D, y/D)` with weight `w/W`.  This file
turns such a list into the `(A, w)` of `packing_le_weight`, and gives kernel-checkable Boolean
tests (`decide +kernel`) for the two facts about the data the `s(32)` theorem needs:

* the total weight (`PTree.wsum`), and
* **D4 invariance** (`D4Inv`), via `x ↦ M − x` and `x ↔ y` on the integer triples.

The data are stored as a binary search tree `PTree` on the key `(x, y)` (lexicographic), so that a
membership query costs `O(log n)` kernel steps and the invariance check `O(n log n)`; a flat list
of 13,085 entries would need `O(n²)`.  The search-tree ordering is *not* trusted: `PTree.mem` is
sound for any tree (`PTree.mem_sound`), and a mis-ordered tree can only make the check fail.

* `coverA`, `coverW` — the aggregated weighted point set of a finite family of entries:
  `coverW p` is the total weight of the entries at `p`.
* `sum_filter_coverA` — the weight `(coverA, coverW)` captures in a set `S` is the total weight of
  the entries whose point lies in `S` (duplicates add).
* `sum_coverA` — the total weight is the total of the entries.
* `D4Inv_cover` — integer-level invariance gives `D4Inv`.
-/

open Finset

namespace SquarePacking

/-! ## 1.  From a finite family of entries to `(A, w)` -/

section family

variable {β : Type*}

/-- The points of a finite family of entries. -/
noncomputable def coverA (E : Finset β) (pt : β → ℝ × ℝ) : Finset (ℝ × ℝ) :=
  open Classical in E.image pt

/-- The aggregated weight: the total weight of the entries at `p`. -/
noncomputable def coverW (E : Finset β) (pt : β → ℝ × ℝ) (wt : β → ℝ) (p : ℝ × ℝ) : ℝ :=
  open Classical in ∑ e ∈ E.filter (fun e => pt e = p), wt e

open Classical in
/-- The weight captured by a set `S` is the total weight of the entries whose point is in `S`. -/
theorem sum_filter_coverA (E : Finset β) (pt : β → ℝ × ℝ) (wt : β → ℝ) (S : Set (ℝ × ℝ)) :
    ∑ a ∈ (coverA E pt).filter (fun a => a ∈ S), coverW E pt wt a
      = ∑ e ∈ E.filter (fun e => pt e ∈ S), wt e := by
  rw [← Finset.sum_fiberwise_of_maps_to (s := E.filter (fun e => pt e ∈ S))
    (t := (coverA E pt).filter (fun a => a ∈ S)) (g := pt)]
  · refine Finset.sum_congr rfl fun a ha => ?_
    simp only [Finset.mem_filter] at ha
    unfold coverW
    rw [Finset.filter_filter]
    congr 1
    ext e
    simp only [Finset.mem_filter]
    constructor
    · rintro ⟨h1, h2⟩; exact ⟨h1, h2 ▸ ha.2, h2⟩
    · rintro ⟨h1, _, h2⟩; exact ⟨h1, h2⟩
  · intro e he
    simp only [Finset.mem_filter] at he ⊢
    exact ⟨Finset.mem_image_of_mem pt he.1, he.2⟩

open Classical in
/-- The total weight of `(coverA, coverW)` is the total weight of the entries. -/
theorem sum_coverA (E : Finset β) (pt : β → ℝ × ℝ) (wt : β → ℝ) :
    ∑ a ∈ coverA E pt, coverW E pt wt a = ∑ e ∈ E, wt e := by
  have h := sum_filter_coverA E pt wt Set.univ
  simp only [Set.mem_univ, Finset.filter_true_of_mem (fun _ _ => trivial)] at h
  exact h

/-- An involution `g` of the plane, induced on the entries by an involution `ĝ` of `E` that keeps
weights, preserves the aggregated weighted point set. -/
theorem cover_invol (E : Finset β) (pt : β → ℝ × ℝ) (wt : β → ℝ)
    (g : ℝ × ℝ → ℝ × ℝ) (hg : ∀ p, g (g p) = p) (gh : β → β)
    (hE : ∀ e ∈ E, gh e ∈ E ∧ pt (gh e) = g (pt e) ∧ wt (gh e) = wt e ∧ gh (gh e) = e) :
    ∀ a ∈ coverA E pt, g a ∈ coverA E pt ∧ coverW E pt wt (g a) = coverW E pt wt a := by
  classical
  intro a ha
  obtain ⟨e, he, rfl⟩ := Finset.mem_image.mp ha
  refine ⟨Finset.mem_image.mpr ⟨gh e, (hE e he).1, (hE e he).2.1⟩, ?_⟩
  unfold coverW
  refine Finset.sum_nbij' gh gh ?_ ?_ ?_ ?_ ?_
  · intro e' he'
    simp only [Finset.mem_filter] at he' ⊢
    refine ⟨(hE e' he'.1).1, ?_⟩
    rw [(hE e' he'.1).2.1, he'.2, hg]
  · intro e' he'
    simp only [Finset.mem_filter] at he' ⊢
    refine ⟨(hE e' he'.1).1, ?_⟩
    rw [(hE e' he'.1).2.1, he'.2]
  · intro e' he'
    simp only [Finset.mem_filter] at he'
    exact (hE e' he'.1).2.2.2
  · intro e' he'
    simp only [Finset.mem_filter] at he'
    exact (hE e' he'.1).2.2.2
  · intro e' he'
    simp only [Finset.mem_filter] at he'
    exact ((hE e' he'.1).2.2.1).symm

/-- Integer-level invariance under the two generators gives `D4Inv`. -/
theorem D4Inv_cover (m : ℝ) (E : Finset β) (pt : β → ℝ × ℝ) (wt : β → ℝ) (gX gS : β → β)
    (hX : ∀ e ∈ E, gX e ∈ E ∧ pt (gX e) = reflX m (pt e) ∧ wt (gX e) = wt e ∧ gX (gX e) = e)
    (hS : ∀ e ∈ E, gS e ∈ E ∧ pt (gS e) = swapXY (pt e) ∧ wt (gS e) = wt e ∧ gS (gS e) = e) :
    D4Inv m (coverA E pt) (coverW E pt wt) := fun a ha =>
  ⟨cover_invol E pt wt (reflX m) (reflX_reflX m) gX hX a ha,
   cover_invol E pt wt swapXY swapXY_swapXY gS hS a ha⟩

end family

/-! ## 2.  Integer data in a search tree -/

/-- A binary search tree of integer cover entries `(x, y, w)`, keyed on `(x, y)`. -/
inductive PTree
  | leaf
  | node (l : PTree) (x y w : ℕ) (r : PTree)

namespace PTree

/-- The entries, in order. -/
def toList : PTree → List (ℕ × ℕ × ℕ)
  | leaf => []
  | node l x y w r => l.toList ++ (x, y, w) :: r.toList

/-- The lexicographic strict order on the key `(x, y)`. -/
def keyLt (a b : ℕ × ℕ × ℕ) : Bool :=
  Nat.blt a.1 b.1 || (Nat.beq a.1 b.1 && Nat.blt a.2.1 b.2.1)

/-- Search-tree lookup of a whole entry (key *and* weight). -/
def mem : PTree → ℕ × ℕ × ℕ → Bool
  | leaf, _ => false
  | node l x y w r, e =>
    bif Nat.beq e.1 x && Nat.beq e.2.1 y then Nat.beq e.2.2 w
    else bif keyLt e (x, y, w) then l.mem e else r.mem e

/-- A test on every entry. -/
def all (p : ℕ × ℕ × ℕ → Bool) : PTree → Bool
  | leaf => true
  | node l x y w r => l.all p && p (x, y, w) && r.all p

/-- The total weight. -/
def wsum : PTree → ℕ
  | leaf => 0
  | node l _ _ w r => l.wsum + w + r.wsum

/-- Consecutive entries strictly increasing in the key. -/
def chainB : List (ℕ × ℕ × ℕ) → Bool
  | a :: b :: l => keyLt a b && chainB (b :: l)
  | _ => true

theorem mem_sound (t : PTree) (e : ℕ × ℕ × ℕ) (h : t.mem e = true) : e ∈ t.toList := by
  induction t with
  | leaf => simp [mem] at h
  | node l x y w r ihl ihr =>
    simp only [toList, List.mem_append, List.mem_cons]
    unfold mem at h
    cases hk : (Nat.beq e.1 x && Nat.beq e.2.1 y)
    · rw [hk, cond_false] at h
      cases hl : keyLt e (x, y, w)
      · rw [hl, cond_false] at h; exact Or.inr (Or.inr (ihr h))
      · rw [hl, cond_true] at h; exact Or.inl (ihl h)
    · rw [hk, cond_true] at h
      simp only [Bool.and_eq_true, Nat.beq_eq] at hk
      have hw := Nat.beq_eq.mp h
      refine Or.inr (Or.inl ?_)
      obtain ⟨a, b, c⟩ := e
      simp only at hk hw
      rw [hk.1, hk.2, hw]

theorem all_iff (p : ℕ × ℕ × ℕ → Bool) (t : PTree) :
    t.all p = true ↔ ∀ e ∈ t.toList, p e = true := by
  induction t with
  | leaf => simp [all, toList]
  | node l x y w r ihl ihr =>
    simp only [all, Bool.and_eq_true, ihl, ihr, toList, List.mem_append, List.mem_cons]
    constructor
    · rintro ⟨⟨h1, h2⟩, h3⟩ e (he | rfl | he)
      exacts [h1 e he, h2, h3 e he]
    · intro h
      exact ⟨⟨fun e he => h e (Or.inl he), h _ (Or.inr (Or.inl rfl))⟩,
        fun e he => h e (Or.inr (Or.inr he))⟩

theorem wsum_eq (t : PTree) : t.wsum = (t.toList.map (fun e => e.2.2)).sum := by
  induction t with
  | leaf => rfl
  | node l x y w r ihl ihr =>
    simp only [wsum, toList, List.map_append, List.map_cons, List.sum_append, List.sum_cons,
      ihl, ihr]
    ring

theorem keyLt_trans {a b c : ℕ × ℕ × ℕ} (h1 : keyLt a b = true) (h2 : keyLt b c = true) :
    keyLt a c = true := by
  simp only [keyLt, Bool.or_eq_true, Bool.and_eq_true, Nat.blt_eq, Nat.beq_eq] at *
  omega

theorem keyLt_ne {a b : ℕ × ℕ × ℕ} (h : keyLt a b = true) : a ≠ b := by
  rintro rfl
  simp [keyLt] at h

theorem nodup_of_chainB (L : List (ℕ × ℕ × ℕ)) (h : chainB L = true) : L.Nodup := by
  have hc : List.IsChain (fun a b => keyLt a b = true) L := by
    induction L using chainB.induct with
    | case1 a b l ih =>
      simp only [chainB, Bool.and_eq_true] at h
      exact List.IsChain.cons_cons h.1 (ih h.2)
    | case2 l hl =>
      match l, hl with
      | [], _ => exact List.IsChain.nil
      | [a], _ => exact List.IsChain.singleton a
      | _ :: _ :: _, hl => exact absurd rfl (hl _ _ _)
  have htr : Trans (fun a b : ℕ × ℕ × ℕ => keyLt a b = true)
      (fun a b => keyLt a b = true) (fun a b => keyLt a b = true) := ⟨keyLt_trans⟩
  have hp : L.Pairwise (fun a b => keyLt a b = true) :=
    List.isChain_iff_pairwise.mp hc
  exact hp.imp keyLt_ne

end PTree

end SquarePacking
