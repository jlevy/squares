import PackingCertMathlib.Statements.Open.RingPocket

/-!
# -- OPEN: CENTRE-DISC — the centre set of the ring pocket, the flat-corner refutation and the
# poker-anchored obligation — A252

`docs/proofs/centre_disc.md`.  A251 reduced RING-POCKET(11) to a RADIUS: if every unit square of
the pocket has its centre within `R < 1/√3` of the container centre `O`, the pocket holds at most
two squares (`capacity_le_two_of_centre_disc`).  A252 was to prove that radius bound over the
all-ADJ ring family.  It is **false**: when both touchers of one corner tend to the flat squares
`[0,1]×[1,2]`, `[1,2]×[0,1]` of the corner frame (`θ → 90°`, `δ → 1`, the corner box still met by
slivers, the pair interlocking through a channel of width `→ 0`, the wall neighbours poking tips
into the strips Lemma GAP leaves) the disc of radius `1/2` about `(3/2, 3/2)` of the corner frame
is admissible, at distance `(s/2 − 3/2)√2` from `O`, which exceeds `1/√3` for every
`s > 3 + 2/√6 = 3.8165` — the whole window.  `adv252`: `far_O = 0.628 > 0.577` on a feasible ring
at `s = 3.99` (margin `+0.003`).  Worse, in the flat-flat corner limit the corner NOTCH holds a
disc of radius `1/2` but no unit square, so every INRADIUS-only criterion (any centre, two
pieces, three-point dispersion) is lossy there.  A251's axiom `centre_disc_ring` (about `O`) was
therefore removed from `RingPocket.lean`.

**What is a theorem here** (any `n`).
* `capacity_le_two_of_two_pieces` [T]: if the centres lie in `X₁ ∪ X₂` with all pairwise squared
  distances `< 1` inside each piece, at most two squares (pigeonhole + `inradius_sep`).
