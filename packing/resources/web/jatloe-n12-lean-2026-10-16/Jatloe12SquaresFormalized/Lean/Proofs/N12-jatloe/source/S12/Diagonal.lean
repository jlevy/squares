import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Push
import Mathlib.Tactic.Ring

/-!
# Opposite-central-marker exclusion: a checked s(12) pilot

This is the local opposite-diagonal rule used by the initial classification,
not a formalization of the complete packing proof. It strengthens the retained
rule: the forbidden pattern is impossible for an open square of any size.

The source includes a geometric model, both diagonal exclusions, a Boolean
checker for the four central-marker ownership bits, a proof of its soundness,
and kernel-checked acceptance of the two forbidden input patterns.
-/
namespace S12Pilot

set_option maxHeartbeats 400000

/-- Membership in two open intervals of the same width. -/
def InBands (loU loV a u v : ℝ) : Prop :=
  loU < u ∧ u < loU + a ∧ loV < v ∧ v < loV + a

/-- All 16 pairs of excluding faces are impossible for this diagonal. -/
theorem diagonal_in_bands (loU loV a X Y : ℝ)
    (hA : InBands loU loV a 0 0)
    (hD : InBands loU loV a (X + Y) (X - Y)) :
    InBands loU loV a X (-Y) ∨ InBands loU loV a Y X := by
  rcases hA with ⟨ha0, ha1, ha2, ha3⟩
  rcases hD with ⟨hd0, hd1, hd2, hd3⟩
  by_contra h
  simp only [InBands, not_or, not_and_or, not_lt] at h
  rcases h with ⟨hB, hC⟩
  rcases hB with hb | hb | hb | hb <;>
    rcases hC with hc | hc | hc | hc <;> linarith

/-- The other diagonal, with all excluding faces checked explicitly. -/
theorem other_diagonal_in_bands (loU loV a X Y : ℝ)
    (hB : InBands loU loV a X (-Y))
    (hC : InBands loU loV a Y X) :
    InBands loU loV a 0 0 ∨ InBands loU loV a (X + Y) (X - Y) := by
  rcases hB with ⟨hb0, hb1, hb2, hb3⟩
  rcases hC with ⟨hc0, hc1, hc2, hc3⟩
  by_contra h
  simp only [InBands, not_or, not_and_or, not_lt] at h
  rcases h with ⟨hA, hD⟩
  rcases hA with ha | ha | ha | ha <;>
    rcases hD with hd | hd | hd | hd <;> linarith

/-- An arbitrary rotated and translated open square in unit-normal coordinates. -/
structure OpenSquare where
  c : ℝ
  s : ℝ
  loU : ℝ
  loV : ℝ
  side : ℝ
  unit_normal : c ^ 2 + s ^ 2 = 1
  side_pos : 0 < side

def OpenSquare.Inside (q : OpenSquare) (x y : ℝ) : Prop :=
  InBands q.loU q.loV q.side (q.c * x + q.s * y) (-q.s * x + q.c * y)

/-- The coordinate transformation preserves squared Euclidean lengths. -/
theorem rotation_preserves_squared_length (q : OpenSquare) (u v : ℝ) :
    (q.c * u - q.s * v) ^ 2 + (q.s * u + q.c * v) ^ 2 = u ^ 2 + v ^ 2 := by
  calc
    _ = (q.c ^ 2 + q.s ^ 2) * (u ^ 2 + v ^ 2) := by ring
    _ = u ^ 2 + v ^ 2 := by rw [q.unit_normal, one_mul]

/-- The strip model is exactly a rotation of a Cartesian open square.
    This explicitly connects the computational coordinates to square geometry. -/
