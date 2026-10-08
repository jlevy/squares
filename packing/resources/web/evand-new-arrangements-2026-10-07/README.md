# Evan Daniel’s Three New Arrangements

[Issue #399](https://github.com/jlevy/squares/issues/399) supplies complete rational
packings for n = 266, 270 and 272 from
[evand/square-packing](https://github.com/evand/square-packing) at
`7eef24f7221b8c3371d6171dd664b52541bbd479`. Nine source files, including all three
certificates, both source checkers, format explanation, licences and credits, are
retained unchanged. Acquisition digests bind the downloaded source bytes.
Duplicate upstream aliases are not repeated.

## Exact Feasibility

T-119 certifies the following upper bounds.
Each display is the least upward sixteen-place ceiling of its complete rational side,
without side inflation.
The full side and every ordered pose remain in `facts/complete-certificates.json.xz`.

| n | Verified ceiling |
| --- | --- |
| 266 | 16.8230287507564760 |
| 270 | 16.9378072284460292 |
| 272 | 16.9681101457696006 |

Both project exact implementations accepted every square, wall and pair in all three
original packings. Both rejected a complete duplicate-square roster and a complete
outside-container roster for each count.
All nine complete deciding inputs and all 18 full native outputs, including exact
rational minima, are retained in `receipts/exact-certification.json.xz`: 650,496 pair
decisions across the two routes.
A separately prompted mathematical reviewer reran every job and obtained identical
non-timing native results in 202.090 seconds.
[The review](../../../../docs/project/reviews/review-2026-10-08-evand-new-arrangements.md)
discloses the shared strict conversion and rational arithmetic.

`devtools.evand_arrangement_reports` strictly admits the entire pinned source roster and
every result on each call.
Explicit replay repeats the geometry.
No source checker was executed or imported.
The two project routes independently implement the same separating-axis theorem; this is
implementation diversity within one method.

The case records and atlas use each complete new pose with its exact side.
The private worker copies the full facts and receipts and admits only three explicit
atlas read links; producer guards refuse writes through those links.
Earlier #375 source `13ee36e`, its T-098/T-101 results and their certificates retain
their original poses and assurance.
Complete pre-adoption case text is preserved in `acquisition/prior-state.json.xz`.

## Scope and Credit

The source reports new arrangements, KKT points, numerical local-minimum evidence and
search history. Feasibility does not establish arrangement novelty, local or global
optimality, rigidity or human oversight.
Those additional claims remain attributed reports in the retained issue text and source
explanation.

Evan Daniel authored the source with disclosed Claude assistance under his direction.
The reported lineage is Ellsworth’s 2024 record for n266 and Couzo’s September record
for n270. The n272 seed instead comes through Cleemann; Arslanov, Mustafin and
Shangitbayev’s s210 conversion; Ellsworth; and Stead’s June refinement.
The source credits the Squares Project (Joshua Levy) register data under CC BY 4.0.
Original MIT licences and `s12/CREDITS.md` are preserved.
The n17 work remains with its existing owner.

## Retained Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source evand-new-arrangements-2026-10-07 --check
uv run --frozen --all-extras --group dev python -m devtools.evand_arrangement_reports check
uv run --frozen --all-extras --group dev python -m devtools.evand_arrangement_reports check --replay
```

Source acquisition checks bytes; ordinary admission checks complete scientific
applicability. Only explicit replay repeats both geometric decisions.
The `certify` command retains individual full subprocess results in an external
`--jobs-dir` and publishes a receipt only after all nine jobs pass their required
outcomes.

## Worker-copy efficiency check

This bounded efficiency iteration compares repeated named-file copies with one copy per
declared destination.
Accept it only if the actual production clone retains both complete scientific inputs as
independently mutable private files, copies each once, preserves separate alias
destinations, rereads mutations on later invocations, and fits the unchanged
201,326,592-byte source cap.
The 45-second linked admission ceiling also stays unchanged.
No geometric input or native verdict is removed.

The baseline at the first complete #399/refinement integration measured 201,400,080
bytes, 73,488 bytes over the cap, and the production-clone test refused at that guard.
The proposed roster deduplicates identical declared paths per invocation, without
resolving aliases or caching filesystem validity.
Results follow the actual clone and mutation checks; external storage and concurrent
host activity preclude a pristine-host latency claim.

The actual production clone and its mutation checks pass, including one copy of each
complete private scientific input and refusal of a changed receipt on a later call.
The separate alias/counting and unchanged-cap refusal regressions also pass.
At the measured candidate tree, the retained `python -m devtools.run_negative_controls
--source-bytes` command reports 200,849,695 bytes with 476,897 bytes of headroom and
606,622 bytes of avoided repeated named copies.
On that same tree, repeated copies would count 201,456,317 bytes.
The earlier baseline predates the final refinement and generated-view refresh and is
retained as an earlier observation.

The storage acceptance rule passes.
This is not a measured latency improvement: the four production/alias tests took 451.11
seconds on this host, dominated by private Git indexing on the external volume.
Linked admission and post-mutation rejection each completed within their unchanged
45-second subprocess bounds.
Final footprint checks include the completed review and this record.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
