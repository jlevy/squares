---
type: is
id: is-01m0p6byr6yrahadhq9dt48q57
title: "PR #5 review D-1: name the layers: sqpack-core owns validity, sqsearch owns move energy"
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m0p6bwcyve6zdv41ezr08e3g
created_at: 2026-08-23T02:14:36.036Z
updated_at: 2026-08-23T02:23:20.057Z
closed_at: 2026-08-23T02:23:20.057Z
close_reason: "FIXED. Added differential_test.py: sqsearch's pair_depth == 0 must agree with sqpack's separated() on 20,000 deterministic near-contact pairs, wired into test.sh and mutation-checked (a loosened threshold produces 925 disagreements). sqsearch gained a --pairdump mode to emit its verdicts for the oracle to check. The layer split is now enforced rather than asserted: sqsearch owns move-loop energy, sqpack owns validity."
---
Measurement is right for the performance half and wrong for the trust half. sqpack-core owns validity semantics; sqsearch's pair_depth is a metric not a verdict, and a second implementation is fine as long as it never says what is valid. Concretely: treat sqsearch overlap as a screen gating nothing downstream, and add a differential test of pair_depth==0 against sqpack's separated() on random near-contact pairs. The JSONL seam is a good boundary, not a stopgap.
