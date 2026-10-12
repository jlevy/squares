---
type: is
id: is-01m4pdmp47pzbka09ak8j79njd
title: Repair macOS font-shift and native radical browser controls
kind: bug
status: open
priority: 2
version: 2
labels:
  - browser
  - testing
dependencies: []
created_at: 2026-10-11T21:24:29.446Z
updated_at: 2026-10-11T21:29:19.187Z
---
Three browser rendering checks fail on the unchanged baseline under the same macOS environment as the 2026-10-11 full checkpoint. They predate the site/prose cleanup. Related checkpoint-environment investigation: think-bbug.

Baseline: c82c3c562eecf832350d2c083c7a2ee25788a903, with the original 40-base reading measure and logo navigation. KPress source: its exact gitlink 515f4a08aaf529f922b4380db7f7b7913b01abf5. Python 3.14.7, pytest 9.1.1, macOS; DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib. Renderer, sqpack, and KPress imports were verified to resolve to the disposable baseline checkout.

The exact checkpoint override SQPACK_CHROMIUM=/Applications/Google Chrome.app/Contents/MacOS/Google Chrome launches Chrome 152.0.7977.83. On this baseline, the following three cases failed in 77.92 seconds, with the same values as the checkpoint:

- tests/test_site_rendering.py::test_results_prose_font_arrival_retains_layout[unadjusted]: CLS 0.0028717770655270654, while the negative control requires CLS > 0.1. The actual temporary prose font is Georgia (395 glyphs), with PT Serif Italic and KPress Quotes also present.
- tests/test_site_rendering.py::test_frontier_native_radical_paints_hook_and_bar_and_rejects_text_font[screen]: hook true, bar false; hook_pixels 183, bar_pixels 18, hook_height 33, text_left 28, width 62, height 46.
- tests/test_site_rendering.py::test_frontier_native_radical_paints_hook_and_bar_and_rejects_text_font[print]: hook true, bar false; hook_pixels 123, bar_pixels 15, hook_height 26, text_left 23, width 50, height 38.

With SQPACK_CHROMIUM explicitly unset, the installed Playwright browser is Chromium 151.0.7922.34. On the same baseline the two radical cases pass; the unadjusted-font control still fails with the identical CLS. That run completed in 41.22 seconds (one failure, two passes). BrowserType.executable_path in Playwright's repr names its default browser and does not establish the executable actually launched; the explicit override and browser.version were recorded separately.

Both runs used the external environment's Python with `-m pytest -vv --tb=long -rA`, exactly the three case IDs above, explicit external TMPDIR/UV_CACHE_DIR/CARGO_TARGET_DIR, and CLI options `-o tmp_path_retention_policy=failed -o tmp_path_retention_count=1 -o cache_dir=<external-evidence>/pytest-cache --basetemp=<external-task-scratch>/pytest`. The Chrome 152 run also used `--showlocals`. No production or test source was changed for either comparison.

Retained local evidence, all under /Volumes/spud-ext1/agent-scratch/squares-site-cleanup-01a12c91/:

- full-gate.log: original checkpoint failures.
- browser-baseline-chrome-evidence/environment.json: exact baseline/import provenance, override, and launched Chrome version.
- browser-baseline-chrome-evidence/pytest.log and junit.xml: same-environment three-case run, including full failure locals.
- browser-baseline-chrome-evidence/radical-screen.png and radical-print.png: failing construction screenshots copied out of pytest temporary storage.
- browser-baseline-evidence/pytest.log, junit.xml, and environment.json: default Chromium 151 comparison.
- browser-baseline-evidence/pytest-setup-error.log: earlier setup-only attempt lacked the KPress instance generator; it is not part of the regression comparison. The baseline was populated from the exact pinned local KPress Git archive before both completed runs.

Investigate the native radical paint differences between Chrome 151 and 152 and the unadjusted-fallback negative control's platform assumptions. Preserve the native hook/overbar paint checks and the production CLS budget. Make the negative controls demonstrate the failures they claim to catch; do not weaken thresholds or discard paint checks merely to make these runs pass. Validate any repair against both browser versions and the positive and deliberately damaged controls.

## Notes

Final combined browser suite after the cleanup: 414 passed, 6 skipped, and exactly the three baseline font-control failures, in 187.29 seconds. Supported native allocation: --jobs 4 --inner-jobs 2. Full output: external task scratch layout-parallel-artifacts/command-2afcfe14e0e941c182af0d3278d4d68f.log. No remaining layout failures.
