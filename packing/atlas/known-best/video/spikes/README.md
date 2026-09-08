# Video Spikes: The Sources, Not the Pages

Two prototypes built on 2026-09-07 and 2026-09-08 for the
[atlas video plan](../../../../../docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md),
under its Phase 0. They are retained here as **generators and records**, so that what
was learned is rebuildable rather than remembered.

**These are spikes, not the implementation.** They do not meet the repository’s lint
floor or module boundaries, they are not wired into any validation tier, and the plan’s
Phases 1 and 3 re-implement what they proved under project conventions.
Read them as evidence for the plan’s decisions.

## What is here, and what is not

The generated pages are **not retained**. The slideshow is 3.5 MB and the transitions
workbench is 2.9 MB, and the repository already declines to serve a 1.2 MB raster for
resolution nothing displays; two multi-megabyte generated documents would be the same
mistake with a larger number.
Rebuild them instead:

```bash
# from this directory, with the project interpreter
../../../../.venv/bin/python3 v1-slideshow/build_candidate.py --repo <repo root> --out <empty dir>
../../../../.venv/bin/python3 v2-transitions/build_candidate.py --out <empty dir> --all
```

Both generators are deterministic: the same inputs give byte-identical output, which
their own tests assert.
`--out` refuses to overwrite, so point it at an empty directory.

| Path | What it is |
| --- | --- |
| `v1-slideshow/build_candidate.py` | Reads the composite figure record, the frontier records and the 324 renderings; writes one self-contained page holding every packing |
| `v1-slideshow/NOTES.md` | Sizes, the font composition, the fact provenance tables, the capture sketch, four revisions of owner feedback |
| `v2-transitions/build_candidate.py` | Computes the correspondence for all 323 consecutive pairs and writes the workbench |
| `v2-transitions/template.html` | The page itself: three animation styles, the annealing dial, the snap and blind modes, the gap bar, two tabs |
| `v2-transitions/transition-stats.json` | The computed record: per pair, the matching method, the identity chain, block statistics, displacements and turns |
| `v2-transitions/NOTES.md` | Eight revisions, with the measurements that answer the plan’s open questions |
| `*/test_candidate.py`, `check_*.py`, `measure_*.py` | The checks and the instruments that produced the measured tables |

Two of the transition tests’ text needles are stale against the current template and are
left alone deliberately; the notes say which.

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
