---
type: is
id: is-01m685wqakx05engdrvf9s4789
title: "Import Mohsen Karimi: 5,308 upper bounds at n = 1182-9944, two-strip construction, Zenodo v5.0 23664800 (#836)"
kind: task
status: in_progress
priority: 2
version: 8
delegate: bold-ritchie-l4
labels:
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
child_order_hints:
  - is-01m685x0n34btg2azt8bwd8d53
hold: null
hold_until: null
created_at: 2026-10-31T05:11:05.811Z
updated_at: 2026-10-31T06:13:59.890Z
started_at: 2026-10-31T05:13:11.988Z
---
New 2026-10-26 issue https://github.com/jlevy/squares/issues/836 (mohsensbu-jpg, 12:18:36Z): Mohsen Karimi's version 5.0 of the two-strip record set of #799, 5,308 upper bounds at n = 1182 to 9944. Same author and construction as #799 (think-5dc3): its rows are decided by the maintained devtools.two_strip_checker and land beside #799's in the walk above 1024 (think-llit). A new issue, so its own import and answer bead; think-5dc3 stays #799's. Stage 0 owner: bold-ritchie-l4 (intake pass 2026-10-31, think-3guf).

blocked_on: think-llit

## Stage 1 triage (2026-10-31, bold-ritchie-l4; read-only; PARTIAL)

zenodo.org is denied by this session's network policy (proxy 403 on CONNECT), so the deposit was not fetched and records.csv was not read. Everything below is from the issue's text and its comments, checked against the record where the record can answer; nothing is compared row by row.

