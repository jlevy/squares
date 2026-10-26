import Sqpack.ZMTree
import Sqpack.MixedMeasure
import Sqpack.SegTree

/-!
# `CovM`: what a pose box certifies for a mixed cover (points + segments)

The mixed-cover analogue of `BoxTree.Cov`.  A cover is a list of point entries `(X, Y, w)` (the
point `(X/D, Y/D)` with mass `w/W`) and a list of segment entries `(X0, Y0, X1, Y1, w)` (mass `w/W`
spread uniformly by length on the closed segment `(X0/D, Y0/D)–(X1/D, Y1/D)`, `SegTree.lean`).  The
mass a closed square `Q` captures is `Σ_{points in Q} w + Σ_segments w · segFrac(Q)` (over `W`), where
`segFrac` is the fraction of the segment's parameter interval mapped into `Q` (`MixedMeasure.lean`).

* `CovM` — every closed unit square inside `[0, Mq/D]²` with centre in the box and angle
  `2 arctan u`, `u` in the bin, captures mass `≥ W` (i.e. `≥ 1` after dividing by `W`).
* `CovM.splitX/Y/U` — gluing (the same one-line proofs as `Cov.split*`); `CovM.of_cov` — a point
  certificate is a mixed certificate (segment mass is `≥ 0`).
* `segD4Check`, **`le_minSide_mixed`** — the end-to-end lower bound: a D4-invariant mixed cover of
  total `< n` whose root box (the D4 fundamental region `[0, Mq/(2D)]² × u ∈ [0, 1/2]`) is covered
  proves `s(n) ≥ Mq/D`, via `MixedCover.measure_apply`, `MixedCover.d4InvM`,
  `d4_reduction_measure_u` and `not_packs_of_measure` (`MixedMeasure.lean`).
-/

open MeasureTheory Finset
open scoped ENNReal

namespace SquarePacking

namespace ZMTreeM

open BoxTree

/-- The endpoints of a segment entry, over `D`. -/
noncomputable def segA (D : ℕ) (e : SegE) : ℝ × ℝ := ((e.1 : ℝ) / D, (e.2.1 : ℝ) / D)
noncomputable def segB (D : ℕ) (e : SegE) : ℝ × ℝ := ((e.2.2.1 : ℝ) / D, (e.2.2.2.1 : ℝ) / D)

/-- The segment mass a closed square captures (weights not yet divided by `W`). -/
noncomputable def segMass (D : ℕ) (segs : List SegE) (Qs : Set (ℝ × ℝ)) : ℝ :=
  ∑ e ∈ segs.toFinset, (e.2.2.2.2 : ℝ) * segFrac (segA D e) (segB D e) Qs

open Classical in
/-- The point mass a closed square captures (weights not yet divided by `W`). -/
noncomputable def ptMass (D : ℕ) (pts : List (ℕ × ℕ × ℕ)) (Qs : Set (ℝ × ℝ)) : ℝ :=
  ∑ e ∈ pts.toFinset.filter (fun e => ptR D e ∈ Qs), (e.2.2 : ℝ)

/-- **What a mixed box-tree node certifies**: every closed unit square inside `[0, Mq/D]²` with
centre in `[x0,x1]×[y0,y1]` (over `Q = D·S`) and angle `2 arctan u`, `u ∈ [u0/R, u1/R]`, captures
point mass plus segment mass `≥ W`. -/
def CovM (D S Mq R W : ℕ) (pts : List (ℕ × ℕ × ℕ)) (segs : List SegE)
    (x0 x1 y0 y1 u0 u1 : ℕ) : Prop :=
  ∀ (c : ℝ × ℝ) (u : ℝ),
    (x0 : ℝ) / (D * S) ≤ c.1 → c.1 ≤ (x1 : ℝ) / (D * S) →
    (y0 : ℝ) / (D * S) ≤ c.2 → c.2 ≤ (y1 : ℝ) / (D * S) →
    (u0 : ℝ) / R ≤ u → u ≤ (u1 : ℝ) / R →
    sq c (2 * Real.arctan u) 1 ⊆ box ((Mq : ℝ) / D) →
    (W : ℝ) ≤ ptMass D pts (sq c (2 * Real.arctan u) 1) + segMass D segs (sq c (2 * Real.arctan u) 1)

