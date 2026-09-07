---
type: is
id: is-01m1yyryhm7gb2t4e1yegawqgr
title: "Cross-branch session-number collision: main and codex/n11-hybrid-overnight both allocated session-096"
kind: chore
status: open
priority: 2
version: 1
labels:
  - process
dependencies: []
created_at: 2026-09-07T22:10:44.902Z
updated_at: 2026-09-07T22:10:44.902Z
---
Found while merging origin/main into codex/n11-hybrid-overnight (PR #110, merge commit 7a2145f4): both sides had independently allocated session-096 and declared the receipt path codex-task-tree-session-096.yaml, so check_session_rollups refused the union (attributed to more than one branch) and packing-ledger render refused the duplicate id. Resolution taken: main's session-096 (started earlier, landed) keeps 096 and the plain receipt filename; the branch's session was renumbered to session-097 (record, receipt codex-task-tree-session-097.yaml, references in agenda-021, agenda-028, X-018, H-120, the four BC-282 result docs, the cartography plan and SYNOPSIS updated with repren); the frozen benchmark stdout logs keep the number they printed. Same shape as think-rzek (session-093 with PR #111). Tell the branch's owner their session is now 097, and consider allocating session numbers from a shared counter (a bead or the ledger on main) so parallel lanes cannot collide.
