---
type: is
id: is-01m5jpfmjqpbx2geqhn5aqw43e
title: "Same-PR News articles: let a registering PR's News entry name itself as a pending delivery, dated by the merge stamp, so no follow-up is needed"
kind: task
status: open
priority: 1
version: 1
labels:
  - process
dependencies: []
parent_id: is-01m5jn336nm6erpp0ygedhgpva
created_at: 2026-10-22T20:57:45.303Z
updated_at: 2026-10-22T20:57:45.303Z
---
From the postmortem (think-jlra, docs/project/postmortems/postmortem-2026-10-22-results-without-news.md once #735 merges). The ordering constraint (render_changelog.validate needs a retained merged delivery and the merge's date) is the root cause; #735's gate is the backstop. Design like stamp_landed's re-date before merge.
