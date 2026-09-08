---
type: is
id: is-01m1tqpkm0hkfa1b9km7s0yq2c
title: "A5: 'Condition 5 says every event cell carries mass at least 1' lacks the reachability qualifier"
kind: bug
status: in_progress
priority: 2
version: 2
labels:
  - review-claude
dependencies: []
parent_id: is-01m1tqpgrh5ym0r6e5apbke7p8
created_at: 2026-09-06T06:50:10.430Z
updated_at: 2026-09-06T06:50:19.033Z
---
explainer-article.md, 'Every Placement Covers Mass at Least One'. Only cells the square's centre can reach inside the container are checked; cells beyond carry as little as 0 (Figure 5's caption says so). Fix: 'every event cell the square's centre can reach without leaving the container, at every net direction, carries mass at least 1.'
