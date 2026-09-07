---
type: is
id: is-01m1yyryhm7gb2t4e1yegawqgr
title: "Cross-branch session-number collision: main and codex/n11-hybrid-overnight both allocated session-096"
kind: chore
status: open
priority: 2
version: 2
labels:
  - process
dependencies: []
created_at: 2026-09-07T22:10:44.902Z
updated_at: 2026-09-07T23:02:55.700Z
---
Found while merging origin/main into codex/n11-hybrid-overnight (PR #110, merge commit 7a2145f4): both sides had independently allocated session-096 and declared the receipt path codex-task-tree-session-096.yaml, so check_session_rollups refused the union (attributed to more than one branch) and packing-ledger render refused the duplicate id. Resolution taken: main's session-096 (started earlier, landed) keeps 096 and the plain receipt filename; the branch's session was renumbered to session-097 (record, receipt codex-task-tree-session-097.yaml, references in agenda-021, agenda-028, X-018, H-120, the four BC-282 result docs, the cartography plan and SYNOPSIS updated with repren); the frozen benchmark stdout logs keep the number they printed. Same shape as think-rzek (session-093 with PR #111). Tell the branch's owner their session is now 097, and consider allocating session numbers from a shared counter (a bead or the ledger on main) so parallel lanes cannot collide.

## Notes

Second collision on the same axis, now resolved across three PRs. PR #110 (codex/n11-hybrid-overnight) initially took 097 per this bead, then rekeyed its own record to session-098 in 1b953c95 ('reconcile concurrent merge with reserved session098') after an inventory of live worktrees found 097 already allocated to the kernel-pricing session; think-dwq8 reserves 098. Session 097 is held by PR #116 (codex/n11-kernel-pricing, session-097-kernel-contract-and-feature-pricing.md). PR #111 (claude/atlas-expansion-300-400-9f79fc) therefore could take neither: it was renumbered 093 -> 097 by its own main merge, and is now renumbered 097 -> 099 in commit 2ace8113 (record, title, id, and the SYNOPSIS / atlas-expansion plan / sources-beyond-100 references, via repren; ledger and close report regenerated). A complete inventory of all 80 origin refs plus that HEAD shows 099 free and unreserved; note the unmerged, PR-less branch codex/stromquist-n26-verification also still carries a session-097 record and will need its own rekey before it can land. Final allocation: 097 = PR #116, 098 = PR #110, 099 = PR #111. Root cause confirmed twice over: each merge agent picked max(main) + 1 while looking only at main, so parallel lanes chose the same number independently and a second round of renumbering was needed even after the first fix. This is the direct argument for the shared counter this bead proposes -- allocation must consult every open PR head and live worktree, not just main.
