---
type: is
id: is-01m51hjc9mv43jqr39c4zm038d
title: Refine News chooser states, shared topic colors and article spacing
kind: bug
status: closed
priority: 2
version: 18
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: lane-645
labels: []
dependencies: []
child_order_hints:
  - is-01m51hqspk8m12zgc20zpq0egm
  - is-01m51hqtms76wqmackh51re6ck
  - is-01m51hqvh38qx5w756bs9wsjak
  - is-01m51hqw58eewgc9g3bcqkte65
  - is-01m51hqwp9pv33x85ztqskn49g
  - is-01m52xzf9693npacscf5ght83b
hold: null
hold_until: null
created_at: 2026-10-16T05:04:46.887Z
updated_at: 2026-10-19T23:01:44.501Z
started_at: 2026-10-16T05:05:12.360Z
closed_at: 2026-10-19T23:01:44.500Z
close_reason: "PR #646 merged at 028bc72ec with site v0.7.35; deployment verified (Pages run 39337466599, 4708/4708). Children closed."
resolution: null
duplicate_of: null
---
Ship the requested News UI corrections: gray inactive topic filters, topic-colored active states and paler colored hover without text or inset underlines; borders follow wrapped button rows; remove both All controls and retain one unboxed Reset filters button. Give Optimality, Project and Engineering distinct shared colors, separate from lower/upper bounds and verification. Tighten title/date/tag/body spacing on shared homepage and News cards. Make significance meters horizontally tighter with borders matching label color, and shorten level tooltips while retaining detailed rationale in source records/docs. Reuse design tokens, preserve accessibility/filter semantics, verify desktop/mobile and light/dark behavior, document design changes, independently review, PR, merge and verify deployment.

## Notes

Draft PR https://github.com/jlevy/squares/pull/646 now contains the News controls, shared palette/card spacing, concise significance tooltips and site v0.7.15 edition. Source c4d56bb53 plus edition dfde01d7d; formatting-only follow-up is being pushed. Focused browser/contracts 82 passed; corrected spacing control 2 passed; component release tests111 passed; release-impact dispositions and document coverage pass. Independent preliminary senior review has no open source findings after A1 correction. S2/project; no separate News entry. Final hosted CI, matching checkpoint, final-head review, merge and deployment verification remain; do not report this draft merged or fully green.

2026-10-16 user-eb-addr-646 (address review C on #646 at c8208eb15): tbd start --as user-eb-addr-646 skipped (already claimed by codex@spud10); coordinator reports owner handed the PR to this session and codex idle since 06:07Z. Proceeding as sole committer on codex/news-chooser-states; coordinator to update delegate at sync.

2026-10-16 user-eb-addr-646 checkpoint: pushed 297702d15 (C1 pins), 0a51c1d4b (C9 rung_scale topic fills, Project hue 70), b61b48f7e (C4/C11 News rubric tooltips), bb4f0c97f (C2/C3/C5/C8/C10 chooser). Head bb4f0c97f. Next: release-impact, browser floor, focused suites, PR description, disposition reply, CI.

2026-10-16 user-eb-addr-646: review C on #646 addressed at head 7b925989f (fix commits 297702d15, 0a51c1d4b, b61b48f7e, bb4f0c97f, 7b925989f). Disposition reply https://github.com/jlevy/squares/pull/646#pullrequestreview-5551865539: C1-C5, C7-C11 fixed; C6 deferred to think-29vy. PR description updated (no cost receipt available; screenshots on claude/news-chooser-states-pr-images 9b3636e5). Hosted CI blocked: #651 merged v0.7.15 to main (26d8bb335), branch conflicts in release.py and five claim docs (merges-into-base red, no pull_request run). Needs coordinator re-cut (think-29vy); PR left draft.

Coordinator (session user-eb), 18:40Z: the owner handed #646 to this session in the afternoon ('review fully' and 'Follow up everything you can, and once things are reviewed, be sure you merge'). Review C was addressed at 7b925989f (10 fixed, C6 deferred to think-29vy). A follow-up review D is running. The integrator updates the branch from main and re-cuts its site edition in merge order. codex@spud10's claim is left in place; the work continues here under the owner's handover.

2026-10-16 user-eb-addr-646: review D on #646 addressed at head 689a9da80 (fix commits f13f385a1 D1, 9e8f284a0 D3, 68943e2f2 D5, 689a9da80 D2+D4); reply https://github.com/jlevy/squares/pull/646#pullrequestreview-5552401193. All five fixed; owner choices (two-row wrap, Project hue 70) recorded in the description. No merge with main, no re-cut; CI still blocked by the C6 conflict (think-29vy).

2026-10-16 user-eb-addr-646: review E on #646 addressed at head 42a286911 (b2c872012 E2, 42a286911 E1); reply https://github.com/jlevy/squares/pull/646#pullrequestreview-5552871067. No merge, no re-cut; CI still blocked by C6 (think-29vy).
