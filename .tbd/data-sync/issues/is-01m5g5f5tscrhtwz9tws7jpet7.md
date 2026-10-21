---
type: is
id: is-01m5g5f5tscrhtwz9tws7jpet7
title: Reuse canonical profile context in project tally behavioral tests
kind: bug
status: closed
priority: 1
version: 5
delegate: profiles_data_integration
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-21T21:21:55.543Z
updated_at: 2026-10-21T21:48:39.371Z
started_at: 2026-10-21T21:22:49.930Z
closed_at: 2026-10-21T21:48:39.370Z
close_reason: Exact-head db3cb6d4f hosted suite-a job 119501038814 passed, including the unchanged CALL wall guard; local runtime/type/review acceptance already passed.
resolution: null
duplicate_of: null
---
Hosted CI at e162a870a reports three tests in test_site_project_tallies.py exceeding the unchanged 45-second CALL guard without assertion failures. Diagnose repeated expensive test/render work and fix only this module and narrowly relevant shared fixtures, coordinating before production edits. Preserve exact project result and credit counts, links, ordering and selection coverage. Validate meaningful per-test runtimes in the existing external Python 3.14 environment. No push or PR mutations.

## Notes

Patch frozen in packing/tests/test_site_project_tallies.py only. Root cause: the independent _attributed oracle reparsed source-coverage and bibliography YAML and called uncached load_occurrences() for each project; the card test loaded occurrences a second time per project. Each low-level load validates all 75 profiles and source spans. Production already caches the equivalent render inputs and was not changed. No global cache was added to the low-level loader, whose file-mutation and alternate-root behavior remains live.

Added one module-scoped frozen _ProjectInputs fixture containing raw coverage/bibliography rows, validated occurrence records and resources. The oracle still derives keys directly from raw URL/venue/extra-key evidence, not the production source-key mapping. The three tests retain every project loop, exact result/credit/record tally, URL, ordering, native-navigation and filter-selection assertion. Hoisted the unchanged result measures out of the per-card loop and prepared the results page in a module fixture as the shared rendering contract requires. Added a non-vacuous regression that refuses raw-loader calls while the oracle processes every project.

Validation: uv run --frozen --all-extras --group dev pytest -q tests/test_site_project_tallies.py --durations=12 --durations-min=0.01 --junitxml=/Volumes/spud-ext2/agent-scratch/about-profiles-20261020/project-tallies-runtime-regression.xml: 16 passed in 36.79 seconds, including resource/render checks and Chromium link selection. Local CALL durations are 0.12 seconds for project ordering, 0.06 seconds for card tallies, 0.04 seconds for exact project row selection, and 0.03 seconds for the no-reload regression. Setup costs are 22.88 seconds for the shared homepage, 2.97 seconds for validated raw inputs and 3.41 seconds for the shared results page. The hosted baseline on e162a870a was respectively 59.26 / 104.50 / 59.83 seconds; these are separate machine measurements, not a controlled cross-host speed ratio. The unchanged 45-second hosted guard remains enabled and awaits final-head CI.

Focused BasedPyright with external Python 3.14 and two threads reports 0 errors, 0 warnings, 0 notes. Ruff check, format check and git diff --check pass. Astra reviewed the fixture repair with no findings. Coordinator owns joint commit and final CI; no staging, commit, push or PR mutation by this worker.

Hosted closure receipt verified with gh run view 39680389693: exact head db3cb6d4fe5f00a44d04a8ef91018aa2b365bad8, suite-a job 119501038814 completed with conclusion success. The unchanged hosted CALL wall guard now accepts the fixture repair committed in e3e33171bf1d687190cc957a40e25fbbc9dbb23c. Job evidence: https://github.com/jlevy/squares/actions/runs/39680389693/job/119501038814. This completes the scoped runtime acceptance in addition to the 16-test local module/runtime, lint/type and review receipts above. The overall workflow was still in progress when this job was verified; this closure does not claim whole-PR green. The coordinator retains frontend CI/handoff work and the open coverage child under think-zpfo. No source changes.
