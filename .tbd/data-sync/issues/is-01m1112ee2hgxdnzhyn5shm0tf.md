---
type: is
id: is-01m1112ee2hgxdnzhyn5shm0tf
title: Audit residual legacy SVG colors and prune diffuse visual prose
kind: bug
status: in_progress
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m10nfh2zgk05e19d991mfhhy
created_at: 2026-08-27T07:13:40.289Z
updated_at: 2026-08-27T07:13:45.089Z
---
Second closeout audit for PR #47. Inventory every maintained SVG and embedded side-by-side image, identify any output or panel still using the legacy palette, regenerate through its owning generator, and add a regression check that covers the missed surface. Audit packing Markdown for descriptive color commentary: retain one or a few focused explanations of hue=angle and shade=full-side contact count, and remove repeated or incidental descriptions elsewhere without changing research claims. Acceptance: exhaustive legacy-color scan is clear; side-by-side images are internally consistent; focused docs own the visual semantics; formatting, generator checks, visual QA, and required PR CI pass.
