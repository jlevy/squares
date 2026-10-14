# PingYou Ltd: A Refined Certificate for 153 Squares

A [comment on issue #504](https://github.com/jlevy/squares/issues/504#issuecomment-6133737268) (BuddenPing, 2026-10-12T22:24Z), and the dated update the author placed at the top of the issue's body, report a refined certificate of the n153 construction T-148 registers and ask that T-148 be re-verified and updated. It is in [BuddenPing/square-packing-certificates](https://github.com/BuddenPing/square-packing-certificates/tree/431186b6c20d444b26b5d321a1cd85d2f2d63274) at `431186b6c20d444b26b5d321a1cd85d2f2d63274` (tree `1504776c7f78d3498a50bca6d4548d9f4f93b651`, committed 2026-10-12T22:23:27Z, parent `5a86ac3`), the revision the comment names. T-148's certificate, at `bc328a7`, is retained by [the 11 October packet](../pingyou-n153-certificate-2026-10-11/README.md).
The source was retrieved at 2026-10-14T04:47Z, when its branch head was `318ab94e821ba7280a68fa8ce2942c9ecdbda41d`; every file of this packet's scope has the same blob there.

| n | Exact side of the certificate | Rounded up at 16 places |
| --- | --- | --- |
| 153 | `3217503462601758500692520223/250000000000000000000000000` | 12.8700138504070341 |

## Who the Source Is

As for the [n207](../pingyou-n207-certificate-2026-10-11/README.md#who-the-source-is) and [n153](../pingyou-n153-certificate-2026-10-11/README.md) packets of 11 October: the repository describes itself as “Exact square-packing certificates and reproducible verification from PingYou Ltd”, its README is headed “Square-packing certificates — PingYou Ltd”, and every commit is authored as `BuddenPing` from an address at the `pingyou.com` domain. GitHub detects no licence and the account names no person or company. The source names no individual author, and this packet names none.
At retrieval `main` held sixteen commits, the head `318ab94` (2026-10-12T23:46:52Z), and five tags `data/pingyou-*`, all at the head, each a GitHub release whose assets carry later certificates (below, [Later Claims by the Same Author](#later-claims-by-the-same-author)).

## Source Custody

The tree has no licence file, and GitHub detects none.
The release READMEs say that upstream software and schema licences are retained beside the files they cover and that no new licence is asserted for third-party material; nothing grants one for the source's own files.
Under the derived-only form of the [existing retention policy](../known-best-packings/README.md), as for the 11 October PingYou packets, this packet keeps no upstream byte. No redistribution permission or licence determination is asserted.

`devtools.acquire_source` wrote the packet from a clone checked out at the pin, from the declaration in [acquisition/declaration.json](acquisition/declaration.json).
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and [acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest.
The scope is the eight paths the pinned commit changed: the six n153 files, first published by `bc328a7`, and `README.md` and `SHA256SUMS`.
All eight are pinned only; the declared `source/` directory is empty by design.

| Upstream path | Git blob | Bytes | SHA-256 | What it is |
| --- | --- | --- | --- | --- |
| `n153.cert.json` | `ebc6bde36a75023506dfc77be944074792dd3ea9` | 21403 | `1ca754f0238f958597ecddc645aa16f5c44c3afc9cf2614b40ce2fd1f6dea670` | The certificate |
| `pingyou-n153-rational.yaml` | `a5e4930027e02a953b0345e0f715b7054da8b251` | 114477 | `7cc142202fc39acfdd01060a6f89744a3f5815d6f193f03dfdb14d8c1f5c3567` | The same packing as a corners Witness/v2 |
| `README.md` | `1564e4391da5f365312751e87046433e31c2c089` | 9939 | `67deff49d275f1bc41ebe7f966116cedc65e7b1c1544f35fd79734b11d81d0d9` | Author prose for every release in the tree |
| `SHA256SUMS` | `911d36fea20fce61f2622a23cd9e1d1b454ca782` | 1543 | `87ac69e51c26832bf943a9b8a0d31425cf775750dd61cfbb9b5c2dd3a339e133` | The source's digests of the tree's release files |
| `n153-SHA256SUMS` | `22fccb702ddb1bebe435bf1887104a2c8e21969c` | 435 | `0d2b9a42e75adeef7c9734f2bb38ea3dc1cae8adf9bf1db295cf13c6e5e2a17b` | The source's digests of this release's files |
| `n153-squares-project.zip` | `c2195ca1ae861421ef55ef2f8cd703a2363b4ec1` | 256521 | `2a0e1affdd82cf613af58cfed03fad41b68a5392ae1de34450578c590ced6121` | The complete package, below |
| `n153-verified-comparison.pdf` | `d6fd32eea4f48037b0e84375ae13624792915d1c` | 129795 | `3a67e4cad430a7ba8d6739009de6c618336cd2aa47893010f01ad3b0513bef6b` | Comparison figure |
| `n153.svg` | `2d077f056c9127863a2ca2fc3c7326acc8abb28f` | 28006 | `071e69c276ece1761856173baaf827d1f50aad044eb6a567ddff64a03ad979a2` | Drawing |

The three digests the issue's update states, for the package, the certificate and the witness, are the ones above, and `n153-SHA256SUMS` lists the same digest for each of the five n153 artifacts it names.

## What the Package Holds

`n153-squares-project.zip` unpacks to `n153-squares-project/`, 54 files, 687,392 bytes.
Its `SHA256SUMS` lists a digest for each of the other 53, and every one equals the digest of the bytes unpacked here.
Byte for byte, `n153-squares-project/evidence/n153-verified-comparison.pdf` is `n153-verified-comparison.pdf`, `n153-squares-project/evidence/packing.cert.json` is `n153.cert.json`, `n153-squares-project/evidence/n153.svg` is `n153.svg`, `n153-squares-project/native/pingyou-n153-rational.yaml` is `pingyou-n153-rational.yaml`.
It holds 18 Python programs, `VERIFY.py` among them; they were read for what they claim and not run.
Among the rest are the construction table and its replay, the n70 parent, the author's polygon-projection checker and Evan Daniel's unchanged checkers, receipts, and the sources and licence of this repository's two checkers at `074ac28`.
Nothing in it is retained.

## The Certificate

`n153.cert.json` has the shape of the 11 October certificate without its metadata: `n`, `s_exact` and 153 `[x, y, t]` rows of rational strings, read with the `pingyou-json` adapter; `pingyou-n153-rational.yaml` states the same squares as rational corners, read with `witness-corners`.

As the source states it, the A=C return, the rational orientations and the guard $5000000000001/5000000000000$ are unchanged, and the centres and side are realized more tightly; the safe twelve-place print, 12.870013850408, is unchanged.

## Against the Record

At `main` `aeef99ef0` the case record's reported and verified ceilings at 153 are both T-148's (PingYou Ltd; `E-pingyou-504-exact-feasibility`), side `6435006925203522001385040447/500000000000000000000000000`. The certificate is below it by `5000000000001/500000000000000000000000000`, about $1.00 \times 10^{-14}$.

| Report | Holders | Side | Relation | Distance |
| --- | --- | --- | --- | --- |
| T-101 (#375) | the Kingbird catalogue, verified by Evan Daniel's exact ceiling | 12.8816667570090047 (retained, shown rounded up) | below | 0.0117 |
| T-125 (#432) | ry-xu | 12.8813062182128813062182 (retained, exact) | below | 0.0113 |
| T-127 (#438) | Nate Chaoweeraprasit (itsnaka), improved by Siddharth Gupta | 12.8796793733293146 (retained, shown rounded up) | below | 0.00967 |
| T-136 (#481) | Nate Chaoweeraprasit | 12.8720298490811809 (retained, shown rounded up) | below | 0.00202 |
| T-146 (regularized lists) | Evan Daniel, regularizing Nate Chaoweeraprasit's packing | 12.8720298490811800 (retained, shown rounded up) | below | 0.00202 |
| #573 | Mishapolk | 12.870013850405 (printed, rounded up) | above | 2.03e-12 |
| #593 | Mishapolk (Mykhailo Polkovskyi) | 12.8700138504044794 (printed, rounding unstated) | above | 2.55e-12 |
| PR #574 | PingYou Ltd | 12.87001385040446434446015340078059 (printed, rounding unstated) | above | 2.57e-12 |

A relation is this certificate's against the other side: *below* means this side is smaller. No report is decidably smallest: the prints do not order #573 and PR #574.

Measured square for square against T-148's certificate, in order, it is the same packing: 151 squares moved by less than $10^{-9}$ and two by more, the farther by 0.0898, and no square turned. The side is smaller by exactly `5000000000001/500000000000000000000000000`, the $1.0000000000002 \times 10^{-14}$ the comment states. Mishapolk's #573 and #593 print smaller sides, from a new arrangement by their account, and the author's own PR #574 states smaller ones still (below). T-114 has no packet reader here, and `devtools.check_standing` at `main` marks it beaten at 153.
[acquisition/claims.json](acquisition/claims.json) freezes these comparisons, and `devtools.upper_bound_reports` rebuilds them from the retained packets.

## Derived Fact and Exact Replay

`devtools.upper_bound_reports derive` read `n153.cert.json` from a checkout at the pin, after `devtools.acquire_source` showed that the checkout yields this packet's acquisition record and manifest, so the bytes it read have the digests above.
It admitted the certificate at the exact fraction the comment prints.
It then read `pingyou-n153-rational.yaml` from the same checkout, as the row's `same_packing` file: all 153 poses and the side are the certificate's exactly.
It wrote the certificate as an exact rational `center-basis` Witness/v2, [facts/n-153.yaml.gz](facts/n-153.yaml.gz), naming the certificate's SHA-256 as `revision_sha256`. The fact is this repository's derivation; offline it must rebuild itself from the certificate it states, and `derive --check` with a checkout compares the fact and the witness again.
The declaration of the import is [acquisition/report.json](acquisition/report.json).

Only the fact enters geometry decisions, through the two-route kernel of `devtools.evand_arrangement_reports`: `sqpack`'s exact witness verifier and the independent rational corner checker, each deciding every wall and every pair over $\mathbb{Q}$.
A positive job, a duplicate-square control and an outside-container control each ran in its own child process, one worker at a time. The positive passes both routes and both routes refuse both controls. Both routes find the same margins: the least wall clearance exactly `1/10000000000000` and the least pair gap `230569505416935261362883180425398357880233/1226584712095994044292471156900000000000000000000000000`, about $1.88 \times 10^{-13}$.
The three jobs made 69,768 pair decisions in 12.55 route CPU seconds and 36.81 job wall seconds, summed; the longest took 12.43 seconds, and `certify` 45 seconds of wall time, with other lanes on the machine.
A fresh `check --replay` decided all three jobs again, equal to the retained rows apart from timing, in 24 seconds.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every deciding input and both routes' complete outputs.
The two routes share certificate parsing, the half-angle conversion, Python's rational arithmetic and the separating-axis method.

The release reports that `packing-witness verify` and `devtools.check_rational_witness_independent`, unchanged at `074ac28`, accept its own witness file; `n153-squares-project/native/native-replay.json` is that receipt. The two maintained routes here decided the certificate from the derived fact; the source's witness file was compared with the certificate pose for pose and not decided separately.

## What Is Not Established

The source reports that its three exact checkers accept all 11,628 pairs and every wall and that its replay rebuilds the certificate from the construction table. Those are author reports.
`VERIFY.py`, the package's checkers, its construction replay, `convert_witness.py` and `replay_upstream.py` were read here and not run: the two maintained routes decide the certificate from its own poses, so none is needed for the bound.
The replay above has not been reviewed.
The certificate establishes a finite upper bound only; the source claims no local or global optimality.

## Later Claims by the Same Author

The author has since submitted further certificates at this count, outside this packet's scope. [PR #574](https://github.com/jlevy/squares/pull/574) (opened 2026-10-13T00:13Z from `BuddenPing/squares`, head `4c319c2`, open and unmerged) requests 148 certificate refinements, and the GitHub releases at the tags `data/pingyou-numerical-refinements-2026-10-13-v1` and `-v2`, `data/pingyou-exact-153-302-2026-10-13(-v1)` and `data/pingyou-algebraic-refinements-2026-10-13-v1`, all on the head, carry them as assets that are not in the Git tree. At 153 it states a rational certificate, about 12.870013850404466647261…, $2.57 \times 10^{-12}$ below this one, and an exact algebraic certificate attaining $12 + (1 + 3t^2)/(1 + 2t - t^2)$ at a root of $t^7 - 9t^6 + 3t^5 - t^4 - t^3 + t^2 - 3t + 1$ in $(7/20, 9/25)$, about 12.87001385040446434446015340078059, a further $2.30 \times 10^{-15}$ below. Read from the PR's `claims.json` files at its head, as data; neither the PR nor the release assets were retained or replayed here, and they are an import of their own.

## Credit

The source credits PingYou Ltd with the construction and its refinement, Ryan Xu with the n70 construction it starts from ([#432](https://github.com/jlevy/squares/issues/432)), Evan Daniel with the exact retention of that construction and with exact checking tools, and SQUISH's n153 ([#481](https://github.com/jlevy/squares/issues/481)) only as the earlier comparison.

The pinned source makes no statement about AI assistance, and neither does the comment. Asked on #503 which account of AI assistance stands, the author answered on 12 October 2026 for the n207 and n153 releases ([comment](https://github.com/jlevy/squares/issues/503#issuecomment-6129716138)): “Both solutions were AI assisted by ‘PY’, an unreleased agentic AI offering by PingYou Ltd.” The refinement states nothing further.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source pingyou-n153-refinement-2026-10-12 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-n153-refinement-2026-10-12 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-n153-refinement-2026-10-12 check --replay
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-n153-refinement-2026-10-12 derive --checkout CHECKOUT --check
```

`--check` re-derives the record from this packet alone.
The importer's `check-claims` and `check --replay` run offline from the fact;
`derive --check` needs a checkout at the pin, refuses one that does not yield this
packet's record and manifest, and compares the fact and the source's witness with the
certificate.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `facts/n-153.yaml.gz` | receipt | `656747a72c6f74d3fd8fd71dd6c68d8e4d438deb` | `5880d4eaa845513136a22225e6ad3d2d5007535e4ef940ce5efb58727870a4a6` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
