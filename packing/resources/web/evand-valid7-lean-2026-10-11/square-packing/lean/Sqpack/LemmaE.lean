import Sqpack.ChordE
import Sqpack.LebCorner
import Sqpack.PolyMin
import Sqpack.CovMP

/-!
# Lemma E at a fixed angle: the bound is least at a vertex of the arrangement

`search/QUADRANT_EXACT.md` §4.4.  Fix `θ` with `s = sin θ > 0`, `c = cos θ > 0`.  The lower bound

  `f(c) = Σ_segments κ · max(0, clampMin M forms c) + Σ_Lebesgue ρ · (1 − ĝ(d_x(c)) − ĝ(d_y(c)))`

(`fE`) is concave on every cell of the arrangement of a list of lines `Ls` in which every form of
every segment, and every `d` and `d − s` of every Lebesgue term, is a positive multiple of a line
(`Fixed`): on such a cell each form has a fixed sign (`ChordE.concaveOn_max0_clampMin`) and each `ĝ`
is in one regime (`convexOn_ghat`).  The cell of a centre `c` in the region `poly side` is a bounded
polygon, so by `PolyMin.exists_vertex_le` some vertex `v` of the arrangement of `side ++ Ls` lies in
`poly side` with `f v ≤ f c` (**`exists_vertex_le_fE`**).
-/

open MeasureTheory Set

namespace SquarePacking

namespace LemmaE

open ChordE PolyMin

/-! ## 1.  `ĝ` is convex in each regime -/

lemma aff_eq_val (F : ℝ × ℝ × ℝ) (p : ℝ × ℝ) : aff F p = F.1 * p.1 + F.2.1 * p.2 + F.2.2 := rfl

lemma convexOn_aff (K : Set (ℝ × ℝ)) (hK : Convex ℝ K) (F : ℝ × ℝ × ℝ) : ConvexOn ℝ K (aff F) := by
  refine ⟨hK, fun x _ y _ a b _ _ hab => ?_⟩
  simp only [aff, smul_eq_mul, Prod.smul_fst, Prod.smul_snd, Prod.fst_add, Prod.snd_add]
  have : b = 1 - a := by linarith
  subst this
  nlinarith

lemma convexOn_aff_sq (K : Set (ℝ × ℝ)) (hK : Convex ℝ K) (F : ℝ × ℝ × ℝ) :
    ConvexOn ℝ K (fun p => aff F p ^ 2) := by
  refine ⟨hK, fun x _ y _ a b ha hb hab => ?_⟩
  have e : aff F (a • x + b • y) = a * aff F x + b * aff F y := by
    simp only [aff, smul_eq_mul, Prod.smul_fst, Prod.smul_snd, Prod.fst_add, Prod.snd_add]
    have : b = 1 - a := by linarith
    subst this; ring
  simp only [smul_eq_mul]
  rw [e]
  have : b = 1 - a := by linarith
  subst this
  nlinarith [mul_nonneg ha hb, sq_nonneg (aff F x - aff F y)]

/-- In each regime of `d` (`d ≤ 0`, `0 ≤ d ≤ s`, `d ≥ s`) on `K`, `ĝ ∘ d` is convex on `K`. -/
theorem convexOn_ghat (K : Set (ℝ × ℝ)) (hK : Convex ℝ K) {s co : ℝ} (hs : 0 < s) (hc : 0 < co)
    (d : ℝ × ℝ × ℝ) (h0 : (∀ p ∈ K, aff d p ≤ 0) ∨ (∀ p ∈ K, 0 ≤ aff d p))
    (h1 : (∀ p ∈ K, aff d p ≤ s) ∨ (∀ p ∈ K, s ≤ aff d p)) :
    ConvexOn ℝ K (fun p => SqArea.ghat s co (aff d p)) := by
  rcases h0 with h0 | h0
  · refine (convexOn_const 0 hK).congr fun p hp => ?_
    simp [SqArea.ghat, h0 p hp]
  rcases h1 with h1 | h1
  · -- `ĝ = d²/(2sc)`
    have hconv := (convexOn_aff_sq K hK d).smul (show (0 : ℝ) ≤ 1 / (2 * s * co) by positivity)
    refine hconv.congr fun p hp => ?_
    simp only [SqArea.ghat, smul_eq_mul]
    split_ifs with h2 h3
    · have : aff d p = 0 := le_antisymm h2 (h0 p hp)
      rw [this]; ring
    · ring
    · exact absurd (h1 p hp) h3
  · -- `ĝ = (d − s/2)/c`
    have hconv := ((convexOn_aff K hK d).sub (concaveOn_const (s / 2) hK)).smul
      (show (0 : ℝ) ≤ 1 / co by positivity)
    refine hconv.congr fun p hp => ?_
    simp only [SqArea.ghat, smul_eq_mul, Pi.sub_apply]
    have hs' := h1 p hp
    split_ifs with h2 h3
    · linarith
    · have : aff d p = s := le_antisymm h3 hs'
      rw [this]; field_simp; ring
    · field_simp

/-! ## 2.  The bound, its cells, and the vertex -/

/-- A segment term `(κ, M, forms)`: `κ · max(0, clampMin M forms)`. -/
abbrev SegT := ℝ × ℝ × List (ℝ × ℝ × ℝ)
/-- The kind of a Lebesgue term: the plain `E′` bound, or one of the corner bounds of `E″`
(`LebCorner.lean`) with the McCormick constants `A, B, β*` (`QUADRANT_EXACT.md` §4.4). -/
inductive LebK where
  | std
  | c3 (A B bs : ℝ)
  | xc (A B bs : ℝ)

/-- The McCormick minorant of `quad(α, β) = (2cαβ + s(β² − α²))/(2c)`:
`αβ ≥ Aβ + Bα − AB` (when `(α − A)(β − B) ≥ 0`), `β² ≥ 2β*β − β*²`, `−α²` kept. -/
noncomputable def mcQ (s co A B bs α β : ℝ) : ℝ :=
  (2 * co * (A * β + B * α - A * B) + s * (2 * bs * β - bs ^ 2) - s * α ^ 2) / (2 * co)

