import Sqpack.CovMP
import Sqpack.SegParts

/-!
# Lemma Z: the `θ = 0` face, exactly (the `AXIS` leaf)

`search/QUADRANT_EXACT.md` §4.1.  At `θ = 0` the square is `Q(c) = [c_x − ½, c_x + ½] × [c_y − ½, c_y + ½]`
and the mass it captures from

* a point `(X, Y)` is its weight when `(X, Y) ∈ Q(c)`;
* a horizontal segment `[X0, X1] × {Y}` is `w · |[X0, X1] ∩ [c_x ± ½]| / (X1 − X0)` when `|Y − c_y| ≤ ½`
  (vertical segments likewise);
* a rectangle of density `ρ` is `ρ · |[X0, X1] ∩ [c_x ± ½]| · |[Y0, Y1] ∩ [c_y ± ½]|`.

On a box of centres in which the indicators are constant (the claimed points and lines are captured at
every centre of the box) and no breakpoint `X ± ½` of a claimed length lies strictly inside, each
length is affine (`clampL_affine`), so the lower bound `F(c)` is bilinear and its minimum over the box
is at a corner (`ge_of_interp`).  The kernel evaluates `F` at the four corners in integer arithmetic
(`axOk`).  This is Lemma Z without its usc/limit argument: the indicator is required on the whole
closed box, which a box tree arranges by cutting at the breakpoints.

`CovMP.of_ax`: an accepted leaf with the angle bin `[0, 0]` is covered.
-/

open MeasureTheory Finset
open scoped ENNReal

namespace SquarePacking

namespace ZMTreeM

open BoxTree

/-! ## 1.  Clamped lengths -/

/-- `|[A, B] ∩ [t − h, t + h]|`. -/
noncomputable def clampL (h A B t : ℝ) : ℝ := max 0 (min B (t + h) - max A (t - h))

lemma clampL_nonneg (h A B t : ℝ) : 0 ≤ clampL h A B t := le_max_left _ _

/-- Away from its four breakpoints a clamped length is affine. -/
lemma clampL_affine {h A B t0 t1 : ℝ}
    (b1 : A - h ≤ t0 ∨ t1 ≤ A - h) (b2 : A + h ≤ t0 ∨ t1 ≤ A + h)
    (b3 : B - h ≤ t0 ∨ t1 ≤ B - h) (b4 : B + h ≤ t0 ∨ t1 ≤ B + h) (hAB : A ≤ B) (hh : 0 ≤ h) :
    ∃ α β : ℝ, ∀ t, t0 ≤ t → t ≤ t1 → clampL h A B t = α + β * t := by
  rcases b3 with b3 | b3 <;> rcases b2 with b2 | b2
  · rcases b4 with b4 | b4
    · refine ⟨0, 0, fun t h0 h1 => ?_⟩
      simp only [clampL]
      rw [min_eq_left (show B ≤ t + h by linarith), max_eq_right (show A ≤ t - h by linarith),
        max_eq_left (show B - (t - h) ≤ 0 by linarith)]; ring
    · refine ⟨B + h, -1, fun t h0 h1 => ?_⟩
      simp only [clampL]
      rw [min_eq_left (show B ≤ t + h by linarith), max_eq_right (show A ≤ t - h by linarith),
        max_eq_right (show 0 ≤ B - (t - h) by linarith)]; ring
  · refine ⟨B - A, 0, fun t h0 h1 => ?_⟩
    simp only [clampL]
    rw [min_eq_left (show B ≤ t + h by linarith), max_eq_left (show t - h ≤ A by linarith),
      max_eq_right (show 0 ≤ B - A by linarith)]; ring
  · refine ⟨2 * h, 0, fun t h0 h1 => ?_⟩
    simp only [clampL]
    rw [min_eq_right (show t + h ≤ B by linarith), max_eq_right (show A ≤ t - h by linarith),
      max_eq_right (show 0 ≤ t + h - (t - h) by linarith)]; ring
  · rcases b1 with b1 | b1
    · refine ⟨h - A, 1, fun t h0 h1 => ?_⟩
      simp only [clampL]
      rw [min_eq_right (show t + h ≤ B by linarith), max_eq_left (show t - h ≤ A by linarith),
        max_eq_right (show 0 ≤ t + h - A by linarith)]; ring
    · refine ⟨0, 0, fun t h0 h1 => ?_⟩
      simp only [clampL]
      rw [min_eq_right (show t + h ≤ B by linarith), max_eq_left (show t - h ≤ A by linarith),
        max_eq_left (show t + h - A ≤ 0 by linarith)]; ring

/-- The clamped length in integer arithmetic. -/
def clampZ (h A B t : ℤ) : ℤ := max 0 (min B (t + h) - max A (t - h))

lemma clampZ_nonneg (h A B t : ℤ) : 0 ≤ clampZ h A B t := le_max_left _ _

lemma clampL_div (h A B t K : ℝ) (hK : 0 < K) :
    clampL (h / K) (A / K) (B / K) (t / K) = clampL h A B t / K := by
  simp only [clampL]
  rw [← add_div, ← sub_div, min_div_div_right hK.le, max_div_div_right hK.le, ← sub_div]
  rcases le_total 0 (min B (t + h) - max A (t - h)) with h0 | h0
  · rw [max_eq_right h0, max_eq_right (div_nonneg h0 hK.le)]
  · rw [max_eq_left h0, max_eq_left (div_nonpos_of_nonpos_of_nonneg h0 hK.le), zero_div]

lemma clampL_cast (h A B t : ℤ) : clampL h A B t = (clampZ h A B t : ℝ) := by
  simp only [clampL, clampZ]; push_cast; rfl

/-! ## 2.  Linear interpolation and the bilinear minimum -/

/-- `f` is the linear interpolation of its end values on `[t0, t1]` (multiplied out). -/
def Interp (t0 t1 : ℝ) (f : ℝ → ℝ) : Prop :=
  ∀ t, t0 ≤ t → t ≤ t1 → f t * (t1 - t0) = (t1 - t) * f t0 + (t - t0) * f t1

lemma interp_of_affine {t0 t1 : ℝ} {f : ℝ → ℝ} (h : ∃ α β : ℝ, ∀ t, t0 ≤ t → t ≤ t1 → f t = α + β * t)
    (h01 : t0 ≤ t1) : Interp t0 t1 f := by
  obtain ⟨α, β, hf⟩ := h
  intro t ht0 ht1
  rw [hf t ht0 ht1, hf t0 le_rfl h01, hf t1 h01 le_rfl]; ring

