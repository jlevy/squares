# Published Core Claims: Adversarial Review and Corrections

The review examined the published `s(11) ≥ 3.81` explainer at commit
`edccf294be375d209c431f4fb8f2eb892f22fd56`, its geometric theorem and verifiers, and the
directly related claims about the method’s limits.
Three independent agent assignments covered the theorem, the event-cell implementation,
and the actual certificate plus ceiling arguments; the coordinator checked the published
version, interval implementation, sources, and proposed findings.
An additional pass challenged the findings against their surrounding definitions.

No counterexample to the headline bound or omitted family of placements was found.
The five findings below concern a separate ceiling checker, its search consumer, and
statements about the method’s reach.
Epic `think-hmtc` tracks their focused remediation and contribution of the independent
geometric oracle.

## Findings

### D-473: A fixed floating-point screen could accept a false ceiling

Bead: `think-lsg0`. Severity: high for the ceiling verifier’s soundness contract.

`sqpack.fractional.ceiling` claimed exact decisions while using a fixed `1e-8` margin to
screen vertices and memberships before exact checking.
Its justification assumed coordinates below ten, but the public certificate accepted
arbitrary positive container sides.

The counterexample uses `L = 10000000010`, `B = 9/10`, half-tangent net
`(0, 1/10, 1/5, 3/10, 2/5, 21/50)`, and two identical unit squares with half-tangent
`1/5` centered at `(10000000000, 70000000004/7)`. With weight one each, their true depth
is two; the checker reported maximum depth zero, decided none of its sixteen vertices
exactly, and accepted the certificate.

Giving each square weight `10^21` and setting `n = 2 × 10^21` produces a false
impossibility conclusion, not merely an invalid witness.
A finite D4-invariant half-integer grid in `[0,L]²`, with unit atom weights, has mass
`(2L+1)² = 400000000840000000441 < n`. Every rotated `B`-square contains an axis-aligned
square of side at least `B/√2 > 1/2`, hence a grid point.
The net reaches `π/4` and satisfies `B(1+D) = 99/100 < 1`, so that grid is a covering
certificate contradicting the accepted ceiling.

This example is outside the retained small-coordinate cases.
The headline lower-bound checker is separate and does not use this screen.
The [ceiling tests](../../../packing/tests/test_fractional_ceiling.py) retain the
counterexample. Exact coordinate, coefficient, family-size and total-weight guards now
justify each floating screen; other inputs take an exact path before conversion.
The reported maximum is also exact when it is below one, protecting the depth used to
scale candidate families.

### D-474: Two upper bounds do not establish a lower slope or a stopping side

Bead: `think-cmi9`. Severity: medium.

The [covering-value record](../../../packing/frontier/covering-values.yaml) compared a
feasible covering mass `11.998960` at side `3.96` with `12.248227` at side `3.97`,
inferred a slope of at least `24.9`, and placed the ladder’s endpoint near `3.96004`.
Its available lower bound at `3.97` was only approximately `10.845594`.

The two feasible masses upper-bound the minimum covering value.
Subtracting them does not lower-bound its increase: a value of `11.9` at both sides
satisfies all the quoted numerical bounds and has zero slope.
That example is a countermodel to the inference, not a claim about the actual optimum.
Even two exact endpoint optima would not bound the slope immediately after `3.96`
without further assumptions.

The slope and endpoint conclusions have been withdrawn from maintained views.
The source run log and session remain historical evidence with explicit corrections in
the maintained records.
The interval at `3.97` straddles twelve, so it does not decide whether the unrestricted
method can certify that side.
The retained `s(12) ≥ 3.96` certificate remains a separate result.

### D-475: The numerical ceiling depends on the direction net

Bead: `think-hekn`. Severity: medium.

The README said no twelve-square certificate of this form can exist above `3.990816`.
The proved ceiling is `4/(1+D)` for a fixed net, and this numerical value belongs to the
retained 181-direction net.
Refining the largest gaps can decrease `D` and raise the ceiling.
The [result record](../../../packing/frontier/results.yaml) already carried this
qualification; the README now does too.

