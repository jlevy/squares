import Sqpack.CovM

/-!
# Segment parts: lower bounds on the segment mass of a square

The real-analysis layer under the piece leaves of `ZMTreeM.lean`.

* `sum_len_le_volume` — ordered, non-overlapping open intervals inside a set `s ⊆ ℝ` have total
  length `≤ volume s`.
* A **part** is `(e, l, h)`: a segment entry `e` (axis-parallel), and a sub-interval `[l, h]` of its
  extent in the line coordinate (`y` on a vertical segment, `x` on a horizontal one) whose interior
  points all lie in the square.  `parts_le_segMass`: if parts on the same entry do not overlap, then
  `Σ_parts w_e (h − l) / |e| ≤ segMass` (`CovM.lean`): each part is a sub-interval of the segment's
  parameter set `segPt⁻¹(Q) ∩ [0,1]`, whose measure is `segFrac`.
* `pair_capture` — **Lemma T at one pose**, in the form used by the germ-pair certificate: for the
  two lines of a germ pair, the singular violation polynomials satisfy
  `G_up(t) + G_down(t') = 4u (t' − t − u)` (`gval_pairV`, `gval_pairH`), and from that alone a *pair*
  (an up-piece `[a,b]` and a down-piece `[c,d]` with `c ≤ a + u₀`, `d ≤ b + u₀`) captures mass
  `≥ m` whenever `m` is at most the mass of each piece.  This is the dual (matching) form of
  `ZM_MIXED.md`'s Corollary T: summing pairs of a monotone coupling of the two lines' masses gives
  `min_T f(T)`, without an explicit minimisation over the threshold `T`.
-/

open MeasureTheory

namespace SquarePacking

namespace ZMTreeM

open BoxTree

/-! ## 1.  Intervals in a set -/

/-- Ordered, non-overlapping open intervals inside `s` have total length at most `volume s`. -/
lemma sum_len_le_volume : ∀ (L : List (ℝ × ℝ)) (s : Set ℝ),
    L.Pairwise (fun p q => p.2 ≤ q.1) → (∀ p ∈ L, p.1 ≤ p.2 ∧ Set.Ioo p.1 p.2 ⊆ s) →
    (L.map fun p => ENNReal.ofReal (p.2 - p.1)).sum ≤ volume s
  | [], _, _, _ => by simp
  | p :: L, s, hpw, hsub => by
    rw [List.pairwise_cons] at hpw
    obtain ⟨hp1, hpw⟩ := hpw
    have hs := measure_inter_add_sdiff (μ := volume) s (measurableSet_Iio (a := p.2))
    have h1 : ENNReal.ofReal (p.2 - p.1) ≤ volume (s ∩ Set.Iio p.2) := by
      rw [← Real.volume_Ioo]
      apply measure_mono
      intro x hx
      exact ⟨(hsub p List.mem_cons_self).2 hx, hx.2⟩
    have h2 : (L.map fun p => ENNReal.ofReal (p.2 - p.1)).sum ≤ volume (s \ Set.Iio p.2) := by
      apply sum_len_le_volume L _ hpw
      intro q hq
      refine ⟨(hsub q (List.mem_cons_of_mem _ hq)).1, fun x hx => ⟨?_, ?_⟩⟩
      · exact (hsub q (List.mem_cons_of_mem _ hq)).2 hx
      · simp only [Set.mem_Iio, not_lt]
        exact le_trans (hp1 q hq) hx.1.le
    simp only [List.map_cons, List.sum_cons]
    rw [← hs]
    exact add_le_add h1 h2

