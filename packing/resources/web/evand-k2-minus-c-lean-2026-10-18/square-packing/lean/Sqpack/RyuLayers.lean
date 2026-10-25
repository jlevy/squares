import Sqpack.RyuFill
import Sqpack.RyuEnds

/-!
# The filled L-shape with two top layers: `c*(k) ≤ 4⌈√(2k − 7)⌉ − 1`

`RyuFill.packs_sub_4sqrt2` fills each band end with one axis layer of `⌊b/2⌋ − 1` squares.  Here, with the same
`b = ⌈√(2k − 7)⌉`, the same rows (`L − 3` per band of length `L`) and the end regions of `RyuEnds`:

* below the first row of each band, `⌊(b − 1)/2⌋` axis squares;
* above the last row of the right band, `⌊b/2⌋` axis squares;
* above the last row of the top band, `⌊b/2⌋ + 1` axis squares and a second layer of one square.

That is `2b` end squares in all, so `k² − 4b` squares pack in side `< k`, six more than `RyuFill`.  For every
`7 ≤ k ≤ 3 · 10⁵` this matches the best count of the construction over all `b` and all axis layers
(`search/ryu/r1prime.py`), so nothing more comes from axis-parallel end fills with these rows.

Each layer fits if it fits at the limiting angle `t₀ = 1/b` (`w = b`) with margin `1/(bD)`, `D = b² + 1`
(`layer_ok`); the angle is `t = 1/b + δ` with `δ · bD(6k + 4b) = 1`.
-/

namespace UnitSquarePacking.Ryu

open UnitSquarePacking.Conjectures

section angle
variable {b t : ℝ}

