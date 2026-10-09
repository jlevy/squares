import Sqpack.LocalMin

/-!
# Local minima from rows (first-order rigidity with positive contact forces)

Rows: `pt j a b i k` = the point `(a, b)` (local coordinates, `|a|, |b| ≤ 1/2`) of square `j` lies on or beyond the
line of side `k` of square `i`; `wall j a b w` = corner `(a, b)` of `j` inside wall `w` (left, right, bottom, top).
Variables: `some (i, 0|1|2)` = `x_i, y_i, w_i = sin δ_i`; `none` = the side.

`isLocalMin_of_rows`: if every row is tight at the record (with the bounds `RowOK`), the multipliers balance
(`Σ λ_r L_r = e_S`, `λ_r ≥ λ_min > 0`) and `G` is an approximate left inverse of `L`, the record is a local minimum.
-/

namespace UnitSquarePacking.LM

open Real

inductive Row (n : ℕ)
  | pt (j : Fin n) (a b : ℚ) (i : Fin n) (k : Fin 4)
  | wall (j : Fin n) (a b : ℚ) (w : Fin 4)

/-- A configuration: centres, `(cos, sin)` of the angles, side. -/
structure Cfg (n : ℕ) where
  X : Fin n → ℝ
  Y : Fin n → ℝ
  C : Fin n → ℝ
  S : Fin n → ℝ
  side : ℝ

noncomputable section

variable {n : ℕ}

def qx (K : Cfg n) (j : Fin n) (a b : ℝ) : ℝ := K.C j * a - K.S j * b
def qy (K : Cfg n) (j : Fin n) (a b : ℝ) : ℝ := K.S j * a + K.C j * b

/-- The value of a row (`≥ 0` for a valid packing near the record). -/
def hval (K : Cfg n) : Row n → ℝ
  | .pt j a b i k => sideVal (K.X i) (K.Y i) (K.C i) (K.S i) k (K.X j + qx K j a b) (K.Y j + qy K j a b) - 1 / 2
  | .wall j a b w => ![K.X j + qx K j a b, K.side - (K.X j + qx K j a b), K.Y j + qy K j a b,
      K.side - (K.Y j + qy K j a b)] w

abbrev Var (n : ℕ) := Option (Fin n × Fin 3)

/-- Coefficients of a point row on the variables of square `j` (x, y, w). -/
def ptJ (K : Cfg n) (j : Fin n) (a b : ℝ) (i : Fin n) (k : Fin 4) : Fin 3 → ℝ :=
  ![(nrm (K.C i) (K.S i) k).1, (nrm (K.C i) (K.S i) k).2,
    (nrm (K.C i) (K.S i) k).1 * -qy K j a b + (nrm (K.C i) (K.S i) k).2 * qx K j a b]

/-- Coefficients of a point row on the variables of square `i` (x, y, w). -/
def ptI (K : Cfg n) (j : Fin n) (a b : ℝ) (i : Fin n) (k : Fin 4) : Fin 3 → ℝ :=
  ![-(nrm (K.C i) (K.S i) k).1, -(nrm (K.C i) (K.S i) k).2,
    -(nrm (K.C i) (K.S i) k).2 * (K.X j + qx K j a b - K.X i) +
      (nrm (K.C i) (K.S i) k).1 * (K.Y j + qy K j a b - K.Y i)]

/-- Coefficients of a wall row on the variables of square `j`. -/
def wallJ (K : Cfg n) (j : Fin n) (a b : ℝ) (w : Fin 4) : Fin 3 → ℝ :=
  ![![1, -1, 0, 0] w, ![0, 0, 1, -1] w, ![-qy K j a b, qy K j a b, qx K j a b, -qx K j a b] w]

/-- `v ↦ g c` on the variables `(l, c)` of square `l = j`, else `0`. -/
def onSq (j : Fin n) (g : Fin 3 → ℝ) : Var n → ℝ
  | none => 0
  | some (l, c) => if l = j then g c else 0

