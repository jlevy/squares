import ElevenSquare.Geometry
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

namespace ElevenSquare

noncomputable section

theorem normSq_nonneg (p : Point) : 0 ≤ normSq p := by
  unfold normSq dot
  nlinarith [sq_nonneg p.1, sq_nonneg p.2]

theorem dot_comm (p q : Point) : dot p q = dot q p := by
  unfold dot
  ring

theorem dot_perp_self (p : Point) : dot p (perp p) = 0 := by
  unfold dot perp
  ring

theorem normSq_perp (p : Point) : normSq (perp p) = normSq p := by
  unfold normSq dot perp
  ring

theorem orthogonal_decomposition (p a : Point) (ha : normSq a = 1) :
    (dot p a)^2 + (dot p (perp a))^2 = normSq p := by
  calc
    (dot p a)^2 + (dot p (perp a))^2 = normSq p * normSq a := by
      dsimp [normSq, dot, perp]
      ring
    _ = normSq p := by rw [ha, mul_one]

theorem coordinate_reconstruction (p a : Point) (ha : normSq a = 1) :
    p = (dot p a * a.1 + dot p (perp a) * (perp a).1,
         dot p a * a.2 + dot p (perp a) * (perp a).2) := by
  dsimp [normSq, dot, perp] at *
  apply Prod.ext <;> dsimp
  · nlinarith [congrArg (fun x : ℝ => p.1 * x) ha]
  · nlinarith [congrArg (fun x : ℝ => p.2 * x) ha]

theorem closed_of_normSq_le (q : UnitSquare) (p : Point)
    (h : normSq (p - q.center) ≤ 1 / 4) : ClosedSquare q p := by
  have he := orthogonal_decomposition (p - q.center) q.axis q.axis_unit
  change (localX q p)^2 + (localY q p)^2 = normSq (p - q.center) at he
  constructor
  · apply abs_le.mpr
    constructor <;> nlinarith [sq_nonneg (localY q p)]
  · apply abs_le.mpr
    constructor <;> nlinarith [sq_nonneg (localX q p)]

theorem open_of_normSq_lt (q : UnitSquare) (p : Point)
    (h : normSq (p - q.center) < 1 / 4) : OpenSquare q p := by
  have he := orthogonal_decomposition (p - q.center) q.axis q.axis_unit
  change (localX q p)^2 + (localY q p)^2 = normSq (p - q.center) at he
  constructor
  · apply abs_lt.mpr
    constructor <;> nlinarith [sq_nonneg (localY q p)]
  · apply abs_lt.mpr
    constructor <;> nlinarith [sq_nonneg (localX q p)]

theorem OpenSquare.closed {q : UnitSquare} {p : Point} (h : OpenSquare q p) :
    ClosedSquare q p := ⟨le_of_lt h.1, le_of_lt h.2⟩

theorem center_mem (q : UnitSquare) : ClosedSquare q q.center := by
  norm_num [ClosedSquare, localX, localY, dot]

theorem Packing.center_separation {n : ℕ} {S : ℝ} (P : Packing n S)
    (i j : Fin n) (hij : i ≠ j) :
    1 ≤ normSq ((P.squares i).center - (P.squares j).center) := by
  by_contra hn
  have hlt : normSq ((P.squares i).center - (P.squares j).center) < 1 :=
    lt_of_not_ge hn
  let p : Point := (((P.squares i).center.1 + (P.squares j).center.1) / 2,
                   ((P.squares i).center.2 + (P.squares j).center.2) / 2)
  have hi : normSq (p - (P.squares i).center) =
      normSq ((P.squares i).center - (P.squares j).center) / 4 := by
    dsimp [p, normSq, dot]
    ring
  have hj : normSq (p - (P.squares j).center) =
      normSq ((P.squares i).center - (P.squares j).center) / 4 := by
    dsimp [p, normSq, dot]
    ring
  exact P.interior_disjoint i j hij p
    ⟨open_of_normSq_lt _ _ (by rw [hi]; linarith),
     open_of_normSq_lt _ _ (by rw [hj]; linarith)⟩

theorem Packing.center_bounds {n : ℕ} {S : ℝ} (P : Packing n S) (i : Fin n) :
    1 / 2 ≤ (P.squares i).center.1 ∧ (P.squares i).center.1 ≤ S - 1 / 2 ∧
    1 / 2 ≤ (P.squares i).center.2 ∧ (P.squares i).center.2 ≤ S - 1 / 2 := by
  have left := P.contained i
    ((P.squares i).center.1 - 1 / 2, (P.squares i).center.2)
    (closed_of_normSq_le _ _ (by norm_num [normSq, dot]))
  have right := P.contained i
    ((P.squares i).center.1 + 1 / 2, (P.squares i).center.2)
    (closed_of_normSq_le _ _ (by norm_num [normSq, dot]))
  have bottom := P.contained i
    ((P.squares i).center.1, (P.squares i).center.2 - 1 / 2)
    (closed_of_normSq_le _ _ (by norm_num [normSq, dot]))
  have top := P.contained i
    ((P.squares i).center.1, (P.squares i).center.2 + 1 / 2)
    (closed_of_normSq_le _ _ (by norm_num [normSq, dot]))
  dsimp [InContainer] at left right bottom top
  constructor
  · linarith [left.1]
  constructor
  · linarith [right.2.1]
  constructor
  · linarith [bottom.2.2.1]
  · linarith [top.2.2.2]

