import Sqpack.V7.Data
import Sqpack.Bentz

/-!
# The box file `L4_k02_box7.txt` as a mixed cover of the pose tree

`Bentz.box7Cover` (the file verbatim: 800 segments indexed by line number, the polygon
`[9/5, 26/5]²`) and `mcoverP 5 10¹² ∅ segsT trects` (the segments normalised and sorted, the
Lebesgue square as a rectangle entry) are the same measure (`box7Cover_eq_mcoverP`).
-/

open MeasureTheory Finset

namespace SquarePacking

namespace LemmaELeaf

open ZMTreeM

set_option maxRecDepth 100000 in
lemma boxSegs_norm_nodup : (Bentz.boxSegs.map segNorm).Nodup := by decide +kernel

set_option maxRecDepth 100000 in
lemma boxSegs_norm_sub : (Bentz.boxSegs.map segNorm).all (fun e => tsegs.contains e) = true := by
  decide +kernel

set_option maxRecDepth 100000 in
lemma tsegs_sub : tsegs.all (fun e => (Bentz.boxSegs.map segNorm).contains e) = true := by
  decide +kernel

lemma segMeasure_segNorm (e : SegE) :
    segMeasure (((e.1 : ℕ) : ℝ) / 5, ((e.2.1 : ℕ) : ℝ) / 5) (((e.2.2.1 : ℕ) : ℝ) / 5, ((e.2.2.2.1 : ℕ) : ℝ) / 5)
      = segMeasure (segA 5 (segNorm e)) (segB 5 (segNorm e)) := by
  unfold segNorm
  split_ifs
  · rfl
  · rw [segMeasure_comm]; rfl

/-- **The box file is the cover of the pose tree.** -/
theorem box7Cover_eq_mcoverP :
    Bentz.box7Cover.measure = (mcoverP 5 1000000000000 PTree.leaf segsT trects).measure := by
  unfold MixedCover.measure
  refine congrArg₂ (· + ·) (congrArg₂ (· + ·) ?_ ?_) ?_
  · rw [show Bentz.box7Cover.pts = ∅ from rfl,
      show (mcoverP 5 1000000000000 PTree.leaf segsT trects).pts = ∅ from rfl, sum_empty, sum_empty]
  · -- the segments: `j ↦ segNorm (boxSegs j)` is a bijection onto `tsegs`
    set F : SegE → Measure (ℝ × ℝ) := fun e =>
      ENNReal.ofReal ((e.2.2.2.2 : ℝ) / (1000000000000 : ℕ)) • segMeasure (segA 5 e) (segB 5 e) with hF
    set φ : Fin Bentz.boxSegs.length → SegE := fun j => segNorm (Bentz.boxSegs.get j) with hφ
    have hterm : ∀ j ∈ (univ : Finset (Fin Bentz.boxSegs.length)),
        ENNReal.ofReal (Bentz.box7Cover.sw j) • segMeasure (Bentz.box7Cover.sa j) (Bentz.box7Cover.sb j)
          = F (φ j) := by
      intro j _
      have hw : (segNorm (Bentz.boxSegs.get j)).2.2.2.2 = (Bentz.boxSegs.get j).2.2.2.2 := by
        unfold segNorm; split_ifs <;> rfl
      simp only [Bentz.box7Cover, hF, hφ, hw]
      rw [← segMeasure_segNorm]
      norm_num
    have hinj : ∀ j₁ ∈ (univ : Finset (Fin Bentz.boxSegs.length)), ∀ j₂ ∈ univ, φ j₁ = φ j₂ → j₁ = j₂ := by
      intro j₁ _ j₂ _ h
      have h' : (Bentz.boxSegs.map segNorm)[j₁.1]'(by simp) = (Bentz.boxSegs.map segNorm)[j₂.1]'(by simp) := by
        simpa [hφ] using h
      exact Fin.ext ((List.Nodup.getElem_inj_iff boxSegs_norm_nodup).mp h')
    have himg : univ.image φ = segsT.toList.toFinset := by
      rw [segsT_toList]
      ext e
      simp only [mem_image, mem_univ, true_and, List.mem_toFinset]
      constructor
      · rintro ⟨j, rfl⟩
        have := List.all_eq_true.mp boxSegs_norm_sub (segNorm (Bentz.boxSegs.get j))
          (List.mem_map.mpr ⟨_, List.get_mem _ _, rfl⟩)
        exact List.contains_iff_mem.mp this
      · intro he
        have h1 := List.all_eq_true.mp tsegs_sub e he
        obtain ⟨x, hx, rfl⟩ := List.mem_map.mp (List.contains_iff_mem.mp h1)
        obtain ⟨j, rfl⟩ := List.mem_iff_get.mp hx
        exact ⟨j, rfl⟩
    rw [show Bentz.box7Cover.segs = univ from rfl, Finset.sum_congr rfl hterm,
      ← Finset.sum_image hinj, himg]
    rfl
  · -- the polygon: `[9/5, 26/5]²` with density one
    have hp : Bentz.convPoly 5 Bentz.boxPolyVerts = rectSet 5 (9, 9, 26, 26, 1000000000000) := by
      rw [Bentz.convPoly_box]
      ext p
      simp only [Bentz.lebSq, rectSet, Set.mem_prod, Set.mem_Icc]
      norm_num
    have hv : (volume (rectSet 5 (9, 9, 26, 26, 1000000000000))).toReal = 289 / 25 := by
      rw [volume_rectSet_toReal 5 (by norm_num) _ (by norm_num) (by norm_num)]
      norm_num
    rw [show (mcoverP 5 1000000000000 PTree.leaf segsT trects).polys = {(9, 9, 26, 26, 1000000000000)}
      from rfl, sum_singleton, show Bentz.box7Cover.polys = univ from rfl, Fintype.sum_unique]
    simp only [Bentz.box7Cover, mcoverP, hp, hv, Bentz.boxPolyW]
    norm_num

end LemmaELeaf

end SquarePacking