/-- The linear part of a row at the record `K`. -/
def rowL (K : Cfg n) : Row n → Var n → ℝ
  | .pt j a b i k, v => onSq j (ptJ K j a b i k) v + onSq i (ptI K j a b i k) v
  | .wall j a b w, v => (match v with | none => ![0, 1, 0, 1] w | some _ => 0) + onSq j (wallJ K j a b w) v

/-- Row conditions at the record: local coordinates in the square, tight, offsets bounded, and (for points) the
other three side values at most `1/2 - μ`. -/
def RowOK (K : Cfg n) (μ : ℝ) : Row n → Prop
  | .pt j a b i k => |(a : ℝ)| ≤ 1 / 2 ∧ |(b : ℝ)| ≤ 1 / 2 ∧ i ≠ j ∧ hval K (.pt j a b i k) = 0 ∧
      |K.X j + qx K j a b - K.X i| ≤ 2 ∧ |K.Y j + qy K j a b - K.Y i| ≤ 2 ∧
      ∀ k', k' ≠ k → sideVal (K.X i) (K.Y i) (K.C i) (K.S i) k' (K.X j + qx K j a b) (K.Y j + qy K j a b) ≤ 1 / 2 - μ
  | .wall j a b w => |(a : ℝ)| ≤ 1 / 2 ∧ |(b : ℝ)| ≤ 1 / 2 ∧ hval K (.wall j a b w) = 0

/-! ## Sums over the variables -/

lemma sum_onSq (j : Fin n) (g : Fin 3 → ℝ) (Δ : Var n → ℝ) :
    ∑ v : Var n, onSq j g v * Δ v = g 0 * Δ (some (j, 0)) + g 1 * Δ (some (j, 1)) + g 2 * Δ (some (j, 2)) := by
  rw [Fintype.sum_option]
  simp only [onSq, zero_mul, zero_add, Fintype.sum_prod_type, ite_mul]
  rw [Finset.sum_eq_single j]
  · simp [Fin.sum_univ_three]
  · intro l _ hl; simp [hl]
  · simp

lemma sum_rowL_pt (K : Cfg n) (j : Fin n) (a b : ℚ) (i : Fin n) (k : Fin 4) (Δ : Var n → ℝ) :
    ∑ v, rowL K (.pt j a b i k) v * Δ v =
      sideLin (nrm (K.C i) (K.S i) k).1 (nrm (K.C i) (K.S i) k).2 (K.X j + qx K j a b - K.X i)
        (K.Y j + qy K j a b - K.Y i) (qx K j a b) (qy K j a b)
        (Δ (some (j, 0)) - Δ (some (i, 0))) (Δ (some (j, 1)) - Δ (some (i, 1))) (Δ (some (i, 2)))
        (Δ (some (j, 2))) := by
  simp only [rowL, add_mul, Finset.sum_add_distrib, sum_onSq]
  simp [ptJ, ptI, sideLin]; ring

lemma sum_rowL_wall (K : Cfg n) (j : Fin n) (a b : ℚ) (w : Fin 4) (Δ : Var n → ℝ) :
    ∑ v, rowL K (.wall j a b w) v * Δ v =
      ![0, 1, 0, 1] w * Δ none + ![1, -1, 0, 0] w * Δ (some (j, 0)) + ![0, 0, 1, -1] w * Δ (some (j, 1)) +
        ![-qy K j a b, qy K j a b, qx K j a b, -qx K j a b] w * Δ (some (j, 2)) := by
  simp only [rowL, add_mul, Finset.sum_add_distrib, sum_onSq]
  rw [Fintype.sum_option]
  simp [wallJ]; ring

/-! ## A competitor as a perturbation of the record -/

