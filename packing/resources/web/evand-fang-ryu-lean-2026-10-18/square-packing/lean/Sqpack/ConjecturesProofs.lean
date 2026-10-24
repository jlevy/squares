import Sqpack.Conjectures

/-!
# Proofs of the elementary "known" items of `Sqpack/Conjectures.lean`

* `tilingBound : TilingBound` — `s(k²n) ≤ k·s(n)`: a `k × k` array of copies of a packing.
* `cStarStepsOfTwo : CStarStepsOfTwo` — `c*(k+1) ≤ c*(k) + 2`: a packing of `k² − c` squares in a
  box of side `t < k` plus an L-shaped border of `2k − 1` axis-parallel squares packs
  `(k+1)² − (c+2)` squares in side `t + 1 < k + 1`.

Both are built from one tool: packings in a region (`PacksIn`), which can be enlarged, shifted and
glued along rectangles whose interiors are disjoint.

Then the implications between the plateau statements (`NoNonIntegerPlateau.finitelyMany`,
`FinitelyManyPlateaus.bounded`, `.perFract`, `FinitelyManyPerFract.plateaus`,
`FinitelyManyPlateausPerFract.finitelyMany`), using `minSide_mono`.
-/

namespace UnitSquarePacking.Conjectures

open Set

/-- `n` unit squares pack in the region `R`. -/
def PacksIn (n : ℕ) (R : Set (ℝ × ℝ)) : Prop :=
  ∃ (c : Fin n → ℝ × ℝ) (θ : Fin n → ℝ), (∀ i, unitSq (c i) (θ i) ⊆ R) ∧
    Pairwise fun i j => Disjoint (interior (unitSq (c i) (θ i))) (interior (unitSq (c j) (θ j)))

/-- The rectangle `[0, a] × [0, h]`. -/
def rect (a h : ℝ) : Set (ℝ × ℝ) := Icc 0 a ×ˢ Icc 0 h

lemma packs_iff_packsIn {n : ℕ} {s : ℝ} : Packs n s ↔ PacksIn n (rect s s) := Iff.rfl

lemma PacksIn.mono {n : ℕ} {R R' : Set (ℝ × ℝ)} (h : PacksIn n R) (hR : R ⊆ R') :
    PacksIn n R' := by
  obtain ⟨c, θ, hin, hd⟩ := h
  exact ⟨c, θ, fun i => (hin i).trans hR, hd⟩

lemma PacksIn.zero (R : Set (ℝ × ℝ)) : PacksIn 0 R :=
  ⟨Fin.elim0, Fin.elim0, fun i => i.elim0, fun i => i.elim0⟩

lemma rect_mono {a a' h h' : ℝ} (ha : a ≤ a') (hh : h ≤ h') : rect a h ⊆ rect a' h' :=
  prod_mono (Icc_subset_Icc le_rfl ha) (Icc_subset_Icc le_rfl hh)

lemma mem_unitSq_add {c v p : ℝ × ℝ} {θ : ℝ} : p ∈ unitSq (c + v) θ ↔ p - v ∈ unitSq c θ := by
  rw [unitSq_eq_setOf, unitSq_eq_setOf]
  simp only [mem_ofPred_eq, Prod.fst_add, Prod.snd_add, Prod.fst_sub, Prod.snd_sub]
  rw [show p.1 - (c.1 + v.1) = p.1 - v.1 - c.1 by ring,
    show p.2 - (c.2 + v.2) = p.2 - v.2 - c.2 by ring]

lemma mem_interior_unitSq_add {c v p : ℝ × ℝ} {θ : ℝ} :
    p ∈ interior (unitSq (c + v) θ) ↔ p - v ∈ interior (unitSq c θ) := by
  rw [interior_unitSq, interior_unitSq]
  simp only [mem_ofPred_eq, Prod.fst_add, Prod.snd_add, Prod.fst_sub, Prod.snd_sub]
  rw [show p.1 - (c.1 + v.1) = p.1 - v.1 - c.1 by ring,
    show p.2 - (c.2 + v.2) = p.2 - v.2 - c.2 by ring]

/-- Shifting a packing by `v`. -/
lemma PacksIn.shift {n : ℕ} {R : Set (ℝ × ℝ)} (h : PacksIn n R) (v : ℝ × ℝ) :
    PacksIn n {p | p - v ∈ R} := by
  obtain ⟨c, θ, hin, hd⟩ := h
  refine ⟨fun i => c i + v, θ, fun i p hp => hin i (mem_unitSq_add.1 hp), fun i j hij => ?_⟩
  change Disjoint _ _
  rw [Set.disjoint_left]
  intro p hpi hpj
  exact Set.disjoint_left.1 (hd hij) (mem_interior_unitSq_add.1 hpi)
    (mem_interior_unitSq_add.1 hpj)

