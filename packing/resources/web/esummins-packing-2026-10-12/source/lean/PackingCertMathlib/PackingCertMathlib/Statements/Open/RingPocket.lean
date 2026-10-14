import PackingCertMathlib.Statements.Open.TypeTChase
import PackingCertMathlib.Statements.Open.FamilyStuck
import PackingCertMathlib.Statements.Open.TwoGrains

/-!
# -- OPEN: RING-POCKET(11) — the pocket of an all-ADJ type-T ring holds at most two squares — A251

`docs/proofs/ring_pocket.md`.  A249 built the ALL-ADJ TYPE-T RING (eight tilted wall touchers,
every one reaching the far slot of its wall, all twelve border cells doubly met) and killed the
one explicit witness at `ŝ` by A237's PIERCE(1) certificate.  A250's count leaves exactly that
family.  RING-POCKET(11) is the statement for the whole family: the pocket of every all-ADJ ring
on `[3.82, 4)` holds at most TWO unit squares, so `8 + 2 < 11`.

**What is a theorem here.**  The capacity route through the INSCRIBED DISC:

* `unit_square_inball` [T-prose]: a unit square contains the open disc of radius `1/2` about its
  centre (`sqdist p c < 1/4 → p ∈ interior S`);
* `inradius_sep` [T]: two interior-disjoint unit squares have centres at squared distance `≥ 1`
  (else their common midpoint is interior to both);
* `three_disc` [T-prose]: three points pairwise at distance `≥ 1` do not fit in a disc of radius
  `R` with `3 R² < 1` (seen from the centre two of them subtend `≤ 120°`, so their distance is at
  most `√3 R`);
* `capacity_le_two_of_centre_disc` [T]: if the centre of every unit square inside a region lies
  within such an `R` of one point, the region holds at most two — **Lemma CENTRE-DISC ⟹
  RING-POCKET**, the reduction A251 delivers.

