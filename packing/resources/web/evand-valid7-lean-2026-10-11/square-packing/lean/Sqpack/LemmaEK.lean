import Sqpack.LemmaEVert
import Sqpack.KBern

/-!
# The vertex test in Kronecker form

On a sub-bin `[U0/R, U1/R]` the degree-`n` Bernstein coefficients of `p` (scaled by binomials) are
the coefficients of `γ(t) = Σₖ pₖ (U0 + U1 t)ᵏ (R + R t)ⁿ⁻ᵏ`.  With `X = 2ᴷ`, `A = U0 + U1 X` and
`B = R (1 + X)`, the number `γ(X) = Bⁿ p(A/B)` carries all of them at once: when `2 Σ|γᵢ| < X` they
are its balanced base-`X` digits, and they are all `≥ 0` iff `γ(X) ≥ 0` and no digit has its top bit
set.  `Bⁿ p(A/B)` is computed directly through the ring operations (`KH`): the numerators of the
rational functions of the vertex test are never expanded as lists.

`KR` carries the list form `r` alongside; the kernel evaluates it only where it is used (the
common-factor certificates).
-/

namespace SquarePacking

namespace LemmaEK

open BernZ RatU ChordE LemmaE LemmaEPoly LemmaEVert ZMTreeM KArith

/-- The vertex context: the evaluation point, the polynomials of the vertex and their images. -/
structure Ctx where
  A : ℤ
  B : ℕ
  K : ℕ
  M : ℕ
  Δ : Poly
  X : Poly
  Y : Poly
  hΔ : KH
  hX : KH
  hY : KH
  hC : KH
  hS : KH
  hN : KH

def mkCtx (Δ X Y : Poly) (b0 b1 R K : ℕ) : Ctx :=
  let A : ℤ := (b0 : ℤ) + (b1 : ℤ) * 2 ^ K
  let B : ℕ := R * (1 + 2 ^ K)
  ⟨A, B, K, max (b0 + b1) (2 * R), Δ, X, Y, hP A B Δ, hP A B X, hP A B Y, hP A B Cp, hP A B Sp,
    hP A B Np⟩

/-! ## Rational functions -/

/-- A rational function with the image of its numerator. -/
structure KR where
  h : KH
  r : RF

def kRF (c : Ctx) (r : RF) : KR := ⟨hP c.A c.B r.num, r⟩

def kconst (n : ℤ) (d : ℕ) : KR := ⟨hconst n, RF.const n d⟩

def kraise (c : Ctx) (r : KR) (a b cc g m : ℕ) : KR :=
  ⟨hmul (hsmul m r.h) (hmul (hpow c.hΔ a) (hmul (hpow c.hC b) (hmul (hpow c.hS cc) (hpow c.hN g)))),
    raise c.Δ r.r a b cc g m⟩

def kadd (c : Ctx) (r s : KR) : KR :=
  let e := max r.r.e s.r.e
  let i := max r.r.i s.r.i
  let j := max r.r.j s.r.j
  let k := max r.r.k s.r.k
  let l := Nat.lcm r.r.d s.r.d
  ⟨hadd c.B (kraise c r (e - r.r.e) (i - r.r.i) (j - r.r.j) (k - r.r.k) (l / r.r.d)).h
      (kraise c s (e - s.r.e) (i - s.r.i) (j - s.r.j) (k - s.r.k) (l / s.r.d)).h,
    RF.add c.Δ r.r s.r⟩

def kmul (r s : KR) : KR := ⟨hmul r.h s.h, RF.mul r.r s.r⟩

def kneg (r : KR) : KR := ⟨hsmul (-1) r.h, RF.neg r.r⟩

def ckK (c : Ctx) (σ : Bool) (r : KR) : Bool := hcheck c.K c.M (!(σ || r.r.e % 2 == 0)) r.h

/-! ## Scaled lines -/

structure KSL where
  P1 : KH
  P2 : KH
  P3 : KH
  s : SL

def kSL (c : Ctx) (L : SL) : KSL := ⟨hP c.A c.B L.P.1, hP c.A c.B L.P.2.1, hP c.A c.B L.P.2.2, L⟩

def kden (c : Ctx) (L : KSL) : KH :=
  hmul (hpow c.hC L.s.i) (hmul (hpow c.hS L.s.j) (hmul (hpow c.hN L.s.k) (hconst L.s.d)))

def ksub (c : Ctx) (L M : KSL) : KSL :=
  let dM := kden c M
  let dL := kden c L
  ⟨hadd c.B (hmul dM L.P1) (hsmul (-1) (hmul dL M.P1)),
    hadd c.B (hmul dM L.P2) (hsmul (-1) (hmul dL M.P2)),
    hadd c.B (hmul dM L.P3) (hsmul (-1) (hmul dL M.P3)), L.s.sub M.s⟩

def katV (c : Ctx) (L : KSL) : KR :=
  ⟨hadd c.B (hadd c.B (hmul L.P1 c.hX) (hmul L.P2 c.hY)) (hmul L.P3 c.hΔ), L.s.atV c.Δ c.X c.Y⟩

