import Sq19Lean.Capture.CensusCapture
import Sq19Lean.Capture.Region

/-! Lower bound from the census, the three capture states and the local hull theorem.

`lower_bound_from_capture`: every family of 19 unit squares with pairwise disjoint interiors in `[0, L]^2` has
`side19 ≤ L`, given as named hypotheses the parts that are not in this file:
* `hexcl`, `hsurv`: the census exclusions (generated module `Complete`) and the list of masks they leave;
* `htree`: the four survivors settled by branch trees (census indices other than 3435, 3438, 3442);
* `hmirror`: state 3435's piece P0 (a13 <= -3.5 deg), whose targets are H through the anti-diagonal mirror;
* `hlocal`: the local hull theorem `Sq19.Endgame.Reduction.side19_le_of_hull` (passed in so that this file does
  not rebuild the 2304-check certificate).
The capture states 3442, 3438 and the P2 piece of 3435 are discharged here through `census_capture`,
`good_of_targets` and the finite checks of `Region`. -/
namespace Sq19.Capture
open Sq17.Propagation Sq17.Propagation.HalfPlaneState Sq17.Propagation.HalfPlaneState.CaptureSummary Sq19.Milp

/-- The census output (as `Sq19.Cover.packing_reaches_census` gives it) for one census index. -/
structure CensusOut (L : ℝ) (k : ℕ) where
  q : Fin 19 → ℝ × ℝ
  u : Fin 19 → ℝ × ℝ
  c : Fin 19 → Fin 25
  hu : ∀ i, (u i).1^2+(u i).2^2 = 1
  hf : ∀ i, Sq17.sq (q i).1 (q i).2 (u i).1 (u i).2 ⊆ Sq19.Cover.frameBox L
  hd : ∀ i j, i ≠ j → Disjoint
    (interior (Sq17.sq (q i).1 (q i).2 (u i).1 (u i).2))
    (interior (Sq17.sq (q j).1 (q j).2 (u j).1 (u j).2))
  hcell : ∀ i, q i ∈ Sq19.Cover.cell (c i)
  himg : Finset.univ.image c = Sq19.Cover.ofMask (Sq19.Cover.censusMasks.getD k 0)

theorem S3442.good (L : ℝ) (hL : L ≤ S3442.side) (o : CensusOut L 3442) :
    ∃ θ dx dy : ℕ → ℝ, Good Endgame.Hull.prob θ dx dy L := by
  obtain ⟨π, -, p, -, hT, hbox, hdis⟩ :=
    S3442.census_capture L hL o.q o.u o.c o.hu o.hf o.hd o.hcell o.himg
  have heq : S3442.P2.targets = Region.S3442.targets := rfl
  rw [heq] at hT
  have hA : (Region.S3442.Amin : ℝ) ≤ (2443/500 - L)/2 - S3442.sigma := by
    have : (Region.S3442.Amin : ℝ) = (2443/500 - S3442.side)/2 - S3442.sigma := by
      simp only [Region.S3442.Amin, S3442.side, S3442.sigma]; norm_num
    rw [this]; linarith
  exact good_of_targets Region.S3442.targets Region.S3442.own Region.S3442.kq Region.S3442.A Region.S3442.Amin
    Region.S3442.Xw Region.S3442.Phi Region.S3442.own_lt Region.S3442.own_inj rfl Region.S3442.sq_ok
    Region.S3442.wall_ok Region.S3442.kq0 L _ hA p hT hbox hdis

theorem S3438.good (L : ℝ) (hL : L ≤ S3438.side) (o : CensusOut L 3438) :
    ∃ θ dx dy : ℕ → ℝ, Good Endgame.Hull.prob θ dx dy L := by
  obtain ⟨π, -, p, -, hT, hbox, hdis⟩ :=
    S3438.census_capture L hL o.q o.u o.c o.hu o.hf o.hd o.hcell o.himg
  have heq : S3438.P0.targets = Region.S3438.targets := rfl
  rw [heq] at hT
  have hA : (Region.S3438.Amin : ℝ) ≤ (2443/500 - L)/2 - S3438.sigma := by
    have : (Region.S3438.Amin : ℝ) = (2443/500 - S3438.side)/2 - S3438.sigma := by
      simp only [Region.S3438.Amin, S3438.side, S3438.sigma]; norm_num
    rw [this]; linarith
  exact good_of_targets Region.S3438.targets Region.S3438.own Region.S3438.kq Region.S3438.A Region.S3438.Amin
    Region.S3438.Xw Region.S3438.Phi Region.S3438.own_lt Region.S3438.own_inj rfl Region.S3438.sq_ok
    Region.S3438.wall_ok Region.S3438.kq0 L _ hA p hT hbox hdis