lemma mcQ_le {s co A B bs α β : ℝ} (hs : 0 ≤ s) (hc : 0 < co) (h : 0 ≤ (α - A) * (β - B)) :
    mcQ s co A B bs α β ≤ (2 * co * α * β + s * (β ^ 2 - α ^ 2)) / (2 * co) := by
  rw [mcQ, div_le_div_iff_of_pos_right (by positivity)]
  nlinarith [mul_nonneg hc.le h, mul_nonneg hs (sq_nonneg (β - bs))]

/-- The Lebesgue bound of a kind from the cap depths: std `1 − ĝ(d_x) − ĝ(d_y)`; corner3 (frame at
the lowest vertex, `α = d_x − s`, `β = d_y`) `min(1 − ĝ_x − ĝ_y + Mc, 1 − ĝ_x)`; xcut (frame at the
leftmost vertex, `α = d_x`, `β = d_y − c`) `min(1 − ĝ_y + Mc, 1 − ĝ_x − ĝ_y)`. -/
noncomputable def lebPhi (s co : ℝ) : LebK → ℝ → ℝ → ℝ
  | .std, dx, dy => 1 - SqArea.ghat s co dx - SqArea.ghat s co dy
  | .c3 A B bs, dx, dy => min (1 - SqArea.ghat s co dx - SqArea.ghat s co dy + mcQ s co A B bs (dx - s) dy)
      (1 - SqArea.ghat s co dx)
  | .xc A B bs, dx, dy => min (1 - SqArea.ghat s co dy + mcQ s co A B bs dx (dy - co))
      (1 - SqArea.ghat s co dx - SqArea.ghat s co dy)

/-- A Lebesgue term `(ρ, d_x, d_y, kind)`: `ρ · lebPhi(kind, d_x, d_y)`. -/
abbrev LebT := ℝ × (ℝ × ℝ × ℝ) × (ℝ × ℝ × ℝ) × LebK

/-- The lower bound of Lemma E at a fixed angle. -/
noncomputable def fE (s co : ℝ) (sts : List SegT) (lts : List LebT) (p : ℝ × ℝ) : ℝ :=
  (sts.map fun t => t.1 * max 0 (clampMin t.2.1 t.2.2 p)).sum +
    (lts.map fun l => l.1 * lebPhi s co l.2.2.2 (aff l.2.1 p) (aff l.2.2.1 p)).sum

/-- `F` is a positive multiple of a line of `Ls`. -/
def PosMul (Ls : List (ℝ × ℝ × ℝ)) (F : ℝ × ℝ × ℝ) : Prop :=
  ∃ L ∈ Ls, ∃ k : ℝ, 0 < k ∧ ∀ p, aff F p = k * aff L p

/-- `F` has a fixed sign on the set `R`. -/
def SignOn (R : Set (ℝ × ℝ)) (F : ℝ × ℝ × ℝ) : Prop :=
  (∀ p ∈ R, 0 ≤ aff F p) ∨ (∀ p ∈ R, aff F p ≤ 0)

/-- `F` is a positive multiple of a line of `Ls`, or has a fixed sign on the whole region `R`. -/
def Pinned (R : Set (ℝ × ℝ)) (Ls : List (ℝ × ℝ × ℝ)) (F : ℝ × ℝ × ℝ) : Prop :=
  PosMul Ls F ∨ SignOn R F

/-- Every form of every term is fixed in sign on the cells of `Ls` inside `R` (and the weights are
`≥ 0`). -/
def Fixed (R : Set (ℝ × ℝ)) (s : ℝ) (Ls : List (ℝ × ℝ × ℝ)) (sts : List SegT) (lts : List LebT) :
    Prop :=
  (∀ t ∈ sts, 0 ≤ t.1 ∧ 0 ≤ t.2.1 ∧ ∀ F ∈ t.2.2, Pinned R Ls F) ∧
    (∀ l ∈ lts, 0 ≤ l.1 ∧ Pinned R Ls l.2.1 ∧ Pinned R Ls (subF l.2.1 (constF s)) ∧
      Pinned R Ls l.2.2.1 ∧ Pinned R Ls (subF l.2.2.1 (constF s)))

lemma Fixed.mono {R R' : Set (ℝ × ℝ)} (hRR : R' ⊆ R) {s : ℝ} {Ls : List (ℝ × ℝ × ℝ)}
    {sts : List SegT} {lts : List LebT} (h : Fixed R s Ls sts lts) : Fixed R' s Ls sts lts := by
  have pm : ∀ {F}, Pinned R Ls F → Pinned R' Ls F := fun hF => hF.imp id fun h' =>
    h'.imp (fun h1 p hp => h1 p (hRR hp)) (fun h1 p hp => h1 p (hRR hp))
  obtain ⟨h1, h2⟩ := h
  exact ⟨fun t ht => ⟨(h1 t ht).1, (h1 t ht).2.1, fun F hF => pm ((h1 t ht).2.2 F hF)⟩,
    fun l hl => ⟨(h2 l hl).1, pm (h2 l hl).2.1, pm (h2 l hl).2.2.1, pm (h2 l hl).2.2.2.1,
      pm (h2 l hl).2.2.2.2⟩⟩

/-- The line `L` oriented to be `≥ 0` at `c`. -/
noncomputable def orient (c : ℝ × ℝ) (L : ℝ × ℝ × ℝ) : ℝ × ℝ × ℝ :=
  if 0 ≤ aff L c then L else (-L.1, -L.2.1, -L.2.2)

lemma aff_orient (c : ℝ × ℝ) (L : ℝ × ℝ × ℝ) (p : ℝ × ℝ) :
    aff (orient c L) p = if 0 ≤ aff L c then aff L p else -aff L p := by
  unfold orient; split_ifs <;> simp [aff]; ring

