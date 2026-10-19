import PackingCertMathlib.Selection
import PackingCertMathlib.Sideband

/-!
# Lemma SWAP (proved) and the RAISE / RING-SWAP conjecture -- OPEN (A222)

**Lemma SWAP** (`docs/proofs/ring_swap.md` §1, any `n`, any side; here `n = 11`).  Let `z` be a
packing at side `m`, `X` a set of its indices, and `z'` a configuration that agrees with `z`
off `X` and whose squares on `X` are unit squares (`t ∈ [0,1]`) inside the container,
interior-disjoint from every OTHER square of `z'` (the untouched ones and each other).  Then
`z'` is a packing at side `m`.  Equivalently: `|X|` unit squares packed inside
`U(X) := (⋃ X) ∪ Free(z)` may replace `X`.  `Selection.teleport_packing` is the case `X = {i}`
with the slot square (`teleport_of_swap` below re-derives it in six lines); Lemma CELLS
(`cells_swap`) is the case "a family `Π` of pairwise interior-disjoint unit squares met, in
the interior, only by squares with indices in the range of an injection `ι`" -- the
Hall-type deficiency criterion `|M(Π)| ≤ |Π|` of `ring_swap.md` §1.3.  All three are theorems
here; the only axiom of this file is the conjecture below.

**Conjecture RAISE(0 → 1)** (`ring_swap.md` §1.5): every packing at a side `m` of the window
`[3.82, ŝ]` exchanges, at the same side, into a packing containing a CORNER slot square.  With
the k1_00 kill (k1-a: no packing at `m < ŝ` contains a corner slot square, the certified tree
`k0_route.md` §3) this empties k0_00 on `[3.82, ŝ)` (`no_packing_of_raise`).  The PI's sweep
(perimeter cells settled one at a time) is a search for the family `Π` of `cells_swap`; the
count `4⌊√n⌋ − 4 = 8` perimeter cells against `n = 11` squares does NOT close it by itself
(`ring_swap.md` §1.4: the sweep needs `|M(Π)| ≤ |Π|` for some prefix, and every four-crowd
witness of A217 over-meets every cell family), so the axiom is the geometric obligation, not a
theorem.  It is stated in its weakest useful form (one corner, any exchange); RAISE(0 → 2)
would add the adjacent cell.

**Status (2026-09-14).**  `swap_packing`, `teleport_of_swap`, `cells_swap`,
`no_packing_of_raise`: theorems.  `raise_zero_one`: axiom [C], tested on A217's witnesses
(`attempts/A222-ring-swap/results/swap222.md`).
-/

namespace PackingCert.S11.OpenLemmas

open Set

