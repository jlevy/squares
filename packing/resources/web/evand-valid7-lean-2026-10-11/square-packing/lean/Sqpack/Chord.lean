import Sqpack.Basic

/-!
# The wall-strip chord lemma

At most **three** closed unit squares with pairwise disjoint interiors inside `[0,t]^2`, `t ≤ 4`,
have their centre within distance `1` of a given wall.

This is Stromquist's and Nagamochi's wall-strip lemma (Nagamochi 2005, Lemma 7(i); Stromquist
1984-I p. 5–8), in the form the certificate tree of `notes/level2-design.md` needs.  The proof is
written out in `notes/chord-lemma.md`; the outline is:

* a closed unit square inside `[0,t]^2` whose centre is at height `c_y ≤ 1` meets the horizontal
  line `y = 9/10` in a chord of length `≥ 1` (`exists_chord`).  `9/10` may be any value in
  `[(3-√2)/2, √2 - 1/2] = [0.79289, 0.91421]`;
* disjoint squares give disjoint chords, hence four pairwise disjoint closed intervals of length
  `≥ 1` inside `[0,t] ⊆ [0,4]`, whose left endpoints are four points of `[0,3]` pairwise more than
  `1` apart -- impossible.

The hypothesis that the *closed* squares are disjoint is essential, and is what the `L > 1`
version supplies: four axis-parallel unit squares in a row across `[0,4]` have disjoint interiors,
centres at height `1/2`, and chords of length exactly `1` summing to exactly `4`.
-/

namespace SquarePacking

/-- The closed container `[0,t]^2`. -/
def box (t : ℝ) : Set (ℝ × ℝ) := {p | 0 ≤ p.1 ∧ p.1 ≤ t ∧ 0 ≤ p.2 ∧ p.2 ≤ t}

/-- The horizontal offsets `ξ` from the centre at which the point at vertical offset `e` lies in
the closed unit square with `cos θ = P`, `sin θ = Q`.  (`sq_mem_iff_slab` ties this to `sq`.) -/
def slab (P Q e : ℝ) : Set ℝ := {ξ | |ξ * P + e * Q| ≤ 1 / 2 ∧ |e * P - ξ * Q| ≤ 1 / 2}

lemma sq_mem_iff_slab (c : ℝ × ℝ) (θ x e : ℝ) :
    (c.1 + x, c.2 + e) ∈ sq c θ 1 ↔ x ∈ slab (Real.cos θ) (Real.sin θ) e := by
  have h1 : (coord c θ (c.1 + x, c.2 + e)).1 = x * Real.cos θ + e * Real.sin θ := by
    simp only [coord]; ring
  have h2 : (coord c θ (c.1 + x, c.2 + e)).2 = e * Real.cos θ - x * Real.sin θ := by
    simp only [coord]; ring
  simp only [sq, slab, Set.mem_setOf_eq, h1, h2]

/-! ### The two sign symmetries of a slab -/

lemma slab_neg_neg (P Q e : ℝ) : slab (-P) (-Q) e = slab P Q e := by
  ext ξ
  have h1 : ξ * -P + e * -Q = -(ξ * P + e * Q) := by ring
  have h2 : e * -P - ξ * -Q = -(e * P - ξ * Q) := by ring
  simp only [slab, Set.mem_setOf_eq, h1, h2, abs_neg]

lemma slab_neg_snd (P Q e : ℝ) : slab P (-Q) (-e) = slab P Q e := by
  ext ξ
  have h1 : ξ * P + -e * -Q = ξ * P + e * Q := by ring
  have h2 : -e * P - ξ * -Q = -(e * P - ξ * Q) := by ring
  simp only [slab, Set.mem_setOf_eq, h1, h2, abs_neg]

/-! ### The chord bound -/

/-- **The chord bound.**  If `P, Q ≥ 0`, `P² + Q² = 1` and the line's offset `e` from the centre
satisfies `|e| ≤ (P+Q)/2 - PQ`, then the slab contains a closed interval of length `1`: the chord
cut by the line out of the unit square is at least as long as the square's side.

