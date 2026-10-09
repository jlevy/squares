import Sqpack.Spec

/-!
# Packings from exact data: corners in the box, separating side lines

A packing given by centres `(x i, y i)` and rotations `(c i, s i)` with `c i ^ 2 + s i ^ 2 = 1` (algebraic data:
no angles, no trigonometry) is valid if

* `InBox`: the four corners of each square lie in `[0, S]²`;
* `SepPair`: for each pair, one side line of one of the two squares has the four corners of the other square on its
  closed outer side.

`packs_of_cert` turns these into `Packs n S`.  For squares the separating-axis theorem only needs face normals, and
the projection of a square onto its own face normal ends exactly at that face, so every valid packing has such a
certificate: the touching pairs with equalities, the others strictly.

The corner of square `(x, y, c, s)` with local coordinates `(a, b)`, `a, b = ±1/2`, is
`(x + c a - s b, y + s a + c b)`, matching `rot`.  The outward normals of its four sides are
`(c, s), (-s, c), (-c, -s), (s, -c)` (`nrm`).
-/

namespace UnitSquarePacking

open Set

/-- Every `(c, s)` on the unit circle is `(cos θ, sin θ)`. -/
lemma exists_angle {c s : ℝ} (h : c ^ 2 + s ^ 2 = 1) : ∃ θ, Real.cos θ = c ∧ Real.sin θ = s := by
  set z : ℂ := ⟨c, s⟩
  have hn : ‖z‖ = 1 := by rw [Complex.norm_eq_sqrt_sq_add_sq]; simp [z, h]
  have hz : z ≠ 0 := by intro h0; rw [h0, norm_zero] at hn; exact zero_ne_one hn
  exact ⟨Complex.arg z, by rw [Complex.cos_arg hz, hn]; simp [z], by rw [Complex.sin_arg, hn]; simp [z]⟩

/-- `a = ±1/2`. -/
def Half (a : ℝ) : Prop := a = 1 / 2 ∨ a = -1 / 2

/-- An affine function of `(a, b)` that is `≥ 0` at the four corners `a, b = ±1/2` is `≥ 0` on the square
`|a|, |b| ≤ 1/2`: it is the bilinear interpolation of its corner values. -/
lemma affine_nonneg {A B C q₁ q₂ : ℝ} (h₁ : -1/2 ≤ q₁ ∧ q₁ ≤ 1/2) (h₂ : -1/2 ≤ q₂ ∧ q₂ ≤ 1/2)
    (h : ∀ a b, Half a → Half b → 0 ≤ A + B * a + C * b) : 0 ≤ A + B * q₁ + C * q₂ := by
  have hpp := h (1/2) (1/2) (Or.inl rfl) (Or.inl rfl)
  have hpm := h (1/2) (-1/2) (Or.inl rfl) (Or.inr rfl)
  have hmp := h (-1/2) (1/2) (Or.inr rfl) (Or.inl rfl)
  have hmm := h (-1/2) (-1/2) (Or.inr rfl) (Or.inr rfl)
  have e : A + B * q₁ + C * q₂ =
      (1/2 + q₁) * (1/2 + q₂) * (A + B * (1/2) + C * (1/2)) +
      (1/2 + q₁) * (1/2 - q₂) * (A + B * (1/2) + C * (-1/2)) +
      (1/2 - q₁) * (1/2 + q₂) * (A + B * (-1/2) + C * (1/2)) +
      (1/2 - q₁) * (1/2 - q₂) * (A + B * (-1/2) + C * (-1/2)) := by ring
  have w₁ : 0 ≤ 1/2 + q₁ := by linarith
  have w₂ : 0 ≤ 1/2 - q₁ := by linarith
  have w₃ : 0 ≤ 1/2 + q₂ := by linarith
  have w₄ : 0 ≤ 1/2 - q₂ := by linarith
  rw [e]
  have := mul_nonneg (mul_nonneg w₁ w₃) hpp
  have := mul_nonneg (mul_nonneg w₁ w₄) hpm
  have := mul_nonneg (mul_nonneg w₂ w₃) hmp
  have := mul_nonneg (mul_nonneg w₂ w₄) hmm
  linarith

/-- The four corners of the square `(x, y, c, s)` lie in `[0, S]²`. -/
def InBox (S x y c s : ℝ) : Prop :=
  ∀ a b, Half a → Half b →
    0 ≤ x + c * a - s * b ∧ x + c * a - s * b ≤ S ∧ 0 ≤ y + s * a + c * b ∧ y + s * a + c * b ≤ S

