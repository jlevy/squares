# Joost de Winter’s 305-Square Packing

Joost de Winter submitted a rational certificate for $s(305) \le 17.945755838742$ on
[issue #1052](https://github.com/jlevy/squares/issues/1052). He refined the arrangement
credited to Tomáš Kodaj and JoeGun in T-309. The submitted side rounds the exact
rational side upward to 12 places.
The
[independent stage 4 review](../../../../docs/project/reviews/review-2026-11-20-de-winter-1052-n305.md)
accepted the certificate and classified it as a new result under Option D.

## Retained Source

The
[original commit](https://github.com/JoostdeWinter/square-packing/tree/db8efcb6bf05906e977bc62f1f6d8ccfcaa296ef/n305)
dates to 20 November 2026 at 17:50:11 UTC. The intake retrieved it on 21 November UTC
and checked the exact file bytes against the pinned Git tree.
The [acquisition manifest](acquisition/sources.json) records which files the packet
retains and which it pins.
The
[registration checksum list](https://github.com/JoostdeWinter/square-packing/blob/5282edd875419bef5a19da1fa726fec53ff04a47/n305/SHA256SUMS)
from a later commit reports the same digests for both certificate files.

The primary input is [n305_exact.json](source/n305/n305_exact.json.gz).
The retained [n305_witness.yaml](source/n305/n305_witness.yaml) is the original corners
serialization.
The independent reviewer documented missing claim and envelope metadata in
that file and checked a repaired reading copy against the primary input.
The acquisition records the original bytes.

De Winter’s repository states the MIT licence.
The root licence matches the copy retained in the
[17 October de Winter packet](../de-winter-upper-bounds-227-229-260-2026-10-17/source/LICENSE).
The source credits OpenAI Codex for search, optimization and certificate work, and
Anthropic Claude for repository files, checks and the figure, under de Winter’s
direction.

## Maintained Replay

The [controls plan](receipts/controls-plan-1052-n305.md) specifies the maintained
replay.
Both maintained routes accepted the exact JSON certificate and rejected the
duplicate-square and outside-container controls. The
[maintained receipt](receipts/exact-certification.json.xz) records 278,160 pair
decisions across the three jobs and two routes, with 111.30 seconds of verifier CPU
time.
All 11 [sharp controls](receipts/sharp-controls.json) returned their planned outcomes.
The merged blind review already records the independent exact geometry checks and
the comparison with T-309. The [305 case record](../../../frontier/n-305.md) gives the
standing of the registered packings.

## Compressed Files

| Stored file | Origin | Upstream Git blob | Decompressed SHA-256 |
| --- | --- | --- | --- |
| `source/n305/n305_exact.json.gz` | upstream | `355cbe46ff685c00c1bb292443b974084dc0b9c4` | `e6c7d0280396a2fa61804a24a7c757365320869dbb89e8cf94316bb8b6a7831f` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
