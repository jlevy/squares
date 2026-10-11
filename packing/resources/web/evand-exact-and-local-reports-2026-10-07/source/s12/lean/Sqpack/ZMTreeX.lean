import Sqpack.LBlockSound

/-!
# The mixed zero-margin tree (`ZTM`): points, S-blocks, T-groups and L-blocks

The tree of the mixed verifier.  A `Z` leaf carries a `ZMTree` point leaf and a piece certificate of
three kinds of blocks (`ZMTreeM.lean`: S-blocks = Lemma S, T-groups = Lemma T; `LBlock.lean`:
L-blocks = Lemma L + Corollary L); the kernel computes the certificate's value `Lp` and runs
`ZMTree.zOk` with the target `W − Lp` (Lemma P).  Tags of the claimed segments: `2s` for S-block `s`,
`2g + 1` for T-group `g < nT`, `2(nT + i) + 1` for L-block `i`.

`soundM`: `checkM` accepts ⇒ `CovM` of the box, for every tree.  `decM`: the digit decoder.
-/

namespace SquarePacking

namespace ZMTreeM

open BoxTree ZMTree

/-! ## 1.  L-blocks in the piece certificate -/

def lblksOk (S Q R x0 x1 y0 y1 U0 U1 : ℕ) (cls : List (SegE × ℕ)) : ℕ → List LBlk → Bool
  | _, [] => true
  | li, B :: bs => lblkOk S Q R x0 x1 y0 y1 U0 U1 cls (Nat.add (Nat.mul 2 li) 1) B &&
      lblksOk S Q R x0 x1 y0 y1 U0 U1 cls (li + 1) bs

def lblksVal (S Q : ℕ) (cls : List (SegE × ℕ)) (lb : List LBlk) : ℕ :=
  (lb.map (lblkVal S Q cls)).sum

lemma lblks_parts {D S R x0 x1 y0 y1 U0 U1 : ℕ} (hD : 0 < D) (hS : 0 < S) (hR : 0 < R)
    {c : ℝ × ℝ} {u : ℝ} (P : Pose S (D * S) R x0 x1 y0 y1 U0 U1 c u) {cls : List (SegE × ℕ)}
    (hnd : (cls.map Prod.fst).Nodup) :
    ∀ (lb : List LBlk) (li : ℕ), lblksOk S (D * S) R x0 x1 y0 y1 U0 U1 cls li lb = true →
      ∃ L : List (SegE × ℝ × ℝ),
        (∀ x ∈ L, PartOK D (sq c (2 * Real.arctan u) 1) x ∧ ∃ j, li ≤ j ∧ (x.1, 2 * j + 1) ∈ cls) ∧
        L.Pairwise PRel ∧ (lblksVal S (D * S) cls lb : ℝ) ≤ (L.map (pval D)).sum
  | [], _, _ => ⟨[], by simp, List.Pairwise.nil, by simp [lblksVal]⟩
  | B :: bs, li, h => by
    simp only [lblksOk, Bool.and_eq_true] at h
    obtain ⟨hB, hbs⟩ := h
    obtain ⟨LB, hB1, hB2, hB3⟩ := lblk_sound hD hS hR P (Nat.succ_pos _) hB
    obtain ⟨L', h1, h2, h3⟩ := lblks_parts hD hS hR P hnd bs (li + 1) hbs
    refine ⟨LB ++ L', ?_, ?_, ?_⟩
    · intro x hx
      rcases List.mem_append.mp hx with hx | hx
      · obtain ⟨a1, a2⟩ := hB1 x hx
        exact ⟨a1, li, le_rfl, by simpa [nat_add_eq, nat_mul_eq] using a2⟩
      · obtain ⟨a1, j, hj, a2⟩ := h1 x hx
        exact ⟨a1, j, by omega, a2⟩
    · rw [List.pairwise_append]
      refine ⟨hB2, h2, fun x hx y hy hxy => ?_⟩
      obtain ⟨_, a2⟩ := hB1 x hx
      obtain ⟨_, j, hj, b2⟩ := h1 y hy
      rw [hxy] at a2
      have := tag_unique hnd a2 b2
      simp only [nat_add_eq, nat_mul_eq] at this
      omega
    · simp only [lblksVal, List.map_cons, List.sum_cons, List.map_append, List.sum_append] at h3 ⊢
      rw [Nat.cast_add]
      linarith

