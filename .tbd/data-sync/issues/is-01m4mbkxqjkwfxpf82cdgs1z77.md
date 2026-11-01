---
type: is
id: is-01m4mbkxqjkwfxpf82cdgs1z77
title: "Import wand125: 15 more n17 sub-pattern kernel certificates, standing verifier full PASS, for admission to certified-sub-patterns.yaml (#495)"
kind: task
status: open
priority: 2
version: 5
labels:
  - result-import
dependencies: []
hold: paused
created_at: 2026-10-11T02:10:38.450Z
updated_at: 2026-10-31T11:18:36.752Z
---
Issue https://github.com/jlevy/squares/issues/495 (wand125, 2026-10-11T02:09:47Z), opened after the 2026-10-10 intake pass's sweep, so it belongs to the next pass. Continues closed #472: 15 sub-pattern kernel certificates made with devtools.check_n17_subpattern (mode A) at 657cc48 (13 with --core octagon), each passing devtools.verify_n17_kernel_certificate in full mode (verifier blob be8135f6e). With main's 72 admitted entries they would leave 2,597 orbits / 20,316 states, down from 3,636 / 28,528. Six are #413 rows (1, 2, 3, 15, 27, 33); may overlap H-342. Objects: release data/n17-kernel-batch3-v1 of wand125/square-packing, 30 objects, 837 MB, HostedData/v1 manifest; one receipt field (directory) rewritten by the author. The standing verifier's full-mode replays total about 4 CPU-hours by the author's timings (sum of the verifier column), so stage 4 needs an owner budget. Next pass: stage 1 triage and acknowledgement, stage 2 custody of the hosted manifest and receipts. Held with the n = 17 intake (think-x4v4).

## Notes

2026-10-12, GitHub tracking (owner's request that the pass's remaining work be tracked as GitHub issues): existing issue https://github.com/jlevy/squares/issues/495 states the remaining work (reply https://github.com/jlevy/squares/issues/495#issuecomment-6119249473: custody, about 4.7 CPU-hours of full-mode replay, census count); #413's rows are mapped there (https://github.com/jlevy/squares/issues/413#issuecomment-6119249016). The budget is on https://github.com/jlevy/squares/issues/543. Tracker https://github.com/jlevy/squares/issues/544.

2026-10-13 owner decision: suspended pending Overbeck's proof that s(17) = L (#557; registered as T-153 by #560, credited by #571), which likely subsumes new s(17) research. Resumes only if the owner lifts the suspension, for example if T-153's replays and reviews find a gap or the candidate is withdrawn. Intake and admission of #495 (wand125's 15 n = 17 sub-pattern certificates, ~4.7 CPU-hours of replay) into this project's n = 17 census; new s(17) research. #495 may want a note that admissions are suspended.

2026-10-31 bold-ritchie-l6 (stalled-bead triage of the 31 October intake pass, think-ztcy): Waits on the owner's standing n = 17 hold of 13 October (pending T-153); #495's admission with its 4.7 CPU-hour full-mode replay, and #413's kernel rows, resume only when the owner lifts it.
