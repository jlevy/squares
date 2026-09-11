---
title: The Workbench, From Spike to Product
description: Converting the retained v2-transitions prototype into project code, without changing what it draws or how it deploys
author: Claude (agent), for the repository maintainer
---
# Feature: The Workbench, From Spike to Product

**Date:** 2026-09-11

**Author:** Claude (agent), for the repository maintainer

**Status:** Planned; no chunk started

**Workflow:** W7 pipeline improvement

**Tracking:** `think-ooi2` (epic)

## Overview

The workbench is the page the owner uses, the page the video is captured from, and the
page published at `/workbench/`. It is also a retained spike: excluded from the lint
floor, run by hand, drawing with its own copy of the palette, and carrying a banner that
says so. Those two facts cannot both keep being true, and this is the work that ends the
second one.

**Nothing here changes what the page draws.** Every chunk is a move, a generation or a
check; the rendered page is expected to stay byte-identical through all of them except
where a chunk says otherwise, and `build_workbench_site.py --check` is what says it did.

## Non-Goals

- **No redesign.** The panel’s layout, the colour scheme, the physics and the beat are
  out of scope. Design changes are cheaper in one template than across split modules, so
  they belong before this work or after it, not during.
- **No change to how it deploys.** See below: the deployment is already the one we want.

## Background

### The deployment is already the real one

Worth stating first, because “still a spike” and “not really deployed” sound like the
same problem and are not.

`devtools/build_workbench_site.py` writes the page into `site/workbench/`;
`.github/workflows/pages.yml` builds it with `--check` before the artifact upload, so it
must reproduce itself byte for byte and pass its own self-containment check; Pages
serves `packing/site` whole, so it lands at `/workbench/` while the explainer keeps `/`;
and the workflow’s path filter names the page’s inputs, held there by two tests.

**This work changes what feeds that pipeline, not the pipeline.**

### What it costs, measured

| file | lines |
| --- | ---: |
| `template.html` | 5,704 — 5,046 script, 393 style, 265 markup |
| `check_workbench.py` | 2,516 |
| `build_candidate.py` | 1,512 |
| `test_candidate.py` | 1,032 |
| eight instruments and checkers | ~1,850 |
| **total** | **~13,700** |

**The lint number is mostly noise.** Dropping the exclusion reports **1,691 findings**,
of which **1,426 are `E501 line-too-long`** and **168 are `T201 print`**. Both are
settings rather than work: `print` is already allowed in `devtools`, `cases`, `tests`
and the console scripts, and this is exactly that kind of tooling; line length is the
formatter’s. That leaves about **97 real findings**, and their top categories are
mechanical — `zip` without `strict`, non-lowercase locals, manual list comprehensions,
boolean positional arguments.
Ruff fixes 12 directly and 209 more under `--unsafe-fixes`.

**The palette is 120 literals**: 20 hues and a 100-entry shade ramp, copied from
`sqpack.render.style` and `sqpack.render.color` and kept in step by hand.
`compare_palette.py` measures that they still agree, which is a check standing in for a
guarantee.

### The one genuinely hard part, and it is not the line count

**JavaScript and HTML live inside Python, in both directions.** `build_candidate.py`
emits the page’s markup from Python strings, and the five checkers embed about two and a
half thousand lines of JavaScript in Python string literals to drive the page.

That is why no checker can lint the page’s script, and it is not theoretical: a `\le`
written as `\\le` inside an f-string reached the rendered page and set `s(11)` on one
line and its own bound on the next, because nothing between the author and the browser
could read the string as code.
Several edits in the session that produced this plan broke on the same seam.

**No auto-fix touches this.** It is the bulk of the work and it gets its own chunks.

## Design

### Five chunks, lettered as the beads letter them

Chunks A, B, C and E were already beads before this spec; D is new, and it is the one
the owner named as a rule rather than as an option.
Each chunk owns a disjoint set of files, so three of them can run at once.
The rule for delegated work is the project’s: **a delegate owns its file list, writes no
commits, and the coordinator re-verifies and commits.**

**D — no JavaScript or HTML inside Python** (`think-7f3p`). Two halves, each landing on
its own.

- **D1, the page’s script and styles leave the HTML.** `template.html` keeps its 265
  lines of markup and gains `assets/workbench.js` and `assets/workbench.css`;
  `build_candidate.py` inlines them at build time exactly as it inlines the faces.
  Owns: `template.html`, `build_candidate.py`, `assets/*`. Done when: the built page is
  byte-identical to the one before the split, and the script is a file a checker could
  read.
- **D2, the checkers’ probes leave Python.** Every `page.evaluate("() => { ... }")`
  becomes a `.js` file the checker loads.
  Owns: `check_workbench.py`, `check_revision6.py`, `check_revision7.py`,
  `check_legend.py`, `test_candidate.py`, `probes/*.js`. Done when: each checker reports
  the same result and the same printed measurements as before, and no JavaScript is
  written inside a Python literal.

