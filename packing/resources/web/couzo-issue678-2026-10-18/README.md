# Francisco Couzo’s 85 Upper Bounds at 7b6c87e (Issue #678)

[Issue #678](https://github.com/jlevy/squares/issues/678), filed 2026-10-18T23:23:19Z as
a follow-up to [#675](https://github.com/jlevy/squares/issues/675), reports 85 upper
bounds for n = 204 to 998 from
[franciscouzo/square-packing](https://github.com/franciscouzo/square-packing/tree/7b6c87e129cf80b5ff9847b90b47fd30b4563c54/certificates/best)
at `7b6c87e129cf80b5ff9847b90b47fd30b4563c54`. The packet retains the 83 certificates the
issue links and the source’s exact checker, records the exact replay of all 85 rows, and
compares each claim with the record and the earlier reports in report order.
[T-223](../../../frontier/RESULTS.md) registers the two claims in the case corpus, at 204
and 260, pending adoption; the 83 beyond it are dated beyond-horizon rows of the
`couzo-issue678-2026-10-18` source in
[source-coverage.yaml](../../../frontier/source-coverage.yaml), read from
[acquisition/beyond-horizon-claims.json](acquisition/beyond-horizon-claims.json).

## Source and Dates

| Field | Value |
| --- | --- |
| Source | [franciscouzo/square-packing](https://github.com/franciscouzo/square-packing) |
| Pin | `7b6c87e129cf80b5ff9847b90b47fd30b4563c54`, tree `281b4e1010907d5065d85760ae792f07e1cbd660`, the head of `master` when retrieved |
| Committed | 2026-10-18T23:19:02Z, “Land 85 verified packing bounds and source provenance” |
| Parent | `c6da0fc7524d667bf3d224559724ba9b60762e60`, the pin of #675 |
| Issue filed | 2026-10-18T23:23:19Z, four minutes after the commit |
| Retrieved | 2026-10-19T16:54Z, a blobless clone with a sparse checkout |
| Licence | none for the data or prose; the checker is MIT-licensed (below) |
| Custody | [declaration](acquisition/declaration.json), [acquisition record](acquisition/sources.json), [manifest](acquisition/upstream-subtree.sha256) |

The issue’s three comments, through 15:31:25Z on 19 October, concern the n260 seed’s
custody and are retained with the
[19 October intake packet](../../../campaign/issue-intake/intake-20261019/README.md).
No later comment existed when this packet was written, at 17:16Z.

## What the Commit Changes

Against its parent `c6da0fc`, `7b6c87e` changes 543 files: 89 under
`certificates/best/` (the 85 certificates of the issue’s rows, `n995.cert`, the
directory’s README, `manifest.json` and `SHA256SUMS`), 171 directly under
`certificates/`, 106 under `certificates/parents/` (105 added), the two drawings of each
of the 85 counts, and seven indexes and provenance files at the root.
`n995.cert`, which the issue does not list, is re-certified at side
31.99478454971099…, as the source’s `manifest.json` at the pin states (read from the
pinned checkout, not retained here); that rounds up to the 12-place print #675 already
claims at 995 by another route.
It is not in this packet’s scope.
Every one of the 544 lines of the source’s `certificates/best/SHA256SUMS` matches the
bytes at the pin.

## Retained Here

`devtools.acquire_source` wrote the packet from the declaration; every file is bound to
its Git blob at the pin.
The scope is 92 files, 10,551,438 bytes:

- **retained**, 85 files, 8,112,271 bytes: the 83 linked certificates under
  [source/certificates/best/](source/certificates/best/), 8,107,636 bytes, listed path by
  path below; and the source’s checker
  [verify_bound_certificate.py](source/verify_bound_certificate.py) with its licence
  [BOUND_VERIFIER_LICENSE.txt](source/BOUND_VERIFIER_LICENSE.txt);
- **pinned by digest only**, 7 files: the root `README.md` and `upper_bounds.json`, the
  certificate directory’s `README.md`, `manifest.json` and `SHA256SUMS`, and the
  manifest’s own certificates at 545 and 641, `n545.cert` and `n641.cert`.

The 8.1 MB of certificates are 2.86 MB as zlib stores them, which is how
[OR-18](../../../../operating-rules.md#or-18-keep-bulk-data-out-of-git-and-never-bind-code-or-verdicts-to-a-git-commit-or-blob)
counts them, so they are kept in Git as T-174’s 2.84 MB of houses were.
The other 457 certificates of `certificates/best/`, the 105 parents, the drawings and the
search programs are pinned by the commit alone; none was retained or run.

The repository states no licence for its data or prose. The certificates are retained as
factual data under the owner decision of 2026-10-09
([Retained Factual Data](../known-best-packings/README.md#retained-factual-data)).
`verify_bound_certificate.py` names itself Evan Daniel’s MIT-licensed verifier with
modifications by Francisco Couzo with Codex, under the MIT licence in
`BOUND_VERIFIER_LICENSE.txt` (Copyright (c) 2026 Evan Daniel); both are retained byte
for byte under it.

### The 83 Certificates

Each retained file, its size and its SHA-256, as the manifest records them.

| n | Certificate | Bytes | SHA-256 |
| ---: | --- | ---: | --- |
| 204 | [n204.cert](source/certificates/best/n204.cert) | 21,387 | `e05b904d940a944323a0937cf3844f89f6893700bde121a4f4e07b0f76c5c469` |
| 260 | [n260.cert](source/certificates/best/n260.cert) | 28,284 | `635dbf25a2550f22e4259a850da1ad02f2762527a367d90193458fa644d12908` |
| 330 | [n330.cert](source/certificates/best/n330.cert) | 68,030 | `9791e92c170b81917cfe83a5b7cb3de2f6100ef725d58ec7ed24cd83b9ed34f4` |
| 343 | [n343.cert](source/certificates/best/n343.cert) | 38,535 | `8b333241d7d866ab51ad8ff7b515bc1a77ce86ed79051f215cab7c8633f9fca1` |
| 418 | [n418.cert](source/certificates/best/n418.cert) | 44,446 | `71e1cd97e3c7d4bf3b729c2e9015bcbe20d4110d4cd19c312ff32b79d61ef59e` |
| 420 | [n420.cert](source/certificates/best/n420.cert) | 52,820 | `e9e398d1b76a97d6f60dcd661f7d627695878f344231a9daf1a4852b1ec17467` |
| 421 | [n421.cert](source/certificates/best/n421.cert) | 47,501 | `60dcd91fe8cce93b53a9bee87ea1efa7e7e7ddceffd64f2753d91cac233cf874` |
| 422 | [n422.cert](source/certificates/best/n422.cert) | 45,319 | `86bb323da4b24dcbc1ae7482281711ed105c87390866839ef846bdde1c8c6c7f` |
| 455 | [n455.cert](source/certificates/best/n455.cert) | 132,615 | `e1bc6a75ab6c20d600acefc7c8dd2118f98686b4622700473f030c1769273024` |
| 456 | [n456.cert](source/certificates/best/n456.cert) | 132,981 | `3e4741058092fd12c6ea577b1563b9d7cda88cce746e8386871d0dad6f9426d5` |
| 458 | [n458.cert](source/certificates/best/n458.cert) | 55,671 | `a09eb24d62404214a7b175f5321c8bb7893576a596c059c5ceed41bf315d42dc` |
| 459 | [n459.cert](source/certificates/best/n459.cert) | 50,977 | `c0fd0fa2de705ca170da1c35ef270efc28cc653e269fc1b6181d0edfa0a74a52` |
| 461 | [n461.cert](source/certificates/best/n461.cert) | 51,576 | `e47c7fca79450656d7ffa9f5acae6d82d244c85454c507469dd3184cd32d4e86` |
| 462 | [n462.cert](source/certificates/best/n462.cert) | 134,010 | `23702299fce0d70d80a47cc6bf1e502076ff32d2fcbca8d3db9bc28410a9d3de` |
| 463 | [n463.cert](source/certificates/best/n463.cert) | 52,176 | `9c47a758b698e47b4986c18417aa919f29a7fa5e4ec6597e717e871c0342abf3` |
| 464 | [n464.cert](source/certificates/best/n464.cert) | 52,322 | `65958ec32a4deb7b75225fc39471b43022915b3abaa20fd8f6c4582e0a246bbb` |
| 497 | [n497.cert](source/certificates/best/n497.cert) | 65,120 | `4543960e3a9d572338c7e6e88a6d67d6d88aa17b9877b4a0d38c98de7b1516ab` |
| 499 | [n499.cert](source/certificates/best/n499.cert) | 139,045 | `d23a5c899886f0dd2c0292439f95ebee741a60635fd87d8f4b7ca0b3d03c7a28` |
| 501 | [n501.cert](source/certificates/best/n501.cert) | 58,467 | `47c040636208e7aed818a7c26a1b2fdd19bd62257f35c74c26ea52ed780f9664` |
| 502 | [n502.cert](source/certificates/best/n502.cert) | 62,016 | `a4027c423c0088fae96a8f99fa3534034fc9575da566c43f289d1785fa995c4d` |
| 505 | [n505.cert](source/certificates/best/n505.cert) | 56,577 | `37795285ae24d1ebfc489ff1ba266c5ba3ec53eaeec2cfd8eff3746f485900cf` |
| 507 | [n507.cert](source/certificates/best/n507.cert) | 56,963 | `3fb32a5a25ffc291b367bf637507e632f7e329c7c24000fe6bb6c0e6ce80ca33` |
| 546 | [n546.cert](source/certificates/best/n546.cert) | 71,058 | `3e2c8455e179372d13365352dd9d513f50d76db46d9217291e2af91efc00627e` |
| 548 | [n548.cert](source/certificates/best/n548.cert) | 75,397 | `b7fa50f2029fb209fcfcb0676a0be09d5527bade0df7b2ed8fe5cf2ab933a5ed` |
| 549 | [n549.cert](source/certificates/best/n549.cert) | 75,545 | `3e4a5362221e9bde4823d4307a1e857c3adff13b519c208fc2ccd7c8f1896de6` |
| 553 | [n553.cert](source/certificates/best/n553.cert) | 61,449 | `cffa682971756b9b06a9bf5a4887c0c54af236b23f84a236d7186e621971ee31` |
| 554 | [n554.cert](source/certificates/best/n554.cert) | 75,258 | `8e839ff0acff3e2c54d4ee8fb64b7880f0f93a308ec89914353e697180c66819` |
| 555 | [n555.cert](source/certificates/best/n555.cert) | 73,823 | `5444185e94b1d68cd28872a9ac0f91b2c405633c311b754fd0ea62d8a6443054` |
| 592 | [n592.cert](source/certificates/best/n592.cert) | 68,549 | `69accbbb9a46a1269a2a6d2949dc4436f13382425dac9112966c21e71dee0eb7` |
| 593 | [n593.cert](source/certificates/best/n593.cert) | 63,745 | `ffe0b75adcc6035e388cc9fa89e559d93f868878f2bc5b51eaeda487c6c0ad69` |
| 597 | [n597.cert](source/certificates/best/n597.cert) | 127,197 | `38e9f33594a9ebec8e3579f29ea589d0d003c35e6caa38d51ece7f483ed6d750` |
| 598 | [n598.cert](source/certificates/best/n598.cert) | 127,486 | `b6de88228dbb62a7c3546b3e1a30364468ad0b9cd03745d9e6eb20d771a7d85b` |
| 600 | [n600.cert](source/certificates/best/n600.cert) | 64,353 | `1ac3fe7e9f84fe0c74c72b8efacd1f579f666058744a6727bab53613f9c54f47` |
| 601 | [n601.cert](source/certificates/best/n601.cert) | 68,188 | `2bf27fcc5251c7d3e9095fb744f064c4aa3f0563050e24b373d60d1e43273f88` |
| 602 | [n602.cert](source/certificates/best/n602.cert) | 76,840 | `e417d509ad9dcdb9cbfff478d1f72a9290e199dee07d8dd35a55a8990f05b25d` |
| 642 | [n642.cert](source/certificates/best/n642.cert) | 70,326 | `53898e18e4243e5f660c3c26de25fd326408fbf28b81e0af01ca8b9e7855321a` |
| 650 | [n650.cert](source/certificates/best/n650.cert) | 111,724 | `774fb1042b9c2030b237d67647102032bf8d10c1ed5e3310113d3dbe7f692b02` |
| 652 | [n652.cert](source/certificates/best/n652.cert) | 77,074 | `30028d7a6ccf040cff81738718ca4df67ebd592bcf23c6c89bd4a560c612a2a6` |
| 653 | [n653.cert](source/certificates/best/n653.cert) | 71,473 | `bb80f21fd679cbbc251a1c8ebd73f0c5407b7c19b8ae1e59b7a87a3e00946268` |
| 654 | [n654.cert](source/certificates/best/n654.cert) | 73,700 | `fa0160361aa4c7c72f5250bee804ad0d14a2362049620b23dab475f76a02c20b` |
| 693 | [n693.cert](source/certificates/best/n693.cert) | 78,067 | `9094537f8258034740ee0bb42c8c8b3713928e50a3ccc97c4b3bfbc322332071` |
| 700 | [n700.cert](source/certificates/best/n700.cert) | 77,813 | `01bde818c821e474db9b85549afa23b10b99a544d4a997ba2a4125d2e99fd10b` |
| 701 | [n701.cert](source/certificates/best/n701.cert) | 143,601 | `c268dc5989ed00fae48875e446da5f58733d6f960989f58b267abece8b0c5170` |
| 703 | [n703.cert](source/certificates/best/n703.cert) | 78,416 | `2c22ac8cb4b4e5956ea88dd8ee58969da47b2ac150cce78a283e76f9fcecf8e2` |
| 704 | [n704.cert](source/certificates/best/n704.cert) | 148,835 | `df5cef379b51d8d574b501d74caf0b39e2b5ff6e964119ba1b30396410e6c68b` |
| 705 | [n705.cert](source/certificates/best/n705.cert) | 149,127 | `15a476af34812b95652fcb03602806d03586da60d0aa4b719e70007c4a214298` |
| 706 | [n706.cert](source/certificates/best/n706.cert) | 79,507 | `33d7150d2cf4ebf055ef7335ab8d12f8505781ef6a3b06ed8e806c6217240160` |
| 749 | [n749.cert](source/certificates/best/n749.cert) | 101,745 | `58c469dbbadce3b55616d7e324ab2d381e2603575bcecaee108b239d4d04aaa8` |
| 751 | [n751.cert](source/certificates/best/n751.cert) | 85,437 | `262fbf35c333ac63a7a6587fe4b2d59405dcd7eeec1316c720f312fe925ec704` |
| 752 | [n752.cert](source/certificates/best/n752.cert) | 86,060 | `c5cd53625fe6d15e07ee5a3aae15932023062323abce39b8f02207b10f6710c8` |
| 753 | [n753.cert](source/certificates/best/n753.cert) | 86,188 | `44e47e54620333f8086e3026a6ea5bc2f51396c7818e671f12469205a7ecb90c` |
| 754 | [n754.cert](source/certificates/best/n754.cert) | 81,006 | `d8e7899488e594b0d1289b9374c71a9d4bab12540d2043298f09513ed21ce683` |
| 755 | [n755.cert](source/certificates/best/n755.cert) | 85,787 | `39fec0a910bfa02da60337a43fc6f0b1cab5ffba56a4e88de670889cef73c090` |
| 760 | [n760.cert](source/certificates/best/n760.cert) | 86,213 | `ede397f11939046a9ee6a3c7452686c01d1aeedc67a7245d76e1e66a5a8240a4` |
| 804 | [n804.cert](source/certificates/best/n804.cert) | 91,219 | `71497e083eddaf22d6a6b777bf8b0a72dc735a8e3d01dfde83ff8b193ab4a3c1` |
| 805 | [n805.cert](source/certificates/best/n805.cert) | 112,968 | `78e1ce70fd5fa85c8500a81753cc3757bbe2e8478e65a9fb691baec96f1a12c0` |
| 806 | [n806.cert](source/certificates/best/n806.cert) | 90,563 | `0e138a758bb536af2106e02ee0329a15aa26e48584aa19164f98fa44e930b965` |
| 808 | [n808.cert](source/certificates/best/n808.cert) | 89,588 | `f03433f694b613a74669adb64eb089c151254c223fc4e25ac29a38714621bb6f` |
| 815 | [n815.cert](source/certificates/best/n815.cert) | 89,613 | `b3ab12313b6319776efd4914c69d2f40ce0a8eda50213c0dd721a4a61d02464c` |
| 863 | [n863.cert](source/certificates/best/n863.cert) | 213,681 | `b4512251fa041fc40a329bcd5176a0883bd96b17fa910caff44ac12e99cf87bb` |
| 865 | [n865.cert](source/certificates/best/n865.cert) | 98,151 | `b8990532742f170ecfd8fbf7148fa07180b2d9fa0261bbd272c2ab028ba02315` |
| 867 | [n867.cert](source/certificates/best/n867.cert) | 98,294 | `c1fa89eada6b28b9217f27a8d13e77e424355170ac8130efac087ed505754344` |
| 868 | [n868.cert](source/certificates/best/n868.cert) | 254,314 | `8b3725caa599d544e96fd65371c625c39317257d502cfb9ca2802892920ad345` |
| 870 | [n870.cert](source/certificates/best/n870.cert) | 97,208 | `396cd265a5e4eef546f89d95136445ab0aa22df410ea81589cd8b75a7e239be7` |
| 872 | [n872.cert](source/certificates/best/n872.cert) | 93,137 | `e4ecc7cd40f3c1e704baccf40f7011fad83b25476dcca9283ad9fc31192441d7` |
| 873 | [n873.cert](source/certificates/best/n873.cert) | 114,451 | `68b8a583694f95a8c830f8fadccf57d64ef3b5b9c85958be5ab388b38a92ad55` |
| 874 | [n874.cert](source/certificates/best/n874.cert) | 114,665 | `b6e888cd952cf16d8a23a15e5c9d7f831f9bac66dd1c62a52fd8e043e6c42599` |
| 919 | [n919.cert](source/certificates/best/n919.cert) | 228,620 | `7ab1c120b7697d7694ca18c91cd6adea395f32e23f6dbebd047ff02c40a17d41` |
| 924 | [n924.cert](source/certificates/best/n924.cert) | 101,681 | `af3f280db6256e74576d0ea6e7f593775f359ace4a630f932d3d94d149fea2dd` |
| 926 | [n926.cert](source/certificates/best/n926.cert) | 224,534 | `caeef6eec71bc3a5c26b4fd716da877b5aff7f7354e2dcec79ff90f7597a5fe4` |
| 927 | [n927.cert](source/certificates/best/n927.cert) | 103,723 | `f9bf81d2850ccd6fe49d3e922f579b51e608ce34d1a9e7899c4e8f3d5251e42e` |
| 928 | [n928.cert](source/certificates/best/n928.cert) | 103,834 | `2bda7b68acbecf1bfba4a773bca41c49f9d673af844cbc6f32c3333e2b916176` |
| 930 | [n930.cert](source/certificates/best/n930.cert) | 104,275 | `931d1e9a8341587dced9bbdeb00bb616373ff3ff9ec71c53ddd6cca390c36283` |
| 933 | [n933.cert](source/certificates/best/n933.cert) | 121,559 | `c0bb8c57011bb755c86b282deb5705eff9934e40c3995b174637241d59e61168` |
| 934 | [n934.cert](source/certificates/best/n934.cert) | 131,918 | `58fb69d4b1ea5c707b862e9bbcc3f089367e374b51b847baf1c9c320d4015502` |
| 984 | [n984.cert](source/certificates/best/n984.cert) | 119,837 | `318fb041acbf84574c53059eba2e7c1c13772aaafb87bc519d15a0a72ec8416c` |
| 987 | [n987.cert](source/certificates/best/n987.cert) | 215,925 | `e7350aecc4267eae0ce4930a51f82a7c5a76b77ecca9398b7f6c1d56c0c74bc1` |
| 989 | [n989.cert](source/certificates/best/n989.cert) | 107,362 | `509453ffd0f345689717110e9c757617779d496cccc1cb6ac6dd5e94971d87cd` |
| 990 | [n990.cert](source/certificates/best/n990.cert) | 110,629 | `57a5dd7be2780cb6fe33c1e5edd6f9667d090e4b781cf3286f53980117bf3cf4` |
| 991 | [n991.cert](source/certificates/best/n991.cert) | 291,869 | `0e88e41ecac198f5d312f4778e078cd367ad39d5d3c842db97ffa8e0a260995b` |
| 992 | [n992.cert](source/certificates/best/n992.cert) | 109,103 | `6c0ca181942c03c521dc62332e512e25178d8b502234fde8044e0b5972b3f3b3` |
| 994 | [n994.cert](source/certificates/best/n994.cert) | 113,501 | `5ee5a4bb9e742789ca82cd3ce837a83fc382f976147be346512287986e1e5a58` |
| 998 | [n998.cert](source/certificates/best/n998.cert) | 113,589 | `a1aec4b31df9f284a624286dd9f2243ad2ed3a0c465751e194a6a9cc9926b339` |
| | **83 certificates** | **8,107,636** | |

## The Claims

Each row claims `s(n) <= P`, with `P` the exact side in the linked certificate’s header
rounded up at 12 places; the issue makes the header authoritative.
A certificate is `n S` and then `n` rows `x y t`: a unit square’s centre and
`t = tan(theta/2)`.
At 545 and 641 the issue links the 546 and 642 certificates, “delete 1”.
The source’s `manifest.json` instead names separate files at those counts,
`n545.cert` (23.889010439313, rounded up) and `n641.cert` (25.881306220599), each above
the side the issue claims; the issue’s rows, not those files, are decided here.
Every other row’s header side equals the bound the manifest states for it, and its
SHA-256 the digest the manifest records.

## Exact Replay

[`devtools.couzo_678_replay`](../../../devtools/couzo_678_replay.py) reads every
certificate from this packet, holds it to the manifest digest, and decides each of the
85 rows over $\mathbb{Q}$:

- **the side.** The header side `S` satisfies `P - 10^-12 < S <= P`: the printed side is
  its upward rounding at 12 places.
- **two exact routes.** Route `sqpack` materializes the certificate through
  `sqpack.witness` and decides with `sqpack.verify`’s exact predicates (unit shape,
  separating axes); route `independent` builds corners by the kernel’s half-angle
  conversion and decides with `devtools.check_rational_witness_independent`’s
  predicates. Both check every corner against every wall, and accept contact: the
  contract is a closed container and disjoint interiors.
- **an exactly justified filter.** A unit square’s interior lies in the open disc of
  radius √2/2 about its centre, so squares whose centres are at least √2 apart cannot
  overlap. Only pairs with `dx^2 + dy^2 < 2`, compared exactly from the certificate’s
  centres, are decided; both routes check that every square is a unit square whose
  corner mean is that centre, which the lemma needs.
  The source’s own checker uses the same lemma after exact cells of side 2.
  `sqpack.verify`’s bucket mode, which buckets float centres, is not used.
- **the deletion rows.** 545 and 641 are the 546 and 642 certificates without their last
  square, at the same side. A subset of a packing is a packing, so the choice of square
  does not matter.
- **five controls per certificate**, each with a known answer and each decided by both
  routes: square 2 replaced by square 1; square 1 moved `S + 2` to the right; the side
  lowered by the least top or right clearance plus `10^-18`; square 1 enlarged by
  `10^-12` about its centre; and, for the candidate pair with the least `|dy|` (at most
  1/2), one square given the other’s `x`, so their inscribed discs of radius 1/2 meet.

### Results

**All 85 rows are verified.** Every printed side is its header side rounded up at 12
places, and both routes accept every packing: 140,866 candidate pairs of 21,393,271, and
every corner against every wall.
The least wall clearance is exactly 0 at 62 rows, where a square touches a wall, and
exactly `10^-15` at the other 23.
The least pair gap is exactly 0 at nine rows (499, 501, 600, 602, 808, 815, 872, 924 and
989), 695 touching pairs in all, and elsewhere between $1.85 \times 10^{-13}$ (at 459)
and $9.16 \times 10^{-11}$ (at 330).
**All 415 controls are refused by both routes**, each on the overlap, wall or shape it
was built to break.
The positive decisions took 90.8 CPU seconds. With the controls, three workers took
1,631.5 seconds of wall from 17:10:17Z on 19 October, on a four-core machine shared with
other lanes at a load average of 15 to 25.
[receipts/filtered-exact-replay.json](receipts/filtered-exact-replay.json) keeps every
row’s side, both routes’ counts, least clearance, least gap and failures, the controls,
and, from the source’s pinned `manifest.json`, each row’s stated bound, digest and credit.

**The source’s checker**, run unchanged from its retained copy (SHA-256
`1c8b89eb0de71bc751db57061a015b8ed8ffb354d38ce13bcf8201ce8c90e98b`, read before it was
run) in a `python -I` child process, accepts all 85 packings under its default contract
and refuses all 332 controls the certificate format states (83 certificates, four each).
Its `--strict` verdict, open container and disjoint closed squares, is false at 62 rows,
the contacts above. Receipt:
[receipts/source-checker-replay.json](receipts/source-checker-replay.json).

**The all-pairs kernel**, `devtools.evand_arrangement_reports`’s two routes with no
filter, decided every pair at 204, 260 and 343 and at the two deletion rows, 545 and 641:
466,389 pairs. Both routes accept all five, and their least pair gaps and wall
clearances equal the filtered decision’s exactly, so the filter skipped nothing that
decides a margin there. It took 267.6 CPU seconds, 0.57 milliseconds a pair for both
routes on the loaded machine. At that rate the all-pairs positives of the 83 certificates,
21,039,911 pairs, are 3.35 CPU-hours; `upper_bound_reports certify`’s three jobs a count
are 10.06, and 20.12 with `check --replay`. That is under the owner’s 40 CPU-hour cap,
but past this session’s wall bound, and the 641 job alone took 587 seconds of wall,
against the kernel’s 600-second job ceiling. It did not run here; the import bead
prices it. Receipt: [receipts/exhaustive-sample.json](receipts/exhaustive-sample.json).

**Göbel’s classical constructions.** Every claimed side is below Göbel’s side at its
count (Göbel squares, Göbel strips and corner-touching strips, with deletion), by
$4.31 \times 10^{-3}$ at 919 or more, decided exactly by the 15 October packet’s
[goebel_beyond_horizon.py](../couzo-verified-bounds-2026-10-14/review/goebel_beyond_horizon.py),
read from its retained path. Friedman’s off-centre constructions, square tilings and
repeated L borders, which the issue also compares against, are not checked here.
Receipt: [receipts/goebel-comparison.json](receipts/goebel-comparison.json).

## Against the Record, in Report Order

The [19 October ledger](../../../campaign/issue-intake/upper-bounds-20261019/README.md)
walks every report at the 85 counts in report order, from the record on `main` at
`d588ad987bd8de53361d087b8961a7f2bf157c41`, frozen again on 20 October; the first reading,
at `f3d5da7bd77d931c915db7e9393f9ebff75a85ac` on 19 October, decided every claim the
same way. It walks de Winter’s #666, Couzo’s #670, #672 and #675, then #678, each #678
claim at its exact header side.

**Every #678 claim is recorded**: each is below every number the standing side and
every earlier report at its count may be.
At the 55 counts #675 also claims, #678 is below #675’s print by at least
$6.56 \times 10^{-10}$ (at 652) and up to $3.86 \times 10^{-2}$ (at 458); #675’s claims
are recorded before it, and #678 changes none of them.
At the other 30 counts it is decided against #670 at nine, #672 at seven, #666 at one,
the record’s beyond-horizon rows at twelve (eleven from
[couzo-verified-bounds-2026-10-14](../couzo-verified-bounds-2026-10-14/README.md), one from
[evand-record-hunt3-2026-10-10](../evand-record-hunt3-2026-10-10/README.md)), and at 260
against T-196, de Winter’s #668 certificate registered through PR #676 and pending
adoption.
**At 260** the claim, `146417594016514621500994169/8796093022208000000000000`, is below
T-196’s exact side by $2.56 \times 10^{-5}$. It reached this repository after T-196, so it
is recorded after it and does not rewrite it.
The issue’s own prior column at 260, 16.645778786062, is the intermediate evand seed
recorded on #678’s custody thread, 1.8e-08 below T-196; this record does not use that
column.
The ledger orders reports and verifies no certificate; registration is Stage 3’s.
Stage 3 registered 204 and 260 as T-223 and took the 83 beyond the corpus as rows of
the `couzo-issue678-2026-10-18` source, each superseding the row that stood at its count
where one did: 57 of `couzo-verified-bounds-2026-10-14`’s, two of
`couzo-certificates-2026-10-14`’s and `evand-record-hunt3-2026-10-10`’s at 343.

### Per Row

Each row’s print, its exact side rounded up at 16 places, what the ledger decided it
against and by how much, #675’s print where #675 claims the count, the least pair gap the
filtered decision found, and its pairs.

| n | Printed, up | Exact side, up at 16 | Standing before #678 | Below it by | #675 printed | Least pair gap | Pairs decided / all |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 204 | 14.808642841982 | 14.8086428419812473 | #675 | at least 1.53e-06 | 14.808644367227 | 5.56e-11 | 486 / 20,706 |
| 260 | 16.645753250545 | 16.6457532505449560 | T-196 (#668), pending adoption | 2.56e-05 | - | 1.24e-12 | 561 / 33,670 |
| 330 | 18.692697855726 | 18.6926978557252946 | #672 | at least 9.39e-07 | - | 9.16e-11 | 782 / 54,285 |
| 343 | 18.978232204823 | 18.9782322048224772 | row evand-record-hunt3-2026-10-10 | at least 3.19e-07 | - | 1.60e-12 | 763 / 58,653 |
| 418 | 20.942828529884 | 20.9428285298837412 | #670 | at least 2.41e-03 | - | 7.91e-12 | 920 / 87,153 |
| 420 | 20.974164562587 | 20.9741645625865331 | row couzo-verified-bounds-2026-10-14 | at least 3.09e-04 | - | 1.11e-12 | 962 / 87,990 |
| 421 | 20.981525640927 | 20.9815256409269584 | #675 | at least 1.29e-03 | 20.982817268367 | 1.22e-12 | 1,019 / 88,410 |
| 422 | 20.983607201006 | 20.9836072010059935 | #675 | at least 1.09e-07 | 20.983607310148 | 8.05e-11 | 960 / 88,831 |
| 455 | 21.882183551471 | 21.8821835514705696 | row couzo-verified-bounds-2026-10-14 | at least 2.67e-04 | - | 1.01e-12 | 1,194 / 103,285 |
| 456 | 21.882183551471 | 21.8821835514705696 | row couzo-verified-bounds-2026-10-14 | at least 1.73e-02 | - | 1.01e-12 | 1,197 / 103,740 |
| 458 | 21.903778442820 | 21.9037784428199681 | #675 | at least 3.86e-02 | 21.942423483273 | 1.20e-12 | 1,021 / 104,653 |
| 459 | 21.942365250364 | 21.9423652503631486 | #675 | at least 5.82e-05 | 21.942423483273 | 1.85e-13 | 1,085 / 105,111 |
| 461 | 21.971318847922 | 21.9713188479212424 | #675 | at least 2.97e-04 | 21.971616092121 | 1.20e-12 | 1,115 / 106,030 |
| 462 | 21.974888792980 | 21.9748887929798488 | #675 | at least 5.60e-03 | 21.980489088007 | 1.12e-12 | 1,070 / 106,491 |
| 463 | 21.983603993953 | 21.9836039939523906 | #675 | at least 1.91e-06 | 21.983605908182 | 1.26e-12 | 1,125 / 106,953 |
| 464 | 21.987753655547 | 21.9877536555467385 | #675 | at least 2.82e-04 | 21.988035588879 | 1.20e-12 | 1,149 / 107,416 |
| 497 | 22.823104027272 | 22.8231040272712966 | row couzo-verified-bounds-2026-10-14 | at least 5.32e-03 | - | 1.12e-12 | 1,103 / 123,256 |
| 499 | 22.882183551471 | 22.8821835514705696 | row couzo-verified-bounds-2026-10-14 | at least 1.73e-02 | - | 0 | 1,316 / 124,251 |
| 501 | 22.903778442820 | 22.9037784428199681 | #670 | at least 3.00e-02 | - | 0 | 1,145 / 125,250 |
| 502 | 22.942219237446 | 22.9422192374459178 | #675 | at least 1.83e-04 | 22.942402035201 | 1.17e-12 | 1,124 / 125,751 |
| 505 | 22.971592368271 | 22.9715923682703486 | #670 | at least 7.25e-04 | - | 1.52e-12 | 1,167 / 127,260 |
| 507 | 22.973697163680 | 22.9736971636792371 | #672 | at least 6.45e-06 | - | 1.20e-12 | 1,226 / 128,271 |
| 545 | 23.889010439304 | 23.8890104393033385 | #675 | at least 7.12e-04 | 23.889722420681 | 1.18e-12 | 1,303 / 148,240 |
| 546 | 23.889010439304 | 23.8890104393033385 | #675 | at least 7.12e-04 | 23.889722420681 | 1.18e-12 | 1,306 / 148,785 |
| 548 | 23.956345132949 | 23.9563451329487750 | #675 | at least 1.11e-03 | 23.957455469976 | 1.23e-12 | 1,353 / 149,878 |
| 549 | 23.956345132949 | 23.9563451329487750 | #675 | at least 1.11e-03 | 23.957455469976 | 1.23e-12 | 1,357 / 150,426 |
| 553 | 23.980727660940 | 23.9807276609393850 | #670 | at least 8.60e-04 | - | 1.08e-12 | 1,241 / 152,628 |
| 554 | 23.993524047733 | 23.9935240477329903 | #675 | at least 5.67e-05 | 23.993580713561 | 1.21e-12 | 1,311 / 153,181 |
| 555 | 23.993580713561 | 23.9935807135603365 | #666 | at least 7.31e-05 | - | 1.12e-12 | 1,272 / 153,735 |
| 592 | 24.888988759404 | 24.8889887594033189 | #675 | at least 7.34e-04 | 24.889722420681 | 9.25e-13 | 1,355 / 174,936 |
| 593 | 24.888988761769 | 24.8889887617682897 | #675 | at least 7.34e-04 | 24.889722420681 | 8.96e-11 | 1,391 / 175,528 |
| 597 | 24.961502766154 | 24.9615027661533137 | row couzo-verified-bounds-2026-10-14 | at least 5.14e-05 | - | 1.01e-12 | 1,596 / 177,906 |
| 598 | 24.961502766154 | 24.9615027661533137 | #675 | at least 1.41e-03 | 24.962908839930 | 1.01e-12 | 1,600 / 178,503 |
| 600 | 24.980727660940 | 24.9807276609393850 | #670 | at least 8.58e-04 | - | 0 | 1,373 / 179,700 |
| 601 | 24.987983019378 | 24.9879830193779427 | row couzo-verified-bounds-2026-10-14 | at least 1.50e-03 | - | 1.34e-12 | 1,389 / 180,300 |
| 602 | 24.993580713561 | 24.9935807135603365 | #675 | at least 2.42e-09 | 24.993580715986 | 0 | 1,401 / 180,901 |
| 641 | 25.881306220594 | 25.8813062205932259 | #675 | at least 8.26e-03 | 25.889564291814 | 8.49e-11 | 1,484 / 205,120 |
| 642 | 25.881306220594 | 25.8813062205932259 | #675 | at least 8.42e-03 | 25.889722420681 | 8.49e-11 | 1,486 / 205,761 |
| 650 | 25.982275449119 | 25.9822754491182190 | #675 | at least 1.53e-04 | 25.982428402604 | 9.79e-12 | 1,549 / 210,925 |
| 652 | 25.994256214773 | 25.9942562147726842 | #675 | at least 6.56e-10 | 25.994256215430 | 1.26e-12 | 1,622 / 212,226 |
| 653 | 25.994414202392 | 25.9944142023919690 | #672 | at least 5.53e-05 | - | 7.83e-12 | 1,567 / 212,878 |
| 654 | 25.995888235804 | 25.9958882358035543 | #675 | at least 1.76e-05 | 25.995905846673 | 1.20e-12 | 1,599 / 213,531 |
| 693 | 26.881306218365 | 26.8813062183644839 | #675 | at least 8.42e-03 | 26.889722420681 | 7.46e-12 | 1,602 / 239,778 |
| 700 | 26.972679052192 | 26.9726790521910391 | #675 | at least 2.75e-04 | 26.972954520906 | 1.27e-12 | 1,785 / 244,650 |
| 701 | 26.975549413717 | 26.9755494137163356 | #675 | at least 1.06e-05 | 26.975560060840 | 3.39e-11 | 1,919 / 245,350 |
| 703 | 26.987459573204 | 26.9874595732034160 | #670 | at least 3.38e-05 | - | 1.37e-12 | 1,726 / 246,753 |
| 704 | 26.994256369878 | 26.9942563698777493 | #672 | at least 2.13e-04 | - | 2.95e-12 | 1,783 / 247,456 |
| 705 | 26.994256369878 | 26.9942563698777493 | #675 | at least 1.65e-03 | 26.995905846673 | 2.95e-12 | 1,786 / 248,160 |
| 706 | 26.998542133963 | 26.9985421339622461 | #675 | at least 9.74e-05 | 26.998639495676 | 1.38e-12 | 1,676 / 248,865 |
| 749 | 27.911194713730 | 27.9111947137295638 | #672 | at least 1.28e-02 | - | 1.20e-12 | 1,711 / 280,126 |
| 751 | 27.932448900769 | 27.9324489007686474 | row couzo-verified-bounds-2026-10-14 | at least 1.73e-02 | - | 1.20e-12 | 1,840 / 281,625 |
| 752 | 27.932449886404 | 27.9324498864032791 | row couzo-verified-bounds-2026-10-14 | at least 1.73e-02 | - | 1.59e-12 | 1,799 / 282,376 |
| 753 | 27.932449886404 | 27.9324498864032791 | #675 | at least 3.09e-03 | 27.935538484638 | 1.59e-12 | 1,802 / 283,128 |
| 754 | 27.937423317053 | 27.9374233170529219 | #670 | at least 2.01e-07 | - | 8.92e-11 | 1,844 / 283,881 |
| 755 | 27.951504031492 | 27.9515040314915140 | #675 | at least 8.94e-05 | 27.951593396552 | 1.60e-12 | 1,703 / 284,635 |
| 760 | 27.995022162160 | 27.9950221621593884 | #675 | at least 9.25e-04 | 27.995946706541 | 1.20e-12 | 1,806 / 288,420 |
| 804 | 28.909246527138 | 28.9092465271370989 | #675 | at least 2.07e-03 | 28.911312576594 | 1.20e-12 | 2,137 / 322,806 |
| 805 | 28.909665866810 | 28.9096658668092057 | #675 | at least 1.65e-03 | 28.911312576594 | 1.20e-12 | 2,121 / 323,610 |
| 806 | 28.919759255285 | 28.9197592552841084 | #675 | at least 1.70e-03 | 28.921462680479 | 1.38e-12 | 2,085 / 324,415 |
| 808 | 28.932449886404 | 28.9324498864032791 | row couzo-verified-bounds-2026-10-14 | at least 1.43e-03 | - | 0 | 1,959 / 326,028 |
| 815 | 28.995022162160 | 28.9950221621593884 | #672 | at least 9.24e-04 | - | 0 | 1,961 / 331,705 |
| 863 | 29.916419307447 | 29.9164193074468816 | #675 | at least 5.04e-03 | 29.921462677966 | 6.83e-12 | 2,319 / 371,953 |
| 865 | 29.932449886402 | 29.9324498864014173 | #675 | at least 1.74e-04 | 29.932623425046 | 1.20e-12 | 2,073 / 373,680 |
| 867 | 29.949688481977 | 29.9496884819769584 | #675 | at least 4.17e-04 | 29.950105216770 | 1.53e-12 | 1,955 / 375,411 |
| 868 | 29.977390686090 | 29.9773906860898733 | #675 | at least 3.97e-03 | 29.981359990606 | 1.01e-12 | 2,289 / 376,278 |
| 870 | 29.985424855417 | 29.9854248554168545 | #675 | at least 9.94e-05 | 29.985524292952 | 1.23e-12 | 2,218 / 378,015 |
| 872 | 29.995022162160 | 29.9950221621593884 | #675 | at least 9.24e-04 | 29.995946381399 | 0 | 2,071 / 379,756 |
| 873 | 29.996375057644 | 29.9963750576433815 | #675 | at least 1.80e-03 | 29.998171180951 | 1.11e-12 | 2,151 / 380,628 |
| 874 | 29.996375057644 | 29.9963750576433815 | #675 | at least 1.80e-03 | 29.998171180951 | 1.11e-12 | 2,154 / 381,501 |
| 919 | 30.844931419278 | 30.8449314192776452 | #675 | at least 4.30e-03 | 30.849232404954 | 1.20e-12 | 1,936 / 421,821 |
| 924 | 30.932449886402 | 30.9324498864014173 | #675 | at least 1.28e-04 | 30.932577553094 | 0 | 2,240 / 426,426 |
| 926 | 30.945612117331 | 30.9456121173306243 | #670 | at least 4.02e-03 | - | 1.01e-12 | 2,525 / 428,275 |
| 927 | 30.975475685281 | 30.9754756852801427 | #675 | at least 1.47e-03 | 30.976949083864 | 1.20e-12 | 2,279 / 429,201 |
| 928 | 30.975475685281 | 30.9754756852801427 | #675 | at least 1.47e-03 | 30.976949083864 | 1.20e-12 | 2,283 / 430,128 |
| 930 | 30.981535303483 | 30.9815353034825086 | #675 | at least 7.89e-06 | 30.981543197185 | 1.20e-12 | 2,161 / 431,985 |
| 933 | 30.994238714880 | 30.9942387148793669 | #675 | at least 1.05e-03 | 30.995293256848 | 1.11e-12 | 2,220 / 434,778 |
| 934 | 30.995302140806 | 30.9953021408052538 | #672 | at least 3.48e-05 | - | 1.20e-12 | 2,196 / 435,711 |
| 984 | 31.914115712696 | 31.9141157126954608 | row couzo-verified-bounds-2026-10-14 | at least 6.19e-03 | - | 1.13e-12 | 2,177 / 483,636 |
| 987 | 31.944662519483 | 31.9446625194825725 | #670 | at least 4.97e-03 | - | 1.01e-12 | 2,714 / 486,591 |
| 989 | 31.975475685281 | 31.9754756852801427 | #675 | at least 6.50e-04 | 31.976125363479 | 0 | 2,454 / 488,566 |
| 990 | 31.977918827720 | 31.9779188277198206 | #675 | at least 1.26e-04 | 31.978044872634 | 1.20e-12 | 2,514 / 489,555 |
| 991 | 31.981485095638 | 31.9814850956377101 | #675 | at least 5.05e-05 | 31.981535631408 | 1.01e-12 | 2,566 / 490,545 |
| 992 | 31.984796372085 | 31.9847963720847924 | #675 | at least 4.47e-05 | 31.984841090107 | 1.20e-12 | 2,409 / 491,536 |
| 994 | 31.993645614627 | 31.9936456146265014 | #675 | at least 2.20e-04 | 31.993865896560 | 1.20e-12 | 2,435 / 493,521 |
| 998 | 31.998301106112 | 31.9983011061119749 | #675 | at least 8.06e-07 | 31.998301912120 | 1.34e-12 | 2,437 / 497,503 |

## What Is Not Established

The certificates establish finite upper bounds at their exact sides, nothing more.
Novelty, local or global optimality and rigidity are not decided, and neither are the
source’s credit and lineage statements: the manifest’s seed, construction and parent
records are the author’s.
The issue says every new or changed witness passed the jlevy/squares corner verifier and
the source’s checker; those runs are the author’s.
The filtered route is a first-party program written for this replay. Its two routes
share the certificate parser, the half-angle conversion, the pair filter and Python’s
rational arithmetic, so it is two implementations of the unit-shape, pair and wall
predicates, not two independent replays.
Its one adversarial review to date is the 19 October mathematical review on the import
bead: independent all-pairs checks at 204, 260, 330, 545, 641 and 998 and an independent
separating-axis test on all 140,866 candidate pairs agreed with the receipts.
The maintained all-pairs kernel has run only on the sample above.

## Credit and Licence

Francisco Couzo wrote the source, which states no licence for its data; the certificates
are kept as factual data and nothing of the source is relicensed.
The manifest credits Couzo at every row and keeps seed and construction credits beside
it: Joost de Winter’s constructions at 16 rows (260, 464, 555, 602, 652 to 654, 705,
706, 760, 815, 872, 874, 933, 934 and 998), Mykhailo Polkovskyi’s at 204, Evan Daniel’s
(after Kevin Fang) at 343, Kevin Fang’s rectangle and gluing with PingYou Ltd’s square
input at 703, and Couzo’s own earlier packings elsewhere.
The issue names de Winter’s Young-corner, slipped-ribbon and four-block families and
Fang’s rectangle and gluing constructions.
The checker is Evan Daniel’s, modified by Couzo with Codex. The issue states nothing
about AI assistance; the checker’s header names Codex, and the author’s issues of 13 and
14 October disclose OpenAI Codex and Claude Code assistance.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source couzo-issue678-2026-10-18 --check
uv run --frozen --all-extras --group dev python -m devtools.couzo_678_replay check
uv run --frozen --all-extras --group dev python -m devtools.couzo_678_replay check --replay
uv run --frozen --all-extras --group dev python -m devtools.couzo_678_replay filtered --pinned CHECKOUT --workers 3
uv run --frozen --all-extras --group dev python -m devtools.couzo_678_replay source-checker --scratch SCRATCH
uv run --frozen --all-extras --group dev python -m devtools.couzo_678_replay exhaustive --n 204 260 343 545 641
uv run --frozen --all-extras --group dev python -m devtools.couzo_678_replay goebel
uv run --frozen --all-extras --group dev python -m devtools.couzo_678_replay claims-record
```

`check` reads the four receipts and the beyond-horizon claims record against the issue
and the packet; `check --replay` decides every row and control again. `filtered`,
`source-checker`, `exhaustive` and `goebel` rewrite their receipts, and `claims-record`
rewrites `acquisition/beyond-horizon-claims.json`; `--pinned` names a checkout at the
pin, from which the source’s `manifest.json` is read and held to its digest.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
