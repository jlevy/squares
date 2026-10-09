import Sqpack.Chord

/-!
# The wall-strip chord lemma on a single line, strengthened to `h = (3√2 - 2)/2`

`Chord.lean` proves `wall_strip_le_three` for centres at height `≤ 1`, cutting with the line
`y = 9/10`.  Here the same argument is run with the line `y = y₀ := √2 - 1/2 ≈ 0.91421`, which
admits every centre height up to `h₁ := (3√2 - 2)/2 = 3√2/2 - 1 ≈ 1.12132`
(`notes/chord-lemma.md` §3, "Remark (how much room there is)";
`tasks/n12-chat-lemmas/README.md`, "h vs leaves").

With `P = |cos θ|`, `Q = |sin θ|`, `u = P + Q ∈ [1, √2]`, `PQ = (u² - 1)/2`, the chord on a line at
offset `e` from the centre has length `≥ 1` when `|e| ≤ D(u) := u/2 - PQ`
(`exists_unit_interval_subset_slab`).  A square in the box has centre height `c ≥ u/2`
(`half_height_le_centre`).  The two inequalities needed are

* downwards, `y₀ - c ≤ y₀ - u/2 ≤ D(u)`, i.e. `u²/2 - u + √2 - 1 = (u - √2)(u - (2 - √2))/2 ≤ 0`;
* upwards, `c - y₀ ≤ h₁ - y₀ = (√2 - 1)/2 ≤ D(u)`, i.e. `(u - √2)(1 - √2 - u)/2 ≥ 0`;

both tight at `u = √2` (the 45° square).  The counting step and the boundary semantics are
exactly those of `wall_strip_le_three`: `t ≤ 4` and closed disjointness (the four axis-parallel
squares in a row across `[0,4]` show this is needed).
-/

namespace SquarePacking

/-- The cut line `y₀ = √2 - 1/2`. -/
noncomputable def chordLineY : ℝ := Real.sqrt 2 - 1 / 2

/-- The strip height `h₁ = (3√2 - 2)/2` admitted by the single line `y = y₀`. -/
noncomputable def chordLineH : ℝ := (3 * Real.sqrt 2 - 2) / 2

