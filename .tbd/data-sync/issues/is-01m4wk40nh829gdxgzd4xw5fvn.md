---
type: is
id: is-01m4wk40nh829gdxgzd4xw5fvn
title: Make registration date backfill preserve dates across second-proof fields
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
created_at: 2026-10-14T06:55:41.232Z
updated_at: 2026-10-14T08:44:52.668Z
started_at: 2026-10-14T06:57:10.866Z
closed_at: 2026-10-14T08:44:52.668Z
close_reason: Fixed, independently confirmed in PR592 reviews D/E/F/G, green fast+Pages+full checkpoint38530454327 at final7a184720, and merged as f73e9de13d8ccc40b91d844b164f9c2ad9c032c1. Full mathematical proof replays remain tracked separately; no new verified n17 bound claimed.
resolution: null
duplicate_of: null
---
PR592 suite-a insert_dates duplicates registered:x because proves_kind appears betweenkind and existingregistered in T054/T055/T154. Make idempotent backfill tolerate valid fieldorder while preserving date precision and other metadata; existing full-register backfill regression mustpass.