**What is measured, not proved.**  `mid_notch` [T] (`docs/proofs/ring_pocket.md` §3) closes the
wall notches: `g(t) = (1+sin t)/cos t − 2 sin t` has `min g = 0.72355`, and a disc of radius `1/2`
in a wall's middle notch would need `g(θ) + g(θ′) < 2(4 − s) ≤ 0.36`.  The corner wedges and the
vertex sectors of the separation case analysis are NOT closed, so `centre_disc_ring` — the radius
bound itself — stays an axiom [T-computed] (A251's family-wide search) and `ring_pocket_eleven`
[C] stays the obligation.

**Status (2026-09-17, A252).**  `unit_square_inball`, `three_disc`, `mid_notch_wall`: axioms
[T-prose]; `centre_disc_ring`: REMOVED (false, see `CentreDisc.lean`); `ring_pocket_eleven`,
`family_stuck_non_ring`: axioms [C];
`inradius_sep`, `capacity_le_two_of_centre_disc`, `family_stuck_eleven_of_ring_pocket`: theorems.
-/

namespace PackingCert.S11.OpenLemmas

open Set

/-! ## 1. The inscribed disc -/

/-- **[T-prose]** A unit square contains the open disc of radius `1/2` about its centre. -/
axiom unit_square_inball (S : Set RP) (hS : IsUnitSquare S) :
    ∃ c : RP, ∀ p : RP, sqdist p c < 1 / 4 → p ∈ interior S

/-- **Lemma INRADIUS** [T]: interior-disjoint unit squares have centres at squared
distance `≥ 1`. -/
theorem inradius_sep {S T : Set RP} {c d : RP}
    (hc : ∀ p : RP, sqdist p c < 1 / 4 → p ∈ interior S)
    (hd : ∀ p : RP, sqdist p d < 1 / 4 → p ∈ interior T)
    (hST : Disjoint (interior S) (interior T)) : 1 ≤ sqdist c d := by
  by_contra h
  push_neg at h
  set m : RP := ((c.1 + d.1) / 2, (c.2 + d.2) / 2) with hm
  have hmc : sqdist m c = sqdist c d / 4 := by
    simp only [hm, sqdist]; ring
  have hmd : sqdist m d = sqdist c d / 4 := by
    simp only [hm, sqdist]; ring
  have h1 : m ∈ interior S := hc m (by rw [hmc]; linarith)
  have h2 : m ∈ interior T := hd m (by rw [hmd]; linarith)
  exact Set.disjoint_left.mp hST h1 h2

/-- **Lemma THREE-DISC** [T-prose]: three points pairwise at distance `≥ 1` do not lie in a disc
of radius `R` with `3 R² < 1`. -/
axiom three_disc (o : RP) (R : ℝ) (hR : 3 * R ^ 2 < 1) (c : Fin 3 → RP)
    (hin : ∀ a, sqdist (c a) o ≤ R ^ 2) : ∃ a b, a ≠ b ∧ sqdist (c a) (c b) < 1

/-- **Lemma CENTRE-DISC ⟹ RING-POCKET** [T].  If the centre of every unit square inside `Reg`
lies within `R` of `o` and `3 R² < 1`, then `Reg` holds at most two interior-disjoint unit
squares.  (This is A251's reduction: the capacity bound needs only a radius, not a pierce.) -/
theorem capacity_le_two_of_centre_disc (Reg : Set RP) (o : RP) (R : ℝ) (hR : 3 * R ^ 2 < 1)
    (hcen : ∀ S : Set RP, IsUnitSquare S → S ⊆ Reg →
      ∃ c : RP, sqdist c o ≤ R ^ 2 ∧ ∀ p : RP, sqdist p c < 1 / 4 → p ∈ interior S)
    (ι : Type) [Fintype ι] (P : ι → Set RP) (hunit : ∀ a, IsUnitSquare (P a))
    (hin : ∀ a, P a ⊆ Reg) (hdisj : ∀ a b, a ≠ b → Disjoint (interior (P a)) (interior (P b))) :
    Fintype.card ι ≤ 2 := by
  classical
  by_contra hcard
  push_neg at hcard
  have h3 : Fintype.card (Fin 3) ≤ Fintype.card ι := by
    simp only [Fintype.card_fin]
    omega
  obtain ⟨f⟩ := Function.Embedding.nonempty_of_card_le h3
  choose c hc hball using fun a => hcen (P a) (hunit a) (hin a)
  obtain ⟨a, b, hab, hlt⟩ := three_disc o R hR (fun k => c (f k)) (fun k => hc (f k))
  have hne : f a ≠ f b := fun h => hab (f.injective h)
  exact absurd (inradius_sep (hball (f a)) (hball (f b)) (hdisj _ _ hne)) (not_le.mpr hlt)

/-! ## 2. The ring family and the obligation -/

/-- The ALL-ADJ RING structure of A249 on a family-stuck configuration: the eight corner meeters
touch their walls and each reaches the far slot of its wall (`type_t_chase.md` §2.3, the
parametrisation of `family251.py`). -/
opaque AllAdjRing (m : ℝ) (z : Cfg) : Prop

/-- **Lemma MID-NOTCH** [T] (`ring_pocket.md` §3.3): on `s > 4 − 0.72355` no disc of radius `1/2`
lies in the middle notch of a wall of an all-ADJ ring — between the two touchers' inner edge
lines and the wall.  Stated here as the exclusion it is used for. -/
axiom mid_notch_wall (m : ℝ) (hm : 3.82 ≤ m) (z : Cfg) (hz : CfgPacking m z)
    (hr : AllAdjRing m z) (c : RP)
    (hnotch : ∀ i : Fin 11, Disjoint (interior ((z i).set)) {p : RP | sqdist p c < 1 / 4}) :
    ∃ R : ℝ, 3 * R ^ 2 < 1 ∧ sqdist c (m / 2, m / 2) ≤ R ^ 2

/-! A251's axiom `centre_disc_ring` (every admissible centre within `1/√3` of the container
centre `O`) was REMOVED by A252 (2026-09-17): it is FALSE on the window — the corner MOUTH of a
near-flat corner admits a centre at `(s/2 − 3/2)√2 > 1/√3` from `O` for every `s > 3.8165`
(`docs/proofs/centre_disc.md`, `Statements/Open/CentreDisc.lean`, adv252: `far_O = 0.628` at
`s = 3.99` on a feasible ring).  `mid_notch_wall` below is unaffected (it is the exclusion of the
wall's middle notch, a theorem in prose). -/

/-- **[OPEN] RING-POCKET(11)** [C]: no family-stuck eleven-square packing below side `4` has the
all-ADJ ring structure — the pocket of the eight wall touchers holds at most two squares, and
`8 + 2 < 11`. -/
axiom ring_pocket_eleven (m : ℝ) (hm : 3.82 ≤ m ∧ m < 4) (z : Cfg) (hz : CfgPacking m z)
    (hfs : FamilyStuck m z) (hr : AllAdjRing m z) : False

/-- **[OPEN]** the residue A249's enumeration leaves beside the all-ADJ ring: mixed type-F /
type-T and non-ring family-stuck structures (`ring_pocket.md` §5). -/
axiom family_stuck_non_ring (m : ℝ) (hm : 3.82 ≤ m ∧ m < 4) (z : Cfg) (hz : CfgPacking m z)
    (hfs : FamilyStuck m z) (hr : ¬ AllAdjRing m z) : False

/-- The two together are the family-stuck existence obligation on the window. -/
theorem family_stuck_eleven_of_ring_pocket (m : ℝ) (hm : 3.82 ≤ m ∧ m < 4) (z : Cfg)
    (hz : CfgPacking m z) (hfs : FamilyStuck m z) : False := by
  by_cases hr : AllAdjRing m z
  · exact ring_pocket_eleven m hm z hz hfs hr
  · exact family_stuck_non_ring m hm z hz hfs hr

#print axioms unit_square_inball
#print axioms inradius_sep
#print axioms three_disc
#print axioms capacity_le_two_of_centre_disc
#print axioms mid_notch_wall
#print axioms ring_pocket_eleven
#print axioms family_stuck_eleven_of_ring_pocket

end PackingCert.S11.OpenLemmas
