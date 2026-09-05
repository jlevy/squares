---
type: is
id: is-01m1qf5hps0cc6ypzz0jw6q44n
title: "Certificate page: footnote popovers stay put on the page, not on the viewport"
kind: bug
status: open
priority: 2
version: 1
labels:
  - explainer
  - pr-79
  - kpress
dependencies: []
parent_id: is-01m1q0p63s2evef5mhkyn16e41
created_at: 2026-09-05T00:23:19.512Z
updated_at: 2026-09-05T00:23:19.512Z
---
Review feedback on PR #79: kpress positions a footnote popover in viewport coordinates, appended to body, so it holds a screen position while the page scrolls under it. It should sit at a fixed place on the page beside its reference. Fixed in kpress on the vendored branch; the page picks it up through the render-time bundle.
