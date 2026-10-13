---
type: is
id: is-01m4t090xcjhj0ctbksmgn9t7g
title: "PR #560 A1: report entry names no programs, so T-153's Verification Code reads 'no program held'"
kind: bug
status: in_progress
priority: 2
version: 2
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4t08pw394csxmekxmdydj5y
hold: null
hold_until: null
created_at: 2026-10-13T06:47:53.516Z
updated_at: 2026-10-13T06:48:09.017Z
started_at: 2026-10-13T06:48:09.017Z
---
Medium. packing/frontier/evidence.yaml:31673 verifiers: [] on E-n017-overbeck-optimality-candidate-report. Fix: list the source's registered checkers; regenerate. Review A https://github.com/jlevy/squares/pull/560#pullrequestreview-5499724625
