# SQUISH Second Update: Nine Confirmed Rational Upper Bounds

Nate Chaoweeraprasit (itsnaka), using SQUISH,
[reports nine new or smaller packings](https://github.com/jlevy/squares/issues/422).
The source is pinned to
[`e63e4e52b1728b6671b2f263c5e02a4aa79a39d3`](https://github.com/itsnaka/squish-certs/tree/e63e4e52b1728b6671b2f263c5e02a4aa79a39d3/squish-submission-2026-10-07b),
published and retrieved on 7 October 2026. T-116 is confirmed at V3/C3: two local
exact routes accepted all nine unchanged rational packings, and two distinct scoped
AI reviews accepted their complete scientific replay evidence. Earlier certificates
remain evidence for their own source geometries.

Five counts are additional to the author's previous submissions: 88, 199, 207, 236
and 302. Four replace earlier SQUISH reports: 108 and 180 replace original-release
packings, while 179 and 263 replace first-update packings. The original eleven and
first-update thirteen source facts, their complete certificates, evidence, receipts,
reviews and finder credit remain retained. Together the source's original and two
update packets cover 23 distinct counts. The first update's unchanged n153 remains
provenance for its original certificate.

## Source, Attribution and Custody

No root licence file is published in the retained source tree. Raw JSON, producer
code, prose, drawings, numerical checker logs and screenshots remain outside Git.
This packet retains attributed normalized rational geometry, brief claim facts,
acquisition metadata and the project’s exact replay evidence. The source SHA-256 and byte count apply at this external
acquisition boundary; local applicability follows complete exact semantic values.

The author credits Kingbird's catalogue, maintained by David Ellsworth, for the
s(41) and s(37) seeds of n88 and n199; Francisco Couzo for the s(180) and s(297)
seeds of n179 and n263; and SQUISH's own intermediate packings for the other counts.
This is author-reported lineage, not an independently established construction
history. Seed credit does not mean that a seed author found this new pose.

The author discloses Claude Opus 5.5 coding and research assistance under his own
direction, management, review and steering, including solver, verification and filed
issue preparation. He credits David Ellsworth's numerical checker. His reports of
checker success, nearby search and squeeze remain source claims. The separate local
exact replay establishes feasibility; it does not establish optimality, rigidity or
independently audited human oversight.

## Exact Sides and Displays

All nine records retain exact rational centres and half-angle parameters for all
1,762 squares. Original finite source prints remain quotations. Each selected display
is the least sixteen-place upward ceiling of the exact rational side.

| n | Safe bound display | Author-reported seed |
| --- | --- | --- |
| 88 | 9.8824510304821347 | Kingbird s(41), grafted |
| 108 | 10.9099400734448775 | SQUISH s(110), two squares removed, nearby search |
| 179 | 13.8837954905121866 | Couzo s(180), one square removed, nearby search |
| 180 | 13.9176534174514757 | SQUISH s(182), two squares removed, nearby search |
| 199 | 14.6175721735980400 | Kingbird s(37), grafted |
| 207 | 14.8879922583077482 | SQUISH s(88), grafted |
| 236 | 15.8678008394255397 | SQUISH s(88), grafted |
| 263 | 16.7404196795387766 | Couzo s(297), carved, nearby search, squeeze |
| 302 | 17.8813062180958085 | SQUISH s(88), grafted |

For 179, 207, 236, 263 and 302, the source print lies below the exact side. For
example, n263 prints `16.7404196795387747`, while its exact side is
`9424018478849569/562949953421312`; the safe display is `16.7404196795387766`.
Neither source printing precision nor the metadata flag `squeezed` decides feasibility
or local optimality.

## Retained Records and Replay

[Acquisition metadata](acquisition/sources.json) retains each pinned source path, byte
count, source checksum, printed and exact side, safe display, metadata and lineage.
[Claims](acquisition/update-claims.json) enumerate exactly nine offered safe bounds.
[The historical comparison](acquisition/frontier-comparison.json) retains the
complete earlier reported and verified upper lanes. Normalized geometry lives in
`facts/n-NNN.json.gz`, one file per count.

From `packing/`, the reusable packet tool checks these records without a geometry
decision:

```shell
uv run --frozen --all-extras --group dev python -m devtools.squish_second_update_packets check
```

The reported-only packet's `record` command rebuilds its reported lanes and refuses
to promote a new confirmation. Its atlas producer reconstructs the nine exact house
witnesses and drawings. Atlas geometry and result assurance have separate evidence.

The confirmation adapter checks the complete retained run without executing either
geometry decider:

```shell
uv run --frozen --all-extras --group dev python -m devtools.squish_second_update_confirmation check-certification
```

Its `record` command updates the nine verified lanes only after full admission.
`restore-witnesses` reconstructs the canonical proofs from admitted facts. Add
`--replay` to `check-certification` to repeat both decisions for all three jobs per
case; `--n N` selects a case without weakening complete retained-roster admission.

The [certification index](receipts/certification.json.xz) maps nine canonical
`W-squish-422-nNNN` proofs to nine bounded complete case records. Each
`receipts/n-NNN.json.xz` retains its actual positive and both complete-roster control
receipts, all deciding inputs and full witness metadata. Historical execution paths
remain historical custody values. Canonical repository-relative proof IDs, fact
paths and replay instructions are a separately retained metadata transformation,
validated by equality of every ordered corner and complete scientific input.

The [replay protocol](receipts/replay-protocol.json) retains the original custody,
preparation manifest, execution summary, actual module and schema identities,
27 child exit statuses and outer exit status zero. The retained adapter and selected
schema are under `protocol/`. All nine positives passed both routes; all eighteen
controls were rejected by both. The positives contain 1,762 squares and 190,303 pairs
per route. All jobs account for 570,909 pairs per route, 1,141,818 across both routes.
The recorded per-job dual-route decision wall times sum to 222.246477794 seconds.
That sum is not the parallel batch elapsed time, which was not recorded.

The [mathematics review](../../../../docs/project/reviews/review-2026-10-07-squish-second-update-mathematics.md)
independently reconstructs the source rotation matrices and every complete corner.
The separately prompted [semantic-binding review](../../../../docs/project/reviews/review-2026-10-07-squish-second-update-semantic-binding.md)
checks all actual receipts, runtime identities and control outcomes. Their complete
reviewed inputs and structured decisions are retained in `reviews/` and the case
records. These accepted scientific reviews do not approve a later integration PR.

The two independently implemented SAT routes share the SAT theorem, Python
`Fraction`, YAML loading and serialized source-to-corner conversion. The separate
rotation-matrix review addresses that shared conversion. Exact sides remain
unchanged with zero dilation; source prints and safe ceilings stay separate.

The private negative-control snapshot copies every scientific input and review.
Nine canonical proof paths and eight specifically admitted generated house witness
leaves may be read through links only after complete semantic custody checks.
n263 remains private and indexed; registered mutations and existing document/result
consumers rescue private copies of any selected house leaf. All writers reject linked
outputs before creating figures or files. This keeps the existing 192 MiB private
snapshot ceiling without dropping source proofs, scientific evidence or controls.

<!-- This document follows common-doc-guidelines.md. -->
