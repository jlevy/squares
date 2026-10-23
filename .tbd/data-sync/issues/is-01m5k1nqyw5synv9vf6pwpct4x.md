---
type: is
id: is-01m5k1nqyw5synv9vf6pwpct4x
title: "Owner decision: #734 (wand125) proposal to submit and fetch upper bounds by API — automation level 1/2/3, Level 3 substitutions and auto-merge, api/v1 on squaremath.org"
kind: task
status: open
priority: 2
version: 1
labels:
  - owner-decision
dependencies: []
created_at: 2026-10-23T00:13:19.575Z
updated_at: 2026-10-23T00:13:19.575Z
---
jlevy/squares#734 (wand125, 2026-10-22T20:40Z), a proposal for discussion, not a result. Proposes: submit a Witness/v2 by issue/API; a workflow runs packing-witness verify and compares with the house by exact arithmetic and comments (Level 1); a same-day bot PR records smaller packings as reported (Level 2, bot merges reported-only PRs on green checks); a PR adopting and regularizing the new house with one maintainer approval (Level 3); static JSON of current bests and witnesses at squaremath.org/api/v1/. Three owner questions: (1) how far to automate; (2) accept Level 3's substitutions (form credit fields, issue number instead of import bead, one approval for review) and whether the bot merges after approval; (3) is api/v1 on squaremath.org right, and lower bounds from the start? Coordinator posts no reply until the owner decides. Record in result-requests.yaml (triage: pending, kind proposal, not intake) in the next intake bookkeeping PR.
