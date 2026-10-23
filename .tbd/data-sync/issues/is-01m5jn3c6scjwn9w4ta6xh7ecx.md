---
type: is
id: is-01m5jn3c6scjwn9w4ta6xh7ecx
title: "Home page 'Recently added' section: every result, house change and beyond-horizon row of the last seven days (owner request)"
kind: feature
status: open
priority: 1
version: 4
labels:
  - site
dependencies: []
created_at: 2026-10-22T20:33:34.936Z
updated_at: 2026-10-23T02:44:14.042Z
---
Owner, 22 Oct: 'It should be clear if you come to the site and see all the things that have recently merged now.' c-lane-home-recent-1022, branch claude/home-recently-added.

## Notes

2026-10-23 00:30Z (c-lane-home-recent-1022): Recently Added pushed on #736 (https://github.com/jlevy/squares/pull/736), commit 7f59cf375, head d2a5b5ce9.
- Home page, above News: one disclosure a day over the results page's seven days (15-22 Oct), newest open. Each day lists its results at any significance (added_entry, linked to results.html#t-NNN, plus the day's table link), its house best packing moves (upper_bound_houses.ADOPTED + adopted_on; each checked against the case record's verified upper-bound holder) and its dated beyond-horizon rows by source (source-coverage.yaml, day = source `reviewed`; count, span, credit, since-superseded count; link to the packet README on GitHub).
- Today: 45 results, 61 counts' house moves on 7 days, 876 rows from 11 sources. 23,651 bytes (test budget 40,000); index.html 570,482 of 1,300,000.
- Reuses results.css and the results renderer; results.html is byte-identical apart from the stylesheet hash.
- No site page lists beyond-horizon rows. Proposed smallest page: a "Beyond n = 324" table on atlas.html under the Frontier Survey, generated from the current rows.
- Tests: tests/test_home_recent.py (8), test_recently_added_reads_as_the_results_pages_days_with_and_without_scripts (1280/390, light/dark, no-JS).

2026-10-23 (c-lane-home-recent-1022): review A fixes at e07648d0e. Houses and rows now dated by the day main first held them via packing/frontier/landings.yaml (schema Landings/v1), written by stamp_landed at the merge step (branch_additions) and backfilled from main's first-parent history; no render reads Git (OR-18). One window for all kinds (arrival_reference); intro names the days shown (16-23 Oct). Render no longer reads upper_bound_houses (removed from RENDER_INPUTS and pages.yml). Edit tier passed at 52ff7795a.

2026-10-23 02:40Z (c-lane-home-recent-1022): #736 at 2c50762d4 (main fcf2f96a5 #730 merged; release.py conflict resolved, re-pinned; #730's 11 row sources backfilled to 23 Oct). Hosted 31/31 pass, mergeable; edit tier passed. Recently Added 16-23 Oct: 42 results, 58 house counts, 1,195 rows from 22 sources; 27,146 bytes.
