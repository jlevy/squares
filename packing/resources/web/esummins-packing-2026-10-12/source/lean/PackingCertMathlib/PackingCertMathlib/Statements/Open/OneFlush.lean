import PackingCertMathlib.Crowd
import PackingCertMathlib.Selection
import PackingCertMathlib.Statements.Open.LemmaCEIL
import PackingCertMathlib.Statements.Open.TwoGrains

/-!
# -- OPEN: Conjecture ONE-FLUSH (n-general) and its n = 11 corollary (A226)

`docs/proofs/one_flush.md`.  The PI (2026-09-14, 23:40): "for the k0 exclusion to work at any n it must be
something invalid about the IDEA of packing n into side < ⌈√n⌉: at least one corner can always be teleported
to flush."

**Conjecture ONE-FLUSH(n)** (`one_flush.md` §1, [C]).  Let `n` be such that `s(n) < ⌈√n⌉`.  Every OPTIMAL
packing of `n` unit squares (side `s = s(n)`) has a corner whose open unit corner box is met, in the
interior, by AT MOST ONE square -- so Lemma K0-FREE (`Selection.teleport_packing`) teleports that square to
the corner slot and the optimum is attained in the class of packings with a FLUSH corner.  Stated here as the
axiom `one_flush` over the n-general packing predicate `IsPacking n s Q` (`Parametrize.lean`), with
optimality `IsOptimalPacking` = no packing of `n` squares at a smaller side (`Fits`).