**Pin (as the issue states it; not yet fetched or hashed here).** Zenodo 10.5281/zenodo.23664800, version v5.0, published 2026-10-26: karimi_two_strip_records_v3_lite.zip, 96,138 bytes, SHA-256 9c70c4d84c8fb9795a00d1a792210f4bd6e44bf17de245351f2f03a69fcc6325; members records.csv (SHA-256 7e78c15de4c2acc6e6313e4954a4454eb13825b4c0cd1ad2334ec86caef3e941), regenerate.py (stated unchanged from version 2, whose copy is byte-identical to version 1's in the karimi-two-strip-2026-10-24 packet), README.md. Code in karimi_two_strip_code_v1_lite.zip in the same record. Whether 23664800 is a version of #799's concept 10.5281/zenodo.23624432 is unconfirmed (its version label and file names say so; Zenodo unreachable).

**Claims (the issue's own count).**
- C1: 5,308 rows, one per n, n = 1182..9944, columns: exact side, previous best side, K, mH, tH, phH, mV, tV, phV (the #799 format, which two_strip_checker reads), plus below_all_reported. Search window widened from [K - 0.1, K) to [K - 0.5, K), K = 35..100.
  - 2,484 counts not in version 2 (record 23628190);
  - 1,434 of version 2's 2,824 counts at a smaller side;
  - 1,390 version 2 rows unchanged.
- C2: 51 rows marked below_all_reported = no, where Couzo's index lists a smaller side derived from a Kaggle leaderboard value with no coordinates. A side with no coordinates is not a report here (#799's triage), so those 51 stay candidates; the walk decides each against the reports it reads.
- C3: every side strictly below the verified entry at its n in Mishapolk/square-packing-records 7e82c64 and franciscouzo/square-packing 1c17153; improvements 0.00016 to 0.204. (The walk reads more reports than these two: #715, #732 17cc220, #763, 964ee2b, 43f666c, Fang bef5c42, #799's own versions.)
- C4: every packing rebuilt by regenerate.py in exact rationals and accepted by Mishapolk's verify_bound_certificate.py (7e82c64). Producer's own check, not retained.
- C5 (comment 6418810023, 2026-10-26T14:40:30Z, maximusrufus): a third party rebuilt all 5,308 with the submitter's regenerate.py and re-checked them in exact rationals (5,308 valid; a 398-row sample also through Mishapolk's verifier). That reproduces with the producer's code; its program and receipt are not retained, so it is no evidence entry. Note it in the entry.
- C6 (body, last paragraph): the author withdraws two conjectures: frac(s(n)) > 1/2 whenever s(n) < ceil(sqrt n) (contradicted by Hajba's s(1765) ~ 42.488), and Conjecture 1 of his note (c*(K) of order sqrt K). An evidence update on #799's entry (its summary and theorem-near-integer still say the note keeps the conjecture), owned by think-x0kn.
- C7: comment 6433611255 (2026-10-27T04:16:22Z) posted a filled-end set V1.0, Zenodo 10.5281/zenodo.23681705, 4,571 rows at 1184..9946; comment 6529319971 (2026-10-30T17:38:24Z) sets 45 of them aside against Couzo's 712c6a6; comment 6534369793 (2026-10-30T21:57:59Z) says V1.0 is superseded by V2.0 in #847. V1.0's rows belong to #847's import (think-r94q); they are mapped there.
- Credit: Mohsen Karimi (ORCID 0009-0004-1055-8267). Construction: instances of Sungjoon Ryu's L-shaped packing (10.5281/zenodo.23278927, Theorem 1.3) with independent band widths, angles and phases, found independently (the author's wording, as agreed on #799). Claude assistance disclosed; part of the search in MATLAB Online.

**Map to the record.** All counts are above 1024: rows of source-coverage.yaml in think-llit's walk above 1024, not register entries; no T-NNN. Report order: dated by the issue, 2026-10-26T12:18:36Z, pinned at record 23664800. At the 1,390 unchanged counts a tie stays with the earlier report: version 1's row (19:49:24Z on 24 October) where version 2 tied version 1 (682 of version 1's 683 counts, 1184-3775), else version 2's (22:34:47Z). At the 1,434 lowered counts the row is recorded after version 2's, superseding it. The 2,484 new counts, 1182 and 1183 among them, are new reports. Each is recorded only where the walk finds it below every earlier report and Göbel's construction; the walk, not this triage, decides it. Expected rows: at most 3,918.

**Checker (corrected 31 October after review A2 of #848).** The parameters are #799's (K, mH, tH, phH, mV, tV, phV), which devtools.two_strip_checker (W8, #808) decides. But the issue says v5's records.csv adds a column below_all_reported, and two_strip_checker.parse_records requires the header to be exactly its 11 COLUMNS (two_strip_checker.py:258-270, :558-560) and raises CustodyError on any extra column, so the checker as written refuses v5's file. Ingest needs a column set per deposit (each Deposit naming its columns, with below_all_reported read and not decided), a small code change made on fetch once the header is read; written against an unread header it would guess the column's name, position and values. On fetch also confirm the K range and that regenerate.py is byte-identical to the packet's.

**Price (CPU-hours; basis: W8's receipts and R5's figures in the rows-above-1024 plan).**
- Checker on every row with seven controls: W8 decided version 2's 2,824 rows in 67 CPU-s, so about 0.035 for 5,308.
- Written-out positives on both maintained routes for the rows the walk records: R5's 5.95 for 2,825 rows is 7.6 CPU-s a row (extrapolated past the 3775 sample), so about 8.3 for 3,918.
- Six controls on both routes at one count per K (66 values of K): about 0.9.
- The ingest change above: code time, not compute (its tests take seconds).
- **Total about 9.2**, one item under the 40 CPU-h cap. Measure one count near 9944 on both routes with its six controls first, and re-price. Six controls at every recorded count would be about 75, over the cap.

**Custody.** The zip is 96 KB: into Git in a new packet (karimi-two-strip-2026-10-26, or a v5 directory in the existing packet as a later revision of the same source), checked with check_added_blobs before the first commit. Written-out certificates, about 1 GB raw at #799's 555 MB for 2,824, are derived, not retained: each receipt pins a SHA-256 and the checker rewrites the file. No hosted release is needed unless the owner wants the written-out certificates kept.

**Plan.** Stage 2 (retain) needs zenodo.org: allow it in the environment's network settings, or the owner fetches the zip. Stage 3 (rows) needs R1 (the walk above 1024) and joins R5 (think-5dc3, #799's rows): one slice records #799's 2,825 and #836's rows together, both decided by two_strip_checker. Stage 4: validation bead think-gw1s (~9.2 CPU-h).

**Answer bead:** this one. The acknowledgement draft is in its notes, to post after the pull request that carries this triage merges.

## Notes

2026-10-31 bold-ritchie-l4, after review A of #848 (A2, A4): the checker claim is corrected in the description (v5's below_all_reported column needs an ingest change on fetch) and the draft below says so; ties stay with the earlier report, version 1's or version 2's.

2026-10-31 bold-ritchie-l4: stage 0-1 (partial) recorded on branch claude/bold-ritchie-xo28us-beyond (requests entry, triage: pending). Not checked: zenodo.org refused by the session's network policy, so the deposit is neither fetched nor hashed and no row is compared. Next for this bead: fetch and pin record 23664800 (and confirm it is a version of concept 23624432), confirm records.csv's columns and that regenerate.py is the packet's byte for byte, run two_strip_checker over the 5,308 rows read-only, and re-derive the claim counts against the record; then retain (stage 2) and land the rows with R5 (think-5dc3) after R1.

--- DRAFT ACKNOWLEDGEMENT #836 (post after the pull request carrying this triage merges; names no T-NNN and no rung) ---
Thank you, @mohsensbu-jpg. This acknowledges #836, your comments of 26 October (14:53Z), 27 October and 30 October, and @maximusrufus's check of 26 October. As with #799, these counts are above 1024, where the record keeps upper bounds as dated rows of its coverage register rather than as register entries.

**What was received.** Version v5.0 of your two-strip record set, Zenodo [10.5281/zenodo.23664800](https://doi.org/10.5281/zenodo.23664800), with `karimi_two_strip_records_v3_lite.zip` (96,138 bytes, SHA-256 `9c70c4d84c8fb9795a00d1a792210f4bd6e44bf17de245351f2f03a69fcc6325` as you state it): 5,308 rows at n = 1182 to 9944. The filled-end set V1.0 of your 27 October comment, and its V2.0 in #847, are taken in with #847.

**Where it stands.** We could not yet fetch the deposit: the session that read this issue could not reach zenodo.org. Nothing has been compared row by row, and the counts above are yours. The next step is to pin the record by its digests, retain `records.csv`, `README.md` and `regenerate.py` beside versions 1 and 2 in the record's packet, and decide every row with the maintained two-strip checker. It decides your parameters as it does #799's; its reader takes only version 2's columns today, so it will learn to read `below_all_reported` once we have the file.

**How the rows will be read.** Each row is dated by this issue and joins the record's walk over counts above 1024, which takes every report in the order it reached this repository:

- where v5 states version 2's side again (1,390 counts by your count), the earlier report's row stands: version 1's where version 2 tied it, else version 2's;
- where v5 is lower (1,434), its row is recorded after version 2's;
- the 2,484 new counts are recorded wherever the walk finds them below every earlier report and Göbel's construction.

A side derived from a Kaggle value with no coordinates is not a report here, so your 51 rows marked `no` are not set aside on that account. The written-out packings will be checked on both of this repository's exact routes, with negative controls, as for #799. @maximusrufus's rebuild used your `regenerate.py`; it is noted with the issue, but its program and receipts are not retained here, so the record does not count it as evidence.

Thank you also for withdrawing the two conjectures; the record will say so with #799's note.

A reply will follow when the rows land.

---
_Generated by [Claude Code](https://claude.ai/code)_
--- END DRAFT ---
