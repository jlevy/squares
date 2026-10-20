---
type: is
id: is-01m4z41xj0y1apyem4s5k2s9y6
title: "Validate s(28) > 1149/200: replay of the 43 slabs on the reviewed T-145 kernel (route B)"
kind: task
status: open
priority: 3
version: 1
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m4z41fnn0pf6c5wgngeg94gx
created_at: 2026-10-15T06:30:07.168Z
updated_at: 2026-10-15T06:30:07.168Z
---
## Validation
- Claim: s(28) > 1149/200 (wand125/square-packing continuous_n28_L5745, pinned at 8530bafb03d48444f30f241fbc1f29f01cd7c96c; asset SHA-256 d7249d0d...9ab8). Checker: this record's reviewed copy of Guzhou0806's continuous-pose kernel (V-guzhou-n40-continuous-pose, source da06206b, built from the T-145 packet with the release flags into the CI binary 69bc9e64...) on the pose input regenerated here (SHA-256 214b2731..., equal to the source's), over T-145's 43 slabs; and the near-axis patch at A = 249499501/250000000, whose 33.5 million-vertex grid the reviewed axis kernel's 15M cap refuses: decided by check2's axis kernel (caps raised, no arithmetic changed; binary 3d144a45...) or by sqverify-fast's exact axis sweep at core A, as T-145's was a second way.
- Run: a preparation slice first (W7): a `replay` subcommand of `devtools.continuous_pose_followup` that runs the 43 slabs at two workers, writes slabs.jsonl.gz and a judged replay receipt as `devtools.audit_continuous_pose run`/`check-replay` do for T-145, and adds a sensitive control; `sample --slabs 0,...,42` already runs and judges each slab one at a time. Then the axis patch both ways, and the controls: the published 985/1000 control (refused at the axis in seconds) and a mutant whose axis patch still holds, run at the least-bound slabs.
- Cost: 12.7 CPU-hours here (high 30.4, the source's own CPU): slabs 0 and 14 ran in 567.6 CPU-s (kernel timing 675.2 s) against the source's 1,613.8 s (ratio 0.42), applied to the source's 109,538 s over the 43 slabs (receipts/sample-diagnostic-n28.json); about 6.4 h wall at two workers. The axis patch takes seconds and about 2.1 GB. The preparation slice is a few agent-hours.
- Budget status: runnable after the preparation slice and an owner budget; under the 40 CPU-hour cap.
- Possible subset under the cap: the whole run fits.
- Depends on: the preparation slice; the owner's budget; the records PR that registers the result; a review that reads this certificate.
- Done when: all 43 slabs verified here with nodes, leaves and least bounds equal to the source's receipt, the axis patch proved, the controls refused, receipts retained in the packet, and the evidence registered as re-implemented sharing the producer's components (the source's check2 runs the same kernel).
- Machine note: CPU-bound, single-threaded kernel processes of a few MB; the axis kernel needs about 2.1 GB for a few seconds. Two workers share a four-core host with a gate.
