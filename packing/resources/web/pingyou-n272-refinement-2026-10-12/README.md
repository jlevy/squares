# PingYou Ltd: A Contact Refinement at 272

[Issue #569](https://github.com/jlevy/squares/issues/569) (BuddenPing, 2026-10-12T22:58Z) reports an exact contact refinement of Nate Chaoweeraprasit's SQUISH packing of 272 (T-151) in [BuddenPing/square-packing-certificates](https://github.com/BuddenPing/square-packing-certificates/tree/260aaf50230483654802790589c2dfce73237604) at `260aaf50230483654802790589c2dfce73237604` (tree `77398835e64d7623683e164080b9628d6c4c9221`, committed 2026-10-12T22:57:18Z, parent `21498b1`), the revision the issue names. The same commit finalized the n105 release, which [its own packet](../pingyou-n105-refinement-2026-10-12/README.md) retains.
The source was retrieved at 2026-10-14T04:47Z, when its branch head was `318ab94e821ba7280a68fa8ce2942c9ecdbda41d`; every file of this packet's scope has the same blob there.

| n | Exact side of the certificate | Rounded up at 16 places |
| --- | --- | --- |
| 272 | exact, with a 111-digit denominator | 16.9655864748376707 |

## Who the Source Is

As for the [n207](../pingyou-n207-certificate-2026-10-11/README.md#who-the-source-is) and [n153](../pingyou-n153-certificate-2026-10-11/README.md) packets of 11 October: the repository describes itself as “Exact square-packing certificates and reproducible verification from PingYou Ltd”, its README is headed “Square-packing certificates — PingYou Ltd”, and every commit is authored as `BuddenPing` from an address at the `pingyou.com` domain. GitHub detects no licence and the account names no person or company. The source names no individual author, and this packet names none.
At retrieval `main` held sixteen commits, the head `318ab94` (2026-10-12T23:46:52Z), and five tags `data/pingyou-*`, all at the head, each a GitHub release whose assets carry later certificates (below, [Later Claims by the Same Author](#later-claims-by-the-same-author)).

## Source Custody

The tree has no licence file, and GitHub detects none.
The release READMEs say that upstream software and schema licences are retained beside the files they cover and that no new licence is asserted for third-party material; nothing grants one for the source's own files.
Under the derived-only form of the [existing retention policy](../known-best-packings/README.md), as for the 11 October PingYou packets, this packet keeps no upstream byte. No redistribution permission or licence determination is asserted.

`devtools.acquire_source` wrote the packet from a clone checked out at the pin, from the declaration in [acquisition/declaration.json](acquisition/declaration.json).
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and [acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest.
The scope is the seven n272 files the pinned commit adds and `witness.schema.yaml`, which `n272-SHA256SUMS` names.
All eight are pinned only; the declared `source/` directory is empty by design. The schema's digest equals that of this repository's `packing/witnesses/witness.schema.yaml` at `main` `aeef99ef0`.

| Upstream path | Git blob | Bytes | SHA-256 | What it is |
| --- | --- | --- | --- | --- |
| `n272.cert.json` | `80350e7ee962e3c5ab23101cc01f5bb5dbc374f7` | 150545 | `1bfe74e4af5dba4bfb6865ad953ff169620c2b85d91f919abd0ef5527cae21e0` | The certificate |
| `pingyou-n272-rational.yaml` | `bdbd82f15b728ccb236277895f81594d22803930` | 840580 | `b620b946df1c5f9ab2926c9d545dbf5de42d11f5f1f58d2329655abd0a38820d` | The same packing as a corners Witness/v2 |
| `n272-README.txt` | `0b0d1483b51a1c3b38c9482516e1c026b6550251` | 3195 | `be84525d1b247db55391302c1a662f6516bb2adacd8af8bc4ff20702e86fa9b4` | Author prose: claim, method, credit, replay |
| `n272-SHA256SUMS` | `21e537dab2110c0575d3662b44c0e9451a7064e8` | 612 | `8022b9f3cf921a02935e54be31afb9b5d2948bdc14b59b648b31ceb3854d3e6d` | The source's digests of this release's files |
| `n272-native-replay.json` | `9bd61974cce475b8c48fec2d4c472ad5ebbd2fc9` | 4483 | `19d759cdab86d4755c7b8c443cb9787ad6ea461e8b5f1723bd2b8ef5e1d8eaf9` | The author's receipt of this repository's two checkers at `074ac28` |
| `n272-squares-project.zip` | `a934b67ad80ef7e3ff32ae88d8404686cfa5c933` | 464822 | `ccc49fa5c2660a4cc95255951870e2f0d271272cd9c2d698755e55ccd32d3a5e` | The complete package, below |
| `n272-verification.json` | `3f0dafce33af666749cf668a5735b0009a34f51b` | 3388 | `eb2d84da9d7b34ffc6c7fec02ccb2ff01c1d1b4e96ea2d5fd34ae2ccd6dc1cc9` | The author's receipt of its own exact checks |
| `witness.schema.yaml` | `e24b54308721eb1660d4c19a2640b06324c04d82` | 9013 | `754ddd6eea0558344c174302318ed1e7235d9665f37ef4f6fdea1f1e627664dc` | This repository's witness schema, as the source copied it |

The certificate digest the issue states is the one above, and `n272-SHA256SUMS` lists the same digest for each of the other seven files of the scope.

## What the Package Holds

`n272-squares-project.zip` unpacks to `n272-squares-project/`, 65 files, 2,725,975 bytes.
Its `SHA256SUMS` lists a digest for each of the other 64, and every one equals the digest of the bytes unpacked here.
Byte for byte, `n272-squares-project/README.txt` is `n272-README.txt`, `n272-squares-project/evidence/native-replay.json` is `n272-native-replay.json`, `n272-squares-project/evidence/independent-verification.json` is `n272-verification.json`, `n272-squares-project/n272.cert.json` is `n272.cert.json`, `n272-squares-project/pingyou-n272-rational.yaml` is `pingyou-n272-rational.yaml`.
It holds 20 Python programs, `VERIFY.py` among them; they were read for what they claim and not run.
Among the rest are the construction equations, solver states and source, SQUISH's source certificate, an independently reconstructed pre-stationarity projection, a scoped rational dual bound, the author's exact checkers, and the sources and licence of this repository's two checkers at `074ac28`.
Nothing in it is retained.

## The Certificate

`n272.cert.json` holds `n`, `s_exact` and 272 `[x, y, t]` rows of rational strings, read with the `pingyou-json` adapter; `pingyou-n272-rational.yaml` states the same squares as rational corners, read with `witness-corners`.

As the source states it, Evan Daniel's solver at `31523f8`, seeded with SQUISH's certificate at `itsnaka/squish-certs` `56fa71f`, solved its 1,564 inherited incidence equations with the stationarity system, 22 translation coordinates frozen, at 100 and 120 digits, and the witness uses the 120-digit result with a $10^{-100}$ rational guard.

## Against the Record

At `main` `aeef99ef0` the case record's reported and verified ceilings at 272 are both T-151's (Nate Chaoweeraprasit (itsnaka); `E-squish-500-exact-feasibility`), side 16.9655864748376712 rounded up, its exact fraction in the claim record. The certificate is below it by $5.26 \times 10^{-16}$ (exactly; the fraction is in the claim record).

| Report | Holders | Side | Relation | Distance |
| --- | --- | --- | --- | --- |
| T-098 (#375) | Francisco Couzo, improved by Evan Daniel | 16.9681658678521584 (retained, shown rounded up) | below | 0.00258 |
| T-119 (#399) | Evan Daniel | 16.9681101457696006 (retained, shown rounded up) | below | 0.00252 |
| #593 | Mishapolk (Mykhailo Polkovskyi) | 16.9655864748376715 (printed, rounding unstated) | below | 8.64e-16 |
| PR #574 | PingYou Ltd | 16.9655864748376706357560070334220455696299 (printed, rounded up) | undecided | 2.42e-41 |

A relation is this certificate's against the other side: *below* means this side is smaller. No report is decidably smallest: the prints do not order this certificate and PR #574.

Measured square for square against T-151's certificate, in order, it is the same packing: 245 squares moved by less than $10^{-9}$ and 27 by more, none by more than $1.15 \times 10^{-7}$, and 38 turned, none by more than $1.42 \times 10^{-5}$ degrees. The side is $5.26 \times 10^{-16}$ smaller, the margin the issue states. Only the author's own PR #574 states a smaller side (below), by a margin its print does not resolve. T-056 and T-092 have no packet reader here, and `devtools.check_standing` at `main` marks both superseded.
[acquisition/claims.json](acquisition/claims.json) freezes these comparisons, and `devtools.upper_bound_reports` rebuilds them from the retained packets.

## Derived Fact and Exact Replay

`devtools.upper_bound_reports derive` read `n272.cert.json` from a checkout at the pin, after `devtools.acquire_source` showed that the checkout yields this packet's acquisition record and manifest, so the bytes it read have the digests above.
It admitted the certificate at the exact fraction the issue prints.
It then read `pingyou-n272-rational.yaml` from the same checkout, as the row's `same_packing` file: all 272 poses and the side are the certificate's exactly.
It wrote the certificate as an exact rational `center-basis` Witness/v2, [facts/n-272.yaml.gz](facts/n-272.yaml.gz), naming the certificate's SHA-256 as `revision_sha256`. The fact is this repository's derivation; offline it must rebuild itself from the certificate it states, and `derive --check` with a checkout compares the fact and the witness again.
The declaration of the import is [acquisition/report.json](acquisition/report.json).

Only the fact enters geometry decisions, through the two-route kernel of `devtools.evand_arrangement_reports`: `sqpack`'s exact witness verifier and the independent rational corner checker, each deciding every wall and every pair over $\mathbb{Q}$.
A positive job, a duplicate-square control and an outside-container control each ran in its own child process, one worker at a time. The positive passes both routes and both routes refuse both controls. Both routes find the same margins: the least wall clearance exactly `1/20000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000` and the least pair gap a rational of 1,043 characters, whose denominator has 571 digits, longer than the 1,024 characters the kernel's receipt check admitted before this import, about $1.00 \times 10^{-100}$.
The three jobs made 221,136 pair decisions in 185.95 route CPU seconds and 240.0 job wall seconds, summed; the longest took 106.39 seconds, and `certify` 245 seconds of wall time, with other lanes on the machine.
A fresh `check --replay` decided all three jobs again, equal to the retained rows apart from timing, in 575 seconds.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every deciding input and both routes' complete outputs.
The two routes share certificate parsing, the half-angle conversion, Python's rational arithmetic and the separating-axis method.

The release reports that `packing-witness verify` and `devtools.check_rational_witness_independent`, unchanged at `074ac28`, accept its own witness file; `n272-native-replay.json` is that receipt. The two maintained routes here decided the certificate from the derived fact; the source's witness file was compared with the certificate pose for pose and not decided separately.

## What Is Not Established

The source reports that its exact separating-axis and polygon checkers accept all 36,856 pairs and every wall, for the new witness, SQUISH's certificate and its projection, and that its dual bound holds within a stated angular neighbourhood. Those are author reports.
`VERIFY.py`, the package's checkers, its construction replay, `convert_witness.py` and `replay_upstream.py` were read here and not run: the two maintained routes decide the certificate from its own poses, so none is needed for the bound.
The replay above has not been reviewed.
The certificate establishes a finite upper bound only; the source claims no local or global optimality.

## Later Claims by the Same Author

The author has since submitted further certificates at this count, outside this packet's scope. [PR #574](https://github.com/jlevy/squares/pull/574) (opened 2026-10-13T00:13Z from `BuddenPing/squares`, head `4c319c2`, open and unmerged) requests 148 certificate refinements, and the GitHub releases at the tags `data/pingyou-numerical-refinements-2026-10-13-v1` and `-v2`, `data/pingyou-exact-153-302-2026-10-13(-v1)` and `data/pingyou-algebraic-refinements-2026-10-13-v1`, all on the head, carry them as assets that are not in the Git tree. At 272 it states a rational certificate (v2) whose pre-batch comparison is this release's `n272.cert.json`, by digest, $1.70 \times 10^{-99}$ below it; its 40-place print is the issue's. Read from the PR's `claims.json` files at its head, as data; neither the PR nor the release assets were retained or replayed here, and they are an import of their own.

## Credit

The source credits PingYou Ltd with this contact refinement and submission, Nate Chaoweeraprasit (SQUISH) with the original arrangement, including its SQUISH s(240) and former Kingbird s(182) components, and Evan Daniel with the contact solver; the native verifiers and schema are credited to this project.

The issue states: “Computation, checking and submission preparation were AI-assisted; the requested attribution is as stated above.” The pinned source makes no statement about AI assistance. Asked on #503 which account of AI assistance stands, the author answered on 12 October 2026 for the n207 and n153 releases ([comment](https://github.com/jlevy/squares/issues/503#issuecomment-6129716138)): “Both solutions were AI assisted by ‘PY’, an unreleased agentic AI offering by PingYou Ltd.” The issue names no tool.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source pingyou-n272-refinement-2026-10-12 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-n272-refinement-2026-10-12 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-n272-refinement-2026-10-12 check --replay
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-n272-refinement-2026-10-12 derive --checkout CHECKOUT --check
```

`--check` re-derives the record from this packet alone.
The importer's `check-claims` and `check --replay` run offline from the fact;
`derive --check` needs a checkout at the pin, refuses one that does not yield this
packet's record and manifest, and compares the fact and the source's witness with the
certificate.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `facts/n-272.yaml.gz` | receipt | `43fef17475481b80306bcb9cda732eae438312ee` | `385af97b85d98381bce5d01e0582d495485095a5e2dcf4cb705c06358ad13d4e` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
