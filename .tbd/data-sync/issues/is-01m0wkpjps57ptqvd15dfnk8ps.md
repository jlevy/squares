---
type: is
id: is-01m0wkpjps57ptqvd15dfnk8ps
title: Route provenance Git probes through validation timeout seam
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/src/sqpack/cli/validate.py
delegate: validation_timeout_policy
labels:
  - packing
  - robustness
  - testing
dependencies: []
parent_id: is-01m0vpakbh6fy8p18cxsmtydgd
created_at: 2026-08-25T14:03:02.232Z
updated_at: 2026-08-25T14:19:53.428Z
closed_at: 2026-08-25T14:19:53.427Z
close_reason: Implemented bounded Git provenance probes; focused regression passes.
resolution: null
duplicate_of: null
---
The first production-timeout draft routed normal validation commands through the finite context default but left _commit_state's git cat-file and git merge-base subprocesses on raw subprocess.run, so a provenance step could still hang outside the new seam. Route both through the bounded return-code-preserving primitive, add focused coverage, record the defect, and keep D-239 open for pure-Python/aggregate/Windows limits.
