import Mathlib.Data.Finset.Card

/-! A verified finite-domain disjoint-ownership solver. No geometrical fact is
assumed here; each input domain must separately be proved to contain every
possible ownership set for its square. -/
namespace S12
variable {P : Type} [DecidableEq P]

def feasible : List (List (Finset P)) → Finset P → Bool
  | [], _ => true
  | d :: ds, used => d.any fun m => decide (Disjoint m used) && feasible ds (used ∪ m)

/-- This is the mathematical meaning of a domain solution. -/
inductive Assignment : List (List (Finset P)) → Finset P → Prop
  | nil (used) : Assignment [] used
  | cons {d ds used m} : m ∈ d → Disjoint m used →
      Assignment ds (used ∪ m) → Assignment (d :: ds) used

theorem feasible_iff (ds : List (List (Finset P))) (used : Finset P) :
    feasible ds used = true ↔ Assignment ds used := by
  induction ds generalizing used with
  | nil => simp [feasible]; exact Assignment.nil used
  | cons d ds ih =>
    simp only [feasible, List.any_eq_true, Bool.and_eq_true, decide_eq_true_eq, ih]
    constructor
    · rintro ⟨m, hm, hd, hr⟩
      exact Assignment.cons hm hd hr
    · intro h
      cases h with
      | cons hm hd hr => exact ⟨_, hm, hd, hr⟩

theorem rejected_domain_impossible (ds : List (List (Finset P)))
    (h : feasible ds ∅ = false) : ¬ Assignment ds ∅ := by
  intro ha
  have := (feasible_iff ds ∅).mpr ha
  simp [h] at this

/-- Independently specified actual owner sets induce a solver assignment. -/
theorem actual_owners_give_assignment
    (ds : List (List (Finset P))) (owners : List (Finset P)) (used : Finset P)
    (hmem : List.Forall₂ (fun m d => m ∈ d) owners ds)
    (hused : ∀ m ∈ owners, Disjoint m used)
    (hdis : owners.Pairwise Disjoint) : Assignment ds used := by
  induction hmem generalizing used with
  | nil => exact Assignment.nil used
  | @cons m d owners ds hm hmem ih =>
    obtain ⟨hmrest, hrest⟩ := List.pairwise_cons.mp hdis
    apply Assignment.cons hm (hused m (by simp))
    apply ih
    · intro n hn
      exact Finset.disjoint_union_right.mpr
        ⟨hused n (by simp [hn]), (hmrest n hn).symm⟩
    · exact hrest

#print axioms feasible_iff
#print axioms actual_owners_give_assignment
end S12
