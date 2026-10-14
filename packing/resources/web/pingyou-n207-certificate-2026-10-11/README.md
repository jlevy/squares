# PingYou Ltd: An Exact Packing of 207 Squares

[Issue #503](https://github.com/jlevy/squares/issues/503) (BuddenPing,
2026-10-11T10:27Z) reports an exact rational certificate for 207 unit squares in
[BuddenPing/square-packing-certificates](https://github.com/BuddenPing/square-packing-certificates/tree/9dc93b6ac2f8fefe038062a74c9a75bf05afdba6)
at `9dc93b6ac2f8fefe038062a74c9a75bf05afdba6` (tree
`14d567766fef3053f29927f52274db33edeae533`, committed 2026-10-11T10:30:57Z, parent
`0d8b9c1bae55c47e774394bb3ef3fe9948f454e4`), the revision the issue names.
The source was retrieved at 2026-10-11T20:33Z, when its branch head was
`bc328a7d727aedd0eabebd6ea80285f572b65d2d`, the n153 release of
[issue #504](https://github.com/jlevy/squares/issues/504), which
[its own packet](../pingyou-n153-certificate-2026-10-11/README.md) retains.

| n | Exact side of the certificate | Rounded up at 16 places |
| --- | --- | --- |
| 207 | `148809603730436756319360591381170501178639/10000000000000000000000000000000000000000` | 14.8809603730436757 |

## Who the Source Is

The repository README is headed “Square-packing certificates — PingYou Ltd” and asks
that **PingYou Ltd** be credited with the n207 assembly; the repository description
reads “Exact square-packing certificates and reproducible verification from PingYou
Ltd.” The three commits are authored as `BuddenPing`, from an address at the
`pingyou.com` domain, and the GitHub account names no person or company.
The source names no individual author, and this packet names none.

The record already holds an undated abstract with the author line “PINGYOU LTD”,
received from the owner on 7 October
([packet](../pingyou-fibonacci-torus-2026-10-07/README.md), bead `think-aj43`). Nothing
in this release refers to that abstract, and the record does not link the two.

## Source Custody

The tree has no licence file, and GitHub detects none.
The README says that included upstream material keeps its own attribution and licence
terms and that the repository adds no new licence grant for third-party material; it
grants none for the source’s own files.
Under the derived-only form of the
[existing retention policy](../known-best-packings/README.md), as for the
[SQUISH](../squish-481-third-request-2026-10-09/README.md) and
[Deleeuw](../ebdeleeuw-n70-refinement-2026-10-10/README.md) packets, this packet keeps
no upstream byte. No redistribution permission or licence determination is asserted.

`devtools.acquire_source` wrote the packet from a clone checked out at the pin, from the
declaration in [acquisition/declaration.json](acquisition/declaration.json).
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest.
The scope is the whole tree at the pin, seven files, all pinned only; the declared
`source/` directory is empty by design.

| Upstream path | Git blob | Bytes | SHA-256 | What it is |
| --- | --- | --- | --- | --- |
| `n207.cert.json` | `6316a8e28a6d20d4103cf6acd1fb5f8a09cdea1a` | 44614 | `1c334f3170ece68cf2c2f16341660f7a80ef44bf7a9cdb083940d1b99756c071` | The certificate |
| `pingyou-n207-rational.yaml` | `c2a509d0457fc527c03eb595b47b63ef6d5c67e3` | 224645 | `09e6d0dff17ae71ae84bde1466b805a67f3b1592496f9ca438b02bde603f6182` | The same packing as a corners Witness/v2 |
| `01-squares-project.zip` | `13bc991eee5ac32411d0afcd612dcac5ae1918ff` | 146732 | `d3b6505292ce647903708c7e5d6f8476a686d360ebcc22547dbd3c20ebe96ed6` | The complete package, below |
| `README.md` | `49c480adfb4ce89e8c160a86d7d4e2f525a6f216` | 3276 | `4dd80c149763bfcf24cd7731fe07d6a32d1806d5361da92805d043226dda1a65` | Author prose |
| `SHA256SUMS` | `ce459d2b2c26f26d30026550e6479a6bb14b3772` | 509 | `584bcae2e0631ae2f3ba8bdc1986c54dc36dd42810de365089bba38a434cfb1f` | The source’s digests of the other six |
| `n207-verified-comparison.pdf` | `70661d6763ec21ecaae5caefdba1c6dbb6cf6472` | 20317 | `ae323e59850c8bad109358d00df487de51c7349989a6b25cbdf4b4e0518fa12e` | Two-page comparison |
| `n207.svg` | `cf3305b0c0fd9929968730740e0d7464b736aea2` | 45578 | `c56d600c749471b328e5bcbe391b9a383c1c3353c5f4557b4dcf98ee0dbf7a88` | Drawing |

The three digests the issue states, for the certificate, the witness and the package,
are the ones above, and `SHA256SUMS` lists the same digest for each of the other six
files.

### The Three Commits

The repository was created at 2026-10-11T10:25:46Z and has three commits on `main`:

- `0d8b9c1` (10:26:22Z) first published all seven files.
  The certificate, the witness, the PDF and the drawing have the same blobs there as at
  the pin, so the certificate was first committed at 10:26:22Z.
- `9dc93b6` (10:30:57Z), the pin, titled “Correct attribution in submission materials”,
  changed only `01-squares-project.zip`, `README.md` and `SHA256SUMS`. It removed the
  README’s sentence “Verification, comparison review and package preparation were
  assisted by OpenAI Codex.”
  Inside the package it removed the same statement from `ISSUE_BODY.txt` and changed
  “the same Codex-assisted workflow” there to “the same workflow”, and `manifest.json`
  changed with that file’s digest; the other 31 members are unchanged.
  The issue, opened at 10:27:00Z citing `0d8b9c1`, was edited at 10:31:52Z to cite the
  pin and to drop the same two passages.
- `bc328a7` (10:39:06Z) adds the n153 release and an n153 section to `README.md` and
  `SHA256SUMS`, and leaves the n207 files unchanged; the n153 packet retains it.

## What the Package Holds

`01-squares-project.zip` unpacks to `01-squares-project/`, 33 files.
Its `manifest.json` lists a SHA-256 for each of the other 32, and every one equals the
digest of the bytes unpacked here.
Nothing in it is retained; no program in it ran here.

| Member | Bytes | SHA-256 | What it is |
| --- | --- | --- | --- |
| `evidence/packing.cert.json` | 44614 | `1c334f3170ece68cf2c2f16341660f7a80ef44bf7a9cdb083940d1b99756c071` | The certificate, byte-identical to `n207.cert.json` |
| `native/pingyou-n207-rational.yaml` | 224645 | `09e6d0dff17ae71ae84bde1466b805a67f3b1592496f9ca438b02bde603f6182` | The witness, byte-identical to the top-level one |
| `evidence/parents/n070.cert.json` | 11399 | `d508ee05fd6b33b2ccd6cbd592d94a47f8458a46f5f580b0d63285b1535d7e8a` | The n70 source, below |
| `evidence/baselines/prior-n207.cert.json` | 76780 | `da36d750f0385d7f64567cb3fe0ffbdb41e94d936d506349c591d10e8d2ffb1b` | SQUISH’s #481 n207 certificate, byte-identical to the one the [SQUISH packet](../squish-481-third-request-2026-10-09/README.md) pins |
| `evidence/reproduce.py` | 3960 | `a2d24786505bbfb3dfa921bef759daeedff4ac3df5c303a8fa4aadc87ac0b5aa` | Rebuilds the 207 poses from the n70 source and runs the three checkers |
| `evidence/audit_all.py` | 2594 | `46ce27cd668642a83555321b56bac175ae1f863f88dc90ebff08acc1163605cf` | Centre and support-radius separating axes |
| `evidence/vertex_check.py` | 4914 | `0635bd472cb4f066a9bc060f018c57350d2d3dea2c127f286a3ec94b136b4028` | Vertex projections |
| `evidence/polygon_check.py` | 2118 | `85b881c132f6b0502fd1fe2eb5cfb0ba8949095c60f1ba8d3b142df737c1f0dd` | Rational polygon clipping |
| `VERIFY.py` | 3100 | `78aca3ed4f1658e50ad617dba1e9636648112e7dac6e68cb2c90ce6f4ad55671` | Checks the manifest, then runs the scripts above |
| `native/convert_witness.py` | 5986 | `0fc9573f8bcd8b6a13c18d2d620c07b5e932bdf334e727199b02bcb94466e0f0` | Writes or checks the witness from the certificate |
| `native/replay_upstream.py` | 1534 | `c98536a9efc28794dad04eec39a651b6a5192a7bfa8c98ddff9276de503579ab` | Imports this repository’s two exact checkers from a checkout |
| `evidence/reproduction_audit.json` | 3516 | `6e4f641510ddeb81cb164cbcfd95626289e1d09f6ace7a8cef1cf1c33c1b09f7` | Receipt of `reproduce.py` |
| `native/native-replay.json` | 1708 | `d1525e4a61e952b78d31bd9c7b69e18e884c7302b0f1ae57c7e527320f124c1d` | Receipt of the two checkers here, at `5b0eb012` |
| `native/conversion-check.json` | 585 | `0c405eb702492cb210f390ca9102903129afb74eb0a031c1a34cf09d55024ba4` | Receipt of the witness check |
| `native/conversion-creation.json` | 585 | `f105e8f1474bc6ad6b884eb7f83e8dd7f4c3d9bcc9882897b2975fc88f8aee34` | Receipt of the witness’s writing |
| `native-replay-source-manifest.json` | 1106 | `5a34895064b7bce64cbc608cd081d587d7a580e85b59c152e3f3a11c7df4fa93` | Digests of seven checker files here, at `5b0eb012` |
| `upstream-sources.json` | 2630 | `19bb5afa952a99ff4d49cbe9bd2e69cfc03267d99d45a8a9d5b977fe90ae81c2` | Digests of nine files here the author read, at `5b0eb012` |
| `native/witness.schema.yaml` | 9013 | `754ddd6eea0558344c174302318ed1e7235d9665f37ef4f6fdea1f1e627664dc` | This repository’s witness schema, byte-identical at `5b0eb012` |
| `UPSTREAM-LICENSE.txt` | 21153 | `7428341239cf4ee78c4b951b7fd8a2284b24835aeb0ede82f032b2e95e92cc00` | This repository’s `LICENSE`, byte-identical at `5b0eb012` |
| `ATTRIBUTION.txt` | 688 | `aa6397bd07d2f939ff79fe9179870346fbb44d0244d9672090406fc4c9db4640` | Credits the schema to this repository |
| `evidence/README.txt` | 4295 | `c9282c4ea69f3418897c4729873cc9d7267997a46750265a130b6eb2003149d7` | The package’s account of the result and the construction |
| `evidence/public-comparison.json` | 3681 | `bd26489968fbf854e5607397b8c455db53f901be5f1c5a2590b33e26dc3e8fbf` | The author’s dated survey of prior n207 sides |
| `evidence/document-binding.json` | 817 | `f1e6e14d0de1e9933f0621ded412a024517ddc235564d55a2dac7fd3b14082f6` | Digests of the certificate before and after two path strings changed |
| `evidence/centres-and-halfangles.csv` | 34987 | `e36568d67113488d5e39a447b941aab387ecb08484ed2b7d87d124ec8f46c169` | Export of the poses |
| `evidence/vertices-exact.csv` | 170598 | `69b6e08cdc02500ad13593a615bacd8f25dea6b8486ed1669a44b09ec83652e9` | Export of the corners |
| `evidence/vertices-decimal.csv` | 70635 | `7cd31a2992f693691fec3e51310e01bf4a3281f6f6ce5e316ca79f2403b5e1bb` | 50-digit corners, a preview |
| `evidence/n207-verified-comparison.pdf` | 20317 | `ae323e59850c8bad109358d00df487de51c7349989a6b25cbdf4b4e0518fa12e` | The top-level PDF |
| `evidence/n207.svg` | 45578 | `c56d600c749471b328e5bcbe391b9a383c1c3353c5f4557b4dcf98ee0dbf7a88` | The top-level drawing |
| `START-HERE.txt` | 2099 | `29ee35ca5f7aab80221a5b30c86a98935ca55641a2a6528a52134e8844535488` | Preparation notes, written before publication |
| `SQUARES_PROJECT_REQUIREMENTS.txt` | 6692 | `ca2a65389ec643987381215c98939c24f5e7bb08e4ce830d304a59b2303fb5a1` | The author’s reading of this repository’s intake rules |
| `ISSUE_TITLE.txt` | 49 | `584762e9e9e4de281bfd171480db6633b43763ae379f15b51e1299e129a40f26` | Draft issue title |
| `ISSUE_BODY.txt` | 5627 | `2b0a3261f0217b4ea1ff7ed4294c19d3a29fd62d7b107ff709395ce693243a1e` | Draft issue text |
| `manifest.json` | 3386 | `90c60999487b023e3ec8624a2ab726abf04ee753bd2f5f344b78321af22e58c9` | The package’s digest list |

The n70 source is a JSON certificate of side
`8880960371555579594785501178639/1000000000000000000000000000000`, whose `provenance`
names Evan Daniel’s `search/regularize/lists/certs/n-070.cert.gz` at `7dfca4e` with
SHA-256 `65b1c4698129560857ad4f91ec9a7a12980de0ceb619bcc814e55a3fd9ef597d`. That is the
digest the [T-146 packet](../evand-regularized-2026-10-10/README.md) records for the
file, and the side is T-146’s n70 side exactly.
Whether its poses are that file’s was not checked here.

## The Certificate

`n207.cert.json` is a JSON object with `n`, `s_exact` (a rational string), `squares`,
one `[x, y, t]` triple of rational strings per square, the centre in $[0, S]^2$ and
$t = \tan(\theta/2)$, so $\cos\theta = (1-t^2)/(1+t^2)$ and $\sin\theta = 2t/(1+t^2)$
exactly, and `provenance`, the construction record.
`devtools.upper_bound_reports` reads it with the `pingyou-json` adapter, which takes
`s_exact` and `squares` and reads `provenance` without believing it.

The construction, as the source states it: two differently placed patches of the n70
source, one reflected in both axes, transposed and translated by $(6, 6)$, keep 60 and
69 whole squares, and upright grids of $7 \times 6$ and $6 \times 6$ squares add 42 and
36, $60 + 69 + 42 + 36 = 207$, in a box of side $14 + f$. Every centre and the box are
then dilated by $10000000001/10000000000$, the squares keeping side 1. The provenance
states $f$ as `880960371555579594780501178639/1000000000000000000000000000000` and the
dilation, and their product with $14 + f$ is `s_exact`.

`pingyou-n207-rational.yaml` states the same 207 squares as rational corners in this
repository’s Witness/v2 format, in JSON syntax.
The `witness-corners` adapter recovers each pose from its corners exactly.

## Against the Record

At `main` `3a5a91a90` the case record’s reported and verified ceilings are both
Siddharth Gupta’s refinement of a SQUISH packing, side
`14887992258302657381304248932763/1000000000000000000000000000000` (T-127,
`E-gupta-438-exact-feasibility`). The certificate is below it by
`70318852589817493681897946459498821361/10000000000000000000000000000000000000000`,
about $7.03 \times 10^{-3}$.

The one register entry pending at 207 is SQUISH’s T-136 (#481), whose exact side,
$14.885506308841677682\ldots$, is rebuilt from the
[SQUISH packet](../squish-481-third-request-2026-10-09/README.md).
The certificate is below it by $4.5459357980020505 \times 10^{-3}$, the margin the issue
states.
Of the other reports of 11 October, #500, #501, #504, #505 and #506 state no side
at 207. [acquisition/claims.json](acquisition/claims.json) freezes these comparisons,
and `devtools.upper_bound_reports` rebuilds them from the retained packets.

## Derived Fact and Exact Replay

`devtools.upper_bound_reports derive` read `n207.cert.json` from a checkout at the pin,
after `devtools.acquire_source` showed that the checkout yields this packet’s
acquisition record and manifest, so the bytes it read have the digests above.
It admitted the certificate at the exact fraction the issue prints.
It then read `pingyou-n207-rational.yaml` from the same checkout, as the row’s
`same_packing` file: all 207 poses and the side are the certificate’s exactly.
It wrote the certificate as an exact rational `center-basis` Witness/v2,
[facts/n-207.yaml.gz](facts/n-207.yaml.gz), naming the certificate’s SHA-256 as
`revision_sha256`. The fact is this repository’s derivation; offline it must rebuild
itself from the certificate it states, and `derive --check` with a checkout compares the
fact and the witness again.
The declaration of the import is [acquisition/report.json](acquisition/report.json).

Only the fact enters geometry decisions, through the two-route kernel of
`devtools.evand_arrangement_reports`: `sqpack`’s exact witness verifier and the
independent rational corner checker, each deciding every wall and every pair over
$\mathbb{Q}$. A positive job, a duplicate-square control and an outside-container
control each ran in their own child process, one worker at a time.
The positive passes both routes and both routes refuse both controls.
Both routes find the least wall clearance exactly $1/20000000000$ and the least pair gap
`19999999989999999999016010000001601/200000000000000000000000000000000000000000000`,
about $1.0 \times 10^{-10}$, the margins the source’s `native-replay.json` records.
The three jobs made 127,926 pair decisions in 54.66 route CPU seconds and 103.49 job
wall seconds, summed; the longest took 40.08 seconds, and the run 1 minute 53 seconds of
wall time, with other lanes on the machine.
`check --replay` decided all three jobs again in 2 minutes 10 seconds.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.
The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method.

The issue reports that `packing-witness verify` and
`devtools.check_rational_witness_independent` at `5b0eb012` accept the source’s own
witness file. The seven files of this repository that
`native-replay-source-manifest.json` names have the digests it records, and they, the
`packing-witness` command and the independent checker are unchanged from `5b0eb012` to
`3a5a91a90`. Run here on the pinned bytes of `pingyou-n207-rational.yaml`, both accept
all 207 squares and 21,321 pairs with the margins above, in about 13 and 6 seconds
including start-up. Their outputs were not kept; the receipt above is the replay.

## What Is Not Established

The source reports that its three exact checkers accept all 21,321 pairs and every wall,
and that `reproduce.py` rebuilds every pose and the side from the n70 parent.
Those are author reports.
`VERIFY.py`, `reproduce.py`, the three checkers, `convert_witness.py` and
`replay_upstream.py` were read here and not run: the two maintained routes decide the
certificate from its own poses, so none is needed for the bound.
That the 207 poses are the stated transformation of the n70 source bears on credit, and
was not checked here.
The replay above has not been reviewed.
The certificate establishes a finite upper bound only; the source claims no local or
global optimality.

## Credit

The source credits PingYou Ltd with the n207 assembly, Ryan Xu with the n70 construction
it uses ([#432](https://github.com/jlevy/squares/issues/432)), Evan Daniel with the
exact retention of that construction, and Nate Chaoweeraprasit (SQUISH) with the prior
n207, which it uses only as the comparison.
It claims neither the n70 packing nor patch composition in general.

The pinned source makes no statement about AI assistance.
Its first commit and the issue as first posted said that OpenAI Codex assisted the
verification, the comparison review and the package; the pinned commit, titled “Correct
attribution in submission materials”, removed that sentence, and the issue was edited to
match. Neither says why.
Asked on the issue which account stands, the author answered on 12 October 2026, for
this release and the n153 one
([comment](https://github.com/jlevy/squares/issues/503#issuecomment-6129716138)): “Both
solutions were AI assisted by ‘PY’, an unreleased agentic AI offering by PingYou Ltd.”

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source pingyou-n207-certificate-2026-10-11 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-n207-certificate-2026-10-11 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-n207-certificate-2026-10-11 check --replay
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-n207-certificate-2026-10-11 derive --checkout CHECKOUT --check
```

`--check` re-derives the record from this packet alone.
The importer’s `check-claims` and `check --replay` run offline from the fact;
`derive --check` needs a checkout at the pin, refuses one that does not yield this
packet’s record and manifest, and compares the fact and the source’s witness with the
certificate.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `facts/n-207.yaml.gz` | receipt | `ac87d2583a7897c236c491b6d760d75cffef7ba4` | `8a561c4c1b784622b6e820897758a812f265e2b86242b6651aa1282bd22dce60` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