/-! ## The vertex test, mirrored -/

def kget (c : Ctx) (Ls : List SL) (i : ℕ) : KSL := kSL c (Ls.getD i (SL.cst 0 1))

def segValK (c : Ctx) (w D len : ℕ) (ups los : List SL) (iu il : ℕ) : KR :=
  kmul (kconst (w * D : ℕ) len) (katV c (ksub c (kget c ups iu) (kget c los il)))

def ghOkK (c : Ctx) (σ : Bool) (cap : SL) (mode : ℕ) : Bool :=
  if mode = 0 then ckK c σ (katV c (ksub c (kSL c (SL.cst 0 1)) (kSL c cap)))
  else if mode = 1 then true
  else ckK c σ (katV c (ksub c (kSL c cap) (kSL c (sSL 1))))

def ghUK (c : Ctx) (cap : SL) (mode : ℕ) : KR :=
  if mode = 0 then kconst 0 1
  else if mode = 1 then
    kmul (kmul (katV c (kSL c cap)) (katV c (kSL c cap))) (kRF c ⟨BernZ.mul Np Np, 0, 1, 1, 0, 2⟩)
  else kmul (katV c (ksub c (kSL c cap) (kSL c (sSL 2)))) (kRF c ⟨Np, 0, 1, 0, 0, 1⟩)

def segOkAK (c : Ctx) (σ : Bool) (ups los : List SL) (Ua La : List ℕ) : Bool :=
  !Ua.isEmpty && !La.isEmpty && Ua.all (· < ups.length) && La.all (· < los.length) &&
    ups.all (fun U => Ua.any fun a => ckK c σ (katV c (ksub c (kSL c U) (kget c ups a)))) &&
    los.all (fun L => La.any fun b => ckK c σ (katV c (ksub c (kget c los b) (kSL c L))))

def segAltsK (c : Ctx) (w D len : ℕ) (ups los : List SL) (Ua La : List ℕ) : List KR :=
  Ua.flatMap fun a => La.map fun b => segValK c w D len ups los a b

def segCAltsK (c : Ctx) (w D len : ℕ) (ups los : List SL) (bx : List ℕ × List ℕ) : SegC → List KR
  | .drop => [kconst 0 1]
  | .box => segAltsK c w D len ups los bx.1 bx.2
  | .alt Ua La => segAltsK c w D len ups los Ua La

def segCOkK (c : Ctx) (σ : Bool) (ups los : List SL) (bx : List ℕ × List ℕ) : SegC → Bool
  | .drop => true
  | .box => !bx.1.isEmpty && !bx.2.isEmpty && bx.1.all (· < ups.length) && bx.2.all (· < los.length)
  | .alt Ua La => segOkAK c σ ups los Ua La

def sprocK (c : Ctx) (sp : Split) (b : Bool) : KR :=
  if b then kneg (kmul (kconst sp.np sp.dp) (katV c (kSL c sp.q)))
  else kmul (kconst sp.nm sp.dm) (katV c (kSL c sp.q))

def capAOkK (c : Ctx) (σ : Bool) (splits : List Split) (cap : SL) : CapA → Bool
  | .zeroC => ghOkK c σ cap 0
  | .zeroT k => decide (k < splits.length) && splitAt splits k == cap
  | .par => true
  | .parT k _ => decide (k < splits.length)
  | .linC => ghOkK c σ cap 2
  | .linT k => decide (k < splits.length) && splitAt splits k == cap.sub (sSL 1)

def capAUK (c : Ctx) (cap : SL) : CapA → KR
  | .zeroC => ghUK c cap 0
  | .zeroT _ => ghUK c cap 0
  | .par => ghUK c cap 1
  | .parT _ _ => ghUK c cap 1
  | .linC => ghUK c cap 2
  | .linT _ => ghUK c cap 2

def lebRFK (c : Ctx) (D : ℕ) (r : RectM) (ax ay : CapA) : KR :=
  kmul (kconst r.1.2.2.2.2 1) (kadd c (kadd c (kconst 1 1)
    (kneg (capAUK c (capXm D r) ax))) (kneg (capAUK c (capYm D r) ay)))

def slAtPK (c : Ctx) (L : SL) (x y q : ℕ) : KR :=
  let K := kSL c L
  ⟨hadd c.B (hadd c.B (hsmul x K.P1) (hsmul y K.P2)) (hsmul q K.P3), slAtP L x y q⟩

def mcRFK (c : Ctx) (A B bs α β : KR) : KR :=
  kmul (kRF c i2cRF) (kadd c (kadd c
    (kmul (kmul (kconst 2 1) (kRF c cRF)) (kadd c (kadd c (kmul A β) (kmul B α)) (kneg (kmul A B))))
    (kmul (kRF c sRF) (kadd c (kmul (kmul (kconst 2 1) bs) β) (kneg (kmul bs bs)))))
    (kneg (kmul (kRF c sRF) (kmul α α))))

