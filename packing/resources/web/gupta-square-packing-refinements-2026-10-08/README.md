# Gupta Precision Refinements: Factual Source Packet

This packet retains all seventeen original certificates and seventeen complete
comparators for [issue #438](https://github.com/jlevy/squares/issues/438) from
[Gupta’s pinned source](https://github.com/SidG2k1/square-packing-refinements/tree/9643cb5a78c1d4dcfc867c80a6920c3a6219d05a).
Every file in the
[immutable v1.0.0 ZIP](https://github.com/SidG2k1/square-packing-refinements/releases/tag/v1.0.0)
matches the pinned Git tree.
The ZIP has 170,197 bytes and SHA-256
`960536b8dd8f019c35cf5baf795c3800cdcb937f8344d30611cf541abb85eab7`.

The source reports precision refinements at n = 88, 130, 153, 154, 179, 180, 199, 207,
208, 209, 236, 237, 238, 239. Its n = 108, 123 and 129 certificates are withdrawn after
smaller #432 constructions appeared.
All seventeen inputs remain complete.
Source feasibility logs are unconfirmed reports.

The source credits Nate Chaoweeraprasit (itsnaka) for the published SQUISH
constructions, Evan Daniel for the optimizer, and Siddharth Gupta for these refinements.
The original CREDITS.txt and CITATION.cff are hash-pinned in the acquisition record.

## Licence Boundary

No bundle-wide licence is stated.
The retained Evan Daniel MIT notice covers the cited solver; it does not license Gupta’s
programs or prose. The three source programs, two README files, CREDITS.txt and
CITATION.cff are hash-pinned without copying.
No author program was executed.
Factual certificates, comparators, findings, audit outputs, integrity manifests and the
solver licence notice are retained byte-for-byte after decompression.

## Custody and Reading

`acquisition/case-inputs.json` maps every count to original paths, original SHA-256
hashes, Git blobs and exact sides.
`acquisition/file-inventory.json` adds compressed hashes and sizes.
The subtree manifest covers all 49 pinned Git files.
The declaration and sources record follow the maintained `devtools.acquire_source`
contract.

Read a source path with
`devtools.retained_data.read_retained_bytes(packet / "source" / original_path, limit=1000000)`,
then `devtools.evand_exact_certificates.parse(text, expected_n=n)`. The maintained
reader bounds stored and decompressed bytes and refuses inconsistent plain/gzip twins.
All retained source files use deterministic `gzip -9n`; original input bytes are
unchanged. This API acquisition uses the maintained compression and validation APIs
without a local checkout.
Check it with `acquire_source.check(packet, repository_root)` and
`retained_data.check_packet(packet)`; the repository-relative paths match the
integration location.

The release record pins all eight assets.
The original ZIP and timestamp instructions are hash-pinned; the factual digest list,
timestamp query/reply, certificate chain and source verification transcript are
retained. These artifacts concern custody of bytes, not correctness or priority.
The local OpenSSL query and exact archive-digest checks passed against the supplied
certificate chain; an altered imprint was refused.
The commands and outputs are in `acquisition/timestamp-custody-check.json`. External
timestamp trust has not been independently established.

## Finite Feasibility Verification

The original two-worker native campaign completed all 51 full jobs in 255.693 seconds:
seventeen positives and 34 duplicate/outside controls through both maintained routes,
including every withdrawal.
The complete source facts and actual inputs/results remain in
`facts/complete-certificates-and-comparators.json.xz` and
`receipts/exact-certification.json.xz`.

T-127 records V3/C3 finite feasibility with independently re-implemented deciding code.
This relation concerns the source producer’s verification code; the two repository
routes share rational parsing, half-angle conversion, Fraction arithmetic and SAT
methodology. The
[mapped review](../../../../docs/project/reviews/review-2026-10-08-gupta-exact-refinements.md)
retains that scope.

A separate actual hosted private-worker transaction passed in 15.224 seconds with all
four ordinary scientific inputs, complete 17-source/51-job admission, all fourteen
houses, live input/result/source/comparator mutations and restorations, and producer
guards under the unchanged 45-second child deadline.
It forbids geometric deciders; custody admission is not a fresh replay or a source of
assurance by itself.

Fourteen exact finite upper bounds are selected.
The three withdrawn certificates remain fully verified and retained without
selected-bound credit.
No optimizer, lower-bound theorem, local minimum, rigidity, novelty, priority, global
optimum, formal proof or human oversight is established.

## Compressed Files

| Stored path | Origin | Git blob of original bytes | SHA-256 of original bytes |
| --- | --- | --- | --- |
| `source/LICENSES/Evan-Daniel-MIT.txt.gz` | upstream | `52cf89d2125f517a425c9a57c998dd85d83d7741` | `c51886c0f7e6724a7d89fc22cb237a1688ba1bbff04cb21a13b8e1a01fb15578` |
| `source/SHA256SUMS.gz` | upstream | `3f9654e033af35217999b4faa6ca6e93b975ee94` | `c05eff3a1a363c5b557fa082f0c83f492ed729ed185ace5fee877af98b8576c5` |
| `source/audit/frontier-correction.json.gz` | upstream | `9b7c3b39adf4ee06882aef042838f3f78652cc80` | `0060f9d677b0ffc29b69c16a38c6ec88031394888bcfda626767ee40aaa49b30` |
| `source/audit/public-comparisons.json.gz` | upstream | `ae5bb95aed3ec7e9cff4c196138057e80d8d6a07` | `23882fa925cb0b4acf9f803035f64ecbfc7444604487cbda758f6cbe807505d5` |
| `source/comparators/public-088.cert.json.gz` | upstream | `3c73026225e3f3775e6b0fb7f759c6f30f7e03dd` | `84bd5ce83eda8147734491f7dfb12891f71b83d1afe0bd22b248c2b0db3a6624` |
| `source/comparators/public-108.cert.json.gz` | upstream | `8e7f98c5648aa51dd22480686d637fb12b0476a1` | `852f580f762df5845bc46cd6c41c02010dbbf3616d090175d7dbe12eeedc98df` |
| `source/comparators/public-123.cert.json.gz` | upstream | `82af1e80c8d3860a8223fd972eaddc4ab33a8daa` | `30f740f1fda4ab5f19ff3a9cf45b3643b7befad83d9a1b48ddf3c9ca2e04f290` |
| `source/comparators/public-129.cert.json.gz` | upstream | `5265a42346861f26926271c1eef50f251f37c562` | `67ed26af2ffdfa506465ec32f1045b663765283f9b842e29bc154a627ca73271` |
| `source/comparators/public-130.cert.json.gz` | upstream | `974bf2204b2c28695c8d2b001b5121b507ada97c` | `080129fca3dadcb2c6a924b6e629e54d5405988a349008776c5e1a642ef116dc` |
| `source/comparators/public-153.cert.json.gz` | upstream | `8dbdbbdf9f832fffab3c0b2b90375ce5acb3bd66` | `4035079327be66751ccf03a69b27be2a5c267624cbd5a005da9aba7209eb87a9` |
| `source/comparators/public-154.cert.json.gz` | upstream | `de8c647bbbb5f26d7e1de1946a62b9594ff486cf` | `7ff2bf1a133130ef2149fa827bcb49f92fcf2d9591fb9cb3798f0b6bcaa16850` |
| `source/comparators/public-179.cert.json.gz` | upstream | `a401b424eb064ed2c6e4ce4f706b72c98c5c8626` | `a019651e811dca7b2423c58f97cb977a822b980631797820ef0962f352f380c3` |
| `source/comparators/public-180.cert.json.gz` | upstream | `7c6720b6c0636badbeb9ff549431ebaa75164cbb` | `4a182ac6aa4d96f26e6aff68400bc74b5c89a25c7abeb9f35a4b47b64a0d5219` |
| `source/comparators/public-199.cert.json.gz` | upstream | `a4bca57d8aae27897566c57b8073c0d850471430` | `e50cf3c3b4bb618766d1979ff845d5d1396267dd6ed4ba8be600e6da2116fd77` |
| `source/comparators/public-207.cert.json.gz` | upstream | `df1ffe4dc6bc393acc3a4d0afebe2b8b964f16f5` | `f1ea9c5eacdf45f8ed15b665618e066a1218632a367d7636e1fac411b3b94c1d` |
| `source/comparators/public-208.cert.json.gz` | upstream | `d8bbfeb2f508948946bc11410eb189243639e499` | `0b55cb8128a0d3cee8ce5cea158255afc40d978348d2699aea5c74db9190c3eb` |
| `source/comparators/public-209.cert.json.gz` | upstream | `09b0ce77ca910278b2175a25838520bf3d0354c2` | `13937d0ca56b0dae8da4d3c9471e1d9581f9239aa6d30d54071f7bd1f05aaef4` |
| `source/comparators/public-236.cert.json.gz` | upstream | `ee203137d079424269514aeb69ec2d470c937f50` | `402033174ffb3f0338ec15414d49e89ed3781682cc4e49b89a3e7c735e9ac4fe` |
| `source/comparators/public-237.cert.json.gz` | upstream | `781abcb3c217308da44d6908161e014ba7ec51d4` | `4585209b3e5508c5d571b654762e5ee5ba3aced6cbd63c0b697e673307f76f80` |
| `source/comparators/public-238.cert.json.gz` | upstream | `498aa80f74a187be48a1fd6fda570f61198b958d` | `98ecd8b20aab71122dc731fb4186d093bc50f9585c9e7491c4addbf622f58592` |
| `source/comparators/public-239.cert.json.gz` | upstream | `b4c20a340a70b3e3b575ebf00ed3e66337736719` | `08b6d49934f26df517343a085d0441c10ff9a97664d7c2dfa776e89c6ff970a7` |
| `source/findings.json.gz` | upstream | `3a200e2f98e276b02e777f6821464addd8d75ed5` | `b8797fa6fcde3e7f6632d48e6defe638e173e2111474890cbc802be4d9aa2bd6` |
| `source/integrity.json.gz` | upstream | `882b39418e41ca0f5f52a6145543f33fe72a1707` | `18f8128e641adc9317968dfa376a380a1f19ce6ea2f2ab27c31719624ff9a07f` |
| `source/negative-controls.txt.gz` | upstream | `5af4f17897e7f41bbd0cdb86f276fb553659d6b1` | `6c7ca28780aa22676f0adfe23b5c01b2b92f041447736a3c03c77c5c18ddc106` |
| `source/superseded/packing-108.cert.gz` | upstream | `2fe2ef4017cdeb60a0174c4488871a1e24bbe7fe` | `f018a35dba5da844822f6568bfcce4c862f2c5dcb516439118445c363bfd4b7b` |
| `source/superseded/packing-123.cert.gz` | upstream | `ac84fe68f700e19fc84c3a2cd5ee96dd85432f42` | `d27b37590d512533b7b00bf14df220fc29d0b4fbf3d16b096d57bc116e8fcea5` |
| `source/superseded/packing-129.cert.gz` | upstream | `6daaacf58bf6095f9ba5c9bf5bc87e7b1f77bb72` | `e5854cdcbf71d1388a52e7b9dad437660af0c349b6b548de72f069a6388c8df8` |
| `source/verification-results.txt.gz` | upstream | `0fefecae6b97007e866b0dc23eca6990e0fe967c` | `3bc774cc77ec91563f02ddfabf2b884f46e4e6e022c8b7ad8581ef658421fd54` |
| `source/witnesses/packing-088.cert.gz` | upstream | `fefca0b28682e26d2e1464c6fe1624268992a98f` | `4f20bc1a279cfa33266730b578ad4482c047064fc6b46f5128e24f5cb8f8d985` |
| `source/witnesses/packing-130.cert.gz` | upstream | `104e8fdff9cc4ad81ea3540c744f93f44bc4dc59` | `f979cb02bcaf78926d805d4819464dd9d363e148750a3d36bc03585f97ceb588` |
| `source/witnesses/packing-153.cert.gz` | upstream | `d336e60f32287ee0c5e4e004c255ae45d4a46038` | `9e13f02f78be58144ac82ff2419a78475ddd4303fb39023e38fe5f9c084fa1ab` |
| `source/witnesses/packing-154.cert.gz` | upstream | `14570645b69f45c79a121ee9525682dc79a16ae5` | `5df6e4b04ae1fc335fd9340bca0a7ba0376432dc7e74a4f88622123dc63ea5b7` |
| `source/witnesses/packing-179.cert.gz` | upstream | `b1d3fe5901dcda3adfa470d01603e81f9ceb6602` | `f3aa4fd8324f1ba83af92efd461640e84cc6ad709c1b8cb52972a8f6495ff4d0` |
| `source/witnesses/packing-180.cert.gz` | upstream | `f244aba89864b4b7da581d426d04718e0e5e4d37` | `118b7ac88f32af6b71825ae0caaf83d06d51d791791368599be4be3206cb4c84` |
| `source/witnesses/packing-199.cert.gz` | upstream | `d0c5f879f5b3d6d73a8cddc833f09972a38d286d` | `55182c4a4b7d1074622b97e8d39f0c42897b1ed7850cc67655956f39addc5fe0` |
| `source/witnesses/packing-207.cert.gz` | upstream | `316158175898e398c49af626aab401dc3c8069a5` | `6a1d668de181f9db6b91f524c78e037f460619af2285ef48da4ea3a22ecc4a37` |
| `source/witnesses/packing-208.cert.gz` | upstream | `5ef4cd488cac5c8e21dcf70d38111f001f5c55b3` | `03ae70a134e26bb10b9bcc89bdecb9a9ecf02776e8239ccc381e447c450da045` |
| `source/witnesses/packing-209.cert.gz` | upstream | `51b12e8c7bc865f7ad4618d1dc0511d787a79fed` | `3c06bdb435980286fa0dbfc4d2ef6a93e7aba05ec6d4a0410d45c300cf85fc45` |
| `source/witnesses/packing-236.cert.gz` | upstream | `84c1fd3e482f420dedb0631fbc425ca19d71b86e` | `e2dbadfb6ddb041617ea14cea79567d4336c4022a4366d70843f75bb52d469bf` |
| `source/witnesses/packing-237.cert.gz` | upstream | `670e6c9b17fda7d0f2fb3b63d40bfa5d56242d3f` | `28e230df1809af101fecbc5a75dc3588bad5ea7805e86794596193f28c3752eb` |
| `source/witnesses/packing-238.cert.gz` | upstream | `a953dc863ba0a1f9e968851f9ff31bc7b64f7649` | `434d3c830148d1842c2f249cbb24ed0684db7b5231aee9b9af6313593f1b03e5` |
| `source/witnesses/packing-239.cert.gz` | upstream | `5ba15244c371aa24483327e799d7f22ac3f04040` | `a94462e07bd39fe9b2b5e869ee3ff70c013d95cb1c158dde50f40554b143096a` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
