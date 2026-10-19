import Sq19Lean.Capture.Assembly
import Sq19Lean.Assembly.CensusBridge

/-! From the census to a capture region.

`Sq19.Cover.packing_reaches_census` places a packing in `[0, L]^2` concentrically (shift `t = (U - L)/2`,
`U = 2443/500`), moves it by a symmetry `g`, and assigns its squares to distinct cells `c`, the cells of
census mask `censusMasks.get k`. `census_to_capture`: if a symmetry `h` maps those cells onto the roster `r`
of a capture region, then `h` applied to the census packing, relabelled into the region's owner order and
translated by `-(σ, σ)`, satisfies every hypothesis of the region's capture statement, so it has poses with the
region's conclusion. The translated family lies in `[t - σ, t - σ + L]^2`: the offset `t - σ` from the
packing's own box is at most `(side - L)/2` plus the trace slack (it is 0 at `L = U - 2σ`).

The per-state facts (the mask, the symmetry, the shifted cells) are finite checks below. -/
namespace Sq19.Capture
open Sq17.Propagation Sq17.Propagation.HalfPlaneState

/-- The box `[a, a + L]^2`. -/
def boxA (a L : ℝ) : Set (ℝ × ℝ) := {z | a ≤ z.1 ∧ z.1 ≤ a + L ∧ a ≤ z.2 ∧ z.2 ≤ a + L}