/-- The real version: the lengths sum to at most `(volume s).toReal` (for `volume s < ∞`). -/
lemma sum_len_le_toReal (L : List (ℝ × ℝ)) (s : Set ℝ) (hfin : volume s ≠ ⊤)
    (hpw : L.Pairwise (fun p q => p.2 ≤ q.1)) (hsub : ∀ p ∈ L, p.1 ≤ p.2 ∧ Set.Ioo p.1 p.2 ⊆ s) :
    (L.map fun p => p.2 - p.1).sum ≤ (volume s).toReal := by
  have hnn : ∀ q ∈ L, 0 ≤ q.2 - q.1 := fun q hq => by linarith [(hsub q hq).1]
  have e : ∀ M : List (ℝ × ℝ), (∀ q ∈ M, 0 ≤ q.2 - q.1) →
      (M.map fun p => ENNReal.ofReal (p.2 - p.1)).sum = ENNReal.ofReal (M.map fun p => p.2 - p.1).sum := by
    intro M hM
    induction M with
    | nil => simp
    | cons a M ih =>
      simp only [List.map_cons, List.sum_cons]
      rw [ih fun q hq => hM q (List.mem_cons_of_mem _ hq),
        ENNReal.ofReal_add (hM a List.mem_cons_self)
          (List.sum_nonneg fun x hx => by
            obtain ⟨q, hq, rfl⟩ := List.mem_map.mp hx
            exact hM q (List.mem_cons_of_mem _ hq))]
  have h := sum_len_le_volume L s hpw hsub
  rw [e L hnn] at h
  have := ENNReal.toReal_mono hfin h
  rwa [ENNReal.toReal_ofReal (List.sum_nonneg fun x hx => by
    obtain ⟨q, hq, rfl⟩ := List.mem_map.mp hx
    exact hnn q hq)] at this

/-! ## 2.  Parts of axis-parallel segments -/

/-- An entry is an axis-parallel, non-degenerate, normalised segment. -/
def isVert (e : SegE) : Prop := e.1 = e.2.2.1 ∧ e.2.1 < e.2.2.2.1
def isHorz (e : SegE) : Prop := e.2.1 = e.2.2.2.1 ∧ e.1 < e.2.2.1

open Classical in
/-- The ends of the segment in its line coordinate (`y` for vertical, `x` otherwise), over `D`. -/
noncomputable def elo (D : ℕ) (e : SegE) : ℝ := if e.1 = e.2.2.1 then (e.2.1 : ℝ) / D else (e.1 : ℝ) / D
open Classical in
noncomputable def ehi (D : ℕ) (e : SegE) : ℝ :=
  if e.1 = e.2.2.1 then (e.2.2.2.1 : ℝ) / D else (e.2.2.1 : ℝ) / D
open Classical in
/-- The point of the segment's line with line coordinate `t`. -/
noncomputable def lpE (D : ℕ) (e : SegE) (t : ℝ) : ℝ × ℝ :=
  if e.1 = e.2.2.1 then ((e.1 : ℝ) / D, t) else (t, (e.2.1 : ℝ) / D)

/-- A part `(e, l, h)` at a square `Qs`: `e` axis-parallel, `[l, h]` inside its extent, and every
point strictly between `l` and `h` on its line lies in `Qs`. -/
def PartOK (D : ℕ) (Qs : Set (ℝ × ℝ)) (p : SegE × ℝ × ℝ) : Prop :=
  (isVert p.1 ∨ isHorz p.1) ∧ elo D p.1 ≤ p.2.1 ∧ p.2.1 ≤ p.2.2 ∧ p.2.2 ≤ ehi D p.1 ∧
    ∀ t, p.2.1 < t → t < p.2.2 → lpE D p.1 t ∈ Qs

/-- The mass a part certifies: `w · (h − l) / |e|` (weights not divided by `W`). -/
noncomputable def pval (D : ℕ) (p : SegE × ℝ × ℝ) : ℝ :=
  (p.1.2.2.2.2 : ℝ) * (p.2.2 - p.2.1) / (ehi D p.1 - elo D p.1)

lemma elo_lt_ehi {D : ℕ} (hD : 0 < D) {e : SegE} (he : isVert e ∨ isHorz e) : elo D e < ehi D e := by
  have hDr : (0 : ℝ) < D := by exact_mod_cast hD
  rcases he with ⟨h1, h2⟩ | ⟨h1, h2⟩
  · simp only [elo, ehi, h1, if_true]
    exact div_lt_div_of_pos_right (by exact_mod_cast h2) hDr
  · have hne : e.1 ≠ e.2.2.1 := ne_of_lt h2
    simp only [elo, ehi, hne, if_false]
    exact div_lt_div_of_pos_right (by exact_mod_cast h2) hDr

