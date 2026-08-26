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
        <rect class="stage-background" width="{VIEW_WIDTH}" height="{VIEW_HEIGHT}" rx="18" />
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
          <rect x="583" y="44" width="134" height="82" rx="12"
            fill="url(#obstruction-hatch)" stroke="#b42318" stroke-width="2" />
          <text x="650" y="80" text-anchor="middle" class="obstruction-title">+W blocked</text>
          <text x="650" y="103" text-anchor="middle" class="obstruction-subtitle">at second order</text>
        </g>
      </svg>"""


CSS = r"""
:root {
  color-scheme: light;
  --paper: #f7f6f2;
  --panel: #ffffff;
  --ink: #171717;
  --muted: #5d615f;
  --line: #d9d8d2;
  --accent: #087f8c;
  --contact: #b19610;
  --danger: #b42318;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--paper); color: var(--ink); }
header, main { width: min(1240px, calc(100% - 32px)); margin-inline: auto; }
header { padding: 34px 0 18px; }
h1 { margin: 0; font-size: clamp(1.65rem, 3vw, 2.5rem); letter-spacing: -.035em; }
.lede { max-width: 78ch; margin: 10px 0 0; color: var(--muted); line-height: 1.55; }
.controls, .stage-card, .readout { background: var(--panel); border: 1px solid var(--line); border-radius: 18px; }
.controls { display: flex; flex-wrap: wrap; gap: 14px; align-items: end; padding: 16px; margin-bottom: 16px; }
.control { display: grid; gap: 6px; min-width: 140px; }
.control.parameter { flex: 1 1 260px; }
label, .control-label { color: var(--muted); font-size: .82rem; font-weight: 700; letter-spacing: .02em; }
select, button, input[type="range"] { font: inherit; }
select, button { min-height: 44px; border: 1px solid #aaa9a3; border-radius: 10px; background: #fff; color: var(--ink); padding: 0 12px; }
button { cursor: pointer; font-weight: 700; }
button.primary { background: var(--ink); color: #fff; border-color: var(--ink); }
button:disabled { cursor: not-allowed; opacity: .45; }
button:focus-visible, select:focus-visible, input:focus-visible { outline: 3px solid #70c6cf; outline-offset: 2px; }
.toggle-row { display: flex; flex-wrap: wrap; gap: 8px 14px; width: 100%; padding-top: 2px; }
.toggle-row > .control-label { flex: 0 0 100%; }
.toggle-row label { display: inline-flex; align-items: center; gap: 7px; min-height: 36px; color: var(--ink); font-weight: 600; }
.lab-grid { display: grid; grid-template-columns: minmax(0, 1.65fr) minmax(280px, .85fr); gap: 16px; align-items: start; }
.stage-card { overflow: hidden; }
#motion-stage { display: block; width: 100%; height: auto; }
.stage-background { fill: #fbfaf7; }
.container { fill: #fff; stroke: #000; stroke-width: 1.5; vector-effect: non-scaling-stroke; }
.square { fill-opacity: .76; stroke: #000; stroke-width: 1.5; vector-effect: non-scaling-stroke; }
.ghost-square { fill: none; stroke: var(--accent); stroke-width: 2.2; stroke-dasharray: 8 5; vector-effect: non-scaling-stroke; }
.trail { stroke: #6b6f6d; stroke-width: 1.5; stroke-dasharray: 2 5; vector-effect: non-scaling-stroke; }
.tangent { stroke: var(--accent); stroke-width: 2.2; stroke-dasharray: 7 5; vector-effect: non-scaling-stroke; }
.contact-link { stroke: var(--contact); stroke-width: 8; stroke-opacity: .62; vector-effect: non-scaling-stroke; }
.contact-link.opening { stroke-dasharray: 9 6; }
.contact-link.closing { stroke-dasharray: 2 5; stroke-width: 10; }
.square-label { fill: #000; font-size: 14px; font-weight: 800; text-anchor: middle; dominant-baseline: middle; paint-order: stroke; stroke: #fff; stroke-width: 3px; }
.obstruction-title { fill: #fff; font-size: 17px; font-weight: 900; paint-order: stroke; stroke: var(--danger); stroke-width: 5px; }
.obstruction-subtitle { fill: #fff; font-size: 12px; font-weight: 800; paint-order: stroke; stroke: var(--danger); stroke-width: 4px; }
.figure-key { display: flex; flex-wrap: wrap; gap: 12px 20px; margin: 0; padding: 14px 18px 17px; border-top: 1px solid var(--line); color: var(--muted); font-size: .85rem; }
.key { display: inline-flex; align-items: center; gap: 8px; }
.swatch { width: 28px; height: 0; border-top: 3px solid #000; }
.swatch.ghost { border-color: var(--accent); border-top-style: dashed; }
.swatch.contact { border-color: var(--contact); border-width: 7px; opacity: .65; }
.readout { padding: 18px; }
.readout h2 { margin: 0 0 14px; font-size: 1.15rem; }
.status-grid { display: grid; gap: 12px; margin: 0; }
.status-grid div { padding-bottom: 11px; border-bottom: 1px solid #ecebe6; }
.status-grid div:last-child { border-bottom: 0; }
dt { color: var(--muted); font-size: .78rem; font-weight: 800; text-transform: uppercase; letter-spacing: .055em; }
dd { margin: 4px 0 0; line-height: 1.45; }
code { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: .88em; overflow-wrap: anywhere; }
.claim { margin: 16px 0 0; padding: 12px 14px; background: #eff7f7; border-left: 4px solid var(--accent); border-radius: 8px; line-height: 1.5; }
.claim.obstructed { background: #fff0ee; border-color: var(--danger); }
.branch { margin-top: 16px; padding: 13px; border: 1px solid #e1b0aa; border-radius: 10px; background: #fff8f7; }
.branch p { margin: 6px 0; line-height: 1.45; }
.fine-print { margin: 14px 0 0; color: var(--muted); font-size: .82rem; line-height: 1.45; }
.noscript-notice { margin: 0 0 16px; padding: 12px 14px; border: 2px solid var(--danger); border-radius: 10px; background: #fff; line-height: 1.5; }
@media (max-width: 860px) { .lab-grid { grid-template-columns: 1fr; } }
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { scroll-behavior: auto !important; transition: none !important; } }
"""


MOTION_MODEL_JAVASCRIPT = r"""
"use strict";
function scalar(value) { return Number(value.decimal); }
function baseAngle(square) { return Number(square.orientation.radians || 0); }

function posesAt(scene, progress, tangent) {
  const extent = scalar(scene.parameter.upper);
  const parameter = extent * progress;
  return scene.squares.map((square) => {
    const x = scalar(square.centre_start.x) + parameter * scalar(square.centre_derivative.x);
    const y = scalar(square.centre_start.y) + parameter * scalar(square.centre_derivative.y);
    const velocity = scalar(square.angle_derivative_at_zero);
    let angle = baseAngle(square);
    if (scene.mode === "certified-path" && square.orientation.kind === "rational-half-angle") {
      angle = tangent ? scene.sigma * parameter : 2 * Math.atan(scene.sigma * parameter / 2);
    } else if (scene.mode === "second-order-obstruction" && tangent) {
      angle += velocity * parameter;
    }
    return { id: square.id, x, y, angle };
  });
}

function phaseAt(scene, progress) {
  if (scene.mode === "second-order-obstruction" || progress === 0) return "base";
  if (progress === 1) return "endpoint";
  return "open_interval";
}

function sceneControlState(scene) {
  const certifiedPath = scene.mode === "certified-path";
  return {
    ownerDisabled: certifiedPath,
    playDisabled: !certifiedPath,
    branchHidden: certifiedPath,
  };
}

function normalizedPercent(progress) {
  return (progress * 100).toFixed(1).replace(/\.0$/, "");
}

function parameterValueText(scene, progress) {
  const value = scalar(scene.parameter.upper) * progress;
  return `${normalizedPercent(progress)}% of interval; ${scene.parameter.name} = ${value.toFixed(7)}`;
}

function stageDescriptionText(scene, progress) {
  const percent = normalizedPercent(progress);
  const phase = phaseAt(scene, progress);
  const contacts = (scene.contacts[phase] || [])
    .map((pair) => `${pair[0]}–${pair[1]}`)
    .join(", ");
  if (scene.mode === "second-order-obstruction") {
    return `Five unit squares in a fixed square container, showing +W at ${scene.stratum}. `
      + `The solid packing stays at its base pose; the dashed first-order predictor is `
      + `shown at ${percent}% of the display scale and is obstructed at second order. `
      + `Base contact pairs: ${contacts}.`;
  }
  return `Five unit squares in a fixed square container, showing ${scene.class} at `
    + `${scene.stratum}, ${percent}% through the certified path. Solid squares show the `
    + `exact pose; dashed squares, when enabled, show the first-order tangent predictor. `
    + `Active contact pairs: ${contacts}.`;
}
"""


JAVASCRIPT = (
    MOTION_MODEL_JAVASCRIPT
    + r"""
const byId = (id) => document.getElementById(id);
const manifest = JSON.parse(byId("motion-data").textContent);
const scenes = new Map(manifest.scenes.map((scene) => [scene.id, scene]));
const motionSelect = byId("motion-select");
const stratumSelect = byId("stratum-select");
const ownerSelect = byId("owner-select");
const progressInput = byId("parameter-input");
const playButton = byId("play-button");
const restartButton = byId("restart-button");
const idsToggle = byId("ids-toggle");
const contactsToggle = byId("contacts-toggle");
const trailsToggle = byId("trails-toggle");
const tangentToggle = byId("tangent-toggle");
const liveRegion = byId("live-region");
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const left = 42;
const bottom = 564;
const scale = 185;
const durationMilliseconds = 5000;
let animationFrame = null;
let animationStart = null;
let animationOrigin = 0;

function currentScene() { return scenes.get(`${motionSelect.value}:${stratumSelect.value}`); }
function currentProgress() { return Number(progressInput.value) / Number(progressInput.max); }
function transform(pose) {
  return `translate(${pose.x} ${pose.y}) rotate(${pose.angle * 180 / Math.PI})`;
}
function screenPoint(pose) { return [left + scale * pose.x, bottom - scale * pose.y]; }

function pairKey(pair) { return `${pair[0]}-${pair[1]}`; }
function contactLabel(pair) { return `${pair[0]}–${pair[1]}`; }

function setLine(line, first, second) {
  line.setAttribute("x1", first.x);
  line.setAttribute("y1", first.y);
  line.setAttribute("x2", second.x);
  line.setAttribute("y2", second.y);
}

function setShown(element, shown) {
  if (shown) element.removeAttribute("display");
  else element.setAttribute("display", "none");
}

function updateGeometry(scene, progress) {
  const obstruction = scene.mode === "second-order-obstruction";
  const actual = posesAt(scene, obstruction ? 0 : progress, false);
  const base = posesAt(scene, 0, false);
  const predictor = posesAt(scene, progress, true);
  const endpoint = posesAt(scene, 1, true);
  const extent = scalar(scene.parameter.upper);
  actual.forEach((pose, index) => {
    const square = byId(`square-${pose.id}`);
    square.setAttribute("transform", transform(pose));
    const ghost = byId(`ghost-${pose.id}`);
    ghost.setAttribute("transform", transform(predictor[index]));
    setShown(ghost, tangentToggle.checked && progress > 0);
    const label = byId(`label-${pose.id}`);
    const labelPoint = screenPoint(pose);
    label.setAttribute("x", labelPoint[0]);
    label.setAttribute("y", labelPoint[1] + 5);
    setShown(label, idsToggle.checked);
    const trail = byId(`trail-${pose.id}`);
    setLine(trail, base[index], endpoint[index]);
    const centreMoves = base[index].x !== endpoint[index].x || base[index].y !== endpoint[index].y;
    setShown(trail, trailsToggle.checked && centreMoves);
    const tangent = byId(`tangent-${pose.id}`);
    const start = base[index];
    const arrowEnd = {
      x: start.x + scalar(scene.squares[index].centre_derivative.x) * extent * .72,
      y: start.y + scalar(scene.squares[index].centre_derivative.y) * extent * .72,
    };
    setLine(tangent, start, arrowEnd);
    setShown(
      tangent,
      tangentToggle.checked && (start.x !== arrowEnd.x || start.y !== arrowEnd.y),
    );
  });
  setShown(byId("obstruction-badge"), obstruction);
  updateContacts(scene, progress, actual);
}

function updateContacts(scene, progress, poses) {
  const phase = phaseAt(scene, progress);
  const active = new Set((scene.contacts[phase] || []).map(pairKey));
  const persistent = new Set(["0-4", "2-4", "3-4"]);
  const obstruction = scene.mode === "second-order-obstruction";
  for (const key of ["0-3", "0-4", "1-4", "2-4", "3-4"]) {
    const line = byId(`contact-${key}`);
    const [first, second] = key.split("-").map(Number);
    setLine(line, poses[first], poses[second]);
    setShown(line, contactsToggle.checked && active.has(key));
    const stateClass = obstruction
      ? "base-only"
      : persistent.has(key)
        ? "persistent"
        : key === "1-4"
          ? "opening"
          : "closing";
    line.setAttribute("class", `contact-link ${stateClass}`);
  }
  const labels = (scene.contacts[phase] || []).map(contactLabel).join(", ");
  const event = obstruction
    ? "Base graph only; no feasible contact evolution is certified"
    : phase === "base"
      ? "1–4 opens immediately"
      : phase === "endpoint"
        ? "0–3 closes here"
        : "1–4 is open; 0–3 has not closed";
  byId("contacts-value").textContent = `${labels}. ${event}.`;
}

function updateReadout(scene, progress) {
  const value = scalar(scene.parameter.upper) * progress;
  progressInput.setAttribute("aria-valuetext", parameterValueText(scene, progress));
  byId("stage-description").textContent = stageDescriptionText(scene, progress);
  byId("scene-value").textContent = `${scene.class} at ${scene.stratum}`;
  byId("parameter-name").textContent = scene.parameter.name;
  byId("parameter-value").textContent = value.toFixed(7);
  byId("evidence-value").textContent = scene.evidence.status.replaceAll("-", " ");
  byId("source-value").textContent = scene.evidence.source_record;
  if (scene.evidence.geometry_source_record) {
    byId("source-value").textContent += `; ghost geometry: ${scene.evidence.geometry_source_record}`;
  }
  byId("claim-value").textContent = scene.evidence.claim;
  byId("claim-value").classList.toggle("obstructed", scene.mode === "second-order-obstruction");
  const controls = sceneControlState(scene);
  const rotating = controls.ownerDisabled;
  const angle = rotating ? 2 * Math.atan(scene.sigma * value / 2) * 180 / Math.PI : value * 180 / Math.PI;
  byId("angle-value").textContent = rotating
    ? `${angle.toFixed(5)}° on square 1; θ=2 atan(σu/2)`
    : `${angle.toFixed(5)}° linear ghost on squares 3 and 4`;
  ownerSelect.disabled = controls.ownerDisabled;
  playButton.disabled = controls.playDisabled;
  byId("branch-panel").hidden = controls.branchHidden;
  if (!rotating) {
    const branch = scene.branches[ownerSelect.value];
    const amount = scalar(branch.coefficient) * value * value;
    byId("branch-title").textContent = `${branch.label}: ${branch.quantity}`;
    byId("branch-formula").textContent = branch.formula;
    byId("branch-value").textContent = `displayed quadratic term: ${amount.toExponential(5)}`;
    byId("branch-note").textContent = branch.note;
  }
  byId("motion-note").textContent = reduceMotion
    ? "Reduced-motion preference detected: the lab starts paused; manual scrubbing remains available."
    : "The lab starts paused and runs one pass only after Play is pressed.";
}

function update() {
  const scene = currentScene();
  const progress = currentProgress();
  updateGeometry(scene, progress);
  updateReadout(scene, progress);
}

function stopPlayback() {
  if (animationFrame !== null) cancelAnimationFrame(animationFrame);
  animationFrame = null;
  animationStart = null;
  playButton.textContent = "Play";
}

function tick(timestamp) {
  if (animationStart === null) animationStart = timestamp;
  const elapsed = (timestamp - animationStart) / durationMilliseconds;
  const next = Math.min(1, animationOrigin + elapsed);
  progressInput.value = String(Math.round(next * Number(progressInput.max)));
  update();
  if (next >= 1) {
    stopPlayback();
    liveRegion.textContent = "Certified path reached its endpoint.";
    return;
  }
  animationFrame = requestAnimationFrame(tick);
}

function startPlayback() {
  if (currentScene().mode !== "certified-path") return;
  if (currentProgress() >= 1) progressInput.value = "0";
  animationOrigin = currentProgress();
  animationStart = null;
  playButton.textContent = "Pause";
  liveRegion.textContent = "Certified path playback started.";
  animationFrame = requestAnimationFrame(tick);
}

playButton.addEventListener("click", () => {
  if (animationFrame === null) startPlayback(); else stopPlayback();
});
restartButton.addEventListener("click", () => {
  stopPlayback();
  progressInput.value = "0";
  update();
  liveRegion.textContent = "Scene returned to its base configuration.";
});
progressInput.addEventListener("input", () => { stopPlayback(); update(); });
for (const select of [motionSelect, stratumSelect]) {
  select.addEventListener("change", () => {
    stopPlayback();
    progressInput.value = "0";
    update();
    liveRegion.textContent = `${currentScene().class} ${currentScene().stratum} scene selected.`;
  });
}
ownerSelect.addEventListener("change", update);
for (const toggle of [idsToggle, contactsToggle, trailsToggle, tangentToggle]) {
  toggle.addEventListener("change", update);
}
update();
"""
)


def render_motion_lab() -> str:
    """Return the complete deterministic HTML artifact."""
    manifest = build_motion_lab_manifest()
    data = json.dumps(manifest, indent=2, sort_keys=True).replace("</", "<\\/")
    svg = _static_svg(manifest)
    source_records = manifest["source_records"]
    if not isinstance(source_records, dict):
        raise TypeError("motion manifest source records must be an object")
    exp042 = html.escape(str(source_records["exp-042"]))
    exp036 = html.escape(str(source_records["exp-036"]))
    return f"""<!doctype html>
<html lang="en" data-contract="packing.squares:MotionLab/v1">
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
