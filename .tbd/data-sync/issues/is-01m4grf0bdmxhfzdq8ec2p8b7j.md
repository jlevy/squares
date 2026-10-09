---
type: is
id: is-01m4grf0bdmxhfzdq8ec2p8b7j
title: Unify PDF text colors and information-block spacing
kind: task
status: in_progress
priority: 2
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-09T16:38:11.050Z
updated_at: 2026-10-09T16:43:26.484Z
started_at: 2026-10-09T16:38:41.898Z
---
Apply the latest print-only refinement systematically to both n=324 and n=100 PDFs: render the title and any retained subtitle in gray, make all remaining explanatory/legend/credits/closing text black, and use consistent whitespace between information blocks, including before Best packings due to. Preserve semantic result/angle/contact marks, the latest printable unlinked closing text and consistent typography, n=324 complete triangle layout and n=100 Grid layout. Keep the previously removed 324 subtitle removed. Regenerate both PDFs through maintained producers, inspect actual PDF text colors and block geometry and preview the resulting exports, then include the change in PR474 with current review and CI. Coordinate disjoint source ownership with think-e49r.

## Notes

Additional direct user refinements: share annotation text/construction across both PDF layouts; put the n=100 Grid problem/legend/credits/diagram/date-version details in its footer and the plain black inline The Squares Project · github.com/jlevy/squares below its title, without duplicating that reference in its footer. Retain the 324 upper-left information arrangement. Adjust PDF row height by about 0.25 container-box height and inter-item/row space by about 0.125 box size consistently across both PDFs; direction and spacing axis are awaiting the user’s answer because the row-height verb was missing. Center the PDF boxed status glyph ink, including =, inside their boxes. Implementation is delegated to atlas_print_consistency; root owns docs, official layout-record/pin/export generation and publication. Finder reveal of the latest 324 PDF succeeded.
