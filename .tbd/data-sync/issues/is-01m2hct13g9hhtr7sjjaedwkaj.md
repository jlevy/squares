---
type: is
id: is-01m2hct13g9hhtr7sjjaedwkaj
title: "PR #125 review D28: the PR description misstates evidence and scope"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m2hb401yy3ph99cfn5mhpcv4
created_at: 2026-09-15T02:02:20.143Z
updated_at: 2026-09-15T02:02:20.143Z
---
Review source: PR #125 review F31 (Medium); triage row D28.

The PR #125 description, which becomes the merge record, misstates evidence and scope: "3,975 resulting packings were re-verified out of process by the exact oracle" (verify-archive runs verify_packing at float_sign(1e-9), assurance numerically-checked; 4,419 poses_checked derivable); cites H-135..H-138 and exp-134..exp-138 (now H-201..H-205, exp-201..exp-206) and "four hypotheses, five experiments" (five and six); "excluded from the lint floor" (included); capture "deferred" (capture_video.py exists); "348 E501s" (0); "15 retained papers" (87); "2.9 MB" (4.4 MB); stale head. Lanes do not edit PRs: the corrected body is written to the coordinator's attic/reviews/pr-bodies/pr125.md.