theorem inside_iff_rotated_box (q : OpenSquare) (x y : ℝ) :
    q.Inside x y ↔ ∃ u v : ℝ, InBands q.loU q.loV q.side u v ∧
      x = q.c * u - q.s * v ∧ y = q.s * u + q.c * v := by
  constructor
  · intro h
    refine ⟨q.c * x + q.s * y, -q.s * x + q.c * y, h, ?_, ?_⟩
    · calc
        x = (q.c ^ 2 + q.s ^ 2) * x := by rw [q.unit_normal, one_mul]
        _ = q.c * (q.c * x + q.s * y) - q.s * (-q.s * x + q.c * y) := by ring
    · calc
        y = (q.c ^ 2 + q.s ^ 2) * y := by rw [q.unit_normal, one_mul]
        _ = q.s * (q.c * x + q.s * y) + q.c * (-q.s * x + q.c * y) := by ring
  · rintro ⟨u, v, h, rfl, rfl⟩
    have hu : q.c * (q.c * u - q.s * v) + q.s * (q.s * u + q.c * v) = u := by
      calc
        _ = (q.c ^ 2 + q.s ^ 2) * u := by ring
        _ = u := by rw [q.unit_normal, one_mul]
    have hv : -q.s * (q.c * u - q.s * v) + q.c * (q.s * u + q.c * v) = v := by
      calc
        _ = (q.c ^ 2 + q.s ^ 2) * v := by ring
        _ = v := by rw [q.unit_normal, one_mul]
    simpa only [OpenSquare.Inside, hu, hv] using h

/-- Translate the coordinate origin, preserving the square and its orientation. -/
def OpenSquare.translated (q : OpenSquare) (x y : ℝ) : OpenSquare where
  c := q.c
  s := q.s
  loU := q.loU - (q.c * x + q.s * y)
  loV := q.loV - (-q.s * x + q.c * y)
  side := q.side
  unit_normal := q.unit_normal
  side_pos := q.side_pos

theorem inside_translated_iff (q : OpenSquare) (x y u v : ℝ) :
    (q.translated x y).Inside u v ↔ q.Inside (x + u) (y + v) := by
  dsimp [OpenSquare.Inside, OpenSquare.translated, InBands]
  constructor <;> rintro ⟨h0, h1, h2, h3⟩ <;>
    refine ⟨?_, ?_, ?_, ?_⟩ <;> linarith

/-- No bound on the side length or on the test-square size is needed. -/
theorem opposite_diagonal_origin (q : OpenSquare) (d : ℝ)
    (hA : q.Inside 0 0) (hD : q.Inside d d) :
    q.Inside d 0 ∨ q.Inside 0 d := by
  have hA' : InBands q.loU q.loV q.side 0 0 := by
    simpa [OpenSquare.Inside] using hA
  have hD' : InBands q.loU q.loV q.side (d * q.c + d * q.s) (d * q.c - d * q.s) := by
    simpa [OpenSquare.Inside, mul_comm, sub_eq_add_neg, add_comm] using hD
  have h := diagonal_in_bands q.loU q.loV q.side (d * q.c) (d * q.s) hA' hD'
  simpa [OpenSquare.Inside, mul_comm] using h

theorem other_diagonal_origin (q : OpenSquare) (d : ℝ)
    (hB : q.Inside d 0) (hC : q.Inside 0 d) :
    q.Inside 0 0 ∨ q.Inside d d := by
  have hB' : InBands q.loU q.loV q.side (d * q.c) (-(d * q.s)) := by
    simpa [OpenSquare.Inside, mul_comm] using hB
  have hC' : InBands q.loU q.loV q.side (d * q.s) (d * q.c) := by
    simpa [OpenSquare.Inside, mul_comm] using hC
  have h := other_diagonal_in_bands q.loU q.loV q.side (d * q.c) (d * q.s) hB' hC'
  simpa [OpenSquare.Inside, mul_comm, sub_eq_add_neg, add_comm] using h

theorem opposite_diagonal (q : OpenSquare) (x y d : ℝ)
    (hA : q.Inside x y) (hD : q.Inside (x + d) (y + d)) :
    q.Inside (x + d) y ∨ q.Inside x (y + d) := by
  have hA' : (q.translated x y).Inside 0 0 := by
    rw [inside_translated_iff]; simpa using hA
  have hD' : (q.translated x y).Inside d d := by
    rw [inside_translated_iff]; exact hD
  have h := opposite_diagonal_origin (q.translated x y) d hA' hD'
  simpa only [inside_translated_iff, add_zero] using h

theorem other_diagonal (q : OpenSquare) (x y d : ℝ)
    (hB : q.Inside (x + d) y) (hC : q.Inside x (y + d)) :
    q.Inside x y ∨ q.Inside (x + d) (y + d) := by
  have hB' : (q.translated x y).Inside d 0 := by
    rw [inside_translated_iff]; simpa using hB
  have hC' : (q.translated x y).Inside 0 d := by
    rw [inside_translated_iff]; simpa using hC
  have h := other_diagonal_origin (q.translated x y) d hB' hC'
  simpa only [inside_translated_iff, add_zero] using h

