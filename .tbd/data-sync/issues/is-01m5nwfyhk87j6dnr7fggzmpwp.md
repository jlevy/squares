---
type: is
id: is-01m5nwfyhk87j6dnr7fggzmpwp
title: "PR #766 (merge): senior review"
kind: task
status: in_progress
priority: 2
version: 4
delegate: c-rev-766-1024
labels: []
dependencies: []
parent_id: is-01m5nq1f8n1jcjddbfz2zx2x97
child_order_hints:
  - is-01m5nxqvt6ga8v5hqr0akqjk44
hold: null
hold_until: null
created_at: 2026-10-24T02:40:30.259Z
updated_at: 2026-10-24T03:02:18.182Z
started_at: 2026-10-24T02:40:36.971Z
---

## Notes

2026-10-24 c-rev-766-1024: senior review A, round 1, of PR #766 at head 41d16f773 (merge base da117ad0b), posted as a PR comment: https://github.com/jlevy/squares/pull/766#issuecomment-6379048844 (jlevy, 03:00:52Z). No earlier tbd:review marker existed on the PR.

Verdict: approve; nothing blocks merge. Findings: A1 Medium, A2-A4 Low, A5 a suggestion; no Blocker or High.
- A1 (Medium): result-requests.yaml:17508-17509 and :19701-19702, and reply-715.md:24 and :15, call think-rx26 "the record's own exact check of the certificate". think-rx26 is the exact check of the 8 October decimal poses (its title; the record's own :19607). The 02f9690 certificate was already decided exactly in couzo-exact-certificates-2026-10-09. The text also omits the author's own conclusion, "the bound we stand behind is the certificate's". No impact: f1ceee4's 335 is 1.607e-12 below the print, so it supersedes the row either way.
- A2 (Low): reply-670.md:30 omits T-229 (23 October) from T-226's superseders, which the record (results.yaml:31396-31399) names.
- A3 (Low): reply-719.md:18 puts the three hop rounds between T-186 and #678. They end at #670's certificate, which #678 refines.
- A4 (Low): reply-734.md:24 says the runbook uses four checkers; result-import.md names only devtools.exact_sides.
- A5 (suggestion): rewrap bibliography.yaml:3352, results.yaml:31357 and :31848.

Verified:
- The six chain credit lines, re-derived from T-186's 204 lineage (T-162 via T-174) in T-186's order. Nakajima is not carried, consistent with T-174 and T-186. Short credits are unchanged.
- occurrences.yaml, compared semantically: 41 spans correct (Ostashev joined to daniil-ostashev; PingYou Ltd non-person), and the other 1,598 rows are identical.
- Upstream blobs: n204.txt is ba1fb29 (SHA-256 3e7c2456); best/n204.cert is 301c930, the same as 70a033f's square-204.cert (SHA-256 f0885fa8, as T-186's sources.json records). Both were first committed at 4e4c8ce.
- My own pairing gives 3.936016e-12; my own wall counts give 32 and 88.
- #670, #675, #719 and #734 records match the comments. #725 News keeps its date and PR.
- The intake-watch trees are equal.

Tests, all passing:
- pytest -n 2 on the three named modules: 126 passed.
- seed-identity test: 1 passed.
- contributor_census --stale: [].
- check_requests: exit 0.
- render_changelog --check at origin/main da117ad0b: pass.
- acquire_source --check on the three packets: PACKET_MATCHES_ITS_CONTRACT.

After the pin, main moved to c35b21a14 (#765, #767). #765 touches CHANGELOG.md and site-changelog.yaml; the merge-tree is clean. render_changelog --check against c35b21a14 refuses the un-merged branch on #765's new frozen entry. Re-run it after the merge-prep re-merge.

No dedicated review is warranted. Nothing was committed, pushed, posted on issues or synced.
