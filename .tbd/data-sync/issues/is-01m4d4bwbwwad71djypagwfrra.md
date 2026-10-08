---
type: is
id: is-01m4d4bwbwwad71djypagwfrra
title: "n17 native verifier: publish receipts atomically before operational adoption"
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/reviews/review-2026-10-07-n17-pr410-integration.md
labels: []
dependencies: []
parent_id: is-01m4d110wy172kc3ncrnqvbqp3
created_at: 2026-10-08T06:49:13.851Z
updated_at: 2026-10-08T06:49:13.851Z
---
Senior PR410 review C1 Medium: current Rust write_receipt uses direct fs::write, as the Python oracle does. Interruption or disk exhaustion can truncate an existing valid output. Before operational adoption, use same-directory temporary publication and platform-correct atomic replace, with injected write/rename interruption controls preserving the old receipt. Partial JSON cannot pass current admission; defer for additive UNADOPTED merge, no production/admission change in PR410 preparation.
