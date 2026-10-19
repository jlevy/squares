# Guzhou0806’s New Rectangle Supports: s(40) > 3359/500

Guzhou0806’s comment of 2026-10-11T07:39:30Z on
[issue #485](https://github.com/jlevy/squares/issues/485#issuecomment-6106761997) reports a
lower bound for $n = 40$, unrestricted rotations, from
[Guzhou0806/n40-square-packing](https://github.com/Guzhou0806/n40-square-packing/tree/6a65957e6c5c51cdf267917d882dab7f5b4928dd)
at `6a65957e6c5c51cdf267917d882dab7f5b4928dd` (tree
`3258ec542a0cf7fe42812487a23c7e2cc2a72365`, committed 2026-10-11T07:12:04Z), which the
release tag `n40-new-supports-6718-20261011` names.
The commit descends from `71c97d07`, the pin of the
[continuous-pose packet](../guzhou-n40-continuous-pose-2026-10-10/README.md) that retains
`T-145`’s $s(40) > 1340000/199529$. The issue was retitled
“s(40) > 3359/500 = 6.718: updated registration request”.

| Bound | Exact form | What it rests on |
| --- | --- | --- |
| $s(40) > 3359/500 = 6.718$ | strict | every side-$B$ square in $K$ captures at least $\tau$ of a new density: the continuous kernel over 43 slabs for $t \in [10^{-6}, 83/200]$ and the axis kernel at side $A$ for $t \in [0, 10^{-6}]$; then $40\tau - M = 1/500$ |

Here $K = [0, 67/10]^2$, $B = 3350/3359$, $\tau = 4999/5000$, $M = 3999/100$,
$A = 249329659/250000000$ and $t = \tan(\theta/2)$.
The bound raises `T-145`’s by exactly $217911/99764500 = 0.0021842539\ldots$.

What is new is the density. `certificate/certified_candidate.json` (SHA-256
`984fcd3acc605fe3c50a84912eed77e0192ca5b7253b19b6aa31a4e28e1bf5c2`) lists 685 positive
D4 rectangle orbits: 522 marked `inherited`, each a row of wand125’s `rect_n40_L67` pool
by its `source_index`, and 163 marked `generated`, outside that pool; every weight is new.
A weight $w$ on a box $R$ puts density $w/(8|R|)$ on each of its eight images (`PROOF.md`,
section 1), so the mass is $\sum w = M$.
`certificate/original_density.json` is the pool itself, byte for byte the copy the
[2026-10-01 rectangle packet](../wand125-rectangle-certificates-2026-10-01/README.md)
retains (SHA-256 `71011d0356dd179c6e7e6e02c9a064ff30f6f13844016ce3b97463bf7ef53dc0`).
Both kernels and the tests’ harnesses and oracle are byte for byte `T-145`’s, which the
[10 October review](../../../../docs/project/reviews/review-2026-10-10-guzhou-n40-continuous-pose-bound.md)
read line by line; the review of this release is
[review-2026-10-12-n40-new-supports-6718.md](../../../../docs/project/reviews/review-2026-10-12-n40-new-supports-6718.md),
which found no blocking defect, and the complete replay here is below.

The release also states a separate negative result, in `OBSTRUCTION.md`: no nonnegative
weighting of the 2,526 original uniform D4 rectangle orbits gives a uniform per-square
charging contradiction at $X \ge 168/25 = 6.72$, by a finite exact dual over 388 poses
that a Python `Fraction` program and a C++ Boost rational program both check.
It is not an upper bound on $s(40)$ and bears on no register value.

The release `n40-new-supports-6718-20261011` was published 2026-10-11T07:39:20Z with
one archive, `n40-6718.zip`, 196,420 bytes, SHA-256
`e6e495901b2bfb590a4154ad5cc296b72dff785c9fda5e9b40ef0711158e3b3f`, the comment’s, and
its digest file `n40-6718.zip.sha256`.
The sources were retrieved at 2026-10-11T20:35Z.

## Retained Here

`devtools.acquire_source` wrote [`source/`](source) from a full clone checked out at the
pin, from the declaration in [acquisition/declaration.json](acquisition/declaration.json);
every file is bound to its Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest
of all 35 files of the tree (812,343 bytes).
The source’s own `SHA256SUMS` holds for every one of its 34 lines in the tree and in the
ZIP.

Thirty-four files are retained (479,496 bytes):

| Upstream path | Git blob | Bytes | SHA-256 |
| --- | --- | --- | --- |
| `.gitattributes` | `1f9683ba325ebf468c324187e140a55c0eb25523` | 58 | `2d5c072f5cbe11a4c74660a6e47beffcf246fc3546a5aaa534b21c724fe2f9fc` |
| `.github/workflows/verify.yml` | `4452a79c402841f7f851e24ae9ffebf5d8d52994` | 1436 | `e22fb3fd8a977166546b04fde0ebe18d18b1ea4339627068185f04a59ee410dc` |
| `.gitignore` | `5ef9f3a66a0b531e7d6dc905a2e9e482d19473f5` | 37 | `85e9e61c0a8dee51b98253a262d7a2f3f8fe29badf2d145a68b510bdd330b7f5` |
| `LICENSE` | `654ff03eb31bc71611c2a709767d2044d88af0cf` | 1067 | `94be33291ae276999b6f49d7ebc3ed2d35e11e61e2fcd443f810178c09a2fad9` |
| `OBSTRUCTION.md` | `f355b0ccf9463794260537af7d714e8586891a9a` | 5144 | `2c3f1d8bb879564020c2b5002dd535aa3aa6e930ed9651d14c6854b6b85993e1` |
| `PROOF.md` | `5c2977fbc34ddeb8eaa0b7cea759ed81d5695c21` | 15587 | `bff9666bd08582f990041684c66c489be543f99a7646acdddfbe6995ef361a40` |
| `README.md` | `61cb146cb9c1c6b875b7863ea9466989f17026f4` | 2872 | `69c54ccfd67c625977f0b89496e624cbef8c059a68a3f3d9398f569ad3b128ba` |
| `REPRODUCIBILITY.md` | `b736d503f57ac101abcbeb03a4d6f12d001c39ed` | 3860 | `f03db2eff1693d52a4a3c9882cff0756d4335163c9204798ba9421c863ba22a1` |
| `SHA256SUMS` | `38b84225383c904bd077ce7e0b73066ca6f58537` | 2961 | `8dfd478ca99bd6d3f644c9d396e48df6fddfcc7981f058e3b22071ce2065ae17` |
| `SOURCES.md` | `00d51ac171e77bba4e11dff9a057681694b049d1` | 4042 | `5d5d28122bcfd045e777443ed857502999c332bd5ca24247dd98981eeae0a0f7` |
| `VERIFICATION.md` | `13a65e0a03a57bb20bc62f7796a0fdc49a34e414` | 4069 | `4bb5a30cb6757bcd4bfd6d141e71043865902dfb7df1d340dca606c82bcfb4f9` |
| `certificate/certified_candidate.json` | `34b9e12db7add79fd0f809cade8dc1864844f146` | 209537 | `984fcd3acc605fe3c50a84912eed77e0192ca5b7253b19b6aa31a4e28e1bf5c2` |
| `certificate/parameters.json` | `78170b35842be75c7082cceb7bc717b0231ad8e2` | 790 | `498d01eda89a0cedecce25f944329a26da578ff73f52850b92a9390eb7f4dc11` |
| `licenses/jlevy-squares.txt` | `239dffb892be26bfe17991b8396ae78ad9235cee` | 21153 | `7428341239cf4ee78c4b951b7fd8a2284b24835aeb0ede82f032b2e95e92cc00` |
| `licenses/tokoharu.txt` | `3b9a49cd1e449395373f48106c357e63cc2ed683` | 1065 | `8dc3364f10709e043998e74d0de02774a7f6c9b08dde3a8a58336948d9ed8ad8` |
| `licenses/wand125.txt` | `bbfbff131ef8ccbba5ed8b8b395f2c457eb8922c` | 1064 | `c0dd43e7892932c81335f74a2fdbf1a98f5977bab14c0c4c30e3abcc97c34904` |
| `obstruction/certificate.json` | `82774999cec21733f21c886e4b76eef0adafd429` | 93053 | `f4edfa9a08efaffe8916d3da2c2a8ff567489a2185319de742e8b9e97e3939f9` |
| `obstruction/check.cpp` | `71857e26c823b1f42c0d75b57b8634a9f0a38d39` | 4129 | `fd46b3c6235b2ad5fc720b9df89e338149be4e8b48b9d925810c88a4392fba92` |
| `obstruction/check.py` | `5a549c757e74bbd1d6c156ac4467db9e27f53dc5` | 3704 | `ab7098051a951fb400882d546a1cc27ceaf85fd4b8c180bd356fcbffa962a026` |
| `obstruction/run.py` | `54c4311297b6d7ab3c0962569913ec798ea5e8bd` | 3494 | `c8feec6bed2148abb1b1640a5c9bd1fd561db50da2b7ad4a099630b9ab48095e` |
| `results/axis.json` | `e6a9a04752f66fa26fb8921be8f76ac1863ceeff` | 719 | `0db283c86a302e2efa23dbb024bda1f244f12d0205a294630fc298bc59df0136` |
| `results/obstruction.json` | `8716ffe089db84acfb5fca25fd09acccf4ed9eec` | 3596 | `63e88db5a4ba9bce053d7d20650916621b60c205637f98fc5b63c242ef929591` |
| `results/slabs.jsonl` | `d031eadfad13e331ce73a505eb71127d5ffc1746` | 33402 | `7f66379f4c4be56092cdad20289b98268c9ec7329c0a4afba0bdfc27c344dcb8` |
| `results/verification.json` | `1104bd78cbe5e599eaf960d3d91b470028c70660` | 11061 | `201c8cc0fab66ffac023095efea404cb544ae988f9bf8d278e7078d34c45b608` |
| `tests/kernel_harness.cpp` | `20082196d8721819d007c2c2bf5e6a2ed8e3c19f` | 888 | `4ee681bced642c708eda7d71845836d3ea18d61c350ff49ef26e199fb9ee6e40` |
| `tests/oracle.py` | `3e36d5811b35c772dfc875c6bc1ddccbf51b869c` | 1073 | `395fa622bec60607798a3da4103162313833fe9c139a40ca2023cd00c14d581e` |
| `tests/rounding_harness.cpp` | `c43913a913d546d3a2d78ad4f385675d70bb1f81` | 1161 | `96bd022242b4c0e44ff3eb27a8294d3d359bc74263f898e350768eeb78fdfc9f` |
| `tests/test_admission.py` | `ff089bb8d88189776f3eeb387c7ced2b9672608b` | 3455 | `cea5c8839fe193244cf0c826c51904eba7401c777ca8f1adad4f75ca22bc14de` |
| `tests/test_kernel.py` | `4cd487cae629135c134085e22787e055b16f94c9` | 3458 | `3632528e0ef39973ab0cfbc39db8b0cc40a773652e94c2848889d92d6c179087` |
| `verifier/audit.py` | `9f6064b3ae8dcd75b2171b766b6ad3883ad30d16` | 8835 | `3d7f6a426060ef054bb52fed1af4e0bf336e06ae4805879fa6f6bdf0460f91a1` |
| `verifier/axis_integer_grid.cpp` | `37701463136ba902486b1834f4e6ebfb8b1b1635` | 4143 | `f5bc3f60065aaea3d14ffb8465865750fca22cf8bbc6bd8739b5120200b6277d` |
| `verifier/continuous_pose.cpp` | `c4e351b3e245429912519eec259ea54c2af55fac` | 11075 | `da06206b8e83a57b8a710ba62e743c6d3a1959e9160ff32ae89ede583841c73c` |
| `verifier/exact.py` | `0080a026ed0a640c61c54c13a9777a5bcad5d13f` | 9899 | `41423a54d1c5ba2262bbf086f57fd03bd0457d9e35ddc8fdafb4b819b04e677e` |
| `verifier/run.py` | `ce80c21a6809b20b324ab6ccb78329d58d5bfefc` | 7609 | `a62978611fa2f4a57b8cab0f36051ed7cea62a6ac947274ddffcf606c76d7534` |

One file is pinned by digest and not copied: `certificate/original_density.json`
(332,847 bytes) is wand125’s pool, the bytes of the 2026-10-01 packet’s
`wand125-rectangles/certificates/rect_n40_L67/certified_candidate.json.gz`, which
`acquire_source --check` compares.
The `results/` the tree holds are the producer’s local run.

## The Release ZIP and Its CI Receipt

The ZIP holds the 35 files of the tree, of which 30 are byte-identical
([release-ci/zip-entries.sha256](release-ci/zip-entries.sha256) digests every entry).
The other five are its four `results/` files and the `SHA256SUMS` whose four lines name
them: the ZIP carries the receipt of GitHub Actions run
[38120568498](https://github.com/Guzhou0806/n40-square-packing/actions/runs/38120568498)
(`success` on `6a65957e`, 2026-10-11T07:12:07Z to 07:38:58Z) in place of the tree’s.
Both are kept and named for what they are:

| Receipt | Where | `source_commit` | Pose binary | Axis binary | Compiler | Python | Slab seconds | Full entry |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| producer’s local run | `source/results/` | null | `a5dcfa3e…` | `a3a82b57…` | GCC 15.2.0 | 3.14.4 | 2,655.3 | 858.95 s |
| CI run 38120568498 | `release-ci/results/` | `6a65957e…` | `69bc9e64…` | `19288b2f…` | GCC 13.3.0 | 3.12.3 | 5,229.5 | 1,587.30 s |

Both report four workers, 43 of 43 slabs `verified`, 60,500,889 nodes, 30,250,466
leaves, 13,812,428 angle bisections, the least leaf bound
$9005397816695287/2^{53} = 0.99980000020\ldots$, the axis minimum
$1001486431423867090847280653/10^{27}$ over $3293^2 = 10{,}843{,}849$ vertices, the
derived inputs `6c64a2d2…` (pose) and `10dd46b0…` (axis), and the dual
`EXACT_FAMILY_OBSTRUCTION` from both of its programs; every non-timing field of their 43
slab outputs and their axis output is identical.
The pose binaries are `T-145`’s (the CI one byte for byte); the axis binaries are new,
because `run.py` now builds the unchanged axis source with the pose kernel’s flags,
`-O3 -std=c++17 -fno-fast-math -ffp-contract=off`, in place of `-O2 -std=c++17`.
[release-ci/](release-ci) also keeps the ZIP’s `SHA256SUMS`, the release’s own digest
file, and the GitHub API records of the release and of the run (metadata only; the run’s
log was not read).

## What Was Checked Here

[`devtools.audit_n40_new_supports`](../../../devtools/audit_n40_new_supports.py) is a
first-party tool, written without opening the release’s `verifier/exact.py`,
`verifier/audit.py`, `obstruction/` programs or tests; its docstring is the read log.
Its receipts are in [receipts/](receipts).

**The finite audit** (`check`, [receipts/finite-audit.json](receipts/finite-audit.json),
`FINITE_STEPS_HOLD`, 68 checks, about ten seconds), in exact rationals on the retained
bytes.
After the orbit facts, its checks are the ones
[`devtools.audit_continuous_pose`](../../../devtools/audit_continuous_pose.py) makes of
`T-145`’s release, made of this one, not copies of them:

- The density’s orbits: 685 sites, all positive, 522 `inherited` and 163 `generated`;
  every box a proper rectangle in $K$; each inherited box equal to its `source_index`
  row of the pool exactly, no row used twice (427 of the 522 rows carried positive weight
  in `rect_n40_L67`, 95 were among its zero-weight candidates); no generated box
  D4-equivalent to any of the pool’s 2,526 rectangles; the 685 orbits pairwise distinct;
  the weights summing to $3999/100$.
- The expansion: 5,480 terms and 5,424 distinct rectangles, D4-invariant, integral $M$.
- Both kernel inputs regenerated from the retained density, in the release’s order, to the
  digests both receipts name: the pose input `6c64a2d2…`, whose 27,402 numbers each lie
  in a binary64 pair that brackets them (this release writes $B$ as a hexadecimal pair,
  where `T-145`’s wrote a decimal one), and the axis input `10dd46b0…`, 5,480 rows each
  dominated by its term, none dropped, quarter-turn invariant, of mass
  $M - 2.57 \times 10^{-6}$; the int128 guard
  $627444222088298915573283512797161984 < 2^{125}$; the $3293 \times 3293$ grid, of
  which the receipts’ minimiser $(3490012394, 6201340682)/10^9$ is a vertex; the
  dominated measure’s capture there, evaluated again in integers, equal to the axis
  minimum, and the density’s own capture there $1.0014864996\ldots$.
- The scalar chain: $X = L/B = 3359/500$, $217911/99764500$ above `T-145`;
  $40\tau - M = 1/500$; $L > B \cdot 1414213562373096/10^{15}$; $T^2 + 2T - 1 =
  89/40000$; the 44 endpoints partitioning $[10^{-6}, 83/200]$; the kernel’s threshold
  $\mathrm{up}(\mathrm{fl}(\tau))$ at least $\tau$, whose terms are inside the kernel’s
  input bounds, and the receipts’ least leaf bound at least that, by
  $2.0 \times 10^{-10}$; $B - AW(\varepsilon) =
  424025836324581/839750000000839750000000$, `PROOF.md`’s value; the axis minimum above
  $\tau$ by $1.69 \times 10^{-3}$.
- Every `parameters`, `scalar`, `admission`, `coverage` and `axis` block of both receipts,
  every slab row as the contract runs it (exit 0, an empty stderr, the inputs, source
  and binary it names), the fourteen control stages’ exits, and the 30 source digests
  each receipt lists, which are the manifest’s.
- The kernels: the five files this release keeps from `T-145`’s (both kernels, both
  harnesses and the oracle) are in both packets’ manifests with one digest, which their
  retained bytes here have, and are byte for byte `T-145`’s retained files; the CI run’s
  pose binary `69bc9e64…` is the one `T-145`’s CI receipt names and `T-145`’s replay
  rebuilt with the CI compiler.
- Controls, each refused: $A$ one step of $1/250000000$ larger (the near-axis
  containment fails); $\tau = 3999/4000$; $T = 41/100$; $\varepsilon = 10^{-5}$; a
  generated site moved onto a pool rectangle’s mirror image; one weight scaled by
  $99/100$; and a hundredth of one site’s weight moved to another, which keeps every
  orbit fact and the mass, so only the digests binding the density to both kernels’
  inputs refuse it.

**The axis stage** (`run-axis`, [receipts/axis-stage.json](receipts/axis-stage.json),
judged in [receipts/axis-check.json](receipts/axis-check.json), `AXIS_STAGE_HOLDS`):
the retained `verifier/axis_integer_grid.cpp`, built in a scratch tree as `run.py`
builds it, with `g++ (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0`, is `19288b2f…`, byte for
byte the CI run’s axis binary. On the derived input it printed `AXIS_COVERAGE_PROVED`,
every field equal to both receipts’, in 1.9 s; at $\tau = 1.001488$, just above the
minimum, it refused (`AXIS_TEST_REFUSED`, exit 2), and at $\tau = 1.001486$, just below,
it proved. `sqverify-fast`, built with `cargo build --release --locked -j 1` (rustc
1.98.0) from crate source `d97758bb…`, which `sqverify_fast_census --source-digest` names
as reviewed for declared nets, decided the near-axis statement a second way, on the new
685-orbit density itself, undominated, with its weights scaled by $5000/4999$ (mass
$199950/4999 < 40$; 5,424 distinct rectangles once expanded) and threshold 1: `verified`
by the exact axis-vertex sweep over 10,929,636 vertices, least certified
1.0016868361671276, in 2.8 s. That decision shares no code with the axis kernel and reads
the density itself rather than the dominated measure.
`check-axis` holds it to the input derived here from the retained density: the density
is the release’s candidate, `984fcd3a…`; the digest the record and the crate’s own
premises state, `192f5df6…`, is that input’s; and the premises name its $L$, $n$, 5,424
expanded rectangles and net.
It refuses an axis stage whose record lacks this decision unless it is told
`--without-crate`, and a judgement without it reports
`AXIS_KERNEL_HOLDS_WITHOUT_CRATE`, never `AXIS_STAGE_HOLDS`.

The `price` block of the finite audit priced the slabs from both receipts, scaled by
`T-145`’s replay here (1,854.9 CPU-seconds against its local receipt’s 1,891.8 and its
CI receipt’s 3,693.3): about 2,630 CPU-seconds, 0.74 CPU-hours, with the longest slab
about 164 s. The replay below measured 5,242.6 CPU-seconds.

## The Replay Here

On 12 October 2026 the complete replay ran, by `run-replay`, which drives
[`devtools.audit_continuous_pose`](../../../devtools/audit_continuous_pose.py)’s runner
and judge with this release’s contract (its `Replay` record: this density, both
receipts’ totals, control H’s thresholds either side of this axis minimum, control G’s
mutant in this release’s `exact.py`) and adds a stage for the release’s two dual
programs; `check-replay` judges the receipts and must print `REPLAY_HOLDS`, and its
output is [receipts/replay-check.json](receipts/replay-check.json), 70
checks.
The 10 October review’s contract is what ran, at the new parameters; the mathematical
review of this release is
[review-2026-10-12-n40-new-supports-6718.md](../../../../docs/project/reviews/review-2026-10-12-n40-new-supports-6718.md).
The runs were on a 4-core x86-64 Linux container shared with other work, at a one-minute
load average between 7.6 and 27.0, with at most two worker processes.

**The builds** ([receipts/builds.json](receipts/builds.json)): the retained
`verifier/continuous_pose.cpp`, `verifier/axis_integer_grid.cpp` and
`tests/rounding_harness.cpp` copied to their upstream paths in a scratch tree and built
there with relative paths as `run.py` builds them, both kernels at
`-O3 -std=c++17 -fno-fast-math -ffp-contract=off`, by
`g++ (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0`, the CI run’s compiler: the pose binary
`69bc9e6485102d3636db5377884ba6304f749be94d6ca913d82d80108f1ed4ab` (`T-145`’s, and the
CI run’s) and the axis binary
`19288b2f9bcb1cfa86a0bde9db1e1fbb79d43dc8044bc7243af8f6ad405899af` (the CI run’s), byte
for byte; the rounding harness `81f15ab0…`, which no receipt names.

| Contract | Here |
| --- | --- |
| **3.** `axis axis-input.txt`: `AXIS_COVERAGE_PROVED`, 3,293 nodes per axis, minimum `1001486431423867090847280653` at scale $10^{27}$, minimiser `3490012394, 6201340682`, `direct_sum_matches`, evaluation bound `627444222088298915573283512797161984` | the same, every field equal to both receipts’, exit 0, 7.0 s ([receipts/axis-run.json](receipts/axis-run.json)) |
| **3.** `sqverify-fast --candidate axis-A.json --n 40 --side 67/10 --directions 0 --threshold 1 --threads 1 --confirm` on the 685 rows scaled by $5000/4999$, input `192f5df6…` | `verified`, `axis-vertex-sweep`, 10,929,636 vertices, least certified 1.0016868361671276, the axis stage’s decision of 11 October again, 2.9 s |
| **4.** the 43 slabs, `continuous PL PH 1000000 4999 5000 30000000` over the consecutive endpoints, each `verified`, exit 0, every non-timing field equal to `results/slabs.jsonl` | all 43, against both the local and the CI receipt ([receipts/slabs.jsonl.gz](receipts/slabs.jsonl.gz)) |
| **4.** 60,500,889 nodes, 30,250,466 leaves, 13,812,428 angle splits, least `lower_bound` $9005397816695287/2^{53}$ at slab 40 | the same; $2.0 \times 10^{-10}$ above $\tau$; every slab’s nodes $= 2\,\text{leaves} - 1$ |
| **4.** price: about 2,630 CPU-seconds, 22 minutes on two workers | 5,242.6 CPU-seconds and 12,629 s of wall time on two workers under the shared load (slab 0 took 68.6, slab 1 322.1 and slab 42 134.0 CPU-seconds, against the local receipt’s 32.8, 158.6 and 66.0 and the CI receipt’s 67.6, 327.3 and 104.6) |
| **6.** `sqverify-fast` on the same rows at side $B = 3350/3359$, `D` $83/80000$, `angle_count` 401 (input `c458f7adc0b5529bcc70b4ceb877957950ad77270a55b3c2cf73e8dedc44b71f`), all directions, threshold 1, two threads | `VERIFIED`, 401 of 401, no direction refused, 35,375,590 boxes, least certified 1.000000000310131 at $r = 398$; at $r = 0$, the exact axis-vertex sweep at side $B$, least 1.001700339663363; 1,782.6 s of wall time and 720.9 CPU-seconds at two threads under the shared load ([receipts/crate-runs.json.gz](receipts/crate-runs.json.gz)) |

The crate was built with `cargo build --release --locked -j 1` at rustc 1.98.0 (88d9e12ae 2026-08-18), the toolchain the crate pins from crate
source `d97758bb…`, which `sqverify_fast_census --source-digest` names as reviewed source
for declared nets; the binary is `567a0fd58f7ae4e981580f2a90bed5c92ac44fa8f3ebb442b166e93043c15ed4`.

**5. Controls**, each as the contract states it at this release’s parameters, on the
binaries above ([receipts/controls.jsonl.gz](receipts/controls.jsonl.gz) and
[receipts/control-G-release.json](receipts/control-G-release.json)):

| Control | Contract | Here |
| --- | --- | --- |
| A | the release’s `synthetic-negative` (uniform density $1/2$, slab `[1,415000]`, budget 10,000) and `limited-budget` (pose input, slab `[100000,110000]`, budget 1): exit 3, `unresolved` | exit 3, `unresolved`, at 83 and 1 nodes; the release’s `synthetic-positive` (density 2) beside them, `verified` at 117 |
| B | uniform $\rho = \tau(1 - 10^{-9})/B^2$ on $K$: exit 3 within 100 nodes | three slabs, `[1,500]`, `[100000,110000]`, `[410000,415000]`, on the full budget: exit 3 at 92, 87 and 89 nodes |
| C | density $\rho$ on $K$ less a strip of depth $h$ at the top or the right, scaled so the least capture, at the slab’s left end, is $\tau(1 - 10^{-9})$: exit 3 | the review’s seven slab–depth pairs, both regimes: all 14 exit 3, budget 1,500,000; the two on `[410000,415000]` by the budget, the rest at the width floor |
| D | density off a gap $[0, L] \times [L/2 \pm 1/200]$, least capture $\tau(1 - 10^{-9})$ at the slab’s right end: exit 3 | five slabs: all exit 3, four by the budget of 1,500,000 |
| E | C’s densities at $\tau(1 + 10^{-4})$; D’s at about $\tau(1 + 3.4 \times 10^{-4})$ on `[400000,410000]`: `verified` within 260,000 and 141,000 nodes | all 14 cuts `verified`, the largest at 251,857 nodes; the gap `verified` at 140,819 |
| F | `ieee-neighbors`, `wrong-rounding`, `ftz`, `reject-ndebug`, `reject-fastmath`: exit 0, $-6$, $-6$, 1, 1 | the same: 1,000,008 values `PASSED`; the rounding and MXCSR assertions fire; both compilations stop at the kernel’s `#error` |
| G | $A$ replaced by $249329660/250000000$, one step larger: `exact.py` refuses `NEAR_AXIS_CONTAINMENT` | the release’s `scalar()`, run on a scratch copy of `exact.py` with that one value changed, refuses `NEAR_AXIS_CONTAINMENT`, and on the unchanged copy returns both receipts’ scalar block |
| H | $\tau = 62593/62500$ in the axis header, just above the minimum: `AXIS_TEST_REFUSED`, exit 2 | refused, exit 2; $\tau = 500743/500000$, just below, proved; the contract’s $1/2$, below the minimum, proved |

**The duals** ([receipts/duals.json](receipts/duals.json)): the release’s
`obstruction/run.py`, its own entry point for `OBSTRUCTION.md`, ran on a scratch copy of
the retained tree at its upstream paths with the pinned pool restored from the
2026-10-01 packet, every file the manifest’s, under the project interpreter and `g++`
13.3.0 with Boost 1.83 headers: the Python `Fraction` program and the C++ Boost program
both `EXACT_FAMILY_OBSTRUCTION`, column 201, score
$24998348431654956215746/1000000000003000000000000$, slack `66062736801751370160`, the
one-pose false dual refused (exit 2), `EXACT_DUAL_CODE_DISTINCT_CHECKED`; every
non-timing field equal to both receipts’, in 703.0 s; the dual binary
`d5ecc193a842c21e86281c7facdc4f92a70cec92a28f5f7e002ed5d3a77cf51c`, byte for byte the CI run’s. The result is a statement about the original support family and bears
on no bound.

**What the checkers share.** The continuous cover and the axis certificate were decided
by the release’s own kernels, rebuilt from the retained source into the CI run’s
binaries: the replay reproduces the producer’s run with the producer’s code.
The near-axis statement was decided a second time by `sqverify-fast`, which shares no
code with the axis kernel and reads the density itself rather than the dominated
measure.
The finite steps were re-implemented here apart from `exact.py`; the two share the
density’s definition, its D4 expansion, the kernels’ input order, the enclosure rule and
the inward rounding, and nothing else.
`exact.py` was searched for the one string control G mutates, after the finite audit was
written, and not otherwise read by the tool’s authors.

## What Is Not Established

No second method decided the continuous cover (GC-4 of the 10 October review, GN-4 of
the 12 October review): nothing in this repository covers the pose domain with the angle
as an interval dimension, and the 401-direction run of `sqverify-fast` is a necessary
condition the claim passed, not the claim.
The kernels’ lemmas rest on the 10 October review of `T-145`, which read the same bytes;
how the new density was found (the dual pricing and the rationalized weights) is outside
every check, which needs only the density as it stands.
wand125’s comment of 2026-10-11T17:14:50Z on the issue, edited 2026-10-12T02:19Z,
reports a fresh run of the release’s entry point (`COMPLETE`, `REPLAYED_SAME_KERNEL`,
every count equal) and a continuous-angle verifier of his own, since published at
`wand125/square-packing` `f30cc2cf` (`tools/sqverify_continuous`, v3), that verified the
density in 86 roots; it publishes no receipt, so it is a third party’s report and not
retained here as a replay (bead `think-xzob` holds the read of that commit).
The release’s `tests/test_kernel.py` and `tests/test_admission.py` were not run here.
No packing, optimality or priority is claimed by the source or established here.

## Credit and Licence

The new material is Guzhou0806’s under the MIT licence (`LICENSE`, copyright 2026
Guzhou0806). `SOURCES.md` credits the original density and candidate rectangles to
wand125 (pinned at `wand125/square-packing-bounds` `1a25a5ed…`), the translation-derivative
structure to Tokoharu’s rectangle-density method, says the concave-section calculations
“draw on Joshua Levy’s Squares Project” (pinned at `ef79288a4`), and names prior measure
and unavoidable-set work by Stromquist, Burns and Massaccesi.
It gives Guzhou0806’s AI-assisted contributions as “new supports, weight optimization,
the continuous-cover certificate and the exact obstruction for the full original support
family”, and says “AI assisted mathematical exploration, code, tests, proof writing and
publication preparation”.
The density’s MIT licence is retained in `licenses/wand125.txt`, Tokoharu’s in
`licenses/tokoharu.txt` and this repository’s in `licenses/jlevy-squares.txt`.
The comment asks the record to “credit new supports, reweighting, the 6.718 certificate
and the full-source-family obstruction to Guzhou0806, AI-assisted, retaining wand125’s
credit for the original density/pool, Tokoharu’s for the density/translation-derivative
method and Joshua Levy / the Squares Project’s for concave-section inspiration”.

## Compressed Files

The two upstream data files of more than 1,000 lines are stored as deterministic gzip;
`gunzip -k` restores each beside it.

| Stored file | Origin | Git blob (decompressed) | SHA-256 (decompressed) |
| --- | --- | --- | --- |
| `source/certificate/certified_candidate.json.gz` | upstream | `34b9e12db7add79fd0f809cade8dc1864844f146` | `984fcd3acc605fe3c50a84912eed77e0192ca5b7253b19b6aa31a4e28e1bf5c2` |
| `source/obstruction/certificate.json.gz` | upstream | `82774999cec21733f21c886e4b76eef0adafd429` | `f4edfa9a08efaffe8916d3da2c2a8ff567489a2185319de742e8b9e97e3939f9` |
| `receipts/slabs.jsonl.gz` | receipt | `7267a43204594b1aeefb96ba0075c28181dfe6ad` | `a0839747c0940d12cd179ebe711fabe9701c5f7e1a6d9108d6996ab0b9511477` |
| `receipts/controls.jsonl.gz` | receipt | `7c12faf25da807e5f8cfeb1a3199462e974b4879` | `1705375a324946c543618f87ea8f802880cd8ae89a48ee3f4b4bc5a2011f0e12` |
| `receipts/crate-runs.json.gz` | receipt | `3b7551f814a3629dbbc15e5cbfb7833bd8f98936` | `85a5949ea99981a8bd55ab123522de0af675ff161563679fc377053319ebc705` |

The other receipts are plain JSON: `finite-audit.json` from `check`, `axis-stage.json`
from `run-axis`, `axis-check.json` from `check-axis`, and from `run-replay`
`builds.json` (the compiler, each build’s command, exit, wall and binary digest),
`axis-run.json`, `control-G-release.json` and `duals.json`; `replay-check.json` is
`check-replay`’s judgement of them all.

## Commands

From `packing/`, each after `uv run --frozen --all-extras --group dev`:

```sh
python -m devtools.acquire_source guzhou-n40-new-supports-2026-10-11 --check
python -m devtools.audit_n40_new_supports check
python -m devtools.audit_n40_new_supports check-axis
python -m devtools.audit_n40_new_supports derive --out SCRATCH
python -m devtools.audit_n40_new_supports run-axis --out SCRATCH \
    --crate-binary sqverify_fast/target/release/sqverify-fast
python -m devtools.audit_n40_new_supports run-replay --out SCRATCH --workers 2 \
    --crate-binary sqverify_fast/target/release/sqverify-fast
python -m devtools.audit_n40_new_supports check-replay [--receipts SCRATCH/receipts]
```

`check`, `check-axis` and `check-replay` read the retained files only, and their
`--output` equals `receipts/finite-audit.json`, `receipts/axis-check.json` and
`receipts/replay-check.json`; `run-axis` needs `g++` and a crate build of reviewed
source, and takes seconds; `run-replay` needs those, the Boost headers for its `duals`
stage, and about 1.5 CPU-hours, most of it the 43 slabs, which `--stages`
splits as `devtools.audit_continuous_pose run` does (`duals` is this release’s own
stage).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
