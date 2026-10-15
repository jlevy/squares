---
type: is
id: is-01m50ey9mm24zk1872jxfyn3a7
title: Normalize News prose, Markdown typography and mathematical notation
kind: bug
status: in_progress
priority: 1
version: 8
delegate: codex@spud10.local
labels: []
dependencies: []
child_order_hints:
  - is-01m50f9b766c52vrtq1ew2p95j
  - is-01m50fdg13gkf8mszjd06c5asb
  - is-01m50febxgjt75fmvmbfk6r3h6
  - is-01m50fpqk70xdm3m5vsbacpkq1
hold: null
hold_until: null
created_at: 2026-10-15T18:59:37.224Z
updated_at: 2026-10-15T19:55:27.820Z
started_at: 2026-10-15T19:01:01.841Z
---
Audit every News/changelog article for overly verbose prose, inconsistent n/N packing notation, literal equations or code formatting used for math, and Markdown typography. Reuse the established site math renderer and shared article styling on News and homepage cards. Preserve scientific claims, author credit, significance/rung caveats, dates, entry IDs, PR membership and delivery evidence. Add focused rendering controls, build and inspect a real preview, independently review and ship. Root owns Git/beads/release integration; renderer and prose writers have disjoint paths.

## Notes

PR623 merged at 6e73ef1c2b88fbbd349247b9f86d34fb46a01d4e from final reviewed source f026be7a892d9909efc418b823ceead7a5c4f0db. Independent Astra senior A5538976175 and security B5538977701 are clear, 27 changed paths covered. Matching-head Packing38796366140 and Pages38796365877 are fully green; Packing wall484s (8m04), three-minute goal remains open. Local147 integrated,42 renderer and111 native component tests passed; the broad807.26s pre-push failed10 nodes, subsequently all10passed in targeted groups plus negativecontrol (11 checks). Exact failure and repair evidence remains recorded, no whole-suite rerun presented as green. Eight owner visual checklist items are in PRbody. Production Pages deploy/verify and main native owners are being watched at the exact merge; root will check actual live v0.7.10 News/tutorial/About before closing. Durable receipt: primary .codex/regularization-closeout-evidence-2026-10-13/pr623-reader-corrections-20261015.json.