def lebRFsK (c : Ctx) (D : ℕ) (r : RectM) (ax ay : CapA) : List KR :=
  let w := kconst r.1.2.2.2.2 1
  let gx := kneg (capAUK c (capXm D r) ax)
  let gy := kneg (capAUK c (capYm D r) ay)
  match r.2.2.2 with
  | .std => [lebRFK c D r ax ay]
  | .c3 xa ya ym q =>
    let aL := (capX D r.1.1).sub (sSL 1)
    let bL := capY D r.1.2.1
    let mc := mcRFK c (slAtPK c aL xa ya q) (slAtPK c bL xa ya q) (slAtPK c bL xa ym q)
      (katV c (kSL c ((capXm D r).sub (sSL 1)))) (katV c (kSL c (capYm D r)))
    [kmul w (kadd c (kadd c (kadd c (kconst 1 1) gx) gy) mc), kmul w (kadd c (kconst 1 1) gx)]
  | .xc xa ya ym q =>
    let aL := capX D r.1.1
    let bL := (capY D r.1.2.1).sub (cSL 1)
    let mc := mcRFK c (slAtPK c aL xa ya q) (slAtPK c bL xa ya q) (slAtPK c bL xa ym q)
      (katV c (kSL c (capXm D r))) (katV c (kSL c ((capYm D r).sub (cSL 1))))
    [kmul w (kadd c (kadd c (kconst 1 1) gy) mc), lebRFK c D r ax ay]

def sumK (c : Ctx) : List KR → KR
  | [] => kconst 0 1
  | r :: rs => kadd c r (sumK c rs)

def totOkK (c : Ctx) (σ : Bool) (b0 b1 R : ℕ) (splits : List Split) (pat : List Bool)
    (fcs : List FCert) (T : KR) : Bool :=
  ckK c σ T || fcs.any fun f => fcOk σ c.Δ c.X c.Y b0 b1 R splits pat f T.r

def hAltsPK (c : Ctx) (D : ℕ) (pat : List Bool) (q : (SegE × (List ℕ × List ℕ)) × List (SegC × Tag)) :
    List KR :=
  (q.2.filter fun x => tagOk pat x.2).flatMap fun x =>
    segCAltsK c q.1.1.2.2.2.2 D (q.1.1.2.2.1 - q.1.1.1) (hUps D q.1.1) (hLos D q.1.1) q.1.2 x.1
def vAltsPK (c : Ctx) (D : ℕ) (pat : List Bool) (q : (SegE × (List ℕ × List ℕ)) × List (SegC × Tag)) :
    List KR :=
  (q.2.filter fun x => tagOk pat x.2).flatMap fun x =>
    segCAltsK c q.1.1.2.2.2.2 D (q.1.1.2.2.2.1 - q.1.1.2.1) (vUps D q.1.1) (vLos D q.1.1) q.1.2 x.1
def lAltsPK (c : Ctx) (D : ℕ) (pat : List Bool) (p : RectM × (List CapA × List CapA)) : List KR :=
  (p.2.1.filter fun a => tagOk pat (capTag a)).flatMap fun ax =>
    (p.2.2.filter fun a => tagOk pat (capTag a)).flatMap fun ay => lebRFsK c D p.1 ax ay

def reordK (L : List (List KR)) : List (List KR) :=
  L.filter (fun l => l.length != 1) ++ L.filter (fun l => l.length == 1)

def vertOkK' (c : Ctx) (D W : ℕ) (σ : Bool) (b0 b1 R : ℕ) (chs cvs : List SegE)
    (crs : List RectM) (hbx vbx : List (List ℕ × List ℕ)) (v : VCert) : Bool :=
  hbx.length == chs.length && vbx.length == cvs.length &&
    v.hc.length == chs.length && v.vc.length == cvs.length && v.lc.length == crs.length &&
    v.splits.all (fun sp => sp.dm != 0 && sp.dp != 0) &&
    ((chs.zip hbx).zip v.hc).all (fun q => q.2.all fun x =>
      segCOkK c σ (hUps D q.1.1) (hLos D q.1.1) q.1.2 x.1) &&
    ((cvs.zip vbx).zip v.vc).all (fun q => q.2.all fun x =>
      segCOkK c σ (vUps D q.1.1) (vLos D q.1.1) q.1.2 x.1) &&
    (crs.zip v.lc).all (fun p => p.2.1.all (capAOkK c σ v.splits (capXm D p.1)) &&
      p.2.2.all (capAOkK c σ v.splits (capYm D p.1))) &&
    (pats v.splits.length).all fun pat =>
      v.hc.all (fun l => l.any fun x => tagOk pat x.2) &&
      v.vc.all (fun l => l.any fun x => tagOk pat x.2) &&
      v.lc.all (fun l => l.1.any (fun a => tagOk pat (capTag a)) && l.2.any (fun a => tagOk pat (capTag a))) &&
      (cprod (reordK (((chs.zip hbx).zip v.hc).map (hAltsPK c D pat) ++
          ((cvs.zip vbx).zip v.vc).map (vAltsPK c D pat) ++
          (crs.zip v.lc).map (lAltsPK c D pat)))).all fun comb =>
        totOkK c σ b0 b1 R v.splits pat v.fcs (sumK c (comb ++
          (v.splits.zip pat).map (fun x => sprocK c x.1 x.2) ++ [kconst (-(W : ℤ)) 1]))

