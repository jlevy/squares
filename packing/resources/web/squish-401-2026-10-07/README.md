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

## Compressed Files

Derived packing facts are stored as deterministic gzip.
The table identifies the decompressed facts, which are repository-generated receipts
rather than upstream files.

| Stored path | Origin | Git blob of decompressed bytes | SHA-256 of decompressed bytes |
| --- | --- | --- | --- |
| `facts/n-108.json.gz` | receipt | `82a3d82b7b70e4e5bb54bd9a4b4a3ebd1fb4ee7f` | `57315c199e13f91e9027d2964cfe5e8fd2fd73e9b6e44a084f9b9fd44300cc02` |
| `facts/n-126.json.gz` | receipt | `f9c86b60cd6e6cb3d41df8943d7b9c8cc4f34c7d` | `dc219ae63ad31bba1f188900922bd24dc12c8c968311246964c143a2fa5d4c6e` |
| `facts/n-129.json.gz` | receipt | `ca35fb3899028c740cf29e6eed0e6307861d5ba5` | `07e279e2647be9f20f3c21d76e18dccb3627082d3446fb937a9ff6a03c18d9aa` |
| `facts/n-130.json.gz` | receipt | `6aac09473b0bdda45e4fbb787511a4f5835ea4ab` | `43d736676d32e47ca274d7d188f26a30ca32597961661dc9a70a65360ba39445` |
| `facts/n-153.json.gz` | receipt | `d271754f8f269ca5e2cb5576b36dbb338cfd757f` | `49d37a427984e9e7301cd81a539fdf7bbf39dcee4dfce56f55894f1da9f5da76` |
| `facts/n-154.json.gz` | receipt | `1cc802b87b1282a9c2324fd0f4f924751028eee8` | `8778a48f85a0d4997ce0be71e74a23a62b4463dce5a08e8cdc426479efa6d307` |
| `facts/n-155.json.gz` | receipt | `0f6ee13baaa11ccf37c6ab7cca85537797b1604a` | `7c90f44187ed98c01aacd4ade8cf3bf8c0fad0a7eb1bb8f44aaa19c0ea6b0980` |
| `facts/n-180.json.gz` | receipt | `443fdf1e1f621b5b4ab53e0ec86ec6c5be8308dd` | `96726b4f726017add9055d7fd898b6116768681d281945db1b13802bde9ff299` |
| `facts/n-209.json.gz` | receipt | `c5929ecb486fb75da50cf4c2646d824edc8f6cd2` | `695a78e65c4d53888664f6d22ce893a535873ceba2e59eeddd6b43ed26a15ffd` |
| `facts/n-238.json.gz` | receipt | `dd5e376668adbad2c6c9b4dc1929566befa6dd5d` | `99c3b0567857f537c415d660d3846e3f029be7f755c3e7308f66e132acb093b0` |
| `facts/n-303.json.gz` | receipt | `dec26911d9ddd5138d5ed70523472a89714232e2` | `6b7e9c55bd9b0fa524e2a9da6d263d7adcd9c773ff2264f0b7f1097f2c172b96` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
