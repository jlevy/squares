import Sqpack.ZeroMargin

/-!
# The D4 reduction

A weighted cover of `box m = [0,m]²` that is invariant under the symmetry group `D4` of the square
needs to be checked only on the **fundamental region**: centres in `[0,m/2]²` and angles
`θ ∈ [0, π/4]` (`search/S32_EXACT.md` §7 and §11.3(d)).  This is what `zmcheck --d4` and
`zeromargin.py`'s D4 mode rely on.

* `sq_add_pi_div_two` — `sq c (θ + π/2) 1 = sq c θ 1`: the axis square is invariant under the
  quarter turn, so the angle only matters mod `π/2`.
* `mem_sq_reflX`, `mem_sq_swapXY` — the two generators `x ↦ m − x` and `x ↔ y` map
  `sq c θ 1` onto `sq (g c) (−θ) 1`.
* `sq_subset_box_reflX_iff`, `sq_subset_box_swapXY_iff` — both preserve containment in `box m`.
* `capt_reflX`, `capt_swapXY`, `capt_add_pi_div_two` — and, for a `D4Inv` weight, the captured
  weight.
* `d4_reduce` — the pure pose bookkeeping: a pose predicate invariant under these three moves
  and true on the fundamental region is true at every centre in `box m`.
* **`d4_reduction`** — the cover statement, in the form `packing_le_weight`'s `hcover` takes.
* **`d4_reduction_u`** — the same with the fundamental region written as the checkers' root domain:
  `θ = 2 arctan u`, `u ∈ [0, 1/2]` (which contains `[0°, 45°]`, as `u ≤ √2 − 1 < 1/2` there).

Only the generators `x ↦ m − x` and `x ↔ y` enter the invariance hypothesis `D4Inv`; the other six
elements of `D4` are products of them, and the proof composes the two generator lemmas.
-/

open Finset
open scoped Classical

namespace SquarePacking

/-- The reflection `x ↦ m − x` of `[0,m]²`. -/
def reflX (m : ℝ) (p : ℝ × ℝ) : ℝ × ℝ := (m - p.1, p.2)

/-- The diagonal reflection `x ↔ y`. -/
def swapXY (p : ℝ × ℝ) : ℝ × ℝ := (p.2, p.1)

lemma reflX_reflX (m : ℝ) (p : ℝ × ℝ) : reflX m (reflX m p) = p := by
  simp [reflX]

lemma swapXY_swapXY (p : ℝ × ℝ) : swapXY (swapXY p) = p := rfl

/-- The captured weight of a pose: the total weight of the points in the closed unit square. -/
noncomputable def capt (A : Finset (ℝ × ℝ)) (w : ℝ × ℝ → ℝ) (c : ℝ × ℝ) (θ : ℝ) : ℝ :=
  ∑ a ∈ A.filter (fun a => a ∈ sq c θ 1), w a

/-- **D4 invariance** of a weighted point set, on the two generators of `D4`: the points are
mapped into the set, with the same weight, by `x ↦ m − x` and by `x ↔ y`.  (Since both are
involutions, they then permute the set.)  This is what `Checker.symmetric_d4` and `zmcheck --d4`
check exactly on the aggregated weight map. -/
def D4Inv (m : ℝ) (A : Finset (ℝ × ℝ)) (w : ℝ × ℝ → ℝ) : Prop :=
  ∀ a ∈ A, (reflX m a ∈ A ∧ w (reflX m a) = w a) ∧ (swapXY a ∈ A ∧ w (swapXY a) = w a)

/-! ## 1.  How the three moves act on a closed unit square -/

/-- The quarter turn about the centre fixes the axis square, so `θ` matters only mod `π/2`. -/
lemma sq_add_pi_div_two (c : ℝ × ℝ) (θ L : ℝ) : sq c (θ + Real.pi / 2) L = sq c θ L := by
  ext p
  simp only [sq, Set.mem_ofPred_eq]
  have h1 : (coord c (θ + Real.pi / 2) p).1 = (coord c θ p).2 := by
    simp only [coord, Real.cos_add_pi_div_two, Real.sin_add_pi_div_two]; ring
  have h2 : (coord c (θ + Real.pi / 2) p).2 = -(coord c θ p).1 := by
    simp only [coord, Real.cos_add_pi_div_two, Real.sin_add_pi_div_two]; ring
  rw [h1, h2, abs_neg, and_comm]

