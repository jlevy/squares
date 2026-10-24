---
type: is
id: is-01m5kjb20ed6wb6c1zbp2my2xc
title: "Apply the owner's D1 answer: track beyond-horizon rows above 1024 (#666, #715, #719, #732), with a hosted-data manifest for the bulk certificates (think-f2io, 2026-10-23)"
kind: task
status: in_progress
priority: 1
version: 8
delegate: c-plan-1024-llit
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-23T05:04:35.342Z
updated_at: 2026-10-24T10:18:46.750Z
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
