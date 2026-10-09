# Francisco Couzo: Five Follow-Up Exact Rational Refinements

A
[comment on pull request #460](https://github.com/jlevy/squares/pull/460#issuecomment-6070798890)
reports smaller exact rational certificates at $n=84,86,105,175,270$, published in
[the pinned source](https://github.com/franciscouzo/square-packing/tree/2d32a6e96f55c5dc1a2dd0e3581098e7c0105252)
(commit `2d32a6e`, tree `1e98bf6`, committed 2026-10-08T22:12:27Z, parent `ffd900d`).
This packet keeps those five certificates as derived exact facts.

The author starts from Ryan Xu’s #432 packings at 84, 86, 105 and 175 and from Evan
Daniel’s #399 packing at 270. Couzo’s basin hopping refined 84, 86, 105 and 270; David
Ellsworth’s refine_packing followed by Evan Daniel’s fq refined 175. Evan Daniel’s exact
contact solver wrote the certificates.
The commit names Claude as a co-author, disclosing AI assistance.
These are source attributions, not independent priority findings.

The author reports that all five pass Evan Daniel’s `verify_cert.py` and a copy of this
repository’s `sqpack` verifier, lie within about $10^{-19}$ of a KKT point and admit no
first-order descent.
Those statements are author claims here; no author program runs.

## Source Custody and Retention

The repository has no licence file, and its README states no reuse terms.
`certificates/README.md` names the MIT-licensed solver that wrote the certificates,
which does not license this bundle.
Under the [existing retention policy](../known-best-packings/README.md) this packet
therefore keeps no upstream byte: no certificate, decimal pose, SVG, README or program.
No redistribution permission or licence determination is asserted.

[`acquisition/sources.json`](acquisition/sources.json) records the commit, its parent
and all 136 leaves of the pinned tree, with `raw_asset_retained: false`. Each of the
five [facts](facts/) is an exact rational `center-basis` Witness/v2 converted from the
certificate’s centres and half-angle parameters.
It is the deciding witness of the maintained exact route.

From `packing/`, with the project interpreter, the offline packet check is:

```bash
python -m devtools.couzo_followup_reports check-packet
```

It rebuilds the pinned tree root from its leaves, recovers every half-angle exactly from
the facts and rebuilds each certificate’s exact text and Git blob identity.
It also checks that the seven other certificates at this commit, $n=108$, 127, 131, 155,
180, 228 and 306, and their decimal poses are byte-identical to the
[issue #451 originals](../couzo-exact-refinements-2026-10-08/README.md).
The earlier $n=105$ certificate stays retained in that packet with its own replay; the
author calls it still valid, and the new one is smaller.

The decimal poses `n84.txt` to `n270.txt` are source context, held by identity with
their printed sides quoted.
Only the five rational certificates enter geometry decisions.
The same commit also changes the outside-horizon `n375.txt` and `n378.txt`; this packet
records their identities and printed sides only, and their claims stay with the
[outside-horizon packet](../couzo-extended-reports-2026-10-09/README.md).

## Exact Replay

[`receipts/exact-certification.json.xz`](receipts/exact-certification.json.xz) holds all
fifteen jobs of the maintained protocol: each certificate, the same certificate with its
second square moved onto its first, and the same certificate with its first square
translated outside the container.
Every job keeps its complete deciding input and the full results of both exact routes,
the `sqpack` rational witness verifier and the independent rational corner checker.

All five positives pass both routes; all ten controls fail both, on the overlap or the
wall they were built to break.
The positives clear every wall by at least $1/200000000000000000000$ and every pair by
about $10^{-20}$. The run made 384,846 pair decisions in 79.55 seconds wall with two
workers, 141.06 CPU seconds, under the kernel’s unchanged 600-second child deadline.
A fresh serial `check --replay` reproduced all fifteen results apart from timing in
130.93 seconds.

| $n$ | Exact side, rounded up | Selected ceiling before | Below it by |
| ---: | --- | --- | ---: |
| 84 | 9.6979347990149214 | 9.6980520605096981, Ryan Xu (T-125) | $1.17 \times 10^{-4}$ |
| 86 | 9.8205354074967423 | 9.8205657300098206, Ryan Xu (T-125) | $3.03 \times 10^{-5}$ |
| 105 | 10.7893037837481589 | 10.7906765754107907, Ryan Xu (T-125) | $1.37 \times 10^{-3}$ |
| 175 | 13.7671551635425492 | 13.7688992766137689, Ryan Xu (T-125) | $1.74 \times 10^{-3}$ |
| 270 | 16.9367230228761835 | 16.9378072284460292, Evan Daniel (T-119) | $1.08 \times 10^{-3}$ |

Each comparison is exact: the acquisition record freezes the selected and verified
rational sides it was made against.
At $n=105$ the new side is also $1.31 \times 10^{-3}$ below Couzo’s earlier issue #451
certificate (T-128).

```bash
python -m devtools.couzo_followup_reports certify --jobs-dir SCRATCH/jobs --workers 2
python -m devtools.couzo_followup_reports check --replay
```

The certificates establish finite feasibility only.
No KKT, local-minimum, rigidity, novelty or optimality claim is admitted, and the
selected cases do not change in this packet: independent review, preservation of the
historical source houses and a confirming record come first.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
