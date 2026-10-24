---
type: is
id: is-01m5pwb2kmk5xd6tfkzyhh4h3y
title: "Import the 99 Kaggle-credited sides franciscouzo/square-packing published at 964ee2b (pushed 2026-10-23T23:38:42Z): 87 certificates and 12 recipes at 325-1024, each 1.46e-4 to 6.60e-2 below main's record, credited to notebook authors (no issue)"
kind: task
status: in_progress
priority: 1
version: 5
delegate: c-triage-lyf9-1024
labels:
  - result-import
dependencies:
  - type: blocks
    target: is-01m5pjxq31vpw03t0emgwnvhfe
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T11:57:05.011Z
updated_at: 2026-10-24T13:59:05.761Z
started_at: 2026-10-24T13:38:16.607Z
---

## Notes

2026-10-24 coord-intake-1024, from #789 review B (B1, High, deferred here as the review allows): https://github.com/jlevy/squares/pull/789#issuecomment-6383901035. The 23:38:42Z push that published 964ee2b also put into Couzo's repository sides credited to Kaggle notebook authors at 99 counts in 325-1024: 87 certificates, 12 recipes, 1.46e-4 to 6.60e-2 below main's record at e5c1c64e3, disjoint from #763's counts. A certificate in a watched repository is a report from its first commit (the owner, 2026-10-14), so each is a report at 23:38:42Z, ahead of 43f666c (46 of the 99 overlap 43f666c's 126 counts, where think-cncq assumed 964ee2b's side stands). The list: scratchpad rev-789b/others-below-main-964ee2b.tsv (n327 and n994 checked against GitHub). Next: stage 1 triage of credit (notebook authors, the parents manifest), then import before think-gn29's walk; recipes wait on the D2 checker.
blocked_on: think-ptkk


2026-10-24 c-triage-lyf9-1024 (stage 1, read-only; coordinator coord-intake-1024; claude-opus-5-5 at xhigh). Nothing committed, pushed, posted, synced or edited in records. Read against main 2ec489d1e (with #789) and franciscouzo/square-packing at 964ee2b (main's retained packet couzo-issue763-2026-10-23, gzip indexes and best manifest, bound to the pin's Git blobs) plus the blobless clone (tree reads, one batched blob fetch; nothing in it run). Tools and outputs: scratchpad triage-lyf9/ (lyf9_verdicts.py, lyf9_earlier.py, lyf9_commits.py, lyf9_later.py; verdicts.json, commits.json, later.json, parents-manifest-964ee2b.json). Project interpreter only, nice, at most 2 workers, about 2 CPU-min in all.

THE SET (independent re-derivation)
- certified_bounds.json at 964ee2b has 473 entries at 325-1024 not credited to Couzo; 141 lie below every member of main's start now (tree_members(read_on=2026-10-24), Göbel decided exactly as p + q sqrt2). 42 of those are earlier publications (in the history scan or f1ceee4's receipts): PingYou rationalizations about 1e-23 below their own rows, Friedman's off-centre constructions, Göbel/Ellsworth forms. The other 99 are exactly review B's list.
- Every one of the 99 is 1.46e-4 (875) to 6.60e-2 (923) below the least member of main's start, below Göbel's construction by 2.43e-3 to 0.85 (Göbel is the least member at 11 counts), and restates nothing. The margins agree with review B's to 0.1% relative. upper_bounds.json's verified lane equals the certified bound at all 99. No #789 row (couzo-issue763 or couzo-964ee2b) sits at any of the 99 counts.
- The 87 certificates: every header side equals the index side and every SHA-256 equals the index's (9,780,397 bytes raw). 77 supersede a current row (Polkovskyi 50: f1ceee4 30, #719 12, #732 8; Couzo 24; Muglich 3) and 10 replace the grid (376, 537, 604, 685, 738, 761, 793, 861, 920, 971).
- The 12 recipes are square-tiling-and-L-border constructions on certificates among the 87: 445 and 488 from 404 (1 and 2 layers), 580 from 533, 679/732/787/844/903/964 from 628 (1-6 layers), 913 from 854, 967 from 906, 859 from 802. Each source bound matches its certificate.

