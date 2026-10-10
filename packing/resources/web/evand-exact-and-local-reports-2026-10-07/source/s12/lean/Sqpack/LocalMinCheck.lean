import Sqpack.LocalMinRows
import Sqpack.ExactCheck

/-!
# Local-minimum certificates over a number field

`LCert`: an exact packing certificate `P` (`ExactCheck.Cert`), the rotations `(C, S)` as field elements
(`C d ≡ c`, `S d ≡ s` with `P`'s numerators `c, s` and denominator `d`), rows, multipliers `λ_r` (field elements),
a rational approximate left inverse `G` (one list per variable), and sparse rational midpoints of the linear parts
(`Lc w`: the nonzero entries of column `w`) with one global radius `eps`.  The left-inverse condition
`Σ_w |Σ_r G_vr L_rw − δ_vw| ≤ 1/2` is checked on the midpoints (sparse dot products) plus `(3n+1)·Gn·eps`, so the
cost is linear in the number of nonzero entries rather than `(3n+1)²·m` interval products.

Every check is decidable with exact rational arithmetic (`decide +kernel`), and `isLocalMin_of_lcert` turns them
into `IsLocalMinPacking` for the exact configuration at any root `t ∈ [a, b]` of `f`.
-/

namespace UnitSquarePacking.LMC

open EC LM Real

structure LCert (n m : ℕ) where
  P : Cert n
  C : Fin n → Poly
  S : Fin n → Poly
  rows : Fin m → Row n
  mu : ℚ
  lam : Fin m → Poly
  lmin : ℚ
  Lam : ℚ
  /-- Row `v` of the left inverse, a list of length `m`. -/
  Gr : Var n → List ℚ
  Gn : ℚ
  /-- Column `w` of the linear parts at the record: rational midpoints of its nonzero entries, `(row, value)`. -/
  Lc : Var n → List (Fin m × ℚ)
  eps : ℚ

variable {n m : ℕ} (L : LCert n m)

/-! ## Polynomial versions of the row quantities -/

def Xp (j : Fin n) : Poly := (L.P.sq j).x
def Yp (j : Fin n) : Poly := (L.P.sq j).y
def qxP (j : Fin n) (a b : ℚ) : Poly := psub (psmul a (L.C j)) (psmul b (L.S j))
def qyP (j : Fin n) (a b : ℚ) : Poly := padd (psmul a (L.S j)) (psmul b (L.C j))
def sideValP (xi yi ci si : Poly) (k : Fin 4) (Px Py : Poly) : Poly :=
  padd (pmul (nrmN ci si k).1 (psub Px xi)) (pmul (nrmN ci si k).2 (psub Py yi))
def AxP (j : Fin n) (a b : ℚ) (i : Fin n) : Poly := psub (padd (Xp L j) (qxP L j a b)) (Xp L i)
def AyP (j : Fin n) (a b : ℚ) (i : Fin n) : Poly := psub (padd (Yp L j) (qyP L j a b)) (Yp L i)
def svP (j : Fin n) (a b : ℚ) (i : Fin n) (k : Fin 4) : Poly :=
  sideValP (Xp L i) (Yp L i) (L.C i) (L.S i) k (padd (Xp L j) (qxP L j a b)) (padd (Yp L j) (qyP L j a b))

def hvalP : Row n → Poly
  | .pt j a b i k => psub (svP L j a b i k) [1 / 2]
  | .wall j a b w => ![padd (Xp L j) (qxP L j a b), psub L.P.S (padd (Xp L j) (qxP L j a b)),
      padd (Yp L j) (qyP L j a b), psub L.P.S (padd (Yp L j) (qyP L j a b))] w

def ptJP (j : Fin n) (a b : ℚ) (i : Fin n) (k : Fin 4) : Fin 3 → Poly :=
  ![(nrmN (L.C i) (L.S i) k).1, (nrmN (L.C i) (L.S i) k).2,
    padd (pmul (nrmN (L.C i) (L.S i) k).1 (psmul (-1) (qyP L j a b))) (pmul (nrmN (L.C i) (L.S i) k).2 (qxP L j a b))]
def ptIP (j : Fin n) (a b : ℚ) (i : Fin n) (k : Fin 4) : Fin 3 → Poly :=
  ![psmul (-1) (nrmN (L.C i) (L.S i) k).1, psmul (-1) (nrmN (L.C i) (L.S i) k).2,
    padd (pmul (psmul (-1) (nrmN (L.C i) (L.S i) k).2) (AxP L j a b i)) (pmul (nrmN (L.C i) (L.S i) k).1 (AyP L j a b i))]
def wallJP (j : Fin n) (a b : ℚ) (w : Fin 4) : Fin 3 → Poly :=
  ![[![1, -1, 0, 0] w], [![0, 0, 1, -1] w],
    ![psmul (-1) (qyP L j a b), qyP L j a b, qxP L j a b, psmul (-1) (qxP L j a b)] w]
def onSqP (j : Fin n) (g : Fin 3 → Poly) : Var n → Poly
  | none => []
  | some (l, c) => if l = j then g c else []

def rowLP : Row n → Var n → Poly
  | .pt j a b i k, v => padd (onSqP j (ptJP L j a b i k) v) (onSqP i (ptIP L j a b i k) v)
  | .wall j a b w, v => padd (match v with | none => [![0, 1, 0, 1] w] | some _ => []) (onSqP j (wallJP L j a b w) v)

/-! ## The real configuration and evaluation lemmas -/

noncomputable def cfg (t : ℝ) : Cfg n :=
  ⟨fun i => peval (Xp L i) t, fun i => peval (Yp L i) t, fun i => peval (L.C i) t, fun i => peval (L.S i) t,
    peval L.P.S t⟩

variable {L}

lemma nrmN_peval (c s : Poly) (k : Fin 4) (t : ℝ) :
    peval (nrmN c s k).1 t = (nrm (peval c t) (peval s t) k).1 ∧
      peval (nrmN c s k).2 t = (nrm (peval c t) (peval s t) k).2 := by
  fin_cases k <;> simp [nrmN, nrm]

lemma qxP_peval (j : Fin n) (a b : ℚ) (t : ℝ) : peval (qxP L j a b) t = qx (cfg L t) j a b := by
  simp [qxP, qx, cfg]; ring
lemma qyP_peval (j : Fin n) (a b : ℚ) (t : ℝ) : peval (qyP L j a b) t = qy (cfg L t) j a b := by
  simp [qyP, qy, cfg]; ring

lemma svP_peval (j : Fin n) (a b : ℚ) (i : Fin n) (k : Fin 4) (t : ℝ) :
    peval (svP L j a b i k) t = sideVal ((cfg L t).X i) ((cfg L t).Y i) ((cfg L t).C i) ((cfg L t).S i) k
      ((cfg L t).X j + qx (cfg L t) j a b) ((cfg L t).Y j + qy (cfg L t) j a b) := by
  obtain ⟨h1, h2⟩ := nrmN_peval (L.C i) (L.S i) k t
  simp only [svP, sideValP, peval_padd, peval_pmul, peval_psub, h1, h2, qxP_peval, qyP_peval, sideVal]
  rfl

lemma hvalP_peval (row : Row n) (t : ℝ) : peval (hvalP L row) t = hval (cfg L t) row := by
  rcases row with ⟨j, a, b, i, k⟩ | ⟨j, a, b, w⟩
  · simp only [hvalP, hval, peval_psub, svP_peval]; simp
  · simp only [hvalP, hval]
    fin_cases w <;> simp [qxP_peval, qyP_peval, cfg]

lemma onSqP_peval (j : Fin n) (g : Fin 3 → Poly) (v : Var n) (t : ℝ) :
    peval (onSqP j g v) t = onSq j (fun c => peval (g c) t) v := by
  rcases v with _ | ⟨l, c⟩
  · rfl
  · simp only [onSqP, onSq]; split_ifs <;> rfl

lemma ptJP_peval (j : Fin n) (a b : ℚ) (i : Fin n) (k : Fin 4) (t : ℝ) :
    (fun c => peval (ptJP L j a b i k c) t) = ptJ (cfg L t) j a b i k := by
  obtain ⟨e1, e2⟩ := nrmN_peval (L.C i) (L.S i) k t
  funext c; fin_cases c <;> simp [ptJP, ptJ, e1, e2, qxP_peval, qyP_peval, cfg]

lemma ptIP_peval (j : Fin n) (a b : ℚ) (i : Fin n) (k : Fin 4) (t : ℝ) :
    (fun c => peval (ptIP L j a b i k c) t) = ptI (cfg L t) j a b i k := by
  obtain ⟨e1, e2⟩ := nrmN_peval (L.C i) (L.S i) k t
  funext c; fin_cases c <;> simp [ptIP, ptI, e1, e2, AxP, AyP, qxP_peval, qyP_peval, cfg]

lemma wallJP_peval (j : Fin n) (a b : ℚ) (w : Fin 4) (t : ℝ) :
    (fun c => peval (wallJP L j a b w c) t) = wallJ (cfg L t) j a b w := by
  funext c; fin_cases c <;> fin_cases w <;> simp [wallJP, wallJ, qxP_peval, qyP_peval]

lemma rowLP_peval (row : Row n) (v : Var n) (t : ℝ) : peval (rowLP L row v) t = rowL (cfg L t) row v := by
  rcases row with ⟨j, a, b, i, k⟩ | ⟨j, a, b, w⟩
  · simp only [rowLP, rowL, peval_padd, onSqP_peval, ptJP_peval, ptIP_peval]
  · simp only [rowLP, rowL, peval_padd, onSqP_peval, wallJP_peval]
    congr 1
    rcases v with _ | _
    · fin_cases w <;> simp
    · simp

/-! ## Sparse sums -/

/-- Sparse lookup: the value stored for `r`, or `0`. -/
def lk {m : ℕ} : List (Fin m × ℚ) → Fin m → ℚ
  | [], _ => 0
  | p :: l, r => if p.1 = r then p.2 else lk l r

/-- Σ over the variables, as nested list sums (`none` = the side `S`, then `(i, c)`). -/
def sumV {n : ℕ} (h : Var n → ℚ) : ℚ :=
  h none + ((List.finRange n).map fun i => ((List.finRange 3).map fun c => h (some (i, c))).sum).sum

lemma lk_eq_zero {m : ℕ} {l : List (Fin m × ℚ)} {r : Fin m} (h : r ∉ l.map Prod.fst) : lk l r = 0 := by
  induction l with
  | nil => rfl
  | cons p l ih =>
    simp only [List.map_cons, List.mem_cons, not_or] at h
    simp only [lk, if_neg (Ne.symm h.1), ih h.2]

lemma sum_mul_lk {m : ℕ} (g : Fin m → ℝ) {l : List (Fin m × ℚ)} (hl : (l.map Prod.fst).Nodup) :
    ∑ r, g r * (lk l r : ℝ) = (l.map fun p => g p.1 * (p.2 : ℝ)).sum := by
  induction l with
  | nil => simp [lk]
  | cons p l ih =>
    simp only [List.map_cons, List.nodup_cons] at hl
    have e : ∀ r, g r * (lk (p :: l) r : ℝ) = (if p.1 = r then g r * p.2 else 0) + g r * lk l r := by
      intro r
      by_cases h : p.1 = r
      · subst h; simp [lk, lk_eq_zero hl.1]
      · simp [lk, h]
    simp only [e, Finset.sum_add_distrib, Finset.sum_ite_eq, Finset.mem_univ, if_true, ih hl.2,
      List.map_cons, List.sum_cons]

lemma sum_getD {m : ℕ} (f : ℚ → ℝ) {l : List ℚ} (hl : l.length = m) :
    ∑ r : Fin m, f (l.getD r 0) = (l.map f).sum := by
  subst hl
  rw [← List.sum_ofFn]
  congr 1
  apply List.ext_getElem <;> simp

lemma sumV_cast {n : ℕ} (h : Var n → ℚ) : ((sumV h : ℚ) : ℝ) = ∑ w, (h w : ℝ) := by
  simp [sumV, Fintype.sum_option, Fintype.sum_prod_type, Fin.sum_univ_def, Rat.cast_list_sum, List.map_map,
    Function.comp_def]

lemma sum_const_var {n : ℕ} (c : ℝ) : ∑ _w : Var n, c = (3 * n + 1) * c := by
  rw [Finset.sum_const, Finset.card_univ, Fintype.card_option, Fintype.card_prod, Fintype.card_fin, Fintype.card_fin,
    nsmul_eq_mul]
  push_cast; ring

/-! ## The checks -/

variable (L)

def nn (p : Poly) : Bool := nonnegOK L.P.f L.P.a L.P.b p

/-- `C d ≡ c`, `S d ≡ s` (the numerators and denominator of the packing certificate). -/
def unitOK (i : Fin n) : Bool :=
  zeroOK L.P.f (psub (pmul (L.C i) (dd (L.P.sq i))) (csN (L.P.sq i)).1) &&
    zeroOK L.P.f (psub (pmul (L.S i) (dd (L.P.sq i))) (csN (L.P.sq i)).2)

def rowOKb : Row n → Bool
  | .pt j a b i k => decide (|a| ≤ 1 / 2) && decide (|b| ≤ 1 / 2) && decide (i ≠ j) &&
      zeroOK L.P.f (hvalP L (.pt j a b i k)) &&
      nn L (psub [2] (AxP L j a b i)) && nn L (padd [2] (AxP L j a b i)) &&
      nn L (psub [2] (AyP L j a b i)) && nn L (padd [2] (AyP L j a b i)) &&
      (List.finRange 4).all (fun k' => decide (k' = k) || nn L (psub [1 / 2 - L.mu] (svP L j a b i k')))
  | .wall j a b w => decide (|a| ≤ 1 / 2) && decide (|b| ≤ 1 / 2) && zeroOK L.P.f (hvalP L (.wall j a b w))

def psumF (g : Fin m → Poly) : Poly := (List.finRange m).foldr (fun r acc => padd (g r) acc) []

def lamOK (r : Fin m) : Bool := nn L (psub (L.lam r) [L.lmin])
def lamSumOK : Bool := nn L (psub [L.Lam] (psumF L.lam)) && decide (0 < L.lmin) && decide (0 < L.mu)
def kktOK (v : Var n) : Bool :=
  zeroOK L.P.f (psub (psumF fun r => pmul (L.lam r) (rowLP L (L.rows r) v)) [if v = none then 1 else 0])
/-- `|L_rw − Lc_rw| ≤ eps`: structurally zero entries outside the support pass without field arithmetic. -/
def boundOK (r : Fin m) (w : Var n) : Bool :=
  (allZero (rowLP L (L.rows r) w) && decide (lk (L.Lc w) r = 0)) ||
    (nn L (psub (rowLP L (L.rows r) w) [lk (L.Lc w) r - L.eps]) &&
      nn L (psub [lk (L.Lc w) r + L.eps] (rowLP L (L.rows r) w)))
/-- Column supports without repeated rows. -/
def colOK (w : Var n) : Bool := decide ((L.Lc w).map Prod.fst).Nodup
def GnOK (v : Var n) : Bool := decide ((L.Gr v).length = m) && decide (((L.Gr v).map abs).sum ≤ L.Gn)
/-- Sparse `Σ_r g_r Lc_rw`. -/
def dotS (g : List ℚ) (l : List (Fin m × ℚ)) : ℚ := (l.map fun p => g.getD p.1 0 * p.2).sum
def GOK (v : Var n) : Bool :=
  decide (0 ≤ L.eps) &&
    decide (sumV (fun w => |dotS (L.Gr v) (L.Lc w) - (if v = w then 1 else 0)|) + (3 * n + 1) * L.Gn * L.eps ≤ 1 / 2)

variable {L}

lemma psumF_peval (g : Fin m → Poly) (t : ℝ) : peval (psumF g) t = ∑ r, peval (g r) t := by
  rw [Fin.sum_univ_def, psumF]
  induction (List.finRange m) with
  | nil => simp
  | cons r l ih => simp [ih]

lemma nn_le {p : Poly} (h : nn L p = true) {t : ℝ} (hf : peval L.P.f t = 0) (ha : (L.P.a : ℝ) ≤ t)
    (hb : t ≤ L.P.b) : 0 ≤ peval p t := nonneg_of_nonnegOK h hf ha hb

lemma AxP_peval (j : Fin n) (a b : ℚ) (i : Fin n) (t : ℝ) :
    peval (AxP L j a b i) t = (cfg L t).X j + qx (cfg L t) j a b - (cfg L t).X i := by
  simp [AxP, qxP_peval, cfg]
lemma AyP_peval (j : Fin n) (a b : ℚ) (i : Fin n) (t : ℝ) :
    peval (AyP L j a b i) t = (cfg L t).Y j + qy (cfg L t) j a b - (cfg L t).Y i := by
  simp [AyP, qyP_peval, cfg]

/-! ## Soundness -/

theorem isLocalMin_of_lcert (hSl : SlOK L.P = true) (hbox : ∀ i, boxOK L.P i = true) (hrowP : ∀ i, EC.rowOK L.P i = true)
    (hunit : ∀ i, unitOK L i = true) (hrows : ∀ r, rowOKb L (L.rows r) = true) (hlam : ∀ r, lamOK L r = true)
    (hlamS : lamSumOK L = true) (hkkt : ∀ v, kktOK L v = true) (hbnd : ∀ r v, boundOK L r v = true)
    (hcol : ∀ w, colOK L w = true) (hGn : ∀ v, GnOK L v = true) (hG : ∀ v, GOK L v = true) {t : ℝ} (hf : peval L.P.f t = 0) (ha : (L.P.a : ℝ) ≤ t)
    (hb : t ≤ L.P.b) :
    ∃ θ : Fin n → ℝ, IsLocalMinPacking n (peval L.P.S t) (fun i => (peval (Xp L i) t, peval (Yp L i) t)) θ := by
  have hsq : ∀ i, sqOK L.P.f (L.P.sq i) = true := fun i => sqOK_of_boxOK L.P (hbox i)
  have hCS : ∀ i, peval (L.C i) t = cR (L.P.sq i) t ∧ peval (L.S i) t = sR (L.P.sq i) t := by
    intro i
    have h := hunit i
    simp only [unitOK, Bool.and_eq_true] at h
    have e1 := zero_of_zeroOK h.1 hf
    have e2 := zero_of_zeroOK h.2 hf
    simp only [peval_psub, peval_pmul] at e1 e2
    have hd := (dd_pos (hsq i) hf).ne'
    simp only [cR, sR]
    constructor <;> field_simp <;> linarith
  choose θ hθc hθs using fun i => exists_angle (cR_sq_add (hsq i) hf)
  refine ⟨θ, ?_⟩
  -- the record is a packing
  have hpack : IsPacking n (peval L.P.S t) (fun i => (peval (Xp L i) t, peval (Yp L i) t)) θ := by
    refine ⟨fun i => unitSq_subset_container (hθc i) (hθs i) (inBox_of_boxOK L.P (hbox i) hSl hf ha hb), ?_⟩
    have pos : ∀ i j, i < j → Disjoint (interior (unitSq (peval (Xp L i) t, peval (Yp L i) t) (θ i)))
        (interior (unitSq (peval (Xp L j) t, peval (Yp L j) t) (θ j))) := fun i j hij =>
      disjoint_of_pairOK L.P (hbox i) (hbox j) (pairOK_of_rowOK L.P (hrowP i) hij) hf ha hb
        (hθc i) (hθs i) (hθc j) (hθs j)
    intro i j hij
    rcases lt_or_gt_of_ne hij with h | h
    · exact pos i j h
    · exact (pos j i h).symm
  have hθc' : ∀ i, Real.cos (θ i) = (cfg L t).C i := fun i => by rw [hθc]; exact (hCS i).1.symm
  have hθs' : ∀ i, Real.sin (θ i) = (cfg L t).S i := fun i => by rw [hθs]; exact (hCS i).2.symm
  simp only [lamSumOK, Bool.and_eq_true, decide_eq_true_eq] at hlamS
  obtain ⟨⟨hΛ, hlmin⟩, hmu⟩ := hlamS
  refine isLocalMin_of_rows (cfg L t) θ hθc' hθs' hpack L.rows (μ := L.mu) (by exact_mod_cast hmu) ?_
    (fun r => peval (L.lam r) t) (fun v r => (((L.Gr v).getD r 0 : ℚ) : ℝ)) (lmin := L.lmin) (Λ := L.Lam) (Gn := L.Gn)
    (by exact_mod_cast hlmin) ?_ ?_ ?_ ?_ ?_
  · -- rows
    intro r
    have h := hrows r
    generalize L.rows r = row at h ⊢
    rcases row with ⟨j, a, b, i, k⟩ | ⟨j, a, b, w⟩
    · simp only [rowOKb, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true, List.mem_finRange,
        true_implies, Bool.or_eq_true] at h
      obtain ⟨⟨⟨⟨⟨⟨⟨⟨ha', hb'⟩, hij⟩, hz⟩, hx1⟩, hx2⟩, hy1⟩, hy2⟩, hmar⟩ := h
      have ex1 := nn_le hx1 hf ha hb
      have ex2 := nn_le hx2 hf ha hb
      have ey1 := nn_le hy1 hf ha hb
      have ey2 := nn_le hy2 hf ha hb
      simp only [peval_psub, peval_padd, peval_cons, peval_nil, AxP_peval, AyP_peval] at ex1 ex2 ey1 ey2
      refine ⟨by simpa using (Rat.cast_le (K := ℝ)).mpr ha', by simpa using (Rat.cast_le (K := ℝ)).mpr hb', hij, ?_, ?_, ?_, ?_⟩
      · rw [← hvalP_peval]; exact zero_of_zeroOK hz hf
      · rw [abs_le]; constructor <;> push_cast at ex1 ex2 <;> linarith
      · rw [abs_le]; constructor <;> push_cast at ey1 ey2 <;> linarith
      · intro k' hk'
        have hm := hmar k'
        simp only [decide_eq_true_eq, hk', false_or] at hm
        have := nn_le hm hf ha hb
        simp only [peval_psub, peval_cons, peval_nil, svP_peval] at this
        push_cast at this; linarith
    · simp only [rowOKb, Bool.and_eq_true, decide_eq_true_eq] at h
      obtain ⟨⟨ha', hb'⟩, hz⟩ := h
      refine ⟨by simpa using (Rat.cast_le (K := ℝ)).mpr ha', by simpa using (Rat.cast_le (K := ℝ)).mpr hb', ?_⟩
      rw [← hvalP_peval]; exact zero_of_zeroOK hz hf
  · -- multipliers ≥ λ_min
    intro r
    have := nn_le (hlam r) hf ha hb
    simp only [peval_psub, peval_cons, peval_nil] at this; push_cast at this; linarith
  · -- Σ λ ≤ Λ
    have := nn_le hΛ hf ha hb
    simp only [peval_psub, peval_cons, peval_nil, psumF_peval] at this; push_cast at this; linarith
  · -- Σ λ_r L_r = e_S
    intro v
    have := zero_of_zeroOK (hkkt v) hf
    simp only [peval_psub, psumF_peval, peval_pmul, rowLP_peval, peval_cons, peval_nil] at this
    split_ifs at this ⊢ <;> push_cast at this <;> linarith
  · -- Σ |G| ≤ Gn
    intro v
    have h := hGn v
    simp only [GnOK, Bool.and_eq_true, decide_eq_true_eq] at h
    rw [sum_getD (fun q => |(q : ℝ)|) h.1]
    have := (Rat.cast_le (K := ℝ)).mpr h.2
    simpa [Rat.cast_list_sum, List.map_map, Function.comp_def] using this
  · -- ‖G L - I‖ ≤ 1/2
    intro v
    have h := hG v
    simp only [GOK, Bool.and_eq_true, decide_eq_true_eq] at h
    obtain ⟨heps, hq⟩ := h
    have heps' : (0 : ℝ) ≤ L.eps := by exact_mod_cast heps
    have hgl : (L.Gr v).length = m := by
      have h := hGn v; simp only [GnOK, Bool.and_eq_true, decide_eq_true_eq] at h; exact h.1
    have hGn' : ∑ r : Fin m, |(((L.Gr v).getD (r : ℕ) 0 : ℚ) : ℝ)| ≤ L.Gn := by
      have h := hGn v
      simp only [GnOK, Bool.and_eq_true, decide_eq_true_eq] at h
      rw [sum_getD (fun q => |(q : ℝ)|) h.1]
      have := (Rat.cast_le (K := ℝ)).mpr h.2
      simpa [Rat.cast_list_sum, List.map_map, Function.comp_def] using this
    -- entry bounds
    have hbd : ∀ r w, |rowL (cfg L t) (L.rows r) w - (lk (L.Lc w) r : ℝ)| ≤ L.eps := by
      intro r w
      have h := hbnd r w
      simp only [boundOK, Bool.or_eq_true, Bool.and_eq_true, decide_eq_true_eq] at h
      rcases h with ⟨hz, hd⟩ | ⟨h1, h2⟩
      · rw [← rowLP_peval, peval_eq_zero_of_allZero hz, hd]; simpa using heps'
      · have e1 := nn_le h1 hf ha hb
        have e2 := nn_le h2 hf ha hb
        simp only [peval_psub, peval_cons, peval_nil, rowLP_peval] at e1 e2
        push_cast at e1 e2
        rw [abs_le]; constructor <;> linarith
    -- the midpoint products are the sparse dot products
    have hdot : ∀ w, ∑ r : Fin m, (((L.Gr v).getD (r : ℕ) 0 : ℚ) : ℝ) * (lk (L.Lc w) r : ℝ) = (dotS (L.Gr v) (L.Lc w) : ℝ) := by
      intro w
      have hc := hcol w
      simp only [colOK, decide_eq_true_eq] at hc
      rw [sum_mul_lk _ hc, dotS]
      simp [Rat.cast_list_sum, List.map_map, Function.comp_def]
    have key : ∀ w, |(∑ r : Fin m, (((L.Gr v).getD (r : ℕ) 0 : ℚ) : ℝ) * rowL (cfg L t) (L.rows r) w) -
        (if v = w then 1 else 0)| ≤ |((dotS (L.Gr v) (L.Lc w) : ℚ) : ℝ) - (if v = w then 1 else 0)| + L.Gn * L.eps := by
      intro w
      have e : (∑ r : Fin m, (((L.Gr v).getD (r : ℕ) 0 : ℚ) : ℝ) * rowL (cfg L t) (L.rows r) w) =
          (dotS (L.Gr v) (L.Lc w) : ℝ) + ∑ r : Fin m, (((L.Gr v).getD (r : ℕ) 0 : ℚ) : ℝ) *
            (rowL (cfg L t) (L.rows r) w - (lk (L.Lc w) r : ℝ)) := by
        rw [← hdot w, ← Finset.sum_add_distrib]; congr 1; ext r; ring
      have hE : |∑ r : Fin m, (((L.Gr v).getD (r : ℕ) 0 : ℚ) : ℝ) * (rowL (cfg L t) (L.rows r) w - (lk (L.Lc w) r : ℝ))| ≤
          L.Gn * L.eps := by
        calc _ ≤ ∑ r : Fin m, |(((L.Gr v).getD (r : ℕ) 0 : ℚ) : ℝ) * (rowL (cfg L t) (L.rows r) w - (lk (L.Lc w) r : ℝ))| :=
              Finset.abs_sum_le_sum_abs _ _
          _ ≤ ∑ r : Fin m, |(((L.Gr v).getD (r : ℕ) 0 : ℚ) : ℝ)| * L.eps := by
              apply Finset.sum_le_sum; intro r _; rw [abs_mul]
              exact mul_le_mul_of_nonneg_left (hbd r w) (abs_nonneg _)
          _ = (∑ r : Fin m, |(((L.Gr v).getD (r : ℕ) 0 : ℚ) : ℝ)|) * L.eps := by rw [Finset.sum_mul]
          _ ≤ L.Gn * L.eps := mul_le_mul_of_nonneg_right hGn' heps'
      rw [e]
      calc _ = |((dotS (L.Gr v) (L.Lc w) : ℚ) : ℝ) - (if v = w then 1 else 0) +
              ∑ r : Fin m, (((L.Gr v).getD (r : ℕ) 0 : ℚ) : ℝ) * (rowL (cfg L t) (L.rows r) w - (lk (L.Lc w) r : ℝ))| := by
            congr 1; ring
        _ ≤ _ := (abs_add_le _ _).trans (by linarith)
    have hq' := (Rat.cast_le (K := ℝ)).mpr hq
    push_cast at hq'
    rw [sumV_cast] at hq'
    have e2 : ∀ w : Var n, (((|dotS (L.Gr v) (L.Lc w) - (if v = w then 1 else 0)| : ℚ)) : ℝ) =
        |((dotS (L.Gr v) (L.Lc w) : ℚ) : ℝ) - (if v = w then 1 else 0)| := by
      intro w; split_ifs <;> simp
    simp only [e2] at hq'
    calc _ ≤ ∑ w, (|((dotS (L.Gr v) (L.Lc w) : ℚ) : ℝ) - (if v = w then 1 else 0)| + L.Gn * L.eps) :=
          Finset.sum_le_sum fun w _ => key w
      _ = (∑ w, |((dotS (L.Gr v) (L.Lc w) : ℚ) : ℝ) - (if v = w then 1 else 0)|) + (3 * n + 1) * (L.Gn * L.eps) := by
          rw [Finset.sum_add_distrib, sum_const_var]
      _ ≤ 1 / 2 := by linarith

end UnitSquarePacking.LMC
