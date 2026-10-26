import S12.AuxCoverGeometry

namespace S12
open S12Pilot

def CornerPairOwned (q : OpenSquare) : Prop :=
  (Owns q 0 ∧ Owns q 1) ∨ (Owns q 2 ∧ Owns q 3) ∨
  (Owns q 4 ∧ Owns q 5) ∨ (Owns q 6 ∧ Owns q 7)

theorem cornerPair_pullX (q : OpenSquare) : CornerPairOwned (pullX q) ↔ CornerPairOwned q := by
  simp only [CornerPairOwned, owns_pullX]
  norm_num [permX]
  tauto
theorem cornerPair_pullY (q : OpenSquare) : CornerPairOwned (pullY q) ↔ CornerPairOwned q := by
  simp only [CornerPairOwned, owns_pullY]
  norm_num [permY]
  tauto
theorem cornerPair_pullSwap (q : OpenSquare) : CornerPairOwned (pullSwap q) ↔ CornerPairOwned q := by
  simp only [CornerPairOwned, owns_pullSwap]
  norm_num [permSwap]
  tauto

theorem no_corner_local (q : OpenSquare) (h : ¬CornerPairOwned q) :
    ¬Owns q 0 ∨ ¬Owns q 1 := by
  apply not_and_or.mp
  intro hp
  exact h (Or.inl hp)

theorem aux_left_rectangle (q : OpenSquare) (ha : 1<q.side) (hbox : InsideContainer q)
    (hf : AvoidsF q) (hc : ¬CornerPairOwned q) (hx : centerX q≤2) :
    1≤centerX q ∧ 87/50≤centerY q ∧ centerY q≤113/50 := by
  by_cases hy : centerY q≤2
  · obtain ⟨h1,h2⟩ := aux_lower_localization q ha hbox hf (no_corner_local q hc) hx hy
    exact ⟨h1.le,h2.le,by linarith⟩
  · have hc' : ¬CornerPairOwned (pullY q) := by
      simpa only [cornerPair_pullY] using hc
    obtain ⟨h1,h2⟩ := aux_lower_localization (pullY q) ha (container_pullY q hbox)
      (avoidsF_pullY q hf) (no_corner_local _ hc') (by simpa using hx) (by simp; linarith)
    simp only [center_pullY_x,center_pullY_y] at h1 h2
    exact ⟨h1.le,by linarith,by linarith⟩

theorem aux_left_pair (q : OpenSquare) (ha : 1<q.side) (hbox : InsideContainer q)
    (hf : AvoidsF q) (hc : ¬CornerPairOwned q) (hx : centerX q≤2) :
    Owns q 8 ∧ Owns q 11 := by
  obtain ⟨hx0,hy0,hy1⟩ := aux_left_rectangle q ha hbox hf hc hx
  refine ⟨aux_central_fan q ha hf hx0 hx hy0 hy1,?_⟩
  have h := aux_central_fan (pullY q) ha (avoidsF_pullY q hf)
    (by simpa using hx0) (by simpa using hx) (by simp; linarith) (by simp; linarith)
  simpa [owns_pullY,permY] using h

def FExempt (q : OpenSquare) : Prop := CornerPairOwned q ∨
  (Owns q 8 ∧ Owns q 11) ∨ (Owns q 9 ∧ Owns q 10)

/-- The complete auxiliary F covering rule, proved from the walls and
triangle decompositions rather than importing the original diagram. -/
theorem avoidingF_forces_pair (q : OpenSquare) (ha : 1<q.side) (hbox : InsideContainer q)
    (hf : AvoidsF q) : FExempt q := by
  by_cases hc : CornerPairOwned q
  · exact Or.inl hc
  right
  by_cases hx : centerX q≤2
  · exact Or.inl (aux_left_pair q ha hbox hf hc hx)
  · have hc' : ¬CornerPairOwned (pullX q) := by simpa only [cornerPair_pullX] using hc
    have h := aux_left_pair (pullX q) ha (container_pullX q hbox) (avoidsF_pullX q hf)
      hc' (by simp; linarith)
    right
    simpa [owns_pullX,permX] using h

def AvoidsG (q : OpenSquare) : Prop := ∀ i : Fin 10, ¬q.Inside (fPoint i).2 (fPoint i).1
def GExempt (q : OpenSquare) : Prop := CornerPairOwned q ∨
  (Owns q 8 ∧ Owns q 9) ∨ (Owns q 10 ∧ Owns q 11)

/-- The G covering rule includes the exact coordinate and marker transport. -/
theorem avoidingG_forces_pair (q : OpenSquare) (ha : 1<q.side) (hbox : InsideContainer q)
    (hg : AvoidsG q) : GExempt q := by
  have hf : AvoidsF (pullSwap q) := by
    intro i hi; exact hg i ((inside_pullSwap q _ _).mp hi)
  have h := avoidingF_forces_pair (pullSwap q) ha (container_pullSwap q hbox) hf
  simp only [FExempt,cornerPair_pullSwap,owns_pullSwap] at h
  norm_num [permSwap] at h
  dsimp [GExempt]
  tauto

#print axioms avoidingF_forces_pair
#print axioms avoidingG_forces_pair
end S12