/-- `x ↦ m − x` maps `sq c θ 1` onto `sq (reflX m c) (−θ) 1`. -/
lemma mem_sq_reflX (m : ℝ) (c : ℝ × ℝ) (θ : ℝ) (p : ℝ × ℝ) :
    reflX m p ∈ sq (reflX m c) (-θ) 1 ↔ p ∈ sq c θ 1 := by
  simp only [sq, Set.mem_ofPred_eq]
  have h1 : (coord (reflX m c) (-θ) (reflX m p)).1 = -(coord c θ p).1 := by
    simp only [coord, reflX, Real.cos_neg, Real.sin_neg]; ring
  have h2 : (coord (reflX m c) (-θ) (reflX m p)).2 = (coord c θ p).2 := by
    simp only [coord, reflX, Real.cos_neg, Real.sin_neg]; ring
  rw [h1, h2, abs_neg]

/-- `x ↔ y` maps `sq c θ 1` onto `sq (swapXY c) (−θ) 1`. -/
lemma mem_sq_swapXY (c : ℝ × ℝ) (θ : ℝ) (p : ℝ × ℝ) :
    swapXY p ∈ sq (swapXY c) (-θ) 1 ↔ p ∈ sq c θ 1 := by
  simp only [sq, Set.mem_ofPred_eq]
  have h1 : (coord (swapXY c) (-θ) (swapXY p)).1 = (coord c θ p).2 := by
    simp only [coord, swapXY, Real.cos_neg, Real.sin_neg]; ring
  have h2 : (coord (swapXY c) (-θ) (swapXY p)).2 = (coord c θ p).1 := by
    simp only [coord, swapXY, Real.cos_neg, Real.sin_neg]; ring
  rw [h1, h2, and_comm]

lemma wid_neg (θ : ℝ) : wid (-θ) = wid θ := by
  simp [wid, Real.cos_neg, Real.sin_neg, abs_neg]

/-- `x ↦ m − x` preserves containment in `box m`. -/
lemma sq_subset_box_reflX_iff (m : ℝ) (c : ℝ × ℝ) (θ : ℝ) :
    sq (reflX m c) (-θ) 1 ⊆ box m ↔ sq c θ 1 ⊆ box m := by
  rw [sq_subset_box_iff, sq_subset_box_iff]
  simp only [Adm, reflX, wid_neg]
  constructor
  · rintro ⟨h1, h2, h3, h4⟩; exact ⟨by linarith, by linarith, h3, h4⟩
  · rintro ⟨h1, h2, h3, h4⟩; exact ⟨by linarith, by linarith, h3, h4⟩

/-- `x ↔ y` preserves containment in `box m`. -/
lemma sq_subset_box_swapXY_iff (m : ℝ) (c : ℝ × ℝ) (θ : ℝ) :
    sq (swapXY c) (-θ) 1 ⊆ box m ↔ sq c θ 1 ⊆ box m := by
  rw [sq_subset_box_iff, sq_subset_box_iff]
  simp only [Adm, swapXY, wid_neg]
  constructor
  · rintro ⟨h1, h2, h3, h4⟩; exact ⟨h3, h4, h1, h2⟩
  · rintro ⟨h1, h2, h3, h4⟩; exact ⟨h3, h4, h1, h2⟩

