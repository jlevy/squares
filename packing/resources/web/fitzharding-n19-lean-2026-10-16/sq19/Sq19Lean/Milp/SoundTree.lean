import Sq19Lean.Milp.SoundRows

/-!
# Soundness of the tree replay and of `checkCert`

`checkCert_sound`: if `checkCert P text = true` then no configuration of the squares of `P` with
relative angles and offsets in their boxes, every square inside `[0, L]^2`, pairwise disjoint
interiors and `L ≤ side19` exists.
-/
namespace Sq19.Milp
open Sq17.Propagation

@[simp] theorem Ctx.ofProb_P (P : Prob) : (Ctx.ofProb P).P = P := rfl
@[simp] theorem Ctx.ofProb_pairs (P : Prob) : (Ctx.ofProb P).pairs = P.pairs := rfl
@[simp] theorem Ctx.ofProb_zinfo (P : Prob) : (Ctx.ofProb P).zinfo = zinfoOf P.pairs := rfl
@[simp] theorem Ctx.ofProb_rows (P : Prob) : (Ctx.ofProb P).rows = P.rows := rfl

theorem Ctx.possible_eq (P : Prob) (ang : ℕ → Iv) (p oi : ℕ) :
    (Ctx.ofProb P).possible (boxTrig ang) (boxH ang) p oi =
      facePossible (boxTrig ang) (boxH ang)
        (optSqs P.sqs (P.pairs.getD p Pair.default) ((P.pairs.getD p Pair.default).opts.getD oi ⟨false, 0⟩)).1
        (optSqs P.sqs (P.pairs.getD p Pair.default) ((P.pairs.getD p Pair.default).opts.getD oi ⟨false, 0⟩)).2
        ((P.pairs.getD p Pair.default).opts.getD oi ⟨false, 0⟩).k := rfl

theorem Ctx.colBox_eq (P : Prob) (zfix : ℕ → Option Bool) (j : ℕ) :
    (Ctx.ofProb P).colBox zfix j =
      if j < 2 * P.n then (if j % 2 = 0 then (P.sq (j / 2)).x else (P.sq (j / 2)).y)
      else match zfix (j - 2 * P.n) with
        | some true => Iv.pt 1
        | some false => Iv.pt 0
        | none => ⟨0, 1⟩ := rfl

theorem Xval_lt (P : Prob) (θ dx dy : ℕ → ℝ) {j : ℕ} (hj : j < 2 * P.n) :
    Xval P θ dx dy j = if j % 2 = 0 then dx (P.sq (j / 2)).s else dy (P.sq (j / 2)).s := by
  unfold Xval; rw [if_pos hj]
theorem Xval_ge (P : Prob) (θ dx dy : ℕ → ℝ) {j : ℕ} (hj : ¬ j < 2 * P.n) :
    Xval P θ dx dy j = if zb P θ dx dy (j - 2 * P.n) then 1 else 0 := by
  unfold Xval; rw [if_neg hj]

section
variable {P : Prob} {θ dx dy : ℕ → ℝ} {L : ℝ}

theorem rows_hold (hg : Good P θ dx dy L) (hM : P.bigMOk = true) :
    ∀ r ∈ P.rows, r.Holds θ (Xval P θ dx dy) L := by
  intro r hr
  unfold Prob.rows at hr
  rcases List.mem_append.mp hr with h | h
  · obtain ⟨qi, hqi, hr⟩ := List.mem_flatMap.mp h
    exact wall_rows_hold hg hqi r hr
  · obtain ⟨pp, hpp, hr⟩ := List.mem_flatMap.mp h
    exact pair_rows_hold hg hM hpp r hr

