---
type: is
id: is-01m2pk4k24sz9126rtj5khg93n
title: check_generated_markdown fails the gate on gitignored attic scratch files
kind: bug
status: open
priority: 3
version: 1
labels:
  - tooling
  - validation
dependencies: []
created_at: 2026-09-17T02:29:09.823Z
updated_at: 2026-09-17T02:29:09.823Z
---
On 2026-09-17 packing-validate --records failed its 'defect log' step on PR #188's worktree only because devtools.check_generated_markdown found a generated-header preview at attic/session-record/ledger.preview.md (a gitignored E0 scratch file written by an agent) and demanded it be added to .flowmarkignore. The step printed nothing in the gate summary beyond the step name; the reason appeared only when the checker was run directly. Scratch under attic/ is not repository content. Make the checker walk tracked files (or skip gitignored paths), and surface the checker's message in the step output.
