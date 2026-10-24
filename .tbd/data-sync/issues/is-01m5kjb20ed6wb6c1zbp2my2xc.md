---
type: is
id: is-01m5kjb20ed6wb6c1zbp2my2xc
title: "Apply the owner's D1 answer: track beyond-horizon rows above 1024 (#666, #715, #719, #732), with a hosted-data manifest for the bulk certificates (think-f2io, 2026-10-23)"
kind: task
status: open
priority: 1
version: 22
spec_path: docs/project/specs/active/plan-2026-10-24-rows-above-1024.md
delegate: null
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
child_order_hints:
  - is-01m5qby09kkaa1rny3x82s2784
  - is-01m5qby16169h30h6s4cg3r70a
hold: null
hold_until: null
created_at: 2026-10-23T05:04:35.342Z
updated_at: 2026-10-24T18:33:16.285Z
started_at: 2026-10-23T05:05:14.273Z
---
Owner decision of 23 October (think-f2io note): yes, no ceiling. Needs a plan: the rows' walks above 1024 (report order), custody without Git blobs (D4 hosted-data manifest; OR-18), the replay price at thousands of certificates (compute cap), and the frontier README rule. Stage 1 triage and pricing first, read-only.

## Notes

2026-10-23 c-triage-1024-1023 (stage 1, read-only; files in the coordinator scratchpad triage-1024/: claim-map.md, tools/, data/). Summary:
- Sources above 1024: #732 5,078 counts (5,077 at head 7b6366f; 5,208,759,377 B of files; author's zip 350,285,426 B); Couzo 5a299b4 index 5,078 non-grid (95 certificates, 187 deletions, 4,796 tiling/L-border recipes); #715 1,112 counts (~129 files, 825 recipes, 158 deletions); Fang bef5c42 62; #666 8; #719 8; Kingbird 4 (1453, 1765, 1850, 2043); Daniel 49907ec 2 (1092, 1228); Barnett d2356fa 1 (2043, below every other report).
- Rows under today's rules (D1 only): 4,489 rows at 4,345 counts (#732 4,319), 5,430 held (D2 4,787; D6 172; above Goebel 467; N1 4). Every row A: 9,919; scenario B (recipes/deletions/catalogue out, Goebel as earlier report): 4,743.
- Price (19-certificate sample on both maintained routes, all 24 controls refused): positives for everything above 1024 ~17.2 CPU-h; #732 with all six controls ~157 CPU-h; D2 recipes written out ~98 CPU-h. Under a 40 CPU-h cap: all positives + controls for every source but #732 + 10% of #732's controls + a 3-count kernel sample, ~36 CPU-h.
- Custody: #732 ~273 MB (~128 MB as nine tar.xz shards) as a hosted release the owner publishes; Couzo ~13 MB (host or commit); Fang 4 MB, #719 0.06 MB, Daniel/Barnett < 0.2 MB in Git.
- Code: LIMIT = 1024 in beyond_horizon_replay.py:174 (uses at 335, 1126-1137, 1502, 1569, 1668, 1690, 1900, 1953, 2033, 2055, 2998) and couzo_715_replay.py:113; Goebel module only to 1073-1100; hosted reads via sqpack.hosted_data.require; intake_ledger summary README; gate cost re-measure; frontier/README rule text; no site page lists rows (a table above 1024 would be ~1 MB).
- PR plan: PR-0 #742; PR-1 code (W7); PR-2 records for #666/#719/#715/Fang/Barnett (~3.5 CPU-h); PR-3 #732's 4,319 rows with the hosted manifest (~32 CPU-h under cap, or 157 on the owner's word); PR-4 held rows after D2/D6/Goebel answers.
- Owner questions: D2, D5, D6, #613/think-8krd (Goebel), N1 (Kingbird beyond 324), N2 (#732 controls compute), N3 (hosting form), N4 (one source-coverage file or split), N5 (site shows rows above 1024?), N6 (pin #732 at 17cc220 or 7b6366f).

2026-10-23 coord-intake-1023: OWNER DECISIONS (in conversation, 23 October): N2 #732's compute stays UNDER the 40 CPU-h cap: all positives on both routes plus six controls on a stratified 10% of #732's files (~36 CPU-h with the rest); N3 hosting as nine tar.xz shards (~128 MB) that the owner publishes as hosted data (agents stage the manifest only). Goebel is the baseline (think-8krd: yes); recipes become rows via a maintained checker (think-f2io D2: yes). Still open: D3, D5, D6, N1, N4, N5, N6.

