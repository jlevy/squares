import Sqpack.Basic

/-!
# Unit squares in rectangles: small `n`

`RectPacks n w h`: `n` closed unit squares (any angles) in `[0,w] × [0,h]` with pairwise disjoint
interiors.  The region `R_n = {(w, h) | RectPacks n w h}` is the object; this file starts the ladder.

* `half_extent` — a unit square of angle `θ` in the rectangle keeps its centre at distance at least
  `k = (|cos θ| + |sin θ|)/2` from every wall.
* `mem_sqInt_of_close` — the point `m` lies in the open square whenever both coordinates of `m - c` are
  smaller than `1 - k` in absolute value (because `2k(1-k) ≤ 1/2`).
* `rect2` — two unit squares need `2 ≤ w` or `2 ≤ h`: in a rectangle with both sides `< 2` every
  unit square contains the centre of the rectangle in its interior.
-/

namespace SquarePacking

/-- The rectangle `[0,w] × [0,h]`. -/
def rbox (w h : ℝ) : Set (ℝ × ℝ) := {p | 0 ≤ p.1 ∧ p.1 ≤ w ∧ 0 ≤ p.2 ∧ p.2 ≤ h}

/-- `n` closed unit squares in `[0,w] × [0,h]` with pairwise disjoint interiors. -/
def RectPacks (n : ℕ) (w h : ℝ) : Prop :=
  ∃ (ctr : Fin n → ℝ × ℝ) (ang : Fin n → ℝ), (∀ i, sq (ctr i) (ang i) 1 ⊆ rbox w h) ∧
    ∀ i j, i ≠ j → Disjoint (sqInt (ctr i) (ang i) 1) (sqInt (ctr j) (ang j) 1)

/-- The point with rotated coordinates `(u, v)` lies in the closed unit square when `|u|, |v| ≤ 1/2`. -/
lemma pt_mem_sq (c : ℝ × ℝ) (θ u v : ℝ) (hu : |u| ≤ 1 / 2) (hv : |v| ≤ 1 / 2) :
    (c.1 + (u * Real.cos θ - v * Real.sin θ), c.2 + (u * Real.sin θ + v * Real.cos θ)) ∈ sq c θ 1 := by
  have hCS : Real.cos θ ^ 2 + Real.sin θ ^ 2 = 1 := Real.cos_sq_add_sin_sq θ
  refine ⟨?_, ?_⟩
  · have : (coord c θ (c.1 + (u * Real.cos θ - v * Real.sin θ),
        c.2 + (u * Real.sin θ + v * Real.cos θ))).1 = u * (Real.cos θ ^ 2 + Real.sin θ ^ 2) := by
      simp only [coord]; ring
    rw [this, hCS, mul_one]; linarith
  · have : (coord c θ (c.1 + (u * Real.cos θ - v * Real.sin θ),
        c.2 + (u * Real.sin θ + v * Real.cos θ))).2 = v * (Real.cos θ ^ 2 + Real.sin θ ^ 2) := by
      simp only [coord]; ring
    rw [this, hCS, mul_one]; linarith

/-- `|a|/2` as `±a/2` with the sign chosen by `a`. -/
lemma sgn_half (a : ℝ) : ∃ s : ℝ, |s| = 1 / 2 ∧ s * a = |a| / 2 := by
  rcases le_or_gt 0 a with h | h
  · exact ⟨1 / 2, by norm_num, by rw [abs_of_nonneg h]; ring⟩
  · exact ⟨-(1 / 2), by norm_num, by rw [abs_of_neg h]; ring⟩

