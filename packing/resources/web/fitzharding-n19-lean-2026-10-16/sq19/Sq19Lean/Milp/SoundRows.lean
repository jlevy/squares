import Sq19Lean.Milp.Sound

/-!
# Every row holds at a packing

For a configuration in the root box with every square in `[0, L]^2` and pairwise disjoint
interiors, define the indicator of each option as `1` exactly for the first separating option of
its pair. Then all rows of `Prob.rows` hold (`rows_hold`).
-/
namespace Sq19.Milp
open Sq17.Propagation

/-- A configuration of the included squares satisfying the packing constraints in the box. -/
structure Good (P : Prob) (θ dx dy : ℕ → ℝ) (L : ℝ) : Prop where
  ang : InAng θ P.rootAng
  pos : ∀ q ∈ P.sqs, InPos dx dy q
  fit : ∀ q ∈ P.sqs, Sq17.sq (cenOf dx dy q).1 (cenOf dx dy q).2
    (Real.cos (angOf θ q)) (Real.sin (angOf θ q)) ⊆ containerBox L
  dis : ∀ i j, i < P.n → j < P.n → i ≠ j →
    Disjoint (interior (Sq17.sq (cenOf dx dy (P.sq i)).1 (cenOf dx dy (P.sq i)).2
        (Real.cos (angOf θ (P.sq i))) (Real.sin (angOf θ (P.sq i)))))
      (interior (Sq17.sq (cenOf dx dy (P.sq j)).1 (cenOf dx dy (P.sq j)).2
        (Real.cos (angOf θ (P.sq j))) (Real.sin (angOf θ (P.sq j)))))

theorem Prob.sq_mem (P : Prob) {i : ℕ} (h : i < P.n) : P.sq i ∈ P.sqs := by
  simp only [Prob.sq, List.getD_eq_getElem?_getD]
  rw [List.getElem?_eq_getElem h]; exact List.getElem_mem h

theorem optSqs_eq (sqs : List Sq) (pr : Pair) (o : Opt) :
    optSqs sqs pr o = optSqs sqs ⟨pr.i, pr.j, []⟩ o := rfl

theorem optSqs_cols (P : Prob) (pr : Pair) (o : Opt) :
    (optSqs P.sqs pr o).1 = P.sq (optCols pr o).1 ∧ (optSqs P.sqs pr o).2 = P.sq (optCols pr o).2 := by
  unfold optSqs optCols Prob.sq; split_ifs <;> exact ⟨rfl, rfl⟩

theorem mem_pairs {P : Prob} {pr : Pair} (h : pr ∈ P.pairs) :
    pr.i < P.n ∧ pr.j < P.n ∧ pr.i < pr.j ∧
    pr.opts = allOpts.filter (fun o => facePossible (boxTrig P.rootAng) (boxH P.rootAng)
      (optSqs P.sqs pr o).1 (optSqs P.sqs pr o).2 o.k) := by
  unfold Prob.pairs at h
  simp only [List.mem_filterMap, List.mem_flatMap, List.mem_range, List.mem_map, List.mem_filter,
    decide_eq_true_eq] at h
  obtain ⟨⟨a, b⟩, ⟨i, hi, j, ⟨hj, hij⟩, he⟩, hf⟩ := h
  simp only [Prod.mk.injEq] at he
  obtain ⟨rfl, rfl⟩ := he
  split_ifs at hf
  simp only [Option.some.injEq] at hf
  subst hf
  exact ⟨hi, hj, hij, rfl⟩

/-- Option `o` of `pr` separates its pair. -/
def OptSep (P : Prob) (θ dx dy : ℕ → ℝ) (pr : Pair) (o : Opt) : Prop :=
  Sep (cenOf dx dy (optSqs P.sqs pr o).1) (angOf θ (optSqs P.sqs pr o).1)
    (cenOf dx dy (optSqs P.sqs pr o).2) (angOf θ (optSqs P.sqs pr o).2) o.k

