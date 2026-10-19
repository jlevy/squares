# PingYou Ltd: A Further Refinement at 261

[Issue #567](https://github.com/jlevy/squares/issues/567) (BuddenPing, opened 2026-10-12T22:40Z; title and body replaced at 23:45Z, with a comment saying so) reports a further refinement of Robert Barnett's refinement (T-150) of Ryan Xu's packing of 261 in [BuddenPing/square-packing-certificates](https://github.com/BuddenPing/square-packing-certificates/tree/e70342d149f9363b32ef6043ecfa8d0e0c4b51aa) at `e70342d149f9363b32ef6043ecfa8d0e0c4b51aa` (tree `a0f46cf386775680fedcda2beaa1f0afda8e5115`, committed 2026-10-12T23:44:55Z, parent `820b9ff`), the revision the updated issue names. The issue's first version cited `8f96ceb`, whose certificate this one replaces, about $2.02 \times 10^{-13}$ larger; it is not retained.
The source was retrieved at 2026-10-14T04:47Z, when its branch head was `318ab94e821ba7280a68fa8ce2942c9ecdbda41d`; every file of this packet's scope has the same blob there.

| n | Exact side of the certificate | Rounded up at 16 places |
| --- | --- | --- |
| 261 | exact, with a 913-digit denominator | 16.6787798753429099 |

## Who the Source Is

As for the [n207](../pingyou-n207-certificate-2026-10-11/README.md#who-the-source-is) and [n153](../pingyou-n153-certificate-2026-10-11/README.md) packets of 11 October: the repository describes itself as “Exact square-packing certificates and reproducible verification from PingYou Ltd”, its README is headed “Square-packing certificates — PingYou Ltd”, and every commit is authored as `BuddenPing` from an address at the `pingyou.com` domain. GitHub detects no licence and the account names no person or company. The source names no individual author, and this packet names none.
At retrieval `main` held sixteen commits, the head `318ab94` (2026-10-12T23:46:52Z), and five tags `data/pingyou-*`, all at the head, each a GitHub release whose assets carry later certificates (below, [Later Claims by the Same Author](#later-claims-by-the-same-author)).

## Source Custody

The tree has no licence file, and GitHub detects none.
The release READMEs say that upstream software and schema licences are retained beside the files they cover and that no new licence is asserted for third-party material; nothing grants one for the source's own files.
Under the derived-only form of the [existing retention policy](../known-best-packings/README.md), as for the 11 October PingYou packets, this packet keeps no upstream byte. No redistribution permission or licence determination is asserted.

`devtools.acquire_source` wrote the packet from a clone checked out at the pin, from the declaration in [acquisition/declaration.json](acquisition/declaration.json).
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and [acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest.
The scope is the seven n261 paths the pinned commit changed, first published by `8f96ceb`. The tree's `README.md` and `SHA256SUMS` index them only from the head, outside the scope.
All seven are pinned only; the declared `source/` directory is empty by design.

| Upstream path | Git blob | Bytes | SHA-256 | What it is |
| --- | --- | --- | --- | --- |
| `n261.cert.json` | `16e12071bb001a522773f00d5dec3323ea2bca8d` | 1076936 | `f850cb35c31e018d5f6fdde90940f3d55ad36ecdb88341b805af47639c7e16c2` | The certificate |
| `pingyou-n261-rational.yaml` | `9d4a5f0f2b9e9180a90badf8b3412e5d9205bc4e` | 4842525 | `211ce191271e4815c80b0efcb83b141f5e7b1593db1274927ec1b34bb06d83e7` | The same packing as a corners Witness/v2 |
| `n261-README.txt` | `a9dff42645eaa936b9290fa849ae51afa2811e53` | 3634 | `6b2aa9dfe12fc1d83dba25ae0279a9212721ad3dc0c34df9ea9b9b4c94d857f7` | Author prose: claim, method, credit, replay |
| `n261-SHA256SUMS` | `07a999f8b7067fc75adb26fc7045d41976859a26` | 12420 | `9841ca1f34d5ce614e9d05d0ade0c18d7b931f9725ca9a5a0b4b843f09dd6fee` | The source's digests of this release's files |
| `n261-native-replay.json` | `7821c44e1504d7c468bf30d60483582d31704729` | 5403 | `14707c852e14af81b27a1e66d1757576ca7544397d3d6cfcacdea0bc9b19d6e5` | The author's receipt of this repository's two checkers at `074ac28` |
| `n261-squares-project.zip` | `3641097d0559048ccfdb45c2a17c19e90ff70c49` | 3238321 | `d340c92e6e5b108e57982b1dda6872812ddedcc100655d814e342e4780589165` | The complete package, below |
| `n261-verification.json` | `d1853daa149852992cf2ad1672b07537fc23df51` | 9283 | `23358072906b7edf6b42168b44788679b40a16ef88a34a87bbccafd7ac979d69` | The author's receipt of its own exact checks |

The certificate digest the issue states is the one above. `n261-SHA256SUMS` is the package's own digest list, byte-identical to the package's `SHA256SUMS`, and `n261-README.txt`, `n261-native-replay.json` and `n261-verification.json` are byte-identical to members of the package.

## What the Package Holds

`n261-squares-project.zip` unpacks to `n261/`, 109 files, 12,531,766 bytes.
Its `SHA256SUMS` lists a digest for each of the other 108, and every one equals the digest of the bytes unpacked here.
Byte for byte, `n261/README.txt` is `n261-README.txt`, `n261/SHA256SUMS` is `n261-SHA256SUMS`, `n261/native/native-replay.json` is `n261-native-replay.json`, `n261/verification.json` is `n261-verification.json`, `n261/n261.cert.json` is `n261.cert.json`, `n261/pingyou-n261-rational.yaml` is `pingyou-n261-rational.yaml`.
It holds 22 Python programs, `VERIFY.py` among them; they were read for what they claim and not run.
Among the rest are the method, the inherited contact system, the fixed-frame separation word with its 34,974 support rows encoded from the source and marks, the solver states, Evan Daniel's contact solver with its MIT licence, the prior witnesses, the author's two exact checkers, and the sources and licence of this repository's two checkers at `074ac28`.
Nothing in it is retained.

## The Certificate

`n261.cert.json` holds `n`, `s_exact`, 261 `[x, y, t]` rows of rational strings and a `provenance` object, read with the `pingyou-json` adapter. It is the largest certificate this importer has read: 1,076,936 bytes, a side whose denominator has 913 digits and row literals up to 2,141 characters; its witness is 4,842,525 bytes with corner literals up to 2,522 characters. The importer's file and literal ceilings, 1,000,000 bytes and 1,024 characters before this import, were raised to 6,000,000 bytes and 4,096 characters to read them, and the kernel's receipt check now admits diagnostics of up to 4,096 characters, since the replay's outside-container control states a wall clearance of 2,205. The issue prints the side rounded up at 40 places, and it rounds up there to that print. It says boundary contacts are permitted, and the certificate has them (below).

As the source states it, a coupled-contact realization was made feasible by an exact common centre and host separation repair; a final centre refinement kept every owner and frame of that intermediate witness within the complete fixed-frame support-inequality system, each centre coordinate and the side moved by at most $10^{-6}$ before an exact rational repair and crop. The bound includes both repairs.

## Against the Record

At `main` `aeef99ef0` the case record's reported and verified ceilings at 261 are both T-150's (ry-xu, improved by Robert Barnett; `E-barnett-505-exact-feasibility`), side 16.6787798753432078 rounded up, its exact fraction in the claim record. The certificate is below it by $2.98 \times 10^{-13}$ (exactly; the fraction is in the claim record).

| Report | Holders | Side | Relation | Distance |
| --- | --- | --- | --- | --- |
| T-101 (#375) | the Kingbird catalogue, verified by Evan Daniel's exact ceiling | 16.6829268292682927 (retained, shown rounded up) | below | 0.00415 |
| T-125 (#432) | ry-xu | 16.6787798754166787798754 (retained, exact) | below | 7.38e-11 |
| #593 | Mishapolk (Mykhailo Polkovskyi) | 16.6787798753432064 (printed, rounding unstated) | below | 2.97e-13 |
| PR #574 | PingYou Ltd | 16.67877987534290981493522894955687214451016932272043904390384940483363 (printed, rounding unstated) | above | 1.99e-21 |

A relation is this certificate's against the other side: *below* means this side is smaller. The smallest report at the count is PR #574.

Measured square for square against T-150's certificate, in order, it is the same packing: 38 squares moved by less than $10^{-9}$ and 223 by more, none by more than $1.42 \times 10^{-6}$, and 62 turned, none by more than $1.2 \times 10^{-6}$ degrees. Against T-150 the side is $2.98 \times 10^{-13}$ smaller. Only the author's own PR #574 states a smaller side (below).
[acquisition/claims.json](acquisition/claims.json) freezes these comparisons, and `devtools.upper_bound_reports` rebuilds them from the retained packets.

## Derived Fact and Exact Replay

`devtools.upper_bound_reports derive` read `n261.cert.json` from a checkout at the pin, after `devtools.acquire_source` showed that the checkout yields this packet's acquisition record and manifest, so the bytes it read have the digests above.
It admitted the certificate at the 40-place decimal the issue prints, to which its exact side rounds up.
It then read `pingyou-n261-rational.yaml` from the same checkout, as the row's `same_packing` file: all 261 poses and the side are the certificate's exactly.
It wrote the certificate as an exact rational `center-basis` Witness/v2, [facts/n-261.yaml.gz](facts/n-261.yaml.gz), naming the certificate's SHA-256 as `revision_sha256`. The fact is this repository's derivation; offline it must rebuild itself from the certificate it states, and `derive --check` with a checkout compares the fact and the witness again.
The declaration of the import is [acquisition/report.json](acquisition/report.json).

Only the fact enters geometry decisions, through the two-route kernel of `devtools.evand_arrangement_reports`: `sqpack`'s exact witness verifier and the independent rational corner checker, each deciding every wall and every pair over $\mathbb{Q}$.
A positive job, a duplicate-square control and an outside-container control each ran in its own process, one at a time, as `decide-job`, the command `certify` runs for each job, but without the driver's 600-second deadline, which the positive was priced to exceed on this shared machine; `certify --finished` then assembled and admitted the receipt from the three outputs, as it admits any, as the [Couzo packet of 11 October](../couzo-certificates-2026-10-11/README.md) did for its last three jobs. The positive passes both routes and both routes refuse both controls. Both routes find the least wall clearance and the least pair gap exactly `0`: some square touches the wall and some pair of squares touch. These are exact contacts, which the source says it permits; each route admits them, since each decides containment in the closed box and disjoint interiors.
The three jobs made 203,580 pair decisions in 1391.79 route CPU seconds and 2068.46 job wall seconds, summed; the longest took 930.66 seconds, and the three `decide-job` runs 933, 544, 597 seconds of wall time, with other lanes on the machine.
A fresh `check --replay` decided all three jobs again, equal to the retained rows apart from timing, in 1832 seconds.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every deciding input and both routes' complete outputs.
The two routes share certificate parsing, the half-angle conversion, Python's rational arithmetic and the separating-axis method.

The release reports that `packing-witness verify` and `devtools.check_rational_witness_independent`, unchanged at `074ac28`, accept its own witness file; `n261-native-replay.json` is that receipt. The two maintained routes here decided the certificate from the derived fact; the source's witness file was compared with the certificate pose for pose and not decided separately.

## What Is Not Established

The source reports that its exact separating-axis and polygon checkers accept all 33,930 pairs and every wall and that every declared support inequality holds. Those are author reports.
`VERIFY.py`, the package's checkers, its construction replay, `convert_witness.py` and `replay_upstream.py` were read here and not run: the two maintained routes decide the certificate from its own poses, so none is needed for the bound.
The replay above has not been reviewed.
The certificate establishes a finite upper bound only; the source claims no local or global optimality.

## Later Claims by the Same Author

The author has since submitted further certificates at this count, outside this packet's scope. [PR #574](https://github.com/jlevy/squares/pull/574) (opened 2026-10-13T00:13Z from `BuddenPing/squares`, head `4c319c2`, open and unmerged) requests 148 certificate refinements, and the GitHub releases at the tags `data/pingyou-numerical-refinements-2026-10-13-v1` and `-v2`, `data/pingyou-exact-153-302-2026-10-13(-v1)` and `data/pingyou-algebraic-refinements-2026-10-13-v1`, all on the head, carry them as assets that are not in the Git tree. At 261 only the supplement states a certificate (v2 omits 261 as already public): a rational one whose predecessor is this release's `n261.cert.json`, by digest, $1.99 \times 10^{-21}$ below it, about 16.678779875342909814935228949556872… Read from the PR's `claims.json` files at its head, as data; neither the PR nor the release assets were retained or replayed here, and they are an import of their own.

## Credit

The source credits PingYou Ltd with this further refinement, Ryan Xu with the original layout, Robert Barnett with the preceding refinement and its source certificate ([#505](https://github.com/jlevy/squares/issues/505), T-150), and Evan Daniel with the contact solver and source custody.

Neither the pinned source nor the issue makes a statement about AI assistance. Asked on #503 which account of AI assistance stands, the author answered on 12 October 2026 for the n207 and n153 releases ([comment](https://github.com/jlevy/squares/issues/503#issuecomment-6129716138)): “Both solutions were AI assisted by ‘PY’, an unreleased agentic AI offering by PingYou Ltd.” That answer names those two solutions only. The certificate's `provenance` field and the package's construction records name machine-local paths under a directory named `ChatGPT`; they are file paths, not a statement about assistance, and this packet draws nothing from them.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source pingyou-n261-refinement-2026-10-12 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-n261-refinement-2026-10-12 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-n261-refinement-2026-10-12 check --replay
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-n261-refinement-2026-10-12 derive --checkout CHECKOUT --check
```

`--check` re-derives the record from this packet alone.
The importer's `check-claims` and `check --replay` run offline from the fact;
`derive --check` needs a checkout at the pin, refuses one that does not yield this
packet's record and manifest, and compares the fact and the source's witness with the
certificate.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `facts/n-261.yaml.gz` | receipt | `105809762d43b908fe54479b469c584f4b249ba5` | `3c223da8fcd47b13440bf5568718d7b434a73c8f8f57e4d0153b30d86ff4ddc2` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
