import Sqpack.Bentz4

/-!
# Splitting `Valid7` / `Valid9`: the tilted run, the axis face (Lemma Z), the D4 reduction

`Valid7` (`Bentz.lean`) and `Valid9` (`Bentz4.lean`) say that every closed unit square in the box
has mass `≥ 1`.  The Python certificate establishes this in three parts:

1. `qx2_zm.py`'s box run: centres in `[0, m/2]²` (the root boxes of `zeromargin.d4_roots`), `u =
   tan(θ/2) > 0` with `θ ≤ 45°` (the roots reach `u = 1/2`, but leaves with `u₀² + 2u₀ − 1 ≥ 0` are
   labelled `SYM` and delegated to the D4 symmetry; `AXIS` leaves, `u = 0`, to Lemma Z), admissible
   squares only.  This is `ValidTilt` below, stated in the checker's coordinate `u`.
2. Lemma Z (`qx2_zm.py axis`): the `θ = 0` face.  `ValidAxis`.
3. The D4 reduction (paper): the cover is invariant under the symmetries of the box, so the
   fundamental domain suffices.

This file proves (3) and (2) in Lean, generically:

* `valid_of_tilt_axis` — `D4InvM m μ → ValidTilt m μ → ValidAxis m μ → (every closed unit square in
  box m has μ-mass ≥ 1)`.
* `gridCover K A den w` — a measure made of unit segments of the `1/5`-grid inside `[0,K]²` (mass
  `w s / den` each, uniformly by length) plus Lebesgue measure on `[A/5, K − A/5]²`.  Both box files
  are of this form (`ValidSplit7.lean`, `ValidSplit9.lean`).
* `d4InvM_gridCover` — D4 invariance of such a measure when the weight table is invariant under the
  index maps of `x ↦ K − x` and `x ↔ y` (`SymW`; decided by `symOKP`, §5).
* `validAxis_gridCover` — **Lemma Z** from a finite statement `AxisW` (decided by `axisOKP`): for
  each `(1/5)`-cell `(p, q)` of lower-left corners of the axis square and each corner `(a, b) ∈
  {0,1}²` of the cell, the mass of the corner's one-sided limit (an integer sum over 50 unit
  segments, plus the Lebesgue overlap) is `≥ 1`.  Soundness: on the closed cell the mass is at
  least the bilinear interpolation of the four corner values (each segment's length fraction is
  exact or larger, the indicator of its line is the cell's interior value or larger — closed
  squares; the Lebesgue overlaps interpolate exactly), and a convex combination of numbers `≥ 1`
  is `≥ 1`.
* §5: packed weight tables (one `ℕ` literal per box file) and the kernel checks `fitOK`, `symOKP`,
  `axisOKP`.

`notes/lean-valid-split.md`.
-/

open MeasureTheory Finset
open scoped ENNReal

namespace SquarePacking
namespace ValidSplit

open Bentz (SegIx segA segB grid mem_grid)

/-! ## 1.  The split: tilted run + axis face + D4 -/

/-- **What `qx2_zm.py`'s box run certifies** (the D4 root domain): every admissible closed unit
square with centre in `[0, m/2]²` and angle `θ = 2 arctan u`, `u > 0`, `u² + 2u ≤ 1` (i.e. `0 < θ ≤
45°`), has mass `≥ 1`. -/
def ValidTilt (m : ℝ) (μ : Measure (ℝ × ℝ)) : Prop :=
  ∀ (c : ℝ × ℝ) (u : ℝ), c.1 ∈ Set.Icc 0 (m / 2) → c.2 ∈ Set.Icc 0 (m / 2) → 0 < u →
    u ^ 2 + 2 * u ≤ 1 → sq c (2 * Real.arctan u) 1 ⊆ box m →
      1 ≤ μ (sq c (2 * Real.arctan u) 1)

/-- **Lemma Z's statement**: every axis-parallel closed unit square in `box m` has mass `≥ 1`. -/
def ValidAxis (m : ℝ) (μ : Measure (ℝ × ℝ)) : Prop :=
  ∀ c : ℝ × ℝ, sq c 0 1 ⊆ box m → 1 ≤ μ (sq c 0 1)

/-- For `0 < θ ≤ π/4`, `u = tan(θ/2)` has `θ = 2 arctan u`, `u > 0` and `u² + 2u ≤ 1`. -/
lemma exists_u_of_theta_pos {θ : ℝ} (h0 : 0 < θ) (h1 : θ ≤ Real.pi / 4) :
    ∃ u : ℝ, 0 < u ∧ u ^ 2 + 2 * u ≤ 1 ∧ 2 * Real.arctan u = θ := by
  have hpi := Real.pi_pos
  set u := Real.tan (θ / 2) with hu
  have he : 2 * Real.arctan u = θ := by
    rw [hu, Real.arctan_tan (by linarith) (by linarith)]; ring
  refine ⟨u, Real.tan_pos_of_pos_of_lt_pi_div_two (by linarith) (by linarith), ?_, he⟩
  have hs : Real.sin θ ≤ Real.sin (Real.pi / 4) :=
    Real.sin_le_sin_of_le_of_le_pi_div_two (by linarith) (by linarith) h1
  have hc : Real.cos (Real.pi / 4) ≤ Real.cos θ :=
    Real.cos_le_cos_of_nonneg_of_le_pi h0.le (by linarith) h1
  rw [Real.sin_pi_div_four] at hs
  rw [Real.cos_pi_div_four] at hc
  rw [← he, sin_two_arctan] at hs
  rw [← he, cos_two_arctan] at hc
  have hN : (0 : ℝ) < 1 + u ^ 2 := by positivity
  have key : 2 * u ≤ 1 - u ^ 2 := by
    have := le_trans hs hc
    rwa [div_le_div_iff_of_pos_right hN] at this
  linarith

/-- **The split.**  A D4-invariant measure for which the tilted run's domain (`ValidTilt`) and the
axis face (`ValidAxis`) are valid gives every closed unit square in `box m` mass `≥ 1`. -/
theorem valid_of_tilt_axis {m : ℝ} {μ : Measure (ℝ × ℝ)} (hinv : D4InvM m μ)
    (ht : ValidTilt m μ) (ha : ValidAxis m μ) :
    ∀ (c : ℝ × ℝ) (θ : ℝ), sq c θ 1 ⊆ box m → 1 ≤ μ (sq c θ 1) := by
  refine d4_reduction_measure m μ hinv fun c θ h1 h2 hθ hsub => ?_
  rcases eq_or_lt_of_le hθ.1 with h0 | h0
  · subst h0; exact ha c hsub
  · obtain ⟨u, hu0, hu1, rfl⟩ := exists_u_of_theta_pos h0 hθ.2
    exact ht c u h1 h2 hu0 hu1 hsub

/-! ## 2.  Grid covers -/

/-- The unit segments of the `1/5`-grid that lie in `[0,K]²`. -/
def segsIn (K : ℕ) : Finset SegIx :=
  (grid K).filter fun s => (s.1 = true ∧ s.2.2 < 5 * (K : ℤ)) ∨ (s.1 = false ∧ s.2.1 < 5 * (K : ℤ))

lemma mem_segsIn {K : ℕ} {o : Bool} {i j : ℤ} :
    (o, i, j) ∈ segsIn K ↔ (0 ≤ i ∧ i ≤ 5 * (K : ℤ)) ∧ (0 ≤ j ∧ j ≤ 5 * (K : ℤ)) ∧
      ((o = true ∧ j < 5 * (K : ℤ)) ∨ (o = false ∧ i < 5 * (K : ℤ))) := by
  simp only [segsIn, mem_filter, mem_grid, and_assoc]

/-- **A grid cover**: mass `w s / den` on each unit segment `s` of the `1/5`-grid in `[0,K]²`
(uniformly by length), and Lebesgue measure on `[A/5, K − A/5]²` (as a polygon with mass = area). -/
noncomputable def gridCover (K A den : ℕ) (w : SegIx → ℕ) : MixedCover Empty SegIx Unit where
  pts := ∅
  pt := fun e => e.elim
  pw := fun e => e.elim
  segs := segsIn K
  sa := segA
  sb := segB
  sw := fun s => (w s : ℝ) / den
  polys := univ
  poly := fun _ => BentzFam.lebSq A K
  gw := fun _ => ((K : ℝ) - 2 * A / 5) ^ 2

lemma gridCover_nonneg (K A den : ℕ) (w : SegIx → ℕ) : (gridCover K A den w).Nonneg :=
  ⟨fun e => e.elim, fun _ _ => by simp only [gridCover]; positivity,
    fun _ _ => by simp only [gridCover]; positivity⟩

/-- The weights vanish on the grid segments outside `[0,K]²` (on `x = K + ...`, `y = K + ...`). -/
def outOK (K : ℕ) (w : SegIx → ℕ) : Bool :=
  (List.range (5 * K + 1)).all fun j =>
    w (false, ((5 * K : ℕ) : ℤ), (j : ℤ)) == 0 && w (true, (j : ℤ), ((5 * K : ℕ) : ℤ)) == 0

lemma outOK_spec {K : ℕ} {w : SegIx → ℕ} (h : outOK K w = true) {s : SegIx} (hs : s ∈ grid K)
    (hn : s ∉ segsIn K) : w s = 0 := by
  obtain ⟨o, i, j⟩ := s
  rw [mem_grid] at hs
  simp only at hs
  rw [mem_segsIn] at hn
  simp only [outOK, List.all_eq_true, List.mem_range, Bool.and_eq_true, beq_iff_eq] at h
  cases o
  · have hi : i = ((5 * K : ℕ) : ℤ) := by push_cast; simp at hn; omega
    have := (h j.toNat (by omega)).1
    rwa [show ((j.toNat : ℕ) : ℤ) = j by omega, ← hi] at this
  · have hj : j = ((5 * K : ℕ) : ℤ) := by push_cast; simp at hn; omega
    have := (h i.toNat (by omega)).2
    rwa [show ((i.toNat : ℕ) : ℤ) = i by omega, ← hj] at this

/-- **A cover of grid-cover shape over the whole grid `[0,K]²` (as the families' `μ_K` are) is the
grid cover**, when the weights vanish outside `[0,K]²`. -/
theorem measure_eq_gridCover (M : MixedCover Empty SegIx Unit) (K A den : ℕ) (w : SegIx → ℕ)
    (hpts : M.pts = ∅) (hsegs : M.segs = grid K) (hsa : M.sa = segA) (hsb : M.sb = segB)
    (hsw : ∀ s, M.sw s = (w s : ℝ) / den) (hpolys : M.polys = univ)
    (hpoly : ∀ u, M.poly u = BentzFam.lebSq A K) (hgw : ∀ u, M.gw u = ((K : ℝ) - 2 * A / 5) ^ 2)
    (hout : outOK K w = true) : M.measure = (gridCover K A den w).measure := by
  unfold MixedCover.measure
  refine congrArg₂ (· + ·) (congrArg₂ (· + ·) ?_ ?_) ?_
  · rw [hpts, sum_empty]; exact sum_empty.symm
  · rw [hsegs, show (gridCover K A den w).segs = segsIn K from rfl]
    have hf : ∀ j, ENNReal.ofReal (M.sw j) • segMeasure (M.sa j) (M.sb j) =
        ENNReal.ofReal ((gridCover K A den w).sw j) •
          segMeasure ((gridCover K A den w).sa j) ((gridCover K A den w).sb j) := fun j => by
      rw [hsw, hsa, hsb]; rfl
    simp only [hf]
    symm
    refine Finset.sum_subset (Finset.filter_subset _ (grid K)) fun s hs hn => ?_
    simp [gridCover, outOK_spec hout hs hn]
  · rw [hpolys]
    refine Finset.sum_congr rfl fun u _ => ?_
    rw [hpoly, hgw]; rfl

/-- The weight of a unit segment in a `BentzFam` family measure: both layers. -/
def famW (F : BentzFam.Fam) (K : ℕ) (s : SegIx) : ℕ :=
  BentzFam.wN F K (s, false) + BentzFam.wN F K (s, true)

/-- **A `BentzFam` family measure `μ_K` is a grid cover** (the two layers of a unit segment added),
when the weights vanish outside `[0,K]²`. -/
theorem famCover_measure_eq (F : BentzFam.Fam) (K : ℕ) (hout : outOK K (famW F K) = true) :
    (BentzFam.famCover F K).measure = (gridCover K F.A F.den (famW F K)).measure := by
  unfold MixedCover.measure
  refine congrArg₂ (· + ·) (congrArg₂ (· + ·) rfl ?_) rfl
  change ∑ x ∈ grid K ×ˢ (univ : Finset Bool),
      ENNReal.ofReal ((BentzFam.wN F K x : ℝ) / F.den) • segMeasure (segA x.1) (segB x.1)
    = ∑ s ∈ segsIn K, ENNReal.ofReal ((famW F K s : ℝ) / F.den) • segMeasure (segA s) (segB s)
  have hterm : ∀ s : SegIx, ∑ b ∈ (univ : Finset Bool),
      ENNReal.ofReal ((BentzFam.wN F K (s, b) : ℝ) / F.den) • segMeasure (segA s) (segB s)
      = ENNReal.ofReal ((famW F K s : ℝ) / F.den) • segMeasure (segA s) (segB s) := by
    intro s
    rw [Fintype.sum_bool, ← add_smul, ← ENNReal.ofReal_add (by positivity) (by positivity)]
    congr 2
    simp only [famW, Nat.cast_add]; ring
  rw [Finset.sum_product]
  simp only [hterm]
  symm
  refine Finset.sum_subset (Finset.filter_subset _ (grid K)) fun s hs hn => ?_
  simp [outOK_spec hout hs hn]

/-! ## 3.  D4 invariance from a finite check -/

/-- The index map of `x ↦ K − x` on unit segments. -/
def reflIx (K : ℕ) (s : SegIx) : SegIx :=
  if s.1 then (true, 5 * (K : ℤ) - s.2.1, s.2.2) else (false, 5 * (K : ℤ) - 1 - s.2.1, s.2.2)

/-- The index map of `x ↔ y` on unit segments. -/
def swapIx (s : SegIx) : SegIx := (!s.1, s.2.2, s.2.1)

/-- **The weights are D4-invariant**: unchanged by the index maps of `x ↦ K − x` and `x ↔ y`. -/
def SymW (K : ℕ) (w : SegIx → ℕ) : Prop :=
  ∀ s ∈ segsIn K, w (reflIx K s) = w s ∧ w (swapIx s) = w s

lemma lebSq_reflX (A K : ℕ) : BentzFam.lebSq A K = reflX K ⁻¹' BentzFam.lebSq A K := by
  ext p
  simp only [BentzFam.lebSq, Set.mem_preimage, reflX, Set.mem_prod, Set.mem_Icc]
  constructor <;> rintro ⟨⟨h1, h2⟩, h3, h4⟩ <;> exact ⟨⟨by linarith, by linarith⟩, h3, h4⟩

lemma lebSq_swapXY (A K : ℕ) : BentzFam.lebSq A K = swapXY ⁻¹' BentzFam.lebSq A K := by
  ext p
  simp only [BentzFam.lebSq, Set.mem_preimage, swapXY, Set.mem_prod, Set.mem_Icc]
  constructor <;> rintro ⟨h1, h2⟩ <;> exact ⟨h2, h1⟩

/-- **D4 invariance of a grid cover** with D4-invariant weights. -/
theorem d4InvM_gridCover {K A den : ℕ} {w : SegIx → ℕ} (h : SymW K w) :
    D4InvM K (gridCover K A den w).measure := by
  refine (gridCover K A den w).d4InvM K ?_ id id (reflIx K) swapIx id id
    (fun e => e.elim) ?_ ?_ (fun e => e.elim) ?_ ?_
  · intro _ _
    exact measurableSet_Icc.prod measurableSet_Icc
  · intro s hs
    obtain ⟨o, i, j⟩ := s
    change (o, i, j) ∈ segsIn K at hs
    have hw := (h _ hs).1
    rw [mem_segsIn] at hs
    simp only [gridCover]
    cases o <;> simp only [Bool.false_eq_true, Bool.true_eq_false, false_and, true_and, false_or,
      or_false] at hs
    · refine ⟨?_, ?_, ?_, Or.inr ⟨?_, ?_⟩⟩
      · simp only [reflIx, if_false, mem_segsIn, Bool.false_eq_true, false_and,
          true_and, false_or]; omega
      · simp only [hw]
      · simp only [reflIx, Bool.false_eq_true, if_false]; ext <;> simp
      · simp only [reflIx, Bool.false_eq_true, if_false, segA, segB, reflX]
        ext <;> push_cast <;> ring
      · simp only [reflIx, Bool.false_eq_true, if_false, segA, segB, reflX]
        ext <;> push_cast <;> ring
    · refine ⟨?_, ?_, ?_, Or.inl ⟨?_, ?_⟩⟩
      · simp only [reflIx, if_true, mem_segsIn, Bool.true_eq_false, false_and,
          true_and, or_false]; omega
      · simp only [hw]
      · simp only [reflIx, if_true]; ext <;> simp
      · simp only [reflIx, if_true, segA, reflX]
        ext <;> push_cast <;> ring
      · simp only [reflIx, if_true, segB, reflX]
        ext <;> push_cast <;> ring
  · intro u _
    exact ⟨mem_univ _, by trivial, by trivial, lebSq_reflX A K⟩
  · intro s hs
    obtain ⟨o, i, j⟩ := s
    change (o, i, j) ∈ segsIn K at hs
    have hw := (h _ hs).2
    rw [mem_segsIn] at hs
    simp only [gridCover]
    cases o <;> simp only [Bool.false_eq_true, Bool.true_eq_false, false_and, true_and, false_or,
      or_false] at hs
    · refine ⟨?_, ?_, ?_, Or.inl ⟨?_, ?_⟩⟩
      · simp only [swapIx, Bool.not_false, mem_segsIn, Bool.true_eq_false,
          false_and, true_and, or_false]; omega
      · simp only [hw]
      · simp [swapIx]
      · simp [swapIx, segA, swapXY]
      · simp [swapIx, segB, swapXY]
    · refine ⟨?_, ?_, ?_, Or.inl ⟨?_, ?_⟩⟩
      · simp only [swapIx, Bool.not_true, mem_segsIn, Bool.false_eq_true,
          false_and, true_and, false_or]; omega
      · simp only [hw]
      · simp [swapIx]
      · simp [swapIx, segA, swapXY]
      · simp [swapIx, segB, swapXY]
  · intro u _
    exact ⟨mem_univ _, by trivial, by trivial, lebSq_swapXY A K⟩

/-! ## 4.  Lemma Z from a finite check

An axis-parallel closed unit square is `[x₀, x₀ + 1] × [y₀, y₀ + 1]`; write `5x₀ = p + σ`, `5y₀ = q
+ τ` with `p, q ∈ {0, …, 5K − 6}` and `σ, τ ∈ [0, 1]`.  At the corner `(a, b) ∈ {0,1}²` of the cell
`(p, q)` the one-sided limit of the mass "from inside the cell" counts, in full, the horizontal unit
segments `(i, j)` with `p + a ≤ i ≤ p + a + 4`, `q + 1 ≤ j ≤ q + 5` and the vertical ones with
`p + 1 ≤ i ≤ p + 5`, `q + b ≤ j ≤ q + b + 4` (`cornerSet`), and Lebesgue overlaps `lov (p + a)`,
`lov (q + b)` (in fifths).  On the closed cell the mass is at least the bilinear interpolation of
the four corner values. -/

/-- The unit segments counted in full at corner `(a, b)` of cell `(p, q)`. -/
def cornerSet (p q a b : ℕ) : Finset SegIx :=
  ((range 5 ×ˢ range 5).image fun x : ℕ × ℕ =>
      ((false, ((p + a + x.1 : ℕ) : ℤ), ((q + 1 + x.2 : ℕ) : ℤ)) : SegIx)) ∪
    ((range 5 ×ˢ range 5).image fun x : ℕ × ℕ =>
      ((true, ((p + 1 + x.1 : ℕ) : ℤ), ((q + b + x.2 : ℕ) : ℤ)) : SegIx))

/-- The weight counted at corner `(a, b)` of cell `(p, q)`. -/
def cornerSum (w : SegIx → ℕ) (p q a b : ℕ) : ℕ :=
  (∑ x ∈ range 5 ×ˢ range 5, w (false, ((p + a + x.1 : ℕ) : ℤ), ((q + 1 + x.2 : ℕ) : ℤ))) +
    ∑ x ∈ range 5 ×ˢ range 5, w (true, ((p + 1 + x.1 : ℕ) : ℤ), ((q + b + x.2 : ℕ) : ℤ))

/-- The overlap of `[A, 5K − A]` with `[n, n + 5]` (in fifths). -/
def lov (K A n : ℕ) : ℕ := min (5 * K - A) (n + 5) - max A n

/-- **Lemma Z, the finite statement**: at every corner of every cell of lower-left corners
`[0, K − 1]²`, `mass ≥ 1`, i.e. `25·den ≤ 25·(segment weight) + den·(Lebesgue overlaps)`.  (Decided
by `axisOKP` for packed weights, §5.) -/
def AxisW (K A den : ℕ) (w : SegIx → ℕ) : Prop :=
  ∀ p q a b : ℕ, p < 5 * K - 5 → q < 5 * K - 5 → a < 2 → b < 2 →
    25 * den ≤ 25 * cornerSum w p q a b + den * (lov K A (p + a) * lov K A (q + b))

lemma mem_cornerSet_false {p q a b : ℕ} {i j : ℤ} :
    (false, i, j) ∈ cornerSet p q a b ↔
      ((p + a : ℕ) : ℤ) ≤ i ∧ i ≤ (p + a : ℕ) + 4 ∧ (q : ℤ) + 1 ≤ j ∧ j ≤ (q : ℤ) + 5 := by
  simp only [cornerSet, mem_union, mem_image, mem_product, mem_range, Prod.mk.injEq]
  constructor
  · rintro (⟨⟨x, y⟩, ⟨hx, hy⟩, -, rfl, rfl⟩ | ⟨_, _, h, -⟩)
    · push_cast; omega
    · exact absurd h (by decide)
  · rintro ⟨h1, h2, h3, h4⟩
    left
    refine ⟨((i - (p + a : ℕ)).toNat, (j - (q + 1)).toNat), ⟨by omega, by omega⟩, trivial, ?_,
      ?_⟩ <;> push_cast at * <;> omega

lemma mem_cornerSet_true {p q a b : ℕ} {i j : ℤ} :
    (true, i, j) ∈ cornerSet p q a b ↔
      (p : ℤ) + 1 ≤ i ∧ i ≤ (p : ℤ) + 5 ∧ ((q + b : ℕ) : ℤ) ≤ j ∧ j ≤ (q + b : ℕ) + 4 := by
  simp only [cornerSet, mem_union, mem_image, mem_product, mem_range, Prod.mk.injEq]
  constructor
  · rintro (⟨_, _, h, -⟩ | ⟨⟨x, y⟩, ⟨hx, hy⟩, -, rfl, rfl⟩)
    · exact absurd h (by decide)
    · push_cast; omega
  · rintro ⟨h1, h2, h3, h4⟩
    right
    refine ⟨((i - (p + 1)).toNat, (j - (q + b : ℕ)).toNat), ⟨by omega, by omega⟩, trivial, ?_,
      ?_⟩ <;> push_cast at * <;> omega

lemma cornerSet_subset {K p q a b : ℕ} (hp : p + 6 ≤ 5 * K) (hq : q + 6 ≤ 5 * K) (ha : a ≤ 1)
    (hb : b ≤ 1) : cornerSet p q a b ⊆ segsIn K := by
  rintro ⟨o, i, j⟩ hs
  rw [mem_segsIn]
  cases o
  · rw [mem_cornerSet_false] at hs; push_cast at hs
    simp only [Bool.false_eq_true, false_and, true_and, false_or]; omega
  · rw [mem_cornerSet_true] at hs; push_cast at hs
    simp only [true_and]; omega

/-- The corner sum is the weight of `cornerSet`. -/
lemma sum_cornerSet (w : SegIx → ℕ) (p q a b : ℕ) :
    ∑ s ∈ cornerSet p q a b, w s = cornerSum w p q a b := by
  unfold cornerSet cornerSum
  rw [sum_union, sum_image, sum_image]
  · rintro ⟨x, y⟩ _ ⟨x', y'⟩ _ h
    simp only [Prod.mk.injEq, Nat.cast_inj] at h
    simp only [Prod.mk.injEq]; omega
  · rintro ⟨x, y⟩ _ ⟨x', y'⟩ _ h
    simp only [Prod.mk.injEq, Nat.cast_inj] at h
    simp only [Prod.mk.injEq]; omega
  · rw [Finset.disjoint_left]
    intro s hs1 hs2
    obtain ⟨_, _, rfl⟩ := mem_image.mp hs1
    obtain ⟨_, _, h⟩ := mem_image.mp hs2
    simp at h

/-- The closed axis-parallel unit square. -/
lemma sq_zero (c : ℝ × ℝ) :
    sq c 0 1 =
      Set.Icc (c.1 - 1 / 2) (c.1 - 1 / 2 + 1) ×ˢ Set.Icc (c.2 - 1 / 2) (c.2 - 1 / 2 + 1) := by
  ext p
  simp only [sq, coord, Real.cos_zero, Real.sin_zero, mul_one, mul_zero, add_zero, zero_add,
    Set.mem_ofPred_eq, Set.mem_prod, Set.mem_Icc, abs_le]
  constructor
  · rintro ⟨⟨h1, h2⟩, h3, h4⟩; exact ⟨⟨by linarith, by linarith⟩, by linarith, by linarith⟩
  · rintro ⟨⟨h1, h2⟩, h3, h4⟩; exact ⟨⟨by linarith, by linarith⟩, by linarith, by linarith⟩

/-- A segment carries at least the fraction `hi − lo` in `S` if its parameter range `[lo, hi] ⊆
[0, 1]` lies in `S`. -/
lemma segFrac_ge {a b : ℝ × ℝ} {S : Set (ℝ × ℝ)} {lo hi : ℝ} (h0 : 0 ≤ lo) (h1 : hi ≤ 1)
    (hS : ∀ t, lo ≤ t → t ≤ hi → segPt a b t ∈ S) : hi - lo ≤ segFrac a b S := by
  unfold segFrac
  rcases le_or_gt lo hi with hlh | hlh
  · have hsub : Set.Icc lo hi ⊆ segPt a b ⁻¹' S ∩ Set.Icc 0 1 := fun t ht =>
      ⟨hS t ht.1 ht.2, by constructor <;> linarith [ht.1, ht.2]⟩
    have hfin : volume (segPt a b ⁻¹' S ∩ Set.Icc (0 : ℝ) 1) ≠ ⊤ :=
      ne_top_of_le_ne_top (by simp [Real.volume_Icc]) (measure_mono Set.inter_subset_right)
    calc hi - lo = (volume (Set.Icc lo hi)).toReal := by
          rw [Real.volume_Icc, ENNReal.toReal_ofReal (by linarith)]
      _ ≤ _ := ENNReal.toReal_mono hfin (measure_mono hsub)
  · linarith [ENNReal.toReal_nonneg (a := volume (segPt a b ⁻¹' S ∩ Set.Icc (0 : ℝ) 1))]

lemma segFrac_nonneg' (a b : ℝ × ℝ) (S : Set (ℝ × ℝ)) : 0 ≤ segFrac a b S := ENNReal.toReal_nonneg

/-- The indicator of `cornerSet`. -/
noncomputable def cE (p q a b : ℕ) (s : SegIx) : ℝ := if s ∈ cornerSet p q a b then 1 else 0

/-- The interpolation weights. -/
noncomputable def lam (σ τ : ℝ) (a b : ℕ) : ℝ :=
  (if a = 0 then 1 - σ else σ) * (if b = 0 then 1 - τ else τ)

/-- **Per segment**: the length fraction in the square is at least the bilinear interpolation of
the corner indicators. -/
lemma seg_lb {p q : ℕ} {σ τ x₀ y₀ : ℝ} (hσ0 : 0 ≤ σ) (hσ1 : σ ≤ 1) (hτ0 : 0 ≤ τ) (hτ1 : τ ≤ 1)
    (hx : 5 * x₀ = p + σ) (hy : 5 * y₀ = q + τ) (s : SegIx) :
    lam σ τ 0 0 * cE p q 0 0 s + lam σ τ 1 0 * cE p q 1 0 s + lam σ τ 0 1 * cE p q 0 1 s +
        lam σ τ 1 1 * cE p q 1 1 s
      ≤ segFrac (segA s) (segB s) (Set.Icc x₀ (x₀ + 1) ×ˢ Set.Icc y₀ (y₀ + 1)) := by
  have hF := segFrac_nonneg' (segA s) (segB s) (Set.Icc x₀ (x₀ + 1) ×ˢ Set.Icc y₀ (y₀ + 1))
  obtain ⟨o, i, j⟩ := s
  simp only [lam, cE, if_true, one_ne_zero, if_false]
  cases o
  · simp only [mem_cornerSet_false]
    push_cast
    have hpt : ∀ t, segPt (segA (false, i, j)) (segB (false, i, j)) t =
        (((i : ℝ) + t) / 5, (j : ℝ) / 5) := by
      intro t; simp only [segPt, segA, segB, Bool.false_eq_true, if_false]; ext <;> simp; ring_nf
    by_cases hj : (q : ℤ) + 1 ≤ j ∧ j ≤ (q : ℤ) + 5
    · have hjr : (q : ℝ) + 1 ≤ j ∧ (j : ℝ) ≤ q + 5 := by
        constructor <;> [exact_mod_cast hj.1; exact_mod_cast hj.2]
      have key : ∀ lo hi : ℝ, 0 ≤ lo → hi ≤ 1 →
          (∀ t, lo ≤ t → t ≤ hi → (p : ℝ) + σ ≤ i + t ∧ (i : ℝ) + t ≤ p + σ + 5) →
          hi - lo ≤ segFrac (segA (false, i, j)) (segB (false, i, j))
            (Set.Icc x₀ (x₀ + 1) ×ˢ Set.Icc y₀ (y₀ + 1)) := by
        intro lo hi h0 h1 h
        refine segFrac_ge h0 h1 fun t ht1 ht2 => ?_
        obtain ⟨h3, h4⟩ := h t ht1 ht2
        rw [hpt, Set.mem_prod, Set.mem_Icc, Set.mem_Icc]
        exact ⟨⟨by linarith, by linarith⟩, by linarith, by linarith⟩
      rcases (show i < p ∨ i = p ∨ ((p : ℤ) + 1 ≤ i ∧ i ≤ p + 4) ∨ i = p + 5 ∨ (p : ℤ) + 5 < i by
        omega) with h | h | h | h | h
      · split_ifs <;> first | (exfalso; omega) | nlinarith
      · have hi : (i : ℝ) = p := by exact_mod_cast h
        have := key σ 1 hσ0 le_rfl fun t h1 h2 => ⟨by linarith, by linarith⟩
        split_ifs <;> first | (exfalso; omega) | nlinarith
      · have hr1 : (p : ℝ) + 1 ≤ i := by exact_mod_cast h.1
        have hr2 : (i : ℝ) ≤ p + 4 := by exact_mod_cast h.2
        have := key 0 1 le_rfl le_rfl fun t h1 h2 => ⟨by linarith, by linarith⟩
        split_ifs <;> first | (exfalso; omega) | nlinarith
      · have hi : (i : ℝ) = p + 5 := by exact_mod_cast h
        have := key 0 σ le_rfl hσ1 fun t h1 h2 => ⟨by linarith, by linarith⟩
        split_ifs <;> first | (exfalso; omega) | nlinarith
      · split_ifs <;> first | (exfalso; omega) | nlinarith
    · split_ifs <;> first | (exfalso; omega) | nlinarith
  · simp only [mem_cornerSet_true]
    push_cast
    have hpt : ∀ t, segPt (segA (true, i, j)) (segB (true, i, j)) t =
        ((i : ℝ) / 5, ((j : ℝ) + t) / 5) := by
      intro t; simp only [segPt, segA, segB, if_true]; ext <;> simp; ring_nf
    by_cases hi : (p : ℤ) + 1 ≤ i ∧ i ≤ (p : ℤ) + 5
    · have hir : (p : ℝ) + 1 ≤ i ∧ (i : ℝ) ≤ p + 5 := by
        constructor <;> [exact_mod_cast hi.1; exact_mod_cast hi.2]
      have key : ∀ lo hi : ℝ, 0 ≤ lo → hi ≤ 1 →
          (∀ t, lo ≤ t → t ≤ hi → (q : ℝ) + τ ≤ j + t ∧ (j : ℝ) + t ≤ q + τ + 5) →
          hi - lo ≤ segFrac (segA (true, i, j)) (segB (true, i, j))
            (Set.Icc x₀ (x₀ + 1) ×ˢ Set.Icc y₀ (y₀ + 1)) := by
        intro lo hi h0 h1 h
        refine segFrac_ge h0 h1 fun t ht1 ht2 => ?_
        obtain ⟨h3, h4⟩ := h t ht1 ht2
        rw [hpt, Set.mem_prod, Set.mem_Icc, Set.mem_Icc]
        exact ⟨⟨by linarith, by linarith⟩, by linarith, by linarith⟩
      rcases (show j < q ∨ j = q ∨ ((q : ℤ) + 1 ≤ j ∧ j ≤ q + 4) ∨ j = q + 5 ∨ (q : ℤ) + 5 < j by
        omega) with h | h | h | h | h
      · split_ifs <;> first | (exfalso; omega) | nlinarith
      · have hj : (j : ℝ) = q := by exact_mod_cast h
        have := key τ 1 hτ0 le_rfl fun t h1 h2 => ⟨by linarith, by linarith⟩
        split_ifs <;> first | (exfalso; omega) | nlinarith
      · have hr1 : (q : ℝ) + 1 ≤ j := by exact_mod_cast h.1
        have hr2 : (j : ℝ) ≤ q + 4 := by exact_mod_cast h.2
        have := key 0 1 le_rfl le_rfl fun t h1 h2 => ⟨by linarith, by linarith⟩
        split_ifs <;> first | (exfalso; omega) | nlinarith
      · have hj : (j : ℝ) = q + 5 := by exact_mod_cast h
        have := key 0 τ le_rfl hτ1 fun t h1 h2 => ⟨by linarith, by linarith⟩
        split_ifs <;> first | (exfalso; omega) | nlinarith
      · split_ifs <;> first | (exfalso; omega) | nlinarith
    · split_ifs <;> first | (exfalso; omega) | nlinarith


/-! ### The Lebesgue square -/

/-- `max c 0` interpolates below `max (c + dσ) 0` for integers `c`, `d ∈ {−1, 0, 1}`. -/
lemma interp_max (c d : ℤ) (hd : -1 ≤ d ∧ d ≤ 1) {σ : ℝ} (hσ0 : 0 ≤ σ) (_hσ1 : σ ≤ 1) :
    (1 - σ) * max (c : ℝ) 0 + σ * max ((c : ℝ) + d) 0 ≤ max ((c : ℝ) + d * σ) 0 := by
  have hd1 : (-1 : ℝ) ≤ d := by exact_mod_cast hd.1
  have hd2 : (d : ℝ) ≤ 1 := by exact_mod_cast hd.2
  rcases (show c ≤ -1 ∨ 0 ≤ c by omega) with hc | hc <;>
    rcases (show c + d ≤ -1 ∨ 0 ≤ c + d by omega) with hcd | hcd
  · have h1 : (c : ℝ) ≤ -1 := by exact_mod_cast hc
    have h2 : (c : ℝ) + d ≤ -1 := by exact_mod_cast hcd
    rw [max_eq_right (by linarith), max_eq_right (by linarith)]
    simp only [mul_zero, add_zero]; exact le_max_right _ _
  · have h1 : (c : ℝ) ≤ -1 := by exact_mod_cast hc
    have h2 : (0 : ℝ) ≤ c + d := by exact_mod_cast hcd
    rw [max_eq_right (by linarith), max_eq_left h2]
    refine le_trans ?_ (le_max_right _ _)
    nlinarith
  · have h1 : (0 : ℝ) ≤ c := by exact_mod_cast hc
    have h2 : (c : ℝ) + d ≤ -1 := by exact_mod_cast hcd
    rw [max_eq_left h1, max_eq_right (by linarith)]
    refine le_trans ?_ (le_max_right _ _)
    nlinarith
  · have h1 : (0 : ℝ) ≤ c := by exact_mod_cast hc
    have h2 : (0 : ℝ) ≤ c + d := by exact_mod_cast hcd
    rw [max_eq_left h1, max_eq_left h2]
    refine le_trans (le_of_eq (by ring_nf)) (le_max_left _ _)

/-- The overlap of `[A, B]` with `[x, x + 5]`, in fifths. -/
noncomputable def ovl (A B x : ℝ) : ℝ := max (min B (x + 5) - max A x) 0

lemma interp_max' (c d : ℤ) (hd : -1 ≤ d ∧ d ≤ 1) {σ : ℝ} (hσ0 : 0 ≤ σ) (hσ1 : σ ≤ 1)
    {x₀ x₁ xs : ℝ} (h0 : x₀ = c) (h1 : x₁ = c + d) (hs : xs = c + d * σ) :
    (1 - σ) * max x₀ 0 + σ * max x₁ 0 ≤ max xs 0 := by
  subst h0 h1 hs; exact interp_max c d hd hσ0 hσ1

/-- **The Lebesgue overlap interpolates exactly enough**: on `[P, P + 1]` (integer ends of the grid)
it is at least the linear interpolation of its values at `P` and `P + 1`. -/
lemma ovl_interp (A B P : ℕ) {σ : ℝ} (hσ0 : 0 ≤ σ) (hσ1 : σ ≤ 1) :
    (1 - σ) * ovl A B P + σ * ovl A B ((P : ℝ) + 1) ≤ ovl A B (P + σ) := by
  unfold ovl
  rcases (show A ≤ P ∨ P + 1 ≤ A by omega) with hA | hA <;>
    rcases (show P + 6 ≤ B ∨ B ≤ P + 5 by omega) with hB | hB
  · have h1 : (A : ℝ) ≤ P := by exact_mod_cast hA
    have h2 : (P : ℝ) + 6 ≤ B := by exact_mod_cast hB
    refine interp_max' 5 0 (by norm_num) hσ0 hσ1 ?_ ?_ ?_
    · rw [min_eq_right (by linarith), max_eq_right h1]; push_cast; ring
    · rw [min_eq_right (show (P : ℝ) + 1 + 5 ≤ B by linarith),
        max_eq_right (show (A : ℝ) ≤ P + 1 by linarith)]; push_cast; ring
    · rw [min_eq_right (show (P : ℝ) + σ + 5 ≤ B by linarith),
        max_eq_right (show (A : ℝ) ≤ P + σ by linarith)]; push_cast; ring
  · have h1 : (A : ℝ) ≤ P := by exact_mod_cast hA
    have h2 : (B : ℝ) ≤ P + 5 := by exact_mod_cast hB
    refine interp_max' ((B : ℤ) - P) (-1) (by norm_num) hσ0 hσ1 ?_ ?_ ?_
    · rw [min_eq_left h2, max_eq_right h1]; push_cast; ring
    · rw [min_eq_left (show (B : ℝ) ≤ P + 1 + 5 by linarith),
        max_eq_right (show (A : ℝ) ≤ P + 1 by linarith)]; push_cast; ring
    · rw [min_eq_left (show (B : ℝ) ≤ P + σ + 5 by linarith),
        max_eq_right (show (A : ℝ) ≤ P + σ by linarith)]; push_cast; ring
  · have h1 : (P : ℝ) + 1 ≤ A := by exact_mod_cast hA
    have h2 : (P : ℝ) + 6 ≤ B := by exact_mod_cast hB
    refine interp_max' ((P : ℤ) + 5 - A) 1 (by norm_num) hσ0 hσ1 ?_ ?_ ?_
    · rw [min_eq_right (by linarith), max_eq_left (show (P : ℝ) ≤ A by linarith)]; push_cast; ring
    · rw [min_eq_right (show (P : ℝ) + 1 + 5 ≤ B by linarith),
        max_eq_left (show (P : ℝ) + 1 ≤ A by linarith)]; push_cast; ring
    · rw [min_eq_right (show (P : ℝ) + σ + 5 ≤ B by linarith),
        max_eq_left (show (P : ℝ) + σ ≤ A by linarith)]; push_cast; ring
  · have h1 : (P : ℝ) + 1 ≤ A := by exact_mod_cast hA
    have h2 : (B : ℝ) ≤ P + 5 := by exact_mod_cast hB
    refine interp_max' ((B : ℤ) - A) 0 (by norm_num) hσ0 hσ1 ?_ ?_ ?_
    · rw [min_eq_left h2, max_eq_left (show (P : ℝ) ≤ A by linarith)]; push_cast; ring
    · rw [min_eq_left (show (B : ℝ) ≤ P + 1 + 5 by linarith),
        max_eq_left (show (P : ℝ) + 1 ≤ A by linarith)]; push_cast; ring
    · rw [min_eq_left (show (B : ℝ) ≤ P + σ + 5 by linarith),
        max_eq_left (show (P : ℝ) + σ ≤ A by linarith)]; push_cast; ring

lemma cast_tsub (a b : ℕ) : ((a - b : ℕ) : ℝ) = max ((a : ℝ) - b) 0 := by
  rcases le_total b a with h | h
  · rw [Nat.cast_sub h, max_eq_left (by linarith [(Nat.cast_le (α := ℝ)).mpr h])]
  · rw [Nat.sub_eq_zero_of_le h, max_eq_right (by linarith [(Nat.cast_le (α := ℝ)).mpr h])]
    simp

lemma lov_eq (K A n : ℕ) : (lov K A n : ℝ) = ovl A ((5 * K - A : ℕ) : ℝ) n := by
  rw [lov, cast_tsub, ovl, Nat.cast_min, Nat.cast_max]; push_cast; rfl

/-- The area of `[x₀, x₀ + 1] × [y₀, y₀ + 1]` inside `[a, b]²`. -/
lemma vol_inter (x₀ y₀ a b : ℝ) :
    (volume ((Set.Icc x₀ (x₀ + 1) ×ˢ Set.Icc y₀ (y₀ + 1)) ∩ (Set.Icc a b ×ˢ Set.Icc a b))).toReal
      = max (min (x₀ + 1) b - max x₀ a) 0 * max (min (y₀ + 1) b - max y₀ a) 0 := by
  rw [Set.prod_inter_prod, Set.Icc_inter_Icc, Set.Icc_inter_Icc, Measure.volume_eq_prod,
    Measure.prod_prod, Real.volume_Icc, Real.volume_Icc, ENNReal.toReal_mul,
    ENNReal.toReal_ofReal', ENNReal.toReal_ofReal']

/-- One factor in fifths. -/
lemma fac_eq (K A : ℕ) (hA : A ≤ 5 * K) (x : ℝ) :
    max (min (x + 1) ((K : ℝ) - A / 5) - max x (A / 5)) 0
      = ovl A ((5 * K - A : ℕ) : ℝ) (5 * x) / 5 := by
  rw [ovl, Nat.cast_sub hA]
  push_cast
  have e1 : min ((5 : ℝ) * K - A) (5 * x + 5) = 5 * min (x + 1) ((K : ℝ) - A / 5) := by
    rw [mul_min_of_nonneg _ _ (by norm_num : (0 : ℝ) ≤ 5)]
    rw [min_comm]; congr 1 <;> ring_nf
  have e2 : max (A : ℝ) (5 * x) = 5 * max x (A / 5) := by
    rw [mul_max_of_nonneg _ _ (by norm_num : (0 : ℝ) ≤ 5)]
    rw [max_comm]; congr 1; ring_nf
  rw [e1, e2, ← mul_sub, show (0 : ℝ) = 5 * 0 by ring, ← mul_max_of_nonneg _ _ (by norm_num)]
  ring_nf

/-! ### Assembly -/

/-- The cell of a lower-left corner coordinate. -/
lemma exists_cell {K : ℕ} (hK : 2 ≤ K) {x : ℝ} (h0 : 0 ≤ x) (h1 : x ≤ (K : ℝ) - 1) :
    ∃ p : ℕ, ∃ σ : ℝ, p + 6 ≤ 5 * K ∧ 0 ≤ σ ∧ σ ≤ 1 ∧ 5 * x = p + σ := by
  have hK' : (2 : ℝ) ≤ K := by exact_mod_cast hK
  have hf1 := Nat.floor_le (show 0 ≤ 5 * x by linarith)
  have hf2 := Nat.lt_floor_add_one (5 * x)
  by_cases h : ⌊5 * x⌋₊ + 6 ≤ 5 * K
  · exact ⟨⌊5 * x⌋₊, 5 * x - ⌊5 * x⌋₊, h, by linarith, by linarith, by ring⟩
  · refine ⟨5 * K - 6, 5 * x - ((5 * K - 6 : ℕ) : ℝ), by omega, ?_, ?_, by ring⟩
    · have : ((5 * K - 6 : ℕ) : ℝ) ≤ ⌊5 * x⌋₊ := by
        exact_mod_cast (show 5 * K - 6 ≤ ⌊5 * x⌋₊ by omega)
      linarith
    · rw [Nat.cast_sub (by omega)]; push_cast; linarith

lemma sum_cE {K : ℕ} (w : SegIx → ℕ) (den : ℕ) {p q a b : ℕ} (hp : p + 6 ≤ 5 * K)
    (hq : q + 6 ≤ 5 * K) (ha : a ≤ 1) (hb : b ≤ 1) :
    ∑ s ∈ segsIn K, (w s : ℝ) / den * cE p q a b s = (cornerSum w p q a b : ℝ) / den := by
  simp only [cE, mul_ite, mul_one, mul_zero]
  rw [← Finset.sum_filter, Finset.filter_mem_eq_inter,
    Finset.inter_eq_right.mpr (cornerSet_subset hp hq ha hb), ← sum_div, ← Nat.cast_sum,
    sum_cornerSet]

/-- **Lemma Z, soundness**: a grid cover satisfying `AxisW` gives every axis-parallel closed unit
square in `[0,K]²` mass `≥ 1`. -/
theorem validAxis_gridCover {K A den : ℕ} {w : SegIx → ℕ} (hK : 2 ≤ K) (hA : 2 * A < 5 * K)
    (hden : 0 < den) (h : AxisW K A den w) :
    ValidAxis K (gridCover K A den w).measure := by
  intro c hsub
  rw [MixedCover.measure_apply _ (gridCover_nonneg _ _ _ _) (measurableSet_sq _ _ _),
    ← ENNReal.ofReal_one]
  apply ENNReal.ofReal_le_ofReal
  have hadm := (sq_subset_box_iff K c 0).mp hsub
  have hw0 : wid 0 = 1 := by simp [wid]
  simp only [Adm, hw0] at hadm
  obtain ⟨hx1, hx2, hy1, hy2⟩ := hadm
  have hK' : (2 : ℝ) ≤ K := by exact_mod_cast hK
  have hA5 : A ≤ 5 * K := by omega
  have hAr : 2 * (A : ℝ) / 5 < K := by
    have : (2 * A : ℝ) < 5 * K := by exact_mod_cast hA
    linarith
  obtain ⟨p, σ, hp, hσ0, hσ1, hx⟩ :=
    exists_cell hK (x := c.1 - 1 / 2) (by linarith) (by linarith)
  obtain ⟨q, τ, hq, hτ0, hτ1, hy⟩ :=
    exists_cell hK (x := c.2 - 1 / 2) (by linarith) (by linarith)
  rw [sq_zero]
  set Q := Set.Icc (c.1 - 1 / 2) (c.1 - 1 / 2 + 1) ×ˢ Set.Icc (c.2 - 1 / 2) (c.2 - 1 / 2 + 1)
    with hQ
  unfold MixedCover.mass
  -- the three parts
  have hpoly : ∑ k ∈ (gridCover K A den w).polys,
      (gridCover K A den w).gw k * areaFrac ((gridCover K A den w).poly k) Q
      = max (min (c.1 - 1 / 2 + 1) ((K : ℝ) - A / 5) - max (c.1 - 1 / 2) (A / 5)) 0 *
          max (min (c.2 - 1 / 2 + 1) ((K : ℝ) - A / 5) - max (c.2 - 1 / 2) (A / 5)) 0 := by
    simp only [gridCover, Finset.sum_const, Finset.card_univ, Fintype.card_unit, one_smul]
    rw [BentzFam.polyTerm hAr, hQ, BentzFam.lebSq, vol_inter]
  rw [show (gridCover K A den w).pts = ∅ from rfl, Finset.filter_empty, Finset.sum_empty, zero_add,
    hpoly, fac_eq K A hA5, fac_eq K A hA5, hx, hy]
  -- the segments
  set B : ℝ := ((5 * K - A : ℕ) : ℝ) with hB
  set S : ℕ → ℕ → ℝ := fun a b => (cornerSum w p q a b : ℝ) / den with hS
  set L : ℕ → ℕ → ℝ := fun a b => (lov K A (p + a) : ℝ) * lov K A (q + b) / 25 with hL
  have hseg : lam σ τ 0 0 * S 0 0 + lam σ τ 1 0 * S 1 0 + lam σ τ 0 1 * S 0 1 + lam σ τ 1 1 * S 1 1
      ≤ ∑ j ∈ (gridCover K A den w).segs,
          (gridCover K A den w).sw j *
            segFrac ((gridCover K A den w).sa j) ((gridCover K A den w).sb j) Q := by
    simp only [gridCover, hS]
    rw [← sum_cE w den hp hq (a := 0) (b := 0) (by norm_num) (by norm_num),
      ← sum_cE w den hp hq (a := 1) (b := 0) (by norm_num) (by norm_num),
      ← sum_cE w den hp hq (a := 0) (b := 1) (by norm_num) (by norm_num),
      ← sum_cE w den hp hq (a := 1) (b := 1) (by norm_num) (by norm_num)]
    simp only [mul_sum, ← sum_add_distrib]
    refine Finset.sum_le_sum fun s _ => ?_
    have hw : (0 : ℝ) ≤ (w s : ℝ) / den := by positivity
    have hl := seg_lb hσ0 hσ1 hτ0 hτ1 (x₀ := c.1 - 1 / 2) (y₀ := c.2 - 1 / 2) hx hy s
    calc _ = (w s : ℝ) / den * (lam σ τ 0 0 * cE p q 0 0 s + lam σ τ 1 0 * cE p q 1 0 s +
            lam σ τ 0 1 * cE p q 0 1 s + lam σ τ 1 1 * cE p q 1 1 s) := by ring
      _ ≤ _ := mul_le_mul_of_nonneg_left hl hw
  -- the Lebesgue square
  have hleb : lam σ τ 0 0 * L 0 0 + lam σ τ 1 0 * L 1 0 + lam σ τ 0 1 * L 0 1 + lam σ τ 1 1 * L 1 1
      ≤ ovl A B (p + σ) / 5 * (ovl A B (q + τ) / 5) := by
    simp only [hL, lov_eq, ← hB, add_zero]
    have ix := ovl_interp A (5 * K - A) p hσ0 hσ1
    have iy := ovl_interp A (5 * K - A) q hτ0 hτ1
    rw [← hB] at ix iy
    have n0 : ∀ x, 0 ≤ ovl A B x := fun x => le_max_right _ _
    have hm := mul_le_mul ix iy (by have := n0 q; have := n0 ((q : ℝ) + 1); positivity)
      (n0 _)
    have e : lam σ τ 0 0 * (ovl A B p * ovl A B q / 25) +
        lam σ τ 1 0 * (ovl A B ((p + 1 : ℕ) : ℝ) * ovl A B q / 25) +
        lam σ τ 0 1 * (ovl A B p * ovl A B ((q + 1 : ℕ) : ℝ) / 25) +
        lam σ τ 1 1 * (ovl A B ((p + 1 : ℕ) : ℝ) * ovl A B ((q + 1 : ℕ) : ℝ) / 25)
        = ((1 - σ) * ovl A B p + σ * ovl A B ((p : ℝ) + 1)) *
            ((1 - τ) * ovl A B q + τ * ovl A B ((q : ℝ) + 1)) / 25 := by
      simp only [lam, if_true, one_ne_zero, if_false]; push_cast; ring
    rw [e]
    linarith
  -- each corner has mass `≥ 1`
  have hd : (0 : ℝ) < den := by exact_mod_cast hden
  have hcorner : ∀ a b : ℕ, a < 2 → b < 2 → 1 ≤ S a b + L a b := by
    intro a b ha hb
    have hc := h p q a b (by omega) (by omega) ha hb
    have hc' : (25 * den : ℝ) ≤ 25 * cornerSum w p q a b +
        den * ((lov K A (p + a) : ℝ) * lov K A (q + b)) := by exact_mod_cast hc
    simp only [hS, hL]
    rw [div_add_div _ _ hd.ne' (by norm_num), le_div_iff₀ (by positivity)]
    calc 1 * ((den : ℝ) * 25) = 25 * den := by ring
      _ ≤ _ := hc'
      _ = _ := by ring
  have l00 : 0 ≤ lam σ τ 0 0 := by simp only [lam, if_true]; nlinarith
  have l10 : 0 ≤ lam σ τ 1 0 := by simp only [lam, if_true, one_ne_zero, if_false]; nlinarith
  have l01 : 0 ≤ lam σ τ 0 1 := by simp only [lam, if_true, one_ne_zero, if_false]; nlinarith
  have l11 : 0 ≤ lam σ τ 1 1 := by simp only [lam, one_ne_zero, if_false]; nlinarith
  have hlam : lam σ τ 0 0 + lam σ τ 1 0 + lam σ τ 0 1 + lam σ τ 1 1 = 1 := by
    simp only [lam, if_true, one_ne_zero, if_false]; ring
  have c00 := mul_le_mul_of_nonneg_left (hcorner 0 0 (by norm_num) (by norm_num)) l00
  have c10 := mul_le_mul_of_nonneg_left (hcorner 1 0 (by norm_num) (by norm_num)) l10
  have c01 := mul_le_mul_of_nonneg_left (hcorner 0 1 (by norm_num) (by norm_num)) l01
  have c11 := mul_le_mul_of_nonneg_left (hcorner 1 1 (by norm_num) (by norm_num)) l11
  have hsum := add_le_add hseg hleb
  rw [mul_add, mul_one] at c00 c10 c01 c11
  linarith

/-! ## 5.  Packed weight tables: the kernel checks

The weights of a box file are packed into one natural number, `48` bits per unit segment of the
grid `{0, …, n}²` (`n = 5K`; index `(o·(n+1) + i)·(n+1) + j` for orientation `o`, x-index `i`,
y-index `j`).  The kernel evaluates `>>>` and `%` on such a literal with GMP, so the checks below
cost a few `ℕ` operations per weight; an evaluation of a family's code-table weight (`Bentz.wN`,
`BentzFam.wN`: `ℤ` arithmetic and list lookups) costs about a millisecond in the kernel.  The packed
table is tied to the family by `fitOK` (one evaluation of the family's weight per grid segment). -/

/-- Field `k` (48 bits) of `P`. -/
def fld (P k : ℕ) : ℕ := (P >>> (48 * k)) % 281474976710656

/-- The packed weight of the unit segment `(o, i, j)`, `o ∈ {0, 1}`, `i, j ≤ n`. -/
def unpackN (P n o i j : ℕ) : ℕ := fld P ((o * (n + 1) + i) * (n + 1) + j)

/-- The weights of a packed table (zero off `{0, …, n}²`). -/
def wP (P n : ℕ) (s : SegIx) : ℕ :=
  if 0 ≤ s.2.1 ∧ s.2.1 ≤ n ∧ 0 ≤ s.2.2 ∧ s.2.2 ≤ n then
    unpackN P n s.1.toNat s.2.1.toNat s.2.2.toNat else 0

lemma wP_nat (P n : ℕ) (o : Bool) {i j : ℕ} (hi : i ≤ n) (hj : j ≤ n) :
    wP P n (o, (i : ℤ), (j : ℤ)) = unpackN P n o.toNat i j := by
  simp only [wP]
  rw [if_pos (by omega)]
  simp

/-- **The packed table is the weight function `w`** on the grid `{0, …, n}²`. -/
def fitOK (n : ℕ) (w : SegIx → ℕ) (P : ℕ) : Bool :=
  [false, true].all fun o => (List.range (n + 1)).all fun i => (List.range (n + 1)).all fun j =>
    w (o, (i : ℤ), (j : ℤ)) == unpackN P n o.toNat i j

lemma fitOK_spec {n : ℕ} {w : SegIx → ℕ} {P : ℕ} (h : fitOK n w P = true) {o : Bool} {i j : ℤ}
    (hi : 0 ≤ i ∧ i ≤ n) (hj : 0 ≤ j ∧ j ≤ n) : w (o, i, j) = wP P n (o, i, j) := by
  simp only [fitOK, List.all_eq_true, List.mem_cons, List.mem_range, beq_iff_eq,
    List.not_mem_nil, or_false] at h
  obtain ⟨i', rfl⟩ : ∃ i' : ℕ, i = i' := ⟨i.toNat, by omega⟩
  obtain ⟨j', rfl⟩ : ∃ j' : ℕ, j = j' := ⟨j.toNat, by omega⟩
  rw [h o (by cases o <;> simp) i' (by omega) j' (by omega), wP_nat P n o (by omega) (by omega)]

/-- A grid cover's measure depends only on the weights of the segments in `[0,K]²`. -/
theorem gridCover_fit {K A den : ℕ} {w : SegIx → ℕ} {P : ℕ} (h : fitOK (5 * K) w P = true) :
    (gridCover K A den w).measure = (gridCover K A den (wP P (5 * K))).measure := by
  unfold MixedCover.measure
  refine congrArg₂ (· + ·) (congrArg₂ (· + ·) rfl ?_) rfl
  refine Finset.sum_congr rfl fun s hs => ?_
  obtain ⟨o, i, j⟩ := s
  change (o, i, j) ∈ segsIn K at hs
  rw [mem_segsIn] at hs
  simp only [gridCover]
  rw [fitOK_spec h (by push_cast; omega) (by push_cast; omega)]

/-- **D4 invariance of a packed table** (`x ↦ K − x` on horizontal and vertical segments; `x ↔ y`
maps horizontal `(i, j)` to vertical `(j, i)`). -/
def symOKP (n P : ℕ) : Bool :=
  ((List.range n).all fun i => (List.range (n + 1)).all fun j =>
    unpackN P n 0 (n - 1 - i) j == unpackN P n 0 i j && unpackN P n 1 j i == unpackN P n 0 i j) &&
  ((List.range (n + 1)).all fun i => (List.range n).all fun j =>
    unpackN P n 1 (n - i) j == unpackN P n 1 i j)

lemma symW_of_symOKP {K P : ℕ} (h : symOKP (5 * K) P = true) : SymW K (wP P (5 * K)) := by
  intro s hs
  obtain ⟨o, i, j⟩ := s
  rw [mem_segsIn] at hs
  simp only [symOKP, Bool.and_eq_true, List.all_eq_true, List.mem_range, beq_iff_eq] at h
  obtain ⟨h1, h2⟩ := h
  obtain ⟨i', rfl⟩ : ∃ i' : ℕ, i = i' := ⟨i.toNat, by omega⟩
  obtain ⟨j', rfl⟩ : ∃ j' : ℕ, j = j' := ⟨j.toNat, by omega⟩
  cases o
  · have hb : i' < 5 * K ∧ j' ≤ 5 * K := by simp at hs; omega
    obtain ⟨e1, e2⟩ := h1 i' hb.1 j' (by omega)
    simp only [reflIx, swapIx, Bool.false_eq_true, if_false, Bool.not_false]
    rw [show 5 * (K : ℤ) - 1 - i' = ((5 * K - 1 - i' : ℕ) : ℤ) by omega,
      wP_nat _ _ _ (by omega) (by omega), wP_nat _ _ _ (by omega) (by omega),
      wP_nat _ _ _ (by omega) (by omega)]
    exact ⟨e1, e2⟩
  · have hb : i' ≤ 5 * K ∧ j' < 5 * K := by simp at hs; omega
    have e1 := h2 i' (by omega) j' hb.2
    obtain ⟨-, e2⟩ := h1 j' hb.2 i' (by omega)
    simp only [reflIx, swapIx, if_true, Bool.not_true]
    rw [show 5 * (K : ℤ) - i' = ((5 * K - i' : ℕ) : ℤ) by omega,
      wP_nat _ _ _ (by omega) (by omega), wP_nat _ _ _ (by omega) (by omega),
      wP_nat _ _ _ (by omega) (by omega)]
    exact ⟨e1, e2.symm⟩

/-- `f 0 + ⋯ + f 4`. -/
def s5 (f : ℕ → ℕ) : ℕ := f 0 + f 1 + f 2 + f 3 + f 4

/-- `cornerSum` of a packed table, in `ℕ` indices. -/
def cornerSumN (P n p q a b : ℕ) : ℕ :=
  s5 (fun x => s5 fun y => unpackN P n 0 (p + a + x) (q + 1 + y)) +
    s5 (fun x => s5 fun y => unpackN P n 1 (p + 1 + x) (q + b + y))

/-- **Lemma Z, the kernel check** (`AxisW` for a packed table). -/
def axisOKP (K A den P : ℕ) : Bool :=
  (List.range (5 * K - 5)).all fun p => (List.range (5 * K - 5)).all fun q =>
    (List.range 2).all fun a => (List.range 2).all fun b =>
      Nat.ble (25 * den)
        (25 * cornerSumN P (5 * K) p q a b + den * (lov K A (p + a) * lov K A (q + b)))

lemma sum_range5_prod (f : ℕ → ℕ → ℕ) :
    ∑ x ∈ range 5 ×ˢ range 5, f x.1 x.2 = s5 fun x => s5 fun y => f x y := by
  rw [Finset.sum_product]
  simp [Finset.sum_range_succ, s5]

lemma cornerSum_wP {P n p q a b : ℕ} (hp : p + 6 ≤ n) (hq : q + 6 ≤ n) (ha : a ≤ 1) (hb : b ≤ 1) :
    cornerSum (wP P n) p q a b = cornerSumN P n p q a b := by
  unfold cornerSum cornerSumN
  have h1 : ∑ x ∈ range 5 ×ˢ range 5,
      wP P n (false, ((p + a + x.1 : ℕ) : ℤ), ((q + 1 + x.2 : ℕ) : ℤ))
      = ∑ x ∈ range 5 ×ˢ range 5, unpackN P n 0 (p + a + x.1) (q + 1 + x.2) :=
    Finset.sum_congr rfl fun x hx => by
      rw [mem_product, mem_range, mem_range] at hx
      rw [wP_nat P n false (by omega) (by omega)]; rfl
  have h2 : ∑ x ∈ range 5 ×ˢ range 5,
      wP P n (true, ((p + 1 + x.1 : ℕ) : ℤ), ((q + b + x.2 : ℕ) : ℤ))
      = ∑ x ∈ range 5 ×ˢ range 5, unpackN P n 1 (p + 1 + x.1) (q + b + x.2) :=
    Finset.sum_congr rfl fun x hx => by
      rw [mem_product, mem_range, mem_range] at hx
      rw [wP_nat P n true (by omega) (by omega)]; rfl
  rw [h1, h2, sum_range5_prod (fun x y => unpackN P n 0 (p + a + x) (q + 1 + y)),
    sum_range5_prod (fun x y => unpackN P n 1 (p + 1 + x) (q + b + y))]

lemma axisW_of_axisOKP {K A den P : ℕ} (h : axisOKP K A den P = true) :
    AxisW K A den (wP P (5 * K)) := by
  intro p q a b hp hq ha hb
  simp only [axisOKP, List.all_eq_true, List.mem_range, Nat.ble_eq] at h
  rw [cornerSum_wP (by omega) (by omega) (by omega) (by omega)]
  exact h p hp q hq a ha b hb

/-- **D4 invariance**, from the kernel check `symOKP`. -/
theorem d4InvM_packed {K A den P : ℕ} (h : symOKP (5 * K) P = true) :
    D4InvM K (gridCover K A den (wP P (5 * K))).measure :=
  d4InvM_gridCover (symW_of_symOKP h)

/-- **Lemma Z**, from the kernel check `axisOKP`. -/
theorem validAxis_packed {K A den P : ℕ} (hK : 2 ≤ K) (hA : 2 * A < 5 * K) (hden : 0 < den)
    (h : axisOKP K A den P = true) :
    ValidAxis K (gridCover K A den (wP P (5 * K))).measure :=
  validAxis_gridCover hK hA hden (axisW_of_axisOKP h)

end ValidSplit
end SquarePacking