def projectionRadius (q : UnitSquare) (v : Point) : ℝ :=
  (|dot q.axis v| + |dot (perp q.axis) v|) / 2

theorem dot_reconstruction (q : UnitSquare) (p v : Point) :
    dot (p - q.center) v =
      localX q p * dot q.axis v + localY q p * dot (perp q.axis) v := by
  have h := coordinate_reconstruction (p - q.center) q.axis q.axis_unit
  have hx := congrArg Prod.fst h
  have hy := congrArg Prod.snd h
  dsimp [dot, localX, localY, perp] at *
  nlinarith [congrArg (fun x : ℝ => x * v.1) hx,
    congrArg (fun x : ℝ => x * v.2) hy]

theorem closed_projection_bound {q : UnitSquare} {p : Point}
    (h : ClosedSquare q p) (v : Point) :
    |dot (p - q.center) v| ≤ projectionRadius q v := by
  rw [dot_reconstruction]
  calc
    |localX q p * dot q.axis v + localY q p * dot (perp q.axis) v|
        ≤ |localX q p * dot q.axis v| + |localY q p * dot (perp q.axis) v| :=
      abs_add_le _ _
    _ = |localX q p| * |dot q.axis v| + |localY q p| * |dot (perp q.axis) v| := by
      rw [abs_mul, abs_mul]
    _ ≤ (1 / 2) * |dot q.axis v| + (1 / 2) * |dot (perp q.axis) v| :=
      add_le_add (mul_le_mul_of_nonneg_right h.1 (abs_nonneg _))
        (mul_le_mul_of_nonneg_right h.2 (abs_nonneg _))
    _ = projectionRadius q v := by unfold projectionRadius; ring

theorem open_projection_lt {q : UnitSquare} {p : Point}
    (h : OpenSquare q p) (v : Point) (hv : 0 < normSq v) :
    |dot (p - q.center) v| < projectionRadius q v := by
  have he := orthogonal_decomposition v q.axis q.axis_unit
  rw [dot_comm v q.axis, dot_comm v (perp q.axis)] at he
  have hpos : 0 < |dot q.axis v| + |dot (perp q.axis) v| := by
    by_contra hn
    have hz₁ : |dot q.axis v| = 0 := by
      nlinarith [abs_nonneg (dot q.axis v), abs_nonneg (dot (perp q.axis) v)]
    have hz₂ : |dot (perp q.axis) v| = 0 := by
      nlinarith [abs_nonneg (dot q.axis v), abs_nonneg (dot (perp q.axis) v)]
    rw [abs_eq_zero.mp hz₁, abs_eq_zero.mp hz₂] at he
    norm_num at he
    linarith
  have hsum : |localX q p| * |dot q.axis v| +
      |localY q p| * |dot (perp q.axis) v| < projectionRadius q v := by
    unfold projectionRadius
    rcases lt_or_eq_of_le (abs_nonneg (dot q.axis v)) with hp | hz
    · have h₁ := mul_lt_mul_of_pos_right h.1 hp
      have h₂ := mul_le_mul_of_nonneg_right (le_of_lt h.2)
        (abs_nonneg (dot (perp q.axis) v))
      linarith
    · have hp₂ : 0 < |dot (perp q.axis) v| := by linarith
      have h₂ := mul_lt_mul_of_pos_right h.2 hp₂
      have h₁ := mul_le_mul_of_nonneg_right (le_of_lt h.1)
        (abs_nonneg (dot q.axis v))
      linarith
  rw [dot_reconstruction]
  exact lt_of_le_of_lt (by simpa only [abs_mul] using
    (abs_add_le (localX q p * dot q.axis v) (localY q p * dot (perp q.axis) v))) hsum

theorem separated_interiors (a b : UnitSquare) (v : Point)
    (hv : 0 < normSq v)
    (hsep : projectionRadius a v + projectionRadius b v ≤ dot (b.center - a.center) v) :
    ∀ p, ¬ (OpenSquare a p ∧ OpenSquare b p) := by
  intro p hp
  have ha := (abs_lt.mp (open_projection_lt hp.1 v hv)).2
  have hb := (abs_lt.mp (open_projection_lt hp.2 v hv)).1
  have hid : dot (b.center - a.center) v =
      dot (p - a.center) v - dot (p - b.center) v := by
    dsimp [dot]
    ring
  linarith

