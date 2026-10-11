---
type: is
id: is-01m3qnty2dvtgva1s2tdp5m33p
title: Isolate negative-control snapshot cache probe from concurrent xdist workers
kind: bug
status: closed
priority: 1
version: 3
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
labels: []
dependencies: []
parent_id: is-01m3p5wj25knm7rbx0g4a4tpvg
created_at: 2026-09-29T22:51:15.393Z
updated_at: 2026-10-06T08:34:56.075Z
closed_at: 2026-10-06T08:34:56.075Z
close_reason: |
  Done (bead review 2026-10-06, origin/main eb43ffe9a): packing/tests/test_negative_controls.py on origin/main runs the 1,000,003-byte cache probe inside the private control snapshot via a child process and asserts the live root stays free of it (assert not CACHE_PROBE_ROOT.exists())
resolution: null
duplicate_of: null
---
The slow cache-exclusion regression writes a deliberately counted 1,000,003-byte file under the live packing root. Concurrent xdist workers can call snapshot_source_bytes during that window, producing an exact +1,000,003-byte cap failure. Move the probe into a private mutation snapshot while preserving the ordinary-byte and cache-exclusion assertions; do not raise the cap or prune evidence.

## Notes

Root cause confirmed on 2026-09-29: the failed snapshot count 168,549,242 exceeded the clean count 167,549,239 by exactly CACHE_PROBE_BYTES (1,000,003). The slow cache regression wrote packing/.negative-control-cache-probe/counted.bin in the shared checkout while another xdist worker measured snapshot_source_bytes. Commit 82600c1bc moves the mutation into an existing private control snapshot and a source-bound child process; it preserves the exact ordinary-byte increment, complete cache stripping, retained counted-file, real cap assertion, and live-root absence checks. Concurrent focused reproduction passed 2 tests in 51.98s with -n2; Ruff check/format and BasedPyright are clean. Independent static review found no blocker. Leave open until integrated published CI passes.
