# Feature: Video delivery profiles

**Date:** 2026-09-21 (last updated 2026-09-21)

**Author:** Joshua Levy, with Claude Opus 5

**Status:** In Review

## Overview

`workbench_tools.capture_video` turns the built workbench page into an MP4 and writes a
receipt saying what the frames are.
It stops one step short of the thing the owner actually needs: a statement that the file
it produced is one the destination will accept.

This adds that step.
A **delivery profile** is a named, declared set of constraints on the encoded file —
codec, H.264 profile and level, pixel format, frame size, frame rate, and any ceiling
the destination puts on duration or bytes.
One profile drives the encoder arguments and then checks the encoded file against the
same declaration, so what was asked for and what came out are compared rather than
assumed.

## Goals

- Name the encoder’s settings once, as data, and use that one declaration to both encode
  and verify.
- Fail a capture whose output does not conform, in the same way
  `capture_video.price_steps` already fails a capture whose frame clock is not the
  page’s.
- Record the conformance measurement in the receipt, so a file and its receipt together
  answer “will this upload” without re-running anything.
- Measure fidelity against the page’s own PNG frames, not against another encode, so a
  quality claim is distance from the page.
- Leave one command that validates a delivered file on its own.

## Non-Goals

- Choosing where the videos are hosted, or uploading anything.
  This produces files and evidence about them.
- A per-destination catalogue.
  Two profiles are enough for what exists: an unconstrained archive master and one
  social profile carrying the tightest ceiling we actually face.
- Audio. The animation is silent, and the destinations under consideration accept silent
  MP4.
- Replacing `--height`. The stage’s own coordinates and the 1080p/4K device scales are
  settled in the video plan and are not revisited here.

## Background

Three facts from the end-to-end run on 2026-09-21, which cut n = 1..100 and the whole n
= 1..324 ascent:

- **x264 tags the output level 5.0.** At `-preset slow` it keeps five reference frames,
  whose decoded-picture-buffer size at 1920x1080 exceeds what level 4.0 allows, so it
  raises the level rather than dropping a reference.
  1080p30 needs level 4.0, and the higher tag buys nothing: cutting n = 1..100 both ways
  gives 11,659,220 bytes at level 4.0 against 11,659,739 at 5.0 over the same 3,342
  frames, the constrained file coming out 519 bytes smaller.

- **Nothing checks the file.** The receipt names the encoder’s arguments but not the
  encoded stream, so the two could disagree — an ffmpeg that ignored a flag, a filter
  that changed the frame size — and the receipt would still read as if they had not.

- **The duration ceiling is real and it binds.** n = 1..100 runs 111.4 s and n = 1..324
  runs 382.7 s. A standard X post takes 140 s. Which excerpt fits is a fact about the
  range, decided long before anyone opens an upload dialog, and the tool already knows
  the range’s duration before it captures a frame.

The first cut also found [`D-492`](../../../../defects.md): `rangeDuration` priced a
range without the `fastSimple` speed-up, so the page quoted a range it played faster
than it said, and `price_steps` refused every capture.
Fixed at `e00c4529`. It is the reason this plan exists — the check that caught it is the
model for the check proposed here.

## Design

### Approach

A profile is a frozen dataclass, and the registry of profiles is a module constant.
`capture_video` takes `--profile`, passes it to the encoder, and then measures the file
it wrote and refuses to write a receipt for a file that does not conform.

The measurement and the check are separate functions over plain data, so both are
testable without ffmpeg and without a browser: `measure` parses `ffprobe`’s JSON into a
`DeliveredVideo`, and `conformance` compares a `DeliveredVideo` against a
`DeliveryProfile` and returns the failures.

### Components

| Path | What it is |
| --- | --- |
| `packages/workbench/tools/workbench_tools/delivery.py` | New. `DeliveryProfile`, `PROFILES`, `encode_arguments`, `measure`, `conformance`, `fidelity`, and a `main` that validates a file on its own |
| `packages/workbench/tools/workbench_tools/capture_video.py` | Takes `--profile`; encodes through `delivery.encode_arguments`; checks the encoded file before the receipt is written; records the profile and the measurement in the receipt |
| `packages/workbench/tests/test_delivery.py` | New. Profile-versus-measurement cases over plain data, and the encoder argument contract |
| `packages/workbench/tests/test_capture_and_export.py` | The existing `encode_arguments` contract moves to the profile-driven form |
| `packages/workbench/pyproject.toml` | `squares-workbench-check-delivery` console script |

### API Changes

`capture_video.encode_arguments` moves to `delivery.encode_arguments` and takes a
`DeliveryProfile` as its first argument.
It has one consumer in the repository and one contract test, both updated here.

