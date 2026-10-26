import Sqpack.SquareArea
import Sqpack.SegParts

/-!
# Chords of a tilted square on the grid lines, and the concavity behind Lemma E

`search/QUADRANT_EXACT.md` §4.3–4.4.  Fix the angle `θ` with `s = sin θ > 0`, `c = cos θ > 0`.

* `mem_sq_iff_hchord` — on a horizontal line `y = η` the square `Q(c)` cuts the chord
  `max(t_A, t_B) ≤ t ≤ min(t_C, t_D)`; the four ends are affine in the centre (`tA … tD`).  On a
  vertical line the chord is the slice of `SquareArea.lean` (`lowX … upY`).
* A segment `[A, B]` of such a line captures `w · max(0, min(B, r↑) − max(A, r↓)) / (B − A)`, and
  `min(B, r↑) − max(A, r↓)` is the least of finitely many affine forms of the centre
  (`clampMin`).  `seg_part_h`, `seg_part_v` give the part of the segment inside `Q` for
  `parts_le_segMass`.
* **`concaveOn_max0_clampMin`** — if on a convex set `K` every one of those affine forms has a fixed
  sign, then `max(0, least form)` is concave on `K`.  This is the cell-wise concavity of Lemma E,
  segment by segment: the lines `t_k = A` (up options), `t_j = B` (lo options) and `t_k = t_j` of the
  arrangement fix the signs.
-/

open MeasureTheory Set
open scoped ENNReal

namespace SquarePacking

namespace ChordE

/-! ## 1.  Affine forms and their clamped minimum -/

/-- The affine form `(α, β, γ) : c ↦ α c₁ + β c₂ + γ`. -/
def aff (F : ℝ × ℝ × ℝ) (c : ℝ × ℝ) : ℝ := F.1 * c.1 + F.2.1 * c.2 + F.2.2

/-- The least of the constant `M` and the forms `Fs` at `c`. -/
def clampMin (M : ℝ) (Fs : List (ℝ × ℝ × ℝ)) (c : ℝ × ℝ) : ℝ :=
  Fs.foldr (fun F m => min (aff F c) m) M

lemma clampMin_le_M (M : ℝ) : ∀ (Fs : List (ℝ × ℝ × ℝ)) (c : ℝ × ℝ), clampMin M Fs c ≤ M
  | [], _ => le_rfl
  | _ :: Fs, c => le_trans (min_le_right _ _) (clampMin_le_M M Fs c)

lemma clampMin_le (M : ℝ) : ∀ (Fs : List (ℝ × ℝ × ℝ)) (c : ℝ × ℝ), ∀ F ∈ Fs,
    clampMin M Fs c ≤ aff F c
  | [], _, _, h => absurd h List.not_mem_nil
  | G :: Fs, c, F, h => by
    rcases List.mem_cons.mp h with rfl | h
    · exact min_le_left _ _
    · exact le_trans (min_le_right _ _) (clampMin_le M Fs c F h)

lemma le_clampMin {M x : ℝ} : ∀ (Fs : List (ℝ × ℝ × ℝ)) (c : ℝ × ℝ), x ≤ M →
    (∀ F ∈ Fs, x ≤ aff F c) → x ≤ clampMin M Fs c
  | [], _, hM, _ => hM
  | G :: Fs, c, hM, h =>
    le_min (h G List.mem_cons_self) (le_clampMin Fs c hM fun F hF => h F (List.mem_cons_of_mem _ hF))

lemma concaveOn_aff (K : Set (ℝ × ℝ)) (hK : Convex ℝ K) (F : ℝ × ℝ × ℝ) :
    ConcaveOn ℝ K (aff F) := by
  refine ⟨hK, fun x _ y _ a b _ _ hab => ?_⟩
  simp only [aff, smul_eq_mul, Prod.smul_fst, Prod.smul_snd, Prod.fst_add, Prod.snd_add]
  have : b = 1 - a := by linarith
  subst this
  nlinarith

lemma concaveOn_clampMin (K : Set (ℝ × ℝ)) (hK : Convex ℝ K) (M : ℝ) :
    ∀ Fs : List (ℝ × ℝ × ℝ), ConcaveOn ℝ K (clampMin M Fs)
  | [] => concaveOn_const M hK
  | F :: Fs => (concaveOn_aff K hK F).inf (concaveOn_clampMin K hK M Fs)

