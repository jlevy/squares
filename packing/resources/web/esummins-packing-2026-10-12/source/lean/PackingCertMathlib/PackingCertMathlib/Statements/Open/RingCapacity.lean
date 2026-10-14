import PackingCertMathlib.Statements.Open.LocalLock

/-!
# -- OPEN: Conjecture RING-CAPACITY — a stable ring needs side ≥ ⌈√n⌉ — and what the capacity count proves (A236)

`docs/proofs/ring_capacity.md`.  The PI (2026-09-15, 21:00): "show that the minimal side required to build a
stable ring requires a side length strictly greater than the trivial packing at ⌈√n⌉".

**The statement (n-general).**  A STABLE RING is a four-crowd (`FourCrowdN`: every corner box met by two
squares) none of whose meeters RETREATS (`Retreats`, A233; LOCKED ⇒ retreat-free, and at the Ψ-minimal optimum
every meeter is retreat-free — `no_retreat_of_psiMin`).  **Conjecture RING-CAPACITY(n)** [C], axiom
`ring_capacity`: every stable ring of `n` unit squares has side `≥ ⌈√n⌉`.  It is stated for EVERY packing (the
PI's "minimal side to build a stable ring"), so it is formally stronger than A233's `locked_crowd_free`
(which asks it of OPTIMAL packings only); `locked_crowd_free_of_ring_capacity` derives that residue from it,
`one_flush_value_of_ring_capacity` gives ONE-FLUSH(n) in its value form through the extremal route, and
`optimal_psiMin_not_stuck_of_ring_capacity` is the n = 11 corollary.  Evidence (`ring_capacity.md` §4): the
193 held four-crowds all sit at side ≥ 4.0014, the eight-square crowd ring of A226 leaves room for ONE further
square below 4 (9 < 11), no stable ring below `⌈√n⌉` is known at any `n`.

**What the CAPACITY route proves, and why it does not close** (`ring_capacity.md` §2–3, [T] in prose).  Cut the
container at the unit band: the open CENTRE `(1, s−1)²` (`centreOpen`), its closure (`centreClosed`); every
square is a BAND square (interior missing the centre, `IsBand`), a CORE square (inside the closed centre,
`IsCore`) or a STRADDLER (`IsStraddler`), and `core_not_band` says the first two classes are disjoint.
Lemma TILT-BAND: for `s > 2 + √2` every TILTED square meets the open centre, with no lower bound on its
intrusion; Lemma BAND-FLUSH: a band square is flush and touches a wall; Lemma BAND-COUNT: a four-crowd below
`⌈√n⌉ = m` has at most `4(m − 2)` band squares; Lemma CORE-CAP: at most `(m − 2)² − 3` core squares (Nagamochi:
`s(k² − 2) = k`; at `m = 4` the direct Lemma TWO, `N(σ) = 1` for `σ < 2`); ONE-TILTED: at least `4` straddlers.
**Theorem NO-CLOSURE** (`count_never_closes`, pure arithmetic): `4(m − 2) + ((m − 2)² − 3) + 4 = m² − 3 ≥ n`
for every `n` with `s(n) < m` — the band-plus-core count has room for exactly every `n` that packs below `m`,
so the capacity inequality excludes a four-crowd for NO `n`; at `n = 11` the count is `8 + 1 + 4 = 13 ≥ 11`.
The residue is the straddlers' geometry (the ring's POCKET), a region-packing statement, [C] at every `n`.

**Status (2026-09-15).**  `ring_capacity`: axiom [C]; everything else: theorems.
-/

namespace PackingCert.S11.OpenLemmas

open Set

/-- The open CENTRE `(1, s − 1)²`: the container minus the closed unit band along its four walls. -/
def centreOpen (s : ℝ) : Set RP := Ioo (1 : ℝ) (s - 1) ×ˢ Ioo (1 : ℝ) (s - 1)

/-- The closed centre `[1, s − 1]²`. -/
def centreClosed (s : ℝ) : Set RP := Icc (1 : ℝ) (s - 1) ×ˢ Icc (1 : ℝ) (s - 1)

/-- A BAND square: its interior misses the open centre (Lemma BAND-FLUSH: it is then flush and touches a
wall). -/
def IsBand (s : ℝ) (Q : Set RP) : Prop := Disjoint (interior Q) (centreOpen s)

/-- A CORE square: contained in the closed centre. -/
def IsCore (s : ℝ) (Q : Set RP) : Prop := Q ⊆ centreClosed s

/-- A STRADDLER: neither band nor core (every tilted non-core square is one, Lemma TILT-BAND). -/
def IsStraddler (s : ℝ) (Q : Set RP) : Prop := ¬ IsBand s Q ∧ ¬ IsCore s Q

/-- A STABLE RING: a four-crowd none of whose meeters retreats (LOCKED ⇒ retreat-free, A233). -/
def StableRing (s : ℝ) {n : ℕ} (Q : Fin n → Set RP) : Prop :=
  FourCrowdN s Q ∧ ∀ (c : Fin 4) (i : Fin n), MeetsCornerN s Q c i → ¬ Retreats s Q c i

/-- **[OPEN] Conjecture RING-CAPACITY.**  A stable ring of `n` unit squares has side `≥ ⌈√n⌉`. -/
axiom ring_capacity (n : ℕ) (s : ℝ) (Q : Fin n → Set RP) (hP : IsPacking n s Q)
    (hring : StableRing s Q) : ((Nat.ceil (Real.sqrt (n : ℝ)) : ℕ) : ℝ) ≤ s

