import Sqpack.Spec
import Sqpack.SpecBridge
import Sqpack.SpecFC
import Sqpack.Attain

/-!
# Bridge to chelokot's square-packing archive

The archive `chelokot/square-packing-archive` (GitHub; we read commit `753079e`) proves exact
values of `s(n)` in Lean 4, e.g. `s6_eq_three : IsMinimumSide 6 3`
(`formal/SquarePackingArchive/Records/Square6Exact.lean`), and likewise `s10_eq_goebel`,
`s13_eq_four`, `s22_eq_five`, `s33_eq_six` and others in `formal/SquarePackingArchive/Records/`.
Their framework lives in `formal/SquarePackingArchive/Geometry.lean` (`Point`, `Frame`,
`PlacedSquare`, `PlacedSquare.Contains` / `InteriorContains` / `Fits` / `InteriorDisjoint`,
`Container.Contains`, `Packing`, `HasPacking`, `IsLowerBound`, `IsMinimumSide`).

**Nothing is imported or copied from that repository.**  The definitions in the namespace
`UnitSquarePacking.Chelokot` below are our own restatements of theirs, written from the
mathematics and checked against their source by reading (no code of theirs was built or run).
In words, their definitions are:

* a *frame* is a pair `(cos, sin)` of reals with `cos² + sin² = 1`, acting on local coordinates
  by `(a, b) ↦ (a cos − b sin, a sin + b cos)` (a counterclockwise rotation; no reflections);
* a *placed square* is a centre point and a frame; the point with local coordinates `(a, b)` is
  the centre plus the frame applied to `(a, b)`;
* the square *contains* a point if it is the point with local coordinates `(a, b)` for some
  `|a| ≤ 1/2`, `|b| ≤ 1/2` (closed unit square); it *interior-contains* it if this holds with
  `|a| < 1/2`, `|b| < 1/2`;
* the *container* of side `s` is `{(x, y) | 0 ≤ x ≤ s, 0 ≤ y ≤ s}` (closed), and a square *fits*
  if every point it contains is in the container;
* two squares are *interior-disjoint* if no point is interior-contained in both;
* a *packing* of `n` squares with side `s` is a family `Fin n → PlacedSquare` with `0 ≤ s`, every
  square fitting, and distinct indices interior-disjoint; `HasPacking n s` says one exists;
* `IsLowerBound n a`: every `s` with `HasPacking n s` has `a ≤ s`;
  `IsMinimumSide n s`: `HasPacking n s ∧ IsLowerBound n s`.

These agree with `Sqpack/Spec.lean` (closed squares, closed box, disjoint interiors,
counterclockwise rotation by the angle whose `(cos, sin)` is the frame) with **one difference**:
their `Packing` carries the field `0 ≤ side`, ours does not.  So `HasPacking n s ↔ Packs n s ∧
0 ≤ s` for every `n` (`hasPacking_iff`), and for `n ≥ 1` the side condition is automatic
(`hasPacking_iff_packs`).  For `n = 0` the two differ: their `IsMinimumSide 0 0` holds, while
`{s | Packs 0 s} = univ` has no least element.  All their records have `n ≥ 1`.

Main results:

* `hasPacking_iff`, `hasPacking_iff_packs`, `setOf_hasPacking_eq`;
* `isLowerBound_iff (hn : 1 ≤ n) : IsLowerBound n a ↔ ∀ s, Packs n s → a ≤ s`;
* `isMinimumSide_iff_isLeast (hn : 1 ≤ n) : IsMinimumSide n s ↔ IsLeast {s | Packs n s} s`;
* `isMinimumSide_iff_minSide_eq (hn : 1 ≤ n) : IsMinimumSide n s ↔ minSide n = s`.

**Corollary (remark, not an import).**  Their `s6_eq_three : IsMinimumSide 6 3` gives, by
`isMinimumSide_iff_minSide_eq (n := 6)`, `UnitSquarePacking.minSide 6 = 3` and
`IsLeast {s | Packs 6 s} 3`; in the same way `s10_eq_goebel` gives `minSide 10 = 3 + √2/2`,
`s13_eq_four` gives `minSide 13 = 4`, `s22_eq_five` gives `minSide 22 = 5` and `s33_eq_six`
gives `minSide 33 = 6` — provided their `IsMinimumSide` is the predicate restated here, which is
what we checked by reading `Geometry.lean` at `753079e`.  (Their proofs themselves are not
checked by this file; to make the transfer formal one would build both projects together and
prove their `IsMinimumSide` equal to `Chelokot.IsMinimumSide`, which is `Iff.rfl` up to names.)
-/

