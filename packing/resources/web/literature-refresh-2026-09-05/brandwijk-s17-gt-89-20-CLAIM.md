# s(17) > 89/20 — a certified lower bound for packing 17 unit squares in a square

**Claim.** `s(17) > 89/20 = 4.45`, where `s(n)` is the side of the smallest
square into which `n` unit squares pack with pairwise disjoint interiors.

## Theorem

> Let `P` be the 16 points below and let the container be `[0, 89/20]²`.
> Every **closed unit square contained in the container covers at least one
> point of `P` in its open interior.**

**Consequently `s(17) > 89/20`.** *(Pigeonhole.)* Among any 17 unit squares
with pairwise disjoint interiors packed in `[0, 89/20]²`, each covers some
point of `P` in its interior; since `|P| = 16`, two of them would cover the
**same** point in their interiors and hence overlap — impossible. So 17 unit
squares do not pack into `[0, 89/20]²`.

## The 16 points (exact rationals — never floats)

```
point  x                y
p00    995193/1000000   36877/40000
p01    989519/500000    36877/40000
p02    2962883/1000000  36877/40000
p03    3492141/1000000  36877/40000
p04    957859/1000000   1790649/1000000
p05    1487117/1000000  1790649/1000000
p06    1235481/500000   1790649/1000000
p07    3454807/1000000  1790649/1000000
p08    995193/1000000   2659351/1000000
p09    989519/500000    2659351/1000000
p10    2962883/1000000  2659351/1000000
p11    3492141/1000000  2659351/1000000
p12    957859/1000000   882019/250000
p13    1487117/1000000  882019/250000
p14    1235481/500000   882019/250000
p15    3454807/1000000  882019/250000
```

## Conventions (fixed; stated in every artifact)

- A placement is `(x, y, θ)`: centre `(x, y)`, rotation `θ`, half-extent
  `h = 1/2`, axes `a1 = (cos θ, sin θ)`, `a2 = (−sin θ, cos θ)`.
- **Coverage is strict** (open interior); therefore the *refuted* system —
  "some contained placement avoids all points" — uses **closed** (non-strict)
  avoidance atoms. Containment of the square in the container is closed.
  This is what makes the pigeonhole **survive tangencies**, which are generic
  in optimal packings.
- **Weierstrass parameterization**: `t = tan(θ/2) ∈ [0, 1]` covers
  `θ ∈ [0, π/2]` (sufficient by the square's 4-fold symmetry), with
  `c = (1 − t²)/(1 + t²)`, `s = 2t/(1 + t²)`. Every obligation is polynomial
  in `(x, y, t)` after clearing the positive denominator `d = 1 + t²` — no
  trigonometry, no algebraic numbers, **no libm in the trust chain**.

## How it is certified

An interval branch-and-bound over `(x, y, t)` in exact rational arithmetic
refutes avoidance on every box — **Certified, 60393653 boxes**. Each leaf
carries its refutation: `covered k` (point `k` lies in the open square across
the whole box) or `not-containable side` (the square cannot fit the
container). The full split tree is exported as a self-contained
`SQUAREPACK-REPLAY 1.1` proof object; completeness is **recomputed from the
splits**, never trusted. An independent verifier — one that **shares no
geometry code with the producer** (its only dependencies are `flate2` and
`num-bigint`; the rational layer is hand-rolled) — re-checks it:
`completeness: VALID`, `leaf-validity: VALID`, `checksum: VALID`,
`verdict: VALID`. Mutation controls (perturbing p0.x by +0.01, and the
container by +0.01) flip the certifier to avoidable with exact-verified
witnesses: `witness: VALID`.

That independence is stronger than it may look, and stronger than "both sides
read the same document": the verifier did **not** read a v1.1 spec, because
none existed when it was written (`git show 8594d3e:docs/replay-format.md |
grep -c "SQUAREPACK-REPLAY 1.1"` → `0`). It **reconstructed** the v1.1
semantics from first principles plus the producer's artifacts, and when the
normative spec later landed the two matched on every structural and semantic
point — including, numerically, an independently recounted leaf total of
30,196,827 against the producer's declared 30,196,827.

## Prior art (verbatim — E2 rule: verbatim or it does not exist)

Erich Friedman, *"Packing Unit Squares in Squares: A Survey and New Results"*,
Electronic J. Combinatorics **DS#7**, states:

> "Trevor Green has shown [8]: **Theorem 9.** `s(n²+1) ≥ 2√2 − 1 +
> (n(n−1)² + (n−1)√(2n))/(n²+1)`"

with unavoidable sets illustrated in **Figure 34**, whose caption reads
**`s(17) ≥ (40√2+19)/17`** — that is, `s(17) ≥ 4.44521…`.

## The improvement

`89/20 = 4.45 > (40√2+19)/17 = 4.445208382…`. To our knowledge (literature
searched 2026-07: the EJC survey DS#7 and the current square-packing bound
trackers list Green's bound as the best published *lower* bound for `s(17)` and
treat Bidwell's construction as an *upper* bound), this is the **first certified
improvement** over that best published lower bound, strictly above it by
≈ `0.0048`.

What this result actually shows, stated precisely: **Green's family contains
members stronger than the one he analyzed.** The certified point set is **not**
Green's construction. It is an optimizer-found member of the same topological
(5-parameter glide) family, reached by freeing `g` and `h` (`g < 1`, `h > 1/2`)
where his analyzed member binds the uniform-lemma constraints exactly
(`g = 1`, `h = 1/2`). The improvement is a fact about the family's interior,
not a claim about his unpublished proof — and emphatically not a suggestion
that his construction "outlived his analysis". We cannot see his proof; we can
see that the family has more in it than the member he published.

One further honesty note: this is a **lower-bound improvement, not a record**.
The record packing gives `s(17) ≤ 4.67553009360455…` (Bidwell 1998; degree-18
polynomial root, Ellsworth 2023) — a known feasible packing, not a proved
optimum — and it remains 0.225 above. Closing that gap needs new structure, not
this family: our 5-parameter glide **driver** walls between 4.45 and 4.4525,
where the fast evaluator claims a certificate at 4.4525 that the interval B&B
refutes (see `s17-glide-family-wall`). That is a statement about where this
numerical driver stops — not a proof about the family's global optimum, and the
4.4525 refutation itself did not exact-verify.

**Superseded rung:** `s17-gt-8893-2000` — `s(17) > 8893/2000`,
the first rung above Green, which this capsule supersedes.

*Verify it yourself: `reproduce.sh l2` re-checks the full proof offline; `l1` (the mutation controls) is under a second.*
