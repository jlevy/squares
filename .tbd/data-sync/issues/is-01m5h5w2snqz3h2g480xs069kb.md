---
type: is
id: is-01m5h5w2snqz3h2g480xs069kb
title: "Stage 4 for #719's in-corpus entry at 105 and 204: replay, independent review, adoption and regularization"
kind: task
status: in_progress
priority: 2
version: 3
delegate: coord-intake-1021b
labels:
  - result-import
dependencies: []
parent_id: is-01m5h3rxsgydmfjazs3vmw05wp
hold: null
hold_until: null
created_at: 2026-10-22T06:48:12.852Z
updated_at: 2026-10-22T09:58:55.821Z
started_at: 2026-10-22T06:48:15.575Z
---
From the #719 triage (scratchpad triage-719/in-corpus.md): 105 is 5.18e-12 below T-174 (same arrangement re-solved); 204 is 1.006e-8 below T-225 (one to one, 6 squares moved > 0.1, one turned 25.6 deg). Replay ~1 CPU-min, one strong-max review, adoption and regularization 10-50 CPU-min; 105's grid-slack view and SETTLED[204] lapse; think-13e9 then superseded. After #719's records PR.
blocked_on: think-xyhn

## Notes

2026-10-22 c-lane-719-import: the entry is T-229 on branch claude/intake-2026-10-22 (records PR for #719; quote no id to the author until it is on main): s(105) <= 674331486483935962030285457609/62500000000000000000000000000 (5.18e-12 below T-174) and s(204) <= 882663895519250432/59604644775390625 (1.006e-8 below T-225), V0/C0, pending adoption at both, draft S2, regularizations of T-174 (105) and T-225 (204), identity measured (resources/web/mishapolk-issue719-2026-10-22/measure/identity.json). Its unfinished_confirmations names this bead at C3, priced 0.5 to 1 CPU-h. Inputs for stage 4: the facts facts/n-105.yaml.gz and n-204.yaml.gz (derived; no licence, so no upstream byte; derive --check from a checkout at 12fc466 rebuilds them), receipts/exact-certification.json.xz (both routes accept both, all 4 controls refused, 156,996 pairs, 22.55 CPU s; 105 clears walls by 5.00e-21 and pairs by 9.99e-21, 204 by 5.0e-13 and 9.98e-13), acquisition/claims.json (frozen at main 0281e7763). Not run here: the filtered six-control decision at 105 and 204 (beyond_horizon_replay decides only beyond the corpus); the triage measured it in scratch (4.2 CPU s, 6/6 refused on both). The judgment the review should look at: 204 is listed as a regularization of T-225 although one square is re-oriented by 25.64 deg (one to one; 67 beyond 1e-3, 6 beyond 0.1, at most 0.273; T-225 itself moves up to 0.442 from T-223). The release's second 204 file (certificates/n204.cert, 1.48e-11 lower, same packing) is pinned by digest only; if the author names it the entry states its side instead.
