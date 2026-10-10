---
type: is
id: is-01m4jk49sdqkab8sbngjs0tvwm
title: "Import TheSnakeFang: s(308) <= 17.999309855162748, s(343) <= 18.994903529220497, s(344) <= 18.995489275430816 (#484)"
kind: task
status: in_progress
priority: 1
version: 3
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
hold: null
hold_until: null
created_at: 2026-10-10T09:43:26.253Z
updated_at: 2026-10-10T11:39:07.470Z
started_at: 2026-10-10T09:49:26.352Z
---
Issue https://github.com/jlevy/squares/issues/484 (opened 2026-10-10). Two-wedge constructions one k up from Arslanov-Mustafin-Shangitbayev; 308 is inside the n <= 324 horizon (register holds the grid 18), 343 and 344 are beyond it (dated beyond-horizon rows). Source TheSnakeFang/squarepack-certs at c75bebd87933416d3e1c7aba35ec733ea8ac7da0, folders n0308, n0343, n0344, Evan Daniel's rational .cert format. Stages 1-3 and a maintained exact replay (seconds).

## Notes

2026-10-10 (sub-agent lane, commit bd43e9c09): stage 2 packet packing/resources/web/fang-two-wedge-certificates-2026-10-10/ at c75bebd8793 (MIT verify.py, CC0 certificates; whole tree retained, drawings pinned only). Each .cert and its SQUISH-layout .cert.json state one exact packing. All three sides round up to the issue's 15-place prints. 308 is below the grid's 18 (case, both lanes) by 6.90e-4. 343 and 344 are beyond the horizon, with no case and no beyond-horizon row when read; below the grid's 19 by 5.10e-3 and 4.51e-3, and below Mishapolk's README prints (19.000000000007, 19.002369297056). Recording: dated rows in source-coverage.yaml beyond_horizon_claims (disposition tracked-outside-case-corpus, value as printed), with the source's claims_record acquisition/beyond-horizon-claims.json, which check_source_coverage.load_claims reparses to exactly {343, 344}. Replay: 9 jobs, all pass/refuse as required, least wall clearance 2^-65. register-plan printed; nothing registered.
