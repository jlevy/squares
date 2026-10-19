import Sqpack.ExactPack

/-!
# Local minima of the side

`IsLocalMinPacking n S c θ`: the packing `(c, θ)` of `n` unit squares in `[0, S]²` has a ball around it in pose
space (centres within `ε`, angles within `ε` modulo quarter turns, squares matched by index) containing no packing
in a smaller square.  (A broad plateau with a downhill exit far away is a local minimum in this sense; this is the
first, easy notion.)

`rigidity`: the algebraic core of the first-order argument.  Rows `h_r ≥ 0` with linear parts `L_r` up to `M δ²`,
multipliers `λ_r ≥ λ_min > 0` with `Σ λ_r L_r = e_S`, and an approximate left inverse `G` of `L`
(`‖G L - I‖ ≤ 1/2`) force `Δ_S ≥ 0` once `2 ‖G‖ Λ M δ < λ_min`, where `δ` is the sup norm of `Δ`.
-/

namespace UnitSquarePacking

open Set Real

/-- `n` unit squares with centres `c` and angles `θ` form a packing in `[0, s]²`. -/
def IsPacking (n : ℕ) (s : ℝ) (c : Fin n → ℝ × ℝ) (θ : Fin n → ℝ) : Prop :=
  (∀ i, unitSq (c i) (θ i) ⊆ container s) ∧
    Pairwise fun i j => Disjoint (interior (unitSq (c i) (θ i))) (interior (unitSq (c j) (θ j)))

lemma packs_iff_isPacking {n : ℕ} {s : ℝ} : Packs n s ↔ ∃ c θ, IsPacking n s c θ := Iff.rfl

