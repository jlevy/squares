---
type: is
id: is-01m2m66zx2kaa04dgecjgzvj8b
title: The used half of the probe check is forgeable by a dead constant
kind: task
status: deferred
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01m2m4aptpzqgmmhqxgxz3vba5
created_at: 2026-09-16T04:04:48.161Z
updated_at: 2026-09-16T05:10:31.934Z
---
Lane L4, second half: check_probes counts a probe used when any string literal in a caller beside the tree equals its name, so a dead constant or a docstring counts. Tightening it to real reachability is what the module docstring deliberately declines -- a name that reaches the loader through a tuple, a loop or a helper still has to count -- so the fix is a dataflow pass, not a narrower literal search, and it would trade a forgery nobody can exploit for false dead-probe reports. Deferred from #175 with that argument on the record.

## Notes

Deferred from PR #175: eliminating dead-string/docstring forgery without false dead-probe reports requires a dataflow pass through tuples, loops, and helpers. The merge-boundary fixes for actual Node-only callers and missing/invalid probes are complete; this is future precision work.
