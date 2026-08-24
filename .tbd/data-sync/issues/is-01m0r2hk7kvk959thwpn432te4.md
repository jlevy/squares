---
type: is
id: is-01m0r2hk7kvk959thwpn432te4
title: "Gate wall time: 480s -> 152s done, the remaining 101s unexamined"
kind: task
status: open
priority: 1
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - focus-efficiency
dependencies: []
parent_id: is-01m0rkz14t04yjme92gnfncfv7
created_at: 2026-08-23T19:46:15.411Z
updated_at: 2026-08-24T01:00:51.352Z
---
A gate slow enough that people stop running it is not a gate. This one reached 480s, and 70% of that was the two checks added for basin work.

DONE (claude/packing-overnight-strategy-queue, PR #14):

Per-step timing instrumented first -- test.sh now prints where its minutes went, which is how the rest was found rather than guessed.

Golden 221s -> 0.6s. The expensive part of a golden is REGENERATING it; the assertions are cheap, because the committed file already holds the sides. verify_stored() re-derives every closed form, compares against the proved s(n), and refuses any stored basin below a proved optimum, in milliseconds. That still catches a golden edited to make a test pass, because the oracles are mathematics rather than a prior run. It does NOT catch a change in the tools that would produce a different map -- only regeneration does -- so ./test.sh --deep still regenerates, and the handover gate before an unattended night requires the deep run.

Atlas check 115s -> 11s. Its six invariants are properties of the STORE and need basin keys, not real ones. Synthetic keys now, plus one real quench so the check still exercises the real pipeline end to end.

Total 152s.

REMAINING, and honestly unexamined:

  59s  soundness perimeter
  42s  negative controls
  11s  fixed-angle cell LP
  11s  basin atlas
  10s  lint floor

The perimeter and the controls are now 101s of the 152s, and nobody has looked at either. Before optimising them, note that both are in the category the defect log says actually catches things -- the perimeter is the R1 guard and the controls are what make every other check evidence -- so the bar for making them cheaper is higher than it was for the golden, and "skip it by default" is not an acceptable answer. The likely win in the controls is that each one shells out a fresh interpreter per control; the likely win in the perimeter is that it rebuilds configurations it could cache.
