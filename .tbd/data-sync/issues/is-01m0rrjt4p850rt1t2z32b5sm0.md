---
type: is
id: is-01m0rrjt4p850rt1t2z32b5sm0
title: "No CI: every check has only ever run on one developer's machine"
kind: task
status: open
priority: 2
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
labels:
  - engineering-maturity
dependencies: []
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
created_at: 2026-08-24T02:11:23.925Z
updated_at: 2026-08-24T21:22:11.732Z
---
There is no .github/workflows. The Makefile has format, format-check, hooks-install, skills-sync, skills-check and a 'check' target that runs skills-check alone. lefthook runs only the Markdown formatter on pre-commit. explorations/packing/test.sh is the entire gate and nothing runs it automatically.

Everything the defect log worries about -- a check that is silently unreachable (D-004), a generated view left stale (D-027, D-028) -- is a thing CI catches for free and a thing a local-only gate catches only when someone remembers.

Now that the gate is ~22s this is cheap to wire up. Two jobs worth having: the full gate on every PR, and a second one on a DIFFERENT architecture, which is what would surface the golden's cross-machine fragility (think-lwao) before an unattended cloud run does.
