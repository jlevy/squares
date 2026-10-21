---
type: is
id: is-01m5g28824ts9q4byp8ezh6sxf
title: Diagnose hosted T-037 mobile layout shift
kind: bug
status: closed
priority: 1
version: 5
delegate: about_profiles_implementation
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-21T20:25:42.722Z
updated_at: 2026-10-21T21:27:18.497Z
started_at: 2026-10-21T20:25:51.879Z
closed_at: 2026-10-21T21:27:18.497Z
close_reason: Fixed font-driven result-title wrapping in e2925e726. Local mobile CLS fell from 0.10275 to 0.00199; held-font and accessibility regressions passed. Hosted Pages run 39676438414 at e162a870a completed successfully, including overview job 119487793812, with the unchanged CLS limit. Final-head overall CI remains tracked separately.
resolution: null
duplicate_of: null
---
Pages run 39669145614, overview job 119462390704 at head 7b566ae73, reports result/t-037.html at 390px in light and dark with CLS 0.103 above the unchanged 0.1 limit. Timing exceedances are empty. Inspect retained layout-shift sources, reproduce through existing repository rendering checks, and repair actual geometry if needed without relaxing thresholds. New head c3e8f1cc has only URL-date changes; CI is being monitored independently. No source commit or push before reporting evidence.

## Notes

Root cause reproduced from hosted run 39669145614/job119462390704 and local unchanged c3e8f1cc: fallback heading math fit beside T-037, then the loaded font widened it and wrapped it, moving the following header32.765625px. Local before CLS0.102751115 in all3runs for each390px theme. Hosted rerun39669953858/job119465269629 reproduced0.103.

Implemented one H1 with existing id and ID/headline spans; screen<=40rem places only record ID on its own line. Desktop and print remain inline. Heading math resets inherited caps/tracking, preserving actual s/S distinction and semantic MathML. No threshold change, fixed-height reservation, hidden content, font preload expansion or runtime JavaScript.

Validation:18focused tests passed32.41s, including all224titles preserving prose and exact semantic MathML. FinalCSS result-popover module16passed15.80s. Held-font title geometry stable at320/390/640/641/1280; long formulaT057/plainT186 stay withinviewport. Existing fetched-title/accessibility tests pass. Ruff/format,BasedPyright andBiome zero findings; gitdiff--check clean. Astra final_profiles_senior_review found no actionable finding.

Exactfinal immutableasset normalcheck: ci-t037-cls-preview-final.json: T037 mobileCLS0.001994234, desktop0.000621884, each3runs/theme,0unreadable math. Peer Pages surfaces index/atlas/case11/results: ci-t037-cls-overview-peers-final.json,16scenarios,0failures, maximumCLS0.000131536. Timing report-only matches Pages policy and leavesCLS0.1enforced.

Refreshed all224canonical results plus656HTML stylesheetreferences in site-integrated-reviewed. New immutable assets site.2bb0bcf7fcdd16bc.css and site-result.781c1f00b515b697.css. T174277849bytes below300000 unchangedlimit. LiveHTTP200 for http://127.0.0.1:8790/result/t-037.html?cls=think-i2l2 and bothassets200.

No source commit/push by worker. Ready for coordinator normal-hook commit and final-head CI. Original failing artifacts and before/candidate/final JSON reports retained under /Volumes/spud-ext2/agent-scratch/about-profiles-20261020/.

Hosted acceptance confirmed on 2026-10-21: Pages run 39676438414 completed successfully at e162a870a899a61cc77cd47fa2f56c0ff388c8ea, an ancestor of current e3e33171bf1d687190cc957a40e25fbbc9dbb23c. The overview job 119487793812, which enforces T-037 layout shift at 390px in light and dark, passed with the unchanged 0.1 CLS limit. Run: https://github.com/jlevy/squares/actions/runs/39676438414 ; overview: https://github.com/jlevy/squares/actions/runs/39676438414/job/119487793812 . The fix is in commit e2925e726. Local before/after and regression receipts remain above. Closing only this resolved CLS bug; final-head overall CI and the profile integration parent remain separate.
