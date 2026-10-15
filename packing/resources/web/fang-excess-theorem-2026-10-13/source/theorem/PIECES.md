# Pieces of the theorem inventory

Every input certificate used by `tools/instantiate_theorem.py`. Squeeze: square of side S, m = ceil S: m - S; rectangle W x H in the box a x b = ceil W x ceil H: min(a - W, b - H); rounded down (truncated to 9 decimal places). Excess of a square piece: count - (m^2 - m). Gain of a rectangle: b - waste, the excess one Lemma 3 step adds. Role `theorem`: used by the theorem chain; `extra`: only by --best.

| piece | path | count | box | waste | excess / gain | squeeze (rounded down) | role | provenance | sha256 |
|---|---|---:|---|---:|---:|---|---|---|---|
| R | `r17x16_n0257.cert` | 257 | 17 × 16 | 15 | gain 1 | 0.000743691 | theorem | ours | `6921624a762d234bf4486555f5ad590226962adf0d309883efd0a8bb5e46fd15` |
| R' | `r22x21_n0443.cert` | 443 | 22 × 21 | 19 | gain 2 | 0.009439615 | theorem | ours | `7219a6169875f9b925503210a26c220429fcb4362bde73404732b9c338ce0c00` |
| n-211 | (fetched, see third_party/fetch_unlicensed.sh) | 211 | 15 × 15 | 14 | excess 1 | 0.002039295 | theorem | de Winter, unlicensed, fetched (Daniel's exact certificate of de Winter's packing; not redistributed) | `ca491d50bb17c976f82edc0ef0accf1316aeac692c9e26bba49921f46ad942ef` |
| n-241 | `third_party/daniel/n-241.cert` | 241 | 16 × 16 | 15 | excess 1 | 0.011867560 | theorem | Evan Daniel, MIT (exact certificate of Ellsworth/Stead's 241, Kingbird) | `9fe9370c0cd7a93096aa6c41877eb1675b46de432f8ab31381e724ef44de584e` |
| n-273 | `third_party/daniel/n-273.cert` | 273 | 17 × 17 | 16 | excess 1 | 0.016074037 | theorem | Evan Daniel, MIT (exact certificate of Ellsworth/Stead's 273, Kingbird) | `4555cd31a62f243ecf74105ea370f62fff622d12a7b33a32ef29d95980b7c025` |
| n0308 | `n0308.cert` | 308 | 18 × 18 | 16 | excess 2 | 0.000690144 | theorem | ours | `0d563d8c1197da49ca7c1a1a64531953b4c4314ad7daafaa19281569db2eccd3` |
| n0343 | `n0343.cert` | 343 | 19 × 19 | 18 | excess 1 | 0.005096470 | theorem | ours | `34f680f8f0d2db8335d8d7db76fa1ca3fd9d0215cde2ef225deba1d22d45ee5f` |
| n0381 | `n0381.cert` | 381 | 20 × 20 | 19 | excess 1 | 0.023030259 | theorem | ours | `5b9410ecac453e466deb16cf095623a6965a8a0f6e30b592d9212e54cc40b42e` |
| n0421 | `n0421.cert` | 421 | 21 × 21 | 20 | excess 1 | 0.013849683 | theorem | ours | `e68d4d8c8a3b3132f9d06600881f59cfa7f1d3fb5086b65b8377b4f3d3f473cb` |
| n0463 | `n0463.cert` | 463 | 22 × 22 | 21 | excess 1 | 0.013119593 | theorem | ours | `13681395624bc699e9cc038b3c6ea2d36d7d41dd7759a21afd8af5d3d4946838` |
| n0507 | `n0507.cert` | 507 | 23 × 23 | 22 | excess 1 | 0.002192816 | theorem | ours | `8bac8b61dff0e19b778a935af9179a60933ad7597a8d6adfffc9624a6dcfb63b` |
| n0553 | `n0553.cert` | 553 | 24 × 24 | 23 | excess 1 | 0.001188979 | theorem | ours | `12095f68fc60d2549457aef0d12b68c65588f3c6bd1f2b8eeb8684394ffb9122` |
| n0601 | `n0601.cert` | 601 | 25 × 25 | 24 | excess 1 | 0.001085427 | theorem | ours | `f8e3a97ed2756965e92be64ab6485bf0e12ddd55763f6a604133f28c3d3b645c` |
| n0651 | `n0651.cert` | 651 | 26 × 26 | 25 | excess 1 | 0.008452184 | theorem | ours | `6c013ff77bdacba64cfc14dd84427e6bcee7b7facf9146bceb8c1b2ea3390d2b` |
| n-110 | `third_party/daniel/n-110.cert` | 110 | 11 × 11 | 11 | excess 0 | 0.003216603 | theorem | Evan Daniel, MIT (exact certificate of Ellsworth's 110) | `fc6c309bd060e629a9d38287dc27b82a7a197ed84463879540df39986e4a5b8d` |
| n-132 | `third_party/daniel/n-132.cert` | 132 | 12 × 12 | 12 | excess 0 | 0.008672112 | theorem | Evan Daniel, MIT (exact certificate of the AMS21 packing of 132) | `c08e34825e7112dfab3d8af87f473219bdb417ff9d8bc2b172cb272013d91fdb` |
| n-156 | `third_party/daniel/n-156.cert` | 156 | 13 × 13 | 13 | excess 0 | 0.017917301 | theorem | Evan Daniel, MIT (exact certificate of the AMS21 packing of 156) | `f35bc8982fa5a96f4ffbb6d4d9170c6d21b2a9b0177bac1acc10cf887398e1ae` |
| n-182 | `third_party/daniel/n-182.cert` | 182 | 14 × 14 | 14 | excess 0 | 0.025909286 | theorem | Evan Daniel, MIT (exact certificate of the AMS21 packing of 182) | `ad5c8eeac0c358fce1b9c4a65c6b4c9fc5767f44bf64be81bb4fee719580bd17` |
| n-210 | `third_party/daniel/n-210.cert` | 210 | 15 × 15 | 15 | excess 0 | 0.026998883 | extra | Evan Daniel, MIT (exact certificate of the AMS21 packing of 210) | `8d3555a54ac461177fe02a625ebe3a80137ecd8bebcfb3742e3b41e2e47dc4cf` |
| n0380 | `n0380.cert` | 380 | 20 × 20 | 20 | excess 0 | 0.023224566 | extra | ours | `aa4b6577cc4a6c427bc618631c45b52e84b2db1defa854ddf4f97082f088660d` |
| n0344 | `n0344.cert` | 344 | 19 × 19 | 17 | excess 2 | 0.004510724 | extra | ours | `1a9019bb26be7223d1768672894b55e77963db90dcdcdaa0a5984ad0be4dda91` |
| n0382 | `n0382.cert` | 382 | 20 × 20 | 18 | excess 2 | 0.010520270 | extra | ours | `cb200c0fce9cc1ce7bacc5e9ecb2848853ef2c342b055e21f2790dfcd8db448c` |
| n0422 | `n0422.cert` | 422 | 21 × 21 | 19 | excess 2 | 0.011563475 | extra | ours | `c4be8e28a056acdfdb62c32ce56b1facc87d1ee4c4587f843e70221b7dd3a7d4` |
| n0464 | `n0464.cert` | 464 | 22 × 22 | 20 | excess 2 | 0.008290463 | extra | ours | `38b26a58f25cca740f0faa6516e41e220314aeff93cda9b5302376370bf13d3e` |
| n0508 | `n0508.cert` | 508 | 23 × 23 | 21 | excess 2 | 0.005266150 | extra | ours | `58431ee9f25901e734645b5c9d7d45681ba87a3939766eda5d8f906ab6c33fe7` |
| n0758 | `n0758.cert` | 758 | 28 × 28 | 26 | excess 2 | 0.003653757 | extra | ours | `372b48290b957e131b82b73587d6cb2743a844aafb8b6aa965e9a7fe67d84a3e` |
| n0814 | `n0814.cert` | 814 | 29 × 29 | 27 | excess 2 | 0.000126396 | extra | ours | `4dace4d0edf719d426362989c6f9808da6f249283c9aa5102c2596295706c599` |
| r18x17 | `r18x17_n0290.cert` | 290 | 18 × 17 | 16 | gain 1 | 0.002449182 | extra | ours | `a0a5cbc007f02acbd03986c4532a719ecfc1ce48589a0ff81ef717ce1ee6bd87` |
| r19x18 | `r19x18_n0325.cert` | 325 | 19 × 18 | 17 | gain 1 | 0.005951344 | extra | ours | `b46bee39f17554265e5e209da30ca929150b772c0ff115fdfa84a6a1e3bf48ee` |
| r21x20 | `r21x20_n0401.cert` | 401 | 21 × 20 | 19 | gain 1 | 0.011712763 | extra | ours | `a6a5a023e053d615420ccbeb0704e8ebd27facc3532da331569cb142f6b30efe` |
| r22x21w20 | `r22x21_n0442.cert` | 442 | 22 × 21 | 20 | gain 1 | 0.002779638 | extra | ours | `4f0860acf3b05c61ceaa57d1b6ce2d0ba8e83e891f9d1b5d95ccf640f674b7f0` |

Uniform squeeze: d0 = 1/10000 = 0.0001. Minimum piece squeeze: n0814 (0.000126396017...), so d0 < every squeeze (checked exactly).

## Definitions

Theorem (note v0.6): for every n >= 15 and integers p, q >= 0 with 16p + 21q <= n - 15, n^2 - n + 1 + p + 2q unit squares pack in a square of side < n. F(n) = 1 + max{p + 2q : 16p + 21q <= n - 15}.

`inventory.tsv`, one row per n: (p, q) maximise p + 2q, tie-break larger q; the remainder r = n - 16p - 21q is in 15..30. Base at r: the square piece listed for r (15: n-211, 16: n-241, 17: n-273, 18..26: n0308, n0343, n0381, n0421, n0463, n0507, n0553, n0601, n0651; `[k]` = only the first k squares kept, so the base has excess exactly 1), or for r = 27..30 R glued to n-110, n-132, n-156, n-182. Then q steps with R' and p with R. Every step is Lemma 3 at squeeze d0 (`squarepack.glue.glue(..., d=d0, strict=False)`), closed side exactly n - d0; the final certificate is strictified once (centres and side times 1 + d0/(2(n - d0)), side n - d0/2). Count n^2 - n + F(n). Columns: side = exact strict side, side_up15 = rounded up to 15 places, strict_ok = squarepack.verify --strict, rectcheck_ok = tools/rectcheck.py, closed_ok = squarepack.verify on the closed certificate, sha256 = strict file, chain = pieces in gluing order.

`best.tsv` ranges over exactly this inventory: every square packing obtained from one base (a square piece above, or the Lemma 3 composite of an ordered pair of rectangle pieces) by a finite sequence of Lemma 3 steps, each gluing one rectangle piece (as A) onto the current square (as B), all at squeeze d0. A step with rectangle a × b of waste w takes (n, excess j) to (n + b, j + b - w), so the maximum excess at each n is a DP; the row gives the maximiser with the fewest gluing steps (then theorem pieces only). Where it equals F(n) the theorem certificate is that maximiser and is not duplicated. This is a lower-bound inventory of these pieces, not a claim that no other packing does better.
