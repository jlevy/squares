---
type: is
id: is-01m5qsa3atwx2vwehndjk0p9aa
title: "Record amundsk's #755 answers of 24 October: T-239's wall clearance, dilate_cert provenance, CC0"
kind: task
status: closed
priority: 3
version: 8
assignee: null
delegate: c-import-798-1024
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T20:23:21.689Z
updated_at: 2026-10-25T03:54:47.499Z
started_at: 2026-10-24T20:24:13.185Z
closed_at: 2026-10-25T03:54:47.499Z
close_reason: "#755's answers read into the record in #802 (merged 3bdff2443); follow-up posted (issuecomment-6393163946)."
resolution: null
duplicate_of: null
---
Comment https://github.com/jlevy/squares/issues/755#issuecomment-6388401978 (amundsk, 2026-10-24T19:13:49Z, after the issue closed) answers the final reply's three questions on T-239 at 303: (1) the issue's 8.2e-13 wall clearance was an earlier, unsubmitted certificate's; s303_amund.cert at 511f56b has 6.020e-13 (square #3), as the review measured; (2) the certificate was made with search/packer/dilate_cert.py at evand/square-packing 7982d7a9346e29e36cab3ce075274f3023114353 from s303_amund.input.txt, on macOS 26 arm64 with Python 3.14.6 (Apple libm), explaining a last-place tangent difference; only the comment line was edited after; (3) CC0 1.0 for s303_amund.cert, s303_amund.input.txt and the README in gist 78f9f0e7, and for every certificate, input and README in #798's gist at c9be7b7. Record: read_through, the packet's licence and retention (amundsk-n303-2026-10-23 was retained as a derived exact fact for want of a licence), the review's open questions answered. Rides the #798 records change.

## Notes

2026-10-24 c-triage-798-1024 (read-only; draft in /tmp/claude-0/-home-user-squares/d57983cc-21aa-53cd-a24f-c90463a5a3c0/scratchpad/triage-798/record-changes-755.md). Comment 6388401978 created=updated 19:13:49Z. Proposed: read_through 2026-10-24T19:13:49Z; answer_bead think-fc1n (think-tqb5 closed); notes paragraph; packet amundsk-n303-2026-10-23 re-acquired at the same pin retaining all three files under CC0 (keep the derived fact and its bound receipts; derive --check offline); licence text in declaration, README, resources/README; T-239 notes and E-amundsk-755-n303-report limitations gain the answers (8.2e-13 = earlier unsubmitted cert, side 17.909763172478; macOS 26 arm64 Python 3.14.6 Apple libm); review left unedited, its Q1-Q3 answered in the record. Reply owed (stage 7: reading a comment into the record touches the issue; #670 precedent): follow-up on the closed issue after the merge and verified deploy, kind follow-up; no rung moves. #794 (T-240 adopted at 303) was open at triage: adjust the reply's house line if it merges first.


2026-10-25 c-import-798-1024 (PR #802). Applied record-changes-755.md: #755 requests entry read_through 2026-10-24T19:13:49Z, beads + think-fc1n, answer_bead think-fc1n, notes paragraph, summary custody sentence; amundsk-n303-2026-10-23 re-acquired at 511f56b retaining all three files under CC0 (digests unchanged; record keeps retrieved_at_utc 2026-10-23T16:11Z since the derived fact names it), answer kept as acquisition/answer.json, README answers RF-1 RF-3 RF-8; the derived fact stays (upper_bound_reports now admits a fact beside a retained file and holds it to the retained bytes); T-239 claim and notes record the answers (artifacts left unchanged so result/t-239.html keeps its URL identity); E-amundsk-755-n303-report limitations; n303 coverage notes, bibliography note, resources row. Review left unedited. #794 merged first, so the reply names T-240 as the house at 303. Follow-up draft for #755 (kind follow-up; post after merge and verified deploy, coordinator):

@amundsk, thank you for the answers, and for the CC0 dedication. [#802](https://github.com/jlevy/squares/pull/802) read them
into the record on main:

- **The wall clearance.** T-239's notes and the packet now say that the issue's
  8.2·10⁻¹³ came from an earlier, unsubmitted certificate from the same search, and
  that `verify_cert.py` prints 6.020·10⁻¹³ on `s303_amund.cert`, as measured here.
- **The tangents.** The record now says the certificate was made with `dilate_cert.py`
  at `7982d7a` on macOS arm64, Python 3.14.6, so with Apple's libm. That accounts for
  the 36 tangents one unit in the last place from a Linux replay. Side and centres were
  already reproduced to the last digit.
- **Retention.** [The packet](https://github.com/jlevy/squares/blob/main/packing/resources/web/amundsk-n303-2026-10-23/README.md)
  now keeps `s303_amund.cert`, `s303_amund.input.txt` and the README under CC0 1.0, with
  the same digests as before. The exact fact derived from the certificate on 23 October
  stays beside them, since the replay's receipts name it.

Nothing about the result changes. [T-239](https://squaremath.org/result/t-239.html)
stays V3/C3, confirmed, independently re-implemented, S2. Since #794 the house best
packing at 303 is T-240 (#763), 2.78·10⁻³ below, and T-239 is retained as history, as the
final comment said would happen. Your dedication of #798's gist is recorded with that
import. Nothing is queued here, and the issue stays closed.

---
_Generated by [Claude Code](https://claude.ai/code)_

2026-10-25 coord-intake-1024: #755 follow-up posted https://github.com/jlevy/squares/issues/755#issuecomment-6393163946 after #802 merged (3bdff2443) and deployed (40159122496); recorded by #805's round.