/-- The evaluation point `2ᴷ` used by the leaf test. -/
def kK : ℕ := 1024

/-- **The vertex test** at the evaluation point `2ᴷ`. -/
def vertOkK (D W : ℕ) (σ : Bool) (Δ X Y : Poly) (b0 b1 R K : ℕ) (chs cvs : List SegE)
    (crs : List RectM) (hbx vbx : List (List ℕ × List ℕ)) (v : VCert) : Bool :=
  vertOkK' (mkCtx Δ X Y b0 b1 R K) D W σ b0 b1 R chs cvs crs hbx vbx v

/-! ## Soundness: every image carries its rational function -/

/-- The context carries its polynomials. -/
structure CtxOk (c : Ctx) : Prop where
  hB : 0 < c.B
  hΔ : RepH c.A c.B c.Δ c.hΔ
  hX : RepH c.A c.B c.X c.hX
  hY : RepH c.A c.B c.Y c.hY
  hC : RepH c.A c.B Cp c.hC
  hS : RepH c.A c.B Sp c.hS
  hN : RepH c.A c.B Np c.hN

lemma mkCtx_ok {Δ X Y : Poly} {b0 b1 R K : ℕ} (hR : 0 < R) : CtxOk (mkCtx Δ X Y b0 b1 R K) := by
  have hB : 0 < R * (1 + 2 ^ K) := Nat.mul_pos hR (by positivity)
  exact ⟨hB, rep_hP hB _, rep_hP hB _, rep_hP hB _, rep_hP hB _, rep_hP hB _, rep_hP hB _⟩

def RepK (c : Ctx) (r : KR) : Prop := RepH c.A c.B r.r.num r.h

def RepS (c : Ctx) (L : KSL) : Prop :=
  RepH c.A c.B L.s.P.1 L.P1 ∧ RepH c.A c.B L.s.P.2.1 L.P2 ∧ RepH c.A c.B L.s.P.2.2 L.P3

section rep

variable {c : Ctx} (hc : CtxOk c)
include hc

lemma rep_kRF (r : RF) : RepK c (kRF c r) := rep_hP hc.hB r.num

omit hc in
lemma rep_kconst (n : ℤ) (d : ℕ) : RepK c (kconst n d) := rep_hconst n

lemma rep_kraise {r : KR} (hr : RepK c r) (a b cc g m : ℕ) : RepK c (kraise c r a b cc g m) :=
  rep_hmul (rep_hsmul _ hr) (rep_hmul (rep_hpow hc.hΔ a) (rep_hmul (rep_hpow hc.hC b)
    (rep_hmul (rep_hpow hc.hS cc) (rep_hpow hc.hN g))))

lemma rep_kadd {r s : KR} (hr : RepK c r) (hs : RepK c s) : RepK c (kadd c r s) :=
  rep_hadd hc.hB (rep_kraise hc hr _ _ _ _ _) (rep_kraise hc hs _ _ _ _ _)

omit hc in
lemma rep_kmul {r s : KR} (hr : RepK c r) (hs : RepK c s) : RepK c (kmul r s) := rep_hmul hr hs

omit hc in
lemma rep_kneg {r : KR} (hr : RepK c r) : RepK c (kneg r) := rep_hsmul (-1) hr

lemma rep_kSL (L : SL) : RepS c (kSL c L) := ⟨rep_hP hc.hB _, rep_hP hc.hB _, rep_hP hc.hB _⟩

lemma rep_kden (L : KSL) : RepH c.A c.B (sdenP L.s) (kden c L) :=
  rep_hmul (rep_hpow hc.hC _) (rep_hmul (rep_hpow hc.hS _) (rep_hmul (rep_hpow hc.hN _) (rep_hconst _)))

lemma rep_ksub {L M : KSL} (hL : RepS c L) (hM : RepS c M) : RepS c (ksub c L M) :=
  ⟨rep_hadd hc.hB (rep_hmul (rep_kden hc M) hL.1) (rep_hsmul (-1) (rep_hmul (rep_kden hc L) hM.1)),
    rep_hadd hc.hB (rep_hmul (rep_kden hc M) hL.2.1) (rep_hsmul (-1) (rep_hmul (rep_kden hc L) hM.2.1)),
    rep_hadd hc.hB (rep_hmul (rep_kden hc M) hL.2.2) (rep_hsmul (-1) (rep_hmul (rep_kden hc L) hM.2.2))⟩

lemma rep_katV {L : KSL} (hL : RepS c L) : RepK c (katV c L) :=
  rep_hadd hc.hB (rep_hadd hc.hB (rep_hmul hL.1 hc.hX) (rep_hmul hL.2.1 hc.hY)) (rep_hmul hL.2.2 hc.hΔ)

lemma rep_slAtPK (L : SL) (x y q : ℕ) : RepK c (slAtPK c L x y q) :=
  have hL := rep_kSL hc L
  rep_hadd hc.hB (rep_hadd hc.hB (rep_hsmul _ hL.1) (rep_hsmul _ hL.2.1)) (rep_hsmul _ hL.2.2)

