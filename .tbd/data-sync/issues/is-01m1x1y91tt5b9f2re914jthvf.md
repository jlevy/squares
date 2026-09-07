---
type: is
id: is-01m1x1y91tt5b9f2re914jthvf
title: Plan integration of hybrid n11 research with Agenda 027
kind: task
status: in_progress
priority: 1
version: 7
labels: []
dependencies: []
created_at: 2026-09-07T04:27:36.365Z
updated_at: 2026-09-07T05:26:19.436Z
---
Publish the consolidated strategic review as a stacked PR. Review and independent audits complete. Final commit 73aa747a contains a three-file diff from PR107 at 81e8a615: one review and two navigation entries. It incorporates the source closeout already in PR107, uses final X-017, and reviews the later PR105 priority amendment at 6d8b2b38 without changing its source records. H-110 and the new short conditional-compatibility assessment retain source ownership; H-107 is deferred under think-7fec. All new scientific IDs remain placeholders. Pre-push checks run in an isolated checkout under attic/n11-hybrid-review-publication to keep logs and fixtures in the attic without polluting source scans. Next: push, create PR against codex/research-agenda-exploration, observe matching fast and deferred CI, close and sync. Original spike instruments remain unpublished in stash 8f6592818f17f1cea83a617bb11ed6ffd6e112a6; mathematical arguments needed for incorporation are included in the review.

## Notes

PR108 is open at https://github.com/jlevy/squares/pull/108, head 73aa747a, targeting PR107 at 81e8a615. The final diff is exactly the review plus SYNOPSIS and document-map navigation. Pre-push checks passed all 45 selected steps in 74.02s; 604 behavioral tests passed, 3 deselected. Fast run 34086743120 and deferred run 34086743130 are in progress on the same PR merge revision. Source review refreshed through PR105 6d8b2b38: H107 deferred; H110 plus the short conditional-compatibility assessment remain source-owned. All new labels remain placeholders. Separate attic-scan follow-up recorded as think-a98k. All publication files and logs are in attic/n11-hybrid-review-publication. Next: observe final CI, replace pending PR-body lines with exact outcomes, close and sync.