`capture_video.capture_receipt` gains `profile` and `delivered`, so an existing receipt
read by a future consumer gains two keys rather than changing any.

### The two profiles

|  | `archive` | `social` |
| --- | --- | --- |
| Purpose | The master. Nothing is traded for a destination’s rules | An upload to X, which is the tightest ceiling we face |
| H.264 profile / level | high / 4.0 | high / 4.0 |
| Pixel format | `yuv420p` | `yuv420p` |
| CRF / preset | 18 / `slow` | 18 / `slow` |
| Duration ceiling | none | none (140 s until 2026-09-22) |
| Byte ceiling | none | 512 MB |

Level 4.0 is in both because the measurement says it costs nothing and it is the level
1080p30 requires; a master tagged for hardware that cannot play it is not a better
master. What separates the profiles is only the ceilings, which is the honest split: a
ceiling is a property of a destination, not of an encode.

CRF and preset are declared per profile even though both profiles currently agree,
because that is the axis a future destination would move.

### What conformance checks

Codec, H.264 profile, level, pixel format, width, height, frame rate, and that the
stream’s duration matches the receipt’s to within one frame.
Under a profile carrying ceilings, also duration and bytes.
`faststart` is checked by position of the `moov` atom rather than by trusting the flag.

A failure names the constraint, the declared value and the measured one, in that order,
because the useful question on a red check is always which of the two is wrong.

### Fidelity

`fidelity` runs ffmpeg’s `psnr` and `ssim` filters over a declared window of the
capture’s retained PNG frames against the encoded file, and returns both figures with
the window that produced them.
It is not part of conformance: a profile is a statement about the container and the
stream, and fidelity is a measurement whose acceptable value is a judgement.
It is reported, recorded when frames are available, and never silently turned into a
threshold.

The window is declared rather than defaulted to the start of the run, because the first
frames of the ascent are three squares on white and say nothing about how the encoder
handles n = 300.

## Implementation Plan

### Phase 1: profiles, conformance, and the capture wiring

- [x] `delivery.py`: `DeliveryProfile`, `PROFILES`, `encode_arguments`,
  `DeliveredVideo`, `measure`, `conformance`, `fidelity`, `main`.
- [x] `capture_video`: `--profile`, encode through the profile, check before the
  receipt, record `profile` and `delivered` in the receipt.
- [x] Move the `encode_arguments` contract test to the profile-driven form.
- [x] `test_delivery.py`: conformance over plain data — a conforming measurement, each
  constraint violated one at a time, the ceilings under `social` and their absence under
  `archive`, and a duration that disagrees with the receipt by more than a frame.
- [x] Console script `squares-workbench-check-delivery`.
- [x] Ruff, BasedPyright and `pytest ../packages/workbench/tests` at zero findings.

### Phase 2: re-cut and validate the deliverables

- [x] Cut n = 1..100 at both 30 and 60 fps under `social` for comparison.
  The owner chose 60 fps (2026-09-21), and `capture_video` now defaults to it.
- [x] Re-capture n = 1..324 under `archive` and n = 1..100 under `social`, at 60 fps,
  from the reviewed page at `17dcb3f92`, frames and files on the external drive.
  The n = 1..100 cut runs 159.65 s, past X’s standard 140 s. The earlier 135.2 s cut
  predated the arrival delay merged from main (`4c2f2da27`), which adds 0.69 s to every
  moving step; `capture_video --price-against` measures that per kind of step.
  The owner kept the full excerpt (2026-09-22), and the `social` duration ceiling was
  dropped.
- [x] Record the measured fidelity and the conformance result for each.

| Cut | Profile | Frames | Length | Size | Fidelity (PSNR, SSIM) |
| --- | --- | ---: | ---: | ---: | --- |
| n = 1..100 | `social` | 9,579 | 159.65 s | 43.8 MB | 49.6 to 51.3 dB, 0.999 |
| n = 1..324 | `archive` | 33,626 | 560.43 s | 239.2 MB | 47.9 to 51.4 dB, 0.998 to 0.999 |

The n = 1..100 cut was replaced on 2026-09-22 (`v0.4.1-b7690c`, citations on, grid fills
at 4x): 9,203 frames, 153.383 s, 44.0 MB, conforming, captured in 564 s. Its repeated
frames inside motion fell from 73 to 15 over that day — 44 of them the container box’s
one-frame blink (`think-dh9j`), 8 of them frames the 480 × 270 measurement called
repeats and a full-size reading did not, and the rest a mixture.
Ten of the 15 that remain are the one- to two-frame beat on a grid fill between the
arriving square settling and the facts column starting its handover, which is a timing
choice rather than a defect and is the owner’s to disposition.

