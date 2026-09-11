---
type: is
id: is-01m27md3ey54fd0hcsygp9fggs
title: State the tolerance the gap bar decides 'met' against
kind: bug
status: open
priority: 3
version: 1
spec_path: docs/project/specs/active/plan-2026-09-09-packing-strategies-as-a-shared-language.md
labels: []
dependencies: []
created_at: 2026-09-11T07:02:40.861Z
updated_at: 2026-09-11T07:02:40.861Z
---
Three steps in 290..324 report a drawn side about 1e-6 above the record -- n = 300 gives 17.824124 against a record of 17.824123, n = 303 and 306 differ only past the sixth decimal. That is the rounding of the printed value, not a real excess, but 'met' is currently decided against it with an implicit tolerance. State the tolerance and compare against it.