2026-10-23 c-fix-754b-1023 (PR https://github.com/jlevy/squares/pull/754, review B, B3: https://github.com/jlevy/squares/pull/754#issuecomment-6376229374). The refusal above 1073 refuses a whole input, not only its counts above 1073. From 23 October 2026 (`intake_ledger.GOEBEL_FROM`), one count above the retained Göbel program's reach (`intake_ledger.goebel_reach`, 1073) refuses:
- **an entire import**: `upper_bound_reports.compare` builds every row before it writes, so a declaration read from 23 October with one claim above 1073 refuses the packet (`construction_side` raises, re-raised as `ReportError`);
- **an entire earlier-publications receipt**: `beyond_horizon_replay.standing_sides` maps every claimed count, those above `LIMIT` included, and raises `ReplayError`;
- **an entire gather**: `tree_members` adds Göbel's construction at every count beyond 324 and refuses above 1073 ("FAIL gather: n = 1074: the retained Göbel program gives no side above 1073"); `check --tree` fails the same way (`test_tree_drift_reports_goebel_s_member_only_from_23_october`).

#715 and #732 claim counts up to 9913, so the above-1024 work must handle this before any import, receipt or gather above 1073: extend the program's reach and re-verify it against a larger build (review A of #754 matched it against a 5000 build to 1073), or split every input at 1073.

Two more obligations from review B1 (`intake_ledger.answer_problems`, #754): a ledger read from 23 October lists the `restatement` ruling through its top count, so the 66 counts above 1024 where #732 is below #715's print by less than 1e-12 (think-f2io) are walked under it; and it applies Göbel's baseline at every count it walks beyond 324, through its `classical-constructions` ruling or a frozen start member. A ruling it does not apply at some count, as Göbel's above 1073, is named under `rulings_not_applied` with the reason, or `check`, `render` and `gather` fail.

2026-10-24 coord-intake-1024: released (no live lane after the interruption of coord-intake-1023's session); open for the next lane. #763's 233 rows above 1024 join this walk (think-cnn7's plan).

2026-10-24 coord-intake-1024: the plan landed as PR #791 (docs/project/specs/active/plan-2026-10-24-rows-above-1024.md) after review A (approve after six Mediums; all 17 findings fixed, dispositions https://github.com/jlevy/squares/pull/791#issuecomment-6383725520). Slices: W7 code (after #789), R1 (~4.3 CPU-h), R2 #732 (~32, owner publishes the hosted shards first), R3 (#763/964ee2b/43f666c, ~0.1), R4 (held rows). Open owner questions with the coordinator's recommendations: D5, think-kzme's sub-question, N1, N5; D4 recorded as the record's disposition (hosted data/couzo-715-certificates-v1). Next: W7 after #789 merges.

2026-10-24 c-w7-1024 (W7, branch claude/w7-2026-10-24-rows-above-1024-code). Design questions and findings, for the coordinator:
- STOPPED ON (plan wrong against the code): "The RECIPE hold class becomes settled for every recipe the checker decides. D2's answer applies as Held.answer, the way DELETION_ANSWER applies D6's." In the code an answered Held means the publication has NO row (held_problems refuses a row at any held count; declared_rows skips held counts; held_sentence prints "have no row by {answer}"), while D2's answer makes a decided recipe a row. W7 therefore does not settle recipes through Held.answer: a recipe the walk records and does not hold is a declared row carrying its recipe, decided by devtools.construction_checker into receipts/recipe-decisions.json, and the RECIPE class holds only recipes the checker refuses (classical parents, think-zkxy; Fang composites). No frozen walk changes: every recipe in them stays held as written. If the coordinator wants the Held.answer form instead, that is a change to Held's meaning (an answer that settles a publication AS a row), which the plan should state.
- Fang composites: the plan says the checker "refuses a Fang composite unless his table states the composite's parts", but states no rule for deciding a composite whose parts are stated. W7 refuses every composite, naming unstated parts when the table states none; a composite rule needs its own decision.
- The summary README threshold is 400 walked counts (intake_ledger.SUMMARY_FROM): above every retained walk (the history walk walks 392 counts, its README 339 kB), so every frozen README renders byte for byte.
- Base finding, not W7's: the #678 Goebel receipt (couzo-issue678-2026-10-18/receipts/goebel-comparison.json) does not rebuild byte for byte at main 2ec489d1e: couzo_678_replay.goebel writes families "... and corner-touching strips ..." where the committed file says "... corner-touching Goebel strips ...". Left as committed; a one-line records fix for a later slice.
- For R1: history-publications and earlier still scan HISTORY_COUNTS (325..1024); scanning the watched repositories above 1024 is R1's change, with the walk above 1024's name in WALKS (above=1024, through=None), Release.walk_above on each lifted release, CLAIM_MAP_WALKS/WALK_READ_AT_MAIN entries, and Barnett's repository in WATCHED_HOLDERS.

2026-10-24 c-w7-1024: W7 is draft PR https://github.com/jlevy/squares/pull/793 at 6d44159fc (S2, project), every hosted check passed; records nothing.

2026-10-24 coord-intake-1024 on W7's two stops (PR #793 at 6d44159fc): (1) RECIPE hold: confirmed as built. The owner's D2 answer is that recipes become rows via a maintained checker (think-f2io), so a decided recipe is a declared row and the RECIPE class holds only recipes the checker refuses; the plan's 'as Held.answer' wording is wrong against the code and is corrected in #793's review round. Not an owner question. (2) Fang composites: refusing every composite until a rule exists is the safe default; a bead holds the rule.

2026-10-24 c-w7-1024, PR #793 round 1 (reviews A senior, B correctness, C security; one push). Fixed: A1 A2 A4 A10 (plan and rule text: a decided recipe is a declared row, RECIPE holds refused recipes only; composites wait on think-tj3x; a deletion is no recipe row, D6 or think-kzme; "capacity less the stated deletions"), A3 and B3 (one Hosting per call: acquisition record, manifest and receipts read once, tested at 5,000 hosted rows; one pinned-entry helper for side and blob; is_hosted is hosted_pins' predicate), A5 (byte-change refusals tested), A6 (recipe_pin_problems), A7 and C1 to C4 (hosted_shards: counting reader under tarfile stream mode bounds pax and long-name records; per-member bound 64 MiB; chunked hash before publish; DIR-members/STEM; ShardError at the root; members dir inside the repository; the unused `sizes` check dropped, no source states sizes), A8 with B2 (recipe certificate_n = source_n; claim_side tS + L in decided_sides and release_sides; a recipe row is dated by the index commit that first states its recipe, and first_commits refuses one until R1 reads index history), A9, A12 (evand_exact_certificates.header shared with header_side; release record amended, 51/51 renders identical), B1 (#719 sources read #666 above FROZEN_THROUGH; lifted-#666 test), B4 (later_publications refuses a receipt below its walk), B5, B6. Deferred: A11 -> think-z236 (R1), A13 -> think-j83l. Review C's out-of-diff load_manifest note -> think-eyrn. Each new test fails with its fix mutated out (13 of 13). No record changes.

2026-10-24 c-w7-1024: #793 round 1 pushed as acb59dba11f98bf2b8331f00e6a7e32a9e8b7b1d (fixes c3bb93b47, 72e2eba50, ae6c93fe0, acb59dba1); main had not moved, no merge. CI green: Packing validation 40113441342 (attempt 1), Certificate page 40113441337 (attempt 5; earlier attempts failed on HTTP 502 from the jobs API in wait_for_run_artifact, think-nnk7). Dispositions replies: A issuecomment-6387505266, B -6387505446, C -6387505611. Open from this round: think-z236 (A11, R1), think-j83l (A13), think-eyrn (C, outside the diff), think-nnk7 (CI waiter).

2026-10-24 c-w7-1024, PR #793 round 2 (review D, follow-up; one push): head b28584668e4a55df4e6202694c959ae8be39c15c. Fixed in 4e7a218b3: D1 (stream allowance starts at MAX_HEADERS and grows per admitted member; C1 test at the shipped bounds; review C 512 MiB records refused at the defaults, peak RSS 55 MiB), D2 (member-read errors are ShardError), D3 (a link anywhere below the members directory refused), D4 (release_sides clone branch tested), D5 (receipt without limit refused), D6 (header_side in both branches). 5 of 5 mutations detected. Merged main 3480b5fd3 (#792) as 96bbef3b5: one conflict, two no-change records in release.py, both kept; W7 record re-measured in b28584668 (51/51 identical); release_pin current (3a9c5b60); site_urls --history-ref origin/main passes. Validation: 1,059 tests passed, rebuild driver clean, --records 53/53 (148 s). CI green first attempt: Packing validation 40120155316, Certificate page 40120155325, mergeability 40120151956; PR MERGEABLE. Reply D: issuecomment-6387969029.

2026-10-24 coord-intake-1024: W7 landed as PR #793 (dd0061553, merged 2026-10-24T18:32:59Z) after review A (senior), B (correctness), C (security) and follow-up D, all dispositioned; hosted CI green first attempt at b28584668. Phase 1 done. Next: R1 (records: #666, #719, #715, Couzo 5a299b4, Fang, Barnett; owner to publish data/couzo-715-certificates-v1 first, D4), then R2 (#732 under N2, owner publishes the #732 shards), R3 (#763's 233 rows, 964ee2b's 6, 43f666c's 831 recipes after think-gn29), R4 (held rows after D5/kzme/N1/N5). Open: think-z236, think-j83l, think-eyrn, think-nnk7, think-tj3x.
