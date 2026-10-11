# Guzhou0806’s Clipped-Corner Transfer: s(40) > 335427/50000 on wand125’s Density

[Issue #485](https://github.com/jlevy/squares/issues/485) (Guzhou0806, opened
2026-10-10T07:28:06Z) reports two lower bounds for $n = 40$, unrestricted rotations,
from [Guzhou0806/n40-square-packing](https://github.com/Guzhou0806/n40-square-packing/tree/e5abeb4d078a5c5b35df6204dd9b93378e5a7880)
at `e5abeb4d078a5c5b35df6204dd9b93378e5a7880` (tree
`8c01f4dd532befca302b8a04337c94e41096f787`, committed 2026-10-10T06:47:01Z), which the
release tag `n40-670854-20261010` names:

| Bound | Exact form | What it rests on |
| --- | --- | --- |
| $s(40) > 335427/50000 = 6.70854$ | strict | the nodal statement below, the density’s essential supremum $g \le H = 2818711359413/10^9$, and the clipped-corner transfer |
| $s(40) > 67000\sqrt{6400006889}/798988091 > 6.70848908$ | strict | the nodal statement alone (the full-core argument) |

The nodal statement is that every closed square of side $B = 9977/10000$ inside
$K = [0, 67/10]^2$, at each of the 401 directions $\theta_j = 2\arctan(83j/80000)$,
$j = 0, \ldots, 400$, captures at least $10001/10000$ of wand125’s `rect_n40_L67`
density. That density is the one the
[2026-10-01 rectangle packet](../wand125-rectangle-certificates-2026-10-01/README.md)
retains for `T-068`’s $s(40) \ge 67/10$; the source’s copy is byte for byte the same
(SHA-256 `71011d0356dd179c6e7e6e02c9a064ff30f6f13844016ce3b97463bf7ef53dc0`), so this is
an extension of a certificate the record already holds, not a new density.
The argument is in the source’s `PROOF.md`; the mathematical review is
[review-2026-10-10-guzhou-n40-clipped-corner-bound.md](../../../../docs/project/reviews/review-2026-10-10-guzhou-n40-clipped-corner-bound.md),
which found no blocking defect and wrote the replay contract this packet’s receipts
answer.

The release `n40-670854-20261010` was published 2026-10-10T06:50:59Z with one archive,
`n40-670854.zip`, 203,095 bytes, SHA-256
`dbefee8658dc8f7d2e4a6ed21b0c3cd29f36ae393405a218f6bbfdce54465bc5`, the issue’s.
The repository’s only earlier commit, `485dd8f` (2026-10-07T18:50:46Z), published a
weaker $s(40) > 33509/5000 = 6.7018$ on the standard 201-direction net; it is pinned by
the history and not retained.
The sources were retrieved at 2026-10-10T10:28Z.

## Retained Here

`devtools.acquire_source` wrote [`source/`](source) from a full clone checked out at the
pin, from the declaration in [acquisition/declaration.json](acquisition/declaration.json);
every file is bound to its Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest
of all 36 files of the tree (783,901 bytes).
The source’s own `SHA256SUMS` holds for every one of its 35 lines in the tree and in the
ZIP.

Twenty files are retained (266,160 bytes):

| Upstream path | Git blob | Bytes | SHA-256 |
| --- | --- | --- | --- |
| `.gitattributes` | `fa1385d99a319b43c06f5309d1aae9fdd3adea46` | 8 | `705fd4d6451a31d36b3df7de96f83f30ac976c9b4a6d1e51671d8e2f33e2d0da` |
| `.github/workflows/verify.yml` | `115cdbe122dee85100773a3815b75d146123bef4` | 1361 | `01855e33fd9a5971bbe298d2caf1f63e739c8e36f93aa46b9012763c12c9675a` |
| `.gitignore` | `d42f3bf5659d0bf42dab359b2c19b896c1a313b9` | 60 | `f100449959ece70d800b04473f6bd6c60b3e59985b5d933522bb3bec57ac07dd` |
| `LICENSE` | `654ff03eb31bc71611c2a709767d2044d88af0cf` | 1067 | `94be33291ae276999b6f49d7ebc3ed2d35e11e61e2fcd443f810178c09a2fad9` |
| `PROOF.md` | `af47121dcc74c40b9fd9e60f87ae6cb562ec8b9d` | 13098 | `6b3b69747eb61a1ed50904b5ff9139748f8ccb64c9178ec051500b148d6947e3` |
| `README.md` | `cef659195ca1f298ef2c122d26b8c8f2fe93373a` | 2700 | `2ea3cb55d5fe73c3573fdcab51af1fbbc046c71d8846ad1cf2cf994e385c0dfd` |
| `REPRODUCIBILITY.md` | `ba4660ef7ab431690a885ba11ab25f801c135b2c` | 4023 | `5cb19bd763987c8b61c8c139bfe312442139f3c4fce1c902955a18f6553ea5be` |
| `SHA256SUMS` | `c0d13154dc9d848513612356bfb2c9a7bce07f1f` | 3265 | `0d3b33f4d558ef9b0453ce5cfda2304e6be38db1cf0ac2fc9356ea6b89722baa` |
| `SOURCES.md` | `5ec0c8b204ce5f9996a54d06324c3bc5e35bd72b` | 4080 | `ae8d1ff72c41af0ba0d55043dd817c4a838a82d7a0742e6d5fe96f2d40b9d746` |
| `VERIFICATION.md` | `b15a067d98af6a6dfae096f493dd6c8cf694b81e` | 3932 | `56866b42763e89b3cd6bc361d56dec08d58e2f1dbc2a0363b15b706786b56c67` |
| `certificate/parameters.json` | `6df4aba53258da90377a8cf6dd4e415b9cbfb5c2` | 257 | `25948860a141dc0895ed439d923bb29efef223ffed1cfa0ce01e6e0f1b06dba4` |
| `licenses/jlevy-squares.txt` | `239dffb892be26bfe17991b8396ae78ad9235cee` | 21153 | `7428341239cf4ee78c4b951b7fd8a2284b24835aeb0ede82f032b2e95e92cc00` |
| `licenses/wand125.txt` | `bbfbff131ef8ccbba5ed8b8b395f2c457eb8922c` | 1064 | `c0dd43e7892932c81335f74a2fdbf1a98f5977bab14c0c4c30e3abcc97c34904` |
| `results/nodes.jsonl` | `f36052aef506626e3e0f85cb1b26f61a64db001d` | 173496 | `bc06cf4c97ad0421cc84bda64079d4b947eb78f1b90ae80e579f3824c3d27442` |
| `results/verification.json` | `d22bd45ac7517379f1b97d4583859be3f1ff865e` | 6987 | `12f15658343ffa9e982ac97045d69c719bcee873588f19f3f5cd7a197e289a3a` |
| `tests/test_finite.py` | `8042c5bc558f54c28cab43d253a9aafada8da0d7` | 4363 | `6dcd01f7574ba23fe77b2ea2f244dfc57f293f749a134e07d0a756e72bef1233` |
| `verifier/finite.py` | `4c520b51837c729bd732a1ad9a8419c49d2ad514` | 9473 | `6046849f25beeb3491789f2dd0a2c59e5ce51696e1078c201c410c8f1affc861` |
| `verifier/prepare.py` | `d2cc377d6cb0eaff2afbf40ed79c817a1f778f8d` | 2391 | `a460713e04799b085c4df37eb4baa41dc10dc71904128f456212b5ec63f92669` |
| `verifier/release.py` | `045c1a76a61d83071641291a881ffb5da9638d64` | 7214 | `65e80efa05142f13a03a4b47b403dacd8577dfccb7de2e7ff96088c77800555e` |
| `verifier/run.py` | `4c6d33d371ad45c1b64bc95cf0dc4a22a0487c0b` | 6168 | `4efa0d97dfb0cc0dcce172dfd31c9bb2f4547cfb472d4bde1e84b78695181485` |

Sixteen files are pinned by digest and not copied (517,741 bytes); the record lists
each with its size and digest:

- `certificate/certified_candidate.json` (332,847 bytes) is wand125’s density, the bytes
  of the 2026-10-01 packet’s
  `wand125-rectangles/certificates/rect_n40_L67/certified_candidate.json.gz`, which
  `acquire_source --check` compares.
- The fifteen files of `verifier/sqverify_fast/` are this repository’s own crate,
  `packing/sqverify_fast`, vendored byte for byte from `ef79288a4`: each was compared
  with the crate here at acquisition, the crate is unchanged since that commit, and
  `build.rs`’s digest of the vendored copy is `d97758bb…`, the reviewed source the replay
  below was built from.

The source’s scripts were read and none was run here.
The `results/` the tree holds are the producer’s local run (GN-3 of the review).

## The Release ZIP and Its CI Receipt

The ZIP holds the 36 files of the tree, of which 33 are byte-identical
([release-ci/zip-entries.sha256](release-ci/zip-entries.sha256) digests every entry).
The other three are its `results/` and the `SHA256SUMS` lines that name them: the ZIP
carries the receipt of GitHub Actions run
[38032128403](https://github.com/Guzhou0806/n40-square-packing/actions/runs/38032128403)
(`success` on `e5abeb4d`, started 2026-10-10T06:47:00Z) in place of the tree’s.
Both are kept and named for what they are:

| Receipt | Where | `verification.json` | `nodes.jsonl` | `source_commit` | Binary | Wall | CPU | Python |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| producer’s local run | `source/results/` | `12f15658…` | `bc06cf4c…` | null | `75a14053…` | 60.06 s | 234.58 s | 3.14.4 |
| CI run 38032128403 | `release-ci/results/` | `f8122b80…` | `2e7e9b33…` | `e5abeb4d…` | `f167c16b…` | 72.35 s | 286.71 s | 3.12.3 |

Both report Rust 1.98.0, four threads, 401 of 401 directions verified, 32,970,910 boxes,
the crate source `d97758bb…` and the derived input
`49f696a4533ded9532b879bf69706da35bc03a49db79718573760adc08cd458e`; their 401 rows are
identical apart from timing.
[release-ci/](release-ci) also keeps the ZIP’s `SHA256SUMS`
(`77527e85…`), the release’s own digest file `n40-670854.zip.sha256`, and the GitHub API
records of the release and of the run (metadata only; the run’s log was not read).

## The Replay Here

The review’s replay contract has four parts, and each ran here by
[`devtools.audit_clipped_corner_transfer`](../../../devtools/audit_clipped_corner_transfer.py),
a first-party tool that shares no code with the release’s `verifier/finite.py`.
Its receipts are in [receipts/](receipts).

**The derived input.** Regenerated from the retained candidate as the contract states:
the 480 positive-weight rows in file order as exact fractions, with the net in the
`certificate` metadata (`D = 83/80000`, `angle_count = 401`).
Its SHA-256 is `49f696a4533ded9532b879bf69706da35bc03a49db79718573760adc08cd458e`, the
input both release receipts name.

**The nodal run.** On a build of reviewed crate source:
`sqverify_fast_census --source-digest` printed `d97758bb…` as reviewed source for the
standard and declared nets (`910b6b12c`, the declared-net soundness review of 6
October); `cargo build --release --locked -j 2` with rustc 1.98.0 (`88d9e12ae`
2026-08-18) gave the binary `567a0fd58f7ae4e981580f2a90bed5c92ac44fa8f3ebb442b166e93043c15ed4`,
the 6 October review’s, which embeds that digest.
The command was the contract’s:

```text
sqverify-fast --candidate derived-401.json --n 40 --side 67/10 --directions all \
    --threshold 10001/10000 --threads 2 --confirm --receipts receipts
```

| Contract | Here |
| --- | --- |
| 401 rows `verified`, summary `VERIFIED`, `refused_directions: []`, no fault injected, exit 0 | the same |
| premises `format T`, `net_origin metadata`, `angle_count 401`, `D 83/80000`, `mass_exact 3999/100`, `expanded_rectangles 3792`, `input_sha256 49f696a4…` | the same, every field equal to the finite audit’s values |
| $r = 0$ by the axis sweep over 4,879,681 vertices, 2,209 events per axis, bound 1.0012141064171602 | the same |
| 32,970,910 boxes, greatest depth 30, least certified bound 1.000100000471634 at $r = 73$ | the same |
| rows identical apart from timing to the release’s | all 401 rows, against both the local and the CI receipt |
| even rows equal the retained 201-direction census row of `rect_n40_L67` | all 201 (row $r = 2k$ here is census row $k$, apart from timing and index) |
| two to three minutes at two threads | 299.5 s wall, 241.0 CPU-seconds (the summary’s direction CPU 240.87 s, against the source’s 234.58 s), on four cores shared with other work at a one-minute load average of 6.8 before and 8.0 after |

`--receipts` wrote each stdout row with the input’s digest, and the summary.
An earlier run of the same command with the same binary, before the tool drove it, took
396.0 s of wall time and 242.6 CPU-seconds at a one-minute load average of 15.6 before
and 12.8 after, and its rows were also identical to both release receipts apart from
timing. The wall time over the contract’s estimate is the shared machine’s load; the
CPU time is the source’s.

**Controls A to D,** on the crate:

| Control | Contract | Here |
| --- | --- | --- |
| A: weights × 99/100, metadata kept, directions 73 and 220 | refused at both with exact witnesses below $\tau$, exit 1 | `REFUSED` at `[73, 220]`, exit 1; exact captures 0.999322755117 and 0.999227715635 at the witnesses |
| B: weights × 499392017517921/500000000000000 at direction 220 | refused with an exact witness 1.00009999… | `REFUSED` at `[220]`, exit 1; exact capture 1.0000999998 at the witness |
| C: the `certificate` block removed | admitted on the standard net, another claim | exit 0, `net_origin standard`, 201 directions at `83/40000` |
| D: `angle_count 201` with `D 83/80000` | admission refuses | exit 2, “the net does not reach past pi/4” |

The control point is the census’s: of the 400 least-bound leaf centres at the oblique
directions, the one of least exact capture, $r = 220$ at
$(3.353931795732347, 5.09801085267264)$, capture 1.0013165658, where the crate’s
`--probe` gives the same rational; B’s factor is the census rule at that capture.
Every witness lies in Tokoharu’s centre domain and its capture, evaluated again by
`sqpack.rectangle_density`, equals the crate’s exact value.

**The finite steps.** `check` recomputes, in exact rationals and on the retained density:
480 rows, $M = 3999/100$, 3,840 terms and 3,792 distinct rectangles, D4 invariance,
$\int g = M$; the exact essential supremum
$2818.71135941178\ldots \le H$ ($H - \operatorname{ess\,sup} g = 1.215 \times 10^{-9}$),
with $H$ reproduced by rounding the merged densities up to $10^{-9}$; the net’s premises;
$q \ge B$; the first branch’s containment (slack $1.63 \times 10^{-15}$);
$b = 41804244441680000/80000042740596391757$; $\chi = 0.999790035571 \ge 99979/100000$;
$40\chi - M = 0.00160142285$; $40 \cdot 99979/100000 - M = 1/625$; and the full-core
closed form.
Every value equals the `finite` block of both receipts, and the parameters, digests and
nodal premises of both agree with it.
Its controls are refused: E ($H - 2/10^9$) fails the density bound; F
($X = 335428/50000$) fails at every admissible $h$, the margin bounded above by
$-0.00998$; G ($h + 10^{-15}$) fails the containment; H (the 201 net with the same
$h$) gives $\chi = -0.956$.

**What the checkers share.** The nodal statement was decided by `sqverify-fast`, which
is the code the release itself ran, vendored from this repository: the replay reproduces
the producer’s nodal run with the producer’s code (GN-4 of the review).
The finite steps were re-implemented here independently of `finite.py`; the two share
the definition of the density, its D4 expansion and the transfer’s formulas, and nothing
else. The control evaluator `sqpack.rectangle_density` was written before the crate.

## What Is Not Established

No second method decided the nodal statement: Tokoharu’s `verify.cpp` at 401 directions
would be one, at roughly twice its 201-direction cost on this density, and needs an
input generator for a finer net.
The crate’s lemmas beyond the admission path rest on the reviews of 3 and 6 October; the
format T metadata-net path has no review of its own (GN-6), and the 10 October review
read its admission.
The census route for this certificate is not run (GN-5): the driver and evaluator now
read a format T metadata net, but no census case holds the derived input.
wand125’s review comment on the issue
([6095317723](https://github.com/jlevy/squares/issues/485#issuecomment-6095317723),
2026-10-10T07:53:18Z), reporting a third run of the release’s entry point and an
independent exact check of the transfer, is third-party evidence on the issue and was
not reproduced as such here.
No packing, optimality or priority is claimed by the source or established here.

## Credit and Licence

The new material is Guzhou0806’s under the MIT licence (`LICENSE`, copyright 2026
Guzhou0806). `SOURCES.md` credits the rectangle density and the original verification
method to wand125, Tokoharu “and their cited predecessors, including Stromquist, Burns
and Massaccesi”, says the Rust sources keep their byte identity from this repository at
`ef79288a4`, and gives Guzhou0806’s contribution as “finer-net verification, strict core
transfer and the uniform clipped-corner integral composition giving 6.70854”, from
“AI-assisted research”. The density’s MIT licence is retained in
`licenses/wand125.txt` and this repository’s licence in `licenses/jlevy-squares.txt`.
The issue’s AI-assistance statement: “AI assisted the mathematical exploration, proof
drafting, implementation, testing, packaging and this submission under my direction.”
wand125’s comment on the issue calls the issue’s credit wording “accurate from our side”.

## Compressed Files

The replay and control receipts are stored as deterministic gzip; `gunzip -k` restores
each beside it.

| Stored file | Origin | Git blob (decompressed) | SHA-256 (decompressed) |
| --- | --- | --- | --- |
| `receipts/control-A-scaled-99-100.jsonl.gz` | receipt | `5ff72cd354c9501cdd0f9c4b6695afb475d85a57` | `8e0db83430028cb0eeec9d309e0a36df878d1a6b92aefc1f3a8dca964c7d7e61` |
| `receipts/control-B-near-threshold.jsonl.gz` | receipt | `4786c22ddd136f30a219e06916cef0b222860127` | `255a32ad64e4b7a0ad5c3dc0f7111f71be3d46178880e7619de3d8352c8d88af` |
| `receipts/control-C-no-metadata.jsonl.gz` | receipt | `847465327b0ec3fa6c58f1bb0f2d75a5ad7a483f` | `35f5d13272fb37fdeec6a8eac08ac73c36cec610d81205fd5b854582c5bc5ef0` |
| `receipts/control-D-short-net.jsonl.gz` | receipt | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `receipts/replay-401.jsonl.gz` | receipt | `ee9ad793777db0a0992db3070ac1eb5bfa21e86b` | `2e52131e8f962116f1e6bddc0aafc6fa392a28338ac6faff4a6a05384663799b` |

Control D’s receipt is empty: admission refused the input before any row, and the
refusal is in `receipts/runs.json`.

## Commands

From `packing/`, each after `uv run --frozen --all-extras --group dev`:

```sh
python -m devtools.acquire_source guzhou-n40-clipped-corner-2026-10-10 --check
python -m devtools.audit_clipped_corner_transfer check
python -m devtools.audit_clipped_corner_transfer check-replay --rank
python -m devtools.sqverify_fast_census --source-digest
python -m devtools.audit_clipped_corner_transfer run \
    --binary sqverify_fast/target/release/sqverify-fast --out SCRATCH --threads 2
```

`check` and `check-replay` read the retained files only; `run` builds nothing and
writes fresh receipts to `SCRATCH`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
