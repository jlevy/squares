---
type: is
id: is-01m0nykzwb0b8kwndbvf27aefk
title: "Phase 5: compiled verification core (Rust), where the profile says"
kind: epic
status: closed
priority: 1
version: 10
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0nykzjp79rawg3g2x0hx2rf
child_order_hints:
  - is-01m0nym0hvhtp7kvr9n0j1ejjk
  - is-01m0nym0vyhgqmzz7rfv5st5f4
  - is-01m0nym15cp58q045s10cb3awb
  - is-01m0nym1fbdpy3pvjsnbrp55kb
  - is-01m0nym1ss6x3jvmj2brvaw7v5
  - is-01m0nym25asfyw6cwc3msk6e2c
  - is-01m0nym2fzzr8g8vr5j8sh9xzz
created_at: 2026-08-22T23:59:10.731Z
updated_at: 2026-08-23T05:26:48.338Z
closed_at: 2026-08-23T05:26:48.337Z
close_reason: "Superseded by think-u83z, the revised spec's Phase 5. This epic was the pre-revision 'Phase 1: verification core' and its label contradicted the spec after the plan was rebuilt around the quench spine; its seven children are re-parented to think-u83z, which carries the same work with the measured rationale. Reconciliation debt from review finding F-3, now closed."
---
The spine; everything depends on it and it is independently useful on landing -- it delivers the first exact re-verification of the record corpus. Done when verify() returns a certificate in under 10 ms for n=11 (vs 0.35 s today), Rust and the Python oracle agree everywhere, and every analytically-optimized record verifies exactly.