/-- **Coverage.** Some option of every pair separates it. -/
theorem exists_optSep {P : Prob} {θ dx dy : ℕ → ℝ} {L : ℝ} (hg : Good P θ dx dy L)
    {pr : Pair} (h : pr ∈ P.pairs) : ∃ o ∈ pr.opts, OptSep P θ dx dy pr o := by
  obtain ⟨hi, hj, hij, ho⟩ := mem_pairs h
  have hd := hg.dis pr.i pr.j hi hj (Nat.ne_of_lt hij)
  obtain ⟨k, hk, hs | hs⟩ := face_disjunction _ _ _ _ hd
  · refine ⟨⟨false, k⟩, ?_, hs⟩
    rw [ho, List.mem_filter]
    refine ⟨by simp [allOpts]; omega, ?_⟩
    exact facePossible_sound hg.ang _ _ (hg.pos _ (P.sq_mem hi)) (hg.pos _ (P.sq_mem hj)) k hs
  · refine ⟨⟨true, k⟩, ?_, hs⟩
    rw [ho, List.mem_filter]
    refine ⟨by simp [allOpts]; omega, ?_⟩
    exact facePossible_sound hg.ang _ _ (hg.pos _ (P.sq_mem hj)) (hg.pos _ (P.sq_mem hi)) k hs

open Classical in
/-- Index of the first separating option. -/
noncomputable def firstSep (P : Prob) (θ dx dy : ℕ → ℝ) (pr : Pair) : ℕ :=
  pr.opts.findIdx (fun o => decide (OptSep P θ dx dy pr o))

theorem firstSep_spec {P : Prob} {θ dx dy : ℕ → ℝ} {L : ℝ} (hg : Good P θ dx dy L)
    {pr : Pair} (h : pr ∈ P.pairs) :
    ∃ hl : firstSep P θ dx dy pr < pr.opts.length, OptSep P θ dx dy pr (pr.opts[firstSep P θ dx dy pr]) := by
  classical
  obtain ⟨o, ho, hs⟩ := exists_optSep hg h
  unfold firstSep
  have hl := List.findIdx_lt_length_of_exists (p := fun o => decide (OptSep P θ dx dy pr o))
    ⟨o, ho, by simpa using hs⟩
  refine ⟨hl, ?_⟩
  have := List.findIdx_getElem (p := fun o => decide (OptSep P θ dx dy pr o)) (w := hl)
  simpa using this

/-! ## Indicators and column values -/

theorem mem_zinfo {pairs : List Pair} {p oi : ℕ} :
    (p, oi) ∈ zinfoOf pairs ↔ ∃ h : p < pairs.length, 1 < pairs[p].opts.length ∧ oi < pairs[p].opts.length := by
  unfold zinfoOf
  simp only [List.mem_flatMap, List.mem_filter, List.mem_map, List.mem_range, Prod.mk.injEq,
    decide_eq_true_eq]
  constructor
  · rintro ⟨⟨pr, q⟩, ⟨hm, hl⟩, o, ho, rfl, rfl⟩
    rw [List.mem_zipIdx_iff_getElem?, List.getElem?_eq_some_iff] at hm
    obtain ⟨hq, he⟩ := hm
    simp only at hq he hl ho ⊢
    refine ⟨hq, ?_, ?_⟩ <;> rw [he] <;> assumption
  · rintro ⟨hp, hl, ho⟩
    refine ⟨⟨pairs[p], p⟩, ⟨?_, hl⟩, oi, ho, rfl, rfl⟩
    rw [List.mem_zipIdx_iff_getElem?]; simp [hp]

theorem zinfo_getD_idxOf {pairs : List Pair} {p oi : ℕ} (h : (p, oi) ∈ zinfoOf pairs) :
    (zinfoOf pairs).getD ((zinfoOf pairs).idxOf (p, oi)) (0, 0) = (p, oi) := by
  have hl := List.idxOf_lt_length_of_mem h
  rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hl]
  simp [List.getElem_idxOf hl]

