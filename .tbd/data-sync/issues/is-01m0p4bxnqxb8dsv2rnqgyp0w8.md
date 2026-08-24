---
type: is
id: is-01m0p4bxnqxb8dsv2rnqgyp0w8
title: "H-010: reproduce the Stromquist falsifier triple"
kind: task
status: open
priority: 3
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0p4bxca8pjaj4v9jwww1kvg
created_at: 2026-08-23T01:39:37.782Z
updated_at: 2026-08-24T01:49:14.550Z
---
Known-answer test: the falsifier finds the stage-one escape on the 10-point set and saturates on the 12-point set. Its kill criterion is inverted - a failure is a machinery bug by definition.

## Notes

2026-08-24 primary-source reread found H-010 is not a faithful known-answer target: Stromquist does not prove a standalone 12-point set unavoidable. The ten-point avoidance localizes a box, Lemmas 4/6 force the same box to contain A1-A3, and nine further points complete a conditional counting contradiction. The instrument must reproduce the full implication/certificate.
