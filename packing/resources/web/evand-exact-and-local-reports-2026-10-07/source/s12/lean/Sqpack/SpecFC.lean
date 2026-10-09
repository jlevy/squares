import Sqpack.Spec
import Sqpack.FCSquarePacking

/-!
# Bridge to formal-conjectures' definitions

`packs_iff_nonempty_packing : Packs n x ↔ Nonempty (Packing n UnitSquare (Square x))`, where
`Packing`, `UnitSquare`, `Square` are formal-conjectures' (`Sqpack/FCSquarePacking.lean`): open
unit squares placed by isometric equivalences of `EuclideanSpace ℝ (Fin 2)`, pairwise disjoint,
inside the open square `(0, x)²`.

* Isometries are affine (Mazur–Ulam, `IsometryEquiv.toRealLinearIsometryEquiv`), and their linear
  part maps the standard basis to an orthonormal pair `u, v`; so `u = (cos φ, sin φ)` and
  `v = ε (-sin φ, cos φ)` with `ε = ±1` (`exists_frame`).
* Either way the image of the open unit square is the interior of a closed unit square
  (`frame_image`: a reflection `ε = -1` maps the square onto itself).
* Open squares in `(0, x)²` ↔ closed squares in `[0, x]²`: interior and closure.

The equivalence holds for every `n` and `x` (for `n = 0` both sides are trivially true), and
`setOf_packs_eq` turns it into an equality of the sets of admissible sides.
-/

namespace UnitSquarePacking

open Set FCSquarePacking

/-! ## Coordinates -/

/-- `EuclideanSpace ℝ (Fin 2) ≃ ℝ × ℝ`, `p ↦ (p 0, p 1)`. -/
noncomputable def toPair : ℝ² ≃ ℝ × ℝ where
  toFun p := (p 0, p 1)
  invFun x := !₂[x.1, x.2]
  left_inv p := by ext i; fin_cases i <;> simp
  right_inv x := by simp

@[simp] lemma toPair_apply (p : ℝ²) : toPair p = (p 0, p 1) := rfl

@[simp] lemma toPair_symm_zero (x : ℝ × ℝ) : toPair.symm x 0 = x.1 := by simp [toPair]

@[simp] lemma toPair_symm_one (x : ℝ × ℝ) : toPair.symm x 1 = x.2 := by simp [toPair]

lemma square_eq (x : ℝ) : Square x = toPair ⁻¹' (Ioo 0 x ×ˢ Ioo 0 x) := by
  ext p; simp [Square, and_assoc]

lemma unitSquare_eq : UnitSquare = toPair ⁻¹' (Ioo 0 1 ×ˢ Ioo 0 1) := square_eq 1

