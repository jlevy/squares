import Sqpack.LemmaE
import Sqpack.RatU

/-!
# Lemma E in `u = tan(θ/2)`: scaled lines with polynomial coefficients

Every affine form of Lemma E (a chord end, a segment end, a cap depth) is, at `θ = 2 arctan u`,
`aff P(u) c / (C^i S^j N^k d)` for an integer polynomial triple `P` (`PL`) and a positive
denominator (`C = 1 − u²`, `S = 2u`, `N = 1 + u²`): a *scaled line* `SL`.  This file

* gives the scaled lines of the chord ends of a horizontal (`hTA … hTD`) and a vertical
  (`vLX … vUY`) grid line, of the segment ends, and of the cap depths, and proves them equal to the
  real forms of `LemmaE.lean` (`val_hTA` …);
* closes `SL` under subtraction (`SL.sub`, `val_sub`), so every form `up − lo` of a segment is a
  scaled line (`formsSL`), hence a positive multiple of its numerator line (`posMul_of_SL`);
* evaluates a scaled line at a vertex `(X/Δ, Y/Δ)` as an `RF` (`SL.atV`, `eval_atV`).
-/

namespace SquarePacking

namespace LemmaEPoly

open BernZ RatU ChordE LemmaE

/-- A triple of integer polynomials in `u`. -/
abbrev PL := Poly × Poly × Poly

noncomputable def evalPL (P : PL) (u : ℝ) : ℝ × ℝ × ℝ := (eval P.1 u, eval P.2.1 u, eval P.2.2 u)

def addPL (P Q : PL) : PL := (BernZ.add P.1 Q.1, BernZ.add P.2.1 Q.2.1, BernZ.add P.2.2 Q.2.2)
def mulPL (p : Poly) (P : PL) : PL := (BernZ.mul p P.1, BernZ.mul p P.2.1, BernZ.mul p P.2.2)
def negPL (P : PL) : PL := (smul (-1) P.1, smul (-1) P.2.1, smul (-1) P.2.2)

lemma aff_addPL (P Q : PL) (u : ℝ) (c : ℝ × ℝ) :
    aff (evalPL (addPL P Q) u) c = aff (evalPL P u) c + aff (evalPL Q u) c := by
  simp only [aff, evalPL, addPL, BernZ.eval_add]; ring

lemma aff_mulPL (p : Poly) (P : PL) (u : ℝ) (c : ℝ × ℝ) :
    aff (evalPL (mulPL p P) u) c = eval p u * aff (evalPL P u) c := by
  simp only [aff, evalPL, mulPL, BernZ.eval_mul]; ring

lemma aff_negPL (P : PL) (u : ℝ) (c : ℝ × ℝ) : aff (evalPL (negPL P) u) c = -aff (evalPL P u) c := by
  simp only [aff, evalPL, negPL, BernZ.eval_smul]; push_cast; ring

/-! ## Scaled lines -/

/-- `aff P(u) c / (C^i S^j N^k d)`. -/
structure SL where
  P : PL
  i : ℕ
  j : ℕ
  k : ℕ
  d : ℕ
  deriving DecidableEq

/-- The positive denominator of a scaled line. -/
noncomputable def sden (L : SL) (u : ℝ) : ℝ := (1 - u ^ 2) ^ L.i * (2 * u) ^ L.j * (1 + u ^ 2) ^ L.k * L.d

noncomputable def SL.val (L : SL) (u : ℝ) (c : ℝ × ℝ) : ℝ := aff (evalPL L.P u) c / sden L u

/-- The polynomial `C^i S^j N^k d`. -/
def sdenP (L : SL) : Poly :=
  BernZ.mul (ppow Cp L.i) (BernZ.mul (ppow Sp L.j) (BernZ.mul (ppow Np L.k) [(L.d : ℤ)]))

lemma eval_sdenP (L : SL) (u : ℝ) : eval (sdenP L) u = sden L u := by
  simp only [sdenP, BernZ.eval_mul, eval_ppow, eval_Cp, eval_Sp, eval_Np, sden, eval_cons, eval_nil,
    mul_zero, add_zero]
  push_cast
  ring

