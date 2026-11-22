# Source evidence for issues 1060 through 1063

[The acquisition record](acquisition.json) binds the retained original numerical files
to seven GitHub attachments supplied by Joost de Winter on 21 November 2026. Only the
listed mathematical data are retained. Programs and prose in the submissions stay in
their original archives. The receipts used the repository’s readers and exact
arithmetic, with one worker per guarded run.

## Lower-bound claims in #1060

Attachment D’s final table has 166 distinct counts. It states 40 strict and 126 weak
inequalities. The previous endpoints match the C table. D raises 22 of those endpoints
and leaves 144 as filed. Sixty rows name Hosono’s T-180 for the unchanged region. See
[the table inventory](receipts/1060-final-table-inventory.json) and
[exact comparison](receipts/1060-final-baseline-comparison.json). The claims await
per-family proof review and replay.

## Algebraic claims in #1061

[The root comparison](receipts/1061-exact-sides-and-relations.json) verifies three
identities between isolated roots by shifting the exact polynomials and comparing
their rational isolating intervals. The identities are L199 = L172 + 1,
L268 = L129 + 5, and L292 = L259 + 1. Each is a relation between filed construction
sides. The maintained number-field route accepted 11 constructions and both controls
on two-square slices for each. The three identities have exact side and full
construction receipts for both members. The source includes 259 as a dependency for the
last identity and asks for review of the other eleven counts.

At 109, the [independent exact side check](receipts/1061-n109-independent-side.json)
proved that the submitted side lies between 10.94928958094335364162 and
10.94928958094335364268, roughly 2.025696e-12 below T-335. The
[frozen checker](receipts/1061_n109_side_probe.py.txt) isolated the field root, evaluated
the original side polynomial in that field and proved that the advertised degree-44
polynomial vanishes there. Its six controls passed. The full 109-square geometry exceeds
the maintained reader’s input ceiling and remains undecided. A separate check against
the advertised side interval stopped at host memory pressure 2.

To replay the side check, use the official archive in the acquisition record, the T-335
witness pinned by digest in the receipt, a fresh external output directory and the
project interpreter. Pass the checker `--archive`, `--witness`, `--output`, `--gate`
and `--guard-log`. Start an observe-only memory guard on the checker before releasing
its gate. The checker stops at 180 seconds, pressure 2 or a measured footprint above
0.30 GiB.

## Rational claims in #1062 and #1063

The 232-square source gives an exact candidate below the T-307 first-contact side by
about 4.00173e-9 and below JoeGun’s earlier rational certificate at its own first
contact by about 2.00880e-34. The [independent review](n232/review/README.md) accepted every pair. [The comparison](receipts/1062-comparison-to-prior-first-contact.json)
uses the earlier concrete certificates. It does not compare against the local solver’s
unrounded limiting point.

Both maintained routes replayed the 232-square witness and the duplicate-square and
outside-container controls with [exact GMP rationals](n232/receipts/native-exact-gmp.json.xz).
Each route checked all 26,796 pairs in each job. The three jobs took 35.19, 40.01 and
37.72 seconds under [memory supervision](n232/receipts/native-exact-gmp-supervision.json).
The package retains the original rational certificate and both routes’ complete
input and output records.

For all 13 supplements, the stated center scaling and a common translation reproduce
every exact center and preserve the exact angles and the 12-place upward print of the
enclosed input. All thirteen ends are strictly below the corresponding registered
witnesses contracted to first contact. The
[initial source checks](receipts/1063-exact-source-reading.json) and
[registered-house comparisons](receipts/1063-first-contact-comparison.json) separate
those two tests. [Full exact replay](receipts/1063-finite-rational-replay.json)
accepts all 13 submitted witnesses and all 52 controls. The
[pose comparison](receipts/1063-prior-house-pose-identity.json.gz) checks their
geometry against the older houses. The nearest-center correspondence is bijective
for all 13 layouts. The largest measured move is 0.04834, at 130. No square
turns by more than one degree. The standing construction credits follow those
measured matches. Independent review and adoption stay open.

## Replaying the rational supplements

