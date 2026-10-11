---
type: is
id: is-01m3v4zvg2qhsk3amx5abyv6j1
title: "Results table: restore the red star on new best results"
kind: bug
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T07:13:48.542Z
updated_at: 2026-10-01T16:04:21.878Z
closed_at: 2026-10-01T16:04:21.877Z
close_reason: "0d64a22d1 and 843151ad1, merged with jlevy/squares#264 (main fe6399451): the star follows the atlas rule (12 results, the same 27 cases) and never wraps alone."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: we seem to have lost the red star for new best results on the results table. The star marked a result that is new and the current best for its case (as the atlas popover still does with its star and 'new result'); find where the table lost it (the Recent Results one-table rewrite 69050befd, the shared table component, or the row-popover change dad5a3bc8), restore it on Recent Results and on all-results.html from the same rule the atlas uses, and pin it in a test.
