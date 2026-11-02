---
type: is
id: is-01m68a6y7b61h6k2p3da5acs4m
title: "Answer Hyukdong Kim's comment of 26 October on #804: a public copy of his attachments, and the CC0 correction to our 26 October follow-up"
kind: task
status: open
priority: 2
version: 12
delegate: bold-ritchie-l15
labels:
  - intake
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-31T06:26:34.858Z
updated_at: 2026-11-02T02:02:36.229Z
started_at: 2026-11-01T18:59:31.153Z
closed_at: null
close_reason: null
resolution: null
duplicate_of: null
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


2026-11-01 bold-ritchie-l15 (lane L15 of the 31 October intake): **posted** the #804 confirmation after #868 merged (main b02ca7f7a) and its Pages deploy verified (run 41338863020, verify-deployment 6,035 of 6,035): https://github.com/jlevy/squares/issues/804#issuecomment-6562502956 (19:05:20Z, read back identical to the draft). It states T-247 at V3/C3, confirmed, pending adoption, on route B (verify_exact.py VALID, 1,750 identities, four controls refused; E-hyukdongkim-804-s297-verify-exact); both bundles' files kept from f480441e; route 1 queued (think-ozx8), route A held (think-vv1q); adoption on think-ot5c and think-ikku, then stage 4; the t244 files ask queued (think-4rzl). Recorded on draft PR #871 (branch claude/bold-ritchie-xo28us-l15). check_requests: no reply due on #804, not closeable (the t244 files ask), so this bead stays open as #804's answer bead; the coordinator closes it after #871 merges.

2026-11-02 bold-ritchie-l20 (lane L20 of the intake pass, think-ozx8), branch claude/bold-ritchie-xo28us-l20, PR #876; this draft replaces the one this lane wrote here earlier today, after review A of #876 (finding 3): the reply must name which kind of confirmation T-247 now holds. Route 1 of T-247's route B is recorded (receipts/algebraic-route1-n297.json.xz, evidence E-hyukdongkim-804-s297-exact-feasibility, mapped under #804's side-297). check_requests on the branch: #804 reply due, "side-297: E-hyukdongkim-804-s297-exact-feasibility (verified, replayed-here): confirmed, and no reply has named it".

ONE reply for #804, NOT posted. Lane L22 (think-4rzl, the t244 files ask, #804's last queued ask) adds its news to this same draft rather than writing a second one; if that ask is done, the asks bullet and the closing line change, and check_requests --report on main says whether #804 is closeable (then the reply is the final comment and the entry's state and closed are set). Post after the PRs merge and their Pages deploys are verified, edited against `check_requests --draft 804` rendered from main: it must give T-247 at the rungs, status, mark and position main gives it, and the asks' states main holds. Record it under #804's replies with `reported` for side-297: T-247 V3/C3, confirmed, pending adoption, and E-hyukdongkim-804-s297-exact-feasibility, confirmed; `beads` as named. Keep the footer the earlier replies carry.

