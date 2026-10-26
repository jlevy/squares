import Sqpack.Basic
import Sqpack.Chord

/-!
# Soundness of the zero-margin checker's exact primitives

`search/zeromargin.py` decides, for a *pose box*
`B = [cx₀,cx₁] × [cy₀,cy₁] × [u₀,u₁]` (`u = tan(θ/2)`), whether the points of a weighted cover
that it can prove captured by *every admissible pose of the box* already weigh `≥ 1`.  Its exact
primitives are the lemmas of `search/RUNG2.md`:

* **Lemma A** (§3.1, monotone corners) — `mem_sq_of_corners`, `lemmaA`: the four containment
  inequalities `|X| ≤ ½`, `|Y| ≤ ½` are monotone in the centre when `cos θ, sin θ ≥ 0`, so each
  is implied by its value at one *specified* corner of the admissible centre rectangle.
* **Lemma C**, degree-`≤ 2` branch (§3.3) — `maxQuad`, `le_maxQuad`, `maxQuad_mem`: the exact
  maximum of a quadratic over `[u₀,u₁]` (`_max_quad` in the Python).
* **Lemma E** (§6.2, the four-corner maximum) — `gsum_le_gmax`, `gmax_mem`: a combination of
  violation polynomials is affine in `(c_x,c_y)` and quadratic in `u`, so its maximum over the
  box is the max over the four centre corners of the exact quadratic maximum (`_gmax`).
* **Lemma F** (§6.2, chain) — `chain_regions_cover`, `chain_region_down`.
* **Lemma G** (§6.2, the opposite side) — `lemmaG`, `lemmaG'`, `lemmaG_box`.
* **Lemma H** (§6.2, empty product regions) — `lemmaH`, `lemmaH_box`.
* **`clip_bin`** (§4.6) — `sq_subset_box_iff`, `widU_strictMonoOn`, `adm_widU_le`,
  `clip_bin_no_loss`: the admissible poses of a box at angle `θ` are its centre rectangle clipped
  to `[w(θ)/2, m − w(θ)/2]²`, so a pose of the box is admissible only if `w(θ) ≤ K` with
  `K = 2 min(cx₁, m−cx₀, cy₁, m−cy₀)`, and `w` is strictly increasing in `u` on `[0°,45°]`.

Notation follows `RUNG2.md` §1: container `[0,m]²` (`box m` of `Chord.lean`), pose `(c,θ)`,
`X = d_x cos θ + d_y sin θ`, `Y = -d_x sin θ + d_y cos θ` with `d = p - c`, which is exactly
`coord c θ p` of `Basic.lean`; `p ∈ sq c θ 1 ↔ |X| ≤ ½ ∧ |Y| ≤ ½` by definition.

See `notes/lean-zeromargin.md` for the statement ↔ implementation correspondence.
-/

open Finset

namespace SquarePacking

/-! ## 0.  Width and admissibility (`RUNG2.md` §1) -/

/-- `w(θ) = |cos θ| + |sin θ|`, the side of the axis-parallel bounding box of a unit square at
angle `θ`. -/
noncomputable def wid (θ : ℝ) : ℝ := |Real.cos θ| + |Real.sin θ|

/-- A pose `(c,θ)` is **admissible** for the container `[0,m]²` when
`c_x, c_y ∈ [w(θ)/2, m − w(θ)/2]` (`RUNG2.md` §1).  `sq_subset_box_iff` below shows this is
exactly `sq c θ 1 ⊆ box m`. -/
def Adm (m : ℝ) (c : ℝ × ℝ) (θ : ℝ) : Prop :=
  wid θ / 2 ≤ c.1 ∧ c.1 ≤ m - wid θ / 2 ∧ wid θ / 2 ≤ c.2 ∧ c.2 ≤ m - wid θ / 2

/-- The point at rotated offset `(x,y)` from the centre lies in the closed unit square. -/
lemma mem_sq_offset (c : ℝ × ℝ) (θ x y : ℝ) (hx : |x| ≤ 1 / 2) (hy : |y| ≤ 1 / 2) :
    (c.1 + (x * Real.cos θ - y * Real.sin θ),
     c.2 + (x * Real.sin θ + y * Real.cos θ)) ∈ sq c θ 1 := by
  have hCS : Real.cos θ ^ 2 + Real.sin θ ^ 2 = 1 := Real.cos_sq_add_sin_sq θ
  have h1 : (coord c θ (c.1 + (x * Real.cos θ - y * Real.sin θ),
      c.2 + (x * Real.sin θ + y * Real.cos θ))).1 = x * (Real.cos θ ^ 2 + Real.sin θ ^ 2) := by
    simp only [coord]; ring
  have h2 : (coord c θ (c.1 + (x * Real.cos θ - y * Real.sin θ),
      c.2 + (x * Real.sin θ + y * Real.cos θ))).2 = y * (Real.cos θ ^ 2 + Real.sin θ ^ 2) := by
    simp only [coord]; ring
  exact ⟨by rw [h1, hCS, mul_one]; exact hx, by rw [h2, hCS, mul_one]; exact hy⟩

/-- The offset of `p` from `c` is recovered from `coord c θ p` by the inverse rotation. -/
lemma sub_eq_of_coord (c : ℝ × ℝ) (θ : ℝ) (p : ℝ × ℝ) :
    p.1 - c.1 = (coord c θ p).1 * Real.cos θ - (coord c θ p).2 * Real.sin θ ∧
      p.2 - c.2 = (coord c θ p).1 * Real.sin θ + (coord c θ p).2 * Real.cos θ := by
  have hCS : Real.cos θ ^ 2 + Real.sin θ ^ 2 = 1 := Real.cos_sq_add_sin_sq θ
  refine ⟨?_, ?_⟩
  · simp only [coord]; linear_combination (c.1 - p.1) * hCS
  · simp only [coord]; linear_combination (c.2 - p.2) * hCS

/-- A unit square at angle `θ` reaches at most `w(θ)/2` from its centre in each axis direction. -/
lemma abs_sub_le_wid {c p : ℝ × ℝ} {θ : ℝ} (hp : p ∈ sq c θ 1) :
    |p.1 - c.1| ≤ wid θ / 2 ∧ |p.2 - c.2| ≤ wid θ / 2 := by
  obtain ⟨hX, hY⟩ := hp
  obtain ⟨e1, e2⟩ := sub_eq_of_coord c θ p
  have hC := abs_nonneg (Real.cos θ)
  have hS := abs_nonneg (Real.sin θ)
  have h1 : |(coord c θ p).1| * |Real.cos θ| ≤ 1 / 2 * |Real.cos θ| :=
    mul_le_mul_of_nonneg_right hX hC
  have h2 : |(coord c θ p).2| * |Real.sin θ| ≤ 1 / 2 * |Real.sin θ| :=
    mul_le_mul_of_nonneg_right hY hS
  have h3 : |(coord c θ p).1| * |Real.sin θ| ≤ 1 / 2 * |Real.sin θ| :=
    mul_le_mul_of_nonneg_right hX hS
  have h4 : |(coord c θ p).2| * |Real.cos θ| ≤ 1 / 2 * |Real.cos θ| :=
    mul_le_mul_of_nonneg_right hY hC
  refine ⟨?_, ?_⟩
  · rw [e1]
    calc |(coord c θ p).1 * Real.cos θ - (coord c θ p).2 * Real.sin θ|
        = |(coord c θ p).1 * Real.cos θ + -((coord c θ p).2 * Real.sin θ)| := by
          rw [sub_eq_add_neg]
      _ ≤ |(coord c θ p).1 * Real.cos θ| + |-((coord c θ p).2 * Real.sin θ)| := abs_add_le _ _
      _ = |(coord c θ p).1| * |Real.cos θ| + |(coord c θ p).2| * |Real.sin θ| := by
          rw [abs_neg, abs_mul, abs_mul]
      _ ≤ wid θ / 2 := by simp only [wid]; linarith
  · rw [e2]
    calc |(coord c θ p).1 * Real.sin θ + (coord c θ p).2 * Real.cos θ|
        ≤ |(coord c θ p).1 * Real.sin θ| + |(coord c θ p).2 * Real.cos θ| := abs_add_le _ _
      _ = |(coord c θ p).1| * |Real.sin θ| + |(coord c θ p).2| * |Real.cos θ| := by
          rw [abs_mul, abs_mul]
      _ ≤ wid θ / 2 := by simp only [wid]; linarith

/-- **The support-function fact, i.e. `clip_bin`'s premise** (`RUNG2.md` §1, §4.6).  A closed unit
square at angle `θ` lies in the container `[0,m]²` exactly when its centre lies in the square
`[w(θ)/2, m − w(θ)/2]²`.  This is the definition of *admissible* that `zeromargin.py` uses
throughout (`clip_bin`'s docstring; `_adm_specs`'s `'W'`/`'M'` bounds). -/
theorem sq_subset_box_iff (m : ℝ) (c : ℝ × ℝ) (θ : ℝ) :
    sq c θ 1 ⊆ box m ↔ Adm m c θ := by
  constructor
  · intro hsub
    -- the four extreme vertices, written with the signs of `cos θ` and `sin θ`
    set sc : ℝ := if 0 ≤ Real.cos θ then 1 else -1 with hsc
    set ss : ℝ := if 0 ≤ Real.sin θ then 1 else -1 with hss
    have hscC : sc * Real.cos θ = |Real.cos θ| := by
      rw [hsc]; split_ifs with h
      · rw [abs_of_nonneg h]; ring
      · rw [abs_of_neg (not_le.mp h)]; ring
    have hssS : ss * Real.sin θ = |Real.sin θ| := by
      rw [hss]; split_ifs with h
      · rw [abs_of_nonneg h]; ring
      · rw [abs_of_neg (not_le.mp h)]; ring
    have habs : ∀ t : ℝ, (t = 1 ∨ t = -1) → |(-t) / 2| ≤ 1 / 2 ∧ |t / 2| ≤ 1 / 2 := by
      rintro t (rfl | rfl) <;> norm_num
    have hsc' : sc = 1 ∨ sc = -1 := by rw [hsc]; split_ifs <;> simp
    have hss' : ss = 1 ∨ ss = -1 := by rw [hss]; split_ifs <;> simp
    have hA := habs sc hsc'
    have hB := habs ss hss'
    refine ⟨?_, ?_, ?_, ?_⟩
    · -- `c_x ≥ w/2`: the vertex at offset `(-sc/2, ss/2)` has `p_x - c_x = -w/2`
      have h := (hsub (mem_sq_offset c θ (-sc / 2) (ss / 2) hA.1 hB.2)).1
      simp only [wid] at *
      nlinarith [hscC, hssS, h]
    · have h := (hsub (mem_sq_offset c θ (sc / 2) (-ss / 2) hA.2 hB.1)).2.1
      simp only [wid] at *
      nlinarith [hscC, hssS, h]
    · have h := (hsub (mem_sq_offset c θ (-ss / 2) (-sc / 2) hB.1 hA.1)).2.2.1
      simp only [wid] at *
      nlinarith [hscC, hssS, h]
    · have h := (hsub (mem_sq_offset c θ (ss / 2) (sc / 2) hB.2 hA.2)).2.2.2
      simp only [wid] at *
      nlinarith [hscC, hssS, h]
  · rintro ⟨h1, h2, h3, h4⟩ p hp
    obtain ⟨hx, hy⟩ := abs_sub_le_wid hp
    rw [abs_le] at hx hy
    exact ⟨by linarith [hx.1], by linarith [hx.2], by linarith [hy.1], by linarith [hy.2]⟩