/-- The segment point of parameter `τ` is the line point of coordinate `elo + τ (ehi − elo)`. -/
lemma segPt_eq_lpE {D : ℕ} {e : SegE} (he : isVert e ∨ isHorz e) (τ : ℝ) :
    segPt (segA D e) (segB D e) τ = lpE D e (elo D e + τ * (ehi D e - elo D e)) := by
  rcases he with ⟨h1, _⟩ | ⟨h1, h2⟩
  · simp only [segPt, segA, segB, lpE, elo, ehi, h1, if_true]
    ext <;> (simp; try ring)
  · have hne : e.1 ≠ e.2.2.1 := ne_of_lt h2
    simp only [segPt, segA, segB, lpE, elo, ehi, hne, if_false, h1]
    ext <;> (simp; try ring)

/-- **Parts on one entry**: non-overlapping parts of `e` inside `Qs` have total length at most
`|e| · segFrac`. -/
lemma parts_one {D : ℕ} (hD : 0 < D) {e : SegE} (he : isVert e ∨ isHorz e) (Qs : Set (ℝ × ℝ))
    (L : List (ℝ × ℝ)) (hpw : L.Pairwise (fun p q => p.2 ≤ q.1))
    (hok : ∀ p ∈ L, elo D e ≤ p.1 ∧ p.1 ≤ p.2 ∧ p.2 ≤ ehi D e ∧
      ∀ t, p.1 < t → t < p.2 → lpE D e t ∈ Qs) :
    (L.map fun p => p.2 - p.1).sum ≤ (ehi D e - elo D e) * segFrac (segA D e) (segB D e) Qs := by
  set len := ehi D e - elo D e with hlen
  have hl : 0 < len := by rw [hlen]; linarith [elo_lt_ehi hD he]
  -- map to parameter intervals
  let f : ℝ × ℝ → ℝ × ℝ := fun p => ((p.1 - elo D e) / len, (p.2 - elo D e) / len)
  set s := segPt (segA D e) (segB D e) ⁻¹' Qs ∩ Set.Icc (0 : ℝ) 1 with hs
  have hfin : volume s ≠ ⊤ := by
    apply ne_top_of_le_ne_top (b := volume (Set.Icc (0 : ℝ) 1))
    · simp [Real.volume_Icc]
    · exact measure_mono Set.inter_subset_right
  have hpw' : (L.map f).Pairwise (fun p q => p.2 ≤ q.1) := by
    rw [List.pairwise_map]
    refine hpw.imp fun {p q} h => ?_
    exact div_le_div_of_nonneg_right (by linarith) hl.le
  have hsub : ∀ p ∈ L.map f, p.1 ≤ p.2 ∧ Set.Ioo p.1 p.2 ⊆ s := by
    intro p hp
    obtain ⟨q, hq, rfl⟩ := List.mem_map.mp hp
    obtain ⟨h0, h1, h2, h3⟩ := hok q hq
    refine ⟨div_le_div_of_nonneg_right (by linarith) hl.le, fun τ hτ => ?_⟩
    obtain ⟨hτ1, hτ2⟩ := hτ
    simp only [f] at hτ1 hτ2
    have k1 : q.1 < elo D e + τ * len := by
      rw [div_lt_iff₀ hl] at hτ1; linarith
    have k2 : elo D e + τ * len < q.2 := by
      rw [lt_div_iff₀ hl] at hτ2; linarith
    refine ⟨?_, ?_, ?_⟩
    · simp only [Set.mem_preimage]
      rw [segPt_eq_lpE he]
      exact h3 _ k1 k2
    · have : 0 ≤ τ * len := by nlinarith
      exact (mul_nonneg_iff_of_pos_right hl).mp this
    · have : τ * len ≤ len := by linarith
      exact (mul_le_iff_le_one_left hl).mp this
  have key := sum_len_le_toReal (L.map f) s hfin hpw' hsub
  have e1 : ((L.map f).map fun p => p.2 - p.1).sum = (L.map fun p => p.2 - p.1).sum / len := by
    rw [List.map_map]
    have : ∀ M : List (ℝ × ℝ), (M.map ((fun p : ℝ × ℝ => p.2 - p.1) ∘ f)).sum
        = (M.map fun p => p.2 - p.1).sum / len := by
      intro M
      induction M with
      | nil => simp
      | cons a M ih =>
        simp only [List.map_cons, List.sum_cons, ih, Function.comp, f]
        field_simp
        ring
    exact this L
  rw [e1] at key
  have hfr : (volume s).toReal = segFrac (segA D e) (segB D e) Qs := rfl
  rw [hfr, div_le_iff₀ hl] at key
  linarith

