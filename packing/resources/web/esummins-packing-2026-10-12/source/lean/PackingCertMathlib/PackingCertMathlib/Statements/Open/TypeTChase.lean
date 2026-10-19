import PackingCertMathlib.Statements.Open.CornerChase
import PackingCertMathlib.Statements.Open.PocketWaste

/-!
# -- OPEN: the corner chase for TYPE-T corners (both meeters tilted) -- A249

`docs/proofs/type_t_chase.md`.  A248's chase closed the type-F corner (a flat meeter and its
poker) on the window by Lemma TWO-POKERS (`s* = 3.9342 > ŝ`).  This file records the type-T
corner: the wall-side meeter `B` touching the wall `u = 0` with lowest vertex at height `δ_B` and
tilt `θ_B`, the floor-side meeter `A` touching the floor with leftmost vertex at abscissa `δ_A` and
tilt `θ_A` (`wallSquare`, `floorSquare`; the mirror `u ↔ v` is `(θ_B, δ_B) ↔ (90° − θ_A, δ_A)`).

**T-CELLS** [T-prose] (`type_t_chase.md` §1): `B` meets the corner box iff `δ_B < 1`, the wall slot
`(0,1) × (1,2)` iff `δ_B + sin θ_B + cos θ_B > 1` (always, in a doubly-met corner), and the floor
slot `(1,2) × (0,1)` iff its lower edge `V → R` crosses `u = 1` below height `1`:
`δ_B + (1 − sin θ_B) tan θ_B < 1`.  Mirror for `A`.  So a type-T corner with both meeters touching
supplies each of its own slots once by itself (SLOT-MET is automatic) and its second slot
incidences come from the tips (T2 / T3, never both: NOT-SELF-SUFFICIENT).

**T-TIP** [T-prose] (§1.3): if `A` meets the wall slot, its open chord at height `1`,
`(u_A(1), u_A(1) + λ_A)` with `u_A(1) = δ_A + (1 − cos θ_A) cot θ_A` and
`λ_A = (sin θ_A + cos θ_A − 1)/(sin θ_A cos θ_A)`, is disjoint from `B`'s open chord at height `1`
(`(b₁, u_B(1))`, `u_B(1) = sin θ_B + (1 − δ_B) cot θ_B`): `A`'s tip rises into the wall slot to the
RIGHT of `B`'s cap (so `B` misses the floor slot) or under `B`'s bottom edge.  Proof: a point of
`A` in the slot above `B` would put the segment to `A`'s floor vertex through `int B`; the two
open chords at the interior height `1` are interior to their squares.

