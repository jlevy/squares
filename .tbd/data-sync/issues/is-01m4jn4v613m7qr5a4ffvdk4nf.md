---
type: is
id: is-01m4jn4v613m7qr5a4ffvdk4nf
title: "Import squarepacker: preprint v1.1, twelve-tier c*(k) < C_i k^{3/8} + a_i, below the k^{2/5} bound for k >= 2.48e12 (#486)"
kind: task
status: closed
priority: 1
version: 8
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
hold: null
hold_until: null
created_at: 2026-10-10T10:18:41.217Z
updated_at: 2026-10-12T23:39:05.087Z
started_at: 2026-10-10T10:18:41.872Z
closed_at: 2026-10-12T23:39:05.086Z
close_reason: "Completed: squarepacker v1.1 (#486) recorded as reported in asymptotic-waste-bounds.yaml with its coverings replayed; final reply posted and issue closed 2026-10-12."
resolution: null
duplicate_of: null
---
Issue https://github.com/jlevy/squares/issues/486 (opened 2026-10-10T09:46:30Z): version 1.1 of #471's preprint (Zenodo 10.5281/zenodo.23278927, release v1.1 of squarepacker/k2-minus-c-upper). Theorem 1.1 becomes twelve tiers with interval-certified constants, among them 42.09 k^{3/8} + 0.05 (k >= 2.48e12), 41.19 k^{3/8} + 0.04 (k >= 5.22e12), 40.62 k^{3/8} + 1.4e-5 (k >= 3.4e26), superseding v1.0's 43.06 k^{3/8} + 2e-5; Theorems 1.2, 1.4, 1.6 reported unchanged. The mathematical review runs with #471's in the Fable lane (think-rd8u); a later release raising an earlier entry's values is a new register entry.

## Notes

## Draft acknowledgement (2026-10-10, not posted; the owner posts it)

Thank you. Version 1.1 is pinned at release commit 5742311db220b4bd8e825167aeae689a1bd65ce9 (DOI 10.5281/zenodo.23278927, zip md5 d9e681e599152a533f056eaf82d85c0c). It is taken in as a later release of the preprint of #471: the twelve tiers will be a new reported entry beside the version 1.0 bound, which keeps its statement. We will re-derive the new Sections 8.2, 8.3 and 8.6 (ZC', Lemmas 8.2-8.8 and 8.11, Corollary 8.12) and replay cert_v3.py and cert_v4.py for all twelve tiers with their merge checks of the stated constants; the three further coverings per tier, the direct covering of C1-C3 below 10^16 and the fifteen large end packings you describe are not in the release and will be recorded as reported. We will follow up here when the review is on main.

## Records lane, stages 2-4 (2026-10-10, branch worktree-agent-ad6222b29b6c64137)

Commits: 23f18a264 (packets), 947fc1e46 (schema and rows), 742d53765 (tools and tests), e03edc588 (receipts), efd89b421 (correction to the Theorem 1.4 row).

Stage 2. Packet packing/resources/web/squarepacker-k2-minus-c-upper-v11-2026-10-10 (tag v1.1 = 5742311db220b4bd8e825167aeae689a1bd65ce9, tree a88be3b0bc4aa4e12a221121f6fee25fb2d5dbde, committed 2026-10-10T09:20:20Z, retrieved 2026-10-10T10:54:04Z). The Zenodo zip (DOI 10.5281/zenodo.23278927) was downloaded again: md5 d9e681e599152a533f056eaf82d85c0c equals the record; all 102 members equal the tag tree by Git blob; all 99 SHA256SUMS entries verify. 74 new or changed files retained (1,417,122 bytes); 28 unchanged files pinned only: 23 bound by identical_to to the 2026-10-09 packet (two licences, six programs, fifteen recorded outputs), the five certificates bound by equal digest (three retained as original gzip in the v1.0 packet, two hosted; identical_to cannot bind them because it compares a .gz copy decompressed). acquire_source --check: PACKET_MATCHES_ITS_CONTRACT. The repository head after the tag, c6df2f4a07159166df4335167bda237e7a831910, changes only the README's citation DOI.

Stage 4. ryu_upper_replay.py from the packets (Python 3.14.7, mpmath 1.3.0 where the source recorded 1.4.1): all twelve coverings in the source's 24 slices at 320 x 128 boxes, each slice equal to its recorded slice field by field (seconds aside), 38-112 s per slice at load 6-19; each tier's merge of the replayed slices with the stated constants equal to the recorded merge (merged_v3.json entries, C1.json-C3.json; files field aside); the recorded slices merged again, equal; cert_v3.py's regression on the v1.0 row equal (Psi_sup 96.4768909805421, C_E 14.963643923032722); sl_t2_test.py 3000 500 equal; p3test.py 10000 0.5 4 3/2 0.65 1 equal (66.5 s); a10.py for b2_zcp_102400 equal (341.8 s). finalize_v3.py not run (rewrites tiers_v3.json in cwd and calls PATH python, RF-9); its merges were run directly. 52 jobs, all match. Receipts: packing/resources/web/squarepacker-k2-minus-c-upper-v11-2026-10-10/receipts/replay/. Independent: ryu_upper_constants.py decides each tier's C_i, k_i, a_i against its C_E and the table's crossing column (all hold).

