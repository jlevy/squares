import Sqpack.LemmaEK
import Sqpack.RowMinK

/-!
# The vertex test without enumerating the combinations

`LemmaEK.vertOkK'` checks every combination of the segments' alternatives (one term per row) by
the Kronecker test of its sum.  Here all the terms are raised to one common denominator and degree
and the rows are replaced by their digit-wise minima (`KArith.rmLoop`): if those pass, every
combination's sum is `≥ 0` at every pose of the sub-bin (`rowOkM_sound`).  The cost is linear in
the number of terms.
-/

namespace SquarePacking

namespace LemmaEK

open BernZ RatU ChordE LemmaE LemmaEPoly LemmaEVert ZMTreeM KArith

/-! ## 1.  The common denominator and degree -/

def maxN (l : List ℕ) : ℕ := l.foldr max 0

def lcmN (l : List ℕ) : ℕ := l.foldr Nat.lcm 1

lemma le_maxN : ∀ {l : List ℕ} {a : ℕ}, a ∈ l → a ≤ maxN l
  | _ :: _, _, List.Mem.head _ => le_max_left _ _
  | _ :: _, _, List.Mem.tail _ h => (le_maxN h).trans (le_max_right _ _)

lemma dvd_lcmN : ∀ {l : List ℕ} {a : ℕ}, a ∈ l → a ∣ lcmN l
  | _ :: _, _, List.Mem.head _ => Nat.dvd_lcm_left _ _
  | _ :: l, _, List.Mem.tail _ h => (dvd_lcmN (l := l) h).trans (Nat.dvd_lcm_right _ _)

lemma lcmN_ne_zero : ∀ {l : List ℕ}, (∀ a ∈ l, a ≠ 0) → lcmN l ≠ 0
  | [], _ => one_ne_zero
  | a :: l, h => Nat.lcm_ne_zero (h a List.mem_cons_self)
      (lcmN_ne_zero fun x hx => h x (List.mem_cons_of_mem _ hx))

/-- A term raised to the denominator `Δᴱ Cᴵ Sᴶ Nᴷ L`. -/
def rzK (c : Ctx) (E I J Kx L : ℕ) (r : KR) : KR :=
  kraise c r (E - r.r.e) (I - r.r.i) (J - r.r.j) (Kx - r.r.k) (L / r.r.d)

/-- An image lifted to the degree `N`. -/
def liftH (B N : ℕ) (h : KH) : KH := hadd B h ⟨0, N, 0⟩

/-- **The test**: the rows' minima and the fixed terms, digit by digit, over the common
denominator and degree. -/
def rowOkM (c : Ctx) (σ : Bool) (rows : List (List KR)) (fx : List KR) : Bool :=
  let ts := rows.flatten ++ fx
  let E := maxN (ts.map (·.r.e))
  let I := maxN (ts.map (·.r.i))
  let J := maxN (ts.map (·.r.j))
  let Kx := maxN (ts.map (·.r.k))
  let L := lcmN (ts.map (·.r.d))
  let N := maxN (ts.map fun r => (rzK c E I J Kx L r).h.n)
  let ε : ℤ := if σ || E % 2 == 0 then 1 else -1
  decide (0 < c.K) &&
    ts.all (fun r => r.r.d != 0 &&
      decide (2 * (liftH c.B N (rzK c E I J Kx L r).h).b * c.M ^ N < 2 ^ c.K)) &&
    rmLoop c.K ε (N + 2) (rows.map (·.map fun r => (liftH c.B N (rzK c E I J Kx L r).h).v))
      (fx.map fun r => (liftH c.B N (rzK c E I J Kx L r).h).v)

/-! ## 2.  Soundness -/

lemma add_nil' : ∀ p : Poly, add p [] = p
  | [] => rfl
  | _ :: _ => rfl

