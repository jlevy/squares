---
type: is
id: is-01m5gg2v4ers872jhw0rz9cwpf
title: Balance main action button labels against their visible capital-letter ink
kind: bug
status: closed
priority: 2
version: 5
delegate: upstream_integration
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-22T00:27:25.698Z
updated_at: 2026-10-22T09:19:51.013Z
started_at: 2026-10-22T00:28:08.071Z
closed_at: 2026-10-22T09:19:51.013Z
close_reason: "Implemented and validated in PR #578, merged as d660905ec81383d7ca89830ff23a68e1832426e5 at 2026-10-22T09:14:53Z. Accepted candidate a020a6a11: final delta 9/9, full pool 23 pass, ordinary CI 31 successes, full checkpoint 39751078588 all ten workers and aggregate passed, Reviews N/O accepted, fresh site and four PDFs built with 7333 publication checks. Historical population, coverage and Results-growth follow-ups remain open; deployment is separate."
resolution: null
duplicate_of: null
---
The main shared site-action links and buttons have equal physical padding, but their uppercase Source Sans labels appear high inside the filled rectangle. Measure line-box and cap-ink geometry using retained browser tests, repair the shared typography rule without guessed pixel offsets, retain icon alignment and hit areas, and refresh the immutable CSS preview. No unrelated source edits or push.

## Notes

Measured the actual loaded Source Sans uppercase ink using a retained browser probe with a baseline marker inside the text flex item. Main labels were 0.2575px above the button center despite equal 7.2px padding. Shared 0.016em inset redistribution centers the label without changing total padding or click height; the shared arrow margin compensation preserves geometric icon centers and existing rotations.

Regression: zero-offset negative control fails the 0.1px center bound; corrected link/native-button/popover cases pass at 1280px and 390px (2 passed in 3.10s). Ruff, Ruff format, Biome, BasedPyright and git diff --check pass. Parent is running the selected push gate; no duplicate broad suite started.

Preview published through SiteAssets, creating immutable site.328fa91c97049e5c.css and atomically updating 656 HTML references in site-final-e3e33171b. Standard publication checker passes 7300/7300. Six live routes return HTTP200 and match output bytes; all61 referenced shared assets are served whole. Live URL: http://127.0.0.1:8790/?button=think-5nvy . Evidence logs remain in external task scratch: button-padding-red.log, button-padding-green.log and button-padding-published-site-check.log. Source frozen for coordinator commit/CI and CUA visual recheck.
