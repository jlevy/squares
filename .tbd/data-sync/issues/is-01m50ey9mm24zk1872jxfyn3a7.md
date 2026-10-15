---
type: is
id: is-01m50ey9mm24zk1872jxfyn3a7
title: Normalize News prose, Markdown typography and mathematical notation
kind: bug
status: in_progress
priority: 1
version: 7
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
updated_at: 2026-10-15T19:36:22.132Z
started_at: 2026-10-15T19:01:01.841Z
---
Audit every News/changelog article for overly verbose prose, inconsistent n/N packing notation, literal equations or code formatting used for math, and Markdown typography. Reuse the established site math renderer and shared article styling on News and homepage cards. Preserve scientific claims, author credit, significance/rung caveats, dates, entry IDs, PR membership and delivery evidence. Add focused rendering controls, build and inspect a real preview, independently review and ship. Root owns Git/beads/release integration; renderer and prose writers have disjoint paths.

## Notes

Final reader changes at 81fd12161d5dc21ad6545b1297bd2aa85f468a4a; independent senior and dedicated security Astra reviews clear. PR body prepared with owner visual acceptance checklist for News math/styles/filters, homepage excerpts and verification caveats, expansion behavior, tutorial credits/dates, About links, H1 spacing/mobile/themes and v0.7.10 live footer. Root will verify matching-head CI, merged Pages deploy/verify and actual live pages before closing. 147 integrated tests, 42 renderer tests and 111 native component tests passed; broad native pre-push still running.
