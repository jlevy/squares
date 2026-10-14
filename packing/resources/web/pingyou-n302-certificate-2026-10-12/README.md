# PingYou Ltd: An Exact Packing of 302 Squares

[Issue #564](https://github.com/jlevy/squares/issues/564) (BuddenPing, opened 2026-10-12T21:27Z; title and body replaced at 22:17Z, with a comment saying so) reports an exact rational certificate for 302 unit squares in [BuddenPing/square-packing-certificates](https://github.com/BuddenPing/square-packing-certificates/tree/5a86ac3ec09beae5f11e2a8f7115954e76fa616a) at `5a86ac3ec09beae5f11e2a8f7115954e76fa616a` (tree `b90fa532d61451c73f17bc1ea2dc6468973c16d9`, committed 2026-10-12T22:16:11Z, parent `a0e6fb4`), the revision the updated issue names. The parent, `a0e6fb4`, published the issue's original certificate, side `17.8702753841786227538399992`, which the update supersedes by `0.00000000144486300001444863` and which this packet does not retain.
The source was retrieved at 2026-10-14T04:47Z, when its branch head was `318ab94e821ba7280a68fa8ce2942c9ecdbda41d`; every file of this packet's scope has the same blob there.

| n | Exact side of the certificate | Rounded up at 16 places |
| --- | --- | --- |
| 302 | `1787027538273375975382555057/100000000000000000000000000` | 17.8702753827337598 |

## Who the Source Is

As for the [n207](../pingyou-n207-certificate-2026-10-11/README.md#who-the-source-is) and [n153](../pingyou-n153-certificate-2026-10-11/README.md) packets of 11 October: the repository describes itself as “Exact square-packing certificates and reproducible verification from PingYou Ltd”, its README is headed “Square-packing certificates — PingYou Ltd”, and every commit is authored as `BuddenPing` from an address at the `pingyou.com` domain. GitHub detects no licence and the account names no person or company. The source names no individual author, and this packet names none.
At retrieval `main` held sixteen commits, the head `318ab94` (2026-10-12T23:46:52Z), and five tags `data/pingyou-*`, all at the head, each a GitHub release whose assets carry later certificates (below, [Later Claims by the Same Author](#later-claims-by-the-same-author)).

## Source Custody

The tree has no licence file, and GitHub detects none.
The release READMEs say that upstream software and schema licences are retained beside the files they cover and that no new licence is asserted for third-party material; nothing grants one for the source's own files.
Under the derived-only form of the [existing retention policy](../known-best-packings/README.md), as for the 11 October PingYou packets, this packet keeps no upstream byte. No redistribution permission or licence determination is asserted.

`devtools.acquire_source` wrote the packet from a clone checked out at the pin, from the declaration in [acquisition/declaration.json](acquisition/declaration.json).
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and [acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest.
The scope is the eight paths the pinned commit changed: the six n302 files, first published by `a0e6fb4`, and `README.md` and `SHA256SUMS`.
All eight are pinned only; the declared `source/` directory is empty by design.

| Upstream path | Git blob | Bytes | SHA-256 | What it is |
| --- | --- | --- | --- | --- |
| `n302.cert.json` | `eae2a570c062090eb78524323f857e34fc5c8d75` | 41563 | `fc57b683ccd411660bb5d5f9758fb2ac013733220bf525936d73f2a11fd8d2cd` | The certificate |
| `pingyou-n302-rational.yaml` | `064a0f3483ef865e0f182bc55eddf6a0aa035b90` | 235451 | `542974911e45a4dec335d07ad072ab7a86ab5b0d7ab84ecb720dab8253b2aa38` | The same packing as a corners Witness/v2 |
| `README.md` | `c9c2721e5a47f432fc9750d53afe11f6013a9c25` | 10387 | `f888ce4c9861086105d5ace6adb3f7cc6359a9a3874cef2c81f8e76ca2e5fa09` | Author prose for every release in the tree |
| `SHA256SUMS` | `f3e301a12310423daa876694b8d954a9ec89cc6f` | 1543 | `98bf78301ea62b903134bc08c1c41d9999a47c58d290287cd726be6d0affe61b` | The source's digests of the tree's release files |
| `n302-SHA256SUMS` | `1522e2decb5271e68da75d8097e68a2fb5d414b9` | 435 | `7185c112127a0cab5ccc1251609c0bc28d3efdd3e102ae65e4d2d68fca5383c9` | The source's digests of this release's files |
| `n302-squares-project.zip` | `4b46f1246c915920aeeb92ade1b68b8afa4ab372` | 172265 | `4a1a33ca4802734755c40cb429f9701646b2f896791f87df200afc50cebadde2` | The complete package, below |
| `n302-verified-comparison.pdf` | `e82e7a98928e2104b20666d1f0b624748b89b328` | 15431 | `f4afa625814dea2007f1d0b6cdd93bff7dbb2f376755b225f056ade93ab3c24b` | Comparison figure |
| `n302.svg` | `7931b3408b19169fd204a3e48931d33f6cc4c3b4` | 52846 | `53460f57a283d217a8f95820f7eac6828a9d46a5416b4c098b16f765a49db6b0` | Drawing |

The three digests the issue states, for the package, the certificate and the witness, are the ones above, and `n302-SHA256SUMS` lists the same digest for each of the five n302 artifacts it names.

## What the Package Holds

`n302-squares-project.zip` unpacks to `n302-squares-project/`, 51 files, 835,913 bytes.
Its `SHA256SUMS` lists a digest for each of the other 50, and every one equals the digest of the bytes unpacked here.
Byte for byte, `n302-squares-project/evidence/n302-verified-comparison.pdf` is `n302-verified-comparison.pdf`, `n302-squares-project/evidence/packing.cert.json` is `n302.cert.json`, `n302-squares-project/evidence/n302.svg` is `n302.svg`, `n302-squares-project/native/pingyou-n302-rational.yaml` is `pingyou-n302-rational.yaml`.
It holds 17 Python programs, `VERIFY.py` among them; they were read for what they claim and not run.
Among the rest are the n70 parent, the construction table and its replay (`construction/`), the author's polygon-projection checker and Evan Daniel's unchanged `verify_cert.py` and `verify_cert2.py` (`checkers/`), receipts, and the sources and licence of this repository's two checkers at `074ac28` (`native/`).
Nothing in it is retained.

## The Certificate

`n302.cert.json` is a JSON object with `n`, `s_exact` (a rational string) and `squares`, one `[x, y, t]` triple of rational strings per square, the centre in $[0, S]^2$ and $t = \tan(\theta/2)$. `devtools.upper_bound_reports` reads it with the `pingyou-json` adapter.
`pingyou-n302-rational.yaml` states the same 302 squares as rational corners in this repository's Witness/v2 format, in JSON syntax; the `witness-corners` adapter recovers each pose from its corners exactly.

The construction, as the source states it: four patches of the n70 source contribute 16, 9, 9 and 16 whole squares and two upright banks 105 and 147, $16 + 9 + 9 + 16 + 105 + 147 = 302$; 254 squares are upright and two mirrored tilted populations hold 24 each, at a frame where a middle-seam return and a short return meet at a root of $2t^3 - 3t^2 - 2t + 1 = 0$. Centres and the box are dilated by $100000000001/100000000000$, the squares keeping side 1. The update refines the centres of the same construction at the same frame and guard.

## Against the Record

At `main` `aeef99ef0` the case record's reported and verified ceilings at 302 are both T-146's (Nate Chaoweeraprasit (itsnaka), improved by Evan Daniel; `E-evand-regularized-exact-feasibility`), side `558500932783786874181638432249/31250000000000000000000000000`. The certificate is below it by `109654146713763749179953873/62500000000000000000000000000`, about $1.75 \times 10^{-3}$.

| Report | Holders | Side | Relation | Distance |
| --- | --- | --- | --- | --- |
| T-098 (#375) | Francisco Couzo, improved by Evan Daniel | 17.8859938925304107 (retained, shown rounded up) | below | 0.0157 |
| T-116 (#422) | Nate Chaoweeraprasit | 17.8813062180958085 (retained, shown rounded up) | below | 0.011 |
| T-136 (#481) | Nate Chaoweeraprasit | 17.8720298490811800 (retained, shown rounded up) | below | 0.00175 |
| T-138 (#470) | Mishapolk | 17.881306218091 (retained, exact) | below | 0.011 |
| #583 | Francisco Couzo | 17.870013850405 (printed, rounded up) | above | 0.000262 |
| #593 | Mishapolk (Mykhailo Polkovskyi) | 17.8702753825550609 (printed, rounding unstated) | above | 1.79e-10 |
| PR #574 | PingYou Ltd | 17.87027538255505966957269257339824 (printed, rounding unstated) | above | 1.79e-10 |

A relation is this certificate's against the other side: *below* means this side is smaller. The smallest report at the count is #583.

Measured square for square, the packing is not T-146's: under none of the box's eight symmetries does matching each square to the nearest of T-146's pair them one to one, and under the best of them 50 squares lie more than a tenth of a unit from the nearest of its squares. Francisco Couzo's #583, the smallest report here, says it continues this arrangement; the record holds no measurement of that. T-056 has no packet reader here, and `devtools.check_standing` at `main` marks it superseded.
[acquisition/claims.json](acquisition/claims.json) freezes these comparisons, and `devtools.upper_bound_reports` rebuilds them from the retained packets.

## Derived Fact and Exact Replay

`devtools.upper_bound_reports derive` read `n302.cert.json` from a checkout at the pin, after `devtools.acquire_source` showed that the checkout yields this packet's acquisition record and manifest, so the bytes it read have the digests above.
It admitted the certificate at the exact fraction the issue prints.
It then read `pingyou-n302-rational.yaml` from the same checkout, as the row's `same_packing` file: all 302 poses and the side are the certificate's exactly.
It wrote the certificate as an exact rational `center-basis` Witness/v2, [facts/n-302.yaml.gz](facts/n-302.yaml.gz), naming the certificate's SHA-256 as `revision_sha256`. The fact is this repository's derivation; offline it must rebuild itself from the certificate it states, and `derive --check` with a checkout compares the fact and the witness again.
The declaration of the import is [acquisition/report.json](acquisition/report.json).

Only the fact enters geometry decisions, through the two-route kernel of `devtools.evand_arrangement_reports`: `sqpack`'s exact witness verifier and the independent rational corner checker, each deciding every wall and every pair over $\mathbb{Q}$.
A positive job, a duplicate-square control and an outside-container control each ran in its own child process, one worker at a time. The positive passes both routes and both routes refuse both controls. Both routes find the same margins: the least wall clearance exactly `1/200000000000` and the least pair gap a rational of 160 characters, whose denominator has 85 digits, about $9.99 \times 10^{-12}$.
The three jobs made 272,706 pair decisions in 51.27 route CPU seconds and 64.61 job wall seconds, summed; the longest took 21.66 seconds, and `certify` 67 seconds of wall time, with other lanes on the machine.
A fresh `check --replay` decided all three jobs again, equal to the retained rows apart from timing, in 85 seconds.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every deciding input and both routes' complete outputs.
The two routes share certificate parsing, the half-angle conversion, Python's rational arithmetic and the separating-axis method.

The release reports that `packing-witness verify` and `devtools.check_rational_witness_independent`, unchanged at `074ac28`, accept its own witness file; `n302-squares-project/native/native-replay.json` is that receipt. The two maintained routes here decided the certificate from the derived fact; the source's witness file was compared with the certificate pose for pose and not decided separately.

## What Is Not Established

The source reports that its three exact checkers accept all 45,451 pairs and every wall and that its replay rebuilds every pose from the construction table. Those are author reports.
`VERIFY.py`, the package's checkers, its construction replay, `convert_witness.py` and `replay_upstream.py` were read here and not run: the two maintained routes decide the certificate from its own poses, so none is needed for the bound.
The replay above has not been reviewed.
The certificate establishes a finite upper bound only; the source claims no local or global optimality.
That the 302 poses are the stated composition of the n70 source bears on credit, and was not checked here.

## Later Claims by the Same Author

The author has since submitted further certificates at this count, outside this packet's scope. [PR #574](https://github.com/jlevy/squares/pull/574) (opened 2026-10-13T00:13Z from `BuddenPing/squares`, head `4c319c2`, open and unmerged) requests 148 certificate refinements, and the GitHub releases at the tags `data/pingyou-numerical-refinements-2026-10-13-v1` and `-v2`, `data/pingyou-exact-153-302-2026-10-13(-v1)` and `data/pingyou-algebraic-refinements-2026-10-13-v1`, all on the head, carry them as assets that are not in the Git tree. At 302 it states a rational certificate, about 17.8702753825550596695761313748…, $1.79 \times 10^{-10}$ below this one, and an exact algebraic certificate attaining $33/2 + (7/2)t + t^2$ at the root of $2t^3 - 3t^2 - 2t + 1$ in $(7/20, 9/25)$, about 17.87027538255505966957269257339824, a further $3.44 \times 10^{-21}$ below. Read from the PR's `claims.json` files at its head, as data; neither the PR nor the release assets were retained or replayed here, and they are an import of their own.

## Credit

The source credits PingYou Ltd with the n302 construction and its refinement, Ryan Xu with the n70 construction it uses ([#432](https://github.com/jlevy/squares/issues/432)), Evan Daniel with the exact retention of that construction and with the prior n302 regularization, and Nate Chaoweeraprasit (SQUISH) with the prior n302 construction ([#481](https://github.com/jlevy/squares/issues/481)), which it uses only as the comparison. It claims neither the n70 packing nor patch composition in general.

Neither the pinned source nor the issue makes a statement about AI assistance. Asked on #503 which account of AI assistance stands, the author answered on 12 October 2026 for the n207 and n153 releases ([comment](https://github.com/jlevy/squares/issues/503#issuecomment-6129716138)): “Both solutions were AI assisted by ‘PY’, an unreleased agentic AI offering by PingYou Ltd.” That answer names the n207 and n153 solutions; whether it covers this one is not stated.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source pingyou-n302-certificate-2026-10-12 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-n302-certificate-2026-10-12 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-n302-certificate-2026-10-12 check --replay
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-n302-certificate-2026-10-12 derive --checkout CHECKOUT --check
```

`--check` re-derives the record from this packet alone.
The importer's `check-claims` and `check --replay` run offline from the fact;
`derive --check` needs a checkout at the pin, refuses one that does not yield this
packet's record and manifest, and compares the fact and the source's witness with the
certificate.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `facts/n-302.yaml.gz` | receipt | `f11cbd0d36565848c3c77c3f2672b599ff35e728` | `81a0bb096a9110027d3ab5d789328bcccf1bc209a1f71d03e53f08c1cdd0a2be` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
