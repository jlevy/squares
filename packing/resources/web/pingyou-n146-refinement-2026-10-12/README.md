# PingYou Ltd: A Further Refinement at 146

[Issue #566](https://github.com/jlevy/squares/issues/566) (BuddenPing, opened 2026-10-12T22:38Z; title and body replaced at 23:41Z, with a comment saying so) reports a further refinement of Robert Barnett's refinement (T-150) of Ryan Xu's packing of 146 in [BuddenPing/square-packing-certificates](https://github.com/BuddenPing/square-packing-certificates/tree/820b9ffb11dd602d735f7a03cd472db98a2d3bb6) at `820b9ffb11dd602d735f7a03cd472db98a2d3bb6` (tree `32adc0e3cfbb0159774d36500055ef303faddf48`, committed 2026-10-12T23:41:08Z, parent `2030fd1`), the revision the updated issue names. The issue's first version cited `18092df`, whose certificate this one replaces, about $1.32 \times 10^{-13}$ larger; it is not retained.
The source was retrieved at 2026-10-14T04:47Z, when its branch head was `318ab94e821ba7280a68fa8ce2942c9ecdbda41d`; every file of this packet's scope has the same blob there.

| n | Exact side of the certificate | Rounded up at 16 places |
| --- | --- | --- |
| 146 | exact, with a 90-digit denominator | 12.5837822039508343 |

## Who the Source Is

As for the [n207](../pingyou-n207-certificate-2026-10-11/README.md#who-the-source-is) and [n153](../pingyou-n153-certificate-2026-10-11/README.md) packets of 11 October: the repository describes itself as “Exact square-packing certificates and reproducible verification from PingYou Ltd”, its README is headed “Square-packing certificates — PingYou Ltd”, and every commit is authored as `BuddenPing` from an address at the `pingyou.com` domain. GitHub detects no licence and the account names no person or company. The source names no individual author, and this packet names none.
At retrieval `main` held sixteen commits, the head `318ab94` (2026-10-12T23:46:52Z), and five tags `data/pingyou-*`, all at the head, each a GitHub release whose assets carry later certificates (below, [Later Claims by the Same Author](#later-claims-by-the-same-author)).

## Source Custody

The tree has no licence file, and GitHub detects none.
The release READMEs say that upstream software and schema licences are retained beside the files they cover and that no new licence is asserted for third-party material; nothing grants one for the source's own files.
Under the derived-only form of the [existing retention policy](../known-best-packings/README.md), as for the 11 October PingYou packets, this packet keeps no upstream byte. No redistribution permission or licence determination is asserted.

`devtools.acquire_source` wrote the packet from a clone checked out at the pin, from the declaration in [acquisition/declaration.json](acquisition/declaration.json).
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and [acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest.
The scope is the seven n146 paths the pinned commit changed, first published by `18092df`. The tree's `README.md` and `SHA256SUMS` index them only from the head, outside the scope.
All seven are pinned only; the declared `source/` directory is empty by design.

| Upstream path | Git blob | Bytes | SHA-256 | What it is |
| --- | --- | --- | --- | --- |
| `n146.cert.json` | `cef0bde00d6ee236b4c2aa064b50a974139e225a` | 68539 | `a88ede7e2faa9d62fe8b6d0e46f7d38dde7df1f5a198d15bc6d6d726df77d13d` | The certificate |
| `pingyou-n146-rational.yaml` | `ae50c0961acbce4a0a3a30e7e92947eca2ed1845` | 374604 | `15c7ce633c73e8ac6a60b6e1cffef81e76ae4c5beb28efd643c9c3a62e843ee4` | The same packing as a corners Witness/v2 |
| `n146-README.txt` | `8f9860d4e70494cee82d58626789890c0495e48e` | 2618 | `5f01faa0d31fa34b1ee793c606e8eda8deb9247f7893c2cfe333642f2c9bc398` | Author prose: claim, method, credit, replay |
| `n146-SHA256SUMS` | `a13581e8b401c41035775bf5d6101e2bf3d85136` | 5989 | `30156d7461897c8a49aa7fdefa05fe2bdc017d505288f47c02049bc6333cb3c9` | The source's digests of this release's files |
| `n146-native-replay.json` | `511cc5d5b101dc0650d45e210ebc59f4659f6285` | 3246 | `cae9ee7d80b9e9f49db8b71e0dbe20bd4148a71622109cb5aafe7ac11edc13a5` | The author's receipt of this repository's two checkers at `074ac28` |
| `n146-squares-project.zip` | `a027dff73668f2ceaa32dfb558a430251e0b682f` | 399603 | `8a900e2887983e81bd95ee1cbee675c6ae4b9e0edf71b251d6be9ee2277fd742` | The complete package, below |
| `n146-verification.json` | `f7b4771d0a9e6a5b98808d57f95c82ae65ed2fa0` | 1927 | `a346ee7d431d0c16de78d66c51cdcc8b3948b15ecf070861d81851f430e4863a` | The author's receipt of its own exact checks |

The certificate digest the issue states is the one above. `n146-SHA256SUMS` is the package's own digest list, byte-identical to the package's `SHA256SUMS`, and `n146-README.txt`, `n146-native-replay.json` and `n146-verification.json` are byte-identical to members of the package.

## What the Package Holds

`n146-squares-project.zip` unpacks to `n146/`, 59 files, 1,759,160 bytes.
Its `SHA256SUMS` lists a digest for each of the other 58, and every one equals the digest of the bytes unpacked here.
Byte for byte, `n146/README.txt` is `n146-README.txt`, `n146/SHA256SUMS` is `n146-SHA256SUMS`, `n146/native/native-replay.json` is `n146-native-replay.json`, `n146/verification.json` is `n146-verification.json`, `n146/n146.cert.json` is `n146.cert.json`, `n146/pingyou-n146-rational.yaml` is `pingyou-n146-rational.yaml`.
It holds 21 Python programs, `VERIFY.py` among them; they were read for what they claim and not run.
Among the rest are the method, the inherited contact system with its 663 declared incidences and the solver states (`construction/`), Evan Daniel's contact solver with its MIT licence, the prior witnesses, the author's two exact checkers, and the sources and licence of this repository's two checkers at `074ac28`.
Nothing in it is retained.

## The Certificate

`n146.cert.json` holds `n`, `s_exact`, 146 `[x, y, t]` rows of rational strings and a `provenance` object, read with the `pingyou-json` adapter, which reads `provenance` without believing it. The side is a fraction with a 90-digit denominator; the issue prints it rounded up at 40 places, and it rounds up there to that print. `pingyou-n146-rational.yaml` states the same squares as rational corners, read with `witness-corners`.

As the source states it, a high-precision coupled realization of the inherited square-corner, square-side and wall contacts produced the rational packing directly, valid without a common dilation repair.

## Against the Record

At `main` `aeef99ef0` the case record's reported and verified ceilings at 146 are both T-150's (ry-xu, improved by Robert Barnett; `E-barnett-505-exact-feasibility`), side 12.5837822039510463 rounded up, its exact fraction in the claim record. The certificate is below it by $2.12 \times 10^{-13}$ (exactly; the fraction is in the claim record).

| Report | Holders | Side | Relation | Distance |
| --- | --- | --- | --- | --- |
| T-101 (#375) | the Kingbird catalogue, verified by Evan Daniel's exact ceiling | 12.6009077785130183 (retained, shown rounded up) | below | 0.0171 |
| T-125 (#432) | ry-xu | 12.5837822775125837822775 (retained, exact) | below | 7.36e-8 |
| T-146 (no issue) | Evan Daniel | 12.5837822774150769 (retained, shown rounded up) | below | 7.35e-8 |
| #593 | Mishapolk (Mykhailo Polkovskyi) | 12.5837822039510456 (printed, rounding unstated) | below | 2.11e-13 |
| PR #574 | PingYou Ltd | 12.58378220395083429191346793705115136677288617306781128303885385076117 (printed, rounding unstated) | undecided | 4.54e-69 |

A relation is this certificate's against the other side: *below* means this side is smaller. No report is decidably smallest: the prints do not order this certificate and PR #574.

Measured square for square against T-150's certificate, in order, it is the same packing: 127 squares moved by less than $10^{-9}$ and 19 by more, none by more than $1.61 \times 10^{-6}$, and nine turned, none by more than $9.1 \times 10^{-5}$ degrees. The issue compares the side with its own earlier certificate; against T-150 it is $2.12 \times 10^{-13}$ smaller. Only the author's own PR #574 states a smaller side (below), by margins its prints do not resolve.
[acquisition/claims.json](acquisition/claims.json) freezes these comparisons, and `devtools.upper_bound_reports` rebuilds them from the retained packets.

## Derived Fact and Exact Replay

`devtools.upper_bound_reports derive` read `n146.cert.json` from a checkout at the pin, after `devtools.acquire_source` showed that the checkout yields this packet's acquisition record and manifest, so the bytes it read have the digests above.
It admitted the certificate at the 40-place decimal the issue prints, to which its exact side rounds up.
It then read `pingyou-n146-rational.yaml` from the same checkout, as the row's `same_packing` file: all 146 poses and the side are the certificate's exactly.
It wrote the certificate as an exact rational `center-basis` Witness/v2, [facts/n-146.yaml.gz](facts/n-146.yaml.gz), naming the certificate's SHA-256 as `revision_sha256`. The fact is this repository's derivation; offline it must rebuild itself from the certificate it states, and `derive --check` with a checkout compares the fact and the witness again.
The declaration of the import is [acquisition/report.json](acquisition/report.json).

Only the fact enters geometry decisions, through the two-route kernel of `devtools.evand_arrangement_reports`: `sqpack`'s exact witness verifier and the independent rational corner checker, each deciding every wall and every pair over $\mathbb{Q}$.
A positive job, a duplicate-square control and an outside-container control each ran in its own child process, one worker at a time. The positive passes both routes and both routes refuse both controls. Both routes find the same margins: the least wall clearance exactly `1/200000000000000000000000000000000000000000000000000000000000000000000000000000000` and the least pair gap a rational of 487 characters, whose denominator has 283 digits, about $1.00 \times 10^{-80}$.
The three jobs made 63,510 pair decisions in 32.7 route CPU seconds and 48.92 job wall seconds, summed; the longest took 16.69 seconds, and `certify` 52 seconds of wall time, with other lanes on the machine.
A fresh `check --replay` decided all three jobs again, equal to the retained rows apart from timing, in 48 seconds.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every deciding input and both routes' complete outputs.
The two routes share certificate parsing, the half-angle conversion, Python's rational arithmetic and the separating-axis method.

The release reports that `packing-witness verify` and `devtools.check_rational_witness_independent`, unchanged at `074ac28`, accept its own witness file; `n146-native-replay.json` is that receipt. The two maintained routes here decided the certificate from the derived fact; the source's witness file was compared with the certificate pose for pose and not decided separately.

## What Is Not Established

The source reports that its exact separating-axis and polygon checkers accept all 10,585 pairs and every wall, and documents the coupled solve by its saved states and an audit. Those are author reports.
`VERIFY.py`, the package's checkers, its construction replay, `convert_witness.py` and `replay_upstream.py` were read here and not run: the two maintained routes decide the certificate from its own poses, so none is needed for the bound.
The replay above has not been reviewed.
The certificate establishes a finite upper bound only; the source claims no local or global optimality.

## Later Claims by the Same Author

The author has since submitted further certificates at this count, outside this packet's scope. [PR #574](https://github.com/jlevy/squares/pull/574) (opened 2026-10-13T00:13Z from `BuddenPing/squares`, head `4c319c2`, open and unmerged) requests 148 certificate refinements, and the GitHub releases at the tags `data/pingyou-numerical-refinements-2026-10-13-v1` and `-v2`, `data/pingyou-exact-153-302-2026-10-13(-v1)` and `data/pingyou-algebraic-refinements-2026-10-13-v1`, all on the head, carry them as assets that are not in the Git tree. At 146 it states a rational certificate (v2) whose pre-batch comparison is this release's `n146.cert.json`, by digest, $1.26 \times 10^{-79}$ below it, and in the supplement a rational certificate a further $6.53 \times 10^{-95}$ below; both print 12.5837822039508342919134679370511513667729 at 40 places. Read from the PR's `claims.json` files at its head, as data; neither the PR nor the release assets were retained or replayed here, and they are an import of their own.

## Credit

The source credits PingYou Ltd with this further refinement, Ryan Xu with the original layout, Robert Barnett with the preceding refinement and its source certificate ([#505](https://github.com/jlevy/squares/issues/505), T-150), and Evan Daniel with the contact solver, source custody and the earlier n146 regularization.

Neither the pinned source nor the issue makes a statement about AI assistance. Asked on #503 which account of AI assistance stands, the author answered on 12 October 2026 for the n207 and n153 releases ([comment](https://github.com/jlevy/squares/issues/503#issuecomment-6129716138)): “Both solutions were AI assisted by ‘PY’, an unreleased agentic AI offering by PingYou Ltd.” That answer names those two solutions only. The certificate's `provenance` field and the package's construction records name machine-local paths under a directory named `ChatGPT`; they are file paths, not a statement about assistance, and this packet draws nothing from them.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source pingyou-n146-refinement-2026-10-12 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-n146-refinement-2026-10-12 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-n146-refinement-2026-10-12 check --replay
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-n146-refinement-2026-10-12 derive --checkout CHECKOUT --check
```

`--check` re-derives the record from this packet alone.
The importer's `check-claims` and `check --replay` run offline from the fact;
`derive --check` needs a checkout at the pin, refuses one that does not yield this
packet's record and manifest, and compares the fact and the source's witness with the
certificate.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `facts/n-146.yaml.gz` | receipt | `92fdd67b93982c452a220dec8c2204572873219b` | `f5a9b7bf519e398afc77e612fd8a1878f6a1626a60b84da5abea44d579f14225` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
