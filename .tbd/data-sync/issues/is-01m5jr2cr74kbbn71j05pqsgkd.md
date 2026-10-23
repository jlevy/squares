---
type: is
id: is-01m5jr2cr74kbbn71j05pqsgkd
title: "Site navigation performance: faster page-to-page transitions"
kind: epic
status: open
priority: 1
version: 12
labels: []
dependencies: []
child_order_hints:
  - is-01m5jr2d9y616b6b95kt3dpmry
  - is-01m5jr2dx0je5fepe3c93n3q7r
  - is-01m5jr2efbxnghkkqh0fncahw8
  - is-01m5jr2f0ysaefsw819esatgvn
  - is-01m5jr2fjt4wp8zryw7wceq0hw
  - is-01m5jr2g54r568rrq3yg3dwj6w
  - is-01m5jr2gpy49zr55rdh1cqaghc
  - is-01m5k1wqbd2k8scqht90p33qm3
  - is-01m5k62y0meb5c72fjzjqd97h2
  - is-01m5k93vknqqa0ve9qvbvpjv8y
  - is-01m5kd967v3k8pnx1mh9c6bpxn
created_at: 2026-10-22T21:25:28.455Z
updated_at: 2026-10-23T03:36:11.259Z
---
Measured 2026-10-22 against squaremath.org and a local mirror in headless Chromium 141. A nav click is a full document load; on heavy pages (results 22,560 elements, atlas 13,726) the new page is busy 1.0-1.5 s after the click, mostly style recalc and layout, not script. Two quick fixes land first (headroom scroll-padding guard, prerender on hover); the rest are follow-up PRs. Warm-cache click-to-settled: index->results ~1,240 ms as deployed, ~800 ms with the headroom fix, ~110 ms with fix + prerender.
