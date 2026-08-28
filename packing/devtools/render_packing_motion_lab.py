#!/usr/bin/env python3
# ruff: noqa: E501, RUF001 -- embedded HTML, CSS, and JavaScript retain readable lines and notation
"""Generate a deterministic, self-contained HTML+SVG square-packing motion lab."""

from __future__ import annotations

import argparse
import html
import json
import math
import sys
from decimal import Decimal
from pathlib import Path

from strif import atomic_output_file

from devtools.packing_motion_studies import CONTACTS, build_motion_lab_manifest, project_scene
from sqpack.motion_lab.assets import asset_text, motion_lab_css
from sqpack.motion_lab.scenarios.exact_n5 import exact_n5_scenario
from sqpack.render.numbers import format_svg_number

VIEW_WIDTH = 760
VIEW_HEIGHT = 620
PLOT_LEFT = Decimal(42)
PLOT_BOTTOM = Decimal(564)
PLOT_SCALE = Decimal(185)
SQUARE_IDS = range(5)
CONTACT_PAIRS = ((0, 3), (0, 4), (1, 4), (2, 4), (3, 4))


def _number(value: float) -> str:
    return format_svg_number(Decimal(repr(value)))


def _transform(x: float, y: float, radians: float) -> str:
    degrees = radians * 180 / math.pi
    return f"translate({_number(x)} {_number(y)}) rotate({_number(degrees)})"


def _static_svg(manifest: dict[str, object]) -> str:
    scenes = manifest["scenes"]
    if not isinstance(scenes, list):
        raise TypeError("motion manifest scenes must be a list")
    scene = next(value for value in scenes if value["id"] == manifest["default_scene"])
    poses = project_scene(scene, 0)
    squares = scene["squares"]
    square_lines = []
    ghost_lines = []
    trail_lines = []
    tangent_lines = []
    label_lines = []
    for pose, square in zip(poses, squares, strict=True):
        square_id = pose.square_id
        fill = html.escape(square["fill"], quote=True)
        transform = _transform(pose.centre_x, pose.centre_y, pose.angle_radians)
        square_lines.append(
            f'<g id="square-{square_id}" data-square="{square_id}" '
            f'transform="{transform}"><rect class="square" x="-.5" y="-.5" '
            f'width="1" height="1" fill="{fill}" /></g>'
        )
        ghost_lines.append(
            f'<g id="ghost-{square_id}" data-square="{square_id}" '
            f'transform="{transform}" display="none"><rect class="ghost-square" x="-.5" '
            'y="-.5" width="1" height="1" /></g>'
        )
        trail_lines.append(
            f'<line id="trail-{square_id}" class="trail" data-square="{square_id}" '
            'display="none" />'
        )
        tangent_lines.append(
            f'<line id="tangent-{square_id}" class="tangent" data-square="{square_id}" '
            'marker-end="url(#arrowhead)" display="none" />'
        )
        screen_x = PLOT_LEFT + PLOT_SCALE * Decimal(repr(pose.centre_x))
        screen_y = PLOT_BOTTOM - PLOT_SCALE * Decimal(repr(pose.centre_y))
        label_lines.append(
            f'<text id="label-{square_id}" class="square-label" '
            f'x="{format_svg_number(screen_x)}" y="{format_svg_number(screen_y + 5)}">'
            f"{square_id}</text>"
        )
    poses_by_id = {pose.square_id: pose for pose in poses}
    base_contacts = set(CONTACTS["base"])
    contact_lines = []
    for first, second in CONTACT_PAIRS:
        first_pose = poses_by_id[first]
        second_pose = poses_by_id[second]
        state_class = (
            "opening"
            if (first, second) == (1, 4)
            else "closing"
            if (first, second) == (0, 3)
            else "persistent"
        )
        hidden = "" if (first, second) in base_contacts else ' display="none"'
        contact_lines.append(
            f'<line id="contact-{first}-{second}" class="contact-link {state_class}" '
            f'data-pair="{first}-{second}" x1="{_number(first_pose.centre_x)}" '
            f'y1="{_number(first_pose.centre_y)}" x2="{_number(second_pose.centre_x)}" '
            f'y2="{_number(second_pose.centre_y)}"{hidden} />'
        )
    contacts = "".join(contact_lines)
    side = scene["container_side"]
    if not isinstance(side, dict) or not isinstance(side.get("decimal"), str):
        raise TypeError("motion scene container side is malformed")
    side_value = side["decimal"]
    return f"""<svg id="motion-stage" viewBox="0 0 {VIEW_WIDTH} {VIEW_HEIGHT}" role="img"
          aria-labelledby="stage-title stage-description">
        <title id="stage-title">Five-square motion scene</title>
        <desc id="stage-description">Five unit squares in a fixed square container. Solid
          shapes are source-backed geometry; dashed shapes show a first-order predictor.
          Base contact pairs are 0–4, 1–4, 2–4, and 3–4.</desc>
        <defs>
          <marker id="arrowhead" viewBox="0 0 10 10" refX="8" refY="5"
            markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#087f8c" />
          </marker>
          <pattern id="obstruction-hatch" width="8" height="8" patternUnits="userSpaceOnUse"
            patternTransform="rotate(45)">
            <line x1="0" y1="0" x2="0" y2="8" stroke="#b42318" stroke-width="2" />
          </pattern>
        </defs>
        <rect class="stage-background" width="{VIEW_WIDTH}" height="{VIEW_HEIGHT}" rx="6" />
        <g id="math-plane" transform="translate({PLOT_LEFT} {PLOT_BOTTOM}) scale({PLOT_SCALE} -{PLOT_SCALE})">
          <rect id="container" class="container" x="0" y="0" width="{side_value}"
            height="{side_value}" />
          <g id="trail-layer" aria-hidden="true">{"".join(trail_lines)}</g>
          <g id="contact-layer" aria-hidden="true">{contacts}</g>
          <g id="ghost-layer" aria-hidden="true">{"".join(ghost_lines)}</g>
          <g id="square-layer">{"".join(square_lines)}</g>
          <g id="tangent-layer" aria-hidden="true">{"".join(tangent_lines)}</g>
        </g>
        <g id="label-layer" aria-hidden="true">{"".join(label_lines)}</g>
        <g id="obstruction-badge" display="none">
          <rect x="583" y="44" width="134" height="82" rx="6"
            fill="url(#obstruction-hatch)" stroke="#b42318" stroke-width="2" />
          <text x="650" y="80" text-anchor="middle" class="obstruction-title">+W blocked</text>
          <text x="650" y="103" text-anchor="middle" class="obstruction-subtitle">at second order</text>
        </g>
      </svg>"""