lemma convex_poly (cs : List (ℝ × ℝ × ℝ)) : Convex ℝ (poly cs) := by
  intro x hx y hy a b ha hb hab C hC
  have e : C.1 * (a • x + b • y).1 + C.2.1 * (a • x + b • y).2 + C.2.2 =
      a * (C.1 * x.1 + C.2.1 * x.2 + C.2.2) + b * (C.1 * y.1 + C.2.1 * y.2 + C.2.2) := by
    simp only [Prod.smul_fst, Prod.smul_snd, Prod.fst_add, Prod.snd_add, smul_eq_mul]
    have : b = 1 - a := by linarith
    subst this; ring
  rw [e]
  exact add_nonneg (mul_nonneg ha (hx C hC)) (mul_nonneg hb (hy C hC))

/-- On the cell of `c`, every line of `Ls` has a fixed sign. -/
lemma sign_fixed {side Ls : List (ℝ × ℝ × ℝ)} (c : ℝ × ℝ) {L : ℝ × ℝ × ℝ} (hL : L ∈ Ls) :
    (∀ p ∈ poly (side ++ Ls.map (orient c)), 0 ≤ aff L p) ∨
      (∀ p ∈ poly (side ++ Ls.map (orient c)), aff L p ≤ 0) := by
  have hmem : orient c L ∈ side ++ Ls.map (orient c) := List.mem_append_right _ (List.mem_map_of_mem hL)
  by_cases h : 0 ≤ aff L c
  · left; intro p hp
    have := hp _ hmem
    rw [← aff_eq_val, aff_orient, if_pos h] at this; exact this
  · right; intro p hp
    have := hp _ hmem
    rw [← aff_eq_val, aff_orient, if_neg h] at this; linarith

lemma sign_of_posMul {K R : Set (ℝ × ℝ)} (hKR : K ⊆ R) {Ls : List (ℝ × ℝ × ℝ)}
    {F : ℝ × ℝ × ℝ}
    (hsign : ∀ L ∈ Ls, (∀ p ∈ K, 0 ≤ aff L p) ∨ (∀ p ∈ K, aff L p ≤ 0)) (h : Pinned R Ls F) :
    (∀ p ∈ K, 0 ≤ aff F p) ∨ (∀ p ∈ K, aff F p ≤ 0) := by
  rcases h with h | h
  swap
  · rcases h with h | h
    · exact Or.inl fun p hp => h p (hKR hp)
    · exact Or.inr fun p hp => h p (hKR hp)
  obtain ⟨L, hL, k, hk, hF⟩ := h
  rcases hsign L hL with h | h
  · left; intro p hp; rw [hF]; exact mul_nonneg hk.le (h p hp)
  · right; intro p hp; rw [hF]; exact mul_nonpos_of_nonneg_of_nonpos hk.le (h p hp)

lemma concaveOn_list_sum {ι : Type*} (K : Set (ℝ × ℝ)) (hK : Convex ℝ K) (L : List ι)
    (f : ι → ℝ × ℝ → ℝ) (hf : ∀ i ∈ L, ConcaveOn ℝ K (f i)) :
    ConcaveOn ℝ K (fun p => (L.map fun i => f i p).sum) := by
  induction L with
  | nil => simpa using concaveOn_const (0 : ℝ) hK
  | cons a L ih =>
    simp only [List.map_cons, List.sum_cons]
    exact (hf a List.mem_cons_self).add (ih fun i hi => hf i (List.mem_cons_of_mem _ hi))

/-- The McCormick term is concave in the centre (`−sα²/(2c)` with `α` affine). -/
lemma concaveOn_mcQ (K : Set (ℝ × ℝ)) (hK : Convex ℝ K) {s co : ℝ} (hs : 0 < s) (hc : 0 < co)
    (A B bs : ℝ) (Fa Fb : ℝ × ℝ × ℝ) :
    ConcaveOn ℝ K (fun p => mcQ s co A B bs (aff Fa p) (aff Fb p)) := by
  set G : ℝ × ℝ × ℝ := ((A + s * bs / co) * Fb.1 + B * Fa.1, (A + s * bs / co) * Fb.2.1 + B * Fa.2.1,
    (A + s * bs / co) * Fb.2.2 + B * Fa.2.2 - A * B - s * bs ^ 2 / (2 * co))
  have hk : 0 ≤ s / (2 * co) := by positivity
  refine ((concaveOn_aff K hK G).sub ((convexOn_aff_sq K hK Fa).smul hk)).congr fun p _ => ?_
  simp only [mcQ, G, aff, Pi.sub_apply, Pi.smul_apply, smul_eq_mul]
  field_simp
  ring

lemma concaveOn_lebPhi (K : Set (ℝ × ℝ)) (hK : Convex ℝ K) {s co : ℝ} (hs : 0 < s) (hc : 0 < co)
    (k : LebK) {Fx Fy : ℝ × ℝ × ℝ} (cx : ConvexOn ℝ K (fun p => SqArea.ghat s co (aff Fx p)))
    (cy : ConvexOn ℝ K (fun p => SqArea.ghat s co (aff Fy p))) :
    ConcaveOn ℝ K (fun p => lebPhi s co k (aff Fx p) (aff Fy p)) := by
  match k with
  | .std => exact ((concaveOn_const 1 hK).sub cx).sub cy
  | .c3 A B bs =>
    have m := concaveOn_mcQ K hK hs hc A B bs (subF Fx (constF s)) Fy
    refine ((((concaveOn_const 1 hK).sub cx).sub cy).add m |>.inf ((concaveOn_const 1 hK).sub cx)).congr
      fun p _ => ?_
    simp only [lebPhi, aff_subF, aff_constF, Pi.inf_apply, Pi.add_apply, Pi.sub_apply]
  | .xc A B bs =>
    have m := concaveOn_mcQ K hK hs hc A B bs Fx (subF Fy (constF co))
    refine ((((concaveOn_const 1 hK).sub cy).add m) |>.inf (((concaveOn_const 1 hK).sub cx).sub cy)).congr
      fun p _ => ?_
    simp only [lebPhi, aff_subF, aff_constF, Pi.inf_apply, Pi.add_apply, Pi.sub_apply]

