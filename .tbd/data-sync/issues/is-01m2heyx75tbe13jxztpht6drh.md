---
type: is
id: is-01m2heyx75tbe13jxztpht6drh
title: "PR #160 review D55: the floor's liveness tests skip on every pull request"
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T02:39:57.157Z
updated_at: 2026-09-15T02:40:56.638Z
closed_at: 2026-09-15T02:40:56.637Z
close_reason: "Fixed on #160 at f7a640a2: liveness tests fail under CI without the pinned tools, the suite job installs Node and runs npm ci, and a workflow test requires Node on every job selecting fast behavioral tests (negative control removes it from suite)."
resolution: null
duplicate_of: null
---
Review finding, PR #160 stack triage (2026-09-14), lane D-tools.

The floor's liveness tests (Biome, tsc, ESLint) skipped on every PR because the `suite` job, which runs them, installed no Node.

Sources: #125 F20; #160 R19.

Files: `packing/tests/test_browser_floor_contract.py:246`, `:273`, `:293`, `:315` (@bb3f7c99); `.github/workflows/packing-validation.yml` `suite` job.
