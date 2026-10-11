---
type: is
id: is-01m31gpgmxd034echmxq2peq0s
title: Gate the archive annotation census
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m31gn7263sfhfbq8xfabkh3p
created_at: 2026-09-21T08:18:10.190Z
updated_at: 2026-10-06T08:47:23.874Z
closed_at: 2026-10-06T08:47:23.874Z
close_reason: "Done: packing/devtools/check_archive_annotations.py on origin/main recomputes the file, banner and README census counts and fails on any disagreement; it is a step in packing/src/sqpack/cli/validate.py and has tests (packing/tests/test_check_archive_annotations.py)."
resolution: null
duplicate_of: null
---
PR 204 review finding F4 (Medium). AGENTS.md makes the count the guarantee - repairs flagged inline and counted in the archive README - and PR 204 moves Bentz 2016 from 3 to 7 across packing/resources/README.md:128, the file banner, and the D-505/D-506 fix fields. It is correct (hand-verified 7 markers = banner = README) but nothing under packing/devtools/ or packing/tests/ recomputes it, while the defect count is gated end to end. A miscount would pass every gate and silently degrade the one ground-truth boundary the repo keeps against an external source.
