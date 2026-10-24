---
type: is
id: is-01m5nq1jz1wykwtgx07hbhdqmk
title: "PR #758 follow-up review B"
kind: task
status: in_progress
priority: 2
version: 4
delegate: c-rev-758b-1024
labels: []
dependencies: []
parent_id: is-01m5myjasmbm71pa68wgypjv9s
child_order_hints:
  - is-01m5nr6nr7740kpr59fd8c049v
hold: null
hold_until: null
created_at: 2026-10-24T01:05:16.769Z
updated_at: 2026-10-24T01:25:32.039Z
started_at: 2026-10-24T01:05:24.893Z
---

## Notes

2026-10-24 c-rev-758b-1024: review B (follow-up, round 2) of PR #758 published as a PR comment: https://github.com/jlevy/squares/pull/758#issuecomment-6378129147
Marker: <!-- tbd:review v=1 id=B kind=follow-up pr=758 round=2 head=d7645385283ba99b48f7ad2e3f3236099d8ad407 base=64b316b6cc8fa31177824e20733853708b996fb5 -->
Verdict: changes requested before merge, one High.
- B1 High: the #725 story (couzo-and-polkovskyi-certificates-confirmed, site-changelog.yaml:76-82, :99-103) contradicts main after #753 (merged 01:03Z 24 Oct): "as Evan Daniel regularized it" (204 lineage withdrawn), "now the houses at both counts" (T-231 since 24 Oct), "not yet imported or drawn" (T-231).
- B2 Medium: A7 partial; #644 summary still "now draws" / "drawings stay" (:450-454) against the new later line (:462-464).
- B3 Low: #657 details present tense at 154, 204, 271, 303 (:420-422).
- B4 suggestion: A16 deferral note; result-import.md:1289 is a second "S3 News stays optional".
Dispositions: A1, A3-A6, A8-A15 hold; A2 held at head, not on main (B1); A7 partial (B2); A16 deferral justified.
Tests at d76453852: render_changelog --check (origin/main 5f5294d82) exit 0; pytest tests/test_changelog.py 63 passed.
