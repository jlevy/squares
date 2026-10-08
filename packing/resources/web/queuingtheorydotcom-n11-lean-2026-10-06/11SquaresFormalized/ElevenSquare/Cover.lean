import Mathlib.Data.Finset.Max
import ElevenSquare.BasicGeometry
import Mathlib.Data.Finset.Lattice.Basic
import Mathlib.Data.Finset.Card
import Mathlib.Data.Fintype.Fin
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Choose
import ElevenSquare.GeneratedCover0
import ElevenSquare.GeneratedCover1
import ElevenSquare.GeneratedCover2
import ElevenSquare.GeneratedCover3

noncomputable section
namespace ElevenSquare

def InUnitBox (p : Point) : Prop :=
  0 ≤ p.1 ∧ p.1 ≤ 1 ∧ 0 ≤ p.2 ∧ p.2 ≤ 1

/-- Closed nearest-site cells; ties are deliberately retained. -/
def ClosedCell (i : Fin 16) (p : Point) : Prop :=
  InUnitBox p ∧ ∀ j : Fin 16,
    coordinateDistanceSq p (coverSite i) ≤ coordinateDistanceSq p (coverSite j)

theorem unit_box_covered : BoxCovered 0 0 1 := by
  apply boxCovered_split
  · convert coverQuadrant0 using 1 <;> norm_num
  · convert coverQuadrant1 using 1 <;> norm_num
  · convert coverQuadrant2 using 1 <;> norm_num
  · convert coverQuadrant3 using 1 <;> norm_num

theorem exists_closedCell (p : Point) (hp : InUnitBox p) :
    ∃ i : Fin 16, ClosedCell i p := by
  obtain ⟨i, _, hi⟩ := Finset.exists_min_image (Finset.univ : Finset (Fin 16))
    (fun i => coordinateDistanceSq p (coverSite i)) Finset.univ_nonempty
  exact ⟨i, hp, fun j => hi j (Finset.mem_univ j)⟩

theorem closedCell_radius {i : Fin 16} {p : Point} (hp : ClosedCell i p) :
    coordinateDistanceSq p (coverSite i) ≤ coverRadius^2 := by
  obtain ⟨j, hj⟩ := unit_box_covered p hp.1.1 (by simpa using hp.1.2.1)
    hp.1.2.2.1 (by simpa using hp.1.2.2.2)
  exact le_trans (hp.2 j) hj

theorem coordinateDistanceSq_le_twice (p q c : Point) :
    coordinateDistanceSq p q ≤
      2 * (coordinateDistanceSq p c + coordinateDistanceSq q c) := by
  unfold coordinateDistanceSq
  nlinarith [sq_nonneg (p.1 + q.1 - 2*c.1), sq_nonneg (p.2 + q.2 - 2*c.2)]

theorem closedCell_diameter {i : Fin 16} {p q : Point}
    (hp : ClosedCell i p) (hq : ClosedCell i q) :
    coordinateDistanceSq p q ≤ 4 * coverRadius^2 := by
  have h1 := closedCell_radius hp
  have h2 := closedCell_radius hq
  have h3 := coordinateDistanceSq_le_twice p q (coverSite i)
  linarith

theorem coverCap_gt_one : 1 < coverCap := by norm_num [coverCap]

def normalizeCenter (p : Point) : Point :=
  ((p.1 - 1/2) / (coverCap-1), (p.2-1/2) / (coverCap-1))

theorem center_in_unit_box {n : ℕ} {S : ℝ} (P : Packing n S)
    (hS : S ≤ coverCap) (i : Fin n) : InUnitBox (normalizeCenter (P.squares i).center) := by
  have hc := P.center_bounds i
  have hu : 0 < coverCap-1 := sub_pos.mpr coverCap_gt_one
  unfold InUnitBox normalizeCenter
  simp only [Prod.fst, Prod.snd]
  refine ⟨div_nonneg (by linarith) hu.le, (div_le_one hu).2 ?_,
    div_nonneg (by linarith) hu.le, (div_le_one hu).2 ?_⟩ <;> linarith

