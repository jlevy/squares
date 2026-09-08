---
type: is
id: is-01m1t2wz5cedf1wjtjednsr389
title: The n=12 independent verifier's recorded replay is a no-op and its base path is absolute
kind: bug
status: closed
priority: 1
version: 2
labels:
  - research
dependencies: []
parent_id: is-01m1t2sgqmantgyx59knjxqheg
created_at: 2026-09-06T00:46:38.747Z
updated_at: 2026-09-06T01:02:19.744Z
closed_at: 2026-09-06T01:02:19.744Z
close_reason: "Implemented on PR 89 in commit c0db25cf: devtools.freeze_cutting_primal (bridge with tests), run_fractional_cutting --seed-certificate/--seed-map with tests, and cases/n12_fractional_certificate/replay_independent.py with the evidence replay repointed and tested; agenda-025 pre-registers the scalar 61/16 probe for the coordinator to allocate or decline at T+0."
resolution: null
duplicate_of: null
---
packing/frontier/evidence.yaml records the replay 'python cases/n12_fractional_certificate/independent_verify.py cases/.../certificate-77-20.json', but the reviewer's script reads argv[1] as a mode name (both, 19-5, 77-20), so a path selects neither branch, verifies nothing and exits 0; and its base path is the reviewer's /home/user/squares/..., so even the mode form cannot run here. Agenda-025 notes the defect without a bead. The reviewer's file is retained verbatim as evidence (tests/test_lint_floor_contract.py), so add a small wrapper, replay_independent.py, that loads the reviewer's module and runs its verify() on a given certificate path, point the evidence replay at the wrapper, cover it with a test, and update agenda-025's note.
