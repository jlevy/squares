import Sqpack.SquareArea
import Sqpack.CovMP
import Sqpack.D4
import Sqpack.LemmaEPoly

/-!
# Lemma K (caps of the Lebesgue rectangle paid by the segments on its sides)

A closed unit square `Q` with centre right of the line `x = a` loses at most `d · len(a)` of area
left of the line (`SqArea.cap_le_chord`, `d = a − x_min`), where `len(a)` is the chord of `Q` on the
line.  If the cover's pieces on `x = a` cover the chord with density (weight per length) at least
`ρ`, they put at least `ρ · len(a)` of mass in `Q`.  So `w · d ≤ ρ` (the rectangle's weight `w` per
area) pays for the cap.  With the same on `y = a`, a square inside `{x ≤ b, y ≤ b}` has mass at
least the rectangle's weight (`QUADRANT_EXACT.md` §4.2, Lemma K).

Here: the chord range (`chord_mem`), the mass of a vertical piece (`segFrac_vert_ge`), and a chain of
contiguous pieces (`chain_mass_ge`).
-/

open MeasureTheory Set

namespace SquarePacking

namespace CapK

open SqArea

section chord

variable {c : ℝ × ℝ} {θ : ℝ}

/-- The ends of the chord of `Q` on the line `x = a`. -/
noncomputable def lo (c : ℝ × ℝ) (θ a : ℝ) : ℝ := max (lowX c θ a) (lowY c θ a)
noncomputable def hi (c : ℝ × ℝ) (θ a : ℝ) : ℝ := min (upX c θ a) (upY c θ a)

lemma len_eq (a : ℝ) : len c θ a = hi c θ a - lo c θ a := rfl

/-- **The chord range**: on `x = a = x_min + d`, the chord lies within `[y_TL − (cos/sin) d,
y_TL + (sin/cos) d]`, `y_TL = c_y + (cos − sin)/2` (the leftmost vertex), and within
`[c_y − (cos + sin)/2, c_y + (cos + sin)/2]`. -/
lemma hi_le (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ) (a : ℝ) :
    hi c θ a ≤ c.2 + (Real.cos θ - Real.sin θ) / 2 + Real.sin θ / Real.cos θ * (a - xmin c θ) := by
  refine (min_le_right _ _).trans (le_of_eq ?_)
  have h1 : Real.cos θ ^ 2 + Real.sin θ ^ 2 = 1 := by rw [add_comm]; exact Real.sin_sq_add_cos_sq θ
  simp only [upY, xmin]
  field_simp
  nlinarith [h1]

lemma lo_ge (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ) (a : ℝ) :
    c.2 + (Real.cos θ - Real.sin θ) / 2 - Real.cos θ / Real.sin θ * (a - xmin c θ) ≤ lo c θ a := by
  refine le_trans (le_of_eq ?_) (le_max_left _ _)
  have h1 : Real.cos θ ^ 2 + Real.sin θ ^ 2 = 1 := by rw [add_comm]; exact Real.sin_sq_add_cos_sq θ
  simp only [lowX, xmin]
  field_simp
  nlinarith [h1]

end chord

section piece

variable {c : ℝ × ℝ} {θ : ℝ}

/-- The overlap of `[p0, p1]` with the chord, nonnegative. -/
noncomputable def ovl (c : ℝ × ℝ) (θ a p0 p1 : ℝ) : ℝ := max 0 (min p1 (hi c θ a) - max p0 (lo c θ a))

