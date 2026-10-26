---
type: is
id: is-01m5wd6xy2vpj999dmpekj4820
title: News closes with a button to the Changelog
kind: task
status: in_progress
priority: 2
version: 3
delegate: claude-code@vm
labels: []
dependencies:
  - type: blocks
    target: is-01m5wd7re80yjz5wacnp5fqzy5
parent_id: is-01m5wd6833v6wx316fc361515a
hold: null
hold_until: null
created_at: 2026-10-26T15:28:07.105Z
updated_at: 2026-10-26T15:28:58.245Z
started_at: 2026-10-26T15:28:58.245Z
---
The News archive's closing action row has one button, Full changelog, which leaves for
`CHANGELOG.md` on GitHub (`render_changelog.render_news`, the `limit is None` branch).
It gains an on-site Changelog button; the GitHub button stays, since the file is the
generated root view.

With the detailed log on the site, the retained bookmarks follow it:

- `archived_news_targets` sends a below-floor entry's anchor to `changelog.html#<anchor>`
  rather than to GitHub's `CHANGELOG.md#<anchor>`.
- `legacy_news_anchors` (About) keeps sending `#changelog` and every entry anchor to
  wherever the view now lives.
- `site_documents.RECORD_PAGES[repo_links.CHANGELOG]` becomes `changelog.html`, so a
  Markdown link to `CHANGELOG.md` lands on the page that shows it.
- `check_published_site.changelog_checks` splits: the article roster and launch links
  stay a News check, and the full-history check, with its one `id="changelog"`, moves to
  `changelog.html`.
