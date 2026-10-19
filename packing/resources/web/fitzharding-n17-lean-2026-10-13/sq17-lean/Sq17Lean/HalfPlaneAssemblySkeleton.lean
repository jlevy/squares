import Sq17Lean.OrbitPackingReduction
import Sq17Lean.RepresentativeCaseCheck
import Sq17Lean.EndpointPacking
import Sq17Lean.EndpointSideSharp
import Sq17Lean.CaptureTerminalOptimality

/-! A checked, CONDITIONAL assembly skeleton. Remaining obligations are named
structure fields, not `sorry` or new axioms. There is no concrete inhabitant of
Obligations in this file, and therefore no unconditional optimality theorem.

Use OrbitCensus.exhaustive and all_representatives_classified for the first two
fields. full_cases.tsv supplies sourceCase; its roster binding must be checked
against the actual case theorem definitions. Per-case roster selection, pattern
symmetry and translation into each header frame remain dispatch obligations. -/
namespace Sq17.HalfPlaneAssembly
open Propagation CenteredOrbitFrame OrbitCellAssignment RepresentativeCases

structure RepresentativePacking (holes : List (Fin 24)) (L : ℝ) where
  c : Fin 17 → ℝ × ℝ
  u : Fin 17 → ℝ × ℝ
  assigned : Fin 17 → Fin 24
  occupied_card : (holes.toFinsetᶜ).card = 17
  injective : Function.Injective assigned
  occupied : ∀ i, assigned i ∈ holes.toFinsetᶜ
  centres : ∀ i, c i ∈ traceCell 0 (assigned i)
  unit : ∀ i, (u i).1^2 + (u i).2^2 = 1
  fit : ∀ i, Sq17.sq (c i).1 (c i).2 (u i).1 (u i).2 ⊆ traceBox L 0
  disjoint : ∀ i j, i ≠ j → Disjoint
    (interior (Sq17.sq (c i).1 (c i).2 (u i).1 (u i).2))
    (interior (Sq17.sq (c j).1 (c j).2 (u j).1 (u j).2))

/-- `sourceCase` maps compact full-roster indices to zero-based all_orbits IDs.
`sourceRoster` must be bound to each imported case theorem's actual roster.
`ordinary` must be instantiated from the 2776-case manifest. -/
structure Obligations (tree : FiniteOrbitCover.RepTree)
    (patterns fullCases sourceRoster : ℕ → List (Fin 24))
    (sourceCase : ℕ → ℕ) (ordinary : ℕ → Prop) : Prop where
  census : ∀ s : Finset (Fin 24), s.card = 17 → FiniteOrbitCover.Reaches tree s
  classification : ∀ holes, tree.Contains holes →
    ∃ a, Matches patterns fullCases holes a
  source_roster : ∀ k, fullCases k = sourceRoster (sourceCase k)
  full_route : ∀ k, (fullCases k).length = 17 →
    ordinary (sourceCase k) ∨ sourceCase k ∈ [1447, 7220, 7223, 7255] ∨ sourceCase k = 1442
  pattern_dispatch : ∀ L, L < EndpointGeometry.side → ∀ holes,
    RepresentativePacking holes L → ∀ index g,
    Matches patterns fullCases holes (.pattern index g) → False
  ordinary_dispatch : ∀ caseId, ordinary caseId → ∀ L, L < EndpointGeometry.side →
    ∀ holes, RepresentativePacking holes L →
    (sourceRoster caseId).toFinset = holes.toFinsetᶜ → False
  neighbour_dispatch : ∀ caseId, caseId ∈ [1447, 7220, 7223, 7255] →
    ∀ L, L < EndpointGeometry.side → ∀ holes, RepresentativePacking holes L →
    (sourceRoster caseId).toFinset = holes.toFinsetᶜ → False
  /- This field includes the family reflection, owner permutation, cell seeding,
  OPEN trace acceptance, and the half-plane-to-polygon terminal cover. -/
  capture_dispatch : ∀ L, L < EndpointGeometry.side → ∀ holes,
    RepresentativePacking holes L → (sourceRoster 1442).toFinset = holes.toFinsetᶜ →
    ∃ p : Fin 17 → AnglePose,
      Represents (stateDomains CaptureChart.terminalState) p ∧
      (∀ i, (p i).square ⊆ traceBox L CaptureChart.terminalSigma) ∧
      (∀ i j, i ≠ j → Disjoint (interior (p i).square) (interior (p j).square))

