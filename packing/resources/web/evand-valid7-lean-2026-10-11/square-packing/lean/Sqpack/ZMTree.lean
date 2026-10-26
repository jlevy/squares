import Sqpack.BoxTree

/-!
# Zero-margin leaves for the box-tree verifier (rung 2 of the Lean ladder)

`BoxTree.lean` certifies a pose box only by a *monotone witness set*: points that lie in every
admissible square of the box.  At a container side where the bound is sharp (`s(13) = 4`, the
4×4 tiling) that is provably not enough (`search/RUNG2.md` §2: any such tree needs total weight
`≥ m²`).  This file adds the leaf types of `search/zeromargin.py` that close the gap — the exact
`ADM` test with the container walls as polynomial bounds, `clip_bin`, `EMPTY`, and the
disjunctive `CHAIN` (one monotone chain of pivot inequalities, or the product of two) — as a
sibling tree type `ZT` with its own kernel check `check` and soundness theorem `sound`, stated
for the same `BoxTree.Cov`, so that `BoxTree.le_minSide` turns a covered root box into `s(n) ≥ m`.

## The computation (natural numbers only)

Box coordinates are over `Q = D·S`, the angle parameter `u = tan(θ/2) = v/R`.  Signed quantities
are pairs `(p, n)` of naturals (`SP`, value `p − n`), so every test is `Nat.ble` of two sums of
products, as in `BoxTree`.

* **`qOk`** — the exact maximum of a quadratic `a₀ + a₁v + a₂v²` on `[U₀,U₁]` is `≤ 0`
  (`maxQuad` of `ZeroMargin.lean`: both endpoints, and the vertex when `a₂ < 0` and it lies
  inside), `_quad_le0` in the Python.
* **`bOk`** — the degree-4 Bernstein bound (`maxBern`, `_bern_le0_i`).
* **`gq`** — `R²Q·G_k(v/R)` for the violation polynomial `G_k` of `ZeroMargin.lean` at a centre
  corner.
* **`admK`** — Lemma A: condition `k` of a point at every admissible pose of the box, at the
  condition's own corner, with the lower centre bound either the box side or the wall `w(θ)/2`
  (`cpoly`, Lemma B, degree 4).  `_adm_cond_ok_int`.
* **`pairOk`** — Lemma E: `λ_a G_p + λ_b G_q ≤ 0` on the whole box (four corners, exact
  quadratic maximum); `λ = (1,−1)` is the chain comparison (Lemma F), `(1,1)`, `(2,1)`, `(1,2)` the
  opposite side (Lemma G) and the empty product regions (Lemma H).  `_gle0`.
* **Leaf `Z`** — claimed entries, each with a tag: `4` (all four conditions by `admK`: the `ADM`
  witness set `T`) or a *swing kind* `k` (three conditions by `admK`, condition `k` by a *down*
  reason `G_p ≤ G_{q_d}` and/or an *up* reason `λ_a G_p + λ_b G_{q_u} ≤ 0` against pivots of chain
  A or B).  At a pose, the monotone chains cut the box into regions `(r, s)` (Lemma F); an entry
  counts in a region when its reason applies there; every region not certified empty must reach
  weight `W`.
* **`E`** (no admissible pose: `w(θ)/2 > c₁` at both ends of the bin, `w` being quasi-concave),
  **`C us`** (`clip_bin`: poses with `u > us` are inadmissible since `w` increases there).

Nothing about the tree is trusted: `sound` holds for every tree.
-/

namespace SquarePacking

namespace ZMTree

open BoxTree

/-! ## Signed integers as pairs of naturals -/

/-- A signed integer `p − n`, as the pair `(p, n)`. -/
abbrev SP := ℕ × ℕ

def sadd (a b : SP) : SP := (Nat.add a.1 b.1, Nat.add a.2 b.2)
def ssub (a b : SP) : SP := (Nat.add a.1 b.2, Nat.add a.2 b.1)
def sneg (a : SP) : SP := (a.2, a.1)
def smul (a b : SP) : SP :=
  (Nat.add (Nat.mul a.1 b.1) (Nat.mul a.2 b.2), Nat.add (Nat.mul a.1 b.2) (Nat.mul a.2 b.1))
def sk (k : ℕ) (a : SP) : SP := (Nat.mul k a.1, Nat.mul k a.2)
def sle0 (a : SP) : Bool := Nat.ble a.1 a.2
def slt0 (a : SP) : Bool := Nat.blt a.1 a.2
def spos (a : SP) : Bool := Nat.blt a.2 a.1

/-- The value of a signed pair. -/
noncomputable def sv (a : SP) : ℝ := (a.1 : ℝ) - a.2

@[simp] lemma sv_sadd (a b : SP) : sv (sadd a b) = sv a + sv b := by
  simp only [sv, sadd, nat_add_eq, Nat.cast_add]; ring
@[simp] lemma sv_ssub (a b : SP) : sv (ssub a b) = sv a - sv b := by
  simp only [sv, ssub, nat_add_eq, Nat.cast_add]; ring
@[simp] lemma sv_sneg (a : SP) : sv (sneg a) = -sv a := by
  simp only [sv, sneg]; ring
@[simp] lemma sv_smul (a b : SP) : sv (smul a b) = sv a * sv b := by
  simp only [sv, smul, nat_add_eq, nat_mul_eq, Nat.cast_add, Nat.cast_mul]; ring
@[simp] lemma sv_sk (k : ℕ) (a : SP) : sv (sk k a) = k * sv a := by
  simp only [sv, sk, nat_mul_eq, Nat.cast_mul]; ring
@[simp] lemma sv_mk (p n : ℕ) : sv (p, n) = (p : ℝ) - n := rfl

lemma sle0_iff (a : SP) : sle0 a = true ↔ sv a ≤ 0 := by
  simp only [sle0, Nat.ble_eq, sv, sub_nonpos, Nat.cast_le]
lemma slt0_iff (a : SP) : slt0 a = true ↔ sv a < 0 := by
  simp only [slt0, Nat.blt_eq, sv, sub_neg, Nat.cast_lt]
lemma spos_iff (a : SP) : spos a = true ↔ 0 < sv a := by
  simp only [spos, Nat.blt_eq, sv, sub_pos, Nat.cast_lt]

/-! ## Exact quadratic maximum and the degree-4 Bernstein bound -/

/-- `a₀ + a₁ v + a₂ v²` at a natural `v`. -/
def qev (a0 a1 a2 : SP) (v : ℕ) : SP := sadd a0 (sadd (sk v a1) (sk (Nat.mul v v) a2))

@[simp] lemma sv_qev (a0 a1 a2 : SP) (v : ℕ) :
    sv (qev a0 a1 a2 v) = sv a0 + sv a1 * v + sv a2 * (v : ℝ) ^ 2 := by
  simp only [qev, sv_sadd, sv_sk, nat_mul_eq, Nat.cast_mul]; ring

/-- **The exact maximum of a quadratic on `[U₀,U₁]` is `≤ 0`** (`_quad_le0`): both endpoint values,
and, when `a₂ < 0` and the vertex `−a₁/(2a₂)` is strictly inside, the vertex value
(`4a₀a₂ − a₁² ≥ 0`). -/
def qOk (a0 a1 a2 : SP) (U0 U1 : ℕ) : Bool :=
  sle0 (qev a0 a1 a2 U0) && sle0 (qev a0 a1 a2 U1) &&
    (!(slt0 a2 && spos (sadd a1 (sk (Nat.mul 2 U0) a2)) &&
        slt0 (sadd a1 (sk (Nat.mul 2 U1) a2)))
      || sle0 (ssub (smul a1 a1) (sk 4 (smul a0 a2))))

