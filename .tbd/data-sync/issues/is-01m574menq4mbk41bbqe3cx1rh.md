---
type: is
id: is-01m574menq4mbk41bbqe3cx1rh
title: Fix PR435 n83 coefficient link selecting the n87 catalogue entry
kind: bug
status: closed
priority: 2
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4mv11d6aw0ekqzdjfg07w0e
hold: null
hold_until: null
created_at: 2026-10-18T09:14:09.966Z
updated_at: 2026-10-18T09:59:34.689Z
started_at: 2026-10-18T09:43:54.119Z
closed_at: 2026-10-18T09:59:34.688Z
close_reason: F1 source fix published on PR435 at 7c1fe653c5dc30717f1e0546100b1de4ab0a30d7; actual generated case83 URL now resolves to n83 and all673 coefficients. Regression reproduced n87 before fix;32 scoped controls pass in60.82s; Ruff/types/hooks pass. Disposition https://github.com/jlevy/squares/pull/435#issuecomment-6248506970 . Full/parent integration qualification stays open under think-6vrv,think-ht59,think-w0if; current Packing/Pages coverage is not claimed.
resolution: null
duplicate_of: null
---
PR #435 review F1, pinned head 273abfa593d64a01256f8da0059aeae2e4d64186.

The n=83 case page's complete-coefficient link selects n=87 in the lazy catalogue. packing/devtools/render_case_pages.py:551 constructs #current-polynomial-for--83 from the count, while exact_catalogue.output_files assigns that legacy anchor by polynomial order. The current exporter gives current-n83 degree672 anchor --79 and current-n87 degree41 anchor --83. overview/exact-side-values.js:386 resolves the latter directly to n87. tests/test_case_pages.py:505 currently asserts the wrong literal.

Use the stable current-n83 identity (or the authoritative generated anchor) and add a producer-to-browser resolver regression proving that the case83 link selects n83 and exposes its 673 coefficients. Preserve all source custody, numeric bounds, polynomial strings and publication limits. Existing 17 catalogue tests pass in29.99s but miss this cross-consumer defect.

This is an engineering follow-up under the existing stack owner think-6vrv. No mathematical replay, source edits, commits, pushes or merges were performed during the bounded review.
