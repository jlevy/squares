---
type: is
id: is-01m3bx1enypyg5wawh2sqdq3x3
title: "BC-386: native C4 decision of Guzhou R052 (lift native coverage ceilings, re-baseline audit, full run)"
kind: task
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/archive/plan-2026-09-25-after-r052-planning.md
labels: []
dependencies: []
parent_id: is-01m3bsc3bsdbq1jk7xnx6p0hev
created_at: 2026-09-25T09:06:15.869Z
updated_at: 2026-10-12T23:51:26.137Z
closed_at: 2026-10-12T23:39:10.166Z
close_reason: "Superseded: agenda-042 BC-386 records R052 replaced by Kleddamag v1.1.0 on 2026-09-27; the native decision carries over to BC-393 (think-0rbj)."
resolution: canceled
duplicate_of: null
---
Lift interval.py/threshold_interval.py memory ceilings behind an explicit byte budget recorded in receipts; contract test admitting R052 dimensions; re-baseline the n11 native audit; run devtools.verify_guzhou_r052_native on all 15,721 rows on a clean reviewed commit (~15 CPU-h, 2 workers). Fable xhigh checks the transfer contract. Refusal is recorded, never a negative.