theorem qOk_sound {a0 a1 a2 : SP} {U0 U1 : ℕ} (h : qOk a0 a1 a2 U0 U1 = true) {v : ℝ}
    (h0 : (U0 : ℝ) ≤ v) (h1 : v ≤ U1) : sv a0 + sv a1 * v + sv a2 * v ^ 2 ≤ 0 := by
  simp only [qOk, Bool.and_eq_true, Bool.or_eq_true, Bool.not_eq_true'] at h
  obtain ⟨⟨he0, he1⟩, hv⟩ := h
  rw [sle0_iff, sv_qev] at he0 he1
  refine le_trans (le_maxQuad ⟨h0, h1⟩) ?_
  unfold maxQuad
  split_ifs with hc
  · obtain ⟨ha, hlo, hhi⟩ := hc
    have h2a : 2 * sv a2 < 0 := by linarith
    have c1 : 0 < sv a1 + 2 * U0 * sv a2 := by
      rw [lt_div_iff_of_neg h2a] at hlo; linarith
    have c2 : sv a1 + 2 * U1 * sv a2 < 0 := by
      rw [div_lt_iff_of_neg h2a] at hhi; linarith
    have hb : (slt0 a2 && spos (sadd a1 (sk (Nat.mul 2 U0) a2)) &&
        slt0 (sadd a1 (sk (Nat.mul 2 U1) a2))) = true := by
      simp only [Bool.and_eq_true, slt0_iff, spos_iff, sv_sadd, sv_sk, nat_mul_eq,
        Nat.cast_mul, Nat.cast_ofNat]
      refine ⟨⟨ha, by linarith⟩, by linarith⟩
    rcases hv with hv | hv
    · rw [hb] at hv; exact absurd hv (by simp)
    · rw [sle0_iff] at hv
      simp only [sv_ssub, sv_smul, sv_sk, Nat.cast_ofNat] at hv
      refine max_le (max_le he0 he1) ?_
      have h4 : 4 * sv a2 < 0 := by linarith
      have hne : sv a2 ≠ 0 := ne_of_lt ha
      have : sv a0 - sv a1 ^ 2 / (4 * sv a2) = (4 * sv a0 * sv a2 - sv a1 ^ 2) / (4 * sv a2) := by
        field_simp
      rw [this]
      exact div_nonpos_of_nonneg_of_nonpos (by nlinarith) h4.le
  · exact max_le he0 he1

/-- The quadratic `c₀ + c₁v + c₂v²` is `≤ 0` on `[U₀,U₁]`. -/
def QNP (c0 c1 c2 : SP) (U0 U1 : ℕ) : Prop :=
  ∀ v : ℝ, (U0 : ℝ) ≤ v → v ≤ U1 → sv c0 + sv c1 * v + sv c2 * v ^ 2 ≤ 0

/-- **Degree-2 Bernstein bound**: a quadratic is `≤ 0` on `[u₀,u₁]` if its values at the ends and
its polar value `c₀ + c₁(u₀+u₁)/2 + c₂u₀u₁` are. -/
lemma bern2 {c0 c1 c2 u0 u1 v : ℝ} (h0 : u0 ≤ v) (h1 : v ≤ u1)
    (e0 : c0 + c1 * u0 + c2 * u0 ^ 2 ≤ 0) (e1 : c0 + c1 * u1 + c2 * u1 ^ 2 ≤ 0)
    (ep : c0 + c1 * ((u0 + u1) / 2) + c2 * (u0 * u1) ≤ 0) : c0 + c1 * v + c2 * v ^ 2 ≤ 0 := by
  have key : (u1 - u0) ^ 2 * (c0 + c1 * v + c2 * v ^ 2)
      = (u1 - v) ^ 2 * (c0 + c1 * u0 + c2 * u0 ^ 2)
        + 2 * ((v - u0) * (u1 - v)) * (c0 + c1 * ((u0 + u1) / 2) + c2 * (u0 * u1))
        + (v - u0) ^ 2 * (c0 + c1 * u1 + c2 * u1 ^ 2) := by ring
  rcases eq_or_lt_of_le (le_trans h0 h1) with h | h
  · have hv : v = u0 := by linarith
    subst hv; exact e0
  · have hpos : 0 < (u1 - u0) ^ 2 := pow_pos (by linarith) 2
    have t1 := mul_nonpos_of_nonneg_of_nonpos (sq_nonneg (u1 - v)) e0
    have t2 := mul_nonpos_of_nonneg_of_nonpos
      (mul_nonneg (by norm_num : (0:ℝ) ≤ 2)
        (mul_nonneg (by linarith : 0 ≤ v - u0) (by linarith : 0 ≤ u1 - v))) ep
    have t3 := mul_nonpos_of_nonneg_of_nonpos (sq_nonneg (v - u0)) e1
    have hle : (u1 - u0) ^ 2 * (c0 + c1 * v + c2 * v ^ 2) ≤ 0 := by rw [key]; linarith
    by_contra hc
    exact absurd hle (not_le.mpr (mul_pos hpos (not_le.mp hc)))

theorem qOk_qnp {a0 a1 a2 : SP} {U0 U1 : ℕ} (h : qOk a0 a1 a2 U0 U1 = true) : QNP a0 a1 a2 U0 U1 :=
  fun _ h0 h1 => qOk_sound h h0 h1

/-- The five scaled Bernstein tests of a quartic `Σ pⱼ vʲ` on `[U₀,U₁]` (`_bern_le0_i`, with the
coefficients `12β₀, 3·4β₁, 2·6β₂, 3·4β₃, 12β₄` divided by their positive common factors). -/
def bOk (p0 p1 p2 p3 p4 : SP) (U0 U1 : ℕ) : Bool :=
  let H := Nat.sub U1 U0
  let b0 := sadd p0 (sk U0 (sadd p1 (sk U0 (sadd p2 (sk U0 (sadd p3 (sk U0 p4)))))))
  let b1 := sk H (sadd p1 (sk U0 (sadd (sk 2 p2) (sk U0 (sadd (sk 3 p3) (sk (Nat.mul U0 4) p4))))))
  let b2 := sk (Nat.mul H H) (sadd p2 (sk U0 (sadd (sk 3 p3) (sk (Nat.mul U0 6) p4))))
  let b3 := sk (Nat.mul (Nat.mul H H) H) (sadd p3 (sk (Nat.mul U0 4) p4))
  let b4 := sk (Nat.mul (Nat.mul H H) (Nat.mul H H)) p4
  sle0 b0 && sle0 (sadd (sk 4 b0) b1) && sle0 (sadd (sadd (sk 6 b0) (sk 3 b1)) b2) &&
    sle0 (sadd (sadd (sadd (sk 4 b0) (sk 3 b1)) (sk 2 b2)) b3) &&
    sle0 (sadd (sadd (sadd (sadd b0 b1) b2) b3) b4)

theorem bOk_sound {p0 p1 p2 p3 p4 : SP} {U0 U1 : ℕ} (h : bOk p0 p1 p2 p3 p4 U0 U1 = true)
    (hU : U0 ≤ U1) {v : ℝ} (h0 : (U0 : ℝ) ≤ v) (h1 : v ≤ U1) :
    sv p0 + sv p1 * v + sv p2 * v ^ 2 + sv p3 * v ^ 3 + sv p4 * v ^ 4 ≤ 0 := by
  have hH : ((Nat.sub U1 U0 : ℕ) : ℝ) = (U1 : ℝ) - U0 := by
    rw [nat_sub_eq, Nat.cast_sub hU]
  simp only [bOk, Bool.and_eq_true, sle0_iff, sv_sadd, sv_sk, nat_mul_eq, Nat.cast_mul,
    Nat.cast_ofNat, hH] at h
  obtain ⟨⟨⟨⟨c0, c1⟩, c2⟩, c3⟩, c4⟩ := h
  have key := qeval4_le_maxBern (sv p0, sv p1, sv p2, sv p3, sv p4) (u₀ := (U0 : ℝ))
    (u₁ := (U1 : ℝ)) ⟨h0, h1⟩
  simp only [qeval4] at key
  refine le_trans key ?_
  simp only [maxBern, bernCoef, bshift]
  refine max_le (max_le (max_le (max_le ?_ ?_) ?_) ?_) ?_ <;> nlinarith [c0, c1, c2, c3, c4]

/-! ## Violation polynomials at a corner -/

/-- The kind of a violation polynomial (`k ≥ 3` is kind `3`). -/
def kf (k : ℕ) : Fin 4 :=
  match k with
  | 0 => 0
  | 1 => 1
  | 2 => 2
  | _ => 3

lemma kf_val (k : Fin 4) : kf k.val = k := by fin_cases k <;> rfl

/-- `R²Q·G_k(v/R)` at the offsets `(A/Q, B/Q)`, as the coefficient triple of a quadratic in `v`. -/
def gq (Q R : ℕ) (k : ℕ) (A B : SP) : SP × SP × SP :=
  match k with
  | 0 => (sk (Nat.mul R R) (ssub (sk 2 A) (Q, 0)), sk (Nat.mul 4 R) B, sneg (sadd (sk 2 A) (Q, 0)))
  | 1 => (sk (Nat.mul R R) (sneg (sadd (sk 2 A) (Q, 0))), sneg (sk (Nat.mul 4 R) B),
          ssub (sk 2 A) (Q, 0))
  | 2 => (sk (Nat.mul R R) (ssub (sk 2 B) (Q, 0)), sneg (sk (Nat.mul 4 R) A),
          sneg (sadd (sk 2 B) (Q, 0)))
  | _ => (sk (Nat.mul R R) (sneg (sadd (sk 2 B) (Q, 0))), sk (Nat.mul 4 R) A,
          ssub (sk 2 B) (Q, 0))

lemma gq_eval (Q R k : ℕ) (A B : SP) (hQ : 0 < Q) (hR : 0 < R) (v : ℝ) :
    sv (gq Q R k A B).1 + sv (gq Q R k A B).2.1 * v + sv (gq Q R k A B).2.2 * v ^ 2
      = (Q : ℝ) * R ^ 2 * gval (kf k) (sv A / Q) (sv B / Q) (v / R) := by
  have hQr : (Q : ℝ) ≠ 0 := by exact_mod_cast hQ.ne'
  have hRr : (R : ℝ) ≠ 0 := by exact_mod_cast hR.ne'
  rcases k with _ | _ | _ | k <;>
    simp only [gq, kf, gval, gc, sv_sadd, sv_ssub, sv_sneg, sv_sk, sv_mk, nat_mul_eq,
      Nat.cast_mul, Nat.cast_ofNat, Nat.cast_zero, sub_zero] <;>
    field_simp <;> ring

/-! ### Fast paths (degree-2 Bernstein with per-box triples)

At `v`, `R²Q·G_k` at a corner is linear in the point: `α A + β B − γ` for kind `0` (with the signs
of `gc` for the others), `(α, β, γ) = (2(R² − v²), 4Rv, Q(R² + v²))` (`triV`); its polar value on
`[U₀,U₁]` has `(2(R² − U₀U₁), 2R(U₀+U₁), Q(R² + U₀U₁))` (`triP`).  The triples depend only on the
box, so a point costs a few products — `BoxTree.triOk`'s form.  These tests are tried first; the
exact tests (`qOk`) are the fallback, and since the fast tests imply them, the verdict of every
`fast || exact` is the exact one. -/

def triV (Q R v : ℕ) : ℕ × ℕ × ℕ :=
  (Nat.mul 2 (Nat.sub (Nat.mul R R) (Nat.mul v v)), Nat.mul 4 (Nat.mul R v),
    Nat.mul Q (Nat.add (Nat.mul R R) (Nat.mul v v)))

def triP (Q R U0 U1 : ℕ) : ℕ × ℕ × ℕ :=
  (Nat.mul 2 (Nat.sub (Nat.mul R R) (Nat.mul U0 U1)), Nat.mul 2 (Nat.mul R (Nat.add U0 U1)),
    Nat.mul Q (Nat.add (Nat.mul R R) (Nat.mul U0 U1)))

/-- `G_k` at the corner `(cx, cy)` with the triple `t`, as a signed pair. -/
def lin (k : ℕ) (t : ℕ × ℕ × ℕ) (XS YS cx cy : ℕ) : SP :=
  match k with
  | 0 => (Nat.add (Nat.mul t.1 XS) (Nat.mul t.2.1 YS),
          Nat.add (Nat.add t.2.2 (Nat.mul t.1 cx)) (Nat.mul t.2.1 cy))
  | 1 => (Nat.add (Nat.mul t.1 cx) (Nat.mul t.2.1 cy),
          Nat.add (Nat.add t.2.2 (Nat.mul t.1 XS)) (Nat.mul t.2.1 YS))
  | 2 => (Nat.add (Nat.mul t.1 YS) (Nat.mul t.2.1 cx),
          Nat.add (Nat.add t.2.2 (Nat.mul t.2.1 XS)) (Nat.mul t.1 cy))
  | _ => (Nat.add (Nat.mul t.2.1 XS) (Nat.mul t.1 cy),
          Nat.add (Nat.add t.2.2 (Nat.mul t.1 YS)) (Nat.mul t.2.1 cx))

lemma lin_triV {Q R v : ℕ} (hv : v ≤ R) (k XS YS cx cy : ℕ) :
    sv (lin k (triV Q R v) XS YS cx cy)
      = sv (gq Q R k (XS, cx) (YS, cy)).1 + sv (gq Q R k (XS, cx) (YS, cy)).2.1 * v
        + sv (gq Q R k (XS, cx) (YS, cy)).2.2 * (v : ℝ) ^ 2 := by
  have h : v * v ≤ R * R := Nat.mul_le_mul hv hv
  rcases k with _ | _ | _ | k <;>
    simp only [lin, triV, gq, sv_sadd, sv_ssub, sv_sneg, sv_sk, sv_mk, nat_mul_eq, nat_add_eq,
      nat_sub_eq, Nat.cast_mul, Nat.cast_add, Nat.cast_sub h, Nat.cast_ofNat, Nat.cast_zero,
      sub_zero] <;> ring

lemma lin_triP {Q R U0 U1 : ℕ} (h : U0 * U1 ≤ R * R) (k XS YS cx cy : ℕ) :
    sv (lin k (triP Q R U0 U1) XS YS cx cy)
      = sv (gq Q R k (XS, cx) (YS, cy)).1
        + sv (gq Q R k (XS, cx) (YS, cy)).2.1 * (((U0 : ℝ) + U1) / 2)
        + sv (gq Q R k (XS, cx) (YS, cy)).2.2 * ((U0 : ℝ) * U1) := by
  rcases k with _ | _ | _ | k <;>
    simp only [lin, triP, gq, sv_sadd, sv_ssub, sv_sneg, sv_sk, sv_mk, nat_mul_eq, nat_add_eq,
      nat_sub_eq, Nat.cast_mul, Nat.cast_add, Nat.cast_sub h, Nat.cast_ofNat, Nat.cast_zero,
      sub_zero] <;> ring

/-- The fast test of one violation polynomial at a corner. -/
def rrFast (Q R U0 U1 k XS YS cx cy : ℕ) : Bool :=
  sle0 (lin k (triV Q R U0) XS YS cx cy) && sle0 (lin k (triV Q R U1) XS YS cx cy) &&
    sle0 (lin k (triP Q R U0 U1) XS YS cx cy)

lemma rrFast_qnp {Q R U0 U1 k XS YS cx cy : ℕ} (hU01 : U0 ≤ U1) (hU1 : U1 ≤ R)
    (h : rrFast Q R U0 U1 k XS YS cx cy = true) :
    QNP (gq Q R k (XS, cx) (YS, cy)).1 (gq Q R k (XS, cx) (YS, cy)).2.1
      (gq Q R k (XS, cx) (YS, cy)).2.2 U0 U1 := by
  intro v h0 h1
  simp only [rrFast, Bool.and_eq_true, sle0_iff] at h
  obtain ⟨⟨e0, e1⟩, ep⟩ := h
  rw [lin_triV (le_trans hU01 hU1)] at e0
  rw [lin_triV hU1] at e1
  rw [lin_triP (Nat.mul_le_mul (le_trans hU01 hU1) hU1)] at ep
  exact bern2 h0 h1 e0 e1 ep

/-- A quadratic triple is `≤ 0` on the bin. -/
def qOk3 (g : SP × SP × SP) (U0 U1 : ℕ) : Bool := qOk g.1 g.2.1 g.2.2 U0 U1

/-- The combination `λ_a·a + λ_b·b`, `(λ_a, λ_b) = (1,−1), (1,1), (2,1), (1,2)` for `l = 0..3`. -/
def comb (l : ℕ) (a b : SP) : SP :=
  match l with
  | 0 => ssub a b
  | 1 => sadd a b
  | 2 => sadd (sk 2 a) b
  | _ => sadd a (sk 2 b)

def combQ (l : ℕ) (g h : SP × SP × SP) : SP × SP × SP :=
  (comb l g.1 h.1, comb l g.2.1 h.2.1, comb l g.2.2 h.2.2)

/-- The multipliers of `comb`. -/
def lamA (l : ℕ) : ℝ := if l = 2 then 2 else 1
def lamB (l : ℕ) : ℝ := if l = 0 then -1 else if 3 ≤ l then 2 else 1

lemma sv_comb (l : ℕ) (a b : SP) : sv (comb l a b) = lamA l * sv a + lamB l * sv b := by
  rcases l with _ | _ | _ | l
  · simp [comb, lamA, lamB]; ring
  · simp [comb, lamA, lamB]
  · simp [comb, lamA, lamB]
  · have h3 : 3 ≤ l + 1 + 1 + 1 := by omega
    have h2 : l + 1 + 1 + 1 ≠ 2 := by omega
    simp [comb, lamA, lamB, h3, h2]

@[simp] lemma lamA_zero : lamA 0 = 1 := by norm_num [lamA]
@[simp] lemma lamB_zero : lamB 0 = -1 := by norm_num [lamB]

lemma lamA_pos (l : ℕ) : 0 < lamA l := by unfold lamA; split_ifs <;> norm_num
lemma lamB_pos {l : ℕ} (h : 0 < l) : 0 < lamB l := by
  unfold lamB; split_ifs <;> first | omega | norm_num

/-- The fast test of a combination at a corner. -/
def cornFast (Q R U0 U1 l kp XSp YSp kq XSq YSq cx cy : ℕ) : Bool :=
  sle0 (comb l (lin kp (triV Q R U0) XSp YSp cx cy) (lin kq (triV Q R U0) XSq YSq cx cy)) &&
  sle0 (comb l (lin kp (triV Q R U1) XSp YSp cx cy) (lin kq (triV Q R U1) XSq YSq cx cy)) &&
  sle0 (comb l (lin kp (triP Q R U0 U1) XSp YSp cx cy) (lin kq (triP Q R U0 U1) XSq YSq cx cy))

/-- **Lemma E on one corner**: `λ_a G_p + λ_b G_q ≤ 0` at the centre `(cx, cy)/Q` for the whole
bin. -/
def cornOk (Q R U0 U1 l kp XSp YSp kq XSq YSq cx cy : ℕ) : Bool :=
  cornFast Q R U0 U1 l kp XSp YSp kq XSq YSq cx cy ||
    qOk3 (combQ l (gq Q R kp (XSp, cx) (YSp, cy)) (gq Q R kq (XSq, cx) (YSq, cy))) U0 U1

lemma cornOk_qnp {Q R U0 U1 l kp XSp YSp kq XSq YSq cx cy : ℕ} (hU01 : U0 ≤ U1) (hU1 : U1 ≤ R)
    (h : cornOk Q R U0 U1 l kp XSp YSp kq XSq YSq cx cy = true) :
    QNP (combQ l (gq Q R kp (XSp, cx) (YSp, cy)) (gq Q R kq (XSq, cx) (YSq, cy))).1
      (combQ l (gq Q R kp (XSp, cx) (YSp, cy)) (gq Q R kq (XSq, cx) (YSq, cy))).2.1
      (combQ l (gq Q R kp (XSp, cx) (YSp, cy)) (gq Q R kq (XSq, cx) (YSq, cy))).2.2 U0 U1 := by
  simp only [cornOk, Bool.or_eq_true] at h
  rcases h with h | h
  · intro v h0 h1
    simp only [cornFast, Bool.and_eq_true, sle0_iff, sv_comb] at h
    obtain ⟨⟨e0, e1⟩, ep⟩ := h
    rw [lin_triV (le_trans hU01 hU1), lin_triV (le_trans hU01 hU1)] at e0
    rw [lin_triV hU1, lin_triV hU1] at e1
    rw [lin_triP (Nat.mul_le_mul (le_trans hU01 hU1) hU1),
      lin_triP (Nat.mul_le_mul (le_trans hU01 hU1) hU1)] at ep
    simp only [combQ, sv_comb]
    set g := gq Q R kp (XSp, cx) (YSp, cy)
    set g' := gq Q R kq (XSq, cx) (YSq, cy)
    apply bern2 h0 h1
    · convert e0 using 1; ring
    · convert e1 using 1; ring
    · convert ep using 1; ring
  · exact qOk_qnp h

/-- The combination does not depend on the centre: `G_p − G_q` for equal kinds, `G_p + G_q` for
opposite kinds (`0/1`, `2/3`).  Then one corner decides `pairOk`. -/
def cfree (l kp kq : ℕ) : Bool :=
  (Nat.beq l 0 && Nat.beq kp kq) ||
    (Nat.beq l 1 && ((Nat.beq kp 0 && Nat.beq kq 1) || (Nat.beq kp 1 && Nat.beq kq 0) ||
      (Nat.beq kp 2 && Nat.beq kq 3) || (Nat.beq kp 3 && Nat.beq kq 2)))

/-- **Lemma E** (`_gle0`): `λ_a G_p + λ_b G_q ≤ 0` on the whole pose box. -/
def pairOk (Q R x0 x1 y0 y1 U0 U1 l kp XSp YSp kq XSq YSq : ℕ) : Bool :=
  (cfree l kp kq && cornOk Q R U0 U1 l kp XSp YSp kq XSq YSq x0 y0) ||
  cornOk Q R U0 U1 l kp XSp YSp kq XSq YSq x0 y0 &&
    cornOk Q R U0 U1 l kp XSp YSp kq XSq YSq x0 y1 &&
    cornOk Q R U0 U1 l kp XSp YSp kq XSq YSq x1 y0 &&
    cornOk Q R U0 U1 l kp XSp YSp kq XSq YSq x1 y1

/-- The violation polynomial of kind `k` of the point `(XS, YS)/Q` at the pose `(c, u)`. -/
noncomputable def Gv (Q k XS YS : ℕ) (c : ℝ × ℝ) (u : ℝ) : ℝ :=
  gval (kf k) ((XS : ℝ) / Q - c.1) ((YS : ℝ) / Q - c.2) u

lemma cornOk_sound {Q R U0 U1 l kp XSp YSp kq XSq YSq cx cy : ℕ} (hQ : 0 < Q) (hR : 0 < R)
    (hU01 : U0 ≤ U1) (hU1 : U1 ≤ R)
    (h : cornOk Q R U0 U1 l kp XSp YSp kq XSq YSq cx cy = true) {u : ℝ}
    (hu0 : (U0 : ℝ) / R ≤ u) (hu1 : u ≤ (U1 : ℝ) / R) :
    lamA l * Gv Q kp XSp YSp ((cx : ℝ) / Q, (cy : ℝ) / Q) u
      + lamB l * Gv Q kq XSq YSq ((cx : ℝ) / Q, (cy : ℝ) / Q) u ≤ 0 := by
  have hQr : (0 : ℝ) < Q := by exact_mod_cast hQ
  have hRr : (0 : ℝ) < R := by exact_mod_cast hR
  have hv0 : (U0 : ℝ) ≤ u * R := by rw [div_le_iff₀ hRr] at hu0; linarith
  have hv1 : u * R ≤ (U1 : ℝ) := by rw [le_div_iff₀ hRr] at hu1; linarith
  have hq := cornOk_qnp hU01 hU1 h _ hv0 hv1
  simp only [combQ, sv_comb] at hq
  have e1 := gq_eval Q R kp (XSp, cx) (YSp, cy) hQ hR (u * R)
  have e2 := gq_eval Q R kq (XSq, cx) (YSq, cy) hQ hR (u * R)
  have huR : u * R / R = u := by field_simp
  rw [huR] at e1 e2
  set g := gq Q R kp (XSp, cx) (YSp, cy)
  set g' := gq Q R kq (XSq, cx) (YSq, cy)
  have hq2 : lamA l * (sv g.1 + sv g.2.1 * (u * R) + sv g.2.2 * (u * R) ^ 2)
      + lamB l * (sv g'.1 + sv g'.2.1 * (u * R) + sv g'.2.2 * (u * R) ^ 2) ≤ 0 := by
    convert hq using 1; ring
  rw [e1, e2] at hq2
  have ex : ∀ X c : ℕ, sv (X, c) / Q = (X : ℝ) / Q - (c : ℝ) / Q := by
    intro X c; rw [sv_mk, sub_div]
  rw [ex, ex, ex, ex] at hq2
  simp only [Gv]
  have hpos : (0 : ℝ) < Q * R ^ 2 := by positivity
  have key : (Q : ℝ) * R ^ 2 * (lamA l * gval (kf kp) ((XSp : ℝ) / Q - (cx : ℝ) / Q)
      ((YSp : ℝ) / Q - (cy : ℝ) / Q) u + lamB l * gval (kf kq) ((XSq : ℝ) / Q - (cx : ℝ) / Q)
      ((YSq : ℝ) / Q - (cy : ℝ) / Q) u) ≤ 0 := by
    convert hq2 using 1; ring
  by_contra hc
  exact absurd key (not_le.mpr (mul_pos hpos (not_le.mp hc)))

/-- An affine function of `(x, y)` that is `≤ 0` at the four corners of a rectangle is `≤ 0` on
it. -/
lemma affine_corners {K A B x0 x1 y0 y1 x y : ℝ} (hx0 : x0 ≤ x) (hx1 : x ≤ x1) (hy0 : y0 ≤ y)
    (hy1 : y ≤ y1) (h00 : K + A * x0 + B * y0 ≤ 0) (h01 : K + A * x0 + B * y1 ≤ 0)
    (h10 : K + A * x1 + B * y0 ≤ 0) (h11 : K + A * x1 + B * y1 ≤ 0) : K + A * x + B * y ≤ 0 := by
  rcases le_total 0 A with hA | hA <;> rcases le_total 0 B with hB | hB
  · nlinarith [mul_le_mul_of_nonneg_left hx1 hA, mul_le_mul_of_nonneg_left hy1 hB]
  · nlinarith [mul_le_mul_of_nonneg_left hx1 hA, mul_le_mul_of_nonpos_left hy0 hB]
  · nlinarith [mul_le_mul_of_nonpos_left hx0 hA, mul_le_mul_of_nonneg_left hy1 hB]
  · nlinarith [mul_le_mul_of_nonpos_left hx0 hA, mul_le_mul_of_nonpos_left hy0 hB]

/-- The combination of two violation polynomials is affine in the centre. -/
lemma comb_affine (Q l kp XSp YSp kq XSq YSq : ℕ) (u : ℝ) :
    ∃ K A B : ℝ, ∀ c : ℝ × ℝ, lamA l * Gv Q kp XSp YSp c u + lamB l * Gv Q kq XSq YSq c u
      = K + A * c.1 + B * c.2 := by
  refine ⟨lamA l * (-(1 + u ^ 2) + galpha (kf kp) u * ((XSp : ℝ) / Q)
        + gbeta (kf kp) u * ((YSp : ℝ) / Q))
      + lamB l * (-(1 + u ^ 2) + galpha (kf kq) u * ((XSq : ℝ) / Q)
        + gbeta (kf kq) u * ((YSq : ℝ) / Q)),
    -(lamA l * galpha (kf kp) u + lamB l * galpha (kf kq) u),
    -(lamA l * gbeta (kf kp) u + lamB l * gbeta (kf kq) u), fun c => ?_⟩
  simp only [Gv, gval_eq]; ring

lemma cfree_const {Q l kp XSp YSp kq XSq YSq : ℕ} (h : cfree l kp kq = true) (u : ℝ)
    (c c' : ℝ × ℝ) :
    lamA l * Gv Q kp XSp YSp c u + lamB l * Gv Q kq XSq YSq c u
      = lamA l * Gv Q kp XSp YSp c' u + lamB l * Gv Q kq XSq YSq c' u := by
  simp only [cfree, Bool.or_eq_true, Bool.and_eq_true, Nat.beq_eq] at h
  rcases h with ⟨rfl, rfl⟩ | ⟨rfl, (((⟨rfl, rfl⟩ | ⟨rfl, rfl⟩) | ⟨rfl, rfl⟩) | ⟨rfl, rfl⟩)⟩ <;>
    simp only [Gv, gval_eq, lamA, lamB, kf, galpha, gbeta] <;> norm_num <;> ring

/-- **Soundness of `pairOk`** (Lemma E): the combination is `≤ 0` at every pose of the box. -/
theorem pairOk_sound {Q R x0 x1 y0 y1 U0 U1 l kp XSp YSp kq XSq YSq : ℕ} (hQ : 0 < Q) (hR : 0 < R)
    (hU01 : U0 ≤ U1) (hU1 : U1 ≤ R)
    (h : pairOk Q R x0 x1 y0 y1 U0 U1 l kp XSp YSp kq XSq YSq = true) {c : ℝ × ℝ} {u : ℝ}
    (hx0 : (x0 : ℝ) / Q ≤ c.1) (hx1 : c.1 ≤ (x1 : ℝ) / Q)
    (hy0 : (y0 : ℝ) / Q ≤ c.2) (hy1 : c.2 ≤ (y1 : ℝ) / Q)
    (hu0 : (U0 : ℝ) / R ≤ u) (hu1 : u ≤ (U1 : ℝ) / R) :
    lamA l * Gv Q kp XSp YSp c u + lamB l * Gv Q kq XSq YSq c u ≤ 0 := by
  simp only [pairOk, Bool.and_eq_true, Bool.or_eq_true] at h
  rcases h with ⟨hcf, h00⟩ | ⟨⟨⟨h00, h01⟩, h10⟩, h11⟩
  · rw [cfree_const hcf u c ((x0 : ℝ) / Q, (y0 : ℝ) / Q)]
    exact cornOk_sound hQ hR hU01 hU1 h00 hu0 hu1
  obtain ⟨K, A, B, hf⟩ := comb_affine Q l kp XSp YSp kq XSq YSq u
  have c00 := cornOk_sound hQ hR hU01 hU1 h00 hu0 hu1
  have c01 := cornOk_sound hQ hR hU01 hU1 h01 hu0 hu1
  have c10 := cornOk_sound hQ hR hU01 hU1 h10 hu0 hu1
  have c11 := cornOk_sound hQ hR hU01 hU1 h11 hu0 hu1
  rw [hf] at c00 c01 c10 c11 ⊢
  exact affine_corners hx0 hx1 hy0 hy1 c00 c01 c10 c11

/-! ## Lemma A with the wall bounds (`ADM`) -/

/-- `Q·U`, `U = 2(1+u²)p_x − X_n`, for the box bound `X_n = xnR (c/Q)`. -/
def uR (XS c : ℕ) : SP × SP × SP :=
  ((Nat.mul 2 XS, Nat.mul 2 c), (0, 0), (Nat.mul 2 XS, Nat.mul 2 c))

/-- `Q·U` for the wall bound `X_n = xnW` (`c ≥ w(θ)/2`). -/
def uW (Q XS : ℕ) : SP × SP × SP :=
  ((Nat.mul 2 XS, Q), (0, Nat.mul 2 Q), (Nat.add (Nat.mul 2 XS) Q, 0))

/-- `Q R⁴ · condPoly_k(U, V)(v/R)` as the coefficients of a quartic in `v` (`_cond_poly_i`). -/
def cpoly (Q R : ℕ) (k : ℕ) (U V : SP × SP × SP) : SP × SP × SP × SP × SP :=
  let q : SP := (Q, 0)
  let q2 : SP := (Nat.mul 2 Q, 0)
  let c : SP × SP × SP × SP × SP :=
    match k with
    | 0 => (ssub U.1 q, sadd U.2.1 (sk 2 V.1), ssub (sadd (ssub U.2.2 U.1) (sk 2 V.2.1)) q2,
            sadd (sneg U.2.1) (sk 2 V.2.2), sneg (sadd U.2.2 q))
    | 1 => (sneg (sadd U.1 q), sneg (sadd U.2.1 (sk 2 V.1)),
            ssub (ssub (ssub U.1 U.2.2) (sk 2 V.2.1)) q2, ssub U.2.1 (sk 2 V.2.2), ssub U.2.2 q)
    | 2 => (ssub V.1 q, ssub V.2.1 (sk 2 U.1), ssub (ssub (ssub V.2.2 V.1) (sk 2 U.2.1)) q2,
            sneg (sadd V.2.1 (sk 2 U.2.2)), sneg (sadd V.2.2 q))
    | _ => (sneg (sadd V.1 q), ssub (sk 2 U.1) V.2.1, ssub (sadd (ssub V.1 V.2.2) (sk 2 U.2.1)) q2,
            sadd V.2.1 (sk 2 U.2.2), ssub V.2.2 q)
  (sk (Nat.mul (Nat.mul R R) (Nat.mul R R)) c.1, sk (Nat.mul (Nat.mul R R) R) c.2.1,
    sk (Nat.mul R R) c.2.2.1, sk R c.2.2.2.1, c.2.2.2.2)

/-- A quartic is `≤ 0` on the bin (Bernstein). -/
def bOk5 (p : SP × SP × SP × SP × SP) (U0 U1 : ℕ) : Bool :=
  bOk p.1 p.2.1 p.2.2.1 p.2.2.2.1 p.2.2.2.2 U0 U1

/-- `Q·Ur = svT U`: the signed triple `U` represents `Q` times the real triple `Ur`. -/
def Rep (Q : ℕ) (U : SP × SP × SP) (Ur : ℝ × ℝ × ℝ) : Prop :=
  sv U.1 = Q * Ur.1 ∧ sv U.2.1 = Q * Ur.2.1 ∧ sv U.2.2 = Q * Ur.2.2

lemma rep_uR {Q : ℕ} (hQ : 0 < Q) (XS c : ℕ) :
    Rep Q (uR XS c) (ucoef ((XS : ℝ) / Q) (xnR ((c : ℝ) / Q))) := by
  have hQr : (Q : ℝ) ≠ 0 := by exact_mod_cast hQ.ne'
  refine ⟨?_, ?_, ?_⟩ <;> simp only [uR, ucoef, xnR, sv_mk, nat_mul_eq, Nat.cast_mul,
    Nat.cast_ofNat, Nat.cast_zero] <;> field_simp
  ring

lemma rep_uW {Q : ℕ} (hQ : 0 < Q) (XS : ℕ) : Rep Q (uW Q XS) (ucoef ((XS : ℝ) / Q) xnW) := by
  have hQr : (Q : ℝ) ≠ 0 := by exact_mod_cast hQ.ne'
  refine ⟨?_, ?_, ?_⟩ <;> simp only [uW, ucoef, xnW, sv_mk, nat_mul_eq, nat_add_eq,
    Nat.cast_mul, Nat.cast_add, Nat.cast_ofNat, Nat.cast_zero] <;> field_simp <;> ring

lemma cpoly_eval {Q R : ℕ} (hR : 0 < R) (k : ℕ) {U V : SP × SP × SP} {Ur Vr : ℝ × ℝ × ℝ}
    (hU : Rep Q U Ur) (hV : Rep Q V Vr) (v : ℝ) :
    sv (cpoly Q R k U V).1 + sv (cpoly Q R k U V).2.1 * v + sv (cpoly Q R k U V).2.2.1 * v ^ 2
      + sv (cpoly Q R k U V).2.2.2.1 * v ^ 3 + sv (cpoly Q R k U V).2.2.2.2 * v ^ 4
      = (Q : ℝ) * R ^ 4 * qeval4 (condPoly (kf k) Ur Vr) (v / R) := by
  have hRr : (R : ℝ) ≠ 0 := by exact_mod_cast hR.ne'
  obtain ⟨u1, u2, u3⟩ := hU
  obtain ⟨v1, v2, v3⟩ := hV
  rcases k with _ | _ | _ | k <;>
    simp only [cpoly, kf, condPoly, qeval4, sv_sadd, sv_ssub, sv_sneg, sv_sk, sv_mk, nat_mul_eq,
      Nat.cast_mul, Nat.cast_ofNat, Nat.cast_zero, sub_zero, u1, u2, u3, v1, v2, v3] <;>
    field_simp <;> ring

/-- The quartic test at a bound pair, read back as the violation polynomial at the corner
`(X_n(u), Y_n(u))/(2(1+u²))`. -/
lemma w4_sound {Q R U0 U1 k : ℕ} {U V : SP × SP × SP} {px py : ℝ} {Xn Yn : ℝ × ℝ × ℝ}
    (hQ : 0 < Q) (hR : 0 < R) (hU01 : U0 ≤ U1)
    (hU : Rep Q U (ucoef px Xn)) (hV : Rep Q V (ucoef py Yn))
    (h : bOk5 (cpoly Q R k U V) U0 U1 = true) {u : ℝ}
    (hu0 : (U0 : ℝ) / R ≤ u) (hu1 : u ≤ (U1 : ℝ) / R) :
    gval (kf k) (px - qeval Xn u / (2 * (1 + u ^ 2))) (py - qeval Yn u / (2 * (1 + u ^ 2))) u
      ≤ 0 := by
  have hQr : (0 : ℝ) < Q := by exact_mod_cast hQ
  have hRr : (0 : ℝ) < R := by exact_mod_cast hR
  have hv0 : (U0 : ℝ) ≤ u * R := by rw [div_le_iff₀ hRr] at hu0; linarith
  have hv1 : u * R ≤ (U1 : ℝ) := by rw [le_div_iff₀ hRr] at hu1; linarith
  have hb := bOk_sound h hU01 hv0 hv1
  rw [cpoly_eval hR k hU hV] at hb
  have huR : u * R / R = u := by field_simp
  rw [huR] at hb
  have hpos : (0 : ℝ) < Q * R ^ 4 := by positivity
  have hq : qeval4 (condPoly (kf k) (ucoef px Xn) (ucoef py Yn)) u ≤ 0 := by
    by_contra hc
    exact absurd hb (not_le.mpr (mul_pos hpos (not_le.mp hc)))
  exact (condPoly_nonpos_iff _ _ _ _ _ _).mp hq

def rrOk (Q R U0 U1 k XS YS cx cy : ℕ) : Bool :=
  rrFast Q R U0 U1 k XS YS cx cy || qOk3 (gq Q R k (XS, cx) (YS, cy)) U0 U1

/-- The quadratic test at a constant corner, read back. -/
lemma rr_sound {Q R U0 U1 k XS YS cx cy : ℕ} (hQ : 0 < Q) (hR : 0 < R) (hU01 : U0 ≤ U1)
    (hU1 : U1 ≤ R)
    (h : rrOk Q R U0 U1 k XS YS cx cy = true) {u : ℝ} (hu0 : (U0 : ℝ) / R ≤ u)
    (hu1 : u ≤ (U1 : ℝ) / R) :
    gval (kf k) ((XS : ℝ) / Q - (cx : ℝ) / Q) ((YS : ℝ) / Q - (cy : ℝ) / Q) u ≤ 0 := by
  have hQr : (0 : ℝ) < Q := by exact_mod_cast hQ
  have hRr : (0 : ℝ) < R := by exact_mod_cast hR
  have hv0 : (U0 : ℝ) ≤ u * R := by rw [div_le_iff₀ hRr] at hu0; linarith
  have hv1 : u * R ≤ (U1 : ℝ) := by rw [le_div_iff₀ hRr] at hu1; linarith
  have hqnp : QNP (gq Q R k (XS, cx) (YS, cy)).1 (gq Q R k (XS, cx) (YS, cy)).2.1
      (gq Q R k (XS, cx) (YS, cy)).2.2 U0 U1 := by
    simp only [rrOk, Bool.or_eq_true] at h
    rcases h with h | h
    · exact rrFast_qnp hU01 hU1 h
    · exact qOk_qnp h
  have hq := hqnp _ hv0 hv1
  rw [gq_eval Q R k _ _ hQ hR] at hq
  have huR : u * R / R = u := by field_simp
  rw [huR] at hq
  simp only [sv_mk, sub_div] at hq
  have hpos : (0 : ℝ) < Q * R ^ 2 := by positivity
  by_contra hc
  exact absurd hq (not_le.mpr (mul_pos hpos (not_le.mp hc)))

/-- **Lemma A** for the four kinds: the violation polynomial is monotone in the offsets, with the
signs of its coefficients for `u ∈ [0,1]`. -/
lemma gval0_mono {a b a' b' u : ℝ} (hu0 : 0 ≤ u) (hu1 : u ≤ 1) (ha : a ≤ a') (hb : b ≤ b') :
    gval 0 a b u ≤ gval 0 a' b' u := by
  rw [gval_eq, gval_eq]; simp only [galpha, gbeta]
  nlinarith [mul_nonneg (by nlinarith : (0 : ℝ) ≤ 2 * (1 - u ^ 2)) (sub_nonneg.mpr ha),
    mul_nonneg (by linarith : (0 : ℝ) ≤ 4 * u) (sub_nonneg.mpr hb)]
lemma gval1_mono {a b a' b' u : ℝ} (hu0 : 0 ≤ u) (hu1 : u ≤ 1) (ha : a' ≤ a) (hb : b' ≤ b) :
    gval 1 a b u ≤ gval 1 a' b' u := by
  rw [gval_eq, gval_eq]; simp only [galpha, gbeta]
  nlinarith [mul_nonneg (by nlinarith : (0 : ℝ) ≤ 2 * (1 - u ^ 2)) (sub_nonneg.mpr ha),
    mul_nonneg (by linarith : (0 : ℝ) ≤ 4 * u) (sub_nonneg.mpr hb)]
lemma gval2_mono {a b a' b' u : ℝ} (hu0 : 0 ≤ u) (hu1 : u ≤ 1) (ha : a' ≤ a) (hb : b ≤ b') :
    gval 2 a b u ≤ gval 2 a' b' u := by
  rw [gval_eq, gval_eq]; simp only [galpha, gbeta]
  nlinarith [mul_nonneg (by nlinarith : (0 : ℝ) ≤ 2 * (1 - u ^ 2)) (sub_nonneg.mpr hb),
    mul_nonneg (by linarith : (0 : ℝ) ≤ 4 * u) (sub_nonneg.mpr ha)]
lemma gval3_mono {a b a' b' u : ℝ} (hu0 : 0 ≤ u) (hu1 : u ≤ 1) (ha : a ≤ a') (hb : b' ≤ b) :
    gval 3 a b u ≤ gval 3 a' b' u := by
  rw [gval_eq, gval_eq]; simp only [galpha, gbeta]
  nlinarith [mul_nonneg (by nlinarith : (0 : ℝ) ≤ 2 * (1 - u ^ 2)) (sub_nonneg.mpr hb),
    mul_nonneg (by linarith : (0 : ℝ) ≤ 4 * u) (sub_nonneg.mpr ha)]

def w4Ok (Q R U0 U1 k : ℕ) (U V : SP × SP × SP) : Bool := bOk5 (cpoly Q R k U V) U0 U1

/-- **`ADM`** (`_adm_cond_ok_int`): condition `k` of the point `(XS, YS)/Q` holds at every
admissible pose of the box, tested at the condition's corner (Lemma A) with the lower centre
bounds taken as the box side (`'R'`, exact quadratic maximum) or the wall `w(θ)/2` (`'W'`,
Bernstein). -/
def admK (Q R x0 x1 y0 y1 U0 U1 XS YS : ℕ) (k : ℕ) : Bool :=
  match k with
  | 0 => rrOk Q R U0 U1 0 XS YS x0 y0 || w4Ok Q R U0 U1 0 (uR XS x0) (uW Q YS) ||
      w4Ok Q R U0 U1 0 (uW Q XS) (uR YS y0) || w4Ok Q R U0 U1 0 (uW Q XS) (uW Q YS)
  | 1 => rrOk Q R U0 U1 1 XS YS x1 y1
  | 2 => rrOk Q R U0 U1 2 XS YS x1 y0 || w4Ok Q R U0 U1 2 (uR XS x1) (uW Q YS)
  | _ => rrOk Q R U0 U1 3 XS YS x0 y1 || w4Ok Q R U0 U1 3 (uW Q XS) (uR YS y1)

/-- **Soundness of `admK`.** -/
theorem admK_sound {Q R x0 x1 y0 y1 U0 U1 XS YS k : ℕ} (hQ : 0 < Q) (hR : 0 < R)
    (hU01 : U0 ≤ U1) (hU1 : U1 ≤ R) (h : admK Q R x0 x1 y0 y1 U0 U1 XS YS k = true)
    {c : ℝ × ℝ} {u : ℝ}
    (hx0 : (x0 : ℝ) / Q ≤ c.1) (hx1 : c.1 ≤ (x1 : ℝ) / Q)
    (hy0 : (y0 : ℝ) / Q ≤ c.2) (hy1 : c.2 ≤ (y1 : ℝ) / Q)
    (hu0 : (U0 : ℝ) / R ≤ u) (hu1 : u ≤ (U1 : ℝ) / R)
    (hwx : wid (2 * Real.arctan u) / 2 ≤ c.1) (hwy : wid (2 * Real.arctan u) / 2 ≤ c.2) :
    Gv Q k XS YS c u ≤ 0 := by
  have hRr : (0 : ℝ) < R := by exact_mod_cast hR
  have hu0' : 0 ≤ u := le_trans (div_nonneg (Nat.cast_nonneg _) hRr.le) hu0
  have hu1' : u ≤ 1 := le_trans hu1 ((div_le_one hRr).mpr (by exact_mod_cast hU1))
  have eR : ∀ a : ℝ, qeval (xnR a) u / (2 * (1 + u ^ 2)) = a := fun a => xnR_spec a u
  have eW : qeval xnW u / (2 * (1 + u ^ 2)) = wid (2 * Real.arctan u) / 2 := xnW_spec hu0' hu1'
  have W4 := fun {k : ℕ} {U V} {px py} {Xn Yn} (hU : Rep Q U (ucoef px Xn))
      (hV : Rep Q V (ucoef py Yn)) (h : bOk5 (cpoly Q R k U V) U0 U1 = true) =>
    w4_sound hQ hR hU01 hU hV h hu0 hu1
  unfold Gv
  rcases k with _ | _ | _ | k
  · simp only [admK, Bool.or_eq_true] at h
    rcases h with ((h | h) | h) | h
    · exact le_trans (gval0_mono hu0' hu1' (by linarith) (by linarith))
        (rr_sound hQ hR hU01 hU1 h hu0 hu1)
    · have := W4 (rep_uR hQ XS x0) (rep_uW hQ YS) h
      rw [eR, eW] at this
      exact le_trans (gval0_mono hu0' hu1' (by linarith) (by linarith)) this
    · have := W4 (rep_uW hQ XS) (rep_uR hQ YS y0) h
      rw [eR, eW] at this
      exact le_trans (gval0_mono hu0' hu1' (by linarith) (by linarith)) this
    · have := W4 (rep_uW hQ XS) (rep_uW hQ YS) h
      rw [eW] at this
      exact le_trans (gval0_mono hu0' hu1' (by linarith) (by linarith)) this
  · simp only [admK] at h
    exact le_trans (gval1_mono hu0' hu1' (by linarith) (by linarith))
        (rr_sound hQ hR hU01 hU1 h hu0 hu1)
  · simp only [admK, Bool.or_eq_true] at h
    rcases h with h | h
    · exact le_trans (gval2_mono hu0' hu1' (by linarith) (by linarith))
        (rr_sound hQ hR hU01 hU1 h hu0 hu1)
    · have := W4 (rep_uR hQ XS x1) (rep_uW hQ YS) h
      rw [eR, eW] at this
      exact le_trans (gval2_mono hu0' hu1' (by linarith) (by linarith)) this
  · simp only [admK, Bool.or_eq_true] at h
    rcases h with h | h
    · exact le_trans (gval3_mono hu0' hu1' (by linarith) (by linarith))
        (rr_sound hQ hR hU01 hU1 h hu0 hu1)
    · have := W4 (rep_uW hQ XS) (rep_uR hQ YS y1) h
      rw [eR, eW] at this
      exact le_trans (gval3_mono hu0' hu1' (by linarith) (by linarith)) this

/-! ### Fast `ADM` without walls: `BoxTree.ptOk` with one kind skipped

`BoxTree.ptOk` tests all four conditions on the whole rectangle with shared products (12 linear
tests; `ptOk_mem`).  `ptOkK kp` skips the test of kind `kp` (`kp ≥ 4`: none), so it serves both the
`ADM` witnesses (`kp = 4`) and the three non-swing conditions of a chain entry.  It implies the
corresponding `admK` tests, so it only saves kernel time. -/

def triOkK (kp G α β xl xh yl yh aX bY bX aY : ℕ) : Bool :=
  (Nat.beq kp 0 || Nat.ble (Nat.add aX bY) (Nat.add (Nat.add G (Nat.mul α xl)) (Nat.mul β yl))) &&
  (Nat.beq kp 1 || Nat.ble (Nat.add (Nat.mul α xh) (Nat.mul β yh)) (Nat.add (Nat.add G aX) bY)) &&
  (Nat.beq kp 2 || Nat.ble (Nat.add aY (Nat.mul β xh)) (Nat.add (Nat.add G bX) (Nat.mul α yl))) &&
  (Nat.beq kp 3 || Nat.ble (Nat.add bX (Nat.mul α yh)) (Nat.add (Nat.add G aY) (Nat.mul β xl)))

def triPtK (kp Q α β γ xl xh yl yh X Y : ℕ) : Bool :=
  triOkK kp (Nat.mul γ Q) α β xl xh yl yh (Nat.mul α X) (Nat.mul β Y) (Nat.mul β X) (Nat.mul α Y)

def ptOkK (kp Q R U0 U1 xl xh yl yh X Y : ℕ) : Bool :=
  triPtK kp Q (Nat.mul 2 (Nat.sub (Nat.mul R R) (Nat.mul U0 U0))) (Nat.mul 4 (Nat.mul R U0))
    (Nat.add (Nat.mul R R) (Nat.mul U0 U0)) xl xh yl yh X Y &&
  triPtK kp Q (Nat.mul 2 (Nat.sub (Nat.mul R R) (Nat.mul U1 U1))) (Nat.mul 4 (Nat.mul R U1))
    (Nat.add (Nat.mul R R) (Nat.mul U1 U1)) xl xh yl yh X Y &&
  triPtK kp Q (Nat.mul 2 (Nat.sub (Nat.mul R R) (Nat.mul U0 U1)))
    (Nat.mul 2 (Nat.mul R (Nat.add U0 U1))) (Nat.add (Nat.mul R R) (Nat.mul U0 U1)) xl xh yl yh X Y

lemma triOkK_sound {kp G α β xl xh yl yh X Y : ℕ}
    (h : triOkK kp G α β xl xh yl yh (Nat.mul α X) (Nat.mul β Y) (Nat.mul β X) (Nat.mul α Y)
      = true) :
    (kp ≠ 0 → (α : ℝ) * ((X : ℝ) - xl) + β * ((Y : ℝ) - yl) ≤ G) ∧
    (kp ≠ 1 → (α : ℝ) * ((xh : ℝ) - X) + β * ((yh : ℝ) - Y) ≤ G) ∧
    (kp ≠ 2 → (α : ℝ) * ((Y : ℝ) - yl) + β * ((xh : ℝ) - X) ≤ G) ∧
    (kp ≠ 3 → (α : ℝ) * ((yh : ℝ) - Y) + β * ((X : ℝ) - xl) ≤ G) := by
  simp only [triOkK, Bool.and_eq_true, Bool.or_eq_true, Nat.beq_eq, Nat.ble_eq, nat_add_eq,
    nat_mul_eq] at h
  obtain ⟨⟨⟨h1, h2⟩, h3⟩, h4⟩ := h
  refine ⟨fun hk => ?_, fun hk => ?_, fun hk => ?_, fun hk => ?_⟩
  · have c : ((α * X + β * Y : ℕ) : ℝ) ≤ ((G + α * xl + β * yl : ℕ) : ℝ) := by
      exact_mod_cast h1.resolve_left hk
    push_cast at c; linarith
  · have c : ((α * xh + β * yh : ℕ) : ℝ) ≤ ((G + α * X + β * Y : ℕ) : ℝ) := by
      exact_mod_cast h2.resolve_left hk
    push_cast at c; linarith
  · have c : ((α * Y + β * xh : ℕ) : ℝ) ≤ ((G + β * X + α * yl : ℕ) : ℝ) := by
      exact_mod_cast h3.resolve_left hk
    push_cast at c; linarith
  · have c : ((β * X + α * yh : ℕ) : ℝ) ≤ ((G + α * Y + β * xl : ℕ) : ℝ) := by
      exact_mod_cast h4.resolve_left hk
    push_cast at c; linarith

/-- **Soundness of `ptOkK`** (as `BoxTree.ptOk_mem`, kind by kind). -/
theorem ptOkK_sound {kp Q R U0 U1 xl xh yl yh X Y : ℕ} (hQ : 0 < Q) (hR : 0 < R) (hU : U0 ≤ U1)
    (hU1 : U1 ≤ R) (h : ptOkK kp Q R U0 U1 xl xh yl yh X Y = true) (c : ℝ × ℝ) (u : ℝ)
    (hu0 : (U0 : ℝ) / R ≤ u) (hu1 : u ≤ (U1 : ℝ) / R)
    (hx0 : (xl : ℝ) / Q ≤ c.1) (hx1 : c.1 ≤ (xh : ℝ) / Q)
    (hy0 : (yl : ℝ) / Q ≤ c.2) (hy1 : c.2 ≤ (yh : ℝ) / Q) (k : Fin 4) (hk : k.val ≠ kp) :
    gval k ((X : ℝ) / Q - c.1) ((Y : ℝ) / Q - c.2) u ≤ 0 := by
  have hQr : (0 : ℝ) < Q := by exact_mod_cast hQ
  have hRr : (0 : ℝ) < R := by exact_mod_cast hR
  have hU0r : (0 : ℝ) ≤ U0 := Nat.cast_nonneg _
  have hU1r : (U1 : ℝ) ≤ R := by exact_mod_cast hU1
  simp only [ptOkK, triPtK, Bool.and_eq_true] at h
  obtain ⟨⟨h0, h1⟩, hm⟩ := h
  have T0 := triOkK_sound h0
  have T1 := triOkK_sound h1
  have Tm := triOkK_sound hm
  have n00 : U0 * U0 ≤ R * R := Nat.mul_le_mul (le_trans hU hU1) (le_trans hU hU1)
  have n11 : U1 * U1 ≤ R * R := Nat.mul_le_mul hU1 hU1
  have n01 : U0 * U1 ≤ R * R := Nat.mul_le_mul (le_trans hU hU1) hU1
  rw [cast_alpha n00] at T0
  rw [cast_alpha n11] at T1
  rw [cast_alpha n01] at Tm
  simp only [nat_mul_eq, nat_add_eq] at T0 T1 Tm
  push_cast at T0 T1 Tm
  set v := u * R with hv
  have hv0 : (U0 : ℝ) ≤ v := by rw [div_le_iff₀ hRr] at hu0; linarith
  have hv1 : v ≤ (U1 : ℝ) := by rw [le_div_iff₀ hRr] at hu1; linarith
  have hu0' : 0 ≤ u := le_trans (div_nonneg hU0r hRr.le) hu0
  have hu1' : u ≤ 1 := le_trans hu1 ((div_le_one hRr).mpr hU1r)
  have cx0 : (xl : ℝ) ≤ c.1 * Q := by rw [div_le_iff₀ hQr] at hx0; linarith
  have cx1 : c.1 * Q ≤ (xh : ℝ) := by rw [le_div_iff₀ hQr] at hx1; linarith
  have cy0 : (yl : ℝ) ≤ c.2 * Q := by rw [div_le_iff₀ hQr] at hy0; linarith
  have cy1 : c.2 * Q ≤ (yh : ℝ) := by rw [le_div_iff₀ hQr] at hy1; linarith
  have eX : ((X : ℝ) / Q - c.1) * Q = X - c.1 * Q := by field_simp
  have eY : ((Y : ℝ) / Q - c.2) * Q = Y - c.2 * Q := by field_simp
  have L := fun {a b : ℝ}
      (e0 : 2 * ((R : ℝ) ^ 2 - U0 * U0) * a + 4 * R * U0 * b ≤ (R ^ 2 + U0 * U0) * Q)
      (e1 : 2 * ((R : ℝ) ^ 2 - U1 * U1) * a + 4 * R * U1 * b ≤ (R ^ 2 + U1 * U1) * Q)
      (em : 2 * ((R : ℝ) ^ 2 - U0 * U1) * a + 2 * R * (U0 + U1) * b ≤ (R ^ 2 + U0 * U1) * Q) =>
    lin3 (Q := (Q : ℝ)) (R := (R : ℝ)) (v := v) (a := a) (b := b) hv0 hv1
      (by rw [pow_two]; linarith) (by rw [pow_two]; linarith) em
  fin_cases k
  · have hk0 : kp ≠ 0 := fun h => hk (by simp [h])
    refine gval0_le hQr hRr hu0' hu1' (ac := X - xl) (bc := Y - yl) (by rw [eX]; linarith)
      (by rw [eY]; linarith) (L ?_ ?_ ?_) <;> linarith [T0.1 hk0, T1.1 hk0, Tm.1 hk0]
  · have hk1 : kp ≠ 1 := fun h => hk (by simp [h])
    change gval 1 _ _ _ ≤ 0
    rw [gval_one]
    refine gval0_le hQr hRr hu0' hu1' (ac := xh - X) (bc := yh - Y)
      (by rw [neg_mul, eX]; linarith)
      (by rw [neg_mul, eY]; linarith) (L ?_ ?_ ?_) <;>
      linarith [T0.2.1 hk1, T1.2.1 hk1, Tm.2.1 hk1]
  · have hk2 : kp ≠ 2 := fun h => hk (by simp [h])
    change gval 2 _ _ _ ≤ 0
    rw [gval_two]
    refine gval0_le hQr hRr hu0' hu1' (ac := Y - yl) (bc := xh - X) (by rw [eY]; linarith)
      (by rw [neg_mul, eX]; linarith) (L ?_ ?_ ?_) <;>
      linarith [T0.2.2.1 hk2, T1.2.2.1 hk2, Tm.2.2.1 hk2]
  · have hk3 : kp ≠ 3 := fun h => hk (by simp [h])
    change gval 3 _ _ _ ≤ 0
    rw [gval_three]
    refine gval0_le hQr hRr hu0' hu1' (ac := yh - Y) (bc := X - xl)
      (by rw [neg_mul, eY]; linarith)
      (by rw [eX]; linarith) (L ?_ ?_ ?_) <;>
      linarith [T0.2.2.2 hk3, T1.2.2.2 hk3, Tm.2.2.2 hk3]

/-! ## Widths: `E` leaves and `clip_bin` -/

lemma widU_sub (x y : ℝ) : widU y - widU x
    = 2 * (y - x) * (1 - (x + y + x * y)) / ((1 + x ^ 2) * (1 + y ^ 2)) := by
  have hx : (0 : ℝ) < 1 + x ^ 2 := by positivity
  have hy : (0 : ℝ) < 1 + y ^ 2 := by positivity
  rw [widU, widU]; field_simp; ring

/-- `w` is quasi-concave on `[0, ∞)`: on `[a, b]` it is at least its smaller endpoint value. -/
lemma widU_ge_min {a u b : ℝ} (ha : 0 ≤ a) (hau : a ≤ u) (hub : u ≤ b) :
    min (widU a) (widU b) ≤ widU u := by
  have hu : 0 ≤ u := le_trans ha hau
  have hd1 : (0 : ℝ) < (1 + a ^ 2) * (1 + u ^ 2) := by positivity
  have hd2 : (0 : ℝ) < (1 + u ^ 2) * (1 + b ^ 2) := by positivity
  rcases le_total 0 (1 - (a + u + a * u)) with h | h
  · have := widU_sub a u
    have : 0 ≤ widU u - widU a := by
      rw [this]; exact div_nonneg (by nlinarith) hd1.le
    exact le_trans (min_le_left _ _) (by linarith)
  · have h' : 1 - (u + b + u * b) ≤ 0 := by nlinarith
    have := widU_sub u b
    have : widU b - widU u ≤ 0 := by
      rw [this]; exact div_nonpos_of_nonpos_of_nonneg (by nlinarith) hd2.le
    exact le_trans (min_le_right _ _) (by linarith)

/-- `w(U/R)/2 > K/Q`, in naturals (`U ≤ R`). -/
def wgt (Q R U K : ℕ) : Bool :=
  Nat.blt (Nat.mul (Nat.mul 2 K) (Nat.add (Nat.mul R R) (Nat.mul U U)))
    (Nat.mul Q (Nat.sub (Nat.add (Nat.mul R R) (Nat.mul 2 (Nat.mul U R))) (Nat.mul U U)))

/-- `w(U/R)/2 ≥ K/Q`, in naturals. -/
def wge (Q R U K : ℕ) : Bool :=
  Nat.ble (Nat.mul (Nat.mul 2 K) (Nat.add (Nat.mul R R) (Nat.mul U U)))
    (Nat.mul Q (Nat.sub (Nat.add (Nat.mul R R) (Nat.mul 2 (Nat.mul U R))) (Nat.mul U U)))

lemma widU_div (R U : ℕ) (hR : 0 < R) :
    widU ((U : ℝ) / R) = ((R : ℝ) * R + 2 * (U * R) - U * U) / (R * R + U * U) := by
  have hRr : (R : ℝ) ≠ 0 := by exact_mod_cast hR.ne'
  have hpos : (0 : ℝ) < R * R + U * U := by positivity
  rw [widU]; field_simp; ring

lemma sub_cast (R U : ℕ) (hU : U ≤ R) :
    ((Nat.sub (Nat.add (Nat.mul R R) (Nat.mul 2 (Nat.mul U R))) (Nat.mul U U) : ℕ) : ℝ)
      = (R : ℝ) * R + 2 * (U * R) - U * U := by
  have : U * U ≤ R * R + 2 * (U * R) := le_trans (Nat.mul_le_mul hU hU) (Nat.le_add_right _ _)
  simp only [nat_sub_eq, nat_add_eq, nat_mul_eq]
  rw [Nat.cast_sub this]; push_cast; ring

lemma wgt_sound {Q R U K : ℕ} (hQ : 0 < Q) (hR : 0 < R) (hU : U ≤ R) (h : wgt Q R U K = true) :
    (K : ℝ) / Q < widU ((U : ℝ) / R) / 2 := by
  have hQr : (0 : ℝ) < Q := by exact_mod_cast hQ
  have hpos : (0 : ℝ) < R * R + U * U := by
    have : (0 : ℝ) < R := by exact_mod_cast hR
    positivity
  have hsub : U * U ≤ R * R + 2 * (U * R) :=
    le_trans (Nat.mul_le_mul hU hU) (Nat.le_add_right _ _)
  simp only [wgt, Nat.blt_eq, nat_mul_eq, nat_add_eq, nat_sub_eq] at h
  have h' : ((2 * K * (R * R + U * U) : ℕ) : ℝ)
      < ((Q * (R * R + 2 * (U * R) - U * U) : ℕ) : ℝ) := by
    exact_mod_cast h
  push_cast [Nat.cast_sub hsub] at h'
  rw [widU_div R U hR, div_div, div_lt_div_iff₀ hQr (by positivity)]
  nlinarith

lemma wge_sound {Q R U K : ℕ} (hQ : 0 < Q) (hR : 0 < R) (hU : U ≤ R) (h : wge Q R U K = true) :
    (K : ℝ) / Q ≤ widU ((U : ℝ) / R) / 2 := by
  have hQr : (0 : ℝ) < Q := by exact_mod_cast hQ
  have hpos : (0 : ℝ) < R * R + U * U := by
    have : (0 : ℝ) < R := by exact_mod_cast hR
    positivity
  have hsub : U * U ≤ R * R + 2 * (U * R) :=
    le_trans (Nat.mul_le_mul hU hU) (Nat.le_add_right _ _)
  simp only [wge, Nat.ble_eq, nat_mul_eq, nat_add_eq, nat_sub_eq] at h
  have h' : ((2 * K * (R * R + U * U) : ℕ) : ℝ)
      ≤ ((Q * (R * R + 2 * (U * R) - U * U) : ℕ) : ℝ) := by
    exact_mod_cast h
  push_cast [Nat.cast_sub hsub] at h'
  rw [widU_div R U hR, div_div, div_le_div_iff₀ hQr (by positivity)]
  nlinarith

/-- **`E`**: `c₁ < w/2` (in `x` or in `y`) at both ends of the bin, so no pose of the box is
admissible. -/
def eOk (Q R x1 y1 U0 U1 : ℕ) : Bool :=
  (wgt Q R U0 x1 && wgt Q R U1 x1) || (wgt Q R U0 y1 && wgt Q R U1 y1)

/-- **`clip_bin`**: every pose with `u > us/R` is inadmissible — `w(us)/2 ≥ min(x₁, y₁)/Q` and `w`
increases on `[us, U₁]` (`(1 + us)(1 + u₁) < 2`). -/
def clipOk (Q R x1 y1 U0 U1 us : ℕ) : Bool :=
  Nat.ble U0 us && Nat.ble us U1 && wge Q R us (min x1 y1) &&
    Nat.blt (Nat.mul (Nat.add R us) (Nat.add R U1)) (Nat.mul 2 (Nat.mul R R))

/-- Admissible poses have `w/2 ≤ c` in both coordinates. -/
lemma adm_lo {m : ℝ} {c : ℝ × ℝ} {u : ℝ} (hsub : sq c (2 * Real.arctan u) 1 ⊆ box m) :
    wid (2 * Real.arctan u) / 2 ≤ c.1 ∧ wid (2 * Real.arctan u) / 2 ≤ c.2 := by
  obtain ⟨a1, _, a3, _⟩ := (sq_subset_box_iff m c _).mp hsub
  exact ⟨a1, a3⟩

theorem E_cov {D S Mq R W : ℕ} {pts : List (ℕ × ℕ × ℕ)} (hD : 0 < D) (hS : 0 < S) (hR : 0 < R)
    {x0 x1 y0 y1 U0 U1 : ℕ} (hU1 : U1 ≤ R) (h : eOk (D * S) R x1 y1 U0 U1 = true) :
    Cov D S Mq R W pts x0 x1 y0 y1 U0 U1 := by
  intro c u _ hx1 _ hy1 hu0 hu1 hsub
  exfalso
  have hQ : 0 < D * S := Nat.mul_pos hD hS
  have hRr : (0 : ℝ) < R := by exact_mod_cast hR
  have hQc : ((D : ℝ) * S) = ((D * S : ℕ) : ℝ) := by push_cast; ring
  rw [hQc] at hx1 hy1
  have hu0' : 0 ≤ u := le_trans (div_nonneg (Nat.cast_nonneg _) hRr.le) hu0
  have hu1' : u ≤ 1 := le_trans hu1 ((div_le_one hRr).mpr (by exact_mod_cast hU1))
  obtain ⟨wx, wy⟩ := adm_lo hsub
  rw [wid_two_arctan hu0' hu1'] at wx wy
  have hU0R : U0 ≤ R := by
    have : (U0 : ℝ) / R ≤ (U1 : ℝ) / R := le_trans hu0 hu1
    rw [div_le_div_iff_of_pos_right hRr] at this
    exact le_trans (by exact_mod_cast this) hU1
  have hmin := widU_ge_min (div_nonneg (Nat.cast_nonneg U0) hRr.le) hu0 hu1
  simp only [eOk, Bool.or_eq_true, Bool.and_eq_true] at h
  rcases h with ⟨h0, h1⟩ | ⟨h0, h1⟩
  · have e0 := wgt_sound hQ hR hU0R h0
    have e1 := wgt_sound hQ hR hU1 h1
    rcases min_choice (widU ((U0 : ℝ) / R)) (widU ((U1 : ℝ) / R)) with hm | hm <;>
      rw [hm] at hmin <;> linarith
  · have e0 := wgt_sound hQ hR hU0R h0
    have e1 := wgt_sound hQ hR hU1 h1
    rcases min_choice (widU ((U0 : ℝ) / R)) (widU ((U1 : ℝ) / R)) with hm | hm <;>
      rw [hm] at hmin <;> linarith

theorem C_cov {D S Mq R W : ℕ} {pts : List (ℕ × ℕ × ℕ)} (hD : 0 < D) (hS : 0 < S) (hR : 0 < R)
    {x0 x1 y0 y1 U0 U1 us : ℕ} (h : clipOk (D * S) R x1 y1 U0 U1 us = true)
    (hc : Cov D S Mq R W pts x0 x1 y0 y1 U0 us) : Cov D S Mq R W pts x0 x1 y0 y1 U0 U1 := by
  intro c u hx0 hx1 hy0 hy1 hu0 hu1 hsub
  simp only [clipOk, Bool.and_eq_true, Nat.ble_eq, Nat.blt_eq] at h
  obtain ⟨⟨⟨_, hsU1⟩, hw⟩, hmono⟩ := h
  rcases le_or_gt u ((us : ℝ) / R) with hle | hgt
  · exact hc c u hx0 hx1 hy0 hy1 hu0 hle hsub
  exfalso
  have hQ : 0 < D * S := Nat.mul_pos hD hS
  have hRr : (0 : ℝ) < R := by exact_mod_cast hR
  have hQc : ((D : ℝ) * S) = ((D * S : ℕ) : ℝ) := by push_cast; ring
  rw [hQc] at hx1 hy1
  simp only [nat_mul_eq, nat_add_eq] at hmono
  have hmr : ((R : ℝ) + us) * (R + U1) < 2 * (R * R) := by exact_mod_cast hmono
  have husR : us < R := by
    by_contra hh
    push Not at hh
    have : (R : ℝ) ≤ us := by exact_mod_cast hh
    nlinarith [(Nat.cast_nonneg U1 : (0 : ℝ) ≤ U1)]
  have hus0 : (0 : ℝ) ≤ (us : ℝ) / R := div_nonneg (Nat.cast_nonneg _) hRr.le
  have hu0' : 0 ≤ u := le_trans hus0 hgt.le
  have hU1R : (U1 : ℝ) < R := by nlinarith [(Nat.cast_nonneg us : (0 : ℝ) ≤ us)]
  have hu1' : u ≤ 1 := le_trans hu1 ((div_le_one hRr).mpr hU1R.le)
  obtain ⟨wx, wy⟩ := adm_lo hsub
  rw [wid_two_arctan hu0' hu1'] at wx wy
  have hK := wge_sound hQ hR husR.le hw
  -- `w(u) > w(us/R)`
  have hprod : 1 - ((us : ℝ) / R + u + (us : ℝ) / R * u) > 0 := by
    have hu1R : u * R ≤ U1 := by rw [le_div_iff₀ hRr] at hu1; linarith
    have e : 1 - ((us : ℝ) / R + u + (us : ℝ) / R * u)
        = (2 * (R * R) - (R + us) * (R + u * R)) / (R * R) := by field_simp; ring
    rw [e]
    apply div_pos _ (by positivity)
    nlinarith [(Nat.cast_nonneg us : (0 : ℝ) ≤ us)]
  have hinc : widU ((us : ℝ) / R) < widU u := by
    have := widU_sub ((us : ℝ) / R) u
    have hd : (0 : ℝ) < (1 + ((us : ℝ) / R) ^ 2) * (1 + u ^ 2) := by positivity
    have : 0 < widU u - widU ((us : ℝ) / R) := by
      rw [this]; exact div_pos (mul_pos (by linarith) hprod) hd
    linarith
  rcases min_choice x1 y1 with hm | hm <;> rw [hm] at hK
  · linarith
  · linarith

/-! ## The `Z` leaf -/

/-- A certificate entry `(X, Y, w)`, a chain pivot `(X, Y, kind)`, a reason `(d, u, l)` and a tag
`(kp, reason in chain A, reason in chain B)`. -/
abbrev Ent := ℕ × ℕ × ℕ
abbrev Piv := ℕ × ℕ × ℕ
abbrev Rsn := ℕ × ℕ × ℕ
abbrev Tag := ℕ × Rsn × Rsn

def dflt : Piv := (0, 0, 0)

/-- Lemma E against a pivot. -/
def pivOk (S Q R x0 x1 y0 y1 U0 U1 l kp XS YS : ℕ) (q : Piv) : Bool :=
  pairOk Q R x0 x1 y0 y1 U0 U1 l kp XS YS q.2.2 (Nat.mul q.1 S) (Nat.mul q.2.1 S)

/-- A reason `(d, u, l)`: `d > 0` — *down*, `G_p ≤ G_{q_d}` (Lemma F's down-set); `u > 0` — *up*,
`λ_a G_p + λ_b G_{q_u} ≤ 0` with `λ_b > 0` (Lemma G). -/
def rsnOk (S Q R x0 x1 y0 y1 U0 U1 : ℕ) (ch : List Piv) (kp XS YS : ℕ) (rs : Rsn) : Bool :=
  (Nat.beq rs.1 0 ||
    (Nat.ble rs.1 ch.length &&
      pivOk S Q R x0 x1 y0 y1 U0 U1 0 kp XS YS (ch.getD (Nat.sub rs.1 1) dflt))) &&
  (Nat.beq rs.2.1 0 ||
    (Nat.ble rs.2.1 ch.length && Nat.blt 0 rs.2.2 &&
      pivOk S Q R x0 x1 y0 y1 U0 U1 rs.2.2 kp XS YS (ch.getD (Nat.sub rs.2.1 1) dflt)))

/-- The non-swing conditions of an entry (all four when `kp = 4`): `ptOkK` first, the exact
`admK` tests (walls, exact maxima) otherwise. -/
def admAll (Q R x0 x1 y0 y1 U0 U1 kp XS YS : ℕ) : Bool :=
  ptOkK kp Q R U0 U1 x0 x1 y0 y1 XS YS ||
    ((Nat.beq kp 0 || admK Q R x0 x1 y0 y1 U0 U1 XS YS 0) &&
     (Nat.beq kp 1 || admK Q R x0 x1 y0 y1 U0 U1 XS YS 1) &&
     (Nat.beq kp 2 || admK Q R x0 x1 y0 y1 U0 U1 XS YS 2) &&
     (Nat.beq kp 3 || admK Q R x0 x1 y0 y1 U0 U1 XS YS 3))

/-- The tests of one claimed entry. -/
def entOk (S Q R x0 x1 y0 y1 U0 U1 : ℕ) (chA chB : List Piv) (et : Ent × Tag) : Bool :=
  Nat.ble et.2.1 4 &&
  admAll Q R x0 x1 y0 y1 U0 U1 et.2.1 (Nat.mul et.1.1 S) (Nat.mul et.1.2.1 S) &&
  (Nat.beq et.2.1 4 ||
    (rsnOk S Q R x0 x1 y0 y1 U0 U1 chA et.2.1 (Nat.mul et.1.1 S) (Nat.mul et.1.2.1 S) et.2.2.1 &&
     rsnOk S Q R x0 x1 y0 y1 U0 U1 chB et.2.1 (Nat.mul et.1.1 S) (Nat.mul et.1.2.1 S) et.2.2.2))

/-- Consecutive pivots are monotone on the box (Lemma F). -/
def chainOk (S Q R x0 x1 y0 y1 U0 U1 : ℕ) : List Piv → Bool
  | a :: b :: t => pivOk S Q R x0 x1 y0 y1 U0 U1 0 a.2.2 (Nat.mul a.1 S) (Nat.mul a.2.1 S) b &&
      chainOk S Q R x0 x1 y0 y1 U0 U1 (b :: t)
  | _ => true

/-- The emptiness staircase (Lemma H): `emp[r] = (e, l)` with `e > 0` certifies that pivots
`A_{r+1}` and `B_e` are never violated together. -/
def empOk (S Q R x0 x1 y0 y1 U0 U1 : ℕ) (chA chB : List Piv) (emp : List (ℕ × ℕ)) : Bool :=
  (List.range chA.length).all fun r =>
    Nat.beq (emp.getD r (0, 0)).1 0 ||
      (Nat.ble (emp.getD r (0, 0)).1 chB.length && Nat.blt 0 (emp.getD r (0, 0)).2 &&
        pivOk S Q R x0 x1 y0 y1 U0 U1 (emp.getD r (0, 0)).2 (chA.getD r dflt).2.2
          (Nat.mul (chA.getD r dflt).1 S) (Nat.mul (chA.getD r dflt).2.1 S)
          (chB.getD (Nat.sub (emp.getD r (0, 0)).1 1) dflt))

/-- Does a reason apply in region `r` (the first `r` pivots satisfied, the others violated)? -/
def capR (rs : Rsn) (r : ℕ) : Bool := (Nat.blt 0 rs.1 && Nat.ble rs.1 r) || Nat.blt r rs.2.1

/-- Is an entry counted in region `(r, s)`? -/
def capt (t : Tag) (r s : ℕ) : Bool := Nat.beq t.1 4 || capR t.2.1 r || capR t.2.2 s

/-- The weight counted in region `(r, s)`. -/
def regW : List (Ent × Tag) → ℕ → ℕ → ℕ
  | [], _, _ => 0
  | et :: rest, r, s => Nat.add (cond (capt et.2 r s) et.1.2.2 0) (regW rest r s)

/-- `ADM` witnesses count in every region. -/
def isT (et : Ent × Tag) : Bool := Nat.beq et.2.1 4

/-- The weight of the `ADM` witnesses. -/
def tsum : List (Ent × Tag) → ℕ
  | [] => 0
  | et :: rest => Nat.add (cond (isT et) et.1.2.2 0) (tsum rest)

/-- Every region not certified empty reaches weight `W` (the `ADM` weight once, the chain entries
region by region). -/
def regOk (W : ℕ) (cl : List (Ent × Tag)) (ka kb : ℕ) (emp : List (ℕ × ℕ)) : Bool :=
  (List.range (ka + 1)).all fun r => (List.range (kb + 1)).all fun s =>
    (Nat.blt r ka && Nat.blt s (emp.getD r (0, 0)).1) ||
      Nat.ble W (Nat.add (tsum cl) (regW (cl.filter fun et => !isT et) r s))

lemma regW_split (r s : ℕ) : ∀ cl : List (Ent × Tag),
    regW cl r s = tsum cl + regW (cl.filter fun et => !isT et) r s
  | [] => rfl
  | et :: rest => by
    have ih := regW_split r s rest
    by_cases h : isT et = true
    · have hc : capt et.2 r s = true := by
        simp only [isT] at h; simp [capt, h]
      simp [regW, tsum, h, hc, ih]; ring
    · have h' : isT et = false := by simpa using h
      simp [regW, tsum, h', ih]; ring

/-- **The `Z` leaf test.** -/
def zOk (W S Q R x0 x1 y0 y1 U0 U1 : ℕ) (cl : List (Ent × Tag)) (chA chB : List Piv)
    (emp : List (ℕ × ℕ)) : Bool :=
  cl.all (entOk S Q R x0 x1 y0 y1 U0 U1 chA chB) && chainOk S Q R x0 x1 y0 y1 U0 U1 chA &&
    chainOk S Q R x0 x1 y0 y1 U0 U1 chB && empOk S Q R x0 x1 y0 y1 U0 U1 chA chB emp &&
    regOk W cl chA.length chB.length emp

/-- The claimed entries: gaps into the candidate list, each with its tag. -/
def claim : List (ℕ × Tag) → List Ent → List (Ent × Tag)
  | [], _ => []
  | (k, t) :: ks, c =>
    match c.drop k with
    | [] => []
    | e :: rest => (e, t) :: claim ks rest

lemma claim_sub : ∀ (sel : List (ℕ × Tag)) (c : List Ent), ((claim sel c).map Prod.fst).Sublist c
  | [], _ => by simp [claim]
  | (k, t) :: ks, c => by
    simp only [claim]
    split
    · simp
    · rename_i e rest hdrop
      simp only [List.map_cons]
      have h1 : (e :: rest).Sublist c := hdrop ▸ List.drop_sublist k c
      exact ((claim_sub ks rest).cons_cons e).trans h1

lemma regW_eq (r s : ℕ) : ∀ cl : List (Ent × Tag),
    regW cl r s = ((((cl.filter fun et => capt et.2 r s)).map Prod.fst).map fun e => e.2.2).sum
  | [] => rfl
  | et :: rest => by
    simp only [regW, nat_add_eq, List.filter_cons]
    rw [regW_eq r s rest]
    cases capt et.2 r s <;> simp

lemma chainOk_get {S Q R x0 x1 y0 y1 U0 U1 : ℕ} : ∀ {ch : List Piv},
    chainOk S Q R x0 x1 y0 y1 U0 U1 ch = true → ∀ i, i + 1 < ch.length →
      pivOk S Q R x0 x1 y0 y1 U0 U1 0 (ch.getD i dflt).2.2 (Nat.mul (ch.getD i dflt).1 S)
        (Nat.mul (ch.getD i dflt).2.1 S) (ch.getD (i + 1) dflt) = true
  | [], _, i, hi => by simp at hi
  | [_], _, i, hi => by simp at hi
  | a :: b :: t, h, i, hi => by
    simp only [chainOk, Bool.and_eq_true] at h
    rcases i with _ | i
    · simpa using h.1
    · have := chainOk_get h.2 i (by simp at hi ⊢; omega)
      simpa using this

/-- **Lemma F**: a chain monotone on `[1, k]` cuts the line into regions. -/
lemma regions (k : ℕ) (g : ℕ → ℝ) (hmono : ∀ j, 1 ≤ j → j < k → g j ≤ g (j + 1)) :
    ∃ r ≤ k, (∀ j, 1 ≤ j → j ≤ r → g j ≤ 0) ∧ (∀ j, r < j → j ≤ k → 0 < g j) := by
  induction k with
  | zero => exact ⟨0, le_rfl, fun j h1 h2 => by omega, fun j h1 h2 => by omega⟩
  | succ k ih =>
    obtain ⟨r, hrk, h1, h2⟩ := ih (fun j hj1 hj2 => hmono j hj1 (by omega))
    have trans : ∀ i j, 1 ≤ i → i ≤ j → j ≤ k + 1 → g i ≤ g j := by
      intro i j hi hij hj
      induction j with
      | zero => omega
      | succ j ihj =>
        rcases Nat.eq_or_lt_of_le hij with h | h
        · rw [h]
        · exact le_trans (ihj (by omega) (by omega)) (hmono j (by omega) (by omega))
    by_cases hk : g (k + 1) ≤ 0
    · exact ⟨k + 1, le_rfl, fun j hj1 hj2 => le_trans (trans j (k + 1) hj1 hj2 le_rfl) hk,
        fun j hj1 hj2 => by omega⟩
    · refine ⟨r, by omega, h1, fun j hjr hjk => ?_⟩
      rcases Nat.lt_or_ge j (k + 1) with hlt | hge
      · exact h2 j hjr (by omega)
      · have : j = k + 1 := by omega
        rw [this]; exact not_le.mp hk

/-- The pose-level facts a leaf uses. -/
structure Pose (S Q R x0 x1 y0 y1 U0 U1 : ℕ) (c : ℝ × ℝ) (u : ℝ) : Prop where
  hx0 : (x0 : ℝ) / Q ≤ c.1
  hx1 : c.1 ≤ (x1 : ℝ) / Q
  hy0 : (y0 : ℝ) / Q ≤ c.2
  hy1 : c.2 ≤ (y1 : ℝ) / Q
  hu0 : (U0 : ℝ) / R ≤ u
  hu1 : u ≤ (U1 : ℝ) / R
  hwx : wid (2 * Real.arctan u) / 2 ≤ c.1
  hwy : wid (2 * Real.arctan u) / 2 ≤ c.2
  hU01 : U0 ≤ U1
  hU1 : U1 ≤ R

/-- The value of a pivot's violation polynomial at the pose. -/
noncomputable def Gq (S Q : ℕ) (q : Piv) (c : ℝ × ℝ) (u : ℝ) : ℝ :=
  Gv Q q.2.2 (Nat.mul q.1 S) (Nat.mul q.2.1 S) c u

lemma pivOk_sound {S Q R x0 x1 y0 y1 U0 U1 l kp XS YS : ℕ} {q : Piv} {c : ℝ × ℝ} {u : ℝ}
    (hQ : 0 < Q) (hR : 0 < R) (P : Pose S Q R x0 x1 y0 y1 U0 U1 c u)
    (h : pivOk S Q R x0 x1 y0 y1 U0 U1 l kp XS YS q = true) :
    lamA l * Gv Q kp XS YS c u + lamB l * Gq S Q q c u ≤ 0 :=
  pairOk_sound hQ hR P.hU01 P.hU1 h P.hx0 P.hx1 P.hy0 P.hy1 P.hu0 P.hu1

/-- The chain's values at the pose, `g j = G_{q_j}` for `j ≥ 1`. -/
noncomputable def gch (S Q : ℕ) (ch : List Piv) (c : ℝ × ℝ) (u : ℝ) (j : ℕ) : ℝ :=
  Gq S Q (ch.getD (j - 1) dflt) c u

lemma chain_regions {S Q R x0 x1 y0 y1 U0 U1 : ℕ} {ch : List Piv} {c : ℝ × ℝ} {u : ℝ}
    (hQ : 0 < Q) (hR : 0 < R) (P : Pose S Q R x0 x1 y0 y1 U0 U1 c u)
    (h : chainOk S Q R x0 x1 y0 y1 U0 U1 ch = true) :
    ∃ r ≤ ch.length, (∀ j, 1 ≤ j → j ≤ r → gch S Q ch c u j ≤ 0) ∧
      (∀ j, r < j → j ≤ ch.length → 0 < gch S Q ch c u j) := by
  apply regions
  intro j hj1 hj2
  have hp := pivOk_sound hQ hR P (chainOk_get h (j - 1) (by omega))
  have e : j - 1 + 1 = j + 1 - 1 := by omega
  rw [e] at hp
  simp only [lamA_zero, lamB_zero, one_mul, neg_one_mul, Gq] at hp
  simp only [gch, Gq]
  linarith

/-- An entry counted in its region lies in the square. -/
lemma capt_mem {S Q R x0 x1 y0 y1 U0 U1 D : ℕ} {chA chB : List Piv} {c : ℝ × ℝ} {u : ℝ}
    (hQ : 0 < Q) (hR : 0 < R) (hU01 : U0 ≤ U1) (hU1 : U1 ≤ R) (hQD : Q = D * S)
    (hD : 0 < D) (hS : 0 < S) (P : Pose S Q R x0 x1 y0 y1 U0 U1 c u)
    {r s : ℕ} (hA : ∀ j, 1 ≤ j → j ≤ r → gch S Q chA c u j ≤ 0)
    (hA' : ∀ j, r < j → j ≤ chA.length → 0 < gch S Q chA c u j)
    (hB : ∀ j, 1 ≤ j → j ≤ s → gch S Q chB c u j ≤ 0)
    (hB' : ∀ j, s < j → j ≤ chB.length → 0 < gch S Q chB c u j)
    {et : Ent × Tag} (he : entOk S Q R x0 x1 y0 y1 U0 U1 chA chB et = true)
    (hc : capt et.2 r s = true) : ptR D et.1 ∈ sq c (2 * Real.arctan u) 1 := by
  set XS := Nat.mul et.1.1 S
  set YS := Nat.mul et.1.2.1 S
  set kp := et.2.1
  have eX : (et.1.1 : ℝ) / D = (XS : ℝ) / Q := by
    rw [hQD]; simp only [XS, nat_mul_eq]; push_cast
    have : (S : ℝ) ≠ 0 := by exact_mod_cast hS.ne'
    field_simp
  have eY : (et.1.2.1 : ℝ) / D = (YS : ℝ) / Q := by
    rw [hQD]; simp only [YS, nat_mul_eq]; push_cast
    have : (S : ℝ) ≠ 0 := by exact_mod_cast hS.ne'
    field_simp
  simp only [entOk, Bool.and_eq_true, Bool.or_eq_true, Nat.beq_eq, Nat.ble_eq] at he
  obtain ⟨⟨hk4, hall⟩, hrs⟩ := he
  have adm : ∀ k : Fin 4, k.val ≠ kp → Gv Q k.val XS YS c u ≤ 0 := by
    intro k hk
    simp only [admAll, Bool.or_eq_true, Bool.and_eq_true, Nat.beq_eq] at hall
    rcases hall with hf | ⟨⟨⟨h0, h1⟩, h2⟩, h3⟩
    · rw [Gv, kf_val]
      exact ptOkK_sound hQ hR hU01 hU1 hf c u P.hu0 P.hu1 P.hx0 P.hx1 P.hy0 P.hy1 k hk
    · have A := fun (k : ℕ) (hk : admK Q R x0 x1 y0 y1 U0 U1 XS YS k = true) =>
        admK_sound hQ hR hU01 hU1 hk P.hx0 P.hx1 P.hy0 P.hy1 P.hu0 P.hu1 P.hwx P.hwy
      fin_cases k
      · exact A 0 (h0.resolve_left (by simp at hk ⊢; omega))
      · exact A 1 (h1.resolve_left (by simp at hk ⊢; omega))
      · exact A 2 (h2.resolve_left (by simp at hk ⊢; omega))
      · exact A 3 (h3.resolve_left (by simp at hk ⊢; omega))
  -- the swing condition, when `kp < 4`
  have swing : kp ≠ 4 → Gv Q kp XS YS c u ≤ 0 := by
    intro hne
    rcases hrs with h | ⟨hrA, hrB⟩
    · exact absurd h hne
    simp only [capt, capR, Bool.or_eq_true, Bool.and_eq_true, Nat.beq_eq, Nat.blt_eq,
      Nat.ble_eq] at hc
    have rsn : ∀ (ch : List Piv) (rs : Rsn) (t : ℕ),
        (∀ j, 1 ≤ j → j ≤ t → gch S Q ch c u j ≤ 0) →
        (∀ j, t < j → j ≤ ch.length → 0 < gch S Q ch c u j) →
        rsnOk S Q R x0 x1 y0 y1 U0 U1 ch kp XS YS rs = true →
        ((0 < rs.1 ∧ rs.1 ≤ t) ∨ t < rs.2.1) → Gv Q kp XS YS c u ≤ 0 := by
      intro ch rs t hlo hhi hok hcap
      simp only [rsnOk, Bool.and_eq_true, Bool.or_eq_true, Nat.beq_eq, Nat.ble_eq,
        Nat.blt_eq] at hok
      obtain ⟨hd, hu⟩ := hok
      rcases hcap with ⟨hd0, hdt⟩ | hut
      · rcases hd with hd | ⟨hdl, hp⟩
        · omega
        have := pivOk_sound hQ hR P hp
        simp only [lamA_zero, lamB_zero, one_mul, neg_one_mul, Gq, nat_sub_eq] at this
        have hg := hlo rs.1 hd0 hdt
        simp only [gch, Gq] at hg
        linarith
      · rcases hu with hu | ⟨⟨hul, hl⟩, hp⟩
        · omega
        have := pivOk_sound hQ hR P hp
        simp only [Gq, nat_sub_eq] at this
        have hg := hhi rs.2.1 hut hul
        simp only [gch, Gq] at hg
        have ha := lamA_pos rs.2.2
        have hb := lamB_pos hl
        nlinarith
    rcases hc with (h | h) | h
    · exact absurd h hne
    · exact rsn chA _ r hA hA' hrA h
    · exact rsn chB _ s hB hB' hrB h
  rw [ptR, mem_sq_iff_gval]
  intro k
  have hk : gval k ((et.1.1 : ℝ) / D - c.1) ((et.1.2.1 : ℝ) / D - c.2) u
      = Gv Q k.val XS YS c u := by
    rw [Gv, kf_val, eX, eY]
  simp only
  rw [hk]
  by_cases hkp : k.val = kp
  · rw [hkp]
    exact swing (by have := k.isLt; omega)
  · exact adm k hkp

/-- **Soundness of a `Z` leaf.** -/
theorem Z_cov {D S Mq R W : ℕ} {pts : List Ent} (hD : 0 < D) (hS : 0 < S) (hR : 0 < R)
    (hnd : pts.Nodup) {x0 x1 y0 y1 U0 U1 : ℕ} {cl : List (Ent × Tag)} {chA chB : List Piv}
    {emp : List (ℕ × ℕ)} (hcl : (cl.map Prod.fst).Sublist pts) (hU01 : U0 ≤ U1) (hU1 : U1 ≤ R)
    (h : zOk W S (D * S) R x0 x1 y0 y1 U0 U1 cl chA chB emp = true) :
    Cov D S Mq R W pts x0 x1 y0 y1 U0 U1 := by
  classical
  intro cc u hx0 hx1 hy0 hy1 hu0 hu1 hsub
  set Q := D * S with hQdef
  have hQ : 0 < Q := Nat.mul_pos hD hS
  have hQc : ((D : ℝ) * S) = (Q : ℝ) := by rw [hQdef]; push_cast; ring
  rw [hQc] at hx0 hx1 hy0 hy1
  obtain ⟨wx, wy⟩ := adm_lo hsub
  have P : Pose S Q R x0 x1 y0 y1 U0 U1 cc u := ⟨hx0, hx1, hy0, hy1, hu0, hu1, wx, wy, hU01, hU1⟩
  simp only [zOk, Bool.and_eq_true, List.all_eq_true] at h
  obtain ⟨⟨⟨⟨hent, hchA⟩, hchB⟩, hemp⟩, hreg⟩ := h
  simp only [empOk, List.all_eq_true] at hemp
  simp only [regOk, List.all_eq_true] at hreg
  obtain ⟨r, hr, hA, hA'⟩ := chain_regions hQ hR P hchA
  obtain ⟨s, hs, hB, hB'⟩ := chain_regions hQ hR P hchB
  -- the region is not certified empty
  have hne : ¬(r < chA.length ∧ s < (emp.getD r (0, 0)).1) := by
    rintro ⟨hra, hse⟩
    have := hemp r (List.mem_range.mpr hra)
    simp only [Bool.or_eq_true, Bool.and_eq_true, Nat.beq_eq, Nat.ble_eq, Nat.blt_eq] at this
    rcases this with he | ⟨⟨hel, hl⟩, hp⟩
    · omega
    have hp' := pivOk_sound hQ hR P hp
    have ga := hA' (r + 1) (by omega) (by omega)
    have gb := hB' _ hse hel
    simp only [gch, Gq, Nat.add_sub_cancel] at ga gb
    have ha := lamA_pos (emp.getD r (0, 0)).2
    have hb := lamB_pos hl
    simp only [Gq, nat_sub_eq] at hp'
    nlinarith
  have hW := hreg r (List.mem_range.mpr (by omega)) s (List.mem_range.mpr (by omega))
  simp only [Bool.or_eq_true, Bool.and_eq_true, Nat.blt_eq, Nat.ble_eq] at hW
  have hW' : W ≤ regW cl r s := by
    rw [regW_split]; simpa [nat_add_eq] using hW.resolve_left hne
  rw [regW_eq] at hW'
  -- the counted entries are captured
  set L := (cl.filter fun et => capt et.2 r s).map Prod.fst with hL
  have hLs : L.Sublist pts := ((List.filter_sublist).map Prod.fst).trans hcl
  have hT : ∀ e ∈ L, e ∈ {e : Ent | ptR D e ∈ sq cc (2 * Real.arctan u) 1} := by
    intro e he
    rw [hL, List.mem_map] at he
    obtain ⟨et, het, rfl⟩ := he
    rw [List.mem_filter] at het
    exact capt_mem hQ hR hU01 hU1 hQdef hD hS P hA hA' hB hB' (hent et het.1) het.2
  have hsum := le_trans hW' (sum_le_captured hnd hLs _ hT)
  have hsumr : (W : ℝ) ≤ ((∑ e ∈ pts.toFinset.filter
      (· ∈ {e : Ent | ptR D e ∈ sq cc (2 * Real.arctan u) 1}), e.2.2 : ℕ) : ℝ) := by
    exact_mod_cast hsum
  rw [Nat.cast_sum] at hsumr
  simpa using hsumr

/-! ## The tree -/

/-- A zero-margin pose-space tree: `Z` leaves (ADM witnesses and chains), `E` (no admissible
pose), `C us t` (`clip_bin` to `u ≤ us/R`), midpoint splits `X`, `Y`, `U`, pruning `F`, and splits
at an explicit coordinate `XM`, `YM`, `UM` (for a root grid that is not dyadic). -/
inductive ZT
  | Z (cl : List (ℕ × Tag)) (chA chB : List Piv) (emp : List (ℕ × ℕ))
  | E
  | C (us : ℕ) (t : ZT)
  | X (l r : ZT)
  | Y (l r : ZT)
  | U (l r : ZT)
  | F (t : ZT)
  | XM (m : ℕ) (l r : ZT)
  | YM (m : ℕ) (l r : ZT)
  | UM (m : ℕ) (l r : ZT)

/-- The tree check on the box `[x0,x1]×[y0,y1]×[u0,u1]` with candidate list `c`. -/
def check (W S Q R F : ℕ) : ZT → ℕ → ℕ → ℕ → ℕ → ℕ → ℕ → List Ent → Bool
  | .Z cl chA chB emp, x0, x1, y0, y1, u0, u1, c =>
    Nat.ble u1 R && Nat.ble u0 u1 && zOk W S Q R x0 x1 y0 y1 u0 u1 (claim cl c) chA chB emp
  | .E, _, x1, _, y1, u0, u1, _ => Nat.ble u1 R && eOk Q R x1 y1 u0 u1
  | .C us t, x0, x1, y0, y1, u0, u1, c =>
    clipOk Q R x1 y1 u0 u1 us && check W S Q R F t x0 x1 y0 y1 u0 us c
  | .F t, x0, x1, y0, y1, u0, u1, c =>
    check W S Q R F t x0 x1 y0 y1 u0 u1 (near S F x0 x1 y0 y1 c)
  | .X l r, x0, x1, y0, y1, u0, u1, c =>
    check W S Q R F l x0 (Nat.div (Nat.add x0 x1) 2) y0 y1 u0 u1 c &&
    check W S Q R F r (Nat.div (Nat.add x0 x1) 2) x1 y0 y1 u0 u1 c
  | .Y l r, x0, x1, y0, y1, u0, u1, c =>
    check W S Q R F l x0 x1 y0 (Nat.div (Nat.add y0 y1) 2) u0 u1 c &&
    check W S Q R F r x0 x1 (Nat.div (Nat.add y0 y1) 2) y1 u0 u1 c
  | .U l r, x0, x1, y0, y1, u0, u1, c =>
    check W S Q R F l x0 x1 y0 y1 u0 (Nat.div (Nat.add u0 u1) 2) c &&
    check W S Q R F r x0 x1 y0 y1 (Nat.div (Nat.add u0 u1) 2) u1 c
  | .XM m l r, x0, x1, y0, y1, u0, u1, c =>
    check W S Q R F l x0 m y0 y1 u0 u1 c && check W S Q R F r m x1 y0 y1 u0 u1 c
  | .YM m l r, x0, x1, y0, y1, u0, u1, c =>
    check W S Q R F l x0 x1 y0 m u0 u1 c && check W S Q R F r x0 x1 m y1 u0 u1 c
  | .UM m l r, x0, x1, y0, y1, u0, u1, c =>
    check W S Q R F l x0 x1 y0 y1 u0 m c && check W S Q R F r x0 x1 y0 y1 m u1 c

/-- **Soundness of the zero-margin tree check.** -/
theorem sound (D S Mq R W F : ℕ) (pts : List Ent) (hD : 0 < D) (hS : 0 < S) (hR : 0 < R)
    (hnd : pts.Nodup) :
    ∀ (t : ZT) (x0 x1 y0 y1 u0 u1 : ℕ) (c : List Ent), c.Sublist pts →
      check W S (D * S) R F t x0 x1 y0 y1 u0 u1 c = true →
      Cov D S Mq R W pts x0 x1 y0 y1 u0 u1 := by
  intro t
  induction t with
  | Z cl chA chB emp =>
    intro x0 x1 y0 y1 u0 u1 c hc h
    simp only [check, Bool.and_eq_true, Nat.ble_eq] at h
    exact Z_cov hD hS hR hnd ((claim_sub cl c).trans hc) h.1.2 h.1.1 h.2
  | E =>
    intro x0 x1 y0 y1 u0 u1 c hc h
    simp only [check, Bool.and_eq_true, Nat.ble_eq] at h
    exact E_cov hD hS hR h.1 h.2
  | C us t ih =>
    intro x0 x1 y0 y1 u0 u1 c hc h
    simp only [check, Bool.and_eq_true] at h
    exact C_cov hD hS hR h.1 (ih _ _ _ _ _ _ _ hc h.2)
  | F t ih =>
    intro x0 x1 y0 y1 u0 u1 c hc h
    simp only [check] at h
    exact ih _ _ _ _ _ _ _ ((List.filter_sublist).trans hc) h
  | X l r ihl ihr =>
    intro x0 x1 y0 y1 u0 u1 c hc h
    simp only [check, Bool.and_eq_true] at h
    exact Cov.splitX _ (ihl _ _ _ _ _ _ _ hc h.1) (ihr _ _ _ _ _ _ _ hc h.2)
  | Y l r ihl ihr =>
    intro x0 x1 y0 y1 u0 u1 c hc h
    simp only [check, Bool.and_eq_true] at h
    exact Cov.splitY _ (ihl _ _ _ _ _ _ _ hc h.1) (ihr _ _ _ _ _ _ _ hc h.2)
  | U l r ihl ihr =>
    intro x0 x1 y0 y1 u0 u1 c hc h
    simp only [check, Bool.and_eq_true] at h
    exact Cov.splitU _ (ihl _ _ _ _ _ _ _ hc h.1) (ihr _ _ _ _ _ _ _ hc h.2)
  | XM m l r ihl ihr =>
    intro x0 x1 y0 y1 u0 u1 c hc h
    simp only [check, Bool.and_eq_true] at h
    exact Cov.splitX m (ihl _ _ _ _ _ _ _ hc h.1) (ihr _ _ _ _ _ _ _ hc h.2)
  | YM m l r ihl ihr =>
    intro x0 x1 y0 y1 u0 u1 c hc h
    simp only [check, Bool.and_eq_true] at h
    exact Cov.splitY m (ihl _ _ _ _ _ _ _ hc h.1) (ihr _ _ _ _ _ _ _ hc h.2)
  | UM m l r ihl ihr =>
    intro x0 x1 y0 y1 u0 u1 c hc h
    simp only [check, Bool.and_eq_true] at h
    exact Cov.splitU m (ihl _ _ _ _ _ _ _ hc h.1) (ihr _ _ _ _ _ _ _ hc h.2)

/-! ## Compact encoding

A chunk ships as a natural number (the tree structure, base-`B` digits, least significant first:
`0` a `Z` leaf, `1`, `2`, `3` `X`, `Y`, `U` and their subtrees, `4` `F`, `5` `E`, `6` `C` with its
value in two digits, `7`, `8`, `9` `XM`, `YM`, `UM` with the coordinate in two digits) and a list
of natural numbers, one per `Z` leaf, in tree order.  A leaf's
number holds `n`, then `n` entries `8·gap + kp` (followed, when `kp < 4`, by one digit per chain,
`d + 256u + 65536l`), then `ka` and `ka` pivots `X + 16384·kind, Y`, `kb` and its pivots, `ne`
and `ne` digits `e + 256l`.  Small numerals keep the kernel's digit extraction cheap.  The
decoder needs no proof. -/

def decRsn (r : ℕ) : Rsn := (Nat.mod r 256, Nat.mod (Nat.div r 256) 256, Nat.div r 65536)

def decEnt (B n : ℕ) : (ℕ × Tag) × ℕ :=
  cond (Nat.blt (Nat.mod (Nat.mod n B) 8) 4)
    ((Nat.div (Nat.mod n B) 8, Nat.mod (Nat.mod n B) 8, decRsn (Nat.mod (Nat.div n B) B),
      decRsn (Nat.mod (Nat.div (Nat.div n B) B) B)), Nat.div (Nat.div (Nat.div n B) B) B)
    ((Nat.div (Nat.mod n B) 8, Nat.mod (Nat.mod n B) 8, (0, 0, 0), (0, 0, 0)), Nat.div n B)

def decEnts (B : ℕ) : ℕ → ℕ → List (ℕ × Tag) × ℕ
  | 0, n => ([], n)
  | k + 1, n => ((decEnt B n).1 :: (decEnts B k (decEnt B n).2).1, (decEnts B k (decEnt B n).2).2)

def decPivs (B : ℕ) : ℕ → ℕ → List Piv × ℕ
  | 0, n => ([], n)
  | k + 1, n =>
    ((Nat.mod (Nat.mod n B) 16384, Nat.mod (Nat.div n B) B, Nat.div (Nat.mod n B) 16384) ::
      (decPivs B k (Nat.div (Nat.div n B) B)).1,
     (decPivs B k (Nat.div (Nat.div n B) B)).2)

def decEmps (B : ℕ) : ℕ → ℕ → List (ℕ × ℕ) × ℕ
  | 0, n => ([], n)
  | k + 1, n =>
    ((Nat.mod (Nat.mod n B) 256, Nat.div (Nat.mod n B) 256) :: (decEmps B k (Nat.div n B)).1,
     (decEmps B k (Nat.div n B)).2)

def decZ (B n : ℕ) : ZT :=
  .Z (decEnts B (Nat.mod n B) (Nat.div n B)).1
    (decPivs B (Nat.mod (decEnts B (Nat.mod n B) (Nat.div n B)).2 B)
      (Nat.div (decEnts B (Nat.mod n B) (Nat.div n B)).2 B)).1
    (decPivs B (Nat.mod (decPivs B (Nat.mod (decEnts B (Nat.mod n B) (Nat.div n B)).2 B)
      (Nat.div (decEnts B (Nat.mod n B) (Nat.div n B)).2 B)).2 B)
      (Nat.div (decPivs B (Nat.mod (decEnts B (Nat.mod n B) (Nat.div n B)).2 B)
        (Nat.div (decEnts B (Nat.mod n B) (Nat.div n B)).2 B)).2 B)).1
    (decEmps B (Nat.mod (decPivs B (Nat.mod (decPivs B (Nat.mod (decEnts B (Nat.mod n B)
      (Nat.div n B)).2 B) (Nat.div (decEnts B (Nat.mod n B) (Nat.div n B)).2 B)).2 B)
      (Nat.div (decPivs B (Nat.mod (decEnts B (Nat.mod n B) (Nat.div n B)).2 B)
        (Nat.div (decEnts B (Nat.mod n B) (Nat.div n B)).2 B)).2 B)).2 B)
      (Nat.div (decPivs B (Nat.mod (decPivs B (Nat.mod (decEnts B (Nat.mod n B)
        (Nat.div n B)).2 B) (Nat.div (decEnts B (Nat.mod n B) (Nat.div n B)).2 B)).2 B)
        (Nat.div (decPivs B (Nat.mod (decEnts B (Nat.mod n B) (Nat.div n B)).2 B)
          (Nat.div (decEnts B (Nat.mod n B) (Nat.div n B)).2 B)).2 B)).2 B)).1

/-- Decode a tree of depth `≤ fuel` from the structure stream `n` and the leaf list `L`; returns
the tree and what is left of both. -/
def dec (B : ℕ) : ℕ → ℕ → List ℕ → ZT × ℕ × List ℕ
  | 0, n, L => (.E, n, L)
  | f + 1, n, L =>
    match Nat.mod n B with
    | 0 => (decZ B (L.headD 0), Nat.div n B, L.tail)
    | 1 => (.X (dec B f (Nat.div n B) L).1
              (dec B f (dec B f (Nat.div n B) L).2.1 (dec B f (Nat.div n B) L).2.2).1,
            (dec B f (dec B f (Nat.div n B) L).2.1 (dec B f (Nat.div n B) L).2.2).2)
    | 2 => (.Y (dec B f (Nat.div n B) L).1
              (dec B f (dec B f (Nat.div n B) L).2.1 (dec B f (Nat.div n B) L).2.2).1,
            (dec B f (dec B f (Nat.div n B) L).2.1 (dec B f (Nat.div n B) L).2.2).2)
    | 3 => (.U (dec B f (Nat.div n B) L).1
              (dec B f (dec B f (Nat.div n B) L).2.1 (dec B f (Nat.div n B) L).2.2).1,
            (dec B f (dec B f (Nat.div n B) L).2.1 (dec B f (Nat.div n B) L).2.2).2)
    | 4 => (.F (dec B f (Nat.div n B) L).1, (dec B f (Nat.div n B) L).2)
    | 5 => (.E, Nat.div n B, L)
    | 7 => (.XM
              (Nat.add (Nat.mod (Nat.div n B) B) (Nat.mul B (Nat.mod (Nat.div (Nat.div n B) B) B)))
              (dec B f (Nat.div (Nat.div (Nat.div n B) B) B) L).1
              (dec B f (dec B f (Nat.div (Nat.div (Nat.div n B) B) B) L).2.1
                (dec B f (Nat.div (Nat.div (Nat.div n B) B) B) L).2.2).1,
            (dec B f (dec B f (Nat.div (Nat.div (Nat.div n B) B) B) L).2.1
                (dec B f (Nat.div (Nat.div (Nat.div n B) B) B) L).2.2).2)
    | 8 => (.YM
              (Nat.add (Nat.mod (Nat.div n B) B) (Nat.mul B (Nat.mod (Nat.div (Nat.div n B) B) B)))
              (dec B f (Nat.div (Nat.div (Nat.div n B) B) B) L).1
              (dec B f (dec B f (Nat.div (Nat.div (Nat.div n B) B) B) L).2.1
                (dec B f (Nat.div (Nat.div (Nat.div n B) B) B) L).2.2).1,
            (dec B f (dec B f (Nat.div (Nat.div (Nat.div n B) B) B) L).2.1
                (dec B f (Nat.div (Nat.div (Nat.div n B) B) B) L).2.2).2)
    | 9 => (.UM
              (Nat.add (Nat.mod (Nat.div n B) B) (Nat.mul B (Nat.mod (Nat.div (Nat.div n B) B) B)))
              (dec B f (Nat.div (Nat.div (Nat.div n B) B) B) L).1
              (dec B f (dec B f (Nat.div (Nat.div (Nat.div n B) B) B) L).2.1
                (dec B f (Nat.div (Nat.div (Nat.div n B) B) B) L).2.2).1,
            (dec B f (dec B f (Nat.div (Nat.div (Nat.div n B) B) B) L).2.1
                (dec B f (Nat.div (Nat.div (Nat.div n B) B) B) L).2.2).2)
    | _ =>
      (.C (Nat.add (Nat.mod (Nat.div n B) B) (Nat.mul B (Nat.mod (Nat.div (Nat.div n B) B) B)))
        (dec B f (Nat.div (Nat.div (Nat.div n B) B) B) L).1,
       (dec B f (Nat.div (Nat.div (Nat.div n B) B) B) L).2)

end ZMTree

end SquarePacking
