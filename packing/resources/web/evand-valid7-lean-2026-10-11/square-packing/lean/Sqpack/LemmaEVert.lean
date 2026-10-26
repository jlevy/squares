import Sqpack.LemmaEPoly

/-!
# Lemma E: the bound at a vertex, certified in integer arithmetic

At a vertex `v(u) = (X(u)/Δ(u), Y(u)/Δ(u))` of the arrangement, on a sub-bin of `u` where `Δ` has a
certified sign, the kernel bounds `fE(v)` from below and compares with `W`:

* a claimed segment contributes `κ · (up − lo)` for a chosen upper end `up ∈ {B, t_C, t_D}` and lower
  end `lo ∈ {A, t_A, t_B}` (vertical lines: `{B, upX, upY}`, `{A, lowX, lowY}`), after checking
  that `up` is the least of the three and `lo` the largest (`segOk`); or `0` (dropped);
* a Lebesgue rectangle contributes `ρ (1 − ĝ_x − ĝ_y)`, each `ĝ` bounded above by `0` (when `d ≤ 0`
  is checked), by the parabola `d²/(2 s c)` (always), or by `(d − s/2)/c` (when `d ≥ s` is checked);
* the sum minus `W` is checked `≥ 0`.

All quantities are `RF`s (`RatU.lean`); `vertOk_sound` turns an accepted certificate into
`W ≤ fE(v)`.
-/

namespace SquarePacking

namespace LemmaEVert

open BernZ RatU ChordE LemmaE LemmaEPoly ZMTreeM

/-! ## 1.  Sign of `Δ` on a sub-bin -/

/-- `Δ = u^m Δ'` and `σ Δ' > 0` on the closed sub-bin: then `Δ` has sign `σ` on `(b0/R, b1/R]`. -/
def signOk (σ : Bool) (Δ : Poly) (m b0 b1 R : ℕ) : Bool :=
  (Δ.take m).all (· == 0) &&
    checkPos (if σ then Δ.drop m else smul (-1) (Δ.drop m)) ((Δ.drop m).length - 1) b0 b1 R

lemma eval_take_drop (p : Poly) (m : ℕ) (h : (p.take m).all (· == 0) = true) (u : ℝ) :
    eval p u = u ^ m * eval (p.drop m) u := by
  induction m generalizing p with
  | zero => simp
  | succ m ih =>
    cases p with
    | nil => simp
    | cons a q =>
      simp only [List.take_succ_cons, List.all_cons, Bool.and_eq_true, beq_iff_eq] at h
      rw [eval_cons, h.1, List.drop_succ_cons, ih q h.2, pow_succ]
      push_cast; ring

lemma sign_of_signOk {σ : Bool} {Δ : Poly} {m b0 b1 R : ℕ} (h : signOk σ Δ m b0 b1 R = true)
    (hR : 0 < R) {u : ℝ} (hu0 : 0 < u) (hb0 : (b0 : ℝ) / R ≤ u) (hb1 : u ≤ (b1 : ℝ) / R) :
    if σ then 0 < eval Δ u else eval Δ u < 0 := by
  simp only [signOk, Bool.and_eq_true] at h
  obtain ⟨hz, hp⟩ := h
  have hpos := pos_of_checkPos hp hR hb0 hb1
  rw [eval_take_drop Δ m hz u]
  have hum : 0 < u ^ m := pow_pos hu0 m
  cases σ
  · simp only [Bool.false_eq_true, if_false, eval_smul] at hpos ⊢
    push_cast at hpos
    nlinarith
  · simp only [if_true] at hpos ⊢
    exact mul_pos hum hpos

/-! ## 2.  A segment's term -/

/-- The candidate ends of a horizontal segment `(X0, Y, X1, ·, w)` and of a vertical one. -/
def hUps (D : ℕ) (e : SegE) : List SL := [SL.cst e.2.2.1 D, hTC D e.2.1, hTD D e.2.1]
def hLos (D : ℕ) (e : SegE) : List SL := [SL.cst e.1 D, hTA D e.2.1, hTB D e.2.1]
def vUps (D : ℕ) (e : SegE) : List SL := [SL.cst e.2.2.2.1 D, vUXs D e.1, vUYs D e.1]
def vLos (D : ℕ) (e : SegE) : List SL := [SL.cst e.2.1 D, vLXs D e.1, vLYs D e.1]

/-- `RF ≥ 0` on the sub-bin, with a Bernstein degree of at least the numerator's. -/
def ckRF (σ : Bool) (r : RF) (b0 b1 R : ℕ) : Bool := checkRF σ r (r.num.length - 1) b0 b1 R

/-- The value of a segment's choice: `κ · (up − lo)` with `κ = w D / len`. -/
def segVal (Δ X Y : Poly) (w D len : ℕ) (ups los : List SL) (iu il : ℕ) : RF :=
  RF.mul (RF.const (w * D : ℕ) len) (((ups.getD iu (SL.cst 0 1)).sub (los.getD il (SL.cst 0 1))).atV Δ X Y)

/-! ### Soundness of a segment's term -/

/-- The data of a vertex on a sub-bin, as real numbers. -/
structure VCtx (ck : RF → Bool) (Δ X Y : Poly) (σ : Bool) (b0 b1 R : ℕ) (u δ : ℝ) : Prop where
  hR : 0 < R
  hu0 : 0 < u
  hu1 : u < 1
  hb0 : (b0 : ℝ) / R ≤ u
  hb1 : u ≤ (b1 : ℝ) / R
  hΔ : eval Δ u = δ
  hσ : if σ then 0 < δ else δ < 0
  /-- the sign test is sound at this vertex -/
  hck : ∀ r : RF, ck r = true → r.d ≠ 0 → 0 ≤ r.eval δ u

lemma VCtx.ok {ck : RF → Bool} {Δ X Y : Poly} {σ : Bool} {b0 b1 R : ℕ} {u δ : ℝ} (h : VCtx ck Δ X Y σ b0 b1 R u δ) :
    Ok δ u :=
  ⟨h.hu0, h.hu1, by have := h.hσ; split_ifs at this <;> [exact this.ne'; exact this.ne]⟩

/-- The vertex. -/
noncomputable def vtx (X Y : Poly) (δ u : ℝ) : ℝ × ℝ := (eval X u / δ, eval Y u / δ)

lemma ckRF_sound {ck : RF → Bool} {σ : Bool} {r : RF} {b0 b1 R : ℕ} (hc : ck r = true)
    {Δ X Y : Poly} {u δ : ℝ} (h : VCtx ck Δ X Y σ b0 b1 R u δ) (hd : r.d ≠ 0) : 0 ≤ r.eval δ u :=
  h.hck r hc hd

/-- The Bernstein test of the numerator is sound at every vertex of the sub-bin. -/
lemma ckRF_hck {σ : Bool} {b0 b1 R : ℕ} {u δ : ℝ} (hR : 0 < R) (h : Ok δ u)
    (hσ : if σ then 0 < δ else δ < 0) (hb0 : (b0 : ℝ) / R ≤ u) (hb1 : u ≤ (b1 : ℝ) / R) :
    ∀ r : RF, ckRF σ r b0 b1 R = true → r.d ≠ 0 → 0 ≤ r.eval δ u :=
  fun _ hc hd => nonneg_of_checkRF hc hR h hσ hd hb0 hb1

/-- If the chosen element is checked against all others (`U' − U ≥ 0` at the vertex), it is the
least of their values. -/
lemma le_of_all {ck : RF → Bool} {σ : Bool} {Δ X Y : Poly} {b0 b1 R : ℕ} {u δ : ℝ} (h : VCtx ck Δ X Y σ b0 b1 R u δ)
    {Ls : List SL} (hd : ∀ L ∈ Ls, L.d ≠ 0) {U : SL} (hU : U.d ≠ 0)
    (hall : Ls.all (fun U' => ck ((U'.sub U).atV Δ X Y)) = true) :
    ∀ U' ∈ Ls, U.val u (vtx X Y δ u) ≤ U'.val u (vtx X Y δ u) := by
  intro U' hU'
  have hc := (List.all_eq_true.mp hall) U' hU'
  have h0 := ckRF_sound hc h (Nat.mul_ne_zero (hd U' hU') hU)
  rw [eval_atV _ _ _ _ h.hΔ h.ok.hδ, val_sub _ _ (hd U' hU') hU h.hu0 h.hu1] at h0
  simpa [vtx] using h0

lemma ge_of_all {ck : RF → Bool} {σ : Bool} {Δ X Y : Poly} {b0 b1 R : ℕ} {u δ : ℝ} (h : VCtx ck Δ X Y σ b0 b1 R u δ)
    {Ls : List SL} (hd : ∀ L ∈ Ls, L.d ≠ 0) {U : SL} (hU : U.d ≠ 0)
    (hall : Ls.all (fun L => ck ((U.sub L).atV Δ X Y)) = true) :
    ∀ L ∈ Ls, L.val u (vtx X Y δ u) ≤ U.val u (vtx X Y δ u) := by
  intro L hL
  have hc := (List.all_eq_true.mp hall) L hL
  have h0 := ckRF_sound hc h (Nat.mul_ne_zero hU (hd L hL))
  rw [eval_atV _ _ _ _ h.hΔ h.ok.hδ, val_sub _ _ hU (hd L hL) h.hu0 h.hu1] at h0
  simpa [vtx] using h0

lemma getD_mem {α : Type*} {l : List α} {i : ℕ} (d : α) (h : i < l.length) : l.getD i d ∈ l := by
  rw [List.getD_eq_getElem _ _ h]; exact List.getElem_mem h

