# Robert Barnett’s Refinements at 2573ff5

[Issue #505](https://github.com/jlevy/squares/issues/505), filed 2026-10-11T14:24Z,
reports exact rational certificates for 146 and 261 unit squares, local refinements of
Ryan Xu’s packings, in
[RobertBarnettProjects/square-packing-research](https://github.com/RobertBarnettProjects/square-packing-research/tree/2573ff51c4b160c952bbb2d1c399e7430d9f9ae2)
at `2573ff51c4b160c952bbb2d1c399e7430d9f9ae2` (tree
`074518888aa78d0175eaa8d37a3e599e4e9f6067`, committed 2026-10-11T13:52:00Z), the
revision the issue pins. The source was retrieved at 2026-10-11T20:35Z.

| n | Printed by the issue, or else by the README at the pin | Rounded up at 16 places | Requested |
| --- | --- | --- | --- |
| 146 | 12.583782203951046204 | 12.5837822039510463 | yes |
| 261 | 16.678779875343207747 | 16.6787798753432078 | yes |
| 70 | 8.880960371668802 | 8.8809603716688020 | no: the README marks it superseded |
| 103 | 10.679232047495411 | 10.6792320474954110 | no: superseded |
| 123 | 11.591378145643661 | 11.5913781456436610 | no: superseded |
| 237 | 15.903670905778137 | 15.9036709057781370 | no: superseded |
| 295 | 17.704232790955142 | 17.7042327909551420 | no: superseded |

Each certificate is in Evan Daniel’s format: the header `n S`, then `x y t` per square,
a rational centre in $[0, S]^2$ and a rational $t = \tan(\theta/2)$. The exact sides at
146 and 261 are fractions with 118- and 113-digit denominators, the certificates’ first
data rows; each rounds up, at the 18 places the issue prints, to the printed side.
The five sides the README lists as historical are the certificates’ exact terminating
decimals.

## The Release

The pinned commit holds nine certificates. The README at the pin lists 146, 261 and
2043 as current results, and 70, 103, 123, 237 and 295 as historical, “valid
improvements over their dated starting sources” that newer packings beat and that it
excludes from the request. The 2043 certificate lies far beyond the case corpus and the
record’s beyond-horizon rows, which reach 379; it is pinned by digest and not compared.
The certificates at 70, 103, 123 and 295 were first committed in `c55926c`
(2026-10-10T01:47:37Z), 237 in `d2356fa` (2026-10-09T12:49:04Z), and 146 and 261 in the
pin.

`main` has since moved to `52cf1cc` (2026-10-11T14:44:32Z). Its three commits add
diagrams of 146 and 261, move the historical certificates into `superseded/` with
earlier refinements at 70, 103, 123, 129, 146 and 295 of 10 October, and leave
`certificates/n146.cert` and `certificates/n261.cert` byte-identical
(`720b63b7`, `71fe0491`). None of that is retained here.

The issue’s attachment, `square-packing-results.zip` (37,787 bytes, SHA-256
`49aaa81ca0dde2049ed9eb4e4d79efa5cd5fd0ebfe8f86efcc6767f92a0d1ff3`, the digest the issue
states), holds three files: the two certificates, byte-identical to the pinned ones, and
`results/submission.json` (SHA-256
`947d314b16fd39db65afbc7e92a436467a218ba390cef8f7284e3f0a4775b790`), which says it is
`results/review-2026-10-11.json` at the pin filtered to the two counts. The attachment
was read and is not retained.

## Source Custody

The tree has no licence file and its README states no reuse terms.
Under the derived-only form of the
[existing retention policy](../known-best-packings/README.md), as for the
[Deleeuw refinement](../ebdeleeuw-n70-refinement-2026-10-10/README.md), this packet keeps
no upstream byte. No redistribution permission or licence determination is asserted.

`devtools.acquire_source` wrote the packet from a clone checked out at the pin, from the
declaration in [acquisition/declaration.json](acquisition/declaration.json).
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest.
All eleven files of the tree are pinned only, 502,546 bytes; the declared `source/`
directory is empty by design.

| Upstream path | Git blob | Bytes | SHA-256 | What it is |
| --- | --- | --- | --- | --- |
| `certificates/n146.cert` | `720b63b721317e8d03f23135babfde79b219261a` | 74239 | `77b5524f387472a8e5996e319d05735e2a6a0046c24e7043995549bf3945fa3d` | The 146 certificate |
| `certificates/n261.cert` | `71fe0491342268e303a40a80bd6ec58dbfde343f` | 125135 | `9141f7eb86ae23388d349efd810992727f16ca09bc9d0d1a5b94cd5e2a3f0019` | The 261 certificate |
| `certificates/n070.cert` | `5794ba160ce76a4cbd8774c065bfdc8d6ba13202` | 5892 | `767adfdc54477bf1fc2c46eeaf0f71cdfc87c8639391bb43ec5a0586bff4cdc2` | Historical |
| `certificates/n103.cert` | `a2e81937263d132604448d545b65305d8e3bbb88` | 8802 | `496da623c14ea7983729f7b3e380cb1c7431612a85de52b0c30f636d3d3a2952` | Historical |
| `certificates/n123.cert` | `bde71587af79c5e86dceacdf138d1fa8fd2d87c7` | 9859 | `b3ea89a34eda651cc851f126d9adb023f74e9e2cdb49745c114abe4b9142cd1c` | Historical |
| `certificates/n237.cert` | `69c5182c11079d9aa739d23bdbf3fabe3cc9c940` | 22290 | `76253edce982bae58907c8c39a18433a053eb2a89adccd2dcea58737e09966b6` | Historical |
| `certificates/n295.cert` | `c780885a5fcb5eeb2e832729edfae3a42a97fd88` | 27730 | `e9226d79456445dd4513c6fb95d8b34ebe568959816bf77e60a19af937b3ac73` | Historical |
| `certificates/n2043.cert` | `dca4acfff5dc5826403fe00c860ac58b44cda8dd` | 198698 | `bfbefba7df7481d409620da9843a51fcaf92c02fdcb733f0c0e24796fb5bd779` | Beyond the corpus |
| `results/review-2026-10-11.json` | `49c53f1a76ff82d67751f802082abf048d392fa6` | 16523 | `7b19d2fe41037206ae44fe4a3d43ee5d4e3024e83507a75d2e67fe058936b712` | Author’s sides, comparisons and receipts |
| `results/quiet-2026-10-10.json` | `807844b8ef5d099aa26db2fe57f4ea8cd84c9907` | 4979 | `cc7527ae32674bb2700db8be72f5af05984498924fd113adca42369c89d584c4` | Author’s earlier results |
| `README.md` | `5fc9e6c116faaefda8fccb516f8ad9f5d5c65b34` | 8399 | `40b97e99f8b16856264b2bf6c3fbf053045f24203397d6666718edee4f7de922` | Author prose |

The digests of `n146.cert` and `n261.cert` are the ones the issue and the README state.

## Derived Facts and Exact Replay

`devtools.upper_bound_reports` read each in-horizon certificate from the checkout at the
pin, after `devtools.acquire_source` showed that the checkout yields this packet’s
acquisition record and manifest, so the bytes it read have the digests above.
It wrote each as an exact rational `center-basis` Witness/v2 under `facts/`, the deciding
witness of the maintained exact route, naming the certificate’s SHA-256 as
`revision_sha256`. The facts are this repository’s derivation; offline each must rebuild
itself from the certificate it states. The declaration of the import is
[acquisition/report.json](acquisition/report.json).

Only the facts enter geometry decisions, through the maintained two-route kernel of
`devtools.evand_arrangement_reports`: `sqpack`’s exact witness verifier and the
independent rational corner checker, each deciding every wall and every pair over
$\mathbb{Q}$. The replay covers all seven in-horizon certificates. Each count ran a
positive job, a duplicate-square control and an outside-container control, each in its
own child process, on one worker.

All seven positives pass both routes, and both routes refuse all 14 controls, each on the
overlap or the wall it was built to break. In every positive the two routes find the
same least wall clearance and the same least pair gap. At 146 they are
$3.93 \times 10^{-14}$ and $1.21 \times 10^{-16}$, and at 261 $4.69 \times 10^{-14}$ and
$1.21 \times 10^{-16}$, the margins the source reports; at the five historical counts
both lie between $9.39 \times 10^{-12}$ and $1.20 \times 10^{-11}$. The 21 jobs made 786,102 pair decisions in 530.82 route CPU
seconds and 1,329.06 job wall seconds, summed; the longest job took 224.09 seconds. The
one-worker run took 23 minutes 17 seconds of wall time with the machine at a load of 9
to 25. A fresh serial `check --replay` decided all 21 jobs again, equal to the retained
rows apart from timing, in 27 minutes 15 seconds at a similar load.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)
keeps every deciding input and both routes’ complete outputs.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. Neither is the source’s code. The third exact route
(`devtools.check_half_angle_area`) has not read these certificates.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes each certificate against the
record at `main` `3a5a91a90` (11 October 2026). `check-claims` rebuilds it, each case
ceiling from its holder’s own packet and each pending entry’s side from its own packet.

| n | Case ceiling, holder | Below it by | Pending entries at the count | Smallest |
| --- | --- | --- | --- | --- |
| 146 | 12.5837822775125838, Ryan Xu (T-125) | $7.36 \times 10^{-8}$ | T-146, Evan Daniel’s regularization of Ryan Xu’s packing, above by $7.35 \times 10^{-8}$ | this certificate |
| 261 | 16.6787798754166788, Ryan Xu (T-125) | $7.35 \times 10^{-11}$ | none | this certificate |
| 70 | 8.8809603717088810, Ryan Xu (T-125) | $4.01 \times 10^{-11}$ | T-137 (#483) below by $1.03 \times 10^{-10}$; T-146 below by $1.13 \times 10^{-10}$ | T-146 |
| 103 | 10.6792320475106793, Ryan Xu (T-125) | $1.53 \times 10^{-11}$ | T-138 (#470) below by $1.33 \times 10^{-10}$; T-146 below by $1.34 \times 10^{-10}$ | T-146 |
| 123 | 11.5913781457115914, Ryan Xu (T-125) | $6.79 \times 10^{-11}$ | T-146 below by $1.46 \times 10^{-10}$ | T-146 |
| 237 | 15.9036762351891381, Gupta’s refinement of SQUISH (T-127) | $5.33 \times 10^{-6}$ | T-134 (#476) below by $1.98 \times 10^{-10}$; T-136 (#481) below by $6.82 \times 10^{-4}$; T-140 (#488) below by $7.21 \times 10^{-4}$ | T-140 |
| 295 | 17.7042327915177043, Ryan Xu (T-125) | $5.63 \times 10^{-10}$ | T-146 below by $2.19 \times 10^{-10}$ | T-146 |

At 146 the margin is the issue’s, $7.35 \times 10^{-8}$ below T-146’s exact side.
At 261 Ryan Xu’s certificate side, which the case holds, is his printed side
$16.6787798754$ with every centre dilated by $1 + 10^{-12}$, exactly
`83393899377083393899377/5000000000000000000000`; that dilation is
$1.67 \times 10^{-11}$. The certificate here is below the dilated side by
$7.35 \times 10^{-11}$ and below the undilated printed side by $5.68 \times 10^{-11}$, so
it does not merely remove the dilation: it is below everything the record and #432
print at 261. No other report of 11 October (#500, #501, #503, #504, #506) names any of
these counts.

## What Is Not Established

The source reports four exact checks of both certificates with zero tolerance: a
separating-axis checker and a polygon checker written in the same assisted project, and
Evan Daniel’s `verify_cert.py` and `verify_cert2.py` at
`268af529546176a25224ea3b2c7d29cef8d9e911`, plus David Ellsworth’s `check_packing.py` on
140-digit exports at tolerance $10^{-90}$ as numerical evidence. Those are author
reports; no program of the source has run here, and the replay above has not been
reviewed. That each certificate refines Ryan Xu’s packing, and is not another
arrangement, is the source’s statement; this packet retains no comparison of the poses.
The certificates establish finite upper bounds only; the source claims no optimality.

## Credit

The source credits Ryan Xu with both original layouts and Robert Barnett with the
refinements, by minimum-movement sequential linear programming followed by an exact
rational contraction and recertification, on a CPU. At 146 it credits Evan Daniel’s
public regularization in the comparison, and does not say which certificate the
refinement started from. It discloses OpenAI Codex assistance with the solver, the
certificate and checker code, the source review and the preparation, and says the search
code and run logs are held outside the repository.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source barnett-refinements-2026-10-11 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports barnett-refinements-2026-10-11 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports barnett-refinements-2026-10-11 check --replay
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports barnett-refinements-2026-10-11 derive --checkout CHECKOUT --check
```

`--check` re-derives the record from this packet alone. The importer’s `check-claims`
and `check --replay` run offline from the facts; `derive --check` needs a checkout at the
pin, refuses one that does not yield this packet’s record and manifest, and compares the
facts it derives with the retained ones.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `facts/n-070.yaml.gz` | receipt | `29a447acae4a2d2857ef8754ab5f2420655394ec` | `25c3116cbc5585f7c2e8e53b1ea51d53e23e99f5abdb371b292e071ac9679f06` |
| `facts/n-103.yaml.gz` | receipt | `b050afa6ecc035b7df1cb212354ce9ee30a496cb` | `27c0f02ed0e960901341296f6392c7769d900fa19be25ae31c0278879de420ac` |
| `facts/n-123.yaml.gz` | receipt | `fba1948705f55c4b5dd57e18662b8a0bab240897` | `57ba0649d720b11c7f1b4f9fe4078367056878f44a5e3f36cfcfd982521b6884` |
| `facts/n-146.yaml.gz` | receipt | `4aa503d4c65c2424d8ec36bd87baa08c5b214fae` | `659101e4e3e52388ccb779b4a35913764ea17534533d48c81dfd84436ca48989` |
| `facts/n-237.yaml.gz` | receipt | `ae07c83129bd1ff5be7fcf63b53bdd0a2c60e3e2` | `a1aac175dc4e61eeb66bf622d7433b18e9fbf8f08183619c1b9bfe6cffee5ba4` |
| `facts/n-261.yaml.gz` | receipt | `1654121f7c56808c3ee4937e94e5bd21bf0fa33b` | `6310d3d00e01bfb0135d84382532ea58c1a3b3b6b239da52795632b89c22cca4` |
| `facts/n-295.yaml.gz` | receipt | `f2432de25fe5870d72b5f8bac7f008a1c856d145` | `03a884480db700875e07419561a8184fe5d2285ba5cc9f0222aa0983e8ef2010` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
