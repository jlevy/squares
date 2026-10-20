# Reported Fine-Net Lower Bounds at 18 Counts, 16 October

Eighteen commits of 16 October to wand125/square-packing, one per certificate, add
check2 measure certificates at n = 38, 40, 41, 43, 51, 68, 84 to 86, 88 to 92 and 106 to
110\. The author reports them in a comment on
[jlevy/squares#446](https://github.com/jlevy/squares/issues/446#issuecomment-6210736972)
(created 2026-10-16T07:49:56Z, edited 09:00:31Z), with three of 13 October that the
record already holds (n = 37, 39 and 44: T-178, T-176 and T-177, from the
[13 October packet](../wand125-fine-net-n37-n39-n44-2026-10-13/README.md)). Each bound
was above both lower lanes of its case record at registration.
The n108 certificate has an accepted retained native replay and certificate-specific
reviews; its case adopts $531/50$. The accepted Mac checkpoints for n68, n84 and n85 are
now retained with mapped mathematical reviews and prepared V3/C3 records, confirmed by
re-implementation sharing the producer’s crate apart from the declared-net readers.
Their exact audits decide premises and saved poses only.
The other 14 remain reported at V0/C0 under
[stage 4](../../../campaign/result-import.md#stage-4-validate).

The five at n = 38 to 51 are on the 2,073-direction net of T-132, T-142 and T-143 (core
$4999/5000$, half-angle step $1/5002$); the 13 at n = 68 to 110 are on the 201-direction
standard net, which their candidates declare (core $9977/10000$, step $83/40000$). Six
are marked lifted: the search started from a published certificate at a smaller count,
mapped to the new side and re-solved by linear programming
(`provenance/search-notes.md`). Lifting is provenance only; the certificate is the
measure, checked like any other.

| n | Certificate | Claim | Added by | Release asset (bytes, SHA-256) | Positive rows | Candidate digest | Net |
| ---: | --- | --- | --- | --- | ---: | --- | --- |
| 38 | [`mixed_n38_L65775`](https://github.com/wand125/square-packing/tree/02c5595f26e8cf1f6be89080fdd66a9a5d6d364f/problems/square-lower-bounds/certificates/mixed_n38_L65775) | $s(38) \ge 2631/400$ | `02c5595`, 2026-10-16T07:45:44Z | 642,158, `b6fc8a4f…70c0` | 654 | `90806e2d…0045` | 2,073 of step 1/5002, core 4999/5000 |
| 40 | [`mixed_n40_L6735`](https://github.com/wand125/square-packing/tree/4762e420765d663f601f007c60c9c47351c959ea/problems/square-lower-bounds/certificates/mixed_n40_L6735) | $s(40) \ge 1347/200$ | `4762e42`, 2026-10-16T07:46:04Z | 658,266, `7ba00d72…29ed` | 707 | `12c56587…f4f8` | 2,073 of step 1/5002, core 4999/5000 |
| 41 | [`mixed_n41_L68025`](https://github.com/wand125/square-packing/tree/209369b6a186e2304548d52584425125d4c97736/problems/square-lower-bounds/certificates/mixed_n41_L68025) | $s(41) \ge 2721/400$ | `209369b`, 2026-10-16T07:46:24Z | 634,762, `acffa158…1f55` | 629 | `8ec6f61b…a488` | 2,073 of step 1/5002, core 4999/5000 |
| 43 | [`mixed_n43_L69425`](https://github.com/wand125/square-packing/tree/d3c115c5b7a12c7c057ef567cc426df909846e92/problems/square-lower-bounds/certificates/mixed_n43_L69425) | $s(43) \ge 2777/400$ | `d3c115c`, 2026-10-16T07:46:42Z | 653,990, `182905f6…7a3b` | 714 | `b9471722…2073` | 2,073 of step 1/5002, core 4999/5000 |
| 51 | [`mixed_n51_L75275`](https://github.com/wand125/square-packing/tree/9cd2b2d43dfe57e12da066a1e85a51f457c0fc9f/problems/square-lower-bounds/certificates/mixed_n51_L75275) | $s(51) \ge 3011/400$ | `9cd2b2d`, 2026-10-16T07:46:59Z | 666,772, `5d0ede76…35f3` | 908 | `88ea7b82…1893` | 2,073 of step 1/5002, core 4999/5000 |
| 68 | [`mixed_n68_L853`](https://github.com/wand125/square-packing/tree/14b4b0badd79cd95f9456143b304d5d158cf2ac7/problems/square-lower-bounds/certificates/mixed_n68_L853) | $s(68) \ge 853/100$ | `14b4b0b`, 2026-10-16T07:47:16Z | 330,712, `7e502405…4a9c` | 726 | `e2ab1b5b…ef2e` | 201 of step 83/40000, core 9977/10000 |
| 84 | [`mixed_n84_L94225`](https://github.com/wand125/square-packing/tree/f28b5f3d0ebc500a761a02514c1ce5b9b9e203f1/problems/square-lower-bounds/certificates/mixed_n84_L94225) | $s(84) \ge 3769/400$ | `f28b5f3`, 2026-10-16T07:47:34Z | 345,918, `25869a15…544c` | 815 | `2d698805…e178` | 201 of step 83/40000, core 9977/10000 |
| 85 | [`mixed_n85_L9475`](https://github.com/wand125/square-packing/tree/fc2e96f0a253e00fbc4263625f4fc34774d157a6/problems/square-lower-bounds/certificates/mixed_n85_L9475) | $s(85) \ge 379/40$ | `fc2e96f`, 2026-10-16T07:47:51Z | 342,379, `c9ca6caa…26a5` | 838 | `92eed10e…ecdd` | 201 of step 83/40000, core 9977/10000 |
| 86 | [`mixed_n86_L95275`](https://github.com/wand125/square-packing/tree/2ad6bda87c58fa9a67debc3d3ef303810525fd34/problems/square-lower-bounds/certificates/mixed_n86_L95275) | $s(86) \ge 3811/400$ | `2ad6bda`, 2026-10-16T07:48:10Z | 342,314, `4f840709…f1bf` | 750 | `4939aed7…4761` | 201 of step 83/40000, core 9977/10000 |
| 88 | [`mixed_n88_L96325`](https://github.com/wand125/square-packing/tree/f8f99e3d82c682f9600539c15b2a6f76b9e4e4c3/problems/square-lower-bounds/certificates/mixed_n88_L96325) | $s(88) \ge 3853/400$ | `f8f99e3`, 2026-10-16T07:48:28Z | 350,207, `306ce4fe…a804` | 754 | `a7ae1619…246b` | 201 of step 83/40000, core 9977/10000 |
| 89 | [`mixed_n89_L9685`](https://github.com/wand125/square-packing/tree/a361ba247b3dac28ee3ab8ff8e62e827bcdf8120/problems/square-lower-bounds/certificates/mixed_n89_L9685) | $s(89) \ge 1937/200$ | `a361ba2`, 2026-10-16T07:48:44Z | 329,872, `93e6750c…bcae` | 651 | `863b20a6…2b8e` | 201 of step 83/40000, core 9977/10000 |
| 90 | [`mixed_n90_L978`](https://github.com/wand125/square-packing/tree/8155028aea6ed235b0c2766b38657dd21704aff4/problems/square-lower-bounds/certificates/mixed_n90_L978) | $s(90) \ge 489/50$ (lifted) | `8155028`, 2026-10-16T07:52:16Z | 429,331, `430d540c…a107` | 1415 | `81bf5b0f…3407` | 201 of step 83/40000, core 9977/10000 |
| 91 | [`mixed_n91_L97875`](https://github.com/wand125/square-packing/tree/e060e98b540e46f88e84ac6fd18462dcb209ee42/problems/square-lower-bounds/certificates/mixed_n91_L97875) | $s(91) \ge 783/80$ | `e060e98`, 2026-10-16T07:49:02Z | 334,797, `74de784e…dec8` | 712 | `b9a08498…0e48` | 201 of step 83/40000, core 9977/10000 |
| 92 | [`mixed_n92_L986`](https://github.com/wand125/square-packing/tree/599a67c371b09a4c05d3709be63c3d6be4a9cd14/problems/square-lower-bounds/certificates/mixed_n92_L986) | $s(92) \ge 493/50$ (lifted) | `599a67c`, 2026-10-16T07:52:33Z | 354,699, `2685bb69…45fd` | 860 | `464e1312…5815` | 201 of step 83/40000, core 9977/10000 |
| 106 | [`mixed_n106_L10503`](https://github.com/wand125/square-packing/tree/3b2538704f36b699795a50b5ef19686c843150ab/problems/square-lower-bounds/certificates/mixed_n106_L10503) | $s(106) \ge 10503/1000$ (lifted) | `3b25387`, 2026-10-16T07:52:50Z | 348,800, `6da3bb6a…ddb9` | 735 | `745aa9c9…d736` | 201 of step 83/40000, core 9977/10000 |
| 107 | [`mixed_n107_L1058`](https://github.com/wand125/square-packing/tree/021702fa6b3d345ffc51e053ef6b05f03df55cd5/problems/square-lower-bounds/certificates/mixed_n107_L1058) | $s(107) \ge 529/50$ (lifted) | `021702f`, 2026-10-16T07:53:07Z | 375,508, `ceea74bc…29f9` | 1022 | `1edab306…9ba0` | 201 of step 83/40000, core 9977/10000 |
| 108 | [`mixed_n108_L1062`](https://github.com/wand125/square-packing/tree/6af3c00991c937d40ac0fe867fe049b8e9f3bf2d/problems/square-lower-bounds/certificates/mixed_n108_L1062) | $s(108) \ge 531/50$ (lifted) | `6af3c00`, 2026-10-16T07:53:23Z | 356,853, `187c71b5…3522` | 823 | `5ce2449f…e1a9` | 201 of step 83/40000, core 9977/10000 |
| 110 | [`mixed_n110_L1073`](https://github.com/wand125/square-packing/tree/718887cfaa8727cc75108c5924fa1330df4fa098/problems/square-lower-bounds/certificates/mixed_n110_L1073) | $s(110) \ge 1073/100$ (lifted) | `718887c`, 2026-10-16T07:53:40Z | 346,089, `3e4021e2…1212` | 872 | `53026439…05bb` | 201 of step 83/40000, core 9977/10000 |

The packet is pinned at `718887cfaa8727cc75108c5924fa1330df4fa098`, the last of the 18
commits, which holds all 18 directories.
Each directory is the same Git tree from the commit that adds it through the
repository’s head when read, `aaed7d5` (2026-10-17), whose later commits change the
cubes problem, a rectangle theorem, the closed-form layer and the site, and not these
directories or their licence.
Retrieved 2026-10-17T17:58Z.

## The Standing Bounds

Each claim against the case record’s lower lanes on `main` at `804eff369`. At 106 to 110
the reported lane is wand125’s closed form (T-180) and the verified lane Karakuş’s strip
bound; the bundles’ own READMEs compare against the latter.

| n | Claim | Reported lower lane | Verified lower lane | Gain over the reported lane | Reported upper bound |
| ---: | --- | --- | --- | --- | --- |
| 38 | $2631/400 = 6.5775$ | T-068: $1309/200$ | T-074: $1309/200$ | $13/400$ | 6.707107… |
| 40 | $1347/200 = 6.735$ | T-157: $3359/500$ | T-157: $3359/500$ | $17/1000$ | 6.828427… |
| 41 | $2721/400 = 6.8025$ | T-111: $271/40$ | T-111: $271/40$ | $11/400$ | 6.926693… |
| 43 | $2777/400 = 6.9425$ | T-090: $2763/400$ | T-090: $2763/400$ | $7/200$ | 7.000000… |
| 51 | $3011/400 = 7.5275$ | T-090: $747/100$ | T-090: $747/100$ | $23/400$ | 7.690356… |
| 68 | $853/100 = 8.53$ | T-068: $851/100$ | T-074: $851/100$ | $1/50$ | 8.798795… |
| 84 | $3769/400 = 9.4225$ | T-094: $9411/1000$ | T-094: $9411/1000$ | $23/2000$ | 9.697935… |
| 85 | $379/40 = 9.475$ | T-075: $473/50$ | T-075: $473/50$ | $3/200$ | 9.742641… |
| 86 | $3811/400 = 9.5275$ | T-090: $9503/1000$ | T-090: $9503/1000$ | $49/2000$ | 9.820535… |
| 88 | $3853/400 = 9.6325$ | T-091: $481/50$ | T-091: $481/50$ | $1/80$ | 9.882451… |
| 89 | $1937/200 = 9.685$ | T-082: $193/20$ | T-082: $193/20$ | $7/200$ | 9.949747… |
| 90 | $489/50 = 9.78$ | T-091: $973/100$ | T-091: $973/100$ | $1/20$ | 10.000000… |
| 91 | $783/80 = 9.7875$ | T-091: $781/80$ | T-091: $781/80$ | $1/40$ | 10.000000… |
| 92 | $493/50 = 9.86$ | T-082: $977/100$ | T-082: $977/100$ | $9/100$ | 10.000000… |
| 106 | $10503/1000 = 10.503$ | T-180: 10.403976649170… | T-083, T-084: 10.3107084351… ($1/2 + \sqrt{n - \lfloor\sqrt n\rfloor + 1/4}$) | 0.0990 | 10.822908… |
| 107 | $529/50 = 10.58$ | T-180: 10.436790394042… | T-083, T-084: 10.3615414616… ($1/2 + \sqrt{n - \lfloor\sqrt n\rfloor + 1/4}$) | 0.1432 | 10.846667… |
| 108 | $531/50 = 10.62$ | T-180: 10.484093855851… | T-083, T-084: 10.4121138007… ($1/2 + \sqrt{n - \lfloor\sqrt n\rfloor + 1/4}$) | 0.1359 | 10.904821… |
| 110 | $1073/100 = 10.73$ | T-180: 10.600000000000… | T-083, T-084: 10.5124921972… ($1/2 + \sqrt{n - \lfloor\sqrt n\rfloor + 1/4}$) | $13/100$ | 10.996783… |

No count is settled: the least gap to an upper bound is n = 43’s
$7 - 2777/400 = 23/400$.

## What Is Retained

Two tools wrote the packet, and each has a check that re-derives it from the packet
alone.

- **The documents.** [`devtools.acquire_source`](../../../devtools/acquire_source.py)
  wrote them from its [declaration](acquisition/declaration.json): the
  [acquisition record](acquisition/sources.json) and the
  [subtree manifest](acquisition/upstream-subtree.sha256) give the size and SHA-256 of
  all 199 files in scope, and `--check` re-derives them.
  Retained byte for byte under
  [`square-packing/`](square-packing/problems/square-lower-bounds/certificates/): each
  directory’s `README.md`, `ASSET.json`, `bundle.json` and `files-sha256.json`, and the
  six lifted certificates’ own `provenance/search-notes.md`. Pinned by digest only, with
  their reasons in the record: the licence, the other twelve `search-notes.md`, and each
  `check2/src/` document, all byte-identical to copies earlier packets retain or, for
  `SOUNDNESS.md` and `INDEPENDENCE.md`, this repository’s own files of 3 October.
- **The release assets’ data.** Each directory’s data is a tarball in release
  `square-lower-bounds-v1`, which its `ASSET.json` names and says unpacks in place
  beside the documents.
  `devtools.fine_net_followup retain` refused each asset unless its size and SHA-256
  were the pinned ones, unpacked it safely, and copied six of its eight members to
  [`release/`](release/certificates/) at their own paths in the asset: `candidate.json`
  (stored as deterministic gzip, by the archive’s rule for data of more than 1,000
  lines), `check2/receipt.json`, `check2/control.json`, the run log
  `check2/run.jsonl.gz` and the control log `check2/control-197_200.jsonl.gz` (both kept
  as published), and `verification/prepublication-receipt.json`. The
  [retention record](acquisition/release-assets.json) lists every member of every asset
  with its size and SHA-256, and `fine_net_followup check-retained` re-derives it.

Two members of each asset are pinned by digest and not copied:

- `check2/src/sqverify-proof-net-fe12e036c.tar.gz`, 69,540 bytes, SHA-256
  `e495f9bf…71e81` in all 18: the source’s adaptation of this repository’s
  `sqverify_fast`, the archive the 6 and 13 October packets pin by the same digest.
  It carries no notice of its own, and it is kept out of this tree beside the crate
  whose declared-net change was written apart from it
  ([`sqverify_fast/INDEPENDENCE.md`](../../../sqverify_fast/INDEPENDENCE.md)). It was
  digested and not opened.
- the sealed inner bundle `n*-check2-bundle.tar.gz` (179,240 to 347,318 bytes), whose
  payloads repeat this directory’s files; each premises receipt inventories its members.

Under
[`OR-18`](../../../../operating-rules.md#or-18-keep-bulk-data-out-of-git-and-never-bind-code-or-verdicts-to-a-git-commit-or-blob)
the retained set is small enough for Git: 2.38 MB in a checkout and about 2.3 MB as Git
stores it, since the logs are compressed already.
The largest file is n = 43’s run log, 0.18 MB.

## What Was Checked

**Custody.** Each asset’s size and SHA-256 equal its `ASSET.json` at the pin and its
line of the release’s `SHA256SUMS` (lines 447 to 464), downloaded on 2026-10-17. Each
document has the Git blob its commit names.

**Input premises.** `devtools.fine_net_followup premises` unpacked each asset beside the
pinned documents and ran the maintained readers on the candidate
(`receipts/premises-nN.json`). All 18 end `EXACT_PREMISES_HOLD`: lemma N0’s premises and
its last bin hold on the declared net, with $B(1 + D) = 25009997/25010000$ on the fine
net and $399908091/400000000$ on the standard one; the mass is $n - 1/100000$ over
positive rows only; one candidate digest appears throughout; and the full check2 reader
holds every premise.
Each sealed bundle holds 16 files and matches its `files-sha256.json`, and each
directory’s README differs from its sealed edition.
No program of the source ran.

**Two reported complete runs each.** Each check2 receipt records the source’s adapted
crate (source digest `ab6e33e1…`, binary `ec04d332…`) verifying every direction, and
each pre-publication receipt a second run of the same source on a fresh Ubuntu 24.04
machine, not the run the check2 receipt embeds.
Each control scales every mass by $197/200$ at 32 sampled directions and reports all 32
refused, 31 with an exact capture below the threshold.
These are attributed author outcomes; a sampled control does not replace the whole-net
controls the records lane requires.

| n | check2 run: wall (s), threads | Direction CPU (s) | Nodes | Pre-publication run (s) | 197/200 control: refused, exact below 1 |
| ---: | --- | ---: | ---: | ---: | --- |
| 38 | 1,000.3, 16 | 15,424 | 891,069,250 | 656 | 32 of 32, 31 |
| 40 | 2,740.4, 12 | 23,501 | 962,785,180 | 1,042 | 32 of 32, 31 |
| 41 | 1,951.5, 16 | 22,697 | 963,246,604 | 1,051 | 32 of 32, 31 |
| 43 | 4,451.4, 16 | 44,907 | 1,321,515,092 | 2,143 | 32 of 32, 31 |
| 51 | 2,395.2, 16 | 28,602 | 1,374,662,152 | 1,354 | 32 of 32, 31 |
| 68 | 255.6, 12 | 1,730 | 104,110,078 | 75 | 32 of 32, 31 |
| 84 | 328.4, 12 | 3,091 | 136,054,170 | 121 | 32 of 32, 31 |
| 85 | 255.1, 12 | 2,733 | 126,895,910 | 124 | 32 of 32, 31 |
| 86 | 173.6, 8 | 1,353 | 113,360,590 | 131 | 32 of 32, 31 |
| 88 | 453.2, 12 | 3,894 | 139,087,350 | 156 | 32 of 32, 31 |
| 89 | 164.2, 8 | 1,271 | 114,922,328 | 123 | 32 of 32, 31 |
| 90 | 688.8, 7 | 4,678 | 247,038,884 | 489 | 32 of 32, 31 |
| 91 | 225.4, 8 | 1,722 | 134,970,880 | 167 | 32 of 32, 31 |
| 92 | 404.2, 7 | 2,398 | 189,532,510 | 255 | 32 of 32, 31 |
| 106 | 179.2, 8 | 1,393 | 141,802,590 | 150 | 32 of 32, 31 |
| 107 | 1,733.1, 16 | 5,069 | 188,941,088 | 244 | 32 of 32, 31 |
| 108 | 154.5, 8 | 1,210 | 136,113,602 | 141 | 32 of 32, 31 |
| 110 | 976.3, 16 | 5,099 | 163,846,790 | 249 | 32 of 32, 31 |

## The Price of a Complete Replay

The census route of the 6 October soundness review: `sqverify-fast` at every direction
of the declared net, then the whole-net controls (the $99/100$ mutant at every
direction, and the original and the near-threshold mutant at the least-bound direction),
so about twice each source receipt’s direction CPU. On this host’s ratio of 0.871 to the
source (think-w76a’s eight-direction sample) that is 82.6 CPU-hours for all 18, and 94.9
if this host is no faster: 0.6 to 2.8 each at 68 to 110, 7.5 to 8.6 at 38, 11 to 13 at
40 and 41, 13.8 to 15.9 at 51 and 21.7 to 25.0 at 43. Each is under the owner’s 40
CPU-hour item cap, and the owner asked on 17 October for all 18 to run.
The census reads each candidate from `release/`, and its receipts are kept under
`benchmarks/measure-verifier/census-mixed/wand125-fine-net-lower-bounds-2026-10-16/`.

## Sources and Notices

The nearest enclosing source notice, `problems/square-lower-bounds/LICENSE`, is MIT,
Copyright 2026 wand125, byte-identical to the notice the FN-1 packet retains.
Each `ASSET.json` places its tarball’s data files in the directory it covers.
The nested verifier archive carries no notice of its own and is not retained.

The source credits wand125 (Hiroaki Hosono), with code and formats credited to Evan
Daniel, tokoharu and jlevy/squares; all 18 commits are authored by Hiroaki Hosono.
The `problems/square-lower-bounds/README.md` says parts of the work were produced with
AI assistance under human direction, and each commit names Claude Opus 5.5 as co-author.

## Compressed Files

| Stored file | Origin | Git blob (decompressed) | SHA-256 (decompressed) |
| --- | --- | --- | --- |
| `release/certificates/mixed_n106_L10503/candidate.json.gz` | upstream | `d533a2584e0d37fe56413762dbb2c0706ccc4bce` | `414b0876446746a1f5e03d9a30bff7883a8c74a9d29129f26dd0f47b99c8a51c` |
| `release/certificates/mixed_n107_L1058/candidate.json.gz` | upstream | `afd883b0920ff668186173fe7168de2f34990289` | `fa3c7c63a886db1d7348f72c2724bd44f677fc8475e7eff81bd641b628a8280e` |
| `release/certificates/mixed_n108_L1062/candidate.json.gz` | upstream | `627fddd90ffa4ac2e7310a1d0223490efebf76cd` | `4d72da64052667a3ebf057f7e78ea9d40f1521a0b86ddef210a2be319d27042a` |
| `release/certificates/mixed_n110_L1073/candidate.json.gz` | upstream | `0a55d2b49a9a03551330d0b5b8f774d24b4a89ef` | `e1dab896d997182632c470268ab022f216b3a1160068328e305d0a6d15da2081` |
| `release/certificates/mixed_n38_L65775/candidate.json.gz` | upstream | `98ddb8026977434db4ea1d9484c8fff7d556f5f0` | `0fa317b9bdcb201cec3e1a90dd26a48888817296d9b9625f217f30776ec7ace0` |
| `release/certificates/mixed_n40_L6735/candidate.json.gz` | upstream | `35374eb287a8f00f9f5d34cab522dedaf8677cf8` | `c5ed5c517f22a74e851c368428aeaf93e378b9e389723c964b788207ca4115b6` |
| `release/certificates/mixed_n41_L68025/candidate.json.gz` | upstream | `54ab7f27e6bb924e64844ae3f4aa99f3164bf551` | `bdcf6684da8bda6e71af458d70b68a43fbade4b67008f81484a917ef693fab29` |
| `release/certificates/mixed_n43_L69425/candidate.json.gz` | upstream | `ae175500f5cf4d9effb53eae1b7dd0ee84753e2a` | `ed64d923a6ccf98e47db79aa7a9ee937704cdb79d8b6f57a8ff49c1aa773a65f` |
| `release/certificates/mixed_n51_L75275/candidate.json.gz` | upstream | `3ee4deaee4daa574077333f385c958a8598e1d6c` | `a282e0b6c237613bb7f723e60135d33b3ec7f0503dc2f30e20387ed2c1df57be` |
| `release/certificates/mixed_n68_L853/candidate.json.gz` | upstream | `2328812a729119b6c137966f786bda9c43b1bdf4` | `3c5521d6ce47688cc32c900f3e97fd4f0db01aa85b0217a7ed5f3eacfbd2be6a` |
| `release/certificates/mixed_n84_L94225/candidate.json.gz` | upstream | `39b05fd8d40746957b3019a75ccabc0f054fee91` | `afcba2f978c0ba6c796c901e2d04964d8949d3d11172f7b3fd934cce6946876f` |
| `release/certificates/mixed_n85_L9475/candidate.json.gz` | upstream | `7574fb9d5f4eab13d379817fe4bb52b7c5fc6d27` | `313710d6333e02b8967d185bfafa2ed0d9c4142c289ab1e5a983ab2ab7d30822` |
| `release/certificates/mixed_n86_L95275/candidate.json.gz` | upstream | `2ec2cdc0b4428bad65bbf79118c7a6e6857e4ce9` | `c73f08a2b601c14b8d7b91c704bb6a3443d286324a48eab30cca03450246ffd7` |
| `release/certificates/mixed_n88_L96325/candidate.json.gz` | upstream | `5de287cc57a915228dbefcd63d2493cbe77ff2f8` | `96dd13d30d45f2d4279c8e4bed540205b0a9c6fddc4a4979d4e84a21e5bdaf11` |
| `release/certificates/mixed_n89_L9685/candidate.json.gz` | upstream | `b59334d751aaf99d748c4ed4d0c2644450c839e7` | `6e72be0b6e39bf4ebcfd042335260ef84b53ab7f941338b14925d73d8a6718af` |
| `release/certificates/mixed_n90_L978/candidate.json.gz` | upstream | `f1286611356e705a7b5087b5d935dd4521842eb9` | `7c39766321cd0fceee7d5ae26292065a8e87d523ee57ca8fafae4597aa038da1` |
| `release/certificates/mixed_n91_L97875/candidate.json.gz` | upstream | `85938a238dd17f6b68d5826e30ac8c2753a36d12` | `5a1bc0e828da11566391f19af733a531616db8c1cf3245685ad3a741f1e23f9d` |
| `release/certificates/mixed_n92_L986/candidate.json.gz` | upstream | `c519c3c4eef5a86a881bdd9dad057fb2e16257d4` | `ef2edc690eadf1fff2779a309f726931c33e38ef007359a9567ebd3d3788b3b1` |
| `review-mac/n68-certificate-math/audit-result.json.gz` | receipt | `930aa5b411581b27881851758b47ef5580934333` | `356589fe57947be6b20d4de4118c21206e37b0453e1215f79d804e7d943536b2` |
| `review-mac/n84-n85-certificate-math/n84-audit-result.json.gz` | receipt | `5ffd458c2c28cffed04fae4c3a0bb5c92b7d0039` | `b47b36c0e4d85aea114315182ab494ea0bf8e0ac3ae9fb521eb5f55355365bce` |
| `review-mac/n84-n85-certificate-math/n85-audit-result.json.gz` | receipt | `b68a7c764cdd7a4ffab16b5e5c7f7a6382990766` | `430f258400019efbf48e07117b53e5d35504d91834f17e73d5aa6e62a8a2924c` |

## Original Gzip Files

| Stored file | Origin | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `release/certificates/mixed_n106_L10503/check2/control-197_200.jsonl.gz` | upstream | `ecfd19061d81ba416db012a325a7dfc9429456ee` | `05b3dfba5c549d460e29819ecd10923097bb413ff7b74428fe7ef6376721928b` |
| `release/certificates/mixed_n106_L10503/check2/run.jsonl.gz` | upstream | `bd3a51c3fb1df3ecde4710735e71fef1f76bc0e8` | `38abcdf255220e430183c7b9b79a7802c5ff173939fe82185d70c0947bccb54a` |
| `release/certificates/mixed_n107_L1058/check2/control-197_200.jsonl.gz` | upstream | `c65c18a4a354c2a417864194f2465aa366fb3e12` | `1677949d295f90eb88175d78e19a1d5180a925fb000fad56c7be67c6557c1ce1` |
| `release/certificates/mixed_n107_L1058/check2/run.jsonl.gz` | upstream | `d7c7f20a7a2307f9953ecc14a57a5595c0bd76f0` | `f97cdc4f8365985c8519ee00030efdaa21c082f5bae2ffe69098154e95d7bd0f` |
| `release/certificates/mixed_n108_L1062/check2/control-197_200.jsonl.gz` | upstream | `c2fd49cbb78b029841d15343c971a32e1123ff5c` | `142b576ac0aa5e9602665cf456e981b666b4e1666ef808a51d589ebf79277803` |
| `release/certificates/mixed_n108_L1062/check2/run.jsonl.gz` | upstream | `9d1cc314d6759abdd166a924b6544c84abc24c34` | `671ed371ac6a0a16fc5da83aaaeeaefe70bb126b5381bafdf9831e2c4d9999db` |
| `release/certificates/mixed_n110_L1073/check2/control-197_200.jsonl.gz` | upstream | `ef1e33956d2406a6f21b58462fc25f8992914f43` | `1f1a3689fd2847765fea8aab5ee5be6b75d2a19a3ee24be187e8630d27b46711` |
| `release/certificates/mixed_n110_L1073/check2/run.jsonl.gz` | upstream | `19e5c71d30c5210aa496eb3f07d4ea5dd66681cd` | `fbe6ddb090322c07b97c6ddd1dfeb4ff764324776f11441c7df21bf910f7dea9` |
| `release/certificates/mixed_n38_L65775/check2/control-197_200.jsonl.gz` | upstream | `5853c91e4016545586ad0c6952585c01e698c399` | `bbf88c5913cd1e654546de6fcccd7678d7ae18b4363e04731da3715b28970858` |
| `release/certificates/mixed_n38_L65775/check2/run.jsonl.gz` | upstream | `346c1b188522c92cdd91cd3a50c8243155befeca` | `9f86e320f1ecc37ded02f16055e1ba490fe04bed03c69ace71a5ded0e2ec948c` |
| `release/certificates/mixed_n40_L6735/check2/control-197_200.jsonl.gz` | upstream | `20c528719c0548a73503b1170410f007f97bbed0` | `11f79e2f37eba46b46cb6f11f6b803288a7eccc48d494375a2acb77d87898c26` |
| `release/certificates/mixed_n40_L6735/check2/run.jsonl.gz` | upstream | `962e56c6c1104ac70ed0cb2e5ce1f633ba93050b` | `4d8825e4e30a7a6bb49ae2896b15bfb667515fdde4fcb4fddafe8eff5ad41e78` |
| `release/certificates/mixed_n41_L68025/check2/control-197_200.jsonl.gz` | upstream | `d759695e1ae37d5dba8616e5c908c769581b6c2a` | `5f479627ea24a4ef0145d19bcca4b2fe7ba43aa146bb251924276d8a4a612ace` |
| `release/certificates/mixed_n41_L68025/check2/run.jsonl.gz` | upstream | `a4451d6a44b2cacb92849869f0ad24956f4f8df8` | `78f240b57b2aecbd2e1e3fe9e006f5d4df8316ba4f7c5fe5e40571586651d291` |
| `release/certificates/mixed_n43_L69425/check2/control-197_200.jsonl.gz` | upstream | `a3520827ab633198716923113d529ce9f0697e34` | `553b6a370ba929ef05e9940462a6c44f73d6606ca56771702e16e2cebf58d7c8` |
| `release/certificates/mixed_n43_L69425/check2/run.jsonl.gz` | upstream | `8a827f6b6e6f0b883a23078b0b9f63bdd60fda96` | `51eb3b9acae21f19d1505a0ada9b39c4fa8b05352ed355f22f55b3d9237000d4` |
| `release/certificates/mixed_n51_L75275/check2/control-197_200.jsonl.gz` | upstream | `4b6cf35e15fdeb2cc272c2054dc96809c383112b` | `2c2795ad01e60e06e4745204dc91997917a36590888ede537623e44be2faef71` |
| `release/certificates/mixed_n51_L75275/check2/run.jsonl.gz` | upstream | `523fcc56991a203aa3499a233bcf74b09719897d` | `8e22c5e29dff5d2b011e4b27c19113d1dcc57c43de34f1d1b7e20ec76a8d009b` |
| `release/certificates/mixed_n68_L853/check2/control-197_200.jsonl.gz` | upstream | `ac5323976b71990da6e37fe78c22c4ffb8225899` | `2714e759d2febf14d59ef7558b63c340b270f3dcf1833781401f176a4479bb62` |
| `release/certificates/mixed_n68_L853/check2/run.jsonl.gz` | upstream | `3536e458e5c3f215f0d6cc056b62cde2aa7c8ec2` | `484a9d9288a233c8e6a00567ef818a2148ab540a3c4dd3aea1a4c02c6a6dd0a0` |
| `release/certificates/mixed_n84_L94225/check2/control-197_200.jsonl.gz` | upstream | `4426c8c247775147251c71071c9a82e05cd6e362` | `de163b3f06657ced806ed297de0696e693ac40e11068ef98098c297e439366c6` |
| `release/certificates/mixed_n84_L94225/check2/run.jsonl.gz` | upstream | `1741bf652d23e38875eb9ffcf7ed7223ca1bc061` | `7a7ef4241a2b0329df27e8e26e544c17bcbc43a11864190979d1e4ab55e8b6c7` |
| `release/certificates/mixed_n85_L9475/check2/control-197_200.jsonl.gz` | upstream | `97e0caa46c2c58ddf7f039b717326a43a7a2b105` | `d5d4b71833930b72255d8c3bd462f40e2b10a78c15fbb40991ee1b7c7116a4a6` |
| `release/certificates/mixed_n85_L9475/check2/run.jsonl.gz` | upstream | `7db420d922487d365d07a39515b50da38f768f86` | `e338e6b1e1f1332874a92222dfd99b2196c5363845b1f854ca7e7aa45089ec9a` |
| `release/certificates/mixed_n86_L95275/check2/control-197_200.jsonl.gz` | upstream | `b55baa3ed99ccde33ecbfbd41298b88031852a38` | `0625a29ffa802d7a4b58680ef4ebae4eef20e9cc5814f6ada031cba47081c09f` |
| `release/certificates/mixed_n86_L95275/check2/run.jsonl.gz` | upstream | `cfe05c0524b03357666440d0c1b15236cd142785` | `3b0ade200ee4c26aa852513f2c400a139da51e5434ede6498adb435c9e5ece1d` |
| `release/certificates/mixed_n88_L96325/check2/control-197_200.jsonl.gz` | upstream | `10cf4b826feb9ca1cff349f0211f8d51a18d2d91` | `daa8c56f78d552f2b368ec8a8bea4e302b0855d5eafa00364b7d522be7dfa20f` |
| `release/certificates/mixed_n88_L96325/check2/run.jsonl.gz` | upstream | `8ff3da38050ec1eb22c942548c12f2557598378f` | `43424744ee20569f614d3f5c3c027c7c30f4bedfc2fb1580a17dd5375f3995c1` |
| `release/certificates/mixed_n89_L9685/check2/control-197_200.jsonl.gz` | upstream | `593c12d57e027c8170435a702ba266a1e59e1b0a` | `ac28c027acb32b85ff41ffb4b63e1b5dd450aac14a84600e2fbe594cbdb692dc` |
| `release/certificates/mixed_n89_L9685/check2/run.jsonl.gz` | upstream | `126c9197e20e4aecf7c77ee42eeab2705ab8d346` | `7e0fa5eb43304c9f8354494bccde6c445f6ebb8533dae928d3055168c2807863` |
| `release/certificates/mixed_n90_L978/check2/control-197_200.jsonl.gz` | upstream | `4fdebade5a18e8af916bd8da705f5d9769c0f283` | `5800f9cf15055248cd5afaf9f5b859ab4c4ee12b4fa58ce104f636a5363ed6ce` |
| `release/certificates/mixed_n90_L978/check2/run.jsonl.gz` | upstream | `ce2b578ecae037bda02dd8b73d5bb6229b6c36b4` | `a8a5ccf54ca66e79692e55cb08fc8f8338ed6fc1ebb06ab70afe5fccf6cb10e3` |
| `release/certificates/mixed_n91_L97875/check2/control-197_200.jsonl.gz` | upstream | `6a6e872ab5e3799a1ad7566411076051fda574b7` | `ada0d6b9d5520c695d6910f6b6d7d477144c992c46608a7e376f773f58fc442e` |
| `release/certificates/mixed_n91_L97875/check2/run.jsonl.gz` | upstream | `24078c40ca92517cf2354b14d4e7acfb3f44ebf4` | `b15ead0f7c3cef944ca7a0d8227d5977e4d1a1200e4514118c9e5433f23eb4a4` |
| `release/certificates/mixed_n92_L986/check2/control-197_200.jsonl.gz` | upstream | `7456fc5efd22835d8b8da8398541c2f8fd9d7d90` | `15070de3684337a81996dc4b64090445d2ef3cf3083c12899e8b989dc8076613` |
| `release/certificates/mixed_n92_L986/check2/run.jsonl.gz` | upstream | `f415aca2d8f1e54556ad3c8b3f8728857aee8e2a` | `04c0e038ea3d570d7898aa16508664ede63b604476163986b420449a273720e4` |

## n108 Mathematical Review and Exact Receipt Audit

The
[18 October mathematical review](../../../../docs/project/reviews/review-2026-10-18-wand125-n108-certificate-mathematics.md)
accepts the n108 certificate on the retained, reviewed sqverify-fast route.
It covers one certificate; the other 17 have no verdict from that review.
The full coverage implementation shares the producer’s components.
No native verifier was rerun by this review or this integration.

The retained [audit tool](../../../devtools/audit_fine_net_receipt.py) imports only the
Python standard library.
It reads this packet’s candidate, the maintained census and control receipts.
It recomputes exact mass and net premises and all 201 saved refusal-point captures with
its own polygon clipping.
It decides no coverage between those points.
The [receipt](review/n108-exact-audit.json) records PASS for the integrated tree; the
mathematical note records the review’s separate invocation and its provenance.
The adapted source archive remains unopened.

From `packing/`, run:

```bash
uv run --frozen --group dev python -m devtools.audit_fine_net_receipt \
  --root .. --packet wand125-fine-net-lower-bounds-2026-10-16 \
  --certificate mixed_n108_L1062 --n 108 --side 531/50
```

This premise audit supports the stage-4 records lane alongside the native replay and
accepted reviews. It cannot promote a result’s rung on its own.

The current tool binds the candidate and generated binary identities across the saved
runtime receipts and requires their complete historical build objects to agree.
It does not read or gate the current verifier source, and accepts no source-digest or
Git-revision pin. Its `recorded_native_source_sha256` is reported historical build
metadata, not a check of this checkout.
Review B’s original source-pinned invocation is preserved in the mathematical note,
followed by the dated engineering correction and current command.

The separate
[maximum-reasoning review](../../../../docs/project/reviews/review-2026-10-18-n108-fine-net-mathematics-max.md)
accepts the implication and exact premises after its own five-pose audit: four of the
201 saved native control poses and the axis pose among the source’s 32 sampled controls.
These five points cover neither five entire direction domains nor the continuum of
centres. The full coverage decision remains the native replay, sharing the producer’s
verifier components.

**Control-log filename (Review C1).** The archived n108 source README lists
`check2/control.jsonl.gz`; its manifest and retained release instead name
[`check2/control-197_200.jsonl.gz`](release/certificates/mixed_n108_L1062/check2/control-197_200.jsonl.gz).
This affects discovery only.
The archived README and its digest remain unchanged.
The author question is whether the living bundle inventory can use the manifest’s
`check2/control-197_200.jsonl.gz` filename; no author message has been sent.

## Accepted n68, n84 and n85 Mac Checkpoints, 19 October

The [retained audit and read log](review-mac/README.md) inventories every reviewer
program, imported helper, PASS receipt, per-command timing file and historical source
context. Only the three accepted census rows were merged into the existing census; the
original eighteen reported entries and candidates and historical Linux n108 remain
retained. The
[packet’s census folder](../../../benchmarks/measure-verifier/census-mixed/wand125-fine-net-lower-bounds-2026-10-16/README.md)
indexes their receipts, and the regenerated
[Milestone B census](../../../benchmarks/measure-verifier/census-mixed/README.md) lists
the three rows beside every other mixed certificate.

The n68 capture’s outer exit remains unobserved after recovery, with native exit zero;
its whole-net control has 197 refusals and four verified mutant directions, 46–49. Both
n84 and n85 have observed zero outer capture, check and control exits and 201 whole-net
refusals each. All three captures verify all 201 directions.
Their authentic execution records preserve the distinct observations, actual Mac build,
unavailable direction CPU and separate native-process and aggregate-command CPU
measurements.

The mapped mathematical reviews accept these exact checkpoints.
This retention pass reran no native verifier or historical exact audit.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
