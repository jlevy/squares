---
type: is
id: is-01m0vj2mqvh3gcsdqcn0ky52d4
title: "PR #23 review R12: Remove the negative-control step-name collision"
kind: bug
status: closed
priority: 3
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
delegate: codex@spud10
labels:
  - engineering-maturity
  - pr-review
  - pr-23
dependencies: []
parent_id: is-01m0vj13yefxcxhhew81ewfpvq
hold: null
hold_until: null
created_at: 2026-08-25T04:15:25.947Z
updated_at: 2026-08-25T04:44:38.879Z
started_at: 2026-08-25T04:16:15.517Z
closed_at: 2026-08-25T04:44:38.878Z
close_reason: "Completed in 69e65eb: the verifier step is now named 'verifier perturbation limits', eliminating the negative-control substring collision."
resolution: null
duplicate_of: null
---
PR 23 review R12. File: explorations/packing/src/sqpack/cli/validate.py step registry. Rename the verifier tolerance step so substring selection cannot also select the mutation-control suite.
