---
type: is
id: is-01m4ymtr7pa1sjzwftc1sjrbkt
title: "Validation (#610, think-ribz): full zm_mixed.py pass over all 160,000 D4 roots of the s(95) cover, about 190 CPU-h, held over the 40 CPU-h cap"
kind: task
status: open
priority: 3
version: 4
delegate: null
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-15T02:04:03.701Z
updated_at: 2026-10-31T05:02:27.259Z
started_at: 2026-10-31T05:00:30.201Z
---
Held validation item for the #610 import (think-ribz): zm_mixed.py alone over the whole D4 region of the s(95) cover, the exact-rational second route the source has not run.

## Validation
- Claim: s(95) >= 10 (hence s(95) = 10 with the grid), by bengreff/s95-certificate at dd7297d06adc664268c65005369b895e4ded7547, cover/s95_cover_v2.txt.gz (unpacked SHA-256 8b2d2152867585c82920bc90c6c3ec2a2458ef2ba57311ccd7dd436d1344cb7c), retained in packing/resources/web/bengreff-s95-certificate-2026-10-15/. Checker: Evan Daniel's zm_mixed.py ee3e2915 with mixed_cover.py bb89de15 and zeromargin.py 640fe453, from the retained evand packets of 26 and 28 September (the digests the source's verify.sh pins).
- Run: stage the three checker files and the unpacked cover in scratch as receipts/programs/run_zm_mixed.sh does, then from the checker directory: python3 -I -u zm_mixed.py cert COVER --d4 --cert-mode --disj --chain-from 0 --pitch 1/20 --ubins 16 --depth 24 --nproc P --resume OUT/zm_full.jsonl --manifest OUT/zm_full_manifest.json, under devtools.replay_receipt; it resumes from the .jsonl after an interruption. Rerun any root left uncertified alone at greater depth (the source's verify.sh --full-zm pattern: --cx-lo .. --u-hi and --depth D, own --resume file). Then the source's tools/check_full.py with K=10 (read first, run with -I from scratch) and the packet's zm_records.py-style exact reader over all 160,000 cells; commit the records (gzip -9n over 1,000 lines) and receipts.
- Cost: about 190 CPU-hours, an estimate: the source's full pass for s(76) took 181 CPU-h for 129,600 roots (5.03 CPU-s a root, #594 comment of 14 October), times 160,000 roots, times 0.855, this host's measured ratio to the source on the 304 s(95) sub-roots (receipts/n95_zm_mixed). About 8 days on one worker, 2 on four.
- Budget status: held. 190 CPU-h is above the owner's 40 CPU-h per-item cap.
- Possible subset under the cap: none completes a route. A stratified 1% sample (1,600 roots, about 2 CPU-h) would be a diagnostic only. Cheaper still: the author offered on #610 to run the pass; if he publishes the records, auditing them with check_full.py and an exact reader takes minutes, and a sample of his roots can be replayed under the cap.
- Depends on: the owner raising the cap or approving a subset, or the author's records. No code slice needed (the W7 slice of think-ribz would make the audit a repository tool).
- Done when: every one of the 160,000 D4 roots is certified (UNCERT 0, empty unc) in the full run or a deeper rerun with the same checker digests, cover digest and settings apart from depth and region; check_full.py prints OK; receipts committed on the bead's branch; an evidence entry for the exact-rational route (performed_by repository, same-implementation) cited beside T-NNN's rung.
- What it would raise: no rung by T-184's precedent; C3 needs the D4 composite (zmx2 + zm_mixed on the 304 sub-roots) as evidence and a review. It would give the lower half a second machine route in exact arithmetic that does not rest on zmx2's binary64 enclosures, recorded beside the rung (result-import.md: a second route is not a condition of C3), as T-066's next_rung describes for s(59).
- Machine note: CPU only, about 200 MB per process; shares the host with a gate at one or two workers.

## Notes

2026-10-31 bold-ritchie-l5 (intake pass of 31 October, epic think-3guf, lane L5): the sweep read #610 in this bead's title as its blocker, and #610 has closed. That was never the wait. The full zm_mixed.py pass is priced at about 190 CPU-hours, above the owner's standing 40 CPU-hour cap per item (think-lh7d), and it stays held on that cap. It resumes when the owner raises the cap for it or approves a subset (a stratified 1,600-root sample at about 2 CPU-hours would be a diagnostic only), or when the author publishes his records, which an audit with check_full.py and an exact reader would take minutes to read. Nothing was run.
blocked_on: the owner's word on the 40 CPU-hour cap (raise it for this item, or approve a subset), or the author's published zm_mixed records (no issue or bead tracks either)
