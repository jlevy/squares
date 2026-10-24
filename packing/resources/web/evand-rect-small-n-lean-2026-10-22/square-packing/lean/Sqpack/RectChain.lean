import Sqpack.Rect

/-!
# Chain tools: unit squares in a strip of height `< 2`

Reusable steps of the chain argument (`Rect3.lean`; written to be reused for `n ≥ 4`).

* `framed` — a unit square in the rectangle in a frame `(P, Q)`, `P, Q ≥ 0`: its points are
  `c + u (P, Q) + v (-Q, P)`, `|u|, |v| ≤ 1/2`, and its centre is `(P + Q)/2` from every wall.
* `separate` — two unit squares with disjoint interiors lie on opposite sides of a line
  (Mathlib's Hahn–Banach on the open squares, extended to the closed ones); `support_le/ge`.
* `upright_repl` — an upright square pushed to the left wall lies on the same side of any line
  `u·p = s`, `u₁ ≥ 0`, as the tilted one.
* `left_shelf`, `right_shelf` — if `a` is left of `b` (by centre) in a strip of height `H < 2`, every
  point of `b` at the heights of some band `[lo, lo + 1] ⊆ [0, H]` has `x ≥ 1`.  The right shelf is the
  left one for the mirror image `x ↦ L - x`.
* `witness` — which point of `b` the shelf constrains: its side vertex, or a point on an adjacent edge
  at the band's bottom or top (`Wit`, three alternatives).
-/

namespace SquarePacking

/-! ## Frames -/

/-- The points `c + u (P, Q) + v (-Q, P)`, `|u|, |v| ≤ 1/2`, all lie in `X`. -/
def FrameIn (X : Set (ℝ × ℝ)) (c : ℝ × ℝ) (P Q : ℝ) : Prop :=
  ∀ u v : ℝ, |u| ≤ 1 / 2 → |v| ≤ 1 / 2 → ((c.1 + (u * P - v * Q), c.2 + (u * Q + v * P)) : ℝ × ℝ) ∈ X

/-- A frame `(P, Q)`, `P, Q ≥ 0`, of the square (a quarter turn of `(cos θ, sin θ)`). -/
theorem frame (c : ℝ × ℝ) (θ : ℝ) : ∃ P Q : ℝ, 0 ≤ P ∧ 0 ≤ Q ∧ P ^ 2 + Q ^ 2 = 1 ∧
    P + Q = |Real.cos θ| + |Real.sin θ| ∧ FrameIn (sq c θ 1) c P Q := by
  set C := Real.cos θ; set S := Real.sin θ
  have hCS : C ^ 2 + S ^ 2 = 1 := Real.cos_sq_add_sin_sq θ
  have hn : ∀ x : ℝ, |x| ≤ 1 / 2 → |-x| ≤ 1 / 2 := fun x h => by rwa [abs_neg]
  rcases le_total 0 C with hC | hC <;> rcases le_total 0 S with hS | hS
  · exact ⟨C, S, hC, hS, hCS, by rw [abs_of_nonneg hC, abs_of_nonneg hS],
      fun u v hu hv => pt_mem_sq c θ u v hu hv⟩
  · refine ⟨-S, C, by linarith, hC, by linear_combination hCS,
      by rw [abs_of_nonneg hC, abs_of_nonpos hS]; ring, fun u v hu hv => ?_⟩
    convert pt_mem_sq c θ (-v) u (hn v hv) hu using 2 <;> simp only [C, S] <;> ring
  · refine ⟨S, -C, hS, by linarith, by linear_combination hCS,
      by rw [abs_of_nonpos hC, abs_of_nonneg hS]; ring, fun u v hu hv => ?_⟩
    convert pt_mem_sq c θ v (-u) hv (hn u hu) using 2 <;> simp only [C, S] <;> ring
  · refine ⟨-C, -S, by linarith, by linarith, by linear_combination hCS,
      by rw [abs_of_nonpos hC, abs_of_nonpos hS], fun u v hu hv => ?_⟩
    convert pt_mem_sq c θ (-u) (-v) (hn u hu) (hn v hv) using 2 <;> simp only [C, S] <;> ring

/-- A unit square in the rectangle, in a frame `(P, Q)`, with its half extent `(P + Q)/2` to every wall. -/
theorem framed {c : ℝ × ℝ} {θ L H : ℝ} (hin : sq c θ 1 ⊆ rbox L H) : ∃ P Q : ℝ, 0 ≤ P ∧ 0 ≤ Q ∧
    P ^ 2 + Q ^ 2 = 1 ∧ (P + Q) / 2 ≤ c.1 ∧ c.1 ≤ L - (P + Q) / 2 ∧ (P + Q) / 2 ≤ c.2 ∧
    c.2 ≤ H - (P + Q) / 2 ∧ FrameIn (sq c θ 1) c P Q := by
  obtain ⟨P, Q, hP, hQ, hPQ, hk, hpt⟩ := frame c θ
  obtain ⟨h1, h2, h3, h4⟩ := half_extent hin
  rw [← hk] at h1 h2 h3 h4
  exact ⟨P, Q, hP, hQ, hPQ, h1, h2, h3, h4, hpt⟩

/-! ## Separation and support -/

/-- Limit along a segment: `a + t b < s` for all `t ∈ [0,1)` gives `a + b ≤ s`. -/
theorem lim_le (a b s : ℝ) (h : ∀ t : ℝ, 0 ≤ t → t < 1 → a + t * b < s) : a + b ≤ s := by
  by_contra hc; push Not at hc
  have h0 := h 0 le_rfl one_pos; simp only [zero_mul, add_zero] at h0
  have hb : 0 < b := by linarith
  have := h ((s - a) / b) (div_nonneg (by linarith) hb.le) ((div_lt_one hb).2 (by linarith))
  rw [div_mul_cancel₀ _ hb.ne'] at this; linarith

lemma sqInt_shrink {c p : ℝ × ℝ} {θ t : ℝ} (hp : p ∈ sq c θ 1) (ht0 : 0 ≤ t) (ht1 : t < 1) :
    (c.1 + t * (p.1 - c.1), c.2 + t * (p.2 - c.2)) ∈ sqInt c θ 1 := by
  have e : coord c θ (c.1 + t * (p.1 - c.1), c.2 + t * (p.2 - c.2)) =
      (t * (coord c θ p).1, t * (coord c θ p).2) := by simp only [coord]; ext <;> ring
  obtain ⟨h1, h2⟩ := hp
  simp only [sqInt, Set.mem_ofPred_eq, e, abs_mul, abs_of_nonneg ht0]
  constructor <;> nlinarith

/-- A linear bound on the open square extends to the closed square. -/
lemma lin_le_of_sqInt {c : ℝ × ℝ} {θ u1 u2 s : ℝ}
    (h : ∀ q ∈ sqInt c θ 1, u1 * q.1 + u2 * q.2 < s) : ∀ p ∈ sq c θ 1, u1 * p.1 + u2 * p.2 ≤ s := by
  intro p hp
  have := lim_le (u1 * c.1 + u2 * c.2) (u1 * (p.1 - c.1) + u2 * (p.2 - c.2)) s (fun t ht0 ht1 => by
    have := h _ (sqInt_shrink hp ht0 ht1); simp only at this; linarith)
  linarith

lemma ctr_mem_sqInt (c : ℝ × ℝ) (θ : ℝ) : c ∈ sqInt c θ 1 := by
  simp [sqInt, coord]

lemma sqInt_isOpen (c : ℝ × ℝ) (θ : ℝ) : IsOpen (sqInt c θ 1) := by
  have h1 : Continuous fun p : ℝ × ℝ => |(coord c θ p).1| := by unfold coord; fun_prop
  have h2 : Continuous fun p : ℝ × ℝ => |(coord c θ p).2| := by unfold coord; fun_prop
  exact (isOpen_lt h1 continuous_const).inter (isOpen_lt h2 continuous_const)

lemma sqInt_convex (c : ℝ × ℝ) (θ : ℝ) : Convex ℝ (sqInt c θ 1) := by
  intro p hp q hq a b ha hb hab
  obtain ⟨hp1, hp2⟩ := hp; obtain ⟨hq1, hq2⟩ := hq
  have e : coord c θ (a • p + b • q) = (a * (coord c θ p).1 + b * (coord c θ q).1,
      a * (coord c θ p).2 + b * (coord c θ q).2) := by
    simp only [coord, Prod.fst_add, Prod.snd_add, Prod.smul_fst, Prod.smul_snd, smul_eq_mul]
    ext
    · simp only; linear_combination (c.1 * Real.cos θ + c.2 * Real.sin θ) * hab
    · simp only; linear_combination (-c.1 * Real.sin θ + c.2 * Real.cos θ) * hab
  have key : ∀ x y : ℝ, |x| < 1 / 2 → |y| < 1 / 2 → |a * x + b * y| < 1 / 2 := by
    intro x y hx hy
    calc |a * x + b * y| ≤ a * |x| + b * |y| := by
          calc |a * x + b * y| ≤ |a * x| + |b * y| := abs_add_le _ _
            _ = a * |x| + b * |y| := by rw [abs_mul, abs_mul, abs_of_nonneg ha, abs_of_nonneg hb]
      _ < 1 / 2 := by
          rcases eq_or_lt_of_le ha with h0 | h0
          · subst h0; simp at hab; subst hab; simpa using hy
          · nlinarith [abs_nonneg x, abs_nonneg y]
  simp only [sqInt, Set.mem_ofPred_eq, e]
  exact ⟨key _ _ hp1 hq1, key _ _ hp2 hq2⟩

/-- **Separation.**  Two unit squares with disjoint interiors lie on opposite sides of a line. -/
theorem separate {ca cb : ℝ × ℝ} {θa θb : ℝ} (hd : Disjoint (sqInt ca θa 1) (sqInt cb θb 1)) :
    ∃ u1 u2 s : ℝ, (u1 ≠ 0 ∨ u2 ≠ 0) ∧ (∀ p ∈ sq ca θa 1, u1 * p.1 + u2 * p.2 ≤ s) ∧
      (∀ p ∈ sq cb θb 1, s ≤ u1 * p.1 + u2 * p.2) := by
  obtain ⟨f, s, hf1, hf2⟩ := geometric_hahn_banach_open_open (sqInt_convex ca θa) (sqInt_isOpen ca θa)
    (sqInt_convex cb θb) (sqInt_isOpen cb θb) hd
  have hf : ∀ p : ℝ × ℝ, f p = f (1, 0) * p.1 + f (0, 1) * p.2 := by
    intro p
    have : p = p.1 • ((1 : ℝ), (0 : ℝ)) + p.2 • ((0 : ℝ), (1 : ℝ)) := by ext <;> simp
    conv_lhs => rw [this]
    rw [map_add, map_smul, map_smul, smul_eq_mul, smul_eq_mul]; ring
  refine ⟨f (1, 0), f (0, 1), s, ?_, ?_, ?_⟩
  · by_contra h0; push Not at h0
    have a := hf1 ca (ctr_mem_sqInt ca θa); have b := hf2 cb (ctr_mem_sqInt cb θb)
    rw [hf, h0.1, h0.2] at a b; simp at a b; linarith
  · exact lin_le_of_sqInt (fun q hq => by rw [← hf]; exact hf1 q hq)
  · intro p hp
    have := lin_le_of_sqInt (u1 := -f (1, 0)) (u2 := -f (0, 1)) (s := -s)
      (fun q hq => by have := hf2 q hq; rw [hf] at this; linarith) p hp
    linarith

/-- **Support.**  A framed square below the line `u·p = s` has `u·c + (|u·e| + |u·e⊥|)/2 ≤ s`,
`e = (P, Q)`, `e⊥ = (-Q, P)`. -/
theorem support_le {X : Set (ℝ × ℝ)} {c : ℝ × ℝ} {P Q u1 u2 s : ℝ} (hpt : FrameIn X c P Q)
    (h : ∀ p ∈ X, u1 * p.1 + u2 * p.2 ≤ s) :
    u1 * c.1 + u2 * c.2 + (|u1 * P + u2 * Q| + |-u1 * Q + u2 * P|) / 2 ≤ s := by
  obtain ⟨a, ha, hax⟩ := sgn_half (u1 * P + u2 * Q)
  obtain ⟨b, hb, hby⟩ := sgn_half (-u1 * Q + u2 * P)
  have := h _ (hpt a b ha.le hb.le)
  simp only at this
  nlinarith [hax, hby]

theorem support_ge {X : Set (ℝ × ℝ)} {c : ℝ × ℝ} {P Q u1 u2 s : ℝ} (hpt : FrameIn X c P Q)
    (h : ∀ p ∈ X, s ≤ u1 * p.1 + u2 * p.2) :
    s ≤ u1 * c.1 + u2 * c.2 - (|u1 * P + u2 * Q| + |-u1 * Q + u2 * P|) / 2 := by
  have := support_le (u1 := -u1) (u2 := -u2) (s := -s) hpt (fun p hp => by have := h p hp; linarith)
  rw [show -u1 * P + -u2 * Q = -(u1 * P + u2 * Q) by ring,
    show - -u1 * Q + -u2 * P = -(-u1 * Q + u2 * P) by ring, abs_neg, abs_neg] at this
  linarith

/-- `|u₁|, |u₂| ≤ |u·e| + |u·e⊥|` for a unit vector `e = (C, S)`. -/
theorem abs_le_supp (C S u1 u2 : ℝ) (hCS : C^2 + S^2 = 1) :
    |u1| ≤ |u1 * C + u2 * S| + |-u1 * S + u2 * C| ∧ |u2| ≤ |u1 * C + u2 * S| + |-u1 * S + u2 * C| := by
  have hC1 : |C| ≤ 1 := by rw [abs_le]; constructor <;> nlinarith
  have hS1 : |S| ≤ 1 := by rw [abs_le]; constructor <;> nlinarith
  set X := u1 * C + u2 * S; set Y := -u1 * S + u2 * C
  have e1 : u1 = C * X - S * Y := by simp only [X, Y]; linear_combination (-u1) * hCS
  have e2 : u2 = S * X + C * Y := by simp only [X, Y]; linear_combination (-u2) * hCS
  have hX := abs_nonneg X; have hY := abs_nonneg Y
  constructor
  · rw [e1]
    calc |C * X - S * Y| ≤ |C| * |X| + |S| * |Y| := by rw [← abs_mul, ← abs_mul]; exact abs_sub _ _
      _ ≤ |X| + |Y| := by nlinarith [mul_le_mul_of_nonneg_right hC1 hX, mul_le_mul_of_nonneg_right hS1 hY]
  · rw [e2]
    calc |S * X + C * Y| ≤ |S| * |X| + |C| * |Y| := by rw [← abs_mul, ← abs_mul]; exact abs_add_le _ _
      _ ≤ |X| + |Y| := by nlinarith [mul_le_mul_of_nonneg_right hC1 hY, mul_le_mul_of_nonneg_right hS1 hX]

/-- The separating normal points right when the centres are ordered in `x` and the vertical
offset is below `1`. -/
theorem u1_pos {u1 u2 xa xb ya yb Sa Sb s : ℝ} (hu : u1 ≠ 0 ∨ u2 ≠ 0) (hx : xa ≤ xb)
    (hdy : |yb - ya| < 1)
    (ha : u1 * xa + u2 * ya + Sa / 2 ≤ s) (hb : s ≤ u1 * xb + u2 * yb - Sb / 2)
    (ha1 : |u1| ≤ Sa) (ha2 : |u2| ≤ Sa) (hb1 : |u1| ≤ Sb) (hb2 : |u2| ≤ Sb) : 0 < u1 := by
  by_contra hc; push Not at hc
  set dx := xb - xa; set dy := yb - ya
  have h : (Sa + Sb) / 2 ≤ u1 * dx + u2 * dy := by simp only [dx, dy]; linarith
  have h1 : u1 * dx ≤ 0 := mul_nonpos_of_nonpos_of_nonneg hc (by simp only [dx]; linarith)
  have h2 : u2 * dy ≤ |u2| * |dy| := by rw [← abs_mul]; exact le_abs_self _
  rcases hu with hu | hu
  · have : 0 < |u1| := abs_pos.2 hu
    nlinarith [abs_nonneg dy, abs_nonneg u2]
  · have : 0 < |u2| := abs_pos.2 hu
    nlinarith [abs_nonneg dy]

/-! ## Upright replacement -/

/-- Upright replacement, core case `u₂ ≥ 0`. -/
theorem upright_core (C S u1 u2 : ℝ) (hCS : C^2 + S^2 = 1) (hu1 : 0 ≤ u1) (hC : 0 ≤ C) (hS : 0 ≤ S)
    (hu2 : 0 ≤ u2) :
    2 * (u1 + u2) ≤ (C + S) * (u1 + u2) + |u1 * C + u2 * S| + |-u1 * S + u2 * C| := by
  have hC1 : C ≤ 1 := by nlinarith
  have hS1 : S ≤ 1 := by nlinarith
  rw [abs_of_nonneg (by positivity : 0 ≤ u1 * C + u2 * S)]
  rcases le_total 0 (-u1 * S + u2 * C) with hY | hY
  · rw [abs_of_nonneg hY]
    have h1 : 0 ≤ (1 + C) * (u2 * (C + S - 1) - u1 * (1 - C)) := by
      have e : (1 + C) * (u2 * (C + S - 1) - u1 * (1 - C)) = S * (u2 * (1 + C - S) - u1 * S) := by
        linear_combination (u1 + u2) * hCS
      rw [e]; apply mul_nonneg hS; nlinarith [mul_nonneg hu2 (sub_nonneg.2 hS1)]
    have h2 : 0 ≤ u2 * (C + S - 1) - u1 * (1 - C) := by
      by_contra h; push Not at h; nlinarith
    nlinarith
  · rw [abs_of_nonpos hY]
    have h1 : 0 ≤ (1 + S) * (u1 * (C + S - 1) - u2 * (1 - S)) := by
      have e : (1 + S) * (u1 * (C + S - 1) - u2 * (1 - S)) = C * (u1 * (1 + S - C) - u2 * C) := by
        linear_combination (u1 + u2) * hCS
      rw [e]; apply mul_nonneg hC; nlinarith [mul_nonneg hu1 (sub_nonneg.2 hC1)]
    have h2 : 0 ≤ u1 * (C + S - 1) - u2 * (1 - S) := by
      by_contra h; push Not at h; nlinarith
    nlinarith

/-- **Upright replacement.**  For a framed unit square (`P, Q ≥ 0`) and a direction `u` with `u₁ ≥ 0`:
`2 (u₁ + |u₂|) ≤ (P + Q)(u₁ + |u₂|) + |u·e| + |u·e⊥|`.  (An upright square pushed to the wall is
on the same side of any line `u·p = s`, `u₁ > 0`, as the tilted one.)  `u₂ < 0` is the vertical mirror,
which swaps `P` and `Q`. -/
theorem upright_repl (P Q u1 u2 : ℝ) (hP : 0 ≤ P) (hQ : 0 ≤ Q) (hPQ : P^2 + Q^2 = 1) (hu1 : 0 ≤ u1) :
    2 * (u1 + |u2|) ≤ (P + Q) * (u1 + |u2|) + |u1 * P + u2 * Q| + |-u1 * Q + u2 * P| := by
  rcases le_total 0 u2 with hu2 | hu2
  · rw [abs_of_nonneg hu2]; exact upright_core P Q u1 u2 hPQ hu1 hP hQ hu2
  · have := upright_core Q P u1 (-u2) (by linarith) hu1 hQ hP (by linarith)
    rw [show u1 * Q + -u2 * P = -(-u1 * Q + u2 * P) by ring, abs_neg,
      show -u1 * P + -u2 * Q = -(u1 * P + u2 * Q) by ring, abs_neg] at this
    rw [abs_of_nonpos hu2]; linarith

/-! ## Shelves -/

/-- **Separation in a strip.**  Two squares ordered by centre `x` in a strip of height `H < 2` are
separated by a line whose normal points right (`u₁ > 0`). -/
theorem separate_lr {ca cb : ℝ × ℝ} {θa θb L H : ℝ} (hA : sq ca θa 1 ⊆ rbox L H)
    (hB : sq cb θb 1 ⊆ rbox L H) (hd : Disjoint (sqInt ca θa 1) (sqInt cb θb 1))
    (hx : ca.1 ≤ cb.1) (hH : H < 2) :
    ∃ u1 u2 s : ℝ, 0 < u1 ∧ (∀ p ∈ sq ca θa 1, u1 * p.1 + u2 * p.2 ≤ s) ∧
      (∀ p ∈ sq cb θb 1, s ≤ u1 * p.1 + u2 * p.2) := by
  obtain ⟨u1, u2, s, hu, hsa, hsb⟩ := separate hd
  obtain ⟨P, Q, hP, hQ, hPQ, -, -, a3, a4, hpa⟩ := framed hA
  obtain ⟨P', Q', hP', hQ', hPQ', -, -, b3, b4, hpb⟩ := framed hB
  obtain ⟨la1, la2⟩ := abs_le_supp P Q u1 u2 hPQ
  obtain ⟨lb1, lb2⟩ := abs_le_supp P' Q' u1 u2 hPQ'
  have hk : 1 ≤ P + Q := by nlinarith
  have hk' : 1 ≤ P' + Q' := by nlinarith
  exact ⟨u1, u2, s, u1_pos hu hx (by rw [abs_lt]; constructor <;> linarith) (support_le hpa hsa)
    (support_ge hpb hsb) la1 la2 lb1 lb2, hsa, hsb⟩

/-- **Left shelf.**  If `a` is left of `b` (by centre) in a strip of height `H < 2`, some height band
`[lo, lo + 1] ⊆ [0, H]` has every point of `b` at those heights at `x ≥ 1`: the upright square
`[0,1] × [lo, lo + 1]` lies on `a`'s side of the separating line. -/
theorem left_shelf {ca cb : ℝ × ℝ} {θa θb L H : ℝ} (hA : sq ca θa 1 ⊆ rbox L H)
    (hB : sq cb θb 1 ⊆ rbox L H) (hd : Disjoint (sqInt ca θa 1) (sqInt cb θb 1))
    (hx : ca.1 ≤ cb.1) (hH : H < 2) :
    ∃ lo, 0 ≤ lo ∧ lo ≤ H - 1 ∧ ∀ p ∈ sq cb θb 1, lo ≤ p.2 → p.2 ≤ lo + 1 → 1 ≤ p.1 := by
  obtain ⟨u1, u2, s, hu1, hsa, hsb⟩ := separate_lr hA hB hd hx hH
  obtain ⟨P, Q, hP, hQ, hPQ, a1, -, a3, a4, hpa⟩ := framed hA
  have sa := support_le hpa hsa
  have hk : 1 ≤ P + Q := by nlinarith
  have rep := upright_repl P Q u1 u2 hP hQ hPQ hu1.le
  have hxa : u1 * ((P + Q) / 2) ≤ u1 * ca.1 := mul_le_mul_of_nonneg_left a1 hu1.le
  rcases le_or_gt 0 u2 with hu2 | hu2
  · rw [abs_of_nonneg hu2] at rep
    refine ⟨ca.2 - (P + Q) / 2, by linarith, by linarith, fun p hp h1 h2 => ?_⟩
    have := hsb p hp
    by_contra hc; push Not at hc
    nlinarith [mul_le_mul_of_nonneg_left h2 hu2, mul_lt_mul_of_pos_left hc hu1]
  · rw [abs_of_neg hu2] at rep
    refine ⟨ca.2 + (P + Q) / 2 - 1, by linarith, by linarith, fun p hp h1 h2 => ?_⟩
    have := hsb p hp
    by_contra hc; push Not at hc
    nlinarith [mul_le_mul_of_nonpos_left h1 hu2.le, mul_lt_mul_of_pos_left hc hu1]

/-- The mirror `x ↦ L - x`. -/
def mir (L : ℝ) (p : ℝ × ℝ) : ℝ × ℝ := (L - p.1, p.2)

lemma mir_mir (L : ℝ) (p : ℝ × ℝ) : mir L (mir L p) = p := by simp [mir]

lemma coord_mir (L : ℝ) (c p : ℝ × ℝ) (θ : ℝ) :
    coord (mir L c) (-θ) (mir L p) = (-(coord c θ p).1, (coord c θ p).2) := by
  simp only [coord, mir, Real.cos_neg, Real.sin_neg]; ext <;> simp only <;> ring

lemma mem_sq_mir (L : ℝ) (c p : ℝ × ℝ) (θ : ℝ) : mir L p ∈ sq (mir L c) (-θ) 1 ↔ p ∈ sq c θ 1 := by
  simp only [sq, Set.mem_ofPred_eq, coord_mir, abs_neg]

lemma mem_sqInt_mir (L : ℝ) (c p : ℝ × ℝ) (θ : ℝ) :
    mir L p ∈ sqInt (mir L c) (-θ) 1 ↔ p ∈ sqInt c θ 1 := by
  simp only [sqInt, Set.mem_ofPred_eq, coord_mir, abs_neg]

lemma sq_mir_subset {c : ℝ × ℝ} {θ L H : ℝ} (h : sq c θ 1 ⊆ rbox L H) :
    sq (mir L c) (-θ) 1 ⊆ rbox L H := by
  intro p hp
  rw [← mir_mir L p, mem_sq_mir] at hp
  have := h hp
  simp only [rbox, mir, Set.mem_ofPred_eq] at this ⊢
  exact ⟨by linarith, by linarith, this.2.2.1, this.2.2.2⟩

lemma disj_mir {ca cb : ℝ × ℝ} {θa θb : ℝ} (L : ℝ) (hd : Disjoint (sqInt ca θa 1) (sqInt cb θb 1)) :
    Disjoint (sqInt (mir L ca) (-θa) 1) (sqInt (mir L cb) (-θb) 1) := by
  rw [Set.disjoint_left]
  intro p h1 h2
  rw [← mir_mir L p, mem_sqInt_mir] at h1 h2
  exact Set.disjoint_left.1 hd h1 h2

/-- The mirror `y ↦ H - y`. -/
def vmir (H : ℝ) (p : ℝ × ℝ) : ℝ × ℝ := (p.1, H - p.2)

lemma vmir_vmir (H : ℝ) (p : ℝ × ℝ) : vmir H (vmir H p) = p := by simp [vmir]

lemma mem_sq_vmir (H : ℝ) (c p : ℝ × ℝ) (θ : ℝ) :
    vmir H p ∈ sq (vmir H c) (-θ) 1 ↔ p ∈ sq c θ 1 := by
  have e : coord (vmir H c) (-θ) (vmir H p) = ((coord c θ p).1, -(coord c θ p).2) := by
    simp only [coord, vmir, Real.cos_neg, Real.sin_neg]; ext <;> simp only <;> ring
  simp only [sq, Set.mem_ofPred_eq, e, abs_neg]

lemma sq_vmir_subset {c : ℝ × ℝ} {θ L H : ℝ} (h : sq c θ 1 ⊆ rbox L H) :
    sq (vmir H c) (-θ) 1 ⊆ rbox L H := by
  intro p hp
  rw [← vmir_vmir H p, mem_sq_vmir] at hp
  have := h hp
  simp only [rbox, vmir, Set.mem_ofPred_eq] at this ⊢
  exact ⟨this.1, this.2.1, by linarith, by linarith⟩

/-- The half turn `p ↦ (L, H) - p` about the rectangle's centre. -/
def rot (L H : ℝ) (p : ℝ × ℝ) : ℝ × ℝ := (L - p.1, H - p.2)

lemma rot_rot (L H : ℝ) (p : ℝ × ℝ) : rot L H (rot L H p) = p := by simp [rot]

lemma mem_sq_rot (L H : ℝ) (c p : ℝ × ℝ) (θ : ℝ) :
    rot L H p ∈ sq (rot L H c) θ 1 ↔ p ∈ sq c θ 1 := by
  have e : coord (rot L H c) θ (rot L H p) = (-(coord c θ p).1, -(coord c θ p).2) := by
    simp only [coord, rot]; ext <;> simp only <;> ring
  simp only [sq, Set.mem_ofPred_eq, e, abs_neg]

lemma sq_rot_subset {c : ℝ × ℝ} {θ L H : ℝ} (h : sq c θ 1 ⊆ rbox L H) :
    sq (rot L H c) θ 1 ⊆ rbox L H := by
  intro p hp
  rw [← rot_rot L H p, mem_sq_rot] at hp
  have := h hp
  simp only [rbox, rot, Set.mem_ofPred_eq] at this ⊢
  exact ⟨by linarith, by linarith, by linarith, by linarith⟩

/-- **Right shelf**, the left shelf of the mirror image: points of `b` at the band's heights have
`x ≤ L - 1`. -/
theorem right_shelf {cb cc : ℝ × ℝ} {θb θc L H : ℝ} (hB : sq cb θb 1 ⊆ rbox L H)
    (hC : sq cc θc 1 ⊆ rbox L H) (hd : Disjoint (sqInt cb θb 1) (sqInt cc θc 1))
    (hx : cb.1 ≤ cc.1) (hH : H < 2) :
    ∃ lo, 0 ≤ lo ∧ lo ≤ H - 1 ∧ ∀ p ∈ sq cb θb 1, lo ≤ p.2 → p.2 ≤ lo + 1 → p.1 ≤ L - 1 := by
  obtain ⟨lo, h0, h1, h⟩ := left_shelf (sq_mir_subset hC) (sq_mir_subset hB) (disj_mir L hd.symm)
    (by simp only [mir]; linarith) hH
  refine ⟨lo, h0, h1, fun p hp hl hu => ?_⟩
  have := h (mir L p) ((mem_sq_mir L cb p θb).2 hp) hl hu
  simp only [mir] at this; linarith

/-! ## Witnesses -/

/-- What a left shelf `[lo, lo + 1]` gives for a square with frame `(P, Q)` and centre height `y`, in
terms of its left gap `A = x - 1 - (P + Q)/2`: its left vertex (height `y + (P - Q)/2`) is right of the
wall square (`A ≥ 0`), or the edge above it crosses the band's bottom right of it, or the edge below it
crosses the band's top right of it. -/
def Wit (P Q y lo A : ℝ) : Prop :=
  0 ≤ A ∨ (y + (P - Q) / 2 < lo ∧ lo ≤ y + (P + Q) / 2 ∧ 0 ≤ Q * A + P * (lo - (y + (P - Q) / 2))) ∨
    (lo + 1 < y + (P - Q) / 2 ∧ y - (P + Q) / 2 ≤ lo + 1 ∧ 0 ≤ P * A + Q * (y + (P - Q) / 2 - lo - 1))

/-- **Witness.**  The square's points at heights `[lo, lo + 1]` all have `x ≥ 1`; the witness is its left
vertex if the band contains it, else the point on the adjacent edge at the band's near end. -/
theorem witness {P Q x y lo : ℝ}
    (htop : lo ≤ y + (P + Q) / 2) (hbot : y - (P + Q) / 2 ≤ lo + 1)
    (hl : ∀ u v : ℝ, |u| ≤ 1 / 2 → |v| ≤ 1 / 2 → lo ≤ y + (u * Q + v * P) →
      y + (u * Q + v * P) ≤ lo + 1 → 1 ≤ x + (u * P - v * Q)) :
    Wit P Q y lo (x - 1 - (P + Q) / 2) := by
  have hh : |(1 / 2 : ℝ)| ≤ 1 / 2 := by norm_num
  have hmh : |(-(1 / 2) : ℝ)| ≤ 1 / 2 := by norm_num
  rcases lt_or_ge (y + (P - Q) / 2) lo with h | h
  · -- the edge from the left vertex up to the top vertex (`v = 1/2`), at height `lo`
    have hQ0 : 0 < Q := by linarith
    set u := (lo - y - P / 2) / Q
    have huQ : u * Q = lo - y - P / 2 := by simp only [u]; field_simp
    have hu : |u| ≤ 1 / 2 := by
      rw [abs_le]; constructor
      · rw [le_div_iff₀ hQ0]; linarith
      · rw [div_le_iff₀ hQ0]; linarith
    have := hl u (1 / 2) hu hh (by linarith) (by linarith)
    right; left
    refine ⟨h, htop, ?_⟩
    have e : Q * (x - 1 - (P + Q) / 2) + P * (lo - (y + (P - Q) / 2)) = Q * (x + (u * P - 1 / 2 * Q) - 1) := by
      linear_combination (-P) * huQ
    rw [e]; exact mul_nonneg hQ0.le (by linarith)
  rcases le_or_gt (y + (P - Q) / 2) (lo + 1) with h' | h'
  · -- the left vertex itself
    have := hl (-(1 / 2)) (1 / 2) hmh hh (by linarith) (by linarith)
    left; linarith
  · -- the edge from the left vertex down to the bottom vertex (`u = -1/2`), at height `lo + 1`
    have hP0 : 0 < P := by linarith
    set v := (lo + 1 - y + Q / 2) / P
    have hvP : v * P = lo + 1 - y + Q / 2 := by simp only [v]; field_simp
    have hv : |v| ≤ 1 / 2 := by
      rw [abs_le]; constructor
      · rw [le_div_iff₀ hP0]; linarith
      · rw [div_le_iff₀ hP0]; linarith
    have := hl (-(1 / 2)) v hmh hv (by linarith) (by linarith)
    right; right
    refine ⟨h', hbot, ?_⟩
    have e : P * (x - 1 - (P + Q) / 2) + Q * (y + (P - Q) / 2 - lo - 1) = P * (x + (-(1 / 2) * P - v * Q) - 1) := by
      linear_combination Q * hvP
    rw [e]; exact mul_nonneg hP0.le (by linarith)

/-- Both witnesses for a square `b` between a left and a right shelf: the right one is the left one of
the mirror image (frame `(Q, P)`, gap `B = (L - x) - 1 - (P + Q)/2`). -/
theorem witnesses {cb : ℝ × ℝ} {θb L H lo lo2 P Q : ℝ}
    (hk : 1 ≤ P + Q) (hH : H < 2) (hy1 : (P + Q) / 2 ≤ cb.2) (hy2 : cb.2 ≤ H - (P + Q) / 2)
    (hlo : 0 ≤ lo) (hlo' : lo ≤ H - 1) (hlo2 : 0 ≤ lo2) (hlo2' : lo2 ≤ H - 1)
    (hpt : FrameIn (sq cb θb 1) cb P Q)
    (hl : ∀ p ∈ sq cb θb 1, lo ≤ p.2 → p.2 ≤ lo + 1 → 1 ≤ p.1)
    (hr : ∀ p ∈ sq cb θb 1, lo2 ≤ p.2 → p.2 ≤ lo2 + 1 → p.1 ≤ L - 1) :
    Wit P Q cb.2 lo (cb.1 - 1 - (P + Q) / 2) ∧ Wit Q P cb.2 lo2 (L - cb.1 - 1 - (Q + P) / 2) := by
  refine ⟨witness (by linarith) (by linarith) fun u v hu hv h1 h2 => hl _ (hpt u v hu hv) h1 h2,
    witness (by linarith) (by linarith) fun u v hu hv h1 h2 => ?_⟩
  have := hr _ (hpt v u hv hu) (by simp only; linarith) (by simp only; linarith)
  simp only at this; linarith

end SquarePacking