/-- **A horizontal segment's term** is at least its certified value. -/
theorem hseg_core {ck : RF → Bool} {D : ℕ} (hD : 0 < D) {σ : Bool} {Δ X Y : Poly} {b0 b1 R : ℕ} {u δ : ℝ}
    (h : VCtx ck Δ X Y σ b0 b1 R u δ) {e : SegE} (hx : e.1 < e.2.2.1) {U L : SL}
    (hUm : U ∈ hUps D e) (hLm : L ∈ hLos D e)
    (u1 : ∀ U' ∈ hUps D e, U.val u (vtx X Y δ u) ≤ U'.val u (vtx X Y δ u))
    (l1 : ∀ L' ∈ hLos D e, L'.val u (vtx X Y δ u) ≤ L.val u (vtx X Y δ u)) :
    (RF.mul (RF.const (e.2.2.2.2 * D : ℕ) (e.2.2.1 - e.1)) ((U.sub L).atV Δ X Y)).eval δ u ≤
      (hsegT (2 * Real.arctan u) D e).1 *
        max 0 (clampMin (hsegT (2 * Real.arctan u) D e).2.1 (hsegT (2 * Real.arctan u) D e).2.2
          (vtx X Y δ u)) := by
  have hD2 : 2 * D ≠ 0 := by omega
  have hdU : ∀ L ∈ hUps D e, L.d ≠ 0 := by
    intro L hL; simp only [hUps, List.mem_cons, List.not_mem_nil, or_false] at hL
    rcases hL with rfl | rfl | rfl <;> simp [SL.cst, hTC, hTD] <;> omega
  have hdL : ∀ L ∈ hLos D e, L.d ≠ 0 := by
    intro L hL; simp only [hLos, List.mem_cons, List.not_mem_nil, or_false] at hL
    rcases hL with rfl | rfl | rfl <;> simp [SL.cst, hTA, hTB] <;> omega
  set v := vtx X Y δ u
  set θ := 2 * Real.arctan u
  set η := (e.2.1 : ℝ) / D
  set A := (e.1 : ℝ) / D
  set B := (e.2.2.1 : ℝ) / D
  -- the values of the candidates
  have vB : (SL.cst e.2.2.1 D).val u v = B := by rw [val_cst]; push_cast; rfl
  have vA : (SL.cst e.1 D).val u v = A := by rw [val_cst]; push_cast; rfl
  have vC := val_hTC hD h.hu0 h.hu1 e.2.1 v
  have vDd := val_hTD hD h.hu0 h.hu1 e.2.1 v
  have vA' := val_hTA hD h.hu0 h.hu1 e.2.1 v
  have vB' := val_hTB hD h.hu0 h.hu1 e.2.1 v
  have hmin : U.val u v ≤ min B (min (aff (chC θ η) v) (aff (chD θ η) v)) := by
    refine le_min ?_ (le_min ?_ ?_)
    · have := u1 (SL.cst e.2.2.1 D) (by simp [hUps]); rwa [vB] at this
    · have := u1 (hTC D e.2.1) (by simp [hUps]); rwa [vC] at this
    · have := u1 (hTD D e.2.1) (by simp [hUps]); rwa [vDd] at this
  have hmax : max A (max (aff (chA θ η) v) (aff (chB θ η) v)) ≤ L.val u v := by
    refine max_le ?_ (max_le ?_ ?_)
    · have := l1 (SL.cst e.1 D) (by simp [hLos]); rwa [vA] at this
    · have := l1 (hTA D e.2.1) (by simp [hLos]); rwa [vA'] at this
    · have := l1 (hTB D e.2.1) (by simp [hLos]); rwa [vB'] at this
  have hcl := min_sub_max_formsOf A B (chA θ η) (chB θ η) (chC θ η) (chD θ η) v
  have hAB : A < B := by
    have hDr : (0 : ℝ) < D := by exact_mod_cast hD
    exact div_lt_div_of_pos_right (by exact_mod_cast hx) hDr
  have hval : (RF.mul (RF.const (e.2.2.2.2 * D : ℕ) (e.2.2.1 - e.1)) ((U.sub L).atV Δ X Y)).eval δ u =
      (e.2.2.2.2 : ℝ) / (B - A) * (U.val u v - L.val u v) := by
    have hlen : (e.2.2.1 - e.1 : ℕ) ≠ 0 := by omega
    rw [eval_mul h.ok (by simp [RF.const]; omega) (Nat.mul_ne_zero (hdU U hUm) (hdL L hLm)),
      eval_const, eval_atV _ _ _ _ h.hΔ h.ok.hδ, val_sub _ _ (hdU U hUm) (hdL L hLm) h.hu0 h.hu1]
    have hDr : (D : ℝ) ≠ 0 := by positivity
    have hsub : ((e.2.2.1 - e.1 : ℕ) : ℝ) = (e.2.2.1 : ℝ) - e.1 := Nat.cast_sub hx.le
    simp only [B, A, hsub]
    push_cast
    have : (e.2.2.1 : ℝ) - e.1 ≠ 0 := by
      have : (e.1 : ℝ) < e.2.2.1 := by exact_mod_cast hx
      linarith
    field_simp
    rfl
  rw [hval]
  simp only [hsegT]
  refine mul_le_mul_of_nonneg_left ?_ (div_nonneg (Nat.cast_nonneg _) (by linarith))
  rw [← hcl]
  exact le_trans (by linarith) (le_max_right _ _)

/-- **A vertical segment's term** is at least its certified value. -/
theorem vseg_core {ck : RF → Bool} {D : ℕ} (hD : 0 < D) {σ : Bool} {Δ X Y : Poly} {b0 b1 R : ℕ} {u δ : ℝ}
    (h : VCtx ck Δ X Y σ b0 b1 R u δ) {e : SegE} (hx : e.2.1 < e.2.2.2.1) {U L : SL}
    (hUm : U ∈ vUps D e) (hLm : L ∈ vLos D e)
    (u1 : ∀ U' ∈ vUps D e, U.val u (vtx X Y δ u) ≤ U'.val u (vtx X Y δ u))
    (l1 : ∀ L' ∈ vLos D e, L'.val u (vtx X Y δ u) ≤ L.val u (vtx X Y δ u)) :
    (RF.mul (RF.const (e.2.2.2.2 * D : ℕ) (e.2.2.2.1 - e.2.1)) ((U.sub L).atV Δ X Y)).eval δ u ≤
      (vsegT (2 * Real.arctan u) D e).1 *
        max 0 (clampMin (vsegT (2 * Real.arctan u) D e).2.1 (vsegT (2 * Real.arctan u) D e).2.2
          (vtx X Y δ u)) := by
  have hD2 : 2 * D ≠ 0 := by omega
  have hdU : ∀ L ∈ vUps D e, L.d ≠ 0 := by
    intro L hL; simp only [vUps, List.mem_cons, List.not_mem_nil, or_false] at hL
    rcases hL with rfl | rfl | rfl <;> simp [SL.cst, vUXs, vUYs] <;> omega
  have hdL : ∀ L ∈ vLos D e, L.d ≠ 0 := by
    intro L hL; simp only [vLos, List.mem_cons, List.not_mem_nil, or_false] at hL
    rcases hL with rfl | rfl | rfl <;> simp [SL.cst, vLXs, vLYs] <;> omega
  set v := vtx X Y δ u
  set θ := 2 * Real.arctan u
  set ξ := (e.1 : ℝ) / D
  set A := (e.2.1 : ℝ) / D
  set B := (e.2.2.2.1 : ℝ) / D
  -- the values of the candidates
  have vB : (SL.cst e.2.2.2.1 D).val u v = B := by rw [val_cst]; push_cast; rfl
  have vA : (SL.cst e.2.1 D).val u v = A := by rw [val_cst]; push_cast; rfl
  have vC := val_vUX hD h.hu0 h.hu1 e.1 v
  have vDd := val_vUY hD h.hu0 h.hu1 e.1 v
  have vA' := val_vLX hD h.hu0 h.hu1 e.1 v
  have vB' := val_vLY hD h.hu0 h.hu1 e.1 v
  have hmin : U.val u v ≤ min B (min (aff (vUX θ ξ) v) (aff (vUY θ ξ) v)) := by
    refine le_min ?_ (le_min ?_ ?_)
    · have := u1 (SL.cst e.2.2.2.1 D) (by simp [vUps]); rwa [vB] at this
    · have := u1 (vUXs D e.1) (by simp [vUps]); rwa [vC] at this
    · have := u1 (vUYs D e.1) (by simp [vUps]); rwa [vDd] at this
  have hmax : max A (max (aff (vLX θ ξ) v) (aff (vLY θ ξ) v)) ≤ L.val u v := by
    refine max_le ?_ (max_le ?_ ?_)
    · have := l1 (SL.cst e.2.1 D) (by simp [vLos]); rwa [vA] at this
    · have := l1 (vLXs D e.1) (by simp [vLos]); rwa [vA'] at this
    · have := l1 (vLYs D e.1) (by simp [vLos]); rwa [vB'] at this
  have hcl := min_sub_max_formsOf A B (vLX θ ξ) (vLY θ ξ) (vUX θ ξ) (vUY θ ξ) v
  have hAB : A < B := by
    have hDr : (0 : ℝ) < D := by exact_mod_cast hD
    exact div_lt_div_of_pos_right (by exact_mod_cast hx) hDr
  have hval : (RF.mul (RF.const (e.2.2.2.2 * D : ℕ) (e.2.2.2.1 - e.2.1)) ((U.sub L).atV Δ X Y)).eval δ u =
      (e.2.2.2.2 : ℝ) / (B - A) * (U.val u v - L.val u v) := by
    have hlen : (e.2.2.2.1 - e.2.1 : ℕ) ≠ 0 := by omega
    rw [eval_mul h.ok (by simp [RF.const]; omega) (Nat.mul_ne_zero (hdU U hUm) (hdL L hLm)),
      eval_const, eval_atV _ _ _ _ h.hΔ h.ok.hδ, val_sub _ _ (hdU U hUm) (hdL L hLm) h.hu0 h.hu1]
    have hDr : (D : ℝ) ≠ 0 := by positivity
    have hsub : ((e.2.2.2.1 - e.2.1 : ℕ) : ℝ) = (e.2.2.2.1 : ℝ) - e.2.1 := Nat.cast_sub hx.le
    simp only [B, A, hsub]
    push_cast
    have : (e.2.2.2.1 : ℝ) - e.2.1 ≠ 0 := by
      have : (e.2.1 : ℝ) < e.2.2.2.1 := by exact_mod_cast hx
      linarith
    field_simp
    rfl
  rw [hval]
  simp only [vsegT]
  refine mul_le_mul_of_nonneg_left ?_ (div_nonneg (Nat.cast_nonneg _) (by linarith))
  rw [← hcl]
  exact le_trans (by linarith) (le_max_right _ _)

/-! ## 3.  A Lebesgue term -/

/-- `sin θ / h = 2u/((1+u²) h)` as a scaled line. -/
def sSL (h : ℕ) : SL := ⟨([0], [0], Sp), 0, 0, 1, h⟩

lemma val_sSL {h : ℕ} (hh : h ≠ 0) (u : ℝ) (c : ℝ × ℝ) :
    (sSL h).val u c = 2 * u / (1 + u ^ 2) / h := by
  have hN : (1 : ℝ) + u ^ 2 ≠ 0 := by positivity
  have hh' : (h : ℝ) ≠ 0 := by exact_mod_cast hh
  simp only [SL.val, sden, sSL, aff, evalPL, eval_Sp, eval_cons, eval_nil]
  push_cast
  field_simp
  ring

/-- `cos θ / h`. -/
def cSL (h : ℕ) : SL := ⟨([0], [0], Cp), 0, 0, 1, h⟩

lemma val_cSL {h : ℕ} (hh : h ≠ 0) (u : ℝ) (c : ℝ × ℝ) :
    (cSL h).val u c = (1 - u ^ 2) / (1 + u ^ 2) / h := by
  simp only [SL.val, sden, cSL, aff, evalPL, eval_Cp, eval_cons, eval_nil]
  simp [div_div]

/-- The test of a cap mode: `0`: `d ≤ 0`; `1`: none (parabola); `2`: `d ≥ s`. -/
def ghOk (ck : RF → Bool) (σ : Bool) (Δ X Y : Poly) (b0 b1 R : ℕ) (cap : SL) (mode : ℕ) : Bool :=
  if mode = 0 then ck (((SL.cst 0 1).sub cap).atV Δ X Y)
  else if mode = 1 then true
  else ck ((cap.sub (sSL 1)).atV Δ X Y)

/-- The upper bound of `ĝ(d)` of a cap mode: `0`, `d² N²/(2 S C)`, `(d − s/2) N / C`. -/
def ghU (Δ X Y : Poly) (cap : SL) (mode : ℕ) : RF :=
  if mode = 0 then RF.const 0 1
  else if mode = 1 then RF.mul (RF.mul (cap.atV Δ X Y) (cap.atV Δ X Y)) ⟨BernZ.mul Np Np, 0, 1, 1, 0, 2⟩
  else RF.mul ((cap.sub (sSL 2)).atV Δ X Y) ⟨Np, 0, 1, 0, 0, 1⟩

lemma ghU_d (Δ X Y : Poly) (cap : SL) (hc : cap.d ≠ 0) (mode : ℕ) : (ghU Δ X Y cap mode).d ≠ 0 := by
  unfold ghU; split_ifs <;> simp [RF.const, RF.mul, SL.atV, SL.sub, sSL] <;> omega

lemma ghat_le_par {s co d : ℝ} (hs : 0 < s) (hc : 0 < co) : SqArea.ghat s co d ≤ d ^ 2 / (2 * s * co) := by
  unfold SqArea.ghat
  split_ifs with h1 h2
  · positivity
  · exact le_rfl
  · rw [div_le_div_iff₀ hc (by positivity)]
    nlinarith [sq_nonneg (d - s)]

lemma ghU_sound {ck : RF → Bool} {σ : Bool} {Δ X Y : Poly} {b0 b1 R : ℕ} {u δ : ℝ} (h : VCtx ck Δ X Y σ b0 b1 R u δ)
    {cap : SL} (hcap : cap.d ≠ 0) {mode : ℕ} (hok : ghOk ck σ Δ X Y b0 b1 R cap mode = true) :
    SqArea.ghat (Real.sin (2 * Real.arctan u)) (Real.cos (2 * Real.arctan u))
        (cap.val u (vtx X Y δ u)) ≤ (ghU Δ X Y cap mode).eval δ u := by
  have hN : (0 : ℝ) < 1 + u ^ 2 := by positivity
  have hC : (0 : ℝ) < 1 - u ^ 2 := by nlinarith [h.hu0, h.hu1]
  have hu := h.hu0
  rw [(trig u).1, (trig u).2]
  have hs : (0 : ℝ) < 2 * u / (1 + u ^ 2) := by positivity
  have hc : (0 : ℝ) < (1 - u ^ 2) / (1 + u ^ 2) := by positivity
  set d := cap.val u (vtx X Y δ u)
  have hd : (cap.atV Δ X Y).eval δ u = d := eval_atV _ _ _ _ h.hΔ h.ok.hδ
  unfold ghOk at hok; unfold ghU
  split_ifs at hok ⊢ with h0 h1
  · have hd0 : d ≤ 0 := by
      have := ckRF_sound hok h (by simpa [SL.atV, SL.sub, SL.cst] using hcap)
      rw [eval_atV _ _ _ _ h.hΔ h.ok.hδ, val_sub _ _ (by simp [SL.cst]) hcap h.hu0 h.hu1,
        val_cst] at this
      simp only [Int.cast_zero, Nat.cast_one, zero_div, zero_sub] at this
      have h' : 0 ≤ -d := this
      linarith
    rw [eval_const]
    simp only [SqArea.ghat, if_pos hd0, Int.cast_zero, Nat.cast_one, zero_div, le_refl]
  · refine le_trans (ghat_le_par hs hc) (le_of_eq ?_)
    rw [eval_mul h.ok (by simpa [RF.mul, SL.atV] using Nat.mul_ne_zero hcap hcap) (by norm_num),
      eval_mul h.ok (by simpa [SL.atV] using hcap) (by simpa [SL.atV] using hcap), hd]
    simp only [RF.eval, den, BernZ.eval_mul, eval_Np]
    push_cast
    field_simp
  · have hds : 2 * u / (1 + u ^ 2) ≤ d := by
      have := ckRF_sound hok h (by simpa [SL.atV, SL.sub, sSL] using hcap)
      rw [eval_atV _ _ _ _ h.hΔ h.ok.hδ, val_sub _ _ hcap (by simp [sSL]) h.hu0 h.hu1,
        val_sSL (by norm_num)] at this
      simp only [Nat.cast_one, div_one] at this
      have h' : 0 ≤ d - 2 * u / (1 + u ^ 2) := this
      linarith
    rw [eval_mul h.ok (by simpa [SL.atV, SL.sub, sSL] using hcap) (by norm_num),
      eval_atV _ _ _ _ h.hΔ h.ok.hδ, val_sub _ _ hcap (by simp [sSL]) h.hu0 h.hu1,
      val_sSL (by norm_num), show cap.val u (eval X u / δ, eval Y u / δ) = d from rfl]
    have key : SqArea.ghat (2 * u / (1 + u ^ 2)) ((1 - u ^ 2) / (1 + u ^ 2)) d =
        (d - 2 * u / (1 + u ^ 2) / 2) / ((1 - u ^ 2) / (1 + u ^ 2)) := by
      unfold SqArea.ghat
      rw [if_neg (by linarith)]
      split_ifs with h3
      · have : d = 2 * u / (1 + u ^ 2) := le_antisymm h3 hds
        rw [this]; field_simp; ring
      · ring
    rw [key]
    apply le_of_eq
    simp only [RF.eval, den, eval_Np]
    push_cast
    field_simp

/-! ### Pointwise bounds of `ĝ` -/

lemma ghat_le_parU {ck : RF → Bool} {σ : Bool} {Δ X Y : Poly} {b0 b1 R : ℕ} {u δ : ℝ} (h : VCtx ck Δ X Y σ b0 b1 R u δ)
    {cap : SL} (hcap : cap.d ≠ 0) :
    SqArea.ghat (Real.sin (2 * Real.arctan u)) (Real.cos (2 * Real.arctan u))
        (cap.val u (vtx X Y δ u)) ≤ (ghU Δ X Y cap 1).eval δ u := by
  have ok : ghOk ck σ Δ X Y b0 b1 R cap 1 = true := by simp [ghOk]
  exact ghU_sound h hcap ok

lemma ghat_le_linU {ck : RF → Bool} {σ : Bool} {Δ X Y : Poly} {b0 b1 R : ℕ} {u δ : ℝ} (h : VCtx ck Δ X Y σ b0 b1 R u δ)
    {cap : SL} (hcap : cap.d ≠ 0) (hds : 2 * u / (1 + u ^ 2) ≤ cap.val u (vtx X Y δ u)) :
    SqArea.ghat (Real.sin (2 * Real.arctan u)) (Real.cos (2 * Real.arctan u))
        (cap.val u (vtx X Y δ u)) ≤ (ghU Δ X Y cap 2).eval δ u := by
  have hN : (0 : ℝ) < 1 + u ^ 2 := by positivity
  have hC : (0 : ℝ) < 1 - u ^ 2 := by nlinarith [h.hu0, h.hu1]
  have hu := h.hu0
  rw [(trig u).1, (trig u).2]
  set d := cap.val u (vtx X Y δ u)
  simp only [ghU, show (2 : ℕ) ≠ 0 by norm_num, show (2 : ℕ) ≠ 1 by norm_num, if_false]
  rw [eval_mul h.ok (by simpa [SL.atV, SL.sub, sSL] using hcap) (by norm_num),
    eval_atV _ _ _ _ h.hΔ h.ok.hδ, val_sub _ _ hcap (by simp [sSL]) h.hu0 h.hu1,
    val_sSL (by norm_num), show cap.val u (eval X u / δ, eval Y u / δ) = d from rfl]
  have key : SqArea.ghat (2 * u / (1 + u ^ 2)) ((1 - u ^ 2) / (1 + u ^ 2)) d =
      (d - 2 * u / (1 + u ^ 2) / 2) / ((1 - u ^ 2) / (1 + u ^ 2)) := by
    unfold SqArea.ghat
    rw [if_neg (by have : (0 : ℝ) < 2 * u / (1 + u ^ 2) := by positivity
                   linarith)]
    split_ifs with h3
    · have : d = 2 * u / (1 + u ^ 2) := le_antisymm h3 hds
      rw [this]; field_simp; ring
    · ring
  rw [key]
  apply le_of_eq
  simp only [RF.eval, den, eval_Np]
  push_cast
  field_simp

lemma ghat_zero_of {s co d : ℝ} (hd : d ≤ 0) : SqArea.ghat s co d = 0 := by
  simp [SqArea.ghat, hd]

/-! ### Cap bounds with alternatives -/

/-- A cap's bound: `0` (checked `d ≤ 0`), the parabola, the line (checked `d ≥ s`), or a split at
`d = 0` (`zp`) or at `d = s` (`pl`) whose two branches carry S-procedure terms with multipliers
`n/d ≥ 0`: whichever side of the split `u` is on, that branch bounds `ĝ`. -/
inductive CapM where
  | zero
  | par
  | lin
  | zp (n0 d0 n1 d1 : ℕ)
  | pl (n0 d0 n1 d1 : ℕ)

def capOk (ck : RF → Bool) (σ : Bool) (Δ X Y : Poly) (b0 b1 R : ℕ) (cap : SL) : CapM → Bool
  | .zero => ghOk ck σ Δ X Y b0 b1 R cap 0
  | .par => true
  | .lin => ghOk ck σ Δ X Y b0 b1 R cap 2
  | .zp _ d0 _ d1 => d0 != 0 && d1 != 0
  | .pl _ d0 _ d1 => d0 != 0 && d1 != 0

def capAlts (Δ X Y : Poly) (cap : SL) : CapM → List RF
  | .zero => [ghU Δ X Y cap 0]
  | .par => [ghU Δ X Y cap 1]
  | .lin => [ghU Δ X Y cap 2]
  | .zp n0 d0 n1 d1 => [RF.neg (RF.mul (RF.const n0 d0) (cap.atV Δ X Y)),
      RF.add Δ (ghU Δ X Y cap 1) (RF.mul (RF.const n1 d1) (cap.atV Δ X Y))]
  | .pl n0 d0 n1 d1 => [RF.add Δ (ghU Δ X Y cap 1) (RF.mul (RF.const n0 d0) (((sSL 1).sub cap).atV Δ X Y)),
      RF.add Δ (ghU Δ X Y cap 2) (RF.mul (RF.const n1 d1) ((cap.sub (sSL 1)).atV Δ X Y))]

lemma capAlts_d {ck : RF → Bool} (Δ X Y : Poly) {cap : SL} (hcap : cap.d ≠ 0) {m : CapM} (σ : Bool) (b0 b1 R : ℕ)
    (hok : capOk ck σ Δ X Y b0 b1 R cap m = true) : ∀ r ∈ capAlts Δ X Y cap m, r.d ≠ 0 := by
  have g0 := ghU_d Δ X Y cap hcap 0
  have g1 := ghU_d Δ X Y cap hcap 1
  have g2 := ghU_d Δ X Y cap hcap 2
  intro r hr
  cases m with
  | zero => simp [capAlts] at hr; subst hr; exact g0
  | par => simp [capAlts] at hr; subst hr; exact g1
  | lin => simp [capAlts] at hr; subst hr; exact g2
  | zp n0 d0 n1 d1 =>
    simp only [capOk, Bool.and_eq_true, bne_iff_ne, ne_eq] at hok
    simp only [capAlts, List.mem_cons, List.not_mem_nil, or_false] at hr
    rcases hr with rfl | rfl
    · simp [RF.neg, RF.mul, RF.const, SL.atV, hok.1, hcap]
    · exact RF.add_d _ g1 (by simp [RF.mul, RF.const, SL.atV, hok.2, hcap])
  | pl n0 d0 n1 d1 =>
    simp only [capOk, Bool.and_eq_true, bne_iff_ne, ne_eq] at hok
    simp only [capAlts, List.mem_cons, List.not_mem_nil, or_false] at hr
    rcases hr with rfl | rfl
    · exact RF.add_d _ g1 (by simp [RF.mul, RF.const, SL.atV, SL.sub, sSL, hok.1, hcap])
    · exact RF.add_d _ g2 (by simp [RF.mul, RF.const, SL.atV, SL.sub, sSL, hok.2, hcap])

/-- **A cap**: some alternative bounds `ĝ(d)` from above at `u`. -/
theorem capAlts_sound {ck : RF → Bool} {σ : Bool} {Δ X Y : Poly} {b0 b1 R : ℕ} {u δ : ℝ}
    (h : VCtx ck Δ X Y σ b0 b1 R u δ) {cap : SL} (hcap : cap.d ≠ 0) {m : CapM}
    (hok : capOk ck σ Δ X Y b0 b1 R cap m = true) :
    ∃ t ∈ capAlts Δ X Y cap m, SqArea.ghat (Real.sin (2 * Real.arctan u))
      (Real.cos (2 * Real.arctan u)) (cap.val u (vtx X Y δ u)) ≤ t.eval δ u := by
  set d := cap.val u (vtx X Y δ u)
  have hd : (cap.atV Δ X Y).eval δ u = d := eval_atV _ _ _ _ h.hΔ h.ok.hδ
  have hdc := capAlts_d Δ X Y hcap σ b0 b1 R hok
  have hpar := ghat_le_parU h hcap (Δ := Δ)
  cases m with
  | zero => exact ⟨_, List.mem_singleton_self _, ghU_sound h hcap hok⟩
  | par => exact ⟨_, List.mem_singleton_self _, hpar⟩
  | lin => exact ⟨_, List.mem_singleton_self _, ghU_sound h hcap hok⟩
  | zp n0 d0 n1 d1 =>
    simp only [capOk, Bool.and_eq_true, bne_iff_ne, ne_eq] at hok
    have hl0 : (0 : ℝ) ≤ (n0 : ℝ) / d0 := by positivity
    have hl1 : (0 : ℝ) ≤ (n1 : ℝ) / d1 := by positivity
    rcases le_total d 0 with hd0 | hd0
    · refine ⟨RF.neg (RF.mul (RF.const n0 d0) (cap.atV Δ X Y)), by simp [capAlts], ?_⟩
      rw [ghat_zero_of hd0, eval_neg, eval_mul h.ok (by simp [RF.const, hok.1])
        (by simpa [SL.atV] using hcap), eval_const, hd]
      push_cast
      nlinarith
    · refine ⟨RF.add Δ (ghU Δ X Y cap 1) (RF.mul (RF.const n1 d1) (cap.atV Δ X Y)),
        by simp [capAlts], ?_⟩
      rw [eval_add h.ok h.hΔ (ghU_d Δ X Y cap hcap 1) (by simp [RF.mul, RF.const, SL.atV, hok.2, hcap]),
        eval_mul h.ok (by simp [RF.const, hok.2]) (by simpa [SL.atV] using hcap), eval_const, hd]
      push_cast
      nlinarith
  | pl n0 d0 n1 d1 =>
    simp only [capOk, Bool.and_eq_true, bne_iff_ne, ne_eq] at hok
    have hl0 : (0 : ℝ) ≤ (n0 : ℝ) / d0 := by positivity
    have hl1 : (0 : ℝ) ≤ (n1 : ℝ) / d1 := by positivity
    have hsd : (((sSL 1).sub cap).atV Δ X Y).eval δ u = 2 * u / (1 + u ^ 2) - d := by
      rw [eval_atV _ _ _ _ h.hΔ h.ok.hδ, val_sub _ _ (by simp [sSL]) hcap h.hu0 h.hu1,
        val_sSL (by norm_num)]
      simp [d, vtx]
    have hds' : ((cap.sub (sSL 1)).atV Δ X Y).eval δ u = d - 2 * u / (1 + u ^ 2) := by
      rw [eval_atV _ _ _ _ h.hΔ h.ok.hδ, val_sub _ _ hcap (by simp [sSL]) h.hu0 h.hu1,
        val_sSL (by norm_num)]
      simp [d, vtx]
    rcases le_total d (2 * u / (1 + u ^ 2)) with hds | hds
    · refine ⟨RF.add Δ (ghU Δ X Y cap 1) (RF.mul (RF.const n0 d0) (((sSL 1).sub cap).atV Δ X Y)),
        by simp [capAlts], ?_⟩
      rw [eval_add h.ok h.hΔ (ghU_d Δ X Y cap hcap 1)
          (by simp [RF.mul, RF.const, SL.atV, SL.sub, sSL, hok.1, hcap]),
        eval_mul h.ok (by simp [RF.const, hok.1]) (by simp [SL.atV, SL.sub, sSL, hcap]), eval_const,
        hsd]
      push_cast
      nlinarith
    · refine ⟨RF.add Δ (ghU Δ X Y cap 2) (RF.mul (RF.const n1 d1) ((cap.sub (sSL 1)).atV Δ X Y)),
        by simp [capAlts], ?_⟩
      have hlin := ghat_le_linU h hcap hds (Δ := Δ)
      rw [eval_add h.ok h.hΔ (ghU_d Δ X Y cap hcap 2)
          (by simp [RF.mul, RF.const, SL.atV, SL.sub, sSL, hok.2, hcap]),
        eval_mul h.ok (by simp [RF.const, hok.2]) (by simp [SL.atV, SL.sub, sSL, hcap]), eval_const,
        hds']
      push_cast
      nlinarith

/-! ## 4.  The whole bound at a vertex -/

def sumRF (Δ : Poly) : List RF → RF
  | [] => RF.const 0 1
  | r :: rs => RF.add Δ r (sumRF Δ rs)

lemma sumRF_d (Δ : Poly) : ∀ rs : List RF, (∀ r ∈ rs, r.d ≠ 0) → (sumRF Δ rs).d ≠ 0
  | [], _ => by simp [sumRF, RF.const]
  | r :: rs, h => by
    simp only [sumRF]
    exact RF.add_d Δ (h r List.mem_cons_self)
      (sumRF_d Δ rs fun x hx => h x (List.mem_cons_of_mem _ hx))

lemma eval_sumRF {Δ : Poly} {δ u : ℝ} (h : Ok δ u) (hΔ : eval Δ u = δ) :
    ∀ rs : List RF, (∀ r ∈ rs, r.d ≠ 0) → (sumRF Δ rs).eval δ u = (rs.map (·.eval δ u)).sum
  | [], _ => by simp [sumRF, eval_const]
  | r :: rs, hd => by
    have h1 := hd r List.mem_cons_self
    have h2 : ∀ x ∈ rs, x.d ≠ 0 := fun x hx => hd x (List.mem_cons_of_mem _ hx)
    simp only [sumRF, List.map_cons, List.sum_cons]
    rw [eval_add h hΔ h1 (sumRF_d Δ rs h2), eval_sumRF h hΔ rs h2]

/-! ### Alternatives -/

/-- The test of a segment's alternatives `Ua`, `La` (indices into the candidate upper and lower
ends): every candidate upper end is `≥` one in `Ua`, every lower end `≤` one in `La`. -/
def segOkA (ck : RF → Bool) (σ : Bool) (Δ X Y : Poly) (b0 b1 R : ℕ) (ups los : List SL) (Ua La : List ℕ) : Bool :=
  !Ua.isEmpty && !La.isEmpty && Ua.all (· < ups.length) && La.all (· < los.length) &&
    ups.all (fun U => Ua.any fun a => ck ((U.sub (ups.getD a (SL.cst 0 1))).atV Δ X Y)) &&
    los.all (fun L => La.any fun b => ck (((los.getD b (SL.cst 0 1)).sub L).atV Δ X Y))

/-- The values of a segment's alternatives `κ (up_a − lo_b)`. -/
def segAlts (Δ X Y : Poly) (w D len : ℕ) (ups los : List SL) (Ua La : List ℕ) : List RF :=
  Ua.flatMap fun a => La.map fun b => segVal Δ X Y w D len ups los a b

/-- Pointwise dominance: every candidate upper end is `≥` an alternative, every lower end `≤` one. -/
def DomU (u : ℝ) (v : ℝ × ℝ) (ups : List SL) (Ua : List ℕ) : Prop :=
  ∀ U ∈ ups, ∃ a ∈ Ua, (ups.getD a (SL.cst 0 1)).val u v ≤ U.val u v
def DomL (u : ℝ) (v : ℝ × ℝ) (los : List SL) (La : List ℕ) : Prop :=
  ∀ L ∈ los, ∃ b ∈ La, L.val u v ≤ (los.getD b (SL.cst 0 1)).val u v

lemma domU_of_check {ck : RF → Bool} {σ : Bool} {Δ X Y : Poly} {b0 b1 R : ℕ} {u δ : ℝ}
    (h : VCtx ck Δ X Y σ b0 b1 R u δ) {ups : List SL} (hd : ∀ L ∈ ups, L.d ≠ 0) {Ua : List ℕ}
    (hlt : ∀ a ∈ Ua, a < ups.length)
    (hall : ups.all (fun U => Ua.any fun a =>
      ck ((U.sub (ups.getD a (SL.cst 0 1))).atV Δ X Y)) = true) :
    DomU u (vtx X Y δ u) ups Ua := by
  intro U hU
  obtain ⟨b, hb, hc⟩ := List.any_eq_true.mp ((List.all_eq_true.mp hall) U hU)
  have hbm := getD_mem (SL.cst 0 1) (hlt b hb)
  have h0 := ckRF_sound hc h (Nat.mul_ne_zero (hd U hU) (hd _ hbm))
  rw [eval_atV _ _ _ _ h.hΔ h.ok.hδ, val_sub _ _ (hd U hU) (hd _ hbm) h.hu0 h.hu1] at h0
  exact ⟨b, hb, by simp only [vtx] at h0 ⊢; linarith⟩

lemma domL_of_check {ck : RF → Bool} {σ : Bool} {Δ X Y : Poly} {b0 b1 R : ℕ} {u δ : ℝ}
    (h : VCtx ck Δ X Y σ b0 b1 R u δ) {los : List SL} (hd : ∀ L ∈ los, L.d ≠ 0) {La : List ℕ}
    (hlt : ∀ a ∈ La, a < los.length)
    (hall : los.all (fun L => La.any fun b =>
      ck (((los.getD b (SL.cst 0 1)).sub L).atV Δ X Y)) = true) :
    DomL u (vtx X Y δ u) los La := by
  intro L hL
  obtain ⟨b, hb, hc⟩ := List.any_eq_true.mp ((List.all_eq_true.mp hall) L hL)
  have hbm := getD_mem (SL.cst 0 1) (hlt b hb)
  have h0 := ckRF_sound hc h (Nat.mul_ne_zero (hd _ hbm) (hd L hL))
  rw [eval_atV _ _ _ _ h.hΔ h.ok.hδ, val_sub _ _ (hd _ hbm) (hd L hL) h.hu0 h.hu1] at h0
  exact ⟨b, hb, by simp only [vtx] at h0 ⊢; linarith⟩

lemma exists_min_of_dom {u : ℝ} {v : ℝ × ℝ} {ups : List SL} {Ua : List ℕ} (hne : Ua ≠ [])
    (hdom : DomU u v ups Ua) :
    ∃ a ∈ Ua, ∀ U' ∈ ups, (ups.getD a (SL.cst 0 1)).val u v ≤ U'.val u v := by
  classical
  obtain ⟨a, ha, hmin⟩ := Ua.toFinset.exists_min_image (fun a => (ups.getD a (SL.cst 0 1)).val u v)
    (by obtain ⟨x, hx⟩ := List.exists_mem_of_ne_nil Ua hne; exact ⟨x, List.mem_toFinset.mpr hx⟩)
  refine ⟨a, List.mem_toFinset.mp ha, fun U' hU' => ?_⟩
  obtain ⟨b, hb, hle⟩ := hdom U' hU'
  exact le_trans (hmin b (List.mem_toFinset.mpr hb)) hle

lemma exists_max_of_dom {u : ℝ} {v : ℝ × ℝ} {los : List SL} {La : List ℕ} (hne : La ≠ [])
    (hdom : DomL u v los La) :
    ∃ b ∈ La, ∀ L' ∈ los, L'.val u v ≤ (los.getD b (SL.cst 0 1)).val u v := by
  classical
  obtain ⟨a, ha, hmax⟩ := La.toFinset.exists_max_image (fun a => (los.getD a (SL.cst 0 1)).val u v)
    (by obtain ⟨x, hx⟩ := List.exists_mem_of_ne_nil La hne; exact ⟨x, List.mem_toFinset.mpr hx⟩)
  refine ⟨a, List.mem_toFinset.mp ha, fun L' hL' => ?_⟩
  obtain ⟨b, hb, hle⟩ := hdom L' hL'
  exact le_trans hle (hmax b (List.mem_toFinset.mpr hb))

lemma hd_hUps {D : ℕ} (hD : 0 < D) (e : SegE) : ∀ L ∈ hUps D e, L.d ≠ 0 := by
  intro L hL; simp only [hUps, List.mem_cons, List.not_mem_nil, or_false] at hL
  rcases hL with rfl | rfl | rfl <;> simp [SL.cst, hTC, hTD] <;> omega
lemma hd_hLos {D : ℕ} (hD : 0 < D) (e : SegE) : ∀ L ∈ hLos D e, L.d ≠ 0 := by
  intro L hL; simp only [hLos, List.mem_cons, List.not_mem_nil, or_false] at hL
  rcases hL with rfl | rfl | rfl <;> simp [SL.cst, hTA, hTB] <;> omega
lemma hd_vUps {D : ℕ} (hD : 0 < D) (e : SegE) : ∀ L ∈ vUps D e, L.d ≠ 0 := by
  intro L hL; simp only [vUps, List.mem_cons, List.not_mem_nil, or_false] at hL
  rcases hL with rfl | rfl | rfl <;> simp [SL.cst, vUXs, vUYs] <;> omega
lemma hd_vLos {D : ℕ} (hD : 0 < D) (e : SegE) : ∀ L ∈ vLos D e, L.d ≠ 0 := by
  intro L hL; simp only [vLos, List.mem_cons, List.not_mem_nil, or_false] at hL
  rcases hL with rfl | rfl | rfl <;> simp [SL.cst, vLXs, vLYs] <;> omega

/-- **A horizontal segment's term** is at least one of its alternatives, under dominance. -/
theorem hseg_dom {ck : RF → Bool} {D : ℕ} (hD : 0 < D) {σ : Bool} {Δ X Y : Poly} {b0 b1 R : ℕ} {u δ : ℝ}
    (h : VCtx ck Δ X Y σ b0 b1 R u δ) {e : SegE} (hx : e.1 < e.2.2.1) {Ua La : List ℕ}
    (hUa : Ua ≠ []) (hLa : La ≠ []) (hlu : ∀ a ∈ Ua, a < (hUps D e).length)
    (hll : ∀ b ∈ La, b < (hLos D e).length) (du : DomU u (vtx X Y δ u) (hUps D e) Ua)
    (dl : DomL u (vtx X Y δ u) (hLos D e) La) :
    ∃ t ∈ segAlts Δ X Y e.2.2.2.2 D (e.2.2.1 - e.1) (hUps D e) (hLos D e) Ua La,
      t.eval δ u ≤ (hsegT (2 * Real.arctan u) D e).1 *
        max 0 (clampMin (hsegT (2 * Real.arctan u) D e).2.1 (hsegT (2 * Real.arctan u) D e).2.2
          (vtx X Y δ u)) := by
  obtain ⟨a, ha, hamin⟩ := exists_min_of_dom hUa du
  obtain ⟨b, hb, hbmax⟩ := exists_max_of_dom hLa dl
  refine ⟨_, List.mem_flatMap.mpr ⟨a, ha, List.mem_map.mpr ⟨b, hb, rfl⟩⟩, ?_⟩
  exact hseg_core hD h hx (getD_mem _ (hlu a ha)) (getD_mem _ (hll b hb)) hamin hbmax

theorem vseg_dom {ck : RF → Bool} {D : ℕ} (hD : 0 < D) {σ : Bool} {Δ X Y : Poly} {b0 b1 R : ℕ} {u δ : ℝ}
    (h : VCtx ck Δ X Y σ b0 b1 R u δ) {e : SegE} (hx : e.2.1 < e.2.2.2.1) {Ua La : List ℕ}
    (hUa : Ua ≠ []) (hLa : La ≠ []) (hlu : ∀ a ∈ Ua, a < (vUps D e).length)
    (hll : ∀ b ∈ La, b < (vLos D e).length) (du : DomU u (vtx X Y δ u) (vUps D e) Ua)
    (dl : DomL u (vtx X Y δ u) (vLos D e) La) :
    ∃ t ∈ segAlts Δ X Y e.2.2.2.2 D (e.2.2.2.1 - e.2.1) (vUps D e) (vLos D e) Ua La,
      t.eval δ u ≤ (vsegT (2 * Real.arctan u) D e).1 *
        max 0 (clampMin (vsegT (2 * Real.arctan u) D e).2.1 (vsegT (2 * Real.arctan u) D e).2.2
          (vtx X Y δ u)) := by
  obtain ⟨a, ha, hamin⟩ := exists_min_of_dom hUa du
  obtain ⟨b, hb, hbmax⟩ := exists_max_of_dom hLa dl
  refine ⟨_, List.mem_flatMap.mpr ⟨a, ha, List.mem_map.mpr ⟨b, hb, rfl⟩⟩, ?_⟩
  exact vseg_core hD h hx (getD_mem _ (hlu a ha)) (getD_mem _ (hll b hb)) hamin hbmax

/-! ### Combinations -/

/-- All ways of picking one element from each list. -/
def cprod {α : Type*} : List (List α) → List (List α)
  | [] => [[]]
  | l :: ls => l.flatMap fun a => (cprod ls).map (a :: ·)

lemma mem_cprod_iff {α : Type*} : ∀ (L : List (List α)) (c : List α),
    c ∈ cprod L ↔ List.Forall₂ (fun a l => a ∈ l) c L
  | [], c => by simp [cprod]
  | l :: L, c => by
    simp only [cprod, List.mem_flatMap, List.mem_map]
    constructor
    · rintro ⟨a, ha, c', hc', rfl⟩
      exact List.Forall₂.cons ha ((mem_cprod_iff L c').mp hc')
    · intro h
      cases h with
      | cons ha hrest => exact ⟨_, ha, _, (mem_cprod_iff L _).mpr hrest, rfl⟩

/-- The positions with several alternatives first, the fixed ones last: `sumRF` folds from the
right, so the sum of the fixed terms is one subterm shared by every combination. -/
def reord (L : List (List RF)) : List (List RF) :=
  L.filter (fun l => l.length != 1) ++ L.filter (fun l => l.length == 1)

lemma exists_reord {L : List (List RF)} {c : List RF} (h : c ∈ cprod L) :
    ∃ c' ∈ cprod (reord L), c'.Perm c := by
  rw [mem_cprod_iff] at h
  have key : ∀ (P : List RF → Bool) (L : List (List RF)) (c : List RF),
      List.Forall₂ (fun a l => a ∈ l) c L →
      ∃ c1 c2, List.Forall₂ (fun a l => a ∈ l) c1 (L.filter P) ∧
        List.Forall₂ (fun a l => a ∈ l) c2 (L.filter (fun l => !P l)) ∧ (c1 ++ c2).Perm c := by
    intro P L c h
    induction h with
    | nil => exact ⟨[], [], by simp, by simp, by simp⟩
    | @cons a l c L ha _ ih =>
      obtain ⟨c1, c2, h1, h2, hp⟩ := ih
      cases hP : P l
      · refine ⟨c1, a :: c2, by simpa [List.filter_cons, hP] using h1, ?_, ?_⟩
        · have := List.Forall₂.cons (R := fun a l => a ∈ l) ha h2
          simpa [List.filter_cons, hP] using this
        · exact (List.perm_middle).trans (List.Perm.cons a hp)
      · refine ⟨a :: c1, c2, ?_, by simpa [List.filter_cons, hP] using h2, ?_⟩
        · have := List.Forall₂.cons (R := fun a l => a ∈ l) ha h1
          simpa [List.filter_cons, hP] using this
        · exact List.Perm.cons a hp
  obtain ⟨c1, c2, h1, h2, hp⟩ := key (fun l => l.length != 1) L c h
  refine ⟨c1 ++ c2, ?_, hp⟩
  rw [mem_cprod_iff, reord]
  have e : L.filter (fun l => !(l.length != 1)) = L.filter (fun l => l.length == 1) := by
    congr 1; funext l; simp [bne]
  rw [e] at h2
  exact List.rel_append h1 h2

/-- If each `x_s` is at least some alternative of list `s`, some combination sums to at most
`Σ x_s`. -/
lemma exists_comb_le {f : RF → ℝ} :
    ∀ (Ls : List (List RF)) (xs : List ℝ), Ls.length = xs.length →
      (∀ p ∈ Ls.zip xs, ∃ t ∈ p.1, f t ≤ p.2) →
      ∃ comb ∈ cprod Ls, (comb.map f).sum ≤ xs.sum
  | [], [], _, _ => ⟨[], by simp [cprod], by simp⟩
  | [], _ :: _, h, _ => by simp at h
  | _ :: _, [], h, _ => by simp at h
  | l :: Ls, x :: xs, h, hp => by
    obtain ⟨t, ht, htx⟩ := hp (l, x) List.mem_cons_self
    obtain ⟨comb, hc, hcs⟩ := exists_comb_le Ls xs (by simpa using h)
      fun p hq => hp p (List.mem_cons_of_mem _ hq)
    refine ⟨t :: comb, List.mem_flatMap.mpr ⟨t, ht, List.mem_map.mpr ⟨comb, hc, rfl⟩⟩, ?_⟩
    simp only [List.map_cons, List.sum_cons]
    linarith

lemma mem_cprod {α : Type*} {P : α → Prop} : ∀ (Ls : List (List α)), (∀ l ∈ Ls, ∀ a ∈ l, P a) →
    ∀ comb ∈ cprod Ls, ∀ a ∈ comb, P a
  | [], _, comb, hc, a, ha => by simp [cprod] at hc; subst hc; simp at ha
  | l :: Ls, h, comb, hc, a, ha => by
    obtain ⟨b, hb, hc'⟩ := List.mem_flatMap.mp hc
    obtain ⟨c, hc'', rfl⟩ := List.mem_map.mp hc'
    rcases List.mem_cons.mp ha with rfl | ha
    · exact h l List.mem_cons_self a hb
    · exact mem_cprod Ls (fun l' hl' => h l' (List.mem_cons_of_mem _ hl')) c hc'' a ha

/-! ### The test at a vertex -/

/-- A segment's certificate at a vertex: dropped, the leaf's box-wide alternatives (dominance
certified once for the whole region), or alternatives checked at this vertex. -/
inductive SegC where
  | drop
  | box
  | alt (Ua La : List ℕ)

def segCAlts (Δ X Y : Poly) (w D len : ℕ) (ups los : List SL) (bx : List ℕ × List ℕ) : SegC → List RF
  | .drop => [RF.const 0 1]
  | .box => segAlts Δ X Y w D len ups los bx.1 bx.2
  | .alt Ua La => segAlts Δ X Y w D len ups los Ua La

def segCOk (ck : RF → Bool) (σ : Bool) (Δ X Y : Poly) (b0 b1 R : ℕ) (ups los : List SL) (bx : List ℕ × List ℕ) :
    SegC → Bool
  | .drop => true
  | .box => !bx.1.isEmpty && !bx.2.isEmpty && bx.1.all (· < ups.length) && bx.2.all (· < los.length)
  | .alt Ua La => segOkA ck σ Δ X Y b0 b1 R ups los Ua La

lemma segVal_d {D : ℕ} (hD : 0 < D) {Δ X Y : Poly} {w len : ℕ} (hlen : len ≠ 0) {ups los : List SL}
    (hu : ∀ L ∈ ups, L.d ≠ 0) (hl : ∀ L ∈ los, L.d ≠ 0) (iu il : ℕ) :
    (segVal Δ X Y w D len ups los iu il).d ≠ 0 := by
  have a : (ups.getD iu (SL.cst 0 1)).d ≠ 0 := by
    by_cases h : iu < ups.length
    · exact hu _ (getD_mem _ h)
    · rw [List.getD_eq_default _ _ (by omega)]; simp [SL.cst]
  have b : (los.getD il (SL.cst 0 1)).d ≠ 0 := by
    by_cases h : il < los.length
    · exact hl _ (getD_mem _ h)
    · rw [List.getD_eq_default _ _ (by omega)]; simp [SL.cst]
  simp only [segVal, RF.mul, RF.const, SL.atV, SL.sub]
  exact Nat.mul_ne_zero hlen (Nat.mul_ne_zero a b)

lemma segCAlts_d {D : ℕ} (hD : 0 < D) {Δ X Y : Poly} {w len : ℕ} (hlen : len ≠ 0)
    {ups los : List SL} (hu : ∀ L ∈ ups, L.d ≠ 0) (hl : ∀ L ∈ los, L.d ≠ 0) (bx : List ℕ × List ℕ)
    (c : SegC) : ∀ r ∈ segCAlts Δ X Y w D len ups los bx c, r.d ≠ 0 := by
  intro r hr
  cases c with
  | drop => simp [segCAlts] at hr; subst hr; simp [RF.const]
  | box =>
    obtain ⟨a, _, hr⟩ := List.mem_flatMap.mp hr
    obtain ⟨b, _, rfl⟩ := List.mem_map.mp hr
    exact segVal_d hD hlen hu hl a b
  | alt Ua La =>
    obtain ⟨a, _, hr⟩ := List.mem_flatMap.mp hr
    obtain ⟨b, _, rfl⟩ := List.mem_map.mp hr
    exact segVal_d hD hlen hu hl a b

lemma exists_comb_zip {β : Type*} {f : RF → ℝ} :
    ∀ (ps : List β) (alts : β → List RF) (x : β → ℝ), (∀ p ∈ ps, ∃ t ∈ alts p, f t ≤ x p) →
      ∃ comb ∈ cprod (ps.map alts), (comb.map f).sum ≤ (ps.map x).sum
  | [], _, _, _ => ⟨[], by simp [cprod], by simp⟩
  | p :: ps, alts, x, h => by
    obtain ⟨t, ht, htx⟩ := h p List.mem_cons_self
    obtain ⟨comb, hc, hcs⟩ := exists_comb_zip ps alts x fun q hq => h q (List.mem_cons_of_mem _ hq)
    refine ⟨t :: comb, ?_, ?_⟩
    · simp only [List.map_cons, cprod]
      exact List.mem_flatMap.mpr ⟨t, ht, List.mem_map.mpr ⟨comb, hc, rfl⟩⟩
    · simp only [List.map_cons, List.sum_cons]; linarith

lemma cprod_append {α : Type*} : ∀ (A B : List (List α)) {c1 c2 : List α}, c1 ∈ cprod A →
    c2 ∈ cprod B → c1 ++ c2 ∈ cprod (A ++ B)
  | [], B, c1, c2, h1, h2 => by simp [cprod] at h1; subst h1; simpa using h2
  | l :: A, B, c1, c2, h1, h2 => by
    obtain ⟨a, ha, h1'⟩ := List.mem_flatMap.mp h1
    obtain ⟨c, hc, rfl⟩ := List.mem_map.mp h1'
    simp only [List.cons_append, cprod]
    exact List.mem_flatMap.mpr ⟨a, ha, List.mem_map.mpr ⟨c ++ c2, cprod_append A B hc h2, rfl⟩⟩

lemma sum_map_zip_fst {α β : Type*} (l : List α) (m : List β) (g : α → ℝ) (h : m.length = l.length) :
    ((l.zip m).map fun q => g q.1).sum = (l.map g).sum := by
  rw [show (fun q : α × β => g q.1) = g ∘ Prod.fst from rfl, ← List.map_map,
    List.map_fst_zip (by omega)]

/-- The leaf's box-wide dominance, at the vertex. -/
def BoxDom (D : ℕ) (u : ℝ) (v : ℝ × ℝ) (chs cvs : List SegE) (hbx vbx : List (List ℕ × List ℕ)) :
    Prop :=
  (∀ q ∈ chs.zip hbx, DomU u v (hUps D q.1) q.2.1 ∧ DomL u v (hLos D q.1) q.2.2) ∧
    (∀ q ∈ cvs.zip vbx, DomU u v (vUps D q.1) q.2.1 ∧ DomL u v (vLos D q.1) q.2.2)

/-! ### Splits, tags, and the test at a vertex -/

/-- A split of a vertex certificate on the sign of a scaled line `q` at the vertex, with S-procedure
multipliers `nm/dm` (used where `q < 0`) and `np/dp` (used where `q ≥ 0`). -/
structure Split where
  q : SL
  nm : ℕ
  dm : ℕ
  np : ℕ
  dp : ℕ

/-- A tag: usable always (`none`), or only when split `k` is on side `b` (`true`: `q ≥ 0`). -/
abbrev Tag := Option (ℕ × Bool)

def tagOk (pat : List Bool) : Tag → Bool
  | none => true
  | some (k, b) => pat.getD k false == b

/-- All sign patterns of `n` splits. -/
def pats : ℕ → List (List Bool)
  | 0 => [[]]
  | n + 1 => (pats n).flatMap fun p => [false :: p, true :: p]

lemma mem_pats : ∀ p : List Bool, p ∈ pats p.length
  | [] => by simp [pats]
  | b :: p => by
    simp only [List.length_cons, pats, List.mem_flatMap, List.mem_cons, List.mem_singleton,
      List.not_mem_nil, or_false]
    exact ⟨p, mem_pats p, by cases b <;> simp⟩

/-- The S-procedure term of a split on side `b`: `μ⁺ q` subtracted where `q ≥ 0`, `μ⁻ q` added where
`q < 0`; either way it is `≤ 0` on its side. -/
def sproc (Δ X Y : Poly) (sp : Split) (b : Bool) : RF :=
  if b then RF.neg (RF.mul (RF.const sp.np sp.dp) (sp.q.atV Δ X Y))
  else RF.mul (RF.const sp.nm sp.dm) (sp.q.atV Δ X Y)

/-- A cap alternative: `0` (checked `d ≤ 0` on the sub-bin, or by a split on `d` on its negative
side), the parabola, or the line (checked `d ≥ s`, or by a split on `d − s` on its side `≥ 0`). -/
inductive CapA where
  | zeroC
  | zeroT (k : ℕ)
  | par
  | parT (k : ℕ) (b : Bool)
  | linC
  | linT (k : ℕ)

def capTag : CapA → Tag
  | .zeroT k => some (k, false)
  | .parT k b => some (k, b)
  | .linT k => some (k, true)
  | _ => none

def splitAt (splits : List Split) (k : ℕ) : SL := (splits.getD k ⟨SL.cst 0 1, 0, 1, 0, 1⟩).q

def capAOk (ck : RF → Bool) (σ : Bool) (Δ X Y : Poly) (b0 b1 R : ℕ) (splits : List Split) (cap : SL) : CapA → Bool
  | .zeroC => ghOk ck σ Δ X Y b0 b1 R cap 0
  | .zeroT k => decide (k < splits.length) && splitAt splits k == cap
  | .par => true
  | .parT k _ => decide (k < splits.length)
  | .linC => ghOk ck σ Δ X Y b0 b1 R cap 2
  | .linT k => decide (k < splits.length) && splitAt splits k == cap.sub (sSL 1)

def capAU (Δ X Y : Poly) (cap : SL) : CapA → RF
  | .zeroC => ghU Δ X Y cap 0
  | .zeroT _ => ghU Δ X Y cap 0
  | .par => ghU Δ X Y cap 1
  | .parT _ _ => ghU Δ X Y cap 1
  | .linC => ghU Δ X Y cap 2
  | .linT _ => ghU Δ X Y cap 2

/-- The rectangle term `ρ (1 − U_x − U_y)` for two cap alternatives. -/
def lebRF (Δ X Y : Poly) (D : ℕ) (r : RectM) (ax ay : CapA) : RF :=
  RF.mul (RF.const r.1.2.2.2.2 1) (RF.add Δ (RF.add Δ (RF.const 1 1)
    (RF.neg (capAU Δ X Y (capXm D r) ax))) (RF.neg (capAU Δ X Y (capYm D r) ay)))

/-- A scaled line at the fixed point `(x/q, y/q)`: a constant of the centre (`e = 0`). -/
def slAtP (L : SL) (x y q : ℕ) : RF :=
  ⟨BernZ.add (BernZ.add (smul (x : ℤ) L.P.1) (smul (y : ℤ) L.P.2.1)) (smul (q : ℤ) L.P.2.2), 0, L.i, L.j, L.k,
    L.d * q⟩

/-- `cos θ`, `sin θ` and `1/(2 cos θ)` as rational functions of `u`. -/
def cRF : RF := ⟨Cp, 0, 0, 0, 1, 1⟩
def sRF : RF := ⟨Sp, 0, 0, 0, 1, 1⟩
def i2cRF : RF := ⟨Np, 0, 1, 0, 0, 2⟩

/-- The McCormick term `LemmaE.mcQ` from the values of `A, B, β*, α, β`. -/
def mcRF (Δ : Poly) (A B bs α β : RF) : RF :=
  RF.mul i2cRF (RF.add Δ (RF.add Δ
    (RF.mul (RF.mul (RF.const 2 1) cRF) (RF.add Δ (RF.add Δ (RF.mul A β) (RF.mul B α)) (RF.neg (RF.mul A B))))
    (RF.mul sRF (RF.add Δ (RF.mul (RF.mul (RF.const 2 1) bs) β) (RF.neg (RF.mul bs bs)))))
    (RF.neg (RF.mul sRF (RF.mul α α))))

/-- The alternatives of a rectangle's term for two cap alternatives: one for std, the two branches of
the minimum for a corner kind (`LemmaE.lebPhi`). -/
def lebRFs (Δ X Y : Poly) (D : ℕ) (r : RectM) (ax ay : CapA) : List RF :=
  let w := RF.const r.1.2.2.2.2 1
  let gx := RF.neg (capAU Δ X Y (capXm D r) ax)
  let gy := RF.neg (capAU Δ X Y (capYm D r) ay)
  match r.2.2.2 with
  | .std => [lebRF Δ X Y D r ax ay]
  | .c3 xa ya ym q =>
    let aL := (capX D r.1.1).sub (sSL 1)
    let bL := capY D r.1.2.1
    let mc := mcRF Δ (slAtP aL xa ya q) (slAtP bL xa ya q) (slAtP bL xa ym q)
      (((capXm D r).sub (sSL 1)).atV Δ X Y) ((capYm D r).atV Δ X Y)
    [RF.mul w (RF.add Δ (RF.add Δ (RF.add Δ (RF.const 1 1) gx) gy) mc), RF.mul w (RF.add Δ (RF.const 1 1) gx)]
  | .xc xa ya ym q =>
    let aL := capX D r.1.1
    let bL := (capY D r.1.2.1).sub (cSL 1)
    let mc := mcRF Δ (slAtP aL xa ya q) (slAtP bL xa ya q) (slAtP bL xa ym q)
      ((capXm D r).atV Δ X Y) (((capYm D r).sub (cSL 1)).atV Δ X Y)
    [RF.mul w (RF.add Δ (RF.add Δ (RF.const 1 1) gy) mc), lebRF Δ X Y D r ax ay]

/-! ### Common-factor certificates (`qx2_zm._gcdcert`) -/

/-- The numerator with the sign of the denominator folded in (`σ^e · num`). -/
def snum (σ : Bool) (r : RF) : Poly := if σ || r.e % 2 == 0 then r.num else smul (-1) r.num

lemma snum_sign {ck : RF → Bool} {σ : Bool} {Δ X Y : Poly} {b0 b1 R : ℕ} {u δ : ℝ} (h : VCtx ck Δ X Y σ b0 b1 R u δ)
    {r : RF} (hd : r.d ≠ 0) :
    (0 ≤ r.eval δ u ↔ 0 ≤ eval (snum σ r) u) ∧ (r.eval δ u < 0 ↔ eval (snum σ r) u < 0) := by
  have h1 : (0 : ℝ) < 1 - u ^ 2 := by nlinarith [h.hu0, h.hu1]
  have h2 : (0 : ℝ) < 2 * u := by linarith [h.hu0]
  have h3 : (0 : ℝ) < 1 + u ^ 2 := by positivity
  have h4 : (0 : ℝ) < r.d := by exact_mod_cast Nat.pos_of_ne_zero hd
  have hrest : 0 < (1 - u ^ 2) ^ r.i * (2 * u) ^ r.j * (1 + u ^ 2) ^ r.k * (r.d : ℝ) := by positivity
  have hden : den r δ u = δ ^ r.e * ((1 - u ^ 2) ^ r.i * (2 * u) ^ r.j * (1 + u ^ 2) ^ r.k * r.d) := by
    unfold den; ring
  unfold RF.eval snum
  rw [hden]
  by_cases hpos : σ = true ∨ r.e % 2 = 0
  · have hsel : (if σ || r.e % 2 == 0 then r.num else smul (-1) r.num) = r.num := by
      rcases hpos with hp | hp <;> simp [hp]
    rw [hsel]
    have hδe : 0 < δ ^ r.e := by
      rcases hpos with hp | hp
      · have := h.hσ; simp only [hp, if_true] at this; exact pow_pos this _
      · exact Even.pow_pos (Nat.even_iff.mpr hp) h.ok.hδ
    have hD := mul_pos hδe hrest
    exact ⟨⟨fun h0 => by
        by_contra hc; push_neg at hc; have := div_neg_of_neg_of_pos hc hD; linarith,
      fun h0 => div_nonneg h0 hD.le⟩,
      ⟨fun h0 => by
        by_contra hc; push_neg at hc; have := div_nonneg hc hD.le; linarith,
      fun h0 => div_neg_of_neg_of_pos h0 hD⟩⟩
  · simp only [not_or, Bool.not_eq_true] at hpos
    obtain ⟨hp1, hp2⟩ := hpos
    have hsel : (if σ || r.e % 2 == 0 then r.num else smul (-1) r.num) = smul (-1) r.num := by
      simp [hp1, hp2]
    rw [hsel, eval_smul]
    have hσ := h.hσ; simp only [hp1, Bool.false_eq_true, if_false] at hσ
    have hodd : Odd r.e := Nat.odd_iff.mpr (by omega)
    have hδe : δ ^ r.e < 0 := hodd.pow_neg hσ
    have hD := mul_neg_of_neg_of_pos hδe hrest
    push_cast
    constructor
    · constructor
      · intro h0
        by_contra hc; push_neg at hc
        have : 0 < eval r.num u := by linarith
        have := div_neg_of_pos_of_neg this hD; linarith
      · intro h0; exact div_nonneg_of_nonpos (by linarith) hD.le
    · constructor
      · intro h0
        by_contra hc; push_neg at hc
        have : eval r.num u ≤ 0 := by linarith
        have := div_nonneg_of_nonpos this hD.le; linarith
      · intro h0; exact div_neg_of_pos_of_neg (by linarith) hD

/-- Trailing zeros removed. -/
def ptrim (p : Poly) : Poly := (p.reverse.dropWhile (· == 0)).reverse

lemma eval_append_zeros (p : Poly) (n : ℕ) (u : ℝ) : eval (p ++ List.replicate n 0) u = eval p u := by
  induction p with
  | nil =>
    induction n with
    | zero => simp
    | succ n ih =>
      simp only [List.nil_append, eval_nil] at ih ⊢
      rw [List.replicate_succ, eval_cons, ih]; simp
  | cons a p ih => simp [ih]

lemma ptrim_spec (p : Poly) : ∃ n, p = ptrim p ++ List.replicate n 0 := by
  unfold ptrim
  obtain ⟨n, hn⟩ : ∃ n, p.reverse = List.replicate n 0 ++ p.reverse.dropWhile (· == 0) := by
    generalize p.reverse = l
    induction l with
    | nil => exact ⟨0, by simp⟩
    | cons a l ih =>
      by_cases ha : a = 0
      · subst ha; obtain ⟨n, hn⟩ := ih
        refine ⟨n + 1, ?_⟩
        simp only [List.dropWhile_cons, beq_self_eq_true, if_true]
        rw [List.replicate_succ, List.cons_append, ← hn]
      · exact ⟨0, by simp [List.dropWhile_cons, ha]⟩
  refine ⟨n, ?_⟩
  have := congrArg List.reverse hn
  rw [List.reverse_reverse, List.reverse_append, List.reverse_replicate] at this
  exact this

lemma eval_ptrim (p : Poly) (u : ℝ) : eval (ptrim p) u = eval p u := by
  obtain ⟨n, hn⟩ := ptrim_spec p
  conv_rhs => rw [hn]
  rw [eval_append_zeros]

/-- Equality of polynomials up to trailing zeros. -/
def peqb (p q : Poly) : Bool := ptrim p == ptrim q

lemma eval_of_peqb {p q : Poly} (h : peqb p q = true) (u : ℝ) : eval p u = eval q u := by
  simp only [peqb, beq_iff_eq] at h
  rw [← eval_ptrim p, h, eval_ptrim]

/-- Exact division of `p` by `g` over the integers (high coefficients first); any result is
re-checked by multiplication, so it need not be proved correct. -/
def divHL (rg : List ℤ) : ℕ → List ℤ → List ℤ
  | 0, _ => []
  | fuel + 1, rp =>
    if rp.length < rg.length then [] else
      match rp, rg with
      | a :: _, b :: _ =>
        let c := a / b
        c :: divHL rg fuel (List.zipWith (fun x y => x - c * y) rp (rg ++ List.replicate (rp.length - rg.length) 0)).tail
      | _, _ => []

def pdiv (p g : Poly) : Poly :=
  (divHL (ptrim g).reverse (ptrim p).length (ptrim p).reverse).reverse

/-- A common-factor certificate: split `k`'s numerator is `G · g₁` with `g₁ = u^m g₁' > 0` on the
sub-bin; then on that split's side the sign of `G` is known, and a total `T = G · c₁` is `≥ 0` there
if `c₁` has the matching sign. -/
structure FCert where
  k : ℕ
  G : Poly
  g1 : Poly
  m : ℕ

def fcOk (σ : Bool) (Δ X Y : Poly) (b0 b1 R : ℕ) (splits : List Split) (pat : List Bool) (f : FCert)
    (T : RF) : Bool :=
  let c1 := pdiv (snum σ T) f.G
  decide (f.k < splits.length) &&
    peqb (snum σ ((splitAt splits f.k).atV Δ X Y)) (BernZ.mul f.G f.g1) &&
    (f.g1.take f.m).all (· == 0) &&
    checkPos (f.g1.drop f.m) ((f.g1.drop f.m).length - 1) b0 b1 R &&
    peqb (snum σ T) (BernZ.mul f.G c1) &&
    BernZ.check (if pat.getD f.k false then c1 else smul (-1) c1) (c1.length - 1) b0 b1 R

/-- The total test: `T ≥ 0` by Bernstein, or by a common-factor certificate. -/
def totOk (ck : RF → Bool) (σ : Bool) (Δ X Y : Poly) (b0 b1 R : ℕ) (splits : List Split) (pat : List Bool)
    (fcs : List FCert) (T : RF) : Bool :=
  ck T || fcs.any fun f => fcOk σ Δ X Y b0 b1 R splits pat f T

/-- A certificate at a vertex. -/
structure VCert where
  splits : List Split
  fcs : List FCert
  hc : List (List (SegC × Tag))
  vc : List (List (SegC × Tag))
  lc : List (List CapA × List CapA)

/-- The alternatives of a horizontal (vertical) segment consistent with a pattern. -/
def hAltsP (Δ X Y : Poly) (D : ℕ) (pat : List Bool) (q : (SegE × (List ℕ × List ℕ)) × List (SegC × Tag)) :
    List RF :=
  (q.2.filter fun x => tagOk pat x.2).flatMap fun x =>
    segCAlts Δ X Y q.1.1.2.2.2.2 D (q.1.1.2.2.1 - q.1.1.1) (hUps D q.1.1) (hLos D q.1.1) q.1.2 x.1
def vAltsP (Δ X Y : Poly) (D : ℕ) (pat : List Bool) (q : (SegE × (List ℕ × List ℕ)) × List (SegC × Tag)) :
    List RF :=
  (q.2.filter fun x => tagOk pat x.2).flatMap fun x =>
    segCAlts Δ X Y q.1.1.2.2.2.2 D (q.1.1.2.2.2.1 - q.1.1.2.1) (vUps D q.1.1) (vLos D q.1.1) q.1.2 x.1
def lAltsP (Δ X Y : Poly) (D : ℕ) (pat : List Bool) (p : RectM × (List CapA × List CapA)) : List RF :=
  (p.2.1.filter fun a => tagOk pat (capTag a)).flatMap fun ax =>
    (p.2.2.filter fun a => tagOk pat (capTag a)).flatMap fun ay => lebRFs Δ X Y D p.1 ax ay

/-- **The test at a vertex**: every choice is valid, for every sign pattern of the splits every term
has a consistent alternative, and every consistent combination plus the S-procedure terms is
`≥ W`. -/
def vertOk (ck : RF → Bool) (D W : ℕ) (σ : Bool) (Δ X Y : Poly) (b0 b1 R : ℕ) (chs cvs : List SegE)
    (crs : List RectM) (hbx vbx : List (List ℕ × List ℕ)) (c : VCert) : Bool :=
  hbx.length == chs.length && vbx.length == cvs.length &&
    c.hc.length == chs.length && c.vc.length == cvs.length && c.lc.length == crs.length &&
    c.splits.all (fun sp => sp.dm != 0 && sp.dp != 0) &&
    ((chs.zip hbx).zip c.hc).all (fun q => q.2.all fun x =>
      segCOk ck σ Δ X Y b0 b1 R (hUps D q.1.1) (hLos D q.1.1) q.1.2 x.1) &&
    ((cvs.zip vbx).zip c.vc).all (fun q => q.2.all fun x =>
      segCOk ck σ Δ X Y b0 b1 R (vUps D q.1.1) (vLos D q.1.1) q.1.2 x.1) &&
    (crs.zip c.lc).all (fun p => p.2.1.all (capAOk ck σ Δ X Y b0 b1 R c.splits (capXm D p.1)) &&
      p.2.2.all (capAOk ck σ Δ X Y b0 b1 R c.splits (capYm D p.1))) &&
    (pats c.splits.length).all fun pat =>
      c.hc.all (fun l => l.any fun x => tagOk pat x.2) &&
      c.vc.all (fun l => l.any fun x => tagOk pat x.2) &&
      c.lc.all (fun l => l.1.any (fun a => tagOk pat (capTag a)) && l.2.any (fun a => tagOk pat (capTag a))) &&
      (cprod (reord (((chs.zip hbx).zip c.hc).map (hAltsP Δ X Y D pat) ++
          ((cvs.zip vbx).zip c.vc).map (vAltsP Δ X Y D pat) ++
          (crs.zip c.lc).map (lAltsP Δ X Y D pat)))).all fun comb =>
        totOk ck σ Δ X Y b0 b1 R c.splits pat c.fcs (sumRF Δ (comb ++
          (c.splits.zip pat).map (fun x => sproc Δ X Y x.1 x.2) ++ [RF.const (-(W : ℤ)) 1]))

/-! ### Soundness -/

/-- A segment choice: some alternative is at most the term. -/
lemma segC_ge {ck : RF → Bool} {σ : Bool} {Δ X Y : Poly} {b0 b1 R : ℕ} {u δ : ℝ} (h : VCtx ck Δ X Y σ b0 b1 R u δ)
    {ups los : List SL} {bx : List ℕ × List ℕ} {sc : SegC} {w D len : ℕ} {T : ℝ} (hT : 0 ≤ T)
    (hok : segCOk ck σ Δ X Y b0 b1 R ups los bx sc = true)
    (hbox : DomU u (vtx X Y δ u) ups bx.1 ∧ DomL u (vtx X Y δ u) los bx.2)
    (hcore : ∀ Ua La, Ua ≠ [] → La ≠ [] → (∀ a ∈ Ua, a < ups.length) → (∀ b ∈ La, b < los.length) →
      DomU u (vtx X Y δ u) ups Ua → DomL u (vtx X Y δ u) los La →
      ∃ t ∈ segAlts Δ X Y w D len ups los Ua La, t.eval δ u ≤ T)
    (hdu : ∀ L ∈ ups, L.d ≠ 0) (hdl : ∀ L ∈ los, L.d ≠ 0) :
    ∃ t ∈ segCAlts Δ X Y w D len ups los bx sc, t.eval δ u ≤ T := by
  cases sc with
  | drop => exact ⟨_, List.mem_singleton_self _, by rw [eval_const]; simpa using hT⟩
  | box =>
    simp only [segCOk, Bool.and_eq_true, Bool.not_eq_true', List.isEmpty_eq_false_iff,
      List.all_eq_true, decide_eq_true_eq] at hok
    obtain ⟨⟨⟨h1, h2⟩, h3⟩, h4⟩ := hok
    exact hcore _ _ h1 h2 h3 h4 hbox.1 hbox.2
  | alt Ua La =>
    simp only [segCOk, segOkA, Bool.and_eq_true, Bool.not_eq_true', List.isEmpty_eq_false_iff,
      List.all_eq_true, decide_eq_true_eq] at hok
    obtain ⟨⟨⟨⟨⟨h1, h2⟩, h3⟩, h4⟩, h5⟩, h6⟩ := hok
    exact hcore _ _ h1 h2 h3 h4 (domU_of_check h hdu h3 (List.all_eq_true.mpr h5))
      (domL_of_check h hdl h4 (List.all_eq_true.mpr h6))

/-- The pattern of the splits at the vertex: `true` where `q ≥ 0`. -/
noncomputable def patAt (splits : List Split) (u : ℝ) (v : ℝ × ℝ) : List Bool :=
  splits.map fun sp => decide (0 ≤ sp.q.val u v)

lemma patAt_getD (splits : List Split) (u : ℝ) (v : ℝ × ℝ) {k : ℕ} (hk : k < splits.length) :
    (patAt splits u v).getD k false = decide (0 ≤ (splitAt splits k).val u v) := by
  rw [patAt, List.getD_eq_getElem _ _ (by simpa using hk), List.getElem_map, splitAt,
    List.getD_eq_getElem _ _ hk]

/-- A cap alternative consistent with the pattern at the vertex bounds `ĝ`. -/
lemma capA_ge {ck : RF → Bool} {σ : Bool} {Δ X Y : Poly} {b0 b1 R : ℕ} {u δ : ℝ} (h : VCtx ck Δ X Y σ b0 b1 R u δ)
    {splits : List Split} {cap : SL} (hcap : cap.d ≠ 0) {a : CapA}
    (hok : capAOk ck σ Δ X Y b0 b1 R splits cap a = true)
    (htag : tagOk (patAt splits u (vtx X Y δ u)) (capTag a) = true) :
    SqArea.ghat (Real.sin (2 * Real.arctan u)) (Real.cos (2 * Real.arctan u))
      (cap.val u (vtx X Y δ u)) ≤ (capAU Δ X Y cap a).eval δ u := by
  cases a with
  | zeroC => exact ghU_sound h hcap hok
  | par => exact ghat_le_parU h hcap
  | parT _ _ => exact ghat_le_parU h hcap
  | linC => exact ghU_sound h hcap hok
  | zeroT k =>
    simp only [capAOk, Bool.and_eq_true, decide_eq_true_eq, beq_iff_eq] at hok
    simp only [capTag, tagOk, beq_iff_eq] at htag
    rw [patAt_getD _ _ _ hok.1, hok.2] at htag
    have hneg : cap.val u (vtx X Y δ u) < 0 := by simpa using htag
    rw [ghat_zero_of hneg.le]
    simp only [capAU, ghU, if_true, eval_const]; simp
  | linT k =>
    simp only [capAOk, Bool.and_eq_true, decide_eq_true_eq, beq_iff_eq] at hok
    simp only [capTag, tagOk, beq_iff_eq] at htag
    rw [patAt_getD _ _ _ hok.1, hok.2] at htag
    have hpos : 0 ≤ (cap.sub (sSL 1)).val u (vtx X Y δ u) := by simpa using htag
    rw [val_sub _ _ hcap (by simp [sSL]) h.hu0 h.hu1, val_sSL (by norm_num)] at hpos
    simp only [Nat.cast_one, div_one] at hpos
    exact ghat_le_linU h hcap (by linarith)

lemma capAU_d (Δ X Y : Poly) {cap : SL} (hcap : cap.d ≠ 0) (a : CapA) : (capAU Δ X Y cap a).d ≠ 0 := by
  cases a <;> simp only [capAU] <;> exact ghU_d Δ X Y cap hcap _

lemma lebRF_d (Δ X Y : Poly) {D : ℕ} (hD : 0 < D) (r : RectM) (hmx : modeP r.2.1 = true)
    (hmy : modeP r.2.2.1 = true) (ax ay : CapA) :
    (lebRF Δ X Y D r ax ay).d ≠ 0 := by
  have a := capAU_d Δ X Y (cap := capXm D r) (capXm_d hD r hmx) ax
  have b := capAU_d Δ X Y (cap := capYm D r) (capYm_d hD r hmy) ay
  exact Nat.mul_ne_zero one_ne_zero (RF.add_d _ (RF.add_d _ (by simp [RF.const])
    (by simpa [RF.neg] using a)) (by simpa [RF.neg] using b))

lemma lebRF_le {ck : RF → Bool} {D : ℕ} (hD : 0 < D) {σ : Bool} {Δ X Y : Poly} {b0 b1 R : ℕ} {u δ : ℝ}
    (h : VCtx ck Δ X Y σ b0 b1 R u δ) (r : RectM) (hmx : modeP r.2.1 = true)
    (hmy : modeP r.2.2.1 = true) {ax ay : CapA}
    (gx : SqArea.ghat (Real.sin (2 * Real.arctan u)) (Real.cos (2 * Real.arctan u))
      ((capXm D r).val u (vtx X Y δ u)) ≤ (capAU Δ X Y (capXm D r) ax).eval δ u)
    (gy : SqArea.ghat (Real.sin (2 * Real.arctan u)) (Real.cos (2 * Real.arctan u))
      ((capYm D r).val u (vtx X Y δ u)) ≤ (capAU Δ X Y (capYm D r) ay).eval δ u) :
    (lebRF Δ X Y D r ax ay).eval δ u ≤
      (rectT (2 * Real.arctan u) D r).1 *
        (1 - SqArea.ghat (Real.sin (2 * Real.arctan u)) (Real.cos (2 * Real.arctan u))
          (aff (rectT (2 * Real.arctan u) D r).2.1 (vtx X Y δ u)) -
          SqArea.ghat (Real.sin (2 * Real.arctan u)) (Real.cos (2 * Real.arctan u))
          (aff (rectT (2 * Real.arctan u) D r).2.2.1 (vtx X Y δ u))) := by
  have hcx : (capXm D r).d ≠ 0 := capXm_d hD r hmx
  have hcy : (capYm D r).d ≠ 0 := capYm_d hD r hmy
  have ex : aff (rectT (2 * Real.arctan u) D r).2.1 (vtx X Y δ u) = (capXm D r).val u (vtx X Y δ u) := by
    rw [val_capXm hD h.hu0 h.hu1 r hmx]; rfl
  have ey : aff (rectT (2 * Real.arctan u) D r).2.2.1 (vtx X Y δ u) = (capYm D r).val u (vtx X Y δ u) := by
    rw [val_capYm hD h.hu0 h.hu1 r hmy]; rfl
  rw [ex, ey]
  have dx := capAU_d Δ X Y hcx ax
  have dy := capAU_d Δ X Y hcy ay
  have d1 : (RF.const 1 1).d ≠ 0 := by simp [RF.const]
  have d2 : (RF.neg (capAU Δ X Y (capXm D r) ax)).d ≠ 0 := by simpa [RF.neg] using dx
  have d3 : (RF.neg (capAU Δ X Y (capYm D r) ay)).d ≠ 0 := by simpa [RF.neg] using dy
  rw [lebRF, eval_mul h.ok (by simp [RF.const]) (RF.add_d _ (RF.add_d _ d1 d2) d3),
    eval_add h.ok h.hΔ (RF.add_d _ d1 d2) d3, eval_add h.ok h.hΔ d1 d2, eval_neg, eval_neg,
    eval_const, eval_const]
  simp only [rectT, Int.cast_one, Nat.cast_one, div_one, Int.cast_natCast]
  exact mul_le_mul_of_nonneg_left (by linarith) (Nat.cast_nonneg _)

lemma eval_slAtP (L : SL) (x y q : ℕ) (hq : q ≠ 0) (δ u : ℝ) :
    (slAtP L x y q).eval δ u = L.val u ((x : ℝ) / q, (y : ℝ) / q) := by
  have hq' : (q : ℝ) ≠ 0 := by exact_mod_cast hq
  simp only [RF.eval, slAtP, den, SL.val, sden, aff, evalPL, BernZ.eval_add, BernZ.eval_smul]
  push_cast
  field_simp

lemma mul_d {r s : RF} (hr : r.d ≠ 0) (hs : s.d ≠ 0) : (RF.mul r s).d ≠ 0 := Nat.mul_ne_zero hr hs
lemma neg_d {r : RF} (hr : r.d ≠ 0) : (RF.neg r).d ≠ 0 := hr
lemma atV_d {L : SL} (hL : L.d ≠ 0) (Δ X Y : Poly) : (L.atV Δ X Y).d ≠ 0 := hL
lemma slAtP_d {L : SL} (hL : L.d ≠ 0) {q : ℕ} (hq : q ≠ 0) (x y : ℕ) : (slAtP L x y q).d ≠ 0 :=
  Nat.mul_ne_zero hL hq
lemma sub_d {L M : SL} (hL : L.d ≠ 0) (hM : M.d ≠ 0) : (L.sub M).d ≠ 0 := Nat.mul_ne_zero hL hM
lemma const_d (n : ℤ) {d : ℕ} (hd : d ≠ 0) : (RF.const n d).d ≠ 0 := hd

/-- The `d ≠ 0` side conditions of the `RF` arithmetic. -/
macro "rf_dok0" : tactic =>
  `(tactic| repeat' (first | with_reducible assumption | with_reducible apply mul_d | with_reducible apply neg_d | with_reducible apply RF.add_d | with_reducible apply atV_d | with_reducible apply slAtP_d | with_reducible apply sub_d | with_reducible apply const_d | exact one_ne_zero | exact two_ne_zero | (simp only [cRF, sRF, i2cRF, sSL, cSL]; decide)))

lemma mcRF_d {Δ : Poly} {A B bs α β : RF} (dA : A.d ≠ 0) (dB : B.d ≠ 0) (dbs : bs.d ≠ 0)
    (dα : α.d ≠ 0) (dβ : β.d ≠ 0) : (mcRF Δ A B bs α β).d ≠ 0 := by
  simp only [mcRF]; rf_dok0

/-- `rf_dok0` with `mcRF_d`. -/
macro "rf_dok" : tactic =>
  `(tactic| repeat' (first | with_reducible assumption | with_reducible apply mul_d | with_reducible apply neg_d | with_reducible apply RF.add_d | with_reducible apply atV_d | with_reducible apply slAtP_d | with_reducible apply sub_d | with_reducible apply const_d | with_reducible apply mcRF_d | exact one_ne_zero | exact two_ne_zero | (simp only [cRF, sRF, i2cRF, sSL, cSL]; decide)))

/-- A corner kind has `q ≠ 0`. -/
def ckOk : CK → Bool
  | .std => true
  | .c3 _ _ _ q => Nat.blt 0 q
  | .xc _ _ _ q => Nat.blt 0 q

lemma eval_mcRF {Δ : Poly} {A B bs α β : RF} {δ u : ℝ} (h : Ok δ u) (hΔ : BernZ.eval Δ u = δ)
    (dA : A.d ≠ 0) (dB : B.d ≠ 0) (dbs : bs.d ≠ 0) (dα : α.d ≠ 0) (dβ : β.d ≠ 0) :
    (mcRF Δ A B bs α β).eval δ u = mcQ (2 * u / (1 + u ^ 2)) ((1 - u ^ 2) / (1 + u ^ 2))
      (A.eval δ u) (B.eval δ u) (bs.eval δ u) (α.eval δ u) (β.eval δ u) := by
  have h1 : (0 : ℝ) < 1 - u ^ 2 := by nlinarith [h.hu0, h.hu1]
  have hN : (0 : ℝ) < 1 + u ^ 2 := by positivity
  have ec : cRF.eval δ u = (1 - u ^ 2) / (1 + u ^ 2) := by simp [RF.eval, cRF, den, eval_Cp]
  have es : sRF.eval δ u = 2 * u / (1 + u ^ 2) := by simp [RF.eval, sRF, den, eval_Sp]
  have e2 : i2cRF.eval δ u = 1 / (2 * ((1 - u ^ 2) / (1 + u ^ 2))) := by
    simp only [RF.eval, i2cRF, den, eval_Np]; push_cast; field_simp
  simp (disch := rf_dok) only [mcRF, eval_mul h, eval_add h hΔ, eval_neg, eval_const, ec, es, e2]
  simp only [mcQ]
  field_simp
  ring

lemma lebRFs_d (Δ X Y : Poly) {D : ℕ} (hD : 0 < D) (r : RectM) (hmx : modeP r.2.1 = true)
    (hmy : modeP r.2.2.1 = true) (hk : ckOk r.2.2.2 = true) (ax ay : CapA) :
    ∀ t ∈ lebRFs Δ X Y D r ax ay, t.d ≠ 0 := by
  have a := capAU_d Δ X Y (cap := capXm D r) (capXm_d hD r hmx) ax
  have b := capAU_d Δ X Y (cap := capYm D r) (capYm_d hD r hmy) ay
  have cx := capXm_d hD r hmx
  have cy := capYm_d hD r hmy
  have dX : (capX D r.1.1).d ≠ 0 := by simp [capX]; omega
  have dY : (capY D r.1.2.1).d ≠ 0 := by simp [capY]; omega
  have l0 := lebRF_d Δ X Y hD r hmx hmy ax ay
  rcases r with ⟨R, m1, m2, k⟩
  intro t ht
  match k, ht, hk with
  | .std, ht, _ => simp only [lebRFs, List.mem_singleton] at ht; subst ht; exact l0
  | .c3 xa ya ym q, ht, hk =>
    have hq : q ≠ 0 := by simp [ckOk] at hk; omega
    simp only [lebRFs, List.mem_cons, List.not_mem_nil, or_false] at ht
    rcases ht with rfl | rfl <;> (try simp only [mcRF]) <;> rf_dok
  | .xc xa ya ym q, ht, hk =>
    have hq : q ≠ 0 := by simp [ckOk] at hk; omega
    simp only [lebRFs, List.mem_cons, List.not_mem_nil, or_false] at ht
    rcases ht with rfl | rfl
    · simp only [mcRF]; rf_dok
    · exact l0

lemma lebRFs_le {ck : RF → Bool} {D : ℕ} (hD : 0 < D) {σ : Bool} {Δ X Y : Poly} {b0 b1 R : ℕ} {u δ : ℝ}
    (h : VCtx ck Δ X Y σ b0 b1 R u δ) (r : RectM) (hmx : modeP r.2.1 = true)
    (hmy : modeP r.2.2.1 = true) (hk : ckOk r.2.2.2 = true) {ax ay : CapA}
    (gx : SqArea.ghat (Real.sin (2 * Real.arctan u)) (Real.cos (2 * Real.arctan u))
      ((capXm D r).val u (vtx X Y δ u)) ≤ (capAU Δ X Y (capXm D r) ax).eval δ u)
    (gy : SqArea.ghat (Real.sin (2 * Real.arctan u)) (Real.cos (2 * Real.arctan u))
      ((capYm D r).val u (vtx X Y δ u)) ≤ (capAU Δ X Y (capYm D r) ay).eval δ u) :
    ∃ t ∈ lebRFs Δ X Y D r ax ay, t.eval δ u ≤
      (rectT (2 * Real.arctan u) D r).1 * lebPhi (Real.sin (2 * Real.arctan u))
        (Real.cos (2 * Real.arctan u)) (rectT (2 * Real.arctan u) D r).2.2.2
        (aff (rectT (2 * Real.arctan u) D r).2.1 (vtx X Y δ u))
        (aff (rectT (2 * Real.arctan u) D r).2.2.1 (vtx X Y δ u)) := by
  have l0 := lebRF_le hD h r hmx hmy gx gy
  have ex : aff (rectT (2 * Real.arctan u) D r).2.1 (vtx X Y δ u) = (capXm D r).val u (vtx X Y δ u) := by
    rw [val_capXm hD h.hu0 h.hu1 r hmx]; rfl
  have ey : aff (rectT (2 * Real.arctan u) D r).2.2.1 (vtx X Y δ u) = (capYm D r).val u (vtx X Y δ u) := by
    rw [val_capYm hD h.hu0 h.hu1 r hmy]; rfl
  have dax := capAU_d Δ X Y (capXm_d hD r hmx) ax
  have day := capAU_d Δ X Y (capYm_d hD r hmy) ay
  have cx := capXm_d hD r hmx
  have cy := capYm_d hD r hmy
  have hs1 : (sSL 1).d ≠ 0 := by simp [sSL]
  have hc1 : (cSL 1).d ≠ 0 := by simp [cSL]
  have hδ := h.ok.hδ
  rw [ex, ey]
  rw [ex, ey] at l0
  set dx := (capXm D r).val u (vtx X Y δ u) with hdx
  set dy := (capYm D r).val u (vtx X Y δ u) with hdy
  set Gx := (capAU Δ X Y (capXm D r) ax).eval δ u
  set Gy := (capAU Δ X Y (capYm D r) ay).eval δ u
  have evx : (RF.neg (capAU Δ X Y (capXm D r) ax)).eval δ u = -Gx := eval_neg _ _ _
  have evy : (RF.neg (capAU Δ X Y (capYm D r) ay)).eval δ u = -Gy := eval_neg _ _ _
  have tr1 := (trig u).1
  have tr2 := (trig u).2
  rcases r with ⟨Rr, m1, m2, k⟩
  have dX : (capX D Rr.1).d ≠ 0 := by simp [capX]; omega
  have dY : (capY D Rr.2.1).d ≠ 0 := by simp [capY]; omega
  cases k with
  | std =>
    exact ⟨_, List.mem_singleton_self _, l0⟩
  | c3 xa ya ym q =>
    have hq : q ≠ 0 := by simp [ckOk] at hk; omega
    have hq' : (q : ℝ) ≠ 0 := by exact_mod_cast hq
    have eA : (slAtP ((capX D Rr.1).sub (sSL 1)) xa ya q).eval δ u =
        (Rr.1 : ℝ) / D - xa / q + ((1 - u ^ 2) / (1 + u ^ 2) - 2 * u / (1 + u ^ 2)) / 2 := by
      rw [eval_slAtP _ _ _ _ hq, val_sub _ _ dX hs1 h.hu0 h.hu1, val_capX hD h.hu0 h.hu1, val_sSL one_ne_zero,
        tr1, tr2]; push_cast; ring
    have eB : (slAtP (capY D Rr.2.1) xa ya q).eval δ u =
        (Rr.2.1 : ℝ) / D - ya / q + (2 * u / (1 + u ^ 2) + (1 - u ^ 2) / (1 + u ^ 2)) / 2 := by
      rw [eval_slAtP _ _ _ _ hq, val_capY hD h.hu0 h.hu1, tr1, tr2]; ring
    have ebs : (slAtP (capY D Rr.2.1) xa ym q).eval δ u =
        (Rr.2.1 : ℝ) / D - ym / q + (2 * u / (1 + u ^ 2) + (1 - u ^ 2) / (1 + u ^ 2)) / 2 := by
      rw [eval_slAtP _ _ _ _ hq, val_capY hD h.hu0 h.hu1, tr1, tr2]; ring
    have eα : (((capXm D (Rr, m1, m2, .c3 xa ya ym q)).sub (sSL 1)).atV Δ X Y).eval δ u = dx - 2 * u / (1 + u ^ 2) := by
      rw [eval_atV _ Δ X Y h.hΔ hδ, val_sub _ _ cx hs1 h.hu0 h.hu1, val_sSL one_ne_zero, hdx]; simp [vtx]
    have eβ : ((capYm D (Rr, m1, m2, .c3 xa ya ym q)).atV Δ X Y).eval δ u = dy := by
      rw [eval_atV _ Δ X Y h.hΔ hδ, hdy]; rfl
    have emc := eval_mcRF (A := slAtP ((capX D Rr.1).sub (sSL 1)) xa ya q) (B := slAtP (capY D Rr.2.1) xa ya q)
      (bs := slAtP (capY D Rr.2.1) xa ym q)
      (α := ((capXm D (Rr, m1, m2, .c3 xa ya ym q)).sub (sSL 1)).atV Δ X Y)
      (β := (capYm D (Rr, m1, m2, .c3 xa ya ym q)).atV Δ X Y) h.ok h.hΔ
      (slAtP_d (sub_d dX hs1) hq _ _) (slAtP_d dY hq _ _) (slAtP_d dY hq _ _) (atV_d (sub_d cx hs1) _ _ _)
      (atV_d cy _ _ _)
    rw [eA, eB, ebs, eα, eβ] at emc
    simp only [lebRFs, rectT, kindK, lebPhi, List.mem_cons, List.not_mem_nil, or_false, exists_eq_or_imp,
      exists_eq_left]
    simp only [tr1, tr2] at gx gy ⊢
    have ew : ∀ z : ℝ, ((((Rr.2.2.2.2 : ℕ) : ℤ) : ℝ) / ((1 : ℕ) : ℝ)) * z = (Rr.2.2.2.2 : ℝ) * z := by
      intro z; push_cast; ring
    have e1 : (((1 : ℤ) : ℝ) / ((1 : ℕ) : ℝ)) = 1 := by norm_num
    rcases le_total (1 - SqArea.ghat (2 * u / (1 + u ^ 2)) ((1 - u ^ 2) / (1 + u ^ 2)) dx -
        SqArea.ghat (2 * u / (1 + u ^ 2)) ((1 - u ^ 2) / (1 + u ^ 2)) dy +
        mcQ (2 * u / (1 + u ^ 2)) ((1 - u ^ 2) / (1 + u ^ 2))
          ((Rr.1 : ℝ) / D - xa / q + ((1 - u ^ 2) / (1 + u ^ 2) - 2 * u / (1 + u ^ 2)) / 2)
          ((Rr.2.1 : ℝ) / D - ya / q + (2 * u / (1 + u ^ 2) + (1 - u ^ 2) / (1 + u ^ 2)) / 2)
          ((Rr.2.1 : ℝ) / D - ym / q + (2 * u / (1 + u ^ 2) + (1 - u ^ 2) / (1 + u ^ 2)) / 2)
          (dx - 2 * u / (1 + u ^ 2)) dy)
      (1 - SqArea.ghat (2 * u / (1 + u ^ 2)) ((1 - u ^ 2) / (1 + u ^ 2)) dx) with hle | hle
    · left
      rw [min_eq_left hle]
      simp (disch := rf_dok) only [eval_mul h.ok, eval_add h.ok h.hΔ, eval_const, evx, evy]
      rw [emc, ew, e1]
      exact mul_le_mul_of_nonneg_left (by linarith) (Nat.cast_nonneg _)
    · right
      rw [min_eq_right hle]
      simp (disch := rf_dok) only [eval_mul h.ok, eval_add h.ok h.hΔ, eval_const, evx]
      rw [ew, e1]
      exact mul_le_mul_of_nonneg_left (by linarith) (Nat.cast_nonneg _)
  | xc xa ya ym q =>
    have hq : q ≠ 0 := by simp [ckOk] at hk; omega
    have hq' : (q : ℝ) ≠ 0 := by exact_mod_cast hq
    have eA : (slAtP (capX D Rr.1) xa ya q).eval δ u =
        (Rr.1 : ℝ) / D - xa / q + ((1 - u ^ 2) / (1 + u ^ 2) + 2 * u / (1 + u ^ 2)) / 2 := by
      rw [eval_slAtP _ _ _ _ hq, val_capX hD h.hu0 h.hu1, tr1, tr2]
    have eB : (slAtP ((capY D Rr.2.1).sub (cSL 1)) xa ya q).eval δ u =
        (Rr.2.1 : ℝ) / D - ya / q - ((1 - u ^ 2) / (1 + u ^ 2) - 2 * u / (1 + u ^ 2)) / 2 := by
      rw [eval_slAtP _ _ _ _ hq, val_sub _ _ dY hc1 h.hu0 h.hu1, val_capY hD h.hu0 h.hu1, val_cSL one_ne_zero,
        tr1, tr2]; push_cast; ring
    have ebs : (slAtP ((capY D Rr.2.1).sub (cSL 1)) xa ym q).eval δ u =
        (Rr.2.1 : ℝ) / D - ym / q - ((1 - u ^ 2) / (1 + u ^ 2) - 2 * u / (1 + u ^ 2)) / 2 := by
      rw [eval_slAtP _ _ _ _ hq, val_sub _ _ dY hc1 h.hu0 h.hu1, val_capY hD h.hu0 h.hu1, val_cSL one_ne_zero,
        tr1, tr2]; push_cast; ring
    have eα : ((capXm D (Rr, m1, m2, .xc xa ya ym q)).atV Δ X Y).eval δ u = dx := by
      rw [eval_atV _ Δ X Y h.hΔ hδ, hdx]; rfl
    have eβ : (((capYm D (Rr, m1, m2, .xc xa ya ym q)).sub (cSL 1)).atV Δ X Y).eval δ u =
        dy - (1 - u ^ 2) / (1 + u ^ 2) := by
      rw [eval_atV _ Δ X Y h.hΔ hδ, val_sub _ _ cy hc1 h.hu0 h.hu1, val_cSL one_ne_zero, hdy]; simp [vtx]
    have emc := eval_mcRF (A := slAtP (capX D Rr.1) xa ya q) (B := slAtP ((capY D Rr.2.1).sub (cSL 1)) xa ya q)
      (bs := slAtP ((capY D Rr.2.1).sub (cSL 1)) xa ym q)
      (α := (capXm D (Rr, m1, m2, .xc xa ya ym q)).atV Δ X Y)
      (β := ((capYm D (Rr, m1, m2, .xc xa ya ym q)).sub (cSL 1)).atV Δ X Y) h.ok h.hΔ
      (slAtP_d dX hq _ _) (slAtP_d (sub_d dY hc1) hq _ _) (slAtP_d (sub_d dY hc1) hq _ _) (atV_d cx _ _ _)
      (atV_d (sub_d cy hc1) _ _ _)
    rw [eA, eB, ebs, eα, eβ] at emc
    simp only [lebRFs, rectT, kindK, lebPhi, List.mem_cons, List.not_mem_nil, or_false, exists_eq_or_imp,
      exists_eq_left]
    simp only [tr1, tr2] at gx gy l0 ⊢
    have ew : ∀ z : ℝ, ((((Rr.2.2.2.2 : ℕ) : ℤ) : ℝ) / ((1 : ℕ) : ℝ)) * z = (Rr.2.2.2.2 : ℝ) * z := by
      intro z; push_cast; ring
    have e1 : (((1 : ℤ) : ℝ) / ((1 : ℕ) : ℝ)) = 1 := by norm_num
    rcases le_total (1 - SqArea.ghat (2 * u / (1 + u ^ 2)) ((1 - u ^ 2) / (1 + u ^ 2)) dy +
        mcQ (2 * u / (1 + u ^ 2)) ((1 - u ^ 2) / (1 + u ^ 2))
          ((Rr.1 : ℝ) / D - xa / q + ((1 - u ^ 2) / (1 + u ^ 2) + 2 * u / (1 + u ^ 2)) / 2)
          ((Rr.2.1 : ℝ) / D - ya / q - ((1 - u ^ 2) / (1 + u ^ 2) - 2 * u / (1 + u ^ 2)) / 2)
          ((Rr.2.1 : ℝ) / D - ym / q - ((1 - u ^ 2) / (1 + u ^ 2) - 2 * u / (1 + u ^ 2)) / 2)
          dx (dy - (1 - u ^ 2) / (1 + u ^ 2)))
      (1 - SqArea.ghat (2 * u / (1 + u ^ 2)) ((1 - u ^ 2) / (1 + u ^ 2)) dx -
        SqArea.ghat (2 * u / (1 + u ^ 2)) ((1 - u ^ 2) / (1 + u ^ 2)) dy) with hle | hle
    · left
      rw [min_eq_left hle]
      simp (disch := rf_dok) only [eval_mul h.ok, eval_add h.ok h.hΔ, eval_const, evy]
      rw [emc, ew, e1]
      exact mul_le_mul_of_nonneg_left (by linarith) (Nat.cast_nonneg _)
    · right
      rw [min_eq_right hle]
      exact l0

lemma sproc_d (Δ X Y : Poly) {sp : Split} (hq : sp.q.d ≠ 0) (hm : sp.dm ≠ 0) (hp : sp.dp ≠ 0)
    (b : Bool) : (sproc Δ X Y sp b).d ≠ 0 := by
  cases b <;> simp [sproc, RF.neg, RF.mul, RF.const, SL.atV, hq, hm, hp]

lemma sproc_le {ck : RF → Bool} {σ : Bool} {Δ X Y : Poly} {b0 b1 R : ℕ} {u δ : ℝ} (h : VCtx ck Δ X Y σ b0 b1 R u δ)
    {sp : Split} (hq : sp.q.d ≠ 0) (hm : sp.dm ≠ 0) (hp : sp.dp ≠ 0) :
    (sproc Δ X Y sp (decide (0 ≤ sp.q.val u (vtx X Y δ u)))).eval δ u ≤ 0 := by
  have e := eval_atV sp.q Δ X Y h.hΔ h.ok.hδ
  by_cases hs : 0 ≤ sp.q.val u (vtx X Y δ u)
  · simp only [hs, decide_true, sproc, if_true]
    rw [eval_neg, eval_mul h.ok (by simp [RF.const, hp]) (by simpa [SL.atV] using hq), eval_const, e]
    have : (0 : ℝ) ≤ (sp.np : ℤ) / (sp.dp : ℝ) := by push_cast; positivity
    have h2 : 0 ≤ sp.q.val u (eval X u / δ, eval Y u / δ) := hs
    nlinarith
  · simp only [hs, decide_false, sproc, Bool.false_eq_true, if_false]
    rw [eval_mul h.ok (by simp [RF.const, hm]) (by simpa [SL.atV] using hq), eval_const, e]
    have : (0 : ℝ) ≤ (sp.nm : ℤ) / (sp.dm : ℝ) := by push_cast; positivity
    have h2 : sp.q.val u (eval X u / δ, eval Y u / δ) < 0 := not_le.mp hs
    nlinarith

lemma list_sum_nonpos : ∀ (l : List ℝ), (∀ y ∈ l, y ≤ 0) → l.sum ≤ 0
  | [], _ => by simp
  | a :: l, h => by
    simp only [List.sum_cons]
    linarith [h a List.mem_cons_self, list_sum_nonpos l fun y hy => h y (List.mem_cons_of_mem _ hy)]

/-- **Soundness of the total test.** -/
lemma totOk_sound {ck : RF → Bool} {σ : Bool} {Δ X Y : Poly} {b0 b1 R : ℕ} {u δ : ℝ} (h : VCtx ck Δ X Y σ b0 b1 R u δ)
    {splits : List Split} (hsq : ∀ sp ∈ splits, sp.q.d ≠ 0) {fcs : List FCert} {T : RF}
    (hT : T.d ≠ 0) (hok : totOk ck σ Δ X Y b0 b1 R splits (patAt splits u (vtx X Y δ u)) fcs T = true) :
    0 ≤ T.eval δ u := by
  simp only [totOk, Bool.or_eq_true, List.any_eq_true] at hok
  rcases hok with hok | ⟨f, _, hf⟩
  · exact ckRF_sound hok h hT
  simp only [fcOk, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true, beq_iff_eq] at hf
  obtain ⟨⟨⟨⟨⟨hk, hq⟩, hz⟩, hg⟩, hTc⟩, hc⟩ := hf
  set q := splitAt splits f.k
  have hqd : q.d ≠ 0 := by
    have : q ∈ splits.map Split.q := by
      simp only [q, splitAt, List.getD_eq_getElem _ _ hk]; exact List.mem_map_of_mem (List.getElem_mem _)
    obtain ⟨sp, hsp, hspq⟩ := List.mem_map.mp this
    rw [← hspq]; exact hsq sp hsp
  -- `g₁ > 0`
  have hg1 : 0 < eval f.g1 u := by
    rw [eval_take_drop f.g1 f.m (List.all_eq_true.mpr fun x hx => by simpa using hz x hx) u]
    exact mul_pos (pow_pos h.hu0 _) (pos_of_checkPos hg h.hR h.hb0 h.hb1)
  have eq1 := eval_of_peqb hq u
  have eq2 := eval_of_peqb hTc u
  rw [BernZ.eval_mul] at eq1 eq2
  set c1 := pdiv (snum σ T) f.G
  have hqs := snum_sign h (r := q.atV Δ X Y) (by simpa [SL.atV] using hqd)
  have hTs := snum_sign h hT
  rw [eval_atV _ _ _ _ h.hΔ h.ok.hδ] at hqs
  rw [patAt_getD _ _ _ hk] at hc
  refine hTs.1.mpr ?_
  rw [eq2]
  by_cases hb : 0 ≤ q.val u (vtx X Y δ u)
  · rw [show decide (0 ≤ q.val u (vtx X Y δ u)) = true from decide_eq_true hb, if_pos rfl] at hc
    have hc' := BernZ.nonneg_of_check hc h.hR h.hb0 h.hb1
    have hG : 0 ≤ eval f.G u := by
      have := hqs.1.mp (by simpa [vtx] using hb)
      rw [eq1] at this
      exact nonneg_of_mul_nonneg_left this hg1
    exact mul_nonneg hG hc'
  · rw [show decide (0 ≤ q.val u (vtx X Y δ u)) = false from decide_eq_false hb,
      if_neg (by simp)] at hc
    have hc' := BernZ.nonneg_of_check hc h.hR h.hb0 h.hb1
    rw [eval_smul] at hc'; push_cast at hc'
    have hG : eval f.G u < 0 := by
      have := hqs.2.mp (by simpa [vtx] using not_le.mp hb)
      rw [eq1] at this
      by_contra hc2; push_neg at hc2
      have := mul_nonneg hc2 hg1.le; linarith
    nlinarith

/-- **Soundness of the test at a vertex**: `W ≤ fE(v)`. -/
theorem vertOk_sound {ck : RF → Bool} {D W : ℕ} (hD : 0 < D) {σ : Bool} {Δ X Y : Poly} {b0 b1 R : ℕ} {u δ : ℝ}
    (h : VCtx ck Δ X Y σ b0 b1 R u δ) {chs cvs : List SegE} {crs : List RectM}
    (hch : ∀ e ∈ chs, e.1 < e.2.2.1) (hcv : ∀ e ∈ cvs, e.2.1 < e.2.2.2.1)
    {hbx vbx : List (List ℕ × List ℕ)} (hbd : BoxDom D u (vtx X Y δ u) chs cvs hbx vbx) {c : VCert}
    (hsq : ∀ sp ∈ c.splits, sp.q.d ≠ 0) (hmd : ∀ r ∈ crs, modeP r.2.1 = true ∧ modeP r.2.2.1 = true ∧ ckOk r.2.2.2 = true)
    (hok : vertOk ck D W σ Δ X Y b0 b1 R chs cvs crs hbx vbx c = true) :
    (W : ℝ) ≤ fE (Real.sin (2 * Real.arctan u)) (Real.cos (2 * Real.arctan u))
      (chs.map (hsegT (2 * Real.arctan u) D) ++ cvs.map (vsegT (2 * Real.arctan u) D))
      (crs.map (rectT (2 * Real.arctan u) D)) (vtx X Y δ u) := by
  simp only [vertOk, Bool.and_eq_true, beq_iff_eq, List.all_eq_true] at hok
  obtain ⟨⟨⟨⟨⟨⟨⟨⟨⟨lh, lv⟩, l1⟩, l2⟩, l3⟩, hsp⟩, hH⟩, hV⟩, hL⟩, hpat⟩ := hok
  set θ := 2 * Real.arctan u
  set v := vtx X Y δ u
  set pat := patAt c.splits u v with hpatdef
  have hpm : pat ∈ pats c.splits.length := by
    have := mem_pats pat; simpa [pat, patAt] using this
  obtain ⟨⟨⟨nh, nv⟩, nl⟩, htot⟩ := by simpa only [Bool.and_eq_true, List.all_eq_true] using hpat pat hpm
  have hspd : ∀ sp ∈ c.splits, sp.dm ≠ 0 ∧ sp.dp ≠ 0 := fun sp hs => by
    have := hsp sp hs; simp only [Bool.and_eq_true, bne_iff_ne, ne_eq] at this; exact this
  -- every term has a consistent alternative below it
  have hH' : ∀ q ∈ (chs.zip hbx).zip c.hc, ∃ t ∈ hAltsP Δ X Y D pat q, t.eval δ u ≤
      (hsegT θ D q.1.1).1 * max 0 (clampMin (hsegT θ D q.1.1).2.1 (hsegT θ D q.1.1).2.2 v) := by
    intro q hq
    have hq1 := (List.of_mem_zip hq).1
    have hx := hch q.1.1 (List.of_mem_zip hq1).1
    have hDr : (0 : ℝ) < D := by exact_mod_cast hD
    have hAB : (q.1.1.1 : ℝ) / D < q.1.1.2.2.1 / D := div_lt_div_of_pos_right (by exact_mod_cast hx) hDr
    obtain ⟨x, hxm, hxt⟩ := List.any_eq_true.mp (nh q.2 (List.of_mem_zip hq).2)
    obtain ⟨t, ht, hle⟩ := segC_ge h (sc := x.1)
      (mul_nonneg (by simp only [hsegT]; exact div_nonneg (Nat.cast_nonneg _) (by linarith))
        (le_max_left _ _)) ((hH q hq) x hxm) (hbd.1 q.1 hq1)
      (fun Ua La h1 h2 h3 h4 du dl => hseg_dom hD h hx h1 h2 h3 h4 du dl)
      (hd_hUps hD q.1.1) (hd_hLos hD q.1.1)
    exact ⟨t, List.mem_flatMap.mpr ⟨x, List.mem_filter.mpr ⟨hxm, hxt⟩, ht⟩, hle⟩
  have hV' : ∀ q ∈ (cvs.zip vbx).zip c.vc, ∃ t ∈ vAltsP Δ X Y D pat q, t.eval δ u ≤
      (vsegT θ D q.1.1).1 * max 0 (clampMin (vsegT θ D q.1.1).2.1 (vsegT θ D q.1.1).2.2 v) := by
    intro q hq
    have hq1 := (List.of_mem_zip hq).1
    have hx := hcv q.1.1 (List.of_mem_zip hq1).1
    have hDr : (0 : ℝ) < D := by exact_mod_cast hD
    have hAB : (q.1.1.2.1 : ℝ) / D < q.1.1.2.2.2.1 / D :=
      div_lt_div_of_pos_right (by exact_mod_cast hx) hDr
    obtain ⟨x, hxm, hxt⟩ := List.any_eq_true.mp (nv q.2 (List.of_mem_zip hq).2)
    obtain ⟨t, ht, hle⟩ := segC_ge h (sc := x.1)
      (mul_nonneg (by simp only [vsegT]; exact div_nonneg (Nat.cast_nonneg _) (by linarith))
        (le_max_left _ _)) ((hV q hq) x hxm) (hbd.2 q.1 hq1)
      (fun Ua La h1 h2 h3 h4 du dl => vseg_dom hD h hx h1 h2 h3 h4 du dl)
      (hd_vUps hD q.1.1) (hd_vLos hD q.1.1)
    exact ⟨t, List.mem_flatMap.mpr ⟨x, List.mem_filter.mpr ⟨hxm, hxt⟩, ht⟩, hle⟩
  have hL' : ∀ p ∈ crs.zip c.lc, ∃ t ∈ lAltsP Δ X Y D pat p, t.eval δ u ≤
      (rectT θ D p.1).1 * lebPhi (Real.sin θ) (Real.cos θ) (rectT θ D p.1).2.2.2 (aff (rectT θ D p.1).2.1 v)
        (aff (rectT θ D p.1).2.2.1 v) := by
    intro p hp
    have hk := hL p hp
    have hn := nl p.2 (List.of_mem_zip hp).2
    obtain ⟨ax, hax, hxt⟩ := List.any_eq_true.mp hn.1
    obtain ⟨ay, hay, hyt⟩ := List.any_eq_true.mp hn.2
    have hm := hmd p.1 (List.of_mem_zip hp).1
    have gx := capA_ge h (capXm_d hD p.1 hm.1) (hk.1 ax hax) hxt
    have gy := capA_ge h (capYm_d hD p.1 hm.2.1) (hk.2 ay hay) hyt
    obtain ⟨t, ht, hle⟩ := lebRFs_le hD h p.1 hm.1 hm.2.1 hm.2.2 gx gy
    exact ⟨t, List.mem_flatMap.mpr ⟨ax, List.mem_filter.mpr ⟨hax, hxt⟩,
      List.mem_flatMap.mpr ⟨ay, List.mem_filter.mpr ⟨hay, hyt⟩, ht⟩⟩, hle⟩
  obtain ⟨c1, hc1, hs1⟩ := exists_comb_zip (f := fun t => t.eval δ u) _ _ _ hH'
  obtain ⟨c2, hc2, hs2⟩ := exists_comb_zip (f := fun t => t.eval δ u) _ _ _ hV'
  obtain ⟨c3, hc3, hs3⟩ := exists_comb_zip (f := fun t => t.eval δ u) _ _ _ hL'
  have hcomb0 := cprod_append _ _ (cprod_append _ _ hc1 hc2) hc3
  obtain ⟨cc, hcomb, hperm⟩ := exists_reord hcomb0
  -- constants
  have dAll : ∀ l ∈ ((chs.zip hbx).zip c.hc).map (hAltsP Δ X Y D pat) ++
      ((cvs.zip vbx).zip c.vc).map (vAltsP Δ X Y D pat) ++
      (crs.zip c.lc).map (lAltsP Δ X Y D pat), ∀ r ∈ l, r.d ≠ 0 := by
    intro l hl r hr
    simp only [List.mem_append, List.mem_map] at hl
    rcases hl with (⟨q, hq, rfl⟩ | ⟨q, hq, rfl⟩) | ⟨p, hp, rfl⟩
    · have hx := hch q.1.1 (List.of_mem_zip (List.of_mem_zip hq).1).1
      obtain ⟨x, _, hr⟩ := List.mem_flatMap.mp hr
      exact segCAlts_d hD (by omega) (hd_hUps hD q.1.1) (hd_hLos hD q.1.1) _ _ r hr
    · have hx := hcv q.1.1 (List.of_mem_zip (List.of_mem_zip hq).1).1
      obtain ⟨x, _, hr⟩ := List.mem_flatMap.mp hr
      exact segCAlts_d hD (by omega) (hd_vUps hD q.1.1) (hd_vLos hD q.1.1) _ _ r hr
    · obtain ⟨ax, _, hr⟩ := List.mem_flatMap.mp hr
      obtain ⟨ay, _, hr⟩ := List.mem_flatMap.mp hr
      have hm := hmd p.1 (List.of_mem_zip hp).1
      exact lebRFs_d Δ X Y hD p.1 hm.1 hm.2.1 hm.2.2 ax ay r hr
  have dS : ∀ r ∈ (c.splits.zip pat).map (fun x => sproc Δ X Y x.1 x.2), r.d ≠ 0 := by
    intro r hr
    obtain ⟨x, hx, rfl⟩ := List.mem_map.mp hr
    have hs := (List.of_mem_zip hx).1
    exact sproc_d Δ X Y (hsq x.1 hs) (hspd x.1 hs).1 (hspd x.1 hs).2 x.2
  have hall : ∀ r ∈ cc ++ (c.splits.zip pat).map (fun x => sproc Δ X Y x.1 x.2) ++
      [RF.const (-(W : ℤ)) 1], r.d ≠ 0 := by
    intro r hr
    rcases List.mem_append.mp hr with hr | hr
    · rcases List.mem_append.mp hr with hr | hr
      · exact mem_cprod (P := fun r => r.d ≠ 0) _ dAll _ hcomb0 r (hperm.mem_iff.mp hr)
      · exact dS r hr
    · simp at hr; subst hr; simp [RF.const]
  have hsumP : ((cc.map fun t => t.eval δ u)).sum = (((c1 ++ c2 ++ c3).map fun t => t.eval δ u)).sum :=
    (hperm.map _).sum_eq
  have h0 := totOk_sound h hsq (sumRF_d Δ _ (by simpa [List.append_assoc] using hall)) (htot _ hcomb)
  rw [eval_sumRF h.ok h.hΔ _ (by simpa [List.append_assoc] using hall)] at h0
  -- the S-procedure terms are `≤ 0`
  have hsp0 : (((c.splits.zip pat).map (fun x => sproc Δ X Y x.1 x.2)).map (fun r => r.eval δ u)).sum ≤ 0 := by
    refine list_sum_nonpos _ fun y hy => ?_
    simp only [List.map_map, List.mem_map] at hy
    obtain ⟨x, hx, rfl⟩ := hy
    have hs := (List.of_mem_zip hx).1
    have hxp : x.2 = decide (0 ≤ x.1.q.val u v) := by
      obtain ⟨k, hk, hkx⟩ := List.mem_iff_getElem.mp hx
      simp only [List.getElem_zip] at hkx
      rw [← hkx]
      simp [pat, patAt]
    simp only [Function.comp]
    rw [hxp]
    exact sproc_le h (hsq x.1 hs) (hspd x.1 hs).1 (hspd x.1 hs).2
  simp only [List.map_append, List.sum_append, List.map_cons, List.map_nil, List.sum_cons,
    List.sum_nil, eval_const] at h0
  have z1 := sum_map_zip_fst (chs.zip hbx) c.hc
    (fun q => (hsegT θ D q.1).1 * max 0 (clampMin (hsegT θ D q.1).2.1 (hsegT θ D q.1).2.2 v))
    (by simp [l1, lh])
  have z1' := sum_map_zip_fst chs hbx
    (fun e => (hsegT θ D e).1 * max 0 (clampMin (hsegT θ D e).2.1 (hsegT θ D e).2.2 v)) lh
  have z2 := sum_map_zip_fst (cvs.zip vbx) c.vc
    (fun q => (vsegT θ D q.1).1 * max 0 (clampMin (vsegT θ D q.1).2.1 (vsegT θ D q.1).2.2 v))
    (by simp [l2, lv])
  have z2' := sum_map_zip_fst cvs vbx
    (fun e => (vsegT θ D e).1 * max 0 (clampMin (vsegT θ D e).2.1 (vsegT θ D e).2.2 v)) lv
  have z3 := sum_map_zip_fst crs c.lc
    (fun r => (rectT θ D r).1 * lebPhi (Real.sin θ) (Real.cos θ) (rectT θ D r).2.2.2 (aff (rectT θ D r).2.1 v)
      (aff (rectT θ D r).2.2.1 v)) l3
  rw [z1, z1'] at hs1
  rw [z2, z2'] at hs2
  rw [z3] at hs3
  simp only [fE, List.map_append, List.sum_append, List.map_map]
  simp only [List.map_append, List.sum_append] at hsumP
  simp only [Function.comp_def, List.map_map] at h0 hs1 hs2 hs3 hsp0 hsumP ⊢
  push_cast at h0
  linarith


end LemmaEVert

end SquarePacking
