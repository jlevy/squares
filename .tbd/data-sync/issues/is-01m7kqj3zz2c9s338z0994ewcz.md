---
type: is
id: is-01m7kqj3zz2c9s338z0994ewcz
title: "Owner decision 2026-11-17: the results-page lightening and the News card layout fix go to the site agent"
kind: task
status: closed
priority: 1
version: 2
labels:
  - decision
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
created_at: 2026-11-17T03:07:13.278Z
updated_at: 2026-11-17T03:07:15.925Z
closed_at: 2026-11-17T03:07:15.925Z
close_reason: Owner answered in conversation, 2026-11-17 (asked by coord-intake-1117).
resolution: null
duplicate_of: null
---
Asked who fixes results.html (2 MB hard ceiling in about three weeks) and news.html (story cards fold after first paint, failing the layout-shift check; about 36 days of room). Owner's answer: "Hand both to the site agent (Recommended)". Intake keeps raising results.html's exception in measured 100,000-byte steps up to HARD_HTML_LIMIT, per the 5 and 12 November precedent. Affects think-v1qe, think-lsam, think-3oxz.
