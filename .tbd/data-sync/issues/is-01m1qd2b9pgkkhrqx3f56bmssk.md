---
type: is
id: is-01m1qd2b9pgkkhrqx3f56bmssk
title: "Certificate page: footnote text is too small"
kind: bug
status: closed
priority: 2
version: 2
labels:
  - explainer
  - pr-79
dependencies: []
parent_id: is-01m1q0p63s2evef5mhkyn16e41
created_at: 2026-09-04T23:46:37.484Z
updated_at: 2026-09-05T00:04:03.452Z
closed_at: 2026-09-05T00:04:03.451Z
close_reason: Commit 387c3508, verified in the browser.
resolution: null
duplicate_of: null
---
Review feedback on PR #79. The footnotes render at 14.4px against 18px prose: kpress's .kpress-footnotes sets font-size 0.9em, which compounds under the page's base. Set the footnotes to the small token size on the page and file the compounding upstream.
