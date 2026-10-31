---
type: is
id: is-01m685wzp4h0xvh1qv6pn93we4
title: "Import Mohsen Karimi: 5,134 upper bounds at n = 1182-9946, filled-end two-band L packings, Zenodo V2.0 23819397 (#847)"
kind: task
status: in_progress
priority: 2
version: 9
delegate: bold-ritchie-l4
labels:
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
child_order_hints:
  - is-01m685x87zdg13w910fy66rd68
  - is-01m685x9g3gm6q41qv9147fwb5
hold: null
hold_until: null
created_at: 2026-10-31T05:11:14.372Z
updated_at: 2026-10-31T06:14:58.530Z
started_at: 2026-10-31T05:13:12.006Z
---
New 2026-10-30 issue https://github.com/jlevy/squares/issues/847 (mohsensbu-jpg, 21:56:32Z): Mohsen Karimi's filled-end record set V2.0, 5,134 upper bounds at n = 1182 to 9946, a new construction: the two-band L packing of #836 with the band ends filled by axis-parallel layers. It supersedes V1.0, posted on #836 (comment 6433611255, 2026-10-27T04:16:22Z). Same author as #799 (think-5dc3) and #836 (think-7yrs); a different construction, which two_strip_checker does not read, so it needs W9 (think-fuwd). Stage 0 owner: bold-ritchie-l4 (intake pass 2026-10-31, think-3guf).

blocked_on: think-fuwd, think-llit

## Stage 1 triage (2026-10-31, bold-ritchie-l4; read-only; PARTIAL)

zenodo.org is denied by this session's network policy (proxy 403 on CONNECT), so neither deposit was fetched or read. Everything below is from the issue's text and #836's comments; nothing is compared row by row.

**Pins (as the issue states them; not yet fetched or hashed here).**
- V2.0: Zenodo 10.5281/zenodo.23819397, published 2026-10-30: filled_records.csv (681,083 bytes, SHA-256 1cbfecf886a2000bd9d5f54304813d7422f785a2fb9a15655f2119a33f8c48f5, md5 43dee564ec2a4dd06cc36ee9afa3dbbf), filled_ends.py, regenerate_filled.py, check_cert.py, README_filled.md.
- V1.0: Zenodo 10.5281/zenodo.23681705, published 2026-10-27: karimi_filled_end_v2.zip (200,542 bytes, SHA-256 f1684581d9756ec2c0515ab65a3702e09d915843687b8f326fb37e56ee7cfa97, md5 0c531ee486af13182e482d4138e07636), holding filled_records.csv (SHA-256 f047c44b7d627d7d5e2e990136931a6d8cf4c19ded439482ab1ef9f8bd030b56), filled_ends.py, regenerate_filled.py, check_cert.py, README_filled.md. Retained beside V2.0: it is a report in its own right (dated 27 October), whatever the walk decides of its rows.

**Claims.**
- C1 (V2.0): 5,134 rows, one per n, n = 1182..9946: exact side, previous best side and its source, and exact parameters K, bV, tV, yV, bH, tH, yH (an independent width, tilt and lift split for each band), searched over K = 35..100.
  - 4,841 rows lower a v5 row of #836 (10.5281/zenodo.23664800);
  - 293 rows at counts not in v5.
