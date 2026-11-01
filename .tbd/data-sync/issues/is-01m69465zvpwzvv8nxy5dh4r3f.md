---
type: is
id: is-01m69465zvpwzvv8nxy5dh4r3f
title: "check_requests --report marks an issue closeable while its record carries blocked: owner-decision (seen on #846, 31 Oct)"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
created_at: 2026-10-31T14:00:33.019Z
updated_at: 2026-10-31T14:00:33.019Z
---
On 2026-10-31 check_requests --report listed #846 as closeable although its requests entry is blocked: owner-decision and its close_when needs the owner's answer (think-ikku). Lane L2 correctly kept #846 open by hand. The report should not mark an issue closeable while a blocked entry stands (or while close_when names an unmet owner decision); add a test.
