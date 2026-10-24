# Francisco Couzo’s Upper Bounds at 964ee2bd (Issue #763)

[Issue #763](https://github.com/jlevy/squares/issues/763), filed 2026-10-23T23:35:51Z
as a follow-up to [#715](https://github.com/jlevy/squares/issues/715), asks that 436
improved upper bounds for n = 268 to 9802 be registered from
[franciscouzo/square-packing](https://github.com/franciscouzo/square-packing/tree/964ee2bdf301d0c8912d956d4010f478dcbbd5ea)
at `964ee2bdf301d0c8912d956d4010f478dcbbd5ea`: 203 at or below 1024 and 233 above.
The issue carries no table, so this packet re-derives the claims from the source’s own
indexes, retains every certificate they read, and records the import of the 203 at or
below 1024 (think-ptkk):

- **268 and 303**, in the n ≤ 324 corpus, are registered as reported as T-240, each
  below the house and every earlier report at its count.
- **At 325 to 1024**, the
  [ledger of 24 October for issue 763](../../../campaign/issue-intake/upper-bounds-issue763-20261024/README.md)
  records 198 of the 201 claims in report order. 184 certificates are dated
  beyond-horizon rows of the `couzo-issue763-2026-10-23` source in
  [source-coverage.yaml](../../../frontier/source-coverage.yaml); 13 L-border recipes and
  the deletion bound at 683 are held for decisions; 328, 850 and 909 restate the f1ceee4
  rows the record already holds.
- **The 233 above 1024** are retained where they are certificates and wait on think-llit,
  which applies the owner’s answer that rows above 1024 are tracked.
- **15 further index rows** at or below 1024, which the issue’s selection rule leaves out,
  are an import of their own: 10 are rows of the `couzo-964ee2b-2026-10-23` source.

## Source and Dates

| Field | Value |
| --- | --- |
| Source | [franciscouzo/square-packing](https://github.com/franciscouzo/square-packing) |
| Pin | `964ee2bdf301d0c8912d956d4010f478dcbbd5ea`, “Land the 23 October live records, notebook packings and Mishapolk certificates”, the commit the issue names |
| Committed | 2026-10-23T22:38:09Z; its parents `fa6237e` (18:59:39Z) and `efef7d1` (18:16:49Z) follow `6b7391d`, the pin of #715 |
| Published | 2026-10-23T23:38:42Z, when one push moved `master` from `6b7391d` to `964ee2b`, as GitHub’s activity API records it (`gh api repos/franciscouzo/square-packing/activity`, read 24 October); `beyond_horizon_replay.PUSHED_LATER` holds that push, so `efef7d1` and `fa6237e`, committed before Polkovskyi’s `f1ceee4` (#732’s comment of 20:35:12Z), are dated after it |
| Issue filed | 2026-10-23T23:35:51Z, 2 min 51 s before the push; no comment or edit since, and the `intake` label added at 02:03:56Z on 24 October |
| Retrieved | 2026-10-24T08:27Z, a full clone of the history to the head `1c17153` and a checkout at the pin |
| Later commits | `43f666c`, `73eac5b` and `1c17153`, pushed at 2026-10-24T06:10:44Z, are not read here |
| Custody | [declaration](acquisition/declaration.json), [acquisition record](acquisition/sources.json), [manifest](acquisition/upstream-subtree.sha256) |

The four indexes the issue links have the SHA-256 the triage read: `upper_bounds.json`
`212b33b6…`, `certified_bounds.json` `f368786a…`, `certificates/best/manifest.json`
`d95f2bd6…` and `public_bounds.json` `dca2d4b6…`.

## Retained Here

`devtools.acquire_source` wrote the packet from the declaration; every file is bound to its
Git blob at the pin. The scope is 223 files: 217 retained under [source/](source/)
(85,984,743 bytes; 32 MB as stored, the four indexes as deterministic gzip) and 6 pinned by
digest.

- **Retained:** the certificate `certificates/best/nN.cert` of every count the claims and
  the unrequested rows read, 208 files (the 194 own-count certificates of the 436 claims and
  the 14 the 15 unrequested rows read), and 304’s, which `fa6237e` first committed and #763
  does not claim, the first report at its count, for its own import (think-l49q); the two
  Kaggle parents the manifest names at 268 and
  303 (`certificates/parents/85dbd707…` and `22f07a7c…`); the four indexes; the README; and
  the construction checker `certificate_constructions.py`, which no program here runs.
- **Pinned by digest:** the provenance review and per-count provenance, the catalogue’s
  README and digest list, and the exact checker `verify_bound_certificate.py` with its
  licence, both byte-identical to the
  [18 October packet](../couzo-issue678-2026-10-18/README.md)’s retained copies.
- **Pinned by the commit alone:** the other 880 certificates under `certificates/best/`,
  the other 3,833 parents, `certificates/extended/`, the root `certificates/nN.cert` files,
  the drawings, the search programs and the Rust and CUDA sources. Nothing was run.
- **Not imported here:** the same push also publishes sides credited to other authors’
  Kaggle notebooks at 99 counts between 325 and 1024, each below the record (87
  certificates and 12 recipes), which no issue reports; think-lyf9 imports them, before
  think-gn29’s walk of `43f666c`.

`check_added_blobs --base origin/main --staged` passed before the first commit, at 15.1 MB
as a thin pack with every blob under the per-blob ceiling, so the packet is kept in Git, as
#715’s was.

**Licence.** The repository states no licence for its data or prose.
GitHub reports MIT from `BOUND_VERIFIER_LICENSE.txt`, which is Evan Daniel’s licence for
the verifier. Couzo submitted this source to the repository in issue #763, and the owner
ruled on 24 October 2026 that a source its author submitted carries a presumption of
permission to retain and import it (think-cnn7; the rule is in
[result-import.md, stage 2](../../../campaign/result-import.md#stage-2-retain)).
The certificates, indexes, README and construction checker are retained on that
presumption, and the certificates are factual data under the
[owner decision of 2026-10-09](../known-best-packings/README.md#retained-factual-data) as
well. think-m8f4 follows up the exact licence without holding the import.
The presumption covers Couzo’s own material only. The 268 parent is Kirill Tymchishin’s
notebook packing, whose provenance in the manifest states the notebook’s licence as
Apache-2.0, and it is retained as factual data under that decision; Evan Daniel’s verifier
is pinned under its MIT licence.

**AI assistance.** The source states it in one place, the header of
`verify_bound_certificate.py`: “Copyright (c) 2026 Evan Daniel; modifications by Francisco
Couzo with Codex.” Neither the README nor the indexes say more about how the packings were
found than their credits.

## The Claims

The issue’s body ends at its legend: it lists no rows, and it has no comment.
[`devtools.couzo_763_claims`](../../../devtools/couzo_763_claims.py) re-derives them from
the retained `certified_bounds.json` and `public_bounds.json` by the rule the source’s
README states for its own table, and writes
[receipts/claim-map.json](receipts/claim-map.json):

- a claim is a count whose certified entry, a certificate or a construction, is credited
  to Couzo; the index also holds notebook packings by other authors, which the issue says
  are not part of the request;
- the comparison is the count’s reviewed public bound, except that the competition’s staff
  per-puzzle leaderboard, whose packings are not public, is replaced by the bound it
  superseded;
- against Couzo’s own comparison the side’s 12-place print must be lower, and against
  another author’s the side must be more than `1e-10` below.

Each comparison is decided exactly, `r + s√2` included. The derivation reproduces every
count the issue states: **436 rows, 203 at or below 1024 and 233 above, and 196
certificate rows** (194 own-count certificates and the deletions 683 and 1646), with 239
recipes and the recipe deletion 1727, so deletion bounds at exactly 683, 1646 and 1727.
Two of the issue’s counts are not reproduced, and are reported, not forced: its legend
counts 345 rows that refine another author’s packing where the credits give 351 (A 253, B
94, C 1, E 1, and 2 from Tymchishin’s notebook “22-3662-cpu-cuda-mps-eda-union”, which the
legend omits), and it counts 180 counts where the leaderboard is smaller where the index
gives 182 at n ≤ 1000. The index’s 12-place print is the exact side rounded up at every one
of the 436.

The rule as the issue’s own sentence states it, the 12-place print alone, lists 15 more
counts at or below 1024: 204 in the corpus and 14 at 335 to 998. The triage of 24 October
counted the 14 and did not name 204, which lies 3.87e-12 above T-231 at its count. Those 15
are the unrequested rows below.

At 325 to 1024 the 201 claims are 186 certificates, 14 recipes (365, 444, 487, 632, 733,
734, 737, 788, 789, 845, 909, 910, 966 and 970, each an L-border of a certificate at a
smaller count) and 683, 684’s certificate less its last square.

## Exact Replay

[`devtools.beyond_horizon_replay`](../../../devtools/beyond_horizon_replay.py) declares
two releases on this packet: issue #763, whose rows its walk records
([acquisition/declared-rows.json](acquisition/declared-rows.json)), and the index’s
unrequested rows, `franciscouzo/square-packing@964ee2b`, a publication with its own
[declaration](acquisition/watched-release-964ee2b.json), record and receipts under
[receipts/964ee2b/](receipts/964ee2b/). Each decided row runs the filtered two-route
decision of [`devtools.couzo_678_replay`](../../../devtools/couzo_678_replay.py), reused
unchanged, with its six controls: route `sqpack` through `sqpack.witness` and
`sqpack.verify`’s exact predicates, route `independent` through
`devtools.check_rational_witness_independent`’s, over every corner against every wall and
every pair whose centres are closer than √2 by exact comparison.

**All 194 certificates are verified.** Every row’s print is its header side rounded up at
12 places, and both routes accept every packing: for #763’s 184, 312,122 candidate pairs of
47,431,604 and every corner against every wall; for the 10 unrequested rows, 11,973 of
1,568,628. **All 1,164 controls are refused by both routes** (1,104 and 60), each on the
overlap, wall or shape it was built to break. Every square of the 184 clears the box by at
least `1e-15`, and no pair the filter decides touches, the least pair gap 1e-14 (at 536).
Of the unrequested rows, 452 touches the box (102 corner contacts with a wall, which the
closed contract allows) and the others clear it by `1e-15`; their least pair gap is
2.08e-13 (452). The positive decisions took 271.1 and 8.5 CPU seconds; with the controls,
two workers took 2,568 s of wall from 08:49:35Z on 24 October, 5,128 s summed over the
rows, about 43 CPU-minutes, at `nice` on a four-core machine shared with other lanes.
[receipts/filtered-exact-replay.json](receipts/filtered-exact-replay.json) and
[receipts/964ee2b/filtered-exact-replay.json](receipts/964ee2b/filtered-exact-replay.json)
keep every row’s side, both routes’ counts, least clearance, least gap and failures, and
the controls.

**The all-pairs kernel**, `devtools.evand_arrangement_reports`’s two routes with no
filter, decided every pair at 333, 684 and 997 (785,370 pairs, 328.5 CPU seconds) and at
998 among the unrequested rows (497,503 pairs, 154.8 CPU seconds). Both routes accept all
four, and their least pair gaps and wall clearances equal the filtered decision’s exactly
([receipts/exhaustive-sample.json](receipts/exhaustive-sample.json),
[receipts/964ee2b/exhaustive-sample.json](receipts/964ee2b/exhaustive-sample.json)).

The two certificates in the corpus have
[`devtools.upper_bound_reports`](../../../devtools/upper_bound_reports.py)’s complete
replay ([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)): a
positive, a duplicate-square and an outside-container job for each, on both of
`devtools.evand_arrangement_reports`’s exact routes over every pair. Both pass and both
controls are refused at each: 489,186 pair decisions in 59.47 route CPU seconds, every wall
clearing by at least `1e-15` and every pair by at least 2.07e-13.

**Göbel’s classical constructions.** Every decided side is below Göbel’s side at its count,
decided exactly by the 15 October packet’s
[goebel_beyond_horizon.py](../couzo-verified-bounds-2026-10-14/review/goebel_beyond_horizon.py)
([receipts/goebel-comparison.json](receipts/goebel-comparison.json) and
[receipts/964ee2b/goebel-comparison.json](receipts/964ee2b/goebel-comparison.json)).

**First commits.** 174 of the 184 certificates were first committed at `964ee2b`, 8 at
`fa6237e` and 2 at `efef7d1`; of the 10 unrequested rows, 7 at `964ee2b` and 3 at
`efef7d1` ([receipts/first-commits.json](receipts/first-commits.json)). The push of
23:38:42Z made all three commits public together.

The source’s own checker was not run here.

## Against the Record, in Report Order

The ledger’s start is the record on `main` at `e5c1c64e3` (#756’s merge), the first `main`
that holds Polkovskyi’s `f1ceee4` rows (#769) and T-239 at 303 (#757), with Göbel’s
construction beside each row; both answers of 23 October apply through 1024. Its claims
are dated by the issue. The earlier reports strictly below the start are walked beside
them: the history scan’s publications, Polkovskyi’s repository through `f1ceee4` and the
commits after it, and #715’s re-certifications.

- **268 and 303 are recorded.** 268 is 4.45e-3 below T-174 (PingYou Ltd’s house, of
  Couzo’s packing as Daniel improved it) and below every earlier report; 303 is 2.78e-3
  below T-239 (Kristiansen’s house) and 2.79e-3 below T-230 and Polkovskyi’s `7e82c64`.
- **184 certificates are recorded as rows**, each the count’s current row at its exact side
  rounded up at 12 places, below the standing side by 2.80e-11 (803, against f1ceee4’s
  row) to 6.78e-2 (696), median 2.9e-2. They supersede f1ceee4’s rows (92), #719’s (40),
  #732’s `17cc220` rows (20), `couzo-index-2026-10-15`’s (13), `couzo-verified-bounds`’s
  (4), #715’s (3), #670’s (2), `evand-compositions`’ (1) and `couzo-certificates-2026-10-14`’s
  (1); at 8 counts no row stood before them (Göbel’s construction at 7, the grid at 465).
- **Held:** the 13 recipes, which wait on a maintained construction checker (think-g2qy,
  after D2 on think-f2io), and 683, which the issue claims, on think-kzme’s question whether
  an issue-claimed deletion bound gets a row (think-2z2n). The walk records them, so they
  stand at their counts, and no row holds them.
- **Not recorded:** 328, 850 and 909 are below f1ceee4’s rows by 3.16e-13, 6.75e-14 and
  2.57e-13 at the same 12-place print, so by the owner’s answer of 23 October (think-fwa9)
  they restate those rows. 365 and 970, 8.25e-13 and 4.85e-13 below f1ceee4’s rows, are
  recorded only because those rows’ exact sides round up to a higher print; both are held
  recipes.
- At 19 counts the walk records Couzo’s own `23aff0c` constructions, and at 7 of them his
  `4e4c8ce` deletion bounds, which the history walk holds, below the start; #763 is
  recorded below them at all 19. The earlier publications whose verdicts rest on those holds
  are declared in `beyond_horizon_replay.WALKS`.

## The Unrequested Rows

`certified_bounds.json` at the pin states 15 rows credited to Couzo at or below 1024 that
are below the reviewed comparison’s print but, where the comparison is another author’s,
by `1e-10` or less: 204, 335, 339, 344, 379, 380, 421, 452, 490, 507, 535, 792, 800, 935
and 998. No issue reports them, so by the runbook they are an import of their own, the
watched repository’s publication dated by the push of 23:38:42Z.
The walk records 10 as current rows, below the standing side by 5.82e-12 (335) to
5.08e-11 (421), superseding #719’s rows (7), Muglich’s #686 rows (2) and f1ceee4’s at 335.
490, 535, 792 and 800 restate f1ceee4’s rows, and 204 is above T-231. The index credits
421, 792 and 800 as refinements of Polkovskyi’s packings, so margins this small may be
re-certifications of the comparison’s own packing; the author is asked whether he claims
them.

## Credit and Lineage

Credit is read from the source’s own files and names each person by name. The manifest
credits Couzo at every row, after the packing each search started from:

- **A, 253 rows** (131 of the 184 rows, and 303): Couzo after Vladislav Lavrentev
  (lightningv08), Kaggle notebook “CUDA Packing Search” v11. At 303 the manifest’s parent
  is Couzo’s own Kaggle push refinement of that packing (`certificates/parents/22f07a7c…`).
- **B, 94 rows** (43 of the 184): Couzo after Kirill Tymchishin (kirilltym), Kaggle
  notebook “CPU Alternating Reclosure” v3.
- **C, 268**: Couzo after Tymchishin, Kaggle notebook “CPU/GPU/MPS EDA+Seam LP” v4; the
  manifest’s parent is that notebook’s packing (`certificates/parents/85dbd707…`).
- **334 and 597**: Couzo after Tymchishin, notebook “22-3662-cpu-cuda-mps-eda-union”, run
  361576574, which the issue’s legend omits.
- **E, 422**: Couzo after Darius Muglich (#686).
- **85 rows credited to Couzo alone** (7 of the 184) keep the chain of the row or
  certificate they build on.

The manifest’s `previous_source` at 268 and 303 is the source’s previous record (PingYou
Ltd’s at 268, Daniel’s T-230 at 303), not the lineage; the stage 4 review measures the
identity. The issue says the notebooks’ own source notices carry their earlier construction
credits; the source does not publish them, so they are asked of the author. The bibliography
key is `[Couzo issue 763 2026-10-23]`, credit “Couzo after Lavrentev, Tymchishin, Muglich,
Polkovskyi, Daniel, Fang, de Winter, Levy”.

## Questions for the Author

Drafted in think-ptkk’s notes for the reply after the merge:

1. The issue lists no rows. Please attach the table as a file at the pinned commit, so the
   record can hold its claims to it rather than to a re-derivation.
2. Do you claim the 15 index rows the selection rule leaves out (204, 335, 339, 344, 379,
   380, 421, 452, 490, 507, 535, 792, 800, 935 and 998)?
3. The certificates at 1765, 1647 and 1648 name no seed (“ct105 recovered candidate”), and
   64 rows above 1024 read them: the three and 61 recipes and deletions built on them. What
   did each start from?
4. Which version of each Kaggle notebook did the parents come from, and what do the
   notebooks’ source notices credit?
5. Does #763 extend to the rows of your later commit `43f666c` (think-gn29 holds them)?
6. Who ran the CT105 store’s “browser searches” the manifest names?
7. `43f666c`’s README no longer lists 303, and its commit message says “303 is
   pjmathematician’s, submitted before our 3.5e-11 refinement”: a per-puzzle leaderboard
   entry submitted on 23 October 2026 at 11:56:49 UTC, a side-only print 3.47e-11 above
   this side. Does #763 still claim 303?
8. Should the 268 credit name Lavrentev? Evan Daniel’s commit `8a8879a` describes his 268
   certificate as “Vladislav Lavrentev’s (Kaggle lightningv08) public packing … the first
   public packing at that side”, and the manifest’s lineage for the 268 parent begins at
   `kaggle-public-portfolio-20261022`, source `cuda`. The triage of 24 October measured the
   three as one packing in a scratch measurement no retained tool holds; the stage 4 review
   measures it.
9. Is Tymchishin the finder of the packing at 304 (`certificates/best/n304.cert`, first
   committed at `fa6237e`), which #763 does not claim?

## The Notebook Rows

Added on 24 October 2026 by the import of think-lyf9, and revised the same day for review A
of #795, which reads the push commit by commit. The sections above describe #763’s import
as it landed; where their counts of the retained files differ from this section’s, this
section’s are current.

The push of 2026-10-23T23:38:42Z that made `964ee2b` public also published, in its
`certified_bounds.json`, sides credited to the authors of seven Kaggle notebooks, not to
Couzo. #763 says the index’s notebook packings by other authors are not part of its
request, and no other issue reports them. By the owner’s rule of 14 October 2026 a
certificate in a watched repository is a report from its first commit, so they are the
push’s publication, and an import of their own.

**The selection.** [`devtools.couzo_763_claims`](../../../devtools/couzo_763_claims.py)
lists them in [receipts/claim-map.json](receipts/claim-map.json) as `others`: each
certificate or construction at 325 to 1024 whose credit does not name Couzo, strictly below
Göbel’s construction at its count (decided exactly as p + q√2), and not an earlier
publication, a count and side the history scan or f1ceee4’s receipts already hold.
Of the 149 such entries, 50 are earlier publications. The other **99** are the stage 1
triage’s set exactly: **87 certificates and 12 L-border recipes** (445, 488, 580, 679,
732, 787, 844, 859, 903, 913, 964 and 967), the derivation’s controls. Each recipe has a
certificate of its own: `964ee2b` keeps the recipe’s full n-square expansion under
`certificates/parents/` at exactly its side, first committed at the recipe’s own commit,
and the claim map names it (`recipe_certificate`). The walk below finds every one strictly
below the record on `main`, the rest of the triage’s rule.

**The push, commit by commit.** The push carried three commits, `efef7d1` (committed
18:16:49Z), `fa6237e` (18:59:39Z) and `964ee2b` (22:38:09Z), and the repository reads a
push as the history scan does, one publication a commit.
`beyond_horizon_replay push-publications` writes
[receipts/push/push-publications.json](receipts/push/push-publications.json): every
certificate header and index bound each commit adds or changes at the 99 counts, and each
commit’s least side there that no earlier commit or publication states, strictly below the
frozen start. It refuses unless the commits are a chain and every claim is held by a
certificate `964ee2b` keeps at the same Git blob, and its controls are the claims of each
commit, 40, 90 and 60, and that the last at each count is the claim map’s row. Besides the
99, `efef7d1` and `fa6237e` state **91 more sides at 63 of the counts**: 76 as Couzo’s own,
37 of which the index says refine Lavrentev’s (33) or Tymchishin’s (4) packings, one at 994
that the index credits to Mykhailo Polkovskyi, 9 of Lavrentev’s v11 and 5 of Tymchishin’s
v3, all replaced at `964ee2b` and kept under `certificates/parents/` or as root
certificates. A side the index credits to neither Couzo nor a notebook has no release, so
the walk may only rule it out; the one at 994 restates Polkovskyi’s own #732 row.

**Retained.** The 87 certificates `certificates/best/nN.cert`, 9,780,397 bytes, were added
to this packet’s scope from a checkout of the same commit for the import, and the 103
certificates that hold the other sides the push states, 12,720,179 bytes, for review A:
69 under `certificates/parents/`, the 12 recipes’ expansions among them, and 34 root
certificates `certificates/nN.cert`. Each is bound to its Git blob there. The parents’
README and 2.9 MB manifest are pinned by digest. The packet now retains 407 of its 415
files (108,485,319 bytes).

**Licence.** The notebook certificates are the packings of other authors’ notebooks, so
the presumption of permission from Couzo’s submission does not cover them. They are
retained as factual data under the
[owner decision of 2026-10-09](../known-best-packings/README.md#retained-factual-data), as
the 268 parent is. The manifest states Apache-2.0 for the notebooks of Tymchishin’s “CPU
Alternating Reclosure” v3 and Lavrentev’s “CUDA Packing Search” v11 and “per the notebook”
for the other five, and the source notices it cites,
`submissions/kaggle-public-portfolio-20261022/SOURCE_NOTICES.md`, are not in the tree at
`964ee2b`. think-m8f4 follows up those licences and notices, and holds nothing. Of the 103
added for review A, 76 are sides the index states as Couzo’s own, retained on the
presumption as well, one is the side at 994 it credits to Polkovskyi, and 26 are notebook
packings (Tymchishin’s v3 16, Lavrentev’s v11 9 and the 859 recipe of Lavrentev’s later
run).

**The releases.** Each holder at each commit is a coverage source with its own bibliography
key, credited by name where the source states one and by handle where it gives only a
handle; Couzo’s own sides cite #763’s key:

| Holder, as the source names it | Run | Commit | Rows | Last rows | Recipes | Source |
| --- | --- | --- | --- | --- | --- | --- |
| Francisco Couzo, his own sides | - | `efef7d1` | 35 | 0 | - | `couzo-efef7d1-2026-10-23` |
| Francisco Couzo, his own sides | - | `fa6237e` | 37 | 0 | - | `couzo-fa6237e-2026-10-23` |
| Kirill Tymchishin (kirilltym), “CPU Alternating Reclosure” v3, Apache-2.0 | 361239073 | `fa6237e` | 42 | 37 | 11 | `tymchishin-reclosure-v3-2026-10-23` |
| Vladislav Lavrentev (lightningv08), “CUDA Packing Search” v11, Apache-2.0 | 361263594 | `fa6237e` | 11 | 2 | - | `lavrentev-cuda-v11-2026-10-23` |
| Kirill Tymchishin, “22-3662-cpu-cuda-mps-eda-union” | 361576574 | `964ee2b` | 15 | 15 | - | `tymchishin-22-3662-2026-10-23` |
| kyleluecke, “inos-v0-6-k-mosh-squares-in-squares-22-366222” | 361592092 | `964ee2b` | 18 | 18 | - | `kyleluecke-inos-2026-10-23` |
| alexchilton, “fault-line-dp-basin-hopping-lb-22-3747” | 361412241 | `964ee2b` | 11 | 11 | - | `alexchilton-fault-line-2026-10-23` |
| aqibrazadev, “squares-in-squares-top-lb-blending-visualization” | 361516058 | `964ee2b` | 9 | 9 | - | `aqibrazadev-blending-2026-10-23` |
| Vladislav Lavrentev, “squares-in-squares-cuda-packing-search”, a later run | 361589987 | `964ee2b` | 7 | 7 | 1 (859) | `lavrentev-cuda-run-361589987-2026-10-23` |

“Last rows” are the current rows, the 99; the other 86 are each superseded by a later
commit of the push. The five notebooks after the first two give a run and no version, and
their licence is “per the notebook”. Kaggle’s public profile pages of the three handles,
read on 24 October 2026, are titled “Kyle Luecke”, “alex chilton” and “Aqib Raza”; their
profiles record those as the names the pages state, and whether each account is that person
is asked of the publisher. Every notebook entry says its earlier construction credits are
kept in the notebook, or in its source notices; neither is published here. The manifest
records each certificate under `certificates/best/` as the publisher’s certificate of the
notebook’s packing, dilated by 1+1e-12 (1+1e-11 at 340 and 1+1e-10 at 409 and 509).

**Exact replay.**
[`devtools.beyond_horizon_replay`](../../../devtools/beyond_horizon_replay.py) declares
each release on this packet, with its declaration
(`acquisition/watched-release-push-TAG.json`), record
(`acquisition/beyond-horizon-rows-push-TAG.json`) and receipts under
[receipts/push/](receipts/push/), the tag a notebook run or `couzo-` and the commit. The
filtered two-route decision, reused unchanged with its six controls, **verified all 185**,
every print the header side rounded up at 12 places: 293,710 candidate pairs of 48,049,913
and every corner against every wall, in 213.8 positive CPU seconds. **All 1,110 controls
are refused by both routes.** The 12 recipe expansions, Lavrentev’s v11 side at 411 and
Couzo’s own sides at 594 (`fa6237e`) and at 21 counts of `efef7d1` touch the box, and all
but 5 of `efef7d1`’s also have touching pairs, which the closed contract allows; every other
row clears the box by at least `1e-15`, and no pair the filter decides there touches. The four releases whose
rows did not change keep their run of 14:21:45Z (697 s of wall); the other five ran from
17:22:00Z (731 s), both with two workers at `nice` on a four-core machine shared with other
lanes. The all-pairs kernel, with no filter, decided every pair at 975 and 994 (968,346
pairs, 225.2 CPU seconds): both routes accept both, and their least pair gaps and wall
clearances equal the filtered decision’s exactly
([receipts/push/361239073/exhaustive-sample.json](receipts/push/361239073/exhaustive-sample.json),
[receipts/push/361516058/exhaustive-sample.json](receipts/push/361516058/exhaustive-sample.json)).
Every side is below Göbel’s construction at its count (each release’s
`goebel-comparison.json`). Each certificate’s blob first appears at the commit its release
declares (`first-commits.json`): 35 at `efef7d1`, 90 at `fa6237e` and 60 at `964ee2b`. The
source’s own checker was not run here.

**In report order.** The
[ledger of 24 October for the notebook rows](../../../campaign/issue-intake/upper-bounds-couzo-964ee2b-notebooks-20261024/README.md)
walks the 99 counts from starts frozen at `main` `2ec489d1e` (#789’s merge), with Göbel’s
construction beside each row, as three reports, `franciscouzo/square-packing@efef7d1` (40),
`@fa6237e` (90) and `@964ee2b` (60). All three are dated by the push, and the walk takes
them in commit order (`intake_ledger.walk` orders a tie in report time by each claim’s first
commit). **It records 185**: all of `fa6237e`’s and `964ee2b`’s, and 35 of `efef7d1`’s; at
633, 791, 856, 919 and 994 `efef7d1` restates an earlier publication below the 12-place
print (think-fwa9). At 60 counts two or three of the push’s sides are recorded in turn, and
the last is the count’s current row, below the record by 1.46e-4 (875, against Muglich’s
#686 row) to 6.60e-2 (923, against f1ceee4’s); Göbel’s construction is the least member of
the start at 11 counts. The push’s first row at each count supersedes the row that stood
there, 86 in all: f1ceee4’s (32), `couzo-index-2026-10-15`’s (13), #719’s (12), #732’s
`17cc220` rows (8), `couzo-reconcile-2026-10-20`’s (8), `couzo-verified-bounds-2026-10-14`’s
(4), Muglich’s #686 rows (3) and 6 more of Couzo’s; at 13 counts (376, 445, 488, 537, 604,
685, 738, 761, 793, 861, 920, 964 and 971) no row stood before them. At 16 counts the walk
also records Couzo’s own `487b058`, `4e4c8ce` and `23aff0c` publications that the history
walk holds, below the start, and the push’s rows are recorded below them at all 16.

**Identity and credit.** At five counts the last row is within 1.1e-7 of the push’s earlier
side, and `964ee2b`’s manifest names that earlier certificate as the row’s
`previous_source`. `beyond_horizon_replay push-identity` measures each pair with the
packet’s pose measure (`measured_identity`, as `pose-identity` does for #732’s comment;
`devtools.measure_identity`, think-jv2s, had not landed) and writes
[receipts/push/pose-identity.json](receipts/push/pose-identity.json):

| n | Row | Earlier side of the push | Below by | Pairing | Beyond 1e-3 |
| ---: | --- | --- | --- | --- | ---: |
| 364 | aqibrazadev | Tymchishin’s v3, `fa6237e` | 1.35e-9 | not one to one | 116 |
| 378 | kyleluecke | Lavrentev’s v11, `fa6237e` | 3.11e-8 | one to one, largest 4.42e-8 | 0 |
| 405 | kyleluecke | Lavrentev’s v11, `fa6237e` | 1.89e-8 | one to one, largest 2.46e-8 | 0 |
| 450 | kyleluecke | Tymchishin’s v3, `fa6237e` | 2.08e-9 | not one to one | 200 |
| 874 | kyleluecke | Couzo’s, `fa6237e`, which the index says refines Lavrentev’s | 1.07e-7 | not one to one | 234 |

Each row is credited by the record’s chain rule: every link the source’s files state is
credited, and the manifest’s `previous_source` is the link at all five counts. At 378 and
405 kyleluecke’s row is Lavrentev’s packing refined, every square within 5e-8 and every
turn within 5e-8 degrees, so the ledger records a refinement and the row is credited to
kyleluecke after Vladislav Lavrentev. At 364, 450 and 874 more than fifty squares move
beyond 0.1: the search moved the arrangement it was seeded from, which does not contradict
the seed link. The ledger records each as a new packing seeded from the earlier side, with
the measurement beside it, and credits it after that side’s finders: aqibrazadev after
Kirill Tymchishin at 364, kyleluecke after Kirill Tymchishin at 450, and kyleluecke after
Francisco Couzo and Vladislav Lavrentev at 874, where the index credits Couzo’s side as a
refinement of Lavrentev’s packing.

**Later.** Couzo’s `43f666c`, pushed at 2026-10-24T06:10:44Z, is below the notebook side at
46 of the 99 counts. think-gn29 walks it after this import, from these rows. The questions
for the publisher are drafted in think-lyf9’s notes for the next reply on #763.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `source/certificates/best/manifest.json.gz` | upstream | `38c5734575472e95fb9f17c25c6a590588ffa080` | `d95f2bd6410abf07d568cbed937afb066de7ed6b01a35f74e6b461ac6a44c5ae` |
| `source/certified_bounds.json.gz` | upstream | `691df67a5b81414c25cf8e8277fd65cee102408a` | `f368786a706a6911f087b11b9cb0fe4f81edcb441f66b88467fa253217a3f263` |
| `source/public_bounds.json.gz` | upstream | `95fb9f74ee36969db1deb331c7e45606dc8a81c2` | `dca2d4b6604189f75aea7656ece1ff739bb1b665c1fb11a71b0c5a3115fc989f` |
| `source/upper_bounds.json.gz` | upstream | `e397754d7def09eb0950f911967ee8e02e43fc4c` | `212b33b6f0e21012ec9b69d4ec8fb0d9e81693c8666e69095e8c806d23ea7aa6` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
