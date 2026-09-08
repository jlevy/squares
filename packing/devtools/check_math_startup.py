"""Measure natural math startup and neighboring text movement, without delaying fonts.

Each load starts a fresh browser and context. Browser caches are cold; the operating
system's file and font caches are uncontrolled. Paired runs alternate control and
candidate order and retain every observation, including invalid loads. Times are
relative to navigation start. An animation-frame observation is an opportunity to
paint, not a compositor presentation timestamp. Exposed math includes the active
document below the fold; the probe never scrolls to manufacture an earlier result.

The primary latency measurement is ``parameters_ready_ms``: all fourteen initial
Figure 6 math labels and readouts are readable in the same observed frame. Geometry
follows persistent adjacent text characters, including their positions relative to
the containing block. Text-range bottoms are baseline proxies, not font baselines.
Layout and latency remain descriptive: this tool does not invent a performance
acceptance threshold. Missing math, anchors, or instrumentation invalidates a run.

The explicit ``parameters`` mode measures only the fourteen parameter targets. It
omits all-page text discovery and geometry, retaining the same source and exposure
checks once each target can be visible, and stops frame sampling when all fourteen
are readable. This records an animation-frame paint opportunity, not a compositor
presentation or first-contentful-paint timestamp. Final settlement rediscovers and
validates every target; ``finish_validation_ms`` records that later work separately
from ``sampler_total_ms``. Its timings form a separate instrument regime; compare
control and candidate within that mode, never across modes.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import platform
import statistics
import subprocess
import sys
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Literal

from devtools.check_math_loading import EXPOSED, page_url
from devtools.render_explainer_pdf import BROWSER_OVERRIDE, PAGE, READY, SETTLED

type BrowserName = Literal["chromium", "firefox", "webkit"]
type MeasurementMode = Literal["full", "parameters"]
type JsonRecord = dict[str, Any]

EXPECTED_PARAMETERS = 14

#: Installed before parsing. Wrappers observe the original calls and return their
#: original promises, preserving resolution order and rejection behavior. No waits,
#: styles, input events, or rendering mutations are introduced by the instrument.
_STARTUP_SCRIPT = r"""
(() => {
  const mode = '__MODE__', full = mode === 'full';
  const clock = () => performance.now();
  const state = globalThis.__mathStartup = {
    mode,
    metrics: {instrumentation_installed_ms: clock()},
    counters: {frames: 0, font_hooks: 0, katex_hooks: 0, runtime_hooks: 0,
      katex_calls: 0, ready_calls: 0, render_calls: 0, hydrate_calls: 0,
      hydrate_hooks: 0, anchor_samples: 0},
    capabilities: {longtask: false, layout_shift: false},
    fonts: [], ready: [], renders: [], hydrates: [], katex: [], longtasks: [], shifts: [],
    targets: [], anchors: [], snapshots: [], errors: [], stop: false,
    pre_reveal_frame_observed: false, pending_observed: false,
  };
  const metrics = state.metrics;
  const first = (name, value = clock()) => {
    if (metrics[name] == null) metrics[name] = value;
  };
  const observed = (promise, record) => {
    // Returning this exact promise matters: observation must not become a font gate.
    if (promise && typeof promise.then === 'function') promise.then(
      () => { record.end_ms = clock(); record.outcome = 'resolved'; },
      error => { record.end_ms = clock(); record.outcome = 'rejected';
        record.error = String(error); });
    return promise;
  };
  const originals = [];
  function wrap(owner, key, make) {
    const original = owner?.[key];
    if (typeof original !== 'function') return false;
    owner[key] = make(original);
    originals.push(() => { owner[key] = original; });
    return true;
  }
  const fontOwners = [globalThis.FontFace?.prototype,
    document.fonts && Object.getPrototypeOf(document.fonts)];
  for (const [index, owner] of fontOwners.entries()) {
    if (wrap(owner, 'load', original => function(...args) {
      if (state.stop) return original.apply(this, args);
      const record = {kind: index === 0 ? 'face' : 'set', start_ms: clock(),
        request: index === 0 ? `${this.family} ${this.style} ${this.weight}` : String(args[0]),
        outcome: 'pending'};
      state.fonts.push(record);
      try { return observed(original.apply(this, args), record); }
      catch (error) { record.end_ms = clock(); record.outcome = 'threw'; throw error; }
    })) state.counters.font_hooks++;
  }
  if (document.fonts) {
    document.fonts.addEventListener('loading', () => first('font_loading_event_ms'));
    document.fonts.addEventListener('loadingdone', () => {
      metrics.font_loading_done_ms = clock();
    });
  }
  const sources = new WeakMap();
  function globalObject(name, install) {
    let value = globalThis[name];
    const installed = new WeakSet();
    const accept = object => {
      if (object && !installed.has(object)) { installed.add(object); install(object); }
    };
    Object.defineProperty(globalThis, name, {configurable: true, enumerable: true,
      get: () => value, set: object => { value = object; accept(object); }});
    accept(value);
  }
  globalObject('katex', api => {
    first('katex_available_ms');
    if (wrap(api, 'render', original => function(...args) {
      if (state.stop) return original.apply(this, args);
      const record = {start_ms: clock(), source: String(args[0]),
        target: args[1]?.id || null};
      state.counters.katex_calls++;
      try { return original.apply(this, args); }
      finally { record.duration_ms = clock() - record.start_ms; state.katex.push(record); }
    })) state.counters.katex_hooks++;
  });
  globalObject('kpressMathText', api => {
    first('runtime_available_ms');
    if (wrap(api, 'ready', original => function(...args) {
      first('first_ready_call_ms'); state.counters.ready_calls++;
      const record = {start_ms: clock(), outcome: 'pending'};
      state.ready.push(record);
      return observed(original.apply(this, args), record);
    })) state.counters.runtime_hooks++;
    if (wrap(api, 'hydrate', original => function(...args) {
      state.counters.hydrate_calls++;
      const [source, node] = args;
      const record = {start_ms: clock(), source: String(source), target: node?.id || null,
        outcome: 'pending'};
      if (node) sources.set(node, record);
      state.hydrates.push(record);
      return observed(original.apply(this, args), record);
    })) state.counters.hydrate_hooks++;
    if (wrap(api, 'render', original => function(...args) {
      state.counters.render_calls++;
      const [source, node] = args;
      const record = {start_ms: clock(), source: String(source), target: node?.id || null,
        outcome: 'pending'};
      if (node) sources.set(node, record);
      state.renders.push(record);
      return observed(original.apply(this, args), record);
    })) state.counters.runtime_hooks++;
  });
  const observers = [], drainObservers = [];
  for (const [type, capability, records] of [
    ['longtask', 'longtask', state.longtasks], ['layout-shift', 'layout_shift', state.shifts],
  ]) {
    if (!globalThis.PerformanceObserver?.supportedEntryTypes?.includes(type)) continue;
    state.capabilities[capability] = true;
    const receive = entries => {
      for (const entry of entries) records.push(type === 'longtask'
        ? {start_ms: entry.startTime, duration_ms: entry.duration}
        : {start_ms: entry.startTime, value: entry.value,
          had_recent_input: entry.hadRecentInput,
          sources: (entry.sources || []).map(source => ({
            node: source.node?.id || source.node?.tagName || null,
            previous: source.previousRect.toJSON(), current: source.currentRect.toJSON(),
          }))});
    };
    const observer = new PerformanceObserver(list => {
      if (!state.stop) receive(list.getEntries());
    });
    observer.observe({type, buffered: true}); observers.push(observer);
    drainObservers.push(() => receive(observer.takeRecords()));
  }
  document.addEventListener('DOMContentLoaded', () => first('dom_content_loaded_observed_ms'));
  window.addEventListener('load', () => first('load_observed_ms'));
  const pending = () => {
    const root = document.documentElement;
    if (!root) return;
    if (root.hasAttribute('data-kpress-math-pending')) {
      state.pending_observed = true; first('pending_set_ms');
    } else if (state.pending_observed) first('pending_cleared_ms');
    if (root.classList.contains('math-ready')) first('math_ready_marker_ms');
  };
  let dirty = true;
  const mutations = new MutationObserver(() => { dirty = true; pending(); });
  mutations.observe(document, {subtree: true, childList: true, attributes: true,
    attributeFilter: ['data-kpress-math-pending', 'class', 'hidden']});
  const exposed = __EXPOSED__;
  const mathWrapper = '.katex,.kpress-math,.kpress-math-render,'
    + '.kpress-math-semantic,.tex,.tex-d';
  const normalized = text => (text || '').replace(/\s+/g, '').replace(/\\mkern1mu/g, '');
  const annotation = node => [...node.querySelectorAll(
    'annotation[encoding="application/x-tex"]')]
    .map(part => part.textContent.trim());
  const visibleMath = node => {
    const maths = [...node.querySelectorAll('.katex')];
    return maths.length > 0 && !node.querySelector('.katex-error') && maths.every(math => {
      // The publication's pending rule necessarily hides these targets. Avoid
      // forcing prepared-page layout merely to measure an invisible formula.
      // Eligible targets still undergo the same actual exposure checks below.
      if (!full && document.documentElement.hasAttribute('data-kpress-math-pending')) {
        const target = math.closest('.tex,.tex-d,[data-kpress-math-prepared="true"]');
        if (target && target.dataset.squaresMathReady !== 'true') return false;
      }
      const html = math.querySelector('.katex-html');
      return html && html.textContent.trim() && exposed(html) && annotation(math).every(Boolean)
        && annotation(math).length > 0;
    });
  };
  const active = node => !node.closest('.cert-figure[hidden]') && exposed(node);
  const slugOf = node => node.closest('.cert-figure')?.dataset.cert || null;
  const snapshot = () => {
    const viewport = document.querySelector('[data-kpress-viewport]')
      || document.scrollingElement;
    return {at_ms: clock(), width: innerWidth, height: innerHeight,
      scroll_x: viewport?.scrollLeft || 0, scroll_y: viewport?.scrollTop || 0,
      document_scroll_x: scrollX, document_scroll_y: scrollY,
      visibility: document.visibilityState, focused: document.hasFocus(), hash: location.hash,
      document_ready_state: document.readyState,
      math_ready: document.documentElement.classList.contains('math-ready'),
      certificate_elements: document.querySelectorAll('.cert-figure').length,
      active_certificates: [...new Set([...document.querySelectorAll('.cert-figure')]
        .filter(node => full ? active(node) : !node.closest('[hidden]'))
        .map(node => node.dataset.cert))]};
  };
  let prose = [], captions = [], parameters = [];
  const targetTimes = new WeakMap(), anchorNodes = new WeakMap(), tracked = [];
  const blockEdges = new WeakMap();
  const expectedLabels = ['\\varphi', 'K', '\\varphi', '\\theta', 'd', 'D', 'B',
    'B(\\cos d + \\sin d)'];
  function correctTarget(node, index) {
    if (!visibleMath(node)) return false;
    const texts = annotation(node);
    if (index < 8 && normalized(texts.join('')) !== normalized(expectedLabels[index])) {
      return false;
    }
    if (node.id.startsWith('s-phi-')) {
      const slider = document.getElementById(node.id.slice(2));
      if (!slider || normalized(texts[0]) !== normalized(
        (Number(slider.value) / 10).toFixed(3) + '^{\\circ}')) return false;
    }
    const containers = [node, ...node.querySelectorAll(mathWrapper)];
    return containers.every(container => {
      const request = sources.get(container);
      return !request || annotation(container)
        .some(text => normalized(text) === normalized(request.source));
    });
  }
  function discoverAnchors() {
    const blocks = document.querySelectorAll(
      '.kpress-prose p, .kpress-figcaption, figcaption, figure[data-figure="6"] .caps, '
      + 'figure[data-figure="6"] dt');
    for (const block of blocks) {
      const previous = blockEdges.get(block);
      if (previous && previous.last === block.lastChild
          && previous.count === block.childNodes.length) continue;
      if (!block.querySelector(mathWrapper) || !active(block)) continue;
      blockEdges.set(block, {last: block.lastChild, count: block.childNodes.length});
      const category = block.closest('.kpress-figcaption,figcaption') ? 'caption'
        : block.closest('figure[data-figure="6"]') ? 'parameter' : 'prose';
      const walker = document.createTreeWalker(block,
        NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT, {acceptNode(node) {
          // Reject whole math subtrees. Prepared markup must not cost the observer
          // a walk through thousands of glyph spans that the control lacks.
          if (node.nodeType === Node.ELEMENT_NODE) return node.matches(mathWrapper)
            ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_SKIP;
          return node.textContent.trim() ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
        }});
      const texts = [];
      while (walker.nextNode()) {
        const node = walker.currentNode;
        texts.push(node);
      }
      // At most four persistent characters per block. The outside edges detect
      // rewrapping without walking every KaTeX glyph on every frame.
      for (const text of new Set([texts[0], texts.at(-1)].filter(Boolean))) {
        if (anchorNodes.has(text)) continue;
        const value = text.textContent;
        const offsets = new Set([value.search(/\S/), value.search(/\s*$/) - 1]);
        const anchors = [];
        for (const offset of offsets) {
          if (offset < 0) continue;
          const range = document.createRange();
          range.setStart(text, offset); range.setEnd(text, offset + 1);
          const record = {id: `anchor-${tracked.length}`, category,
            text: value.trim().replace(/\s+/g, ' ').slice(0, 100), character: value[offset],
            offset, block: block.id || block.tagName.toLowerCase(), samples: 0,
            initial: null, final: null, max_absolute_px: 0, max_local_px: 0,
            max_start_x_px: 0, max_start_y_px: 0, max_bottom_px: 0};
          tracked.push({node: text, block, range, record}); anchors.push(record);
          state.anchors.push(record);
        }
        anchorNodes.set(text, anchors);
      }
    }
  }
  function discover() {
    if (full) {
      prose = [...document.querySelectorAll('.kpress-prose p')].filter(node =>
        !node.closest('.cert-figure,figcaption,.kpress-figcaption') && active(node));
      captions = [...document.querySelectorAll('.kpress-figcaption,figcaption')].filter(active);
    }
    const figure = [...document.querySelectorAll('figure[data-figure="6"]')]
      .find(node => full ? active(node) : !node.closest('[hidden]'));
    // Keep labels before readouts so the eight published label contracts are stable.
    parameters = figure ? [...figure.querySelectorAll('.panel .ctl .caps, .panel .kv dt'),
      ...figure.querySelectorAll('.panel .kv dd')] : [];
    if (full) discoverAnchors();
    dirty = false;
  }
  function sampleAnchors(at) {
    const blocks = new Map();
    for (const {node, block, range, record} of tracked) {
      if (!node.isConnected) continue;
      if (!blocks.has(block)) {
        blocks.set(block, active(block) ? block.getBoundingClientRect() : null);
      }
      const box = blocks.get(block);
      if (!box) continue;
      if (!node.parentElement.checkVisibility(
        {opacityProperty: true, visibilityProperty: true})) continue;
      const rect = range.getBoundingClientRect();
      if (rect.width <= 0 || rect.height <= 1) continue;
      const position = {at_ms: at, x: rect.x, y: rect.y, bottom: rect.bottom,
        local_x: rect.x - box.x, local_y: rect.y - box.y, local_bottom: rect.bottom - box.y};
      record.initial ||= position; record.final = position; record.samples++;
      record.bounds ||= {};
      for (const key of ['x', 'y', 'bottom', 'local_x', 'local_y', 'local_bottom']) {
        const bounds = record.bounds[key] ||= {min: position[key], max: position[key]};
        bounds.min = Math.min(bounds.min, position[key]);
        bounds.max = Math.max(bounds.max, position[key]);
      }
      const span = key => record.bounds[key].max - record.bounds[key].min;
      record.max_start_x_px = span('x'); record.max_start_y_px = span('y');
      record.max_bottom_px = span('bottom');
      record.max_absolute_px = Math.max(record.max_absolute_px, record.max_start_x_px,
        record.max_start_y_px, record.max_bottom_px);
      record.max_local_px = Math.max(span('local_x'), span('local_y'), span('local_bottom'));
      state.counters.anchor_samples++;
    }
  }
  function sample() {
    if (state.stop) return;
    const start = clock(); state.counters.frames++; first('first_frame_ms', start);
    pending(); if (dirty) discover();
    if (full) sampleAnchors(start);
    if (full && state.anchors.some(anchor => anchor.samples)) {
      first('first_anchor_frame_ms', start);
      const current = snapshot(), previous = state.snapshots.at(-1);
      const changed = !previous || Object.keys(current).some(key => key !== 'at_ms'
        && JSON.stringify(current[key]) !== JSON.stringify(previous[key]));
      if (changed) state.snapshots.push(current);
    }
    if (metrics.first_prose_math_ms == null && prose.some(visibleMath)) {
      first('first_prose_math_ms', start);
    }
    if (metrics.first_caption_math_ms == null && captions.some(visibleMath)) {
      first('first_caption_math_ms', start);
    }
    const ready = parameters.map((node, index) => {
      const correct = correctTarget(node, index);
      if (correct && !targetTimes.has(node)) targetTimes.set(node, start);
      return correct;
    });
    if (ready.some(Boolean)) first('first_parameter_math_ms', start);
    // Scroll offsets can flush layout too. In parameter mode take the first
    // state snapshot only after a target already required an exposure check.
    if (!full && ready.some(Boolean) && !state.snapshots.length) {
      state.snapshots.push(snapshot());
    }
    if (parameters.length === 14 && ready.every(Boolean)) first('parameters_ready_ms', start);
    else if (state.anchors.some(anchor => anchor.samples)) {
      state.pre_reveal_frame_observed = true;
    }
    const duration = clock() - start;
    metrics.sampler_total_ms = (metrics.sampler_total_ms || 0) + duration;
    metrics.sampler_max_ms = Math.max(metrics.sampler_max_ms || 0, duration);
    if (full || metrics.parameters_ready_ms == null) requestAnimationFrame(sample);
  }
  requestAnimationFrame(sample);
  state.finish = () => {
    const validationStart = clock();
    drainObservers.forEach(drain => drain());
    state.stop = true; pending(); mutations.disconnect();
    observers.forEach(observer => observer.disconnect());
    originals.forEach(restore => restore());
    // Parameter-mode sampling stopped at first readiness. Re-read final coverage
    // so a later addition, removal, or reclassification cannot evade validation.
    discover();
    state.snapshots.push(snapshot());
    first('observation_end_ms');
    state.targets = parameters.map((node, index) => ({
      id: node.id || `figure6-${slugOf(node)}-label-${index}`, slug: slugOf(node),
      source: annotation(node), first_visible_ms: targetTimes.get(node) ?? null,
      correct: correctTarget(node, index), exposed: active(node),
      in_viewport: node.getBoundingClientRect().top < innerHeight
        && node.getBoundingClientRect().bottom > 0,
    }));
    const nav = performance.getEntriesByType('navigation')[0];
    if (nav) for (const [metric, key] of Object.entries({response_start_ms: 'responseStart',
      response_end_ms: 'responseEnd', dom_interactive_ms: 'domInteractive',
      dom_content_loaded_ms: 'domContentLoadedEventEnd', load_event_ms: 'loadEventEnd'})) {
      metrics[metric] = nav[key] || null;
    }
    const paints = performance.getEntriesByType('paint');
    for (const entry of paints) {
      metrics[entry.name.replaceAll('-', '_') + '_ms'] = entry.startTime;
    }
    metrics.initial_ready_end_ms = state.ready[0]?.end_ms ?? null;
    metrics.initial_ready_wait_ms = state.ready[0]?.end_ms != null
      ? state.ready[0].end_ms - state.ready[0].start_ms : null;
    metrics.last_font_end_ms = state.fonts
      .reduce((max, entry) => Math.max(max, entry.end_ms || 0), 0) || null;
    metrics.katex_total_ms = state.katex.reduce((sum, entry) => sum + entry.duration_ms, 0);
    metrics.katex_max_ms = Math.max(0, ...state.katex.map(entry => entry.duration_ms));
    metrics.first_katex_call_ms = state.katex[0]?.start_ms ?? null;
    metrics.last_katex_end_ms = state.katex.length
      ? Math.max(...state.katex.map(entry => entry.start_ms + entry.duration_ms)) : null;
    metrics.first_render_call_ms = state.renders[0]?.start_ms ?? null;
    metrics.last_render_end_ms = state.renders.length
      ? Math.max(...state.renders.map(entry => entry.end_ms || 0)) || null : null;
    metrics.first_hydrate_call_ms = state.hydrates[0]?.start_ms ?? null;
    metrics.last_hydrate_end_ms = state.hydrates.length
      ? Math.max(...state.hydrates.map(entry => entry.end_ms || 0)) || null : null;
    metrics.post_ready_to_first_katex_ms = metrics.first_katex_call_ms != null
      && metrics.initial_ready_end_ms != null
      ? metrics.first_katex_call_ms - metrics.initial_ready_end_ms : null;
    metrics.longtask_total_ms = state.capabilities.longtask
      ? state.longtasks.reduce((sum, entry) => sum + entry.duration_ms, 0) : null;
    metrics.layout_shift_score = state.capabilities.layout_shift
      ? state.shifts.filter(entry => !entry.had_recent_input)
        .reduce((sum, entry) => sum + entry.value, 0) : null;
    const anchorMax = key => Math.max(0, ...state.anchors.map(anchor => anchor[key]));
    metrics.anchor_max_displacement_px = anchorMax('max_absolute_px');
    metrics.anchor_max_local_displacement_px = anchorMax('max_local_px');
    metrics.anchor_max_start_x_px = anchorMax('max_start_x_px');
    metrics.anchor_max_start_y_px = anchorMax('max_start_y_px');
    metrics.anchor_max_bottom_px = anchorMax('max_bottom_px');
    if (!full) for (const name of ['anchor_max_displacement_px',
      'anchor_max_local_displacement_px', 'anchor_max_start_x_px',
      'anchor_max_start_y_px', 'anchor_max_bottom_px']) metrics[name] = null;
    state.source = {url: location.href, title: document.title,
      revision_url: document.querySelector(
        'a[href*="github.com/jlevy/squares/blob/"]')?.href || null};
    metrics.finish_validation_ms = clock() - validationStart;
    return {...state, finish: undefined};
  };
})();
""".replace("__EXPOSED__", EXPOSED)

STARTUP_SCRIPT = _STARTUP_SCRIPT.replace("__MODE__", "full")


def startup_findings(report: JsonRecord, *, width: int, height: int) -> list[str]:
    """Reject incomplete measurements; speed and movement need a separate criterion."""
    findings: list[str] = []
    mode = report.get("mode", "full")
    if mode not in ("full", "parameters"):
        findings.append(f"unknown startup measurement mode: {mode}")
    full = mode != "parameters"
    counters = report.get("counters", {})
    for name, minimum in {
        "frames": 1,
        "font_hooks": 2,
        "katex_hooks": 1,
        "runtime_hooks": 2,
        **({"anchor_samples": 1} if full else {}),
    }.items():
        if counters.get(name, 0) < minimum:
            findings.append(f"missing instrumentation: {name}")
    if counters.get("render_calls", 0) + counters.get("hydrate_calls", 0) == 0:
        findings.append("no observed math rendering or hydration activity")
    metrics = report.get("metrics", {})
    milestones = [
        "instrumentation_installed_ms",
        "parameters_ready_ms",
        "math_ready_marker_ms",
    ]
    if full:
        milestones.extend(("first_prose_math_ms", "first_caption_math_ms"))
    for name in milestones:
        value = metrics.get(name)
        if not isinstance(value, (int, float)) or not math.isfinite(value):
            findings.append(f"missing startup milestone: {name}")
    targets = report.get("targets", [])
    if len(targets) != EXPECTED_PARAMETERS:
        findings.append(
            f"expected {EXPECTED_PARAMETERS} active parameter targets, found {len(targets)}"
        )
    findings.extend(
        f"missing, hidden, or incorrect parameter math: {target.get('id')}"
        for target in targets
        if not target.get("correct") or not target.get("exposed")
    )
    anchors = report.get("anchors", [])
    findings.extend(
        f"no readable neighboring text anchors: {category}"
        for category in (("prose", "caption", "parameter") if full else ())
        if not any(
            anchor.get("category") == category and anchor.get("samples", 0)
            for anchor in anchors
        )
    )
    snapshots = report.get("snapshots", [])
    if len(snapshots) < 2:
        findings.append("missing initial or final viewport state")
    for index, snapshot in enumerate(snapshots):
        if snapshot.get("width") != width or snapshot.get("height") != height:
            findings.append("viewport dimensions changed during startup")
        if snapshot.get("visibility") != "visible" or not snapshot.get("focused"):
            findings.append("page was not visible and focused during startup")
        initializing = (
            index < len(snapshots) - 1
            and not snapshot.get("math_ready")
            and not snapshot.get("active_certificates")
        )
        if not initializing and len(snapshot.get("active_certificates", [])) != 1:
            findings.append("expected exactly one active certificate")
    if snapshots:
        findings.extend(
            f"startup changed viewport state: {key}"
            for key in (
                "scroll_x",
                "scroll_y",
                "document_scroll_x",
                "document_scroll_y",
            )
            if any(snapshot.get(key) != snapshots[0].get(key) for snapshot in snapshots[1:])
        )
        certificates = [
            snapshot["active_certificates"]
            for snapshot in snapshots
            if snapshot.get("active_certificates")
        ]
        if certificates and any(value != certificates[0] for value in certificates[1:]):
            findings.append("startup changed viewport state: active_certificates")
    findings.extend(f"page error: {error}" for error in report.get("errors", []))
    return findings


def measure_startup(
    path: Path | str = PAGE,
    *,
    width: int = 1280,
    height: int = 720,
    browser_name: BrowserName = "chromium",
    mode: MeasurementMode = "full",
    timeout_ms: int = 60_000,
) -> JsonRecord:
    """Observe one untouched navigation in a fresh browser process and context."""
    from playwright.sync_api import TimeoutError as PlaywrightTimeoutError  # noqa: PLC0415
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    with sync_playwright() as driver:
        override = os.environ.get(BROWSER_OVERRIDE) if browser_name == "chromium" else None
        browser = getattr(driver, browser_name).launch(executable_path=override)
        try:
            page = browser.new_page(viewport={"width": width, "height": height})
            page.set_default_timeout(timeout_ms)
            errors: list[str] = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.add_init_script(_STARTUP_SCRIPT.replace("__MODE__", mode))
            timeout: str | None = None
            try:
                page.goto(page_url(path), wait_until="domcontentloaded")
                page.wait_for_selector(READY)
                # Evaluate does not honor Playwright's default timeout. Start the
                # real settlement promise without awaiting it in that call, then
                # use the bounded wait API so broken pages still retain a report.
                page.evaluate(
                    "() => { const state = globalThis.__mathStartup;"
                    " state.settlement_state = 'pending';"
                    f" ({SETTLED})().then(() => {{ state.settlement_state = 'resolved'; }},"
                    " error => { state.errors.push(String(error));"
                    " state.settlement_state = 'rejected'; }); }"
                )
                page.wait_for_function(
                    "globalThis.__mathStartup.settlement_state !== 'pending'"
                )
            except PlaywrightTimeoutError as error:
                timeout = str(error).splitlines()[0]
            report: JsonRecord = page.evaluate("() => globalThis.__mathStartup.finish()")
            report["errors"].extend(errors)
            report["environment"] = {
                "browser": browser_name,
                "browser_version": browser.version,
                "browser_cache": "cold: fresh process and context per load",
                "os_cache": "uncontrolled: file and font caches may be warm",
                "headless": True,
                "viewport": {"width": width, "height": height},
                "recorded_at": datetime.now(UTC).isoformat(),
            }
            report["requested_source"] = str(path)
            report["findings"] = startup_findings(report, width=width, height=height)
            if timeout:
                report["findings"].append(f"startup did not settle: {timeout}")
            return report
        finally:
            browser.close()


def summarize(runs: Sequence[JsonRecord]) -> JsonRecord:
    """Keep missing observations absent from statistics, never turn them into zeros."""
    names = sorted({name for run in runs for name in run.get("metrics", {})})
    summary: JsonRecord = {}
    for name in names:
        values = [
            value
            for run in runs
            if isinstance(value := run.get("metrics", {}).get(name), (int, float))
            and math.isfinite(value)
        ]
        summary[name] = {
            "count": len(values),
            "missing": len(runs) - len(values),
            "median": statistics.median(values) if values else None,
            "min": min(values) if values else None,
            "max": max(values) if values else None,
        }
    return summary


def instrument_provenance(runs: Sequence[JsonRecord]) -> JsonRecord:
    """Record the executing tool's provenance directly from Git and the process."""
    repo = Path(__file__).resolve().parents[2]

    def git(*args: str) -> str:
        return subprocess.run(
            ["git", *args], cwd=repo, check=True, capture_output=True, text=True
        ).stdout.strip()

    return {
        "git_head": git("rev-parse", "HEAD"),
        "git_dirty": bool(git("status", "--porcelain")),
        "entry_point": "devtools.check_math_startup",
        "argv": sys.orig_argv,
        "platform": platform.platform(),
        "python": sys.version,
        "python_executable": sys.executable,
        "browser_versions": sorted(
            {
                f"{run['environment']['browser']} {run['environment']['browser_version']}"
                for run in runs
                if "environment" in run
            }
        ),
    }


