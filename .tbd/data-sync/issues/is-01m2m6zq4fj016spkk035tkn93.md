---
type: is
id: is-01m2m6zq4fj016spkk035tkn93
title: "PR #180 review R2: declare nested package parse-mode changes"
kind: bug
status: in_progress
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2m6y4gw224dgrwf37bgqnhd
created_at: 2026-09-16T04:18:18.382Z
updated_at: 2026-09-16T04:18:53.468Z
---
Enumerate every tracked nested package.json that can change JS module parsing, especially type=commonjs, and require an exact declared set with reasons. A planted undeclared package must fail the floor contract.
