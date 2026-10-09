# Square-packing workbench

This package owns the workbench’s typed browser modules and Python adapters.
The
[workbench plan](../../docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md)
defines the finished product and migration phases; the
[review](../../docs/project/reviews/review-2026-09-12-workbench-stack-architecture.md)
tracks repairs and their evidence.

The package builds a self-contained Animate, Pack and experimental Search page, opening
on Animate. Pack has its own seeded, arbitrary-count session, snapshot import/export and
bounded overlap repair.
Animate retains the catalogue and animation studio.
Search runs a bounded browser preview and can export and resume exact-plan ledgers; its
wider scheduler, calibration and research acceptance remain open in the plan.
The checked JavaScript application is still large, and its historical pair-based Pack
path needs retirement after the remaining consumers migrate.
The source, probes, build tools and workbench-specific Python adapters now live in this
package.

## Development

Use Node 24 (the baseline is pinned in the repository’s `.node-version`) and the
repository’s Python 3.14 environment.
From the repository root:

```bash
npm ci
npm run check --workspace @squares/workbench
```

The package check builds the browser and benchmark bundles, runs Biome and the
type-aware promise floor, type-checks the modules, and runs the Node contract tests.
Python adapters are installed with the repository’s `workbench` extra.
From `packing/`:

```bash
uv run --frozen --all-extras --group dev python -m pytest ../packages/workbench/tests
uv run --frozen --all-extras --group dev python -m workbench_tools.build_site
```

The latter builds the self-contained page in `packing/site/workbench/`. Its publisher
checks the generated full corpus and that the page is self-contained, stamps the source
revision, and with `--check` requires two builds to match byte for byte.
The GitHub Pages deployment is owned by the repository workflow.

## Design system

Every colour, space, type size, weight, line height, radius, border width, shadow, layer
and duration the page uses is a custom property in the `:root` block at the top of
[`assets/workbench.css`](assets/workbench.css).
The rest of the stylesheet refers to those tokens and nothing else.
The block has three families:

- **UI chrome** (`--color-*`, `--space-*`, `--font-*`, `--radius-*`, `--control-*`,
  `--layout-*`): semantic colour roles, a 4 px spacing scale, a five-step type scale and
  one control height. The font families and their names follow kpress.
- **The stage** (`--stage-*`): the 1920 × 1080 poster the video is captured from, in
  stage pixels.
- **Scene and plot colours** (`--scene-*`, `--plot-*`): what is drawn rather than the
  chrome. Square fills are data from `sqpack.render` and are not tokens.

The stage draws one frame around the packing, whichever mode owns it.
The catalogue’s box, the trace of where it just was and the container Pack and the
animation studio draw are all `--scene-frame-width` wide, and the colour is the only
thing that changes: the box is `--scene-frame-locked` where it rests at the best known
side and `--scene-frame` on its way, the trace is `--scene-trace`, and the container is
`--scene-frame`.

**The stage names its sources on request.** Under PROVEN, the CITATION section gives
each bound’s reference and the frontier case record they are held in.
Everything this project has to say about a bound is one grey parenthesis after the
reference, in one vocabulary: `(reported)` where the register carries the bound without
certifying it, `(confirmed T-009)` where a result of ours checks it, and
`(reported; confirmed T-009)` where both are true.
A certificate of an earlier, weaker ceiling remains linked in the case record and does
not confirm the displayed bound.
The words are composed with the data, not at the stage, and the width a line is checked
against counts them.
It is a setting — `show citations`, off until it is asked for, `setCitations` on the
browser API — and its data is
[`bound-citations.json`](../../packing/atlas/known-best/bound-citations.json), read at
build time; a page built without that file has nothing to cite and says so.
`squares-workbench-capture --citations` draws the section for a cut, and the cut’s
receipt records that it was on, the file’s sha256 and the version.
The stage’s bottom right carries that version, `sqpack.release.PUBLICATION_EDITION`, so
every captured frame names the data it was drawn from.

**The panel trades its text rather than dissolving it.** A word both n draw holds at
full ink and swaps at the midpoint; a word that changes leaves before its replacement
arrives, over `TEXT_HANDOVER`, which is seven frames at 60 fps.
Cross-fading the two put the old sentence and the new one in the same place at half ink
each, and neither could be read (`think-0few`). `check_animate_view` holds both halves
of that: two different strings drawn in one place are never both legible, and a slot
with nothing holding it up may be under half ink for `BLANK_DIP_SECONDS` and no longer.

**A grid fill plays faster, by a factor you set.** `speed up simple transitions` is the
toggle and `grid fill speed` the factor, 1 to 8 in halves and 4 by default: a step where
every square is already square to the container has nothing to watch.
`setSimpleSpeed` is the browser API, `squares-workbench-capture --simple-speed` the
cut’s, and the receipt’s `simple_speed` names the clock its step lengths were measured
on — so a length means nothing without it, and a cut that asks for a factor the page
declines is refused.

