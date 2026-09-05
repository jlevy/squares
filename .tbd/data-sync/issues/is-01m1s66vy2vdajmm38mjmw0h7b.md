---
type: is
id: is-01m1s66vy2vdajmm38mjmw0h7b
title: "Explainer and atlas: one accent everywhere, no link blue; atlas URL in title ink"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-09-05T16:25:14.434Z
updated_at: 2026-09-05T16:25:22.449Z
closed_at: 2026-09-05T16:25:22.449Z
close_reason: "Done in 3bd273e6. Root cause found in a browser rather than guessed: the tooltip's border-left computed to oklch hue 254.7 (blue) while the accent is hue 186.4, because kpress declares --kpress-doc-link on :root, .kpress and per theme/palette attribute selectors, all of which outrank the body the page set it on, and the popovers carry .kpress-tooltip plus their own resolved-theme attribute. The token is now redeclared at those same scopes. Verified by sweeping every element's computed color, borderLeftColor, backgroundColor, fill, stroke and textDecorationColor with a popover open: nothing lands in the blue band. Atlas repository URL moved from PAPER_THEME.muted to PAPER_THEME.ink."
resolution: null
duplicate_of: null
---
Owner 2026-09-05: the footnote tooltip's left border accent should be the document's green accent, the design-system variables should be used consistently, and the generic blue link colour should appear nowhere. Also the GitHub URL under the atlas title should be black rather than grey.
