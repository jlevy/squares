---
type: is
id: is-01m4d4bwbwwad71djypagwfrra
title: "n17 native verifier: publish receipts atomically before operational adoption"
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/reviews/review-2026-10-07-n17-pr410-integration.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4d110wy172kc3ncrnqvbqp3
hold: null
hold_until: null
created_at: 2026-10-08T06:49:13.851Z
updated_at: 2026-10-08T19:06:18.154Z
started_at: 2026-10-08T16:08:27.745Z
closed_at: 2026-10-08T19:06:18.152Z
close_reason: "Atomic-publication source and Linux qualification captured in PR #453 with green current-head required CI and bounded Astra review. Windows execution and full verifier adoption remain separate."
resolution: null
duplicate_of: null
---
Senior PR410 review C1 Medium: current Rust write_receipt uses direct fs::write, as the Python oracle does. Interruption or disk exhaustion can truncate an existing valid output. Before operational adoption, use same-directory temporary publication and platform-correct atomic replace, with injected write/rename interruption controls preserving the old receipt. Partial JSON cannot pass current admission; defer for additive UNADOPTED merge, no production/admission change in PR410 preparation.

## Notes

PR #453 at b1948591b00091de2daf01532af516b723206f9e captures same-directory staging and platform replacement of complete native receipt bytes. Handled write/rename failures preserve the previous destination and report cleanup failures. Hosted Linux controls at 9aa4a65f passed all six named receipt tests, 28 unit tests, one compiled-world control and Rust floor in 74.72 seconds against the unchanged 90-second ceiling. The corrected head's Packing, Pages and mergeability aggregates all passed, observed October 8 at 19:01:34 UTC. Final bounded Astra source review found no blocking finding or changed mathematical acceptance predicate. Atomic visibility is distinct from power-loss durability; mode 0600, symlink replacement and abrupt-kill staging limits remain documented. Windows execution, Python-oracle atomic writes and full same-object ordinary-U parity/adoption remain separate obligations under think-kk7w; centered U/V/offset/hull-48 support is still unimplemented. No new admission, bound or verifier speedup is claimed. Bounded source and Linux qualification are complete on this draft; GitHub review and merge remain separate.
