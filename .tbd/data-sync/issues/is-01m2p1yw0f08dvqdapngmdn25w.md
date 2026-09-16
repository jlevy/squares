---
type: is
id: is-01m2p1yw0f08dvqdapngmdn25w
title: Close fail-closed CI budget review gaps
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m2m5zjmj7dsycs1x6yxwcwwt
created_at: 2026-09-16T21:28:56.590Z
updated_at: 2026-09-16T21:28:56.590Z
---
Address the final review findings before PR 188 certification: reject fractional tier resource counts; reject duplicate YAML keys in tier and PR-wall budget authorities; fail whole-tier validation when its budget register is unavailable or missing the tier; reject mixed-attempt/negative PR-wall timestamps; and let read_tier_walls ingest completed jobs whose validation steps passed but whose budget verdict alone failed. Add focused negative tests and preserve scoped-run behavior.