/-- RING-CAPACITY(n) ⇒ LOCKED-CROWD-FREE(n) (A233's residue, `locked_crowd_free`'s statement). -/
theorem locked_crowd_free_of_ring_capacity (n : ℕ) (s : ℝ) (Q : Fin n → Set RP)
    (hopt : IsOptimalPacking n s Q) (hs : s < ((Nat.ceil (Real.sqrt (n : ℝ)) : ℕ) : ℝ))
    (hcrowd : FourCrowdN s Q)
    (hlock : ∀ (c : Fin 4) (i : Fin n), MeetsCornerN s Q c i → ¬ Retreats s Q c i) : False :=
  absurd (ring_capacity n s Q hopt.1 ⟨hcrowd, hlock⟩) (not_le.mpr hs)

/-- **ONE-FLUSH(n), value form, from RING-CAPACITY**: an optimal `Ψ`-minimal packing below `⌈√n⌉` has a
singly-met corner (the extremal route of A233 with `ring_capacity` in place of `locked_crowd_free`). -/
theorem one_flush_value_of_ring_capacity (n : ℕ) (s : ℝ) (Q : Fin n → Set RP)
    (hopt : IsOptimalPacking n s Q) (hpsi : PsiMin n s Q)
    (hs : s < ((Nat.ceil (Real.sqrt (n : ℝ)) : ℕ) : ℝ)) :
    ∃ c : Fin 4, SinglyMet s Q c := by
  by_contra hno
  have hcrowd : FourCrowdN s Q := fun c hc => hno ⟨c, hc⟩
  exact locked_crowd_free_of_ring_capacity n s Q hopt hs hcrowd
    (fun c i _ => no_retreat_of_psiMin hpsi c i)

/-- **Corollary (n = 11).**  An optimal, `Ψ`-minimal eleven-square packing below side 4 is not
teleport-stuck. -/
theorem optimal_psiMin_not_stuck_of_ring_capacity (m : ℝ) (hm : m < 4) (z : Cfg) (hz : CfgPacking m z)
    (hopt : ∀ s' : ℝ, Fits 11 s' → m ≤ s') (hpsi : PsiMin 11 m (fun i => (z i).set)) :
    ¬ TeleportStuck m z := by
  intro hst
  have hopt' : IsOptimalPacking 11 m (fun i => (z i).set) := ⟨hz.2, hopt⟩
  have h4 : m < ((Nat.ceil (Real.sqrt ((11 : ℕ) : ℝ)) : ℕ) : ℝ) := by
    rw [ceil_sqrt_eleven]
    exact_mod_cast hm
  obtain ⟨c, hc⟩ := one_flush_value_of_ring_capacity 11 m _ hopt' hpsi h4
  obtain ⟨i, j, hij, hi, hj⟩ := hst c
  exact hij (hc i j hi hj)

/-! ## The trichotomy and the count -/

/-- The interior of the closed centre is the open centre. -/
theorem interior_centreClosed (s : ℝ) : interior (centreClosed s) = centreOpen s := by
  unfold centreClosed centreOpen
  rw [interior_prod_eq, interior_Icc]

/-- A core square with non-empty interior is not a band square: the two classes are disjoint. -/
theorem core_not_band {s : ℝ} {Q : Set RP} (hne : (interior Q).Nonempty) (hcore : IsCore s Q) :
    ¬ IsBand s Q := by
  intro hband
  obtain ⟨p, hp⟩ := hne
  have h1 : p ∈ centreOpen s := by
    rw [← interior_centreClosed]
    exact interior_mono hcore hp
  exact Set.disjoint_left.mp hband hp h1

/-- Every square is band, core or straddler. -/
theorem band_or_core_or_straddler (s : ℝ) (Q : Set RP) :
    IsBand s Q ∨ IsCore s Q ∨ IsStraddler s Q := by
  by_cases hb : IsBand s Q
  · exact Or.inl hb
  · by_cases hc : IsCore s Q
    · exact Or.inr (Or.inl hc)
    · exact Or.inr (Or.inr ⟨hb, hc⟩)

/-- **Theorem NO-CLOSURE.**  The capacity count — at most `4(m − 2)` band squares, at most
`(m − 2)² − 3` core squares, at least `4` straddlers (the tilted meeters) — sums to exactly `m² − 3`,
and every `n` with `s(n) < m` satisfies `n ≤ m² − 3` (`s(m² − 2) = m`, Nagamochi): the inequality
`n ≤ B + K + X` never contradicts, at any `n`. -/
theorem count_never_closes (n m : ℤ) (hn : n ≤ m ^ 2 - 3) :
    n ≤ 4 * (m - 2) + ((m - 2) ^ 2 - 3) + 4 := by
  have h : 4 * (m - 2) + ((m - 2) ^ 2 - 3) + 4 = m ^ 2 - 3 := by ring
  rw [h]
  exact hn

#print axioms ring_capacity
#print axioms locked_crowd_free_of_ring_capacity
#print axioms one_flush_value_of_ring_capacity
#print axioms optimal_psiMin_not_stuck_of_ring_capacity
#print axioms interior_centreClosed
#print axioms core_not_band
#print axioms band_or_core_or_straddler
#print axioms count_never_closes

end PackingCert.S11.OpenLemmas