> @HyukdongKim, your configuration at 297 is now decided here on a second exact route, one that uses none of your code or of `verify_exact.py`'s, and the files of your last bundle are kept.
>
> **Since our reply of 1 November, 19:05Z.** That reply gave T-247, s(297), as V3/C3, confirmed and reproduced with the source's own checker, and gave route 1 as queued. Route 1 has now run ([#876](https://github.com/jlevy/squares/pull/876)). T-247 stays at **V3/C3, confirmed**, still pending adoption. It now reads **independently re-implemented**: this repository's verifier imports none of your code and none of `verify_exact.py`'s, and it reads your file's poses the way `verify_exact.py` does.
>
> **Route 1, decided on your file.** This repository's exact verifier, `sqpack.witness.exact_verify`, ran over K, the field of degree 21, on your `n297.minpoly.json` (SHA-256 `e5c340b8…2826`), rebuilt as a witness with every centre in K. It decided every unit-square identity, wall and pair, 43,956 pairs, and accepted the configuration. It refused a duplicated square, on overlap, and a square moved outside the box, on containment. Your file gives the angle parameter of 190 squares as the empty list. We read those as zero, as `verify_exact.py` does. This is `E-hyukdongkim-804-s297-exact-feasibility`, confirmed, independently re-implemented after reading the source's checker. So 297 is now decided on two exact routes, as 172 and 263 were: this verifier and Evan Daniel's `verify_exact.py`. Your own checker, controls and distance script were not run here.
>
> **Your files at 172 and 263.** The seven files of `t244-exact-configurations.zip` are now kept byte for byte in the configurations packet ([#878](https://github.com/jlevy/squares/pull/878)), read on 2 November from your public copy at `f480441e`. The zip was held to your comment's SHA-256 (`16e6ad9d…9a2d`), and `n172.minpoly.json` and `n263.minpoly.json` to theirs (`9230aa7a…02db` and `de646870…4686`), before anything was written. Each certificate is byte for byte the file our decision of 31 October rebuilt from the packet's derived facts, so that decision read exactly these bytes, and nothing in it changes: T-244 stays at **V3/C3, confirmed**, superseded at 172 by T-257 and pending adoption at 263. Your programs in the bundle are kept as text and were not run here. All three of your bundles are now kept, so nothing you asked for is queued.
>
> **What remains.**
> - **Route A**, this project's own configuration at the side, is still held over the CPU cap (`think-vv1q`). It would add a route and raise no rung.
> - **Adoption at 297.** Nothing is adopted yet. Your side is the exact value of the house's own arrangement, 3.359×10⁻⁹⁰ below T-174's rational certificate. As at 263, its adoption waits on a writer that lets a house carry an algebraic side (`think-ot5c`). It also waits on the owner's ruling on whether such a side moves a case (`think-ikku`). If both allow it, a stage 4 review of the configuration comes first.
>
> **On `main`.** [`packing/frontier/RESULTS.md`](https://github.com/jlevy/squares/blob/main/packing/frontier/RESULTS.md), [`packing/frontier/n-297.md`](https://github.com/jlevy/squares/blob/main/packing/frontier/n-297.md), [`packing/frontier/n-172.md`](https://github.com/jlevy/squares/blob/main/packing/frontier/n-172.md), [`packing/frontier/n-263.md`](https://github.com/jlevy/squares/blob/main/packing/frontier/n-263.md), [the 297 packet](https://github.com/jlevy/squares/blob/main/packing/resources/web/hyukdongkim-s297-2026-10-25/README.md), [the configurations packet](https://github.com/jlevy/squares/blob/main/packing/resources/web/hyukdongkim-t244-configurations-2026-10-25/README.md).
>
> Nothing you asked for is queued, so this issue is closed with this comment.
>
> ---
> _Generated by [Claude Code](https://claude.ai/code)_

2026-11-02 bold-ritchie-l22 (lane L22 of the intake pass, think-4rzl), branch claude/bold-ritchie-xo28us-l22, draft PR https://github.com/jlevy/squares/pull/878: the t244 files ask, #804's last queued ask, is done on the branch, so L22 filled its placeholders in the one draft above (the opening line, the new **Your files at 172 and 263.** paragraph in place of the asks bullet, the n-172, n-263 and configurations-packet links, and main's closing line) instead of writing a second draft. `check_requests --report` on the branch gives #804 "Closeable: yes, with a final comment"; `--draft 804` ends "Nothing you asked for is queued, so this issue is closed with this comment." So the reply above is the final comment. Post it only after both #876 and #878 merge (#876 first; #878 then merges origin/main) and the later merge's Pages deploy is verified, edited against `check_requests --draft 804` from main. If #878 merges first, hold it until #876 merges: a final comment posted before #876 would close #804 with route 1 at 297 unreported. If #876 is dropped, post the reply without its route-1 paragraphs, and with the closing line only if main still gives #804 closeable. Record it as `kind: final`, with `reported` for side-297 as L20 says and for configurations-172-263 (T-244 V3/C3, confirmed, pending adoption), `beads: [think-ozx8, think-4rzl, think-vv1q, think-ot5c, think-ikku]`; then set #804's state to closed and close the issue as completed.
