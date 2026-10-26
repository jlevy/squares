import Sqpack.RatU

/-!
# Kronecker arithmetic: polynomials as one integer

The kernel evaluates list polynomials slowly (every coefficient operation is many reduction steps).
Here a polynomial `p` is carried as `KP`: its value `p(X)` at a large integer `X` (one number: sums
and products are single big-integer operations), with an upper bound on `Σ |pᵢ|` and on the length.
When `2 · bound < X`, the coefficients are recovered exactly as the balanced digits of `p(X)` in
base `X` (`kdig_getD`).  `RepP X k p` says that `k` carries `p`.
-/

namespace SquarePacking

namespace KArith

open BernZ RatU

/-! ## 1.  Evaluation at an integer, and the `ℓ¹` size -/

def evalZ : Poly → ℤ → ℤ
  | [], _ => 0
  | a :: p, x => a + x * evalZ p x

lemma evalZ_add : ∀ (p q : Poly) (x : ℤ), evalZ (add p q) x = evalZ p x + evalZ q x
  | [], q, x => by simp [add, evalZ]
  | a :: p, [], x => by simp [add, evalZ]
  | a :: p, b :: q, x => by simp only [add, evalZ, evalZ_add p q x]; ring

lemma evalZ_smul (c : ℤ) : ∀ (p : Poly) (x : ℤ), evalZ (smul c p) x = c * evalZ p x
  | [], x => by simp [smul, evalZ]
  | a :: p, x => by
    have ih := evalZ_smul c p x
    simp only [smul, List.map_cons, evalZ] at ih ⊢
    rw [ih]; ring

lemma evalZ_mul : ∀ (p q : Poly) (x : ℤ), evalZ (mul p q) x = evalZ p x * evalZ q x
  | [], q, x => by simp [mul, evalZ]
  | a :: p, q, x => by
    rw [mul, evalZ_add, evalZ_smul, evalZ, evalZ_mul p q x, evalZ]; ring

def l1 (p : Poly) : ℕ := (p.map Int.natAbs).sum

@[simp] lemma l1_nil : l1 [] = 0 := rfl
@[simp] lemma l1_cons (a : ℤ) (p : Poly) : l1 (a :: p) = a.natAbs + l1 p := by simp [l1]

lemma l1_add : ∀ (p q : Poly), l1 (add p q) ≤ l1 p + l1 q
  | [], q => by simp [add]
  | a :: p, [] => by simp [add]
  | a :: p, b :: q => by
    simp only [add, l1_cons]
    have := l1_add p q
    have := Int.natAbs_add_le a b
    omega

lemma l1_smul (c : ℤ) : ∀ (p : Poly), l1 (smul c p) = c.natAbs * l1 p
  | [] => by simp [smul]
  | a :: p => by
    have ih := l1_smul c p
    simp only [smul, List.map_cons, l1_cons] at ih ⊢
    rw [ih, Int.natAbs_mul]; ring

lemma l1_mul : ∀ (p q : Poly), l1 (mul p q) ≤ l1 p * l1 q
  | [], q => by simp [mul]
  | a :: p, q => by
    rw [mul]
    refine (l1_add _ _).trans ?_
    rw [l1_smul, l1_cons, l1_cons, Int.natAbs_zero, zero_add, add_mul]
    exact Nat.add_le_add_left (l1_mul p q) _

lemma length_add : ∀ (p q : Poly), (add p q).length = max p.length q.length
  | [], q => by simp [add]
  | a :: p, [] => by simp [add]
  | a :: p, b :: q => by simp [add, length_add p q, Nat.succ_max_succ]

lemma length_smul (c : ℤ) (p : Poly) : (smul c p).length = p.length := by simp [smul]

lemma length_mul : ∀ (p q : Poly), (mul p q).length ≤ p.length + q.length
  | [], q => by simp [mul]
  | a :: p, q => by
    rw [mul, length_add, length_smul]
    have := length_mul p q
    simp only [List.length_cons]
    omega

/-! ## 2.  Kronecker images -/