**Why OPTIMAL and not "every packing below ⌈√n⌉"** (`one_flush.md` §3, [T]+[M]).  The all-packings form
(STUCK(n): no teleport-stuck packing at any side `< ⌈√n⌉`, A223's `click_down` ⟺ STUCK-4 at n = 11) is
FALSE in general: Proposition CROWD-ABOVE builds, from any packing whose four corners carry a flush
corner square with a flush along-wall neighbour (a corner DOMINO), a packing at EVERY larger side with all
four corner boxes doubly met (slide the corner square `ε` up its wall, tilt the neighbour by `ε/2` so its
vertex pokes under it, shift the rest by `(ε, ε)`); verified as packings at sides strictly below `⌈√n⌉` for
n = 26, 28, 29, 37, 40, 50, 51, 55 (`attempts/A226-one-flush/results/crowd226.md`).  Only the optimal form
has content, and at n = 11 it is exactly the k0_00 obligation on `[3.82, ŝ]`.

**Survey** (`one_flush.md` §2, [M]): every best-known packing below `⌈√n⌉` (n = 5, 10, 11, 17, 18, 19,
26-29, 37-41, 50-55; Ellsworth's page, 2026-09-14) has at least THREE flush corners; all but Trump's
n = 11 have FOUR.  The PI's second conjecture ("no non-trivial optimal packing has four flush corners") is
therefore FALSE: n = 5 and n = 10 (Göbel, both PROVED optimal) have four flush corners.  No axiom for it.

**Corollary (n = 11)** (`optimal_not_stuck`, a theorem): an optimal packing of eleven squares at side
`m < 4` is not teleport-stuck (`TwoGrains.TeleportStuck`); with `ceil_sqrt_eleven` from `LemmaCEIL.lean`.
`no_optimal_of_kill`: with K0-FREE's exchange (`link`, A223's O-LINK) and the k1-a kill of the k1_00 tree (no
packing at side `m` contains a corner slot square) as hypotheses, no optimal packing exists at `m < 4` -- the
value part of the k0_00 route (`k0_route.md` §3, `ring_swap.md` §1.7), pure logic over `one_flush`.

**Status (2026-09-14).**  `one_flush`: axiom [C]; `optimal_not_stuck`, `no_optimal_of_kill`: theorems.
-/

namespace PackingCert.S11.OpenLemmas

open Set

/-- Square `Q i` of an n-family MEETS the open unit corner box of corner `c` at side `s`. -/
def MeetsCornerN (s : ℝ) {n : ℕ} (Q : Fin n → Set RP) (c : Fin 4) (i : Fin n) : Prop :=
  ¬ Disjoint (interior (cornerBox s 1 c)) (interior (Q i))

/-- Corner `c` is SINGLY MET: at most one square of the family meets its open box. -/
def SinglyMet (s : ℝ) {n : ℕ} (Q : Fin n → Set RP) (c : Fin 4) : Prop :=
  ∀ i j, MeetsCornerN s Q c i → MeetsCornerN s Q c j → i = j

/-- An OPTIMAL packing of `n` unit squares: a packing at side `s` such that no packing of `n` unit
squares exists at any smaller side. -/
def IsOptimalPacking (n : ℕ) (s : ℝ) (Q : Fin n → Set RP) : Prop :=
  IsPacking n s Q ∧ ∀ s' : ℝ, Fits n s' → s ≤ s'

/-- **[OPEN] Conjecture ONE-FLUSH.**  An optimal packing of `n` unit squares at a side below `⌈√n⌉` has a
singly-met corner (which K0-FREE then teleports to a flush corner). -/
axiom one_flush (n : ℕ) (s : ℝ) (Q : Fin n → Set RP) (hopt : IsOptimalPacking n s Q)
    (hs : s < ((Nat.ceil (Real.sqrt (n : ℝ)) : ℕ) : ℝ)) :
    ∃ c : Fin 4, SinglyMet s Q c

/-- **Corollary (n = 11).**  An optimal eleven-square packing below side 4 is not teleport-stuck. -/
theorem optimal_not_stuck (m : ℝ) (hm : m < 4) (z : Cfg) (hz : CfgPacking m z)
    (hopt : ∀ s' : ℝ, Fits 11 s' → m ≤ s') : ¬ TeleportStuck m z := by
  intro hst
  have hopt' : IsOptimalPacking 11 m (fun i => (z i).set) := ⟨hz.2, hopt⟩
  have h4 : m < ((Nat.ceil (Real.sqrt ((11 : ℕ) : ℝ)) : ℕ) : ℝ) := by
    rw [ceil_sqrt_eleven]
    exact_mod_cast hm
  obtain ⟨c, hc⟩ := one_flush 11 m _ hopt' h4
  obtain ⟨i, j, hij, hi, hj⟩ := hst c
  exact hij (hc i j hi hj)

/-- **The value route at n = 11.**  ONE-FLUSH plus K0-FREE in its Lean-consumable form (`link`: a packing
that is not teleport-stuck exchanges, at the same side, into one containing a corner slot square -- this is
`teleport_packing` plus the identity of `cornerBox m 1 c` with the slot box of `⟨c, 0, 0⟩`, A223's routine
obligation O-LINK, taken as a hypothesis here) plus the k1-a kill (no packing at side `m` contains a corner
slot square; the k1_00 tree) leaves no OPTIMAL packing at side `m < 4`.  Pure logic. -/
theorem no_optimal_of_kill (m : ℝ) (hm : m < 4)
    (link : ∀ z : Cfg, CfgPacking m z → ¬ TeleportStuck m z →
      ∃ z' : Cfg, CfgPacking m z' ∧ ∃ c : Fin 4, ContainsPins {⟨c, 0, 0⟩} m z')
    (kill : ∀ (c : Fin 4) (z : Cfg), CfgPacking m z → ¬ ContainsPins {⟨c, 0, 0⟩} m z) :
    ∀ z : Cfg, CfgPacking m z → ¬ (∀ s' : ℝ, Fits 11 s' → m ≤ s') := by
  intro z hz hopt
  obtain ⟨z', hz', c, hc⟩ := link z hz (optimal_not_stuck m hm z hz hopt)
  exact kill c z' hz' hc

#print axioms one_flush
#print axioms optimal_not_stuck
#print axioms no_optimal_of_kill

end PackingCert.S11.OpenLemmas
