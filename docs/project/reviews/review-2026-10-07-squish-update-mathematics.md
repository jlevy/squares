# Mathematical review of the SQUISH October 7 follow-up

Verdict: accepted for exact feasibility of the pinned rational certificates.
This is an external reviewer report, not an assurance-ledger update or a review of the
writer’s final registration implementation.
An accepted review must be mapped to the retained artifacts before its repository
assurance status changes.

The source is `itsnaka/squish-certs` revision
`5e32bbd7028b6e3b869979278079cd37ed6770aa`, directory `squish-submission-2026-10-07`.
The thirteen bounded JSON files were acquired into `raw/`; `acquisition.json` records
their pinned URLs, sizes, and external-source SHA-256 values.
Duplicate JSON keys and inexact numeric coordinate inputs are rejected by the existing
packet parser. No upstream program was executed.

## Decision and replay

All thirteen complete certificates pass both
`devtools.check_rational_witness_independent` and `sqpack.witness.exact_verify`: **2,462
unit squares and 248,653 unordered pairs per checker**. Positive replay took **108.598
seconds**, serially, with Python 3.14.7. The final process exited zero.
Every per-certificate receipt contains the full exact checker input and both verdicts;
`summary.json` records aggregate counts and time.
The twelve genuinely new geometries contain 2,309 squares and 237,025 pairs per checker.
The duplicate n153 replay completed in 4.596 seconds before the parent requested reuse;
the original eleven-certificate suite was not rerun.

The source declares center coordinates x,y and rational t=tan(theta/2). Set
c=(1-t²)/(1+t²), s=2t/(1+t²), u=(c,s), and v=(-s,c). The denominator is positive for
rational t; c²+s²=1 and u·v=0. Corners are center ±u/2 ±v/2 in cyclic order.
The reviewer independently re-derived the corners with the sign-pair formula and
compared every exact coordinate to the adapter output.
There is no trigonometric rounding, dilation, or side inflation.

Both deciding routes check unit edges, right angles, all corner containment
inequalities, and exact separating axes.
The independent checker also checks opposite-edge closure.
The independent route enumerates every unordered pair with `itertools.combinations`; the
native route calls `verify_packing` with `bucket=False`. Every measured pair count
matches n(n−1)/2. Closed-square boundary contact is permitted; interior overlap is not.
The routes have independent geometry implementations, but share the serialized corner
input and basic Python rational arithmetic.
The separate conversion check addresses that shared input boundary; this is not a third
independent SAT implementation.

Two full-size negative controls retain all 123 squares.
Duplicating square 1 as square 2 is rejected by both routes with a genuine overlap; the
independent worst gap is exactly −1. Translating square 1 left by twice the side is
rejected by both routes with exact containment clearance
−3265365246780355/140737488355328. Each control still checks all 7,503 pairs in each
route. The controls took 7.684 seconds total.
`controls.json` preserves complete mutated inputs and failure results.

## Source identity and displays

The new n153 file has SHA-256
`4035079327be66751ccf03a69b27be2a5c267624cbd5a005da9aba7209eb87a9`, equal to the
original attachment acquisition record.
Its normalized facts are identical to the old facts, and its full exact checker input
equals the retained old witness.
Its exact side is 7250614903299225/562949953421312. It is a newly pinned source location
for an existing geometry, not a new witness discovery.
See `n153-comparison.json` and `lineage-comparison.json`.

Counts 126,129,154,155,238 strictly improve their earlier exact rational sides; this
comparison used exact subtraction, not displayed decimals.
Seven counts are additional to the completed eleven: 123,179,208,237,239,258,263. Thus
there are eighteen selected counts and twenty-three distinct geometries when the five
superseded geometries remain in history.
The source’s phrase eight new counts is relative to its original ten-file request, which
omitted the separately supplied n153 attachment.

The source decimal is a quotation, not a proof bound.
The verified display is the least upward decimal ceiling at the source’s sixteen-place
precision. The reviewer checked ceiling−10^-16 < exact side ≤ ceiling for every row.
Some source prints are below the exact side; n129’s source print is above the least safe
ceiling. These differences must remain explicit, and issue-table truncations must not
replace the exact side.

| n | Source print | Least upward ceiling | Pairs per checker |
| --- | --- | --- | --- |
| 123 | 11.6009077785163406 | 11.6009077785163406 | 7503 |
| 126 | 11.7733036066072394 | 11.7733036066072403 | 7875 |
| 129 | 11.8793752067111296 | 11.8793752067111287 | 8256 |
| 153 | 12.8796793733329640 | 12.8796793733329640 | 11628 |
| 154 | 12.9265622458535390 | 12.9265622458535390 | 11781 |
| 155 | 12.9525032026045128 | 12.9525032026045129 | 11935 |
| 179 | 13.8913125657406979 | 13.8913125657406980 | 15931 |
| 208 | 14.9245187720328190 | 14.9245187720328190 | 21528 |
| 237 | 15.9036762351906287 | 15.9036762351906287 | 27966 |
| 238 | 15.9261468570124709 | 15.9261468570124710 | 28203 |
| 239 | 15.9493131697291908 | 15.9493131697291908 | 28441 |
| 258 | 16.5634480021391539 | 16.5634480021391540 | 33153 |
| 263 | 16.7404464800428698 | 16.7404464800428692 | 34453 |

## Attribution and evidence limits

The reviewed issue comment 6043191866 was created at 2026-10-07T17:27:53Z and edited at
18:33:04Z. The later-created summary comment 6043263840 has creation/read-through time
17:32:04Z; the edit time is a separate fact.
`source-claims.json` preserves both bodies and timestamps.

Credit remains Nate Chaoweeraprasit with SQUISH. The edited author statement credits
Francisco Couzo’s seed packings for 123,126,129,155,179,208,237,239,258,263 and own
seeds for 153,154,238. Its specific seed counts and graft/removal descriptions should be
retained as author-reported lineage.
Mathematical feasibility does not reproduce that search history or establish an
original-discovery claim.
The author explicitly reports AI assistance and personal direction, management, review,
and steering; record that disclosure without treating it as independent verification of
oversight.

The reported upstream SQUISH and Ellsworth checker outcomes and unsuccessful further
squeezes are author assertions.
Neither producer checker was executed in this review.
No global optimality, exhaustive search, historical priority, or independently audited
human oversight follows from these rational feasibility checks.
The evidence supports feasible upper bounds for the exact sides.

No tracked source, assurance record, bead, GitHub object, or configuration was changed
by this review. Raw upstream assets and reviewer outputs remain outside Git.

## Retained Replay Custody

The filenames above identify the completed reviewer run.
Its original thirteen-case summary, including the duplicate n153 timing, is retained
under `original_batch` in
`packing/resources/web/squish-401-update-2026-10-07/receipts/replay-summary.json`. The
twelve new geometries’ complete inputs and verdicts are retained in
`receipts/certification.json.xz`, and both complete 123-square controls in
`receipts/negative-controls.json.xz`. The twelve-case positive wall time is 104.001
seconds; the thirteen-case 108.598-second measurement is reused.
The source URLs, byte counts and acquisition digests remain in
`acquisition/sources.json`; normalized geometry is in `facts/`. Raw upstream assets
remain external. n153 keeps its original certificate and evidence; this retained review
adds no n153 assurance.
The comparison and lineage facts remain in `acquisition/n153-comparison.json` and
`acquisition/frontier-comparison.json`. Issue comments are cited in the packet README.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
