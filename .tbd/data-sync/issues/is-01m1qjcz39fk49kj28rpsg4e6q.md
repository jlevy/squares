---
type: is
id: is-01m1qjcz39fk49kj28rpsg4e6q
title: "Certificate page: prose and headings lost the serif face and size in the Markdown refactor"
kind: bug
status: closed
priority: 0
version: 2
labels:
  - explainer
  - pr-79
dependencies: []
parent_id: is-01m1qgrj2q8kmrbqrgvkaksn87
created_at: 2026-09-05T01:19:48.327Z
updated_at: 2026-09-05T01:21:54.996Z
closed_at: 2026-09-05T01:21:54.995Z
close_reason: Commit 77c441c4, verified in the browser.
resolution: null
duplicate_of: null
---
Regression reported on the Markdown-rendered page: body text and h2s are sans and too small. The old HTML wrapped every section in kpress-prose, which carries the prose face and the normal size; the Markdown body renders outside it. Fix: the body wrapper carries kpress-prose; verify computed font family and size on prose, h2 and captions against the earlier page.
