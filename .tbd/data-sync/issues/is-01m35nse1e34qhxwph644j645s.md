---
type: is
id: is-01m35nse1e34qhxwph644j645s
title: Fix threshold net-refinement provenance before the next frozen rung
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-22T23:04:06.435Z
updated_at: 2026-09-22T23:04:06.435Z
---
devtools.measure_threshold_net_refinement hard-codes derived_from to cases/n11_threshold_certificate/certificate.json while computing the weight multiplier relative to its actual input. The frozen T-033 net2880 bytes disclose this mismatch and remain digest-bound; fix the producer and add a regression check before any later certificate is frozen. Do not rewrite the retained T-033 bytes.
