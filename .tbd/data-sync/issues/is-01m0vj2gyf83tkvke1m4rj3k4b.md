---
type: is
id: is-01m0vj2gyf83tkvke1m4rj3k4b
title: "PR #23 review R2: Make the repo-bound command dependency boundary honest"
kind: bug
status: closed
priority: 1
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
created_at: 2026-08-25T04:15:22.062Z
updated_at: 2026-08-25T04:44:35.235Z
started_at: 2026-08-25T04:16:15.445Z
closed_at: 2026-08-25T04:44:35.234Z
close_reason: "Completed in 69e65eb: repository applications now validate an explicit project root, fail clearly outside a checkout, document their non-library boundary, and expose case/devtool subprocess edges to architecture tests."
resolution: null
duplicate_of: null
---
PR 23 review R2. Files: explorations/packing/src/sqpack/cli/validate.py, campaign/runner.py, campaign/ledger.py, and tests/test_module_boundaries.py. Resolve hidden repository dependencies expressed through file ancestry and module-name strings; align architecture enforcement, packaging behavior, and development.md.
