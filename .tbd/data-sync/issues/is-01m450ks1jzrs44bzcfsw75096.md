---
type: is
id: is-01m450ks1jzrs44bzcfsw75096
title: "Import Francisco Couzo: new records at franciscouzo/square-packing 6042c56 (2026-10-03, no issue)"
kind: task
status: closed
priority: 1
version: 6
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m44qz0rxvkakmyqaj7qdgagv
hold: null
hold_until: null
created_at: 2026-10-05T03:09:42.834Z
updated_at: 2026-10-05T07:19:52.438Z
started_at: 2026-10-05T03:10:47.110Z
closed_at: 2026-10-05T07:19:52.438Z
close_reason: "Done in jlevy/squares#353 / #359 (merged 2026-10-05)"
resolution: null
duplicate_of: null
---

## Notes

Stage 1 triage (2026-10-05, lane couzo, branch claude/ecstatic-pascal-pothtx-couzo).

Pin: franciscouzo/square-packing 6042c56b43b64c09fe5a32c64879e698f399beaf, committed 2026-10-03T12:33:31Z ("new records"), one commit past T-056's pin f3c5a52. Changes n208/209/228/263/272/303/306 (.txt and .svg) and the README table; no new count, no LICENSE, no AI statement in the repository.

Claim map (Couzo new side / record before = Couzo f3c5a52 T-056 printed side / retained Kingbird 2026-09-30):
- 208: 14.926534459703511 / 14.937018796984567 / 14.93776656277905
- 209: 14.953939011860642 / 14.955041639430016 / 14.95861500087481
- 228: 15.604602454552252 / 15.604638007678682 / 15.60902282132495
- 263: 16.742270262031791 / 16.742280159187313 / 16.74264068711928
- 272: 16.968165867864400 / 16.968279785326896 / 16.96971602419903
- 303: 17.924341009860250 / 17.924349265547932 / 17.93125509556197
- 306: 17.963438139777139 / 17.963449907261179 / 17.96913960675661
All seven improve the record; Couzo (T-056) held all seven. Casson's sides (2026-09-23) are larger at all six he reports. No claim at n = 69, 83, 87.

Register action: a later release that lowers an earlier entry's values -> new entry (T-092 on this branch), T-056 keeps its claim; case records decide which is current.

Validation plan: T-056's two routes on the seven new poses, minutes: devtools.upper_bound_packets certify (robust-rational promotion + independent Fraction checker, ~15 CPU-min) and devtools.upper_bound_intervals certify (seconds). Both exist; the tooling needs a second Couzo source (W7 slice inside this import). Kingbird live page denied by the proxy (403), so no live-catalogue receipt.

Stages 2-4 (2026-10-05, same branch):
- Stage 2: packet packing/resources/web/franciscouzo-square-packing-2026-10-03/ (facts for the seven, all 99 upstream files pinned by SHA-256, history; no raw bytes, no licence). Key [franciscouzo square-packing 2026-10-03], dated 2026-10-03. Tooling: upper_bound_packets Source gains layout/retrieved/control/supersedes; apply_upper_bound_packets chains a later registration over an earlier one at a count.
- Stage 4 replay (both T-056 routes): exact certify 264 s wall on 4 workers, all seven at centre dilation 1, both checkers pass; interval certify 1 s, all VERIFIED at 40 digits, agrees with exact at every count. Controls on n = 208 (side -1e-15, square 2 +1e-6, degrees) refused. Verified = printed at 228/272/303, +1 unit at 208/209/263, +2 units at 306 (conflict + mathematics blocker, as T-056 at 206/259/305).
- Stage 3: T-092 registered V3/C3 (derived from replayed-here exact-algebraic + interval-certified evidence with controls), S3 draft. Case records n-208..306 written by devtools.apply_upper_bound_packets; coverage source franciscouzo-square-packing-2026-10-03 with seven overrides, T-056's seven sides superseded.
- Still open in this bead: the stage 4 review lane (a mapped review of the seven certificates under docs/project/reviews/), not run in this lane; stage 7 has no issue to answer.

Committed 2026-10-05 on claude/ecstatic-pascal-pothtx-couzo (not pushed): 78dfeb79e (import, T-092) and 52951e145 (DATA_REVISION re-pin). Validation: --records fails only on register id contiguity (T-092 before T-088..T-091 merge); with T-092 renumbered to T-088 in a throwaway edit, check_results and --records pass and 399 targeted tests pass. --push (1575 s): contiguity, the two environmental test_fixed_core_packet* reaping tests, and two real findings fixed before the final commit (bound-citations.json stale; render-colors wrapped-frame count 36 -> 35 because n = 208 now carries 16 angle classes). Exact replay `upper_bound_packets check --replay --source franciscouzo-square-packing-2026-10-03 --workers 4`: 7/7 VERIFIED, regenerated identical, 91 s. Sweep after import: franciscouzo/square-packing no longer under Needs Action (head 6042c56 is pinned).

Remaining: the stage 4 review lane (mapped review of T-092 under docs/project/reviews/). No issue asked, so no answer is owed; issue #227 (T-056) has no reply due by the requests rule since T-056's id and rungs are unchanged.