theorem census_to_capture (r : Fin 19 → Fin 25) (hr : Function.Injective r) (σ side shift : ℚ)
    (cells : List (List (ℚ × ℚ)))
    (hcells : ∀ j : Fin 19, cells.getD j [] = (Sq19.Census.vertices (r j)).map (shiftVertex σ))
    (hlo : (2443/500 : ℝ) - 2 * σ ≤ side + 2 * shift) (hhi : (side : ℝ) ≤ 2443/500 - 2 * σ + 2 * shift)
    (holds : (ℕ → AnglePose) → Prop)
    (capture : ∀ c u : ℕ → ℝ × ℝ,
      (∀ i, i < 19 → (u i).1^2+(u i).2^2 = 1) →
      (∀ i, i < 19 → c i ∈ convexHull ℝ (realPoint '' {v | v ∈ cells.getD i []})) →
      (∀ i j, i < 19 → j < 19 → i ≠ j → Disjoint
        (interior (Sq17.sq (c i).1 (c i).2 (u i).1 (u i).2))
        (interior (Sq17.sq (c j).1 (c j).2 (u j).1 (u j).2))) →
      (∀ i, i < 19 → Sq17.sq (c i).1 (c i).2 (u i).1 (u i).2 ⊆ traceContainer side shift) →
      ∃ p, Describes c u p ∧ holds p)
    (L : ℝ) (hL : L ≤ side) (h : Fin 8) (q u : Fin 19 → ℝ × ℝ) (c : Fin 19 → Fin 25)
    (hu : ∀ i, (u i).1^2+(u i).2^2 = 1)
    (hf : ∀ i, Sq17.sq (q i).1 (q i).2 (u i).1 (u i).2 ⊆ Sq19.Cover.frameBox L)
    (hd : ∀ i j, i ≠ j → Disjoint
      (interior (Sq17.sq (q i).1 (q i).2 (u i).1 (u i).2))
      (interior (Sq17.sq (q j).1 (q j).2 (u j).1 (u j).2)))
    (hcell : ∀ i, q i ∈ Sq19.Cover.cell (c i))
    (himg : ∀ j, ∃ i, Sq19.Cover.perm h (c i) = r j) :
    ∃ π : Fin 19 → Fin 19, Function.Injective π ∧ ∃ p : ℕ → AnglePose,
      (∀ j : Fin 19, (p j.val).center = Sq19.Cover.actG h (q (π j)) + (-(σ:ℝ), -(σ:ℝ)) ∧
        (p j.val).square = Sq17.sq (Sq19.Cover.actG h (q (π j)) + (-(σ:ℝ), -(σ:ℝ))).1
          (Sq19.Cover.actG h (q (π j)) + (-(σ:ℝ), -(σ:ℝ))).2
          (Sq19.Cover.dirG h (u (π j))).1 (Sq19.Cover.dirG h (u (π j))).2) ∧ holds p ∧
      (∀ j : Fin 19, (p j.val).square ⊆ boxA ((2443/500 - L)/2 - σ) L) ∧
      (∀ i j : Fin 19, i ≠ j → Disjoint (interior (p i.val).square) (interior (p j.val).square)) := by
  choose π hπ using himg
  have hπi : Function.Injective π := fun a b hab => hr (by rw [← hπ a, ← hπ b, hab])
  let s : ℝ × ℝ := (-(σ:ℝ), -(σ:ℝ))
  let C : ℕ → ℝ × ℝ := fun j => if hj : j < 19 then Sq19.Cover.actG h (q (π ⟨j, hj⟩)) + s else 0
  let V : ℕ → ℝ × ℝ := fun j => if hj : j < 19 then Sq19.Cover.dirG h (u (π ⟨j, hj⟩)) else (1, 0)
  have hC : ∀ j : Fin 19, C j.val = Sq19.Cover.actG h (q (π j)) + s := fun j => by simp [C, j.isLt]
  have hV : ∀ j : Fin 19, V j.val = Sq19.Cover.dirG h (u (π j)) := fun j => by simp [V, j.isLt]
  have hsq : ∀ j : Fin 19, Sq17.sq (C j.val).1 (C j.val).2 (V j.val).1 (V j.val).2 =
      (fun z => z + s) '' Sq17.sq (Sq19.Cover.actG h (q (π j))).1 (Sq19.Cover.actG h (q (π j))).2
        (Sq19.Cover.dirG h (u (π j))).1 (Sq19.Cover.dirG h (u (π j))).2 := by
    intro j; rw [hC j, hV j]; exact sq_translate _ _ _ _ _ _
  obtain ⟨p, hp, hh⟩ := capture C V
    (fun i hi => by rw [hV ⟨i, hi⟩]; exact Sq19.Cover.dir_unit _ _ _ _ (hu _))
    (fun i hi => by
      rw [hC ⟨i, hi⟩, hcells ⟨i, hi⟩]
      apply hull_shift
      have hm := Sq19.Cover.actG_mem_cell h _ (hcell (π ⟨i, hi⟩))
      rw [hπ, Sq19.Assembly.cell_eq] at hm
      have e : Sq19.Cover.actG h (q (π ⟨i, hi⟩)) + s + ((σ:ℝ), (σ:ℝ)) = Sq19.Cover.actG h (q (π ⟨i, hi⟩)) := by
        ext <;> simp [s]
      rw [e]; exact hm)
    (fun i j hi hj hij => by
      rw [hsq ⟨i, hi⟩, hsq ⟨j, hj⟩]
      apply translate_disjoint
      exact Sq19.Cover.act_disjoint _ _ _ _ _ _ _ (hu _) (hu _)
        (hd _ _ (fun he => hij (by simpa using congrArg Fin.val (hπi he)))))
    (fun i hi => by
      rw [hsq ⟨i, hi⟩]
      have hfr := Sq19.Cover.act_square_subset (Sq19.Cover.gb h).1 (Sq19.Cover.gb h).2.1 (Sq19.Cover.gb h).2.2
        (Sq19.Cover.frameBox L) (fun z hz => Sq19.Cover.act_frameBox _ _ _ L z hz) _ _ (hf (π ⟨i, hi⟩))
      intro w hw
      obtain ⟨z, hz, rfl⟩ := hw
      obtain ⟨h1, h2, h3, h4⟩ := hfr hz
      unfold Sq19.Cover.shift at h1 h2 h3 h4
      refine ⟨?_, ?_, ?_, ?_⟩ <;> simp only [s, Prod.fst_add, Prod.snd_add] <;> linarith)
  have hbox : ∀ j : Fin 19, Sq17.sq (C j.val).1 (C j.val).2 (V j.val).1 (V j.val).2 ⊆ boxA ((2443/500 - L)/2 - σ) L := by
    intro j
    rw [hsq j]
    have hfr := Sq19.Cover.act_square_subset (Sq19.Cover.gb h).1 (Sq19.Cover.gb h).2.1 (Sq19.Cover.gb h).2.2
      (Sq19.Cover.frameBox L) (fun z hz => Sq19.Cover.act_frameBox _ _ _ L z hz) _ _ (hf (π j))
    intro w hw
    obtain ⟨z, hz, rfl⟩ := hw
    obtain ⟨h1, h2, h3, h4⟩ := hfr hz
    unfold Sq19.Cover.shift at h1 h2 h3 h4
    refine ⟨?_, ?_, ?_, ?_⟩ <;> simp only [s, Prod.fst_add, Prod.snd_add] <;> linarith
  refine ⟨π, hπi, p, fun j => ?_, hh, fun j => ?_, fun i j hij => ?_⟩
  · obtain ⟨h1, h2⟩ := hp j.val j.isLt
    rw [hC j] at h1; rw [h2, hC j, hV j]
    exact ⟨h1, rfl⟩
  · rw [(hp j.val j.isLt).2]; exact hbox j
  · rw [(hp i.val i.isLt).2, (hp j.val j.isLt).2, hsq i, hsq j]
    apply translate_disjoint
    exact Sq19.Cover.act_disjoint _ _ _ _ _ _ _ (hu _) (hu _) (hd _ _ (fun he => hij (hπi he)))

end Sq19.Capture

#print axioms Sq19.Capture.census_to_capture
