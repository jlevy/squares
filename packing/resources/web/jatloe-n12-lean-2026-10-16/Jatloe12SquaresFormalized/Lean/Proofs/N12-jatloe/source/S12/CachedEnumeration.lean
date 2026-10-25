import S12.Enumeration

namespace S12
variable {M G : Type} [LinearOrder M] [DecidableEq G]

def cachedEnumerate (candidates : List G) (support : G → Finset M)
    (fuel : Nat) (available : Finset M) (k : Nat) : List (Finset G) :=
  (enumerate (candidates.map fun g => (g,support g)) Prod.snd fuel available k).map
    (Finset.image Prod.fst)

/-- Cache each candidate's marker set once, without changing coverage. -/
theorem cachedEnumerate_complete (candidates : List G) (support : G → Finset M)
    (fuel : Nat) (available : Finset M) (chosen : Finset G)
    (hfuel : available.card ≤ fuel)
    (ha : Admissible candidates support available chosen) :
    chosen ∈ cachedEnumerate candidates support fuel available chosen.card := by
  let tag : G → G × Finset M := fun g => (g,support g)
  let lifted := chosen.image tag
  have hinj : Function.Injective tag := by
    intro x y h; exact congrArg Prod.fst h
  have hc : lifted.card = chosen.card := Finset.card_image_of_injective _ hinj
  have hl : Admissible (candidates.map tag) Prod.snd available lifted := by
    constructor
    · intro p hp
      obtain ⟨g,hg,rfl⟩ := Finset.mem_image.mp hp
      exact ⟨List.mem_map.mpr ⟨g,(ha.1 g hg).1,rfl⟩,(ha.1 g hg).2⟩
    · intro p hp q hq hne
      obtain ⟨g,hg,rfl⟩ := Finset.mem_image.mp hp
      obtain ⟨h,hh,rfl⟩ := Finset.mem_image.mp hq
      apply ha.2 g hg h hh
      intro he; subst h; exact hne rfl
  have he := enumerate_complete (candidates.map tag) Prod.snd fuel available lifted hfuel hl
  rw [hc] at he
  apply List.mem_map.mpr
  refine ⟨lifted,he,?_⟩
  simp [lifted,tag,Finset.image_image,Function.comp_def]

#print axioms cachedEnumerate_complete
end S12
