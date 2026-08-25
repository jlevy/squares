---
type: is
id: is-01m0vxmhjdsq7rdy94g9pxx3nx
title: "TUTORIAL: add a precision section—which arithmetic regime to use where, and what it costs"
kind: task
status: closed
priority: 1
version: 6
spec_path: explorations/packing/docs/project/reviews/review-2026-08-25-tutorial-pedagogy-and-accuracy.md
labels: []
dependencies:
  - type: blocks
    target: is-01m0vxns5mzy4axt8mdrhaachj
parent_id: is-01m0vxe4ntpat4xcagtf04c37z
created_at: 2026-08-25T07:37:26.861Z
updated_at: 2026-08-25T08:29:43.768Z
closed_at: 2026-08-25T08:29:43.768Z
close_reason: "Implemented in TUTORIAL.md on claude/packing-tutorial-review-r2p25t (82c68dc), on top of the SVG toolkit and the #31 frontier-assurance branch. Notation card (new §10) and vocabulary card rebuilt; the LP written out with an on-ramp; the quench's two loops described with the path-dependence reason; precision costs, latency budgets and the 1e-11 cause added; the primitive element theorem answered; §11 further reading and arithmetic inventory added; assurance and method tokens aligned to witnesses/witness.schema.yaml; accuracy fixes applied. TR-2 needed no work — #31 had already replaced the superseded absolute. The restated gate step count was removed rather than corrected, so it cannot drift a fourth time; the status-document half stays open as think-4b9m."
resolution: null
duplicate_of: null
---
§5 argues that exactness is not optional and describes the `ℚ(α)` machinery, but it
never tells a reader *what precision to work at*, how the regimes relate to hardware, or
what each costs. The evidence-tier table names `f64_screen`, `polished`, and `exact`
without saying what arithmetic sits behind each.
The material to answer this already exists in the directory and is not in the tutorial.

## Four regimes, not two

The tutorial reads as a binary—float versus exact. There are four, and the third and
fourth are routinely conflated:

1. **Hardware `f64`.** Machine epsilon `2.2e-16`. Screening and search.
2. **`f64` with an error bound, or outward-rounded intervals.** Can prove strict
   separation when the enclosure clears zero; *never* proves equality.
3. **Arbitrary-precision floating point.** Hundreds to thousands of digits.
   §5 already relies on it—"high-precision Newton followed by an integer relation
   algorithm", and `cases.kingbird29.verify_svg` is a 160-digit reconstruction—but never
   names it as a distinct regime or says the thing that matters: **more digits is still
   not exactness.** A degree-8 relation holding to 500 digits is, in §5's own words,
   "overwhelming evidence and zero proof."
4. **Exact `ℚ(α)`.** Equality is decidable. The only tier permitted to say *record*.

## The architectural fact that makes this cheap, and is missing

From `research-2026-08-22-infrastructure-for-packing-exploration.md`: every quantity the
separating-axis test evaluates is a **polynomial** in the configuration variables—four
candidate axes, eight dot products per axis, no divisions and no square roots.
So one implementation is correct over `f64`, over intervals, and over an exact field;
only the scalar type changes. That is why `verify_packing(..., sign=exact_sign)` and
`sign=float_sign(1e-9)` share one predicate, and it is the reason "work exactly" is an
affordable policy rather than a rewrite.
The tutorial calls the verifier "generic over its scalar type" in §6 without ever saying
why that genericity is available.

## The measured answer to "how much does exactness cost"

| Operation | Cost |
| --- | --- |
| Separating-axis pair test, Rust `f64` | 57 ns |
| Same test, Python float backend | 2,726 ns |
| `ℚ(α)` multiplication, degree 8 (`s(11)`), pure Python | 215.5 µs |
| Same, python-flint | 1.2 µs |
| `ℚ(α)` multiplication, degree 62, pure Python | 13 ms |
| Full exact verification of Trump's packing, 55 pairs, pure Python | 0.35 s |

Two readings the tutorial should carry.
**Exactness is free where it is used.** A complete exact verification costs 0.35 s
against a model turn of seconds, so optimising it is optimising noise.
**The cost is not uniform.** The exact-versus-float ratio grows with algebraic degree
(177× at degree 8, 578× at degree 62), so exact arithmetic is worst exactly where the
problem is hardest, and that is the constraint on ever putting exact arithmetic inside a
search loop.

The framing that makes this concrete is the three latency tiers: an agent tier (1–10 s
per operation, genuinely free), an interactive tier (10 ms – 1 s), and an inner loop
(10 ns – 1 µs executed `1e9`–`1e12` times). Exact arithmetic belongs in the first two;
the third is `f64` and always will be.

## The `1e-11` floor is not a hardware limit, and the tutorial invites the wrong reading

§5 and §8 give the `polished` tier "a floor of about `1e-11` in the side" with no cause.
A reader who knows `f64` will assume machine epsilon and be wrong by five orders.
It is the **LP solver's feasibility tolerance**, pinned at HiGHS's strictest `1e-10`
([D-021](defects.md)); at the default `1e-7` the solver returned a packing violating its
own separation constraint by `9.876e-08`, and so a side below Trump's
([D-014](defects.md)). The quench nonetheless reaches `1.33e-15` at `n = 10`—near
machine precision—so the floor is what the tier *guarantees*, not what runs achieve.
The fix is an exact LP over rational or algebraic coefficients, which is unbuilt.
Saying this ties §5, §6, and §8 together; at present each states a piece.

## And the reproducibility consequence

§8's open item 6—the same seed reaching a different endpoint under a different
toolchain—is a *consequence* of operating a degenerate LP in `f64`, not an unrelated
engineering complaint. It belongs next to the precision discussion.

## Proposal

A short subsection in §5, before "The number field": the four regimes, what each can
decide, what each costs, and the rule for which to use where—screen in `f64`, refine in
`f64`, decide in `ℚ(α)`, and never let a number cross a tier boundary.
Numbers stay owned by `SYNOPSIS.md` and the infrastructure report; the tutorial cites
them.

## Notes

Scope NARROWED by PR #31. Its "Assurance, method, and precision" section resolves the
classification half of this bead, and does it better than the bead proposed: assurance
is separated from method and from actual precision/tolerance, and it states outright
that "A numerical result remains numerical at tolerance 1e-100" — which was this bead's
third regime, arbitrary-precision floating point, the one the tutorial used to collapse
into "exact".

REMAINING scope, three parts:
1. Costs are still absent. No figure in the document, so a reader cannot answer "what
   precision should I work at" for their own task. The table in the bead body stands
   (57 ns / 2,726 ns / 215.5 us / 1.2 us / 13 ms / 0.35 s), as does the
   exact-to-float ratio growing with degree (177x at 8, 578x at 62) and the three
   latency tiers.
2. The 1e-11 floor still has no cause. §8 item 5 now reads "What a floating LP result
   means below 1e-11" and says only that the solver has a noise floor there. It is
   HiGHS's feasibility tolerance pinned at 1e-10 (D-021), five orders above machine
   epsilon.
3. The "one predicate, three scalar types" fact went missing rather than getting
   explained: #31 replaced §6's "generic over its scalar type" with "rational and
   algebraic separating-axis verification", so the claim is gone and the reason for it
   still is not stated.

The token-consistency fallout of the same migration is think-po3b, not this bead.
