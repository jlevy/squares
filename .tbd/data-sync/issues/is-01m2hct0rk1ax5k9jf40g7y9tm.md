---
type: is
id: is-01m2hct0rk1ax5k9jf40g7y9tm
title: "PR #125 review D27: development.md setup omits npm ci and hand-copies a step count"
kind: bug
status: closed
priority: 2
version: 4
labels: []
dependencies: []
parent_id: is-01m2hb401yy3ph99cfn5mhpcv4
created_at: 2026-09-15T02:02:19.794Z
updated_at: 2026-09-15T02:13:11.281Z
closed_at: 2026-09-15T02:13:11.280Z
close_reason: "Fixed in 6eb6a3df: setup recipe starts with npm ci --ignore-scripts (and names make hooks-install); hand-copied step count dropped."
resolution: null
duplicate_of: null
---
Review source: PR #125 review F26 (Medium); triage row D27. The tier table half is fixed in #160 at 15d97a59.

development.md Supported Environment (:24-30) says uv sync then packing-validate --fast, but with no node_modules the browser floor step raises StepFailureError, so the recipe fails without npm ci. development.md :137 hand-copies the full checkpoint's step count (74), which is wrong on every PR (75 on #125, 76 on #160). Decision: drop the count rather than correct it.
