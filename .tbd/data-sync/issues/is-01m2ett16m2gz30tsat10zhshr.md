---
type: is
id: is-01m2ett16m2gz30tsat10zhshr
title: Run the full merge checkpoint on the frozen n11 stack top
kind: task
status: open
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - validation
  - landing
dependencies:
  - type: blocks
    target: is-01m2ett207c0f76hc55gp435wz
  - type: blocks
    target: is-01m2ettfz0drj6x542rqxghvqa
parent_id: is-01m2etr75jfh3t3ry7kj1ccqrb
created_at: 2026-09-14T02:09:17.010Z
updated_at: 2026-09-14T02:09:32.127Z
---
Run one full merge checkpoint on the frozen stack top and record it.

No existing full run counts: #156's full dispatch was at 3daa1b73 (run 34739731760), #157's at e0a1a65e, and #157's deferred dispatch 34790705030 tested 786154bd merged into 2f8925b2. Every PR body still says the full research/merge checkpoint is pending.

Procedure (as for #148/#149): freeze heads; dispatch `Packing validation` (workflow_dispatch) on the top branch of the chain once think-dc10 is integrated (it contains main f2e24e07, so one run covers #156 through the top); hosted wall about 45–55 min. Labeling each PR `deep-gate` would instead run about seven 45-minute jobs. Fix any failure before merging (operating-rules.md:551). Void if main moves before the merge.

Record run ID, head SHA, and step results here and in the PR descriptions (think-j007 description-refresh child).
