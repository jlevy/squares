import Sqpack.ExactPack

/-!
# Rational shadows: cheap validity checks for packings

A packing given by real data `(x, y, c, s)` per square (`c² + s² = 1`) is usually *far* from touching for most pairs
and most walls.  For those, exact arithmetic (in a number field, or with huge rationals) is wasted: rational
enclosures of the data suffice.

* `Encl`: rational intervals for `x, y, c, s` of one square.  Proved once per square, by whatever means.
* `farOK`: the centres are at least `√2` apart (`gap² ≥ 2` on the enclosures), so the interiors are disjoint
  (`disjoint_of_far`): an interior point is within `√(1/2)` of its centre.
* `sepOK`: interval arithmetic shows that side `k` of square `i` has the corners of `j` on its closed outer side
  (`SepSide`, as in `ExactPack`).
* `inBoxOK`: interval arithmetic shows the four corners lie in `[0, S]` for any `S ≥ Sl`.

`packs_of_shadow`: enclosures + (`inBoxOK` or an exact `InBox`) for every square + (`pairOK` or an exact
`SepPair`) for every pair ⟹ `Packs n S`.  The exact alternatives are hypotheses, so a checker uses the cheap test
first and falls back only at contacts.  Everything here is decidable rational arithmetic (`decide +kernel`).
-/

namespace UnitSquarePacking.Shadow

open Set

/-- The corner coordinates `±1/2`. -/
def halves : List ℚ := [1/2, -1/2]

lemma half_cases {a : ℝ} (h : Half a) : ∃ a' ∈ halves, (a' : ℝ) = a := by
  rcases h with rfl | rfl
  · exact ⟨1/2, by simp [halves], by norm_num⟩
  · exact ⟨-1/2, by simp [halves], by norm_num⟩

/-! ## Rational interval arithmetic -/

/-- A rational interval `[lo, hi]`. -/
abbrev Iv := ℚ × ℚ

def Iv.Mem (I : Iv) (x : ℝ) : Prop := (I.1 : ℝ) ≤ x ∧ x ≤ I.2

def iadd (a b : Iv) : Iv := (a.1 + b.1, a.2 + b.2)
def ineg (a : Iv) : Iv := (-a.2, -a.1)
def isub (a b : Iv) : Iv := iadd a (ineg b)
def imul (a b : Iv) : Iv :=
  (min (min (a.1 * b.1) (a.1 * b.2)) (min (a.2 * b.1) (a.2 * b.2)),
   max (max (a.1 * b.1) (a.1 * b.2)) (max (a.2 * b.1) (a.2 * b.2)))
/-- The point interval. -/
def ipt (q : ℚ) : Iv := (q, q)

lemma mem_iadd {a b : Iv} {x y : ℝ} (ha : a.Mem x) (hb : b.Mem y) : (iadd a b).Mem (x + y) := by
  simp only [Iv.Mem, iadd] at *; push_cast; constructor <;> linarith [ha.1, ha.2, hb.1, hb.2]

lemma mem_ineg {a : Iv} {x : ℝ} (ha : a.Mem x) : (ineg a).Mem (-x) := by
  simp only [Iv.Mem, ineg] at *; push_cast; constructor <;> linarith [ha.1, ha.2]

lemma mem_isub {a b : Iv} {x y : ℝ} (ha : a.Mem x) (hb : b.Mem y) : (isub a b).Mem (x - y) := by
  rw [sub_eq_add_neg]; exact mem_iadd ha (mem_ineg hb)

lemma mem_ipt (q : ℚ) : (ipt q).Mem (q : ℝ) := ⟨le_rfl, le_rfl⟩