/-- **A vertical piece** `[(a, p0), (a, p1)]` puts at least its overlap with the chord, over its
length, of its weight in `Q`. -/
lemma segFrac_vert_ge (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ) {a p0 p1 : ℝ} (hp : p0 < p1) :
    ovl c θ a p0 p1 / (p1 - p0) ≤ segFrac (a, p0) (a, p1) (sq c θ 1) := by
  have hL : 0 < p1 - p0 := by linarith
  set t0 := max 0 ((lo c θ a - p0) / (p1 - p0))
  set t1 := min 1 ((hi c θ a - p0) / (p1 - p0))
  have hsub : Icc t0 t1 ⊆ segPt (a, p0) (a, p1) ⁻¹' sq c θ 1 ∩ Icc (0 : ℝ) 1 := by
    rintro t ⟨h0, h1⟩
    have ht0 : 0 ≤ t := (le_max_left _ _).trans h0
    have ht1 : t ≤ 1 := h1.trans (min_le_left _ _)
    have hlo : (lo c θ a - p0) / (p1 - p0) ≤ t := (le_max_right _ _).trans h0
    have hhi : t ≤ (hi c θ a - p0) / (p1 - p0) := h1.trans (min_le_right _ _)
    rw [div_le_iff₀ hL] at hlo
    rw [le_div_iff₀ hL] at hhi
    refine ⟨?_, ht0, ht1⟩
    simp only [mem_preimage, segPt, sub_self, mul_zero, add_zero]
    rw [mem_sq_iff_slice hs hc]
    exact ⟨by simp only [lo] at hlo; linarith, by simp only [hi] at hhi; linarith⟩
  have hvol := measure_mono (μ := volume) hsub
  rw [Real.volume_Icc] at hvol
  have hfin : volume (segPt (a, p0) (a, p1) ⁻¹' sq c θ 1 ∩ Icc (0 : ℝ) 1) ≠ ⊤ :=
    ne_top_of_le_ne_top (by simp [Real.volume_Icc]) (measure_mono inter_subset_right)
  have key : max 0 (t1 - t0) ≤ segFrac (a, p0) (a, p1) (sq c θ 1) := by
    unfold segFrac
    rcases le_total t1 t0 with h | h
    · rw [max_eq_left (by linarith)]; exact ENNReal.toReal_nonneg
    · rw [max_eq_right (by linarith)]
      calc t1 - t0 = (ENNReal.ofReal (t1 - t0)).toReal := (ENNReal.toReal_ofReal (by linarith)).symm
        _ ≤ _ := ENNReal.toReal_mono hfin hvol
  refine le_trans ?_ key
  have a1 : (min p1 (hi c θ a) - p0) / (p1 - p0) ≤ t1 :=
    le_min (by rw [div_le_one hL]; linarith [min_le_left p1 (hi c θ a)])
      (div_le_div_of_nonneg_right (by linarith [min_le_right p1 (hi c θ a)]) hL.le)
  have a2 : t0 ≤ (max p0 (lo c θ a) - p0) / (p1 - p0) :=
    max_le (div_nonneg (by linarith [le_max_left p0 (lo c θ a)]) hL.le)
      (div_le_div_of_nonneg_right (by linarith [le_max_right p0 (lo c θ a)]) hL.le)
  unfold ovl
  rw [div_le_iff₀ hL]
  rcases le_total (min p1 (hi c θ a) - max p0 (lo c θ a)) 0 with h | h
  · rw [max_eq_left h]; positivity
  · rw [max_eq_right h]
    have : (min p1 (hi c θ a) - max p0 (lo c θ a)) / (p1 - p0) ≤ t1 - t0 := by
      have e : (min p1 (hi c θ a) - max p0 (lo c θ a)) / (p1 - p0) =
          (min p1 (hi c θ a) - p0) / (p1 - p0) - (max p0 (lo c θ a) - p0) / (p1 - p0) := by
        rw [← sub_div]; ring_nf
      rw [e]; linarith
    rw [div_le_iff₀ hL] at this
    nlinarith [le_max_right 0 (t1 - t0)]

end piece

section chain

/-- The overlap of `[x, y]` with `[lo, hi]`. -/
noncomputable def ov (lo hi x y : ℝ) : ℝ := max 0 (min y hi - max x lo)

lemma ov_nonneg (lo hi x y : ℝ) : 0 ≤ ov lo hi x y := le_max_left _ _

lemma ov_add {lo hi x m y : ℝ} (h1 : x ≤ m) (h2 : m ≤ y) :
    ov lo hi x y ≤ ov lo hi x m + ov lo hi m y := by
  unfold ov
  have hA := le_max_right 0 (min m hi - max x lo)
  have hB := le_max_right 0 (min y hi - max m lo)
  have hA0 := le_max_left 0 (min m hi - max x lo)
  have hB0 := le_max_left 0 (min y hi - max m lo)
  refine max_le (by linarith) ?_
  rcases lt_or_ge m lo with h | h
  · have e1 : max x lo = lo := max_eq_right (h1.trans h.le)
    have e2 : max m lo = lo := max_eq_right h.le
    simp only [e1, e2] at hA hB hA0 hB0 ⊢; linarith
  · rcases le_or_gt m hi with h' | h'
    · have e1 : min m hi = m := min_eq_left h'
      have e2 : max m lo = m := max_eq_left h
      simp only [e1, e2] at hA hB hA0 hB0 ⊢; linarith
    · have e1 : min m hi = hi := min_eq_right h'.le
      have e2 : min y hi = hi := min_eq_right (h'.le.trans h2)
      simp only [e1, e2] at hA hB hA0 hB0 ⊢; linarith

/-- A chain of intervals starting at `x`: `[x, p₁], [p₁, p₂], …`. -/
def ChainFrom : ℝ → List (ℝ × ℝ) → Prop
  | _, [] => True
  | x, p :: l => p.1 = x ∧ p.1 ≤ p.2 ∧ ChainFrom p.2 l

/-- Its end. -/
def endOf : ℝ → List (ℝ × ℝ) → ℝ
  | x, [] => x
  | _, p :: l => endOf p.2 l

lemma le_endOf : ∀ (l : List (ℝ × ℝ)) (x : ℝ), ChainFrom x l → x ≤ endOf x l
  | [], x, _ => le_rfl
  | p :: l, x, ⟨h1, h2, h3⟩ => by
    simp only [endOf]; have := le_endOf l p.2 h3; rw [← h1]; linarith

/-- **The pieces of a chain overlap `[lo, hi]` at least as much as the whole chain does.** -/
lemma ov_chain (lo hi : ℝ) : ∀ (l : List (ℝ × ℝ)) (x : ℝ), ChainFrom x l →
    ov lo hi x (endOf x l) ≤ (l.map fun p => ov lo hi p.1 p.2).sum
  | [], x, _ => by simp [endOf, ov]
  | p :: l, x, ⟨h1, h2, h3⟩ => by
    simp only [endOf, List.map_cons, List.sum_cons]
    have ih := ov_chain lo hi l p.2 h3
    have he := le_endOf l p.2 h3
    rw [← h1]
    calc ov lo hi p.1 (endOf p.2 l) ≤ ov lo hi p.1 p.2 + ov lo hi p.2 (endOf p.2 l) := ov_add h2 he
      _ ≤ _ := by linarith

lemma ov_cover {lo hi x y : ℝ} (hx : x ≤ lo) (hy : hi ≤ y) : hi - lo ≤ ov lo hi x y := by
  unfold ov
  rw [min_eq_right hy, max_eq_right hx]; exact le_max_right _ _

end chain

section side

variable {c : ℝ × ℝ} {θ : ℝ}

/-- **One side of Lemma K**: the cap of `Q` left of `x = a` (centre right of the line), times the
weight per area `we`, is paid by a chain of vertical pieces `(p0, p1, w)` on the line covering the
chord with weight per length `≥ ρ ≥ we · d̄`. -/
theorem side_x (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ) {a : ℝ} (ha : a ≤ c.1) {we ρ dbar : ℝ}
    (hwe : 0 ≤ we) (hρ : 0 ≤ ρ) (hd : a - xmin c θ ≤ dbar) (hwd : we * dbar ≤ ρ)
    (pcs : List (ℝ × ℝ × ℝ)) {P : ℝ} (hch : ChainFrom P (pcs.map fun p => (p.1, p.2.1)))
    (hpos : ∀ p ∈ pcs, p.1 < p.2.1) (hden : ∀ p ∈ pcs, ρ * (p.2.1 - p.1) ≤ p.2.2)
    (hP : lo c θ a < hi c θ a → P ≤ lo c θ a ∧ hi c θ a ≤ endOf P (pcs.map fun p => (p.1, p.2.1))) :
    we * (volume (sq c θ 1 ∩ {p | p.1 < a})).toReal ≤
      (pcs.map fun p => p.2.2 * segFrac (a, p.1) (a, p.2.1) (sq c θ 1)).sum := by
  have hcap := cap_le_chord (c := c) hs hc ha
  have hcap' : (volume (sq c θ 1 ∩ {p | p.1 < a})).toReal ≤ max 0 ((a - xmin c θ) * len c θ a) := by
    have := ENNReal.toReal_mono ENNReal.ofReal_ne_top hcap
    rwa [ENNReal.toReal_ofReal', max_comm] at this
  -- each piece: `ρ · overlap ≤ w · segFrac`
  have hterm : ∀ p ∈ pcs, ρ * ov (lo c θ a) (hi c θ a) p.1 p.2.1 ≤
      p.2.2 * segFrac (a, p.1) (a, p.2.1) (sq c θ 1) := by
    intro p hp
    have hL : 0 < p.2.1 - p.1 := by linarith [hpos p hp]
    have hw : 0 ≤ p.2.2 := le_trans (mul_nonneg hρ hL.le) (hden p hp)
    have hf := segFrac_vert_ge (c := c) hs hc (a := a) (hpos p hp)
    have hov := ov_nonneg (lo c θ a) (hi c θ a) p.1 p.2.1
    calc ρ * ov (lo c θ a) (hi c θ a) p.1 p.2.1
        ≤ p.2.2 * (ov (lo c θ a) (hi c θ a) p.1 p.2.1 / (p.2.1 - p.1)) := by
          rw [mul_div_assoc', le_div_iff₀ hL]
          nlinarith [hden p hp]
      _ ≤ p.2.2 * segFrac (a, p.1) (a, p.2.1) (sq c θ 1) := mul_le_mul_of_nonneg_left hf hw
  have hsum : ρ * (pcs.map fun p => ov (lo c θ a) (hi c θ a) p.1 p.2.1).sum ≤
      (pcs.map fun p => p.2.2 * segFrac (a, p.1) (a, p.2.1) (sq c θ 1)).sum := by
    rw [← List.sum_map_mul_left]
    exact List.sum_le_sum fun p hp => hterm p hp
  have hsum0 : 0 ≤ (pcs.map fun p => ov (lo c θ a) (hi c θ a) p.1 p.2.1).sum :=
    List.sum_nonneg fun x hx => by obtain ⟨p, _, rfl⟩ := List.mem_map.mp hx; exact ov_nonneg _ _ _ _
  have hchain := ov_chain (lo c θ a) (hi c θ a) _ P hch
  simp only [List.map_map, Function.comp_def] at hchain
  by_cases hz : len c θ a ≤ 0 ∨ a - xmin c θ ≤ 0
  · have h0 : (volume (sq c θ 1 ∩ {p | p.1 < a})).toReal = 0 := by
      rcases le_or_gt (a - xmin c θ) 0 with h | h
      · have hg := cap_le_ghat (c := c) hs hc a
        rw [show ghat (Real.sin θ) (Real.cos θ) (a - xmin c θ) = 0 by simp [ghat, h],
          ENNReal.ofReal_zero, nonpos_iff_eq_zero] at hg
        rw [hg]; rfl
      · have hl : len c θ a ≤ 0 := hz.resolve_right (not_le.mpr h)
        rw [max_eq_left (mul_nonpos_of_nonneg_of_nonpos h.le hl)] at hcap'
        exact le_antisymm hcap' ENNReal.toReal_nonneg
    rw [h0, mul_zero]; exact le_trans (mul_nonneg hρ hsum0) hsum
  · push_neg at hz
    obtain ⟨hl, hx⟩ := hz
    have hlh : lo c θ a < hi c θ a := by rw [len_eq] at hl; linarith
    obtain ⟨h1, h2⟩ := hP hlh
    have hcov := ov_cover (lo := lo c θ a) (hi := hi c θ a) h1 h2
    rw [← len_eq] at hcov
    have hmax : max 0 ((a - xmin c θ) * len c θ a) = (a - xmin c θ) * len c θ a :=
      max_eq_right (mul_pos hx hl).le
    rw [hmax] at hcap'
    calc we * (volume (sq c θ 1 ∩ {p | p.1 < a})).toReal
        ≤ we * ((a - xmin c θ) * len c θ a) := mul_le_mul_of_nonneg_left hcap' hwe
      _ ≤ we * (dbar * len c θ a) := mul_le_mul_of_nonneg_left (mul_le_mul_of_nonneg_right hd hl.le) hwe
      _ = (we * dbar) * len c θ a := by ring
      _ ≤ ρ * len c θ a := mul_le_mul_of_nonneg_right hwd hl.le
      _ ≤ ρ * (pcs.map fun p => ov (lo c θ a) (hi c θ a) p.1 p.2.1).sum :=
          mul_le_mul_of_nonneg_left (hcov.trans hchain) hρ
      _ ≤ _ := hsum

end side

section swap

variable {c : ℝ × ℝ} {θ : ℝ}

/-- `x ↔ y` maps `Q(c, θ)` onto `Q(swap c, π/2 − θ)`. -/
lemma mem_sq_swap (p : ℝ × ℝ) :
    swapXY p ∈ sq (swapXY c) (Real.pi / 2 - θ) 1 ↔ p ∈ sq c θ 1 := by
  rw [show Real.pi / 2 - θ = -θ + Real.pi / 2 by ring, sq_add_pi_div_two, mem_sq_swapXY]

lemma swap_preimage_sq :
    swapXY ⁻¹' (sq (swapXY c) (Real.pi / 2 - θ) 1) = sq c θ 1 := by
  ext p; exact mem_sq_swap p

lemma volume_cap_y (a : ℝ) :
    volume (sq c θ 1 ∩ {p | p.2 < a}) =
      volume (sq (swapXY c) (Real.pi / 2 - θ) 1 ∩ {p | p.1 < a}) := by
  have hmp : MeasurePreserving (swapXY : ℝ × ℝ → ℝ × ℝ) volume volume := by
    have : (swapXY : ℝ × ℝ → ℝ × ℝ) = Prod.swap := by funext p; rfl
    rw [this, Measure.volume_eq_prod]; exact Measure.measurePreserving_swap
  have hmeas : MeasurableSet (sq (swapXY c) (Real.pi / 2 - θ) 1 ∩ {p : ℝ × ℝ | p.1 < a}) :=
    (isClosed_sq' _ _ 1).measurableSet.inter (measurableSet_lt measurable_fst measurable_const)
  rw [← hmp.measure_preimage hmeas.nullMeasurableSet]
  congr 1
  ext p
  simp only [Set.mem_preimage, Set.mem_inter_iff, Set.mem_setOf_eq, mem_sq_swap]
  rfl

lemma segFrac_swap (a b : ℝ × ℝ) :
    segFrac (swapXY a) (swapXY b) (sq (swapXY c) (Real.pi / 2 - θ) 1) = segFrac a b (sq c θ 1) := by
  unfold segFrac
  congr 2
  ext t
  simp only [Set.mem_preimage, Set.mem_inter_iff]
  rw [← mem_sq_swap (c := c) (θ := θ)]
  rfl

/-- **The other side**: the cap of `Q` below `y = a`, paid by horizontal pieces on the line
(the hypotheses read on the swapped square). -/
theorem side_y (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ) {a : ℝ} (ha : a ≤ c.2) {we ρ dbar : ℝ}
    (hwe : 0 ≤ we) (hρ : 0 ≤ ρ)
    (hd : a - xmin (swapXY c) (Real.pi / 2 - θ) ≤ dbar) (hwd : we * dbar ≤ ρ)
    (pcs : List (ℝ × ℝ × ℝ)) {P : ℝ} (hch : ChainFrom P (pcs.map fun p => (p.1, p.2.1)))
    (hpos : ∀ p ∈ pcs, p.1 < p.2.1) (hden : ∀ p ∈ pcs, ρ * (p.2.1 - p.1) ≤ p.2.2)
    (hP : lo (swapXY c) (Real.pi / 2 - θ) a < hi (swapXY c) (Real.pi / 2 - θ) a →
      P ≤ lo (swapXY c) (Real.pi / 2 - θ) a ∧
        hi (swapXY c) (Real.pi / 2 - θ) a ≤ endOf P (pcs.map fun p => (p.1, p.2.1))) :
    we * (volume (sq c θ 1 ∩ {p | p.2 < a})).toReal ≤
      (pcs.map fun p => p.2.2 * segFrac (p.1, a) (p.2.1, a) (sq c θ 1)).sum := by
  have hs' : 0 < Real.sin (Real.pi / 2 - θ) := by rw [Real.sin_pi_div_two_sub]; exact hc
  have hc' : 0 < Real.cos (Real.pi / 2 - θ) := by rw [Real.cos_pi_div_two_sub]; exact hs
  have h := side_x (c := swapXY c) hs' hc' (a := a) ha hwe hρ hd hwd pcs hch hpos hden hP
  rw [volume_cap_y]
  refine h.trans (le_of_eq ?_)
  congr 1
  refine List.map_congr_left fun p _ => ?_
  rw [← segFrac_swap (c := c) (θ := θ) (p.1, a) (p.2.1, a)]
  rfl

end swap

section pose

open ZMTreeM

variable {c : ℝ × ℝ} {θ : ℝ}

/-- The segment mass of a sub-list of distinct entries is at most the whole segment mass. -/
lemma segMass_ge_sub {D : ℕ} {segs : List SegE} (l : List SegE) (hnd : l.Nodup)
    (hsub : ∀ x ∈ l, x ∈ segs) (Qs : Set (ℝ × ℝ)) :
    (l.map fun x => (x.2.2.2.2 : ℝ) * segFrac (segA D x) (segB D x) Qs).sum ≤ segMass D segs Qs := by
  unfold segMass
  rw [← List.sum_toFinset _ hnd]
  exact Finset.sum_le_sum_of_subset_of_nonneg (fun x hx => List.mem_toFinset.mpr (hsub x (List.mem_toFinset.mp hx)))
    fun _ _ _ => mul_nonneg (Nat.cast_nonneg _) (segFrac_nonneg _ _ _)

/-- **Lemma K at one pose**: if the square lies left of and below the far sides of the rectangle `e`
(weight `we` per area) and its two caps are paid by distinct pieces of the cover, its mass is at
least `we`. -/
theorem lemmaK_pose {D : ℕ} (hD : 0 < D) {segs : List SegE} {rects : List RectE} {e : RectE}
    (he : e ∈ rects) (hQ : ∀ p ∈ sq c θ 1, p.1 ≤ (e.2.2.1 : ℝ) / D ∧ p.2 ≤ (e.2.2.2.1 : ℝ) / D)
    (chX chY : List SegE) (hnd : (chX ++ chY).Nodup) (hsegs : ∀ x ∈ chX ++ chY, x ∈ segs)
    (hX : (e.2.2.2.2 : ℝ) * (volume (sq c θ 1 ∩ {p | p.1 < (e.1 : ℝ) / D})).toReal ≤
      (chX.map fun x => (x.2.2.2.2 : ℝ) * segFrac (segA D x) (segB D x) (sq c θ 1)).sum)
    (hY : (e.2.2.2.2 : ℝ) * (volume (sq c θ 1 ∩ {p | p.2 < (e.2.1 : ℝ) / D})).toReal ≤
      (chY.map fun x => (x.2.2.2.2 : ℝ) * segFrac (segA D x) (segB D x) (sq c θ 1)).sum) :
    (e.2.2.2.2 : ℝ) ≤ segMass D segs (sq c θ 1) + rectMass D rects (sq c θ 1) := by
  set Qs := sq c θ 1
  set we : ℝ := (e.2.2.2.2 : ℝ)
  -- the area: `1 ≤ |Q ∩ R| + |Q ∩ {x < a}| + |Q ∩ {y < a'}|`
  have hcover : Qs ⊆ (Qs ∩ rectSet D e) ∪ (Qs ∩ {p | p.1 < (e.1 : ℝ) / D}) ∪
      (Qs ∩ {p | p.2 < (e.2.1 : ℝ) / D}) := by
    intro p hp
    obtain ⟨h1, h2⟩ := hQ p hp
    by_cases hx : p.1 < (e.1 : ℝ) / D
    · exact Or.inl (Or.inr ⟨hp, hx⟩)
    by_cases hy : p.2 < (e.2.1 : ℝ) / D
    · exact Or.inr ⟨hp, hy⟩
    exact Or.inl (Or.inl ⟨hp, ⟨not_lt.mp hx, h1⟩, ⟨not_lt.mp hy, h2⟩⟩)
  have hfin : ∀ S : Set (ℝ × ℝ), volume (Qs ∩ S) ≠ ⊤ := fun S =>
    ne_top_of_le_ne_top (by rw [volume_sq]; exact ENNReal.one_ne_top) (measure_mono Set.inter_subset_left)
  have harea : (1 : ℝ) ≤ (volume (Qs ∩ rectSet D e)).toReal +
      (volume (Qs ∩ {p | p.1 < (e.1 : ℝ) / D})).toReal + (volume (Qs ∩ {p | p.2 < (e.2.1 : ℝ) / D})).toReal := by
    set A := Qs ∩ rectSet D e
    set B := Qs ∩ {p : ℝ × ℝ | p.1 < (e.1 : ℝ) / D}
    set C := Qs ∩ {p : ℝ × ℝ | p.2 < (e.2.1 : ℝ) / D}
    have h1 : volume Qs ≤ volume (A ∪ B ∪ C) := measure_mono hcover
    have h2 : volume (A ∪ B ∪ C) ≤ volume A + volume B + volume C :=
      (measure_union_le (A ∪ B) C).trans (by gcongr; exact measure_union_le A B)
    have h := h1.trans h2
    rw [volume_sq] at h
    have := ENNReal.toReal_mono (ENNReal.add_ne_top.mpr ⟨ENNReal.add_ne_top.mpr ⟨hfin _, hfin _⟩, hfin _⟩) h
    rwa [ENNReal.toReal_add (ENNReal.add_ne_top.mpr ⟨hfin _, hfin _⟩) (hfin _),
      ENNReal.toReal_add (hfin _) (hfin _), ENNReal.toReal_one] at this
  -- the rectangle's term of `rectMass`
  have hrect : we * (volume (Qs ∩ rectSet D e)).toReal ≤ rectMass D rects Qs := by
    unfold rectMass
    exact Finset.single_le_sum (f := fun e : RectE => (e.2.2.2.2 : ℝ) * (volume (Qs ∩ rectSet D e)).toReal)
      (fun _ _ => mul_nonneg (Nat.cast_nonneg _) ENNReal.toReal_nonneg) (List.mem_toFinset.mpr he)
  have hseg := segMass_ge_sub (D := D) (chX ++ chY) hnd hsegs Qs
  rw [List.map_append, List.sum_append] at hseg
  have hwe : 0 ≤ we := Nat.cast_nonneg _
  nlinarith [mul_le_mul_of_nonneg_left harea hwe]

end pose

section boxside

variable {c : ℝ × ℝ} {θ : ℝ}

/-- A nonempty chord: its ends are points of the square, so the line meets the square. -/
lemma chord_pts (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ) {a : ℝ} (h : lo c θ a < hi c θ a) :
    (a, lo c θ a) ∈ sq c θ 1 ∧ (a, hi c θ a) ∈ sq c θ 1 := by
  constructor <;> rw [mem_sq_iff_slice hs hc] <;> simp only [lo, hi] at h ⊢ <;>
    constructor <;> linarith [le_max_left (lowX c θ a) (lowY c θ a), min_le_left (upX c θ a) (upY c θ a)]

lemma wid_eq (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ) : wid θ = Real.cos θ + Real.sin θ := by
  simp [wid, abs_of_pos hs, abs_of_pos hc]

/-- **One side over a box of centres and angles**: the conditions of `side_x` from bounds on the
centre (`cx0 ≤ c.1`, `cy0 ≤ c.2 ≤ cy1`), on `cos θ + sin θ ≤ ŵ` and on `cos θ`, `sin θ`; the chain's
ends cover the chord by the crude range `c_y ± ŵ/2` or by the tight one. -/
theorem side_box (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ) {a cx0 cy0 cy1 w dbar we ρ : ℝ}
    {cmin cmax smin smax : ℝ} (hc0 : cmin ≤ Real.cos θ) (hc1 : Real.cos θ ≤ cmax)
    (hs0 : smin ≤ Real.sin θ) (hs1 : Real.sin θ ≤ smax)
    (hcx : cx0 ≤ c.1) (hcy0 : cy0 ≤ c.2) (hcy1 : c.2 ≤ cy1) (hw : Real.cos θ + Real.sin θ ≤ w)
    (ha : a ≤ cx0) (hdb : a - cx0 + w / 2 ≤ dbar) (hwe : 0 ≤ we) (hρ : 0 ≤ ρ) (hwd : we * dbar ≤ ρ)
    (pcs : List (ℝ × ℝ × ℝ)) {P : ℝ} (hch : ChainFrom P (pcs.map fun p => (p.1, p.2.1)))
    (hpos : ∀ p ∈ pcs, p.1 < p.2.1) (hden : ∀ p ∈ pcs, ρ * (p.2.1 - p.1) ≤ p.2.2)
    (hlow : P ≤ cy0 - w / 2 ∨ (0 < smin ∧ P ≤ cy0 + (cmin - smax) / 2 - cmax / smin * dbar))
    (hhigh : cy1 + w / 2 ≤ endOf P (pcs.map fun p => (p.1, p.2.1)) ∨
      (0 < cmin ∧ cy1 + (cmax - smin) / 2 + smax / cmin * dbar ≤ endOf P (pcs.map fun p => (p.1, p.2.1)))) :
    we * (volume (sq c θ 1 ∩ {p | p.1 < a})).toReal ≤
      (pcs.map fun p => p.2.2 * segFrac (a, p.1) (a, p.2.1) (sq c θ 1)).sum := by
  have hd : a - xmin c θ ≤ dbar := by simp only [xmin]; linarith
  refine side_x hs hc (ha.trans hcx) hwe hρ hd hwd pcs hch hpos hden fun hlh => ?_
  obtain ⟨plo, phi⟩ := chord_pts hs hc hlh
  have hwid := wid_eq hs hc
  -- the line meets the square: `d ≥ 0`
  have hd0 : 0 ≤ a - xmin c θ := by
    have := (abs_sub_le_wid plo).1
    rw [abs_le, hwid] at this
    simp only [xmin]; linarith [this.1]
  have hlo := lo_ge (c := c) hs hc a
  have hhi := hi_le (c := c) hs hc a
  constructor
  · rcases hlow with h | ⟨hsm, h⟩
    · have := (abs_sub_le_wid plo).2
      rw [abs_le, hwid] at this
      linarith [this.1]
    · have r1 : Real.cos θ / Real.sin θ ≤ cmax / smin := div_le_div₀ (hc.le.trans hc1) hc1 hsm hs0
      have k : Real.cos θ / Real.sin θ * (a - xmin c θ) ≤ cmax / smin * dbar :=
        (mul_le_mul_of_nonneg_right r1 hd0).trans
          (mul_le_mul_of_nonneg_left hd (div_nonneg (hc.le.trans hc1) hsm.le))
      linarith
  · rcases hhigh with h | ⟨hcm, h⟩
    · have := (abs_sub_le_wid phi).2
      rw [abs_le, hwid] at this
      linarith [this.2]
    · have r1 : Real.sin θ / Real.cos θ ≤ smax / cmin := div_le_div₀ (hs.le.trans hs1) hs1 hcm hc0
      have k : Real.sin θ / Real.cos θ * (a - xmin c θ) ≤ smax / cmin * dbar :=
        (mul_le_mul_of_nonneg_right r1 hd0).trans
          (mul_le_mul_of_nonneg_left hd (div_nonneg (hs.le.trans hs1) hcm.le))
      linarith

end boxside

section check

open ZMTreeM

/-- A side's certificate: the boxes' squares never cross the line, or a chain of pieces `(p0, p1, w)`
(over `D`, along the line) with weight per length `≥ ρ`. -/
inductive SideC where
  | far
  | chain (pcs : List (ℕ × ℕ × ℕ)) (ρ : ℚ)

/-- Consecutive pieces from `P`. -/
def chainN : ℕ → List (ℕ × ℕ × ℕ) → Bool
  | _, [] => true
  | P, p :: l => p.1 == P && Nat.blt p.1 p.2.1 && chainN p.2.1 l

def endN : ℕ → List (ℕ × ℕ × ℕ) → ℕ
  | P, [] => P
  | _, p :: l => endN p.2.1 l

/-- **A side's test** for the line at `a`: centres in `cx0 ≤ c_⊥`, `cy0 ≤ c_∥ ≤ cy1`, `cos + sin ≤ w`,
`cos ∈ [cmin, cmax]`, `sin ∈ [smin, smax]` (in the side's frame), rectangle weight `we` per area. -/
def sideOk (D : ℕ) (a cx0 cy0 cy1 w we cmin cmax smin smax : ℚ) : SideC → Bool
  | .far => decide (a + w / 2 ≤ cx0)
  | .chain [] _ => false
  | .chain (p :: l) ρ =>
    let P : ℚ := (p.1 : ℚ) / D
    let E : ℚ := (endN p.1 (p :: l) : ℚ) / D
    let dbar := a - cx0 + w / 2
    decide (a ≤ cx0) && decide (0 ≤ ρ) && decide (we * dbar ≤ ρ) && chainN p.1 (p :: l) &&
      (p :: l).all (fun q => decide (ρ * (((q.2.1 : ℚ) - q.1) / D) ≤ q.2.2)) &&
      (decide (P ≤ cy0 - w / 2) || (decide (0 < smin) &&
        decide (P ≤ cy0 + (cmin - smax) / 2 - cmax / smin * dbar))) &&
      (decide (cy1 + w / 2 ≤ E) || (decide (0 < cmin) &&
        decide (cy1 + (cmax - smin) / 2 + smax / cmin * dbar ≤ E)))

def sidePcs : SideC → List (ℕ × ℕ × ℕ)
  | .far => []
  | .chain pcs _ => pcs

/-- A cap certificate: the rectangle, the side `x = e.1/D` and the side `y = e.2.1/D`. -/
structure CapC where
  e : RectE
  sx : SideC
  sy : SideC

/-- The vertical pieces of the side `x = A` as segment entries, and the horizontal ones of `y = A`. -/
def vSeg (A : ℕ) (p : ℕ × ℕ × ℕ) : SegE := (A, p.1, A, p.2.1, p.2.2)
def hSeg (A : ℕ) (p : ℕ × ℕ × ℕ) : SegE := (p.1, A, p.2.1, A, p.2.2)

/-- Bounds of `cos θ`, `sin θ` for `u = tan(θ/2) ∈ [U0/R, U1/R]`. -/
def cminQ (R U1 : ℕ) : ℚ := ((R : ℚ) ^ 2 - (U1 : ℚ) ^ 2) / ((R : ℚ) ^ 2 + (U1 : ℚ) ^ 2)
def cmaxQ (R U0 : ℕ) : ℚ := ((R : ℚ) ^ 2 - (U0 : ℚ) ^ 2) / ((R : ℚ) ^ 2 + (U0 : ℚ) ^ 2)
def sminQ (R U0 : ℕ) : ℚ := 2 * (U0 : ℚ) * R / ((R : ℚ) ^ 2 + (U0 : ℚ) ^ 2)
def smaxQ (R U1 : ℕ) : ℚ := 2 * (U1 : ℚ) * R / ((R : ℚ) ^ 2 + (U1 : ℚ) ^ 2)

/-- **The test of a `CAP` box** (Lemma K). -/
def capOk (D S R W x0 x1 y0 y1 U0 U1 : ℕ) (segs : List SegE) (rects : List RectE) (k : CapC) : Bool :=
  let Q : ℚ := (D : ℚ) * S
  let w : ℚ := (widN R U0 U1 : ℚ) / widD R U0
  let we : ℚ := k.e.2.2.2.2
  let segsK := (sidePcs k.sx).map (vSeg k.e.1) ++ (sidePcs k.sy).map (hSeg k.e.2.1)
  Nat.blt U1 R && Nat.ble U0 U1 && rects.contains k.e && Nat.ble W k.e.2.2.2.2 &&
    decide ((x1 : ℚ) / Q + w / 2 ≤ (k.e.2.2.1 : ℚ) / D) &&
    decide ((y1 : ℚ) / Q + w / 2 ≤ (k.e.2.2.2.1 : ℚ) / D) &&
    decide segsK.Nodup && segsK.all (fun x => segs.contains x) &&
    sideOk D ((k.e.1 : ℚ) / D) (x0 / Q) (y0 / Q) (y1 / Q) w we (cminQ R U1) (cmaxQ R U0)
      (sminQ R U0) (smaxQ R U1) k.sx &&
    sideOk D ((k.e.2.1 : ℚ) / D) (y0 / Q) (x0 / Q) (x1 / Q) w we (sminQ R U0) (smaxQ R U1)
      (cminQ R U1) (cmaxQ R U0) k.sy

end check

section checkSound

open ZMTreeM LemmaEPoly

lemma trig_bounds {R U0 U1 : ℕ} (hR : 0 < R) (hU1 : U1 < R) {u : ℝ} (hu0 : (U0 : ℝ) / R < u)
    (hu1 : u ≤ (U1 : ℝ) / R) :
    ((cminQ R U1 : ℚ) : ℝ) ≤ Real.cos (2 * Real.arctan u) ∧
      Real.cos (2 * Real.arctan u) ≤ ((cmaxQ R U0 : ℚ) : ℝ) ∧
      ((sminQ R U0 : ℚ) : ℝ) ≤ Real.sin (2 * Real.arctan u) ∧
      Real.sin (2 * Real.arctan u) ≤ ((smaxQ R U1 : ℚ) : ℝ) ∧
      0 < Real.sin (2 * Real.arctan u) ∧ 0 < Real.cos (2 * Real.arctan u) := by
  have hRr : (0 : ℝ) < R := by exact_mod_cast hR
  have hU0 : (0 : ℝ) ≤ U0 := Nat.cast_nonneg _
  have h0 : (U0 : ℝ) < R * u := by rw [div_lt_iff₀ hRr] at hu0; linarith
  have h1 : R * u ≤ (U1 : ℝ) := by rw [le_div_iff₀ hRr] at hu1; linarith
  have hUR : (U1 : ℝ) < R := by exact_mod_cast hU1
  have hu : 0 < u := by nlinarith
  have hu1' : u < 1 := by nlinarith
  rw [(trig u).1, (trig u).2]
  simp only [cminQ, cmaxQ, sminQ, smaxQ]
  push_cast
  have hN : (0 : ℝ) < 1 + u ^ 2 := by positivity
  have hRU0 : (0 : ℝ) < (R : ℝ) ^ 2 + (U0 : ℝ) ^ 2 := by positivity
  have hRU1 : (0 : ℝ) < (R : ℝ) ^ 2 + (U1 : ℝ) ^ 2 := by positivity
  refine ⟨?_, ?_, ?_, ?_, by positivity, div_pos (by nlinarith) hN⟩
  · rw [div_le_div_iff₀ hRU1 hN]; nlinarith [mul_le_mul h1 h1 (by positivity) (by positivity)]
  · rw [div_le_div_iff₀ hN hRU0]; nlinarith [mul_le_mul h0.le h0.le hU0 (by positivity)]
  · rw [div_le_div_iff₀ hRU0 hN]
    nlinarith [mul_nonneg hU0 hu.le, mul_nonneg (sub_nonneg.mpr h0.le) (sub_nonneg.mpr (by nlinarith : (U0 : ℝ) * u ≤ R)),
      mul_pos hRr hu]
  · rw [div_le_div_iff₀ hN hRU1]
    nlinarith [mul_nonneg (sub_nonneg.mpr h1) (sub_nonneg.mpr (by nlinarith : (U1 : ℝ) * u ≤ R)), mul_pos hRr hu,
      hU0]

lemma chainN_sound {D : ℝ} (hD : 0 ≤ D) : ∀ (l : List (ℕ × ℕ × ℕ)) (P : ℕ), chainN P l = true →
    ChainFrom ((P : ℝ) / D) (l.map fun p => ((p.1 : ℝ) / D, (p.2.1 : ℝ) / D)) ∧
      endOf ((P : ℝ) / D) (l.map fun p => ((p.1 : ℝ) / D, (p.2.1 : ℝ) / D)) = (endN P l : ℝ) / D
  | [], P, _ => ⟨trivial, rfl⟩
  | p :: l, P, h => by
    simp only [chainN, Bool.and_eq_true, beq_iff_eq, Nat.blt_eq] at h
    obtain ⟨⟨h1, h2⟩, h3⟩ := h
    obtain ⟨ih1, ih2⟩ := chainN_sound hD l p.2.1 h3
    refine ⟨⟨by simp [h1], div_le_div_of_nonneg_right (by exact_mod_cast h2.le) hD, ih1⟩, ?_⟩
    simp only [List.map_cons, endOf, endN]
    exact ih2


lemma chainN_pos : ∀ (l : List (ℕ × ℕ × ℕ)) (P : ℕ), chainN P l = true → ∀ q ∈ l, q.1 < q.2.1
  | [], _, _, q, hq => by simp at hq
  | p :: l, P, h, q, hq => by
    simp only [chainN, Bool.and_eq_true, beq_iff_eq, Nat.blt_eq] at h
    rcases List.mem_cons.mp hq with rfl | hq
    · exact h.1.2
    · exact chainN_pos l p.2.1 h.2 q hq

/-- **A side's test is sound**: the cap times the rectangle's weight is paid by the side's pieces. -/
theorem sideOk_sound {D : ℕ} (hD : 0 < D) {a cx0 cy0 cy1 w we cmin cmax smin smax : ℚ} {sc : SideC}
    (h : sideOk D a cx0 cy0 cy1 w we cmin cmax smin smax sc = true) {c : ℝ × ℝ} {θ : ℝ}
    (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ)
    (hc0 : (cmin : ℝ) ≤ Real.cos θ) (hc1 : Real.cos θ ≤ cmax) (hs0 : (smin : ℝ) ≤ Real.sin θ)
    (hs1 : Real.sin θ ≤ smax) (hcx : (cx0 : ℝ) ≤ c.1) (hcy0 : (cy0 : ℝ) ≤ c.2) (hcy1 : c.2 ≤ cy1)
    (hw : Real.cos θ + Real.sin θ ≤ w) (hwe : 0 ≤ we) :
    (we : ℝ) * (volume (sq c θ 1 ∩ {p | p.1 < (a : ℝ)})).toReal ≤
      ((sidePcs sc).map fun q => (q.2.2 : ℝ) * segFrac ((a : ℝ), (q.1 : ℝ) / D) (a, (q.2.1 : ℝ) / D)
        (sq c θ 1)).sum := by
  have hDr : (0 : ℝ) < D := by exact_mod_cast hD
  revert h
  cases sc with
  | far =>
    intro h
    simp only [sideOk, decide_eq_true_eq] at h
    have hr : (a : ℝ) + w / 2 ≤ cx0 := by exact_mod_cast h
    have hemp : sq c θ 1 ∩ {p | p.1 < (a : ℝ)} = ∅ := by
      ext p
      simp only [Set.mem_inter_iff, Set.mem_setOf_eq, Set.mem_empty_iff_false, iff_false, not_and, not_lt]
      intro hp
      have := (abs_sub_le_wid hp).1
      rw [abs_le, wid_eq hs hc] at this
      linarith [this.1]
    simp [hemp, sidePcs]
  | chain pcs ρ =>
    intro h
    rcases pcs with _ | ⟨p, l⟩
    · simp [sideOk] at h
    simp only [sideOk, Bool.and_eq_true, Bool.or_eq_true, decide_eq_true_eq, List.all_eq_true] at h
    obtain ⟨⟨⟨⟨⟨⟨h1, h2⟩, h3⟩, h4⟩, h5⟩, h6⟩, h7⟩ := h
    have hch := chainN_sound hDr.le (p :: l) p.1 h4
    set pcsR : List (ℝ × ℝ × ℝ) := (p :: l).map fun q => ((q.1 : ℝ) / D, (q.2.1 : ℝ) / D, (q.2.2 : ℝ))
    have hm : (pcsR.map fun q => (q.1, q.2.1)) = (p :: l).map fun q => ((q.1 : ℝ) / D, (q.2.1 : ℝ) / D) := by
      simp only [pcsR, List.map_map, Function.comp_def]
    have hres := side_box (c := c) (θ := θ) hs hc hc0 hc1 hs0 hs1 hcx hcy0 hcy1 hw
      (a := (a : ℝ)) (dbar := ((a - cx0 + w / 2 : ℚ) : ℝ)) (we := (we : ℝ)) (ρ := (ρ : ℝ))
      (by exact_mod_cast h1) (by push_cast; exact le_rfl) (by exact_mod_cast hwe) (by exact_mod_cast h2)
      (by exact_mod_cast h3) pcsR (P := (p.1 : ℝ) / D) (by rw [hm]; exact hch.1)
      (by
        intro q hq
        obtain ⟨q', hq', rfl⟩ := List.mem_map.mp hq
        exact div_lt_div_of_pos_right (by exact_mod_cast chainN_pos _ _ h4 q' hq') hDr)
      (by
        intro q hq
        obtain ⟨q', hq', rfl⟩ := List.mem_map.mp hq
        have := h5 q' hq'
        have hr : ((ρ * (((q'.2.1 : ℚ) - q'.1) / D) : ℚ) : ℝ) ≤ ((q'.2.2 : ℚ) : ℝ) := by exact_mod_cast this
        push_cast at hr
        simp only
        rw [← sub_div]; exact hr)
      (by
        rcases h6 with h6 | ⟨h6a, h6b⟩
        · left; have := (Rat.cast_le (K := ℝ)).mpr h6; push_cast at this ⊢; linarith
        · right; refine ⟨by exact_mod_cast h6a, ?_⟩
          have := (Rat.cast_le (K := ℝ)).mpr h6b; push_cast at this ⊢; linarith)
      (by
        rw [hm, hch.2]
        rcases h7 with h7 | ⟨h7a, h7b⟩
        · left; have := (Rat.cast_le (K := ℝ)).mpr h7; push_cast at this ⊢; linarith
        · right; refine ⟨by exact_mod_cast h7a, ?_⟩
          have := (Rat.cast_le (K := ℝ)).mpr h7b; push_cast at this ⊢; linarith)
    simpa [pcsR, sidePcs, List.map_map, Function.comp_def] using hres


/-- **Lemma K on a box**: a passing `CAP` certificate covers the box. -/
theorem capOk_sound {D S Mq R W x0 x1 y0 y1 U0 U1 : ℕ} {pts : List (ℕ × ℕ × ℕ)} {segs : List SegE}
    {rects : List RectE} {k : CapC} (hD : 0 < D) (hS : 0 < S) (hR : 0 < R)
    (h : capOk D S R W x0 x1 y0 y1 U0 U1 segs rects k = true) :
    CovMPo D S Mq R W pts segs rects x0 x1 y0 y1 U0 U1 := by
  intro c u hx0 hx1 hy0 hy1 hu0 hu1 _
  simp only [capOk, Bool.and_eq_true, Nat.blt_eq, Nat.ble_eq, decide_eq_true_eq, List.all_eq_true,
    List.contains_iff_mem] at h
  obtain ⟨⟨⟨⟨⟨⟨⟨⟨⟨hU1, _⟩, he⟩, hW⟩, hxr⟩, hyr⟩, hnd⟩, hin⟩, hsx⟩, hsy⟩ := h
  set θ := 2 * Real.arctan u
  obtain ⟨hc0, hc1, hs0, hs1, hs, hc⟩ := trig_bounds hR hU1 hu0 hu1
  have hDr : (0 : ℝ) < D := by exact_mod_cast hD
  have hSr : (0 : ℝ) < S := by exact_mod_cast hS
  have hwid : wid θ ≤ (widN R U0 U1 : ℝ) / widD R U0 :=
    wid_le_widHat hR hU1.le hu0.le hu1
  rw [wid_eq hs hc] at hwid
  have cQ : ∀ n : ℕ, (((n : ℚ) / ((D : ℚ) * S) : ℚ) : ℝ) = (n : ℝ) / (D * S) := fun n => by push_cast; rfl
  have cw : (((widN R U0 U1 : ℚ) / widD R U0 : ℚ) : ℝ) = (widN R U0 U1 : ℝ) / widD R U0 := by push_cast; rfl
  have cA : ∀ n : ℕ, (((n : ℚ) / D : ℚ) : ℝ) = (n : ℝ) / D := fun n => by push_cast; rfl
  -- the square is left of and below the far sides
  have hxr' := (Rat.cast_le (K := ℝ)).mpr hxr
  have hyr' := (Rat.cast_le (K := ℝ)).mpr hyr
  push_cast at hxr' hyr'
  have hQ : ∀ p ∈ sq c θ 1, p.1 ≤ (k.e.2.2.1 : ℝ) / D ∧ p.2 ≤ (k.e.2.2.2.1 : ℝ) / D := by
    intro p hp
    obtain ⟨a1, a2⟩ := abs_sub_le_wid hp
    rw [abs_le, wid_eq hs hc] at a1 a2
    constructor <;> linarith [a1.2, a2.2]
  -- the side `x = e.1/D`
  have hX := sideOk_sound hD hsx (c := c) (θ := θ) hs hc
    (by exact_mod_cast hc0) (by exact_mod_cast hc1) (by exact_mod_cast hs0) (by exact_mod_cast hs1)
    (by rw [cQ]; exact hx0) (by rw [cQ]; exact hy0) (by rw [cQ]; exact hy1) (by rw [cw]; exact hwid)
    (by positivity)
  -- the side `y = e.2.1/D`, on the swapped square
  have hs' : 0 < Real.sin (Real.pi / 2 - θ) := by rw [Real.sin_pi_div_two_sub]; exact hc
  have hc' : 0 < Real.cos (Real.pi / 2 - θ) := by rw [Real.cos_pi_div_two_sub]; exact hs
  have hY := sideOk_sound hD hsy (c := swapXY c) (θ := Real.pi / 2 - θ) hs' hc'
    (by rw [Real.cos_pi_div_two_sub]; exact_mod_cast hs0) (by rw [Real.cos_pi_div_two_sub]; exact_mod_cast hs1)
    (by rw [Real.sin_pi_div_two_sub]; exact_mod_cast hc0) (by rw [Real.sin_pi_div_two_sub]; exact_mod_cast hc1)
    (by rw [cQ]; exact hy0) (by rw [cQ]; exact hx0) (by rw [cQ]; exact hx1)
    (by rw [cw, Real.cos_pi_div_two_sub, Real.sin_pi_div_two_sub]; linarith) (by positivity)
  rw [← volume_cap_y] at hY
  have hK := lemmaK_pose (c := c) (θ := θ) hD he hQ ((sidePcs k.sx).map (vSeg k.e.1))
    ((sidePcs k.sy).map (hSeg k.e.2.1)) hnd hin
    (by
      refine (le_of_eq ?_).trans (hX.trans (le_of_eq ?_))
      · rw [cA]; push_cast; rfl
      · simp only [List.map_map, Function.comp_def, vSeg, segA, segB, cA])
    (by
      refine (le_of_eq ?_).trans (hY.trans (le_of_eq ?_))
      · rw [cA]; push_cast; rfl
      · simp only [List.map_map, Function.comp_def, hSeg, segA, segB, cA]
        congr 1
        refine List.map_congr_left fun q _ => ?_
        rw [← segFrac_swap (c := c) (θ := θ)]
        rfl)
  have hWr : (W : ℝ) ≤ k.e.2.2.2.2 := by exact_mod_cast hW
  have := ptMass_nonneg D pts (sq c θ 1)
  linarith

end checkSound

end CapK

end SquarePacking
