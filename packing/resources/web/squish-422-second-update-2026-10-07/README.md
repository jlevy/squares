# SQUISH Second Update: Nine Reported Rational Upper Bounds

Nate Chaoweeraprasit (itsnaka), using SQUISH,
[reports nine new or smaller packings](https://github.com/jlevy/squares/issues/422).
The source is pinned to
[`e63e4e52b1728b6671b2f263c5e02a4aa79a39d3`](https://github.com/itsnaka/squish-certs/tree/e63e4e52b1728b6671b2f263c5e02a4aa79a39d3/squish-submission-2026-10-07b),
published and retrieved on 7 October 2026. This reported layer registers T-116 at
V0/C0. Complete earlier verified bounds remain in their own case lanes; no earlier
certificate confirms the smaller geometry merely because it has the same count.

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
This packet contains only attributed normalized rational geometry, brief claim facts
and acquisition metadata. The source SHA-256 and byte count apply at this external
acquisition boundary; local applicability follows complete exact semantic values.

The author credits Kingbird's catalogue, maintained by David Ellsworth, for the
s(41) and s(37) seeds of n88 and n199; Francisco Couzo for the s(180) and s(297)
seeds of n179 and n263; and SQUISH's own intermediate packings for the other counts.
This is author-reported lineage, not an independently established construction
history. Seed credit does not mean that a seed author found this new pose.

The author discloses Claude Opus 5.5 coding and research assistance under his own
direction, management, review and steering, including solver, verification and filed
issue preparation. He credits David Ellsworth's numerical checker. His reports of
checker success, nearby search and squeeze are retained as source claims, with no
project feasibility, optimality, rigidity or human oversight conclusion.

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

Its `record` command reconstructs the selected reported lanes while keeping the
historical verified lanes. Its `atlas --jobs 2` command rebuilds only these nine
house witnesses and drawings, preserves the other 315 entries, and refreshes the
complete source and figure metadata. It refuses an unselected case's changed side
or source plan. An exact drawing check establishes the visualization geometry;
result confirmation requires separately retained complete replay and scoped review.

No externally completed feasibility receipt or review is admitted by this reported
packet. A separate confirmation layer must bind all nine unchanged source sides,
complete witnesses, full checker inputs, both complete-roster geometric controls
per case, actual dual verdicts and two freshly prompted scoped reviews before
promoting verified lanes.

<!-- This document follows common-doc-guidelines.md. -->
