# Evan Daniel’s Exact-Data Release: s(29) and Grade C

Evan Daniel published the data behind two exact reports of
[evand/square-packing](https://github.com/evand/square-packing) as the release
[`exact-data-2026-10-12`](https://github.com/evand/square-packing/releases/tag/exact-data-2026-10-12),
in answer to the request of
[issue #545](https://github.com/jlevy/squares/issues/545#issuecomment-6126076974).
Neither report is a bound.
The release is tagged at `31523f87316bdfda00f5459dd9077928e264f133` (committed
2026-10-12T13:59:32Z) and was published at 2026-10-12T14:14:15Z. It is not marked
immutable, so its assets are pinned here by digest. The assets were downloaded at
2026-10-12T14:41Z.
The reports themselves, and the scripts that produced them, are retained at `ad86d42` by
the [evand-exact-and-local-reports-2026-10-12](../evand-exact-and-local-reports-2026-10-12/README.md)
packet; nothing under `search/exact/` or `tasks/` changed between that pin and the tag.

| Asset | Bytes | SHA-256 | Here |
| --- | --- | --- | --- |
| `s29-minpoly.tar.zst` | 87,237,962 | `708e1b8b45894667f90a0d18b55bb35ed6079b84d33f9656976fd5cfa6f3729c` | pinned by digest; three small files retained |
| `gradec-233.tar.zst` | 238,231 | `c71633f3850eb8b06c40ba04f824e9b6262b27b7996f62f69c6ad014a4ea9fa3` | retained as published |
| `SHA256SUMS` | 171 | `cd98b11150843e1a38b1f1afb943b17c2464c9df0d4088bfcb9dd96dab860e03` | retained |

Both archive digests match the release’s `SHA256SUMS`, the digests GitHub reports, and
the digests the issue comment prints.
[acquisition/release.json](acquisition/release.json) records the release, each asset,
and every member of the s(29) archive with its size and digest.

## The s(29) Archive

The archive holds 21 files, 201,735,244 bytes unpacked: the polynomial $p$
(`n29_poly_q4.json`), the shape-lemma parametrization of the five class angles
(`n29_param_t1.json` to `n29_param_t5.json`), the exported system (`n29_system.jl`), the
Krawczyk box (`n29_krawczyk.json`), the side to about 40,000 digits (`n29_S0.txt`), the
four roots the homotopy missed (`n29_q4_ref133k.txt`), and the original logs.
Every member was read here as a stream and matches the archive’s own `SHA256SUMS`; none
was unpacked to disk but the three retained.
Retained under [acquisition/release/s29/](acquisition/release/s29/): the archive’s
README, with the five replay commands, its `SHA256SUMS`, and `n29_krawczyk.json`.

Read from `n29_poly_q4.json` here: 7,214 integer coefficients, so degree 7,213; a
positive leading coefficient of 325 digits; a height of 5,074 digits; a constant term of
4,566 digits. The file’s own metadata reports 165 real roots and irreducibility by degree
patterns, with no possible factor degree.
The Krawczyk box gives the zero $t^\ast$ to radius $10^{-50}$ and the side
$S = 5.933833462676929189689460616352019138433834181077886974638\ldots$ with radius
$1.07 \times 10^{-48}$, the value the case record compares with its verified rational
ceiling.

**Not run.** The replay costs about 2.5 CPU-hours by the author’s measure, almost all in
`verify_mod.py`, and needs `PREC=220000` for `link.py`; its two identity steps are Monte
Carlo, and the packing’s non-overlap at the exact point is checked by none of it.
Irreducibility, the enclosure, the link and the identities were not checked here.

## The Grade-C Archive

The archive holds 723 files, 15,787,809 bytes unpacked: `n-N.contacts.json` and
`n-N.gradec.json` for the 233 configurations `gradec.py` reports VALID, the run logs of
all 250, three `GRADEC_DROPZERO=1` logs (10, 230 and 261) and the two status files.
Each file is a single-line JSON or a short log, so the packet keeps the archive itself,
[acquisition/release/gradec-233.tar.zst](acquisition/release/gradec-233.tar.zst), bound to
the digest the release states, and not its 15.8 MB of contents.
Python 3.14’s standard library reads it (`tarfile`, mode `r:zst`).
Unpacked in scratch space, all 722 files its `SHA256SUMS` lists match.
Its README and the two status files are also kept unpacked, under
[acquisition/release/gradec/](acquisition/release/gradec/).

**Recomputed at n = 10.** The source’s `gradec.py`, read first and run from a copy
outside the repository under the package versions `env.sh` pins, rebuilt the n = 10
certificate from the committed exact form, `search/exact/minpoly/data/n-10.minpoly.json.gz`
(retained here as its upstream gzip), and the archive’s `n-10.contacts.json`.
The output is byte-identical to the archive’s `n-10.gradec.json`, SHA-256
`ffc0c1ee41b0c2037ab241806215b0df9d2a0111893256fa2a2116e3df02208f`: VALID, 36 rows, a
2-dimensional flat family, least multiplier 1/16.
It took 9.2 seconds of wall time and 2.5 CPU seconds.
[receipts/gradec-n10-recompute.json](receipts/gradec-n10-recompute.json) records the
program, the inputs, the environment and the output.
This is the author’s own checker on the author’s data: it shows the published certificate
is what `gradec.py` computes from the published inputs, not that Theorem C or
`gradec.py` is sound.

**The price of the rest.** The logs print each VALID run’s build time. They sum to
38,026 seconds, about 10.6 CPU-hours: 154 runs took under a minute (1,249 seconds in
all), 212 under ten minutes (3.9 hours), and the longest, 313, took 1,741 seconds.
Those are the author’s times with eight jobs in parallel, so a re-run here may be slower.
The 17 timeouts would not finish under `gradec.py` as written.
Ten stop after the multipliers, in the reduced-Hessian step, with $\dim W$ from 12 to
16, while every run that finished has $\dim W \le 11$; `gradec.py` sums each leading
minor over all $k!$ permutations.
The other seven, 274, 275 and 308 to 312, stop before the null vectors, with flat
families of dimension 210 to 274.

## The Review of 23 October 2026

The stage 4 mathematical review of Theorem C,
[review-2026-10-23-evand-grade-c-theorem-c.md](../../../../docs/project/reviews/review-2026-10-23-evand-grade-c-theorem-c.md),
found the theorem true under its hypotheses and repaired a gap in its proof at side-end
rows. Its own checker, which shares no code with the source, decided all 233
configurations again from the exact forms retained here and the archive’s contacts files:
every one valid, in 1,463 CPU-seconds, agreeing with every published certificate on rows,
ranks, flat families and $\dim W$.
The programs and how to run them are in [review/](review/README.md), and their receipts
in `receipts/review-*`.

## Original Gzip Files

| Stored path | Origin | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `source/search/exact/minpoly/data/n-1.minpoly.json.gz` | upstream | `4ea18a515b517a986ce1a7b98065902b0aa0c90f` | `0265b03e45df1a1ba3d63e1d4530b8b1df888064ad3a1182852e8cb890db17ef` |
| `source/search/exact/minpoly/data/n-2.minpoly.json.gz` | upstream | `928b29cac9cce0b271ecd28a398b58dad362b96b` | `f6ec03fa385a2660d4dfe64b5ecfc7bc4f8d455d417d5ba71e7656abcfe960c9` |
| `source/search/exact/minpoly/data/n-3.minpoly.json.gz` | upstream | `366da0a5ef3582dae7de2b40c2c14ad29857c9da` | `eb3a6f2a2e5d298ab4e0104be978edf86dffd00a79b20a8f9532c8d357d3aa0b` |
| `source/search/exact/minpoly/data/n-4.minpoly.json.gz` | upstream | `cd31b10a5ee3d5bdd87d0a674097bb0e8b623919` | `c39e247290ce855fa1456efa3aed47bc062cf45722f8bc5d19ca2e748c503f37` |
| `source/search/exact/minpoly/data/n-5.minpoly.json.gz` | upstream | `44a468aa6889f15f4e63e9f96bb3e4fefceb56c6` | `b3d764c98305bf5553f05479769a97fcdd5e509f6812bdbb98ab7978e2ae515a` |
| `source/search/exact/minpoly/data/n-6.minpoly.json.gz` | upstream | `e1002aeec53bbebb469919ba3a051c5a868e3025` | `637fd09c60403857dc745fb508d394b4e77c8dc3612f05efed5a80b136d941e0` |
| `source/search/exact/minpoly/data/n-7.minpoly.json.gz` | upstream | `b78d08f9ecee1990ddbd1ebde741c476d99409ff` | `3597a5a607d2e6d6f0d7357a96576d8952f3c0fe467ba69be76ce971b31758fa` |
| `source/search/exact/minpoly/data/n-8.minpoly.json.gz` | upstream | `13e994f32b53372596e85a2c7cd128fc6fd37f26` | `2d94a8319a64ecd8d66dbfbd92d034e956cb7741c744b24234ba5e8adea2f796` |
| `source/search/exact/minpoly/data/n-9.minpoly.json.gz` | upstream | `25cb0432125aae9b767e67e2eb57a38f8371eca3` | `248a0780ba6055b8662b347494c386ffcdd8c5aa271f0a0cf2ed3fa2a748e3fd` |
| `source/search/exact/minpoly/data/n-10.minpoly.json.gz` | upstream | `1b8b87ba186f28adf4e8a1a0e335bd527ca64c43` | `efe6d26daf56f866a3d8b7bfc245a94074e4786b8c3e5150b18738ca349be438` |
| `source/search/exact/minpoly/data/n-12.minpoly.json.gz` | upstream | `cdaa2908412ab1910c26310ed04d19ac0e8f524c` | `88ddcd391dc4c62b6b837bcdc43f90aa86fb4ccdeb49c66aada8e7926d8cefb8` |
| `source/search/exact/minpoly/data/n-13.minpoly.json.gz` | upstream | `818b1df9d3c1e5bbcbab139b9e354724aa780a71` | `9d62482b40d37a78ee549b57d25836a4c491ef9fa65208da4c8d7d179094ce36` |
| `source/search/exact/minpoly/data/n-14.minpoly.json.gz` | upstream | `a7e07f428bb71716abf81592edbb9e9e94104665` | `a5f36d18f3a8ee726c53f32e93eff55af343177a968d120853db62de580b1919` |
| `source/search/exact/minpoly/data/n-15.minpoly.json.gz` | upstream | `bfa6c764bcdd0fa4b65f4ac371d11c61a1e80b27` | `df4adcc97989d0e75e1069d495147e8ee3f9d212d6b422f6f121ed0b55f85c1b` |
| `source/search/exact/minpoly/data/n-16.minpoly.json.gz` | upstream | `4023f1b5fd26d37fb16d43134e80b8a3ed8ed904` | `9004f51ef34055dcde190337fd67796cc11574c0bdd67d9e948aed663ef20e17` |
| `source/search/exact/minpoly/data/n-18.minpoly.json.gz` | upstream | `93f910ab3f02cc611c6f3c4b2d461e39170dcd63` | `42cd4c2f2331b60a2da4f4168c440100b1b668e446955091ea289dccdf816ab2` |
| `source/search/exact/minpoly/data/n-19.minpoly.json.gz` | upstream | `4a75c05d28ca26ff6bd0039b2ddf75bf558b1d8d` | `2f465a9aa36c821151c1998110024deac8f5fe6d3891b1fc8511e4d55bbdb029` |
| `source/search/exact/minpoly/data/n-20.minpoly.json.gz` | upstream | `96c024254e13561fa4a0bbbe4bcf407433e2b365` | `e526d998e22f7c013b7827e58fcc0227d1400983f076ec809607bfcdd7354198` |
| `source/search/exact/minpoly/data/n-21.minpoly.json.gz` | upstream | `5b43edbf4304ace9f6d5d90aa88f531b18c935f2` | `f9cac836347275178c0466475f879cce354bcb339d970254d36d58b459043885` |
| `source/search/exact/minpoly/data/n-22.minpoly.json.gz` | upstream | `21d2e69caa5d59a0ff17b19c206d50fea85e015d` | `ca7e8dc0ae5532e47e67cfe919b63c3b65c788a4a3490ba8968de3de4b315e55` |
| `source/search/exact/minpoly/data/n-23.minpoly.json.gz` | upstream | `aab21edfd720a918c6efa3c2f92ac87f89dd4ccb` | `55e1f2cc5e9be03d07a27840823a2a07ecb5957f17e1a5d3a3c919b64ba8b001` |
| `source/search/exact/minpoly/data/n-24.minpoly.json.gz` | upstream | `d7d4db7fad5b34bad2c3b27ad3fe854c8d07ef3c` | `b0fb1bfe6cea3e1a3324d7ad416122607a36d9b83185820971bdf5554cac7422` |
| `source/search/exact/minpoly/data/n-25.minpoly.json.gz` | upstream | `4768c2af7d76bb04ec8c562de5104d9206da3640` | `f3d14a41891f6a434563fee31420ac8650483eb47e23d3a5b1c16c0e058374ae` |
| `source/search/exact/minpoly/data/n-26.minpoly.json.gz` | upstream | `b6260ccf0cd9a7b1137b527a047d7d99bf827be9` | `9b754b0ffdc15ce37125678ec7dce110f3297ff38e729d54cd863c141d7e4fff` |
| `source/search/exact/minpoly/data/n-27.minpoly.json.gz` | upstream | `50008db46ede02bb1a8a8f0ec3f73e9fcc2e2bcb` | `48b5e58913574a1223b8a29265134032ae977015e995b5a2dd32da599604818f` |
| `source/search/exact/minpoly/data/n-30.minpoly.json.gz` | upstream | `41a0e83ca001850f15b299012059b96835b3c9d0` | `1c70ba1c425107a74c7fada399bcdb9d37e37baee4d7b3a40409b4dda2887402` |
| `source/search/exact/minpoly/data/n-31.minpoly.json.gz` | upstream | `1f80e6aa06de5e609e56fdbcd05b2fbbf9197ab4` | `f62aa2c1d86a050dac68a1872328dd3522a801a96123614b2fddb2ef080f9a7c` |
| `source/search/exact/minpoly/data/n-32.minpoly.json.gz` | upstream | `658dfe6b7508b086913893d73e54281c5f9aed04` | `7d89355a1b8cd4ea0d94601971cd540f805c4f03ec910f9ff1ead3a4dd461f95` |
| `source/search/exact/minpoly/data/n-33.minpoly.json.gz` | upstream | `6cbf9d96daca9a89eea028d44991afcd0af8024d` | `872458538b051f7457d0f9fb148032b93c572561e14e881341be7d8e484fd75c` |
| `source/search/exact/minpoly/data/n-34.minpoly.json.gz` | upstream | `4bf10abc9ee4b3b753cd72396ea54619838ea836` | `6f90d62e2e58e43b236aed1efa765ec87d3c769f7bcb49d5cca3894b4a373e4e` |
| `source/search/exact/minpoly/data/n-35.minpoly.json.gz` | upstream | `fbdf3080d686f56e7f3b97fa95942610dcaa4235` | `d1ca6b7795dfff32ebef662d0c1ddb22c8c143539019067da5b6e32d3af96d9f` |
| `source/search/exact/minpoly/data/n-36.minpoly.json.gz` | upstream | `5a7a44b105e1f7a8ea2208066dbbdd6facd64e50` | `d7a3834e14d819068bc709dd5f0be9baf5e24a5fb017188f1454f6f4eb2cd319` |
| `source/search/exact/minpoly/data/n-38.minpoly.json.gz` | upstream | `98a24a060b7b94f3111cb712954fbcbdeeda4077` | `a34f019dd4a19c8ce4078c3f912fec0556d21b912fa1c866dd20d0a07de2e041` |
| `source/search/exact/minpoly/data/n-40.minpoly.json.gz` | upstream | `dbcae2019f3901c2a29f125920a0a562d2e83137` | `07ce02bee64376c904df5448cee98ade1505c996dc289275ea64269175d30212` |
| `source/search/exact/minpoly/data/n-42.minpoly.json.gz` | upstream | `4f7395a8768b6b9c2c3ef096ebeb99fc608a7e36` | `d027a872e15460d89a200f96d74b4d8f29b726a8ab7eecf78ada166c8631721c` |
| `source/search/exact/minpoly/data/n-43.minpoly.json.gz` | upstream | `5739da9b0624cbf043fc46f59df14881ef270a19` | `6ea93ea70789b7465ab67794e77f4cc057e0e3b9db8459d2cdff2aefd7e8da9d` |
| `source/search/exact/minpoly/data/n-44.minpoly.json.gz` | upstream | `abdee850b0944b838e878f3b21334d30744d4ad9` | `a20c75b417081d292155658135d8720018fd390c44a4b3eba7fdab450672bb3e` |
| `source/search/exact/minpoly/data/n-45.minpoly.json.gz` | upstream | `240ee23f26736cfec3083ac907597d64587293ca` | `55cfb7a368be456fe0d7be29aba8776e6035b686c53fcfdd06fcef4c6e18d6d7` |
| `source/search/exact/minpoly/data/n-46.minpoly.json.gz` | upstream | `422cda6cbe2730b883bc5140ad40a6e79bae48e0` | `8be7bc1734b2f080154dc0d3f3f6bc962eed2d399a3aa84b0c8a3b5a52ee8de9` |
| `source/search/exact/minpoly/data/n-47.minpoly.json.gz` | upstream | `eaec3b3d4c084b5c0acc2bd959899afb83b201e2` | `6ff807959ea40fbc2a218bd2213d2f8e34ab4663747847fc5b87df58269be865` |
| `source/search/exact/minpoly/data/n-48.minpoly.json.gz` | upstream | `280ded2e5db74ade9df83d18eaa905ec1495496c` | `af82914af3111299330db2152358c1ab9b0b1debf976f9628a43cf033205abf5` |
| `source/search/exact/minpoly/data/n-49.minpoly.json.gz` | upstream | `4266dbb097420adf1afa377f91aedcb2af283055` | `7939a55618fdf6bfb3c93ea8997c49f0736cddac9b4c2dd7f30dde5696fde8e5` |
| `source/search/exact/minpoly/data/n-50.minpoly.json.gz` | upstream | `64f2ed97c207afc33ec377f5b981249e87909d00` | `33b0fba6ce85a7fe3050598b5a2d7900a5e6de2c70a6f0826b91b78685a8680e` |
| `source/search/exact/minpoly/data/n-52.minpoly.json.gz` | upstream | `2dc27028400467591a330e92d0003f384fd61e14` | `65be68df579a5cc06bf534636205242871bfa31a492812c736e07a3856f596b1` |
| `source/search/exact/minpoly/data/n-53.minpoly.json.gz` | upstream | `1d4f27bae060d1b75ba6c68f40971dd8d18ee451` | `3ebd5b7a1145851f345cbb70f3f44d042e6be1ace8231f2e7345b01d63711767` |
| `source/search/exact/minpoly/data/n-54.minpoly.json.gz` | upstream | `646a67f899c69ee6492a0dd4e38dc7eae093f8e9` | `497e105a31b50dd022c6a544299859bceddfdd7f1414ed14e00d5767a203cbc7` |
| `source/search/exact/minpoly/data/n-56.minpoly.json.gz` | upstream | `7a5edc684476a3e7b786bd1c2283d22d76ac6e79` | `2e51a5a181c1ed8aa023031944b2a3243cfbc74337639afc514cc2b5137cdfad` |
| `source/search/exact/minpoly/data/n-57.minpoly.json.gz` | upstream | `03766941f67a0bdc9f1a13c2c3d121d1ead47222` | `78345fc8f57f89c73a19db2181258ff95ce648fe273a8f7f12efb9a390ec20d7` |
| `source/search/exact/minpoly/data/n-58.minpoly.json.gz` | upstream | `45fadd24c89e91ab341c0109fbd5279a75669b9c` | `b4044838d4de03269075fd20cbf5240b7e84263c3684418d99dafc71c8e2615c` |
| `source/search/exact/minpoly/data/n-59.minpoly.json.gz` | upstream | `91f147b57ff3955fb773e96d4614ba6c378bfe41` | `02f3a8556b99ae2f49c0a7c54b2b77b6cfc450b9bdcfc54477f156150336a156` |
| `source/search/exact/minpoly/data/n-60.minpoly.json.gz` | upstream | `75af21c28e546ab9bf718bb5e8d6912f4ab53119` | `97c9a5e9c5784443e88a4ca0ddb01e3a492f31c7503b1edc8a85f722cbe57669` |
| `source/search/exact/minpoly/data/n-61.minpoly.json.gz` | upstream | `f6cc7c1ea0b1cd1245e1d35eab54a0d662552bbb` | `390c3c40b37aba9b626b3801c93db9aac8b28da41507475c83076ff429d84eb0` |
| `source/search/exact/minpoly/data/n-62.minpoly.json.gz` | upstream | `6ef20935df48a07dd7eee6e7110569db0be2f02e` | `332d9ce66d5f1d38ce272347c65a8714192310750916412902d2b7f3efab2795` |
| `source/search/exact/minpoly/data/n-63.minpoly.json.gz` | upstream | `c06bc71796e46972dcce93f3a440efccf1bdb921` | `bdcadfb2a543c089632153722121b071f5f0c538dafb75d08c0c0316b4e2be38` |
| `source/search/exact/minpoly/data/n-64.minpoly.json.gz` | upstream | `2859a85b8fe2ff05ad03d86b01726bf1d3f9cd74` | `c27bd8a09b95934f3fc4e3276287ffd70b7450ef0ecc8c70754e736af8f1aade` |
| `source/search/exact/minpoly/data/n-65.minpoly.json.gz` | upstream | `84e7fc9d06aef7fd9743522c11442d8bebd14b95` | `59b4f4872bb421949286ba2ad66f203c05af6a72a6918c6106e608cf81eaca0e` |
| `source/search/exact/minpoly/data/n-66.minpoly.json.gz` | upstream | `26c74ac3296035007a13452d060d8a0efaf0aca7` | `f1e7b70b6d997fc442951997cb1e4d9a550596b3ddf8fdcace19afcb45101f29` |
| `source/search/exact/minpoly/data/n-67.minpoly.json.gz` | upstream | `791cf77d0a8b86c2faf0fdf70b8d7d82ff01dcfc` | `5a612d27032f1be62131da85a1a364287431eb45355a451f73888ef5e88982cd` |
| `source/search/exact/minpoly/data/n-70.minpoly.json.gz` | upstream | `f59fe59c79468391bf6a1d93ebf8f67177bcd776` | `82cd8c44dae3151588f33300828112e1252cd18dd825d5ad57d25299b07ecad6` |
| `source/search/exact/minpoly/data/n-72.minpoly.json.gz` | upstream | `9f279d1beb22eb28e4e24c743cdc538ed7b22fbf` | `dd9e509ac51c896bd72b6a35ab7ee07ffe91efbcc5c5892027b27189d320a7cf` |
| `source/search/exact/minpoly/data/n-73.minpoly.json.gz` | upstream | `2ad8cebdcf93902aefc3673938d2b32a8b769384` | `cd2e15944659099b575d4502197f4bee9057d3cc766aa4540e8b7d7c3ae87ed3` |
| `source/search/exact/minpoly/data/n-74.minpoly.json.gz` | upstream | `dbf4c29d4e77f8bc1b884525e07cec4dc4349275` | `42bba0fc95dd06b4c4ee29790550a588a50b1b0ce2344f5d5cedda386bd03918` |
| `source/search/exact/minpoly/data/n-75.minpoly.json.gz` | upstream | `099369dde1e036cbe225c2dee3c116dcbcb5f057` | `275fbfe36fdf2a64f7fd55a98acd3f6d3b8175313dd3131ee6134ca2061b1a0a` |
| `source/search/exact/minpoly/data/n-76.minpoly.json.gz` | upstream | `9253a55cf8697d69c3bbabcf4d828b8ebffdf1dc` | `526b4f59e8765aafe66070212c5e74a165f35a9b049cb61fddb95d3c541f825c` |
| `source/search/exact/minpoly/data/n-77.minpoly.json.gz` | upstream | `ad4e26f08556d82e7495f596e8a8b472306fb5b6` | `22d41567722d9d77171bded97fe3295f846d255de6ef23fc9204f4b97d4f5974` |
| `source/search/exact/minpoly/data/n-78.minpoly.json.gz` | upstream | `0435f7337bf84cacf9ef14ec2126adb713a62f22` | `e26c17510452b36a384b2dd0bd22bb7c88c9a2bff22c984d31ce006e1752ce9d` |
| `source/search/exact/minpoly/data/n-79.minpoly.json.gz` | upstream | `5e9f5f4a0e72ed39a6edd739159452a9d4d1c9d2` | `8ef366a2d4c6a56277e75b3d20a790ed0005214326af15142f63089e43e89f45` |
| `source/search/exact/minpoly/data/n-80.minpoly.json.gz` | upstream | `98f181cd3e5627347535e936ad4ae9fa26f22fef` | `e2faa3014beff9e692c1341118b611e061c65d86a664cac2e7a4a561e0d37660` |
| `source/search/exact/minpoly/data/n-81.minpoly.json.gz` | upstream | `94684919ec37a4e7c9778578ee6ec672686d541e` | `cb61372d430085c6fca209d81fa68ea3986d3b8da01293159211b7be2a2ad547` |
| `source/search/exact/minpoly/data/n-82.minpoly.json.gz` | upstream | `dd894836de5785518b5f4fd4e80c6a2354233659` | `16adf9aea32cd1a279e3d41891559acb1198269e6193dbd4c669df85e2cef735` |
| `source/search/exact/minpoly/data/n-84.minpoly.json.gz` | upstream | `e0c1edc17bac4c4eccfe8ddca9559bcb503d80ef` | `94614b3dd722f0136a7714ca33691ea8d24150292d6e08c41907d7e2f4f0688d` |
| `source/search/exact/minpoly/data/n-85.minpoly.json.gz` | upstream | `450534a25c591273ec10572a06837d04ecdfcf8f` | `e1167162610f8f9a58f7fe78cc20efee9a1c65da095006b23d55193ed346da26` |
| `source/search/exact/minpoly/data/n-86.minpoly.json.gz` | upstream | `6149cec36558df72a61f8e8d782ee4302814004e` | `a3fab473450306c5028ea5e136cb023e57a9af87568b49ce8f4aa8e22827d258` |
| `source/search/exact/minpoly/data/n-89.minpoly.json.gz` | upstream | `6d72287e181747dde43db8097c42374970b30423` | `610c71058249b12123a20254a1cbb6fb45fbafdb42f7177116fce706ed8a7ade` |
| `source/search/exact/minpoly/data/n-90.minpoly.json.gz` | upstream | `8824d9a4b9a146d02b33912e8d05b331c6971041` | `3a92fb8974c3aff8edce0b101112c4be41349c4a9077ba0a15fb3f71c2ac2b3f` |
| `source/search/exact/minpoly/data/n-91.minpoly.json.gz` | upstream | `836f63574dbfea90de0bae2b413c722955c81a57` | `e0edce67ca1c2e0eac2dbd3049eee67832eb7f0704677764704d1c1114d5b668` |
| `source/search/exact/minpoly/data/n-92.minpoly.json.gz` | upstream | `edbf351b6de5ece17eb90ffa60f5554594befec5` | `09e9b0da28bb032b328c499dea5bad97cfdd8a7ad462daa4db104b398b0fd9f9` |
| `source/search/exact/minpoly/data/n-93.minpoly.json.gz` | upstream | `eb71f26cbe424915dc970ae97dd3ea5aba3d0efa` | `71113876de68cf74a01ccf19373e1cace9e8520f8eabd6663aa0ea58a214c9e3` |
| `source/search/exact/minpoly/data/n-94.minpoly.json.gz` | upstream | `0d25d2693bdcd0310c6259ce1f385c40e8790806` | `dbd0ac2b62b4ea9e2322f43ecdc0ec8a9b579e16c3f1e73ab23eb9792616cfac` |
| `source/search/exact/minpoly/data/n-95.minpoly.json.gz` | upstream | `252253931715b8da0e4c0325547323c080afa0b6` | `c6c6a0fb8e4ae778326f6967b959a5d9578eb2df44d5f692241c5d601885c1a7` |
| `source/search/exact/minpoly/data/n-96.minpoly.json.gz` | upstream | `4db835d6ecdc91f6ea8f44877e9efb89453f30d3` | `2f4046393793e538065c61a0962bd57193c52dcaecfdb0029e8842f420833034` |
| `source/search/exact/minpoly/data/n-97.minpoly.json.gz` | upstream | `a1b9b8c387d871368dd4fc34c9ebe0208bf571b6` | `9453e739e1430fa1725db1c66e9758d9a8b3b70c339a1dbb3caccf509a35bc5f` |
| `source/search/exact/minpoly/data/n-98.minpoly.json.gz` | upstream | `17648a15fee4f0307ff41f1b40e139f32a3afe3d` | `d3adb4b00e47511f5665016c935548dd1cedcdb7cd445ce05b42dafb64654a4d` |
| `source/search/exact/minpoly/data/n-99.minpoly.json.gz` | upstream | `436c521092c5e1c649da1d678581452e59e3f482` | `4378749eab2ad4723e22f0c5816cb2671636087cc5b23b9575c6aa7dcd5650eb` |
| `source/search/exact/minpoly/data/n-100.minpoly.json.gz` | upstream | `8dd2dee1b4314aae00ceb78a9debea4d10922b33` | `05ede6f225ff779b548c17d0cbbb42e987475bd052d0d12adc1aa3f01db1bfff` |
| `source/search/exact/minpoly/data/n-101.minpoly.json.gz` | upstream | `670eac3ac8160ec2f7ea3bc79b94116a39002fe5` | `8bc049db587a337d30deaabf223e317ec9b1ad3d84bc8d0b3744df1712f0cfc2` |
| `source/search/exact/minpoly/data/n-104.minpoly.json.gz` | upstream | `4d93d259217bebbb11a042082b5b9b975661c6a5` | `a707d76bff03a1419292b4c129fd32151a0b30205cbf8b89584dc86a8ff029f3` |
| `source/search/exact/minpoly/data/n-107.minpoly.json.gz` | upstream | `4cbd27d385d117bfa7fd32615948ef08c0639909` | `67925fbd274013c727ce529d5f97752a69ac3a38c7ca5a94269f9cd117bf1994` |
| `source/search/exact/minpoly/data/n-109.minpoly.json.gz` | upstream | `92d1aaa9387bc664c76d80a775c33f8a8eea4641` | `6032f2d60ed095ec42b0f3637ccec3ecfd6259a273970035ab74763a0a0c3946` |
| `source/search/exact/minpoly/data/n-111.minpoly.json.gz` | upstream | `2b171cc89522a9092b91e5e3641ec67b278db02b` | `170cef7cd7c00667bc65cd4c6b22d8b43e9ba15f2fa20d12ba23afbda8d89e1b` |
| `source/search/exact/minpoly/data/n-112.minpoly.json.gz` | upstream | `eabf1fef6de0a126090b30728dd4703adcf2ebe7` | `eb08f39fad7fb54c185456d8f285233f1eb25a896777f6d1e2241b57787598f9` |
| `source/search/exact/minpoly/data/n-113.minpoly.json.gz` | upstream | `4642b684d6e92155a84a3782081fefbb36485f0f` | `3ea6e34db9a9bc00f5703e9b0eb39bc86ed73437809b49ae0a19ade50f68b6df` |
| `source/search/exact/minpoly/data/n-114.minpoly.json.gz` | upstream | `85802699f36dbb2920935272a64362662bb640ff` | `f5dda2a641776488bf0b17acc4ed8dc01ddb43c95075598bf4ae14118a369222` |
| `source/search/exact/minpoly/data/n-115.minpoly.json.gz` | upstream | `d7ef6d2028078208eeea484bd8fc78e63d25cf42` | `9bb73db1f95e41aa26329b0074279a6922d09441af6909f8ef8ba75219e339d7` |
| `source/search/exact/minpoly/data/n-116.minpoly.json.gz` | upstream | `8451ab16da492ecc63c5e4bbbffca02d78904df3` | `e9a92febc9d5100380b738b9434534dfa56af54faa95058fca7935b41c71a46f` |
| `source/search/exact/minpoly/data/n-117.minpoly.json.gz` | upstream | `1b19674a46433519a98f024298b6256767bfcda9` | `06dcb3741801247eeaa7be74b8c3f45bf12ec283e909867b58b2963bdc2343e2` |
| `source/search/exact/minpoly/data/n-118.minpoly.json.gz` | upstream | `a92fadc3182c818c7ab0a05d4a6735e25e1b442b` | `3065d9ba00ed018ee5563f4a36d0e8119652e81499c086e013222cc71b1ba917` |
| `source/search/exact/minpoly/data/n-119.minpoly.json.gz` | upstream | `e47b0bf689cb16393bf2a3d22248242ec1790b9d` | `bf90b17f77f23854fdf1ab24853914d4f6ba617f14395fa1cd71dfac89c987a2` |
| `source/search/exact/minpoly/data/n-120.minpoly.json.gz` | upstream | `9ccabef3a9e8264a157d18f86d219411d40f84c7` | `2e8314423bce92b00b8c92c0f08d50f716f08f3051d6b41fca49e0e8e355d801` |
| `source/search/exact/minpoly/data/n-121.minpoly.json.gz` | upstream | `a67e842c38575d2774e9f7330b50370db88ecda9` | `b5b44cfd1cf72b5125f9f79d3f5a1aa04df556ec12a647bd6da6f10b46bb84fe` |
| `source/search/exact/minpoly/data/n-122.minpoly.json.gz` | upstream | `c29fc0adfc89cbaf7cefb80ae4565d9cec661cb7` | `b16e5e63428974ca9aa4034adb881c8638c7a4853b7c0c1550a21caa2ab8ace8` |
| `source/search/exact/minpoly/data/n-124.minpoly.json.gz` | upstream | `3d87d65758a91ace8072a19970ce211caa815c64` | `eacce72c8cc3515ebe44b53a8a7636e8a131e43f0348fa2b1ed80298e00164fa` |
| `source/search/exact/minpoly/data/n-125.minpoly.json.gz` | upstream | `77b4a2a6d98a88af7302210fc60b736bb0a7bc23` | `11b45b84309df5809aec605ce71cf9780e9998efe6f0186648c262d02c4d4442` |
| `source/search/exact/minpoly/data/n-127.minpoly.json.gz` | upstream | `714661c25e4dc29e6c2d40c648a9e6841a925bad` | `cebf5a75ad5f72fd99e6e2e169516ba44978badffd302810e0e3752cee52a97f` |
| `source/search/exact/minpoly/data/n-133.minpoly.json.gz` | upstream | `23ac7bab520a92a57fdf603742e10850977b2ffe` | `a432bf3f9e03ff12b2b17644d9b286a501fc4721f725ba085fef6b72e5f0f6d7` |
| `source/search/exact/minpoly/data/n-134.minpoly.json.gz` | upstream | `686c74f4d5d57140859c49de523359521aba09d9` | `c3c0e6f40d10e3140217b6c2b0a8d736211bffab40c3a4d81fe891f81bdd0796` |
| `source/search/exact/minpoly/data/n-135.minpoly.json.gz` | upstream | `d9981a00954e26572bf3ff484977513c1066a3bf` | `14165e99598ba8e1fd14e01f645b76c6fce4f0603efe8aaa09e40c84229f9ba9` |
| `source/search/exact/minpoly/data/n-136.minpoly.json.gz` | upstream | `e82cb9efe36b7f45acfabc19ec92022ed47901ba` | `9890507502b6686f7399e97731464b28c2fc8d18a1edb1e142827044e0a04f3c` |
| `source/search/exact/minpoly/data/n-137.minpoly.json.gz` | upstream | `a7942cef0d10683d069721c19786f7bf3dec5bb7` | `fbf75f39056100503a7753535ccc9a82366c54e75853be3dc99c36b25e1bcd72` |
| `source/search/exact/minpoly/data/n-138.minpoly.json.gz` | upstream | `f89033dc68c6ad1e5e74069f2bf02c7dade611d4` | `8cdc013b878bac29c0e81e4aef6b70a95553d280c1b026a119d6edf8f56e494d` |
| `source/search/exact/minpoly/data/n-139.minpoly.json.gz` | upstream | `c85a5bef30e865858a3afbb829e14625c525b3a0` | `98fda29dd5b194d4337c30534fef911e84bee2cce2bd14bf54a4d9a1b16bfd63` |
| `source/search/exact/minpoly/data/n-140.minpoly.json.gz` | upstream | `293b1d80a384ffde246108ff4fbf1f362d95b049` | `829e51ccbc385f73bb44e360a58555e314ede9fd1ba9d7d4529d1a11df8d2506` |
| `source/search/exact/minpoly/data/n-141.minpoly.json.gz` | upstream | `20dd2422fd75a3566f4fe4f2f4457af36631ec49` | `99c909a2932a26e25e088945fc529d7ce034a7c096b5f0dcfb8110ea6572a9e2` |
| `source/search/exact/minpoly/data/n-142.minpoly.json.gz` | upstream | `40043d5a1dddca53adef848186b72bceda384111` | `944deb79666da525f402607c2eaca9a52c162895ee1d521b916eecb0efa97b92` |
| `source/search/exact/minpoly/data/n-143.minpoly.json.gz` | upstream | `cec60c9da612ab6ef357970e8f4e0cf30e4ad928` | `576d88412a0b21217b165977f3a7e5153b777275c6ae6b178852afd203811d42` |
| `source/search/exact/minpoly/data/n-144.minpoly.json.gz` | upstream | `289876bd3266a090b057bdffa0642262058b00b5` | `508496a502053ec2c51abd034b0e65454f668ea49ecddc0d676b6f40bcf49912` |
| `source/search/exact/minpoly/data/n-145.minpoly.json.gz` | upstream | `981961b37382f390e37c79a9f05e2c6a41882e84` | `e9d10f37f1f80f24de792bd715d80524cb38c47f21ca7cc355c077304a85c891` |
| `source/search/exact/minpoly/data/n-147.minpoly.json.gz` | upstream | `3d7dab028877252c697e440f41e1652395cd5a4b` | `6d7052167b2a809c2f9cb2bb4cf88e0fa468b322fb2f7a80388e968a3ee1a556` |
| `source/search/exact/minpoly/data/n-148.minpoly.json.gz` | upstream | `45e5511fc9a6b4f0bd9352bb1a3cb2c1acd8651e` | `67cd414f2b5fbe75567a81ad26d81332f77a7916f7c74ee441a3ad06ef7dc78a` |
| `source/search/exact/minpoly/data/n-149.minpoly.json.gz` | upstream | `ee8a95cf49fca0723c82745578814dcdb4cb9f2f` | `ef8230b355944040dbc3c0291a5caf2f7016de9ed37b3bee2db9bfbf6440f7af` |
| `source/search/exact/minpoly/data/n-150.minpoly.json.gz` | upstream | `933fed9e41d08e03af36502d631255273e2321dc` | `6935d696a71d015d9a1750579897285c2e9268c732a7b0bb432e6b43ac35729f` |
| `source/search/exact/minpoly/data/n-151.minpoly.json.gz` | upstream | `e54111dbd07b6da16dbc329704800390c01c12da` | `0c492c0aa40f386f5a7856be6061934ac3bb3597510130c394726552f8714a87` |
| `source/search/exact/minpoly/data/n-153.minpoly.json.gz` | upstream | `40538bc8c4bbced30967a17e93457ae24cb70120` | `977b4eb07cc3e90c9063918def6fa81ef98242b636c22a1907b37775fa8588f2` |
| `source/search/exact/minpoly/data/n-157.minpoly.json.gz` | upstream | `a1ca456599d1b5bd3a96705a7a9d8aebc5d130ab` | `0cfbd02af2f52c9b1654cea4c066821f79bb34d7640b3460923b0220d8d79e9d` |
| `source/search/exact/minpoly/data/n-158.minpoly.json.gz` | upstream | `b3fe6cad1f9fd24f9dcc45c55761f3351faf9844` | `d4c8f6ee4ef064f15d0cd5c81aedeb9434632a5ad55093f4bf05f9a9f14d12c5` |
| `source/search/exact/minpoly/data/n-159.minpoly.json.gz` | upstream | `1be63645b1393b57061dc84849a9dbf44ecd5842` | `30768ed1c660dc7e16a5b43eede79599d56d82abc2183154b9306a3bdadb5b87` |
| `source/search/exact/minpoly/data/n-160.minpoly.json.gz` | upstream | `98440f45c09d0b73d6be98d5567844e42f926acf` | `c6c24afbd2255d0a16e98fa5d0038e43ded7b5ae26ab3ae4bc31695d8320288a` |
| `source/search/exact/minpoly/data/n-161.minpoly.json.gz` | upstream | `0e2d4e506fd20bbe973eb7efe447b507052dd245` | `01e3629d0d66844ae4ee9d398cf16f7424d9b134203b79b88bc1a4f868d417ed` |
| `source/search/exact/minpoly/data/n-162.minpoly.json.gz` | upstream | `3fff44c006fc147d437dd75f7d76fe92c21a6e02` | `d93425556763de2d017fb9c1583625085e621e0a954358ad21665d631ac2b733` |
| `source/search/exact/minpoly/data/n-163.minpoly.json.gz` | upstream | `1bff4b9eb3b712988659cc15a6984da7408c7784` | `939c790fcc78fa49515372f52b86d918652328af7685069de33ba021209cbe6d` |
| `source/search/exact/minpoly/data/n-164.minpoly.json.gz` | upstream | `7ca5900229a4e5019bbed8b9d2db2ff4d3ec3d9e` | `1d87df331ab483618ad86e91732d8503cbaca5ef2badb99341cb38421ba5a924` |
| `source/search/exact/minpoly/data/n-165.minpoly.json.gz` | upstream | `bd791c71662f7c71a93feeb858eb550a4d53c476` | `aec3aebbea769e0dc9f4a8d7617ffd4726096d96b81f926493357040f4835d3f` |
| `source/search/exact/minpoly/data/n-166.minpoly.json.gz` | upstream | `48e26f483e391e47cf06ece779cc05debf94c733` | `a03b6a320efb966d0b5ce4a51e12c39bb0defe6a429e7f2f78126339f2ae2c86` |
| `source/search/exact/minpoly/data/n-167.minpoly.json.gz` | upstream | `cfb863abb39fa568f72ee50a12f0a82a6184886c` | `0dad0d98962a28948647c4c0446248b8e359d0d9c85dcc50b02c1e9ced6835ec` |
| `source/search/exact/minpoly/data/n-168.minpoly.json.gz` | upstream | `62ccd3ea3389c6796128710299ffe1e2d440c18a` | `57ef47ee9f41c9b2bba4c7b195b15b84c4a0fa1952c266114d1c5264fdd329ce` |
| `source/search/exact/minpoly/data/n-169.minpoly.json.gz` | upstream | `b8c36939d38c1a25bacea80136d36649d03411c7` | `0de615fdb29d4da7cb90cd42fcf78b04ef9677c58285a9c0bfec65240a57bf63` |
| `source/search/exact/minpoly/data/n-170.minpoly.json.gz` | upstream | `4223e467fc1b34e3671a00358bcb37d74e754354` | `c1f12b21602cf57fa58c1a36bf64380511d72db7887432f825c415c8fd0860cd` |
| `source/search/exact/minpoly/data/n-171.minpoly.json.gz` | upstream | `afc203b23c2d7f4ee6b390906cf28e124aacc7e3` | `32f336590f5b65d5f8ced9b348aacdb4786627f9ce93265fc2796598be2f077b` |
| `source/search/exact/minpoly/data/n-173.minpoly.json.gz` | upstream | `fa6a2df04552d1b3e589433d6b7ca1c89a95b284` | `2f5abaadd2f3c4d0ab23fefb836b13999cb443a43092b027711139c11244a2a1` |
| `source/search/exact/minpoly/data/n-175.minpoly.json.gz` | upstream | `f263a8cc2182e287b42d77cc1011cdce4a480c46` | `3a4a3fdb429cdc6e2097739ec65da32505ddf8b8a8bd81f2fb7baf11ddabaeb6` |
| `source/search/exact/minpoly/data/n-176.minpoly.json.gz` | upstream | `8a7c31a32e69fea24782bea6bcece648c5d69885` | `104eba90c7584a9c534e7b31b3acbb84043128057110186cc4749e0911a1b7bb` |
| `source/search/exact/minpoly/data/n-178.minpoly.json.gz` | upstream | `8db74e917427a815cd53a16d36e17330ee40d406` | `f04d51d02df440d0811ab003f51156b5f52acea4e9e7768afb9664648a862873` |
| `source/search/exact/minpoly/data/n-183.minpoly.json.gz` | upstream | `e818a94105810cb99c30eabfacca6f25e9aa23cf` | `6efe3418c2a214878261061d945015cf2ce516c933583b7740cf8c209ed094ff` |
| `source/search/exact/minpoly/data/n-184.minpoly.json.gz` | upstream | `59135d3d2e76610cf24f7015914faff6f18af855` | `b74c70ea4e34a27b0d77affbc38aa68160ac352ad05da70bd8be1388625e76e6` |
| `source/search/exact/minpoly/data/n-185.minpoly.json.gz` | upstream | `6f23dbdb46018e8c3aceb9c51fbdc91c66a44f41` | `1e4fc62830baaf3bf2a4a8c5ef89ba5be8de4ff7e6c01cd85d435fef52a6a95b` |
| `source/search/exact/minpoly/data/n-186.minpoly.json.gz` | upstream | `8fd28c0b315bdd122253feb650915a395b036451` | `b0eba2edcad2d6724b014bb729061139cc79f933d51300f6bb3c34065be7f197` |
| `source/search/exact/minpoly/data/n-187.minpoly.json.gz` | upstream | `5db37b3d3c27db23e6c50c35aa93839d6fc48084` | `b13178a0b197e46452e4fa61fa3a43095f4ea3cd3dc7a81bfcbe6c3353b872a1` |
| `source/search/exact/minpoly/data/n-188.minpoly.json.gz` | upstream | `0a94d9a4531ff672eff842a2cd6f509de06007f3` | `430839362923a03cfffd7f62e9342c30b6140aa65173f398490e405ba1d502d2` |
| `source/search/exact/minpoly/data/n-189.minpoly.json.gz` | upstream | `6703546627a4ad463a002b8b1ce45663a6dd729b` | `cb645fbbc6a3982036d1794932935fd5470b5d8298de22b8ee51297d8c29b1a8` |
| `source/search/exact/minpoly/data/n-190.minpoly.json.gz` | upstream | `376dbb47a7dc69c662252948dde57afaa6b1b163` | `bc698687a162f98efa17b28286874613bd8c82b0fa7d6b72c799b59b1435ccfc` |
| `source/search/exact/minpoly/data/n-191.minpoly.json.gz` | upstream | `353ff572d9ac648a6f93d92daaf8e1320cbbca51` | `d2717936c06df31344fce47f13368dcc5aed5e3cf5f1f197d3159d313c376f4b` |
| `source/search/exact/minpoly/data/n-192.minpoly.json.gz` | upstream | `3a6d7e48cbf170250027d11314cf2d327f795f19` | `a9549785888aaf12ff3ed2ddb2163ba8396d325c56254ce753bec57cdcaa2e68` |
| `source/search/exact/minpoly/data/n-193.minpoly.json.gz` | upstream | `2c4a7061dde3df6d77d3645fde5798d6a6aa2bfb` | `a7dd988dd2385e44e61a28990f4dfea4eaf8239dbf4561d2d074b8b0f7a347c6` |
| `source/search/exact/minpoly/data/n-194.minpoly.json.gz` | upstream | `bc996394bd7e5580e14f4f90ecda904d271eb0a1` | `a8859d988ec4128c75698042890600045118a310d1cefb874cd52bc9d3cf8016` |
| `source/search/exact/minpoly/data/n-195.minpoly.json.gz` | upstream | `cf5de96eb6e434911bcbfcd0d7c2a1aa8b534b78` | `ddd9676d5204f1a0fa70a74244dcef6ad4633e61b5458d30ecb82d0e8d229d9d` |
| `source/search/exact/minpoly/data/n-196.minpoly.json.gz` | upstream | `86b9fec289b322f8ad0f560ad011c5bbd2e91cc3` | `05f01caf6df1e815127019510f5ab7a8cb72d27313755086083839a646b7116d` |
| `source/search/exact/minpoly/data/n-197.minpoly.json.gz` | upstream | `90163b925a3b6115f628f3f69730257db5028dcd` | `6affbc5cc7e23039bf2eeccf9cb1a217bea69e9fa9c25b41bfcd489164b0f508` |
| `source/search/exact/minpoly/data/n-198.minpoly.json.gz` | upstream | `a90880638bd570c0dc924768183a6f6891930b26` | `f6d765a743f3c1b5180000ab5a3f1ff121d913539ce7d2edcc799ad39c493362` |
| `source/search/exact/minpoly/data/n-200.minpoly.json.gz` | upstream | `628244b632263a848f79a7407abc5e36e17c4866` | `261fd438686ed752b782405f36c09464d16c90e98e761b1a649e5e807bbfe18d` |
| `source/search/exact/minpoly/data/n-202.minpoly.json.gz` | upstream | `ad7e24dc550f0cf1129a4250eb434147e95f4428` | `bfce4688160acdfa8b5715f8b3858a20af793a81f78fb2f518ad111a873fb88b` |
| `source/search/exact/minpoly/data/n-203.minpoly.json.gz` | upstream | `a1be82106c3293793b0956b16733e064ce038cac` | `9fe4d696bd7803739f5aa8e020b3c8380f2f774971478ac1e5d1f1b7a2164faa` |
| `source/search/exact/minpoly/data/n-212.minpoly.json.gz` | upstream | `63c9c19297855ad63e8c4692f4594c8e7eb40a1c` | `2a7e3e60472f97d0171e87073a5cd167bf9e11b9c4ca2f6093f86c6746931d37` |
| `source/search/exact/minpoly/data/n-213.minpoly.json.gz` | upstream | `e5fde54ef65e5bdfa3b1d6158b77e6705f212759` | `c3b592072f813948ba05921acf280fbf59582f162277b1fc4c1aaf9432efe31a` |
| `source/search/exact/minpoly/data/n-214.minpoly.json.gz` | upstream | `1a54e343895d1eb3867e8663170ecbd56ea0a91e` | `f0867cdc67f3bc85e63d8b49adfea4a409a2e84599cca58d587bf88ddff21d5b` |
| `source/search/exact/minpoly/data/n-215.minpoly.json.gz` | upstream | `567adfc7ade642480a6dcb6caf86f3b9f85b493c` | `c453580c797fd97ad6078ae96abd78e5a05e9a7b791768c3ca8fef8490ea1127` |
| `source/search/exact/minpoly/data/n-216.minpoly.json.gz` | upstream | `518c4b32684426e25db024201ecf164efaaa06de` | `768081b150fec797d0334ecd35f461dd97424e4d593439da7df79c0f3d1d6560` |
| `source/search/exact/minpoly/data/n-217.minpoly.json.gz` | upstream | `864415e8e82ea4050d4dd704d1827d9097855f92` | `535277224e1df76d334403042d73ec9ed7b8c14efd78e3d3d4876935554d6571` |
| `source/search/exact/minpoly/data/n-218.minpoly.json.gz` | upstream | `71900e5f9fd2ef7cecacb20e8c30c2ce64980910` | `95f6133d11e4d082804e21f834e709924ad3820cd667ba56e1b450347f71eaf1` |
| `source/search/exact/minpoly/data/n-219.minpoly.json.gz` | upstream | `a94f8a675106769c96f411fbfad740d17b85e9df` | `a8f9c9fde229f453e3963b4041f927321d934ab54b6be24d88fbaab5cdcc3f7b` |
| `source/search/exact/minpoly/data/n-220.minpoly.json.gz` | upstream | `c266744975b49aaa1eed8be4e2edf1e20eaa8ce3` | `236b760a2b461b23939e55e5b3b531893b6359ee3d566ff190906cb32cfab3ec` |
| `source/search/exact/minpoly/data/n-221.minpoly.json.gz` | upstream | `bb0b16ab70016bb835d3123cd48ce6ca41186e59` | `5babd10060bee5c2d48bdc3460257f084079d36a55e43227bc60adbb8a1faf4d` |
| `source/search/exact/minpoly/data/n-222.minpoly.json.gz` | upstream | `e4b107a6dd630a5998e628733584f98171132cb5` | `671e5da90c538cd65e879c3d518a6747cfb2f8f34a7a974bc391763ff95ebbeb` |
| `source/search/exact/minpoly/data/n-223.minpoly.json.gz` | upstream | `c941234b194d4a68dc0b1ba1d4f610e0822fe8fc` | `bd492c31b95627e782d5f31cb55e75e93fe417e46a5006b21d353a467203194e` |
| `source/search/exact/minpoly/data/n-224.minpoly.json.gz` | upstream | `c3490a68bafb00d4d7aef1155c374fd87518ecfd` | `975d8c91e9536c4ed2c316ad5f7cf838159f6cf407e63d8d6fb67b8834c02832` |
| `source/search/exact/minpoly/data/n-225.minpoly.json.gz` | upstream | `3b039a886154820eaafc83d59c8535b2ba6f7774` | `0fee0925e7792fa578d85ba9d5e33f61464a2a2c0ffd333f48e5fe45c343d7bd` |
| `source/search/exact/minpoly/data/n-226.minpoly.json.gz` | upstream | `9aea148b805d07981750eef67a9dc090acf1c29f` | `ab1a0737a3a772964a4ca5e9ad4874e02aa5a28a3f28b285c0e84d8aa982fcc2` |
| `source/search/exact/minpoly/data/n-227.minpoly.json.gz` | upstream | `33e74403c2bc8cef77880c3acadc177c2a2c95e1` | `7b475244f96de5b8bb5fd6fbaf226c9d48ed5f1ec58b97f780e431931c26c2fe` |
| `source/search/exact/minpoly/data/n-229.minpoly.json.gz` | upstream | `19b85ff4b797a0e76c2a2917627372403b4ec6c5` | `28de5aa258af0ad9f6476145c062b45b4ec30ad6dcf738556d49f23244181166` |
| `source/search/exact/minpoly/data/n-230.minpoly.json.gz` | upstream | `def71b5fcd450fd50bc9c2d8fc2d61e506f3c8b7` | `9579351d00f7869a572bd91a2fa9c87c12f5a8daa48cca740917ab1f4f05206a` |
| `source/search/exact/minpoly/data/n-232.minpoly.json.gz` | upstream | `e45e6949920b4d335cd8b2fd61e780493328061e` | `ce169747d297ec61ff37509dcbbdb91b1127dac9f11748fc69d92772e34d0beb` |
| `source/search/exact/minpoly/data/n-233.minpoly.json.gz` | upstream | `70644bd0515589a84b88212aaa0e6c17155b6ef3` | `fb8d527c25b8ac42897d5e43b0d532bb17ee1861bcbfb2d797428cd908923ee3` |
| `source/search/exact/minpoly/data/n-242.minpoly.json.gz` | upstream | `67ece822fb2d27f75c9bd8349b0084d886ecf8f3` | `0dc1c993831b66697c4bb18da0ee6135cc9d9de82638ecdc9249b9573ab04dbd` |
| `source/search/exact/minpoly/data/n-243.minpoly.json.gz` | upstream | `fc48ed379889023305a579d10bfd1ef2e68624b7` | `527f2a4c7f72be5e8e2731741c1cede42d2c28028f0153e43ea23f3d35491efb` |
| `source/search/exact/minpoly/data/n-244.minpoly.json.gz` | upstream | `6a273c59f2b8348c9475ba7df7ae9e31da14f5b4` | `8ce6e2772ab12579e2857d1cef4ba519e1b44032d4f440d8e6afb6fbcfed2012` |
| `source/search/exact/minpoly/data/n-245.minpoly.json.gz` | upstream | `cf67ea54d6a444a4322ec997efd35b302e1f4d82` | `bb9444008702a1dd986ee2fb360cdf28e1eb8b539a4417326b4c8db89cf0fe1f` |
| `source/search/exact/minpoly/data/n-246.minpoly.json.gz` | upstream | `9f5af2366beb040f19e926494cf8a629a66156d2` | `122b9db32d495842a76ac12726e883e48d90829b63a238c763c28d971459c693` |
| `source/search/exact/minpoly/data/n-247.minpoly.json.gz` | upstream | `3440d2ca39943d5360108d5c5138a015f9695f94` | `21b6d9533f02e5daf6b99fc1deb64270f494335690788120b460002922a40577` |
| `source/search/exact/minpoly/data/n-248.minpoly.json.gz` | upstream | `1abdee8350f07bbdf25f8a4735b54fef28e8168f` | `d3f4df2fd7b85d00fcd07c39b1ab574e4731003b4d429b2428ba03ce34c2715d` |
| `source/search/exact/minpoly/data/n-249.minpoly.json.gz` | upstream | `dca21ddd2d375bfc5b74f0574ef7460c118f83dd` | `9b633f8b4bad2826e22db48807ebbc467bce26228b35d67b6a5b24740805a1c0` |
| `source/search/exact/minpoly/data/n-250.minpoly.json.gz` | upstream | `642efc96146539a549cf26819b1edaf946fb53b8` | `5e669c2b29ec2e3ed9cdbc1134bc5bc6a12cffe5292f5e199d2df73b8cd5f0d5` |
| `source/search/exact/minpoly/data/n-251.minpoly.json.gz` | upstream | `02f0d4a80be7b4d3fe8ea25e304d65e953e07fdb` | `f5be97cc0014d6fa6b79aea9af1a4504ac99b420f09c03c97bcbab63b1d7c627` |
| `source/search/exact/minpoly/data/n-252.minpoly.json.gz` | upstream | `a063ce9567a5a541b2d06aa29671e867650ab1f1` | `e7d2c916b87a883ee319b679d5ca06cf29d1d0b6e49cd0023e1ce4b774913d89` |
| `source/search/exact/minpoly/data/n-253.minpoly.json.gz` | upstream | `675cd06ba2aef42c50809211925f14577d72c94e` | `7de44ef41bf5f8b405da52b3e66ed1d5fe2bccb7f1148142abc1dd7664345ba4` |
| `source/search/exact/minpoly/data/n-254.minpoly.json.gz` | upstream | `266456418aa71a4b8e35bd080b406619d77f7b62` | `47457054602421c08c3acacfa8be965c24cecc3cb1c8993a76d6619e212e9dfd` |
| `source/search/exact/minpoly/data/n-255.minpoly.json.gz` | upstream | `7d229de29552412f7c7256d72acf4ea7e3097469` | `05b9633bfb3fefc3c7f6a7d84742ab69ddb7af530811a3d7e2b63d808f37fcd6` |
| `source/search/exact/minpoly/data/n-256.minpoly.json.gz` | upstream | `b4bc72f87da05d3d849a64de78cea29e3b26b5ff` | `c750f11bb7e6e19bf70751fafc780f35758bcbb632fd0905d5d11e84ac10f656` |
| `source/search/exact/minpoly/data/n-258.minpoly.json.gz` | upstream | `c4f69dad3f452563694d839a62307312908eb09a` | `0e3940db319dd229cc4aecb2be454322de068a054d1dd8740a81d57e92a57bfa` |
| `source/search/exact/minpoly/data/n-260.minpoly.json.gz` | upstream | `bcfd4555aec750f5a52b6f14bcc7b523434fd1ce` | `c29fa344f8340e75533bf69c3df6a671ff6144c7a2843720ab714aad5f4f6b6d` |
| `source/search/exact/minpoly/data/n-261.minpoly.json.gz` | upstream | `9353bfc2ab2254e8f6062e38766079d838cc91cc` | `5b6fb045e27f354570e6a0dd2fef276b0ad911c38e153f13cf2c1b2957948756` |
| `source/search/exact/minpoly/data/n-264.minpoly.json.gz` | upstream | `831bdd911374616b1232323602a8c90a2756b1aa` | `9253aee967731458e59519ce3aab1b0fea68d13e949ef12fc626941815b22b7e` |
| `source/search/exact/minpoly/data/n-265.minpoly.json.gz` | upstream | `ea6eb73e819137581a1fd7be82ed1d925da7f38f` | `3378f73eab7b41e68c363cf5793bfdb07c594febe9e06d6550d5df7a5da39c84` |
| `source/search/exact/minpoly/data/n-267.minpoly.json.gz` | upstream | `ad0da71e8e602a9d5b279f0cd96b523a62f2d286` | `5d812547c189224cb5431ba3f4df488cfe8ed4f7ba85a35d445950fa15d9af53` |
| `source/search/exact/minpoly/data/n-276.minpoly.json.gz` | upstream | `072813f9e236101d609f08a77b298396a62f91bd` | `b6e0f40a7c9b8d768615085d8f8955f3893ec64a558a040e7de43fd823116ef4` |
| `source/search/exact/minpoly/data/n-277.minpoly.json.gz` | upstream | `3eb04fe48c095504539cc778969120ca4087bf76` | `93f774c21fcef01a7c7b2cd8776b48a1126c79cc0ccacce769607970ee89b602` |
| `source/search/exact/minpoly/data/n-278.minpoly.json.gz` | upstream | `bfa6e2a96d693ae99f29511891558dd48d8472be` | `7210d0a723d68d23d1793e69420ed1c2121a05ab7349c16dc1fcc67f232b5de8` |
| `source/search/exact/minpoly/data/n-279.minpoly.json.gz` | upstream | `696495c3f13751fc6c682663bcdadbb7932be7e3` | `be482a73d134d36b8e02f99a30cc118a8d78fbff4fb2388facf2908080b55801` |
| `source/search/exact/minpoly/data/n-280.minpoly.json.gz` | upstream | `709585ceca8ce9e9548b5a58ecd5f4ec4f1331c3` | `700c38286966fb1734a2785dfdeaef0f8868ef49aa604bbd06364199fd71d69d` |
| `source/search/exact/minpoly/data/n-281.minpoly.json.gz` | upstream | `4716b9dd140fb86827f5d503f5f8f2d35934fbb2` | `be681eb0b1f996e345a9d995c576281d9e6258aac470f3ce891b3d69bcc2f7f1` |
| `source/search/exact/minpoly/data/n-282.minpoly.json.gz` | upstream | `ff11ac92ff89ceb6253887318b8fa0a1893c857b` | `2c53cde5b6eebd80e9c411c05abaa4ad1b3ac1c7b6074be142b4539af9c35422` |
| `source/search/exact/minpoly/data/n-283.minpoly.json.gz` | upstream | `0774292c85c110a96bb46d88bc12829e1b5bb20a` | `1714f69070935ef92199edf2d725927189dbf3da3a197769cc416ebe12a60434` |
| `source/search/exact/minpoly/data/n-284.minpoly.json.gz` | upstream | `d3ec32d1c50759dae37bd9c7c64e039c171ece29` | `d3ccc2ef00e036696da38fa410802cd0e6636c5c779a363d0ca38f936a35800b` |
| `source/search/exact/minpoly/data/n-285.minpoly.json.gz` | upstream | `ef5c86c6670c6dd015e48ba13541dd075f2e7818` | `00e694134dfc7d66c92815655fc3be4df2464a5f068a88c8efb76c867d318360` |
| `source/search/exact/minpoly/data/n-286.minpoly.json.gz` | upstream | `74d48942b3e716e1689b67a59fbdfae27743595a` | `dd54b0eb79f286291c2e8148dc9ee021f4fa5696c6ae72b5c5bd6b89770f6da6` |
| `source/search/exact/minpoly/data/n-287.minpoly.json.gz` | upstream | `dafafd79eb345822f45416b84c014e82858e8a63` | `48682b20e3f5913a362e58b551c76e190b19ba6082f7996d57d9265b8dfa9433` |
| `source/search/exact/minpoly/data/n-288.minpoly.json.gz` | upstream | `902c29e095c6c1eb3f4b08f9d2136c73f3494ed8` | `167c785f4ad8cfce2aaca2c53418f714b8f0949cb95a7a79538b407578635611` |
| `source/search/exact/minpoly/data/n-289.minpoly.json.gz` | upstream | `a02d48f890adb6b06f934db33432d2cf1bc29e6c` | `df7ffb293650a64082c5d2538609b2fa37972665d1aecb4270150747f22dc8a1` |
| `source/search/exact/minpoly/data/n-290.minpoly.json.gz` | upstream | `5ecc23d9545492ecc2e8e1b03266c5463c9b9358` | `deb232479489e2b47037b2298026273d06171385dbc1d5860449f3227f90242d` |
| `source/search/exact/minpoly/data/n-291.minpoly.json.gz` | upstream | `a1e412f5f4824a48b8acf5176c032c491fff4a12` | `5940d6984609e2b496da7916f7c7a0c39f1aeeca5ce915fd1c71aaf8e2954246` |
| `source/search/exact/minpoly/data/n-293.minpoly.json.gz` | upstream | `f1fbcb77c725cccc540645ce877684683b7fa0e1` | `36cba207c8e33db11889f38f89b2f0dddaae04d532aa9aaac882f7ca667e2873` |
| `source/search/exact/minpoly/data/n-294.minpoly.json.gz` | upstream | `bd6dad8f58ac07dcb6588118a9411bd4da74902d` | `fe8c21b58ea4a3a5cdc52a7c40db1366b39e7043f66be71419fcf4aab4f7f289` |
| `source/search/exact/minpoly/data/n-298.minpoly.json.gz` | upstream | `a405c7ed2092516508241baa116fcd05a988dfdf` | `fa49fa328049d7e70da6931a77eae9051ac5a320154726b1514e9b046b2bf170` |
| `source/search/exact/minpoly/data/n-313.minpoly.json.gz` | upstream | `958dc4aa3d13b2a0329168314925a3139c6295f4` | `4445b324a7518f77c47aec94f8c8ab6710f560f600ad1c67b45fc8bcdce58b1c` |
| `source/search/exact/minpoly/data/n-314.minpoly.json.gz` | upstream | `7888d9e837e1adb48dca87b489de100c4e8abb60` | `9383a774baed850c2255a786c4b17ff8f478efcabb958592e4a1cae6b2376e09` |
| `source/search/exact/minpoly/data/n-315.minpoly.json.gz` | upstream | `2b79b6003784fded57cfbd9a215711ab88a859ef` | `8b92f12d22a1c2f2c25317484b92802c4dd76b73536caed6d72a4e1f702eb42f` |
| `source/search/exact/minpoly/data/n-316.minpoly.json.gz` | upstream | `daf5d4cd516693c56412fc4ca2c0d1198858364f` | `bfc89593aa1e88bdbe280fe928d42e5bcd0ebefd6735ae14b8b3b2a341911f20` |
| `source/search/exact/minpoly/data/n-317.minpoly.json.gz` | upstream | `0eb7b562105dab5582f2c221c2e8d29318f3e7ed` | `4cff40df64123f12a5d58b235eb3c1dbb9ec26807961c7c9ddb7bc4b3ca4c2a8` |
| `source/search/exact/minpoly/data/n-318.minpoly.json.gz` | upstream | `19686a8351e835d4010f24503eba52526033dfae` | `c5128e901fd1adbe92a112eb23049d6b15d814e04ee4a819b9a8b73c698de3f4` |
| `source/search/exact/minpoly/data/n-319.minpoly.json.gz` | upstream | `da1d65dfb35422b443fdea2bfb40a80e711b9794` | `56c4868218375c0426cb547eb0d514d9dc0254e8b031ca48a19e97ed5430c200` |
| `source/search/exact/minpoly/data/n-320.minpoly.json.gz` | upstream | `6d4b49ef69d67d6000a1134d9e26909cab51c843` | `587de4d8cd0462dbf1a893f37f40b2d29f167de83ae51ca1448e8d54972b5178` |
| `source/search/exact/minpoly/data/n-321.minpoly.json.gz` | upstream | `5390e1f67529dfb7e81ea3065ac17b29cfc8ce22` | `5f6570daa9395bf6a32a4aa34ae011c7fa0f9947d1d77bf7b74895648d296c90` |
| `source/search/exact/minpoly/data/n-322.minpoly.json.gz` | upstream | `6958c106a03362afcaf9e49f722d66a6ae2cb502` | `2580b50b379f1e6d91acf5138e45a11c4e9108d23afaeaf8df15715f557b8f59` |
| `source/search/exact/minpoly/data/n-323.minpoly.json.gz` | upstream | `ccb87073b1fb3ae5904ec294a24e46a1bca87014` | `aec4cbdb30cbcc54760991fd1391283b7f51da11326a8b1cfdfbcc874bb64def` |
| `source/search/exact/minpoly/data/n-324.minpoly.json.gz` | upstream | `7477d0f7562ad32f81e9df7b861a16ec716d6c60` | `fd119584d10dcfc89fbb6f22f93cfc24c2141899d210ed049560a066ba4ddb8d` |

## Retained Here

`devtools.acquire_source` wrote the tree part of the packet from a sparse checkout at the
tag commit, from the declaration in
[acquisition/declaration.json](acquisition/declaration.json).
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest:
242 files, 2,116,155 bytes.
Retained, 235 files and 2,046,118 bytes: `LICENSE`, `CREDITS.md`, and the exact forms of
the 233 configurations the grade-C archive certifies,
`search/exact/minpoly/data/n-N.minpoly.json.gz`, as their upstream gzip files, each bound
by the Original Gzip Files table. The n = 10 recomputation read one of them; the 23 October review’s
checker read all 233. Those at 230 and 261 are also retained, identical, by the `ad86d42`
packet. The other 36 exact forms in that directory, of field degree above 4 or timed out,
are pinned by the commit alone.
Pinned by digest against the identical copies the `ad86d42` packet retains:
`gradec.py`, `localmin.py`, `verify_exact.py`, `geom.py`, `env.sh`,
`search/exact/homotopy/N29.md` and `tasks/exact-minpoly/grade-C.md`.
The release assets are not in the Git tree; `acquisition/release.json` binds them.

## Credit and Licence

Evan Daniel wrote the source under the MIT licence (`LICENSE`), with credits in
`CREDITS.md`, which says the repository’s work was produced by Claude (Anthropic) under
human direction. The archives carry no licence file of their own; their READMEs name the
repository.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source evand-exact-data-2026-10-12 --check
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
