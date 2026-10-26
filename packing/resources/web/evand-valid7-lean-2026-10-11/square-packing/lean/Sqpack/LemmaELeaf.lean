import Sqpack.LemmaEK
import Sqpack.LebCredit

/-!
# Lemma E on a pose box: the `EXACT` leaf

For a box of centres and an angle bin `u ∈ (U0/R, U1/R]`, the leaf names the claimed segments and
rectangles, a list of lines `Ls` (polynomial triples in `u`), and for every pair of lines of
`side ++ Ls` (`side`: the four sides of the region) a certificate on sub-bins of `u`: the pair is
parallel (`Δ ≡ 0`), or on each sub-bin `Δ` has a certified sign and the vertex `(X/Δ, Y/Δ)` is
outside the region (a side is negative there) or `fE ≥ W` there (`vertOk`).  Every form of the
claimed terms is a line of `Ls` or has a certified sign on the region (four corners).  Then every
admissible pose of the box captures mass `≥ W` (`CovMPo.of_exact`).

This file: the vertex of two lines (`cramer`), sub-bin and pair certificates, and their soundness.
-/

namespace SquarePacking

namespace LemmaELeaf

open BernZ RatU ChordE LemmaE LemmaEPoly LemmaEVert PolyMin ZMTreeM

/-! ## 1.  The vertex of two lines -/

/-- `Δ`, `X`, `Y` of two polynomial lines: the vertex is `(X/Δ, Y/Δ)`. -/
def detP (P Q : PL) : Poly := BernZ.add (BernZ.mul P.1 Q.2.1) (smul (-1) (BernZ.mul Q.1 P.2.1))
def xP (P Q : PL) : Poly := BernZ.add (BernZ.mul P.2.1 Q.2.2) (smul (-1) (BernZ.mul Q.2.1 P.2.2))
def yP (P Q : PL) : Poly := BernZ.add (BernZ.mul Q.1 P.2.2) (smul (-1) (BernZ.mul P.1 Q.2.2))

lemma eval_detP (P Q : PL) (u : ℝ) :
    eval (detP P Q) u = (evalPL P u).1 * (evalPL Q u).2.1 - (evalPL P u).2.1 * (evalPL Q u).1 := by
  simp only [detP, evalPL, BernZ.eval_add, BernZ.eval_mul, eval_smul]; push_cast; ring

/-- **Cramer**: two lines with `det ≠ 0`, both zero at `v`, meet at `(X/Δ, Y/Δ)`. -/
lemma cramer (P Q : PL) (u : ℝ) (v : ℝ × ℝ) (hdet : eval (detP P Q) u ≠ 0)
    (h1 : aff (evalPL P u) v = 0) (h2 : aff (evalPL Q u) v = 0) :
    v = vtx (xP P Q) (yP P Q) (eval (detP P Q) u) u := by
  simp only [aff, evalPL] at h1 h2
  ext
  · show v.1 = eval (xP P Q) u / eval (detP P Q) u
    rw [eq_div_iff hdet, eval_detP]
    simp only [xP, BernZ.eval_add, BernZ.eval_mul, eval_smul, evalPL]
    push_cast
    linear_combination (eval Q.2.1 u) * h1 - (eval P.2.1 u) * h2
  · show v.2 = eval (yP P Q) u / eval (detP P Q) u
    rw [eq_div_iff hdet, eval_detP]
    simp only [yP, BernZ.eval_add, BernZ.eval_mul, eval_smul, evalPL]
    push_cast
    linear_combination (eval P.1 u) * h2 - (eval Q.1 u) * h1

lemma detP_swap (P Q : PL) (u : ℝ) : eval (detP Q P) u = -eval (detP P Q) u := by
  simp only [eval_detP]; ring

/-! ## 2.  Certificates for a pair of lines on sub-bins -/

/-- What a sub-bin `[b0, b1]` shows about the vertex of a pair: it lies outside the region (side
`k` is negative there, with `u^m` divided out of the numerator), or the bound holds there. -/
inductive Kind where
  | out (k m : ℕ)
  | val (c : VCert)

/-- A sub-bin: its upper end, the sign of `Δ` and the power of `u` dividing `Δ`, and its kind. -/
structure SubBin where
  b1 : ℕ
  σ : Bool
  m : ℕ
  kind : Kind

/-- `σ ·` a polynomial. -/
def sgn (σ : Bool) (p : Poly) : Poly := if σ then p else smul (-1) p

/-- The test of one sub-bin of the pair `(P, Q)`. -/
def subOk (D W R : ℕ) (side : List PL) (chs cvs : List SegE) (crs : List RectM)
    (hbx vbx : List (List ℕ × List ℕ)) (P Q : PL)
    (b0 : ℕ) (sb : SubBin) : Bool :=
  let Δ := detP P Q; let X := xP P Q; let Y := yP P Q
  Nat.blt b0 sb.b1 && signOk sb.σ Δ sb.m b0 sb.b1 R &&
    match sb.kind with
    | .out k m =>
      let S := side.getD k ([0], [0], [0])
      let nm := (SL.atV ⟨S, 0, 0, 0, 1⟩ Δ X Y).num
      decide (k < side.length) && (nm.take m).all (· == 0) &&
        checkPos (sgn (!sb.σ) (nm.drop m)) ((nm.drop m).length - 1) b0 sb.b1 R
    | .val c => c.splits.all (fun sp => sp.q.d != 0) &&
      LemmaEK.vertOkK D W sb.σ Δ X Y b0 sb.b1 R LemmaEK.kK chs cvs crs hbx vbx c

/-- A pair's certificate: parallel, or sub-bins covering `[U0, U1]` in order. -/
inductive PairCert where
  | par
  | bins (sbs : List SubBin)

def binsOk (D W R : ℕ) (side : List PL) (chs cvs : List SegE) (crs : List RectM)
    (hbx vbx : List (List ℕ × List ℕ)) (P Q : PL) :
    ℕ → ℕ → List SubBin → Bool
  | b0, U1, [] => b0 == U1
  | b0, U1, sb :: sbs =>
    subOk D W R side chs cvs crs hbx vbx P Q b0 sb &&
      binsOk D W R side chs cvs crs hbx vbx P Q sb.b1 U1 sbs

def pairOk (D W R U0 U1 : ℕ) (side : List PL) (chs cvs : List SegE) (crs : List RectM)
    (hbx vbx : List (List ℕ × List ℕ)) (P Q : PL) :
    PairCert → Bool
  | .par => (detP P Q).all (· == 0)
  | .bins sbs => binsOk D W R side chs cvs crs hbx vbx P Q U0 U1 sbs

/-- One row: the certificates of `P` with the later lines `Ps` in order. -/
def rowOk (D W R U0 U1 : ℕ) (side : List PL) (chs cvs : List SegE) (crs : List RectM)
    (hbx vbx : List (List ℕ × List ℕ)) (P : PL) (Ps : List PL) (cs : List PairCert) : Bool :=
  cs.length == Ps.length && (Ps.zip cs).all (fun q => pairOk D W R U0 U1 side chs cvs crs hbx vbx P q.1 q.2)

/-- All pairs `i < j` of a list, the certificates of `L[i]` with the later lines in order. -/
def allPairsOk (D W R U0 U1 : ℕ) (side : List PL) (chs cvs : List SegE) (crs : List RectM)
    (hbx vbx : List (List ℕ × List ℕ)) :
    List PL → List (List PairCert) → Bool
  | [], _ => true
  | _ :: _, [] => false
  | P :: Ps, cs :: css =>
    rowOk D W R U0 U1 side chs cvs crs hbx vbx P Ps cs &&
      allPairsOk D W R U0 U1 side chs cvs crs hbx vbx Ps css

/-! ### Splitting the check into small theorems

A leaf is checked row by row, or pair by pair, each in its own `decide`; these steps glue the
pieces back together along `List.drop`. -/

lemma all_drop_step {α : Type*} (p : α → Bool) (l : List α) (i : ℕ) (d : α) (hi : i < l.length)
    (h1 : p (l.getD i d) = true) (h2 : (l.drop (i + 1)).all p = true) : (l.drop i).all p = true := by
  rw [List.drop_eq_getElem_cons hi, List.all_cons, h2, Bool.and_true]
  rwa [List.getD_eq_getElem _ _ hi] at h1

lemma all_drop_end {α : Type*} (p : α → Bool) (l : List α) (m : ℕ) (h : l.length ≤ m) :
    (l.drop m).all p = true := by
  simp [List.drop_eq_nil_of_le h]

lemma rowOk_of {D W R U0 U1 : ℕ} {side : List PL} {chs cvs : List SegE} {crs : List RectM}
    {hbx vbx : List (List ℕ × List ℕ)} {P : PL} {Ps : List PL} {cs : List PairCert}
    (hl : cs.length = Ps.length)
    (h : ((Ps.zip cs).drop 0).all (fun q => pairOk D W R U0 U1 side chs cvs crs hbx vbx P q.1 q.2) = true) :
    rowOk D W R U0 U1 side chs cvs crs hbx vbx P Ps cs = true := by
  simpa [rowOk, hl] using h

lemma allPairsOk_drop_step {D W R U0 U1 : ℕ} {side : List PL} {chs cvs : List SegE} {crs : List RectM}
    {hbx vbx : List (List ℕ × List ℕ)} (L : List PL) (C : List (List PairCert)) (i : ℕ) (d : PL)
    (hi : i < L.length) (hc : i < C.length)
    (h1 : rowOk D W R U0 U1 side chs cvs crs hbx vbx (L.getD i d) (L.drop (i + 1)) (C.getD i []) = true)
    (h2 : allPairsOk D W R U0 U1 side chs cvs crs hbx vbx (L.drop (i + 1)) (C.drop (i + 1)) = true) :
    allPairsOk D W R U0 U1 side chs cvs crs hbx vbx (L.drop i) (C.drop i) = true := by
  rw [List.drop_eq_getElem_cons hi, List.drop_eq_getElem_cons hc, allPairsOk, h2, Bool.and_true]
  rwa [List.getD_eq_getElem _ _ hi, List.getD_eq_getElem _ _ hc] at h1

lemma allPairsOk_drop_end {D W R U0 U1 : ℕ} {side : List PL} {chs cvs : List SegE} {crs : List RectM}
    {hbx vbx : List (List ℕ × List ℕ)} (L : List PL) (C : List (List PairCert)) (m : ℕ) (h : L.length ≤ m) :
    allPairsOk D W R U0 U1 side chs cvs crs hbx vbx (L.drop m) C = true := by
  simp [List.drop_eq_nil_of_le h, allPairsOk]

/-! ## 3.  Soundness of the pair certificates -/

/-- The common hypotheses on the claims. -/
structure Claims (D : ℕ) (chs cvs : List SegE) : Prop where
  hD : 0 < D
  hch : ∀ e ∈ chs, e.1 < e.2.2.1
  hcv : ∀ e ∈ cvs, e.2.1 < e.2.2.2.1

