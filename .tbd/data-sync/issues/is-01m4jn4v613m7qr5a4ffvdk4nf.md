---
type: is
id: is-01m4jn4v613m7qr5a4ffvdk4nf
title: "Import squarepacker: preprint v1.1, twelve-tier c*(k) < C_i k^{3/8} + a_i, below the k^{2/5} bound for k >= 2.48e12 (#486)"
kind: task
status: in_progress
priority: 1
version: 3
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
hold: null
hold_until: null
created_at: 2026-10-10T10:18:41.217Z
updated_at: 2026-10-10T10:52:26.594Z
started_at: 2026-10-10T10:18:41.872Z
---
Issue https://github.com/jlevy/squares/issues/486 (opened 2026-10-10T09:46:30Z): version 1.1 of #471's preprint (Zenodo 10.5281/zenodo.23278927, release v1.1 of squarepacker/k2-minus-c-upper). Theorem 1.1 becomes twelve tiers with interval-certified constants, among them 42.09 k^{3/8} + 0.05 (k >= 2.48e12), 41.19 k^{3/8} + 0.04 (k >= 5.22e12), 40.62 k^{3/8} + 1.4e-5 (k >= 3.4e26), superseding v1.0's 43.06 k^{3/8} + 2e-5; Theorems 1.2, 1.4, 1.6 reported unchanged. The mathematical review runs with #471's in the Fable lane (think-rd8u); a later release raising an earlier entry's values is a new register entry.

## Notes

## Draft acknowledgement (2026-10-10, not posted; the owner posts it)

Thank you. Version 1.1 is pinned at release commit 5742311db220b4bd8e825167aeae689a1bd65ce9 (DOI 10.5281/zenodo.23278927, zip md5 d9e681e599152a533f056eaf82d85c0c). It is taken in as a later release of the preprint of #471: the twelve tiers will be a new reported entry beside the version 1.0 bound, which keeps its statement. We will re-derive the new Sections 8.2, 8.3 and 8.6 (ZC', Lemmas 8.2-8.8 and 8.11, Corollary 8.12) and replay cert_v3.py and cert_v4.py for all twelve tiers with their merge checks of the stated constants; the three further coverings per tier, the direct covering of C1-C3 below 10^16 and the fifteen large end packings you describe are not in the release and will be recorded as reported. We will follow up here when the review is on main.
