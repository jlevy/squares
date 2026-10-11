---
type: is
id: is-01m4ksrvt2wctpe4pvy742xcj4
title: Use results.html as the canonical results page
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-10T20:58:45.952Z
updated_at: 2026-10-11T01:13:23.029Z
started_at: 2026-10-10T20:59:56.639Z
closed_at: 2026-10-11T01:13:23.029Z
close_reason: Implemented and source-reviewed in PR462 at 53c8d37a2. Final ordinary Packing38100510883 and Pages38100510886 pass, including frontend and publication assembly. Shared Row outlines match width/alignment and paint gray behind black; web case/Atlas/table data retain ordinary ink. Later neutral-number and shared-spacing requests supersede earlier red-number/spacing intents. Final deferred/merge/deploy remain tracked separately by think-mvh7, think-21wu and think-xio5; controlled CI-performance follow-up remains think-ht59.
resolution: null
duplicate_of: null
---
Publish the full results index at results.html instead of all-results.html. Update website navigation, buttons, canonical URL registry and published links. Retain all-results.html as a query/fragment-preserving forwarder. Preserve existing results filtering and row popovers; update focused routing/publication contracts and PR462.

## Notes

Implementation frozen for the canonical Results URL rename. results.html is the live index, all-results.html is the one-way compatibility forwarder preserving query/fragment; current navigation, buttons/cards, result/case records, 404 recovery, filters, reader docs and active contract sections link directly to results.html. Internal all_results APIs are unchanged. Registry derivation/check:924 rows,0 failures; only the two route roles and measured budget destination changed, without scientific/PDF/content amendments.

Focused proof: Node overview_forward/overview_table/overview_urls49 PASS (0.103s). Python retained routing/registry/head/link selection60 PASS +1 alphabetical expected-findings mismatch in14.28s; corrected only that ordering, and its single rerun1 PASS2.80s. All61 selected contracts therefore pass across these receipts, not an aggregate suite. New registry regression requires canonical/live results, legacy forwarded all-results and sitemap exclusion; legacy and missing-link negative controls remain. Ruff check/format25 Python files, Biome5 JS/Node files and diff-check pass. Repository-pinned Flowmark applied with whole-tree exclusion policy to owned docs. Final shared100-case homepage controls,2.5rem title margin and90% contextual labels documented; external PR body checker passes. Await combined preview/browser proof, final Astra approval and exact pushed-head CI. Keep this bead open until parent authorizes closeout.
