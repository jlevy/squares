---
type: is
id: is-01m5kcx4ampkzwwy5h447fcb2e
title: "Close settled intake issues as a standard step: closeable issues close at stage 7 after the verified deploy; only record-blocking questions to the reporter keep an issue open"
kind: task
status: in_progress
priority: 1
version: 9
delegate: c-close-1023
labels:
  - process
dependencies: []
child_order_hints:
  - is-01m57xskzp84r50zqxn5cp8b7b
  - is-01m57xsn5sv2ag6y1h7bz6m4ty
hold: null
hold_until: null
created_at: 2026-10-23T03:29:36.084Z
updated_at: 2026-10-23T22:20:56.061Z
started_at: 2026-10-23T03:30:24.440Z
---
Owner, 23 Oct 03:3xZ: 'if we have actually imported something, it's already on the website, and we validated that, we should close the issues. That should be our standard process.' Things that are unresolved, or need the reporter's feedback, stay open. Finding: check_requests already defines closeable (triage done, every result confirmed or refuted, no ask queued), but 12 issues were closeable and open (317, 470, 529, 570, 573, 582, 584, 624, 670, 672, 675, 728): nothing runs the closing step, intake_sweep does not list closeable issues, and lanes kept issues open for informational questions to the author that the record does not track. Fix: (1) a recorded 'awaiting the author' item for questions whose answer would change the record (credit, lineage, which file), which keeps an issue open and which check_requests counts; informational questions go in the closing comment; (2) intake_sweep's Needs Action lists every closeable issue still open; (3) result-import.md stage 7: after the verified deploy, run check_requests --report and close each closeable issue with its final comment; the six-hourly check-in does the same; (4) a closing pass now. #570 is owner-reserved (#557, #565, #570, #574): never close or reply; list for the owner.

## Notes

2026-10-23 c-close-1023: parts 1 to 3 on claude/intake-2026-10-23-close-issues, draft https://github.com/jlevy/squares/pull/747 (S2, intake, project). e89ed0848: awaiting_author in the requests schema and check_requests (an awaited question blocks closeable; asked must be a recorded reply; none awaited on a closed issue); intake_sweep lists every closeable issue still open under Needs Action ("closeable, still open", exit 1) and each awaited question under the answer bead; result-import.md stage 7 "Close a Settled Issue", the pass steps, the prompt, the requests record and epistemics.md.
Part 4, the closing pass: none closed, nothing posted. #570 owner-reserved. #582, #584, #624, #675 and #728 are closed on GitHub and recorded by #742. #470 (lineage per count, question 2 of the reply of 12 October; that reply was a confirmation, not a final comment, and the 16 October final draft was never posted, so the issue is open on GitHub), #670 (lineage of the 204 seed, question 2 of the follow-up of 23 October) and #672 (credit for the CT105 submission at 227, question 1 of 23 October; review RF-3 says it bears on the house at 227) each hold a credit or lineage question, recorded under awaiting_author (c4f86cbca). #317, #529 and #573 wait on the owner's umbrella or decisions, recorded as queued asks (think-1gbu, think-xnj5, think-g0o4). Coordinator's or owner's call whether #470's and #670's lineage questions are informational: set state withdrawn with a note, then close with a final comment.

2026-10-23 coord-intake-1023: #747 review A (https://github.com/jlevy/squares/pull/747#issuecomment-6360911091): changes requested (A1 owner hold missing, A2 replay not in the register; A3 the awaited questions). Coordinator's A3 call, following the review: keep #672's credit question; withdraw #670's lineage question (already stated and measured in T-226); measure #470's lineage at T-138's counts and credit or withdraw. Addressing agent c-addr-747-1023.

2026-10-23 c-addr-747-1023: review A of #747 added an entry-level owner hold (held) to the requests record; #557, #565, #570 and #574 carry it, with a note saying this bead is where the previous coordinator recorded the owner's reservation. The admission test for awaiting_author is narrowed (the record asserts something the answer could falsify and no measurement here can settle it). #670's and #470's questions are withdrawn (#470 measured pose by pose), #672's stays. Commits 712bbbd0a, cdefdcdba, 1a5fe2b2c, ef43bf583.

2026-10-23 coord-intake-1023: OWNER ASKED about the four holds. In conversation at about 22:00Z on 23 October, the coordinator asked "Which of these four should stay reserved for you? A reserved issue gets no comments and is never closed by the intake ...", with the options #557, #565, #570 and #574. The owner answered "[No preference]". As with think-qh3s, no preference keeps the status quo: all four stay held (basis recorded-reservation). The records' "pending the owner's confirmation" should now say that the owner, asked on 23 October, stated no preference and the holds stand. This rides the next records PR (#753 on merge day).