/-- Markers 8 and 10 force marker 9 or marker 11 into the same square. -/
theorem central_marker_exclusion (q : OpenSquare)
    (h8 : q.Inside (33 / 20) (33 / 20))
    (h10 : q.Inside (47 / 20) (47 / 20)) :
    q.Inside (47 / 20) (33 / 20) ∨ q.Inside (33 / 20) (47 / 20) := by
  have hD : q.Inside (33 / 20 + 7 / 10) (33 / 20 + 7 / 10) := by
    norm_num; exact h10
  have h := opposite_diagonal q (33 / 20) (33 / 20) (7 / 10) h8 hD
  norm_num at h
  exact h

/-- Markers 9 and 11 force marker 8 or marker 10 into the same square. -/
theorem central_marker_other_exclusion (q : OpenSquare)
    (h9 : q.Inside (47 / 20) (33 / 20))
    (h11 : q.Inside (33 / 20) (47 / 20)) :
    q.Inside (33 / 20) (33 / 20) ∨ q.Inside (47 / 20) (47 / 20) := by
  have hB : q.Inside (33 / 20 + 7 / 10) (33 / 20) := by norm_num; exact h9
  have hC : q.Inside (33 / 20) (33 / 20 + 7 / 10) := by norm_num; exact h11
  have h := other_diagonal q (33 / 20) (33 / 20) (7 / 10) hB hC
  norm_num at h
  exact h

/-- Four bits encode actual strict interior membership, not optional ownership. -/
structure MarkerPattern where
  m8 : Bool
  m9 : Bool
  m10 : Bool
  m11 : Bool
  deriving DecidableEq, Repr

/-- Executable local exclusion checker. `true` means the pattern is impossible. -/
def rejects (p : MarkerPattern) : Bool :=
  (p.m8 && p.m10 && !p.m9 && !p.m11) ||
  (p.m9 && p.m11 && !p.m8 && !p.m10)

/-- The exact connection between the four input bits and geometry. -/
def Realizes (q : OpenSquare) (p : MarkerPattern) : Prop :=
  (q.Inside (33 / 20) (33 / 20) ↔ p.m8 = true) ∧
  (q.Inside (47 / 20) (33 / 20) ↔ p.m9 = true) ∧
  (q.Inside (47 / 20) (47 / 20) ↔ p.m10 = true) ∧
  (q.Inside (33 / 20) (47 / 20) ↔ p.m11 = true)

/-- Soundness for EVERY input pattern and EVERY geometrically represented square.
    No claim that an accepted/rejected bit is supplied truthfully is assumed:
    the required connection to geometry is stated explicitly as `Realizes`. -/
theorem rejects_sound (p : MarkerPattern) (h : rejects p = true) :
    ¬ ∃ q : OpenSquare, Realizes q p := by
  rintro ⟨q, hr⟩
  have hd := central_marker_exclusion q
  have he := central_marker_other_exclusion q
  rcases p with ⟨b8, b9, b10, b11⟩
  cases b8 <;> cases b9 <;> cases b10 <;> cases b11 <;>
    simp_all [rejects, Realizes]

/-- Concrete certificate acceptance is proved by kernel reduction. -/
theorem first_pattern_rejected : rejects ⟨true, false, true, false⟩ = true := by decide

theorem second_pattern_rejected : rejects ⟨false, true, false, true⟩ = true := by decide

/-- Complete local conclusion: combine checker soundness with concrete acceptance. -/
theorem first_pattern_impossible :
    ¬ ∃ q : OpenSquare, Realizes q ⟨true, false, true, false⟩ :=
  rejects_sound _ first_pattern_rejected

theorem second_pattern_impossible :
    ¬ ∃ q : OpenSquare, Realizes q ⟨false, true, false, true⟩ :=
  rejects_sound _ second_pattern_rejected

#print axioms inside_iff_rotated_box
#print axioms rejects_sound
#print axioms first_pattern_rejected
#print axioms first_pattern_impossible
#print axioms second_pattern_impossible

end S12Pilot
