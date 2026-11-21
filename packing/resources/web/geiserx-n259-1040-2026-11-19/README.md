# GeiserX’s 259-square packing and de Winter’s rational certificate

[Issue #1040](https://github.com/jlevy/squares/issues/1040) links the original
[attachment](https://github.com/user-attachments/files/35066502/packing-259.zip).
This packet retains its factual geometry and comparator, bound to their measured byte
lengths and SHA-256 digests in [the acquisition record](acquisition/sources.json).
The raw ZIP is 446,768 bytes.
Its embedded commit records the attachment’s own revision.
The archive binds the bytes used here.

Sergio Fernández Rubio (GeiserX) constructed the packing by joining bands from his 292-
and 445-square layouts.
Joost de Winter, with OpenAI Codex as credited in the attachment, refined the
coordinates and supplied the exact certificate.
The original [GeiserX packet](../geiserx-squares-in-squares-2026-11-18/README.md)
retains his CC BY 4.0 licence and NOTICE, including credit to Sergio Fernández Rubio
(GeiserX), https://github.com/GeiserX/squares-in-squares.
Nevska’s earlier score comes from a leaderboard without coordinates.
The attachment attributes the earlier record to Nate Chaoweeraprasit, PingYou Ltd and
Evan Daniel.

The two original geometry files represent the same 259 squares.
The centre and half-angle file gives an upward 12-place print of **16.590016439230**.
The derived JSON copy retains every coordinate and the exact side.
Its only semantic change is naming the informational decimal `side_decimal_info_only`.
The original corner file is retained as supplied.
The reading-copy receipt documents the separate metadata and identifier normalization
used in an earlier parser check.
Sergio Fernández Rubio’s direct CSV rows at 259 preserve the published row order, header
and decimal lexemes from the pinned upstream archive.

The maintained exact algebraic comparison places the rational certificate about
0.001361706267708597 below the existing T-193 house.
The portable reader’s exact Option D comparison establishes a refinement of the public
GeiserX arrangement.
Its direct-reader contraction to first contact stops about 1.08266561 × 10⁻¹³ above the
refined side. The corresponding measurements and custody are reported in the retained
JSON receipts. The exact corner encodings have 129 and 77 non-axis-aligned squares
respectively. The maintained identity measures at two rational midpoint precisions count
59 and 49 turns of at least one degree, and find that no box symmetry pairs the nearest
centres one to one. That comparison establishes distinct arrangements at the measured
scale. Independent mathematical review remains separate.

## Controlled replay plan

The replay uses repository code and the normalized centre and half-angle file.
First compare its roster, exact side and all corner sets with the submitted encodings.
Both maintained routes must accept the original, reject a duplicated square for overlap
and reject a square translated outside the box for containment.

Run all eleven sharp controls from the maintained upper-bound harness.
The wall, tightest pair and collective translation tests must accept at contact and
refuse the specified penetration at 10⁻³⁰ past contact.
Enlarged squares must fail the unit-shape check.
Where the enlargement passes contact, it must additionally fail clearance or overlap
under the harness’s exact predictions, including its zero-clearance rules.

This packet retains the mathematical data and comparison receipts.
It leaves registration and adoption to the separate reviewed stages.

## Replay receipts

Both maintained routes accepted the source geometry, checking 33,411 pairs, and declined
the duplicate and outside-box controls.
All eleven sharp controls matched their exact predicted outcomes.
The retained replay used one worker and generated `receipts/exact-certification.json.xz`
and `receipts/sharp-controls.json`.

Run `replay_n259.py` and `compare_t193.py` with the project interpreter from `packing/`.
The identity program compares against the T-193 witness at the intake revision; after an
adoption, a replay should use the witness of T-193 from that earlier revision.
It writes `receipts/identity-t193.json`.

## Compressed Files

| Stored file | Origin | Git blob of uncompressed bytes | Decompressed SHA-256 |
| --- | --- | --- | --- |
| `derived/geiserx-n259.csv.gz` | receipt | `ca232138adc5764399bed3917c91f03cedc5c07f` | `89595f52e350c2025906f1f1e06baf64c26f10af6f999f043ef171445369f659` |

## Original Gzip Files

| Stored file | Origin | Git blob of stored bytes | SHA-256 of stored bytes |
| --- | --- | --- | --- |
| `source/upper/n259/packing.json.gz` | upstream | `1f3f35e872c9c6637cc9c745f586fd6aedd29c0b` | `bfd1b2890ad846efe030113f5e4535a79f786ed6c2f0371257dd342ddd48970c` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
