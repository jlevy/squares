import Sqpack.LemmaESplit
import Sqpack.LemmaELeafX

/-!
# A pair of `LemmaELeafX` in one kernel check per sub-bin

`LemmaESplit`'s gluing of `binsOk` and `pairOk`, for `binsOkX` and `pairOkX`.
-/

namespace SquarePacking

namespace LemmaELeaf

open BernZ RatU ChordE LemmaE LemmaEPoly LemmaEVert ZMTreeM KArith LemmaEK

lemma binsOkX_step {D W R : ℕ} {side : List PL} {chs cvs : List SegE} {crs : List RectM}
    {hbx vbx : List (List ℕ × List ℕ)} {P Q : PL} {U0 U1 : ℕ} {S : List SubBin} (t : ℕ)
    (ht : t < S.length) (h1 : subOkX D W R side chs cvs crs hbx vbx P Q (bAt U0 S t) (S.getD t dSB) = true)
    (h2 : binsOkX D W R side chs cvs crs hbx vbx P Q (bAt U0 S (t + 1)) U1 (S.drop (t + 1)) = true) :
    binsOkX D W R side chs cvs crs hbx vbx P Q (bAt U0 S t) U1 (S.drop t) = true := by
  rw [List.drop_eq_getElem_cons ht, binsOkX, Bool.and_eq_true]
  rw [List.getD_eq_getElem _ _ ht] at h1
  refine ⟨h1, ?_⟩
  simp only [bAt] at h2
  rwa [List.getD_eq_getElem _ _ ht] at h2

lemma binsOkX_end {D W R : ℕ} {side : List PL} {chs cvs : List SegE} {crs : List RectM}
    {hbx vbx : List (List ℕ × List ℕ)} {P Q : PL} {U0 U1 : ℕ} {S : List SubBin} (n : ℕ)
    (hn : S.length ≤ n) (he : (bAt U0 S n == U1) = true) :
    binsOkX D W R side chs cvs crs hbx vbx P Q (bAt U0 S n) U1 (S.drop n) = true := by
  rw [List.drop_eq_nil_of_le hn, binsOkX]
  exact he

lemma pairOkX_of_sbs {D W R U0 U1 : ℕ} {side : List PL} {chs cvs : List SegE} {crs : List RectM}
    {hbx vbx : List (List ℕ × List ℕ)} {P Q : PL} {cert : PairCert} (hb : isBins cert = true)
    (h : binsOkX D W R side chs cvs crs hbx vbx P Q (bAt U0 (sbsOf cert) 0) U1 ((sbsOf cert).drop 0) = true) :
    pairOkX D W R U0 U1 side chs cvs crs hbx vbx P Q cert = true := by
  cases cert with
  | par => simp [isBins] at hb
  | bins s => simpa [pairOkX, sbsOf, bAt] using h

end LemmaELeaf

end SquarePacking