theorem normalized_distance (p q : Point) :
    coordinateDistanceSq p q = (coverCap-1)^2 *
      coordinateDistanceSq (normalizeCenter p) (normalizeCenter q) := by
  have hu : coverCap-1 ≠ 0 := ne_of_gt (sub_pos.mpr coverCap_gt_one)
  unfold coordinateDistanceSq normalizeCenter
  simp only [Prod.fst, Prod.snd]
  field_simp [hu]
  <;> ring

theorem normSq_sub_eq_distance (p q : Point) : normSq (p-q) = coordinateDistanceSq p q := by
  simp [normSq, dot, coordinateDistanceSq, pow_two]

/-- This is a property of the concrete sixteen cells, not a hypothesis. -/
theorem closedCell_capacity {n : ℕ} {S : ℝ} (P : Packing n S)
    {i j : Fin n} {k : Fin 16}
    (hi : ClosedCell k (normalizeCenter (P.squares i).center))
    (hj : ClosedCell k (normalizeCenter (P.squares j).center)) : i = j := by
  by_contra hij
  have hsep := P.center_separation i j hij
  rw [normSq_sub_eq_distance, normalized_distance] at hsep
  have hd := closedCell_diameter hi hj
  have hm := mul_le_mul_of_nonneg_left hd (sq_nonneg (coverCap-1))
  have hc : (coverCap-1)^2 * (4*coverRadius^2) < 1 := by
    norm_num [coverCap, coverRadius]
  linarith

def Occupies {S : ℝ} (P : Packing 11 S) (m : Finset (Fin 16)) : Prop :=
  ∃ a : Fin 11 → Fin 16, Function.Injective a ∧ Finset.univ.image a = m ∧
    ∀ i, ClosedCell (a i) (normalizeCenter (P.squares i).center)

theorem packing_occupies_eleven_cells {S : ℝ} (P : Packing 11 S) (hS : S ≤ coverCap) :
    ∃ m : Finset (Fin 16), m.card = 11 ∧ Occupies P m := by
  have h : ∀ i : Fin 11, ∃ k : Fin 16, ClosedCell k (normalizeCenter (P.squares i).center) :=
    fun i => exists_closedCell _ (center_in_unit_box P hS i)
  choose a ha using h
  have hinj : Function.Injective a := by
    intro i j hij
    exact closedCell_capacity P (ha i) (by rw [hij]; exact ha j)
  refine ⟨Finset.univ.image a, ?_, a, hinj, rfl, ha⟩
  rw [Finset.card_image_of_injective _ hinj]
  simp

def turnPoint (p : Point) : Point := (1-p.1, 1-p.2)

theorem coverSite_halfTurn (i : Fin 16) : coverSite i.rev = turnPoint (coverSite i) := by
  fin_cases i <;> norm_num [coverSite, turnPoint, Fin.rev]

theorem turnPoint_distance (p q : Point) :
    coordinateDistanceSq (turnPoint p) (turnPoint q) = coordinateDistanceSq p q := by
  unfold coordinateDistanceSq turnPoint
  simp only [Prod.fst, Prod.snd]
  ring

theorem closedCell_halfTurn {i : Fin 16} {p : Point} (hp : ClosedCell i p) :
    ClosedCell i.rev (turnPoint p) := by
  refine ⟨?_, ?_⟩
  · rcases hp.1 with ⟨hx0,hx1,hy0,hy1⟩
    unfold InUnitBox turnPoint
    simp only [Prod.fst, Prod.snd]
    exact ⟨by linarith, by linarith, by linarith, by linarith⟩
  · intro j
    rw [coverSite_halfTurn, turnPoint_distance]
    have hj := coverSite_halfTurn j.rev
    rw [Fin.rev_rev] at hj
    rw [hj, turnPoint_distance]
    exact hp.2 j.rev

end ElevenSquare
end