end rep

section rep2

variable {c : Ctx} (hc : CtxOk c)
include hc

lemma rep_segValK (w D len : ℕ) (ups los : List SL) (iu il : ℕ) :
    RepK c (segValK c w D len ups los iu il) :=
  rep_kmul (rep_kconst _ _) (rep_katV hc (rep_ksub hc (rep_kSL hc _) (rep_kSL hc _)))

lemma rep_ghUK (cap : SL) (mode : ℕ) : RepK c (ghUK c cap mode) := by
  unfold ghUK
  split_ifs
  · exact rep_kconst _ _
  · exact rep_kmul (rep_kmul (rep_katV hc (rep_kSL hc _)) (rep_katV hc (rep_kSL hc _))) (rep_kRF hc _)
  · exact rep_kmul (rep_katV hc (rep_ksub hc (rep_kSL hc _) (rep_kSL hc _))) (rep_kRF hc _)

lemma rep_capAUK (cap : SL) (a : CapA) : RepK c (capAUK c cap a) := by
  cases a <;> exact rep_ghUK hc _ _

lemma rep_lebRFK (D : ℕ) (r : RectM) (ax ay : CapA) : RepK c (lebRFK c D r ax ay) :=
  rep_kmul (rep_kconst _ _) (rep_kadd hc (rep_kadd hc (rep_kconst _ _)
    (rep_kneg (rep_capAUK hc _ _))) (rep_kneg (rep_capAUK hc _ _)))

lemma rep_mcRFK {A B bs α β : KR} (hA : RepK c A) (hB : RepK c B) (hbs : RepK c bs)
    (hα : RepK c α) (hβ : RepK c β) : RepK c (mcRFK c A B bs α β) :=
  rep_kmul (rep_kRF hc _) (rep_kadd hc (rep_kadd hc
    (rep_kmul (rep_kmul (rep_kconst _ _) (rep_kRF hc _)) (rep_kadd hc (rep_kadd hc (rep_kmul hA hβ)
      (rep_kmul hB hα)) (rep_kneg (rep_kmul hA hB))))
    (rep_kmul (rep_kRF hc _) (rep_kadd hc (rep_kmul (rep_kmul (rep_kconst _ _) hbs) hβ)
      (rep_kneg (rep_kmul hbs hbs)))))
    (rep_kneg (rep_kmul (rep_kRF hc _) (rep_kmul hα hα))))

lemma rep_lebRFsK (D : ℕ) (r : RectM) (ax ay : CapA) : ∀ x ∈ lebRFsK c D r ax ay, RepK c x := by
  unfold lebRFsK
  split
  · simp only [List.mem_singleton]; rintro x rfl; exact rep_lebRFK hc _ _ _ _
  · simp only [List.mem_cons, List.mem_singleton, List.not_mem_nil, or_false]
    rintro x (rfl | rfl)
    · exact rep_kmul (rep_kconst _ _) (rep_kadd hc (rep_kadd hc (rep_kadd hc (rep_kconst _ _)
        (rep_kneg (rep_capAUK hc _ _))) (rep_kneg (rep_capAUK hc _ _))) (rep_mcRFK hc
        (rep_slAtPK hc _ _ _ _) (rep_slAtPK hc _ _ _ _) (rep_slAtPK hc _ _ _ _)
        (rep_katV hc (rep_kSL hc _)) (rep_katV hc (rep_kSL hc _))))
    · exact rep_kmul (rep_kconst _ _) (rep_kadd hc (rep_kconst _ _) (rep_kneg (rep_capAUK hc _ _)))
  · simp only [List.mem_cons, List.mem_singleton, List.not_mem_nil, or_false]
    rintro x (rfl | rfl)
    · exact rep_kmul (rep_kconst _ _) (rep_kadd hc (rep_kadd hc (rep_kconst _ _)
        (rep_kneg (rep_capAUK hc _ _))) (rep_mcRFK hc
        (rep_slAtPK hc _ _ _ _) (rep_slAtPK hc _ _ _ _) (rep_slAtPK hc _ _ _ _)
        (rep_katV hc (rep_kSL hc _)) (rep_katV hc (rep_kSL hc _))))
    · exact rep_lebRFK hc _ _ _ _

lemma rep_segAltsK (w D len : ℕ) (ups los : List SL) (Ua La : List ℕ) :
    ∀ x ∈ segAltsK c w D len ups los Ua La, RepK c x := by
  intro x hx
  simp only [segAltsK, List.mem_flatMap, List.mem_map] at hx
  obtain ⟨a, _, b, _, rfl⟩ := hx
  exact rep_segValK hc _ _ _ _ _ _ _

lemma rep_segCAltsK (w D len : ℕ) (ups los : List SL) (bx : List ℕ × List ℕ) (sc : SegC) :
    ∀ x ∈ segCAltsK c w D len ups los bx sc, RepK c x := by
  cases sc with
  | drop => simp only [segCAltsK, List.mem_singleton]; rintro x rfl; exact rep_kconst _ _
  | box => exact rep_segAltsK hc _ _ _ _ _ _ _
  | alt Ua La => exact rep_segAltsK hc _ _ _ _ _ _ _