lemma interp_const (t0 t1 a : ℝ) : Interp t0 t1 (fun _ => a) := fun _ _ _ => by ring

lemma interp_add {t0 t1 : ℝ} {f g : ℝ → ℝ} (hf : Interp t0 t1 f) (hg : Interp t0 t1 g) :
    Interp t0 t1 (fun t => f t + g t) := fun t h0 h1 => by
  have a := hf t h0 h1; have b := hg t h0 h1; linear_combination a + b

lemma interp_mul {t0 t1 : ℝ} {f : ℝ → ℝ} (a : ℝ) (hf : Interp t0 t1 f) :
    Interp t0 t1 (fun t => a * f t) := fun t h0 h1 => by
  have b := hf t h0 h1; linear_combination a * b

lemma interp_sum {ι : Type*} {t0 t1 : ℝ} (L : List ι) (f : ι → ℝ → ℝ)
    (hf : ∀ i ∈ L, Interp t0 t1 (f i)) : Interp t0 t1 (fun t => (L.map fun i => f i t).sum) := by
  induction L with
  | nil => simpa using interp_const t0 t1 0
  | cons a L ih =>
    simp only [List.map_cons, List.sum_cons]
    exact interp_add (hf a List.mem_cons_self) (ih fun i hi => hf i (List.mem_cons_of_mem _ hi))

lemma ge_of_interp1 {t0 t1 W : ℝ} {f : ℝ → ℝ} (hf : Interp t0 t1 f) (h0 : W ≤ f t0) (h1 : W ≤ f t1)
    {t : ℝ} (ht0 : t0 ≤ t) (ht1 : t ≤ t1) : W ≤ f t := by
  rcases eq_or_lt_of_le (le_trans ht0 ht1) with e | hlt
  · have : t = t0 := le_antisymm (e ▸ ht1) ht0
    rw [this]; exact h0
  · have key := hf t ht0 ht1
    have : W * (t1 - t0) ≤ f t * (t1 - t0) := by
      rw [key]; nlinarith [mul_le_mul_of_nonneg_left h0 (sub_nonneg.mpr ht1),
        mul_le_mul_of_nonneg_left h1 (sub_nonneg.mpr ht0)]
    exact le_of_mul_le_mul_right this (sub_pos.mpr hlt)

/-- **The bilinear minimum**: separately interpolating in `x` and in `y`, `F` is at least its least
corner value on the box. -/
lemma ge_of_interp {x0 x1 y0 y1 W : ℝ} {F : ℝ → ℝ → ℝ}
    (hx : ∀ y, Interp x0 x1 (fun x => F x y)) (hy : ∀ x, Interp y0 y1 (fun y => F x y))
    (h00 : W ≤ F x0 y0) (h01 : W ≤ F x0 y1) (h10 : W ≤ F x1 y0) (h11 : W ≤ F x1 y1)
    {x y : ℝ} (hx0 : x0 ≤ x) (hx1 : x ≤ x1) (hy0 : y0 ≤ y) (hy1 : y ≤ y1) : W ≤ F x y :=
  ge_of_interp1 (hx y) (ge_of_interp1 (hy x0) h00 h01 hy0 hy1)
    (ge_of_interp1 (hy x1) h10 h11 hy0 hy1) hx0 hx1

/-! ## 3.  The mass at `θ = 0` -/

lemma sq_zero (c : ℝ × ℝ) :
    sq c 0 1 = Set.Icc (c.1 - 1 / 2) (c.1 + 1 / 2) ×ˢ Set.Icc (c.2 - 1 / 2) (c.2 + 1 / 2) := by
  ext p
  simp only [sq, coord, Real.cos_zero, Real.sin_zero, mul_one, mul_zero, add_zero, zero_add,
    Set.mem_ofPred_eq, Set.mem_prod, Set.mem_Icc, abs_le]
  constructor <;> rintro ⟨⟨a, b⟩, c', d⟩ <;> exact ⟨⟨by linarith, by linarith⟩, by linarith, by linarith⟩

/-- The rectangle mass at `θ = 0` is the product of the two clamped lengths. -/
lemma volume_sq_zero_inter_rect (D : ℕ) (c : ℝ × ℝ) (e : RectE) :
    (volume (sq c 0 1 ∩ rectSet D e)).toReal =
      clampL (1 / 2) ((e.1 : ℝ) / D) ((e.2.2.1 : ℝ) / D) c.1 *
        clampL (1 / 2) ((e.2.1 : ℝ) / D) ((e.2.2.2.1 : ℝ) / D) c.2 := by
  rw [sq_zero, rectSet, Set.prod_inter_prod, Set.Icc_inter_Icc, Set.Icc_inter_Icc,
    Measure.volume_eq_prod, Measure.prod_prod, Real.volume_Icc, Real.volume_Icc, ENNReal.toReal_mul,
    ENNReal.toReal_ofReal', ENNReal.toReal_ofReal', clampL, clampL]
  congr 1
  · rw [min_comm (c.1 + 1 / 2), max_comm (c.1 - 1 / 2), max_comm _ 0]
  · rw [min_comm (c.2 + 1 / 2), max_comm (c.2 - 1 / 2), max_comm _ 0]

/-! ## 4.  The `AXIS` leaf -/

/-- The value of `F` at a centre (weights not divided by `W`): claimed points, horizontal and vertical
segments (their captured fraction times their weight), rectangles (density times area). -/
noncomputable def axF (D : ℕ) (cps : List (ℕ × ℕ × ℕ)) (chs cvs : List SegE) (crs : List RectE)
    (x y : ℝ) : ℝ :=
  (cps.map fun p => (p.2.2 : ℝ)).sum
    + (chs.map fun e => (e.2.2.2.2 : ℝ) * clampL (1 / 2) ((e.1 : ℝ) / D) ((e.2.2.1 : ℝ) / D) x /
        ((e.2.2.1 : ℝ) / D - (e.1 : ℝ) / D)).sum
    + (cvs.map fun e => (e.2.2.2.2 : ℝ) * clampL (1 / 2) ((e.2.1 : ℝ) / D) ((e.2.2.2.1 : ℝ) / D) y /
        ((e.2.2.2.1 : ℝ) / D - (e.2.1 : ℝ) / D)).sum
    + (crs.map fun r => (r.2.2.2.2 : ℝ) * (clampL (1 / 2) ((r.1 : ℝ) / D) ((r.2.2.1 : ℝ) / D) x *
        clampL (1 / 2) ((r.2.1 : ℝ) / D) ((r.2.2.2.1 : ℝ) / D) y)).sum

