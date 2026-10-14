# A243 -- the simple-square climb at n = 17 and n = 19 (corners pinned; FC run forward as a slot-set tree)

Generated 2026-10-07 20:59 by code/report243.py from results/verdicts243_n*.jsonl (the descend243 / chain243 runs are resumable and may still be running: `pending` rows are not yet run).  Method and soundness: notes/climb243.md.

## n = 17

Window [116511/25000, 4675531/1000000]: s_lo = 116511/25000 (T-043; T-093 raises it to 18641771/4000000), s_hi = 4675531/10^6 >= T-065's 4.67553009360455....

Census (A53's Young slot-set classes, D4-reduced, window-stable) and the descent's verdicts per k (spine trees, pad window, no LP; `root dead` = closed at stage 0 or at the tree's root node):

| k | classes | corners4 | DEAD | REDUCES | ALIVE | pending | root dead | stage-0 dead | CPU-s |
|---|---|---|---|---|---|---|---|---|---|
| 16 | 73 | 17 | 17 | 0 | 0 | 56 | 17 | 8 | 3 |
| 15 | 148 | 35 | 35 | 0 | 0 | 113 | 35 | 10 | 556 |
| 14 | 256 | 68 | 31 | 0 | 0 | 225 | 4 | 1 | 826 |
| 13 | 325 | 91 | 0 | 0 | 0 | 325 | 0 | 0 | 0 |
| 12 | 374 | 112 | 0 | 0 | 0 | 374 | 0 | 0 | 0 |
| 11 | 356 | 103 | 0 | 0 | 0 | 356 | 0 | 0 | 0 |
| 10 | 319 | 89 | 0 | 0 | 0 | 319 | 0 | 0 | 0 |
| 9 | 242 | 57 | 0 | 0 | 0 | 242 | 0 | 0 | 0 |
| 8 | 177 | 37 | 0 | 0 | 0 | 177 | 0 | 0 | 0 |
| 7 | 107 | 14 | 0 | 0 | 0 | 107 | 0 | 0 | 0 |
| 6 | 64 | 7 | 0 | 0 | 0 | 64 | 0 | 0 | 0 |
| 5 | 31 | 1 | 0 | 0 | 0 | 31 | 0 | 0 | 0 |
| 4 | 17 | 1 | 0 | 0 | 0 | 17 | 0 | 0 | 0 |
| 3 | 6 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 0 |
| 2 | 3 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 |
| 1 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |

Decided 83 classes in 0.38 CPU-h.  Kills by rule (tree leaves; STAGE0 = classes closed by the closed-form stage 0 + CSP): {"COUNT": 5, "EmptyBox": 55, "FC": 52, "NOROOM": 63, "S-CLIP": 3, "STAGE0": 19}.

**Record class** n17_k08_0156: PENDING.  **Soundness canary** (no class contained in the record's may be DEAD -- the record realises it inside the window): OK.

**The climb** from the four-corner root n17_k04_0016 (task 2; nodes = classes on root-to-leaf paths, depth capped at the record's k): 1 path nodes over 1 classes, depth 0, leaves {'DEAD': 0, 'ALIVE': 0, 'PENDING': 1, 'REDUCES': 0, 'ERROR': 0}, reaches the record class: False.

**Rigidity of the record [M]** (rigid243.py, first-order, side fixed): 39 contacts, rank 37 of 51, rattlers none; first-order motion LP max |v|_1 = 0.0 over squares [] -> infinitesimally RIGID.

## n = 19

Window [193/40, 4885619/1000000]: s_lo = 193/40 (T-103, superseding T-020's 24/5), s_hi = 4885619/10^6 >= the best known 3 + 4 sqrt2/3 = 4.88561808....

Census (A53's Young slot-set classes, D4-reduced, window-stable) and the descent's verdicts per k (spine trees, pad window, no LP; `root dead` = closed at stage 0 or at the tree's root node):

| k | classes | corners4 | DEAD | REDUCES | ALIVE | pending | root dead | stage-0 dead | CPU-s |
|---|---|---|---|---|---|---|---|---|---|
| 16 | 73 | 17 | 0 | 0 | 0 | 73 | 0 | 0 | 0 |
| 15 | 148 | 35 | 0 | 0 | 0 | 148 | 0 | 0 | 0 |
| 14 | 256 | 68 | 0 | 0 | 0 | 256 | 0 | 0 | 0 |
| 13 | 325 | 91 | 0 | 0 | 0 | 325 | 0 | 0 | 0 |
| 12 | 374 | 112 | 0 | 0 | 0 | 374 | 0 | 0 | 0 |
| 11 | 356 | 103 | 0 | 0 | 0 | 356 | 0 | 0 | 0 |
| 10 | 319 | 89 | 0 | 0 | 0 | 319 | 0 | 0 | 0 |
| 9 | 242 | 57 | 0 | 0 | 0 | 242 | 0 | 0 | 0 |
| 8 | 177 | 37 | 0 | 0 | 0 | 177 | 0 | 0 | 0 |
| 7 | 107 | 14 | 0 | 0 | 0 | 107 | 0 | 0 | 0 |
| 6 | 64 | 7 | 0 | 0 | 0 | 64 | 0 | 0 | 0 |
| 5 | 31 | 1 | 0 | 0 | 0 | 31 | 0 | 0 | 0 |
| 4 | 17 | 1 | 0 | 0 | 0 | 17 | 0 | 0 | 0 |
| 3 | 6 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 0 |
| 2 | 3 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 |
| 1 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |

Decided 0 classes in 0.00 CPU-h.  Kills by rule (tree leaves; STAGE0 = classes closed by the closed-form stage 0 + CSP): {}.

**Record class** n19_k11_0236: PENDING.  **Soundness canary** (no class contained in the record's may be DEAD -- the record realises it inside the window): OK.

**The climb** from the four-corner root n19_k04_0016 (task 2; nodes = classes on root-to-leaf paths, depth capped at the record's k): 1 path nodes over 1 classes, depth 0, leaves {'DEAD': 0, 'ALIVE': 0, 'PENDING': 1, 'REDUCES': 0, 'ERROR': 0}, reaches the record class: False.

**Rigidity of the record [M]** (rigid243.py, first-order, side fixed): 45 contacts, rank 40 of 57, rattlers none; first-order motion LP max |v|_1 = 0.0 over squares [] -> infinitesimally RIGID.

