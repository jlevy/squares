---
type: is
id: is-01m5jkkavda6rk0m0qvgt4dkva
title: "Import Mishapolk: 5,468 certificates 328–10000 at 814fbe9, '#715 resolution' and a boundary-saturation proof claim (#732)"
kind: task
status: open
priority: 1
version: 2
labels:
  - result-import
dependencies: []
created_at: 2026-10-22T20:07:20.685Z
updated_at: 2026-10-22T20:49:09.692Z
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
