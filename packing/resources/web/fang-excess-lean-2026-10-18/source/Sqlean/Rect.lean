import Sqlean.Vendor.ExactPack

/-!
# Rectangular containers and the far-pair shortcut

* `containerR W H = [0, W] × [0, H]`, `PacksR n W H`; `Packs n s ↔ PacksR n s s` is `Iff.rfl`.
* `InBoxR`: the four corners in `[0, W] × [0, H]` (`InBox` of `ExactPack.lean` with two sides).
* `disjoint_of_far`: unit squares whose centres are more than `√2` apart have disjoint interiors
  (each interior lies in the open disc of radius `1/√2` about its centre).
* `packsR_of_cert`: `packs_of_cert` for rectangles, where a pair may be certified either by a
  separating side (`SepPair`) or by `(xi - xj)² + (yi - yj)² > 2`.
-/

open Set

namespace UnitSquarePacking

/-- The container `[0, W] × [0, H]`. -/
def containerR (W H : ℝ) : Set (ℝ × ℝ) := Icc 0 W ×ˢ Icc 0 H

/-- `n` unit squares can be packed in `[0, W] × [0, H]`. -/
def PacksR (n : ℕ) (W H : ℝ) : Prop :=
  ∃ (c : Fin n → ℝ × ℝ) (θ : Fin n → ℝ), (∀ i, unitSq (c i) (θ i) ⊆ containerR W H) ∧
    Pairwise fun i j => Disjoint (interior (unitSq (c i) (θ i))) (interior (unitSq (c j) (θ j)))

theorem packs_iff_packsR {n : ℕ} {s : ℝ} : Packs n s ↔ PacksR n s s := Iff.rfl

/-- The four corners of the square `(x, y, c, s)` lie in `[0, W] × [0, H]`. -/
def InBoxR (W H x y c s : ℝ) : Prop :=
  ∀ a b, Half a → Half b →
    0 ≤ x + c * a - s * b ∧ x + c * a - s * b ≤ W ∧ 0 ≤ y + s * a + c * b ∧ y + s * a + c * b ≤ H

lemma unitSq_subset_containerR {W H x y c s θ : ℝ} (hc : Real.cos θ = c) (hs : Real.sin θ = s)
    (h : InBoxR W H x y c s) : unitSq (x, y) θ ⊆ containerR W H := by
  rintro p ⟨q, ⟨⟨h1, h2⟩, h3, h4⟩, rfl⟩
  simp only [rot, hc, hs, containerR, mem_prod, mem_Icc, Prod.fst_add, Prod.snd_add]
  refine ⟨⟨?_, ?_⟩, ?_, ?_⟩
  · have := affine_nonneg (A := x) (B := c) (C := -s) ⟨h1, h2⟩ ⟨h3, h4⟩
      (fun a b ha hb => by have := (h a b ha hb).1; linarith)
    linarith
  · have := affine_nonneg (A := W - x) (B := -c) (C := s) ⟨h1, h2⟩ ⟨h3, h4⟩
      (fun a b ha hb => by have := (h a b ha hb).2.1; linarith)
    linarith
  · have := affine_nonneg (A := y) (B := s) (C := c) ⟨h1, h2⟩ ⟨h3, h4⟩
      (fun a b ha hb => by have := (h a b ha hb).2.2.1; linarith)
    linarith
  · have := affine_nonneg (A := H - y) (B := -s) (C := -c) ⟨h1, h2⟩ ⟨h3, h4⟩
      (fun a b ha hb => by have := (h a b ha hb).2.2.2; linarith)
    linarith

/-- An interior point of a unit square is within distance `1/√2` of its centre. -/
lemma dist_sq_lt_of_mem_interior {x y θ : ℝ} {p : ℝ × ℝ} (hp : p ∈ interior (unitSq (x, y) θ)) :
    (p.1 - x) ^ 2 + (p.2 - y) ^ 2 < 1 / 2 := by
  rw [interior_unitSq] at hp
  obtain ⟨h1, h2⟩ := hp
  simp only at h1 h2
  set α := (p.1 - x) * Real.cos θ + (p.2 - y) * Real.sin θ
  set β := -(p.1 - x) * Real.sin θ + (p.2 - y) * Real.cos θ
  have hcs := Real.sin_sq_add_cos_sq θ
  have e : (p.1 - x) ^ 2 + (p.2 - y) ^ 2 = α ^ 2 + β ^ 2 := by
    simp only [α, β]; linear_combination (-((p.1 - x) ^ 2 + (p.2 - y) ^ 2)) * hcs
  have ha : α ^ 2 < 1 / 4 := by
    have := sq_abs α; nlinarith [abs_nonneg α]
  have hb : β ^ 2 < 1 / 4 := by
    have := sq_abs β; nlinarith [abs_nonneg β]
  linarith

/-- **Far pairs.** Unit squares whose centres are more than `√2` apart have disjoint interiors. -/
lemma disjoint_of_far {xi yi θi xj yj θj : ℝ} (h : 2 < (xi - xj) ^ 2 + (yi - yj) ^ 2) :
    Disjoint (interior (unitSq (xi, yi) θi)) (interior (unitSq (xj, yj) θj)) := by
  rw [Set.disjoint_left]
  intro p hpi hpj
  have h1 := dist_sq_lt_of_mem_interior hpi
  have h2 := dist_sq_lt_of_mem_interior hpj
  nlinarith [sq_nonneg (xi + xj - 2 * p.1), sq_nonneg (yi + yj - 2 * p.2)]

/-- **Exact data ⇒ packing in a rectangle**, with the far-pair shortcut. -/
theorem packsR_of_cert {n : ℕ} {W H : ℝ} (x y c s : Fin n → ℝ) (hu : ∀ i, c i ^ 2 + s i ^ 2 = 1)
    (hbox : ∀ i, InBoxR W H (x i) (y i) (c i) (s i))
    (hsep : ∀ i j, i < j → 2 < (x i - x j) ^ 2 + (y i - y j) ^ 2 ∨
      SepPair (x i) (y i) (c i) (s i) (x j) (y j) (c j) (s j)) : PacksR n W H := by
  choose θ hc hs using fun i => exists_angle (hu i)
  refine ⟨fun i => (x i, y i), θ, fun i => unitSq_subset_containerR (hc i) (hs i) (hbox i), ?_⟩
  have pos : ∀ i j, i < j →
      Disjoint (interior (unitSq (x i, y i) (θ i))) (interior (unitSq (x j, y j) (θ j))) := by
    intro i j hij
    rcases hsep i j hij with hf | ⟨k, hk⟩ | ⟨k, hk⟩
    · exact disjoint_of_far hf
    · exact disjoint_of_sepSide (hc i) (hs i) (hc j) (hs j) (hu i) (hu j) hk
    · exact (disjoint_of_sepSide (hc j) (hs j) (hc i) (hs i) (hu j) (hu i) hk).symm
  intro i j hij
  rcases lt_or_gt_of_ne hij with h | h
  · exact pos i j h
  · exact (pos j i h).symm

end UnitSquarePacking
