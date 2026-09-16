# Video Spikes: The Sources, Not the Pages

Two prototypes built on 2026-09-07 and 2026-09-08 for the
[atlas video plan](../../../../../docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md),
under its Phase 0. They are retained here as **generators and records**, so that what
was learned is rebuildable rather than remembered.

**These are spikes, not the implementation.** The v2 generator, page and checks grew
into the workbench and moved to
[`packages/workbench/`](../../../../../packages/workbench/) at `15d97a59`; what stays
here is the v1 slideshow, the v2 notes and instruments, and two frozen outputs.
The Python here is held to the repository’s Ruff and BasedPyright floor and the
slideshow’s script to the browser floor, but no validation tier runs the slideshow’s
test or the instruments.
Read them as evidence for the plan’s decisions.

## What is here, and what is not

The generated pages are **not retained**. Built at `f3874426`, the slideshow is
3,520,936 bytes and the workbench (`index-all.html`, all 323 pairs) 4,806,337 bytes, and
the repository already declines to serve a 1.2 MB raster for resolution nothing
displays; two multi-megabyte generated documents would be the same mistake with a larger
number. Rebuild them instead, from `packing/`:

```bash
uv run --frozen --all-extras --group dev python \
    atlas/known-best/video/spikes/v1-slideshow/build_candidate.py --repo .. --out <dir>
uv run --frozen --all-extras --group dev python -m workbench_tools.build_candidate --out <dir> --all
```

Neither generator refuses to overwrite: each creates `--out` if needed and writes over
the files it names there.
Omitting `--out` is safe but not tidy: the slideshow then writes `index.html` beside its
source and the workbench writes to `packages/workbench/dist/`, and git ignores both.
Pass `--repo` to the slideshow, whose default is one machine’s absolute path.
The slideshow’s `test_candidate.py` asserts that two builds are byte-identical, and so
does `workbench_tools.check_candidate` for the workbench.
The published page is built by `squares-workbench-build` into
`packing/site/workbench/index.html`; the v2 instruments that open a page default to it,
except `calibrate.py`, which takes the page as its argument.

| Path | What it is |
| --- | --- |
| `v1-slideshow/build_candidate.py` | Reads the composite figure record, the frontier records and the 324 renderings; writes one self-contained page holding every packing |
| `v1-slideshow/test_candidate.py`, `timeline_harness.js`, `node-harness.d.ts` | The slideshow’s checks, with the stub-DOM harness its timeline test runs in |
| `v1-slideshow/render_review.py` | The slideshow’s review stills |
| `v1-slideshow/NOTES.md` | Sizes, the font composition, the fact provenance tables, the capture sketch, four revisions of owner feedback |
| `v2-transitions/NOTES.md` | The first build and its revisions through 16, with the measurements that answer the plan’s open questions; a dated correction at the top says what moved |
| `v2-transitions/transition-stats.json`, `v2-transitions/stats-summary.md` | **Frozen historical output**, last regenerated at `0281a508`: per pair, the matching method, the identity chain, block statistics, displacements and turns, and their summary. Nothing rebuilds them or compares them with a build. At `f3874426` a fresh record differed from this one only in `generated_by`; the summary’s closing run times omit `correct`, where the generator now prints the run time the page reports |
| `v2-transitions/calibrate.py`, `compare_palette.py`, `dump_fills.py`, `experiment_*.py`, `grade_motion.py`, `measure_*.py`, `smoke_styles.py` | The instruments that produced the measured tables in the notes |

The moved check, `workbench_tools.check_candidate`, is not run by any tier and fails on
stale text needles (`think-tn0j`). Its browser checks run only once every other
assertion passes, and on a build of `f3874426` they stop at their first call, because
`atlasTransitions` refuses calls outside the Animate view (`think-7sw8`).

## What the spikes established

- **The slideshow is cheap to capture.** About 42 ms per frame at 1080p and 145 ms at 4K
  in the project’s pinned headless browser, with repeated captures of one instant
  byte-identical, which is what makes a reproducible export possible.
- **Squares have no identity across packings**, so a correspondence has to be computed.
  Of the 323 consecutive pairs, 160 are exact prefixes, five are the catalogue’s own
  shared pictures, and 158 need a real matching.
- **Matching square by square looks wrong.** A tilted block returning to grid rows
  becomes a conveyor of one-unit hops.
  Matching blocks first and squares second puts 90 per cent of moving squares into rigid
  groups.
- **The physics does not find the packing.** Aimed straight at a known answer with the
  final snap disabled it still rests one to 1.7 units away per square and 0.1 to 1.1 per
  cent wide; run blind, with no targets at all, every genuinely packed case loses, by up
  to 6.8 per cent.
- **Shaking harder fixes orientations, not positions.** Raising the annealing dial more
  than halves the worst angle error twice over while the container side stays flat,
  which is the same defect the
  [annealing survey](../../../../../docs/project/research/research-2026-09-08-annealing-for-square-packing.md)
  names and the search campaign then measured directly.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
