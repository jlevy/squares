---
type: is
id: is-01m32nbcfd76tn4ket9p6xad3n
title: Agents sharing the scratchpad overwrote each other's PR body and it reached a live PR
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m32dvmtc77znp14556p7c5w2
created_at: 2026-09-21T18:58:42.796Z
updated_at: 2026-09-21T18:58:42.796Z
---
2026-09-21: two agents in one session both wrote .../scratchpad/BODY.md. One agent's gh pr edit 212 pushed the other's unrelated body (a transcription/PDF PR description) to PR 212 before it was caught and rewritten in full.

No lasting damage -- the body was restored and passes check_pr_description -- but an unrelated description was live on a pull request for several minutes, and nothing detected it; the agent noticed by accident.

Convention to adopt: agent-scoped subdirectories in the shared scratchpad, never bare filenames at its root. Worth stating wherever sub-agent briefs are templated, since the collision is silent and the failure mode is publishing the wrong thing under your own name.