CSS = motion_lab_css()
MOTION_MODEL_JAVASCRIPT = asset_text("exact-n5-model.js")
JAVASCRIPT = MOTION_MODEL_JAVASCRIPT + asset_text("motion-lab.js")


def render_motion_lab() -> str:
    """Return the complete deterministic HTML artifact."""
    manifest = build_motion_lab_manifest()
    data = json.dumps(manifest, indent=2, sort_keys=True).replace("</", "<\\/")
    scenario = exact_n5_scenario(manifest)
    registry = {
        "contract": "packing.squares:MotionLabShell/v1",
        "schema_version": 1,
        "default_scenario": scenario.scenario_id,
        "scenarios": [scenario.to_record()],
    }
    registry_data = json.dumps(registry, indent=2, sort_keys=True).replace("</", "<\\/")
    svg = _static_svg(manifest)
    source_records = manifest["source_records"]
    if not isinstance(source_records, dict):
        raise TypeError("motion manifest source records must be an object")
    exp042 = html.escape(str(source_records["exp-042"]))
    exp036 = html.escape(str(source_records["exp-036"]))
    return f"""<!doctype html>
<html lang="en" data-contract="packing.squares:MotionLab/v1"
  data-shell-contract="packing.squares:MotionLabShell/v1">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta http-equiv="Content-Security-Policy"
    content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline';
      img-src data:; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'" />
  <title>n=5 square-packing motion lab</title>
  <style>{CSS}</style>
  <noscript><style>
    .controls, .readout, #live-region {{ display: none !important; }}
    .lab-grid {{ display: block !important; }}
    .stage-card {{ max-width: 760px; margin-inline: auto; }}
  </style></noscript>
</head>
<body>
  <header>
    <h1>n=5 square-packing motion lab</h1>
    <p class="lede">Scrub six exact R4/R5 release paths or inspect the obstructed +W
      first-order ghost. Solid geometry, dashed predictors, contact-graph edges, and
      evidence labels are kept distinct so the picture cannot silently upgrade a claim.</p>
  </header>
  <main>
    <noscript><p class="noscript-notice">JavaScript is disabled. The static figure shows
      the R4/A base packing and its source-backed base contact graph. Use the retained
      publication SVGs for a script-free document artifact.</p></noscript>
    <section class="controls" aria-label="Motion controls">
      <div class="control">
        <label for="motion-select">Motion</label>
        <select id="motion-select">
          <option value="R4">R4 certified path</option>
          <option value="R5">R5 certified path</option>
          <option value="plus-W">+W obstruction</option>
        </select>
      </div>
      <div class="control">
        <label for="stratum-select">Base stratum</label>
        <select id="stratum-select">
          <option value="A">A</option>
          <option value="interior">Interior</option>
          <option value="B">B</option>
        </select>
      </div>
      <div class="control">
        <label for="owner-select">Obstruction branch</label>
        <select id="owner-select" disabled>
          <option value="owner-4">Owner 4</option>
          <option value="owner-3">Owner 3</option>
        </select>
      </div>
      <button id="play-button" class="primary" type="button">Play</button>
      <button id="restart-button" type="button">Restart</button>
      <div class="control parameter">
        <label for="parameter-input">Path position</label>
        <input id="parameter-input" type="range" min="0" max="1000" value="0" step="1"
          aria-valuetext="0% of interval; u = 0.0000000" />
      </div>
      <div class="toggle-row" role="group" aria-labelledby="overlays-label">
        <span id="overlays-label" class="control-label">Overlays</span>
        <label><input id="ids-toggle" type="checkbox" checked /> Square IDs</label>
        <label><input id="contacts-toggle" type="checkbox" checked /> Contact graph</label>
        <label><input id="trails-toggle" type="checkbox" checked /> Center trails</label>
        <label><input id="tangent-toggle" type="checkbox" checked /> Tangent predictor</label>
      </div>
    </section>
    <div class="lab-grid">
      <section class="stage-card" aria-label="Motion visualization">
        {svg}
        <p class="figure-key">
          <span class="key"><span class="swatch"></span> source-backed pose</span>
          <span class="key"><span class="swatch ghost"></span> first-order predictor</span>
          <span class="key"><span class="swatch contact"></span> contact-graph relation</span>
        </p>
      </section>
      <aside class="readout" aria-labelledby="readout-title">
        <h2 id="readout-title">Scene evidence</h2>
        <dl class="status-grid">
          <div><dt>Scene</dt><dd id="scene-value">R4 at A</dd></div>
          <div><dt>Parameter</dt><dd><code id="parameter-name">u</code> =
            <code id="parameter-value">0.0000000</code></dd></div>
          <div><dt>Orientation</dt><dd id="angle-value"></dd></div>
          <div><dt>Contacts</dt><dd id="contacts-value"></dd></div>
          <div><dt>Evidence</dt><dd id="evidence-value"></dd></div>
          <div><dt>Source record</dt><dd><code id="source-value">{exp042}</code></dd></div>
        </dl>
        <p id="claim-value" class="claim"></p>
        <section id="branch-panel" class="branch" hidden aria-label="Second-order branch">
          <strong id="branch-title"></strong>
          <p><code id="branch-formula"></code></p>
          <p id="branch-value"></p>
          <p id="branch-note"></p>
        </section>
        <p class="fine-print">Contact marks are graph edges between square centers, not
          Euclidean gap segments. The exact contact inventory comes from <code>{exp042}</code>.
          The +W direction comes from exp-035, and its contradiction comes from
          <code>{exp036}</code>.</p>
        <p id="motion-note" class="fine-print"></p>
      </aside>
    </div>
    <p id="live-region" class="fine-print" role="status" aria-live="polite"></p>
  </main>
  <script id="scenario-registry" type="application/json">{registry_data}</script>
  <script id="motion-data" type="application/json">{data}</script>
  <script>{JAVASCRIPT}</script>
</body>
</html>
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare the output path with a fresh deterministic render without writing",
    )
    return parser.parse_args()


def _require_current_output(path: Path, rendered: str) -> None:
    if path.read_text(encoding="utf-8") != rendered:
        raise ValueError(f"retained motion lab differs from fresh render: {path}")


def main() -> int:
    args = parse_args()
    try:
        rendered = render_motion_lab()
        if args.check:
            _require_current_output(args.output, rendered)
            print(f"PASS: {args.output} matches the deterministic motion-lab render")
        else:
            with atomic_output_file(args.output, make_parents=True) as temporary:
                temporary.write_text(rendered, encoding="utf-8")
            print(f"wrote {args.output} ({len(rendered.encode())} bytes)")
    except (OSError, TypeError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