/-- The kernel's value of `F` at the corner `(x, y)/(D S)`, times `4 D² S² Lc`. -/
def axVal (D S Lc : ℕ) (cps : List (ℕ × ℕ × ℕ)) (chs cvs : List SegE) (crs : List RectE)
    (x y : ℕ) : ℤ :=
  (cps.map fun p => (p.2.2 : ℤ) * (4 * D * D * S * S * Lc : ℕ)).sum
    + (chs.map fun e => (e.2.2.2.2 : ℤ) *
        clampZ (D * S : ℕ) (2 * e.1 * S : ℕ) (2 * e.2.2.1 * S : ℕ) (2 * x : ℕ) *
        (2 * D * D * S * (Lc / (e.2.2.1 - e.1)) : ℕ)).sum
    + (cvs.map fun e => (e.2.2.2.2 : ℤ) *
        clampZ (D * S : ℕ) (2 * e.2.1 * S : ℕ) (2 * e.2.2.2.1 * S : ℕ) (2 * y : ℕ) *
        (2 * D * D * S * (Lc / (e.2.2.2.1 - e.2.1)) : ℕ)).sum
    + (crs.map fun r => (r.2.2.2.2 : ℤ) *
        (clampZ (D * S : ℕ) (2 * r.1 * S : ℕ) (2 * r.2.2.1 * S : ℕ) (2 * x : ℕ) *
          clampZ (D * S : ℕ) (2 * r.2.1 * S : ℕ) (2 * r.2.2.2.1 * S : ℕ) (2 * y : ℕ)) * (Lc : ℤ)).sum

/-- A coordinate `X/D` is within `½` of every centre coordinate in `[x0, x1]/(D S)`. -/
def capX (D S x0 x1 X : ℕ) : Bool :=
  Nat.ble (2 * X * S) (2 * x0 + D * S) && Nat.ble (2 * x1) (2 * X * S + D * S)

/-- No breakpoint `A/D ± ½`, `B/D ± ½` lies strictly inside `(x0, x1)/(D S)` (all over `2 D S`). -/
def bpOk (D S x0 x1 A B : ℕ) : Bool :=
  ([(2 * A * S : ℤ) - D * S, (2 * A * S : ℤ) + D * S, (2 * B * S : ℤ) - D * S,
    (2 * B * S : ℤ) + D * S]).all fun b => decide (b ≤ 2 * x0) || decide ((2 * x1 : ℤ) ≤ b)

/-- **The `AXIS` leaf test.** -/
def axOk (D S W Lc x0 x1 y0 y1 : ℕ) (pts : List (ℕ × ℕ × ℕ)) (segs : List SegE)
    (rects : List RectE) (cps : List (ℕ × ℕ × ℕ)) (chs cvs : List SegE) (crs : List RectE) : Bool :=
  Nat.blt 0 Lc && Nat.ble x0 x1 && Nat.ble y0 y1 && decide cps.Nodup &&
    cps.all (fun p => pts.contains p && capX D S x0 x1 p.1 && capX D S y0 y1 p.2.1) &&
    decide (chs ++ cvs).Nodup &&
    chs.all (fun e => segs.contains e && e.2.1 == e.2.2.2.1 && Nat.blt e.1 e.2.2.1 &&
      Lc % (e.2.2.1 - e.1) == 0 && capX D S y0 y1 e.2.1 && bpOk D S x0 x1 e.1 e.2.2.1) &&
    cvs.all (fun e => segs.contains e && e.1 == e.2.2.1 && Nat.blt e.2.1 e.2.2.2.1 &&
      Lc % (e.2.2.2.1 - e.2.1) == 0 && capX D S x0 x1 e.1 && bpOk D S y0 y1 e.2.1 e.2.2.2.1) &&
    decide crs.Nodup &&
    crs.all (fun r => rects.contains r && Nat.ble r.1 r.2.2.1 && Nat.ble r.2.1 r.2.2.2.1 &&
      bpOk D S x0 x1 r.1 r.2.2.1 && bpOk D S y0 y1 r.2.1 r.2.2.2.1) &&
    [(x0, y0), (x0, y1), (x1, y0), (x1, y1)].all fun q =>
      decide (((W * (4 * D * D * S * S * Lc) : ℕ) : ℤ) ≤ axVal D S Lc cps chs cvs crs q.1 q.2)

/-! ### Real-number facts from the tests -/

lemma capX_sound {D S x0 x1 X : ℕ} (hD : 0 < D) (hS : 0 < S) (h : capX D S x0 x1 X = true)
    {t : ℝ} (h0 : (x0 : ℝ) / (D * S) ≤ t) (h1 : t ≤ (x1 : ℝ) / (D * S)) : |(X : ℝ) / D - t| ≤ 1 / 2 := by
  simp only [capX, Bool.and_eq_true, Nat.ble_eq] at h
  have hDr : (0 : ℝ) < D := by exact_mod_cast hD
  have hSr : (0 : ℝ) < S := by exact_mod_cast hS
  have a : ((2 * X * S : ℕ) : ℝ) ≤ ((2 * x0 + D * S : ℕ) : ℝ) := by exact_mod_cast h.1
  have b : ((2 * x1 : ℕ) : ℝ) ≤ ((2 * X * S + D * S : ℕ) : ℝ) := by exact_mod_cast h.2
  push_cast at a b
  rw [div_le_iff₀ (by positivity)] at h0
  rw [le_div_iff₀ (by positivity)] at h1
  have e : (X : ℝ) / D - t = (X * S - t * (D * S)) / (D * S) := by field_simp
  rw [e, abs_div, abs_of_pos (by positivity : (0 : ℝ) < D * S), div_le_iff₀ (by positivity), abs_le]
  constructor <;> nlinarith

