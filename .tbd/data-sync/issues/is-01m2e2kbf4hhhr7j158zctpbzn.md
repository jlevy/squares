---
type: is
id: is-01m2e2kbf4hhhr7j158zctpbzn
title: "PR157: resolve failing PDF build check before merge"
kind: bug
status: in_progress
priority: 1
version: 6
assignee: root
delegate: pdf_control_sol
labels: []
dependencies: []
parent_id: is-01m2csyyq4nzfqppqj639avs51
created_at: 2026-09-13T19:06:12.323Z
updated_at: 2026-09-13T21:13:34.370Z
---
At remote head cadbf7e1 on 2026-09-13, certificate-page build job 103770982964 failed at render_explainer_pdf --check-artifact: two normalized 843157-byte PDFs differ first at byte 524772 in object 156. CI reports cause unknown and retains /tmp/explainer-pdf-check/pdf-check-644lkxd1 diagnostics. This is an occurrence of tracked D-490 (think-ptit), not evidence that PR157 source caused it. Retrieve artifacts, diagnose or rerun with evidence, then push and wait full hosted CI; keep separate from PR156 admission.

## Notes

Read-only September 13 20:03 UTC GitHub check: PR157 advanced from failing cadbf7e1 to head 876c5945, base still published PR156 52e4ab65, mergeState CLEAN; all active hosted checks including build, validate, suite, font-loading, macOS portability, and packing-required now SUCCESS, with policy-deferred jobs SKIPPED. This supersedes the earlier failed D-490 occurrence for this PR head. Cause and code change have not been independently reviewed here; PR156 base is about to advance from 52e4ab65 to local 9c56e901, so stacked CI must be rechecked after that push. Generic D-490 remains separate under think-ptit.

2026-09-13 21:13Z: Optional prepared-text control/treatment diagnostic is functionally complete in four uncommitted files. Sol 65 focused tests, Ruff and BasedPyright pass; Astra verifier independently accepted 75 tests and confirmed default untraced strict artifact gate unchanged. Early evaluate failure now records interrupted/unknown mutation state. Local saved-HTML Mac full-Chrome two-draw control and treatment both passed; an intermediate control mismatched one normalized PDF byte. No causal conclusion or Linux fix. Required --push gate active since 20:54:30Z at /private/tmp/pr157-pdf-control-push-artifacts; commit/push/manual Linux dispatch pending its exact result. Historical D-490 root cause think-ptit remains open.
