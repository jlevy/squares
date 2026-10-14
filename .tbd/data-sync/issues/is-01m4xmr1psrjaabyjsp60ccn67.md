---
type: is
id: is-01m4xmr1psrjaabyjsp60ccn67
title: "Import Kevin Fang's Section 5 composites (bef5c42): 81 beyond-horizon rows (smallest at 28 shipped and 53 table-only counts); exact replay of the 38 shipped ~122 CPU-h"
kind: task
status: open
priority: 2
version: 1
labels:
  - result-import
dependencies: []
parent_id: is-01m4wsqt2sjrksybyz375sarb3
created_at: 2026-10-14T16:43:20.665Z
updated_at: 2026-10-14T16:43:20.665Z
---
TheSnakeFang/squarepack-certs composites/ (bef5c42, unchanged at 078789a): table.csv has 230 rows over 84 counts (83 beyond 324); 38 shipped .cert files, 192 reproducible-only.

The composite is the smallest report at 81 counts, 420 to 4035. A record row is smaller at 306, 342 and 380. The smallest is a shipped certificate at 28 counts and table-only at 53. At 10 shipped counts (757, 813, 871, 931, 1058, 2760, 2866, 2974, 3084, 3196) a table-only row is smaller.

Price: the 81 beyond-horizon rows are data entry only. The exact replay of the 38 shipped is 1.064e8 pairs x 0.69 ms x 3 jobs x 2 routes = 122.3 CPU-h (the 28 smallest alone: 94.5 CPU-h; largest job n = 4035, about 5,616 s per route-job). That is over the 4 CPU-h delegation budget, so it needs the owner's word. The 53 table-only rows need reproduce.sh first (unmeasured).

The sweep's 'unretained paths' flag on bef5c42 and d6b0122 is only .gitignore; every composites/ and third_party/daniel/ path is inside the 078789a packets' scope. Also correct the Fang theorem packet README's '81 of 84 beyond 324' wording to '81 of 84 counts, all beyond 324', and '38 shipped, 43 table-only' to 28 and 53.