- C2 (V2.0): every row strictly below the verified entry at its n in franciscouzo/square-packing 712c6a6 and Mishapolk/square-packing-records ab8e833, where one exists. Both heads are later than V1.0's report; the walk reads every report in order.
- C3 (V2.0): every packing rebuilt in exact rationals by regenerate_filled.py and accepted by Mishapolk's verify_bound_certificate.py (ab8e833): 5,134 accepted, 0 rejected. The producer's own check, not retained.
- C4 (V1.0, comment on #836): 4,571 rows at n = 1184..9946: 4,261 lower a v5 row; 310 at counts not in v5, each stated below Mishapolk ab8e833. The comment of 2026-10-30T17:38:24Z sets 45 of them aside as not below Couzo's 712c6a6 (28 October).
- C5 (V2.0 against V1.0): 40 V1.0 rows are not in V2.0 (1240, 1245, 1246, 1247, 1375, 1450, 1451, 2214, 3484, 3972, 4625, 4762, 5185, 5330, 5477, 5626, 5777, 5930, 6085, 6242, 6401, 6562, 6725, 6890, 7057, 7226, 7397, 7570, 7745, 7922, 8101, 8282, 8465, 8650, 8837, 9026, 9217, 9410, 9605, 9802), all among the 310 V1.0 rows at counts not in v5. At 1244, 2407, 3603, 3724 and 3847, V2.0 has a smaller side than V1.0's. No V1.0 row that improved v5 was dropped.
- C6 (the author's instructions): use V2.0 only if no V1.0 row was taken in; otherwise replace V1.0's rows with V2.0's and withdraw the 40; where V2.0 is below v5 take V2.0; the 467 v5 rows with no V2.0 row stand. With v5, 5,601 distinct counts in 1182..9946.
- Credit: Mohsen Karimi (ORCID 0009-0004-1055-8267) for the rows, the independent band parameters and the per-n search. Construction: Ryu's L-shaped packing (10.5281/zenodo.23278927, Theorem 1.3); the axis-layer fill of the band ends is Evan Daniel's idea (evand/square-packing, certificates/k2-minus-c/), written as in Kevin Fang's note (10.5281/zenodo.23624565, Sections 2-3). The author's own attribution, to be read from README_filled.md at the pin. Claude assistance disclosed; search in MATLAB Online, reproduced in Python.

**Map to the record.** All counts above 1024: rows of the walk above 1024 (think-llit), not register entries; no T-NNN. Report order: V1.0 dated by its comment (2026-10-27T04:16:22Z) and V2.0 by this issue (2026-10-30T21:56:32Z); each row is recorded only where the walk finds it below every earlier report (v5's row included) and Göbel's construction. How V1.0 enters is Q-847a below: if it counts as a report, a V2.0 side equal to V1.0's is a tie that stays with V1.0's row and a lower one is recorded after it; if not, V2.0's rows stand alone in order.

**Owner questions (no stated rule decides them).**
- Q-847a (restated 31 October after review A1 of #848): #847's instruction is conditional: "If no V1.0 row has been taken in, please use V2.0 only and ignore V1.0. If V1.0 rows have been taken in, please replace them with the V2.0 rows and withdraw the 40 rows listed above." No V1.0 row has been taken in, so the first branch applies: the author asks that V1.0 be ignored. The question: does a published deposit whose author asks, before any intake, that it be ignored still count as a report in report order? think-8m4k's answer covers only "a watched certificate its author withdrew from an issue, claiming a lower file later". (a) Yes: V1.0 is a report dated 2026-10-27T04:16:22Z; its rows are recorded wherever they are below every earlier report, a V2.0 side equal to one is a tie that stays with V1.0, and a lower V2.0 side is recorded after it. (b) No: V1.0 stays among the walk's publications, retained in the packet, and the walk keeps it out of the record, as think-8m4k's withdrawn files are (beyond_horizon_replay.Held.answer); V2.0's rows stand alone in order. Recommended: (b), the author's request and think-8m4k's mechanics, read as reaching a whole deposit withdrawn before any row was written. It changes the rows at the counts where V1.0 is the earliest side below the standing one, including the 40 V1.0 rows V2.0 drops, which (a) would record wherever they were below every report before 27 October, superseded later by Couzo's 712c6a6 (28 October), which the author says is below them. The walk can count both readings once both deposits are read.
- Q-847b (credit text only): describe the construction as "Ryu's L-shaped packing (Theorem 1.3) with the band ends filled by axis-parallel layers, after Evan Daniel's k2-minus-c certificates as written in Kevin Fang's note", credited to Karimi for the rows. Recommended as the author states it; no row waits on it.

**Checker.** None maintained reads this construction. W9 (think-fuwd) writes devtools.filled_end_checker, deciding a row exactly from its seven parameters, with negative controls and a write-out builder, read from filled_ends.py and the README as the specification (W8's pattern for #799). It needs the deposit first.

**Price (CPU-hours; basis: W8's receipts and R5's figures in the rows-above-1024 plan, extrapolated; the filled ends add squares, not checks of another kind).**
- W9: about 0.05 (tests, controls, five written-out counts on both routes), as W8.
- Checker on every row with its controls: about 0.04 for V2.0's 5,134, 0.04 for V1.0's 4,571.
- Written-out positives on both routes for the rows the walk records: 7.6 CPU-s a row, so about 10.8 for V2.0's 5,134, and up to about 9.6 more for V1.0's 4,571 if the walk records them under Q-847a.
- Six controls on both routes at one count per K (66 values): about 0.9 a deposit.
- **Total about 11.8 for V2.0, up to about 21.3 with V1.0**, one item under the 40 CPU-h cap either way. Measure one count near 9946 on both routes first, and re-price.

**Custody.** V2.0's files are about 0.7 MB and V1.0's zip 0.2 MB: into Git in a new packet, checked with check_added_blobs before the first commit. Written-out certificates, about 1 GB raw a deposit, are derived and not retained: receipts pin each SHA-256 and the checker rewrites it. No hosted release is needed unless the owner wants the written-out certificates kept.

**Plan.** Stage 2 (retain, both deposits) needs zenodo.org. Then W9 (think-fuwd). Stage 3 needs R1 and lands as a slice after R5 (think-5dc3, with #836's rows), recording V1.0's and V2.0's rows in report order. Stage 4: think-qczx (~11.8, up to ~21.3 CPU-h).

**Answer bead:** this one. The acknowledgement draft is in its notes, to post after the pull request that carries this triage merges.

## Notes

2026-10-31 bold-ritchie-l4, after review A of #848 (A1): Q-847a restated in the description (the first branch of #847's conditional applies: ignore V1.0); the draft below says so.

2026-10-31 bold-ritchie-l4: stage 0-1 (partial) recorded on branch claude/bold-ritchie-xo28us-beyond (requests entry, triage: pending; #836's entry maps V1.0 as filled-end-v1 on this bead). Not checked: zenodo.org refused by the session's network policy, so neither deposit (23819397, 23681705) is fetched or hashed and no row is compared. Next for this bead: fetch and pin both records; read README_filled.md's attribution; read filled_ends.py and regenerate_filled.py as the specification for W9 (think-fuwd); re-derive the claim counts; put Q-847a to the owner with the counts each reading changes.

--- DRAFT ACKNOWLEDGEMENT #847 (post after the pull request carrying this triage merges; names no T-NNN and no rung) ---
Thank you, @mohsensbu-jpg. This acknowledges #847 and the V1.0 set of your 27 October comment on #836.

**What was received.** The filled-end record set V2.0, Zenodo [10.5281/zenodo.23819397](https://doi.org/10.5281/zenodo.23819397), with `filled_records.csv` (681,083 bytes, SHA-256 `1cbfecf886a2000bd9d5f54304813d7422f785a2fb9a15655f2119a33f8c48f5` as you state it), `filled_ends.py`, `regenerate_filled.py`, `check_cert.py` and `README_filled.md`: 5,134 rows at n = 1182 to 9946. Also V1.0, [10.5281/zenodo.23681705](https://doi.org/10.5281/zenodo.23681705), with `karimi_filled_end_v2.zip` (200,542 bytes, SHA-256 `f1684581d9756ec2c0515ab65a3702e09d915843687b8f326fb37e56ee7cfa97`): 4,571 rows at 1184 to 9946. No V1.0 row has been taken in.

**Where it stands.** We could not yet fetch either deposit: the session that read this issue could not reach zenodo.org. Nothing has been compared row by row, and the counts above are yours. The construction is new to the record, and no checker this project maintains reads it yet. The next steps are:

1. Retain both deposits by their digests.
2. Write a maintained checker for the filled-end packing from your `filled_ends.py` and README. It will decide each row exactly from its seven parameters, with negative controls, as `two_strip_checker` does for #799 and #836.
3. Check written-out packings on both of this repository's exact routes.

**How the rows will be read.** Each V2.0 row is dated by this issue and joins the record's walk over counts above 1024, which takes every report in the order it reached this repository. A row is recorded wherever it is below every earlier report there, your v5 row and V1.0's included, and below Göbel's construction. You asked that V1.0 be ignored if none of its rows had been taken in, and none had. Whether a published deposit its author asks to have ignored still counts as an earlier report, under the rule that takes reports in the order they arrive, is a question for the project's owner; until it is answered, no V1.0 row is recorded. The record states your credit for the rows, the band parameters and the search, and the construction as Ryu's L-shaped packing (Theorem 1.3) with the band ends filled after Evan Daniel's idea, as written in Kevin Fang's note, as this issue states it.

A reply will follow when the rows land.

---
_Generated by [Claude Code](https://claude.ai/code)_
--- END DRAFT ---