lemma rep_liftH {A : ℤ} {B N : ℕ} (hB : 0 < B) {p : Poly} {h : KH} (hp : RepH A B p h) :
    RepH A B p (liftH B N h) := by
  have h0 : RepH A B [] ⟨0, N, 0⟩ := ⟨by simp, by simp, by simp⟩
  have := rep_hadd hB hp h0
  rwa [add_nil'] at this

lemma liftH_n (B N : ℕ) {h : KH} (hn : h.n ≤ N) : (liftH B N h).n = N := by
  have e : (⟨0, N, 0⟩ : KH).n = N := rfl
  unfold liftH hadd
  split_ifs with e1 e2 <;> simp only [e] at * <;> omega

lemma sum_div_list {α : Type*} (l : List α) (f : α → ℝ) (d : ℝ) :
    (l.map f).sum / d = (l.map fun x => f x / d).sum := by
  induction l with
  | nil => simp
  | cons a l ih => simp [add_div, ih]

lemma rzK_r (c : Ctx) (E I J Kx L : ℕ) (r : KR) :
    (rzK c E I J Kx L r).r = raise c.Δ r.r (E - r.r.e) (I - r.r.i) (J - r.r.j) (Kx - r.r.k) (L / r.r.d) := rfl

lemma mem_flatten_of_forall₂ {α : Type*} :
    ∀ {comb : List α} {rows : List (List α)}, List.Forall₂ (fun a l => a ∈ l) comb rows →
      ∀ x ∈ comb, x ∈ rows.flatten
  | [], [], _, x, hx => absurd hx List.not_mem_nil
  | a :: comb, r :: rows, List.Forall₂.cons ha h, x, hx => by
    rcases List.mem_cons.mp hx with rfl | hx
    · exact List.mem_flatten.mpr ⟨r, List.mem_cons_self, ha⟩
    · obtain ⟨l, hl, hxl⟩ := List.mem_flatten.mp (mem_flatten_of_forall₂ h x hx)
      exact List.mem_flatten.mpr ⟨l, List.mem_cons_of_mem _ hl, hxl⟩

lemma forall₂_map {α β : Type*} (f : α → β) :
    ∀ {comb : List α} {rows : List (List α)}, List.Forall₂ (fun a l => a ∈ l) comb rows →
      List.Forall₂ (fun a l => a ∈ l) (comb.map f) (rows.map (·.map f))
  | [], [], _ => List.Forall₂.nil
  | _ :: _, _ :: _, List.Forall₂.cons ha h => List.Forall₂.cons (List.mem_map_of_mem ha) (forall₂_map f h)

/-- **Every combination is `≥ 0`** at every pose of the sub-bin. -/
theorem rowOkM_sound {Δ X Y : Poly} {b0 b1 R K : ℕ} (hR : 0 < R) {σ : Bool}
    {rows : List (List KR)} {fx : List KR}
    (h : rowOkM (mkCtx Δ X Y b0 b1 R K) σ rows fx = true)
    (hrep : ∀ r ∈ rows.flatten ++ fx, RepK (mkCtx Δ X Y b0 b1 R K) r)
    {u δ : ℝ} (hok : Ok δ u) (hΔ : eval Δ u = δ) (hσ : if σ then 0 < δ else δ < 0)
    (hu0 : (b0 : ℝ) / R ≤ u) (hu1 : u ≤ (b1 : ℝ) / R)
    {comb : List KR} (hcomb : comb ∈ cprod rows) :
    0 ≤ (sumRF Δ ((comb ++ fx).map KR.r)).eval δ u := by
  set c := mkCtx Δ X Y b0 b1 R K with hcdef
  have hc : CtxOk c := mkCtx_ok hR
  set ts := rows.flatten ++ fx with hts
  set E := maxN (ts.map (·.r.e)) with hE
  set I := maxN (ts.map (·.r.i)) with hI
  set J := maxN (ts.map (·.r.j)) with hJ
  set Kx := maxN (ts.map (·.r.k)) with hKx
  set L := lcmN (ts.map (·.r.d)) with hL
  set N := maxN (ts.map fun r => (rzK c E I J Kx L r).h.n) with hN
  set ε : ℤ := if σ || E % 2 == 0 then 1 else -1 with hε
  simp only [rowOkM, ← hts, ← hE, ← hI, ← hJ, ← hKx, ← hL, ← hN, ← hε, Bool.and_eq_true,
    decide_eq_true_eq, List.all_eq_true, bne_iff_ne, ne_eq] at h
  obtain ⟨⟨hK, hall⟩, hloop⟩ := h
  have hf2 := (mem_cprod_iff rows comb).mp hcomb
  set S := comb ++ fx with hS
  have hSts : ∀ x ∈ S, x ∈ ts := by
    intro x hx
    rcases List.mem_append.mp hx with hx | hx
    · exact List.mem_append_left _ (mem_flatten_of_forall₂ hf2 x hx)
    · exact List.mem_append_right _ hx
  have hd : ∀ x ∈ ts, x.r.d ≠ 0 := fun x hx => (hall x hx).1
  have hL0 : L ≠ 0 := lcmN_ne_zero fun a ha => by
    obtain ⟨x, hx, rfl⟩ := List.mem_map.mp ha; exact hd x hx
  -- the raised terms: the same value, the common denominator
  have hm : ∀ x ∈ ts, L / x.r.d ≠ 0 := fun x hx =>
    (Nat.div_pos (Nat.le_of_dvd (Nat.pos_of_ne_zero hL0) (dvd_lcmN (List.mem_map_of_mem hx)))
      (Nat.pos_of_ne_zero (hd x hx))).ne'
  have hval : ∀ x ∈ ts, x.r.eval δ u = (rzK c E I J Kx L x).r.eval δ u := fun x hx => by
    rw [rzK_r]; exact (eval_raise hok hΔ (hd x hx) (hm x hx)).symm
  set D0 : RF := ⟨[], E, I, J, Kx, L⟩
  have hden : ∀ x ∈ ts, den (rzK c E I J Kx L x).r δ u = den D0 δ u := fun x hx => by
    have e1 : x.r.e + (E - x.r.e) = E := by have := le_maxN (List.mem_map_of_mem (f := (·.r.e)) hx); omega
    have e2 : x.r.i + (I - x.r.i) = I := by have := le_maxN (List.mem_map_of_mem (f := (·.r.i)) hx); omega
    have e3 : x.r.j + (J - x.r.j) = J := by have := le_maxN (List.mem_map_of_mem (f := (·.r.j)) hx); omega
    have e4 : x.r.k + (Kx - x.r.k) = Kx := by have := le_maxN (List.mem_map_of_mem (f := (·.r.k)) hx); omega
    have e5 : x.r.d * (L / x.r.d) = L := Nat.mul_div_cancel' (dvd_lcmN (List.mem_map_of_mem hx))
    simp only [rzK_r, raise, den, e1, e2, e3, e4, e5, D0]
  -- the sum over the common denominator
  set Ssum : RF := ⟨sumP (S.map fun x => (rzK c E I J Kx L x).r.num), E, I, J, Kx, L⟩
  have hsum : (sumRF Δ (S.map KR.r)).eval δ u = Ssum.eval δ u := by
    rw [eval_sumRF hok hΔ _ (fun r hr => by
      obtain ⟨x, hx, rfl⟩ := List.mem_map.mp hr; exact hd x (hSts x hx))]
    simp only [RF.eval, Ssum, eval_sumP, List.map_map, Function.comp_def]
    have : den ⟨sumP (S.map fun x => (rzK c E I J Kx L x).r.num), E, I, J, Kx, L⟩ δ u = den D0 δ u := rfl
    rw [this, sum_div_list]
    refine congrArg List.sum (List.map_congr_left fun x hx => ?_)
    have e := hval x (hSts x hx)
    simp only [RF.eval] at e
    rw [e, hden x (hSts x hx)]
  rw [hsum]
  refine nonneg_of_snumP hok hσ hL0 ?_
  -- the numerator's sign from the digits
  have hsel : eval (if σ || Ssum.e % 2 == 0 then Ssum.num else smul (-1) Ssum.num) u =
      ε * (S.map fun x => eval (rzK c E I J Kx L x).r.num u).sum := by
    simp only [Ssum, hε]
    split_ifs <;> simp [BernZ.eval_smul, eval_sumP, List.map_map, Function.comp_def]
  rw [hsel]
  have hM1 : b0 + b1 ≤ c.M := le_max_left _ _
  have hM2 : 2 * R ≤ c.M := le_max_right _ _
  have := nonneg_of_digits (U0 := b0) (U1 := b1) (R := R) (K := K) (M := c.M) (N := N) hK hR hM1 hM2
    (ε := ε) (S.map fun x => ((rzK c E I J Kx L x).r.num, liftH c.B N (rzK c E I J Kx L x).h))
    (fun y hy => by
      obtain ⟨x, hx, rfl⟩ := List.mem_map.mp hy
      exact rep_liftH hc.hB (rep_kraise hc (hrep x (hSts x hx)) _ _ _ _ _))
    (fun y hy => by
      obtain ⟨x, hx, rfl⟩ := List.mem_map.mp hy
      exact liftH_n _ _ (le_maxN (List.mem_map_of_mem (f := fun r => (rzK c E I J Kx L r).h.n) (hSts x hx))))
    (fun y hy => by
      obtain ⟨x, hx, rfl⟩ := List.mem_map.mp hy
      exact (hall x (hSts x hx)).2)
    (fun i hi => by
      have := rmLoop_sound (N + 2) _ _ _ hloop
        (forall₂_map (fun r => (liftH c.B N (rzK c E I J Kx L r).h).v) hf2) i hi
      have hcK : c.K = K := rfl
      simpa [List.map_append, List.map_map, Function.comp_def, hS, hcK] using this)
    hu0 hu1
  simpa [List.map_map, Function.comp_def] using this

/-! ## 3.  The vertex test -/

/-- `vertOkK'` with the rows' minima in place of the combinations (the combinations remain as the
fallback, for the certificates with common-factor parts). -/
def vertOkM (c : Ctx) (D W : ℕ) (σ : Bool) (b0 b1 R : ℕ) (chs cvs : List SegE)
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
      (rowOkM c σ (reordK (((chs.zip hbx).zip v.hc).map (hAltsPK c D pat) ++
          ((cvs.zip vbx).zip v.vc).map (vAltsPK c D pat) ++ (crs.zip v.lc).map (lAltsPK c D pat)))
          ((v.splits.zip pat).map (fun x => sprocK c x.1 x.2) ++ [kconst (-(W : ℤ)) 1]) ||
        (cprod (reordK (((chs.zip hbx).zip v.hc).map (hAltsPK c D pat) ++
          ((cvs.zip vbx).zip v.vc).map (vAltsPK c D pat) ++
          (crs.zip v.lc).map (lAltsPK c D pat)))).all fun comb =>
        totOkK c σ b0 b1 R v.splits pat v.fcs (sumK c (comb ++
          (v.splits.zip pat).map (fun x => sprocK c x.1 x.2) ++ [kconst (-(W : ℤ)) 1])))