/-- The bound `fE` at `θ = 2 arctan u` for the claims. -/
noncomputable def fEu (D : ℕ) (chs cvs : List SegE) (crs : List RectM) (u : ℝ) (p : ℝ × ℝ) : ℝ :=
  fE (Real.sin (2 * Real.arctan u)) (Real.cos (2 * Real.arctan u))
    (chs.map (hsegT (2 * Real.arctan u) D) ++ cvs.map (vsegT (2 * Real.arctan u) D))
    (crs.map (rectT (2 * Real.arctan u) D)) p

lemma binsOk_find {D W R : ℕ} {side : List PL} {chs cvs : List SegE} {crs : List RectM}
    {hbx vbx : List (List ℕ × List ℕ)} {P Q : PL}
    {u : ℝ} (hR : 0 < R) :
    ∀ (sbs : List SubBin) (b0 U1 : ℕ), binsOk D W R side chs cvs crs hbx vbx P Q b0 U1 sbs = true →
      (b0 : ℝ) / R < u → u ≤ (U1 : ℝ) / R →
      ∃ b0' : ℕ, ∃ sb : SubBin, subOk D W R side chs cvs crs hbx vbx P Q b0' sb = true ∧
        (b0' : ℝ) / R ≤ u ∧ u ≤ (sb.b1 : ℝ) / R
  | [], b0, U1, h, h0, h1 => by
    simp only [binsOk, beq_iff_eq] at h
    subst h; linarith
  | sb :: sbs, b0, U1, h, h0, h1 => by
    simp only [binsOk, Bool.and_eq_true] at h
    by_cases hu : u ≤ (sb.b1 : ℝ) / R
    · exact ⟨b0, sb, h.1, h0.le, hu⟩
    · exact binsOk_find hR sbs sb.b1 U1 h.2 (not_le.mp hu) h1

/-- **One pair**: if two lines of a certified pair meet at a point of the region, the bound holds
there. -/
theorem pair_sound {D W R U0 U1 : ℕ} {side : List PL} {chs cvs : List SegE} {crs : List RectM}
    {hbx vbx : List (List ℕ × List ℕ)}
    (hcl : Claims D chs cvs) (hmd : ∀ r ∈ crs, modeP r.2.1 = true ∧ modeP r.2.2.1 = true ∧ ckOk r.2.2.2 = true) (hR : 0 < R)
    {P Q : PL} {cert : PairCert}
    (hok : pairOk D W R U0 U1 side chs cvs crs hbx vbx P Q cert = true) {u : ℝ} (hu0 : (U0 : ℝ) / R < u)
    (hu1 : u ≤ (U1 : ℝ) / R) (hpos : 0 < u) (hlt : u < 1) {v : ℝ × ℝ}
    (hdet : eval (detP P Q) u ≠ 0) (h1 : aff (evalPL P u) v = 0) (h2 : aff (evalPL Q u) v = 0)
    (hv : v ∈ poly (side.map (evalPL · u)))
    (hbd : ∀ p ∈ poly (side.map (evalPL · u)), BoxDom D u p chs cvs hbx vbx) :
    (W : ℝ) ≤ fEu D chs cvs crs u v := by
  cases cert with
  | par =>
    exfalso; apply hdet
    simp only [pairOk, List.all_eq_true, beq_iff_eq] at hok
    rw [eval_eq_sum]
    refine Finset.sum_eq_zero fun k hk => ?_
    have : (detP P Q).getD k 0 = 0 := by
      rw [List.getD_eq_getElem _ _ (Finset.mem_range.mp hk)]
      exact hok _ (List.getElem_mem _)
    rw [this]; simp
  | bins sbs =>
    simp only [pairOk] at hok
    obtain ⟨b0, sb, hsub, hb0, hb1⟩ := binsOk_find hR sbs U0 U1 hok hu0 hu1
    have hv' := cramer P Q u v hdet h1 h2
    simp only [subOk, Bool.and_eq_true, Nat.blt_eq] at hsub
    obtain ⟨⟨_, hsg⟩, hk⟩ := hsub
    have hσ := sign_of_signOk hsg hR hpos hb0 hb1
    have hδ : eval (detP P Q) u ≠ 0 := by split_ifs at hσ <;> [exact hσ.ne'; exact hσ.ne]
    have ctx : VCtx (LemmaEK.ckP (LemmaEK.mkCtx (detP P Q) (xP P Q) (yP P Q) b0 sb.b1 R LemmaEK.kK) sb.σ)
        (detP P Q) (xP P Q) (yP P Q) sb.σ b0 sb.b1 R u (eval (detP P Q) u) :=
      ⟨hR, hpos, hlt, hb0, hb1, rfl, hσ, LemmaEK.ckP_hck hR ⟨hpos, hlt, hδ⟩ hσ hb0 hb1⟩
    rcases hsbk : sb.kind with ⟨k, m⟩ | c
    · -- outside the region: a contradiction
      rw [hsbk] at hk
      simp only [Bool.and_eq_true, decide_eq_true_eq] at hk
      obtain ⟨⟨hkl, hz⟩, hp⟩ := hk
      exfalso
      set S := side.getD k ([0], [0], [0])
      have hS : S ∈ side := getD_mem _ hkl
      have hge := hv (evalPL S u) (List.mem_map_of_mem hS)
      set nm := (SL.atV ⟨S, 0, 0, 0, 1⟩ (detP P Q) (xP P Q) (yP P Q)).num
      have hpos' := pos_of_checkPos hp hR hb0 hb1
      have hnm := eval_take_drop nm m hz u
      have hat : eval nm u / eval (detP P Q) u = aff (evalPL S u) v := by
        have e1 := eval_atV (⟨S, 0, 0, 0, 1⟩ : SL) (detP P Q) (xP P Q) (yP P Q) rfl ctx.ok.hδ
        have hden : den (SL.atV ⟨S, 0, 0, 0, 1⟩ (detP P Q) (xP P Q) (yP P Q)) (eval (detP P Q) u) u =
            eval (detP P Q) u := by simp [den, SL.atV]
        rw [RF.eval, hden] at e1
        refine e1.trans ?_
        rw [hv']
        simp [SL.val, sden, vtx]
      have hum : 0 < u ^ m := pow_pos hpos m
      have key : aff (evalPL S u) v < 0 := by
        rw [← hat, hnm]
        cases hσ' : sb.σ
        · rw [hσ'] at hσ hpos'
          simp only [Bool.false_eq_true, if_false] at hσ
          simp only [sgn, Bool.not_false, if_true] at hpos'
          exact div_neg_of_pos_of_neg (mul_pos hum hpos') hσ
        · rw [hσ'] at hσ hpos'
          simp only [if_true] at hσ
          simp only [sgn, Bool.not_true, Bool.false_eq_true, if_false, eval_smul] at hpos'
          push_cast at hpos'
          exact div_neg_of_neg_of_pos (mul_neg_of_pos_of_neg hum (by linarith)) hσ
      simp only [aff] at key hge
      linarith
    · rw [hsbk] at hk
      rw [hv']
      simp only [Bool.and_eq_true, List.all_eq_true, bne_iff_ne, ne_eq] at hk
      exact vertOk_sound hcl.hD ctx hcl.hch hcl.hcv (by rw [← hv']; exact hbd v hv) hk.1 hmd
        (LemmaEK.vertOkK'_imp (LemmaEK.mkCtx_ok hR) hk.2)

/-- **All pairs**: every pair `i < j` of the list has a passing certificate. -/
lemma allPairs_sound {D W R U0 U1 : ℕ} {side : List PL} {chs cvs : List SegE} {crs : List RectM}
    {hbx vbx : List (List ℕ × List ℕ)} :
    ∀ (L : List PL) (css : List (List PairCert)), allPairsOk D W R U0 U1 side chs cvs crs hbx vbx L css = true →
      ∀ (i j : ℕ) (hi : i < j) (hj : j < L.length),
        ∃ c, pairOk D W R U0 U1 side chs cvs crs hbx vbx (L[i]'(by omega)) (L[j]) c = true
  | [], _, _, i, j, _, hj => absurd hj (by simp)
  | _ :: _, [], h, _, _, _, _ => by simp [allPairsOk] at h
  | P :: Ps, cs :: css, h, i, j, hij, hj => by
    simp only [allPairsOk, rowOk, Bool.and_eq_true, beq_iff_eq, List.all_eq_true] at h
    obtain ⟨⟨hl, hall⟩, hrest⟩ := h
    cases i with
    | zero =>
      obtain ⟨j', rfl⟩ : ∃ j', j = j' + 1 := ⟨j - 1, by omega⟩
      have hj' : j' < Ps.length := by simpa using hj
      have hmem : (Ps[j'], cs[j']'(by omega)) ∈ Ps.zip cs := by
        rw [List.mem_iff_getElem]
        exact ⟨j', by simp [hl]; omega, by simp⟩
      exact ⟨_, hall _ hmem⟩
    | succ i =>
      obtain ⟨j', rfl⟩ : ∃ j', j = j' + 1 := ⟨j - 1, by omega⟩
      obtain ⟨c, hc⟩ := allPairs_sound Ps css hrest i j' (by omega) (by simpa using hj)
      exact ⟨c, by simpa using hc⟩

/-! ## 4.  The region and the pinning of forms -/

/-- The region's four sides: the lower `x` side is the box side `Q x ≥ x0` or the wall
`2N x ≥ C + S` (`x ≥ w/2`), the upper side `Q x ≤ x1`; likewise in `y`. -/
def sideL (Q x0 x1 y0 y1 : ℕ) (wx wy : Bool) : List PL :=
  [if wx then (smul 2 Np, [0], smul (-1) (BernZ.add Cp Sp)) else ([(Q : ℤ)], [0], [-(x0 : ℤ)]),
    ([-(Q : ℤ)], [0], [(x1 : ℤ)]),
    if wy then ([0], smul 2 Np, smul (-1) (BernZ.add Cp Sp)) else ([0], [(Q : ℤ)], [-(y0 : ℤ)]),
    ([0], [-(Q : ℤ)], [(y1 : ℤ)])]

/-- The wall lines `c₁ ≥ w/2`, `c₂ ≥ w/2` (`w = (C + S)/N`). -/
def wallX : PL := (smul 2 Np, [0], smul (-1) (BernZ.add Cp Sp))
def wallY : PL := ([0], smul 2 Np, smul (-1) (BernZ.add Cp Sp))

/-- The region with extra wall constraints (`ex`, `ey`): for a box whose side the wall crosses
inside the bin, both the side and the wall bound the admissible centres. -/
def sideE (Q x0 x1 y0 y1 : ℕ) (wx wy ex ey : Bool) : List PL :=
  sideL Q x0 x1 y0 y1 wx wy ++ ((if ex then [wallX] else []) ++ (if ey then [wallY] else []))

lemma poly_sideE_sub {Q x0 x1 y0 y1 : ℕ} {wx wy ex ey : Bool} (u : ℝ) :
    poly ((sideE Q x0 x1 y0 y1 wx wy ex ey).map (evalPL · u)) ⊆
      poly ((sideL Q x0 x1 y0 y1 wx wy).map (evalPL · u)) := fun p hp C hC =>
  hp C (by simp only [sideE, List.map_append, List.mem_append]; exact Or.inl hC)

/-- The lower ends of the region (`RF`s without `Δ`). -/
def loX (Q x0 : ℕ) (wx : Bool) : RF := if wx then ⟨BernZ.add Cp Sp, 0, 0, 0, 1, 2⟩ else RF.const x0 Q

lemma eval_loX {Q x0 : ℕ} (hQ : 0 < Q) (wx : Bool) (δ u : ℝ) :
    (loX Q x0 wx).eval δ u = if wx then (1 - u ^ 2 + 2 * u) / (2 * (1 + u ^ 2)) else (x0 : ℝ) / Q := by
  unfold loX; split_ifs
  · simp only [RF.eval, den, BernZ.eval_add, eval_Cp, eval_Sp]; push_cast; ring
  · rw [eval_const]; push_cast; rfl

/-- The region is the rectangle `[loX, x1/Q] × [loY, y1/Q]`. -/
lemma mem_region {Q x0 x1 y0 y1 : ℕ} (hQ : 0 < Q) {wx wy : Bool} {u : ℝ} {p : ℝ × ℝ}
    (hp : p ∈ poly ((sideL Q x0 x1 y0 y1 wx wy).map (evalPL · u))) :
    (loX Q x0 wx).eval 1 u ≤ p.1 ∧ p.1 ≤ (x1 : ℝ) / Q ∧ (loX Q y0 wy).eval 1 u ≤ p.2 ∧
      p.2 ≤ (y1 : ℝ) / Q := by
  have hQr : (0 : ℝ) < Q := by exact_mod_cast hQ
  have hN : (0 : ℝ) < 1 + u ^ 2 := by positivity
  have h := fun C (hC : C ∈ sideL Q x0 x1 y0 y1 wx wy) => hp _ (List.mem_map_of_mem hC)
  simp only [sideL, List.mem_cons, List.not_mem_nil, or_false, forall_eq_or_imp, forall_eq] at h
  obtain ⟨h1, h2, h3, h4⟩ := h
  rw [eval_loX hQ, eval_loX hQ]
  refine ⟨?_, ?_, ?_, ?_⟩
  · split_ifs at h1 ⊢
    · simp only [evalPL, eval_smul, eval_Np, BernZ.eval_add, eval_Cp, eval_Sp, eval_cons, eval_nil]
        at h1
      push_cast at h1
      rw [div_le_iff₀ (by positivity)]; nlinarith
    · simp only [evalPL, eval_cons, eval_nil] at h1
      push_cast at h1
      rw [div_le_iff₀ hQr]; nlinarith
  · simp only [evalPL, eval_cons, eval_nil] at h2
    push_cast at h2
    rw [le_div_iff₀ hQr]; nlinarith
  · split_ifs at h3 ⊢
    · simp only [evalPL, eval_smul, eval_Np, BernZ.eval_add, eval_Cp, eval_Sp, eval_cons, eval_nil]
        at h3
      push_cast at h3
      rw [div_le_iff₀ (by positivity)]; nlinarith
    · simp only [evalPL, eval_cons, eval_nil] at h3
      push_cast at h3
      rw [div_le_iff₀ hQr]; nlinarith
  · simp only [evalPL, eval_cons, eval_nil] at h4
    push_cast at h4
    rw [le_div_iff₀ hQr]; nlinarith

lemma region_bounded {Q x0 x1 y0 y1 : ℕ} (hQ : 0 < Q) (wx wy : Bool) (u : ℝ) :
    Bornology.IsBounded (poly ((sideL Q x0 x1 y0 y1 wx wy).map (evalPL · u))) := by
  refine (Metric.isBounded_Icc ((loX Q x0 wx).eval 1 u, (loX Q y0 wy).eval 1 u)
    ((x1 : ℝ) / Q, (y1 : ℝ) / Q)).subset fun p hp => ?_
  obtain ⟨a, b, c, d⟩ := mem_region hQ hp
  exact ⟨⟨a, c⟩, ⟨b, d⟩⟩

/-- The value of a line at a point given by two `RF`s (no `Δ`: pass `Δ = [1]`). -/
def affRF (P : PL) (x y : RF) : RF :=
  RF.add [1] (RF.add [1] (RF.mul ⟨P.1, 0, 0, 0, 0, 1⟩ x) (RF.mul ⟨P.2.1, 0, 0, 0, 0, 1⟩ y))
    ⟨P.2.2, 0, 0, 0, 0, 1⟩

lemma affRF_d (P : PL) {x y : RF} (hx : x.d ≠ 0) (hy : y.d ≠ 0) : (affRF P x y).d ≠ 0 := by
  simp only [affRF]
  exact RF.add_d _ (RF.add_d _ (by simp [RF.mul, hx]) (by simp [RF.mul, hy])) (by simp)

lemma eval_affRF (P : PL) {x y : RF} (hx : x.d ≠ 0) (hy : y.d ≠ 0) {u : ℝ} (hu0 : 0 < u)
    (hu1 : u < 1) : (affRF P x y).eval 1 u = aff (evalPL P u) (x.eval 1 u, y.eval 1 u) := by
  have ok : Ok 1 u := ⟨hu0, hu1, one_ne_zero⟩
  have e1 : BernZ.eval [1] u = 1 := by simp
  unfold affRF
  rw [eval_add ok e1 (RF.add_d _ (by simp [RF.mul, hx]) (by simp [RF.mul, hy])) (by simp),
    eval_add ok e1 (by simp [RF.mul, hx]) (by simp [RF.mul, hy]), eval_mul ok (by simp) hx,
    eval_mul ok (by simp) hy]
  simp [RF.eval, den, aff, evalPL]

/-- A corner coordinate as a quotient of polynomials: `x/Q`, or the wall `(C + S)/(2N)`. -/
def cnum (x : ℕ) (w : Bool) : Poly := if w then BernZ.add Cp Sp else [(x : ℤ)]
def cden (Q : ℕ) (w : Bool) : Poly := if w then smul 2 Np else [(Q : ℤ)]

lemma eval_cden_pos {Q : ℕ} (hQ : 0 < Q) (w : Bool) (u : ℝ) : 0 < eval (cden Q w) u := by
  unfold cden; split_ifs
  · rw [eval_smul, eval_Np]; push_cast; positivity
  · simp; exact_mod_cast hQ

lemma loX_eq {Q : ℕ} (hQ : 0 < Q) (x : ℕ) (w : Bool) (u : ℝ) :
    (loX Q x w).eval 1 u = eval (cnum x w) u / eval (cden Q w) u := by
  rw [eval_loX hQ]
  unfold cnum cden; split_ifs
  · rw [BernZ.eval_add, eval_Cp, eval_Sp, eval_smul, eval_Np]; push_cast; ring
  · simp

/-- `aff P (nx/dx, ny/dy) · dx · dy` as a polynomial. -/
def cornerPoly (P : PL) (nx dx ny dy : Poly) : Poly :=
  BernZ.add (BernZ.add (BernZ.mul P.1 (BernZ.mul nx dy)) (BernZ.mul P.2.1 (BernZ.mul ny dx)))
    (BernZ.mul P.2.2 (BernZ.mul dx dy))

lemma eval_cornerPoly (P : PL) (nx dx ny dy : Poly) (u : ℝ) (hx : eval dx u ≠ 0)
    (hy : eval dy u ≠ 0) :
    eval (cornerPoly P nx dx ny dy) u =
      aff (evalPL P u) (eval nx u / eval dx u, eval ny u / eval dy u) * (eval dx u * eval dy u) := by
  simp only [cornerPoly, BernZ.eval_add, BernZ.eval_mul, aff, evalPL]
  field_simp

/-- A form is `≥ 0` (`neg = false`) or `≤ 0` (`neg = true`) at the four corners of the region. -/
def cornersOk (Q x0 x1 y0 y1 U0 U1 R : ℕ) (wx wy neg : Bool) (P : PL) : Bool :=
  [(cnum x0 wx, cden Q wx, cnum y0 wy, cden Q wy), (cnum x0 wx, cden Q wx, cnum y1 false, cden Q false),
    (cnum x1 false, cden Q false, cnum y0 wy, cden Q wy),
    (cnum x1 false, cden Q false, cnum y1 false, cden Q false)].all fun c =>
    BernZ.check (if neg then smul (-1) (cornerPoly P c.1 c.2.1 c.2.2.1 c.2.2.2)
      else cornerPoly P c.1 c.2.1 c.2.2.1 c.2.2.2)
      ((cornerPoly P c.1 c.2.1 c.2.2.1 c.2.2.2).length - 1) U0 U1 R

lemma affine_nonneg_rect {a b k xl xh yl yh x y : ℝ} (hx0 : xl ≤ x) (hx1 : x ≤ xh) (hy0 : yl ≤ y)
    (hy1 : y ≤ yh) (c00 : 0 ≤ a * xl + b * yl + k) (c01 : 0 ≤ a * xl + b * yh + k)
    (c10 : 0 ≤ a * xh + b * yl + k) (c11 : 0 ≤ a * xh + b * yh + k) : 0 ≤ a * x + b * y + k := by
  rcases le_total 0 a with ha | ha <;> rcases le_total 0 b with hb | hb
  · nlinarith [mul_le_mul_of_nonneg_left hx0 ha, mul_le_mul_of_nonneg_left hy0 hb]
  · nlinarith [mul_le_mul_of_nonneg_left hx0 ha, mul_le_mul_of_nonpos_left hy1 hb]
  · nlinarith [mul_le_mul_of_nonpos_left hx1 ha, mul_le_mul_of_nonneg_left hy0 hb]
  · nlinarith [mul_le_mul_of_nonpos_left hx1 ha, mul_le_mul_of_nonpos_left hy1 hb]

/-- **The corner test**: a form `≥ 0` (or `≤ 0`) at the four corners has that sign on the region. -/
lemma corners_sound {Q x0 x1 y0 y1 U0 U1 R : ℕ} (hQ : 0 < Q) (hR : 0 < R) {wx wy neg : Bool}
    {P : PL} (h : cornersOk Q x0 x1 y0 y1 U0 U1 R wx wy neg P = true) {u : ℝ} (hu0 : 0 < u)
    (hu1 : u < 1) (hb0 : (U0 : ℝ) / R ≤ u) (hb1 : u ≤ (U1 : ℝ) / R) :
    ∀ p ∈ poly ((sideL Q x0 x1 y0 y1 wx wy).map (evalPL · u)),
      if neg then aff (evalPL P u) p ≤ 0 else 0 ≤ aff (evalPL P u) p := by
  intro p hp
  obtain ⟨hx0, hx1, hy0, hy1⟩ := mem_region hQ hp
  rw [loX_eq hQ] at hx0 hy0
  have hcq : ∀ z : ℕ, (z : ℝ) / Q = eval (cnum z false) u / eval (cden Q false) u := by
    intro z; simp [cnum, cden]
  rw [hcq] at hx1 hy1
  simp only [cornersOk, List.all_cons, List.all_nil, Bool.and_true, Bool.and_eq_true] at h
  obtain ⟨c1, c2, c3, c4⟩ := h
  have val : ∀ (nx dx ny dy : Poly), 0 < eval dx u → 0 < eval dy u →
      BernZ.check (if neg then smul (-1) (cornerPoly P nx dx ny dy) else cornerPoly P nx dx ny dy)
        ((cornerPoly P nx dx ny dy).length - 1) U0 U1 R = true →
      if neg then aff (evalPL P u) (eval nx u / eval dx u, eval ny u / eval dy u) ≤ 0
        else 0 ≤ aff (evalPL P u) (eval nx u / eval dx u, eval ny u / eval dy u) := by
    intro nx dx ny dy hx hy hc
    have h0 := BernZ.nonneg_of_check hc hR hb0 hb1
    have hxy := mul_pos hx hy
    split_ifs at h0 ⊢
    · rw [eval_smul, eval_cornerPoly P nx dx ny dy u hx.ne' hy.ne'] at h0
      push_cast at h0
      by_contra hc'; push_neg at hc'
      have := mul_pos hc' hxy; linarith
    · rw [eval_cornerPoly P nx dx ny dy u hx.ne' hy.ne'] at h0
      by_contra hc'; push_neg at hc'
      have := mul_neg_of_neg_of_pos hc' hxy; linarith
  have v1 := val _ _ _ _ (eval_cden_pos hQ wx u) (eval_cden_pos hQ wy u) c1
  have v2 := val _ _ _ _ (eval_cden_pos hQ wx u) (eval_cden_pos hQ false u) c2
  have v3 := val _ _ _ _ (eval_cden_pos hQ false u) (eval_cden_pos hQ wy u) c3
  have v4 := val _ _ _ _ (eval_cden_pos hQ false u) (eval_cden_pos hQ false u) c4
  simp only [aff, evalPL] at v1 v2 v3 v4 ⊢
  split_ifs at v1 v2 v3 v4 ⊢
  · have := affine_nonneg_rect (a := -eval P.1 u) (b := -eval P.2.1 u) (k := -eval P.2.2 u)
      hx0 hx1 hy0 hy1 (by linarith) (by linarith) (by linarith) (by linarith)
    linarith
  · exact affine_nonneg_rect hx0 hx1 hy0 hy1 v1 v2 v3 v4

/-! ### Pinning -/

/-- A scaled line is pinned: its line is in `Ls`, or it is `≥ 0` / `≤ 0` at the corners. -/
def pinOk (Q x0 x1 y0 y1 U0 U1 R : ℕ) (wx wy : Bool) (Ls : List PL) (L : SL) : Bool :=
  Ls.contains L.P || cornersOk Q x0 x1 y0 y1 U0 U1 R wx wy false L.P ||
    cornersOk Q x0 x1 y0 y1 U0 U1 R wx wy true L.P

lemma pin_sound {Q x0 x1 y0 y1 U0 U1 R : ℕ} (hQ : 0 < Q) (hR : 0 < R) {wx wy : Bool}
    {Ls : List PL} {L : SL} (h : pinOk Q x0 x1 y0 y1 U0 U1 R wx wy Ls L = true) (hd : L.d ≠ 0)
    {u : ℝ} (hu0 : 0 < u) (hu1 : u < 1) (hb0 : (U0 : ℝ) / R ≤ u) (hb1 : u ≤ (U1 : ℝ) / R)
    {F : ℝ × ℝ × ℝ} (hF : ∀ c, aff F c = L.val u c) :
    Pinned (poly ((sideL Q x0 x1 y0 y1 wx wy).map (evalPL · u))) (Ls.map (evalPL · u)) F := by
  simp only [pinOk, Bool.or_eq_true, List.contains_iff_mem] at h
  have hsd := sden_pos L hd hu0 hu1
  rcases h with (h | h) | h
  · exact Or.inl (posMul_of_SL L hd hu0 hu1 hF (List.mem_map_of_mem h))
  · right; left; intro p hp
    have := corners_sound hQ hR h hu0 hu1 hb0 hb1 p hp
    simp only [Bool.false_eq_true, if_false] at this
    rw [hF, SL.val]; exact div_nonneg this hsd.le
  · right; right; intro p hp
    have := corners_sound hQ hR h hu0 hu1 hb0 hb1 p hp
    simp only [if_true] at this
    rw [hF, SL.val]; exact div_nonpos_of_nonpos_of_nonneg this hsd.le

/-- The scaled lines of `formsOf`, in the same order. -/
def formsSL (A B lo1 lo2 up1 up2 : SL) : List SL :=
  [up1.sub A, up2.sub A, B.sub lo1, B.sub lo2, up1.sub lo1, up1.sub lo2, up2.sub lo1, up2.sub lo2]

lemma formsSL_match {u : ℝ} (hu0 : 0 < u) (hu1 : u < 1) {A B : ℝ} {lo1 lo2 up1 up2 : ℝ × ℝ × ℝ}
    {A' B' lo1' lo2' up1' up2' : SL} (dA : A'.d ≠ 0) (dB : B'.d ≠ 0) (d1 : lo1'.d ≠ 0)
    (d2 : lo2'.d ≠ 0) (d3 : up1'.d ≠ 0) (d4 : up2'.d ≠ 0)
    (eA : ∀ c, A'.val u c = A) (eB : ∀ c, B'.val u c = B) (e1 : ∀ c, aff lo1 c = lo1'.val u c)
    (e2 : ∀ c, aff lo2 c = lo2'.val u c) (e3 : ∀ c, aff up1 c = up1'.val u c)
    (e4 : ∀ c, aff up2 c = up2'.val u c) :
    ∀ F ∈ formsOf A B lo1 lo2 up1 up2, ∃ L ∈ formsSL A' B' lo1' lo2' up1' up2', L.d ≠ 0 ∧
      ∀ c, aff F c = L.val u c := by
  intro F hF
  simp only [formsOf, List.mem_cons, List.not_mem_nil, or_false] at hF
  simp only [formsSL, List.mem_cons, List.not_mem_nil, or_false, exists_eq_or_imp, exists_eq_left]
  rcases hF with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · left; exact ⟨Nat.mul_ne_zero d3 dA, fun c => by rw [aff_subF, aff_constF, val_sub _ _ d3 dA hu0 hu1, e3, eA]⟩
  · right; left; exact ⟨Nat.mul_ne_zero d4 dA, fun c => by rw [aff_subF, aff_constF, val_sub _ _ d4 dA hu0 hu1, e4, eA]⟩
  · right; right; left; exact ⟨Nat.mul_ne_zero dB d1, fun c => by rw [aff_subF, aff_constF, val_sub _ _ dB d1 hu0 hu1, e1, eB]⟩
  · right; right; right; left; exact ⟨Nat.mul_ne_zero dB d2, fun c => by rw [aff_subF, aff_constF, val_sub _ _ dB d2 hu0 hu1, e2, eB]⟩
  · right; right; right; right; left; exact ⟨Nat.mul_ne_zero d3 d1, fun c => by rw [aff_subF, val_sub _ _ d3 d1 hu0 hu1, e3, e1]⟩
  · right; right; right; right; right; left; exact ⟨Nat.mul_ne_zero d3 d2, fun c => by rw [aff_subF, val_sub _ _ d3 d2 hu0 hu1, e3, e2]⟩
  · right; right; right; right; right; right; left; exact ⟨Nat.mul_ne_zero d4 d1, fun c => by rw [aff_subF, val_sub _ _ d4 d1 hu0 hu1, e4, e1]⟩
  · right; right; right; right; right; right; right; exact ⟨Nat.mul_ne_zero d4 d2, fun c => by rw [aff_subF, val_sub _ _ d4 d2 hu0 hu1, e4, e2]⟩

/-- Box-wide dominance of a segment's alternatives: checked at the region's corners. -/
def boxDomOk (Q x0 x1 y0 y1 U0 U1 R : ℕ) (wx wy : Bool) (ups los : List SL) (bx : List ℕ × List ℕ) :
    Bool :=
  ups.all (fun U => bx.1.any fun a =>
      cornersOk Q x0 x1 y0 y1 U0 U1 R wx wy false (U.sub (ups.getD a (SL.cst 0 1))).P) &&
    los.all (fun L => bx.2.any fun b =>
      cornersOk Q x0 x1 y0 y1 U0 U1 R wx wy false ((los.getD b (SL.cst 0 1)).sub L).P)

lemma getD_d {ups : List SL} (hd : ∀ L ∈ ups, L.d ≠ 0) (a : ℕ) : (ups.getD a (SL.cst 0 1)).d ≠ 0 := by
  by_cases h : a < ups.length
  · exact hd _ (getD_mem _ h)
  · rw [List.getD_eq_default _ _ (by omega)]; simp [SL.cst]

lemma boxDom_sound {Q x0 x1 y0 y1 U0 U1 R : ℕ} (hQ : 0 < Q) (hR : 0 < R) {wx wy : Bool}
    {ups los : List SL} {bx : List ℕ × List ℕ}
    (hok : boxDomOk Q x0 x1 y0 y1 U0 U1 R wx wy ups los bx = true)
    (hdu : ∀ L ∈ ups, L.d ≠ 0) (hdl : ∀ L ∈ los, L.d ≠ 0) {u : ℝ} (hu0 : 0 < u) (hu1 : u < 1)
    (hb0 : (U0 : ℝ) / R ≤ u) (hb1 : u ≤ (U1 : ℝ) / R) :
    ∀ p ∈ poly ((sideL Q x0 x1 y0 y1 wx wy).map (evalPL · u)), DomU u p ups bx.1 ∧ DomL u p los bx.2 := by
  intro p hp
  simp only [boxDomOk, Bool.and_eq_true, List.all_eq_true, List.any_eq_true] at hok
  refine ⟨fun U hU => ?_, fun L hL => ?_⟩
  · obtain ⟨a, ha, hc⟩ := hok.1 U hU
    have h0 := corners_sound hQ hR hc hu0 hu1 hb0 hb1 p hp
    simp only [Bool.false_eq_true, if_false] at h0
    have hd1 := hdu U hU
    have hd2 := getD_d hdu a
    have hsd := sden_pos (U.sub (ups.getD a (SL.cst 0 1))) (Nat.mul_ne_zero hd1 hd2) hu0 hu1
    have hv : 0 ≤ (U.sub (ups.getD a (SL.cst 0 1))).val u p := div_nonneg h0 hsd.le
    rw [val_sub _ _ hd1 hd2 hu0 hu1] at hv
    exact ⟨a, ha, by linarith⟩
  · obtain ⟨b, hb, hc⟩ := hok.2 L hL
    have h0 := corners_sound hQ hR hc hu0 hu1 hb0 hb1 p hp
    simp only [Bool.false_eq_true, if_false] at h0
    have hd1 := getD_d hdl b
    have hd2 := hdl L hL
    have hsd := sden_pos ((los.getD b (SL.cst 0 1)).sub L) (Nat.mul_ne_zero hd1 hd2) hu0 hu1
    have hv : 0 ≤ ((los.getD b (SL.cst 0 1)).sub L).val u p := div_nonneg h0 hsd.le
    rw [val_sub _ _ hd1 hd2 hu0 hu1] at hv
    exact ⟨b, hb, by linarith⟩

/-! ## 5.  The `EXACT` leaf -/

/-- The data of a leaf: the lower sides (`wx`, `wy`: wall or box side), the claims, the lines of
the arrangement, and the pair certificates for `sideL ++ Ls`. -/
structure ExLeaf where
  wx : Bool
  wy : Bool
  chs : List SegE
  cvs : List SegE
  crs : List RectM
  Ls : List PL
  hbx : List (List ℕ × List ℕ)
  vbx : List (List ℕ × List ℕ)
  certs : List (List PairCert)
  ex : Bool := false
  ey : Bool := false
  /-- a Lebesgue credit (with no rectangle terms): the target of the vertex test is `W − amt` -/
  cred : Option LebCredit.Cred := none

/-- The credit of a leaf (`0` without one). -/
def credAmt (lf : ExLeaf) : ℕ :=
  match lf.cred with
  | none => 0
  | some cr => cr.amt

/-- The credit's test: no rectangle terms, `amt ≤ W`, and the strips. -/
def credOkL (D S R W x0 x1 y0 y1 U0 U1 : ℕ) (rects : List RectE) (lf : ExLeaf) : Bool :=
  match lf.cred with
  | none => true
  | some cr => lf.crs.isEmpty && Nat.ble cr.amt W &&
      LebCredit.credOk D (D * S) x0 x1 y0 y1 U0 U1 R rects cr

def hFormsSLs (D : ℕ) (e : SegE) : List SL :=
  formsSL (SL.cst e.1 D) (SL.cst e.2.2.1 D) (hTA D e.2.1) (hTB D e.2.1) (hTC D e.2.1) (hTD D e.2.1)
def vFormsSLs (D : ℕ) (e : SegE) : List SL :=
  formsSL (SL.cst e.2.1 D) (SL.cst e.2.2.2.1 D) (vLXs D e.1) (vLYs D e.1) (vUXs D e.1) (vUYs D e.1)
def lebSLs (D : ℕ) (r : RectM) : List SL :=
  [capXm D r, (capXm D r).sub (sSL 1), capYm D r, (capYm D r).sub (sSL 1)]


/-- The `tan` regime of one cap is certified on the region: `d* = n/m ≤ 1` and `d ≥ s`, `d ≥ c`
at its four corners (`d` affine in the centre). -/
def tanAx (Q x0 x1 y0 y1 U0 U1 R : ℕ) (wx wy : Bool) (L : SL) : Option (ℕ × ℕ) → Bool
  | none => true
  | some (n, m) => Nat.blt 0 m && Nat.ble n m &&
      cornersOk Q x0 x1 y0 y1 U0 U1 R wx wy false (L.sub (sSL 1)).P &&
      cornersOk Q x0 x1 y0 y1 U0 U1 R wx wy false (L.sub (cSL 1)).P

def tanOk (Q x0 x1 y0 y1 U0 U1 R : ℕ) (wx wy : Bool) (D : ℕ) (r : RectM) : Bool :=
  tanAx Q x0 x1 y0 y1 U0 U1 R wx wy (capX D r.1.1) r.2.1 &&
    tanAx Q x0 x1 y0 y1 U0 U1 R wx wy (capY D r.1.2.1) r.2.2.1

lemma tanAx_sound {Q x0 x1 y0 y1 U0 U1 R : ℕ} (hQ : 0 < Q) (hR : 0 < R) {wx wy : Bool} {L : SL}
    (hL : L.d ≠ 0) {mo : Option (ℕ × ℕ)} (h : tanAx Q x0 x1 y0 y1 U0 U1 R wx wy L mo = true) {u : ℝ}
    (hu0 : 0 < u) (hu1 : u < 1) (hb0 : (U0 : ℝ) / R ≤ u) (hb1 : u ≤ (U1 : ℝ) / R) :
    modeP mo = true ∧ ∀ p ∈ poly ((sideL Q x0 x1 y0 y1 wx wy).map (evalPL · u)),
      ModeOk (2 * Real.arctan u) mo (L.val u p) := by
  match mo, h with
  | none, _ => exact ⟨rfl, fun _ _ => trivial⟩
  | some (n, m), h =>
    simp only [tanAx, Bool.and_eq_true, Nat.blt_eq, Nat.ble_eq] at h
    obtain ⟨⟨⟨hm, hnm⟩, c1⟩, c2⟩ := h
    refine ⟨by simp [modeP, hm, hnm], fun p hp => ⟨?_, ?_⟩⟩
    · rw [div_le_one (by exact_mod_cast hm)]; exact_mod_cast hnm
    · have ds : (sSL 1).d ≠ 0 := by simp [sSL]
      have dc : (cSL 1).d ≠ 0 := by simp [cSL]
      have k1 := corners_sound hQ hR c1 hu0 hu1 hb0 hb1 p hp
      have k2 := corners_sound hQ hR c2 hu0 hu1 hb0 hb1 p hp
      try simp only [if_false, Bool.false_eq_true] at k1 k2
      have v1 : 0 ≤ (L.sub (sSL 1)).val u p :=
        div_nonneg k1 (sden_pos _ (Nat.mul_ne_zero hL ds) hu0 hu1).le
      have v2 : 0 ≤ (L.sub (cSL 1)).val u p :=
        div_nonneg k2 (sden_pos _ (Nat.mul_ne_zero hL dc) hu0 hu1).le
      rw [val_sub _ _ hL ds hu0 hu1, val_sSL one_ne_zero] at v1
      rw [val_sub _ _ hL dc hu0 hu1, val_cSL one_ne_zero] at v2
      rw [(trig u).1, (trig u).2, max_le_iff]
      try norm_num at v1 v2
      constructor <;> linarith

/-- An affine form signed on the region gives a scaled line signed on the region. -/
lemma sl_sign {Q x0 x1 y0 y1 U0 U1 R : ℕ} (hQ : 0 < Q) (hR : 0 < R) {wx wy neg : Bool} {L : SL}
    (hL : L.d ≠ 0) (h : cornersOk Q x0 x1 y0 y1 U0 U1 R wx wy neg L.P = true) {u : ℝ} (hu0 : 0 < u)
    (hu1 : u < 1) (hb0 : (U0 : ℝ) / R ≤ u) (hb1 : u ≤ (U1 : ℝ) / R) :
    ∀ p ∈ poly ((sideL Q x0 x1 y0 y1 wx wy).map (evalPL · u)),
      if neg then L.val u p ≤ 0 else 0 ≤ L.val u p := by
  intro p hp
  have k := corners_sound hQ hR h hu0 hu1 hb0 hb1 p hp
  have hd := sden_pos L hL hu0 hu1
  cases neg
  · exact div_nonneg (by simpa using k) hd.le
  · exact div_nonpos_of_nonpos_of_nonneg (by simpa using k) hd.le

/-- `x − q c₁` (`fst`) or `x − q c₂`: the anchor side of a centre coordinate. -/
def ancPL (x q : ℕ) (fst : Bool) : PL :=
  if fst then ([-(q : ℤ)], [0], [(x : ℤ)]) else ([0], [-(q : ℤ)], [(x : ℤ)])

/-- The McCormick anchor `(xa, ya)/q` is a corner of the region on the same side in both
coordinates: `(xa/q − c₁)(ya/q − c₂) ≥ 0`. -/
def ancOk (Q x0 x1 y0 y1 U0 U1 R : ℕ) (wx wy : Bool) (xa ya q : ℕ) : Bool :=
  (cornersOk Q x0 x1 y0 y1 U0 U1 R wx wy false (ancPL xa q true) &&
    cornersOk Q x0 x1 y0 y1 U0 U1 R wx wy false (ancPL ya q false)) ||
  (cornersOk Q x0 x1 y0 y1 U0 U1 R wx wy true (ancPL xa q true) &&
    cornersOk Q x0 x1 y0 y1 U0 U1 R wx wy true (ancPL ya q false))

/-- `c·α + s·β − 1` for scaled lines `α`, `β`, over `N · den α · den β`. -/
def xiPL (A B : SL) : PL :=
  addPL (addPL (mulPL (BernZ.mul Cp (sdenP B)) A.P) (mulPL (BernZ.mul Sp (sdenP A)) B.P))
    ([0], [0], smul (-1) (BernZ.mul Np (BernZ.mul (sdenP A) (sdenP B))))

lemma aff_xiPL (A B : SL) (hA : A.d ≠ 0) (hB : B.d ≠ 0) {u : ℝ} (hu0 : 0 < u) (hu1 : u < 1)
    (p : ℝ × ℝ) : aff (evalPL (xiPL A B) u) p = (1 + u ^ 2) * sden A u * sden B u *
      ((1 - u ^ 2) / (1 + u ^ 2) * A.val u p + 2 * u / (1 + u ^ 2) * B.val u p - 1) := by
  have a := (sden_pos A hA hu0 hu1).ne'
  have b := (sden_pos B hB hu0 hu1).ne'
  have hN : (1 : ℝ) + u ^ 2 ≠ 0 := by positivity
  rw [xiPL, aff_addPL, aff_addPL, aff_mulPL, aff_mulPL]
  simp only [SL.val, BernZ.eval_mul, eval_sdenP, eval_Cp, eval_Sp, aff, evalPL, BernZ.eval_smul,
    eval_Np, eval_cons, eval_nil]
  field_simp
  push_cast
  ring

/-- **The corner conditions** of a rectangle entry, certified on the region. -/
def cornerOk (Q x0 x1 y0 y1 U0 U1 R : ℕ) (wx wy : Bool) (D : ℕ) (r : RectM) : Bool :=
  let co := cornersOk Q x0 x1 y0 y1 U0 U1 R wx wy
  match r.2.2.2 with
  | .std => true
  | .c3 xa ya _ q => Nat.blt 0 q && r.2.1.isNone && r.2.2.1.isNone &&
      co false ((capX D r.1.1).sub (sSL 1)).P && co true (((capX D r.1.1).sub (sSL 1)).sub (cSL 1)).P &&
      co true ((capY D r.1.2.1).sub (cSL 1)).P &&
      co true (xiPL ((capX D r.1.1).sub (sSL 1)) (capY D r.1.2.1)) &&
      ancOk Q x0 x1 y0 y1 U0 U1 R wx wy xa ya q
  | .xc xa ya _ q => Nat.blt 0 q && r.2.1.isNone && r.2.2.1.isNone &&
      co true ((capX D r.1.1).sub (sSL 1)).P && co true ((capY D r.1.2.1).sub (cSL 1)).P &&
      ancOk Q x0 x1 y0 y1 U0 U1 R wx wy xa ya q

lemma ancOk_sound {Q x0 x1 y0 y1 U0 U1 R : ℕ} (hQ : 0 < Q) (hR : 0 < R) {wx wy : Bool} {xa ya q : ℕ}
    (hq : 0 < q) (h : ancOk Q x0 x1 y0 y1 U0 U1 R wx wy xa ya q = true) {u : ℝ} (hu0 : 0 < u)
    (hu1 : u < 1) (hb0 : (U0 : ℝ) / R ≤ u) (hb1 : u ≤ (U1 : ℝ) / R) :
    ∀ p ∈ poly ((sideL Q x0 x1 y0 y1 wx wy).map (evalPL · u)),
      0 ≤ ((xa : ℝ) / q - p.1) * ((ya : ℝ) / q - p.2) := by
  intro p hp
  have hqr : (0 : ℝ) < q := by exact_mod_cast hq
  have ex : aff (evalPL (ancPL xa q true) u) p = q * ((xa : ℝ) / q - p.1) := by
    simp [ancPL, aff, evalPL]; field_simp; ring
  have ey : aff (evalPL (ancPL ya q false) u) p = q * ((ya : ℝ) / q - p.2) := by
    simp [ancPL, aff, evalPL]; field_simp; ring
  simp only [ancOk, Bool.or_eq_true, Bool.and_eq_true] at h
  rcases h with ⟨h1, h2⟩ | ⟨h1, h2⟩
  · have k1 := corners_sound hQ hR h1 hu0 hu1 hb0 hb1 p hp
    have k2 := corners_sound hQ hR h2 hu0 hu1 hb0 hb1 p hp
    simp only [if_false, Bool.false_eq_true, ex, ey] at k1 k2
    exact mul_nonneg (nonneg_of_mul_nonneg_right (by linarith) hqr)
      (nonneg_of_mul_nonneg_right (by linarith) hqr)
  · have k1 := corners_sound hQ hR h1 hu0 hu1 hb0 hb1 p hp
    have k2 := corners_sound hQ hR h2 hu0 hu1 hb0 hb1 p hp
    simp only [if_true, ex, ey] at k1 k2
    have a1 : (xa : ℝ) / q - p.1 ≤ 0 := by nlinarith
    have a2 : (ya : ℝ) / q - p.2 ≤ 0 := by nlinarith
    exact mul_nonneg_of_nonpos_of_nonpos a1 a2

lemma cornerOk_sound {Q x0 x1 y0 y1 U0 U1 R D : ℕ} (hQ : 0 < Q) (hR : 0 < R) (hD : 0 < D)
    {wx wy : Bool} {r : RectM} (h : cornerOk Q x0 x1 y0 y1 U0 U1 R wx wy D r = true) {u : ℝ}
    (hu0 : 0 < u) (hu1 : u < 1) (hb0 : (U0 : ℝ) / R ≤ u) (hb1 : u ≤ (U1 : ℝ) / R) :
    ckOk r.2.2.2 = true ∧ ∀ p ∈ poly ((sideL Q x0 x1 y0 y1 wx wy).map (evalPL · u)),
      KindOk (2 * Real.arctan u) D r p := by
  have dX : (capX D r.1.1).d ≠ 0 := by simp [capX]; omega
  have dY : (capY D r.1.2.1).d ≠ 0 := by simp [capY]; omega
  have ds : (sSL 1).d ≠ 0 := by simp [sSL]
  have dc : (cSL 1).d ≠ 0 := by simp [cSL]
  have hN : (0 : ℝ) < 1 + u ^ 2 := by positivity
  have h1u : (0 : ℝ) < 1 - u ^ 2 := by nlinarith
  rcases r with ⟨Rr, m1, m2, k⟩
  cases k with
  | std => exact ⟨rfl, fun _ _ => trivial⟩
  | c3 xa ya ym q =>
    simp only [cornerOk, Bool.and_eq_true, Nat.blt_eq, Option.isNone_iff_eq_none] at h
    obtain ⟨⟨⟨⟨⟨⟨⟨hq, rfl⟩, rfl⟩, k1⟩, k2⟩, k3⟩, k4⟩, k5⟩ := h
    refine ⟨by simp [ckOk, hq], fun p hp => ?_⟩
    have v1 := sl_sign hQ hR (sub_d dX ds) k1 hu0 hu1 hb0 hb1 p hp
    have v2 := sl_sign hQ hR (sub_d (sub_d dX ds) dc) k2 hu0 hu1 hb0 hb1 p hp
    have v3 := sl_sign hQ hR (sub_d dY dc) k3 hu0 hu1 hb0 hb1 p hp
    have v4 := corners_sound hQ hR k4 hu0 hu1 hb0 hb1 p hp
    have v5 := ancOk_sound hQ hR hq k5 hu0 hu1 hb0 hb1 p hp
    simp only [if_true, if_false, Bool.false_eq_true] at v1 v2 v3 v4
    try dsimp only at v1 v2 v3 v4 ⊢
    rw [aff_xiPL _ _ (sub_d dX ds) dY hu0 hu1] at v4
    have hpos : 0 < (1 + u ^ 2) * sden ((capX D Rr.1).sub (sSL 1)) u * sden (capY D Rr.2.1) u :=
      mul_pos (mul_pos hN (sden_pos _ (sub_d dX ds) hu0 hu1)) (sden_pos _ dY hu0 hu1)
    have v4' := nonpos_of_mul_nonpos_right v4 hpos
    rw [val_sub _ _ dX ds hu0 hu1, val_capX hD hu0 hu1, val_sSL one_ne_zero] at v1 v4'
    rw [val_sub _ _ (sub_d dX ds) dc hu0 hu1, val_sub _ _ dX ds hu0 hu1, val_capX hD hu0 hu1,
      val_sSL one_ne_zero, val_cSL one_ne_zero] at v2
    rw [val_sub _ _ dY dc hu0 hu1, val_capY hD hu0 hu1, val_cSL one_ne_zero] at v3
    rw [val_capY hD hu0 hu1] at v4'
    simp only [KindOk, (trig u).1, (trig u).2] at v1 v2 v3 v4' ⊢
    push_cast at v1 v2 v3 v4'
    refine ⟨trivial, trivial, by linarith, by linarith, by linarith, by linarith, v5⟩
  | xc xa ya ym q =>
    simp only [cornerOk, Bool.and_eq_true, Nat.blt_eq, Option.isNone_iff_eq_none] at h
    obtain ⟨⟨⟨⟨⟨hq, rfl⟩, rfl⟩, k1⟩, k2⟩, k5⟩ := h
    refine ⟨by simp [ckOk, hq], fun p hp => ?_⟩
    have v1 := sl_sign hQ hR (sub_d dX ds) k1 hu0 hu1 hb0 hb1 p hp
    have v3 := sl_sign hQ hR (sub_d dY dc) k2 hu0 hu1 hb0 hb1 p hp
    have v5 := ancOk_sound hQ hR hq k5 hu0 hu1 hb0 hb1 p hp
    simp only [if_true] at v1 v3
    try dsimp only at v1 v3 ⊢
    rw [val_sub _ _ dX ds hu0 hu1, val_capX hD hu0 hu1, val_sSL one_ne_zero] at v1
    rw [val_sub _ _ dY dc hu0 hu1, val_capY hD hu0 hu1, val_cSL one_ne_zero] at v3
    simp only [KindOk, (trig u).1, (trig u).2] at v1 v3 ⊢
    push_cast at v1 v3
    refine ⟨trivial, trivial, by linarith, by linarith, v5⟩

/-- **The `EXACT` leaf test.** -/
def exOk (D S R W x0 x1 y0 y1 U0 U1 : ℕ) (segs : List SegE) (rects : List RectE) (lf : ExLeaf) :
    Bool :=
  let side := sideE (D * S) x0 x1 y0 y1 lf.wx lf.wy lf.ex lf.ey
  let pin := pinOk (D * S) x0 x1 y0 y1 U0 U1 R lf.wx lf.wy lf.Ls
  Nat.blt U1 R && Nat.ble U0 U1 && decide (lf.chs ++ lf.cvs).Nodup && decide (lf.crs.map Prod.fst).Nodup &&
    lf.chs.all (fun e => segs.contains e && e.2.1 == e.2.2.2.1 && Nat.blt e.1 e.2.2.1 &&
      (hFormsSLs D e).all pin) &&
    lf.cvs.all (fun e => segs.contains e && e.1 == e.2.2.1 && Nat.blt e.2.1 e.2.2.2.1 &&
      (vFormsSLs D e).all pin) &&
    lf.crs.all (fun r => rects.contains r.1 &&
      Nat.ble (2 * x1 * widD R U0 + D * S * widN R U0 U1) (2 * r.1.2.2.1 * S * widD R U0) &&
      Nat.ble (2 * y1 * widD R U0 + D * S * widN R U0 U1) (2 * r.1.2.2.2.1 * S * widD R U0) &&
      (lebSLs D r).all pin && tanOk (D * S) x0 x1 y0 y1 U0 U1 R lf.wx lf.wy D r &&
      cornerOk (D * S) x0 x1 y0 y1 U0 U1 R lf.wx lf.wy D r) &&
    lf.hbx.length == lf.chs.length && lf.vbx.length == lf.cvs.length &&
    (lf.chs.zip lf.hbx).all (fun q => boxDomOk (D * S) x0 x1 y0 y1 U0 U1 R lf.wx lf.wy
      (hUps D q.1) (hLos D q.1) q.2) &&
    (lf.cvs.zip lf.vbx).all (fun q => boxDomOk (D * S) x0 x1 y0 y1 U0 U1 R lf.wx lf.wy
      (vUps D q.1) (vLos D q.1) q.2) &&
    credOkL D S R W x0 x1 y0 y1 U0 U1 rects lf &&
    allPairsOk D (W - credAmt lf) R U0 U1 side lf.chs lf.cvs lf.crs lf.hbx lf.vbx (side ++ lf.Ls) lf.certs

/-- Everything in `exOk` except the pair certificates. -/
def exHead (D S R W x0 x1 y0 y1 U0 U1 : ℕ) (segs : List SegE) (rects : List RectE) (lf : ExLeaf) :
    Bool :=
  let side := sideE (D * S) x0 x1 y0 y1 lf.wx lf.wy lf.ex lf.ey
  let pin := pinOk (D * S) x0 x1 y0 y1 U0 U1 R lf.wx lf.wy lf.Ls
  Nat.blt U1 R && Nat.ble U0 U1 && decide (lf.chs ++ lf.cvs).Nodup && decide (lf.crs.map Prod.fst).Nodup &&
    lf.chs.all (fun e => segs.contains e && e.2.1 == e.2.2.2.1 && Nat.blt e.1 e.2.2.1 &&
      (hFormsSLs D e).all pin) &&
    lf.cvs.all (fun e => segs.contains e && e.1 == e.2.2.1 && Nat.blt e.2.1 e.2.2.2.1 &&
      (vFormsSLs D e).all pin) &&
    lf.crs.all (fun r => rects.contains r.1 &&
      Nat.ble (2 * x1 * widD R U0 + D * S * widN R U0 U1) (2 * r.1.2.2.1 * S * widD R U0) &&
      Nat.ble (2 * y1 * widD R U0 + D * S * widN R U0 U1) (2 * r.1.2.2.2.1 * S * widD R U0) &&
      (lebSLs D r).all pin && tanOk (D * S) x0 x1 y0 y1 U0 U1 R lf.wx lf.wy D r &&
      cornerOk (D * S) x0 x1 y0 y1 U0 U1 R lf.wx lf.wy D r) &&
    lf.hbx.length == lf.chs.length && lf.vbx.length == lf.cvs.length &&
    (lf.chs.zip lf.hbx).all (fun q => boxDomOk (D * S) x0 x1 y0 y1 U0 U1 R lf.wx lf.wy
      (hUps D q.1) (hLos D q.1) q.2) &&
    (lf.cvs.zip lf.vbx).all (fun q => boxDomOk (D * S) x0 x1 y0 y1 U0 U1 R lf.wx lf.wy
      (vUps D q.1) (vLos D q.1) q.2) &&
    credOkL D S R W x0 x1 y0 y1 U0 U1 rects lf

lemma exOk_of {D S R W x0 x1 y0 y1 U0 U1 : ℕ} {segs : List SegE} {rects : List RectE} {lf : ExLeaf}
    (h1 : exHead D S R W x0 x1 y0 y1 U0 U1 segs rects lf = true)
    (h2 : allPairsOk D (W - credAmt lf) R U0 U1 (sideE (D * S) x0 x1 y0 y1 lf.wx lf.wy lf.ex lf.ey)
      lf.chs lf.cvs lf.crs lf.hbx lf.vbx (sideE (D * S) x0 x1 y0 y1 lf.wx lf.wy lf.ex lf.ey ++ lf.Ls)
      lf.certs = true) :
    exOk D S R W x0 x1 y0 y1 U0 U1 segs rects lf = true := by
  simp only [exHead] at h1
  simp only [exOk, h1, h2, Bool.and_self]

lemma pinned_of_formsSL {Q x0 x1 y0 y1 U0 U1 R : ℕ} (hQ : 0 < Q) (hR : 0 < R) {wx wy : Bool}
    {Ls : List PL} {u : ℝ} (hu0 : 0 < u) (hu1 : u < 1) (hb0 : (U0 : ℝ) / R ≤ u)
    (hb1 : u ≤ (U1 : ℝ) / R) {Ls' : List SL}
    (hall : Ls'.all (pinOk Q x0 x1 y0 y1 U0 U1 R wx wy Ls) = true) {Fs : List (ℝ × ℝ × ℝ)}
    (hm : ∀ F ∈ Fs, ∃ L ∈ Ls', L.d ≠ 0 ∧ ∀ c, aff F c = L.val u c) :
    ∀ F ∈ Fs, Pinned (poly ((sideL Q x0 x1 y0 y1 wx wy).map (evalPL · u))) (Ls.map (evalPL · u)) F := by
  intro F hF
  obtain ⟨L, hL, hd, he⟩ := hm F hF
  exact pin_sound hQ hR ((List.all_eq_true.mp hall) L hL) hd hu0 hu1 hb0 hb1 he

/-- **Soundness of the `EXACT` leaf** (Lemma E). -/
theorem CovMPo.of_exact {D S Mq R W x0 x1 y0 y1 U0 U1 : ℕ} {pts : List (ℕ × ℕ × ℕ)}
    {segs : List SegE} {rects : List RectE} (hD : 0 < D) (hS : 0 < S) (hR : 0 < R) {lf : ExLeaf}
    (h : exOk D S R W x0 x1 y0 y1 U0 U1 segs rects lf = true) :
    CovMPo D S Mq R W pts segs rects x0 x1 y0 y1 U0 U1 := by
  simp only [exOk, Bool.and_eq_true, Nat.blt_eq, Nat.ble_eq, decide_eq_true_eq, List.all_eq_true,
    beq_iff_eq, List.contains_iff_mem] at h
  obtain ⟨⟨⟨⟨⟨⟨⟨⟨⟨⟨⟨⟨hU1, hU01⟩, hnd⟩, hcr⟩, hch⟩, hcv⟩, hcrs⟩, lhb⟩, lvb⟩, hhb⟩, hvb⟩, hcred⟩, hpairs⟩ := h
  intro c u hx0 hx1 hy0 hy1 hu0 hu1 hbox
  have hQ : 0 < D * S := Nat.mul_pos hD hS
  have hRr : (0 : ℝ) < R := by exact_mod_cast hR
  have hpos : 0 < u := lt_of_le_of_lt (by positivity) hu0
  have hlt : u < 1 := by
    have : (U1 : ℝ) < R := by exact_mod_cast hU1
    have := (div_lt_one hRr).mpr this
    linarith
  have hb0 : (U0 : ℝ) / R ≤ u := hu0.le
  have hmd : ∀ r ∈ lf.crs, modeP r.2.1 = true ∧ modeP r.2.2.1 = true ∧ ckOk r.2.2.2 = true :=
    fun r hr => by
    have htan := (hcrs r hr).1.2
    simp only [tanOk, Bool.and_eq_true] at htan
    exact ⟨(tanAx_sound hQ hR (L := capX D r.1.1) (by simp [capX]; omega) htan.1 hpos hlt hb0 hu1).1,
      (tanAx_sound hQ hR (L := capY D r.1.2.1) (by simp [capY]; omega) htan.2 hpos hlt hb0 hu1).1,
      (cornerOk_sound hQ hR hD (hcrs r hr).2 hpos hlt hb0 hu1).1⟩
  set θ := 2 * Real.arctan u with hθ
  have hs : 0 < Real.sin θ := by rw [hθ, (trig u).1]; positivity
  have hc : 0 < Real.cos θ := by
    rw [hθ, (trig u).2]; apply div_pos _ (by positivity); nlinarith
  -- 2. the centre is in the region
  have hadm := (sq_subset_box_iff _ c θ).mp hbox
  have hwθ : wid θ = (1 - u ^ 2 + 2 * u) / (1 + u ^ 2) := by
    rw [hθ, wid_two_arctan hpos.le hlt.le, widU]
  have hcreg : c ∈ poly ((sideL (D * S) x0 x1 y0 y1 lf.wx lf.wy).map (evalPL · u)) := by
    have hQr : (0 : ℝ) < ((D * S : ℕ) : ℝ) := by exact_mod_cast hQ
    intro C hC
    simp only [List.mem_map, sideL, List.mem_cons, List.not_mem_nil, or_false] at hC
    obtain ⟨P, hP, rfl⟩ := hC
    obtain ⟨a1, a2, a3, a4⟩ := hadm
    rw [hwθ] at a1 a3
    have hN : (0 : ℝ) < 1 + u ^ 2 := by positivity
    rcases hP with rfl | rfl | rfl | rfl
    · split_ifs
      · simp only [evalPL, eval_smul, eval_Np, BernZ.eval_add, eval_Cp, eval_Sp, eval_cons, eval_nil]
        push_cast
        rw [div_div, div_le_iff₀ (by positivity)] at a1
        nlinarith
      · simp only [evalPL, eval_cons, eval_nil]; push_cast
        rw [div_le_iff₀ (by push_cast at hQr; exact hQr)] at hx0
        push_cast at hx0; nlinarith
    · simp only [evalPL, eval_cons, eval_nil]; push_cast
      rw [le_div_iff₀ (by push_cast at hQr; exact hQr)] at hx1
      push_cast at hx1; nlinarith
    · split_ifs
      · simp only [evalPL, eval_smul, eval_Np, BernZ.eval_add, eval_Cp, eval_Sp, eval_cons, eval_nil]
        push_cast
        rw [div_div, div_le_iff₀ (by positivity)] at a3
        nlinarith
      · simp only [evalPL, eval_cons, eval_nil]; push_cast
        rw [div_le_iff₀ (by push_cast at hQr; exact hQr)] at hy0
        push_cast at hy0; nlinarith
    · simp only [evalPL, eval_cons, eval_nil]; push_cast
      rw [le_div_iff₀ (by push_cast at hQr; exact hQr)] at hy1
      push_cast at hy1; nlinarith
  -- 1. the mass is at least `fE` at the centre
  have hwid : wid θ / 2 ≤ (widN R U0 U1 : ℝ) / widD R U0 / 2 := by
    have := wid_le_widHat hR (Nat.le_of_lt hU1) hb0 hu1; linarith
  have hwd : 0 < widD R U0 := by unfold widD; have : 0 < R * R := Nat.mul_pos hR hR; omega
  have hmass := fE_le_mass hD hs hc c hnd
    (fun e he => ⟨(hch e he).1.1.1, (hch e he).1.1.2, (hch e he).1.2⟩)
    (fun e he => ⟨(hcv e he).1.1.1, (hcv e he).1.1.2, (hcv e he).1.2⟩) hcr
    (fun r hr => by
      obtain ⟨⟨⟨⟨⟨hm, h1⟩, h2⟩, _⟩, htan⟩, hcor⟩ := hcrs r hr
      simp only [tanOk, Bool.and_eq_true] at htan
      have tx := (tanAx_sound hQ hR (L := capX D r.1.1) (by simp [capX]; omega) htan.1 hpos hlt hb0 hu1).2 c hcreg
      have ty := (tanAx_sound hQ hR (L := capY D r.1.2.1) (by simp [capY]; omega) htan.2 hpos hlt hb0 hu1).2 c hcreg
      rw [val_capX hD hpos hlt] at tx
      rw [val_capY hD hpos hlt] at ty
      refine ⟨hm, fun p hp => ?_, ?_, ?_, (cornerOk_sound hQ hR hD hcor hpos hlt hb0 hu1).2 c hcreg⟩
      · obtain ⟨a1, a2⟩ := abs_sub_le_wid hp
        rw [abs_le] at a1 a2
        have k1 := add_half_le hD hS hwd h1
        have k2 := add_half_le hD hS hwd h2
        push_cast at hx1 hy1
        constructor <;> linarith
      · convert tx using 1; simp only [SqArea.xmin]; ring
      · convert ty using 1; simp only [SqArea.ymin]; ring)
  -- 3. every form is pinned
  have hfix : Fixed (poly ((sideL (D * S) x0 x1 y0 y1 lf.wx lf.wy).map (evalPL · u)))
      (Real.sin θ) (lf.Ls.map (evalPL · u))
      (lf.chs.map (hsegT θ D) ++ lf.cvs.map (vsegT θ D)) (lf.crs.map (rectT θ D)) := by
    have hDr : (0 : ℝ) < D := by exact_mod_cast hD
    have d2D : 2 * D ≠ 0 := by omega
    refine ⟨fun t ht => ?_, fun l hl => ?_⟩
    · rcases List.mem_append.mp ht with ht | ht
      · obtain ⟨e, he, rfl⟩ := List.mem_map.mp ht
        obtain ⟨⟨⟨_, _⟩, hx⟩, hpin⟩ := hch e he
        have hAB : (e.1 : ℝ) / D < e.2.2.1 / D := div_lt_div_of_pos_right (by exact_mod_cast hx) hDr
        refine ⟨div_nonneg (Nat.cast_nonneg _) (by linarith), by simp only [hsegT]; linarith,
          pinned_of_formsSL hQ hR hpos hlt hb0 hu1 (List.all_eq_true.mpr hpin) ?_⟩
        refine formsSL_match hpos hlt (by simp [SL.cst]; omega) (by simp [SL.cst]; omega)
          (by simp [hTA]; omega) (by simp [hTB]; omega) (by simp [hTC]; omega) (by simp [hTD]; omega)
          (fun c => by rw [val_cst]; push_cast; rfl) (fun c => by rw [val_cst]; push_cast; rfl)
          (fun c => (val_hTA hD hpos hlt _ c).symm) (fun c => (val_hTB hD hpos hlt _ c).symm)
          (fun c => (val_hTC hD hpos hlt _ c).symm) (fun c => (val_hTD hD hpos hlt _ c).symm)
      · obtain ⟨e, he, rfl⟩ := List.mem_map.mp ht
        obtain ⟨⟨⟨_, _⟩, hy⟩, hpin⟩ := hcv e he
        have hAB : (e.2.1 : ℝ) / D < e.2.2.2.1 / D :=
          div_lt_div_of_pos_right (by exact_mod_cast hy) hDr
        refine ⟨div_nonneg (Nat.cast_nonneg _) (by linarith), by simp only [vsegT]; linarith,
          pinned_of_formsSL hQ hR hpos hlt hb0 hu1 (List.all_eq_true.mpr hpin) ?_⟩
        refine formsSL_match hpos hlt (by simp [SL.cst]; omega) (by simp [SL.cst]; omega)
          (by simp [vLXs]; omega) (by simp [vLYs]; omega) (by simp [vUXs]; omega) (by simp [vUYs]; omega)
          (fun c => by rw [val_cst]; push_cast; rfl) (fun c => by rw [val_cst]; push_cast; rfl)
          (fun c => (val_vLX hD hpos hlt _ c).symm) (fun c => (val_vLY hD hpos hlt _ c).symm)
          (fun c => (val_vUX hD hpos hlt _ c).symm) (fun c => (val_vUY hD hpos hlt _ c).symm)
    · obtain ⟨r, hr, rfl⟩ := List.mem_map.mp hl
      obtain ⟨⟨⟨_, hpin⟩, htan⟩, _⟩ := hcrs r hr
      have hp := hpin
      have hm := hmd r hr
      have dX : (capXm D r).d ≠ 0 := capXm_d hD r hm.1
      have dY : (capYm D r).d ≠ 0 := capYm_d hD r hm.2.1
      have ds : (sSL 1).d ≠ 0 := by simp [sSL]
      have ex : ∀ c, aff (rectT θ D r).2.1 c = (capXm D r).val u c := fun c =>
        (val_capXm hD hpos hlt r hm.1 c).symm
      have ey : ∀ c, aff (rectT θ D r).2.2.1 c = (capYm D r).val u c := fun c =>
        (val_capYm hD hpos hlt r hm.2.1 c).symm
      have hsθ : Real.sin θ = 2 * u / (1 + u ^ 2) := by rw [hθ, (trig u).1]
      refine ⟨Nat.cast_nonneg _, pin_sound hQ hR (hp (capXm D r) (by simp [lebSLs])) dX hpos hlt hb0 hu1 ex,
        pin_sound hQ hR (hp ((capXm D r).sub (sSL 1)) (by simp [lebSLs])) (Nat.mul_ne_zero dX ds) hpos hlt hb0 hu1 ?_,
        pin_sound hQ hR (hp (capYm D r) (by simp [lebSLs])) dY hpos hlt hb0 hu1 ey,
        pin_sound hQ hR (hp ((capYm D r).sub (sSL 1)) (by simp [lebSLs])) (Nat.mul_ne_zero dY ds) hpos hlt hb0 hu1 ?_⟩
      · intro c; rw [aff_subF, aff_constF, val_sub _ _ dX ds hpos hlt, val_sSL one_ne_zero, ex, hsθ]
        simp
      · intro c; rw [aff_subF, aff_constF, val_sub _ _ dY ds hpos hlt, val_sSL one_ne_zero, ey, hsθ]
        simp
  -- 4. the vertex
  have hsubE := poly_sideE_sub (Q := D * S) (x0 := x0) (x1 := x1) (y0 := y0) (y1 := y1) (wx := lf.wx)
    (wy := lf.wy) (ex := lf.ex) (ey := lf.ey) u
  have hcregE : c ∈ poly ((sideE (D * S) x0 x1 y0 y1 lf.wx lf.wy lf.ex lf.ey).map (evalPL · u)) := by
    intro C hC
    simp only [sideE, List.map_append, List.mem_append] at hC
    rcases hC with hC | hC
    · exact hcreg C hC
    obtain ⟨a1, a2, a3, a4⟩ := hadm
    rw [hwθ] at a1 a3
    have hN : (0 : ℝ) < 1 + u ^ 2 := by positivity
    have wX : 0 ≤ aff (evalPL wallX u) c := by
      simp only [wallX, aff, evalPL, eval_smul, eval_Np, BernZ.eval_add, eval_Cp, eval_Sp, eval_cons,
        eval_nil]
      push_cast
      rw [div_div, div_le_iff₀ (by positivity)] at a1; nlinarith
    have wY : 0 ≤ aff (evalPL wallY u) c := by
      simp only [wallY, aff, evalPL, eval_smul, eval_Np, BernZ.eval_add, eval_Cp, eval_Sp, eval_cons,
        eval_nil]
      push_cast
      rw [div_div, div_le_iff₀ (by positivity)] at a3; nlinarith
    cases hex : lf.ex <;> cases hey : lf.ey <;>
      simp only [hex, hey, if_true, if_false, Bool.false_eq_true, List.map_cons, List.map_nil,
        List.mem_cons, List.not_mem_nil, or_false] at hC
    all_goals first
      | exact hC.elim
      | (rw [hC]; first | exact wX | exact wY)
      | (rcases hC with h | h <;> first | exact h.elim | (rw [h]; first | exact wX | exact wY))
  obtain ⟨v, hv, ⟨C1, hC1, C2, hC2, hdet, ht1, ht2⟩, hle⟩ :=
    exists_vertex_le_fE hs hc ((region_bounded hQ lf.wx lf.wy u).subset hsubE) (hfix.mono hsubE) hcregE
  set side := sideE (D * S) x0 x1 y0 y1 lf.wx lf.wy lf.ex lf.ey
  have hmemL : ∀ C ∈ side.map (evalPL · u) ++ lf.Ls.map (evalPL · u),
      ∃ P ∈ side ++ lf.Ls, C = evalPL P u := by
    intro C hC
    rw [← List.map_append] at hC
    obtain ⟨P, hP, rfl⟩ := List.mem_map.mp hC
    exact ⟨P, hP, rfl⟩
  obtain ⟨A, hA, rfl⟩ := hmemL C1 hC1
  obtain ⟨B, hB, rfl⟩ := hmemL C2 hC2
  obtain ⟨i, hi, hiA⟩ := List.mem_iff_getElem.mp hA
  obtain ⟨j, hj, hjB⟩ := List.mem_iff_getElem.mp hB
  have hdetAB : eval (detP A B) u ≠ 0 := by rw [eval_detP]; exact hdet
  have hbd : ∀ p ∈ poly ((sideE (D * S) x0 x1 y0 y1 lf.wx lf.wy lf.ex lf.ey).map (evalPL · u)),
      BoxDom D u p lf.chs lf.cvs lf.hbx lf.vbx := by
    intro p hp
    replace hp := hsubE hp
    refine ⟨fun q hq => ?_, fun q hq => ?_⟩
    · exact boxDom_sound hQ hR (hhb q hq) (hd_hUps hD q.1) (hd_hLos hD q.1) hpos hlt hb0 hu1 p hp
    · exact boxDom_sound hQ hR (hvb q hq) (hd_vUps hD q.1) (hd_vLos hD q.1) hpos hlt hb0 hu1 p hp
  have hcl : Claims D lf.chs lf.cvs :=
    ⟨hD, fun e he => (hch e he).1.2, fun e he => (hcv e he).1.2⟩
  have hW : ((W - credAmt lf : ℕ) : ℝ) ≤ fEu D lf.chs lf.cvs lf.crs u v := by
    rcases lt_trichotomy i j with hij | hij | hij
    · obtain ⟨cert, hc'⟩ := allPairs_sound _ _ hpairs i j hij hj
      rw [hiA, hjB] at hc'
      exact pair_sound hcl hmd hR hc' hu0 hu1 hpos hlt hdetAB ht1 ht2 hv hbd
    · subst hij
      exfalso; apply hdetAB
      have : A = B := hiA.symm.trans hjB
      rw [this, eval_detP]; ring
    · obtain ⟨cert, hc'⟩ := allPairs_sound _ _ hpairs j i hij hi
      rw [hiA, hjB] at hc'
      refine pair_sound hcl hmd hR hc' hu0 hu1 hpos hlt ?_ ht2 ht1 hv hbd
      rw [detP_swap]; exact neg_ne_zero.mpr hdetAB
  -- 5. assemble: with a credit, the rectangles are not in `fE` and the credit bounds their mass
  have h1 : fEu D lf.chs lf.cvs lf.crs u v ≤ fEu D lf.chs lf.cvs lf.crs u c := hle
  have h2 := ptMass_nonneg D pts (sq c θ 1)
  have hcr' : fEu D lf.chs lf.cvs lf.crs u c + credAmt lf ≤
      segMass D segs (sq c θ 1) + rectMass D rects (sq c θ 1) ∧ credAmt lf ≤ W := by
    unfold credOkL at hcred
    unfold credAmt
    split at hcred
    · simp only [Nat.cast_zero, add_zero, zero_le, and_true]
      exact hmass
    · rename_i cr _
      simp only [Bool.and_eq_true, List.isEmpty_iff, Nat.ble_eq] at hcred ⊢
      obtain ⟨⟨hnil, hamtW⟩, hok⟩ := hcred
      refine ⟨?_, hamtW⟩
      have hm0 := fE_le_mass (rects := []) hD hs hc c hnd
        (fun e he => ⟨(hch e he).1.1.1, (hch e he).1.1.2, (hch e he).1.2⟩)
        (fun e he => ⟨(hcv e he).1.1.1, (hcv e he).1.1.2, (hcv e he).1.2⟩) hcr
        (fun r hr => by rw [hnil] at hr; exact absurd hr List.not_mem_nil)
      have hr0 : rectMass D [] (sq c θ 1) = 0 := by simp [rectMass]
      have hQr : ((D * S : ℕ) : ℝ) = (D : ℝ) * S := by push_cast; ring
      have hc' := LebCredit.cred_sound (Q := D * S) hD hQ hR hok hpos hlt hb0 hu1
        (by rw [hQr]; exact hx0) (by rw [hQr]; exact hx1) (by rw [hQr]; exact hy0) (by rw [hQr]; exact hy1)
      simp only [fEu, hnil, List.map_nil] at hm0 ⊢
      rw [hr0, add_zero] at hm0
      linarith
  obtain ⟨hcr1, hcr2⟩ := hcr'
  rw [Nat.cast_sub hcr2] at hW
  simp only [fEu] at hW h1 hcr1
  linarith

end LemmaELeaf

end SquarePacking
