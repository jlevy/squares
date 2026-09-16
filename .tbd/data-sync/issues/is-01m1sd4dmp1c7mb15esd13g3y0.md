---
type: is
id: is-01m1sd4dmp1c7mb15esd13g3y0
title: "BC-216: a declared CI-cost ceiling the gate enforces, so a tier regression cannot go unnoticed"
kind: task
status: closed
priority: 0
version: 3
labels: []
dependencies: []
created_at: 2026-09-05T18:26:14.294Z
updated_at: 2026-09-16T00:20:18.486Z
closed_at: 2026-09-16T00:20:18.485Z
close_reason: |
  Landed. The declared CI-cost ceiling shipped on 2026-09-06 as packing/devtools/gate-budgets.yaml, enforced by packing/devtools/check_gate_budgets.py and the gate's gate_budgets judge. think-z121 extended it on 2026-09-15 with the unrecorded-tier rule, the attribution ratchet, and a 180 s budget on the pull-request wall itself.
resolution: null
duplicate_of: null
---

## Notes

2026-09-15 (think-z121): closing as landed. BC-216's declared CI-cost ceiling shipped on 2026-09-06 as `packing/devtools/gate-budgets.yaml`, with `packing/devtools/check_gate_budgets.py` and the gate's own `gate_budgets` judge enforcing a ceiling, a drift ratio and a stale ratio per tier. It stopped the first spiral and not the second, so think-z121 extended it on 2026-09-15 with the three rules it lacked: a tier a pull-request job runs may not have an empty record (rule 5 -- three of five pull-request tiers had one, and `checks` failed its ceiling at least nine times in eight days with every step green); a record may not rise past 1.2x of the lowest record since its last attributed one without an `attribution:` naming the per-step or per-file costs that grew (rule 6 -- `suite` had been re-based 102.83 -> 162.62 -> 118.72 -> 183.44 s with the ceiling following it); and the pull request's own wall is budgeted at 180 s with a 1.2x regression rule by `packing/devtools/check_pr_wall.py` (rule 7).
