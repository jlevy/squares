import Mathlib

/-!
# A concave function on a bounded polygon attains its minimum at a vertex

A polygon is given by a finite list `cs` of half-planes `a * x + b * y + k ≥ 0`.
`exists_vertex_le` : if `poly cs` is bounded and `f` is concave on it, then for every point
`p ∈ poly cs` there is a vertex `v` of the arrangement (two constraints with independent normals
tight at `v`) with `v ∈ poly cs` and `f v ≤ f p`.

The proof is an elementary rank-increasing walk (no Krein–Milman).  For a direction `d ≠ 0`
along which every constraint tight at `p` is constant, walk from `p` in directions `d` and `-d`
until a new constraint becomes tight; the two ends exist because the polygon is bounded and are
given explicitly as minima over the finitely many blocking constraints.  By concavity `f` is at
most `f p` at one of the two ends.  Starting from a tight constraint with normal `(a, b) ≠ 0`
and walking along `(-b, a)` produces a vertex; if no such constraint is tight, one preliminary
walk along `(1, 0)` creates one.
-/

namespace SquarePacking.PolyMin

/-- The polygon cut out by the half-planes `(a, b, k)`, i.e. `a * x + b * y + k ≥ 0`. -/
def poly (cs : List (ℝ × ℝ × ℝ)) : Set (ℝ × ℝ) :=
  {p | ∀ c ∈ cs, 0 ≤ c.1 * p.1 + c.2.1 * p.2 + c.2.2}

/-- `p` is a vertex of the arrangement: two constraints of `cs` with independent normals are
tight at `p`. -/
def IsVertex (cs : List (ℝ × ℝ × ℝ)) (p : ℝ × ℝ) : Prop :=
  ∃ c ∈ cs, ∃ d ∈ cs, c.1 * d.2.1 - c.2.1 * d.1 ≠ 0 ∧
    c.1 * p.1 + c.2.1 * p.2 + c.2.2 = 0 ∧ d.1 * p.1 + d.2.1 * p.2 + d.2.2 = 0

/-- The value of the affine form of a constraint at a point. -/
def val (c : ℝ × ℝ × ℝ) (p : ℝ × ℝ) : ℝ := c.1 * p.1 + c.2.1 * p.2 + c.2.2

/-- The linear part of a constraint applied to a direction. -/
def dot (c : ℝ × ℝ × ℝ) (d : ℝ × ℝ) : ℝ := c.1 * d.1 + c.2.1 * d.2

lemma val_add_smul (c : ℝ × ℝ × ℝ) (p d : ℝ × ℝ) (t : ℝ) :
    val c (p + t • d) = val c p + t * dot c d := by
  simp only [val, dot, Prod.fst_add, Prod.snd_add, Prod.smul_fst, Prod.smul_snd, smul_eq_mul]
  ring

lemma mem_poly {cs : List (ℝ × ℝ × ℝ)} {p : ℝ × ℝ} :
    p ∈ poly cs ↔ ∀ c ∈ cs, 0 ≤ val c p := Iff.rfl