/-- `length_ok4` for any `t ∈ [1/b, 1/b + 1/(D(6K + 4b))]`. -/
lemma length_ok4' {L K : ℝ} (hb : 2 ≤ b) (hL0 : 0 ≤ L) (hLb : 2 * L ≤ b ^ 2 + 7) (hLK : L ≤ K)
    (hK : 0 < K) (ht0 : 1 / b ≤ t) (hδ : (t - 1 / b) * ((b ^ 2 + 1) * (6 * K + 4 * b)) ≤ 1) :
    (L - 4) * dd t + hh b t + (b - ww b t) ≤ L := by
  have hb0 : 0 < b := by linarith
  set D := b ^ 2 + 1 with hD
  have hD0 : 0 < D := by positivity
  set δ := t - 1 / b with hδd
  have hδ0 : 0 ≤ δ := by rw [hδd]; linarith
  have hc0 : 0 < 6 * K + 4 * b := by positivity
  have hδK : δ * (6 * K + 4 * b) ≤ 1 / D := by
    rw [le_div_iff₀ hD0]; nlinarith
  have hδs : δ ≤ 1 / 10 := by
    have : 10 ≤ D * (6 * K + 4 * b) := by nlinarith [mul_pos hD0 hK]
    nlinarith
  have h35 : t ≤ 3 / 5 := by
    have : 1 / b ≤ 1 / 2 := by rw [div_le_div_iff₀ hb0 (by norm_num)]; linarith
    linarith
  have hd := d_le (t₀ := 1 / b) (by positivity) ht0 h35
  have hh' := h_le (b := b) (t₀ := 1 / b) hb0.le (by positivity) ht0
  have hw := w_ge hb0 ht0
  rw [dd_t0 (by linarith)] at hd
  rw [hh_t0 hb0] at hh'
  rw [← hδd] at hd hh' hw
  have hb1 : 0 < b ^ 2 - 1 := by nlinarith
  have slack : (L - 4) * (1 + 2 / (b ^ 2 - 1)) + (3 - 4 / D) ≤ L - 4 / D := by
    have : (L - 4) * (2 / (b ^ 2 - 1)) ≤ 1 := by
      rw [mul_div_assoc', div_le_iff₀ hb1]; linarith
    nlinarith
  have pd : (L - 4) * dd t ≤ (L - 4) * (1 + 2 / (b ^ 2 - 1)) + 6 * L * δ := by
    have hdd : 1 + 2 / (b ^ 2 - 1) ≤ dd t := by
      rw [← dd_t0 (by linarith)]
      unfold dd
      have tp : 0 ≤ t := le_trans (by positivity) ht0
      have a : 0 < 1 - t ^ 2 := by nlinarith
      have a0 : 0 < 1 - (1 / b) ^ 2 := by
        have : 1 / b ≤ 1 / 2 := by rw [div_le_div_iff₀ hb0 (by norm_num)]; linarith
        nlinarith [show (0 : ℝ) < 1 / b by positivity]
      rw [div_le_div_iff₀ a0 a]
      have hsq : (1 / b) ^ 2 ≤ t ^ 2 := pow_le_pow_left₀ (by positivity) ht0 2
      nlinarith
    rcases le_total 4 L with h5 | h5
    · nlinarith [mul_le_mul_of_nonneg_left hd (by linarith : (0 : ℝ) ≤ L - 4)]
    · nlinarith [mul_le_mul_of_nonpos_left hdd (by linarith : L - 4 ≤ (0 : ℝ))]
  have total : 6 * L * δ + 2 * b * δ + 2 * b * δ ≤ 1 / D := by
    nlinarith [mul_le_mul_of_nonneg_right hLK hδ0]
  have hDp : 0 < 4 / D - 1 / D := by rw [← sub_div]; positivity
  linarith

/-- `cos` moves by at most `2(t² − t₀²)`. -/
lemma cos_pert {t₀ : ℝ} (h0 : 0 ≤ t₀) (h1 : t₀ ≤ t) :
    (1 - t₀ ^ 2) / (1 + t₀ ^ 2) - 2 * ((t - t₀) * (t + t₀)) ≤ (1 - t ^ 2) / (1 + t ^ 2) := by
  have a : 0 < 1 + t ^ 2 := by positivity
  have a0 : 0 < 1 + t₀ ^ 2 := by positivity
  have key : (1 - t₀ ^ 2) / (1 + t₀ ^ 2) - (1 - t ^ 2) / (1 + t ^ 2) =
      2 * ((t - t₀) * (t + t₀)) / ((1 + t ^ 2) * (1 + t₀ ^ 2)) := by field_simp; ring
  have hp : 0 ≤ (t - t₀) * (t + t₀) := mul_nonneg (by linarith) (by linarith)
  have : 2 * ((t - t₀) * (t + t₀)) / ((1 + t ^ 2) * (1 + t₀ ^ 2)) ≤ 2 * ((t - t₀) * (t + t₀)) := by
    rw [div_le_iff₀ (by positivity)]
    nlinarith [mul_nonneg hp (by positivity : (0 : ℝ) ≤ t ^ 2 + t₀ ^ 2 + t ^ 2 * t₀ ^ 2)]
  linarith

/-- `sin` moves by at most `2(t − t₀)`, and does not decrease on `[0, 1]`. -/
lemma sin_pert {t₀ : ℝ} (h0 : 0 ≤ t₀) (h1 : t₀ ≤ t) (h2 : t ≤ 1) :
    2 * t₀ / (1 + t₀ ^ 2) ≤ 2 * t / (1 + t ^ 2) ∧ 2 * t / (1 + t ^ 2) ≤ 2 * t₀ / (1 + t₀ ^ 2) + 2 * (t - t₀) := by
  have a : 0 < 1 + t ^ 2 := by positivity
  have a0 : 0 < 1 + t₀ ^ 2 := by positivity
  have key : 2 * t / (1 + t ^ 2) - 2 * t₀ / (1 + t₀ ^ 2) =
      2 * (t - t₀) * (1 - t * t₀) / ((1 + t ^ 2) * (1 + t₀ ^ 2)) := by field_simp; ring
  have e : 0 ≤ t - t₀ := by linarith
  have q : 0 ≤ 1 - t * t₀ := by nlinarith
  have q1 : 1 - t * t₀ ≤ 1 := by nlinarith
  constructor
  · have : 0 ≤ 2 * (t - t₀) * (1 - t * t₀) / ((1 + t ^ 2) * (1 + t₀ ^ 2)) := by positivity
    linarith
  · have : 2 * (t - t₀) * (1 - t * t₀) / ((1 + t ^ 2) * (1 + t₀ ^ 2)) ≤ 2 * (t - t₀) := by
      rw [div_le_iff₀ (by positivity)]
      have h1' : 1 ≤ (1 + t ^ 2) * (1 + t₀ ^ 2) := by
        nlinarith [sq_nonneg t, sq_nonneg t₀, mul_nonneg (sq_nonneg t) (sq_nonneg t₀)]
      have := mul_le_mul_of_nonneg_left (q1.trans h1') (by linarith : (0 : ℝ) ≤ 2 * (t - t₀))
      linarith
    linarith

/-- **A layer fits.**  With `γ, σ` at `t ∈ [1/b, 1/b + 1/(bD(6K + 4b))]`, the condition `σn ≤ γ(L − 1 − j) − R + σ²`
holds if it holds at `t₀ = 1/b` (where `γ₀ = (b² − 1)/D`, `σ₀ = 2b/D`) for some `L₀ ≥ L` within `2bδ` of `L`, with
margin `1/(bD)`. -/
lemma layer_ok {L L₀ K R n j : ℝ} (hb : 3 ≤ b) (ht0 : 1 / b ≤ t)
    (hδ : (t - 1 / b) * (b * (b ^ 2 + 1) * (6 * K + 4 * b)) ≤ 1)
    (hn0 : 0 ≤ n) (hnb : n ≤ b) (hbK : b ≤ K) (hj0 : 0 ≤ j) (hLj : 0 ≤ L - 1 - j) (hLL : L ≤ L₀) (hL₀K : L₀ ≤ K)
    (hL : L₀ - 2 * b * (t - 1 / b) ≤ L)
    (h0 : 2 * b / (b ^ 2 + 1) * n + 1 / (b * (b ^ 2 + 1)) ≤
      (b ^ 2 - 1) / (b ^ 2 + 1) * (L₀ - 1 - j) - R + (2 * b / (b ^ 2 + 1)) ^ 2) :
    2 * t / (1 + t ^ 2) * n ≤ (1 - t ^ 2) / (1 + t ^ 2) * (L - 1 - j) - R + (2 * t / (1 + t ^ 2)) ^ 2 := by
  have hb0 : 0 < b := by linarith
  set D := b ^ 2 + 1 with hD
  have hD0 : 0 < D := by positivity
  set δ := t - 1 / b with hδd
  have hδ0 : 0 ≤ δ := by rw [hδd]; linarith
  have hK : 0 < K := by linarith
  have hc0 : 0 < b * D * (6 * K + 4 * b) := by positivity
  have hδ' : δ ≤ 1 / (b * D * (6 * K + 4 * b)) := by rw [le_div_iff₀ hc0]; linarith
  have hδs : δ ≤ 1 / 100 := by
    have : 100 ≤ b * D * (6 * K + 4 * b) := by
      have : 10 ≤ D := by nlinarith
      have : 30 ≤ b * D := by nlinarith
      nlinarith
    calc δ ≤ 1 / (b * D * (6 * K + 4 * b)) := hδ'
      _ ≤ 1 / 100 := by rw [div_le_div_iff₀ hc0 (by norm_num)]; linarith
  have ht0' : 1 / b ≤ 1 / 3 := by rw [div_le_div_iff₀ hb0 (by norm_num)]; linarith
  have ht1 : t ≤ 1 := by linarith
  have e0 : (1 - (1 / b) ^ 2) / (1 + (1 / b) ^ 2) = (b ^ 2 - 1) / D := by rw [hD]; field_simp
  have e1 : 2 * (1 / b) / (1 + (1 / b) ^ 2) = 2 * b / D := by rw [hD]; field_simp
  have hcos := cos_pert (t := t) (t₀ := 1 / b) (by positivity) ht0
  have hsin := sin_pert (t := t) (t₀ := 1 / b) (by positivity) ht0 ht1
  rw [e0, ← hδd] at hcos
  rw [e1, ← hδd] at hsin
  set γ := (1 - t ^ 2) / (1 + t ^ 2) with hγ
  set σ := 2 * t / (1 + t ^ 2) with hσ
  set γ₀ := (b ^ 2 - 1) / D with hγ₀
  set σ₀ := 2 * b / D with hσ₀
  have hγ₀0 : 0 ≤ γ₀ := by rw [hγ₀]; apply div_nonneg (by nlinarith) hD0.le
  have hγ₀1 : γ₀ ≤ 1 := by rw [hγ₀, div_le_one hD0]; linarith
  have hσ₀0 : 0 ≤ σ₀ := by positivity
  have htt : t + 1 / b ≤ 1 := by linarith
  -- the three perturbations
  have pγ : γ₀ - 2 * δ ≤ γ := by
    have : (t - 1 / b) * (t + 1 / b) ≤ δ := by
      rw [← hδd]; nlinarith [mul_le_mul_of_nonneg_left htt hδ0]
    linarith
  have pσ2 : σ₀ ^ 2 ≤ σ ^ 2 := pow_le_pow_left₀ hσ₀0 hsin.1 2
  -- `γ(L − 1 − j) ≥ γ₀(L₀ − 1 − j) − 2δK − 2bδ`
  have pL : γ₀ * (L₀ - 1 - j) - 2 * δ * K - 2 * b * δ ≤ γ * (L - 1 - j) := by
    have a1 : (γ₀ - 2 * δ) * (L - 1 - j) ≤ γ * (L - 1 - j) := mul_le_mul_of_nonneg_right pγ hLj
    have a2 : L - 1 - j ≤ K := by linarith
    have a2' := mul_le_mul_of_nonneg_left a2 hδ0
    have a3 : γ₀ * (L₀ - L) ≤ 1 * (2 * b * δ) := mul_le_mul hγ₀1 (by linarith) (by linarith) (by norm_num)
    linarith
  have pn : σ * n ≤ σ₀ * n + 2 * b * δ := by
    have a1 := mul_le_mul_of_nonneg_right hsin.2 hn0
    have a2 := mul_le_mul_of_nonneg_left hnb hδ0
    linarith
  -- the perturbation is below the margin
  have hsmall : 2 * δ * K + 4 * b * δ ≤ 1 / (b * D) := by
    have a1 : δ * (b * D * (6 * K + 4 * b)) ≤ 1 := hδ
    have a2 : δ * (b * D * (2 * K + 4 * b)) ≤ 1 := by
      have := mul_le_mul_of_nonneg_left (show b * D * (2 * K + 4 * b) ≤ b * D * (6 * K + 4 * b) by
        apply mul_le_mul_of_nonneg_left (by linarith) (by positivity)) hδ0
      linarith
    rw [le_div_iff₀ (by positivity)]
    linarith
  linarith

end angle

/-- The margin at `t₀`: if `X − 2bn ≥ −3` then `σ₀ n + 1/(bD) ≤ X/D + σ₀²`. -/
lemma margin_ok {b X n : ℝ} (hb : 3 ≤ b) (hX : -3 ≤ X - 2 * b * n) :
    2 * b / (b ^ 2 + 1) * n + 1 / (b * (b ^ 2 + 1)) ≤ X / (b ^ 2 + 1) + (2 * b / (b ^ 2 + 1)) ^ 2 := by
  have hb0 : 0 < b := by linarith
  have hD0 : 0 < b ^ 2 + 1 := by positivity
  have e : X / (b ^ 2 + 1) + (2 * b / (b ^ 2 + 1)) ^ 2 - (2 * b / (b ^ 2 + 1) * n + 1 / (b * (b ^ 2 + 1))) =
      ((X - 2 * b * n) * b * (b ^ 2 + 1) + 4 * b ^ 3 - (b ^ 2 + 1)) / (b * (b ^ 2 + 1) ^ 2) := by
    field_simp; ring
  have num : 0 ≤ (X - 2 * b * n) * b * (b ^ 2 + 1) + 4 * b ^ 3 - (b ^ 2 + 1) := by
    have := mul_le_mul_of_nonneg_right hX (by positivity : (0 : ℝ) ≤ b * (b ^ 2 + 1))
    nlinarith [mul_pos hb0 hb0, mul_pos (mul_pos hb0 hb0) hb0]
  have : 0 ≤ ((X - 2 * b * n) * b * (b ^ 2 + 1) + 4 * b ^ 3 - (b ^ 2 + 1)) / (b * (b ^ 2 + 1) ^ 2) := by
    positivity
  linarith

/-! ## The counts -/

set_option maxHeartbeats 4000000 in
/-- **The L-shape with two top layers.**  For `3 ≤ b`, `b + 4 ≤ k`, `2k ≤ b² + 7`: `k² − 4b` unit squares pack in a
square of side `< k`. -/
theorem packs_layers (k b : ℕ) (hb : 3 ≤ b) (hkb : b + 4 ≤ k) (hk : 2 * k ≤ b ^ 2 + 7) :
    ∃ s < (k : ℝ), Packs (k * k - 4 * b) s := by
  obtain ⟨r, rfl⟩ : ∃ r, k = b + 4 + r := ⟨k - (b + 4), by omega⟩
  have hb' : (3 : ℝ) ≤ b := by exact_mod_cast hb
  have hb0 : (0 : ℝ) < b := by linarith
  have hr0 : (0 : ℝ) ≤ r := by positivity
  have hk2 : 2 * ((b : ℝ) + 4 + r) ≤ b ^ 2 + 7 := by exact_mod_cast hk
  set K : ℝ := (b : ℝ) + 4 + r with hKd
  have hK : (0 : ℝ) < K := by positivity
  set D : ℝ := (b : ℝ) ^ 2 + 1 with hD
  have hD0 : 0 < D := by positivity
  set δ : ℝ := 1 / (b * D * (6 * K + 4 * b)) with hδd
  have hδpos : 0 < δ := by positivity
  set t : ℝ := 1 / b + δ with ht
  have htδ : t - 1 / b = δ := by rw [ht]; ring
  have hδeq : δ * (b * D * (6 * K + 4 * b)) = 1 := by rw [hδd, one_div, inv_mul_cancel₀ (by positivity)]
  have ht0 : 1 / (b : ℝ) ≤ t := by rw [ht]; linarith
  have ht0' : 1 / (b : ℝ) < t := by rw [ht]; linarith
  have hδ1 : (t - 1 / b) * (D * (6 * K + 4 * b)) ≤ 1 := by
    rw [htδ]
    have h0 : 0 ≤ δ * (D * (6 * K + 4 * b)) := by positivity
    nlinarith
  have hδb : (t - 1 / b) * (b * (b ^ 2 + 1) * (6 * K + 4 * b)) ≤ 1 := by rw [htδ, ← hD]; linarith
  have htpos : 0 < t := lt_of_lt_of_le (by positivity) ht0
  have hδs : δ ≤ 1 / 100 := by
    rw [hδd, div_le_div_iff₀ (by positivity) (by norm_num)]
    have : 10 ≤ D := by nlinarith
    have : 30 ≤ (b : ℝ) * D := by nlinarith
    nlinarith
  have ht13 : 1 / (b : ℝ) ≤ 1 / 3 := by rw [div_le_div_iff₀ hb0 (by norm_num)]; linarith
  have ht1 : t < 1 := by linarith
  have h2bδ' : 2 * (b : ℝ) * δ ≤ 1 / (b * D) := by
    rw [hδd, le_div_iff₀ (by positivity)]; field_simp; nlinarith
  have h2bδ : 2 * (b : ℝ) * δ ≤ 1 / 10 := by
    rw [hδd]; field_simp
    nlinarith [mul_pos hD0 hK]
  clear_value t δ K D
  -- the angle
  have hu : ((1 - t ^ 2) / (1 + t ^ 2)) ^ 2 + (2 * t / (1 + t ^ 2)) ^ 2 = 1 := by field_simp; ring
  obtain ⟨θ, hc, hs⟩ := exists_angle hu
  have hγ : 0 < Real.cos θ := by rw [hc]; apply div_pos <;> nlinarith
  have hσ : 0 < Real.sin θ := by rw [hs]; positivity
  have huθ : Real.cos θ ^ 2 + Real.sin θ ^ 2 = 1 := by rw [add_comm]; exact Real.sin_sq_add_cos_sq θ
  have ed : 1 / Real.cos θ = dd t := by rw [hc, dd, one_div_div]
  have eh : (b : ℝ) * Real.sin θ + Real.cos θ = hh b t := by rw [hc, hs, hh]; field_simp; ring
  have ew : (b : ℝ) * Real.cos θ + Real.sin θ = ww b t := by rw [hc, hs, ww]; field_simp
  have hww : ww b t < b := w_lt hb0 ht0'
  have hwge : (b : ℝ) - 2 * b * δ ≤ ww b t := by have := w_ge hb0 ht0; rw [htδ] at this; linarith
  set γ := Real.cos θ with hγd
  set σ := Real.sin θ with hσd
  have L1 := length_ok4' (b := (b : ℝ)) (t := t) (L := K) (K := K) (by linarith) hK.le hk2 le_rfl hK ht0 (by rw [← hD]; exact hδ1)
  have L2 := length_ok4' (b := (b : ℝ)) (t := t) (L := (4 : ℝ) + r) (K := K) (by linarith)
    (by positivity) (by linarith) (by rw [hKd]; linarith) hK ht0 (by rw [← hD]; exact hδ1)
  have eH : ∀ R : ℕ, ((R : ℝ) - 1) / γ + b * σ + γ = ((R : ℝ) - 1) * dd t + hh b t := by
    intro R; rw [← eh, ← ed]; ring
  -- row lengths: `b + 1 + r` rows in `(4 + r) + w`, `1 + r` rows in `4 + r`
  have HR1 : (((b + 1 + r : ℕ) : ℝ) - 1) / γ + b * σ + γ ≤ ((4 + r : ℕ) : ℝ) + (b * γ + σ) := by
    rw [eH, ew]; push_cast; rw [hKd] at L1; linarith [L1]
  have HR2 : (((1 + r : ℕ) : ℝ) - 1) / γ + b * σ + γ ≤ ((4 + r : ℕ) : ℝ) := by
    rw [eH]; push_cast; linarith [L2]
  -- the end conditions
  have top : ∀ (R : ℕ) (L : ℝ) (j n : ℕ), σ * n ≤ γ * (L - 1 - j) - R + σ ^ 2 →
      γ * (j + 1) - σ * (b * γ + σ - n) ≤ γ * (L - ((R - 1) / γ + b * σ + γ)) - σ ^ 2 := by
    intro R L j n h
    have e : γ * ((R - 1) / γ) = R - 1 := by field_simp
    have e2 : γ * (L - ((R - 1) / γ + b * σ + γ)) = γ * L - γ * ((R - 1) / γ) - b * σ * γ - γ ^ 2 := by ring
    rw [e2, e]
    linarith
  have bot : ∀ n : ℕ, (n : ℝ) ≤ b * γ - γ / σ →
      γ * (((0 : ℕ) : ℝ) + 1) - σ * (b * γ + σ - n) ≤ γ * 0 - σ ^ 2 := by
    intro n h
    have e : σ * (γ / σ) = γ := by field_simp
    have := mul_le_mul_of_nonneg_left h hσ.le
    push_cast
    have e2 : σ * (b * γ - γ / σ) = b * γ * σ - σ * (γ / σ) := by ring
    rw [e2, e] at this
    linarith
  -- `layer_ok`, in the `γ, σ` of `θ`
  have lay : ∀ (L L₀ R n j : ℝ), 0 ≤ n → n ≤ b → 0 ≤ j → 0 ≤ L - 1 - j → L ≤ L₀ → L₀ ≤ K →
      L₀ - 2 * b * δ ≤ L →
      2 * b / (b ^ 2 + 1) * n + 1 / (b * (b ^ 2 + 1)) ≤
        (b ^ 2 - 1) / (b ^ 2 + 1) * (L₀ - 1 - j) - R + (2 * b / (b ^ 2 + 1)) ^ 2 →
      σ * n ≤ γ * (L - 1 - j) - R + σ ^ 2 := by
    intro L L₀ R n j h1 h2 h3 h4 h5 h6 h7 h8
    have := layer_ok (b := (b : ℝ)) (t := t) (K := K) hb' ht0 hδb h1 h2 (by rw [hKd]; linarith) h3 h4 h5 h6
      (by rw [htδ]; exact h7) h8
    rw [hc, hs]; exact this
  -- the fill counts
  set nb : ℕ := (b - 1) / 2 with hnbd
  set nh : ℕ := b / 2 with hnhd
  have hnb2 : 2 * nb + 1 ≤ b := by omega
  have hnh2 : 2 * nh ≤ b := by omega
  have hsum : nb + nh + 1 = b := by omega
  have hnb2' : 2 * (nb : ℝ) + 1 ≤ b := by exact_mod_cast hnb2
  have hnh2' : 2 * (nh : ℝ) ≤ b := by exact_mod_cast hnh2
  have hwb : (b : ℝ) - 1 / 10 ≤ b * γ + σ := by rw [ew]; linarith
  -- bottom: `nb ≤ bγ − γ/σ`
  have hnb : (nb : ℝ) ≤ b * γ - γ / σ := by
    have hcot : γ / σ ≤ ((b : ℝ) ^ 2 - 1) / (2 * b) := by
      have e : γ / σ = (1 - t ^ 2) / (2 * t) := by rw [hc, hs]; field_simp
      rw [e, div_le_div_iff₀ (by positivity) (by positivity)]
      have : 1 ≤ b * t := by rw [div_le_iff₀ hb0] at ht0; linarith
      nlinarith [mul_nonneg (by linarith : (0 : ℝ) ≤ b * t - 1) (by positivity : (0 : ℝ) ≤ b + t)]
    have hcos := cos_pert (t := t) (t₀ := 1 / b) (by positivity) ht0
    have e0 : (1 - (1 / (b : ℝ)) ^ 2) / (1 + (1 / b) ^ 2) = ((b : ℝ) ^ 2 - 1) / D := by rw [hD]; field_simp
    rw [e0, ← hc, htδ] at hcos
    have hpp : δ * (t + 1 / b) ≤ δ := by
      have : t + 1 / (b : ℝ) ≤ 1 := by linarith
      nlinarith [mul_le_mul_of_nonneg_left this hδpos.le]
    have hbγ : (b : ℝ) * (((b : ℝ) ^ 2 - 1) / D) - 2 * b * δ ≤ b * γ := by
      nlinarith [mul_le_mul_of_nonneg_left hcos hb0.le]
    have at0 : ((b : ℝ) - 1) / 2 + 1 / (b * D) ≤ b * (((b : ℝ) ^ 2 - 1) / D) - ((b : ℝ) ^ 2 - 1) / (2 * b) := by
      have e : b * (((b : ℝ) ^ 2 - 1) / D) - ((b : ℝ) ^ 2 - 1) / (2 * b) - (((b : ℝ) - 1) / 2 + 1 / (b * D)) =
          ((b : ℝ) ^ 3 - 3 * b ^ 2 + b - 1) / (2 * b * D) := by
        rw [hD]; field_simp; ring
      have : 0 ≤ ((b : ℝ) ^ 3 - 3 * b ^ 2 + b - 1) / (2 * b * D) := by
        apply div_nonneg _ (by positivity)
        nlinarith [mul_nonneg (mul_nonneg hb0.le hb0.le) (by linarith : (0 : ℝ) ≤ b - 3)]
      linarith
    linarith
  have hnbw : (nb : ℝ) ≤ b * γ + σ := by linarith
  have hnhw : (nh : ℝ) + 1 ≤ b * γ + σ := by linarith
  -- the four end packings
  have P0 : PacksIn nb (endReg γ σ (b * γ + σ) 0) := by
    have := axis_layers (γ := γ) (σ := σ) (w := b * γ + σ) (y := 0) hγ.le hσ.le 1 (fun _ => nb)
      (fun j hj => hnbw) (fun j hj => by
        obtain rfl : j = 0 := by omega
        exact bot nb hnb)
    simpa using this.mono Set.inter_subset_left
  set y₁ : ℝ := ((4 + r : ℕ) : ℝ) + (b * γ + σ) - ((((b + 1 + r : ℕ) : ℝ) - 1) / γ + b * σ + γ) with hy₁
  set y₂ : ℝ := ((4 + r : ℕ) : ℝ) - ((((1 + r : ℕ) : ℝ) - 1) / γ + b * σ + γ) with hy₂
  have P1 : PacksIn nh (endReg γ σ (b * γ + σ) y₁) := by
    have m0 : 2 * b / ((b : ℝ) ^ 2 + 1) * nh + 1 / (b * ((b : ℝ) ^ 2 + 1)) ≤
        ((b : ℝ) ^ 2 - 1) / (b ^ 2 + 1) * (K - 1 - 0) - (((b + 1 + r : ℕ) : ℝ)) + (2 * b / ((b : ℝ) ^ 2 + 1)) ^ 2 := by
      have e : ((b : ℝ) ^ 2 - 1) / (b ^ 2 + 1) * (K - 1 - 0) - (((b + 1 + r : ℕ) : ℝ)) =
          (2 * b ^ 2 - 2 * b - 2 * r - 4) / (b ^ 2 + 1) := by rw [hKd]; push_cast; field_simp; ring
      rw [e]
      apply margin_ok hb'
      nlinarith [mul_le_mul_of_nonneg_left hnh2' hb0.le]
    have c0 : σ * nh ≤ γ * (((4 + r : ℕ) : ℝ) + (b * γ + σ) - 1 - ((0 : ℕ) : ℝ)) - ((b + 1 + r : ℕ) : ℝ) +
        σ ^ 2 := by
      have h4 : (0 : ℝ) ≤ ((4 + r : ℕ) : ℝ) + (b * γ + σ) - 1 - ((0 : ℕ) : ℝ) := by push_cast; linarith
      have h5 : ((4 + r : ℕ) : ℝ) + (b * γ + σ) ≤ K := by rw [hKd, ew]; push_cast; linarith
      have h7 : K - 2 * b * δ ≤ ((4 + r : ℕ) : ℝ) + (b * γ + σ) := by rw [hKd, ew]; push_cast; linarith
      have := lay _ K _ _ _ (by positivity) (by linarith) (le_refl (0 : ℝ)) (by simpa using h4) h5 le_rfl h7 m0
      simpa using this
    have := axis_layers (γ := γ) (σ := σ) (w := b * γ + σ) (y := y₁) hγ.le hσ.le 1 (fun _ => nh)
      (fun j hj => by linarith) (fun j hj => by
        obtain rfl : j = 0 := by omega
        rw [hy₁]; exact top _ _ 0 nh c0)
    simpa using this.mono Set.inter_subset_left
  have P2 : PacksIn (nh + 1 + 1) (endReg γ σ (b * γ + σ) y₂) := by
    have hm4 : ((4 + r : ℕ) : ℝ) ≤ K := by rw [hKd]; push_cast; linarith
    have hm4' : ((4 + r : ℕ) : ℝ) - 2 * b * δ ≤ ((4 + r : ℕ) : ℝ) := by nlinarith [hδpos]
    have m0 : 2 * b / ((b : ℝ) ^ 2 + 1) * ((nh + 1 : ℕ) : ℝ) + 1 / (b * ((b : ℝ) ^ 2 + 1)) ≤
        ((b : ℝ) ^ 2 - 1) / (b ^ 2 + 1) * (((4 + r : ℕ) : ℝ) - 1 - 0) - (((1 + r : ℕ) : ℝ)) +
          (2 * b / ((b : ℝ) ^ 2 + 1)) ^ 2 := by
      have e : ((b : ℝ) ^ 2 - 1) / (b ^ 2 + 1) * (((4 + r : ℕ) : ℝ) - 1 - 0) - (((1 + r : ℕ) : ℝ)) =
          (2 * b ^ 2 - 2 * r - 4) / (b ^ 2 + 1) := by push_cast; field_simp; ring
      rw [e]
      apply margin_ok hb'
      push_cast
      nlinarith [mul_le_mul_of_nonneg_left hnh2' hb0.le]
    have m1 : 2 * b / ((b : ℝ) ^ 2 + 1) * ((1 : ℕ) : ℝ) + 1 / (b * ((b : ℝ) ^ 2 + 1)) ≤
        ((b : ℝ) ^ 2 - 1) / (b ^ 2 + 1) * (((4 + r : ℕ) : ℝ) - 1 - 1) - (((1 + r : ℕ) : ℝ)) +
          (2 * b / ((b : ℝ) ^ 2 + 1)) ^ 2 := by
      have e : ((b : ℝ) ^ 2 - 1) / (b ^ 2 + 1) * (((4 + r : ℕ) : ℝ) - 1 - 1) - (((1 + r : ℕ) : ℝ)) =
          (b ^ 2 - 2 * r - 3) / (b ^ 2 + 1) := by push_cast; field_simp; ring
      rw [e]
      apply margin_ok hb'
      push_cast
      nlinarith
    have c0 : σ * ((nh + 1 : ℕ) : ℝ) ≤ γ * (((4 + r : ℕ) : ℝ) - 1 - ((0 : ℕ) : ℝ)) - ((1 + r : ℕ) : ℝ) + σ ^ 2 := by
      have := lay _ _ _ _ 0 (by positivity) (by push_cast; linarith) (le_refl (0 : ℝ)) (by push_cast; linarith)
        le_rfl hm4 hm4' m0
      simpa using this
    have c1 : σ * ((1 : ℕ) : ℝ) ≤ γ * (((4 + r : ℕ) : ℝ) - 1 - ((1 : ℕ) : ℝ)) - ((1 + r : ℕ) : ℝ) + σ ^ 2 := by
      have := lay _ _ _ _ 1 (by positivity) (by push_cast; linarith) (by norm_num) (by push_cast; linarith)
        le_rfl hm4 hm4' m1
      simpa using this
    have := axis_layers (γ := γ) (σ := σ) (w := b * γ + σ) (y := y₂) hγ.le hσ.le 2
      (fun j => if j = 0 then nh + 1 else 1)
      (fun j hj => by split_ifs <;> push_cast <;> linarith) (fun j hj => by
        rcases (show j = 0 ∨ j = 1 by omega) with rfl | rfl
        · simp only [if_true]; rw [hy₂]; exact top _ _ 0 (nh + 1) c0
        · simp only [one_ne_zero, if_false]; rw [hy₂]; exact top _ _ 1 1 c1)
    have e : ∑ j ∈ Finset.range 2, (if j = 0 then nh + 1 else 1) = nh + 1 + 1 := by
      simp [Finset.sum_range_succ]
    rw [e] at this
    exact this.mono Set.inter_subset_left
  -- the two bands
  have hy₁0 : 0 ≤ y₁ := by rw [hy₁]; linarith
  have hy₂0 : 0 ≤ y₂ := by rw [hy₂]; linarith
  have B1' : PacksIn (nb + (b + 1 + r) * b + nh) (rect (b * γ + σ) (((4 + r : ℕ) : ℝ) + (b * γ + σ))) :=
    band_ends (L := ((4 + r : ℕ) : ℝ) + (b * γ + σ)) hγ hσ.le (b + 1 + r) b (by omega) (le_refl (0 : ℝ)) hy₁0
      (le_of_eq (by rw [hy₁]; ring)) P0 P1
  have B2' : PacksIn (nb + (1 + r) * b + (nh + 1 + 1)) (rect (b * γ + σ) ((4 + r : ℕ) : ℝ)) :=
    band_ends (L := ((4 + r : ℕ) : ℝ)) hγ hσ.le (1 + r) b (by omega) (le_refl (0 : ℝ)) hy₂0
      (le_of_eq (by rw [hy₂]; ring)) P0 P2
  have P := lshape (by linarith : (0 : ℝ) ≤ b * γ + σ) B1' B2'
  refine ⟨((4 + r : ℕ) : ℝ) + (b * γ + σ), ?_, ?_⟩
  · rw [ew]; push_cast; linarith
  · have key : (4 + r) * (4 + r) + (nb + (b + 1 + r) * b + nh) + (nb + (1 + r) * b + (nh + 1 + 1)) + 4 * b =
        (b + 4 + r) * (b + 4 + r) := by
      have : nb + nh = b - 1 := by omega
      have h2 : 2 * nb + 2 * nh + 2 = 2 * b := by omega
      nlinarith [h2]
    rw [show (b + 4 + r) * (b + 4 + r) - 4 * b = (4 + r) * (4 + r) + (nb + (b + 1 + r) * b + nh) +
      (nb + (1 + r) * b + (nh + 1 + 1)) by omega]
    exact P

/-- **`c*(k) ≤ 4⌈√(2k − 7)⌉ − 1`** for every `k ≥ 7`: `k² − 4b` unit squares pack in a square of side `< k`, with
`b = ⌈√(2k − 7)⌉ = Nat.sqrt (2k − 8) + 1`. -/
theorem packs_sub_4sqrt2_layers (k : ℕ) (hk : 7 ≤ k) :
    ∃ s < (k : ℝ), Packs (k * k - 4 * (Nat.sqrt (2 * k - 8) + 1)) s := by
  set b := Nat.sqrt (2 * k - 8) + 1 with hbd
  have hb : 3 ≤ b := by
    have : 2 ≤ Nat.sqrt (2 * k - 8) := Nat.le_sqrt.2 (by omega)
    omega
  have hk2 : 2 * k ≤ b ^ 2 + 7 := by
    have := Nat.lt_succ_sqrt (2 * k - 8)
    have : 2 * k - 8 < b ^ 2 := by rw [hbd]; nlinarith
    omega
  have hkb : b + 4 ≤ k := by
    have : Nat.sqrt (2 * k - 8) < k - 4 := by
      rw [Nat.sqrt_lt']
      obtain ⟨j, rfl⟩ : ∃ j, k = j + 7 := ⟨k - 7, by omega⟩
      have e1 : 2 * (j + 7) - 8 = 2 * j + 6 := by omega
      have e2 : j + 7 - 4 = j + 3 := by omega
      rw [e1, e2]; nlinarith
    omega
  exact packs_layers k b hb hkb hk2

end UnitSquarePacking.Ryu