/-- `x y` lies between two of the corner products. -/
lemma mul_between {a₁ a₂ b₁ b₂ x y : ℝ} (hx : a₁ ≤ x ∧ x ≤ a₂) (hy : b₁ ≤ y ∧ y ≤ b₂) :
    min (min (a₁ * b₁) (a₁ * b₂)) (min (a₂ * b₁) (a₂ * b₂)) ≤ x * y ∧
      x * y ≤ max (max (a₁ * b₁) (a₁ * b₂)) (max (a₂ * b₁) (a₂ * b₂)) := by
  obtain ⟨hx1, hx2⟩ := hx
  obtain ⟨hy1, hy2⟩ := hy
  -- `x y` is between `a₁ y` and `a₂ y`; each of those is between its two corner products
  have k1 : min (a₁ * b₁) (a₁ * b₂) ≤ a₁ * y ∧ a₁ * y ≤ max (a₁ * b₁) (a₁ * b₂) := by
    rcases le_total 0 a₁ with h | h
    · exact ⟨(min_le_left _ _).trans (mul_le_mul_of_nonneg_left hy1 h),
        (mul_le_mul_of_nonneg_left hy2 h).trans (le_max_right _ _)⟩
    · exact ⟨(min_le_right _ _).trans (mul_le_mul_of_nonpos_left hy2 h),
        (mul_le_mul_of_nonpos_left hy1 h).trans (le_max_left _ _)⟩
  have k2 : min (a₂ * b₁) (a₂ * b₂) ≤ a₂ * y ∧ a₂ * y ≤ max (a₂ * b₁) (a₂ * b₂) := by
    rcases le_total 0 a₂ with h | h
    · exact ⟨(min_le_left _ _).trans (mul_le_mul_of_nonneg_left hy1 h),
        (mul_le_mul_of_nonneg_left hy2 h).trans (le_max_right _ _)⟩
    · exact ⟨(min_le_right _ _).trans (mul_le_mul_of_nonpos_left hy2 h),
        (mul_le_mul_of_nonpos_left hy1 h).trans (le_max_left _ _)⟩
  have k3 : min (a₁ * y) (a₂ * y) ≤ x * y ∧ x * y ≤ max (a₁ * y) (a₂ * y) := by
    rcases le_total 0 y with h | h
    · exact ⟨(min_le_left _ _).trans (mul_le_mul_of_nonneg_right hx1 h),
        (mul_le_mul_of_nonneg_right hx2 h).trans (le_max_right _ _)⟩
    · exact ⟨(min_le_right _ _).trans (mul_le_mul_of_nonpos_right hx2 h),
        (mul_le_mul_of_nonpos_right hx1 h).trans (le_max_left _ _)⟩
  constructor
  · refine le_trans ?_ k3.1
    refine le_min ?_ ?_
    · exact (min_le_left _ _).trans k1.1
    · exact (min_le_right _ _).trans k2.1
  · refine k3.2.trans ?_
    refine max_le ?_ ?_
    · exact k1.2.trans (le_max_left _ _)
    · exact k2.2.trans (le_max_right _ _)

lemma mem_imul {a b : Iv} {x y : ℝ} (ha : a.Mem x) (hb : b.Mem y) : (imul a b).Mem (x * y) := by
  have := mul_between ha hb
  simp only [Iv.Mem, imul]; push_cast; exact this

/-! ## Enclosures of a square -/

structure Encl where
  x : Iv
  y : Iv
  c : Iv
  s : Iv

def Encl.Mem (E : Encl) (x y c s : ℝ) : Prop := E.x.Mem x ∧ E.y.Mem y ∧ E.c.Mem c ∧ E.s.Mem s

/-! ## Far pairs: a disc test -/

/-- A lower bound for `|x - y|` from enclosures. -/
def gap (a b : Iv) : ℚ := max 0 (max (b.1 - a.2) (a.1 - b.2))

lemma gap_sq_le {a b : Iv} {x y : ℝ} (ha : a.Mem x) (hb : b.Mem y) : ((gap a b : ℚ) : ℝ) ^ 2 ≤ (x - y) ^ 2 := by
  have h0 : (0 : ℝ) ≤ gap a b := by exact_mod_cast le_max_left _ _
  have hg : ((gap a b : ℚ) : ℝ) ≤ |x - y| := by
    simp only [gap]; push_cast
    refine max_le (abs_nonneg _) (max_le ?_ ?_)
    · have := neg_abs_le (x - y); linarith [ha.2, hb.1]
    · have := le_abs_self (x - y); linarith [ha.1, hb.2]
  have := pow_le_pow_left₀ h0 hg 2
  rwa [sq_abs] at this

