---
type: is
id: is-01m20zzqjwygewaj8wkyt57shq
title: sqsearch arms behind flags, and the two sweep instruments
kind: feature
status: closed
priority: 1
version: 5
labels: []
dependencies: []
parent_id: is-01m20zyy839t6mbvpqy8ay2hsn
created_at: 2026-09-08T17:10:24.588Z
updated_at: 2026-10-06T08:47:05.764Z
closed_at: 2026-10-06T08:47:05.764Z
close_reason: "Done, as its description says: sqsearch's --p-perturb/--perturb-scale, --mu0/--mu1 and --budget-pair-tests flags are in packing/sqsearch/src/main.rs on origin/main, with packing/devtools/run_arm_sweep.py and run_basin_hopping.py; it has no open children and its review defects are tracked under think-6c2j (closed)."
resolution: null
duplicate_of: null
---
Done in this session, recorded so the follow-ups have a parent.

sqsearch gained three flags, all off by default so the control stays reachable and bit-identical:
- --p-perturb / --perturb-scale: Gensane layer 3, a proposal that displaces every square at once (H-135).
- --mu0 / --mu1: an aggregate inward wall-pressure term, geom::spread, ramped like lambda (H-136).
- --budget-pair-tests: a per-chain cap in the campaign's declared budget currency, so arms whose per-move cost differs are comparable.

The selftest pins the control chain to the literal the pre-arm engine printed, exercises both arms for validity, and checks the pair-test cap binds. unsafe_code = "forbid" and the pedantic clippy floor are unchanged; cargo test is green.

Instruments: packing/devtools/run_arm_sweep.py and packing/devtools/run_basin_hopping.py.

## Notes

2026-09-14 (PR #125 review, lane A): three review defects land on this feature's code and are tracked as children of think-6c2j rather than here, so this record stays open as the arms' parent. D03 (think-0suz, fixed in 37309cae): the selftest's control comparison could not fail; it now compares against a frozen pre-arm loop, so the description's "pins the control chain to the literal" is superseded. D23 (think-yeyi): run_arm_sweep did not enforce verification. D75 (think-a0x7): arm flags unvalidated; engine half fixed in d484ab55.