section Config
variable (P : Prob) (θ dx dy : ℕ → ℝ)

/-- Indicator `z` is the first separating option of its pair. -/
noncomputable def zb (z : ℕ) : Bool :=
  let po := (zinfoOf P.pairs).getD z (0, 0)
  decide (po.2 = firstSep P θ dx dy (P.pairs.getD po.1 Pair.default))

/-- Column values: offsets, then indicators. -/
noncomputable def Xval (j : ℕ) : ℝ :=
  if j < 2 * P.n then (if j % 2 = 0 then dx (P.sq (j / 2)).s else dy (P.sq (j / 2)).s)
  else if zb P θ dx dy (j - 2 * P.n) then 1 else 0

theorem Xval_x {i : ℕ} (h : i < P.n) : Xval P θ dx dy (2*i) = dx (P.sq i).s := by
  unfold Xval; rw [if_pos (by omega), if_pos (by omega)]; congr 3; omega
theorem Xval_y {i : ℕ} (h : i < P.n) : Xval P θ dx dy (2*i+1) = dy (P.sq i).s := by
  unfold Xval; rw [if_pos (by omega), if_neg (by omega)]; congr 3; omega
theorem Xval_z (z : ℕ) : Xval P θ dx dy (2*P.n + z) = if zb P θ dx dy z then 1 else 0 := by
  unfold Xval; rw [if_neg (by omega), Nat.add_sub_cancel_left]

end Config

theorem zipIdx_get {α : Type} {l : List α} {a : α} {i : ℕ} (d : α) (h : (a, i) ∈ l.zipIdx) :
    i < l.length ∧ l.getD i d = a := by
  rw [List.mem_zipIdx_iff_getElem?, List.getElem?_eq_some_iff] at h
  obtain ⟨hi, he⟩ := h
  refine ⟨hi, ?_⟩
  rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hi]; simpa using he

theorem wall_rows_hold {P : Prob} {θ dx dy : ℕ → ℝ} {L : ℝ} (hg : Good P θ dx dy L)
    {q : Sq} {i : ℕ} (hqi : (q, i) ∈ P.sqs.zipIdx) :
    ∀ r ∈ wallRowsOf q i, r.Holds θ (Xval P θ dx dy) L := by
  obtain ⟨hi, hq⟩ := zipIdx_get Sq.default hqi
  have hqm : q ∈ P.sqs := by rw [← hq]; exact P.sq_mem hi
  have hx := Xval_x P θ dx dy hi
  have hy := Xval_y P θ dx dy hi
  have hsq : P.sq i = q := hq
  rw [hsq] at hx hy
  intro r hr
  simp only [wallRowsOf, List.mem_flatMap, List.mem_finRange, true_and, List.mem_cons,
    List.not_mem_nil, or_false] at hr
  obtain ⟨j, hr⟩ := hr
  have hv := vertex_in_container (cenOf dx dy q) (angOf θ q) L (hg.fit q hqm) j
  simp only [cenOf] at hv
  rcases hr with rfl | rfl | rfl | rfl <;>
    simp only [Row.Holds, List.map_cons, List.map_nil, List.sum_cons, List.sum_nil, Ex.real,
      vxE_real, vyE_real, hx, hy] <;> push_cast <;> linarith [hv.1, hv.2.1, hv.2.2.1, hv.2.2.2]

private theorem cs_bound (a1 a2 b1 b2 : ℝ) : (a1*b1 + a2*b2)^2 ≤ (a1^2 + a2^2) * (b1^2 + b2^2) := by
  nlinarith [sq_nonneg (a1*b2 - a2*b1)]