**B — the Python comes under the floors** (`think-vi3v`). The spike’s exclusion goes and
what falls out gets fixed; ruff’s own `--fix` and `--unsafe-fixes` do most of it.
Owns: the ten instruments — `compare_palette.py`, `grade_motion.py`, `measure_law.py`,
`measure_greens.py`, `capture_stills.py`, `smoke_capture.py`, `smoke_styles.py`,
`dump_fills.py` and the two `experiment_*.py`. Done when: `packing-validate --edit`
covers the workbench’s Python.

**A — one source for the palette** (`think-fk8h`). The 120 literals are emitted from
`sqpack.render.style` and `sqpack.render.color` at build time, so a palette change
reaches the workbench the way it reaches every other drawing.
Runs after D1, because it edits the extracted script rather than the template.
Owns: `build_candidate.py`, `assets/workbench.js`. Done when: no colour constant in the
page’s source is written by hand, and `compare_palette.py` still reports every sampled n
reproducing its rendering exactly.

**C — the gates run where gates run** (`think-tmqs`). `check_workbench.py` becomes a
step in `packing-validate --fast` with a declared budget, like every other.
Owns: `src/sqpack/cli/validate.py`. Done when: a change to the page that breaks the
colouring fails a pull request.

**E — it lives where the code lives, and the banner comes off** (`think-g0lh`). The
generator becomes `devtools/build_workbench.py`, run with `python -m`; the instruments
become `devtools` modules; the exclusion in `pyproject.toml` goes; the prototype banner
comes off. Owns: `pyproject.toml`, `.github/workflows/pages.yml`, the tree move.

**The banner is last on purpose.** It is what makes the current state honest, and taking
it off before the rest would make the page claim something that is not yet true.

### What could go wrong, and what catches it

| risk | what catches it |
| --- | --- |
| The split changes the rendered page | `build_workbench_site.py --check` plus a byte comparison against the pre-split build |
| A checker’s probe changes meaning when it leaves Python | each checker reports the same pass and the same printed measurements as before |
| The palette emitter disagrees with the copy it replaces | `compare_palette.py --per-n`, which already compares the page against the renderings |
| The move breaks the Pages build | `pages.yml` builds on pull requests, where nothing deploys |
| Three agents collide | disjoint owned-file lists, and no delegate commits |

## Implementation Map

| # | chunk | bead | owns | change |
| --- | --- | --- | --- | --- |
| 1 | D1 | `think-7f3p` | `template.html`, `build_candidate.py`, `assets/*` | Script and styles out of the HTML; the build inlines them. |
| 2 | D2 | `think-7f3p` | the five checkers, `probes/*.js` | Every embedded probe becomes a file. |
| 3 | B | `think-vi3v` | the ten instruments | Under ruff and BasedPyright. |
| 4 | A | `think-fk8h` | `build_candidate.py`, `assets/workbench.js` | 120 colour literals emitted from `sqpack`. |
| 5 | C | `think-tmqs` | `src/sqpack/cli/validate.py` | The page’s gate joins `--fast`. |
| 6 | E | `think-g0lh` | `pyproject.toml`, `pages.yml`, the tree | Into `devtools`, banner off. |

Two and three run beside one; four waits on one; five and six are last.

## Testing Strategy

The page’s own checkers are the test suite and they already exist: `check_workbench.py`
(about 90 seconds, the current gate), `check_revision6.py`, `check_revision7.py`,
`check_legend.py` and `test_candidate.py`. Every chunk runs all five before it is
committed.

Two additional checks belong to this work specifically:

- **A byte comparison of the built page** across D1, which is the only chunk that could
  silently change what is drawn.
- **`compare_palette.py --per-n`** across A, which is the only chunk that could silently
  change a colour.

## What the Owner Found on the Built Page

Not part of the conversion, but found while it was being planned, and worth recording
here because two of the three were caused by the same thing the conversion is for — a
page whose script nothing can read.

- **`think-lkbk`, fixed.** The bar’s lower-bound numeral came out in the panel’s 48 px
  serif. The SVG text carried `class="gapbar-num lower"` and the facts panel has a bare
  `.lower` rule; same specificity, later in the sheet, so it won.
  The modifiers are now `is-lower` and `is-record`.
- **`think-uy41`, fixed.** The bound arrows were clipped at the low end, because the
  rail’s ends were also the scale’s ends and an arrow centred on either is half outside
  the viewBox. The rail now runs the full width and the scale’s ends are ticks inset into
  it.
- **`think-9yzq`, fixed.** Switching Pack and Animate carried the run across, so the
  page described one thing and drew another — `showing the step 10 -> 11` over eleven
  squares pushed around for 110 steps.
  Switching is now a reset, and each mode keeps its own n.
- **`think-2m96`, open.** At the first frame of every step the incoming square sits
  exactly on the existing arrangement, a measured overlap of 1.0, so the bar’s pointer
  hides. How long it lasts is the first thing to establish.

## Open Questions

- **What lints the page’s script once it is a file?** The honest options are a pinned
  `biome` or `eslint` in the build, or type-checking it with `tsc --checkJs` and JSDoc.
  The first is cheaper; the second would have caught the `\\le` bug.
  Decide at D1, when the file exists and its shape is known.
- **Does `test_candidate.py`’s full sweep belong in the fast tier or the deep gate?** It
  walks 324 pairs at two instants; `check_workbench.py` does not.
  Measure at C.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