/-- **The full piece certificate**: S-blocks, T-groups, L-blocks. -/
def pcOkX (S Q R x0 x1 y0 y1 U0 U1 : ℕ) (cls : List (SegE × ℕ)) (sb : List SBlk)
    (tg : List TGrp) (lb : List LBlk) : Bool :=
  pcOk S Q R x0 x1 y0 y1 U0 U1 cls sb tg && lblksOk S Q R x0 x1 y0 y1 U0 U1 cls tg.length lb

def pcValX (S Q : ℕ) (cls : List (SegE × ℕ)) (sb : List SBlk) (tg : List TGrp) (lb : List LBlk) : ℕ :=
  pcVal S cls sb tg + lblksVal S Q cls lb

/-- **Soundness of the full piece certificate.** -/
theorem pc_soundX {D S R x0 x1 y0 y1 U0 U1 : ℕ} (hD : 0 < D) (hS : 0 < S) (hR : 0 < R)
    {segs : List SegE} {c : ℝ × ℝ} {u : ℝ} (P : Pose S (D * S) R x0 x1 y0 y1 U0 U1 c u)
    {cls : List (SegE × ℕ)} {sb : List SBlk} {tg : List TGrp} {lb : List LBlk}
    (hcls : (cls.map Prod.fst).Sublist segs) (hsnd : segs.Nodup)
    (h : pcOkX S (D * S) R x0 x1 y0 y1 U0 U1 cls sb tg lb = true) :
    (pcValX S (D * S) cls sb tg lb : ℝ) ≤ segMass D segs (sq c (2 * Real.arctan u) 1) := by
  simp only [pcOkX, pcOk, Bool.and_eq_true] at h
  obtain ⟨⟨⟨hsb, hsc⟩, htg⟩, hlb⟩ := h
  have hnd : (cls.map Prod.fst).Nodup := hcls.nodup hsnd
  obtain ⟨hS1, hS2⟩ := sparts hD hS rfl hR P hsb cls hsc
  obtain ⟨LT, hT1, hT2, hT3⟩ := groups_parts hD hS rfl hR P hnd tg 0 htg
  obtain ⟨LL, hL1, hL2, hL3⟩ := lblks_parts hD hS hR P hnd lb tg.length hlb
  set LS := (cls.filter fun ec => Nat.mod ec.2 2 = 0).map (sPart S (D * S) sb) with hLS
  have hmemcls : ∀ {e : SegE} {t : ℕ}, (e, t) ∈ cls → e ∈ segs.toFinset := by
    intro e t h
    rw [List.mem_toFinset]
    exact hcls.subset (List.mem_map_of_mem (f := Prod.fst) h)
  have hSnd : (LS.map Prod.fst).Nodup := by
    rw [hLS, List.map_map]
    have : (Prod.fst ∘ sPart S (D * S) sb) = (Prod.fst : SegE × ℕ → SegE) := by
      funext ec; exact sPart_fst S (D * S) sb ec
    rw [this]
    exact hnd.sublist (List.filter_sublist.map _)
  have key := parts_le_segMass hD segs (sq c (2 * Real.arctan u) 1) (LS ++ LT ++ LL) ?_ ?_ ?_
  · simp only [pcValX, pcVal, List.map_append, List.sum_append] at key ⊢
    rw [Nat.cast_add, Nat.cast_add]
    linarith
  · intro x hx
    simp only [List.mem_append] at hx
    rcases hx with (hx | hx) | hx
    · obtain ⟨_, t, _, hm⟩ := hS1 x hx; exact hmemcls hm
    · obtain ⟨_, j, _, _, hm⟩ := hT1 x hx; exact hmemcls hm
    · obtain ⟨_, j, _, hm⟩ := hL1 x hx; exact hmemcls hm
  · intro x hx
    simp only [List.mem_append] at hx
    rcases hx with (hx | hx) | hx
    · exact (hS1 x hx).1
    · exact (hT1 x hx).1
    · exact (hL1 x hx).1
  · rw [List.pairwise_append, List.pairwise_append]
    refine ⟨⟨?_, hT2, fun x hx y hy hxy => ?_⟩, hL2, fun x hx y hy hxy => ?_⟩
    · have := List.nodup_iff_pairwise_ne.mp hSnd
      rw [List.pairwise_map] at this
      exact this.imp fun h e => absurd e h
    · obtain ⟨_, t, ht, hm⟩ := hS1 x hx
      obtain ⟨_, j, _, _, hm'⟩ := hT1 y hy
      rw [hxy] at hm
      have := tag_unique hnd hm hm'
      have ht' : t % 2 = 0 := ht
      omega
    · obtain ⟨_, j, _, hm'⟩ := hL1 y hy
      rcases List.mem_append.mp hx with hx | hx
      · obtain ⟨_, t, ht, hm⟩ := hS1 x hx
        rw [hxy] at hm
        have := tag_unique hnd hm hm'
        have ht' : t % 2 = 0 := ht
        omega
      · obtain ⟨_, i, _, hi, hm⟩ := hT1 x hx
        rw [hxy] at hm
        have := tag_unique hnd hm hm'
        omega