`(P+Q)/2 - PQ` is exactly the largest offset at which the chord still has length `≥ 1`: at
`P = 1, Q = 0` it is `1/2` (the whole square), and at `P = Q = 1/√2` it is `(√2-1)/2`, the constant
in Nagamochi's Lemma 2. -/
lemma exists_unit_interval_subset_slab {P Q e : ℝ} (hP : 0 ≤ P) (hQ : 0 ≤ Q)
    (hPQ : P ^ 2 + Q ^ 2 = 1) (he : |e| ≤ (P + Q) / 2 - P * Q) :
    ∃ x : ℝ, Set.Icc x (x + 1) ⊆ slab P Q e := by
  obtain ⟨he1, he2⟩ := abs_le.mp he
  have hP1 : P ≤ 1 := by nlinarith
  have hQ1 : Q ≤ 1 := by nlinarith
  have hE : e * (P ^ 2 + Q ^ 2) = e := by rw [hPQ]; ring
  rcases eq_or_lt_of_le hQ with hQ0 | hQ0
  · -- `Q = 0`, so `P = 1`: the square is axis-parallel and the slab is the interval `[-1/2, 1/2]`
    have hQ' : Q = 0 := hQ0.symm
    have hP' : P = 1 := by nlinarith
    have he' : |e| ≤ 1 / 2 := by rw [hP', hQ'] at he; simpa using he
    refine ⟨-(1 / 2), fun ξ hξ => ⟨?_, ?_⟩⟩
    · have hval : ξ * P + e * Q = ξ := by rw [hP', hQ']; ring
      rw [hval, abs_le]; exact ⟨by linarith [hξ.1], by linarith [hξ.2]⟩
    · have hval : e * P - ξ * Q = e := by rw [hP', hQ']; ring
      rw [hval]; exact he'
  rcases eq_or_lt_of_le hP with hP0 | hP0
  · -- `P = 0`, so `Q = 1`: the square is at a right angle to the line, and again the slab has
    -- width exactly `1`
    have hP' : P = 0 := hP0.symm
    have hQ' : Q = 1 := by nlinarith
    have he' : |e| ≤ 1 / 2 := by rw [hP', hQ'] at he; simpa using he
    refine ⟨-(1 / 2), fun ξ hξ => ⟨?_, ?_⟩⟩
    · have hval : ξ * P + e * Q = e := by rw [hP', hQ']; ring
      rw [hval]; exact he'
    · have hval : e * P - ξ * Q = -ξ := by rw [hP', hQ']; ring
      rw [hval, abs_neg, abs_le]; exact ⟨by linarith [hξ.1], by linarith [hξ.2]⟩
  -- The generic case `P, Q > 0`.  The slab is the intersection of two strips of widths `1/P` and
  -- `1/Q`; its left endpoint is the larger of the two strips' left endpoints.
  set x := max ((-(1 / 2) - e * Q) / P) ((e * P - 1 / 2) / Q) with hxdef
  have hxa : -(1 / 2) - e * Q ≤ x * P := by
    have h := le_max_left ((-(1 / 2) - e * Q) / P) ((e * P - 1 / 2) / Q)
    rw [← hxdef, div_le_iff₀ hP0] at h; linarith
  have hxb : e * P - 1 / 2 ≤ x * Q := by
    have h := le_max_right ((-(1 / 2) - e * Q) / P) ((e * P - 1 / 2) / Q)
    rw [← hxdef, div_le_iff₀ hQ0] at h; linarith
  refine ⟨x, fun ξ hξ => ?_⟩
  obtain ⟨hl, hu⟩ := hξ
  have hlP : x * P ≤ ξ * P := mul_le_mul_of_nonneg_right hl hP
  have hlQ : x * Q ≤ ξ * Q := mul_le_mul_of_nonneg_right hl hQ
  have huP : ξ * P ≤ x * P + P := by nlinarith [mul_le_mul_of_nonneg_right hu hP]
  have huQ : ξ * Q ≤ x * Q + Q := by nlinarith [mul_le_mul_of_nonneg_right hu hQ]
  rcases max_cases ((-(1 / 2) - e * Q) / P) ((e * P - 1 / 2) / Q) with ⟨hx, -⟩ | ⟨hx, -⟩
  · -- the first strip binds on the left; the second must then not bind too early on the right,
    -- which is exactly `-e ≤ (P+Q)/2 - PQ`
    have hxP : x * P = -(1 / 2) - e * Q := by
      rw [← hxdef] at hx; rw [hx]; field_simp
    have hxQ : x * Q ≤ e * P + 1 / 2 - Q := by
      rw [← hxdef] at hx
      rw [hx, div_mul_eq_mul_div, div_le_iff₀ hP0]
      nlinarith
    exact ⟨abs_le.mpr ⟨by linarith, by linarith⟩, abs_le.mpr ⟨by linarith, by linarith⟩⟩
  · have hxQ : x * Q = e * P - 1 / 2 := by
      rw [← hxdef] at hx; rw [hx]; field_simp
    have hxP : x * P ≤ 1 / 2 - e * Q - P := by
      rw [← hxdef] at hx
      rw [hx, div_mul_eq_mul_div, div_le_iff₀ hQ0]
      nlinarith
    exact ⟨abs_le.mpr ⟨by linarith, by linarith⟩, abs_le.mpr ⟨by linarith, by linarith⟩⟩