open Classical in
/-- The checker at one pose: the Kronecker test, or `r ≥ 0` there. -/
noncomputable def ckU (c : Ctx) (σ : Bool) (δ u : ℝ) (r : RF) : Bool :=
  ckP c σ r || decide (r.d ≠ 0 → 0 ≤ r.eval δ u)

lemma ckU_of_ckP {c : Ctx} {σ : Bool} {δ u : ℝ} {r : RF} (h : ckP c σ r = true) :
    ckU c σ δ u r = true := by simp [ckU, h]

/-- The checker `ckU` is sound at its pose. -/
lemma ckU_hck {Δ X Y : Poly} {b0 b1 R K : ℕ} {σ : Bool} {u δ : ℝ} (hR : 0 < R) (h : Ok δ u)
    (hσ : if σ then 0 < δ else δ < 0) (hb0 : (b0 : ℝ) / R ≤ u) (hb1 : u ≤ (b1 : ℝ) / R) :
    ∀ r : RF, ckU (mkCtx Δ X Y b0 b1 R K) σ δ u r = true → r.d ≠ 0 → 0 ≤ r.eval δ u := by
  intro r hr hd
  simp only [ckU, Bool.or_eq_true, decide_eq_true_eq] at hr
  rcases hr with hr | hr
  · exact ckP_hck hR h hσ hb0 hb1 r hr hd
  · exact hr hd

