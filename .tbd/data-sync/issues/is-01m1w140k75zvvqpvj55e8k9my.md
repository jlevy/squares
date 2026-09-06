---
type: is
id: is-01m1w140k75zvvqpvj55e8k9my
title: Verify deferred full validation of landed research planning
kind: task
status: in_progress
priority: 1
version: 4
spec_path: packing/campaign/agendas/agenda-024-post-381-24h-portfolio.md
assignee: codex
labels: []
dependencies: []
parent_id: is-01m1tvqp2v2js8437xek2xk2gz
child_order_hints:
  - is-01m1w3nwm3vpjys7r8mxy2kf06
created_at: 2026-09-06T18:54:01.318Z
updated_at: 2026-09-06T19:38:44.216Z
---
The operator explicitly directed publication and landing without waiting on long-lasting tooling. Full packing-validate is running on committed tree d29342bb3e8c0852be46b729bca004aca8f651f5 in unified exec session 76502 (uv PID 67153, validator PID 67168), started 2026-09-06 around 18:20:24 UTC. Command from packing: DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib PYTHONUNBUFFERED=1 uv run --frozen --all-extras --group dev packing-validate --jobs 3 --inner-jobs 1. Poll nonblocking and retain the actual terminal verdict; process exit alone is not evidence of success. Required hosted CI is green on the same PR head. If the full run fails, triage exact failures and open a separate correction PR after PR97 lands. No new research execution on the planning branch. Do not change frozen scientific criteria or invent a missing result. If the retained process session is unavailable, record that explicitly and recover suitable validation evidence. Close only after a recorded verdict and disposition; a heartbeat owns follow-up.

## Notes

2026-09-06 follow-up: isolated maintenance checkout /private/tmp/squares-validation-followup.aKw8XK on codex/post-381-validation-followup, base c14451f5. The operating-rule negative control reproduced exit 1: it injects OR16, now already present; expected summary drift is masked by duplicate-ID diagnostic. Correct fixture to next OR17 and replay the operating-rule controls. The consumer test passes in the isolated small checkout (1 passed in 0.26s, call 0.22s), but inspection found sorted(REPO.rglob("*")) walks nested .venv, .git and .claude/worktrees before later exclusions. Prune excluded directories during traversal and add focused controls; do not raise the 12-second floor or declare the old 12.33s failure mere contention. Changes belong in this separate maintenance PR; no edits or push yet. Project interpreter Python3.14 with PYTHONPATH=src, not PATH python3.
