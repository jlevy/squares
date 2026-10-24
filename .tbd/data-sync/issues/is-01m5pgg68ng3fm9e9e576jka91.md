---
type: is
id: is-01m5pgg68ng3fm9e9e576jka91
title: "Triage franciscouzo/square-packing 43f666c-1c17153 (no issue): the 24 October per-puzzle board and live records since 964ee2b (#763's pin), and the gzip-hash and 227/260 credit commits (#678)"
kind: task
status: closed
priority: 1
version: 5
delegate: c-triage-watch-1024
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T08:30:09.684Z
updated_at: 2026-10-24T09:12:53.097Z
started_at: 2026-10-24T08:44:29.407Z
closed_at: 2026-10-24T09:12:53.097Z
close_reason: "Stage 1 triage done (notes): 43f666c's 126 counts to 1024 and 831 recipes above go to import bead think-gn29; 73eac5b and 1c17153 are evidence for think-mdfr; the 1c17153 read rides the next records PR naming think-gn29."
resolution: null
duplicate_of: null
---

## Notes

2026-10-24 coord-intake-1024: from the sweep (franciscouzo/square-packing 6 commits past the 6b7391d read; efef7d1, fa6237e and 964ee2b are #763's). 43f666c (00:55Z 24 Oct) 'Land the 24 October per-puzzle board and the live records since 964ee2b'; 73eac5b and 1c17153 (04:43Z, 04:53Z) label external gzip hashes and credit 227/260, which Couzo's #678 answer of 06:11Z reports (think-mdfr). Read-only triage first (stage 1): which rows are later reports than 964ee2b, whether an issue claims them, and their report order against #763 and the evand candidates.


2026-10-24 c-triage-watch-1024 (stage 1, read-only; coordinator coord-intake-1024). Nothing committed, pushed or posted. Read against main e5c1c64e3 (post #757 and #769) and franciscouzo/square-packing@964ee2b (#763's pin). Scratch data and tools: scratchpad triage-watch/ (data/couzo/{964ee2b,43f666c,73eac5b,1c17153}/ indexes; tools/index_diff.py, tools/against_tree.py, tools/corpus_below.py; out/certified-964-43f.tsv, out/against-tree-43f.tsv).

SOURCE AND TIMING
- Head 1c1715399709bc955e9b402947ab8b52bbacdfc3. GitHub activity API: 964ee2b->1c17153 pushed together at 2026-10-24T06:10:44Z (43f666c committed 00:55:44Z; 73eac5b 04:52:11Z; 1c17153 04:53:53Z). Dated by the push (PUSHED_LATER, as think-cnn7's A7 note says for fa6237e), 43f666c is a report from 06:10:44Z; by either time it follows #763 (23:35:51Z) and shares no count with evand's 8a8879a (04:53:53Z), so their order does not matter.
- CLAIMS: none. #763 has 0 comments (updated 02:03:56Z, label intake). Couzo's comments after 23:35Z are #672 (06:10:57Z, issuecomment-6380747582: CT105 227 credit, sqpack.verify call), #678 (06:11:30Z, issuecomment-6380752551: evand pin, n260 seed, hash kinds, 227/260 credit) and #715 (06:12:05Z, issuecomment-6380757758: construction credits restored in 43f666c/73eac5b for 662 assembly pieces; 1061, 1413, 1489). None claims a bound. No other issue or non-owner comment reported a bound between #763 and 06:10:44Z.
- SHA-256 at 964ee2b match think-cnn7 (upper_bounds.json 212b33b6, certified_bounds.json f368786a).

WHAT 43f666c CHANGES (certified_bounds.json 964ee2b -> 43f666c; 73eac5b and 1c17153 change no bound: 13 lane entries gain sha256_kind/decompressed_sha256 or credit text)
- 957 counts lowered, none raised. 227 and 260: same sides, certificates replaced by T-225's (Daniel's solved views), credited "Evan Daniel; start: Francisco Couzo" (evidence for think-mdfr; no bound).
- At or below 1024: 126 counts, 330-997. 108 own-count certificates, 1 deletion (690 from 691, -1 square), 17 L-border recipes (367 from 330; 444, 487 from 403; 632, 683 from 583; 732, 787, 844, 903, 964 from 679; 733, 788, 845 from 680; 737, 792 from 684; 744 from 691; 800 from 745). No change at or below 324 except 227/260; 268, 303 and 304 unchanged.
- Above 1024: 831 counts, 1027-9836, all "square tiling and L-border" recipes on 14 of the new certificates (679, 981, 984, 987, 988, 989, 991-996: 68 each; 975: 13; 997: 2). No certificate or deletion above 1024.
- Credit lines of the 126: Couzo after Lavrentev CUDA v11 76, after Tymchishin Alternating Reclosure v3 40, after kyleluecke ("inos-v0-6-k-mosh...", run 361592092) 3, after alexchilton ("fault-line-dp-basin-hopping-lb-22-3747", run 361412241) 2, after Tymchishin "22-3662..." 2, after aqibrazadev ("squares-in-squares-top-lb-blending-visualization", run 361516058) 1, after Polkovskyi 1, own 1 (plus the two Daniel rows). The commit: "Exact certificates for 111 counts from CT105's live records (coordinator, live sync and browser searches), credited to Francisco Couzo".
- README (56 counts, from 71): drops 21 counts where Kaggle board teams now report smaller sides, including 303 ("303 is pjmathematician's, submitted before our 3.5e-11 refinement": board 17.906978233833611, submitted 2026-10-23 11:56:49 UTC, 3.47e-11 above #763's exact side); holds 340, 679, 732, 787, 844, 903 ("board sides about 5e-12 below our packings re-certify them"). 268 stays "held by this project" against panpanpanda's board side 16.874361715872031 (23 Oct 14:48:22 UTC), 1.79e-12 below #763's side. 304's reported lane is now Amin's board side 17.924726031170107 (23 Oct 00:15:35 UTC); its verified lane is still fa6237e's certificate.

VERDICTS (exact Fractions; members from intake_ledger.tree_members(read_on=2026-10-24) on e5c1c64e3, Göbel to 1073; plus 964ee2b's own bound at each count, i.e. #763's rows)
- At or below 1024: all 126 below every tree member and below 964ee2b's side, which is the standing side at every one of them (964ee2b <= main at all 126). Margin below 964ee2b: 2.49e-14 to 1.33e-2, median 5.3e-9; 53 above 1e-6, 22 in 1e-10..1e-6, 51 below 1e-10. Margin below main: 6.65e-13 (792, PR C's f1ceee4 row) to 6.78e-2, median 2.57e-2.
  - Restate #763's row by the think-fwa9 ruling (below by < 1e-12, same 12-place print): 797 (8.4e-13) and 847 (2.5e-14), if PR A records #763's rows there. 459 is 8.5e-14 below but across a print boundary, so recorded, as 365 and 970 were.
  - 792: 4.6e-13 below 964ee2b's (which restated PR C) and 6.65e-13 below PR C's; a recipe, so held anyway.
  - Rows writable once measured: 106 certificates (108 less 797 and 847). Held: 17 recipes (D2 maintained construction checker, W7, as #763's 13), 690 (deletion, think-kzme).
- Above 1024: all 831 below the grid, below Göbel where it reaches (1027-1073) and below 964ee2b's side (8.8e-12 to 4.0e-3, median 4.2e-5; 136 below 1e-10). The comparison against Kingbird, Daniel, Barnett, Fang, #666, #715, #719 and #732 was not redone here; it is think-llit's walk, as for #763's 233.
- Every row is a later report by the same author at a count #763 already reported or published (a refinement of his own 964ee2b row); no issue claims any. By stage 1 ("a claim in scope that the request does not mention becomes an import of its own") they are an import of their own, walked after PR A's rows.

PRICE (cap 40 CPU-h)
- Files: 108 certificates at or below 1024 plus 691's for 690, in 111 changed best/ files of 12.1 MB raw (GitHub trees API sizes), about 2-3 MB in Git at Couzo's zlib ratio; the indexes (certified_bounds.json 8.7 MB, upper_bounds.json 15.0 MB, manifest) as in PR A's packet; 180 new parents (24.6 MB raw), of which only the new Kaggle sources' parents (kyleluecke, alexchilton, aqibrazadev, the 22-3662 run) are needed for credit.
- Replay of 108 files on both maintained routes with controls: about 0.25-0.3 CPU-h, about 10 min wall on 2 workers (basis: #715's 8.2 CPU-s per Couzo certificate).
- 17 + 831 recipes: seconds with the D2 checker (W7 slice); 690: seconds once think-kzme answers.
- No in-corpus entry, so no stage 4 review beyond the replay; no adoption (all beyond 324). Total about 0.3-0.5 CPU-h.

PROPOSED DISPOSITION
1. Import bead (new): "Import franciscouzo: 126 upper bounds at 330-997 and 831 L-border recipes above 1024, the live records since #763's pin, at 43f666c (no issue)". Packet at 1c17153 (or 43f666c), ledger directory upper-bounds-couzo-43f666c-2026-10-24 frozen at post-PR-A main, claims to 1024; the above-1024 rows join think-llit's walk as its latest report. Acknowledge on #763 and ask whether #763 extends to them.
   blocked_on: think-ptkk (its rows walk after #763's), think-llit for the 831 above 1024.
2. Evidence, no bound: 43f666c/73eac5b/1c17153's hash kinds and the 227/260 credit go to think-mdfr (#678); the 662 restored construction credits to #715's entry owner.
3. Read in intake-watch.yaml at 1c17153 naming the import bead; draft below.

FOR PR A (think-ptkk)
- 303: Couzo's later release 43f666c withdraws 303 from his README's list of claims, ceding it to pjmathematician's side-only board entry (submitted 23 Oct 11:56:49 UTC, before #763) as "submitted before our 3.5e-11 refinement". Its index still credits the certificate "Couzo after Lavrentev CUDA v11". When a later release changes the attribution, the bibliography key for that release records the wording (epistemics.md); ask Couzo before PR A's 303 credit and News go out. Daniel's 8a8879a also names Chris Deotte's public Kaggle packing, the same arrangement as #763's 303 parent within 2-4 squares (think-6r5p).
- 268: panpanpanda's board side (23 Oct 14:48:22 UTC) is 1.79e-12 below #763's exact side, and Daniel's source says the packing first appeared in Lavrentev's lightningv08 output (think-6r5p). Side-only entries are not reports by any current rule.
- 304: retain certificates/best/n304.cert from 964ee2b in PR A's packet (think-6r5p's import uses it as the first report at 304).
- PR A's verdicts at 268, 303 and its 198 rows to 1024 do not change: 43f666c is later. After both land, 43f666c's rows supersede #763's wherever both are recorded (at most 124 counts; 797 and 847 restate #763's).
- Aside, nothing new: 964ee2b's index is also below main at 88, 126, 199, 266, 267, 292 and 301 by about 1e-19, each credited to PingYou Ltd and first published at 4e4c8ce (15 Oct; 88 checked), which the 6b7391d read already classes as tighter rationalizations of exact sides the register states. 304 is the only other corpus count where 964ee2b is below main.

AUTHOR QUESTIONS (Couzo, for the #763 acknowledgement)
- Does #763 extend to 43f666c's 957 lowered bounds, or will they get an issue of their own? Who ran the "browser searches" among CT105's live records, and is the credit yours alone (as at 227)?
- 303: your 24 October README cedes 303 to pjmathematician's board entry. Does #763 still claim 303, and how do you want the record to credit it? Which came first, Lavrentev's CUDA v11 packing or Chris Deotte's public notebook packing (the same arrangement within 2-4 squares)?
- 268: Evan Daniel's notes say the packing first appears in Lavrentev's (lightningv08) CUDA Packing Search output, which was Tymchishin's EDA+Seam LP input. Should #763's credit name Lavrentev, and which notebook versions and dates?
- 304: your fa6237e certificate of Tymchishin's "CPU Alternating Reclosure" v3 packing (17.926898903393, unclaimed in #763): is Tymchishin its finder? (Daniel: finder unknown; earliest copy kozykappa's notebook.)

DRAFT intake-watch.yaml READ
  - url: https://github.com/franciscouzo/square-packing
    read_through: 1c1715399709bc955e9b402947ab8b52bbacdfc3
    read_on: '2026-10-24'
    bead: <the import bead>
    note: >-
      The six commits past the 6b7391d read. efef7d1, fa6237e and 964ee2b, pushed together
      at 2026-10-23T23:38:42Z, are #763's, which PR A's packet pins at 964ee2b
      (think-ptkk). 43f666c, 73eac5b and 1c17153 were pushed together at
      2026-10-24T06:10:44Z. 43f666c lowers certified_bounds.json at 957 counts, each below
      #763's side and every bound this record held: at or below 1024, 108 own-count
      certificates at 330 to 997, a deletion at 690 and 17 L-border recipes; above 1024,
      831 L-border recipes on 14 of those certificates. No issue or comment claims them;
      they are held for the import bead. 43f666c also adds the Kaggle per-puzzle
      leaderboard of 24 October to its public comparison, after which its README cedes
      303 to pjmathematician's side-only entry, 3.47e-11 above #763's side, and holds
      340, 679, 732, 787, 844 and 903. It and 73eac5b replace 227 and 260 by T-225's
      certificates, credited "Evan Daniel; start: Francisco Couzo"; 73eac5b and 1c17153
      state the kind of every external gzip hash, as Couzo's #678 comment of 06:11:30Z
      reports (think-mdfr), and change no bound. Nothing else to import.

blocked_on: think-ptkk, think-llit
