---
type: is
id: is-01m4jk4am36yqbh6zcwxys40mj
title: "Import itsnaka (SQUISH): 15 new packings at n = 131-307 and smaller packings at 154 and 237 (#481)"
kind: task
status: in_progress
priority: 1
version: 4
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
hold: null
hold_until: null
created_at: 2026-10-10T09:43:27.107Z
updated_at: 2026-10-10T10:52:27.729Z
started_at: 2026-10-10T09:49:26.857Z
---
Issue https://github.com/jlevy/squares/issues/481 (opened 2026-10-09). Counts 131, 153, 207, 209, 232, 236, 259, 263, 269, 270, 292, 302, 303, 305, 307, plus 154 and 237 replacing SQUISH's #401 packings. Source itsnaka/squish-certs at d45669b48cc9 (squish-submission-2026-10-09, 50-digit certificates). Overlaps #476 at 237, 263, 270, 303 and #470 at several counts: compare by value and date. Stages 1-3 and maintained exact replays.

## Notes

2026-10-10 stage 1-2 lane (intake W1, branch worktree-agent-af22382952a5d839e, packet commit fce6a2f35).

PIN: itsnaka/squish-certs d45669b48cc97ad3aa17a6c847a8d06630f66eac (tree 91e24bc22a6f010e2ffae17eb0902f6b64d53ae2; authored 2026-10-09T20:07:51Z, committed 2026-10-09T21:23:14Z; parent e63e4e52b1728b6671b2f263c5e02a4aa79a39d3). First commit containing squish-submission-2026-10-09. Retrieved 2026-10-10T09:54Z. No licence file: derived-only custody.
PACKET: packing/resources/web/squish-481-third-request-2026-10-09 (acquire_source declaration; scope README.md + squish-submission-2026-10-09, 111 files, 9,043,090 bytes, all pinned only; acquire_source --check: PACKET_MATCHES_ITS_CONTRACT).

CLAIM MAP (exact side of nNNN.cert.json, rounded up at 15 places; case verified ceiling at main 657cc4861; smallest of all pending reports):
131 11.949659588035861 | case 11.951150044911952 ry-xu T-125 | others T-128 11.951105389414678, #470 11.951105389418 | SQUISH smallest, -1.490e-3
153 12.872029849081181 | case 12.879679373329315 Gupta T-127 | #470 12.879679373332; also below SQUISH n153 2026-10-07 (12.8796793733329640, already superseded by Gupta) | SQUISH, -7.650e-3
154 12.923070202301141 | case 12.926562245852347 Gupta | #470 12.926562245853 | SQUISH, -3.492e-3 (replaces SQUISH #401 n154)
207 14.885506308841678 | case 14.887992258302658 Gupta | #470 14.887992258303 | SQUISH, -2.486e-3
209 14.946223654487920 | case 14.949617952200399 Gupta | #470 14.949617952201 | SQUISH, -3.394e-3
232 15.767428349941842 | case reported 15.77817459305202 Kingbird (8+11/2 sqrt2), verified 15.77817459305203 evand exact ceiling | none | SQUISH, -1.075e-2
236 15.863955747159268 | case 15.867800839419917 Gupta | #470 15.867800839421 | SQUISH, -3.845e-3
237 15.902989220874966 | case 15.903676235189139 Gupta | #476 15.903670905580624, #470 15.903676235190 | SQUISH, -6.870e-4 (replaces SQUISH #401 n237)
259 16.591378145497699 | case 16.602568490493365 evand exact optimum of Couzo T-098 | none | SQUISH, -1.119e-2
263 16.733166007899884 | case 16.740419679538777 SQUISH second update | #476 16.740412653819157, #470 16.740419683047 | SQUISH, -7.254e-3
269 16.901513582189133 | case 16.905967058583841 evand/Couzo T-098 | none | SQUISH, -4.453e-3
270 16.929780126241172 | case 16.937807228446030 evand #399 T-119 | T-130 16.936723022876184, #476 16.936720031121016, #470 16.936723155038 | SQUISH, -8.027e-3
292 17.591378145497901 | case 17.597249391156466 Rehwaldt/Couzo | none | SQUISH, -5.871e-3
302 17.872029849081180 | case 17.881306218095809 SQUISH second update | #470 17.881306218091 | SQUISH, -9.276e-3
303 17.913065462738533 | case 17.920312372920350 SQUISH ten packings | #476 17.917443925494236, #470 17.920312372919 | SQUISH, -7.247e-3
305 17.951196144147386 | case 17.952959459015528 evand/Couzo | none | SQUISH, -1.763e-3
307 17.980862784054692 | case 17.981030548633311 evand/Couzo | none | SQUISH, -1.678e-4
Not filed: sources/squish-s155 (12.953161952032931), s240 (15.973009544313486), s306 (17.963510218121059), each ABOVE its case ceiling by 6.59e-4, 3.32e-3, 7.21e-5: no register action, stays in the packet.
Register action proposed: one new upper-bound entry, scope the 17 counts (bounds of one kind at several counts in one release); published 2026-10-09. 154 and 237 replace SQUISH's own #401 packings; earlier entries keep their claims.
Display note: the issue's 15-digit S_n and each cert's s_decimal are not roundings of s_exact (|diff| up to 1.8e-15); at 131, 153, 154, 207, 263, 269, 305, 307 the issue display is below the exact side. Safe display = upward ceiling of s_exact.

FORMAT (for the importer's SQUISH adapter): JSON {n, s_exact "p/q", s_decimal, note, squares: [[x, y, t], ...]} rational strings, box [0, S]^2, cos=(1-t^2)/(1+t^2), sin=2t/(1+t^2). Numerators/denominators ~80 digits. Same layout as the 2026-10-07 SQUISH packets. Files: squish-submission-2026-10-09/nNNN/nNNN.cert.json (17), sources/squish-sNNN-source.cert.json (3); SHA-256 in the packet manifest and README table.

PRICE: a timing probe of sqpack.verify.verify_packing (exact Fraction SAT, all pairs) found n131 valid in 1.00 s (8,515 pairs) and n307 valid in 5.36 s (46,971 pairs): ~0.11 ms/pair. All 17 positives = 526,784 pairs per route, about 1 min per route; with duplicate-square and outside-container controls on both routes, about 6 min serial, 3 min on 2 workers. Minutes: stage 4 can run on the import branch per the runbook. The probe is a price, not a recorded replay.

## Draft acknowledgement (2026-10-10, not posted; the owner posts it)

Thank you, Nate. We received the seventeen exact certificates in `squish-submission-2026-10-09` and pinned itsnaka/squish-certs at d45669b48cc97ad3aa17a6c847a8d06630f66eac, the commit that adds them; the three certificates in `sources/` (n = 155, 240, 306) are recorded with them as provenance, each above the current bound at its count. Each of the seventeen sides is below the bound the record holds at its count today and below every other report pending there, including #470 and #476. The tree has no licence, so as before we keep digests and derived facts rather than the files. Next we will replay every certificate exactly from `s_exact`, the rational centres and the half-angle tangents, by two maintained exact routes with duplicate-square and outside-container controls, and review the replay. One note: the 15-digit values in the issue and each certificate's `s_decimal` are not roundings of `s_exact`; at 131, 153, 154, 207, 263, 269, 305 and 307 they sit up to 1.8e-15 below it, so the record will display each side rounded up from the exact fraction.
