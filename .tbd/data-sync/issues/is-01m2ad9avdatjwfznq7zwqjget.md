---
type: is
id: is-01m2ad9avdatjwfznq7zwqjget
title: Validate and publish the reconciled PR149 head
kind: task
status: in_progress
priority: 1
version: 9
delegate: root integration lane
labels: []
dependencies:
  - type: blocks
    target: is-01m2anzgc2aqn6vzx29ps3rpn2
parent_id: is-01m26rygs7f0s76v147x0px4cd
child_order_hints:
  - is-01m2ar91msd279bq940mkybctf
created_at: 2026-09-12T08:56:00.620Z
updated_at: 2026-09-12T13:36:48.534Z
---
Run focused unit, lint, type, live-browser geometry, queue-watchdog, exact-head pre-push, hosted CI, and the full research checkpoint on the combined PR149 revision. Push without overwriting concurrent author work, update the PR title and body with exact costs and evidence limits, verify the PR remains stacked on PR148 and mergeable, then close and sync every completed bead.

## Notes

Published exact head 4d00ab68 after returning the intact verified-upper-bound corpus test to the fast lane. Focused tests, Ruff, BasedPyright, records, Chromium held-font, exact-head PDF, and unrestricted pre-push pass; the current pre-push covered 46/74 named steps, 5,057 tests, and 1,782 Ruff files in 1,049.94s with zero type findings. Every required hosted check is green and PR149 remains mergeable, non-draft, and stacked on PR148. The first full checkpoint ran 7,467.30s and failed only because the intact corpus test measured 0.97s below the one-second slow-marker floor; think-5rh4 removed only that marker and registry row. The repeated exact-head full checkpoint is still running. PR body now records hosted green separately from that pending checkpoint.
