---
type: is
id: is-01m1sj8xgrbn08w9tkpx6r5brq
title: "Explainer: Open Graph and social metadata, with the atlas PNG as the share image"
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-09-05T19:56:04.504Z
updated_at: 2026-09-05T20:39:14.460Z
closed_at: 2026-09-05T20:39:14.460Z
close_reason: "Full Open Graph and Twitter card set added with a canonical link, every value substituted from the certificate. Share image is the 1x atlas PNG: the 2x export is 4800x5792 and X caps a card image at 4096x4096, so it exceeds that on both axes and would not render. The canonical link was the one thing the self-containment refusal caught; widened to exempt exactly rel=canonical, with five other rel values still refused and each pinned by a test."
resolution: null
duplicate_of: null
---
Check the page's head for correct og:title, og:description, og:image, og:url, og:type and the Twitter card equivalents, plus a canonical link. The share image should be the atlas PNG so a shared link previews the hundred packings. og:image must be an absolute URL and the file must be reachable from the deploy; note the page is self-contained, so the image reference is the one thing that legitimately points outward.