/-! ## 1.  Lemma A — monotone corners (`RUNG2.md` §3.1, `_adm_cond_ok`)

Each of the four inequalities is checked at *one* corner of the admissible centre rectangle, and
each is checked with its own pair of bounds: the Python offers the box side (`'R'`) and, when the
wall can bind on the bin, the wall bound (`'W'`/`'M'`), and accepts the inequality if *any*
offered combination certifies it (`_adm_specs`, `_adm_cond_ok`).  The four lemmas below are
therefore stated with independent corner values; that is exactly what makes the per-condition
choice sound, since any lower bound for the admissible `c_x` may be used in place of
`A_x = max(cx₀, w/2)` — lowering `A_x` only strengthens the inequality. -/

/-- Inequality (i) of Lemma A: `X ≤ ½` tested at the corner `(A_x, A_y)`. -/
lemma coord_fst_le_of_corner {p c : ℝ × ℝ} {θ Ax Ay : ℝ}
    (hcos : 0 ≤ Real.cos θ) (hsin : 0 ≤ Real.sin θ)
    (h : (p.1 - Ax) * Real.cos θ + (p.2 - Ay) * Real.sin θ ≤ 1 / 2)
    (hx : Ax ≤ c.1) (hy : Ay ≤ c.2) : (coord c θ p).1 ≤ 1 / 2 := by
  simp only [coord]
  nlinarith [mul_nonneg (sub_nonneg.mpr hx) hcos, mul_nonneg (sub_nonneg.mpr hy) hsin]

/-- Inequality (ii) of Lemma A: `X ≥ -½` tested at the corner `(B_x, B_y)`. -/
lemma neg_half_le_coord_fst {p c : ℝ × ℝ} {θ Bx By : ℝ}
    (hcos : 0 ≤ Real.cos θ) (hsin : 0 ≤ Real.sin θ)
    (h : -(1 / 2) ≤ (p.1 - Bx) * Real.cos θ + (p.2 - By) * Real.sin θ)
    (hx : c.1 ≤ Bx) (hy : c.2 ≤ By) : -(1 / 2) ≤ (coord c θ p).1 := by
  simp only [coord]
  nlinarith [mul_nonneg (sub_nonneg.mpr hx) hcos, mul_nonneg (sub_nonneg.mpr hy) hsin]

/-- Inequality (iii) of Lemma A: `Y ≤ ½` tested at the corner `(B_x, A_y)`. -/
lemma coord_snd_le_of_corner {p c : ℝ × ℝ} {θ Bx Ay : ℝ}
    (hcos : 0 ≤ Real.cos θ) (hsin : 0 ≤ Real.sin θ)
    (h : -(p.1 - Bx) * Real.sin θ + (p.2 - Ay) * Real.cos θ ≤ 1 / 2)
    (hx : c.1 ≤ Bx) (hy : Ay ≤ c.2) : (coord c θ p).2 ≤ 1 / 2 := by
  simp only [coord]
  nlinarith [mul_nonneg (sub_nonneg.mpr hx) hsin, mul_nonneg (sub_nonneg.mpr hy) hcos]

/-- Inequality (iv) of Lemma A: `Y ≥ -½` tested at the corner `(A_x, B_y)`. -/
lemma neg_half_le_coord_snd {p c : ℝ × ℝ} {θ Ax By : ℝ}
    (hcos : 0 ≤ Real.cos θ) (hsin : 0 ≤ Real.sin θ)
    (h : -(1 / 2) ≤ -(p.1 - Ax) * Real.sin θ + (p.2 - By) * Real.cos θ)
    (hx : Ax ≤ c.1) (hy : c.2 ≤ By) : -(1 / 2) ≤ (coord c θ p).2 := by
  simp only [coord]
  nlinarith [mul_nonneg (sub_nonneg.mpr hx) hsin, mul_nonneg (sub_nonneg.mpr hy) hcos]

/-- **Lemma A, corner form** (`RUNG2.md` §3.1).  The four inequalities are tested at four
*different* corners, each with its own pair of bounds; every bound needs only to be a sound bound
for the admissible range of the centre at this `θ`.  This is `_adm_cond_ok` / `_adm_exact` of
`search/zeromargin.py` with the `'R'`/`'W'`/`'M'` choices already made. -/
theorem mem_sq_of_corners {p c : ℝ × ℝ} {θ : ℝ}
    {Ax₁ Ay₁ Bx₂ By₂ Bx₃ Ay₃ Ax₄ By₄ : ℝ}
    (hcos : 0 ≤ Real.cos θ) (hsin : 0 ≤ Real.sin θ)
    (h₁ : (p.1 - Ax₁) * Real.cos θ + (p.2 - Ay₁) * Real.sin θ ≤ 1 / 2)
    (h₂ : -(1 / 2) ≤ (p.1 - Bx₂) * Real.cos θ + (p.2 - By₂) * Real.sin θ)
    (h₃ : -(p.1 - Bx₃) * Real.sin θ + (p.2 - Ay₃) * Real.cos θ ≤ 1 / 2)
    (h₄ : -(1 / 2) ≤ -(p.1 - Ax₄) * Real.sin θ + (p.2 - By₄) * Real.cos θ)
    (hx₁ : Ax₁ ≤ c.1) (hy₁ : Ay₁ ≤ c.2) (hx₂ : c.1 ≤ Bx₂) (hy₂ : c.2 ≤ By₂)
    (hx₃ : c.1 ≤ Bx₃) (hy₃ : Ay₃ ≤ c.2) (hx₄ : Ax₄ ≤ c.1) (hy₄ : c.2 ≤ By₄) :
    p ∈ sq c θ 1 := by
  refine ⟨abs_le.mpr ⟨?_, ?_⟩, abs_le.mpr ⟨?_, ?_⟩⟩
  · have := neg_half_le_coord_fst hcos hsin h₂ hx₂ hy₂; linarith
  · have := coord_fst_le_of_corner hcos hsin h₁ hx₁ hy₁; linarith
  · have := neg_half_le_coord_snd hcos hsin h₄ hx₄ hy₄; linarith
  · have := coord_snd_le_of_corner hcos hsin h₃ hx₃ hy₃; linarith

/-- `A_x(θ) = max(cx₀, w(θ)/2)`, the exact lower bound for the admissible `c_x` of a pose box. -/
noncomputable def admLo (c₀ : ℝ) (θ : ℝ) : ℝ := max c₀ (wid θ / 2)

/-- `B_x(θ) = min(cx₁, m − w(θ)/2)`, the exact upper bound for the admissible `c_x`. -/
noncomputable def admHi (m c₁ : ℝ) (θ : ℝ) : ℝ := min c₁ (m - wid θ / 2)

/-- **Lemma A** (`RUNG2.md` §3.1).  Let `[cx₀,cx₁] × [cy₀,cy₁]` be the centre rectangle of a pose
box and `Bin` its set of angles, on which `cos θ, sin θ ≥ 0` (which is the hypothesis
`u₀ ≥ 0, u₁ ≤ 1`, i.e. `θ ∈ [0°,90°]`).  If the four inequalities (i)–(iv) hold at the four
*specified* corners `(A_x,A_y)`, `(B_x,B_y)`, `(B_x,A_y)`, `(A_x,B_y)` for **every** `θ` in the
bin, then `p ∈ sq c θ 1` for **every admissible pose** `(c,θ)` of the box.

At an angle where `A_x > B_x` the conclusion is vacuous but the hypotheses are still sound; that
is precisely the conservatism `clip_bin` (§4.6) removes. -/
theorem lemmaA (m : ℝ) (p : ℝ × ℝ) (cx₀ cx₁ cy₀ cy₁ : ℝ) (Bin : Set ℝ)
    (hBin : ∀ θ ∈ Bin, 0 ≤ Real.cos θ ∧ 0 ≤ Real.sin θ)
    (h₁ : ∀ θ ∈ Bin, (p.1 - admLo cx₀ θ) * Real.cos θ
            + (p.2 - admLo cy₀ θ) * Real.sin θ ≤ 1 / 2)
    (h₂ : ∀ θ ∈ Bin, -(1 / 2) ≤ (p.1 - admHi m cx₁ θ) * Real.cos θ
            + (p.2 - admHi m cy₁ θ) * Real.sin θ)
    (h₃ : ∀ θ ∈ Bin, -(p.1 - admHi m cx₁ θ) * Real.sin θ
            + (p.2 - admLo cy₀ θ) * Real.cos θ ≤ 1 / 2)
    (h₄ : ∀ θ ∈ Bin, -(1 / 2) ≤ -(p.1 - admLo cx₀ θ) * Real.sin θ
            + (p.2 - admHi m cy₁ θ) * Real.cos θ) :
    ∀ (c : ℝ × ℝ) (θ : ℝ), θ ∈ Bin → c.1 ∈ Set.Icc cx₀ cx₁ → c.2 ∈ Set.Icc cy₀ cy₁ →
      sq c θ 1 ⊆ box m → p ∈ sq c θ 1 := by
  intro c θ hθ hcx hcy hsub
  obtain ⟨ha1, ha2, ha3, ha4⟩ := (sq_subset_box_iff m c θ).mp hsub
  obtain ⟨hcos, hsin⟩ := hBin θ hθ
  have hlox : admLo cx₀ θ ≤ c.1 := max_le hcx.1 ha1
  have hloy : admLo cy₀ θ ≤ c.2 := max_le hcy.1 ha3
  have hhix : c.1 ≤ admHi m cx₁ θ := le_min hcx.2 ha2
  have hhiy : c.2 ≤ admHi m cy₁ θ := le_min hcy.2 ha4
  exact mem_sq_of_corners hcos hsin (h₁ θ hθ) (h₂ θ hθ) (h₃ θ hθ) (h₄ θ hθ)
    hlox hloy hhix hhiy hhix hloy hlox hhiy

