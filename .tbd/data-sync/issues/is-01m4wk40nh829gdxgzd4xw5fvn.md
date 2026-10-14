---
type: is
id: is-01m4wk40nh829gdxgzd4xw5fvn
title: Make registration date backfill preserve dates across second-proof fields
kind: bug
status: in_progress
priority: 2
version: 2
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wajcx0q76t3ppdzfbjxq4d
hold: null
hold_until: null
created_at: 2026-10-14T06:55:41.232Z
updated_at: 2026-10-14T06:57:10.867Z
started_at: 2026-10-14T06:57:10.866Z
---
PR592 suite-a insert_dates duplicates registered:x because proves_kind appears betweenkind and existingregistered in T054/T055/T154. Make idempotent backfill tolerate valid fieldorder while preserving date precision and other metadata; existing full-register backfill regression mustpass.
