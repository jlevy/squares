---
type: is
id: is-01m3td1fcc3vnxmaqx07yg1jwb
title: Flowmark leaks reference-link placeholders inside Markdown footnotes
kind: bug
status: open
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-10-01T00:15:15.850Z
updated_at: 2026-10-01T00:21:21.279Z
---
Observed while preparing T-060 explainer: pinned flowmark-rs 0.4.0 transformed reference links inside footnotes into private-use hex placeholders, leaving broken hrefs. Paper workaround uses direct relative links in footnotes, with rendering regression guard. Reproduce with a minimal footnote/reference-link fixture, report upstream, and assess repository-wide affected docs before changing formatter pin. Do not rewrite archived sources.

## Notes

Publication workaround is in n11-optimality-article.md: 39 footnote links use direct source-relative destinations; actual-article renderer test refuses private-use placeholder code points and requires pinned source links. No formatter upgrade in this paper slice.
