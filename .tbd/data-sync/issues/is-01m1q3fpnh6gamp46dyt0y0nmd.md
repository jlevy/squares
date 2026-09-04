---
type: is
id: is-01m1q3fpnh6gamp46dyt0y0nmd
title: "kpress: expose the caps-label idiom as a class"
kind: task
status: open
priority: 3
version: 3
labels:
  - kpress-upstream
dependencies: []
parent_id: is-01m1q3fmvn9py28rcm0q3jadvk
created_at: 2026-09-04T20:59:09.361Z
updated_at: 2026-09-04T21:00:06.788Z
---
The uppercase section-label idiom (`--kpress-caps-transform`, `--kpress-caps-spacing`, `--kpress-caps-label-size`, sans family, medium weight) is re-declared at 5 sites in `components.css` and has no class a consumer can apply. The certificate page wrote its own `.caps` with the same five declarations.

Proposal: a `.kpress-caps` class in `components.css` carrying the idiom, applied at the 5 internal sites and documented for consumers.
