import Sqpack.KArith

/-!
# The Bernstein test as one number

On the bin `[U0/R, U1/R]`, `p ≥ 0` follows from `γ(t) = Σₖ pₖ (U0 + U1 t)ᵏ (R + R t)ⁿ⁻ᵏ` having
non-negative coefficients (`t = (Ru − U0)/(U1 − Ru)` maps the bin onto `[0, ∞)`, the right end by
continuity).  With `X = 2ᴷ`, `A = U0 + U1 X`, `B = R (1 + X)`, the integer `γ(X) = Bⁿ p(A/B)` holds
those coefficients as its balanced digits (when `2 Σ|γᵢ| < X`), and they are all `≥ 0` iff
`γ(X) ≥ 0` and no digit has its top bit set: one `&&&` with a mask (`hcheck_sound`).

`KH` carries `Bⁿ p(A/B)` (with bounds on `Σ|pᵢ|` and on the length) through sums and products
(`RepH`), so the numerators of a vertex test never need to be expanded.
-/

namespace SquarePacking

namespace KArith

open BernZ RatU

/-! ## 1.  Homogeneous images -/

/-- `v = Bⁿ p(A/B)` for a polynomial `p` of length `≤ n + 1` with `Σ|pᵢ| ≤ b`. -/
structure KH where
  v : ℤ
  n : ℕ
  b : ℕ

def RepH (A : ℤ) (B : ℕ) (p : Poly) (h : KH) : Prop :=
  (h.v : ℝ) = (B : ℝ) ^ h.n * eval p ((A : ℝ) / B) ∧ l1 p ≤ h.b ∧ p.length ≤ h.n + 1

def hconst (c : ℤ) : KH := ⟨c, 0, c.natAbs⟩

def hadd (B : ℕ) (p q : KH) : KH :=
  if p.n = q.n then ⟨p.v + q.v, p.n, p.b + q.b⟩
  else if p.n < q.n then ⟨p.v * ((B ^ (q.n - p.n) : ℕ) : ℤ) + q.v, q.n, p.b + q.b⟩
  else ⟨p.v + q.v * ((B ^ (p.n - q.n) : ℕ) : ℤ), p.n, p.b + q.b⟩

/-- The product (a factor `1` is skipped). -/
def hmul (p q : KH) : KH :=
  if q.n = 0 ∧ q.v = 1 ∧ q.b = 1 then p
  else if p.n = 0 ∧ p.v = 1 ∧ p.b = 1 then q
  else ⟨p.v * q.v, p.n + q.n, p.b * q.b⟩

def hsmul (c : ℤ) (p : KH) : KH := ⟨c * p.v, p.n, c.natAbs * p.b⟩

def hpow (p : KH) : ℕ → KH
  | 0 => hconst 1
  | 1 => p
  | n + 2 => hmul p (hpow p (n + 1))

def hP (A : ℤ) (B : ℕ) : Poly → KH
  | [] => ⟨0, 0, 0⟩
  | [a] => hconst a
  | a :: b :: p =>
    match hP A B (b :: p) with
    | ⟨v, n, c⟩ => ⟨a * ((B ^ (n + 1) : ℕ) : ℤ) + A * v, n + 1, a.natAbs + c⟩

lemma length_mul' : ∀ (p q : Poly), (mul p q).length ≤ p.length + (q.length - 1)
  | [], q => by simp [mul]
  | a :: p, q => by
    rw [mul, length_add, length_smul]
    have := length_mul' p q
    simp only [List.length_cons]
    rcases q with _ | ⟨b, q⟩
    · simp only [List.length_nil, Nat.zero_sub, add_zero] at this ⊢; omega
    · simp only [List.length_cons] at this ⊢; omega

section rep

variable {A : ℤ} {B : ℕ}

lemma rep_hconst (c : ℤ) : RepH A B [c] (hconst c) := ⟨by simp [hconst], by simp [hconst], by simp [hconst]⟩

