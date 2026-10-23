---
type: is
id: is-01m5kj2w9ktzkntkb07takp53s
title: "Home page atlas: show all 324 with no expander, and a viewport-aware default tile size for the Triangle (owner, 23 October)"
kind: task
status: open
priority: 1
version: 5
delegate: null
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-23T05:00:07.347Z
updated_at: 2026-10-23T06:40:18.165Z
started_at: 2026-10-23T05:00:08.212Z
---

## Notes

c-atlas-1023, branch claude/awesome-hamilton-gr597e (worktree /home/user/wt-atlas).

Done on the branch:
- Expander removed from both atlases: markup (toggle row, data-atlas-rest split,
  data-atlas-first/count, no-script override), atlas-grid.js state and handlers,
  atlas-view.js beforeArrange and hidden filter, CSS rest/hidden/toggle rules,
  --site-atlas-toggle-space renamed --site-atlas-controls-space, tests and probes that
  pinned it, design doc and the 2026-10-08 plan (supersession note).
- Size rule: automaticSize(wide, width, row) in atlas-view.js. Wide (>= 75rem) keeps
  Medium; narrow takes Small when less than half of the 35-tile row fits at Medium.
  Half the row is >= 17.5 Medium cells (> 80rem even at the phone's 4.6rem), so every
  window under 75rem takes Small: the switch stays the 75rem breakpoint.
- Measured default (share of row 18 shown): 390 Small 0.176 (319-324), 768 Small 0.264
  (316-324), 1280 Medium 0.289 (315-324), 1920 Medium 0.465 (309-324). The triangle
  opens at its right edge.

Open for the owner: "ideally half the bottom row" on a phone is not reached; it needs
tiles of about 17 px at 390 px (a fourth, fitted size). Not implemented.

Draft PR: https://github.com/jlevy/squares/pull/744 (labels S1, project). Head 721630e50
after a test fix; main 44df28b07 (#743) merged in at c1de8b9d5. Hosted run 39909088040
at edeee25fd failed only shard A on two test assertions (aria-hidden matched), fixed.

2026-10-23 coord-intake-1023: STOPPED. The owner says the atlas visuals are another agent's work and this intake session should not adjust them; the request reached this session by mistake. Draft PR https://github.com/jlevy/squares/pull/744 (branch claude/awesome-hamilton-gr597e, head 721630e50, CI green) is left as is for the owner or that agent to use or close; this session will not merge it. Released: status open, no delegate.