def farOK (Ei Ej : Encl) : Bool := decide (2 ≤ gap Ei.x Ej.x ^ 2 + gap Ei.y Ej.y ^ 2)

/-- An interior point of a unit square is within `√(1/2)` of its centre. -/
lemma dist_sq_lt_of_mem_interior {x y θ : ℝ} {p : ℝ × ℝ} (hp : p ∈ interior (unitSq (x, y) θ)) :
    (p.1 - x) ^ 2 + (p.2 - y) ^ 2 < 1 / 2 := by
  rw [interior_unitSq] at hp
  obtain ⟨h1, h2⟩ := hp
  simp only at h1 h2
  have e : (p.1 - x) ^ 2 + (p.2 - y) ^ 2 =
      ((p.1 - x) * Real.cos θ + (p.2 - y) * Real.sin θ) ^ 2 +
        (-(p.1 - x) * Real.sin θ + (p.2 - y) * Real.cos θ) ^ 2 := by
    have := Real.cos_sq_add_sin_sq θ
    linear_combination (-(p.1 - x) ^ 2 - (p.2 - y) ^ 2) * this
  have a1 : ((p.1 - x) * Real.cos θ + (p.2 - y) * Real.sin θ) ^ 2 < 1 / 4 := by
    have := abs_lt.1 h1; nlinarith
  have a2 : (-(p.1 - x) * Real.sin θ + (p.2 - y) * Real.cos θ) ^ 2 < 1 / 4 := by
    have := abs_lt.1 h2; nlinarith
  linarith

lemma disjoint_of_dist {xi yi θi xj yj θj : ℝ} (h : 2 ≤ (xi - xj) ^ 2 + (yi - yj) ^ 2) :
    Disjoint (interior (unitSq (xi, yi) θi)) (interior (unitSq (xj, yj) θj)) := by
  rw [Set.disjoint_left]
  intro p hpi hpj
  have h1 := dist_sq_lt_of_mem_interior hpi
  have h2 := dist_sq_lt_of_mem_interior hpj
  nlinarith [sq_nonneg (p.1 - xi + (p.1 - xj)), sq_nonneg (p.2 - yi + (p.2 - yj))]

lemma disjoint_of_farOK {Ei Ej : Encl} {xi yi ci si xj yj cj sj θi θj : ℝ} (hi : Ei.Mem xi yi ci si)
    (hj : Ej.Mem xj yj cj sj) (h : farOK Ei Ej = true) :
    Disjoint (interior (unitSq (xi, yi) θi)) (interior (unitSq (xj, yj) θj)) := by
  simp only [farOK, decide_eq_true_eq] at h
  have h' : (2 : ℝ) ≤ ((gap Ei.x Ej.x : ℚ) : ℝ) ^ 2 + ((gap Ei.y Ej.y : ℚ) : ℝ) ^ 2 := by exact_mod_cast h
  have gx := gap_sq_le hi.1 hj.1
  have gy := gap_sq_le hi.2.1 hj.2.1
  exact disjoint_of_dist (by linarith)

/-! ## Near pairs: a separating side by interval arithmetic -/

def nrmI (c s : Iv) : Fin 4 → Iv × Iv
  | 0 => (c, s)
  | 1 => (ineg s, c)
  | 2 => (ineg c, ineg s)
  | 3 => (s, ineg c)

lemma mem_nrmI {c s : Iv} {cr sr : ℝ} (hc : c.Mem cr) (hs : s.Mem sr) (k : Fin 4) :
    (nrmI c s k).1.Mem (nrm cr sr k).1 ∧ (nrmI c s k).2.Mem (nrm cr sr k).2 := by
  fin_cases k
  · exact ⟨hc, hs⟩
  · exact ⟨mem_ineg hs, hc⟩
  · exact ⟨mem_ineg hc, mem_ineg hs⟩
  · exact ⟨hs, mem_ineg hc⟩

