import Sqpack.ExactPack
import Sqpack.ShadowCheck

/-!
# A checker for packings over a number field

Data (`Cert`): a polynomial `f ∈ ℚ[T]`, a rational interval `[a, b]`, and for each square a centre `(x, y)` and an
angle parameter `u` (polynomials in `T`), plus a rotation by `m` quarter turns; the side `S` (a polynomial in `T`);
and for each pair `i < j` the side line that separates it (`sep i j`: a side of `i` (`true`) or of `j`, and which).

Meaning: for any real root `t ∈ [a, b]` of `f`, square `i` has centre `(x(t), y(t))` and rotation
`(c, s) = R^m ((1 - u²)/(1 + u²), 2u/(1 + u²))` at `u = u(t)`; the container has side `S(t)`.

`check` decides, with exact rational arithmetic only, that every corner lies in the box and every pair is separated by
the given side line.  Each such condition, multiplied by a positive denominator, is `N(t) ≥ 0` for an explicit
`N ∈ ℚ[T]` (`boxN`, `sepN`), and is proved either as an identity (`N = q f`, so `N(t) = 0`) or by a bound:
`r = N - q f` has `r(t) = N(t)`, and `r(m) - w B > 0` where `m` is the midpoint, `w` the half-width and `B` bounds
`|r'|` (`posOK`).  Polynomial division is not trusted: `N = q f + r` is re-checked as an identity of coefficient lists.

Rational shadows (`ShadowCheck`): each square also carries rational enclosures of `(x, y, c, s)` (`encl`, proved once
per square by `enclOK`), and `S ≥ Sl`.  Walls and pairs try the cheap interval / disc tests first and fall back to
the exact conditions only where those fail (in practice: at contacts), so the field arithmetic is O(contacts), not
O(n²).

`packs_of_check`: `check C = true`, `f(t) = 0`, `t ∈ [a, b]` ⟹ `Packs n (S(t))`.  With a sign change of `f` on
`[a, b]` (`exists_root`), such a `t` exists.  Everything is decidable, so a concrete certificate is checked by
`decide +kernel` (no `native_decide`).
-/

namespace UnitSquarePacking.EC

/-! ## Polynomials as coefficient lists -/

/-- Polynomials over `ℚ`, ascending coefficients. -/
abbrev Poly := List ℚ

def peval : Poly → ℝ → ℝ
  | [], _ => 0
  | c :: p, t => (c : ℝ) + t * peval p t

def qeval : Poly → ℚ → ℚ
  | [], _ => 0
  | c :: p, t => c + t * qeval p t

def padd : Poly → Poly → Poly
  | [], q => q
  | a :: p, [] => a :: p
  | a :: p, b :: q => (a + b) :: padd p q

def psmul (c : ℚ) (p : Poly) : Poly := p.map (c * ·)

def psub (p q : Poly) : Poly := padd p (psmul (-1) q)

def pmul : Poly → Poly → Poly
  | [], _ => []
  | a :: p, q => padd (psmul a q) (0 :: pmul p q)

/-- `p ∘ q`, by Horner. -/
def pcomp : Poly → Poly → Poly
  | [], _ => []
  | c :: p, q => padd [c] (pmul q (pcomp p q))

@[simp] lemma peval_nil (t : ℝ) : peval [] t = 0 := rfl
@[simp] lemma peval_cons (c : ℚ) (p : Poly) (t : ℝ) : peval (c :: p) t = c + t * peval p t := rfl

@[simp] lemma peval_padd (p q : Poly) (t : ℝ) : peval (padd p q) t = peval p t + peval q t := by
  induction p generalizing q with
  | nil => simp [padd]
  | cons a p ih =>
    cases q with
    | nil => simp [padd]
    | cons b q => simp only [padd, peval_cons, ih]; push_cast; ring

@[simp] lemma peval_psmul (c : ℚ) (p : Poly) (t : ℝ) : peval (psmul c p) t = c * peval p t := by
  induction p with
  | nil => simp [psmul]
  | cons a p ih =>
    simp only [psmul, List.map_cons, peval_cons] at ih ⊢; rw [ih]; push_cast; ring

@[simp] lemma peval_psub (p q : Poly) (t : ℝ) : peval (psub p q) t = peval p t - peval q t := by
  simp [psub]; ring

@[simp] lemma peval_pmul (p q : Poly) (t : ℝ) : peval (pmul p q) t = peval p t * peval q t := by
  induction p with
  | nil => simp [pmul]
  | cons a p ih => simp only [pmul, peval_padd, peval_psmul, peval_cons, ih]; push_cast; ring

@[simp] lemma peval_pcomp (p q : Poly) (t : ℝ) : peval (pcomp p q) t = peval p (peval q t) := by
  induction p with
  | nil => simp [pcomp]
  | cons c p ih => simp only [pcomp, peval_padd, peval_pmul, peval_cons, peval_nil, ih]; ring

lemma qeval_cast (p : Poly) (m : ℚ) : ((qeval p m : ℚ) : ℝ) = peval p m := by
  induction p with
  | nil => simp [qeval]
  | cons c p ih => simp only [qeval, peval_cons]; push_cast; rw [ih]

