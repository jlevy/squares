---
type: is
id: is-01m5fqbw4gey86dc038cvz6aef
title: Share significance result tallies and separate credit counts across projects and profiles
kind: task
status: closed
priority: 2
version: 5
delegate: profiles-data-integration
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-21T17:15:27.247Z
updated_at: 2026-10-21T21:45:33.722Z
started_at: 2026-10-21T17:17:38.514Z
closed_at: 2026-10-21T21:45:33.721Z
close_reason: Completed bounded implementation, reviewed evidence and local/hosted feature acceptance. Final-head CI and separate runtime/evidence followups remain open.
resolution: null
duplicate_of: null
---
One reusable model and rendering component for reviewed primary-authored distinct Results, disjoint nonprimary person/result Credits and descending S5 through S1 breakdowns. Share across homepage project cards, directory and profile pages; deduplicate per result/person, keep project received-credit scope tied to exact source evidence, and preserve blank-zero and optional-link behavior.

## Notes

Single occupied significance level uses compact wording: 1 result at S5 or 3 results at S4. Mixed levels retain parenthesized descending breakdown. Credits are separately defined reviewed attribution entries, not derived result-list rows; project credit scope must stay local to the project, not all owner credits.

Completed final semantics: one shared ResultTally/CreditTally and rendering path serves project cards, directory rows and profiles. Results are reviewed primary-authored T IDs; Credits are disjoint nonprimary person/result associations, deduplicated once per citing result and scored from that result. This supersedes the earlier recorded-mention wording in these notes. Project received credits remain restricted to reviewed project authors and exact project-source evidence. Counts, descending significance histograms, single-level parentheses, optional links and blank-zero behavior are covered. Local post-adoption identity/tally/coverage selection passed 54 tests in 8.47 seconds; the final project-card/resource/Chromium module passed 16 tests in 36.79 seconds with all original assertions retained.

Final integration evidence: the scoped work is committed and published in https://github.com/jlevy/squares/pull/578, currently at db3cb6d4fe5f00a44d04a8ef91018aa2b365bad8. Hosted validation at e162a870a899a61cc77cd47fa2f56c0ff388c8ea passed Pages, Packing Validate and suites B/C; suite A passed all 4,364 assertion tests, then failed only the separate project-tally CALL wall guard. That independent runtime defect is fixed in e3e33171bf1d687190cc957a40e25fbbc9dbb23c and remains tracked by think-rolz while final-head CI runs. The exact final db3 CI verdict is not claimed here. This closure is for completed bounded acceptance; the overall think-zpfo handoff, think-uwd6 coverage parent, historical registrations, pending PDF census and real evidence gaps remain open.
