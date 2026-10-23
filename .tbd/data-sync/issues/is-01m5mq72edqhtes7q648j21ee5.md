---
type: is
id: is-01m5mq72edqhtes7q648j21ee5
title: "PR #751 A5: the packet does not date the 23 October fetch of the 232 exact forms"
kind: bug
status: closed
priority: 3
version: 3
delegate: c-review-thmc-1023
labels: []
dependencies: []
parent_id: is-01m5mq5vh52bze2e8j4eapg0bj
hold: null
hold_until: null
created_at: 2026-10-23T15:49:02.028Z
updated_at: 2026-10-23T16:18:07.630Z
started_at: 2026-10-23T15:49:18.254Z
closed_at: 2026-10-23T16:18:07.630Z
close_reason: "fixed in dbdb747e2 on claude/intake-2026-10-23-theorem-c-review (PR #751); disposition reply https://github.com/jlevy/squares/pull/751#issuecomment-6369458790; confirmed by the records tier and the affected tests at 0e9cfdc18"
resolution: null
duplicate_of: null
---
Review A, finding A5 (Low), PR #751, https://github.com/jlevy/squares/pull/751#issuecomment-6368595518. acquisition/sources.json:3 and declaration.json give retrieved_at_utc 2026-10-12T14:41Z only; README.md:342-360 (Retained Here) does not say the 232 forms were fetched on 23 October by Git blob from 31523f8. result-import.md:491.
