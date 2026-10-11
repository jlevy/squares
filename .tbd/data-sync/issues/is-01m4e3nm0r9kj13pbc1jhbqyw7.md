---
type: is
id: is-01m4e3nm0r9kj13pbc1jhbqyw7
title: Reconcile postdeployment result-record links after PR395 static page publication
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-10-08T15:56:18.838Z
updated_at: 2026-10-08T15:56:18.838Z
---
Main913781538 published/deployed the static site, but postdeployment run37801347555 job113396572976 failed verify-deployment: index.html and all-results.html lack the old evidence.yaml/results.yaml record-link strings for all116 result rows. Main packing validation37801347513 passed. Diagnose desired permanent-page/proof-record navigation contract, repair real navigation or checker compatibility with retained meaningful controls, and verify actual deployed pages. Do not treat this publication failure as a scientific failure or weaken proof/navigation checks. Captured during tracker405 reconciliation; no repair executed. Evidence https://github.com/jlevy/squares/actions/runs/37801347555/job/113396572976 .