lemma rep_hadd (hB : 0 < B) {p q : Poly} {h k : KH} (hp : RepH A B p h) (hq : RepH A B q k) :
    RepH A B (add p q) (hadd B h k) := by
  obtain ⟨a, b, c⟩ := hp; obtain ⟨a', b', c'⟩ := hq
  have hl := l1_add p q
  have hlen := length_add p q
  unfold hadd
  split_ifs with e1 e2
  · refine ⟨?_, by simp only; omega, by simp only; omega⟩
    simp only [Int.cast_add, a, a', BernZ.eval_add, e1]; ring
  · refine ⟨?_, by simp only; omega, by simp only; omega⟩
    simp only [Int.cast_add, Int.cast_mul, a, a', BernZ.eval_add]
    push_cast
    rw [show (B : ℝ) ^ k.n = (B : ℝ) ^ h.n * (B : ℝ) ^ (k.n - h.n) by
      rw [← pow_add, Nat.add_sub_cancel' (by omega)]]
    ring
  · refine ⟨?_, by simp only; omega, by simp only; omega⟩
    simp only [Int.cast_add, Int.cast_mul, a, a', BernZ.eval_add]
    push_cast
    rw [show (B : ℝ) ^ h.n = (B : ℝ) ^ k.n * (B : ℝ) ^ (h.n - k.n) by
      rw [← pow_add, Nat.add_sub_cancel' (by omega)]]
    ring

lemma rep_hmul {p q : Poly} {h k : KH} (hp : RepH A B p h) (hq : RepH A B q k) :
    RepH A B (mul p q) (hmul h k) := by
  obtain ⟨a, b, c⟩ := hp; obtain ⟨a', b', c'⟩ := hq
  have hl := l1_mul p q
  have hn := length_mul' p q
  unfold hmul
  split_ifs with e1 e2
  · obtain ⟨n0, v1, b1⟩ := e1
    rw [n0, v1] at a'; rw [b1] at b'; rw [n0] at c'
    refine ⟨?_, by nlinarith, by omega⟩
    rw [a, BernZ.eval_mul]
    simp only [Int.cast_one, pow_zero, one_mul] at a'
    rw [← a', mul_one]
  · obtain ⟨n0, v1, b1⟩ := e2
    rw [n0, v1] at a; rw [b1] at b; rw [n0] at c
    refine ⟨?_, by nlinarith, by omega⟩
    rw [a', BernZ.eval_mul]
    simp only [Int.cast_one, pow_zero, one_mul] at a
    rw [← a, one_mul]
  · refine ⟨?_, hl.trans (Nat.mul_le_mul b b'), hn.trans (by show _ ≤ h.n + k.n + 1; omega)⟩
    simp only [Int.cast_mul, a, a', BernZ.eval_mul, pow_add]; ring

lemma rep_hsmul (c : ℤ) {p : Poly} {h : KH} (hp : RepH A B p h) : RepH A B (smul c p) (hsmul c h) := by
  obtain ⟨a, b, d⟩ := hp
  refine ⟨?_, by rw [l1_smul]; exact Nat.mul_le_mul_left _ b, by rw [length_smul]; exact d⟩
  simp only [hsmul, Int.cast_mul, a, BernZ.eval_smul]; ring

lemma rep_hpow {p : Poly} {h : KH} (hp : RepH A B p h) : ∀ n, RepH A B (ppow p n) (hpow h n)
  | 0 => by simpa [hpow, ppow] using rep_hconst (A := A) (B := B) 1
  | 1 => by
    rw [hpow]
    obtain ⟨a, b, c⟩ := hp
    refine ⟨?_, ?_, ?_⟩
    · rw [a, ppow, BernZ.eval_mul, ppow]; simp
    · refine le_trans ?_ b; rw [ppow, ppow]; exact (l1_mul _ _).trans (by simp [l1])
    · refine le_trans ?_ c; rw [ppow, ppow]; exact (length_mul' _ _).trans (by simp)
  | n + 2 => by rw [hpow, ppow]; exact rep_hmul hp (rep_hpow hp (n + 1))

lemma rep_hP (hB : 0 < B) : ∀ p : Poly, RepH A B p (hP A B p)
  | [] => ⟨by simp [hP], by simp [hP], by simp [hP]⟩
  | [a] => by rw [hP]; exact rep_hconst a
  | a :: b :: p => by
    have ih := rep_hP hB (b :: p)
    rw [hP]
    generalize hP A B (b :: p) = k at ih
    obtain ⟨v, n, c⟩ := k
    obtain ⟨e1, e2, e3⟩ := ih
    simp only at e1 e2 e3
    have hB' : (B : ℝ) ≠ 0 := by exact_mod_cast hB.ne'
    refine ⟨?_, ?_, ?_⟩
    · simp only [Int.cast_add, Int.cast_mul, e1]
      push_cast
      rw [eval_cons a (b :: p)]
      field_simp
      ring
    · simp only [l1_cons] at e2 ⊢; omega
    · simp only [List.length_cons] at e3 ⊢; omega

end rep

/-! ## 2.  The polynomial `γ` -/

/-- `Σₖ pₖ Aᵏ Bⁿ⁻ᵏ` for polynomials `A`, `B`. -/
def homP (Ap Bp : Poly) : ℕ → Poly → Poly
  | _, [] => []
  | n, a :: p => add (smul a (ppow Bp n)) (mul Ap (homP Ap Bp (n - 1) p))

lemma eval_homP (Ap Bp : Poly) (x : ℝ) (hB : eval Bp x ≠ 0) :
    ∀ (p : Poly) (n : ℕ), p.length ≤ n + 1 →
      eval (homP Ap Bp n p) x = eval Bp x ^ n * eval p (eval Ap x / eval Bp x)
  | [], n, _ => by simp [homP]
  | a :: p, n, hl => by
    rw [homP, BernZ.eval_add, BernZ.eval_smul, BernZ.eval_mul, eval_ppow, eval_cons]
    rcases p with _ | ⟨b, p⟩
    · simp [homP]; ring
    · simp only [List.length_cons] at hl
      obtain ⟨m, rfl⟩ : ∃ m, n = m + 1 := ⟨n - 1, by omega⟩
      rw [Nat.add_sub_cancel, eval_homP Ap Bp x hB (b :: p) m (by simp; omega)]
      field_simp
      ring

lemma l1_ppow (q : Poly) : ∀ n, l1 (ppow q n) ≤ l1 q ^ n
  | 0 => by simp [ppow, l1]
  | n + 1 => by
    rw [ppow, pow_succ']
    exact (l1_mul _ _).trans (Nat.mul_le_mul_left _ (l1_ppow q n))

lemma length_ppow2 {q : Poly} (hq : q.length = 2) : ∀ n, (ppow q n).length ≤ n + 1
  | 0 => by simp [ppow]
  | n + 1 => by
    rw [ppow]
    have := length_ppow2 hq n
    exact (length_mul' _ _).trans (by omega)

lemma l1_homP {Ap Bp : Poly} {M : ℕ} (hA : l1 Ap ≤ M) (hB : l1 Bp ≤ M) :
    ∀ (p : Poly) (n : ℕ), p.length ≤ n + 1 → l1 (homP Ap Bp n p) ≤ l1 p * M ^ n
  | [], n, _ => by simp [homP]
  | a :: p, n, hl => by
    rw [homP]
    refine (l1_add _ _).trans ?_
    rw [l1_smul, l1_cons, add_mul]
    refine Nat.add_le_add (Nat.mul_le_mul_left _ ((l1_ppow Bp n).trans (Nat.pow_le_pow_left hB n))) ?_
    refine (l1_mul _ _).trans ?_
    rcases p with _ | ⟨b, p⟩
    · simp [homP]
    · simp only [List.length_cons] at hl
      obtain ⟨m, rfl⟩ : ∃ m, n = m + 1 := ⟨n - 1, by omega⟩
      rw [Nat.add_sub_cancel]
      have ih := l1_homP hA hB (b :: p) m (by simp; omega)
      calc l1 Ap * l1 (homP Ap Bp m (b :: p)) ≤ M * (l1 (b :: p) * M ^ m) := Nat.mul_le_mul hA ih
        _ = l1 (b :: p) * M ^ (m + 1) := by ring

lemma length_homP {Ap Bp : Poly} (hA : Ap.length = 2) (hB : Bp.length = 2) :
    ∀ (p : Poly) (n : ℕ), p.length ≤ n + 1 → (homP Ap Bp n p).length ≤ n + 2
  | [], n, _ => by simp [homP]
  | a :: p, n, hl => by
    rw [homP, length_add, length_smul]
    have h1 := length_ppow2 hB n
    have h2 := length_mul' Ap (homP Ap Bp (n - 1) p)
    rcases p with _ | ⟨b, p⟩
    · simp only [homP, List.length_nil, Nat.zero_sub, add_zero, hA] at h2 ⊢; omega
    · simp only [List.length_cons] at hl
      obtain ⟨m, rfl⟩ : ∃ m, n = m + 1 := ⟨n - 1, by omega⟩
      simp only [Nat.add_sub_cancel] at h2 ⊢
      have ih := length_homP hA hB (b :: p) m (by simp; omega)
      rw [hA] at h2
      omega

/-! ## 3.  Digits by a mask -/

lemma evalZ_cast : ∀ (p : Poly) (x : ℤ), ((evalZ p x : ℤ) : ℝ) = eval p (x : ℝ)
  | [], x => by simp [evalZ]
  | a :: p, x => by simp [evalZ, evalZ_cast p x]

/-- The top bit of each of `L` digits base `2ᴷ`. -/
def maskR (K : ℕ) : ℕ → ℕ
  | 0 => 0
  | L + 1 => 2 ^ (K - 1) + 2 ^ K * maskR K L

lemma land_mask {K : ℕ} (hK : 0 < K) (n m : ℕ) (h : n &&& (2 ^ (K - 1) + 2 ^ K * m) = 0) :
    n % 2 ^ K < 2 ^ (K - 1) ∧ (n / 2 ^ K) &&& m = 0 := by
  have hlt' : 2 ^ (K - 1) < 2 ^ K := Nat.pow_lt_pow_right (by norm_num) (by omega)
  have key : ∀ i, (n.testBit i && (2 ^ K * m + 2 ^ (K - 1)).testBit i) = false := by
    intro i
    rw [← Nat.testBit_and, add_comm, h, Nat.zero_testBit]
  constructor
  · apply Nat.lt_pow_two_of_testBit
    intro i hi
    rcases Nat.eq_or_lt_of_le hi with e | hi
    · subst e
      have k := key (K - 1)
      rw [Nat.testBit_two_pow_mul_add m hlt', if_pos (by omega), Nat.testBit_two_pow_self,
        Bool.and_true] at k
      rw [Nat.testBit_mod_two_pow, k, Bool.and_false]
    · exact Nat.testBit_lt_two_pow ((Nat.mod_lt _ (by positivity)).trans_le
        (Nat.pow_le_pow_right (by norm_num) (by omega)))
  · apply Nat.eq_of_testBit_eq
    intro j
    have k := key (j + K)
    rw [Nat.testBit_two_pow_mul_add m hlt', if_neg (by omega), Nat.add_sub_cancel] at k
    rw [Nat.testBit_and, Nat.testBit_div_two_pow, k, Nat.zero_testBit]

/-- If the digits are small, a number `≥ 0` whose digits' top bits are clear has non-negative
coefficients. -/
lemma nonneg_digits {K : ℕ} (hK : 0 < K) :
    ∀ (L : ℕ) (q : Poly) (n : ℕ), q.length ≤ L → 2 * (l1 q : ℤ) < 2 ^ K →
      evalZ q (2 ^ K) = n → n &&& maskR K L = 0 → ∀ c ∈ q, 0 ≤ c
  | _, [], _, _, _, _, _ => by simp
  | 0, _ :: _, _, hl, _, _, _ => by simp at hl
  | L + 1, c :: q, n, hl, hb, he, hm => by
    have hX : (0 : ℤ) < 2 ^ K := by positivity
    have hcb : 2 * |c| < (2 : ℤ) ^ K := by
      have : (c.natAbs : ℤ) ≤ l1 (c :: q) := by simp
      rw [Int.abs_eq_natAbs]; linarith
    have hqb : 2 * (l1 q : ℤ) < 2 ^ K := by
      have : (l1 q : ℤ) ≤ l1 (c :: q) := by simp
      linarith
    obtain ⟨hlo, hm'⟩ := land_mask hK n (maskR K L) hm
    simp only [evalZ] at he
    set v := evalZ q (2 ^ K)
    have hhalf : (2 : ℤ) ^ K = 2 * 2 ^ (K - 1) := by
      rw [← pow_succ']; congr 1; omega
    have hlo' : ((n % 2 ^ K : ℕ) : ℤ) < 2 ^ (K - 1) := by exact_mod_cast hlo
    have hmod : ((n % 2 ^ K : ℕ) : ℤ) = (n : ℤ) % 2 ^ K := by push_cast; rfl
    have hdiv : ((n / 2 ^ K : ℕ) : ℤ) = (n : ℤ) / 2 ^ K := by push_cast; rfl
    have habs := abs_lt.mp (show |c| < 2 ^ (K - 1) by linarith)
    -- `c ≥ 0`: otherwise the low digit of `n` is `c + 2ᴷ ≥ 2ᴷ⁻¹`
    have hc : 0 ≤ c := by
      by_contra hneg
      push_neg at hneg
      have e : (n : ℤ) % 2 ^ K = c + 2 ^ K := by
        rw [← he, show c + 2 ^ K * v = (c + 2 ^ K) + 2 ^ K * (v - 1) by ring, Int.add_mul_emod_self_left]
        exact Int.emod_eq_of_lt (by linarith) (by linarith)
      rw [← hmod] at e
      linarith
    have e1 : (n : ℤ) % 2 ^ K = c := by
      rw [← he, Int.add_mul_emod_self_left]; exact Int.emod_eq_of_lt hc (by linarith)
    have e2 : (n : ℤ) / 2 ^ K = v := by
      rw [← he, Int.add_mul_ediv_left _ _ hX.ne', Int.ediv_eq_zero_of_lt hc (by linarith), zero_add]
    intro x hx
    rcases List.mem_cons.mp hx with rfl | hx
    · exact hc
    · exact nonneg_digits hK L q (n / 2 ^ K) (by simp at hl; omega) hqb
        (by rw [hdiv, e2]) hm' x hx

lemma eval_nonneg_of_coeffs : ∀ (q : Poly), (∀ c ∈ q, 0 ≤ c) → ∀ t : ℝ, 0 ≤ t → 0 ≤ eval q t
  | [], _, _, _ => by simp
  | c :: q, h, t, ht => by
    rw [eval_cons]
    have := eval_nonneg_of_coeffs q (fun x hx => h x (List.mem_cons_of_mem _ hx)) t ht
    have hc : (0 : ℝ) ≤ c := by exact_mod_cast h c List.mem_cons_self
    positivity

lemma continuous_eval : ∀ p : Poly, Continuous (fun u => eval p u)
  | [] => by simp; exact continuous_const
  | a :: p => by
    simp only [eval_cons]
    exact continuous_const.add (continuous_id.mul (continuous_eval p))

/-! ## 4.  The test -/

/-- **The Kronecker sign test** of `±p` on `[U0/R, U1/R]` (`A = U0 + U1 2ᴷ`, `B = R (1 + 2ᴷ)`,
`M ≥ U0 + U1, 2R`). -/
def hcheck (K M : ℕ) (neg : Bool) (h : KH) : Bool :=
  let v := if neg then -h.v else h.v
  decide (0 < K) && decide (2 * h.b * M ^ h.n < 2 ^ K) && decide (0 ≤ v) &&
    (v.toNat &&& maskR K (h.n + 2) == 0)

lemma rep_neg {A : ℤ} {B : ℕ} {p : Poly} {h : KH} (hp : RepH A B p h) :
    RepH A B (smul (-1) p) ⟨-h.v, h.n, h.b⟩ := by
  have := rep_hsmul (-1) hp
  simpa [hsmul] using this

theorem hcheck_sound {U0 U1 R K M : ℕ} (hR : 0 < R) (hM1 : U0 + U1 ≤ M) (hM2 : 2 * R ≤ M)
    {p : Poly} {h : KH} (hp : RepH ((U0 : ℤ) + U1 * 2 ^ K) (R * (1 + 2 ^ K)) p h)
    (hc : hcheck K M false h = true) {u : ℝ} (hu0 : (U0 : ℝ) / R ≤ u) (hu1 : u ≤ (U1 : ℝ) / R) :
    0 ≤ eval p u := by
  simp only [hcheck, Bool.false_eq_true, if_false, Bool.and_eq_true, decide_eq_true_eq,
    beq_iff_eq] at hc
  obtain ⟨⟨⟨hK, hb⟩, hv0⟩, hm⟩ := hc
  obtain ⟨hv, hl1, hlen⟩ := hp
  set Ap : Poly := [(U0 : ℤ), U1]
  set Bp : Poly := [(R : ℤ), R]
  set q := homP Ap Bp h.n p
  have hRr : (0 : ℝ) < R := by exact_mod_cast hR
  have eA : ∀ t : ℝ, eval Ap t = U0 + U1 * t := fun t => by simp [Ap]; ring
  have eB : ∀ t : ℝ, eval Bp t = R * (1 + t) := fun t => by simp [Bp]; ring
  -- the number is `γ(2ᴷ)`
  have hq : evalZ q (2 ^ K) = h.v := by
    have : ((evalZ q (2 ^ K) : ℤ) : ℝ) = (h.v : ℝ) := by
      rw [evalZ_cast, eval_homP Ap Bp _ (by rw [eB]; positivity) p h.n hlen, hv, eA, eB]
      push_cast
      ring_nf
    exact_mod_cast this
  -- its coefficients are `≥ 0`
  have hlq : l1 q ≤ h.b * M ^ h.n :=
    (l1_homP (by simp [Ap, l1]; omega) (by simp [Bp, l1]; omega) p h.n hlen).trans
      (Nat.mul_le_mul_right _ hl1)
  have hcoef : ∀ c ∈ q, 0 ≤ c := by
    refine nonneg_digits hK (h.n + 2) q h.v.toNat
      (length_homP (by simp [Ap]) (by simp [Bp]) p h.n hlen) ?_ ?_ hm
    · have : 2 * l1 q < 2 ^ K := lt_of_le_of_lt (by nlinarith) hb
      exact_mod_cast this
    · rw [hq]; exact (Int.toNat_of_nonneg hv0).symm
  have hγ : ∀ t : ℝ, 0 ≤ t → 0 ≤ (R * (1 + t)) ^ h.n * eval p ((U0 + U1 * t) / (R * (1 + t))) := by
    intro t ht
    have := eval_nonneg_of_coeffs q hcoef t ht
    rwa [eval_homP Ap Bp _ (by rw [eB]; positivity) p h.n hlen, eA, eB] at this
  have hpos : ∀ t : ℝ, 0 ≤ t → 0 ≤ eval p ((U0 + U1 * t) / (R * (1 + t))) := fun t ht =>
    (mul_nonneg_iff_of_pos_left (pow_pos (by positivity) _)).mp (hγ t ht)
  -- every pose of the half-open bin is reached
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

/-- The test of `±p` (`neg`: of `−p`). -/
theorem hcheck_sound' {U0 U1 R K M : ℕ} (hR : 0 < R) (hM1 : U0 + U1 ≤ M) (hM2 : 2 * R ≤ M)
    {p : Poly} {h : KH} (hp : RepH ((U0 : ℤ) + U1 * 2 ^ K) (R * (1 + 2 ^ K)) p h) {neg : Bool}
    (hc : hcheck K M neg h = true) {u : ℝ} (hu0 : (U0 : ℝ) / R ≤ u) (hu1 : u ≤ (U1 : ℝ) / R) :
    0 ≤ eval (if neg then smul (-1) p else p) u := by
  cases neg
  · exact hcheck_sound hR hM1 hM2 hp hc hu0 hu1
  · exact hcheck_sound (h := ⟨-h.v, h.n, h.b⟩) hR hM1 hM2 (rep_neg hp) (by simpa [hcheck] using hc) hu0 hu1

end KArith

end SquarePacking
