---
type: is
id: is-01m7ntt9vv7ra5j9r8j1ekm5zk
title: "Gate: list any accepted review on main whose covered T-NNN do not carry it in reviews (unmapped accepted reviews)"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
created_at: 2026-11-17T22:42:36.027Z
updated_at: 2026-11-17T22:42:36.027Z
---
Review A10 of #1011. From #1013's merge until think-i38n lands, R1's accepted review of T-310 to T-313 sits on main unmapped, and no gate sees that state; only the bead holds it. Add a sweep or records-tier line (devtools.intake_sweep or check_results) that lists every mapped-able review record on main (docs/project/reviews/review-*.md with an accepted verdict naming T-NNN or issues) whose covered entries lack it in reviews, naming the bead that owns the mapping, and fails or warns past a grace period. L57/L58 (2026-11-08) are the precedent of a review merged before its mapping.