theorem rowAt_holds (hg : Good P θ dx dy L) (hM : P.bigMOk = true) (i : ℕ) :
    (rowAt P.rows i).Holds θ (Xval P θ dx dy) L := by
  unfold rowAt
  rw [List.getD_eq_getElem?_getD]
  by_cases hi : i < P.rows.length
  · rw [List.getElem?_eq_getElem hi]; exact rows_hold hg hM _ (List.getElem_mem hi)
  · rw [List.getElem?_eq_none (by omega)]
    simp [Row.Holds, Row.default, Ex.real]

/-- Node invariant: angles in the node's box, indicators consistent with the fixings. -/
def Inv (P : Prob) (θ dx dy : ℕ → ℝ) (ang : ℕ → Iv) (zfix : ℕ → Option Bool) : Prop :=
  InAng θ ang ∧ ∀ z b, zfix z = some b → zb P θ dx dy z = b

theorem possible_of_sep (hg : Good P θ dx dy L) {ang : ℕ → Iv} (hθ : InAng θ ang)
    {p oi : ℕ} (hp : p < P.pairs.length) (ho : oi < P.pairs[p].opts.length)
    (hs : OptSep P θ dx dy P.pairs[p] (P.pairs[p].opts[oi])) :
    (Ctx.ofProb P).possible (boxTrig ang) (boxH ang) p oi = true := by
  have hprm : P.pairs[p] ∈ P.pairs := List.getElem_mem hp
  obtain ⟨hi, hj, _, _⟩ := mem_pairs hprm
  obtain ⟨hA, hB⟩ := optSqs_cols P P.pairs[p] (P.pairs[p].opts[oi])
  have hca : (optCols P.pairs[p] (P.pairs[p].opts[oi])).1 < P.n := by unfold optCols; split_ifs <;> assumption
  have hcb : (optCols P.pairs[p] (P.pairs[p].opts[oi])).2 < P.n := by unfold optCols; split_ifs <;> assumption
  have pA := hg.pos _ (P.sq_mem hca)
  have pB := hg.pos _ (P.sq_mem hcb)
  rw [← hA] at pA; rw [← hB] at pB
  rw [Ctx.possible_eq]
  have g1 : P.pairs.getD p Pair.default = P.pairs[p] := by
    rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hp]; rfl
  have g2 : P.pairs[p].opts.getD oi ⟨false, 0⟩ = P.pairs[p].opts[oi] := by
    rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem ho]; rfl
  rw [g1, g2]
  exact facePossible_sound hθ _ _ pA pB _ hs