lemma rep_hAltsPK (D : ℕ) (pat : List Bool) (q : (SegE × (List ℕ × List ℕ)) × List (SegC × Tag)) :
    ∀ x ∈ hAltsPK c D pat q, RepK c x := by
  intro x hx
  simp only [hAltsPK, List.mem_flatMap] at hx
  obtain ⟨y, _, hy⟩ := hx
  exact rep_segCAltsK hc _ _ _ _ _ _ _ x hy

lemma rep_vAltsPK (D : ℕ) (pat : List Bool) (q : (SegE × (List ℕ × List ℕ)) × List (SegC × Tag)) :
    ∀ x ∈ vAltsPK c D pat q, RepK c x := by
  intro x hx
  simp only [vAltsPK, List.mem_flatMap] at hx
  obtain ⟨y, _, hy⟩ := hx
  exact rep_segCAltsK hc _ _ _ _ _ _ _ x hy

lemma rep_lAltsPK (D : ℕ) (pat : List Bool) (p : RectM × (List CapA × List CapA)) :
    ∀ x ∈ lAltsPK c D pat p, RepK c x := by
  intro x hx
  simp only [lAltsPK, List.mem_flatMap] at hx
  obtain ⟨ax, _, ay, _, hy⟩ := hx
  exact rep_lebRFsK hc _ _ _ _ x hy

lemma rep_sprocK (sp : Split) (b : Bool) : RepK c (sprocK c sp b) := by
  unfold sprocK
  split_ifs
  · exact rep_kneg (rep_kmul (rep_kconst _ _) (rep_katV hc (rep_kSL hc _)))
  · exact rep_kmul (rep_kconst _ _) (rep_katV hc (rep_kSL hc _))

lemma rep_sumK : ∀ l : List KR, (∀ x ∈ l, RepK c x) → RepK c (sumK c l)
  | [], _ => rep_kconst _ _
  | r :: rs, h => rep_kadd hc (h r List.mem_cons_self)
      (rep_sumK rs fun x hx => h x (List.mem_cons_of_mem _ hx))

end rep2

/-! ## The list forms -/

section lists

variable (c : Ctx)

lemma segAltsK_r (w D len : ℕ) (ups los : List SL) (Ua La : List ℕ) :
    (segAltsK c w D len ups los Ua La).map KR.r = segAlts c.Δ c.X c.Y w D len ups los Ua La := by
  simp only [segAltsK, segAlts, List.map_flatMap, List.map_map]
  rfl

lemma segCAltsK_r (w D len : ℕ) (ups los : List SL) (bx : List ℕ × List ℕ) (sc : SegC) :
    (segCAltsK c w D len ups los bx sc).map KR.r = segCAlts c.Δ c.X c.Y w D len ups los bx sc := by
  cases sc with
  | drop => rfl
  | box => exact segAltsK_r c _ _ _ _ _ _ _
  | alt Ua La => exact segAltsK_r c _ _ _ _ _ _ _

lemma hAltsPK_r (D : ℕ) (pat : List Bool) (q : (SegE × (List ℕ × List ℕ)) × List (SegC × Tag)) :
    (hAltsPK c D pat q).map KR.r = hAltsP c.Δ c.X c.Y D pat q := by
  simp only [hAltsPK, hAltsP, List.map_flatMap, segCAltsK_r]

lemma vAltsPK_r (D : ℕ) (pat : List Bool) (q : (SegE × (List ℕ × List ℕ)) × List (SegC × Tag)) :
    (vAltsPK c D pat q).map KR.r = vAltsP c.Δ c.X c.Y D pat q := by
  simp only [vAltsPK, vAltsP, List.map_flatMap, segCAltsK_r]

lemma ghUK_r (cap : SL) (mode : ℕ) : (ghUK c cap mode).r = ghU c.Δ c.X c.Y cap mode := by
  unfold ghUK ghU; split_ifs <;> rfl

lemma capAUK_r (cap : SL) (a : CapA) : (capAUK c cap a).r = capAU c.Δ c.X c.Y cap a := by
  cases a <;> exact ghUK_r c _ _

lemma lebRFK_r (D : ℕ) (r : RectM) (ax ay : CapA) : (lebRFK c D r ax ay).r = lebRF c.Δ c.X c.Y D r ax ay := by
  simp only [lebRFK, lebRF, kmul, kadd, kneg, kconst, capAUK_r]

lemma lebRFsK_r (D : ℕ) (r : RectM) (ax ay : CapA) :
    (lebRFsK c D r ax ay).map KR.r = lebRFs c.Δ c.X c.Y D r ax ay := by
  obtain ⟨r1, mx, my, k⟩ := r
  cases k <;> simp only [lebRFsK, lebRFs, List.map_cons, List.map_nil, kmul, kadd, kneg, kconst,
    capAUK_r, lebRFK_r, mcRFK, mcRF, kRF, slAtPK, katV, kSL] <;> rfl

