# Independent Rational Review of the Later 228-Square Submission

The completed review accepts the rational certificate in de Winter’s later issue 1038
attachment as a feasible packing of 228 exact unit squares in a closed square of side

```text
15.596043116631669919627353842076861324679045385375355711985032
```

All 3,648 corner-wall inequalities and all 25,878 unordered square pairs passed.
The minimum wall margin is exactly zero, with 36 corner-wall equalities.
Every pair has a strictly positive maximum separating-axis gap.
Its smallest value is approximately 7.7818672523146487705565015e-68, with the exact
rational retained in the [checker receipt](checker-receipt.json).

The mathematical review implementation was authored and frozen by a separate
Squares Project reviewer before opening either new witness’s geometry.
Its prior exposure included the original T-334 adoption metadata and attribution, plus
the submission README’s claimed acceptance and verification outline.
The frozen plan records that exposure.
The checker imports Python’s standard library and GMP rational arithmetic through
`gmpy2`, and implements its own geometric predicates.
The retained freeze records that the author had read no producer implementation and
imported no project geometry code.
This is independent implementation evidence with the stated exposure.
[Frozen plan](frozen-plan.md), [freeze record](freeze.json)

A separate agent prepared the input reading copy and executed the
frozen code. The implementation author then checked the custody bridge and successful
receipt. A third agent assembled this report from those artifacts and checked the custody
chain with 26 byte and consistency checks.
The role division and execution measurements are retained alongside the result.
[Author custody check](author-custody-check.json),
[execution summary](execution-summary.json),
[consolidation audit](consolidation-custody-audit.json)

The original ZIP is 232,825 bytes with SHA-256
`5e0c62d9ad52b1afd78929e55e2fabf8d21f37fbe5f6e6c5a105f013ab970bd2`. Its
`n228_rational.json` member is 139,016 bytes with SHA-256
`58465564994035e8e6c7f40c6651c0638f12e5e04546bd4b5225ced7808ba1bc`. The original
mathematical input and its existing attribution and licence notices accompany the intake
source packet. The submission credits jazivxt’s published layout, Doğa Özden’s starting
certificate, and Codex’s refinement at de Winter’s request.
Finder and publication-order questions continue in the intake ledger.
[Original submission](https://github.com/jlevy/squares/issues/1038#issuecomment-7046716722)

The first execution stopped at the outer Witness envelope before any geometric
predicate. The successful input is the complete parsed `.witness` object serialized as
UTF-8 with `json.dumps(inner, indent=2, ensure_ascii=False) + "\n"`. It preserves the
side, source metadata, coordinate convention and all 228 rows as parsed JSON. Its
SHA-256 is `603efbf226b672576264431c21707047c416ad68ca93faa047dea385249ac883`. The
checker receipt’s `source_sha256` names this reading copy, and the custody record binds
it to the original ZIP member.
[Reading-copy custody](reading-copy-custody.json)

The [frozen checker](frozen-rational-checker.py.txt) has SHA-256
`98ceabc8ff67c87017d3db173b0cef7e53f74a930e0f3dea931c77c8b48ccb4a`. The `.py.txt` suffix
retains its exact bytes as an inert review artifact.
It parses rational strings through `Fraction` and transfers integer numerators and
denominators into exact GMP rationals.
It forms each square’s four corners from its center and basis, verifies all four unit
edges and adjacent orthogonality with consistent orientation, and tests every corner
against the closed container.

For each pair the checker projects all corners onto both edge directions of each square.
These directions also supply the square’s edge-normal axes.
At least one nonnegative projection gap establishes disjoint interiors by the
separating-axis theorem.
Every source pair was decided, and the exact minimum of its best gaps is retained in the
receipt.

All six controls declared before geometry exposure passed.
The exact shared-edge fixture and exact unit-container fixture were accepted.
The duplicate-square, translated-outside-container, inward-pair and outward-wall
fixtures were refused for their intended geometric defects.
These negative checks stop at the first decisive violation as the frozen plan permits.
Their receipt identifies the offending geometry and exact gap.
[Full receipt](checker-receipt.json)

The checker completed in 6.394 seconds, the worker in 6.824 seconds and the supervised
launch in 8.711 seconds.
Worker and guard exits were zero.
Eleven observe-only samples recorded pressure level 1 and a maximum sampled process-tree
footprint of 0.02 GiB. The authorized worker ceiling was 180 seconds with a 0.30-GiB
sampled-tree limit and a stop at pressure level 2. Separate CPU time and process-wide
peak RSS were unmeasured.
[Execution summary](execution-summary.json)

A replay can reconstruct the reading copy from the retained original mathematical input
using the serialization above and the [retained input](../../source/n228_rational.json.gz), verify both input digests, and invoke Python 3.14.7 with
`-I -B frozen-rational-checker.py.txt READING_JSON RESULT_JSON`. Use the project’s pinned `gmpy2` dependency and the retained execution limits.
This report consolidates the completed replay without rerunning geometry.

The accepted conclusion covers this rational certificate’s finite feasibility.
The stronger degree-seven certificate’s independent geometry review, exact pose and
drawing comparisons, registration and adoption remain open. The source’s local and global optimality statements remain outside this
review’s proved scope.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