/-! ## 2.  The mixed tree -/

/-- Segment candidate pruning: keep the segments whose bounding box (over `Q`) meets the box
widened by `F`.  A pure speed device (any sublist is sound). -/
def nearS (S F x0 x1 y0 y1 : ℕ) (c : List SegE) : List SegE :=
  c.filter fun e => Nat.ble x0 (Nat.add (Nat.mul e.2.2.1 S) F) && Nat.ble (Nat.mul e.1 S) (Nat.add x1 F) &&
    Nat.ble y0 (Nat.add (Nat.mul e.2.2.2.1 S) F) && Nat.ble (Nat.mul e.2.1 S) (Nat.add y1 F)

/-- A zero-margin pose-space tree for mixed covers: the leaves of `ZMTree.ZT` with a piece
certificate added to `Z`, and `G` (segment candidate pruning). -/
inductive ZTM
  | Z (cl : List (ℕ × Tag)) (chA chB : List Piv) (emp : List (ℕ × ℕ)) (sc : List (ℕ × ℕ))
      (sb : List SBlk) (tg : List TGrp) (lb : List LBlk)
  | E
  | C (us : ℕ) (t : ZTM)
  | X (l r : ZTM)
  | Y (l r : ZTM)
  | U (l r : ZTM)
  | F (t : ZTM)
  | G (t : ZTM)
  | XM (m : ℕ) (l r : ZTM)
  | YM (m : ℕ) (l r : ZTM)
  | UM (m : ℕ) (l r : ZTM)

