---
type: is
id: is-01m5wd6x8apd2yfvdpcp652dvd
title: A Changelog page on this site
kind: task
status: in_progress
priority: 1
version: 4
delegate: claude-code@vm
labels: []
dependencies:
  - type: blocks
    target: is-01m5wd6xy2vpj999dmpekj4820
  - type: blocks
    target: is-01m5wd7re80yjz5wacnp5fqzy5
parent_id: is-01m5wd6833v6wx316fc361515a
hold: null
hold_until: null
created_at: 2026-10-26T15:28:06.410Z
updated_at: 2026-10-26T15:28:57.675Z
started_at: 2026-10-26T15:28:57.674Z
---
`changelog.html`: the retained project history, every entry rather than the S3+ stories
News shows, with the GitHub issue and pull-request links each entry already carries.

`render_changelog.render_markdown(document, destination="site")` already writes exactly
this view, with `id="changelog"`, a date heading per day and an anchor per entry, and
nothing on the site renders it yet.

- A `changelog-article.md` template and `changelog_page()` in `render_overview.py`,
  registered in `PAGES` and `SITE_PAGES`.
- The `#changelog` bookmark moves off `news.html`'s title to this page.
- Register the URL: `devtools.site_urls --write`, which rewrites
  `docs/project/site-urls.md`, then `--check --history-ref origin/main`. New rows use
  `REGISTRATION_DATE`.
- Measure the page against the 600,000-byte page budget; a path exception is a reviewed
  edit with measured evidence, so prefer staying under it.
