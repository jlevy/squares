import Sq19Lean.Milp.Expr

/-!
# Farkas leaf check

Rows `Σ_t e_t(θ) x_{col_t} ≤ b0(θ) + b1 L` with angle-dependent coefficients. For multipliers
`y ≥ 0` (sparse, row index and weight) the check builds `r_j = Σ_i y_i a_ij` and
`N = Σ_j xc_j r_j - Σ_i y_i b0_i` as expressions, encloses them on the angle box by Taylor forms,
and accepts when
  `min N - Σ_j h_j max |r_j| - (Σ_i y_i b1_i) Lmax > 0`
(`xc_j ± h_j` the column box, `Lmax` an upper bound of `L`). `leaf_sound`: then the rows cannot
all hold at any point of the box.
-/
namespace Sq19.Milp

structure Row where
  terms : List (ℕ × Ex)
  b0 : Ex
  b1 : ℚ

def Row.default : Row := ⟨[], .c 0, 0⟩

/-- The row holds at angles `θ`, column values `X` and side `L`. -/
def Row.Holds (r : Row) (θ : ℕ → ℝ) (X : ℕ → ℝ) (L : ℝ) : Prop :=
  (r.terms.map (fun t => t.2.real θ * X t.1)).sum ≤ r.b0.real θ + r.b1 * L

def rowAt (rows : List Row) (i : ℕ) : Row := rows.getD i Row.default

/-- Coefficient of column `j` in the combination. -/
def combCol (rows : List Row) (y : List (ℕ × ℚ)) (j : ℕ) : Ex :=
  Ex.sum (y.flatMap (fun p => ((rowAt rows p.1).terms.filter (fun t => t.1 = j)).map
    (fun t => Ex.mul (.c p.2) t.2)))

/-- The combined right-hand side `- Σ y_i b0_i`. -/
def combB0 (rows : List Row) (y : List (ℕ × ℚ)) : Ex :=
  Ex.sum (y.map (fun p => Ex.mul (.c (-p.2)) (rowAt rows p.1).b0))

def combB1 (rows : List Row) (y : List (ℕ × ℚ)) : ℚ :=
  (y.map (fun p => p.2 * (rowAt rows p.1).b1)).sum

/-- The leaf check. `col j` is the box of column `j < ncol`. -/
def leafCheck (T : Trig) (H : ℕ → ℚ) (rows : List Row) (ncol : ℕ) (col : ℕ → Iv) (Lmax : ℚ)
    (y : List (ℕ × ℚ)) : Bool :=
  let ok := y.all (fun p => decide (p.1 < rows.length ∧ 0 ≤ p.2 ∧ 0 ≤ (rowAt rows p.1).b1) &&
    (rowAt rows p.1).terms.all (fun t => decide (t.1 < ncol)))
  let N := Ex.add (Ex.sum ((List.range ncol).map (fun j => Ex.mul (.c (col j).mid) (combCol rows y j))))
    (combB0 rows y)
  let hs := ((List.range ncol).map (fun j => (col j).rad * ((combCol rows y j).tf T H |>.range H).mag)).sum
  ok && decide (0 < ((N.tf T H).range H).lo - hs - combB1 rows y * Lmax)

/-! ## Soundness -/

/-- Left side of a row. -/
noncomputable def rowLhs (r : Row) (θ X : ℕ → ℝ) : ℝ := (r.terms.map (fun t => t.2.real θ * X t.1)).sum

/-- Coefficient of column `j` in a row. -/
noncomputable def colCoef (r : Row) (θ : ℕ → ℝ) (j : ℕ) : ℝ :=
  ((r.terms.filter (fun t => t.1 = j)).map (fun t => t.2.real θ)).sum

theorem rowLhs_cols (θ X : ℕ → ℝ) (n : ℕ) (r : Row) (hc : ∀ t ∈ r.terms, t.1 < n) :
    rowLhs r θ X = ∑ j ∈ Finset.range n, colCoef r θ j * X j := by
  unfold rowLhs colCoef
  obtain ⟨ts, b0, b1⟩ := r
  simp only at hc ⊢
  induction ts with
  | nil => simp
  | cons t ts ih =>
    rw [List.map_cons, List.sum_cons, ih (fun u hu => hc u (List.mem_cons_of_mem _ hu))]
    have ht : t.1 ∈ Finset.range n := Finset.mem_range.mpr (hc t List.mem_cons_self)
    have e : ∀ j, ((t :: ts).filter (fun t => t.1 = j)).map (fun t => t.2.real θ) =
        (if t.1 = j then [t.2.real θ] else []) ++ (ts.filter (fun t => t.1 = j)).map (fun t => t.2.real θ) := by
      intro j; by_cases h : t.1 = j <;> simp [h]
    simp only [e, List.sum_append, add_mul, Finset.sum_add_distrib]
    congr 1
    rw [Finset.sum_eq_single t.1]
    · simp
    · intro b _ hb; simp [Ne.symm hb]
    · intro h; exact absurd ht h

