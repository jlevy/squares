---
type: is
id: is-01m1stdrm8cqae7z20qng5xtv9
title: "Explainer: the certificate chooser drops focus and the page has no live regions"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-05T22:18:31.944Z
updated_at: 2026-09-05T22:18:31.944Z
---
Measured 2026-09-05. Focus the Tighter button in Figure 5 and press Enter: the switch is correct (all four figures swap, aria-pressed flips on all eight buttons, the hash becomes #381-100) but document.activeElement becomes body. show() sets hidden on the subtree containing the button just pressed and never moves focus to its twin, which show() already locates for its scroll adjustment. Chrome's sequential-focus fallback softens it -- one Tab landed on #kslider-381-100 -- but Shift+Tab is unanchored and screen-reader virtual focus is lost.

Compounding it: [aria-live], [role=status], [role=alert] match nothing on the page. Four figures change and a screen-reader user is told nothing; the same gap means no announcement when 'Scan this direction' rewrites the hint text or the slider moves the mass readout.
