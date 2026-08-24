---
type: is
id: is-01m0shjchxzwd7t1yg829bkjte
title: Correct stale n=3 constant-contact-certificate claim
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/sqpack/canonical.py
labels:
  - packing
  - focus-soundness
dependencies: []
parent_id: is-01m0shdh4arvmv3vyfyfpnqfpx
created_at: 2026-08-24T09:28:04.412Z
updated_at: 2026-08-24T10:48:19.769Z
closed_at: 2026-08-24T10:48:19.769Z
close_reason: D-140 is fixed. Living claims now distinguish the open n=3 stratum certificate from the wall-endpoint certificate while preserving one connected family; exp-014 and the permanent gate replay reject the stale constant-closed-family claim and byte-check the quotient SVG.
resolution: null
duplicate_of: null
---
After D-093 restored node attributes, the closed n=3 sliding family no longer has one constant contact certificate: t=1/2 and 3/2 have wall-count multiset [2,2,2], while the open stratum has [1,2,2]. Current canonical.py, D-034, SYNOPSIS, the master review, the PR15 response, and the landscape report retain the old constant-hash wording. Correct every living claim while preserving the real counterexample: infinitely many interior geometric keys share one certificate and all strata lie in one connected family. Add exact n=3 stratum regression under exp-014.
