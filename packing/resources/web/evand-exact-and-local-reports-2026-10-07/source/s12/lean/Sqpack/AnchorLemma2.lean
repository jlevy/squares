import Sqpack.D4

/-!
# Lemma 2 of `notes/clique-family.md`: the transversal threshold at a wall

Let `0 ≤ p_x < 1`, `0 ≤ ε ≤ 1 - p_x` and `ρ* = ε p_x / √(1 - p_x²)`.  The vertical segment
`A_ρ = {p_x + ε} × [p_y - ρ, p_y + ρ]` meets **every** closed unit square that lies in the
half-plane `x ≥ 0` and contains `p = (p_x, p_y)` iff `ρ ≥ ρ*`.

* `anchor_lemma2` — the "if" direction (the one that matters: `K(p, A_ρ) ⊇ P_p`).
* `anchor_lemma2_sharp` — the "only if" direction: for `ρ < ρ*` the square at angle
  `arccos p_x` with `p` at its corner `c + ½(e₁ + e₂)` touches the wall and misses `A_ρ`.
* `anchor_lemma2_iff` — both together.

Only the left wall `x ≥ 0` is used (the note's hypotheses are `0 < p_x`, `0 < ε < 1 - p_x` and
admissibility in a box `[0,t]²`, which implies the half-plane condition).