lemma sden_pos (L : SL) (hd : L.d ≠ 0) {u : ℝ} (hu0 : 0 < u) (hu1 : u < 1) : 0 < sden L u := by
  have h1 : (0 : ℝ) < 1 - u ^ 2 := by nlinarith
  have h4 : (0 : ℝ) < L.d := by exact_mod_cast Nat.pos_of_ne_zero hd
  unfold sden; positivity

/-- `L − M`. -/
def SL.sub (L M : SL) : SL :=
  ⟨addPL (mulPL (sdenP M) L.P) (negPL (mulPL (sdenP L) M.P)), L.i + M.i, L.j + M.j, L.k + M.k,
    L.d * M.d⟩

lemma val_sub (L M : SL) (hL : L.d ≠ 0) (hM : M.d ≠ 0) {u : ℝ} (hu0 : 0 < u) (hu1 : u < 1)
    (c : ℝ × ℝ) : (L.sub M).val u c = L.val u c - M.val u c := by
  have a := (sden_pos L hL hu0 hu1).ne'
  have b := (sden_pos M hM hu0 hu1).ne'
  have e : sden (L.sub M) u = sden L u * sden M u := by
    simp only [sden, SL.sub]; push_cast; ring
  simp only [SL.val, e]
  rw [show (L.sub M).P = addPL (mulPL (sdenP M) L.P) (negPL (mulPL (sdenP L) M.P)) from rfl,
    aff_addPL, aff_negPL, aff_mulPL, aff_mulPL, eval_sdenP, eval_sdenP]
  field_simp
  ring

/-- The constant `n/d`. -/
def SL.cst (n : ℤ) (d : ℕ) : SL := ⟨([0], [0], [n]), 0, 0, 0, d⟩

lemma val_cst (n : ℤ) (d : ℕ) (u : ℝ) (c : ℝ × ℝ) : (SL.cst n d).val u c = n / d := by
  simp [SL.val, SL.cst, sden, aff, evalPL]

/-- A scaled line with `d ≠ 0` is a positive multiple of its numerator line. -/
lemma posMul_of_SL {Ls : List (ℝ × ℝ × ℝ)} {F : ℝ × ℝ × ℝ} (L : SL) (hd : L.d ≠ 0) {u : ℝ}
    (hu0 : 0 < u) (hu1 : u < 1) (hF : ∀ c, aff F c = L.val u c) (hmem : evalPL L.P u ∈ Ls) :
    PosMul Ls F :=
  ⟨_, hmem, (sden L u)⁻¹, inv_pos.mpr (sden_pos L hd hu0 hu1), fun c => by
    rw [hF, SL.val, div_eq_inv_mul]⟩

/-! ## The value at a vertex -/

/-- `aff P (X/Δ, Y/Δ) = (a X + b Y + k Δ)/Δ`, divided by the scale: an `RF` with `e = 1`. -/
def SL.atV (L : SL) (Δ X Y : Poly) : RF :=
  ⟨BernZ.add (BernZ.add (BernZ.mul L.P.1 X) (BernZ.mul L.P.2.1 Y)) (BernZ.mul L.P.2.2 Δ),
    1, L.i, L.j, L.k, L.d⟩

lemma eval_atV (L : SL) (Δ X Y : Poly) {δ u : ℝ} (hΔ : eval Δ u = δ) (hδ : δ ≠ 0) :
    (L.atV Δ X Y).eval δ u = L.val u (eval X u / δ, eval Y u / δ) := by
  simp only [RF.eval, SL.atV, den, SL.val, sden, aff, evalPL, BernZ.eval_add, BernZ.eval_mul, hΔ]
  field_simp

/-! ## The chord ends and the cap depths -/

section lines

variable (D : ℕ)

/-- `2D·p`. -/
def tw (p : Poly) : Poly := smul (2 * D) p

/-- Horizontal line `y = Y/D`: `t_A = aff(2DC, 2DS, −DN − 2YS)/(2DC)`, `t_B = aff(2DS, −2DC,
2YC − DN)/(2DS)`, `t_C = aff(2DC, 2DS, DN − 2YS)/(2DC)`, `t_D = aff(2DS, −2DC, 2YC + DN)/(2DS)`. -/
def hTA (Y : ℕ) : SL := ⟨(tw D Cp, tw D Sp, BernZ.add (smul (-(D : ℤ)) Np) (smul (-2 * Y) Sp)),
  1, 0, 0, 2 * D⟩
