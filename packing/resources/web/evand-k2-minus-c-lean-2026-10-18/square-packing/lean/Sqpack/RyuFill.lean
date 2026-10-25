import Sqpack.RyuBound

/-!
# Ryu's L-shape with filled band ends: `c*(k) ≤ 4⌈√(2k − 7)⌉ + 5`

The "R1′" variant (`literature/waste-constructions-2026-10-17.md` §3, found by a literature-reading agent of this
repository on 2026-10-17): Ryu's L-shaped packing (`RyuBand.lpacking`) with `nf = ⌊b/2⌋ − 1` axis squares under the
first row and over the last row of each band (`RyuBand.band_fill`).  With `b ≈ √(2k)` each band holds `L − 3` rows
(`length_ok4`, valid for `2L ≤ b² + 7`), so the waste is `6b − 4 nf ≤ 4b + 6`, against `8b` with `b ≈ √k` in Ryu's
Theorem 1.4: about `4√2 √k ≈ 5.66 √k` instead of `8 √k`.

Both fill conditions reduce to `nf ≤ bγ − cot θ` (`fill_ok`), which at `t = 1/b` is `(b² − 1)²/(2b(b² + 1))`, about
`b/2`.
-/

namespace UnitSquarePacking.Ryu

open UnitSquarePacking.Conjectures

section angle
variable {b t : ℝ}

