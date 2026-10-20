---
type: is
id: is-01m4jk49sdqkab8sbngjs0tvwm
title: "Import TheSnakeFang: s(308) <= 17.999309855162748, s(343) <= 18.994903529220497, s(344) <= 18.995489275430816 (#484)"
kind: task
status: closed
priority: 1
version: 6
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
hold: null
hold_until: null
created_at: 2026-10-10T09:43:26.253Z
updated_at: 2026-10-12T23:39:11.858Z
started_at: 2026-10-10T09:49:26.352Z
closed_at: 2026-10-12T23:39:11.858Z
close_reason: "Completed: #484 imported, registered as T-135, answered and closed (issue closed 2026-10-12); request entry closed on main."
resolution: null
duplicate_of: null
---
Issue https://github.com/jlevy/squares/issues/484 (opened 2026-10-10). Two-wedge constructions one k up from Arslanov-Mustafin-Shangitbayev; 308 is inside the n <= 324 horizon (register holds the grid 18), 343 and 344 are beyond it (dated beyond-horizon rows). Source TheSnakeFang/squarepack-certs at c75bebd87933416d3e1c7aba35ec733ea8ac7da0, folders n0308, n0343, n0344, Evan Daniel's rational .cert format. Stages 1-3 and a maintained exact replay (seconds).

## Notes

2026-10-10 (sub-agent lane, commit bd43e9c09): stage 2 packet packing/resources/web/fang-two-wedge-certificates-2026-10-10/ at c75bebd8793 (MIT verify.py, CC0 certificates; whole tree retained, drawings pinned only). Each .cert and its SQUISH-layout .cert.json state one exact packing. All three sides round up to the issue's 15-place prints. 308 is below the grid's 18 (case, both lanes) by 6.90e-4. 343 and 344 are beyond the horizon, with no case and no beyond-horizon row when read; below the grid's 19 by 5.10e-3 and 4.51e-3, and below Mishapolk's README prints (19.000000000007, 19.002369297056). Recording: dated rows in source-coverage.yaml beyond_horizon_claims (disposition tracked-outside-case-corpus, value as printed), with the source's claims_record acquisition/beyond-horizon-claims.json, which check_source_coverage.load_claims reparses to exactly {343, 344}. Replay: 9 jobs, all pass/refuse as required, least wall clearance 2^-65. register-plan printed; nothing registered.

## Stage 7 draft (2026-10-10, to post after PR #487 merges; not posted)

