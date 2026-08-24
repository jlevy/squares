---
type: is
id: is-01m0tth2dgvwnagwh2975ac6k3
title: Write packing development.md and link the engineering orientation
kind: task
status: closed
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
labels:
  - engineering-maturity
  - documentation
dependencies: []
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
created_at: 2026-08-24T21:23:52.879Z
updated_at: 2026-08-24T22:55:29.319Z
closed_at: 2026-08-24T22:55:29.318Z
close_reason: Created and linked development.md with Python 3.14 setup, E0-E3 placement, commands, testing, CLI, shell, persistence, golden, compatibility, and performance policies plus governing-guideline links and footer.
resolution: null
duplicate_of: null
---
Create explorations/packing/development.md as the concise entry point for engineering work and link it from the packing README. Document Python 3.14 and uv setup, module and maturity boundaries, placement rules, fast and full validation commands, lint and type checks, CLI and Bash policy, red-green-refactor workflow, golden review, compatibility and persisted-format decisions, provenance, atomic output, and performance measurement. Link to tbd guidance instead of copying rules that can drift, and keep research status in its current owners. Acceptance: a low-context agent can select the right module and validation loop without reading implementation files first, all commands are verified, and the common-doc footer is present.
