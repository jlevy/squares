---
type: is
id: is-01m4mycgjrz4e4w2trtbfz54eh
title: "PR #406 A5: 4 MiB metadata ceiling refuses long branches with the wrong remedy"
kind: bug
status: closed
priority: 2
version: 3
delegate: claude-code@spud10
labels: []
dependencies: []
parent_id: is-01m4mybh5kcffr8zqzm2ajg86e
hold: null
hold_until: null
created_at: 2026-10-11T07:38:38.550Z
updated_at: 2026-10-11T18:58:29.513Z
started_at: 2026-10-11T07:39:13.243Z
closed_at: 2026-10-11T18:58:29.512Z
close_reason: "fixed in 0a4a69d5e: 64 MiB per-query bound and a remedy per refusal kind. Disposition: https://github.com/jlevy/squares/pull/406#issuecomment-6112530517"
resolution: null
duplicate_of: null
---
Medium. check_added_blobs.py:80-81; development.md:1856-1857. log --raw for base..main is 7.14 MiB; #469 2.69 MiB. Review A: https://github.com/jlevy/squares/pull/406#pullrequestreview-5482287656 (PR #406).
