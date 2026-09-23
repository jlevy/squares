# Atlas Exports Receipt (W5 efficiency block, agenda-042, `think-6grx`)

Lane C of
[`agenda-042`](../../../../agendas/agenda-042-efficiency-block-the-development-cycle.md),
2026-09-23, against `main` at `f5c9c8453`. Measured by a delegated lane; nothing was
written to the tree and `--update` was not run.
The two `--update` walls it compares against, 4m46s and 4m43s, are the lead’s readings
from merging `main` into PR #221 the same night.

W5 efficiency block, 2026-09-23, tree `f5c9c8453`, on a shared 4-vCPU VM (contended
readings are marked).
“Measured” means a command produced it; “inferred” does not.

## Verdict

**For the atlas, the owner’s hypothesis, that checking the rasters and PDFs slows the
commit and merge cycle, does not hold.** Checking the rasters and PDFs takes under a
second and is off the pull-request critical path.
The time goes to regenerating and merging them.
Drawing the six exports takes ~20 s. An `--update` takes 4m45s because every update
rebuilds all 324 cases, even when the only change is the 6-character footer stamp.
Almost all of that rebuild is mpmath re-proving non-overlap for 141 Kingbird-derived
witnesses.

## 1. History (measured, `git log` over HEAD; the files first appear 2026-08-26)

| File | Current bytes | Versions | Raw MB | Packed MB |
| --- | ---: | ---: | ---: | ---: |
| `known-best-1-100.png` | 592,777 | 44 | 25.5 | 19.1 |
| `known-best-1-100@2x.png` | 1,289,680 | 28 | 34.7 | 22.8 |
| `known-best-1-100-card.png` | 220,298 | 27 | 5.7 | 4.0 |
| `known-best-1-100.pdf` | 84,700 | 42 | 3.3 | 2.7 |
| `known-best-1-324.png` | 2,428,367 | 18 | 42.9 | 32.0 |
| `known-best-1-324.pdf` | 496,600 | 18 | 8.9 | 7.5 |
| **Six exports** | **5,112,422** | **177** | **120.9** | **88.1** |

- **17% of the 525 MiB pack**, built up in 28 days.
  PNG and PDF do not delta, so each full regeneration adds ~5 MB. The two composite SVGs
  (62 versions, 214 MB raw) pack to **7.7 MB**. **2026-09-22 alone added 48 blobs** (8
  regenerations, 29.3 MB packed), against 24 blobs and 14.8 MB in the whole preceding
  week.
- **44 non-merge commits** touched the exports; **24 of 158** PR merges carried them.
  **9 of the 44 were pure regenerations:** five for data
  (`7b1e5d8ea a379b6ba8 f26966578 444574e22 3e27b28e6`), and four **stamp-only**, where
  the `release-stamp` line was the entire SVG diff
  (`affe97215 a3a95928a daae425fb 99c95b4fe`).
- **`DATA_REVISION` was re-pinned 5 times in the ~6 h after its rule landed**
  (`a4bdfae4c` at 17:47Z to `affe97215` at 23:53Z), each a full `--update`. Two re-pins
  followed a merge of main; three followed a data edit.
