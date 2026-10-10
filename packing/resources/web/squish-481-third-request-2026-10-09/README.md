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

## What Is Not Established

The source reports that SQUISH’s exact `Fraction` checker accepts all seventeen, testing
every pair close enough to touch by separating axes and every square against the box,
and that David Ellsworth’s `check_packing.py` accepts each 50-digit export at
$\varepsilon = 10^{-50}$. It reports drawing each certificate from a 60-digit contact
solution with clearance $10^{-32}$, about $10^{-14}$ at 263 and 292. Those are author
reports; no program of the source has run here, and no replay is recorded yet.
The certificates would establish finite upper bounds only. The source gives no KKT,
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
```

`--check` re-derives the record from this packet alone. A replay reads the certificates
from a checkout at the pin and refuses bytes whose SHA-256 differs from the manifest’s.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