**TWO-TILTED fails on the window** [T-computed] (§2): unlike the type-F poker pair, two type-T
corners on one wall with the wall slots served by each other's wall meeters exist at every side of
the window (the wall problem's sup SAT margin is `+0.078` at `3.82`, `+0.074` at `ŝ`), and so does
the ALL-ADJ TYPE-T RING -- eight tilted wall-touching meeters, every one reaching the far slot of
its wall, all twelve border cells doubly met by the eight alone (`two_tilted_ring_exists`: an exact
rational witness at `ŝ`, `test249.test_ring_exact`; it is a pinwheel of eight squares at tilt
`14.6°`, A239's window ring family in type-T form).  Its POCKET holds ONE square only (A237's
PIERCE(1) certificate at the centre, residual `0`): `8 + 1 = 9 < 11`.  So on the window the type-T
chase does NOT reach a wall inequality; the residue is the room for the three free squares
(`type_t_chase_closes` [C] = POCKET(11) under the 12-stuck / FAMILY-STUCK hypothesis), exactly
A246 / A248's residue with the type-T ring now known to exist.

**Status (2026-09-17).**  `t_cells`, `t_cells_floor`, `t_tip`: axioms [T-prose];
`two_tilted_ring_exists`: axiom [T-computed] (exact witness + certificate);
`no_two_tilted_bound`: theorem (the analogue of `two_pokers_window` is FALSE at `ŝ`);
`type_t_chase_closes`: axiom [C]; `optimal_psiMin_not_twelve_stuck_typeT`: theorem.
-/

namespace PackingCert.S11.OpenLemmas

open Set

/-- The wall-touching tilted square: wall vertex `L = (0, δ + cos θ)`, edge `L → V = (sin θ, −cos θ)`
(its lowest vertex `V = (sin θ, δ)`), edge `L → T = (cos θ, sin θ)`. -/
noncomputable def wallSquare (θ δ : ℝ) : Set RP :=
  sqSet (0, δ + Real.cos θ) (Real.sin θ, -Real.cos θ)

/-- The floor-touching tilted square: lowest vertex `V = (δ + sin θ, 0)`, edge `V → R = (cos θ, sin θ)`,
edge `V → W = (−sin θ, cos θ)` (its leftmost vertex `W = (δ, cos θ)`). -/
noncomputable def floorSquare (θ δ : ℝ) : Set RP :=
  sqSet (δ + Real.sin θ, 0) (Real.cos θ, Real.sin θ)

/-- **T-CELLS** [T-prose], the wall square (`type_t_chase.md` §1.1, any `n`, any side). -/
axiom t_cells (θ δ : ℝ) (hθ : 0 < θ ∧ θ < Real.pi / 2) (hδ : 0 ≤ δ) :
    (MeetsCell (wallSquare θ δ) 0 1 0 1 ↔ δ < 1) ∧
    (MeetsCell (wallSquare θ δ) 0 1 1 2 ↔ 1 < δ + Real.sin θ + Real.cos θ) ∧
    (MeetsCell (wallSquare θ δ) 1 2 0 1 ↔ δ + (1 - Real.sin θ) * Real.tan θ < 1)

/-- **T-CELLS**, the floor square (the mirror `u ↔ v`, `θ ↦ 90° − θ`). -/
axiom t_cells_floor (θ δ : ℝ) (hθ : 0 < θ ∧ θ < Real.pi / 2) (hδ : 0 ≤ δ) :
    (MeetsCell (floorSquare θ δ) 0 1 0 1 ↔ δ < 1) ∧
    (MeetsCell (floorSquare θ δ) 1 2 0 1 ↔ 1 < δ + Real.sin θ + Real.cos θ) ∧
    (MeetsCell (floorSquare θ δ) 0 1 1 2 ↔ δ + (1 - Real.cos θ) / Real.tan θ < 1)

/-- The left end of `B`'s chord at height `1`: on the edge `L → V` when the wall vertex is above `1`,
on the edge `L → T` otherwise. -/
noncomputable def chordLeftB (θ δ : ℝ) : ℝ :=
  if 1 ≤ δ + Real.cos θ then (δ + Real.cos θ - 1) * Real.tan θ else (1 - δ - Real.cos θ) / Real.tan θ

/-- **T-TIP** [T-prose] (`type_t_chase.md` §1.3): the floor meeter's tip enters the wall slot only
right of the wall meeter's cap or under its bottom edge -- the two open chords at height `1` are
disjoint. -/
axiom t_tip (θA δA θB δB : ℝ) (hA : 0 < θA ∧ θA < Real.pi / 2) (hB : 0 < θB ∧ θB < Real.pi / 2)
    (hδA : 0 ≤ δA) (hδB : 0 ≤ δB ∧ δB < 1)
    (hdisj : Disjoint (interior (floorSquare θA δA)) (interior (wallSquare θB δB)))
    (hc01 : MeetsCell (floorSquare θA δA) 0 1 1 2) :
    Real.sin θB + (1 - δB) / Real.tan θB ≤ δA + (1 - Real.cos θA) / Real.tan θA ∨
    δA + (1 - Real.cos θA) / Real.tan θA +
      (Real.sin θA + Real.cos θA - 1) / (Real.sin θA * Real.cos θA) ≤ chordLeftB θB δB

/-- The twelve border cells of `[0, m]²` at unit scale (four corner boxes, eight wall slots), as
`(x0, x1, y0, y1)`. -/
def borderCells (m : ℝ) : List (ℝ × ℝ × ℝ × ℝ) :=
  [(0, 1, 0, 1), (m - 1, m, 0, 1), (m - 1, m, m - 1, m), (0, 1, m - 1, m),
   (0, 1, 1, 2), (1, 2, 0, 1), (m - 1, m, 1, 2), (m - 2, m - 1, 0, 1),
   (m - 1, m, m - 2, m - 1), (m - 2, m - 1, m - 1, m), (0, 1, m - 2, m - 1), (1, 2, m - 1, m)]

/-- Every border cell is met by two distinct squares of the family. -/
def TwelveMet (m : ℝ) {k : ℕ} (Q : Fin k → Set RP) : Prop :=
  ∀ c ∈ borderCells m, ∃ i j : Fin k, i ≠ j ∧
    MeetsCell (Q i) c.1 c.2.1 c.2.2.1 c.2.2.2 ∧ MeetsCell (Q j) c.1 c.2.1 c.2.2.1 c.2.2.2

/-- An axis-parallel unit square. -/
def IsFlat (Q : Set RP) : Prop := ∃ a b : ℝ, Q = Icc a (a + 1) ×ˢ Icc b (b + 1)

/-- The window's upper end, Trump's side. -/
noncomputable def sHat : ℝ := 3.877084

/-- **THE TYPE-T RING EXISTS** [T-computed] (`type_t_chase.md` §2.3): eight pairwise
interior-disjoint tilted unit squares in `[0, ŝ]²` meeting all twelve border cells twice (every
meeter reaches the far slot of its wall), whose pocket holds no two further unit squares (PIERCE(1)
residual `0` at the centre, A237's certificate; exact rational witness `test249.test_ring_exact`). -/
axiom two_tilted_ring_exists :
    ∃ Q : Fin 8 → Set RP, IsPacking 8 sHat Q ∧ TwelveMet sHat Q ∧ (∀ i, ¬ IsFlat (Q i)) ∧
      PocketCapacityLT sHat Q Finset.univ 2

/-- The analogue of `two_pokers_window` for type T would say: no 8-square tilted 12-stuck
skeleton exists at `ŝ`.  It is FALSE. -/
theorem no_two_tilted_bound :
    ¬ (∀ Q : Fin 8 → Set RP, IsPacking 8 sHat Q → TwelveMet sHat Q → (∀ i, ¬ IsFlat (Q i)) → False) := by
  intro h
  obtain ⟨Q, hP, h12, hflat, _⟩ := two_tilted_ring_exists
  exact h Q hP h12 hflat

/-- **[OPEN] TYPE-T-CHASE** [C]: the chase's closing statement for the corners A248 did not reach --
no Ψ-minimal optimal eleven-square packing below side `4` is 12-stuck.  What the chase proves of it
is that the type-T ring is NOT excluded by any wall inequality on the window (`no_two_tilted_bound`)
and that the known ring's pocket holds one square; the residue is the room for the three free
squares beside a 12-stuck ring (POCKET(11) in the 12-stuck / FAMILY-STUCK form). -/
axiom type_t_chase_closes (m : ℝ) (hm : m < 4) (z : Cfg) (hz : CfgPacking m z)
    (hopt : ∀ s' : ℝ, Fits 11 s' → m ≤ s') (hpsi : PsiMin 11 m (fun i => (z i).set))
    (h12 : TwelveStuck m z) : False

theorem optimal_psiMin_not_twelve_stuck_typeT (m : ℝ) (hm : m < 4) (z : Cfg) (hz : CfgPacking m z)
    (hopt : ∀ s' : ℝ, Fits 11 s' → m ≤ s') (hpsi : PsiMin 11 m (fun i => (z i).set)) :
    ¬ TwelveStuck m z :=
  fun h12 => type_t_chase_closes m hm z hz hopt hpsi h12

#print axioms t_cells
#print axioms t_cells_floor
#print axioms t_tip
#print axioms two_tilted_ring_exists
#print axioms no_two_tilted_bound
#print axioms type_t_chase_closes
#print axioms optimal_psiMin_not_twelve_stuck_typeT

end PackingCert.S11.OpenLemmas
