---
type: is
id: is-01m15b69acbnaetfj9f895en85
title: Run the full gate and open the PR
kind: task
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m15219m6eh8fww5pm9sc2sqd
created_at: 2026-08-28T23:27:29.611Z
updated_at: 2026-08-28T23:27:56.447Z
closed_at: 2026-08-28T23:27:56.446Z
close_reason: "Duplicate: this epic already had a child bead tree; superseded by think-5q7n/anzp/lcjk/41b6/5xsh/pnle/dw3i/oq00"
resolution: null
duplicate_of: null
---
packing-validate --fast during the loop, the complete gate before merge. The full gate is what catches the generated-view and negative-control regressions; --fast does not run them.

Verify zero broken relative links across the repository as a separate check.