/-- `θ` is within `ε` of `θ'` modulo quarter turns (a square is unchanged by a quarter turn). -/
def AngleNear (ε θ θ' : ℝ) : Prop := ∃ m : ℤ, |θ - θ' - m * (π / 2)| < ε

/-- **Local minimum of the side**: a packing in `[0, S]²` with a pose-space ball around it containing no packing
in a smaller square. -/
def IsLocalMinPacking (n : ℕ) (S : ℝ) (c : Fin n → ℝ × ℝ) (θ : Fin n → ℝ) : Prop :=
  IsPacking n S c θ ∧ ∃ ε > 0, ∀ (s : ℝ) (c' : Fin n → ℝ × ℝ) (θ' : Fin n → ℝ), IsPacking n s c' θ' →
    (∀ i, |(c' i).1 - (c i).1| < ε ∧ |(c' i).2 - (c i).2| < ε ∧ AngleNear ε (θ' i) (θ i)) → S ≤ s

lemma container_mono {s s' : ℝ} (h : s ≤ s') : container s ⊆ container s' := by
  intro p hp
  simp only [container, mem_prod, mem_Icc] at hp ⊢
  exact ⟨⟨hp.1.1, hp.1.2.trans h⟩, hp.2.1, hp.2.2.trans h⟩

lemma IsPacking.mono {n : ℕ} {s s' : ℝ} {c : Fin n → ℝ × ℝ} {θ : Fin n → ℝ} (h : IsPacking n s c θ)
    (hs : s ≤ s') : IsPacking n s' c θ :=
  ⟨fun i => (h.1 i).trans (container_mono hs), h.2⟩

lemma unitSq_add_pi_div_two (c : ℝ × ℝ) (θ : ℝ) : unitSq c (θ + π / 2) = unitSq c θ := by
  rw [unitSq_eq_setOf, unitSq_eq_setOf]
  ext p
  simp only [mem_setOf_eq, Real.cos_add_pi_div_two, Real.sin_add_pi_div_two, abs_le]
  constructor <;> rintro ⟨⟨h1, h2⟩, h3, h4⟩ <;> refine ⟨⟨?_, ?_⟩, ?_, ?_⟩ <;> linarith

lemma unitSq_add_int_mul (c : ℝ × ℝ) (θ : ℝ) (m : ℤ) : unitSq c (θ + m * (π / 2)) = unitSq c θ := by
  induction m using Int.induction_on with
  | zero => simp
  | succ k ih =>
    rw [show θ + (((k : ℤ) + 1 : ℤ) : ℝ) * (π / 2) = (θ + ((k : ℤ) : ℝ) * (π / 2)) + π / 2 by push_cast; ring,
      unitSq_add_pi_div_two, ih]
  | pred k ih =>
    rw [← ih, show θ + ((-(k : ℤ) : ℤ) : ℝ) * (π / 2) = (θ + ((-(k : ℤ) - 1 : ℤ) : ℝ) * (π / 2)) + π / 2 by
      push_cast; ring, unitSq_add_pi_div_two]

/-! ## The rigidity lemma -/

theorem rigidity {ι κ : Type*} [Fintype ι] [DecidableEq ι] [Fintype κ] [DecidableEq κ]
    (L : ι → κ → ℝ) (lam : ι → ℝ) (G : κ → ι → ℝ) (iS : κ)
    {lmin Λ Gn M δ : ℝ} (hlmin : 0 < lmin) (hlam : ∀ r, lmin ≤ lam r) (hΛ : ∑ r, lam r ≤ Λ)
    (hsum : ∀ v, ∑ r, lam r * L r v = if v = iS then 1 else 0)
    (hGn : ∀ v, ∑ r, |G v r| ≤ Gn)
    (hG : ∀ v, ∑ w, |(∑ r, G v r * L r w) - (if v = w then 1 else 0)| ≤ 1 / 2)
    (hM : 0 ≤ M) (Δ : κ → ℝ) (hδ : ∀ v, |Δ v| ≤ δ) (hδmax : ∃ v, |Δ v| = δ)
    (h : ι → ℝ) (hh : ∀ r, 0 ≤ h r) (hQ : ∀ r, |h r - ∑ v, L r v * Δ v| ≤ M * δ ^ 2)
    (hsmall : 2 * Gn * Λ * M * δ < lmin) : 0 ≤ Δ iS := by
  by_contra hneg
  push_neg at hneg
  set l : ι → ℝ := fun r => ∑ v, L r v * Δ v with hl
  have hlam0 : ∀ r, 0 ≤ lam r := fun r => hlmin.le.trans (hlam r)
  -- Σ λ_r l_r = Δ_S
  have key : ∑ r, lam r * l r = Δ iS := by
    simp only [hl, Finset.mul_sum]
    rw [Finset.sum_comm]
    have : ∀ v, ∑ r, lam r * (L r v * Δ v) = (if v = iS then 1 else 0) * Δ v := by
      intro v; rw [← hsum v, Finset.sum_mul]; congr 1; ext r; ring
    simp only [this, ite_mul, one_mul, zero_mul, Finset.sum_ite_eq', Finset.mem_univ, if_true]
  have hlo : ∀ r, -(M * δ ^ 2) ≤ l r := by
    intro r; have := hQ r; rw [abs_le] at this; have := hh r; simp only [hl]; linarith [this]
  -- Λ ≥ λ_min (the rows are nonempty: Σ λ_r L_r = e_S)
  have hne : Nonempty ι := by
    by_contra hc
    rw [not_nonempty_iff] at hc
    have := hsum iS
    simp at this
  obtain ⟨r0⟩ := hne
  have hΛl : lmin ≤ Λ := by
    have : lam r0 ≤ ∑ r, lam r := Finset.single_le_sum (fun r _ => hlam0 r) (Finset.mem_univ r0)
    linarith [hlam r0]
  have hΛ0 : 0 ≤ Λ := hlmin.le.trans hΛl
  -- upper bound: λ_r l_r ≤ Λ M δ²
  have hhi : ∀ r, lam r * l r ≤ Λ * (M * δ ^ 2) := by
    intro r
    have hs := Finset.add_sum_erase Finset.univ (fun r => lam r * l r) (Finset.mem_univ r)
    have h1 : ∑ r' ∈ Finset.univ.erase r, -(lam r' * l r') ≤ ∑ r' ∈ Finset.univ.erase r, lam r' * (M * δ ^ 2) := by
      apply Finset.sum_le_sum; intro r' _
      have := mul_le_mul_of_nonneg_left (hlo r') (hlam0 r'); linarith
    have h2 : ∑ r' ∈ Finset.univ.erase r, lam r' * (M * δ ^ 2) ≤ ∑ r', lam r' * (M * δ ^ 2) :=
      Finset.sum_le_sum_of_subset_of_nonneg (Finset.erase_subset _ _)
        (fun r' _ _ => mul_nonneg (hlam0 r') (mul_nonneg hM (sq_nonneg δ)))
    have h3 : ∑ r', lam r' * (M * δ ^ 2) ≤ Λ * (M * δ ^ 2) := by
      rw [← Finset.sum_mul]; exact mul_le_mul_of_nonneg_right hΛ (mul_nonneg hM (sq_nonneg δ))
    simp only [Finset.sum_neg_distrib] at h1
    linarith
  set B := Λ * M / lmin with hB
  have hB0 : 0 ≤ B := div_nonneg (mul_nonneg hΛ0 hM) hlmin.le
  have habs : ∀ r, |l r| ≤ B * δ ^ 2 := by
    intro r
    rw [abs_le]; constructor
    · have : M * δ ^ 2 ≤ B * δ ^ 2 := by
        apply mul_le_mul_of_nonneg_right _ (sq_nonneg δ)
        rw [hB, le_div_iff₀ hlmin]; nlinarith
      linarith [hlo r]
    · by_cases hp : l r ≤ 0
      · exact hp.trans (mul_nonneg hB0 (sq_nonneg δ))
      · push_neg at hp
        have : lmin * l r ≤ Λ * (M * δ ^ 2) := (mul_le_mul_of_nonneg_right (hlam r) hp.le).trans (hhi r)
        rw [hB, div_mul_eq_mul_div, le_div_iff₀ hlmin]; linarith
  -- injectivity: |Δ_v| ≤ Gn B δ² + δ / 2
  have hinj : ∀ v, |Δ v| ≤ Gn * (B * δ ^ 2) + δ / 2 := by
    intro v
    have e : Δ v = ∑ r, G v r * l r - ∑ w, ((∑ r, G v r * L r w) - (if v = w then 1 else 0)) * Δ w := by
      simp only [hl, Finset.mul_sum, sub_mul, Finset.sum_sub_distrib, ite_mul, one_mul, zero_mul,
        Finset.sum_ite_eq, Finset.mem_univ, if_true]
      rw [Finset.sum_comm]
      simp only [Finset.sum_mul]
      have : ∀ w, ∑ r, G v r * (L r w * Δ w) = ∑ r, G v r * L r w * Δ w := fun w => by
        congr 1; ext r; ring
      simp only [this]; ring
    rw [e]
    have hδ0 : 0 ≤ δ := (abs_nonneg _).trans (hδ v)
    calc |∑ r, G v r * l r - ∑ w, ((∑ r, G v r * L r w) - (if v = w then 1 else 0)) * Δ w|
        ≤ |∑ r, G v r * l r| + |∑ w, ((∑ r, G v r * L r w) - (if v = w then 1 else 0)) * Δ w| := abs_sub _ _
      _ ≤ ∑ r, |G v r| * (B * δ ^ 2) + ∑ w, |(∑ r, G v r * L r w) - (if v = w then 1 else 0)| * δ := by
          gcongr
          · refine (Finset.abs_sum_le_sum_abs _ _).trans (Finset.sum_le_sum fun r _ => ?_)
            rw [abs_mul]; exact mul_le_mul_of_nonneg_left (habs r) (abs_nonneg _)
          · refine (Finset.abs_sum_le_sum_abs _ _).trans (Finset.sum_le_sum fun w _ => ?_)
            rw [abs_mul]; exact mul_le_mul_of_nonneg_left (hδ w) (abs_nonneg _)
      _ = (∑ r, |G v r|) * (B * δ ^ 2) + (∑ w, |(∑ r, G v r * L r w) - (if v = w then 1 else 0)|) * δ := by
          rw [Finset.sum_mul, Finset.sum_mul]
      _ ≤ Gn * (B * δ ^ 2) + 1 / 2 * δ := by
          gcongr
          · exact hGn v
          · exact hG v
      _ = Gn * (B * δ ^ 2) + δ / 2 := by ring
  obtain ⟨v0, hv0⟩ := hδmax
  have hδpos : 0 < δ := lt_of_lt_of_le (abs_pos.2 hneg.ne) (hδ iS)
  have h1 := hinj v0
  rw [hv0] at h1
  -- δ ≤ Gn B δ² + δ/2 ⇒ 1 ≤ 2 Gn B δ, against hsmall
  have h2 : 1 ≤ 2 * Gn * B * δ := by nlinarith
  have h3 : 2 * Gn * B * δ < 1 := by
    rw [hB]
    have : 2 * Gn * (Λ * M / lmin) * δ = (2 * Gn * Λ * M * δ) / lmin := by ring
    rw [this, div_lt_one hlmin]; exact hsmall
  linarith

/-! ## Expanding a row around the record

Record: side normal `N` of square `i`, offset `A = P* - c_i*` of the point from the centre of `i`, and `q = R_j* p`.
Perturbation: centres move by `dC = Δc_j - Δc_i`; angles by `δ`, with `w = sin δ`, `u = cos δ - 1` (`|u| ≤ w²`).
Then the normal is `(1 + u_i) N + w_i J N` and the offset `A + dC + u_j q + w_j J q` (`J` = quarter turn), and
the side value is its record value plus a linear part plus `O(δ²)`. -/

/-- The linear part of a side value. -/
def sideLin (Nx Ny Ax Ay qx qy dCx dCy wi wj : ℝ) : ℝ :=
  Nx * dCx + Ny * dCy + wi * (-Ny * Ax + Nx * Ay) + wj * (Nx * -qy + Ny * qx)

lemma side_expand {Nx Ny Ax Ay qx qy dCx dCy ui wi uj wj δ : ℝ} (hδ1 : δ ≤ 1)
    (hN : |Nx| ≤ 1 ∧ |Ny| ≤ 1) (hA : |Ax| ≤ 2 ∧ |Ay| ≤ 2) (hq : |qx| + |qy| ≤ 2)
    (hdC : |dCx| ≤ 2 * δ ∧ |dCy| ≤ 2 * δ) (hwi : |wi| ≤ δ) (hwj : |wj| ≤ δ) (hui : |ui| ≤ δ ^ 2)
    (huj : |uj| ≤ δ ^ 2) :
    |(((1 + ui) * Nx - wi * Ny) * (Ax + dCx + uj * qx - wj * qy) +
        ((1 + ui) * Ny + wi * Nx) * (Ay + dCy + uj * qy + wj * qx)) - (Nx * Ax + Ny * Ay) -
        sideLin Nx Ny Ax Ay qx qy dCx dCy wi wj| ≤ 30 * δ ^ 2 := by
  have hδ0 : 0 ≤ δ := (abs_nonneg _).trans hwi
  set Vx := Ax + dCx + uj * qx - wj * qy
  set Vy := Ay + dCy + uj * qy + wj * qx
  have e : (((1 + ui) * Nx - wi * Ny) * Vx + ((1 + ui) * Ny + wi * Nx) * Vy) - (Nx * Ax + Ny * Ay) -
      sideLin Nx Ny Ax Ay qx qy dCx dCy wi wj =
      uj * (Nx * qx + Ny * qy) + ui * (Nx * Vx + Ny * Vy) + wi * (-Ny * (Vx - Ax) + Nx * (Vy - Ay)) := by
    simp only [sideLin, Vx, Vy]; ring
  rw [e]
  have hNq : |Nx * qx + Ny * qy| ≤ 2 := by
    calc |Nx * qx + Ny * qy| ≤ |Nx| * |qx| + |Ny| * |qy| := by
          rw [← abs_mul, ← abs_mul]; exact abs_add_le _ _
      _ ≤ 1 * |qx| + 1 * |qy| := by gcongr; exact hN.1; exact hN.2
      _ ≤ 2 := by linarith
  have hqx : |qx| ≤ 2 := by linarith [abs_nonneg qy]
  have hqy : |qy| ≤ 2 := by linarith [abs_nonneg qx]
  have hδ2 : δ ^ 2 ≤ δ := by nlinarith
  have hujq : |uj * qx| ≤ 2 * δ ^ 2 ∧ |uj * qy| ≤ 2 * δ ^ 2 := by
    rw [abs_mul, abs_mul]; constructor <;> nlinarith [abs_nonneg uj, abs_nonneg qx, abs_nonneg qy]
  have hwjq : |wj * qx| ≤ 2 * δ ∧ |wj * qy| ≤ 2 * δ := by
    rw [abs_mul, abs_mul]; constructor <;> nlinarith [abs_nonneg wj, abs_nonneg qx, abs_nonneg qy]
  have hVx : |Vx - Ax| ≤ 2 * δ + 2 * δ ^ 2 + 2 * δ := by
    have : Vx - Ax = dCx + uj * qx - wj * qy := by simp only [Vx]; ring
    rw [this]
    calc |dCx + uj * qx - wj * qy| ≤ |dCx| + |uj * qx| + |wj * qy| := by
          have := abs_add_le (dCx + uj * qx) (-(wj * qy)); rw [abs_neg] at this
          have := abs_add_le dCx (uj * qx); rw [sub_eq_add_neg]; linarith
      _ ≤ 2 * δ + 2 * δ ^ 2 + 2 * δ := by linarith [hdC.1, hujq.1, hwjq.2]
  have hVy : |Vy - Ay| ≤ 2 * δ + 2 * δ ^ 2 + 2 * δ := by
    have : Vy - Ay = dCy + uj * qy + wj * qx := by simp only [Vy]; ring
    rw [this]
    calc |dCy + uj * qy + wj * qx| ≤ |dCy| + |uj * qy| + |wj * qx| := by
          have := abs_add_le (dCy + uj * qy) (wj * qx)
          have := abs_add_le dCy (uj * qy); linarith
      _ ≤ 2 * δ + 2 * δ ^ 2 + 2 * δ := by linarith [hdC.2, hujq.2, hwjq.1]
  have hNV : |Nx * Vx + Ny * Vy| ≤ 16 := by
    have h1 : |Vx| ≤ 8 := by
      have := abs_sub_abs_le_abs_sub Vx Ax; nlinarith [hA.1]
    have h2 : |Vy| ≤ 8 := by
      have := abs_sub_abs_le_abs_sub Vy Ay; nlinarith [hA.2]
    calc |Nx * Vx + Ny * Vy| ≤ |Nx| * |Vx| + |Ny| * |Vy| := by
          rw [← abs_mul, ← abs_mul]; exact abs_add_le _ _
      _ ≤ 1 * |Vx| + 1 * |Vy| := by gcongr; exact hN.1; exact hN.2
      _ ≤ 16 := by linarith
  have hJV : |-Ny * (Vx - Ax) + Nx * (Vy - Ay)| ≤ 12 * δ := by
    calc |-Ny * (Vx - Ax) + Nx * (Vy - Ay)| ≤ |Ny| * |Vx - Ax| + |Nx| * |Vy - Ay| := by
          have := abs_add_le (-Ny * (Vx - Ax)) (Nx * (Vy - Ay))
          rw [abs_mul, abs_mul, abs_neg] at this; exact this
      _ ≤ 1 * (2 * δ + 2 * δ ^ 2 + 2 * δ) + 1 * (2 * δ + 2 * δ ^ 2 + 2 * δ) := by
          gcongr; exact hN.2; exact hN.1
      _ ≤ 12 * δ := by nlinarith
  calc |uj * (Nx * qx + Ny * qy) + ui * (Nx * Vx + Ny * Vy) + wi * (-Ny * (Vx - Ax) + Nx * (Vy - Ay))|
      ≤ |uj| * |Nx * qx + Ny * qy| + |ui| * |Nx * Vx + Ny * Vy| + |wi| * |-Ny * (Vx - Ax) + Nx * (Vy - Ay)| := by
        rw [← abs_mul, ← abs_mul, ← abs_mul]
        have := abs_add_le (uj * (Nx * qx + Ny * qy) + ui * (Nx * Vx + Ny * Vy)) (wi * (-Ny * (Vx - Ax) + Nx * (Vy - Ay)))
        have := abs_add_le (uj * (Nx * qx + Ny * qy)) (ui * (Nx * Vx + Ny * Vy)); linarith
    _ ≤ δ ^ 2 * 2 + δ ^ 2 * 16 + δ * (12 * δ) := by
        gcongr
    _ = 30 * δ ^ 2 := by ring

lemma sideLin_bound {Nx Ny Ax Ay qx qy dCx dCy wi wj δ : ℝ}
    (hN : |Nx| ≤ 1 ∧ |Ny| ≤ 1) (hA : |Ax| ≤ 2 ∧ |Ay| ≤ 2) (hq : |qx| + |qy| ≤ 2)
    (hdC : |dCx| ≤ 2 * δ ∧ |dCy| ≤ 2 * δ) (hwi : |wi| ≤ δ) (hwj : |wj| ≤ δ) :
    |sideLin Nx Ny Ax Ay qx qy dCx dCy wi wj| ≤ 12 * δ := by
  have hδ0 : 0 ≤ δ := (abs_nonneg _).trans hwi
  have b1 : |Nx * dCx + Ny * dCy| ≤ 4 * δ := by
    calc |Nx * dCx + Ny * dCy| ≤ |Nx| * |dCx| + |Ny| * |dCy| := by
          rw [← abs_mul, ← abs_mul]; exact abs_add_le _ _
      _ ≤ 1 * (2 * δ) + 1 * (2 * δ) := by gcongr; exact hN.1; exact hdC.1; exact hN.2; exact hdC.2
      _ = 4 * δ := by ring
  have b2 : |-Ny * Ax + Nx * Ay| ≤ 4 := by
    calc |-Ny * Ax + Nx * Ay| ≤ |Ny| * |Ax| + |Nx| * |Ay| := by
          have := abs_add_le (-Ny * Ax) (Nx * Ay); rw [abs_mul, abs_mul, abs_neg] at this; exact this
      _ ≤ 1 * 2 + 1 * 2 := by gcongr; exact hN.2; exact hA.1; exact hN.1; exact hA.2
      _ = 4 := by ring
  have b3 : |Nx * -qy + Ny * qx| ≤ 2 := by
    calc |Nx * -qy + Ny * qx| ≤ |Nx| * |qy| + |Ny| * |qx| := by
          have := abs_add_le (Nx * -qy) (Ny * qx); rw [abs_mul, abs_mul, abs_neg] at this; exact this
      _ ≤ 1 * |qy| + 1 * |qx| := by gcongr; exact hN.1; exact hN.2
      _ ≤ 2 := by linarith
  simp only [sideLin]
  calc |Nx * dCx + Ny * dCy + wi * (-Ny * Ax + Nx * Ay) + wj * (Nx * -qy + Ny * qx)|
      ≤ |Nx * dCx + Ny * dCy| + |wi| * |-Ny * Ax + Nx * Ay| + |wj| * |Nx * -qy + Ny * qx| := by
        rw [← abs_mul, ← abs_mul]
        have := abs_add_le (Nx * dCx + Ny * dCy + wi * (-Ny * Ax + Nx * Ay)) (wj * (Nx * -qy + Ny * qx))
        have := abs_add_le (Nx * dCx + Ny * dCy) (wi * (-Ny * Ax + Nx * Ay)); linarith
    _ ≤ 4 * δ + δ * 4 + δ * 2 := by gcongr
    _ ≤ 12 * δ := by linarith

/-- Wall rows: the coordinate `C + (1 + u) q₁ - w q₂` of a corner, expanded. -/
lemma wall_expand {C dC q1 q2 u w δ : ℝ} (hq : |q1| ≤ 2) (hu : |u| ≤ δ ^ 2) :
    |(C + dC + ((1 + u) * q1 - w * q2)) - (C + q1) - (dC - w * q2)| ≤ 30 * δ ^ 2 := by
  have : (C + dC + ((1 + u) * q1 - w * q2)) - (C + q1) - (dC - w * q2) = u * q1 := by ring
  rw [this, abs_mul]
  have := abs_nonneg q1
  nlinarith [abs_nonneg u, sq_nonneg δ]

/-! ## Angles: `w = sin δ`, `u = cos δ - 1` -/

lemma angle_facts {δ : ℝ} (h : |δ| ≤ 1) :
    |Real.sin δ| ≤ |δ| ∧ |Real.cos δ - 1| ≤ Real.sin δ ^ 2 := by
  refine ⟨Real.abs_sin_le_abs, ?_⟩
  have hpi : 1 ≤ π / 2 := by linarith [Real.pi_gt_three]
  have hc0 : 0 ≤ Real.cos δ := Real.cos_nonneg_of_neg_pi_div_two_le_of_le
    (by linarith [neg_abs_le δ]) (by linarith [le_abs_self δ])
  have hc1 := Real.cos_le_one δ
  have hsc := Real.sin_sq_add_cos_sq δ
  rw [abs_of_nonpos (by linarith)]
  nlinarith

/-! ## A point of square `j` is outside the open square `i` -/

lemma interior_unitSq_eq_image (c : ℝ × ℝ) (θ : ℝ) :
    interior (unitSq c θ) = (fun p => c + rot θ p) '' (Ioo (-1/2) (1/2) ×ˢ Ioo (-1/2) (1/2)) := by
  rw [unitSq, ← interior_Icc, ← interior_prod_eq]
  exact ((place c θ).image_interior _).symm

lemma unitSq_subset_closure_interior (c : ℝ × ℝ) (θ : ℝ) : unitSq c θ ⊆ closure (interior (unitSq c θ)) := by
  rw [interior_unitSq_eq_image]
  have e : (fun p => c + rot θ p) = place c θ := rfl
  rw [e, ← (place c θ).image_closure, closure_prod_eq, closure_Ioo (by norm_num)]
  exact subset_of_eq rfl

/-- The value of side `k` of square `(xi, yi, ci, si)` at the point `P`. -/
def sideVal (xi yi ci si : ℝ) (k : Fin 4) (Px Py : ℝ) : ℝ :=
  (nrm ci si k).1 * (Px - xi) + (nrm ci si k).2 * (Py - yi)

/-- **Relaxation.**  A point of closed square `j` lies outside the open square `i` (disjoint interiors); if three
side values of `i` there are `< 1/2`, the fourth is `≥ 1/2`. -/
lemma sideVal_ge_of_disjoint {xi yi ci si θi xj yj cj sj θj a b : ℝ} (hci : Real.cos θi = ci)
    (hsi : Real.sin θi = si) (hcj : Real.cos θj = cj) (hsj : Real.sin θj = sj)
    (hd : Disjoint (interior (unitSq (xi, yi) θi)) (interior (unitSq (xj, yj) θj)))
    (ha : |a| ≤ 1 / 2) (hb : |b| ≤ 1 / 2) (k : Fin 4)
    (hother : ∀ k', k' ≠ k → sideVal xi yi ci si k' (xj + cj * a - sj * b) (yj + sj * a + cj * b) < 1 / 2) :
    1 / 2 ≤ sideVal xi yi ci si k (xj + cj * a - sj * b) (yj + sj * a + cj * b) := by
  set P : ℝ × ℝ := (xj + cj * a - sj * b, yj + sj * a + cj * b)
  have hP : P ∈ unitSq (xj, yj) θj := by
    refine ⟨(a, b), ⟨⟨?_, ?_⟩, ?_, ?_⟩, ?_⟩
    · linarith [neg_abs_le a]
    · linarith [le_abs_self a]
    · linarith [neg_abs_le b]
    · linarith [le_abs_self b]
    · simp only [rot, hcj, hsj, P, Prod.mk_add_mk]; ext <;> ring
  have hPi : P ∉ interior (unitSq (xi, yi) θi) := by
    intro h
    exact Set.disjoint_left.1 (hd.closure_right isOpen_interior) h (unitSq_subset_closure_interior _ _ hP)
  rw [interior_unitSq] at hPi
  simp only [mem_setOf_eq, hci, hsi, not_and_or, not_lt] at hPi
  by_contra hk
  push_neg at hk
  have hall : ∀ k', sideVal xi yi ci si k' P.1 P.2 < 1 / 2 := by
    intro k'
    by_cases h : k' = k
    · rw [h]; exact hk
    · exact hother k' h
  have h0 := hall 0
  have h1 := hall 1
  have h2 := hall 2
  have h3 := hall 3
  simp only [sideVal, nrm, P] at h0 h1 h2 h3 hPi
  rcases hPi with h | h <;> rw [le_abs] at h <;> rcases h with h | h <;> linarith

end UnitSquarePacking