theorem fix_inv (hg : Good P θ dx dy L) {ang : ℕ → Iv} {zf : ZF}
    (hI : Inv P θ dx dy ang (zget zf)) :
    Inv P θ dx dy ang (zget ((Ctx.ofProb P).fix (boxTrig ang) (boxH ang) zf)) := by
  refine ⟨hI.1, ?_⟩
  intro z b hz
  unfold Ctx.fix at hz
  rw [zget_append_false] at hz
  split_ifs at hz with himp
  · simp only [Option.some.injEq] at hz
    subst hz
    simp only [List.contains_iff_mem, List.mem_filter, List.mem_range, Bool.and_eq_true,
      decide_eq_true_eq, Bool.not_eq_true'] at himp
    obtain ⟨hzl, _, hnp⟩ := himp
    by_contra hb
    have hzb : zb P θ dx dy z = true := by simpa using hb
    simp only [Ctx.ofProb_zinfo] at hzl hnp
    set po := (zinfoOf P.pairs).getD z (0, 0)
    have hmem : po ∈ zinfoOf P.pairs := by
      simp only [po]; rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hzl]; exact List.getElem_mem hzl
    obtain ⟨hp, hm, ho⟩ := mem_zinfo.mp (show (po.1, po.2) ∈ zinfoOf P.pairs from hmem)
    have ezb : zb P θ dx dy z = decide (po.2 = firstSep P θ dx dy (P.pairs.getD po.1 Pair.default)) := rfl
    rw [ezb] at hzb
    have hzb2 := of_decide_eq_true hzb
    have g1 : P.pairs.getD po.1 Pair.default = P.pairs[po.1] := by
      rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hp]; rfl
    rw [g1] at hzb2
    obtain ⟨hfl, hfs⟩ := firstSep_spec hg (List.getElem_mem hp)
    have hs : OptSep P θ dx dy P.pairs[po.1] (P.pairs[po.1].opts[po.2]) := by
      have h' : P.pairs[po.1].opts[firstSep P θ dx dy P.pairs[po.1]]'hfl = P.pairs[po.1].opts[po.2] := by
        congr 1; exact hzb2.symm
      rw [← h']; exact hfs
    have := possible_of_sep hg hI.1 hp ho hs
    rw [this] at hnp
    exact absurd hnp (by decide)
  · exact hI.2 z b hz

theorem emptyPair_false (hg : Good P θ dx dy L) {ang : ℕ → Iv} {zfix : ℕ → Option Bool}
    (hI : Inv P θ dx dy ang zfix) {p : ℕ}
    (h : (Ctx.ofProb P).emptyPair (boxTrig ang) (boxH ang) zfix p = true) : False := by
  unfold Ctx.emptyPair at h
  simp only [Ctx.ofProb_pairs, Ctx.ofProb_zinfo, Bool.and_eq_true, List.all_eq_true, List.mem_range,
    Bool.or_eq_true, Bool.not_eq_true'] at h
  obtain ⟨⟨hp, hm⟩, hall⟩ := h
  have hp' : p < P.pairs.length := of_decide_eq_true hp
  have hget : P.pairs.getD p Pair.default = P.pairs[p] := by
    rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hp']; rfl
  have hm' : 1 < P.pairs[p].opts.length := by rw [← hget]; exact of_decide_eq_true hm
  obtain ⟨hfl, hfs⟩ := firstSep_spec hg (List.getElem_mem hp')
  have hfl' : firstSep P θ dx dy P.pairs[p] < (P.pairs.getD p Pair.default).opts.length := by
    rw [hget]; exact hfl
  rcases hall _ hfl' with h1 | h1
  · have := hI.2 _ _ (of_decide_eq_true h1)
    rw [zb_idxOf hp' hget hm' hfl] at this
    simp at this
  · have := possible_of_sep hg hI.1 hp' hfl hfs
    rw [this] at h1
    exact absurd h1 (by decide)

theorem side19_le_s19hi : side19 ≤ (s19hi : ℝ) := by
  have h2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hp : 0 ≤ Real.sqrt 2 := Real.sqrt_nonneg 2
  unfold side19 s19hi; push_cast
  nlinarith

theorem leaf_false (hg : Good P θ dx dy L) (hL : L ≤ side19) (hM : P.bigMOk = true)
    {ang : ℕ → Iv} {zfix : ℕ → Option Bool} (hI : Inv P θ dx dy ang zfix) {y : List (ℕ × ℚ)}
    (h : leafCheck (boxTrig ang) (boxH ang) (Ctx.ofProb P).rows (Ctx.ofProb P).ncol
      ((Ctx.ofProb P).colBox zfix) s19hi y = true) : False := by
  apply leaf_sound (boxTrig ang) (boxTrig_valid ang) (boxH ang) _ _ _ _ y h
    (fun k => θ k - (boxTrig ang).cen k) (boxH_bound hI.1) (Xval P θ dx dy) ?_ L
    (hL.trans side19_le_s19hi)
  · intro p _
    rw [boxTrig_shift θ ang]
    exact rowAt_holds hg hM p.1
  · intro j _
    rw [Ctx.colBox_eq]
    by_cases hjn : j < 2 * P.n
    · rw [if_pos hjn, Xval_lt P θ dx dy hjn]
      have hi : j / 2 < P.n := by omega
      have pos := hg.pos _ (P.sq_mem hi)
      by_cases hev : j % 2 = 0
      · rw [if_pos hev, if_pos hev]; exact pos.1
      · rw [if_neg hev, if_neg hev]; exact pos.2
    · rw [if_neg hjn, Xval_ge P θ dx dy hjn]
      cases hz : zfix (j - 2 * P.n) with
      | none =>
        simp only
        split_ifs <;> simp [Iv.mem]
      | some b =>
        have := hI.2 _ _ hz
        cases b <;> simp [this, Iv.mem, Iv.pt]

theorem check_sound (hg : Good P θ dx dy L) (hL : L ≤ side19) (hM : P.bigMOk = true)
    (t : Cert) : ∀ ang (zf : ZF), Inv P θ dx dy ang (zget zf) → (Ctx.ofProb P).check ang zf t = true → False := by
  induction t with
  | Z k one zero ih1 ih0 =>
    intro ang zf hI h
    simp only [Ctx.check, Bool.and_eq_true] at h
    have hF := fix_inv hg hI
    cases hk : zb P θ dx dy k
    · apply ih0 _ _ ?_ h.2
      refine ⟨hF.1, fun z b hz => ?_⟩
      rw [zget_cons] at hz
      split_ifs at hz with he
      · subst he; simp only [Option.some.injEq] at hz; rw [hk, ← hz]
      · exact hF.2 z b hz
    · apply ih1 _ _ ?_ h.1
      refine ⟨hF.1, fun z b hz => ?_⟩
      rw [zget_cons] at hz
      split_ifs at hz with he
      · subst he; simp only [Option.some.injEq] at hz; rw [hk, ← hz]
      · exact hF.2 z b hz
  | S s m lo hi ihl ihh =>
    intro ang zf hI h
    simp only [Ctx.check, Bool.and_eq_true] at h
    have hF := fix_inv hg hI
    rcases le_total (θ s) m with hm | hm
    · apply ihl _ _ ⟨fun k => ?_, hF.2⟩ h.1
      unfold splitLo; split_ifs with he
      · subst he; exact ⟨(hI.1 k).1, hm⟩
      · exact hI.1 k
    · apply ihh _ _ ⟨fun k => ?_, hF.2⟩ h.2
      unfold splitHi; split_ifs with he
      · subst he; exact ⟨hm, (hI.1 k).2⟩
      · exact hI.1 k
  | E p =>
    intro ang zf hI h
    simp only [Ctx.check] at h
    exact emptyPair_false hg (fix_inv hg hI) h
  | C y =>
    intro ang zf hI h
    simp only [Ctx.check] at h
    exact leaf_false hg hL hM (fix_inv hg hI) h
  | F =>
    intro ang zf hI h
    simp [Ctx.check] at h

end

/-- **Soundness of the certificate check.** -/
theorem checkTree_sound (P : Prob) (t : Cert) (h : checkTree P t = true)
    (θ dx dy : ℕ → ℝ) (L : ℝ) (hL : L ≤ side19)
    (hbox : ∀ q ∈ P.sqs, Iv.mem (θ q.s) q.a ∧ Iv.mem (dx q.s) q.x ∧ Iv.mem (dy q.s) q.y)
    (hfit : ∀ q ∈ P.sqs, Sq17.sq (q.rx + dx q.s) (q.ry + dy q.s)
      (Real.cos (q.m * Real.pi / 4 + θ q.s)) (Real.sin (q.m * Real.pi / 4 + θ q.s)) ⊆ containerBox L)
    (hdis : ∀ i j, i < P.sqs.length → j < P.sqs.length → i ≠ j →
      Disjoint (interior (Sq17.sq ((P.sq i).rx + dx (P.sq i).s) ((P.sq i).ry + dy (P.sq i).s)
          (Real.cos ((P.sq i).m * Real.pi / 4 + θ (P.sq i).s))
          (Real.sin ((P.sq i).m * Real.pi / 4 + θ (P.sq i).s))))
        (interior (Sq17.sq ((P.sq j).rx + dx (P.sq j).s) ((P.sq j).ry + dy (P.sq j).s)
          (Real.cos ((P.sq j).m * Real.pi / 4 + θ (P.sq j).s))
          (Real.sin ((P.sq j).m * Real.pi / 4 + θ (P.sq j).s))))) : False := by
  classical
  -- angles off the squares are irrelevant; put them at 0
  let θ' : ℕ → ℝ := fun k => if (P.sqs.find? (fun q => q.s = k)).isSome then θ k else 0
  have hθ' : ∀ q ∈ P.sqs, θ' q.s = θ q.s := by
    intro q hq
    have : (P.sqs.find? (fun r => r.s = q.s)).isSome := by
      rw [List.find?_isSome]; exact ⟨q, hq, by simp⟩
    simp only [θ', this, if_true]
  unfold checkTree at h
  simp only [Bool.and_eq_true] at h
  · have hg : Good P θ' dx dy L := by
      refine ⟨fun k => ?_, fun q hq => ⟨(hbox q hq).2.1, (hbox q hq).2.2⟩, fun q hq => ?_, ?_⟩
      · unfold Prob.rootAng
        cases hf : P.sqs.find? (fun q => q.s = k) with
        | none => simp only [θ', hf, Option.isSome_none]; simp [Iv.mem, Iv.pt]
        | some q =>
          have hq := List.mem_of_find?_eq_some hf
          have hqs := List.find?_some hf
          simp only [decide_eq_true_eq] at hqs
          simp only [θ', hf, Option.isSome_some, if_true]
          rw [← hqs]; exact (hbox q hq).1
      · simp only [cenOf, angOf, hθ' q hq]; exact hfit q hq
      · intro i j hi hj hij
        simp only [cenOf, angOf, hθ' _ (P.sq_mem hi), hθ' _ (P.sq_mem hj)]
        exact hdis i j hi hj hij
    exact check_sound hg hL h.1 t P.rootAng []
      ⟨hg.ang, fun z b hz => by simp [zget] at hz⟩ h.2

/-- The text form. -/
theorem checkCert_sound (P : Prob) (text : String) (h : checkCert P text = true)
    (θ dx dy : ℕ → ℝ) (L : ℝ) (hL : L ≤ side19)
    (hbox : ∀ q ∈ P.sqs, Iv.mem (θ q.s) q.a ∧ Iv.mem (dx q.s) q.x ∧ Iv.mem (dy q.s) q.y)
    (hfit : ∀ q ∈ P.sqs, Sq17.sq (q.rx + dx q.s) (q.ry + dy q.s)
      (Real.cos (q.m * Real.pi / 4 + θ q.s)) (Real.sin (q.m * Real.pi / 4 + θ q.s)) ⊆ containerBox L)
    (hdis : ∀ i j, i < P.sqs.length → j < P.sqs.length → i ≠ j →
      Disjoint (interior (Sq17.sq ((P.sq i).rx + dx (P.sq i).s) ((P.sq i).ry + dy (P.sq i).s)
          (Real.cos ((P.sq i).m * Real.pi / 4 + θ (P.sq i).s))
          (Real.sin ((P.sq i).m * Real.pi / 4 + θ (P.sq i).s))))
        (interior (Sq17.sq ((P.sq j).rx + dx (P.sq j).s) ((P.sq j).ry + dy (P.sq j).s)
          (Real.cos ((P.sq j).m * Real.pi / 4 + θ (P.sq j).s))
          (Real.sin ((P.sq j).m * Real.pi / 4 + θ (P.sq j).s))))) : False := by
  unfold checkCert at h
  split at h
  · rename_i t _
    exact checkTree_sound P t h θ dx dy L hL hbox hfit hdis
  · simp at h

end Sq19.Milp

#print axioms Sq19.Milp.checkTree_sound
#print axioms Sq19.Milp.checkCert_sound
