---
type: is
id: is-01m5g8xj3hqca5wcen9f71dtnd
title: "Import franciscouzo: 1285 upper bounds at 328–9913 (#715)"
kind: task
status: in_progress
priority: 1
version: 6
delegate: coord-intake-1021b
labels:
  - result-import
dependencies: []
child_order_hints:
  - is-01m5ghbpszw0r22b4wm95vgkfr
  - is-01m5ghp413dqrnqz5w3ww2thdd
hold: null
hold_until: null
created_at: 2026-10-21T22:22:12.593Z
updated_at: 2026-10-22T00:55:25.968Z
started_at: 2026-10-21T22:22:13.353Z
---
Issue #715 (https://github.com/jlevy/squares/issues/715), opened 2026-10-21T20:55:57Z by Francisco Couzo as a follow-up to #678: 1285 strict improvements over the strongest retained public comparison (173 below 1024, 1112 above; first request above 1024), source commit 6b7391de820fd01f3ff6984e4a081e8c86845588 (upper_bounds.json, certified_bounds.json, certificates/best/manifest.json, public_bounds.json). Includes 343 at 18.977575126267, below #702's row registered today. Stage 0 owner; stage 1 triage (read-only, priced) first.
blocked_on: none

## Notes

2026-10-21 c-triage-715 (stage 1 triage, read-only, against main bb0c24e9f). The full
working files are in the coordinator’s scratchpad, triage-715/: claim-map.md, policy.md,
price.md and acknowledgement.md.

## Claim Map

**Source.** #715’s pin, franciscouzo/square-packing
6b7391de820fd01f3ff6984e4a081e8c86845588, is not public.
- `git ls-remote` shows only master, at 7b6c87e (#678’s pin).
- A fetch by hash answers “not our ref”, and the API answers 422.
- The repository has no tags, releases, pull requests or forks; pushed_at is
  2026-10-18T23:23:41Z.
- The four evidence links 404.

Stage 1 step 1 (pin) cannot finish, and stage 2 cannot start, until the author pushes or
names the ref. The #678 source patch (evand pin refresh, gzip/decompressed hash labels,
Daniel’s n260 certificate credit; think-xu4d’s ask) is not at 7b6c87e either:
bound_sources.json still pins evand at 0f37f49. #715’s body does not mention it.

**Counts.** 1285 rows: 173 at 328-996 and 1112 at 1033-9913. None is in the n <= 324
corpus, so there is no register entry; every row is a beyond-horizon row.

**64 of the 173 are already public at 7b6c87e, byte for byte.** Blobs were traced
through all 38 commits:
- 02f9690 (2026-10-09): 335, 336, 337, 341, 373, 374; owner think-a4wq/think-1545.
- f311f08 (10-11): 340; owner think-om5l.
- a7067d7 (10-12): 338, the identical blob 55c627a already on main as
  couzo-certificates-2026-10-12.
- 4e4c8ce (10-15): 56 counts from 410 to 988, 4 of them deletion rows; owner think-yfoo.

By the watched-repository rule these are reports from their first commits, not from
#715.
- 62 are below main and enter dated by those commits.
- 335 (18.822875655562) is 1.84e-11 above Couzo’s own 8 October decimal row and is not
  recorded.
- 338 ties the existing row, so it adds no row.
- All 55 rows that are below main by less than 1e-10 are in this group:
  re-certifications of his own 487b058 and 8 October packings.
- No other report sits at these 64 counts, so first-commit dating changes no verdict.

**1221 rows are new reports of #715** (109 at <= 1024, 1112 above), not in any public
commit. Each is decidably below main’s current row or the grid, and below every earlier
open report (#666, #670, #672, #675, #678, #686, #702). Margins at <= 1024 run from
3.85e-9 (496) to 0.172 (860).

**Ledger outcomes.**
- 343: #678 -> #702 -> #715, each below the last (#715 by 1.0736e-4), so all three are
  recorded. #715 becomes current, and #702’s row is superseded.
- Muglich’s #686: #715 is below all 50 of his current rows it meets (328-996), by
  3.85e-9 to 7.45e-3.
- #666 above 1024: #715 is below at 1061, 1266, 1339, 1413, 1489 and 1568 (4.1e-10 to
  1.48e-4), three of them refinements under 2e-9.
- #715 is below all 120 pending-report claims at its counts.
- All 1285 prints are below Gobel’s squares and strips with deletion through 9913, so
  #613 holds nothing back.

**Certificates.** One certificate per non-deletion row reproduces exactly the 60 files
7b6c87e holds for the public rows.
On that model:
- 98 new certificates at <= 1024 (68,879 squares; about 12 MB checkout, 4.4 MB as Git
  stores it);
- 316 above 1024 (1.39 million squares; about 251 MB checkout, 89 MB zlib);
- the lower bound above 1024 is 83 (25 MB zlib).