/-- An involution that maps a weighted set into itself preserving weights, and carries `S` onto
`S'`, preserves the captured weight. -/
lemma sum_filter_invol (A : Finset (ℝ × ℝ)) (w : ℝ × ℝ → ℝ) (g : ℝ × ℝ → ℝ × ℝ)
    (hg : ∀ p, g (g p) = p) (hA : ∀ a ∈ A, g a ∈ A ∧ w (g a) = w a)
    (S S' : Set (ℝ × ℝ)) (hS : ∀ p, g p ∈ S' ↔ p ∈ S) :
    ∑ a ∈ A.filter (fun a => a ∈ S'), w a = ∑ a ∈ A.filter (fun a => a ∈ S), w a := by
  refine Finset.sum_nbij' g g ?_ ?_ ?_ ?_ ?_
  · intro a ha
    simp only [Finset.mem_filter] at ha ⊢
    refine ⟨(hA a ha.1).1, ?_⟩
    rw [← hS, hg]; exact ha.2
  · intro a ha
    simp only [Finset.mem_filter] at ha ⊢
    exact ⟨(hA a ha.1).1, (hS a).mpr ha.2⟩
  · intro a _; exact hg a
  · intro a _; exact hg a
  · intro a ha
    simp only [Finset.mem_filter] at ha
    exact ((hA a ha.1).2).symm

lemma capt_reflX {m : ℝ} {A : Finset (ℝ × ℝ)} {w : ℝ × ℝ → ℝ} (hinv : D4Inv m A w)
    (c : ℝ × ℝ) (θ : ℝ) : capt A w (reflX m c) (-θ) = capt A w c θ :=
  sum_filter_invol A w (reflX m) (reflX_reflX m) (fun a ha => (hinv a ha).1) _ _
    (mem_sq_reflX m c θ)

lemma capt_swapXY {m : ℝ} {A : Finset (ℝ × ℝ)} {w : ℝ × ℝ → ℝ} (hinv : D4Inv m A w)
    (c : ℝ × ℝ) (θ : ℝ) : capt A w (swapXY c) (-θ) = capt A w c θ :=
  sum_filter_invol A w swapXY swapXY_swapXY (fun a ha => (hinv a ha).2) _ _
    (mem_sq_swapXY c θ)

lemma capt_add_pi_div_two (A : Finset (ℝ × ℝ)) (w : ℝ × ℝ → ℝ) (c : ℝ × ℝ) (θ : ℝ) :
    capt A w c (θ + Real.pi / 2) = capt A w c θ := by
  simp only [capt, sq_add_pi_div_two]

/-! ## 2.  The pose bookkeeping -/

/-- **Every pose reduces into the fundamental region.**  A predicate on poses that is invariant
under `θ ↦ θ + π/2`, under `(c, θ) ↦ (reflX m c, −θ)` and under `(c, θ) ↦ (swapXY c, −θ)`, and
holds for centres in `[0,m/2]²` and `θ ∈ [0, π/4]`, holds for every centre in `box m` and every
`θ`.  (`S32_EXACT.md` §11.3(d), step (4).) -/
theorem d4_reduce (m : ℝ) (P : ℝ × ℝ → ℝ → Prop)
    (hper : ∀ c θ, P c (θ + Real.pi / 2) ↔ P c θ)
    (hX : ∀ c θ, P c θ → P (reflX m c) (-θ))
    (hS : ∀ c θ, P c θ → P (swapXY c) (-θ))
    (hreg : ∀ (c : ℝ × ℝ) (θ : ℝ), c.1 ∈ Set.Icc 0 (m / 2) → c.2 ∈ Set.Icc 0 (m / 2) →
      θ ∈ Set.Icc 0 (Real.pi / 4) → P c θ) :
    ∀ c ∈ box m, ∀ θ, P c θ := by
  have hpi : 0 < Real.pi / 2 := by positivity
  -- the quarter turn `(x, y) ↦ (m − y, x)` = `reflX ∘ swapXY` keeps `θ`
  have hrot : ∀ c θ, P c θ → P (m - c.2, c.1) θ := by
    intro c θ h
    have := hX _ _ (hS c θ h)
    simpa [reflX, swapXY, neg_neg] using this
  -- step B: `θ ∈ [0, π/4]`, centre anywhere in the box (the four quarter turns)
  have hB : ∀ c ∈ box m, ∀ θ ∈ Set.Icc 0 (Real.pi / 4), P c θ := by
    rintro ⟨x, y⟩ ⟨hx0, hxm, hy0, hym⟩ θ hθ
    simp only at hx0 hxm hy0 hym
    rcases le_or_gt x (m / 2) with hx | hx <;> rcases le_or_gt y (m / 2) with hy | hy
    · exact hreg _ _ ⟨hx0, hx⟩ ⟨hy0, hy⟩ hθ
    · -- `(x, y) = rot³ (m − y, x)`
      have h := hrot _ _ (hrot _ _ (hrot _ _
        (hreg (m - y, x) θ ⟨by linarith, by linarith⟩ ⟨hx0, hx⟩ hθ)))
      have e : (m - (m - (m - (m - y, x).2, (m - y, x).1).2,
          (m - (m - y, x).2, (m - y, x).1).1).2,
          (m - (m - (m - y, x).2, (m - y, x).1).2, (m - (m - y, x).2, (m - y, x).1).1).1)
          = (x, y) := by
        ext <;> simp
      rwa [e] at h
    · -- `(x, y) = rot (y, m − x)`
      have h := hrot _ _ (hreg (y, m - x) θ ⟨hy0, hy⟩ ⟨by linarith, by linarith⟩ hθ)
      have e : (m - (y, m - x).2, (y, m - x).1) = (x, y) := by ext <;> simp
      rwa [e] at h
    · -- `(x, y) = rot² (m − x, m − y)`
      have h := hrot _ _ (hrot _ _
        (hreg (m - x, m - y) θ ⟨by linarith, by linarith⟩ ⟨by linarith, by linarith⟩ hθ))
      have e : (m - (m - (m - x, m - y).2, (m - x, m - y).1).2,
          (m - (m - x, m - y).2, (m - x, m - y).1).1) = (x, y) := by ext <;> simp
      rwa [e] at h
  -- step C: `θ ∈ [0, π/2)`, via `x ↦ m − x` when `θ > π/4`
  have hC : ∀ c ∈ box m, ∀ θ ∈ Set.Ico 0 (Real.pi / 2), P c θ := by
    intro c hc θ hθ
    rcases le_or_gt θ (Real.pi / 4) with h | h
    · exact hB c hc θ ⟨hθ.1, h⟩
    · have hc' : reflX m c ∈ box m := by
        obtain ⟨h1, h2, h3, h4⟩ := hc
        exact ⟨by simp [reflX]; linarith, by simp [reflX]; linarith, h3, h4⟩
      have h1 := hX _ _ (hB (reflX m c) hc' (Real.pi / 2 - θ)
        ⟨by linarith [hθ.2], by linarith⟩)
      rw [reflX_reflX] at h1
      have h2 := (hper c (-(Real.pi / 2 - θ))).mpr h1
      have e : -(Real.pi / 2 - θ) + Real.pi / 2 = θ := by ring
      rwa [e] at h2
  -- step D: any `θ`, reduced mod `π/2`
  have hZ : ∀ (k : ℤ) c θ, P c (θ + k * (Real.pi / 2)) ↔ P c θ := by
    intro k
    induction k using Int.induction_on with
    | zero => intro c θ; simp
    | succ k ih =>
      intro c θ
      have e : θ + ((k : ℤ) + 1 : ℤ) * (Real.pi / 2) = (θ + k * (Real.pi / 2)) + Real.pi / 2 := by
        push_cast; ring
      have := ih c θ
      push_cast at this
      rw [e, hper, this]
    | pred k ih =>
      intro c θ
      rw [← hper]
      have e : θ + ((-(k : ℤ) - 1 : ℤ) : ℝ) * (Real.pi / 2) + Real.pi / 2
          = θ + ((-(k : ℤ) : ℤ) : ℝ) * (Real.pi / 2) := by
        push_cast; ring
      rw [e, ih]
  intro c hc θ
  have hmem := toIcoMod_mem_Ico' hpi θ
  have heq := toIcoMod_add_toIcoDiv_zsmul hpi 0 θ
  have h := (hZ (toIcoDiv hpi 0 θ) c (toIcoMod hpi 0 θ)).mpr (hC c hc _ hmem)
  rwa [← zsmul_eq_mul, heq] at h

/-! ## 3.  The reduction for weighted covers -/

/-- The centre of a closed unit square lies in it. -/
lemma mem_sq_self (c : ℝ × ℝ) (θ : ℝ) : c ∈ sq c θ 1 := by
  simp [sq, coord]

/-- **D4 reduction.**  Let the weighted point set `(A, w)` be invariant under `x ↦ m − x` and
`x ↔ y` (hence under all of `D4`).  If every closed unit square inside `box m` with centre in
`[0,m/2]²` and angle `θ ∈ [0, π/4]` captures weight `≥ 1`, then every closed unit square inside
`box m` does.  The conclusion is exactly the `hcover` hypothesis of `packing_le_weight` with
`C = box m`. -/
theorem d4_reduction (m : ℝ) (A : Finset (ℝ × ℝ)) (w : ℝ × ℝ → ℝ) (hinv : D4Inv m A w)
    (hreg : ∀ (c : ℝ × ℝ) (θ : ℝ), c.1 ∈ Set.Icc 0 (m / 2) → c.2 ∈ Set.Icc 0 (m / 2) →
      θ ∈ Set.Icc 0 (Real.pi / 4) → sq c θ 1 ⊆ box m →
        1 ≤ ∑ a ∈ A.filter (fun a => a ∈ sq c θ 1), w a) :
    ∀ (c : ℝ × ℝ) (θ : ℝ), sq c θ 1 ⊆ box m →
      1 ≤ ∑ a ∈ A.filter (fun a => a ∈ sq c θ 1), w a := by
  let P : ℝ × ℝ → ℝ → Prop := fun c θ => sq c θ 1 ⊆ box m → 1 ≤ capt A w c θ
  have hP : ∀ c ∈ box m, ∀ θ, P c θ := by
    refine d4_reduce m P ?_ ?_ ?_ ?_
    · intro c θ
      simp only [P, sq_add_pi_div_two, capt_add_pi_div_two]
    · intro c θ h hsub
      rw [capt_reflX hinv]
      exact h ((sq_subset_box_reflX_iff m c θ).mp hsub)
    · intro c θ h hsub
      rw [capt_swapXY hinv]
      exact h ((sq_subset_box_swapXY_iff m c θ).mp hsub)
    · intro c θ h1 h2 h3 hsub
      exact hreg c θ h1 h2 h3 hsub
  intro c θ hsub
  exact hP c (hsub (mem_sq_self c θ)) θ hsub

/-- For `θ ∈ [0, π/4]`, `u = tan(θ/2)` satisfies `θ = 2 arctan u` and `0 ≤ u ≤ 1/2`
(in fact `u ≤ √2 − 1`). -/
lemma exists_u_of_theta {θ : ℝ} (hθ : θ ∈ Set.Icc 0 (Real.pi / 4)) :
    ∃ u ∈ Set.Icc (0 : ℝ) (1 / 2), 2 * Real.arctan u = θ := by
  obtain ⟨h0, h1⟩ := hθ
  have hpi := Real.pi_pos
  refine ⟨Real.tan (θ / 2), ⟨?_, ?_⟩, ?_⟩
  · apply Real.tan_nonneg_of_nonneg_of_le_pi_div_two <;> linarith
  · -- `cos θ ≥ sin θ` on `[0, π/4]`, i.e. `1 − u² ≥ 2u`
    set u := Real.tan (θ / 2) with hu
    have he : 2 * Real.arctan u = θ := by
      rw [hu, Real.arctan_tan (by linarith) (by linarith)]; ring
    have hs : Real.sin θ ≤ Real.sin (Real.pi / 4) :=
      Real.sin_le_sin_of_le_of_le_pi_div_two (by linarith) (by linarith) h1
    have hc : Real.cos (Real.pi / 4) ≤ Real.cos θ :=
      Real.cos_le_cos_of_nonneg_of_le_pi h0 (by linarith) h1
    rw [Real.sin_pi_div_four] at hs
    rw [Real.cos_pi_div_four] at hc
    rw [← he, sin_two_arctan, cos_two_arctan] at *
    have hN : (0 : ℝ) < 1 + u ^ 2 := by positivity
    have key : 2 * u ≤ 1 - u ^ 2 := by
      have := le_trans hs hc
      rwa [div_le_div_iff_of_pos_right hN] at this
    nlinarith
  · rw [Real.arctan_tan (by linarith) (by linarith)]; ring

/-- **D4 reduction, in the checkers' coordinates.**  The fundamental region as `zeromargin.py`
and `zmcheck --d4` cover it: centres in `[0,m/2]²`, `θ = 2 arctan u` with `u ∈ [0, 1/2]`
(the root boxes `[0,m/2]² × [0,½]`).  This hypothesis is stronger than `d4_reduction`'s (it
asks for `θ` up to `2 arctan ½ ≈ 53.13°`), so this is a corollary. -/
theorem d4_reduction_u (m : ℝ) (A : Finset (ℝ × ℝ)) (w : ℝ × ℝ → ℝ) (hinv : D4Inv m A w)
    (hreg : ∀ (c : ℝ × ℝ) (u : ℝ), c.1 ∈ Set.Icc 0 (m / 2) → c.2 ∈ Set.Icc 0 (m / 2) →
      u ∈ Set.Icc 0 (1 / 2) → sq c (2 * Real.arctan u) 1 ⊆ box m →
        1 ≤ ∑ a ∈ A.filter (fun a => a ∈ sq c (2 * Real.arctan u) 1), w a) :
    ∀ (c : ℝ × ℝ) (θ : ℝ), sq c θ 1 ⊆ box m →
      1 ≤ ∑ a ∈ A.filter (fun a => a ∈ sq c θ 1), w a := by
  refine d4_reduction m A w hinv fun c θ h1 h2 hθ hsub => ?_
  obtain ⟨u, hu, rfl⟩ := exists_u_of_theta hθ
  exact hreg c u h1 h2 hu hsub

end SquarePacking