private theorem sum_indicator (n f : ℕ) :
    ((List.range n).map (fun oi => if oi = f then (1:ℝ) else 0)).sum = if f < n then 1 else 0 := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [List.range_succ, List.map_append, List.sum_append, ih]
    by_cases h1 : f < n
    · have : n ≠ f := by omega
      simp [h1, this, show f < n + 1 by omega]
    · by_cases h2 : f = n
      · subst h2; simp
      · have : n ≠ f := Ne.symm h2
        simp [h1, this, show ¬ f < n + 1 by omega]

/-- The big-M rows are slack enough: `n.(Δ + v) ≥ 1/2 - M` on the root box. -/
theorem bigM_slack {P : Prob} {θ dx dy : ℕ → ℝ} {L : ℝ} (hg : Good P θ dx dy L)
    (hM : P.bigMOk = true) {pr : Pair} (hpr : pr ∈ P.pairs) (o : Opt) (j : Fin 4) :
    let A := (optSqs P.sqs pr o).1
    let B := (optSqs P.sqs pr o).2
    nx (angOf θ A) o.k * ((cenOf dx dy B).1 + vx (angOf θ B) j - (cenOf dx dy A).1) +
      ny (angOf θ A) o.k * ((cenOf dx dy B).2 + vy (angOf θ B) j - (cenOf dx dy A).2) ≥
      1/2 - P.bigM := by
  intro A B
  obtain ⟨hi, hj, _, _⟩ := mem_pairs hpr
  unfold Prob.bigMOk at hM
  have hb := of_decide_eq_true (List.all_eq_true.mp hM pr hpr)
  set gx := (dIv (P.sq pr.i).rx (P.sq pr.j).rx (P.sq pr.i).x (P.sq pr.j).x).mag
  set gy := (dIv (P.sq pr.i).ry (P.sq pr.j).ry (P.sq pr.i).y (P.sq pr.j).y).mag
  have pI := hg.pos _ (P.sq_mem hi)
  have pJ := hg.pos _ (P.sq_mem hj)
  have hgx : |((P.sq pr.j).rx + dx (P.sq pr.j).s) - ((P.sq pr.i).rx + dx (P.sq pr.i).s)| ≤ (gx : ℝ) :=
    Iv.abs_le_mag (mem_dIv pI.1 pJ.1)
  have hgy : |((P.sq pr.j).ry + dy (P.sq pr.j).s) - ((P.sq pr.i).ry + dy (P.sq pr.i).s)| ≤ (gy : ℝ) :=
    Iv.abs_le_mag (mem_dIv pI.2 pJ.2)
  set Dx := (cenOf dx dy B).1 - (cenOf dx dy A).1
  set Dy := (cenOf dx dy B).2 - (cenOf dx dy A).2
  have hD : Dx^2 + Dy^2 ≤ (gx:ℝ)^2 + (gy:ℝ)^2 := by
    have hAB : (A = P.sq pr.i ∧ B = P.sq pr.j) ∨ (A = P.sq pr.j ∧ B = P.sq pr.i) := by
      simp only [A, B, optSqs, Prob.sq]; split_ifs
      · exact Or.inr ⟨rfl, rfl⟩
      · exact Or.inl ⟨rfl, rfl⟩
    have h1 := sq_abs (((P.sq pr.j).rx + dx (P.sq pr.j).s) - ((P.sq pr.i).rx + dx (P.sq pr.i).s))
    have h2 := sq_abs (((P.sq pr.j).ry + dy (P.sq pr.j).s) - ((P.sq pr.i).ry + dy (P.sq pr.i).s))
    have e1 := pow_le_pow_left₀ (abs_nonneg _) hgx 2
    have e2 := pow_le_pow_left₀ (abs_nonneg _) hgy 2
    rcases hAB with ⟨hA, hB⟩ | ⟨hA, hB⟩ <;> simp only [Dx, Dy, cenOf, hA, hB] <;> nlinarith
  have hM1 : (121/100 : ℝ) ≤ P.bigM := by
    have := (Rat.cast_le (K := ℝ)).mpr hb.1; push_cast at this; exact this
  have hM2 : (gx:ℝ)^2 + (gy:ℝ)^2 ≤ (P.bigM - 121/100)^2 := by
    have := (Rat.cast_le (K := ℝ)).mpr hb.2; push_cast at this; exact this
  set n1 := nx (angOf θ A) o.k
  set n2 := ny (angOf θ A) o.k
  have hn : n1^2 + n2^2 = 1 := by
    simp only [n1, n2, nx, ny]; rw [add_comm]; exact Real.sin_sq_add_cos_sq _
  have hv : vx (angOf θ B) j ^ 2 + vy (angOf θ B) j ^ 2 = 1/2 := by
    have h := Real.sin_sq_add_cos_sq (angOf θ B)
    have : ox j ^ 2 + oy j ^ 2 = 1/2 := by
      rw [← sq_abs (ox j), ← sq_abs (oy j), abs_ox, abs_oy]; norm_num
    simp only [vx, vy]; nlinarith
  have c1 := cs_bound n1 n2 Dx Dy
  have c2 := cs_bound n1 n2 (vx (angOf θ B) j) (vy (angOf θ B) j)
  rw [hn, one_mul] at c1 c2
  have b1 : |n1 * Dx + n2 * Dy| ≤ P.bigM - 121/100 := by
    apply abs_le_of_sq_le_sq' _ (by linarith) |>.elim (fun h1 h2 => abs_le.mpr ⟨h1, h2⟩)
    nlinarith
  have b2 : |n1 * vx (angOf θ B) j + n2 * vy (angOf θ B) j| ≤ 71/100 := by
    apply abs_le_of_sq_le_sq' _ (by norm_num) |>.elim (fun h1 h2 => abs_le.mpr ⟨h1, h2⟩)
    nlinarith
  have := neg_abs_le (n1 * Dx + n2 * Dy)
  have := neg_abs_le (n1 * vx (angOf θ B) j + n2 * vy (angOf θ B) j)
  simp only [Dx, Dy] at *
  nlinarith