lemma unitSq_subset_container {S x y c s θ : ℝ} (hc : Real.cos θ = c) (hs : Real.sin θ = s)
    (h : InBox S x y c s) : unitSq (x, y) θ ⊆ container S := by
  rintro p ⟨q, ⟨⟨h1, h2⟩, h3, h4⟩, rfl⟩
  simp only [rot, hc, hs, container, mem_prod, mem_Icc, Prod.fst_add, Prod.snd_add]
  refine ⟨⟨?_, ?_⟩, ?_, ?_⟩
  · have := affine_nonneg (A := x) (B := c) (C := -s) ⟨h1, h2⟩ ⟨h3, h4⟩
      (fun a b ha hb => by have := (h a b ha hb).1; linarith)
    linarith
  · have := affine_nonneg (A := S - x) (B := -c) (C := s) ⟨h1, h2⟩ ⟨h3, h4⟩
      (fun a b ha hb => by have := (h a b ha hb).2.1; linarith)
    linarith
  · have := affine_nonneg (A := y) (B := s) (C := c) ⟨h1, h2⟩ ⟨h3, h4⟩
      (fun a b ha hb => by have := (h a b ha hb).2.2.1; linarith)
    linarith
  · have := affine_nonneg (A := S - y) (B := -s) (C := -c) ⟨h1, h2⟩ ⟨h3, h4⟩
      (fun a b ha hb => by have := (h a b ha hb).2.2.2; linarith)
    linarith

/-- The outward normal of side `k` of a square with rotation `(c, s)`. -/
def nrm (c s : ℝ) : Fin 4 → ℝ × ℝ
  | 0 => (c, s)
  | 1 => (-s, c)
  | 2 => (-c, -s)
  | 3 => (s, -c)

/-- Side `k` of square `i = (xi, yi, ci, si)` has the four corners of square `j` on its closed outer side. -/
def SepSide (xi yi ci si xj yj cj sj : ℝ) (k : Fin 4) : Prop :=
  ∀ a b, Half a → Half b →
    1 / 2 ≤ (nrm ci si k).1 * (xj + cj * a - sj * b - xi) + (nrm ci si k).2 * (yj + sj * a + cj * b - yi)

/-- An interior point of square `i` lies strictly inside each of its side lines. -/
lemma lt_of_mem_interior {xi yi ci si θ : ℝ} (hc : Real.cos θ = ci) (hs : Real.sin θ = si) {p : ℝ × ℝ}
    (hp : p ∈ interior (unitSq (xi, yi) θ)) (k : Fin 4) :
    (nrm ci si k).1 * (p.1 - xi) + (nrm ci si k).2 * (p.2 - yi) < 1 / 2 := by
  rw [interior_unitSq] at hp
  obtain ⟨h1, h2⟩ := hp
  simp only [hc, hs] at h1 h2
  rw [abs_lt] at h1 h2
  fin_cases k <;> simp only [nrm] <;> linarith [h1.1, h1.2, h2.1, h2.2]

lemma pos_comb {A B u v : ℝ} (hA : 0 ≤ A) (hB : 0 ≤ B) (hAB : A ^ 2 + B ^ 2 = 1) (hu : 0 < u) (hv : 0 < v) :
    0 < A * u + B * v := by
  have h1 := mul_nonneg hA hu.le
  have h2 := mul_nonneg hB hv.le
  by_contra hc
  have e1 : A * u = 0 := by linarith
  have e2 : B * v = 0 := by linarith
  have hA0 : A = 0 := (mul_eq_zero.1 e1).resolve_right hu.ne'
  have hB0 : B = 0 := (mul_eq_zero.1 e2).resolve_right hv.ne'
  rw [hA0, hB0] at hAB; norm_num at hAB

