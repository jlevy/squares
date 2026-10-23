import Sqpack.RyuBand

/-!
# Ryu's bound `c*(k) ≤ 8⌈√(k − 4)⌉ − 1` (his Theorems 1.3–1.4)

S. Ryu, squarepacker/k2-minus-c-upper v1.1 (jlevy/squares#471, #486).  The geometry is `RyuBand.lpacking`.  Here
the angle and the counts.

The tilt is `θ = 2 arctan t` with `t` rational, so `γ = cos θ = (1 − t²)/(1 + t²)`, `σ = sin θ = 2t/(1 + t²)`.
In terms of `t`: row spacing `d = 1/γ = (1 + t²)/(1 − t²)`, row height `h = bσ + γ`, band width `w = bγ + σ`.
At `t₀ = 1/b`: `d = 1 + 2/(b² − 1)`, `h = 3 − 4/(b² + 1)`, `w = b`; for `t > t₀`, `w < b`.

We take `R₁ = k − 4` rows on the right and `R₂ = k − b − 4` on top (Ryu's counts `R(L) = L − 3 − ⌊η_L⌋` with both
floors equal to 1; no ceilings are needed).  Then `k² − N = b(2k − b − R₁ − R₂) = 8b`.  A band of `L − 4` rows needs
length `(L − 5)d + h`, which at `t₀` leaves slack `2 + 4/D − 2(L − 5)/(b² − 1) ≥ 4/D` (`D = b² + 1`) when
`L ≤ b² + 4`.  Moving to `t = t₀ + δ` costs at most `δ (6L + 4b)` (`d_le`, `h_le`, `w_ge`), and
`δ = 1/(D (6k + 4b))` keeps both bands inside.  This replaces Ryu's mean-value argument (Lemma 4.2) and his
`M = 14kb² + 1`.
-/

namespace UnitSquarePacking.Ryu

open UnitSquarePacking.Conjectures

section angle
variable {b t : ℝ}

/-- Row spacing `1/γ`. -/
noncomputable def dd (t : ℝ) : ℝ := (1 + t ^ 2) / (1 - t ^ 2)
/-- Row height `bσ + γ`. -/
noncomputable def hh (b t : ℝ) : ℝ := (2 * b * t + 1 - t ^ 2) / (1 + t ^ 2)
/-- Band width `bγ + σ`. -/
noncomputable def ww (b t : ℝ) : ℝ := (b * (1 - t ^ 2) + 2 * t) / (1 + t ^ 2)

lemma d_le {t₀ : ℝ} (h0 : 0 ≤ t₀) (h1 : t₀ ≤ t) (h2 : t ≤ 3 / 5) : dd t ≤ dd t₀ + 6 * (t - t₀) := by
  have a : 0 < 1 - t ^ 2 := by nlinarith
  have a0 : 0 < 1 - t₀ ^ 2 := by nlinarith
  unfold dd
  rw [div_add' _ _ _ a0.ne', div_le_div_iff₀ a a0]
  have e : 0 ≤ t - t₀ := by linarith
  have p1 : 16 / 25 ≤ 1 - t ^ 2 := by nlinarith
  have p2 : 16 / 25 ≤ 1 - t₀ ^ 2 := by nlinarith
  have key : 2 * (t + t₀) ≤ 6 * (1 - t ^ 2) * (1 - t₀ ^ 2) := by
    nlinarith [mul_le_mul p1 p2 (by norm_num) (by linarith)]
  nlinarith [mul_nonneg e (by nlinarith : 0 ≤ 6 * (1 - t ^ 2) * (1 - t₀ ^ 2) - 2 * (t + t₀)), mul_pos a a0]

lemma h_le {t₀ : ℝ} (hb : 0 ≤ b) (h0 : 0 ≤ t₀) (h1 : t₀ ≤ t) :
    hh b t ≤ hh b t₀ + 2 * b * (t - t₀) := by
  have a : 0 < 1 + t ^ 2 := by positivity
  have a0 : 0 < 1 + t₀ ^ 2 := by positivity
  have key : hh b t - hh b t₀ =
      (t - t₀) * (2 * b - 2 * b * t * t₀ - 2 * (t + t₀)) / ((1 + t ^ 2) * (1 + t₀ ^ 2)) := by
    unfold hh; field_simp; ring
  have e : 0 ≤ t - t₀ := by linarith
  have ht : 0 ≤ t := by linarith
  have : (t - t₀) * (2 * b - 2 * b * t * t₀ - 2 * (t + t₀)) / ((1 + t ^ 2) * (1 + t₀ ^ 2)) ≤
      2 * b * (t - t₀) := by
    rw [div_le_iff₀ (by positivity)]
    have q : 1 ≤ (1 + t ^ 2) * (1 + t₀ ^ 2) := by nlinarith [sq_nonneg t, sq_nonneg t₀, mul_nonneg (sq_nonneg t) (sq_nonneg t₀)]
    nlinarith [mul_nonneg (mul_nonneg hb e) (mul_nonneg ht h0), mul_nonneg e (add_nonneg ht h0),
      mul_le_mul_of_nonneg_left q (mul_nonneg hb e)]
  linarith

lemma w_ge (hb : 0 < b) (h1 : 1 / b ≤ t) : b - ww b t ≤ 2 * b * (t - 1 / b) := by
  have a : 0 < 1 + t ^ 2 := by positivity
  have ht : 0 < t := lt_of_lt_of_le (by positivity) h1
  have key : b - ww b t = 2 * t * b * (t - 1 / b) / (1 + t ^ 2) := by
    unfold ww; field_simp; ring
  have e0 : 0 ≤ t - 1 / b := by linarith
  rw [key, div_le_iff₀ a]
  nlinarith [mul_nonneg (mul_nonneg hb.le e0) (by nlinarith : 0 ≤ (1 + t ^ 2) - t)]

lemma w_lt (hb : 0 < b) (h1 : 1 / b < t) : ww b t < b := by
  have a : 0 < 1 + t ^ 2 := by positivity
  unfold ww
  rw [div_lt_iff₀ a]
  have : 1 < b * t := by rwa [div_lt_iff₀ hb, mul_comm] at h1
  have ht : 0 < t := lt_trans (by positivity) h1
  nlinarith

lemma dd_t0 (hb : 1 < b) : dd (1 / b) = 1 + 2 / (b ^ 2 - 1) := by
  have : 0 < b ^ 2 - 1 := by nlinarith
  unfold dd; field_simp; ring

lemma hh_t0 (hb : 0 < b) : hh b (1 / b) = 3 - 4 / (b ^ 2 + 1) := by
  unfold hh; field_simp; ring

/-- **The length condition.**  `L − 4` rows plus the width deficit fit in length `L`. -/
lemma length_ok {L K : ℝ} (hb : 2 ≤ b) (hL0 : 0 ≤ L) (hLb : L ≤ b ^ 2 + 4) (hLK : L ≤ K)
    (hK : 0 < K) (ht : t = 1 / b + 1 / ((b ^ 2 + 1) * (6 * K + 4 * b))) :
    (L - 5) * dd t + hh b t + (b - ww b t) ≤ L := by
  have hb0 : 0 < b := by linarith
  set D := b ^ 2 + 1 with hD
  have hD0 : 0 < D := by positivity
  set δ := 1 / (D * (6 * K + 4 * b)) with hδ
  have hδ0 : 0 < δ := by positivity
  have hc0 : 0 < 6 * K + 4 * b := by positivity
  have hδK : δ * (6 * K + 4 * b) = 1 / D := by rw [hδ]; field_simp
  have ht0 : 1 / b ≤ t := by rw [ht]; linarith
  have hδs : δ ≤ 1 / 10 := by
    rw [hδ, div_le_div_iff₀ (by positivity) (by norm_num)]
    nlinarith [mul_pos hD0 hK]
  have h35 : t ≤ 3 / 5 := by
    have : 1 / b ≤ 1 / 2 := by rw [div_le_div_iff₀ hb0 (by norm_num)]; linarith
    rw [ht]; linarith
  have e : t - 1 / b = δ := by rw [ht]; ring
  have hd := d_le (t₀ := 1 / b) (by positivity) ht0 h35
  have hh' := h_le (b := b) (t₀ := 1 / b) hb0.le (by positivity) ht0
  have hw := w_ge hb0 ht0
  rw [dd_t0 (by linarith)] at hd
  rw [hh_t0 hb0] at hh'
  rw [e] at hd hh' hw
  -- the slack at `t₀`
  have hb1 : 0 < b ^ 2 - 1 := by nlinarith
  have slack : (L - 5) * (1 + 2 / (b ^ 2 - 1)) + (3 - 4 / D) ≤ L - 4 / D := by
    have : (L - 5) * (2 / (b ^ 2 - 1)) ≤ 2 := by
      rw [mul_div_assoc', div_le_iff₀ hb1]; linarith
    nlinarith
  -- the perturbation
  have pd : (L - 5) * dd t ≤ (L - 5) * (1 + 2 / (b ^ 2 - 1)) + 6 * L * δ := by
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
    rcases le_total 5 L with h5 | h5
    · nlinarith [mul_le_mul_of_nonneg_left hd (by linarith : (0 : ℝ) ≤ L - 5)]
    · nlinarith [mul_le_mul_of_nonpos_left hdd (by linarith : L - 5 ≤ (0 : ℝ))]
  have total : 6 * L * δ + 2 * b * δ + 2 * b * δ ≤ 1 / D := by
    rw [← hδK]; nlinarith
  have hDp : 0 < 4 / D - 1 / D := by rw [← sub_div]; positivity
  linarith

end angle

/-- **Ryu's Theorem 1.4, in the form used here.**  For `2 ≤ b`, `b + 4 ≤ k ≤ b² + 4`: `k² − 8b` unit squares pack
in a square of side `< k`. -/
theorem packs_sub_8b (k b : ℕ) (hb : 2 ≤ b) (hkb : b + 4 ≤ k) (hk : k ≤ b ^ 2 + 4) :
    ∃ s < (k : ℝ), Packs (k * k - 8 * b) s := by
  set t : ℝ := 1 / b + 1 / ((b ^ 2 + 1) * (6 * k + 4 * b)) with ht
  have hb' : (2 : ℝ) ≤ b := by exact_mod_cast hb
  have hb0 : (0 : ℝ) < b := by linarith
  have hk' : (b : ℝ) + 4 ≤ k := by exact_mod_cast hkb
  have hk2 : (k : ℝ) ≤ b ^ 2 + 4 := by exact_mod_cast hk
  have hK : (0 : ℝ) < k := by linarith
  have htpos : 0 < t := by rw [ht]; positivity
  have ht35 : t < 1 := by
    have : 1 / (b : ℝ) ≤ 1 / 2 := by rw [div_le_div_iff₀ hb0 (by norm_num)]; linarith
    have : 1 / (((b : ℝ) ^ 2 + 1) * (6 * k + 4 * b)) ≤ 1 / 10 := by
      rw [div_le_div_iff₀ (by positivity) (by norm_num)]; nlinarith
    rw [ht]; linarith
  -- the angle
  have hu : ((1 - t ^ 2) / (1 + t ^ 2)) ^ 2 + (2 * t / (1 + t ^ 2)) ^ 2 = 1 := by
    field_simp; ring
  obtain ⟨θ, hc, hs⟩ := exists_angle hu
  have hγ : 0 < Real.cos θ := by rw [hc]; apply div_pos <;> nlinarith
  have hσ : 0 ≤ Real.sin θ := by rw [hs]; positivity
  have ed : 1 / Real.cos θ = dd t := by rw [hc, dd, one_div_div]
  have eh : (b : ℝ) * Real.sin θ + Real.cos θ = hh b t := by rw [hc, hs, hh]; field_simp; ring
  have ew : (b : ℝ) * Real.cos θ + Real.sin θ = ww b t := by rw [hc, hs, ww]; field_simp
  -- the counts: k = b + 4 + r
  obtain ⟨r, rfl⟩ : ∃ r, k = b + 4 + r := ⟨k - (b + 4), by omega⟩
  have L1 := length_ok (b := (b : ℝ)) (t := t) (L := ((b + 4 + r : ℕ) : ℝ)) (K := ((b + 4 + r : ℕ) : ℝ)) hb'
    (by positivity) hk2 le_rfl hK ht
  have L2 := length_ok (b := (b : ℝ)) (t := t) (L := ((4 + r : ℕ) : ℝ)) (K := ((b + 4 + r : ℕ) : ℝ)) hb'
    (by positivity) (by push_cast at hk2 ⊢; linarith) (by push_cast; linarith) hK ht
  have hpos : (0 : ℝ) < 1 / ((b ^ 2 + 1) * (6 * ↑(b + 4 + r) + 4 * b)) := by positivity
  have hww : ww b t < b := w_lt hb0 (by rw [ht]; linarith)
  have P := lpacking hγ hσ (4 + r) b (b + r) r ?_ ?_
  · refine ⟨((4 + r : ℕ) : ℝ) + (b * Real.cos θ + Real.sin θ), ?_, ?_⟩
    · rw [ew]; push_cast; linarith
    · have : (b + 4 + r) * (b + 4 + r) - 8 * b = (4 + r) * (4 + r) + (b + r) * b + r * b := by
        have : 8 * b ≤ (b + 4 + r) * (b + 4 + r) := by nlinarith
        zify [this]; ring
      rw [this]; exact P
  · -- right band: `b + r` rows in length `(4 + r) + w`
    have key : (((b + r : ℕ) : ℝ) - 1) / Real.cos θ + b * Real.sin θ + Real.cos θ =
        (((b + 4 + r : ℕ) : ℝ) - 5) * dd t + hh b t := by
      rw [← eh, ← ed]; push_cast; ring
    rw [key, ew]
    push_cast at L1 ⊢
    linarith
  · -- top band: `r` rows in length `4 + r`
    have key : ((r : ℝ) - 1) / Real.cos θ + b * Real.sin θ + Real.cos θ =
        (((4 + r : ℕ) : ℝ) - 5) * dd t + hh b t := by
      rw [← eh, ← ed]; push_cast; ring
    rw [key]
    push_cast at L2 ⊢
    linarith

/-- **Ryu's bound** (Theorem 1.4): for every `k ≥ 6`, `k² − 8⌈√(k − 4)⌉` unit squares pack in a square of side
`< k`, i.e. `c*(k) ≤ 8⌈√(k − 4)⌉ − 1`.  Here `⌈√(k − 4)⌉ = Nat.sqrt (k − 5) + 1`. -/
theorem packs_sub_8sqrt (k : ℕ) (hk : 6 ≤ k) :
    ∃ s < (k : ℝ), Packs (k * k - 8 * (Nat.sqrt (k - 5) + 1)) s := by
  apply packs_sub_8b
  · have : 1 ≤ Nat.sqrt (k - 5) := Nat.le_sqrt.2 (by omega)
    omega
  · have := Nat.sqrt_le_self (k - 5); omega
  · have := Nat.lt_succ_sqrt (k - 5)
    have : k - 5 < (Nat.sqrt (k - 5) + 1) ^ 2 := by nlinarith
    omega

end UnitSquarePacking.Ryu