**The two rows below were cut at a grid-fill speed-up of 3, which is no longer the
default.** The factor is a setting now (`think-gr3j`, default 4), so a length means
nothing without it: the receipt’s `simple_speed` names the clock its step lengths were
measured on, and a cut that asks for a factor the page declines is refused rather than
cut at whatever the page settled for.
Priced at 4, the same ranges are 153.39 s and 542.02 s, all of the difference in the 55
and 160 grid fills each contains.

Both rows conform.
Fidelity is measured over three windows of each cut, early, middle and
late, against the capture’s own PNGs.

Smoothness is measured by `squares-workbench-check-cadence`, which this phase added:

- **The clock is exact.** Every presentation-time gap in both files is within 0.7 µs of
  one sixtieth of a second.
- **The capture is faithful.** Every flagged frame is drawn again from the page, and no
  kept frame is the page one frame early.
- **Playback holds for one frame in a few places.** At a moving step’s last frame, and
  where the physics move joins its tightening, playback holds still where a fresh draw
  of the same instants moves.
  That is 41 of 33,626 frames in the full ascent and 16 of 9,579 in n = 1..100. The
  other flagged holds are the page’s own, eased phases meeting at a boundary.
  Tracked as `think-dh9j`.
- A slow color fade steps 8-bit fills one level at a time, so the mean change between
  frames alternates while nothing moves.
  The check therefore judges motion on pixels that change by more than 12 grey levels,
  not on the mean.

## Testing Strategy

`conformance` and `measure` are pure functions over plain data, so the table of cases
runs with no ffmpeg, no browser and no fixture video: a conforming `DeliveredVideo`,
then one field wrong at a time, then the ceilings present and absent.

What the unit tests cannot establish is that `measure` parses what `ffprobe` actually
emits. That is covered by the capture itself: every capture now measures its own output
and fails on a mismatch, so a parse that stopped working stops the next cut rather than
passing quietly.

The `fidelity` window’s arithmetic — which frames it names — is tested over plain data;
the filter invocation is not mocked, because a mocked ffmpeg proves nothing about
ffmpeg.

## Rollout Plan

Nothing is published by this change.
It alters a developer tool and adds a checker.

The captures live outside the repository: `packing/site/` is gitignored and built by CI,
and a multi-megabyte MP4 is not committed.
How a finished cut reaches a reader is **Publication** below.

## Publication

A cut is published as a **GitHub Release asset**, and linked or embedded from the pages
this repository already serves.
The route was chosen against three alternatives on 2026-09-22; what follows is the
reasoning, then the procedure.

### Why not commit the file

`sqpack.release` says it in the code that pins the data revision: the videos are release
assets, never committed.
Two measurements stand behind that.
GitHub refuses a file over 100 MB outright, and the n = 1..324 archive cut is about 230
MB, so the long cut could not be committed even if the policy allowed it.
And a committed binary is permanent: the repository is already 502 MB, and every re-cut
would add its predecessor to history forever.

### Why not Actions artifacts, Git LFS, or Pages alone

| Mechanism | Cost on this public repository | Lifetime | Can a page link it? |
| --- | --- | --- | --- |
| Actions artifact | free | 90 days at most | **No** — no anonymous URL; a download needs a signed-in session or a token |
| Git LFS | billed past its free quota | permanent | **No** — Pages serves the pointer file, not the video |
| Committed and served by Pages | free | permanent, unfortunately | yes, under a 100 MB per-file wall |
| **Release asset** | **free** | until deleted | **yes**, 2 GB per file |

The one that matters for video is the last column *and* range requests: a `<video>`
element seeks by asking for byte ranges, and a host that answers 200 with the whole file
makes seeking a full download.
Measured on 2026-09-22: a release asset URL 302-redirects to
`release-assets.githubusercontent.com`, which answers a `Range: bytes=0-99` request with
`HTTP 206` and `accept-ranges: bytes`. That is what makes this route work.

### The tag

The tag is the **publication version alone** — `v0.4.1`, which is
`sqpack.release.PUBLICATION_VERSION` — and carries no data revision.
The frames carry the full edition, `PUBLICATION_EDITION`, which appends the first six
characters of the pinned data revision: `v0.4.1-b7690c`. The two are deliberately
different. The tag names a release, which is a thing a reader cites and a maintainer
moves forward; the stamp names the evidence a particular frame was drawn from, which is
finer-grained and changes whenever the records do.
A release may carry assets stamped with different revisions, and the stamp in the corner
is what says which.

### The procedure

1. **Cut and verify.** `capture_video --citations` writes the file and its receipt,
   refuses a file that does not conform to its profile, and prices the range against the
   page. Run `squares-workbench-check-cadence` on the result and record where its
   smoothness stands.

2. **Tag and create the release** from the commit the page was built at.

