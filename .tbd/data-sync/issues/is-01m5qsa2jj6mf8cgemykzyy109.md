---
type: is
id: is-01m5qsa2jj6mf8cgemykzyy109
title: "Import #799: Mohsen Karimi's 683 upper bounds at 1184–3775 (two-strip construction, Zenodo 23624433)"
kind: task
status: in_progress
priority: 2
version: 6
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
updated_at: 2026-10-25T04:41:32.890Z
started_at: 2026-10-24T20:24:13.700Z
---
New 2026-10-24 issue https://github.com/jlevy/squares/issues/799 (mohsensbu-jpg, 19:49:24Z): 683 upper bounds for s(n), n in [1184, 3775], 85 of them below the trivial grid ceil(sqrt n); two tilted strips (rows on the bottom wall, columns on the right) with rational tan(a/2), the rest an axis-parallel grid. Data doi:10.5281/zenodo.23624433 (table and regenerate.py rebuilding every certificate exactly); also registered at Mishapolk/square-packing-records. All above 1024: rows join think-llit's walk above 1024 (the owner's D1 answer), in report order against #715, #732, Couzo 5a299b4/964ee2b/43f666c, Fang and the rest. Stage 0 owner; stage 1 triage read-only first.

## Notes

2026-10-24 c-triage-799-1024 (stage 1, read-only; files in the coordinator scratchpad triage-799/). Pin: Zenodo 10.5281/zenodo.23624433 V1.0 (19:32:47Z, sole version; CC BY 4.0 data, MIT code): karimi_two_strip_records_v1_lite.zip 13,329 B sha256 0d4f89b0...78c5 = the #799 attachment byte for byte (README 2,626 B, records.csv 52,333 B with 683 rows, regenerate.py 3,379 B read as text only); no certificates in the record. Mishapolk/square-packing-records#1 opened 19:44:35Z (no commit; main still 7e82c64); #799 19:49:24Z. Report order: all 683 below Goebel (maintained module) and below every earlier report (#715, Couzo 5a299b4/6b7391d, #732 17cc220, #763, 964ee2b, 43f666c/1c17153, Fang bef5c42 and #797), margins 5.6e-4 (2363) to 8.8e-2; 0 above, 0 restatements, 0 undecided; previous-best column = least verified index statement at 683/683 (grid at 85). Kaggle no-coordinate sides below at 26 counts (not reports). At 61 of the 85 grid counts a theorem says s(n) < k with no numeric side (Daniel Lean aa12b98 at 59 incl. 1813; Fang #797 at 45). Construction = Ryu's L-shape (Thm 1.3) with independent strips; source does not cite it. Checker: parentless two-strip lemma decides all 683 from parameters in 0.168 CPU-s, controls refused (capacity+1, side below binding fit, mH+1, tH=0; side-1e-12 is NOT a control, slack >= 1.13e-8). Exact replay of written-out certs at 1184, 1193, 1813, 2363, 3775: both routes pass, all six controls refused by both, 10.2-42.2 CPU-s each; extrapolated positives 0.60 CPU-h, positives + six controls 5.1 CPU-h. Custody: 58 KB in Git; written-out certs 58.5 MB raw (~7.3 MB zlib) derived, not retained; no hosted manifest. Plan: enters R1's walk; rows in R5 after R1 + a W8 checker slice. Owner questions O1-O6 in questions-799.md.

2026-10-24 coord-intake-1024 on c-triage-799-1024's report (scratch triage-799/): Zenodo 10.5281/zenodo.23624433 V1.0 holds a 683-row parameter table and regenerate.py, no certificates; all 683 below every earlier report and Göbel; the construction is Ryu's L (Theorem 1.3) with two strips. Decisions by stated rules: (O2) build the maintained two-strip checker as a code slice (W8, OR-1 and the D2 pattern: a construction decided by a maintained checker), with all positives on both routes and six controls at one count per K (~0.8 CPU-h); (O4) credit Mohsen Karimi, the construction described as a two-strip L-packing after Ryu's Theorem 1.3, eponym held for the author's answer; (O5) dated by the issue, pinned at the Zenodo version; (O6) the 58 KB in Git, written-out certificates as receipts' digests only. (O3) rows land in their own slice after R1 creates the walk above 1024; R1 waits on the owner publishing data/couzo-715-certificates-v1 (D4). OWNER QUESTION O1 (not needed for #799): do theorem-wide k^2 - c statements (Ryu 1.3/1.4, T-163, #797, Daniel's Lean bounds) count as earlier reports beyond 324, as Göbel's does? Triage recommends admitting them at the side their construction gives, computed by a maintained module; until then noted in walks, kept out of starts.
blocked_on: think-llit

2026-10-25 c-w8-two-strip-1025 (W8, think-clgp; branch claude/w8-2026-10-25-two-strip-checker): the stage 7 acknowledgement for #799, updated for what W8 retained and checked; names no T-NNN and no rung; for the coordinator to post after W8 merges. It also notes the two comments after the triage's read (22:09:22Z theorem preprint 10.5281/zenodo.23627827; 22:34:47Z version 2, record 23628190, 2,824 rows to 9944), which are not triaged; drop that paragraph if they are answered first.

