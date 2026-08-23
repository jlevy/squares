---
type: is
id: is-01m0p4crw6kj13rv926fekveyr
title: Build the unattended runner and rehearse it
kind: task
status: open
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0p4cr8nk338kqtbksaf63f9
created_at: 2026-08-23T01:40:05.637Z
updated_at: 2026-08-23T01:41:11.030Z
---
The protocol is specified in the skill's unattended.md and campaign/README.md but nothing implements it. Needs: claim-by-flock id allocation, lease with expiry, budget and stop conditions, refusal list enforcement, and the session report. Then run the six-step rehearsal from unattended.md, including racing the id allocator with concurrent processes and deliberately breaking the harness to confirm the consecutive-failure stop fires and exits non-zero. A loop nobody has watched complete one round will not complete fifty.
