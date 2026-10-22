---
type: is
id: is-01m5jea09nya5xe3ka2qebws88
title: Measure Results page cost of shared popover header controls
kind: task
status: in_progress
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-10-contributor-profiles.md
delegate: domain-squares-measure
labels: []
dependencies: []
parent_id: is-01m5jct23n8s7fj3ydf94n0yhv
hold: null
hold_until: null
created_at: 2026-10-22T18:34:52.083Z
updated_at: 2026-10-22T18:46:03.679Z
started_at: 2026-10-22T18:34:59.165Z
---
Measure source-byte delta, retained Results runway through 225 entries, and browser timings before any page-size ceiling adjustment.

## Notes

Measured 2026-10-22 against exact origin/main 78dc902c19d814fa021432f66ed476b0fb1a4266, using isolated external outputs under /Volumes/spud-ext2/agent-scratch/about-profiles-20261020/results-measure-20261022. No source or budget files edited by measurement worker. Baseline rendered from a detached local sparse clone at that commit with retained evidence restored by devtools.render_contributors --checkout-evidence; shared vendor/kpress matches main. Current rendered after coordinator confirmed sprite optimization stable. Both use existing render_overview.results_page(), asset_files(), site_assets.write_assets() and favicon support assets.

Source bytes: baseline 1,248,215; current 1,324,108; delta +75,893 (+6.08%). Earlier pre-optimization shared preview was 1,405,048, so optimized current saves 80,940 bytes. Invoked existing test_the_results_page_has_room_through_its_room_count on both output strings: 228 registered results, P90 row 4,654 bytes, average added entry 263 bytes, more=max(0,225-228)=0. Baseline passes former 1,250,000 limit with only 1,785 bytes left; current exceeds it by 74,108. Recommended 1,400,000 limit retains 75,892 bytes, about 15 further rows at the existing 4,917-byte allowance; do not silently advance fixed RESULTS_ROOM_THROUGH=225. Coordinator subsequently applied that ceiling in its own write set.

Timing command from active packing/ after sourcing integration-env.sh: uv run --frozen --all-extras --group dev python -m devtools.check_site_rendering <baseline-site or current-site> --page results.html --runs 3 --timing-mode report-only > <baseline-rendering.json or current-rendering.json>. Both exited 0, failures=[], timing_exceedances=[]. Existing protocol: fresh Chromium contexts, local gzip unthrottled, observer before navigation, 250ms settle, scroll samples at 0/0.5/1, 1280/390px each light/dark, three JS samples per pair plus separate no-JS run. All no-JS checks pass; no browser/HTTP errors; CLS median 0 for all pairs.

Medians in ms as LCP / longest task / blocking: baseline 1280 light 344/167/141; 1280 dark 340/171/141; 390 light 380/178/140; 390 dark 388/168/173. Current 1280 light 444/189/155; 1280 dark 400/194/150; 390 light 344/178/132; 390 dark 340/197/153. Current maxima across pairs: LCP 444 vs 4000 budget, task 197 vs 300, blocking 155 vs 600; CLS 0 vs 0.1. These are bounded advisory timing receipts on a shared Mac concurrently running preview rendering/prepush checks, not a controlled regression/noise comparison. No repeat campaign or new measurement tools.

Raw receipts: baseline-rendering.json and current-rendering.json in the external measurement directory above, alongside baseline-site/results.html, current-site/results.html and origin-main clone. Timing/projection results retained here because scratch outputs are disposable. No commits or pushes.
