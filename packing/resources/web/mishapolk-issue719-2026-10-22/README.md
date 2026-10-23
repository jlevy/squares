# Mishapolk’s Issue 719: 122 Certificates at 12fc4667, n = 105 to 1568

[Issue #719](https://github.com/jlevy/squares/issues/719), opened 2026-10-22T05:30:47Z
by Mishapolk, asks to register 122 upper bounds for n = 105 to 1568, each the exact
rational side of a certificate `certificates/n-N.cert` in
[Mishapolk/square-packing-records](https://github.com/Mishapolk/square-packing-records/tree/12fc46678fa8eefa3f156ff37dfffd84c8f3a580/certificates)
at `12fc46678fa8eefa3f156ff37dfffd84c8f3a580` (committed 2026-10-22T06:05:07Z), the
revision the issue pins. The source was read at 08:41Z on 22 October; `main` stood at
`dc440a8804565b4beaabc489df38345cada8cad1`, whose one later commit adds only
`ISSUE_SUBMISSION_122.md`, the issue’s body.

Two of the counts are in the n ≤ 324 case corpus, 105 and 204, and one register entry
records them, pending adoption at both ([Against the Record](#against-the-record)).
111 of the 112 beyond the corpus at or below 1024 are dated beyond-horizon rows, each the
current row at its count ([Beyond the Corpus](#beyond-the-corpus)); 366 is not recorded,
below an earlier certificate; the 8 above 1024 wait on the owner.

## What the Issue Reports

- **Versions.** The issue opened with 221 counts to 4035, pinned at `1851c2c`; an edit
  at 05:35:31Z changed the credit name, and an edit at 06:05:31Z cut it to 122 counts
  pinned at `12fc466`, withdrawing 101 and adding 366 and 447. No side or digest of a
  surviving row changed. The issue had no comments when it was read. An edit at
  11:35:16Z, after that read, changed only the two credit lines.
- **Credit name.** The credit line alternated across the four versions: “Mishapolk
  (Mikhail Polk)” at 05:30:47Z and 06:05:31Z, and “Mishapolk (Mykhailo Polkovskyi)”, the
  name the record has used since issue 593, at 05:35:31Z and in the current body, edited
  at 11:35:16Z. [acquisition/issue.json](acquisition/issue.json) keeps the 06:05:31Z
  body as read.
- **Sides.** The table’s “Certified Side S (16 dec)” is each exact header side’s binary64
  value printed at 16 places. At 76 of the 122 rows that print lies below the exact side,
  so it is no upper bound as written; this packet compares and records the exact sides.
  `LEGAL_VICTORIES.jsonl` at the pin states each exact `side_fraction` with the file’s
  SHA-256 at 120 of the 122, and the importer admits each certificate at that fraction’s
  decimal expansion; at 366, which the index omits, and at 447, whose index line names the
  bytes `12fc466` replaced, the certificate’s own header states it.
- **Digests.** The issue’s second table names each count’s file and its SHA-256; all 122
  are the digests of the pinned files.
- **Checks.** The issue says Evan Daniel’s `verify_cert.py` and this repository’s
  `sqpack/verify.py`, run from the author’s copies under `tools/`, accept all 122 with
  zero tolerance. Neither copy is in the pinned tree, and no source program ran here.
- **Not claimed.** No global optimality, local rigidity or KKT condition.
- **Lineage.** Each row names a baseline holder, and the closing paragraph credits the
  finders the packings build on: Erich Friedman, Joshua Levy, Evan Daniel, Francisco
  Couzo, Nate Chaoweeraprasit, Robert Barnett, Daniil Ostashev, Frits Göbel, Joost de
  Winter “and other contributors”. No row names its parent packing.
- **AI assistance.** “Gemini assisted with solver scripting, precision checks, and
  formatting.”

## Source Custody

The tree has no licence file and its README states no reuse terms. Under the derived-only
form of the [existing retention policy](../known-best-packings/README.md), as for the
author’s packets of issues 470, 573 and 593, this packet keeps no upstream byte. No
redistribution permission or licence determination is asserted.

`devtools.acquire_source` wrote the custody record from a full clone checked out at the
pin, from [acquisition/declaration.json](acquisition/declaration.json);
[acquisition/sources.json](acquisition/sources.json) is the record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest.
Its scope is 173 files, 14,943,057 bytes, every one pinned by digest and bound to its
Git blob at the pin: the README, both victory indexes, the 122 claimed certificates, and
48 more certificates this packet answers for without importing them ([Not
Imported](#not-imported)). The other 437 of the tree’s 607 certificates are pinned by
the commit alone, among them `certificates/n105.cert`, a second 105 file $4.64 \times
10^{-12}$ above `n-105.cert`, which the issue does not name.
[acquisition/issue.json](acquisition/issue.json) keeps the issue as read.

## Derived Facts

`devtools.upper_bound_reports` read the 114 claimed certificates at or below 1024 from the
checkout, after `acquire_source` showed that the checkout yields this packet’s record, so
the bytes have the digests the manifest pins. It wrote each as an exact rational
`center-basis` Witness/v2 under `facts/`, naming the certificate’s SHA-256 as
`revision_sha256`, from the declaration in [acquisition/report.json](acquisition/report.json).
Offline, each fact must rebuild itself from the certificate it states. The 8 above 1024
are pinned by digest and not derived until the owner decides whether the record tracks
those counts (think-f2io, think-9vr8).

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes each derived certificate
against the record at `main` `0281e7763` (22 October 2026), and `check-claims` rebuilds
it.

| n | Exact side | House | Below the house by | Also below |
| --- | --- | --- | --- | --- |
| 105 | `674331486483935962030285457609/62500000000000000000000000000` | T-174 (PingYou Ltd after Couzo after Xu) | $5.18 \times 10^{-12}$ | #593’s 105, the same packing, by $5.18 \times 10^{-12}$ |
| 204 | `882663895519250432/59604644775390625` | T-225 (Daniel after Couzo) | $1.006 \times 10^{-8}$ | T-223 by $1.145 \times 10^{-8}$, T-228 by $1.54 \times 10^{-6}$, T-226 by $1.59 \times 10^{-6}$, T-186 by $2.04 \times 10^{-5}$ |

No earlier certificate states either side. Couzo’s copies of the house sides, at
`4e4c8ce` (105) and `5a299b4` (204), equal them. One register entry records both, at
V0/C0, pending adoption at both counts; it lists each as a regularization of the house
packing it re-solves.

**Pose by pose.** [measure/identity.py](measure/identity.py) measures each against the
packings the record credits, with the measures of the
[evand-regularized-2026-10-20](../evand-regularized-2026-10-20/README.md) packet’s
identity program, and writes [measure/identity.json](measure/identity.json). A
measurement, which decides nothing:

- At 105 nearest centres pair the squares one to one with T-174’s packing: 42 move
  beyond $10^{-3}$, none beyond a tenth, at most 0.049, turning up to 2.41°. The author’s
  own 105 of issue 593 is the same packing at this scale, and measures the same.
- At 204 they pair one to one with T-225’s and with T-223’s: 67 move beyond $10^{-3}$ and
  6 beyond a tenth, at most 0.273, and every square turns less than 1° but one, which is
  re-oriented by 25.64°. T-225 itself moves 4 squares beyond a tenth of T-223’s, at most
  0.442, which the record registers as the same packing regularized. It does not pair with
  the author’s own 204 of 13 and 14 October (T-183, T-186): 14 move beyond a tenth under
  an optimal assignment.
- #719’s 105 has 43 tilted squares and its 204 has 77.

## Report Order

The repository is watched, so its certificates are reports from their first commit
([receipts/first-commits.json](receipts/first-commits.json), from a clone of the
source’s 55-commit history): `1851c2c` at 05:29:48Z for 121 of the 122, a minute before
the issue, and `12fc466` at 06:05:07Z for 447. No other report reached this repository
at these counts between those times.

`devtools.beyond_horizon_replay earlier` read every certificate and index bound in the
histories of Francisco Couzo’s and Evan Daniel’s repositories published before #719’s
row at each count, and kept those strictly below the record’s standing side there
([receipts/earlier-publications.json](receipts/earlier-publications.json)). Couzo’s
three commits after `7b6c87e` are dated by their push, at 2026-10-21T22:56:37Z, as
`devtools.couzo_715_replay` found. At 60 of the 122 counts an earlier publication is
below the standing side: `4e4c8ce` (15 October) at 42, `23aff0c` (17 October) at 447, and
`5a299b4` (pushed 21 October) at 41, 33 of them at or below 1024, among them issue 715’s
re-certifications, and the 8 above 1024, where issue 666’s and issue 715’s rows also come
first.

The [ledger of 22 October for issue 719](../../../campaign/issue-intake/upper-bounds-issue719-20261022/README.md)
walks them in report order from starts frozen at `main` `0281e7763`. It records 121 of
#719’s rows and not 366, where Couzo’s `4e4c8ce` certificate `certificates/best/n366.cert`
(15 October) is $8.19 \times 10^{-2}$ below. At 51 of the 111 beyond the corpus at or below
1024 the report the walk records just before #719 is one no row yet holds, each its own
import’s: Couzo’s `4e4c8ce` certificates at 19 (think-yfoo), issue 715’s
re-certifications at 19 (think-fwa9), and `5a299b4`’s certificates at 12 and `23aff0c`’s
at 447 (think-tmwt). Each enters below #719’s row when it lands.
Since 22 October 2026 the [history walk of Couzo’s watched publications](../../../campaign/issue-intake/upper-bounds-couzo-history-20261022/README.md)
records them where they were first: at 49 of the 111 the row just before #719’s is
Couzo’s own, his `4e4c8ce` index at 38 (couzo-index-2026-10-15) and his `5a299b4`
reconciliation at 11 (couzo-reconcile-2026-10-20).
The re-certifications below the 12-place print, issue 715’s and `5a299b4`’s, stay held
(think-fwa9), as does `23aff0c`’s bound at 447, which deletes a square from Friedman’s
classical construction at 448 (think-f2io, think-8krd), and the chain
passes over them.

At 631 #719 is $2.73 \times 10^{-13}$ below Couzo’s `4e4c8ce` certificate and issue 715’s
re-certification of it, and all three round up to the same 12 places, 25.656854249519.
The rule compares exact sides, so the row is recorded, and every row of this source
records its side rounded up at 16 places, where all 111 differ from every earlier side.

## Exact Replay

**Beyond the corpus.** `devtools.beyond_horizon_replay` decides each of the 112 rows
beyond the corpus at or below 1024 from its derived fact with the filtered two-route
decision of `devtools.couzo_678_replay`, reused unchanged: `sqpack.verify`’s predicates
and the independent rational corner checker’s, over every wall and every pair whose
centres are closer than $\sqrt 2$, by exact comparison, with six controls on each
certificate. All 112 pass both routes, and both routes refuse all 672 controls
([receipts/filtered-exact-replay.json](receipts/filtered-exact-replay.json)). The
replay decided 164,280 of 25,394,281 pairs, 160.2 CPU seconds for the positives and 27.3
CPU minutes with the controls, in 845 seconds on two workers on 22 October 2026. No
square touches the box and no pair touches: every wall clears by at least
$2.02 \times 10^{-13}$ and every pair by at least $4.04 \times 10^{-13}$. Each print is the
binary64 value of its exact side at 16 places.

The maintained all-pairs kernel of `devtools.evand_arrangement_reports`, every pair and
no filter, decided the positives at 447, 652 and 997, one of each margin class: 808,413
pairs in 401.2 CPU seconds, both routes accepting each, and each least pair gap and wall
clearance equal, exactly, to the filtered decision’s
([receipts/exhaustive-sample.json](receipts/exhaustive-sample.json)).

[receipts/goebel-comparison.json](receipts/goebel-comparison.json) holds every decided
side to Göbel’s classical squares and strips, with deletion, using the 15 October packet’s
retained program: 111 are below, and 366 is above Göbel’s strip at 369, $19 + \sqrt2/2$,
by 0.0317.

**In the corpus.** 105 and 204 go through the same kernel by the declaration-driven
importer `devtools.upper_bound_reports`: a positive job, a duplicate-square control and an
outside-container control at each count, each in its own child process. Both positives
pass both routes, and both routes refuse all four controls: 156,996 pair decisions in
22.55 route CPU seconds on 22 October 2026
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz), every
deciding input and both routes’ complete outputs). At 105 every wall clears by at least
$5.00 \times 10^{-21}$ and every pair by $9.99 \times 10^{-21}$; at 204 by
$5.0 \times 10^{-13}$ and $9.98 \times 10^{-13}$.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method. No source program ran here.

## Beyond the Corpus

[acquisition/beyond-horizon-rows.json](acquisition/beyond-horizon-rows.json) is the
record the source register reads the 111 rows from: each row’s side is its exact side
rounded up at 16 places, with the issue’s print beside it. Each is the current row at its
count and supersedes the row that stood there: 42 of Darius Muglich’s #686
(`muglich-issue686-2026-10-19`), 39 of Couzo’s `487b058` index
(`couzo-verified-bounds-2026-10-14`), 16 of Couzo’s #715, seven of his #678, three of his
14 October certificates (`couzo-certificates-2026-10-14`) and three of his #670, at 370,
452 and 536, and his 8 October report at 372. The margins run from
$1.28 \times 10^{-12}$ (339, below #686) to $1.39 \times 10^{-2}$ (447, below `487b058`’s
row, which is above Göbel’s construction there).

## Not Imported

Each is pinned by digest in the manifest, and the reply asks the author about it:

- **Ten withdrawn rows.** The opening body claimed `certificates/n-N.cert` at 411, 451,
  494, 495, 539, 540, 583, 587, 632 and 683, which the triage found below every earlier
  report by $9.3 \times 10^{-13}$ to $1.14 \times 10^{-11}$. The 06:05Z edit withdrew them;
  both victory indexes still list them.
- **In-corpus files below the record beyond the twelfth place.** 34 files, mostly
  `nN_tight.cert`, at 17, 28, 37, 39, 41, 55, 69, 71, 83, 87, 106, 110, 128, 129, 130,
  146, 152, 154, 155, 156, 176, 177, 183, 205, 211, 235, 236, 241, 264, 271, 300, 304, 305
  and 308: in triage 17 measured below the house by $1.1 \times 10^{-70}$ to
  $1.8 \times 10^{-19}$, and 17 undecided against an algebraic or catalogue lane. The issue
  does not request them; the owner’s question think-fwa9 is the same at a larger scale.
- **Three files that failed both exact routes in triage:**
  `certificates/n-133_breakthrough.cert` (squares cross the walls),
  `certificates/n266_fresh.cert` (33 overlapping pairs) and `certificates/n275.cert`.
  Neither the issue nor the indexes claim them.
- **A second 204 file.** `certificates/n204.cert` is the same packing as `n-204.cert`,
  $1.48 \times 10^{-11}$ lower, and passed both routes in triage. The issue and the
  indexes name `n-204.cert`.

## What Is Not Established

A finite packing certifies an upper bound and nothing more. No optimality, rigidity or
KKT statement is replayed, no arrangement identity beyond the measurement above is
decided, and the source’s checkers were not run. The entry for 105 and 204 awaits its
stage 4 review (think-4h23); a beyond-horizon row owes none.

## Credit

Mykhailo Polkovskyi (Mishapolk), the name the record has used since issue 593 and the
issue’s credit since its 11:35:16Z edit. At 105 and 204 the entry credits each packing’s
finders first, as a regularization: Ryan Xu’s packing as Francisco Couzo and PingYou Ltd
refined it, and Couzo’s packing as Evan Daniel regularized it, which Couzo’s source
credits to Polkovskyi’s own construction. Per-row lineage beyond the corpus is not
stated by the source, and per-row credit beyond the horizon is the owner’s open question
from #686. The issue discloses Gemini assistance.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source mishapolk-issue719-2026-10-22 --check
python -m devtools.upper_bound_reports mishapolk-issue719-2026-10-22 derive --checkout CHECKOUT --check
python -m devtools.upper_bound_reports mishapolk-issue719-2026-10-22 check-claims
python -m devtools.upper_bound_reports mishapolk-issue719-2026-10-22 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports mishapolk-issue719-2026-10-22 check --replay
python -m devtools.beyond_horizon_replay first-commits --issue 719 --clone CLONE
python -m devtools.beyond_horizon_replay earlier --issue 719 --couzo COUZO --evand EVAND --source CLONE
python -m devtools.beyond_horizon_replay ledger-sources --issue 719 --read-at-main 0281e776342f2f1b63d3df66dc3c1737e8202945 --read-on 2026-10-22
python -m devtools.beyond_horizon_replay check --issue 719 --replay --workers 2
python resources/web/mishapolk-issue719-2026-10-22/measure/identity.py --out resources/web/mishapolk-issue719-2026-10-22/measure/identity.json
```

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `facts/n-105.yaml.gz` | receipt | `a68aa84df684dc678aea2bf177a7b18c8b73f0f8` | `09ef4b6e1462ccf23dd69a1cfbe443bd827d0f52629141346c65dca101166cbc` |
| `facts/n-204.yaml.gz` | receipt | `cdd3d59021bab353e2ba86fab7dbc560dd75836b` | `c122e34b6c34e25a671551b58c4fcd1857c8725ea8d2db4cf43fc22040c68621` |
| `facts/n-330.yaml.gz` | receipt | `8e74e40164d453954a973ce49d4b58247dac3378` | `8ea5f5be7b23a8a1c42107e610763f7477d6e39c86f6ead364f6d4bbff3e82a5` |
| `facts/n-339.yaml.gz` | receipt | `082ff59afe9840c599ae8fa6cac01f46d709c624` | `111aae2a06b896fdab0ac859467ec73197b60a6d4a1ee12eb51d817219d9f5e9` |
| `facts/n-342.yaml.gz` | receipt | `91966cdd99fd1facb8f1f4e817d0300eff42bed8` | `c1cdde1aa489157bd012d9b5ed0ed4d7044cb3e961f58ea06649a92ccc270877` |
| `facts/n-344.yaml.gz` | receipt | `dc1b7edff9cdf5c5eb68b2e03e9d5bc91efd9bd8` | `38866dbf987f4ffaf102ec05b579a1a08423cc41c3ead557ef6828f048d80146` |
| `facts/n-366.yaml.gz` | receipt | `200b1e68619d43a4264f1599e67ca4ab240ac169` | `2079b3b6b9787332ca8102cc3b0f42878a8985382519678544941903fe06e20c` |
| `facts/n-370.yaml.gz` | receipt | `0b4de4eb2c5acea586eb03f0d9e809b3d308978d` | `dd3c6de6e17b02297844e9e3c4fcf4bbf05192860e456efe9c939aa254c4395d` |
| `facts/n-372.yaml.gz` | receipt | `debc92e789953239723b2370ff65bc5f3d871537` | `5c4f5f7f9835f2e4ce574713139e052072508a6753a2ceaf66ea5274cd566e4d` |
| `facts/n-377.yaml.gz` | receipt | `e0d1a1173b446e02e6a166569e6373561c839fe1` | `9c3d2ea47b9087e284c514cbb586f77c693d2fc6799e5604dd22240b2e8135c1` |
| `facts/n-378.yaml.gz` | receipt | `c3434e33642200783d93eb4ec22d3d39772ea24f` | `7af130a10016d0338509dc75eac154dd12fc481e78196515507cf7f157f353ea` |
| `facts/n-379.yaml.gz` | receipt | `be6e63085096cb5b03b08150eca749af8d97c798` | `a8142a77c6c852cc7f6be90782920e0b8b55347d61509f94bedabf9825965eac` |
| `facts/n-380.yaml.gz` | receipt | `848127fba6dedd4b80723ef5bcedf884b7c6372b` | `5306c30c33280c4a517a5e4e882616d76bd28cd9e282206fbc4e68c51464dcce` |
| `facts/n-381.yaml.gz` | receipt | `89457b1461707aa73aacfedfb443253e8a320766` | `0505d880e49b8d999ff0a279a312b6afd7cce4040ac98941ed0316902f2f7a39` |
| `facts/n-409.yaml.gz` | receipt | `9989c764f351647932d100597ef7fcd55d3657cc` | `ad419100104db687f006f03422d199e39c4f387d13b921df9a5c1c4afa6eab93` |
| `facts/n-410.yaml.gz` | receipt | `05072e826a1018edd5facbebc928ab009ec5ae3b` | `b840278c354e6c461b5e9a255cc2cc591800de33ebeb5ae4cc7890310d9267a5` |
| `facts/n-412.yaml.gz` | receipt | `c5ac47de0546e439c3dc712ff10f5eef1db0007d` | `6d49eca7e0fdbd76a1070312891d5622866284024efb91ec9683ee78dafb476f` |
| `facts/n-413.yaml.gz` | receipt | `ffb6ab7e5658aedcb91577b6a1ed276a4cad8169` | `6b3ff3dff05cbd74438dcc0524af880c8dd05c31d582539682310889d4b5abf3` |
| `facts/n-417.yaml.gz` | receipt | `55f6dc7348f7bac35919b2d9c52692b3f41c727f` | `71e5f74001a89aebb63a14f202a5807c8dbbcf3a70c6e8a65454ea86ef5b0a96` |
| `facts/n-418.yaml.gz` | receipt | `c9a647d83a44211f9664d489106db6447b110d2c` | `ee337ff4da4461de0818c09cd4596284f39c6b30089e5ebada2dde9541bd1d36` |
| `facts/n-419.yaml.gz` | receipt | `a1c052039f3783270cb182ac93b82c43edb75499` | `652ffa2b4a6b0ee58d1692366c2e1e3ffda59d9202e7e93474b344cbbad38e8c` |
| `facts/n-420.yaml.gz` | receipt | `1c7773d0b94a2914b8d758abb87d2057949c67a9` | `77412697797c8c217355a64126a92b8102edcf6bc2781f7be38bf9a27767fb96` |
| `facts/n-421.yaml.gz` | receipt | `b05958512360f3f1d6eb1d3612cd032cadfb1e23` | `73a977b5c4326a64cd74f0f0e6662cadcb68a1d6f425469afff2e8dc7356b201` |
| `facts/n-422.yaml.gz` | receipt | `56308ed98219d285e103cd1551221b9a5b951875` | `fdd0dc1d9d3e63f8ffda31b8a365ea584ddf7f95a167de948428cd55f101e879` |
| `facts/n-447.yaml.gz` | receipt | `d3189ee709b178229beaa3770912d7033958c06a` | `eab7017cc3965f83bf0243bf4aff96de776190c2db7427fe35174dab45f5dba2` |
| `facts/n-450.yaml.gz` | receipt | `a99fedbb8d32c2687466ac9ba60b5331560ac342` | `292b6038c15b787deff8f3e6d462e22bb70d987bc1b30d6111162654c7cd8c21` |
| `facts/n-452.yaml.gz` | receipt | `9c1b377483e84d3ab87856f85dcbfcf487cd5b08` | `d3f93644658fb1b49df4d5b2b4ca5ce9cd30ccc003d335f528e6d66c5cbb0627` |
| `facts/n-453.yaml.gz` | receipt | `5209963bc37bc442328411f81d4f4dbf0d696f78` | `e3b51b07e40ae517109d9c178f960c5a17b2b93716c1c4db7072640f530c4c5e` |
| `facts/n-454.yaml.gz` | receipt | `b6002a179248f5922b4e4264a505f854ce7f9a48` | `7671de39f6cc53eb35e3a750533662174c1adedd9badd66a96ff558455d9b219` |
| `facts/n-456.yaml.gz` | receipt | `42a4417d957f12477aaa238b89b71e43997d70c8` | `4d51f9618930c8fbae9dac4fa3fc14d060b317becd1469fd6a995ae381d8b86c` |
| `facts/n-460.yaml.gz` | receipt | `7bf1906cb149289d764fb9c71796e2f083798ac8` | `808c36be5c8f78bd4a7abc4d3f92588bcd729ef594b81e592c216a7712fb8b7c` |
| `facts/n-462.yaml.gz` | receipt | `2959c3248b2c6511fe6a21a99a9d1b45e5b8f429` | `2836cfdccf527b1a358d5763f5f9e11a3e99e8e87f6f16070dec29694dd2f2e9` |
| `facts/n-490.yaml.gz` | receipt | `10713c730b6ddf31d2baf9e268e0fa8deed10dce` | `5a53120006394dce940b43ba942f829e9da145e9ced447fc8f18803302244b50` |
| `facts/n-498.yaml.gz` | receipt | `ec009051340c2a74ee0c0560ed95a6788e05a602` | `3fa276d77a1ebf1256745fd038bcb73e48ac94247e33f6285fcc68736550c84d` |
| `facts/n-499.yaml.gz` | receipt | `88427ea3b1c279693baae9ead21c7096a15b9824` | `5f9cc169ddbf896248e700a2d59fae0622c09fc8438ad6d2e8614a81eefdbf3b` |
| `facts/n-507.yaml.gz` | receipt | `f60c9c9fa6076c1e4651f321d021ba3182f9b80f` | `e61dc09a8f28aae87d7182e6b2bf4862cdf964221d29e90c20fe0cc47590d64e` |
| `facts/n-508.yaml.gz` | receipt | `eeaa6c57d56b950b7cdb54e248886f118defa8a3` | `eec3119eb5c82d86c909ae5e283215bd8f79b1f3b6a825a72e064a4377606287` |
| `facts/n-535.yaml.gz` | receipt | `d69f09438f1a3d242045068d28f85b0bafe72094` | `4845d84c2a9f432bf89f87a10933dd6df5ef86ce4d09525541c51f9068c26dd6` |
| `facts/n-536.yaml.gz` | receipt | `f4c37d1feaa336fc4a71707c20c685ee95523b74` | `f7cf280eb089aff4f5e28405dd2b4d814dd636951392d8a2ca6efbd737234aa8` |
| `facts/n-544.yaml.gz` | receipt | `49efce59683741ae7eaacd6a0bea52d46438a171` | `673b05c3ff8eff301d4d9c1077a88a5840c215190c1edf8ae6da13592d2de979` |
| `facts/n-551.yaml.gz` | receipt | `acbec0841fb58f6563666145f416602f186b0eae` | `f883b8f560580c8bbf3b8fcb3268337d017fed59bdc1d294380702213ae12a7a` |
| `facts/n-552.yaml.gz` | receipt | `86b370f6d0c070c887b4a4de0837856fa0bda9cb` | `cb1af90773634be0ed0ec993cec0863f08dd28a1df5ba9ae8f9b7563d11268a4` |
| `facts/n-553.yaml.gz` | receipt | `a6df6f00e13e57b86177df01389cde58299e0950` | `0cecfaf102c743e29d298bb6fc930f47c933bd6c7c2f90f5eafdd8b930484b77` |
| `facts/n-555.yaml.gz` | receipt | `0ae84b9cb8f95f4c12a3f141db417cf77f5ff924` | `5e278e4e1118df09fa5d7131d45efa1bfb597db244884b538d4e0bec80f2e417` |
| `facts/n-582.yaml.gz` | receipt | `8d70e3b989cf12e2d3ec1ae6170a2c5036981a15` | `1b10536e834a9417e4c098e61e064d18cf27286f9d4045dd39d2056bd7790726` |
| `facts/n-584.yaml.gz` | receipt | `3a1157537b53298682e0a56107ad5a693fa24ecc` | `255a13a47dc3398de12fd966ac73d8a80d397f82f9fb25532a30188d452810ea` |
| `facts/n-591.yaml.gz` | receipt | `3b671fba06f6b70d6aa2d22d39f063247e520b8e` | `bb148a44219c9637da326604f5a01e47bae3c561dd325fd2861933911c06fa56` |
| `facts/n-596.yaml.gz` | receipt | `0e43fa886356a51c913db9ec1e58f87c2de928e7` | `efb7110ce1ea4f1017b3b4348f7244e5d8cf356e97c1938e80e2aaca36b84feb` |
| `facts/n-601.yaml.gz` | receipt | `f017f668d00a5062238fb90b537f9e761b82713b` | `84fc7b7578daa84239fed8dfbba1d76e29b5a1bbf5d984bfce9309ee813ad849` |
| `facts/n-631.yaml.gz` | receipt | `1fa8ab6559ba284c36fc1f0b9893630df398bd9f` | `b1734bc81148d16e0ab91177d326f8a5527c70a4d1521ecc507278c3343ca92a` |
| `facts/n-633.yaml.gz` | receipt | `157847402c7c1b9cd848e1a60088fd6a9ae2b372` | `12f73282e909cbd89b7a927687c3fdafccbb385b96904cdac15c85c242ba7c94` |
| `facts/n-637.yaml.gz` | receipt | `927c8d07c7384f9058e6ae32d0a59f05aef775c5` | `fcba1748363c4710527ea925a52b0eca1a8e7038d978b384e42f60e41b5648d2` |
| `facts/n-640.yaml.gz` | receipt | `361c4ddd7b7a79c4c55480d1f578203ab254737a` | `5be12848c3e520478d2e752021237dba8b335ebea6e75c3fe0d7e0ddc6451a7f` |
| `facts/n-641.yaml.gz` | receipt | `1391acc0a653eea9a8684a5a65c6e412d05929e7` | `fc0ce3a86b85c21272a54dc5bf6bd03c2308338daae2e5857140d89bd4e5a2de` |
| `facts/n-642.yaml.gz` | receipt | `0bae729da80bdbf2f96f1e39cb7a43cb7395c80a` | `b87cd3a6661b9e1c3b6aa7a5c0a9d8c2ea6f10e3bd2e0a4111340a8d2764eac8` |
| `facts/n-644.yaml.gz` | receipt | `da22d4d42ed462d16c6cc2e1b00fdd6f800b3c70` | `6234f7f5b137272f9cce8334f123957f435480c1b2c584976b9a1b0fc64ae076` |
| `facts/n-649.yaml.gz` | receipt | `a768b6bb4b5760dbc8a200fe2c5eb82435aa1f73` | `4ed669a568c9ad94704707d5d9590b060153c0873d67a108c0dcd987d8457c06` |
| `facts/n-650.yaml.gz` | receipt | `bd6f5c37db34699deb3e4a3e80c802b7806de309` | `b4a2854057e5626cc14b83184f3f846f230afb53aefb8951a44498795a0ef90b` |
| `facts/n-652.yaml.gz` | receipt | `1ec222bb93a17605e1f92f424574fb44069670a4` | `4f9d5e5ed705f4bb305daf79143a6f026154b22e6544ce4ad0134dde00200f09` |
| `facts/n-682.yaml.gz` | receipt | `03cb7b42fa747f3417f3ff9507f97e8d9c057184` | `c386182d4dbb445a24ced06fbaf613f5cd335649869405dcf46cf76724cbd0c2` |
| `facts/n-684.yaml.gz` | receipt | `836f184ffd9ba2e025d03783704f1f086823096f` | `37055969f3dbfe416f47947d57a3233b1f548443b0ab59ef83e1e44fb6438a27` |
| `facts/n-689.yaml.gz` | receipt | `98b6fc124c692c8a27cea692b013a90240598a78` | `9435d69ce812fceb463bccd3909dd621decc15c64702afbf65d2abbb2eb790f1` |
| `facts/n-691.yaml.gz` | receipt | `e943bef992981793037f07d41c1d9eec4545f9cf` | `2e8bb0019d28a7168132dcb37fb7496c84493be4f6da27356522aacc76f19fb5` |
| `facts/n-692.yaml.gz` | receipt | `d34979affc4d2296288d41c051f5e578fa2f7bc4` | `82edad2b1eaefe38b41737d303837b05b86e83a71a59725e826b0faca2f566e7` |
| `facts/n-693.yaml.gz` | receipt | `d8a3756aa3b9e225b5acc7147b5c984ff776b020` | `1152532f89f69712be5f81bc705adc49952bb9f3cc20b1e0718991ca6dbe6249` |
| `facts/n-695.yaml.gz` | receipt | `233ea74b07d367c8bdbe2730bac98d1bf69bace9` | `33cb57be71218af373fcf55589880be9f15c9b0317796dfab13a97e347ee81ce` |
| `facts/n-699.yaml.gz` | receipt | `d7a0f28395b10dabd311ff0504e07ec9743f8d01` | `00757dff9f0520c476d61c14cefaa8bf5553db6cf39e9af5f6614d98f18d5479` |
| `facts/n-701.yaml.gz` | receipt | `a887ac7cd9de292d2c8c311c6bfa1ad9dd4dab5c` | `e409af346f9426383704e7b2436b9e3ea51d881e13f7da3349e48108a0c55887` |
| `facts/n-703.yaml.gz` | receipt | `3a56991e01417e917dcbe257cd1607bc447b0474` | `acb49327a310ea3c56ecd39eef507accde47001b73e8e0b93129c3d02b671a3a` |
| `facts/n-704.yaml.gz` | receipt | `0955cb491ceb031723f003a175526f751068880e` | `049e4a56c26845b2b5ccc9f7259e03e3890739cce14f5208c4c2d9353348c838` |
| `facts/n-705.yaml.gz` | receipt | `b10f8d4893d244c9fb87c20145473e442d0fa707` | `546d93179169cebd961961735b84f30d26a57fa8f20dd90d8678f637a53f3550` |
| `facts/n-735.yaml.gz` | receipt | `b3048373871522c51c9815d4afaed0529bbbffc1` | `faa7ec699299f53a7a08a69065c1ade73147250eabffe1ed3d64dfcd4c2c0e55` |
| `facts/n-736.yaml.gz` | receipt | `729c5fb88b89faf202d14ebb1eae77690cf71918` | `79b124c71aa26f7b4cb5c8927db32a2a5b7943a0f9e7ef754db0186824f63377` |
| `facts/n-737.yaml.gz` | receipt | `67f3625fec432ae7f658852e7f81e0140053f408` | `e085e57ddfd5785c182d86322dcc15072a329ad276747dc1e1171b5d7ea1c08e` |
| `facts/n-742.yaml.gz` | receipt | `ab01e8fa1605a129f5ff745f6f277aa2b5824555` | `4bdf47504fc1120a6d314e15abb5ca7d8e84542e6708c569344012658ea0b19d` |
| `facts/n-743.yaml.gz` | receipt | `d6d478b135f19d2b90dbbb47094d531cd48eed7f` | `26abfcb60563cabdda8a5926bad9cdae879fb0d657bf1865ffc575217dfbcf1e` |
| `facts/n-744.yaml.gz` | receipt | `e6d710d81a1c702cdcb8a004ba3e074ad7773c53` | `23e84654b82d051d4a39900798b07a6b5ebaef31eee0633900955a27d957890f` |
| `facts/n-745.yaml.gz` | receipt | `1d6be4ac37c5f6bd62c0700dec6b23e7897c1f0c` | `9e75e130a6dcb3f50d9d4666edbbd5098df18422a436cb1400a06b0a54790ae8` |
| `facts/n-746.yaml.gz` | receipt | `0afc8b99d5f6661321f91a417fc1874ed4a6c25d` | `8086bed082dddfb3c6fff5da5dba023341e8cc2e5ee009a497385c2f88854ec5` |
| `facts/n-753.yaml.gz` | receipt | `0c025637705ea3c39c99ab74fa5ebb4a2321fd7a` | `b73a64f77231adb973f1f29de7a6d94094a1fee9aba0d7eab1bef8baec69a833` |
| `facts/n-754.yaml.gz` | receipt | `9c0d84a2fd3f39b6ea025cdf73438294ae6fa59f` | `6218a2489dc411952c5e6ac90de13c3bce943e9657ce509601aeaaf61a8b6c00` |
| `facts/n-755.yaml.gz` | receipt | `29c84bdaf7e6b8d04385887a6b55b309fe3cdb76` | `e8408a5021352410429a01331d54a8a7e53c85f6c1f34136b092e684b43b277a` |
| `facts/n-757.yaml.gz` | receipt | `e98d6757a103362571e945668aeb98ecf737533b` | `0481e9356a7ebb41a5f18fc7b539add9b57f88e0d204c4b14295708bf791f348` |
| `facts/n-758.yaml.gz` | receipt | `c20279d80b8c8873dfe99b79d46991067e2657de` | `e1fc38edcd4734b3cd6a1f4f090dde5472dfe47bfadd147c8fea5d5b46a7c223` |
| `facts/n-759.yaml.gz` | receipt | `8aeb6d0aeb14955d3bd27ad42d89d563ed371695` | `b6c310286d94dafdbee8375f62286de1e0edd5ccfc51bed9d0e8ff361f6de1f0` |
| `facts/n-790.yaml.gz` | receipt | `2e670aabb00386ac4254471cee34dfc99374ac59` | `9596eda928773847b81277719b8e7139b530b0a71f1ef0126ba26865a22eb3e0` |
| `facts/n-791.yaml.gz` | receipt | `bb17d7678ad15e8c4740adcb5d5f5ec86a6cd11d` | `34ef032a07e4c11567007798e57fcd5d46093e0a5f14f44ec6613aac49b0673d` |
| `facts/n-792.yaml.gz` | receipt | `030fc4ef77af95037b309c5b263f213e9178fdc5` | `4b9c9c3ab2a8e8a4be64b4985386f2382e569a2c599dd5f0ccd6ab57c4f44c5d` |
| `facts/n-797.yaml.gz` | receipt | `6e49e2c05fc5d7aa5fc84e3ff9d57cd15e492cbe` | `ecaa2b0bd2ac950faa9bd978e2c4f3f22a9af57ccfd3a066f95c1cfed0a59d50` |
| `facts/n-798.yaml.gz` | receipt | `f8b7c62441aac824f71c69468173bd483ae1ab46` | `e917c2bc48015a0341bf9337caefc7ca5b450e568da0c36e1e85d18a626e08ae` |
| `facts/n-799.yaml.gz` | receipt | `8d99a1d2c6cbf7b3247a0079c949e33c7d43eb83` | `b275c13152a9dbea9eb47d47ec79e2404b1617d515a427164f53d56a2cacddf4` |
| `facts/n-800.yaml.gz` | receipt | `676b7b632595d034abac728d49bc73009721d7c4` | `3841029cefaeab85e75a6dd5136bd0f3f80f0907d9c4d555ecb492221359e3f0` |
| `facts/n-810.yaml.gz` | receipt | `30bd405a6f293d805c1d547beed4f16d5bb71eb8` | `7fe9b63b84c4d541379ef9c8dbf74b63e1244e933df3edf9d4731b312a4a5b43` |
| `facts/n-811.yaml.gz` | receipt | `8f83542c768189270072bf80e3e73e59a94f6be0` | `fa93f7c6b94781cefcd7a0c27b4adad1cfec74c4e3e74d10bdaad374fb5bd760` |
| `facts/n-812.yaml.gz` | receipt | `4263ceaf2769110c38ee4c27ecebec3598f0ade6` | `fae4f508dd327ad31063a4f43b9a0516447b8b09782dba472e108af50512b63c` |
| `facts/n-816.yaml.gz` | receipt | `429bdd905351ba193ea8ac92c36b493507daa350` | `dc51b4fd8493b70b8265b987ae969529cbfa1885f46a84c4fe6fb387b2d2e055` |
| `facts/n-868.yaml.gz` | receipt | `57486743641cd91901e5a13812725c4c18f9d489` | `5058385c5a9149b34d92045ad3eb710035324e5fb4d6d187e9bdec84ef33d4ad` |
| `facts/n-869.yaml.gz` | receipt | `c1f534487e7709b4b550c479f11c64b0e968534a` | `0a3cbd912657d486243100d1ef0f9453401c80cdc59e91866acf6c2e7228016d` |
| `facts/n-872.yaml.gz` | receipt | `06cc688b7e083cabd64ef97b83a62f2243747dd2` | `09bcfaa937d6b82c207bf8dd0678e7888ebb24f671b5826571b5fe7bf28d3a70` |
| `facts/n-874.yaml.gz` | receipt | `313df8cdc00037e91266216f496495f751e36afe` | `01e5afe06868e40a61720b7ec3cac2d05233fb09896dd4a97f04a88c540155ff` |
| `facts/n-927.yaml.gz` | receipt | `993d3ef6037d641a11faaf41bb8908edf122880b` | `fb6aa6d49045495578d6200925c278a5d5028923b04f4bf7add2b99771cc43fa` |
| `facts/n-928.yaml.gz` | receipt | `827179d140d4d9d779e5c4f62eaff3fbeb77cbae` | `ea662400469cd05710e98a82834e5063061dcc7b08490d0dee6c575d95d66512` |
| `facts/n-929.yaml.gz` | receipt | `eaf5a546a51994f59081aef1b06ed0787d298ce5` | `872cc9b5aa92ce1b47303ad05df27225498b098049734183c9fe0d532349a012` |
| `facts/n-930.yaml.gz` | receipt | `302e5ceeb8b1cbe3945f406680c39668edc92285` | `e012d42f1e80a5a71849fd759a4a46b40a48ccd978e0cbee2e287676cf0e90fd` |
| `facts/n-932.yaml.gz` | receipt | `c9fe89117c6f36b655f26df305b51877dbd7c07d` | `9d6ebe80913d6606e704aa4d772b0a70af137a04f503ea4a4bc7c1010f966390` |
| `facts/n-933.yaml.gz` | receipt | `a454fdc5e592a168b861fde538a5ef47caedf775` | `e516ca4c174097eec854965c939dfdf21c03173881ea783c2afcd64ac8fab487` |
| `facts/n-934.yaml.gz` | receipt | `d272e92d7cab3217d105382fb585dda699aa6386` | `7a91b64cdad4220a5b2abffd7b3d2a55aeccce2241d543af1fdbee543c87c4bd` |
| `facts/n-990.yaml.gz` | receipt | `57bc9984aff69fde2d0390a7b7458172ddea48da` | `62b620a47b931b8f158282e915d6143b439ec0340322faa62d665a4740456186` |
| `facts/n-991.yaml.gz` | receipt | `f7ea868b0cc03a6cfecedf68f539447fd43669f9` | `8765ff437894700e81cfb2378a5b539b987b515349d71666113eb10e8c99a21e` |
| `facts/n-992.yaml.gz` | receipt | `16e4555095290722455e67049593d0f825a7e61b` | `1e2d93eed250e99627c775bed551f791adab8b08a95b0611f027de5dc40cb050` |
| `facts/n-993.yaml.gz` | receipt | `0dd6ff6a866ba5c69b5a09b94760d01f5a040e88` | `593bfb76d4b85645c06187341643b7c12d54eae2c2431ef8c977dde58867567b` |
| `facts/n-994.yaml.gz` | receipt | `4c4326559378119089c97260e9788e73a8962407` | `49ebd99bd4cc94815a0b98a232f4469060c318bbe9c6dfc27cae75e4027ee080` |
| `facts/n-996.yaml.gz` | receipt | `9e0ad3341f5259017b2044e70b6af8c23faee88e` | `461516e70bdbc91f57c3722a4c984c7a34307876b3200be9cbb0e51bfbc078f7` |
| `facts/n-997.yaml.gz` | receipt | `061e7a6cf6ebc6f1942bc1ce55066cf2ad21dd3d` | `8a29872d7de44da035a76944672987be7bfd543cd64d1c2e276aeb7ecf1d318a` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
