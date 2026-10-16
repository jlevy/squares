---
type: is
id: is-01m51bfq5cqtppb1ntyzk40kph
title: "PR #637 A2: four posted follow-ups misattribute or misdate supersessions (#506, #583, #575, #561)"
kind: bug
status: in_progress
priority: 1
version: 2
delegate: ecstatic-edison-replies-stack
labels: []
dependencies: []
parent_id: is-01m51bf8swfxxv0hbffaxdzk0r
hold: null
hold_until: null
created_at: 2026-10-16T03:18:28.268Z
updated_at: 2026-10-16T03:18:35.862Z
started_at: 2026-10-16T03:18:35.862Z
---
Medium. result-requests.yaml:5949 (#506 6206057024), :8325 (#583 6206060386), :8192 (#575 6206059896), #561 6206059300. #506 presents current rows as the superseding reports 'in the order they reached us', dates four to #627, omits Kevin Fang at 380/381; #583 dates all five to #627 (only 381 moved); #575 dates T-186 to #627 (registered 15 Oct by #612); #561 names #584 at 375 (Couzo's 13 Oct certificate was first). Fix: edit in place with a visible Edited line and note each on the entry, or post corrections recorded with corrects. https://github.com/jlevy/squares/pull/637#pullrequestreview-5542558537