/-- `fE` is concave on every cell. -/
theorem concaveOn_fE {s co : ℝ} (hs : 0 < s) (hc : 0 < co) {R : Set (ℝ × ℝ)}
    {Ls : List (ℝ × ℝ × ℝ)} {sts : List SegT} {lts : List LebT} (hfix : Fixed R s Ls sts lts)
    (K : Set (ℝ × ℝ)) (hKR : K ⊆ R) (hK : Convex ℝ K)
    (hsign : ∀ L ∈ Ls, (∀ p ∈ K, 0 ≤ aff L p) ∨ (∀ p ∈ K, aff L p ≤ 0)) :
    ConcaveOn ℝ K (fE s co sts lts) := by
  obtain ⟨h1, h2⟩ := hfix
  refine (concaveOn_list_sum K hK sts _ fun t ht => ?_).add
    (concaveOn_list_sum K hK lts _ fun l hl => ?_)
  · obtain ⟨hk, hM, hF⟩ := h1 t ht
    exact (concaveOn_max0_clampMin K hK hM t.2.2 fun F hFm =>
      sign_of_posMul hKR hsign (hF F hFm)).smul hk
  · obtain ⟨hρ, hx, hx', hy, hy'⟩ := h2 l hl
    have sx := sign_of_posMul hKR hsign hx
    have sx' := sign_of_posMul hKR hsign hx'
    have sy := sign_of_posMul hKR hsign hy
    have sy' := sign_of_posMul hKR hsign hy'
    have cx := convexOn_ghat K hK hs hc l.2.1 (Or.symm sx) (by
      rcases sx' with h | h
      · right; intro p hp; have := h p hp; simp only [aff_subF, aff_constF] at this; linarith
      · left; intro p hp; have := h p hp; simp only [aff_subF, aff_constF] at this; linarith)
    have cy := convexOn_ghat K hK hs hc l.2.2.1 (Or.symm sy) (by
      rcases sy' with h | h
      · right; intro p hp; have := h p hp; simp only [aff_subF, aff_constF] at this; linarith
      · left; intro p hp; have := h p hp; simp only [aff_subF, aff_constF] at this; linarith)
    exact (concaveOn_lebPhi K hK hs hc l.2.2.2 cx cy).smul hρ

/-- **Lemma E's vertex reduction, at a fixed angle.**  On the bounded region `poly side`, `fE` at any
point is at least its value at some vertex of the arrangement of `side ++ Ls` inside the region. -/
theorem exists_vertex_le_fE {s co : ℝ} (hs : 0 < s) (hc : 0 < co) {side Ls : List (ℝ × ℝ × ℝ)}
    (hb : Bornology.IsBounded (poly side)) {sts : List SegT} {lts : List LebT}
    (hfix : Fixed (poly side) s Ls sts lts) {c : ℝ × ℝ} (hcs : c ∈ poly side) :
    ∃ v ∈ poly side, (∃ C1 ∈ side ++ Ls, ∃ C2 ∈ side ++ Ls, C1.1 * C2.2.1 - C1.2.1 * C2.1 ≠ 0 ∧
      aff C1 v = 0 ∧ aff C2 v = 0) ∧ fE s co sts lts v ≤ fE s co sts lts c := by
  set cs := side ++ Ls.map (orient c)
  have hsub : poly cs ⊆ poly side := fun p hp C hC => hp C (List.mem_append_left _ hC)
  have hcK : c ∈ poly cs := by
    intro C hC
    rcases List.mem_append.mp hC with h | h
    · exact hcs C h
    · obtain ⟨L, _, rfl⟩ := List.mem_map.mp h
      rw [← aff_eq_val, aff_orient]
      split_ifs with h' <;> [exact h'; linarith]
  have hconc := concaveOn_fE hs hc hfix (poly cs) hsub (convex_poly cs) fun L hL => sign_fixed c hL
  obtain ⟨v, hv, ⟨C1, hC1, C2, hC2, hdet, ht1, ht2⟩, hle⟩ :=
    exists_vertex_le cs (hb.subset hsub) _ hconc hcK
  -- a constraint of `cs` is a constraint of `side ++ Ls` up to sign
  have back : ∀ C ∈ cs, ∃ C' ∈ side ++ Ls, (C' = C ∨ C' = (-C.1, -C.2.1, -C.2.2)) := by
    intro C hC
    rcases List.mem_append.mp hC with h | h
    · exact ⟨C, List.mem_append_left _ h, Or.inl rfl⟩
    · obtain ⟨L, hL, rfl⟩ := List.mem_map.mp h
      refine ⟨L, List.mem_append_right _ hL, ?_⟩
      unfold orient; split_ifs
      · exact Or.inl rfl
      · right; simp
  obtain ⟨D1, hD1, e1⟩ := back C1 hC1
  obtain ⟨D2, hD2, e2⟩ := back C2 hC2
  refine ⟨v, hsub hv, ⟨D1, hD1, D2, hD2, ?_, ?_, ?_⟩, hle⟩
  · rcases e1 with rfl | rfl <;> rcases e2 with rfl | rfl
    · exact hdet
    · intro h; apply hdet; dsimp only at h; linarith
    · intro h; apply hdet; dsimp only at h; linarith
    · intro h; apply hdet; dsimp only at h; linarith
  · rcases e1 with rfl | rfl
    · exact ht1
    · simp only [aff]; linarith
  · rcases e2 with rfl | rfl
    · exact ht2
    · simp only [aff]; linarith

/-! ## 3.  The bound is at most the mass at the pose -/

section pose

open ZMTreeM

variable (θ : ℝ)

/-- The chord ends on a horizontal line `y = η`, as affine forms of the centre. -/
noncomputable def chA (η : ℝ) : ℝ × ℝ × ℝ :=
  (1, Real.sin θ / Real.cos θ, (-(1 / 2) - η * Real.sin θ) / Real.cos θ)
