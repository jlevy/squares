# BC-230 Adaptive-Core Control Matrix

Status: author checkpoint for BC-231 implementation.
Each row states an executable oracle.
No row in this packet has been run against an adaptive verifier because that verifier
does not yet exist.

Launch base: `c55726e1e885227f63110131c0a914665175ff89`\
Frozen preregistration: `f1b6c641e8d3a2fea39cf5aa5292cb8fc1221772`\
The theorem and field meanings are in
[`bc-230-adaptive-core-contract.md`](bc-230-adaptive-core-contract.md).

## Required Positive Controls

| ID | Fixture and operation | Exact oracle |
| --- | --- | --- |
| P1 | Load `packing/cases/n11_fractional_certificate/certificate.json` through the unchanged scalar route and through the in-memory adaptive specialization with every `B_k = 9977/10000`. Do not rewrite the fixture. | Both routes accept and return the same total `434547/40000`, least mass `4001/4000`, and first worst direction `0`. |
| P2 | Repeat P1 for `packing/cases/n12_fractional_certificate/certificate.json`. As a fixture-generation assertion, run the unchanged scalar route on the frozen bytes, require a nonnull `worst_direction`, and write its returned label as the literal `expected_first_worst_direction` in the test data before any adaptive comparison. Generation fails if it does not freeze that scalar literal. | Both routes accept and return total `149987/12500` and least mass `12501/12500`. Each route’s first-worst direction equals the frozen `expected_first_worst_direction` literal, so the routes also equal one another; the source bytes remain unchanged. |
| P3 | Load `packing/cases/n11_fractional_certificate/thirdparty/control-n17-massaccesi.json` through the scalar and adaptive in-memory exact verifiers, then run the archived verifier and `packing/cases/n11_fractional_certificate/thirdparty/check.py` on the original bytes. Separately submit the unchanged object to the retention command. | Both in-memory routes recompute total `203/12` and least mass `1`; the archived and source-distinct programs accept. The retention command gives the same named refusal on both interpretations because `least_cell_mass` is undeclared. No route rewrites the source fixture. |
| P4 | Build a small adaptive fixture with at least three unequal `B_k`, expanded `D4` atoms, and a brute-force-sized event grid. | Project sweep, interval route, and standalone route agree on every per-direction minimum and the global minimum. |
| P5 | For P4, evaluate a center on a single event boundary and one at a multiple-event intersection, together with representatives from every incident open event cell. Independently form the boundary covered-atom set by direct exact closed-square membership, and form the union of the covered-atom sets from all incident open cells; do not derive either set from sweep deltas. | The direct boundary-membership set equals the union of the incident open-cell membership sets, and its exact mass equals the boundary result. The boundary mass is at least the maximum mass over every incident open cell; the open-cell minimum is unchanged. |
| P6 | Evaluate every derived seam with the lower-index ownership rule. | Exactly one ownership cell is selected; both neighboring closed-cell mismatch bounds contain the seam; the selected core is strictly contained. |
| P7 | Fold representative orientations from all eight `D4` sectors, including axis and diagonal boundaries, and run the interval route’s doubled-net directions. | The folded cell index is deterministic, the unfolded witness has the same exact mass as its folded representative, and each reflected direction uses the same `B_k` as its source cell. |
| P8 | Run the adaptive standalone verifier under normal CPython and `-O` on the same frozen bytes. | Exit status, stdout verdict, exact minima, and printed SHA-256 are identical. |
| P9 | Add complete generic, axis, diagonal, center, and zero-weight `D4` orbits to the brute-force fixture, then compare with the version that omits the complete zero orbit. | Every distinct image is serialized once; orbit stabilizers create no mass multiplicity; adding or omitting the complete zero orbit leaves total mass and every exact minimum unchanged. |

P1 through P3 are the scalar-compatibility gate.
A changed retained verdict blocks the adaptive implementation even if a new candidate
would pass.

## Format and Cell-Geometry Refusals