lemma lAltsPK_r (D : ℕ) (pat : List Bool) (p : RectM × (List CapA × List CapA)) :
    (lAltsPK c D pat p).map KR.r = lAltsP c.Δ c.X c.Y D pat p := by
  simp only [lAltsPK, lAltsP, List.map_flatMap, lebRFsK_r]

lemma sumK_r : ∀ l : List KR, (sumK c l).r = sumRF c.Δ (l.map KR.r)
  | [] => rfl
  | r :: rs => by
    show RF.add c.Δ r.r (sumK c rs).r = _
    rw [sumK_r rs]; rfl

lemma sprocK_r (sp : Split) (b : Bool) : (sprocK c sp b).r = sproc c.Δ c.X c.Y sp b := by
  unfold sprocK sproc; split_ifs <;> rfl

end lists

lemma reord_map (L : List (List KR)) :
    reord (L.map (List.map KR.r)) = (reordK L).map (List.map KR.r) := by
  simp [reord, reordK, List.filter_map, Function.comp_def]

lemma cprod_map {α β : Type*} (f : α → β) :
    ∀ L : List (List α), cprod (L.map (List.map f)) = (cprod L).map (List.map f)
  | [] => rfl
  | l :: L => by
    simp only [List.map_cons, cprod, cprod_map f L, List.flatMap_map, List.map_flatMap, List.map_map]
    rfl

/-! ## The Kronecker test implies the list test with the checker `ckP` -/

open Classical in
/-- `r` has an image that passes the Kronecker test. -/
noncomputable def ckP (c : Ctx) (σ : Bool) (r : RF) : Bool :=
  decide (∃ kr : KR, RepK c kr ∧ kr.r = r ∧ ckK c σ kr = true)

lemma ckP_of {c : Ctx} {σ : Bool} {kr : KR} (hk : RepK c kr) (h : ckK c σ kr = true) :
    ckP c σ kr.r = true := by
  unfold ckP; simp only [decide_eq_true_eq]; exact ⟨kr, hk, rfl, h⟩

section imp

variable {c : Ctx} (hc : CtxOk c)
include hc

lemma segCOkK_imp {σ : Bool} {ups los : List SL} {bx : List ℕ × List ℕ} {sc : SegC} (b0 b1 R : ℕ)
    (h : segCOkK c σ ups los bx sc = true) :
    segCOk (ckP c σ) σ c.Δ c.X c.Y b0 b1 R ups los bx sc = true := by
  cases sc with
  | drop => rfl
  | box => exact h
  | alt Ua La =>
    simp only [segCOkK, segOkAK, segCOk, segOkA, Bool.and_eq_true, List.all_eq_true,
      List.any_eq_true] at h ⊢
    obtain ⟨⟨h1, h2⟩, h3⟩ := h
    refine ⟨⟨h1, fun U hU => ?_⟩, fun L hL => ?_⟩
    · obtain ⟨a, ha, hk⟩ := h2 U hU
      exact ⟨a, ha, ckP_of (rep_katV hc (rep_ksub hc (rep_kSL hc _) (rep_kSL hc _))) hk⟩
    · obtain ⟨b, hb, hk⟩ := h3 L hL
      exact ⟨b, hb, ckP_of (rep_katV hc (rep_ksub hc (rep_kSL hc _) (rep_kSL hc _))) hk⟩

lemma ghOkK_imp {σ : Bool} {cap : SL} {mode : ℕ} (b0 b1 R : ℕ) (h : ghOkK c σ cap mode = true) :
    ghOk (ckP c σ) σ c.Δ c.X c.Y b0 b1 R cap mode = true := by
  unfold ghOkK at h; unfold ghOk
  split_ifs at h ⊢
  · exact ckP_of (rep_katV hc (rep_ksub hc (rep_kSL hc _) (rep_kSL hc _))) h
  · rfl
  · exact ckP_of (rep_katV hc (rep_ksub hc (rep_kSL hc _) (rep_kSL hc _))) h

lemma capAOkK_imp {σ : Bool} {splits : List Split} {cap : SL} {a : CapA} (b0 b1 R : ℕ)
    (h : capAOkK c σ splits cap a = true) :
    capAOk (ckP c σ) σ c.Δ c.X c.Y b0 b1 R splits cap a = true := by
  cases a <;> first | exact h | exact ghOkK_imp hc b0 b1 R h

omit hc in
lemma totOkK_imp {σ : Bool} {b0 b1 R : ℕ} {splits : List Split} {pat : List Bool}
    {fcs : List FCert} {T : KR} (hT : RepK c T) (h : totOkK c σ b0 b1 R splits pat fcs T = true) :
    totOk (ckP c σ) σ c.Δ c.X c.Y b0 b1 R splits pat fcs T.r = true := by
  simp only [totOkK, totOk, Bool.or_eq_true] at h ⊢
  rcases h with h | h
  · exact Or.inl (ckP_of hT h)
  · exact Or.inr h

