---
type: is
id: is-01m5wd6wjc69grgr1c0sqnkep4
title: "Site navigation: a Project menu over Overview, News and Changelog"
kind: task
status: in_progress
priority: 1
version: 4
delegate: claude-code@vm
labels: []
dependencies:
  - type: blocks
    target: is-01m5wd6x8apd2yfvdpcp652dvd
  - type: blocks
    target: is-01m5wd7re80yjz5wacnp5fqzy5
parent_id: is-01m5wd6833v6wx316fc361515a
hold: null
hold_until: null
created_at: 2026-10-26T15:28:05.708Z
updated_at: 2026-10-26T15:28:57.215Z
started_at: 2026-10-26T15:28:57.215Z
---
`devtools/site_navigation.py` grows a `project` group, first in `NAVIGATION`, with no
path of its own (a group with children never has one, which
`test_menu_destinations_supply_canonical_titles_and_categories_have_no_urls` holds) and
three children: Overview `./`, News `news.html`, Changelog `changelog.html`.

- `_LEGACY_PATHS` gains `changelog`.
- `_PARENTS` gains `news.html` and `changelog.html` under `("project",)`. The homepage
  keeps no parents, so it keeps no breadcrumb trail; `_SELF_NAMED` already keeps its
  title The Squares Project while its menu label is Overview.
- `navigation_links` marks a group current when the current page is the group's own or
  any child's, not only when `_PARENTS` names it, so Project reads as current on the
  homepage although the homepage has no trail.

Tests to move with it: `test_site_navigation.py` (the per-group destination test, the
canonical-title test's homepage exception), `test_overview.py`'s menu-label test (News
now carries a breadcrumb; the homepage still does not), and the Learn/Results group
tests that enumerate the bar.
