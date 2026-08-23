---
type: is
id: is-01m0nym1ss6x3jvmj2brvaw7v5
title: Retain the separating axis and sign in the Python oracle's separated()
kind: task
status: open
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0p5tswc9s27gb5c1d3da27b
created_at: 2026-08-22T23:59:12.696Z
updated_at: 2026-08-23T05:26:46.703Z
---
separated() already computes exactly this and discards it, returning 1/0/None without saying which axis. Nearly free to keep, and it makes both implementations emit the same certificate shape so the differential test can compare certificates rather than booleans.
