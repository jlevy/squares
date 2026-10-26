import S12.AuxPacking

namespace S12
open S12Pilot
set_option maxHeartbeats 0

theorem combined_point (i : Fin 20) : (auxPoints 2)[i.val]! =
    if i.val<10 then (auxPoints 0)[i.val]! else (auxPoints 1)[i.val-10]! := by
  fin_cases i <;> rfl

theorem mem_combined_low (x y : Finset Nat) (i : Nat) (hi : i<10) :
    i∈combinedOwners x y ↔ i∈x := by
  simp only [combinedOwners,Finset.mem_union,Finset.mem_image]
  constructor
  · rintro (h | ⟨j,_,hj⟩)
    · exact h
    · omega
  · exact Or.inl

theorem mem_combined_high (x y : Finset Nat) (hx : x⊆Finset.range 10)
    (i : Nat) (hi : 10≤i) : i∈combinedOwners x y ↔ i-10∈y := by
  simp only [combinedOwners,Finset.mem_union,Finset.mem_image]
  constructor
  · rintro (h | ⟨j,hj,he⟩)
    · have := Finset.mem_range.mp (hx h); omega
    · have : i-10=j := by omega
      simpa only [this] using hj
  · intro h
    exact Or.inr ⟨i-10,h,by omega⟩

theorem combined_exact (q : OpenSquare) (x y : Finset Nat)
    (hx : x⊆Finset.range 10) (he : AuxExact q 0 x) (hf : AuxExact q 1 y) :
    AuxExact q 2 (combinedOwners x y) := by
  intro i hi
  have hil : i<20 := List.mem_range.mp hi
  have hp := combined_point ⟨i,hil⟩
  change (auxPoints 2)[i]! = _ at hp
  rw [hp]
  by_cases h : i<10
  · rw [if_pos h,mem_combined_low x y i h]
    exact he i (List.mem_range.mpr h)
  · have hge : 10≤i := by omega
    rw [if_neg h,mem_combined_high x y hx i hge]
    exact hf (i-10) (List.mem_range.mpr (by change i-10<10; omega))

noncomputable def natCombinedOwners (p : NormalizedPacking) (i : Fin 12) : Finset Nat :=
  combinedOwners (natAuxOwners p 0 i) (natAuxOwners p 1 i)

theorem nat_combined_exact (p : NormalizedPacking) (i : Fin 12) :
    AuxExact (p.square i) 2 (natCombinedOwners p i) :=
  combined_exact _ _ _ (nat_aux_subset p 0 i) (nat_aux_exact p 0 i) (nat_aux_exact p 1 i)

theorem nat_combined_disjoint (p : NormalizedPacking) (i j : Fin 12) (hij : i≠j) :
    Disjoint (natCombinedOwners p i) (natCombinedOwners p j) := by
  apply Finset.disjoint_left.mpr
  intro n hi hj
  by_cases hn : n<10
  · exact Finset.disjoint_left.mp (nat_aux_disjoint p 0 i j hij)
      ((mem_combined_low _ _ n hn).mp hi) ((mem_combined_low _ _ n hn).mp hj)
  · have hge : 10≤n := by omega
    exact Finset.disjoint_left.mp (nat_aux_disjoint p 1 i j hij)
      ((mem_combined_high _ _ (nat_aux_subset p 0 i) n hge).mp hi)
      ((mem_combined_high _ _ (nat_aux_subset p 0 j) n hge).mp hj)

#print axioms nat_combined_exact
end S12
