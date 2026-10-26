import Mathlib

/-!
# Bernstein certificates of any degree, in integer arithmetic

`ZeroMargin.lean` bounds polynomials of degree `≤ 4` in `u = tan(θ/2)` on a bin by their Bernstein
coefficients (`maxBern`, `ZMTree.bOk`).  Lemma R / `SPLIT`, the wall corners of Corollary L
(`notes/lean-segments.md` §5) and the vertex bounds of Lemma E (`search/QUADRANT_EXACT.md` §4.4) need
the same test at **any degree**.  This file gives it, once, in a form the kernel evaluates with
integer arithmetic only.

## The test

A polynomial `p(u) = Σ_j a_j u^j` with `a_j ∈ ℤ` is a list `Poly` (lowest degree first).  On the bin
`u ∈ [U0/R, U1/R]` (naturals, `R > 0`) put `u = (U0 + H t)/R`, `H = U1 − U0`, `t ∈ [0, 1]`:

* `hom U0 H R n p` is the integer polynomial in `t` equal to `Rⁿ · p((U0 + H t)/R)`
  (`eval_hom`; `n ≥ deg p`), by Horner's rule;
* its Bernstein form of degree `n`: `Σ_k b_k tᵏ = Σ_i γ_i tⁱ (1 − t)ⁿ⁻ⁱ` with
  `γ_i = Σ_{k ≤ i} C(n − k, i − k) b_k` (`sum_eq_bern`; the binomial factors of the usual Bernstein
  basis are absorbed into `γ`, so every `γ_i` is an integer and nothing is divided);
* `check`: all `γ_i ≥ 0` ⇒ `p ≥ 0` on the bin (`nonneg_of_check`); `checkPos`: moreover
  `γ_0 > 0` and `γ_n > 0` ⇒ `p > 0` on the bin (`pos_of_checkPos`).

Binomials are computed from factorials (`chooseF`), not by `Nat.choose`'s Pascal recursion, whose
kernel evaluation is exponential.  Nothing about the polynomial is trusted: the theorems hold for
every input.
-/

open Finset

namespace SquarePacking
namespace BernZ

/-- An integer polynomial, coefficients lowest degree first. -/
abbrev Poly := List ℤ

/-- Evaluation at a real number (Horner). -/
noncomputable def eval : Poly → ℝ → ℝ
  | [], _ => 0
  | a :: p, x => a + x * eval p x

@[simp] lemma eval_nil (x : ℝ) : eval [] x = 0 := rfl

@[simp] lemma eval_cons (a : ℤ) (p : Poly) (x : ℝ) : eval (a :: p) x = a + x * eval p x := rfl

/-! ## 1.  Ring operations on `Poly` -/

def add : Poly → Poly → Poly
  | [], q => q
  | a :: p, [] => a :: p
  | a :: p, b :: q => (a + b) :: add p q

lemma eval_add : ∀ (p q : Poly) (x : ℝ), eval (add p q) x = eval p x + eval q x
  | [], q, x => by simp [add]
  | a :: p, [], x => by simp [add]
  | a :: p, b :: q, x => by
    simp only [add, eval_cons, eval_add p q x]
    push_cast
    ring

def smul (c : ℤ) (p : Poly) : Poly := p.map (c * ·)

lemma eval_smul (c : ℤ) : ∀ (p : Poly) (x : ℝ), eval (smul c p) x = c * eval p x
  | [], x => by simp [smul]
  | a :: p, x => by
    have ih := eval_smul c p x
    simp only [smul, List.map_cons, eval_cons] at ih ⊢
    rw [ih]
    push_cast
    ring

def mul : Poly → Poly → Poly
  | [], _ => []
  | a :: p, q => add (smul a q) (0 :: mul p q)

lemma eval_mul : ∀ (p q : Poly) (x : ℝ), eval (mul p q) x = eval p x * eval q x
  | [], q, x => by simp [mul]
  | a :: p, q, x => by
    rw [mul, eval_add, eval_smul, eval_cons, eval_mul p q x, eval_cons]
    push_cast
    ring

/-! ## 2.  The substitution `u = (U0 + H t)/R` -/

/-- `hom U0 H R n p` is `Rⁿ · p((U0 + H t)/R)` as a polynomial in `t` (for `deg p ≤ n`). -/
def hom (U0 H R : ℤ) : ℕ → Poly → Poly
  | _, [] => []
  | n, [a] => [a * R ^ n]
  | n, a :: p => add [a * R ^ n] (mul [U0, H] (hom U0 H R (n - 1) p))

