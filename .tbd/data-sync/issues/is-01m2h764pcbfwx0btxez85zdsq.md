---
type: is
id: is-01m2h764pcbfwx0btxez85zdsq
title: Extract JavaScript from the explainer, print and math tools and their tests
kind: task
status: closed
priority: 1
version: 6
labels: []
dependencies: []
parent_id: is-01m2h76347zn3abcahzd3642ac
created_at: 2026-09-15T00:24:05.578Z
updated_at: 2026-09-15T17:26:45.038Z
closed_at: 2026-09-15T17:26:45.037Z
close_reason: "Done in PR #181 (https://github.com/jlevy/squares/pull/181): 324 sites in 25 files extracted, allowlist entries removed, identity evidence in the PR"
resolution: null
duplicate_of: null
---
Extract every JavaScript string from the explainer, print and math tooling into probe files, with behaviour unchanged. About 1,700 lines in:

- `packing/devtools/`: `check_print_layout.py` (415 lines), `inspect_explainer_typography.py` (267), `check_math_loading.py` (236), `render_explainer_pdf.py` (206), `render_explainer.py` (105), `sans_instances.py` (86), `check_math_faces.py` (72), `compare_math_fonts.py` (50), `prepare_explainer_math.py` (25), `check_katex.py` (20), `check_scroll_restoration.py` (20), `check_published_site.py` (5) and `check_math_startup.py` (3);
- `packing/tests/`: `test_check_print_layout.py` (121) and `test_pdf_math_browser.py` (87).

Acceptance: these files leave the guard's allowlist; the render and print checks produce byte-identical output where they are deterministic; the affected tests pass; and each new probe is formatted and linted by Biome and type-checked.

## Notes

PR #175's guard measures this bead's scope at 324 sites in 25 files, not the 15 files listed above. The allowlist in packing/devtools/embedded-javascript.yaml is authoritative, and 'python -m devtools.check_no_embedded_js --inventory' lists every site.

Beyond the listed files it adds Node scripts inside tests (test_math_loading, test_render_explainer_pdf, test_render_explainer_fonts, test_motion_lab, test_motion_lab_interactive, test_prepare_explainer_math, test_sans_instances, test_math_startup) and test_check_published_site.

Two files need a decision rather than a probe: test_browser_floor_contract.py (must-fail JavaScript fixtures for Biome and tsc) and test_codex_log_rollup.py (Codex code-mode payloads, which belong in a JSONL fixture).

check_math_startup.py is 5 sites, not 3 lines: a ~400-line init script built by .replace from constants in check_math_loading and render_explainer_pdf. Start with those two modules. For add_init_script with values, use sqpack.probes.applied.

check_published_site.py is already done in #175.

2026-09-15, #175 merge-up of the reviewed stack (#171 at b7627cef) into 9f88e4a7: the guard's inventory still counts 324 sites in 25 files for this bead. The stack added no site here and removed none. The whole allowlist is now 460 sites in 42 files, down from 477 in 48. The name check on devtools.check_probes is stricter now: every literal handed to a loader beside packing/tests/probes or packing/devtools/probes must name a file, so a test that needs a missing name holds it in a variable.

2026-09-15, PR #181 (claude/no-js-explainer-tools, stacked on #179): all 324 sites in the 25 files are gone and their allowlist entries removed; with #178 and #179 the allowlist is empty. 138 probe files, 37 Node scripts (packing/tests/node/, devtools/node/check-katex.mjs), 7 fixtures. Shared helpers are one reference probe, probes/math/library.js, passed as a JSHandle or installed for init scripts by MATH_LIBRARY_INIT; composition never splices text. Identity: prepare_math_html output byte-identical (d473772b); the final page differs only by the host adapter's Biome-formatted text (restoring the old text reproduces d473772b); the PDF from the base page is byte-identical and from the final page differs only in its source-HTML receipt; print-layout, typography, sans-instance, math-font, reload and KaTeX reports byte-identical after path normalisation; timing reports differ only in named timing fields. Floor exception: packing/tests/fixtures/browser-floor (three must-fail samples), declared in DECLARED_BIOME_EXCLUSIONS with a single biome.json includes entry. Nothing deleted instead of extracted. Left open: the shell template's inline page scripts (explainer-shell.html) are outside Biome, as before.
