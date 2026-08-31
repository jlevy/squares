---
type: is
id: is-01m1112ee2hgxdnzhyn5shm0tf
title: Audit residual legacy SVG colors and prune diffuse visual prose
kind: bug
status: closed
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01m10nfh2zgk05e19d991mfhhy
created_at: 2026-08-27T07:13:40.289Z
updated_at: 2026-08-27T07:32:22.463Z
closed_at: 2026-08-27T07:32:22.462Z
close_reason: "Completed on PR #47 exact head e6f377c: exhaustively audited all 225 repository SVGs and every multi-panel/document image use; zero maintained outputs retain former-only colors, all 32,017 indexed fills across 211 SVGs now have a per-file contract regression, visual prose is concentrated in focused renderer docs, all eight generator ownership checks and local gates passed, independent review found no issues, and required Linux PR checks are green."
resolution: null
duplicate_of: null
---
Second closeout audit for PR #47. Inventory every maintained SVG and embedded side-by-side image, identify any output or panel still using the legacy palette, regenerate through its owning generator, and add a regression check that covers the missed surface. Audit packing Markdown for descriptive color commentary: retain one or a few focused explanations of hue=angle and shade=full-side contact count, and remove repeated or incidental descriptions elsewhere without changing research claims. Acceptance: exhaustive legacy-color scan is clear; side-by-side images are internally consistent; focused docs own the visual semantics; formatting, generator checks, visual QA, and required PR CI pass.
