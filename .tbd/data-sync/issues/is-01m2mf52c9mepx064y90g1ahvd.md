---
type: is
id: is-01m2mf52c9mepx064y90g1ahvd
title: "PR #181 integration: replace inherited pdf.SETTLED script argument"
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m2m6xx00sabcq5zqkrneavd0
created_at: 2026-09-16T06:41:02.338Z
updated_at: 2026-09-16T06:53:40.585Z
closed_at: 2026-09-16T06:53:40.584Z
close_reason: "Completed at PR #181 head 7f990cbb: the PDF browser test now imports the existing file-backed SETTLED probe instead of passing an opaque module attribute. Guard: 907 Python files, zero sites; focused tests: 139 passed, 6 skipped; probe check: 387/387."
resolution: null
duplicate_of: null
---
Merging final #179 into #181 makes the strengthened no-embedded-JavaScript guard catch packing/tests/test_pdf_math_browser.py passing pdf.SETTLED directly to wait_for_function. Move this remaining executable JavaScript expression into the existing file-backed probe boundary and add/retain contract coverage so #181 actually reaches zero Python sites.
