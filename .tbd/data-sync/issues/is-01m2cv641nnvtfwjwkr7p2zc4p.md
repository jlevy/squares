---
type: is
id: is-01m2cv641nnvtfwjwkr7p2zc4p
title: "PR157-READ-02: Make weighted records structurally incompatible with old decoders"
kind: bug
status: closed
priority: 1
version: 5
delegate: proof_review
labels: []
dependencies: []
parent_id: is-01m2csyyq4nzfqppqj639avs51
created_at: 2026-09-13T07:37:24.276Z
updated_at: 2026-09-13T08:03:09.456Z
closed_at: 2026-09-13T08:03:09.456Z
close_reason: Fixed in e0a1a65e7c3694554ae76f91092dc9d5c80499f3 with retained regressions and independent Astra Max cross-review. Integrated pre-push gate passed all 46 steps, including 1696 tests; final lint/type checks passed. Parent think-zo70 retains final hosted checkpoint, PR description and per-finding disposition work.
resolution: null
duplicate_of: null
---
PR157 review finding PR157-READ-02: Make weighted records structurally incompatible with old decoders. Published review: https://github.com/jlevy/squares/pull/157#issuecomment-5651978187 . Full exact references, reproduction, and requested remedy are retained in that comment. Address using the address-pr-review shortcut; retain the finding ID in disposition. Review source fa8c3b21817ae10eef903e6c39e5b5d8753b74eb; fixes target the integrated PR156/157 tree.

## Notes

Devtool portion fixed and independently accepted: strict model decoding at orbit boundary; exact and fixed-support admission refuse raw weighted field presence before normalization, including null and empty prototype fields. Current producer-shape and malformed controls pass in owned 132-test suite. Shared serializer and standalone/publication portions are coordinated by root/proof lanes; root owns final combined closure.
