---
type: is
id: is-01m4vrwgar1ddwmmg41vszn983
title: Math preparation serializes an empty style attribute in either order, so the n = 11 explainer's twin renders can differ
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-10-13T23:17:12.152Z
updated_at: 2026-10-13T23:17:12.152Z
---
The Certificate page workflow's prepare step renders packing/site/papers/n11-lower-bounds-explainer.html twice concurrently and diffs them. On PR #578 head b80b19d01 (run 38483004586, job 115590035457) line 1350 differed only in attribute order on the inline math span for 'n' after 'The target': one render wrote aria-hidden="true" style="" data-kpress-math-source=..., the other aria-hidden="true" data-kpress-math-source=... data-kpress-math-display="inline" style="". Same length (9148 chars), no content difference. The PR does not touch the renderer, vendor/kpress or the math preparation; the same check passed on main at 22:04Z and on the branch's earlier heads. Likely an asynchronous style set/clear in the browser preparation racing serialization. Fix: canonicalize attribute order (or drop empty style) before writing, or make the preparation set style synchronously.
