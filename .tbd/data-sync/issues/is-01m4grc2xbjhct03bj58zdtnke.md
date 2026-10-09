---
type: is
id: is-01m4grc2xbjhct03bj58zdtnke
title: Compact the web atlas and make Small the default
kind: task
status: in_progress
priority: 2
version: 4
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-09T16:36:35.370Z
updated_at: 2026-10-09T17:17:16.796Z
started_at: 2026-10-09T16:37:12.688Z
---
Apply the current web-only presentation request: remove dimension/GRID captions while preserving explicit grid segments and half-drawing gap; make Small the default in markup, CSS, head bootstrap, fallback, no-JavaScript and plain addresses; preserve explicit Medium/Large URL choices and accessible controls; compact uniform triangle row gaps to the existing cell-gap token. Shared legend counts use count/total, e.g. proved optimal (77/324), consistently with PDF labels. Print captions stay in the print renderer; concurrent PDF refinements are tracked separately under think-dwqg. Update maintained contracts/docs, manual preview and PR474 with focused browser checks, change-reachable push validation, independent review and current CI. Latest324 PDF revealed in Finder. No automated navigation of localhost8799 or GitHub merge.

## Notes

Web implementation is frozen after independent review: Small/Triangle default, print-only GRID captions removed from web, accessible first-grid segmentation retained, row gap8px desktop/5.6px phone and inherited image margins removed. Actual Small drawing pitch98.14px desktop and77.50px phone, down32px while drawing widths remain unchanged. Five counted legend items use canonical count/324 (77,292,32,22,297). Existing89 browser tests passed34.51s; Node40 and measurement16 passed; browser style/types clean. Maintained manual site build completed and actual served index markup has all five count/total labels. Independent strong-tier gpt6-astra xhigh delta review found no web findings; two print findings are assigned under think-dwqg. Two writers used moderate gpt6.1-sol xhigh; root owns publication and records. Evidence final/web-compact-20261009/web under the external evidence root. No source commit or push for this iteration yet, and prior PR474 CI is not qualification of this uncommitted slice. Root now running final overview/helper unit tests after count fractions; complete required push validation and current-head CI before closing.