--- DRAFT ACKNOWLEDGEMENT #799 ---
Thank you, @mohsensbu-jpg. This acknowledges #799. The counts are above 1024, where the record keeps upper bounds as dated rows of its coverage register rather than as register entries, so nothing here takes a register number.

**What was received.** Zenodo record [10.5281/zenodo.23624433](https://doi.org/10.5281/zenodo.23624433), version V1.0, published 2026-10-24T19:32:47Z. Its `karimi_two_strip_records_v1_lite.zip` (13,329 bytes, SHA-256 `0d4f89b0b9353af405139cbb249831edd4f480cece86e219431ac924546978c5`) holds `records.csv`, `regenerate.py` and `README.md`. The zip attached to your comment is the same file, byte for byte. The record holds 683 rows at n = 1184 to 3775, each with an exact side S below ⌈√n⌉ and the construction's parameters, and no certificate files. The record takes the exact sides from `records.csv`. The issue's six-place prints round to nearest (at 2342 the print is 48.900000 and the side 48.90000012), so they are not used as bounds. The claims are dated by this issue, 2026-10-24T19:49:24Z. We note the same text at Mishapolk/square-packing-records#1, opened five minutes earlier; that repository's main has not changed since 23 October.

**What the triage found.** In exact arithmetic, every one of the 683 sides is below Göbel's classical construction at its count. Each is also below every earlier report the record reads at its count: Francisco Couzo's #715, #763 and his published indexes, Mykhailo Polkovskyi's #732, and Kevin Fang's certificates. The "previous best" column matches the least of these at all 683 counts. Kaggle leaderboard sides that state no coordinates are not reports here, so their being lower at 26 counts does not count against any row.

**What was retained and checked.** The repository now keeps version V1.0's `records.csv`, `README.md` and `regenerate.py`, with its `issue_text-1.md`, in the packet [`karimi-two-strip-2026-10-24`](https://github.com/jlevy/squares/blob/main/packing/resources/web/karimi-two-strip-2026-10-24/README.md). A checker this project maintains, [`devtools.two_strip_checker`](https://github.com/jlevy/squares/blob/main/packing/devtools/two_strip_checker.py), decides all 683 rows exactly from their parameters. Within each strip the squares sit on a lattice whose squares cannot overlap. The two strips and the grid fill disjoint regions of the box whenever the two fit inequalities hold. Each row's count is at most what the construction holds: exactly n at 403 rows, and at most 19 more elsewhere. Every row's seven negative controls are refused. They include one square more than the construction holds and a side 10⁻¹⁵ below the binding fit inequality. The checker writes the packing out at each count, and at 1184, 1193, 1813, 2363 and 3775 those packings pass both of this repository's exact routes, with all six controls of each refused by both. The 683 written-out certificates are not stored: each is pinned by its SHA-256, and the checker writes it again byte for byte. Your `regenerate.py` was read but not run.

**What comes next.** The rows join the record's work on counts above 1024, which walks every count in report order from the reports to date. Each is recorded there with this checker's decision. A reply will follow when the rows land.

**Your later comments.** Your comments of 22:09Z and 22:34Z, on the theorem preprint ([10.5281/zenodo.23627827](https://doi.org/10.5281/zenodo.23627827)) and on version 2 (2,824 rows to n = 9944), arrived after this triage. They will be read separately.

**Questions**, which hold nothing the record states:

1. The construction appears to be Sungjoon Ryu's L-shaped packing (an axis-parallel grid and two bands of tilted rows; his Theorem 1.3, [doi:10.5281/zenodo.23278927](https://doi.org/10.5281/zenodo.23278927)), with independent widths, angles and phases for the two bands and a side chosen below K. Evan Daniel formalized variants of it in Lean on 18 October, and Kevin Fang's #797 uses it. Did you derive it independently, and do you agree with describing your rows as optimized instances of Ryu's L-packing? The record will credit the rows to you either way. The question is only how the README text describes the construction.
2. Would you publish the 683 certificate files you checked, for example as a new version of the Zenodo record? The record does not need them, because it rebuilds the packings from your parameters. With them it could also state that its packings are the ones you verified, by digest.
3. At 61 of the 85 counts where the table's previous best is the grid, an earlier theorem already gives s(n) < ⌈√n⌉. Examples are Daniel's Lean bound c*(k) ≤ 4⌈√(2k − 7)⌉ − 1, which covers 1813 = 43² − 36, and Fang's #797. Neither states a numeric side, and your sides are well below the grid there, so this changes none of your rows. Would you like the README's "85 improve on the trivial grid" to say "where the least numeric bound was the grid"?

---
_Generated by [Claude Code](https://claude.ai/code)_
--- END DRAFT ---