def hTB (Y : ℕ) : SL := ⟨(tw D Sp, smul (-1) (tw D Cp), BernZ.add (smul (2 * Y) Cp) (smul (-(D : ℤ)) Np)),
  0, 1, 0, 2 * D⟩
def hTC (Y : ℕ) : SL := ⟨(tw D Cp, tw D Sp, BernZ.add (smul (D : ℤ) Np) (smul (-2 * Y) Sp)),
  1, 0, 0, 2 * D⟩
def hTD (Y : ℕ) : SL := ⟨(tw D Sp, smul (-1) (tw D Cp), BernZ.add (smul (2 * Y) Cp) (smul (D : ℤ) Np)),
  0, 1, 0, 2 * D⟩

/-- Vertical line `x = X/D`: `lowX = aff(2DC, 2DS, −DN − 2XC)/(2DS)`, `upX = aff(2DC, 2DS,
DN − 2XC)/(2DS)`, `lowY = aff(−2DS, 2DC, 2XS − DN)/(2DC)`, `upY = aff(−2DS, 2DC, 2XS + DN)/(2DC)`. -/
def vLXs (X : ℕ) : SL := ⟨(tw D Cp, tw D Sp, BernZ.add (smul (-(D : ℤ)) Np) (smul (-2 * X) Cp)),
  0, 1, 0, 2 * D⟩
def vUXs (X : ℕ) : SL := ⟨(tw D Cp, tw D Sp, BernZ.add (smul (D : ℤ) Np) (smul (-2 * X) Cp)),
  0, 1, 0, 2 * D⟩
def vLYs (X : ℕ) : SL := ⟨(smul (-1) (tw D Sp), tw D Cp, BernZ.add (smul (2 * X) Sp) (smul (-(D : ℤ)) Np)),
  1, 0, 0, 2 * D⟩
def vUYs (X : ℕ) : SL := ⟨(smul (-1) (tw D Sp), tw D Cp, BernZ.add (smul (2 * X) Sp) (smul (D : ℤ) Np)),
  1, 0, 0, 2 * D⟩

/-- The cap depths of a rectangle entry `(X0, Y0, …)`: `d_x = X0/D − c₁ + (cos θ + sin θ)/2` and
`d_y` likewise, over `2DN`. -/
def capX (X0 : ℕ) : SL := ⟨(smul (-(2 * D : ℤ)) Np, [0],
  BernZ.add (smul (2 * X0) Np) (smul (D : ℤ) (BernZ.add Cp Sp))), 0, 0, 1, 2 * D⟩
def capY (Y0 : ℕ) : SL := ⟨([0], smul (-(2 * D : ℤ)) Np,
  BernZ.add (smul (2 * Y0) Np) (smul (D : ℤ) (BernZ.add Cp Sp))), 0, 0, 1, 2 * D⟩

/-- The `tan` transform of a cap line `aff P/(2DN)` at `d* = n/m` (`LemmaE.tanF`), over `S N 2Dm²`:
`K = m(S + C) − nN`, numerator `mK·P + 2Dm²SC − DK² − 2DnNK + Dm²S²`. -/
def tanK (n m : ℕ) : Poly := BernZ.add (smul (m : ℤ) (BernZ.add Sp Cp)) (smul (-(n : ℤ)) Np)

def tanC (n m : ℕ) : Poly :=
  BernZ.add (BernZ.add (smul (2 * D * m * m : ℤ) (BernZ.mul Sp Cp)) (smul (-(D : ℤ)) (BernZ.mul (tanK n m) (tanK n m))))
    (BernZ.add (smul (-(2 * D * n) : ℤ) (BernZ.mul Np (tanK n m))) (smul (D * m * m : ℤ) (BernZ.mul Sp Sp)))

def tanCap (n m : ℕ) (P : PL) : SL :=
  let mK := smul (m : ℤ) (tanK n m)
  ⟨(BernZ.mul mK P.1, BernZ.mul mK P.2.1, BernZ.add (BernZ.mul mK P.2.2) (tanC D n m)), 0, 1, 1, 2 * D * m * m⟩

