---
type: is
id: is-01m2dz5j7vkkz99ssnz99c0rtc
title: "F2: bind the executing calibration reader file to its claimed revision"
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
created_at: 2026-09-13T18:06:14.779Z
updated_at: 2026-09-13T18:43:40.604Z
closed_at: 2026-09-13T18:43:40.604Z
close_reason: Repair committed at reader head 7e4d2487 with maintained focused controls; independent Astra Max exact-head rereview accepted original F1-F5 at their stated scope. See docs/project/reviews/review-2026-09-13-n11-bc329-reader-rereview.md. F6 and separate Git object-type gap remain open.
resolution: null
duplicate_of: null
---
Require the actual resolved running module path and bytes to match the expected checkout path and Git blob; refuse external or altered copies through the public CLI.
