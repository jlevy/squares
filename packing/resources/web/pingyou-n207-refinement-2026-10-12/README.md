# PingYou Ltd: A Refined Certificate for 207 Squares

A [comment on issue #503](https://github.com/jlevy/squares/issues/503#issuecomment-6133755143) (BuddenPing, 2026-10-12T22:25Z), and the dated update the author placed at the top of the issue's body, report a refined certificate of the n207 assembly T-147 registers and ask that T-147 be re-verified and updated. It is in [BuddenPing/square-packing-certificates](https://github.com/BuddenPing/square-packing-certificates/tree/10418630bfb00853a539ad7ad9908b2d746147c0) at `10418630bfb00853a539ad7ad9908b2d746147c0` (tree `7920d484d01e833b87ace499dcf1881e2a5aab28`, committed 2026-10-12T22:24:32Z, parent `431186b`), the revision the comment names. T-147's certificate, at `9dc93b6`, is retained by [the 11 October packet](../pingyou-n207-certificate-2026-10-11/README.md).
The source was retrieved at 2026-10-14T04:47Z, when its branch head was `318ab94e821ba7280a68fa8ce2942c9ecdbda41d`; every file of this packet's scope has the same blob there.

| n | Exact side of the certificate | Rounded up at 16 places |
| --- | --- | --- |
| 207 | `3720240092889639048018577779/250000000000000000000000000` | 14.8809603715585562 |

## Who the Source Is

As for the [n207](../pingyou-n207-certificate-2026-10-11/README.md#who-the-source-is) and [n153](../pingyou-n153-certificate-2026-10-11/README.md) packets of 11 October: the repository describes itself as “Exact square-packing certificates and reproducible verification from PingYou Ltd”, its README is headed “Square-packing certificates — PingYou Ltd”, and every commit is authored as `BuddenPing` from an address at the `pingyou.com` domain. GitHub detects no licence and the account names no person or company. The source names no individual author, and this packet names none.
At retrieval `main` held sixteen commits, the head `318ab94` (2026-10-12T23:46:52Z), and five tags `data/pingyou-*`, all at the head, each a GitHub release whose assets carry later certificates (below, [Later Claims by the Same Author](#later-claims-by-the-same-author)).

## Source Custody

The tree has no licence file, and GitHub detects none.
The release READMEs say that upstream software and schema licences are retained beside the files they cover and that no new licence is asserted for third-party material; nothing grants one for the source's own files.
Under the derived-only form of the [existing retention policy](../known-best-packings/README.md), as for the 11 October PingYou packets, this packet keeps no upstream byte. No redistribution permission or licence determination is asserted.

`devtools.acquire_source` wrote the packet from a clone checked out at the pin, from the declaration in [acquisition/declaration.json](acquisition/declaration.json).
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and [acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest.
The scope is the eight paths the pinned commit changed: the package `01-squares-project.zip` and the n207 certificate, witness, figure and drawing, first published by `0d8b9c1` and `9dc93b6`, the new `n207-SHA256SUMS`, and `README.md` and `SHA256SUMS`.
All eight are pinned only; the declared `source/` directory is empty by design.

| Upstream path | Git blob | Bytes | SHA-256 | What it is |
| --- | --- | --- | --- | --- |
| `n207.cert.json` | `598a99863ff38f7b8800792c460144f9378ef7e3` | 28616 | `94dc19ce0ab4e8c35de7a4a542ff2b46d0dafe717bb84ebf6d3fcd351a212a5c` | The certificate |
| `pingyou-n207-rational.yaml` | `09786bdf7d07935cedafad6bba483f988d866475` | 150908 | `7a683bfc118080e9eb8922549130a64f84caa402d565a5fdd5e0a2cd22819497` | The same packing as a corners Witness/v2 |
| `01-squares-project.zip` | `02520bdffe74ddbfc90be8cf28ce83df2be5a11c` | 261995 | `915a82aeffc5c6e79d836e14ab9e890138feead877733f43c33418b51da922c2` | The complete package, below |
| `README.md` | `0c81fed8e4932fd0e7c348acfe38f2c2f18d6d46` | 9837 | `0ac83648e8c489012078d134f9002a2191da4cd5aee2fbbe8da1098ff28e337d` | Author prose for every release in the tree |
| `SHA256SUMS` | `09aa3204a0f029c6e7354526e81424f64ee751f2` | 1625 | `857bf68ca9b8d86bdf199cefe4017cc256ce8fe7a82d5aaa67dce3b69f7a5646` | The source's digests of the tree's release files |
| `n207-SHA256SUMS` | `b88f16f8cfa73f4e506eb27f79f13ee945a67873` | 433 | `dd25965e75f4fa97742651dc1dcf9c8b4a726e0299ef2c2a21d0792f88884482` | The source's digests of this release's files |
| `n207-verified-comparison.pdf` | `f5bc5f7ce0f6ca7e9e6f9e8dae0af4aed4d87ee2` | 135040 | `6ca2959fc59abe8aa9b0b29d8a16697ea3a4441ec06ab3884743ac37c5240de3` | Comparison figure |
| `n207.svg` | `91f4fbdafc258c16f25ece4f076e745f560d657f` | 37794 | `9bc07f755e197ba538af274ec6cc0f48e577ad6a7c233886e7480b62bd3f6f8f` | Drawing |

The three digests the issue's update states, for the package, the certificate and the witness, are the ones above, and `n207-SHA256SUMS` lists the same digest for each of the five n207 artifacts it names.

## What the Package Holds

`01-squares-project.zip` unpacks to `01-squares-project/`, 49 files, 746,917 bytes.
Its `SHA256SUMS` lists a digest for each of the other 48, and every one equals the digest of the bytes unpacked here.
Byte for byte, `01-squares-project/evidence/n207-verified-comparison.pdf` is `n207-verified-comparison.pdf`, `01-squares-project/evidence/packing.cert.json` is `n207.cert.json`, `01-squares-project/evidence/n207.svg` is `n207.svg`, `01-squares-project/native/pingyou-n207-rational.yaml` is `pingyou-n207-rational.yaml`.
It holds 17 Python programs, `VERIFY.py` among them; they were read for what they claim and not run.
Among the rest are the construction table and its replay, the n70 parent, the author's polygon-projection checker and Evan Daniel's unchanged checkers, receipts, and the sources and licence of this repository's two checkers at `074ac28`.
Nothing in it is retained.

## The Certificate

`n207.cert.json` has the shape of the 11 October certificate without its metadata: `n`, `s_exact` and 207 `[x, y, t]` rows of rational strings, read with the `pingyou-json` adapter; `pingyou-n207-rational.yaml` states the same squares as rational corners, read with `witness-corners`.

As the source states it, the inherited-frame prescription and the whole-owner assembly are retained; the certificate uses a new rational approximation to the frame and reduces the centre and container guard from $10000000001/10000000000$ to $5000000000001/5000000000000$. It is not an angle search.

## Against the Record

At `main` `aeef99ef0` the case record's reported and verified ceilings at 207 are both T-147's (PingYou Ltd; `E-pingyou-503-exact-feasibility`), side `148809603730436756319360591381170501178639/10000000000000000000000000000000000000000`. The certificate is below it by `14851194398617480221170501178639/10000000000000000000000000000000000000000`, about $1.49 \times 10^{-9}$.

| Report | Holders | Side | Relation | Distance |
| --- | --- | --- | --- | --- |
| T-098 (#375) | Francisco Couzo, improved by Evan Daniel | 14.8939546342372274 (retained, shown rounded up) | below | 0.013 |
| T-116 (#422) | Nate Chaoweeraprasit | 14.8879922583077482 (retained, shown rounded up) | below | 0.00703 |
| T-127 (#438) | Nate Chaoweeraprasit (itsnaka), improved by Siddharth Gupta | 14.8879922583026574 (retained, shown rounded up) | below | 0.00703 |
| T-136 (#481) | Nate Chaoweeraprasit | 14.8855063088416777 (retained, shown rounded up) | below | 0.00455 |
| #573 | Mishapolk | 14.880960371558 (printed, rounded up) | above | 5.56e-13 |
| #593 | Mishapolk (Mykhailo Polkovskyi) | 14.8809603715580003 (printed, rounding unstated) | above | 5.56e-13 |
| PR #574 | PingYou Ltd | 14.88096037155557959469669157492336415899451456818029930847400016655138 (printed, rounding unstated) | above | 2.98e-12 |

A relation is this certificate's against the other side: *below* means this side is smaller. The smallest report at the count is PR #574.

Measured square for square against T-147's certificate, in order, it is the same assembly: 68 squares moved by less than $10^{-9}$ and 139 by more, none by more than 0.0757, and no square turned by more than $2.7 \times 10^{-13}$ degrees. The side is smaller by exactly the `14851194398617480221170501178639/10000000000000000000000000000000000000000` the comment states. Mishapolk's #573 and #593 print smaller sides, from a new arrangement by their account, and the author's own PR #574 states smaller ones still (below). T-056 has no packet reader here, and `devtools.check_standing` at `main` marks it superseded.
[acquisition/claims.json](acquisition/claims.json) freezes these comparisons, and `devtools.upper_bound_reports` rebuilds them from the retained packets.

## Derived Fact and Exact Replay

`devtools.upper_bound_reports derive` read `n207.cert.json` from a checkout at the pin, after `devtools.acquire_source` showed that the checkout yields this packet's acquisition record and manifest, so the bytes it read have the digests above.
It admitted the certificate at the exact fraction the comment prints.
It then read `pingyou-n207-rational.yaml` from the same checkout, as the row's `same_packing` file: all 207 poses and the side are the certificate's exactly.
It wrote the certificate as an exact rational `center-basis` Witness/v2, [facts/n-207.yaml.gz](facts/n-207.yaml.gz), naming the certificate's SHA-256 as `revision_sha256`. The fact is this repository's derivation; offline it must rebuild itself from the certificate it states, and `derive --check` with a checkout compares the fact and the witness again.
The declaration of the import is [acquisition/report.json](acquisition/report.json).

Only the fact enters geometry decisions, through the two-route kernel of `devtools.evand_arrangement_reports`: `sqpack`'s exact witness verifier and the independent rational corner checker, each deciding every wall and every pair over $\mathbb{Q}$.
A positive job, a duplicate-square control and an outside-container control each ran in its own child process, one worker at a time. The positive passes both routes and both routes refuse both controls. Both routes find the same margins: the least wall clearance exactly `1/10000000000000` and the least pair gap `16858318585131418176527842273953121313111/88901712681142539078557480500000000000000000000000000`, about $1.90 \times 10^{-13}$.
The three jobs made 127,926 pair decisions in 21.96 route CPU seconds and 40.17 job wall seconds, summed; the longest took 15.77 seconds, and `certify` 45 seconds of wall time, with other lanes on the machine.
A fresh `check --replay` decided all three jobs again, equal to the retained rows apart from timing, in 38 seconds.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every deciding input and both routes' complete outputs.
The two routes share certificate parsing, the half-angle conversion, Python's rational arithmetic and the separating-axis method.

The release reports that `packing-witness verify` and `devtools.check_rational_witness_independent`, unchanged at `074ac28`, accept its own witness file; `01-squares-project/native/native-replay.json` is that receipt. The two maintained routes here decided the certificate from the derived fact; the source's witness file was compared with the certificate pose for pose and not decided separately.

## What Is Not Established

The source reports that its three exact checkers accept all 21,321 pairs and every wall and that its replay rebuilds the certificate and the owner lineage from the construction table. Those are author reports.
`VERIFY.py`, the package's checkers, its construction replay, `convert_witness.py` and `replay_upstream.py` were read here and not run: the two maintained routes decide the certificate from its own poses, so none is needed for the bound.
The replay above has not been reviewed.
The certificate establishes a finite upper bound only; the source claims no local or global optimality.

## Later Claims by the Same Author

The author has since submitted further certificates at this count, outside this packet's scope. [PR #574](https://github.com/jlevy/squares/pull/574) (opened 2026-10-13T00:13Z from `BuddenPing/squares`, head `4c319c2`, open and unmerged) requests 148 certificate refinements, and the GitHub releases at the tags `data/pingyou-numerical-refinements-2026-10-13-v1` and `-v2`, `data/pingyou-exact-153-302-2026-10-13(-v1)` and `data/pingyou-algebraic-refinements-2026-10-13-v1`, all on the head, carry them as assets that are not in the Git tree. At 207 it states a rational certificate, about 14.880960371555581469373…, $2.97 \times 10^{-12}$ below this one, and an algebraic certificate of degree five over $t^5 - 14t^4 + 6t^3 + 4t^2 - 7t + 2$, about 14.8809603715555795946966915749…, a further $1.87 \times 10^{-15}$ below. Read from the PR's `claims.json` files at its head, as data; neither the PR nor the release assets were retained or replayed here, and they are an import of their own.

## Credit

The source credits PingYou Ltd with the assembly and its refinement, Ryan Xu with the n70 construction its patches come from ([#432](https://github.com/jlevy/squares/issues/432)), Evan Daniel with the exact retention of that construction and with exact checking tools, and SQUISH's n207 ([#481](https://github.com/jlevy/squares/issues/481)) only as the earlier comparison.

The pinned source makes no statement about AI assistance, and neither does the comment. Asked on #503 which account of AI assistance stands, the author answered on 12 October 2026 for the n207 and n153 releases ([comment](https://github.com/jlevy/squares/issues/503#issuecomment-6129716138)): “Both solutions were AI assisted by ‘PY’, an unreleased agentic AI offering by PingYou Ltd.” The refinement states nothing further.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source pingyou-n207-refinement-2026-10-12 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-n207-refinement-2026-10-12 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-n207-refinement-2026-10-12 check --replay
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-n207-refinement-2026-10-12 derive --checkout CHECKOUT --check
```

`--check` re-derives the record from this packet alone.
The importer's `check-claims` and `check --replay` run offline from the fact;
`derive --check` needs a checkout at the pin, refuses one that does not yield this
packet's record and manifest, and compares the fact and the source's witness with the
certificate.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `facts/n-207.yaml.gz` | receipt | `b0a20248962275b9dd1ee5eddffa4a282f87e4be` | `47e10366c1e2c1ab6511b0b596c806dbfc953f05e4e75ba14d1edf8b52b1f46c` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
