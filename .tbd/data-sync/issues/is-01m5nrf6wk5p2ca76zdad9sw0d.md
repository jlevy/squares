---
type: is
id: is-01m5nrf6wk5p2ca76zdad9sw0d
title: "Triage #763 (Couzo, 23 October 23:35Z): 436 improved upper bounds at 268-9802 (203 at or below 1024, 233 above), source franciscouzo/square-packing@964ee2b"
kind: task
status: in_progress
priority: 2
version: 5
delegate: c-triage-763-1024
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T01:30:11.731Z
updated_at: 2026-10-24T05:27:46.840Z
started_at: 2026-10-24T01:30:16.579Z
---

## Notes

2026-10-24 c-triage-763-1024 (stage 1, read-only; coordinator coord-intake-1023). Nothing committed, pushed or posted. Read against origin/main 0bbb0a2c4, #757 head 01d5c60f (T-239 at 303), PR C's data f1ceee4 (Mishapolk/square-packing-records), #745 d8138ad5 and #756 7bc4cae1. Data and tools: scratchpad triage-763/ (data/out/claim-map.tsv, above1024.tsv, unrequested.tsv, above1024-unrequested.tsv, credit-families.tsv, needed-certs.json, claim-sides.json; tools/*.py; ack-763.md).

SOURCE AND TIMING
- Pin franciscouzo/square-packing@964ee2bdf301d0c8912d956d4010f478dcbbd5ea, committed 22:38:09Z. GitHub's activity API shows efef7d1, fa6237e and 964ee2b pushed together at 2026-10-23T23:38:42Z, 2 min 51 s after the issue (23:35:51Z). Either time is after PR C's f1ceee4 report (#732 comment, 20:35:12Z), so the order is the same.
- SHA-256: upper_bounds.json 212b33b6, certified_bounds.json f368786a, manifest.json d95f2bd6, public_bounds.json dca2d4b6, certificates/best/SHA256SUMS db25312a. The per-certificate digests in the index match the files at 268, 303, 684 and 1647.
- Licence: none for data or prose. GitHub reports MIT from BOUND_VERIFIER_LICENSE.txt, which is Evan Daniel's verifier licence ("modifications by Francisco Couzo with Codex"), as in the #715 packet. Retain the certificates as factual data under the 2026-10-09 decision. AI assistance is stated only in verify_bound_certificate.py (Codex). The licences of the Kaggle notebooks the parents come from were not read; check them at stage 2.

CLAIM MAP
- The issue body has no table: it ends at the Refines legend, it has 0 comments, and the timeline is empty.
- Reconstructed from certified_bounds.json, using the README's selection rule: strictly below the 12-place print against Couzo's own comparison, more than 1e-10 below another author's (the leaderboard is replaced by its superseded_review). The rule as the issue states it gives 450, with 14 more at 335-998.
- That reconstruction gives 436 = 203 at or below 1024 + 233 above, 196 certificate rows (194 own-count certificates plus deletions 683 and 1646 from 684 and 1647), and −d at exactly 683, 1646 and 1727. All of these match the issue.
- Two counts do not match: refines 351 against the issue's 345 (A 253, B 94, C 1, E 1, and 2 from Tymchishin's "22-3662-cpu-cuda-mps-eda-union" notebook, which the legend omits; D 0). Leaderboard-smaller is 182 against 180.
- Kinds:
  - corpus: 268 and 303, certificates;
  - 325-1024: 186 certificates, 14 L-border recipes (365, 444, 487, 632, 733, 734, 737, 788, 789, 845, 909, 910, 966, 970; the own-count best/ files at those counts are older and looser) and 1 deletion (683);
  - above 1024 (1029-9802): 6 certificates (1486, 1647, 1648, 1765, 1898, 2263), 1 deletion (1646) and 226 recipes, one of them recipe plus deletion (1727, from 1647 +1L −1). Their source counts: 1765 (57), 905 (23), 986 and 990 (15 each) and 19 more.
- Files the replay needs: 194 distinct certificates, 26.9 MB raw (188 at or below 1024, 24.3 MB; 6 above, 2.6 MB). At Couzo's zlib ratio of 4.3-6.5 that is about 4-6 MB in Git, so Git, as with #715; run check_added_blobs before the first commit.
- Every requested side changed since the #715 pin, 6b7391d.

