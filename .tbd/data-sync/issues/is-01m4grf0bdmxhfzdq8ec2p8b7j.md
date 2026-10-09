---
type: is
id: is-01m4grf0bdmxhfzdq8ec2p8b7j
title: Unify PDF text colors and information-block spacing
kind: task
status: in_progress
priority: 2
version: 5
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-09T16:38:11.050Z
updated_at: 2026-10-09T17:17:17.826Z
started_at: 2026-10-09T16:38:41.898Z
---
Apply the latest print-only refinement systematically to both n=324 and n=100 PDFs: render the title and any retained subtitle in gray, make all remaining explanatory/legend/credits/closing text black, and use consistent whitespace between information blocks, including before Best packings due to. Preserve semantic result/angle/contact marks, the latest printable unlinked closing text and consistent typography, n=324 complete triangle layout and n=100 Grid layout. Keep the previously removed 324 subtitle removed. Regenerate both PDFs through maintained producers, inspect actual PDF text colors and block geometry and preview the resulting exports, then include the change in PR474 with current review and CI. Coordinate disjoint source ownership with think-e49r.

## Notes

Latest superseding print style: title, exact two-line problem definition and case numbers same gray; other ordinary text black, semantic recent-result red and angle/contact colors retained. Definition breaks after 'that can', proper italic s and n with roman parentheses, no final period; credits no final period. Shared four-plus-four legend with own count/100 or count/324, twenty unique construction credits newest first, common typography/leading and equal ink-to-ink block gaps. Grid100 keeps Grid, with plain black inline The Squares Project · github.com/jlevy/squares below title and other annotations/footer without duplicated reference. Triangle324 remains complete/right-aligned with upper-left information and two-line plain-black Project/address closing. Annotation slice23 focused tests passed8.81s, Ruff/BasedPyright clean; source proposes2400×3201 Grid and8347×6602 Triangle with current row pitches unchanged. Root rendered both retained-identity styling drafts via maintained APIs to external final/web-compact-20261009/print, inspected Poppler PNGs and revealed latest324 draft in Finder. These are previews, not qualified canonical exports. Independent gpt6-astra xhigh review found two Medium issues: stale Grid100 golden anchor filter/rigid count, and Arial-specific ink metrics fail three existing tests under actual LiberationSansBold nativeCairo fallback. Print author gpt6.1-sol xhigh addressing both with deterministic redistributable font custody; preserve measurement assertions. PDF row height adjustment0.25box and spacing reduction0.125box still await user direction/axis clarification; no elapsed-time assumption. Root owns docs/schema/layout records/pin/export generation, release qualification and PR474 publication. No scientific values or constructions change; no GitHub merge.
