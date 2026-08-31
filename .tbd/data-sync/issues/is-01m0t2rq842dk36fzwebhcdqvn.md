---
type: is
id: is-01m0t2rq842dk36fzwebhcdqvn
title: Guard the current hypothesis count in the synopsis
kind: bug
status: closed
priority: 2
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels: []
dependencies: []
created_at: 2026-08-24T14:28:37.755Z
updated_at: 2026-08-24T14:34:23.537Z
closed_at: 2026-08-24T14:34:23.537Z
close_reason: Corrected the live synopsis to 41 hypotheses, logged D-161, added a registry-derived consistency check plus a focused mutation control, and passed the full strict/deep gate.
resolution: null
duplicate_of: null
---
H-041 increased the live hypothesis registry to 41, but SYNOPSIS still stated 40 and no current check rejected the drift. Correct the current count, log D-161, and make tools/check_synopsis.py compare the prose count against the registry so the next addition cannot silently undercount it.
