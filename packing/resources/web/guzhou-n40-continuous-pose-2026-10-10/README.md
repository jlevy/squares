# Guzhou0806’s Continuous-Pose Kernel: s(40) > 1340000/199529 on wand125’s Density

Guzhou0806’s comment of 2026-10-10T14:50:00Z on
[issue #485](https://github.com/jlevy/squares/issues/485#issuecomment-6098734391) reports a
lower bound for $n = 40$, unrestricted rotations, from
[Guzhou0806/n40-square-packing](https://github.com/Guzhou0806/n40-square-packing/tree/71c97d07553d7d5ff5c5c82f0c9d1c75a150a4e3)
at `71c97d07553d7d5ff5c5c82f0c9d1c75a150a4e3` (tree
`11280a385872af75e7f5a181a89580e977282a6f`, committed 2026-10-10T14:30:28Z), which the
release tag `n40-continuous-1340000-199529-20261010` names.
The commit descends from `e5abeb4d`, the pin of the
[clipped-corner packet](../guzhou-n40-clipped-corner-2026-10-10/README.md) that retains
`T-133`’s $s(40) > 335427/50000$.

| Bound | Exact form | What it rests on |
| --- | --- | --- |
| $s(40) > 1340000/199529 = 6.715815746082023\ldots$ | strict | every side-$B$ square in $K$ captures at least $\tau$: the continuous kernel over 43 slabs for $t \in [10^{-6}, 83/200]$ and the axis kernel at side $A$ for $t \in [0, 10^{-6}]$; then $40\tau - M = 1/500$ |

Here $K = [0, 67/10]^2$, $B = 199529/200000$, $\tau = 4999/5000$, $M = 3999/100$,
$A = 997643/1000000$ and $t = \tan(\theta/2)$.
The bound raises `T-133`’s by exactly $72586117/9976450000$.
The density is wand125’s `rect_n40_L67`, the one the
[2026-10-01 rectangle packet](../wand125-rectangle-certificates-2026-10-01/README.md)
retains for `T-068`’s $s(40) \ge 67/10$; the source’s copy is byte for byte the same
(SHA-256 `71011d0356dd179c6e7e6e02c9a064ff30f6f13844016ce3b97463bf7ef53dc0`), so this is
a second extension of a certificate the record already holds, not a new density.
The argument is in the source’s `PROOF.md`; the mathematical review is
[review-2026-10-10-guzhou-n40-continuous-pose-bound.md](../../../../docs/project/reviews/review-2026-10-10-guzhou-n40-continuous-pose-bound.md),
which found no blocking defect and wrote the replay contract this packet’s receipts
answer.

The release `n40-continuous-1340000-199529-20261010` was published 2026-10-10T14:49:22Z
with one archive, `n40-continuous-1340000-199529.zip`, 129,976 bytes, SHA-256
`78d693ae5bd08cc3065348c6593c2bec36412bebe48eb2f744786dc115bba26f`, the comment’s, and
its digest file `n40-continuous-1340000-199529.zip.sha256`.
The sources were retrieved at 2026-10-10T17:25Z.

## Retained Here

`devtools.acquire_source` wrote [`source/`](source) from a full clone checked out at the
pin, from the declaration in [acquisition/declaration.json](acquisition/declaration.json);
every file is bound to its Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest
of all 28 files of the tree (487,953 bytes).
The source’s own `SHA256SUMS` holds for every one of its 27 lines in the tree and in the
ZIP.

Twenty-seven files are retained (155,106 bytes):

| Upstream path | Git blob | Bytes | SHA-256 |
| --- | --- | --- | --- |
| `.gitattributes` | `1f9683ba325ebf468c324187e140a55c0eb25523` | 58 | `2d5c072f5cbe11a4c74660a6e47beffcf246fc3546a5aaa534b21c724fe2f9fc` |
| `.github/workflows/verify.yml` | `616194be8ca8d5a3dd6fb1080d7fde01c277d84e` | 1346 | `9c209614911a6adc4f1e7f496fa62b5a91255f0034efd8c314aaa8a1f674907a` |
| `.gitignore` | `5ef9f3a66a0b531e7d6dc905a2e9e482d19473f5` | 37 | `85e9e61c0a8dee51b98253a262d7a2f3f8fe29badf2d145a68b510bdd330b7f5` |
| `LICENSE` | `654ff03eb31bc71611c2a709767d2044d88af0cf` | 1067 | `94be33291ae276999b6f49d7ebc3ed2d35e11e61e2fcd443f810178c09a2fad9` |
| `PROOF.md` | `c7cecc853c70eb7e67095ea275dbb53117962490` | 21961 | `6fc34dff6ccd9bd8a3aa1703baf200f2cde75f3151759f8c76186fe4214e5856` |
| `README.md` | `e4b2e4e97d8cffe7bd0b7e97551d0244249c6a79` | 2289 | `49b16634ff28668272fb8201667c4a1d635ea3391c30e417286385446891fc21` |
| `REPRODUCIBILITY.md` | `4eed62523a57dbe681d0d0b3eee0896ee3d4c5b3` | 3542 | `99abb5ff99a3575badb752fe971950264ddbf9e93497edee07e3f3c9c39f6b04` |
| `SHA256SUMS` | `6aa67c983c0ba0091d664a71e5bf5586879e2ffc` | 2334 | `33441e09c3eca25817cdbdb727aa25a54cc092292a207645dc5d0e0524172d14` |
| `SOURCES.md` | `9880a2959a733f40f4f654d061802e063abfc7f7` | 3887 | `76d52c1c9957d1993d3d891fa94f17b137595582b684ce506fc9915ef2792cb3` |
| `VERIFICATION.md` | `7ffd8d5e952c2282e8d84be28fdd40a999e4d74b` | 3849 | `f4372132f34829fe1e167fe03add00f03a60fa30a28d4e598fffddabc0edda71` |
| `certificate/parameters.json` | `5370d34381975bc5c8dd28e50abf76d34e513a5b` | 795 | `4d153cb377a84e52333cbd76facb7a7a48ee586ea2567b5ac5d397ab7d9407c5` |
| `licenses/jlevy-squares.txt` | `239dffb892be26bfe17991b8396ae78ad9235cee` | 21153 | `7428341239cf4ee78c4b951b7fd8a2284b24835aeb0ede82f032b2e95e92cc00` |
| `licenses/tokoharu.txt` | `3b9a49cd1e449395373f48106c357e63cc2ed683` | 1065 | `8dc3364f10709e043998e74d0de02774a7f6c9b08dde3a8a58336948d9ed8ad8` |
| `licenses/wand125.txt` | `bbfbff131ef8ccbba5ed8b8b395f2c457eb8922c` | 1064 | `c0dd43e7892932c81335f74a2fdbf1a98f5977bab14c0c4c30e3abcc97c34904` |
| `results/axis.json` | `711e44909020c565f336bc065b5eced29a7d54cf` | 718 | `041ac9d9f1f2cbae17b642f41f67beaddb4974247dcd93d083c99a38ad1e7b9c` |
| `results/slabs.jsonl` | `19a78691652afba55d600ed4398f211692a591db` | 33429 | `4fb7708313eebe540d7674c62d3352e5e1be0b1ea777067346b117dfe4b123f0` |
| `results/verification.json` | `e49a341c6f7373ebad8a27e7258f991636a786cf` | 10288 | `e465f7656f53779cfaece7b14ea148b0a1a83ba05c6b8a529b70db71940b97f7` |
| `tests/kernel_harness.cpp` | `20082196d8721819d007c2c2bf5e6a2ed8e3c19f` | 888 | `4ee681bced642c708eda7d71845836d3ea18d61c350ff49ef26e199fb9ee6e40` |
| `tests/oracle.py` | `3e36d5811b35c772dfc875c6bc1ddccbf51b869c` | 1073 | `395fa622bec60607798a3da4103162313833fe9c139a40ca2023cd00c14d581e` |
| `tests/rounding_harness.cpp` | `c43913a913d546d3a2d78ad4f385675d70bb1f81` | 1161 | `96bd022242b4c0e44ff3eb27a8294d3d359bc74263f898e350768eeb78fdfc9f` |
| `tests/test_admission.py` | `cbc969e093cfc1647e7cfbe3ee66d82f11516e13` | 3146 | `797689e9f891e59d6f8caea9d691cfb81606378e401e8489881fde19f13f632c` |
| `tests/test_kernel.py` | `21db83602b9e69c8a9d784099e6929d95c6dbbed` | 3475 | `6963d2ef8b0d16f1aa41b31f9091b2185be8630c03994bf66ac97105d7299aa5` |
| `verifier/audit.py` | `ed448328c0103d337c2fbc6c244acffb7f846b39` | 7129 | `9ecbabfc483b181d21dc2a298d5c35b228218176eba97dcf856113238348281e` |
| `verifier/axis_integer_grid.cpp` | `37701463136ba902486b1834f4e6ebfb8b1b1635` | 4143 | `f5bc3f60065aaea3d14ffb8465865750fca22cf8bbc6bd8739b5120200b6277d` |
| `verifier/continuous_pose.cpp` | `c4e351b3e245429912519eec259ea54c2af55fac` | 11075 | `da06206b8e83a57b8a710ba62e743c6d3a1959e9160ff32ae89ede583841c73c` |
| `verifier/exact.py` | `a92be31b718e40c3c9faaa8893ffc0e662385daa` | 7151 | `3e2aa3ca8e324a39e018ccb28267606344a9de585d72f43d79d80663b7c312cf` |
| `verifier/run.py` | `27830a226941fa653d987d86d9b05aaa46439936` | 6983 | `3387697cfba17021242b06e06d11df7975c72f5cca97a276cf758fea7e187ba6` |

One file is pinned by digest and not copied: `certificate/certified_candidate.json`
(332,847 bytes) is wand125’s density, the bytes of the 2026-10-01 packet’s
`wand125-rectangles/certificates/rect_n40_L67/certified_candidate.json.gz`, which
`acquire_source --check` compares.
The two kernels’ sources are the digests the release names as frozen: `da06206b…` for
`verifier/continuous_pose.cpp` and `f5bc3f60…` for `verifier/axis_integer_grid.cpp`.
The `results/` the tree holds are the producer’s local run (GC-3 of the review).

## The Release ZIP and Its CI Receipt

The ZIP holds the 28 files of the tree, of which 24 are byte-identical
([release-ci/zip-entries.sha256](release-ci/zip-entries.sha256) digests every entry).
The other four are its three `results/` files and the `SHA256SUMS` whose three lines name
them: the ZIP carries the receipt of GitHub Actions run
[38059878931](https://github.com/Guzhou0806/n40-square-packing/actions/runs/38059878931)
(`success` on `71c97d07`, 2026-10-10T14:30:32Z to 14:47:05Z) in place of the tree’s.
Both are kept and named for what they are:

| Receipt | Where | `verification.json` | `slabs.jsonl` | `axis.json` | `source_commit` | Pose binary | Axis binary | Compiler | Python | Wall |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| producer’s local run | `source/results/` | `e465f765…` | `4fb77083…` | `041ac9d9…` | null | `a5dcfa3e…` | `051e306d…` | GCC 15.2.0 | 3.14.4 | 510.96 s |
| CI run 38059878931 | `release-ci/results/` | `575a5860…` | `24d16b52…` | `3ace101e…` | `71c97d07…` | `69bc9e64…` | `cccecb9a…` | GCC 13.3.0 | 3.12.3 | 983.95 s |

Both report four workers, 43 of 43 slabs `verified`, 61,860,927 nodes, 30,930,485
leaves, 14,096,668 angle bisections, the least leaf bound
$2251349454150741/2^{51} = 0.99980000019017\ldots$, the axis minimum
$249950896232809301864786207/(25 \cdot 10^{25})$ over $2213^2 = 4{,}897{,}369$
vertices, and the derived inputs `ccf7b68a…` (pose) and `d57e8bb2…` (axis); every
non-timing field of their 43 slab outputs and their axis output is identical.
[release-ci/](release-ci) also keeps the ZIP’s `SHA256SUMS` (`ac8bd643…`), the
release’s own digest file, and the GitHub API records of the release and of the run
(metadata only; the run’s log was not read).

## The Replay Here

The review’s replay contract has seven parts, and each ran here by
[`devtools.audit_continuous_pose`](../../../devtools/audit_continuous_pose.py), a
first-party tool whose finite checks share no code with the release’s `verifier/exact.py`.
Its receipts are in [receipts/](receipts).
The runs were on a 4-core x86-64 Linux container shared with other work, at a one-minute
load average between 3.0 and 18.0, with at most two worker processes.

**0. Retention** is the two sections above.

**1. The derived inputs.** `derive` regenerated both kernel inputs from the retained
candidate: the pose input, `L` as a hexadecimal pair, `B` as a 17-digit decimal pair, then
the 3,840 terms of the D4 expansion in the release’s order, each value as a binary64 pair
that brackets it; and the axis input, the same terms in quarter-turn order rounded inward to
the $10^{-9}$ grid, under the header `6700000000 997643000 1000000000 1000000000 4999 5000
3840`. Their SHA-256 are
`ccf7b68aa89fdcfcf0d78ac135cfa24e4a73b822eb412b2aac46e9c49e2b9925` and
`d57e8bb267dc1a17d57fa0f17f662bf552b6aef46427a0eb9308ae16539ed1cb`, the digests both
release receipts bind; all 19,202 numbers of the pose input bracket their rationals, and
the axis input’s 3,840 rows are each dominated by their term, none dropped, quarter-turn
invariant, of mass $M - 4.10 \times 10^{-6}$.

**2. The builds.** The tool copies the retained `verifier/continuous_pose.cpp`,
`verifier/axis_integer_grid.cpp` and `tests/rounding_harness.cpp` to their upstream paths
in a scratch tree, checks each against the manifest, and builds there with relative paths,
as the release’s runner does:

```text
g++ -O3 -std=c++17 -fno-fast-math -ffp-contract=off verifier/continuous_pose.cpp -o continuous
g++ -O2 -std=c++17 verifier/axis_integer_grid.cpp -o axis
g++ -O3 -std=c++17 -fno-fast-math -ffp-contract=off -I verifier tests/rounding_harness.cpp -o rounding
```

With `g++ (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0`, the CI run’s compiler, the pose
binary is `69bc9e6485102d3636db5377884ba6304f749be94d6ca913d82d80108f1ed4ab` and the axis
binary `cccecb9ab1ca0ecd88b0994c04ebf7965cf0982b7e400966702da6f7e893265c`, byte for byte
the CI run’s; the rounding harness, which no receipt names, is `81f15ab0…`.

| Contract | Here |
| --- | --- |
| **3.** `axis axis-input.txt`: `AXIS_COVERAGE_PROVED`, 2,213 nodes per axis, minimum `999803584931237207459144828` at scale $10^{27}$, minimiser `4207731377, 6201178500`, `direct_sum_matches`, evaluation bound `384178892657373682994447839008000000`, under a second | the same, every field equal to both receipts’, exit 0, 0.30 s; the finite audit evaluated the dominated measure’s capture at that minimiser again, in integers, and it equals the minimum |
| **3.** `sqverify-fast --candidate axis-A.json --n 40 --side 67/10 --directions 0 --threshold 1 --threads 1 --confirm` on input `379193ff…`: `verified`, `axis-vertex-sweep`, 4,897,369 vertices, least certified 1.0000037044548487 | the same, exit 0, 0.53 s, argmin $(2103865688632621/(5 \cdot 10^{14}),\ 12402357/(2 \cdot 10^{6}))$, the breakpoint of the kernel’s minimiser on the original density; the summary reads `PARTIAL`, since one direction of the net was asked |
| **4.** the 43 slabs, `continuous PL PH 1000000 4999 5000 30000000` over the consecutive endpoints, each `verified`, exit 0, every non-timing field equal to `results/slabs.jsonl` | all 43, against both the local and the CI receipt |
| **4.** 61,860,927 nodes, 30,930,485 leaves, 14,096,668 angle splits, least `lower_bound` 0.99980000019017234 at slab 1 | the same; $2251349454150741/2^{51}$, $1.9 \times 10^{-10}$ above $\tau$; every slab’s nodes $= 2\,\text{leaves} - 1$ |
| **4.** price: about 16 minutes on two workers | 1,364 s of wall time on two workers, 1,854.9 CPU-seconds (the local receipt’s slab time is 1,891.8 s); slab 0 took 21.4, slab 1 86.6 and slab 42 57.8 CPU-seconds, against the receipts’ 22.0, 87.5 and 55.6 s |
| **6.** `sqverify-fast` on input `94c3ab2e…` (`B` `199529/200000`, `D` `83/80000`, `angle_count` 401), all directions, threshold 1: `VERIFIED`, 401 of 401, least certified 1.000000000357051 at $r = 289$, 32,763,798 boxes, about three minutes at two threads | the same, exit 0, 313.6 s of wall time and 295.1 CPU-seconds at two threads; $r = 0$ by the axis sweep at side $B$, least 1.000091413240477 |

The crate was built with `cargo build --release --locked -j 2` at rustc 1.98.0
(`88d9e12ae` 2026-08-18) from crate source `d97758bb…`, which `sqverify_fast_census
--source-digest` names as reviewed source for declared nets (`910b6b12c`); the binary is
`567a0fd58f7ae4e981580f2a90bed5c92ac44fa8f3ebb442b166e93043c15ed4`, the reviewed build.
Both crate inputs carry the 480 positive rows with their weights scaled by $5000/4999$
(mass $199950/4999 < 40$) and threshold 1, the same statement as capture at least $\tau$
of the original density (GC-4).

**5. Controls**, each as the contract states it, on the binaries above:

| Control | Contract | Here |
| --- | --- | --- |
| A | the release’s `synthetic-negative` (uniform density $1/2$, slab `[1,415000]`, budget 10,000) and `limited-budget` (pose input, slab `[100000,110000]`, budget 1): exit 3, `unresolved` | exit 3, `unresolved`, at 83 and 1 nodes; the release’s `synthetic-positive` (density 2) beside them, `verified` |
| B | uniform $\rho = \tau(1 - 10^{-9})/B^2$ on $K$: exit 3 within 100 nodes | three slabs, `[1,500]`, `[100000,110000]`, `[410000,415000]`, on the full budget: exit 3 at 92, 87 and 89 nodes |
| C | density $\rho$ on $K$ less a strip of depth $h$ at the top, scaled so the least capture, at the slab’s left end, is $\tau(1 - 10^{-9})$: exit 3 | the review’s seven slab–depth pairs, top and right cuts, both regimes: all 14 exit 3, budget 1,500,000; the two on `[410000,415000]` by the budget, the rest at the width floor |
| D | density off a gap $[0, L] \times [L/2 \pm 1/200]$, least capture $\tau(1 - 10^{-9})$ at the slab’s right end: exit 3 | five slabs: all exit 3, four by the budget of 1,500,000 |
| E | C’s densities at $\tau(1 + 10^{-4})$; D’s at $\tau(1 + 10^{-4} + \text{spread})$, about $\tau(1 + 3.4 \times 10^{-4})$, on `[400000,410000]`: `verified` within 260,000 and 141,000 nodes | all 14 cuts `verified`, the largest at 251,829 nodes; the gap `verified` at 140,859 |
| F | `ieee-neighbors`, `wrong-rounding`, `ftz`, `reject-ndebug`, `reject-fastmath`: exit 0, $-6$, $-6$, 1, 1 | the same: 1,000,008 values `PASSED`; the rounding and MXCSR assertions fire; both compilations stop at the kernel’s `#error` |
| G | $A$ replaced by $997644/10^6$: `exact.py` refuses `NEAR_AXIS_CONTAINMENT` | the release’s `scalar()`, run on a scratch copy of `exact.py` with that one value changed, refuses `NEAR_AXIS_CONTAINMENT`, and on the unchanged copy returns both receipts’ scalar block; the finite audit refuses the same mutant, $AW(\varepsilon) - B = 9.95 \times 10^{-7}$ |
| H | $\tau = 1/2$ in the axis header: `AXIS_TEST_REFUSED`, exit 2 | as written this control is admitted, `AXIS_COVERAGE_PROVED`, exit 0, since $1/2$ is below the minimum; the refusal it was meant to show ran at $\tau = 999804/10^6$, just above the minimum: `AXIS_TEST_REFUSED`, exit 2, beside $999803/10^6$, just below it, proved |

A budget exit is `unresolved`, never an acceptance (GC-5).
Controls B to E are regression controls of the kind GC-8 describes, with the least
capture known in closed form; none is a second decision of the cover.

**The finite steps.** `check` decides in exact rationals, on the retained density: 480
rows, 3,840 terms and 3,792 distinct rectangles, D4 invariance, $\int g = M$; both inputs’
identity, enclosures and dominated measure as above; $X = L/B = 1340000/199529$ and the
raise over `T-133`, $72586117/9976450000$; $40\tau - M = 1/500$; $L > B \cdot
1414213562373096/10^{15}$ with that bound’s square above 2; $T^2 + 2T - 1 = 89/40000$
and $T \le 1/2$; the 44 endpoints partitioning $[10^{-6}, 83/200]$; the kernel’s
threshold $\mathrm{up}(\mathrm{fl}(4999/5000))$ at least $\tau$, by
$1.33 \times 10^{-16}$; the receipts’ least leaf bound at least that threshold;
$W(\varepsilon) \ge 1$, $A \le B$ and $B - AW(\varepsilon) =
589499411/125000000000125000$; the axis minimum at least $\lceil 10^{27}\tau \rceil$, by
$3.58 \times 10^{-6}$, the int128 guards and the $2213 \times 2213$ grid.
Every value equals the `scalar`, `admission`, `coverage` and `axis` blocks of both
release receipts, every slab row of both is the contract’s run, and the source digests
both receipts list are the retained files’.
It refuses four altered parameters: G, the contract’s; $\tau = 3999/4000$, where
$40\tau = M$; $T = 41/100$, short of $\pi/4$; and $\varepsilon = 10^{-5}$, where
$AW(\varepsilon) > B$.

**What the checkers share.** The continuous cover and the axis certificate were decided
by the release’s own kernels, rebuilt from the retained source into the CI run’s binaries:
the replay reproduces the producer’s run with the producer’s code.
The near-axis statement was decided a second time by `sqverify-fast`, which shares no code
with the axis kernel and reads the original density rather than the dominated one.
The finite steps were re-implemented here apart from `exact.py`; the two share the
density’s definition, its D4 expansion, the kernels’ input order, the enclosure rule and
the inward rounding, and nothing else.
`exact.py` was opened only after the finite audit was written, to run control G on it.

## What Is Not Established

No second method decided the continuous cover (GC-4): nothing in this repository covers
the pose domain with the angle as an interval dimension, and the 401-direction run of
`sqverify-fast` is a necessary condition the claim passed, not the claim.
The kernel’s lemmas rest on the 10 October review, which re-derived them and read the
kernel line by line; its arithmetic rests on IEEE-754 round-to-nearest without fused
multiply-add or flush-to-zero, which the kernel asserts where it can, and on GCC
honouring `-fno-fast-math -ffp-contract=off` at `-O3`.
The release’s `tests/test_kernel.py` and `tests/test_admission.py` were not run here.
No packing, optimality or priority is claimed by the source or established here.

## Credit and Licence

The new material is Guzhou0806’s under the MIT licence (`LICENSE`, copyright 2026
Guzhou0806). `SOURCES.md` credits the density to wand125, “the rectangle-density method
and original translation-derivative verification structure” to Tokoharu, prior measure
and unavoidable-set work to Stromquist, Burns and Massaccesi, and says the concave-section
bound “is informed by the Rust implementation in Joshua Levy’s Squares Project”, pinned
at `ef79288a4`, and that the new C++ kernel “is not an unchanged replay of that Rust
program”. It gives Guzhou0806’s contribution as “the continuous-pose extension,
smaller-square coverage, near-axis patch, exact composition and associated
implementation/testing”, from “AI-assisted research”.
The density’s MIT licence is retained in `licenses/wand125.txt`, Tokoharu’s in
`licenses/tokoharu.txt` and this repository’s in `licenses/jlevy-squares.txt`.
The comment’s AI-assistance statement: “AI assisted mathematical exploration, proof
drafting, implementation, regression tests, packaging and this update under my
direction.”
The comment asks the record to “credit the continuous-pose extension, smaller-square
coverage, near-axis patch and resulting improvement to Guzhou0806, AI-assisted,
retaining wand125 for the original density, Tokoharu for the rectangle-density method
and translation-derivative structure, and Joshua Levy / the Squares Project for the
concave-section inspiration”.

## Compressed Files

The replay’s slab, control and crate receipts are stored as deterministic gzip;
`gunzip -k` restores each beside it.

| Stored file | Origin | Git blob (decompressed) | SHA-256 (decompressed) |
| --- | --- | --- | --- |
| `receipts/controls.jsonl.gz` | receipt | `31722e8303c1c4ccca475a418b4e63c4919a1503` | `ad01821e16d4bac0935661b4b88cb878924c9819b9865c2387ed0058e339848a` |
| `receipts/crate-runs.json.gz` | receipt | `173966536d75611c8acc17392d80f918f0f5cfea` | `2016fd579827b106ae8b2a8db4d1c733804358827b3fcca2bb5233b9c87df9d5` |
| `receipts/slabs.jsonl.gz` | receipt | `a97a19176d7974bed39f39ac7e48e851d6c6cb3b` | `8f8791cfddcdc843bb9796e7a9ec810c7732fde51310d2e04acbedb2b3b94012` |

The other receipts are plain JSON: `builds.json` (the compiler, each build’s command,
exit, wall and binary digest), `axis-run.json`, `control-G-release.json`, and the two
reports, `finite-audit.json` from `check` and `replay-check.json` from `check-replay`.

## Commands

From `packing/`, each after `uv run --frozen --all-extras --group dev`:

```sh
python -m devtools.acquire_source guzhou-n40-continuous-pose-2026-10-10 --check
python -m devtools.audit_continuous_pose check
python -m devtools.audit_continuous_pose check-replay
python -m devtools.audit_continuous_pose derive --out SCRATCH
python -m devtools.sqverify_fast_census --source-digest
python -m devtools.audit_continuous_pose run --out SCRATCH --workers 2 \
    --crate-binary sqverify_fast/target/release/sqverify-fast
```

`check` and `check-replay` read the retained files only, and their `--output` equals
`receipts/finite-audit.json` and `receipts/replay-check.json`; `run` needs `g++` and a
crate build of reviewed source, builds the kernels in `SCRATCH`, and writes fresh
receipts to `SCRATCH/receipts`, about 25 minutes at two workers on a shared host.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