/-- Gluing packings of two regions with disjoint interiors. -/
lemma PacksIn.union {m n : ℕ} {R R' : Set (ℝ × ℝ)} (h1 : PacksIn m R) (h2 : PacksIn n R')
    (hd : Disjoint (interior R) (interior R')) : PacksIn (m + n) (R ∪ R') := by
  obtain ⟨c1, θ1, hin1, hd1⟩ := h1
  obtain ⟨c2, θ2, hin2, hd2⟩ := h2
  have k1 : ∀ i, interior (unitSq (c1 i) (θ1 i)) ⊆ interior R := fun i => interior_mono (hin1 i)
  have k2 : ∀ i, interior (unitSq (c2 i) (θ2 i)) ⊆ interior R' := fun i => interior_mono (hin2 i)
  refine ⟨Fin.append c1 c2, Fin.append θ1 θ2, fun i => ?_, fun i j hij => ?_⟩
  · induction i using Fin.addCases with
    | left i => simp only [Fin.append_left]; exact (hin1 i).trans subset_union_left
    | right i => simp only [Fin.append_right]; exact (hin2 i).trans subset_union_right
  · change Disjoint _ _
    induction i using Fin.addCases <;> induction j using Fin.addCases <;>
      simp only [Fin.append_left, Fin.append_right]
    · exact hd1 fun h => hij (by rw [h])
    · exact hd.mono (k1 _) (k2 _)
    · exact hd.symm.mono (k2 _) (k1 _)
    · exact hd2 fun h => hij (by rw [h])

lemma interior_rect_shift (a b c d : ℝ) :
    interior (Icc a b ×ˢ Icc c d) = Ioo a b ×ˢ Ioo c d := by
  rw [interior_prod_eq, interior_Icc, interior_Icc]

/-- One axis-parallel unit square fills `[0, 1]²`. -/
lemma packsIn_unit : PacksIn 1 (rect 1 1) := by
  refine ⟨fun _ => (1/2, 1/2), fun _ => 0, fun _ p hp => ?_,
    fun i j h => absurd (Subsingleton.elim i j) h⟩
  rw [unitSq_eq_setOf] at hp
  simp only [Real.cos_zero, Real.sin_zero, mul_one, mul_zero, add_zero, zero_add, 
    mem_ofPred_eq, abs_le] at hp
  obtain ⟨⟨h1, h2⟩, h3, h4⟩ := hp
  exact ⟨⟨by linarith, by linarith⟩, by linarith, by linarith⟩

/-- Side by side: `[0, a] × [0, h]` and `[0, b] × [0, h]` give `[0, a + b] × [0, h]`. -/
lemma PacksIn.hcat {m n : ℕ} {a b h : ℝ} (ha : 0 ≤ a) (hb : 0 ≤ b) (h1 : PacksIn m (rect a h))
    (h2 : PacksIn n (rect b h)) : PacksIn (m + n) (rect (a + b) h) := by
  have h2' : PacksIn n (Icc a (a + b) ×ˢ Icc 0 h) := (h2.shift (a, 0)).mono fun p hp => by
    simp only [rect, mem_ofPred_eq, mem_prod, mem_Icc, Prod.fst_sub, Prod.snd_sub, sub_zero] at hp ⊢
    exact ⟨⟨by linarith, by linarith⟩, hp.2⟩
  refine (h1.union h2' ?_).mono (union_subset (rect_mono (by linarith) le_rfl) ?_)
  · rw [rect, interior_rect_shift, interior_rect_shift, Set.disjoint_left]
    rintro p ⟨⟨_, hp⟩, _⟩ ⟨⟨hp', _⟩, _⟩
    linarith
  · exact prod_mono (Icc_subset_Icc ha le_rfl) le_rfl

/-- One above the other: `[0, w] × [0, a]` and `[0, w] × [0, b]` give `[0, w] × [0, a + b]`. -/
lemma PacksIn.vcat {m n : ℕ} {w a b : ℝ} (ha : 0 ≤ a) (hb : 0 ≤ b) (h1 : PacksIn m (rect w a))
    (h2 : PacksIn n (rect w b)) : PacksIn (m + n) (rect w (a + b)) := by
  have h2' : PacksIn n (Icc 0 w ×ˢ Icc a (a + b)) := (h2.shift (0, a)).mono fun p hp => by
    simp only [rect, mem_ofPred_eq, mem_prod, mem_Icc, Prod.fst_sub, Prod.snd_sub, sub_zero] at hp ⊢
    exact ⟨hp.1, by linarith, by linarith⟩
  refine (h1.union h2' ?_).mono (union_subset (rect_mono le_rfl (by linarith)) ?_)
  · rw [rect, interior_rect_shift, interior_rect_shift, Set.disjoint_left]
    rintro p ⟨_, _, hp⟩ ⟨_, hp', _⟩
    linarith
  · exact prod_mono le_rfl (Icc_subset_Icc ha le_rfl)

/-- `k` copies in a row. -/
lemma PacksIn.row {n : ℕ} {s h : ℝ} (hs : 0 ≤ s) (hp : PacksIn n (rect s h)) :
    ∀ k : ℕ, PacksIn (k * n) (rect (k * s) h)
  | 0 => by simpa using PacksIn.zero _
  | k + 1 => by
    rw [Nat.succ_mul, show ((k + 1 : ℕ) : ℝ) * s = k * s + s by push_cast; ring]
    exact (PacksIn.row hs hp k).hcat (by positivity) hs hp

/-- `k` copies in a column. -/
lemma PacksIn.col {n : ℕ} {w s : ℝ} (hs : 0 ≤ s) (hp : PacksIn n (rect w s)) :
    ∀ k : ℕ, PacksIn (k * n) (rect w (k * s))
  | 0 => by simpa using PacksIn.zero _
  | k + 1 => by
    rw [Nat.succ_mul, show ((k + 1 : ℕ) : ℝ) * s = k * s + s by push_cast; ring]
    exact (PacksIn.col hs hp k).vcat (by positivity) hs hp

/-- **Tiling.**  A packing of `n` squares in side `s` gives one of `k²n` squares in side `k·s`. -/
theorem packs_tile {n : ℕ} {s : ℝ} (hs : 0 ≤ s) (h : Packs n s) (k : ℕ) :
    Packs (k ^ 2 * n) (k * s) := by
  have h1 := (packs_iff_packsIn.1 h).row hs k
  have h2 := h1.col hs k
  rw [show k ^ 2 * n = k * (k * n) by ring]
  exact h2

/-- A box holding a unit square has side `≥ 0` (the centre lies in it). -/
lemma nonneg_of_packs' {n : ℕ} {s : ℝ} (hn : 1 ≤ n) (h : Packs n s) : 0 ≤ s := by
  obtain ⟨c, θ, hin, -⟩ := h
  have hc : c ⟨0, hn⟩ ∈ unitSq (c ⟨0, hn⟩) (θ ⟨0, hn⟩) :=
    ⟨0, ⟨⟨by norm_num, by norm_num⟩, by norm_num, by norm_num⟩, by simp [rot]⟩
  obtain ⟨⟨h1, h2⟩, -⟩ := hin _ hc
  linarith

/-- `n` squares fit in side `n` (a row). -/
lemma packs_self {n : ℕ} (hn : 1 ≤ n) : Packs n n := by
  refine packs_iff_packsIn.2 ?_
  have := packsIn_unit.row zero_le_one n
  rw [mul_one, mul_one] at this
  exact this.mono (rect_mono le_rfl (by exact_mod_cast hn))

lemma minSide_nonneg {n : ℕ} (hn : 1 ≤ n) : 0 ≤ minSide n :=
  le_csInf ⟨n, packs_self hn⟩ fun _ hs => nonneg_of_packs' hn hs

/-- `s` is monotone. -/
lemma minSide_mono {m m' : ℕ} (hm : 1 ≤ m) (h : m ≤ m') : minSide m ≤ minSide m' :=
  csInf_le_csInf ⟨0, fun _ hs => nonneg_of_packs' hm hs⟩ ⟨m', packs_self (hm.trans h)⟩
    fun _ hs => packs_of_le hs h

/-- **`s(k²n) ≤ k·s(n)`.**  (No attainment needed: tile every packing of `n`, then take `sInf`.) -/
theorem tilingBound : TilingBound := by
  intro n k hn hk
  have hk' : (0 : ℝ) < k := by exact_mod_cast hk
  have hpos : 1 ≤ k ^ 2 * n := Nat.mul_pos (pow_pos hk 2) hn
  have hne : ({s | Packs n s} : Set ℝ).Nonempty := ⟨n, packs_self hn⟩
  have hbdd : BddBelow ({s | Packs (k ^ 2 * n) s} : Set ℝ) :=
    ⟨0, fun _ hs => nonneg_of_packs' hpos hs⟩
  have h : minSide (k ^ 2 * n) / k ≤ minSide n := by
    refine le_csInf hne fun s hs => ?_
    rw [div_le_iff₀ hk', mul_comm s]
    exact csInf_le hbdd (packs_tile (nonneg_of_packs' hn hs) hs k)
  rw [div_le_iff₀ hk'] at h
  linarith

/-- **`c*(k+1) ≤ c*(k) + 2`**, by an L-shaped border. -/
theorem cStarStepsOfTwo : CStarStepsOfTwo := by
  intro k c hk h2
  by_contra hne
  simp only [GridOptimal, not_forall, not_le] at hne
  obtain ⟨s, hs, hlt⟩ := hne
  have hk1 : (1 : ℝ) ≤ k := by exact_mod_cast hk
  set t := max s ((k : ℝ) - 1) with ht
  have ht0 : 0 ≤ t := le_max_of_le_right (by linarith)
  have htk : t < k := max_lt hlt (by linarith)
  have hkt : (k : ℝ) - 1 ≤ t := le_max_right _ _
  have hcast : ((k - 1 : ℕ) : ℝ) = k - 1 := by rw [Nat.cast_sub hk]; simp
  have hA : PacksIn (k ^ 2 - c) (rect t t) :=
    (packs_iff_packsIn.1 hs).mono (rect_mono (le_max_left _ _) (le_max_left _ _))
  have hcol : PacksIn (k - 1) (rect 1 t) := by
    have := packsIn_unit.col zero_le_one (k - 1)
    rw [mul_one, hcast, mul_one] at this
    exact this.mono (rect_mono le_rfl hkt)
  have hrow : PacksIn k (rect (t + 1) 1) := by
    have := packsIn_unit.row zero_le_one k
    rw [mul_one, mul_one] at this
    exact this.mono (rect_mono (by linarith) le_rfl)
  have hC := (hA.hcat ht0 zero_le_one hcol).vcat ht0 zero_le_one hrow
  have hle : (k + 1) ^ 2 - (c + 2) ≤ k ^ 2 - c + (k - 1) + k := by
    have : (k + 1) ^ 2 = k ^ 2 + 2 * k + 1 := by ring
    omega
  have := h2 (t + 1) (packs_of_le (packs_iff_packsIn.2 hC) hle)
  push_cast at this
  linarith

/-! ## How the plateau statements relate -/

theorem NoNonIntegerPlateau.finitelyMany (h : NoNonIntegerPlateau) : FinitelyManyPlateaus :=
  Set.finite_empty.subset fun n hn => h n hn

theorem FinitelyManyPlateaus.perFract (h : FinitelyManyPlateaus) :
    FinitelyManyPlateausPerFract :=
  fun _ => h.subset fun _ hn => hn.1

/-- An integer value of `s` is a natural number. -/
lemma not_nonIntegral_of_fract_eq_zero {n : ℕ} (hn : 1 ≤ n) (h : Int.fract (minSide n) = 0) :
    ¬ NonIntegral n := by
  intro hni
  obtain ⟨z, hz⟩ := Int.fract_eq_zero_iff.1 h
  have hz0 : (0 : ℤ) ≤ z := by exact_mod_cast hz ▸ minSide_nonneg hn
  apply hni z.toNat
  rw [← hz]
  exact_mod_cast (Int.toNat_of_nonneg hz0).symm

theorem FinitelyManyPerFract.plateaus (h : FinitelyManyPerFract) :
    FinitelyManyPlateausPerFract := by
  intro β
  rcases le_or_gt β 0 with hβ | hβ
  · refine Set.finite_empty.subset fun n ⟨hp, hf⟩ => ?_
    have h0 : Int.fract (minSide n) = 0 := le_antisymm (hf ▸ hβ) (Int.fract_nonneg _)
    exact not_nonIntegral_of_fract_eq_zero hp.1 h0 hp.2.2
  · exact (h β hβ).subset fun n hn => ⟨hn.1.1, hn.2⟩

theorem FinitelyManyPlateausPerFract.finitelyMany (h : FinitelyManyPlateausPerFract)
    (hf : PlateauFractsFinite) : FinitelyManyPlateaus := by
  refine (hf.biUnion fun β _ => h β).subset fun n hn => ?_
  simp only [Set.mem_iUnion, Set.mem_image, Set.mem_ofPred_eq, exists_prop]
  exact ⟨_, ⟨n, hn, rfl⟩, hn, rfl⟩

theorem FinitelyManyPlateaus.bounded (h : FinitelyManyPlateaus) : PlateausBounded := by
  obtain ⟨M, hM⟩ := h.bddAbove
  refine ⟨M + 1, fun n hn hni => lt_of_le_of_ne (minSide_mono hn (by omega)) fun heq => ?_⟩
  have hlo : minSide n ≤ minSide (n + M) := minSide_mono hn (by omega)
  have hhi : minSide (n + M) ≤ minSide (n + M + 1) := minSide_mono (by omega) (by omega)
  have hval : minSide (n + M) = minSide n := le_antisymm (by rw [heq, ← add_assoc] at *; linarith)
    hlo
  have hp : NonIntPlateau (n + M) :=
    ⟨by omega, by rw [hval, heq, add_assoc], fun m hm => hni m (hval ▸ hm)⟩
  have := hM hp
  omega

/-! ## The large-`k` case of "tilings are never optimal", from the waste bound -/

/-- **Waste `O(s^{3/5})` and positive waste at non-integer sides give the large-`k` case of
`TilingsNeverOptimal`.**  With `s = s(n)` and `u = (s + n/s)/2` (so `√n < u < s`), the waste bound
at side `k·u` packs at least `k²u² − C·k·u ≥ k²n` squares once `k·(u² − n) ≥ |C|·u`. -/
theorem tilingsEventuallyNotOptimal_of (hw : ThreeFifthsWaste) (ha : AreaStrict) :
    TilingsEventuallyNotOptimal := by
  intro n hn hni
  obtain ⟨C, hC⟩ := hw
  have hn1 : (1 : ℝ) ≤ n := by exact_mod_cast hn
  have hδ := ha n hn hni
  set s := minSide n with hs
  have hs0 : 0 ≤ s := minSide_nonneg hn
  have hs1 : 1 < s := by nlinarith
  set u := (s + n / s) / 2 with hu
  have hns : (n : ℝ) / s < s := by rw [div_lt_iff₀ (by linarith)]; nlinarith
  have hus : u < s := by rw [hu]; linarith
  have hnpos : (0 : ℝ) < n / s := by positivity
  have hγ : 0 < u ^ 2 - n := by
    have h1 : u ^ 2 - n = ((s - n / s) / 2) ^ 2 := by
      rw [hu]; field_simp; ring
    rw [h1]; have : 0 < s - n / s := by linarith
    positivity
  have hu1 : 1 ≤ u := by nlinarith
  obtain ⟨K, hK⟩ := exists_nat_ge (|C| * u / (u ^ 2 - n))
  refine ⟨max K 1, fun k hk => ?_⟩
  have hk1 : (1 : ℝ) ≤ k := by exact_mod_cast (le_max_right K 1).trans hk
  have hkK : |C| * u / (u ^ 2 - n) ≤ k := hK.trans (by exact_mod_cast (le_max_left K 1).trans hk)
  have hkγ : |C| * u ≤ k * (u ^ 2 - n) := by rwa [div_le_iff₀ hγ] at hkK
  have hx1 : 1 ≤ (k : ℝ) * u := by nlinarith
  obtain ⟨N, hN, hP⟩ := hC (k * u) hx1
  have hrp : ((k : ℝ) * u) ^ (3 / 5 : ℝ) ≤ k * u := by
    calc ((k : ℝ) * u) ^ (3 / 5 : ℝ) ≤ ((k : ℝ) * u) ^ (1 : ℝ) :=
          Real.rpow_le_rpow_of_exponent_le hx1 (by norm_num)
      _ = k * u := Real.rpow_one _
  have hCx : C * ((k : ℝ) * u) ^ (3 / 5 : ℝ) ≤ |C| * (k * u) :=
    (mul_le_mul_of_nonneg_right (le_abs_self C) (by positivity)).trans
      (mul_le_mul_of_nonneg_left hrp (abs_nonneg C))
  have hcount : ((k ^ 2 * n : ℕ) : ℝ) ≤ N := by
    push_cast
    nlinarith
  have hpk : Packs (k ^ 2 * n) (k * u) := packs_of_le hP (by exact_mod_cast hcount)
  have hpos : 1 ≤ k ^ 2 * n := Nat.mul_pos (pow_pos (by exact_mod_cast hk1) 2) hn
  calc minSide (k ^ 2 * n) ≤ k * u := csInf_le ⟨0, fun _ h => nonneg_of_packs' hpos h⟩ hpk
    _ < k * s := by nlinarith

end UnitSquarePacking.Conjectures
