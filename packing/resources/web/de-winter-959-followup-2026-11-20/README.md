# De Winter’s algebraic certificate for 179 squares

[Joost de Winter’s comment on #959](https://github.com/jlevy/squares/issues/959#issuecomment-7050119161)
submits an algebraic reconstruction of Doğa Özden’s diagonal-band packing after Ryan
Xu’s 70-square construction and Evan Daniel’s refinement. De Winter credits OpenAI
GPT 6.2 Astra for assistance. The attachment names Sergio Fernández Rubio (GeiserX) as
the source of the numerical starting coordinates. The stated input
`inputs/poses/n179_GeiserX.json` and its source revision are missing from the bundle.
Its exact digest is in [the acquisition record](acquisition/sources.json).

## Source and exact side

The [attachment](https://github.com/user-attachments/files/35184249/n179-exact-construction.zip)
is 34,150 bytes, with SHA-256
`143e9298eaf8c96e0e36bd7346a41b765e1d8e77dc1be10c76e17846ce73c3c8`.
Its ten manifest rows matched. This packet retains the submitted mathematical
certificate and the GeiserX credit and CC BY 4.0 notices. The package’s verification
licence identifies n = 232 and n = 270. Its scope at n = 179 is unclear, so the
contributor’s verification programs and prose stay outside the packet.

The side begins `13.88096037155557959469669157…` and is the isolated root of the
degree-five integer polynomial in the certificate. Exact arithmetic in the stated real
number field gives `S179 = L70 + 5 = L207 − 1` for the two published retained
certificates, with the generator mapped by `t = −alpha`. The
[side comparison](receipts/side-comparison.json) puts it about
`2.64542659e-12` below T-294 and `7.94241969e-14` below T-294 contracted to first
contact. Those measurements supply the comparison under Option D.

## Finite feasibility

The maintained number-field verifier and the independent algebraic witness checker
accepted the [reading copy](derived/n179-reading.yaml) on all 15,931 pairs, with 417
touching pairs. Both refused the four stated negative controls on two-square slices,
including overlap and wall escape at `1e-30`. The
[slice plan](receipts/finite/finite-slice-plan.json) and
[run summary](receipts/finite/summary.json) record the scope. The retained reading copy
changes the schema reference to match its repository location. The source certificate
is byte-for-byte the original. This is a finite-feasibility result.
The [source-only review](../../../../docs/project/reviews/review-2026-11-21-n179-independent-algebraic-certificate.md) separately checks the full geometry.

## Compressed Files

| Stored file | Origin | Git blob of uncompressed bytes | Decompressed SHA-256 |
| --- | --- | --- | --- |
| `review/n179-independent-2026-11-21/frozen/run-02/pairs.jsonl.gz` | receipt | `e4f50e755f9cf9b125d71f7c45e1b4cdf3c50ef8` | `490db2ee08edb4592efbe262da4909ccbe1cfb4eb9e61c1ff3199b8331579332` |
| `review/n179-independent-2026-11-21/frozen/run-02/walls.json.gz` | receipt | `be9624b6885b4b16b30feaa95aaf8c3f77348a74` | `eca9a211b08e0b50d03ac41bf8de31c5f0ae280573b71a32d70020b419709d92` |

## Original Gzip Files

| Stored file | Origin | Git blob of stored bytes | SHA-256 of stored bytes |
| --- | --- | --- | --- |
| `source/n179.minpoly.json.gz` | upstream | `89a24c6d7c8a55bebfb2e3a08e80e1b1f8231cb9` | `28edf9561e87037b5c681e4ff0051a1bd1b8e5401c1a8376fe2e66c2c18663d1` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
