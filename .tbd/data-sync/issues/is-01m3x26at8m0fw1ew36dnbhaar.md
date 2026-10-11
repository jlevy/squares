---
type: is
id: is-01m3x26at8m0fw1ew36dnbhaar
title: main's post-merge validate job fails 11 browser layout tests on Linux at 07f014386 (results and frontier tables)
kind: bug
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-02T01:03:23.972Z
updated_at: 2026-10-02T05:16:12.486Z
closed_at: 2026-10-02T05:16:12.485Z
close_reason: "Fixed in jlevy/squares#300 (commit 761b6f149 and its merge). Cause: Playwright's Chromium headless shell hints text at HINTING_FULL, which on Linux rounds every glyph advance to a whole pixel, so the pixel-pinned table tests measured about ten pixels wide (24ch read 232 against 224.8). No pull-request job ran the two files with a browser, and every main run reused a PR tree until 07f014386. Fix: launch with --font-render-hinting=none through one launcher (preview_site.launch_chromium, tests/site_browser.py), and a new gate step 'site table layout in Chromium' in the frontend job that fails when no Chromium launches. Hosted run 36967715134: the step reads 74 passed on Linux. Defect D-513. Follow-up for the other thirteen browser-backed test files is a separate bead."
resolution: null
duplicate_of: null
---
Run 36943941580 (Packing validation on main at 07f014386, the merge of #286 on top of #289), job validate, both attempts: tests/test_site_frontier_table.py::test_the_table_fits_its_track_at_1280_and_scrolls_in_its_wrap_below (table 1210.8 in a 1200 frame) and ten in tests/test_site_result_columns.py (credit 'Queuingtheorydotcom' breaks inside the name at 1024 and 768; a formula ends a line after ', the ...ng of 2' at 1280; a case list measures 232 against 224.8; the table is 938.2 wide at 1024), on index.html and all-results.html. Deterministic: a full re-run failed the same eleven. Not reproduced on macOS: at 07f014386 both files pass locally, 74 passed. The Pages deployment of the same commit succeeded and check_published_site passed 848 of 848, so the live site is not affected; this is the test surface.

What is known. The validate job normally skips these: when a pull-request run passed the exact tree it reuses 73 fast steps. 07f014386's tree was never a PR head (#286 was green at df0ef9f91 before #289 merged, #289 at 4f3b64cd2), so the whole surface ran in validate, with Chromium from 'playwright install --with-deps --only-shell chromium'. The previous main runs (48e7e5aa8, f25a85cb5) were green by reuse, so they say nothing about these tests in that job. Everything is about ten pixels wider than the macOS measurement, which points at text metrics (a face not applied when measured, or a different fallback) rather than at a rule in #286 or #289; neither PR's site.css diff touches the tables.

To decide: (1) whether the PR shards run these two files with a browser at all, or skip them (shard summaries show '6 skipped'); (2) run the two files in the validate job's environment on 48e7e5aa8 to see whether the failure predates #286/#289; (3) if it is the environment, make the validate job and the shards use one browser and font set; if it is the merge, bisect #286 against #289.

A merge whose tree equals a green PR head (a PR that is up to date with main) is reused and stays green, so this does not block such merges, but main shows red until it is fixed.

## Notes

Findings (2026-10-02, PR #300, branch claude/validate-layout-tests).

Q1, which PR job runs tests/test_site_result_columns.py and tests/test_site_frontier_table.py
with a browser: none did. The four shards install no Chromium, so both files skipped there
(shard A on PR run 36964274240: "2062 passed, 6 skipped"); the frontend job installs Chromium
but ran only check_frontend ("56 passed"); validate on a PR runs --checks, which has no
browser step. A gap in the PR surface (OR-13), now closed for these two files.

Q2, whether they failed in the validate job's environment before #286/#289: no CI evidence
exists either way, because every main run since the pins landed (903b63a09, 3cbbfd1c2,
69c79ed81, eaa1a4b45, f25a85cb5, 48e7e5aa8, and 8aaa411dc after) reused a PR head's tree
("pull-request run N passed this exact tree: 7x tree-reusable fast steps are not repeated");
07f014386 was the first tree no PR had run. The failure is content-free: the 24ch measure
(site.css --site-cases-measure) read 24 x 9 + 16 = 232 px on Linux against 24 x 8.7 + 16 =
224.8 on macOS, so it would have failed at 48e7e5aa8 too. Docker is not installed here, so
no container reproduction.

Q3, what differs: Playwright's Chromium headless shell (151.0.7922.34 in the pinned 1.62.0)
defaults font_render_hinting to HINTING_FULL (headless/public/headless_browser.h); on Linux
FreeType then rounds every glyph advance to a whole pixel, where CoreText on macOS does not.
Same Chromium build, same web fonts (KPress's Source Sans 3 Variable, inlined as data URIs),
settle_math is not involved; the T-060 credit and T-064 list only exposed it at the credit
column's 184 px floor.

Fix: devtools.preview_site.launch_chromium launches every site measurement with
--font-render-hinting=none (identical pixels on macOS with and without it); tests.site_browser
is how the site's tests launch, skipping where no Chromium launches unless
SQPACK_REQUIRE_CHROMIUM is set, when it fails; the quick lane ignores the two files
(SITE_LAYOUT_TESTS); the new frontend step "site table layout in Chromium" runs them with the
requirement set and is classified tree-reusable; workflow guard tests; D-513; tier table at
89 steps; synopsis counts. Hosted Linux reading: run 36967092452, job 110713091091, "74 passed
in 23.87s", 24.16 s inside a 93.16 s frontend wall (150 s ceiling, 104.74 s record).

Not done: the other thirteen browser-backed test files still skip on PRs; all fifteen cost
203 s locally against the frontend tier's 150 s ceiling, so they need a job of their own.
Frontend budget record left for the four-step cohort to re-take.

The run on 761b6f149, 36967715134, is green on all nine PR jobs and packing-required.