lemma continuous_peval (p : Poly) : Continuous (peval p) := by
  induction p with
  | nil => exact continuous_const
  | cons c p ih => exact continuous_const.add (continuous_id.mul ih)

/-! ## Exact zero tests and division (untrusted) -/

def allZero (p : Poly) : Bool := p.all (· == 0)

lemma peval_eq_zero_of_allZero {p : Poly} (h : allZero p = true) (t : ℝ) : peval p t = 0 := by
  induction p with
  | nil => rfl
  | cons c p ih =>
    simp only [allZero, List.all_cons, Bool.and_eq_true, beq_iff_eq] at h
    simp [h.1, ih (by simpa [allZero] using h.2)]

/-- Subtract `k · g` from the front of `p` (descending coefficients). -/
def subFront (k : ℚ) : List ℚ → List ℚ → List ℚ
  | p, [] => p
  | [], _ => []
  | c :: p, d :: g => (c - k * d) :: subFront k p g

/-- Long division on descending coefficient lists: `fd` = divisor without its leading coefficient `lc`. -/
def divDesc (fd : List ℚ) (lc : ℚ) : ℕ → List ℚ → List ℚ → List ℚ × List ℚ
  | 0, q, p => (q, p)
  | fuel + 1, q, p =>
    if p.length ≤ fd.length then (q, p) else
    match p with
    | [] => (q, [])
    | c :: rest => divDesc fd lc fuel ((c / lc) :: q) (subFront (c / lc) rest fd)

/-- Quotient and remainder of `p` by `f` (ascending lists).  Not trusted: `nonnegOK` re-checks `p = q f + r`. -/
def pdivmod (p f : Poly) : Poly × Poly :=
  match f.reverse with
  | [] => ([], p)
  | lc :: fd =>
    let r := divDesc fd lc p.length [] p.reverse
    (r.1, r.2.reverse)

/-! ## Positivity on an interval -/

/-- `Σ |c_i| R^i`, a bound for `|p(t)|` on `|t| ≤ R`. -/
def bndA (R : ℚ) : Poly → ℚ
  | [] => 0
  | c :: p => |c| + R * bndA R p

/-- A Lipschitz bound for `p` on `|t| ≤ R`. -/
def bndB (R : ℚ) : Poly → ℚ
  | [] => 0
  | c :: p => bndA R p + R * bndB R p

lemma bndA_nonneg {R : ℚ} (hR : 0 ≤ R) (p : Poly) : 0 ≤ bndA R p := by
  induction p with
  | nil => simp [bndA]
  | cons c p ih => simp only [bndA]; positivity

lemma bndB_nonneg {R : ℚ} (hR : 0 ≤ R) (p : Poly) : 0 ≤ bndB R p := by
  induction p with
  | nil => simp [bndB]
  | cons c p ih => simp only [bndB]; have := bndA_nonneg hR p; positivity

lemma abs_peval_le {R : ℚ} (hR : 0 ≤ R) {t : ℝ} (ht : |t| ≤ R) (p : Poly) : |peval p t| ≤ bndA R p := by
  induction p with
  | nil => simp [bndA]
  | cons c p ih =>
    simp only [peval_cons, bndA]; push_cast
    calc |(c : ℝ) + t * peval p t| ≤ |(c : ℝ)| + |t| * |peval p t| := by
          rw [← abs_mul]; exact abs_add_le _ _
      _ ≤ |(c : ℝ)| + R * bndA R p := by
          gcongr

lemma abs_peval_sub_le {R : ℚ} (hR : 0 ≤ R) {t m : ℝ} (ht : |t| ≤ R) (hm : |m| ≤ R) (p : Poly) :
    |peval p t - peval p m| ≤ |t - m| * bndB R p := by
  induction p with
  | nil => simp [bndB]
  | cons c p ih =>
    simp only [peval_cons, bndB]; push_cast
    have e : (c : ℝ) + t * peval p t - (c + m * peval p m) =
        (t - m) * peval p t + m * (peval p t - peval p m) := by ring
    rw [e]
    have hA := abs_peval_le hR ht p
    have hB : (0 : ℝ) ≤ bndB R p := by exact_mod_cast bndB_nonneg hR p
    calc |(t - m) * peval p t + m * (peval p t - peval p m)|
        ≤ |t - m| * |peval p t| + |m| * |peval p t - peval p m| := by
          rw [← abs_mul, ← abs_mul]; exact abs_add_le _ _
      _ ≤ |t - m| * bndA R p + R * (|t - m| * bndB R p) := by
          gcongr
      _ = |t - m| * (bndA R p + R * bndB R p) := by ring

/-- `p > 0` on `[m - w, m + w]` (inside `|t| ≤ R`): `p(m) > w B`. -/
def posOK (p : Poly) (m w R : ℚ) : Bool := decide (w * bndB R p < qeval p m)

