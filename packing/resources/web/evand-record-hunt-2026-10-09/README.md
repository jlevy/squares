# Evan Daniel’s Record-Hunt Certificates: 132 and 155

[Issue #465](https://github.com/jlevy/squares/issues/465) reports two exact rational
packings from Evan Daniel’s record hunt `hunt1`, in
[evand/square-packing](https://github.com/evand/square-packing/tree/e0081804736a4613c2cf44c693ef1afe92518927/search/packer/candidates)
at `e0081804736a4613c2cf44c693ef1afe92518927` (tree
`c8ca38bb5205c649f778b7edd6486a84f6bce91b`, committed 2026-10-09T03:34:37Z):

| n | Exact side of the certificate | Rounded up at 16 places |
| --- | --- | --- |
| 132 | `2397419866449012645435948575487/200000000000000000000000000000` | 11.9870993322450633 |
| 155 | `647624947200700369098292528347/50000000000000000000000000000` | 12.9524989440140074 |

Each certificate gives 132 or 155 unit squares, each a rational centre and a rational
$t = \tan(\theta/2)$, in an open square of the stated side.
The certificates were first committed in `8af2421` (n = 132, 2026-10-09T00:17:26Z) and
`9401eb7` (n = 155, 2026-10-09T00:27:01Z); the pinned commit adds the hunt’s summary to
the packer log and leaves both unchanged.
The sources were retrieved at 2026-10-09T20:51Z.

## Retained Here

`devtools.acquire_source` wrote the packet from a sparse checkout at the pin, from the
declaration in [acquisition/declaration.json](acquisition/declaration.json); every file
is bound to its Git blob at the pin. [acquisition/sources.json](acquisition/sources.json)
is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest.

| Upstream path | Git blob | Bytes | SHA-256 |
| --- | --- | --- | --- |
| `search/packer/candidates/hunt1_n132.cert` | `5d936d5580838a22e041c55ef618a6b697ddda6d` | 21684 | `ba5517d658bb146c1c7791d0c3a86751b2e100da0c0753b0dbb05071c8ca5d16` |
| `search/packer/candidates/hunt1_n132.exact.txt` | `75542a667f823ef179c6fddd8fcac89d754db008` | 26277 | `7a224d2e47de54aa7790bd33598f5f6f32a3a2d3abcfc73fcdf350da24c699bc` |
| `search/packer/candidates/hunt1_n132.input.txt` | `35eea2ae640367ab59df9cd864f4573061932d12` | 7126 | `9995d911220b1b2e2ad179ef465a51374c6f8b801c12109ea89ef2fce76e8814` |
| `search/packer/candidates/hunt1_n132.json` | `482d40bbd1f86e80b5dff011d5ad03918183a3ab` | 4740 | `1c20deb80e86e3ee85f0708b25041de23067e5780f9b41b46fe2ade1cc8277fd` |
| `search/packer/candidates/hunt1_n155.cert` | `890b7de32721e1539d5dc79bf753de1b4bb37948` | 25413 | `d7fda2ba5037fe64b638cd6073bb69f5cd3f971ef66c1e4f9af4d9380a6ebee3` |
| `search/packer/candidates/hunt1_n155.exact.txt` | `f5e72988277ad0f9a0db1ed4a6770bfc481dea6d` | 30434 | `30e24a9a94cbb472d408e654b23aae575da192473b7c8e0617f8ded746039512` |
| `search/packer/candidates/hunt1_n155.input.txt` | `0fd9609851d8200d5c6b504f0a0d4f4ac76b27c5` | 7756 | `20026b3b5f017dc06ef40c09621d6d8f02d59108832538d4689d395195a63a14` |
| `search/packer/candidates/hunt1_n155.json` | `c5cc94c45e00f5c3e612ffca387c35ef5c02e2a7` | 5308 | `79bd56d25a6ad21710ad5072ae2e9d3e77fa7a537b4877818412159cb3207eed` |
| `search/exact/README.md` | `60e4281acf45acdd920561428a9fcf588092beb0` | 13635 | `17715bc889e8fb5fc24662bcf9798abf88f7e1322254553147949e522eef5eab` |
| `CREDITS.md` | `1d7dcb7853e58ba38a472c7c976c2c0e4eedbc0a` | 7501 | `778884d09f88ce159ea2cea2134d30fb14bf01bf58fc9e69c6f3d77433da8168` |
| `LICENSE` | `52cf89d2125f517a425c9a57c998dd85d83d7741` | 1068 | `c51886c0f7e6724a7d89fc22cb237a1688ba1bbff04cb21a13b8e1a01fb15578` |

Per count, the `.cert` file is the certificate, `.exact.txt` the 80-digit KKT point it
was rounded from, `.input.txt` the binary64 packing that point was solved from, and
`.json` the solver’s report: multipliers, the reduced Hessian, and the corner-to-corner
jamming check. The source’s two checkers, `search/exact/verify_cert.py` and
`verify_cert2.py`, are pinned by digest only: they are byte-identical to the copies the
[issue-399 packet](../evand-new-arrangements-2026-10-07/README.md) retains, and were not
run. The packer’s working log, `search/packer/PACKER.md` (93,441 bytes), is pinned by
digest only.

## Exact Replay

Only the two certificates enter geometry decisions, through the maintained two-route
kernel of `devtools.evand_arrangement_reports`, the one the issue-399 and Couzo
follow-up imports used: `sqpack`’s exact witness verifier and the independent rational
corner checker, each deciding every wall and every pair over $\mathbb{Q}$ after an exact
half-angle conversion. Each count runs a positive job, a duplicate-square control and an
outside-container control, each in its own child process.

Both positives pass both routes, and both routes refuse all four controls, each on the
overlap or the wall it was built to break.
In each positive, both routes find the least wall clearance exactly
`1/200000000000000000000` ($5 \times 10^{-21}$) and the least pair gap just under
$10^{-20}$; the receipt keeps the exact values.
The six jobs made 123,486 pair decisions in 38.66 route CPU seconds and 38.79 job wall
seconds, summed; the longest job took 7.72 seconds, and the two-worker run took 22.3
seconds of wall time.
A fresh serial `check --replay` reproduced all six results apart from timing in 38.7
seconds. [receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)
keeps every deciding input and both routes’ complete outputs.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. No source program ran here.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes each certificate against the
record as it stood when the issue was read (`main` at `d3860c97a`, 9 October 2026), and
`check-claims` rebuilds it from the houses’ own retained packets:

| n | Case ceiling, house | Below it by |
| --- | --- | --- |
| 132 | 11.9913278876915015, Evan Daniel’s exact optimum of Francisco Couzo’s packing (T-098) | $4.23 \times 10^{-3}$ |
| 155 | 12.9525032026045129, Nate Chaoweeraprasit’s SQUISH update (T-115) | $4.26 \times 10^{-6}$ |

At $n = 155$ the side is exactly the side of Francisco Couzo’s certificate from
[issue #451](https://github.com/jlevy/squares/issues/451), committed on 8 October 2026
and registered as T-128, pending adoption.
The two certificates share 152 of their 155 exact poses, centre and rotation alike.
The three that differ include square 83 of this certificate (counting from zero), which
the source’s report lists as free.
The source calls this packing a nearby minimum of SQUISH’s; Couzo’s issue credits SQUISH
for his.

At $n = 132$ no certificate the record holds is as small.
The source reports this packing as a different local minimum from Couzo’s, reached from
it by an uphill excursion through intermediate minima, at an RMS distance per square of
0.124 from the register’s packing.

## What Is Not Established

The certificates establish finite upper bounds at their exact sides, nothing more.
The source’s statements that each exact point is a KKT point with positive multipliers on
its load-bearing contacts, that its reduced Hessian is positive semidefinite modulo exact
flat motions (33 at 132, 2 at 155) and that it is jammed in every corner-to-corner
branch are numerical evidence, as the source itself says, and were not replayed here.
Novelty, local or global optimality and rigidity are not established, and no review of
the replay has been made.

## Credit and Licence

Evan Daniel wrote the source under the MIT licence (`LICENSE`), with credits in
`CREDITS.md`; its commits disclose Claude (Anthropic) as co-author, and on
[#375](https://github.com/jlevy/squares/issues/375) the author described the solver and
checkers as written with Claude under his direction.
The n = 132 packing descends from Francisco Couzo’s, and the n = 155 packing from Nate
Chaoweeraprasit’s SQUISH packing; the register data the search started from is this
project’s.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source evand-record-hunt-2026-10-09 --check
uv run --frozen --all-extras --group dev python -m devtools.evand_hunt_reports check-claims
uv run --frozen --all-extras --group dev python -m devtools.evand_hunt_reports check
uv run --frozen --all-extras --group dev python -m devtools.evand_hunt_reports check --replay
```

`check` admits the receipt structurally against the retained certificates; only
`--replay` decides the geometry again.
`certify --jobs-dir SCRATCH --workers 2` writes a new receipt from a fresh job directory.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
