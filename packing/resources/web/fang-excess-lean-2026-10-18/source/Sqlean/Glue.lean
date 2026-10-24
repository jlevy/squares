import Sqlean.Rect

/-!
# Gluing packings (Lemma 3 of the note)

* `PackIn ι K`: unit squares indexed by `ι`, each inside `K`, with pairwise disjoint interiors.
  `Packs n s` and `PacksR n W H` are `PackIn (Fin n)` of the container.
* `PackIn.mono`, `PackIn.comp` (restrict along an injection), `PackIn.translate`, `packIn_grid`
  (the integer block), `packIn_sigma` (a union of packings in boxes with disjoint interiors).
* `packs_of_le` (drop squares), `packs_mono` (enlarge the container), `minSide_le_of_packs`.
* **`glue`**: Lemma 3: from `PacksR nA (a - d) (b - d)` and `PacksR nB (a' - d) (b' - d)` with
  `n = b + b'`, `a, a' ≤ n`, `0 ≤ d ≤ b, b'` and `n - a' ≤ a - d`,
  `Packs (nA + (n - a) * b + (n - a') * (n - b) + nB) (n - d)`; `glue_sq` is the case `a' = b' = m`.
-/

open Set Function

namespace UnitSquarePacking

/-- Unit squares indexed by `ι`, each inside `K`, with pairwise disjoint interiors. -/
def PackIn (ι : Type) (K : Set (ℝ × ℝ)) : Prop :=
  ∃ (c : ι → ℝ × ℝ) (θ : ι → ℝ), (∀ i, unitSq (c i) (θ i) ⊆ K) ∧
    Pairwise fun i j => Disjoint (interior (unitSq (c i) (θ i))) (interior (unitSq (c j) (θ j)))

/-- The rectangle `[x0, x1] × [y0, y1]`. -/
def rect (x0 x1 y0 y1 : ℝ) : Set (ℝ × ℝ) := Icc x0 x1 ×ˢ Icc y0 y1

theorem packsR_iff_packIn {n : ℕ} {W H : ℝ} : PacksR n W H ↔ PackIn (Fin n) (rect 0 W 0 H) :=
  Iff.rfl

theorem packs_iff_packIn {n : ℕ} {s : ℝ} : Packs n s ↔ PackIn (Fin n) (rect 0 s 0 s) := Iff.rfl

lemma rect_subset {x0 x1 y0 y1 X0 X1 Y0 Y1 : ℝ} (h0 : X0 ≤ x0) (h1 : x1 ≤ X1) (h2 : Y0 ≤ y0)
    (h3 : y1 ≤ Y1) : rect x0 x1 y0 y1 ⊆ rect X0 X1 Y0 Y1 :=
  prod_mono (Icc_subset_Icc h0 h1) (Icc_subset_Icc h2 h3)

lemma interior_rect (x0 x1 y0 y1 : ℝ) : interior (rect x0 x1 y0 y1) = Ioo x0 x1 ×ˢ Ioo y0 y1 := by
  rw [rect, interior_prod_eq, interior_Icc, interior_Icc]

