import PackingCertMathlib.CaseBridge

/-!
# V.CASE — soundness of the case-LP certificate verifier

**What it says.**  `checkCaseI` is the decision core of `verify_case.py` (the atomic measure,
the cores, the NO-families, the budget) written as a Lean `Bool` function over exact integer
interval arithmetic.  If it returns `true` on a certificate `c` with no NO-families, then NO
family of `c.n` pairwise-disjoint closed unit squares inside `[0, side(c)]²` has its designated
owner squares containing the `r` cores (`checkCaseI_kill`).  With NO-families the conclusion is
the B-NO form: some non-owner square is NO-exempt (`checkCaseI_no_family`).

**Why it matters.**  This is the bridged claim `hcert` that Lemma B (`Statements/Dilation.lean`)
needs, produced per PASS file — the meaning of every kill leaf of every class tree.  A kill
certificate is a `Bool` fact about a file plus this theorem; no prose enters.

**How it is proved** (`CaseChecker.lean`, `CaseSat.lean`, `CaseHyp.lean`, `CaseBridge.lean`,
A70): SAT sufficiency for two squares (geometric Hahn–Banach + the 4-cone support bound),
exemption-test soundness, the pricing claim (P2) of the frozen spec
(`docs/specs/case_lp_certificate_v1.md`) scaled by `wd`, and the pricing pigeonhole.  One
certificate is replayed end to end in `CaseK506.lean` (`k5_06` at `s = 191/50`).

**For any `n`.**  Stated for the certificate's own `c.n`; nothing is specific to `11`.
-/

namespace PackingCert.S11

open Set MeasureI CaseI

/-- **V.CASE, kill form.**  A passing certificate with no NO-families refutes every strict
family whose owners contain the cores. -/
theorem case_verifier_kill {c : CCertI} (h : checkCaseI c = true) (hno : c.nofams = [])
    {Q : Fin c.n → Set RP} (hQ : IsStrictFamily c.n (caseSide c) Q)
    (own : Fin c.cores.length → Fin c.n)
    (hown : ∀ j : Fin c.cores.length, coreSet (c.cores.get j) ⊆ Q (own j)) :
    False :=
  checkCaseI_kill h hno hQ own hown

/-- **V.CASE, B-NO form.**  With NO-families some non-owner is NO-exempt. -/
theorem case_verifier_no_family {c : CCertI} (h : checkCaseI c = true)
    {Q : Fin c.n → Set RP} (hQ : IsStrictFamily c.n (caseSide c) Q)
    (own : Fin c.cores.length → Fin c.n)
    (hown : ∀ j : Fin c.cores.length, coreSet (c.cores.get j) ⊆ Q (own j)) :
    ∃ i : Fin c.n, (∀ j, own j ≠ i) ∧ CaseExempt c (Q i) :=
  checkCaseI_no_family h hQ own hown

#print axioms case_verifier_kill
#print axioms case_verifier_no_family

end PackingCert.S11
