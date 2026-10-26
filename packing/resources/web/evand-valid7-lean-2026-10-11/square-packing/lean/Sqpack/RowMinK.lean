import Sqpack.KBern

/-!
# The Kronecker sign test of all combinations at once

A vertex test sums one term from each of several rows (the alternatives of a segment), for every
combination.  Over a common degree `N`, each term `p` has its image `γ(2ᴷ) = Bᴺ p(A/B)` whose balanced
digits base `2ᴷ` are the coefficients of `γ(t) = Σₖ pₖ (U0 + U1 t)ᵏ (R + R t)ᴺ⁻ᵏ`.  The digits of a
sum are the sums of the digits, so if, digit by digit, the row minima plus the fixed terms are
`≥ 0`, every combination's `γ` has non-negative coefficients, and the combination is `≥ 0` on the
bin `[U0/R, U1/R]` (`rmLoop_sound`).  The cost is the number of terms, not of combinations.
-/

namespace SquarePacking

namespace KArith

open BernZ RatU

/-! ## 1.  Balanced digits -/

/-- The balanced digit of `v` base `2ᴷ`: `v mod 2ᴷ` in `[-2ᴷ⁻¹, 2ᴷ⁻¹)`. -/
def balD (K : ℕ) (v : ℤ) : ℤ :=
  if v % 2 ^ K < 2 ^ (K - 1) then v % 2 ^ K else v % 2 ^ K - 2 ^ K

/-- The rest after the digit. -/
def shiftD (K : ℕ) (v : ℤ) : ℤ := (v - balD K v) / 2 ^ K

