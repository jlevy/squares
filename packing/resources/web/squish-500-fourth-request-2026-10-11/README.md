# SQUISH Fourth Request: Nine Exact Rational Packings

Nate Chaoweeraprasit (itsnaka), using SQUISH,
[reports nine new packings, four of them smaller packings of counts already his](https://github.com/jlevy/squares/issues/500),
in
[itsnaka/squish-certs](https://github.com/itsnaka/squish-certs/tree/aeacc6c124df339074f7370e1e010bb6e8c1b5ca/squish-submission-2026-10-11)
at `aeacc6c124df339074f7370e1e010bb6e8c1b5ca` (tree
`e67d0004e65363d58e8090560f92544093507104`, authored and committed 2026-10-11T05:30:10Z,
parent `bd0c72e278b8f62f5b22169594daea1f171a49c4`). The pin is the first commit that
contains the `squish-submission-2026-10-11` directory.
The head when read, `56fa71f949234b63534772b3f3b4f1320fbf2afd` (2026-10-11T05:30:50Z),
changes only the root `README.md`, to link the issue, so no claim depends on it.
The source was retrieved at 2026-10-11T20:34Z.

The nine counts are 176, 181, 238, 239, 270, 271, 272, 304 and 305, all found by
SQUISH’s Mondrian composition.
At 238 and 239 they are smaller than SQUISH’s #401 packings, which the cases hold as
refined by Siddharth Gupta, and at 270 and 305 smaller than SQUISH’s #481 packings
(T-136). Since #481 the method narrows a piece within its own rectangle before composing
(all but 176), and at 176 it interlocks two pieces.

## Source Custody

The tree has no licence file, and neither README states reuse terms.
Under the derived-only form of the
[existing retention policy](../known-best-packings/README.md), as for the
[earlier SQUISH packets](../squish-481-third-request-2026-10-09/README.md), this packet
keeps no upstream byte.
No redistribution permission or licence determination is asserted.

`devtools.acquire_source` wrote the packet from a clone checked out at the pin, from the
declaration in [acquisition/declaration.json](acquisition/declaration.json).
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest.
The scope is the paths the pinned commit changed: the root `README.md` and the whole
`squish-submission-2026-10-11` directory, 67 files and 5,866,372 bytes, all pinned only.
The declared `source/` directory is empty by design.
The earlier submission directories are unchanged at this pin and belong to the packets
that pinned them.

Each of the nine count folders holds six files: the certificate `nNNN.cert.json`, its
50-digit export `nNNN.cert.txt` in David Ellsworth’s text format, `nNNN.cert50.txt` (the
same blob at all nine), a drawing, a raster comparison with the record and the author’s
`check_packing.py` output.
`sources/` holds five earlier certificates with their text exports, and the directory’s
`README.md` and `summary.csv` carry the claims, the exact fractions and the pieces.

## The Certificates

`nNNN.cert.json` is a JSON object with `n`, `s_exact` (a rational string), `s_decimal`,
`note` and `squares`, one `[x, y, t]` triple of rational strings per square: the centre
in $[0, S]^2$ and $t = \tan(\theta/2)$, so $\cos\theta = (1-t^2)/(1+t^2)$ and
$\sin\theta = 2t/(1+t^2)$ exactly.
The numerators and denominators run to about 80 digits.
`summary.csv` repeats every `s_exact`, equal to the certificate’s at all nine counts,
with a 40-digit truncation.

The table binds each certificate to its Git blob and SHA-256, and compares its side with
the case record’s verified ceiling at `main` `3a5a91a90`. Every side is below it.

| n | Certificate | Git blob | Bytes | SHA-256 | Side, rounded up | Case ceiling, house | Below by |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 176 | `n176/n176.cert.json` | `b10fd271660ea1196812499fe97b7b7857222795` | 65305 | `42fc373b225ce75f3654ecd986b28d97fd75b3b804d04870b88df8eca52f52b0` | 13.8128562532770564 | 13.8228756555322953, Evan Daniel’s exact ceiling of [Kingbird] | 1.001e-02 |
| 181 | `n181/n181.cert.json` | `01c86175b1a09400efb108d8bd088ae306590f9b` | 65304 | `cc0afa669ae8bb88762284bb19bbd61706a9cddd5b4a10091e6ebd38c1e4f7a0` | 13.9508195310229241 | 13.9537488219544025, [evand exact optima 2026-10-05] | 2.929e-03 |
| 238 | `n238/n238.cert.json` | `4948cc6253255e49ed7899b49f497e7b2e61ea75` | 88160 | `42c72bc2fdb736572a0712db48b495a5ab4dfbe6b5df0df9d912614149313f0a` | 15.9241067853214947 | 15.9261468570109784, [Gupta rational refinements 2026-10-08] | 2.040e-03 |
| 239 | `n239/n239.cert.json` | `e88fed215d13464096e05adb90b5f0d82688186f` | 86144 | `b7be0948c96ffe58e56de744330915b417c97a0561b28e32359f35f99b17f805` | 15.9484433273005000 | 15.9493131697276962, [Gupta rational refinements 2026-10-08] | 8.698e-04 |
| 270 | `n270/n270.cert.json` | `da7857f51d589b6f950634bbce24cb793bd86d33` | 97905 | `e52e241481e812e54eb368fff3b447f44d7156fc253d151545dcb9a0c526d5de` | 16.9281969933290166 | 16.9378072284460292, [Daniel new arrangements 2026-10-07] | 9.610e-03 |
| 271 | `n271/n271.cert.json` | `d1745c0384370ccd6f9cc7fbb3ddbdd3a6b680f1` | 97523 | `3868ef22494b88fdfabdfb051df8f378c9c828339ebc07cc2db584e9f130924d` | 16.9491166878150100 | 16.9508207926249588, [evand exact optima 2026-10-05] | 1.704e-03 |
| 272 | `n272/n272.cert.json` | `f5f472a1419d62d37e9dab25cc30a6e46fac0ceb` | 98859 | `495fa4d68825fd72453c730c3cc01a342bfd46b1419e1a638f98aa945cbda52f` | 16.9655864748376712 | 16.9681101457696006, [Daniel new arrangements 2026-10-07] | 2.523e-03 |
| 304 | `n304/n304.cert.json` | `1d6714c9e6361ba7262e84feef6d294d1f8ade44` | 112681 | `ce52b2ed338874604fcfe744e5d66d31086051a619e4f10ea6b908808311c47c` | 17.9296570421708801 | 17.9346500183906818, [evand exact optima 2026-10-05] | 4.992e-03 |
| 305 | `n305/n305.cert.json` | `bbb232988845e01e6171875de4deb91d81e532e8` | 114719 | `95a291460f3c128a9c80c1ba571c4d8118293f36860f38d5d55775636da80d33` | 17.9505448539256365 | 17.9529594590155280, [evand exact optima 2026-10-05] | 2.414e-03 |

Each margin is cut, not rounded, at four digits; the exact difference is in
[acquisition/claims.json](acquisition/claims.json).
At 176 the case reports the Kingbird catalogue’s 13.82287565553229, the side
$(25 + \sqrt{7})/2$ cut at 14 places, and verifies Evan Daniel’s rational ceiling of
that packing (T-101), which the column shows; the certificate is below both.

The issue’s 15-digit displays are the exact sides cut, not rounded: at all nine counts
the display lies below `s_exact`, by $3.86 \times 10^{-17}$ (304) to
$9.72 \times 10^{-16}$ (271). Each certificate’s `s_decimal` is not a rounding of
`s_exact` either, differing from it by $-1.57 \times 10^{-15}$ (305) to
$+6.94 \times 10^{-16}$ (239), cut at three digits.
The exact side decides, the source’s prints remain quotations, and a safe display is the
upward ceiling in the table.
The issue’s “register now” column names the cases’ sides by finder and is not a ceiling
here.

### The Five Source Packings

`sources/` holds five earlier SQUISH certificates the release does not file, named in
its lineage as the sources of pieces; a sixth, `squish-s240-source`, is in the
[#481 packet’s](../squish-481-third-request-2026-10-09/README.md) scope.
None asks for a register entry, and each stays in this packet: three are above the case
ceiling at their count, and the other two are below it but above the certificate this
release files at the same count.

| n | Certificate | Git blob | SHA-256 | Side, rounded up | Against the case ceiling | Against this release |
| --- | --- | --- | --- | --- | --- | --- |
| 154 | `sources/squish-s154-a-source.cert.json` | `f72c11b1388a9ca41a70fda0eece1cb25d914035` | `40b8f1b14e88d830e45fa8d71809735e5994a23819eed635f6de0ccd3e65b517` | 12.9292934240939391 | above 12.9265622458523470, [Gupta rational refinements 2026-10-08], by 2.731e-03 | no 154 filed; above T-136’s 12.9230702023011408 |
| 154 | `sources/squish-s154-b-source.cert.json` | `0b2fccb9246fe21f3aba0fef68e39a30f6d2ab6a` | `94ce4566f7cc41923caebb5d038e2d11a5d766936c37f7905996b720b4f5876e` | 12.9305839972855079 | above it by 4.021e-03 | as above |
| 240 | `sources/squish-s240-b-source.cert.json` | `9470787a6197e382297b83817be3516ea8df65c0` | `4088d345613d61b92e8baf777ede6a419601c74e1260659ec150386ca765c255` | 15.9739500348208213 | above 15.9696853375307804, [evand exact optima 2026-10-05], by 4.264e-03 | no 240 filed |
| 272 | `sources/squish-s272-source.cert.json` | `348330f4ed8e519dd1a600e557bf43b0bfe5e4b1` | `4b34e44c02a25f1a7149024a7ca0f0da2dbcf677ebdbae00b9fc2767b718c04f` | 16.9655871623998319 | below 16.9681101457696006, [Daniel new arrangements 2026-10-07], by 2.522e-03 | above the filed 272 by 6.875e-07: the same packing before its squeeze |
| 305 | `sources/squish-s305-source.cert.json` | `a0e9db7f9aa7762b3bc8fedb8a8d09ad09a4b2d0` | `cb28ee4bc8b7f55af89898bb8d168ef395ac13144590abc0fc44cad783a1c405` | 17.9508590931679247 | below 17.9529594590155280, [evand exact optima 2026-10-05], by 2.100e-03 | above the filed 305 by 3.142e-04, which it gave pieces to through the 272 |

The source 305 is also below T-136’s 305 and T-140’s, by $3.37 \times 10^{-4}$ and
$2.80 \times 10^{-4}$, and above #506’s print; the filed 305 supersedes it.

## Against the Other Reports

Every other report at these counts is compared by exact sides where its certificate is
retained, and by its printed ceiling otherwise.
At seven counts this certificate is the smallest report:

- at 270, below T-130 (#460) by $8.526 \times 10^{-3}$, T-134 (#476) by
  $8.523 \times 10^{-3}$, T-138 (#470) by $8.526 \times 10^{-3}$, SQUISH’s own #481
  packing (T-136) by $1.583 \times 10^{-3}$ and Francisco Couzo’s #488 refinement of it
  (T-140) by $1.578 \times 10^{-3}$;
- at 238 and 239, below #470’s retained packings, which are above the cases and
  unregistered there;
- at 181, 271, 272 and 304, below the certificates the #476 packet retains and does not
  request.

At 304 and 305 Francisco Couzo’s [#506](https://github.com/jlevy/squares/issues/506)
(commit `337078c`), built from these very packings, prints 17.929565946849 and
17.950466482138, each its exact side rounded up at 12 places, so it is smaller by at
least $9.109 \times 10^{-5}$ and $7.837 \times 10^{-5}$. #506 credits these packings as
its starting points, so they stay retained and replayed here.
At 305 this certificate is still below T-136 by $6.512 \times 10^{-4}$, T-140 and the
#489 certificate that ties it by $5.949 \times 10^{-4}$, and #476’s retained 305 by
$2.414 \times 10^{-3}$. T-146 has no row at any of these counts, and #501, #503, #504
and #505 name none of them.

[acquisition/claims.json](acquisition/claims.json) freezes these comparisons, and
`devtools.upper_bound_reports` rebuilds them: each case ceiling from its holder’s own
packet, each retained report from its packet, and #506 at its printed 12-place ceilings.

## Derived Facts and Exact Replay

`devtools.upper_bound_reports` read the nine `nNNN.cert.json` files from a checkout at
the pin, after `devtools.acquire_source` showed that the checkout yields this packet’s
acquisition record and manifest, so the bytes it read have the digests above.
Each certificate is admitted only where its exact side equals the exact fraction
`summary.csv` prints; the issue’s own 15-digit displays are quotations, as above.
Each is written as an exact rational `center-basis` Witness/v2 under [facts/](facts/),
the deciding witness of the maintained exact route, naming its certificate’s SHA-256 as
`revision_sha256`, and stored compressed.
The facts are this repository’s derivation; no upstream byte is retained, and offline
each fact must rebuild itself from the certificate it states.
The declaration of the import is [acquisition/report.json](acquisition/report.json).
The five `sources/` certificates are not offered as records and are not imported.

Only the facts enter geometry decisions, through the two-route kernel of
`devtools.evand_arrangement_reports`: `sqpack`’s exact witness verifier and the
independent rational corner checker, each deciding every wall and every pair over
$\mathbb{Q}$. Each count ran a positive job, a duplicate-square control and an
outside-container control, each in its own child process.
All nine positives pass both routes, and both routes refuse all 18 controls, the
duplicate-square controls on the overlap of squares 0 and 1 and the outside-container
controls on square 0’s wall.
In every positive both routes find the least wall clearance exactly 0: squares touch the
box, a closed-box packing, which is what $s(n) \le S$ asks and both routes accept.
Both find the least pair gap $10^{-32}$ to 16 significant digits, above it by about
$5.6 \times 10^{-49}$, the clearance the source states.
The 27 jobs made 1,743,036 pair decisions in 1,253.51 route CPU seconds and 2,322.21 job
wall seconds, summed; the longest job, the duplicate-square control at 304, took 202.56
seconds. The one-worker run took 40 minutes 10 seconds of wall time, from
2026-10-11T20:39:56Z, while other lanes raised the machine’s load average from 2 to 14
on four cores. The whole receipt is 2,412,308 bytes of uncompressed evidence, under the
kernel’s 4,000,000-byte ceiling, so it is kept whole as
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz), with every
deciding input and both routes’ complete outputs.
`check --replay` then decided all 27 jobs again in one process and found each equal to
its retained row, in 53 minutes 41 seconds of wall time from 2026-10-11T21:20:20Z, at a
load average of 12 to 19. The two routes share certificate parsing, the half-angle
conversion, Python’s rational arithmetic and the separating-axis method.

## What Is Not Established

The source reports that SQUISH’s exact `Fraction` checker accepts all nine, testing
every pair close enough to touch by separating axes and every square against the box,
and that David Ellsworth’s `check_packing.py` accepts each 50-digit export and the
`sources/` exports at $\varepsilon = 10^{-50}$. It reports drawing each certificate from
a 60-digit contact solution with clearance $10^{-32}$, so that each side is within about
$10^{-30}$ of the bottom of its arrangement, and that an hour of nearby search and a
deep squeeze moved none by more than $7 \times 10^{-7}$. Those are author reports; no
program of the source has run here, and the replay above has not been reviewed.
The certificates establish finite upper bounds only.
The source gives no KKT, interval or local-optimality evidence, no closed forms and no
optimality claim.

## Credit

The source credits Nate Chaoweeraprasit, using SQUISH (SQuare-packing Using Iterative
Shrink-Hopping) and its Mondrian composition method.
Its lineage names the packings the pieces came from, and the issue body gives each
count’s pieces:

| n | Pieces, as the source names them | After composition |
| --- | --- | --- |
| 176 | Francisco Couzo’s $s(127)$ (#451, commit `ffd900d`), 121 squares with a 2 × 3 corner of cells taken out, interlocked with the Kingbird catalogue’s $s(5)$, whole | one square added by the search |
| 181 | SQUISH’s unfiled $s(154)$, 37 squares narrowed (`squish-s154-a-source`), and its other $s(154)$, 42 squares narrowed (`squish-s154-b-source`) | seam repair |
| 238 | SQUISH’s unfiled $s(305)$, 68 squares narrowed (`squish-s305-source`), and $s(154)$, 42 squares narrowed (`squish-s154-b-source`) | seam repair, nearby search |
| 239 | SQUISH’s #401 $s(209)$ as refined by Siddharth Gupta, 57 squares narrowed, and SQUISH’s unfiled $s(240)$, 52 squares narrowed (`squish-s240-b-source`) | seam repair |
| 270 | SQUISH’s #481 $s(209)$, whole, and the Kingbird catalogue’s former $s(19)$, 3 squares narrowed | seam repair, nearby search |
| 271 | SQUISH’s unfiled $s(305)$, 68 squares narrowed, and its $s(240)$ of #481’s `sources/`, 47 squares | seam repair, nearby search |
| 272 | SQUISH’s $s(240)$ of #481’s `sources/`, 63 squares, and the Kingbird catalogue’s former $s(182)$, 58 squares narrowed | seam repair, squeeze |
| 304 | SQUISH’s #481 $s(209)$, whole, and the Kingbird catalogue’s former $s(11)$, 8 squares narrowed | seam repair |
| 305 | SQUISH’s unfiled $s(272)$, two pieces of 63 squares narrowed (`squish-s272-source`, the 272 here before its squeeze) | seam repair, nearby search |

By finder, as the source lists them: Francisco Couzo’s $s(127)$ in 176; the Kingbird
catalogue’s $s(5)$ in 176 and its former $s(11)$, $s(19)$ and $s(182)$ in 304, 270 and
272; Siddharth Gupta’s refinement of SQUISH’s #401 $s(209)$ in 239; and SQUISH’s own
packings in the rest.
This is author-reported lineage, not an independently established construction history.

The issue states that SQUISH’s solver, its verification and the issue were written with
Claude Opus 5.5 for coding and research, that the Mondrian composition method was
planned, ideated and formulated by the author and then implemented with Claude Opus 5.5,
and that the SQUISH project is directed, managed, reviewed and steered by Nate
Chaoweeraprasit.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source squish-500-fourth-request-2026-10-11 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports squish-500-fourth-request-2026-10-11 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports squish-500-fourth-request-2026-10-11 check --replay
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports squish-500-fourth-request-2026-10-11 derive --checkout CHECKOUT --check
```

`--check` re-derives the record from this packet alone.
The importer’s `check-claims` and `check --replay` run offline from the facts;
`derive --check` needs a checkout at the pin, refuses one that does not yield this
packet’s record and manifest, and compares each fact it derives with the retained one.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `facts/n-176.yaml.gz` | receipt | `29ee0d60792c9eb1e7f4b07377af3e7a155ed02d` | `3411e2e020efa5a23d270dab67280c297b91070b83142649c75967388a68e03c` |
| `facts/n-181.yaml.gz` | receipt | `166825aecb0a4d18d21bd8ddfc37cb64d3f2184a` | `d657a0ce32517fd9c507de20a82f8afcf7a5810f2974ff6dfca0baa26bae5238` |
| `facts/n-238.yaml.gz` | receipt | `3c7dddf76d779af75361c523a97b69bd02ccbcb5` | `31f8ca6609a0711e3fc7abcaf30703f871c5b150aa8edec34d90b408ba7bd435` |
| `facts/n-239.yaml.gz` | receipt | `fc4dff44800b88ff87550b71d7c28e387e046037` | `58a4bd4c096b6a5c7f0daf53c1247ff12dc7b748ed196d6237f23b8a65c252fb` |
| `facts/n-270.yaml.gz` | receipt | `85c622f51adbf7c262735ba485f6d17b7670e4a5` | `45c6bfcf6648adae2d44c5d18bb91d1a664d03468d3de050363351035d22bc4e` |
| `facts/n-271.yaml.gz` | receipt | `9ca0110f52db7a2e74acf82e3ef7ebb1fbb853ae` | `8229ab50528ea9abf7db638f74500fa22fd2ee94aee254622d2d3c4d5fda1b6a` |
| `facts/n-272.yaml.gz` | receipt | `14643935fef3635946f0232fa3f0e6fa27485c40` | `712b10b9f30dd26fbcd9c4d66893ef7abf45cb51aa20ba3780be0483af4533f4` |
| `facts/n-304.yaml.gz` | receipt | `b22f57e82fafe9cb5266c9b4e84d5cd46f5a116d` | `673d6a9d6f5aa9092423776a73e2a0b00ab3daddf2bab746c7c8899f4b574afd` |
| `facts/n-305.yaml.gz` | receipt | `9e19b75d0cdd8b5ab5031c6ac71d0b281907d689` | `76e51da873c947d51b411774e96beea7979efb919ee560a34ca8930f0294f593` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
