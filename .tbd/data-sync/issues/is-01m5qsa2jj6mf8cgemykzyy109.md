---
type: is
id: is-01m5qsa2jj6mf8cgemykzyy109
title: "Import #799: Mohsen Karimi's 683 upper bounds at 1184–3775 (two-strip construction, Zenodo 23624433)"
kind: task
status: in_progress
priority: 2
version: 5
delegate: c-triage-799-1024
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
child_order_hints:
  - is-01m5qvfqtde25k8jmdn7skvkpc
hold: null
hold_until: null
created_at: 2026-10-24T20:23:20.914Z
updated_at: 2026-10-24T21:01:23.661Z
started_at: 2026-10-24T20:24:13.700Z
---
New 2026-10-24 issue https://github.com/jlevy/squares/issues/799 (mohsensbu-jpg, 19:49:24Z): 683 upper bounds for s(n), n in [1184, 3775], 85 of them below the trivial grid ceil(sqrt n); two tilted strips (rows on the bottom wall, columns on the right) with rational tan(a/2), the rest an axis-parallel grid. Data doi:10.5281/zenodo.23624433 (table and regenerate.py rebuilding every certificate exactly); also registered at Mishapolk/square-packing-records. All above 1024: rows join think-llit's walk above 1024 (the owner's D1 answer), in report order against #715, #732, Couzo 5a299b4/964ee2b/43f666c, Fang and the rest. Stage 0 owner; stage 1 triage read-only first.

## Notes

2026-10-24 c-triage-799-1024 (stage 1, read-only; files in the coordinator scratchpad triage-799/). Pin: Zenodo 10.5281/zenodo.23624433 V1.0 (19:32:47Z, sole version; CC BY 4.0 data, MIT code): karimi_two_strip_records_v1_lite.zip 13,329 B sha256 0d4f89b0...78c5 = the #799 attachment byte for byte (README 2,626 B, records.csv 52,333 B with 683 rows, regenerate.py 3,379 B read as text only); no certificates in the record. Mishapolk/square-packing-records#1 opened 19:44:35Z (no commit; main still 7e82c64); #799 19:49:24Z. Report order: all 683 below Goebel (maintained module) and below every earlier report (#715, Couzo 5a299b4/6b7391d, #732 17cc220, #763, 964ee2b, 43f666c/1c17153, Fang bef5c42 and #797), margins 5.6e-4 (2363) to 8.8e-2; 0 above, 0 restatements, 0 undecided; previous-best column = least verified index statement at 683/683 (grid at 85). Kaggle no-coordinate sides below at 26 counts (not reports). At 61 of the 85 grid counts a theorem says s(n) < k with no numeric side (Daniel Lean aa12b98 at 59 incl. 1813; Fang #797 at 45). Construction = Ryu's L-shape (Thm 1.3) with independent strips; source does not cite it. Checker: parentless two-strip lemma decides all 683 from parameters in 0.168 CPU-s, controls refused (capacity+1, side below binding fit, mH+1, tH=0; side-1e-12 is NOT a control, slack >= 1.13e-8). Exact replay of written-out certs at 1184, 1193, 1813, 2363, 3775: both routes pass, all six controls refused by both, 10.2-42.2 CPU-s each; extrapolated positives 0.60 CPU-h, positives + six controls 5.1 CPU-h. Custody: 58 KB in Git; written-out certs 58.5 MB raw (~7.3 MB zlib) derived, not retained; no hosted manifest. Plan: enters R1's walk; rows in R5 after R1 + a W8 checker slice. Owner questions O1-O6 in questions-799.md.

2026-10-24 coord-intake-1024 on c-triage-799-1024's report (scratch triage-799/): Zenodo 10.5281/zenodo.23624433 V1.0 holds a 683-row parameter table and regenerate.py, no certificates; all 683 below every earlier report and Göbel; the construction is Ryu's L (Theorem 1.3) with two strips. Decisions by stated rules: (O2) build the maintained two-strip checker as a code slice (W8, OR-1 and the D2 pattern: a construction decided by a maintained checker), with all positives on both routes and six controls at one count per K (~0.8 CPU-h); (O4) credit Mohsen Karimi, the construction described as a two-strip L-packing after Ryu's Theorem 1.3, eponym held for the author's answer; (O5) dated by the issue, pinned at the Zenodo version; (O6) the 58 KB in Git, written-out certificates as receipts' digests only. (O3) rows land in their own slice after R1 creates the walk above 1024; R1 waits on the owner publishing data/couzo-715-certificates-v1 (D4). OWNER QUESTION O1 (not needed for #799): do theorem-wide k^2 - c statements (Ryu 1.3/1.4, T-163, #797, Daniel's Lean bounds) count as earlier reports beyond 324, as Göbel's does? Triage recommends admitting them at the side their construction gives, computed by a maintained module; until then noted in walks, kept out of starts.
blocked_on: think-llit
