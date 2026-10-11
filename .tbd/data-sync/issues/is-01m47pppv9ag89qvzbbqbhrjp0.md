---
type: is
id: is-01m47pppv9ag89qvzbbqbhrjp0
title: "sqverify-fast tests: the metadata rule is held only loosely and only for format M (DR-4); tighten in a clean lane"
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m47hea1vkqx8h5wzdzcyqs5k
created_at: 2026-10-06T04:14:16.424Z
updated_at: 2026-10-06T04:14:16.424Z
---
DR-4 of docs/project/reviews/review-2026-10-06-sqverify-fast-declared-net-soundness.md (non-blocking, tests). In tests/declared_net.rs, metadata_may_restate_a_declared_net_but_never_change_it accepts any refusal whose message contains "net": {"D": "83/40000"} is refused by (b) and {"angle_count": 201} by (c), not by the metadata rule. In tests/adversarial.rs both variants of format_l_and_m_nets_cannot_be_overridden are refused before the metadata rule (format L by (d), format M by (c)). A mutant that disables the rule for format L alone passes every test. Fix: give each variant a net that meets (a) to (e) and match "may not change it", for format L as well as M. This edits the crate's tests (not source_sha256): do it in a lane that has not read the 5 October declared-net review's section "What the Authors' Code Shows" (lane R1 has), and record its reads in INDEPENDENCE.md.