Register: the twelve-tier row in deficiency_upper_bounds (source key '[squarepacker k2-minus-c-upper v1.1 2026]', proposed to the coordinator); the v1.0 row keeps its claim. Not reproduced and remaining reported: the three further coverings per tier, the direct covering of C1-C3, the 133-instance re-implementation, the fifteen large end packings (not in the release).

## Stage 7 draft (2026-10-10, to post after PR #487 merges; not posted)

Supports posting after merge: yes (facts checked against PR #487's head 6fb495b3a; no T-NNN or site row is involved, so it can be posted as soon as the merge lands, best after the #471 reply it refers to). Ledger: closeable (check_requests --report: the one result settled as not registered by scope, no ask queued).

@squarepacker, thank you. Version 1.1 is imported on `main` through [PR #487](https://github.com/jlevy/squares/pull/487), as a row of its own in the [asymptotic waste-bounds record](https://github.com/jlevy/squares/blob/main/packing/frontier/asymptotic-waste-bounds.yaml) (`deficiency_upper_bounds`), credited Ryu after Bui. Version 1.0's row keeps its claim.

- **Theorem 1.1 of version 1.1**, twelve tiers c*(k) < C_i k^{3/8} + a_i for every integer k ≥ k_i, is recorded as reported with each tier's C_i, k_i and a_i: B1 46.31, 2.2·10^13, 0.035; B1s 45.49, 4.5·10^13, 0.029; B2 45.08, 6.4·10^13, 0.026; A1 48.76, 4.6·10^14, 0.019; A1s 48.38, 6.1·10^14, 0.017; A2 46.42, 2.7·10^15, 0.011; A3 43.61, 9.6·10^16, 0.0039; A4 41.73, 1.5·10^20, 5.7·10^-4; A5 40.62, 3.4·10^26, 1.4·10^-5; C1 41.19, 5.22·10^12, 0.04; C2 41.78, 2.95·10^12, 0.047; C3 42.09, 2.48·10^12, 0.05. The tiers are below Theorem 1.2's bound for every k ≥ 2.48·10^12, and tier A5 supersedes version 1.0's 43.06 k^{3/8} + 2·10^-5.
- **Theorems 1.2, 1.4 and 1.6** are unchanged in version 1.1, and their rows, answered on #471, say so.
- **Why there is no register entry:** none of these settles a count n ≤ 324, and those counts are what the result register covers.

**How it was checked.**
- The separately prompted AI [review](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-10-squarepacker-k2-minus-c-upper.md) that covers #471 also re-derived the new lemmas and found no gap: ZC′ and Lemmas 8.2–8.5, the sawtooth Lemmas 8.6–8.8, Lemma 8.11, Corollary 8.12 and the tiered proof. It is one AI reading, not a referee's report, and no human review is claimed.
- Your coverings were replayed here at your resolution of 320 × 128 boxes, in your 24 slices, under mpmath 1.3.0: `cert_v3.py` for the nine tiers A and B, and `cert_v4.py` for the three tiers C. Every slice equals its recorded slice field by field, wall time apart. Each tier's merge of the replayed slices reproduces the recorded merge, with every stated-constant check true. `cert_v3.py`'s regression on the version 1.0 row, `sl_t2_test.py`, `p3test.py` and `a10.py` reproduce their recorded outputs too.
- `cases/asymptotic/ryu_upper_constants.py`, written here, recomputes the stated inequalities between each tier's C_i, k_i, a_i and C_E, and the table's crossing column. All hold.

**What rests on your report.** The replays are one covering per tier, your own, and they do not check the transcription of the lemmas into the normalised inequalities. The three further coverings per tier, the direct un-normalised covering of the tiers C for b ≤ 10^16, the 133-instance re-implementation and the fifteen large end packings are not in the release, so they remain reported.

**Notes from the review**, for a later release:
- RF-9: `cert_v3.py` and `finalize_v3.py` read `tiers_v3.json` from the current directory, and the finaliser calls `python` from `PATH`, so they reproduce only from inside `code/cert_v3`. Here the merges were run directly instead of through `finalize_v3.py`.
- RF-3: the last t-piece of a covering can end one unit in the last place below t_u in `cert_v3.py` (line 211), as in `cert3e.py`. The slack makes it harmless here; `cert_v4.py` already sets the end to t_u.

Nothing you asked for is queued, so this issue is closed with this comment.

---
_Generated by [Claude Code](https://claude.ai/code)_

2026-10-10, records lane R4 of the 2026-10-10 intake pass (think-fvz4): correction to the stage 2 note above. Counted from the packet's acquisition record (acquisition/sources.json, sources[0].pinned_only) and its declaration (acquisition/declaration.json, pinned_only), the 28 unchanged files pinned only are 26 bound by identical_to to the 2026-10-09 packet (two licences, six programs, fifteen recorded outputs under code/checker_outputs/, and the three smaller certificates, compared as stored gzip and not decompressed) and 2 bound by digest alone (data/stair_k38250000.json.gz and data/stair_k100000000.json.gz, which the hosted-data manifest packing/hosted/squarepacker-k2-minus-c-upper-certificates.yaml pins), not 23 and 5. The packet README already says 26 and 2. The release data/squarepacker-k2-minus-c-upper-certificates-v1 that the manifest names does not exist yet (HTTP 404 on 2026-10-10; publishing it is the owner's decision, think-sk6b), so the two are to be hosted there once it is published, and the hosted_data fetch command works only then; the records now say so.


## Stage 7 draft from main at c6bf2d46f, 2026-10-11 — not posted (owner: leave as drafts)

Ledger: closeable (`check_requests --report` at c6bf2d46f: the one result settled as not registered by scope, no ask queued). Supersedes the 10 October draft above: names the 11 October final review as a second reading of the tiered proof; no T-NNN or site row is involved. Best posted after the #471 reply it refers to.

@squarepacker, thank you. Version 1.1 is imported on `main` through [PR #487](https://github.com/jlevy/squares/pull/487), as a row of its own in the [asymptotic waste-bounds record](https://github.com/jlevy/squares/blob/main/packing/frontier/asymptotic-waste-bounds.yaml) (`deficiency_upper_bounds`), credited Ryu after Bui. Version 1.0's row keeps its claim.

- **Theorem 1.1 of version 1.1**, twelve tiers c*(k) < C_i k^{3/8} + a_i for every integer k ≥ k_i, is recorded as reported with each tier's C_i, k_i and a_i: B1 46.31, 2.2·10^13, 0.035; B1s 45.49, 4.5·10^13, 0.029; B2 45.08, 6.4·10^13, 0.026; A1 48.76, 4.6·10^14, 0.019; A1s 48.38, 6.1·10^14, 0.017; A2 46.42, 2.7·10^15, 0.011; A3 43.61, 9.6·10^16, 0.0039; A4 41.73, 1.5·10^20, 5.7·10^-4; A5 40.62, 3.4·10^26, 1.4·10^-5; C1 41.19, 5.22·10^12, 0.04; C2 41.78, 2.95·10^12, 0.047; C3 42.09, 2.48·10^12, 0.05. The tiers are below Theorem 1.2's bound for every k ≥ 2.48·10^12, and tier A5 supersedes version 1.0's 43.06 k^{3/8} + 2·10^-5.
- **Theorems 1.2, 1.4 and 1.6** are unchanged in version 1.1, and their rows, answered on #471, say so.
- **Why there is no register entry:** none of these settles a count n ≤ 324, and those counts are what the result register covers.

**How it was checked.**
- The separately prompted AI [review](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-10-squarepacker-k2-minus-c-upper.md) that covers #471 also re-derived the new lemmas and found no gap: ZC′ and Lemmas 8.2–8.5, the sawtooth Lemmas 8.6–8.8, Lemma 8.11, Corollary 8.12 and the tiered proof. The [11 October final review](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-11-final-asymptotic-and-grading.md), by a distinct AI reviewer, re-derived the proof again from the reduction to the tiered constants and accepted the row. Neither is a referee's report, and no human review is claimed.
- Your coverings were replayed here at your resolution of 320 × 128 boxes, in your 24 slices, under mpmath 1.3.0: `cert_v3.py` for the nine tiers A and B, and `cert_v4.py` for the three tiers C. Every slice equals its recorded slice field by field, wall time apart. Each tier's merge of the replayed slices reproduces the recorded merge, with every stated-constant check true. `cert_v3.py`'s regression on the version 1.0 row, `sl_t2_test.py`, `p3test.py` and `a10.py` reproduce their recorded outputs too.
- `cases/asymptotic/ryu_upper_constants.py`, written here, recomputes the stated inequalities between each tier's C_i, k_i, a_i and C_E, and the table's crossing column. All hold.

**What rests on your report.** The replays are one covering per tier, your own, reproduced with your code, and they do not check the transcription of the lemmas into the normalised inequalities. The three further coverings per tier, the direct un-normalised covering of the tiers C for b ≤ 10^16, the 133-instance re-implementation and the fifteen large end packings are not in the release, so they remain reported.

**Notes from the review**, for a later release:
- RF-9: `cert_v3.py` and `finalize_v3.py` read `tiers_v3.json` from the current directory, and the finaliser calls `python` from `PATH`, so they reproduce only from inside `code/cert_v3`. Here the merges were run directly instead of through `finalize_v3.py`.
- RF-3: the last t-piece of a covering can end one unit in the last place below t_u in `cert_v3.py` (line 211), as in `cert3e.py`. The slack makes it harmless here; `cert_v4.py` already sets the end to t_u.

Nothing you asked for is queued, so this issue is closed with this comment.

---
_Generated by [Claude Code](https://claude.ai/code)_
