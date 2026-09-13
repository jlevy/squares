---
type: is
id: is-01m2e2kbf4hhhr7j158zctpbzn
title: "PR157: resolve failing PDF build check before merge"
kind: bug
status: in_progress
priority: 1
version: 3
assignee: root
delegate: root
labels: []
dependencies: []
parent_id: is-01m2csyyq4nzfqppqj639avs51
created_at: 2026-09-13T19:06:12.323Z
updated_at: 2026-09-13T19:15:45.500Z
---
At remote head cadbf7e1 on 2026-09-13, certificate-page build job 103770982964 failed at render_explainer_pdf --check-artifact: two normalized 843157-byte PDFs differ first at byte 524772 in object 156. CI reports cause unknown and retains /tmp/explainer-pdf-check/pdf-check-644lkxd1 diagnostics. This is an occurrence of tracked D-490 (think-ptit), not evidence that PR157 source caused it. Retrieve artifacts, diagnose or rerun with evidence, then push and wait full hosted CI; keep separate from PR156 admission.

## Notes

September 13 root takeover: raw failed pair and exact prepared HTML were saved before any retry. Independent byte and visual review localizes this occurrence to one tan baseline on page 15, about 0.164095 PDF points; all text and embedded fonts match, but the upstream cause is unproven. A narrow optional math-layout trace is undergoing independent review and a real-browser smoke; the ordinary exact artifact gate remains unchanged. Current PR156 owner separately completes its newer continuation. No retry, normalization relaxation, main merge, or deployment has occurred.
