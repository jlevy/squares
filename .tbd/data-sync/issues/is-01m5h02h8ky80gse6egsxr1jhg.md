---
type: is
id: is-01m5h02h8ky80gse6egsxr1jhg
title: "Quote YAML plain scalars that a ' #N' cuts short: results.yaml:8042, verifiers.yaml (10+ written_by settings from 1925), upper-bounds-20261014/comments.yaml:41"
kind: task
status: open
priority: 3
version: 2
labels:
  - records
dependencies: []
created_at: 2026-10-22T05:06:52.819Z
updated_at: 2026-10-22T07:17:27.704Z
---
Found by c-lane-pr-b on 22 October 2026 while fixing the same defect in result-requests.yaml (#565's ask, #684's summary and four others, fixed in PR-B). An unquoted plain scalar that contains ' #' ends there: YAML reads the rest as a comment. Scan (yaml.compose over every tracked YAML outside packing/resources/, plain scalars followed on their line by whitespace + '#digit'): packing/frontier/results.yaml line 8042 (a review's reviewer 'claim-chain review lane of the 3 October import of #316, separately prompted' reads 'import of'); packing/frontier/verifiers.yaml lines 1925, 1965, 2006, 2046, 2081, 2118, 2158, 2200, 2239, 2277 and more (written_by setting 'the mathematical-correctness review lane of the #557 intake, ...' reads 'lane of the'); packing/campaign/issue-intake/upper-bounds-20261014/comments.yaml line 41 ('the same claim as #582' reads 'the same claim as'). Done when: each is quoted or folded with its full text, the rendered views (VERIFIERS.md, RESULTS.md) re-rendered, intake_comments --check still passes for the 14 October ledger, and a test or check refuses a plain scalar cut by ' #' in the registers. blocked_on: none

## Notes

2026-10-22 c-lane-pr-b (PR #720 review A, A7): the guard now exists for the requests record. devtools.check_requests.comment_cut_scalars(text) composes a YAML text and refuses every plain scalar whose line goes on with whitespace and '#'; the check_requests gate runs it on campaign/result-requests.yaml (commit 76961e6e7, test test_a_value_an_unquoted_hash_cuts_short_is_refused). Run over the others it finds exactly this bead's set: frontier/results.yaml line 8042, frontier/verifiers.yaml 20 written_by settings from line 1925, campaign/issue-intake/upper-bounds-20261014/comments.yaml line 41; source-coverage.yaml, evidence.yaml and intake-watch.yaml have none. To finish this bead: quote those 22 values, re-render VERIFIERS.md and RESULTS.md, then call comment_cut_scalars on the registers too (check_results / verifier_registry / intake_comments --check, or one small lint over every tracked YAML outside packing/resources/).
