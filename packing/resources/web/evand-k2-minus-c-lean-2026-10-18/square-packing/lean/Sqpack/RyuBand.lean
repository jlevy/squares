import Sqpack.FangGlue
import Sqpack.ExactPack

/-!
# Ryu's L-shaped packings: the geometry

S. Ryu, *k² − c upper bounds* (squarepacker/k2-minus-c-upper v1.1; jlevy/squares#471, #486), Theorem 1.3:
an axis grid of `m²` squares, plus two bands of tilted rows (`b` squares per row, angle `θ` slightly above
`2 arctan(1/b)`, where a row is exactly `b` wide), one band along the right side and one, transposed, along the top.

This file is the geometry, for any angle with `cos θ = γ > 0`, `sin θ = σ ≥ 0`:

* `sep_U`, `sep_V`: two squares at the same angle whose centres differ by `≥ 1` in a rotated coordinate have
  disjoint interiors.
* `unitSq_subset_box`: a square lies in a box if its four corners do.
* `PacksIn.transpose`: `(x, y) ↦ (y, x)` maps a packing of `[0, w] × [0, h]` to one of `[0, h] × [0, w]`.
* `band`: `R` rows of `b` squares pack in `[0, bγ + σ] × [0, (R − 1)/γ + bσ + γ]` (Ryu's Lemmas 3.1–3.4).
* `lshape`: grid + right band + transposed top band (Ryu's Lemma 4.1).
-/

namespace UnitSquarePacking.Ryu

open Set UnitSquarePacking.Conjectures UnitSquarePacking.FangGlue

/-- The rotated coordinates of `p` for the angle with `(cos, sin) = (γ, σ)`. -/
def U (γ σ : ℝ) (p : ℝ × ℝ) : ℝ := p.1 * γ + p.2 * σ
def V (γ σ : ℝ) (p : ℝ × ℝ) : ℝ := -p.1 * σ + p.2 * γ

lemma U_sub (γ σ : ℝ) (p c : ℝ × ℝ) : U γ σ p - U γ σ c = (p.1 - c.1) * γ + (p.2 - c.2) * σ := by
  simp only [U]; ring

lemma V_sub (γ σ : ℝ) (p c : ℝ × ℝ) : V γ σ p - V γ σ c = -(p.1 - c.1) * σ + (p.2 - c.2) * γ := by
  simp only [V]; ring

lemma mem_interior_iff {c p : ℝ × ℝ} {θ : ℝ} :
    p ∈ interior (unitSq c θ) ↔ |U (Real.cos θ) (Real.sin θ) p - U (Real.cos θ) (Real.sin θ) c| < 1 / 2 ∧
      |V (Real.cos θ) (Real.sin θ) p - V (Real.cos θ) (Real.sin θ) c| < 1 / 2 := by
  rw [interior_unitSq, U_sub, V_sub]; rfl

/-- Same angle, centres `≥ 1` apart in `U`: disjoint interiors. -/
lemma sep_U {c c' : ℝ × ℝ} {θ : ℝ}
    (h : 1 ≤ |U (Real.cos θ) (Real.sin θ) c - U (Real.cos θ) (Real.sin θ) c'|) :
    Disjoint (interior (unitSq c θ)) (interior (unitSq c' θ)) := by
  rw [Set.disjoint_left]
  intro p hp hp'
  rw [mem_interior_iff] at hp hp'
  obtain ⟨h1, h2⟩ := abs_lt.1 hp.1
  obtain ⟨h3, h4⟩ := abs_lt.1 hp'.1
  rcases le_abs'.1 h with h5 | h5 <;> linarith

/-- Same angle, centres `≥ 1` apart in `V`: disjoint interiors. -/
lemma sep_V {c c' : ℝ × ℝ} {θ : ℝ}
    (h : 1 ≤ |V (Real.cos θ) (Real.sin θ) c - V (Real.cos θ) (Real.sin θ) c'|) :
    Disjoint (interior (unitSq c θ)) (interior (unitSq c' θ)) := by
  rw [Set.disjoint_left]
  intro p hp hp'
  rw [mem_interior_iff] at hp hp'
  obtain ⟨h1, h2⟩ := abs_lt.1 hp.2
  obtain ⟨h3, h4⟩ := abs_lt.1 hp'.2
  rcases le_abs'.1 h with h5 | h5 <;> linarith

/-- A square lies in `[x₀, x₁] × [y₀, y₁]` if its four corners do. -/
lemma unitSq_subset_box {c : ℝ × ℝ} {θ x₀ x₁ y₀ y₁ : ℝ}
    (h : ∀ a b, Half a → Half b →
      x₀ ≤ c.1 + Real.cos θ * a - Real.sin θ * b ∧ c.1 + Real.cos θ * a - Real.sin θ * b ≤ x₁ ∧
      y₀ ≤ c.2 + Real.sin θ * a + Real.cos θ * b ∧ c.2 + Real.sin θ * a + Real.cos θ * b ≤ y₁) :
    unitSq c θ ⊆ box x₀ x₁ y₀ y₁ := by
  rintro p ⟨q, ⟨⟨h1, h2⟩, h3, h4⟩, rfl⟩
  simp only [rot, box, mem_prod, mem_Icc, Prod.fst_add, Prod.snd_add]
  refine ⟨⟨?_, ?_⟩, ?_, ?_⟩
  · have := affine_nonneg (A := c.1 - x₀) (B := Real.cos θ) (C := -Real.sin θ) ⟨h1, h2⟩ ⟨h3, h4⟩
      (fun a b ha hb => by have := (h a b ha hb).1; linarith)
    linarith
  · have := affine_nonneg (A := x₁ - c.1) (B := -Real.cos θ) (C := Real.sin θ) ⟨h1, h2⟩ ⟨h3, h4⟩
      (fun a b ha hb => by have := (h a b ha hb).2.1; linarith)
    linarith
  · have := affine_nonneg (A := c.2 - y₀) (B := Real.sin θ) (C := Real.cos θ) ⟨h1, h2⟩ ⟨h3, h4⟩
      (fun a b ha hb => by have := (h a b ha hb).2.2.1; linarith)
    linarith
  · have := affine_nonneg (A := y₁ - c.2) (B := -Real.sin θ) (C := -Real.cos θ) ⟨h1, h2⟩ ⟨h3, h4⟩
      (fun a b ha hb => by have := (h a b ha hb).2.2.2; linarith)
    linarith

/-! ## Transposition -/

/-- `(x, y) ↦ (y, x)` maps `unitSq c θ` onto `unitSq (c.2, c.1) (π/2 − θ)`. -/
lemma mem_unitSq_swap {c p : ℝ × ℝ} {θ : ℝ} :
    (p.2, p.1) ∈ unitSq c θ ↔ p ∈ unitSq (c.2, c.1) (Real.pi / 2 - θ) := by
  rw [unitSq_eq_setOf, unitSq_eq_setOf]
  simp only [mem_ofPred_eq, Real.cos_pi_div_two_sub, Real.sin_pi_div_two_sub]
  constructor <;> rintro ⟨h1, h2⟩
  · refine ⟨by convert h1 using 2; ring, ?_⟩
    rw [← abs_neg]; convert h2 using 2; ring
  · refine ⟨by convert h1 using 2; ring, ?_⟩
    rw [← abs_neg]; convert h2 using 2; ring

lemma mem_interior_unitSq_swap {c p : ℝ × ℝ} {θ : ℝ} :
    (p.2, p.1) ∈ interior (unitSq c θ) ↔ p ∈ interior (unitSq (c.2, c.1) (Real.pi / 2 - θ)) := by
  rw [interior_unitSq, interior_unitSq]
  simp only [mem_ofPred_eq, Real.cos_pi_div_two_sub, Real.sin_pi_div_two_sub]
  constructor <;> rintro ⟨h1, h2⟩
  · refine ⟨by convert h1 using 2; ring, ?_⟩
    rw [← abs_neg]; convert h2 using 2; ring
  · refine ⟨by convert h1 using 2; ring, ?_⟩
    rw [← abs_neg]; convert h2 using 2; ring

/-- Transposing a packing of `[0, w] × [0, h]`. -/
lemma _root_.UnitSquarePacking.Conjectures.PacksIn.transpose {n : ℕ} {w h : ℝ} (hp : PacksIn n (rect w h)) :
    PacksIn n (rect h w) := by
  obtain ⟨c, θ, hin, hd⟩ := hp
  refine ⟨fun i => ((c i).2, (c i).1), fun i => Real.pi / 2 - θ i, fun i p hp' => ?_, fun i j hij => ?_⟩
  · have := hin i (mem_unitSq_swap.2 hp')
    simp only [rect, mem_prod, mem_Icc] at this ⊢
    exact ⟨this.2, this.1⟩
  · change Disjoint _ _
    rw [Set.disjoint_left]
    intro p hpi hpj
    exact Set.disjoint_left.1 (hd hij) (mem_interior_unitSq_swap.2 hpi) (mem_interior_unitSq_swap.2 hpj)

/-! ## One band -/

/-- The centre of square `i` of row `j` (Ryu's `Q_i(P_j)` with `P_0 = (σ, 0)`), for `(cos, sin) = (γ, σ)`. -/
noncomputable def ctr (γ σ : ℝ) (i j : ℕ) : ℝ × ℝ :=
  ((σ, 0) : ℝ × ℝ) + ((i + 1/2 + j * (σ / γ)) * γ - (j + 1/2) * σ, (i + 1/2 + j * (σ / γ)) * σ + (j + 1/2) * γ)

lemma U_ctr {γ σ : ℝ} (hu : γ ^ 2 + σ ^ 2 = 1) (i j : ℕ) :
    U γ σ (ctr γ σ i j) = σ * γ + (i + 1/2 + j * (σ / γ)) := by
  simp only [U, ctr, Prod.fst_add, Prod.snd_add]
  linear_combination (↑i + 1 / 2 + ↑j * (σ / γ)) * hu

lemma V_ctr {γ σ : ℝ} (hu : γ ^ 2 + σ ^ 2 = 1) (i j : ℕ) :
    V γ σ (ctr γ σ i j) = -σ * σ + (j + 1/2) := by
  simp only [V, ctr, Prod.fst_add, Prod.snd_add]
  linear_combination (↑j + 1 / 2) * hu

/-- The centres of a band of `R` rows of `b` squares, indexed by `Fin (R * b)`. -/
noncomputable def bandCen (γ σ : ℝ) (R b : ℕ) (k : Fin (R * b)) : ℝ × ℝ :=
  ctr γ σ (((finProdFinEquiv : Fin R × Fin b ≃ Fin (R * b)).symm k).2)
    (((finProdFinEquiv : Fin R × Fin b ≃ Fin (R * b)).symm k).1)

/-- **One band** (Ryu, Lemmas 3.1–3.4), explicitly: containment and pairwise disjointness. -/
theorem band_explicit {θ : ℝ} (hγ : 0 < Real.cos θ) (hσ : 0 ≤ Real.sin θ) (R b : ℕ) :
    (∀ k, unitSq (bandCen (Real.cos θ) (Real.sin θ) R b k) θ ⊆
      rect (b * Real.cos θ + Real.sin θ) ((R - 1) / Real.cos θ + b * Real.sin θ + Real.cos θ)) ∧
    Pairwise fun k k' => Disjoint (interior (unitSq (bandCen (Real.cos θ) (Real.sin θ) R b k) θ))
      (interior (unitSq (bandCen (Real.cos θ) (Real.sin θ) R b k') θ)) := by
  set γ := Real.cos θ with hγd
  set σ := Real.sin θ with hσd
  have hu : γ ^ 2 + σ ^ 2 = 1 := by rw [hγd, hσd, add_comm]; exact Real.sin_sq_add_cos_sq θ
  set e := (finProdFinEquiv : Fin R × Fin b ≃ Fin (R * b)) with he
  set cen : Fin (R * b) → ℝ × ℝ := bandCen γ σ R b with hcen
  refine ⟨fun k => ?_, fun k k' hkk => ?_⟩
  · -- containment, corner by corner
    have hj := (e.symm k).1.isLt
    have hi := (e.symm k).2.isLt
    set j : ℕ := ((e.symm k).1 : ℕ)
    set i : ℕ := ((e.symm k).2 : ℕ)
    have hj' : (j : ℝ) ≤ R - 1 := by
      have : j + 1 ≤ R := hj
      have : (j : ℝ) + 1 ≤ R := by exact_mod_cast this
      linarith
    have hi' : (i : ℝ) + 1 ≤ b := by exact_mod_cast hi
    have hi0 : (0 : ℝ) ≤ i := by positivity
    have hj0 : (0 : ℝ) ≤ j := by positivity
    show unitSq (bandCen γ σ R b k) θ ⊆ _
    have hsub := unitSq_subset_box (c := ctr γ σ i j) (θ := θ) (x₀ := 0) (x₁ := b * γ + σ) (y₀ := 0)
      (y₁ := (R - 1) / γ + b * σ + γ) ?_
    · intro p hp
      have := hsub hp
      simp only [box, rect, mem_prod, mem_Icc] at this ⊢
      exact this
    intro a c ha hc
    have ea : 0 ≤ 1/2 + a ∧ 1/2 + a ≤ 1 := by rcases ha with rfl | rfl <;> norm_num
    have ec : 0 ≤ 1/2 + c ∧ 1/2 + c ≤ 1 := by rcases hc with rfl | rfl <;> norm_num
    have ex : (ctr γ σ i j).1 + γ * a - σ * c = σ * (1 - (1/2 + c)) + γ * (i + (1/2 + a)) := by
      simp only [ctr, Prod.fst_add]; field_simp; ring
    have ey : (ctr γ σ i j).2 + σ * a + γ * c = σ * (i + (1/2 + a)) + j / γ + γ * (1/2 + c) := by
      simp only [ctr, Prod.snd_add]; field_simp; linear_combination (2 * (j : ℝ)) * hu
    set ε₁ := 1/2 + a
    set ε₂ := 1/2 + c
    have hb1 : (i : ℝ) + ε₁ ≤ b := by linarith [ea.2]
    have hb0 : 0 ≤ (i : ℝ) + ε₁ := by linarith [ea.1]
    have g1 := mul_le_mul_of_nonneg_left hb1 hγ.le
    have g2 := mul_le_mul_of_nonneg_left hb1 hσ
    have g3 := mul_nonneg hγ.le hb0
    have g4 := mul_nonneg hσ hb0
    have g5 := div_le_div_of_nonneg_right hj' hγ.le
    have g6 := div_nonneg hj0 hγ.le
    have g7 := mul_nonneg hσ (by linarith [ec.2] : (0 : ℝ) ≤ 1 - ε₂)
    have g8 := mul_le_mul_of_nonneg_left (by linarith [ec.1] : 1 - ε₂ ≤ (1 : ℝ)) hσ
    have g9 := mul_nonneg hγ.le ec.1
    have g10 := mul_le_mul_of_nonneg_left ec.2 hγ.le
    rw [ex, ey]
    refine ⟨by linarith, by linarith, by linarith, by linarith⟩
  · -- disjointness: different rows by `V`, same row by `U`
    have hne : e.symm k ≠ e.symm k' := fun h => hkk (e.symm.injective h)
    simp only [cen, bandCen]
    by_cases hrow : (e.symm k).1 = (e.symm k').1
    · have hcol : ((e.symm k).2 : ℕ) ≠ (e.symm k').2 := by
        intro h; exact hne (Prod.ext hrow (Fin.ext h))
      apply sep_U
      rw [← hγd, ← hσd, U_ctr hu, U_ctr hu, hrow]
      have : (1 : ℝ) ≤ |((e.symm k).2 : ℝ) - (e.symm k').2| := by
        rcases Nat.lt_or_gt_of_ne hcol with h | h
        · have : ((e.symm k).2 : ℝ) + 1 ≤ (e.symm k').2 := by exact_mod_cast h
          rw [abs_sub_comm, abs_of_nonneg (by linarith)]; linarith
        · have : ((e.symm k').2 : ℝ) + 1 ≤ (e.symm k).2 := by exact_mod_cast h
          rw [abs_of_nonneg (by linarith)]; linarith
      convert this using 2; ring
    · have hrow' : ((e.symm k).1 : ℕ) ≠ (e.symm k').1 := fun h => hrow (Fin.ext h)
      apply sep_V
      rw [← hγd, ← hσd, V_ctr hu, V_ctr hu]
      have : (1 : ℝ) ≤ |((e.symm k).1 : ℝ) - (e.symm k').1| := by
        rcases Nat.lt_or_gt_of_ne hrow' with h | h
        · have : ((e.symm k).1 : ℝ) + 1 ≤ (e.symm k').1 := by exact_mod_cast h
          rw [abs_sub_comm, abs_of_nonneg (by linarith)]; linarith
        · have : ((e.symm k').1 : ℝ) + 1 ≤ (e.symm k).1 := by exact_mod_cast h
          rw [abs_of_nonneg (by linarith)]; linarith
      convert this using 2; ring


theorem band {θ : ℝ} (hγ : 0 < Real.cos θ) (hσ : 0 ≤ Real.sin θ) (R b : ℕ) :
    PacksIn (R * b) (rect (b * Real.cos θ + Real.sin θ) ((R - 1) / Real.cos θ + b * Real.sin θ + Real.cos θ)) :=
  ⟨bandCen _ _ R b, fun _ => θ, (band_explicit hγ hσ R b).1, (band_explicit hγ hσ R b).2⟩

lemma V_bandCen {γ σ : ℝ} (hu : γ ^ 2 + σ ^ 2 = 1) {R b : ℕ} (k : Fin (R * b)) :
    -σ ^ 2 + 1 / 2 ≤ V γ σ (bandCen γ σ R b k) ∧ V γ σ (bandCen γ σ R b k) ≤ R - σ ^ 2 - 1 / 2 := by
  simp only [bandCen]
  rw [V_ctr hu]
  have h := ((finProdFinEquiv : Fin R × Fin b ≃ Fin (R * b)).symm k).1.isLt
  have h' : (((finProdFinEquiv : Fin R × Fin b ≃ Fin (R * b)).symm k).1 : ℝ) + 1 ≤ R := by exact_mod_cast h
  constructor
  · have : (0 : ℝ) ≤ (((finProdFinEquiv : Fin R × Fin b ≃ Fin (R * b)).symm k).1 : ℝ) := by positivity
    nlinarith
  · nlinarith

/-! ## Filled band ends -/

/-- An affine function `≤ c` at the four corners is `≤ c` on the square. -/
lemma unitSq_subset_half {c₀ : ℝ × ℝ} {θ α β c : ℝ}
    (h : ∀ a b, Half a → Half b →
      α * (c₀.1 + Real.cos θ * a - Real.sin θ * b) + β * (c₀.2 + Real.sin θ * a + Real.cos θ * b) ≤ c) :
    unitSq c₀ θ ⊆ {p | α * p.1 + β * p.2 ≤ c} := by
  rintro p ⟨q, ⟨⟨h1, h2⟩, h3, h4⟩, rfl⟩
  simp only [rot, Set.mem_ofPred_eq, Prod.fst_add, Prod.snd_add]
  have := affine_nonneg (A := c - α * c₀.1 - β * c₀.2) (B := -(α * Real.cos θ + β * Real.sin θ))
    (C := α * Real.sin θ - β * Real.cos θ) ⟨h1, h2⟩ ⟨h3, h4⟩
    (fun a b ha hb => by have := h a b ha hb; nlinarith)
  nlinarith

/-- A square inside `{V ≤ c}` and a square at angle `θ` with centre at `V ≥ c + 1/2` have disjoint interiors. -/
lemma disjoint_half {c₀ c₁ : ℝ × ℝ} {θ₀ θ c : ℝ}
    (h₀ : unitSq c₀ θ₀ ⊆ {p | -Real.sin θ * p.1 + Real.cos θ * p.2 ≤ c})
    (h₁ : c + 1 / 2 ≤ V (Real.cos θ) (Real.sin θ) c₁) :
    Disjoint (interior (unitSq c₀ θ₀)) (interior (unitSq c₁ θ)) := by
  rw [Set.disjoint_left]
  intro p hp hp'
  have hv := h₀ (interior_subset hp)
  rw [mem_interior_iff] at hp'
  obtain ⟨h2, _⟩ := abs_lt.1 hp'.2
  have hvp : V (Real.cos θ) (Real.sin θ) p ≤ c := by
    simp only [Set.mem_ofPred_eq] at hv; simp only [V]; linarith
  linarith

/-- The mirror image: `{V ≥ c}` against centre `V ≤ c − 1/2`. -/
lemma disjoint_half' {c₀ c₁ : ℝ × ℝ} {θ₀ θ c : ℝ}
    (h₀ : unitSq c₀ θ₀ ⊆ {p | Real.sin θ * p.1 + -Real.cos θ * p.2 ≤ -c})
    (h₁ : V (Real.cos θ) (Real.sin θ) c₁ ≤ c - 1 / 2) :
    Disjoint (interior (unitSq c₀ θ₀)) (interior (unitSq c₁ θ)) := by
  rw [Set.disjoint_left]
  intro p hp hp'
  have hv := h₀ (interior_subset hp)
  rw [mem_interior_iff] at hp'
  obtain ⟨_, h2⟩ := abs_lt.1 hp'.2
  have hvp : c ≤ V (Real.cos θ) (Real.sin θ) p := by
    simp only [Set.mem_ofPred_eq] at hv; simp only [V]; linarith
  linarith

/-- Two explicit families in a common region, pairwise disjoint within and across, append. -/
lemma append_explicit {m n : ℕ} {S : Set (ℝ × ℝ)} {c₁ : Fin m → ℝ × ℝ} {θ₁ : Fin m → ℝ}
    {c₂ : Fin n → ℝ × ℝ} {θ₂ : Fin n → ℝ}
    (h₁ : ∀ i, unitSq (c₁ i) (θ₁ i) ⊆ S) (h₂ : ∀ i, unitSq (c₂ i) (θ₂ i) ⊆ S)
    (d₁ : Pairwise fun i j => Disjoint (interior (unitSq (c₁ i) (θ₁ i))) (interior (unitSq (c₁ j) (θ₁ j))))
    (d₂ : Pairwise fun i j => Disjoint (interior (unitSq (c₂ i) (θ₂ i))) (interior (unitSq (c₂ j) (θ₂ j))))
    (d : ∀ i j, Disjoint (interior (unitSq (c₁ i) (θ₁ i))) (interior (unitSq (c₂ j) (θ₂ j)))) :
    (∀ i, unitSq (Fin.append c₁ c₂ i) (Fin.append θ₁ θ₂ i) ⊆ S) ∧
    Pairwise fun i j => Disjoint (interior (unitSq (Fin.append c₁ c₂ i) (Fin.append θ₁ θ₂ i)))
      (interior (unitSq (Fin.append c₁ c₂ j) (Fin.append θ₁ θ₂ j))) := by
  refine ⟨fun i => ?_, fun i j hij => ?_⟩
  · induction i using Fin.addCases with
    | left i => simp only [Fin.append_left]; exact h₁ i
    | right i => simp only [Fin.append_right]; exact h₂ i
  · induction i using Fin.addCases <;> induction j using Fin.addCases <;>
      simp only [Fin.append_left, Fin.append_right]
    · exact d₁ fun h => hij (by rw [h])
    · exact d _ _
    · exact (d _ _).symm
    · exact d₂ fun h => hij (by rw [h])

lemma half_cases' {a : ℝ} (h : Half a) : a = 1 / 2 ∨ a = -1 / 2 := h

/-- **A band with filled ends** (the "R1′" variant of Ryu's band): besides the `R` rows, `nf` axis squares under the
first row (`[w − 1 − q, w − q] × [0, 1]`) and `nf` over the last (`[q, q + 1] × [L − 1, L]`), where
`nf ≤ bγ − cot θ`. -/
theorem band_fill {θ : ℝ} (hγ : 0 < Real.cos θ) (hσ : 0 < Real.sin θ) (R b nf : ℕ) {L : ℝ}
    (hL : (R - 1) / Real.cos θ + b * Real.sin θ + Real.cos θ ≤ L) (hL2 : 2 ≤ L)
    (hnf : (nf : ℝ) ≤ b * Real.cos θ - Real.cos θ / Real.sin θ) :
    PacksIn (R * b + nf + nf) (rect (b * Real.cos θ + Real.sin θ) L) := by
  set γ := Real.cos θ with hγd
  set σ := Real.sin θ with hσd
  have hu : γ ^ 2 + σ ^ 2 = 1 := by rw [hγd, hσd, add_comm]; exact Real.sin_sq_add_cos_sq θ
  set w := b * γ + σ with hw
  have hcot : 0 ≤ γ / σ := div_nonneg hγ.le hσ.le
  have hnfw : (nf : ℝ) ≤ w := by
    have : (b : ℝ) * γ ≤ w := by rw [hw]; linarith
    linarith
  have hkey : σ * (w - nf) ≥ σ ^ 2 + γ := by
    have : w - nf ≥ σ + γ / σ := by rw [hw]; linarith
    have := mul_le_mul_of_nonneg_left this hσ.le
    rw [mul_add, mul_div_cancel₀ _ hσ.ne'] at this
    nlinarith
  -- the three families
  let cB : Fin (R * b) → ℝ × ℝ := bandCen γ σ R b
  let tB : Fin (R * b) → ℝ := fun _ => θ
  let cD : Fin nf → ℝ × ℝ := fun q => (w - 1 / 2 - q, 1 / 2)
  let cT : Fin nf → ℝ × ℝ := fun q => ((q : ℝ) + 1 / 2, L - 1 / 2)
  let t0 : Fin nf → ℝ := fun _ => 0
  have hB := band_explicit hγ hσ.le R b
  have sB : ∀ i, unitSq (cB i) (tB i) ⊆ rect w L := fun i =>
    (hB.1 i).trans (rect_mono le_rfl hL)
  have axis_sub : ∀ (c : ℝ × ℝ), 0 ≤ c.1 - 1 / 2 → c.1 + 1 / 2 ≤ w → 0 ≤ c.2 - 1 / 2 → c.2 + 1 / 2 ≤ L →
      unitSq c 0 ⊆ rect w L := by
    intro c h1 h2 h3 h4 p hp
    have := unitSq_subset_box (c := c) (θ := 0) (x₀ := 0) (x₁ := w) (y₀ := 0) (y₁ := L) (by
      intro a b' ha hb
      simp only [Real.cos_zero, Real.sin_zero, one_mul, zero_mul, sub_zero, add_zero]
      rcases ha with rfl | rfl <;> rcases hb with rfl | rfl <;> refine ⟨?_, ?_, ?_, ?_⟩ <;> linarith) hp
    simpa [box, rect] using this
  have sD : ∀ q, unitSq (cD q) (t0 q) ⊆ rect w L := fun q => by
    have hq : (q : ℝ) + 1 ≤ nf := by exact_mod_cast q.isLt
    apply axis_sub <;> simp only [cD] <;> linarith
  have sT : ∀ q, unitSq (cT q) (t0 q) ⊆ rect w L := fun q => by
    have hq : (q : ℝ) + 1 ≤ nf := by exact_mod_cast q.isLt
    have : (0 : ℝ) ≤ q := by positivity
    apply axis_sub <;> simp only [cT] <;> linarith
  have axis_disj : ∀ (c c' : ℝ × ℝ), 1 ≤ |c.1 - c'.1| ∨ 1 ≤ |c.2 - c'.2| →
      Disjoint (interior (unitSq c 0)) (interior (unitSq c' 0)) := by
    intro c c' h
    rcases h with h | h
    · apply sep_U; simp only [U, Real.cos_zero, Real.sin_zero, mul_one, mul_zero, add_zero]; exact h
    · apply sep_V; simp only [V, Real.cos_zero, Real.sin_zero, mul_one, mul_zero, neg_zero, zero_add]; exact h
  have int_gap : ∀ q q' : Fin nf, q ≠ q' → 1 ≤ |(q : ℝ) - q'| := by
    intro q q' h
    have h' : (q : ℕ) ≠ q' := fun e => h (Fin.ext e)
    rcases Nat.lt_or_gt_of_ne h' with h | h
    · have : (q : ℝ) + 1 ≤ q' := by exact_mod_cast h
      rw [abs_sub_comm, abs_of_nonneg (by linarith)]; linarith
    · have : (q' : ℝ) + 1 ≤ q := by exact_mod_cast h
      rw [abs_of_nonneg (by linarith)]; linarith
  have dD : Pairwise fun i j => Disjoint (interior (unitSq (cD i) (t0 i))) (interior (unitSq (cD j) (t0 j))) := by
    intro q q' h; apply axis_disj; left
    have := int_gap q q' h
    simp only [cD]; rw [abs_sub_comm]; convert this using 2; ring
  have dT : Pairwise fun i j => Disjoint (interior (unitSq (cT i) (t0 i))) (interior (unitSq (cT j) (t0 j))) := by
    intro q q' h; apply axis_disj; left
    have := int_gap q q' h
    simp only [cT]; convert this using 2; ring
  -- band against the bottom fill: the fill lies in `{V ≤ −σ²}`
  have hDhalf : ∀ q : Fin nf, unitSq (cD q) 0 ⊆ {p | -σ * p.1 + γ * p.2 ≤ -σ ^ 2} := fun q => by
    have hq : (q : ℝ) + 1 ≤ nf := by exact_mod_cast q.isLt
    apply unitSq_subset_half
    intro a b' ha hb
    simp only [cD, Real.cos_zero, Real.sin_zero, one_mul, zero_mul, sub_zero, add_zero]
    rcases ha with rfl | rfl <;> rcases hb with rfl | rfl <;> nlinarith
  have dBD : ∀ i j, Disjoint (interior (unitSq (cB i) (tB i))) (interior (unitSq (cD j) (t0 j))) := by
    intro i j
    exact (disjoint_half (θ := θ) (c := -σ ^ 2) (hDhalf j) (by have := (V_bandCen hu i).1; linarith)).symm
  -- band against the top fill: the fill lies in `{V ≥ R − σ²}`
  have hrow : γ * (L - 1) ≥ R - 1 + b * σ * γ + γ ^ 2 - γ := by
    have := mul_le_mul_of_nonneg_left hL hγ.le
    rw [mul_add, mul_add, mul_div_cancel₀ _ hγ.ne'] at this
    nlinarith
  have hTop : σ * (b * γ - nf) ≥ γ := by
    have := mul_le_mul_of_nonneg_left hnf hσ.le
    rw [mul_sub, mul_div_cancel₀ _ hσ.ne'] at this
    nlinarith
  have hThalf : ∀ q : Fin nf, unitSq (cT q) 0 ⊆ {p | σ * p.1 + -γ * p.2 ≤ -(R - σ ^ 2)} := fun q => by
    have hq : (q : ℝ) + 1 ≤ nf := by exact_mod_cast q.isLt
    have hq0 : (0 : ℝ) ≤ q := by positivity
    apply unitSq_subset_half
    intro a b' ha hb
    simp only [cT, Real.cos_zero, Real.sin_zero, one_mul, zero_mul, sub_zero, add_zero]
    rcases ha with rfl | rfl <;> rcases hb with rfl | rfl <;> nlinarith
  have dBT : ∀ i j, Disjoint (interior (unitSq (cB i) (tB i))) (interior (unitSq (cT j) (t0 j))) := by
    intro i j
    exact (disjoint_half' (θ := θ) (c := R - σ ^ 2) (hThalf j) (by have := (V_bandCen hu i).2; linarith)).symm
  have dDT : ∀ i j, Disjoint (interior (unitSq (cD i) (t0 i))) (interior (unitSq (cT j) (t0 j))) := by
    intro i j; apply axis_disj; right
    simp only [cD, cT]
    rw [abs_sub_comm, abs_of_nonneg (by linarith)]; linarith
  -- assemble: band ++ bottom, then ++ top
  have A1 := append_explicit sB sD hB.2 dD dBD
  have A2 := append_explicit A1.1 sT A1.2 dT (fun i j => by
    induction i using Fin.addCases with
    | left i => simp only [Fin.append_left]; exact dBT i j
    | right i => simp only [Fin.append_right]; exact dDT i j)
  exact ⟨_, _, A2.1, A2.2⟩

/-! ## The L-shape -/

/-- **The L-shape** (Ryu, Lemma 4.1): an `m × m` grid, a band of width `w` and length `m + w` on the right, and a
band of width `w` and length `m`, transposed, on top. -/
theorem lshape {m X₁ X₂ : ℕ} {w : ℝ} (hw : 0 ≤ w) (h₁ : PacksIn X₁ (rect w (m + w)))
    (h₂ : PacksIn X₂ (rect w m)) : Packs (m * m + X₁ + X₂) (m + w) := by
  have hm : (0 : ℝ) ≤ m := by positivity
  have PG := (packsIn_block m m).toBox 0 0
  have PA := h₁.toBox m 0
  have PT := h₂.transpose.toBox 0 m
  have GA := PG.union PA (disjoint_box_x (by linarith))
  have dT : Disjoint (interior (box 0 (0 + m) 0 (0 + m) ∪ box m (m + w) 0 (0 + (m + w))))
      (interior (box 0 (0 + m) m (m + w))) := by
    refine (disjoint_interior_union isOpen_interior (isClosed_box _ _ _ _) ?_ ?_).symm
    · exact (disjoint_box_y (by linarith)).symm
    · exact disjoint_box_x (by linarith)
  have all := GA.union PT dT
  refine packs_iff_packsIn.2 (all.mono ?_)
  intro p hp
  simp only [box, rect, Set.mem_union, Set.mem_prod, Set.mem_Icc] at hp ⊢
  rcases hp with ((⟨⟨h1, h2⟩, h3, h4⟩ | ⟨⟨h1, h2⟩, h3, h4⟩) | ⟨⟨h1, h2⟩, h3, h4⟩) <;>
    refine ⟨⟨?_, ?_⟩, ?_, ?_⟩ <;> linarith

/-- **Ryu's Theorem 1.3, geometric part.**  With `γ = cos θ > 0`, `σ = sin θ ≥ 0` and the band width
`w = bγ + σ`, if `R₁` rows fit along `m + w` and `R₂` along `m`, then `m² + b(R₁ + R₂)` squares pack in side `m + w`. -/
theorem lpacking {θ : ℝ} (hγ : 0 < Real.cos θ) (hσ : 0 ≤ Real.sin θ) (m b R₁ R₂ : ℕ)
    (hL1 : (R₁ - 1) / Real.cos θ + b * Real.sin θ + Real.cos θ ≤ m + (b * Real.cos θ + Real.sin θ))
    (hL2 : (R₂ - 1) / Real.cos θ + b * Real.sin θ + Real.cos θ ≤ m) :
    Packs (m * m + R₁ * b + R₂ * b) (m + (b * Real.cos θ + Real.sin θ)) := by
  have hw : 0 ≤ b * Real.cos θ + Real.sin θ := by positivity
  exact lshape hw ((band hγ hσ R₁ b).mono (rect_mono le_rfl hL1)) ((band hγ hσ R₂ b).mono (rect_mono le_rfl hL2))

/-- **The L-shape with filled band ends.** -/
theorem lpacking_fill {θ : ℝ} (hγ : 0 < Real.cos θ) (hσ : 0 < Real.sin θ) (m b R₁ R₂ nf : ℕ) (hm : 2 ≤ m)
    (hL1 : (R₁ - 1) / Real.cos θ + b * Real.sin θ + Real.cos θ ≤ m + (b * Real.cos θ + Real.sin θ))
    (hL2 : (R₂ - 1) / Real.cos θ + b * Real.sin θ + Real.cos θ ≤ m)
    (hnf : (nf : ℝ) ≤ b * Real.cos θ - Real.cos θ / Real.sin θ) :
    Packs (m * m + (R₁ * b + nf + nf) + (R₂ * b + nf + nf)) (m + (b * Real.cos θ + Real.sin θ)) := by
  have hw : 0 ≤ b * Real.cos θ + Real.sin θ := by positivity
  have hm' : (2 : ℝ) ≤ m := by exact_mod_cast hm
  exact lshape hw (band_fill hγ hσ R₁ b nf hL1 (by linarith) hnf) (band_fill hγ hσ R₂ b nf hL2 hm' hnf)

end UnitSquarePacking.Ryu
