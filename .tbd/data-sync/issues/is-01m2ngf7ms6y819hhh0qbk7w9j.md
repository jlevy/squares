---
type: is
id: is-01m2ngf7ms6y819hhh0qbk7w9j
title: Remove the remaining explainer TypeScript inference relaxations
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-16T16:23:18.424Z
updated_at: 2026-09-16T16:23:18.424Z
---
PR #181 moved the explainer's inline programs into checked files, but tsconfig.explainer.json still relaxes noImplicitAny, strictNullChecks, noUncheckedIndexedAccess, and exactOptionalPropertyTypes. The prior tracker think-7f3p was closed when extraction landed, leaving the browser-floor contract pointing at a dead tracker. Acceptance: add the missing DOM/JSDoc types, remove all four relaxations, and keep the explainer typecheck and browser probes green.
