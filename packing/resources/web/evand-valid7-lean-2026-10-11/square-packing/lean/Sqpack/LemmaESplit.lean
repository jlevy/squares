import Sqpack.LemmaEDec

/-!
# A heavy pair certificate in small kernel checks

The vertex test of a sub-bin runs over every combination of the segments' alternatives
(`cprod`).  One `decide` over thousands of combinations is slow and memory hungry in the kernel
(its caches live as long as the declaration), so a heavy pair is checked in pieces: each sub-bin on
its own, and a heavy sub-bin's combinations in chunks.  The lemmas here glue the pieces back into
`pairOk`; nothing is assumed beyond the definitions of `LemmaELeaf` and `LemmaEK`.
-/

namespace SquarePacking

namespace LemmaELeaf

open BernZ RatU ChordE LemmaE LemmaEPoly LemmaEVert ZMTreeM KArith LemmaEK

/-! ### Lists in chunks -/

lemma all_chunk_step {α : Type*} (f : α → Bool) (l : List α) (k m : ℕ)
    (h1 : ((l.drop k).take m).all f = true) (h2 : (l.drop (k + m)).all f = true) :
    (l.drop k).all f = true := by
  rw [← List.take_append_drop m (l.drop k), List.all_append, h1, List.drop_drop, Bool.true_and]
  simpa [Nat.add_comm] using h2

lemma all_of_drop_zero {α : Type*} {f : α → Bool} {l : List α} (h : (l.drop 0).all f = true) :
    l.all f = true := by simpa using h

lemma and_of {a b : Bool} (ha : a = true) (hb : b = true) : (a && b) = true := by simp [ha, hb]

/-! ### The vertex test in parts -/

/-- The part of `vertOkK'` before the patterns. -/
def vHead (c : Ctx) (D : ℕ) (σ : Bool) (chs cvs : List SegE) (crs : List RectM)
    (hbx vbx : List (List ℕ × List ℕ)) (v : VCert) : Bool :=
  hbx.length == chs.length && vbx.length == cvs.length &&
    v.hc.length == chs.length && v.vc.length == cvs.length && v.lc.length == crs.length &&
    v.splits.all (fun sp => sp.dm != 0 && sp.dp != 0) &&
    ((chs.zip hbx).zip v.hc).all (fun q => q.2.all fun x =>
      segCOkK c σ (hUps D q.1.1) (hLos D q.1.1) q.1.2 x.1) &&
    ((cvs.zip vbx).zip v.vc).all (fun q => q.2.all fun x =>
      segCOkK c σ (vUps D q.1.1) (vLos D q.1.1) q.1.2 x.1) &&
    (crs.zip v.lc).all (fun p => p.2.1.all (capAOkK c σ v.splits (capXm D p.1)) &&
      p.2.2.all (capAOkK c σ v.splits (capYm D p.1)))

/-- Every segment has an alternative consistent with the pattern. -/
def vPre (v : VCert) (pat : List Bool) : Bool :=
  v.hc.all (fun l => l.any fun x => tagOk pat x.2) &&
    v.vc.all (fun l => l.any fun x => tagOk pat x.2) &&
    v.lc.all (fun l => l.1.any (fun a => tagOk pat (capTag a)) && l.2.any (fun a => tagOk pat (capTag a)))

/-- The combinations of a pattern. -/
def vL (c : Ctx) (D : ℕ) (chs cvs : List SegE) (crs : List RectM)
    (hbx vbx : List (List ℕ × List ℕ)) (v : VCert) (pat : List Bool) : List (List KR) :=
  cprod (reordK (((chs.zip hbx).zip v.hc).map (hAltsPK c D pat) ++
    ((cvs.zip vbx).zip v.vc).map (vAltsPK c D pat) ++
    (crs.zip v.lc).map (lAltsPK c D pat)))

/-- The test of one combination. -/
def vF (c : Ctx) (W : ℕ) (σ : Bool) (b0 b1 R : ℕ) (v : VCert) (pat : List Bool) (comb : List KR) :
    Bool :=
  totOkK c σ b0 b1 R v.splits pat v.fcs (sumK c (comb ++
    (v.splits.zip pat).map (fun x => sprocK c x.1 x.2) ++ [kconst (-(W : ℤ)) 1]))

lemma vertOkK'_eq (c : Ctx) (D W : ℕ) (σ : Bool) (b0 b1 R : ℕ) (chs cvs : List SegE)
    (crs : List RectM) (hbx vbx : List (List ℕ × List ℕ)) (v : VCert) :
    vertOkK' c D W σ b0 b1 R chs cvs crs hbx vbx v =
      (vHead c D σ chs cvs crs hbx vbx v && (pats v.splits.length).all fun pat =>
        vPre v pat && (vL c D chs cvs crs hbx vbx v pat).all (vF c W σ b0 b1 R v pat)) := rfl

