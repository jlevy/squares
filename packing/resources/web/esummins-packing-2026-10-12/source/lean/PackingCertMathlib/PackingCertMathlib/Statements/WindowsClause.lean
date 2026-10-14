import PackingCertMathlib.WindowsCore

/-!
# Theorem W — the boxed-windows clause of the case certificate

**What it says.**  A case certificate may carry, per boxed square, a finite list of
`(t, c)`-boxes (its WINDOW); the per-window walk of `checkWindowsI` then prices only the poses
inside the window, with the cores attached to OTHER windows exempt.  If the checker passes and
every window's cores are certified inside every pose of the window (`checkCoreInBox`, a
Bernstein certificate on the four corners), then no strict family at the certified side has
(H1) an injective choice of a window square per window lying in it, (H2) the unattached cores
inside their owners, and (H3) no NO-exempt square.

**Why it matters.**  It is the clause that lets a tree node's OWN hypothesis (the boxes the
tree has already established for `H` and the instantiated meeters) enter the LP: the budget
drops from `n − r` to `n − m + |att|`, which is what kills at budget 0 on a fully named page.

**How it is proved** (`Windows.lean`, `WindowsCheck.lean`, `WindowsCore.lean`,
`WindowsRound.lean`, A192; prose `docs/proofs/boxed_windows.md` Theorem W): the counting core
`count_core`, the bookkeeping `windowed_counted`, and the walk soundness `goC_box_price` with
the starting box a parameter.  What the Lean statement takes as DATA: the pieces as integer
boxes (`windowBox`, outward rounding) and the Bernstein certificates.

**For any `n`.**  Stated for the certificate's own `n`.
-/

namespace PackingCert.S11

open Set MeasureI CaseI WindowsW LocalCertT

/-- **Theorem W for a PASS**, with (V3) discharged by `checkCoreInBox` on every piece of every
window that carries a core. -/
theorem windows_clause_kill {C : CCertW} (h : checkWindowsI C = true)
    (certs : Fin C.windows.length → IBox → List (List (List Poly)))
    (hV3 : ∀ i (j : Fin C.c.cores.length), (C.windows.get i).core = some (j : ℕ) →
      ∀ b ∈ (C.windows.get i).pieces,
        checkCoreInBox (mkCtx (toMCert C.c)) (C.c.cores.get j) b (certs i b) = true)
    {Q : Fin C.c.n → Set RP} (hQ : IsStrictFamily C.c.n (caseSide C.c) Q)
    (σ : Fin C.windows.length → Fin C.c.n) (hσ : Function.Injective σ)
    (hH1 : ∀ i, WinSet (mkCtx (toMCert C.c)) (C.windows.get i) (Q (σ i)))
    (own : Fin C.c.cores.length → Fin C.c.n)
    (hH2 : ∀ j : Fin C.c.cores.length, (∀ i, (C.windows.get i).core ≠ some (j : ℕ)) →
      coreSet (C.c.cores.get j) ⊆ Q (own j))
    (hH3 : ∀ k, ¬ CaseExempt C.c (Q k)) : False :=
  checkWindowsI_kill_of_check h certs hV3 hQ σ hσ hH1 own hH2 hH3

#print axioms windows_clause_kill

end PackingCert.S11