/-- The cap lines of a rectangle entry in its modes. -/
def capXm (r : RectM) : SL :=
  match r.2.1 with
  | none => capX D r.1.1
  | some (n, m) => tanCap D n m (capX D r.1.1).P
def capYm (r : RectM) : SL :=
  match r.2.2.1 with
  | none => capY D r.1.2.1
  | some (n, m) => tanCap D n m (capY D r.1.2.1).P

end lines

/-- A mode is well formed: `d* = n/m` with `0 < m`, `n ≤ m`. -/
def modeP : Option (ℕ × ℕ) → Bool
  | none => true
  | some (n, m) => Nat.blt 0 m && Nat.ble n m

lemma capXm_d {D : ℕ} (hD : 0 < D) (r : RectM) (hm : modeP r.2.1 = true) : (capXm D r).d ≠ 0 := by
  rcases r with ⟨r, mx, my, k⟩
  match mx, hm with
  | none, _ => simp only [capXm, capX]; omega
  | some (n, m), hm =>
    simp only [modeP, Bool.and_eq_true, Nat.blt_eq, Nat.ble_eq] at hm
    simp only [capXm, tanCap, ne_eq, mul_eq_zero, not_or]; omega

lemma capYm_d {D : ℕ} (hD : 0 < D) (r : RectM) (hm : modeP r.2.2.1 = true) : (capYm D r).d ≠ 0 := by
  rcases r with ⟨r, mx, my, k⟩
  match my, hm with
  | none, _ => simp only [capYm, capY]; omega
  | some (n, m), hm =>
    simp only [modeP, Bool.and_eq_true, Nat.blt_eq, Nat.ble_eq] at hm
    simp only [capYm, tanCap, ne_eq, mul_eq_zero, not_or]; omega

/-- `sin θ = 2u/(1+u²)`, `cos θ = (1−u²)/(1+u²)` at `θ = 2 arctan u`. -/
lemma trig (u : ℝ) : Real.sin (2 * Real.arctan u) = 2 * u / (1 + u ^ 2) ∧
    Real.cos (2 * Real.arctan u) = (1 - u ^ 2) / (1 + u ^ 2) :=
  ⟨sin_two_arctan u, cos_two_arctan u⟩

section identities

variable {D : ℕ} (hD : 0 < D) {u : ℝ} (hu0 : 0 < u) (hu1 : u < 1)
include hD hu0 hu1

private lemma pos_facts : (0 : ℝ) < D ∧ (0 : ℝ) < 1 - u ^ 2 ∧ (0 : ℝ) < 2 * u ∧ (0 : ℝ) < 1 + u ^ 2 :=
  ⟨by exact_mod_cast hD, by nlinarith, by linarith, by positivity⟩

lemma val_hTA (Y : ℕ) (c : ℝ × ℝ) :
    (hTA D Y).val u c = aff (chA (2 * Real.arctan u) ((Y : ℝ) / D)) c := by
  obtain ⟨h1, h2, h3, h4⟩ := pos_facts hD hu0 hu1
  rw [aff_chA (by rw [(trig u).2]; positivity)]
  simp only [SL.val, sden, hTA, tw, aff, evalPL, tA, (trig u).1, (trig u).2, BernZ.eval_smul,
    BernZ.eval_add, eval_Cp, eval_Sp, eval_Np]
  push_cast
  field_simp
  ring

lemma val_hTB (Y : ℕ) (c : ℝ × ℝ) :
    (hTB D Y).val u c = aff (chB (2 * Real.arctan u) ((Y : ℝ) / D)) c := by
  obtain ⟨h1, h2, h3, h4⟩ := pos_facts hD hu0 hu1
  rw [aff_chB (by rw [(trig u).1]; positivity)]
  simp only [SL.val, sden, hTB, tw, aff, evalPL, tB, (trig u).1, (trig u).2, BernZ.eval_smul,
    BernZ.eval_add, eval_Cp, eval_Sp, eval_Np]
  push_cast
  field_simp
  ring