lemma bpOk_sound {D S x0 x1 A B : ℕ} (hD : 0 < D) (hS : 0 < S) (h : bpOk D S x0 x1 A B = true) :
    let t0 := (x0 : ℝ) / (D * S); let t1 := (x1 : ℝ) / (D * S)
    ((A : ℝ) / D - 1 / 2 ≤ t0 ∨ t1 ≤ (A : ℝ) / D - 1 / 2) ∧
      ((A : ℝ) / D + 1 / 2 ≤ t0 ∨ t1 ≤ (A : ℝ) / D + 1 / 2) ∧
      ((B : ℝ) / D - 1 / 2 ≤ t0 ∨ t1 ≤ (B : ℝ) / D - 1 / 2) ∧
      ((B : ℝ) / D + 1 / 2 ≤ t0 ∨ t1 ≤ (B : ℝ) / D + 1 / 2) := by
  intro t0 t1
  simp only [bpOk, List.all_cons, List.all_nil, Bool.and_true, Bool.and_eq_true, Bool.or_eq_true,
    decide_eq_true_eq] at h
  have hK : (0 : ℝ) < 2 * D * S := by positivity
  have conv : ∀ (b : ℤ) (s : ℝ), (b : ℝ) / (2 * D * S) = s →
      ((b ≤ 2 * x0 ∨ (2 * x1 : ℤ) ≤ b) → (s ≤ t0 ∨ t1 ≤ s)) := by
    intro b s hs hb
    have e0 : t0 = ((2 * x0 : ℤ) : ℝ) / (2 * D * S) := by
      simp only [t0]; push_cast; field_simp
    have e1 : t1 = ((2 * x1 : ℤ) : ℝ) / (2 * D * S) := by
      simp only [t1]; push_cast; field_simp
    rw [← hs, e0, e1]
    rcases hb with hb | hb
    · left; exact div_le_div_of_nonneg_right (by exact_mod_cast hb) hK.le
    · right; exact div_le_div_of_nonneg_right (by exact_mod_cast hb) hK.le
  obtain ⟨h1, h2, h3, h4⟩ := h
  refine ⟨conv _ _ ?_ h1, conv _ _ ?_ h2, conv _ _ ?_ h3, conv _ _ ?_ h4⟩ <;>
    · push_cast; field_simp

lemma clampL_grid {D S : ℕ} (hD : 0 < D) (hS : 0 < S) (A B x : ℕ) :
    clampL (1 / 2) ((A : ℝ) / D) ((B : ℝ) / D) ((x : ℝ) / (D * S)) =
      (clampZ (D * S : ℕ) (2 * A * S : ℕ) (2 * B * S : ℕ) (2 * x : ℕ) : ℝ) / (2 * D * S) := by
  have hK : (0 : ℝ) < 2 * D * S := by positivity
  have hD' : (D : ℝ) ≠ 0 := by positivity
  have hS' : (S : ℝ) ≠ 0 := by positivity
  rw [show (1 / 2 : ℝ) = (((D * S : ℕ) : ℤ) : ℝ) / (2 * D * S) by push_cast; field_simp,
    show (A : ℝ) / D = (((2 * A * S : ℕ) : ℤ) : ℝ) / (2 * D * S) by push_cast; field_simp,
    show (B : ℝ) / D = (((2 * B * S : ℕ) : ℤ) : ℝ) / (2 * D * S) by push_cast; field_simp,
    show (x : ℝ) / (D * S) = (((2 * x : ℕ) : ℤ) : ℝ) / (2 * D * S) by push_cast; field_simp,
    clampL_div _ _ _ _ _ hK, clampL_cast]

/-! ### The corner values -/

lemma list_sum_mul_eq {ι : Type*} (L : List ι) (f : ι → ℝ) (g : ι → ℤ) (K : ℝ)
    (h : ∀ i ∈ L, f i * K = g i) : (L.map f).sum * K = (((L.map g).sum : ℤ) : ℝ) := by
  induction L with
  | nil => simp
  | cons a L ih =>
    simp only [List.map_cons, List.sum_cons, Int.cast_add]
    rw [add_mul, h a List.mem_cons_self, ih fun i hi => h i (List.mem_cons_of_mem _ hi)]

lemma seg_term {D S Lc A B w x : ℕ} (hD : 0 < D) (hS : 0 < S) (hAB : A < B) (hL : Lc % (B - A) = 0) :
    (w : ℝ) * clampL (1 / 2) ((A : ℝ) / D) ((B : ℝ) / D) ((x : ℝ) / (D * S)) /
        ((B : ℝ) / D - (A : ℝ) / D) * ((4 * D * D * S * S * Lc : ℕ) : ℝ) =
      (((w : ℤ) * clampZ (D * S : ℕ) (2 * A * S : ℕ) (2 * B * S : ℕ) (2 * x : ℕ) *
        (2 * D * D * S * (Lc / (B - A)) : ℕ) : ℤ) : ℝ) := by
  rw [clampL_grid hD hS]
  have hdvd : (B - A) ∣ Lc := Nat.dvd_of_mod_eq_zero hL
  set q := Lc / (B - A) with hq
  have hLc : (Lc : ℝ) = q * ((B : ℝ) - A) := by
    have : Lc = q * (B - A) := (Nat.div_mul_cancel hdvd).symm
    rw [this, Nat.cast_mul, Nat.cast_sub hAB.le]
  have hBA : (0 : ℝ) < (B : ℝ) - A := by
    have : (A : ℝ) < B := by exact_mod_cast hAB
    linarith
  have hDr : (0 : ℝ) < D := by exact_mod_cast hD
  have hSr : (0 : ℝ) < S := by exact_mod_cast hS
  push_cast
  rw [hLc, div_sub_div_same]
  field_simp
  ring