theorem combCol_real (rows : List Row) (y : List (ℕ × ℚ)) (j : ℕ) (θ : ℕ → ℝ) :
    (combCol rows y j).real θ = (y.map (fun p => (p.2 : ℝ) * colCoef (rowAt rows p.1) θ j)).sum := by
  unfold combCol colCoef
  rw [Ex.real_sum]
  induction y with
  | nil => simp
  | cons p y ih =>
    rw [List.flatMap_cons, List.map_append, List.sum_append, ih, List.map_cons, List.sum_cons]
    congr 1
    rw [List.map_map, ← List.sum_map_mul_left]
    congr 1

theorem combB0_real (rows : List Row) (y : List (ℕ × ℚ)) (θ : ℕ → ℝ) :
    (combB0 rows y).real θ = -(y.map (fun p => (p.2 : ℝ) * (rowAt rows p.1).b0.real θ)).sum := by
  unfold combB0
  rw [Ex.real_sum]
  induction y with
  | nil => simp
  | cons p y ih =>
    rw [List.map_cons, List.map_cons, List.sum_cons, List.map_map] at *
    rw [List.map_cons, List.sum_cons, ih]
    simp only [Ex.real]; push_cast; ring

theorem weighted_rows (rows : List Row) (y : List (ℕ × ℚ)) (θ X : ℕ → ℝ) (L : ℝ)
    (hy : ∀ p ∈ y, 0 ≤ p.2) (hrows : ∀ p ∈ y, (rowAt rows p.1).Holds θ X L) :
    (y.map (fun p => (p.2 : ℝ) * rowLhs (rowAt rows p.1) θ X)).sum ≤
      (y.map (fun p => (p.2 : ℝ) * (rowAt rows p.1).b0.real θ)).sum + (combB1 rows y : ℝ) * L := by
  unfold combB1
  induction y with
  | nil => simp
  | cons p y ih =>
    simp only [List.map_cons, List.sum_cons]
    have h1 := ih (fun q hq => hy q (List.mem_cons_of_mem _ hq))
      (fun q hq => hrows q (List.mem_cons_of_mem _ hq))
    have hp : (0 : ℝ) ≤ p.2 := by exact_mod_cast hy p List.mem_cons_self
    have h2 := mul_le_mul_of_nonneg_left (hrows p List.mem_cons_self) hp
    change (p.2 : ℝ) * rowLhs (rowAt rows p.1) θ X ≤ _ at h2
    push_cast at h1 ⊢
    nlinarith

