# Mykhailo Polkovskyi’s Certificates of Issue 846 at 52aa267

This packet retains the certificates Mykhailo Polkovskyi’s
[Mishapolk/square-packing-records](https://github.com/Mishapolk/square-packing-records/tree/52aa2672c74c91931686d60a49bdf97ec798291c)
holds at `52aa2672c74c91931686d60a49bdf97ec798291c` (committed 2026-10-30T05:40:00Z), the
head on 31 October 2026. Issue [#846](https://github.com/jlevy/squares/issues/846),
opened 6 minutes 42 seconds after the commit, reports 14 of them. The 211 and 241
certificates the issue names were first committed on 23 October and are retained by the
[mishapolk-1023-refinements-2026-10-30](../mishapolk-1023-refinements-2026-10-30/README.md)
packet, against whose copies they are pinned here.

## What the Source Claims

- Issue #846 (opened 2026-10-30T05:46:42Z by Mishapolk) reports 14 upper bounds at 105, 130, 146, 156, 182, 204, 211, 229, 241, 260, 268, 299, 304 and 308 from certificates/0000-0999/nN.cert at 52aa267, each the certificate's exact rational side rounded up at 12 places, in two categories: A, 'Literature World Records' at 130, 182 and 268, and B, 'Micro-Refinement Packings' at the other eleven.
- Every 12-place print the issue states is its certificate's header side rounded up. At 204, 211 and 241 the exact fraction the issue's table prints is not the certificate's header (it is 9.75e-14 above at 204, 1.50e-19 above at 211, and 2.39e-13 below at 241), and at 268 its denominator has one digit more than the header's; the header is the certificate's side.
- The 130 certificate's header calls it a dilation (dilate_cert.py, delta 2e-14) of isolated_lab/tmp_couzo_noalm.txt; the issue says it beats Francisco Couzo's #843 by 2.08e-12. The 182, 268, 299 and 304 headers call them dilations of the source's own candidates; the 105 and 260 headers call them exact contracted certificates; the rest are exact centre and half-angle certificates.
- The issue says every certificate yields valid and strictly valid under verify_bound_certificate.py --strict, Evan Daniel's separating-axis verifier. Those statements are the author's; no source program ran here.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is 22 files: 15 retained under [source/](source/) (421,467 bytes) and 7 pinned by digest.

| File | Bytes |
| --- | --- |
| `ISSUE_SUBMISSION_CATEGORY_A.md` | 3,818 |
| `ISSUE_SUBMISSION_CATEGORY_B.md` | 4,253 |
| `README.md` | 4,737 |
| `certificates/0000-0999/n105.cert` | 16,679 |
| `certificates/0000-0999/n130.cert` | 16,505 |
| `certificates/0000-0999/n146.cert` | 22,916 |
| `certificates/0000-0999/n156.cert` | 42,554 |
| `certificates/0000-0999/n182.cert` | 24,165 |
| `certificates/0000-0999/n204.cert` | 33,336 |
| `certificates/0000-0999/n229.cert` | 33,067 |
| `certificates/0000-0999/n260.cert` | 37,365 |
| `certificates/0000-0999/n268.cert` | 41,771 |
| `certificates/0000-0999/n299.cert` | 46,202 |
| `certificates/0000-0999/n304.cert` | 46,915 |
| `certificates/0000-0999/n308.cert` | 47,184 |
| `BOUND_VERIFIER_LICENSE.txt` | 1,068, pinned by digest |
| `LICENSE` | 1,088, pinned by digest |
| `certificates/0000-0999/n211.cert` | 46,553, pinned by digest |
| `certificates/0000-0999/n241.cert` | 51,672, pinned by digest |
| `certified_bounds.json` | 4,625,979, pinned by digest |
| `upper_bounds.json` | 7,710,565, pinned by digest |
| `verify_bound_certificate.py` | 3,567, pinned by digest |

[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the full
manifest, and [acquisition/sources.json](acquisition/sources.json) the record. The packet
is well under a megabyte, so it is kept in Git.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `3978a7f61` on 31 October
2026):

- **105:** exact side 10.7893037837429754…, below the case’s house (T-229) by 1.00e-21 (requested).
- **130:** exact side 11.9024306459822658…, below the case’s house (T-174) by 2.05e-03; below T-253 (#843) by 2.08e-12 (requested).
- **146:** exact side 12.5837821901518604…, below the case’s house (T-187) by 1.00e-21 (requested).
- **156:** exact side 12.9791658538342765…, below the case’s house (T-186) by 1.00e-41 (requested).
- **182:** exact side 13.9709164362148191…, above the case’s house (T-243) by 1.40e-13 (compared, not requested).
- **204:** exact side 14.8086428305130872…, equal the case’s house (T-231) (compared, not requested).
- **211:** exact side 14.9935496262994211…, below the case’s house (T-188) by 1.50e-19; equal T-252, Polkovskyi of 23 October (no issue) (compared, not requested).
- **229:** exact side 15.6501615138764311…, below the case’s house (T-225) by 1.00e-21 (requested).
- **241:** exact side 15.9871170951502388…, below the case’s house (T-182) by 1.60e-19; equal T-252, Polkovskyi of 23 October (no issue) (compared, not requested).
- **260:** exact side 16.6457532505198122…, below the case’s house (T-225) by 1.00e-21; above T-254, Couzo of 28 October (no issue) by 7.22e-03; above T-255 (#844) by 8.72e-03; above T-256 (#845) by 1.18e-02 (compared, not requested).
- **268:** exact side 16.8743617158708279…, above the case’s house (T-242) by 1.48e-12 (compared, not requested).
- **299:** exact side 17.8036954353157388…, below the case’s house (T-101) by 1.92e-02; below T-248 (#824) by 1.66e-11; above T-257 (#824 update) by 2.46e-03 (compared, not requested).
- **304:** exact side 17.9268989003667642…, above the case’s house (T-242) by 1.00e-11 (compared, not requested).
- **308:** exact side 17.9971491212709088…, below the case’s house (T-221) by 1.00e-21 (requested).

## Report Order

The [ledger of 31 October for this pass](../../../campaign/issue-intake/upper-bounds-843-846-20261031/README.md) walks every report at these
counts in the order it reached this repository, from starts frozen at `main` `3978a7f61`,
and records this packet’s claims at 105, 130, 146, 156, 229 and 308; its README
gives each count’s verdicts and what holds the others.

## Pose by Pose

`devtools.measure_identity` measured each recorded certificate against the packing the
ledger compares it with, and wrote the receipts under [measure/](measure/). A
measurement for credit; it decides nothing.

- **105** ([measure/identity-n105.json](measure/identity-n105.json)): against T-229, one to one by nearest centres (symmetry 0), 0 squares beyond 1e-3 and 0 beyond 1e-9, the largest move 0.000000e+6 and turn 0 degrees. Tilted beyond 1 degree: #846 41, T-229 41.
- **130** ([measure/identity-n130.json](measure/identity-n130.json)): against #843, one to one by nearest centres (symmetry 0), 0 squares beyond 1e-3 and 14 beyond 1e-9, the largest move 1.129810e-6 and turn 5.58e-05 degrees. Tilted beyond 1 degree: #846 33, #843 33.
- **146** ([measure/identity-n146.json](measure/identity-n146.json)): against T-187, one to one by nearest centres (symmetry 0), 0 squares beyond 1e-3 and 0 beyond 1e-9, the largest move 0.000000e+6 and turn 0 degrees. Tilted beyond 1 degree: #846 37, T-187 37.
- **156** ([measure/identity-n156.json](measure/identity-n156.json)): against T-186, one to one by nearest centres (symmetry 0), 0 squares beyond 1e-3 and 0 beyond 1e-9, the largest move 0.000000e+6 and turn 0 degrees. Tilted beyond 1 degree: #846 62, T-186 62.
- **229** ([measure/identity-n229.json](measure/identity-n229.json)): against T-225, one to one by nearest centres (symmetry 0), 0 squares beyond 1e-3 and 0 beyond 1e-9, the largest move 0.000000e+6 and turn 0 degrees. Tilted beyond 1 degree: #846 60, T-225 60.
- **308** ([measure/identity-n308.json](measure/identity-n308.json)): against T-221, one to one by nearest centres (symmetry 0), 0 squares beyond 1e-3 and 0 beyond 1e-9, the largest move 0.000000e+6 and turn 0 degrees. Tilted beyond 1 degree: #846 102, T-221 102.

## Exact Replay

`devtools.upper_bound_reports certify` decided every certificate of the packet and its
duplicate-square and outside-container controls on both maintained routes, each job in its
own child process: 42 jobs, 2,149,266 pair decisions, 338.1 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). Every positive passed and every control was refused on both routes.

`devtools.upper_bound_reports sharp-controls` took each certificate to exact contact and
1e-30 past it (`receipts/sharp-controls-nNNN.json`, one per count (14 files)). It lowered the side by the least far-wall clearance,
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

MIT, copyright (c) 2026 Mykhailo Polkovskyi (LICENSE, added at 17cc220). The issue
credits “Mishapolk (Mikhail Polk) & Antigravity Autonomous Research Lab”. Each packing
the ledger records is another holder’s, re-certified: at 130 Francisco Couzo’s (#843),
and at 105, 146, 156, 229 and 308 the house packing at each count, credited to its
finder; Polkovskyi is credited with the refinement. The bibliography key is
**[Mishapolk issue 846 2026-10-30]**.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source mishapolk-issue846-2026-10-30 --checkout CHECKOUT
python -m devtools.acquire_source mishapolk-issue846-2026-10-30 --check
python -m devtools.upper_bound_reports mishapolk-issue846-2026-10-30 check-claims --write
python -m devtools.upper_bound_reports mishapolk-issue846-2026-10-30 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports mishapolk-issue846-2026-10-30 check --replay
python -m devtools.upper_bound_reports mishapolk-issue846-2026-10-30 sharp-controls
python -m devtools.measure_identity --n N 'VIEW=packet:mishapolk-issue846-2026-10-30' 'HOUSE=packet:HOUSE_PACKET' \
  --out resources/web/mishapolk-issue846-2026-10-30/measure/identity-nNNN.json
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