namespace UnitSquarePacking.Chelokot

open Set

/-! ## The restated definitions -/

/-- A point of the plane, with named coordinates. -/
structure Point where
  x : ℝ
  y : ℝ

/-- An orientation: a unit vector `(cos, sin)`. -/
structure Frame where
  cos : ℝ
  sin : ℝ
  unit : cos ^ 2 + sin ^ 2 = 1

/-- A unit square placed in the plane: centre and orientation. -/
structure PlacedSquare where
  center : Point
  frame : Frame

/-- The point with local coordinates `(a, b)` relative to the square. -/
def PlacedSquare.point (q : PlacedSquare) (a b : ℝ) : Point :=
  ⟨q.center.x + (a * q.frame.cos - b * q.frame.sin),
    q.center.y + (a * q.frame.sin + b * q.frame.cos)⟩

/-- The closed square contains `p`. -/
def PlacedSquare.Contains (q : PlacedSquare) (p : Point) : Prop :=
  ∃ a b : ℝ, |a| ≤ 1 / 2 ∧ |b| ≤ 1 / 2 ∧ p = q.point a b

/-- The open square contains `p`. -/
def PlacedSquare.InteriorContains (q : PlacedSquare) (p : Point) : Prop :=
  ∃ a b : ℝ, |a| < 1 / 2 ∧ |b| < 1 / 2 ∧ p = q.point a b

/-- The closed container `[0, s]²`. -/
def ContainerContains (s : ℝ) (p : Point) : Prop :=
  0 ≤ p.x ∧ p.x ≤ s ∧ 0 ≤ p.y ∧ p.y ≤ s

/-- Every point of the closed square is in the container. -/
def PlacedSquare.Fits (q : PlacedSquare) (s : ℝ) : Prop :=
  ∀ ⦃p⦄, q.Contains p → ContainerContains s p

/-- No point lies in both open squares. -/
def PlacedSquare.InteriorDisjoint (q r : PlacedSquare) : Prop :=
  ∀ p, ¬(q.InteriorContains p ∧ r.InteriorContains p)

/-- A packing of `n` unit squares in the container of side `s` (note the field `0 ≤ s`). -/
structure Packing (n : ℕ) (s : ℝ) where
  squares : Fin n → PlacedSquare
  side_nonneg : 0 ≤ s
  fits : ∀ i, (squares i).Fits s
  disjoint : ∀ i j, i ≠ j → (squares i).InteriorDisjoint (squares j)

def HasPacking (n : ℕ) (s : ℝ) : Prop := Nonempty (Packing n s)

def IsLowerBound (n : ℕ) (a : ℝ) : Prop := ∀ s, HasPacking n s → a ≤ s

def IsMinimumSide (n : ℕ) (s : ℝ) : Prop := HasPacking n s ∧ IsLowerBound n s

/-! ## Points and squares in `Spec.lean` terms -/

/-- `Point ≃ ℝ × ℝ`. -/
def toP (p : Point) : ℝ × ℝ := (p.x, p.y)

/-- The inverse of `toP`. -/
def ofP (x : ℝ × ℝ) : Point := ⟨x.1, x.2⟩

@[simp] lemma toP_ofP (x : ℝ × ℝ) : toP (ofP x) = x := rfl

lemma toP_injective : Function.Injective toP := by
  rintro ⟨_, _⟩ ⟨_, _⟩ h
  simp only [toP, Prod.mk.injEq] at h
  rw [h.1, h.2]

/-- Every frame is `(cos θ, sin θ)` for some angle `θ`. -/
lemma Frame.exists_angle (f : Frame) : ∃ θ, Real.cos θ = f.cos ∧ Real.sin θ = f.sin :=
  exists_cos_sin f.unit

/-- The frame of the angle `θ`. -/
noncomputable def Frame.ofAngle (θ : ℝ) : Frame :=
  ⟨Real.cos θ, Real.sin θ, Real.cos_sq_add_sin_sq θ⟩

lemma toP_point {q : PlacedSquare} {θ : ℝ} (hc : Real.cos θ = q.frame.cos)
    (hs : Real.sin θ = q.frame.sin) (a b : ℝ) :
    toP (q.point a b) = toP q.center + rot θ (a, b) := by
  simp only [toP, PlacedSquare.point, rot, hc, hs, Prod.mk_add_mk]
  congr 1 <;> ring

lemma mem_Icc_half (a : ℝ) : a ∈ Icc (-1/2 : ℝ) (1/2) ↔ |a| ≤ 1 / 2 := by
  rw [mem_Icc, abs_le]; norm_num

