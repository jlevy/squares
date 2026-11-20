---
type: is
id: is-01m7vzh60yxt0yczy9rt2t4gfx
title: "Intake 2026-11-20 lane c6-records: record eight position-superseded follow-ups (#366, #914, #929, #931, #943, #944, #945, #985), draft #1018 stage 7 reply, read and record the #1012 comment"
kind: task
status: in_progress
priority: 2
version: 4
delegate: c6-records
labels: []
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
hold: null
hold_until: null
created_at: 2026-11-20T08:00:26.654Z
updated_at: 2026-11-20T08:56:33.797Z
started_at: 2026-11-20T08:00:30.189Z
---
Lane c6-records of the 2026-11-20 intake pass (coordinator bold-ritchie-coord1120). One draft PR on claude/intake-2026-11-20-records-followups: (1) record the eight follow-ups the coordinator posted from main at 07:54Z as kind: follow-up replies naming only the superseded result(s), no corrects; (2) draft the #1018 stage 7 final reply to the scratchpad, not posted; (3) read #1012 issuecomment-6972165182 and record it per result-import.md (bead think-wvr8).

## Notes

## Progress (2026-11-20, lane c6-records)

Branch claude/intake-2026-11-20-records-followups (worktree in the scratchpad, resources hardlinked from the coordinator checkout for disk), fast-forwarded to origin/main 935e79c36.

- fabbd4d3e records: the eight follow-ups of 07:54Z (#366 issuecomment-7033770691, #914 -7033771041, #929 -7033771310, #931 -7033771630, #943 -7033771960, #944 -7033772271, #945 -7033772565, #985 -7033772930) recorded as kind: follow-up, reported = only the superseded ids (T-107/T-108/T-109; T-269, T-277, T-279, T-287, T-288, T-289, T-302), V3/C3 confirmed superseded, no corrects; successors (T-142/T-132/T-143; T-314..T-326) in notes as context; read_through unchanged.
- Same commit: #1012 de Winter comment issuecomment-6972165182 read: read_through 2026-11-18T07:33:46Z; attaches the exact Witness/v2 at 109 (Kodaj's packing, side 547464479047171949843/50000000000000000000, s(109) <= 10.949289580944), import still queued on think-wvr8, nothing retained; asks credit "as your sources support" (Kodaj, Prabhat, Fonseca's pinwheel 6 Nov, Samanyu-dev per #958); withdraws 270 (his #1022 is below both Kaggle sides) -> n270-kaggle queued: false; blocked: author removed (test count author 2 -> 1). Coordinator: remove the blocked:author label on #1012 after merge.
- 3bc2051e1 release: no-public-change record 2026-11-20-c6-records-1120-followups.yaml (methods survey 43 files byte-identical vs 935e79c36). release_pin --check: pin is last data commit; stamp_landed: nothing.
- #1018 stage 7 draft (not posted): scratchpad c6-1018-reply.md; names T-327, T-216, T-180, E-de-winter-1018-n108-report, E-de-winter-1018-n108-sqverify-fast-replay.
- intake_sweep before/after: the 8 "owes a follow-up" rows, the 8 "reply missing" rows, the #1012 unread-comment row and the n270-kaggle queued row are gone; one new row: #1012 carries blocked:author the record no longer names (clears when the label is removed after merge).

## 2026-11-20 later: #1018 recorded (coordinator's request)

- The coordinator posted the draft as issuecomment-7034745518 (08:46:10Z) and closed #1018 as completed (08:46:11Z); read back identical to the draft but for a blank line before the footer.
- aa32d6dd1 records: #1018 replies gets the final reply (T-327 V3/C3 confirmed current; E-de-winter-1018-n108-sqverify-fast-replay confirmed; E-de-winter-1018-n108-report reviewed), state closed, closed 2026-11-20, read_through 2026-11-20T08:46:10Z, three notes paragraphs; the release record names it, re-measured (43 files byte-identical vs 935e79c36).
- check_requests: #1018 closed 1/1 settled; records tier 55/55; test_check_requests + test_release 146 passed; release_pin --check ok; intake_sweep: #1018's rows gone. Pushed aa32d6dd1 to #1043.