section mono

variable {ck1 ck2 : RF → Bool} (hm : ∀ r, ck1 r = true → ck2 r = true)
include hm

lemma ghOk_mono {σ : Bool} {Δ X Y : Poly} {b0 b1 R : ℕ} {cap : SL} {mode : ℕ}
    (h : ghOk ck1 σ Δ X Y b0 b1 R cap mode = true) : ghOk ck2 σ Δ X Y b0 b1 R cap mode = true := by
  unfold ghOk at h ⊢
  split_ifs at h ⊢
  · exact hm _ h
  · rfl
  · exact hm _ h

lemma segOkA_mono {σ : Bool} {Δ X Y : Poly} {b0 b1 R : ℕ} {ups los : List SL} {Ua La : List ℕ}
    (h : segOkA ck1 σ Δ X Y b0 b1 R ups los Ua La = true) :
    segOkA ck2 σ Δ X Y b0 b1 R ups los Ua La = true := by
  simp only [segOkA, Bool.and_eq_true, List.all_eq_true, List.any_eq_true] at h ⊢
  obtain ⟨⟨h1, h2⟩, h3⟩ := h
  refine ⟨⟨h1, fun U hU => ?_⟩, fun L hL => ?_⟩
  · obtain ⟨a, ha, hk⟩ := h2 U hU; exact ⟨a, ha, hm _ hk⟩
  · obtain ⟨b, hb, hk⟩ := h3 L hL; exact ⟨b, hb, hm _ hk⟩