Copy the retained 232-square checker to an external scratch file with a `.py`
extension before importing its exact predicates. The archived replay takes the
upstream `rational-enclosures.zip`, that scratch checker and a fresh receipt path.

## Compressed Files

| Stored file | Origin | Git blob of uncompressed bytes | Decompressed SHA-256 |
| --- | --- | --- | --- |
| `lower/A/claims-166.csv.gz` | upstream | `4d923694ac3d0fca88f48057bd3a277c1e56eecb` | `b4b809ce60de7af41c9648822fa2a7fe2da1c87409578d49b1ea76443a72028d` |
| `lower/C/claims-166-updated.csv.gz` | upstream | `4d923694ac3d0fca88f48057bd3a277c1e56eecb` | `b4b809ce60de7af41c9648822fa2a7fe2da1c87409578d49b1ea76443a72028d` |
| `lower/D/claims-final.csv.gz` | upstream | `3110257ab9aa6eaa70fcedf6bff84bb6e1a05f86` | `81e11c944fd64f80fb59314f75c2969a5bf4cba433e74fc94995dc8b7bc3ca42` |
| `receipts/1063-prior-house-pose-identity.json.gz` | receipt | `dea4f8559005dfdd0c8d490dedd62221032572a8` | `42f6b70144521cf7d50774c72d67731bcc5c21fa7e10b62c0d58acb9a3b62fb2` |
| `lower/review-dependencies/scalar-audit.json.gz` | receipt | `3974676e451376551edc5bfc13b1a833f56b4ed8` | `b09af7dd29b258798842deeca1e1e367520539d38d970561af8a92d07247636b` |

## Original Gzip Files