lemma rect_disjoint_x {x0 x1 y0 y1 x0' x1' y0' y1' : ℝ} (h : x1 ≤ x0') :
    Disjoint (interior (rect x0 x1 y0 y1)) (interior (rect x0' x1' y0' y1')) := by
  rw [interior_rect, interior_rect, Set.disjoint_left]
  rintro p ⟨⟨-, h1⟩, -⟩ ⟨⟨h2, -⟩, -⟩
  linarith

lemma rect_disjoint_y {x0 x1 y0 y1 x0' x1' y0' y1' : ℝ} (h : y1 ≤ y0') :
    Disjoint (interior (rect x0 x1 y0 y1)) (interior (rect x0' x1' y0' y1')) := by
  rw [interior_rect, interior_rect, Set.disjoint_left]
  rintro p ⟨-, ⟨-, h1⟩⟩ ⟨-, ⟨h2, -⟩⟩
  linarith

theorem PackIn.mono {ι : Type} {K K' : Set (ℝ × ℝ)} (h : PackIn ι K) (hK : K ⊆ K') :
    PackIn ι K' := by
  obtain ⟨c, θ, hs, hd⟩ := h
  exact ⟨c, θ, fun i => (hs i).trans hK, hd⟩

theorem PackIn.comp {ι κ : Type} {K : Set (ℝ × ℝ)} (h : PackIn ι K) (f : κ → ι)
    (hf : Injective f) : PackIn κ K := by
  obtain ⟨c, θ, hs, hd⟩ := h
  exact ⟨c ∘ f, θ ∘ f, fun i => hs (f i), fun i j hij => hd (hf.ne hij)⟩

lemma mem_unitSq_add {c v : ℝ × ℝ} {θ : ℝ} {p : ℝ × ℝ} :
    p ∈ unitSq (c + v) θ ↔ p - v ∈ unitSq c θ := by
  simp only [unitSq_eq_setOf, mem_ofPred_eq, Prod.fst_add, Prod.snd_add, Prod.fst_sub,
    Prod.snd_sub, sub_sub, add_comm v.1, add_comm v.2]

lemma mem_interior_unitSq_add {c v : ℝ × ℝ} {θ : ℝ} {p : ℝ × ℝ} :
    p ∈ interior (unitSq (c + v) θ) ↔ p - v ∈ interior (unitSq c θ) := by
  simp only [interior_unitSq, mem_ofPred_eq, Prod.fst_add, Prod.snd_add, Prod.fst_sub,
    Prod.snd_sub, sub_sub, add_comm v.1, add_comm v.2]

/-- Translate a packing of `[0, W] × [0, H]` to `[x0, x1] × [y0, y1]`. -/
theorem PackIn.translate {ι : Type} {W H x0 x1 y0 y1 : ℝ} (h : PackIn ι (rect 0 W 0 H))
    (hx : x1 = x0 + W) (hy : y1 = y0 + H) : PackIn ι (rect x0 x1 y0 y1) := by
  obtain ⟨c, θ, hs, hd⟩ := h
  refine ⟨fun i => c i + (x0, y0), θ, fun i p hp => ?_, fun i j hij => ?_⟩
  · have := hs i (mem_unitSq_add.1 hp)
    simp only [rect, mem_prod, mem_Icc, Prod.fst_sub, Prod.snd_sub] at this ⊢
    subst hx hy
    refine ⟨⟨?_, ?_⟩, ?_, ?_⟩ <;> linarith [this.1.1, this.1.2, this.2.1, this.2.2]
  · dsimp only
    rw [Set.disjoint_left]
    intro p hpi hpj
    exact Set.disjoint_left.1 (hd hij) (mem_interior_unitSq_add.1 hpi)
      (mem_interior_unitSq_add.1 hpj)

lemma unitSq_zero (c : ℝ × ℝ) :
    unitSq c 0 = {p | |p.1 - c.1| ≤ 1 / 2 ∧ |p.2 - c.2| ≤ 1 / 2} := by
  rw [unitSq_eq_setOf]; simp

lemma interior_unitSq_zero (c : ℝ × ℝ) :
    interior (unitSq c 0) = {p | |p.1 - c.1| < 1 / 2 ∧ |p.2 - c.2| < 1 / 2} := by
  rw [interior_unitSq]; simp

lemma far_of_ne_nat {i j : ℕ} {x u : ℝ} (hij : i ≠ j) (hu : |u - (x + i + 1 / 2)| < 1 / 2)
    (hv : |u - (x + j + 1 / 2)| < 1 / 2) : False := by
  rw [abs_lt] at hu hv
  rcases lt_or_gt_of_ne hij with h | h
  · have : (i : ℝ) + 1 ≤ j := by exact_mod_cast h
    linarith [hu.1, hu.2, hv.1, hv.2]
  · have : (j : ℝ) + 1 ≤ i := by exact_mod_cast h
    linarith [hu.1, hu.2, hv.1, hv.2]

/-- The integer block: `p × q` axis-parallel unit squares fill `[x0, x0 + p] × [y0, y0 + q]`. -/
theorem packIn_grid (p q : ℕ) {x0 x1 y0 y1 : ℝ} (hx : x1 = x0 + p) (hy : y1 = y0 + q) :
    PackIn (Fin p × Fin q) (rect x0 x1 y0 y1) := by
  refine ⟨fun ij => (x0 + (ij.1 : ℕ) + 1 / 2, y0 + (ij.2 : ℕ) + 1 / 2), fun _ => 0,
    fun ij z hz => ?_, fun ij kl hne => ?_⟩
  · rw [unitSq_zero] at hz
    obtain ⟨h1, h2⟩ := hz
    rw [abs_le] at h1 h2
    have hi : ((ij.1 : ℕ) : ℝ) + 1 ≤ p := by exact_mod_cast ij.1.2
    have hj : ((ij.2 : ℕ) : ℝ) + 1 ≤ q := by exact_mod_cast ij.2.2
    have hi0 : (0 : ℝ) ≤ ((ij.1 : ℕ) : ℝ) := Nat.cast_nonneg _
    have hj0 : (0 : ℝ) ≤ ((ij.2 : ℕ) : ℝ) := Nat.cast_nonneg _
    simp only [rect, mem_prod, mem_Icc]
    subst hx hy
    refine ⟨⟨?_, ?_⟩, ?_, ?_⟩ <;> linarith [h1.1, h1.2, h2.1, h2.2]
  · dsimp only
    rw [Set.disjoint_left]
    intro z hz1 hz2
    rw [interior_unitSq_zero] at hz1 hz2
    obtain ⟨a1, b1⟩ := hz1
    obtain ⟨a2, b2⟩ := hz2
    by_cases h1 : (ij.1 : ℕ) = (kl.1 : ℕ)
    · have h2 : (ij.2 : ℕ) ≠ (kl.2 : ℕ) := by
        intro h2; exact hne (Prod.ext (Fin.ext h1) (Fin.ext h2))
      exact far_of_ne_nat h2 b1 b2
    · exact far_of_ne_nat h1 a1 a2

/-- Packings in boxes with pairwise disjoint interiors combine. -/
theorem packIn_sigma {κ : Type} {ι : κ → Type} {K : κ → Set (ℝ × ℝ)}
    (h : ∀ k, PackIn (ι k) (K k))
    (hd : Pairwise fun k l => Disjoint (interior (K k)) (interior (K l))) :
    PackIn (Σ k, ι k) (⋃ k, K k) := by
  choose c θ hs hp using h
  refine ⟨fun x => c x.1 x.2, fun x => θ x.1 x.2,
    fun x => (hs x.1 x.2).trans (subset_iUnion K x.1), ?_⟩
  rintro ⟨k, i⟩ ⟨l, j⟩ hne
  by_cases hkl : k = l
  · subst hkl
    have hij : i ≠ j := fun h => hne (by rw [h])
    exact hp k hij
  · exact (hd hkl).mono (interior_mono (hs k i)) (interior_mono (hs l j))

theorem packs_of_packIn {ι : Type} [Fintype ι] {K : Set (ℝ × ℝ)} {s : ℝ} (h : PackIn ι K)
    (hK : K ⊆ rect 0 s 0 s) : Packs (Fintype.card ι) s :=
  (h.mono hK).comp (Fintype.equivFin ι).symm (Fintype.equivFin ι).symm.injective

/-- Drop squares. -/
theorem packs_of_le {m n : ℕ} {s : ℝ} (h : Packs n s) (hmn : m ≤ n) : Packs m s :=
  PackIn.comp h (Fin.castLE hmn) (Fin.castLE_injective hmn)

/-- Enlarge the container. -/
theorem packs_mono {n : ℕ} {s t : ℝ} (h : Packs n s) (hst : s ≤ t) : Packs n t :=
  PackIn.mono h (rect_subset le_rfl hst le_rfl hst)

theorem nonneg_of_packs {n : ℕ} {s : ℝ} (hn : 1 ≤ n) (h : Packs n s) : 0 ≤ s := by
  obtain ⟨c, θ, hs, -⟩ := h
  have hc : c ⟨0, hn⟩ ∈ unitSq (c ⟨0, hn⟩) (θ ⟨0, hn⟩) := by
    rw [unitSq_eq_setOf]; simp
  have := hs ⟨0, hn⟩ hc
  simp only [container, mem_prod, mem_Icc] at this
  linarith [this.1.1, this.1.2]

theorem minSide_le_of_packs {n : ℕ} {s : ℝ} (hn : 1 ≤ n) (h : Packs n s) : minSide n ≤ s :=
  csInf_le ⟨0, fun _ ht => nonneg_of_packs hn ht⟩ h

/-- **Lemma 3 (gluing).** `A` (an `(a - d) × (b - d)` packing) top left, the integer block
`(n - a) × b` top right, the integer block `(n - a') × (n - b)` bottom left, `B` (an
`(a' - d) × (b' - d)` packing) bottom right. -/
theorem glue {nA nB a b a' b' n : ℕ} {d : ℝ} (hA : PacksR nA (a - d) (b - d))
    (hB : PacksR nB (a' - d) (b' - d)) (hn : n = b + b') (hd : 0 ≤ d) (hdb : d ≤ b)
    (hdb' : d ≤ b') (ha : a ≤ n) (ha' : a' ≤ n) (hc : ((n - a' : ℕ) : ℝ) ≤ a - d) :
    Packs (nA + (n - a) * b + (n - a') * (n - b) + nB) (n - d) := by
  subst hn
  set N : ℝ := ((b + b' : ℕ) : ℝ) with hN
  have hNbb : N = b + b' := by rw [hN]; push_cast; ring
  have e1 : (((b + b' - a : ℕ) : ℕ) : ℝ) = N - a := by rw [Nat.cast_sub ha]
  have e2 : (((b + b' - a' : ℕ) : ℕ) : ℝ) = N - a' := by rw [Nat.cast_sub ha']
  have e3 : (((b + b' - b : ℕ) : ℕ) : ℝ) = b' := by rw [Nat.add_sub_cancel_left]
  have hc' : N - a' ≤ a - d := by rw [← e2]; exact hc
  have hc0 : (0 : ℝ) ≤ N - a' := by rw [← e2]; exact Nat.cast_nonneg _
  have ha'' : (a : ℝ) ≤ N := by rw [hN]; exact_mod_cast ha
  -- the four pieces
  let m : Fin 4 → ℕ := ![nA, (b + b' - a) * b, (b + b' - a') * (b + b' - b), nB]
  let K : Fin 4 → Set (ℝ × ℝ) := ![rect 0 (a - d) (N - b) (N - d),
    rect (a - d) (N - d) (N - d - b) (N - d), rect 0 (N - a') 0 (N - b),
    rect (N - a') (N - d) 0 (N - d - b)]
  have pA : PackIn (Fin nA) (rect 0 (a - d) (N - b) (N - d)) :=
    PackIn.translate (packsR_iff_packIn.1 hA) (by ring) (by ring)
  have pD : PackIn (Fin ((b + b' - a) * b)) (rect (a - d) (N - d) (N - d - b) (N - d)) :=
    (packIn_grid (b + b' - a) b (by rw [e1]; ring) (by ring)).comp finProdFinEquiv.symm
      finProdFinEquiv.symm.injective
  have pC : PackIn (Fin ((b + b' - a') * (b + b' - b))) (rect 0 (N - a') 0 (N - b)) :=
    (packIn_grid (b + b' - a') (b + b' - b) (by rw [e2]; ring) (by rw [e3, hNbb]; ring)).comp
      finProdFinEquiv.symm finProdFinEquiv.symm.injective
  have pB : PackIn (Fin nB) (rect (N - a') (N - d) 0 (N - d - b)) :=
    PackIn.translate (packsR_iff_packIn.1 hB) (by ring) (by rw [hNbb]; ring)
  have hall : ∀ k, PackIn (Fin (m k)) (K k) := by
    intro k; fin_cases k
    · exact pA
    · exact pD
    · exact pC
    · exact pB
  have hdis : Pairwise fun k l => Disjoint (interior (K k)) (interior (K l)) := by
    intro k l hkl
    fin_cases k <;> fin_cases l <;> simp (config := { decide := true }) only [K] at hkl ⊢
    all_goals first
      | exact absurd rfl hkl
      | exact rect_disjoint_x (by linarith)
      | exact rect_disjoint_y (by linarith)
      | exact (rect_disjoint_x (by linarith)).symm
      | exact (rect_disjoint_y (by linarith)).symm
  have hsub : (⋃ k, K k) ⊆ rect 0 (N - d) 0 (N - d) := by
    refine iUnion_subset fun k => ?_
    fin_cases k <;> simp only [K] <;> apply rect_subset <;> linarith
  have h := packs_of_packIn (packIn_sigma hall hdis) hsub
  have hcard : Fintype.card (Σ k, Fin (m k)) =
      nA + (b + b' - a) * b + (b + b' - a') * (b + b' - b) + nB := by
    simp [m, Fin.sum_univ_four, add_assoc]
  rw [hcard] at h
  exact h

/-- Lemma 3 with a square second piece: `a' = b' = m`, `n = b + m`. -/
theorem glue_sq {nA nB a b m n : ℕ} {d : ℝ} (hA : PacksR nA (a - d) (b - d))
    (hB : Packs nB (m - d)) (hn : n = b + m) (hd : 0 ≤ d) (hdb : d ≤ b) (hdm : d ≤ m)
    (ha : a ≤ n) (hc : (b : ℝ) ≤ a - d) :
    Packs (nA + (n - a) * b + (n - m) * (n - b) + nB) (n - d) := by
  refine glue hA (packs_iff_packsR.1 hB) hn hd hdb hdm ha (by omega) ?_
  rw [show n - m = b by omega]; exact hc

end UnitSquarePacking
