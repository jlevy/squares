---
type: is
id: is-01m3s36jew3nmbz2yhdf33yf8w
title: Index pinned near-capture source in one parse for replay
kind: task
status: closed
priority: 0
version: 4
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3rp1yjrw96h7yy6azcahx2w
created_at: 2026-09-30T12:04:02.651Z
updated_at: 2026-09-30T13:02:43.028Z
closed_at: 2026-09-30T13:02:43.027Z
close_reason: null
resolution: null
duplicate_of: null
---
Measure and implement one-pass, source-hash-bound extraction of the 121 ordered near-capture steps, header, and final state into external scratch. Keep every original field; verify input hash before/after and indexed record integrity. Use indexed reads only after independent review, with no cached PASS premise or source mutation. Compare extraction time to repeated jq and retain a reproducible cost receipt.

## Notes

Astra-approved indexer SHA94075042 frozen in cf4a45327. Fresh build_and_open binds fixed source to derived stream in memory; forged rewritten stream+index refused in focused controls (5 pass). Actual pinned near source 185,901,535 bytes/121 steps indexed once: jq10.019s, scan2.280s, total12.617s; compact receipt capture-near-index/result.json SHA7ce0a9e4, no proof acceptance. Remaining: integrate fresh index within near geometric checker after r111 accepted, pin helper, verify before/after, retain complete geometric receipt. Repeated jq step0 parse observed2.62s; index avoids 121 full parses.

Indexed geometric replay completed under reviewed checker ab824a14 in isolated commit d8230670c. Fresh build_and_open SHA94075042 was invoked inside checker and verified before/after. Three-worker near result e428a9ab PASS_CHILD_NODE_STATE, all121 complete updates, exact final state a6d45c0c, wall302.528s incl fresh index10.904s; source491af and r111 premise5efd bound. Astra independently approved source/result and live-pose projection. 119,372 query rows/7,568,064 exact facets; full tree/global remain separate. One-worker initial attempt was terminated uncredited (exit143, no result). Retained result/stdout/provenance under capture-child-near-full-indexed/; source index remains disposable external scratch.