**Proof of the "if" direction** (not the note's separating-axis argument, but the same
inequalities).  Reduce `θ` mod `π/2` to `[0, π/2)`, so `c := cos θ > 0`, `s := sin θ ≥ 0`.
Write `s₁, s₂` for the square coordinates of `p`.  The point `(p_x + ε, p_y + t)` has square
coordinates `(s₁ + εc + ts, s₂ - εs + tc)`, so we need a `t ∈ [-ρ, ρ]` lying in the two
intervals `|s₁ + εc + ts| ≤ ½`, `|s₂ - εs + tc| ≤ ½`.  Three intervals on a line meet iff every
lower end is `≤` every upper end; of the nine comparisons, two are the note's cases `(1,+)` and
`(2,-)`, which reduce to the algebraic inequality `key` (the erratum's bound in `z = cos θ`),
and the rest are immediate.  The wall enters only through the corner `c + (-½, ½)` of the square,
giving `c_x ≥ (c + s)/2`.
-/

namespace SquarePacking

open Real

/-- Squares are `π/2`-periodic in the angle, for every integer multiple. -/
lemma sq_add_int_mul_pi_div_two (c : ℝ × ℝ) (θ L : ℝ) (k : ℤ) :
    sq c (θ + k * (π / 2)) L = sq c θ L := by
  induction k using Int.induction_on with
  | zero => simp
  | succ k ih =>
    have e : θ + ((k : ℤ) + 1 : ℤ) * (π / 2) = (θ + ((k : ℤ) : ℝ) * (π / 2)) + π / 2 := by
      push_cast; ring
    rw [e, sq_add_pi_div_two, ih]
  | pred k ih =>
    rw [← sq_add_pi_div_two]
    have e : θ + ((-(k : ℤ) - 1 : ℤ) : ℝ) * (π / 2) + π / 2
        = θ + ((-(k : ℤ) : ℤ) : ℝ) * (π / 2) := by
      push_cast; ring
    rw [e, ih]

/-- The algebraic core (cases `(1,+)` and `(2,-)` of the note, after the erratum).
With `S = √(1-a²)`, `ρ S ≥ ε a`, `0 ≤ ε ≤ 1-a` and a point `(z, w)` of the unit circle with
`a < z ≤ 1`, `w ≥ 0`: `a - z + ε z² ≤ ρ z w`. -/
lemma key {a ε ρ S z w : ℝ} (ha : 0 ≤ a) (hS : 0 < S) (hS2 : S ^ 2 = 1 - a ^ 2)
    (hε0 : 0 ≤ ε) (hε : ε ≤ 1 - a) (hρ : ε * a ≤ ρ * S) (hz : a < z) (hz1 : z ≤ 1)
    (hw : 0 ≤ w) (hzw : z ^ 2 + w ^ 2 = 1) : a - z + ε * z ^ 2 ≤ ρ * z * w := by
  have hz0 : 0 < z := lt_of_le_of_lt ha hz
  set D := z * S - a * w with hDdef
  have hP : 0 < z * S + a * w := by positivity
  have hD : D * (z * S + a * w) = z ^ 2 - a ^ 2 := by
    rw [hDdef]; linear_combination z ^ 2 * hS2 - a ^ 2 * hzw
  have hza : 0 < z ^ 2 - a ^ 2 := by nlinarith
  have hD0 : 0 ≤ D := by
    by_contra h
    push Not at h
    nlinarith
  -- `(1-a) z D ≤ (z-a) S`, multiplied out by `zS + aw > 0`
  have h1 : (1 - a) * z * D ≤ (z - a) * S := by
    have hm : (1 - a) * z * D * (z * S + a * w) ≤ (z - a) * S * (z * S + a * w) := by
      have e1 : (1 - a) * z * D * (z * S + a * w) = (1 - a) * z * (z ^ 2 - a ^ 2) := by
        rw [mul_assoc, hD]
      have e2 : (z - a) * S * (z * S + a * w)
          = (z - a) * z * (1 - a ^ 2) + (z - a) * a * S * w := by
        linear_combination (z - a) * z * hS2
      rw [e1, e2]
      have : 0 ≤ (z - a) * a * S * w := by
        have : 0 ≤ z - a := by linarith
        positivity
      have : 0 ≤ (z - a) * z * (1 - a) * (1 - z) := by
        have : 0 ≤ z - a := by linarith
        have : 0 ≤ 1 - a := by linarith
        have : 0 ≤ 1 - z := by linarith
        positivity
      nlinarith
    exact le_of_mul_le_mul_right hm hP
  have h2 : ε * z * D ≤ (1 - a) * z * D := by
    have : 0 ≤ z * D := mul_nonneg hz0.le hD0
    nlinarith
  -- multiply the goal by `S > 0`
  have h3 : ε * a * z * w ≤ ρ * S * z * w := by
    have : 0 ≤ z * w := mul_nonneg hz0.le hw
    nlinarith
  have hm : (a - z + ε * z ^ 2) * S ≤ ρ * z * w * S := by
    have e : (a - z + ε * z ^ 2) * S = -((z - a) * S) + ε * z * D + ε * a * z * w := by
      rw [hDdef]; ring
    rw [e]; nlinarith
  exact le_of_mul_le_mul_right hm hS

/-- The angle-free form of the "if" direction: with `c = cos θ > 0`, `s = sin θ ≥ 0` and the
square coordinates `s₁, s₂` of `p`, there is an admissible offset `t ∈ [-ρ, ρ]`. -/
lemma core {px ε ρ S c s s1 s2 : ℝ} (hpx0 : 0 ≤ px) (hS : 0 < S) (hS2 : S ^ 2 = 1 - px ^ 2)
    (hε0 : 0 ≤ ε) (hε1 : ε ≤ 1 - px) (hρS : ε * px ≤ ρ * S) (hc : 0 < c) (hs : 0 ≤ s)
    (hcs : c ^ 2 + s ^ 2 = 1) (h1 : |s1| ≤ 1 / 2) (h2 : |s2| ≤ 1 / 2)
    (hadm : (c + s) / 2 ≤ px - s1 * c + s2 * s) :
    ∃ t, |t| ≤ ρ ∧ |s1 + ε * c + t * s| ≤ 1 / 2 ∧ |s2 - ε * s + t * c| ≤ 1 / 2 := by
  rw [abs_le] at h1 h2
  have hρ0 : 0 ≤ ρ := by
    have : 0 ≤ ρ * S := le_trans (mul_nonneg hε0 hpx0) hρS
    exact nonneg_of_mul_nonneg_left this hS
  have hc1 : c ≤ 1 := by nlinarith [sq_nonneg s]
  have hs1 : s ≤ 1 := by nlinarith [sq_nonneg c]
  have hw1 : 1 ≤ c + s := by
    nlinarith [mul_nonneg hc.le (sub_nonneg.2 hc1), mul_nonneg hs (sub_nonneg.2 hs1)]
  -- products used below
  have hεc : 0 ≤ ε * c := mul_nonneg hε0 hc.le
  have hεs : 0 ≤ ε * s := mul_nonneg hε0 hs
  have hρc : 0 ≤ ρ * c := mul_nonneg hρ0 hc.le
  have hρs : 0 ≤ ρ * s := mul_nonneg hρ0 hs
  have hs1c : -(1 / 2) * c ≤ s1 * c := mul_le_mul_of_nonneg_right h1.1 hc.le
  have hs1c' : s1 * c ≤ 1 / 2 * c := mul_le_mul_of_nonneg_right h1.2 hc.le
  have hs2s : -(1 / 2) * s ≤ s2 * s := mul_le_mul_of_nonneg_right h2.1 hs
  have hs2s' : s2 * s ≤ 1 / 2 * s := mul_le_mul_of_nonneg_right h2.2 hs
  have hεcs : ε * c ^ 2 + ε * s ^ 2 = ε := by rw [← mul_add, hcs, mul_one]
  -- case (1,+)
  have H1p : s1 + ε * c - 1 / 2 ≤ ρ * s := by
    rcases le_or_gt c px with hcp | hcp
    · have hsS : S ≤ s := by
        have hcc : c ^ 2 ≤ px ^ 2 := pow_le_pow_left₀ hc.le hcp 2
        exact (pow_le_pow_iff_left₀ hS.le hs two_ne_zero).mp (by linarith)
      have := mul_le_mul_of_nonneg_left hcp hε0
      have := mul_le_mul_of_nonneg_left hsS hρ0
      linarith
    · have hk := key hpx0 hS hS2 hε0 hε1 hρS hcp hc1 hs hcs
      have : c * (s1 + ε * c - 1 / 2) ≤ c * (ρ * s) := by
        have e1 : c * (s1 + ε * c - 1 / 2) = s1 * c + ε * c ^ 2 - c / 2 := by ring
        have e2 : c * (ρ * s) = ρ * c * s := by ring
        rw [e1, e2]; linarith
      exact le_of_mul_le_mul_left this hc
  -- case (2,-)
  have H2m : -(1 / 2) - s2 + ε * s ≤ ρ * c := by
    rcases le_or_gt s px with hsp | hsp
    · have hcS : S ≤ c := by
        have hss : s ^ 2 ≤ px ^ 2 := pow_le_pow_left₀ hs hsp 2
        exact (pow_le_pow_iff_left₀ hS.le hc.le two_ne_zero).mp (by linarith)
      have := mul_le_mul_of_nonneg_left hsp hε0
      have := mul_le_mul_of_nonneg_left hcS hρ0
      linarith
    · have hk := key hpx0 hS hS2 hε0 hε1 hρS hsp hs1 hc.le (by linarith)
      have hs0 : 0 < s := lt_of_le_of_lt hpx0 hsp
      have : s * (-(1 / 2) - s2 + ε * s) ≤ s * (ρ * c) := by
        have e1 : s * (-(1 / 2) - s2 + ε * s) = -(s / 2) - s2 * s + ε * s ^ 2 := by ring
        have e2 : s * (ρ * c) = ρ * s * c := by ring
        rw [e1, e2]; linarith
      exact le_of_mul_le_mul_left this hs0
  -- the easy cases (1,-), (2,+) and the two cross conditions (the axis `e_x`)
  have H1m : -(1 / 2) - s1 - ε * c ≤ ρ * s := by linarith
  have H2p : s2 - ε * s - 1 / 2 ≤ ρ * c := by linarith
  have X1 : (-(1 / 2) - (s1 + ε * c)) * c ≤ (1 / 2 - (s2 - ε * s)) * s := by
    have e1 : (-(1 / 2) - (s1 + ε * c)) * c = -(c / 2) - s1 * c - ε * c ^ 2 := by ring
    have e2 : (1 / 2 - (s2 - ε * s)) * s = s / 2 - s2 * s + ε * s ^ 2 := by ring
    rw [e1, e2]; nlinarith [sq_nonneg c, sq_nonneg s]
  have X2 : (-(1 / 2) - (s2 - ε * s)) * s ≤ (1 / 2 - (s1 + ε * c)) * c := by
    have e1 : (-(1 / 2) - (s2 - ε * s)) * s = -(s / 2) - s2 * s + ε * s ^ 2 := by ring
    have e2 : (1 / 2 - (s1 + ε * c)) * c = c / 2 - s1 * c - ε * c ^ 2 := by ring
    rw [e1, e2]; linarith
  rcases eq_or_lt_of_le hs with hs0 | hs0
  · -- `θ = 0`: `s = 0`, `c = 1`
    have hc1' : c = 1 := by
      rw [← hs0] at hcs; nlinarith
    rw [← hs0, hc1'] at H1p H2m H2p ⊢
    simp only [mul_zero, add_zero, sub_zero, mul_one] at H1p H2m H2p ⊢
    refine ⟨max (-ρ) (-(1 / 2) - s2), ?_, ?_, ?_⟩
    · rw [abs_le]; constructor
      · exact le_max_left _ _
      · exact max_le (by linarith) (by linarith)
    · rw [abs_le]; constructor <;> linarith
    · rw [abs_le]; constructor
      · have := le_max_right (-ρ) (-(1 / 2) - s2); linarith
      · have : max (-ρ) (-(1 / 2) - s2) ≤ 1 / 2 - s2 := max_le (by linarith) (by linarith)
        linarith
  · set a1 := s1 + ε * c
    set a2 := s2 - ε * s
    set t := max (-ρ) (max ((-(1 / 2) - a1) / s) ((-(1 / 2) - a2) / c)) with ht
    have hl0 : -ρ ≤ t := le_max_left _ _
    have hl1 : (-(1 / 2) - a1) / s ≤ t := le_trans (le_max_left _ _) (le_max_right _ _)
    have hl2 : (-(1 / 2) - a2) / c ≤ t := le_trans (le_max_right _ _) (le_max_right _ _)
    have hu0 : t ≤ ρ := max_le (by linarith) (max_le
      (by rw [div_le_iff₀ hs0]; linarith) (by rw [div_le_iff₀ hc]; linarith))
    have hu1 : t ≤ (1 / 2 - a1) / s := max_le (by rw [le_div_iff₀ hs0]; linarith) (max_le
      (div_le_div_of_nonneg_right (by linarith) hs0.le)
      (by rw [div_le_div_iff₀ hc hs0]; linarith))
    have hu2 : t ≤ (1 / 2 - a2) / c := max_le (by rw [le_div_iff₀ hc]; linarith) (max_le
      (by rw [div_le_div_iff₀ hs0 hc]; linarith)
      (div_le_div_of_nonneg_right (by linarith) hc.le))
    rw [div_le_iff₀ hs0] at hl1
    rw [div_le_iff₀ hc] at hl2
    rw [le_div_iff₀ hs0] at hu1
    rw [le_div_iff₀ hc] at hu2
    refine ⟨t, abs_le.mpr ⟨by linarith, hu0⟩, abs_le.mpr ⟨by linarith, by linarith⟩,
      abs_le.mpr ⟨by linarith, by linarith⟩⟩

/-- **Lemma 2, "if" direction.**  Let `0 ≤ p_x < 1`, `0 ≤ ε ≤ 1 - p_x` and
`ρ ≥ ε p_x / √(1 - p_x²)`.  Every closed unit square in the half-plane `x ≥ 0` that contains
`p = (p_x, p_y)` meets the vertical segment `{p_x + ε} × [p_y - ρ, p_y + ρ]`. -/
theorem anchor_lemma2 {px py ε ρ : ℝ} (hpx0 : 0 ≤ px) (hpx1 : px < 1) (hε0 : 0 ≤ ε)
    (hε1 : ε ≤ 1 - px) (hρ : ε * px / √(1 - px ^ 2) ≤ ρ)
    (c : ℝ × ℝ) (θ : ℝ) (hwall : sq c θ 1 ⊆ {q | 0 ≤ q.1}) (hp : (px, py) ∈ sq c θ 1) :
    (sq c θ 1 ∩ {q | q.1 = px + ε ∧ |q.2 - py| ≤ ρ}).Nonempty := by
  -- reduce the angle to `[0, π/2)`
  have hpi : (0 : ℝ) < π / 2 := by positivity
  have heq := toIcoMod_add_toIcoDiv_zsmul hpi 0 θ
  rw [zsmul_eq_mul] at heq
  have hmem := toIcoMod_mem_Ico' hpi θ
  set θ' := toIcoMod hpi 0 θ
  rw [← heq, sq_add_int_mul_pi_div_two] at hwall hp ⊢
  set co := cos θ' with hco
  set si := sin θ' with hsi
  have hc : 0 < co := cos_pos_of_mem_Ioo ⟨by linarith [hmem.1, pi_pos], hmem.2⟩
  have hs : 0 ≤ si := sin_nonneg_of_nonneg_of_le_pi hmem.1 (by linarith [hmem.2, pi_pos])
  have hcs : co ^ 2 + si ^ 2 = 1 := by rw [hco, hsi, add_comm]; exact sin_sq_add_cos_sq θ'
  -- the square coordinates of `p`
  set s1 := (coord c θ' (px, py)).1 with hs1
  set s2 := (coord c θ' (px, py)).2 with hs2
  have hp1 : |s1| ≤ 1 / 2 := hp.1
  have hp2 : |s2| ≤ 1 / 2 := hp.2
  have hcx : c.1 = px - s1 * co + s2 * si := by
    simp only [hs1, hs2, coord]; linear_combination (px - c.1) * hcs
  -- the wall, through the corner `c + (-½)e₁ + ½e₂`
  have hcorner : (c.1 - (co + si) / 2, c.2 + (co - si) / 2) ∈ sq c θ' 1 := by
    have e1 : (coord c θ' (c.1 - (co + si) / 2, c.2 + (co - si) / 2)).1 = -(1 / 2) := by
      simp only [coord]; linear_combination (-(1 / 2) : ℝ) * hcs
    have e2 : (coord c θ' (c.1 - (co + si) / 2, c.2 + (co - si) / 2)).2 = 1 / 2 := by
      simp only [coord]; linear_combination (1 / 2 : ℝ) * hcs
    change |_| ≤ 1 / 2 ∧ |_| ≤ 1 / 2
    rw [e1, e2]; norm_num
  have hwc : (0 : ℝ) ≤ c.1 - (co + si) / 2 := hwall hcorner
  have hadm : (co + si) / 2 ≤ px - s1 * co + s2 * si := by linarith
  -- the threshold
  have h1p : 0 < 1 - px ^ 2 := by nlinarith
  have hS : 0 < √(1 - px ^ 2) := sqrt_pos.mpr h1p
  have hS2 : √(1 - px ^ 2) ^ 2 = 1 - px ^ 2 := sq_sqrt h1p.le
  have hρS : ε * px ≤ ρ * √(1 - px ^ 2) := (div_le_iff₀ hS).mp hρ
  obtain ⟨t, ht0, ht1, ht2⟩ := core hpx0 hS hS2 hε0 hε1 hρS hc hs hcs hp1 hp2 hadm
  refine ⟨(px + ε, py + t), ?_, rfl, by simpa using ht0⟩
  have e1 : (coord c θ' (px + ε, py + t)).1 = s1 + ε * co + t * si := by
    simp only [hs1, coord]; ring
  have e2 : (coord c θ' (px + ε, py + t)).2 = s2 - ε * si + t * co := by
    simp only [hs2, coord]; ring
  change |_| ≤ 1 / 2 ∧ |_| ≤ 1 / 2
  rw [e1, e2]; exact ⟨ht1, ht2⟩

/-- **Lemma 2, "only if" direction (sharpness).**  If `0 ≤ p_x < 1` and `ρ < ε p_x / √(1-p_x²)`,
the unit square at angle `arccos p_x` having `p` as its corner `c + ½(e₁ + e₂)` lies in `x ≥ 0`
(it touches the wall), contains `p`, and misses the segment. -/
theorem anchor_lemma2_sharp {px py ε ρ : ℝ} (hpx0 : 0 ≤ px) (hpx1 : px < 1)
    (hρ : ρ < ε * px / √(1 - px ^ 2)) :
    ∃ (c : ℝ × ℝ) (θ : ℝ), sq c θ 1 ⊆ {q | 0 ≤ q.1} ∧ (px, py) ∈ sq c θ 1 ∧
      sq c θ 1 ∩ {q | q.1 = px + ε ∧ |q.2 - py| ≤ ρ} = ∅ := by
  have h1p : 0 < 1 - px ^ 2 := by nlinarith
  set S := √(1 - px ^ 2) with hSdef
  have hS : 0 < S := sqrt_pos.mpr h1p
  have hS2 : S ^ 2 = 1 - px ^ 2 := sq_sqrt h1p.le
  have hρS : ρ * S < ε * px := (lt_div_iff₀ hS).mp hρ
  have hcos : cos (arccos px) = px := cos_arccos (by linarith) hpx1.le
  have hsin : sin (arccos px) = S := sin_arccos px
  refine ⟨(px - px / 2 + S / 2, py - S / 2 - px / 2), arccos px, ?_, ?_, ?_⟩
  · rintro q ⟨hu, hv⟩
    simp only [coord, hcos, hsin] at hu hv
    rw [abs_le] at hu hv
    change 0 ≤ q.1
    have e : q.1 = (px - px / 2 + S / 2) + ((q.1 - (px - px / 2 + S / 2)) * px
        + (q.2 - (py - S / 2 - px / 2)) * S) * px
        - (-(q.1 - (px - px / 2 + S / 2)) * S + (q.2 - (py - S / 2 - px / 2)) * px) * S := by
      linear_combination (-(q.1 - (px - px / 2 + S / 2))) * hS2
    rw [e]
    nlinarith
  · change |_| ≤ 1 / 2 ∧ |_| ≤ 1 / 2
    simp only [coord, hcos, hsin]
    constructor <;> rw [abs_le] <;> constructor <;> nlinarith
  · ext q
    simp only [Set.mem_inter_iff, Set.mem_ofPred_eq, Set.mem_empty_iff_false, iff_false]
    rintro ⟨⟨hu, -⟩, hq1, hq2⟩
    simp only [coord, hcos, hsin, hq1] at hu
    rw [abs_le] at hu hq2
    have : 1 / 2 < (px + ε - (px - px / 2 + S / 2)) * px + (q.2 - (py - S / 2 - px / 2)) * S := by
      nlinarith
    linarith [hu.2]

/-- **Lemma 2 of `notes/clique-family.md`** (with the half-plane `x ≥ 0` as the only admissibility
constraint): for `0 ≤ p_x < 1` and `0 ≤ ε ≤ 1 - p_x`, the segment
`{p_x + ε} × [p_y - ρ, p_y + ρ]` is a transversal of the unit squares in `x ≥ 0` through `p` iff
`ρ ≥ ε p_x / √(1 - p_x²)`. -/
theorem anchor_lemma2_iff {px py ε ρ : ℝ} (hpx0 : 0 ≤ px) (hpx1 : px < 1) (hε0 : 0 ≤ ε)
    (hε1 : ε ≤ 1 - px) :
    (∀ (c : ℝ × ℝ) (θ : ℝ), sq c θ 1 ⊆ {q | 0 ≤ q.1} → (px, py) ∈ sq c θ 1 →
      (sq c θ 1 ∩ {q | q.1 = px + ε ∧ |q.2 - py| ≤ ρ}).Nonempty) ↔
    ε * px / √(1 - px ^ 2) ≤ ρ := by
  constructor
  · intro h
    by_contra hlt
    push Not at hlt
    obtain ⟨c, θ, hw, hp, he⟩ := anchor_lemma2_sharp (py := py) hpx0 hpx1 hlt
    exact (h c θ hw hp).ne_empty he
  · intro hρ c θ hw hp
    exact anchor_lemma2 hpx0 hpx1 hε0 hε1 hρ c θ hw hp

end SquarePacking
