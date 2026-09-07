---
title: Math Text Face Integration
description: Take kpress's math text face (letters and digits from PT Serif inside KaTeX) into the explainer page, its PDF, and the validation tiers, and keep the measurements in a devtool
author: Claude (agent), for samanthadrakova@gmail.com
date: 2026-09-07
status: active
---
# Feature: Math Text Face Integration

**Date:** 2026-09-07 (last updated 2026-09-07)

**Status:** Implemented (2026-09-07) except the Safari and Firefox checks and the pull
request.

**Workflow entry:** feature implementation from spec.
**Tracking:** epic `think-rk9v`; squares tasks `think-58av` (integration, blocked on the
kpress feature), `think-do8b` (devtool), `think-0vju` (verification).
The feature itself is tracked in kpress’s own tbd as epic `kpr-sc4f`, with the deferred
sans-math and Greek-sizing features `kpr-7f9z` and `kpr-c2tr`.

## Overview

The explainer page sets prose in PT Serif and mathematics in KaTeX, and the two disagree
in x-height and weight.
The research that diagnosed it and the feature that fixes it live in kpress, on the
vendored `squares/page-fixes` branch, because both are about kpress typography rather
than this paper:
[the research brief](../../../../vendor/kpress/docs/math-text-face.research.md) and
[the feature plan](../../../../vendor/kpress/docs/math-text-face.plan.md).
The feature draws every Latin letter and digit inside mathematics from the reading face,
keeps operators, relations, delimiters, radicals and Greek in the KaTeX faces, sets
inline math at the prose size, and gives KaTeX the reading face’s metrics.
It is on by default in kpress once it lands.

This plan is the squares side: what the renderer, the PDF export and the validation
tiers need so the page picks the feature up, and where the measurements that settled the
design live afterwards.

## Goals

- The explainer page and its PDF render with the math text face through the submodule,
  with no change to what the page’s own stylesheet says about math.
- Every existing check still passes: render self-agreement, PDF self-agreement, print
  layout, supporting typography.
- The measurements and comparisons from the research live in a devtool, not in one-off
  scripts (OR-1).

## Non-Goals

- The feature itself, its option, its CSS and its metrics generator: kpress’s plan.
- Sans math and Greek sizing: deferred, tracked in kpress as `kpr-7f9z` and `kpr-c2tr`.

## Background

What is specific to this page, found while prototyping the feature on it:

- The renderer inlines everything.
  `kpress_css` rewrites `url("../fonts/…")` to data URIs; `katex_css` keeps only the ten
  KaTeX faces in `KATEX_FACES` and drops the rest.
  The composite family names `../katex/fonts/…` sources, which the rewrite does not
  match today.
- The page renders its own math: the explainer template calls `katex.render` directly
  (`tex()` in the shell and the walkthrough script), so the metrics table has to be
  inlined and applied before those calls, not only inside kpress’s `katex-init.js`.
- The `\mkern1mu` kern the renderer adds between a function name and its parenthesis
  (`s(n)`) is what keeps the PT Serif italic, which has no italic correction of its own,
  from setting the parenthesis against the letter.
  It stays.
- The display blocks carry `padding-block: 0.45rem`, which is what hid the one-pixel
  numerator overflow of the CSS-only routes; with the metrics table it is no longer
  doing that job, and can stay for the headroom it was added for.
- Sans contexts: figure captions, the mass line and the panels are set in Source Sans
  and their math now carries PT Serif letters rather than Computer Modern.
  Either is a serif in a sans line; consistency of the math face across the document is
  the usual choice, and restricting the feature to prose contexts is one selector if the
  captions read better the old way.
- The PDF pipeline is unaffected.
  The recommended page exported through `render_explainer_pdf.render_pdf_bytes` gives
  the same 14 pages as the current one; `check_print_layout` reports both clean; two
  consecutive exports agree byte for byte after date normalisation; in the file the math
  letters and digits come from the `PTSerif-Regular` and `PTSerif-Italic` subsets the
  prose already embeds, at the prose’s 11.2pt, while `≤`, `√`, the fraction bar and the
  Greek still come from the embedded KaTeX faces; the PDF is 35 KB smaller because
  `KaTeX_Main-Bold` is no longer needed.
  The check ran the exporter against the installed Google Chrome (`SQPACK_CHROMIUM`),
  since Playwright’s pinned headless shell is not downloaded on the development machine;
  the layout engine is the same, the bytes are not.

## Design

### Approach

Nothing in the page’s template or stylesheet changes.
The renderer learns to inline the composite’s KaTeX-side sources and the metrics asset,
the submodule gitlink moves to the commit that carries the feature, and the checks run.
The measurement scripts from the research become one devtool with three commands.

### Components

- `vendor/kpress` gitlink bump to the branch commit that carries the feature, and the
  `pyproject.toml` comment that lists what the branch carries.
- `devtools/render_explainer.py`: `inline_font_urls` also rewrites
  `url("../katex/fonts/…")`; `katex/katex-text-metrics.js` is inlined after
  `katex.min.js` and before the page’s own scripts; `KATEX_FACES` unchanged.
- `devtools/compare_math_fonts.py`: `metrics` prints the x-height, cap height, digit
  height, ascender, operator centre, hairline and stem of the shipped faces from their
  woff2 files; `variants` builds pages from the rendered explainer by injecting CSS from
  a small spec; `shots` takes Playwright element screenshots of named paragraphs and
  display blocks in each variant and stacks them into montages.
  fontTools in the dev group, pinned past the 14-day cool-off.
- Validation: `render_explainer --check`, `render_explainer_pdf --check`,
  `check_print_layout`, `inspect_explainer_typography --check-supporting`; the Pages
  workflow already checks out the submodule and installs the headless shell, so it needs
  no change.

### API Changes

- `python -m devtools.compare_math_fonts {metrics,variants,shots}`.
- `inline_font_urls` accepts both `../fonts/` and `../katex/fonts/` sources.

## Implementation Plan

One phase; the kpress feature landed first.

- [x] Bump the gitlink; extend `inline_font_urls`; inline the metrics asset ahead of the
  page’s KaTeX calls; render and run every check.
- [x] Add `devtools/compare_math_fonts.py` and fontTools to the dev group; regenerate
  the brief’s metrics table and montages with it and check they agree.
- [ ] Verify in Safari and Firefox (Playwright WebKit and Firefox builds, or by hand),
  and confirm the PDF `--check` on the pinned headless shell in CI.
- [ ] Open a pull request that leads with what the branch cost and links the two kpress
  documents.

## Testing Strategy

- The four existing checks above, plus the PDF check on CI’s pinned browser.
- `compare_math_fonts metrics` reproduces the brief’s table for the shipped faces;
  `shots` reproduces the current-versus-recommended montages.

## Rollout Plan

The page picks the feature up on the gitlink bump and its next Pages deploy.

## Open Questions

- Whether captions and panels keep the math text face or revert to the KaTeX faces (see
  Background).

## References

- [Research: Harmonizing the Reading Face with KaTeX Mathematics](../../../../vendor/kpress/docs/math-text-face.research.md)
  and [Math Text Face](../../../../vendor/kpress/docs/math-text-face.plan.md), in
  kpress.
- [`render_explainer.py`](../../../../packing/devtools/render_explainer.py),
  [`render_explainer_pdf.py`](../../../../packing/devtools/render_explainer_pdf.py),
  [`check_print_layout.py`](../../../../packing/devtools/check_print_layout.py),
  [`inspect_explainer_typography.py`](../../../../packing/devtools/inspect_explainer_typography.py).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
