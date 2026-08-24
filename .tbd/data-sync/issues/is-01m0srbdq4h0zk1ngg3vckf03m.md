---
type: is
id: is-01m0srbdq4h0zk1ngg3vckf03m
title: Correct Stromquist's extraneous Lemma 4 root at a = sqrt(4/5)
kind: bug
status: open
priority: 1
version: 4
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0p4bxnqxb8dsv2rnqgyp0w8
created_at: 2026-08-24T11:26:36.247Z
updated_at: 2026-08-24T11:58:23.999Z
---
Soundness/source correction. Stromquist's middle Lemma 4 table reports theta*=24.1 degrees and f(sqrt(4/5))=.926, but the smaller positive cubic root is extraneous for the unsquared stationarity equation. The true minimizer is theta about 31.455 degrees with f about .914537789. The particular a=sqrt(4/5), b=.9 application survives; the distinct Figure 14 a=.95,b=.8 cover failure is tracked by think-bv1d/D-152. Acceptance: archive preserves the printed row with a visible correction note; an exact/interval calculation certifies the admissible root and b=.9 inequality; H-010 rejects selecting the extraneous root; all downstream descriptions distinguish source text, this local correction, and the separate proof gap.

## Notes

2026-08-24: D-151 records the extraneous 24.1-degree root and corrected f=0.9145377886. The specific a=sqrt(4/5), b=.9 Lemma 4 application remains valid, but the broader cover audit exposed a distinct apparent failure at the Figure 14 left-lower cell (a=.95,b=.8), tracked by think-bv1d/D-152. Keep D-151 open until the exact checker certifies the admissible root and .9 inequality directly; do not claim the entire theorem survives from that one inequality.