VERDICTS
- Method: exact Fractions against intake_ledger.tree_members(read_on=2026-10-24), which gives both case lanes, pending entries, beyond-horizon rows at exact sides, and Göbel above 324, read as spans. On top of that, PR C's 138 f1ceee4 rows wherever they are below main, and #757's T-239. Above 1024 the comparison set is Kingbird, Daniel, Barnett, Fang, #666, #715 prints, Couzo's 6b7391d index, #719, #732 at 7b6366f, the grid and Göbel to 10000 (the above-1024 triage's reimplementation).
- corpus: 268 and 303 are below every member.
  - 268: 16.874361715874, against T-174 16.878814821007 (−4.45e-3).
  - 303: 17.906978233799, against T-230 17.909772217275 and #757's T-239 17.909762327476 (−2.78e-3).
- 325-1024: 201 rows. Margins against main run from 1.75e-11 to 6.79e-2, median 2.6e-2. PR C is ahead at 98 of them.
  - 198 would be recorded: 184 certificates, 13 recipes and 683.
  - 3 restate PR C (think-fwa9): 328 (3.2e-13 below), 850 (6.7e-14) and 909 (2.6e-13). Measured at 328 and 850 against f1ceee4: the same packing, 0 squares beyond 0.1, max centre distance 5.2e-2 and 7.1e-2.
  - 365 and 970 are 8.3e-13 and 4.9e-13 below PR C. They are recorded only because PR C's exact sides round up to …496 and …500.
  - Mishapolk's index prints 70 of f1ceee4's 138 rows one unit low, because it rounds to nearest. The PR C lane must print exact sides rounded up.
  - No row is above Mishapolk's 34e59f3, c0bf150 or 7e82c64. No row is within 1e-12 of Göbel.
- Holds: the 13 recipes wait on the D2 maintained construction checker; beyond_horizon_replay still holds RECIPE, so this is a W7 slice. 683 waits on think-kzme Q1/Q2 (an issue-claimed deletion bound).
- Rows writable now: the 2 corpus counts and 184 certificate rows.
- What the 198 supersede once PR C has landed: PR C's own rows at 95 counts. At the other 103: mishapolk-issue719 40, mishapolk-issue732 22, couzo-index-2026-10-15 16, Göbel 8, couzo-verified-bounds 7, couzo-issue715 3, couzo-issue670 3, the grid 1, evand-compositions 1, couzo-reconcile 1, couzo-certificates-2026-10-14 1. Follow-ups are owed after the merge on #732 (PR C's rows and its own), #719 and #715, and on #686 if the unrequested 935 and 998 ride.
- Above 1024: all 233 are below every earlier report and below Göbel. The least margin is 2.84e-11, against Couzo's own index, at 1033/1098/1165/1234/1305/1378: these are 850 +kL rows whose gain is entirely the 850 re-certification that restates PR C. The median margin is 1.8e-2. The closest earlier report is #732 at 171 counts, 6b7391d at 60 and Kingbird at 2.
- Unrequested rows of the release:
  - 14 at 335-998. 10 would be recorded: 335, 339, 344, 379, 380, 421, 452, 507, 935 and 998. 4 restate PR C: 490, 535, 792 and 800.
  - 908 above 1024: 6 below every earlier report (850 +10L to +15L, 1530-1945), 901 not below #732, and 1 not below Kingbird.
  - By the runbook ("a claim in scope that the request does not mention becomes an import of its own"), the 10 below 1024 ride the same import as the index's publication rows. Ask the author whether he claims them.

IN-CORPUS ENTRIES (T-ids, stage 4)
By the claim table these are one entry, scope 268 and 303: "bounds of one kind at several counts in one release". Draft S3. Identity was measured in binary64 with an optimal assignment over the 8 symmetries (tools/identity.py):
- 268 against main's house (T-174, PingYou's packing): 119 squares beyond 0.1, 104 orientation changes. It is a new arrangement relative to the record. Against its stated parent, Tymchishin's EDA+Seam LP v4 packing (parents/85dbd707…): 0 beyond 0.1, max 5.9e-2, so it refines Tymchishin's. Tymchishin's packing is itself 122 squares from T-174's.
- 303 against main's T-230 (Daniel): 123 beyond 0.1. Against #757's T-239 (Kristiansen): 132 beyond 0.1. It is a new arrangement relative to both houses. Against Couzo's own Kaggle push parent (parents/22f07a7c…): 3 beyond 0.1, so it refines that parent, whose seed credit is Lavrentev's CUDA v11. No Lavrentev certificate at 303 is retained. The manifest's previous_source (Daniel T-230 at 303, PingYou at 268) is the store's previous record, not lineage: the measured distance between them is 122-124 squares.