Supports posting after merge: yes (facts checked against PR #487's head 6fb495b3a; post once the merge's Pages deployment shows the T-135 row, and recheck the id if anything else merges first). Ledger: closeable (check_requests --report: both results settled, no ask queued; house adoption at 308 waits on PR #403 under think-fvz4, the project's own round, not an ask of the author).

@TheSnakeFang, thank you, Kevin. Your three certificates are imported on `main` through [PR #487](https://github.com/jlevy/squares/pull/487).

- **n = 308** is registered as **[T-135](https://jlevy.github.io/squares/all-results.html#t-135), V3/C3**, confirmed, at the exact side of `n0308.cert`: s(308) ≤ 496906684150483564257053639569689586211617178631487101147707692165192097/27606985387162255916575391130373464080218179016903156277167119960899584, which rounds up at 15 places to your 17.999309855162748. It is below the grid's 18, which the [n = 308 case record](https://github.com/jlevy/squares/blob/main/packing/frontier/n-308.md) holds in both lanes, by 6.90e-04.
- **n = 343 and 344** lie beyond the case corpus, so they have no case record or register entry. Your sides, s(343) ≤ 18.994903529220497 and s(344) ≤ 18.995489275430816, were recorded as verified beyond-horizon rows in the source register from the same evidence, 5.10e-03 and 4.51e-03 below the grid's 19.

**What came after.** Evan Daniel's #489, built on your packings, has smaller sides at all three counts. At 308 it is registered as T-141, 1.04e-03 below yours. At 343 and 344 his rows, 18.978232523635611279730512106023 and 18.994450514277401521114135796864, now supersede yours, which the record keeps. His issue asks that the two-wedge construction be credited to you, and T-141's credit does so.

The case record at 308 is unchanged for now. House adoption waits for [PR #403](https://github.com/jlevy/squares/pull/403), which rewrites every case record, and for a custody record of the replay workers; the case's house is chosen in that later adoption round. The reviews now recommend #489's certificate as the house at 308, crediting your construction, with T-135 kept verified.

**How it was checked.**
- All nine jobs, the three positives each with a duplicate-square and an outside-container control, were decided again by both maintained exact routes, `sqpack.verify` and `devtools.check_rational_witness_independent`, and equal their retained rows: 989,562 pair decisions. Every positive clears every wall by at least 2^-65 = 2.71e-20.
- A third exact route, `devtools.check_half_angle_area` (half-extent containment and exact intersection area), decided the three with six controls each, four of them sharp, and found each `.cert` equal to its `.cert.json`.
- No route here is your code, so the replay is independently re-implemented. The two maintained routes share one parse, the half-angle conversion and the separating-axis method, and all three share Fraction arithmetic. Evan Daniel's `verify_cert.py`, David Ellsworth's `check_packing.py` and your `verify.py` did not run here.
- A separately prompted AI [review](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-10-upper-bound-imports-476-481-483-484.md) reproduced the replay and found no blocking defect. No human review is claimed.

This confirms finite feasibility only, not optimality.

**Credit and custody.** T-135 credits you, with the two-wedge family of Arslanov, Mustafin and Shangitbayev, grown from David Ellsworth's and Tej Stead's packings on the Kingbird table; the certificate format is Evan Daniel's and the JSON layout SQUISH's. Your tree is retained under its own terms: `verify.py` under MIT, and the certificates as `ATTRIBUTION.md` releases them.

Nothing you asked for is queued, so this issue is closed with this comment. If the adoption round changes what this comment says, a follow-up will note it.

---
_Generated by [Claude Code](https://claude.ai/code)_


## Stage 7 draft from main at c6bf2d46f, 2026-10-11 — not posted (owner: leave as drafts)

Ledger: closeable (`check_requests --report` at c6bf2d46f: both results settled, no ask queued). Supersedes the 10 October draft above only in form: the facts at 308, 343 and 344 are unchanged at the merge; the 11 October final review is a second accepted review; links point at `results.html`. Raw `--draft 484` omits that 343/344 are superseded beyond-horizon rows (think-ri84 defect 6); this text says so. No case ceiling moved.

@TheSnakeFang, thank you, Kevin. Your three certificates are imported on `main` through [PR #487](https://github.com/jlevy/squares/pull/487).

- **n = 308** is registered as **[T-135](https://jlevy.github.io/squares/results.html#t-135), V3/C3**, confirmed, independently re-implemented, at the exact side of `n0308.cert`: s(308) ≤ 496906684150483564257053639569689586211617178631487101147707692165192097/27606985387162255916575391130373464080218179016903156277167119960899584, which rounds up at 15 places to your 17.999309855162748. It is below the grid's 18, which the [n = 308 case record](https://github.com/jlevy/squares/blob/main/packing/frontier/n-308.md) holds in both lanes, by 6.90e-04.
- **n = 343 and 344** lie beyond the case corpus, so they have no case record or register entry. Your sides, s(343) ≤ 18.994903529220497 and s(344) ≤ 18.995489275430816, were recorded as verified beyond-horizon rows in the source register from the same evidence, 5.10e-03 and 4.51e-03 below the grid's 19.

**What came after.** Evan Daniel's #489, built on your packings, has smaller sides at all three counts. At 308 it is registered as T-141, 1.04e-03 below yours. At 343 and 344 his rows, 18.978232523635611279730512106023 and 18.994450514277401521114135796864, now supersede yours, which the record keeps. His issue asks that the two-wedge construction be credited to you, and T-141's credit does so.

No case ceiling has moved: the case record at 308 is unchanged for now. House adoption waits for [jlevy/squares#403](https://github.com/jlevy/squares/pull/403), which rewrites every case record, and for a custody record of the replay workers; the case's house is chosen in that later adoption round. The reviews recommend #489's certificate (T-141) as the house at 308, crediting your construction, with T-135 kept verified.

**How it was checked.**
- All nine jobs, the three positives each with a duplicate-square and an outside-container control, were decided again by both maintained exact routes, `sqpack.verify` and `devtools.check_rational_witness_independent`, and equal their retained rows: 989,562 pair decisions. Every positive clears every wall by at least 2^-65 = 2.71e-20.
- A third exact route, `devtools.check_half_angle_area` (half-extent containment and exact intersection area), decided the three with six controls each, four of them sharp, and found each `.cert` equal to its `.cert.json`.
- No route here is your code, so the replay is independently re-implemented. The two maintained routes share one parse, the half-angle conversion and the separating-axis method, and all three share Fraction arithmetic. Evan Daniel's `verify_cert.py`, David Ellsworth's `check_packing.py` and your `verify.py` did not run here.
- A separately prompted AI [review](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-10-upper-bound-imports-476-481-483-484.md) reproduced the replay and found no blocking defect, and the [11 October final review](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-11-final-upper-bounds.md), by a distinct AI reviewer, accepted the entry again. No human review is claimed.

This confirms finite feasibility only, not optimality.

**Credit and custody.** T-135 credits you, with the two-wedge family of Arslanov, Mustafin and Shangitbayev, grown from David Ellsworth's and Tej Stead's packings on the Kingbird table; the certificate format is Evan Daniel's and the JSON layout SQUISH's. Your tree is retained under its own terms: `verify.py` under MIT, and the certificates as `ATTRIBUTION.md` releases them.

Nothing you asked for is queued, so this issue is closed with this comment. If the adoption round changes what this comment says, a follow-up will note it.

---
_Generated by [Claude Code](https://claude.ai/code)_
