---
type: is
id: is-01m5pcb1tm1x4jd4xdfwwftb0h
title: "Stage 7 for #770: post the 14 tracking-issue acknowledgements (#772-#780, #782-#786) and the #603 and #294 notes after the deploy; write their reply records"
kind: task
status: closed
priority: 1
version: 4
delegate: c-post-770-1024
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T07:17:26.996Z
updated_at: 2026-10-24T07:33:26.968Z
started_at: 2026-10-24T07:17:32.885Z
closed_at: 2026-10-24T07:33:26.967Z
close_reason: "16 comments posted 2026-10-24 after deploy 40073374851 (edition v0.9.2-d7f02b): acks on #772-#780, #782-#786; follow-ups on #603 (6381479105) and #294 (6381479220). Reply-record patch scratchpad/post770/requests.patch handed to think-9i18 (the stage-7 records PR) to land."
resolution: null
duplicate_of: null
---

## Notes

2026-10-24 lane c-post-770-1024 (stage 7 for #770):
- Deploy: Pages run 40073374851 (Certificate page) conclusion success; every job success (deploy, verify-deployment, publish, pages-required included) except candidate-infographics and startup-timing, skipped by their conditions. squaremath.org serves v0.9.2-d7f02b = release.PUBLICATION_EDITION at main 11d0ab06b.
- Profiles: kevin-fang.html#records lists T-163; hiroaki-hosono.html#records lists T-073 and T-080; 0 of 76 profile pages plus the index carry 'Review pending'.
- Posted (16):
  - #772 https://github.com/jlevy/squares/issues/772#issuecomment-6381477449
  - #773 https://github.com/jlevy/squares/issues/773#issuecomment-6381477713
  - #774 https://github.com/jlevy/squares/issues/774#issuecomment-6381477862
  - #775 https://github.com/jlevy/squares/issues/775#issuecomment-6381477972
  - #776 https://github.com/jlevy/squares/issues/776#issuecomment-6381478097
  - #777 https://github.com/jlevy/squares/issues/777#issuecomment-6381478206
  - #778 https://github.com/jlevy/squares/issues/778#issuecomment-6381478328
  - #779 https://github.com/jlevy/squares/issues/779#issuecomment-6381478445
  - #780 https://github.com/jlevy/squares/issues/780#issuecomment-6381478547
  - #782 https://github.com/jlevy/squares/issues/782#issuecomment-6381478640
  - #783 https://github.com/jlevy/squares/issues/783#issuecomment-6381478743
  - #784 https://github.com/jlevy/squares/issues/784#issuecomment-6381478818
  - #785 https://github.com/jlevy/squares/issues/785#issuecomment-6381478925
  - #786 https://github.com/jlevy/squares/issues/786#issuecomment-6381479019
  - #603 https://github.com/jlevy/squares/issues/603#issuecomment-6381479105
  - #294 https://github.com/jlevy/squares/issues/294#issuecomment-6381479220
- Held: none. #603 posted with two changes from the draft: #770 linked, and T-236's build price corrected from 'about 2 to 3' to 'about 1.5 to 3 CPU-hours' to match the record (results.yaml T-163, T-236's page). deficiency_family on main: smallest k=15..68,70..75, tied 69,76, Ryu 1.3 smaller at every k from 77 to 399. #781 still open at post time.
- Patch: /tmp/claude-0/-home-user-squares/f8504540-2b5a-5f78-8968-eb4ffa4c4b64/scratchpad/post770/requests.patch against main 11d0ab06b (result-requests.yaml, +248/-14); git apply --check ok; on a scratch copy check_requests rc=0 and --report shows Reply due: no on all 16.
