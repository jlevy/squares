---
type: is
id: is-01m4jn4v613m7qr5a4ffvdk4nf
title: "Import squarepacker: preprint v1.1, twelve-tier c*(k) < C_i k^{3/8} + a_i, below the k^{2/5} bound for k >= 2.48e12 (#486)"
kind: task
status: in_progress
priority: 1
version: 4
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
hold: null
hold_until: null
created_at: 2026-10-10T10:18:41.217Z
updated_at: 2026-10-10T11:54:16.224Z
started_at: 2026-10-10T10:18:41.872Z
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
