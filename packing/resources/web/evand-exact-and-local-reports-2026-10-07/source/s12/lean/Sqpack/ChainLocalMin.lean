import Sqpack.LocalMin

/-!
# Local minima held by a band of squares (integer side)

**Band lemma.**  If a horizontal line `y = y₀` meets `k` squares of a packing in `[0, s]²`, each nearly
axis-parallel (angle `δ` mod 90°) with its centre close enough to the line
(`|y₀ - b| / cos δ + |sin δ| / 2 < 1/2`), then `k ≤ s`.

Proof: each such square contains the closed horizontal unit segment centred at `x_m = a - (y₀ - b) tan δ`
on the line, with its open part in the interior (`band_chord`).  Disjoint interiors force the centres `x_m` of
different squares to be at least `1` apart, and the container forces `x_m ∈ [1/2, s - 1/2]`; `k` points of
`[1/2, s - 1/2]` that are pairwise `≥ 1` apart need `s - 1 ≥ k - 1` (`card_le_of_sep`, via `⌊x_m - 1/2⌋₊`).
No contacts, multipliers or field arithmetic.

**Local minimum** (`isLocalMin_of_band`): if the record has side `k` and `k` axis-parallel squares whose centres
lie within `1/2 - m` of one horizontal line (`m > 0`; an aligned row has `m = 1/2`, a *staggered* row needs a
vertical spread `< 1`), then every packing within `ε = m/2` in pose space has side `≥ k`.

**Certificates** (`isLocalMin_of_axisCert`): an axis-parallel rational record `P` (all angles `0`), checked by
`axisOK` (squares in `[0, k]²`, pairs separated along `x` or `y`), and a band (`bandOK`: `k` distinct indices,
centres within `1/2 - m` of `y₀`).  Both checks are decidable rational arithmetic (`decide +kernel`).
-/

namespace UnitSquarePacking

open Set Real

/-! ## The chord through a nearly axis-parallel square -/

/-- A square at angle `δ` (`cos δ > 0`) whose centre is close to the line `y = y₀` contains the closed unit
segment of that line centred at `x_m = a - (y₀ - b) sin δ / cos δ`, and its interior contains the open one. -/
lemma band_chord {a b δ y0 : ℝ} (hc : 0 < Real.cos δ)
    (hd : |y0 - b| / Real.cos δ + |Real.sin δ| / 2 < 1 / 2) (u : ℝ) :
    (|u| ≤ 1 / 2 → (a - (y0 - b) * Real.sin δ / Real.cos δ + u, y0) ∈ unitSq (a, b) δ) ∧
    (|u| < 1 / 2 → (a - (y0 - b) * Real.sin δ / Real.cos δ + u, y0) ∈ interior (unitSq (a, b) δ)) := by
  set C := Real.cos δ
  set S := Real.sin δ
  set d := y0 - b
  have hC1 : C ≤ 1 := Real.cos_le_one δ
  have hCS : C ^ 2 + S ^ 2 = 1 := by rw [add_comm]; exact Real.sin_sq_add_cos_sq δ
  -- the two rotated coordinates of the point
  have e1 : (a - d * S / C + u - a) * C + (y0 - b) * S = u * C := by
    simp only [d]; field_simp; ring
  have e2 : -(a - d * S / C + u - a) * S + (y0 - b) * C = d / C - u * S := by
    calc -(a - d * S / C + u - a) * S + (y0 - b) * C = d * (C ^ 2 + S ^ 2) / C - u * S := by
          simp only [d]; field_simp; ring
      _ = d / C - u * S := by rw [hCS, mul_one]
  have hdC : |d / C| = |d| / C := by rw [abs_div, abs_of_pos hc]
  have b1 : ∀ v, |v| ≤ 1 / 2 → |v * C| ≤ |v| := fun v _ => by
    rw [abs_mul, abs_of_pos hc]; nlinarith [abs_nonneg v]
  have b2 : ∀ v, |v| ≤ 1 / 2 → |d / C - v * S| < 1 / 2 := fun v hv => by
    calc |d / C - v * S| ≤ |d / C| + |v * S| := abs_sub _ _
      _ = |d| / C + |v| * |S| := by rw [hdC, abs_mul]
      _ ≤ |d| / C + 1 / 2 * |S| := by gcongr
      _ < 1 / 2 := by linarith
  constructor
  · intro hu
    rw [unitSq_eq_setOf]
    simp only [mem_ofPred_eq]
    rw [e1, e2]
    exact ⟨(b1 u hu).trans hu, (b2 u hu).le⟩
  · intro hu
    rw [interior_unitSq]
    simp only [mem_ofPred_eq]
    rw [e1, e2]
    exact ⟨(b1 u hu.le).trans_lt hu, b2 u hu.le⟩

