import Sqpack.Bentz

/-!
# Fixed-profile families of edge-zone width `R`: the all-`k` reduction, generically

`Bentz.lean` proves `s(k² − 3) = k` (`k ≥ 6`) from one finite hypothesis on a box cover of `[0,7]²`,
for the family `R = w = 2`.  This file is the same argument for a family of any edge-zone width `R`
(pitch `1/5`), so that `k² − 4` (`R = 3`, box `9`, `Bentz4.lean`) and later families are only data
plus a few lines.

* `Fam` — the family data: `R`, the Lebesgue corner `A/5`, the mass denominator `den`, and two code
  tables `tab`, `tab2` (`5R + 7` columns).  `famCover F k` is its measure `μ_k` on `[0,k]²`: unit
  segments of the `1/5`-grid in two *layers*, the mass of a segment depending only on its layer and
  the codes of its cell and line (`cellT`, `lineT`: offset from the nearer wall in the edge zones,
  phase in the band zone, a separate code for the band's closed ends `R`, `k − R`); plus Lebesgue on
  `[A/5, k − A/5]²`.  (Two layers because a box file may list two entries for one unit segment — the
  corner module and the profile both put mass on the band's end lines.)
* `fileCover` — a FORMAT.md v1 box file (no points, unit segments, one polygon) verbatim, as a
  `MixedCover`.
* `fileCover_measure` — if three kernel-checkable list conditions hold (every entry is a unit grid
  segment carrying the family's mass in one of the layers, no (segment, layer) twice, every
  (segment, layer) of `[0,K]²` with non-zero mass is listed) and the polygon is the Lebesgue square,
  the file's measure **is** `famCover F K`.
* `mass_shift` — localisation: for `k ≥ 2R + 2`, every closed unit square in `[0,k]²` has the
  `μ_k`-mass of an integer translate of it in `[0, 2R + 3]²` under `μ_{2R+3}`.
* `seg_total` — accounting: the segment mass of `μ_k`, `k = m + 2R + 1`, is a polynomial in `m`
  whose coefficients are explicit finite sums over the tables (evaluated by the kernel per
  instance).
* `minSide_eq` — the end: box validity for `μ_{2R+3}` and `total(μ_k) < n ≤ k²` give
  `minSide n = k`.

The shared geometry (`segA`, `segB`, shifts, `segFrac` translation invariance, `wid θ < 2`) is
reused from `Bentz.lean`.  `notes/lean-k2m4-reduction.md`.
-/

open MeasureTheory Finset
open scoped ENNReal

namespace SquarePacking
namespace BentzFam

open Bentz (SegIx segA segB idx mem_idx convPoly)

/-! ## 1.  Families -/

/-- A fixed-profile family of edge-zone width `R` on the `1/5`-grid: Lebesgue from `A/5`, masses in
units `1/den`, code tables `tab` (layer 1) and `tab2` (layer 2), each `(5R + 7) × (5R + 7)` as a
list of rows (read with default `0`). -/
structure Fam where
  R : ℕ
  A : ℕ
  den : ℕ
  tab : List (List ℕ)
  tab2 : List (List ℕ)

/-- The code of the cell `[i/5, (i+1)/5]` in `[0,k]`: offset `0..5R−1` from the nearer wall in the
edge zones, `5R + phase` in the band zone `[R, k − R]`, `5R + 6` outside `[0,k]`. -/
def cellT (R k : ℕ) (i : ℤ) : ℤ :=
  if i < 0 ∨ 5 * (k : ℤ) ≤ i then 5 * (R : ℤ) + 6
  else if i < 5 * (R : ℤ) then i
  else if 5 * (k : ℤ) - 5 * (R : ℤ) ≤ i then 5 * (k : ℤ) - 1 - i
  else 5 * (R : ℤ) + i % 5

/-- The code of the line `j/5` in `[0,k]`: offset `0..5R` from the nearer wall (offset `5R`: the
band's closed ends `R`, `k − R`), `5R + 1 + phase` in the open band zone, `5R + 6` outside
`[0,k]`. -/
def lineT (R k : ℕ) (j : ℤ) : ℤ :=
  if j < 0 ∨ 5 * (k : ℤ) < j then 5 * (R : ℤ) + 6
  else if j ≤ 5 * (R : ℤ) then j
  else if 5 * (k : ℤ) - 5 * (R : ℤ) ≤ j then 5 * (k : ℤ) - j
  else 5 * (R : ℤ) + 1 + j % 5

/-- A table entry. -/
def tabW (t : List (List ℕ)) (c l : ℤ) : ℕ := (t.getD c.toNat []).getD l.toNat 0

/-- The table of a layer. -/
def Fam.layer (F : Fam) (b : Bool) : List (List ℕ) := if b then F.tab2 else F.tab

/-- Family segment indices: (unit segment, layer). -/
abbrev FIx := SegIx × Bool

/-- The mass of a layer of a unit segment in `μ_k`, in units `1/den` (horizontal: code of the x-cell
and of the y-line; vertical: the diagonal image). -/
def wN (F : Fam) (k : ℕ) (s : FIx) : ℕ :=
  if s.1.1 then tabW (F.layer s.2) (cellT F.R k s.1.2.2) (lineT F.R k s.1.2.1)
  else tabW (F.layer s.2) (cellT F.R k s.1.2.1) (lineT F.R k s.1.2.2)

/-- The (segment, layer) indices of `[0,k]²`. -/
def grid (k : ℕ) : Finset FIx := (univ ×ˢ (idx k ×ˢ idx k)) ×ˢ univ

/-- The Lebesgue square `[A/5, k − A/5]²`. -/
def lebSq (A k : ℕ) : Set (ℝ × ℝ) :=
  Set.Icc ((A : ℝ) / 5) ((k : ℝ) - A / 5) ×ˢ Set.Icc ((A : ℝ) / 5) ((k : ℝ) - A / 5)

/-- **The family measure `μ_k` on `[0,k]²`**, as a mixed cover. -/
noncomputable def famCover (F : Fam) (k : ℕ) : MixedCover Empty FIx Unit where
  pts := ∅
  pt := fun e => e.elim
  pw := fun e => e.elim
  segs := grid k
  sa := fun s => segA s.1
  sb := fun s => segB s.1
  sw := fun s => (wN F k s : ℝ) / F.den
  polys := univ
  poly := fun _ => lebSq F.A k
  gw := fun _ => ((k : ℝ) - 2 * F.A / 5) ^ 2

/-- The tables vanish on the `outside` row and column. -/
def OutZero (F : Fam) : Prop :=
  ∀ b : Bool, ∀ n, n < 5 * F.R + 7 →
    ((F.layer b).getD (5 * F.R + 6) []).getD n 0 = 0 ∧
      ((F.layer b).getD n []).getD (5 * F.R + 6) 0 = 0

instance (F : Fam) : Decidable (OutZero F) := by unfold OutZero; infer_instance

/-! ## 2.  A box file as a mixed cover -/

/-- **A box file** (FORMAT.md v1, coordinates `X/5`, masses `w/den`), verbatim: no points; the
segments `segs` (`(X0/5, Y0/5)`–`(X1/5, Y1/5)`, mass `w/den` spread uniformly by length) indexed by
their position in the list; the one polygon with vertices `verts` and mass `pw/den` spread uniformly
by area. -/
noncomputable def fileCover (den : ℕ) (segs : List (ℕ × ℕ × ℕ × ℕ × ℕ)) (verts : List (ℕ × ℕ))
    (pw : ℕ) :
    MixedCover Empty (Fin segs.length) Unit where
  pts := ∅
  pt := fun e => e.elim
  pw := fun e => e.elim
  segs := univ
  sa := fun j => (((segs.get j).1 : ℝ) / 5, ((segs.get j).2.1 : ℝ) / 5)
  sb := fun j => (((segs.get j).2.2.1 : ℝ) / 5, ((segs.get j).2.2.2.1 : ℝ) / 5)
  sw := fun j => ((segs.get j).2.2.2.2 : ℝ) / den
  polys := univ
  poly := fun _ => convPoly 5 verts
  gw := fun _ => (pw : ℝ) / den

/-- The (segment, layer) of a file entry: layer 1 if the entry carries the layer-1 mass, else layer
2. -/
def fileIx (F : Fam) (K : ℕ) (e : ℕ × ℕ × ℕ × ℕ × ℕ) : FIx :=
  (Bentz.fileIx e, wN F K (Bentz.fileIx e, false) != e.2.2.2.2)

/-- A file entry is a unit segment of the `1/5`-grid. -/
def segGeom (e : ℕ × ℕ × ℕ × ℕ × ℕ) : Bool :=
  (e.2.1 == e.2.2.2.1 && (e.2.2.1 == e.1 + 1 || e.1 == e.2.2.1 + 1)) ||
    (e.1 == e.2.2.1 && (e.2.2.2.1 == e.2.1 + 1 || e.2.1 == e.2.2.2.1 + 1))

/-- A file entry is a unit grid segment with positive mass equal to the family's in its layer. -/
def segOK (F : Fam) (K : ℕ) (e : ℕ × ℕ × ℕ × ℕ × ℕ) : Bool :=
  segGeom e && (0 < e.2.2.2.2 && wN F K (fileIx F K e) == e.2.2.2.2)

/-! The bijection between file entries and the non-zero (segment, layer)s of `[0,K]²` is checked
through sorted natural-number keys, in `O(n log n)` kernel steps (a pairwise `Nodup` / `contains`
check is quadratic and too slow for 2000+ entries): the keys of the file entries, merge-sorted, must
be exactly the keys of the non-zero grid entries enumerated in lexicographic order, and that list
must be strictly increasing. -/

/-- The key of a (segment, layer); injective on `grid K` for `5K < 4096` (`keyN_inj`). -/
def keyN (s : FIx) : ℕ :=
  ((s.1.1.toNat * 4096 + s.1.2.1.toNat) * 4096 + s.1.2.2.toNat) * 2 + s.2.toNat

/-- All (segment, layer)s of `[0,K]²`, in lexicographic order. -/
def gridList (K : ℕ) : List FIx :=
  [false, true].flatMap fun o => (List.range (5 * K + 1)).flatMap fun (i : ℕ) =>
    (List.range (5 * K + 1)).flatMap fun (j : ℕ) =>
      [false, true].map fun b => ((o, (i : ℤ), (j : ℤ)), b)

/-- The keys of the (segment, layer)s of `[0,K]²` with non-zero mass, in lexicographic order. -/
def gridKeys (F : Fam) (K : ℕ) : List ℕ := ((gridList K).filter fun s => wN F K s != 0).map keyN

/-- Merge with fuel. -/
def mergeF : ℕ → List ℕ → List ℕ → List ℕ
  | 0, xs, ys => xs ++ ys
  | _ + 1, [], ys => ys
  | _ + 1, x :: xs, [] => x :: xs
  | f + 1, x :: xs, y :: ys =>
    if Nat.ble x y then x :: mergeF f xs (y :: ys) else y :: mergeF f (x :: xs) ys

/-- Split into the elements at even and at odd positions. -/
def splitAlt : List ℕ → List ℕ × List ℕ
  | [] => ([], [])
  | [a] => ([a], [])
  | a :: b :: l => match splitAlt l with
    | (x, y) => (a :: x, b :: y)

/-- Merge sort with fuel (depth `f`). -/
def msort : ℕ → List ℕ → List ℕ
  | 0, xs => xs
  | _ + 1, [] => []
  | _ + 1, [a] => [a]
  | f + 1, a :: b :: l => match splitAlt (a :: b :: l) with
    | (x, y) => mergeF (l.length + 2) (msort f x) (msort f y)

/-- Strictly increasing after `a`. -/
def strictAux (a : ℕ) : List ℕ → Bool
  | [] => true
  | b :: l => Nat.blt a b && strictAux b l

/-- Strictly increasing. -/
def strictB : List ℕ → Bool
  | [] => true
  | a :: l => strictAux a l

lemma mergeF_perm : ∀ (f : ℕ) (xs ys : List ℕ), (mergeF f xs ys).Perm (xs ++ ys)
  | 0, xs, ys => by simp [mergeF]
  | _ + 1, [], ys => by simp [mergeF]
  | _ + 1, x :: xs, [] => by simp [mergeF]
  | f + 1, x :: xs, y :: ys => by
    simp only [mergeF]
    split
    · exact (mergeF_perm f xs (y :: ys)).cons x
    · exact ((mergeF_perm f (x :: xs) ys).cons y).trans List.perm_middle.symm

lemma splitAlt_perm : ∀ l : List ℕ, ((splitAlt l).1 ++ (splitAlt l).2).Perm l
  | [] => by simp [splitAlt]
  | [a] => by simp [splitAlt]
  | a :: b :: l => by
    have ih := splitAlt_perm l
    rcases hl : splitAlt l with ⟨x, y⟩
    rw [hl] at ih
    simp only [splitAlt, hl, List.cons_append]
    exact ((List.perm_middle.trans (ih.cons b))).cons a

lemma msort_perm : ∀ (f : ℕ) (l : List ℕ), (msort f l).Perm l
  | 0, l => by simp [msort]
  | _ + 1, [] => by simp [msort]
  | _ + 1, [a] => by simp [msort]
  | f + 1, a :: b :: l => by
    have hp := splitAlt_perm (a :: b :: l)
    rcases hs : splitAlt (a :: b :: l) with ⟨x, y⟩
    rw [hs] at hp
    simp only [msort, hs]
    exact (mergeF_perm _ _ _).trans (((msort_perm f x).append (msort_perm f y)).trans hp)

lemma strictAux_spec : ∀ (a : ℕ) (l : List ℕ), strictAux a l = true → (∀ x ∈ l, a < x) ∧ l.Nodup
  | _, [] => by simp
  | a, b :: l => by
    intro h
    simp only [strictAux, Bool.and_eq_true, Nat.blt_eq] at h
    obtain ⟨h1, h2⟩ := strictAux_spec b l h.2
    refine ⟨?_, List.nodup_cons.mpr ⟨fun hb => lt_irrefl b (h1 b hb), h2⟩⟩
    intro x hx
    rcases List.mem_cons.mp hx with rfl | hx
    · exact h.1
    · exact h.1.trans (h1 x hx)

lemma strictB_nodup : ∀ l : List ℕ, strictB l = true → l.Nodup
  | [] => fun _ => List.nodup_nil
  | a :: l => fun h => by
    obtain ⟨h1, h2⟩ := strictAux_spec a l h
    exact List.nodup_cons.mpr ⟨fun ha => lt_irrefl a (h1 a ha), h2⟩

lemma seg_of_geom (e : ℕ × ℕ × ℕ × ℕ × ℕ) (h : segGeom e = true) :
    segMeasure ((e.1 : ℝ) / 5, (e.2.1 : ℝ) / 5) ((e.2.2.1 : ℝ) / 5, (e.2.2.2.1 : ℝ) / 5)
      = segMeasure (segA (Bentz.fileIx e)) (segB (Bentz.fileIx e)) := by
  obtain ⟨a, b, c, d, w⟩ := e
  simp only [segGeom, Bool.and_eq_true, Bool.or_eq_true, beq_iff_eq] at h
  rcases h with ⟨rfl, rfl | rfl⟩ | ⟨rfl, rfl | rfl⟩
  · simp [Bentz.fileIx, segA, segB]
  · rw [segMeasure_comm]; simp [Bentz.fileIx, segA, segB]
  · simp [Bentz.fileIx, segA, segB]
  · rw [segMeasure_comm]; simp [Bentz.fileIx, segA, segB]

/-! ## 3.  Codes, and the support of `μ_k` -/

lemma cellT_range (R k : ℕ) (i : ℤ) : 0 ≤ cellT R k i ∧ cellT R k i ≤ 5 * (R : ℤ) + 6 := by
  unfold cellT; split_ifs <;> omega

lemma lineT_range (R k : ℕ) (j : ℤ) : 0 ≤ lineT R k j ∧ lineT R k j ≤ 5 * (R : ℤ) + 6 := by
  unfold lineT; split_ifs <;> omega

lemma tabW_out_left {F : Fam} (h : OutZero F) (b : Bool) (l : ℤ)
    (hl : 0 ≤ l ∧ l ≤ 5 * (F.R : ℤ) + 6) :
    tabW (F.layer b) (5 * (F.R : ℤ) + 6) l = 0 := by
  unfold tabW
  rw [show (5 * (F.R : ℤ) + 6).toNat = 5 * F.R + 6 by omega]
  exact (h b l.toNat (by omega)).1

lemma tabW_out_right {F : Fam} (h : OutZero F) (b : Bool) (c : ℤ)
    (hc : 0 ≤ c ∧ c ≤ 5 * (F.R : ℤ) + 6) :
    tabW (F.layer b) c (5 * (F.R : ℤ) + 6) = 0 := by
  unfold tabW
  rw [show (5 * (F.R : ℤ) + 6).toNat = 5 * F.R + 6 by omega]
  exact (h b c.toNat (by omega)).2

lemma mem_grid {k : ℕ} {s : FIx} :
    s ∈ grid k ↔ (0 ≤ s.1.2.1 ∧ s.1.2.1 ≤ 5 * (k : ℤ)) ∧ (0 ≤ s.1.2.2 ∧ s.1.2.2 ≤ 5 * (k : ℤ)) := by
  simp only [grid, mem_product, mem_univ, true_and, and_true, mem_idx]

lemma cellT_out {R k : ℕ} {i : ℤ} (h : ¬ (0 ≤ i ∧ i ≤ 5 * (k : ℤ))) :
    cellT R k i = 5 * (R : ℤ) + 6 := by
  unfold cellT; split_ifs <;> omega

lemma lineT_out {R k : ℕ} {j : ℤ} (h : ¬ (0 ≤ j ∧ j ≤ 5 * (k : ℤ))) :
    lineT R k j = 5 * (R : ℤ) + 6 := by
  unfold lineT; split_ifs <;> omega

/-- The masses vanish off the grid. -/
lemma wN_eq_zero {F : Fam} (hF : OutZero F) {k : ℕ} {s : FIx} (hs : s ∉ grid k) : wN F k s = 0 := by
  rw [mem_grid, not_and_or] at hs
  obtain ⟨⟨o, i, j⟩, b⟩ := s
  cases o <;> simp only [wN, Bool.false_eq_true, if_false, if_true] <;> rcases hs with h | h
  · rw [cellT_out h]; exact tabW_out_left hF _ _ (lineT_range _ k j)
  · rw [lineT_out h]; exact tabW_out_right hF _ _ (cellT_range _ k i)
  · rw [lineT_out h]; exact tabW_out_right hF _ _ (cellT_range _ k j)
  · rw [cellT_out h]; exact tabW_out_left hF _ _ (lineT_range _ k i)

lemma mem_grid_of_wN {F : Fam} (hF : OutZero F) {k : ℕ} {s : FIx} (h : wN F k s ≠ 0) :
    s ∈ grid k := by
  by_contra hs; exact h (wN_eq_zero hF hs)

/-! ## 4.  The box file is `μ_K` -/

lemma convPoly_sq (A K : ℕ) (hAK : 2 * A < 5 * K) :
    convPoly 5 [(A, A), (5 * K - A, A), (5 * K - A, 5 * K - A), (A, 5 * K - A)] = lebSq A K := by
  have hz : ([(A, A), (5 * K - A, A), (5 * K - A, 5 * K - A), (A, 5 * K - A)] : List (ℕ × ℕ)).zip
      ([(A, A), (5 * K - A, A), (5 * K - A, 5 * K - A), (A, 5 * K - A)].rotate 1) =
      [((A, A), (5 * K - A, A)), ((5 * K - A, A), (5 * K - A, 5 * K - A)),
        ((5 * K - A, 5 * K - A), (A, 5 * K - A)), ((A, 5 * K - A), (A, A))] := rfl
  have hc : (((5 * K - A : ℕ) : ℝ)) / 5 = (K : ℝ) - A / 5 := by
    rw [Nat.cast_sub (by omega)]; push_cast; ring
  have hd : (0 : ℝ) < (K : ℝ) - A / 5 - A / 5 := by
    have : (2 * A : ℝ) < 5 * K := by exact_mod_cast hAK
    linarith
  ext p
  simp only [convPoly, hz, List.forall_mem_cons, List.not_mem_nil, IsEmpty.forall_iff,
    implies_true, and_true, Set.mem_ofPred_eq, lebSq, Set.mem_prod, Set.mem_Icc]
  constructor
  · rintro ⟨h1, h2, h3, h4⟩; refine ⟨⟨?_, ?_⟩, ?_, ?_⟩ <;> nlinarith
  · rintro ⟨⟨h1, h2⟩, h3, h4⟩; refine ⟨?_, ?_, ?_, ?_⟩ <;> nlinarith

lemma fileIx_inj {F : Fam} {K : ℕ} {segs : List (ℕ × ℕ × ℕ × ℕ × ℕ)}
    (hnd : (segs.map (fileIx F K)).Nodup) {j₁ j₂ : Fin segs.length}
    (h : fileIx F K (segs.get j₁) = fileIx F K (segs.get j₂)) : j₁ = j₂ := by
  have h' : (segs.map (fileIx F K))[j₁.1]'(by simp) = (segs.map (fileIx F K))[j₂.1]'(by simp) := by
    simpa using h
  exact Fin.ext ((List.Nodup.getElem_inj_iff hnd).mp h')

lemma keyN_inj {K : ℕ} (hK : 5 * K < 4096) {s t : FIx} (hs : s ∈ grid K) (ht : t ∈ grid K)
    (h : keyN s = keyN t) : s = t := by
  obtain ⟨⟨o, i, j⟩, b⟩ := s
  obtain ⟨⟨o', i', j'⟩, b'⟩ := t
  rw [mem_grid] at hs ht
  simp only at hs ht
  simp only [keyN] at h
  have hi : i = i' ∧ j = j' ∧ o.toNat = o'.toNat ∧ b.toNat = b'.toNat := by
    have ho := Bool.toNat_le o
    have ho' := Bool.toNat_le o'
    have hb := Bool.toNat_le b
    have hb' := Bool.toNat_le b'
    omega
  obtain ⟨rfl, rfl, ho, hb⟩ := hi
  have ho' : o = o' := by cases o <;> cases o' <;> simp_all
  have hb' : b = b' := by cases b <;> cases b' <;> simp_all
  rw [ho', hb']

lemma mem_gridList {K : ℕ} {s : FIx} (hs : s ∈ grid K) : s ∈ gridList K := by
  obtain ⟨⟨o, i, j⟩, b⟩ := s
  rw [mem_grid] at hs
  simp only at hs
  simp only [gridList, List.mem_flatMap, List.mem_map]
  refine ⟨o, by cases o <;> simp, i.toNat, List.mem_range.mpr (show i.toNat < 5 * K + 1 by omega),
    j.toNat, List.mem_range.mpr (show j.toNat < 5 * K + 1 by omega), b, by cases b <;> simp, ?_⟩
  simp only [Prod.mk.injEq, and_true, true_and]
  omega

/-- The sorted-keys check gives the bijection: no (segment, layer) twice ... -/
lemma nodup_of_keys {F : Fam} {K : ℕ} {segs : List (ℕ × ℕ × ℕ × ℕ × ℕ)} {keys : List ℕ}
    (hkeys : segs.map (fun e => keyN (fileIx F K e)) = keys) (hsort : msort 32 keys = gridKeys F K)
    (hstrict : strictB (gridKeys F K) = true) : (segs.map (fileIx F K)).Nodup := by
  have h1 : (msort 32 keys).Nodup := hsort ▸ strictB_nodup _ hstrict
  have h2 := (msort_perm _ _).nodup_iff.mp h1
  rw [← hkeys, show (segs.map fun e => keyN (fileIx F K e)) = (segs.map (fileIx F K)).map keyN by
    rw [List.map_map]; rfl] at h2
  exact h2.of_map keyN

/-- ... and every (segment, layer) of `[0,K]²` with non-zero mass is a file entry. -/
lemma complete_of_keys {F : Fam} (hF : OutZero F) {K : ℕ} (hK : 5 * K < 4096)
    {segs : List (ℕ × ℕ × ℕ × ℕ × ℕ)} {keys : List ℕ} (hok : segs.all (segOK F K) = true)
    (hkeys : segs.map (fun e => keyN (fileIx F K e)) = keys) (hsort : msort 32 keys = gridKeys F K)
    (s : FIx) (hs : s ∈ grid K) :
    wN F K s = 0 ∨ ∃ j : Fin segs.length, fileIx F K (segs.get j) = s := by
  by_cases h0 : wN F K s = 0
  · exact Or.inl h0
  right
  have hm : keyN s ∈ gridKeys F K :=
    List.mem_map.mpr ⟨s, List.mem_filter.mpr ⟨mem_gridList hs, by simpa using h0⟩, rfl⟩
  rw [← hsort] at hm
  have hm' := (msort_perm _ _).mem_iff.mp hm
  rw [← hkeys] at hm'
  obtain ⟨e, he, hke⟩ := List.mem_map.mp hm'
  have hokE := List.all_eq_true.mp hok e he
  simp only [segOK, Bool.and_eq_true, beq_iff_eq, decide_eq_true_eq] at hokE
  have hg : fileIx F K e ∈ grid K := mem_grid_of_wN hF (by rw [hokE.2.2]; omega)
  have hfe := keyN_inj hK hg hs hke
  obtain ⟨j', hj'⟩ := List.mem_iff_get.mp he
  exact ⟨j', by rw [hj', hfe]⟩

/-- **A box file that passes the list checks, with the Lebesgue square as its polygon, is `μ_K`.**
-/
theorem fileCover_measure (F : Fam) (hF : OutZero F) (K : ℕ) (segs : List (ℕ × ℕ × ℕ × ℕ × ℕ))
    (verts : List (ℕ × ℕ)) (pw : ℕ) (hok : segs.all (segOK F K) = true)
    (hK : 5 * K < 4096) (keys : List ℕ) (hkeys : segs.map (fun e => keyN (fileIx F K e)) = keys)
    (hsort : msort 32 keys = gridKeys F K) (hstrict : strictB (gridKeys F K) = true)
    (hpoly : convPoly 5 verts = lebSq F.A K)
    (hpw : (pw : ℝ) / F.den = ((K : ℝ) - 2 * F.A / 5) ^ 2) :
    (fileCover F.den segs verts pw).measure = (famCover F K).measure := by
  have hnd := nodup_of_keys hkeys hsort hstrict
  unfold MixedCover.measure
  refine congrArg₂ (· + ·) (congrArg₂ (· + ·) ?_ ?_) ?_
  · rw [show (fileCover F.den segs verts pw).pts = ∅ from rfl, show (famCover F K).pts = ∅ from rfl,
      sum_empty, sum_empty]
  · -- the segments
    set G : FIx → Measure (ℝ × ℝ) := fun s =>
      ENNReal.ofReal ((wN F K s : ℝ) / F.den) • segMeasure (segA s.1) (segB s.1) with hG
    set φ : Fin segs.length → FIx := fun j => fileIx F K (segs.get j) with hφ
    have hok' : ∀ j : Fin segs.length, segGeom (segs.get j) = true ∧ 0 < (segs.get j).2.2.2.2 ∧
        wN F K (φ j) = (segs.get j).2.2.2.2 := fun j => by
      have h := List.all_eq_true.mp hok _ (List.get_mem segs j)
      simpa only [segOK, Bool.and_eq_true, beq_iff_eq, decide_eq_true_eq] using h
    have hterm : ∀ j ∈ (univ : Finset (Fin segs.length)),
        ENNReal.ofReal ((fileCover F.den segs verts pw).sw j) •
          segMeasure ((fileCover F.den segs verts pw).sa j) ((fileCover F.den segs verts pw).sb j)
          = G (φ j) := by
      intro j _
      obtain ⟨hgeo, _, hw⟩ := hok' j
      simp only [fileCover, hG]
      rw [seg_of_geom _ hgeo, hw]
      rfl
    have hL : ∑ j ∈ (univ : Finset (Fin segs.length)),
        ENNReal.ofReal ((fileCover F.den segs verts pw).sw j) •
          segMeasure ((fileCover F.den segs verts pw).sa j) ((fileCover F.den segs verts pw).sb j)
          = ∑ s ∈ univ.image φ, G s := by
      rw [Finset.sum_congr rfl hterm, Finset.sum_image]
      intro j₁ _ j₂ _ h; exact fileIx_inj hnd h
    change _ = ∑ s ∈ grid K, G s
    rw [show (fileCover F.den segs verts pw).segs = univ from rfl, hL]
    refine Finset.sum_subset ?_ ?_
    · intro s hs
      obtain ⟨j, _, rfl⟩ := mem_image.mp hs
      obtain ⟨_, hw0, hw⟩ := hok' j
      exact mem_grid_of_wN hF (by rw [hw]; omega)
    · intro s hs hns
      rcases complete_of_keys hF hK hok hkeys hsort s hs with h0 | ⟨j, hj⟩
      · simp [hG, h0]
      · exact absurd (mem_image.mpr ⟨j, mem_univ _, hj⟩) hns
  · -- the polygon
    refine Finset.sum_congr rfl fun u _ => ?_
    simp only [fileCover, famCover, hpoly, hpw]

/-! ## 5.  Localisation: an integer shift per axis -/

/-- An integer shift `n` taking the axis range `[x₀, x₁]` of a square in `[0,k]` into `[0, 2R + 3]`
without changing what `μ_k` looks like there: keep it (near the wall `0`), move the far wall `k` to
`2R + 3`, or move a range inside the open band zone `(R, k − R)` into `(R, R + 3)`. -/
def Good (R k : ℕ) (n : ℤ) (x₀ x₁ : ℝ) : Prop :=
  (n = 0 ∧ x₁ < (R : ℝ) + 3 ∧ x₁ < (k : ℝ) - R) ∨
    (n = (k : ℤ) - (2 * (R : ℤ) + 3) ∧ (R : ℝ) < x₀ ∧ (k : ℝ) - R - 3 < x₀) ∨
    ((R : ℝ) < x₀ ∧ x₁ < (k : ℝ) - R ∧ (R : ℝ) < x₀ - n ∧ x₁ - n < (R : ℝ) + 3)

/-- A good shift exists for every range of width `< 2` once `k ≥ 2R + 2`. -/
lemma exists_good {R k : ℕ} (hk : 2 * R + 2 ≤ k) {x₀ x₁ : ℝ} (hw : x₁ - x₀ < 2) :
    ∃ n : ℤ, Good R k n x₀ x₁ := by
  have hk' : 2 * (R : ℝ) + 2 ≤ k := by exact_mod_cast hk
  by_cases hA : x₁ < (R : ℝ) + 3 ∧ x₁ < (k : ℝ) - R
  · exact ⟨0, Or.inl ⟨rfl, hA⟩⟩
  by_cases hB : (R : ℝ) < x₀ ∧ (k : ℝ) - R - 3 < x₀
  · exact ⟨(k : ℤ) - (2 * (R : ℤ) + 3), Or.inr (Or.inl ⟨rfl, hB⟩)⟩
  refine ⟨⌈x₀⌉ - ((R : ℤ) + 1), Or.inr (Or.inr ?_)⟩
  have hc1 := Int.le_ceil x₀
  have hc2 := Int.ceil_lt_add_one x₀
  push_cast
  rw [not_and_or, not_lt, not_lt] at hA
  rw [not_and_or, not_lt, not_lt] at hB
  have h2 : (R : ℝ) < x₀ ∧ x₁ < (k : ℝ) - R := by
    rcases hA with hA | hA <;> rcases hB with hB | hB <;> constructor <;> linarith
  exact ⟨h2.1, h2.2, by linarith, by linarith⟩

lemma int_lt {a b : ℤ} (h : (a : ℝ) < b) : a < b := by exact_mod_cast h
lemma int_le {a b : ℤ} (h : (a : ℝ) ≤ b) : a ≤ b := by exact_mod_cast h

lemma good_cell {R k : ℕ} {n : ℤ} {x₀ x₁ : ℝ} (hg : Good R k n x₀ x₁) (h0 : 0 ≤ x₀)
    (h1 : x₁ ≤ k) {i : ℤ} (hi1 : (i : ℝ) ≤ 5 * x₁) (hi0 : 5 * x₀ ≤ i + 1) :
    cellT R k i = cellT R (2 * R + 3) (i - 5 * n) := by
  rcases hg with ⟨rfl, ha, hb⟩ | ⟨rfl, ha, hb⟩ | ⟨ha, hb, hc, hd⟩
  · have e1 : i < 5 * (R : ℤ) + 15 := int_lt (by push_cast; linarith)
    have e2 : i < 5 * (k : ℤ) - 5 * (R : ℤ) := int_lt (by push_cast; linarith)
    have e3 : -1 ≤ i := int_le (by push_cast; linarith)
    unfold cellT; push_cast; split_ifs <;> omega
  · have e1 : 5 * (R : ℤ) - 1 < i := int_lt (by push_cast; linarith)
    have e2 : 5 * (k : ℤ) - 5 * (R : ℤ) - 16 < i := int_lt (by push_cast; linarith)
    have e3 : i ≤ 5 * (k : ℤ) := int_le (by push_cast; linarith)
    unfold cellT; push_cast; split_ifs <;> omega
  · have e1 : 5 * (R : ℤ) - 1 < i := int_lt (by push_cast; linarith)
    have e2 : i < 5 * (k : ℤ) - 5 * (R : ℤ) := int_lt (by push_cast; linarith)
    have e3 : 5 * (R : ℤ) - 1 < i - 5 * n := int_lt (by push_cast; linarith)
    have e4 : i - 5 * n < 5 * (R : ℤ) + 15 := int_lt (by push_cast; linarith)
    unfold cellT; push_cast; split_ifs <;> omega

lemma good_line {R k : ℕ} {n : ℤ} {x₀ x₁ : ℝ} (hg : Good R k n x₀ x₁) (h0 : 0 ≤ x₀)
    (h1 : x₁ ≤ k) {j : ℤ} (hj0 : 5 * x₀ ≤ j) (hj1 : (j : ℝ) ≤ 5 * x₁) :
    lineT R k j = lineT R (2 * R + 3) (j - 5 * n) := by
  rcases hg with ⟨rfl, ha, hb⟩ | ⟨rfl, ha, hb⟩ | ⟨ha, hb, hc, hd⟩
  · have e1 : j < 5 * (R : ℤ) + 15 := int_lt (by push_cast; linarith)
    have e2 : j < 5 * (k : ℤ) - 5 * (R : ℤ) := int_lt (by push_cast; linarith)
    have e3 : 0 ≤ j := int_le (by push_cast; linarith)
    unfold lineT; push_cast; split_ifs <;> omega
  · have e1 : 5 * (R : ℤ) < j := int_lt (by push_cast; linarith)
    have e2 : 5 * (k : ℤ) - 5 * (R : ℤ) - 15 < j := int_lt (by push_cast; linarith)
    have e3 : j ≤ 5 * (k : ℤ) := int_le (by push_cast; linarith)
    unfold lineT; push_cast; split_ifs <;> omega
  · have e1 : 5 * (R : ℤ) < j := int_lt (by push_cast; linarith)
    have e2 : j < 5 * (k : ℤ) - 5 * (R : ℤ) := int_lt (by push_cast; linarith)
    have e3 : 5 * (R : ℤ) < j - 5 * n := int_lt (by push_cast; linarith)
    have e4 : j - 5 * n < 5 * (R : ℤ) + 15 := int_lt (by push_cast; linarith)
    unfold lineT; push_cast; split_ifs <;> omega

lemma good_leb {R A k : ℕ} (hA : (A : ℝ) / 5 ≤ R) {n : ℤ} {x₀ x₁ : ℝ} (hg : Good R k n x₀ x₁)
    {x : ℝ} (hx0 : x₀ ≤ x) (hx1 : x ≤ x₁) :
    ((A : ℝ) / 5 ≤ x ∧ x ≤ (k : ℝ) - A / 5) ↔
      ((A : ℝ) / 5 ≤ x - n ∧ x - n ≤ ((2 * R + 3 : ℕ) : ℝ) - A / 5) := by
  push_cast
  rcases hg with ⟨rfl, ha, hb⟩ | ⟨rfl, ha, hb⟩ | ⟨ha, hb, hc, hd⟩ <;> push_cast <;>
    constructor <;> rintro ⟨h1, h2⟩ <;> constructor <;> linarith

lemma good_box {R k : ℕ} {n : ℤ} {x₀ x₁ : ℝ} (hg : Good R k n x₀ x₁) (h0 : 0 ≤ x₀) (h1 : x₁ ≤ k) :
    0 ≤ x₀ - n ∧ x₁ - n ≤ ((2 * R + 3 : ℕ) : ℝ) := by
  push_cast
  rcases hg with ⟨rfl, ha, hb⟩ | ⟨rfl, ha, hb⟩ | ⟨ha, hb, hc, hd⟩ <;> push_cast <;>
    constructor <;> linarith

/-! ## 6.  Translation -/

/-- The index shift by `(-5 nx, -5 ny)`, keeping the layer. -/
def shiftF (nx ny : ℤ) (s : FIx) : FIx := (Bentz.shiftIx nx ny s.1, s.2)

/-- The segment part of the mass. -/
noncomputable def segTerm (F : Fam) (k : ℕ) (S : Set (ℝ × ℝ)) (s : FIx) : ℝ :=
  (wN F k s : ℝ) / F.den * segFrac (segA s.1) (segB s.1) S

/-- Re-indexing the segment sums by a shift that matches the terms. -/
lemma sum_segTerm_shift {F : Fam} (hF : OutZero F) {k K : ℕ} (S S' : Set (ℝ × ℝ)) (nx ny : ℤ)
    (hterm : ∀ s, segTerm F k S s = segTerm F K S' (shiftF nx ny s)) :
    ∑ s ∈ grid k, segTerm F k S s = ∑ s ∈ grid K, segTerm F K S' s := by
  set τ := shiftF nx ny with hτ
  set τ' := shiftF (-nx) (-ny) with hτ'
  have h1 : ∀ s, τ' (τ s) = s := fun s => by
    obtain ⟨⟨o, i, j⟩, b⟩ := s; simp [hτ, hτ', shiftF, Bentz.shiftIx]
  have h2 : ∀ s, τ (τ' s) = s := fun s => by
    obtain ⟨⟨o, i, j⟩, b⟩ := s; simp [hτ, hτ', shiftF, Bentz.shiftIx]
  have hinj : Set.InjOn τ (grid k : Set FIx) := fun a _ b _ h => by
    rw [← h1 a, h, h1 b]
  rw [Finset.sum_congr rfl fun s _ => hterm s, ← Finset.sum_image hinj]
  have hzK : ∀ s, s ∉ grid K → segTerm F K S' s = 0 := fun s hs => by
    simp [segTerm, wN_eq_zero hF hs]
  have hzk : ∀ s ∈ grid K, s ∉ (grid k).image τ → segTerm F K S' s = 0 := fun s _ hs => by
    have hn : τ' s ∉ grid k := fun hm => hs (mem_image.mpr ⟨τ' s, hm, h2 s⟩)
    rw [← h2 s, ← hterm]
    simp [segTerm, wN_eq_zero hF hn]
  have e1 : ∑ s ∈ (grid k).image τ, segTerm F K S' s
      = ∑ s ∈ (grid k).image τ ∪ grid K, segTerm F K S' s :=
    Finset.sum_subset Finset.subset_union_left
      (fun s hs hns => hzk s ((mem_union.mp hs).resolve_left hns) hns)
  have e2 : ∑ s ∈ grid K, segTerm F K S' s
      = ∑ s ∈ (grid k).image τ ∪ grid K, segTerm F K S' s :=
    Finset.sum_subset Finset.subset_union_right (fun s _ hns => hzK s hns)
  rw [e1, e2]

lemma volume_lebSq {A k : ℕ} (hk : 2 * (A : ℝ) / 5 ≤ k) :
    volume (lebSq A k) = ENNReal.ofReal (((k : ℝ) - 2 * A / 5) ^ 2) := by
  rw [lebSq, Measure.volume_eq_prod, Measure.prod_prod, Real.volume_Icc,
    ← ENNReal.ofReal_mul (by linarith)]
  congr 1; ring

lemma polyTerm {A k : ℕ} (hk : 2 * (A : ℝ) / 5 < k) (S : Set (ℝ × ℝ)) :
    ((k : ℝ) - 2 * A / 5) ^ 2 * areaFrac (lebSq A k) S = (volume (S ∩ lebSq A k)).toReal := by
  have hpos : 0 < ((k : ℝ) - 2 * A / 5) ^ 2 := by
    have : 0 < (k : ℝ) - 2 * A / 5 := by linarith
    positivity
  rw [areaFrac, volume_lebSq hk.le, ENNReal.toReal_mul, ENNReal.toReal_inv,
    ENNReal.toReal_ofReal hpos.le, ← mul_assoc, mul_inv_cancel₀ hpos.ne', one_mul]

/-- **Localisation.**  For `k ≥ 2R + 2`, the mass of any closed unit square in `[0,k]²` under `μ_k`
is the mass under `μ_{2R+3}` of an integer translate of it that lies in `[0, 2R + 3]²`. -/
theorem mass_shift (F : Fam) (hF : OutZero F) (hA : F.A ≤ 5 * F.R) {k : ℕ} (hk : 2 * F.R + 2 ≤ k)
    (c : ℝ × ℝ) (θ : ℝ) (hS : sq c θ 1 ⊆ box k) :
    ∃ v : ℝ × ℝ, sq (c - v) θ 1 ⊆ box ((2 * F.R + 3 : ℕ) : ℝ) ∧
      (famCover F k).mass (sq c θ 1) = (famCover F (2 * F.R + 3)).mass (sq (c - v) θ 1) := by
  have hA' : (F.A : ℝ) / 5 ≤ F.R := by
    have : (F.A : ℝ) ≤ 5 * F.R := by exact_mod_cast hA
    linarith
  have hk' : 2 * (F.R : ℝ) + 2 ≤ k := by exact_mod_cast hk
  obtain ⟨ha1, ha2, ha3, ha4⟩ := (sq_subset_box_iff k c θ).mp hS
  have hw := Bentz.wid_lt_two θ
  obtain ⟨nx, hgx⟩ := exists_good hk (x₀ := c.1 - wid θ / 2) (x₁ := c.1 + wid θ / 2) (by linarith)
  obtain ⟨ny, hgy⟩ := exists_good hk (x₀ := c.2 - wid θ / 2) (x₁ := c.2 + wid θ / 2) (by linarith)
  have hx0 : 0 ≤ c.1 - wid θ / 2 := by linarith
  have hx1 : c.1 + wid θ / 2 ≤ k := by linarith
  have hy0 : 0 ≤ c.2 - wid θ / 2 := by linarith
  have hy1 : c.2 + wid θ / 2 ≤ k := by linarith
  set v : ℝ × ℝ := ((nx : ℝ), (ny : ℝ)) with hv
  refine ⟨v, ?_, ?_⟩
  · obtain ⟨b1, b2⟩ := good_box hgx hx0 hx1
    obtain ⟨b3, b4⟩ := good_box hgy hy0 hy1
    refine (sq_subset_box_iff _ (c - v) θ).mpr ⟨?_, ?_, ?_, ?_⟩ <;>
      simp only [hv, Prod.fst_sub, Prod.snd_sub] <;> linarith
  -- the bounding box of the square
  have hbox : ∀ p ∈ sq c θ 1, (c.1 - wid θ / 2 ≤ p.1 ∧ p.1 ≤ c.1 + wid θ / 2) ∧
      (c.2 - wid θ / 2 ≤ p.2 ∧ p.2 ≤ c.2 + wid θ / 2) := fun p hp => by
    obtain ⟨h1, h2⟩ := abs_sub_le_wid hp
    rw [abs_le] at h1 h2
    exact ⟨⟨by linarith, by linarith⟩, by linarith, by linarith⟩
  unfold MixedCover.mass
  refine congrArg₂ (· + ·) (congrArg₂ (· + ·) ?_ ?_) ?_
  · have h : ∀ (T : Finset Empty) (f : Empty → ℝ), ∑ e ∈ T, f e = 0 := fun T f => by
      simp [Finset.eq_empty_of_isEmpty T]
    rw [h, h]
  · -- the segments
    change ∑ s ∈ grid k, segTerm F k (sq c θ 1) s
      = ∑ s ∈ grid (2 * F.R + 3), segTerm F (2 * F.R + 3) (sq (c - v) θ 1) s
    refine sum_segTerm_shift hF _ _ nx ny fun s => ?_
    simp only [segTerm, shiftF]
    rw [Bentz.segFrac_shift]
    by_cases h0 : segFrac (segA s.1) (segB s.1) (sq c θ 1) = 0
    · rw [h0]; simp
    obtain ⟨t, ⟨t0, t1⟩, ht⟩ := Bentz.exists_of_segFrac_ne h0
    obtain ⟨⟨p1, p2⟩, p3, p4⟩ := hbox _ ht
    obtain ⟨⟨o, i, j⟩, b⟩ := s
    congr 3
    cases o
    · simp only [segPt, segA, segB, Bool.false_eq_true, if_false] at p1 p2 p3 p4
      simp only [wN, Bentz.shiftIx, Bool.false_eq_true, if_false]
      rw [good_cell hgx hx0 hx1 (i := i) (by nlinarith) (by nlinarith),
        good_line hgy hy0 hy1 (j := j) (by nlinarith) (by nlinarith)]
    · simp only [segPt, segA, segB, if_true] at p1 p2 p3 p4
      simp only [wN, Bentz.shiftIx, if_true]
      rw [good_cell hgy hy0 hy1 (i := j) (by nlinarith) (by nlinarith),
        good_line hgx hx0 hx1 (j := i) (by nlinarith) (by nlinarith)]
  · -- the Lebesgue square
    simp only [famCover, Finset.sum_const, Finset.card_univ, Fintype.card_unit, one_smul]
    have hK : 2 * (F.A : ℝ) / 5 < ((2 * F.R + 3 : ℕ) : ℝ) := by push_cast; linarith
    rw [polyTerm (by linarith), polyTerm hK]
    congr 1
    have hset : sq (c - v) θ 1 ∩ lebSq F.A (2 * F.R + 3)
        = (fun p => p + v) ⁻¹' (sq c θ 1 ∩ lebSq F.A k) := by
      ext p
      simp only [Set.mem_inter_iff, Set.mem_preimage, Bentz.mem_sq_sub]
      refine and_congr_right fun hp => ?_
      obtain ⟨⟨p1, p2⟩, p3, p4⟩ := hbox _ hp
      simp only [Prod.fst_add, Prod.snd_add, hv] at p1 p2 p3 p4
      simp only [lebSq, Set.mem_prod, Set.mem_Icc, Prod.fst_add, Prod.snd_add, hv]
      rw [good_leb hA' hgx p1 p2, good_leb hA' hgy p3 p4]
      simp only [add_sub_cancel_right]
    rw [hset, measure_preimage_add_right]

/-! ## 7.  Accounting

For `k = m + 2R + 1` the cells of `[0,k]` have each edge code twice, each band phase `m + 1` times,
and `outside` once (`sum_cellT`); the lines have each edge code `0..5R` twice, band phase 0 `m`
times, the other phases `m + 1` times (`sum_lineT`).  So the segment mass is a polynomial in `m`
whose coefficients are finite sums over the tables. -/

/-- Cell sums: the constant part. -/
def C0 (R : ℕ) (g : ℤ → ℕ) : ℕ :=
  2 * ∑ a ∈ range (5 * R), g a + ∑ p ∈ range 5, g (5 * (R : ℤ) + p) + g (5 * (R : ℤ) + 6)
/-- Cell sums: the part linear in `m`. -/
def C1 (R : ℕ) (g : ℤ → ℕ) : ℕ := ∑ p ∈ range 5, g (5 * (R : ℤ) + p)
/-- Line sums: the constant part. -/
def L0 (R : ℕ) (g : ℤ → ℕ) : ℕ :=
  2 * ∑ a ∈ range (5 * R), g a + 2 * g (5 * (R : ℤ)) + ∑ q ∈ range 4, g (5 * (R : ℤ) + 2 + q)
/-- Line sums: the part linear in `m`. -/
def L1 (R : ℕ) (g : ℤ → ℕ) : ℕ := ∑ p ∈ range 5, g (5 * (R : ℤ) + 1 + p)

lemma sum_cellT (R m : ℕ) (g : ℤ → ℕ) :
    ∑ i ∈ idx (m + 2 * R + 1), g (cellT R (m + 2 * R + 1) i) = C0 R g + m * C1 R g := by
  rw [idx, sum_map, show 5 * (m + 2 * R + 1) + 1 = 5 * R + (5 * (m + 1) + (5 * R + 1)) by ring,
    sum_range_add, sum_range_add, sum_range_succ (n := 5 * R)]
  simp only [Function.Embedding.coeFn_mk]
  have h1 : ∑ x ∈ range (5 * R), g (cellT R (m + 2 * R + 1) (x : ℤ)) = ∑ a ∈ range (5 * R), g a :=
    sum_congr rfl fun x hx => by
      rw [mem_range] at hx; congr 1; unfold cellT; split_ifs <;> omega
  have h2 : ∑ x ∈ range (5 * (m + 1)), g (cellT R (m + 2 * R + 1) ((5 * R + x : ℕ) : ℤ))
      = ∑ x ∈ range (5 * (m + 1)), (fun p : ℕ => g (5 * (R : ℤ) + (p : ℤ))) (x % 5) :=
    sum_congr rfl fun x hx => by
      rw [mem_range] at hx; simp only; congr 1; unfold cellT; split_ifs <;> omega
  have h3 : ∑ x ∈ range (5 * R), g (cellT R (m + 2 * R + 1) ((5 * R + (5 * (m + 1) + x) : ℕ) : ℤ))
      = ∑ x ∈ range (5 * R), (fun a : ℕ => g a) (5 * R - 1 - x) :=
    sum_congr rfl fun x hx => by
      rw [mem_range] at hx; simp only; congr 1; unfold cellT; split_ifs <;> omega
  have h4 : cellT R (m + 2 * R + 1) ((5 * R + (5 * (m + 1) + 5 * R) : ℕ) : ℤ)
      = 5 * (R : ℤ) + 6 := by
    unfold cellT; split_ifs <;> omega
  rw [h1, h2, h3, h4, Bentz.sum_range_mod (m + 1) (fun p : ℕ => g (5 * (R : ℤ) + (p : ℤ))),
    sum_range_reflect (fun a : ℕ => g a) (5 * R)]
  unfold C0 C1
  ring

lemma sum_lineT (R m : ℕ) (g : ℤ → ℕ) :
    ∑ j ∈ idx (m + 2 * R + 1), g (lineT R (m + 2 * R + 1) j) = L0 R g + m * L1 R g := by
  rw [idx, sum_map,
    show 5 * (m + 2 * R + 1) + 1 = 5 * R + (1 + (4 + (5 * m + (1 + 5 * R)))) by ring,
    sum_range_add, sum_range_add, sum_range_add, sum_range_add, sum_range_add]
  simp only [Function.Embedding.coeFn_mk, sum_range_one]
  have h1 : ∑ x ∈ range (5 * R), g (lineT R (m + 2 * R + 1) (x : ℤ)) = ∑ a ∈ range (5 * R), g a :=
    sum_congr rfl fun x hx => by
      rw [mem_range] at hx; congr 1; unfold lineT; split_ifs <;> omega
  have h2 : lineT R (m + 2 * R + 1) ((5 * R + 0 : ℕ) : ℤ) = 5 * (R : ℤ) := by
    unfold lineT; split_ifs <;> omega
  have h3 : ∑ x ∈ range 4, g (lineT R (m + 2 * R + 1) ((5 * R + (1 + x) : ℕ) : ℤ))
      = ∑ q ∈ range 4, g (5 * (R : ℤ) + 2 + q) :=
    sum_congr rfl fun x hx => by
      rw [mem_range] at hx; congr 1; unfold lineT; split_ifs <;> omega
  have h4 : ∑ x ∈ range (5 * m), g (lineT R (m + 2 * R + 1) ((5 * R + (1 + (4 + x)) : ℕ) : ℤ))
      = ∑ x ∈ range (5 * m), (fun p : ℕ => g (5 * (R : ℤ) + 1 + (p : ℤ))) (x % 5) :=
    sum_congr rfl fun x hx => by
      rw [mem_range] at hx; simp only; congr 1; unfold lineT; split_ifs <;> omega
  have h5 : lineT R (m + 2 * R + 1) ((5 * R + (1 + (4 + (5 * m + 0)))  : ℕ) : ℤ) = 5 * (R : ℤ) := by
    unfold lineT; split_ifs <;> omega
  have h6 : ∑ x ∈ range (5 * R),
        g (lineT R (m + 2 * R + 1) ((5 * R + (1 + (4 + (5 * m + (1 + x)))) : ℕ) : ℤ))
      = ∑ x ∈ range (5 * R), (fun a : ℕ => g a) (5 * R - 1 - x) :=
    sum_congr rfl fun x hx => by
      rw [mem_range] at hx; simp only; congr 1; unfold lineT; split_ifs <;> omega
  rw [h1, h2, h3, h4, h5, h6, Bentz.sum_range_mod m (fun p : ℕ => g (5 * (R : ℤ) + 1 + (p : ℤ))),
    sum_range_reflect (fun a : ℕ => g a) (5 * R)]
  unfold L0 L1
  ring

/-- The polynomial of a table: coefficients. -/
def H00 (R : ℕ) (T : ℤ → ℤ → ℕ) : ℕ := C0 R (fun c => L0 R (T c))
def H01 (R : ℕ) (T : ℤ → ℤ → ℕ) : ℕ := C0 R (fun c => L1 R (T c))
def H10 (R : ℕ) (T : ℤ → ℤ → ℕ) : ℕ := C1 R (fun c => L0 R (T c))
def H11 (R : ℕ) (T : ℤ → ℤ → ℕ) : ℕ := C1 R (fun c => L1 R (T c))

lemma sum_cell_line (R m : ℕ) (T : ℤ → ℤ → ℕ) :
    ∑ i ∈ idx (m + 2 * R + 1), ∑ j ∈ idx (m + 2 * R + 1),
        T (cellT R (m + 2 * R + 1) i) (lineT R (m + 2 * R + 1) j)
      = H00 R T + m * (H01 R T + H10 R T) + m ^ 2 * H11 R T := by
  rw [sum_congr rfl fun i _ => sum_lineT R m (T (cellT R (m + 2 * R + 1) i))]
  rw [sum_cellT R m (fun c => L0 R (T c) + m * L1 R (T c))]
  have lin0 : ∀ a b : ℤ → ℕ, C0 R (fun c => a c + m * b c) = C0 R a + m * C0 R b := by
    intro a b; simp only [C0, sum_add_distrib, ← mul_sum]; ring
  have lin1 : ∀ a b : ℤ → ℕ, C1 R (fun c => a c + m * b c) = C1 R a + m * C1 R b := by
    intro a b; simp only [C1, sum_add_distrib, ← mul_sum]
  rw [lin0, lin1]
  unfold H00 H01 H10 H11
  ring

/-- The segment mass of a layer, `k = m + 2R + 1`, horizontal half. -/
def Hpoly (F : Fam) (b : Bool) (m : ℕ) : ℕ :=
  H00 F.R (tabW (F.layer b)) + m * (H01 F.R (tabW (F.layer b)) + H10 F.R (tabW (F.layer b)))
    + m ^ 2 * H11 F.R (tabW (F.layer b))

theorem seg_total (F : Fam) (m : ℕ) :
    ∑ s ∈ grid (m + 2 * F.R + 1), wN F (m + 2 * F.R + 1) s
      = 2 * Hpoly F false m + 2 * Hpoly F true m := by
  have hb : ∀ b : Bool, ∑ seg ∈ univ ×ˢ (idx (m + 2 * F.R + 1) ×ˢ idx (m + 2 * F.R + 1)),
      wN F (m + 2 * F.R + 1) (seg, b) = 2 * Hpoly F b m := by
    intro b
    rw [sum_product, Fintype.sum_bool]
    simp only [sum_product, wN, if_true, Bool.false_eq_true, if_false]
    rw [sum_comm (s := idx (m + 2 * F.R + 1)) (t := idx (m + 2 * F.R + 1))
      (f := fun i j =>
        tabW (F.layer b) (cellT F.R (m + 2 * F.R + 1) j) (lineT F.R (m + 2 * F.R + 1) i))]
    rw [sum_cell_line F.R m (tabW (F.layer b))]
    unfold Hpoly
    ring
  rw [grid, sum_product, sum_comm, Fintype.sum_bool, hb, hb]
  ring

lemma famCover_nonneg (F : Fam) (k : ℕ) : (famCover F k).Nonneg :=
  ⟨fun e => e.elim, fun _ _ => by simp only [famCover]; positivity,
    fun _ _ => by simp only [famCover]; positivity⟩

/-- **Accounting**: the total mass of `μ_k`, `k = m + 2R + 1`. -/
theorem famCover_total (F : Fam) (m : ℕ) :
    (famCover F (m + 2 * F.R + 1)).total
      = ((2 * Hpoly F false m + 2 * Hpoly F true m : ℕ) : ℝ) / F.den
        + (((m + 2 * F.R + 1 : ℕ) : ℝ) - 2 * F.A / 5) ^ 2 := by
  have hs : ∑ s ∈ grid (m + 2 * F.R + 1), (wN F (m + 2 * F.R + 1) s : ℝ) / F.den
      = ((2 * Hpoly F false m + 2 * Hpoly F true m : ℕ) : ℝ) / F.den := by
    rw [← sum_div, ← Nat.cast_sum, seg_total]
  have he : ∀ f : Empty → ℝ, ∑ e ∈ (∅ : Finset Empty), f e = 0 := fun f => sum_empty
  simp only [MixedCover.total, famCover, he, hs, sum_const, card_univ, Fintype.card_unit, one_smul,
    zero_add]

/-! ## 8.  The end theorem -/

/-- Box validity for `μ_{2R+3}` gives every closed unit square in `[0,k]²` mass `≥ 1` under `μ_k`,
`k ≥ 2R + 2`. -/
theorem valid_of_box (F : Fam) (hF : OutZero F) (hA : F.A ≤ 5 * F.R)
    (hval : ∀ (c : ℝ × ℝ) (θ : ℝ), sq c θ 1 ⊆ box ((2 * F.R + 3 : ℕ) : ℝ) →
      1 ≤ (famCover F (2 * F.R + 3)).measure (sq c θ 1))
    {k : ℕ} (hk : 2 * F.R + 2 ≤ k) (c : ℝ × ℝ) (θ : ℝ) (hS : sq c θ 1 ⊆ box k) :
    1 ≤ (famCover F k).measure (sq c θ 1) := by
  obtain ⟨v, hv, hm⟩ := mass_shift F hF hA hk c θ hS
  have h := hval _ _ hv
  rw [MixedCover.measure_apply _ (famCover_nonneg F _) (measurableSet_sq _ _ _)] at h
  rw [MixedCover.measure_apply _ (famCover_nonneg F k) (measurableSet_sq _ _ _), hm]
  exact h

/-- **The end**: box validity for `μ_{2R+3}`, `k ≥ 2R + 2` and `total(μ_k) < n ≤ k²` give `minSide n
= k`. -/
theorem minSide_eq (F : Fam) (hF : OutZero F) (hA : F.A ≤ 5 * F.R)
    (hval : ∀ (c : ℝ × ℝ) (θ : ℝ), sq c θ 1 ⊆ box ((2 * F.R + 3 : ℕ) : ℝ) →
      1 ≤ (famCover F (2 * F.R + 3)).measure (sq c θ 1))
    {k n : ℕ} (hk : 2 * F.R + 2 ≤ k) (hn0 : 0 < n) (htot : (famCover F k).total < n)
    (hn : n ≤ k * k) :
    minSide n = k := by
  have hbox : (famCover F k).measure (box k) < (n : ℝ≥0∞) := calc
    (famCover F k).measure (box k) ≤ (famCover F k).measure Set.univ :=
        measure_mono (Set.subset_univ _)
    _ ≤ ENNReal.ofReal (famCover F k).total := (famCover F k).measure_univ_le (famCover_nonneg _ _)
    _ < ENNReal.ofReal n := (ENNReal.ofReal_lt_ofReal_iff (by exact_mod_cast hn0)).mpr htot
    _ = n := ENNReal.ofReal_natCast _
  have hnot : ∀ s : ℝ, s < k → ¬ Packs n s := fun s hs =>
    not_packs_of_measure k (famCover F k).measure (valid_of_box F hF hA hval hk) n hbox hs
  have hp : Packs n k := packs_grid k n hn
  have hl : IsLeast {s | Packs n s} (k : ℝ) := ⟨hp, fun _ hs => not_lt.mp fun hlt => hnot _ hlt hs⟩
  exact hl.csInf_eq

end BentzFam
end SquarePacking
