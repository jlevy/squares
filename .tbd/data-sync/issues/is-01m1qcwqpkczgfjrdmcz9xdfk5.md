---
type: is
id: is-01m1qcwqpkczgfjrdmcz9xdfk5
title: "Certificate page: citations as kpress footnotes, not parentheticals"
kind: task
status: closed
priority: 2
version: 2
labels:
  - explainer
  - pr-79
  - kpress
dependencies: []
parent_id: is-01m1q0p63s2evef5mhkyn16e41
created_at: 2026-09-04T23:43:33.586Z
updated_at: 2026-09-04T23:45:37.263Z
closed_at: 2026-09-04T23:45:37.262Z
close_reason: Commit 4f504ed9.
resolution: null
duplicate_of: null
---
Review feedback on PR #79. Stromquist 2003, Friedman's survey and the Trump packing's source become numbered footnotes in kpress's own markup (sup.kpress-footnote-ref, section.kpress-footnotes with backrefs), with the parenthetical and inline-link citations removed. Hover previews are kpress's runtime behaviour, which the self-contained page does not load.