lemma eval_hom (U0 H R : ℤ) (hR : (R : ℝ) ≠ 0) (t : ℝ) (p : Poly) :
    ∀ n : ℕ, p.length ≤ n + 1 →
      eval (hom U0 H R n p) t = (R : ℝ) ^ n * eval p ((U0 + H * t) / R) := by
  induction p with
  | nil => intro n _; simp [hom]
  | cons a p ih =>
    intro n hl
    cases p with
    | nil =>
      simp only [hom, eval_cons, eval_nil, mul_zero, add_zero]
      push_cast
      ring
    | cons b q =>
      rw [show hom U0 H R n (a :: b :: q) =
        add [a * R ^ n] (mul [U0, H] (hom U0 H R (n - 1) (b :: q))) from rfl, eval_add, eval_mul]
      simp only [List.length_cons] at hl
      obtain ⟨m, rfl⟩ : ∃ m, n = m + 1 := ⟨n - 1, by omega⟩
      rw [ih (m + 1 - 1) (by simp only [List.length_cons]; omega), Nat.add_sub_cancel]
      set x : ℝ := ((U0 : ℝ) + (H : ℝ) * t) / R with hxdef
      have hx : (R : ℝ) * x = U0 + H * t := by rw [hxdef]; field_simp
      rw [eval_cons a (b :: q) x]
      generalize eval (b :: q) x = E
      simp only [eval_cons, eval_nil, mul_zero, add_zero]
      push_cast
      linear_combination (-(R : ℝ) ^ m * E) * hx

/-! ## 3.  The Bernstein form -/