variable {D S Mq R W : ℕ} {pts : List (ℕ × ℕ × ℕ)} {segs : List SegE} {x0 x1 y0 y1 u0 u1 : ℕ}

theorem CovM.splitX (m : ℕ) (h1 : CovM D S Mq R W pts segs x0 m y0 y1 u0 u1)
    (h2 : CovM D S Mq R W pts segs m x1 y0 y1 u0 u1) : CovM D S Mq R W pts segs x0 x1 y0 y1 u0 u1 := by
  intro c u hx0 hx1 hy0 hy1 hu0 hu1 hsub
  rcases le_total c.1 ((m : ℝ) / (D * S)) with h | h
  · exact h1 c u hx0 h hy0 hy1 hu0 hu1 hsub
  · exact h2 c u h hx1 hy0 hy1 hu0 hu1 hsub

theorem CovM.splitY (m : ℕ) (h1 : CovM D S Mq R W pts segs x0 x1 y0 m u0 u1)
    (h2 : CovM D S Mq R W pts segs x0 x1 m y1 u0 u1) : CovM D S Mq R W pts segs x0 x1 y0 y1 u0 u1 := by
  intro c u hx0 hx1 hy0 hy1 hu0 hu1 hsub
  rcases le_total c.2 ((m : ℝ) / (D * S)) with h | h
  · exact h1 c u hx0 hx1 hy0 h hu0 hu1 hsub
  · exact h2 c u hx0 hx1 h hy1 hu0 hu1 hsub

theorem CovM.splitU (m : ℕ) (h1 : CovM D S Mq R W pts segs x0 x1 y0 y1 u0 m)
    (h2 : CovM D S Mq R W pts segs x0 x1 y0 y1 m u1) : CovM D S Mq R W pts segs x0 x1 y0 y1 u0 u1 := by
  intro c u hx0 hx1 hy0 hy1 hu0 hu1 hsub
  rcases le_total u ((m : ℝ) / R) with h | h
  · exact h1 c u hx0 hx1 hy0 hy1 hu0 h hsub
  · exact h2 c u hx0 hx1 hy0 hy1 h hu1 hsub

lemma segFrac_nonneg (a b : ℝ × ℝ) (Qs : Set (ℝ × ℝ)) : 0 ≤ segFrac a b Qs := ENNReal.toReal_nonneg

lemma segMass_nonneg (D : ℕ) (segs : List SegE) (Qs : Set (ℝ × ℝ)) : 0 ≤ segMass D segs Qs :=
  Finset.sum_nonneg fun _ _ => mul_nonneg (Nat.cast_nonneg _) (segFrac_nonneg _ _ _)

/-- A point certificate is a mixed certificate. -/
theorem CovM.of_cov (h : Cov D S Mq R W pts x0 x1 y0 y1 u0 u1) :
    CovM D S Mq R W pts segs x0 x1 y0 y1 u0 u1 := by
  intro c u hx0 hx1 hy0 hy1 hu0 hu1 hsub
  have := h c u hx0 hx1 hy0 hy1 hu0 hu1 hsub
  have h0 := segMass_nonneg D segs (sq c (2 * Real.arctan u) 1)
  unfold ptMass
  linarith

/-! ## The D4 data check for segments -/

/-- The images of a segment entry under `x ↦ Mq − x` and `x ↔ y` (re-normalised). -/
def sXg (Mq : ℕ) (e : SegE) : SegE := segNorm (Mq - e.1, e.2.1, Mq - e.2.2.1, e.2.2.2.1, e.2.2.2.2)
def sSg (e : SegE) : SegE := segNorm (e.2.1, e.1, e.2.2.2.1, e.2.2.1, e.2.2.2.2)