/-! ## 2.  Lemma C, degree `≤ 2` — the exact quadratic maximum (`_max_quad`) -/

/-- The exact maximum of `a₀ + a₁u + a₂u²` over `[u₀,u₁]`: the larger endpoint value, and the
vertex value `a₀ − a₁²/(4a₂)` when the leading coefficient is negative and the vertex
`-a₁/(2a₂)` lies strictly inside.  This is `_max_quad` of `search/zeromargin.py` (which returns
`a₀ + a₁u_v + a₂u_v²` at `u_v = -a₁/(2a₂)`, which equals `a₀ − a₁²/(4a₂)`). -/
noncomputable def maxQuad (a₀ a₁ a₂ u₀ u₁ : ℝ) : ℝ :=
  if a₂ < 0 ∧ u₀ < -a₁ / (2 * a₂) ∧ -a₁ / (2 * a₂) < u₁ then
    max (max (a₀ + a₁ * u₀ + a₂ * u₀ ^ 2) (a₀ + a₁ * u₁ + a₂ * u₁ ^ 2))
      (a₀ - a₁ ^ 2 / (4 * a₂))
  else max (a₀ + a₁ * u₀ + a₂ * u₀ ^ 2) (a₀ + a₁ * u₁ + a₂ * u₁ ^ 2)

/-- The vertex value of a quadratic with negative leading coefficient is its global maximum. -/
lemma quad_le_vertex {a₀ a₁ a₂ : ℝ} (ha : a₂ < 0) (u : ℝ) :
    a₀ + a₁ * u + a₂ * u ^ 2 ≤ a₀ - a₁ ^ 2 / (4 * a₂) := by
  have ha0 : a₂ ≠ 0 := ne_of_lt ha
  have key : 4 * a₂ * (a₁ * u + a₂ * u ^ 2 + a₁ ^ 2 / (4 * a₂)) = (2 * a₂ * u + a₁) ^ 2 := by
    field_simp; ring
  nlinarith [key, sq_nonneg (2 * a₂ * u + a₁), ha]

/-- **Soundness of `_max_quad`**: `maxQuad` is an upper bound on `[u₀,u₁]`. -/
theorem le_maxQuad {a₀ a₁ a₂ u₀ u₁ u : ℝ} (hu : u ∈ Set.Icc u₀ u₁) :
    a₀ + a₁ * u + a₂ * u ^ 2 ≤ maxQuad a₀ a₁ a₂ u₀ u₁ := by
  obtain ⟨hu0, hu1⟩ := hu
  rw [maxQuad]
  split_ifs with h
  · exact le_max_of_le_right (quad_le_vertex h.1 u)
  · rcases lt_or_ge a₂ 0 with ha | ha
    · -- `a₂ < 0` and the vertex is outside: the quadratic is monotone on `[u₀,u₁]`
      have h2a : 2 * a₂ < 0 := by linarith
      rcases not_and_or.mp (fun hv => h ⟨ha, hv⟩) with hno | hno
      · have h' : -a₁ / (2 * a₂) ≤ u₀ := not_lt.mp hno
        rw [div_le_iff_of_neg h2a] at h'
        refine le_max_of_le_left ?_
        nlinarith [mul_nonneg (sub_nonneg.mpr hu0) (neg_nonneg.mpr (le_of_lt ha))]
      · have h' : u₁ ≤ -a₁ / (2 * a₂) := not_lt.mp hno
        rw [le_div_iff_of_neg h2a] at h'
        refine le_max_of_le_right ?_
        nlinarith [mul_nonneg (sub_nonneg.mpr hu1) (neg_nonneg.mpr (le_of_lt ha))]
    · -- `a₂ ≥ 0`: the quadratic is convex, so its max is at an endpoint
      rcases eq_or_lt_of_le hu0 with rfl | hlt
      · exact le_max_left _ _
      have hu01 : u₀ < u₁ := lt_of_lt_of_le hlt hu1
      have hkey : (u₁ - u) * ((a₀ + a₁ * u₀ + a₂ * u₀ ^ 2) - (a₀ + a₁ * u + a₂ * u ^ 2))
          + (u - u₀) * ((a₀ + a₁ * u₁ + a₂ * u₁ ^ 2) - (a₀ + a₁ * u + a₂ * u ^ 2))
          = a₂ * ((u₁ - u) * (u - u₀) * (u₁ - u₀)) := by ring
      have h0 : a₀ + a₁ * u₀ + a₂ * u₀ ^ 2
          ≤ max (a₀ + a₁ * u₀ + a₂ * u₀ ^ 2) (a₀ + a₁ * u₁ + a₂ * u₁ ^ 2) := le_max_left _ _
      have h1 : a₀ + a₁ * u₁ + a₂ * u₁ ^ 2
          ≤ max (a₀ + a₁ * u₀ + a₂ * u₀ ^ 2) (a₀ + a₁ * u₁ + a₂ * u₁ ^ 2) := le_max_right _ _
      have hpos : 0 ≤ a₂ * ((u₁ - u) * (u - u₀) * (u₁ - u₀)) :=
        mul_nonneg ha (mul_nonneg (mul_nonneg (by linarith) (by linarith)) (by linarith))
      nlinarith [hkey, hpos, h0, h1]

/-- **Exactness of `_max_quad`**: `maxQuad` is attained on `[u₀,u₁]`, so the checker's bound has
no slack (`RUNG2.md` §3.3, the `deg ≤ 2` branch; §6.2, "no Bernstein slack"). -/
theorem maxQuad_mem {a₀ a₁ a₂ u₀ u₁ : ℝ} (h : u₀ ≤ u₁) :
    ∃ u ∈ Set.Icc u₀ u₁, a₀ + a₁ * u + a₂ * u ^ 2 = maxQuad a₀ a₁ a₂ u₀ u₁ := by
  rw [maxQuad]
  split_ifs with hv
  · obtain ⟨ha, hlo, hhi⟩ := hv
    have hne2 : (2 : ℝ) * a₂ ≠ 0 := by intro hc; nlinarith
    have hvert : a₀ + a₁ * (-a₁ / (2 * a₂)) + a₂ * (-a₁ / (2 * a₂)) ^ 2
        = a₀ - a₁ ^ 2 / (4 * a₂) := by field_simp; ring
    refine ⟨-a₁ / (2 * a₂), ⟨le_of_lt hlo, le_of_lt hhi⟩, ?_⟩
    rw [hvert, max_eq_right (max_le (quad_le_vertex ha u₀) (quad_le_vertex ha u₁))]
  · rcases le_total (a₀ + a₁ * u₀ + a₂ * u₀ ^ 2) (a₀ + a₁ * u₁ + a₂ * u₁ ^ 2) with hle | hle
    · exact ⟨u₁, ⟨h, le_rfl⟩, (max_eq_right hle).symm⟩
    · exact ⟨u₀, ⟨le_rfl, h⟩, (max_eq_left hle).symm⟩

/-! ## 3.  The violation polynomials and Lemma E (`RUNG2.md` §6.2, `_gcoef` / `_gmax`) -/

/-- The quadratic coefficients (in `u = tan(θ/2)`) of the four **violation polynomials** at
offsets `a = p_x − c_x`, `b = p_y − c_y`.  This is `_gcoef` of `search/zeromargin.py`:
`G_{p,0} = 2aC + 2bS − N`, `G_{p,1} = −2aC − 2bS − N`, `G_{p,2} = −2aS + 2bC − N`,
`G_{p,3} = 2aS − 2bC − N`, with `C = 1−u²`, `S = 2u`, `N = 1+u²`. -/
def gc : Fin 4 → ℝ → ℝ → ℝ × ℝ × ℝ
  | 0, a, b => (2 * a - 1, 4 * b, -2 * a - 1)
  | 1, a, b => (-2 * a - 1, -4 * b, 2 * a - 1)
  | 2, a, b => (2 * b - 1, -4 * a, -2 * b - 1)
  | 3, a, b => (-2 * b - 1, 4 * a, 2 * b - 1)

/-- The violation polynomial `G_{p,k}` evaluated at `u`. -/
def gval (k : Fin 4) (a b u : ℝ) : ℝ :=
  (gc k a b).1 + (gc k a b).2.1 * u + (gc k a b).2.2 * u ^ 2

lemma cos_two_arctan (u : ℝ) :
    Real.cos (2 * Real.arctan u) = (1 - u ^ 2) / (1 + u ^ 2) := by
  have hpos : (0 : ℝ) < 1 + u ^ 2 := by positivity
  rw [Real.cos_two_mul, Real.cos_sq_arctan]
  field_simp
  ring

lemma sin_two_arctan (u : ℝ) :
    Real.sin (2 * Real.arctan u) = 2 * u / (1 + u ^ 2) := by
  have hpos : (0 : ℝ) < 1 + u ^ 2 := by positivity
  have hsq : Real.sqrt (1 + u ^ 2) ^ 2 = 1 + u ^ 2 := Real.sq_sqrt (le_of_lt hpos)
  have hne : Real.sqrt (1 + u ^ 2) ≠ 0 := by
    intro hc; rw [hc] at hsq; norm_num at hsq; linarith
  rw [Real.sin_two_mul, Real.sin_arctan, Real.cos_arctan]
  field_simp
  rw [hsq]