lemma val_hTC (Y : ℕ) (c : ℝ × ℝ) :
    (hTC D Y).val u c = aff (chC (2 * Real.arctan u) ((Y : ℝ) / D)) c := by
  obtain ⟨h1, h2, h3, h4⟩ := pos_facts hD hu0 hu1
  rw [aff_chC (by rw [(trig u).2]; positivity)]
  simp only [SL.val, sden, hTC, tw, aff, evalPL, tC, (trig u).1, (trig u).2, BernZ.eval_smul,
    BernZ.eval_add, eval_Cp, eval_Sp, eval_Np]
  push_cast
  field_simp
  ring

lemma val_hTD (Y : ℕ) (c : ℝ × ℝ) :
    (hTD D Y).val u c = aff (chD (2 * Real.arctan u) ((Y : ℝ) / D)) c := by
  obtain ⟨h1, h2, h3, h4⟩ := pos_facts hD hu0 hu1
  rw [aff_chD (by rw [(trig u).1]; positivity)]
  simp only [SL.val, sden, hTD, tw, aff, evalPL, tD, (trig u).1, (trig u).2, BernZ.eval_smul,
    BernZ.eval_add, eval_Cp, eval_Sp, eval_Np]
  push_cast
  field_simp
  ring

lemma val_vLX (X : ℕ) (c : ℝ × ℝ) :
    (vLXs D X).val u c = aff (vLX (2 * Real.arctan u) ((X : ℝ) / D)) c := by
  obtain ⟨h1, h2, h3, h4⟩ := pos_facts hD hu0 hu1
  simp only [SL.val, sden, vLXs, vLX, tw, aff, evalPL, (trig u).1, (trig u).2, BernZ.eval_smul,
    BernZ.eval_add, eval_Cp, eval_Sp, eval_Np]
  push_cast
  field_simp
  ring

lemma val_vUX (X : ℕ) (c : ℝ × ℝ) :
    (vUXs D X).val u c = aff (vUX (2 * Real.arctan u) ((X : ℝ) / D)) c := by
  obtain ⟨h1, h2, h3, h4⟩ := pos_facts hD hu0 hu1
  simp only [SL.val, sden, vUXs, vUX, tw, aff, evalPL, (trig u).1, (trig u).2, BernZ.eval_smul,
    BernZ.eval_add, eval_Cp, eval_Sp, eval_Np]
  push_cast
  field_simp
  ring

lemma val_vLY (X : ℕ) (c : ℝ × ℝ) :
    (vLYs D X).val u c = aff (vLY (2 * Real.arctan u) ((X : ℝ) / D)) c := by
  obtain ⟨h1, h2, h3, h4⟩ := pos_facts hD hu0 hu1
  simp only [SL.val, sden, vLYs, vLY, tw, aff, evalPL, (trig u).1, (trig u).2, BernZ.eval_smul,
    BernZ.eval_add, eval_Cp, eval_Sp, eval_Np]
  push_cast
  field_simp
  ring

lemma val_vUY (X : ℕ) (c : ℝ × ℝ) :
    (vUYs D X).val u c = aff (vUY (2 * Real.arctan u) ((X : ℝ) / D)) c := by
  obtain ⟨h1, h2, h3, h4⟩ := pos_facts hD hu0 hu1
  simp only [SL.val, sden, vUYs, vUY, tw, aff, evalPL, (trig u).1, (trig u).2, BernZ.eval_smul,
    BernZ.eval_add, eval_Cp, eval_Sp, eval_Np]
  push_cast
  field_simp

lemma val_capX (X0 : ℕ) (c : ℝ × ℝ) :
    (capX D X0).val u c = (X0 : ℝ) / D - c.1 +
      (Real.cos (2 * Real.arctan u) + Real.sin (2 * Real.arctan u)) / 2 := by
  obtain ⟨h1, h2, h3, h4⟩ := pos_facts hD hu0 hu1
  simp only [SL.val, sden, capX, aff, evalPL, (trig u).1, (trig u).2, BernZ.eval_smul,
    BernZ.eval_add, eval_Cp, eval_Sp, eval_Np, eval_cons, eval_nil]
  push_cast
  field_simp
  ring