/-! ## Counting separated points -/

/-- `k` points of `[a, b]` pairwise at least `1` apart: `k ≤ b - a + 1`. -/
lemma card_le_of_sep {k : ℕ} (t : Fin k → ℝ) {a b : ℝ} (hab : ∀ i, a ≤ t i ∧ t i ≤ b)
    (hsep : ∀ i j, i ≠ j → 1 ≤ |t i - t j|) (hk : 0 < k) : (k : ℝ) ≤ b - a + 1 := by
  have hba : 0 ≤ b - a := by have := hab ⟨0, hk⟩; linarith [this.1, this.2]
  set f : Fin k → ℕ := fun i => ⌊t i - a⌋₊
  have hmaps : ∀ i ∈ (Finset.univ : Finset (Fin k)), f i ∈ Finset.range (⌊b - a⌋₊ + 1) := by
    intro i _
    rw [Finset.mem_range, Nat.lt_succ_iff]
    exact Nat.floor_le_floor (by linarith [(hab i).2])
  have hinj : Set.InjOn f (Finset.univ : Finset (Fin k)) := by
    intro i _ j _ hij
    by_contra hne
    -- the lower point is at least `1` below the other: its floor is smaller
    have key : ∀ i j, t i + 1 ≤ t j → f i ≠ f j := by
      intro i j h
      have h0 : 0 ≤ t i - a := by linarith [(hab i).1]
      have : ⌊t i - a + 1⌋₊ ≤ ⌊t j - a⌋₊ := Nat.floor_le_floor (by linarith)
      rw [Nat.floor_add_one h0] at this
      simp only [f]; omega
    rcases le_abs'.1 (hsep i j hne) with h | h
    · exact key i j (by linarith) hij
    · exact key j i (by linarith) hij.symm
  have hcard := Finset.card_le_card_of_injOn f hmaps hinj
  rw [Finset.card_univ, Fintype.card_fin, Finset.card_range] at hcard
  have hcast : (k : ℝ) ≤ (⌊b - a⌋₊ : ℝ) + 1 := by exact_mod_cast hcard
  linarith [Nat.floor_le hba]

/-! ## The band lemma -/

/-- **Band lemma.**  `k` distinct squares of a packing in `[0, s]²` (indices `e`), each equal as a set to a square
at an angle `δ i` with `cos (δ i) > 0` and its centre close to the line `y = y₀`, force `k ≤ s`. -/
theorem le_side_of_band {n k : ℕ} {s : ℝ} {c : Fin n → ℝ × ℝ} {θ : Fin n → ℝ} (hP : IsPacking n s c θ)
    (e : Fin k → Fin n) (he : Function.Injective e) (hk : 0 < k) (y0 : ℝ) (δ : Fin k → ℝ)
    (hδ : ∀ i, unitSq (c (e i)) (θ (e i)) = unitSq (c (e i)) (δ i))
    (hcos : ∀ i, 0 < Real.cos (δ i))
    (hnear : ∀ i, |y0 - (c (e i)).2| / Real.cos (δ i) + |Real.sin (δ i)| / 2 < 1 / 2) :
    (k : ℝ) ≤ s := by
  set t : Fin k → ℝ := fun i =>
    (c (e i)).1 - (y0 - (c (e i)).2) * Real.sin (δ i) / Real.cos (δ i) with ht
  have chord := fun i u => band_chord (a := (c (e i)).1) (hcos i) (hnear i) u
  -- the closed segment lies in the container
  have hin : ∀ i, 1 / 2 ≤ t i ∧ t i ≤ s - 1 / 2 := by
    intro i
    have hsub : unitSq (c (e i)) (δ i) ⊆ container s := by rw [← hδ i]; exact hP.1 (e i)
    have hl := hsub ((chord i (-1 / 2)).1 (by norm_num [abs_of_neg]))
    have hr := hsub ((chord i (1 / 2)).1 (by norm_num [abs_of_pos]))
    simp only [container, mem_prod, mem_Icc] at hl hr
    constructor <;> simp only [t] <;> linarith [hl.1.1, hr.1.2]
  -- disjoint interiors: centres of the open segments at least `1` apart
  have hsep : ∀ i j, i ≠ j → 1 ≤ |t i - t j| := by
    intro i j hij
    by_contra hlt
    push Not at hlt
    have hd : Disjoint (interior (unitSq (c (e i)) (θ (e i)))) (interior (unitSq (c (e j)) (θ (e j)))) :=
      hP.2 (he.ne hij)
    rw [hδ i, hδ j] at hd
    set x := (t i + t j) / 2
    have hi := (chord i (x - t i)).2 (by
      rw [show x - t i = (t j - t i) / 2 by simp only [x]; ring, abs_div, abs_sub_comm]; norm_num; linarith)
    have hj := (chord j (x - t j)).2 (by
      rw [show x - t j = (t i - t j) / 2 by simp only [x]; ring, abs_div]; norm_num; linarith)
    have ei : (c (e i)).1 - (y0 - (c (e i)).2) * Real.sin (δ i) / Real.cos (δ i) + (x - t i) = x := by
      simp only [t]; ring
    have ej : (c (e j)).1 - (y0 - (c (e j)).2) * Real.sin (δ j) / Real.cos (δ j) + (x - t j) = x := by
      simp only [t]; ring
    rw [ei, Prod.mk.eta] at hi
    rw [ej, Prod.mk.eta] at hj
    exact Set.disjoint_left.1 hd hi hj
  have := card_le_of_sep t hin hsep hk
  linarith

