---
type: is
id: is-01m1tkdxbxetk2mhj6rqeezmwr
title: "generate(): the docstring promises an exact decision the function never makes (F9a)"
kind: chore
status: closed
priority: 3
version: 3
labels:
  - review-gpt6
dependencies: []
parent_id: is-01m1tkdspk8c3n71xsc2e2t4g7
created_at: 2026-09-06T05:35:31.196Z
updated_at: 2026-09-06T06:21:09.304Z
closed_at: 2026-09-06T06:21:09.304Z
close_reason: "Implemented in 41fb401a on claude/pdf-paper-small-fixes (PR #92); reviewed by the coordinator; CI green"
resolution: null
duplicate_of: null
---
Finding 9a, confirmed: packing/src/sqpack/fractional/generate.py:500 docstring 'Search for a certificate at one setting, then decide it exactly', but generate() never calls verify (imported at line 30, re-exported at 535, unused in the body). Returning an unverified candidate is fine; the contract should say so, or the function should call verify and return the verdict. One-line fix plus a test if the behaviour changes.