| ID | Mutation | Required refusal before any sweep |
| --- | --- | --- |
| F1 | Delete one `angle_cells` entry. | Missing or noncontiguous cell index; folded arc uncovered. |
| F2 | Duplicate an index, swap two cells, or repeat a half-tangent. | Indices or half-tangents are not strictly ordered. |
| F3 | Change a lower or upper boundary while leaving the half-tangents fixed. | Declared boundary differs from the exact derived seam. |
| F4 | Call the pure closed-cover validator directly, bypassing serialized-field and derived-field-equality validation, on the valid closure sequence `[0,1/3]`, `[1/3,2/3]`, `[2/3,1]`. Change the second lower endpoint to `2/5` for the gap case and to `1/4` for the overlap case. | The direct validator reaches its cover branch and gives the named gap or overlap refusal. The test asserts that serialized-field validation was not invoked. |
| F5 | Exercise two independent branches. First, call the pure endpoint validator directly on the F4 valid sequence after changing only its first endpoint to `1/100`, then after changing only its last endpoint to `99/100`; both calls bypass serialized-field validation. Second, specialize `packing/cases/n12_fractional_certificate/certificate.json` as adaptive, replace only its final half-tangent by `t_K = 1/2`, and recompute every dependent seam, boundary, and mismatch declaration. In that serialized case, `q_K = 164144306/142927847 > 1`; keep bounded format, canonical rationals, contiguous indices, strict half-tangent order, and the final direction bracket valid. | The direct calls reach and refuse the axis and fold endpoint branches. The serialized mutation passes parsing, ordering, and derived-field equality, then reaches the named `q_K >= 1` final-seam refusal. No stale dependent field may trigger F3 instead. |
| F6 | Change `seam_owner`, omit it, or encode ownership per cell inconsistently. | Only `lower-index` is accepted by this contract version. |
| F7 | Change a declared `D_k` without changing its direction or boundaries. | Declared mismatch differs from the exact endpoint maximum. |
| F8 | Shorten the net so `t_K^2 + 2t_K - 1 < 0`. | Net does not reach the fold. |
| F9 | Move the penultimate direction across `pi/4`, or make `t_K >= 1`. | The final pair does not form the required folded-endpoint bracket. |
| F10 | Encode a rational as a JSON float, `NaN`, `Infinity`, a string longer than 512 characters, or a zero-denominator string. | Exact-format or bounded-input refusal. |
| F11 | Add an unknown top-level or cell field, declare an unknown variant, or combine scalar and adaptive representations. | Closed-schema or ambiguous-variant refusal. |
| F12 | Duplicate a JSON key. | Duplicate-key refusal before object construction. |
| F13 | Exceed 8,388,608 input bytes, 4,096 atoms, or 10,001 angle cells, one limit at a time. | The corresponding input-budget refusal before geometry or sweeping, identically in all three routes. |
| F14 | Replace a reduced rational string by an equal but noncanonical spelling such as `2/4`, `0/7`, or `01`. | Canonical-rational refusal; exact numerical equality does not rescue noncanonical bytes. |
| F15 | Encode `n` or a cell index as a Boolean, string, or nonintegral JSON number. | Exact-integer refusal; Boolean subclasses of integer in Python must not pass. |
| F16 | Omit each required top-level or cell field, one mutation at a time. | A named missing-field refusal before object construction completes. |
| F17 | Replace `angle_cells` or `atoms` with a nonarray, a cell with a nonobject, or an atom with a row other than three entries. | A named structural refusal before rational or geometry work. |

## Theorem and Containment Refusals

| ID | Mutation | Required refusal |
| --- | --- | --- |
| T1 | Set one side to exact equality `B_k(1+D_k) = 1`. | Strict containment fails in that named cell. |
| T2 | Increase one `B_k` past the equality threshold while retaining a sampled center that happens to fit. | Strict containment fails; samples cannot rescue it. |
| T3 | Set one `B_k <= 0`. | Invalid witness-side precondition. |
| T4 | Remove one image from a nontrivial positive-weight atom orbit. | Missing `D4` image under Condition 1. |
| T5 | Change one orbit image’s weight. | Unequal `D4` image weight under Condition 1. |
| T6 | Give one atom a negative weight. | Nonnegative-measure precondition; no event or interval sweep runs. |
| T7 | Duplicate a site or place a site outside `[0,L]^2`. | Distinct-site or container-support refusal. |
| T8 | Change `total_mass` without changing the atoms. | Declared total differs from the exact atom sum. |
| T9 | Raise the total to exactly `n`. | Condition 2 is strict and fails. |
| T10 | Start from the adaptive equal-side specialization of `packing/cases/n12_fractional_certificate/certificate-77-20.json`. Reduce all eight distinct `D4` images of the generic orbit through `(37/44,423/440)` by `1/10000`, changing every orbit weight from `7/32` to `4373/20000`. Set `total_mass` to `119367/10000` and independently declare `least_cell_mass = 4999/5000`. Before route testing, a direct-membership fixture generator independent of the project, interval, and standalone routes must enumerate the full event grid and freeze the exact cell index, direction, and center of a witness attaining that minimum; generation fails unless the exact global minimum is `4999/5000`. Assert that bounded format, canonical fields, derived geometry, complete equal-weight `D4` orbits, nonnegative weights, total mass below `n`, the claim, and strict containment still pass before Condition 5. | All three routes reach Condition 5 and return the frozen cell index, direction, center, and exact mass `4999/5000 < 1`. They refuse on that same subunit witness, with no earlier-premise refusal. |
| T11 | Change `least_cell_mass` from the recomputed global minimum or leave it null at retention. | Declared-minimum or undecided-candidate refusal. |
| T12 | Change `claim` to a side or `n` not carried by the object. | Claim does not equal the theorem conclusion. |
| T13 | Set `n <= 0` or `L <= 0`. | Positive-instance precondition refusal before cell geometry. |
| T14 | Change `symmetry` from `D4` or omit it. | Unsupported- or missing-symmetry refusal before any use of folded coverage. |
| T15 | Delete one image from a serialized zero-weight orbit. | Listed-domain completeness refusal before the theorem conditions. The report must distinguish this closed-schema failure from measure-level `D4` invariance, which absent zero-weight sites do not break. |