/-- **Cell-wise concavity.**  If every form has a fixed sign on the convex set `K` and `M ≥ 0`,
then `max(0, clampMin M Fs)` is concave on `K`. -/
theorem concaveOn_max0_clampMin (K : Set (ℝ × ℝ)) (hK : Convex ℝ K) {M : ℝ} (hM : 0 ≤ M)
    (Fs : List (ℝ × ℝ × ℝ))
    (hsign : ∀ F ∈ Fs, (∀ c ∈ K, 0 ≤ aff F c) ∨ (∀ c ∈ K, aff F c ≤ 0)) :
    ConcaveOn ℝ K (fun c => max 0 (clampMin M Fs c)) := by
  by_cases hneg : ∃ F ∈ Fs, ∀ c ∈ K, aff F c ≤ 0
  · obtain ⟨F, hF, hle⟩ := hneg
    refine (concaveOn_const 0 hK).congr fun c hc => ?_
    exact (max_eq_left (le_trans (clampMin_le M Fs c F hF) (hle c hc))).symm
  · simp only [not_exists, not_and, not_forall, not_le] at hneg
    have hpos : ∀ F ∈ Fs, ∀ c ∈ K, 0 ≤ aff F c := by
      intro F hF
      rcases hsign F hF with h | h
      · exact h
      · obtain ⟨c, hc, hlt⟩ := hneg F hF
        exact absurd (h c hc) (not_le.mpr hlt)
    refine (concaveOn_clampMin K hK M Fs).congr fun c hc => ?_
    exact (max_eq_right (le_clampMin Fs c hM fun F hF => hpos F hF c hc)).symm

/-! ## 2.  Chords on horizontal lines -/

section chord

variable (θ η : ℝ)

/-- The chord ends of `Q(c)` on the horizontal line `y = η` (`s = sin θ`, `c = cos θ`): `t_A`, `t_B`
are lower ends (`X ≥ −½`, `Y ≤ ½`), `t_C`, `t_D` upper ends (`X ≤ ½`, `Y ≥ −½`). -/
noncomputable def tA (c : ℝ × ℝ) : ℝ := c.1 + (-(1 / 2) - (η - c.2) * Real.sin θ) / Real.cos θ
noncomputable def tB (c : ℝ × ℝ) : ℝ := c.1 + ((η - c.2) * Real.cos θ - 1 / 2) / Real.sin θ
noncomputable def tC (c : ℝ × ℝ) : ℝ := c.1 + (1 / 2 - (η - c.2) * Real.sin θ) / Real.cos θ
noncomputable def tD (c : ℝ × ℝ) : ℝ := c.1 + ((η - c.2) * Real.cos θ + 1 / 2) / Real.sin θ

variable {θ η}