lemma segCOk_mono {σ : Bool} {Δ X Y : Poly} {b0 b1 R : ℕ} {ups los : List SL}
    {bx : List ℕ × List ℕ} {sc : SegC} (h : segCOk ck1 σ Δ X Y b0 b1 R ups los bx sc = true) :
    segCOk ck2 σ Δ X Y b0 b1 R ups los bx sc = true := by
  cases sc with
  | drop => rfl
  | box => exact h
  | alt Ua La => exact segOkA_mono (σ := σ) (b0 := b0) (b1 := b1) (R := R) hm h

lemma capAOk_mono {σ : Bool} {Δ X Y : Poly} {b0 b1 R : ℕ} {splits : List Split} {cap : SL}
    {a : CapA} (h : capAOk ck1 σ Δ X Y b0 b1 R splits cap a = true) :
    capAOk ck2 σ Δ X Y b0 b1 R splits cap a = true := by
  cases a <;> first | exact h | exact ghOk_mono (σ := σ) (b0 := b0) (b1 := b1) (R := R) hm h

lemma totOk_mono {σ : Bool} {Δ X Y : Poly} {b0 b1 R : ℕ} {splits : List Split} {pat : List Bool}
    {fcs : List FCert} {T : RF} (h : totOk ck1 σ Δ X Y b0 b1 R splits pat fcs T = true) :
    totOk ck2 σ Δ X Y b0 b1 R splits pat fcs T = true := by
  simp only [totOk, Bool.or_eq_true] at h ⊢
  rcases h with h | h
  · exact Or.inl (hm _ h)
  · exact Or.inr h

end mono

