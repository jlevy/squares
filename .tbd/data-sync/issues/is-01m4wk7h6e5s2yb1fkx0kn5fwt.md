---
type: is
id: is-01m4wk7h6e5s2yb1fkx0kn5fwt
title: "Import dostashev: s(176) <= 13.795872318437, s(211) <= 14.993694186584, s(241) <= 15.987134249051, s(304) <= 17.929427758076 (#575)"
kind: task
status: in_progress
priority: 1
version: 3
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-14T06:57:36.461Z
updated_at: 2026-10-14T07:18:39.571Z
started_at: 2026-10-14T06:57:49.305Z
---
https://github.com/jlevy/squares/issues/575 (2026-10-13T00:42:43Z; body edited 2026-10-13T04:13:29Z to add 304, comment of 04:13:31Z). dostashev/square-packing at b909e1b74cda50906e12b4373e010ddee39e47e4, records/n0176, n0211, n0241, n0304 (.sqcert, .sqpk). Stages 1-2 and the stage 4 replay through devtools.upper_bound_reports, intake lane ostashev of 2026-10-14.

## Notes

Issue: https://github.com/jlevy/squares/issues/575 (opened 2026-10-13T00:42:43Z by dostashev; body edited and title renamed 2026-10-13T04:13:29Z to add 304; one comment 2026-10-13T04:13:31Z by the author: "added s(304) <= 17.929427758076 ... The certificate commit is now b909e1b...; in it the 176, 211 and 241 files are unchanged (same SHA-256 as at b572f10)"; label intake added 2026-10-14T04:38Z).

## Stage 1 triage, 2026-10-14, intake lane ostashev (branch claude/wizardly-meitner-wqn4x3-intake-1014-ostashev from main aeef99ef0)

Pin: dostashev/square-packing b909e1b74cda50906e12b4373e010ddee39e47e4 (committed 2026-10-13T03:03:29Z), the head when cloned at 2026-10-14T06:54Z and the commit the edited issue names; its eight SHA-256 match the files there. First commits holding the bytes: 176 e54ac1b (2026-10-12T23:06:00Z), 211 and 241 b572f10 (2026-10-13T00:41:41Z), 304 b909e1b (2026-10-13T03:03:29Z). MIT licence.

Claims the release makes, and their register map:
1. s(176) <= 13.79587231843640726331185405391207744387, s(211) <= 14.99369418658324657063591818176125142354, s(241) <= 15.98713424905084041461665739745571396866, s(304) <= 17.92942775807517496566632613898911486244 (issue, 38 places rounded up; README 15 places). One new entry whose scope is 176, 211, 241, 304.
2. 211 "updates our T-149 entry with a different packing": a later release at a count an entry holds with another packing. By the stage 1 table, a new entry; T-149 keeps its claim and the case records decide which is current.
3. README at the pin: Couzo improved the author's 156 to 12.979165853835 and the author's first 176 to 13.807637227056. Couzo's claims (#561), not this source's: no entry here.
4. The commit rewrites #562's 129/204/303 and #528's 175/232/264 files in canonical form (883aa4b) at the same exact sides (measured here: equal). Pinned by digest only; no new claim.
5. KKT exact first-order optimum, two routes agreeing: author's local-optimality report, not registered.
6. Lineage: V-band merges by all-soft GPU re-hardening (soft-to-rigid after Nakajima), seeded from the author's 176 composition, Daniel's exact optimum of de Winter's 211 and Daniel's exact optimum of Couzo's 241 (the house); 304 a relaxed composition (55-square (h+8) x h and 68-square (h+7) x h pieces). Author asks the seeds' authors (Couzo, Daniel, de Winter) and pieces' sources be acknowledged. AI assistance stated.

Who else holds each value (frozen in acquisition/claims.json against main aeef99ef0):
- Every register upper-bound entry at these counts with a reader was rebuilt here and is above the certificate: T-101, T-151 at 176; T-098, T-149 at 211; T-098 at 241; T-098, T-151, T-152 at 304 (T-056, T-057 have no reader and print larger sides).
- 176: case T-151 (SQUISH) 13.8128562532770564, below by 1.698e-2; Couzo #561 13.807637227056 below by 1.176e-2 (Couzo's head b85dee2 13.807637226803, also above); the author's own fe43a64 176 below by 1.279e-2; #593 prints 13.7958723184364072 (undecided at its print).
- 211: case T-149 (the author's own #501 packing) 14.9963367213363157, below by 2.643e-3; ABOVE Couzo #583 14.993558914123 and #586 14.993558913975, and #593 14.9935589139740060, each by 1.353e-4. Couzo's #583/#586 say they continue this author's arrangement; #593's certificate is exactly Couzo's b85dee2 side. Smallest: #586 and #593 (one exact side; undecided by prints).
- 241: case T-098 (Couzo, improved by Daniel) 15.988132439524990848590591447359, below by 9.982e-4; ABOVE #583 15.987117095169, #586 15.987117095151 and #593 15.9871170951502393, each by 1.715e-5. Smallest: #586 and #593 (one exact side).
- 304: case T-152 (Chaoweeraprasit, improved by Couzo) 17.9295659468485010, below by 1.382e-4; #593 prints 17.9294277580751746, below this side by 3.7e-16 as printed, so the frozen record names #593 smallest; but #593's certificate at 46f638c (fetched to scratch, SHA-256 matching the issue) states this side rounded up at 30 places, 8.9e-31 above it. Measured exactly, this certificate is the smallest at 304, and at 176 too (#593 above by 9.2e-31). #593's 16-place prints are binary64 renderings.
- SQUISH's T-151 at 176 (13.8128562532770564) and Couzo's 561/583/586 at 176/211/241 are above or below as stated; T-152 at 304 is Couzo's. No other open report names these counts. Open PRs #585, #587, #591 change no bound lane here.

Validation plan (priced): sqcert adapter; both maintained exact routes, --workers 1: 12 jobs, about 20-35 min each pass at load 12-15. Third route and review: records lane. Source programs pinned against the #501 packet, not run.

## Draft acknowledgement (not posted)

Thank you, Daniil. We received the four certificates at dostashev/square-packing b909e1b (records/n0176, n0211, n0241 and n0304), and the eight SHA-256 values match the files there, including the 176, 211 and 241 files unchanged since b572f10. We will retain that commit, read each .sqcert exactly, and decide each packing with a duplicate-square and an outside-container control on our two maintained exact routes, then on a third exact route in review. We will compare each side with the record at its count and with the other reports open there; at 211 and 241, Francisco Couzo's #583 and #586, which continue your arrangements, are currently smaller. Your new 211 is a different packing from T-149, so it will be its own entry, and T-149 keeps its claim.