/-- **The mixed tree check** on the box `[x0,x1]×[y0,y1]×[u0,u1]` with point candidates `c` and
segment candidates `s`.  A `Z` leaf: the piece certificate holds, and `ZMTree.zOk` holds for the
target `W − Lp` (Lemma P). -/
def checkM (W S Q R F : ℕ) : ZTM → ℕ → ℕ → ℕ → ℕ → ℕ → ℕ → List Ent → List SegE → Bool
  | .Z cl chA chB emp sc sb tg lb, x0, x1, y0, y1, u0, u1, c, s =>
    Nat.ble u1 R && Nat.ble u0 u1 && pcOkX S Q R x0 x1 y0 y1 u0 u1 (sclaim sc s) sb tg lb &&
      zOk (Nat.sub W (pcValX S Q (sclaim sc s) sb tg lb)) S Q R x0 x1 y0 y1 u0 u1 (claim cl c) chA chB emp
  | .E, _, x1, _, y1, u0, u1, _, _ => Nat.ble u1 R && eOk Q R x1 y1 u0 u1
  | .C us t, x0, x1, y0, y1, u0, u1, c, s =>
    clipOk Q R x1 y1 u0 u1 us && checkM W S Q R F t x0 x1 y0 y1 u0 us c s
  | .F t, x0, x1, y0, y1, u0, u1, c, s =>
    checkM W S Q R F t x0 x1 y0 y1 u0 u1 (near S F x0 x1 y0 y1 c) s
  | .G t, x0, x1, y0, y1, u0, u1, c, s =>
    checkM W S Q R F t x0 x1 y0 y1 u0 u1 c (nearS S F x0 x1 y0 y1 s)
  | .X l r, x0, x1, y0, y1, u0, u1, c, s =>
    checkM W S Q R F l x0 (Nat.div (Nat.add x0 x1) 2) y0 y1 u0 u1 c s &&
    checkM W S Q R F r (Nat.div (Nat.add x0 x1) 2) x1 y0 y1 u0 u1 c s
  | .Y l r, x0, x1, y0, y1, u0, u1, c, s =>
    checkM W S Q R F l x0 x1 y0 (Nat.div (Nat.add y0 y1) 2) u0 u1 c s &&
    checkM W S Q R F r x0 x1 (Nat.div (Nat.add y0 y1) 2) y1 u0 u1 c s
  | .U l r, x0, x1, y0, y1, u0, u1, c, s =>
    checkM W S Q R F l x0 x1 y0 y1 u0 (Nat.div (Nat.add u0 u1) 2) c s &&
    checkM W S Q R F r x0 x1 y0 y1 (Nat.div (Nat.add u0 u1) 2) u1 c s
  | .XM m l r, x0, x1, y0, y1, u0, u1, c, s =>
    checkM W S Q R F l x0 m y0 y1 u0 u1 c s && checkM W S Q R F r m x1 y0 y1 u0 u1 c s
  | .YM m l r, x0, x1, y0, y1, u0, u1, c, s =>
    checkM W S Q R F l x0 x1 y0 m u0 u1 c s && checkM W S Q R F r x0 x1 m y1 u0 u1 c s
  | .UM m l r, x0, x1, y0, y1, u0, u1, c, s =>
    checkM W S Q R F l x0 x1 y0 y1 u0 m c s && checkM W S Q R F r x0 x1 y0 y1 m u1 c s

section soundM

variable {D S Mq R W : ℕ} {pts : List Ent} {segs : List SegE}

/-- `clip_bin` for mixed covers (the proof of `ZMTree.C_cov`, for `CovM`). -/
theorem CM_cov (hD : 0 < D) (hS : 0 < S) (hR : 0 < R) {x0 x1 y0 y1 U0 U1 us : ℕ}
    (h : clipOk (D * S) R x1 y1 U0 U1 us = true)
    (hc : CovM D S Mq R W pts segs x0 x1 y0 y1 U0 us) : CovM D S Mq R W pts segs x0 x1 y0 y1 U0 U1 := by
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