/-- **Half extents.**  A closed unit square of angle `θ` in `[0,w] × [0,h]` has its centre at distance
at least `(|cos θ| + |sin θ|)/2` from each of the four walls. -/
lemma half_extent {c : ℝ × ℝ} {θ w h : ℝ} (hin : sq c θ 1 ⊆ rbox w h) :
    (|Real.cos θ| + |Real.sin θ|) / 2 ≤ c.1 ∧ c.1 ≤ w - (|Real.cos θ| + |Real.sin θ|) / 2 ∧
    (|Real.cos θ| + |Real.sin θ|) / 2 ≤ c.2 ∧ c.2 ≤ h - (|Real.cos θ| + |Real.sin θ|) / 2 := by
  obtain ⟨a, ha, hac⟩ := sgn_half (Real.cos θ)
  obtain ⟨b, hb, hbs⟩ := sgn_half (Real.sin θ)
  have hb' : |-b| = 1 / 2 := by rw [abs_neg, hb]
  have ha' : |-a| = 1 / 2 := by rw [abs_neg, ha]
  -- x: corner (u, v) = (a, -b) has x-offset (|C| + |S|)/2; (-a, b) has the opposite.
  have p1 := hin (pt_mem_sq c θ a (-b) (le_of_eq ha) (le_of_eq hb'))
  have p2 := hin (pt_mem_sq c θ (-a) b (le_of_eq ha') (le_of_eq hb))
  -- y: corner (b, a) has y-offset (|S| + |C|)/2; (-b, -a) the opposite.
  have p3 := hin (pt_mem_sq c θ b a (le_of_eq hb) (le_of_eq ha))
  have p4 := hin (pt_mem_sq c θ (-b) (-a) (le_of_eq hb') (le_of_eq ha'))
  simp only [rbox, Set.mem_ofPred_eq] at p1 p2 p3 p4
  refine ⟨?_, ?_, ?_, ?_⟩ <;> nlinarith [p1, p2, p3, p4]

/-- `|cos θ| + |sin θ| ≥ 1`. -/
lemma one_le_abs_cos_add_abs_sin (θ : ℝ) : 1 ≤ |Real.cos θ| + |Real.sin θ| := by
  have hCS : |Real.cos θ| ^ 2 + |Real.sin θ| ^ 2 = 1 := by
    rw [sq_abs, sq_abs]; exact Real.cos_sq_add_sin_sq θ
  nlinarith [abs_nonneg (Real.cos θ), abs_nonneg (Real.sin θ),
    mul_nonneg (abs_nonneg (Real.cos θ)) (abs_nonneg (Real.sin θ))]

/-- **The close-point lemma.**  With `k = (|cos θ| + |sin θ|)/2`, a point `m` with
`|m.1 - c.1| < 1 - k` and `|m.2 - c.2| < 1 - k` lies in the open unit square: both rotated coordinates
are below `(1 - k) · 2k ≤ 1/2`. -/
lemma mem_sqInt_of_close {c m : ℝ × ℝ} {θ : ℝ}
    (hx : |m.1 - c.1| < 1 - (|Real.cos θ| + |Real.sin θ|) / 2)
    (hy : |m.2 - c.2| < 1 - (|Real.cos θ| + |Real.sin θ|) / 2) :
    m ∈ sqInt c θ 1 := by
  set C := Real.cos θ; set S := Real.sin θ
  set k := (|C| + |S|) / 2 with hk
  have hk1 : 1 ≤ 2 * k := by rw [hk]; linarith [one_le_abs_cos_add_abs_sin θ]
  have hbnd : ∀ x y : ℝ, |x| < 1 - k → |y| < 1 - k → |x * C + y * S| < 1 / 2 := by
    intro x y hx hy
    have h1 : |x * C + y * S| ≤ |x| * |C| + |y| * |S| := by
      calc |x * C + y * S| ≤ |x * C| + |y * S| := abs_add_le _ _
        _ = |x| * |C| + |y| * |S| := by rw [abs_mul, abs_mul]
    have h2 : |x| * |C| + |y| * |S| < (1 - k) * (2 * k) := by
      have hC := abs_nonneg C; have hS := abs_nonneg S
      have : |x| * |C| + |y| * |S| ≤ (1 - k) * |C| + (1 - k) * |S| := by
        nlinarith [abs_nonneg x, abs_nonneg y]
      have hpos : 0 < |C| + |S| := by linarith
      rcases (lt_or_ge 0 |C|) with hCp | hC0
      · have : |x| * |C| < (1 - k) * |C| := by nlinarith
        nlinarith
      · have hS0 : 0 < |S| := by linarith
        have : |y| * |S| < (1 - k) * |S| := by nlinarith
        nlinarith
    have h3 : (1 - k) * (2 * k) ≤ 1 / 2 := by nlinarith [sq_nonneg (2 * k - 1)]
    linarith
  refine ⟨?_, ?_⟩
  · show |(m.1 - c.1) * C + (m.2 - c.2) * S| < 1 / 2
    exact hbnd _ _ hx hy
  · show |(-(m.1 - c.1)) * S + (m.2 - c.2) * C| < 1 / 2
    have := hbnd (m.2 - c.2) (-(m.1 - c.1)) hy (by rw [abs_neg]; exact hx)
    rwa [show (-(m.1 - c.1)) * S + (m.2 - c.2) * C = (m.2 - c.2) * C + (-(m.1 - c.1)) * S by ring]

/-- In a rectangle with both sides `< 2`, every unit square contains the centre in its interior. -/
lemma centre_mem_sqInt {c : ℝ × ℝ} {θ w h : ℝ} (hin : sq c θ 1 ⊆ rbox w h) (hw : w < 2) (hh : h < 2) :
    ((w / 2, h / 2) : ℝ × ℝ) ∈ sqInt c θ 1 := by
  obtain ⟨h1, h2, h3, h4⟩ := half_extent hin
  apply mem_sqInt_of_close
  · rw [abs_lt]; constructor <;> simp only <;> linarith
  · rw [abs_lt]; constructor <;> simp only <;> linarith

/-- **`R₂`.**  Two unit squares in `[0,w] × [0,h]` need a side of length at least `2`. -/
theorem rect2 {w h : ℝ} (hp : RectPacks 2 w h) : 2 ≤ w ∨ 2 ≤ h := by
  by_contra hc
  push Not at hc
  obtain ⟨ctr, ang, hin, hdisj⟩ := hp
  have h0 := centre_mem_sqInt (hin 0) hc.1 hc.2
  have h1 := centre_mem_sqInt (hin 1) hc.1 hc.2
  exact Set.disjoint_left.mp (hdisj 0 1 (by decide)) h0 h1

/-- A unit square in `[0,w] × [0,h]` forces `1 ≤ w` and `1 ≤ h`. -/
lemma one_le_sides {c : ℝ × ℝ} {θ w h : ℝ} (hin : sq c θ 1 ⊆ rbox w h) : 1 ≤ w ∧ 1 ≤ h := by
  obtain ⟨h1, h2, h3, h4⟩ := half_extent hin
  have := one_le_abs_cos_add_abs_sin θ
  constructor <;> linarith

/-- The axis-parallel unit square centred at `c`. -/
lemma sq_zero (c p : ℝ × ℝ) : p ∈ sq c 0 1 ↔ |p.1 - c.1| ≤ 1 / 2 ∧ |p.2 - c.2| ≤ 1 / 2 := by
  simp [sq, coord]

lemma sqInt_zero (c p : ℝ × ℝ) : p ∈ sqInt c 0 1 ↔ |p.1 - c.1| < 1 / 2 ∧ |p.2 - c.2| < 1 / 2 := by
  simp [sqInt, coord]

/-- An axis-parallel unit square with centre in `[1/2, w - 1/2] × [1/2, h - 1/2]` lies in the rectangle. -/
lemma sq_zero_subset {c : ℝ × ℝ} {w h : ℝ} (h1 : 1 / 2 ≤ c.1) (h2 : c.1 ≤ w - 1 / 2)
    (h3 : 1 / 2 ≤ c.2) (h4 : c.2 ≤ h - 1 / 2) : sq c 0 1 ⊆ rbox w h := by
  intro p hp
  rw [sq_zero, abs_le, abs_le] at hp
  simp only [rbox, Set.mem_ofPred_eq]
  refine ⟨?_, ?_, ?_, ?_⟩ <;> linarith [hp.1.1, hp.1.2, hp.2.1, hp.2.2]

/-- **`R₂` exactly.**  Two unit squares fit in `[0,w] × [0,h]` iff both sides are at least `1` and one
is at least `2`. -/
theorem rect2_iff {w h : ℝ} : RectPacks 2 w h ↔ 1 ≤ w ∧ 1 ≤ h ∧ (2 ≤ w ∨ 2 ≤ h) := by
  constructor
  · intro hp
    obtain ⟨hw, hh⟩ := one_le_sides (hp.choose_spec.choose_spec.1 0)
    exact ⟨hw, hh, rect2 hp⟩
  · rintro ⟨hw, hh, hw2 | hh2⟩
    · refine ⟨![(1 / 2, 1 / 2), (3 / 2, 1 / 2)], ![0, 0], ?_, ?_⟩
      · intro i; fin_cases i <;> exact sq_zero_subset (by norm_num) (by simp; linarith)
          (by norm_num) (by simp; linarith)
      · intro i j hij
        fin_cases i <;> fin_cases j <;> simp at hij <;>
        · rw [Set.disjoint_left]; intro p hp hq
          simp [sqInt, coord, abs_lt] at hp hq
          norm_num at hp hq; linarith
    · refine ⟨![(1 / 2, 1 / 2), (1 / 2, 3 / 2)], ![0, 0], ?_, ?_⟩
      · intro i; fin_cases i <;> exact sq_zero_subset (by norm_num) (by simp; linarith)
          (by norm_num) (by simp; linarith)
      · intro i j hij
        fin_cases i <;> fin_cases j <;> simp at hij <;>
        · rw [Set.disjoint_left]; intro p hp hq
          simp [sqInt, coord, abs_lt] at hp hq
          norm_num at hp hq; linarith

/-! ## The swap `x ↔ y` -/

lemma coord_swap (c p : ℝ × ℝ) (θ : ℝ) :
    coord (c.2, c.1) (Real.pi / 2 - θ) p =
      ((coord c θ (p.2, p.1)).1, -(coord c θ (p.2, p.1)).2) := by
  simp only [coord, Real.cos_pi_div_two_sub, Real.sin_pi_div_two_sub]; ext <;> simp only <;> ring

lemma mem_sq_swap (c p : ℝ × ℝ) (θ : ℝ) :
    p ∈ sq (c.2, c.1) (Real.pi / 2 - θ) 1 ↔ (p.2, p.1) ∈ sq c θ 1 := by
  simp only [sq, Set.mem_ofPred_eq, coord_swap, abs_neg]

lemma mem_sqInt_swap (c p : ℝ × ℝ) (θ : ℝ) :
    p ∈ sqInt (c.2, c.1) (Real.pi / 2 - θ) 1 ↔ (p.2, p.1) ∈ sqInt c θ 1 := by
  simp only [sqInt, Set.mem_ofPred_eq, coord_swap, abs_neg]

/-- Packings are symmetric in the two sides. -/
theorem RectPacks.swap {n : ℕ} {w h : ℝ} (hp : RectPacks n w h) : RectPacks n h w := by
  obtain ⟨ctr, ang, hin, hd⟩ := hp
  refine ⟨fun i => ((ctr i).2, (ctr i).1), fun i => Real.pi / 2 - ang i, fun i p hp => ?_,
    fun i j hij => ?_⟩
  · have := hin i ((mem_sq_swap _ _ _).1 hp)
    simp only [rbox, Set.mem_ofPred_eq] at this ⊢
    exact ⟨this.2.2.1, this.2.2.2, this.1, this.2.1⟩
  · rw [Set.disjoint_left]
    intro p h1 h2
    exact Set.disjoint_left.1 (hd i j hij) ((mem_sqInt_swap _ _ _).1 h1) ((mem_sqInt_swap _ _ _).1 h2)

/-! ## Constructions -/

/-- Converse of `half_extent`: a unit square whose centre keeps distance `(|cos θ| + |sin θ|)/2` from
every wall lies in the rectangle. -/
lemma sq_subset_rbox {c : ℝ × ℝ} {θ w h : ℝ}
    (h1 : (|Real.cos θ| + |Real.sin θ|) / 2 ≤ c.1) (h2 : c.1 ≤ w - (|Real.cos θ| + |Real.sin θ|) / 2)
    (h3 : (|Real.cos θ| + |Real.sin θ|) / 2 ≤ c.2) (h4 : c.2 ≤ h - (|Real.cos θ| + |Real.sin θ|) / 2) :
    sq c θ 1 ⊆ rbox w h := by
  intro p ⟨hu, hv⟩
  set C := Real.cos θ; set S := Real.sin θ
  have hCS : C ^ 2 + S ^ 2 = 1 := Real.cos_sq_add_sin_sq θ
  set u := (coord c θ p).1; set v := (coord c θ p).2
  have ex : p.1 - c.1 = u * C - v * S := by
    simp only [u, v, coord]; linear_combination -(p.1 - c.1) * hCS
  have ey : p.2 - c.2 = u * S + v * C := by
    simp only [u, v, coord]; linear_combination -(p.2 - c.2) * hCS
  have bx : |p.1 - c.1| ≤ (|C| + |S|) / 2 := by
    rw [ex]
    calc |u * C - v * S| ≤ |u| * |C| + |v| * |S| := by
          rw [← abs_mul, ← abs_mul]; exact abs_sub _ _
      _ ≤ 1 / 2 * |C| + 1 / 2 * |S| := by
          gcongr
      _ = (|C| + |S|) / 2 := by ring
  have by' : |p.2 - c.2| ≤ (|C| + |S|) / 2 := by
    rw [ey]
    calc |u * S + v * C| ≤ |u| * |S| + |v| * |C| := by
          rw [← abs_mul, ← abs_mul]; exact abs_add_le _ _
      _ ≤ 1 / 2 * |S| + 1 / 2 * |C| := by
          gcongr
      _ = (|C| + |S|) / 2 := by ring
  rw [abs_le] at bx by'
  simp only [rbox, Set.mem_ofPred_eq]
  refine ⟨?_, ?_, ?_, ?_⟩ <;> linarith [bx.1, bx.2, by'.1, by'.2]

/-- **The wedge.**  Two upright squares in the bottom corners of `[0,L] × [0,S]` and a `45°` square
between them touching the top wall: three unit squares fit whenever `2 ≤ L ≤ 3` and
`S ≥ 2 + √2 - L/2` (the tilted piece of `R₃`'s boundary, for `2√2 ≤ L ≤ 3`; the piece
`x + 2y = 4 + 2√2` of `S₂` in Friedman's Math Magic, June 2010). -/
theorem rect3_wedge {L S : ℝ} (hL : 2 ≤ L) (hL3 : L ≤ 3) (hS : 2 + Real.sqrt 2 - L / 2 ≤ S) :
    RectPacks 3 L S := by
  have r2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have r2p : 0 < Real.sqrt 2 := by positivity
  have r2l : Real.sqrt 2 < 3 / 2 := by nlinarith
  have r2g : 1 < Real.sqrt 2 := by nlinarith
  have a2 : |Real.sqrt 2 / 2| = Real.sqrt 2 / 2 := abs_of_pos (by positivity)
  have hc : Real.cos (Real.pi / 4) = Real.sqrt 2 / 2 := Real.cos_pi_div_four
  have hs : Real.sin (Real.pi / 4) = Real.sqrt 2 / 2 := Real.sin_pi_div_four
  have k45 : (|Real.cos (Real.pi / 4)| + |Real.sin (Real.pi / 4)|) / 2 = Real.sqrt 2 / 2 := by
    rw [hc, hs, abs_of_pos (by positivity)]; ring
  refine ⟨![(1 / 2, 1 / 2), (L - 1 / 2, 1 / 2), (L / 2, S - Real.sqrt 2 / 2)], ![0, 0, Real.pi / 4],
    ?_, ?_⟩
  · intro i
    fin_cases i
    · exact sq_zero_subset (by norm_num) (by simp; linarith) (by norm_num) (by simp; linarith)
    · exact sq_zero_subset (by simp; linarith) (by simp) (by norm_num) (by simp; linarith)
    · apply sq_subset_rbox <;> simp [hc, hs, a2] <;> nlinarith
  · -- interiors, as inequalities
    have i0 : ∀ p, p ∈ sqInt ((2⁻¹, 2⁻¹) : ℝ × ℝ) 0 1 → p.1 < 1 ∧ p.2 < 1 := by
      intro p hp; simp [sqInt, coord, abs_lt] at hp; constructor <;> linarith
    have i1 : ∀ p, p ∈ sqInt ((L - 2⁻¹, 2⁻¹) : ℝ × ℝ) 0 1 → L - 1 < p.1 ∧ p.2 < 1 := by
      intro p hp; simp [sqInt, coord, abs_lt] at hp; constructor <;> linarith
    have i2 : ∀ p, p ∈ sqInt ((L / 2, S - Real.sqrt 2 / 2) : ℝ × ℝ) (Real.pi / 4) 1 →
        L / 2 + S - Real.sqrt 2 < p.1 + p.2 ∧ S - Real.sqrt 2 - L / 2 < p.2 - p.1 := by
      intro p hp
      simp only [sqInt, coord, hc, hs, Set.mem_ofPred_eq, abs_lt] at hp
      obtain ⟨⟨a1, -⟩, ⟨b1, -⟩⟩ := hp
      constructor <;> nlinarith
    intro i j hij
    rw [Set.disjoint_left]
    intro p hp hq
    fin_cases i <;> fin_cases j <;> simp at hij hp hq
    · have := i0 p hp; have := i1 p hq; linarith
    · have := i0 p hp; have := i2 p hq; linarith
    · have := i1 p hp; have := i0 p hq; linarith
    · have := i1 p hp; have := i2 p hq; linarith
    · have := i2 p hp; have := i0 p hq; linarith
    · have := i2 p hp; have := i1 p hq; linarith

end SquarePacking