/-- State 3435: the P2 branch here; the P0 branch (mirrored targets) is the hypothesis `hmirror`. -/
theorem S3435.good (L : ℝ) (hL : L ≤ S3435.side) (o : CensusOut L 3435)
    (hmirror : ∀ p : ℕ → AnglePose, (∀ i : Fin 19, (S3435.P0.targets[i.val]!).Holds (p i.val)) →
      (∀ j : Fin 19, (p j.val).square ⊆ boxA ((2443/500 - L)/2 - S3435.sigma) L) →
      (∀ i j : Fin 19, i ≠ j → Disjoint (interior (p i.val).square) (interior (p j.val).square)) →
      ∃ θ dx dy : ℕ → ℝ, Good Endgame.Hull.prob θ dx dy L) :
    ∃ θ dx dy : ℕ → ℝ, Good Endgame.Hull.prob θ dx dy L := by
  obtain ⟨π, -, p, -, hT, hbox, hdis⟩ :=
    S3435.census_capture L hL o.q o.u o.c o.hu o.hf o.hd o.hcell o.himg
  rcases hT with h0 | h2
  · exact hmirror p h0 hbox hdis
  have heq : S3435.P2.targets = Region.S3435.targets := rfl
  rw [heq] at h2
  have hA : (Region.S3435.Amin : ℝ) ≤ (2443/500 - L)/2 - S3435.sigma := by
    have : (Region.S3435.Amin : ℝ) = (2443/500 - S3435.side)/2 - S3435.sigma := by
      simp only [Region.S3435.Amin, S3435.side, S3435.sigma]; norm_num
    rw [this]; linarith
  exact good_of_targets Region.S3435.targets Region.S3435.own Region.S3435.kq Region.S3435.A Region.S3435.Amin
    Region.S3435.Xw Region.S3435.Phi Region.S3435.own_lt Region.S3435.own_inj rfl Region.S3435.sq_ok
    Region.S3435.wall_ok Region.S3435.kq0 L _ hA p h2 hbox hdis

/-- State 3435, piece P0 (mirrored targets) into `Hull.prob`. -/
theorem S3435.mirror (L : ℝ) (hL : L ≤ S3435.side) (p : ℕ → AnglePose)
    (hT : ∀ i : Fin 19, (S3435.P0.targets[i.val]!).Holds (p i.val))
    (hbox : ∀ j : Fin 19, (p j.val).square ⊆ boxA ((2443/500 - L)/2 - S3435.sigma) L)
    (hdis : ∀ i j : Fin 19, i ≠ j → Disjoint (interior (p i.val).square) (interior (p j.val).square)) :
    ∃ θ dx dy : ℕ → ℝ, Good Endgame.Hull.prob θ dx dy L := by
  have heq : S3435.P0.targets = Region.S3435P0.targets := rfl
  rw [heq] at hT
  have hD : L + (Region.S3435P0.A : ℝ) ≤ Region.S3435P0.Dhi := by
    have : (Region.S3435P0.Dhi : ℝ) = S3435.side + Region.S3435P0.A := by
      simp only [Region.S3435P0.Dhi, Region.S3435P0.A, S3435.side]; norm_num
    rw [this]; linarith
  exact good_of_targets_mirror Region.S3435P0.targets Region.S3435P0.own Region.S3435P0.kq Region.S3435P0.A
    Region.S3435P0.Xw Region.S3435P0.Phi Region.S3435P0.Y0 Region.S3435P0.Phi2 Region.S3435P0.Dlo
    Region.S3435P0.Dhi 2 0 Region.S3435P0.own_lt Region.S3435P0.own_inj (by norm_num) (by norm_num)
    Region.S3435P0.sq_ok Region.S3435P0.wall_ok Region.S3435P0.top_ok L _ hD p hT hbox hdis

