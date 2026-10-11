---
type: is
id: is-01m3qys80tffp6yf5c3rs00zwg
title: Independently verify candidate438 near-state pose inclusion
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md
delegate: codex-sol-pose
labels:
  - n11
dependencies: []
parent_id: is-01m3qw8b5q2xgjp85cxx24134c
created_at: 2026-09-30T01:27:37.241Z
updated_at: 2026-09-30T01:45:25.887Z
closed_at: 2026-09-30T01:45:25.886Z
close_reason: Conditional fixed-T pose inclusion independently checked; source ancestry and global obligations remain separate.
resolution: null
duplicate_of: null
---
Check every near-state pose against the independently accepted fixed-T local rectangle. Select only the pinned near-refined1024-240.json and local-capture-guards.json objects; verify compressed and decoded identities, extract the final state with retained tooling, and check exact cap U, scale B=(191/50)/U, mask438, bijective roles, all136 live closed angular rows and1542 vertices including point/segment residuals. Use inverse chart (yf/B-U/2,U/2-xf/B), compare with exact construction centers minus T/2, and certify entire angle intervals modulo pi/2 including0 and1. Bind the accepted33 radii and local-isolation receipt. PASS means pose-domain inclusion only, conditional on separately accepted geometric ancestry; capture/global-optimality flags remain false. Retain wall/CPU phase costs, ceilings, and endpoint/omission/wrong-frame refusal controls. No full archive or broad repository tests.

## Notes

Conditional pose inclusion PASS against pinned f9e0de7 source and accepted local result a98623f5. Independent checker SHA72347b98, result SHA c5b97045, exact 136 live closed rows/1542 vertices across 11 role owners, all top/state frame and constraint fields bound, t=0/1 observed; 10,852 source rows. Full source 185,901,535 decoded bytes and guard 37,904 bytes hash verified; compact 265,639-byte derived live rows retained. Tightest exact positive slack about 2.28e-12 (label7 y). Bounded run checker wall3.300s/processCPU0.418s excluding jq child; outer real3.38,user2.73,sys0.54. Six focused omission/frame/chart/source-identity controls pass in1.11s; Ruff/BasedPyright zero. Astra reviewed math. Source ancestry, capture and global optimality remain open.