def halfWidth (q : UnitSquare) : ℝ := (|q.axis.1| + |q.axis.2|) / 2

theorem projectionRadius_horizontal (q : UnitSquare) :
    projectionRadius q (1, 0) = halfWidth q := by
  simp [projectionRadius, halfWidth, dot, perp]

theorem projectionRadius_vertical (q : UnitSquare) :
    projectionRadius q (0, 1) = halfWidth q := by
  simp [projectionRadius, halfWidth, dot, perp, add_comm]

theorem projectionRadius_axis (q : UnitSquare) : projectionRadius q q.axis = 1 / 2 := by
  have h := q.axis_unit
  change dot q.axis q.axis = 1 at h
  have hp : dot (perp q.axis) q.axis = 0 := by rw [dot_comm]; exact dot_perp_self _
  simp [projectionRadius, h, hp]

theorem projectionRadius_perp_axis (q : UnitSquare) :
    projectionRadius q (perp q.axis) = 1 / 2 := by
  have hp : dot (perp q.axis) (perp q.axis) = 1 := by
    change normSq (perp q.axis) = 1
    rw [normSq_perp, q.axis_unit]
  simp [projectionRadius, dot_perp_self, hp]

theorem contained_of_center_bounds (q : UnitSquare) (S : ℝ)
    (hx₀ : halfWidth q ≤ q.center.1) (hx₁ : q.center.1 + halfWidth q ≤ S)
    (hy₀ : halfWidth q ≤ q.center.2) (hy₁ : q.center.2 + halfWidth q ≤ S) :
    ∀ p, ClosedSquare q p → InContainer S p := by
  intro p hp
  have hx := closed_projection_bound hp (1, 0)
  have hy := closed_projection_bound hp (0, 1)
  rw [projectionRadius_horizontal] at hx
  rw [projectionRadius_vertical] at hy
  simp only [dot, Prod.fst_sub, Prod.snd_sub, mul_one, mul_zero, add_zero, zero_add] at hx hy
  rcases abs_le.mp hx with ⟨hx₂, hx₃⟩
  rcases abs_le.mp hy with ⟨hy₂, hy₃⟩
  unfold InContainer
  exact ⟨by linarith, by linarith, by linarith, by linarith⟩

def Packing.enlarge {n : ℕ} {S U : ℝ} (P : Packing n S) (hSU : S ≤ U) : Packing n U where
  squares := P.squares
  side_nonneg := le_trans P.side_nonneg hSU
  contained := by
    intro i p hp
    rcases P.contained i p hp with ⟨hx₀, hx₁, hy₀, hy₁⟩
    exact ⟨hx₀, le_trans hx₁ hSU, hy₀, le_trans hy₁ hSU⟩
  interior_disjoint := P.interior_disjoint

theorem localX_translated (q : UnitSquare) (v p : Point) :
    localX (translatedSquare q v) p = localX q (p - v) := by
  dsimp [localX, translatedSquare, dot]
  ring

theorem localY_translated (q : UnitSquare) (v p : Point) :
    localY (translatedSquare q v) p = localY q (p - v) := by
  dsimp [localY, translatedSquare, dot, perp]
  ring

theorem closed_translated (q : UnitSquare) (v p : Point) :
    ClosedSquare (translatedSquare q v) p ↔ ClosedSquare q (p - v) := by
  simp only [ClosedSquare, localX_translated, localY_translated]

theorem open_translated (q : UnitSquare) (v p : Point) :
    OpenSquare (translatedSquare q v) p ↔ OpenSquare q (p - v) := by
  simp only [OpenSquare, localX_translated, localY_translated]

/-- Embed a packing in a larger container with the two container centres aligned. -/
def Packing.enlargeCentered {n : ℕ} {S U : ℝ} (P : Packing n S)
    (hSU : S ≤ U) : Packing n U where
  squares i := translatedSquare (P.squares i) ((U - S) / 2, (U - S) / 2)
  side_nonneg := le_trans P.side_nonneg hSU
  contained := by
    intro i p hp
    have hold := P.contained i (p - ((U - S) / 2, (U - S) / 2))
      ((closed_translated _ _ _).mp hp)
    dsimp [InContainer] at hold ⊢
    exact ⟨by linarith [hold.1], by linarith [hold.2.1],
      by linarith [hold.2.2.1], by linarith [hold.2.2.2]⟩
  interior_disjoint := by
    intro i j hij p hp
    exact P.interior_disjoint i j hij (p - ((U - S) / 2, (U - S) / 2))
      ⟨(open_translated _ _ _).mp hp.1, (open_translated _ _ _).mp hp.2⟩

end

end ElevenSquare
