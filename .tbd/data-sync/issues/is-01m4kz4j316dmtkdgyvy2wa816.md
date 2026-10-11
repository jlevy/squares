---
type: is
id: is-01m4kz4j316dmtkdgyvy2wa816
title: Assess locked brace-expansion denial-of-service advisories
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-10-10T22:32:32.096Z
updated_at: 2026-10-10T22:32:32.096Z
---
npm ci/audit against the existing Squares package-lock on 2026-10-10 reports one high-severity development-tool dependency: brace-expansion versions 4.0.0 through 5.0.11, advisories GHSA-q2hr-2g5m-vwhr, GHSA-qhr7-859c-m2p7, GHSA-6j4f-fj2g-mc7p. Assess reachable use and update lockfile under supply-chain policy if warranted; no dependency versions changed during bead reconciliation. Found while provisioning locked validation tools externally for think-p2z4.
