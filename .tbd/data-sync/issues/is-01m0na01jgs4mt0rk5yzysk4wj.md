---
type: is
id: is-01m0na01jgs4mt0rk5yzysk4wj
title: Verify the hook actually blocks unformatted Markdown
kind: task
status: closed
priority: 1
version: 2
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0na001wtn9wb0fkwndgwwrq
created_at: 2026-08-22T17:58:45.584Z
updated_at: 2026-08-22T18:02:48.741Z
closed_at: 2026-08-22T18:02:48.741Z
close_reason: "Verified with a deliberately unformatted file: hook fired, file reformatted, git show HEAD confirmed stage_fixed committed the formatted version, and md5sums confirmed the archive .raw.md files were untouched."
---
Test with a deliberately unformatted file: confirm the hook catches it, and confirm it does not fire on the excluded paths in .flowmarkignore.