lemma val_capY (Y0 : ℕ) (c : ℝ × ℝ) :
    (capY D Y0).val u c = (Y0 : ℝ) / D - c.2 +
      (Real.cos (2 * Real.arctan u) + Real.sin (2 * Real.arctan u)) / 2 := by
  obtain ⟨h1, h2, h3, h4⟩ := pos_facts hD hu0 hu1
  simp only [SL.val, sden, capY, aff, evalPL, (trig u).1, (trig u).2, BernZ.eval_smul,
    BernZ.eval_add, eval_Cp, eval_Sp, eval_Np, eval_cons, eval_nil]
  push_cast
  field_simp
  ring

lemma val_tanCap (n m : ℕ) (hm : 0 < m) (P : PL) (c : ℝ × ℝ) :
    (tanCap D n m P).val u c =
      (Real.sin (2 * Real.arctan u) + Real.cos (2 * Real.arctan u) - (n : ℝ) / m) /
          Real.sin (2 * Real.arctan u) * (SL.mk P 0 0 1 (2 * D)).val u c +
        (Real.cos (2 * Real.arctan u) -
          (Real.sin (2 * Real.arctan u) + Real.cos (2 * Real.arctan u) - (n : ℝ) / m) ^ 2 /
            (2 * Real.sin (2 * Real.arctan u)) -
          (Real.sin (2 * Real.arctan u) + Real.cos (2 * Real.arctan u) - (n : ℝ) / m) * ((n : ℝ) / m) /
            Real.sin (2 * Real.arctan u) + Real.sin (2 * Real.arctan u) / 2) := by
  obtain ⟨h1, h2, h3, h4⟩ := pos_facts hD hu0 hu1
  have hmr : (0 : ℝ) < m := by exact_mod_cast hm
  simp only [SL.val, sden, tanCap, tanC, tanK, aff, evalPL, (trig u).1, (trig u).2, BernZ.eval_smul,
    BernZ.eval_add, BernZ.eval_mul, eval_Cp, eval_Sp, eval_Np]
  push_cast
  field_simp
  ring

lemma val_capXm (r : RectM) (hm : modeP r.2.1 = true) (c : ℝ × ℝ) :
    (capXm D r).val u c = aff (capFm (2 * Real.arctan u) r.2.1
      (-1, 0, (r.1.1 : ℝ) / D + (Real.cos (2 * Real.arctan u) + Real.sin (2 * Real.arctan u)) / 2)) c := by
  rcases r with ⟨r, mx, my, k⟩
  match mx, hm with
  | none, _ =>
    simp only [capXm, capFm]
    rw [val_capX hD hu0 hu1]; simp only [aff]; ring
  | some (n, m), hm =>
    simp only [modeP, Bool.and_eq_true, Nat.blt_eq, Nat.ble_eq] at hm
    simp only [capXm, capFm]
    rw [val_tanCap hD hu0 hu1 n m hm.1, aff_tanF, show SL.mk (capX D r.1).P 0 0 1 (2 * D) = capX D r.1 from rfl,
      val_capX hD hu0 hu1]
    simp only [aff]; ring

lemma val_capYm (r : RectM) (hm : modeP r.2.2.1 = true) (c : ℝ × ℝ) :
    (capYm D r).val u c = aff (capFm (2 * Real.arctan u) r.2.2.1
      (0, -1, (r.1.2.1 : ℝ) / D + (Real.cos (2 * Real.arctan u) + Real.sin (2 * Real.arctan u)) / 2)) c := by
  rcases r with ⟨r, mx, my, k⟩
  match my, hm with
  | none, _ =>
    simp only [capYm, capFm]
    rw [val_capY hD hu0 hu1]; simp only [aff]; ring
  | some (n, m), hm =>
    simp only [modeP, Bool.and_eq_true, Nat.blt_eq, Nat.ble_eq] at hm
    simp only [capYm, capFm]
    rw [val_tanCap hD hu0 hu1 n m hm.1, aff_tanF, show SL.mk (capY D r.2.1).P 0 0 1 (2 * D) = capY D r.2.1 from rfl,
      val_capY hD hu0 hu1]
    simp only [aff]; ring

end identities

end LemmaEPoly

end SquarePacking
