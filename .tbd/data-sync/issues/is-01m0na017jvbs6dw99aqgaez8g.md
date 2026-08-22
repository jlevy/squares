---
type: is
id: is-01m0na017jvbs6dw99aqgaez8g
title: Choose and implement the hook mechanism
kind: task
status: closed
priority: 1
version: 2
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0na001wtn9wb0fkwndgwwrq
created_at: 2026-08-22T17:58:45.233Z
updated_at: 2026-08-22T18:02:48.424Z
closed_at: 2026-08-22T18:02:48.424Z
close_reason: Implemented lefthook (not a bare .git/hooks script, which is not version-controlled and would not survive a fresh clone). Makefile pins flowmark-rs==0.3.2; package.json pins lefthook 2.1.10.
---
Decide between a git pre-commit hook, lefthook, or the pre-commit framework. Note that .git/hooks is NOT version controlled, so a bare git hook is not shareable and would not survive a fresh clone -- weigh that.