lemma mem_Ioo_half (a : ℝ) : a ∈ Ioo (-1/2 : ℝ) (1/2) ↔ |a| < 1 / 2 := by
  rw [mem_Ioo, abs_lt]; norm_num

/-- The closed placed square is `unitSq` at the same centre, at an angle `θ` with
`(cos θ, sin θ)` equal to its frame. -/
lemma contains_iff {q : PlacedSquare} {θ : ℝ} (hc : Real.cos θ = q.frame.cos)
    (hs : Real.sin θ = q.frame.sin) (p : Point) :
    q.Contains p ↔ toP p ∈ unitSq (toP q.center) θ := by
  constructor
  · rintro ⟨a, b, ha, hb, rfl⟩
    exact ⟨(a, b), ⟨(mem_Icc_half a).mpr ha, (mem_Icc_half b).mpr hb⟩,
      (toP_point hc hs a b).symm⟩
  · rintro ⟨⟨a, b⟩, ⟨ha, hb⟩, he⟩
    refine ⟨a, b, (mem_Icc_half a).mp ha, (mem_Icc_half b).mp hb, toP_injective ?_⟩
    rw [toP_point hc hs]; exact he.symm

/-- The open placed square is the interior of that `unitSq`. -/
lemma interiorContains_iff {q : PlacedSquare} {θ : ℝ} (hc : Real.cos θ = q.frame.cos)
    (hs : Real.sin θ = q.frame.sin) (p : Point) :
    q.InteriorContains p ↔ toP p ∈ interior (unitSq (toP q.center) θ) := by
  have h : interior (unitSq (toP q.center) θ) =
      (fun r => toP q.center + rot θ r) '' (Ioo (-1/2) (1/2) ×ˢ Ioo (-1/2) (1/2)) := by
    rw [unitSq, ← interior_Icc, ← interior_prod_eq]
    exact ((place (toP q.center) θ).image_interior _).symm
  rw [h]
  constructor
  · rintro ⟨a, b, ha, hb, rfl⟩
    exact ⟨(a, b), ⟨(mem_Ioo_half a).mpr ha, (mem_Ioo_half b).mpr hb⟩,
      (toP_point hc hs a b).symm⟩
  · rintro ⟨⟨a, b⟩, ⟨ha, hb⟩, he⟩
    refine ⟨a, b, (mem_Ioo_half a).mp ha, (mem_Ioo_half b).mp hb, toP_injective ?_⟩
    rw [toP_point hc hs]; exact he.symm

lemma containerContains_iff (s : ℝ) (p : Point) :
    ContainerContains s p ↔ toP p ∈ container s := by
  simp only [ContainerContains, toP, container, mem_prod, mem_Icc]
  tauto

lemma fits_iff {q : PlacedSquare} {θ : ℝ} (hc : Real.cos θ = q.frame.cos)
    (hs : Real.sin θ = q.frame.sin) (s : ℝ) :
    q.Fits s ↔ unitSq (toP q.center) θ ⊆ container s := by
  constructor
  · intro h x hx
    rw [← toP_ofP x, ← containerContains_iff]
    exact h ((contains_iff hc hs _).mpr hx)
  · intro h p hp
    exact (containerContains_iff s p).mpr (h ((contains_iff hc hs p).mp hp))

