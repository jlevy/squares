---
type: is
id: is-01m429d94k357kzb3jdng3tgp8
title: "Verify the review fixes on #315 (3172f287a, 03833707a) and #330 (9897ae38c)"
kind: task
status: closed
priority: 2
version: 4
labels: []
dependencies: []
parent_id: is-01m41d7edgm9wc99zdrkaa5ehy
created_at: 2026-10-04T01:45:43.826Z
updated_at: 2026-10-04T01:52:07.614Z
closed_at: 2026-10-04T01:52:07.614Z
close_reason: null
resolution: null
duplicate_of: null
---
Moderate-tier read-only check that each finding of think-rf21 and think-uer5 is resolved without regression.

## Notes

Done 2026-10-04: ten of eleven findings resolved, none regressed. Left: two docstrings still claimed no cross-table links (fixed on #315); a new defect, check_results stopping with a traceback when holders are unreadable (now reported as one problem, with a test); a test pinning T-031 as the only whole declaration (loosened); a comment's line break; and on #330 mask/mask-image wrongly counted as painting (removed, with a test). Known and left: braces inside CSS strings and ';' inside url() still confuse the colour check's parser, as the old one did; no served stylesheet has either.
