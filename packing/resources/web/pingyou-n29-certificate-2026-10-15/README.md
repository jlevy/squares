# N29: A Tighter Exact Packing Certificate

PingYou Ltd submits a complete rational packing of 29 unit squares with a strictly
smaller enclosing side than its preceding published N29 certificate in [PR574][pr574].
The exact reduction is approximately **7.32482673606514 × 10⁻⁹⁰**. This submission
consolidates the three subsequent certificate improvements into one replacement.

The new certificate also improves the exact N29 upper bound currently registered by The
Squares Project by approximately **1.56616581892211 × 10⁻³⁶**, and Evan Daniel’s
motivating batch certificate by approximately **5.93383346269809 × 10⁻²⁰**. These
comparisons use full rational sides.
`claims.json` records the submitted side, and `comparison.json` records the exact
differences and named baselines.

## Complete Witness and Replay

The [versioned evidence release][] contains the complete portable certificate, its
lossless native Witness/v2 encoding, the preceding certificate, exact comparison data,
verification programs and replay receipts.
The [HostedData manifest][hosteddata manifest] pins the archive’s size and SHA-256.

The submitted portable certificate is `n29-certificate/certificates/n029.cert.json` with
SHA-256 `a01428c51875679fbe78c11a803742b8d99f44b916a660ab6801bb0fcf76951b`. All
coordinates and frame components are rational.
Verification checks unit-square geometry, containment and all 406 unordered square
pairs. The native encoding preserves the exact side, square order, centers and frames.

The displayed side begins
`5.93383346267692918968946061635201913843383418107788697463882591508025…`. The fraction
in the certificate is the claimed upper bound; the decimal prefix is for recognition
only.

The evidence includes independent exact native verification and portable separating-axis
and polygon-clipping checks, with invalid controls.
All 29 squares and 406 pairs are covered.
The archive contains its replay commands and receipts.

## Attribution and Scope

Credit **PingYou Ltd** for this numerical certificate refinement.
The construction retains the established credits to **Thomas Schadt** and **David
Ellsworth**; **Evan Daniel** is credited for the public exact-system and certificate
work used as a source.
The preceding regularized certificate from **Joshua Levy’s Squares Project** is retained
as a separate comparison baseline.

The result is a tighter exact upper certificate for the known N29 construction.
Its nominal construction value is unchanged.
This packet requests replacement of the N29 certificate from PR574; the other counts in
that submission retain their own evidence and dispositions.
The [result import process][] describes maintainer intake and registration.

[pr574]: https://github.com/jlevy/squares/pull/574
[versioned evidence release]: https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-n29-certificate-2026-10-15-v1
[hosteddata manifest]: ../../../hosted/pingyou-n29-certificate-2026-10-15.yaml
[result import process]: ../../../campaign/result-import.md

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
