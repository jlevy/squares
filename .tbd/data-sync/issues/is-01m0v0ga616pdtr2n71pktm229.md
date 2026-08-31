---
type: is
id: is-01m0v0ga616pdtr2n71pktm229
title: "PR 24 transition T2: validate the corrected integrated tree"
kind: task
status: closed
priority: 1
version: 4
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - pr24-transition
dependencies: []
parent_id: is-01m0tz8s4yps8zgqwk8cng9qnx
child_order_hints:
  - is-01m0v0s3c8y81w7sfrbvhehz8c
created_at: 2026-08-24T23:08:19.519Z
updated_at: 2026-08-24T23:24:53.765Z
closed_at: 2026-08-24T23:24:53.764Z
close_reason: Exact integrated tree passed focused schema/docs/generated-view checks, Ruff, BasedPyright, format-check, 55/55 controls, and the 30-step normal gate in 36.277 seconds. Deep golden intentionally not run before think-nr5w.
resolution: null
duplicate_of: null
---
Run focused AgentSession/schema/readme/synopsis/negative-control checks, Flowmark and format checks, then the full normal gate on the exact merge tree. Retain command, exit status, elapsed time, and final counts; do not rerun the known-red deep golden before think-nr5w's millisecond fixture.
