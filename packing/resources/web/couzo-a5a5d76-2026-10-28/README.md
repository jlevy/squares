# Francisco Couzo’s Certificates at 260 and 307 at a5a5d76

This packet retains the two certificates Francisco Couzo’s
[franciscouzo/square-packing](https://github.com/franciscouzo/square-packing/tree/a5a5d76790679902ef57270f6d4c2d01786c5a56)
publishes at `a5a5d76790679902ef57270f6d4c2d01786c5a56` (committed
2026-10-28T01:41:35Z), which no issue reports: a publication in a watched repository,
a report from its commit by the owner’s rule of 14 October 2026. The packet pins
a5a5d76 because the head, 712c6a6, replaces both files with the certificates issue
[#844](https://github.com/jlevy/squares/issues/844) reports (the
[couzo-issue844-2026-10-28](../couzo-issue844-2026-10-28/README.md) packet).

## What the Source Claims

- certificates/n260.cert states s(260) <= 67077942617632138527571542307/4031481829251000000000000000 = 16.6385327923192945...; the commit message prints 16.638532792320, below the committed public comparison's 16.645753250520 (Evan Daniel).
- certificates/n307.cert states s(307) <= 436081607184993722962197444889181982917255228924685874736959955436771335630565667211324538123/24254714520872479530466069702814569144398684321103594602674239356738890164429000000000000000 = 17.9792512836925855...; the commit message prints 17.979251283693, below #593's 17.980862784055.
- The commit message says neither packing is the author's construction: both refine the packings ntumlnoob published in the Kaggle notebook 'First 22.268681355 Public Code With Explanation' (run 362957087; its metric gives 16.638533455862 and 17.979253973651), and the gains (6.6e-7 and 2.7e-6) come from the web app's fq, an adaptation of Evan Daniel's fq optimizer (MIT); certificates/n260.json and n307.json say so. Those statements are the author's; no source program ran here.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is 10 files: 5 retained under [source/](source/) (150,760 bytes) and 5 pinned by digest.

| File | Bytes |
| --- | --- |
| `README.md` | 8,584 |
| `certificates/n260.cert` | 33,347 |
| `certificates/n260.json` | 8,718 |
| `certificates/n307.cert` | 89,224 |
| `certificates/n307.json` | 10,887 |
| `BOUND_VERIFIER_LICENSE.txt` | 1,068, pinned by digest |
| `certificates/best/n260.cert` | 33,347, pinned by digest |
| `certificates/best/n307.cert` | 89,224, pinned by digest |
| `n260.txt` | 12,533, pinned by digest |
| `n307.txt` | 18,397, pinned by digest |

[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the full
manifest, and [acquisition/sources.json](acquisition/sources.json) the record. The packet
is well under a megabyte, so it is kept in Git.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `3978a7f61` on 31 October
2026):

- **260:** exact side 16.6385327923192946…, below the case’s house (T-225) by 7.22e-03 (requested).
- **307:** exact side 17.9792512836925856…, below the case’s house (T-174) by 1.61e-03 (requested).

## Report Order

The [ledger of 31 October for this pass](../../../campaign/issue-intake/upper-bounds-843-846-20261031/README.md) walks every report at these
counts in the order it reached this repository, from starts frozen at `main` `3978a7f61`,
and records this packet’s claims at 260 and 307; its README
gives each count’s verdicts and what holds the others.

## Pose by Pose

`devtools.measure_identity` measured each recorded certificate against the packing the
ledger compares it with, and wrote the receipts under [measure/](measure/). A
measurement for credit; it decides nothing.

- **260** ([measure/identity-n260.json](measure/identity-n260.json)): against T-225, no symmetry one to one; the optimal assignment (symmetry 0) moves 167 squares beyond 0.1 and 202 beyond 0.01 (largest 1.00448) and turns squares by up to 27.39 degrees. Tilted beyond 1 degree: a5a5d76 104, T-225 60.
- **307** ([measure/identity-n307.json](measure/identity-n307.json)): against T-174, no symmetry one to one; the optimal assignment (symmetry 6) moves 91 squares beyond 0.1 and 134 beyond 0.01 (largest 1.13735) and turns squares by up to 34.04 degrees. Tilted beyond 1 degree: a5a5d76 107, T-174 103.

## Exact Replay

`devtools.upper_bound_reports certify` decided every certificate of the packet and its
duplicate-square and outside-container controls on both maintained routes, each job in its
own child process: 6 jobs, 483,846 pair decisions, 85.7 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). Every positive passed and every control was refused on both routes.

`devtools.upper_bound_reports sharp-controls` took each certificate to exact contact and
1e-30 past it (). It lowered the side by the least far-wall clearance,
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
  context with this one, has not run; it and the adoption are think-dwzb’s.
- **Optimality** of any kind: a finite certificate proves an upper bound and nothing more.
- **The lineage** the source states, beyond what the measurements above show.

## Credit and Licence

The certificates are factual data, and the presumption of permission the author’s
submissions of this repository carry (#843, #844; think-cnn7, think-m8f4) covers them.
Both packings are ntumlnoob’s, from the Kaggle notebook “First 22.268681355 Public Code
With Explanation”; the refinements and the certificates are Couzo’s, with an adaptation
of Evan Daniel’s fq. The bibliography key is **[Couzo a5a5d76 2026-10-28]**.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source couzo-a5a5d76-2026-10-28 --checkout CHECKOUT
python -m devtools.acquire_source couzo-a5a5d76-2026-10-28 --check
python -m devtools.upper_bound_reports couzo-a5a5d76-2026-10-28 check-claims --write
python -m devtools.upper_bound_reports couzo-a5a5d76-2026-10-28 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports couzo-a5a5d76-2026-10-28 check --replay
python -m devtools.upper_bound_reports couzo-a5a5d76-2026-10-28 sharp-controls
python -m devtools.measure_identity --n N 'VIEW=packet:couzo-a5a5d76-2026-10-28' 'HOUSE=packet:HOUSE_PACKET' \
  --out resources/web/couzo-a5a5d76-2026-10-28/measure/identity-nNNN.json
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