FIRST COMMIT (history-scan check)
- None predates efef7d1: no (n, side) of the 99 in history-publications.json (franciscouzo to 6b7391d, evand 7982d7a, Fang 9ffba0f, de Winter 206c7fc) or f1ceee4's receipts; neither index nor best/root certificate at 6b7391d states any; none of the 87 certificate blobs appears at any path in the 41 commits before efef7d1. No earlier report in any of the 10 ledgers with steps at these counts (986 steps: 691 recorded, 283 not, 12 undecided) states a side at or below the 99's. No parent in the parents manifest at these counts (60 parents, credited to Couzo, de Winter, Daniel, Friedman) is at or below.
- fa6237e (39): 327 330 340 404 406 409 445 446 454 488 509 533 537 541 579 580 589 628 633 679 685 732 735 787 790 791 793 844 846 854 856 903 906 913 964 965 967 971 975. These are Tymchishin's "CPU Alternating Reclosure" v3 and Lavrentev's "CUDA Packing Search" v11.
- 964ee2b (60): the other 60. efef7d1: none. Each blob first appears at the commit that first states its side. All three commits were pushed together at 2026-10-23T23:38:42Z (PUSHED_LATER), so every one of the 99 is a report at 23:38:42Z; under think-gn29's one-report-per-commit labels they are @fa6237e and @964ee2b.

REPORT ORDER AGAINST LATER REPORTS
- 43f666c (pushed 06:10:44Z with 73eac5b and 1c17153; the saved copy is bound to the tree by blob id): it is below the 99's side at 46 counts and unchanged at 53. 1c17153 changes nothing at the 99. The 46 are 330 340 376 377 405 411 451 455 488 504 508 509 594 596 604 637 653 679 691 697 706 732 738 745 746 748 751 755 761 787 807 816 844 856 858 867 903 918 919 924 929 964 975 981 984 994. By finder of the 99 side: Tymchishin 15, Luecke 11, Raza 8, Lavrentev 6, Chilton 6.
  - Margins are 5.04e-12 (377) to 1.33e-2. None restates (every gap exceeds 1e-12 and every 12-place print differs), so all 46 are recorded after the 99, as Couzo's refinements ("Francisco Couzo (square-packing live search); refines the packing of <author>"). 41 are certificates; 5 are recipes from 43f666c's 679 (732 787 844 903 964), held for D2 beside the 99's own recipes there. At 488 and 679, 43f666c's certificates follow the 99's held recipes.
  - 18 of the 46 are under 1e-10 below: 377 405 411 455 508 596 604 653 697 706 738 746 748 761 807 816 919 984, by 5.0e-12 to 3.05e-11. That is of the order of the manifest's witness_dilation 1+1e-12 (side x 1e-12 is 2.0e-11 to 3.2e-11). measured_identity at 377, 405, 596 and 984 gives the same packing: one-to-one under symmetry 0, every centre within 4.3e-11, rotations within 2.7e-9 degrees. These are Couzo's tighter re-certifications of the notebook authors' packings, recorded under the current print rule (T-146 / evand-268 precedent).
- evand 8a8879a (pushed 04:53:53Z) holds only s268/s303/s304 candidates. Its other pushes since the scan (5e862ac at 03:58:45Z, 659ee62 at 05:02:45Z) change no certificate or index outside 268/303/304. So evand reports nothing at the 99 counts. GitHub's activity API, read at 13:55Z, shows no push to either repository after 06:10:44Z.

VERDICTS (proposed, report order, read on 2026-10-24)
- Recorded: all 99 (no restatement; none above Göbel; no earlier report at or below). 87 certificate rows; 12 recipes recorded and held for the D2 maintained construction checker, as #763's 13 (think-g2qy).
- After think-gn29, at the 46 counts:
  - 39 of the 87 certificate rows are superseded by 43f666c certificates;
  - at 488 and 679, 43f666c certificates follow the 99's held recipes;
  - at 732, 787, 844, 903 and 964, both are held recipes.
  At the 53 unchanged counts, 48 certificate rows stay current and 5 recipes stay held (445, 580, 859, 913, 967).