theorem lower_bound (tree : FiniteOrbitCover.RepTree)
    (patterns fullCases sourceRoster : ℕ → List (Fin 24))
    (sourceCase : ℕ → ℕ) (ordinary : ℕ → Prop)
    (obligations : Obligations tree patterns fullCases sourceRoster sourceCase ordinary)
    (L : ℝ) (c u : Fin 17 → ℝ × ℝ)
    (hu : ∀ i, (u i).1^2 + (u i).2^2 = 1)
    (hf : ∀ i, Sq17.sq (c i).1 (c i).2 (u i).1 (u i).2 ⊆ containerBox L)
    (hd : ∀ i j, i ≠ j → Disjoint
      (interior (Sq17.sq (c i).1 (c i).2 (u i).1 (u i).2))
      (interior (Sq17.sq (c j).1 (c j).2 (u j).1 (u j).2))) :
    EndpointGeometry.side ≤ L := by
  by_contra hn
  have hL : L < EndpointGeometry.side := lt_of_not_ge hn
  have hcover : L ≤ 1169/250 := by
    have hb := EndpointIntervals.side_decimal_bounds.2
    linarith
  obtain ⟨g, holes, hholes, hcard, assigned, hinj, hplace, hunit, hfit, hdis⟩ :=
    packing_reaches_trace_table_exact tree obligations.census L 0 hcover c u hu hf hd
  let P : RepresentativePacking holes L :=
    ⟨(fun i => traceCentre g L 0 (c i)), (fun i => CellSymmetry.direction g (u i)),
      assigned, hcard, hinj, (fun i => (hplace i).1), (fun i => (hplace i).2),
      hunit, hfit, hdis⟩
  obtain ⟨a, ha⟩ := obligations.classification holes hholes
  cases a with
  | pattern index symmetry =>
    exact obligations.pattern_dispatch L hL holes P index symmetry ha
  | full k =>
    have hm : (fullCases k).length = 17 ∧ (fullCases k).Nodup ∧
        (fullCases k).toFinset = holes.toFinsetᶜ := ha
    have hroster : (sourceRoster (sourceCase k)).toFinset = holes.toFinsetᶜ := by
      rw [← obligations.source_roster k]
      exact hm.2.2
    rcases obligations.full_route k hm.1 with ho | hn | hc
    · exact obligations.ordinary_dispatch (sourceCase k) ho L hL holes P hroster
    · exact obligations.neighbour_dispatch (sourceCase k) hn L hL holes P hroster
    · rw [hc] at hroster
      obtain ⟨p, hr, hf, hd⟩ := obligations.capture_dispatch L hL holes P hroster
      have heq := CaptureChart.side_eq_of_terminal_representation L p hL.le hr hf hd
      exact (ne_of_lt hL) heq

def Feasible (L : ℝ) : Prop := ∃ c u : Fin 17 → ℝ × ℝ,
  (∀ i, (u i).1^2 + (u i).2^2 = 1) ∧
  (∀ i, Sq17.sq (c i).1 (c i).2 (u i).1 (u i).2 ⊆ containerBox L) ∧
  (∀ i j, i ≠ j → Disjoint
    (interior (Sq17.sq (c i).1 (c i).2 (u i).1 (u i).2))
    (interior (Sq17.sq (c j).1 (c j).2 (u j).1 (u j).2)))

/-- Intended final statement: a packing exists exactly at and above the exact
algebraic side. Still conditional on ALL named assembly obligations. -/
theorem feasible_iff (tree : FiniteOrbitCover.RepTree)
    (patterns fullCases sourceRoster : ℕ → List (Fin 24))
    (sourceCase : ℕ → ℕ) (ordinary : ℕ → Prop)
    (obligations : Obligations tree patterns fullCases sourceRoster sourceCase ordinary)
    (L : ℝ) : Feasible L ↔ EndpointGeometry.side ≤ L := by
  constructor
  · rintro ⟨c, u, hu, hf, hd⟩
    exact lower_bound tree patterns fullCases sourceRoster sourceCase ordinary
      obligations L c u hu hf hd
  · intro hL
    refine ⟨EndpointGeometry.centres, EndpointGeometry.directions,
      EndpointGeometry.directions_unit, ?_, EndpointGeometry.squares_disjoint⟩
    intro i z hz
    obtain ⟨hx0, hx1, hy0, hy1⟩ := EndpointGeometry.squares_contained i hz
    exact ⟨hx0, hx1.trans hL, hy0, hy1.trans hL⟩

end Sq17.HalfPlaneAssembly

#print axioms Sq17.HalfPlaneAssembly.feasible_iff