/-- The segment data check: keys strictly increasing (no repeated entry); every entry stored
normalised, with `X0, X1 ≤ Mq`, and its two reflections (normalised), with the same mass, are
entries. -/
def segD4Check (Mq : ℕ) (segs : STree) : Bool :=
  STree.chainB segs.toList &&
    segs.all (fun e => ptLt e.1 e.2.1 e.2.2.1 e.2.2.2.1 && Nat.ble e.1 Mq && Nat.ble e.2.2.1 Mq &&
      segs.mem (sXg Mq e) && segs.mem (sSg e))

lemma sXg_eq (Mq D : ℕ) (e : SegE) (h : ptLt e.1 e.2.1 e.2.2.1 e.2.2.2.1 = true) (ha : e.1 ≤ Mq)
    (hc : e.2.2.1 ≤ Mq) :
    sXg Mq (sXg Mq e) = e ∧ (sXg Mq e).2.2.2.2 = e.2.2.2.2 ∧
      ((segA D (sXg Mq e) = reflX ((Mq : ℝ) / D) (segA D e) ∧
          segB D (sXg Mq e) = reflX ((Mq : ℝ) / D) (segB D e)) ∨
        (segA D (sXg Mq e) = reflX ((Mq : ℝ) / D) (segB D e) ∧
          segB D (sXg Mq e) = reflX ((Mq : ℝ) / D) (segA D e))) := by
  obtain ⟨a, b, c, d, w⟩ := e
  simp only [ptLt_iff] at h
  simp only at ha hc
  have hA : ((Mq - a : ℕ) : ℝ) = Mq - a := by rw [Nat.cast_sub ha]
  have hC : ((Mq - c : ℕ) : ℝ) = Mq - c := by rw [Nat.cast_sub hc]
  by_cases h1 : ptLt (Mq - a) b (Mq - c) d = true
  · have e1 : sXg Mq (a, b, c, d, w) = (Mq - a, b, Mq - c, d, w) := by
      simp only [sXg, segNorm, h1, if_true]
    have e2 : sXg Mq (Mq - a, b, Mq - c, d, w) = (a, b, c, d, w) := by
      have h2 : ptLt (Mq - (Mq - a)) b (Mq - (Mq - c)) d = true := by
        rw [ptLt_iff]; omega
      simp only [sXg, segNorm, h2, if_true]
      ext <;> simp <;> omega
    refine ⟨by rw [e1, e2], by rw [e1], Or.inl ⟨?_, ?_⟩⟩
    · rw [e1]; simp only [segA, reflX, hA]; ext <;> simp; ring
    · rw [e1]; simp only [segB, reflX, hC]; ext <;> simp; ring
  · have e1 : sXg Mq (a, b, c, d, w) = (Mq - c, d, Mq - a, b, w) := by
      simp only [sXg, segNorm, h1, if_false, Bool.false_eq_true]
    have e2 : sXg Mq (Mq - c, d, Mq - a, b, w) = (a, b, c, d, w) := by
      have h2 : ¬ ptLt (Mq - (Mq - c)) d (Mq - (Mq - a)) b = true := by
        rw [ptLt_iff]; omega
      simp only [sXg, segNorm, h2, if_false, Bool.false_eq_true]
      ext <;> simp <;> omega
    refine ⟨by rw [e1, e2], by rw [e1], Or.inr ⟨?_, ?_⟩⟩
    · rw [e1]; simp only [segA, segB, reflX, hC]; ext <;> simp; ring
    · rw [e1]; simp only [segA, segB, reflX, hA]; ext <;> simp; ring

