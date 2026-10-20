---
type: is
id: is-01m4w50zq05pnxp93gwngwr063
title: Fix the 'source13ee36e' corruption in three results.yaml notes
kind: bug
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-10-14T02:49:21.888Z
updated_at: 2026-10-14T02:49:21.888Z
---
packing/frontier/results.yaml on main has 'source13ee36e' at three notes (lines ~9912, ~10346, ~12456), apparently a commit hash pasted over the possessive "source's"; introduced by 3f5e7d73d (git log -S'source13ee36e'). Recover the intended wording from that commit, fix all sites, regenerate any rendering that carries it (render_results etc.), re-pin DATA_REVISION in its own commit. Found 14 Oct 2026 while porting T-101's note fix to #580.
