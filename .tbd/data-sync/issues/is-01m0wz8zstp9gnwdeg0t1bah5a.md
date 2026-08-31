---
type: is
id: is-01m0wz8zstp9gnwdeg0t1bah5a
title: Copied no-regression count in SYNOPSIS drifted (98 vs 106)
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m0wy9s97fwegw5kqrge2p8sy
created_at: 2026-08-25T17:25:19.802Z
updated_at: 2026-08-25T17:49:31.941Z
closed_at: 2026-08-25T17:49:31.941Z
close_reason: Fixed on the PR 33 branch; see review-2026-08-25-tutorial-soundness-iteration-2.md and defects D-320..D-328. Full gate green.
resolution: null
duplicate_of: null
---
SYNOPSIS's defect narrative restated the no-regression-fix count by hand (ninety-eight) while the generated defects.md counted 106, directly after a sentence promising the surrounding claims cannot drift. Recurrence of D-028. Fixed by removing the copied number and deferring to the computed count. Registered as D-328.
