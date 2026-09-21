---
type: is
id: is-01m31gnvgw9w9q3t7n0v5ws82e
title: Label PR 208 for deep-gate so the V4 control runs before merge
kind: task
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m31gn7263sfhfbq8xfabkh3p
created_at: 2026-09-21T08:17:48.567Z
updated_at: 2026-09-21T08:17:48.567Z
---
PR 208 re-review. The new test_the_gate_decides_the_case_certificate_under_the_corner_clip earns T-031's V4 and is not vacuous (mutating CornerClip.half_planes makes it fail). But gh pr checks 208 shows slow-lane and deferred-slow-lane skipping: slow-lane is gated 'if: github.event_name != pull_request' (.github/workflows/packing-validation.yml:362) and deep-gate.yml is label-gated and advisory. At ~33s the slow placement is correct under OR-13, so the fix is to label the PR before merge rather than move the test.
