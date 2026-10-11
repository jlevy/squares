---
type: is
id: is-01m42sq3q6yasvex7mv2b402y3
title: Fix result-integration record drift on main
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m42sq026mszrdm4fwf5r8g8y
created_at: 2026-10-04T06:30:43.174Z
updated_at: 2026-10-04T06:30:43.174Z
---
From the 2026-10-04 review: (1) result-requests.yaml #294 still state: open, stale read_through for #294 and #296, final replies (#294 issuecomment-5974203335, #296 issuecomment-5974720283) unrecorded, #296 s78-second-route reply entry lacks id; (2) #256 entry notes describe issuecomment-5972549384, which belongs to #294 (misfiled); (3) results.yaml T-064 significance rationale still says V0/C1; (4) T-066 claim mentions s(60)/s(61) but scope is [59]; (5) check_requests keeps a reply due for s32-no-fold on closed #238; (6) T-061 omits the authors' own AI-assistance statement quoted in n-011.md; (7) resources README 626 core-hours lacks review F-6's wall-time caveat. Verify each before editing.