lemma length_ok4 {L K : ℝ} (hb : 2 ≤ b) (hL0 : 0 ≤ L) (hLb : 2 * L ≤ b ^ 2 + 7) (hLK : L ≤ K)
    (hK : 0 < K) (ht : t = 1 / b + 1 / ((b ^ 2 + 1) * (6 * K + 4 * b))) :
    (L - 4) * dd t + hh b t + (b - ww b t) ≤ L := by
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
  have slack : (L - 4) * (1 + 2 / (b ^ 2 - 1)) + (3 - 4 / D) ≤ L - 4 / D := by
    have : (L - 4) * (2 / (b ^ 2 - 1)) ≤ 1 := by
      rw [mul_div_assoc', div_le_iff₀ hb1]; linarith
    nlinarith
  -- the perturbation
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
    rw [← hδK]; nlinarith
  have hDp : 0 < 4 / D - 1 / D := by rw [← sub_div]; positivity
  linarith

/-- **The fill condition**: `(b − 2)/2 ≤ bγ − cot θ` for `t` just above `1/b`. -/
lemma fill_ok (hb : 2 ≤ b) (h1 : 1 / b ≤ t) (h2 : t ≤ 1 / b + 1 / 10) :
    (b - 2) / 2 ≤ b * ((1 - t ^ 2) / (1 + t ^ 2)) - (1 - t ^ 2) / (1 + t ^ 2) / (2 * t / (1 + t ^ 2)) := by
  have hb0 : 0 < b := by linarith
  have ht : 0 < t := lt_of_lt_of_le (by positivity) h1
  have a : 0 < 1 + t ^ 2 := by positivity
  have e : (1 - t ^ 2) / (1 + t ^ 2) / (2 * t / (1 + t ^ 2)) = (1 - t ^ 2) / (2 * t) := by
    field_simp
  rw [e]
  -- u = b t ∈ [1, 1.2]
  have hu1 : 1 ≤ b * t := by rwa [div_le_iff₀ hb0, mul_comm] at h1
  have hu2 : b * t ≤ 1 + b / 10 := by
    have := mul_le_mul_of_nonneg_left h2 hb0.le
    rw [mul_add, mul_div_cancel₀ _ hb0.ne'] at this; linarith
  have ht2 : t ≤ 3 / 5 := by
    have : 1 / b ≤ 1 / 2 := by rw [div_le_div_iff₀ hb0 (by norm_num)]; linarith
    linarith
  rw [div_le_iff₀ (by norm_num : (0 : ℝ) < 2)]
  rw [show (b * ((1 - t ^ 2) / (1 + t ^ 2)) - (1 - t ^ 2) / (2 * t)) * 2 =
      ((1 - t ^ 2) * (2 * b * t - 1 - t ^ 2)) / (t * (1 + t ^ 2)) by field_simp; ring]
  rw [le_div_iff₀ (by positivity)]
  nlinarith [mul_nonneg (by linarith : (0 : ℝ) ≤ b * t - 1) (by nlinarith : (0 : ℝ) ≤ 1 - t ^ 2),
    mul_nonneg hb0.le ht.le, mul_nonneg (mul_nonneg hb0.le ht.le) (sq_nonneg t), sq_nonneg t,
    mul_nonneg (sq_nonneg t) (sq_nonneg t), mul_nonneg ht.le (sq_nonneg t)]

end angle

/-- **The filled L-shape.**  For `2 ≤ b`, `b + 4 ≤ k`, `2k ≤ b² + 7`: `k² − 6b + 4(⌊b/2⌋ − 1)` unit squares pack in
a square of side `< k`. -/
theorem packs_fill (k b : ℕ) (hb : 2 ≤ b) (hkb : b + 4 ≤ k) (hk : 2 * k ≤ b ^ 2 + 7) :
    ∃ s < (k : ℝ), Packs (k * k - 6 * b + 4 * (b / 2 - 1)) s := by
  set t : ℝ := 1 / b + 1 / ((b ^ 2 + 1) * (6 * k + 4 * b)) with ht
  have hb' : (2 : ℝ) ≤ b := by exact_mod_cast hb
  have hb0 : (0 : ℝ) < b := by linarith
  have hk' : (b : ℝ) + 4 ≤ k := by exact_mod_cast hkb
  have hk2 : 2 * (k : ℝ) ≤ b ^ 2 + 7 := by exact_mod_cast hk
  have hK : (0 : ℝ) < k := by linarith
  have htpos : 0 < t := by rw [ht]; positivity
  have hδ : 1 / (((b : ℝ) ^ 2 + 1) * (6 * k + 4 * b)) ≤ 1 / 10 := by
    rw [div_le_div_iff₀ (by positivity) (by norm_num)]; nlinarith
  have ht1 : t < 1 := by
    have : 1 / (b : ℝ) ≤ 1 / 2 := by rw [div_le_div_iff₀ hb0 (by norm_num)]; linarith
    rw [ht]; linarith
  have hu : ((1 - t ^ 2) / (1 + t ^ 2)) ^ 2 + (2 * t / (1 + t ^ 2)) ^ 2 = 1 := by
    field_simp; ring
  obtain ⟨θ, hc, hs⟩ := exists_angle hu
  have hγ : 0 < Real.cos θ := by rw [hc]; apply div_pos <;> nlinarith
  have hσ : 0 < Real.sin θ := by rw [hs]; positivity
  have ed : 1 / Real.cos θ = dd t := by rw [hc, dd, one_div_div]
  have eh : (b : ℝ) * Real.sin θ + Real.cos θ = hh b t := by rw [hc, hs, hh]; field_simp; ring
  have ew : (b : ℝ) * Real.cos θ + Real.sin θ = ww b t := by rw [hc, hs, ww]; field_simp
  obtain ⟨r, rfl⟩ : ∃ r, k = b + 4 + r := ⟨k - (b + 4), by omega⟩
  have L1 := length_ok4 (b := (b : ℝ)) (t := t) (L := ((b + 4 + r : ℕ) : ℝ)) (K := ((b + 4 + r : ℕ) : ℝ)) hb'
    (by positivity) hk2 le_rfl hK ht
  have L2 := length_ok4 (b := (b : ℝ)) (t := t) (L := ((4 + r : ℕ) : ℝ)) (K := ((b + 4 + r : ℕ) : ℝ)) hb'
    (by positivity) (by push_cast at hk2 ⊢; linarith) (by push_cast; linarith) hK ht
  have hww : ww b t < b := w_lt hb0 (by
    have : (0 : ℝ) < 1 / ((b ^ 2 + 1) * (6 * ↑(b + 4 + r) + 4 * b)) := by positivity
    rw [ht]; linarith)
  have hpos' : (0 : ℝ) < 1 / ((b ^ 2 + 1) * (6 * ↑(b + 4 + r) + 4 * b)) := by positivity
  have hfill := fill_ok (b := (b : ℝ)) (t := t) hb' (by rw [ht]; linarith) (by rw [ht]; linarith [hδ])
  have hnf : ((b / 2 - 1 : ℕ) : ℝ) ≤ b * Real.cos θ - Real.cos θ / Real.sin θ := by
    have h2 : 2 * (b / 2 - 1) + 2 ≤ b := by omega
    have h2' : 2 * ((b / 2 - 1 : ℕ) : ℝ) + 2 ≤ b := by exact_mod_cast h2
    rw [hc, hs]; linarith
  have P := lpacking_fill hγ hσ (4 + r) b (b + 1 + r) (1 + r) (b / 2 - 1) (by omega) ?_ ?_ hnf
  · refine ⟨((4 + r : ℕ) : ℝ) + (b * Real.cos θ + Real.sin θ), ?_, ?_⟩
    · rw [ew]; push_cast; linarith
    · have : (b + 4 + r) * (b + 4 + r) - 6 * b + 4 * (b / 2 - 1) =
          (4 + r) * (4 + r) + ((b + 1 + r) * b + (b / 2 - 1) + (b / 2 - 1)) +
            ((1 + r) * b + (b / 2 - 1) + (b / 2 - 1)) := by
        have : 6 * b ≤ (b + 4 + r) * (b + 4 + r) := by nlinarith
        zify [this]; ring
      rw [this]; exact P
  · have key : (((b + 1 + r : ℕ) : ℝ) - 1) / Real.cos θ + b * Real.sin θ + Real.cos θ =
        (((b + 4 + r : ℕ) : ℝ) - 4) * dd t + hh b t := by
      rw [← eh, ← ed]; push_cast; ring
    rw [key, ew]
    push_cast at L1 ⊢
    linarith
  · have key : (((1 + r : ℕ) : ℝ) - 1) / Real.cos θ + b * Real.sin θ + Real.cos θ =
        (((4 + r : ℕ) : ℝ) - 4) * dd t + hh b t := by
      rw [← eh, ← ed]; push_cast; ring
    rw [key]
    push_cast at L2 ⊢
    linarith

/-- **`c*(k) ≤ 4⌈√(2k − 7)⌉ + 5`** for every `k ≥ 7`: `k² − (4b + 6)` unit squares pack in a square of side `< k`,
with `b = ⌈√(2k − 7)⌉ = Nat.sqrt (2k − 8) + 1`.  (Ryu's Theorem 1.4 gives `8⌈√(k − 4)⌉`.) -/
theorem packs_sub_4sqrt2 (k : ℕ) (hk : 7 ≤ k) :
    ∃ s < (k : ℝ), Packs (k * k - (4 * (Nat.sqrt (2 * k - 8) + 1) + 6)) s := by
  set b := Nat.sqrt (2 * k - 8) + 1 with hbd
  have hb : 2 ≤ b := by
    have : 1 ≤ Nat.sqrt (2 * k - 8) := Nat.le_sqrt.2 (by omega)
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
  obtain ⟨s, hs, hp⟩ := packs_fill k b hb hkb hk2
  refine ⟨s, hs, packs_of_le hp ?_⟩
  have : 2 * (b / 2) ≤ b := Nat.mul_div_le b 2
  omega

end UnitSquarePacking.Ryu