lemma pos_of_posOK {p : Poly} {m w R : ℚ} (h : posOK p m w R = true) (hR : 0 ≤ R) {t : ℝ}
    (htm : |t - m| ≤ w) (ht : |t| ≤ R) (hm : |(m : ℝ)| ≤ R) : 0 < peval p t := by
  simp only [posOK, decide_eq_true_eq] at h
  have h1 := abs_peval_sub_le hR ht hm p
  have hB : (0 : ℝ) ≤ bndB R p := by exact_mod_cast bndB_nonneg hR p
  have h2 : ((w * bndB R p : ℚ) : ℝ) < ((qeval p m : ℚ) : ℝ) := by exact_mod_cast h
  rw [qeval_cast] at h2; push_cast at h2
  have h3 : |t - m| * bndB R p ≤ w * bndB R p := by gcongr
  have := neg_abs_le (peval p t - peval p m)
  linarith

/-- The parameters of `posOK` for the interval `[a, b]`. -/
def mid (a b : ℚ) : ℚ := (a + b) / 2
def hw (a b : ℚ) : ℚ := (b - a) / 2
def rad (a b : ℚ) : ℚ := max |a| |b|

lemma interval_facts {a b : ℚ} {t : ℝ} (ha : (a : ℝ) ≤ t) (hb : t ≤ b) :
    |t - mid a b| ≤ hw a b ∧ |t| ≤ rad a b ∧ |((mid a b : ℚ) : ℝ)| ≤ rad a b ∧ 0 ≤ rad a b := by
  simp only [mid, hw, rad]; push_cast
  refine ⟨?_, ?_, ?_, ?_⟩
  · rw [abs_le]; constructor <;> linarith
  · rw [abs_le]
    constructor
    · have := neg_abs_le (a : ℝ); have := le_max_left |(a : ℝ)| |(b : ℝ)|; linarith
    · have := le_abs_self (b : ℝ); have := le_max_right |(a : ℝ)| |(b : ℝ)|; linarith
  · rw [abs_le]
    have := neg_abs_le (a : ℝ); have := le_max_left |(a : ℝ)| |(b : ℝ)|
    have := le_abs_self (b : ℝ); have := le_max_right |(a : ℝ)| |(b : ℝ)|
    have := neg_abs_le (b : ℝ); have := le_abs_self (a : ℝ)
    constructor <;> linarith
  · exact le_trans (abs_nonneg _) (le_max_left _ _)

/-- `N(t) ≥ 0` at every root `t ∈ [a, b]` of `f`: `N = q f + r` (checked), and `r = 0` or `r > 0` on `[a, b]`. -/
def nonnegOK (f : Poly) (a b : ℚ) (N : Poly) : Bool :=
  let qr := pdivmod N f
  allZero (psub N (padd (pmul qr.1 f) qr.2)) &&
    (allZero qr.2 || posOK qr.2 (mid a b) (hw a b) (rad a b))

lemma nonneg_of_nonnegOK {f N : Poly} {a b : ℚ} (h : nonnegOK f a b N = true) {t : ℝ} (hf : peval f t = 0)
    (ha : (a : ℝ) ≤ t) (hb : t ≤ b) : 0 ≤ peval N t := by
  simp only [nonnegOK, Bool.and_eq_true, Bool.or_eq_true] at h
  obtain ⟨hid, hr⟩ := h
  have e := peval_eq_zero_of_allZero hid t
  simp only [peval_psub, peval_padd, peval_pmul, hf, mul_zero, zero_add] at e
  have eN : peval N t = peval (pdivmod N f).2 t := by linarith
  rw [eN]
  rcases hr with hz | hp
  · rw [peval_eq_zero_of_allZero hz]
  · obtain ⟨h1, h2, h3, h4⟩ := interval_facts ha hb
    exact (pos_of_posOK hp h4 h1 h2 h3).le

/-- `N(t) = 0` at every root of `f`. -/
def zeroOK (f N : Poly) : Bool :=
  let qr := pdivmod N f
  allZero (psub N (padd (pmul qr.1 f) qr.2)) && allZero qr.2

lemma zero_of_zeroOK {f N : Poly} (h : zeroOK f N = true) {t : ℝ} (hf : peval f t = 0) : peval N t = 0 := by
  simp only [zeroOK, Bool.and_eq_true] at h
  have e := peval_eq_zero_of_allZero h.1 t
  simp only [peval_psub, peval_padd, peval_pmul, hf, mul_zero, zero_add,
    peval_eq_zero_of_allZero h.2 t] at e
  linarith

/-! ## Squares over the field -/

/-- A square: centre `(x, y)`, angle parameter `u = tan(θ'/2)`, and `m` extra quarter turns. -/
structure SqD where
  x : Poly
  y : Poly
  u : Poly
  m : ℕ
  /-- `R^m (1 - u², 2u)` and `1 + u²`, reduced mod `f` (checked by `sqOK`). -/
  c : Poly
  s : Poly
  d : Poly

/-- `1 + u²`. -/
def dd0 (q : SqD) : Poly := padd [1] (pmul q.u q.u)

def rotN : ℕ → Poly × Poly → Poly × Poly
  | 0, p => p
  | k + 1, p => ((psmul (-1) (rotN k p).2), (rotN k p).1)

