---
type: is
id: is-01m3bx1enypyg5wawh2sqdq3x3
title: "BC-386: native C4 decision of Guzhou R052 (lift native coverage ceilings, re-baseline audit, full run)"
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-25-after-r052-planning.md
labels: []
dependencies: []
parent_id: is-01m3bsc3bsdbq1jk7xnx6p0hev
created_at: 2026-09-25T09:06:15.869Z
updated_at: 2026-09-25T09:06:15.869Z
---
Lift interval.py/threshold_interval.py memory ceilings behind an explicit byte budget recorded in receipts; contract test admitting R052 dimensions; re-baseline the n11 native audit; run devtools.verify_guzhou_r052_native on all 15,721 rows on a clean reviewed commit (~15 CPU-h, 2 workers). Fable xhigh checks the transfer contract. Refusal is recorded, never a negative.