/-- **Lemma SWAP.**  Replacing the squares of `X` by unit squares inside the container that
are interior-disjoint from every other square keeps the packing property at the same side. -/
theorem swap_packing {m : ℝ} {z : Cfg} (hz : CfgPacking m z) (X : Set (Fin 11)) (z' : Cfg)
    (hkeep : ∀ j, j ∉ X → z' j = z j)
    (ht : ∀ i ∈ X, (z' i).t ∈ Icc (0 : ℝ) 1)
    (hbox : ∀ i ∈ X, (z' i).set ⊆ container m)
    (hfree : ∀ i ∈ X, ∀ j, j ≠ i → Disjoint (interior (z' i).set) (interior (z' j).set)) :
    CfgPacking m z' := by
  obtain ⟨htz, hP⟩ := hz
  refine ⟨?_, ?_⟩
  · intro j
    by_cases hj : j ∈ X
    · exact ht j hj
    · rw [hkeep j hj]
      exact htz j
  · refine ⟨?_, ?_, ?_⟩
    · intro j
      exact psq_isUnitSquare _
    · intro j
      by_cases hj : j ∈ X
      · exact hbox j hj
      · rw [hkeep j hj]
        exact hP.contained j
    · intro j l hjl
      by_cases hj : j ∈ X
      · exact hfree j hj l (Ne.symm hjl)
      · by_cases hl : l ∈ X
        · exact (hfree l hl j hjl).symm
        · rw [hkeep j hj, hkeep l hl]
          exact hP.interiorDisjoint j l hjl

/-- `teleport_packing` is SWAP with `X = {i}` and the slot square. -/
theorem teleport_of_swap {m : ℝ} {z : Cfg} (hz : CfgPacking m z) (i : Fin 11) (c : RP)
    (hbox : slotBox c ⊆ container m)
    (hfree : ∀ j, j ≠ i → Disjoint (interior (slotBox c)) (interior (z j).set)) :
    CfgPacking m (teleport z i c) := by
  refine swap_packing hz {i} (teleport z i c) ?_ ?_ ?_ ?_
  · intro j hj
    exact teleport_ne z i c (fun h => hj (Set.mem_singleton_iff.mpr h))
  · intro k hk
    rw [Set.mem_singleton_iff] at hk
    rw [hk]
    simp only [teleport, Function.update_self]
    exact ⟨le_refl _, by norm_num⟩
  · intro k hk
    rw [Set.mem_singleton_iff] at hk
    rw [hk, teleport_self]
    exact hbox
  · intro k hk j hj
    rw [Set.mem_singleton_iff] at hk
    rw [hk] at hj ⊢
    rw [teleport_self, teleport_ne z i c hj]
    exact hfree j hj

/-- **Lemma CELLS** (the deficiency criterion).  `F : Fin k → PSq` is a family of pairwise
interior-disjoint unit squares in the container; the squares of `z` whose interiors meet some
member of `F` all have indices in the range of the injection `ι : Fin k → Fin 11`
(`|M(Π)| ≤ k`).  Then the configuration `z'` that puts `F a` at index `ι a` and keeps every
other square is a packing at side `m`: `z` exchanges into a packing containing all of `F`. -/
theorem cells_swap {m : ℝ} {z : Cfg} (hz : CfgPacking m z) {k : ℕ} (ι : Fin k → Fin 11)
    (F : Fin k → PSq) (z' : Cfg)
    (hF : ∀ a, z' (ι a) = F a) (hkeep : ∀ j, (∀ a, ι a ≠ j) → z' j = z j)
    (htF : ∀ a, (F a).t ∈ Icc (0 : ℝ) 1) (hboxF : ∀ a, (F a).set ⊆ container m)
    (hdisj : ∀ a b, a ≠ b → Disjoint (interior (F a).set) (interior (F b).set))
    (hmiss : ∀ j, (∀ a, ι a ≠ j) → ∀ a, Disjoint (interior (F a).set) (interior (z j).set)) :
    CfgPacking m z' := by
  refine swap_packing hz (Set.range ι) z' ?_ ?_ ?_ ?_
  · intro j hj
    exact hkeep j (fun a h => hj ⟨a, h⟩)
  · rintro i ⟨a, rfl⟩
    rw [hF a]
    exact htF a
  · rintro i ⟨a, rfl⟩
    rw [hF a]
    exact hboxF a
  · rintro i ⟨a, rfl⟩ j hj
    by_cases hjr : j ∈ Set.range ι
    · obtain ⟨b, rfl⟩ := hjr
      have hab : a ≠ b := by
        rintro rfl
        exact hj rfl
      rw [hF a, hF b]
      exact hdisj a b hab
    · have hn : ∀ b, ι b ≠ j := fun b h => hjr ⟨b, h⟩
      rw [hF a, hkeep j hn]
      exact hmiss j hn a

/-- **[OPEN] Conjecture RAISE(0 → 1)** (the RING-SWAP conjecture in its weakest useful form).
Every packing at a window side exchanges, at the same side, into a packing containing a corner
slot square (`Slot` corner `c`, cell `(0, 0)`). -/
axiom raise_zero_one (m : ℝ) (hm : 191 / 50 ≤ m ∧ m ≤ 3877084 / 1000000) (z : Cfg)
    (hz : CfgPacking m z) :
    ∃ z' : Cfg, CfgPacking m z' ∧ ∃ c : Fin 4, ContainsPins {⟨c, 0, 0⟩} m z'

/-- The consequence: RAISE(0 → 1) plus the corner-pin kill at side `m` (k1-a, the k1_00 tree)
leaves no packing at side `m`.  Pure logic. -/
theorem no_packing_of_raise (m : ℝ) (hm : 191 / 50 ≤ m ∧ m ≤ 3877084 / 1000000)
    (kill : ∀ (c : Fin 4) (z : Cfg), CfgPacking m z → ¬ ContainsPins {⟨c, 0, 0⟩} m z) :
    ∀ z : Cfg, ¬ CfgPacking m z := by
  intro z hz
  obtain ⟨z', hz', c, hc⟩ := raise_zero_one m hm z hz
  exact kill c z' hz' hc

#print axioms swap_packing
#print axioms cells_swap
#print axioms raise_zero_one

end PackingCert.S11.OpenLemmas
