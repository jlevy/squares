---
type: is
id: is-01m3xfttskspb2zbw0tzfm5rvw
title: apply_wand125_rectangles replaces an existing case-record intake paragraph that shares its date
kind: bug
status: closed
priority: 1
version: 2
labels:
  - packing
  - result-import
dependencies: []
created_at: 2026-10-02T05:01:47.187Z
updated_at: 2026-10-02T05:40:30.950Z
closed_at: 2026-10-02T05:40:30.949Z
close_reason: "Fixed in the controls commit on claude/zealous-gauss-jem7l9 (PR jlevy/squares#298): paragraph ownership by exact opening, regression tests"
resolution: null
duplicate_of: null
---
Found 2026-10-02 by lane I1 (PR jlevy/squares#298): writing the 2026-10-01 intake paragraph deleted the Evan Daniel and wand125 exact-cover paragraphs of the same date at n = 59, 60, 61, 77 and 78, and wrote figures check_case_prose and check_math_markup reject at 59, 60, 77, 78. Fixed by hand in commit after 928c30a1f; the tool is not fixed, so the next apply (T-068 replays) will recur it. Fix: key the paragraph it owns by source, not by date, and add a test with a foreign same-date paragraph.
