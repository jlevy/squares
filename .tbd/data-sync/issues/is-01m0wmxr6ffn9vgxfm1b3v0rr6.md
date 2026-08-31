---
type: is
id: is-01m0wmxr6ffn9vgxfm1b3v0rr6
title: Reconcile D-318 stale mutation-control expectation
kind: bug
status: closed
priority: 3
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels: []
dependencies: []
parent_id: is-01m0w9a47h5zrn7jf16pp2kpxs
created_at: 2026-08-25T14:24:25.806Z
updated_at: 2026-08-25T14:25:57.033Z
closed_at: 2026-08-25T14:25:57.032Z
close_reason: Recorded D-318 and corrected the mutated unprotected-fix expectation to 105; schema, synopsis, and all 62 negative controls pass.
resolution: null
duplicate_of: null
---
The D-308 unprotected-fix negative control was left expecting the canonical 106 after the canonical record count changed; its mutated state is 105. Record and fix this conservative bookkeeping control defect, then rerun the negative-control suite.
