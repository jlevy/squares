---
type: is
id: is-01m2dz5k4wf297ycgbyerrmgjy
title: "F4: enforce strict JSON value schemas and bounded refusals in calibration readback"
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
created_at: 2026-09-13T18:06:15.707Z
updated_at: 2026-09-13T18:43:40.614Z
closed_at: 2026-09-13T18:43:40.614Z
close_reason: Repair committed at reader head 7e4d2487 with maintained focused controls; independent Astra Max exact-head rereview accepted original F1-F5 at their stated scope. See docs/project/reviews/review-2026-09-13-n11-bc329-reader-rereview.md. F6 and separate Git object-type gap remain open.
resolution: null
duplicate_of: null
---
Reject bool/int/float coercions throughout candidate, rows, receipts, topology, and resource summaries; convert expected oversized-number parser/conversion failures to CLI refusal exit 2.
