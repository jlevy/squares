import PackingCertMathlib.Statements.Open.RingCapacity

/-!
# -- OPEN: POCKET-CAP — the centre pocket of a stable ring cannot hold the other n − p squares (A237)

`docs/proofs/pocket_waste.md`.  The PI (2026-09-16, 00:00): "given the tilt requirements of the loaded ring
… the pocket is almost necessarily quite jagged — use the wastage census on grain boundaries to assert a minimum
wastage in the centre pocket, then show there isn't room for n − (ring)".

**The statement (n-general).**  For a packing `Q` and a set `U` of RING MEMBERS (A233's loaded component: the
meeters, their wall chains and holders — every meeter is in `U`), the POCKET is the container minus the
members' interiors, and `PacksBeside s Q U ι P` says that the family `P` (indexed by a finite type `ι`) packs
in it: unit squares inside the container, pairwise interior-disjoint and interior-disjoint from every member.
`PocketCapacityLT s Q U k`: no family of `k` squares packs beside `U`.  **Conjecture POCKET-CAP(n)** [C], axiom
`pocket_cap`: for a STABLE RING (`StableRing`, A236: a four-crowd none of whose meeters retreats) at side
`s < ⌈√n⌉` and every member set `U` containing the meeters, the pocket's capacity is `< n − |U|`.  It is
A236's residue POCKET(n) made exact; `ring_capacity_of_pocket_cap` derives RING-CAPACITY(n) from it (the other
`n − |U|` squares of the ring DO pack beside `U`), hence LOCKED-CROWD-FREE(n) and ONE-FLUSH(n) in value form
(`locked_crowd_free_of_pocket_cap`, `one_flush_value_of_pocket_cap`) and the n = 11 corollary
(`optimal_psiMin_not_stuck_of_pocket_cap`).

