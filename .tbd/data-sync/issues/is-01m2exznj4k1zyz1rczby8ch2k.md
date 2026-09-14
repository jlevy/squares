---
type: is
id: is-01m2exznj4k1zyz1rczby8ch2k
title: "N11 strategy reset: significant bound improvements or a much simpler proof"
kind: epic
status: open
priority: 1
version: 9
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - strategy
dependencies: []
parent_id: is-01m24sm7wm3s5eh8ke6vze7mw1
child_order_hints:
  - is-01m2ey0af1m0nfd9942ffkby3a
  - is-01m2ey0c330crgmbpxncejahnx
  - is-01m2ey0d8smw4f4w72hyay9070
  - is-01m2ey0dsfhs4cfjqhy7098m7h
  - is-01m2gt509a6wa4kqwbxjrq6exd
  - is-01m2gtknsgp4pb350pdwshx3ek
created_at: 2026-09-14T03:04:47.426Z
updated_at: 2026-09-14T21:09:03.090Z
---
Owner direction, 2026-09-14: stop heavy computer-assisted work aimed at microscopic lower-bound gains. Prefer routes likely to improve the n=11 bounds materially or simplify the proof of s(11) >= 3.82 substantially. The merged T-026 bound is the scientific cutoff; the checked current-state account is SYNOPSIS.md. BC-339/think-uqa4 performs the roll-up, then BC-346/think-9y7p selects exactly one next entry from a possible W5 efficiency checkpoint and Routes A (systematic case split), B (pairwise SDP), S (certificate compression), C (orientation structure), and D (upper-bound search). No route is authorized before that W10 selection.

## Notes

Current controller, 2026-09-14: PRs #156, #157, and #161-#167 are merged. BC-339/think-uqa4 is the checked research-state roll-up and remains the current W7/W8 session until its exact-revision gate is retained. BC-346/think-9y7p depends on it and is the separate W10 planning successor. The planning set is the possible W5 efficiency checkpoint plus Route A systematic case split, Route B pairwise SDP, Route S T-025/T-026 certificate compression, Route C orientation structure, and Route D upper-bound search. Every execution candidate depends on think-9y7p; H-160/H-162, weighted stages 3-4, BC329, and the old H135 reserve remain paused unless W10 reselects them.
