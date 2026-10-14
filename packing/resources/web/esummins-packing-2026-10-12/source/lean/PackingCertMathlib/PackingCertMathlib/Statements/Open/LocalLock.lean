import PackingCertMathlib.Crowd
import PackingCertMathlib.Selection
import PackingCertMathlib.Statements.Open.LemmaCEIL
import PackingCertMathlib.Statements.Open.TwoGrains
import PackingCertMathlib.Statements.Open.OneFlush
import PackingCertMathlib.Statements.Open.Realign

/-!
# -- OPEN: the extremal route to ONE-FLUSH(n), its exact residue LOCKED-CROWD-FREE, and the n = 11 corollary (A233)

`docs/proofs/local_lock.md`.  The PI (2026-09-15, 17:50): "an analytical reason for at least one simple square,
since that would generalise up and allow us to ignore k0 for higher n without re-searching."

**The extremal route, n-general** (`local_lock.md` §1).  Among the packings at the optimal side `s = s(n)` (a
compact set) take one minimising the TOTAL INTRUSION `Ψ = Σ_c Σ_i d_c(Q_i)`, `d_c(Q) = max(0, 1 − μ_c(Q))`,
`μ_c(Q) = inf_{p ∈ Q} max(u, v)` in the corner frame (`muC`, `depthC`, `Psi`; `nocrit_k0_blocked.md` §1 at
n = 11, the same functional at every n).  At such a packing no square RETREATS (`Retreats`: a re-placement of ONE
square at the same side that strictly lowers its depth at a corner and deepens nothing — `no_retreat_of_psiMin`,
a THEOREM).  So the optimum is attained by a packing that is either singly met at some corner (K0-FREE teleports
it to a flush corner: ONE-FLUSH(n) in its VALUE form) or a FOUR-CROWD every meeter of which is swap-locked.
Retreat-freedom is implied by LOCKED (Lemma ROT + ROT-W: a strictly opening first-order motion of one square is a
retreat), so the residue below is WEAKER than `LOCK-FREE⁺` restricted to optimal packings.

