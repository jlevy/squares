---
type: is
id: is-01m0srbdq4h0zk1ngg3vckf03m
title: Correct Stromquist's extraneous Lemma 4 root at a = sqrt(4/5)
kind: bug
status: open
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0p4bxnqxb8dsv2rnqgyp0w8
created_at: 2026-08-24T11:26:36.247Z
updated_at: 2026-08-24T11:28:43.531Z
---
Soundness/source correction. Stromquist's middle Lemma 4 table reports theta*=24.1 degrees and f(sqrt(4/5))=.926, but the smaller positive cubic root is extraneous for the unsquared stationarity equation. The true minimizer is theta about 31.455 degrees with f about .914537789. Theorem 2 survives because b=.9 remains below the corrected minimum. Acceptance: archive preserves the printed row with a visible correction note; an exact/interval calculation certifies the admissible root and b=.9 inequality; H-010 rejects selecting the extraneous root; all downstream descriptions distinguish source text from the corrected computation.

## Notes

2026-08-24: D-151 and source/research annotations record the extraneous 24.1-degree root and corrected f=0.9145377886. Keep open until the exact H-010 checker certifies root admissibility and b=.9 directly.