lemma sSg_eq (D : ℕ) (e : SegE) (h : ptLt e.1 e.2.1 e.2.2.1 e.2.2.2.1 = true) :
    sSg (sSg e) = e ∧ (sSg e).2.2.2.2 = e.2.2.2.2 ∧
      ((segA D (sSg e) = swapXY (segA D e) ∧ segB D (sSg e) = swapXY (segB D e)) ∨
        (segA D (sSg e) = swapXY (segB D e) ∧ segB D (sSg e) = swapXY (segA D e))) := by
  obtain ⟨a, b, c, d, w⟩ := e
  simp only [ptLt_iff] at h
  by_cases h1 : ptLt b a d c = true
  · have e1 : sSg (a, b, c, d, w) = (b, a, d, c, w) := by
      simp only [sSg, segNorm, h1, if_true]
    have e2 : sSg (b, a, d, c, w) = (a, b, c, d, w) := by
      have h2 : ptLt a b c d = true := by rw [ptLt_iff]; omega
      simp only [sSg, segNorm, h2, if_true]
    exact ⟨by rw [e1, e2], by rw [e1], Or.inl ⟨by rw [e1]; rfl, by rw [e1]; rfl⟩⟩
  · have e1 : sSg (a, b, c, d, w) = (d, c, b, a, w) := by
      simp only [sSg, segNorm, h1, if_false, Bool.false_eq_true]
    have e2 : sSg (d, c, b, a, w) = (a, b, c, d, w) := by
      have h2 : ¬ ptLt c d a b = true := by rw [ptLt_iff]; omega
      simp only [sSg, segNorm, h2, if_false, Bool.false_eq_true]
    exact ⟨by rw [e1, e2], by rw [e1], Or.inr ⟨by rw [e1]; rfl, by rw [e1]; rfl⟩⟩

/-! ## The end-to-end lower bound -/

/-- The mixed cover of the data, as a `MixedCover` (no polygons). -/
noncomputable def mcover (D W : ℕ) (pts : PTree) (segs : STree) :
    MixedCover (ℕ × ℕ × ℕ) SegE Empty where
  pts := pts.toList.toFinset
  pt := ptR D
  pw := fun e => (e.2.2 : ℝ) / W
  segs := segs.toList.toFinset
  sa := segA D
  sb := segB D
  sw := fun e => (e.2.2.2.2 : ℝ) / W
  polys := ∅
  poly := fun _ => ∅
  gw := fun _ => 0

