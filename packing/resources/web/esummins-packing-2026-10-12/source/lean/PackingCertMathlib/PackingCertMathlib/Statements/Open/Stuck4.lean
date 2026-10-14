import PackingCertMathlib.Statements.Open.LocalLock
import PackingCertMathlib.Statements.Open.OneFlush
import PackingCertMathlib.Statements.Open.Realign
import PackingCertMathlib.Statements.Open.TwoGrains

/-!
# -- OPEN: STUCK-4(11) -- no teleport-stuck LOCKED packing of eleven squares below side 4 (A242)

`attempts/A242-crowd-root/notes/crowd242.md`.  The PI (2026-09-16, 15:00): "given those results, is
there any way we can show that no stable k0 packing exists below the trivial side?"  "Stable" is
A233's LOCKED = retreat-free (`local_lock.md` §1.1: a strictly opening first-order motion of one
square is a RETREAT, so `¬ Retreats` is implied by LOCKED and rattler meeters are excluded).

**The statement.**  `stuck4_eleven` [C]: no packing of eleven unit squares at a side `m < 4` is
both TELEPORT-STUCK (all four corner boxes doubly met -- `FourCrowdN`, K0-FREE′ of `k0_route.md`
§3) and LOCKED (no meeter retreats).  It is strictly stronger than `locked_crowd_free` at `n = 11`:
it drops the optimality hypothesis, so it does not select a minimiser.

**Why it closes k0_00 for the value.**  Take the side `m < 4` and a Ψ-minimal packing there
(compactness, [S]).  Nothing retreats at it (`no_retreat_of_psiMin`, a THEOREM), so if it were
teleport-stuck it would be a locked four-crowd -- excluded by `stuck4_eleven`.  Hence some corner
is singly met, K0-FREE exchanges it, at the SAME side, into a packing containing a corner slot
square (`link`, A223's routine obligation O-LINK = `teleport_packing`), and the k1_00 tree's
(k1-a) kills that (`kill`).  So no packing of eleven squares exists at `m`: `no_optimal_of_stuck4`.
The chain is the one `no_optimal_of_kill` runs on the ONE-FLUSH axiom, with `stuck4_eleven` in
place of `one_flush` and `PsiMin` supplying the singly-met corner.

**What A242 proved towards it** (`notes/crowd242.md`): the CROWD ROOT `H_B` as a cell over each of
four side bands, the leaf L1 = NO-ROOM(m = 3) over the eight meeters' CORES (A189 Lemma 1, A221
POCKET-DEAD / POCKET-INHERIT, A209 CN -- sound for every packing, locked or not), and the measured
price of the cascade.  `stuck4_eleven` is an AXIOM here: the cascade closed no band.

**Status (2026-09-16).**  `stuck4_eleven`: axiom [C].  Everything else: theorems.
-/

namespace PackingCert.S11.OpenLemmas

open Set

/-- LOCKED, as the cascade's root uses it: no meeter of any corner retreats (A233's retreat-freedom,
which `Retreats` defines and which LOCKED implies). -/
def RetreatFreeCrowd (s : ℝ) {n : ℕ} (Q : Fin n → Set RP) : Prop :=
  ∀ (c : Fin 4) (i : Fin n), MeetsCornerN s Q c i → ¬ Retreats s Q c i

/-- **[OPEN] STUCK-4-UNLOCKED(11)** -- the PI's addendum (2026-09-16, 15:40): *"is it possible to show
that no ring is constructable below `ŝ`, so no fully pinned k0 configuration exists below `ŝ`?"*  No
packing of eleven unit squares at a side below 4 is a four-crowd AT ALL.  This is the form A242's leaf
L1 would deliver, because L1 reads no lock and no force hypothesis: it is the container minus the eight
meeters' CORES against three free squares, so a cell it kills is killed for every packing of that cell,
locked or not (`notes/crowd242.md` §1.3, §2).  Strictly stronger than `stuck4_eleven`; with K0-FREE it
closes k0_00 with no selection and no A233 (`no_packing_of_stuck4`). -/
axiom stuck4_unlocked_eleven (m : ℝ) (hm : m < 4) (Q : Fin 11 → Set RP) (hP : IsPacking 11 m Q)
    (hcrowd : FourCrowdN m Q) : False

/-- **[OPEN] STUCK-4(11)** -- the PI's "no stable k0 packing below the trivial side".  No packing of
eleven unit squares at a side below 4 is a four-crowd all of whose meeters are retreat-free. -/
axiom stuck4_eleven (m : ℝ) (hm : m < 4) (Q : Fin 11 → Set RP) (hP : IsPacking 11 m Q)
    (hcrowd : FourCrowdN m Q) (hlock : RetreatFreeCrowd m Q) : False

/-- STUCK-4(11) gives LOCKED-CROWD-FREE at `n = 11` with no optimality hypothesis: the axiom
`locked_crowd_free 11` is a consequence, not an extra assumption. -/
theorem locked_crowd_free_eleven (m : ℝ) (Q : Fin 11 → Set RP) (hopt : IsOptimalPacking 11 m Q)
    (hm : m < 4) (hcrowd : FourCrowdN m Q) (hlock : RetreatFreeCrowd m Q) : False :=
  stuck4_eleven m hm Q hopt.1 hcrowd hlock

