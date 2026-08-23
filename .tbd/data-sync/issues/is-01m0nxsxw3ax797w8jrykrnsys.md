---
type: is
id: is-01m0nxsxw3ax797w8jrykrnsys
title: Port and polish the experiment-loop agent skill
kind: task
status: closed
priority: 1
version: 3
labels: []
dependencies:
  - type: blocks
    target: is-01m0nxsy5fz6yp69kvcqy49fz0
created_at: 2026-08-22T23:44:56.707Z
updated_at: 2026-08-23T00:55:28.142Z
closed_at: 2026-08-23T00:55:28.141Z
close_reason: Skill ported to .agents/skills/experiment-loop with mirror, drift gate, and tested assets.
---
Bring the draft skill from ~/.claude/skills/experiment-loop into the repo as a portable agent skill under .agents/skills/ (mirrored to .claude/skills/). Refinements: three-role pipeline (explorer/codifier/runner), the idea board as the one-page orientation layer, unattended and parallel operation, sweeps over a declared instance axis, tested schemas and a tested checker.