/-- An interior point of square `j` lies strictly on the inner side of any line that has its four corners on the
closed outer side. -/
lemma gt_of_mem_interior {xj yj cj sj θ : ℝ} (hc : Real.cos θ = cj) (hs : Real.sin θ = sj)
    (hu : cj ^ 2 + sj ^ 2 = 1) {p : ℝ × ℝ} (hp : p ∈ interior (unitSq (xj, yj) θ)) {nx ny K : ℝ}
    (hn : nx ^ 2 + ny ^ 2 = 1)
    (h : ∀ a b, Half a → Half b → K ≤ nx * (xj + cj * a - sj * b) + ny * (yj + sj * a + cj * b)) :
    K < nx * p.1 + ny * p.2 := by
  rw [interior_unitSq] at hp
  obtain ⟨h1, h2⟩ := hp
  simp only [hc, hs] at h1 h2
  rw [abs_lt] at h1 h2
  set α := (p.1 - xj) * cj + (p.2 - yj) * sj
  set β := -(p.1 - xj) * sj + (p.2 - yj) * cj
  have e1 : p.1 = xj + cj * α - sj * β := by simp only [α, β]; linear_combination -(p.1 - xj) * hu
  have e2 : p.2 = yj + sj * α + cj * β := by simp only [α, β]; linear_combination -(p.2 - yj) * hu
  set A := nx * cj + ny * sj
  set B := -nx * sj + ny * cj
  have hAB : A ^ 2 + B ^ 2 = 1 := by
    simp only [A, B]; linear_combination (nx ^ 2 + ny ^ 2) * hu + hn
  have key : ∀ a b, Half a → Half b → K ≤ nx * xj + ny * yj + A * a + B * b := by
    intro a b ha hb; have := h a b ha hb; simp only [A, B]; linarith
  have hp' : nx * p.1 + ny * p.2 = nx * xj + ny * yj + A * α + B * β := by
    rw [e1, e2]; simp only [A, B]; ring
  rw [hp']
  have hpp := key (1/2) (1/2) (Or.inl rfl) (Or.inl rfl)
  have hpm := key (1/2) (-1/2) (Or.inl rfl) (Or.inr rfl)
  have hmp := key (-1/2) (1/2) (Or.inr rfl) (Or.inl rfl)
  have hmm := key (-1/2) (-1/2) (Or.inr rfl) (Or.inr rfl)
  -- `|A| + |B| ≥ 1` and the corner on the far side gives the strict bound
  have h1l := h1.1; have h1r := h1.2; have h2l := h2.1; have h2r := h2.2
  rcases le_total 0 A with hA | hA <;> rcases le_total 0 B with hB | hB
  · have := pos_comb hA hB hAB (u := α + 1/2) (v := β + 1/2) (by linarith) (by linarith); linarith
  · have := pos_comb hA (by linarith : 0 ≤ -B) (by linear_combination hAB) (u := α + 1/2) (v := 1/2 - β)
      (by linarith) (by linarith); linarith
  · have := pos_comb (by linarith : 0 ≤ -A) hB (by linear_combination hAB) (u := 1/2 - α) (v := β + 1/2)
      (by linarith) (by linarith); linarith
  · have := pos_comb (by linarith : 0 ≤ -A) (by linarith : 0 ≤ -B) (by linear_combination hAB) (u := 1/2 - α)
      (v := 1/2 - β) (by linarith) (by linarith); linarith

lemma nrm_norm (c s : ℝ) (hu : c ^ 2 + s ^ 2 = 1) (k : Fin 4) : (nrm c s k).1 ^ 2 + (nrm c s k).2 ^ 2 = 1 := by
  fin_cases k <;> simp only [nrm] <;> linear_combination hu

/-- A separating side line makes the interiors disjoint. -/
lemma disjoint_of_sepSide {xi yi ci si θi xj yj cj sj θj : ℝ} (hci : Real.cos θi = ci) (hsi : Real.sin θi = si)
    (hcj : Real.cos θj = cj) (hsj : Real.sin θj = sj) (hui : ci ^ 2 + si ^ 2 = 1) (huj : cj ^ 2 + sj ^ 2 = 1)
    {k : Fin 4} (h : SepSide xi yi ci si xj yj cj sj k) :
    Disjoint (interior (unitSq (xi, yi) θi)) (interior (unitSq (xj, yj) θj)) := by
  rw [Set.disjoint_left]
  intro p hpi hpj
  have h1 := lt_of_mem_interior hci hsi hpi k
  have h2 := gt_of_mem_interior hcj hsj huj hpj (nrm_norm ci si hui k)
    (K := 1/2 + (nrm ci si k).1 * xi + (nrm ci si k).2 * yi)
    (fun a b ha hb => by have := h a b ha hb; linarith)
  linarith

/-- Separation certificate for a pair: a side of `i` or a side of `j`. -/
def SepPair (xi yi ci si xj yj cj sj : ℝ) : Prop :=
  (∃ k, SepSide xi yi ci si xj yj cj sj k) ∨ ∃ k, SepSide xj yj cj sj xi yi ci si k

/-- **Exact data ⇒ packing.** -/
theorem packs_of_cert {n : ℕ} {S : ℝ} (x y c s : Fin n → ℝ) (hu : ∀ i, c i ^ 2 + s i ^ 2 = 1)
    (hbox : ∀ i, InBox S (x i) (y i) (c i) (s i))
    (hsep : ∀ i j, i < j → SepPair (x i) (y i) (c i) (s i) (x j) (y j) (c j) (s j)) : Packs n S := by
  choose θ hc hs using fun i => exists_angle (hu i)
  refine ⟨fun i => (x i, y i), θ, fun i => unitSq_subset_container (hc i) (hs i) (hbox i), ?_⟩
  have pos : ∀ i j, i < j →
      Disjoint (interior (unitSq (x i, y i) (θ i))) (interior (unitSq (x j, y j) (θ j))) := by
    intro i j hij
    rcases hsep i j hij with ⟨k, hk⟩ | ⟨k, hk⟩
    · exact disjoint_of_sepSide (hc i) (hs i) (hc j) (hs j) (hu i) (hu j) hk
    · exact (disjoint_of_sepSide (hc j) (hs j) (hc i) (hs i) (hu j) (hu i) hk).symm
  intro i j hij
  rcases lt_or_gt_of_ne hij with h | h
  · exact pos i j h
  · exact (pos j i h).symm

end UnitSquarePacking
