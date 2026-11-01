---
type: is
id: is-01m5jkkavda6rk0m0qvgt4dkva
title: "Import Mishapolk: 5,468 certificates 328–10000 at 814fbe9, '#715 resolution' and a boundary-saturation proof claim (#732)"
kind: task
status: open
priority: 1
version: 13
spec_path: docs/project/specs/active/plan-2026-10-24-rows-above-1024.md
delegate: null
labels:
  - result-import
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-22T20:07:20.685Z
updated_at: 2026-10-31T11:17:55.965Z
started_at: 2026-10-23T02:12:17.764Z
---
Issue #732 (https://github.com/jlevy/squares/issues/732), opened 2026-10-22T19:55:03Z by Mishapolk (Mykhailo Polkovskyi): "328–10000: Registration Request (5,468 Exact Rational Certificates), Complete Resolution of Couzo #715, and Algebraic Boundary Saturation Proof". Source Mishapolk/square-packing-records@814fbe9129b7abb301923cc50de621697a53940f (upper_bounds.json, certified_bounds.json, certificates/manifest.json, certificates/census.json with digests in the issue).
From the stage 7 lane after #722 (repo moved past dc440a88): 8a488a1 (19:08:59Z) and 3285fac (19:29:30Z) reorganize certificates/ into thousands folders holding files at 5,594 counts up to 9,913 (126 in the corpus, 390 at 325–1024, 5,078 above 1024); 814fbe9 (19:37:33Z) changes four index JSONs; at 31 of #719's 122 counts the new file states a lower side (7.5e-13 to 8.19e-2, largest at 366); the three failing files and the lower n204.cert are gone; BOUND_VERIFIER_LICENSE.txt is an MIT licence naming Evan Daniel (verifier licence, not the certificates').
Stage 1 triage (read-only) next: c-triage-1022d. Rows above 1024 wait on the owner (D1, think-f2io).
blocked_on: none

## Notes

