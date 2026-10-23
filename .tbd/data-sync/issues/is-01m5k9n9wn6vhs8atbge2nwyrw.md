---
type: is
id: is-01m5k9n9wn6vhs8atbge2nwyrw
title: "Decide: is a watched certificate its author withdrew from an issue a report? (1851c2c at nine counts, #719/#732)"
kind: task
status: in_progress
priority: 2
version: 4
delegate: c-answers-1023
labels:
  - decision
  - result-import
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-23T02:32:53.909Z
updated_at: 2026-10-23T09:40:45.384Z
started_at: 2026-10-23T07:54:20.661Z
---
Owner decision raised by the #732 import (think-0gp6, lane c-lane-732-import-1023), 23 October 2026.

**The question.** Is a certificate in a watched repository a report of its own when its author withdrew it from the issue that first claimed it, and his later release claims a lower side at the same count?

**Where it arises.** Mykhailo Polkovskyi's 1851c2c (2026-10-22T05:29:48Z) holds certificates/n-N.cert at 411, 451, 494, 495, 539, 540, 583, 587, 632 and 683. Issue #719 opened claiming them, and its 06:05:31Z edit withdrew them; #722 pinned them by digest and imported none "until he answers" (mishapolk-issue719-2026-10-22 README, Not Imported). His answer on #719 (issuecomment-6350348588) claims the ten counts "as part of" #732, whose certificates at 17cc220 are new 8a488a1 files at nine of them and the 1851c2c file itself at 539.

**What the walk does.** The report-order walk of #732 (campaign/issue-intake/upper-bounds-issue732-20261023), which counts every certificate in the watched repository from its first commit, records the 1851c2c file at the nine counts other than 539: each is below every earlier report at its count. #732's 8a488a1 side is recorded after it at all nine and is the current row. The walk holds the nine 1851c2c files back from a row (beyond_horizon_replay class `withdrawn`).

**The answer either way.**
- Not reports (recommended: the author withdrew them and claims the lower files): nothing changes. No verdict rests on them; #732's rows stand.
- Reports: nine superseded rows are written for 1851c2c, each superseded on entry by #732's row, from a packet that retains or derives the nine files at 1851c2c (the #719 packet pins them by digest at 12fc466).

blocked_on: owner

## Notes

2026-10-23 coord-intake-1023: OWNER DECISION (in conversation, 23 October): a watched certificate its author withdrew from an issue, claiming a lower file later, is NOT a report. Nothing changes in the rows: #732's rows stand. The #732 walk's 'withdrawn' hold becomes the settled disposition; its text should name this answer rather than an open question (rides the next records PR after #742).

2026-10-23 c-answers-1023 (PR https://github.com/jlevy/squares/pull/754, branch claude/intake-2026-10-23-owner-answers).

**Done.** The #732 walk's `withdrawn` hold is now the settled disposition: `Held.answer`
states the owner's answer (`beyond_horizon_replay.WITHDRAWN_ANSWER`: "a watched certificate
its author withdrew from an issue, claiming a lower file later, is not a report"), the
class text in HELD_CLASSES names it, the walk's sources.yaml note for 1851c2c says the walk
keeps its 9 files (411, 451, 494, 495, 540, 583, 587, 632, 683) out of the record by that
answer, and `held-dependents` lists them under `settled` rather than as an answer to come.
No verdict rests on them and `refusal_flips(withdrawn)` is empty; no row changes: #732's 77
rows stand. The runbook (Several Reports at One Count) and the frontier README state the
rule; #732's and #719's requests entries and packet READMEs name the answer.

**Follow-ups drafted** on think-temp (the #719 and #732 drafts both carry this answer); none
posted.
