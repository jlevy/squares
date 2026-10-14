import PackingCertMathlib.Dilation

/-!
# The λ-dilation bridge — Lemma B and K0-WIDEN

**What it says.**  A packing (closed unit squares, pairwise disjoint INTERIORS — contacts
allowed) at side `m` becomes, after scaling every CENTRE by `λ > 1` and keeping sizes and
tilts, a family of pairwise disjoint CLOSED squares inside `[0, λm]²` (`dilation_bridge`).
Hence a certificate that refutes every such strict family at a rational side `s″` ("no strict
family at `s″` has its designated owners containing the cores") refutes every packing at
`m = s″/λ` whose dilate satisfies the core-containment hypothesis (`lemma_B`).  The
book-keeping lemma `pullback_mem_Icc` records how a zone coordinate of the dilated family is
pulled back: into the OUTWARD-widened interval `[x₀ − (λ−1)x₁, x₁]` — this widening is
Lemma K0-WIDEN, the pad every page hypothesis has to carry (`docs/proofs/k0_route.md` §4.1).

**Why it matters.**  Every case-LP certificate (`verify_case.py`, `checkCaseI`) speaks about
pairwise-disjoint closed squares at ONE rational side, while the theorem quantifies over
interior-disjoint packings at every side of a window.  Lemma B is the only place the two
meet; it also says exactly what an `s₀`-only certificate does and does not reach
(`docs/proofs/closed_disjoint_bridge.md` B.1–B.4).

**For any `n`.**  `dilation_bridge` is stated for every `n`; `lemma_B` for `n = 11` only
because its consumer is.
-/

namespace PackingCert.S11

open Set

/-- **Lemma B.0 — the dilation bridge.**  Scaling centres by `λ > 1` turns an interior-disjoint
packing at side `m` into a strict (closed-disjoint) family at side `λm`. -/
theorem dilation_bridge_stmt {n : ℕ} {m lam : ℝ} (hlam : 1 < lam) {z : Fin n → PSq}
    (ht : ∀ i, (z i).t ∈ Icc (0 : ℝ) 1)
    (hP : IsPacking n m fun i => (z i).set) :
    IsStrictFamily n (lam * m) fun i => (scaleC lam (z i)).set :=
  dilation_bridge hlam ht hP

/-- **Lemma B.**  A bridged certificate claim at side `s″ = λm` kills every packing at side `m`
whose dilate realises the core-containment hypothesis. -/
theorem lemma_B_stmt {m lam s'' : ℝ} (hlam : 1 < lam) (hs : s'' = lam * m)
    {z : Fin 11 → PSq} (ht : ∀ i, (z i).t ∈ Icc (0 : ℝ) 1)
    (hP : IsPacking 11 m fun i => (z i).set)
    {r : ℕ} (K : Fin r → Set RP) (own : Fin r → Fin 11)
    (hcert : ∀ Q : Fin 11 → Set RP, IsStrictFamily 11 s'' Q →
      (∀ j, K j ⊆ interior (Q (own j))) → False)
    (hH : ∀ j, K j ⊆ interior ((scaleC lam (z (own j))).set)) : False :=
  lemma_B hlam hs ht hP K own hcert hH

/-- **Lemma K0-WIDEN (B.2″).**  A dilated coordinate in `[x₀, x₁]` pulls back to
`[x₀ − (λ−1)x₁, x₁]`: zones transfer OUTWARD-widened, never sharper. -/
theorem k0_widen_stmt {lam x0 x1 c : ℝ} (hlam : 1 ≤ lam) (h0 : 0 ≤ x0) (h01 : x0 ≤ x1)
    (hc : lam * c ∈ Icc x0 x1) : c ∈ Icc (x0 - (lam - 1) * x1) x1 :=
  pullback_mem_Icc hlam h0 h01 hc

#print axioms dilation_bridge_stmt
#print axioms lemma_B_stmt
#print axioms k0_widen_stmt

end PackingCert.S11
