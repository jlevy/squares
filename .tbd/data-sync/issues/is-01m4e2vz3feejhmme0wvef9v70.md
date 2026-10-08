---
type: is
id: is-01m4e2vz3feejhmme0wvef9v70
title: Move oversized archived PDFs to hosted data and enforce a tracked-PDF budget
kind: task
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-06-exact-side-values.md
delegate: codex-polynomial-01a118e4
labels: []
dependencies: []
parent_id: is-01m4e2gm6ya1mxg40qmv53ysbn
hold: null
hold_until: null
created_at: 2026-10-08T15:42:18.222Z
updated_at: 2026-10-08T18:19:29.514Z
started_at: 2026-10-08T15:45:52.754Z
---
Migrate every tracked source PDF above a universal 5 MiB cap through the existing hosted-data system. All 13 original byte streams totaling 198944687 bytes are published at data/source-pdfs-v1 and independently checked against original sizes and SHA-256 digests. A missing-file fetch roundtrip for the 25831878-byte El Moumni source passes. Original and fetched working copies were staged recoverably with trash; external-volume Trash remains unemptied. Final committed HEAD and index each contain 135 PDFs totaling 135223924 bytes, with no cap violations; largest is 5127570 bytes. The retained guard reads staged blob metadata or full recursive committed trees, handles mixed-case/nested paths, fails unresolved stages, and runs in CI. Independent Astra review found and confirmed repair of the nested full-tree regression. No history rewrite or cap exemptions. Child publication and final-head CI disposition remain in parent think-okcb.