theorem vertOkK'_imp {D W : ℕ} {σ : Bool} {b0 b1 R : ℕ} {chs cvs : List SegE} {crs : List RectM}
    {hbx vbx : List (List ℕ × List ℕ)} {v : VCert}
    (h : vertOkK' c D W σ b0 b1 R chs cvs crs hbx vbx v = true) :
    vertOk (ckP c σ) D W σ c.Δ c.X c.Y b0 b1 R chs cvs crs hbx vbx v = true := by
  simp only [vertOkK', vertOk, Bool.and_eq_true, List.all_eq_true] at h ⊢
  obtain ⟨⟨⟨⟨⟨⟨⟨⟨⟨l1, l2⟩, l3⟩, l4⟩, l5⟩, l6⟩, hH⟩, hV⟩, hL⟩, hP⟩ := h
  refine ⟨⟨⟨⟨⟨⟨⟨⟨⟨l1, l2⟩, l3⟩, l4⟩, l5⟩, l6⟩, fun q hq x hx => segCOkK_imp hc _ _ _ (hH q hq x hx)⟩,
    fun q hq x hx => segCOkK_imp hc _ _ _ (hV q hq x hx)⟩,
    fun p hp => ⟨fun a ha => capAOkK_imp hc _ _ _ ((hL p hp).1 a ha),
      fun a ha => capAOkK_imp hc _ _ _ ((hL p hp).2 a ha)⟩⟩, fun pat hpat => ?_⟩
  obtain ⟨⟨⟨t1, t2⟩, t3⟩, hall⟩ := hP pat hpat
  refine ⟨⟨⟨t1, t2⟩, t3⟩, ?_⟩
  set LK := ((chs.zip hbx).zip v.hc).map (hAltsPK c D pat) ++ ((cvs.zip vbx).zip v.vc).map
    (vAltsPK c D pat) ++ (crs.zip v.lc).map (lAltsPK c D pat) with hLK
  have e : ((chs.zip hbx).zip v.hc).map (hAltsP c.Δ c.X c.Y D pat) ++ ((cvs.zip vbx).zip v.vc).map
      (vAltsP c.Δ c.X c.Y D pat) ++ (crs.zip v.lc).map (lAltsP c.Δ c.X c.Y D pat) =
      LK.map (List.map KR.r) := by
    simp only [hLK, List.map_append, List.map_map, Function.comp_def, hAltsPK_r, vAltsPK_r, lAltsPK_r]
  have hrepL : ∀ l ∈ reordK LK, ∀ a ∈ l, RepK c a := by
    intro l hl a ha
    have hl' : l ∈ LK := by
      simp only [reordK, List.mem_append, List.mem_filter] at hl
      rcases hl with ⟨h, _⟩ | ⟨h, _⟩ <;> exact h
    simp only [hLK, List.mem_append, List.mem_map] at hl'
    rcases hl' with (⟨q, _, rfl⟩ | ⟨q, _, rfl⟩) | ⟨q, _, rfl⟩
    · exact rep_hAltsPK hc _ _ _ a ha
    · exact rep_vAltsPK hc _ _ _ a ha
    · exact rep_lAltsPK hc _ _ _ a ha
  rw [e, reord_map, cprod_map]
  intro comb hcomb
  obtain ⟨combK, hK, rfl⟩ := List.mem_map.mp hcomb
  have hrep : RepK c (sumK c (combK ++ (v.splits.zip pat).map (fun x => sprocK c x.1 x.2) ++
      [kconst (-(W : ℤ)) 1])) := by
    refine rep_sumK hc _ fun x hx => ?_
    simp only [List.mem_append, List.mem_map, List.mem_singleton] at hx
    rcases hx with (hx | ⟨y, _, rfl⟩) | rfl
    · exact mem_cprod (P := RepK c) _ hrepL combK hK x hx
    · exact rep_sprocK hc _ _
    · exact rep_kconst _ _
  have := totOkK_imp hrep (hall combK hK)
  rw [sumK_r] at this
  simpa only [List.map_append, List.map_map, Function.comp_def, sprocK_r, List.map_cons,
    List.map_nil, kconst] using this

end imp

/-- **The Kronecker test is sound** at every vertex of the sub-bin. -/
lemma ckP_hck {Δ X Y : Poly} {b0 b1 R K : ℕ} {σ : Bool} {u δ : ℝ} (hR : 0 < R) (h : Ok δ u)
    (hσ : if σ then 0 < δ else δ < 0) (hb0 : (b0 : ℝ) / R ≤ u) (hb1 : u ≤ (b1 : ℝ) / R) :
    ∀ r : RF, ckP (mkCtx Δ X Y b0 b1 R K) σ r = true → r.d ≠ 0 → 0 ≤ r.eval δ u := by
  intro r hr hd
  unfold ckP at hr
  simp only [decide_eq_true_eq] at hr
  obtain ⟨kr, hk, rfl, hc⟩ := hr
  have hn := hcheck_sound' (U0 := b0) (U1 := b1) (K := K) hR (le_max_left _ _) (le_max_right _ _)
    hk hc hb0 hb1
  refine nonneg_of_snumP h hσ hd ?_
  cases hb : (σ || kr.r.e % 2 == 0) <;> simp_all

end LemmaEK

end SquarePacking