/-- **The violation polynomials decide containment** (`RUNG2.md` §6.2; checked in floats against
the geometry by `search/zeromargin_stress.py`, "0 disagreements").  With `θ = 2 arctan u`,
`p ∈ sq c θ 1` iff all four `G_{p,k} ≤ 0`. -/
theorem mem_sq_iff_gval (c p : ℝ × ℝ) (u : ℝ) :
    p ∈ sq c (2 * Real.arctan u) 1 ↔ ∀ k : Fin 4, gval k (p.1 - c.1) (p.2 - c.2) u ≤ 0 := by
  have hN : (0 : ℝ) < 1 + u ^ 2 := by positivity
  have hNne : (1 : ℝ) + u ^ 2 ≠ 0 := ne_of_gt hN
  have hX : 2 * (1 + u ^ 2) * (coord c (2 * Real.arctan u) p).1
      = 2 * (p.1 - c.1) * (1 - u ^ 2) + 4 * (p.2 - c.2) * u := by
    simp only [coord, cos_two_arctan, sin_two_arctan]
    field_simp
    ring
  have hY : 2 * (1 + u ^ 2) * (coord c (2 * Real.arctan u) p).2
      = -(4 * (p.1 - c.1) * u) + 2 * (p.2 - c.2) * (1 - u ^ 2) := by
    simp only [coord, cos_two_arctan, sin_two_arctan]
    field_simp
    ring
  constructor
  · rintro ⟨h1, h2⟩ k
    rw [abs_le] at h1 h2
    obtain ⟨h1a, h1b⟩ := h1
    obtain ⟨h2a, h2b⟩ := h2
    fin_cases k <;> simp only [gval, gc] <;> nlinarith [hX, hY, hN, h1a, h1b, h2a, h2b]
  · intro h
    have h0 := h 0
    have h1 := h 1
    have h2 := h 2
    have h3 := h 3
    simp only [gval, gc] at h0 h1 h2 h3
    refine ⟨abs_le.mpr ⟨?_, ?_⟩, abs_le.mpr ⟨?_, ?_⟩⟩
    · nlinarith [hX, hN]
    · nlinarith [hX, hN]
    · nlinarith [hY, hN]
    · nlinarith [hY, hN]

/-! ### Lemma E: affine in the centre, quadratic in `u` -/

/-- The coefficient of `a = p_x − c_x` in `G_{p,k}`. -/
def galpha : Fin 4 → ℝ → ℝ
  | 0, u => 2 * (1 - u ^ 2)
  | 1, u => -(2 * (1 - u ^ 2))
  | 2, u => -(4 * u)
  | 3, u => 4 * u

/-- The coefficient of `b = p_y − c_y` in `G_{p,k}`. -/
def gbeta : Fin 4 → ℝ → ℝ
  | 0, u => 4 * u
  | 1, u => -(4 * u)
  | 2, u => 2 * (1 - u ^ 2)
  | 3, u => -(2 * (1 - u ^ 2))

/-- Every violation polynomial is `-N + α(u)·a + β(u)·b`: **affine in the offsets**, hence affine
in the centre.  This is the first half of Lemma E. -/
lemma gval_eq (k : Fin 4) (a b u : ℝ) :
    gval k a b u = -(1 + u ^ 2) + galpha k u * a + gbeta k u * b := by
  fin_cases k <;> simp only [gval, gc, galpha, gbeta] <;> ring

variable {n : ℕ}

/-- A combination `Σ λ_r G_{p_r, k_r}` evaluated at the pose `(cx, cy, u)`. -/
noncomputable def gsum (lam : Fin n → ℝ) (pt : Fin n → ℝ × ℝ) (kind : Fin n → Fin 4)
    (cx cy u : ℝ) : ℝ :=
  ∑ r : Fin n, lam r * gval (kind r) ((pt r).1 - cx) ((pt r).2 - cy) u

/-- An affine function of one variable attains its maximum over an interval at an endpoint. -/
lemma affine_le_max {A Bc x x₀ x₁ : ℝ} (hx : x ∈ Set.Icc x₀ x₁) :
    A * x + Bc ≤ max (A * x₀ + Bc) (A * x₁ + Bc) := by
  rcases le_or_gt 0 A with hA | hA
  · exact le_max_of_le_right (by nlinarith [hx.2])
  · exact le_max_of_le_left (by nlinarith [hx.1])

/-- `gsum` is affine in `c_x`. -/
lemma gsum_affine_x (lam : Fin n → ℝ) (pt : Fin n → ℝ × ℝ) (kind : Fin n → Fin 4)
    (cx cy u : ℝ) :
    gsum lam pt kind cx cy u
      = (-∑ r : Fin n, lam r * galpha (kind r) u) * cx
        + ∑ r : Fin n, lam r * (-(1 + u ^ 2) + galpha (kind r) u * (pt r).1
            + gbeta (kind r) u * ((pt r).2 - cy)) := by
  simp only [gsum]
  rw [neg_mul, Finset.sum_mul, ← sub_eq_neg_add, ← Finset.sum_sub_distrib]
  refine Finset.sum_congr rfl fun r _ => ?_
  rw [gval_eq]; ring

/-- `gsum` is affine in `c_y`. -/
lemma gsum_affine_y (lam : Fin n → ℝ) (pt : Fin n → ℝ × ℝ) (kind : Fin n → Fin 4)
    (cx cy u : ℝ) :
    gsum lam pt kind cx cy u
      = (-∑ r : Fin n, lam r * gbeta (kind r) u) * cy
        + ∑ r : Fin n, lam r * (-(1 + u ^ 2) + galpha (kind r) u * ((pt r).1 - cx)
            + gbeta (kind r) u * (pt r).2) := by
  simp only [gsum]
  rw [neg_mul, Finset.sum_mul, ← sub_eq_neg_add, ← Finset.sum_sub_distrib]
  refine Finset.sum_congr rfl fun r _ => ?_
  rw [gval_eq]; ring