/-- **The test without the combinations implies the list test** with the checker `ckU` of the
pose. -/
theorem vertOkM_imp {Δ X Y : Poly} {b0 b1 R K : ℕ} (hR : 0 < R) {D W : ℕ} {σ : Bool}
    {chs cvs : List SegE} {crs : List RectM} {hbx vbx : List (List ℕ × List ℕ)} {v : VCert}
    {u δ : ℝ} (hok : Ok δ u) (hΔ : eval Δ u = δ) (hσ : if σ then 0 < δ else δ < 0)
    (hu0 : (b0 : ℝ) / R ≤ u) (hu1 : u ≤ (b1 : ℝ) / R)
    (h : vertOkM (mkCtx Δ X Y b0 b1 R K) D W σ b0 b1 R chs cvs crs hbx vbx v = true) :
    vertOk (ckU (mkCtx Δ X Y b0 b1 R K) σ δ u) D W σ Δ X Y b0 b1 R chs cvs crs hbx vbx v = true := by
  set c := mkCtx Δ X Y b0 b1 R K with hcdef
  have hc : CtxOk c := mkCtx_ok hR
  have hm : ∀ r, ckP c σ r = true → ckU c σ δ u r = true := fun r h => ckU_of_ckP h
  have hcΔ : c.Δ = Δ := rfl
  have hcX : c.X = X := rfl
  have hcY : c.Y = Y := rfl
  simp only [vertOkM, vertOk, Bool.and_eq_true, Bool.or_eq_true, List.all_eq_true] at h ⊢
  obtain ⟨⟨⟨⟨⟨⟨⟨⟨⟨l1, l2⟩, l3⟩, l4⟩, l5⟩, l6⟩, hH⟩, hV⟩, hL⟩, hP⟩ := h
  refine ⟨⟨⟨⟨⟨⟨⟨⟨⟨l1, l2⟩, l3⟩, l4⟩, l5⟩, l6⟩,
    fun q hq x hx => segCOk_mono hm (segCOkK_imp hc _ _ _ (hH q hq x hx))⟩,
    fun q hq x hx => segCOk_mono hm (segCOkK_imp hc _ _ _ (hV q hq x hx))⟩,
    fun p hp => ⟨fun a ha => capAOk_mono hm (capAOkK_imp hc _ _ _ ((hL p hp).1 a ha)),
      fun a ha => capAOk_mono hm (capAOkK_imp hc _ _ _ ((hL p hp).2 a ha))⟩⟩, fun pat hpat => ?_⟩
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
  set FK := (v.splits.zip pat).map (fun x => sprocK c x.1 x.2) ++ [kconst (-(W : ℤ)) 1] with hFK
  have hrepF : ∀ x ∈ FK, RepK c x := by
    intro x hx
    simp only [hFK, List.mem_append, List.mem_map, List.mem_singleton] at hx
    rcases hx with ⟨y, _, rfl⟩ | rfl
    · exact rep_sprocK hc _ _
    · exact rep_kconst _ _
  rw [← hcΔ, ← hcX, ← hcY, e, reord_map, cprod_map]
  intro comb hcomb
  obtain ⟨combK, hK, rfl⟩ := List.mem_map.mp hcomb
  have hsum : combK.map KR.r ++ (v.splits.zip pat).map (fun x => sproc c.Δ c.X c.Y x.1 x.2) ++
      [RF.const (-(W : ℤ)) 1] = (combK ++ FK).map KR.r := by
    simp only [hFK, List.map_append, List.map_map, Function.comp_def, sprocK_r, List.map_cons,
      List.map_nil, kconst, List.append_assoc]
  rcases hall with hrow | hcombs
  · -- the rows' minima
    have hrep : ∀ r ∈ (reordK LK).flatten ++ FK, RepK c r := by
      intro r hr
      rcases List.mem_append.mp hr with hr | hr
      · obtain ⟨l, hl, hrl⟩ := List.mem_flatten.mp hr; exact hrepL l hl r hrl
      · exact hrepF r hr
    have h0 := rowOkM_sound hR hrow hrep hok hΔ hσ hu0 hu1 hK
    simp only [totOk, Bool.or_eq_true]
    left
    rw [hsum]
    simp only [ckU, Bool.or_eq_true, decide_eq_true_eq]
    exact Or.inr fun _ => h0
  · -- the combinations
    have hrep : RepK c (sumK c (combK ++ (v.splits.zip pat).map (fun x => sprocK c x.1 x.2) ++
        [kconst (-(W : ℤ)) 1])) := by
      refine rep_sumK hc _ fun x hx => ?_
      simp only [List.mem_append, List.mem_map, List.mem_singleton] at hx
      rcases hx with (hx | ⟨y, _, rfl⟩) | rfl
      · exact mem_cprod (P := RepK c) _ hrepL combK hK x hx
      · exact rep_sprocK hc _ _
      · exact rep_kconst _ _
    have := totOkK_imp hrep (hcombs combK hK)
    rw [sumK_r] at this
    refine totOk_mono hm ?_
    simpa only [List.map_append, List.map_map, Function.comp_def, sprocK_r, List.map_cons,
      List.map_nil, kconst] using this

end LemmaEK

end SquarePacking
