---
type: is
id: is-01m41cx3q2pckpmsmmwq1rsngz
title: Shrink PR 305's retained data and set one layout for retained JSON results
kind: feature
status: closed
priority: 1
version: 19
labels:
  - session-169
dependencies: []
parent_id: is-01m3xgkna3m3w1w50ky6gqyxyk
child_order_hints:
  - is-01m41cx4hamhczdr7c6fmkpy68
  - is-01m41cx57k479tywz7rqpgrceb
  - is-01m41cx5tj7pwgbrbb6dgk27da
  - is-01m41ephbrdagjrq2q882d007z
  - is-01m41hpr031ch3cs2tmhz1b6j9
  - is-01m41hprm9fep7d20thmgfhyd0
  - is-01m41hps746jvw6hg2jm3at3x5
  - is-01m41hpstenxdv8qt9zzvbk1m9
  - is-01m4206nmmpkyj14ke249x335p
  - is-01m424tye0ptksxhthdgqc60k3
  - is-01m42dfbtqy8q2sdjjck1sgcsv
created_at: 2026-10-03T17:27:33.847Z
updated_at: 2026-10-06T08:27:19.185Z
closed_at: 2026-10-06T08:27:19.185Z
close_reason: "Done: think-1uwx (PR 305) and think-k131 (PR 323, layout check) are merged (e19be6bb0, 2026-10-04). The owner decisions it held are top-level beads now (2pvg, giqi, l51e, 5o8i), and its last child 2qbn is closed."
resolution: null
duplicate_of: null
---
Owner question, 2026-10-03: PR jlevy/squares#305 adds 275,273 lines across 574 files; should it be that big? Measured: 83% of the lines are generated data. The two X-049 censuses (138,135 lines), the T-007 consumer audit (44,882) and the regularized index (15,653) are json.dumps(indent=2), one scalar per line: 198,647 lines for about 2,700 records. Written one record per line they take 2,691 lines and half the bytes, with nothing lost; git stores about 280 KB either way, so gzip would only cost readable diffs. The 51 regularized SVGs are 11 MB, after the house atlas's committed 324 SVGs (52 MB). Owner decision, 2026-10-03: adopt the record-per-line layout in this PR or a PR stacked on it, all in this line of work, tracked by beads and followed up by sub-agents. Children: the four files in PR 305; the repository-wide writer in a stacked PR; and the SVG question.

## Notes

2026-10-03 state: think-1uwx done in PR 305 (five files 201,257 -> 27,501 lines; PR 305 275,273 -> about 102,000 added lines before main's merges); think-k131 done in stacked PR #323 (31 files, 1,480,461 -> 155,443 lines, a layout check on every pull request); think-6o0h measured (keep the SVG drawings committed); think-nkp0 measured (squashing saves 0.5 MB; the repository's size is PDFs, gzip and PNG; four owner decisions filed: think-jhgi, think-giqi, think-2pvg, think-l51e). Open: PR 305's second merge with main (think-ak5w), then session-169's close with its rollups and a certifying gate.
2026-10-04: session-169 closed at 99defa2ea (gate at 0952efb57). This bead was closed then reopened: it stays open as the parent of its six open owner decisions (think-jhgi, think-giqi, think-2pvg, think-l51e, think-5o8i, think-4w2g), since an open bead may not sit under a closed parent (D-025). Close it when they are.
