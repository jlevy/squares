---
type: is
id: is-01m5h02h8ky80gse6egsxr1jhg
title: "Quote YAML plain scalars that a ' #N' cuts short: results.yaml:8042, verifiers.yaml (10+ written_by settings from 1925), upper-bounds-20261014/comments.yaml:41"
kind: task
status: open
priority: 3
version: 1
labels:
  - records
dependencies: []
created_at: 2026-10-22T05:06:52.819Z
updated_at: 2026-10-22T05:06:52.819Z
---
Found by c-lane-pr-b on 22 October 2026 while fixing the same defect in result-requests.yaml (#565's ask, #684's summary and four others, fixed in PR-B). An unquoted plain scalar that contains ' #' ends there: YAML reads the rest as a comment. Scan (yaml.compose over every tracked YAML outside packing/resources/, plain scalars followed on their line by whitespace + '#digit'): packing/frontier/results.yaml line 8042 (a review's reviewer 'claim-chain review lane of the 3 October import of #316, separately prompted' reads 'import of'); packing/frontier/verifiers.yaml lines 1925, 1965, 2006, 2046, 2081, 2118, 2158, 2200, 2239, 2277 and more (written_by setting 'the mathematical-correctness review lane of the #557 intake, ...' reads 'lane of the'); packing/campaign/issue-intake/upper-bounds-20261014/comments.yaml line 41 ('the same claim as #582' reads 'the same claim as'). Done when: each is quoted or folded with its full text, the rendered views (VERIFIERS.md, RESULTS.md) re-rendered, intake_comments --check still passes for the 14 October ledger, and a test or check refuses a plain scalar cut by ' #' in the registers. blocked_on: none
