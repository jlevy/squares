---
type: is
id: is-01m2pz4thm3y5k7p6hj8yg70kx
title: Omit the Open section when nothing is open
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-17T05:59:00.388Z
updated_at: 2026-09-17T05:59:00.388Z
---
Owner request 2026-09-17: in the facts panel, when Open would show only 'none', omit the Open heading and its items entirely. This reverses the earlier choice in packages/workbench/src/view/facts.ts to always head Open so the pair of headings is the panel's shape. Done when the section is absent for every n with no open items, present and unchanged otherwise, and a test pins both.