/-- **The generic lower bound from a mixed cover.**  A mixed cover (points `pts`, segments `segs`),
D4-invariant in `[0, Mq/D]²`, with total weight `< n` (over `W`), whose root box covers the D4
fundamental region `[0, Mq/(2D)]² × {u ∈ [0, Um/R]}` (`Um/R ≥ 1/2`) in the sense of `CovM`, proves
`s(n) ≥ Mq/D`. -/
theorem le_minSide_mixed (D S Mq R Um W : ℕ) (pts : PTree) (segs : STree) (hD : 0 < D) (hS : 0 < S)
    (hR : 0 < R) (hUm : R ≤ 2 * Um) (hnd : pts.toList.Nodup) (hsym : d4Check Mq pts = true)
    (hssym : segD4Check Mq segs = true)
    (hcov : CovM D S Mq R W pts.toList segs.toList 0 (Mq * S - Mq * S / 2) 0 (Mq * S - Mq * S / 2)
      0 Um)
    (n k : ℕ) (hn : pts.wsum + segs.wsum < n * W) (hk : n ≤ k * k) :
    (Mq : ℝ) / D ≤ minSide n := by
  classical
  set m : ℝ := (Mq : ℝ) / D with hm
  set M := mcover D W pts segs with hMdef
  have hW : 0 < W := by
    rcases Nat.eq_zero_or_pos W with h | h
    · rw [h] at hn; simp at hn
    · exact h
  have hWr : (0 : ℝ) < W := by exact_mod_cast hW
  have hDr : (0 : ℝ) < D := by exact_mod_cast hD
  have hSr : (0 : ℝ) < S := by exact_mod_cast hS
  have hRr : (0 : ℝ) < R := by exact_mod_cast hR
  -- the data facts
  simp only [segD4Check, Bool.and_eq_true] at hssym
  obtain ⟨hschain, hsall⟩ := hssym
  have hsnd : segs.toList.Nodup := STree.nodup_of_chainB _ hschain
  have pentry_ok : ∀ e ∈ pts.toList.toFinset,
      e.1 ≤ Mq ∧ (Mq - e.1, e.2.1, e.2.2) ∈ pts.toList.toFinset ∧
        (e.2.1, e.1, e.2.2) ∈ pts.toList.toFinset := by
    intro e he
    have h2 := (PTree.all_iff _ pts).mp hsym e (List.mem_toFinset.mp he)
    simp only [Bool.and_eq_true, Nat.ble_eq] at h2
    exact ⟨h2.1.1, List.mem_toFinset.mpr (PTree.mem_sound _ _ h2.1.2),
      List.mem_toFinset.mpr (PTree.mem_sound _ _ h2.2)⟩
  have sentry_ok : ∀ e ∈ segs.toList.toFinset,
      ptLt e.1 e.2.1 e.2.2.1 e.2.2.2.1 = true ∧ e.1 ≤ Mq ∧ e.2.2.1 ≤ Mq ∧
        sXg Mq e ∈ segs.toList.toFinset ∧ sSg e ∈ segs.toList.toFinset := by
    intro e he
    have h2 := (STree.all_iff _ segs).mp hsall e (List.mem_toFinset.mp he)
    simp only [Bool.and_eq_true, Nat.ble_eq] at h2
    exact ⟨h2.1.1.1.1, h2.1.1.1.2, h2.1.1.2, List.mem_toFinset.mpr (STree.mem_sound _ _ h2.1.2),
      List.mem_toFinset.mpr (STree.mem_sound _ _ h2.2)⟩
  have hnonneg : M.Nonneg :=
    ⟨fun _ _ => by simp only [hMdef, mcover]; positivity,
     fun _ _ => by simp only [hMdef, mcover]; positivity,
     fun k _ => k.elim⟩
  -- D4 invariance of the measure
  have hinv : D4InvM m M.measure := by
    refine M.d4InvM m (fun k => k.elim) (fun e => (Mq - e.1, e.2.1, e.2.2))
      (fun e => (e.2.1, e.1, e.2.2)) (sXg Mq) sSg id id ?_ ?_ (fun k => k.elim) ?_ ?_
      fun k => k.elim
    · intro e he
      obtain ⟨hx, hpX, _⟩ := pentry_ok e he
      refine ⟨hpX, ?_, rfl, ?_⟩
      · change ptR D (Mq - e.1, e.2.1, e.2.2) = reflX m (ptR D e)
        simp only [ptR, reflX, hm, Nat.cast_sub hx]
        ext
        · simp only; field_simp
        · simp
      · obtain ⟨a, b, c⟩ := e
        simp only at hx ⊢
        ext <;> simp; omega
    · intro e he
      obtain ⟨h, ha, hc, hsX, _⟩ := sentry_ok e he
      obtain ⟨h1, h2, h3⟩ := sXg_eq Mq D e h ha hc
      refine ⟨hsX, ?_, h1, h3⟩
      change ((sXg Mq e).2.2.2.2 : ℝ) / W = (e.2.2.2.2 : ℝ) / W
      rw [h2]
    · intro e he
      exact ⟨(pentry_ok e he).2.2, rfl, rfl, rfl⟩
    · intro e he
      obtain ⟨h, _, _, _, hsS⟩ := sentry_ok e he
      obtain ⟨h1, h2, h3⟩ := sSg_eq D e h
      refine ⟨hsS, ?_, h1, h3⟩
      change ((sSg e).2.2.2.2 : ℝ) / W = (e.2.2.2.2 : ℝ) / W
      rw [h2]
  -- the measure of a square is the mass
  have hmass : ∀ (Qs : Set (ℝ × ℝ)), MeasurableSet Qs →
      M.measure Qs = ENNReal.ofReal ((ptMass D pts.toList Qs + segMass D segs.toList Qs) / W) := by
    intro Qs hQs
    rw [M.measure_apply hnonneg hQs]
    congr 1
    simp only [MixedCover.mass, hMdef, mcover, Finset.sum_empty, add_zero, ptMass, segMass]
    rw [add_div, Finset.sum_div, Finset.sum_div]
    congr 1
    refine Finset.sum_congr rfl fun e _ => ?_
    ring
  -- the region statement, from the tree
  have hcover : ∀ (c : ℝ × ℝ) (θ : ℝ), sq c θ 1 ⊆ box m → 1 ≤ M.measure (sq c θ 1) := by
    refine d4_reduction_measure_u m M.measure hinv fun c u h1 h2 hu hsub => ?_
    rw [hmass _ (measurableSet_sq _ _ _), ← ENNReal.ofReal_one]
    apply ENNReal.ofReal_le_ofReal
    have hhalf : m / 2 ≤ (((Mq * S - Mq * S / 2 : ℕ) : ℝ)) / (D * S) := by
      have h2 : Mq * S ≤ 2 * (Mq * S - Mq * S / 2) := by omega
      have h2r : ((Mq * S : ℕ) : ℝ) ≤ 2 * ((Mq * S - Mq * S / 2 : ℕ) : ℝ) := by exact_mod_cast h2
      rw [hm, div_div, div_le_div_iff₀ (by positivity) (by positivity)]
      push_cast at h2r
      nlinarith
    have hU : ((0 : ℕ) : ℝ) / R ≤ u := by simpa using hu.1
    have hU1 : u ≤ (Um : ℝ) / R := by
      rw [le_div_iff₀ hRr]
      have : (R : ℝ) ≤ 2 * Um := by exact_mod_cast hUm
      nlinarith [hu.2]
    have hc := hcov c u (by simpa using h1.1) (le_trans h1.2 hhalf) (by simpa using h2.1)
      (le_trans h2.2 hhalf) hU hU1 hsub
    rw [le_div_iff₀ hWr, one_mul]
    exact hc
  -- the total
  have htot : M.measure (box m) < n := by
    have h1 : M.measure (box m) ≤ ENNReal.ofReal M.total :=
      (measure_mono (Set.subset_univ _)).trans (M.measure_univ_le hnonneg)
    have hsum : M.total = ((pts.wsum : ℝ) + segs.wsum) / W := by
      have hp : ∑ e ∈ pts.toList.toFinset, (e.2.2 : ℝ) = pts.wsum := by
        have : ∑ e ∈ pts.toList.toFinset, e.2.2 = pts.wsum := by
          rw [List.sum_toFinset _ hnd, PTree.wsum_eq]
        rw [← this]; push_cast; rfl
      have hs : ∑ e ∈ segs.toList.toFinset, (e.2.2.2.2 : ℝ) = segs.wsum := by
        have : ∑ e ∈ segs.toList.toFinset, e.2.2.2.2 = segs.wsum := by
          rw [List.sum_toFinset _ hsnd, STree.wsum_eq]
        rw [← this]; push_cast; rfl
      simp only [MixedCover.total, hMdef, mcover, Finset.sum_empty, add_zero]
      rw [← Finset.sum_div, ← Finset.sum_div, hp, hs, add_div]
    have h2 : ENNReal.ofReal M.total < n := by
      rw [hsum]
      have hlt : ((pts.wsum : ℝ) + segs.wsum) < n * W := by exact_mod_cast hn
      have : ((pts.wsum : ℝ) + segs.wsum) / W < n := by rw [div_lt_iff₀ hWr]; exact hlt
      have hn0 : (0 : ℝ) < n := lt_of_le_of_lt (by positivity) this
      calc ENNReal.ofReal (((pts.wsum : ℝ) + segs.wsum) / W) < ENNReal.ofReal n :=
            (ENNReal.ofReal_lt_ofReal_iff hn0).mpr this
        _ = n := ENNReal.ofReal_natCast n
    exact h1.trans_lt h2
  -- `s(n)`
  have hne : ({s | Packs n s} : Set ℝ).Nonempty := ⟨k, packs_grid k n hk⟩
  refine le_csInf hne fun s hs => ?_
  by_contra hlt
  exact not_packs_of_measure m M.measure hcover n htot (not_le.mp hlt) hs

end ZMTreeM

end SquarePacking
