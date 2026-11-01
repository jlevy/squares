---
type: is
id: is-01m68a6y7b61h6k2p3da5acs4m
title: "Answer Hyukdong Kim's comment of 26 October on #804: a public copy of his attachments, and the CC0 correction to our 26 October follow-up"
kind: task
status: open
priority: 2
version: 5
labels:
  - intake
dependencies: []
created_at: 2026-10-31T06:26:34.858Z
updated_at: 2026-10-31T18:13:13.214Z
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

2026-10-31 bold-ritchie-l1 (think-6m6e; review A of #854, A1 and A4): the #804 follow-up was posted on 31 October (issuecomment-6541022924) and recorded by #854. think-8r92 stays open as #804's answer bead (check_bead_tree holds an open issue's answer bead live), until the next #804 follow-up lands with think-4rzl's or think-ozx8's change. That next follow-up must name think-9vai as taking in squares-exact-forms.zip's files (the hyukdongkim-exact-forms-2026-10-25 packet): the 31 October reply named only think-4rzl (T-244's configurations) and think-ozx8 (297) for the three CC0 bundles.

2026-10-31 bold-ritchie-l8 (lane L8 of the 31 October intake, think-4rzl), branch claude/bold-ritchie-xo28us-l8: Hyukdong Kim's exact configurations for T-244 are decided on both exact routes. Draft reply for #804, not posted. Post it after the PR merges, on the owner's word. It also answers his question of 26 October, which this bead owns; keep the CC0 correction this bead already drafts, and fold that paragraph in where it fits:

> Thank you for the exact configurations at 172 and 263. Both are now decided here on two exact routes.
>
> - **Your files hold.** Each configuration rebuilds your attached `n172.minpoly.json` and `n263.minpoly.json` byte for byte, with the SHA-256 your comment states. Each side is T-244's: the same irreducible polynomial, a root of it in K, and the same real root.
> - **Route 1**, this repository's exact verifier over K (degree 24 at 172, 17 at 263), decided every unit-square identity, wall and pair. Both configurations are accepted, and both refuse a duplicated square and a square moved outside the box.
> - **Route 2**, Evan Daniel's `verify_exact.py`, run unchanged from the copy this repository retains. Both are VALID, and at each count four mutated controls are refused: a square pushed 10⁻⁶ through a wall it touches, the side raised by 10⁻⁶ in K, the side's interval moved below its root, and a duplicated square.
> - **What it means for the record.** At 263 your exact side is 2.13×10⁻⁹⁴ below the house's rational certificate there (T-174). Once the stage 4 review of the configurations is done, the house rule adopts it, crediting the packing to its finders and the exact side to you. At 172 the house moved on 31 October to Evan Daniel's certificate of issue 845, 1.05×10⁻³ below your exact side. Your configuration there is an exact form of T-174's packing, which is no longer the record, so T-244 stands as a registered bound that a later result supersedes at 172.
>
> Your angle parameters for axis-aligned squares are stated as the empty list (127 squares at 172, 184 at 263). We read them as zero, as `verify_exact.py` does. Your own checker, controls and distance script were not run here.

2026-10-31 bold-ritchie-l8: **posted** the #804 follow-up after #861 merged (main 3c7dd5900) and its Pages deploy verified (run 41226697869): https://github.com/jlevy/squares/issues/804#issuecomment-6547236771. It states T-244 at V3/C3 (both routes and their controls), superseded at 172 by T-257, parked at 263 (think-3trq on think-ot5c and think-ikku); the 13:27Z public copy read; and names think-9vai as taking in squares-exact-forms.zip's files (the owed point from review A4 of #854), think-4rzl for t244-exact-configurations.zip and think-ozx8 for 297's route B; T-247 unchanged. The CC0 correction was already posted on 31 October (issuecomment-6541022924, recorded by #854). Recorded on PR #864 (branch claude/bold-ritchie-xo28us-l8-replies). check_requests: no reply due on #804, not closeable (side-297 open), so this bead stays open as #804's answer bead.