/-- In a bounded polygon every ray from a point is blocked by some constraint. -/
lemma exists_neg_dot {cs : List (ℝ × ℝ × ℝ)} (hb : Bornology.IsBounded (poly cs))
    {p : ℝ × ℝ} (hp : p ∈ poly cs) {d : ℝ × ℝ} (hd : d ≠ 0) :
    ∃ c ∈ cs, dot c d < 0 := by
  by_contra h
  simp only [not_exists, not_and, not_lt] at h
  have hp' := mem_poly.1 hp
  have hray : ∀ t : ℝ, 0 ≤ t → p + t • d ∈ poly cs := by
    intro t ht
    refine mem_poly.2 fun c hc => ?_
    rw [val_add_smul]
    have h1 := hp' c hc
    have h2 := h c hc
    nlinarith
  obtain ⟨R, hR⟩ := isBounded_iff_forall_norm_le.1 hb
  have hdpos : 0 < ‖d‖ := norm_pos_iff.2 hd
  have hR0 : 0 ≤ R := le_trans (norm_nonneg _) (hR p hp)
  have ht : 0 ≤ (R + ‖p‖ + 1) / ‖d‖ := by positivity
  have h1 := hR _ (hray _ ht)
  have h2 : ‖((R + ‖p‖ + 1) / ‖d‖) • d‖ ≤ ‖p + ((R + ‖p‖ + 1) / ‖d‖) • d‖ + ‖p‖ := by
    calc ‖((R + ‖p‖ + 1) / ‖d‖) • d‖ = ‖(p + ((R + ‖p‖ + 1) / ‖d‖) • d) - p‖ := by simp
      _ ≤ ‖p + ((R + ‖p‖ + 1) / ‖d‖) • d‖ + ‖p‖ := norm_sub_le _ _
  rw [norm_smul, Real.norm_of_nonneg ht, div_mul_cancel₀ _ hdpos.ne'] at h2
  linarith

/-- Walking from `p` along `d` stays in the polygon up to a point where a constraint with
`dot c d < 0` becomes tight. -/
lemma exists_ray_end {cs : List (ℝ × ℝ × ℝ)} (hb : Bornology.IsBounded (poly cs))
    {p : ℝ × ℝ} (hp : p ∈ poly cs) {d : ℝ × ℝ} (hd : d ≠ 0) :
    ∃ t : ℝ, 0 ≤ t ∧ p + t • d ∈ poly cs ∧
      ∃ c ∈ cs, dot c d < 0 ∧ val c (p + t • d) = 0 := by
  classical
  obtain ⟨c0, hc0, hc0d⟩ := exists_neg_dot hb hp hd
  have hp' := mem_poly.1 hp
  have hB : c0 ∈ cs.toFinset.filter (fun c => dot c d < 0) :=
    Finset.mem_filter.2 ⟨List.mem_toFinset.2 hc0, hc0d⟩
  obtain ⟨c, hcB, hmin⟩ := Finset.exists_min_image (cs.toFinset.filter (fun c => dot c d < 0))
    (fun c => val c p / (-dot c d)) ⟨c0, hB⟩
  obtain ⟨hc, hcd⟩ := Finset.mem_filter.1 hcB
  have hc := List.mem_toFinset.1 hc
  have hcv := hp' c hc
  have hneg : 0 < -dot c d := by linarith
  refine ⟨val c p / (-dot c d), div_nonneg hcv hneg.le, ?_, c, hc, hcd, ?_⟩
  · refine mem_poly.2 fun c' hc' => ?_
    rw [val_add_smul]
    have hv' := hp' c' hc'
    rcases lt_or_ge (dot c' d) 0 with h' | h'
    · have hle := hmin c' (Finset.mem_filter.2 ⟨List.mem_toFinset.2 hc', h'⟩)
      have hneg' : 0 < -dot c' d := by linarith
      have := (le_div_iff₀ hneg').1 hle
      nlinarith
    · have := div_nonneg hcv hneg.le
      nlinarith
  · rw [val_add_smul]
    have := div_mul_cancel₀ (val c p) hneg.ne'
    linear_combination (-1 : ℝ) * this

/-- **Step lemma.** If `d ≠ 0`, then some point `q = p + s • d` of the polygon has `f q ≤ f p`
and a constraint `c` with `dot c d ≠ 0` tight at `q`. -/
lemma exists_step {cs : List (ℝ × ℝ × ℝ)} (hb : Bornology.IsBounded (poly cs))
    {f : ℝ × ℝ → ℝ} (hf : ConcaveOn ℝ (poly cs) f) {p : ℝ × ℝ} (hp : p ∈ poly cs)
    {d : ℝ × ℝ} (hd : d ≠ 0) :
    ∃ q ∈ poly cs, f q ≤ f p ∧ (∃ s : ℝ, q = p + s • d) ∧
      ∃ c ∈ cs, dot c d ≠ 0 ∧ val c q = 0 := by
  obtain ⟨t₁, ht₁, hq₁, c₁, hc₁, hc₁d, hc₁v⟩ := exists_ray_end hb hp hd
  obtain ⟨t₂, ht₂, hq₂, c₂, hc₂, hc₂d, hc₂v⟩ := exists_ray_end hb hp (neg_ne_zero.2 hd)
  have hc₂d' : dot c₂ d ≠ 0 := by
    intro h0
    simp only [dot, Prod.fst_neg, Prod.snd_neg] at hc₂d h0
    linarith
  rcases ht₁.eq_or_lt with h0 | hpos
  · refine ⟨p + t₁ • d, hq₁, ?_, ⟨t₁, rfl⟩, c₁, hc₁, hc₁d.ne, hc₁v⟩
    rw [← h0, zero_smul, add_zero]
  · have hsum : 0 < t₁ + t₂ := by linarith
    obtain ⟨a, ha_def⟩ : ∃ a : ℝ, a = t₂ / (t₁ + t₂) := ⟨_, rfl⟩
    obtain ⟨b, hb_def⟩ : ∃ b : ℝ, b = t₁ / (t₁ + t₂) := ⟨_, rfl⟩
    have ha : 0 ≤ a := by rw [ha_def]; positivity
    have hbpos : 0 < b := by rw [hb_def]; positivity
    have hab : a + b = 1 := by
      rw [ha_def, hb_def, ← add_div, add_comm]
      exact div_self hsum.ne'
    have hat : a * t₁ = b * t₂ := by rw [ha_def, hb_def]; ring
    have hcomb : a • (p + t₁ • d) + b • (p + t₂ • -d) = p := by
      ext
      · simp only [Prod.fst_add, Prod.smul_fst, Prod.fst_neg, smul_eq_mul]
        linear_combination p.1 * hab + d.1 * hat
      · simp only [Prod.snd_add, Prod.smul_snd, Prod.snd_neg, smul_eq_mul]
        linear_combination p.2 * hab + d.2 * hat
    have hconc := hf.2 hq₁ hq₂ ha hbpos.le hab
    rw [hcomb, smul_eq_mul, smul_eq_mul] at hconc
    by_cases h : f (p + t₁ • d) ≤ f p
    · exact ⟨_, hq₁, h, ⟨t₁, rfl⟩, c₁, hc₁, hc₁d.ne, hc₁v⟩
    · refine ⟨_, hq₂, ?_, ⟨-t₂, by rw [smul_neg, neg_smul]⟩, c₂, hc₂, hc₂d', hc₂v⟩
      by_contra h'
      have hfp : a * f p + b * f p = f p := by rw [← add_mul, hab, one_mul]
      nlinarith [mul_lt_mul_of_pos_left (not_le.1 h') hbpos,
        mul_le_mul_of_nonneg_left (not_le.1 h).le ha]

/-- From a point where a constraint with nonzero normal is tight, one step along that
constraint reaches a vertex without increasing `f`. -/
lemma exists_vertex_of_tight {cs : List (ℝ × ℝ × ℝ)} (hb : Bornology.IsBounded (poly cs))
    {f : ℝ × ℝ → ℝ} (hf : ConcaveOn ℝ (poly cs) f) {p : ℝ × ℝ} (hp : p ∈ poly cs)
    {c : ℝ × ℝ × ℝ} (hc : c ∈ cs) (hcp : val c p = 0) (hn : c.1 ≠ 0 ∨ c.2.1 ≠ 0) :
    ∃ v ∈ poly cs, IsVertex cs v ∧ f v ≤ f p := by
  have hd : ((-c.2.1, c.1) : ℝ × ℝ) ≠ 0 := by
    intro h
    have h1 := congrArg Prod.fst h
    have h2 := congrArg Prod.snd h
    simp only [Prod.fst_zero, Prod.snd_zero, neg_eq_zero] at h1 h2
    rcases hn with hn | hn
    · exact hn h2
    · exact hn h1
  obtain ⟨q, hq, hfq, ⟨s, rfl⟩, c', hc', hc'd, hc'q⟩ := exists_step hb hf hp hd
  refine ⟨_, hq, ⟨c, hc, c', hc', ?_, ?_, hc'q⟩, hfq⟩
  · intro h
    apply hc'd
    dsimp only [dot]
    linear_combination h
  · show val c _ = 0
    rw [val_add_smul, hcp]
    dsimp only [dot]
    ring

/-- **Main theorem.** A function concave on a bounded polygon is, at every point of it, at least
its value at some vertex of the polygon. -/
theorem exists_vertex_le (cs : List (ℝ × ℝ × ℝ)) (hb : Bornology.IsBounded (poly cs))
    (f : ℝ × ℝ → ℝ) (hf : ConcaveOn ℝ (poly cs) f) {p : ℝ × ℝ} (hp : p ∈ poly cs) :
    ∃ v ∈ poly cs, IsVertex cs v ∧ f v ≤ f p := by
  rcases em (∃ c ∈ cs, val c p = 0 ∧ (c.1 ≠ 0 ∨ c.2.1 ≠ 0)) with ⟨c, hc, hcp, hn⟩ | -
  · exact exists_vertex_of_tight hb hf hp hc hcp hn
  · have hd : ((1, 0) : ℝ × ℝ) ≠ 0 := by
      intro h1
      have := congrArg Prod.fst h1
      simp at this
    obtain ⟨q, hq, hfq, -, c', hc', hc'd, hc'q⟩ := exists_step hb hf hp hd
    have hn : c'.1 ≠ 0 ∨ c'.2.1 ≠ 0 := by
      left
      intro h0
      apply hc'd
      dsimp only [dot]
      rw [h0]
      ring
    obtain ⟨v, hv, hvv, hfv⟩ := exists_vertex_of_tight hb hf hq hc' hc'q hn
    exact ⟨v, hv, hvv, hfv.trans hfq⟩

end SquarePacking.PolyMin
