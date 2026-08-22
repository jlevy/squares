---
type: is
id: is-01m0na00qnreyntbeeszw35wqe
title: Check repo conventions for hooks and third-party checkouts
kind: task
status: closed
priority: 1
version: 2
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0na001wtn9wb0fkwndgwwrq
created_at: 2026-08-22T17:58:44.725Z
updated_at: 2026-08-22T18:02:48.091Z
closed_at: 2026-08-22T18:02:48.091Z
close_reason: "Checked jlevy/softschema (already cloned) for the first-party convention: lefthook.yml delegating to 'make format', tooling-only root package.json pinning lefthook, and a .flowmarkignore. Adopted all three."
---
This repo already has .claude/settings.json hooks and a tbd closing-reminder PostToolUse hook. jlevy's other repos use lefthook. Check the tbd shortcut checkout-third-party-repo for the attic convention before cloning anything.
