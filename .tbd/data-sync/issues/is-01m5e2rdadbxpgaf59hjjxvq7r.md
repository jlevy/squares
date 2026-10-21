---
type: is
id: is-01m5e2rdadbxpgaf59hjjxvq7r
title: Repair recurring disk cleanup coverage and persist physical capacity baselines
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
created_at: 2026-10-21T01:56:03.520Z
updated_at: 2026-10-21T01:56:03.520Z
---
Oct20 disk-growth diagnosis found40 recurring runs inventory-only and all767 ext1 artifact roots unattempted, despite ~42GiB free at start. Internal-disk pressure blocked metadata surveys whose outputs could use external scratch; later ext1 guards perpetuated the hold. Also never describe Trash as empty when inventory is denied and trash -l silently returns empty. Add bounded progress per volume, persistent df/category baselines, explicit aging/coverage alerts, and truthful inaccessible Trash state. Evidence: /Volumes/spud-ext2/agent-evidence/spud-ext1-growth-20261020/{SUMMARY.json,review.txt,REVIEW.txt}. Existing cleanup authority and notification intent must be preserved.
