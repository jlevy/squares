# Mykhailo Polkovskyi’s Certificates of 23 October, e386aab to fbc1749

This packet retains the certificates that ten commits of 23 October 2026 (e386aab,
23:36:37Z, to fbc1749, 23:56:35Z) to Mykhailo Polkovskyi’s
[Mishapolk/square-packing-records](https://github.com/Mishapolk/square-packing-records/tree/52aa2672c74c91931686d60a49bdf97ec798291c)
rewrite or add, unchanged at the pin `52aa2672c74c91931686d60a49bdf97ec798291c`, the head
on 31 October 2026. No issue reports them: a publication in a watched repository, a
report from its commits by the owner’s rule of 14 October 2026.

## What the Source Claims

- Ten commits of 23 October 2026, 23:36:37Z to 23:56:35Z, each titled 'Certify world record for N=...' or 'Certify 6 world records under 308', rewrite or add certificates at 88, 126, 152, 154, 155, 183, 211, 227, 236, 237, 241, 270 and 271 under certificates/0000-0999/, and the index certified_bounds.json credits each to Mykhailo Polkovskyi (Mishapolk), at 88, 126 and 152 'packing refined from PingYou Ltd', at 154, 155, 236 and 271 'packing refined from Evan Daniel', and at 183 'packing refined from Evan Daniel & Francisco Couzo'; at 270 it credits Evan Daniel, 'strict certificate verified by Mishapolk'.
- The commit titles state each side at 12 places and how far it lies below the earlier certificate: about 1.0e-19 to 1.7e-19 below Evan Daniel's at 154, 155, 183, 236 and 271, about 1e-24 below PingYou Ltd's at 88, 126 and 152, and below Couzo, Evan Daniel and PingYou at 204, 211, 227, 237 and 241. No issue reports them. Those statements are the author's; no source program ran here.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is 16 files: 13 retained under [source/](source/) (502,462 bytes) and 3 pinned by digest.

| File | Bytes |
| --- | --- |
| `certificates/0000-0999/n126.cert` | 26,706 |
| `certificates/0000-0999/n152.cert` | 28,183 |
| `certificates/0000-0999/n154.cert` | 30,549 |
| `certificates/0000-0999/n155.cert` | 33,567 |
| `certificates/0000-0999/n183.cert` | 39,925 |
| `certificates/0000-0999/n211.cert` | 46,553 |
| `certificates/0000-0999/n227.cert` | 43,179 |
| `certificates/0000-0999/n236.cert` | 44,643 |
| `certificates/0000-0999/n237.cert` | 44,550 |
| `certificates/0000-0999/n241.cert` | 51,672 |
| `certificates/0000-0999/n270.cert` | 39,318 |
| `certificates/0000-0999/n271.cert` | 55,488 |
| `certificates/0000-0999/n88.cert` | 18,129 |
| `BOUND_VERIFIER_LICENSE.txt` | 1,068, pinned by digest |
| `LICENSE` | 1,088, pinned by digest |
| `verify_bound_certificate.py` | 3,567, pinned by digest |

[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the full
manifest, and [acquisition/sources.json](acquisition/sources.json) the record. The packet
is well under a megabyte, so it is kept in Git.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `3978a7f61` on 31 October
2026):

- **88:** exact side 9.8824510304812469…, below the case’s house (T-127) by 9.88e-20; above T-193 (#639) by 9.88e-30 (compared, not requested).
- **126:** exact side 11.7426406871192852…, below the case’s house (T-139) by 1.17e-19; above T-193 (#639) by 1.17e-29 (compared, not requested).
- **152:** exact side 12.8307188009766100…, below the case’s house (T-098) by 1.28e-19; undecided T-122 (#419) (compared, not requested).
- **154:** exact side 12.9211009407616806…, below the case’s house (T-222) by 1.29e-19 (requested).
- **155:** exact side 12.9522609446505641…, below the case’s house (T-197) by 1.30e-19 (requested).
- **183:** exact side 13.9995801787362526…, below the case’s house (T-220) by 1.40e-19 (requested).
- **211:** exact side 14.9935496262994211…, below the case’s house (T-188) by 1.50e-19 (requested).
- **227:** exact side 15.5636256523251491…, below the case’s house (T-225) by 1.56e-19 (requested).
- **236:** exact side 15.8619343906073587…, below the case’s house (T-218) by 1.59e-19 (requested).
- **237:** exact side 15.9026036382595969…, below the case’s house (T-190) by 1.59e-19 (requested).
- **241:** exact side 15.9871170951502388…, below the case’s house (T-182) by 1.60e-19 (requested).
- **270:** exact side 16.9281622521967502…, equal the case’s house (Evan Daniel) (compared, not requested).
- **271:** exact side 16.9489477337136576…, below the case’s house (T-219) by 1.69e-19 (requested).

## Report Order

The [ledger of 31 October for this pass](../../../campaign/issue-intake/upper-bounds-843-846-20261031/README.md) walks every report at these
counts in the order it reached this repository, from starts frozen at `main` `3978a7f61`,
and records this packet’s claims at 154, 155, 183, 211, 227, 236, 237, 241 and 271; its README
gives each count’s verdicts and what holds the others.

## Pose by Pose

`devtools.measure_identity` measured each recorded certificate against the packing the
ledger compares it with, and wrote the receipts under [measure/](measure/). A
measurement for credit; it decides nothing.

- **154** ([measure/identity-n154.json](measure/identity-n154.json)): against T-222, one to one by nearest centres (symmetry 0), 47 squares beyond 1e-3 and 60 beyond 1e-9, the largest move 7.793035e-2 and turn 0.8514 degrees. Tilted beyond 1 degree: 1023 38, T-222 38.
- **155** ([measure/identity-n155.json](measure/identity-n155.json)): against T-197, one to one by nearest centres (symmetry 0), 0 squares beyond 1e-3 and 0 beyond 1e-9, the largest move 8.600845e-16 and turn 5e-15 degrees. Tilted beyond 1 degree: 1023 56, T-197 56.
- **183** ([measure/identity-n183.json](measure/identity-n183.json)): against T-220, one to one by nearest centres (symmetry 0), 24 squares beyond 1e-3 and 27 beyond 1e-9, the largest move 3.577510e-1 and turn 6.237 degrees. Tilted beyond 1 degree: 1023 73, T-220 73.
- **211** ([measure/identity-n211.json](measure/identity-n211.json)): against T-188, one to one by nearest centres (symmetry 0), 0 squares beyond 1e-3 and 0 beyond 1e-9, the largest move 8.262227e-16 and turn 1e-14 degrees. Tilted beyond 1 degree: 1023 76, T-188 76.
- **227** ([measure/identity-n227.json](measure/identity-n227.json)): against T-225, one to one by nearest centres (symmetry 2), 16 squares beyond 1e-3 and 33 beyond 1e-9, the largest move 1.682026e-1 and turn 2.542 degrees. Tilted beyond 1 degree: 1023 54, T-225 54.
- **236** ([measure/identity-n236.json](measure/identity-n236.json)): against T-218, one to one by nearest centres (symmetry 0), 0 squares beyond 1e-3 and 0 beyond 1e-9, the largest move 9.794766e-16 and turn 5.717e-34 degrees. Tilted beyond 1 degree: 1023 40, T-218 40.
- **237** ([measure/identity-n237.json](measure/identity-n237.json)): against T-190, one to one by nearest centres (symmetry 0), 0 squares beyond 1e-3 and 0 beyond 1e-9, the largest move 1.341019e-15 and turn 7e-15 degrees. Tilted beyond 1 degree: 1023 49, T-190 49.
- **241** ([measure/identity-n241.json](measure/identity-n241.json)): against T-182, one to one by nearest centres (symmetry 0), 0 squares beyond 1e-3 and 1 beyond 1e-9, the largest move 1.562500e-6 and turn 5e-15 degrees. Tilted beyond 1 degree: 1023 85, T-182 85.
- **271** ([measure/identity-n271.json](measure/identity-n271.json)): against T-219, one to one by nearest centres (symmetry 0), 0 squares beyond 1e-3 and 0 beyond 1e-9, the largest move 2.326232e-19 and turn 5.184e-34 degrees. Tilted beyond 1 degree: 1023 69, T-219 69.

## Exact Replay

`devtools.upper_bound_reports certify` decided every certificate of the packet and its
duplicate-square and outside-container controls on both maintained routes, each job in its
own child process: 39 jobs, 1,613,220 pair decisions, 237.8 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). Every positive passed and every control was refused on both routes.

`devtools.upper_bound_reports sharp-controls` took each certificate to exact contact and
1e-30 past it (`receipts/sharp-controls-nNNN.json`, one per count (13 files)). It lowered the side by the least far-wall clearance,
closed the least-gap pair by its gap, and moved every square toward the nearer near wall
by its least clearance: both routes accepted each at contact with margin 0 and refused
each past it. It enlarged one square to its pair and one to its wall: both routes refused
each at contact for its shape alone and 1e-30 past it for the overlap or the wall as
well. Both refused a duplicated square.

The two routes, the `sqpack` rational witness verifier and the independent rational
corner checker, share certificate parsing, half-angle conversion, `Fraction` arithmetic
and the separating-axis method, and read each certificate through the `evand-cert`
reader. The source’s checkers were not run.

## What Is Not Established

- **No review yet.** The stage 4 mathematical review, by a strong-tier lane sharing no
  context with this one, has not run; it and the adoption are think-ikku’s.
- **Optimality** of any kind: a finite certificate proves an upper bound and nothing more.
- **The lineage** the source states, beyond what the measurements above show.

## Credit and Licence

MIT, copyright (c) 2026 Mykhailo Polkovskyi (LICENSE, added at 17cc220). Each packing
the ledger records is the house packing at its count, re-certified about 1e-19 below
it, so its finder keeps the credit and Polkovskyi is credited with the refinement, as
the index says (“packing refined from Evan Daniel” at 154, 155, 236 and 271). The
bibliography key is **[Mishapolk refinements 2026-10-23]**.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source mishapolk-1023-refinements-2026-10-30 --checkout CHECKOUT
python -m devtools.acquire_source mishapolk-1023-refinements-2026-10-30 --check
python -m devtools.upper_bound_reports mishapolk-1023-refinements-2026-10-30 check-claims --write
python -m devtools.upper_bound_reports mishapolk-1023-refinements-2026-10-30 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports mishapolk-1023-refinements-2026-10-30 check --replay
python -m devtools.upper_bound_reports mishapolk-1023-refinements-2026-10-30 sharp-controls
python -m devtools.measure_identity --n N 'VIEW=packet:mishapolk-1023-refinements-2026-10-30' 'HOUSE=packet:HOUSE_PACKET' \
  --out resources/web/mishapolk-1023-refinements-2026-10-30/measure/identity-nNNN.json
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