/-- Enclosures of the corner `(a, b)` of a square: `x + c a - s b`, `y + s a + c b`. -/
def cornerX (E : Encl) (a b : ℚ) : Iv := iadd (iadd E.x (imul E.c (ipt a))) (ineg (imul E.s (ipt b)))
def cornerY (E : Encl) (a b : ℚ) : Iv := iadd (iadd E.y (imul E.s (ipt a))) (imul E.c (ipt b))

lemma mem_cornerX {E : Encl} {x y c s : ℝ} (h : E.Mem x y c s) (a b : ℚ) :
    (cornerX E a b).Mem (x + c * a - s * b) := by
  rw [sub_eq_add_neg]
  exact mem_iadd (mem_iadd h.1 (mem_imul h.2.2.1 (mem_ipt a))) (mem_ineg (mem_imul h.2.2.2 (mem_ipt b)))

lemma mem_cornerY {E : Encl} {x y c s : ℝ} (h : E.Mem x y c s) (a b : ℚ) :
    (cornerY E a b).Mem (y + s * a + c * b) :=
  mem_iadd (mem_iadd h.2.1 (mem_imul h.2.2.2 (mem_ipt a))) (mem_imul h.2.2.1 (mem_ipt b))

/-- Lower bound for side `k` of `i` at corner `(a, b)` of `j` (`SepSide`'s expression). -/
def sepLo (Ei Ej : Encl) (k : Fin 4) (a b : ℚ) : ℚ :=
  (iadd (imul (nrmI Ei.c Ei.s k).1 (isub (cornerX Ej a b) Ei.x))
        (imul (nrmI Ei.c Ei.s k).2 (isub (cornerY Ej a b) Ei.y))).1

def sepOK (Ei Ej : Encl) (k : Fin 4) : Bool :=
  halves.all fun a => halves.all fun b => decide (1 / 2 ≤ sepLo Ei Ej k a b)

lemma sepSide_of_sepOK {Ei Ej : Encl} {xi yi ci si xj yj cj sj : ℝ} (hi : Ei.Mem xi yi ci si)
    (hj : Ej.Mem xj yj cj sj) {k : Fin 4} (h : sepOK Ei Ej k = true) : SepSide xi yi ci si xj yj cj sj k := by
  intro a b ha hb
  obtain ⟨a', ha'm, rfl⟩ := half_cases ha
  obtain ⟨b', hb'm, rfl⟩ := half_cases hb
  simp only [sepOK, List.all_eq_true, decide_eq_true_eq] at h
  have hl := h a' ha'm b' hb'm
  have hn := mem_nrmI hi.2.2.1 hi.2.2.2 k
  have hm := mem_iadd (mem_imul hn.1 (mem_isub (mem_cornerX hj a' b') hi.1))
    (mem_imul hn.2 (mem_isub (mem_cornerY hj a' b') hi.2.1))
  have := hm.1
  have hl' : ((1 / 2 : ℚ) : ℝ) ≤ (sepLo Ei Ej k a' b' : ℝ) := by exact_mod_cast hl
  simp only [sepLo] at hl'
  push_cast at hl' this
  linarith

/-- The cheap pair test: far apart, or a side of either square separates. -/
def pairOK (Ei Ej : Encl) : Bool :=
  farOK Ei Ej || (List.finRange 4).any (sepOK Ei Ej) || (List.finRange 4).any (sepOK Ej Ei)

/-! ## The container -/

def inBoxOK (E : Encl) (Sl : ℚ) : Bool :=
  halves.all fun a => halves.all fun b =>
    decide (0 ≤ (cornerX E a b).1) && decide ((cornerX E a b).2 ≤ Sl) &&
      decide (0 ≤ (cornerY E a b).1) && decide ((cornerY E a b).2 ≤ Sl)

lemma inBox_of_inBoxOK {E : Encl} {x y c s S : ℝ} {Sl : ℚ} (hE : E.Mem x y c s) (hS : (Sl : ℝ) ≤ S)
    (h : inBoxOK E Sl = true) : InBox S x y c s := by
  intro a b ha hb
  obtain ⟨a', ha'm, rfl⟩ := half_cases ha
  obtain ⟨b', hb'm, rfl⟩ := half_cases hb
  simp only [inBoxOK, List.all_eq_true, Bool.and_eq_true, decide_eq_true_eq] at h
  obtain ⟨⟨⟨h1, h2⟩, h3⟩, h4⟩ := h a' ha'm b' hb'm
  have mx := mem_cornerX hE a' b'
  have my := mem_cornerY hE a' b'
  have h1' : (0 : ℝ) ≤ ((cornerX E a' b').1 : ℝ) := by exact_mod_cast h1
  have h2' : ((cornerX E a' b').2 : ℝ) ≤ Sl := by exact_mod_cast h2
  have h3' : (0 : ℝ) ≤ ((cornerY E a' b').1 : ℝ) := by exact_mod_cast h3
  have h4' : ((cornerY E a' b').2 : ℝ) ≤ Sl := by exact_mod_cast h4
  exact ⟨by linarith [mx.1], by linarith [mx.2], by linarith [my.1], by linarith [my.2]⟩

/-! ## The packing theorem -/

/-- `Packs` from per-square containment and per-pair disjointness (for every choice of angles matching `(c, s)`). -/
theorem packs_of_disjoint {n : ℕ} {S : ℝ} (x y c s : Fin n → ℝ) (hu : ∀ i, c i ^ 2 + s i ^ 2 = 1)
    (hbox : ∀ i, InBox S (x i) (y i) (c i) (s i))
    (hdis : ∀ i j, i < j → ∀ θi θj, Real.cos θi = c i → Real.sin θi = s i → Real.cos θj = c j →
      Real.sin θj = s j → Disjoint (interior (unitSq (x i, y i) θi)) (interior (unitSq (x j, y j) θj))) :
    Packs n S := by
  choose θ hc hs using fun i => exists_angle (hu i)
  refine ⟨fun i => (x i, y i), θ, fun i => unitSq_subset_container (hc i) (hs i) (hbox i), ?_⟩
  intro i j hij
  rcases lt_or_gt_of_ne hij with h | h
  · exact hdis i j h _ _ (hc i) (hs i) (hc j) (hs j)
  · exact (hdis j i h _ _ (hc j) (hs j) (hc i) (hs i)).symm

/-- **Packings from rational shadows.**  Cheap tests where they pass; exact proofs only where they don't. -/
theorem packs_of_shadow {n : ℕ} {S : ℝ} (x y c s : Fin n → ℝ) (hu : ∀ i, c i ^ 2 + s i ^ 2 = 1)
    (E : Fin n → Encl) (hE : ∀ i, (E i).Mem (x i) (y i) (c i) (s i)) (Sl : ℚ) (hS : (Sl : ℝ) ≤ S)
    (hbox : ∀ i, inBoxOK (E i) Sl = true ∨ InBox S (x i) (y i) (c i) (s i))
    (hpair : ∀ i j, i < j → pairOK (E i) (E j) = true ∨ SepPair (x i) (y i) (c i) (s i) (x j) (y j) (c j) (s j)) :
    Packs n S := by
  refine packs_of_disjoint x y c s hu (fun i => ?_) ?_
  · rcases hbox i with h | h
    · exact inBox_of_inBoxOK (hE i) hS h
    · exact h
  · intro i j hij θi θj hci hsi hcj hsj
    rcases hpair i j hij with h | h
    · simp only [pairOK, Bool.or_eq_true, List.any_eq_true, List.mem_finRange, true_and] at h
      rcases h with (h | ⟨k, hk⟩) | ⟨k, hk⟩
      · exact disjoint_of_farOK (hE i) (hE j) h
      · exact disjoint_of_sepSide hci hsi hcj hsj (hu i) (hu j) (sepSide_of_sepOK (hE i) (hE j) hk)
      · exact (disjoint_of_sepSide hcj hsj hci hsi (hu j) (hu i) (sepSide_of_sepOK (hE j) (hE i) hk)).symm
    · rcases h with ⟨k, hk⟩ | ⟨k, hk⟩
      · exact disjoint_of_sepSide hci hsi hcj hsj (hu i) (hu j) hk
      · exact (disjoint_of_sepSide hcj hsj hci hsi (hu j) (hu i) hk).symm

end UnitSquarePacking.Shadow