noncomputable def chB (η : ℝ) : ℝ × ℝ × ℝ :=
  (1, -(Real.cos θ / Real.sin θ), (η * Real.cos θ - 1 / 2) / Real.sin θ)
noncomputable def chC (η : ℝ) : ℝ × ℝ × ℝ :=
  (1, Real.sin θ / Real.cos θ, (1 / 2 - η * Real.sin θ) / Real.cos θ)
noncomputable def chD (η : ℝ) : ℝ × ℝ × ℝ :=
  (1, -(Real.cos θ / Real.sin θ), (η * Real.cos θ + 1 / 2) / Real.sin θ)

/-- The chord ends on a vertical line `x = ξ`. -/
noncomputable def vLX (ξ : ℝ) : ℝ × ℝ × ℝ :=
  (Real.cos θ / Real.sin θ, 1, (-(1 / 2) - ξ * Real.cos θ) / Real.sin θ)
noncomputable def vUX (ξ : ℝ) : ℝ × ℝ × ℝ :=
  (Real.cos θ / Real.sin θ, 1, (1 / 2 - ξ * Real.cos θ) / Real.sin θ)
noncomputable def vLY (ξ : ℝ) : ℝ × ℝ × ℝ :=
  (-(Real.sin θ / Real.cos θ), 1, (ξ * Real.sin θ - 1 / 2) / Real.cos θ)
noncomputable def vUY (ξ : ℝ) : ℝ × ℝ × ℝ :=
  (-(Real.sin θ / Real.cos θ), 1, (ξ * Real.sin θ + 1 / 2) / Real.cos θ)

variable {θ}

lemma aff_chA (hc : 0 < Real.cos θ) (η : ℝ) (c : ℝ × ℝ) : aff (chA θ η) c = tA θ η c := by
  simp only [aff, chA, tA]; field_simp; ring
lemma aff_chB (hs : 0 < Real.sin θ) (η : ℝ) (c : ℝ × ℝ) : aff (chB θ η) c = tB θ η c := by
  simp only [aff, chB, tB]; field_simp; ring
lemma aff_chC (hc : 0 < Real.cos θ) (η : ℝ) (c : ℝ × ℝ) : aff (chC θ η) c = tC θ η c := by
  simp only [aff, chC, tC]; field_simp; ring
lemma aff_chD (hs : 0 < Real.sin θ) (η : ℝ) (c : ℝ × ℝ) : aff (chD θ η) c = tD θ η c := by
  simp only [aff, chD, tD]; field_simp; ring
lemma aff_vLX (hs : 0 < Real.sin θ) (ξ : ℝ) (c : ℝ × ℝ) : aff (vLX θ ξ) c = SqArea.lowX c θ ξ := by
  simp only [aff, vLX, SqArea.lowX]; field_simp; ring
lemma aff_vUX (hs : 0 < Real.sin θ) (ξ : ℝ) (c : ℝ × ℝ) : aff (vUX θ ξ) c = SqArea.upX c θ ξ := by
  simp only [aff, vUX, SqArea.upX]; field_simp; ring
lemma aff_vLY (hc : 0 < Real.cos θ) (ξ : ℝ) (c : ℝ × ℝ) : aff (vLY θ ξ) c = SqArea.lowY c θ ξ := by
  simp only [aff, vLY, SqArea.lowY]; field_simp; ring
lemma aff_vUY (hc : 0 < Real.cos θ) (ξ : ℝ) (c : ℝ × ℝ) : aff (vUY θ ξ) c = SqArea.upY c θ ξ := by
  simp only [aff, vUY, SqArea.upY]; field_simp; ring

variable (θ)

/-- The term of a horizontal segment entry. -/
noncomputable def hsegT (D : ℕ) (e : SegE) : SegT :=
  let A := (e.1 : ℝ) / D; let B := (e.2.2.1 : ℝ) / D; let η := (e.2.1 : ℝ) / D
  ((e.2.2.2.2 : ℝ) / (B - A), B - A, formsOf A B (chA θ η) (chB θ η) (chC θ η) (chD θ η))

/-- The term of a vertical segment entry. -/
noncomputable def vsegT (D : ℕ) (e : SegE) : SegT :=
  let A := (e.2.1 : ℝ) / D; let B := (e.2.2.2.1 : ℝ) / D; let ξ := (e.1 : ℝ) / D
  ((e.2.2.2.2 : ℝ) / (B - A), B - A, formsOf A B (vLX θ ξ) (vLY θ ξ) (vUX θ ξ) (vUY θ ξ))

/-- The corner kind of a rectangle entry: none, or corner3 / xcut with the McCormick anchor
`(xa, ya)/q` (a corner of the box) and the tangent point `ym/q` of `β²`. -/
inductive CK where
  | std
  | c3 (xa ya ym q : ℕ)
  | xc (xa ya ym q : ℕ)
  deriving DecidableEq

/-- A rectangle entry with the modes of its two caps (`none` = std, `some (n, m)` = `tan` at
`d* = n/m`) and its corner kind. -/
abbrev RectM := RectE × Option (ℕ × ℕ) × Option (ℕ × ℕ) × CK

/-- The `tan` transform of a cap form `d` (`d* = n/m`): `d' = (k/s) d + c − k²/(2s) − k d*/s + s/2`,
`k = s + c − d*`, so that `ĝ(d') ≥ (d' − s/2)/c = 1 − T_{d*}(d)` (`SqArea.one_sub_tanT`). -/
noncomputable def tanF (n m : ℕ) (F : ℝ × ℝ × ℝ) : ℝ × ℝ × ℝ :=
  let s := Real.sin θ; let co := Real.cos θ; let ds := (n : ℝ) / m; let k := s + co - ds
  (k / s * F.1, k / s * F.2.1, k / s * F.2.2 + (co - k ^ 2 / (2 * s) - k * ds / s + s / 2))

