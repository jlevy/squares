---
type: is
id: is-01m4ez392javr049tjjg63hkcp
title: "n17 PR404 CI: isolate malformed-input CLI controls from producer imports"
kind: bug
status: open
priority: 2
version: 1
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
delegate: sol-merge-engineering
labels:
  - n-17
  - ci
dependencies: []
parent_id: is-01m4eq9mdaejkedd1b09qqn09p
created_at: 2026-10-08T23:55:37.937Z
updated_at: 2026-10-08T23:55:37.937Z
---
Current-source hosted Packing runs40437860039766,45437860039856 and46137860039390 all fail12 shardB controls: ten nested descriptor path/hash refusals expect "paths and digests" but encounter process-wide "producer/kernel/root import in full-square checker"; two gzip EOF CLI refusals likewise encounter the independent-checker purity guard first. The same controls passed as part of366 affected controls run in separate module processes; that retained result did not qualify a combined shard.

Fix test/CLI control isolation so the real submitted-input boundaries are reached in a clean checker process even when producer tests have been collected elsewhere. Preserve mathematical import-purity guards, input refusals and all resource caps; do not skip controls or accept the purity error as their expected outcome. Owned tests: packing/tests/test_check_n17_full_square_partner_coupling.py and test_verify_n17_conditional_owned_hull.py. Any production change needs a demonstrated boundary cause and separate review.

Original/integrated root head18e3a6f4f20f534e80074131d4947c633cca5ef3; exact checkout62a361c8ca69ad672ad01a1600a9c719ada00328/tree720674ded803eefded7dc30fc71a729afaee4f12. Evidence: attic/n17-merge-readiness-20261008/final-source-qualified-hosted-ci-diagnosis.json and pr{404,454,461}-packing-current-suite-b.log. No cap/snapshot worker or rerun launched for diagnosis. Parent CI qualification remains under think-0m0x.
