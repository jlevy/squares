---
type: is
id: is-01m0sz4jzd9jdsc65spmtygc2q
title: Archive PDF bytes triggered Git whitespace diagnostics
kind: bug
status: closed
priority: 2
version: 2
spec_path: explorations/packing/resources/README.md
labels: []
dependencies: []
parent_id: is-01m0n6rttj5zdmkgjxb3690bsb
created_at: 2026-08-24T13:25:12.288Z
updated_at: 2026-08-24T13:36:54.045Z
closed_at: 2026-08-24T13:36:54.044Z
close_reason: Archived PDFs are now explicitly binary, all three source SHA-256 digests remain unchanged, hand-written reading aids have no trailing whitespace, git check-attr reports diff/text unset for each scan, and the staged diff check passes. D-159 records the integration failure and fix.
resolution: null
duplicate_of: null
---
The recovered scanned PDFs were not recognized as binary by Git, so git diff --cached --check parsed compressed streams as text and emitted thousands of false trailing-whitespace diagnostics; the excluded hand-written reading aids also carried hard-break spaces. Acceptance: mark archived PDFs binary without touching source bytes, remove trailing whitespace only from reading aids, record the defect, add a regression check or explicit policy, and prove cached diff plus archive hashes pass.