## Known-Feasible and Route Guards

| ID | Fixture and operation | Required oracle |
| --- | --- | --- |
| G1 | Use the existing signed-weight `n=1`, `L=11/10` forgery whose coverage rows look feasible. | Refuse the negative weight before all five conditions; never print a bound for the known-feasible target. |
| G2 | Replace the forgery’s negative weights by zero as in the retained control. | Refuse because total mass is at least `n`; the signed and legal objects fail for different named reasons. |
| G3 | Delete one full adaptive angle cell while retaining all sampled directions. | Refuse the uncovered folded arc before Condition 5. |
| G4 | Delete a complete atom orbit rather than one image. | Run the decision routes; accept only if all three independently recompute coverage at least one. A generator’s prior verdict is not an oracle. |
| G5 | Make the interval route return an enclosure that contains but does not equal the event-sweep minimum. | Refuse route disagreement; a matching acceptance boolean is insufficient. |
| G6 | Make the standalone route disagree on a cell index, exact minimum, or containment failure. | Refuse the candidate and name the first shared premise. |
| G7 | Mutate the candidate path after one route reads it. | Refuse changed bytes and print no retainable verdict. |
| G8 | Skip a required route or dependency. | Report the skip and refuse; a check that did not run cannot pass. |
| G9 | Supply an adaptive object to the scalar-only `decide_certificate` before BC-231 extends the gate. | Refuse the unsupported variant by name. |
| G10 | Set `L` strictly above `m B_0`, where `m` is the least integer with `m^2 >= n`, then repeat at equality. | Refuse the strict-above case by the adaptive method ceiling. Do not refuse equality on this guard alone. Under scalar specialization, both verdicts match the existing ceiling check. |
| G11 | Give the legacy route a syntactically valid scalar net that reaches the fold but does not satisfy the adaptive variant’s canonical final bracket. | Preserve the existing scalar verdict and bytes. Do not reinterpret the object as adaptive; the same net encoded under the adaptive variant is refused by its folded-cover schema. |

## Scalar-Specialization Assertions

For each scalar fixture and scalar refusal mutation already used by
`packing/tests/test_fractional_certificate.py`,
`packing/tests/test_decide_certificate.py`, and
`packing/cases/n11_fractional_certificate/thirdparty/falsify.py`, BC-231 must compare
the scalar verdict with the adaptive in-memory specialization.
The comparison includes:

- acceptance or refusal;
- exact total and exact global minimum when a sweep is valid;
- first worst direction under the existing net order;
- containment truth, including equality refusal; and
- unchanged source bytes and the same hash after the replay.

The adaptive route may add an earlier format refusal for an object that cannot define a
complete folded cell cover, but it may not turn any current refusal into acceptance or
change a retained positive’s numerical verdict.

## Gate Order and Cost Receipt

BC-231 should run controls in this order:

1. bounded JSON and exact-rational parsing;
2. indices, net, derived seams, endpoint ownership, and mismatch equality;
3. atom, `D4`, total, claim, and strict-containment checks;
4. the cheapest interval or closed-form refusal capable of rejecting the object;
5. project event sweep;
6. source-distinct standalone replay; and
7. frozen-byte reread and digest.

The receipt records wall and CPU time by route, peak cell count or interval boxes, every
skip, and the first named refusal.
BC-231 stops if a retained scalar verdict changes or the three adaptive routes disagree.
BC-236’s later four-times cost guard does not apply to BC-231, but BC-231 must still
price the adaptive decision against the same scalar fixture.

## Post-Review Reconciliation

Date: 2026-09-05. This matrix remains a set of proposed executable controls for BC-231;
this reconciliation does not record a completed run.
It resolves all four findings in the frozen source-distinct review, whose SHA-256 is
`6a7d9f8629864615d096aec4495c3f65637f201214911e5c4553250e92c23218`.

- Prior frozen matrix SHA-256:
  `262029bf695937bf0af98e0b92cb7d94e714578861a0c128205164d6cfdc49b7`
- Reconciled matrix self-normalized SHA-256:
  `7b856c12bdf6b0eced0ba0bb89382f2049fb67ea6b5850b7814680b369a6533d`

The self-normalized digest hashes the complete formatted file after replacing only the
64 hexadecimal digits in the reconciled-digest line above with 64 zeroes.
The final raw-file SHA-256 is reported with the coordinator handoff because embedding a
raw-file digest in the bytes it hashes would change that digest.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
