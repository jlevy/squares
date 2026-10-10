# SQUISH Third Request: Seventeen Exact Rational Packings

Nate Chaoweeraprasit (itsnaka), using SQUISH,
[reports fifteen new packings and two smaller packings of counts already his](https://github.com/jlevy/squares/issues/481),
in
[itsnaka/squish-certs](https://github.com/itsnaka/squish-certs/tree/d45669b48cc97ad3aa17a6c847a8d06630f66eac/squish-submission-2026-10-09)
at `d45669b48cc97ad3aa17a6c847a8d06630f66eac` (tree
`91e24bc22a6f010e2ffae17eb0902f6b64d53ae2`, authored 2026-10-09T20:07:51Z, committed
2026-10-09T21:23:14Z, parent `e63e4e52b1728b6671b2f263c5e02a4aa79a39d3`). The pin is the
first commit that contains the `squish-submission-2026-10-09` directory. The source was
retrieved at 2026-10-10T09:54Z.

The fifteen new counts are 131, 153, 207, 209, 232, 236, 259, 263, 269, 270, 292, 302,
303, 305 and 307; the source calls them compositions of pieces of earlier packings,
found by its Mondrian method. The other two, 154 and 237, are nearby searches from
SQUISH’s own #401 packings, which the case records hold as refined by Siddharth Gupta.

## Source Custody

The tree has no licence file, and neither README states reuse terms.
Under the derived-only form of the
[existing retention policy](../known-best-packings/README.md), as for the
[earlier SQUISH packets](../squish-422-second-update-2026-10-07/README.md), this packet
keeps no upstream byte. No redistribution permission or licence determination is
asserted.

`devtools.acquire_source` wrote the packet from a clone checked out at the pin, from the
declaration in [acquisition/declaration.json](acquisition/declaration.json).
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the
manifest. The scope is the paths the pinned commit changed: the root `README.md` and the
whole `squish-submission-2026-10-09` directory, 111 files and 9,043,090 bytes, all
pinned only. The declared `source/` directory is empty by design.
The earlier submission directories are unchanged at this pin and belong to the packets
that pinned them.

Each of the seventeen count folders holds six files: the certificate `nNNN.cert.json`,
its 50-digit export `nNNN.cert.txt` in David Ellsworth’s text format, `nNNN.cert50.txt`,
a drawing, a raster comparison with the record and the author’s `check_packing.py`
output. For fifteen counts `nNNN.cert.txt` and `nNNN.cert50.txt` are the same blob; at
154 and 237 they differ. `sources/` holds three earlier certificates with their text
exports, and the directory’s `README.md` and `summary.csv` carry the claims, the exact
fractions and the lineage.

## The Certificates

`nNNN.cert.json` is a JSON object with `n`, `s_exact` (a rational string), `s_decimal`
and `squares`, one `[x, y, t]` triple of rational strings per square: the centre in
$[0, S]^2$ and $t = \tan(\theta/2)$, so $\cos\theta = (1-t^2)/(1+t^2)$ and
$\sin\theta = 2t/(1+t^2)$ exactly. The numerators and denominators run to about 80
digits. `summary.csv` repeats every `s_exact`, equal to the certificate’s at all
seventeen counts, with a 40-digit truncation.

The table binds each certificate to its Git blob and SHA-256, and compares its side with
the case record’s verified ceiling at `main` `657cc4861`. Every side is below it.

| n | Certificate | Git blob | Bytes | SHA-256 | Side, rounded up | Case ceiling, house | Below by |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 131 | `n131/n131.cert.json` | `cbb7e30aa79c6d23e6b8dd824477594886772f14` | 48150 | `ffc4f8f6b9964e116687178de3eef54e1d029265e19a5d7e6dcae1e8e9cbaa7d` | 11.9496595880358604 | 11.9511500449119512, [ry-xu square packing 2026] | 1.490e-03 |
| 153 | `n153/n153.cert.json` | `85eb6df41c73e1917c344f974f4caf7de1428d8c` | 53938 | `f29e06ec8e8b481620ab4fbf2c9cada4663bfe91f291513eec895dc519ff3eb2` | 12.8720298490811809 | 12.8796793733293146, [Gupta rational refinements 2026-10-08] | 7.650e-03 |
| 154 | `n154/n154.cert.json` | `577e9b98f9761e6639c35c702f568ffc44a5efb1` | 55937 | `678b3ce885a4d8378d7f0f9d2d6acbb58f4c8b77d992d6c11ab76d8858e36566` | 12.9230702023011408 | 12.9265622458523470, [Gupta rational refinements 2026-10-08] | 3.492e-03 |
| 207 | `n207/n207.cert.json` | `ff6c11961cc951de7f1ce18a617aeaad76de4b70` | 76780 | `da36d750f0385d7f64567cb3fe0ffbdb41e94d936d506349c591d10e8d2ffb1b` | 14.8855063088416777 | 14.8879922583026574, [Gupta rational refinements 2026-10-08] | 2.486e-03 |
| 209 | `n209/n209.cert.json` | `7140ed5f343abf13092921c418fc4f039b9829a5` | 75096 | `473cd1eef2e031d98eba21075629bd2d5b6ecbc31b209aa84cc9c4428ed46f3f` | 14.9462236544879195 | 14.9496179522003981, [Gupta rational refinements 2026-10-08] | 3.394e-03 |
| 232 | `n232/n232.cert.json` | `dda1cfcf1c1036acc51b2d1c0cc572f23d9ae1dd` | 83145 | `f62d44d2d80f38edbf7364596543e70d9b09ea88af3c2b0686fd59308554870d` | 15.7674283499418417 | 15.77817459305203, Evan Daniel’s exact ceiling of [Kingbird] | 1.075e-02 |
| 236 | `n236/n236.cert.json` | `3904de45e43aace2c0f9a65881b01ad47a55bf75` | 82739 | `4cdde0b5b063b21a5d66ec5fe69734b6b86cb31d4bc933f520f7dff7a2db26cc` | 15.8639557471592678 | 15.8678008394199166, [Gupta rational refinements 2026-10-08] | 3.845e-03 |
| 237 | `n237/n237.cert.json` | `1ccdcc67f9b94d624051daeffb2c50f8ec4d2a56` | 83189 | `def222eff08fe0eaaeded2a49e514d4ad6ce4bde6739c808945936a779b6688d` | 15.9029892208749656 | 15.9036762351891381, [Gupta rational refinements 2026-10-08] | 6.870e-04 |
| 259 | `n259/n259.cert.json` | `1c133ab3032d2c12c41f53de6f76acafae604aaf` | 93589 | `68bd3a471ab0b3b4f5569c70a31b1a631e479b53708a80925e85788d0871d5ad` | 16.5913781454976982 | 16.6025684904933646, [evand exact optima 2026-10-05] | 1.119e-02 |
| 263 | `n263/n263.cert.json` | `ee132f2047afb66af55ada5c7cb64b3d904b32ea` | 194670 | `308f950d9b965d5494c81437235b1a7fa13578415cddf2649a9deccfa6350612` | 16.7331660078998839 | 16.7404196795387766, [SQUISH second update 2026-10-07] | 7.254e-03 |
| 269 | `n269/n269.cert.json` | `d6762daa0f4be20a3cd92d1919db4be6da79f8e9` | 94681 | `26d07f4a90fd85501cda1af8126a26a1bbb56efd3a2f5cc579d3bbf75f16be30` | 16.9015135821891329 | 16.9059670585838410, [evand exact optima 2026-10-05] | 4.453e-03 |
| 270 | `n270/n270.cert.json` | `fa416a472f29d131f3b104effab5274de9e07a11` | 99489 | `6af0f646b28b61db28e71bcac0d16140d02c6f1da20aca582284c6ee109c0e89` | 16.9297801262411717 | 16.9378072284460292, [Daniel new arrangements 2026-10-07] | 8.027e-03 |
| 292 | `n292/n292.cert.json` | `b4c260f252a28e2f651b4c60aa4b388808e150f3` | 215670 | `ff098e0508c3095ae067cde5ab56428b71d369c24b5dcaac8ebc988e535808b5` | 17.5913781454979008 | 17.5972493911564651, [Rehwaldt Couzo refinements 2026-10-07] | 5.871e-03 |
| 302 | `n302/n302.cert.json` | `902d9f3752abf57de5072c442ed45b25561d125d` | 112370 | `cb2ed58d9474fef469aa5f1ad93bb51344429de38de4c324703d57c4f782d16d` | 17.8720298490811800 | 17.8813062180958085, [SQUISH second update 2026-10-07] | 9.276e-03 |
| 303 | `n303/n303.cert.json` | `fa9aeed258c7269868766593f457a12b0512ec68` | 106830 | `26d4ad0c5568fdfbf47f46ce1b12d53cacc7bd95b21e4170dbe786b9021ca143` | 17.9130654627385328 | 17.9203123729203498, [SQUISH ten packings 2026-10-07] | 7.247e-03 |
| 305 | `n305/n305.cert.json` | `3f5e1d9b8dbc46b7117dbf5058c282f89e64a334` | 110698 | `bfc8df75f5e6198f6e99a4c6156fd0e8ccf71683ae13c3f86a16dbf1463dc441` | 17.9511961441473858 | 17.9529594590155280, [evand exact optima 2026-10-05] | 1.763e-03 |
| 307 | `n307/n307.cert.json` | `b4c52922691d8c8f75ef0684914ef5807008a7d8` | 115950 | `4fe6c5a8d68f87d9866caf4924c5a826ea240fdd1f805e4c5d1a27145eb0a2a5` | 17.9808627840546911 | 17.9810305486333107, [evand exact optima 2026-10-05] | 1.678e-04 |

The issue’s 15-digit displays and each certificate’s `s_decimal` field are not roundings
of `s_exact`: they differ from it by up to $1.8 \times 10^{-15}$, in both directions. At
131, 153, 154, 207, 263, 269, 305 and 307 the issue’s display lies below the exact side,
by $3.97 \times 10^{-16}$ to $1.80 \times 10^{-15}$; at 263 it prints
`16.733166007899882` where the exact side rounds up to `16.7331660078998839`. The exact
side decides, the source’s prints remain quotations, and a safe display is the upward
ceiling in the table. The issue’s “register now” column names the cases’ sides by
finder and is not a ceiling here.

### The Three Source Packings

`sources/` holds three earlier SQUISH certificates the release does not file, named in
its lineage as the sources of pieces. Each is above the case ceiling at its count, so
none asks for a register entry and each stays in this packet.

| n | Certificate | Git blob | SHA-256 | Side, rounded up | Case ceiling, house | Above by |
| --- | --- | --- | --- | --- | --- | --- |
| 155 | `sources/squish-s155-source.cert.json` | `08a84d02427b2bfc10c2421709b8a0687c84d67d` | `00f18af157b2bc879215751ff3900db8bb3158e16c97e9bc359edbb8eee14a40` | 12.9531619520329305 | 12.9525032026045129, [SQUISH update 2026-10-07] | 6.587e-04 |
| 240 | `sources/squish-s240-source.cert.json` | `a0e79f4583cbc3b62aeedd74814603934f218794` | `d4e6c7a465ad1cf007bcbc9fe89c069adc5e3ea89fec60579d513f0215ee3bbd` | 15.9730095443134852 | 15.9696853375307804, [evand exact optima 2026-10-05] | 3.324e-03 |
| 306 | `sources/squish-s306-source.cert.json` | `d11975874dfd0c9fd69f141be42511cb7591d093` | `08335a44bbdf552d12e2495d9e043715a2d67895aa0ed2c90f626940dd31e004` | 17.9635102181210585 | 17.9634381397640029, [evand exact optima 2026-10-05] | 7.208e-05 |

## Against the Other Reports

Every other report pending at these counts on 2026-10-10 is larger at its count, by
exact comparison of the certificates’ sides, or of the 12-decimal ceilings #470 states:

- [#476](https://github.com/jlevy/squares/issues/476) (Francisco Couzo, 2026-10-09T20:28Z)
  at 237, 263, 270 and 303;
- [#470](https://github.com/jlevy/squares/issues/470) (Mishapolk) at 131, 153, 154, 207,
  209, 236, 237, 263, 270, 302 and 303;
- T-128 (Couzo, issue #451) at 131 and T-130 (Couzo, issue #460) at 270.

At 153 the certificate is also below SQUISH’s own n153 report of 7 October,
`12.8796793733329640`, which the source register already lists as superseded by Siddharth
Gupta’s refinement. Here the sides at 154, 207, 209, 236, 237, 263, 302 and 303 replace
earlier SQUISH packings that the cases hold directly or through Gupta’s refinements. The
earlier certificates stay retained in their own packets.

[acquisition/claims.json](acquisition/claims.json) freezes these comparisons, and
`devtools.upper_bound_reports` rebuilds them: each case ceiling from its holder’s own
packet, #476 from its retained
[packet](../couzo-exact-certificates-2026-10-09/README.md), T-128 and T-130 from theirs,
and #470 at its printed 12-place ceilings. At every count this certificate is the
smallest report. At 232 the case reports the Kingbird catalogue’s 15.77817459305202,
which is below the rational ceiling the case verifies, Evan Daniel’s certificate of side
`3944543648263005692141767432271/250000000000000000000000000000` (T-101); the
certificate is below both.

## Derived Facts and Exact Replay

`devtools.upper_bound_reports` read the seventeen `nNNN.cert.json` files from a checkout
at the pin, after `devtools.acquire_source` showed that the checkout yields this
packet’s acquisition record and manifest, so the bytes it read have the digests above.
Each certificate is admitted only where its exact side equals the exact fraction
`summary.csv` prints, to which the issue points; the issue’s own 15-digit displays are
quotations, as above.
Each is written as an exact rational `center-basis` Witness/v2 under [facts/](facts/),
the deciding witness of the maintained exact route, naming its certificate’s SHA-256 as
`revision_sha256`, and stored compressed.
The facts are this repository’s derivation; no upstream byte is retained, and offline
each fact must rebuild itself from the certificate it states.
The declaration of the import is [acquisition/report.json](acquisition/report.json).
The three `sources/` certificates are not offered as records and are not imported.

Only the facts enter geometry decisions, through the two-route kernel of
`devtools.evand_arrangement_reports`: `sqpack`’s exact witness verifier and the
independent rational corner checker, each deciding every wall and every pair over
$\mathbb{Q}$. Each count ran a positive job, a duplicate-square control and an
outside-container control, each in its own child process.
All seventeen positives pass both routes, and both routes refuse all 34 controls, each on
the overlap or the wall it was built to break.
In every positive both routes find the least wall clearance exactly 0: squares touch the
box, a closed-box packing, which is what $s(n) \le S$ asks and both routes accept. The
least pair gap is exactly $10^{-32}$, the clearance the source states, except at 263 and
292, where it is $3.16 \times 10^{-14}$ and $1.21 \times 10^{-14}$.
The 51 jobs made 3,148,314 pair decisions in 1,340.82 route CPU seconds and 2,487.87 job
wall seconds, summed; the longest job took 208.94 seconds, and the two-worker run 21
minutes 36 seconds of wall time, while other lanes held the machine at a load average of
8 to 9 on four cores.
The whole receipt exceeds the kernel’s 4,000,000-byte ceiling on uncompressed evidence,
so it is kept as one receipt per count, `receipts/exact-certification-nNNN.json.xz`,
each held to the same ceiling and admitted by the same rules; each keeps every deciding
input and both routes’ complete outputs.
The receipts were assembled from the run’s 51 finished job outputs after the first
write of the whole receipt was refused at that ceiling; no job ran twice.
The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method.

## What Is Not Established

The source reports that SQUISH’s exact `Fraction` checker accepts all seventeen, testing
every pair close enough to touch by separating axes and every square against the box,
and that David Ellsworth’s `check_packing.py` accepts each 50-digit export at
$\varepsilon = 10^{-50}$. It reports drawing each certificate from a 60-digit contact
solution with clearance $10^{-32}$, about $10^{-14}$ at 263 and 292. Those are author
reports; no program of the source has run here, and the replay above has not been
reviewed. The certificates establish finite upper bounds only. The source gives no KKT,
interval or local-optimality evidence, no closed forms and no optimality claim.

## Credit

The source credits Nate Chaoweeraprasit, using SQUISH (SQuare-packing Using Iterative
Shrink-Hopping) and its Mondrian composition method. Its lineage names the packings the
pieces came from: the Kingbird catalogue’s $s(5)$ and its former records at 11, 50,
152, 202 and 241; Francisco Couzo’s $s(182)$ and his #451 $s(180)$; Ryan Xu’s #432
$s(123)$, $s(129)$ and $s(175)$; SQUISH’s own $s(88)$, $s(130)$, $s(208)$ and $s(209)$;
and the three source packings above. `summary.csv` names the pieces of each count.
This is author-reported lineage, not an independently established construction
history.

The source states that SQUISH’s solver, its verification and the issue were written
with Claude Opus 5.5, and that the Mondrian method was planned and formulated by the
author and implemented with it, under his direction, management, review and steering.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source squish-481-third-request-2026-10-09 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports squish-481-third-request-2026-10-09 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports squish-481-third-request-2026-10-09 check --replay
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports squish-481-third-request-2026-10-09 derive --checkout CHECKOUT --check
```

`--check` re-derives the record from this packet alone. The importer’s `check-claims`
and `check --replay` run offline from the facts; `derive --check` needs a checkout at
the pin, refuses one that does not yield this packet’s record and manifest, and compares
each fact it derives with the retained one.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `facts/n-131.yaml.gz` | receipt | `b39aee550550f2059eccc5cb7e7051f49ec8c3c8` | `3cc0b799eb4b866985b99ff4e5b538e463a9aa8dd6943e1cb40a67e0b8c58d57` |
| `facts/n-153.yaml.gz` | receipt | `97fe0a5985cc28678a6b2edcfa6ac0828bd3c3c4` | `3fe549aff9734b5b35c8491be1a7ff05e08c6642fd0367a0124e1588487036cb` |
| `facts/n-154.yaml.gz` | receipt | `201bb8e5d95ca0abe7786e645cb53b6b283dacb0` | `2dc546749f72c5c61d56b92d34457c5593a6a6ed8670c9412f27693ddc45afc1` |
| `facts/n-207.yaml.gz` | receipt | `a63aebb8fcf098fc8a42b1609e6379c4e7350166` | `0df6d0b83b5b1741d547e5fd1800f631c0ecfce2b05a1bfe944fd16aa3ffa62b` |
| `facts/n-209.yaml.gz` | receipt | `8ba17443be60040c2ba2ab504f96fe2a2bb41dae` | `59e88014ddb3075c3d71334bde4553805be9f70f20653aedf6e58f15e05f39a0` |
| `facts/n-232.yaml.gz` | receipt | `fb675e7e4f99a4f7eeb6e7d055d5016d4f015b33` | `ae7ef3ec314877611a15943f88edceeb9ea5ac7fca751b7a8f402cf9142fba93` |
| `facts/n-236.yaml.gz` | receipt | `9cbe23b220e9cdd810a1d333d5a2f01e947bff28` | `6366bd8b7f37bdfaee05a1e2f2036c6fda43e50e1bc92284ed03c76128342334` |
| `facts/n-237.yaml.gz` | receipt | `b8ba038e246057cdbd4da02d47ce78c49bffa0dc` | `a3fda264cb07c5c72661c7cc65a34aa61fa9a98ea12cb35b5015d50d695ee283` |
| `facts/n-259.yaml.gz` | receipt | `0607129764f35e4c47aa9be76087dfb24663d04c` | `c4dac9932211ff9374c317b6b4308558765feeab10698d8d684ebbfca81175e0` |
| `facts/n-263.yaml.gz` | receipt | `8b6f554715112c9792a50f271b0f0310176cde7b` | `b74091d065c9748dde278c5f429f21ca109d1b923c63a0998dea383ddac60d5a` |
| `facts/n-269.yaml.gz` | receipt | `7b6902ac61a570e82bed0ba8b63f9714ea653cf4` | `4cb6356781541479a4c53562b2d26e24ce61f8770dfb1c7f85d9968ef0ef709b` |
| `facts/n-270.yaml.gz` | receipt | `d6d72c66f8d449f7452e7cf2eb3f1c855a869f43` | `2c977f77328288a2dddabf0f2f8f556a10ce6502fe223d92f73eeb16394ebdc7` |
| `facts/n-292.yaml.gz` | receipt | `dc74ad1298497ea7618dc3e63cbb6c6e2a43e7ee` | `fa0c93510934c56d35aee5bd3f8799c0e9bb2eece1b09f63e4e3773caee30895` |
| `facts/n-302.yaml.gz` | receipt | `81cbb512e450c57a90d27ae68da9164eb577d770` | `2762f0d1f968f7bb69fa351ebc35fa8921acd1b14243836372d1d7d9b3d416b8` |
| `facts/n-303.yaml.gz` | receipt | `d5bf1c295cab97a1704caf9cdb2917c7e44d6f47` | `7b858c2a0e41c32a7f900f78188425969ea14422b3cc9c94637a67f628ac15d1` |
| `facts/n-305.yaml.gz` | receipt | `aafc3232fb9ef468e1296ad819b3044d54b36907` | `944a01324032c9724e8b5abd4448a0b54b411638393f41b4867b1ff9e20289e9` |
| `facts/n-307.yaml.gz` | receipt | `395876d398e6ee5205cfa593380251eb7a52d62e` | `5b1b6c4a5d83a624c09bcc0d3889a1d2dfea4cfbe2d9a475220fd6713d6b3425` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