def run_measurements(
    sources: Mapping[str, Path | str],
    *,
    runs: int = 3,
    width: int = 1280,
    height: int = 720,
    browser_name: BrowserName = "chromium",
    mode: MeasurementMode = "full",
) -> JsonRecord:
    """Measure matched pairs sequentially, reversing their order on alternate pairs."""
    observations: list[JsonRecord] = []
    for pair in range(runs):
        order = list(sources.items())
        if pair % 2:
            order.reverse()
        for label, path in order:
            report = measure_startup(
                path, width=width, height=height, browser_name=browser_name, mode=mode
            )
            observations.append({"pair": pair + 1, "label": label, **report})
    return {
        "schema_version": 1,
        "measurement": "natural-math-startup",
        "mode": mode,
        "instrument": instrument_provenance(observations),
        "performance_verdict": "not evaluated; acceptance criterion belongs to the experiment",
        "runs": observations,
        "summary": {
            label: summarize([run for run in observations if run["label"] == label])
            for label in sources
        },
        "findings": [
            f"{run['label']} pair {run['pair']}: {finding}"
            for run in observations
            for finding in run["findings"]
        ],
    }


def browser_fixture(mode: str) -> str:
    """A real layout with the same public API and Figure 6 output contract.

    Only the fixtures introduce delays or changed widths. Normal measurements never
    alter page behavior. These small controls isolate the observer from publication
    changes and do not need external fonts, images, or a generated site artifact.
    """
    return r"""<!doctype html>
<html><head><meta charset="utf-8"><title>Math startup observer control</title>
<style>
body {font:16px serif; margin:20px}
.kpress-prose {width:600px; max-width:90vw}
.katex-mathml {position:absolute; width:1px; height:1px; overflow:hidden; clip-path:inset(50%)}
html[data-kpress-math-pending] .tex {visibility:hidden}
dt, dd {height:24px; margin:0} dt {float:left; width:240px} dd {width:480px}
.shift .tex {display:inline-block; width:20px}
</style>
<script>document.documentElement.dataset.kpressMathPending = 'true';</script>
</head><body>
<main class="kpress-prose" data-kpress-viewport>
<p id="prose" class="shift">Before <span class="tex">x</span> after the formula.</p>
<div class="cert-figure" data-cert="test">
<figure data-figure="6"><div class="panel">
<div class="ctl"><span class="caps">Angle <span class="tex">\varphi</span></span>
<input id="phi-test" type="range" min="0" max="450" value="196"></div>
<div class="ctl"><span class="caps">Net <span class="tex">K</span></span></div>
<dl class="kv">
<dt><span class="tex">\varphi</span></dt><dd id="s-phi-test"></dd>
<dt>nearest <span class="tex">\theta</span></dt><dd id="s-theta-test"></dd>
<dt>mismatch <span class="tex">d</span></dt><dd id="s-d-test"></dd>
<dt>largest <span class="tex">D</span></dt><dd id="s-D-test"></dd>
<dt><span class="tex">B</span> admitted</dt><dd id="s-B-test"></dd>
<dt><span class="tex">B(\cos d + \sin d)</span></dt><dd id="s-prod-test"></dd>
</dl></div>
<figcaption class="kpress-figcaption">Caption before
<span class="tex">x</span> after math.</figcaption>
</figure></div></main>
<script>
const mode = '__MODE__';
if (mode === 'missing-anchors') {
  const paragraph = document.getElementById('prose');
  paragraph.replaceChildren(paragraph.querySelector('.tex'));
}
if (mode === 'missing-counters') globalThis.__mathStartup.counters.font_hooks = 0;
globalThis.katex = {render(source, node) {
  const katex = document.createElement('span'); katex.className = 'katex';
  const hidden = document.createElement('span'); hidden.className = 'katex-mathml';
  const annotation = document.createElement('annotation');
  annotation.setAttribute('encoding', 'application/x-tex'); annotation.textContent = source;
  hidden.append(annotation); katex.append(hidden);
  const html = document.createElement('span'); html.className = 'katex-html';
  html.textContent = source; katex.append(html); node.replaceChildren(katex);
}};
const gate = mode === 'delayed' || mode === 'width-change'
  ? new Promise(resolve => setTimeout(resolve, 300)) : Promise.resolve();
globalThis.kpressMathText = {
  ready() { return gate; },
  render(source, node) { katex.render(source, node); return Promise.resolve(); },
  complete() { delete document.documentElement.dataset.kpressMathPending; }
};
const ready = mode === 'no-warmup' ? gate : kpressMathText.ready();
let releaseLateTarget;
const lateTarget = mode === 'late-target'
  ? new Promise(resolve => { releaseLateTarget = resolve; }) : Promise.resolve();
globalThis.squaresMath = {ready, settled: () => lateTarget};
document.fonts.load('16px serif');
ready.then(async () => {
  for (const node of document.querySelectorAll('.tex')) {
    await kpressMathText.render(node.textContent, node);
  }
  for (const [key, source] of Object.entries({phi: '19.600^{\\circ}', theta: '15.000^{\\circ}',
    d: '4.600^{\\circ}', D: '0.1', B: '0.9', prod: '0.97'})) {
    if (mode === 'missing-math' && key === 'phi') continue;
    await kpressMathText.render(source, document.getElementById(`s-${key}-test`));
  }
  if (mode === 'width-change') document.querySelector('.shift .tex').style.width = '180px';
  kpressMathText.complete(); document.documentElement.classList.add('math-ready');
  if (mode === 'late-target') {
    const addAfterFirstReadiness = () => {
      if (globalThis.__mathStartup.metrics.parameters_ready_ms == null) {
        requestAnimationFrame(addAfterFirstReadiness); return;
      }
      const extra = document.createElement('dd'); extra.id = 'late-target';
      document.querySelector('.panel .kv').append(extra);
      kpressMathText.render('0', extra).then(releaseLateTarget);
    };
    requestAnimationFrame(addAfterFirstReadiness);
  }
});
</script></body></html>""".replace("__MODE__", mode)


