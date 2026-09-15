---
type: is
id: is-01m2heyw3hw2aj0gznyxhgd4aj
title: "PR #160 review D52: enforced strategy documents are validated by nothing"
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T02:39:56.016Z
updated_at: 2026-09-15T02:40:55.691Z
closed_at: 2026-09-15T02:40:55.690Z
close_reason: "Fixed on #160 at e90187c8: validate_schemas corpus_paths now includes packing/strategies/*.yaml, so the three enforced documents are validated by the gate (a mutated document fails); test_ascent_and_strategies.py validates and decodes each and pins lock_order."
resolution: null
duplicate_of: null
---
Review finding, PR #160 stack triage (2026-09-14), lane D-tools.

Strategy documents marked `status: enforced` were loaded by no validator, and `capture_video` and `lock_order` had no test. Schema and code reconciliation was fixed at f9099096/15d97a59 (think-karf).

Source: #125 F17 (enforcement and test items).

Files: `packing/strategies/{assemble-then-tighten,sweep-landing,lab-components}.yaml`; `packing/devtools/validate_schemas.py` `corpus_paths`; `packages/workbench/tests/`.
