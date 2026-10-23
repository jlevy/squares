---
type: is
id: is-01m5kjb20ed6wb6c1zbp2my2xc
title: "Apply the owner's D1 answer: track beyond-horizon rows above 1024 (#666, #715, #719, #732), with a hosted-data manifest for the bulk certificates (think-f2io, 2026-10-23)"
kind: task
status: in_progress
priority: 1
version: 3
delegate: c-triage-1024-1023
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-23T05:04:35.342Z
updated_at: 2026-10-23T06:21:28.780Z
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
