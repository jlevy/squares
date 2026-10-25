import Sqpack.RyuBand

/-!
# Lifted bands and their end regions (Ryu, Section 5)

S. Ryu, *k² − c upper bounds* (squarepacker/k2-minus-c-upper v1.1; jlevy/squares#471, #486), Lemma 5.1.  A band of
`R` rows of `b` squares at angle `θ` (`cos θ = γ`, `sin θ = σ`) in the strip `[0, w] × [0, L]`, `w = bγ + σ`, lifted
by `y₀`, leaves two end regions:

* below the first row, `endReg y₀ = {0 ≤ X ≤ w, 0 ≤ Y, γY − σX ≤ γy₀ − σ²}` (Ryu's `Reg(y₀)`: `Y ≤ y₀ + (X − σ) tan θ`);
* above the last row, the rotation by `π` about the centre of the strip of `endReg y₁`, where
  `y₀ + y₁ + (R − 1)/γ + bσ + γ ≤ L`.

`band_ends`: any packings of the two end regions, together with the rows, pack the strip.  The proof separates the
three parts by the rotated coordinate `V = −σX + γY` (`halfplane_disjoint`).

`axis_layers`: axis-parallel layers `[w − n_j, w] × [j, j + 1]` pack `endReg y` when each fits under the ceiling.
-/

namespace UnitSquarePacking.Ryu

open Set UnitSquarePacking.Conjectures UnitSquarePacking.FangGlue

/-! ## Separation by a line -/

/-- Two regions on the two closed sides of a line have disjoint interiors. -/
lemma halfplane_disjoint {R R' : Set (ℝ × ℝ)} {α β c : ℝ} (hαβ : α ^ 2 + β ^ 2 ≠ 0)
    (h : R ⊆ {p | α * p.1 + β * p.2 ≤ c}) (h' : R' ⊆ {p | c ≤ α * p.1 + β * p.2}) :
    Disjoint (interior R) (interior R') := by
  rw [Set.disjoint_left]
  intro x hx hx'
  have hx2 : x ∈ interior (R ∩ R') := by rw [interior_inter]; exact ⟨hx, hx'⟩
  rw [mem_interior_iff_mem_nhds, Metric.mem_nhds_iff] at hx2
  obtain ⟨ε, hε, hball⟩ := hx2
  set M := max |α| |β| + 1 with hM
  have hM0 : 0 < M := by positivity
  set e := ε / (2 * M) with he
  have he0 : 0 < e := by positivity
  set y : ℝ × ℝ := (x.1 + e * α, x.2 + e * β) with hy
  have hyb : y ∈ Metric.ball x ε := by
    rw [Metric.mem_ball, Prod.dist_eq, Real.dist_eq, Real.dist_eq]
    simp only [hy, add_sub_cancel_left, abs_mul, abs_of_pos he0]
    have h1 : |α| ≤ M - 1 := by rw [hM]; simp
    have h2 : |β| ≤ M - 1 := by rw [hM]; simp
    have hlt : e * M < ε := by rw [he]; field_simp; linarith
    apply max_lt <;> nlinarith [abs_nonneg α, abs_nonneg β]
  have hx3 : x ∈ Metric.ball x ε := Metric.mem_ball_self hε
  have a1 := h (hball hyb).1
  have a2 := h' (hball hx3).2
  simp only [mem_ofPred_eq, hy] at a1 a2
  have hpos : 0 < α ^ 2 + β ^ 2 := lt_of_le_of_ne (by positivity) (Ne.symm hαβ)
  nlinarith [mul_pos he0 hpos]

/-- The `V`-extent of a square at angle `θ`: `V` of its centre `± 1/2`. -/
lemma unitSq_V {c : ℝ × ℝ} {θ : ℝ} :
    unitSq c θ ⊆ {p | V (Real.cos θ) (Real.sin θ) c - 1 / 2 ≤ V (Real.cos θ) (Real.sin θ) p ∧
      V (Real.cos θ) (Real.sin θ) p ≤ V (Real.cos θ) (Real.sin θ) c + 1 / 2} := by
  have hu := Real.sin_sq_add_cos_sq θ
  intro p hp
  have up := unitSq_subset_half (c₀ := c) (θ := θ) (α := -Real.sin θ) (β := Real.cos θ)
    (c := V (Real.cos θ) (Real.sin θ) c + 1 / 2) (fun a b ha hb => by
      simp only [V]; rcases hb with rfl | rfl <;> nlinarith) hp
  have lo := unitSq_subset_half (c₀ := c) (θ := θ) (α := Real.sin θ) (β := -Real.cos θ)
    (c := -(V (Real.cos θ) (Real.sin θ) c - 1 / 2)) (fun a b ha hb => by
      simp only [V]; rcases hb with rfl | rfl <;> nlinarith) hp
  simp only [mem_ofPred_eq, V] at up lo ⊢
  constructor <;> linarith

/-! ## The rotation by `π` about the centre of `[0, w] × [0, L]` -/

lemma mem_unitSq_rot180 {c p : ℝ × ℝ} {θ w L : ℝ} :
    (w - p.1, L - p.2) ∈ unitSq c θ ↔ p ∈ unitSq (w - c.1, L - c.2) θ := by
  rw [unitSq_eq_setOf, unitSq_eq_setOf]
  simp only [mem_ofPred_eq]
  constructor <;> rintro ⟨h1, h2⟩
  · refine ⟨?_, ?_⟩
    · rw [← abs_neg]; convert h1 using 2; ring
    · rw [← abs_neg]; convert h2 using 2; ring
  · refine ⟨?_, ?_⟩
    · rw [← abs_neg]; convert h1 using 2; ring
    · rw [← abs_neg]; convert h2 using 2; ring

lemma mem_interior_unitSq_rot180 {c p : ℝ × ℝ} {θ w L : ℝ} :
    (w - p.1, L - p.2) ∈ interior (unitSq c θ) ↔ p ∈ interior (unitSq (w - c.1, L - c.2) θ) := by
  rw [interior_unitSq, interior_unitSq]
  simp only [mem_ofPred_eq]
  constructor <;> rintro ⟨h1, h2⟩
  · refine ⟨?_, ?_⟩
    · rw [← abs_neg]; convert h1 using 2; ring
    · rw [← abs_neg]; convert h2 using 2; ring
  · refine ⟨?_, ?_⟩
    · rw [← abs_neg]; convert h1 using 2; ring
    · rw [← abs_neg]; convert h2 using 2; ring

/-- A unit square is centrally symmetric, so `p ↦ (w − p.1, L − p.2)` maps packings to packings. -/
lemma _root_.UnitSquarePacking.Conjectures.PacksIn.rot180 {n : ℕ} {S : Set (ℝ × ℝ)} (w L : ℝ) (h : PacksIn n S) :
    PacksIn n {p | (w - p.1, L - p.2) ∈ S} := by
  obtain ⟨c, θ, hin, hd⟩ := h
  refine ⟨fun i => (w - (c i).1, L - (c i).2), θ, fun i p hp => hin i (mem_unitSq_rot180.2 hp), fun i j hij => ?_⟩
  change Disjoint _ _
  rw [Set.disjoint_left]
  intro p hpi hpj
  exact Set.disjoint_left.1 (hd hij) (mem_interior_unitSq_rot180.2 hpi) (mem_interior_unitSq_rot180.2 hpj)

/-! ## End regions -/

/-- Ryu's `Reg(y)` in the strip frame: `0 ≤ X ≤ w`, `0 ≤ Y`, `Y ≤ y + (X − σ) σ/γ`. -/
def endReg (γ σ w y : ℝ) : Set (ℝ × ℝ) :=
  {p | 0 ≤ p.1 ∧ p.1 ≤ w ∧ 0 ≤ p.2 ∧ γ * p.2 - σ * p.1 ≤ γ * y - σ ^ 2}

/-- `endReg y` lies below `Y = y + bσ` (for `w = bγ + σ`). -/
lemma endReg_subset {γ σ y L : ℝ} {b : ℝ} (hγ : 0 < γ) (hσ : 0 ≤ σ) (hL : y + b * σ ≤ L) :
    endReg γ σ (b * γ + σ) y ⊆ rect (b * γ + σ) L := by
  rintro p ⟨h1, h2, h3, h4⟩
  refine ⟨⟨h1, h2⟩, h3, ?_⟩
  have : γ * p.2 ≤ γ * (y + b * σ) := by nlinarith
  nlinarith [le_of_mul_le_mul_left this hγ]

/-- **A lifted band** (Ryu's rows `B(P_j)`, `P_j = (σ, y₀ + j/γ)`): `R` rows of `b` squares in the strip, inside the
`V`-slab `[γy₀ − σ², γy₀ − σ² + R]`. -/
theorem band_lift {θ : ℝ} (hγ : 0 < Real.cos θ) (hσ : 0 ≤ Real.sin θ) (R b : ℕ) {y₀ L : ℝ} (hy₀ : 0 ≤ y₀)
    (hL : y₀ + ((R - 1) / Real.cos θ + b * Real.sin θ + Real.cos θ) ≤ L) :
    PacksIn (R * b) (rect (b * Real.cos θ + Real.sin θ) L ∩
      {p | Real.cos θ * y₀ - Real.sin θ ^ 2 ≤ V (Real.cos θ) (Real.sin θ) p ∧
        V (Real.cos θ) (Real.sin θ) p ≤ Real.cos θ * y₀ - Real.sin θ ^ 2 + R}) := by
  set γ := Real.cos θ with hγd
  set σ := Real.sin θ with hσd
  have hu : γ ^ 2 + σ ^ 2 = 1 := by rw [hγd, hσd, add_comm]; exact Real.sin_sq_add_cos_sq θ
  have hB := band_explicit hγ hσ R b
  set H := (R - 1) / γ + b * σ + γ with hH
  have P0 : PacksIn (R * b) (rect (b * γ + σ) H ∩ {p | -σ ^ 2 ≤ V γ σ p ∧ V γ σ p ≤ -σ ^ 2 + R}) := by
    refine ⟨bandCen γ σ R b, fun _ => θ, fun k p hp => ⟨hB.1 k hp, ?_⟩, hB.2⟩
    have hv := V_bandCen hu k
    have := unitSq_V hp
    rw [← hγd, ← hσd] at this
    simp only [mem_ofPred_eq] at this ⊢
    constructor <;> linarith [this.1, this.2, hv.1, hv.2]
  refine (P0.shift (0, y₀)).mono ?_
  rintro p ⟨⟨⟨h1, h2⟩, h3, h4⟩, h5, h6⟩
  simp only [Prod.fst_sub, Prod.snd_sub, sub_zero, V] at h1 h2 h3 h4 h5 h6
  refine ⟨⟨⟨h1, h2⟩, by linarith, by linarith⟩, ?_, ?_⟩ <;> simp only [V] <;> nlinarith

/-- **Ryu's Lemma 5.1.**  The rows of a band lifted by `y₀`, a packing of `endReg y₀` and the rotation by `π` of a
packing of `endReg y₁` pack the strip, if `y₀ + y₁ + (R − 1)/γ + bσ + γ ≤ L`. -/
theorem band_ends {θ : ℝ} (hγ : 0 < Real.cos θ) (hσ : 0 ≤ Real.sin θ) (R b : ℕ) {y₀ y₁ L : ℝ} {n₀ n₁ : ℕ}
    (hR : 1 ≤ R) (hy₀ : 0 ≤ y₀) (hy₁ : 0 ≤ y₁)
    (hL : y₀ + y₁ + ((R - 1) / Real.cos θ + b * Real.sin θ + Real.cos θ) ≤ L)
    (h₀ : PacksIn n₀ (endReg (Real.cos θ) (Real.sin θ) (b * Real.cos θ + Real.sin θ) y₀))
    (h₁ : PacksIn n₁ (endReg (Real.cos θ) (Real.sin θ) (b * Real.cos θ + Real.sin θ) y₁)) :
    PacksIn (n₀ + R * b + n₁) (rect (b * Real.cos θ + Real.sin θ) L) := by
  set γ := Real.cos θ with hγd
  set σ := Real.sin θ with hσd
  have hu : γ ^ 2 + σ ^ 2 = 1 := by rw [hγd, hσd, add_comm]; exact Real.sin_sq_add_cos_sq θ
  set w := b * γ + σ with hw
  have hb0 : (0 : ℝ) ≤ b := by positivity
  have hR0 : (1 : ℝ) ≤ R := by exact_mod_cast hR
  have hd0 : 0 ≤ ((R : ℝ) - 1) / γ := div_nonneg (by linarith) hγ.le
  have hγ1 : γ ≤ 1 := by nlinarith
  have hinv : 1 ≤ 1 / γ := by rw [le_div_iff₀ hγ]; linarith
  have hH : b * σ + γ ≤ (R - 1) / γ + b * σ + γ := by linarith
  set a := γ * y₀ - σ ^ 2 with ha
  have PB := band_lift (L := L) hγ hσ R b hy₀ (by linarith)
  rw [← hγd, ← hσd] at PB
  have P1 := h₁.rot180 w L
  -- the three regions
  set S₀ := endReg γ σ w y₀ with hS₀
  set SB := rect w L ∩ {p | a ≤ V γ σ p ∧ V γ σ p ≤ a + R} with hSB
  set S₁ := {p : ℝ × ℝ | (w - p.1, L - p.2) ∈ endReg γ σ w y₁} with hS₁
  have hαβ : (-σ) ^ 2 + γ ^ 2 ≠ 0 := by rw [neg_sq, add_comm, hu]; norm_num
  have sub0 : S₀ ⊆ {p | -σ * p.1 + γ * p.2 ≤ a} := by
    rintro p ⟨_, _, _, h4⟩; simp only [mem_ofPred_eq]; linarith
  have subB : SB ⊆ {p | a ≤ -σ * p.1 + γ * p.2} ∩ {p | -σ * p.1 + γ * p.2 ≤ a + R} := by
    rintro p ⟨_, h5, h6⟩; simp only [V] at h5 h6; exact ⟨by simp only [mem_ofPred_eq]; linarith, by
      simp only [mem_ofPred_eq]; linarith⟩
  have sub1 : S₁ ⊆ {p | a + R ≤ -σ * p.1 + γ * p.2} := by
    rintro p ⟨_, _, _, h4⟩
    simp only [mem_ofPred_eq] at h4 ⊢
    -- `γ(L − y₀ − y₁) ≥ R − 1 + bσγ + γ²`
    have hrow : γ * (L - y₀ - y₁) ≥ R - 1 + b * σ * γ + γ ^ 2 := by
      have := mul_le_mul_of_nonneg_left (show (R - 1) / γ + b * σ + γ ≤ L - y₀ - y₁ by linarith) hγ.le
      rw [mul_add, mul_add, mul_div_cancel₀ _ hγ.ne'] at this
      nlinarith
    nlinarith
  have d01 : Disjoint (interior S₀) (interior SB) :=
    halfplane_disjoint hαβ sub0 (fun p hp => (subB hp).1)
  have P01 := h₀.union PB d01
  have d2 : Disjoint (interior (S₀ ∪ SB)) (interior S₁) := by
    refine halfplane_disjoint hαβ (c := a + R) ?_ sub1
    rintro p (hp | hp)
    · have := sub0 hp; simp only [mem_ofPred_eq] at this ⊢; linarith
    · exact (subB hp).2
  refine (P01.union P1 d2).mono ?_
  rintro p ((hp | hp) | hp)
  · exact endReg_subset hγ hσ (by linarith) hp
  · exact hp.1
  · have := endReg_subset (L := L) hγ hσ (by linarith) hp
    simp only [rect, mem_prod, mem_Icc] at this ⊢
    refine ⟨⟨?_, ?_⟩, ?_, ?_⟩ <;> linarith [this.1.1, this.1.2, this.2.1, this.2.2]

/-! ## Axis-parallel layers in an end region -/

/-- **Axis layers**: for `j < J`, `n_j` axis squares `[w − n_j, w] × [j, j + 1]`, each fitting under the ceiling at its
top-left corner, pack `endReg y`. -/
theorem axis_layers {γ σ w y : ℝ} (hγ : 0 ≤ γ) (hσ : 0 ≤ σ) (J : ℕ) (n : ℕ → ℕ)
    (hw : ∀ j < J, (n j : ℝ) ≤ w)
    (hc : ∀ j < J, γ * (j + 1) - σ * (w - n j) ≤ γ * y - σ ^ 2) :
    PacksIn (∑ j ∈ Finset.range J, n j) (endReg γ σ w y ∩ {p | p.2 ≤ J}) := by
  induction J with
  | zero =>
    simp only [Finset.range_zero, Finset.sum_empty]; exact PacksIn.zero _
  | succ J ih =>
    rw [Finset.sum_range_succ]
    have IH := ih (fun j hj => hw j (by omega)) (fun j hj => hc j (by omega))
    have hwJ := hw J (by omega)
    have hcJ := hc J (by omega)
    have PL := ((packsIn_block (n J) 1).toBox (w - n J) J)
    simp only [Nat.cast_one, mul_one] at PL
    have hd : Disjoint (interior (endReg γ σ w y ∩ {p | p.2 ≤ J}))
        (interior (box (w - n J) (w - n J + n J) J (J + 1))) := by
      refine halfplane_disjoint (α := 0) (β := 1) (c := J) (by norm_num) ?_ ?_
      · rintro p ⟨_, hp⟩; simp only [mem_ofPred_eq] at hp ⊢; linarith
      · rintro p ⟨_, hp, _⟩; simp only [mem_ofPred_eq]; linarith
    refine (IH.union PL hd).mono ?_
    rintro p (⟨hp, hp'⟩ | ⟨⟨h1, h2⟩, h3, h4⟩)
    · exact ⟨hp, show p.2 ≤ ((J + 1 : ℕ) : ℝ) by have := hp'.out; push_cast; linarith⟩
    · refine ⟨⟨by linarith [(Nat.cast_nonneg (n J) : (0 : ℝ) ≤ n J)], by linarith, by
        linarith [(Nat.cast_nonneg J : (0 : ℝ) ≤ J)], ?_⟩, ?_⟩
      · nlinarith [mul_le_mul_of_nonneg_left h4 hγ, mul_le_mul_of_nonneg_left h1 hσ]
      · simp only [mem_ofPred_eq]; push_cast; linarith

end UnitSquarePacking.Ryu
