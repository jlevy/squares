---
type: is
id: is-01m52xzf9693npacscf5ght83b
title: "PR #646 C6: re-cut the site edition at merge after the v0.7.15 collision"
kind: task
status: closed
priority: 2
version: 7
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: lane-645
labels: []
dependencies: []
parent_id: is-01m51hjc9mv43jqr39c4zm038d
child_order_hints:
  - is-01m59q4nyd0g3g9brgy7dxtes0
  - is-01m5aaxv6g0n2c0kgz9r571ndh
hold: null
hold_until: null
created_at: 2026-10-16T18:00:53.286Z
updated_at: 2026-10-19T23:01:43.574Z
started_at: 2026-10-16T18:01:00.338Z
closed_at: 2026-10-19T23:01:43.574Z
close_reason: "Landed in PR #646 (merged 028bc72ec), site v0.7.35 deployed 22:53Z 19 Oct and verified 4708/4708 (Pages run 39337466599)."
resolution: null
duplicate_of: null
---
Review C finding C6 (Medium) on https://github.com/jlevy/squares/pull/646 (review https://github.com/jlevy/squares/pull/646#pullrequestreview-5550645187). Several open PRs cut site v0.7.15; #651 merged its v0.7.15 (PUBLICATION_REVISION 46ae34f9) into main at 26d8bb335, so codex/news-chooser-states now conflicts with main in packing/src/sqpack/release.py and the five n11 claim documents, and hosted CI cannot run (merges-into-base red at 7b925989f). Per the coordinator, the cut stays as is during addressing; the coordinator re-cuts at merge in merge order: merge origin/main (merge commit), resolve release.py and the claim documents to main's side dropping this branch's v0.7.15 entries, run devtools.cut_release with the next free site version (v0.7.16 or later), rewrite the claim-document ReleaseNoPublicChange reason for the new link revision, keep the papers' ReleaseNoPublicChange record (paths: rating-tooltips.js, render_changelog.py, render_overview.py, site-nav.css), set README and the PR title/body, re-run check_release_impact and the release tests, and say in the PR why the version changed. Waits on the merge order across the open site-edition PRs.

## Notes

2026-10-16 user-eb-addr-646: created under think-slt2 for review C finding C6; claimed by user-eb-addr-646 only because the brief says to claim beads I create. The work is the coordinator's re-cut at merge; reassign the delegate when it starts.
