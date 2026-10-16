import Sq19Lean.Cover.Reduction
import Sq19Lean.Cover.OrbitData
import Std.Data.HashSet.Lemmas

/-!
# The D4 orbit step

The eight symmetries of the cover frame `[0, U]^2`, `U = 2443/500`, in the order of
`make_cover.py` (`d4`), `orbits.c` and `census.c`:
`(x,y)`, `(U-x,y)`, `(x,U-y)`, `(U-x,U-y)`, `(y,x)`, `(U-y,x)`, `(y,U-x)`, `(U-y,U-x)`.
`perm g` is the induced permutation of the 25 cells; the vertex check proves that `g` maps each
whole closed cell `i` into cell `perm g i`.

Every 19-cell set is mapped by some `g` onto the occupied set of one census mask
(`orbit_check`, a single finite check over all 177,100 sets by `native_decide`, about 45 s).
The final theorem `packing_reaches_census` combines this with the reduction.
-/
namespace Sq19.Cover
open Sq17.WallCapacity Sq17.Propagation

/-! ## The symmetries -/

/-- The eight symmetries as (swap, reflect x, reflect y) for `act`, in census order. -/
def gb : Fin 8 → Bool × Bool × Bool := ![
  (false,false,false), (false,true,false), (false,false,true), (false,true,true),
  (true,false,false), (true,true,false), (true,false,true), (true,true,true)]

noncomputable def actG (g : Fin 8) (z : ℝ × ℝ) : ℝ × ℝ := act (gb g).1 (gb g).2.1 (gb g).2.2 z

noncomputable def dirG (g : Fin 8) (z : ℝ × ℝ) : ℝ × ℝ := dir (gb g).1 (gb g).2.1 (gb g).2.2 z

/-- The same maps on exact rational points. -/
def actQ (sw fx fy : Bool) (z : ℚ × ℚ) : ℚ × ℚ :=
  let w : ℚ × ℚ := if sw then (z.2, z.1) else z
  (if fx then 2443/500 - w.1 else w.1, if fy then 2443/500 - w.2 else w.2)

theorem actQ_cast (sw fx fy : Bool) (v : ℚ × ℚ) :
    realPoint (actQ sw fx fy v) = act sw fx fy (realPoint v) := by
  cases sw <;> cases fx <;> cases fy <;> simp [actQ, act, realPoint]

theorem act_affine (sw fx fy : Bool) (x y : ℝ × ℝ) (a b : ℝ) (hab : a+b=1) :
    act sw fx fy (a • x + b • y) = a • act sw fx fy x + b • act sw fx fy y := by
  have hb : b = 1-a := by linarith
  subst hb
  cases sw <;> cases fx <;> cases fy <;> ext <;> simp [act] <;> ring

/-- Every vertex of cell `i` maps to a vertex of cell `perm g i`. -/
theorem vertex_action_checked : ∀ g : Fin 8, ∀ i : Fin 25,
    (vertices i).all (fun v => decide (actQ (gb g).1 (gb g).2.1 (gb g).2.2 v ∈
      vertices (perm g i))) = true := by
  decide +kernel

/-- The whole closed cell `i` maps into cell `perm g i`. -/
theorem actG_mem_cell (g : Fin 8) (i : Fin 25) {p : ℝ × ℝ} (hp : p ∈ cell i) :
    actG g p ∈ cell (perm g i) := by
  let T := cell (perm g i)
  have ht : Convex ℝ T := convex_convexHull ℝ _
  have hpre : Convex ℝ {x | actG g x ∈ T} := by
    intro x hx y hy a b ha hb hab
    change act _ _ _ (a • x+b • y) ∈ T
    rw [act_affine _ _ _ x y a b hab]
    exact ht hx hy ha hb hab
  apply convexHull_min (t := {x | actG g x ∈ T}) ?_ hpre hp
  rintro _ ⟨q,hq,rfl⟩
  change act _ _ _ (realPoint q) ∈ T
  rw [← actQ_cast]
  apply subset_convexHull ℝ _
  refine ⟨_, ?_, rfl⟩
  exact of_decide_eq_true ((List.all_eq_true.mp (vertex_action_checked g i)) q hq)