CREDIT (from the best manifest's provenance; the parents manifest names no notebook author at these counts)
- Kirill Tymchishin (kirilltym), 52:
  - "CPU Alternating Reclosure" v3, https://www.kaggle.com/code/kirilltym/22-408512-cpu-alternating-reclosure, run 361239073, licence Apache-2.0 per the manifest: 37 (26 certificates, 11 recipes), first at fa6237e;
  - "22-3662-cpu-cuda-mps-eda-union", run 361576574, licence "per the notebook": 15 certificates, at 964ee2b.
- kyleluecke, "inos-v0-6-k-mosh-squares-in-squares-22-366222", run 361592092, "per the notebook": 18 certificates, at 964ee2b.
- alexchilton, "fault-line-dp-basin-hopping-lb-22-3747", run 361412241, "per the notebook": 11 certificates, at 964ee2b.
- aqibrazadev, "squares-in-squares-top-lb-blending-visualization", run 361516058, "per the notebook": 9 certificates, at 964ee2b.
- Vladislav Lavrentev (lightningv08), 9:
  - "CUDA Packing Search" v11, run 361263594, Apache-2.0: 330 and 509, at fa6237e;
  - the same notebook, run 361589987, "per the notebook": 6 certificates plus the 859 recipe, at 964ee2b.
- Every entry says "earlier construction credits retained in the notebook" (or "in its source notices"). The SOURCE_NOTICES.md the two Apache entries cite (submissions/kaggle-public-portfolio-20261022/) is not in the tree at 964ee2b. Five notebooks give a run but no version.
- Names: the source names only Tymchishin and Lavrentev. For the three handles, Kaggle's public profile pages (read 2026-10-24T13:52Z) title them "Kyle Luecke", "alex chilton" and "Aqib Raza". By attribution.md a handle stands only where the sources give no other name, so those pages are the evidence a profile would cite; a surname needs its own provenance.
- Profiles needed: Kirill Tymchishin and Vladislav Lavrentev (no person record yet; occurrences.yaml has both "identity review pending (think-ptkk)"), plus three new ones (kyleluecke, alexchilton, aqibrazadev). They are needed before think-gn29's "Couzo after <author>" credits as well.
- Rows carry no credit; the coverage source's key does. The import therefore needs its own coverage sources and bibliography keys, not couzo-964ee2b-2026-10-23 (Couzo's). Use one per notebook (7; keeps run, version and licence on one key) or one per finder (5). That is the coordinator's choice.

LICENCE (question for the coordinator; review A's A7)
- The stage 2 presumption does not cover these, by its own text: "Files of others inside the source keep their own basis, such as their stated licence or the retained-factual-data decision". The submitting author is Couzo, and #763 itself excludes the notebook packings ("the index also holds notebook packings by other authors, which the issue says are not part of the request").
- Proposed basis: the owner's retained-factual-data decision of 2026-10-09 (certificates are factual data), as #789 used for the 268 parent. The Apache-2.0 the manifest states covers 28 of the 87; the other 59 say "per the notebook". A licence follow-up bead (like think-m8f4) records each notebook's licence; it should not hold the import.
- To confirm: (a) that the factual-data basis is enough for 87 third-party certificates republished in a watched repository, and (b) whether the owner's presumption question on #789 should also name third-party files.

PRICE
- Replay of 87 certificates on both maintained routes with six controls each. Fitted to #789's receipt (wall_seconds per row ~ n^1.15; mean n 676 here, 695 there): about 2,100 worker-seconds, about 18 min wall on 2 workers. In #789's CPU accounting (43 CPU-min for 184 rows) that is about 0.3 CPU-h, about 12.6 CPU-s per certificate, close to the 10 CPU-s the #763 triage assumed (0.24 CPU-h).
- Göbel comparison and starts: seconds. The 12 recipes: seconds once the D2 checker exists (W7). Pose identity for 18 pairs (think-gn29): under a minute.
- Custody: 87 certificates of 9.8 MB raw join the existing packet couzo-issue763-2026-10-23. Stage 2: "files added later from the same revision join the packet they belong to"; 964ee2b is that packet's pin. This is about 3 MB as a thin pack, well inside OR-18 (#789's 86 MB raw went in at 15.1 MB); run check_added_blobs before the first commit. No in-corpus count, so no stage 4 review and no adoption.