/-- The cap form in a mode: `none` = std (`ĝ(d)`), `some (n, m)` = `tan` at `d* = n/m`. -/
noncomputable def capFm : Option (ℕ × ℕ) → (ℝ × ℝ × ℝ) → ℝ × ℝ × ℝ
  | none, F => F
  | some (n, m), F => tanF θ n m F

/-- The condition of a mode at a depth `d`: none for std; `d* ≤ 1` and `d ≥ max(s, c)` for `tan`. -/
def ModeOk : Option (ℕ × ℕ) → ℝ → Prop
  | none, _ => True
  | some (n, m), d => (n : ℝ) / m ≤ 1 ∧ max (Real.sin θ) (Real.cos θ) ≤ d

/-- The Lebesgue kind of an entry at `θ`: the McCormick constants are `α`, `β` at the anchor and
`β` at `ym/q` (corner3: `α = d_x − s`, `β = d_y`; xcut: `α = d_x`, `β = d_y − c`). -/
noncomputable def kindK (D : ℕ) (r : RectM) : LebK :=
  let s := Real.sin θ; let co := Real.cos θ
  let X := (r.1.1 : ℝ) / D; let Y := (r.1.2.1 : ℝ) / D
  match r.2.2.2 with
  | .std => .std
  | .c3 xa ya ym q => .c3 (X - xa / q + (co - s) / 2) (Y - ya / q + (s + co) / 2) (Y - ym / q + (s + co) / 2)
  | .xc xa ya ym q => .xc (X - xa / q + (co + s) / 2) (Y - ya / q - (co - s) / 2) (Y - ym / q - (co - s) / 2)

/-- The conditions of a corner kind at the centre `c` (`LebCorner.area_ge_corner3`, `area_ge_xcut`),
with std caps and the anchor condition `(α − A)(β − B) ≥ 0`. -/
def KindOk (D : ℕ) (r : RectM) (c : ℝ × ℝ) : Prop :=
  let s := Real.sin θ; let co := Real.cos θ
  let X := (r.1.1 : ℝ) / D; let Y := (r.1.2.1 : ℝ) / D
  match r.2.2.2 with
  | .std => True
  | .c3 xa ya _ q => r.2.1 = none ∧ r.2.2.1 = none ∧
      0 ≤ X - c.1 + (co - s) / 2 ∧ X - c.1 + (co - s) / 2 ≤ co ∧ Y - c.2 + (s + co) / 2 ≤ co ∧
      co * (X - c.1 + (co - s) / 2) + s * (Y - c.2 + (s + co) / 2) ≤ 1 ∧
      0 ≤ ((xa : ℝ) / q - c.1) * ((ya : ℝ) / q - c.2)
  | .xc xa ya _ q => r.2.1 = none ∧ r.2.2.1 = none ∧
      X - c.1 + (co + s) / 2 ≤ s ∧ Y - c.2 - (co - s) / 2 ≤ 0 ∧
      0 ≤ ((xa : ℝ) / q - c.1) * ((ya : ℝ) / q - c.2)

/-- The term of a rectangle entry with its cap modes: `d_x = X0/D − x_min`, `d_y = Y0/D − y_min`,
each possibly `tan`-transformed. -/
noncomputable def rectT (D : ℕ) (r : RectM) : LebT :=
  ((r.1.2.2.2.2 : ℝ), capFm θ r.2.1 (-1, 0, (r.1.1 : ℝ) / D + (Real.cos θ + Real.sin θ) / 2),
    capFm θ r.2.2.1 (0, -1, (r.1.2.1 : ℝ) / D + (Real.cos θ + Real.sin θ) / 2), kindK θ D r)

variable {θ}

lemma aff_tanF (n m : ℕ) (F : ℝ × ℝ × ℝ) (c : ℝ × ℝ) :
    aff (tanF θ n m F) c = (Real.sin θ + Real.cos θ - (n : ℝ) / m) / Real.sin θ * aff F c +
      (Real.cos θ - (Real.sin θ + Real.cos θ - (n : ℝ) / m) ^ 2 / (2 * Real.sin θ) -
        (Real.sin θ + Real.cos θ - (n : ℝ) / m) * ((n : ℝ) / m) / Real.sin θ + Real.sin θ / 2) := by
  simp only [aff, tanF]; ring

/-- The left cap is at most `ĝ` of its mode's form. -/
lemma cap_le_mode (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ) {c : ℝ × ℝ} {a : ℝ}
    (mo : Option (ℕ × ℕ)) {F : ℝ × ℝ × ℝ} (hF : aff F c = a - SqArea.xmin c θ)
    (hm : ModeOk θ mo (a - SqArea.xmin c θ)) :
    volume (sq c θ 1 ∩ {p | p.1 < a}) ≤
      ENNReal.ofReal (SqArea.ghat (Real.sin θ) (Real.cos θ) (aff (capFm θ mo F) c)) := by
  match mo, hm with
  | none, _ => rw [capFm, hF]; exact SqArea.cap_le_ghat hs hc a
  | some (n, m), ⟨h1, h2⟩ =>
    refine (SqArea.cap_le_tan hs hc h1 h2).trans (ENNReal.ofReal_le_ofReal ?_)
    rw [SqArea.one_sub_tanT hs hc, capFm, aff_tanF, hF]
    exact SqArea.lin_le_ghat hs hc _

/-- The bottom cap is at most `ĝ` of its mode's form. -/
lemma bottom_cap_le_mode (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ) {c : ℝ × ℝ} {a : ℝ}
    (mo : Option (ℕ × ℕ)) {F : ℝ × ℝ × ℝ} (hF : aff F c = a - SqArea.ymin c θ)
    (hm : ModeOk θ mo (a - SqArea.ymin c θ)) :
    volume (sq c θ 1 ∩ {p | p.2 < a}) ≤
      ENNReal.ofReal (SqArea.ghat (Real.sin θ) (Real.cos θ) (aff (capFm θ mo F) c)) := by
  match mo, hm with
  | none, _ => rw [capFm, hF]; exact SqArea.bottom_cap_le_ghat hs hc a
  | some (n, m), ⟨h1, h2⟩ =>
    refine (SqArea.bottom_cap_le_tan hs hc h1 h2).trans (ENNReal.ofReal_le_ofReal ?_)
    rw [SqArea.one_sub_tanT hs hc, capFm, aff_tanF, hF]
    exact SqArea.lin_le_ghat hs hc _

