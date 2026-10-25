import S12.Normalization
import Mathlib.Data.Real.Archimedean
namespace S12
open S12Pilot
set_option maxHeartbeats 0

/-- The explicit 4-by-3 unit grid inside a square of side 4. -/
def gridSquare (i : Fin 12) : OpenSquare where
  c := 1
  s := 0
  loU := (i.val%4 : Nat)
  loV := (i.val/4 : Nat)
  side := 1
  unit_normal := by norm_num
  side_pos := by norm_num

theorem grid_inside (i : Fin 12) (x y : ℝ) :
    (gridSquare i).Inside x y ↔
    (i.val%4 : Nat)<x ∧ x<(i.val%4 : Nat)+1 ∧
    (i.val/4 : Nat)<y ∧ y<(i.val/4 : Nat)+1 := by
  simp [gridSquare,OpenSquare.Inside,InBands]

theorem integer_open_intervals_unique (m n : Nat) (x : ℝ)
    (hm0 : (m:ℝ)<x) (hm1 : x<(m:ℝ)+1) (hn0 : (n:ℝ)<x) (hn1 : x<(n:ℝ)+1) : m=n := by
  rcases lt_trichotomy m n with h | h | h
  · have hh : (m:ℝ)+1≤n := by exact_mod_cast (show m+1≤n by omega)
    linarith
  · exact h
  · have hh : (n:ℝ)+1≤m := by exact_mod_cast (show n+1≤m by omega)
    linarith

def gridPacking : UnitPacking 4 where
  square := gridSquare
  congruent := by intro i; rfl
  contained := by
    intro i x y hh
    obtain ⟨hx0,hx1,hy0,hy1⟩ := (grid_inside i x y).mp hh
    have hc : i.val%4+1≤4 := by have := Nat.mod_lt i.val (by decide : 0<4); omega
    have hr : i.val/4+1≤4 := by have := i.isLt; omega
    have hc' : ((i.val%4:Nat):ℝ)+1≤4 := by exact_mod_cast hc
    have hr' : (i.val/4:Nat)+1≤(4:ℝ) := by exact_mod_cast hr
    have hc0 : (0:ℝ)≤(i.val%4:Nat) := Nat.cast_nonneg _
    have hr0 : (0:ℝ)≤(i.val/4:Nat) := Nat.cast_nonneg _
    exact ⟨by linarith,by linarith,by linarith,by linarith⟩
  disjoint := by
    intro i j hij x y hh
    obtain ⟨hi0,hi1,hi2,hi3⟩ := (grid_inside i x y).mp hh.1
    obtain ⟨hj0,hj1,hj2,hj3⟩ := (grid_inside j x y).mp hh.2
    have hc := integer_open_intervals_unique _ _ x hi0 hi1 hj0 hj1
    have hr := integer_open_intervals_unique _ _ y hi2 hi3 hj2 hj3
    apply hij
    apply Fin.ext
    have hi := Nat.mod_add_div i.val 4
    have hj := Nat.mod_add_div j.val 4
    omega

/-- Positive side lengths admitting twelve unit squares with disjoint interiors. -/
def feasibleSides : Set ℝ := {L | 0<L ∧ Nonempty (UnitPacking L)}
noncomputable def packingConstant12 : ℝ := sInf feasibleSides

theorem four_feasible : (4:ℝ)∈feasibleSides := ⟨by norm_num,⟨gridPacking⟩⟩
theorem feasibleSides_bddBelow : BddBelow feasibleSides :=
  ⟨0,fun _ h => h.1.le⟩
theorem packingConstant12_le_four : packingConstant12≤4 :=
  csInf_le feasibleSides_bddBelow four_feasible

/-- The final connection to the packing constant. Its explicit premise remains
open until every surviving normalized case has been excluded. -/
theorem packingConstant12_eq_four_of_exclusion
    (exclude : ∀ p : NormalizedPacking,False) : packingConstant12=4 := by
  apply le_antisymm packingConstant12_le_four
  apply le_csInf ⟨4,four_feasible⟩
  intro L hL
  by_contra hh
  have hlt : L<4 := lt_of_not_ge hh
  obtain ⟨p⟩ := hL.2
  exact exclude (p.normalize hL.1 hlt)

#print axioms gridPacking
#print axioms packingConstant12_le_four
#print axioms packingConstant12_eq_four_of_exclusion
end S12