lemma balD_shiftD {K : ℕ} (hK : 0 < K) {c v : ℤ} (hc : 2 * |c| < 2 ^ K) :
    balD K (c + 2 ^ K * v) = c ∧ shiftD K (c + 2 ^ K * v) = v := by
  have hX : (0 : ℤ) < 2 ^ K := by positivity
  have hhalf : (2 : ℤ) ^ K = 2 * 2 ^ (K - 1) := by rw [← pow_succ']; congr 1; omega
  have habs := abs_lt.mp (show |c| < 2 ^ (K - 1) by linarith)
  have hb : balD K (c + 2 ^ K * v) = c := by
    unfold balD
    rw [Int.add_mul_emod_self_left]
    rcases le_or_gt 0 c with h0 | h0
    · rw [Int.emod_eq_of_lt h0 (by linarith), if_pos habs.2]
    · have e : c % 2 ^ K = c + 2 ^ K := by
        rw [← Int.add_emod_right]
        exact Int.emod_eq_of_lt (by linarith) (by linarith)
      rw [e, if_neg (by linarith)]; ring
  refine ⟨hb, ?_⟩
  unfold shiftD
  rw [hb, add_sub_cancel_left, Int.mul_ediv_cancel_left _ hX.ne']

/-- The `i`-th digit. -/
def digI (K : ℕ) : ℕ → ℤ → ℤ
  | 0, v => balD K v
  | i + 1, v => digI K i (shiftD K v)

lemma digI_evalZ {K : ℕ} (hK : 0 < K) :
    ∀ (q : Poly), (∀ c ∈ q, 2 * |c| < 2 ^ K) → ∀ i, digI K i (evalZ q (2 ^ K)) = q.getD i 0
  | [], _, i => by
    have h0 : balD K 0 = 0 ∧ shiftD K 0 = 0 := by
      simpa using balD_shiftD (v := 0) hK (c := 0) (by simp)
    induction i with
    | zero => simpa [evalZ, digI] using h0.1
    | succ i ih => simpa [evalZ, digI, h0.2] using ih
  | c :: q, hq, i => by
    have hc : 2 * |c| < 2 ^ K := hq c List.mem_cons_self
    obtain ⟨h1, h2⟩ := balD_shiftD hK (v := evalZ q (2 ^ K)) hc
    cases i with
    | zero => simpa [evalZ, digI] using h1
    | succ i =>
      simp only [evalZ, digI, h2, List.getD_cons_succ]
      exact digI_evalZ hK q (fun x hx => hq x (List.mem_cons_of_mem _ hx)) i

/-! ## 2.  Rows and their minima, digit by digit -/

def minL : List ℤ → ℤ
  | [] => 0
  | [a] => a
  | a :: b :: l => min a (minL (b :: l))

lemma minL_le : ∀ (l : List ℤ) (a : ℤ), a ∈ l → minL l ≤ a
  | [], _, h => absurd h List.not_mem_nil
  | [x], a, h => by simp at h; simp [minL, h]
  | x :: y :: l, a, h => by
    rcases List.mem_cons.mp h with rfl | h
    · exact min_le_left _ _
    · exact (min_le_right _ _).trans (minL_le (y :: l) a h)

/-- The test of the digits `0 .. L-1` (`ε = ±1` the sign wanted). -/
def rmLoop (K : ℕ) (ε : ℤ) : ℕ → List (List ℤ) → List ℤ → Bool
  | 0, _, _ => true
  | L + 1, rows, fx =>
    decide (0 ≤ (rows.map fun r => minL (r.map fun v => ε * balD K v)).sum +
      (fx.map fun v => ε * balD K v).sum) &&
      rmLoop K ε L (rows.map (·.map (shiftD K))) (fx.map (shiftD K))

lemma sum_minL_le {f : ℤ → ℤ} :
    ∀ (rows : List (List ℤ)) (comb : List ℤ), List.Forall₂ (fun a l => a ∈ l) comb rows →
      (rows.map fun r => minL (r.map f)).sum ≤ (comb.map f).sum
  | [], [], _ => by simp
  | r :: rows, a :: comb, List.Forall₂.cons ha h => by
    simp only [List.map_cons, List.sum_cons]
    exact add_le_add (minL_le _ _ (List.mem_map_of_mem ha)) (sum_minL_le rows comb h)

lemma forall₂_map_shift {K : ℕ} :
    ∀ {rows : List (List ℤ)} {comb : List ℤ}, List.Forall₂ (fun a l => a ∈ l) comb rows →
      List.Forall₂ (fun a l => a ∈ l) (comb.map (shiftD K)) (rows.map (·.map (shiftD K)))
  | [], [], _ => List.Forall₂.nil
  | _ :: _, _ :: _, List.Forall₂.cons ha h =>
    List.Forall₂.cons (List.mem_map_of_mem ha) (forall₂_map_shift h)

lemma digI_shift (K : ℕ) (i : ℕ) (v : ℤ) : digI K i (shiftD K v) = digI K (i + 1) v := rfl

/-- **Every combination passes**: for each digit `i < L`, the digits of the chosen terms and of
the fixed ones have sum `≥ 0` (times `ε`). -/
theorem rmLoop_sound {K : ℕ} {ε : ℤ} :
    ∀ (L : ℕ) (rows : List (List ℤ)) (fx comb : List ℤ), rmLoop K ε L rows fx = true →
      List.Forall₂ (fun a l => a ∈ l) comb rows →
      ∀ i < L, 0 ≤ ((comb ++ fx).map fun v => ε * digI K i v).sum
  | 0, _, _, _, _, _, i, hi => absurd hi (Nat.not_lt_zero _)
  | L + 1, rows, fx, comb, h, hc, i, hi => by
    simp only [rmLoop, Bool.and_eq_true, decide_eq_true_eq] at h
    obtain ⟨h0, hrest⟩ := h
    cases i with
    | zero =>
      simp only [List.map_append, List.sum_append, digI]
      have := sum_minL_le (f := fun v => ε * balD K v) rows comb hc
      linarith
    | succ i =>
      have := rmLoop_sound L _ _ _ hrest (forall₂_map_shift hc) i (by omega)
      simpa [List.map_append, List.map_map, Function.comp_def, digI_shift] using this

/-! ## 3.  From digits to the bin -/

lemma getD_add : ∀ (p q : Poly) (i : ℕ), (add p q).getD i 0 = p.getD i 0 + q.getD i 0
  | [], q, i => by simp [add]
  | a :: p, [], i => by simp [add]
  | a :: p, b :: q, i => by
    cases i with
    | zero => simp [add]
    | succ i => simp only [add, List.getD_cons_succ]; exact getD_add p q i

lemma getD_smul (c : ℤ) (p : Poly) (i : ℕ) : (smul c p).getD i 0 = c * p.getD i 0 := by
  unfold smul
  by_cases h : i < p.length
  · rw [List.getD_eq_getElem _ _ (by simpa using h), List.getD_eq_getElem _ _ h]; simp
  · rw [List.getD_eq_default _ _ (by simpa using h), List.getD_eq_default _ _ (by omega)]; simp

/-- The sum of polynomials. -/
def sumP : List Poly → Poly
  | [] => []
  | p :: ps => add p (sumP ps)

lemma getD_sumP (i : ℕ) : ∀ ps : List Poly, (sumP ps).getD i 0 = (ps.map (·.getD i 0)).sum
  | [] => by simp [sumP]
  | p :: ps => by
    simp only [sumP, List.map_cons, List.sum_cons]
    rw [getD_add, getD_sumP i ps]

lemma eval_sumP (x : ℝ) : ∀ ps : List Poly, eval (sumP ps) x = (ps.map (eval · x)).sum
  | [] => by simp [sumP]
  | p :: ps => by simp [sumP, BernZ.eval_add, eval_sumP x ps]

lemma nonneg_of_getD {q : Poly} (h : ∀ i, 0 ≤ q.getD i 0) : ∀ c ∈ q, 0 ≤ c := by
  intro c hc
  obtain ⟨i, hi, rfl⟩ := List.getElem_of_mem hc
  have := h i
  rwa [List.getD_eq_getElem _ _ hi] at this

/-- `0 ≤ p` on the closed bin from `0 ≤ γ(t)` for `t ≥ 0` (`t = (Ru − U0)/(U1 − Ru)`, the right
end by continuity). -/
lemma bin_of_gamma {U0 U1 R N : ℕ} (hR : 0 < R) {p : Poly}
    (hγ : ∀ t : ℝ, 0 ≤ t → 0 ≤ (R * (1 + t)) ^ N * eval p ((U0 + U1 * t) / (R * (1 + t))))
    {u : ℝ} (hu0 : (U0 : ℝ) / R ≤ u) (hu1 : u ≤ (U1 : ℝ) / R) : 0 ≤ eval p u := by
  have hRr : (0 : ℝ) < R := by exact_mod_cast hR
  have hpos : ∀ t : ℝ, 0 ≤ t → 0 ≤ eval p ((U0 + U1 * t) / (R * (1 + t))) := fun t ht =>
    (mul_nonneg_iff_of_pos_left (pow_pos (by positivity) _)).mp (hγ t ht)
  have hIco : ∀ x ∈ Set.Ico ((U0 : ℝ) / R) ((U1 : ℝ) / R), 0 ≤ eval p x := by
    rintro x ⟨hx0, hx1⟩
    have a0 : (U0 : ℝ) ≤ R * x := by rw [div_le_iff₀ hRr] at hx0; linarith
    have a1 : R * x < (U1 : ℝ) := by rw [lt_div_iff₀ hRr] at hx1; linarith
    have ht0 : 0 ≤ (R * x - U0) / (U1 - R * x) := div_nonneg (by linarith) (by linarith)
    have := hpos _ ht0
    have hd : (U1 : ℝ) - R * x ≠ 0 := by linarith
    have hpos' : (0 : ℝ) < R * (1 + (R * x - U0) / (U1 - R * x)) := by positivity
    have e : ((U0 : ℝ) + U1 * ((R * x - U0) / (U1 - R * x))) /
        (R * (1 + (R * x - U0) / (U1 - R * x))) = x := by
      rw [div_eq_iff hpos'.ne']
      field_simp
      ring
    rwa [e] at this
  rcases eq_or_lt_of_le hu1 with e | hlt
  · rcases eq_or_lt_of_le (le_trans hu0 hu1) with e' | hlt'
    · have := hpos 0 le_rfl
      simpa [e, ← e'] using this
    · have hcl : closure (Set.Ico ((U0 : ℝ) / R) ((U1 : ℝ) / R)) ⊆ {x | 0 ≤ eval p x} :=
        (isClosed_le continuous_const (continuous_eval p)).closure_subset_iff.mpr hIco
      rw [closure_Ico hlt'.ne] at hcl
      exact hcl ⟨hu0, hu1⟩
  · exact hIco u ⟨hu0, hlt⟩

/-- **The polynomial step.**  Terms `p` with images `h` at the common degree `N`, small digits, and
`ε` times the digit sums of their images `≥ 0` for every digit: then `ε Σ p ≥ 0` on the bin. -/
theorem nonneg_of_digits {U0 U1 R K M N : ℕ} (hK : 0 < K) (hR : 0 < R) (hM1 : U0 + U1 ≤ M)
    (hM2 : 2 * R ≤ M) {ε : ℤ} (ts : List (Poly × KH))
    (hrep : ∀ x ∈ ts, RepH ((U0 : ℤ) + U1 * 2 ^ K) (R * (1 + 2 ^ K)) x.1 x.2)
    (hn : ∀ x ∈ ts, x.2.n = N) (hb : ∀ x ∈ ts, 2 * x.2.b * M ^ N < 2 ^ K)
    (hdig : ∀ i < N + 2, 0 ≤ (ts.map fun x => ε * digI K i x.2.v).sum)
    {u : ℝ} (hu0 : (U0 : ℝ) / R ≤ u) (hu1 : u ≤ (U1 : ℝ) / R) :
    0 ≤ ε * (ts.map fun x => eval x.1 u).sum := by
  set Ap : Poly := [(U0 : ℤ), U1]
  set Bp : Poly := [(R : ℤ), R]
  have eA : ∀ t : ℝ, eval Ap t = U0 + U1 * t := fun t => by simp [Ap]; ring
  have eB : ∀ t : ℝ, eval Bp t = R * (1 + t) := fun t => by simp [Bp]; ring
  have hRr : (0 : ℝ) < R := by exact_mod_cast hR
  -- the image of each term is `γ(2ᴷ)`, `γ = homP Ap Bp N p`, with small coefficients
  have key : ∀ x ∈ ts, evalZ (homP Ap Bp N x.1) (2 ^ K) = x.2.v ∧
      (∀ c ∈ homP Ap Bp N x.1, 2 * |c| < 2 ^ K) ∧ (homP Ap Bp N x.1).length ≤ N + 2 := by
    intro x hx
    obtain ⟨hv, hl1, hlen⟩ := hrep x hx
    rw [hn x hx] at hv hlen
    have hlq : l1 (homP Ap Bp N x.1) ≤ x.2.b * M ^ N :=
      (l1_homP (by simp [Ap, l1]; omega) (by simp [Bp, l1]; omega) x.1 N hlen).trans
        (Nat.mul_le_mul_right _ hl1)
    refine ⟨?_, fun c hc => ?_, length_homP (by simp [Ap]) (by simp [Bp]) x.1 N hlen⟩
    · have : ((evalZ (homP Ap Bp N x.1) (2 ^ K) : ℤ) : ℝ) = (x.2.v : ℝ) := by
        rw [evalZ_cast, eval_homP Ap Bp _ (by rw [eB]; positivity) x.1 N hlen, hv, eA, eB]
        push_cast
        ring_nf
      exact_mod_cast this
    · have h1 : (c.natAbs : ℤ) ≤ l1 (homP Ap Bp N x.1) := by
        have := List.single_le_sum (fun _ _ => Nat.zero_le _) _ (List.mem_map_of_mem (f := Int.natAbs) hc)
        exact_mod_cast this
      have h2 : 2 * ((x.2.b * M ^ N : ℕ) : ℤ) < 2 ^ K := by
        have := hb x hx; rw [mul_assoc] at this; exact_mod_cast this
      rw [Int.abs_eq_natAbs]
      have : (l1 (homP Ap Bp N x.1) : ℤ) ≤ (x.2.b * M ^ N : ℕ) := by exact_mod_cast hlq
      linarith
  -- `Γ = Σ ε γ` has non-negative coefficients
  set Γ := sumP (ts.map fun x => smul ε (homP Ap Bp N x.1)) with hΓ
  have hcoef : ∀ i, 0 ≤ Γ.getD i 0 := by
    intro i
    rw [hΓ, getD_sumP, List.map_map]
    simp only [Function.comp_def]
    by_cases hi : i < N + 2
    · have e : ∀ x ∈ ts, (smul ε (homP Ap Bp N x.1)).getD i 0 = ε * digI K i x.2.v := by
        intro x hx
        obtain ⟨h1, h2, _⟩ := key x hx
        rw [getD_smul, ← h1, digI_evalZ hK _ h2]
      rw [List.map_congr_left e]
      exact hdig i hi
    · have e : ∀ x ∈ ts, (smul ε (homP Ap Bp N x.1)).getD i 0 = 0 := by
        intro x hx
        rw [getD_smul, List.getD_eq_default _ _ (by have := (key x hx).2.2; omega)]; ring
      rw [List.map_congr_left e]
      simp
  -- so `Γ(t) ≥ 0` for `t ≥ 0`, which is `ε (R(1+t))ᴺ Σ p` at the pose of `t`
  refine bin_of_gamma (N := N) hR (p := sumP (ts.map fun x => smul ε x.1)) ?_ hu0 hu1 |>.trans_eq ?_
  · intro t ht
    have h0 := eval_nonneg_of_coeffs Γ (nonneg_of_getD hcoef) t ht
    rw [hΓ, eval_sumP, List.map_map] at h0
    simp only [Function.comp_def] at h0
    have e : ∀ x ∈ ts, eval (smul ε (homP Ap Bp N x.1)) t =
        (R * (1 + t)) ^ N * eval (smul ε x.1) ((U0 + U1 * t) / (R * (1 + t))) := by
      intro x hx
      have hl : x.1.length ≤ N + 1 := by have := (hrep x hx).2.2; rw [hn x hx] at this; exact this
      rw [BernZ.eval_smul, BernZ.eval_smul, eval_homP Ap Bp t (by rw [eB]; positivity) x.1 N hl, eA, eB]
      ring
    rw [List.map_congr_left e, List.sum_map_mul_left] at h0
    rw [eval_sumP, List.map_map]
    simpa only [Function.comp_def] using h0
  · rw [eval_sumP, List.map_map]
    simp only [Function.comp_def, BernZ.eval_smul]
    rw [List.sum_map_mul_left]

end KArith

end SquarePacking