lemma eval_eq_sum (p : Poly) (x : ℝ) :
    eval p x = ∑ k ∈ range p.length, (p.getD k 0 : ℝ) * x ^ k := by
  induction p with
  | nil => simp
  | cons a p ih =>
    rw [eval_cons, ih, List.length_cons, Finset.sum_range_succ', Finset.mul_sum]
    simp only [List.getD_cons_succ, List.getD_cons_zero, pow_zero, mul_one]
    rw [add_comm]
    congr 1
    refine Finset.sum_congr rfl fun k _ => ?_
    ring

lemma eval_eq_sum' (p : Poly) (x : ℝ) {n : ℕ} (h : p.length ≤ n + 1) :
    eval p x = ∑ k ∈ range (n + 1), (p.getD k 0 : ℝ) * x ^ k := by
  rw [eval_eq_sum]
  refine Finset.sum_subset (Finset.range_mono h) fun k _ hk => ?_
  simp only [Finset.mem_range, not_lt] at hk
  have h0 : p[k]? = none := List.getElem?_eq_none hk
  simp [List.getD, h0]

/-- The (scaled) Bernstein coefficient `γ_i = Σ_{k ≤ i} C(n − k, i − k) b_k`. -/
def gam (n : ℕ) (b : Poly) (i : ℕ) : ℤ :=
  ∑ k ∈ range (i + 1), ((n - k).choose (i - k) : ℤ) * b.getD k 0

/-- `tᵏ` in the degree-`n` Bernstein basis. -/
lemma pow_eq_bern (n k : ℕ) (hk : k ≤ n) (t : ℝ) :
    t ^ k = ∑ i ∈ Ico k (n + 1), ((n - k).choose (i - k) : ℝ) * (t ^ i * (1 - t) ^ (n - i)) := by
  rw [Finset.sum_Ico_eq_sum_range, show n + 1 - k = n - k + 1 by omega]
  have h1 := add_pow t (1 - t) (n - k)
  rw [add_sub_cancel, one_pow] at h1
  calc t ^ k = t ^ k * 1 := (mul_one _).symm
    _ = t ^ k * ∑ j ∈ range (n - k + 1), t ^ j * (1 - t) ^ (n - k - j) * ((n - k).choose j : ℝ) := by
        rw [← h1]
    _ = _ := by
        rw [Finset.mul_sum]
        refine Finset.sum_congr rfl fun j hj => ?_
        rw [Finset.mem_range] at hj
        rw [Nat.add_sub_cancel_left, pow_add, show n - (k + j) = n - k - j by omega]
        ring

/-- **The Bernstein form**: `Σ_{k ≤ n} b_k tᵏ = Σ_{i ≤ n} γ_i tⁱ (1 − t)ⁿ⁻ⁱ`. -/
theorem sum_eq_bern (n : ℕ) (b : Poly) (t : ℝ) :
    ∑ k ∈ range (n + 1), (b.getD k 0 : ℝ) * t ^ k =
      ∑ i ∈ range (n + 1), (gam n b i : ℝ) * (t ^ i * (1 - t) ^ (n - i)) := by
  have step1 : ∑ k ∈ range (n + 1), (b.getD k 0 : ℝ) * t ^ k =
      ∑ k ∈ Ico 0 (n + 1), ∑ i ∈ Ico k (n + 1),
        (b.getD k 0 : ℝ) * (((n - k).choose (i - k) : ℝ) * (t ^ i * (1 - t) ^ (n - i))) := by
    rw [← Finset.range_eq_Ico]
    refine Finset.sum_congr rfl fun k hk => ?_
    rw [Finset.mem_range] at hk
    rw [pow_eq_bern n k (by omega) t, Finset.mul_sum]
  rw [step1, Finset.sum_Ico_Ico_comm, ← Finset.range_eq_Ico]
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [← Finset.range_eq_Ico, gam, Int.cast_sum, Finset.sum_mul]
  refine Finset.sum_congr rfl fun k _ => ?_
  push_cast
  ring

/-! ## 4.  Kernel-friendly evaluation -/

/-- `C(n, k)` from factorials (linear kernel cost; `Nat.choose`'s recursion is exponential). -/
def chooseF (n k : ℕ) : ℕ := if k ≤ n then n.factorial / (k.factorial * (n - k).factorial) else 0

lemma chooseF_eq (n k : ℕ) : chooseF n k = n.choose k := by
  unfold chooseF
  split_ifs with h
  · exact (Nat.choose_eq_factorial_div_factorial h).symm
  · exact (Nat.choose_eq_zero_of_lt (by omega)).symm

lemma list_sum_range (f : ℕ → ℤ) (m : ℕ) : ((List.range m).map f).sum = ∑ k ∈ range m, f k := by
  induction m with
  | zero => simp
  | succ m ih => rw [List.range_succ, List.map_append, List.sum_append, ih, Finset.sum_range_succ]; simp

/-- `γ_i`, as the kernel computes it. -/
def gamK (n : ℕ) (b : Poly) (i : ℕ) : ℤ :=
  ((List.range (i + 1)).map fun k => (chooseF (n - k) (i - k) : ℤ) * b.getD k 0).sum

lemma gamK_eq (n : ℕ) (b : Poly) (i : ℕ) : gamK n b i = gam n b i := by
  rw [gamK, gam, list_sum_range]
  simp only [chooseF_eq]

/-- The coefficients in `t` of `Rⁿ p(u)` on the bin `[U0/R, U1/R]`. -/
def tPoly (p : Poly) (n U0 U1 R : ℕ) : Poly := hom U0 ((U1 : ℤ) - U0) R n p

/-- **The test**: `p ≥ 0` on `[U0/R, U1/R]` because all degree-`n` Bernstein coefficients are `≥ 0`. -/
def check (p : Poly) (n U0 U1 R : ℕ) : Bool :=
  decide (p.length ≤ n + 1) && decide ((tPoly p n U0 U1 R).length ≤ n + 1) &&
    (List.range (n + 1)).all fun i => decide (0 ≤ gamK n (tPoly p n U0 U1 R) i)

/-- **The strict test**: moreover the two end coefficients are `> 0`. -/
def checkPos (p : Poly) (n U0 U1 R : ℕ) : Bool :=
  check p n U0 U1 R && decide (0 < gamK n (tPoly p n U0 U1 R) 0) &&
    decide (0 < gamK n (tPoly p n U0 U1 R) n)

/-- The point `t ∈ [0,1]` of a pose `u` of the bin, and the Bernstein identity there. -/
lemma bern_at {p : Poly} {n U0 U1 R : ℕ} (hp : p.length ≤ n + 1)
    (hb : (tPoly p n U0 U1 R).length ≤ n + 1) (hR : 0 < R)
    {u : ℝ} (hu0 : (U0 : ℝ) / R ≤ u) (hu1 : u ≤ (U1 : ℝ) / R) :
    ∃ t : ℝ, 0 ≤ t ∧ t ≤ 1 ∧ (R : ℝ) ^ n * eval p u =
      ∑ i ∈ range (n + 1), (gamK n (tPoly p n U0 U1 R) i : ℝ) * (t ^ i * (1 - t) ^ (n - i)) := by
  have hRr : (0 : ℝ) < R := by exact_mod_cast hR
  have hRu0 : (U0 : ℝ) ≤ R * u := by rw [div_le_iff₀ hRr] at hu0; linarith
  have hRu1 : R * u ≤ (U1 : ℝ) := by rw [le_div_iff₀ hRr] at hu1; linarith
  -- a parameter `t ∈ [0,1]` with `U0 + H t = R u`
  obtain ⟨t, ht0, ht1, ht⟩ : ∃ t : ℝ, 0 ≤ t ∧ t ≤ 1 ∧ (U0 : ℝ) + ((U1 : ℝ) - U0) * t = R * u := by
    rcases eq_or_lt_of_le (le_trans hRu0 hRu1) with h | h
    · exact ⟨0, le_rfl, zero_le_one, by rw [mul_zero, add_zero]; linarith⟩
    · refine ⟨(R * u - U0) / (U1 - U0), div_nonneg (by linarith) (by linarith),
        (div_le_one (by linarith)).mpr (by linarith), ?_⟩
      field_simp
      ring
  refine ⟨t, ht0, ht1, ?_⟩
  have hR0 : ((R : ℤ) : ℝ) ≠ 0 := by push_cast; exact hRr.ne'
  have e1 := eval_hom (U0 : ℤ) ((U1 : ℤ) - U0) (R : ℤ) hR0 t p n hp
  have e2 : (((U0 : ℤ) : ℝ) + (((U1 : ℤ) - U0 : ℤ) : ℝ) * t) / ((R : ℤ) : ℝ) = u := by
    push_cast
    rw [ht]
    field_simp
  rw [e2] at e1
  push_cast at e1
  rw [← e1, ← tPoly, eval_eq_sum' _ t hb, sum_eq_bern]
  simp only [gamK_eq]

/-- **Soundness of `check`.** -/
theorem nonneg_of_check {p : Poly} {n U0 U1 R : ℕ} (h : check p n U0 U1 R = true) (hR : 0 < R)
    {u : ℝ} (hu0 : (U0 : ℝ) / R ≤ u) (hu1 : u ≤ (U1 : ℝ) / R) : 0 ≤ eval p u := by
  simp only [check, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true, List.mem_range] at h
  obtain ⟨⟨hp, hb⟩, hg⟩ := h
  obtain ⟨t, ht0, ht1, he⟩ := bern_at hp hb hR hu0 hu1
  have hsum : 0 ≤ (R : ℝ) ^ n * eval p u := by
    rw [he]
    refine Finset.sum_nonneg fun i hi => mul_nonneg ?_ (mul_nonneg (pow_nonneg ht0 _)
      (pow_nonneg (by linarith) _))
    exact_mod_cast hg i (Finset.mem_range.mp hi)
  have hRn : (0 : ℝ) < (R : ℝ) ^ n := pow_pos (by exact_mod_cast hR) n
  exact (mul_nonneg_iff_of_pos_left hRn).mp hsum

/-- **Soundness of `checkPos`.** -/
theorem pos_of_checkPos {p : Poly} {n U0 U1 R : ℕ} (h : checkPos p n U0 U1 R = true) (hR : 0 < R)
    {u : ℝ} (hu0 : (U0 : ℝ) / R ≤ u) (hu1 : u ≤ (U1 : ℝ) / R) : 0 < eval p u := by
  simp only [checkPos, check, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true,
    List.mem_range] at h
  obtain ⟨⟨⟨⟨hp, hb⟩, hg⟩, hg0⟩, hgn⟩ := h
  obtain ⟨t, ht0, ht1, he⟩ := bern_at hp hb hR hu0 hu1
  set f : ℕ → ℝ := fun i => (gamK n (tPoly p n U0 U1 R) i : ℝ) * (t ^ i * (1 - t) ^ (n - i)) with hf
  have hf0 : ∀ i ∈ range (n + 1), 0 ≤ f i := fun i hi =>
    mul_nonneg (by exact_mod_cast hg i (Finset.mem_range.mp hi))
      (mul_nonneg (pow_nonneg ht0 _) (pow_nonneg (by linarith) _))
  have hg0r : (0 : ℝ) < gamK n (tPoly p n U0 U1 R) 0 := by exact_mod_cast hg0
  have hgnr : (0 : ℝ) < gamK n (tPoly p n U0 U1 R) n := by exact_mod_cast hgn
  have hpos : 0 < ∑ i ∈ range (n + 1), f i := by
    rcases Nat.eq_zero_or_pos n with rfl | hn
    · simpa [hf] using hg0r
    · have h2 : f 0 + f n ≤ ∑ i ∈ range (n + 1), f i :=
        Finset.add_le_sum hf0 (Finset.mem_range.mpr (by omega)) (Finset.mem_range.mpr (by omega))
          (by omega)
      have h3 : 0 < f 0 + f n := by
        simp only [hf, pow_zero, one_mul, Nat.sub_zero, Nat.sub_self, mul_one]
        rcases lt_or_eq_of_le ht1 with ht | ht
        · have : 0 < (1 - t) ^ n := pow_pos (by linarith) n
          nlinarith [mul_nonneg hgnr.le (pow_nonneg ht0 n)]
        · subst ht
          simp only [one_pow, mul_one, sub_self]
          rw [zero_pow (by omega), mul_zero, zero_add]
          exact hgnr
      linarith
  have hRn : (0 : ℝ) < (R : ℝ) ^ n := pow_pos (by exact_mod_cast hR) n
  have : 0 < (R : ℝ) ^ n * eval p u := by rw [he]; exact hpos
  exact (mul_pos_iff_of_pos_left hRn).mp this

end BernZ
end SquarePacking
