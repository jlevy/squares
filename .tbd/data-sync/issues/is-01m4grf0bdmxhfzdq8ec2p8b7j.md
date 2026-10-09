---
type: is
id: is-01m4grf0bdmxhfzdq8ec2p8b7j
title: Unify PDF text colors and information-block spacing
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
created_at: 2026-10-09T16:38:11.050Z
updated_at: 2026-10-09T16:54:01.884Z
started_at: 2026-10-09T16:38:41.898Z
---
Apply the latest print-only refinement systematically to both n=324 and n=100 PDFs: render the title and any retained subtitle in gray, make all remaining explanatory/legend/credits/closing text black, and use consistent whitespace between information blocks, including before Best packings due to. Preserve semantic result/angle/contact marks, the latest printable unlinked closing text and consistent typography, n=324 complete triangle layout and n=100 Grid layout. Keep the previously removed 324 subtitle removed. Regenerate both PDFs through maintained producers, inspect actual PDF text colors and block geometry and preview the resulting exports, then include the change in PR474 with current review and CI. Coordinate disjoint source ownership with think-e49r.

## Notes

Latest superseding print style: title, two-line problem definition and case numbers all use the same gray; all other ordinary text black, with semantic recent-result red and tilt/contact colors preserved. Exact problem break: The square packing problem asks for the side s(n) of the smallest square that can / hold n unit squares, where the squares are free to rotate but cannot overlap, with proper math and no final period. No final period on credits. Use shared annotations/order/type across324 and100; count/depicted-total on five counted legend items; actual-Cairo ink centering for boxed glyphs; consistent block gaps. Grid100 retains its layout, puts annotations in footer and plain black inline The Squares Project · github.com/jlevy/squares below its title without duplicated footer reference. Triangle324 retains upper-left information and its current project closing. PDF row height adjustment0.25box and spacing reduction0.125box await user direction/axis clarification. Root owns docs/official layout records/pin/export generation and PR publication; no scientific values or constructions change. Web/PDF implementation runs in two disjoint moderate-tier agents; a third administrative lane was unavailable due to tool thread limit, so root handles generation planning.