**Axiom `locked_crowd_free`** ([C], the exact residue, n-general): no optimal packing below `⌈√n⌉` is a four-crowd
all of whose meeters are retreat-free.  What is proved about it (`local_lock.md` §2–§4): LOCALITY (the lock of a
meeter is decided by its row partners, whose centres lie within `√2` of it — inside the corner ARM
`[0, 1 + 2√2]²`), Lemma RADIAL (a loaded arm is held in by a net corner-ward push from OUTSIDE it), Corollary
CHAIN (the loaded component of a crowd reaches a far wall), and — from NOCRIT-SEL — that every retreat cluster
leaves the arm once `s > 2 + 2√2`; so the residue is NOT a local problem, and the per-corner form ("no corner
is doubly met by locked meeters") is FALSE: Trump's TL corner is exactly that (`lockfree.md` §5, 5/5 LOCKED).

**Theorems.**  `one_flush_value_of_locked_crowd_free`: an optimal Ψ-minimal packing below `⌈√n⌉` has a
singly-met corner; `exists_optimal_singly_met`: ONE-FLUSH(n), value form, from the existence of a Ψ-minimal
optimal packing (compactness, [S] prose); `optimal_psiMin_not_stuck`: the n = 11 corollary (not teleport-stuck
below side 4, via `ceil_sqrt_eleven`).

**Status (2026-09-15).**  `locked_crowd_free`: axiom [C]; everything else: theorems.
-/

namespace PackingCert.S11.OpenLemmas

open Set

/-- `μ_c(Q) = inf_{p ∈ Q} max(u, v)` in the frame of corner `c` (`cframe`): the corner box `[0, μ]²` is the
largest one `Q` avoids. -/
noncomputable def muC (s : ℝ) (c : Fin 4) (Q : Set RP) : ℝ :=
  sInf ((fun p : RP => max (cframe s c p).1 (cframe s c p).2) '' Q)

/-- The intrusion depth of `Q` at corner `c`: `max(0, 1 − μ_c(Q))`; positive iff `Q` meets the open unit box. -/
noncomputable def depthC (s : ℝ) (c : Fin 4) (Q : Set RP) : ℝ := max 0 (1 - muC s c Q)

/-- The total intrusion `Ψ` of an n-family. -/
noncomputable def Psi (s : ℝ) {n : ℕ} (Q : Fin n → Set RP) : ℝ :=
  ∑ c : Fin 4, ∑ i : Fin n, depthC s c (Q i)

/-- Square `i` RETREATS at corner `c`: some packing at the same side agrees with `Q` off `i`, has a strictly
smaller depth of square `i` at `c`, and deepens no square at any corner.  A first-order ROT / ROT-W motion of
one square is a retreat, so `¬ Retreats` is implied by LOCKED. -/
def Retreats (s : ℝ) {n : ℕ} (Q : Fin n → Set RP) (c : Fin 4) (i : Fin n) : Prop :=
  ∃ Q' : Fin n → Set RP, IsPacking n s Q' ∧ (∀ j, j ≠ i → Q' j = Q j) ∧
    depthC s c (Q' i) < depthC s c (Q i) ∧
    ∀ (c' : Fin 4) (j : Fin n), depthC s c' (Q' j) ≤ depthC s c' (Q j)

/-- A `Ψ`-minimal packing at side `s` (the extremal choice; exists by compactness, [S]). -/
def PsiMin (n : ℕ) (s : ℝ) (Q : Fin n → Set RP) : Prop :=
  IsPacking n s Q ∧ ∀ Q' : Fin n → Set RP, IsPacking n s Q' → Psi s Q ≤ Psi s Q'

/-- **At a `Ψ`-minimal packing nothing retreats** (the extremal route's lock, one line). -/
theorem no_retreat_of_psiMin {n : ℕ} {s : ℝ} {Q : Fin n → Set RP} (h : PsiMin n s Q)
    (c : Fin 4) (i : Fin n) : ¬ Retreats s Q c i := by
  rintro ⟨Q', hP', -, hlt, hle⟩
  have hsum : Psi s Q' < Psi s Q := by
    unfold Psi
    apply Finset.sum_lt_sum
    · intro c' _
      exact Finset.sum_le_sum (fun j _ => hle c' j)
    · exact ⟨c, Finset.mem_univ c, Finset.sum_lt_sum (fun j _ => hle c j) ⟨i, Finset.mem_univ i, hlt⟩⟩
  exact absurd (h.2 Q' hP') (not_le.mpr hsum)

/-- **[OPEN] LOCKED-CROWD-FREE** — the exact residue of the extremal route.  No optimal packing below `⌈√n⌉` is
a four-crowd all of whose meeters are retreat-free.  Weaker than `LOCK-FREE⁺` on optimal packings; refuted for
NO n (the only fully locked frames known are at side ≥ 4.0002 at n = 11, above the optimum). -/
axiom locked_crowd_free (n : ℕ) (s : ℝ) (Q : Fin n → Set RP) (hopt : IsOptimalPacking n s Q)
    (hs : s < ((Nat.ceil (Real.sqrt (n : ℝ)) : ℕ) : ℝ)) (hcrowd : FourCrowdN s Q)
    (hlock : ∀ (c : Fin 4) (i : Fin n), MeetsCornerN s Q c i → ¬ Retreats s Q c i) : False

/-- An optimal `Ψ`-minimal packing below `⌈√n⌉` has a singly-met corner. -/
theorem one_flush_value_of_locked_crowd_free (n : ℕ) (s : ℝ) (Q : Fin n → Set RP)
    (hopt : IsOptimalPacking n s Q) (hpsi : PsiMin n s Q)
    (hs : s < ((Nat.ceil (Real.sqrt (n : ℝ)) : ℕ) : ℝ)) :
    ∃ c : Fin 4, SinglyMet s Q c := by
  by_contra hno
  have hcrowd : FourCrowdN s Q := fun c hc => hno ⟨c, hc⟩
  exact locked_crowd_free n s Q hopt hs hcrowd (fun c i _ => no_retreat_of_psiMin hpsi c i)

/-- **ONE-FLUSH(n), value form.**  If the optimum `s(n) < ⌈√n⌉` is attained by a `Ψ`-minimal packing (the
extremal route's hypothesis, compactness), some optimal packing has a singly-met corner. -/
theorem exists_optimal_singly_met (n : ℕ) (s : ℝ)
    (hex : ∃ Q : Fin n → Set RP, IsOptimalPacking n s Q ∧ PsiMin n s Q)
    (hs : s < ((Nat.ceil (Real.sqrt (n : ℝ)) : ℕ) : ℝ)) :
    ∃ (Q : Fin n → Set RP) (c : Fin 4), IsOptimalPacking n s Q ∧ SinglyMet s Q c := by
  obtain ⟨Q, hopt, hpsi⟩ := hex
  obtain ⟨c, hc⟩ := one_flush_value_of_locked_crowd_free n s Q hopt hpsi hs
  exact ⟨Q, c, hopt, hc⟩

/-- **Corollary (n = 11).**  An optimal, `Ψ`-minimal eleven-square packing below side 4 is not teleport-stuck
(then K0-FREE teleports it into a packing with a corner slot square, `no_optimal_of_kill`'s `link`). -/
theorem optimal_psiMin_not_stuck (m : ℝ) (hm : m < 4) (z : Cfg) (hz : CfgPacking m z)
    (hopt : ∀ s' : ℝ, Fits 11 s' → m ≤ s') (hpsi : PsiMin 11 m (fun i => (z i).set)) :
    ¬ TeleportStuck m z := by
  intro hst
  have hopt' : IsOptimalPacking 11 m (fun i => (z i).set) := ⟨hz.2, hopt⟩
  have h4 : m < ((Nat.ceil (Real.sqrt ((11 : ℕ) : ℝ)) : ℕ) : ℝ) := by
    rw [ceil_sqrt_eleven]
    exact_mod_cast hm
  obtain ⟨c, hc⟩ := one_flush_value_of_locked_crowd_free 11 m _ hopt' hpsi h4
  obtain ⟨i, j, hij, hi, hj⟩ := hst c
  exact hij (hc i j hi hj)

#print axioms no_retreat_of_psiMin
#print axioms locked_crowd_free
#print axioms one_flush_value_of_locked_crowd_free
#print axioms exists_optimal_singly_met
#print axioms optimal_psiMin_not_stuck

end PackingCert.S11.OpenLemmas