theorem perm_injective_checked : ∀ g : Fin 8, ∀ i j : Fin 25, perm g i = perm g j → i = j := by
  decide +kernel

/-- `perm g` as an embedding. -/
def permEmb (g : Fin 8) : Fin 25 ↪ Fin 25 := ⟨perm g, fun i j h => perm_injective_checked g i j h⟩

/-! ## Squares under the symmetries -/

private theorem abs_pair_iff (A B A' B' : ℝ) (hA : A' = A ∨ A' = -A) (hB : B' = B ∨ B' = -B) :
    (|A'| ≤ 1/2 ∧ |B'| ≤ 1/2) ↔ (|A| ≤ 1/2 ∧ |B| ≤ 1/2) := by
  rcases hA with h | h <;> rcases hB with h' | h' <;> simp [h, h', abs_neg]

theorem act_mem_sq (sw fx fy : Bool) (p u w : ℝ × ℝ) :
    act sw fx fy w ∈ Sq17.sq (act sw fx fy p).1 (act sw fx fy p).2
      (dir sw fx fy u).1 (dir sw fx fy u).2 ↔ w ∈ Sq17.sq p.1 p.2 u.1 u.2 := by
  unfold Sq17.sq
  simp only [Set.mem_ofPred_eq]
  apply abs_pair_iff <;>
  cases sw <;> cases fx <;> cases fy <;> simp only [act, dir] <;> simp <;>
    first | (left; ring1) | (right; ring1)

theorem act_surjective (sw fx fy : Bool) (z : ℝ × ℝ) : ∃ w, act sw fx fy w = z := by
  cases sw <;> cases fx <;> cases fy
  · exact ⟨z, by simp [act]⟩
  · exact ⟨(z.1, 2443/500 - z.2), by ext <;> simp [act]⟩
  · exact ⟨(2443/500 - z.1, z.2), by ext <;> simp [act]⟩
  · exact ⟨(2443/500 - z.1, 2443/500 - z.2), by ext <;> simp [act]⟩
  · exact ⟨(z.2, z.1), by ext <;> simp [act]⟩
  · exact ⟨(2443/500 - z.2, z.1), by ext <;> simp [act]⟩
  · exact ⟨(z.2, 2443/500 - z.1), by ext <;> simp [act]⟩
  · exact ⟨(2443/500 - z.2, 2443/500 - z.1), by ext <;> simp [act]⟩

/-- A set mapped into itself by a symmetry keeps containing the transformed squares. -/
theorem act_square_subset (sw fx fy : Bool) (S : Set (ℝ × ℝ))
    (hS : ∀ z ∈ S, act sw fx fy z ∈ S) (p u : ℝ × ℝ)
    (h : Sq17.sq p.1 p.2 u.1 u.2 ⊆ S) :
    Sq17.sq (act sw fx fy p).1 (act sw fx fy p).2 (dir sw fx fy u).1 (dir sw fx fy u).2 ⊆ S := by
  intro z hz
  obtain ⟨w, rfl⟩ := act_surjective sw fx fy z
  exact hS w (h ((act_mem_sq sw fx fy p u w).mp hz))

/-- The concentric frame of a container of side `L`: `[σ, σ + L]^2`, `σ = (U - L)/2`. -/
def frameBox (L : ℝ) : Set (ℝ × ℝ) :=
  {z | shift L ≤ z.1 ∧ z.1 ≤ shift L + L ∧ shift L ≤ z.2 ∧ z.2 ≤ shift L + L}

theorem act_frameBox (sw fx fy : Bool) (L : ℝ) (z : ℝ × ℝ) (hz : z ∈ frameBox L) :
    act sw fx fy z ∈ frameBox L := by
  obtain ⟨h1,h2,h3,h4⟩ := hz
  unfold shift at h1 h2 h3 h4
  cases sw <;> cases fx <;> cases fy <;> simp only [frameBox, shift, act, Set.mem_ofPred_eq] <;>
    simp <;> refine ⟨?_,?_,?_,?_⟩ <;> linarith

theorem frameBox_subset (L : ℝ) (hL : L ≤ 2443/500) : frameBox L ⊆ containerBox (2443/500) := by
  rintro z ⟨h1,h2,h3,h4⟩
  unfold shift at h1 h2 h3 h4
  exact ⟨by linarith, by linarith, by linarith, by linarith⟩

theorem shifted_fit_frame (L : ℝ) (p u : ℝ × ℝ)
    (hfit : Sq17.sq p.1 p.2 u.1 u.2 ⊆ containerBox L) :
    Sq17.sq (shifted L p).1 (shifted L p).2 u.1 u.2 ⊆ frameBox L := by
  intro z hz
  have h := hfit (shifted_square L p u z hz)
  simp only [containerBox, Set.mem_ofPred_eq] at h
  exact ⟨by linarith [h.1], by linarith [h.2.1], by linarith [h.2.2.1], by linarith [h.2.2.2]⟩

/-! ## The finite orbit check -/

/-- The cells of a mask. -/
def ofMask (m : ℕ) : Finset (Fin 25) := Finset.univ.filter (fun i => m.testBit i.val)

/-- The mask of a cell set. -/
def toMask (t : Finset (Fin 25)) : ℕ := ∑ i ∈ t, 2^i.val

/-- Lookup in the plain table `permRows` (`![...]` lookups are slow in compiled code);
`perm_eq_fast` proves it equal to `perm`. -/
def permFast (g : Fin 8) (i : Fin 25) : Fin 25 :=
  ⟨((permRows.getD g.val []).getD i.val 0) % 25, Nat.mod_lt _ (by norm_num)⟩

theorem perm_eq_fast : ∀ g : Fin 8, ∀ i : Fin 25, permFast g i = perm g i := by
  decide +kernel

def permEmbFast (g : Fin 8) : Fin 25 ↪ Fin 25 :=
  ⟨permFast g, fun i j h => perm_injective_checked g i j (by rw [← perm_eq_fast, ← perm_eq_fast, h])⟩

theorem permEmbFast_eq (g : Fin 8) : permEmbFast g = permEmb g := by
  ext i; exact congrArg Fin.val (perm_eq_fast g i)

/-- Some symmetry maps `s` onto the cells of a mask in `S`. -/
def reachesIn (S : Std.HashSet ℕ) (s : Finset (Fin 25)) : Bool :=
  (List.finRange 8).any (fun g =>
    S.contains (toMask (s.map (permEmbFast g))) &&
      decide (ofMask (toMask (s.map (permEmbFast g))) = s.map (permEmbFast g)))

theorem reachesIn_sound (s : Finset (Fin 25))
    (h : reachesIn (Std.HashSet.ofList censusMasks) s = true) :
    ∃ g : Fin 8, ∃ m ∈ censusMasks, s.map (permEmb g) = ofMask m := by
  simp only [reachesIn, List.any_eq_true, Bool.and_eq_true, decide_eq_true_eq] at h
  obtain ⟨g, _, hc, he⟩ := h
  rw [permEmbFast_eq] at hc he
  refine ⟨g, _, ?_, he.symm⟩
  rw [Std.HashSet.contains_ofList] at hc
  exact List.contains_iff_mem.mp hc

/-- The whole finite check over all 19-element sublists of the 25 cells. The census set is an
argument so that it is built once. -/
def orbitCheck (S : Std.HashSet ℕ) : Bool :=
  ((List.finRange 25).sublistsLen 19).all (fun l => reachesIn S l.toFinset)

/-- **Finite orbit check** (`native_decide`): every 19-cell set reaches a census mask. -/
theorem orbit_check : orbitCheck (Std.HashSet.ofList censusMasks) = true := by
  native_decide

/-- Every 19-cell set is a 19-element sublist of the cell list. -/
theorem finset_as_sublist (s : Finset (Fin 25)) (hs : s.card = 19) :
    ∃ l ∈ (List.finRange 25).sublistsLen 19, l.toFinset = s := by
  classical
  let l := (List.finRange 25).filter (fun i => decide (i ∈ s))
  have hl : l.toFinset = s := by
    ext i; simp [l]
  have hnd : l.Nodup := (List.nodup_finRange 25).filter _
  refine ⟨l, List.mem_sublistsLen.mpr ⟨List.filter_sublist, ?_⟩, hl⟩
  rw [← List.toFinset_card_of_nodup hnd, hl, hs]

theorem orbit_cover (s : Finset (Fin 25)) (hs : s.card = 19) :
    ∃ g : Fin 8, ∃ m ∈ censusMasks, s.map (permEmb g) = ofMask m := by
  obtain ⟨l, hl, rfl⟩ := finset_as_sublist s hs
  exact reachesIn_sound _ ((List.all_eq_true.mp orbit_check) l hl)

/-! ## Packings reach a census mask -/

/-- **Orbit step.** For `L ≤ 2443/500`, a packing of 19 unit squares in `[0, L]^2`, shifted by
`(σ, σ)`, `σ = (2443/500 - L)/2`, and then moved by one symmetry `g`, is a packing in the frame
`[σ, σ + L]^2 ⊆ [0, 2443/500]^2` whose centres lie in pairwise distinct cells, exactly the
occupied cells of census case `k`. -/
theorem packing_reaches_census (L : ℝ) (hL : L ≤ 2443/500)
    (p u : Fin 19 → ℝ × ℝ) (hunit : ∀ i, (u i).1^2+(u i).2^2=1)
    (hfit : ∀ i, Sq17.sq (p i).1 (p i).2 (u i).1 (u i).2 ⊆ containerBox L)
    (hdis : ∀ i j, i ≠ j → Disjoint
      (interior (Sq17.sq (p i).1 (p i).2 (u i).1 (u i).2))
      (interior (Sq17.sq (p j).1 (p j).2 (u j).1 (u j).2))) :
    ∃ g : Fin 8, ∃ k : Fin censusMasks.length,
      (∀ i, (dirG g (u i)).1^2+(dirG g (u i)).2^2=1) ∧
      (∀ i, Sq17.sq (actG g (shifted L (p i))).1 (actG g (shifted L (p i))).2
        (dirG g (u i)).1 (dirG g (u i)).2 ⊆ frameBox L) ∧
      (∀ i j, i ≠ j → Disjoint
        (interior (Sq17.sq (actG g (shifted L (p i))).1 (actG g (shifted L (p i))).2
          (dirG g (u i)).1 (dirG g (u i)).2))
        (interior (Sq17.sq (actG g (shifted L (p j))).1 (actG g (shifted L (p j))).2
          (dirG g (u j)).1 (dirG g (u j)).2))) ∧
      ∃ c : Fin 19 → Fin 25, Function.Injective c ∧
        Finset.univ.image c = ofMask (censusMasks.get k) ∧
        ∀ i, actG g (shifted L (p i)) ∈ cell (c i) := by
  classical
  obtain ⟨assign, hinj, ha⟩ := exists_injective_cell_assignment L hL p u hunit hfit hdis
  have hcard : (Finset.univ.image assign).card = 19 := by
    rw [Finset.card_image_of_injective _ hinj]; simp
  obtain ⟨g, m, hm, hmap⟩ := orbit_cover _ hcard
  obtain ⟨k, hk⟩ := List.get_of_mem hm
  refine ⟨g, k, fun i => dir_unit _ _ _ _ (hunit i), fun i => ?_, fun i j hij => ?_,
    fun i => perm g (assign i), ?_, ?_, fun i => actG_mem_cell g _ (ha i)⟩
  · exact act_square_subset _ _ _ _ (fun z hz => act_frameBox _ _ _ L z hz) _ _
      (shifted_fit_frame L _ _ (hfit i))
  · exact act_disjoint _ _ _ _ _ _ _ (hunit i) (hunit j)
      (shifted_disjoint L _ _ _ _ (hunit i) (hunit j) (hdis i j hij))
  · exact fun i j h => hinj (perm_injective_checked g _ _ h)
  · rw [hk, ← hmap, Finset.map_eq_image, Finset.image_image]
    rfl

/-- The frame of `packing_reaches_census` lies in the cover-frame container. -/
theorem frame_in_container (L : ℝ) (hL : L ≤ 2443/500) :
    frameBox L ⊆ containerBox (2443/500) := frameBox_subset L hL

end Sq19.Cover

#print axioms Sq19.Cover.vertex_action_checked
#print axioms Sq19.Cover.actG_mem_cell
#print axioms Sq19.Cover.orbit_check
#print axioms Sq19.Cover.orbit_cover
#print axioms Sq19.Cover.packing_reaches_census
