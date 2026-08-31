---
type: is
id: is-01m121jxr4fcbfna1rbjjrxhrg
title: Pre-commit lefthook hook points at a purged npx cache path and silently no-ops
kind: bug
status: closed
priority: 1
version: 2
labels:
  - packing
dependencies: []
created_at: 2026-08-27T16:41:54.691Z
updated_at: 2026-08-27T16:42:49.919Z
closed_at: 2026-08-27T16:42:49.917Z
close_reason: "Fixed and verified: 'make hooks-install' regenerated .git/hooks/pre-commit with a resolvable lefthook 2.1.10, and commit 08186be shows format-markdown actually executing (0.07s) instead of printing 'Can't find lefthook in PATH'. The pinning suggestion is left as a separate hardening idea, not a blocker."
resolution: null
duplicate_of: null
---
The installed .git/hooks/pre-commit resolves lefthook through a hardcoded npx cache path (/Users/levy/.npm/_npx/5e761d7efa6d0191/node_modules/lefthook-darwin-arm64/bin/lefthook) that no longer exists. lefthook is also not on PATH and the repo has no node_modules, so every commit prints 'Can't find lefthook in PATH' and the format-markdown hook never runs.

Impact: AGENTS.md states Markdown formatting is applied automatically on commit and that unformatted Markdown cannot be committed by accident. That guarantee is currently false. Four unrelated Markdown files had accumulated flowmark drift on codex/packing-ten-hour-research-agenda and were only caught by running 'make format' by hand (commit 851fcd8).

Fix: re-run 'make hooks-install' (npx lefthook install) so the hook regenerates with a resolvable path, then verify by committing a deliberately unformatted Markdown file and confirming it is reformatted and re-staged. Consider pinning lefthook the way flowmark is pinned in the Makefile, so a purged npx cache cannot silently disable the hook again.