CREDIT (chain rule: every supported link, from the source's own files)
- A, 253 rows: Couzo after Lavrentev (Kaggle "CUDA Packing Search" v11).
- B, 94: Couzo after Tymchishin ("CPU Alternating Reclosure" v3).
- C, 268: Couzo after Tymchishin ("CPU/GPU/MPS EDA+Seam LP" v4).
- 334 and 597: Couzo after Tymchishin ("22-3662…", run 361576574).
- E, 422: Couzo after Muglich (#686).
- own, 85: Couzo, keeping the chain of the row or certificate they build on. Examples: 343, Daniel and Fang two-wedge; Muglich seeds at 2; de Winter at 1.
- Exceptions to that:
  - 63 rows above 1024 built on 1765, 1647 and 1648, whose manifest entries name no seed ("ct105 recovered candidate"). 1765 is below Kingbird's Hajba/Ellsworth print. Ask the author; do not infer.
  - 970 and the 850 +kL rows refine a packing PR C refined first. Measured identical at 850, so "Couzo after Polkovskyi, Couzo" where PR C's row stands.
- Antecedents named in the notebooks' own notices are supported only once those notices are retained: stage 2 should retain them, or the author should name them. Contributor profiles are needed for Lavrentev and Tymchishin (by name, not handle). D5 (per-row credit beyond the horizon) is still open.

PRICE (owner item cap 40 CPU-h, think-lh7d)
- Replay of 188 files at or below 1024, both routes with 6 controls: about 0.4-0.6 CPU-h, about 15-20 min of wall on 2 workers. Basis: the #715 packet's 139 Couzo certificates (13.7 MB) took 1,134 CPU-s with controls, 8.2 CPU-s each; #732's 77 took 389 s of wall on 2 workers, about 10 CPU-s each.
- 6 files above 1024: about 0.06 CPU-h.
- All-pairs sample: about 0.05 CPU-h.
- 240 recipes: seconds with a maintained checker (the W7 slice costs tokens). Written out instead, about 62 MB and 0.6-1.4 CPU-h.
- Deletions: seconds.
- Stage 4 review of the 268/303 entry: one tbd-strong-max review; tokens, under 0.1 CPU-h.
- Adoption and regularization at 268 and 303: 10-50 CPU-min.
- Total about 1-3 CPU-h, so every item runs in the pass; nothing is held for the cap.

PLAN
- Order: #757, then PR C, then PR A, then PR B. think-llit's code PR, then its walk, independently of PR B.
- PR A (W1, records, S3, intake; after PR C and #757 merge):
  - packet at 964ee2b (194 certificates, indexes and manifest, the two Kaggle parents) with bibliography key and coverage;
  - ledger dir upper-bounds-issue763-2026-10-24, starts frozen at post-PR-C main, claims to 1024 only (Göbel reach 1073; the claims above 1024 go under rulings_not_applied or are excluded, since think-llit owns them);
  - a beyond_horizon_replay Release for #763 replaying the 188 files;
  - 184 certificate rows plus the 10 unrequested index rows;
  - the 268/303 entry as reported, T-id taken last;
  - 13 recipes and 683 held with beads;
  - result-requests entry and News draft.
- PR B (W2, after PR A): mapped review, V3/C3, adoption at 268 and 303 and their regularization.
- Recipes at or below 1024 and all 233 rows above 1024 (plus the 6 unrequested) join think-llit's records walk as its latest report, after its code PR (LIMIT, Göbel reach, D2 checker). 683, 1646 and 1727 follow think-kzme.

OWNER QUESTIONS: none new. Existing rules decide each point. The plan waits on think-kzme, D2's implementation (W7), think-llit and D5.

AUTHOR QUESTIONS (in ack-763.md): the table as a file; the 14 unrequested rows; seeds for 1765, 1647 and 1648; notebook versions and notices. #763 has no `intake` label.

blocked_on: none


2026-10-24 coord-intake-1023: OWNER on custody: "so Couzo's has submitted so the presumtion is permission from that. We should track a bead to follow up on the exact license, but it should not impair our ability to import things." The import retains the needed files on that presumption; the licence follow-up is think-m8f4. A general rule for the runbook, stage 2 "Retain": a source its author submitted to this repository carries a presumption of permission to retain and import, and its exact licence is followed up on its own bead without holding the import. It rides the #763 import PR.

2026-10-24 coord-intake-1023, from #769 review A7 (https://github.com/jlevy/squares/pull/769#issuecomment-6380362746): franciscouzo/square-packing `fa6237e` was COMMITTED at 18:59Z on 23 October, before f1ceee4 (20:35:12Z), but PUSHED at 23:38:42Z with efef7d1 and 964ee2b. By its header sides it lies below f1ceee4 at 131 of 138 counts. `beyond_horizon_replay.PUSHED_LATER` (~:1942) holds one push per repository. Before the #763 import walks, it must date those commits by the 23:38:42Z push (publication), or they sort ahead of f1ceee4. The triage compared the pin's commit time and the push time, but not fa6237e's commit time. Add the push to PUSHED_LATER with its evidence (GitHub's activity API) first.