The page has one structure in every mode.
The controls are a single column inside `--layout-gutter`. Every block in it (the mode
panel, a `.panel-row` of `.subpanel`s, a `.workspace`) spans the same two edges and sits
`--layout-stack-gap` from the next.
Within a block, a `.row` holds controls and a `.box-title` names a panel.

Three contracts hold it:

- [`tests/design-system.test.ts`](tests/design-system.test.ts) refuses a raw design
  value outside the token block.
  It also refuses an inline style write in `src/` or the template beyond the counted,
  reasoned allowances in [`design-allowlist.json`](design-allowlist.json), which may
  only shrink. It checks every text, control, focus and stage colour pair against WCAG
  AA. The machinery is in [`tools/design-contract.ts`](tools/design-contract.ts), with
  its negative fixtures in `tests/design-contract.test.ts`.
- `workbench_tools.check_layout` measures Animate at rest and mid-step, the animation
  studio, Pack and Search in Chromium at 1440 × 900, 1024 × 768 and 390 × 844. It checks
  the shared edges, gutters and gaps, one height per control kind, horizontal overflow,
  panel overlap, the stage panel’s OPEN and badge rules (one type, with `new result`
  alone in the star’s scarlet), one type for the PROVEN, CITATION and OPEN heads, the
  CITATION section inside its column and above what it is set over, the one frame width
  in its three colours, and that the attribution stands one legend line under the legend
  at its left edge, with the shared version on its baseline at the column’s right edge,
  both clear of what each mode draws.
  It runs inside `check_stage_resize`’s browser session in `check_frontend`, and
  `tests/test_check_layout.py` proves each rule refuses a page that breaks it.
- `workbench_tools.layout_gallery` photographs every view at every review viewport and
  writes a side-by-side comparison page for design review.

## The transition contract

`workbench_tools.check_transitions` samples every frame of a step at 60 fps and holds it
to the rules in `transition_contract`. A blend shows no hue that neither of its ends
has, and a hue turns only through grey.
A shade blends rather than snapping.
The view moves one way, the box only shrinks once the move starts, and the new square
arrives saturated scarlet.
`check_frontend` runs it on every pull request over the steps that have broken; `--all`
runs every step in the corpus.

When a transition looks wrong, trace it before changing anything.
This prints one square through one step, frame by frame, in OKLCH, with the schedule it
ran on:

```bash
uv run --frozen --all-extras --group dev squares-workbench-check-transitions --trace 11 --square 5
```

## Contracts and ownership

- `src/api` defines the public browser API. Runtime installation and probe declarations
  consume this contract.
- `src/core` owns seed semantics, snapshot checks and navigation.
  Packing poses use radians internally; the retained public browser API uses degrees.
- `src/data` validates the versioned corpus and its stable identities.
  The builder supplies palette/shades from `sqpack.render`; workbench angle clustering
  has a separate declared tolerance.
- `src/animation` computes timing, arrival, range progress and deterministic seeking.
  These operations do not call a solver or require a DOM.
- `probes` holds checked browser instruments.
  Python code does not embed their programs in string literals.
- `tools/workbench_tools` contains Python import, geometry, trial and report contracts.
  Numerical admission retains the exact checked snapshot and its tolerance.

## Regenerating and publishing the ascent videos

