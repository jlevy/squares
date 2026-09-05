---
type: is
id: is-01m1qmzjyv7cazc4sk7r3rny8e
title: "Stale rung figures the audit found: T-017's ladder and runway, T-015's successor, the frontier README's n = 11 gap, the Nagamochi count"
kind: bug
status: closed
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01m1qcc9devr6mz0m6erxswxjc
created_at: 2026-09-05T02:04:55.643Z
updated_at: 2026-09-05T02:38:30.541Z
closed_at: 2026-09-05T02:38:30.541Z
close_reason: "Ported as 25502d86 (D-454): T-017's ladder (eight rungs to 99/25) and runway (0.0308 to 4B = 3.9908), T-015's and T-016's superseded-by rung (459/100), the frontier README's four smallest gaps and n = 17-19 paragraph, and the Nagamochi count split into 95 citing and 83 operative; check_rung_figures and check_nagamochi_bounds derive each from the artifacts."
resolution: null
duplicate_of: null
---
Found by the residual audit of PR 80, all D-442 class, none caught by a detector. (1) results.yaml T-017 rationale says 'seven-rung ladder ... 79/20' and next_rung says '79/20 has 0.0408 of runway left' -- the top rung is 99/25, eight rungs, runway 4 - 99/25 = 0.04 minus... re-derive: PR 80 wrote 0.0308 against the ceiling; compute it from ceiling_side and state which. (2) results.yaml T-015 superseded_by says 'T-019, which certifies 451/100 at n = 17' -- T-019 is 459/100. (3) packing/frontier/README.md's 'Next Family to Fall' table gives n = 11 a gap of 0.0882 (pre-T-018; it is 0.067084) and ranks it on that; recompute the ranking over all open cases from the front matters (the fourth-smallest claim in SYNOPSIS was re-derived on 2026-09-05 as still fourth -- confirm both agree). (4) check_nagamochi_bounds.py's docstring says 85 operative values, results.yaml 86, evidence.yaml 88, while the checker prints 83; PR 80 states 83 with a citations-versus-operative distinction (git diff HEAD 04127189 -- packing/devtools/check_nagamochi_bounds.py packing/frontier/results.yaml packing/frontier/evidence.yaml) -- port the count and the distinction, not its prose wholesale. Extend check_rung_figures or check_synopsis to read the runway and ladder-length forms so the class cannot recur there. One defect entry, recurrence_of D-442.