2026-10-22 c-triage-1022d (stage 1 triage, read-only). Read against `main` `cacdafc1f`
(#722's merge; `origin/main` `4432f51b5` changes no record), #730 at `9118d093f` with the
#730 triage's `planned-rows.json`, and #731 at `3213910d5`. The full working files are in
the coordinator's scratchpad, `triage-732/`: README.md, claim-map.md, price.md and
acknowledgement.md, with band-rows.tsv, the receipts and `tools/` beside them.

**Source.**

- `Mishapolk/square-packing-records@814fbe9` (19:37:33Z) is the head, `main`, and tag
  `v1.0.0`.
- All five digests in the issue match. The release asset's GitHub digest matches too
  (metadata only; not downloaded).
- Custody holds for all 516 files at or below 1024: header, rows, `SHA256SUMS`, manifest
  path, digest and side.
- The licence is Couzo's copy of Daniel's MIT verifier licence: same blobs as
  `franciscouzo@6b7391d`. It does not cover the certificates, so the import is
  derived-only, as for #719.
- Four issue edits by 20:07:33Z, all cosmetic or the release link.

**Files.** 5,594 `nN.cert`: 126 in the corpus, 390 at 328–998, and 5,078 at 1025–9913.
The manifest and census list the 5,468 beyond the corpus.

**Report order** (exact; earlier reports are `main`'s rows, Couzo's, Daniel's and Fang's
publications, and Mishapolk's own files):

| Disposition at 325–1024 | Rows |
| --- | ---: |
| Recorded: new at `8a488a1` (19:08:59Z), by 7.5e-13 to 7.4e-4 | 76 |
| Recorded: 539, `1851c2c`, one of #719's withdrawn rows, claimed again | 1 |
| Held, sub-print (`think-fwa9`): 499, 8.66e-13 below #719's row, same print | 1 |
| Held on #730's index classes: 369 and 376 (`58a7833` recipes, D2); 985 (ties #730's `4e4c8ce` deletion row) | 3 |
| Restates #719's rows | 81 |
| Not recorded: ties 49, above 178, and 335 (D3) | 228 |

- The 77 recorded rows supersede on `main` 29 of #719's rows, 30 of #715's and 18 of
  Couzo's `487b058` rows. After #730, 14 of them supersede #730's `4e4c8ce` rows
  instead.
- All 78 below every earlier report (with 499) are below Göbel.
- The precedents on 499 disagree. #722 recorded #719's 631 in the same class (2.73e-13
  below, same print). Recommended: hold 499 with #730's `SUB_PRINT`.

**In the corpus: nothing.**

- Every in-corpus side was published at or before `1851c2c`, and none is claimed (all
  `reference`).
- No file is below the least of the house, the reported lane, the candidates, T-229 and
  T-230.
- 105 and 204 are T-229's own files, byte for byte.
- 45 are below the house's verified side:
  - the two T-229 files;
  - 42 Kingbird re-rationalizations, 1.35e-36 to 7.23e-15 below, within one unit of the
    reported print, identical in arrangement;
  - 207, above T-174's algebraic side.
- All 45 pass both routes, with both refusing 6/6 controls (triage, 78 CPU-s).
- 303 is above T-186 by 1.79e-20 and above T-230 by 1.86e-4.
- No stage 4 review and no adoption.

**#715.**

- Below every #715 print.
- Exact at 173 counts at or below 1024: below 93, equal 37, above 43 (1.1e-18 to 2.3e-13).
  "0 tied, 0 worse" is false.

**The theorem.**

- Prose only.
- Lemma 1 is T-163's gluing (AMS21).
- Theorem 1 is a closure of the source's own index, verified (`tools/closure.py`), and
  bounds no s(n).
- Corollary 1's and the census's s(N) = ⌈√N⌉ is asserted; it does not follow.
- No entry, no review lane.

**Above 1024.** 5,078 rows wait on D1 (`think-f2io`). 3426 is above its grid side.

**Plan.** One records PR after #730, stacked on it or after it merges:

- the packet `mishapolk-issue732-2026-10-22`, derived facts;
- a release that reads rows from the pinned manifest (W7: a manifest reader, or #730's
  declared rows);
- a ledger;
- 77 rows;
- the filtered replay with six controls (about 20 CPU-min, or 94 for all 390), the
  all-pairs kernel at 499, 752 and 995 (13 to 35 CPU-min), and Göbel;
- the reply.

Under 2.1 CPU-h: in-branch, no validation bead.

**Ask the author:**

- per-row parents (samples re-solve #715's 645, 752 and 931 and #719's 499);
- a licence for the certificates;
- whether s(N) = ⌈√N⌉ is claimed as a lower bound.

#719's questions 2 to 4 stand.

blocked_on: #730 (both edit source-coverage.yaml and beyond_horizon_replay.py, and its
holds decide 369, 376, 985 and 499)

2026-10-23 c-lane-sweep-1023a (sweep of 00:10Z).
- Requests entry for #732 added by claude/intake-bookkeeping-2026-10-23: kind result-report, triage done (the stage 1 triage of c-triage-1022d), read_through 2026-10-22T19:55:03Z (no comments), results rows-325-1024 (queued, blocked_on jlevy/squares#730), rows-above-1024 (queued, blocked_on think-f2io), issue-715-resolution, saturation-argument and ceiling-census (not registered, not queued), and the ask to cap tracking at N = 10,000 (queued on think-f2io). answer_bead think-0gp6; replies [].
- intake-watch.yaml read of Mishapolk/square-packing-records through the head 17cc220131360ef290750eb845a3544c30ccb389 (2026-10-22T20:15:36Z), bead think-0gp6: 8a488a1, 3285fac and 814fbe9 are #732's release; 17cc220 adds only LICENSE (MIT, copyright Mykhailo Polkovskyi). git diff 814fbe9 17cc220: A LICENSE, nothing else, so a packet pinned at 17cc220 holds the same certificates with their licence.
- What the licence changes in the plan: the triage's "derived-only, as for #719" rested on there being no certificate licence. The author's comment on #719 (6350348588) says 17cc220 covers every certificate, catalogue, manifest and tool. The import may retain the files; --source-bytes headroom (about 5.0 MB under the cap at #722) and OR-18 still decide what goes in Git.
- The same comment claims #719's ten withdrawn rows (411, 451, 494, 495, 539, 540, 583, 587, 632, 683) as part of #732. The triage's walk already covers those counts.
- The drafted acknowledgement (triage-732/acknowledgement.md) needs three edits before posting: its Licence paragraph ("does not cover your certificates ... derived exact facts") and question 2 (a licence) are answered by 17cc220; the "#719's other questions ... stay open" line should say the withdrawn rows are now claimed here; and it should name this PR as the one carrying the triage.

2026-10-23 01:25Z coord-intake-1021b: #739 merged (4ad09803c) with #732 triage entry. Stage 1 acknowledgement posted: https://github.com/jlevy/squares/issues/732#issuecomment-6355073019 (edited for 17cc220 MIT licence, ten re-claimed rows, #719 answers). Record this reply under #732 replies (kind acknowledgement, 2026-10-23) in the next records PR. Import of the 77 rows waits on #730; pin 17cc220.

2026-10-23 02:12Z coord-intake-1021b: blocker resolved: #730 merged as fcf2f96a5. The 77-row import of #732 at 325-1024 can start (redo the report-order walk against main with #730 rows; pin 17cc220 under the MIT licence; rows above 1024 stay held on think-f2io).

2026-10-23 c-lane-732-import-1023: the import is draft PR #742 (claude/intake-732-mishapolk-rows, head daf940b42), labels intake and S2.
- Pin 17cc220 (adds only the MIT LICENSE to 814fbe9); the head moved to 7b6366f (01:50:22Z), which only withdraws 3426, so the packet stays at 17cc220, whose indexes carry the issue's five digests. Packet mishapolk-issue732-2026-10-22 retains the 77 recorded certificates, README and LICENSE (9.3 MB; 1.98 MB thin pack, check_added_blobs PASS) and pins the other 313 at 325-1024 and the indexes by digest; receipts/source-history.json holds all 390 to manifest.json.
- Walk upper-bounds-issue732-20261023 from starts frozen at main fcf2f96a5, each row at its exact side (new: intake_ledger reads a beyond-horizon start at the exact side its source states), with Mishapolk's own earlier files and every watched publication below the starts. Same outcome as the triage: 77 rows (76 at 8a488a1, 539 at 1851c2c), all current, superseding #715 30, #719 29, couzo-index-2026-10-15 14, couzo-verified-bounds-2026-10-14 4; 499 recorded and held SUB_PRINT (think-fwa9); 81 restate #719. What #730 changed: 369 and 376 rest on 58a7833's bound held GOEBEL_ABOVE (think-8krd), not a recipe hold; 985 rests on 4e4c8ce's deletion bound (D6). 129 #732 verdicts rest on holds (Göbel 43, recipe 41, sub-print 31, deletion 14); held-dependents: a D6 answer leaving deletion bounds out would record 985, nothing else of #732's flips.
- New: the walk also records the author's 1851c2c files at the nine other withdrawn counts (411 451 494 495 540 583 587 632 683), below every earlier report and above #732's files; held in a new class WITHDRAWN on new decision bead think-8m4k. No verdict rests on them.
- Replay: all 77 verified on both routes, 462 controls refused by both, 82.0 positive CPU s (6.5 min wall); all-pairs at 645, 752, 995 agrees (984,581 pairs, 322.5 CPU s); check --issue 732 --replay OK.
- Requests: #732's acknowledgement and the author's 01:52:47Z comment (read as edited 01:53:19Z) recorded, n499/n985 split out; the four stage 7 replies after #730 (#715, #686 correction of 6350116497, #607, #624) recorded.
- Stage 7 reply drafted in the coordinator scratchpad replies/732-rows/ (not posted).
- Not mine, for the owner/coordinator: Mishapolk's new comment on #719 (issuecomment-6355484781, 01:52:40Z) answers #719's open questions (verify.py called as a module; 204 seeded from Couzo's #678 n204.cert in Couzo's frame) and is unread in #719's requests entry.
2026-10-23 03:5xZ c-lane-732-import-1023: #742 at head e5c4db328, after merging main 6c70d843f (#731) and 31584003e (#737); hosted packing-required and pages-required green there (and at 0e08ecffe). The first run at daf940b42 failed suite-d (test_upper_bound_reports_715 now expects #732's 30 supersessions) and suite-a (a builds-on-project credit names Levy), fixed in 1f3a9b178, and suite-c on a 45.57 s call of test_upper_bound_packets::test_the_records_are_what_the_apply_tool_writes, which takes 11.9 s on main and 11.6 s on the branch locally (runner). Also recorded: #728's final reply (state closed, closed 2026-10-23) and #526's correction; check_requests --github shows no reply missing (unread: #719 6355484781 and #734 6355791263, not this import's). The survey's no-change record re-measured against 31584003e (v0.2.7, 43 files byte-identical). At merge: if #736's landings.yaml is on main, merge main and run stamp_landed --apply, then release_pin --update. Stage 7 reply draft: coordinator scratchpad replies/732-rows/732.md (DATE to fill).

2026-10-23 coord-intake-1023: after #742's merge (598d23289) and its verified deploy (run 39919775813), posted: #732 verdict https://github.com/jlevy/squares/issues/732#issuecomment-6360316121; #732 import reply https://github.com/jlevy/squares/issues/732#issuecomment-6360316595; #715 follow-up https://github.com/jlevy/squares/issues/715#issuecomment-6360316942; #719 follow-up https://github.com/jlevy/squares/issues/719#issuecomment-6360317345 (bodies in the coordinator scratchpad replies/, edited from c-drafts-1023's drafts to main's credit line and recorded answers). Recording rides the #719 records PR (claude/intake-2026-10-23). #732 stays open on 985 (D6), the rows above 1024 (think-llit) and per-row credit (D5).

2026-10-24 coord-intake-1024: #730 merged and the f1ceee4 import landed (#769). What #732 still waits on: the rows above 1024 (think-llit's code PR and walk), 985 and the deletion question D6 (think-kzme), and per-row credit beyond the corpus (D5, think-f2io). Released from c-lane-732-import-1023 (no live lane).
blocked_on: think-llit, think-kzme, think-f2io

2026-10-31 bold-ritchie-l6 (stalled-bead triage of the 31 October intake pass, think-ztcy): Waits on the owner: #732's rows above 1024 are recorded by think-llit's walk (bold-ritchie-l4, live on 31 October), which needs D4 (hosting the certificates above 1024) and zenodo.org access for the #836 and #847 deposits it must read; per-row credit (D5, think-f2io) and the deletion-bound rows (think-kzme) are the owner's too. Nothing here runs before then.
