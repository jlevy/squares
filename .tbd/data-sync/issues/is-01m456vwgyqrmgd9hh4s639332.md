---
type: is
id: is-01m456vwgyqrmgd9hh4s639332
title: "Homepage: cards for the essential external sites (Kingbird / Ellsworth's Squares in Squares, Friedman's Packing Center, evand's Square Packing Atlas, UnitSquare, others the register cites) beside the GitHub projects"
kind: task
status: closed
priority: 1
version: 4
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m44qz0rxvkakmyqaj7qdgagv
hold: null
hold_until: null
created_at: 2026-10-05T04:58:59.998Z
updated_at: 2026-10-05T07:19:55.327Z
started_at: 2026-10-05T04:59:39.795Z
closed_at: 2026-10-05T07:19:55.327Z
close_reason: "Done in jlevy/squares#353 / #359 (merged 2026-10-05)"
resolution: null
duplicate_of: null
---

## Notes

2026-10-05 lane `sites` (worktree squares-lanes/sites, branch claude/ecstatic-pascal-pothtx-sites), commit b4139662d.

Done: Other Square Packing Projects leads with three catalogue cards (CATALOGUE_SITES): Ellsworth's Squares in Squares ([Kingbird], kingbird.myphotos.cc, tally T-088/T-089 via SOURCE_VENUES venue "Kingbird"), Friedman's original Squares in Squares page (Wayback 20230530194618 address the catalogue header links), Evan Daniel's Square Packing Atlas. OTHER_SITES ranked with the GitHub projects: Burns's and Massaccesi's n=17 posts ([Burns–Massaccesi n17], T-015/T-016 on both), Wang–Li Zenodo 23038546 (T-061), UnitSquare hmbelvedere.com (no registered result). Sites join the results-page Project preset. Globe mark (WEB_MARK) for hosts with no saved favicon: the proxy refuses these hosts, none could be fetched.

Tests: every source-coverage source has a card; every website card URL is cited by the record (coverage, bibliography, case records, retained captures); Kingbird leads and counts exactly the venue's results.

Open: paper-design.md (not committed per lane rule) needs the matching prose; patch drafted at scratchpad lane-sites/paper-design-website-cards.patch. Excluded: MinMax Arena (n=26 audit catalogue checked, no result), journals/papers (Papers page). Noticed: chelokot/square-packing-archive is cited by two registered results but is not in source-coverage, so it has no card.

Validation: targeted tests (test_overview, test_site_project_tallies, site hover/math/wide/head/filters/text-token, check_published_site) 423 passed; packing-validate --records 44/44 steps passed; reachable_tests --since HEAD~1 -n 2: 3928 passed, 3 failed, none touching this change (test_audit_ds7_lower_bounds n=17 exact_form 18641771/4000000 vs the test's 116511/25000, from cd1b88195's n-017 record; two fixed_core_packet reaping tests, "worker process group remained alive after SIGKILL", environmental). Not closed: awaiting parent review and the paper-design.md prose.
