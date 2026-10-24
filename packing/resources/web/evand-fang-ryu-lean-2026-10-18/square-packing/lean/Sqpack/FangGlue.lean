import Sqpack.ConjecturesProofs

/-!
# Fang's gluing lemma (Lemma 3 of K. Fang's note, after Arslanov–Mustafin–Shangitbayev)

Let `A` be a packing of `nA` unit squares in the `a × b` box shrunk by `d` (so in `[0, a - d] × [0, b - d]`),
and `B` a packing of `nB` unit squares in the `a' × b'` box shrunk by `d`.  Put `n = b + b'`.  Then the square
`[0, n - d]²` holds

* `A` in `[0, a - d] × [b', n - d]` (top left),
* an aligned block of `(n - a) × b` unit squares in `[a - d, n - d] × [b' - d, n - d]` (top right),
* an aligned block of `(n - a') × b'` unit squares in `[0, n - a'] × [0, b']` (bottom left),
* `B` in `[n - a', n - d] × [0, b' - d]` (bottom right),

so `nA + nB + (n - a) b + (n - a') b'` squares, which is `n² - wA - wB` with `wA = ab - nA`, `wB = a'b' - nB`.
Every horizontal line meets `A` or `B`, and every vertical one meets `A` or `B` too, which is what lets each aligned
block slide by `d`.  The hypotheses are only that the four boxes fit: `a ≤ n`, `a' ≤ n`, `n - a' + d ≤ a`
(bottom-left block left of the top-right one), `d ≤ b'`, `d ≤ b` and `0 ≤ d`.

`glue` is stated for real `d ≥ 0`; with `d > 0` it gives side `n - d < n`.
-/

namespace UnitSquarePacking.FangGlue

open Set UnitSquarePacking.Conjectures

/-- The box `[x₀, x₁] × [y₀, y₁]`. -/
def box (x₀ x₁ y₀ y₁ : ℝ) : Set (ℝ × ℝ) := Icc x₀ x₁ ×ˢ Icc y₀ y₁

lemma isClosed_box (x₀ x₁ y₀ y₁ : ℝ) : IsClosed (box x₀ x₁ y₀ y₁) :=
  isClosed_Icc.prod isClosed_Icc

lemma interior_box (x₀ x₁ y₀ y₁ : ℝ) : interior (box x₀ x₁ y₀ y₁) = Ioo x₀ x₁ ×ˢ Ioo y₀ y₁ :=
  interior_rect_shift _ _ _ _

/-- A packing of `[0, w] × [0, h]`, moved to `[x₀, x₀ + w] × [y₀, y₀ + h]`. -/
lemma _root_.UnitSquarePacking.Conjectures.PacksIn.toBox {n : ℕ} {w h : ℝ} (hp : PacksIn n (rect w h)) (x₀ y₀ : ℝ) :
    PacksIn n (box x₀ (x₀ + w) y₀ (y₀ + h)) :=
  (hp.shift (x₀, y₀)).mono fun p hp => by
    simp only [rect, box, mem_ofPred_eq, mem_prod, mem_Icc, Prod.fst_sub, Prod.snd_sub] at hp ⊢
    exact ⟨⟨by linarith, by linarith⟩, by linarith, by linarith⟩

/-- An aligned `p × q` block of unit squares fills `[0, p] × [0, q]`. -/
lemma packsIn_block (p q : ℕ) : PacksIn (p * q) (rect p q) := by
  have h := (packsIn_unit.row zero_le_one p).col (by positivity) q
  simp only [mul_one] at h
  rwa [mul_comm p q]

/-- An open set meeting neither interior of two regions, the second closed, misses the interior of their union. -/
lemma disjoint_interior_union {U R₁ R₂ : Set (ℝ × ℝ)} (hU : IsOpen U) (h₂ : IsClosed R₂)
    (d₁ : Disjoint U (interior R₁)) (d₂ : Disjoint U (interior R₂)) :
    Disjoint U (interior (R₁ ∪ R₂)) := by
  rw [Set.disjoint_left]
  intro p hpU hpI
  set V := U ∩ interior (R₁ ∪ R₂)
  have hV : IsOpen V := hU.inter isOpen_interior
  by_cases hsub : V ⊆ R₂
  · have : V ⊆ interior R₂ := interior_maximal hsub hV
    exact Set.disjoint_left.1 d₂ hpU (this ⟨hpU, hpI⟩)
  · obtain ⟨q, hqV, hq2⟩ := Set.not_subset.1 hsub
    have hW : IsOpen (V ∩ R₂ᶜ) := hV.inter h₂.isOpen_compl
    have hW1 : V ∩ R₂ᶜ ⊆ R₁ := fun r ⟨⟨_, hr⟩, hr2⟩ =>
      ((interior_subset hr : r ∈ R₁ ∪ R₂)).resolve_right hr2
    have := interior_maximal hW1 hW
    exact Set.disjoint_left.1 d₁ hqV.1 (this ⟨hqV, hq2⟩)