/-- **Soundness of a mixed `Z` leaf** (Lemma P + the piece certificate + `ZMTree.Z_cov`). -/
theorem ZM_cov (hD : 0 < D) (hS : 0 < S) (hR : 0 < R) (hnd : pts.Nodup) (hsnd : segs.Nodup)
    {x0 x1 y0 y1 U0 U1 : ℕ} {cl : List (Ent × Tag)} {chA chB : List Piv} {emp : List (ℕ × ℕ)}
    {cls : List (SegE × ℕ)} {sb : List SBlk} {tg : List TGrp} {lb : List LBlk}
    (hcl : (cl.map Prod.fst).Sublist pts) (hcls : (cls.map Prod.fst).Sublist segs)
    (hU01 : U0 ≤ U1) (hU1 : U1 ≤ R)
    (hpc : pcOkX S (D * S) R x0 x1 y0 y1 U0 U1 cls sb tg lb = true)
    (hz : zOk (Nat.sub W (pcValX S (D * S) cls sb tg lb)) S (D * S) R x0 x1 y0 y1 U0 U1 cl chA chB emp
      = true) :
    CovM D S Mq R W pts segs x0 x1 y0 y1 U0 U1 := by
  have hcov := Z_cov (Mq := Mq) hD hS hR hnd hcl hU01 hU1 hz
  intro cc u hx0 hx1 hy0 hy1 hu0 hu1 hsub
  have hp := hcov cc u hx0 hx1 hy0 hy1 hu0 hu1 hsub
  have hQc : ((D : ℝ) * S) = ((D * S : ℕ) : ℝ) := by push_cast; ring
  rw [hQc] at hx0 hx1 hy0 hy1
  obtain ⟨wx, wy⟩ := adm_lo hsub
  have P : Pose S (D * S) R x0 x1 y0 y1 U0 U1 cc u :=
    ⟨hx0, hx1, hy0, hy1, hu0, hu1, wx, wy, hU01, hU1⟩
  have hs := pc_soundX hD hS hR P hcls hsnd hpc
  set Lp := pcValX S (D * S) cls sb tg lb
  have hW : (W : ℝ) ≤ ((Nat.sub W Lp : ℕ) : ℝ) + Lp := by
    rcases le_total Lp W with h | h
    · rw [nat_sub_eq, Nat.cast_sub h]; linarith
    · rw [nat_sub_eq, Nat.sub_eq_zero_of_le h]; push_cast; rw [zero_add]; exact_mod_cast h
  unfold ptMass
  linarith

/-- **Soundness of the mixed tree check.** -/
theorem soundM (D S Mq R W F : ℕ) (pts : List Ent) (segs : List SegE) (hD : 0 < D) (hS : 0 < S)
    (hR : 0 < R) (hnd : pts.Nodup) (hsnd : segs.Nodup) :
    ∀ (t : ZTM) (x0 x1 y0 y1 u0 u1 : ℕ) (c : List Ent) (s : List SegE), c.Sublist pts →
      s.Sublist segs → checkM W S (D * S) R F t x0 x1 y0 y1 u0 u1 c s = true →
      CovM D S Mq R W pts segs x0 x1 y0 y1 u0 u1 := by
  intro t
  induction t with
  | Z cl chA chB emp sc sb tg lb =>
    intro x0 x1 y0 y1 u0 u1 c s hc hs h
    simp only [checkM, Bool.and_eq_true, Nat.ble_eq] at h
    obtain ⟨⟨⟨hu1, hu01⟩, hpc⟩, hz⟩ := h
    exact ZM_cov hD hS hR hnd hsnd ((claim_sub cl c).trans hc) ((sclaim_sub sc s).trans hs) hu01 hu1
      hpc hz
  | E =>
    intro x0 x1 y0 y1 u0 u1 c s hc hs h
    simp only [checkM, Bool.and_eq_true, Nat.ble_eq] at h
    exact CovM.of_cov (E_cov hD hS hR h.1 h.2)
  | C us t ih =>
    intro x0 x1 y0 y1 u0 u1 c s hc hs h
    simp only [checkM, Bool.and_eq_true] at h
    exact CM_cov hD hS hR h.1 (ih _ _ _ _ _ _ _ _ hc hs h.2)
  | F t ih =>
    intro x0 x1 y0 y1 u0 u1 c s hc hs h
    simp only [checkM] at h
    exact ih _ _ _ _ _ _ _ _ ((List.filter_sublist).trans hc) hs h
  | G t ih =>
    intro x0 x1 y0 y1 u0 u1 c s hc hs h
    simp only [checkM] at h
    exact ih _ _ _ _ _ _ _ _ hc ((List.filter_sublist).trans hs) h
  | X l r ihl ihr =>
    intro x0 x1 y0 y1 u0 u1 c s hc hs h
    simp only [checkM, Bool.and_eq_true] at h
    exact CovM.splitX _ (ihl _ _ _ _ _ _ _ _ hc hs h.1) (ihr _ _ _ _ _ _ _ _ hc hs h.2)
  | Y l r ihl ihr =>
    intro x0 x1 y0 y1 u0 u1 c s hc hs h
    simp only [checkM, Bool.and_eq_true] at h
    exact CovM.splitY _ (ihl _ _ _ _ _ _ _ _ hc hs h.1) (ihr _ _ _ _ _ _ _ _ hc hs h.2)
  | U l r ihl ihr =>
    intro x0 x1 y0 y1 u0 u1 c s hc hs h
    simp only [checkM, Bool.and_eq_true] at h
    exact CovM.splitU _ (ihl _ _ _ _ _ _ _ _ hc hs h.1) (ihr _ _ _ _ _ _ _ _ hc hs h.2)
  | XM m l r ihl ihr =>
    intro x0 x1 y0 y1 u0 u1 c s hc hs h
    simp only [checkM, Bool.and_eq_true] at h
    exact CovM.splitX m (ihl _ _ _ _ _ _ _ _ hc hs h.1) (ihr _ _ _ _ _ _ _ _ hc hs h.2)
  | YM m l r ihl ihr =>
    intro x0 x1 y0 y1 u0 u1 c s hc hs h
    simp only [checkM, Bool.and_eq_true] at h
    exact CovM.splitY m (ihl _ _ _ _ _ _ _ _ hc hs h.1) (ihr _ _ _ _ _ _ _ _ hc hs h.2)
  | UM m l r ihl ihr =>
    intro x0 x1 y0 y1 u0 u1 c s hc hs h
    simp only [checkM, Bool.and_eq_true] at h
    exact CovM.splitU m (ihl _ _ _ _ _ _ _ _ hc hs h.1) (ihr _ _ _ _ _ _ _ _ hc hs h.2)

