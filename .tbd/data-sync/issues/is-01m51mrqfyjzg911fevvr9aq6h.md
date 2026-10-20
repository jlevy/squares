---
type: is
id: is-01m51mrqfyjzg911fevvr9aq6h
title: Diagnose local validation startup delays and stale gate marker
kind: bug
status: open
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-10-10-contributor-profiles.md
delegate: null
labels: []
dependencies: []
parent_id: is-01m4kvnfe7f9nak96hc7bgdwer
hold: null
hold_until: null
created_at: 2026-10-16T06:00:40.694Z
updated_at: 2026-10-19T07:39:45.163Z
started_at: 2026-10-16T06:03:55.149Z
---
Two local pre-push runs at implementation 77fe330dd passed all 68 prerequisites but timed out after 900 seconds of behavioral tests. A verified stale empty gate marker was removed; ten-worker execution was restored, but the retry also timed out. Serial reproduction completed: six of eight selectors passed unchanged. Remaining failures are a nested collection exceeding 30 seconds and a static paragraph longest-task control measuring 402 ms against 300 ms. Three signal/readiness tests, Atlas navigation, representative result columns and the suite-plugin probe passed. Original first-run F833/F1284 identities remain unknown. Investigate marker ownership/recovery and host contention; no product regression or single cause has been established. No source or timeout changes were made. All 31 standard hosted checks pass on final documentation head e1f921bf0. Receipts are under external scratch contributor-profiles-01a126ff/tmp, including the two push logs, profiles-final-merge-artifacts, and serial-process-repro and serial-browser-repro logs.

## Notes

On 2026-10-19, the review integration at ee52c65fd passed all 68 pre-push prerequisites, then failed snapshot-cap and result-page byte assertions, plus native-frontier timing at 1280-dark (LCP 1124 ms, longest task 588 ms, blocking 888 ms). The run was interrupted after retaining failures. It is not a pass or a timeout-only outcome. Snapshot and page repairs are tracked by think-iyao and think-jhst; subsequent merge 134216084 changes only the incoming policy record.

Astra reran the same four native-frontier scenarios serially with PACK_JOBS=1 and unchanged budgets: one failed and three passed in 339.59 seconds. This time 390-light failed at 10164/752/3876 ms (LCP/longest/blocking); 390-dark passed at 404/152/102, 1280-light at 388/157/107, and 1280-dark at 392/161/111. All seven executed navigations had 272 readable math expressions and none unreadable; 390-light without JavaScript was not reached. Budgets remain 4000/300/600 ms. The original observer attributed about 580 ms to atlas forced layout, but the serial failure had distributed work. No exact-main or idle-host control exists. Unchanged scripts do not exclude a rendered-markup regression, and passing other contexts does not clear these failures. Hosted acceptance with unchanged budgets remains pending.

Retained evidence: /Volumes/spud-ext1/agent-evidence/squares-profiles-review-20261019/timing-review/ (serial.log, serial.xml, per-navigation JSON and traces). Continue with a measured same-host main-versus-branch control if hosted results or further evidence warrant it. No causal attribution is established.
