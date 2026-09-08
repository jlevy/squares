---
type: is
id: is-01m1v4w69xve0jbm4d203ck53j
title: Remove historical proof-condition uses of the C0-C5 epistemic labels
kind: task
status: closed
priority: 2
version: 2
labels:
  - documentation
  - epistemics
dependencies: []
parent_id: is-01m1sn5t0dm6rjj200pw5p1b7a
created_at: 2026-09-06T10:40:24.892Z
updated_at: 2026-09-06T10:41:59.247Z
closed_at: 2026-09-06T10:41:59.246Z
close_reason: The branch already used neutral former-condition names in both historical reviews; replaced the sole remaining ambiguous quoted 'C4 decision' with 'coverage decision'. A targeted maintained-prose audit now finds only epistemic uses of C0-C5 in the touched reviews, and Flowmark completed without further change.
resolution: null
duplicate_of: null
---
The repository reserves C0 through C5 exclusively for epistemic confirmation. Historical PR78/PR80 reviews still reproduce former proof-condition labels using those tokens. Rewrite the mappings as 'former symmetry condition', etc., while preserving historical meaning; audit maintained non-archive prose so every remaining C0-C5 token denotes epistemic confirmation. Acceptance: targeted historical tables are unambiguous, no mathematical provenance changes, Flowmark passes, and the terminology lint/gates stay green.
