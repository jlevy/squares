---
type: is
id: is-01m2nhy9nsqpwzpdgccyah2myd
title: Overlap Pages browser setup with prepared-page production
kind: bug
status: closed
priority: 1
version: 5
labels:
  - ci
  - validation
dependencies: []
parent_id: is-01m2m5zjmj7dsycs1x6yxwcwwt
created_at: 2026-09-16T16:49:00.600Z
updated_at: 2026-09-17T16:07:40.072Z
closed_at: 2026-09-17T16:07:40.071Z
close_reason: "Landed with PR #188 (merge 042e791c, 2026-09-17T15:54Z): hosted aggregates and the Deferred checkpoint passed on 7f387990; review dispositions in https://github.com/jlevy/squares/pull/188#issuecomment-5714064819. The first main push deployed GitHub Pages at 042e791c with verify-deployment passing."
resolution: null
duplicate_of: null
---
PR #188 exact-head Pages run 35123561787 measured 235 seconds against OR-14's 180-second wall. browser-geometry (webkit) was critical: 3 seconds queued, 95 setup, 40 work, after the serialized scope+prepare chain. Start browser setup after scope and overlap it with prepare, then wait through a reusable fail-closed artifact-readiness tool before download; require an exact-head wall at or below 180 seconds.

## Notes

2026-09-16 evidence audit at da2259fb: implementation done (all 7 browser jobs need only scope, install, then wait via wait_for_run_artifact and download by artifact id; pages.yml:429-443, 1013-1100; test_page_check_setup_overlaps_prepare_then_joins_its_exact_artifact; commits c302b330, 89e247a7). The exit criterion, an exact-head Pages wall at or below 180 s, is unmeasured: gate-budgets.yaml still records the PR 180 reading of 189 s. Keep open until the final-head hosted run is recorded.


2026-09-17: the first hosted run of this design (run 35175474665 at #188 7d76b044) failed every Pages browser check. download-artifact v4.3.0 extracts a download by artifact-ids into <path>/<artifact name>/, so the prepared page landed in packing/site/prepared-page/. Fixed in 21642ed8 (merge-multiple: true on all nine id downloads, plus contract test test_every_download_by_artifact_id_extracts_into_its_path). Packing validation was fully green on that run (packing-required success). The exact-head Pages wall is still unmeasured.


2026-09-17 hosted evidence at 21642ed8: Pages run 35176748416 green. Packing run 35176748398 attempt 1 failed only the suite_b drift rule (work 82.6 s vs recorded 143.98 s, 0.57x; 4,003 passed); attempt 2 passed suite_b (137-141 s) but packing-required failed the pull-request wall at 216 s against 180 s (suite-b last: queued 3 s, setup 60 s including a 49 s full-history checkout, work 141 s). At 7d76b044 the wall was 178 s. Hosted variance on identical code is up to 1.8x per tier. Independent review of cb705c67..21642ed8: APPROVE WITH NITS for the code; merge blocked by the red required aggregate. Should-fix: session 137 must record 21642ed8, the push and these runs. Nits: agendas 031 and 033-035 wording, cap-comment diff description, SYNOPSIS "repaired" wording, exact deploy-condition test, guard empty artifact ids. In progress: wall stability (checkout cost, multi-cohort shard rebalance), code nits, then register recalibration from new exact-head runs (a record between ~92 and ~138 s accepts all three suite_b readings; 82.6 would not).
