# Francisco Couzo’s Live Records at 43f666c (No Issue)

Francisco Couzo’s commit
[`43f666c`](https://github.com/franciscouzo/square-packing/commit/43f666c23933fbc5cc418fa4e851218268fed0ed)
to [franciscouzo/square-packing](https://github.com/franciscouzo/square-packing), “Land
the 24 October per-puzzle board and the live records since 964ee2b”, lowers the certified
upper bound of `certified_bounds.json` below `964ee2b`’s, the pin of
[issue #763](https://github.com/jlevy/squares/issues/763), at 957 counts.
No issue or comment reports it.
By the owner’s rule of 14 October 2026 a certificate in a watched repository is a report
from its first commit, dated by the push that made that commit public, so `43f666c` is the
repository’s publication and an import of its own (think-gn29).
This packet retains what its claims at or below 1024 read and records their import:

- **At 325 to 1024** the claims are 126 counts from 330 to 997: 108 certificates at their
  own counts, 690 as 691’s certificate less one square, and 17 square tiling and L-border
  recipes of those certificates. The
  [ledger of 24 October for 43f666c](../../../campaign/issue-intake/upper-bounds-couzo-43f666c-20261024/README.md)
  records 106 certificates and 16 recipes as dated beyond-horizon rows of the
  `couzo-43f666c-2026-10-24` source in
  [source-coverage.yaml](../../../frontier/source-coverage.yaml), each the count’s current
  row. 797 and 847 restate #763’s rows, 367 is above a held publication, and 690 has no row
  of its own (below).
- **Above 1024** the other 831 are recipes on 14 of those certificates. The records slice
  above 1024 walks them (think-llit); their parents are retained here.

The same import decides #763’s 13 recipes, which its walk held until a maintained
construction checker existed (think-g2qy). That record lives in the
[issue-763 packet](../couzo-issue763-2026-10-23/README.md#the-recipes-decided).

## Source and Dates

| Field | Value |
| --- | --- |
| Source | [franciscouzo/square-packing](https://github.com/franciscouzo/square-packing) |
| Commit of the claims | `43f666c23933fbc5cc418fa4e851218268fed0ed`, committed 2026-10-24T00:55:44Z; its parent is `964ee2b`, the pin of #763 |
| Pin | `1c1715399709bc955e9b402947ab8b52bbacdfc3`, “Record whether external certificate hashes bind gzip or text bytes”, committed 04:53:53Z, the head of the push; `73eac5b` (04:52:11Z) and `1c17153` change no bound |
| Published | 2026-10-24T06:10:44Z, when one push moved `master` from `964ee2b` to `1c17153`, as GitHub’s activity API records it (`gh api repos/franciscouzo/square-packing/activity`, read on 24 October); `beyond_horizon_replay.PUSHED_LATER` holds that push |
| Claimed | by no issue or comment; Couzo’s comments of 06:10:57Z to 06:12:05Z on #672, #678 and #715 report corrections and claim no bound |
| Retrieved | 2026-10-24T20:49Z, from a blobless clone of the history at the head `1c17153` and a sparse checkout at the pin |
| Custody | [declaration](acquisition/declaration.json), [acquisition record](acquisition/sources.json), [manifest](acquisition/upstream-subtree.sha256) |

## Retained Here

`devtools.acquire_source` wrote the packet from the declaration; every file is bound to its
Git blob at the pin. The scope is 122 files: 114 retained under [source/](source/) (81,274,656
bytes as the source holds them, the four indexes stored as deterministic gzip) and 8 pinned
by digest.

- **Retained:** the 108 certificates `certificates/best/nN.cert` whose bounds `43f666c`
  lowers at 325 to 1024; the deletion at 690 and every recipe, those above 1024 included,
  read certificates among them. The four indexes (`certified_bounds.json`,
  `upper_bounds.json`, `public_bounds.json` and `certificates/best/manifest.json`), the
  README and the construction checker `certificate_constructions.py`, which no program here
  runs.
- **Pinned by digest:** the provenance review and per-count provenance, the catalogue’s
  README and digest list, the parents’ README and manifest, and the exact checker
  `verify_bound_certificate.py` with its licence, both byte-identical to the
  [18 October packet](../couzo-issue678-2026-10-18/README.md)’s retained copies.
- **Pinned by the commit alone:** the other certificates under `certificates/best/`, every
  parent under `certificates/parents/`, `certificates/extended/`, the root
  `certificates/nN.cert` files, the drawings, the search programs and the Rust and CUDA
  sources. Nothing was run.

`check_added_blobs --base origin/main --staged` passed before the first commit (10,386,497 bytes as a thin pack with the rest of this import, every blob under the per-blob ceiling),
so the packet is kept in Git.

**Licence.** The repository states no licence for its data or prose.
GitHub reports MIT from `BOUND_VERIFIER_LICENSE.txt`, which is Evan Daniel’s licence for
the verifier. The certificates and indexes are retained as factual data under the
[owner decision of 2026-10-09](../known-best-packings/README.md#retained-factual-data), as
#795 retained the push of 23:38:42Z; no issue submits `43f666c`, so the presumption of
permission the owner ruled for a source Couzo submitted (think-cnn7) is not stretched to
it. think-m8f4 follows up the exact licence of the source and of the notebooks it credits,
and holds nothing.

**AI assistance.** The source states it in the header of `verify_bound_certificate.py`:
“Copyright (c) 2026 Evan Daniel; modifications by Francisco Couzo with Codex.” The commit’s
message says the certificates come from “CT105’s live records (coordinator, live sync and
browser searches), credited to Francisco Couzo”; Couzo’s answer on #672 of 24 October says
CT105 is the server behind his search web app, which only he runs.

## The Claims

[`devtools.couzo_43f666c_claims`](../../../devtools/couzo_43f666c_claims.py) re-derives
the claims from the retained `certified_bounds.json` and the issue-763 packet’s copy at
`964ee2b`, and writes [receipts/claim-map.json](receipts/claim-map.json): every count
whose certified entry, a certificate or a construction, states a bound strictly below the
one `964ee2b` states, each decided exactly as a rational. Every lowered bound is credited to
Couzo; the module refuses one that is not.

The derivation reproduces the stage 1 triage’s counts (think-cncq): **957 counts lowered,
126 at or below 1024 and 831 above**; at or below 1024, 108 certificates, the deletion at
690 and 17 recipes (367, 444, 487, 632, 683, 732, 733, 737, 744, 787, 788, 792, 800, 844,
845, 903 and 964), each an L-border of one of `43f666c`’s certificates at a smaller count.
The 831 above 1024 are recipes on 14 certificates (679 and 975 to 997).

Each claim keeps the credit the index states, the packing the credit says it refines, and,
for a certificate at its own count, the manifest’s seed credit and its `previous_source`.
The credit and the seed credit agree at all 106 certificates; the manifest states no seed
credit for a recipe, so each of the 16 recipe rows carries the credit line the index
states for it, which is its parent certificate’s at all 16. `previous_source` names the record the
source’s catalogue held at the count before, not the packing the search started from, so
the record keeps it as data and credits nothing by it.

## Exact Replay

[`devtools.beyond_horizon_replay`](../../../devtools/beyond_horizon_replay.py) declares the
publication `franciscouzo/square-packing@43f666c` as a release of this packet, whose rows
its walk records ([acquisition/watched-release.json](acquisition/watched-release.json)).

**The 106 certificates are verified.** Each runs the filtered two-route decision of
[`devtools.couzo_678_replay`](../../../devtools/couzo_678_replay.py), reused unchanged,
with its six controls: route `sqpack` through `sqpack.witness` and `sqpack.verify`’s exact
predicates, route `independent` through `devtools.check_rational_witness_independent`’s,
over every corner against every wall and every pair whose centres are closer than √2 by
exact comparison. **Both routes accept all 106**, and every row’s print is its header side rounded up at 12 places: 178,073 candidate pairs of 28,351,343 and every corner against every wall. **All 636 controls are refused by both routes**, each on the overlap, wall or shape it was built to break. Every square clears the box by at least `1e-15`, and no pair the filter decides touches, the least pair gap 1e-14 (at 629). The positive decisions took 133.3 CPU seconds; with the controls, two workers took 17 min 47 s of wall from 21:01:49Z on 24 October, 2,125 s summed over the rows, at `nice` on a four-core machine shared with other lanes.
[receipts/filtered-exact-replay.json](receipts/filtered-exact-replay.json) keeps every
row’s side, both routes’ counts, least clearance, least gap and failures, and the controls.

**The all-pairs kernel**, `devtools.evand_arrangement_reports`’s two routes with no filter,
decided every pair at 330, 691 and 997 (789,186 pairs, 261.5 CPU seconds). Both routes accept all three, and their least pair gaps and wall clearances equal the filtered decision’s exactly ([receipts/exhaustive-sample.json](receipts/exhaustive-sample.json)).

**The 16 recipes are decided exactly.**
[`devtools.construction_checker`](../../../devtools/construction_checker.py) decides each
from its recipe and its parent certificate in `Fraction`s: the parent is the certificate
the index names by path and SHA-256, a row of this release that both routes accept with
its controls refused; the stated bound is tS + L exactly, and the count is the
construction’s capacity. Every recipe is one L-border layer or more around one tile
(t = 1). The checker decides all 16, each one to five layers on one of the 106 (679’s at 732, 787, 844, 903 and 964; 680’s at 733, 788 and 845; 403’s at 444 and 487; 583’s at 632 and 683; 684’s at 737 and 792; 691’s at 744; 745’s at 800), and refuses all nine of its controls at every one, 144 in all; every parent is a replayed row of the release, so none needed a replay of its own ([receipts/recipe-decisions.json](receipts/recipe-decisions.json)).
Every recipe also has its full n-square expansion under `certificates/parents/` at exactly
its side, which the parents’ manifest records; the record decides the recipe and does not
read the expansion (the author is asked about them).

**Göbel’s classical constructions.** Every decided side is below Göbel’s side at its count,
decided exactly by the 15 October packet’s
[goebel_beyond_horizon.py](../couzo-verified-bounds-2026-10-14/review/goebel_beyond_horizon.py)
([receipts/goebel-comparison.json](receipts/goebel-comparison.json)).

**First commits.** Every certificate was first committed at `43f666c`, and every recipe is
first stated by `43f666c`’s index
([receipts/first-commits.json](receipts/first-commits.json), `recipe_first_commits`).

The source’s own checker was not run here.

## Against the Record, in Report Order

The ledger’s start is the record on `main` at `2ed0ea740` (#795’s merge), the first `main`
that holds the push of 23:38:42Z at the notebook rows’ counts, with Göbel’s construction
beside each row; both answers of 23 October apply through 1024. The claims are dated by the
push of 06:10:44Z. Two reports come between those starts and it, and the walk reads both
(`ClaimMapWalk`):

- **#763’s claims with no row among the starts:** its 13 recipes, which this import
  decides, its deletion bound at 683, held on think-kzme’s question (think-2z2n), and 328,
  850 and 909, which restate f1ceee4’s rows. They are dated by the issue, and their rows are
  the issue-763 source’s.
- **The push of 23:38:42Z, read commit by commit at the walk’s counts**
  (`beyond_horizon_replay earlier-push`, [receipts/earlier-push.json](receipts/earlier-push.json)).
  #795’s review A noted that it put `best/` certificates at #763’s recipe counts, and
  Tymchishin’s and Lavrentev’s notebook recipes are there too: 34 sides below the start,
  8 of `efef7d1`, 12 of `fa6237e` and 14 of `964ee2b`, at #763’s 17 counts and at 792 and
  800. Each is above or equal to #763’s earlier claim, or restates f1ceee4’s row, so none is
  recorded; at 683 the verdicts rest on #763’s held deletion bound.

The earlier publications strictly below the start are walked beside them, as every
claim-map walk reads them: the history scan’s, Polkovskyi’s repository through `f1ceee4`
and the commits after it, and #715’s re-certifications.

- **122 are recorded as rows**, each the count’s current row at its exact side rounded up
  at 12 places, below the standing side by 8.53e-14 (459) to 1.33e-2 (691): 52 by more than
  1e-6, 22 by 1e-10 to 1e-6, and 48 by less than 1e-10. They supersede #763’s rows at 72
  counts (7 of them the recipes this import decides), the push’s notebook rows at 46
  (kyleluecke’s 11, Tymchishin’s v3 10, aqibrazadev’s 8, alexchilton’s 6, Tymchishin’s
  22-3662 5, Lavrentev’s run 361589987 4 and his v11 2), f1ceee4’s at 3 and #732’s at 1.
- **Not recorded:** 797 and 847 are below #763’s rows by 8.43e-13 and 2.49e-14 at the same
  12-place print, so by the owner’s answer of 23 October (think-fwa9) they restate those
  rows. 459 is 8.53e-14 below #763’s row but its exact side rounds up to a lower print, so it
  is recorded. 367, an L-border of 330’s certificate, is 3.83e-12 above `23aff0c`’s index
  bound at 367, Friedman’s off-centre construction at 368 less one square, which the walks
  hold on whether Friedman’s constructions count as Göbel’s do (think-zkxy); its verdict
  rests on that hold, and an answer that leaves it out reruns the walk.
- **No row of its own:** 690, 691’s certificate less one square, is an earlier report by the
  owner’s D6 answer, and has no row on that decision’s recommendation, which think-kzme
  asks the owner to confirm. The walk records it, and the chain passes over it.

## Credit and Lineage

Credit is read from the source’s own files and names each person by name. The index and
manifest credit Couzo’s square-packing live search at every row, after the packing each
refines:

- **74 rows**: Couzo after Vladislav Lavrentev (lightningv08), Kaggle notebook “CUDA
  Packing Search” v11.
- **38 rows**: Couzo after Kirill Tymchishin (kirilltym), Kaggle notebook “CPU Alternating
  Reclosure” v3, and **2** after his notebook “22-3662-cpu-cuda-mps-eda-union”, run
  361576574.
- **3, 2 and 1 rows**: Couzo after the Kaggle notebooks of the accounts kyleluecke (run
  361592092), alexchilton (run 361412241) and aqibrazadev (run 361516058).
- **1 row**: Couzo after Mykhailo Polkovskyi (508). **1** is his own (412).

Each notebook is the run the push of 23:38:42Z published, so the record cites the keys #795
defined for them. The bibliography key is `[Couzo 43f666c 2026-10-24]`, credit “Couzo after
Lavrentev, Tymchishin, kyleluecke, alexchilton, aqibrazadev, Polkovskyi, Levy”, the last for
the manifest’s first checker, this project’s `sqpack/verify.py`. At 18 counts the
row is 5e-12 to 3e-11 below the notebook side `964ee2b` published (think-lyf9’s triage measured
the same packing at 377, 405, 596 and 984), and at 377 the credit names Tymchishin where
`964ee2b` named kyleluecke; the author is asked both.

## Questions for the Author

Drafted in think-gn29’s notes for the next reply on #763, not posted: whether #763 extends
to these rows; whether “Couzo after” at the 18 near-identical counts means a new packing
or a tighter certificate; the credit at 377; what `previous_source` names and which
packing each notebook started from; whether the recipes’ expansions are meant as their
certificates; and #763’s open questions on 303, 268 and 304.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `source/certificates/best/manifest.json.gz` | upstream | `28dba11c8756ec5053575b7a35db6965ffdca757` | `60054305cfbd61b919c638bf05c2d0fc95aa468404580122387dd67eee54a142` |
| `source/certified_bounds.json.gz` | upstream | `6c01f0d96fad4afdf9965ecc457ad3e502e1c517` | `e45a380f790976a01ac83016adecf96f4b6848f2f96b99784355ce38cdedaab3` |
| `source/public_bounds.json.gz` | upstream | `e49a27132657202a51ad52ab512186da88ea3d8e` | `a9b84ca45ce6ac23dcbe373154264c3a3522f567c65f3ae7b6d0053ae62d8307` |
| `source/upper_bounds.json.gz` | upstream | `0ee5b59b7e27f95f6bdb556f362a15f2b670317d` | `970b8dfa8b247c1ca9ceecc3a4e9a68b48ca4fd846e9dfd803e99e48cd9650f2` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