- **4 of 487 merges had both parents changing the exports.** Two were same-file
  conflicts: `d29342bb3` (2026-09-06, 4 files) and `1959611f5` (PR #221, 6 files).
  History cannot show conflicts that were resolved by rebasing.

## 2. Profile of the full rebuild

**`--check` never rasterises and never draws a PDF** (checked in the code).
`check()` compares the text outputs and reads each export’s receipt: the SVG’s sha256,
stored in a PNG `tEXt` chunk or after the PDF’s `%%EOF` (`_png_matches_summary`,
`_composite_pdf_problems`). Only `update()` calls cairosvg, and only for exports whose
receipt is stale. So the export drawing was timed separately.

**Run A: full `--check`, default jobs, 294.5 s wall (measured).** `vmstat 5` shows four
busy CPUs from 5 s to ~277 s (the per-case pool), then one CPU for ~17 s (the serial
tail). Another lane’s pytest contended the pool’s last ~60 s, so an idle run would be
nearer 280 s. This matches the lead’s 4m46s and 4m43s `--update` walls.
`wa` stayed at 0 throughout: nothing waits on I/O, and the pool workers are the only
subprocesses.

| Phase (cProfile, main process with pool, plus a serial sample) | Share |
| --- | --- |
| Per-case pool: 324 witnesses and 324 house renderings | **~246–272 of ~290 s wall (85–93%), ~1,000 CPU-s** |
| … `witness.numerical_check` (mpmath separating-axis margins: `_margin_summary`, `verify_packing`) | **~97% of per-case time** (380.7 of 391.7 s profiled, 36 cases) |
| … house rendering (`_render`), `witness_document` | 1.5%, 0.9% |
| Composite SVG assembly: 424 cards, serial | ~15 s (45.2 s under cProfile) |
| Byte comparison, receipts, manifest | < 1 s |

Of the 324 cases, 141 are Kingbird-derived (177 are exact-grid, 6 UnitSquare), and each
spends ~7 CPU-s re-proving non-overlap.
A re-pin changes none of this.
cProfile inflates code with many small calls the most, so read “97%” as “almost all”.
The same re-verification dominates the pull-request sample step, whose 36 cases include
20 Kingbird cases. That step’s export-receipt part is 0.42 s profiled, and that includes
parsing both composite SVGs.

**Exports drawn by cairosvg from the committed SVGs (measured, contended):**

| Export | Size | Wall s | CPU s |
| --- | --- | ---: | ---: |
| `1-100.png` | 2400×2896 px | 1.51 | 1.10 |
| `1-100@2x.png` | 4800×5792 px | 2.73 | 1.87 |
| `1-100-card.png` | 2400×1256 px | 1.30 | 0.97 |
| `1-100.pdf` | 25×30.17 in | 1.12 | 0.86 |
| `1-324.png` | 4224×4912 px | 9.92 | 7.05 |
| `1-324.pdf` | 44×51.17 in | 9.69 | 6.77 |
| **All six** |  | **26.3** | **18.6** |

So drawing the exports is **~20 s (~7%)** of an `--update`, and the 1-324 poster is 80%
of that.

**`--jobs` is parallel by default:** `worker_count` reads `PACK_JOBS`, or the CPU count
when run from a shell (4 here).
The gate sets `PACK_JOBS` to 2 in the sweeps job and the deep gate.
**The “36 s of user CPU for a 286 s wall” is an accounting artefact.** Python 3.14 on
Linux starts pool workers from a `forkserver`, so their CPU time never reaches the
shell’s `time`. In run A, `time` reported **user 17.3 s**, while `/proc/stat` showed
**~1,135 busy CPU-s** (~1,030 s net of the other lane).
The main Python process’s own `cutime` read 0 after the pool finished, so `uv run` is
not the cause.

## 3. CI on PR #221, head `affe97215` (runs 35800361316, 35800361306)

The PR wall was set by Packing validation at **194 s**. Its slowest jobs were `frontend`
(180 s), `suite-a` (173 s), `suite-b` (163 s) and `validate` (153 s). Certificate page
took 175 s.

| Where | What it does with the atlas exports | Cost | On the critical path? |
| --- | --- | ---: | --- |
| `sweeps` → `known-best atlas records and sample` | rebuilds 36 cases from source; **reads** the 6 receipts | 67.3 s step, 90 s job | **No**: 90 s of slack against `frontend` |
| … `render_composite_pdf --check` (concurrent group) | reads the PDF receipt | 0.72 s | No |
| `validate` → `README agrees with the directory` | README relative links must resolve | 2.13 s | No |
| Pages `prepare` | copies the committed exports into `site/`; draws none | inside a 24 s render | Pages yes, exports no |
| Pages `pdf` | draws the **explainer PDF** in Chromium, **not the atlas** | ~47 s of a 113 s job | No: ends 12 s before `typography` |
| Deep gate: `known-best n=1..324 atlas rebuild` | full `--check`; reads receipts only | 441 s (run 35770490854) | Off the PR surface |

No pull-request job rasterises an atlas export or draws an atlas PDF. The only unit test
that calls cairosvg draws `<svg/>`, and all of `test_known_best_atlas.py` takes 6.2 s.

## 4. What the exports cost the cycle (inferred from sections 1–3)

**Checking** costs ~1 CPU-s per PR and 0 s of PR wall.
**Regenerating** costs ~4m45s of local wall per `--update`, ~90% of it re-proving
unchanged cases.
PR #221’s merge of main paid that twice (9m29s), and the five re-pins of
2026-09-22 paid it five times (~24 min) to change a stamp.
**Merging** produced 2 binary conflicts in 30 days, each needing a full `--update`. The
**repository** gains ~5 MB packed per regeneration.

## 5. Options

| Option | Merge conflicts | Re-pin / regeneration | Check cost | OR-13 / OR-16 |
| --- | --- | --- | --- | --- |
| (a) restamp composites from retained witnesses | ~40 s to resolve | **~4m45s → ~40 s (est.)** | unchanged | kept |
| (b) stop committing rasters/PDFs | **gone** for the six | unchanged (the SVGs keep the stamp) | unchanged | kept |
| (c) `.gitattributes` merge driver | manual step gone; rebuild still owed | unchanged | unchanged | kept |
| (d) no data hash in committed exports | content conflicts remain | **re-pin → 0** | unchanged | kept |
| (e) raster/PDF check off `--fast` | none | none | **≤1 CPU-s, 0 s wall** | **breaks OR-13** |

**(a)** A card needs only its case’s `witness` and `frontier` (`_append_summary_card`),
and both are retained.
An `--update --composites` path could therefore draw both composites from
`witnesses/known-best/*.yaml` in ~40 s: a few seconds of YAML loading, ~15 s of assembly
and ~20 s of exports.
A stamp-only path could rewrite the one text node and redraw in ~20 s. After a merge,
the per-case files are text and merge line by line, so only the 2 SVGs and 6 exports
need redrawing. No check moves: the PR sample and the deep gate’s full rebuild still
guard the retained witnesses from source.
A variant memoizes `numerical_check` locally by witness content, so a plain `--update`
stops re-proving unchanged cases.
(a) does nothing about history growth.

**(b)** Drawing the exports at deploy time removes the six binary conflicts and ~5 MB
per regeneration, but not the re-pin rebuild.
Every relative link to an export would change: `README.md` embeds `known-best-1-100.png`
and links `@2x.png`, `1-324.png` and `1-324.pdf`, and `check_readme`
(`check_synopsis.check_links`) fails a missing relative target.
The links would become Pages URLs; the 1-100 PDF link already is one, and `@2x` is not
deployed. Also touched: `packing/atlas/known-best/README.md`,
`render_explainer.COMPOSITE_ASSETS`, the `pages.yml` path filters, the manifest’s raster
records, `tests/test_known_best_atlas.py` and `run_negative_controls.py`. Pages would
pay ~20 CPU-s per deploy, and reviewers lose GitHub’s image diff.

**(c)** Git has no built-in `ours` driver: each clone needs `git config
merge.<name>.driver`, and GitHub’s “Update branch” ignores it.
After an automatic take-ours, the receipt checks stay red until the exports are redrawn.
It is only worth adding after (a), as a convenience.

**(d)** The committed footer would print `v0.4.1`, and only Pages copies would carry
`v0.4.1-195961`. A re-pin becomes a one-line `release.py` commit, which would have
avoided all 5 rebuilds and all 4 stamp-only commits.
Content conflicts like `1959611f5` would remain.
This reverses the owner’s 2026-09-22 decision that the footer names the data revision.

**(e)** The check reads receipts: 0.72 s for the PDF and milliseconds for the PNGs,
inside a job with 90 s of slack.
Moving it saves nothing, and OR-13 forbids moving a cheap check.

## Recommendation

**Build (a) now.** Its ~40 s is an estimate, because the path does not exist yet.
It is the only option that removes the dominant cost, re-proving unchanged cases.
It helps re-pins and merges alike, moves no check (OR-13) and adds no checksum (OR-16).
**Put (d) to the owner**: it takes re-pins to zero.
**(b) is the follow-up if repository growth matters**; it is the largest change and
leaves rebuild time as it is.
**Do not do (e).**

## Tool gaps (OR-1)

- **No command times export drawing.** The export table came from a `python -c` that
  called `cairosvg.svg2png` and `render_composite_pdf.render_pdf_bytes` and wrote
  nothing. `--report --time-exports` would close the gap.
- **`python -m cProfile -m devtools.build_known_best_atlas` fails under the pool**
  because it pickles `__main__._build_case_unit`. Use `--jobs 1`, or
  `cProfile.run("b.main([...])")` after importing the module by name.
- **Shell `time` under-reports pooled tools ~60×** (forkserver).
  Read CPU from `/proc`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
