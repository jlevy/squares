import PackingCertMathlib.NoRoom

/-!
# The NO-ROOM leaf — A189 Lemma 1 (pocket counting bound)

**What it says.**  At a node with `k` boxed roles the remaining `M = n − k` free unit squares
have pairwise disjoint interiors.  Suppose finitely many closed axis-aligned rectangles with
non-empty interior (the POCKETS `P_j`) cover the CENTRES of every free pose, and for each
pocket a LANE bound `lane j` dominates the number of pairwise interior-disjoint free squares
whose interiors meet `int P_j`.  Then `M ≤ Σ_j lane j`; if the lanes sum to less than `M`, no
such family exists and the node is DEAD.

**Why it matters.**  It is the leaf rule that closes fully-named pages where the boxed roles
leave less room than the free squares need — the coordinator's STEP 34 certificate at
`k = n − 1` (dead iff every pocket has lane 0), and with A161's pair test at `k = n − 2`.

**How it is proved** (`NoRoom.lean`, A192): a unit square whose centre lies in a closed
rectangle with non-empty interior has its interior meeting the rectangle's interior
(`interior_meets_of_centre_mem`: the centre is an interior point of the square, and every
neighbourhood of a point of a closed rectangle meets its interior); then assign each free
square a pocket it meets and bound the fibres by the lanes
(`Finset.card_eq_sum_card_fiberwise`).

**What is still prose / certificate data** (`Statements/Open/NoRoom189.lean`): the residue
cover (that every dropped piece of the bisection is dead) and the lane cover's own soundness
(`multibox.Node.lane`, an exact geometric test) — the two hypotheses of this theorem.

**For any `n`.**  Stated for every `M`, `r`.
-/

namespace PackingCert.S11

open Set NoRoom

/-- **A189 Lemma 1, the leaf.**  Pockets covering the centres, lanes summing below `M` ⇒ no such
family of `M` interior-disjoint unit squares exists. -/
theorem noroom_leaf {M r : ℕ} (q : Fin M → PSq)
    (hdisj : ∀ i j, i ≠ j → Disjoint (interior (q i).set) (interior (q j).set))
    (P : Fin r → Pocket) (lane : Fin r → ℕ)
    (hlane : ∀ j, ∀ G : Finset (Fin M),
      (∀ i ∈ G, ∀ i' ∈ G, i ≠ i' → Disjoint (interior (q i).set) (interior (q i').set)) →
      (∀ i ∈ G, (interior (q i).set ∩ interior (P j).set).Nonempty) → G.card ≤ lane j)
    (hcent : ∀ i, ∃ j, ((q i).cx, (q i).cy) ∈ (P j).set)
    (hsum : ∑ j, lane j < M) : False :=
  noroom_dead q hdisj P lane hlane hcent hsum

#print axioms noroom_leaf

end PackingCert.S11
