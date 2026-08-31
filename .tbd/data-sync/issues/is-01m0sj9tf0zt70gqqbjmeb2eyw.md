---
type: is
id: is-01m0sj9tf0zt70gqqbjmeb2eyw
title: Keep byte-exact raw literature compatible with Git whitespace checks
kind: bug
status: closed
priority: 2
version: 2
spec_path: explorations/packing/resources/README.md
labels:
  - packing
  - process
  - literature
dependencies: []
parent_id: is-01m0shtf6wg4kdc42rrakz1r7w
created_at: 2026-08-24T09:40:52.308Z
updated_at: 2026-08-24T09:43:16.529Z
closed_at: 2026-08-24T09:43:16.528Z
close_reason: Added a path-scoped .gitattributes whitespace exemption for byte-faithful resources/**/*.raw.md; preserved both source hashes and verified git diff --cached --check passes with the raw files staged. Logged as D-141.
resolution: null
duplicate_of: null
---
New faithful pdfminer raw extraction contains trailing blank-line spaces, which git diff --cached --check reports even though normalizing them would break the archive's byte-level ground-truth contract. Acceptance: add a path-scoped .gitattributes exemption only for explorations/packing/resources/**/*.raw.md, preserve all recorded hashes, verify git diff --cached --check passes, and record the conflict/fix in the defect log.