lemma vertOkK'_of {c : Ctx} {D W : ℕ} {σ : Bool} {b0 b1 R : ℕ} {chs cvs : List SegE}
    {crs : List RectM} {hbx vbx : List (List ℕ × List ℕ)} {v : VCert}
    (h0 : vHead c D σ chs cvs crs hbx vbx v = true)
    (h1 : ((pats v.splits.length).drop 0).all (fun pat =>
      vPre v pat && (vL c D chs cvs crs hbx vbx v pat).all (vF c W σ b0 b1 R v pat)) = true) :
    vertOkK' c D W σ b0 b1 R chs cvs crs hbx vbx v = true := by
  rw [vertOkK'_eq, h0, Bool.true_and]
  exact all_of_drop_zero h1

/-! ### A sub-bin, the sub-bins, the pair -/

def dSB : SubBin := ⟨0, true, 0, .out 0 0⟩

/-- The decoder of one encoded sub-bin (`LemmaEDec`): a pair certificate stored as `.bins` of these
decodes, in a kernel check, only the sub-bins it looks at. -/
def decSB (cs : List ℕ) : SubBin := (pSubBin (decNums cs)).1

def isVal : Kind → Bool
  | .val _ => true
  | .out _ _ => false

def vcOf : Kind → VCert
  | .val c => c
  | .out _ _ => ⟨[], [], [], [], []⟩

lemma subOk_of_val {D W R : ℕ} {side : List PL} {chs cvs : List SegE} {crs : List RectM}
    {hbx vbx : List (List ℕ × List ℕ)} {P Q : PL} {b0 : ℕ} {sb : SubBin}
    (hb : Nat.blt b0 sb.b1 = true) (hs : signOk sb.σ (detP P Q) sb.m b0 sb.b1 R = true)
    (hk : isVal sb.kind = true) (hsp : (vcOf sb.kind).splits.all (fun sp => sp.q.d != 0) = true)
    (hv : vertOkK' (mkCtx (detP P Q) (xP P Q) (yP P Q) b0 sb.b1 R kK) D W sb.σ b0 sb.b1 R
      chs cvs crs hbx vbx (vcOf sb.kind) = true) :
    subOk D W R side chs cvs crs hbx vbx P Q b0 sb = true := by
  obtain ⟨b1, σ, m, kind⟩ := sb
  cases kind with
  | out k m' => simp [isVal] at hk
  | val c =>
    simp only [vcOf] at hsp hv
    simp only [subOk, hb, hs, hsp, Bool.true_and]
    exact hv

/-- The lower end of the `t`-th sub-bin. -/
def bAt (U0 : ℕ) (S : List SubBin) : ℕ → ℕ
  | 0 => U0
  | t + 1 => (S.getD t dSB).b1

lemma binsOk_step {D W R : ℕ} {side : List PL} {chs cvs : List SegE} {crs : List RectM}
    {hbx vbx : List (List ℕ × List ℕ)} {P Q : PL} {U0 U1 : ℕ} {S : List SubBin} (t : ℕ)
    (ht : t < S.length) (h1 : subOk D W R side chs cvs crs hbx vbx P Q (bAt U0 S t) (S.getD t dSB) = true)
    (h2 : binsOk D W R side chs cvs crs hbx vbx P Q (bAt U0 S (t + 1)) U1 (S.drop (t + 1)) = true) :
    binsOk D W R side chs cvs crs hbx vbx P Q (bAt U0 S t) U1 (S.drop t) = true := by
  rw [List.drop_eq_getElem_cons ht, binsOk, Bool.and_eq_true]
  rw [List.getD_eq_getElem _ _ ht] at h1
  refine ⟨h1, ?_⟩
  simp only [bAt] at h2
  rwa [List.getD_eq_getElem _ _ ht] at h2

lemma binsOk_end {D W R : ℕ} {side : List PL} {chs cvs : List SegE} {crs : List RectM}
    {hbx vbx : List (List ℕ × List ℕ)} {P Q : PL} {U0 U1 : ℕ} {S : List SubBin} (n : ℕ)
    (hn : S.length ≤ n) (he : (bAt U0 S n == U1) = true) :
    binsOk D W R side chs cvs crs hbx vbx P Q (bAt U0 S n) U1 (S.drop n) = true := by
  rw [List.drop_eq_nil_of_le hn, binsOk]
  exact he

def isBins : PairCert → Bool
  | .bins _ => true
  | .par => false

def sbsOf : PairCert → List SubBin
  | .bins s => s
  | .par => []

lemma pairOk_of_sbs {D W R U0 U1 : ℕ} {side : List PL} {chs cvs : List SegE} {crs : List RectM}
    {hbx vbx : List (List ℕ × List ℕ)} {P Q : PL} {cert : PairCert} (hb : isBins cert = true)
    (h : binsOk D W R side chs cvs crs hbx vbx P Q (bAt U0 (sbsOf cert) 0) U1 ((sbsOf cert).drop 0) = true) :
    pairOk D W R U0 U1 side chs cvs crs hbx vbx P Q cert = true := by
  cases cert with
  | par => simp [isBins] at hb
  | bins s => simpa [pairOk, sbsOf, bAt] using h

end LemmaELeaf

end SquarePacking