end soundM

/-! ## 3.  Compact encoding

As `ZMTree.dec` (structure digits base `B`: `0` a `Z` leaf, `1`–`3` `X`/`Y`/`U`, `4` `F`, `5` `E`,
`6` `C`, `7`–`9` `XM`/`YM`/`UM`, and `10` `G`), but a `Z` leaf takes **two** numbers from the leaf
list: its point part (`ZMTree.decZ` format) and its piece part: `nsc`, then `nsc` claims (gap, tag);
`nsb`, then S-blocks `dir, K, A, B`; `ntg`, then T-groups `dir, K, Au, Bu, Ad, Bd, τu+1, τd+1, np`
and `np` pairs `ju+1, a, b, jd+1, c, d, m` — coordinates and masses as three base-`B` digits.  The
decoder needs no proof. -/

def bigD (B n : ℕ) : ℕ × ℕ :=
  (Nat.add (Nat.mod n B) (Nat.mul B (Nat.add (Nat.mod (Nat.div n B) B)
      (Nat.mul B (Nat.mod (Nat.div (Nat.div n B) B) B)))),
    Nat.div (Nat.div (Nat.div n B) B) B)

def decScs (B : ℕ) : ℕ → ℕ → List (ℕ × ℕ) × ℕ
  | 0, n => ([], n)
  | k + 1, n =>
    match decScs B k (Nat.div (Nat.div n B) B) with
    | (l, r) => ((Nat.mod n B, Nat.mod (Nat.div n B) B) :: l, r)

def decSb (B n : ℕ) : SBlk × ℕ :=
  match bigD B (Nat.div n B) with
  | (K, n1) => match bigD B n1 with
    | (A, n2) => match bigD B n2 with
      | (Bv, n3) => ((Nat.mod n B, K, A, Bv), n3)

def decSbs (B : ℕ) : ℕ → ℕ → List SBlk × ℕ
  | 0, n => ([], n)
  | k + 1, n => match decSb B n with
    | (b, n1) => match decSbs B k n1 with
      | (l, r) => (b :: l, r)

def decTp (B n : ℕ) : TPr × ℕ :=
  match bigD B (Nat.div n B) with
  | (a, n1) => match bigD B n1 with
    | (b, n2) => match bigD B (Nat.div n2 B) with
      | (c, n3) => match bigD B n3 with
        | (d, n4) => match bigD B n4 with
          | (m, n5) => ((Nat.mod n B, a, b, Nat.mod n2 B, c, d, m), n5)

def decTps (B : ℕ) : ℕ → ℕ → List TPr × ℕ
  | 0, n => ([], n)
  | k + 1, n => match decTp B n with
    | (p, n1) => match decTps B k n1 with
      | (l, r) => (p :: l, r)

