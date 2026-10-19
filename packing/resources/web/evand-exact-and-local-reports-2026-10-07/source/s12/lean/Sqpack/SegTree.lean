import Sqpack.Cover

/-!
# Segment entries of a mixed cover, as integer data

A segment line `X0 Y0 X1 Y1 w` of a mixed cover (`certificates/s21/FORMAT.md`) is stored as the
integer 5-tuple `(X0, Y0, X1, Y1, w)`.  As for points (`Cover.lean`, `PTree`), the entries sit in a
binary search tree `STree`, keyed on `(X0, Y0, X1, Y1)` lexicographically, so the kernel can look an
entry up in `O(log n)` steps.  The ordering is not trusted: `STree.mem_sound` holds for any tree.

`segNorm` puts the endpoints of a segment in lexicographic order (the measure of a segment does not
depend on its orientation, `segMeasure_comm`); the generator stores every segment normalised, so the
image of a stored segment under a symmetry is looked up after normalising it.
-/

namespace SquarePacking

/-- A segment entry `(X0, Y0, X1, Y1, w)`. -/
abbrev SegE := ℕ × ℕ × ℕ × ℕ × ℕ

/-- Strict lexicographic order of two integer points `(a, b) < (c, d)`. -/
def ptLt (a b c d : ℕ) : Bool := Nat.blt a c || (Nat.beq a c && Nat.blt b d)

lemma ptLt_iff (a b c d : ℕ) : ptLt a b c d = true ↔ a < c ∨ (a = c ∧ b < d) := by
  simp [ptLt, Nat.blt_eq, Nat.beq_eq]

/-- Put the endpoints of a segment entry in lexicographic order. -/
def segNorm (e : SegE) : SegE :=
  if ptLt e.1 e.2.1 e.2.2.1 e.2.2.2.1 = true then e else (e.2.2.1, e.2.2.2.1, e.1, e.2.1, e.2.2.2.2)

/-- A binary search tree of segment entries. -/
inductive STree
  | leaf
  | node (l : STree) (e : SegE) (r : STree)

namespace STree

/-- The entries, in order. -/
def toList : STree → List SegE
  | leaf => []
  | node l e r => l.toList ++ e :: r.toList

/-- The lexicographic strict order on the key `(X0, Y0, X1, Y1)`. -/
def keyLt (a b : SegE) : Bool :=
  Nat.blt a.1 b.1 || (Nat.beq a.1 b.1 && (Nat.blt a.2.1 b.2.1 || (Nat.beq a.2.1 b.2.1 &&
    (Nat.blt a.2.2.1 b.2.2.1 || (Nat.beq a.2.2.1 b.2.2.1 && Nat.blt a.2.2.2.1 b.2.2.2.1)))))

/-- Equality of keys. -/
def keyEq (a b : SegE) : Bool :=
  Nat.beq a.1 b.1 && Nat.beq a.2.1 b.2.1 && Nat.beq a.2.2.1 b.2.2.1 && Nat.beq a.2.2.2.1 b.2.2.2.1

/-- Search-tree lookup of a whole entry (key *and* weight). -/
def mem : STree → SegE → Bool
  | leaf, _ => false
  | node l x r, e =>
    bif keyEq e x then Nat.beq e.2.2.2.2 x.2.2.2.2
    else bif keyLt e x then l.mem e else r.mem e

/-- A test on every entry. -/
def all (p : SegE → Bool) : STree → Bool
  | leaf => true
  | node l e r => l.all p && p e && r.all p

/-- The total weight. -/
def wsum : STree → ℕ
  | leaf => 0
  | node l e r => l.wsum + e.2.2.2.2 + r.wsum

/-- Consecutive entries strictly increasing in the key. -/
def chainB : List SegE → Bool
  | a :: b :: l => keyLt a b && chainB (b :: l)
  | _ => true

theorem mem_sound (t : STree) (e : SegE) (h : t.mem e = true) : e ∈ t.toList := by
  induction t with
  | leaf => simp [mem] at h
  | node l x r ihl ihr =>
    simp only [toList, List.mem_append, List.mem_cons]
    unfold mem at h
    cases hk : keyEq e x
    · rw [hk, cond_false] at h
      cases hl : keyLt e x
      · rw [hl, cond_false] at h; exact Or.inr (Or.inr (ihr h))
      · rw [hl, cond_true] at h; exact Or.inl (ihl h)
    · rw [hk, cond_true] at h
      simp only [keyEq, Bool.and_eq_true, Nat.beq_eq] at hk
      have hw := Nat.beq_eq.mp h
      refine Or.inr (Or.inl ?_)
      obtain ⟨a, b, c, d, w⟩ := e
      obtain ⟨a', b', c', d', w'⟩ := x
      simp only at hk hw
      obtain ⟨⟨⟨h1, h2⟩, h3⟩, h4⟩ := hk
      rw [h1, h2, h3, h4, hw]

theorem all_iff (p : SegE → Bool) (t : STree) :
    t.all p = true ↔ ∀ e ∈ t.toList, p e = true := by
  induction t with
  | leaf => simp [all, toList]
  | node l x r ihl ihr =>
    simp only [all, Bool.and_eq_true, ihl, ihr, toList, List.mem_append, List.mem_cons]
    constructor
    · rintro ⟨⟨h1, h2⟩, h3⟩ e (he | rfl | he)
      exacts [h1 e he, h2, h3 e he]
    · intro h
      exact ⟨⟨fun e he => h e (Or.inl he), h _ (Or.inr (Or.inl rfl))⟩,
        fun e he => h e (Or.inr (Or.inr he))⟩

theorem wsum_eq (t : STree) : t.wsum = (t.toList.map (fun e => e.2.2.2.2)).sum := by
  induction t with
  | leaf => rfl
  | node l x r ihl ihr =>
    simp only [wsum, toList, List.map_append, List.map_cons, List.sum_append, List.sum_cons,
      ihl, ihr]
    ring

theorem keyLt_trans {a b c : SegE} (h1 : keyLt a b = true) (h2 : keyLt b c = true) :
    keyLt a c = true := by
  simp only [keyLt, Bool.or_eq_true, Bool.and_eq_true, Nat.blt_eq, Nat.beq_eq] at *
  omega

theorem keyLt_ne {a b : SegE} (h : keyLt a b = true) : a ≠ b := by
  rintro rfl
  simp [keyLt] at h

theorem nodup_of_chainB (L : List SegE) (h : chainB L = true) : L.Nodup := by
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
  have htr : Trans (fun a b : SegE => keyLt a b = true)
      (fun a b => keyLt a b = true) (fun a b => keyLt a b = true) := ⟨keyLt_trans⟩
  have hp : L.Pairwise (fun a b => keyLt a b = true) :=
    List.isChain_iff_pairwise.mp hc
  exact hp.imp keyLt_ne

end STree

end SquarePacking
