import PackingCertMathlib.Statements.Open.LocalLock

/-!
# -- OPEN: Theorem CROSS — the PI's X-sketch made exact: planarity of two bracing chains, and what it does
# not give (A240)

`docs/proofs/cross.md`.  The PI (2026-09-16, 12:00): "corner jams require opposing torques ... the left C grain
needs to touch the right C grain to brace against the opposite wall, but that would prevent the W grains from
meeting".

**What is a theorem here.**  (iv) PLANARITY, `crossing_lemma` (a classical fact of plane topology, [T] in
prose, `cross.md` §3: two continua in the square, one meeting the left and right walls and one meeting the
floor and the ceiling, intersect — the Brouwer / Hex lemma, proved through polygonal approximation of the
`ε`-neighbourhoods and Maehara's path-crossing argument; not in Mathlib, hence an axiom).  A CHAIN (`IsChain`) is
a set of indices whose squares' union is connected and meets two given walls.  `chains_meet`: a left-right chain
and a floor-ceiling chain of a packing meet; `chains_share_or_touch`: they share a square OR a square of one
touches a square of the other — the second alternative is what the PI's "share a square" misses (the two
chains may meet at an UNLOADED contact); `isCompact_of_isUnitSquare` supplies the compactness.

**What is NOT a theorem, and is refuted** (`cross.md` §1, §4; A240's census of 1 363 doubly-met corners):
(i) Lemma OPPOSE — "the two meeters of a locked corner have opposite handedness" — is FALSE: 215 LOCKED corners
(both meeters loaded, no external row on either; 44 of them at free Fritz-John points) are same-handed against
11 opposite-handed, most of them flush same-tilt pairs, and the exact torque of a vertex-on-edge partner contact
(Lemma PARTNER-TORQUE) depends on the TILT DIFFERENCE and the contact POSITION, never on the handedness;
(ii) the alternation of wall grains occurs on 0 of 193 four-crowds (110 have a mixed wall);
(v) the shared square is not obstructed: 90 tilted interior squares carry both chains with no external load.
No axiom is added for OPPOSE or for the obstruction: a refuted statement is not an obligation.  The residue
LOCKED-CROWD-FREE(n) (`locked_crowd_free`) is unchanged.

**Status (2026-09-16).**  `crossing_lemma`: axiom [T, classical topology]; `isCompact_of_isUnitSquare`,
`chains_meet`, `chains_share_or_touch`: theorems.
-/

namespace PackingCert.S11.OpenLemmas

open Set

/-- The left wall `x = 0`, right wall `x = s`, floor `y = 0`, ceiling `y = s` of the container (as lines). -/
def wallLeft : Set RP := {p | p.1 = 0}
def wallRight (s : ℝ) : Set RP := {p | p.1 = s}
def wallFloor : Set RP := {p | p.2 = 0}
def wallCeil (s : ℝ) : Set RP := {p | p.2 = s}

/-- A CHAIN of squares from wall `A` to wall `B`: a set `I` of indices whose union `⋃ i ∈ I, Q i` is
connected and meets both walls (a contact chain of squares is connected; the loaded component of a corner's
meeters, Corollary CHAIN, is one). -/
def IsChain {n : ℕ} (Q : Fin n → Set RP) (I : Finset (Fin n)) (A B : Set RP) : Prop :=
  IsConnected (⋃ i ∈ I, Q i) ∧ ((⋃ i ∈ I, Q i) ∩ A).Nonempty ∧ ((⋃ i ∈ I, Q i) ∩ B).Nonempty

/-- **[T, classical] The crossing lemma.**  Two compact connected subsets of the container `[0, s]²`, one
meeting the left and the right wall, the other the floor and the ceiling, intersect.  Prose proof in
`cross.md` §3 (ε-neighbourhoods are open and connected, hence path-connected; two disjoint polygonal crossings
of a square contradict the Brouwer fixed-point theorem, Maehara 1984). -/
axiom crossing_lemma (s : ℝ) (K L : Set RP) (hK : IsCompact K) (hKc : IsConnected K)
    (hL : IsCompact L) (hLc : IsConnected L) (hKin : K ⊆ container s) (hLin : L ⊆ container s)
    (hK0 : (K ∩ wallLeft).Nonempty) (hKs : (K ∩ wallRight s).Nonempty)
    (hL0 : (L ∩ wallFloor).Nonempty) (hLs : (L ∩ wallCeil s).Nonempty) : (K ∩ L).Nonempty

/-- A unit square is compact: the continuous image of `[0,1]²` under `aff`. -/
theorem isCompact_of_isUnitSquare {S : Set RP} (h : IsUnitSquare S) : IsCompact S := by
  obtain ⟨p0, e, -, rfl⟩ := h
  have himg : sqSet p0 e = (fun ab : ℝ × ℝ => aff p0 e ab.1 ab.2) '' (Icc (0 : ℝ) 1 ×ˢ Icc (0 : ℝ) 1) := by
    ext q
    constructor
    · rintro ⟨a, b, ha0, ha1, hb0, hb1, rfl⟩
      exact ⟨(a, b), ⟨⟨ha0, ha1⟩, ⟨hb0, hb1⟩⟩, rfl⟩
    · rintro ⟨⟨a, b⟩, ⟨⟨ha0, ha1⟩, ⟨hb0, hb1⟩⟩, rfl⟩
      exact ⟨a, b, ha0, ha1, hb0, hb1, rfl⟩
  rw [himg]
  refine (isCompact_Icc.prod isCompact_Icc).image ?_
  unfold aff
  fun_prop

/-- **Theorem CROSS-PLANAR (i).**  A left-right chain and a floor-ceiling chain of a packing meet. -/
theorem chains_meet {n : ℕ} {s : ℝ} {Q : Fin n → Set RP} (hP : IsPacking n s Q)
    {I J : Finset (Fin n)} (hI : IsChain Q I wallLeft (wallRight s)) (hJ : IsChain Q J wallFloor (wallCeil s)) :
    ((⋃ i ∈ I, Q i) ∩ (⋃ j ∈ J, Q j)).Nonempty := by
  have hc : ∀ i, IsCompact (Q i) := fun i => isCompact_of_isUnitSquare (hP.unit i)
  refine crossing_lemma s _ _ (I.isCompact_biUnion fun i _ => hc i) hI.1
    (J.isCompact_biUnion fun j _ => hc j) hJ.1 ?_ ?_ hI.2.1 hI.2.2 hJ.2.1 hJ.2.2
  · exact iUnion₂_subset fun i _ => hP.contained i
  · exact iUnion₂_subset fun j _ => hP.contained j

/-- **Theorem CROSS-PLANAR (ii).**  The two chains SHARE a square, or a square of one TOUCHES a square of the
other (a common boundary point; interiors are disjoint in a packing).  The second alternative is the case the
X-sketch omits: the chains may meet at a contact that carries no load. -/
theorem chains_share_or_touch {n : ℕ} {s : ℝ} {Q : Fin n → Set RP} (hP : IsPacking n s Q)
    {I J : Finset (Fin n)} (hI : IsChain Q I wallLeft (wallRight s)) (hJ : IsChain Q J wallFloor (wallCeil s)) :
    (∃ i, i ∈ I ∧ i ∈ J) ∨ ∃ i ∈ I, ∃ j ∈ J, i ≠ j ∧ (Q i ∩ Q j).Nonempty := by
  obtain ⟨p, hpI, hpJ⟩ := chains_meet hP hI hJ
  rw [mem_iUnion₂] at hpI hpJ
  obtain ⟨i, hi, hpi⟩ := hpI
  obtain ⟨j, hj, hpj⟩ := hpJ
  by_cases hij : i = j
  · exact Or.inl ⟨i, hi, hij ▸ hj⟩
  · exact Or.inr ⟨i, hi, j, hj, hij, p, hpi, hpj⟩

#print axioms crossing_lemma
#print axioms isCompact_of_isUnitSquare
#print axioms chains_meet
#print axioms chains_share_or_touch

end PackingCert.S11.OpenLemmas