| Stored file | Origin | Git blob of stored bytes | SHA-256 of stored bytes |
| --- | --- | --- | --- |
| `algebraic/n109/n109.minpoly.json.gz` | upstream | `7911331bb2ddd18cbc417a8de109a5b0da83c1fb` | `fd89b48c5d1f34a5a795262c1b03d3dd4d2893d21ef6bd56edb132aef6835434` |
| `algebraic/n129/n129.minpoly.json.gz` | upstream | `d32bf195ac58257af5125f28d54653fe60bf10cf` | `0fc41cc2193245aa7be8fb1c2e05babcfc3bb1036448f19de63d43f018dc2513` |
| `algebraic/n172/n172.minpoly.json.gz` | upstream | `7473f38970307e8d5c70e9c8680445a8a61fc71a` | `a2482b4955b364382867903ed04f7a4ccd6aaea4af076459676bf18a8fbde651` |
| `algebraic/n175/n175.minpoly.json.gz` | upstream | `94d49c047d225625766f359c50dcbd6867d1cc11` | `6ace303ff57e0b413b96199c148b05e312b516eaa4b17bac5b547314bbe34759` |
| `algebraic/n199/n199.minpoly.json.gz` | upstream | `3dc796e7c4b57e6410b3ce27b358be0f09cf4301` | `feacc43ff836df92c80ea488f1fc992502c232efeb62db0246f261b00e0a0248` |
| `algebraic/n237/n237.minpoly.json.gz` | upstream | `c23e67eb3652fd11abcd3ef5fb5e7f407fc30f66` | `e7516a74ebc4851e66780bf02a168dc554222c37f5afc863dd21027afecf1e1c` |
| `algebraic/n259/n259.minpoly.json.gz` | upstream | `168db9f09a921b4d44e393fa98023f6c1495a450` | `6508a2980bde297d992b298b547e418d881e3b0ec9c6e1cbd65948c12b0f2bf4` |
| `algebraic/n262/n262.minpoly.json.gz` | upstream | `a2e266ab01a8458a1c8faf5d54a95701e8a77cfb` | `cb62178e58ea3361cc85f6b67b2a5f7cbe2f8ce8f2dfd74e811701e186d1583e` |
| `algebraic/n268/n268.minpoly.json.gz` | upstream | `e2dba5d0ce76953957102414b1c5784a890195f2` | `19c8481e05ccf09bb93af0feebf9c4a1ddb16ebfd2e4f9ae0358da6fb95a8bf1` |
| `algebraic/n269/n269.minpoly.json.gz` | upstream | `992bc8653dcf26a00f07f70cf072b1464bacb39d` | `e511cc0c60f999c425b7e878dafa3b4feac34d809af48aef5beec85ff7c864b5` |
| `algebraic/n292/n292.minpoly.json.gz` | upstream | `0e2ff1760b69b886a94763b8199a1d7b5fd67546` | `3402d50a061b634b6cd77ad9754788cde0502a68c931c869fc2e80266ecc743e` |
| `algebraic/n295/n295.minpoly.json.gz` | upstream | `fa421a0023b12289ccedba89c2b4deada272f2ea` | `b54f2414743b4ca2a856d253c478ac09bce94913002cef06f74b1054b1910008` |
| `n232/candidate.json.gz` | upstream | `921583586617e7cc412dadbf53217a589997bc66` | `b72b04c8c3f6b57c4372fd2db17b1666832dd22ad1d734094ed070aacddcf4fe` |
| `n232/input.json.gz` | upstream | `c6a9fc9735db99988540ff1a31fc375a3d657195` | `9ae760cfbd190378872418cc93751846649658a40cd9d37130ca0ace9872ab7a` |
| `supplements/105/candidate.json.gz` | upstream | `12a7d53746baa7fc1f6f6fd96964f9267992a804` | `4151af49b3c6e6900f196912e38ff6f941b3c2e908fee8bc64bafd394e48964f` |
| `supplements/105/input.json.gz` | upstream | `b5b6e926367c33d6c224fc3d4d6dee579aab3856` | `6ebc0100117d0eb09a2568e7a6a948282999b05e840d994373880d1b4ef6bb8d` |
| `supplements/127/candidate.json.gz` | upstream | `3e236b3707416389f08fc33aaca5ee833fc805d2` | `3fc067333f8732f8db7f2a0865345cce877a37bad94d2d8b385b4ea5c5f8d115` |
| `supplements/127/input.json.gz` | upstream | `dd1c7476b5d26710f7d3aa4c465d13415fe16e43` | `c594c948d8b2f0a1b260e249ab31ab6acc0c3477b895c0d4aa196709db2a816f` |
| `supplements/130/candidate.json.gz` | upstream | `e4bba2b155a557ad20d8b097f22d5af58dd36ee8` | `da00d5fef69ef24a3f012bbd74d8ff7ad5945f63dfedd7ae47fae79b7bdf58d0` |
| `supplements/130/input.json.gz` | upstream | `ab363960c5f2b79237ce255db7a4fe91e5c6e9d3` | `1848213c8c15749f86f28bf339654b6135382c1a1f768aea2681501ece5ab02e` |
| `supplements/156/candidate.json.gz` | upstream | `322f213fe44e858b4b9b79b8dff4a2acbf6836a3` | `ba2ce3d6c17db7ae14a73d69243cd416053c038d795c23e872cd411d876f43bc` |
| `supplements/156/input.json.gz` | upstream | `8e1aff8448b07d6c0cb4c8e0531e732b2ffa5721` | `c689d70d445526d9394ece1fcab8e2c44e9844648159a51ea5570308a69abe20` |
| `supplements/180/candidate.json.gz` | upstream | `892963034bd359cf0452b537d049af4f03a30093` | `83e94ebd41b5aea2881c77d03b6e13a39a8969e2a3edefe7b55fdf9c074c9095` |
| `supplements/180/input.json.gz` | upstream | `45ac2e1ced825fd0d8b972d8afd9000798a6ebc3` | `a9f3189a6fa6e62f98b75aab99481e6a7ef27038fdc3ecd75b62b31071ade049` |
| `supplements/182/candidate.json.gz` | upstream | `e1ea1e5f6572e7020ee9a7bd4e6dc134021bbf9a` | `fdde2c3a9cdfd1d2a8b437857fee0e6d14d0d57ef5f231ea6239c0123f23bacd` |
| `supplements/182/input.json.gz` | upstream | `7d9afb3df72e7a78e9e2071bc51c12bb6d8618fc` | `f845f5c45e18ce3ece06278ea8cbea63d5195affd3f65d483ce2832723d4ef91` |
| `supplements/260/candidate.json.gz` | upstream | `d8d40452fb4328cc10a68b77740cb5d7cf653bb2` | `f9a255cc0dcd2e66a783f70a2c4f613595e2f4c348dbe68bb8dd9bfbd5cc744e` |
| `supplements/260/input.json.gz` | upstream | `876f5e67abb2d6c4e3228487724d93efbca14e97` | `a2a05f0514ca40b8c7f555acbd4e4b2b900b36a368dc679a5400b94ad82c6b0a` |
| `supplements/270/candidate.json.gz` | upstream | `207aa35c92b7d0616baaafddb74eba67e806e066` | `f76f733a28984c4413319ff5fec3280899421c6f9a058943a14315c5262f99a4` |
| `supplements/270/input.json.gz` | upstream | `73ff0c2006f814b9d3310731e77abab51a7cf927` | `bf6019f3b4caf789cc4bab9613e346b283fadc686192560c3886554a44d7a95b` |
| `supplements/272/candidate.json.gz` | upstream | `bc290da58448b9237417de854d78975e15540074` | `5d6d210b10e0a960ae7e0b0888fd4da86069d62df0d60336ef51c457f0faa6a6` |
| `supplements/272/input.json.gz` | upstream | `fb3a67c37af417b55d55715a4b68311c51c85aa4` | `4cf4a5114e4632b362f4d96682c351e9c3057a6aa8d9fb08033d5b6701e80e8f` |
| `supplements/299/candidate.json.gz` | upstream | `79d051673f2a026d86f52e99cd0bd2212a259cf7` | `5dcd55a4f0baeac30a8df94bbada6596ecd5b270c78650877d8bf0d110910a35` |
| `supplements/299/input.json.gz` | upstream | `6c64f9dd496afbca3fbf49b9e346700fbd016d8a` | `1da33424f9737ae06aaa69d440491a117fbdf689f7be0d4f803d94b621658e73` |
| `supplements/304/candidate.json.gz` | upstream | `f26a98c218d1f7032007749f98381dd1905b6ebb` | `6a540f98a852b342f9fc243022d299a4bee35786fe18605d43728e1d222e7d1c` |
| `supplements/304/input.json.gz` | upstream | `9d9163134385e42c5ca4227a1c63668766ca5def` | `8b580344539480c49cfc39a6d4c516f7b163204bc03d0b51647dd0713ea70825` |
| `supplements/307/candidate.json.gz` | upstream | `185b01b57e0a3056ffa7f66c2aa4388bd252f3f0` | `fd3038546959c7a14feed85b35053ea3be03f00a6f4f63eb6405903993a07428` |
| `supplements/307/input.json.gz` | upstream | `f15c995b09b97d388c6c7f96c218e5bf0c11fb98` | `cfe68d5d3018d0cf18f32c229d1969d1ebc9129fc1abf5b4301e74da6e74d449` |
| `supplements/308/candidate.json.gz` | upstream | `25f645599f0a295fa4bb90cc8d66dc3ee48e2dee` | `0038e14ebf39d983e2e6be6119b3464d52ba34de5206ec3a6f491705103e79d5` |
| `supplements/308/input.json.gz` | upstream | `d4216e491b6e1dc74f0dbe6b3881312a4e38261b` | `a25bb0aecc025c0054c28e63d724c7c649f2f2ff487cbf64ee0ee70f30c6d391` |
| `n232/review/source/232/candidate.json.gz` | upstream | `921583586617e7cc412dadbf53217a589997bc66` | `b72b04c8c3f6b57c4372fd2db17b1666832dd22ad1d734094ed070aacddcf4fe` |
| `n232/review/source/232/input.json.gz` | upstream | `c6a9fc9735db99988540ff1a31fc375a3d657195` | `9ae760cfbd190378872418cc93751846649658a40cd9d37130ca0ace9872ab7a` |

The [independent dependency review](lower/review-dependencies/README.md) proves the
coarse parallel-chord lemma and checks Attachment D’s final arithmetic. The
sixty T-180-dependent rows retain their existing replay dependency.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
