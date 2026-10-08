---
type: is
id: is-01m4ea1b1pem2sbqddc70wapg5
title: "n17 supporting CI: attribute Frontier initial-load layout shifts"
kind: bug
status: in_progress
priority: 2
version: 3
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
delegate: claude-code@spud10.local
labels:
  - n-17
dependencies: []
parent_id: is-01m4e47f19w8w1d7tyka9raahk
hold: null
hold_until: null
created_at: 2026-10-08T17:47:34.325Z
updated_at: 2026-10-08T21:14:23.496Z
started_at: 2026-10-08T17:47:41.428Z
---
Supporting CI slice only: authored PR453 Pages fails initial-load Frontier CLS 0.1337926875 > 0.1 on unchanged Frontier source/data; current main also reports a 341ms initial long task >300ms. No deterministic product defect established. Retain bounded native layout-shift source identifiers and previous/current rectangles without forced layout reads, preserve metrics and thresholds, extend the existing early-shift regression, then perform one targeted retained Frontier four-viewport/scheme reproduction if external scratch is healthy. Diagnose and fix only an attributed cause; no broad performance campaign, ceiling relaxation or blanket CI reruns. Source scope initially instrument.js and test_site_rendering.py. Different from think-82bp postdeployment missing-record-link check. Root owns publication and followup scope; mathematics remains priority.

## Notes

2026-10-08 diagnostics source PR457 at7b6f8ce32d355bf4292581df0b511b8dc40857e6 has all required Packing/Pages/mergeability passed at19:39:58UTC. Original Firefox setup stalled37m16s before either font assertion; one targeted job rerun87s passed both and unblocked Pages. No source/threshold change during rerun. Bounded retained four-viewport production reproduction maxCLS0.012638/maxlongtask246ms; historical failuresCLS0.1337926875 and341ms did not recur, cause remains unresolved. Native attribution/control instrumentation is captured and reviewed, but no product-cause or general performance improvement claim. Keep followup scoped to a reproduced and attributed failure; no broad repeated jobs, wall/metric ceiling change or proof credit.