No countercertificate above `3.990816` was constructed.
The finding is an unsupported expansion of the cited theorem’s scope.
The separate obstruction to reaching exactly four with one finite net is unchanged; a
family approaching four would require increasingly fine nets and other unresolved
covering conditions.

### D-476: Intermediate cutting bounds bypassed the final verifier

Bead: `think-ozdb`. Severity: high for intermediate exact bounds.

Tracing D-473 through the search consumers found the same screen in
[`cutting.depths_above`](../../../packing/src/sqpack/fractional/cutting.py).
On the counterexample with weights `10^21`, it returned zero depth and no violations,
although exact depth is `2 × 10^21`. The cutting runner used this separation result to
update `best_scaled_total` before calling the final ceiling verifier.
Repairing final verification alone would leave those intermediate purported exact lower
bounds exposed.

The cutting screen now shares the arithmetic guards and exact fallback, with a separate
membership margin accounting for approximate intersection error.
A regression in the [cutting tests](../../../packing/tests/test_fractional_cutting.py)
checks the reproduced depth.
No retained small-coordinate cutting result was shown incorrect.

### D-477: Floating-point deduplication erased a genuine overlap

Bead: `think-hrko`. Severity: high for intermediate exact bounds.

This cutting defect occurs at small coordinates, independently of the large-input
failure above. Set `L = 4` and `ε = 10^-20`. Three axis-aligned unit squares share
y-range `[1, 2]` and have these x-ranges and weights:

| x-range | Weight |
| --- | ---: |
| `[1 − 2ε, 2 − 2ε]` | 0 |
| `[2 − ε, 3 − ε]` | 1 |
| `[1 + ε, 2 + ε]` | 1 |

The two positive-weight squares overlap, so maximum depth is two.
`screened_separation` returned one because its vertex generator deduplicated by
floating-point coordinates.
The overlap vertices rounded to a previously retained vertex of the zero-weight square,
which lies outside the overlap.

The repair retains candidates with identical float coordinates and reconstructs each
exact point before deciding depth.
The [cutting regression](../../../packing/tests/test_fractional_cutting.py) retains this
example. The final ceiling verifier enumerates its vertices independently; this example
demonstrates an invalid intermediate bound, not an accepted final theorem.

## Independent Verification Evidence

The reviewed headline certificate’s SHA-256 is
`b121edbd044b6f326022d8783551efd947c95eec2738269857d039358ac6ae6a`. The full standalone
replay under CPython 3.14.7 accepted all 181 directions and `567130649` reachable cells,
with total mass `434547/40000` and least covered mass `4001/4000`. Its measured runtime
was 64.5 seconds on the review host.
The full doubled-net interval test also passed: 361 directions, no stalled or
budget-exhausted boxes, and minimum enclosure exactly `[4001/4000, 4001/4000]`.

The review’s independently written geometric oracle used separating-axis tests for cell
feasibility and direct atom sums, sharing no clipping, strip-range, or prefix-sum
implementation with the standalone sweeps.
At seed `89213`, all 20,000 rational cases matched `verify_claim.py` in minimum mass and
reachable-cell count; 8,038 eligible cases also matched `minimal_verify.py`. The cases
included empty and singleton feasible domains, axes, coincident events, zero weights,
empty supports, and varying rational denominators.

Bead `think-nq7w` contributes that review script as
[`devtools.check_fractional_sweep`](../../../packing/devtools/check_fractional_sweep.py),
with portable imports, reproducible commands, and bounded ordinary test coverage.
The [development guide](../../../development.md) explains where it fits in validation.
This oracle compares finite cases and can expose discrepancies; it is not a formal
verification of either checker or a replacement for the actual certificate replay.

The mathematical review also checked reflection and pullback, the rational angle net,
strict interior containment, boundary double-counting, nonnegative weights, degenerate
center domains, compactness, and extensions to larger `n`. The Stromquist printed-cover
and repaired-cover instruments replayed with all controls passing, after visual
comparison with the original PDF figures.

The proposed unrestricted `n=20` wall finding was discarded: H-062 explicitly defines an
operational wall for two site constructions and says it is not the unrestricted covering
value. This review does not promote that operational bracket to a theorem about all site
sets.

The review did not audit every registered result or formally verify the programs.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
