---
type: is
id: is-01m2ae6nqy69685v8r37nvd7ya
title: Stop PDF diagnostics from reading object types out of stream payloads
kind: bug
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: root integration lane
labels: []
dependencies: []
parent_id: is-01m26rygs7f0s76v147x0px4cd
created_at: 2026-09-12T09:12:02.045Z
updated_at: 2026-09-12T14:13:40.644Z
closed_at: 2026-09-12T09:22:59.269Z
close_reason: Corrected in 237c4023 and covered by focused regression, static, generated-view, and clean exact-commit browser checks; final publication gates continue in think-o96l.
resolution: null
duplicate_of: null
---
The PDF difference classifier bounds its type search by endobj and 400 bytes but not by the stream boundary. An untyped object whose stream payload begins with /Type /Link is therefore mislabeled as a declared Link. Bound the declaration scan to the object dictionary before stream, add a focused regression using an untyped stream payload, and run the PDF diagnostic and static validation suite.

## Notes

Fixed at 237c4023. The object declaration scan now stops at endobj, 400 bytes, or the first stream boundary, whichever comes first. A regression places /Type /Link inside an untyped stream and proves the report names only object 7. Nineteen PDF cases, the combined 36-test focused run, Ruff, BasedPyright, and exact-commit Chromium controls pass.
