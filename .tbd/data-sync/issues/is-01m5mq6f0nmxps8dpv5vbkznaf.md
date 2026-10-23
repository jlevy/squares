---
type: is
id: is-01m5mq6f0nmxps8dpv5vbkznaf
title: "PR #751 A1: records plan C3 on the review lane's own checker and retire the gradec.py replay"
kind: bug
status: closed
priority: 2
version: 3
delegate: c-review-thmc-1023
labels: []
dependencies: []
parent_id: is-01m5mq5vh52bze2e8j4eapg0bj
hold: null
hold_until: null
created_at: 2026-10-23T15:48:42.133Z
updated_at: 2026-10-23T16:18:02.628Z
started_at: 2026-10-23T15:49:14.645Z
closed_at: 2026-10-23T16:18:02.627Z
close_reason: "fixed in 0f9cf833f on claude/intake-2026-10-23-theorem-c-review (PR #751); disposition reply https://github.com/jlevy/squares/pull/751#issuecomment-6369458790; confirmed by the records tier and the affected tests at 0e9cfdc18"
resolution: null
duplicate_of: null
---
Review A, finding A1 (Medium), PR #751, https://github.com/jlevy/squares/pull/751#issuecomment-6368595518. Where: packing/campaign/result-requests.yaml:7748; docs/project/reviews/review-2026-10-23-evand-grade-c-theorem-c.md:477-478; the PR body's Limits; think-7scz's drafted E-evand-gradec-local-minima-233-review-check ('the first derives V3/C3') and its note that the re-run 'reaches no rung'. result-import.md Stage 4 (lines 595-619) accepts the source's checker, or a first-party one whose soundness has been adversarially reviewed. Coordinator's call: C3 waits on a separate replay lane (the gradec.py re-run, about 10.6 CPU-hours), with check_theorem_c.py as the second route, as at T-225 and T-229.
