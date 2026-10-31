---
type: is
id: is-01m68a6y7b61h6k2p3da5acs4m
title: "Answer Hyukdong Kim's comment of 26 October on #804: a public copy of his attachments, and the CC0 correction to our 26 October follow-up"
kind: task
status: open
priority: 2
version: 2
labels:
  - intake
dependencies: []
created_at: 2026-10-31T06:26:34.858Z
updated_at: 2026-10-31T06:26:52.629Z
---
Hyukdong Kim's comment of 2026-10-26T11:50:22Z on #804 (https://github.com/jlevy/squares/issues/804#issuecomment-6415293035), read into #804's entry on 31 October by PR #833 (think-6m6e), restates the CC0 1.0 dedication of all three of his attachments and ends with a question: he can put the same files, with the same digests, in a public repository or gist, "Just say which you prefer". Review A of #833 (A1) found that nothing owed him the answer: the last reply was posted at 10:29:17Z the same day, and check_requests.replies_due compares days (the tool defect has its own bead).

The reply also owes a correction. Our follow-up of 26 October (issuecomment-6413810519) said the T-244 attachment "states no licence", so its packet keeps only derived facts; his CC0 dedication of 25 October, 12:00:41Z (issuecomment-6397363927), already covered t244-exact-configurations.zip. #833 marks that statement outdated on the reply, so check_requests --report lists #804 as owing a reply that corrects it.

This bead is #804's answer bead from #833. Once #833 merges, render `check_requests --draft 804` from main, check main and the deployed site, post the reply with the correction and the answer below, and record it under #804's replies with `corrects: [issuecomment-6413810519]`. Done when it is posted and recorded.

blocked_on: jlevy/squares#833

## Notes

2026-10-31 bold-ritchie-l1 (think-6m6e): draft of #804's reply, to post only after #833 merges and to edit against `check_requests --draft 804` rendered from main (it must still name T-244 and T-247 at the rungs and positions main gives them):

> @HyukdongKim, thank you for your comment of 26 October.
>
> **A correction.** Our follow-up of 26 October said that `t244-exact-configurations.zip` "states no licence", so its packet keeps only derived facts. That was out of date. Your comment of 25 October, 12:00:41Z, dedicated both `squares-exact-forms.zip` and `t244-exact-configurations.zip`, data and code, to the public domain under CC0 1.0, and your comment on 297 did the same for `s297-exact-configuration.zip`. Your comment of 26 October restates it for all three, with the digests the record holds. So the packets may keep the files themselves, as you ask. Taking them in is `think-4rzl`'s for T-244's configurations and `think-ozx8`'s for 297.
>
> **A public copy.** Yes, please: a public repository rather than a gist. A packet pins a commit, and the intake reads a watched repository's commits, so a repository gives the files a fixed address that stays checkable. The attachments return HTTP 403 to our sessions, so route B at 297, your `n297.minpoly.json` decided on `exact_verify` and on the retained `verify_exact.py`, waits on a copy we can fetch. Please link the repository and commit here.
>
> [The T-244 and T-247 status lines from the rendered draft.]

Record it with `corrects: [https://github.com/jlevy/squares/issues/804#issuecomment-6413810519]`, the ids and rungs it states under `reported`, and the beads it names.
