---
type: is
id: is-01m5p9kwtqasajdsw6emw9jm4z
title: "Owner's call: send wand125 the n31 review's M-1 to M-3 and its five questions (T-232), and where"
kind: task
status: open
priority: 3
version: 1
labels:
  - decision
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-24T06:29:51.063Z
updated_at: 2026-10-24T06:29:51.063Z
---
The owner's call, carried here from think-wop1 so that think-wop1 can close: whether, and where, to send Hiroaki Hosono (wand125) the minor findings and the questions of the stage 4 review of T-232, docs/project/reviews/review-2026-10-23-wand125-n31-fine-net.md (think-oc25), since no issue of his asked for s(31) and #534 is the project's own tracking issue.

What they are (the review's Findings and Questions for the Author):
- M-1, minor: the bundle's README.md line 15 names check2/control.jsonl.gz; the release asset holds check2/control-197_200.jsonl.gz.
- M-2, minor: files-sha256.json line 2 gives the README's sealed digest 3e302ff4..., not the published 6dbab236..., because the pre-publication paragraph was added after the manifest.
- M-3, minor: check2/receipt.json line 90 (and README line 12) calls the check "an independent second-system check"; the verifier is jlevy/squares' sqverify_fast with one change, which is why the replay here is recorded as sharing the producer's components.
- Five questions: (1) correct the control file's name (M-1) and regenerate the manifest or say it describes the sealed bundle (M-2); (2) say in the receipt that the check is independent of the search and is this repository's sqverify_fast with the declared-net change (M-3); (3) what least capture the search targeted, given about 1.2e-4 of slack at direction 1841 (N-4), and whether the least capture over all 2,073 directions is recorded; (4) how many threads the pre-publication run used (7,277 s, no thread count); (5) whether he would consider a control closer to the threshold, such as the 99/100 mutant at every direction (N-2).

None of them changes the record: T-232 is at V3/C3 on main (#745) and the answers would change no rung, credit or lineage, so nothing holds an issue open on them. The #446 follow-up of 2026-10-24T05:40:18Z (issuecomment-6380484985) and the #534 closing reply drafted on 24 October leave them out for this decision.

Options: post them on #446, where the author reports this family of certificates; open an issue or a discussion on wand125/square-packing; or send nothing.