lemma mem_sq_iff_hchord (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ) (c : ℝ × ℝ) (t : ℝ) :
    (t, η) ∈ sq c θ 1 ↔
      max (tA θ η c) (tB θ η c) ≤ t ∧ t ≤ min (tC θ η c) (tD θ η c) := by
  have k1 : ∀ (A b : ℝ) {k : ℝ}, 0 < k → (c.1 + A / k ≤ b ↔ A ≤ (b - c.1) * k) := by
    intro A b k hk; rw [← le_sub_iff_add_le', div_le_iff₀ hk]
  have k2 : ∀ (A b : ℝ) {k : ℝ}, 0 < k → (b ≤ c.1 + A / k ↔ (b - c.1) * k ≤ A) := by
    intro A b k hk; rw [← sub_le_iff_le_add', le_div_iff₀ hk]
  simp only [sq, coord, mem_ofPred_eq, abs_le, max_le_iff, le_min_iff, tA, tB, tC, tD]
  rw [k1 _ _ hc, k1 _ _ hs, k2 _ _ hc, k2 _ _ hs]
  constructor
  · rintro ⟨⟨h1, h2⟩, h3, h4⟩
    refine ⟨⟨?_, ?_⟩, ?_, ?_⟩ <;> nlinarith
  · rintro ⟨⟨h1, h2⟩, h3, h4⟩
    refine ⟨⟨?_, ?_⟩, ?_, ?_⟩ <;> nlinarith

end chord

/-! ## 3.  The part of a segment inside the chord -/

/-- The part `[plo, phi]` of `[A, B]` inside `[lo, hi]`, clipped into `[A, B]`. -/
noncomputable def plo (A B lo : ℝ) : ℝ := min B (max A lo)
noncomputable def phi (A B lo hi : ℝ) : ℝ := max (plo A B lo) (min B hi)

lemma phi_sub_plo (A B lo hi : ℝ) : phi A B lo hi - plo A B lo = max 0 (min B hi - max A lo) := by
  simp only [phi, plo]
  rcases le_total (max A lo) B with h | h
  · rw [min_eq_right h, ← max_sub_sub_right, sub_self]
  · rw [min_eq_left h, max_eq_left (min_le_left _ _), sub_self,
      max_eq_left (by linarith [min_le_left B hi] : min B hi - max A lo ≤ 0)]

lemma plo_props {A B lo hi : ℝ} (hAB : A ≤ B) :
    A ≤ plo A B lo ∧ plo A B lo ≤ phi A B lo hi ∧ phi A B lo hi ≤ B ∧
      ∀ t, plo A B lo < t → t < phi A B lo hi → lo ≤ t ∧ t ≤ hi := by
  refine ⟨le_min hAB (le_max_left _ _), le_max_left _ _, max_le (min_le_left _ _) (min_le_left _ _),
    fun t h1 h2 => ?_⟩
  simp only [phi, plo] at h1 h2
  rcases le_total (max A lo) B with h | h
  · rw [min_eq_right h] at h1 h2
    rcases le_total (max A lo) (min B hi) with h' | h'
    · rw [max_eq_right h'] at h2
      exact ⟨by linarith [le_max_right A lo], by linarith [min_le_right B hi]⟩
    · rw [max_eq_left h'] at h2; linarith
  · rw [min_eq_left h, max_eq_left (min_le_left _ _)] at h2
    rw [min_eq_left h] at h1; linarith

/-- `min(B, C, D) − max(A, a, b)` is the least of the nine differences (`M = B − A` first). -/
lemma min3_sub_max3 (A B a b C D : ℝ) (Fs : List (ℝ × ℝ × ℝ)) (c : ℝ × ℝ)
    (hF : ∀ F ∈ Fs, ∃ up ∈ ({B, C, D} : Set ℝ), ∃ lo ∈ ({A, a, b} : Set ℝ), aff F c = up - lo)
    (hall : ∀ up ∈ ({B, C, D} : Set ℝ), ∀ lo ∈ ({A, a, b} : Set ℝ), up = B ∧ lo = A ∨
      ∃ F ∈ Fs, aff F c ≤ up - lo) :
    min B (min C D) - max A (max a b) = clampMin (B - A) Fs c := by
  apply le_antisymm
  · refine le_clampMin Fs c ?_ fun F hFm => ?_
    · linarith [min_le_left B (min C D), le_max_left A (max a b)]
    · obtain ⟨up, hup, lo, hlo, he⟩ := hF F hFm
      rw [he]
      have h1 : min B (min C D) ≤ up := by
        rcases hup with rfl | rfl | rfl
        · exact min_le_left _ _
        · exact le_trans (min_le_right _ _) (min_le_left _ _)
        · exact le_trans (min_le_right _ _) (min_le_right _ _)
      have h2 : lo ≤ max A (max a b) := by
        rcases hlo with rfl | rfl | rfl
        · exact le_max_left _ _
        · exact le_trans (le_max_left _ _) (le_max_right _ _)
        · exact le_trans (le_max_right _ _) (le_max_right _ _)
      linarith
  · obtain ⟨up, hup, hupe⟩ : ∃ up ∈ ({B, C, D} : Set ℝ), min B (min C D) = up := by
      rcases min_choice B (min C D) with h | h
      · exact ⟨B, Or.inl rfl, h⟩
      · rcases min_choice C D with h' | h'
        · exact ⟨C, Or.inr (Or.inl rfl), h.trans h'⟩
        · exact ⟨D, Or.inr (Or.inr rfl), h.trans h'⟩
    obtain ⟨lo, hlo, hloe⟩ : ∃ lo ∈ ({A, a, b} : Set ℝ), max A (max a b) = lo := by
      rcases max_choice A (max a b) with h | h
      · exact ⟨A, Or.inl rfl, h⟩
      · rcases max_choice a b with h' | h'
        · exact ⟨a, Or.inr (Or.inl rfl), h.trans h'⟩
        · exact ⟨b, Or.inr (Or.inr rfl), h.trans h'⟩
    rw [hupe, hloe]
    rcases hall up hup lo hlo with ⟨rfl, rfl⟩ | ⟨F, hFm, hle⟩
    · exact clampMin_le_M _ Fs c
    · exact le_trans (clampMin_le _ Fs c F hFm) hle

/-! ## 4.  The eight forms of a segment, and its captured part -/

/-- `F − G` and the constant form. -/
def subF (F G : ℝ × ℝ × ℝ) : ℝ × ℝ × ℝ := (F.1 - G.1, F.2.1 - G.2.1, F.2.2 - G.2.2)
def constF (k : ℝ) : ℝ × ℝ × ℝ := (0, 0, k)

@[simp] lemma aff_subF (F G : ℝ × ℝ × ℝ) (c : ℝ × ℝ) : aff (subF F G) c = aff F c - aff G c := by
  simp only [aff, subF]; ring

@[simp] lemma aff_constF (k : ℝ) (c : ℝ × ℝ) : aff (constF k) c = k := by simp [aff, constF]

/-- The forms `up − lo` of a segment `[A, B]` on a line whose chord is `[max(lo₁, lo₂), min(up₁, up₂)]`
(the pair `(B, A)` is the constant `M = B − A` of `clampMin`). -/
def formsOf (A B : ℝ) (lo1 lo2 up1 up2 : ℝ × ℝ × ℝ) : List (ℝ × ℝ × ℝ) :=
  [subF up1 (constF A), subF up2 (constF A), subF (constF B) lo1, subF (constF B) lo2,
    subF up1 lo1, subF up1 lo2, subF up2 lo1, subF up2 lo2]

lemma min_sub_max_formsOf (A B : ℝ) (lo1 lo2 up1 up2 : ℝ × ℝ × ℝ) (c : ℝ × ℝ) :
    min B (min (aff up1 c) (aff up2 c)) - max A (max (aff lo1 c) (aff lo2 c)) =
      clampMin (B - A) (formsOf A B lo1 lo2 up1 up2) c := by
  apply min3_sub_max3
  · intro F hF
    simp only [formsOf, List.mem_cons, List.not_mem_nil, or_false] at hF
    rcases hF with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
      simp only [aff_subF, aff_constF, Set.mem_insert_iff, Set.mem_singleton_iff] <;>
      first
      | exact ⟨_, Or.inr (Or.inl rfl), _, Or.inl rfl, rfl⟩
      | exact ⟨_, Or.inr (Or.inr rfl), _, Or.inl rfl, rfl⟩
      | exact ⟨_, Or.inl rfl, _, Or.inr (Or.inl rfl), rfl⟩
      | exact ⟨_, Or.inl rfl, _, Or.inr (Or.inr rfl), rfl⟩
      | exact ⟨_, Or.inr (Or.inl rfl), _, Or.inr (Or.inl rfl), rfl⟩
      | exact ⟨_, Or.inr (Or.inl rfl), _, Or.inr (Or.inr rfl), rfl⟩
      | exact ⟨_, Or.inr (Or.inr rfl), _, Or.inr (Or.inl rfl), rfl⟩
      | exact ⟨_, Or.inr (Or.inr rfl), _, Or.inr (Or.inr rfl), rfl⟩
  · intro up hup lo hlo
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hup hlo
    simp only [formsOf, List.mem_cons, List.not_mem_nil, or_false, exists_eq_or_imp, exists_eq_left,
      aff_subF, aff_constF]
    rcases hup with rfl | rfl | rfl <;> rcases hlo with rfl | rfl | rfl <;> simp

/-- The captured part `(e, plo, phi)` of a segment entry. -/
noncomputable def partOf (e : SegE) (A B lo hi : ℝ) : SegE × ℝ × ℝ := (e, plo A B lo, phi A B lo hi)

open ZMTreeM in
/-- **A horizontal segment**: its part inside `Q(c)` is a valid part, of value
`w · max(0, clampMin (B − A) forms c)/(B − A)`. -/
theorem hseg_part {D : ℕ} (hD : 0 < D) (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ) (e : SegE)
    (hy : e.2.1 = e.2.2.2.1) (hx : e.1 < e.2.2.1) (c : ℝ × ℝ)
    (lo1 lo2 up1 up2 : ℝ × ℝ × ℝ)
    (e1 : aff lo1 c = tA θ ((e.2.1 : ℝ) / D) c) (e2 : aff lo2 c = tB θ ((e.2.1 : ℝ) / D) c)
    (e3 : aff up1 c = tC θ ((e.2.1 : ℝ) / D) c) (e4 : aff up2 c = tD θ ((e.2.1 : ℝ) / D) c) :
    let A := (e.1 : ℝ) / D; let B := (e.2.2.1 : ℝ) / D
    let p := partOf e A B (max (aff lo1 c) (aff lo2 c)) (min (aff up1 c) (aff up2 c))
    PartOK D (sq c θ 1) p ∧
      pval D p = (e.2.2.2.2 : ℝ) * max 0 (clampMin (B - A) (formsOf A B lo1 lo2 up1 up2) c) / (B - A) := by
  intro A B p
  have hDr : (0 : ℝ) < D := by exact_mod_cast hD
  have hne : e.1 ≠ e.2.2.1 := ne_of_lt hx
  have hAB : A ≤ B := div_le_div_of_nonneg_right (by exact_mod_cast hx.le) hDr.le
  obtain ⟨p1, p2, p3, p4⟩ := plo_props (lo := max (aff lo1 c) (aff lo2 c))
    (hi := min (aff up1 c) (aff up2 c)) hAB
  refine ⟨⟨Or.inr ⟨hy, hx⟩, ?_, p2, ?_, fun t ht1 ht2 => ?_⟩, ?_⟩
  · simp only [p, partOf, elo, hne, if_false]; exact p1
  · simp only [p, partOf, ehi, hne, if_false]; exact p3
  · obtain ⟨q1, q2⟩ := p4 t ht1 ht2
    show lpE D e t ∈ sq c θ 1
    rw [lpE, if_neg hne, mem_sq_iff_hchord hs hc, ← e1, ← e2, ← e3, ← e4]
    exact ⟨q1, q2⟩
  · simp only [p, partOf, pval, elo, ehi, hne, if_false, phi_sub_plo, ← min_sub_max_formsOf]
    rfl

open ZMTreeM in
/-- **A vertical segment**: as `hseg_part`, the chord being the slice of `SquareArea.lean`. -/
theorem vseg_part {D : ℕ} (hD : 0 < D) (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ) (e : SegE)
    (hx : e.1 = e.2.2.1) (hy : e.2.1 < e.2.2.2.1) (c : ℝ × ℝ)
    (lo1 lo2 up1 up2 : ℝ × ℝ × ℝ)
    (e1 : aff lo1 c = SqArea.lowX c θ ((e.1 : ℝ) / D))
    (e2 : aff lo2 c = SqArea.lowY c θ ((e.1 : ℝ) / D))
    (e3 : aff up1 c = SqArea.upX c θ ((e.1 : ℝ) / D))
    (e4 : aff up2 c = SqArea.upY c θ ((e.1 : ℝ) / D)) :
    let A := (e.2.1 : ℝ) / D; let B := (e.2.2.2.1 : ℝ) / D
    let p := partOf e A B (max (aff lo1 c) (aff lo2 c)) (min (aff up1 c) (aff up2 c))
    PartOK D (sq c θ 1) p ∧
      pval D p = (e.2.2.2.2 : ℝ) * max 0 (clampMin (B - A) (formsOf A B lo1 lo2 up1 up2) c) / (B - A) := by
  intro A B p
  have hDr : (0 : ℝ) < D := by exact_mod_cast hD
  have hAB : A ≤ B := div_le_div_of_nonneg_right (by exact_mod_cast hy.le) hDr.le
  obtain ⟨p1, p2, p3, p4⟩ := plo_props (lo := max (aff lo1 c) (aff lo2 c))
    (hi := min (aff up1 c) (aff up2 c)) hAB
  refine ⟨⟨Or.inl ⟨hx, hy⟩, ?_, p2, ?_, fun t ht1 ht2 => ?_⟩, ?_⟩
  · simp only [p, partOf, elo, hx, if_true]; exact p1
  · simp only [p, partOf, ehi, hx, if_true]; exact p3
  · obtain ⟨q1, q2⟩ := p4 t ht1 ht2
    show lpE D e t ∈ sq c θ 1
    rw [lpE, if_pos hx, SqArea.mem_sq_iff_slice hs hc, ← e1, ← e2, ← e3, ← e4]
    exact ⟨q1, q2⟩
  · simp only [p, partOf, pval, elo, ehi, hx, if_true, phi_sub_plo, ← min_sub_max_formsOf]
    rfl

end ChordE

end SquarePacking