/-- **The chord exists, on the line `y = √2 - 1/2`.**  A closed unit square inside `[0,t]^2` whose
centre is at height at most `(3√2 - 2)/2` meets the line `y = √2 - 1/2` in a segment of length at
least `1`. -/
lemma exists_chord_line {c : ℝ × ℝ} {θ t : ℝ} (hin : sq c θ 1 ⊆ box t)
    (hc : c.2 ≤ chordLineH) :
    ∃ x : ℝ, ∀ y ∈ Set.Icc x (x + 1), ((y, chordLineY) ∈ sq c θ 1) := by
  have hP : (0 : ℝ) ≤ |Real.cos θ| := abs_nonneg _
  have hQ : (0 : ℝ) ≤ |Real.sin θ| := abs_nonneg _
  have hPQ : |Real.cos θ| ^ 2 + |Real.sin θ| ^ 2 = 1 := by
    rw [sq_abs, sq_abs]; exact Real.cos_sq_add_sin_sq θ
  have hlow : (|Real.cos θ| + |Real.sin θ|) / 2 ≤ c.2 := half_height_le_centre hin
  have key : |chordLineY - c.2| ≤ (|Real.cos θ| + |Real.sin θ|) / 2
      - |Real.cos θ| * |Real.sin θ| := by
    simp only [chordLineH] at hc
    simp only [chordLineY]
    set P := |Real.cos θ|
    set Q := |Real.sin θ|
    set r := Real.sqrt 2 with hr
    have hr0 : 0 ≤ r := Real.sqrt_nonneg 2
    have hr2 : r ^ 2 = 2 := Real.sq_sqrt (by norm_num)
    have hr1 : 1 < r := by nlinarith
    have hr15 : r < 3 / 2 := by nlinarith
    have hu2 : (P + Q) ^ 2 ≤ 2 := by nlinarith [sq_nonneg (P - Q)]
    have hu1 : 1 ≤ P + Q := by nlinarith [mul_nonneg hP hQ]
    have hur : P + Q ≤ r := by nlinarith
    have hprod : 2 * (P * Q) = (P + Q) ^ 2 - 1 := by nlinarith
    -- downwards: `(√2 - u)(u - (2 - √2)) ≥ 0`
    have hdown : 0 ≤ (r - (P + Q)) * ((P + Q) - (2 - r)) :=
      mul_nonneg (by linarith) (by linarith)
    -- upwards: `(√2 - u)(√2 - 1 + u) ≥ 0`
    have hup : 0 ≤ (r - (P + Q)) * (r - 1 + (P + Q)) :=
      mul_nonneg (by linarith) (by linarith)
    rw [abs_le]
    constructor <;> nlinarith
  -- transport the slab bound through the two sign symmetries
  have hslab : ∃ x : ℝ,
      Set.Icc x (x + 1) ⊆ slab (Real.cos θ) (Real.sin θ) (chordLineY - c.2) := by
    rcases le_or_gt 0 (Real.cos θ) with hc0 | hc0 <;>
      rcases le_or_gt 0 (Real.sin θ) with hs0 | hs0
    · obtain ⟨x, hx⟩ := exists_unit_interval_subset_slab hP hQ hPQ key
      rw [abs_of_nonneg hc0, abs_of_nonneg hs0] at hx
      exact ⟨x, hx⟩
    · obtain ⟨x, hx⟩ := exists_unit_interval_subset_slab hP hQ hPQ (by rwa [abs_neg])
      rw [abs_of_nonneg hc0, abs_of_neg hs0] at hx
      exact ⟨x, by rwa [← slab_neg_snd]⟩
    · obtain ⟨x, hx⟩ := exists_unit_interval_subset_slab hP hQ hPQ (by rwa [abs_neg])
      rw [abs_of_neg hc0, abs_of_nonneg hs0] at hx
      exact ⟨x, by rwa [← slab_neg_snd, ← slab_neg_neg, neg_neg]⟩
    · obtain ⟨x, hx⟩ := exists_unit_interval_subset_slab hP hQ hPQ key
      rw [abs_of_neg hc0, abs_of_neg hs0] at hx
      exact ⟨x, by rwa [← slab_neg_neg]⟩
  obtain ⟨x, hx⟩ := hslab
  refine ⟨x + c.1, fun y hy => ?_⟩
  have hy' : y - c.1 ∈ Set.Icc x (x + 1) := ⟨by linarith [hy.1], by linarith [hy.2]⟩
  have hmem := (sq_mem_iff_slab c θ (y - c.1) (chordLineY - c.2)).mpr (hx hy')
  have e1 : c.1 + (y - c.1) = y := by ring
  have e2 : c.2 + (chordLineY - c.2) = chordLineY := by ring
  rwa [e1, e2] at hmem

/-- **The single-line wall-strip lemma.**  In a container `[0,t]^2` with `t ≤ 4`, at most three
closed unit squares that are pairwise disjoint *as closed sets* have their centre at height at most
`(3√2 - 2)/2 ≈ 1.12132` above the bottom wall.  Proof: every such square has a chord of length
`≥ 1` on the line `y = √2 - 1/2`. -/
theorem wall_strip_le_three_line {N : ℕ} {t : ℝ} (ht : t ≤ 4)
    (ctr : Fin N → ℝ × ℝ) (ang : Fin N → ℝ)
    (hin : ∀ i, sq (ctr i) (ang i) 1 ⊆ box t)
    (hstrip : ∀ i, (ctr i).2 ≤ (3 * Real.sqrt 2 - 2) / 2)
    (hdisj : ∀ i j, i ≠ j → Disjoint (sq (ctr i) (ang i) 1) (sq (ctr j) (ang j) 1)) :
    N ≤ 3 := by
  by_contra hN
  push Not at hN
  choose x hx using fun i => exists_chord_line (hin i) (hstrip i)
  have hrange : ∀ i, x i ∈ Set.Icc (0 : ℝ) 3 := by
    intro i
    have h0 := hin i (hx i (x i) ⟨le_rfl, by linarith⟩)
    have h1 := hin i (hx i (x i + 1) ⟨by linarith, le_rfl⟩)
    exact ⟨h0.1, by have h := h1.2.1; simp only at h ⊢; linarith⟩
  have hgap : ∀ i j, i ≠ j → 1 < |x i - x j| := by
    intro i j hij
    by_contra hle
    push Not at hle
    rw [abs_le] at hle
    rcases le_total (x i) (x j) with h | h
    · exact (Set.disjoint_left.mp (hdisj i j hij)
        (hx i (x j) ⟨h, by linarith [hle.2]⟩)) (hx j (x j) ⟨le_rfl, by linarith⟩)
    · exact (Set.disjoint_left.mp (hdisj i j hij)
        (hx i (x i) ⟨le_rfl, by linarith⟩)) (hx j (x i) ⟨h, by linarith [hle.1]⟩)
  exact no_four_spread hN x hrange hgap

/-- **The single-line wall-strip lemma, packing form.**  Squares of side `L > 1` with pairwise
disjoint interiors in `[0,t]^2`, `t ≤ 4`: at most three have centre height `≤ (3√2 - 2)/2`. -/
theorem wall_strip_le_three_line_of_packing {N : ℕ} {t L : ℝ} (ht : t ≤ 4) (hL : 1 < L)
    (ctr : Fin N → ℝ × ℝ) (ang : Fin N → ℝ)
    (hin : ∀ i, sq (ctr i) (ang i) L ⊆ box t)
    (hstrip : ∀ i, (ctr i).2 ≤ (3 * Real.sqrt 2 - 2) / 2)
    (hdisj : ∀ i j, i ≠ j → Disjoint (sqInt (ctr i) (ang i) L) (sqInt (ctr j) (ang j) L)) :
    N ≤ 3 := by
  have hIntSub : ∀ (c : ℝ × ℝ) (θ : ℝ), sqInt c θ L ⊆ sq c θ L := by
    rintro c θ p ⟨h1, h2⟩; exact ⟨le_of_lt h1, le_of_lt h2⟩
  refine wall_strip_le_three_line ht ctr ang (fun i => ?_) hstrip (fun i j hij => ?_)
  · exact subset_trans (subset_trans (unit_subset_interior hL) (hIntSub _ _)) (hin i)
  · exact Set.disjoint_of_subset (unit_subset_interior hL) (unit_subset_interior hL) (hdisj i j hij)

end SquarePacking
