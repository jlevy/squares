---
type: is
id: is-01m2cv8pae8482wfmfdmtzkfft
title: "PR #157 review DOC-02: reader-refusal and completion claims are too broad"
kind: bug
status: closed
priority: 2
version: 2
labels:
  - n11
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-13T07:38:48.526Z
updated_at: 2026-09-13T08:17:13.633Z
closed_at: 2026-09-13T08:17:13.633Z
close_reason: "Fixed: session-127 lines 73, 241-261 and 352+, SYNOPSIS.md 759-766. Verified against threshold_interval.py:165-186 -- the member row holds one slot per token, _counts sums tokens, and the only refusals are MAX_TOKENS_PER_ATOM/MAX_INTERVAL_ATOMS/MAX_MEMBER_SLOTS. Those are allocation limits on a SUPPORTED input, not admission refusals, so the record's 'three readers refuse one' was wrong about the third. Now two readers, with the interval route described separately. The blanket completion claims are scoped to the model and the controls actually built, with the review's open findings named by bead (think-c656, think-p9w7, think-3yb0, think-cv1w) in an appended dated Correction section following session-100:140's form."
resolution: null
duplicate_of: null
---
session-127 lines 241-251, SYNOPSIS.md:744-757 and the PR body conflate unsupported admission readers with the interval route's size guard. The interval implementation supports weighted counts below the cap; it does not categorically refuse weighted input. The implementation findings also contradict the blanket claim that all consumers were audited successfully. Fix: distinguish admission refusal from allocation limits; reconcile completion claims with the repaired code and regression evidence; preserve dated history with an explicit correction.
