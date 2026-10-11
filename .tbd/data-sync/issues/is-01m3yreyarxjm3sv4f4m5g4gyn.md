---
type: is
id: is-01m3yreyarxjm3sv4f4m5g4gyn
title: "Verifier provenance: record who wrote each verifier and whether a confirmation reproduced the producer's code or re-implemented it"
kind: epic
status: closed
priority: 1
version: 2
labels:
  - verifiers
dependencies: []
parent_id: is-01m3yrdxte02c7bnygkke34ct4
created_at: 2026-10-02T16:51:49.208Z
updated_at: 2026-10-03T22:39:33.826Z
closed_at: 2026-10-03T22:39:33.825Z
close_reason: "Landed on main: packing/frontier/verifiers.yaml (75 verifiers), evidence fields verifiers/relationship_to_generator on 210+ entries, check_results attribute. Census evidence follow-up is think-3ok2."
resolution: null
duplicate_of: null
---
Owner requirement: every confirmation states whether it re-ran the producer's own verification code or an independent implementation, and the records list each verifier by name as external or first-party. Deliverables: packing/frontier/verifiers.yaml registry (id, program, author, provenance external|first-party, language, method, digests, retained source); required evidence fields verifiers: [ids] and verifier_relation: producer-code|independent-implementation|shared-components (with independence_record / shared_components); check_results attribute beside the rung and rendered legend; rendered verifier view; prose rule for the word 'confirmed'; re-runnable backfill tool packing/devtools/backfill_verifier_relation.py. Ships in the stacked PR on top of #298. After the import lanes merge, re-run the backfill on the merged evidence.yaml; new entries carry both fields.
