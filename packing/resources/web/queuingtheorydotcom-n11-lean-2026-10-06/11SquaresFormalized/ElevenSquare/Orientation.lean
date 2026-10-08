import ElevenSquare.Geometry
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Choose

/-!
# Complete square-orientation chart

Quarter turns of a square's local axis preserve the actual closed square and
its open interior. Every square therefore has a first-quadrant representative,
which is parameterized by the closed half-angle interval `0 ≤ t ≤ 1`.
No orientations, including the chart endpoints, are omitted.
-/

namespace ElevenSquare

structure SameSquare (q r : UnitSquare) : Prop where
  center_eq : q.center = r.center
  closed_iff : ∀ p, ClosedSquare q p ↔ ClosedSquare r p
  open_iff : ∀ p, OpenSquare q p ↔ OpenSquare r p

theorem SameSquare.refl (q : UnitSquare) : SameSquare q q :=
  ⟨rfl, fun _ => Iff.rfl, fun _ => Iff.rfl⟩

theorem SameSquare.trans {q r s : UnitSquare}
    (h : SameSquare q r) (k : SameSquare r s) : SameSquare q s :=
  ⟨h.center_eq.trans k.center_eq,
   fun p => (h.closed_iff p).trans (k.closed_iff p),
   fun p => (h.open_iff p).trans (k.open_iff p)⟩

def quarterTurn (q : UnitSquare) : UnitSquare where
  center := q.center
  axis := perp q.axis
  axis_unit := by
    have h := q.axis_unit
    dsimp [normSq, dot, perp] at *
    nlinarith

@[simp] theorem quarterTurn_center (q : UnitSquare) :
    (quarterTurn q).center = q.center := rfl

@[simp] theorem quarterTurn_localX (q : UnitSquare) (p : Point) :
    localX (quarterTurn q) p = localY q p := rfl

@[simp] theorem quarterTurn_localY (q : UnitSquare) (p : Point) :
    localY (quarterTurn q) p = -localX q p := by
  dsimp [localX, localY, quarterTurn, perp, dot]
  ring

theorem quarterTurn_sameSquare (q : UnitSquare) : SameSquare q (quarterTurn q) := by
  refine ⟨rfl, ?_, ?_⟩
  · intro p
    simp only [ClosedSquare, quarterTurn_localX, quarterTurn_localY, abs_neg]
    exact and_comm
  · intro p
    simp only [OpenSquare, quarterTurn_localX, quarterTurn_localY, abs_neg]
    exact and_comm

theorem exists_firstQuadrant (q : UnitSquare) :
    ∃ r : UnitSquare, SameSquare q r ∧ 0 ≤ r.axis.1 ∧ 0 ≤ r.axis.2 := by
  by_cases hx : 0 ≤ q.axis.1
  · by_cases hy : 0 ≤ q.axis.2
    · exact ⟨q, SameSquare.refl q, hx, hy⟩
    · refine ⟨quarterTurn q, quarterTurn_sameSquare q, ?_, ?_⟩
      · change 0 ≤ -q.axis.2
        linarith
      · exact hx
  · by_cases hy : 0 ≤ q.axis.2
    · refine ⟨quarterTurn (quarterTurn (quarterTurn q)),
        (quarterTurn_sameSquare q).trans
          ((quarterTurn_sameSquare (quarterTurn q)).trans
            (quarterTurn_sameSquare (quarterTurn (quarterTurn q)))), ?_, ?_⟩
      · simpa [quarterTurn, perp] using hy
      · change 0 ≤ -q.axis.1
        linarith
    · refine ⟨quarterTurn (quarterTurn q),
        (quarterTurn_sameSquare q).trans (quarterTurn_sameSquare (quarterTurn q)), ?_, ?_⟩
      · change 0 ≤ -q.axis.1
        linarith
      · change 0 ≤ -q.axis.2
        linarith