/-- **The bound is at most the segment and rectangle mass** at the pose (claimed horizontal
segments `chs`, vertical `cvs`, rectangles `crs` whose square lies left of and below their far
sides). -/
theorem fE_le_mass {D : ℕ} (hD : 0 < D) (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ) (c : ℝ × ℝ)
    {segs : List SegE} {rects : List RectE} {chs cvs : List SegE}
    (hnd : (chs ++ cvs).Nodup) (hch : ∀ e ∈ chs, e ∈ segs ∧ e.2.1 = e.2.2.2.1 ∧ e.1 < e.2.2.1)
    (hcv : ∀ e ∈ cvs, e ∈ segs ∧ e.1 = e.2.2.1 ∧ e.2.1 < e.2.2.2.1) {crs : List RectM}
    (hcr : (crs.map Prod.fst).Nodup)
    (hcrs : ∀ r ∈ crs, r.1 ∈ rects ∧
      (∀ p ∈ sq c θ 1, p.1 ≤ (r.1.2.2.1 : ℝ) / D ∧ p.2 ≤ (r.1.2.2.2.1 : ℝ) / D) ∧
      ModeOk θ r.2.1 ((r.1.1 : ℝ) / D - SqArea.xmin c θ) ∧
      ModeOk θ r.2.2.1 ((r.1.2.1 : ℝ) / D - SqArea.ymin c θ) ∧ KindOk θ D r c) :
    fE (Real.sin θ) (Real.cos θ) (chs.map (hsegT θ D) ++ cvs.map (vsegT θ D))
        (crs.map (rectT θ D)) c ≤
      segMass D segs (sq c θ 1) + rectMass D rects (sq c θ 1) := by
  classical
  have hDr : (0 : ℝ) < D := by exact_mod_cast hD
  -- segments
  set hp : SegE → SegE × ℝ × ℝ := fun e =>
    partOf e ((e.1 : ℝ) / D) ((e.2.2.1 : ℝ) / D)
      (max (aff (chA θ ((e.2.1 : ℝ) / D)) c) (aff (chB θ ((e.2.1 : ℝ) / D)) c))
      (min (aff (chC θ ((e.2.1 : ℝ) / D)) c) (aff (chD θ ((e.2.1 : ℝ) / D)) c))
  set vp : SegE → SegE × ℝ × ℝ := fun e =>
    partOf e ((e.2.1 : ℝ) / D) ((e.2.2.2.1 : ℝ) / D)
      (max (aff (vLX θ ((e.1 : ℝ) / D)) c) (aff (vLY θ ((e.1 : ℝ) / D)) c))
      (min (aff (vUX θ ((e.1 : ℝ) / D)) c) (aff (vUY θ ((e.1 : ℝ) / D)) c))
  set parts := chs.map hp ++ cvs.map vp with hparts
  have hHp : ∀ e ∈ chs, PartOK D (sq c θ 1) (hp e) ∧ pval D (hp e) =
      (hsegT θ D e).1 * max 0 (clampMin (hsegT θ D e).2.1 (hsegT θ D e).2.2 c) := by
    intro e he
    obtain ⟨_, hy, hx⟩ := hch e he
    obtain ⟨h1, h2⟩ := hseg_part hD hs hc e hy hx c _ _ _ _ (aff_chA hc _ c) (aff_chB hs _ c)
      (aff_chC hc _ c) (aff_chD hs _ c)
    refine ⟨h1, ?_⟩
    rw [h2]; simp only [hsegT]; ring
  have hVp : ∀ e ∈ cvs, PartOK D (sq c θ 1) (vp e) ∧ pval D (vp e) =
      (vsegT θ D e).1 * max 0 (clampMin (vsegT θ D e).2.1 (vsegT θ D e).2.2 c) := by
    intro e he
    obtain ⟨_, hx, hy⟩ := hcv e he
    obtain ⟨h1, h2⟩ := vseg_part hD hs hc e hx hy c _ _ _ _ (aff_vLX hs _ c) (aff_vLY hc _ c)
      (aff_vUX hs _ c) (aff_vUY hc _ c)
    refine ⟨h1, ?_⟩
    rw [h2]; simp only [vsegT]; ring
  have hfst : parts.map Prod.fst = chs ++ cvs := by
    simp only [hparts, List.map_append, List.map_map]
    congr 1
    · rw [show Prod.fst ∘ hp = id from rfl, List.map_id]
    · rw [show Prod.fst ∘ vp = id from rfl, List.map_id]
  have hpw : parts.Pairwise (fun p q => p.1 = q.1 → p.2.2 ≤ q.2.1) := by
    have h := hnd
    rw [← hfst, List.Nodup, List.pairwise_map] at h
    exact h.imp fun hne heq => absurd heq hne
  have hmem : ∀ p ∈ parts, p.1 ∈ segs.toFinset := by
    intro p hpm
    rcases List.mem_append.mp hpm with h | h
    · obtain ⟨e, he, rfl⟩ := List.mem_map.mp h; exact List.mem_toFinset.mpr (hch e he).1
    · obtain ⟨e, he, rfl⟩ := List.mem_map.mp h; exact List.mem_toFinset.mpr (hcv e he).1
  have hok : ∀ p ∈ parts, PartOK D (sq c θ 1) p := by
    intro p hpm
    rcases List.mem_append.mp hpm with h | h
    · obtain ⟨e, he, rfl⟩ := List.mem_map.mp h; exact (hHp e he).1
    · obtain ⟨e, he, rfl⟩ := List.mem_map.mp h; exact (hVp e he).1
  have Sg := parts_le_segMass hD segs (sq c θ 1) parts hmem hok hpw
  have hsum : (parts.map (pval D)).sum =
      ((chs.map (hsegT θ D) ++ cvs.map (vsegT θ D)).map
        fun t => t.1 * max 0 (clampMin t.2.1 t.2.2 c)).sum := by
    rw [hparts, List.map_append, List.map_append, List.sum_append, List.sum_append, List.map_map,
      List.map_map, List.map_map, List.map_map]
    congr 1
    · congr 1; exact List.map_congr_left fun e he => (hHp e he).2
    · congr 1; exact List.map_congr_left fun e he => (hVp e he).2
  -- rectangles
  have Rc : ((crs.map (rectT θ D)).map fun l => l.1 * lebPhi (Real.sin θ) (Real.cos θ) l.2.2.2
      (aff l.2.1 c) (aff l.2.2.1 c)).sum ≤ rectMass D rects (sq c θ 1) := by
    have hterm : ∀ r ∈ crs, (rectT θ D r).1 * lebPhi (Real.sin θ) (Real.cos θ) (rectT θ D r).2.2.2
        (aff (rectT θ D r).2.1 c) (aff (rectT θ D r).2.2.1 c) ≤
        (r.1.2.2.2.2 : ℝ) * (volume (sq c θ 1 ∩ rectSet D r.1)).toReal := by
      intro r hr
      obtain ⟨_, hb, mx, my, hk⟩ := hcrs r hr
      refine mul_le_mul_of_nonneg_left ?_ (Nat.cast_nonneg _)
      have ex : aff ((-1, 0, (r.1.1 : ℝ) / D + (Real.cos θ + Real.sin θ) / 2) : ℝ × ℝ × ℝ) c =
          (r.1.1 : ℝ) / D - SqArea.xmin c θ := by
        simp only [aff, SqArea.xmin]; ring
      have ey : aff ((0, -1, (r.1.2.1 : ℝ) / D + (Real.cos θ + Real.sin θ) / 2) : ℝ × ℝ × ℝ) c =
          (r.1.2.1 : ℝ) / D - SqArea.ymin c θ := by
        simp only [aff, SqArea.ymin]; ring
      have gx := cap_le_mode hs hc r.2.1 ex mx
      have gy := bottom_cap_le_mode hs hc r.2.2.1 ey my
      obtain ⟨R, m1, m2, k⟩ := r
      simp only [rectT] at gx gy ⊢
      match k, hk with
      | .std, _ =>
        exact SqArea.area_ge_caps (SqArea.ghat_nonneg hs hc) (SqArea.ghat_nonneg hs hc) hb gx gy
      | .c3 xa ya ym q, hk =>
        obtain ⟨rfl, rfl, h1, h2, h3, h4, h5⟩ := hk
        simp only [capFm] at gx gy ⊢
        rw [ex, ey] at *
        simp only [kindK, lebPhi]
        refine le_trans (le_of_eq ?_) (SqArea.area_ge_corner3 (M := mcQ (Real.sin θ) (Real.cos θ)
          ((R.1 : ℝ) / D - xa / q + (Real.cos θ - Real.sin θ) / 2)
          ((R.2.1 : ℝ) / D - ya / q + (Real.sin θ + Real.cos θ) / 2)
          ((R.2.1 : ℝ) / D - ym / q + (Real.sin θ + Real.cos θ) / 2)
          ((R.1 : ℝ) / D - c.1 + (Real.cos θ - Real.sin θ) / 2) ((R.2.1 : ℝ) / D - c.2 + (Real.sin θ + Real.cos θ) / 2))
          hs hc hb gx gy (SqArea.ghat_nonneg hs hc) (SqArea.ghat_nonneg hs hc) h1 h2 h3 h4
          (mcQ_le hs.le hc (by convert h5 using 2 <;> ring)))
        simp only [aff, SqArea.xmin, SqArea.ymin]; ring_nf
      | .xc xa ya ym q, hk =>
        obtain ⟨rfl, rfl, h1, h2, h5⟩ := hk
        simp only [capFm] at gx gy ⊢
        rw [ex, ey] at *
        simp only [kindK, lebPhi]
        refine le_trans (le_of_eq ?_) (SqArea.area_ge_xcut (M := mcQ (Real.sin θ) (Real.cos θ)
          ((R.1 : ℝ) / D - xa / q + (Real.cos θ + Real.sin θ) / 2)
          ((R.2.1 : ℝ) / D - ya / q - (Real.cos θ - Real.sin θ) / 2)
          ((R.2.1 : ℝ) / D - ym / q - (Real.cos θ - Real.sin θ) / 2)
          ((R.1 : ℝ) / D - c.1 + (Real.cos θ + Real.sin θ) / 2) ((R.2.1 : ℝ) / D - c.2 - (Real.cos θ - Real.sin θ) / 2))
          hs hc hb gx gy (SqArea.ghat_nonneg hs hc) (SqArea.ghat_nonneg hs hc) h1 h2
          (mcQ_le hs.le hc (by convert h5 using 2 <;> ring)))
        simp only [aff, SqArea.xmin, SqArea.ymin]; ring_nf
    rw [List.map_map]
    refine le_trans (List.sum_le_sum fun r hr => hterm r hr) ?_
    have hmap : (crs.map fun r => (r.1.2.2.2.2 : ℝ) * (volume (sq c θ 1 ∩ rectSet D r.1)).toReal) =
        (crs.map Prod.fst).map fun e => (e.2.2.2.2 : ℝ) * (volume (sq c θ 1 ∩ rectSet D e)).toReal := by
      rw [List.map_map]; rfl
    rw [hmap, rectMass, ← List.sum_toFinset _ hcr]
    refine Finset.sum_le_sum_of_subset_of_nonneg (fun e he => ?_) fun _ _ _ =>
      mul_nonneg (Nat.cast_nonneg _) ENNReal.toReal_nonneg
    obtain ⟨r, hr, rfl⟩ := List.mem_map.mp (List.mem_toFinset.mp he)
    exact List.mem_toFinset.mpr (hcrs r hr).1
  simp only [fE]
  linarith

end pose

end LemmaE

end SquarePacking
