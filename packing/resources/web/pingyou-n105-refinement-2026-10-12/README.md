# PingYou Ltd: A Contact Refinement at 105

[Issue #568](https://github.com/jlevy/squares/issues/568) (BuddenPing, 2026-10-12T22:57Z) reports an exact contact refinement of Francisco Couzo's refinement (T-130) of Ryan Xu's packing of 105 in [BuddenPing/square-packing-certificates](https://github.com/BuddenPing/square-packing-certificates/tree/260aaf50230483654802790589c2dfce73237604) at `260aaf50230483654802790589c2dfce73237604` (tree `77398835e64d7623683e164080b9628d6c4c9221`, committed 2026-10-12T22:57:18Z, parent `21498b1`), the revision the issue names. The parent, `21498b1` (22:53:57Z), first published the certificate and witness; the pin finalized the package and its digest list and added the n272 release, which [its own packet](../pingyou-n272-refinement-2026-10-12/README.md) retains.
The source was retrieved at 2026-10-14T04:47Z, when its branch head was `318ab94e821ba7280a68fa8ce2942c9ecdbda41d`; every file of this packet's scope has the same blob there.

| n | Exact side of the certificate | Rounded up at 16 places |
| --- | --- | --- |
| 105 | exact, with a 91-digit denominator | 10.7893037837481589 |

## Who the Source Is

As for the [n207](../pingyou-n207-certificate-2026-10-11/README.md#who-the-source-is) and [n153](../pingyou-n153-certificate-2026-10-11/README.md) packets of 11 October: the repository describes itself as “Exact square-packing certificates and reproducible verification from PingYou Ltd”, its README is headed “Square-packing certificates — PingYou Ltd”, and every commit is authored as `BuddenPing` from an address at the `pingyou.com` domain. GitHub detects no licence and the account names no person or company. The source names no individual author, and this packet names none.
At retrieval `main` held sixteen commits, the head `318ab94` (2026-10-12T23:46:52Z), and five tags `data/pingyou-*`, all at the head, each a GitHub release whose assets carry later certificates (below, [Later Claims by the Same Author](#later-claims-by-the-same-author)).

## Source Custody

The tree has no licence file, and GitHub detects none.
The release READMEs say that upstream software and schema licences are retained beside the files they cover and that no new licence is asserted for third-party material; nothing grants one for the source's own files.
Under the derived-only form of the [existing retention policy](../known-best-packings/README.md), as for the 11 October PingYou packets, this packet keeps no upstream byte. No redistribution permission or licence determination is asserted.

`devtools.acquire_source` wrote the packet from a clone checked out at the pin, from the declaration in [acquisition/declaration.json](acquisition/declaration.json).
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and [acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest.
The scope is the seven n105 files and `witness.schema.yaml`, which `n105-SHA256SUMS` names.
All eight are pinned only; the declared `source/` directory is empty by design. The schema's digest equals that of this repository's `packing/witnesses/witness.schema.yaml` at `main` `aeef99ef0`.

| Upstream path | Git blob | Bytes | SHA-256 | What it is |
| --- | --- | --- | --- | --- |
| `n105.cert.json` | `d38844e8c28955af805924e81084288618300729` | 50814 | `8c684d15e87e772bec491f0c77db5b87c0246883875f5c0ad8b0c8a8ac8cd613` | The certificate |
| `pingyou-n105-rational.yaml` | `6a930fea1f7081a344245e84198e012a1c1cd8f9` | 301623 | `a5d68be5bcd77df8f00e9a76a752f86bb432ec2cd1890599b6c3e51238ad71e0` | The same packing as a corners Witness/v2 |
| `n105-README.txt` | `11b6dac14fce3796e1c1c4e42d548c938fa19dc5` | 2941 | `9119b28da24fa5965893804de0ba7417a92b3bc53b2d2815c27e7b2460cd34a0` | Author prose: claim, method, credit, replay |
| `n105-SHA256SUMS` | `2a0f03b24522c22d9f5b1d7cfc83e57ebc4be35f` | 612 | `1a3aeef496f61a461be41d726e7ec1dc627819e7fafea51e239a61949741b546` | The source's digests of this release's files |
| `n105-native-replay.json` | `14e4ac17ad85fd9ac6f555714cc4d27926f1244a` | 3253 | `d3dbde0a37288ff32ca31d55f60663600197661781020ff064a1e50c2c123c84` | The author's receipt of this repository's two checkers at `074ac28` |
| `n105-squares-project.zip` | `755ab261425518f238e9088959ff9d89d0ac2d28` | 208607 | `edce24020838408deabf632b4f676eb28f86a9f0a1a07ec3da05b5269a96a929` | The complete package, below |
| `n105-verification.json` | `61fd5736a406a3ac2e0590627df8fb8cce23fd42` | 5619 | `3a17e8d0aab351c703a04104dadf18cdd4a299f151f25c86e38f0ca6ee8ec1be` | The author's receipt of its own exact checks |
| `witness.schema.yaml` | `e24b54308721eb1660d4c19a2640b06324c04d82` | 9013 | `754ddd6eea0558344c174302318ed1e7235d9665f37ef4f6fdea1f1e627664dc` | This repository's witness schema, as the source copied it |

The certificate digest the issue states is the one above, and `n105-SHA256SUMS` lists the same digest for each of the other seven files of the scope.

## What the Package Holds

`n105-squares-project.zip` unpacks to `n105-squares-project/`, 49 files, 877,638 bytes.
Its `SHA256SUMS` lists a digest for each of the other 48, and every one equals the digest of the bytes unpacked here.
Byte for byte, `n105-squares-project/README.txt` is `n105-README.txt`, `n105-squares-project/evidence/native-replay.json` is `n105-native-replay.json`, `n105-squares-project/evidence/independent-verification.json` is `n105-verification.json`, `n105-squares-project/n105.cert.json` is `n105.cert.json`, `n105-squares-project/pingyou-n105-rational.yaml` is `pingyou-n105-rational.yaml`.
It holds 18 Python programs, `VERIFY.py` among them; they were read for what they claim and not run.
Among the rest are the method and provenance, Francisco Couzo's source certificate, the 140-digit solver report and its equations, Evan Daniel's solver licence, the author's exact checkers, and the sources and licence of this repository's two checkers at `074ac28`. Its optional `RECONSTRUCT.py` fetches Evan Daniel's solver over the network.
Nothing in it is retained.

## The Certificate

`n105.cert.json` holds `n`, `s_exact` and 105 `[x, y, t]` rows of rational strings, read with the `pingyou-json` adapter; `pingyou-n105-rational.yaml` states the same squares as rational corners, read with `witness-corners`.

As the source states it, Evan Daniel's solver at `77f3c0a`, seeded with Francisco Couzo's guarded certificate at `franciscouzo/square-packing` `93570ef`, projected onto its 435 inherited corner, edge and wall equations and closed them with 32 translation coordinates frozen, at 140 digits, with a $10^{-80}$ rational guard. Couzo's writer dilates by $1 + 10^{-20}$ and rounds the side up at 30 places; the author shows the new side below every unpadded design that writer could have started from, by more than $4.29 \times 10^{-29}$.

## Against the Record

At `main` `aeef99ef0` the case record's reported and verified ceilings at 105 are both T-130's (ry-xu, improved by Francisco Couzo; `E-couzo-460-followup-exact-feasibility`), side `10789303783748158831034729697921/1000000000000000000000000000000`. The certificate is below it by $1.08 \times 10^{-19}$ (exactly; the fraction is in the claim record).

| Report | Holders | Side | Relation | Distance |
| --- | --- | --- | --- | --- |
| T-117 (#425) | Francisco Couzo, improved by Seth Rehwaldt | 10.8060778655197047 (retained, shown rounded up) | below | 0.0168 |
| T-125 (#432) | ry-xu | 10.7906765754107906765754 (retained, exact) | below | 0.00137 |
| T-128 (#451) | Francisco Couzo | 10.7906182681071446 (retained, shown rounded up) | below | 0.00131 |
| T-138 (#470) | Mishapolk | 10.789303783751 (retained, exact) | below | 2.84e-12 |
| #593 | Mishapolk (Mykhailo Polkovskyi) | 10.7893037837481582 (printed, rounding unstated) | above | 6.31e-16 |
| PR #574 | PingYou Ltd | 10.7893037837481588309268366600396176597363 (printed, rounded up) | undecided | 8.13e-41 |

A relation is this certificate's against the other side: *below* means this side is smaller. The smallest report at the count is #593.

Measured square for square against T-130's certificate, whose side is the side the issue quotes for its source, in order, it is the same packing: no centre moved by more than $1.03 \times 10^{-19}$, 36 half-angle tangents changed, by at most $1.04 \times 10^{-23}$, and the side is $1.08 \times 10^{-19}$ smaller. That is the scale of the source's certification padding, and the issue says as much: its improvement over the unpadded design is the $4.29 \times 10^{-29}$ above. Mishapolk's #593 prints a side about $6 \times 10^{-16}$ smaller, and the author's own PR #574 states a smaller one (below). T-129 and T-056 have no packet reader here, and `devtools.check_standing` at `main` marks both superseded.
[acquisition/claims.json](acquisition/claims.json) freezes these comparisons, and `devtools.upper_bound_reports` rebuilds them from the retained packets.

## Derived Fact and Exact Replay

`devtools.upper_bound_reports derive` read `n105.cert.json` from a checkout at the pin, after `devtools.acquire_source` showed that the checkout yields this packet's acquisition record and manifest, so the bytes it read have the digests above.
It admitted the certificate at the exact fraction the issue prints.
It then read `pingyou-n105-rational.yaml` from the same checkout, as the row's `same_packing` file: all 105 poses and the side are the certificate's exactly.
It wrote the certificate as an exact rational `center-basis` Witness/v2, [facts/n-105.yaml.gz](facts/n-105.yaml.gz), naming the certificate's SHA-256 as `revision_sha256`. The fact is this repository's derivation; offline it must rebuild itself from the certificate it states, and `derive --check` with a checkout compares the fact and the witness again.
The declaration of the import is [acquisition/report.json](acquisition/report.json).

Only the fact enters geometry decisions, through the two-route kernel of `devtools.evand_arrangement_reports`: `sqpack`'s exact witness verifier and the independent rational corner checker, each deciding every wall and every pair over $\mathbb{Q}$.
A positive job, a duplicate-square control and an outside-container control each ran in its own child process, one worker at a time. The positive passes both routes and both routes refuse both controls. Both routes find the same margins: the least wall clearance exactly `1/200000000000000000000000000000000000000000000000000000000000000000000000000000000` and the least pair gap a rational of 489 characters, whose denominator has 284 digits, about $1.00 \times 10^{-80}$.
The three jobs made 32,760 pair decisions in 21.77 route CPU seconds and 29.39 job wall seconds, summed; the longest took 11.04 seconds, and `certify` 32 seconds of wall time, with other lanes on the machine.
A fresh `check --replay` decided all three jobs again, equal to the retained rows apart from timing, in 33 seconds.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every deciding input and both routes' complete outputs.
The two routes share certificate parsing, the half-angle conversion, Python's rational arithmetic and the separating-axis method.

The release reports that `packing-witness verify` and `devtools.check_rational_witness_independent`, unchanged at `074ac28`, accept its own witness file; `n105-native-replay.json` is that receipt. The two maintained routes here decided the certificate from the derived fact; the source's witness file was compared with the certificate pose for pose and not decided separately.

## What Is Not Established

The source reports that its exact separating-axis and polygon checkers accept all 5,460 pairs and every wall, and that an inverse-dilation control reproduces the source side and its 97 nonfree rows. Those are author reports, as is the comparison with the unpadded design.
`VERIFY.py`, the package's checkers, its construction replay, `convert_witness.py` and `replay_upstream.py` were read here and not run: the two maintained routes decide the certificate from its own poses, so none is needed for the bound.
The replay above has not been reviewed.
The certificate establishes a finite upper bound only; the source claims no local or global optimality.

## Later Claims by the Same Author

The author has since submitted further certificates at this count, outside this packet's scope. [PR #574](https://github.com/jlevy/squares/pull/574) (opened 2026-10-13T00:13Z from `BuddenPing/squares`, head `4c319c2`, open and unmerged) requests 148 certificate refinements, and the GitHub releases at the tags `data/pingyou-numerical-refinements-2026-10-13-v1` and `-v2`, `data/pingyou-exact-153-302-2026-10-13(-v1)` and `data/pingyou-algebraic-refinements-2026-10-13-v1`, all on the head, carry them as assets that are not in the Git tree. At 105 it states a rational certificate (v2) whose pre-batch comparison is this release's `n105.cert.json`, by digest, $1.08 \times 10^{-79}$ below it; its 40-place print is the issue's. Read from the PR's `claims.json` files at its head, as data; neither the PR nor the release assets were retained or replayed here, and they are an import of their own.

## Credit

The source credits PingYou Ltd with this contact refinement and submission, Ryan Xu with the original layout, Francisco Couzo with the preceding refinement, and Evan Daniel with the contact solver; the native verifiers and schema are credited to this project.

The issue states: “Computation, checking and submission preparation were AI-assisted; the requested attribution is as stated above.” The pinned source makes no statement about AI assistance. Asked on #503 which account of AI assistance stands, the author answered on 12 October 2026 for the n207 and n153 releases ([comment](https://github.com/jlevy/squares/issues/503#issuecomment-6129716138)): “Both solutions were AI assisted by ‘PY’, an unreleased agentic AI offering by PingYou Ltd.” The issue names no tool.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source pingyou-n105-refinement-2026-10-12 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-n105-refinement-2026-10-12 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-n105-refinement-2026-10-12 check --replay
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-n105-refinement-2026-10-12 derive --checkout CHECKOUT --check
```

`--check` re-derives the record from this packet alone.
The importer's `check-claims` and `check --replay` run offline from the fact;
`derive --check` needs a checkout at the pin, refuses one that does not yield this
packet's record and manifest, and compares the fact and the source's witness with the
certificate.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `facts/n-105.yaml.gz` | receipt | `d8341588b3e6d08717c5d7536111e1dd55540418` | `516af7f35e390fe6c915ea915b8ed8254c82fe9c9b2530d836062c76911bfcc5` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
