#!/usr/bin/env python3
# ruff: noqa: E501 -- embedded HTML retains readable labels and accessibility copy
"""Render the served, editable square-packing Motion Lab profile."""

from __future__ import annotations

import json

from sqpack.motion_lab.assets import asset_text, motion_lab_css
from sqpack.motion_lab.scenarios.free_quench import free_quench_scenario

DEFAULT_SQUARE_COUNT = 5
DEFAULT_SEED = 7
DEFAULT_SIDE = 3.2


def render_general_motion_lab(*, n: int, seed: int, side: float) -> str:
    """Return the deterministic live profile for one editable starting pose."""
    scenario = free_quench_scenario(n=n, seed=seed, side=side)
    scenario_data = json.dumps(scenario.to_record(), indent=2, sort_keys=True).replace(
        "</", "<\\/"
    )
    css = motion_lab_css()
    javascript = asset_text("free-quench-model.js") + asset_text("free-quench.js")
    return f"""<!doctype html>
<html lang="en" data-contract="packing.squares:GeneralMotionLab/v1"
  data-shell-contract="packing.squares:MotionLabShell/v1">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta http-equiv="Content-Security-Policy"
    content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline';
      img-src data:; connect-src 'self'; object-src 'none'; base-uri 'none'; form-action 'none'" />
  <title>Square-packing Motion Lab</title>
  <style>{css}</style>
</head>
<body class="general-motion-lab">
  <header>
    <h1>Square-packing Motion Lab</h1>
    <p class="lede">Assemble a starting pose, optionally snap squares into temporary
      chunks, then release every chunk and watch the unconstrained numerical quench.
      Fixed-angle LP states and angular probes use different marks.</p>
  </header>
  <main>
    <noscript><p class="noscript-notice">This live scenario needs JavaScript and the
      loopback numerical service. The <a href="/exact-n5">exact n=5 scenario</a> remains
      available as a self-contained static artifact.</p></noscript>
    <section class="controls setup-controls" aria-label="Scenario and setup controls">
      <div class="control">
        <label for="scenario-select">Scenario</label>
        <select id="scenario-select">
          <option value="free-quench" selected>Setup + free quench</option>
          <option value="exact-n5">Exact n=5 paths</option>
        </select>
      </div>
      <div class="control compact-control">
        <label for="n-input">Squares</label>
        <input id="n-input" type="number" min="1" max="20" step="1" value="{n}" />
      </div>
      <div class="control compact-control">
        <label for="side-input">Starting side</label>
        <input id="side-input" type="number" min="1.01" max="20" step="0.05"
          value="{side:.12g}" />
      </div>
      <div class="control compact-control">
        <label for="seed-input">Seed</label>
        <input id="seed-input" type="number" step="1" value="{seed}" />
      </div>
      <button id="new-pose-button" type="button">New pose</button>
      <button id="randomize-all-button" type="button">Randomize all</button>
      <button id="reset-button" type="button">Reset</button>
      <div class="toggle-row editor-toggles" role="group" aria-label="Editor behavior">
        <label><input id="snapping-toggle" type="checkbox" checked /> Sticky setup</label>
        <span class="control-note">Drag a square to move its chunk. Shift-drag rotates
          the chunk. Arrow keys move; Q/E rotate.</span>
      </div>
    </section>

    <section class="controls run-controls" aria-label="Numerical run controls">
      <div class="control compact-control">
        <label for="sweeps-input">Maximum sweeps</label>
        <input id="sweeps-input" type="number" min="1" max="1000" step="1" value="4" />
      </div>
      <div class="control compact-control">
        <label for="budget-input">Time budget (s)</label>
        <input id="budget-input" type="number" min="0.1" max="300" step="0.5" value="5" />
      </div>
      <button id="run-button" class="primary" type="button">Release + run quench</button>
      <button id="download-button" type="button" disabled>Download trace</button>
      <span class="control-note release-note">Setup snapping is released before every numerical run;
        the optimizer receives only side, centers, and angles.</span>
    </section>

    <div class="lab-grid general-lab-grid">
      <section class="stage-card" aria-label="Editable square configuration">
        <svg id="free-stage" viewBox="0 0 620 620" role="img" tabindex="0"
          aria-labelledby="free-stage-title free-stage-description">
          <title id="free-stage-title">Editable square-packing configuration</title>
          <desc id="free-stage-description">Unit squares in a square container. Drag
            a square to translate its temporary chunk; Shift-drag rotates the chunk.</desc>
          <rect class="stage-background" width="620" height="620" />
          <g id="free-math-plane">
            <rect id="free-container" class="container" x="0" y="0" />
            <g id="accepted-layer"></g>
            <g id="probe-layer" aria-hidden="true"></g>
          </g>
          <g id="free-label-layer" aria-hidden="true"></g>
        </svg>
        <div class="stage-toolbar" aria-label="Selected chunk controls">
          <span id="selection-value">No chunk selected</span>
          <button id="rotate-left-button" type="button" disabled aria-label="Rotate selected chunk left">Rotate &minus;15°</button>
          <button id="rotate-right-button" type="button" disabled aria-label="Rotate selected chunk right">Rotate +15°</button>
        </div>
        <p class="figure-key">
          <span class="key"><span class="swatch setup"></span> editable or accepted state</span>
          <span class="key"><span class="swatch lp"></span> fixed-angle LP state</span>
          <span class="key"><span class="swatch probe"></span> angular probe, not accepted</span>
        </p>
      </section>

      <aside class="readout general-readout" aria-labelledby="run-readout-title">
        <h2 id="run-readout-title">Setup</h2>
        <dl class="status-grid">
          <div><dt>Mode</dt><dd id="mode-value">Editable setup</dd></div>
          <div><dt>Temporary chunks</dt><dd id="groups-value">{n} singleton chunks</dd></div>
          <div><dt>Geometry</dt><dd id="diagnostics-value">Checking…</dd></div>
          <div><dt>Phase</dt><dd><span id="phase-badge" class="phase-badge phase-setup">Setup</span></dd></div>
          <div><dt>Event</dt><dd id="event-value">No numerical run yet.</dd></div>
          <div><dt>Counters</dt><dd id="counters-value">—</dd></div>
        </dl>
        <p id="evidence-value" class="claim">The setup pose is editor input. It may
          overlap or leave the container; those defects are shown rather than repaired.</p>
        <p class="fine-print">A dashed probe is a solver evaluation, not the current
          accepted packing. Smooth motion between retained states is illustrative; the
          numbered event endpoints are the recorded numerical states.</p>
      </aside>
    </div>

    <section id="timeline-panel" class="timeline-panel" aria-labelledby="timeline-title" hidden>
      <div class="timeline-heading">
        <div>
          <h2 id="timeline-title">Quench trace</h2>
          <p id="trace-summary" class="fine-print"></p>
        </div>
        <div class="timeline-buttons">
          <button id="previous-event-button" type="button">Previous</button>
          <button id="play-trace-button" class="primary" type="button">Play</button>
          <button id="next-event-button" type="button">Next</button>
          <button id="return-setup-button" type="button">Return to setup</button>
        </div>
      </div>
      <label for="timeline-input">Event <output id="timeline-output">1 / 1</output></label>
      <input id="timeline-input" type="range" min="0" max="0" value="0" step="1" />
      <ol id="timeline-list" class="timeline-list"></ol>
    </section>
    <p id="live-region" class="fine-print" role="status" aria-live="polite"></p>
  </main>
  <script id="free-scenario" type="application/json">{scenario_data}</script>
  <script>{javascript}</script>
</body>
</html>
"""