/-! ## Local minimality -/

/-- **Local minimum from a band.**  A packing in `[0, k]²` with `k` distinct axis-parallel squares (angle `0`)
whose centres lie within `1/2 - m` of the line `y = y₀` (`0 < m ≤ 1/2`) is a local minimum: every packing whose
squares are within `m / 2` of these (centres and angles mod 90°) has side `≥ k`. -/
theorem isLocalMin_of_band {n k : ℕ} {c : Fin n → ℝ × ℝ} {θ : Fin n → ℝ} (hP : IsPacking n k c θ)
    (e : Fin k → Fin n) (he : Function.Injective e) (hk : 0 < k) (y0 m : ℝ) (hm : 0 < m) (hm1 : m ≤ 1 / 2)
    (hθ : ∀ i, θ (e i) = 0) (hy : ∀ i, |(c (e i)).2 - y0| ≤ 1 / 2 - m) :
    IsLocalMinPacking n k c θ := by
  refine ⟨hP, m / 2, by linarith, fun s c' θ' hP' hnear => ?_⟩
  -- per band square: the angle mod 90°, and the centre height
  have hang : ∀ i, ∃ δ, unitSq (c' (e i)) (θ' (e i)) = unitSq (c' (e i)) δ ∧ |δ| < m / 2 := by
    intro i
    obtain ⟨q, hq⟩ := (hnear (e i)).2.2
    rw [hθ i, sub_zero] at hq
    refine ⟨θ' (e i) - q * (π / 2), ?_, hq⟩
    rw [← unitSq_add_int_mul (c' (e i)) (θ' (e i) - q * (π / 2)) q, sub_add_cancel]
  choose δ hδ hδm using hang
  have hδ1 : ∀ i, |δ i| ≤ 1 / 4 := fun i => by linarith [hδm i]
  have hcos : ∀ i, 1 - 1 / 32 ≤ Real.cos (δ i) := fun i => by
    have h1 := Real.one_sub_sq_div_two_le_cos (x := δ i)
    have : δ i ^ 2 ≤ 1 / 16 := by
      rw [← sq_abs]; nlinarith [abs_nonneg (δ i), hδ1 i]
    linarith
  refine le_side_of_band hP' e he hk y0 δ hδ (fun i => by linarith [hcos i]) (fun i => ?_)
  -- `|y₀ - b'| < 1/2 - m/2 ≤ cos δ (1 - |sin δ|) / 2`
  have hs : |Real.sin (δ i)| ≤ |δ i| := Real.abs_sin_le_abs
  have hC := hcos i
  have hC1 : Real.cos (δ i) ≤ 1 := Real.cos_le_one _
  have hcos2 : 1 - |δ i| ^ 2 / 2 ≤ Real.cos (δ i) := by
    rw [sq_abs]; exact Real.one_sub_sq_div_two_le_cos
  have hb : |y0 - (c' (e i)).2| < 1 / 2 - m / 2 := by
    have h1 := abs_le.1 (hy i)
    have h2 := abs_lt.1 (hnear (e i)).2.1
    rw [abs_lt]; constructor <;> linarith [h1.1, h1.2, h2.1, h2.2]
  have hpos : 0 < Real.cos (δ i) := by linarith
  rw [div_add' _ _ _ hpos.ne', div_lt_iff₀ hpos]
  have hδ0 := abs_nonneg (δ i)
  have hδm' := hδm i
  -- cos δ (1 - |sin δ|) ≥ (1 - δ²/2)(1 - |δ|) ≥ 1 - m/2 - m²/8 ≥ 1 - m
  nlinarith [mul_le_mul_of_nonneg_right hs (le_of_lt hpos), abs_nonneg (Real.sin (δ i))]

/-! ## Certificates: rational axis-parallel records -/

/-- The record's centres as reals (`P[i]`, `(0, 0)` past the end). -/
def cenOf (P : List (ℚ × ℚ)) (i : ℕ) : ℝ × ℝ := (((P.getD i 0).1 : ℚ), ((P.getD i 0).2 : ℚ))

/-- An axis-parallel square at `p` lies in `[0, S]²`. -/
def axisBoxOK (S : ℚ) (p : ℚ × ℚ) : Bool :=
  decide (1 / 2 ≤ p.1) && decide (p.1 ≤ S - 1 / 2) && decide (1 / 2 ≤ p.2) && decide (p.2 ≤ S - 1 / 2)

/-- Two axis-parallel squares are separated along `x` or along `y`. -/
def axisSepOK (p q : ℚ × ℚ) : Bool := decide (1 ≤ |p.1 - q.1|) || decide (1 ≤ |p.2 - q.2|)

/-- All pairs of a list. -/
def allPairs {α : Type*} (R : α → α → Bool) : List α → Bool
  | [] => true
  | p :: ps => ps.all (R p) && allPairs R ps

/-- An axis-parallel packing of `P.length` squares in `[0, S]²`. -/
def axisOK (S : ℚ) (P : List (ℚ × ℚ)) : Bool := P.all (axisBoxOK S) && allPairs axisSepOK P

/-- The band: `k` distinct indices `< n`, centres within `1/2 - m` of `y₀`, `0 < m ≤ 1/2`. -/
def bandOK (P : List (ℚ × ℚ)) (n k : ℕ) (band : List ℕ) (y0 m : ℚ) : Bool :=
  decide (band.length = k) && decide band.Nodup && band.all (fun j => decide (j < n)) &&
    band.all (fun j => decide (|(P.getD j 0).2 - y0| ≤ 1 / 2 - m)) && decide (0 < m) && decide (m ≤ 1 / 2) &&
    decide (0 < k)

lemma allPairs_pairwise {α : Type*} {R : α → α → Bool} {l : List α} (h : allPairs R l = true) :
    l.Pairwise fun a b => R a b = true := by
  induction l with
  | nil => exact List.Pairwise.nil
  | cons p ps ih =>
    simp only [allPairs, Bool.and_eq_true, List.all_eq_true] at h
    exact List.Pairwise.cons h.1 (ih h.2)

lemma unitSq_zero_sub {x y : ℝ} {p : ℝ × ℝ} (hp : p ∈ unitSq (x, y) 0) : |p.1 - x| ≤ 1 / 2 ∧ |p.2 - y| ≤ 1 / 2 := by
  rw [unitSq_eq_setOf] at hp
  simpa using hp

lemma interior_unitSq_zero {x y : ℝ} {p : ℝ × ℝ} (hp : p ∈ interior (unitSq (x, y) 0)) :
    |p.1 - x| < 1 / 2 ∧ |p.2 - y| < 1 / 2 := by
  rw [interior_unitSq] at hp
  simpa using hp

/-- `axisOK` is sound: the record is a packing (all angles `0`). -/
theorem isPacking_of_axisOK {n : ℕ} {S : ℚ} {P : List (ℚ × ℚ)} (hn : P.length = n) (h : axisOK S P = true) :
    IsPacking n S (fun i => cenOf P i) (fun _ => 0) := by
  simp only [axisOK, Bool.and_eq_true, List.all_eq_true] at h
  obtain ⟨hbox, hpair⟩ := h
  have hget : ∀ i : Fin n, P.getD i 0 = P[(i : ℕ)]'(by omega) := fun i => by
    rw [List.getD_eq_getElem]
  constructor
  · intro i p hp
    have hb := hbox _ (List.getElem_mem (show (i : ℕ) < P.length by omega))
    rw [← hget i] at hb
    simp only [axisBoxOK, Bool.and_eq_true, decide_eq_true_eq] at hb
    obtain ⟨⟨⟨h1, h2⟩, h3⟩, h4⟩ := hb
    have hp' := unitSq_zero_sub (x := ((P.getD i 0).1 : ℝ)) (y := ((P.getD i 0).2 : ℝ)) hp
    have h1' : ((1 / 2 : ℚ) : ℝ) ≤ ((P.getD i 0).1 : ℝ) := Rat.cast_le.2 h1
    have h2' : ((P.getD i 0).1 : ℝ) ≤ ((S - 1 / 2 : ℚ) : ℝ) := Rat.cast_le.2 h2
    have h3' : ((1 / 2 : ℚ) : ℝ) ≤ ((P.getD i 0).2 : ℝ) := Rat.cast_le.2 h3
    have h4' : ((P.getD i 0).2 : ℝ) ≤ ((S - 1 / 2 : ℚ) : ℝ) := Rat.cast_le.2 h4
    push_cast at h1' h2' h3' h4'
    simp only [container, mem_prod, mem_Icc]
    obtain ⟨a1, a2⟩ := abs_le.1 hp'.1
    obtain ⟨a3, a4⟩ := abs_le.1 hp'.2
    exact ⟨⟨by linarith, by linarith⟩, by linarith, by linarith⟩
  · -- pairs: separated along `x` or `y`
    have hpw := List.pairwise_iff_getElem.1 (allPairs_pairwise hpair)
    have key : ∀ i j : Fin n, (i : ℕ) < j → Disjoint (interior (unitSq (cenOf P i) 0))
        (interior (unitSq (cenOf P j) 0)) := by
      intro i j hij
      have hs := hpw i j (by omega) (by omega) hij
      rw [← hget i, ← hget j] at hs
      simp only [axisSepOK, Bool.or_eq_true, decide_eq_true_eq] at hs
      rw [Set.disjoint_left]
      intro p hpi hpj
      have hi := interior_unitSq_zero hpi
      have hj := interior_unitSq_zero hpj
      rcases hs with hs | hs
      · have hs' : (1 : ℝ) ≤ |((P.getD i 0).1 : ℝ) - ((P.getD j 0).1 : ℝ)| := by exact_mod_cast hs
        have a := abs_lt.1 hi.1
        have b := abs_lt.1 hj.1
        rcases le_abs'.1 hs' with h | h <;> linarith [a.1, a.2, b.1, b.2]
      · have hs' : (1 : ℝ) ≤ |((P.getD i 0).2 : ℝ) - ((P.getD j 0).2 : ℝ)| := by exact_mod_cast hs
        have a := abs_lt.1 hi.2
        have b := abs_lt.1 hj.2
        rcases le_abs'.1 hs' with h | h <;> linarith [a.1, a.2, b.1, b.2]
    intro i j hij
    rcases lt_or_gt_of_ne (Fin.val_ne_of_ne hij) with h | h
    · exact key i j h
    · exact (key j i h).symm

/-- **Certified local minimum** of an axis-parallel rational record with a band. -/
theorem isLocalMin_of_axisCert {n k : ℕ} (P : List (ℚ × ℚ)) (band : List ℕ) (y0 m : ℚ) (hn : P.length = n)
    (hP : axisOK k P = true) (hB : bandOK P n k band y0 m = true) :
    IsLocalMinPacking n k (fun i => cenOf P i) (fun _ => 0) := by
  simp only [bandOK, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true] at hB
  obtain ⟨⟨⟨⟨⟨⟨hlen, hnd⟩, hlt⟩, hy⟩, hm⟩, hm1⟩, hk⟩ := hB
  have hP' := isPacking_of_axisOK hn hP
  push_cast at hP'
  set e : Fin k → Fin n := fun i => ⟨band[(i : ℕ)]'(by omega), hlt _ (List.getElem_mem _)⟩
  have he : Function.Injective e := by
    intro i j hij
    simp only [e, Fin.mk.injEq] at hij
    exact Fin.ext ((List.Nodup.getElem_inj_iff hnd).1 hij)
  refine isLocalMin_of_band hP' e he hk y0 m (by exact_mod_cast hm)
    (by have h : ((m : ℚ) : ℝ) ≤ ((1 / 2 : ℚ) : ℝ) := by exact_mod_cast hm1
        push_cast at h; exact h) (fun _ => rfl)
    (fun i => ?_)
  have h := hy _ (List.getElem_mem (show (i : ℕ) < band.length by omega))
  have h' : ((|(P.getD band[(i : ℕ)] 0).2 - y0| : ℚ) : ℝ) ≤ ((1 / 2 - m : ℚ) : ℝ) := by exact_mod_cast h
  push_cast at h'
  exact h'

end UnitSquarePacking
