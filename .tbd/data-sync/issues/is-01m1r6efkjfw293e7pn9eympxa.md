---
type: is
id: is-01m1r6efkjfw293e7pn9eympxa
title: Merge PR 79 and iterate until the explainer deploys correctly on GitHub Pages
kind: task
status: closed
priority: 1
version: 2
labels: []
dependencies: []
created_at: 2026-09-05T07:10:09.522Z
updated_at: 2026-09-05T08:08:50.077Z
closed_at: 2026-09-05T08:08:50.077Z
close_reason: "PR 79 merged at f060b1d7 (merge commit) after CI green on 719fe43b (validate, packing-required, macos-portability, build). The Certificate page workflow ran build and deploy green on main in 35 s on the first push. https://jlevy.github.io/squares/ serves the page: HTTP 200, 1,107,344 bytes, byte-identical to the local render; known-best-1-100.png and .pdf 200 and identical to the repository's. The deployed bytes driven in headless Chromium under /squares/ (served locally, since the sandbox proxy resets Chromium's connection to github.io): opens on 19/5, switch to 381/100 sets the hash, #19-5 switches back, 11 figures, 135 KaTeX spans, image loaded at 2400 px, PDF link 200, zero console errors, zero failed requests. No iteration was needed."
resolution: null
duplicate_of: null
---
Owner's direction 2026-09-05: once PR 79 is fully ready, merge it (merging is the debugging measure for the deploy, which runs only on main), then watch the Certificate page workflow's deploy job, load https://jlevy.github.io/squares/ and check the page: assets, both certificates, figures, the subpath. Fix and re-merge as needed via merge-upstream.
