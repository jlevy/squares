---
type: is
id: is-01m4xe5txp3t3t4xczs1swedc9
title: Judge the census control's axis refusal against the sweep's enclosure, not AXIS_ROUNDING (F-1 of the 14 October wand125 review; T-142, T-175 to T-177)
kind: task
status: open
priority: 2
version: 2
labels:
  - result-import
dependencies: []
parent_id: is-01m4wsqt2sjrksybyz375sarb3
created_at: 2026-10-14T14:48:32.438Z
updated_at: 2026-10-14T14:48:59.569Z
---
Finding F-1 of the 14 October review (docs/project/reviews/review-2026-10-14-wand125-fine-net-and-linear-lower-bounds.md), major for the records lane and not a defect of any certificate.

`packing/devtools/sqverify_fast_census.py` holds the axis vertex sweep's refusal to a constant, `AXIS_ROUNDING = 1/10^9` (the axis branch of `refusal_record`). The gap the rule measures is half the sweep's enclosure width, which varies by a factor of twenty across the s(37), s(39) and s(44) certificates and exceeds the constant at n = 39, so the n = 39 whole-net control cannot end `CONTROLS_REFUSED` under this rule although its refusal is sound. It bears on T-142 as well.

Fix: one of the review's section 5 options 1 to 3, as a change to control logic read by a reviewer. Not a small importer change, so the records lane of the 14 October intake did not make it: T-175 to T-177 are registered at V0/C1 and their C3 waits on the control. Done when the axis refusal is judged against the sweep's own enclosure, a reviewer has read the change, and the n = 39 control can end CONTROLS_REFUSED.
