# Doğa Özden’s 264-Square Certificate

Doğa Özden reports a rational packing of 264 unit squares at side
16.7721683050405463962634…, which rounds upward to 16.772168305041 at 12 places.
The original certificate lists the four rational corners of each square and establishes
a feasible upper bound.
[Issue #1099](https://github.com/jlevy/squares/issues/1099),
[pinned source](https://github.com/kenaznia-doga/s264-upper-bound-1677216830/tree/72c4d195c85b6099002ad6c675b27df40fdaceac)

## Comparison and Credit

The side is about 0.001639293 below T-308, the house at intake, and remains about
0.001639293 below it after contracting the predecessor to first contact.
It is about 0.000674848 below the earlier 264-square certificate from #1037. The source
discloses a side-only Kaggle entry at 16.770288527750 from its 9 November cache.
That entry supplies no coordinates.
[Exact comparison](acquisition/exact-comparison.json),
[retained #1037 report](../geiserx-exact-1037-2026-11-22/README.md),
[Option D](../../../campaign/result-import.md#several-reports-at-one-count)

Özden’s lab reports that it perturbed Tomáš Kodaj’s packing as JoeGun improved it
(T-308), annealed the arrangement and refined it with Evan Daniel’s ALM+SLP quench.
Claude agents worked under Özden’s direction.
Sergio Fernández Rubio (GeiserX) and Joost de Winter receive separate credit for the
#1037 result. [Source README](source/README.md),
[T-308 case history](../../../frontier/n-264.md#joeguns-certificate-t-308)

## Source Retention

The retained source consists of the exact YAML, the source README and the two licence
notices. The acquisition record binds the bytes to the commit dated 23 November 2026 at
10:55:30 UTC, 17 seconds before the issue.
The issue describes the certificate as centre and half-angle data.
The pinned README and the YAML identify the native representation as rational corners.
[Acquisition record](acquisition/sources.json),
[captured issue](acquisition/issue-1099.json)

The source licenses its certificate, data and text under CC BY 4.0 and its code under
MIT. The optimizer carries a separate MIT notice.
[Source licence](source/LICENSE.md),
[optimizer notice](source/LICENSE-evand-square-packing.txt)

## Maintained Replay

The maintained exact routes accepted the positive geometry and refused both
the duplicate-square and outside-container controls. Each job recorded all
34,716 unordered square pairs per route. Both routes used GMP arithmetic.
The additional sharp-control suite reached its 160-second wall limit before producing a receipt.
[Native replay](receipts/exact-certification.json.xz),
[runner](receipts/n264-gmp-native.py.txt),
[guard summaries](receipts/gmp-execution.json)

## Independent Review

The source-only checker accepted all 264 squares, 1,056 wall tests and 34,716
unordered pairs. The review records the rounded ceiling and the source’s wording
difference about the certificate format. The checker uses a direct integer
projection of exact corner coordinates.
[Independent review](../../../../docs/project/reviews/review-2026-11-23-ozden-1099.md)

## Compressed Files

| Stored file | Origin | Upstream Git blob | Decompressed SHA-256 |
| --- | --- | --- | --- |
| `source/n-264-candidate.yaml.gz` | upstream | `437a5af0200a8266509d644b96dc1f0b2044018c` | `e79b705387160903c31dd287575407c6ef8b2b6e89b6374bcd0a2d71b2939e25` |
| `review/check-result.json.gz` | receipt | `01e0074dfd5b0e2dca03ff8a35fbf3b924368827` | `ae729face30972a08edfd8b802e776b7e13fa0e64738029b443481a37c443fbe` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