/-- **Lemma E, the centre half**: for each fixed `u`, the maximum of `Σ λ_r G_{p_r,k_r}` over the
centre rectangle is attained at one of its four corners (`_gmax`'s corner loop). -/
theorem gsum_le_corners (lam : Fin n → ℝ) (pt : Fin n → ℝ × ℝ) (kind : Fin n → Fin 4)
    {cx₀ cx₁ cy₀ cy₁ cx cy : ℝ} (u : ℝ)
    (hcx : cx ∈ Set.Icc cx₀ cx₁) (hcy : cy ∈ Set.Icc cy₀ cy₁) :
    gsum lam pt kind cx cy u
      ≤ max (max (gsum lam pt kind cx₀ cy₀ u) (gsum lam pt kind cx₀ cy₁ u))
          (max (gsum lam pt kind cx₁ cy₀ u) (gsum lam pt kind cx₁ cy₁ u)) := by
  have stepx : ∀ y : ℝ, gsum lam pt kind cx y u
      ≤ max (gsum lam pt kind cx₀ y u) (gsum lam pt kind cx₁ y u) := by
    intro y
    rw [gsum_affine_x lam pt kind cx y u, gsum_affine_x lam pt kind cx₀ y u,
      gsum_affine_x lam pt kind cx₁ y u]
    exact affine_le_max hcx
  have stepy : ∀ x : ℝ, gsum lam pt kind x cy u
      ≤ max (gsum lam pt kind x cy₀ u) (gsum lam pt kind x cy₁ u) := by
    intro x
    rw [gsum_affine_y lam pt kind x cy u, gsum_affine_y lam pt kind x cy₀ u,
      gsum_affine_y lam pt kind x cy₁ u]
    exact affine_le_max hcy
  calc gsum lam pt kind cx cy u
      ≤ max (gsum lam pt kind cx₀ cy u) (gsum lam pt kind cx₁ cy u) := stepx cy
    _ ≤ max (max (gsum lam pt kind cx₀ cy₀ u) (gsum lam pt kind cx₀ cy₁ u))
          (max (gsum lam pt kind cx₁ cy₀ u) (gsum lam pt kind cx₁ cy₁ u)) :=
        max_le_max (stepy cx₀) (stepy cx₁)

/-- The aggregated quadratic coefficients of `Σ λ_r G_{p_r,k_r}` at the centre `(cx,cy)` — the
`c0, c1, c2` accumulated in `_gmax`'s inner loop. -/
noncomputable def gsc (lam : Fin n → ℝ) (pt : Fin n → ℝ × ℝ) (kind : Fin n → Fin 4)
    (cx cy : ℝ) : ℝ × ℝ × ℝ :=
  (∑ r : Fin n, lam r * (gc (kind r) ((pt r).1 - cx) ((pt r).2 - cy)).1,
   ∑ r : Fin n, lam r * (gc (kind r) ((pt r).1 - cx) ((pt r).2 - cy)).2.1,
   ∑ r : Fin n, lam r * (gc (kind r) ((pt r).1 - cx) ((pt r).2 - cy)).2.2)

/-- **Lemma E, the `u` half**: the combination is a quadratic in `u` with those coefficients. -/
lemma gsum_eq_quad (lam : Fin n → ℝ) (pt : Fin n → ℝ × ℝ) (kind : Fin n → Fin 4)
    (cx cy u : ℝ) :
    gsum lam pt kind cx cy u
      = (gsc lam pt kind cx cy).1 + (gsc lam pt kind cx cy).2.1 * u
        + (gsc lam pt kind cx cy).2.2 * u ^ 2 := by
  have h : ∀ r : Fin n, lam r * gval (kind r) ((pt r).1 - cx) ((pt r).2 - cy) u
      = lam r * (gc (kind r) ((pt r).1 - cx) ((pt r).2 - cy)).1
        + lam r * (gc (kind r) ((pt r).1 - cx) ((pt r).2 - cy)).2.1 * u
        + lam r * (gc (kind r) ((pt r).1 - cx) ((pt r).2 - cy)).2.2 * u ^ 2 := by
    intro r; rw [gval]; ring
  simp only [gsum, h, gsc]
  rw [Finset.sum_add_distrib, Finset.sum_add_distrib, ← Finset.sum_mul, ← Finset.sum_mul]

/-- `_gmax` at one centre corner: the exact quadratic maximum over the bin. -/
noncomputable def gmaxAt (lam : Fin n → ℝ) (pt : Fin n → ℝ × ℝ) (kind : Fin n → Fin 4)
    (cx cy u₀ u₁ : ℝ) : ℝ :=
  maxQuad (gsc lam pt kind cx cy).1 (gsc lam pt kind cx cy).2.1
    (gsc lam pt kind cx cy).2.2 u₀ u₁

/-- **`_gmax`** of `search/zeromargin.py`: the max over the four centre corners of the exact
quadratic maximum over the bin. -/
noncomputable def gmax (lam : Fin n → ℝ) (pt : Fin n → ℝ × ℝ) (kind : Fin n → Fin 4)
    (cx₀ cx₁ cy₀ cy₁ u₀ u₁ : ℝ) : ℝ :=
  max (max (gmaxAt lam pt kind cx₀ cy₀ u₀ u₁) (gmaxAt lam pt kind cx₀ cy₁ u₀ u₁))
    (max (gmaxAt lam pt kind cx₁ cy₀ u₀ u₁) (gmaxAt lam pt kind cx₁ cy₁ u₀ u₁))

/-- **Lemma E** (`RUNG2.md` §6.2).  `gmax` is an upper bound for `Σ λ_r G_{p_r,k_r}` over the
whole pose box — hence over the admissible poses of the box, which are a subset.  No hypothesis on
the signs of `λ` is needed: the bound holds for *every* real combination (the nonnegativity of `λ`
is what Lemmas F–H need, not what makes the maximum computable). -/
theorem gsum_le_gmax (lam : Fin n → ℝ) (pt : Fin n → ℝ × ℝ) (kind : Fin n → Fin 4)
    {cx₀ cx₁ cy₀ cy₁ u₀ u₁ cx cy u : ℝ}
    (hcx : cx ∈ Set.Icc cx₀ cx₁) (hcy : cy ∈ Set.Icc cy₀ cy₁) (hu : u ∈ Set.Icc u₀ u₁) :
    gsum lam pt kind cx cy u ≤ gmax lam pt kind cx₀ cx₁ cy₀ cy₁ u₀ u₁ := by
  have hat : ∀ x y : ℝ, gsum lam pt kind x y u ≤ gmaxAt lam pt kind x y u₀ u₁ := by
    intro x y
    rw [gsum_eq_quad, gmaxAt]
    exact le_maxQuad hu
  refine le_trans (gsum_le_corners lam pt kind u hcx hcy) ?_
  rw [gmax]
  exact max_le_max (max_le_max (hat cx₀ cy₀) (hat cx₀ cy₁))
    (max_le_max (hat cx₁ cy₀) (hat cx₁ cy₁))

/-- **Lemma E, exactness**: `gmax` is attained at a pose of the box, so it is the true maximum and
the `_gmax` test `gmax ≤ 0` is not merely sufficient — it is *equivalent* to
`Σ λ_r G_{p_r,k_r} ≤ 0` on the whole box. -/
theorem gmax_mem (lam : Fin n → ℝ) (pt : Fin n → ℝ × ℝ) (kind : Fin n → Fin 4)
    {cx₀ cx₁ cy₀ cy₁ u₀ u₁ : ℝ} (hx : cx₀ ≤ cx₁) (hy : cy₀ ≤ cy₁) (hu : u₀ ≤ u₁) :
    ∃ cx ∈ Set.Icc cx₀ cx₁, ∃ cy ∈ Set.Icc cy₀ cy₁, ∃ u ∈ Set.Icc u₀ u₁,
      gsum lam pt kind cx cy u = gmax lam pt kind cx₀ cx₁ cy₀ cy₁ u₀ u₁ := by
  have hone : ∃ cx ∈ Set.Icc cx₀ cx₁, ∃ cy ∈ Set.Icc cy₀ cy₁,
      gmaxAt lam pt kind cx cy u₀ u₁ = gmax lam pt kind cx₀ cx₁ cy₀ cy₁ u₀ u₁ := by
    rw [gmax]
    rcases max_cases (max (gmaxAt lam pt kind cx₀ cy₀ u₀ u₁) (gmaxAt lam pt kind cx₀ cy₁ u₀ u₁))
      (max (gmaxAt lam pt kind cx₁ cy₀ u₀ u₁) (gmaxAt lam pt kind cx₁ cy₁ u₀ u₁)) with
      ⟨he, -⟩ | ⟨he, -⟩
    · rw [he]
      rcases max_cases (gmaxAt lam pt kind cx₀ cy₀ u₀ u₁) (gmaxAt lam pt kind cx₀ cy₁ u₀ u₁) with
        ⟨he2, -⟩ | ⟨he2, -⟩
      · exact ⟨cx₀, ⟨le_rfl, hx⟩, cy₀, ⟨le_rfl, hy⟩, he2.symm⟩
      · exact ⟨cx₀, ⟨le_rfl, hx⟩, cy₁, ⟨hy, le_rfl⟩, he2.symm⟩
    · rw [he]
      rcases max_cases (gmaxAt lam pt kind cx₁ cy₀ u₀ u₁) (gmaxAt lam pt kind cx₁ cy₁ u₀ u₁) with
        ⟨he2, -⟩ | ⟨he2, -⟩
      · exact ⟨cx₁, ⟨hx, le_rfl⟩, cy₀, ⟨le_rfl, hy⟩, he2.symm⟩
      · exact ⟨cx₁, ⟨hx, le_rfl⟩, cy₁, ⟨hy, le_rfl⟩, he2.symm⟩
  obtain ⟨cx, hcx, cy, hcy, he⟩ := hone
  obtain ⟨u, hu', hval⟩ := maxQuad_mem (a₀ := (gsc lam pt kind cx cy).1)
    (a₁ := (gsc lam pt kind cx cy).2.1) (a₂ := (gsc lam pt kind cx cy).2.2) hu
  exact ⟨cx, hcx, cy, hcy, u, hu', by rw [gsum_eq_quad, hval, ← he, gmaxAt]⟩

/-! ## 4.  Lemmas F, G, H — what makes `CHAIN` sound (`RUNG2.md` §6.2) -/

/-- **Lemma G** (`RUNG2.md` §6.2, the opposite side).  If `G_a + λ G_q ≤ 0` with `λ > 0`, then at
every pose where `G_q > 0` one has `G_a < 0`. -/
theorem lemmaG {ga gq lam : ℝ} (hlam : 0 < lam) (h : ga + lam * gq ≤ 0) (hq : 0 < gq) :
    ga < 0 := by
  nlinarith

/-- The `λ ≥ 0` variant, with the weak conclusion: `G_a ≤ 0` whenever `G_q ≥ 0`. -/
theorem lemmaG' {ga gq lam : ℝ} (hlam : 0 ≤ lam) (h : ga + lam * gq ≤ 0) (hq : 0 ≤ gq) :
    ga ≤ 0 := by
  nlinarith

/-- **Lemma H** (`RUNG2.md` §6.2, empty product regions).  If `G_q + λ G_q' ≤ 0` with `λ > 0`,
then `G_q` and `G_q'` are never both positive. -/
theorem lemmaH {gq gq' lam : ℝ} (hlam : 0 < lam) (h : gq + lam * gq' ≤ 0) :
    ¬(0 < gq ∧ 0 < gq') := by
  rintro ⟨h1, h2⟩; nlinarith

/-- **Lemma G, box form.**  The two-term combination that `cert_chain`'s `gmax1` tests: if
`_gmax [(1, a, ka), (lam, q, kq)] box ≤ 0` with `lam > 0`, then at every pose of the box at which
`q`'s inequality of kind `kq` is violated, `a`'s inequality of kind `ka` holds strictly. -/
theorem lemmaG_box (lam : ℝ) (hlam : 0 < lam) (pa pq : ℝ × ℝ) (ka kq : Fin 4)
    {cx₀ cx₁ cy₀ cy₁ u₀ u₁ cx cy u : ℝ}
    (hmax : gmax ![1, lam] ![pa, pq] ![ka, kq] cx₀ cx₁ cy₀ cy₁ u₀ u₁ ≤ 0)
    (hcx : cx ∈ Set.Icc cx₀ cx₁) (hcy : cy ∈ Set.Icc cy₀ cy₁) (hu : u ∈ Set.Icc u₀ u₁)
    (hq : 0 < gval kq (pq.1 - cx) (pq.2 - cy) u) :
    gval ka (pa.1 - cx) (pa.2 - cy) u < 0 := by
  have h := le_trans (gsum_le_gmax ![1, lam] ![pa, pq] ![ka, kq] hcx hcy hu) hmax
  simp only [gsum, Fin.sum_univ_two, Matrix.cons_val_zero, Matrix.cons_val_one,
    one_mul] at h
  nlinarith

/-- **Lemma H, box form.**  If `_gmax [(1, q, kq), (lam, q', kq')] box ≤ 0` with `lam > 0`, then no
pose of the box violates both inequalities: the corresponding `CHAIN` product region is empty and
needs no witness. -/
theorem lemmaH_box (lam : ℝ) (hlam : 0 < lam) (pq pq' : ℝ × ℝ) (kq kq' : Fin 4)
    {cx₀ cx₁ cy₀ cy₁ u₀ u₁ cx cy u : ℝ}
    (hmax : gmax ![1, lam] ![pq, pq'] ![kq, kq'] cx₀ cx₁ cy₀ cy₁ u₀ u₁ ≤ 0)
    (hcx : cx ∈ Set.Icc cx₀ cx₁) (hcy : cy ∈ Set.Icc cy₀ cy₁) (hu : u ∈ Set.Icc u₀ u₁) :
    ¬(0 < gval kq (pq.1 - cx) (pq.2 - cy) u ∧ 0 < gval kq' (pq'.1 - cx) (pq'.2 - cy) u) := by
  have h := le_trans (gsum_le_gmax ![1, lam] ![pq, pq'] ![kq, kq'] hcx hcy hu) hmax
  simp only [gsum, Fin.sum_univ_two, Matrix.cons_val_zero, Matrix.cons_val_one,
    one_mul] at h
  rintro ⟨h1, h2⟩; nlinarith

/-- **The chain comparison** that `cert_chain` tests with `_gmax [(1, p, kp), (-1, q, kq)] ≤ 0`:
`G_p ≤ G_q` at every pose of the box.  (This is the one place the checker uses a *negative*
multiplier, which Lemma E covers.) -/
theorem gval_le_of_gmax_sub (pp pq : ℝ × ℝ) (kp kq : Fin 4)
    {cx₀ cx₁ cy₀ cy₁ u₀ u₁ cx cy u : ℝ}
    (hmax : gmax ![1, -1] ![pp, pq] ![kp, kq] cx₀ cx₁ cy₀ cy₁ u₀ u₁ ≤ 0)
    (hcx : cx ∈ Set.Icc cx₀ cx₁) (hcy : cy ∈ Set.Icc cy₀ cy₁) (hu : u ∈ Set.Icc u₀ u₁) :
    gval kp (pp.1 - cx) (pp.2 - cy) u ≤ gval kq (pq.1 - cx) (pq.2 - cy) u := by
  have h := le_trans (gsum_le_gmax ![1, -1] ![pp, pq] ![kp, kq] hcx hcy hu) hmax
  simp only [gsum, Fin.sum_univ_two, Matrix.cons_val_zero, Matrix.cons_val_one,
    one_mul, neg_mul] at h
  linarith

/-- **Lemma F** (`RUNG2.md` §6.2, chain).  Let `g 1 ≤ g 2 ≤ … ≤ g k` be the values at a given pose
of a chain of violation polynomials, monotone on the box (each consecutive comparison certified by
`gval_le_of_gmax_sub`).  Then the pose lies in exactly one of the `k+1` regions
`R₀ = {g 1 > 0}`, `R_r = {g r ≤ 0 < g (r+1)}`, `R_k = {g k ≤ 0}`: there is an `r ≤ k` with
`g j ≤ 0` for all `1 ≤ j ≤ r` and `g j > 0` for all `r < j ≤ k`.  The regions therefore cover the
box, which is what lets `cert_chain` use a different witness set in each. -/
theorem chain_regions_cover (k : ℕ) (g : ℕ → ℝ) (hmono : ∀ i j, i ≤ j → g i ≤ g j) :
    ∃ r ≤ k, (∀ j, 1 ≤ j → j ≤ r → g j ≤ 0) ∧ (∀ j, r < j → j ≤ k → 0 < g j) := by
  induction k with
  | zero => exact ⟨0, le_rfl, fun j hj1 hj2 => by omega, fun j hj1 hj2 => by omega⟩
  | succ k ih =>
    obtain ⟨r, hrk, h1, h2⟩ := ih
    by_cases h : g (k + 1) ≤ 0
    · exact ⟨k + 1, le_rfl, fun j _ hj2 => le_trans (hmono j (k + 1) hj2) h,
        fun j hj _ => by omega⟩
    · refine ⟨r, le_trans hrk (Nat.le_succ k), h1, fun j hjr hjk => ?_⟩
      rcases Nat.lt_or_ge j (k + 1) with hlt | hge
      · exact h2 j hjr (by omega)
      · have hj : j = k + 1 := by omega
        rw [hj]; exact not_le.mp h

/-- **Lemma F, the down-set half.**  On the region `{G_{q_r} ≤ 0}` every point whose violation
polynomial is dominated by `G_{q_r}` on the box satisfies its own inequality — not just the chain
members.  (This is `analyse`'s `down` binary search in `cert_chain`.) -/
theorem chain_region_down {gp gq : ℝ} (h : gp ≤ gq) (hq : gq ≤ 0) : gp ≤ 0 := le_trans h hq

/-! ## 5.  `clip_bin` (`RUNG2.md` §4.6) -/

/-- `w` as a function of `u = tan(θ/2)` on `[0°,45°]`: `w = cos θ + sin θ = ((1−u²)+2u)/(1+u²)`. -/
noncomputable def widU (u : ℝ) : ℝ := (1 - u ^ 2 + 2 * u) / (1 + u ^ 2)

lemma wid_two_arctan {u : ℝ} (h0 : 0 ≤ u) (h1 : u ≤ 1) :
    wid (2 * Real.arctan u) = widU u := by
  have hpos : (0 : ℝ) < 1 + u ^ 2 := by positivity
  have hc : (0 : ℝ) ≤ (1 - u ^ 2) / (1 + u ^ 2) := by
    apply div_nonneg _ (le_of_lt hpos); nlinarith
  have hs : (0 : ℝ) ≤ 2 * u / (1 + u ^ 2) := by
    apply div_nonneg _ (le_of_lt hpos); linarith
  rw [wid, cos_two_arctan, sin_two_arctan, abs_of_nonneg hc, abs_of_nonneg hs, widU]
  field_simp

/-- At `u = √2 − 1` (i.e. `45°`) one has `s² + 2s = 1`, so `w = 1 + s² + 2s − ... = √2`. -/
lemma sqrt_two_sub_one_sq : (Real.sqrt 2 - 1) ^ 2 + 2 * (Real.sqrt 2 - 1) = 1 := by
  have h : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  nlinarith [h]

lemma sqrt_two_sub_one_nonneg : (0 : ℝ) ≤ Real.sqrt 2 - 1 := by
  nlinarith [Real.sq_sqrt (show (0:ℝ) ≤ 2 by norm_num), Real.sqrt_nonneg 2]

lemma sqrt_two_sub_one_lt_one : Real.sqrt 2 - 1 < 1 := by
  nlinarith [Real.sq_sqrt (show (0:ℝ) ≤ 2 by norm_num), Real.sqrt_nonneg 2]

/-- **`w` is strictly increasing in `u` on `[0°,45°]`** — `clip_bin`'s monotonicity hypothesis,
which is why `{u : w(u) ≤ K}` is an initial segment `[u₀, u⁻]` of the bin. -/
theorem widU_strictMonoOn : StrictMonoOn widU (Set.Icc 0 (Real.sqrt 2 - 1)) := by
  intro x hx y hy hxy
  have hxd : (0 : ℝ) < 1 + x ^ 2 := by positivity
  have hyd : (0 : ℝ) < 1 + y ^ 2 := by positivity
  have hs := sqrt_two_sub_one_sq
  have hsum : x + y + x * y < 1 := by
    nlinarith [hx.1, hx.2, hy.1, hy.2, hxy, hs, sqrt_two_sub_one_nonneg]
  have key : widU y - widU x
      = 2 * (y - x) * (1 - (x + y + x * y)) / ((1 + x ^ 2) * (1 + y ^ 2)) := by
    rw [widU, widU]; field_simp; ring
  have hnum : 0 < 2 * (y - x) * (1 - (x + y + x * y)) :=
    mul_pos (by linarith) (by linarith)
  have hdiff : 0 < widU y - widU x := by
    rw [key]; exact div_pos hnum (mul_pos hxd hyd)
  linarith

/-- **The admissibility bound `clip_bin` uses** (`RUNG2.md` §4.6).  Every admissible pose of a box
has `w(θ) ≤ K` with `K = 2 min(cx₁, m−cx₀, cy₁, m−cy₀)`. -/
theorem adm_widU_le (m : ℝ) {cx₀ cx₁ cy₀ cy₁ : ℝ} {c : ℝ × ℝ} {u : ℝ}
    (h0 : 0 ≤ u) (h1 : u ≤ 1)
    (hcx : c.1 ∈ Set.Icc cx₀ cx₁) (hcy : c.2 ∈ Set.Icc cy₀ cy₁)
    (hsub : sq c (2 * Real.arctan u) 1 ⊆ box m) :
    widU u ≤ 2 * min (min cx₁ (m - cx₀)) (min cy₁ (m - cy₀)) := by
  obtain ⟨ha1, ha2, ha3, ha4⟩ := (sq_subset_box_iff m c (2 * Real.arctan u)).mp hsub
  rw [← wid_two_arctan h0 h1]
  have b1 : wid (2 * Real.arctan u) / 2 ≤ cx₁ := le_trans ha1 hcx.2
  have b2 : wid (2 * Real.arctan u) / 2 ≤ m - cx₀ := by linarith [hcx.1]
  have b3 : wid (2 * Real.arctan u) / 2 ≤ cy₁ := le_trans ha3 hcy.2
  have b4 : wid (2 * Real.arctan u) / 2 ≤ m - cy₀ := by linarith [hcy.1]
  have h := le_min (le_min b1 b2) (le_min b3 b4)
  linarith

/-- **`clip_bin` loses no admissible pose** (`RUNG2.md` §4.6).  Let the bin `[u₀,u₁]` lie inside
`[0°,45°]` and let `u*` be any point of the bin with `widU u* ≥ K`, where
`K = 2 min(cx₁, m−cx₀, cy₁, m−cy₀)` — that is the invariant `clip_bin` maintains, returning a
rational `u* ≥ u⁻` *from above* by bisection.  Then every admissible pose of the box has
`u ≤ u*`, so the box may be replaced by its sub-box with bin `[u₀,u*]`. -/
theorem clip_bin_no_loss (m : ℝ) {cx₀ cx₁ cy₀ cy₁ u₀ u₁ ustar : ℝ}
    (h0 : 0 ≤ u₀) (h45 : u₁ ≤ Real.sqrt 2 - 1) (hstar : ustar ∈ Set.Icc u₀ u₁)
    (hK : 2 * min (min cx₁ (m - cx₀)) (min cy₁ (m - cy₀)) ≤ widU ustar)
    {c : ℝ × ℝ} {u : ℝ} (hu : u ∈ Set.Icc u₀ u₁)
    (hcx : c.1 ∈ Set.Icc cx₀ cx₁) (hcy : c.2 ∈ Set.Icc cy₀ cy₁)
    (hsub : sq c (2 * Real.arctan u) 1 ⊆ box m) :
    u ∈ Set.Icc u₀ ustar := by
  have hs1 : Real.sqrt 2 - 1 < 1 := sqrt_two_sub_one_lt_one
  have humem : u ∈ Set.Icc (0 : ℝ) (Real.sqrt 2 - 1) := ⟨le_trans h0 hu.1, le_trans hu.2 h45⟩
  have hsmem : ustar ∈ Set.Icc (0 : ℝ) (Real.sqrt 2 - 1) :=
    ⟨le_trans h0 hstar.1, le_trans hstar.2 h45⟩
  have hadm := adm_widU_le m (le_trans h0 hu.1)
    (le_of_lt (lt_of_le_of_lt humem.2 hs1)) hcx hcy hsub
  refine ⟨hu.1, ?_⟩
  by_contra hgt
  push_neg at hgt
  have hmono := widU_strictMonoOn hsmem humem hgt
  linarith

/-! ## 6.  Lemma B — the centre bounds are polynomials in `u` (`RUNG2.md` §3.2, `_xn`/`_cond_poly`)

The corner values `A_x(θ), B_x(θ)` of Lemma A are not polynomial in `u`, but each of the three
bounds the checker offers is: written as `X_n(u)/(2(1+u²))` with `X_n` a quadratic.  Substituting
them into Lemma A's inequalities and clearing the positive denominator `(1+u²)²` gives a
degree-`≤ 4` polynomial with rational coefficients — `_cond_poly` of `search/zeromargin.py`. -/

/-- Evaluate a quadratic coefficient triple `(a₀,a₁,a₂)`. -/
def qeval (a : ℝ × ℝ × ℝ) (u : ℝ) : ℝ := a.1 + a.2.1 * u + a.2.2 * u ^ 2

/-- Evaluate a degree-4 coefficient tuple `(a₀,…,a₄)`. -/
def qeval4 (a : ℝ × ℝ × ℝ × ℝ × ℝ) (u : ℝ) : ℝ :=
  a.1 + a.2.1 * u + a.2.2.1 * u ^ 2 + a.2.2.2.1 * u ^ 3 + a.2.2.2.2 * u ^ 4

/-- `_xn 'R' a`: the constant bound `c = a`, as `X_n = 2a(1+u²)`. -/
def xnR (a : ℝ) : ℝ × ℝ × ℝ := (2 * a, 0, 2 * a)

/-- `_xn 'W'`: the near-wall bound `c ≥ w(θ)/2`, as `X_n = (1−u²) + 2u`. -/
def xnW : ℝ × ℝ × ℝ := (1, 2, -1)

/-- `_xn 'M'`: the far-wall bound `c ≤ m − w(θ)/2`, as `X_n = 2m(1+u²) − (1−u²) − 2u`. -/
def xnM (m : ℝ) : ℝ × ℝ × ℝ := (2 * m - 1, -2, 2 * m + 1)

/-- The `'R'` bound really is the constant `a`. -/
lemma xnR_spec (a u : ℝ) : qeval (xnR a) u / (2 * (1 + u ^ 2)) = a := by
  have hpos : (0 : ℝ) < 1 + u ^ 2 := by positivity
  rw [qeval, xnR]
  field_simp
  ring

/-- The `'W'` bound really is `w(θ)/2` (for `u ∈ [0,1]`, i.e. `θ ∈ [0°,90°]`). -/
lemma xnW_spec {u : ℝ} (h0 : 0 ≤ u) (h1 : u ≤ 1) :
    qeval xnW u / (2 * (1 + u ^ 2)) = wid (2 * Real.arctan u) / 2 := by
  have hpos : (0 : ℝ) < 1 + u ^ 2 := by positivity
  rw [wid_two_arctan h0 h1, qeval, xnW, widU]
  field_simp
  ring

/-- The `'M'` bound really is `m − w(θ)/2`. -/
lemma xnM_spec (m : ℝ) {u : ℝ} (h0 : 0 ≤ u) (h1 : u ≤ 1) :
    qeval (xnM m) u / (2 * (1 + u ^ 2)) = m - wid (2 * Real.arctan u) / 2 := by
  have hpos : (0 : ℝ) < 1 + u ^ 2 := by positivity
  rw [wid_two_arctan h0 h1, qeval, xnM, widU]
  field_simp
  ring

/-- `U = 2(1+u²) p_x − X_n`, as a quadratic coefficient triple (`_adm_cond_ok`'s `U`, `V`). -/
def ucoef (px : ℝ) (Xn : ℝ × ℝ × ℝ) : ℝ × ℝ × ℝ :=
  (2 * px - Xn.1, -Xn.2.1, 2 * px - Xn.2.2)

lemma ucoef_spec (px : ℝ) (Xn : ℝ × ℝ × ℝ) (u : ℝ) :
    qeval (ucoef px Xn) u = 2 * (1 + u ^ 2) * px - qeval Xn u := by
  rw [qeval, qeval, ucoef]; ring

/-- **`_cond_poly`** of `search/zeromargin.py` (the general, degree-4 branch), `RUNG2.md` §3.2:
`G₁ = U·C + V·S − N²`, `G₂ = −U·C − V·S − N²`, `G₃ = −U·S + V·C − N²`, `G₄ = U·S − V·C − N²`
with `C = 1−u²`, `S = 2u`, `N = 1+u²`, written out in the monomial basis. -/
def condPoly : Fin 4 → (ℝ × ℝ × ℝ) → (ℝ × ℝ × ℝ) → ℝ × ℝ × ℝ × ℝ × ℝ
  | 0, U, V => (U.1 - 1, U.2.1 + 2 * V.1, U.2.2 - U.1 + 2 * V.2.1 - 2,
                -U.2.1 + 2 * V.2.2, -U.2.2 - 1)
  | 1, U, V => (-U.1 - 1, -U.2.1 - 2 * V.1, U.1 - U.2.2 - 2 * V.2.1 - 2,
                U.2.1 - 2 * V.2.2, U.2.2 - 1)
  | 2, U, V => (V.1 - 1, V.2.1 - 2 * U.1, V.2.2 - V.1 - 2 * U.2.1 - 2,
                -V.2.1 - 2 * U.2.2, -V.2.2 - 1)
  | 3, U, V => (-V.1 - 1, 2 * U.1 - V.2.1, V.1 - V.2.2 + 2 * U.2.1 - 2,
                V.2.1 + 2 * U.2.2, V.2.2 - 1)

/-- `G₁ = U·C + V·S − N²`: `_cond_poly`'s coefficients for `cond = 0` (`X ≤ ½`). -/
lemma condPoly_zero (U V : ℝ × ℝ × ℝ) (u : ℝ) :
    qeval4 (condPoly 0 U V) u
      = qeval U u * (1 - u ^ 2) + qeval V u * (2 * u) - (1 + u ^ 2) ^ 2 := by
  simp only [qeval4, qeval, condPoly]; ring

/-- `G₂ = −U·C − V·S − N²`: `cond = 1` (`X ≥ -½`). -/
lemma condPoly_one (U V : ℝ × ℝ × ℝ) (u : ℝ) :
    qeval4 (condPoly 1 U V) u
      = -(qeval U u * (1 - u ^ 2)) - qeval V u * (2 * u) - (1 + u ^ 2) ^ 2 := by
  simp only [qeval4, qeval, condPoly]; ring

/-- `G₃ = −U·S + V·C − N²`: `cond = 2` (`Y ≤ ½`). -/
lemma condPoly_two (U V : ℝ × ℝ × ℝ) (u : ℝ) :
    qeval4 (condPoly 2 U V) u
      = -(qeval U u * (2 * u)) + qeval V u * (1 - u ^ 2) - (1 + u ^ 2) ^ 2 := by
  simp only [qeval4, qeval, condPoly]; ring

/-- `G₄ = U·S − V·C − N²`: `cond = 3` (`Y ≥ -½`). -/
lemma condPoly_three (U V : ℝ × ℝ × ℝ) (u : ℝ) :
    qeval4 (condPoly 3 U V) u
      = qeval U u * (2 * u) - qeval V u * (1 - u ^ 2) - (1 + u ^ 2) ^ 2 := by
  simp only [qeval4, qeval, condPoly]; ring

/-- **Lemma B** (`RUNG2.md` §3.2).  With the centre corner taken at the polynomial bounds
`A_x = X_n(u)/(2(1+u²))`, `A_y = Y_n(u)/(2(1+u²))`, the degree-4 polynomial `_cond_poly` returns
is `(1+u²)` times the violation polynomial `G_{p,k}` of the corresponding offsets.  Since
`1+u² > 0`, the checker's test `_poly_ok` (`max G ≤ 0`) is exactly the geometric condition
`|X| ≤ ½`, `|Y| ≤ ½` at that corner. -/
theorem condPoly_eq_gval (k : Fin 4) (px py : ℝ) (Xn Yn : ℝ × ℝ × ℝ) (u : ℝ) :
    qeval4 (condPoly k (ucoef px Xn) (ucoef py Yn)) u
      = (1 + u ^ 2) * gval k (px - qeval Xn u / (2 * (1 + u ^ 2)))
          (py - qeval Yn u / (2 * (1 + u ^ 2))) u := by
  have hpos : (0 : ℝ) < 1 + u ^ 2 := by positivity
  have hne : (1 : ℝ) + u ^ 2 ≠ 0 := ne_of_gt hpos
  fin_cases k <;>
    simp only [qeval4, qeval, condPoly, ucoef, gval, gc] <;>
    field_simp <;>
    ring

/-- `_poly_ok`'s verdict on `_cond_poly` is exactly the geometric condition. -/
theorem condPoly_nonpos_iff (k : Fin 4) (px py : ℝ) (Xn Yn : ℝ × ℝ × ℝ) (u : ℝ) :
    qeval4 (condPoly k (ucoef px Xn) (ucoef py Yn)) u ≤ 0
      ↔ gval k (px - qeval Xn u / (2 * (1 + u ^ 2)))
          (py - qeval Yn u / (2 * (1 + u ^ 2))) u ≤ 0 := by
  have hpos : (0 : ℝ) < 1 + u ^ 2 := by positivity
  rw [condPoly_eq_gval]
  constructor
  · intro h; nlinarith
  · intro h; nlinarith

/-- **Lemma B's `both_rect` reduction.**  When both bounds are of kind `'R'`, `U` and `V` carry the
factor `N = 1+u²`, so `G` does too, and dividing it out leaves the *quadratic* `G_{p,k}` itself —
which is exactly the triple `_cond_poly` returns in its `both_rect` branch, and why `_poly_ok`
then takes the exact `_max_quad` route with no Bernstein slack. -/
theorem condPoly_rect (k : Fin 4) (px py a b u : ℝ) :
    qeval4 (condPoly k (ucoef px (xnR a)) (ucoef py (xnR b))) u
      = (1 + u ^ 2) * gval k (px - a) (py - b) u := by
  rw [condPoly_eq_gval, xnR_spec, xnR_spec]

/-! ## 7.  Lemma C, degree 3–4 — the Bernstein enclosure (`RUNG2.md` §3.3, `_max_bern`)

For degree `3, 4` the checker bounds `max_{[u₀,u₁]} G` by the largest Bernstein coefficient of `G`
in the degree-4 Bernstein basis on `[u₀,u₁]`.  Because the degree is fixed at 4 the whole thing is
five explicit polynomial identities, verified here by `ring`. -/

/-- `_max_bern`'s shifted monomial coefficients `b_j = Σ_{k≥j} a_k C(k,j) u₀^{k-j} h^j`, i.e. the
coefficients of `G(u₀ + h t)` as a polynomial in `t`. -/
def bshift (a : ℝ × ℝ × ℝ × ℝ × ℝ) (u₀ h : ℝ) : ℝ × ℝ × ℝ × ℝ × ℝ :=
  (a.1 + a.2.1 * u₀ + a.2.2.1 * u₀ ^ 2 + a.2.2.2.1 * u₀ ^ 3 + a.2.2.2.2 * u₀ ^ 4,
   (a.2.1 + 2 * a.2.2.1 * u₀ + 3 * a.2.2.2.1 * u₀ ^ 2 + 4 * a.2.2.2.2 * u₀ ^ 3) * h,
   (a.2.2.1 + 3 * a.2.2.2.1 * u₀ + 6 * a.2.2.2.2 * u₀ ^ 2) * h ^ 2,
   (a.2.2.2.1 + 4 * a.2.2.2.2 * u₀) * h ^ 3,
   a.2.2.2.2 * h ^ 4)

/-- `_max_bern`'s Bernstein coefficients `β_i = Σ_{j≤i} [C(i,j)/C(4,j)] b_j`. -/
noncomputable def bernCoef (b : ℝ × ℝ × ℝ × ℝ × ℝ) : ℝ × ℝ × ℝ × ℝ × ℝ :=
  (b.1,
   b.1 + b.2.1 / 4,
   b.1 + 2 * b.2.1 / 4 + b.2.2.1 / 6,
   b.1 + 3 * b.2.1 / 4 + 3 * b.2.2.1 / 6 + b.2.2.2.1 / 4,
   b.1 + b.2.1 + b.2.2.1 + b.2.2.2.1 + b.2.2.2.2)

/-- **`_max_bern`** of `search/zeromargin.py`: the largest Bernstein coefficient. -/
noncomputable def maxBern (a : ℝ × ℝ × ℝ × ℝ × ℝ) (u₀ u₁ : ℝ) : ℝ :=
  max (max (max (max (bernCoef (bshift a u₀ (u₁ - u₀))).1
    (bernCoef (bshift a u₀ (u₁ - u₀))).2.1)
    (bernCoef (bshift a u₀ (u₁ - u₀))).2.2.1)
    (bernCoef (bshift a u₀ (u₁ - u₀))).2.2.2.1)
    (bernCoef (bshift a u₀ (u₁ - u₀))).2.2.2.2

/-- The affine change of variable `u = u₀ + h t`. -/
lemma qeval4_bshift (a : ℝ × ℝ × ℝ × ℝ × ℝ) (u₀ h t : ℝ) :
    qeval4 a (u₀ + h * t) = qeval4 (bshift a u₀ h) t := by
  simp only [qeval4, bshift]; ring

/-- **The Bernstein representation** in degree 4: `Σ_j b_j t^j = Σ_i β_i B_{i,4}(t)`. -/
lemma qeval4_eq_bern (b : ℝ × ℝ × ℝ × ℝ × ℝ) (t : ℝ) :
    qeval4 b t
      = (bernCoef b).1 * (1 - t) ^ 4 + (bernCoef b).2.1 * (4 * t * (1 - t) ^ 3)
        + (bernCoef b).2.2.1 * (6 * t ^ 2 * (1 - t) ^ 2)
        + (bernCoef b).2.2.2.1 * (4 * t ^ 3 * (1 - t)) + (bernCoef b).2.2.2.2 * t ^ 4 := by
  simp only [qeval4, bernCoef]; ring

/-- **The convex-hull property** of the degree-4 Bernstein basis: the basis functions are
nonnegative on `[0,1]` and sum to `1`, so a combination is bounded by its largest coefficient. -/
lemma bern_le_max {β₀ β₁ β₂ β₃ β₄ t : ℝ} (h0 : 0 ≤ t) (h1 : t ≤ 1) :
    β₀ * (1 - t) ^ 4 + β₁ * (4 * t * (1 - t) ^ 3) + β₂ * (6 * t ^ 2 * (1 - t) ^ 2)
        + β₃ * (4 * t ^ 3 * (1 - t)) + β₄ * t ^ 4
      ≤ max (max (max (max β₀ β₁) β₂) β₃) β₄ := by
  have ht : (0 : ℝ) ≤ 1 - t := by linarith
  have hb0 : (0 : ℝ) ≤ (1 - t) ^ 4 := by positivity
  have hb1 : (0 : ℝ) ≤ 4 * t * (1 - t) ^ 3 :=
    mul_nonneg (by linarith) (pow_nonneg ht 3)
  have hb2 : (0 : ℝ) ≤ 6 * t ^ 2 * (1 - t) ^ 2 := by positivity
  have hb3 : (0 : ℝ) ≤ 4 * t ^ 3 * (1 - t) :=
    mul_nonneg (by positivity) ht
  have hb4 : (0 : ℝ) ≤ t ^ 4 := by positivity
  set M := max (max (max (max β₀ β₁) β₂) β₃) β₄ with hM
  have m0 : β₀ ≤ M := le_max_of_le_left (le_max_of_le_left (le_max_of_le_left (le_max_left _ _)))
  have m1 : β₁ ≤ M := le_max_of_le_left (le_max_of_le_left (le_max_of_le_left (le_max_right _ _)))
  have m2 : β₂ ≤ M := le_max_of_le_left (le_max_of_le_left (le_max_right _ _))
  have m3 : β₃ ≤ M := le_max_of_le_left (le_max_right _ _)
  have m4 : β₄ ≤ M := le_max_right _ _
  have hsum : (1 - t) ^ 4 + 4 * t * (1 - t) ^ 3 + 6 * t ^ 2 * (1 - t) ^ 2
      + 4 * t ^ 3 * (1 - t) + t ^ 4 = 1 := by ring
  have hfin : M * (1 - t) ^ 4 + M * (4 * t * (1 - t) ^ 3) + M * (6 * t ^ 2 * (1 - t) ^ 2)
      + M * (4 * t ^ 3 * (1 - t)) + M * t ^ 4 = M := by linear_combination M * hsum
  have e0 := mul_le_mul_of_nonneg_right m0 hb0
  have e1 := mul_le_mul_of_nonneg_right m1 hb1
  have e2 := mul_le_mul_of_nonneg_right m2 hb2
  have e3 := mul_le_mul_of_nonneg_right m3 hb3
  have e4 := mul_le_mul_of_nonneg_right m4 hb4
  linarith [e0, e1, e2, e3, e4, hfin]

/-- **Lemma C, the Bernstein branch** (`RUNG2.md` §3.3).  `_max_bern` is a sound upper bound for a
degree-`≤ 4` polynomial on `[u₀,u₁]`, so `ADM` never certifies a box it should not. -/
theorem qeval4_le_maxBern (a : ℝ × ℝ × ℝ × ℝ × ℝ) {u₀ u₁ u : ℝ} (hu : u ∈ Set.Icc u₀ u₁) :
    qeval4 a u ≤ maxBern a u₀ u₁ := by
  obtain ⟨hlo, hhi⟩ := hu
  rcases eq_or_lt_of_le (hlo.trans hhi) with heq | hlt
  · -- degenerate bin: `β₀ = G(u₀) = G(u)`
    have hu0 : u = u₀ := le_antisymm (heq ▸ hhi) hlo
    have : qeval4 a u = (bernCoef (bshift a u₀ (u₁ - u₀))).1 := by
      rw [hu0]; simp only [qeval4, bernCoef, bshift]
    rw [this, maxBern]
    exact le_max_of_le_left (le_max_of_le_left (le_max_of_le_left (le_max_left _ _)))
  · have hh : (0 : ℝ) < u₁ - u₀ := by linarith
    have hne : u₁ - u₀ ≠ 0 := ne_of_gt hh
    have hsub : u₀ + (u₁ - u₀) * ((u - u₀) / (u₁ - u₀)) = u := by field_simp; ring
    have ht0 : (0 : ℝ) ≤ (u - u₀) / (u₁ - u₀) := div_nonneg (by linarith) (le_of_lt hh)
    have ht1 : (u - u₀) / (u₁ - u₀) ≤ 1 := by
      rw [div_le_one hh]; linarith
    calc qeval4 a u
        = qeval4 (bshift a u₀ (u₁ - u₀)) ((u - u₀) / (u₁ - u₀)) := by
          rw [← qeval4_bshift, hsub]
      _ = _ := qeval4_eq_bern _ _
      _ ≤ maxBern a u₀ u₁ := by rw [maxBern]; exact bern_le_max ht0 ht1

/-- **The Bernstein bound is exact at the endpoints** (`RUNG2.md` §3.3: `β₀ = G(u₀)`,
`β₄ = G(u₁)`). -/
theorem bern_endpoints (a : ℝ × ℝ × ℝ × ℝ × ℝ) (u₀ u₁ : ℝ) :
    (bernCoef (bshift a u₀ (u₁ - u₀))).1 = qeval4 a u₀ ∧
      (bernCoef (bshift a u₀ (u₁ - u₀))).2.2.2.2 = qeval4 a u₁ := by
  refine ⟨?_, ?_⟩
  · simp only [qeval4, bernCoef, bshift]
  · simp only [qeval4, bernCoef, bshift]; ring

/-- **`_poly_ok`, general branch**: if `_max_bern ≤ 0` then the condition holds at every `u` of the
bin. -/
theorem polyOk_bern {a : ℝ × ℝ × ℝ × ℝ × ℝ} {u₀ u₁ : ℝ} (h : maxBern a u₀ u₁ ≤ 0)
    {u : ℝ} (hu : u ∈ Set.Icc u₀ u₁) : qeval4 a u ≤ 0 :=
  le_trans (qeval4_le_maxBern a hu) h

/-- **`_poly_ok`, degree-`≤ 2` branch**: if the top two coefficients vanish then `_max_quad` is
used, and it is exact. -/
theorem polyOk_quad {a : ℝ × ℝ × ℝ × ℝ × ℝ} {u₀ u₁ : ℝ}
    (h3 : a.2.2.2.1 = 0) (h4 : a.2.2.2.2 = 0) (h : maxQuad a.1 a.2.1 a.2.2.1 u₀ u₁ ≤ 0)
    {u : ℝ} (hu : u ∈ Set.Icc u₀ u₁) : qeval4 a u ≤ 0 := by
  have e : qeval4 a u = a.1 + a.2.1 * u + a.2.2.1 * u ^ 2 := by
    simp only [qeval4, h3, h4]; ring
  rw [e]
  exact le_trans (le_maxQuad hu) h

end SquarePacking