/-- A Ψ-minimal eleven-square packing below side 4 is not teleport-stuck.  (`no_retreat_of_psiMin`
supplies LOCKED; `stuck4_eleven` excludes the locked four-crowd.  No optimality is used.) -/
theorem psiMin_not_stuck (m : ℝ) (hm : m < 4) (z : Cfg) (hz : CfgPacking m z)
    (hpsi : PsiMin 11 m (fun i => (z i).set)) : ¬ TeleportStuck m z := by
  intro hst
  have hcrowd : FourCrowdN m (fun i => (z i).set) := by
    intro c hsm
    obtain ⟨i, j, hij, hi, hj⟩ := hst c
    exact hij (hsm i j hi hj)
  exact stuck4_eleven m hm _ hz.2 hcrowd (fun c i _ => no_retreat_of_psiMin hpsi c i)

/-- A Ψ-minimal eleven-square packing below side 4 has a SINGLY-MET corner (the shape K0-FREE
consumes). -/
theorem psiMin_singly_met (m : ℝ) (hm : m < 4) (z : Cfg) (hz : CfgPacking m z)
    (hpsi : PsiMin 11 m (fun i => (z i).set)) :
    ∃ c : Fin 4, SinglyMet m (fun i => (z i).set) c := by
  by_contra hno
  push_neg at hno
  refine psiMin_not_stuck m hm z hz hpsi (fun c => ?_)
  have h := hno c
  simp only [SinglyMet] at h
  push_neg at h
  obtain ⟨i, j, hi, hj, hij⟩ := h
  exact ⟨i, j, hij, hi, hj⟩

/-- Dropping the lock hypothesis is a weakening: STUCK-4-UNLOCKED implies STUCK-4. -/
theorem stuck4_of_unlocked (m : ℝ) (hm : m < 4) (Q : Fin 11 → Set RP) (hP : IsPacking 11 m Q)
    (hcrowd : FourCrowdN m Q) (_hlock : RetreatFreeCrowd m Q) : False :=
  stuck4_unlocked_eleven m hm Q hP hcrowd

/-- **[unlocked form]** No eleven-square packing below side 4 is teleport-stuck -- no `Ψ`-minimality, no
optimality, no lock. -/
theorem not_stuck_of_unlocked (m : ℝ) (hm : m < 4) (z : Cfg) (hz : CfgPacking m z) :
    ¬ TeleportStuck m z := by
  intro hst
  refine stuck4_unlocked_eleven m hm _ hz.2 (fun c hsm => ?_)
  obtain ⟨i, j, hij, hi, hj⟩ := hst c
  exact hij (hsm i j hi hj)

/-- **[unlocked form] k0_00, closed directly.**  With STUCK-4-UNLOCKED(11), K0-FREE (`link`) and the
k1_00 tree's kill (`kill`), NO eleven-square packing exists at a side `m < 4` at which `kill` holds --
`ŝ` and below, where (k1-a) is available.  No minimiser is selected anywhere in the chain. -/
theorem no_packing_of_stuck4 (m : ℝ) (hm : m < 4)
    (link : ∀ z : Cfg, CfgPacking m z → ¬ TeleportStuck m z →
      ∃ z' : Cfg, CfgPacking m z' ∧ ∃ c : Fin 4, ContainsPins {⟨c, 0, 0⟩} m z')
    (kill : ∀ (c : Fin 4) (z : Cfg), CfgPacking m z → ¬ ContainsPins {⟨c, 0, 0⟩} m z)
    (z : Cfg) (hz : CfgPacking m z) : False := by
  obtain ⟨z', hz', c, hc⟩ := link z hz (not_stuck_of_unlocked m hm z hz)
  exact kill c z' hz' hc

/-- **The k0_00 consequence, for the value.**  With STUCK-4(11), K0-FREE in its Lean-consumable
form (`link`) and the k1_00 tree's kill (`kill`), no eleven-square packing exists at a side `m < 4`
that carries a Ψ-minimal packing.  Pure logic on top of `psiMin_not_stuck`. -/
theorem no_optimal_of_stuck4 (m : ℝ) (hm : m < 4)
    (hex : ∃ z : Cfg, CfgPacking m z ∧ PsiMin 11 m (fun i => (z i).set))
    (link : ∀ z : Cfg, CfgPacking m z → ¬ TeleportStuck m z →
      ∃ z' : Cfg, CfgPacking m z' ∧ ∃ c : Fin 4, ContainsPins {⟨c, 0, 0⟩} m z')
    (kill : ∀ (c : Fin 4) (z : Cfg), CfgPacking m z → ¬ ContainsPins {⟨c, 0, 0⟩} m z) :
    False := by
  obtain ⟨z, hz, hpsi⟩ := hex
  obtain ⟨z', hz', c, hc⟩ := link z hz (psiMin_not_stuck m hm z hz hpsi)
  exact kill c z' hz' hc

#print axioms stuck4_unlocked_eleven
#print axioms stuck4_eleven
#print axioms stuck4_of_unlocked
#print axioms not_stuck_of_unlocked
#print axioms no_packing_of_stuck4
#print axioms locked_crowd_free_eleven
#print axioms psiMin_not_stuck
#print axioms psiMin_singly_met
#print axioms no_optimal_of_stuck4

end PackingCert.S11.OpenLemmas
