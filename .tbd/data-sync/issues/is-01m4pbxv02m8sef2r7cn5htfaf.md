---
type: is
id: is-01m4pbxv02m8sef2r7cn5htfaf
title: Diagnose full-checkpoint timeouts in the external Mac scratch environment
kind: bug
status: in_progress
priority: 2
version: 2
delegate: codex@spud10
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-11T20:54:32.191Z
updated_at: 2026-10-11T21:23:22.279Z
started_at: 2026-10-11T21:23:22.276Z
---
During the 2026-10-11 W8 site/prose cleanup, the default full packing-validate checkpoint on the 10-CPU Mac with a fresh Python 3.14.7 environment and Cargo target under /Volumes/spud-ext1/agent-scratch/squares-site-cleanup-01a12c91 exceeded four fast behavioral shard 900-second limits, the slow behavioral suite 1800-second limit, and native n17 build/test limits. Negative controls reported failure for the exact LP invalid-row control; detailed failure output is pending checkpoint completion. No proof-engine or validation implementation was edited in this branch. Investigate the causes and reproduce under a warmed, isolated allocation without weakening correctness checks or budgets based only on this run. Full log: external task scratch full-gate.log. Site result-table width regression was separately fixed; 76 result-column checks pass.
