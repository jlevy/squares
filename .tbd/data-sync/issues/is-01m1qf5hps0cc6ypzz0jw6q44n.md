---
type: is
id: is-01m1qf5hps0cc6ypzz0jw6q44n
title: "Certificate page: footnote popovers stay put on the page, not on the viewport"
kind: bug
status: closed
priority: 2
version: 3
labels:
  - explainer
  - pr-79
  - kpress
dependencies: []
parent_id: is-01m1pnpwvpjydts81pffmp1nt7
created_at: 2026-09-05T00:23:19.512Z
updated_at: 2026-09-05T01:15:16.558Z
closed_at: 2026-09-05T01:15:16.557Z
close_reason: Commit b5e81669.
resolution: null
duplicate_of: null
---
Review feedback on PR #79: kpress positions a footnote popover in viewport coordinates, appended to body, so it holds a screen position while the page scrolls under it. It should sit at a fixed place on the page beside its reference. Fixed in kpress on the vendored branch; the page picks it up through the render-time bundle.
