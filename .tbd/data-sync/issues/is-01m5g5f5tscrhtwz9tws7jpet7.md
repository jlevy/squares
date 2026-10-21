---
type: is
id: is-01m5g5f5tscrhtwz9tws7jpet7
title: Reuse canonical profile context in project tally behavioral tests
kind: bug
status: in_progress
priority: 1
version: 3
delegate: profiles_data_integration
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-21T21:21:55.543Z
updated_at: 2026-10-21T21:26:42.661Z
started_at: 2026-10-21T21:22:49.930Z
---
Hosted CI at e162a870a reports three tests in test_site_project_tallies.py exceeding the unchanged 45-second CALL guard without assertion failures. Diagnose repeated expensive test/render work and fix only this module and narrowly relevant shared fixtures, coordinating before production edits. Preserve exact project result and credit counts, links, ordering and selection coverage. Validate meaningful per-test runtimes in the existing external Python 3.14 environment. No push or PR mutations.

## Notes

Patch frozen in packing/tests/test_site_project_tallies.py only. Root cause: the independent _attributed oracle reparsed source-coverage and bibliography YAML and called uncached load_occurrences() for each project; the card test loaded occurrences a second time per project. Each low-level load validates all 75 profiles and source spans. Production already caches the equivalent render inputs and was not changed. No global cache was added to the low-level loader, whose file-mutation and alternate-root behavior remains live.

Added one module-scoped frozen _ProjectInputs fixture containing raw coverage/bibliography rows, validated occurrence records and resources. The oracle still derives keys directly from raw URL/venue/extra-key evidence, not the production source-key mapping. The three tests retain every project loop, exact result/credit/record tally, URL, ordering, native-navigation and filter-selection assertion. Hoisted the unchanged result measures out of the per-card loop and prepared the results page in a module fixture as the shared rendering contract requires. Added a non-vacuous regression that refuses raw-loader calls while the oracle processes every project.

Validation: uv run --frozen --all-extras --group dev pytest -q tests/test_site_project_tallies.py --durations=12 --durations-min=0.01 --junitxml=/Volumes/spud-ext2/agent-scratch/about-profiles-20261020/project-tallies-runtime-regression.xml: 16 passed in 36.79 seconds, including resource/render checks and Chromium link selection. Local CALL durations are 0.12 seconds for project ordering, 0.06 seconds for card tallies, 0.04 seconds for exact project row selection, and 0.03 seconds for the no-reload regression. Setup costs are 22.88 seconds for the shared homepage, 2.97 seconds for validated raw inputs and 3.41 seconds for the shared results page. The hosted baseline on e162a870a was respectively 59.26 / 104.50 / 59.83 seconds; these are separate machine measurements, not a controlled cross-host speed ratio. The unchanged 45-second hosted guard remains enabled and awaits final-head CI.

Focused BasedPyright with external Python 3.14 and two threads reports 0 errors, 0 warnings, 0 notes. Ruff check, format check and git diff --check pass. Astra reviewed the fixture repair with no findings. Coordinator owns joint commit and final CI; no staging, commit, push or PR mutation by this worker.
