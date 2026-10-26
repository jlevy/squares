---
type: is
id: is-01m5tv6pzmhzj7t4pgtwgdk8m9
title: Decide T-247's route A configuration at 297 on exact_verify (held over the cap), then its stage 4 review and adoption
kind: task
status: in_progress
priority: 2
version: 3
delegate: w-exact-804-1026
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-26T00:54:11.188Z
updated_at: 2026-10-26T10:51:39.268Z
started_at: 2026-10-26T10:51:39.267Z
---
Decide route A's exact configuration of T-247 (issue 804's exact side at 297, Hyukdong Kim) on sqpack.witness.exact_verify, then the stage 4 review and the house adoption at 297 that the house rule takes once the review accepts. Route B (the author's attachment, s297-exact-configuration.zip, CC0, SHA-256 e08b5d0a...47a7) is a second route, recorded beside the rung when the file is reachable.

## Validation
- Claim: s(297) <= S*, the only real root of the degree-21 polynomial of issuecomment-6397593690. Certificate: route A's exact configuration packing/resources/web/hyukdongkim-s297-2026-10-25/facts/route-a-n297.json.gz (built by devtools.build_field_configuration from T-174's certificate; all 1,208 contacts identities in K, P297(S) = 0 in K). Checker: sqpack.witness.exact_verify over K through devtools.algebraic_witness_reports' jobs.
- Run: from packing/, `bash resources/web/hyukdongkim-s297-2026-10-25/route-a.sh decide` with the project interpreter on PATH (three jobs: positive, duplicate-square-overlap, square-translated-outside-container); then register the replay evidence on T-247 (C3), a certificate-citation deferral until adoption, the stage 4 review (tbd-strong-max), and select_houses/adopt_houses at 297 (algebraic writer, think-ot5c; regularization owed under think-mbdw).
- Cost: about 2.5 CPU-hours a job, 7.5 for all three, up to 12. Basis: measured on 2026-10-26 on a shared 4-core host, the positive ran 89.8 CPU-min and each control 48 CPU-min without finishing (stopped at the 5 CPU-h item cap); the degree-squared scaling from T-193's 302 at degree 7 (231 s) predicted 0.56 h a job and is low by more than 2.7x.
- Budget status: held (over the 5 CPU-h item cap for all three).
- Possible subset under the cap: the positive job alone, about 2.5 CPU-h (up to 4). The two controls could be made cheap by an early-exit mode in the exact verifier (stop at the first refused pair or wall), a tooling slice.
- Depends on: the PR that registers T-247 (think-ozx8) merged; the owner's word on the cap.
- Done when: decide-*.json receipts in the packet show the positive VALID with every pair decided and both controls refused, the replay evidence is registered on T-247, and the review and adoption follow.
- Machine note: single-threaded Python jobs, about 0.3 GB each; run on a quiet host, since a loaded host roughly halves their rate.