def self_test(
    *, browser_name: BrowserName = "chromium", mode: MeasurementMode = "full"
) -> JsonRecord:
    """Run real positive and negative pages; a fast pytest run does not need a browser."""
    observations: JsonRecord = {}
    findings: list[str] = []
    with TemporaryDirectory(prefix="math-startup-controls-") as directory:
        controls = (
            "control",
            "no-warmup",
            "delayed",
            "missing-math",
            "missing-counters",
            "late-target",
            *(("width-change", "missing-anchors") if mode == "full" else ()),
        )
        for control in controls:
            path = Path(directory) / f"{control}.html"
            path.write_text(browser_fixture(control))
            observations[control] = measure_startup(
                path, browser_name=browser_name, mode=mode, timeout_ms=5_000
            )
    for control in (
        "control",
        "no-warmup",
        "delayed",
        *(("width-change",) if mode == "full" else ()),
    ):
        findings.extend(
            f"{control}: {message}" for message in observations[control]["findings"]
        )
    if observations["no-warmup"]["counters"]["ready_calls"] != 0:
        findings.append("the no-warmup control unexpectedly called the warmup API")
    for control, run in observations.items():
        duration = run["metrics"].get("finish_validation_ms")
        if (
            not isinstance(duration, (int, float))
            or not math.isfinite(duration)
            or duration < 0
        ):
            findings.append(f"{control}: missing final-validation cost")
    baseline = observations["control"]["metrics"]
    delayed = observations["delayed"]["metrics"]
    if delayed.get("parameters_ready_ms", 0) - baseline.get("parameters_ready_ms", 0) < 150:
        findings.append("the delayed control did not record the known 300 ms delay")
    if mode == "full":
        changed = observations["width-change"]
        if baseline.get("anchor_max_displacement_px", math.inf) > 0.1:
            findings.append("the stable control reported neighboring text movement")
        if changed["metrics"].get("anchor_max_local_displacement_px", 0) < 100:
            findings.append("the width-change control did not detect adjacent text movement")
        if not changed.get("pre_reveal_frame_observed"):
            findings.append("the width-change control missed the readable pre-reveal frame")
    elif any(run["counters"]["anchor_samples"] for run in observations.values()):
        findings.append("parameter mode unexpectedly sampled all-page text anchors")
    for control, required in {
        "missing-math": "incorrect parameter math",
        "missing-counters": "missing instrumentation: font_hooks",
        "late-target": "expected 14 active parameter targets, found 15",
        **({"missing-anchors": "neighboring text anchors: prose"} if mode == "full" else {}),
    }.items():
        if not any(required in message for message in observations[control]["findings"]):
            findings.append(f"{control}: the negative control was not rejected")
    return {
        "schema_version": 1,
        "mode": mode,
        "instrument": instrument_provenance(list(observations.values())),
        "self_test": observations,
        "findings": findings,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("page", nargs="?", help="Local HTML or HTTP(S) URL")
    parser.add_argument("--control", help="Frozen control HTML or URL")
    parser.add_argument("--candidate", help="Candidate HTML or URL")
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=720)
    parser.add_argument(
        "--browser", choices=("chromium", "firefox", "webkit"), default="chromium"
    )
    parser.add_argument("--mode", choices=("full", "parameters"), default="full")
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--self-test", action="store_true", help="Exercise retained browser controls"
    )
    args = parser.parse_args(argv)
    if args.runs < 1 or args.width < 1 or args.height < 1:
        parser.error("runs and viewport dimensions must be positive")
    if bool(args.control) != bool(args.candidate) or (args.page and args.control):
        parser.error("use a page, or both --control and --candidate")
    report = (
        self_test(browser_name=args.browser, mode=args.mode)
        if args.self_test
        else run_measurements(
            {"control": args.control, "candidate": args.candidate}
            if args.control
            else {"page": args.page or PAGE},
            runs=args.runs,
            width=args.width,
            height=args.height,
            browser_name=args.browser,
            mode=args.mode,
        )
    )
    encoded = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded)
        print(f"Wrote {args.output}")
    else:
        print(encoded, end="")
    for finding in report["findings"]:
        print(f"FAIL: {finding}")
    return int(bool(report["findings"]))


if __name__ == "__main__":
    raise SystemExit(main())