/-! ### From the container to the chord -/

/-- A closed unit square inside `[0,t]^2` has its centre at height at least
`(|cos θ| + |sin θ|)/2`, its own half-height: its lowest vertex is on or above the wall. -/
lemma half_height_le_centre {c : ℝ × ℝ} {θ t : ℝ} (hin : sq c θ 1 ⊆ box t) :
    (|Real.cos θ| + |Real.sin θ|) / 2 ≤ c.2 := by
  have hCS : Real.cos θ ^ 2 + Real.sin θ ^ 2 = 1 := Real.cos_sq_add_sin_sq θ
  set u : ℝ := if 0 ≤ Real.sin θ then -(1 / 2) else 1 / 2 with hu
  set v : ℝ := if 0 ≤ Real.cos θ then -(1 / 2) else 1 / 2 with hv
  have habs : |u| = 1 / 2 ∧ |v| = 1 / 2 := by
    constructor
    · rw [hu]; split_ifs <;> norm_num
    · rw [hv]; split_ifs <;> norm_num
  have hmem : (c.1 + (u * Real.cos θ - v * Real.sin θ),
      c.2 + (u * Real.sin θ + v * Real.cos θ)) ∈ sq c θ 1 := by
    have h1 : (coord c θ (c.1 + (u * Real.cos θ - v * Real.sin θ),
        c.2 + (u * Real.sin θ + v * Real.cos θ))).1
        = u * (Real.cos θ ^ 2 + Real.sin θ ^ 2) := by simp only [coord]; ring
    have h2 : (coord c θ (c.1 + (u * Real.cos θ - v * Real.sin θ),
        c.2 + (u * Real.sin θ + v * Real.cos θ))).2
        = v * (Real.cos θ ^ 2 + Real.sin θ ^ 2) := by simp only [coord]; ring
    exact ⟨by rw [h1, hCS, mul_one]; exact le_of_eq habs.1,
           by rw [h2, hCS, mul_one]; exact le_of_eq habs.2⟩
  have hy : 0 ≤ c.2 + (u * Real.sin θ + v * Real.cos θ) := (hin hmem).2.2.1
  have huS : u * Real.sin θ = -(|Real.sin θ| / 2) := by
    rw [hu]; split_ifs with h
    · rw [abs_of_nonneg h]; ring
    · rw [abs_of_neg (not_le.mp h)]; ring
  have hvC : v * Real.cos θ = -(|Real.cos θ| / 2) := by
    rw [hv]; split_ifs with h
    · rw [abs_of_nonneg h]; ring
    · rw [abs_of_neg (not_le.mp h)]; ring
  rw [huS, hvC] at hy; linarith

