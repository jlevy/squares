import Mathlib

/-!
# Packing unit squares in a square: a common specification

`s(n)` is the side of the smallest square into which `n` unit squares can be packed, rotations
allowed: the squares are closed, lie in the container, and have pairwise disjoint interiors.

* `rot θ` — the rotation of the plane `ℝ × ℝ` by `θ` (written out: `ℝ × ℝ` carries the sup metric,
  so rotations are not `Isometry`s of it).
* `unitSq c θ` — the closed unit square with centre `c` and angle `θ`: the image of
  `[-1/2, 1/2]²` under `p ↦ c + rot θ p`.
* `container s = [0, s]²`.
* `Packs n s` — `n` unit squares fit in `container s`.
* `minSide n = sInf {s | Packs n s}`, i.e. `s(n)`.

Canonical shapes for results about a specific `n` (all three avoid `sInf` conventions):

* exact value: `IsLeast {s | Packs n s} k` (the minimum is attained and equals `k`);
* lower bound: `∀ s, Packs n s → a ≤ s`;
* upper bound: `Packs n b`.

Two characterisations of the squares: `unitSq_eq_setOf` (`p` is in the square iff both rotated
coordinates of `p - c` have absolute value `≤ 1/2`) and `interior_unitSq` (the same with `<`).
-/

namespace UnitSquarePacking

open Set

/-- The rotation of the plane by the angle `θ` (counterclockwise). -/
noncomputable def rot (θ : ℝ) (p : ℝ × ℝ) : ℝ × ℝ :=
  (Real.cos θ * p.1 - Real.sin θ * p.2, Real.sin θ * p.1 + Real.cos θ * p.2)

/-- The closed unit square with centre `c` and angle `θ`. -/
def unitSq (c : ℝ × ℝ) (θ : ℝ) : Set (ℝ × ℝ) :=
  (fun p => c + rot θ p) '' (Icc (-1/2) (1/2) ×ˢ Icc (-1/2) (1/2))

/-- The container `[0, s]²`. -/
def container (s : ℝ) : Set (ℝ × ℝ) := Icc 0 s ×ˢ Icc 0 s

/-- `n` unit squares can be packed in `[0, s]²`: closed squares inside the container, with
pairwise disjoint interiors. -/
def Packs (n : ℕ) (s : ℝ) : Prop :=
  ∃ (c : Fin n → ℝ × ℝ) (θ : Fin n → ℝ), (∀ i, unitSq (c i) (θ i) ⊆ container s) ∧
    Pairwise fun i j => Disjoint (interior (unitSq (c i) (θ i))) (interior (unitSq (c j) (θ j)))

/-- `s(n)`, the least side of a square into which `n` unit squares can be packed. -/
noncomputable def minSide (n : ℕ) : ℝ := sInf {s | Packs n s}

/-! ## The squares as inequalities -/

lemma rot_neg_rot (θ : ℝ) (p : ℝ × ℝ) : rot (-θ) (rot θ p) = p := by
  have h := Real.sin_sq_add_cos_sq θ
  ext <;> simp only [rot, Real.cos_neg, Real.sin_neg]
  · linear_combination p.1 * h
  · linear_combination p.2 * h

lemma continuous_rot (θ : ℝ) : Continuous (rot θ) := by
  unfold rot; fun_prop

/-- `p ↦ c + rot θ p` as a homeomorphism of the plane. -/
noncomputable def place (c : ℝ × ℝ) (θ : ℝ) : (ℝ × ℝ) ≃ₜ (ℝ × ℝ) where
  toFun p := c + rot θ p
  invFun p := rot (-θ) (p - c)
  left_inv p := by simp [rot_neg_rot]
  right_inv p := by
    have h := rot_neg_rot (-θ) (p - c)
    rw [neg_neg] at h
    simp [h]
  continuous_toFun := by have := continuous_rot θ; fun_prop
  continuous_invFun := by have := continuous_rot (-θ); fun_prop

lemma mem_image_place {c : ℝ × ℝ} {θ : ℝ} {S : Set (ℝ × ℝ)} {p : ℝ × ℝ} :
    p ∈ (fun q => c + rot θ q) '' S ↔ rot (-θ) (p - c) ∈ S := by
  change p ∈ place c θ '' S ↔ (place c θ).symm p ∈ S
  rw [(place c θ).image_eq_preimage_symm]; rfl

/-- `p` lies in the closed unit square iff both of its coordinates relative to the square (the
centre moved to `0`, the sides made axis-parallel) have absolute value `≤ 1/2`. -/
theorem unitSq_eq_setOf (c : ℝ × ℝ) (θ : ℝ) :
    unitSq c θ = {p | |(p.1 - c.1) * Real.cos θ + (p.2 - c.2) * Real.sin θ| ≤ 1/2 ∧
                      |-(p.1 - c.1) * Real.sin θ + (p.2 - c.2) * Real.cos θ| ≤ 1/2} := by
  ext p
  rw [unitSq, mem_image_place]
  simp only [rot, Real.cos_neg, Real.sin_neg, mem_prod, mem_Icc,
    mem_ofPred_eq, abs_le, Prod.fst_sub, Prod.snd_sub]
  constructor <;> rintro ⟨⟨h1, h2⟩, h3, h4⟩ <;> refine ⟨⟨?_, ?_⟩, ?_, ?_⟩ <;> linarith

/-- The interior of a unit square: the same inequalities, strict. -/
theorem interior_unitSq (c : ℝ × ℝ) (θ : ℝ) :
    interior (unitSq c θ) =
      {p | |(p.1 - c.1) * Real.cos θ + (p.2 - c.2) * Real.sin θ| < 1/2 ∧
           |-(p.1 - c.1) * Real.sin θ + (p.2 - c.2) * Real.cos θ| < 1/2} := by
  have h : interior (unitSq c θ) =
      (fun p => c + rot θ p) '' (Ioo (-1/2) (1/2) ×ˢ Ioo (-1/2) (1/2)) := by
    rw [unitSq, ← interior_Icc, ← interior_prod_eq]
    exact ((place c θ).image_interior _).symm
  ext p
  rw [h, mem_image_place]
  simp only [rot, Real.cos_neg, Real.sin_neg, mem_prod, mem_Ioo,
    mem_ofPred_eq, abs_lt, Prod.fst_sub, Prod.snd_sub]
  constructor <;> rintro ⟨⟨h1, h2⟩, h3, h4⟩ <;> refine ⟨⟨?_, ?_⟩, ?_, ?_⟩ <;> linarith

end UnitSquarePacking
