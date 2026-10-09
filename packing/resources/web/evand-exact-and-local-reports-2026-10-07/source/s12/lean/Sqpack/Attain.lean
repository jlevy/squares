import Sqpack.S32

/-!
# `s(n)` is attained

`minSide n = sInf {s | Packs n s}` is defined as an infimum.  Here we show that for `n ≥ 1` it is
a **minimum**: there is a packing of `n` unit squares in `[0, minSide n]²`.

* `packs_mono` — a packing in `box s` is a packing in `box t` for `t ≥ s`.
* `packs_nonempty` — `Packs n n` (the grid), so the set of sides is nonempty.
* `one_le_of_packs` — for `n ≥ 1`, any side `s` with `Packs n s` has `1 ≤ s`; hence `BddBelow`.
* **`isLeast_minSide`** — `IsLeast {s | Packs n s} (minSide n)` for `n ≥ 1`.
* `packs_minSide`, `packs_iff_minSide_le`, `le_minSide_iff`, `minSide_eq_iff_isLeast`.

Proof of attainment: take sides `s_m ↓ minSide n` with packings; reduce angles to `[0, 2π)`
(`toIcoMod`; the squares only depend on `cos θ`, `sin θ`); all centres lie in `box s_0` and the
parameters in a compact set, so a subsequence converges.  Containment passes to the limit
through the parametrisation `sqPt c θ a b` of the closed square (a continuous function of `(c, θ)`
landing in the closed set `{(q, t) | q ∈ box t}`); disjointness of interiors passes to the limit
because `{(c, θ) | p ∈ sqInt c θ 1}` is open, so a common interior point of two limit squares is a
common interior point of the approximating squares for large `m`.
-/

open Filter Topology

namespace SquarePacking

/-- The point with rotated coordinates `(a, b)` in the frame of centre `c`, angle `θ`. -/
noncomputable def sqPt (c : ℝ × ℝ) (θ a b : ℝ) : ℝ × ℝ :=
  (c.1 + a * Real.cos θ - b * Real.sin θ, c.2 + a * Real.sin θ + b * Real.cos θ)

lemma coord_sqPt (c : ℝ × ℝ) (θ a b : ℝ) : coord c θ (sqPt c θ a b) = (a, b) := by
  have h := Real.cos_sq_add_sin_sq θ
  simp only [coord, sqPt, Prod.mk.injEq]
  constructor
  · linear_combination a * h
  · linear_combination b * h

lemma sqPt_coord (c : ℝ × ℝ) (θ : ℝ) (p : ℝ × ℝ) :
    sqPt c θ (coord c θ p).1 (coord c θ p).2 = p := by
  have h := Real.cos_sq_add_sin_sq θ
  simp only [coord, sqPt]
  ext
  · simp only; linear_combination (p.1 - c.1) * h
  · simp only; linear_combination (p.2 - c.2) * h

lemma continuous_sqPt (a b : ℝ) : Continuous fun x : (ℝ × ℝ) × ℝ => sqPt x.1 x.2 a b := by
  unfold sqPt; fun_prop

lemma continuous_coord_pose (p : ℝ × ℝ) : Continuous fun x : (ℝ × ℝ) × ℝ => coord x.1 x.2 p := by
  unfold coord; fun_prop

lemma coord_toIcoMod (c : ℝ × ℝ) (θ : ℝ) (p : ℝ × ℝ) :
    coord c (toIcoMod Real.two_pi_pos 0 θ) p = coord c θ p := by
  rw [← self_sub_toIcoDiv_zsmul, zsmul_eq_mul]
  simp only [coord, Real.cos_sub_int_mul_two_pi, Real.sin_sub_int_mul_two_pi]

lemma box_mono {s t : ℝ} (h : s ≤ t) : box s ⊆ box t := by
  rintro p ⟨h1, h2, h3, h4⟩; exact ⟨h1, by linarith, h3, by linarith⟩

lemma isClosed_box_graph : IsClosed {x : (ℝ × ℝ) × ℝ | x.1 ∈ box x.2} := by
  have e : {x : (ℝ × ℝ) × ℝ | x.1 ∈ box x.2} = {x | 0 ≤ x.1.1} ∩ ({x | x.1.1 ≤ x.2} ∩
      ({x | 0 ≤ x.1.2} ∩ {x | x.1.2 ≤ x.2})) := rfl
  rw [e]
  exact (isClosed_le continuous_const (by fun_prop)).inter ((isClosed_le (by fun_prop)
    (by fun_prop)).inter ((isClosed_le continuous_const (by fun_prop)).inter
    (isClosed_le (by fun_prop) (by fun_prop))))

lemma center_mem_sq (c : ℝ × ℝ) (θ : ℝ) : c ∈ sq c θ 1 := by
  simp [sq, coord]

/-- **Monotonicity**: a packing in `[0,s]²` is a packing in `[0,t]²` for `t ≥ s`. -/
theorem packs_mono {n : ℕ} {s t : ℝ} (h : Packs n s) (hst : s ≤ t) : Packs n t := by
  obtain ⟨ctr, ang, hin, hdisj⟩ := h
  exact ⟨ctr, ang, fun i => (hin i).trans (box_mono hst), hdisj⟩

