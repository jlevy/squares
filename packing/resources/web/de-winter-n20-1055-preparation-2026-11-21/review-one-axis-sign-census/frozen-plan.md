# Frozen Plan: Independent One-Axis Sign Census and D4 Audit

This slice will enumerate the complete sign/vacancy roster allowed by the independently
accepted paired-bridge conditions in issue #1055, then audit all eight board symmetries.
It will not enumerate separation graphs or apply general-path clauses.

The exact domain is `0 < tan(theta/2) <= 1/24`, for nineteen independently signed
equal-magnitude tilts and one aligned square in a hypothetical board `S < 5`. The
reviewed near-grid reduction supplies twenty occupied cells in a five-by-five grid, with
one vacancy per row and column.
Every retained paired bridge must supply its horizontal or vertical forward-separating
chain. The accepted local bridge replay makes zero integer chain cost necessary for such
a chain; zero cost is not sufficient for geometric feasibility.

## Immutable Inputs and Prior Exposure

The [specification](census-spec.json) names the original attachment and every source
member read. Its SHA-256 is
`d7261e5ecd4a9cc96b6d01e24ba1925c39946cb7235504ba6db1c828534d8df6`.

The accepted local bridge [receipt](bridge-verification.json.gz) is retained alongside
this checker, independent of transient scratch.
Its original JSON SHA-256 is
`a8b48b5cff9b0b101174e3eb513bb3ed502c05bbfb825e1f8b376fb0c017d286`. The checker will
stream its decompressed bytes with an 8 MiB ceiling and require this exact digest.
It will not rerun the 3,488 polynomial exclusions.

The reviewer has read the producer’s theorem, path/sign/graph programs, prior project
reviews, and the completed local-bridge evidence.
This implementation constructs paired chains directly from their shared diagonal,
enumerates local sign truth tables, solves the resulting finite constraints, and
implements rotations/reflections separately.
It neither imports nor executes contributor code.
It is not a blind review.

## Census and Completeness

Enumerate all 120 permutations of the five vacancy rows.
For each permutation, enumerate all twenty choices of the aligned occupied cell.
The occupied-cell order is lexicographic in `(x,y)`; bit one denotes positive tilt, bit
zero denotes negative tilt, and the aligned cell’s bit is always zero.

Construct each possible paired bridge directly from two neighboring diagonal cells.
The horizontal chain advances across five columns and the vertical chain across five
rows. Retain it only if every cell in both chains is occupied.
The vertical transverse coordinate is `4-x`, so the tilt sign is unchanged by this
quarter-turn of the coordinate frame.
Check that the two chains intersect in exactly their two diagonal cells.

For each chain, enumerate all local nonzero signs with the aligned cell fixed to zero if
present. Compute the exact integer cost from endpoint widths, straight sign differences
and the single diagonal contribution.
Keep precisely the zero-cost local vectors; refuse a negative cost as a broken premise.

A global assignment is retained exactly when, for every paired bridge, its horizontal or
vertical chain matches one of those local vectors.
Enumerate the conjunction of these disjunctions using forced assignments and recursive
branching. Conflicting branches are refused.
Once every bridge is satisfied, enumerate all remaining free signs.
Deduplicate complete assignments.

Completeness follows from the branching rule: every satisfying assignment extends a
viable alternative of the chosen unresolved bridge, and each recursive alternative
assigns at least one previously free sign.
Forced assignments apply only when no other alternative is viable.
Filling the remaining free bits therefore enumerates every assignment admitted by the
bridge conditions. Every emitted assignment is also checked directly against the
integer-cost conditions, separately from the constraint representation.

Expected counts, all to be derived rather than accepted from a saved catalogue:

- 120 vacancy permutations and 2,400 vacancy/aligned-position cases.
- Paired-bridge histogram: 92 permutations with four bridges, 24 with five, four with
  six.
- 29,368 distinct sign/vacancy/aligned-position assignments.

## D4 Audit

Generate four quarter-turns `(x,y) -> (4-y,x)`, each with or without reflection
`x -> 4-x`. Reconstruct each transformed vacancy permutation, occupied-cell bijection
and aligned index. Rotations preserve tilt sign; reflections negate it.

For every retained assignment, require every transformed assignment to belong to the
complete roster. Use the lexicographically least image as representative, and check the
representative regenerates the same orbit.
Verify the orbit partition and retain every assignment’s representative index.

Expected results are 234,944 checked images, 3,671 distinct representatives and 3,671
orbits of size eight.
No quotient is accepted from an unverified symmetry claim.
The output retains the full assignment roster, all representatives, all 2,400 case
counts, the bridge/orbit histograms, and a digest of canonical roster serialization.

## Twelve Predeclared Controls

Six expected acceptances:

1. A positive-sign upward bridge has zero cost.
2. A negative-sign downward bridge has zero cost.
3. An aligned first arm-end cell with the other signs positive has zero cost.
4. Four quarter-turns restore the complete encoded case without changing signs.
5. A reflection negates all nonzero signs, and applying it twice restores the case.
6. The constraint search exactly matches a three-variable brute-force truth table.

Six expected refusals:

1. The all-negative signs on an upward bridge.
2. An aligned cell inside an arm.
3. Reflection transport that omits the sign change.
4. An encoded aligned square with a nonzero sign bit.
5. A truth-table roster with one valid solution removed.
6. A truth-table roster with an invalid solution added.

Any control mismatch, invalid assignment, missing image, wrong count, unexpected
exception or resource ceiling fails the run and prevents a success receipt.

## Scope and Later Obligations

These counts depend on the paired-bridge conditions only.
They do not depend on the 576-certificate bank or general-path clauses.
The latter include five-tile chains with zero to four transverse jumps; the accepted
single-jump bridge result does not establish them.

Before pruning graphs with those clauses, independently certify their exact bounds and
their application to each graph.
Complete graph enumeration, geometric rule extraction and graph-to-certificate coverage
remain separate work.
The source’s 273,584 graphs and 566 used certificates remain reported counts until those
obligations are checked.
This census does not accept the one-axis theorem, the angular-diversity theorem or
either unrestricted lower bound for Stage 4.

## Execution Boundary

Preparation only. Do not execute, import, compile or syntax-check the checker until the
coordinator provides the serial guarded slot.
The prepared source is [check_one_axis_sign_census.py](check_one_axis_sign_census.py).

Proposed invocation with the project Python 3.14 interpreter, from this directory:

```bash
"$PYTHON" -I -B check_one_axis_sign_census.py \
  --spec census-spec.json --bridge-receipt bridge-verification.json.gz \
  --output "$OUT/sign-census.json"
```

Use one worker, external scratch/cache directories and an external supervisor.
Target under 20 seconds and 0.10 GiB peak RSS. The hard outer limits are 60 seconds,
0.25 GiB sampled process-tree cost and memory pressure level 2. An internal 55-second
limit bounds census work.
Further hard limits are one million search nodes, two million raw assignment emissions,
50,000 assignments per case and 50,000 distinct assignments overall.
A cap produces incomplete evidence, never a smaller accepted census.
The output must be new.

No repository, branch, tracker or GitHub write is part of this slice.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
