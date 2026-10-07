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

## Independently Re-implemented Exact Checks

This repository confirmed T-113 and T-114 by independently re-implemented exact-rational
checks, at V3/C3. The native `sqpack.witness.exact_verify` and
[`devtools.check_rational_witness_independent`](../../../devtools/check_rational_witness_independent.py)
accept every original packing after complete unit-square, pair and container-wall tests.
Each route decides all 177,440 pairs over the eleven packings.
The conversion uses the source’s exact rational side and introduces no dilation or
rounding.

The two deciding routes implement the same separating-axis theorem separately.
They share the converted rational corners, YAML infrastructure and Python
integer/`Fraction` arithmetic.
They share no SQUISH verification code.
The source’s own exact checker and Ellsworth numerical checks remain reports; neither
producer checker was reproduced here.

The
[mathematical review](../../../../docs/project/reviews/review-2026-10-06-squish-upper-bound-packings.md)
re-derives the half-angle conversion, unit-square shapes and complete geometric
decisions. The separately prompted
[correctness review](../../../../docs/project/reviews/review-2026-10-06-squish-import-correctness.md)
accepts the strict input, source/fact/witness/receipt bindings and invalid controls.
Both are accepted project AI reviews.
Their reproduced roster and receipt defects were fixed and regression-tested.
No human oversight record is retained.

The [`certification receipt`](receipts/certification.json) records all eleven complete
dual decisions and the rational witness paths under
[`packing/witnesses/squish-401-2026/`](../../../witnesses/squish-401-2026/). The
[`negative-control receipt`](receipts/negative-controls.json) records two mutations of
the 108-square certificate: duplicate one square to force interior overlap, and move one
square outside the container.
Both checkers refuse both controls after examining all 5,778 pairs.
The [receipt regression tests](../../../tests/test_squish_upper_bound_receipts.py)
reject forged successes, incomplete rosters, inconsistent diagnostics and broken
provenance bindings.

The verified decimal ceiling is the exact certificate side rounded upward at sixteen
decimals; the case’s `exact_form` remains the original certified rational side.
The receipt’s `exact_form` and `certified_side` retain that same source rational.
Both bound lanes use this safe decimal display of the source’s exact rational claim. The original source finite display is retained here, in acquisition and original
claims metadata, and in the replay receipt.
At five counts the upward ceiling is smaller than the source display, which was farther
above the exact fraction; at four it is one unit above a display that lay below the
fraction.

| n | Source display | Verified ceiling | Pairs per checker |
| --- | --- | --- | --- |
| 108 | $10.9206589394033085$ | $10.9206589394033085$ | 5778 |
| 126 | $11.7735852916961079$ | $11.7735852916961071$ | 7875 |
| 129 | $11.8808935876459927$ | $11.8808935876459918$ | 8256 |
| 130 | $11.9044830325168771$ | $11.9044830325168772$ | 8385 |
| 153 | $12.8796793733329640$ | $12.8796793733329640$ | 11628 |
| 154 | $12.9282936576777576$ | $12.9282936576777577$ | 11781 |
| 155 | $12.9536770693532741$ | $12.9536770693532733$ | 11935 |
| 180 | $13.9236350042524233$ | $13.9236350042524224$ | 16110 |
| 209 | $14.9496179522017929$ | $14.9496179522017921$ | 21736 |
| 238 | $15.9294090272583144$ | $15.9294090272583145$ | 28203 |
| 303 | $17.9203123729203497$ | $17.9203123729203498$ | 45753 |

From `packing/`, reproduce all geometric decisions and both controls with:

```shell
uv run --frozen --all-extras --group dev python -m devtools.squish_upper_bound_packets check --replay
```

`check` without `--replay` holds the retained receipts to their decided inputs,
provenance, rosters and diagnostics; it does not replace geometric replay.
Each receipt records the complete semantic deciding input: count, rational container
side, unit-square side and the rational corner/id roster.
The fast check compares that input to the current witness while ignoring nongeometric
metadata. External source byte digests remain the acquisition trust boundary.
Git owns the retained implementation and publication history.
The normalized [release claims](acquisition/release-normalized-claims.json) and
[supplement claims](acquisition/supplement-normalized-claims.json) expose those safe
displays to the coverage checker while linking the original finite displays and exact
fractions. The normalization raises four source displays by one final-place unit,
tightens five overly high displays by eight or nine units, and leaves two unchanged.
No certificate establishes local or global optimality or rigidity.

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