/-- Numerators of `(cos, sin)`: `R^m (1 - u², 2u)`; the denominator is `dd0`. -/
def csN0 (q : SqD) : Poly × Poly := rotN q.m (psub [1] (pmul q.u q.u), psmul 2 q.u)

/-- The stored (reduced) numerators and denominator. -/
def csN (q : SqD) : Poly × Poly := (q.c, q.s)
def dd (q : SqD) : Poly := q.d

/-- The stored `c, s, d` agree with `csN0, dd0` mod `f`. -/
def sqOK (f : Poly) (q : SqD) : Bool :=
  zeroOK f (psub q.d (dd0 q)) && zeroOK f (psub q.c (csN0 q).1) && zeroOK f (psub q.s (csN0 q).2)

lemma sqOK_eval {f : Poly} {q : SqD} (h : sqOK f q = true) {t : ℝ} (hf : peval f t = 0) :
    peval (dd q) t = peval (dd0 q) t ∧ peval (csN q).1 t = peval (csN0 q).1 t ∧
      peval (csN q).2 t = peval (csN0 q).2 t := by
  simp only [sqOK, Bool.and_eq_true] at h
  obtain ⟨⟨h1, h2⟩, h3⟩ := h
  have e1 := zero_of_zeroOK h1 hf
  have e2 := zero_of_zeroOK h2 hf
  have e3 := zero_of_zeroOK h3 hf
  simp only [peval_psub] at e1 e2 e3
  simp only [dd, csN]
  exact ⟨by linarith, by linarith, by linarith⟩

lemma dd0_pos (q : SqD) (t : ℝ) : 0 < peval (dd0 q) t := by
  simp only [dd0, peval_padd, peval_pmul, peval_cons, peval_nil]; push_cast
  nlinarith [mul_self_nonneg (peval q.u t)]

lemma dd_pos {f : Poly} {q : SqD} (h : sqOK f q = true) {t : ℝ} (hf : peval f t = 0) :
    0 < peval (dd q) t := by
  rw [(sqOK_eval h hf).1]; exact dd0_pos q t

lemma rotN_sq (k : ℕ) (p : Poly × Poly) (t : ℝ) :
    peval (rotN k p).1 t ^ 2 + peval (rotN k p).2 t ^ 2 = peval p.1 t ^ 2 + peval p.2 t ^ 2 := by
  induction k with
  | zero => rfl
  | succ k ih => simp only [rotN, peval_psmul]; push_cast; linarith [ih]

lemma csN0_sq (q : SqD) (t : ℝ) :
    peval (csN0 q).1 t ^ 2 + peval (csN0 q).2 t ^ 2 = peval (dd0 q) t ^ 2 := by
  simp only [csN0, rotN_sq, dd0, peval_psub, peval_padd, peval_pmul, peval_psmul, peval_cons, peval_nil]
  push_cast; ring

lemma csN_sq {f : Poly} {q : SqD} (h : sqOK f q = true) {t : ℝ} (hf : peval f t = 0) :
    peval (csN q).1 t ^ 2 + peval (csN q).2 t ^ 2 = peval (dd q) t ^ 2 := by
  obtain ⟨e1, e2, e3⟩ := sqOK_eval h hf
  rw [e1, e2, e3]; exact csN0_sq q t

/-- The real data of a square at `t`. -/
noncomputable def xR (q : SqD) (t : ℝ) : ℝ := peval q.x t
noncomputable def yR (q : SqD) (t : ℝ) : ℝ := peval q.y t
noncomputable def cR (q : SqD) (t : ℝ) : ℝ := peval (csN q).1 t / peval (dd q) t
noncomputable def sR (q : SqD) (t : ℝ) : ℝ := peval (csN q).2 t / peval (dd q) t

lemma cR_sq_add {f : Poly} {q : SqD} (h : sqOK f q = true) {t : ℝ} (hf : peval f t = 0) :
    cR q t ^ 2 + sR q t ^ 2 = 1 := by
  have hd := (dd_pos h hf).ne'
  simp only [cR, sR, div_pow]
  rw [← add_div, csN_sq h hf, div_self (pow_ne_zero 2 hd)]

/-! ## Box and separation numerators -/

def lin2 (c d : Poly) (a b : ℚ) : Poly := psub (psmul a c) (psmul b d)   -- a c - b d
def lin2' (c d : Poly) (a b : ℚ) : Poly := padd (psmul a c) (psmul b d)  -- a c + b d