/-- Competitor `K'` = record `K` moved by `dx, dy`, rotated by angles with `w = sin`, `u = cos - 1`. -/
structure Pert (K K' : Cfg n) (Δ : Var n → ℝ) (u : Fin n → ℝ) : Prop where
  hX : ∀ i, K'.X i = K.X i + Δ (some (i, 0))
  hY : ∀ i, K'.Y i = K.Y i + Δ (some (i, 1))
  hC : ∀ i, K'.C i = K.C i * (1 + u i) - K.S i * Δ (some (i, 2))
  hS : ∀ i, K'.S i = K.S i * (1 + u i) + K.C i * Δ (some (i, 2))
  hside : K'.side = K.side + Δ none

lemma nrm_pert (c s u w : ℝ) (k : Fin 4) :
    nrm (c * (1 + u) - s * w) (s * (1 + u) + c * w) k =
      ((1 + u) * (nrm c s k).1 - w * (nrm c s k).2, (1 + u) * (nrm c s k).2 + w * (nrm c s k).1) := by
  fin_cases k <;> simp [nrm] <;> constructor <;> ring

lemma abs_le_one_of_sq {c s : ℝ} (h : c ^ 2 + s ^ 2 = 1) : |c| ≤ 1 ∧ |s| ≤ 1 := by
  constructor <;> rw [abs_le] <;> constructor <;> nlinarith [sq_nonneg c, sq_nonneg s]

lemma nrm_abs_le {c s : ℝ} (h : c ^ 2 + s ^ 2 = 1) (k : Fin 4) : |(nrm c s k).1| ≤ 1 ∧ |(nrm c s k).2| ≤ 1 := by
  obtain ⟨h1, h2⟩ := abs_le_one_of_sq h
  fin_cases k <;> simp [nrm, abs_neg, h1, h2]

lemma q_abs_le {K : Cfg n} {j : Fin n} {a b : ℝ} (hu : K.C j ^ 2 + K.S j ^ 2 = 1) (ha : |a| ≤ 1 / 2)
    (hb : |b| ≤ 1 / 2) : |qx K j a b| + |qy K j a b| ≤ 2 := by
  obtain ⟨h1, h2⟩ := abs_le_one_of_sq hu
  simp only [qx, qy]
  have e1 : |K.C j * a - K.S j * b| ≤ |K.C j| * |a| + |K.S j| * |b| := by
    rw [← abs_mul, ← abs_mul]; exact abs_sub _ _
  have e2 : |K.S j * a + K.C j * b| ≤ |K.S j| * |a| + |K.C j| * |b| := by
    rw [← abs_mul, ← abs_mul]; exact abs_add_le _ _
  have : |K.C j| * |a| ≤ 1 / 2 := by nlinarith [abs_nonneg a, abs_nonneg (K.C j)]
  have : |K.S j| * |b| ≤ 1 / 2 := by nlinarith [abs_nonneg b, abs_nonneg (K.S j)]
  have : |K.S j| * |a| ≤ 1 / 2 := by nlinarith [abs_nonneg a, abs_nonneg (K.S j)]
  have : |K.C j| * |b| ≤ 1 / 2 := by nlinarith [abs_nonneg b, abs_nonneg (K.C j)]
  linarith

/-- The side value of the competitor at its point, as the record's plus a linear part plus `O(δ²)`. -/
lemma sideVal_pert {K K' : Cfg n} {Δ : Var n → ℝ} {u : Fin n → ℝ} (hp : Pert K K' Δ u) {δ : ℝ} (hδ1 : δ ≤ 1)
    (hΔ : ∀ v, |Δ v| ≤ δ) (hu : ∀ i, |u i| ≤ δ ^ 2) (hunit : ∀ i, K.C i ^ 2 + K.S i ^ 2 = 1)
    {j i : Fin n} {a b : ℚ} (k : Fin 4) (ha : |(a : ℝ)| ≤ 1 / 2) (hb : |(b : ℝ)| ≤ 1 / 2)
    (hAx : |K.X j + qx K j a b - K.X i| ≤ 2) (hAy : |K.Y j + qy K j a b - K.Y i| ≤ 2) :
    |sideVal (K'.X i) (K'.Y i) (K'.C i) (K'.S i) k (K'.X j + qx K' j a b) (K'.Y j + qy K' j a b) -
        sideVal (K.X i) (K.Y i) (K.C i) (K.S i) k (K.X j + qx K j a b) (K.Y j + qy K j a b) -
        sideLin (nrm (K.C i) (K.S i) k).1 (nrm (K.C i) (K.S i) k).2 (K.X j + qx K j a b - K.X i)
          (K.Y j + qy K j a b - K.Y i) (qx K j a b) (qy K j a b)
          (Δ (some (j, 0)) - Δ (some (i, 0))) (Δ (some (j, 1)) - Δ (some (i, 1))) (Δ (some (i, 2)))
          (Δ (some (j, 2)))| ≤ 30 * δ ^ 2 := by
  have hδ0 : 0 ≤ δ := (abs_nonneg _).trans (hΔ none)
  have key := side_expand (Nx := (nrm (K.C i) (K.S i) k).1) (Ny := (nrm (K.C i) (K.S i) k).2)
    (Ax := K.X j + qx K j a b - K.X i) (Ay := K.Y j + qy K j a b - K.Y i) (qx := qx K j a b) (qy := qy K j a b)
    (dCx := Δ (some (j, 0)) - Δ (some (i, 0))) (dCy := Δ (some (j, 1)) - Δ (some (i, 1)))
    (ui := u i) (wi := Δ (some (i, 2))) (uj := u j) (wj := Δ (some (j, 2))) hδ1 (nrm_abs_le (hunit i) k)
    ⟨hAx, hAy⟩ (q_abs_le (hunit j) ha hb)
    ⟨by have := abs_sub (Δ (some (j, 0))) (Δ (some (i, 0))); linarith [hΔ (some (j, 0)), hΔ (some (i, 0))],
     by have := abs_sub (Δ (some (j, 1))) (Δ (some (i, 1))); linarith [hΔ (some (j, 1)), hΔ (some (i, 1))]⟩
    (hΔ _) (hΔ _) (hu i) (hu j)
  convert key using 2
  simp only [sideVal, hp.hX, hp.hY, hp.hC, hp.hS, nrm_pert, qx, qy]
  ring

/-! ## The theorem -/

theorem isLocalMin_of_rows {m : ℕ} (K : Cfg n) (θ : Fin n → ℝ) (hθc : ∀ i, Real.cos (θ i) = K.C i)
    (hθs : ∀ i, Real.sin (θ i) = K.S i) (hpack : IsPacking n K.side (fun i => (K.X i, K.Y i)) θ)
    (rows : Fin m → Row n) {μ : ℝ} (hμ : 0 < μ) (hrows : ∀ r, RowOK K μ (rows r))
    (lam : Fin m → ℝ) (G : Var n → Fin m → ℝ) {lmin Λ Gn : ℝ} (hlmin : 0 < lmin) (hlam : ∀ r, lmin ≤ lam r)
    (hΛ : ∑ r, lam r ≤ Λ)
    (hsum : ∀ v, ∑ r, lam r * rowL K (rows r) v = if v = none then 1 else 0)
    (hGn : ∀ v, ∑ r, |G v r| ≤ Gn)
    (hG : ∀ v, ∑ w, |(∑ r, G v r * rowL K (rows r) w) - (if v = w then 1 else 0)| ≤ 1 / 2) :
    IsLocalMinPacking n K.side (fun i => (K.X i, K.Y i)) θ := by
  have hunit : ∀ i, K.C i ^ 2 + K.S i ^ 2 = 1 := fun i => by
    rw [← hθc, ← hθs]; exact Real.cos_sq_add_sin_sq _
  set ε := min (1 / 2) (min (μ / 50) (lmin / (60 * (|Gn| + 1) * (|Λ| + 1)))) with hε
  have hpos : 0 < 60 * (|Gn| + 1) * (|Λ| + 1) := by positivity
  have hε0 : 0 < ε := lt_min (by norm_num) (lt_min (by linarith) (div_pos hlmin hpos))
  have hε1 : ε ≤ 1 / 2 := min_le_left _ _
  have hεμ : ε ≤ μ / 50 := (min_le_right _ _).trans (min_le_left _ _)
  have hεl : ε ≤ lmin / (60 * (|Gn| + 1) * (|Λ| + 1)) := (min_le_right _ _).trans (min_le_right _ _)
  refine ⟨hpack, ε, hε0, ?_⟩
  intro s c' θ' hP hnear
  by_contra hlt
  push_neg at hlt
  choose mm hmm using fun i => (hnear i).2.2
  set δa : Fin n → ℝ := fun i => θ' i - θ i - mm i * (π / 2) with hδa
  set s' := max s (K.side - ε / 2) with hs'
  have hs'lt : s' < K.side := max_lt hlt (by linarith)
  have hs'ge : K.side - ε / 2 ≤ s' := le_max_right _ _
  set θn : Fin n → ℝ := fun i => θ i + δa i with hθn
  have hsq : ∀ i, unitSq (c' i) (θ' i) = unitSq (c' i) (θn i) := fun i => by
    have : θ' i = θn i + (mm i : ℝ) * (π / 2) := by simp only [hθn, hδa]; ring
    rw [this, unitSq_add_int_mul]
  have hPn : IsPacking n s' c' θn := by
    have h1 := hP.mono (le_max_left s (K.side - ε / 2))
    refine ⟨fun i => hsq i ▸ h1.1 i, fun i j hij => ?_⟩
    have := h1.2 hij
    beta_reduce at this ⊢
    rwa [hsq i, hsq j] at this
  set K' : Cfg n := ⟨fun i => (c' i).1, fun i => (c' i).2, fun i => Real.cos (θn i), fun i => Real.sin (θn i), s'⟩
  set Δ : Var n → ℝ := fun v => match v with
    | none => s' - K.side
    | some (i, c) => ![(c' i).1 - K.X i, (c' i).2 - K.Y i, Real.sin (δa i)] c with hΔdef
  set u : Fin n → ℝ := fun i => Real.cos (δa i) - 1
  have hpert : Pert K K' Δ u := by
    refine ⟨fun i => ?_, fun i => ?_, fun i => ?_, fun i => ?_, ?_⟩
    · simp [K', Δ]
    · simp [K', Δ]
    · (simp only [K', Δ, u, hθn, Real.cos_add, hθc, hθs]; simp) <;> ring
    · (simp only [K', Δ, u, hθn, Real.sin_add, hθc, hθs]; simp) <;> ring
    · simp [K', Δ]
  have hne : (Finset.univ : Finset (Var n)).Nonempty := ⟨none, Finset.mem_univ _⟩
  set δ := Finset.univ.sup' hne (fun v => |Δ v|) with hδdef
  have hΔ : ∀ v, |Δ v| ≤ δ := fun v => Finset.le_sup' (fun v => |Δ v|) (Finset.mem_univ v)
  have hδmax : ∃ v, |Δ v| = δ := by
    obtain ⟨v, _, hv⟩ := Finset.exists_mem_eq_sup' hne (fun v => |Δ v|); exact ⟨v, hv.symm⟩
  have hδa : ∀ i, |δa i| < ε := fun i => hmm i
  have hδε : δ < ε := by
    rw [hδdef, Finset.sup'_lt_iff]
    intro v _
    rcases v with _ | ⟨i, c⟩
    · simp only [Δ]; rw [abs_lt]; constructor <;> linarith
    · fin_cases c
      · simpa [Δ] using (hnear i).1
      · simpa [Δ] using (hnear i).2.1
      · simp only [Δ]; simp
        exact (Real.abs_sin_le_abs).trans_lt (hδa i)
  have hδ0 : 0 ≤ δ := (abs_nonneg _).trans (hΔ none)
  have hδ1 : δ ≤ 1 := by linarith
  have hu : ∀ i, |u i| ≤ δ ^ 2 := fun i => by
    have h1 := (angle_facts (le_of_lt (lt_of_lt_of_le (hδa i) (by linarith)))).2
    have h2 : |Real.sin (δa i)| ≤ δ := by have := hΔ (some (i, 2)); simpa [Δ] using this
    have : Real.sin (δa i) ^ 2 ≤ δ ^ 2 := by
      rw [← sq_abs]; exact pow_le_pow_left₀ (abs_nonneg _) h2 2
    exact h1.trans this
  -- the rows
  have hrow : ∀ r, 0 ≤ hval K' (rows r) ∧ |hval K' (rows r) - ∑ v, rowL K (rows r) v * Δ v| ≤ 30 * δ ^ 2 := by
    intro r
    have hok := hrows r
    generalize rows r = row at hok ⊢
    rcases row with ⟨j, a, b, i, k⟩ | ⟨j, a, b, w⟩
    · obtain ⟨ha, hb, hij, htight, hAx, hAy, hmar⟩ := hok
      have hexp := sideVal_pert hpert hδ1 hΔ hu hunit k ha hb hAx hAy
      rw [sum_rowL_pt]
      simp only [hval] at htight ⊢
      refine ⟨?_, by convert hexp using 2; linarith⟩
      have hdC : ∀ c : Fin 3, |Δ (some (j, c)) - Δ (some (i, c))| ≤ 2 * δ := fun c => by
        have := abs_sub (Δ (some (j, c))) (Δ (some (i, c))); linarith [hΔ (some (j, c)), hΔ (some (i, c))]
      have hother : ∀ k', k' ≠ k → sideVal (K'.X i) (K'.Y i) (K'.C i) (K'.S i) k' (K'.X j + qx K' j a b)
          (K'.Y j + qy K' j a b) < 1 / 2 := by
        intro k' hk'
        have e := sideVal_pert hpert hδ1 hΔ hu hunit k' ha hb hAx hAy
        have lb := sideLin_bound (nrm_abs_le (hunit i) k') ⟨hAx, hAy⟩ (q_abs_le (hunit j) ha hb)
          ⟨hdC 0, hdC 1⟩ (hΔ (some (i, 2))) (hΔ (some (j, 2)))
        have hm := hmar k' hk'
        rw [abs_le] at e lb
        nlinarith
      have hge := sideVal_ge_of_disjoint (hci := rfl) (hsi := rfl) (hcj := rfl) (hsj := rfl)
        (hPn.2 hij) ha hb k (fun k' hk' => by
          have h := hother k' hk'; simp only [K', qx, qy] at h; convert h using 2 <;> ring)
      have : sideVal (K'.X i) (K'.Y i) (K'.C i) (K'.S i) k (K'.X j + qx K' j a b) (K'.Y j + qy K' j a b) =
          sideVal (c' i).1 (c' i).2 (Real.cos (θn i)) (Real.sin (θn i)) k
            ((c' j).1 + Real.cos (θn j) * a - Real.sin (θn j) * b) ((c' j).2 + Real.sin (θn j) * a + Real.cos (θn j) * b) := by
        simp only [K', qx, qy]; congr 1 <;> ring
      rw [this]; linarith
    · obtain ⟨ha, hb, htight⟩ := hok
      -- the corner is in the container
      have hmem : ((c' j).1 + (Real.cos (θn j) * a - Real.sin (θn j) * b),
          (c' j).2 + (Real.sin (θn j) * a + Real.cos (θn j) * b)) ∈ container s' := by
        apply hPn.1 j
        refine ⟨((a : ℝ), (b : ℝ)), ⟨⟨?_, ?_⟩, ?_, ?_⟩, ?_⟩
        · linarith [neg_abs_le (a : ℝ)]
        · linarith [le_abs_self (a : ℝ)]
        · linarith [neg_abs_le (b : ℝ)]
        · linarith [le_abs_self (b : ℝ)]
        · ext <;> simp [rot]
      simp only [container, Set.mem_prod, Set.mem_Icc] at hmem
      have hqx := q_abs_le (K := K) (j := j) (hunit j) ha hb
      have hux := hu j
      have hq1 : |qx K j a b| ≤ 2 := by linarith [abs_nonneg (qy K j a b)]
      have hq2 : |qy K j a b| ≤ 2 := by linarith [abs_nonneg (qx K j a b)]
      have hb1 : |u j * qx K j a b| ≤ 30 * δ ^ 2 := by
        rw [abs_mul]; nlinarith [abs_nonneg (u j), abs_nonneg (qx K j a b), sq_nonneg δ]
      have hb2 : |u j * qy K j a b| ≤ 30 * δ ^ 2 := by
        rw [abs_mul]; nlinarith [abs_nonneg (u j), abs_nonneg (qy K j a b), sq_nonneg δ]
      rw [sum_rowL_wall]
      simp only [hval] at htight ⊢
      have eX : K'.X j + qx K' j a b = K.X j + qx K j a b + Δ (some (j, 0)) + u j * qx K j a b -
          Δ (some (j, 2)) * qy K j a b := by
        simp only [qx, qy, hpert.hX, hpert.hC, hpert.hS]; ring
      have eY : K'.Y j + qy K' j a b = K.Y j + qy K j a b + Δ (some (j, 1)) + u j * qy K j a b +
          Δ (some (j, 2)) * qx K j a b := by
        simp only [qx, qy, hpert.hY, hpert.hC, hpert.hS]; ring
      have eS : K'.side = K.side + Δ none := hpert.hside
      fin_cases w
      · simp at htight ⊢
        refine ⟨by simpa [K', qx] using hmem.1.1, ?_⟩
        rw [eX, htight]; convert hb1 using 2; ring
      · simp at htight ⊢
        refine ⟨by have := hmem.1.2; simp [K', qx] at this ⊢; linarith, ?_⟩
        rw [eX, eS]; convert hb1 using 1; rw [← abs_neg]; congr 1; linarith
      · simp at htight ⊢
        refine ⟨by simpa [K', qy] using hmem.2.1, ?_⟩
        rw [eY, htight]; convert hb2 using 2; ring
      · simp at htight ⊢
        refine ⟨by have := hmem.2.2; simp [K', qy] at this ⊢; linarith, ?_⟩
        rw [eY, eS]; convert hb2 using 1; rw [← abs_neg]; congr 1; linarith
  have hsmall : 2 * Gn * Λ * 30 * δ < lmin := by
    have h1 : 2 * Gn * Λ * 30 * δ ≤ 60 * (|Gn| + 1) * (|Λ| + 1) * δ := by
      have : Gn * Λ ≤ (|Gn| + 1) * (|Λ| + 1) := by
        nlinarith [le_abs_self Gn, abs_nonneg Gn, abs_nonneg Λ, neg_abs_le Λ, abs_mul_abs_self Gn,
          abs_mul Gn Λ, le_abs_self (Gn * Λ)]
      nlinarith
    have h2 : 60 * (|Gn| + 1) * (|Λ| + 1) * δ < lmin := by
      have := lt_of_lt_of_le hδε hεl
      rw [lt_div_iff₀ hpos] at this; linarith
    linarith
  have := rigidity (fun r v => rowL K (rows r) v) lam G none hlmin hlam hΛ hsum hGn hG (by norm_num) Δ hΔ hδmax
    (fun r => hval K' (rows r)) (fun r => (hrow r).1) (fun r => (hrow r).2) hsmall
  simp only [Δ] at this
  linarith

end

end UnitSquarePacking.LM