def decTg (B n : ℕ) : TGrp × ℕ :=
  match bigD B (Nat.div n B) with
  | (K, n1) => match bigD B n1 with
    | (Au, n2) => match bigD B n2 with
      | (Bu, n3) => match bigD B n3 with
        | (Ad, n4) => match bigD B n4 with
          | (Bd, n5) => match bigD B n5 with
            | (tu, n6) => match bigD B n6 with
              | (td, n7) => match decTps B (Nat.mod n7 B) (Nat.div n7 B) with
                | (prs, n8) => ((Nat.mod n B, K, Au, Bu, Ad, Bd, tu, td, prs), n8)

def decTgs (B : ℕ) : ℕ → ℕ → List TGrp × ℕ
  | 0, n => ([], n)
  | k + 1, n => match decTg B n with
    | (g, n1) => match decTgs B k n1 with
      | (l, r) => (g :: l, r)


/-- Four base-`B` digits. -/
def big4 (B n : ℕ) : ℕ × ℕ :=
  match bigD B n with
  | (v, n1) => (Nat.add v (Nat.mul (Nat.mul B (Nat.mul B B)) (Nat.mod n1 B)), Nat.div n1 B)

def decLPcs (B : ℕ) : ℕ → ℕ → List (ℕ × ℕ × ℕ) × ℕ
  | 0, n => ([], n)
  | k + 1, n =>
    match big4 B (Nat.div n B) with
    | (lo, n1) => match big4 B n1 with
      | (hi, n2) => match decLPcs B k n2 with
        | (l, r) => ((Nat.mod n B, lo, hi) :: l, r)

def decLLine (B n : ℕ) : LLine × ℕ :=
  match big4 B (Nat.div n B) with
  | (K, n1) => match big4 B n1 with
  | (a, n2) => match big4 B n2 with
  | (b, n3) => match big4 B n3 with
  | (du, n4) => match big4 B n4 with
  | (dd, n5) => match big4 B (Nat.div n5 B) with
  | (sU, n6) => match big4 B n6 with
  | (iUp, n7) => match big4 B n7 with
  | (iUn, n8) => match big4 B n8 with
  | (sD, n9) => match big4 B n9 with
  | (iDp, n10) => match big4 B n10 with
  | (iDn, n11) => match decLPcs B (Nat.mod n11 B) (Nat.div n11 B) with
  | (up, n12) => match decLPcs B (Nat.mod n12 B) (Nat.div n12 B) with
  | (core, n13) => match decLPcs B (Nat.mod n13 B) (Nat.div n13 B) with
  | (dn, n14) =>
    (⟨Nat.mod n B, K, a, b, du, dd, Nat.mod n5 B, sU, (iUp, iUn), sD, (iDp, iDn), up, core, dn⟩, n14)

def decLLines (B : ℕ) : ℕ → ℕ → List LLine × ℕ
  | 0, n => ([], n)
  | k + 1, n => match decLLine B n with
    | (l, n1) => match decLLines B k n1 with
      | (ls, r) => (l :: ls, r)

def decCh (B : ℕ) : ℕ → ℕ → List (ℕ × ℕ × ℕ × ℕ) × ℕ
  | 0, n => ([], n)
  | k + 1, n =>
    match big4 B (Nat.div n B) with
    | (sU, n1) => match big4 B (Nat.div n1 B) with
      | (sD, n2) => match decCh B k n2 with
        | (l, r) => ((Nat.mod n B, sU, Nat.mod n1 B, sD) :: l, r)

def decLBlk (B n : ℕ) : LBlk × ℕ :=
  match decLLines B (Nat.mod n B) (Nat.div n B) with
  | (ls, n1) => match decCh B ls.length n1 with
  | (c0, n2) => match decCh B ls.length n2 with
  | (c1, n3) => match decCh B ls.length n3 with
  | (c2, n4) => match decCh B ls.length n4 with
  | (c3, n5) => match big4 B n5 with
  | (lg, n6) => (⟨ls, [c0, c1, c2, c3], lg⟩, n6)