noncomputable def halfAngleAxis (t : ℝ) : Point :=
  ((1 - t^2) / (1 + t^2), (2 * t) / (1 + t^2))

theorem halfAngleAxis_unit (t : ℝ) : normSq (halfAngleAxis t) = 1 := by
  have hd : 1 + t^2 ≠ 0 := by positivity
  dsimp [halfAngleAxis, normSq, dot]
  field_simp [hd] <;> ring

theorem firstQuadrant_halfAngle (a b : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b)
    (hu : a*a + b*b = 1) :
    let t := b / (1 + a)
    0 ≤ t ∧ t ≤ 1 ∧ halfAngleAxis t = (a, b) := by
  have hd : 0 < 1 + a := by linarith
  have hb1 : b ≤ 1 := by nlinarith [sq_nonneg a]
  have ht0 : 0 ≤ b / (1 + a) := div_nonneg hb (le_of_lt hd)
  have ht1 : b / (1 + a) ≤ 1 := by
    apply (div_le_iff₀ hd).2
    linarith
  refine ⟨ht0, ht1, ?_⟩
  have he : 1 + (b / (1 + a))^2 = 2 / (1 + a) := by
    field_simp [ne_of_gt hd]
    nlinarith
  have hc : 1 - (b / (1 + a))^2 = 2*a / (1 + a) := by
    field_simp [ne_of_gt hd]
    nlinarith
  apply Prod.ext <;> dsimp [halfAngleAxis]
  · rw [he, hc]
    field_simp [ne_of_gt hd]
  · rw [he]
    field_simp [ne_of_gt hd]

/-- Every arbitrary orientation has a shape-equivalent representative in the
closed rational half-angle chart. The center is unchanged. -/
theorem orientation_chart_complete (q : UnitSquare) :
    ∃ t : ℝ, ∃ r : UnitSquare,
      0 ≤ t ∧ t ≤ 1 ∧ r.axis = halfAngleAxis t ∧ SameSquare q r := by
  obtain ⟨r, hsame, hx, hy⟩ := exists_firstQuadrant q
  have hu : r.axis.1 * r.axis.1 + r.axis.2 * r.axis.2 = 1 := r.axis_unit
  obtain ⟨ht0, ht1, haxis⟩ := firstQuadrant_halfAngle r.axis.1 r.axis.2 hx hy hu
  exact ⟨r.axis.2 / (1 + r.axis.1), r, ht0, ht1, haxis.symm, hsame⟩

@[simp] theorem halfAngleAxis_zero : halfAngleAxis 0 = (1, 0) := by
  norm_num [halfAngleAxis]

@[simp] theorem halfAngleAxis_one : halfAngleAxis 1 = (0, 1) := by
  norm_num [halfAngleAxis]

/-- Replacing each local axis by an equivalent chart representative preserves
all actual containment and interior-disjointness conditions. -/
theorem Packing.exists_chart {n : ℕ} {S : ℝ} (P : Packing n S) :
    ∃ (R : Packing n S) (t : Fin n → ℝ),
      (∀ i, 0 ≤ t i ∧ t i ≤ 1 ∧ (R.squares i).axis = halfAngleAxis (t i)) ∧
      (∀ i, SameSquare (P.squares i) (R.squares i)) := by
  classical
  choose t r ht0 ht1 haxis hsame using fun i => orientation_chart_complete (P.squares i)
  let R : Packing n S := {
    squares := r
    side_nonneg := P.side_nonneg
    contained := by
      intro i p hp
      exact P.contained i p ((hsame i).closed_iff p |>.mpr hp)
    interior_disjoint := by
      intro i j hij p hp
      exact P.interior_disjoint i j hij p
        ⟨((hsame i).open_iff p).mpr hp.1, ((hsame j).open_iff p).mpr hp.2⟩ }
  exact ⟨R, t, fun i => ⟨ht0 i, ht1 i, haxis i⟩, hsame⟩

end ElevenSquare