/-- If `e` reads as `F` in coordinates, images correspond. -/
lemma image_preimage_toPair {e : ℝ² → ℝ²} {F : ℝ × ℝ → ℝ × ℝ}
    (h : ∀ p, toPair (e p) = F (toPair p)) (S : Set (ℝ × ℝ)) :
    e '' (toPair ⁻¹' S) = toPair ⁻¹' (F '' S) := by
  ext q
  constructor
  · rintro ⟨p, hp, rfl⟩
    exact ⟨_, hp, (h p).symm⟩
  · rintro ⟨r, hr, hq⟩
    refine ⟨toPair.symm r, by simpa using hr, toPair.injective ?_⟩
    rw [h, Equiv.apply_symm_apply, hq]

/-! ## Frames -/

/-- The affine map `p ↦ b + p.1 • u + p.2 • v`, `u = (cos φ, sin φ)`, `v = ε • (-sin φ, cos φ)`. -/
noncomputable def frame (b : ℝ × ℝ) (φ ε : ℝ) (p : ℝ × ℝ) : ℝ × ℝ :=
  (b.1 + p.1 * Real.cos φ - ε * p.2 * Real.sin φ, b.2 + p.1 * Real.sin φ + ε * p.2 * Real.cos φ)

/-- The image of the centre `(1/2, 1/2)` under `frame b φ ε`. -/
noncomputable def frameCtr (b : ℝ × ℝ) (φ ε : ℝ) : ℝ × ℝ :=
  (b.1 + (Real.cos φ - ε * Real.sin φ) / 2, b.2 + (Real.sin φ + ε * Real.cos φ) / 2)

/-- A frame maps the open unit square `(0,1)²` onto the interior of a unit square. -/
lemma frame_image (b : ℝ × ℝ) (φ ε : ℝ) (hε : ε = 1 ∨ ε = -1) :
    frame b φ ε '' (Ioo 0 1 ×ˢ Ioo 0 1) = interior (unitSq (frameCtr b φ ε) φ) := by
  rw [interior_unitSq]
  have hcs := Real.sin_sq_add_cos_sq φ
  ext ⟨q1, q2⟩
  simp only [mem_image, mem_prod, mem_Ioo, mem_ofPred_eq, frame, frameCtr, abs_lt,
    Prod.ext_iff, Prod.exists]
  set C := Real.cos φ
  set S := Real.sin φ
  rcases hε with rfl | rfl
  · constructor
    · rintro ⟨p1, p2, ⟨⟨h1, h2⟩, h3, h4⟩, e1, e2⟩
      subst e1 e2
      have hX : (b.1 + p1 * C - 1 * p2 * S - (b.1 + (C - 1 * S) / 2)) * C +
          (b.2 + p1 * S + 1 * p2 * C - (b.2 + (S + 1 * C) / 2)) * S = p1 - 1/2 := by
        linear_combination (p1 - 1/2) * hcs
      have hY : -(b.1 + p1 * C - 1 * p2 * S - (b.1 + (C - 1 * S) / 2)) * S +
          (b.2 + p1 * S + 1 * p2 * C - (b.2 + (S + 1 * C) / 2)) * C = p2 - 1/2 := by
        linear_combination (p2 - 1/2) * hcs
      rw [hX, hY]
      exact ⟨⟨by linarith, by linarith⟩, by linarith, by linarith⟩
    · rintro ⟨⟨h1, h2⟩, h3, h4⟩
      refine ⟨(q1 - (b.1 + (C - 1 * S) / 2)) * C + (q2 - (b.2 + (S + 1 * C) / 2)) * S + 1/2,
        -(q1 - (b.1 + (C - 1 * S) / 2)) * S + (q2 - (b.2 + (S + 1 * C) / 2)) * C + 1/2,
        ⟨⟨?_, ?_⟩, ?_, ?_⟩, ?_, ?_⟩
      rotate_left 4
      · linear_combination (q1 - (b.1 + (C - 1 * S) / 2)) * hcs
      · linear_combination (q2 - (b.2 + (S + 1 * C) / 2)) * hcs
      all_goals linarith
  · constructor
    · rintro ⟨p1, p2, ⟨⟨h1, h2⟩, h3, h4⟩, e1, e2⟩
      subst e1 e2
      have hX : (b.1 + p1 * C - -1 * p2 * S - (b.1 + (C - -1 * S) / 2)) * C +
          (b.2 + p1 * S + -1 * p2 * C - (b.2 + (S + -1 * C) / 2)) * S = p1 - 1/2 := by
        linear_combination (p1 - 1/2) * hcs
      have hY : -(b.1 + p1 * C - -1 * p2 * S - (b.1 + (C - -1 * S) / 2)) * S +
          (b.2 + p1 * S + -1 * p2 * C - (b.2 + (S + -1 * C) / 2)) * C = -(p2 - 1/2) := by
        linear_combination (-(p2 - 1/2)) * hcs
      rw [hX, hY]
      exact ⟨⟨by linarith, by linarith⟩, by linarith, by linarith⟩
    · rintro ⟨⟨h1, h2⟩, h3, h4⟩
      refine ⟨(q1 - (b.1 + (C - -1 * S) / 2)) * C + (q2 - (b.2 + (S + -1 * C) / 2)) * S + 1/2,
        -(-(q1 - (b.1 + (C - -1 * S) / 2)) * S +
          (q2 - (b.2 + (S + -1 * C) / 2)) * C) + 1/2, ⟨⟨?_, ?_⟩, ?_, ?_⟩, ?_, ?_⟩
      rotate_left 4
      · linear_combination (q1 - (b.1 + (C - -1 * S) / 2)) * hcs
      · linear_combination (q2 - (b.2 + (S + -1 * C) / 2)) * hcs
      all_goals linarith

/-! ## Placing a square by a rigid motion -/

/-- The corner `b` with `frameCtr b θ 1 = c`. -/
noncomputable def corner (c : ℝ × ℝ) (θ : ℝ) : ℝ × ℝ :=
  (c.1 - (Real.cos θ - Real.sin θ) / 2, c.2 - (Real.sin θ + Real.cos θ) / 2)

lemma frameCtr_corner (c : ℝ × ℝ) (θ : ℝ) : frameCtr (corner c θ) θ 1 = c := by
  ext <;> simp [frameCtr, corner]

/-- The rigid motion of `ℝ²` taking `(0,1)²` onto the open square with centre `c`, angle `θ`. -/
noncomputable def motion (c : ℝ × ℝ) (θ : ℝ) : ℝ² ≃ᵢ ℝ² where
  toFun p := toPair.symm (frame (corner c θ) θ 1 (toPair p))
  invFun r := toPair.symm (rot (-θ) (toPair r - corner c θ))
  left_inv p := by
    have hcs := Real.sin_sq_add_cos_sq θ
    apply toPair.injective
    simp only [Equiv.apply_symm_apply, toPair_apply, frame, rot, Real.cos_neg, Real.sin_neg]
    ext <;> simp only [Prod.fst_sub, Prod.snd_sub]
    · linear_combination (p 0) * hcs
    · linear_combination (p 1) * hcs
  right_inv r := by
    have hcs := Real.sin_sq_add_cos_sq θ
    apply toPair.injective
    simp only [Equiv.apply_symm_apply, toPair_apply, frame, rot, Real.cos_neg, Real.sin_neg]
    ext <;> simp only [Prod.fst_sub, Prod.snd_sub]
    · linear_combination (r 0 - (corner c θ).1) * hcs
    · linear_combination (r 1 - (corner c θ).2) * hcs
  isometry_toFun := by
    refine Isometry.of_dist_eq fun p q => ?_
    have hcs := Real.sin_sq_add_cos_sq θ
    rw [EuclideanSpace.dist_eq, EuclideanSpace.dist_eq]
    congr 1
    simp only [Fin.sum_univ_two, Real.dist_eq, sq_abs, toPair_symm_zero, toPair_symm_one,
      toPair_apply, frame]
    linear_combination ((p 0 - q 0) ^ 2 + (p 1 - q 1) ^ 2) * hcs

lemma toPair_motion (c : ℝ × ℝ) (θ : ℝ) (p : ℝ²) :
    toPair (motion c θ p) = frame (corner c θ) θ 1 (toPair p) :=
  Equiv.apply_symm_apply _ _

lemma motion_image (c : ℝ × ℝ) (θ : ℝ) :
    motion c θ '' UnitSquare = toPair ⁻¹' interior (unitSq c θ) := by
  rw [unitSquare_eq, image_preimage_toPair (toPair_motion c θ),
    frame_image _ _ _ (Or.inl rfl), frameCtr_corner]

/-! ## Every isometry of the plane is a frame -/

lemma norm_sq_eq (x : ℝ²) : ‖x‖ ^ 2 = x 0 ^ 2 + x 1 ^ 2 := by
  rw [EuclideanSpace.real_norm_sq_eq, Fin.sum_univ_two]

/-- A unit vector of `ℝ × ℝ` is `(cos φ, sin φ)`. -/
lemma exists_cos_sin {a b : ℝ} (h : a ^ 2 + b ^ 2 = 1) :
    ∃ φ, Real.cos φ = a ∧ Real.sin φ = b := by
  set z : ℂ := ⟨a, b⟩
  have hz : ‖z‖ = 1 := by
    rw [Complex.norm_def, Complex.normSq_apply]
    simp only [z]
    rw [← sq, ← sq, h, Real.sqrt_one]
  have hz0 : z ≠ 0 := by intro h0; rw [h0, norm_zero] at hz; exact zero_ne_one hz
  exact ⟨Complex.arg z, by rw [Complex.cos_arg hz0, hz, div_one],
    by rw [Complex.sin_arg, hz, div_one]⟩

/-- **Isometries of the plane** (Mazur–Ulam + orthonormal frames): in coordinates every
`e : ℝ² ≃ᵢ ℝ²` is `frame b φ ε` with `ε = ±1`. -/
lemma exists_frame (e : ℝ² ≃ᵢ ℝ²) :
    ∃ (b : ℝ × ℝ) (φ ε : ℝ), (ε = 1 ∨ ε = -1) ∧ ∀ p, toPair (e p) = frame b φ ε (toPair p) := by
  set L := e.toRealLinearIsometryEquiv
  set s0 : ℝ² := EuclideanSpace.single 0 1
  set s1 : ℝ² := EuclideanSpace.single 1 1
  have hL : ∀ p, e p = p 0 • L s0 + p 1 • L s1 + e 0 := by
    intro p
    have hp : p 0 • s0 + p 1 • s1 = p := by ext i; fin_cases i <;> simp [s0, s1]
    calc e p = L p + e 0 := by simp [L]
      _ = L (p 0 • s0 + p 1 • s1) + e 0 := by rw [hp]
      _ = _ := by simp only [map_add, map_smul]
  set u := L s0
  set v := L s1
  have hu : u 0 ^ 2 + u 1 ^ 2 = 1 := by
    rw [← norm_sq_eq, L.norm_map, norm_sq_eq]; simp [s0]
  have hv : v 0 ^ 2 + v 1 ^ 2 = 1 := by
    rw [← norm_sq_eq, L.norm_map, norm_sq_eq]; simp [s1]
  have huv : (u 0 - v 0) ^ 2 + (u 1 - v 1) ^ 2 = 2 := by
    have h := norm_sq_eq (u - v)
    rw [show u - v = L (s0 - s1) from (map_sub L s0 s1).symm, L.norm_map, norm_sq_eq] at h
    simp only [PiLp.sub_apply, map_sub] at h
    simp [s0, s1] at h
    norm_num at h
    linarith
  have hdot : u 0 * v 0 + u 1 * v 1 = 0 := by linear_combination (hu + hv - huv) / 2
  set ε := u 0 * v 1 - u 1 * v 0
  have hε : ε * ε = 1 := by
    simp only [ε]
    linear_combination (v 0 ^ 2 + v 1 ^ 2) * hu + hv - (u 0 * v 0 + u 1 * v 1) * hdot
  have hv0 : v 0 = -ε * u 1 := by
    simp only [ε]; linear_combination (-v 0) * hu + u 0 * hdot
  have hv1 : v 1 = ε * u 0 := by
    simp only [ε]; linear_combination (-v 1) * hu + u 1 * hdot
  obtain ⟨φ, hc, hs⟩ := exists_cos_sin hu
  refine ⟨toPair (e 0), φ, ε, mul_self_eq_one_iff.mp hε, fun p => ?_⟩
  rw [hL p]
  simp only [toPair_apply, frame, hc, hs, PiLp.add_apply, PiLp.smul_apply, smul_eq_mul]
  rw [hv0, hv1]
  ext <;> simp only <;> ring

/-! ## Open squares in the open box, closed squares in the closed box -/

lemma closure_interior_unitSq (c : ℝ × ℝ) (θ : ℝ) :
    closure (interior (unitSq c θ)) = unitSq c θ := by
  have h : interior (unitSq c θ) = place c θ '' (Ioo (-1/2) (1/2) ×ˢ Ioo (-1/2) (1/2)) := by
    rw [unitSq, ← interior_Icc, ← interior_prod_eq]
    exact ((place c θ).image_interior _).symm
  rw [h, ← Homeomorph.image_closure, closure_prod_eq, closure_Ioo (by norm_num)]
  rfl

lemma interior_container (x : ℝ) : interior (container x) = Ioo 0 x ×ˢ Ioo 0 x := by
  rw [container, interior_prod_eq, interior_Icc]

/-- **Bridge to formal-conjectures**: `n` unit squares pack in `[0, x]²` in the sense of
`Spec.lean` iff they do in the sense of formal-conjectures' `Packing` (open squares placed by
isometries of `EuclideanSpace ℝ (Fin 2)`, inside the open square `(0, x)²`). -/
theorem packs_iff_nonempty_packing (n : ℕ) (x : ℝ) :
    Packs n x ↔ Nonempty (Packing n UnitSquare (Square x)) := by
  constructor
  · rintro ⟨c, θ, hin, hdisj⟩
    refine ⟨⟨fun i => motion (c i) (θ i), fun i j hij => ?_, fun i => ?_⟩⟩
    · simp only [motion_image]
      exact (hdisj hij).preimage _
    · rw [motion_image, square_eq, ← interior_container]
      exact preimage_mono (interior_mono (hin i))
  · rintro ⟨P⟩
    choose b φ ε hε hF using fun i => exists_frame (P.embeddings i)
    have himg : ∀ i, P.embeddings i '' UnitSquare =
        toPair ⁻¹' interior (unitSq (frameCtr (b i) (φ i) (ε i)) (φ i)) := fun i => by
      have h := image_preimage_toPair (hF i) (Ioo 0 1 ×ˢ Ioo 0 1)
      rwa [← unitSquare_eq, frame_image _ _ _ (hε i)] at h
    refine ⟨fun i => frameCtr (b i) (φ i) (ε i), φ, fun i => ?_, fun i j hij => ?_⟩
    · have h := P.inside i
      rw [himg, square_eq, toPair.surjective.preimage_subset_preimage_iff] at h
      rw [← closure_interior_unitSq]
      exact closure_minimal (h.trans (prod_mono Ioo_subset_Icc_self Ioo_subset_Icc_self))
        (isClosed_Icc.prod isClosed_Icc)
    · have h := P.disjoint hij
      simp only [himg] at h
      exact (disjoint_preimage_iff toPair.surjective).mp h

/-- The same set of sides, so every canonical shape (`IsLeast`, lower, upper) transfers. -/
theorem setOf_packs_eq (n : ℕ) :
    {s | Packs n s} = {x : ℝ | Nonempty (Packing n UnitSquare (Square x))} :=
  Set.ext fun x => packs_iff_nonempty_packing n x

end UnitSquarePacking
