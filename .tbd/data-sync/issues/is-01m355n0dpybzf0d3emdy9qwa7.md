---
type: is
id: is-01m355n0dpybzf0d3emdy9qwa7
title: Validate file-like evidence certificate paths and report figure-check coverage
kind: bug
status: open
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-09-22T18:22:04.213Z
updated_at: 2026-09-22T18:25:14.783Z
---
PR #220 review R3: check_rung_figures.evidence_limitation_problems blindly prefixes packing/ and silently skips unresolved or unsupported certificates. E-n011-five-dot-full-net and E-n011-five-dot-independent-union (T-023), E-n011-wall-owner-footprints and E-n011-wall-owner-containment already use packing/campaign paths. Correcting that prefix alone does not add figure coverage: these receipts are outside load_certificate supported formats. Add a semantic existence check for file-like evidence certificate values with explicit treatment of historical prose values, normalize the four paths, and report checked vs unsupported counts honestly. Registration docs now require reviewers to resolve files and execute replay commands.

## Notes

The same four legacy rows prefix replay commands with cd packing &&, so they were authored from repository root. Normalize certificate paths and replay working-directory convention together; the new registration guide uses packing-relative certificate paths and commands run from packing.
