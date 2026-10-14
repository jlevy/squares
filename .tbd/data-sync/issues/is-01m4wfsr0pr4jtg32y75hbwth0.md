---
type: is
id: is-01m4wfsr0pr4jtg32y75hbwth0
title: Narrow n17 handover evidence to checks actually performed
kind: bug
status: closed
priority: 2
version: 3
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wajcx0q76t3ppdzfbjxq4d
hold: null
hold_until: null
created_at: 2026-10-14T05:57:38.965Z
updated_at: 2026-10-14T08:44:52.629Z
started_at: 2026-10-14T05:58:20.227Z
closed_at: 2026-10-14T08:44:52.629Z
close_reason: Fixed, independently confirmed in PR592 reviews D/E/F/G, green fast+Pages+full checkpoint38530454327 at final7a184720, and merged as f73e9de13d8ccc40b91d844b164f9c2ad9c032c1. Full mathematical proof replays remain tracked separately; no new verified n17 bound claimed.
resolution: null
duplicate_of: null
---
B3 independent senior review: evidence claims stored G20S/HW acceptance-report windows are checked, but program only prints fields; valid EXPECT/JG + four deliberately wrong FAILED reports still printsFAILURES0. Narrow current coverage to three region inclusion checks and mark stored reports inspected only; preserve dated historical review.