/-- The `n × n` grid packs `n` squares: the set of sides is nonempty. -/
theorem packs_nonempty (n : ℕ) : Packs n n :=
  packs_grid n n (Nat.le_mul_self n)

/-- A closed unit square (any angle) inside `[0,s]²` forces `s ≥ 1`. -/
theorem nonempty_packs (n : ℕ) : ({s | Packs n s} : Set ℝ).Nonempty :=
  ⟨_, packs_nonempty n⟩

theorem one_le_of_sq_subset_box {c : ℝ × ℝ} {θ s : ℝ} (h : sq c θ 1 ⊆ box s) : 1 ≤ s := by
  have hm : ∀ a b : ℝ, |a| ≤ 1/2 → |b| ≤ 1/2 → sqPt c θ a b ∈ box s := fun a b ha hb =>
    h (by simp only [sq, Set.mem_ofPred_eq, coord_sqPt]; exact ⟨by linarith, by linarith⟩)
  have hh : |(1:ℝ)/2| ≤ 1/2 := by norm_num
  have hl : |-(1:ℝ)/2| ≤ 1/2 := by norm_num
  obtain ⟨a1, a2, -, -⟩ := hm (1/2) (-1/2) hh hl
  obtain ⟨b1, b2, -, -⟩ := hm (-1/2) (1/2) hl hh
  obtain ⟨c1, c2, -, -⟩ := hm (1/2) (1/2) hh hh
  obtain ⟨d1, d2, -, -⟩ := hm (-1/2) (-1/2) hl hl
  simp only [sqPt] at a1 a2 b1 b2 c1 c2 d1 d2
  have hcs := Real.cos_sq_add_sin_sq θ
  have hs0 : 0 ≤ s := by linarith
  -- `|cos θ + sin θ| ≤ s` and `|cos θ - sin θ| ≤ s`, and their squares sum to `2`
  have e1 : (Real.cos θ + Real.sin θ) ^ 2 ≤ s ^ 2 := sq_le_sq' (by linarith) (by linarith)
  have e2 : (Real.cos θ - Real.sin θ) ^ 2 ≤ s ^ 2 := sq_le_sq' (by linarith) (by linarith)
  nlinarith

/-- For `n ≥ 1`, every side `s` with `Packs n s` has `s ≥ 1`. -/
theorem one_le_of_packs {n : ℕ} (hn : 1 ≤ n) {s : ℝ} (h : Packs n s) : 1 ≤ s := by
  obtain ⟨ctr, ang, hin, -⟩ := h
  exact one_le_of_sq_subset_box (hin ⟨0, hn⟩)

theorem bddBelow_packs {n : ℕ} (hn : 1 ≤ n) : BddBelow {s | Packs n s} :=
  ⟨1, fun _ hs => one_le_of_packs hn hs⟩

theorem minSide_le {n : ℕ} {s : ℝ} (hn : 1 ≤ n) (h : Packs n s) : minSide n ≤ s :=
  csInf_le (bddBelow_packs hn) h

theorem le_minSide_iff {n : ℕ} (hn : 1 ≤ n) {a : ℝ} :
    a ≤ minSide n ↔ ∀ s, Packs n s → a ≤ s :=
  le_csInf_iff (bddBelow_packs hn) (nonempty_packs n)

/-- Replace each angle by its representative in `[0, 2π)`: the squares do not change. -/
lemma packs_normalize {n : ℕ} {s : ℝ} (h : Packs n s) :
    ∃ (ctr : Fin n → ℝ × ℝ) (ang : Fin n → ℝ), (∀ i, ang i ∈ Set.Icc 0 (2 * Real.pi)) ∧
      (∀ i, sq (ctr i) (ang i) 1 ⊆ box s) ∧
      ∀ i j, i ≠ j → Disjoint (sqInt (ctr i) (ang i) 1) (sqInt (ctr j) (ang j) 1) := by
  obtain ⟨ctr, ang, hin, hdisj⟩ := h
  have hsq : ∀ c θ, sq c (toIcoMod Real.two_pi_pos 0 θ) 1 = sq c θ 1 := by
    intro c θ; ext p; simp only [sq, Set.mem_ofPred_eq, coord_toIcoMod]
  have hsqI : ∀ c θ, sqInt c (toIcoMod Real.two_pi_pos 0 θ) 1 = sqInt c θ 1 := by
    intro c θ; ext p; simp only [sqInt, Set.mem_ofPred_eq, coord_toIcoMod]
  refine ⟨ctr, fun i => toIcoMod Real.two_pi_pos 0 (ang i), fun i => ?_, fun i => ?_,
    fun i j hij => ?_⟩
  · have := toIcoMod_mem_Ico Real.two_pi_pos 0 (ang i)
    rw [zero_add] at this
    exact Set.Ico_subset_Icc_self this
  · rw [hsq]; exact hin i
  · rw [hsqI, hsqI]; exact hdisj i j hij