* `capacity_le_two_of_anchor` [T]: the POKER-ANCHORED form.  The coordinator (2026-09-18 00:30)
  corrected the family-stuck ring structure: the bare ring is teleportable (each eight-cell family
  {four corner boxes + one slot per wall} is met by the eight ring squares only), so the structure
  is ring + a POKER, a free square with a corner in the overlap `[0,1]×[s−2,2]` of one wall's two
  slots and its body in the centre.  If every unit square of the region that is disjoint from the
  poker has its centre in a set `X` of pairwise squared distances `< 1`, the region holds at most
  two squares (the poker and one more).  At `ŝ` the residual centre set is EMPTY
  (`poker252`: poker margin `+0.00166`, A249's `+0.0017`).
* `ring_pocket_of_poker_residual` [T]: the chain from the obligation to RING-POCKET(11).

**What is not.**  `ring_poker_residual` [C] is the exact remaining obligation for the ring family
(the residual centre set beside the poker has diameter `< 1`, over the family and every poker
position); `ring_has_poker` and `pocket_count_three` are [T-prose] (Lemma CELLS on the sixteen
eight-cell families; the count two-per-corner); `PokerOf` is opaque (the overlap-cell incidence of
`poker252.overlap_cell`).  `ring_pocket_eleven` / `family_stuck_non_ring` [C] stay as in A251.

**Status (2026-09-17).**  `capacity_le_two_of_two_pieces`, `capacity_le_two_of_anchor`,
`ring_pocket_of_poker_residual`: theorems; `ring_has_poker`, `pocket_count_three`: axioms
[T-prose]; `ring_poker_residual`: axiom [C].
-/

namespace PackingCert.S11.OpenLemmas

open Set

/-! ## 1. Two capacity criteria that survive (any n) -/

/-- **TWO-PIECES** [T].  If the centre of every unit square inside `Reg` lies in `X₁ ∪ X₂`, where
inside each piece all pairwise squared distances are `< 1`, then `Reg` holds at most two
interior-disjoint unit squares: two of any three centres share a piece, and centres of disjoint
unit squares are at squared distance `≥ 1` (`inradius_sep`). -/
theorem capacity_le_two_of_two_pieces (Reg : Set RP) (X1 X2 : Set RP)
    (hX1 : ∀ p ∈ X1, ∀ q ∈ X1, sqdist p q < 1) (hX2 : ∀ p ∈ X2, ∀ q ∈ X2, sqdist p q < 1)
    (hcen : ∀ S : Set RP, IsUnitSquare S → S ⊆ Reg →
      ∃ c : RP, (c ∈ X1 ∨ c ∈ X2) ∧ ∀ p : RP, sqdist p c < 1 / 4 → p ∈ interior S)
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
  have key : ∀ a b : Fin 3, a ≠ b → ¬ sqdist (c (f a)) (c (f b)) < 1 := fun a b hab hlt =>
    absurd (inradius_sep (hball (f a)) (hball (f b)) (hdisj _ _ (fun h => hab (f.injective h))))
      (not_le.mpr hlt)
  rcases hc (f 0) with h0 | h0 <;> rcases hc (f 1) with h1 | h1 <;> rcases hc (f 2) with h2 | h2 <;>
    first
    | exact key 0 1 (by decide) (hX1 _ h0 _ h1)
    | exact key 0 2 (by decide) (hX1 _ h0 _ h2)
    | exact key 1 2 (by decide) (hX1 _ h1 _ h2)
    | exact key 0 1 (by decide) (hX2 _ h0 _ h1)
    | exact key 0 2 (by decide) (hX2 _ h0 _ h2)
    | exact key 1 2 (by decide) (hX2 _ h1 _ h2)

/-- **POKER-ANCHORED** [T].  `P i0` is the pinned poker.  If every unit square inside `Reg` that is
interior-disjoint from the poker has its centre in a set `X` of pairwise squared distances `< 1`,
then `Reg` holds at most two of the `P a`: two non-poker squares would have centres in `X`, hence
at squared distance `< 1`, against `inradius_sep`. -/
theorem capacity_le_two_of_anchor (Reg : Set RP) (X : Set RP)
    (hX : ∀ p ∈ X, ∀ q ∈ X, sqdist p q < 1)
    (ι : Type) [Fintype ι] [DecidableEq ι] (P : ι → Set RP) (hunit : ∀ a, IsUnitSquare (P a))
    (hin : ∀ a, P a ⊆ Reg) (hdisj : ∀ a b, a ≠ b → Disjoint (interior (P a)) (interior (P b)))
    (i0 : ι)
    (hcen : ∀ S : Set RP, IsUnitSquare S → S ⊆ Reg → Disjoint (interior S) (interior (P i0)) →
      ∃ c : RP, c ∈ X ∧ ∀ p : RP, sqdist p c < 1 / 4 → p ∈ interior S) :
    Fintype.card ι ≤ 2 := by
  classical
  by_contra hcard
  push_neg at hcard
  have hc : 1 < (Finset.univ.erase i0).card := by
    rw [Finset.card_erase_of_mem (Finset.mem_univ i0), Finset.card_univ]
    omega
  obtain ⟨a, ha, b, hb, hab⟩ := Finset.one_lt_card.mp hc
  have ha0 : a ≠ i0 := (Finset.mem_erase.mp ha).1
  have hb0 : b ≠ i0 := (Finset.mem_erase.mp hb).1
  obtain ⟨ca, hca, hballa⟩ := hcen (P a) (hunit a) (hin a) (hdisj a i0 ha0)
  obtain ⟨cb, hcb, hballb⟩ := hcen (P b) (hunit b) (hin b) (hdisj b i0 hb0)
  exact absurd (hX ca hca cb hcb) (not_lt.mpr (inradius_sep hballa hballb (hdisj a b hab)))

/-! ## 2. The corrected ring structure and the obligation -/

/-- Square `j` is a POKER of the ring: its interior meets the overlap of one wall's two slots
(`[0,1]×[m−2,2]` on `x = 0` or a D4 image) — the ninth meeter of both slots of that wall
(`poker252.overlap_cell`). -/
opaque PokerOf (m : ℝ) (z : Cfg) (j : Fin 11) : Prop

/-- **[T-prose] the ring has a poker** (coordinator, 2026-09-18, Lemma CELLS on the sixteen
eight-cell families {four corner boxes + one slot per wall}: below 4 each is admissible and is met
by the eight ring squares only unless some free square meets both slots of a wall, which by
convexity means it meets their overlap). -/
axiom ring_has_poker (m : ℝ) (hm : 3.82 ≤ m ∧ m < 4) (z : Cfg) (hz : CfgPacking m z)
    (hfs : FamilyStuck m z) (hr : AllAdjRing m z) : ∃ j : Fin 11, PokerOf m z j

/-- **[OPEN] RING-POKER-RESIDUAL(11)** [C]: beside the poker, the admissible centres of the
residual pocket form a set of pairwise distances `< 1` — for every all-ADJ ring of the window and
every poker position.  `poker252`: the residual centre set is EMPTY at `ŝ`; the protected
adversarial ladder measures it over the family (`results/disc252.md`). -/
axiom ring_poker_residual (m : ℝ) (hm : 3.82 ≤ m ∧ m < 4) (z : Cfg) (hz : CfgPacking m z)
    (hr : AllAdjRing m z) (j : Fin 11) (hj : PokerOf m z j) :
    ∃ X : Set RP, (∀ p ∈ X, ∀ q ∈ X, sqdist p q < 1) ∧
      ∀ S : Set RP, IsUnitSquare S → S ⊆ container m →
        (∀ i : Fin 11, (∃ c : Fin 4, MeetsCorner m z c i) →
          Disjoint (interior S) (interior ((z i).set))) →
        Disjoint (interior S) (interior ((z j).set)) →
        ∃ c : RP, c ∈ X ∧ ∀ p : RP, sqdist p c < 1 / 4 → p ∈ interior S

/-- **[T-prose] the count**: in an all-ADJ ring exactly eight squares meet a corner box (two per
corner), so a family-stuck eleven-packing has three squares meeting no corner — three pairwise
interior-disjoint unit squares of the pocket inside the container, one of them the poker `j`;
the other two, `a ≠ b`, are disjoint from every corner meeter and from the poker (`CfgPacking`). -/
axiom pocket_count_three (m : ℝ) (hm : 3.82 ≤ m ∧ m < 4) (z : Cfg) (hz : CfgPacking m z)
    (hfs : FamilyStuck m z) (hr : AllAdjRing m z) (j : Fin 11) (hj : PokerOf m z j) :
    ∃ a b : Fin 11, a ≠ b ∧
      (IsUnitSquare ((z a).set) ∧ (z a).set ⊆ container m ∧
        (∀ i : Fin 11, (∃ c : Fin 4, MeetsCorner m z c i) →
          Disjoint (interior ((z a).set)) (interior ((z i).set))) ∧
        Disjoint (interior ((z a).set)) (interior ((z j).set))) ∧
      (IsUnitSquare ((z b).set) ∧ (z b).set ⊆ container m ∧
        (∀ i : Fin 11, (∃ c : Fin 4, MeetsCorner m z c i) →
          Disjoint (interior ((z b).set)) (interior ((z i).set))) ∧
        Disjoint (interior ((z b).set)) (interior ((z j).set))) ∧
      Disjoint (interior ((z a).set)) (interior ((z b).set))

/-- **The chain** [T]: RING-POKER-RESIDUAL + the poker + the count give RING-POCKET(11) for the
ring family: the two non-poker pocket squares have centres in `X`, at squared distance `< 1`,
against `inradius_sep`. -/
theorem ring_pocket_of_poker_residual (m : ℝ) (hm : 3.82 ≤ m ∧ m < 4) (z : Cfg)
    (hz : CfgPacking m z) (hfs : FamilyStuck m z) (hr : AllAdjRing m z) : False := by
  obtain ⟨j, hj⟩ := ring_has_poker m hm z hz hfs hr
  obtain ⟨X, hX, hres⟩ := ring_poker_residual m hm z hz hr j hj
  obtain ⟨a, b, _, ⟨hua, hca, hda, hpa⟩, ⟨hub, hcb, hdb, hpb⟩, hab⟩ :=
    pocket_count_three m hm z hz hfs hr j hj
  obtain ⟨ca, hxa, hballa⟩ := hres _ hua hca hda hpa
  obtain ⟨cb, hxb, hballb⟩ := hres _ hub hcb hdb hpb
  exact absurd (hX ca hxa cb hxb) (not_lt.mpr (inradius_sep hballa hballb hab))

#print axioms capacity_le_two_of_two_pieces
#print axioms capacity_le_two_of_anchor
#print axioms ring_has_poker
#print axioms ring_poker_residual
#print axioms pocket_count_three
#print axioms ring_pocket_of_poker_residual

end PackingCert.S11.OpenLemmas