**What is a theorem here.**  `capacity_le_of_pierce` (PIERCE): if every unit square inside a region contains one
of `k` given points in its INTERIOR, then any interior-disjoint family of unit squares in the region has at most
`k` members — the certificate `pocket237.py` / `family237.py` verify on the lab's pockets (a piercing point of
the eroded free-centre region of every 1° tilt bin; `pocket_waste.md` §2 (J3), §4).  The prose lemmas
TILT-MIN (an UPPER bound on the tilt of a locked flat meeter's partner, `sin θ ≤ δ`), DEPTH-BUDGET, WEDGE and
the coverable-set sandwich (JAGGED) are [T] in `pocket_waste.md` §1–§2 and are not formalised; POCKET-CAP itself
does NOT close analytically at n = 11 (`pocket_waste.md` §3: the waste is O(tilt) and no tilt floor exists,
A89) — the axiom is the residue, unchanged from A236's POCKET(n).

**Status (2026-09-16).**  `pocket_cap`: axiom [C]; everything else: theorems.
-/

namespace PackingCert.S11.OpenLemmas

open Set

/-- The family `P : ι → Set RP` PACKS BESIDE the members `U` of `Q` at side `s`: unit squares inside the
container, pairwise interior-disjoint, each interior-disjoint from every member. -/
def PacksBeside (s : ℝ) {n : ℕ} (Q : Fin n → Set RP) (U : Finset (Fin n)) (ι : Type) [Fintype ι]
    (P : ι → Set RP) : Prop :=
  (∀ a, IsUnitSquare (P a)) ∧ (∀ a, P a ⊆ container s) ∧
    (∀ a b, a ≠ b → Disjoint (interior (P a)) (interior (P b))) ∧
    ∀ a, ∀ i ∈ U, Disjoint (interior (P a)) (interior (Q i))

/-- The pocket of `U` has CAPACITY `< k`: no family of `k` unit squares packs beside `U`. -/
def PocketCapacityLT (s : ℝ) {n : ℕ} (Q : Fin n → Set RP) (U : Finset (Fin n)) (k : ℕ) : Prop :=
  ∀ (ι : Type) [Fintype ι] (P : ι → Set RP), Fintype.card ι = k → ¬ PacksBeside s Q U ι P

/-- **[OPEN] Conjecture POCKET-CAP.**  For a stable ring at side `< ⌈√n⌉` and every member set `U` containing
the meeters, the pocket holds fewer than `n − |U|` unit squares. -/
axiom pocket_cap (n : ℕ) (s : ℝ) (Q : Fin n → Set RP) (hP : IsPacking n s Q) (hring : StableRing s Q)
    (hs : s < ((Nat.ceil (Real.sqrt (n : ℝ)) : ℕ) : ℝ)) (U : Finset (Fin n))
    (hU : ∀ (c : Fin 4) (i : Fin n), MeetsCornerN s Q c i → i ∈ U) :
    PocketCapacityLT s Q U (n - U.card)

/-- The non-members of a packing pack beside the members. -/
theorem packsBeside_compl {n : ℕ} {s : ℝ} {Q : Fin n → Set RP} (hP : IsPacking n s Q) (U : Finset (Fin n)) :
    PacksBeside s Q U {i : Fin n // i ∉ U} (fun a => Q a.1) :=
  ⟨fun a => hP.unit a.1, fun a => hP.contained a.1,
    fun a b hab => hP.interiorDisjoint a.1 b.1 (fun h => hab (Subtype.ext h)),
    fun a i hi => hP.interiorDisjoint a.1 i (fun h => a.2 (h ▸ hi))⟩

/-- **POCKET-CAP(n) ⇒ RING-CAPACITY(n)**: a stable ring has side `≥ ⌈√n⌉`. -/
theorem ring_capacity_of_pocket_cap (n : ℕ) (s : ℝ) (Q : Fin n → Set RP) (hP : IsPacking n s Q)
    (hring : StableRing s Q) : ((Nat.ceil (Real.sqrt (n : ℝ)) : ℕ) : ℝ) ≤ s := by
  classical
  by_contra hs
  push_neg at hs
  let U : Finset (Fin n) := Finset.univ.filter (fun i => ∃ c : Fin 4, MeetsCornerN s Q c i)
  have hU : ∀ (c : Fin 4) (i : Fin n), MeetsCornerN s Q c i → i ∈ U :=
    fun c i hi => Finset.mem_filter.mpr ⟨Finset.mem_univ i, c, hi⟩
  have hcard : Fintype.card {i : Fin n // i ∉ U} = n - U.card := by
    rw [Fintype.card_subtype_compl, Fintype.card_fin]
    congr 1
    exact Fintype.card_coe U
  exact pocket_cap n s Q hP hring hs U hU _ (fun a => Q a.1) hcard (packsBeside_compl hP U)

/-- POCKET-CAP(n) ⇒ LOCKED-CROWD-FREE(n) (A233's residue). -/
theorem locked_crowd_free_of_pocket_cap (n : ℕ) (s : ℝ) (Q : Fin n → Set RP)
    (hopt : IsOptimalPacking n s Q) (hs : s < ((Nat.ceil (Real.sqrt (n : ℝ)) : ℕ) : ℝ))
    (hcrowd : FourCrowdN s Q)
    (hlock : ∀ (c : Fin 4) (i : Fin n), MeetsCornerN s Q c i → ¬ Retreats s Q c i) : False :=
  absurd (ring_capacity_of_pocket_cap n s Q hopt.1 ⟨hcrowd, hlock⟩) (not_le.mpr hs)

/-- **ONE-FLUSH(n), value form, from POCKET-CAP.** -/
theorem one_flush_value_of_pocket_cap (n : ℕ) (s : ℝ) (Q : Fin n → Set RP)
    (hopt : IsOptimalPacking n s Q) (hpsi : PsiMin n s Q)
    (hs : s < ((Nat.ceil (Real.sqrt (n : ℝ)) : ℕ) : ℝ)) :
    ∃ c : Fin 4, SinglyMet s Q c := by
  by_contra hno
  have hcrowd : FourCrowdN s Q := fun c hc => hno ⟨c, hc⟩
  exact locked_crowd_free_of_pocket_cap n s Q hopt hs hcrowd
    (fun c i _ => no_retreat_of_psiMin hpsi c i)

/-- **Corollary (n = 11).**  An optimal, `Ψ`-minimal eleven-square packing below side 4 is not
teleport-stuck. -/
theorem optimal_psiMin_not_stuck_of_pocket_cap (m : ℝ) (hm : m < 4) (z : Cfg) (hz : CfgPacking m z)
    (hopt : ∀ s' : ℝ, Fits 11 s' → m ≤ s') (hpsi : PsiMin 11 m (fun i => (z i).set)) :
    ¬ TeleportStuck m z := by
  intro hst
  have hopt' : IsOptimalPacking 11 m (fun i => (z i).set) := ⟨hz.2, hopt⟩
  have h4 : m < ((Nat.ceil (Real.sqrt ((11 : ℕ) : ℝ)) : ℕ) : ℝ) := by
    rw [ceil_sqrt_eleven]
    exact_mod_cast hm
  obtain ⟨c, hc⟩ := one_flush_value_of_pocket_cap 11 m _ hopt' hpsi h4
  obtain ⟨i, j, hij, hi, hj⟩ := hst c
  exact hij (hc i j hi hj)

/-! ## PIERCE: a piercing set bounds the capacity -/

/-- **Lemma PIERCE.**  If every unit square inside the region `R` contains one of the points `p 0, …, p (k−1)`
in its interior, then an interior-disjoint family of unit squares inside `R` has at most `k` members. -/
theorem capacity_le_of_pierce (R : Set RP) (k : ℕ) (p : Fin k → RP)
    (hpierce : ∀ S : Set RP, IsUnitSquare S → S ⊆ R → ∃ i, p i ∈ interior S)
    (ι : Type) [Fintype ι] (P : ι → Set RP) (hunit : ∀ a, IsUnitSquare (P a)) (hin : ∀ a, P a ⊆ R)
    (hdisj : ∀ a b, a ≠ b → Disjoint (interior (P a)) (interior (P b))) :
    Fintype.card ι ≤ k := by
  classical
  choose f hf using fun a => hpierce (P a) (hunit a) (hin a)
  have hinj : Function.Injective f := by
    intro a b hab
    by_contra hne
    have h1 : p (f a) ∈ interior (P a) := hf a
    have h2 : p (f a) ∈ interior (P b) := by rw [hab]; exact hf b
    exact Set.disjoint_left.mp (hdisj a b hne) h1 h2
  simpa using Fintype.card_le_of_injective f hinj

#print axioms pocket_cap
#print axioms packsBeside_compl
#print axioms ring_capacity_of_pocket_cap
#print axioms locked_crowd_free_of_pocket_cap
#print axioms one_flush_value_of_pocket_cap
#print axioms optimal_psiMin_not_stuck_of_pocket_cap
#print axioms capacity_le_of_pierce

end PackingCert.S11.OpenLemmas
