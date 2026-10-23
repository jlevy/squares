---
type: is
id: is-01m4qkwzyhsj3k6pjnnwya3tt4
title: "Import E. Summins: the simple-square climb at n = 17 and n = 19, a 2,500-class census and a compute request (#523)"
kind: task
status: open
priority: 1
version: 6
delegate: null
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-12T08:33:07.537Z
updated_at: 2026-10-23T06:15:56.388Z
started_at: 2026-10-12T08:52:51.256Z
---
https://github.com/jlevy/squares/issues/523 (2026-10-12T04:12:33Z, labels n-17, intake). Esummins/packing at 651a9a54688341880e9c0dc9fcfc19f2c04cd3cb: writeup/outreach/06-climb-17-19.md; attempts/A243-climb-17-19/ (census243_n{17,19}.json, verdicts243_n17.jsonl, certs/n17/ 276 spine certificates, code/). Census of slot-set classes at the T-043/T-065 and T-103 windows; k = 16 and k = 15 four-corner classes dead at the root at n = 17; a compute request for the descent and the climb. Touches the n = 17 lane (think-x4v4).

## Notes

## Stage 1 triage (2026-10-12, lane intake-esummins, worktree branch intake-esummins from l4 dead83f0e)

- Pin: Esummins/packing 651a9a54688341880e9c0dc9fcfc19f2c04cd3cb (master, committed 2026-10-12T04:11:54Z); head eb3ae15 adds only writeup/outreach/POSTED.md. Issue filed 2026-10-12T04:12:33Z, labels n-17 and intake. Licence: code MIT, documents and data CC BY 4.0. AI assistance: produced by Claude under the PI's direction.
- Claims mapped (stage 1 table):
  1. Theorem [T]: the census of slot-set classes at the windows n = 17 [116511/25000, 4675531/10^6] and n = 19 [193/40, 4885619/10^6] has 2,500 classes, 632 with all four corners. Re-counted here from the retained census243_n17.json and census243_n19.json: 2,500 rows each, census_d4_by_k = 1, 1, 3, 6, 17, 31, 64, 107, 177, 242, 319, 356, 374, 325, 256, 148, 73 for k = 0..16 (sum 2,500), four-corner rows 632 with the per-k counts the note gives (1, 1, 7, 14, 37, 57, 89, 103, 112, 91, 68, 35, 17 for k = 4..16); the record classes n17_k08_0156 and n19_k11_0236 are present. Where: a census/ledger note on n-017.md and n-019.md at most; no register entry.
  2. Certificate-backed [C: exact trace]: at n = 17 every four-corner class with k = 16 and k = 15 is empty on the window at the tree root, k = 14 in 67 of 68. Re-read from verdicts243_n17.jsonl: 120 rows, k = 16 DEAD 17, k = 15 DEAD 35, k = 14 DEAD 67 and ALIVE 1 (n17_k14_0215, wall), seconds summed 2,426; no k = 13 rows are committed at the pin (the note's "k = 13: 1 dead, 3 alive" is not in the file). The kills are traces of the A211 engine's leaf rules with no verifier clause (their own words). Where: a ledger note; no register entry (the `case-exclusion` kind exists, but the record acts on no bound here, and the trust base is an unreviewed engine). The spine certificates (248 files, 8.8 MB) are pinned by digest, not retained.
  3. Measured [M]: the record classes are first-order rigid (rigid243.py, an LP on the exact contact graph). n-017.md already records local rigidity with its own evidence; no record.
  4. The compute request (ask).
- Windows: s_lo at 17 is T-043's 116511/25000 (they note T-093's +2.75e-6 and keep the wider, weaker hypothesis, which is the stronger statement; Guzhou0806's R070/R071 above it are pending, think-1qms); s_hi 4675531/10^6 is an outward rational ceiling of T-065's 4.6755300936045509... At 19, T-103's 193/40 and 4885619/10^6 above Wainwright's 3 + 4 sqrt 2 / 3 = 4.8856180831... Both windows contain no integer, so the slot lattice is window-stable; consistent with the record.
- Price of the compute, from their measurements (06 section 4 and 5): remaining four-corner classes at n = 17, k = 13..5, 91 + 112 + 103 + 89 + 57 + 37 + 14 + 7 + 1 = 511, plus the root; walls 90 s at k >= 8, 300 s at 4 < k < 8, 1,800 s at the root; at the wall that is at most 489 x 90 + 22 x 300 + 1,800 = 52,410 s, about 14.6 CPU-h; --rewall at 1,800 to 3,600 s on ALIVE classes adds up to 1 CPU-h per alive class (1 of 68 alive at k = 14; 3 of 4 so far at k = 13), so 150 to 300 CPU-h is plausible per n if a quarter to a half stay alive; n = 19 the same again; the full census (1,868 more classes per n) beyond. Their "days to weeks" on two workers; here on four shared cores it is not a minutes job and needs an owner budget. Prerequisite: the kills are the lab's engine's traces, so a run here is reproduced with the producer's code on an unreviewed method; the leaf-rule soundness review (#527's ask, about a day) should come first or beside. Their code needs Python 3.11+, numpy and the flags A220_NOROOM_INHERIT=1 A221_LANE=1 A224_SNAP=1; the Windows priority calls are optional.
- How it touches the n = 17 lane (think-x4v4): labelled n-17; it is not a bound and does not touch the sub-pattern census ledger (exp-317, wand125's kernel rows), which stratifies the certificate's sub-patterns, not lattice-slot classes. It touches the lane by using T-043 and T-065 as its window, by asking for CPU on n = 17 beside the 4.7 CPU-hour budget on #543, and by offering a structural statement conditional on four flush corners ("every packing of 17 squares at side in the window with four flush corners contains Bidwell's pins" if the climb closes). Recommendation: think-x4v4 owns the compute decision; any run lands as a census/ledger note on n-017.md, not a register entry.
- Review route and price: the climb rule (Theorem FC's dichotomy as a spine node, Lemma K1 forward, the citation of DEAD extensions) in forced_corners.md, slot_crowds.md, instratum_bridge.md and climb243.md section 3: a mathematics-tier review of about half a day; the leaf rules shared with #527, one to two days. The k = 16 and k = 15 kills are near-trivial by hand (sixteen lattice slots with offsets <= 3 fill a 4 x 4 block and the window's side is below 5, so no room for a seventeenth unit square beside them), which is a cheap sanity check a reviewer can do first.
- Retained: packet esummins-packing-2026-10-12: attempts/A243-climb-17-19/{BRIEF.md, notes, code, results (census, verdicts, rows, climb tables, rigid), the two worker logs}; certs/n17 and the raw engine rows pinned by digest.

## Acknowledgement draft (stage 1; not posted)

@Esummins, thank you. Received: the n = 17 and n = 19 census and the n = 17 descent at [Esummins/packing@651a9a5](https://github.com/Esummins/packing/tree/651a9a54688341880e9c0dc9fcfc19f2c04cd3cb/attempts/A243-climb-17-19), pinned at that commit; the census files, verdict rows, code and notes are retained here and the spine certificates are pinned by digest.

What was checked: the census (2,500 classes, 632 with four corners, your per-k counts) and the verdict rows (17 of 17 at k = 16, 35 of 35 at k = 15, 67 of 68 at k = 14) were re-read from your files; nothing was run. The compute you ask for is priced from your walls at about 15 CPU-hours for the n = 17 four-corner descent at the first walls and considerably more with the re-walls, and it waits on an owner budget and on a review of the engine's leaf rules, since the kills are traces without a verifier clause. Your windows match the register's T-043, T-065 and T-103.

---
_Generated by [Claude Code](https://claude.ai/code)_

2026-10-12 09:00Z: packet committed on worktree branch intake-esummins at 7d4cc96c1 (not pushed); acquire_source --check PACKET_MATCHES_ITS_CONTRACT; proposed result-requests.yaml and intake-watch.yaml entries in the lane scratch file proposed-entries.yaml (reported to the coordinator), nothing applied to the shared records.

2026-10-13 owner decision: #523's n = 17 compute request (descent and climb at the T-043/T-065 window) is suspended pending Overbeck's proof (#560, #571); the intake record, the n = 19 part and the reply to E. Summins continue.
