---
type: is
id: is-01m2mgefcdvttwqkr62hh67fh5
title: "PR #181 integration: scope PDF browser-control probes on pull requests"
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m2m6xx00sabcq5zqkrneavd0
created_at: 2026-09-16T07:03:39.144Z
updated_at: 2026-09-16T07:06:17.326Z
closed_at: 2026-09-16T07:06:17.318Z
close_reason: "Completed at PR #181 head 529a9512: pages_scope derives tests/probes/<test module> runtime assets for workflow pytest controls, every pdf_math_browser probe selects the explainer, and the focused suite passes 100 tests with 6 hosted-browser skips."
resolution: null
duplicate_of: null
---
At final head 87f3b9f1, packing/tests/test_pdf_math_browser.py:34-42 loads runtime controls from packing/tests/probes/pdf_math_browser/, but devtools.pages_scope.declared_inputs() (packing/devtools/pages_scope.py:244-255) only includes builder inputs, executed Python files, their Python import closure, the workflow, and pages_scope itself. render_explainer.RENDER_INPUTS (packing/devtools/render_explainer.py:2510-2533) includes packing/devtools/probes but not packing/tests/probes/pdf_math_browser. Reproduction with project Python 3.14: decide(['packing/tests/probes/pdf_math_browser/font_fault.js'], declared_inputs()) returns explainer=false and workbench=false. The push filter includes this tree, but pull requests have no paths filter and rely entirely on pages_scope. packing/tests/test_pages_workflow.py:162-179 says PRs are covered yet checks only push patterns, so the missing scope remains green. A control-only PR can therefore skip the PDF job that is its sole semantic execution. Add the control-probe directory to the explainer's declared PR inputs (or derive non-Python runtime assets of executed tests) and add a pages_scope assertion that each probe path selects explainer; retain the push-filter assertion.
