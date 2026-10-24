import Sqpack.ExactCheckCut
import Sqpack.ConjecturesProofs

/-!
# Packings in a rectangle from a certificate

A certificate for the `W × H` rectangle (`W ≥ H`) is an ordinary `ExactCheck.Cert` for the square of side `W`
(walls `x ∈ [0, W]`, `y ∈ [0, W]`, all pairs) plus one more wall: every corner has `y ≤ H`.  The extra wall is
checked on the rational enclosures only (`topOK`; no exact fallback), which is enough for squeezed pieces, whose
top margin is positive.

`packsIn_rect_cut`: the checks ⟹ `PacksIn n (rect s H)` with `s` the root of `pS` in `[Sa, Sb]` (for a rational
certificate `s = W`).
-/

namespace UnitSquarePacking.EC

open Set Shadow UnitSquarePacking.Conjectures

variable {n : ℕ} (C : Cert n)

/-- Every corner of square `i` has `y ≤ H` (on the enclosure). -/
def topOK (H : ℚ) (i : Fin n) : Bool :=
  halves.all fun a => halves.all fun b => decide ((cornerY (C.encl i) a b).2 ≤ H)

lemma top_of_topOK {H : ℚ} {i : Fin n} {x y c s : ℝ} (hE : (C.encl i).Mem x y c s) (h : topOK C H i = true) :
    ∀ a b, Half a → Half b → y + s * a + c * b ≤ H := by
  intro a b ha hb
  obtain ⟨a', ha'm, rfl⟩ := half_cases ha
  obtain ⟨b', hb'm, rfl⟩ := half_cases hb
  simp only [topOK, List.all_eq_true, decide_eq_true_eq] at h
  have h4 := h a' ha'm b' hb'm
  have my := mem_cornerY hE a' b'
  have h4' : ((cornerY (C.encl i) a' b').2 : ℝ) ≤ H := by exact_mod_cast h4
  linarith [my.2]

lemma unitSq_subset_rect {W H x y c s θ : ℝ} (hc : Real.cos θ = c) (hs : Real.sin θ = s)
    (h : InBox W x y c s) (ht : ∀ a b, Half a → Half b → y + s * a + c * b ≤ H) :
    unitSq (x, y) θ ⊆ rect W H := by
  intro p hp
  have hW := unitSq_subset_container hc hs h hp
  refine ⟨hW.1, hW.2.1, ?_⟩
  rcases hp with ⟨q, ⟨⟨h1, h2⟩, h3, h4⟩, rfl⟩
  simp only [rot, hc, hs, Prod.snd_add]
  have := affine_nonneg (A := H - y) (B := -s) (C := -c) ⟨h1, h2⟩ ⟨h3, h4⟩
    (fun a b ha hb => by have := ht a b ha hb; linarith)
  linarith

theorem packsIn_rect_of_parts {t : ℝ} (H : ℚ) (hSl : SlOK C = true) (hbox : ∀ i, boxOK C i = true)
    (htop : ∀ i, topOK C H i = true) (hrow : ∀ i, rowOK C i = true)
    (hf : peval C.f t = 0) (ha : (C.a : ℝ) ≤ t) (hb : t ≤ C.b) : PacksIn n (rect (peval C.S t) H) := by
  have hu := fun i => cR_sq_add (sqOK_of_boxOK C (hbox i)) hf
  choose θ hc hs using fun i => exists_angle (hu i)
  refine ⟨fun i => (xR (C.sq i) t, yR (C.sq i) t), θ, fun i => unitSq_subset_rect (hc i) (hs i)
    (inBox_of_boxOK C (hbox i) hSl hf ha hb) (top_of_topOK C (encl_mem C (hbox i) hf ha hb) (htop i)), ?_⟩
  intro i j hij
  rcases lt_or_gt_of_ne hij with h | h
  · exact disjoint_of_pairOK C (hbox i) (hbox j) (pairOK_of_rowOK C (hrow i) h) hf ha hb (hc i) (hs i) (hc j) (hs j)
  · exact (disjoint_of_pairOK C (hbox j) (hbox i) (pairOK_of_rowOK C (hrow j) h) hf ha hb
      (hc j) (hs j) (hc i) (hs i)).symm

/-- **A rectangle packing from a certificate, with sweep-line pruning.** -/
theorem packsIn_rect_cut (pS : Poly) (Sa Sb H : ℚ) (cut : Fin n → ℕ) (hab : C.a ≤ C.b)
    (hsign : qeval C.f C.a * qeval C.f C.b ≤ 0) (hSl : SlOK C = true) (hbox : ∀ i, boxOK C i = true)
    (htop : ∀ i, topOK C H i = true)
    (hs : sortedOK C = true) (hc : ∀ i, cutOK C cut i = true) (hrow : ∀ i, rowOKc C cut i = true)
    (hp : zeroOK C.f (pcomp pS C.S) = true)
    (hlo : nonnegOK C.f C.a C.b (psub C.S [Sa]) = true) (hhi : nonnegOK C.f C.a C.b (psub [Sb] C.S) = true) :
    ∃ s : ℝ, peval pS s = 0 ∧ (Sa : ℝ) ≤ s ∧ s ≤ Sb ∧ PacksIn n (rect s H) := by
  obtain ⟨t, ha, hb, hf⟩ := exists_root hab hsign
  refine ⟨peval C.S t, ?_, ?_, ?_,
    packsIn_rect_of_parts C H hSl hbox htop (fun i => rowOK_of_rowOKc C hs (hc i) (hrow i)) hf ha hb⟩
  · have := zero_of_zeroOK hp hf; rwa [peval_pcomp] at this
  · have := nonneg_of_nonnegOK hlo hf ha hb; simp at this; linarith
  · have := nonneg_of_nonnegOK hhi hf ha hb; simp at this; linarith

end UnitSquarePacking.EC