lemma corner_eq {D S Lc : ℕ} (hD : 0 < D) (hS : 0 < S) (cps : List (ℕ × ℕ × ℕ)) (chs cvs : List SegE)
    (crs : List RectE)
    (hh : ∀ e ∈ chs, e.1 < e.2.2.1 ∧ Lc % (e.2.2.1 - e.1) = 0)
    (hv : ∀ e ∈ cvs, e.2.1 < e.2.2.2.1 ∧ Lc % (e.2.2.2.1 - e.2.1) = 0) (x y : ℕ) :
    axF D cps chs cvs crs ((x : ℝ) / (D * S)) ((y : ℝ) / (D * S)) * ((4 * D * D * S * S * Lc : ℕ) : ℝ) =
      (axVal D S Lc cps chs cvs crs x y : ℝ) := by
  have hDr : (0 : ℝ) < D := by exact_mod_cast hD
  have hSr : (0 : ℝ) < S := by exact_mod_cast hS
  simp only [axF, axVal, add_mul, Int.cast_add]
  rw [list_sum_mul_eq cps _ (fun p => (p.2.2 : ℤ) * (4 * D * D * S * S * Lc : ℕ)) _
      fun p _ => by push_cast; ring,
    list_sum_mul_eq chs _ (fun e => (e.2.2.2.2 : ℤ) *
        clampZ (D * S : ℕ) (2 * e.1 * S : ℕ) (2 * e.2.2.1 * S : ℕ) (2 * x : ℕ) *
        (2 * D * D * S * (Lc / (e.2.2.1 - e.1)) : ℕ)) _
      fun e he => seg_term hD hS (hh e he).1 (hh e he).2,
    list_sum_mul_eq cvs _ (fun e => (e.2.2.2.2 : ℤ) *
        clampZ (D * S : ℕ) (2 * e.2.1 * S : ℕ) (2 * e.2.2.2.1 * S : ℕ) (2 * y : ℕ) *
        (2 * D * D * S * (Lc / (e.2.2.2.1 - e.2.1)) : ℕ)) _
      fun e he => seg_term hD hS (hv e he).1 (hv e he).2,
    list_sum_mul_eq crs _ (fun r => (r.2.2.2.2 : ℤ) *
        (clampZ (D * S : ℕ) (2 * r.1 * S : ℕ) (2 * r.2.2.1 * S : ℕ) (2 * x : ℕ) *
          clampZ (D * S : ℕ) (2 * r.2.1 * S : ℕ) (2 * r.2.2.2.1 * S : ℕ) (2 * y : ℕ)) * (Lc : ℤ)) _
      fun r _ => by rw [clampL_grid hD hS, clampL_grid hD hS]; push_cast; field_simp; ring]

/-! ### The mass at `θ = 0` is at least `F` -/

/-- The part of a segment `[A, B]` of its line inside `[t − ½, t + ½]`, clipped into `[A, B]`. -/
noncomputable def plo (A B t : ℝ) : ℝ := min B (max A (t - 1 / 2))
noncomputable def phi (A B t : ℝ) : ℝ := max (plo A B t) (min B (t + 1 / 2))

lemma phi_sub_plo (A B t : ℝ) : phi A B t - plo A B t = clampL (1 / 2) A B t := by
  simp only [phi, plo, clampL]
  rcases le_total (max A (t - 1 / 2)) B with h | h
  · rw [min_eq_right h, ← max_sub_sub_right, sub_self]
  · rw [min_eq_left h, max_eq_left (min_le_left _ _), sub_self,
      max_eq_left (by linarith [min_le_left B (t + 1 / 2)] : min B (t + 1 / 2) - max A (t - 1 / 2) ≤ 0)]

