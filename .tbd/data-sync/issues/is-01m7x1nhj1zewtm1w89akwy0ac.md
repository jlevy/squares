---
type: is
id: is-01m7x1nhj1zewtm1w89akwy0ac
title: "Record 2026-11-20 replies (#1008, #1015, #1017, #1020, #1001 follow-up) and JoostdeWinter's comments on #1017/#1018/#1020; check 127 credit against the named starting arrangement"
kind: task
status: in_progress
priority: 2
version: 5
delegate: c18-records
labels: []
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
hold: null
hold_until: null
created_at: 2026-11-20T17:57:01.121Z
updated_at: 2026-11-20T18:49:18.857Z
started_at: 2026-11-20T17:57:08.162Z
---

## Notes

Lane c18-records (2026-11-20). Branch claude/intake-2026-11-20-records-replies (worktree in the coordinator's scratchpad), from main 7a3b186a2, merged with main 298e773a2 (#1048).

Done in the branch:
- Recorded the final replies and closes on #1008 (reported [], as its acknowledgement), #1015 (T-328 superseded), #1017 (T-329 superseded), #1020 (T-330 current), each with the replay, both reviews' evidence and the author's report; the review evidence ids joined each result's evidence. #1001's follow-up recorded with T-305 superseded, no corrects.
- Read de Winter's comments of 20 Nov on #1018 (N-3/N-5/N-8 answers), #1017 (start: Chilton best_current.csv v82, Panoras submission.csv v17; Kodaj relation not established; retracts the files sentence), #1020 (input, wall offset padding, squares 69/91 incidental). read_through moved.
- Formatting-only rewrap of docs/project/reviews/review-2026-11-20-de-winter-1012-n109.md (coordinator's request); the packet's frozen digest lists verify.
- No-public-change record: methods survey byte-identical against main 298e773a2.

127 credit finding (no credit change made): the #1017 comment's attachment is absent; the named files are not in JoostdeWinter/square-packing at its head after 18:00Z, and www.kaggle.com answered an empty 404 to the version page and download, so nothing was measured from them. Scouting only (one-off script, not recorded, OR-1): T-305 and T-328 share their file order for 60 of 127 squares (within 0.184, RMS 0.044), the rest in runs of small index offsets; neither order is a geometric sort. Proposed: keep "de Winter after Chilton, Panoras"; add a file-order pairing to devtools.measure_identity; get the rows (re-attachment or the author's repository) and measure v82/v17 (and Chilton v75, Kodaj's notebook) against T-305 and T-328; whether shared order supports naming Kodaj is the owner's decision.

Added at the coordinator's request: the final replies and closes of #1021 (T-331), #1022 (T-332) and #1031 (T-333), each current, with the replay, the stage 4 review's exact feasibility and the author's report. #1009 owes three position follow-ups (T-320, T-321, T-325 now superseded), per check_requests --report; not recorded, held for the coordinator.

Draft PR https://github.com/jlevy/squares/pull/1053, head 0d959f2138452ad6c50412bd6e295df0fbc40907. Local: records tier 55/55 on the head, edit tier 71/71 on 9ba23e79a; test_check_requests 126 passed; check_requests exit 0.
