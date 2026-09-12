---
type: is
id: is-01m2ad9avdatjwfznq7zwqjget
title: Validate and publish the reconciled PR149 head
kind: task
status: in_progress
priority: 1
version: 14
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: root integration lane
labels: []
dependencies:
  - type: blocks
    target: is-01m2anzgc2aqn6vzx29ps3rpn2
  - type: blocks
    target: is-01m26rygs7f0s76v147x0px4cd
parent_id: is-01m26rygs7f0s76v147x0px4cd
child_order_hints:
  - is-01m2ar91msd279bq940mkybctf
created_at: 2026-09-12T08:56:00.620Z
updated_at: 2026-09-12T14:31:55.152Z
---
Run focused unit, lint, type, live-browser geometry, queue-watchdog, exact-head pre-push, hosted CI, and the full research checkpoint on the combined PR149 revision. Push without overwriting concurrent author work, update the PR title and body with exact costs and evidence limits, verify the PR remains stacked on PR148 and mergeable, then close and sync every completed bead.

## Notes

Published exact head 4d00ab68 after returning the intact verified-upper-bound corpus test to the fast lane. Focused tests, Ruff, BasedPyright, records, Chromium held-font, exact-head PDF, unrestricted pre-push, and every required hosted check pass. The first full checkpoint ran 7,467.30s and failed only because the intact corpus test measured 0.97s below the one-second slow-marker floor. One repeated invocation was interrupted after 2,722s when its child environment was found to omit the project uv path. A second replacement was interrupted after 1,146s when the parallel BC gate demonstrated that the sandbox denies required process-tree and loopback controls. Both have no verdict and are cost evidence only. The unrestricted replacement exact-head full checkpoint is running as session 83725 with a retained transcript and complete project environment.
