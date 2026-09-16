---
type: is
id: is-01m2m4c5qza96ejf8s6j3rvhpd
title: "PR #179 review R3: the ESLint directory list grew by hand again"
kind: bug
status: in_progress
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01m2m4c4g60321je3x66a98ne5
created_at: 2026-09-16T03:32:40.830Z
updated_at: 2026-09-16T04:53:29.890Z
---
packing/src/sqpack/cli/validate.py:1539. Same finding as #175 R4; this PR is where the cost first showed. (PR #179, review 5218208340)

## Notes

Deduplicated with PR #175 R4 / think-esf6. The executable ESLINT_PATHS contract fix is commit 0ab75b7c, recovered locally but not yet in the remote #175 ancestry. Close this child only after the integrated #175 head containing 0ab75b7c is pushed and propagated into #179.