theorem zb_idxOf {P : Prob} {θ dx dy : ℕ → ℝ} {pr : Pair} {p oi : ℕ}
    (hp : p < P.pairs.length) (hpr : P.pairs.getD p Pair.default = pr)
    (hm : 1 < pr.opts.length) (ho : oi < pr.opts.length) :
    zb P θ dx dy ((zinfoOf P.pairs).idxOf (p, oi)) = decide (oi = firstSep P θ dx dy pr) := by
  have hpr' : P.pairs[p] = pr := by
    rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hp] at hpr; simpa using hpr
  have hmem : (p, oi) ∈ zinfoOf P.pairs := mem_zinfo.mpr ⟨hp, by rw [hpr']; exact hm, by rw [hpr']; exact ho⟩
  unfold zb
  rw [zinfo_getD_idxOf hmem]
  simp only [hpr]

theorem pair_rows_hold {P : Prob} {θ dx dy : ℕ → ℝ} {L : ℝ} (hg : Good P θ dx dy L)
    (hM : P.bigMOk = true) {pr : Pair} {p : ℕ} (hpp : (pr, p) ∈ P.pairs.zipIdx) :
    ∀ r ∈ pairRowsOf P (zinfoOf P.pairs) P.bigM pr p, r.Holds θ (Xval P θ dx dy) L := by
  obtain ⟨hp, hpr⟩ := zipIdx_get Pair.default hpp
  have hprm : pr ∈ P.pairs := by
    rw [← hpr, List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hp]; exact List.getElem_mem hp
  obtain ⟨hi, hj, _, _⟩ := mem_pairs hprm
  obtain ⟨hfl, hfs⟩ := firstSep_spec hg hprm
  intro r hr
  unfold pairRowsOf at hr
  rcases List.mem_append.mp hr with h | h
  · simp only [List.mem_flatMap, List.mem_map, List.mem_finRange, true_and] at h
    obtain ⟨⟨o, oi⟩, hooi, j, rfl⟩ := h
    obtain ⟨hoi, hoo⟩ := zipIdx_get (⟨false, 0⟩ : Opt) hooi
    have hoo' : pr.opts[oi] = o := by
      rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hoi] at hoo; simpa using hoo
    obtain ⟨hA, hB⟩ := optSqs_cols P pr o
    have hca : (optCols pr o).1 < P.n := by unfold optCols; split_ifs <;> assumption
    have hcb : (optCols pr o).2 < P.n := by unfold optCols; split_ifs <;> assumption
    have xA := Xval_x P θ dx dy hca
    have yA := Xval_y P θ dx dy hca
    have xB := Xval_x P θ dx dy hcb
    have yB := Xval_y P θ dx dy hcb
    rw [← hA] at xA yA
    rw [← hB] at xB yB
    set A := (optSqs P.sqs pr o).1
    set B := (optSqs P.sqs pr o).2
    have hsep_of : oi = firstSep P θ dx dy pr → ∀ j : Fin 4,
        nx (angOf θ A) o.k * ((cenOf dx dy B).1 + vx (angOf θ B) j - (cenOf dx dy A).1) +
        ny (angOf θ A) o.k * ((cenOf dx dy B).2 + vy (angOf θ B) j - (cenOf dx dy A).2) ≥ 1/2 := by
      intro he j
      have h' : pr.opts[firstSep P θ dx dy pr]'hfl = o := by
        rw [← hoo']; congr 1; exact he.symm
      have := hfs
      rw [h'] at this
      exact this j
    unfold optRow
    simp only
    split_ifs with hmult
    · have hz := zb_idxOf (θ := θ) (dx := dx) (dy := dy) hp hpr hmult hoi
      have hX := Xval_z P θ dx dy ((zinfoOf P.pairs).idxOf (p, oi))
      rw [hz] at hX
      simp only [Row.Holds, List.cons_append, List.nil_append, List.map_cons, List.map_nil,
        List.sum_cons, List.sum_nil, Ex.real, nxE_real, nyE_real, vxE_real, vyE_real, xA, yA, xB, yB, hX]
      by_cases he : oi = firstSep P θ dx dy pr
      · have hs := hsep_of he j
        simp only [he, decide_true, if_true, cenOf] at hs ⊢
        push_cast; linarith
      · have hs := bigM_slack hg hM hprm o j
        simp only [he, decide_false, cenOf] at hs ⊢
        push_cast; linarith
    · have hlen : pr.opts.length ≤ 1 := by omega
      have he : oi = firstSep P θ dx dy pr := by omega
      have hs := hsep_of he j
      simp only [Row.Holds, List.map_cons, List.map_nil, List.sum_cons, List.sum_nil, Ex.real,
        nxE_real, nyE_real, vxE_real, vyE_real, xA, yA, xB, yB]
      simp only [cenOf] at hs
      push_cast; linarith
  · split_ifs at h with hmult
    · simp only [List.mem_singleton] at h
      subst h
      simp only [Row.Holds, List.map_map, Ex.real]
      have e : ((List.range pr.opts.length).map ((fun t : ℕ × Ex => t.2.real θ * Xval P θ dx dy t.1) ∘
          fun oi => (2 * P.n + (zinfoOf P.pairs).idxOf (p, oi), Ex.c (-1)))) =
          (List.range pr.opts.length).map (fun oi => (-1:ℝ) * (if oi = firstSep P θ dx dy pr then (1:ℝ) else 0)) := by
        apply List.map_congr_left
        intro oi hoi
        rw [List.mem_range] at hoi
        simp only [Function.comp, Ex.real, Xval_z, zb_idxOf hp hpr hmult hoi]
        by_cases he : oi = firstSep P θ dx dy pr <;> simp [he]
      rw [e, List.sum_map_mul_left, sum_indicator, if_pos hfl]
      push_cast; linarith
    · simp at h

end Sq19.Milp