The explainer plays, and the README links, two cuts of this page’s Animate mode at
1080p60 with the CITATION section on: $n = 1\ldots100$ under the `social` profile and
the full $n = 1\ldots324$ under `archive`. They are GitHub Release assets, never
committed. Why, and what each profile holds, is the
[delivery-profiles plan](../../docs/project/specs/active/plan-2026-09-21-video-delivery-profiles.md#publication);
this section is the procedure, in order.
The spikes under `packing/atlas/known-best/video/spikes/` are not part of it.

**For an agent.** *Inputs*: a full clone of `main` at the commit to cut from (normally
the merge that changed the data), `gh` signed in with write access to `jlevy/squares`,
and the owner’s answer to step 2. *Outputs*: two MP4s and their receipts on the release
named by `PUBLICATION_VERSION`, and one pull request carrying the new poster, the
updated links and the published record.
*Done* when both cuts conform to their profiles, each served asset answers a range
request with 206 and matches its receipt’s digest, and step 10 passes on that pull
request’s merge. Ask the owner at step 2 and before deleting a published asset; nothing
else needs a decision.
Never commit an MP4, a receipt or a frame.
Commands run from `packing/`, with `uv run --frozen --all-extras --group dev` in front
of each `python -m` and `squares-workbench-*` command below.

1. **Prerequisites.** Everything in [A fresh clone](../../AGENTS.md#a-fresh-clone) (full
   history, the submodule, `npm ci`), plus:
   - `ffmpeg` with `libx264` on `PATH`: `ffmpeg -hide_banner -encoders | grep libx264`.
   - Playwright’s pinned Chromium, `playwright install chromium`. The
     `playwright==1.62.0` pin in `pyproject.toml` fixes it at 151.0.7922.34, which each
     receipt records.
   - Node from `.node-version` (the engines field allows `>=24.18.0 <25`).
   - Disk for the PNG frames, which go to a temporary directory (move it with `TMPDIR`)
     and are deleted after the encode.
     A trial near $n = 88$ measured 160 kB a frame, so the 29,639-frame full cut needs
     about 5 GB and more where the packings are denser; keep 10 GB free.
   - Time: the `v0.4.2` receipts record 562.6 s of capture for 8,401 frames and 2,105 s
     for 29,639 on the owner’s machine.

2. **Decide the version first.** Every frame prints `PUBLICATION_EDITION` from
   `packing/src/sqpack/release.py`, and the release tag is `PUBLICATION_VERSION`, so the
   version is fixed before capture, never after.
   New data does not move it by itself: the stamp’s data revision names the data, and
   the version names an edition the owner cuts, at most one per merge, by
   [Cutting an edition](../../development.md#cutting-an-edition).
   Ask the owner whether this re-cut goes out under the current version or a new one.
   A new one is cut and merged in its own pull request, and this procedure then starts
   from that merge.

3. **Preflight.** On a clean tree (`git status` empty; the receipt records `dirty`):
   - `python -m pytest tests/test_release.py` passes, so the pinned `DATA_REVISION` is
     the last data commit.
   - `python -m devtools.build_known_best_atlas --check` passes.
   - `python -m devtools.build_bound_citations --check` passes, and `--review` shows
     credit lines that meet the owner’s rules: no AI agent credited as an author, last
     names or handles in these brief lines, and this project as “Squares Project (Levy)”
     or “Levy”. The frames carry these lines, so a wrong one costs a re-cut.

4. **Build the page** at the checked-out commit:

   ```bash
   python -m workbench_tools.build_site --check --revision "$(git rev-parse HEAD)"
   ```

   It writes `site/workbench/index.html` (gitignored) from the inputs `RENDER_INPUTS` in
   [`build_site.py`](tools/workbench_tools/build_site.py) lists.

5. **Capture both cuts.** Each refuses a file that does not conform to its profile and
   writes `<name>.receipt.json` beside the video.

   ```bash
   squares-workbench-capture --from 2 --to 100 --citations --profile social \
     --out site/workbench/ascent-n1-100-1080p60-citations.mp4
   squares-workbench-capture --from 2 --to 324 --citations --profile archive \
     --out site/workbench/ascent-n1-324-1080p60-citations.mp4
   squares-workbench-check-cadence site/workbench/ascent-n1-*-citations.mp4
   ```

   Record what the cadence check reports, including repeated frames inside motion.
   A nonzero exit is a finding for the published record rather than a stop: the `v0.4.2`
   cuts had 12 and 41 such frames, tracked as `think-dh9j`.

6. **Cut the posters** from the new cuts.
   The $n = 1\ldots100$ cut replaces the explainer’s
   [`assets/ascent-n1-100-poster.png`](assets/ascent-n1-100-poster.png) with its
   $n = 88$ frame, and the $n = 1\ldots324$ cut replaces the overview’s
   [`assets/ascent-n1-324-poster.png`](assets/ascent-n1-324-poster.png) with its
   $n = 290$ frame, both at 1280 × 720, so each updates the version stamp it shows.
   The receipt’s range picks which poster a cut writes:

   ```bash
   squares-workbench-poster site/workbench/ascent-n1-100-1080p60-citations.receipt.json
   squares-workbench-poster site/workbench/ascent-n1-324-1080p60-citations.receipt.json
   ```

   It takes the step’s settled last frame; `--before-end K` takes one $K$ frames
   earlier. The committed posters are the settled ends of $n = 88$ in the `v0.4.2`
   $n = 1\ldots100$ cut, frame 7,864 of 8,401 (17 frames earlier the colour fade has
   already turned the picture grey), and of $n = 290$ in the `v0.4.2` $n = 1\ldots324$
   cut, frame 26,522 of 29,639.

7. **Put the files on the release** named by the version from step 2:

   ```bash
   TAG=$(uv run --frozen python -c 'from sqpack.release import PUBLICATION_VERSION as v; print(v)')
   gh api repos/jlevy/squares/releases/tags/$TAG --jq '.id, (.assets[] | [.id, .name] | @tsv)'
   ```

   A new version has no release yet; create one at the commit the page was built from
   with
   `gh api repos/jlevy/squares/releases -f tag_name=$TAG -f target_commitish=<commit> -f name=$TAG --jq .id`.
   Under an existing version, delete each asset being replaced once the owner agrees,
   with `gh api -X DELETE repos/jlevy/squares/releases/assets/<asset id>`; the embed is
   broken until its replacement is up.
   Then upload the four files through the REST API, since `gh release upload` cannot set
   a content type:

   ```bash
   ID=<release id>
   for f in site/workbench/ascent-n1-{100,324}-1080p60-citations.{mp4,receipt.json}; do
     case $f in *.mp4) type=video/mp4 ;; *) type=application/json ;; esac
     curl -sS --fail -X POST -H "Authorization: Bearer $(gh auth token)" \
       -H "Content-Type: $type" --data-binary "@$f" \
       "https://uploads.github.com/repos/jlevy/squares/releases/$ID/assets?name=$(basename "$f")"
   done
   ```

8. **Verify what is served.** Each video answers a range request with 206, and its bytes
   hash to its receipt’s `video_sha256`:

   ```bash
   for cut in 100 324; do
     url=https://github.com/jlevy/squares/releases/download/$TAG/ascent-n1-$cut-1080p60-citations.mp4
     curl -sSL -r 0-99 -o /dev/null -w '%{http_code}\n' "$url"
     curl -sSL "$url" | shasum -a 256
   done
   ```

   The release API should report both videos as `video/mp4`
   (`gh api repos/jlevy/squares/releases/tags/$TAG --jq '.assets[] | [.name, .content_type] | @tsv'`).
   The download itself is served as `application/octet-stream`, which is expected; the
   plan’s
   [procedure](../../docs/project/specs/active/plan-2026-09-21-video-delivery-profiles.md#the-procedure)
   says why a player accepts it.

9. **Open one pull request** with the poster from step 6 and these edits, then run
   `python -m pytest tests/test_n11_lower_bounds_explainer.py`:
   - [`README.md`](../../README.md), the film paragraph under the atlas: each length
     (`2m 20s` from the receipt’s `seconds`) and size (`38 MB`, the file’s bytes over
     2²⁰), and the tag in its three links if it changed.
   - [`n11-lower-bounds-explainer-article.md`](../../packing/devtools/templates/n11-lower-bounds-explainer-article.md),
     Figure 2: the tag in its three release URLs and the full cut’s length (“runs 8m
     14s”).
   - The plan’s
     [What was published](../../docs/project/specs/active/plan-2026-09-21-video-delivery-profiles.md#what-was-published):
     tag, commit and date, the table rows from the receipts, the page digest prefix and
     stamp, and the cadence findings from step 5; and the URL in
     [The embed](../../docs/project/specs/active/plan-2026-09-21-video-delivery-profiles.md#the-embed)
     if the tag changed.

10. **After it merges**, confirm the deploy as
    [Publishing the Explainer](../../development.md#publishing-the-explainer) says, with
    `python -m devtools.check_published_site --commit <merge commit>`, and play the film
    on the explainer page once to see the new poster and the new stamp.

## Reproducible block reports

From `packing/`, a cohort manifest and a JSONL envelope file produce the report:

```bash
uv run --frozen --all-extras --group dev python -m workbench_tools.block_report \
    /path/to/manifest.json /path/to/trials.jsonl --out /path/to/report.json
```

The manifest schema is `squares.workbench.cohort/v1`. It declares the full source
commit, repository-relative benchmark path (`instrument`), catalogue directory
(`reference_source`), purpose (`research` or `software-validation`) and cohorts.
Each cohort declares its ID, n, style, requested parameter overrides, tuning/held-out or
exploratory partition, block size, step and repair budgets, and ordered seed slots.
Slots explicitly say completed, failed, cancelled or not-started.
Completed slots have exactly one JSONL envelope: `{"cohort":"cohort-id","trial":{...}}`,
with an `AnnealingTrial/v2` receipt.
The [contract tests](tests/test_block_report.py) include an executable complete example.

The report admits geometry through the same rule as run/replay/sweep, checks effective
settings and source/runtime agreement, and preserves unsuccessful blocks and partial
tails.
Rates name their denominators; distributions conditioned on valid outcomes say so.
Wilson intervals describe independent-block sampling assumptions rather than
establishing that a deterministic seed campaign sampled independently.
Zero reference-to-grid gaps have no normalized score.
Unknown cost stays unknown.

Historical summaries are audited by `workbench_tools.historical_summary_audit`; they
cannot be used as raw trials.
See the [annealing runbook](../../packing/campaign/results/annealing/README.md) for
record validation and the limits of the retained evidence.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
