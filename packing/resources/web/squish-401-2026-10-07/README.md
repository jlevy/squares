# SQUISH Rational Packing Upper Bounds, 7 October 2026

Nate Chaoweeraprasit (itsnaka), using SQUISH, reports new rational packing upper bounds
at eleven counts in [jlevy/squares#401](https://github.com/jlevy/squares/issues/401):
ten in the pinned repository release and one in the later
[n = 153 supplement](https://github.com/jlevy/squares/issues/401#issuecomment-6031977107).
The ten-count release is registered as T-113; the supplement as T-114. They establish
upper bounds only. The source supplies no global or local optimality or rigidity proof.

## Source and Credit

| Field | Value |
| --- | --- |
| Repository | [itsnaka/squish-certs](https://github.com/itsnaka/squish-certs/tree/07fe6dde1e5b67405a3076719b90e58e2882b677/squish-submission-2026-10-06) |
| Revision | `07fe6dde1e5b67405a3076719b90e58e2882b677`, authored and committed 2026-10-07T02:28:19Z |
| Release subject | `squish-submission-2026-10-06/`, certificates at n = 108, 126, 129, 130, 154, 155, 180, 209, 238 and 303 |
| Supplement | The n153 rational certificate attachment in issue comment 6031977107, published 2026-10-07T05:59:18Z; its download address and SHA-256 are in the manifest |
| Bibliography keys | **[SQUISH ten packings 2026-10-07]**, **[SQUISH n153 2026-10-07]** |
| Human credit | Nate Chaoweeraprasit after David Ellsworth: the author says he built on Ellsworth’s records and tools, including `parse_svg_packing.py` |
| AI assistance | The author states that SQUISH’s solver, verification and issue were written with Claude Opus 5.5 under his direction, management, review and steering |
| Licence | The repository publishes no LICENSE; the attachment grants no separate reuse terms |
| Retrieved | 7 October 2026, with per-source retrieval metadata in the manifest |

The repository README names SQUISH, expanded as “SQuare-packing Using Iterative
Shrink-Hopping.” The issue supplies the human credit and AI disclosure above.
Nine original packings were seeded from the author’s own certified neighbouring-count
packings, with squares removed or added, then searched and polished; n = 126 came from a
nearby search started at the published record.
The source does not credit this project’s methods, so the bibliography records
independent lineage.

## Retained Facts and Claims

The [known-best retention policy](../known-best-packings/README.md) permits derived
geometry facts and attribution metadata from sources without a licence.
This packet retains:

- [`facts/`](facts/): eleven compressed factual records, each with the exact rational
  side, rational centres and half-angle parameters from the submitted certificate
- [`acquisition/sources.json`](acquisition/sources.json): source addresses, the pinned
  revision, original file sizes and SHA-256 digests, exact sides and decimal displays,
  with `raw_asset_retained: false`
- [`acquisition/release-claims.json`](acquisition/release-claims.json) and
  [`acquisition/supplement-claims.json`](acquisition/supplement-claims.json): the two
  publications’ decimal upper-bound displays, reparsed by the coverage checker
- [`acquisition/frontier-comparison.json`](acquisition/frontier-comparison.json): the
  previous reported and verified bounds and their sources at the eleven counts

No upstream README, certificate file, drawing, screenshot, summary table or
checker-output file is retained.
The source assets are acquired ephemerally; their digests identify what was read across
that trust boundary.

Each source certificate gives rational `(x, y, t)`, with `t = tan(theta/2)`. The
identities

$$
\cos\theta = \frac{1-t^2}{1+t^2},\qquad
\sin\theta = \frac{2t}{1+t^2}
$$

make the orientation an exact unit vector.
Complete pair and wall tests over these facts can establish feasibility without
reproducing the search.
The exact rational side is the claim.
The source’s `s_decimal` is a finite display, below the rational side at n = 130, 154,
238 and 303; a verified decimal bound must round the fraction upward.

The source reports its own exact `Fraction` checks and David Ellsworth’s numerical
checks with epsilon `1e-40`. Registration records those reports at V0/C0. Complete
replay, invalid controls and an independent mathematical review are queued under
`think-mc4u`, and the verified case bounds retain their earlier packings until that work
is recorded.

From `packing/`, the reusable
[`devtools.squish_upper_bound_packets`](../../../devtools/squish_upper_bound_packets.py)
acquires the source facts and checks the packet.
The confirmation change will retain its exact replay receipts and rational witnesses
separately from this reported registration.

## Derived Fact Files

The packet stores derived rational geometry as deterministic gzip.
The bounded source reader and semantic-input checks validate these files; Git records
their retained versions. Original upstream byte digests remain in the acquisition
manifest.

| Stored path | Squares |
| --- | --- |
| `facts/n-108.json.gz` | 108 |
| `facts/n-126.json.gz` | 126 |
| `facts/n-129.json.gz` | 129 |
| `facts/n-130.json.gz` | 130 |
| `facts/n-153.json.gz` | 153 |
| `facts/n-154.json.gz` | 154 |
| `facts/n-155.json.gz` | 155 |
| `facts/n-180.json.gz` | 180 |
| `facts/n-209.json.gz` | 209 |
| `facts/n-238.json.gz` | 238 |
| `facts/n-303.json.gz` | 303 |

From `packing/`, regenerate complete verification receipts with
`uv run --frozen --all-extras --group dev python -m devtools.squish_upper_bound_packets certify --workers 2`,
then replay them with the same command prefix and `check --replay`.
These commands compare exact deciding geometry; descriptive metadata is outside that
comparison.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