/-- **The chord exists.**  A closed unit square inside `[0,t]^2` whose centre is at height at most
`1` meets the line `y = 9/10` in a segment of length at least `1`. -/
lemma exists_chord {c : ℝ × ℝ} {θ t : ℝ} (hin : sq c θ 1 ⊆ box t) (hc : c.2 ≤ 1) :
    ∃ x : ℝ, ∀ y ∈ Set.Icc x (x + 1), ((y, (9 : ℝ) / 10) ∈ sq c θ 1) := by
  have hP : (0 : ℝ) ≤ |Real.cos θ| := abs_nonneg _
  have hQ : (0 : ℝ) ≤ |Real.sin θ| := abs_nonneg _
  have hPQ : |Real.cos θ| ^ 2 + |Real.sin θ| ^ 2 = 1 := by
    rw [sq_abs, sq_abs]; exact Real.cos_sq_add_sin_sq θ
  have hlow : (|Real.cos θ| + |Real.sin θ|) / 2 ≤ c.2 := half_height_le_centre hin
  -- the one-variable inequality: `|9/10 - c.2| ≤ (P+Q)/2 - PQ` whenever `(P+Q)/2 ≤ c.2 ≤ 1`
  have key : |(9 : ℝ) / 10 - c.2| ≤ (|Real.cos θ| + |Real.sin θ|) / 2
      - |Real.cos θ| * |Real.sin θ| := by
    set P := |Real.cos θ|
    set Q := |Real.sin θ|
    have hu2 : (P + Q) ^ 2 ≤ 2 := by nlinarith [sq_nonneg (P - Q)]
    have hu1 : 1 ≤ P + Q := by nlinarith [mul_nonneg hP hQ]
    have hub : P + Q ≤ 1415 / 1000 := by nlinarith
    have hprod : 0 ≤ (P + Q - 1) * (1415 / 1000 - (P + Q)) :=
      mul_nonneg (by linarith) (by linarith)
    rw [abs_le]
    constructor <;> nlinarith
  -- transport the slab bound through the two sign symmetries
  have hslab : ∃ x : ℝ,
      Set.Icc x (x + 1) ⊆ slab (Real.cos θ) (Real.sin θ) ((9 : ℝ) / 10 - c.2) := by
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
  have hmem := (sq_mem_iff_slab c θ (y - c.1) ((9 : ℝ) / 10 - c.2)).mpr (hx hy')
  have e1 : c.1 + (y - c.1) = y := by ring
  have e2 : c.2 + ((9 : ℝ) / 10 - c.2) = (9 : ℝ) / 10 := by ring
  rwa [e1, e2] at hmem

/-! ### The counting step -/

/-- Four points of `[0,3]` cannot be pairwise more than `1` apart. -/
lemma no_four_spread {N : ℕ} (hN : 3 < N) (x : Fin N → ℝ)
    (hrange : ∀ i, x i ∈ Set.Icc (0 : ℝ) 3)
    (hgap : ∀ i j, i ≠ j → 1 < |x i - x j|) : False := by
  have habs : ∀ u v : ℝ, 1 < |u - v| → 1 < u - v ∨ 1 < v - u := by
    intro u v h
    rcases abs_cases (u - v) with ⟨he, -⟩ | ⟨he, -⟩
    · exact Or.inl (he ▸ h)
    · exact Or.inr (by rw [he] at h; linarith)
  have n01 : (⟨0, by omega⟩ : Fin N) ≠ ⟨1, by omega⟩ := by simp [Fin.ext_iff]
  have n02 : (⟨0, by omega⟩ : Fin N) ≠ ⟨2, by omega⟩ := by simp [Fin.ext_iff]
  have n03 : (⟨0, by omega⟩ : Fin N) ≠ ⟨3, by omega⟩ := by simp [Fin.ext_iff]
  have n12 : (⟨1, by omega⟩ : Fin N) ≠ ⟨2, by omega⟩ := by simp [Fin.ext_iff]
  have n13 : (⟨1, by omega⟩ : Fin N) ≠ ⟨3, by omega⟩ := by simp [Fin.ext_iff]
  have n23 : (⟨2, by omega⟩ : Fin N) ≠ ⟨3, by omega⟩ := by simp [Fin.ext_iff]
  have r0 := hrange ⟨0, by omega⟩
  have r1 := hrange ⟨1, by omega⟩
  have r2 := hrange ⟨2, by omega⟩
  have r3 := hrange ⟨3, by omega⟩
  rcases habs _ _ (hgap _ _ n01) with h01 | h01 <;>
    rcases habs _ _ (hgap _ _ n02) with h02 | h02 <;>
    rcases habs _ _ (hgap _ _ n03) with h03 | h03 <;>
    rcases habs _ _ (hgap _ _ n12) with h12 | h12 <;>
    rcases habs _ _ (hgap _ _ n13) with h13 | h13 <;>
    rcases habs _ _ (hgap _ _ n23) with h23 | h23 <;>
    linarith [r0.1, r0.2, r1.1, r1.2, r2.1, r2.2, r3.1, r3.2]

/-- **The chord lemma.**  In a container `[0,t]^2` with `t ≤ 4`, at most three closed unit squares
that are pairwise disjoint *as closed sets* have their centre within distance `1` of the bottom
wall.  The other three walls follow by the symmetries of the container. -/
theorem wall_strip_le_three {N : ℕ} {t : ℝ} (ht : t ≤ 4)
    (ctr : Fin N → ℝ × ℝ) (ang : Fin N → ℝ)
    (hin : ∀ i, sq (ctr i) (ang i) 1 ⊆ box t)
    (hstrip : ∀ i, (ctr i).2 ≤ 1)
    (hdisj : ∀ i j, i ≠ j → Disjoint (sq (ctr i) (ang i) 1) (sq (ctr j) (ang j) 1)) :
    N ≤ 3 := by
  by_contra hN
  push_neg at hN
  choose x hx using fun i => exists_chord (hin i) (hstrip i)
  -- each chord lies in `[0, t]`, so its left endpoint lies in `[0, t - 1] ⊆ [0, 3]`
  have hrange : ∀ i, x i ∈ Set.Icc (0 : ℝ) 3 := by
    intro i
    have h0 := hin i (hx i (x i) ⟨le_rfl, by linarith⟩)
    have h1 := hin i (hx i (x i + 1) ⟨by linarith, le_rfl⟩)
    exact ⟨h0.1, by have h := h1.2.1; simp only at h ⊢; linarith⟩
  -- disjoint squares give disjoint chords, so the left endpoints are more than `1` apart
  have hgap : ∀ i j, i ≠ j → 1 < |x i - x j| := by
    intro i j hij
    by_contra hle
    push_neg at hle
    rw [abs_le] at hle
    rcases le_total (x i) (x j) with h | h
    · exact (Set.disjoint_left.mp (hdisj i j hij)
        (hx i (x j) ⟨h, by linarith [hle.2]⟩)) (hx j (x j) ⟨le_rfl, by linarith⟩)
    · exact (Set.disjoint_left.mp (hdisj i j hij)
        (hx i (x i) ⟨le_rfl, by linarith⟩)) (hx j (x i) ⟨h, by linarith [hle.1]⟩)
  exact no_four_spread hN x hrange hgap

/-- **The chord lemma, packing form.**  In a packing of squares of side `L > 1` with pairwise
disjoint interiors inside `[0,t]^2`, `t ≤ 4`, at most three have their centre within distance `1`
of a given wall.  This is the form the branch tree uses: a packing of unit squares in a container
of side `s' < t` rescales to squares of side `L = t/s' > 1` in `[0,t]^2`, and the concentric
closed unit squares are then pairwise disjoint. -/
theorem wall_strip_le_three_of_packing {N : ℕ} {t L : ℝ} (ht : t ≤ 4) (hL : 1 < L)
    (ctr : Fin N → ℝ × ℝ) (ang : Fin N → ℝ)
    (hin : ∀ i, sq (ctr i) (ang i) L ⊆ box t)
    (hstrip : ∀ i, (ctr i).2 ≤ 1)
    (hdisj : ∀ i j, i ≠ j → Disjoint (sqInt (ctr i) (ang i) L) (sqInt (ctr j) (ang j) L)) :
    N ≤ 3 := by
  have hIntSub : ∀ (c : ℝ × ℝ) (θ : ℝ), sqInt c θ L ⊆ sq c θ L := by
    rintro c θ p ⟨h1, h2⟩; exact ⟨le_of_lt h1, le_of_lt h2⟩
  refine wall_strip_le_three ht ctr ang (fun i => ?_) hstrip (fun i j hij => ?_)
  · exact subset_trans (subset_trans (unit_subset_interior hL) (hIntSub _ _)) (hin i)
  · exact Set.disjoint_of_subset (unit_subset_interior hL) (unit_subset_interior hL) (hdisj i j hij)

end SquarePacking
