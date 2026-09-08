---
type: is
id: is-01m1yzd0n91ataqxvk8fbpdg7w
title: Clarify the one-minute and three-minute verifier timings
kind: task
status: closed
priority: 2
version: 4
labels: []
dependencies: []
parent_id: is-01m1ywjmdsmsjnxqbhd56er89j
created_at: 2026-09-07T22:21:42.427Z
updated_at: 2026-09-07T22:34:53.144Z
closed_at: 2026-09-07T22:34:53.144Z
close_reason: Completed in PR117 at f4e4bd4a. All 45 local pre-push steps and all required hosted checks passed, including the paper build. Independent review accepted the changes; browser and PDF previews were regenerated, inspected, and reopened.
resolution: null
duplicate_of: null
---
Audit the recorded verifier runtimes and clarify the explainer: the current pinned minimal_verify.py checker is about a minute, while the embedded verify_claim.py implementation is about three minutes. Make the reader-facing timing references consistent, keep implementation and historical measurement details in a footnote, and preserve generated certificate variants.

## Notes

Audit accepted by paper_audit. The one-minute and three-minute figures describe separate implementations, not a demonstrated recent speedup: minimal_verify.py recorded at 47.5-67.0 seconds on 2026-09-05; verify_claim.py at 175 seconds on 2026-09-04. Proof card lines 65-76 and the prior C6 same-machine review corroborate this. Main text now consistently links minimal_verify.py and says about a minute. A footnote links recorded runs and identifies the slower embedded checker. All 43 explainer tests pass (5.75 seconds), including single-certificate and comparison variants. Browser opening and claim wording verified; PDF pages 1, 13, and 15 visually reviewed and opened in Preview. Final pre-push check and PR117 update pending.