## Priced Plan

The model is measured here: couzo_678_replay’s filtered two-route decision with six
controls costs 11.8 CPU-s at n=998, 71.7 at n=3992 and 214.4 at n=8982, scaling as
n^1.33.
- **V0, the public 64:** 60 files at about 7 CPU-min, plus an exact check of the 8
  October decimal poses at 335-374. Runnable now from public pins, through think-yfoo,
  think-a4wq and think-om5l.
- **V1, 98 new certificates <= 1024:** about 12 CPU-min.
  Runs in the stage 3 branch on push.
- **V2, 83-316 certificates above 1024:** 2.3-8.1 CPU-h (0.2-0.8 positives only).
  Under the 40 CPU-h item cap, but in CPU-hours: open a validation bead under think-cyal
  and add a backlog row.
  Gated on D1, D4, S1, S2 and the push.
- **V3a, all-pairs cross-check at 343, 996 and 1061:** about 20 CPU-min, with V1.
- **V3b, all-pairs <= 1024:** 6-16 CPU-h, optional; recommend skipping.
- **V3c, all-pairs above 1024:** 300-2,700 CPU-h, over the kernel’s 600 s job ceiling.
  Held, not proposed.
- **Code slices.**
  - S1: a filtered certify for any packet, reading pinned-only or hosted bytes.
  - S2: a deletion/L-border/tiling recipe checker with its lemmas stated.
  - S3: Gobel comparison to n=10,000.
  - S4: the claims record at about 1,285 rows (check_source_coverage takes 2.5 s today).
- **Split.**
  - Now: land stage 1 (#715’s result-requests entry), then post the acknowledgement
    after merge. Fold in V0 if the coordinator agrees.
    Build S1 and S2.
  - On push: stage 2 packet, retaining the <= 1024 certificates and pinning the rest by
    digest; the ledger; V1 and V3a; record the 109 rows.
  - If D1=A: record the 1112 rows above 1024 from exact header sides, as the 487b058
    precedent did, with V2 in its bead.
- **Found in passing:** the filtered route re-prices think-yfoo (held at about 45 CPU-h)
  and think-2d7f (held at 38-48 CPU-h) at about 40 CPU-min each.

## Owner Decisions Needed

- **D1. Track counts above 1024?** No rule sets a ceiling: the schema has n >= 1 with no
  maximum, and the frontier README says every claim of a retained source is accounted
  for. But the record holds none above 998, and #666 waits on the same question.
  Recommend A: in scope, no ceiling, rows recorded as reported.
- **D2. Recipe rows.** Do L-border or tiling rows with no certificate file of their own
  become rows? Deletion has precedent (#678’s 545 and 641); L-step corollaries do not
  (#584 asked for none).
  Recommend yes, decided exactly from the recipe (S2), and write the rule into
  frontier/README.md; 4e4c8ce’s deletion bounds wait on it too.
- **D3. 335.** Recommend no key reason.
  Check the 8 October decimal poses exactly.
  If they fail, bring the owner a deferred-conflict correction.
- **D4. Hosting.** The certificates above 1024 are bulk data under OR-18 (25-89 MB as
  Git stores them). Recommend staging a hosted-data manifest in the stage 2 PR; the owner
  publishes data/couzo-715-certificates-v1 before V2.
- **D5 (existing, #686’s ask).** Per-row credit beyond the horizon covers 343, Muglich’s
  50 counts and #666’s six.

The acknowledgement draft asks the author four questions:
1. Push 6b7391de or name its ref; does it carry the #678 patch?
2. Certificate files versus recipes above 1024, and their size.
3. Lineage: 343 (Daniel/Fang), the #686 counts, de Winter’s 1061-1568.
4. 335 versus the 8 October decimal report.

The author’s push of 6b7391de cannot be a blocker ref: the sweep resolves only issues,
pull requests and beads.
It will surface as a new commit in the sweep’s franciscouzo/square-packing watch
(read_through 7b6c87e).

<!-- Coordinator: open one bead for the owner's D1-D4, then append the closing line below
with its id. Do not append the placeholder as written: a blocked_on line that names no
issue, pull request or bead reads as no wait. -->

2026-10-22 00:50 coord-intake-1021b: 6b7391de is public (Couzo, #678 23:26Z). Acknowledgement posted https://github.com/jlevy/squares/issues/715#issuecomment-6329883508 after #716 entered #715 at triage pending (deploy run 39700175588, check_published_site 4784/4784). It promises an exact check of the 8 October decimal poses at 335. Import of rows <= 1024 under way on claude/intake-2026-10-22 (c-lane-715-import), which also records the acknowledgement and the #678 follow-up. Rows above 1024 wait on the owner (think-f2io).
blocked_on: think-f2io
