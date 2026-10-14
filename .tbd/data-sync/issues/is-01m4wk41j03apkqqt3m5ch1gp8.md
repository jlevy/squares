---
type: is
id: is-01m4wk41j03apkqqt3m5ch1gp8
title: Align legacy independence label contract with unknown reading history
kind: bug
status: in_progress
priority: 2
version: 2
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wajcx0q76t3ppdzfbjxq4d
hold: null
hold_until: null
created_at: 2026-10-14T06:55:42.143Z
updated_at: 2026-10-14T06:57:10.882Z
started_at: 2026-10-14T06:57:10.882Z
---
PR592 verifier-registry test still expects after-reading for unstructured legacyrecord, while B4 correctlyrendersneutral independentimplementation. Update truthful expectation without weakening deciding-program, cleanroom or per-run independence controls.
