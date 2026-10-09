---
type: is
id: is-01m4e36h18crs5ws6c0fm80afy
title: Review and validate the atlas site cleanups
kind: task
status: in_progress
priority: 2
version: 14
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-08T15:48:04.263Z
updated_at: 2026-10-09T01:02:00.870Z
started_at: 2026-10-08T15:49:07.449Z
---
Review source changes and exported atlas, run focused checks and the change-reachable gate, then commit/push a focused PR and confirm CI. Keep the site cleanup epic open for further requests.

## Notes

Current source is frozen after parallel implementation and strong review. The website has 82/82 mandatory Chromium checks passing (26.99 s), plus 17 focused layout/containment checks; the final PDF builder has 20 focused tests passing. The wider 7435×5270 Triangle poster wraps only logical rows 17–18, keeps every physical line at a uniform 252-unit pitch, uses the explicit problem statement without subtitle, and places October 8, 2026 beside the version below separated black project credits. n=211 is now a horizontal reflection of the immutable original and matches n=241; 26 focused orientation checks, exact verifiers and retained replay passed. Figure data, manifest and schema dimensions are now refreshed and enforced-schema checks pass. Documentation has been reconciled, including current 100-grid field counts. Existing PDF/SVG/PNG exports and release pin still refer to older d32 data and must be regenerated after the isolated data and pin commits. The data-only commit hook previously failed because the external UV-cache could not be created (ENOSPC); no hook was bypassed. External headroom has now returned to about 3 GiB and a real write probe succeeded. Current records tier passed 45/47 checks: Ruff is installed but missing from the direct runner PATH; suite_d has an expired pending measurement, now under independent evidence review. The current full-context PR body is retained in the unique external evidence directory. No final --push pass, final source/export commit, push, PR, fresh preview opening, or merge exists yet. Root handles records/exports/Git/beads; separate agents handle independent data/budget review, website/PR context and actual-PDF verification. Next: reviewed isolated data/pin commits; serial exports and actual visual checks; fresh lawful default-browser/PDF openings; current records and full change-reachable push gate; clean PR and exact-head CI.