lemma plo_props {A B t : ℝ} (hAB : A ≤ B) :
    A ≤ plo A B t ∧ plo A B t ≤ phi A B t ∧ phi A B t ≤ B ∧
      ∀ s, plo A B t < s → s < phi A B t → t - 1 / 2 ≤ s ∧ s ≤ t + 1 / 2 := by
  refine ⟨le_min hAB (le_max_left _ _), le_max_left _ _, max_le (min_le_left _ _) (min_le_left _ _),
    fun s h1 h2 => ?_⟩
  simp only [phi, plo] at h1 h2
  rcases le_total (max A (t - 1 / 2)) B with h | h
  · rw [min_eq_right h] at h1 h2
    rcases le_total (max A (t - 1 / 2)) (min B (t + 1 / 2)) with h' | h'
    · rw [max_eq_right h'] at h2
      exact ⟨by linarith [le_max_right A (t - 1 / 2)], by linarith [min_le_right B (t + 1 / 2)]⟩
    · rw [max_eq_left h'] at h2; linarith
  · rw [min_eq_left h, max_eq_left (min_le_left _ _)] at h2
    rw [min_eq_left h] at h1; linarith

/-- **The mass at `θ = 0` is at least `F`.** -/
theorem axF_le_mass {D : ℕ} (hD : 0 < D) {pts : List (ℕ × ℕ × ℕ)} {segs : List SegE}
    {rects : List RectE} {cps : List (ℕ × ℕ × ℕ)} {chs cvs : List SegE} {crs : List RectE}
    (c : ℝ × ℝ) (hcp : cps.Nodup)
    (hcps : ∀ p ∈ cps, p ∈ pts ∧ |(p.1 : ℝ) / D - c.1| ≤ 1 / 2 ∧ |(p.2.1 : ℝ) / D - c.2| ≤ 1 / 2)
    (hsnd : (chs ++ cvs).Nodup)
    (hch : ∀ e ∈ chs, e ∈ segs ∧ e.2.1 = e.2.2.2.1 ∧ e.1 < e.2.2.1 ∧ |(e.2.1 : ℝ) / D - c.2| ≤ 1 / 2)
    (hcv : ∀ e ∈ cvs, e ∈ segs ∧ e.1 = e.2.2.1 ∧ e.2.1 < e.2.2.2.1 ∧ |(e.1 : ℝ) / D - c.1| ≤ 1 / 2)
    (hcr : crs.Nodup) (hcrs : ∀ r ∈ crs, r ∈ rects) :
    axF D cps chs cvs crs c.1 c.2 ≤
      ptMass D pts (sq c 0 1) + segMass D segs (sq c 0 1) + rectMass D rects (sq c 0 1) := by
  classical
  have hDr : (0 : ℝ) < D := by exact_mod_cast hD
  -- points
  have P : (cps.map fun p => (p.2.2 : ℝ)).sum ≤ ptMass D pts (sq c 0 1) := by
    rw [ptMass, ← List.sum_toFinset _ hcp]
    refine Finset.sum_le_sum_of_subset_of_nonneg (fun p hp => ?_) fun _ _ _ => Nat.cast_nonneg _
    obtain ⟨hm, h1, h2⟩ := hcps p (List.mem_toFinset.mp hp)
    rw [abs_le] at h1 h2
    refine Finset.mem_filter.mpr ⟨List.mem_toFinset.mpr hm, ?_⟩
    rw [sq_zero]
    exact ⟨⟨by simp only [ptR]; linarith, by simp only [ptR]; linarith⟩,
      by simp only [ptR]; linarith, by simp only [ptR]; linarith⟩
  -- segments, as parts
  set hpart : SegE → SegE × ℝ × ℝ := fun e =>
    (e, plo ((e.1 : ℝ) / D) ((e.2.2.1 : ℝ) / D) c.1, phi ((e.1 : ℝ) / D) ((e.2.2.1 : ℝ) / D) c.1)
  set vpart : SegE → SegE × ℝ × ℝ := fun e =>
    (e, plo ((e.2.1 : ℝ) / D) ((e.2.2.2.1 : ℝ) / D) c.2,
      phi ((e.2.1 : ℝ) / D) ((e.2.2.2.1 : ℝ) / D) c.2)
  set parts := chs.map hpart ++ cvs.map vpart with hparts
  have hfst : parts.map Prod.fst = chs ++ cvs := by
    simp only [hparts, List.map_append, List.map_map]
    congr 1
    · rw [show Prod.fst ∘ hpart = id from rfl, List.map_id]
    · rw [show Prod.fst ∘ vpart = id from rfl, List.map_id]
  have hpw : parts.Pairwise (fun p q => p.1 = q.1 → p.2.2 ≤ q.2.1) := by
    have h := hsnd
    rw [← hfst, List.Nodup, List.pairwise_map] at h
    exact h.imp fun hne heq => absurd heq hne
  have hmem : ∀ p ∈ parts, p.1 ∈ segs.toFinset := by
    intro p hp
    rcases List.mem_append.mp hp with h | h
    · obtain ⟨e, he, rfl⟩ := List.mem_map.mp h; exact List.mem_toFinset.mpr (hch e he).1
    · obtain ⟨e, he, rfl⟩ := List.mem_map.mp h; exact List.mem_toFinset.mpr (hcv e he).1
  have hok : ∀ p ∈ parts, PartOK D (sq c 0 1) p := by
    intro p hp
    rcases List.mem_append.mp hp with h | h
    · obtain ⟨e, he, rfl⟩ := List.mem_map.mp h
      obtain ⟨_, hy, hx, hc⟩ := hch e he
      have hne : e.1 ≠ e.2.2.1 := ne_of_lt hx
      have hAB : (e.1 : ℝ) / D ≤ (e.2.2.1 : ℝ) / D :=
        div_le_div_of_nonneg_right (by exact_mod_cast hx.le) hDr.le
      obtain ⟨p1, p2, p3, p4⟩ := plo_props (t := c.1) hAB
      rw [abs_le] at hc
      refine ⟨Or.inr ⟨hy, hx⟩, ?_, p2, ?_, fun s hs1 hs2 => ?_⟩
      · simp only [hpart, elo, hne, if_false]; exact p1
      · simp only [hpart, ehi, hne, if_false]; exact p3
      · obtain ⟨q1, q2⟩ := p4 s hs1 hs2
        show lpE D e s ∈ sq c 0 1
        rw [lpE, if_neg hne, sq_zero]
        exact ⟨⟨by linarith, by linarith⟩, by linarith, by linarith⟩
    · obtain ⟨e, he, rfl⟩ := List.mem_map.mp h
      obtain ⟨_, hx, hy, hc⟩ := hcv e he
      have hAB : (e.2.1 : ℝ) / D ≤ (e.2.2.2.1 : ℝ) / D :=
        div_le_div_of_nonneg_right (by exact_mod_cast hy.le) hDr.le
      obtain ⟨p1, p2, p3, p4⟩ := plo_props (t := c.2) hAB
      rw [abs_le] at hc
      refine ⟨Or.inl ⟨hx, hy⟩, ?_, p2, ?_, fun s hs1 hs2 => ?_⟩
      · simp only [vpart, elo, hx, if_true]; exact p1
      · simp only [vpart, ehi, hx, if_true]; exact p3
      · obtain ⟨q1, q2⟩ := p4 s hs1 hs2
        show lpE D e s ∈ sq c 0 1
        rw [lpE, if_pos hx, sq_zero]
        exact ⟨⟨by linarith, by linarith⟩, by linarith, by linarith⟩
  have Sg := parts_le_segMass hD segs (sq c 0 1) parts hmem hok hpw
  have hsum : (parts.map (pval D)).sum =
      (chs.map fun e => (e.2.2.2.2 : ℝ) * clampL (1 / 2) ((e.1 : ℝ) / D) ((e.2.2.1 : ℝ) / D) c.1 /
        ((e.2.2.1 : ℝ) / D - (e.1 : ℝ) / D)).sum
      + (cvs.map fun e => (e.2.2.2.2 : ℝ) * clampL (1 / 2) ((e.2.1 : ℝ) / D) ((e.2.2.2.1 : ℝ) / D) c.2 /
        ((e.2.2.2.1 : ℝ) / D - (e.2.1 : ℝ) / D)).sum := by
    rw [hparts, List.map_append, List.sum_append, List.map_map, List.map_map]
    congr 1
    · congr 1
      refine List.map_congr_left fun e he => ?_
      have hne : e.1 ≠ e.2.2.1 := ne_of_lt (hch e he).2.2.1
      simp only [Function.comp, hpart, pval, elo, ehi, hne, if_false, phi_sub_plo]
    · congr 1
      refine List.map_congr_left fun e he => ?_
      have hx : e.1 = e.2.2.1 := (hcv e he).2.1
      simp only [Function.comp, vpart, pval, elo, ehi, hx, if_true, phi_sub_plo]
  -- rectangles
  have Rc : (crs.map fun r => (r.2.2.2.2 : ℝ) * (clampL (1 / 2) ((r.1 : ℝ) / D) ((r.2.2.1 : ℝ) / D) c.1 *
      clampL (1 / 2) ((r.2.1 : ℝ) / D) ((r.2.2.2.1 : ℝ) / D) c.2)).sum ≤ rectMass D rects (sq c 0 1) := by
    rw [rectMass, ← List.sum_toFinset _ hcr]
    refine le_trans (le_of_eq (Finset.sum_congr rfl fun r _ => ?_))
      (Finset.sum_le_sum_of_subset_of_nonneg (fun r hr => List.mem_toFinset.mpr
        (hcrs r (List.mem_toFinset.mp hr))) fun _ _ _ =>
          mul_nonneg (Nat.cast_nonneg _) ENNReal.toReal_nonneg)
    rw [volume_sq_zero_inter_rect]
  simp only [axF]
  linarith

/-! ### Soundness of the `AXIS` leaf -/

lemma affine_div {t0 t1 a b : ℝ} {f : ℝ → ℝ}
    (h : ∃ α β : ℝ, ∀ t, t0 ≤ t → t ≤ t1 → f t = α + β * t) :
    ∃ α β : ℝ, ∀ t, t0 ≤ t → t ≤ t1 → a * f t / b = α + β * t := by
  obtain ⟨α, β, hf⟩ := h
  exact ⟨a * α / b, a * β / b, fun t h0 h1 => by rw [hf t h0 h1]; ring⟩

lemma affine_mul_right {t0 t1 a k : ℝ} {f : ℝ → ℝ}
    (h : ∃ α β : ℝ, ∀ t, t0 ≤ t → t ≤ t1 → f t = α + β * t) :
    ∃ α β : ℝ, ∀ t, t0 ≤ t → t ≤ t1 → a * (f t * k) = α + β * t := by
  obtain ⟨α, β, hf⟩ := h
  exact ⟨a * α * k, a * β * k, fun t h0 h1 => by rw [hf t h0 h1]; ring⟩

lemma affine_mul_left {t0 t1 a k : ℝ} {f : ℝ → ℝ}
    (h : ∃ α β : ℝ, ∀ t, t0 ≤ t → t ≤ t1 → f t = α + β * t) :
    ∃ α β : ℝ, ∀ t, t0 ≤ t → t ≤ t1 → a * (k * f t) = α + β * t := by
  obtain ⟨α, β, hf⟩ := h
  exact ⟨a * k * α, a * k * β, fun t h0 h1 => by rw [hf t h0 h1]; ring⟩

/-- The clamped length of a claimed interval is affine on the box side. -/
lemma clampL_affine_box {D S x0 x1 A B : ℕ} (hD : 0 < D) (hS : 0 < S) (hAB : A ≤ B)
    (h : bpOk D S x0 x1 A B = true) :
    ∃ α β : ℝ, ∀ t, (x0 : ℝ) / (D * S) ≤ t → t ≤ (x1 : ℝ) / (D * S) →
      clampL (1 / 2) ((A : ℝ) / D) ((B : ℝ) / D) t = α + β * t := by
  have hDr : (0 : ℝ) < D := by exact_mod_cast hD
  obtain ⟨b1, b2, b3, b4⟩ := bpOk_sound hD hS h
  exact clampL_affine b1 b2 b3 b4 (div_le_div_of_nonneg_right (by exact_mod_cast hAB) hDr.le)
    (by norm_num)

/-- **Soundness of the `AXIS` leaf** (Lemma Z on a box, angle bin `[0, 0]`). -/
theorem CovMP.of_ax {D S Mq R W Lc x0 x1 y0 y1 : ℕ} {pts : List (ℕ × ℕ × ℕ)} {segs : List SegE}
    {rects : List RectE} {cps : List (ℕ × ℕ × ℕ)} {chs cvs : List SegE} {crs : List RectE}
    (hD : 0 < D) (hS : 0 < S)
    (h : axOk D S W Lc x0 x1 y0 y1 pts segs rects cps chs cvs crs = true) :
    CovMP D S Mq R W pts segs rects x0 x1 y0 y1 0 0 := by
  simp only [axOk, Bool.and_eq_true, Nat.blt_eq, Nat.ble_eq, decide_eq_true_eq, List.all_eq_true,
    beq_iff_eq, List.contains_iff_mem, List.mem_cons, List.not_mem_nil, or_false,
    forall_eq_or_imp, forall_eq] at h
  obtain ⟨⟨⟨⟨⟨⟨⟨⟨⟨⟨hLc, hx01⟩, hy01⟩, hcp⟩, hcps⟩, hsnd⟩, hch⟩, hcv⟩, hcr⟩, hcrs⟩, hcorn⟩ := h
  intro c u hx0 hx1 hy0 hy1 hu0 hu1 _
  have hu : u = 0 := by
    simp only [Nat.cast_zero, zero_div] at hu0 hu1; linarith
  subst hu
  rw [Real.arctan_zero, mul_zero]
  have hDr : (0 : ℝ) < D := by exact_mod_cast hD
  have hSr : (0 : ℝ) < S := by exact_mod_cast hS
  -- the mass is at least `F`
  have hF := axF_le_mass (pts := pts) (segs := segs) (rects := rects) hD c hcp
    (fun p hp => by
      obtain ⟨⟨hm, h1⟩, h2⟩ := hcps p hp
      exact ⟨hm, capX_sound hD hS h1 hx0 hx1, capX_sound hD hS h2 hy0 hy1⟩)
    hsnd
    (fun e he => by
      obtain ⟨⟨⟨⟨⟨hm, hy⟩, hx⟩, _⟩, hc⟩, _⟩ := hch e he
      exact ⟨hm, hy, hx, capX_sound hD hS hc hy0 hy1⟩)
    (fun e he => by
      obtain ⟨⟨⟨⟨⟨hm, hx⟩, hy⟩, _⟩, hc⟩, _⟩ := hcv e he
      exact ⟨hm, hx, hy, capX_sound hD hS hc hx0 hx1⟩)
    hcr (fun r hr => (hcrs r hr).1.1.1.1)
  -- `F` interpolates in each variable
  have hx01r : (x0 : ℝ) / (D * S) ≤ (x1 : ℝ) / (D * S) :=
    div_le_div_of_nonneg_right (by exact_mod_cast hx01) (by positivity)
  have hy01r : (y0 : ℝ) / (D * S) ≤ (y1 : ℝ) / (D * S) :=
    div_le_div_of_nonneg_right (by exact_mod_cast hy01) (by positivity)
  have hIx : ∀ y, Interp ((x0 : ℝ) / (D * S)) ((x1 : ℝ) / (D * S))
      (fun x => axF D cps chs cvs crs x y) := by
    intro y
    simp only [axF]
    refine interp_add (interp_add (interp_add (interp_const _ _ _) ?_) (interp_const _ _ _)) ?_
    · refine interp_sum _ _ fun e he => interp_of_affine (affine_div ?_) hx01r
      obtain ⟨⟨⟨⟨⟨_, _⟩, hx⟩, _⟩, _⟩, hb⟩ := hch e he
      exact clampL_affine_box hD hS hx.le hb
    · refine interp_sum _ _ fun r hr => interp_of_affine (affine_mul_right ?_) hx01r
      obtain ⟨⟨⟨⟨_, h1⟩, _⟩, hb⟩, _⟩ := hcrs r hr
      exact clampL_affine_box hD hS h1 hb
  have hIy : ∀ x, Interp ((y0 : ℝ) / (D * S)) ((y1 : ℝ) / (D * S))
      (fun y => axF D cps chs cvs crs x y) := by
    intro x
    simp only [axF]
    refine interp_add (interp_add (interp_add (interp_const _ _ _) (interp_const _ _ _)) ?_) ?_
    · refine interp_sum _ _ fun e he => interp_of_affine (affine_div ?_) hy01r
      obtain ⟨⟨⟨⟨⟨_, _⟩, hy⟩, _⟩, _⟩, hb⟩ := hcv e he
      exact clampL_affine_box hD hS hy.le hb
    · refine interp_sum _ _ fun r hr => interp_of_affine (affine_mul_left ?_) hy01r
      obtain ⟨⟨⟨⟨_, _⟩, h2⟩, _⟩, hb⟩ := hcrs r hr
      exact clampL_affine_box hD hS h2 hb
  -- the four corners
  have hK : (0 : ℝ) < ((4 * D * D * S * S * Lc : ℕ) : ℝ) := by
    have : 0 < 4 * D * D * S * S * Lc := by positivity
    exact_mod_cast this
  have hhv : ∀ e ∈ chs, e.1 < e.2.2.1 ∧ Lc % (e.2.2.1 - e.1) = 0 := fun e he => by
    obtain ⟨⟨⟨⟨⟨_, _⟩, hx⟩, hL⟩, _⟩, _⟩ := hch e he; exact ⟨hx, hL⟩
  have hvv : ∀ e ∈ cvs, e.2.1 < e.2.2.2.1 ∧ Lc % (e.2.2.2.1 - e.2.1) = 0 := fun e he => by
    obtain ⟨⟨⟨⟨⟨_, _⟩, hy⟩, hL⟩, _⟩, _⟩ := hcv e he; exact ⟨hy, hL⟩
  have corner : ∀ x y : ℕ, ((W * (4 * D * D * S * S * Lc) : ℕ) : ℤ) ≤ axVal D S Lc cps chs cvs crs x y →
      (W : ℝ) ≤ axF D cps chs cvs crs ((x : ℝ) / (D * S)) ((y : ℝ) / (D * S)) := by
    intro x y hxy
    have h1 := corner_eq hD hS cps chs cvs crs hhv hvv x y
    have h2 : (((W * (4 * D * D * S * S * Lc) : ℕ) : ℤ) : ℝ) ≤ (axVal D S Lc cps chs cvs crs x y : ℝ) := by
      exact_mod_cast hxy
    rw [← h1] at h2
    push_cast at h2
    have h3 : (W : ℝ) * ((4 * D * D * S * S * Lc : ℕ) : ℝ) ≤
        axF D cps chs cvs crs ((x : ℝ) / (D * S)) ((y : ℝ) / (D * S)) * ((4 * D * D * S * S * Lc : ℕ) : ℝ) := by
      push_cast; linarith
    exact le_of_mul_le_mul_right h3 hK
  obtain ⟨c00, c01, c10, c11⟩ := hcorn
  have hW := ge_of_interp hIx hIy (corner _ _ c00) (corner _ _ c01) (corner _ _ c10) (corner _ _ c11)
    hx0 hx1 hy0 hy1
  linarith

/-- At `θ = 0` an admissible centre is at least `½` from the walls `x = 0`, `y = 0`. -/
lemma half_le_of_sq_zero {c : ℝ × ℝ} {m : ℝ} (h : sq c 0 1 ⊆ box m) : 1 / 2 ≤ c.1 ∧ 1 / 2 ≤ c.2 := by
  have h1 := h (show (c.1 - 1 / 2, c.2) ∈ sq c 0 1 by
    rw [sq_zero]; exact ⟨⟨le_rfl, by linarith⟩, by linarith, by linarith⟩)
  have h2 := h (show (c.1, c.2 - 1 / 2) ∈ sq c 0 1 by
    rw [sq_zero]; exact ⟨⟨by linarith, by linarith⟩, le_rfl, by linarith⟩)
  exact ⟨by linarith [h1.1], by linarith [h2.2.2.1]⟩

/-- At `θ = 0`, a box of centres left of `x = ½` is covered by its right edge. -/
theorem CovMP.ax_clipX {D S Mq R W x0 x1 y0 y1 : ℕ} {pts : List (ℕ × ℕ × ℕ)} {segs : List SegE}
    {rects : List RectE} (hD : 0 < D) (hS : 0 < S) (h2 : 2 * x1 ≤ D * S)
    (h : CovMP D S Mq R W pts segs rects x1 x1 y0 y1 0 0) :
    CovMP D S Mq R W pts segs rects x0 x1 y0 y1 0 0 := by
  intro c u _ hx1 hy0 hy1 hu0 hu1 hbox
  have hu : u = 0 := by simp only [Nat.cast_zero, zero_div] at hu0 hu1; linarith
  subst hu
  rw [Real.arctan_zero, mul_zero] at hbox ⊢
  have hc := (half_le_of_sq_zero hbox).1
  have hx : (x1 : ℝ) / (D * S) ≤ 1 / 2 := by
    rw [div_le_iff₀ (by positivity)]
    have : ((2 * x1 : ℕ) : ℝ) ≤ ((D * S : ℕ) : ℝ) := by exact_mod_cast h2
    push_cast at this; linarith
  have := h c 0 (by linarith) hx1 hy0 hy1 hu0 hu1
  rw [Real.arctan_zero, mul_zero] at this
  exact this hbox

/-- At `θ = 0`, a box of centres below `y = ½` is covered by its top edge. -/
theorem CovMP.ax_clipY {D S Mq R W x0 x1 y0 y1 : ℕ} {pts : List (ℕ × ℕ × ℕ)} {segs : List SegE}
    {rects : List RectE} (hD : 0 < D) (hS : 0 < S) (h2 : 2 * y1 ≤ D * S)
    (h : CovMP D S Mq R W pts segs rects x0 x1 y1 y1 0 0) :
    CovMP D S Mq R W pts segs rects x0 x1 y0 y1 0 0 := by
  intro c u hx0 hx1 _ hy1 hu0 hu1 hbox
  have hu : u = 0 := by simp only [Nat.cast_zero, zero_div] at hu0 hu1; linarith
  subst hu
  rw [Real.arctan_zero, mul_zero] at hbox ⊢
  have hc := (half_le_of_sq_zero hbox).2
  have hy : (y1 : ℝ) / (D * S) ≤ 1 / 2 := by
    rw [div_le_iff₀ (by positivity)]
    have : ((2 * y1 : ℕ) : ℝ) ≤ ((D * S : ℕ) : ℝ) := by exact_mod_cast h2
    push_cast at this; linarith
  have := h c 0 hx0 hx1 (by linarith) hy1 hu0 hu1
  rw [Real.arctan_zero, mul_zero] at this
  exact this hbox

end ZMTreeM

end SquarePacking
