---
type: is
id: is-01m5mrzp4cfj4fr5bkvacmp4zr
title: "Site URLs: disposition for the nine atlas/regularized SVGs the algebraic adoption removes (70, 102, 123, 153, 207, 258, 259, 295, 302)"
kind: task
status: closed
priority: 1
version: 6
delegate: c-fix-756-1023
labels:
  - decision
  - site
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-23T16:19:57.196Z
updated_at: 2026-10-24T01:05:11.946Z
started_at: 2026-10-23T22:18:45.109Z
closed_at: 2026-10-24T01:05:11.946Z
close_reason: "Superseded by #761's 324-address regularized view; #756 green at 7bc4cae11 with no URL change"
resolution: null
duplicate_of: null
---
The adoption of the nine algebraic houses on 23 October 2026 (think-ot5c, branch claude/intake-2026-10-23-algebraic-houses) leaves the regularized layer's index with no view at 70, 102, 123, 153, 207, 258, 259, 295 and 302. The axis tool refuses a number-field witness (`unsupported-scalar-kind`), the lapsed strong views are not kept (the owner's answer to question 13, think-r8cn), and no regularizer yet draws an exact view of a number-field witness (think-mbdw). So `render_overview.support_file_paths` no longer declares `atlas/regularized/n-{70,102,123,153,207,258,259,295,302}.svg`. These nine are live rows in packing/site-urls.yaml, first published 2026-10-07.

`site_urls --check --history-ref origin/main` (the records tier's "published URL registry and historical compatibility" step, and the PR gate) fails with "removed live URL atlas/regularized/n-102.svg: retain a forwarder or a withdrawn tombstone". It stops at the first of the nine.

Each disposition the registry offers touches site infrastructure that belongs to the site lane:
- (a) A `render_overview.MOVED_FILES` copy of `atlas/house/n-NNN.svg` at each old address, with the matching `moved` lines in .github/workflows/pages.yml (publish job) and the fixture in tests/test_pages_workflow.py. The address keeps serving the drawing now drawn. When think-mbdw later draws a view there, the same PR has to drop the entry, or the step's "already published" guard fails.
- (b) `status: withdrawn`, which `validate_registry` admits only for `.html` paths, so `site_urls` needs an asset-file withdrawal: code in site_urls.py.
- (c) Hand-editing the rows to `status: forwarded`. The validator would pass, but nothing serves a forward for an asset and the deployed check fetches no assets, so the registry would claim a redirect that does not happen. Not recommended.

Recommended: (a), or (b) if the site lane prefers a withdrawn asset to a stand-in drawing. The intake lane was scoped away from site code (LANE-RULES "Scope"), so it made none of these changes. Done when the nine addresses have a disposition the registry accepts and the algebraic houses PR's records tier passes.

## Notes

2026-10-23 c-fix-756-1023 (lane of coord-intake-1023, PR #756, branch claude/intake-2026-10-23-algebraic-houses):
- Decision received from the coordinator: option (b). Retire the nine addresses as withdrawn, each with a recorded reason, by extending site_urls' withdrawal (HTML-only) to asset files. 102, 123, 153, 207, 258, 259, 302: the house changed on adoption on 23 October and its regularized view is owed on think-mbdw. 70, 295: the adopted house reads regular as published, so the house drawing is the view. No stand-in drawing, no hand-marked forwarder.
- Not implemented, because the premise no longer holds once main is merged. #761 (merged as 77aba4c02; commits 23610ccaf and 87f87c89a) redefined `atlas/regularized/n-N.svg` as every count's Regularized-mode picture, its default picture in its canonical pose (docs/project/specs/active/plan-2026-10-23-flip-regularization.md, "API Changes": "324 addresses, from 95"). `render_frontier_page.drawing_paths` now declares that address for all 324 drawn counts, and #762 (64b316b6c) pins the atlas tile's starting source there. So the builder declares the nine addresses again, and at each it serves the adopted house drawing in its canonical pose. That file is byte-identical to atlas/house/n-N.svg at 123, 153, 207 and 302, and turned at 70, 102, 258, 259 and 295.
- Evidence at the branch head after merging main 64b316b6c (ebf578eb6, and 7bc4cae11 for a test fix):
  - `site_urls --check --history-ref origin/main`: 1388 rows, 0 failures, with site_urls.py, its tests, site-urls.yaml and site-urls.md unchanged;
  - local overview build and `check_published_site --local --partial --producer overview`: 8217 of 8217 checks passed, with 324 files under atlas/regularized/; atlas.html loads atlas/regularized/n-102.svg;
  - hosted at ebf578eb6: the Pages run 40036790434 passes (overview, publish, pages-required), and validation run 40036790440 passes validate and suite-c. Its one failure was a #761 pose test that took 70 as a rational witness, fixed in 7bc4cae11.
- Why (b) cannot be applied in this lane's scope: `derive_registry` restores any declared path as live. Withdrawing the nine would therefore need the builder to stop declaring them, which is site code in render_frontier_page. The atlas tiles also load every count's drawing from that address, so withdrawing it would leave nine tiles without an image, which is a visual change. The brief says to stop and report in that case.
- Open question for the coordinator, the site lane or the owner: the rationale for (b) was that a house drawing served at a "regularized" address misstates which drawing it is. That concern now applies to main's own design at every count without a drawn view (the 229 addresses #761 added, plus these nine). It is not resolved here.
- Outcome: the PR's URL-registry blocker is cleared by the merge alone. There is no registry code, test or register change. The bead is left in_progress, for the coordinator to close or re-decide.
- CI at 7bc4cae11 (after handback): green. Packing validation 40038308777, Pages 40038308826 and Branch mergeability 40038303699 succeed; 31 checks pass, none fail.


2026-10-24 coord-intake-1023: SUPERSEDED, no change needed. #761 (the flip-regularization session) redefined atlas/regularized/n-N.svg as every count's Regularized-mode picture: its default picture in its canonical pose, for all 324 counts. After #756 merged main, the nine addresses are declared again and serve the adopted house in canonical pose, and CI is green at 7bc4cae11. Option (b) is not applied. Closing.
