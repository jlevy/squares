import S12.AuxiliaryPoints
import S12.RawData

namespace S12
open S12Pilot

def AuxExact (q : OpenSquare) (kind : Fin 3) (owned : Finset Nat) : Prop :=
  ∀ i∈List.range (auxPoints kind).length,
    q.Inside ((auxPoints kind)[i]!).1 ((auxPoints kind)[i]!).2 ↔ i∈owned

def auxInsidePoints (kind : Fin 3) (owned : Finset Nat) : List (ℚ × ℚ) :=
  ((List.range (auxPoints kind).length).filter (fun i => decide (i∈owned))).map
    (fun i => (auxPoints kind)[i]!)
def auxOutsidePoints (kind : Fin 3) (owned : Finset Nat) : List (ℚ × ℚ) :=
  ((List.range (auxPoints kind).length).filter (fun i => decide (i∉owned))).map
    (fun i => (auxPoints kind)[i]!)
def markerOutsidePoints (g : Finset Marker) : List (ℚ × ℚ) :=
  ((List.finRange 16).filter (fun i => decide (i∉g))).map marker

def queryInsidePoints (m : Nat) (kind : Fin 3) (owned : Finset Nat) : List (ℚ × ℚ) :=
  seedPoints (maskSupport m) ++ auxInsidePoints kind owned
def queryOutsidePoints (m : Nat) (kind : Fin 3) (owned : Finset Nat) : List (ℚ × ℚ) :=
  markerOutsidePoints (maskSupport m) ++ auxOutsidePoints kind owned

theorem query_inside_sound (m : Nat) (kind : Fin 3) (owned : Finset Nat)
    (q : OpenSquare) (ha : 1<q.side) (hsize : q.side≤1001/1000) (hbox : InsideContainer q)
    (hm : ExactMarkers q (maskSupport m)) (ho : AuxExact q kind owned) :
    ∀ p∈queryInsidePoints m kind owned, q.Inside p.1 p.2 := by
  intro p hp
  rcases List.mem_append.mp hp with hp | hp
  · exact seed_points_sound q ha hsize hbox _ hm p hp
  · obtain ⟨i,hi,rfl⟩ := List.mem_map.mp hp
    obtain ⟨hr,hi'⟩ := List.mem_filter.mp hi
    exact (ho i hr).mpr (of_decide_eq_true hi')

theorem query_outside_sound (m : Nat) (kind : Fin 3) (owned : Finset Nat)
    (q : OpenSquare) (hm : ExactMarkers q (maskSupport m)) (ho : AuxExact q kind owned) :
    ∀ p∈queryOutsidePoints m kind owned, ¬q.Inside p.1 p.2 := by
  intro p hp hi
  rcases List.mem_append.mp hp with hp | hp
  · obtain ⟨i,hi',rfl⟩ := List.mem_map.mp hp
    exact (of_decide_eq_true (List.mem_filter.mp hi').2) ((hm i).mp hi)
  · obtain ⟨i,hi',rfl⟩ := List.mem_map.mp hp
    obtain ⟨hr,hni⟩ := List.mem_filter.mp hi'
    exact (of_decide_eq_true hni) ((ho i hr).mp hi)

structure LocalQuery where
  mask : Nat
  kind : Fin 3
  owned : Finset Nat
  certificate : LocalRejection

def LocalQuery.Check (w : LocalQuery) : Prop :=
  w.certificate.Check (queryInsidePoints w.mask w.kind w.owned) (queryOutsidePoints w.mask w.kind w.owned)
instance LocalQuery.decidableCheck (w : LocalQuery) : Decidable w.Check :=
  inferInstanceAs (Decidable (w.certificate.Check _ _))

/-- A successful local query check rules out the actual geometric ownership
pattern named in its fields, including all boundary conventions. -/
theorem LocalQuery.sound (w : LocalQuery) (hw : w.Check) (q : OpenSquare)
    (ha : 1<q.side) (hsize : q.side≤1001/1000) (hbox : InsideContainer q)
    (hm : ExactMarkers q (maskSupport w.mask)) (ho : AuxExact q w.kind w.owned) : False :=
  w.certificate.sound _ _ hw q ha (query_inside_sound _ _ _ q ha hsize hbox hm ho)
    (query_outside_sound _ _ _ q hm ho)

#print axioms LocalQuery.sound
end S12
