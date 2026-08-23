---
type: is
id: is-01m0p4crw6kj13rv926fekveyr
title: Build the unattended runner and rehearse it
kind: task
status: closed
priority: 1
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0p4cr8nk338kqtbksaf63f9
created_at: 2026-08-23T01:40:05.637Z
updated_at: 2026-08-23T08:10:05.597Z
closed_at: 2026-08-23T08:10:05.596Z
close_reason: "Built on claude/thinking-scratchpad-research-p1wkfg (PR #13) as campaign/runner.py: status/preflight/claim/execute/record/release/run, state on disk between steps, the accepting verdict structurally unreachable, and a generated session report. Driven end to end for exp-011 (H-020 at n=17)."
resolution: null
duplicate_of: null
---
The protocol is specified in the skill's unattended.md and campaign/README.md but nothing implements it. Needs: claim-by-flock id allocation, lease with expiry, budget and stop conditions, refusal list enforcement, and the session report. Then run the six-step rehearsal from unattended.md, including racing the id allocator with concurrent processes and deliberately breaking the harness to confirm the consecutive-failure stop fires and exits non-zero. A loop nobody has watched complete one round will not complete fifty.