def decLBlks (B : ℕ) : ℕ → ℕ → List LBlk × ℕ
  | 0, n => ([], n)
  | k + 1, n => match decLBlk B n with
    | (b, n1) => match decLBlks B k n1 with
      | (l, r) => (b :: l, r)

/-- The piece part of a `Z` leaf: claims, S-blocks, T-groups, L-blocks. -/
def decPc (B n : ℕ) : List (ℕ × ℕ) × List SBlk × List TGrp × List LBlk :=
  match decScs B (Nat.mod n B) (Nat.div n B) with
  | (sc, n1) => match decSbs B (Nat.mod n1 B) (Nat.div n1 B) with
    | (sb, n2) => match decTgs B (Nat.mod n2 B) (Nat.div n2 B) with
      | (tg, n3) => (sc, sb, tg, (decLBlks B (Nat.mod n3 B) (Nat.div n3 B)).1)

/-- A mixed `Z` leaf from its two numbers. -/
def decZM (B n np : ℕ) : ZTM :=
  match ZMTree.decZ B n with
  | .Z cl chA chB emp => match decPc B np with
    | (sc, sb, tg, lb) => .Z cl chA chB emp sc sb tg lb
  | _ => .E

/-- Decode a tree of depth `≤ fuel`. -/
def decM (B : ℕ) : ℕ → ℕ → List ℕ → ZTM × ℕ × List ℕ
  | 0, n, L => (.E, n, L)
  | f + 1, n, L =>
    match Nat.mod n B with
    | 0 => (decZM B (L.headD 0) (L.tail.headD 0), Nat.div n B, L.tail.tail)
    | 1 => match decM B f (Nat.div n B) L with
      | (l, n1, L1) => match decM B f n1 L1 with
        | (r, n2, L2) => (.X l r, n2, L2)
    | 2 => match decM B f (Nat.div n B) L with
      | (l, n1, L1) => match decM B f n1 L1 with
        | (r, n2, L2) => (.Y l r, n2, L2)
    | 3 => match decM B f (Nat.div n B) L with
      | (l, n1, L1) => match decM B f n1 L1 with
        | (r, n2, L2) => (.U l r, n2, L2)
    | 4 => match decM B f (Nat.div n B) L with
      | (t, n1, L1) => (.F t, n1, L1)
    | 5 => (.E, Nat.div n B, L)
    | 7 => match decM B f (Nat.div (Nat.div (Nat.div n B) B) B) L with
      | (l, n1, L1) => match decM B f n1 L1 with
        | (r, n2, L2) =>
          (.XM (Nat.add (Nat.mod (Nat.div n B) B) (Nat.mul B (Nat.mod (Nat.div (Nat.div n B) B) B)))
            l r, n2, L2)
    | 8 => match decM B f (Nat.div (Nat.div (Nat.div n B) B) B) L with
      | (l, n1, L1) => match decM B f n1 L1 with
        | (r, n2, L2) =>
          (.YM (Nat.add (Nat.mod (Nat.div n B) B) (Nat.mul B (Nat.mod (Nat.div (Nat.div n B) B) B)))
            l r, n2, L2)
    | 9 => match decM B f (Nat.div (Nat.div (Nat.div n B) B) B) L with
      | (l, n1, L1) => match decM B f n1 L1 with
        | (r, n2, L2) =>
          (.UM (Nat.add (Nat.mod (Nat.div n B) B) (Nat.mul B (Nat.mod (Nat.div (Nat.div n B) B) B)))
            l r, n2, L2)
    | 10 => match decM B f (Nat.div n B) L with
      | (t, n1, L1) => (.G t, n1, L1)
    | _ => match decM B f (Nat.div (Nat.div (Nat.div n B) B) B) L with
      | (t, n1, L1) =>
        (.C (Nat.add (Nat.mod (Nat.div n B) B) (Nat.mul B (Nat.mod (Nat.div (Nat.div n B) B) B))) t,
          n1, L1)

end ZMTreeM

end SquarePacking