theorem regroup (rows : List Row) (y : List (ℕ × ℚ)) (θ X : ℕ → ℝ) (n : ℕ)
    (hc : ∀ p ∈ y, ∀ t ∈ (rowAt rows p.1).terms, t.1 < n) :
    (y.map (fun p => (p.2 : ℝ) * rowLhs (rowAt rows p.1) θ X)).sum =
      ∑ j ∈ Finset.range n, (combCol rows y j).real θ * X j := by
  simp only [combCol_real]
  induction y with
  | nil => simp
  | cons p y ih =>
    simp only [List.map_cons, List.sum_cons]
    rw [ih (fun q hq => hc q (List.mem_cons_of_mem _ hq)),
      rowLhs_cols θ X n _ (hc p List.mem_cons_self), Finset.mul_sum, ← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl; intro j _; ring

/-- **Leaf soundness.** If the check passes, no point of the box satisfies all the rows used. -/
theorem leaf_sound (T : Trig) (hT : T.Valid) (H : ℕ → ℚ) (rows : List Row) (ncol : ℕ)
    (col : ℕ → Iv) (Lmax : ℚ) (y : List (ℕ × ℚ))
    (hc : leafCheck T H rows ncol col Lmax y = true)
    (δ : ℕ → ℝ) (hδ : ∀ k, |δ k| ≤ H k) (X : ℕ → ℝ) (hX : ∀ j < ncol, Iv.mem (X j) (col j))
    (L : ℝ) (hL : L ≤ Lmax)
    (hrows : ∀ p ∈ y, (rowAt rows p.1).Holds (fun s => T.cen s + δ s) X L) : False := by
  set θ : ℕ → ℝ := fun s => T.cen s + δ s
  simp only [leafCheck, Bool.and_eq_true, List.all_eq_true, decide_eq_true_eq] at hc
  obtain ⟨hok, hpos⟩ := hc
  have hsum := weighted_rows rows y θ X L (fun p hp => (hok p hp).1.2.1) hrows
  rw [regroup rows y θ X ncol (fun p hp => (hok p hp).2)] at hsum
  have hB1 : (0 : ℝ) ≤ combB1 rows y := by
    unfold combB1
    exact_mod_cast List.sum_nonneg (fun x hx => by
      obtain ⟨p, hp, rfl⟩ := List.mem_map.mp hx
      exact mul_nonneg (hok p hp).1.2.1 (hok p hp).1.2.2)
  -- column part: r_j x_j ≥ r_j xc_j - h_j max|r_j|
  have hR : ∀ j ∈ Finset.range ncol, (combCol rows y j).real θ * (col j).mid -
      ((col j).rad : ℝ) * (((combCol rows y j).tf T H).range H).mag ≤
      (combCol rows y j).real θ * X j := by
    intro j hj
    have hXj := Iv.abs_sub_mid (hX j (Finset.mem_range.mp hj))
    have hm := Iv.abs_le_mag (TF.mem_range (Ex.tf_encl hT H (combCol rows y j)) δ hδ)
    have hb : |(combCol rows y j).real θ * (X j - (col j).mid)| ≤
        (((combCol rows y j).tf T H).range H).mag * (col j).rad := by
      rw [abs_mul]; exact mul_le_mul hm hXj (abs_nonneg _) ((abs_nonneg _).trans hm)
    have := neg_abs_le ((combCol rows y j).real θ * (X j - (col j).mid))
    have e : (combCol rows y j).real θ * X j = (combCol rows y j).real θ * (col j).mid +
        (combCol rows y j).real θ * (X j - (col j).mid) := by ring
    rw [e]; nlinarith
  have hRsum := Finset.sum_le_sum hR
  rw [Finset.sum_sub_distrib] at hRsum
  -- the enclosure of N
  have hN := (TF.mem_range (Ex.tf_encl hT H (Ex.add (Ex.sum ((List.range ncol).map
    (fun j => Ex.mul (.c (col j).mid) (combCol rows y j)))) (combB0 rows y))) δ hδ).1
  have eN : (Ex.add (Ex.sum ((List.range ncol).map
      (fun j => Ex.mul (.c (col j).mid) (combCol rows y j)))) (combB0 rows y)).real θ =
      ∑ j ∈ Finset.range ncol, (combCol rows y j).real θ * (col j).mid -
        (y.map (fun p => (p.2 : ℝ) * (rowAt rows p.1).b0.real θ)).sum := by
    simp only [Ex.real, Ex.real_sum, combB0_real, List.map_map]
    have : ((List.range ncol).map ((fun e => Ex.real θ e) ∘ fun j =>
        Ex.mul (.c (col j).mid) (combCol rows y j))).sum =
        ∑ j ∈ Finset.range ncol, (combCol rows y j).real θ * (col j).mid := by
      rw [← List.sum_toFinset _ (List.nodup_range), List.toFinset_range]
      apply Finset.sum_congr rfl; intro j _; simp [Ex.real, mul_comm]
    rw [this]; ring
  rw [eN] at hN
  have hhs : ((((List.range ncol).map (fun j => (col j).rad *
      ((combCol rows y j).tf T H |>.range H).mag)).sum : ℚ) : ℝ) =
      ∑ j ∈ Finset.range ncol, ((col j).rad : ℝ) * (((combCol rows y j).tf T H).range H).mag := by
    rw [← List.sum_toFinset _ (List.nodup_range), List.toFinset_range]; push_cast; rfl
  have hpos' : (0 : ℝ) < (((Ex.add (Ex.sum ((List.range ncol).map (fun j => Ex.mul (.c (col j).mid)
      (combCol rows y j)))) (combB0 rows y)).tf T H).range H).lo -
      ((List.range ncol).map (fun j => (col j).rad * ((combCol rows y j).tf T H |>.range H).mag)).sum -
      combB1 rows y * Lmax := by exact_mod_cast hpos
  rw [hhs] at hpos'
  have hLm : (combB1 rows y : ℝ) * L ≤ combB1 rows y * Lmax := mul_le_mul_of_nonneg_left hL hB1
  linarith

end Sq19.Milp