/-- The four box conditions of corner `(a, b)` times `1 + u²`: `x ≥ 0`, `S - x ≥ 0`, `y ≥ 0`, `S - y ≥ 0`. -/
def boxN (S : Poly) (q : SqD) (a b : ℚ) : List Poly :=
  let cs := csN q
  [padd (pmul (dd q) q.x) (lin2 cs.1 cs.2 a b),
   psub (pmul (dd q) (psub S q.x)) (lin2 cs.1 cs.2 a b),
   padd (pmul (dd q) q.y) (lin2' cs.2 cs.1 a b),
   psub (pmul (dd q) (psub S q.y)) (lin2' cs.2 cs.1 a b)]

/-- Side normal `k` from numerators `(c, s)`. -/
def nrmN (c s : Poly) : Fin 4 → Poly × Poly
  | 0 => (c, s)
  | 1 => (psmul (-1) s, c)
  | 2 => (psmul (-1) c, psmul (-1) s)
  | 3 => (s, psmul (-1) c)

/-- `SepSide` for corner `(a, b)` of `j` and side `k` of `i`, times `2 (1 + u_i²)(1 + u_j²)`. -/
def sepN (qi qj : SqD) (k : Fin 4) (a b : ℚ) : Poly :=
  let ci := csN qi
  let cj := csN qj
  let n := nrmN ci.1 ci.2 k
  psub (psmul 2 (padd (pmul n.1 (padd (pmul (dd qj) (psub qj.x qi.x)) (lin2 cj.1 cj.2 a b)))
                      (pmul n.2 (padd (pmul (dd qj) (psub qj.y qi.y)) (lin2' cj.2 cj.1 a b)))))
       (pmul (dd qi) (dd qj))

def halves : List ℚ := [1/2, -1/2]

lemma half_cases {a : ℝ} (h : Half a) : ∃ a' ∈ halves, (a' : ℝ) = a := by
  rcases h with rfl | rfl
  · exact ⟨1/2, by simp [halves], by norm_num⟩
  · exact ⟨-1/2, by simp [halves], by norm_num⟩

/-! ## The certificate and the checker -/

structure Cert (n : ℕ) where
  f : Poly
  a : ℚ
  b : ℚ
  S : Poly
  sq : Fin n → SqD
  /-- For `i < j`: `(true, k)` = side `k` of `i` separates; `(false, k)` = side `k` of `j`. -/
  sep : Fin n → Fin n → Bool × Fin 4
  /-- Rational enclosures of each square's data at the root. -/
  encl : Fin n → Shadow.Encl
  /-- A rational lower bound for the side. -/
  Sl : ℚ

/-- `encl i` encloses square `i`'s data: eight positivity conditions (`c = cN/d` with `d > 0`). -/
def enclOK {n : ℕ} (C : Cert n) (i : Fin n) : Bool :=
  let q := C.sq i
  let E := C.encl i
  [psub q.x [E.x.1], psub [E.x.2] q.x, psub q.y [E.y.1], psub [E.y.2] q.y,
   psub (csN q).1 (psmul E.c.1 (dd q)), psub (psmul E.c.2 (dd q)) (csN q).1,
   psub (csN q).2 (psmul E.s.1 (dd q)), psub (psmul E.s.2 (dd q)) (csN q).2].all (nonnegOK C.f C.a C.b)

/-- The exact wall conditions. -/
def boxOKx {n : ℕ} (C : Cert n) (i : Fin n) : Bool :=
  halves.all fun a => halves.all fun b => (boxN C.S (C.sq i) a b).all (nonnegOK C.f C.a C.b)

def boxOK {n : ℕ} (C : Cert n) (i : Fin n) : Bool :=
  sqOK C.f (C.sq i) && enclOK C i && (Shadow.inBoxOK (C.encl i) C.Sl || boxOKx C i)

/-- `S ≥ Sl`. -/
def SlOK {n : ℕ} (C : Cert n) : Bool := nonnegOK C.f C.a C.b (psub C.S [C.Sl])

/-- The exact pair conditions. -/
def pairOKx {n : ℕ} (C : Cert n) (i j : Fin n) : Bool :=
  halves.all fun a => halves.all fun b =>
    if (C.sep i j).1 then nonnegOK C.f C.a C.b (sepN (C.sq i) (C.sq j) (C.sep i j).2 a b)
    else nonnegOK C.f C.a C.b (sepN (C.sq j) (C.sq i) (C.sep i j).2 a b)

def pairOK {n : ℕ} (C : Cert n) (i j : Fin n) : Bool :=
  Shadow.pairOK (C.encl i) (C.encl j) || pairOKx C i j

/-- The pairs `(i, j)`, `j > i`: one row. -/
def rowOK {n : ℕ} (C : Cert n) (i : Fin n) : Bool :=
  (List.finRange n).all fun j => !decide (i < j) || pairOK C i j

def check {n : ℕ} (C : Cert n) : Bool :=
  SlOK C && (List.finRange n).all (boxOK C) && (List.finRange n).all (rowOK C)

/-! ## Soundness -/

section sound
variable {n : ℕ} (C : Cert n) {t : ℝ}

lemma inBox_of_boxOKx {i : Fin n} (hsq : sqOK C.f (C.sq i) = true) (h : boxOKx C i = true)
    (hf : peval C.f t = 0) (ha : (C.a : ℝ) ≤ t) (hb : t ≤ C.b) :
    InBox (peval C.S t) (xR (C.sq i) t) (yR (C.sq i) t) (cR (C.sq i) t) (sR (C.sq i) t) := by
  intro a b ha' hb'
  obtain ⟨a', ha'm, rfl⟩ := half_cases ha'
  obtain ⟨b', hb'm, rfl⟩ := half_cases hb'
  simp only [boxOKx, List.all_eq_true] at h
  have hl := h a' ha'm b' hb'm
  have hd := dd_pos hsq hf
  have g : ∀ N ∈ boxN C.S (C.sq i) a' b', 0 ≤ peval N t := fun N hN =>
    nonneg_of_nonnegOK (hl N hN) hf ha hb
  simp only [boxN, List.mem_cons, List.mem_nil_iff, or_false, forall_eq_or_imp, forall_eq] at g
  obtain ⟨g1, g2, g3, g4⟩ := g
  simp only [lin2, lin2', peval_padd, peval_psub, peval_pmul, peval_psmul] at g1 g2 g3 g4
  simp only [xR, yR, cR, sR]
  set d := peval (dd (C.sq i)) t
  set cn := peval (csN (C.sq i)).1 t
  set sn := peval (csN (C.sq i)).2 t
  have e1 : peval (C.sq i).x t + cn / d * a' - sn / d * b' = (d * peval (C.sq i).x t + (a' * cn - b' * sn)) / d := by
    field_simp; ring
  have e2 : peval (C.sq i).y t + sn / d * a' + cn / d * b' = (d * peval (C.sq i).y t + (a' * sn + b' * cn)) / d := by
    field_simp; ring
  rw [e1, e2]
  refine ⟨div_nonneg g1 hd.le, ?_, div_nonneg g3 hd.le, ?_⟩
  · rw [div_le_iff₀ hd]; linarith
  · rw [div_le_iff₀ hd]; linarith

lemma nrmN_eval (q : SqD) (k : Fin 4) :
    (peval (nrmN (csN q).1 (csN q).2 k).1 t / peval (dd q) t,
      peval (nrmN (csN q).1 (csN q).2 k).2 t / peval (dd q) t) = nrm (cR q t) (sR q t) k := by
  fin_cases k <;> simp [nrmN, nrm, cR, sR, neg_div]

lemma sepSide_of_sepN {qi qj : SqD} {k : Fin 4}
    (h : ∀ a ∈ halves, ∀ b ∈ halves, nonnegOK C.f C.a C.b (sepN qi qj k a b) = true)
    (hqi : sqOK C.f qi = true) (hqj : sqOK C.f qj = true)
    (hf : peval C.f t = 0) (ha : (C.a : ℝ) ≤ t) (hb : t ≤ C.b) :
    SepSide (xR qi t) (yR qi t) (cR qi t) (sR qi t) (xR qj t) (yR qj t) (cR qj t) (sR qj t) k := by
  intro a b ha' hb'
  obtain ⟨a', ha'm, rfl⟩ := half_cases ha'
  obtain ⟨b', hb'm, rfl⟩ := half_cases hb'
  have g := nonneg_of_nonnegOK (h a' ha'm b' hb'm) hf ha hb
  have hn := nrmN_eval (t := t) qi k
  rw [Prod.ext_iff] at hn
  rw [← hn.1, ← hn.2]
  simp only [sepN, lin2, lin2', peval_padd, peval_psub, peval_pmul, peval_psmul] at g
  have hdi := dd_pos hqi hf
  have hdj := dd_pos hqj hf
  simp only [xR, yR, cR, sR]
  set di := peval (dd qi) t
  set dj := peval (dd qj) t
  set nx := peval (nrmN (csN qi).1 (csN qi).2 k).1 t
  set ny := peval (nrmN (csN qi).1 (csN qi).2 k).2 t
  set cj := peval (csN qj).1 t
  set sj := peval (csN qj).2 t
  have e : nx / di * (peval qj.x t + cj / dj * a' - sj / dj * b' - peval qi.x t) +
      ny / di * (peval qj.y t + sj / dj * a' + cj / dj * b' - peval qi.y t) - 1 / 2 =
      ((2 : ℝ) * (nx * (dj * (peval qj.x t - peval qi.x t) + (a' * cj - b' * sj)) +
        ny * (dj * (peval qj.y t - peval qi.y t) + (a' * sj + b' * cj))) - di * dj) / (2 * di * dj) := by
    field_simp; ring
  have : 0 ≤ nx / di * (peval qj.x t + cj / dj * a' - sj / dj * b' - peval qi.x t) +
      ny / di * (peval qj.y t + sj / dj * a' + cj / dj * b' - peval qi.y t) - 1 / 2 := by
    rw [e]; push_cast at g; apply div_nonneg _ (by positivity); linarith
  linarith

lemma sqOK_of_boxOK {i : Fin n} (h : boxOK C i = true) : sqOK C.f (C.sq i) = true := by
  simp only [boxOK, Bool.and_eq_true] at h; exact h.1.1

lemma encl_mem {i : Fin n} (h : boxOK C i = true) (hf : peval C.f t = 0) (ha : (C.a : ℝ) ≤ t) (hb : t ≤ C.b) :
    (C.encl i).Mem (xR (C.sq i) t) (yR (C.sq i) t) (cR (C.sq i) t) (sR (C.sq i) t) := by
  have hsq := sqOK_of_boxOK C h
  simp only [boxOK, enclOK, Bool.and_eq_true, List.all_eq_true] at h
  have g : ∀ N ∈ [psub (C.sq i).x [(C.encl i).x.1], psub [(C.encl i).x.2] (C.sq i).x,
      psub (C.sq i).y [(C.encl i).y.1], psub [(C.encl i).y.2] (C.sq i).y,
      psub (csN (C.sq i)).1 (psmul (C.encl i).c.1 (dd (C.sq i))),
      psub (psmul (C.encl i).c.2 (dd (C.sq i))) (csN (C.sq i)).1,
      psub (csN (C.sq i)).2 (psmul (C.encl i).s.1 (dd (C.sq i))),
      psub (psmul (C.encl i).s.2 (dd (C.sq i))) (csN (C.sq i)).2], 0 ≤ peval N t :=
    fun N hN => nonneg_of_nonnegOK (h.1.2 N hN) hf ha hb
  simp only [List.mem_cons, List.mem_nil_iff, or_false, forall_eq_or_imp, forall_eq] at g
  obtain ⟨g1, g2, g3, g4, g5, g6, g7, g8⟩ := g
  simp only [peval_psub, peval_psmul, peval_cons, peval_nil] at g1 g2 g3 g4 g5 g6 g7 g8
  push_cast at g1 g2 g3 g4 g5 g6 g7 g8
  have hd := dd_pos hsq hf
  simp only [Shadow.Encl.Mem, Shadow.Iv.Mem, xR, yR, cR, sR]
  refine ⟨⟨by linarith, by linarith⟩, ⟨by linarith, by linarith⟩, ⟨?_, ?_⟩, ⟨?_, ?_⟩⟩
  · rw [le_div_iff₀ hd]; linarith
  · rw [div_le_iff₀ hd]; linarith
  · rw [le_div_iff₀ hd]; linarith
  · rw [div_le_iff₀ hd]; linarith

lemma Sl_le (hSl : SlOK C = true) (hf : peval C.f t = 0) (ha : (C.a : ℝ) ≤ t) (hb : t ≤ C.b) :
    (C.Sl : ℝ) ≤ peval C.S t := by
  have := nonneg_of_nonnegOK hSl hf ha hb
  simp only [peval_psub, peval_cons, peval_nil] at this; push_cast at this; linarith

lemma inBox_of_boxOK {i : Fin n} (h : boxOK C i = true) (hSl : SlOK C = true) (hf : peval C.f t = 0)
    (ha : (C.a : ℝ) ≤ t) (hb : t ≤ C.b) :
    InBox (peval C.S t) (xR (C.sq i) t) (yR (C.sq i) t) (cR (C.sq i) t) (sR (C.sq i) t) := by
  have hsq := sqOK_of_boxOK C h
  have hE := encl_mem C h hf ha hb
  simp only [boxOK, Bool.and_eq_true, Bool.or_eq_true] at h
  rcases h.2 with h2 | h2
  · exact Shadow.inBox_of_inBoxOK hE (Sl_le C hSl hf ha hb) h2
  · exact inBox_of_boxOKx C hsq h2 hf ha hb

lemma disjoint_of_pairOK {i j : Fin n} (hi : boxOK C i = true) (hj : boxOK C j = true) (h : pairOK C i j = true)
    (hf : peval C.f t = 0) (ha : (C.a : ℝ) ≤ t) (hb : t ≤ C.b) {θi θj : ℝ}
    (hci : Real.cos θi = cR (C.sq i) t) (hsi : Real.sin θi = sR (C.sq i) t)
    (hcj : Real.cos θj = cR (C.sq j) t) (hsj : Real.sin θj = sR (C.sq j) t) :
    Disjoint (interior (unitSq (xR (C.sq i) t, yR (C.sq i) t) θi))
      (interior (unitSq (xR (C.sq j) t, yR (C.sq j) t) θj)) := by
  have hqi := sqOK_of_boxOK C hi
  have hqj := sqOK_of_boxOK C hj
  have hui := cR_sq_add hqi hf
  have huj := cR_sq_add hqj hf
  simp only [pairOK, Bool.or_eq_true] at h
  rcases h with h | h
  · simp only [Shadow.pairOK, Bool.or_eq_true, List.any_eq_true, List.mem_finRange, true_and] at h
    have hEi := encl_mem C hi hf ha hb
    have hEj := encl_mem C hj hf ha hb
    rcases h with (h | ⟨k, hk⟩) | ⟨k, hk⟩
    · exact Shadow.disjoint_of_farOK hEi hEj h
    · exact disjoint_of_sepSide hci hsi hcj hsj hui huj (Shadow.sepSide_of_sepOK hEi hEj hk)
    · exact (disjoint_of_sepSide hcj hsj hci hsi huj hui (Shadow.sepSide_of_sepOK hEj hEi hk)).symm
  · simp only [pairOKx, List.all_eq_true] at h
    by_cases hs : (C.sep i j).1 = true
    · simp only [hs, if_true] at h
      exact disjoint_of_sepSide hci hsi hcj hsj hui huj (sepSide_of_sepN C h hqi hqj hf ha hb)
    · simp only [hs, if_false, Bool.false_eq_true] at h
      exact (disjoint_of_sepSide hcj hsj hci hsi huj hui (sepSide_of_sepN C h hqj hqi hf ha hb)).symm

lemma pairOK_of_rowOK {i j : Fin n} (hrow : rowOK C i = true) (hij : i < j) : pairOK C i j = true := by
  simp only [rowOK, List.all_eq_true, List.mem_finRange, true_implies] at hrow
  have hp := hrow j
  simpa [hij] using hp

theorem packs_of_parts (hSl : SlOK C = true) (hbox : ∀ i, boxOK C i = true) (hrow : ∀ i, rowOK C i = true)
    (hf : peval C.f t = 0) (ha : (C.a : ℝ) ≤ t) (hb : t ≤ C.b) : Packs n (peval C.S t) := by
  refine Shadow.packs_of_disjoint (fun i => xR (C.sq i) t) (fun i => yR (C.sq i) t) (fun i => cR (C.sq i) t)
    (fun i => sR (C.sq i) t) (fun i => cR_sq_add (sqOK_of_boxOK C (hbox i)) hf)
    (fun i => inBox_of_boxOK C (hbox i) hSl hf ha hb) ?_
  intro i j hij θi θj hci hsi hcj hsj
  exact disjoint_of_pairOK C (hbox i) (hbox j) (pairOK_of_rowOK C (hrow i) hij) hf ha hb hci hsi hcj hsj

theorem packs_of_check (h : check C = true) (hf : peval C.f t = 0) (ha : (C.a : ℝ) ≤ t) (hb : t ≤ C.b) :
    Packs n (peval C.S t) := by
  simp only [check, Bool.and_eq_true, List.all_eq_true, List.mem_finRange, true_implies] at h
  exact packs_of_parts C h.1.1 h.1.2 h.2 hf ha hb

end sound

/-- A real root of `f` in `[a, b]` from a sign change. -/
theorem exists_root {f : Poly} {a b : ℚ} (hab : a ≤ b) (h : qeval f a * qeval f b ≤ 0) :
    ∃ t : ℝ, (a : ℝ) ≤ t ∧ t ≤ b ∧ peval f t = 0 := by
  have hab' : (a : ℝ) ≤ b := by exact_mod_cast hab
  have hc := (continuous_peval f).continuousOn (s := Set.Icc (a : ℝ) b)
  have hfa := qeval_cast f a
  have hfb := qeval_cast f b
  have h' : peval f a * peval f b ≤ 0 := by rw [← hfa, ← hfb]; exact_mod_cast h
  have endpoint : peval f a * peval f b = 0 → ∃ t : ℝ, (a : ℝ) ≤ t ∧ t ≤ b ∧ peval f t = 0 := by
    intro h0
    rcases mul_eq_zero.1 h0 with h0 | h0
    · exact ⟨a, le_rfl, hab', h0⟩
    · exact ⟨b, hab', le_rfl, h0⟩
  rcases le_total (peval f a) 0 with ha | ha <;> rcases le_total (peval f b) 0 with hb | hb
  · exact endpoint (le_antisymm h' (mul_nonneg_of_nonpos_of_nonpos ha hb))
  · obtain ⟨t, ht, hft⟩ := intermediate_value_Icc hab' hc ⟨ha, hb⟩
    exact ⟨t, ht.1, ht.2, hft⟩
  · obtain ⟨t, ht, hft⟩ := intermediate_value_Icc' hab' hc ⟨hb, ha⟩
    exact ⟨t, ht.1, ht.2, hft⟩
  · exact endpoint (le_antisymm h' (mul_nonneg ha hb))

/-- **The packing theorem from a certificate.**  `pS` is the integer polynomial of `S`; `[Sa, Sb]` contains `S(t)`. -/
theorem packs_exact {n : ℕ} (C : Cert n) (pS : Poly) (Sa Sb : ℚ) (hab : C.a ≤ C.b)
    (hsign : qeval C.f C.a * qeval C.f C.b ≤ 0) (hSl : SlOK C = true) (hbox : ∀ i, boxOK C i = true) (hrow : ∀ i, rowOK C i = true)
    (hp : zeroOK C.f (pcomp pS C.S) = true)
    (hlo : nonnegOK C.f C.a C.b (psub C.S [Sa]) = true) (hhi : nonnegOK C.f C.a C.b (psub [Sb] C.S) = true) :
    ∃ s : ℝ, peval pS s = 0 ∧ (Sa : ℝ) ≤ s ∧ s ≤ Sb ∧ Packs n s := by
  obtain ⟨t, ha, hb, hf⟩ := exists_root hab hsign
  refine ⟨peval C.S t, ?_, ?_, ?_, packs_of_parts C hSl hbox hrow hf ha hb⟩
  · have := zero_of_zeroOK hp hf; rwa [peval_pcomp] at this
  · have := nonneg_of_nonnegOK hlo hf ha hb; simp at this; linarith
  · have := nonneg_of_nonnegOK hhi hf ha hb; simp at this; linarith

end UnitSquarePacking.EC
