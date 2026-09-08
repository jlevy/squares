---
type: is
id: is-01m1w63jacx1cxbp85rm7jvk6s
title: Reject exponent syntax before constructing density packet rationals
kind: task
status: closed
priority: 1
version: 3
spec_path: packing/campaign/agendas/agenda-026-density-stationarity-and-trump-capture.md
assignee: codex
labels: []
dependencies: []
parent_id: is-01m1w5mr8shaew538zws7xqx4x
created_at: 2026-09-06T20:21:09.578Z
updated_at: 2026-09-06T20:38:40.401Z
closed_at: 2026-09-06T20:38:40.401Z
close_reason: "Bounded output complete and reviewed in ongoing PR101: source Theorem3 control+independent review, restricted instrument design, density readiness review and parser correction, landed-code scalar readiness controls, and OR6/OR9 integrated end-to-end process. Research record is now Session089 without clock reset. No target verdict is claimed; parent research/publication beads retain execution and CI follow-up."
resolution: null
duplicate_of: null
---
Independent BC254 readiness review safely reproduced that a short noncanonical exponent string reaches Fraction construction before rejection, bypassing intended parser resource bounds. Add bounded canonical integer/rational lexical admission before conversion; preserve normalization check. Replay the independently retained intercepted-conversion regression and all density controls, without large allocation or target execution. Keep the initial NO-GO and final disposition in the review.
