---
type: is
id: is-01m1qee2fyzhg168rccz8v2mrk
title: Vendor kpress as a submodule at vendor/kpress and cut a fix branch
kind: task
status: closed
priority: 2
version: 2
labels:
  - kpress-upstream
  - pr-79
dependencies: []
parent_id: is-01m1q3fmvn9py28rcm0q3jadvk
created_at: 2026-09-05T00:10:30.268Z
updated_at: 2026-09-05T00:10:31.007Z
closed_at: 2026-09-05T00:10:31.006Z
close_reason: Submodule at e4f9506 on squares/page-fixes (kpress commits ef3074c7 math sizing, e4f95068 footnote size; kpress lint and 597 tests green). Wiring went in with 387c3508, the two repo-check files with f8809796.
resolution: null
duplicate_of: null
---
Direction on PR #79: the kpress fixes the page needs (math sized to PT Serif, footnotes on the small token) are made in kpress itself. Submodule at vendor/kpress from https://github.com/jlevy/kpress, branch squares/page-fixes cut from v0.3.5 and pushed; uv source path ../vendor/kpress, editable; submodules: true on every CI checkout; README layout tree and document-map exclusion for the new directory.
