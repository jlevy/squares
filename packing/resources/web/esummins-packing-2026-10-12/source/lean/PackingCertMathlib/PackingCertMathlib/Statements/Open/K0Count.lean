import PackingCertMathlib.Sideband

/-!
# -- OPEN: Lemma PUSH — the two meeters of an open corner push each other OUT (A218)

**What it asserts** (`docs/proofs/k0_count.md` §2, any `n`, any side).  Let `q₁`, `q₂` be unit
squares in the closed quadrant `{u ≥ 0, v ≥ 0}` of a corner, both meeting the OPEN unit corner
box `(0, 1)²`, and let the line `{n·x = β}` (unit normal `n`) weakly separate them with `q₁` on
the `≤ β` side — so that at a Fritz-John point the contact force of `q₁` on `q₂` is a positive
multiple of `n`.  Then

* (i) `n` has a strictly positive component: `0 < n_u ∨ 0 < n_v` — the push is never TOWARD the
  corner in both coordinates (proof: otherwise `m = −n ≥ 0` and Lemma B0′ of `sideband.md` §3
  gives `max_{q₂} m·x ≥ m_u + m_v > m·p` for every `p ∈ (0,1)²`, against `q₁ ∋ p` on the far side);
* (ii) if `q₂` touches the floor `v = 0` then `0 < n_u` — the push is AWAY from the corner ALONG
  the touched wall; mirror for the wall `u = 0` (proof: with `n = (−sin α, cos α)` the separating
  line `ℓ` meets the floor at `u₀ ≥ sin α` (Lemma B0 on `q₂`'s support toward `ℓ`) and `q₁`, in
  the wedge under `ℓ`, has every point at `u ≥ u₀ + cos² α / sin α` (the mirror of B0 on `q₁`),
  so `q₁ ⊆ {u ≥ 1/sin α} ⊆ {u ≥ 1}` and cannot meet the open box).

Consequence (Lemma HOLD, prose): at a Fritz-John point a corner meeter pressed by its partner
needs a HOLDER — a third square pushing it toward the corner, along its wall if it touches one.
The count "8 meeters + 4 holders = 12 > 11" that A217 conjectured does NOT follow: the holders
may be meeters of the adjacent corners (the force-balanced ring `rand_0_0569|t20`, nine squares,
only the tilt bound loaded) and the meeters may carry no load at all (rattler crowds: 61 of 70
doubly-met corners at the genuine k0 FJ points).  See `docs/proofs/k0_count.md` §4–5.

**Status (2026-09-14).**  [T] in prose (`k0_count.md` §2, both clauses); measured 10,638 / 10,638
loaded partner pushes on A217's 2,732 witnesses.  Lean obligation: Lemmas B0 / B0′ (and B0's
mirror) as `wrel`-type inequalities (the same obligation as `SecondMeeterCriterion`,
`sideband.md` §5 (ii)) plus the centre bound `(F2)` in its sharp form `cx ≥ (cos θ + sin θ)/2`.
-/

namespace PackingCert.S11.OpenLemmas

open Set

/-- The line `{n·x = β}` with unit normal `n` weakly separates `q₁` (on the `≤ β` side) from
`q₂` (on the `≥ β` side). -/
def Separates (n : RP) (β : ℝ) (q₁ q₂ : PSq) : Prop :=
  n.1 ^ 2 + n.2 ^ 2 = 1 ∧ (∀ p ∈ q₁.set, n.1 * p.1 + n.2 * p.2 ≤ β) ∧
    (∀ p ∈ q₂.set, β ≤ n.1 * p.1 + n.2 * p.2)

/-- **[OPEN] Lemma PUSH.**  Two meeters of the open unit corner box, both in the quadrant,
separated by `{n·x = β}`: the normal pointing into the second one has a positive component,
and a positive component along any corner wall the second one touches. -/
axiom lemma_PUSH (q₁ q₂ : PSq) (h1 : q₁.t ∈ Icc (0 : ℝ) 1) (h2 : q₂.t ∈ Icc (0 : ℝ) 1)
    (hq1 : InQuadrant q₁) (hq2 : InQuadrant q₂) (hm1 : Meets q₁ 1) (hm2 : Meets q₂ 1)
    {n : RP} {β : ℝ} (hsep : Separates n β q₁ q₂) :
    (0 < n.1 ∨ 0 < n.2) ∧
      ((∃ p ∈ q₂.set, p.2 = 0) → 0 < n.1) ∧ ((∃ p ∈ q₂.set, p.1 = 0) → 0 < n.2)

#print axioms lemma_PUSH

end PackingCert.S11.OpenLemmas
