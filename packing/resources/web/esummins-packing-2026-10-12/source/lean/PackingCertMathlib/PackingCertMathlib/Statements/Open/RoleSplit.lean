import PackingCertMathlib.TopLevel

/-!
# Lemma ROLE-SPLIT — bisecting a wide named role (the logical core, proved)

**What it says** (`attempts/A211-coarse-tree/notes/coarse_tree.md` §5).  Let `N` be a node of
the clip tree carrying a role `r`, `u` one of its coordinates (`cx`, `cy`, or the tilt `t`) and
`m` a threshold.  `N_lo = N ∧ u(r) ≤ m`, `N_hi = N ∧ u(r) ≥ m`.  Then `N` is DEAD iff `N_lo` and
`N_hi` are both DEAD.  Every genuine packing gives `r` a definite pose whose coordinate is a real
number, so `u ≤ m ∨ u ≥ m`: the disjunction is exhaustive.

**What is Lean.**  Exactly that — `role_split` below is `le_total`.  What is NOT Lean: that the
child's PIECES (the parent's pieces intersected with the half-space, tilt sub-bins cut at the
exact rational midpoint) are a superset of the poses satisfying the child's hypothesis — the
emitter's clip (`rsplit211.apply_rsplit`), a sound over-approximation by construction.

**Status (2026-09-14).**  Logical core proved here; the piece-level soundness is certificate
data, as for every clip of the cascade.
-/

namespace PackingCert.S11.OpenLemmas

/-- **Lemma ROLE-SPLIT.**  If both halves of a bisection of a role's coordinate are dead, the
node is dead. -/
theorem role_split (N : Cfg → Prop) (r : Fin 11) (u : PSq → ℝ) (m : ℝ)
    (hlo : ∀ z, N z → u (z r) ≤ m → False) (hhi : ∀ z, N z → m ≤ u (z r) → False) :
    ∀ z, N z → False :=
  fun z hz => (le_total (u (z r)) m).elim (hlo z hz) (hhi z hz)

#print axioms role_split

end PackingCert.S11.OpenLemmas
