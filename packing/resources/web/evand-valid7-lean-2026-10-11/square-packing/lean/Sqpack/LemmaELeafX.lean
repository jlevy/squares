import Sqpack.LemmaEKM
import Sqpack.LemmaELeaf

/-!
# The `EXACT` leaf with the vertex test without combinations

`LemmaELeaf` with `LemmaEK.vertOkM` (the rows' minima, `LemmaEKM`) in place of `LemmaEK.vertOkK` in
the sub-bin test; the rest of the leaf test (`exHead`) and its soundness are the same.  Copied from
`LemmaELeaf` with the names suffixed `X`.
-/

namespace SquarePacking

namespace LemmaELeaf

open BernZ RatU ChordE LemmaE LemmaEPoly LemmaEVert PolyMin ZMTreeM

def subOkX (D W R : ℕ) (side : List PL) (chs cvs : List SegE) (crs : List RectM)
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
      LemmaEK.vertOkM (LemmaEK.mkCtx Δ X Y b0 sb.b1 R LemmaEK.kK) D W sb.σ b0 sb.b1 R chs cvs crs hbx vbx c

def binsOkX (D W R : ℕ) (side : List PL) (chs cvs : List SegE) (crs : List RectM)
    (hbx vbx : List (List ℕ × List ℕ)) (P Q : PL) :
    ℕ → ℕ → List SubBin → Bool
  | b0, U1, [] => b0 == U1
  | b0, U1, sb :: sbs =>
    subOkX D W R side chs cvs crs hbx vbx P Q b0 sb &&
      binsOkX D W R side chs cvs crs hbx vbx P Q sb.b1 U1 sbs

def pairOkX (D W R U0 U1 : ℕ) (side : List PL) (chs cvs : List SegE) (crs : List RectM)
    (hbx vbx : List (List ℕ × List ℕ)) (P Q : PL) :
    PairCert → Bool
  | .par => (detP P Q).all (· == 0)
  | .bins sbs => binsOkX D W R side chs cvs crs hbx vbx P Q U0 U1 sbs

def rowOkX (D W R U0 U1 : ℕ) (side : List PL) (chs cvs : List SegE) (crs : List RectM)
    (hbx vbx : List (List ℕ × List ℕ)) (P : PL) (Ps : List PL) (cs : List PairCert) : Bool :=
  cs.length == Ps.length && (Ps.zip cs).all (fun q => pairOkX D W R U0 U1 side chs cvs crs hbx vbx P q.1 q.2)

def allPairsOkX (D W R U0 U1 : ℕ) (side : List PL) (chs cvs : List SegE) (crs : List RectM)
    (hbx vbx : List (List ℕ × List ℕ)) :
    List PL → List (List PairCert) → Bool
  | [], _ => true
  | _ :: _, [] => false
  | P :: Ps, cs :: css =>
    rowOkX D W R U0 U1 side chs cvs crs hbx vbx P Ps cs &&
      allPairsOkX D W R U0 U1 side chs cvs crs hbx vbx Ps css

lemma rowOkX_of {D W R U0 U1 : ℕ} {side : List PL} {chs cvs : List SegE} {crs : List RectM}
    {hbx vbx : List (List ℕ × List ℕ)} {P : PL} {Ps : List PL} {cs : List PairCert}
    (hl : cs.length = Ps.length)
    (h : ((Ps.zip cs).drop 0).all (fun q => pairOkX D W R U0 U1 side chs cvs crs hbx vbx P q.1 q.2) = true) :
    rowOkX D W R U0 U1 side chs cvs crs hbx vbx P Ps cs = true := by
  simpa [rowOkX, hl] using h

lemma allPairsOkX_drop_step {D W R U0 U1 : ℕ} {side : List PL} {chs cvs : List SegE} {crs : List RectM}
    {hbx vbx : List (List ℕ × List ℕ)} (L : List PL) (C : List (List PairCert)) (i : ℕ) (d : PL)
    (hi : i < L.length) (hc : i < C.length)
    (h1 : rowOkX D W R U0 U1 side chs cvs crs hbx vbx (L.getD i d) (L.drop (i + 1)) (C.getD i []) = true)
    (h2 : allPairsOkX D W R U0 U1 side chs cvs crs hbx vbx (L.drop (i + 1)) (C.drop (i + 1)) = true) :
    allPairsOkX D W R U0 U1 side chs cvs crs hbx vbx (L.drop i) (C.drop i) = true := by
  rw [List.drop_eq_getElem_cons hi, List.drop_eq_getElem_cons hc, allPairsOkX, h2, Bool.and_true]
  rwa [List.getD_eq_getElem _ _ hi, List.getD_eq_getElem _ _ hc] at h1

lemma allPairsOkX_drop_end {D W R U0 U1 : ℕ} {side : List PL} {chs cvs : List SegE} {crs : List RectM}
    {hbx vbx : List (List ℕ × List ℕ)} (L : List PL) (C : List (List PairCert)) (m : ℕ) (h : L.length ≤ m) :
    allPairsOkX D W R U0 U1 side chs cvs crs hbx vbx (L.drop m) C = true := by
  simp [List.drop_eq_nil_of_le h, allPairsOkX]

lemma binsOkX_find {D W R : ℕ} {side : List PL} {chs cvs : List SegE} {crs : List RectM}
    {hbx vbx : List (List ℕ × List ℕ)} {P Q : PL}
    {u : ℝ} (hR : 0 < R) :
    ∀ (sbs : List SubBin) (b0 U1 : ℕ), binsOkX D W R side chs cvs crs hbx vbx P Q b0 U1 sbs = true →
      (b0 : ℝ) / R < u → u ≤ (U1 : ℝ) / R →
      ∃ b0' : ℕ, ∃ sb : SubBin, subOkX D W R side chs cvs crs hbx vbx P Q b0' sb = true ∧
        (b0' : ℝ) / R ≤ u ∧ u ≤ (sb.b1 : ℝ) / R
  | [], b0, U1, h, h0, h1 => by
    simp only [binsOkX, beq_iff_eq] at h
    subst h; linarith
  | sb :: sbs, b0, U1, h, h0, h1 => by
    simp only [binsOkX, Bool.and_eq_true] at h
    by_cases hu : u ≤ (sb.b1 : ℝ) / R
    · exact ⟨b0, sb, h.1, h0.le, hu⟩
    · exact binsOkX_find hR sbs sb.b1 U1 h.2 (not_le.mp hu) h1

theorem pair_soundX {D W R U0 U1 : ℕ} {side : List PL} {chs cvs : List SegE} {crs : List RectM}
    {hbx vbx : List (List ℕ × List ℕ)}
    (hcl : Claims D chs cvs) (hmd : ∀ r ∈ crs, modeP r.2.1 = true ∧ modeP r.2.2.1 = true ∧ ckOk r.2.2.2 = true) (hR : 0 < R)
    {P Q : PL} {cert : PairCert}
    (hok : pairOkX D W R U0 U1 side chs cvs crs hbx vbx P Q cert = true) {u : ℝ} (hu0 : (U0 : ℝ) / R < u)
    (hu1 : u ≤ (U1 : ℝ) / R) (hpos : 0 < u) (hlt : u < 1) {v : ℝ × ℝ}
    (hdet : eval (detP P Q) u ≠ 0) (h1 : aff (evalPL P u) v = 0) (h2 : aff (evalPL Q u) v = 0)
    (hv : v ∈ poly (side.map (evalPL · u)))
    (hbd : ∀ p ∈ poly (side.map (evalPL · u)), BoxDom D u p chs cvs hbx vbx) :
    (W : ℝ) ≤ fEu D chs cvs crs u v := by
  cases cert with
  | par =>
    exfalso; apply hdet
    simp only [pairOkX, List.all_eq_true, beq_iff_eq] at hok
    rw [eval_eq_sum]
    refine Finset.sum_eq_zero fun k hk => ?_
    have : (detP P Q).getD k 0 = 0 := by
      rw [List.getD_eq_getElem _ _ (Finset.mem_range.mp hk)]
      exact hok _ (List.getElem_mem _)
    rw [this]; simp
  | bins sbs =>
    simp only [pairOkX] at hok
    obtain ⟨b0, sb, hsub, hb0, hb1⟩ := binsOkX_find hR sbs U0 U1 hok hu0 hu1
    have hv' := cramer P Q u v hdet h1 h2
    simp only [subOkX, Bool.and_eq_true, Nat.blt_eq] at hsub
    obtain ⟨⟨_, hsg⟩, hk⟩ := hsub
    have hσ := sign_of_signOk hsg hR hpos hb0 hb1
    have hδ : eval (detP P Q) u ≠ 0 := by split_ifs at hσ <;> [exact hσ.ne'; exact hσ.ne]
    have ctx : VCtx (LemmaEK.ckU (LemmaEK.mkCtx (detP P Q) (xP P Q) (yP P Q) b0 sb.b1 R LemmaEK.kK) sb.σ
        (eval (detP P Q) u) u)
        (detP P Q) (xP P Q) (yP P Q) sb.σ b0 sb.b1 R u (eval (detP P Q) u) :=
      ⟨hR, hpos, hlt, hb0, hb1, rfl, hσ, LemmaEK.ckU_hck hR ⟨hpos, hlt, hδ⟩ hσ hb0 hb1⟩
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
        (LemmaEK.vertOkM_imp hR ⟨hpos, hlt, hδ⟩ rfl hσ hb0 hb1 hk.2)

lemma allPairs_soundX {D W R U0 U1 : ℕ} {side : List PL} {chs cvs : List SegE} {crs : List RectM}
    {hbx vbx : List (List ℕ × List ℕ)} :
    ∀ (L : List PL) (css : List (List PairCert)), allPairsOkX D W R U0 U1 side chs cvs crs hbx vbx L css = true →
      ∀ (i j : ℕ) (hi : i < j) (hj : j < L.length),
        ∃ c, pairOkX D W R U0 U1 side chs cvs crs hbx vbx (L[i]'(by omega)) (L[j]) c = true
  | [], _, _, i, j, _, hj => absurd hj (by simp)
  | _ :: _, [], h, _, _, _, _ => by simp [allPairsOkX] at h
  | P :: Ps, cs :: css, h, i, j, hij, hj => by
    simp only [allPairsOkX, rowOkX, Bool.and_eq_true, beq_iff_eq, List.all_eq_true] at h
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
      obtain ⟨c, hc⟩ := allPairs_soundX Ps css hrest i j' (by omega) (by simpa using hj)
      exact ⟨c, by simpa using hc⟩

def exOkX (D S R W x0 x1 y0 y1 U0 U1 : ℕ) (segs : List SegE) (rects : List RectE) (lf : ExLeaf) :
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
    allPairsOkX D (W - credAmt lf) R U0 U1 side lf.chs lf.cvs lf.crs lf.hbx lf.vbx (side ++ lf.Ls) lf.certs

lemma exOkX_of {D S R W x0 x1 y0 y1 U0 U1 : ℕ} {segs : List SegE} {rects : List RectE} {lf : ExLeaf}
    (h1 : exHead D S R W x0 x1 y0 y1 U0 U1 segs rects lf = true)
    (h2 : allPairsOkX D (W - credAmt lf) R U0 U1 (sideE (D * S) x0 x1 y0 y1 lf.wx lf.wy lf.ex lf.ey)
      lf.chs lf.cvs lf.crs lf.hbx lf.vbx (sideE (D * S) x0 x1 y0 y1 lf.wx lf.wy lf.ex lf.ey ++ lf.Ls)
      lf.certs = true) :
    exOkX D S R W x0 x1 y0 y1 U0 U1 segs rects lf = true := by
  simp only [exHead] at h1
  simp only [exOkX, h1, h2, Bool.and_self]

theorem CovMPo.of_exactX {D S Mq R W x0 x1 y0 y1 U0 U1 : ℕ} {pts : List (ℕ × ℕ × ℕ)}
    {segs : List SegE} {rects : List RectE} (hD : 0 < D) (hS : 0 < S) (hR : 0 < R) {lf : ExLeaf}
    (h : exOkX D S R W x0 x1 y0 y1 U0 U1 segs rects lf = true) :
    CovMPo D S Mq R W pts segs rects x0 x1 y0 y1 U0 U1 := by
  simp only [exOkX, Bool.and_eq_true, Nat.blt_eq, Nat.ble_eq, decide_eq_true_eq, List.all_eq_true,
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
    · obtain ⟨cert, hc'⟩ := allPairs_soundX _ _ hpairs i j hij hj
      rw [hiA, hjB] at hc'
      exact pair_soundX hcl hmd hR hc' hu0 hu1 hpos hlt hdetAB ht1 ht2 hv hbd
    · subst hij
      exfalso; apply hdetAB
      have : A = B := hiA.symm.trans hjB
      rw [this, eval_detP]; ring
    · obtain ⟨cert, hc'⟩ := allPairs_soundX _ _ hpairs j i hij hi
      rw [hiA, hjB] at hc'
      refine pair_soundX hcl hmd hR hc' hu0 hu1 hpos hlt ?_ ht2 ht1 hv hbd
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
