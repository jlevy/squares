import ElevenSquare.Foundations

/-!
Statement audit for T-060, written in jlevy/squares (lane N11, 2026-10-06), not part of
the source. It elaborates against the source's own definitions and checks, by `Iff.rfl`
or `rfl` where it can, that the formal statement says what the register claims:

1. `ElevenSquare.Optimality` is `IsLeast {S | Packable 11 S} T`, i.e. `s(11) = T` with
   the minimum attained.
2. `T` is `(6u+4)/(1+2u-u^2)` and `u` is the unique root in `[9/25, 37/100]` of the
   register's degree-8 polynomial, written out here term by term.
3. The square, its interior, the container and the packing are the closed unit square
   with centre and an arbitrary real unit axis, its open interior, `[0,S]^2`, and
   containment with pairwise disjoint open interiors.
4. Two controls show the definitions are not vacuous: an axis-aligned square is the
   usual `[c-1/2, c+1/2]^2`, and two unit squares do not fit in a side-1 square.
5. Root-level declarations named `T` and `Packable` do not change what the names mean
   inside `namespace ElevenSquare`, where the public theorem is stated.
-/

open ElevenSquare

-- 1. The global statement.
#print ElevenSquare.Optimality
example : ElevenSquare.Optimality ↔
    (Packable 11 T ∧ ∀ S : ℝ, Packable 11 S → T ≤ S) := Iff.rfl
example : ElevenSquare.Optimality ↔ IsLeast {S : ℝ | Packable 11 S} T := Iff.rfl

-- 2. The endpoint.
#print ElevenSquare.T
#print ElevenSquare.u
#print ElevenSquare.endpointPolynomial
example : T = (6 * u + 4) / (1 + 2 * u - u ^ 2) := rfl
example (x : ℝ) : endpointPolynomial x =
    5 * x ^ 8 - 10 * x ^ 7 - 2 * x ^ 6 + 14 * x ^ 5 + 12 * x ^ 4 - 6 * x ^ 3 + 2 * x ^ 2
      + 2 * x - 1 := rfl
example : u ∈ Set.Ioo (9 / 25 : ℝ) (37 / 100) ∧ endpointPolynomial u = 0 :=
  ⟨u_broad_bounds, u_polynomial⟩
example : ∀ x ∈ Set.Icc (9 / 25 : ℝ) (37 / 100), endpointPolynomial x = 0 → x = u :=
  fun _ hx hp => u_unique hx hp

-- 3. The objects.
#print ElevenSquare.Point
#print ElevenSquare.dot
#print ElevenSquare.normSq
#print ElevenSquare.perp
#print ElevenSquare.UnitSquare
#print ElevenSquare.localX
#print ElevenSquare.localY
#print ElevenSquare.ClosedSquare
#print ElevenSquare.OpenSquare
#print ElevenSquare.InContainer
#print ElevenSquare.Packing
#print ElevenSquare.Packable
example (S : ℝ) : Packable 11 S ↔ Nonempty (Packing 11 S) := Iff.rfl

-- 4a. Control: the axis-aligned unit square at centre c is [c-1/2, c+1/2]^2.
def axisSquare (c : Point) : UnitSquare := ⟨c, (1, 0), by norm_num [normSq, dot]⟩

example (c p : Point) : ClosedSquare (axisSquare c) p ↔
    |p.1 - c.1| ≤ 1 / 2 ∧ |p.2 - c.2| ≤ 1 / 2 := by
  simp [ClosedSquare, axisSquare, localX, localY, dot, perp]

-- 4b. Control: two unit squares do not pack in a square of side 1, so containment and
-- disjoint interiors constrain a packing.
example : ¬ Packable 2 1 := by
  rintro ⟨P⟩
  have h01 := P.center_separation 0 1 (by decide)
  obtain ⟨a1, a2, a3, a4⟩ := P.center_bounds 0
  obtain ⟨b1, b2, b3, b4⟩ := P.center_bounds 1
  have hx : (P.squares 0).center.1 = (P.squares 1).center.1 := by linarith
  have hy : (P.squares 0).center.2 = (P.squares 1).center.2 := by linarith
  have hz : normSq ((P.squares 0).center - (P.squares 1).center) = 0 := by
    simp [normSq, dot, hx, hy]
  linarith

-- The axioms of what this file and the statement closure prove.
#print axioms ElevenSquare.construction_packable
#print axioms ElevenSquare.optimality_of_lower_bound
#print axioms ElevenSquare.u_unique
#print axioms ElevenSquare.T_lt_U
#print axioms ElevenSquare.improvement_within_cover
#print axioms ElevenSquare.packing_has_canonical_mask

-- 5. Name resolution: root-level declarations named `T` and `Packable` do not capture the
-- names inside `namespace ElevenSquare`, where `Optimality.lean` states the theorem.
def T : Nat := 7
def Packable (_n _S : Nat) : Prop := False

namespace ElevenSquare
example : T = (6 * u + 4) / (1 + 2 * u - u ^ 2) := rfl
example : Optimality ↔ (Packable 11 T ∧ ∀ S : ℝ, Packable 11 S → T ≤ S) := Iff.rfl
end ElevenSquare