/-- `side19` is below the capture side `side19 + 1e-12` (the same rational in all three states). -/
theorem side19_lt_side : Sq19.side19 < S3442.side := by
  have h2 : Real.sqrt 2 < 1414213562373096 / 10 ^ 15 := by
    rw [Real.sqrt_lt' (by norm_num)]; norm_num
  simp only [Sq19.side19, S3442.side]; push_cast; nlinarith [Real.sqrt_nonneg 2]

theorem sides_eq : S3435.side = S3442.side ∧ S3438.side = S3442.side := ⟨rfl, rfl⟩

theorem lower_bound_from_capture
    (Excluded : ℕ → Prop)
    (hexcl : ∀ m, Excluded m → ∀ {n : ℕ} (assign : Fin n → Fin 25),
      (∀ d : Fin 25, m.testBit d = true → ∃ j, assign j = d) → ¬ Sq19.Census.Packs assign)
    (hsurv : ∀ k : Fin Sq19.Cover.censusMasks.length, ¬ Excluded (Sq19.Cover.censusMasks.get k) →
      k.val = 3435 ∨ k.val = 3438 ∨ k.val = 3442 ∨ k.val ∈ ([1, 2, 5423, 5453] : List ℕ))
    (htree : ∀ (L : ℝ), L ≤ 2443/500 → ∀ k : Fin Sq19.Cover.censusMasks.length,
      k.val ∈ ([1, 2, 5423, 5453] : List ℕ) → ∀ c : Fin 19 → Fin 25,
      Finset.univ.image c = Sq19.Cover.ofMask (Sq19.Cover.censusMasks.get k) → Sq19.Census.Packs c → False)
    (hmirror : ∀ (L : ℝ) (p : ℕ → AnglePose), (∀ i : Fin 19, (S3435.P0.targets[i.val]!).Holds (p i.val)) →
      (∀ j : Fin 19, (p j.val).square ⊆ boxA ((2443/500 - L)/2 - S3435.sigma) L) →
      (∀ i j : Fin 19, i ≠ j → Disjoint (interior (p i.val).square) (interior (p j.val).square)) →
      ∃ θ dx dy : ℕ → ℝ, Good Endgame.Hull.prob θ dx dy L)
    (hlocal : ∀ (θ dx dy : ℕ → ℝ) (L : ℝ), Good Endgame.Hull.prob θ dx dy L → Sq19.side19 ≤ L)
    (L : ℝ) (p u : Fin 19 → ℝ × ℝ) (hunit : ∀ i, (u i).1^2+(u i).2^2 = 1)
    (hfit : ∀ i, Sq17.sq (p i).1 (p i).2 (u i).1 (u i).2 ⊆ containerBox L)
    (hdis : ∀ i j, i ≠ j → Disjoint
      (interior (Sq17.sq (p i).1 (p i).2 (u i).1 (u i).2))
      (interior (Sq17.sq (p j).1 (p j).2 (u j).1 (u j).2))) :
    Sq19.side19 ≤ L := by
  by_contra hlt
  push_neg at hlt
  have hLs : L ≤ S3442.side := le_trans hlt.le side19_lt_side.le
  have hLU : L ≤ 2443/500 := by
    have : (S3442.side : ℝ) ≤ 2443/500 := by simp only [S3442.side]; norm_num
    linarith
  obtain ⟨g, k, hu, hf, hd, c, hinj, himg, hcell⟩ :=
    Sq19.Cover.packing_reaches_census L hLU p u hunit hfit hdis
  have hpacks : Sq19.Census.Packs c := by
    refine ⟨fun i => Sq19.Cover.actG g (Sq19.Cover.shifted L (p i)), fun i => Sq19.Cover.dirG g (u i), hu,
      fun i => ?_, fun i => (hf i).trans (Sq19.Cover.frame_in_container L hLU), hd⟩
    rw [← Sq19.Assembly.cell_eq]; exact hcell i
  have hne : ¬ Excluded (Sq19.Cover.censusMasks.get k) :=
    fun he => hexcl _ he c (Sq19.Assembly.sub_of_image c himg) hpacks
  have hget : ∀ n, k.val = n → Sq19.Cover.censusMasks.get k = Sq19.Cover.censusMasks.getD n 0 := by
    intro n hn; subst hn; simp [List.getD_eq_getElem?_getD]
  let o : ∀ n, k.val = n → CensusOut L n := fun n hn =>
    ⟨fun i => Sq19.Cover.actG g (Sq19.Cover.shifted L (p i)), fun i => Sq19.Cover.dirG g (u i), c, hu, hf, hd,
      hcell, by rw [himg, hget n hn]⟩
  rcases hsurv k hne with h | h | h | h
  · obtain ⟨θ, dx, dy, hg⟩ := S3435.good L (by rw [sides_eq.1]; exact hLs) (o 3435 h) (hmirror L)
    exact absurd (hlocal θ dx dy L hg) (not_le.mpr hlt)
  · obtain ⟨θ, dx, dy, hg⟩ := S3438.good L (by rw [sides_eq.2]; exact hLs) (o 3438 h)
    exact absurd (hlocal θ dx dy L hg) (not_le.mpr hlt)
  · obtain ⟨θ, dx, dy, hg⟩ := S3442.good L hLs (o 3442 h)
    exact absurd (hlocal θ dx dy L hg) (not_le.mpr hlt)
  · exact htree L hLU k h c himg hpacks

end Sq19.Capture

#print axioms Sq19.Capture.lower_bound_from_capture
