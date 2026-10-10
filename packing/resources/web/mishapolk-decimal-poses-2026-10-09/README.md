# Mishapolk: Decimal Poses at Thirty Counts, n = 84 to 306

[Issue #470](https://github.com/jlevy/squares/issues/470) reports decimal packings below
the register at 28 counts, in
[Mishapolk/square-packing-records](https://github.com/Mishapolk/square-packing-records/tree/dd3da5c753c5ded6cb3b89476193b7b801005415/certificates).
This packet pins `dd3da5c753c5ded6cb3b89476193b7b801005415` (tree
`db3e1d43e22924153213d7a50ed085febadf2eb0`, committed 2026-10-09T08:56:05Z), the
repository head when the source was retrieved at 2026-10-10T09:54Z.

## The Pin the Issue States

The issue’s errata pin the corrected certificates at
`dd3da5c7b39f3796d19e0970bc2350ef9ea14ad`, and link a tree at that string. It has 39
hex digits, and the GitHub API finds no commit by it. The repository’s four commits are:

| Commit | Committed (UTC) | What it changes |
| --- | --- | --- |
| `4e1a6019fe6de6c9ff5b90b93826dcb34899b7de` | 2026-10-09T07:20:27Z | The 28 poses and drawings, the README and `check_packing.py` |
| `2b76e6f7b80cc97b694ab4133e07fe094b8f9c2c` | 2026-10-09T08:26:32Z | Eighteen poses and drawings at $n = 343$ to $360$, and the README |
| `06b484b98f06f13e7b69ec3ef30318996360ac32` | 2026-10-09T08:47:59Z | Poses at $n = 132$ and $267$, and the README |
| `dd3da5c753c5ded6cb3b89476193b7b801005415` | 2026-10-09T08:56:05Z | `square-199.txt` and `square-263.txt` re-quenched, and the README |

`dd3da5c753c5…` shares the stated string’s first eight digits, is `main`, and is the only
commit after `4e1a601` that changes `square-199.txt` or `square-263.txt`. Its 28 pose
files have exactly the SHA-256 digests the issue lists. It is therefore the commit the
errata mean, and this packet pins it. The drawings `square-199.svg` and `square-263.svg`
were last changed in `4e1a601`, so they still draw the replaced poses.

## Every Claim the Release Makes

The issue claims $s(n) \le S_n$ at 84, 86, 88, 103, 105, 108, 127, 130, 131, 153, 154,
175, 179, 180, 199, 207, 208, 209, 236, 237, 238, 239, 258, 263, 270, 302, 303 and 306.
Each $S_n$ is the side printed in `certificates/square-<n>.txt`, rounded up at 12
decimals, and all 28 agree with the files. At 88 the issue says $S_n$ ties SQUISH’s
12-decimal display.

The release holds 20 more poses that the issue does not name:

- **$n = 132$ and $267$**, which the README lists with $S_{132} = 11.986956226066$ and
  $S_{267} = 16.838828608296$. Issue #476 cites slightly different Mishapolk values,
  `11.986956226077` and `16.838828608311`, which match neither file. Both files are the
  same blob at `06b484b` and at the pin.
- **$n = 343$ to $360$**, which the README calls records. Every printed side is at
  least `19.000000000004`, above the grid bound $s(n) \le 19$ that holds for every
  $n \le 361$. All eighteen lie beyond the 1–324 case corpus and above a trivial bound,
  so none asks for a register entry and each stays in this packet. The README’s
  printed sides for 349 to 358 do not match the files either: it prints
  `19.000000000004` where the files print 19.143 to 19.265.

## Source Custody

The tree has no licence file and its README states no reuse terms.
Under the derived-only form of the
[existing retention policy](../known-best-packings/README.md), as for the
[Couzo twenty reports](../couzo-extended-reports-2026-10-08/README.md), this packet keeps
no upstream byte. No redistribution permission or licence determination is asserted.

`devtools.acquire_source` wrote the packet from a clone checked out at the pin, from the
declaration in [acquisition/declaration.json](acquisition/declaration.json).
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the
manifest. All 96 files of the tree, 2,960,637 bytes, are pinned only; the declared
`source/` directory is empty by design. They are the README (blob
`b4b1c4e6252317ff01ecb7277a7664b008c3b242`), a copy of David Ellsworth’s
`check_packing.py` (blob `716c1562b711da0ab5908cf8deab40bc1264737e`, never executed
here), 48 pose files and 46 drawings. The 30 in-horizon poses are:

| n | Pose file | Git blob | Bytes | SHA-256 |
| --- | --- | --- | --- | --- |
| 84 | `certificates/square-84.txt` | `04a98f490cd9bf93bcfd5bf5106ec27480e3f33e` | 6709 | `6819807c98b716afbadd13e8cde7a2ed74392b7b07069865f42170ecbf8bdc8c` |
| 86 | `certificates/square-86.txt` | `90fe9c755811e8fc3f327ec5acc96d68a5322453` | 6856 | `10aabbe0cc7be597218ea7013606c12d073c0653aee52e86ba1ff94f5f5bd2ed` |
| 88 | `certificates/square-88.txt` | `9837f4e9c45ebf165619ab49dbd291ba9b49674f` | 7006 | `67f60fd35d74f7be01025e25d63f985b30eed5e01eda7b0ab8c3167b62451344` |
| 103 | `certificates/square-103.txt` | `81f60dedd1f787abdd00e8ddfa47e4ebf428f4fa` | 8256 | `66e946e5848f2febfca351dddc037a78539cc8591573806cbb0061f896c74d7b` |
| 105 | `certificates/square-105.txt` | `0686ef227bc62e7eff50d5e103ac6913c556bff7` | 8405 | `28a72a9bd4b2b5f88010b380ad696709b8aafd0a3e980fa179cf19061ecc587f` |
| 108 | `certificates/square-108.txt` | `b5227925250be5fb90efa73047b8db838d999724` | 8604 | `deb836cd3c4d64b2a9ab655f53ca4187226dedc6fbe326ff6b6532f8a1c4ef00` |
| 127 | `certificates/square-127.txt` | `caf80c87ce7cd253cd9c299e9168c86090b6cca8` | 10134 | `d72ea01c8fd69d892687a0367ca6da56d62a0867a248ff15e66fb26406e97cb3` |
| 130 | `certificates/square-130.txt` | `419167a2044fe791b5b954ad62d0a2abf25e1333` | 10418 | `46eba43ea47e25db18e0610adaa581c736a7d8b445c33233558fec672a190691` |
| 131 | `certificates/square-131.txt` | `1e845601d4d80a4f424f83b56ee5c409c7d69b3d` | 10494 | `9fe179d60eed2c802ef04617a00619895ee8c23e42b36c48c9d66841400129c6` |
| 132 | `certificates/square-132.txt` | `8a0c34af8ef56964161238c8aadee29411af6cf3` | 18493 | `89115e7393c4d5afafcdd4046f85f8b33d8211503b5aac8143771c7771f40f43` |
| 153 | `certificates/square-153.txt` | `3c348c7285279cfdd8072929ada9f679cd1e0b46` | 12245 | `341a2dc94e0aa8f63bd68e7e87839bf8519377726a8e313434002afddd9463e3` |
| 154 | `certificates/square-154.txt` | `e02e33fd54eeaa26beaa12a8bc5c040b653966d1` | 12359 | `1cea4c25064042c4ef0c5b300b08067ad398680263ac09b79cdfb7ac7cc868c3` |
| 175 | `certificates/square-175.txt` | `9b6238b3967ecb8832fcb885a848143c58a50835` | 14055 | `a3f44fa83b163cdde2ec0abaeb65c2c537b781eac1361e94c29c216f0a4d92cf` |
| 179 | `certificates/square-179.txt` | `58f033ab0a7fa4eadda2f6abffdcd5dab291b453` | 14349 | `e92d88ae577ae47d0efeacbc2aedcc683305b1bd639f97dae86363f532102e07` |
| 180 | `certificates/square-180.txt` | `c3b607a01e612672a1bd51f72e8c97fa53f53bc8` | 14457 | `8edafd0411efd93b831729ab7b63d368a26cf3e4676c6792b61ce74c26289fda` |
| 199 | `certificates/square-199.txt` | `a60ffbd2670676d371636701306a6b68b287982e` | 27927 | `8f4212771950c2824156190f67e1cc205305fad58457cf261f43c079454e4c87` |
| 207 | `certificates/square-207.txt` | `220de7114a0e4709e6226b0d27e2f63f75df9b8a` | 16613 | `c01242eb1b32d72d719f0d50d3bad4e9f9d05523371dd971e6c3a642a96e1212` |
| 208 | `certificates/square-208.txt` | `03fecf78c6b0f79f974acb44f62be7b5ceab04ae` | 16716 | `b2d9d5e70aef2b1d3fa15259382d11a7fed383925af674b266586c9fe6264f04` |
| 209 | `certificates/square-209.txt` | `1496494161bac1c9c96b444ea4f1bf2fb48e197e` | 16806 | `c7c26dc4f8eb76afabd991ed82b1b73eb068ca118f691750c75b2f399c2ff1a5` |
| 236 | `certificates/square-236.txt` | `ed4b677af9a979485c6daf85d8fe76986d398216` | 18973 | `440f31dff992dc19b35b3964d82e46bc5ab81650b679b7670439fcba0ca72988` |
| 237 | `certificates/square-237.txt` | `03e7272487c50297125853712e326a216b2311ea` | 19063 | `49f1150110face947e945f4ea8058c781c15d1a3bca7c4dc32f67795df534ab7` |
| 238 | `certificates/square-238.txt` | `0b6fd2ba7d5890886ac11c5a2d6fc83d6a0a75e5` | 19098 | `43dbdcd41300760a40ec32e105de156d8bbf8f7bdde55aee161a898fc14dceda` |
| 239 | `certificates/square-239.txt` | `aa40996914228543f52dc9ae194b885bea8bf5bc` | 19190 | `819aca7c56b1562bc890f4ed8cf1dc650d9f7f7c0f5d36be25368198a5cf57e6` |
| 258 | `certificates/square-258.txt` | `1f6b29dbf26bc03e524af6baebd21467619607e8` | 20696 | `0cc2a7d9854080ac700939eefe3489f4dedae0f6c9d032419e39a37ecfc00bc6` |
| 263 | `certificates/square-263.txt` | `d33ed53c3f7d1b8cf007cb0c0d96bcc2a63c12b4` | 36921 | `9b2d1cda5eb57dd7709a50db7c8c62d92da906a1455974c1dee4b2cdacd0a97c` |
| 267 | `certificates/square-267.txt` | `b31ce132f6a53f34cb5e7eedddd4b778a6f66723` | 37481 | `4802db4f295af62d909e8e6a710e597b7e135f2fbb947a8dbf31eb1c6946e655` |
| 270 | `certificates/square-270.txt` | `4d7c91dc58581bec7bc890678b12890e077f75df` | 21753 | `6b8b4addbf5cbc24b7c38c0acc0e3516835061091d0ad989bd0e4e65fe1d789c` |
| 302 | `certificates/square-302.txt` | `c2020cdd046c7ba40a3fa4933f4a840255a67569` | 24245 | `6b6a9152623e3428184a83c85ad67f28d5f74a4c29ec383bbd16c428b78c652a` |
| 303 | `certificates/square-303.txt` | `a816723d5e0cf33051f8ff0b601e7a3e03a707b5` | 24318 | `8062a183e1060abf8d45a032a72cd9f4832d7aa437de3d5cf0628f9dffe6d6f5` |
| 306 | `certificates/square-306.txt` | `a4b2c2059c17a89e630861e14e46d8e02398f7a5` | 24639 | `47b488cfb7740516869266fb26b41911a37242533188f9bd6fedb919623430d2` |

## The Poses Are Decimal

Each pose file is David Ellsworth’s text format: `s: SIDE`, then
`Square K: x=X, y=Y, deg=D` per square, the box $[-s/2, s/2]^2$ and the angle in degrees.
The coordinates carry 16 decimals, or 36 at 132, 199, 263 and 267. No file is an
exact witness: the angles’ cosines and sines are not rational, and the printed digits
are rounded. An exact witness therefore needs two declared steps the source does not
take: centres dilated about the box centre to a stated side, and each rotation replaced
by a rational half-angle tangent close to the printed angle. The record has taken
decimal reports the same way before, through `sqpack.witness.promote_rational`.

## Measured at the Printed Digits

`devtools.decimal_pose_margins` reads every printed decimal exactly and encloses each
cosine and sine in outward-rounded interval arithmetic at 60 working digits. For every
pair whose centres lie within 2, it encloses the best separating-axis gap, which is
negative exactly when the interiors overlap. For every square it encloses the least
corner clearance from the box. It measures each pose at its printed side $s$, and at
$S_n$ with the centres dilated by $\lambda = S_n / s$ about the box centre.
[receipts/decimal-pose-margins.json](receipts/decimal-pose-margins.json) holds all 30
measurements, bound to each file’s SHA-256. Its `check` re-measured all 30 in 4.5
seconds and reproduced the receipt.

At the printed side, 11 poses are proved packings and 19 are proved not to be: 12
have pairs that overlap, by at most $1.28 \times 10^{-15}$, and 17 have corners
outside the box, by at most $1.2 \times 10^{-15}$. With the declared dilation to $S_n$,
**every one of the 30 is proved a packing**. Its least pair gap is then at least
$6.6 \times 10^{-16}$, at 238, and its least wall clearance at least
$4.7 \times 10^{-16}$, at 84.

| n | Printed side $s$ | $S_n$ | At $s$ | Least pair gap at $s$ | Least wall at $s$ | Overlapping pairs, outside squares | $\lambda - 1$ | At $S_n$ | Least pair gap | Least wall |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 84 | 9.6979347990169860 | 9.697934799017 | not a packing | 2.00e-13 | -2.48e-16 | 0, 4 | 1.44e-15 | packing | 2.02e-13 | 4.74e-16 |
| 86 | 9.8205354074987188 | 9.820535407499 | packing | 2.01e-13 | 1.00e-13 | 0, 0 | 2.86e-14 | packing | 2.29e-13 | 1.14e-13 |
| 88 | 9.8824510304812740 | 9.882451030482 | packing | 1.79e-15 | 1.93e-15 | 0, 0 | 7.35e-14 | packing | 7.53e-14 | 3.87e-14 |
| 103 | 10.6792320473613369 | 10.679232047362 | packing | 2.29e-15 | 7.36e-16 | 0, 0 | 6.21e-14 | packing | 6.44e-14 | 3.18e-14 |
| 105 | 10.7893037837503627 | 10.789303783751 | packing | 2.03e-13 | 9.99e-14 | 0, 0 | 5.91e-14 | packing | 2.62e-13 | 1.29e-13 |
| 108 | 10.9048210123231399 | 10.904821012324 | not a packing | 2.00e-13 | -5.00e-17 | 0, 32 | 7.89e-14 | packing | 2.79e-13 | 3.94e-14 |
| 127 | 11.8108787875891803 | 11.810878787590 | not a packing | -1.28e-15 | -2.01e-16 | 45, 28 | 6.94e-14 | packing | 6.81e-14 | 3.47e-14 |
| 130 | 11.9044830325157864 | 11.904483032516 | not a packing | -8.21e-16 | -3.47e-16 | 37, 4 | 1.79e-14 | packing | 1.71e-14 | 8.97e-15 |
| 131 | 11.9511053894179291 | 11.951105389418 | not a packing | 2.00e-13 | -7.71e-17 | 0, 7 | 5.93e-15 | packing | 2.06e-13 | 2.89e-15 |
| 132 | 11.986956226065860… | 11.986956226066 | packing | 2.02e-13 | 1.02e-13 | 0, 0 | 1.16e-14 | packing | 2.14e-13 | 1.08e-13 |
| 153 | 12.8796793733319035 | 12.879679373332 | packing | 2.00e-13 | 1.00e-13 | 0, 0 | 7.49e-15 | packing | 2.07e-13 | 1.04e-13 |
| 154 | 12.9265622458523470 | 12.926562245853 | not a packing | -4.69e-16 | -1.53e-16 | 40, 6 | 5.05e-14 | packing | 5.02e-14 | 2.52e-14 |
| 175 | 13.7671551635504397 | 13.767155163551 | not a packing | 6.04e-13 | -1.94e-16 | 0, 2 | 4.07e-14 | packing | 6.45e-13 | 2.02e-14 |
| 179 | 13.8837954905110159 | 13.883795490512 | packing | 7.51e-15 | 1.08e-15 | 0, 0 | 7.09e-14 | packing | 7.84e-14 | 3.65e-14 |
| 180 | 13.9169935224813184 | 13.916993522482 | not a packing | 2.00e-13 | -4.89e-17 | 0, 11 | 4.90e-14 | packing | 2.49e-13 | 2.44e-14 |
| 199 | 14.617572173596022… | 14.617572173597 | packing | 2.04e-13 | 1.00e-13 | 0, 0 | 6.69e-14 | packing | 2.70e-13 | 1.34e-13 |
| 207 | 14.8879922583026598 | 14.887992258303 | not a packing | -4.23e-16 | 0 | 42, 0 | 2.29e-14 | packing | 2.24e-14 | 1.14e-14 |
| 208 | 14.9245187720293568 | 14.924518772030 | not a packing | -7.63e-16 | -2.96e-16 | 99, 1 | 4.31e-14 | packing | 4.23e-14 | 2.15e-14 |
| 209 | 14.9496179522003985 | 14.949617952201 | not a packing | -7.47e-16 | -2.24e-16 | 80, 3 | 4.02e-14 | packing | 3.96e-14 | 2.02e-14 |
| 236 | 15.8678008394207701 | 15.867800839421 | not a packing | -8.57e-16 | -3.73e-16 | 98, 51 | 1.45e-14 | packing | 1.39e-14 | 7.19e-15 |
| 237 | 15.9036762351891383 | 15.903676235190 | not a packing | -9.64e-16 | -5.00e-17 | 68, 52 | 5.42e-14 | packing | 5.35e-14 | 2.70e-14 |
| 238 | 15.9261468570109788 | 15.926146857011 | not a packing | -6.72e-16 | -1.24e-16 | 89, 1 | 1.33e-15 | packing | 6.59e-16 | 6.66e-16 |
| 239 | 15.9493131697276969 | 15.949313169728 | not a packing | -8.60e-16 | -9.13e-18 | 105, 1 | 1.90e-14 | packing | 1.81e-14 | 9.55e-15 |
| 258 | 16.5634480021371502 | 16.563448002138 | packing | 2.01e-13 | 9.98e-14 | 0, 0 | 5.13e-14 | packing | 2.52e-13 | 1.25e-13 |
| 263 | 16.740419683046905… | 16.740419683047 | packing | 2.96e-13 | 1.97e-13 | 0, 0 | 5.65e-15 | packing | 3.01e-13 | 2.00e-13 |
| 267 | 16.838828608295706… | 16.838828608296 | packing | 4.21e-13 | 3.18e-13 | 0, 0 | 1.74e-14 | packing | 4.38e-13 | 3.27e-13 |
| 270 | 16.9367231550373418 | 16.936723155038 | not a packing | 2.01e-13 | -2.43e-16 | 0, 1 | 3.89e-14 | packing | 2.40e-13 | 1.92e-14 |
| 302 | 17.8813062180900033 | 17.881306218091 | not a packing | -9.00e-16 | -5.00e-17 | 94, 48 | 5.57e-14 | packing | 5.48e-14 | 2.78e-14 |
| 303 | 17.9203123729186586 | 17.920312372919 | not a packing | -8.28e-16 | 0 | 141, 0 | 1.91e-14 | packing | 1.84e-14 | 9.53e-15 |
| 306 | 17.9634337174962369 | 17.963433717497 | not a packing | 2.00e-13 | -1.20e-15 | 0, 5 | 4.25e-14 | packing | 2.43e-13 | 2.00e-14 |

Values are the receipt’s lower enclosure endpoints, cut to three digits; the receipt
keeps eight, rounded outward, with both endpoints.
Squarepacker’s finding that the other 26 files of `4e1a601` overlap by at most
$1.3 \times 10^{-15}$ agrees with these measurements: they are rounding of the last
printed place. The dilation that $S_n$ declares pays for it at every count.

A `packing` verdict at $S_n$ is an interval proof that the dilated published pose packs
$n$ unit squares in the square of side $S_n$. It is not an exact witness, and it is not
a replay of the source’s check. Rounding each angle to a rational half-angle tangent at
30 or more digits moves no corner by more than about $10^{-29}$, far inside every margin
above, so an exact witness at $S_n$ is expected to exist at every count; the exact route
decides that, and none has been built here.

### Control: the Replaced 199 and 263

[receipts/decimal-pose-margins-4e1a601-control.json](receipts/decimal-pose-margins-4e1a601-control.json)
measures the `4e1a601` versions of `square-199.txt` (SHA-256
`5fbcf14b4d86dcaf10a28e8cb45d6c317031dac31b4df1c60fed8619edb24cdb`) and `square-263.txt`
(`7ad9b9f96280a4433e016dc675d1dfe3379ebff5e48301ed2ac7002381f803b5`), read from the clone with `git show`. Both are
proved not to be packings, at their printed sides and at their own 12-decimal ceilings.
At 199 the deepest pairs are squares 15 and 35 at $-5.0127245 \times 10^{-10}$ and 24
and 35 at $-2.3122402 \times 10^{-12}$. At 263 the deepest is $-1.3611608 \times 10^{-6}$,
at squares 173 and 246 and at 192 and 246, with 130 pairs overlapping. These match the
depths
[squarepacker reported](https://github.com/jlevy/squares/issues/470#issuecomment-6077002689)
from an independently written 60-digit checker.

## Against the Record

[acquisition/declaration.json](acquisition/declaration.json) lists each claim. Against
`main` `657cc4861` and every report pending on 2026-10-10, by exact comparison:

| n | $S_n$ | Case verified ceiling, house | Below it by | Smaller report dated earlier | Smaller report dated later |
| --- | --- | --- | --- | --- | --- |
| 84 | 9.697934799017 | 9.6980520605096981, [ry-xu square packing 2026] | 1.17e-04 | T-130, 9.6979347990149214 | |
| 86 | 9.820535407499 | 9.8205657300098206, [ry-xu square packing 2026] | 3.03e-05 | T-130, 9.8205354074967423 | |
| 88 | 9.882451030482 | 9.8824510304812469, [Gupta rational refinements 2026-10-08] | -7.53e-13 | the case | |
| 103 | 10.679232047362 | 10.6792320475106793, [ry-xu square packing 2026] | 1.49e-10 | none | none |
| 105 | 10.789303783751 | 10.7906765754107907, [ry-xu square packing 2026] | 1.37e-03 | T-130, 10.7893037837481589 | |
| 108 | 10.904821012324 | 10.9048247851109049, [ry-xu square packing 2026] | 3.77e-06 | T-128, 10.9048210123203565 | |
| 127 | 11.810878787590 | 11.8109366475118110, [ry-xu square packing 2026] | 5.79e-05 | T-128, 11.8108787875891799 | |
| 130 | 11.904483032516 | 11.9044830325157865, [Gupta rational refinements 2026-10-08] | -2.14e-13 | the case | |
| 131 | 11.951105389418 | 11.9511500449119512, [ry-xu square packing 2026] | 4.47e-05 | T-128, 11.9511053894146775 | #481, 11.9496595880358604 |
| 132 | 11.986956226066 | 11.9913278876915015, [evand exact optima 2026-10-05] | 4.37e-03 | none | #476, 11.9869541936403928 |
| 153 | 12.879679373332 | 12.8796793733293146, [Gupta rational refinements 2026-10-08] | -2.69e-12 | the case | #481, 12.8720298490811809 |
| 154 | 12.926562245853 | 12.9265622458523470, [Gupta rational refinements 2026-10-08] | -6.53e-13 | the case | #481, 12.9230702023011408 |
| 175 | 13.767155163551 | 13.7688992766137689, [ry-xu square packing 2026] | 1.74e-03 | T-130, 13.7671551635425492 | |
| 179 | 13.883795490512 | 13.8837954905108985, [Gupta rational refinements 2026-10-08] | -1.10e-12 | the case | |
| 180 | 13.916993522482 | 13.9176534174501843, [Gupta rational refinements 2026-10-08] | 6.60e-04 | T-128, 13.9169935224778325 | |
| 199 | 14.617572173597 | 14.6175721735928069, [Gupta rational refinements 2026-10-08] | -4.19e-12 | the case | |
| 207 | 14.887992258303 | 14.8879922583026574, [Gupta rational refinements 2026-10-08] | -3.43e-13 | the case | #481, 14.8855063088416777 |
| 208 | 14.924518772030 | 14.9245187720293559, [Gupta rational refinements 2026-10-08] | -6.44e-13 | the case | |
| 209 | 14.949617952201 | 14.9496179522003981, [Gupta rational refinements 2026-10-08] | -6.02e-13 | the case | #481, 14.9462236544879195 |
| 236 | 15.867800839421 | 15.8678008394199166, [Gupta rational refinements 2026-10-08] | -1.08e-12 | the case | #481, 15.8639557471592678 |
| 237 | 15.903676235190 | 15.9036762351891381, [Gupta rational refinements 2026-10-08] | -8.62e-13 | the case | #476, #481, 15.9029892208749656 |
| 238 | 15.926146857011 | 15.9261468570109784, [Gupta rational refinements 2026-10-08] | -2.17e-14 | the case | |
| 239 | 15.949313169728 | 15.9493131697276962, [Gupta rational refinements 2026-10-08] | -3.04e-13 | the case | |
| 258 | 16.563448002138 | 16.5634480021391540, [SQUISH update 2026-10-07] | 1.15e-12 | none | none |
| 263 | 16.740419683047 | 16.7404196795387766, [SQUISH second update 2026-10-07] | -3.51e-09 | the case | #476, #481, 16.7331660078998839 |
| 267 | 16.838828608296 | 16.8388319611168389, [ry-xu square packing 2026] | 3.35e-06 | none | #476, 16.8388152699482623 |
| 270 | 16.936723155038 | 16.9378072284460292, [Daniel new arrangements 2026-10-07] | 1.08e-03 | T-130, 16.9367230228761835 | #476, #481, 16.9297801262411717 |
| 302 | 17.881306218091 | 17.8813062180958085, [SQUISH second update 2026-10-07] | 4.81e-12 | none | #481, 17.8720298490811800 |
| 303 | 17.920312372919 | 17.9203123729203498, [SQUISH ten packings 2026-10-07] | 1.35e-12 | none | #476, #481, 17.9130654627385328 |
| 306 | 17.963433717497 | 17.9634381397640029, [evand exact optima 2026-10-05] | 4.42e-06 | T-128, 17.9634337174914258 | |

T-128 and T-130 are Francisco Couzo’s exact certificates of issues #451 and #460,
committed on 2026-10-08, before the release. #476 is Couzo’s, committed
2026-10-09T20:28Z, and #481 is SQUISH’s, committed 2026-10-09T21:23Z, both after it. A
later column naming several reports gives the smallest.

So $S_n$ is the smallest side known only at **103**, $1.49 \times 10^{-10}$ below Ryan
Xu’s certificate, and **258**, $1.15 \times 10^{-12}$ below SQUISH’s. At 132, 267, 302
and 303 it was the smallest when published and has since been beaten. At 84, 86, 105,
108, 127, 131, 175, 180, 270 and 306 an earlier certificate of Couzo’s is smaller. At
88, 130, 153, 154, 179, 199, 207, 208, 209, 236, 237, 238, 239 and 263 it is not below
the case’s verified ceiling.

Several printed sides lie within $10^{-15}$ to $10^{-11}$ of an earlier certificate’s side
at the same count. At 127 the printed side is $4.6 \times 10^{-16}$ above T-128’s; at 130,
$4.0 \times 10^{-17}$ below Gupta’s; at 208, 238 and 239, under $10^{-15}$ above Gupta’s.
The replaced `4e1a601` pose at 199 printed `14.6175721735928068`, the case’s Gupta side cut
at 16 places. The issue’s lineage leaves credit with Stenlund, Friedman, Ellsworth,
SQUISH, Couzo and Ryan Xu where a packing started from the literature, and does not name
Siddharth Gupta or say which count started from which packing. This packet compares sides
only; it has not compared poses, and no priority finding is made.

## What Is Not Established

The issue reports that Ellsworth’s `check_packing.py`, at precision 40 and
$\varepsilon = 10^{-14}$, and an independent 60-digit separating-axis check accept all
28, and that shrinking the container by $10^{-9}$ or moving a square $10^{-6}$ is
refused. Those are author reports, and no program of the source has run here. The
measurements above are interval-certified statements about the dilated published poses.
They are not an exact witness, a replay of the source, or evidence of the KKT
stationarity the issue reports. No optimality is claimed.

## Credit

The issue credits the original discoverers wherever a packing started from the
literature, and describes its method as grain-boundary constructions at rational and
Pythagorean angle families, quasi-static SLSQP on active contact manifolds and
active-set KKT Newton refinement. It discloses Gemini 3.8 assistance with solver
scripting, precision checks and formatting. Squarepacker’s audit of `4e1a601` found the
two overlapping files that `dd3da5c` replaced.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source mishapolk-decimal-poses-2026-10-09 --check
uv run --frozen --all-extras --group dev python -m devtools.decimal_pose_margins check \
    resources/web/mishapolk-decimal-poses-2026-10-09/receipts/decimal-pose-margins.json \
    --root CHECKOUT
```

`CHECKOUT` is a clone of the source at the pin; `check` refuses any pose whose bytes
differ from the receipt’s. The control receipt is checked the same way against a
directory holding `certificates/square-199.txt` and `certificates/square-263.txt` from
`git show 4e1a6019fe6de6c9ff5b90b93826dcb34899b7de:certificates/…`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
