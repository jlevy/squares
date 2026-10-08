# Review of the ry-xu Rational and Radical Packing Packets

Reviewer: independent strong agent, GPT-6 Astra, xhigh.
Reviewed on 2026-10-08 UTC (2026-10-07 in the host’s America/Los_Angeles timezone).
Scientific checkpoint: `5abc1b327d5a3bdbf14f128ff7b176e6abdb64d0`, with the replay
normalization and source-count wording corrections described below.

## Decision and Scope

The reviewed arithmetic, complete source inputs and retained decisions support finite
feasibility for the 25 rational constructions and the separate undilated 51-square
construction. Production house construction, private-worker recovery, frontier adoption,
source-snapshot size and final assurance expression require their own integration gates.
This review does not authorize those gates to be skipped.

The source’s claim of 191 touching pairs for the undilated n=51 construction remains
unconfirmed. Both reviewed exact implementations count 119 touching pairs and 1,156
strictly separated pairs, covering all 1,275 unordered pairs.
This discrepancy does not invalidate the independently checked feasibility claim.
Neither route establishes optimality, novelty, rigidity, local minimality or the history
of the source’s search.

Credit for the constructions belongs to ry-xu.
The primary sources are [issue #432](https://github.com/jlevy/squares/issues/432) and
[the immutable source tree](https://github.com/ry-xu/square_packing/tree/8dc415296f697f5140caea27c7a0193d52deb4e6).
The source describes an LLM-assisted search.
No upstream producer or checker was executed for this review.

## Rational Source and Geometry

The complete roster is 51, 70, 84, 86, 88, 102, 103, 105, 108, 123, 126, 127, 129, 130,
131, 146, 153, 175, 179, 236, 258, 261, 263, 267 and 295. Superseded cases remain in the
packet; current frontier selection must compare exact sides independently.

The reviewer compared every retained original certificate string with the acquired file,
its pinned SHA-256 and the immutable source tree’s Git blob identity.
All 25 matched byte for byte.
The acquisition boundary is implemented in
[`ryxu_arrangement_reports.py`](../../../packing/devtools/ryxu_arrangement_reports.py),
with original factual inputs in the
[source packet](../../../packing/resources/web/ry-xu-new-packings-2026-10-08/README.md).
The parser rejects duplicate JSON keys, missing or extra fields, wrong counts,
incomplete square rosters and unsupported scalar or angle syntax.

For each exact rational half-angle parameter t, the conversion uses c=(1−t²)/(1+t²) and
u=2t/(1+t²). The denominator is positive and c²+u²=1 exactly.
Rotating each corner (±1/2, ±1/2) by this basis produces a unit square with the source
centre.
Native centre/basis materialization and the separate rational corner checker then
decide containment and every unordered pair using exact separating axes.
The half-angle conversion is shared between the two routes and was reviewed as a shared
boundary; their geometric deciding implementations are distinct.

The input uses the source’s exact rational side and all centres and half-angle values.
The source certificates already include their stated dilation.
The importer applies no further dilation.
The printed decimal ceiling does not determine the admitted side; `confirmed_bound`
computes an upward decimal rendering from the exact rational value.
The rational n=51 certificate remains separate from the undilated radical construction.

The retained batch contains 75 full-roster jobs and 150 complete native outcomes: 25
positives, 25 duplicated-square controls and 25 outside-container controls.
The receipt reports 2,078,082 pair decisions and 330.19143345800694 seconds for the
producer’s two-worker run.
The reviewer admitted all 75 jobs against reconstructed full inputs and the exact native
result contracts.
Every positive passes both routes; every control fails both routes with
the required negative pair or wall diagnostic.
The reviewer did not repeat this entire rational batch.
The underlying rational kernel was independently replayed for all three #399
certificates in its separate review.

The fast receipt check validates complete source/control input equality, exact result
field sets, both route identities, rational fields, scope limitations, full pair counts,
verdicts and diagnostic signs.
It does not recompute every diagnostic magnitude.
`check --replay` compares the full freshly computed native outcomes, excluding measured
CPU and wall times.
Git retains the reviewed complete receipts; a structural admission is
not described here as a fresh geometric execution.

## Undilated n=51 Arithmetic and Source Binding

The source root `square_packing_records.json` is 340,048 bytes, with SHA-256
`93130ffb2f9da1b15ba5e8e491e60509192d6fb21108aa2adc86d29c4f071e5d`. The entire selected
51-square record equals the retained fact, whose canonical JSON SHA-256 is
`bf744f8b9b41776cabe43eb46c2e45293fbfe3803eb47578de878c61509357e0`. The reviewer checked
both equality and the original root blob’s source-tree identity.
The full source root’s size must not be confused with the selected record’s size.

[`ryxu_radical_n51.py`](../../../packing/devtools/ryxu_radical_n51.py) uses the exact
fields for all 51 centres and accepts only angles 0 and π/4. Rounded source fields are
retained as source facts and do not decide geometry.
The closed expression parser uses rational strings and specified linear expressions in
√2; it never evaluates source code.

The independent scalar is a+b√2 with a and b rational.
Addition and multiplication use (√2)²=2. Equal-sign coefficients have that sign.
For opposite signs, comparing a² with 2b² and multiplying the comparison by sign(a)
gives the exact sign of a+b√2. No nonzero rational coefficients can make a²=2b². The
native route separately uses the irreducible polynomial x²−2 and isolating interval
(1,2), selecting the positive root.

Axis-aligned corners are the centre plus (±1/2, ±1/2). Diamond corners are the centre
plus (0, ±√2/2) and (±√2/2, 0). Their consecutive edges have squared length one and
oriented determinant one.
The independent route checks those identities, all corner wall clearances and all 1,275
pairs. For each pair it takes the maximum directional projection gap over the edges of
both squares: negative means interior overlap, zero means touching, and positive means
strict separation. Including opposite edges adds redundant axes without changing that
decision.

The admitted side is (16+5√2)/3. Substitution gives 9s²−96s+206=0. This polynomial and
the source coordinates describe a feasible construction; they do not assert equality
with the minimum packing side s(51).

## Fresh Radical Outcomes and the Contact Discrepancy

The reviewer executed the three full radical jobs and compared canonical JSON for
complete inputs and both outcomes against the retained evidence.
All bytes matched these frozen outcome SHA-256 values:

| Job | Complete outcome SHA-256 |
| --- | --- |
| positive | `2170142ecd3e1065a038ad5d1eb38c7f53951d7f9fad6851a34f729ba9b249a2` |
| duplicate-square-overlap | `65dfc3caaf99e148f0a49dfd61702c8b95397cd5e88a17d9413899f83685dc4e` |
| square-translated-outside-container | `02a31fcac9651ffbc3b0a6dab329675c1e2cdecdf263d92c5327b37331a6c0cc` |

Both controls retain 51 squares and test all 1,275 pairs in each route.
The duplicate control replaces the second square by the first.
The outside control translates the first centre by the full side plus two.
The retained number-field decimals are diagnostic renderings; the complete coefficient
pairs remain the exact deciding input.
The full outcome hashes protect every retained diagnostic and metadata field across the
private-worker custody boundary, in addition to the reconstructed input comparison.

A second native positive execution returned 119 touching pairs, 1,156 strictly separated
pairs, 1,275 tested pairs and 52 corner-coordinate incidences on container walls.
The independent rational-pair route also returned 119 touching pairs.
The 52 is a separate corner-coordinate count and does not explain 191. The source
explicitly reports 191 touching pairs and says its exact checker is available on
request, rather than in the repository.
No equivalent alternative definition has been established.

The native count is reproducible from the retained complete input with project Python
3.14, from `packing/`:

```python
from devtools import ryxu_radical_n51 as radical

side, poses = radical.inputs("positive")
_, report = radical.exact_verify(radical.witness(side, poses))
print(report.valid, report.pairs_tested, report.touching_pairs,
      report.strict_pairs, report.container_contacts)
# True 1275 119 1156 52
```

## Findings and Verification Record

**R1: replay comparison rejected valid negative outcomes.** The documented
`python -m devtools.ryxu_radical_n51 check --replay` failed at the scientific
checkpoint. Native failure entries were Python tuples; retained JSON entries were lists.
The positive compared equal directly, and both negatives compared equal under canonical
JSON with their frozen hashes unchanged.
The correction compares canonical JSON of the entire fresh and retained outcomes.
It preserves full-field comparison and source/input binding.
An actual duplicate-square replay regression covers this serialization boundary.
The corrected documented command replayed all three full jobs and exited 0.

**R2: unsupported explanation of the source contact count.** The initial packet README
called the source’s 191 a different contact statistic.
The reviewed correction states that 191 remains unconfirmed and is not used to admit
feasibility.
The record must preserve that distinction when expressing T126 or an adopted
case.

Review logs are under the external task review directory:

- `ryxu-source-custody-audit.log`: all 25 complete source inputs, immutable blob checks,
  selected radical source equality and 75 full receipt contracts; exit 0
- `ryxu-radical-replay-diff.log`: all three fresh canonical outcomes equal retained
  outcomes, full outcome hashes and native contact roster; exit 0
- `ryxu-radical-replay.log`: reproducible pre-fix tuple/list failure
- `ryxu-radical-replay-fixed.log`: documented-command verification of R1; exit 0
- `ryxu-focused-tests.log`: both scientific test modules, 40 passed in 4.23 seconds; the
  actual negative replay regression took 3.51 seconds, below the unchanged 12-second
  per-test ceiling

The producer’s recorded 18.707450165995397 seconds covers its original three radical
jobs and 7,650 pair decisions; it is not the reviewer’s wall measurement.
No claimed source search result, source program output or contact count substituted for
an independently evaluated geometric predicate.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
