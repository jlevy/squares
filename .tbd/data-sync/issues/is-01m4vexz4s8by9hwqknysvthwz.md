---
type: is
id: is-01m4vexz4s8by9hwqknysvthwz
title: "PR #588 B4: archive member count described as checked, but internal to manifest.json; root files size not compared"
kind: bug
status: closed
priority: 2
version: 3
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4vex5amc35y6f4zqamve8q6
hold: null
hold_until: null
created_at: 2026-10-13T20:23:14.329Z
updated_at: 2026-10-13T20:51:08.893Z
started_at: 2026-10-13T20:23:28.649Z
closed_at: 2026-10-13T20:51:08.893Z
close_reason: "fixed in 75a0a94 and 9ab8f8d: root files held to size; prose says member counts are manifest.json's own; receipt byte-identical"
resolution: null
duplicate_of: null
---
Severity Low. PR #588 review https://github.com/jlevy/squares/pull/588#pullrequestreview-5509418328, finding B4. Where: packing/frontier/evidence.yaml:32005, packing/frontier/verifiers.yaml:1579, packet README:199, receipts/programs/check_source_manifest.py:72-94.