/-- **Attainment**: for `n ≥ 1` the infimum `minSide n` is a minimum. -/
theorem isLeast_minSide {n : ℕ} (hn : 1 ≤ n) : IsLeast {s | Packs n s} (minSide n) := by
  refine ⟨?_, fun _ hs => minSide_le hn hs⟩
  obtain ⟨u, hanti, hlim, hmem⟩ :=
    exists_seq_tendsto_sInf (nonempty_packs n) (bddBelow_packs hn)
  choose ctr ang hang hin hdisj using fun m => packs_normalize (hmem m)
  -- the parameters live in a compact set
  set K : Set (Fin n → (ℝ × ℝ) × ℝ) :=
    Set.univ.pi fun _ => box (u 0) ×ˢ Set.Icc 0 (2 * Real.pi) with hK
  have hKc : IsCompact K := by
    refine isCompact_univ_pi fun _ => IsCompact.prod ?_ isCompact_Icc
    have : box (u 0) = Set.Icc 0 (u 0) ×ˢ Set.Icc 0 (u 0) := by
      ext p; simp only [box, Set.mem_prod, Set.mem_Icc, Set.mem_ofPred_eq]; tauto
    rw [this]; exact isCompact_Icc.prod isCompact_Icc
  set x : ℕ → Fin n → (ℝ × ℝ) × ℝ := fun m i => (ctr m i, ang m i) with hx
  have hxK : ∀ m, x m ∈ K := by
    intro m i _
    exact ⟨box_mono (hanti (Nat.zero_le m)) (hin m i (center_mem_sq _ _)), hang m i⟩
  obtain ⟨y, -, φ, hφ, hlimx⟩ := hKc.tendsto_subseq hxK
  have hlimu : Tendsto (u ∘ φ) atTop (𝓝 (minSide n)) := hlim.comp hφ.tendsto_atTop
  have hlimi : ∀ i, Tendsto (fun m => (ctr (φ m) i, ang (φ m) i)) atTop (𝓝 (y i)) :=
    fun i => ((continuous_apply i).tendsto y).comp hlimx
  refine ⟨fun i => (y i).1, fun i => (y i).2, fun i p hp => ?_, fun i j hij => ?_⟩
  · -- containment
    set a := (coord (y i).1 (y i).2 p).1
    set b := (coord (y i).1 (y i).2 p).2
    have hab : |a| ≤ 1/2 ∧ |b| ≤ 1/2 := hp
    have hT : Tendsto (fun m => (sqPt (ctr (φ m) i) (ang (φ m) i) a b, u (φ m))) atTop
        (𝓝 (sqPt (y i).1 (y i).2 a b, minSide n)) :=
      (((continuous_sqPt a b).tendsto (y i)).comp (hlimi i)).prodMk_nhds hlimu
    have := isClosed_box_graph.mem_of_tendsto hT (Eventually.of_forall fun m => by
      refine hin (φ m) i ?_
      simp only [sq, Set.mem_ofPred_eq, coord_sqPt]; exact hab)
    have hpp : sqPt (y i).1 (y i).2 a b = p := sqPt_coord _ _ _
    rwa [hpp] at this
  · -- disjointness of interiors
    rw [Set.disjoint_left]
    intro p hpi hpj
    have hU : IsOpen ({z : ℝ × ℝ | |z.1| < 1/2} ∩ {z | |z.2| < 1/2}) :=
      (isOpen_lt (continuous_abs.comp continuous_fst) continuous_const).inter
        (isOpen_lt (continuous_abs.comp continuous_snd) continuous_const)
    have ev : ∀ k, p ∈ sqInt (y k).1 (y k).2 1 →
        ∀ᶠ m in atTop, p ∈ sqInt (ctr (φ m) k) (ang (φ m) k) 1 := fun k hk =>
      (((continuous_coord_pose p).tendsto (y k)).comp (hlimi k)).eventually (hU.mem_nhds hk)
    obtain ⟨m, hmi, hmj⟩ := ((ev i hpi).and (ev j hpj)).exists
    exact Set.disjoint_left.mp (hdisj (φ m) i j hij) hmi hmj

theorem packs_minSide {n : ℕ} (hn : 1 ≤ n) : Packs n (minSide n) :=
  (isLeast_minSide hn).1

/-- For `n ≥ 1`: `n` unit squares pack in `[0,s]²` iff `s ≥ s(n)`. -/
theorem packs_iff_minSide_le {n : ℕ} (hn : 1 ≤ n) {s : ℝ} : Packs n s ↔ minSide n ≤ s :=
  ⟨minSide_le hn, packs_mono (packs_minSide hn)⟩

theorem minSide_eq_iff_isLeast {n : ℕ} (hn : 1 ≤ n) {k : ℝ} :
    minSide n = k ↔ IsLeast {s | Packs n s} k :=
  ⟨fun h => h ▸ isLeast_minSide hn, IsLeast.csInf_eq⟩

end SquarePacking