/-- `v = p(X)`, `Σ |pᵢ| ≤ b`, `length p ≤ n`. -/
structure KP where
  v : ℤ
  b : ℕ
  n : ℕ

def RepP (X : ℤ) (k : KP) (p : Poly) : Prop := k.v = evalZ p X ∧ l1 p ≤ k.b ∧ p.length ≤ k.n

def kofP (X : ℤ) (p : Poly) : KP := ⟨evalZ p X, l1 p, p.length⟩
def kadd (p q : KP) : KP := ⟨p.v + q.v, p.b + q.b, max p.n q.n⟩
def ksmul (c : ℤ) (p : KP) : KP := ⟨c * p.v, c.natAbs * p.b, p.n⟩
def kmul (p q : KP) : KP := ⟨p.v * q.v, p.b * q.b, p.n + q.n⟩
def kone : KP := ⟨1, 1, 1⟩
def kpow (p : KP) : ℕ → KP
  | 0 => kone
  | n + 1 => kmul p (kpow p n)

lemma rep_kofP (X : ℤ) (p : Poly) : RepP X (kofP X p) p := ⟨rfl, le_rfl, le_rfl⟩

lemma rep_kadd {X : ℤ} {k k' : KP} {p q : Poly} (h : RepP X k p) (h' : RepP X k' q) :
    RepP X (kadd k k') (add p q) := by
  obtain ⟨a, b, c⟩ := h; obtain ⟨a', b', c'⟩ := h'
  refine ⟨by simp [kadd, evalZ_add, a, a'], (l1_add p q).trans (by simp [kadd]; omega), ?_⟩
  simp only [kadd, length_add]; omega

lemma rep_ksmul {X : ℤ} {k : KP} {p : Poly} (c : ℤ) (h : RepP X k p) : RepP X (ksmul c k) (smul c p) := by
  obtain ⟨a, b, d⟩ := h
  refine ⟨by simp [ksmul, evalZ_smul, a], by rw [l1_smul]; exact Nat.mul_le_mul_left _ b, ?_⟩
  simp only [ksmul, length_smul]; exact d

lemma rep_kmul {X : ℤ} {k k' : KP} {p q : Poly} (h : RepP X k p) (h' : RepP X k' q) :
    RepP X (kmul k k') (mul p q) := by
  obtain ⟨a, b, c⟩ := h; obtain ⟨a', b', c'⟩ := h'
  refine ⟨by simp [kmul, evalZ_mul, a, a'], (l1_mul p q).trans (Nat.mul_le_mul b b'), ?_⟩
  exact (length_mul p q).trans (by simp only [kmul]; omega)

lemma rep_kpow {X : ℤ} {k : KP} {p : Poly} (h : RepP X k p) : ∀ n, RepP X (kpow k n) (ppow p n)
  | 0 => ⟨by simp [kpow, kone, ppow, evalZ], by simp [kpow, kone, ppow], by simp [kpow, kone, ppow]⟩
  | n + 1 => by rw [kpow, ppow]; exact rep_kmul h (rep_kpow h n)

/-! ## 3.  The digits -/

/-- `m` balanced digits of `v` in base `X` (each in `[−X/2, X/2)`), least significant first. -/
def kdig (X : ℤ) : ℕ → ℤ → Poly
  | 0, _ => []
  | m + 1, v =>
    let r := v % X
    let a := if X ≤ 2 * r then r - X else r
    a :: kdig X m ((v - a) / X)

lemma kdig_length (X : ℤ) : ∀ (m : ℕ) (v : ℤ), (kdig X m v).length = m
  | 0, _ => rfl
  | m + 1, v => by simp [kdig, kdig_length X m]

lemma kdig_succ {X : ℤ} (hX : 0 < X) (m : ℕ) {a : ℤ} (q : ℤ) (ha : 2 * |a| < X) :
    kdig X (m + 1) (a + X * q) = a :: kdig X m q := by
  have e : (if X ≤ 2 * ((a + X * q) % X) then (a + X * q) % X - X else (a + X * q) % X) = a := by
    rw [Int.add_mul_emod_self_left]
    rcases le_or_gt 0 a with h0 | h0
    · rw [abs_of_nonneg h0] at ha
      rw [Int.emod_eq_of_lt h0 (by linarith), if_neg (by linarith)]
    · rw [abs_of_neg h0] at ha
      have e : a % X = a + X := by
        rw [← Int.add_mul_emod_self_left a X 1, mul_one, Int.emod_eq_of_lt (by linarith) (by linarith)]
      rw [e, if_pos (by linarith)]
      ring
  show (let r := (a + X * q) % X; let a' := if X ≤ 2 * r then r - X else r;
    a' :: kdig X m ((a + X * q - a') / X)) = _
  simp only []
  rw [e, show a + X * q - a = X * q by ring, Int.mul_ediv_cancel_left _ hX.ne']

lemma kdig_zero {X : ℤ} (hX : 0 < X) : ∀ m : ℕ, kdig X m 0 = List.replicate m 0
  | 0 => rfl
  | m + 1 => by
    have := kdig_succ hX m (a := 0) 0 (by simpa using hX)
    simp only [mul_zero, add_zero] at this
    rw [this, kdig_zero hX m]; rfl

lemma kdig_getD {X : ℤ} (hX : 0 < X) :
    ∀ (m : ℕ) (p : Poly), p.length ≤ m → 2 * (l1 p : ℤ) < X →
      ∀ i, (kdig X m (evalZ p X)).getD i 0 = p.getD i 0
  | 0, p, hl, _, i => by
    have : p = [] := List.eq_nil_of_length_eq_zero (by omega)
    subst this; simp [kdig]
  | m + 1, [], _, _, i => by
    rw [show evalZ [] X = 0 from rfl, kdig_zero hX]
    simp [List.getD_eq_getElem?_getD, List.getElem?_replicate]; split_ifs <;> rfl
  | m + 1, a :: p, hl, hb, i => by
    have ha : 2 * |a| < X := by
      have : (a.natAbs : ℤ) ≤ (l1 (a :: p) : ℤ) := by simp
      rw [Int.abs_eq_natAbs]; linarith
    have hb' : 2 * (l1 p : ℤ) < X := by
      have : (l1 p : ℤ) ≤ (l1 (a :: p) : ℤ) := by simp
      linarith
    rw [show evalZ (a :: p) X = a + X * evalZ p X from rfl, kdig_succ hX m _ ha]
    cases i with
    | zero => rfl
    | succ i =>
      simp only [List.getD_cons_succ]
      exact kdig_getD hX m p (by simp at hl; omega) hb' i

/-- The real evaluation depends only on the coefficients (`getD`), not on trailing zeros. -/
lemma eval_congr : ∀ (p q : Poly), (∀ i, p.getD i 0 = q.getD i 0) → ∀ u, eval p u = eval q u
  | [], [], _, _ => rfl
  | [], b :: q, h, u => by
    have h0 := h 0; simp at h0
    have ih := eval_congr [] q (fun i => by have := h (i + 1); simpa using this) u
    simp [eval_cons, ← h0, ← ih]
  | a :: p, [], h, u => by
    have h0 := h 0; simp at h0
    have ih := eval_congr p [] (fun i => by have := h (i + 1); simpa using this) u
    simp [eval_cons, h0, ih]
  | a :: p, b :: q, h, u => by
    have h0 := h 0; simp at h0
    have ih := eval_congr p q (fun i => by have := h (i + 1); simpa using this) u
    simp [eval_cons, h0, ih]

/-- **The digits of a carried polynomial** have its coefficients. -/
lemma rep_kdig {X : ℤ} (hX : 0 < X) {k : KP} {p : Poly} (h : RepP X k p) (hb : 2 * (k.b : ℤ) < X) :
    ∀ i, (kdig X k.n k.v).getD i 0 = p.getD i 0 := by
  obtain ⟨a, b, c⟩ := h
  rw [a]
  exact kdig_getD hX k.n p c (lt_of_le_of_lt (by exact_mod_cast Nat.mul_le_mul_left 2 b) hb)

end KArith

end SquarePacking
