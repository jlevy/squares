# Third-party sources

Every file under `third_party/` and `tools/verify_cert_daniel.py` was fetched with curl from the pinned
raw.githubusercontent.com URL below on 2026-10-12 and is unchanged. Check with
`shasum -a 256` against this table (or against MANIFEST.sha256 at the repository root).

## Evan Daniel, https://github.com/evand/square-packing (MIT)

Commit `29d0cee87c1d717f7b4497b8fb0ee17ac9d0087d`, path `search/exact/batch/certs/`:

| file | n | SHA-256 |
|---|---|---|
| daniel/n-5.cert | 5 | `cf43eb4d940915e3ab11ef43d470678dfed3388f377103e038426deb2b60d52b` |
| daniel/n-11.cert | 11 | `9cc1b667f9ca4e99a0bf8a30912a3b46299411b2a65489a37cc3937691ea32f5` |
| daniel/n-19.cert | 19 | `73758d0fa95137f29d0ba4cbf25955872b9bf8e8e62e599316239108354ba78d` |
| daniel/n-29.cert | 29 | `81fb164fdc5cfe75ebde9bf0842b8856b21aebc48eb446c4be19d86f6e4ea783` |
| daniel/n-41.cert | 41 | `c9c8350a4857f9e5d0b4f5bc33a54ae037f9db95b6f4e73dbbaa69c7c580b697` |
| daniel/n-55.cert | 55 | `36d91d3d7a3f4f5e51983681ac2f230d68786038bb9aacc614edf294f400fa35` |
| daniel/n-71.cert | 71 | `acbe9dac9468e5fb03d27c32a7cf46de6503e6c91614d9235cf203062221d4d1` |
| daniel/n-89.cert | 89 | `b3769230512bac3c630215cae66188c3b12dc64e52e94493f521326516b9c4c4` |
| daniel/n-109.cert | 109 | `1ed2bb61e3e9f911997fa70178e92c2d140a8732e137cb48f41cb69732734070` |
| daniel/n-110.cert | 110 | `fc6c309bd060e629a9d38287dc27b82a7a197ed84463879540df39986e4a5b8d` |
| daniel/n-132.cert | 132 | `c08e34825e7112dfab3d8af87f473219bdb417ff9d8bc2b172cb272013d91fdb` |
| daniel/n-156.cert | 156 | `f35bc8982fa5a96f4ffbb6d4d9170c6d21b2a9b0177bac1acc10cf887398e1ae` |
| daniel/n-182.cert | 182 | `ad5c8eeac0c358fce1b9c4a65c6b4c9fc5767f44bf64be81bb4fee719580bd17` |
| daniel/n-210.cert | 210 | `8d3555a54ac461177fe02a625ebe3a80137ecd8bebcfb3742e3b41e2e47dc4cf` |
| daniel/n-241.cert | 241 | `9fe9370c0cd7a93096aa6c41877eb1675b46de432f8ab31381e724ef44de584e` |
| daniel/n-273.cert | 273 | `4555cd31a62f243ecf74105ea370f62fff622d12a7b33a32ef29d95980b7c025` |

Commit `c013f43cefd006f007a6f37bc3a56aadead815d6`, path `search/packer/candidates/`:

| file | n | SHA-256 |
|---|---|---|
| daniel/hunt3_n308.cert | 308 | `41961a5e096afa5f7763419d81b2958c54f37aae5e54e51a0c54ca23946da734` |
| daniel/hunt3_n343.cert | 343 | `bf05962c580d46bbeef5ad66fee5d3ca45dab7002d726c424126d9b9259f4332` |
| daniel/hunt3_n344.cert | 344 | `54bb6b6696b96ccf6a30db313ee4e62240fe17c070624fd916b59b483f7b20cc` |

Other files from commit `29d0cee87c1d717f7b4497b8fb0ee17ac9d0087d`:

| file | upstream path | SHA-256 |
|---|---|---|
| daniel/LICENSE | LICENSE | `c51886c0f7e6724a7d89fc22cb237a1688ba1bbff04cb21a13b8e1a01fb15578` |
| ../tools/verify_cert_daniel.py | search/exact/verify_cert.py | `3299ca0c0f02f7c221deeea69a9a85b5a90db6bc410b20727fdff211c92bed52` |

## Fetched, not copied

Joost de Winter's packing of 211 unit squares (https://github.com/JoostdeWinter/square-packing-211) is the
base case n = 15 of the note. That repository has no licence, so neither it nor Daniel's exact certificate
of the same packing is redistributed here. `fetch_unlicensed.sh` downloads both from pinned commits into
`third_party/unlicensed/` (ignored by git) and checks these hashes:

| file | source | SHA-256 |
|---|---|---|
| n211__record.json | JoostdeWinter/square-packing-211 at `702df9bb3b1e7fe13279a61a1fa89722aa2d496a` | `94b206475442caade4892a393251c9d464341b3327e58c6ef21076fea3dad372` |
| n-211.cert | evand/square-packing at `29d0cee87c1d717f7b4497b8fb0ee17ac9d0087d`, search/exact/batch/certs/ | `ca491d50bb17c976f82edc0ef0accf1316aeac692c9e26bba49921f46ad942ef` |
