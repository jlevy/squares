---
type: is
id: is-01m2dz5jn4r6dyknxanbvcf5zb
title: "F3: enforce dense and slab witness agreement in calibration readback"
kind: bug
status: closed
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - calibration
  - admission
dependencies: []
parent_id: is-01m2b884a8xfyybgtpfr4rdwgv
created_at: 2026-09-13T18:06:15.203Z
updated_at: 2026-09-13T18:43:40.609Z
closed_at: 2026-09-13T18:43:40.609Z
close_reason: Repair committed at reader head 7e4d2487 with maintained focused controls; independent Astra Max exact-head rereview accepted original F1-F5 at their stated scope. See docs/project/reviews/review-2026-09-13-n11-bc329-reader-rereview.md. F6 and separate Git object-type gap remain open.
resolution: null
duplicate_of: null
---
Require equal canonical witness pairs as well as equal charges, replay both witnesses independently, and retain the exact 3/8 versus 9/32 equal-charge mutation.