lemma interiorDisjoint_iff {q r : PlacedSquare} {θ φ : ℝ} (hc : Real.cos θ = q.frame.cos)
    (hs : Real.sin θ = q.frame.sin) (hc' : Real.cos φ = r.frame.cos)
    (hs' : Real.sin φ = r.frame.sin) :
    q.InteriorDisjoint r ↔
      Disjoint (interior (unitSq (toP q.center) θ)) (interior (unitSq (toP r.center) φ)) := by
  rw [Set.disjoint_left]
  constructor
  · intro h x hx hy
    exact h (ofP x) ⟨(interiorContains_iff hc hs _).mpr hx, (interiorContains_iff hc' hs' _).mpr hy⟩
  · rintro h p ⟨hp, hp'⟩
    exact h ((interiorContains_iff hc hs p).mp hp) ((interiorContains_iff hc' hs' p).mp hp')

/-! ## The packing predicates -/

/-- **Their packing predicate is ours plus `0 ≤ s`** (for every `n`). -/
theorem hasPacking_iff (n : ℕ) (s : ℝ) : HasPacking n s ↔ Packs n s ∧ 0 ≤ s := by
  constructor
  · rintro ⟨P⟩
    choose θ hc hs using fun i => (P.squares i).frame.exists_angle
    refine ⟨⟨fun i => toP (P.squares i).center, θ, fun i => (fits_iff (hc i) (hs i) s).mp
      (P.fits i), fun i j hij => (interiorDisjoint_iff (hc i) (hs i) (hc j) (hs j)).mp
      (P.disjoint i j hij)⟩, P.side_nonneg⟩
  · rintro ⟨⟨c, θ, hin, hdisj⟩, hs0⟩
    let sq : Fin n → PlacedSquare := fun i => ⟨ofP (c i), Frame.ofAngle (θ i)⟩
    have hc : ∀ i, Real.cos (θ i) = (sq i).frame.cos := fun _ => rfl
    have hs : ∀ i, Real.sin (θ i) = (sq i).frame.sin := fun _ => rfl
    exact ⟨⟨sq, hs0, fun i => (fits_iff (hc i) (hs i) s).mpr (hin i),
      fun i j hij => (interiorDisjoint_iff (hc i) (hs i) (hc j) (hs j)).mpr (hdisj hij)⟩⟩

/-- For `n ≥ 1` their packing predicate is exactly `Packs n s`. -/
theorem hasPacking_iff_packs {n : ℕ} (hn : 1 ≤ n) (s : ℝ) : HasPacking n s ↔ Packs n s := by
  rw [hasPacking_iff]
  exact ⟨And.left, fun h => ⟨h, nonneg_of_packs hn h⟩⟩

theorem setOf_hasPacking_eq (n : ℕ) : {s | HasPacking n s} = {s | Packs n s} ∩ Ici 0 :=
  Set.ext fun s => hasPacking_iff n s

theorem setOf_hasPacking_eq_of_pos {n : ℕ} (hn : 1 ≤ n) :
    {s | HasPacking n s} = {s | Packs n s} :=
  Set.ext fun s => hasPacking_iff_packs hn s

/-! ## Lower bounds and minimum sides -/

theorem isLowerBound_iff {n : ℕ} (hn : 1 ≤ n) (a : ℝ) :
    IsLowerBound n a ↔ ∀ s, Packs n s → a ≤ s := by
  simp only [IsLowerBound, hasPacking_iff_packs hn]

theorem isMinimumSide_iff_isLeast {n : ℕ} (hn : 1 ≤ n) (s : ℝ) :
    IsMinimumSide n s ↔ IsLeast {s | Packs n s} s := by
  rw [IsMinimumSide, isLowerBound_iff hn, hasPacking_iff_packs hn]
  rfl

/-- `minSide` of `Spec.lean` is attained (`SquarePacking.isLeast_minSide`, transferred). -/
theorem isLeast_minSide {n : ℕ} (hn : 1 ≤ n) : IsLeast {s | Packs n s} (minSide n) := by
  have h := SquarePacking.isLeast_minSide hn
  rw [minSide_eq] at h
  simpa only [packs_iff] using h

theorem minSide_eq_iff_isLeast {n : ℕ} (hn : 1 ≤ n) {k : ℝ} :
    minSide n = k ↔ IsLeast {s | Packs n s} k :=
  ⟨fun h => h ▸ isLeast_minSide hn, IsLeast.csInf_eq⟩

/-- **Their exact values are ours**: for `n ≥ 1`, `IsMinimumSide n s ↔ minSide n = s`.  So their
`s6_eq_three : IsMinimumSide 6 3` would give `minSide 6 = 3` (see the module docstring). -/
theorem isMinimumSide_iff_minSide_eq {n : ℕ} (hn : 1 ≤ n) (s : ℝ) :
    IsMinimumSide n s ↔ minSide n = s := by
  rw [isMinimumSide_iff_isLeast hn, minSide_eq_iff_isLeast hn]

/-- The one disagreement, at `n = 0`: their `IsMinimumSide 0 0` holds, but `Packs 0 s` holds for
every `s`, so `{s | Packs 0 s}` has no least element. -/
theorem isMinimumSide_zero : IsMinimumSide 0 0 ∧ ¬∃ k, IsLeast {s | Packs 0 s} k := by
  have hP : ∀ s, Packs 0 s := fun s => ⟨Fin.elim0, Fin.elim0, fun i => i.elim0, fun i => i.elim0⟩
  refine ⟨⟨(hasPacking_iff 0 0).mpr ⟨hP 0, le_rfl⟩,
    fun s hs => ((hasPacking_iff 0 s).mp hs).2⟩, ?_⟩
  rintro ⟨k, -, hk⟩
  have := hk (hP (k - 1))
  linarith

end UnitSquarePacking.Chelokot