PROPOSED DISPOSITION AND PLAN
1. One import PR (W1-type, records), before think-gn29.
   - Packet: add the 87 certificates to couzo-issue763-2026-10-23. Its README's "Not imported here" paragraph becomes the import; its licence paragraph names the factual-data basis and the 28/59 split.
   - Claim map: couzo_763_claims gains an `others` list (the 99, with notebook provenance); its receipt holds the selection.
   - Ledger: a new directory, e.g. upper-bounds-couzo-964ee2b-notebooks-20261024, frozen at main 2ec489d1e, with reports @fa6237e (39) and @964ee2b (60), both dated 23:38:42Z, and rulings restatement plus classical-constructions.
   - Replay: the 87 on both routes with controls.
   - Register: 87 beyond-horizon rows (77 supersessions, 10 new); 12 recipes held (a sibling of think-g2qy, or think-g2qy widened); coverage sources, keys, evidence and the profiles above. No T-NNN (no corpus count).
   - Draft significance: as #789's 964ee2b rows (below S4, so no project issue unless rated higher).
   - Acknowledgement: no issue exists. Reply on #763 to Couzo, the publisher, after merge, with the author questions below.
2. Order:
   - this PR, then think-gn29, whose walk takes the 99 as earlier reports at 23:38:42Z;
   - think-llit's W7 is independent for the 87 certificates. Both touch beyond_horizon_replay.py and source-coverage.yaml, so whichever lands second rebases;
   - only the 12 recipes wait on W7's D2 checker.
3. Retained-tool proposals (OR-1):
   - the selection and exact decision (lyf9_verdicts.py) go into devtools.couzo_763_claims as `others`;
   - first-commit dating, header reads and earlier-publication checks (lyf9_commits.py, lyf9_earlier.py) are what devtools.beyond_horizon_replay's first_commits / earlier_publications do once the 99 are a declared release on the packet;
   - the 43f666c comparison (lyf9_later.py) is think-gn29's later_reports / decide_later walk, with pose_identity on the 18 sub-1e-10 counts.
   None of the probes should be kept as written.

AUTHOR QUESTIONS (Couzo, with the reply on #763)
1. Do you claim any part of the 99, or is each notebook author the finder? At 994, for example, the manifest's previous_reference is your Kaggle push packing seeded from Lavrentev's, and aqibrazadev's is a "top-lb-blending" notebook.
2. Which version of each of the five notebooks that give only a run (Tymchishin's 22-3662, Luecke's, Chilton's, Raza's, Lavrentev's run 361589987), and what licence and source notices does each state? Could you commit submissions/kaggle-public-portfolio-20261022/SOURCE_NOTICES.md, which the manifest cites?
3. Are kyleluecke, alexchilton and aqibrazadev Kyle Luecke, Alex Chilton and Aqib Raza, as their Kaggle profiles show?
4. (for think-gn29) At 18 counts 43f666c re-certifies the notebook packing 5e-12 to 3e-11 lower (the same packing at the four measured). Is "Couzo after <author>" meant as a new packing or as a tighter certificate of theirs?

CHANGES FOR think-gn29 AND PR B
- think-gn29:
  - verdicts unchanged: think-cncq already compared against 964ee2b's index sides, which are the 99's at the 46 counts;
  - the rows it supersedes at those 46 are this import's, credited to the notebook authors, not #763's or main's older rows;
  - its walk needs the 99 as earlier reports (land this import first, or declare them in its sources), the PUSHED_LATER entry for 06:10:44Z (A8), profiles for the five finders, and pose identity on the 18 sub-1e-10 counts.
- PR B of #763 (T-240 review, adoption at 268/303): unaffected; the 99 are all at 325-1024 and evand reports nothing there.

INCIDENT: at 13:40Z my `git ls-tree -l` on the blobless clone lazily fetched about 3,474 blobs (114 MB) plus a failed 34 MB auto-gc temp pack, during the disk-full window. I removed the two garbage temp packs. I then rewrote the clone's 47 commits and 122 trees into a new promisor pack (f40cac7f) and dropped the 115 MB pack, returning the clone to blobless (14 MB, all history and trees intact; the dropped blobs re-fetch on demand). Another process fetched about 420 MB into the same clone at 13:46-13:47Z; that was not this lane.

blocked_on: think-g2qy (the 12 recipes only, via think-llit's D2 checker); the 87 certificates are unblocked since #789 merged as 2ec489d1e