/-- Sum over a list, regrouped by entry. -/
lemma list_sum_fiber (E : Finset SegE) (f : SegE × ℝ × ℝ → ℝ) :
    ∀ (ps : List (SegE × ℝ × ℝ)), (∀ p ∈ ps, p.1 ∈ E) →
      (ps.map f).sum = ∑ e ∈ E, ((ps.filter (fun p => p.1 = e)).map f).sum
  | [], _ => by simp
  | p :: ps, hE => by
    have ih := list_sum_fiber E f ps (fun q hq => hE q (List.mem_cons_of_mem _ hq))
    simp only [List.map_cons, List.sum_cons, List.filter_cons]
    have : ∀ e ∈ E, ((if decide (p.1 = e) = true then p :: ps.filter (fun p => p.1 = e)
        else ps.filter (fun p => p.1 = e)).map f).sum
        = (if p.1 = e then f p else 0) + ((ps.filter (fun p => p.1 = e)).map f).sum := by
      intro e _
      by_cases h : p.1 = e <;> simp [h]
    rw [Finset.sum_congr rfl this, Finset.sum_add_distrib, Finset.sum_ite_eq, if_pos (hE p List.mem_cons_self), ih]

/-- **Parts bound the segment mass.**  Parts on entries of the cover, pairwise non-overlapping when
they share an entry, certify at most the segment mass of the square. -/
theorem parts_le_segMass {D : ℕ} (hD : 0 < D) (segs : List SegE) (Qs : Set (ℝ × ℝ))
    (ps : List (SegE × ℝ × ℝ)) (hmem : ∀ p ∈ ps, p.1 ∈ segs.toFinset)
    (hok : ∀ p ∈ ps, PartOK D Qs p)
    (hpw : ps.Pairwise (fun p q => p.1 = q.1 → p.2.2 ≤ q.2.1)) :
    (ps.map (pval D)).sum ≤ segMass D segs Qs := by
  rw [list_sum_fiber segs.toFinset (pval D) ps hmem, segMass]
  refine Finset.sum_le_sum fun e _ => ?_
  set F := ps.filter (fun p => p.1 = e) with hF
  by_cases h0 : F = []
  · rw [h0]; simp only [List.map_nil, List.sum_nil]
    exact mul_nonneg (Nat.cast_nonneg _) (segFrac_nonneg _ _ _)
  have hne : F ≠ [] := h0
  obtain ⟨p0, hp0⟩ := List.exists_mem_of_ne_nil F hne
  have hp0' := List.mem_filter.mp hp0
  have he0 : p0.1 = e := by simpa using hp0'.2
  have hax : isVert e ∨ isHorz e := he0 ▸ (hok p0 hp0'.1).1
  have hl : 0 < ehi D e - elo D e := by linarith [elo_lt_ehi hD hax]
  -- the fiber as intervals
  have hFe : ∀ p ∈ F, p.1 = e := fun p hp => by simpa using (List.mem_filter.mp hp).2
  have hpwF : (F.map fun p => p.2).Pairwise (fun p q => p.2 ≤ q.1) := by
    rw [List.pairwise_map]
    have := hpw.sublist (List.filter_sublist (p := fun p => decide (p.1 = e)))
    refine List.Pairwise.imp_of_mem ?_ this
    intro a b ha hb h
    exact h (by rw [hFe a ha, hFe b hb])
  have hokF : ∀ q ∈ F.map (fun p => p.2), elo D e ≤ q.1 ∧ q.1 ≤ q.2 ∧ q.2 ≤ ehi D e ∧
      ∀ t, q.1 < t → t < q.2 → lpE D e t ∈ Qs := by
    intro q hq
    obtain ⟨p, hp, rfl⟩ := List.mem_map.mp hq
    have hpe := hFe p hp
    obtain ⟨_, h1, h2, h3, h4⟩ := hok p (List.mem_filter.mp hp).1
    rw [hpe] at h1 h3 h4
    exact ⟨h1, h2, h3, h4⟩
  have key := parts_one hD hax Qs (F.map fun p => p.2) hpwF hokF
  have e1 : (F.map (pval D)).sum
      = (e.2.2.2.2 : ℝ) / (ehi D e - elo D e) * ((F.map fun p => p.2).map fun q => q.2 - q.1).sum := by
    rw [List.map_map]
    have : ∀ M : List (SegE × ℝ × ℝ), (∀ p ∈ M, p.1 = e) → (M.map (pval D)).sum
        = (e.2.2.2.2 : ℝ) / (ehi D e - elo D e) * (M.map ((fun q : ℝ × ℝ => q.2 - q.1) ∘ fun p => p.2)).sum := by
      intro M hM
      induction M with
      | nil => simp
      | cons a M ih =>
        simp only [List.map_cons, List.sum_cons]
        rw [ih fun p hp => hM p (List.mem_cons_of_mem _ hp)]
        have ha := hM a List.mem_cons_self
        simp only [pval, Function.comp, ha]
        ring
    exact this F hFe
  rw [e1]
  have hw : (0 : ℝ) ≤ (e.2.2.2.2 : ℝ) / (ehi D e - elo D e) := div_nonneg (Nat.cast_nonneg _) hl.le
  calc (e.2.2.2.2 : ℝ) / (ehi D e - elo D e) * ((F.map fun p => p.2).map fun q => q.2 - q.1).sum
      ≤ (e.2.2.2.2 : ℝ) / (ehi D e - elo D e) * ((ehi D e - elo D e) *
          segFrac (segA D e) (segB D e) Qs) := mul_le_mul_of_nonneg_left key hw
    _ = (e.2.2.2.2 : ℝ) * segFrac (segA D e) (segB D e) Qs := by field_simp

/-! ## 3.  Lemma T at one pose, pair form -/

/-- The singular polynomials of a vertical germ pair (`x = ξ`, kind 1; `x = ξ + 1`, kind 0). -/
lemma gval_pairV (ξ cx cy t t' u : ℝ) :
    gval 1 (ξ - cx) (t - cy) u + gval 0 (ξ + 1 - cx) (t' - cy) u = 4 * u * (t' - t - u) := by
  simp only [gval, gc]; ring

/-- The singular polynomials of a horizontal germ pair (`y = η + 1`, kind 2; `y = η`, kind 3). -/
lemma gval_pairH (η cx cy t t' u : ℝ) :
    gval 2 (t - cx) (η + 1 - cy) u + gval 3 (t' - cx) (η - cy) u = 4 * u * (t' - t - u) := by
  simp only [gval, gc]; ring

/-- **Lemma T, pair form.**  Let `gU`, `gD` be the singular violation polynomials of the up and down
line at a pose, with `gU t + gD t' = 4u(t' − t − u)` (`u ≥ u₀ ≥ 0`).  An up-piece `[a, b]` (density
`ρU`) and a down-piece `[c, d]` (density `ρD`) with `c ≤ a + u₀`, `d ≤ b + u₀` capture at least `m`
for any `m ≤ ρU (b − a)`, `m ≤ ρD (d − c)`: there are `a' ∈ [a,b]`, `d' ∈ [c,d]` with the singular
condition holding on `(a', b)` and on `(c, d')`, and `m ≤ ρU (b − a') + ρD (d' − c)`. -/
lemma pair_capture {gU gD : ℝ → ℝ} {u u0 a b c d ρU ρD m : ℝ}
    (hUD : ∀ t t', gU t + gD t' = 4 * u * (t' - t - u)) (hu0 : 0 ≤ u0) (hu : u0 ≤ u)
    (hab : a ≤ b) (hcd : c ≤ d) (hca : c ≤ a + u0) (hdb : d ≤ b + u0)
    (hρU : 0 ≤ ρU) (hρD : 0 ≤ ρD) (hmU : m ≤ ρU * (b - a)) (hmD : m ≤ ρD * (d - c)) :
    ∃ a' d', a ≤ a' ∧ a' ≤ b ∧ c ≤ d' ∧ d' ≤ d ∧ (∀ t, a' < t → t < b → gU t ≤ 0) ∧
      (∀ t, c < t → t < d' → gD t ≤ 0) ∧ m ≤ ρU * (b - a') + ρD * (d' - c) := by
  have hslope : ∀ t t', gU t' = gU t - 4 * u * (t' - t) := by
    intro t t'
    have h1 := hUD t 0
    have h2 := hUD t' 0
    linarith
  have hDv : ∀ t t', gD t' = 4 * u * (t' - t - u) - gU t := by
    intro t t'; linarith [hUD t t']
  have hu' : 0 ≤ u := le_trans hu0 hu
  by_cases hA : gU a ≤ 0
  · -- the whole up-piece is in
    refine ⟨a, c, le_rfl, hab, le_rfl, hcd, fun t ht _ => ?_, fun t h1 h2 => absurd (lt_trans h1 h2)
      (lt_irrefl _), by nlinarith⟩
    rw [hslope a t]; nlinarith
  push Not at hA
  by_cases hB : 0 < gU b
  · -- no up point is in: the whole down-piece is
    refine ⟨b, d, hab, le_rfl, hcd, le_rfl, fun t h1 h2 => absurd (lt_trans h1 h2) (lt_irrefl _),
      fun t _ ht => ?_, by nlinarith⟩
    rw [hDv b t]
    have : t - b - u ≤ 0 := by linarith
    nlinarith
  push Not at hB
  -- the threshold `T ∈ (a, b]`
  have hu1 : 0 < u := by
    rcases eq_or_lt_of_le hu' with h | h
    · have := hslope a b; rw [← h] at this; linarith
    · exact h
  set T := a + gU a / (4 * u) with hT
  have h4u : 0 < 4 * u := by linarith
  have hgT : gU T = 0 := by
    rw [hslope a T, hT]; field_simp; ring
  have haT : a < T := by rw [hT]; have := div_pos hA h4u; linarith
  have hTb : T ≤ b := by
    have := hslope T b
    rw [hgT] at this
    by_contra hc; push Not at hc; nlinarith
  have hupT : ∀ t, T < t → t < b → gU t ≤ 0 := by
    intro t ht _; rw [hslope T t, hgT]; nlinarith
  have hdnT : ∀ t, t ≤ T + u → gD t ≤ 0 := by
    intro t ht; rw [hDv T t, hgT]; nlinarith
  rcases le_total d (T + u) with hd | hd
  · refine ⟨T, d, haT.le, hTb, hcd, le_rfl, hupT, fun t _ ht => hdnT t (by linarith), ?_⟩
    nlinarith
  · have hcT : c ≤ T + u := by linarith
    refine ⟨T, T + u, haT.le, hTb, hcT, hd, hupT, fun t _ ht => hdnT t ht.le, ?_⟩
    have hba : 0 < b - a := by linarith
    -- `m (b − a) ≤ (ρU (b − T) + ρD (T + u − c)) (b − a)`
    have k1 : m * (b - T) ≤ ρU * (b - a) * (b - T) := mul_le_mul_of_nonneg_right hmU (by linarith)
    have k2 : m * (T - a) ≤ ρD * (d - c) * (T - a) := mul_le_mul_of_nonneg_right hmD (by linarith)
    have k3 : (d - c) * (T - a) ≤ (T + u - c) * (b - a) := by
      have : (T + u - c) * (b - a) - (d - c) * (T - a)
          = (b - T) * (a + u - c) + (T - a) * (b + u - d) := by ring
      nlinarith [mul_nonneg (by linarith : (0 : ℝ) ≤ b - T) (by linarith : (0 : ℝ) ≤ a + u - c),
        mul_nonneg (by linarith : (0 : ℝ) ≤ T - a) (by linarith : (0 : ℝ) ≤ b + u - d)]
    have k4 : ρD * ((d - c) * (T - a)) ≤ ρD * ((T + u - c) * (b - a)) :=
      mul_le_mul_of_nonneg_left k3 hρD
    have key : m * (b - a) ≤ (ρU * (b - T) + ρD * (T + u - c)) * (b - a) := by nlinarith
    exact le_of_mul_le_mul_right key hba

end ZMTreeM

end SquarePacking
