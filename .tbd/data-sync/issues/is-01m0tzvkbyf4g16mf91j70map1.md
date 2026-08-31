---
type: is
id: is-01m0tzvkbyf4g16mf91j70map1
title: "PR 24 review R10: validate agent-session contract identity"
kind: bug
status: closed
priority: 2
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - pr24-review
dependencies: []
parent_id: is-01m0tz8s4yps8zgqwk8cng9qnx
created_at: 2026-08-24T22:57:00.797Z
updated_at: 2026-08-24T23:24:52.313Z
closed_at: 2026-08-24T23:24:52.311Z
close_reason: "Fixed in 0775c20: loader enforces softschema contract and envelope identities with independent mutations."
resolution: null
duplicate_of: null
---
PR #24 ledger.py ignores softschema.contract and softschema.envelope, so a v2 payload labeled with the wrong contract or envelope can pass. Validate metadata against the loaded schema/envelope and mutation-test both mismatches.
