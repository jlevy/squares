---
type: is
id: is-01m41gv134xbbtnamrd9nn94x9
title: "Merge main (PRs 292 and 311) into PR 305: renumber to T-080..T-084 and reconcile the floors"
kind: task
status: closed
priority: 1
version: 7
labels:
  - session-169
dependencies: []
parent_id: is-01m3xgkna3m3w1w50ky6gqyxyk
created_at: 2026-10-03T18:36:19.940Z
updated_at: 2026-10-04T00:37:47.353Z
closed_at: 2026-10-04T00:37:47.352Z
close_reason: PR 305 merged with main through d303e9ef8 (four merges, results T-083..T-087), green at 0952efb57; PR 323 caught up.
resolution: null
duplicate_of: null
---
Main merged jlevy/squares#292 and #311 on 2026-10-03 (228 commits): T-066..T-079 are now wand125's rectangle-density and mixed-cover certificates (replayed at coverage one; s(59) = 8, s(77) = 9, and floors from n = 19 to 105) and two s(12) bounds, none resting on Nagamochi; main also added a generated Verification Code section to all 324 case records. PR 305 conflicts in 67 files (46 case records). Done so far: this branch's results renumbered T-066..T-070 -> T-080..T-084 (commit ff4157988, held on local branch hold/renumber-t080 until the merge, since alone it breaks the register's contiguity). Lane E (Opus, max effort) merges: T-007 stays V0; each case takes the strongest verified floor, never Nagamochi's; both sides' dated prose kept and adjusted where superseded; T-084 is superseded at n = 37 (6.44, T-069) and n = 61 (s(61) = 8) and stays registered by the register's precedent; generated views regenerated; counts re-derived; re-pin alone if needed.

## Notes

2026-10-03, first merge (lane E): main's #292 and #311 merged into PR 305 as e617ae4b1 (re-pin bcb8bdba5, record merge 19d5830bd), fast-forwarded and pushed with the n-034 prose fix d58796b2d and re-pin 309f5fd05. This branch's results were renumbered T-066..T-070 -> T-080..T-084; main's certificate floors won all 45 cases both sides moved; 225 floors still correct Nagamochi 2005 (from 265); T-084 (then; Bašić-Slivková) superseded at n = 37 and 61 and kept registered; the negative-controls snapshot cap was raised 192 -> 224 MiB and the index page test ceiling 4.3 -> 4.7 MB, each with a dated reason (lane B's stacked re-layout brings the snapshot to 178 MiB, so the cap can return to 192 MiB once re-measured).
2026-10-03, second merge (in progress, lane E resumed): main then merged #320 and #322 (79419cdfc), registering T-080 (wand125, s(101..105) >= 257/25) and T-081 (Evan Daniel's s(k^2-4) = k for k >= 5, 14 cases). This branch's results renumber again to T-082..T-086; the k^2-4 half of H-269 is settled by T-081 and gets a dated update.
2026-10-03, second merge done (lane E): d59ee8c9b renumbers alone (T-080..T-084 -> T-082..T-086), 4dee381d4 merges main at 79419cdfc with 20 conflicts resolved, e49798ecc re-pins alone; pushed with the session record 57a525f0d. n = 101..105 take T-080's 257/25 and drop the tag; the eight k^2-4 cases keep Karakus's verified floor with a dated update (T-081 is reported); H-269 gains a dated update, its frozen contract unchanged; 220 floors correct Nagamochi 2005, 188 open cases rest on Karakus. The results page test ceiling was raised 2,800,000 -> 3,000,000 bytes (the merge renders 2,823,439); owner item think-5o8i. Checks: --records, --edit, --sweeps, --push but the two host-only reaping tests, and every record check.
2026-10-03, third merge (lane E resumed 23:04Z): main merged #327, #324 and #328 (0ca18df47) during the second merge, registering its own T-082 (wand125's 22 mixed certificates at n = 51..96, V0/C1) and replaying T-073 and T-076 to V3/C3. This branch's results renumber again to T-083..T-087.
2026-10-04, third and fourth merges done (lane E): 9a2788dec renumbers alone (T-082..T-086 -> T-083..T-087), c4df7e85a merges main at 0ca18df47 (16 conflicts), fa85487ec re-pins, ed78a6b51 merges main at d303e9ef8 (#329, #331: T-064's second Valid7 replay; only INVENTORY and the pin conflicted), d56b9f503 re-pins. T-082's 22 values sit in the reported lane only; n = 82 rises to 233/25 (T-076 V3/C3) and drops the tag; n = 83 keeps 937/100 with T-073 below it; the nine k^2-3 cases stay proved. 219 floors correct Nagamochi 2005, 187 open cases rest on Karakus, 87 results registered (58 by others). No ceiling raised. Hosted CI green at 0952efb57 (run 37164605808, full re-run after a typecheck wall breach, think-4w2g); session-169 closed at 99defa2ea. PR 323 caught up at aa6e0957d and 3b1dde308. Any later merge of main that registers a result renumbers again.
