---
type: is
id: is-01m2p1yw0f08dvqdapngmdn25w
title: Close fail-closed CI budget review gaps
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m2m5zjmj7dsycs1x6yxwcwwt
created_at: 2026-09-16T21:28:56.590Z
updated_at: 2026-09-17T16:07:45.459Z
closed_at: 2026-09-17T16:07:45.457Z
close_reason: "Landed with PR #188 (merge 042e791c, 2026-09-17T15:54Z): hosted aggregates and the Deferred checkpoint passed on 7f387990; review dispositions in https://github.com/jlevy/squares/pull/188#issuecomment-5714064819. The first main push deployed GitHub Pages at 042e791c with verify-deployment passing."
resolution: null
duplicate_of: null
---
Address the final review findings before PR 188 certification: reject fractional tier resource counts; reject duplicate YAML keys in tier and PR-wall budget authorities; fail whole-tier validation when its budget register is unavailable or missing the tier; reject mixed-attempt/negative PR-wall timestamps; and let read_tier_walls ingest completed jobs whose validation steps passed but whose budget verdict alone failed. Add focused negative tests and preserve scoped-run behavior.
