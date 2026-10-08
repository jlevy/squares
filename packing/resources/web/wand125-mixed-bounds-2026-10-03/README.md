# wand125 Mixed-Rectangle Certificates of 3 October 2026, Pinned at `2aff207`

This packet pins the 22 certificate directories that
[wand125/square-packing-bounds](https://github.com/wand125/square-packing-bounds) added on
3 October 2026 (UTC), from `mixed_n95_L996` to `mixed_n69_L8612`, at the commit that
added the last of them. Each was posted in its own comment on
[jlevy/squares#282](https://github.com/jlevy/squares/issues/282). They are rectangle-density
lower bounds of the kind and checker of the six in the
[afternoon packet of 2 October](../wand125-mixed-bounds-afternoon-2026-10-02/README.md)
and the earlier mixed packets, at $n = 51$, 52, 55, 58, 69 to 71, 73 to 76 and 86 to 96.
Its proposed Frontier key is **[wand125 mixed bounds 2026-10-03]**.
The claims below are stated as the source states them.

Six of the 22 are at counts where an earlier mixed certificate of this source is
retained, and each states a larger side: `mixed_n76_L896` over `mixed_n76_L894`,
`mixed_n87_L955` over `mixed_n87_L948`, `mixed_n90_L9725` over `mixed_n90_L960`,
`mixed_n91_L975` over `mixed_n91_L970`, `mixed_n92_L977` over `mixed_n92_L975` and
`mixed_n96_L997` over `mixed_n96_L996`. The source names the first four and the last two
as superseded in its commit messages or READMEs. The other sixteen are the source's first
mixed certificates at their counts.

What was checked here is SHA-256 digests, Git blob ids, the exact premises the audit below
recomputes from the retained bytes, and every check the replay makes before its first
angle, run on each pinned tarball. On 6 October 2026 `sqverify-fast`, this repository’s
clean-room measure verifier, decided the 22 retained candidates at all 201 net directions
([the independent replays](#the-independent-replays)); the source’s own checker has not
been run here on any of the 22.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/wand125/square-packing-bounds> |
| Revision | `2aff2076c492d62340e986c84f60a0a29eb668df`, branch `main`, tree `790200d80683d6fa96eedb186fcacdaa7a6a9267`; the head when retrieved, and the revision the last request names |
| Committed | Authored and committed 2026-10-03T17:58:33Z, 02:58 on 4 October by the author’s clock (`+09:00`) |
| Author | wand125, building on Tokoharu’s format and verifier, as for the other mixed certificates |
| Licence | MIT. The root `LICENSE` reads “Copyright (c) 2026 wand125” and is byte-identical to the [September 27 packet’s copy](../wand125-rectangle-certificates-2026-09-27/wand125-rectangles/LICENSE) |
| Retrieved | 2026-10-03, about 18:49Z: a blob-filtered clone of the whole history, checked out sparsely at this revision (the 22 claim directories and the three root files). `git ls-remote` listed one branch and no tag |
| Pinned subtree | 377 files, 391,933,371 bytes: the 22 claim directories and the three root files, each by SHA-256 in [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) |
| Retained here | 111 files, 4,301,995 bytes upstream, under [`square-packing-bounds/`](square-packing-bounds/), byte-identical to the pinned files after decompression |

**The revisions.** The source’s `main` moved from `b00fc70f`, the afternoon packet’s pin,
through 22 commits on 3 October, each of which adds one certificate directory and changes
the root README, and nothing else. Each directory here has exactly one commit, with equal
author and committer dates, and is unchanged at the pin:

| Claim | Directory | Commit | Committed (UTC) | Request |
| --- | --- | --- | --- | --- |
| $s(51) \ge 373/50$ | `certificates/mixed_n51_L746` | `06a1e9d636e8fa2c5e990b6bc1b02ab790fa8288` | 2026-10-03T07:48:12Z | [07:48:42Z](https://github.com/jlevy/squares/issues/282#issuecomment-5966907664) |
| $s(52) \ge 151/20$ | `certificates/mixed_n52_L755` | `3d365c4755ff2754289c99fe6087329362ea60b2` | 2026-10-03T06:30:51Z | [06:31:38Z](https://github.com/jlevy/squares/issues/282#issuecomment-5966383825) |
| $s(55) \ge 966/125$ | `certificates/mixed_n55_L7728` | `2d22930c5fe0b6022f0435a77a0a3e86ca804dce` | 2026-10-03T10:37:10Z | [10:37:20Z](https://github.com/jlevy/squares/issues/282#issuecomment-5968358529) |
| $s(58) \ge 1581/200$ | `certificates/mixed_n58_L7905` | `7bcfef5e029f9bc6a0b0dd800467e35beb0e9c45` | 2026-10-03T08:26:30Z | [08:26:49Z](https://github.com/jlevy/squares/issues/282#issuecomment-5967170488) |
| $s(69) \ge 2153/250$ | `certificates/mixed_n69_L8612` | `2aff2076c492d62340e986c84f60a0a29eb668df` | 2026-10-03T17:58:33Z | [17:58:45Z](https://github.com/jlevy/squares/issues/282#issuecomment-5971914803) |
| $s(70) \ge 3459/400$ | `certificates/mixed_n70_L86475` | `13188dd16e73898819926271849511d72f46ee4b` | 2026-10-03T16:17:10Z | [16:17:23Z](https://github.com/jlevy/squares/issues/282#issuecomment-5970989651) |
| $s(71) \ge 1741/200$ | `certificates/mixed_n71_L8705` | `044c12719e459efc1df3e3ae5ced4781cdbbd796` | 2026-10-03T16:14:04Z | [16:14:14Z](https://github.com/jlevy/squares/issues/282#issuecomment-5970961348) |
| $s(73) \ge 8809/1000$ | `certificates/mixed_n73_L8809` | `b780f588d238c7b72c77ecfed1adc31762adc878` | 2026-10-03T16:30:42Z | [16:30:53Z](https://github.com/jlevy/squares/issues/282#issuecomment-5971102614) |
| $s(74) \ge 3547/400$ | `certificates/mixed_n74_L88675` | `ce65306381630fb1ef1fed7bcf27a0bf60172243` | 2026-10-03T15:58:27Z | [15:58:38Z](https://github.com/jlevy/squares/issues/282#issuecomment-5970827530) |
| $s(75) \ge 223/25$ | `certificates/mixed_n75_L892` | `216e4b4a5b75c8bc3bb619295b3cd273015aa992` | 2026-10-03T06:44:51Z | [06:45:24Z](https://github.com/jlevy/squares/issues/282#issuecomment-5966471175) |
| $s(76) \ge 224/25$ | `certificates/mixed_n76_L896` | `3d2089e8633aafad5ab490ab1b710d10232e4b5d` | 2026-10-03T12:59:30Z | [12:59:37Z](https://github.com/jlevy/squares/issues/282#issuecomment-5969402336) |
| $s(86) \ge 19/2$ | `certificates/mixed_n86_L950` | `bbb78b2e4c448849212fd7a8ff43342d4d8809ba` | 2026-10-03T04:27:40Z | [04:28:13Z](https://github.com/jlevy/squares/issues/282#issuecomment-5965525458) |
| $s(87) \ge 191/20$ | `certificates/mixed_n87_L955` | `239e95fe13760a19388a695d0231fdcb1f0ad4c1` | 2026-10-03T04:40:33Z | [04:41:00Z](https://github.com/jlevy/squares/issues/282#issuecomment-5965608183) |
| $s(88) \ge 48/5$ | `certificates/mixed_n88_L960` | `bf23abf3fe3c7806b208a27a7632e169189d8f0d` | 2026-10-03T08:24:06Z | [08:24:23Z](https://github.com/jlevy/squares/issues/282#issuecomment-5967152250) |
| $s(89) \ge 193/20$ | `certificates/mixed_n89_L965` | `b1dc461d4d71bdb7481ac72e7bb594775f6b891a` | 2026-10-03T05:16:14Z | [05:16:40Z](https://github.com/jlevy/squares/issues/282#issuecomment-5965873364) |
| $s(90) \ge 389/40$ | `certificates/mixed_n90_L9725` | `4a4f2f816356d1ec454207c41abd727cc706effd` | 2026-10-03T10:48:48Z | [10:49:02Z](https://github.com/jlevy/squares/issues/282#issuecomment-5968439278) |
| $s(91) \ge 39/4$ | `certificates/mixed_n91_L975` | `ee10b727e6a72185578a0a341b81d5250f90a544` | 2026-10-03T08:59:53Z | [09:00:13Z](https://github.com/jlevy/squares/issues/282#issuecomment-5967446024) |
| $s(92) \ge 977/100$ | `certificates/mixed_n92_L977` | `5baaec2742de087c374a09a8f4e568bd021f0be9` | 2026-10-03T12:47:42Z | [12:47:51Z](https://github.com/jlevy/squares/issues/282#issuecomment-5969312608) |
| $s(93) \ge 493/50$ | `certificates/mixed_n93_L986` | `e11387ec374c9424826db20e4dd9e81f58b2dde3` | 2026-10-03T05:03:43Z | [05:04:07Z](https://github.com/jlevy/squares/issues/282#issuecomment-5965785579) |
| $s(94) \ge 248/25$ | `certificates/mixed_n94_L992` | `caabf77f0fb9a3e2b9cade8ee3c6e6686feb6986` | 2026-10-03T03:13:50Z | [03:14:16Z](https://github.com/jlevy/squares/issues/282#issuecomment-5964970265) |
| $s(95) \ge 249/25$ | `certificates/mixed_n95_L996` | `99332265f54fb5aa78916f1eb2a3680790024423` | 2026-10-03T02:49:42Z | [02:50:10Z](https://github.com/jlevy/squares/issues/282#issuecomment-5964806255) |
| $s(96) \ge 997/100$ | `certificates/mixed_n96_L997` | `1695131cbee0b73b3677db9347aed06b45518c48` | 2026-10-03T17:24:51Z | [17:25:01Z](https://github.com/jlevy/squares/issues/282#issuecomment-5971628643) |

## Credit and AI Assistance, as the Source States Them

The root README at the pin is retained. Its Attribution section opens “The method is not
ours.” and credits Walter Stromquist, Hiroshi Nagamochi, Sam Burns, Gustavo Massaccesi
and this repository, and its Status section says “Parts of this work were produced with
AI assistance under human direction.”, as at the afternoon packet’s pin.

- **The 22 certificates.** Each directory README calls the checker “the verifier shipped
  here, `code/mixed_rotated_verify.cpp`”, the same checker as for `mixed_n87_L939` and
  `mixed_n65_L835`, and says the certificate is not in Tokoharu’s format because its least
  oblique bound is below the $1.0001$ his `verify.cpp` requires. Each says the candidate
  was built from scratch at its side from a structured initial measure (“bands at integer
  distances from the walls, as in the Green-series certificates”) and repaired against
  counterexamples on the full net; the `route` of each `completion-audit.json` says the
  same.
- **The pre-publication replays.** Each README says the full 201-angle replay was run
  again from the tarball on a fresh Ubuntu 24.04 machine with only the README’s
  requirements installed. This was not checked.
- **The commits.** Each of the 22 commit messages ends with a co-author trailer naming an
  AI assistant.

## What Is Retained

Retained byte-identical at their upstream paths: the root `README.md`, and from each of
the 22 directories `README.md`, `candidate.json`, `certificate.json`,
`completion-audit.json` and `manifest.json`.

Pinned by digest only:

| Upstream path | Bytes | SHA-256 |
| --- | ---: | --- |
| `LICENSE` | 1,064 | `c0dd43e7892932c81335f74a2fdbf1a98f5977bab14c0c4c30e3abcc97c34904` |
| `.gitignore` | 132 | `0a31c24fe622ff8b4b012fbf790686063a84da3dd306d47e7283aad434653308` |
| `certificates/mixed_n51_L746/n51-L7.46-proof-bundle.tar.gz` | 17,762,923 | `0729dce38e99f6a82d43ead611f5a8dda66708a1ec10066e38b0264b620deade` |
| `certificates/mixed_n52_L755/n52-L7.55-proof-bundle.tar.gz` | 18,083,771 | `f9f12c579f2dfd2236e7f2c99a38965f1349439fbd9f321a3c101749e6e329bb` |
| `certificates/mixed_n55_L7728/n55-L7.728-proof-bundle.tar.gz` | 11,738,199 | `cf91a3fee5311a9da61cd918ae2c2fd7eef29059a97ee2002ef5a4d3ede8bef9` |
| `certificates/mixed_n58_L7905/n58-L7.905-proof-bundle.tar.gz` | 12,665,333 | `d11b4d3fd9e37d535a6d8dced02a036748f94684ee6cc676ddbff847b73d5abe` |
| `certificates/mixed_n69_L8612/n69-L8.612-proof-bundle.tar.gz` | 23,034,012 | `0468c96aaf8ca3e75dfa85ade7961f44a451ed4e6b1f736d5cfa202ca5b4c155` |
| `certificates/mixed_n70_L86475/n70-L8.6475-proof-bundle.tar.gz` | 20,534,888 | `fa020a0c5fff5422c6e01bfe0a78c7f1689076736b2cc1d959cd16ee49d06bbf` |
| `certificates/mixed_n71_L8705/n71-L8.705-proof-bundle.tar.gz` | 19,541,252 | `a94ffa642007d4e1b4cf5f1ce827b93f12d99750001549efc13f7bc40825706e` |
| `certificates/mixed_n73_L8809/n73-L8.809-proof-bundle.tar.gz` | 18,622,834 | `17668509e00d1509a431ba40fd563c9c01fbf6e30c91ed9dbd60fccfc040c205` |
| `certificates/mixed_n74_L88675/n74-L8.8675-proof-bundle.tar.gz` | 21,560,855 | `edc1ff8481a2d9a0f8b51aa5070766f6c556466f89331536c6f0c8b170221903` |
| `certificates/mixed_n75_L892/n75-L8.92-proof-bundle.tar.gz` | 13,193,154 | `75330dd35018a18faa13375712a1b983b0282d0ae9e5b80413398790811fd06a` |
| `certificates/mixed_n76_L896/n76-L8.96-proof-bundle.tar.gz` | 13,101,923 | `85cc7e1e5f6a2ea89d3e294adbd765dcd3187a31adae4cec82ce2020a80192c7` |
| `certificates/mixed_n86_L950/n86-L9.50-proof-bundle.tar.gz` | 20,392,942 | `1f72d911584f7e57b866e74740ef5d533b2b2774338f997fe553817e8fd20ad8` |
| `certificates/mixed_n87_L955/n87-L9.55-proof-bundle.tar.gz` | 20,745,923 | `f8f4a19d25ecbe06df49fc2cd4244f3d9a17a2e97abe56467c70f8e76925f771` |
| `certificates/mixed_n88_L960/n88-L9.60-proof-bundle.tar.gz` | 17,386,081 | `7e4305f16e3eac95ad72025870f513c16e71c2ac6d239d1beccfb763d3200f10` |
| `certificates/mixed_n89_L965/n89-L9.65-proof-bundle.tar.gz` | 16,339,426 | `75e1549d5633ecd29025f7fe53c44c2af1570dcdab57f0918467d3ca828598ee` |
| `certificates/mixed_n90_L9725/n90-L9.725-proof-bundle.tar.gz` | 23,740,402 | `1744a7d62585b31ddeda36bd76a00c21eee21b8232a15a7b105d0d4d7e48cb58` |
| `certificates/mixed_n91_L975/n91-L9.75-proof-bundle.tar.gz` | 18,509,656 | `fa6f3a9cb2f6205cf3186b6d661d4826d261d426cc622fcbd6e08892312b467d` |
| `certificates/mixed_n92_L977/n92-L9.77-proof-bundle.tar.gz` | 13,136,629 | `6e7bbb35ee8fff68308f5da171f0a3ee55c19ebfbd013d962082c06065a1dfed` |
| `certificates/mixed_n93_L986/n93-L9.86-proof-bundle.tar.gz` | 18,020,286 | `10e608e2703da81ed008866dab811aa2c4f04c860acd9c01f5a4eb8b52c780ff` |
| `certificates/mixed_n94_L992/n94-L9.92-proof-bundle.tar.gz` | 19,188,976 | `b866b117904cf01f2c50cc8d9b988c103cb54145bcce5249719acb7ce879f45f` |
| `certificates/mixed_n95_L996/n95-L9.96-proof-bundle.tar.gz` | 16,003,775 | `1f7b67cdcff13efaec9b2d1391bed3134f434183874ad44de1150084e4c683f6` |
| `certificates/mixed_n96_L997/n96-L9.97-proof-bundle.tar.gz` | 13,477,300 | `486bad8c9932a53ccdb16b39f627801c5871692b201f729ee23046f022b53303` |

`LICENSE` is retained byte-identical by the September 27 rectangle packet; a retained
`.gitignore` would act on this repository’s tree. Each tarball is a complete proof bundle.
Each directory’s ten `code/` files and its `requirements.txt` are byte-identical to the
files of the same name in `mixed_n50_L740/`, which the
[September 28 packet](../wand125-point-and-mixed-2026-09-28/README.md) retains, and are
pinned by digest in the subtree list.

Each tarball digest is also the one its directory’s README and `completion-audit.json`
state, and each audit’s `certificate_sha256` is the digest of the retained
`certificate.json`.

[`acquisition/declaration.json`](acquisition/declaration.json) declares the scope and the
pinned-only rules, and [`acquisition/sources.json`](acquisition/sources.json) records the
pin and every pinned-only file with its size, digest, reason and, where one exists, the
retained copy with the same bytes.
From `packing/`,

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source \
  wand125-mixed-bounds-2026-10-03 --checkout CHECKOUT
```

rebuilds the retained files and both acquisition files from a checkout at the pinned
revision, and with `--check` in place of `--checkout CHECKOUT` re-derives the packet from
its manifest without one.

## The Claims, as the Source States Them

| Name here | Claim | Rectangles | Source’s comparison | Improvement stated | Least oblique bound recorded (index) | Axis cells, minimum |
| --- | --- | ---: | --- | --- | --- | --- |
| `n51` | $s(51) \ge 373/50$ | 446 | $2977/400$, “record n51 7.4425” | $7/400$ | $1.0000000003200482$ (107) | 9,048,064, $1.009964249145509$ |
| `n52` | $s(52) \ge 151/20$ | 455 | $1507/200$, “record n52 7.535” | $3/200$ | $1.0000000004141971$ (170) | 8,862,529, $1.0061071116246354$ |
| `n55` | $s(55) \ge 966/125$ | 303 | $617/80$, “record n55 7.7125” | $31/2000$ | $1.0000000014125006$ (114) | 3,837,681, $1.0076941602220786$ |
| `n58` | $s(58) \ge 1581/200$ | 319 | $789/100$, “record n58 7.89” | $3/200$ | $1.0000000036417236$ (109) | 4,239,481, $1.0070002486141336$ |
| `n69` | $s(69) \ge 2153/250$ | 556 | $1717/200$, “record n69 8.585” | $27/1000$ | $1.0000000003818312$ (180) | 12,482,089, $1.0028461704678193$ |
| `n70` | $s(70) \ge 3459/400$ | 495 | $8639/1000$, “our certified n70 8.639 (record 8.6275)” | $17/2000$ | $1.000000002986998$ (112) | 10,771,524, $1.0037504910100976$ |
| `n71` | $s(71) \ge 1741/200$ | 471 | $87/10$, “our certified n71 8.70 (record 8.685)” | $1/200$ | $1.0000000001991776$ (177) | 9,418,761, $1.007609519559992$ |
| `n73` | $s(73) \ge 8809/1000$ | 450 | $439/50$, “record n73 8.78” | $29/1000$ | $1.000000000044086$ (79) | 8,952,064, $1.0046099418362586$ |
| `n74` | $s(74) \ge 3547/400$ | 505 | $3539/400$, “record n74 8.8475” | $1/50$ | $1.000000001545537$ (17) | 11,553,201, $1.0053919510575358$ |
| `n75` | $s(75) \ge 223/25$ | 340 | $89/10$, “record n75 8.9” | $1/50$ | $1.000000006207448$ (177) | 4,206,601, $1.0042340709582527$ |
| `n76-L896` | $s(76) \ge 224/25$ | 341 | $447/50$, “our published n76 8.94” | $1/50$ | $1.0000000015320276$ (7) | 3,783,025, $1.0052760168457555$ |
| `n86` | $s(86) \ge 19/2$ | 509 | $473/50$, “record n86 9.46 (via n85 9.46 monotonicity)” | $1/25$ | $1.0000000001438667$ (171) | 10,562,500, $1.0061406086120193$ |
| `n87-L955` | $s(87) \ge 191/20$ | 509 | $237/25$, “our certified n87 9.48 (record 9.46 via n85 monotonicity)” | $7/100$ | $1.0000000015515935$ (13) | 10,426,441, $1.0011071121810646$ |
| `n88` | $s(88) \ge 48/5$ | 443 | $3791/400$, “record n88 9.4775” | $49/400$ | $1.0000000014645312$ (185) | 7,096,896, $1.0065197740201668$ |
| `n89` | $s(89) \ge 193/20$ | 416 | $48/5$, “our certified n89 9.60 (record 9.565)” | $1/20$ | $1.0000000007032546$ (186) | 6,507,601, $1.003735180782793$ |
| `n90-L9725` | $s(90) \ge 389/40$ | 571 | $97/10$, “our certified n90 9.70 (record 9.60)” | $1/40$ | $1.0000000003009648$ (194) | 13,271,449, $1.003701651702754$ |
| `n91-L975` | $s(91) \ge 39/4$ | 457 | $97/10$, “our certified n91 9.70 (record 9.645)” | $1/20$ | $1.0000000008354386$ (119) | 8,450,649, $1.0042708355544132$ |
| `n92-L977` | $s(92) \ge 977/100$ | 345 | $39/4$, “our certified n92 9.75” | $1/50$ | $1.0000000055876297$ (156) | 4,347,225, $1.002664031677061$ |
| `n93` | $s(93) \ge 493/50$ | 443 | $973/100$, “record n93 9.73” | $13/100$ | $1.0000000019291797$ (183) | 8,139,609, $1.0051573923000485$ |
| `n94` | $s(94) \ge 248/25$ | 488 | $247/25$, “our certified n94 9.88 (record 9.805)” | $1/25$ | $1.0000000002005007$ (191) | 8,300,161, $1.0052232564352899$ |
| `n95` | $s(95) \ge 249/25$ | 438 | $248/25$, “our certified n95 9.92 (record 9.8518)” | $1/25$ | $1.0000000006841734$ (186) | 5,175,625, $1.005856765307342$ |
| `n96-L997` | $s(96) \ge 997/100$ | 376 | $249/25$, “our published n96 9.96” | $1/100$ | $1.0000000012288544$ (157) | 3,489,424, $1.0085332557761764$ |

All 22 are rectangle densities with no point mass (each `candidate.json` has an empty
`points` list and a `scaling_factor` of `1`), of total mass $n - 1/100000$, with core side
$B = 9977/10000$, 201 net half-angles of step $83/40000$ and coverage threshold $1$, as for
every earlier mixed certificate. Each `certificate.json` has status
`ALL_ANGLES_VERIFIED_AND_REPLAYED`. Every comparison is with an exact rational, the
source’s own earlier value at that count; none is with a rounded Green value.

## The Exact Audit and the Pre-Replay Checks

From `packing/`,

```sh
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_point_and_mixed \
  mixed-audit wand125-mixed-bounds-2026-10-03 --check
```

recomputes [`receipts/mixed-audit.json`](receipts/mixed-audit.json) from the retained
bytes and imports no source code, with the checks the afternoon packet describes: pinned
digests; the count, side, core and rectangle count stated; nonnegative masses inside the
container, of total exactly $n - 1/100000$; the candidate digest by the source’s rule,
equal in the manifest, the certificate, the source’s audit and the statement; the net
record equal to the containment facts recomputed here; the checker `89b674a6…` and
`code/` the retained $n = 50$ copy; a replay record at threshold $1$ for each of the 201
angles; the source audit’s certificate and tarball digests; and its improvement equal to
the side less its comparison value. All 22 pass. Each side exceeds Green’s DS7 value at
its count, enclosed to 60 digits, and Nagamochi’s $1 + \sqrt{n - 2\lfloor\sqrt n\rfloor + 1}$,
and the centre domains are recomputed at the oblique nodes. None of it decides
coverage.

On 3 October `mixed-fetch` was run on each pinned tarball, read from the sparse checkout
at the pinned commit. Each has the pinned SHA-256 and size; each unpacked bundle matches
all 621 entries of its `files-sha256.json` with nothing unlisted, and its candidate,
certificate, manifest and `code/` are the retained or `mixed_n50_L740` files; the shipped
driver’s preconditions hold on its own code; every one of the 200 oblique inputs encloses
the exact candidate recomputed here; and every record is `ANGLE_VERIFIED` with an empty
frontier at $\gamma = 1$. Each run’s output is its certificate’s `receipts/NAME/fetch.json`;
the `bundle` field names the scratch directory it was unpacked in.

| Name here | Rectangle images checked | Oblique nodes | Source’s oblique seconds | Source’s CPU-hours | `mixed-price` CPU-hours | Planned CPU-hours |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `n51` | 3,568 | 69,985,426 | 28,158 | 7.82 | 5.6 | 6.3 |
| `n52` | 3,640 | 74,571,040 | 30,137 | 8.37 | 6.1 | 6.9 |
| `n55` | 2,424 | 77,422,814 | 26,356 | 7.32 | 4.2 | 4.8 |
| `n58` | 2,552 | 36,266,794 | 11,702 | 3.25 | 2.1 | 2.3 |
| `n69` | 4,448 | 99,544,986 | 39,356 | 10.93 | 10.1 | 11.2 |
| `n70` | 3,960 | 100,441,798 | 36,800 | 10.22 | 9.0 | 10.0 |
| `n71` | 3,768 | 100,569,226 | 39,188 | 10.89 | 8.5 | 9.6 |
| `n73` | 3,600 | 100,339,538 | 41,330 | 11.48 | 8.1 | 9.1 |
| `n74` | 4,040 | 90,044,046 | 39,422 | 10.95 | 8.1 | 9.1 |
| `n75` | 2,720 | 39,920,680 | 17,088 | 4.75 | 2.4 | 2.7 |
| `n76-L896` | 2,728 | 45,154,982 | 13,310 | 3.70 | 2.7 | 3.1 |
| `n86` | 4,072 | 94,779,600 | 32,931 | 9.15 | 8.7 | 9.7 |
| `n87-L955` | 4,072 | 86,412,558 | 28,647 | 7.96 | 7.9 | 8.9 |
| `n88` | 3,544 | 92,907,150 | 30,741 | 8.54 | 7.4 | 8.3 |
| `n89` | 3,328 | 109,970,334 | 34,933 | 9.70 | 8.2 | 9.2 |
| `n90-L9725` | 4,568 | 110,810,810 | 39,923 | 11.09 | 11.4 | 12.8 |
| `n91-L975` | 3,656 | 128,561,314 | 52,429 | 14.56 | 10.6 | 11.8 |
| `n92-L977` | 2,760 | 37,604,722 | 10,247 | 2.85 | 2.3 | 2.6 |
| `n93` | 3,544 | 94,366,242 | 29,356 | 8.15 | 7.5 | 8.4 |
| `n94` | 3,904 | 57,370,560 | 21,052 | 5.85 | 5.0 | 5.6 |
| `n95` | 3,504 | 53,447,460 | 17,347 | 4.82 | 4.1 | 4.6 |
| `n96-L997` | 3,008 | 72,598,690 | 24,930 | 6.93 | 4.8 | 5.4 |

The source’s seconds are the bundle’s own record of its oblique run, 179.3 CPU-hours in
all. `mixed-price` scales the rate of the three angles timed on 2 October by each
certificate’s node counts and rectangles, 145.1 CPU-hours in all. The planned column is
that estimate times 1.119, the ratio of measured to estimated CPU-hours over the 14
complete replays already merged in this record (`observed_ratio`), 162.4 CPU-hours in all.
On a busier guest $n = 50$’s complete replay took twice its estimate, so budget wall time
toward the source’s figure.

## Replaying the Certificates

The source’s check is its driver `code/verify_mixed_full_proof.py`, run from the unpacked
tarball. `devtools.audit_wand125_point_and_mixed` runs the same check split by net angle,
as for the earlier mixed packets, and names the 22 as in the tables above: a count an
earlier certificate already names takes its side as well.

```sh
# from packing/: one command per range; 0 is the axis direction
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_point_and_mixed \
  mixed-replay n69 --range 0-139 --work /tmp/wand125-n69 --workers 4 --via git
# when every range of a certificate has run
uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_point_and_mixed \
  mixed-merge n69
```

Receipts go to `receipts/NAME/range-AAA-BBB/` as each angle finishes, and a rerun replays
only what has not passed.
`mixed-shard wand125-mixed-bounds-2026-10-03 --runners K` splits the whole packet across
K hosts of four workers: a certificate larger than a quarter of a runner’s share is cut
into ranges of equal estimated cost, and the pieces go, largest first, to the least
loaded runner. For eight 4-core runners it gives:

| Runner | Planned CPU-hours | Wall hours at 4 workers | Ranges, run in this order |
| --- | ---: | ---: | --- |
| r1 | 21.7 | 5.4 | `n52` 0–200, `n75` 0–200, `n76-L896` 0–200, `n87-L955` 136–200, `n95` 0–200 |
| r2 | 19.6 | 4.9 | `n51` 0–200, `n71` 0–135, `n87-L955` 0–135, `n88` 138–200 |
| r3 | 19.4 | 4.8 | `n55` 0–200, `n74` 132–200, `n91-L975` 134–200, `n93` 0–132 |
| r4 | 19.4 | 4.8 | `n71` 136–200, `n73` 0–133, `n88` 0–137, `n91-L975` 0–133 |
| r5 | 19.4 | 4.8 | `n69` 140–200, `n86` 0–134, `n89` 0–135, `n90-L9725` 0–105 |
| r6 | 21.7 | 5.4 | `n58` 0–200, `n69` 0–139, `n74` 0–131, `n86` 135–200, `n90-L9725` 160–200 |
| r7 | 19.4 | 4.8 | `n70` 137–200, `n73` 134–200, `n90-L9725` 106–159, `n94` 0–200 |
| r8 | 21.9 | 5.5 | `n70` 0–136, `n89` 136–200, `n92-L977` 0–200, `n93` 133–200, `n96-L997` 0–200 |

Each runner runs its `mixed-replay` commands one after another, then commits and pushes
its receipts; `mixed-merge NAME` is run for each certificate once every range of it has
arrived. No replay of the source’s checker has been launched.

## The Independent Replays

On 6 October 2026 `devtools.sqverify_fast_census --family mixed` ran `sqverify-fast` on
each retained `candidate.json.gz` at all 201 net directions, at the threshold the
certificate declares, and then ran its two mutants scaled below coverage one at the
least-bound direction.
All 22 are `VERIFIED`, and the control refused both mutants of each; the receipts are in
[`benchmarks/measure-verifier/census-mixed/`](../../../benchmarks/measure-verifier/census-mixed/README.md),
and each certificate’s evidence entry `E-…-sqverify-fast-replay` states its run.
At `mixed_n96_L997` the first control failed closed: the mutant scaled to $99/100$
verified too, at the one direction that control runs it, the certificate having more
than 1% to spare there (think-0uia). Its receipt is kept as
`mixed_n96_L997.control-failed-v1.json`. The repaired control runs that mutant at every
net direction and refused it at 187 of the 201, each at a centre in the per-bin
domain whose exact capture is below 1; its receipt, `mixed_n96_L997.control.json`, is
the census’s first of kind `sqverify-fast-control/v2`.
The build is main’s crate source `d97758bb…`, which the
[soundness review of 6 October](../../../../docs/project/reviews/review-2026-10-06-sqverify-fast-declared-net-soundness.md)
accepted for standard-net certificates; all 22 are on the standard net.

| Certificate | Nodes | Least certified bound (index) | CPU seconds | Threads |
| --- | ---: | --- | ---: | ---: |
| `mixed_n51_L746` | 68,387,056 | $1.000000000282108$ (124) | 940 | 2 |
| `mixed_n52_L755` | 72,804,986 | $1.0000000001604281$ (126) | 1,108 | 2 |
| `mixed_n55_L7728` | 64,084,694 | $1.0000000008205456$ (106) | 1,023 | 2 |
| `mixed_n58_L7905` | 32,915,022 | $1.0000000004229204$ (86) | 556 | 2 |
| `mixed_n69_L8612` | 87,975,724 | $1.0000000004388068$ (142) | 1,859 | 2 |
| `mixed_n70_L86475` | 87,628,026 | $1.0000000002290894$ (170) | 1,754 | 2 |
| `mixed_n71_L8705` | 81,498,764 | $1.0000000006115706$ (172) | 1,678 | 2 |
| `mixed_n73_L8809` | 76,715,880 | $1.0000000002704519$ (188) | 1,820 | 2 |
| `mixed_n74_L88675` | 76,705,524 | $1.0000000001923686$ (161) | 1,741 | 2 |
| `mixed_n75_L892` | 34,025,184 | $1.0000000001483238$ (94) | 716 | 2 |
| `mixed_n76_L896` | 37,661,682 | $1.0000000001194138$ (177) | 700 | 2 |
| `mixed_n86_L950` | 79,636,976 | $1.0000000005619347$ (188) | 1,366 | 2 |
| `mixed_n87_L955` | 74,542,782 | $1.000000000093562$ (34) | 1,395 | 2 |
| `mixed_n88_L960` | 70,872,248 | $1.00000000024589$ (189) | 1,342 | 2 |
| `mixed_n89_L965` | 85,890,638 | $1.0000000003462486$ (135) | 1,533 | 2 |
| `mixed_n90_L9725` | 91,021,318 | $1.0000000001882379$ (199) | 2,001 | 2 |
| `mixed_n91_L975` | 92,358,716 | $1.0000000001703604$ (171) | 2,069 | 2 |
| `mixed_n92_L977` | 29,174,516 | $1.0000000019666107$ (101) | 551 | 2 |
| `mixed_n93_L986` | 75,386,950 | $1.0000000005644345$ (119) | 1,609 | 2 |
| `mixed_n94_L992` | 47,197,040 | $1.0000000001531857$ (101) | 1,056 | 2 |
| `mixed_n95_L996` | 45,979,446 | $1.0000000007947085$ (166) | 907 | 2 |
| `mixed_n96_L997` | 59,643,606 | $1.0000000000057894$ (139) | 979 | 2 |

They took 8.0 CPU-hours in all, at two threads on a shared four-core host. The
verifier was written without opening the source’s checker and shares no code with it,
so these are independent decisions of coverage by the same method, not reproductions of
the source’s records. The source’s checker remains unreplayed here; the range commands
above would add that reproduction.

## Where the Requests and the Retained Files Differ

- **Comparison values no published certificate holds.** Six `compared_note` fields name
  the source’s own “certified” value at a count for which no directory at the pin holds a
  certificate: 8.639 at $n = 70$, 8.70 at 71, 9.60 at 89, 9.70 at 90, 9.88 at 94 and 9.92
  at 95. (The “certified” 9.48 at 87, 9.70 at 91 and 9.75 at 92 are `mixed_n87_L948`,
  `mixed_n91_L970` and `mixed_n92_L975`.) Each is below the side and above the public
  value the comment names, so the improvement stated is smaller than the improvement over
  what the source has published, never larger.
- **Improvement figures that are not lower bounds.** At $n = 88$ and 93 the audit
  compares with the rectangle values $3791/400$ and $973/100$, below the bounds already
  standing there ($237/25$ and $39/4$, and $191/20$ at $n = 88$ from `mixed_n87_L955`,
  which that README names), so `improvement_lower` overstates the margin, as at five
  counts before (review finding OC-1).
- **Nagamochi’s value as a reference.** The comments call his closed form “a reference
  value” and cite [jlevy/squares#295](https://github.com/jlevy/squares/issues/295). The
  comparison facts in the audit receipt state it, and no claim here rests on it.

The [review of these certificates](../../../../docs/project/reviews/review-2026-10-03-wand125-october-3-certificates.md) records these as findings OC-1 and OC-2.

## Limitations

- **The source’s checker is not replayed.** Coverage was decided here by `sqverify-fast`
  alone; the source’s C++ and its axis tables have not run on any of the 22.
- **The bundles are pinned and not held.** A replay needs each tarball from the source at
  the pinned revision, with the digest above. `--via git` fetches it by Git.

## Compressed Files

The 44 upstream data files of more than 1,000 lines, the 22 candidates and the 22
certificates, are stored as deterministic gzip made by `gzip -9n`, with no file name or
timestamp in the header. The table gives the Git blob and SHA-256 of the decompressed
bytes, which are the file’s blob and digest at the pinned commit; each SHA-256 is also
the one [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) pins.
The repository’s readers take the upstream path and decompress through
`devtools.retained_data.read_retained_bytes`, and
`python -m devtools.retained_data check PACKET` re-derives every row.

Before running any of the source’s own programs on this packet, restore the exact upstream
tree from the repository root:

```sh
find packing/resources/web/wand125-mixed-bounds-2026-10-03 -name '*.gz' -exec gunzip -k {} +
```

The restored plain files are untracked, so remove them afterwards; while both copies are
present, the acquisition check reports each as retained twice.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `square-packing-bounds/certificates/mixed_n51_L746/candidate.json.gz` | upstream | `6c233281eb82f3ac868f190088201bd85a5ddfad` | `557027e6e0ed329bf87a3dfc6062d2707e4dcfe4fc7a73bb6e55756a7e21fe39` |
| `square-packing-bounds/certificates/mixed_n51_L746/certificate.json.gz` | upstream | `7d9184599c177e76060f0c909f11048b4521f8b6` | `4d94f03a7929066e5b0b68778bce72a78e64ef46b9f695e50627cce503c10f08` |
| `square-packing-bounds/certificates/mixed_n52_L755/candidate.json.gz` | upstream | `5b4bd6420f4d15bce80d8c9c0e9ab48931d2902a` | `74d8e15c54959e5726ca72b5817c191ed01904f8a6f2e40c04ed3b2fbd7b3e88` |
| `square-packing-bounds/certificates/mixed_n52_L755/certificate.json.gz` | upstream | `d4be098a86420f35395dd0e39bde997bedc3ee9b` | `4bf2a57de562c822faa281c3c884bdf3c252c3da83e5570183fb0a16787d2a8e` |
| `square-packing-bounds/certificates/mixed_n55_L7728/candidate.json.gz` | upstream | `154772cbea8ee081786992dcc6cbff3b5584b788` | `40959262f2afa040613dd89973fc0f40c0adb3d69ab06d7dabab9e6630b6ba7d` |
| `square-packing-bounds/certificates/mixed_n55_L7728/certificate.json.gz` | upstream | `2b9c0fa79d57e725b44f51f924c4a268987b85e8` | `e054e5de7f9681860ebf0b20f0d707eccd654fb1b51afe1cc7bb81c2aa04bb9d` |
| `square-packing-bounds/certificates/mixed_n58_L7905/candidate.json.gz` | upstream | `99fee443e3b181113c5d3b419eebe89e9a842e5b` | `5308e51ada5cc8351bcef55a676fee33cb633669abb7af4b6facb9b51d6412ef` |
| `square-packing-bounds/certificates/mixed_n58_L7905/certificate.json.gz` | upstream | `c7979d80024a6b40ab1094714bf7b17d06516e10` | `dcbbed87261efe3a42bcb2464222fbb71a2eec88e8234e10ef1d617ececff139` |
| `square-packing-bounds/certificates/mixed_n69_L8612/candidate.json.gz` | upstream | `355770b04cfe28352f9116127ab486953f2ecddd` | `2029d5adadbd3d27da7c113baa1f86066144a646c5f8f76eeae58352d088142e` |
| `square-packing-bounds/certificates/mixed_n69_L8612/certificate.json.gz` | upstream | `8dd6b47962a542db9856aa15e553cfc217e9d488` | `3659a728f79ed7dab0d1634fb8b7b25a99b95688c903b8afc154c05ec3f71ce6` |
| `square-packing-bounds/certificates/mixed_n70_L86475/candidate.json.gz` | upstream | `f86c0f04d3e73b8aadf8404548cef08ac2981e24` | `7fc28fe513e9ffd41ebabe50c01c315603366e5dcdce4593f255c6fa984f332e` |
| `square-packing-bounds/certificates/mixed_n70_L86475/certificate.json.gz` | upstream | `dede2a09eaeeef6574233450587f779cd3cc7368` | `0a21f0ccf1886c33873ac7e9f671ad58b0c2d9a704c5c895f516921f48561c93` |
| `square-packing-bounds/certificates/mixed_n71_L8705/candidate.json.gz` | upstream | `646f7bf079dbec63a75f341bc348a1b58ee31fe4` | `74d57054ad04239754f3ac5fe5f5fa2c1d8bddcd7dffb3d172eed43c0b7aaaa6` |
| `square-packing-bounds/certificates/mixed_n71_L8705/certificate.json.gz` | upstream | `55222b14949d9e1a59e8714a5c6421011fb39b24` | `dd4c0c94bccb731d7162e49c3f879ff62286cab775716de4b0cd5fca66042b70` |
| `square-packing-bounds/certificates/mixed_n73_L8809/candidate.json.gz` | upstream | `487401138967849166992b94c6d3c90437ff6364` | `09c72d35cdf6740a495e9b232c92f4942cb68ade99fc06dd3833e89a9d2e0792` |
| `square-packing-bounds/certificates/mixed_n73_L8809/certificate.json.gz` | upstream | `8094f0242509060d320e22835a8ef99944baa817` | `f0136f1eac5f7758230d06c6f1e0face6790e712bf988a19f28ff3202df14be7` |
| `square-packing-bounds/certificates/mixed_n74_L88675/candidate.json.gz` | upstream | `e5a00cfdb4bf1f19ef774a2f7d2ed2b178ced826` | `dd4db4536a8d22b501b7d86e5a4f1705ddd844a0cc68b96e5e3bfa4febe8c204` |
| `square-packing-bounds/certificates/mixed_n74_L88675/certificate.json.gz` | upstream | `f8b67524848c05260315ac660388af82d8391910` | `cf8b673e6d27ff78590ce19347eef5b744ef61b57034d1db6243a87b336bd92c` |
| `square-packing-bounds/certificates/mixed_n75_L892/candidate.json.gz` | upstream | `02811c5a8fbcbfd40cda924ae7f8423fd2ae3836` | `19b8c39aec88e5a0f800a483724c6e2b5e22d87df6176c0afcc2ec6dba95a795` |
| `square-packing-bounds/certificates/mixed_n75_L892/certificate.json.gz` | upstream | `b5d6b839d1177899cf36c9da334b91a7390bcacc` | `47782d9a7bad93ac7a068317df3a9f3206477387204dd72c7f0a5c29960dbfed` |
| `square-packing-bounds/certificates/mixed_n76_L896/candidate.json.gz` | upstream | `de9cecc23da8db895b78f6f26f03f7e8c33331f9` | `baaf56a23e59246e9196753866e1a67d25b644298164b74fb94b9a2450d5fb88` |
| `square-packing-bounds/certificates/mixed_n76_L896/certificate.json.gz` | upstream | `c57846bd96a0965c437716f798f648b206d69f68` | `15fe1fa785c990924f54f2b34b47b3b95676a239ea15d556a64e0e31f0d2ce9e` |
| `square-packing-bounds/certificates/mixed_n86_L950/candidate.json.gz` | upstream | `ee998305508dc7ded2374052db3fd0c8cd4ca5cf` | `58e333d31fe23233666214f66ff3078e70389166449dd351d3427e5d136c2124` |
| `square-packing-bounds/certificates/mixed_n86_L950/certificate.json.gz` | upstream | `ffac38929f828e25cad6733e65d9adf40899d07c` | `3ce539a3cdf59771ee3e5ec5b50998031b846f80c6f53b3c2645250861ebf9eb` |
| `square-packing-bounds/certificates/mixed_n87_L955/candidate.json.gz` | upstream | `5dbfc4e11df3f9a5d32d1c022aad28284a26af99` | `ea2f809a2d666fbdaf01f10ef5540c6aae72764a63f62a53db7d095c74b4f873` |
| `square-packing-bounds/certificates/mixed_n87_L955/certificate.json.gz` | upstream | `d64ff5c28aee197aac4114f636f22189e2a6bb91` | `1e02d8c0a086d89ea209e43dbf7252c9492da6fbaaf59861862363fafae319e8` |
| `square-packing-bounds/certificates/mixed_n88_L960/candidate.json.gz` | upstream | `f06c7ae6ba22a8948c9d2b8b39625244960b3d5c` | `05062008af607a9b3a563c99ee3a1dfc9f6499102feb8373a4e9cf82e5faf15d` |
| `square-packing-bounds/certificates/mixed_n88_L960/certificate.json.gz` | upstream | `bffb026a45fccc387f6bb68518819bca77ea6674` | `7ad1c84e9a368aab299fd519b0c4dc3d87086884104312cf9b62d11cb20e94e1` |
| `square-packing-bounds/certificates/mixed_n89_L965/candidate.json.gz` | upstream | `beab01a9cb44629ea414ad1053f059f816b469af` | `1257871142caebec151a7ae09893027f77a7ee0f1b451f304b7c9e933739b67a` |
| `square-packing-bounds/certificates/mixed_n89_L965/certificate.json.gz` | upstream | `21fd24ec143e915df07ea63607aa4eaed52cefb5` | `7a08ca970d86e46f4d54a29db42264c55ce2babc9e76fce3f1f83481e616aa42` |
| `square-packing-bounds/certificates/mixed_n90_L9725/candidate.json.gz` | upstream | `7cb4656998453f2cd9bbf944ab7c02f0faf10590` | `c061c239dedfabda49e68a9cbe28e6177df6ac634953aea6e804a23622c604cd` |
| `square-packing-bounds/certificates/mixed_n90_L9725/certificate.json.gz` | upstream | `cde855c55daf5cbccc8c3477dfcf17f9537aaa3b` | `4f4985699aed6d668dc42a91d8dabe0478aeb980e6a2958694f65d18f7966687` |
| `square-packing-bounds/certificates/mixed_n91_L975/candidate.json.gz` | upstream | `2df3b9f9e91644e8e44abddffafa37330a44fc93` | `60fa33a2c3bf43ad911f1000fe8af7a6b50320ec02628aeaa3aac5e7613e8be2` |
| `square-packing-bounds/certificates/mixed_n91_L975/certificate.json.gz` | upstream | `78423dae536eb15b0232579a2a54492f584eb7ed` | `4a25348464e30bc09e3f57a9746721a08b6c0dbb2cab882eb4e2e7494c5b1b31` |
| `square-packing-bounds/certificates/mixed_n92_L977/candidate.json.gz` | upstream | `698621ae9c5d709e6156b54d09463b23c2d32b7c` | `d788fcd161eb85874e76e3572cf978c6e4094edef71d613621ce27c01c24cfd6` |
| `square-packing-bounds/certificates/mixed_n92_L977/certificate.json.gz` | upstream | `cb1c67f83ad8af3d45bdc6d91c9ad89d4f08a3e6` | `1ae262843753f61fa7e74cf2a6d48b038084467e95efd39553551c11e806f25d` |
| `square-packing-bounds/certificates/mixed_n93_L986/candidate.json.gz` | upstream | `58a52afe98f4631fb9676a9a0d970834931d5f59` | `8847e1d79939698db4423d9f1c13826a5e13a1a793f5f3bcc371160b38e272b5` |
| `square-packing-bounds/certificates/mixed_n93_L986/certificate.json.gz` | upstream | `44a263d5d7d845ab27e9c8143fb3ae2ac5b4905d` | `45137c7375232247472340801a9a13268e3200fa21916fafcfd84472ab5d6277` |
| `square-packing-bounds/certificates/mixed_n94_L992/candidate.json.gz` | upstream | `8e9d0b6171950846291a36e9106404c370f0761e` | `0734ea3a3c9ec8b72b8395db573bf307bc81a5f99efb9771c3fb69281b4967fc` |
| `square-packing-bounds/certificates/mixed_n94_L992/certificate.json.gz` | upstream | `969b3e6a65dc85c34545435a53f6a7a538218baa` | `9f6ba1d4de5b583b1730be451aa185565e7a7865f8147f1820b10d9e66434456` |
| `square-packing-bounds/certificates/mixed_n95_L996/candidate.json.gz` | upstream | `22a8961d765d3e30e6c7ee8697e57fd05f1a8d23` | `efbbcc1dfc06d5437fdf6ad4d32bac2d8119efa531017cd688a6b95cf80d3098` |
| `square-packing-bounds/certificates/mixed_n95_L996/certificate.json.gz` | upstream | `91c1ad2bd8872b0f45d5d63f8ed52538127c95df` | `ad9351eaee6dec0b59e5dcb0a2a8dd254ad4b476dd3888563e7bef15917ce11d` |
| `square-packing-bounds/certificates/mixed_n96_L997/candidate.json.gz` | upstream | `7998d258f96f1efc2eae315d27c7aefd6138bc59` | `c4bdda4629db55216e238363be13ed301223390498ce4e5b4d85e61a573116bb` |
| `square-packing-bounds/certificates/mixed_n96_L997/certificate.json.gz` | upstream | `a974adbabe4493c0ee6b43ef6ca8245f610fc73e` | `2b2f299b61c95997a1c353372774bdd4cd36b1d7ceb6522c858f053320160ce1` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