3. **Upload the mp4, and do not expect the content type to reach a reader.** Set
   `Content-Type: video/mp4` through the API -- `gh release upload` has no flag for it
   -- because that is what the API and the release page then report the asset as.
   It is **not** what is served.
   Measured on the published `v0.4.1` assets: whatever type an asset is stored with, the
   download redirects to a signed URL that pins
   `response-content-type=application/octet-stream` and
   `Content-Disposition: attachment`. An earlier draft of this section had that
   backwards and said setting the type was what made an embed work.

   What makes it work was measured against the live asset instead: a `<video>` pointed
   at it reached `readyState 4` at 1920 x 1080 and 140.02 s with no error, and seeking
   to 120 s buffered 109.6-134.6 s -- a byte range from the middle of the file rather
   than a download from its start.
   So the browser sniffs past the octet-stream, the `type` attribute on the `<source>`
   is what tells it what to expect, and the range support the table above relies on is
   real.

4. **Upload each receipt beside its video.** The receipt is the provenance — frames,
   duration, the file’s digest, the page’s digest, the citation file’s digest, the beat
   and the grid-fill factor.
   A published video whose receipt is not published is a claim without its evidence.

5. **Verify what is served**, rather than assuming: the status, the content type, and
   that a range request returns 206.

6. **Link or embed** from `templates/explainer-article.md`, which is the explainer’s
   prose source.

### What was published

`v0.4.1`, tagged at `d5b1c2e1b` on 2026-09-22:
<https://github.com/jlevy/squares/releases/tag/v0.4.1>. Four assets — both cuts and both
receipts.

| Asset | Frames | Length | Size | Profile |
| --- | ---: | ---: | ---: | --- |
| `ascent-n1-100-1080p60-citations.mp4` | 8,401 | 140.02 s | 38.0 MB | `social` |
| `ascent-n1-324-1080p60-citations.mp4` | 29,639 | 493.98 s | 206.1 MB | `archive` |

Both drawn from page `575ccc8e` and stamped `v0.4.1-b7690c`. Their clocks are exact to
0.7 microseconds of 1/60 s; repeated frames inside motion are 11 and 39, 0.13% of each,
and ten of the eleven in the excerpt are the one beat `think-dh9j` tracks.

The explainer plays the excerpt under Figure 2, in a `screen-only` block so the typeset
PDF does not carry a black rectangle where a player would be; the PDF still renders 22
pages and reproduces itself.

**GitHub strips `<video>` from Markdown**, so the README links the files rather than
embedding them. Measured through GitHub’s own Markdown API on 2026-09-22: both
`<video src=…>` and the `<source>` form render to an empty paragraph, while `<img>`,
`<a>` and `<details>` survive in the same request, and a bare asset URL becomes a plain
link. The `user-attachments` URL form GitHub produces for drag-and-dropped video is
rendered by its frontend, not by the Markdown pipeline, and cannot be pointed at a
release asset.

### The embed

Read off the delivered file rather than assumed — H.264 High profile, level 4.0,
yuv420p, 1920 x 1080, 60 fps, and no audio track:

```html
<video controls width="960" playsinline>
  <source src="https://github.com/jlevy/squares/releases/download/v0.4.1/ascent-n1-100-1080p60-citations.mp4"
          type='video/mp4; codecs="avc1.640028"'>
</video>
```

`64` is the High profile, `00` the constraint flags, `28` hexadecimal for level 40.
There is no `mp4a` in the codecs string because the cut is silent.

### The alternative, if the asset host’s headers ever become a problem

Pages here deploys from a **workflow artifact** rather than from a branch, so the site
is assembled in CI. A build step could fetch the release asset and place it under
`packing/site/`, which would serve it from the Pages origin with a content type derived
from the extension and a URL under `jlevy.github.io/squares/`. The cost is the file’s
bytes on every deploy, against Pages’ 1 GB site limit and its 100 GB monthly soft
bandwidth limit. Not taken while the release asset serves correctly, because it couples
every page deploy to a large binary.

## Open Questions

- Does a silent AAC track widen what accepts the file enough to be worth carrying?
  Not measured. X accepts silent MP4, which is the destination that prompted this.
- Should the 4K device scale get its own profile?
  Level 4.0 does not admit 3840x2160, so a 4K capture would need level 5.1 and the
  profile table would grow a row.
  Deferred until a 4K cut is actually wanted.

## References

- [Known-best atlas video plan](plan-2026-09-07-known-best-atlas-video.md), whose D9
  defines the receipt this extends
- [Workbench from spike to product](plan-2026-09-11-workbench-from-spike-to-product.md)
- [`D-492`](../../../../defects.md), the timing defect the first end-to-end cut found

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
