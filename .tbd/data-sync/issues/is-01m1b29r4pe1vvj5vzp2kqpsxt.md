---
type: is
id: is-01m1b29r4pe1vvj5vzp2kqpsxt
title: "Lane A3: a bespoke certified lower bound at n = 12 (H-039, with H-006's generator)"
kind: task
status: in_progress
priority: 1
version: 4
spec_path: packing/campaign/explorations/X-010-two-lanes-two-ladders.md
delegate: claude-code@vm
labels:
  - x-010
  - lane-a
dependencies: []
hold: null
hold_until: null
created_at: 2026-08-31T04:47:32.501Z
updated_at: 2026-08-31T10:11:59.319Z
started_at: 2026-08-31T10:08:44.767Z
---
s(12)'s best lower bound is a theorem about n = 11, inherited by monotonicity: any bespoke certified bound above 2 + 4/sqrt(5) ~ 3.7889 is the first result specific to n = 12, a continuum of outcomes between nothing and s(12) = 4. Shape: eleven resources unavoidable at side above 2 + 4/sqrt(5), by counterexample-guided synthesis -- A0 certifier + think-yrvm falsifier as the loop, H-006's LP duals as the candidate generator, H-039 the registered target with its fixed-threshold rule. Run the H-034-style tau* diagnostic at n = 12 side 4 - eps early: it says whether pure points can suffice or thresholds/segments are forced, and is a result about the method either way. Supersedes think-at4f's framing; see also think-iwlr. X-010 Lane A rung 3.

## Notes

2026-08-31 session-059 (BC-102 first slice): tau* pilot built (devtools/pierce_pilot.py, uncertified restricted LP + weighted escape sweep) and run. Ladder: side 3.83 moved 16.00 -> 10.78 -> 11.0000 exactly as grids refined; comparable-grid side trend 10.67 / 11.00 / 12.53 at 3.80 / 3.83 / 3.86. With the duality frame (value >= 11 above s(11)=3.8771 via the eleven-box packing), the eleven-crossing sits near ~3.83: a pure 11-point set has at most a ~0.04-wide window above 2+4/sqrt5, and any ambitious bespoke s(12) bound forces thresholds/segments/moving resources. Caveats: pose refinement RAISES the restricted value so even 3.80 is not safe; nothing is a bound either way; H-034's certified two-sided instrument is still unbuilt (that's the registered follow-up). Synthesis deliberately not attempted tonight; if attempted later: fix the threshold first (H-039) at something in (3.789, 3.83], and go in expecting the narrow window.
