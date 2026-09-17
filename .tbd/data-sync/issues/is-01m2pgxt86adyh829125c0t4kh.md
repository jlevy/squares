---
type: is
id: is-01m2pgxt86adyh829125c0t4kh
title: The published page shows no link preview when shared on X
kind: bug
status: open
priority: 1
version: 1
labels:
  - explainer
  - pages
dependencies: []
created_at: 2026-09-17T01:50:30.661Z
updated_at: 2026-09-17T01:50:30.661Z
---
Reported 2026-09-16: https://jlevy.github.io/squares/ sent in an X (Twitter) DM rendered no social card, although sharing worked previously. think-95aa (closed 2026-09-05) added the Open Graph and Twitter card set with the 1x atlas PNG as the share image, and noted X's 4096x4096 image cap. Determine whether the live head tags, the share image (URL, status, size, dimensions) or the generator regressed, find the regressing commit, fix it with a test on the generated head, and verify the deployed page with a Twitterbot fetch.
