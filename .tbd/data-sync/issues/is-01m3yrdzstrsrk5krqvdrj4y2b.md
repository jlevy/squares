---
type: is
id: is-01m3yrdzstrsrk5krqvdrj4y2b
title: "Verifier provenance: record who wrote each verifier and whether a confirmation reproduced the producer's code or re-implemented it"
kind: epic
status: closed
priority: 1
version: 2
labels:
  - verifiers
dependencies: []
created_at: 2026-10-02T16:51:17.946Z
updated_at: 2026-10-06T08:50:18.541Z
closed_at: 2026-10-06T08:50:18.541Z
close_reason: "Done: packing/frontier/verifiers.yaml and its schema, evidence entries naming their verifiers with relationship_to_generator, packing/devtools/backfill_verifier_relation.py and packing/tests/test_verifier_registry.py are on origin/main, from commit 8a6a265f2 'records: a verifier registry...'."
resolution: null
duplicate_of: null
---
Owner requirement: every confirmation states whether it re-ran the producer's own verification code or an independent implementation, and the records list each verifier by name as external or first-party. Deliverables: packing/frontier/verifiers.yaml registry (id, program, author, provenance external|first-party, language, method, digests, retained source); required evidence fields verifiers: [ids] and verifier_relation: producer-code|independent-implementation|shared-components (with independence_record / shared_components); check_results attribute beside the rung and rendered legend; a rendered verifier view; prose rule for the word 'confirmed'; re-runnable backfill tool packing/devtools/backfill_verifier_relation.py over all confirming evidence. Ships in the stacked PR on top of #298. After merging the import lanes, re-run the backfill on the merged evidence.yaml and require both fields on new entries.