lemma disjoint_box_x {x₀ x₁ y₀ y₁ x₀' x₁' y₀' y₁' : ℝ} (h : x₁ ≤ x₀') :
    Disjoint (interior (box x₀ x₁ y₀ y₁)) (interior (box x₀' x₁' y₀' y₁')) := by
  rw [interior_box, interior_box, Set.disjoint_left]
  rintro p ⟨⟨_, hp⟩, _⟩ ⟨⟨hp', _⟩, _⟩
  linarith

lemma disjoint_box_y {x₀ x₁ y₀ y₁ x₀' x₁' y₀' y₁' : ℝ} (h : y₁ ≤ y₀') :
    Disjoint (interior (box x₀ x₁ y₀ y₁)) (interior (box x₀' x₁' y₀' y₁')) := by
  rw [interior_box, interior_box, Set.disjoint_left]
  rintro p ⟨_, ⟨_, hp⟩⟩ ⟨_, ⟨hp', _⟩⟩
  linarith

/-- **Fang's gluing lemma** (Lemma 3 of the note; Arslanov–Mustafin–Shangitbayev's decomposition). -/
theorem glue {nA nB a b a' b' : ℕ} {d : ℝ} (hd : 0 ≤ d)
    (hA : PacksIn nA (rect (a - d) (b - d))) (hB : PacksIn nB (rect (a' - d) (b' - d)))
    (ha : a ≤ b + b') (ha' : a' ≤ b + b') (hc : ((b + b' - a' : ℕ) : ℝ) + d ≤ a)
    (hdb : d ≤ b) (hdb' : d ≤ b') :
    Packs (nA + nB + (b + b' - a) * b + (b + b' - a') * b') ((b + b' : ℕ) - d) := by
  set n := b + b' with hn
  have cA : ((n - a : ℕ) : ℝ) = n - a := by rw [Nat.cast_sub ha]
  have cA' : ((n - a' : ℕ) : ℝ) = n - a' := by rw [Nat.cast_sub ha']
  have nc : (n : ℝ) = b + b' := by rw [hn]; push_cast; ring
  -- the four pieces, in place
  have PA := hA.toBox 0 b'
  have PB := hB.toBox ((n - a' : ℕ) : ℝ) 0
  have PD := (packsIn_block (n - a) b).toBox (a - d) (b' - d)
  have PC := (packsIn_block (n - a') b').toBox 0 0
  rw [cA'] at PB PC
  rw [cA] at PD
  -- the boxes as named sets
  set XA := box 0 (0 + (a - d)) b' (b' + (b - d))
  set XB := box ((n : ℝ) - a') ((n : ℝ) - a' + (a' - d)) 0 (0 + (b' - d))
  set XD := box ((a : ℝ) - d) ((a : ℝ) - d + ((n : ℝ) - a)) ((b' : ℝ) - d) ((b' : ℝ) - d + b)
  set XC := box 0 (0 + ((n : ℝ) - a')) 0 (0 + (b' : ℝ))
  have hc' : (n : ℝ) - a' + d ≤ a := by rwa [cA'] at hc
  -- top = A ∪ D, bottom = C ∪ B
  have top := PA.union PD (disjoint_box_x (by linarith))
  have bot := PC.union PB (disjoint_box_x (by linarith))
  have dTB : Disjoint (interior (XA ∪ XD)) (interior (XC ∪ XB)) := by
    refine disjoint_interior_union isOpen_interior (isClosed_box _ _ _ _) ?_ ?_
    · refine (disjoint_interior_union isOpen_interior (isClosed_box _ _ _ _) ?_ ?_).symm
      · exact disjoint_box_y (by linarith)
      · exact disjoint_box_x (by linarith)
    · refine (disjoint_interior_union isOpen_interior (isClosed_box _ _ _ _) ?_ ?_).symm
      · exact disjoint_box_y (by linarith)
      · exact disjoint_box_y (by linarith)
  have all := top.union bot dTB
  rw [show nA + nB + (n - a) * b + (n - a') * b' = nA + (n - a) * b + ((n - a') * b' + nB) by ring]
  refine (packs_iff_packsIn.2 (all.mono ?_))
  · intro p hp
    simp only [XA, XB, XC, XD, box, rect, mem_union, mem_prod, mem_Icc] at hp ⊢
    have ha0 : (a : ℝ) ≤ n := by exact_mod_cast ha
    have ha0' : (a' : ℝ) ≤ n := by exact_mod_cast ha'
    have hb0 : (0 : ℝ) ≤ b := by positivity
    rw [nc] at hp ha0 ha0' hc' ⊢
    rcases hp with ((⟨⟨h1, h2⟩, h3, h4⟩ | ⟨⟨h1, h2⟩, h3, h4⟩) | (⟨⟨h1, h2⟩, h3, h4⟩ | ⟨⟨h1, h2⟩, h3, h4⟩)) <;>
      refine ⟨⟨?_, ?_⟩, ?_, ?_⟩ <;> linarith

end UnitSquarePacking.FangGlue
