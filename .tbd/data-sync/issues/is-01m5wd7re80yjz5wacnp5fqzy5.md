---
type: is
id: is-01m5wd7re80yjz5wacnp5fqzy5
title: "Closeout: validation tiers, pull request, changelog entry"
kind: task
status: in_progress
priority: 2
version: 2
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m5wd6833v6wx316fc361515a
hold: null
hold_until: null
created_at: 2026-10-26T15:28:34.248Z
updated_at: 2026-10-26T15:29:00.316Z
started_at: 2026-10-26T15:29:00.316Z
---
The standard release process for a site change.

- `packing-validate --records` before touching the URL registry, `--edit` while editing,
  and the affected tests directly: `test_site_navigation.py`, `test_overview.py`,
  `test_home_recent.py`, `test_changelog.py`, `test_check_published_site.py`,
  `test_site_documents.py`, `test_measure_news_page.py`, `packages/workbench/tests/test_site_nav.py`.
- `devtools.check_published_site --local OUT --partial --producer overview` on a built
  tree, and the browser load and readability protocol for the new page.
- `packing-validate --fast` is the pull-request surface; the full gate closes the session.
- The pull request leads with what the branch cost (OR-9).
- After the merge, record the contribution in `packing/site-changelog.yaml` and run
  `devtools.render_changelog`. The site is never a release-impact candidate, so no cut.
