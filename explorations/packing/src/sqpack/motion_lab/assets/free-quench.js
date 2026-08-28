(() => {
  "use strict";

  const editor = globalThis.MotionLabEditor;
  if (!editor) throw new Error("Motion Lab editor model is unavailable");
  const byId = (id) => document.getElementById(id);
  const svgNamespace = "http://www.w3.org/2000/svg";
  const stageSize = 620;
  const plotLeft = 49;
  const plotBottom = 571;
  const plotExtent = 522;
  const rotationStep = Math.PI / 12;
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const stage = byId("free-stage");
  const mathPlane = byId("free-math-plane");
  const container = byId("free-container");
  const acceptedLayer = byId("accepted-layer");
  const probeLayer = byId("probe-layer");
  const labelLayer = byId("free-label-layer");
  const liveRegion = byId("live-region");
  const scenarioSelect = byId("scenario-select");
  const nInput = byId("n-input");
  const sideInput = byId("side-input");
  const seedInput = byId("seed-input");
  const snappingToggle = byId("snapping-toggle");
  const rotateLeftButton = byId("rotate-left-button");
  const rotateRightButton = byId("rotate-right-button");
  const runButton = byId("run-button");
  const downloadButton = byId("download-button");
  const timelinePanel = byId("timeline-panel");
  const timelineInput = byId("timeline-input");
  const timelineList = byId("timeline-list");
  const playTraceButton = byId("play-trace-button");

  let scenario = JSON.parse(byId("free-scenario").textContent);
  let baseline = editor.stateFromScenario(scenario);
  let state = editor.copyState(baseline);
  let selectedId = null;
  let drag = null;
  let trace = null;
  let traceText = "";
  let traceName = "";
  let eventIndex = 0;
  let displayedFrame = null;
  let playbackTimer = null;
  let tweenFrame = null;
  let playbackIndices = [];
  let editing = true;

  function announce(message) {
    liveRegion.textContent = message;
  }

  function svgElement(name) {
    return document.createElementNS(svgNamespace, name);
  }

  const paletteSize = Number(document.documentElement.dataset.paletteSize);
  if (!Number.isInteger(paletteSize) || paletteSize < 1) {
    throw new Error("Motion Lab palette size is missing from the document");
  }

  function palette(index) {
    return `var(--square-${String(index % paletteSize).padStart(2, "0")})`;
  }

  function scaleFor(side) {
    return plotExtent / side;
  }

  function frameFromState(value) {
    return {
      container_side: value.side,
      squares: value.squares.map((square) => ({
        ...square,
        palette_index: square.square_id,
      })),
    };
  }

  function setPlane(side) {
    const scale = scaleFor(side);
    mathPlane.setAttribute(
      "transform",
      `translate(${plotLeft} ${plotBottom}) scale(${scale} ${-scale})`,
    );
    container.setAttribute("width", side);
    container.setAttribute("height", side);
    return scale;
  }

  function groupMap(layer) {
    return new Map([...layer.children].map((element) => [
      Number(element.getAttribute("data-square-id")),
      element,
    ]));
  }

  function syncSquareLayer(layer, squares, {probe = false, diagnostics = null} = {}) {
    const existing = groupMap(layer);
    const retained = new Set();
    const selectedGroup = selectedId === null || !editing
      ? []
      : editor.groupFor(state, selectedId);
    for (const square of squares) {
      let glyph = existing.get(square.square_id);
      if (!glyph) {
        glyph = svgElement("g");
        glyph.setAttribute("data-square-id", square.square_id);
        const rectangle = svgElement("rect");
        rectangle.setAttribute("x", "-.5");
        rectangle.setAttribute("y", "-.5");
        rectangle.setAttribute("width", "1");
        rectangle.setAttribute("height", "1");
        glyph.append(rectangle);
        layer.append(glyph);
      }
      retained.add(square.square_id);
      glyph.setAttribute(
        "transform",
        `translate(${square.x} ${square.y}) rotate(${square.theta * 180 / Math.PI})`,
      );
      const rectangle = glyph.firstElementChild;
      if (probe) {
        const rejected = stage.dataset.probeOutcome === "rejected";
        rectangle.setAttribute("class", `probe-square${rejected ? " rejected" : ""}`);
        rectangle.removeAttribute("style");
        glyph.removeAttribute("tabindex");
        glyph.removeAttribute("role");
        glyph.removeAttribute("aria-label");
      } else {
        const classes = ["editor-square"];
        if (editing && selectedId === square.square_id) classes.push("selected");
        else if (editing && selectedGroup.includes(square.square_id)) classes.push("group-member");
        if (diagnostics?.overlapIds.has(square.square_id)) classes.push("overlap");
        if (diagnostics?.outsideIds.has(square.square_id)) classes.push("outside");
        rectangle.setAttribute("class", classes.join(" "));
        rectangle.setAttribute("style", `fill: ${palette(square.palette_index)}`);
        if (editing) {
          glyph.setAttribute("tabindex", "0");
          glyph.setAttribute("role", "button");
          glyph.setAttribute(
            "aria-label",
            `Square ${square.square_id}; select or drag its temporary chunk`,
          );
        } else {
          glyph.removeAttribute("tabindex");
          glyph.removeAttribute("role");
          glyph.removeAttribute("aria-label");
        }
      }
    }
    for (const [squareId, glyph] of existing) {
      if (!retained.has(squareId)) glyph.remove();
    }
  }

  function syncLabels(squares, side) {
    const existing = new Map([...labelLayer.children].map((element) => [
      Number(element.getAttribute("data-square-id")),
      element,
    ]));
    const retained = new Set();
    const scale = scaleFor(side);
    for (const square of squares) {
      let label = existing.get(square.square_id);
      if (!label) {
        label = svgElement("text");
        label.setAttribute("class", "free-square-label");
        label.setAttribute("data-square-id", square.square_id);
        label.textContent = square.square_id;
        labelLayer.append(label);
      }
      retained.add(square.square_id);
      label.setAttribute("x", plotLeft + scale * square.x);
      label.setAttribute("y", plotBottom - scale * square.y + 4);
    }
    for (const [squareId, label] of existing) {
      if (!retained.has(squareId)) label.remove();
    }
  }

  function diagnosticSets(value) {
    const result = editor.editorDiagnostics(value);
    return {
      result,
      overlapIds: new Set(result.overlap_pairs.flat()),
      outsideIds: new Set(result.outside_square_ids),
    };
  }

  function updateSetupReadout(diagnostics) {
    const groupCount = state.groups.length;
    byId("groups-value").textContent = `${groupCount} ${groupCount === 1 ? "chunk" : "chunks"}`;
    const issues = [];
    if (diagnostics.result.overlap_pairs.length) {
      issues.push(`${diagnostics.result.overlap_pairs.length} overlapping pair(s)`);
    }
    if (diagnostics.result.outside_square_ids.length) {
      issues.push(`${diagnostics.result.outside_square_ids.length} square(s) outside`);
    }
    byId("diagnostics-value").textContent = issues.length ? issues.join("; ") : "No visible defects";
    if (selectedId === null) {
      byId("selection-value").textContent = "No chunk selected";
    } else {
      const group = editor.groupFor(state, selectedId);
      byId("selection-value").textContent = `Selected chunk: ${group.join(", ")}`;
    }
    rotateLeftButton.disabled = selectedId === null;
    rotateRightButton.disabled = selectedId === null;
  }

  function setPhase(phase, outcome = null) {
    stage.setAttribute("class", `phase-${phase}`);
    stage.dataset.probeOutcome = outcome || "";
    const presentation = editor.phasePresentation({phase, outcome});
    const badge = byId("phase-badge");
    badge.textContent = presentation.label;
    badge.setAttribute("class", `phase-badge phase-${presentation.variant}`);
    return presentation;
  }

  function renderSetup() {
    editing = true;
    const diagnostics = diagnosticSets(state);
    const frame = frameFromState(state);
    setPlane(frame.container_side);
    setPhase("setup");
    syncSquareLayer(acceptedLayer, frame.squares, {diagnostics});
    syncSquareLayer(probeLayer, [], {probe: true});
    syncLabels(frame.squares, frame.container_side);
    displayedFrame = frame;
    byId("run-readout-title").textContent = "Setup";
    byId("mode-value").textContent = "Editable setup";
    byId("event-value").textContent = "No numerical event selected.";
    byId("counters-value").textContent = "—";
    byId("evidence-value").textContent = scenario.initial_frame.evidence.claim;
    updateSetupReadout(diagnostics);
  }

  function pointInMath(event, side = state.side) {
    const bounds = stage.getBoundingClientRect();
    const screenX = (event.clientX - bounds.left) * stageSize / bounds.width;
    const screenY = (event.clientY - bounds.top) * stageSize / bounds.height;
    const scale = scaleFor(side);
    return {x: (screenX - plotLeft) / scale, y: (plotBottom - screenY) / scale};
  }

  function squareTarget(event) {
    if (!(event.target instanceof Element)) return null;
    const glyph = event.target.closest("[data-square-id]");
    return glyph ? Number(glyph.getAttribute("data-square-id")) : null;
  }

  function selectedPivot(value, squareId) {
    const group = new Set(editor.groupFor(value, squareId));
    const members = value.squares.filter((square) => group.has(square.square_id));
    return {
      x: members.reduce((sum, square) => sum + square.x, 0) / members.length,
      y: members.reduce((sum, square) => sum + square.y, 0) / members.length,
    };
  }

  stage.addEventListener("pointerdown", (event) => {
    if (!editing) return;
    const squareId = squareTarget(event);
    if (squareId === null) return;
    selectedId = squareId;
    const start = pointInMath(event);
    const pivot = selectedPivot(state, squareId);
    drag = {
      pointerId: event.pointerId,
      squareId,
      baseline: editor.copyState(state),
      start,
      pivot,
      rotating: event.shiftKey,
      startAngle: Math.atan2(start.y - pivot.y, start.x - pivot.x),
      moved: false,
    };
    stage.setPointerCapture(event.pointerId);
    renderSetup();
    event.preventDefault();
  });

  stage.addEventListener("pointermove", (event) => {
    if (!drag || drag.pointerId !== event.pointerId) return;
    const point = pointInMath(event, drag.baseline.side);
    const distance = Math.hypot(point.x - drag.start.x, point.y - drag.start.y);
    drag.moved ||= distance > 0.01;
    if (drag.rotating) {
      const angle = Math.atan2(point.y - drag.pivot.y, point.x - drag.pivot.x);
      state = editor.rotateGroup(drag.baseline, drag.squareId, angle - drag.startAngle);
    } else {
      state = editor.translateGroup(
        drag.baseline,
        drag.squareId,
        point.x - drag.start.x,
        point.y - drag.start.y,
      );
    }
    renderSetup();
  });

  function finishPointer(event, cancelled) {
    if (!drag || drag.pointerId !== event.pointerId) return;
    if (cancelled) {
      state = drag.baseline;
      announce("Pointer edit cancelled.");
    } else if (drag.rotating && !drag.moved) {
      state = editor.rotateGroup(state, drag.squareId, rotationStep);
      announce("Selected chunk rotated 15 degrees.");
    } else if (!drag.rotating) {
      const threshold = 14 / scaleFor(state.side);
      const snapped = editor.applyBestSnap(state, drag.squareId, threshold);
      state = snapped.state;
      if (snapped.result) {
        const target = snapped.result.target_kind === "wall"
          ? `${snapped.result.target_id} wall`
          : `square ${snapped.result.target_id}`;
        announce(`Temporary chunk snapped to ${target}.`);
      }
    }
    if (stage.hasPointerCapture(event.pointerId)) stage.releasePointerCapture(event.pointerId);
    drag = null;
    renderSetup();
  }

  stage.addEventListener("pointerup", (event) => finishPointer(event, false));
  stage.addEventListener("pointercancel", (event) => finishPointer(event, true));

  stage.addEventListener("keydown", (event) => {
    if (!editing) return;
    const targetId = squareTarget(event);
    if (targetId !== null) selectedId = targetId;
    if (selectedId === null) return;
    const amount = event.shiftKey ? 0.2 : 0.05;
    const translations = {
      ArrowLeft: [-amount, 0],
      ArrowRight: [amount, 0],
      ArrowDown: [0, -amount],
      ArrowUp: [0, amount],
    };
    if (translations[event.key]) {
      state = editor.translateGroup(state, selectedId, ...translations[event.key]);
      const snapped = editor.applyBestSnap(state, selectedId, 14 / scaleFor(state.side));
      state = snapped.state;
    } else if (event.key.toLowerCase() === "q") {
      state = editor.rotateGroup(state, selectedId, -rotationStep);
    } else if (event.key.toLowerCase() === "e") {
      state = editor.rotateGroup(state, selectedId, rotationStep);
    } else if (event.key === "Escape") {
      selectedId = null;
    } else {
      return;
    }
    event.preventDefault();
    renderSetup();
  });

  function rotateSelected(delta) {
    if (selectedId === null) return;
    state = editor.rotateGroup(state, selectedId, delta);
    renderSetup();
    announce(`Selected chunk rotated ${Math.round(Math.abs(delta * 180 / Math.PI))} degrees.`);
  }

  rotateLeftButton.addEventListener("click", () => rotateSelected(-rotationStep));
  rotateRightButton.addEventListener("click", () => rotateSelected(rotationStep));

  snappingToggle.addEventListener("change", () => {
    state = editor.setSnapping(state, snappingToggle.checked);
    announce(snappingToggle.checked ? "Sticky setup enabled." : "Sticky setup disabled.");
  });

  function stopPlayback() {
    if (playbackTimer !== null) window.clearTimeout(playbackTimer);
    if (tweenFrame !== null) cancelAnimationFrame(tweenFrame);
    playbackTimer = null;
    tweenFrame = null;
    playTraceButton.textContent = "Play";
  }

  function clearTraceView() {
    stopPlayback();
    trace = null;
    traceText = "";
    traceName = "";
    eventIndex = 0;
    playbackIndices = [];
    timelinePanel.hidden = true;
    downloadButton.disabled = true;
  }

  function adoptScenario(nextScenario) {
    const keepSnapping = snappingToggle.checked;
    scenario = nextScenario;
    baseline = editor.setSnapping(editor.stateFromScenario(scenario), keepSnapping);
    state = editor.copyState(baseline);
    selectedId = null;
    clearTraceView();
    renderSetup();
  }

  async function loadScenario() {
    const n = Number(nInput.value);
    const side = Number(sideInput.value);
    const seed = Number(seedInput.value);
    const query = new URLSearchParams({n: String(n), side: String(side), seed: String(seed)});
    const response = await fetch(`/api/scenario/free-quench?${query}`);
    const body = await response.json();
    if (!response.ok) throw new Error(body.error?.message || "scenario request failed");
    adoptScenario(body);
    announce(`Loaded deterministic setup for ${n} squares with seed ${seed}.`);
  }

  byId("new-pose-button").addEventListener("click", async () => {
    seedInput.value = String(Number(seedInput.value) + 1);
    try {
      await loadScenario();
    } catch (error) {
      announce(`Could not load setup: ${error.message}`);
    }
  });

  byId("randomize-all-button").addEventListener("click", async () => {
    const seed = Number(seedInput.value) + 1;
    const magnitude = Math.abs(Math.trunc(seed));
    const n = 3 + (magnitude * 17 + 5) % 9;
    const side = Math.sqrt(n) + 0.35 + ((magnitude * 7919) % 70) / 100;
    seedInput.value = String(seed);
    nInput.value = String(n);
    sideInput.value = side.toFixed(2);
    try {
      await loadScenario();
    } catch (error) {
      announce(`Could not load setup: ${error.message}`);
    }
  });

  byId("reset-button").addEventListener("click", () => {
    state = editor.copyState(baseline);
    selectedId = null;
    snappingToggle.checked = state.snapping_enabled;
    renderSetup();
    announce("Setup returned to its seeded baseline.");
  });

  scenarioSelect.addEventListener("change", () => {
    if (scenarioSelect.value === "exact-n5") window.location.assign("/exact-n5");
  });

  function acceptedFrameBefore(index) {
    for (let current = index - 1; current >= 0; current -= 1) {
      if (trace.events[current].phase !== "angular-probe") return trace.events[current].frame;
    }
    return trace.events[0].frame;
  }

  function renderFrame(frame, phase, outcome = null, probeFrame = null) {
    editing = false;
    setPlane(frame.container_side);
    setPhase(phase, outcome);
    syncSquareLayer(acceptedLayer, frame.squares);
    syncSquareLayer(probeLayer, probeFrame ? probeFrame.squares : [], {probe: true});
    syncLabels(frame.squares, frame.container_side);
    displayedFrame = frame;
    rotateLeftButton.disabled = true;
    rotateRightButton.disabled = true;
    byId("selection-value").textContent = "Editor chunks released for this run";
  }

  function updateEventReadout(index) {
    const event = trace.events[index];
    const presentation = editor.phasePresentation(event);
    byId("run-readout-title").textContent = `Event ${index + 1} of ${trace.events.length}`;
    byId("mode-value").textContent = presentation.label;
    byId("event-value").textContent = event.detail;
    byId("counters-value").textContent = event.phase === "stop"
      ? `run total ${trace.result.lp_solves} LP solves; ${trace.result.cell_changes} cell changes`
      : [
        event.call_lp_solves === undefined ? null : `${event.call_lp_solves} LP solves in this call`,
        event.call_cell_changes === undefined ? null : `${event.call_cell_changes} cell changes in this call`,
      ].filter(Boolean).join("; ") || "No counters on this event";
    byId("groups-value").textContent = "Released; no optimizer constraints";
    byId("diagnostics-value").textContent = `${event.frame.squares.length} retained square poses`;
    byId("evidence-value").textContent = event.frame.evidence.claim;
    byId("timeline-output").textContent = `${index + 1} / ${trace.events.length}`;
    timelineInput.value = String(index);
    renderTimelineWindow(index);
  }

  function renderEvent(index) {
    eventIndex = Math.max(0, Math.min(index, trace.events.length - 1));
    const event = trace.events[eventIndex];
    if (event.phase === "angular-probe") {
      const accepted = acceptedFrameBefore(eventIndex);
      renderFrame(accepted, event.phase, event.outcome, event.frame);
    } else {
      renderFrame(event.frame, event.phase, event.outcome);
    }
    updateEventReadout(eventIndex);
  }

  function angleBetween(first, second, progress) {
    const quarter = Math.PI / 2;
    let delta = (second - first) % quarter;
    if (delta > quarter / 2) delta -= quarter;
    if (delta < -quarter / 2) delta += quarter;
    return first + delta * progress;
  }

  function interpolatedFrame(first, second, progress) {
    if (first.squares.length !== second.squares.length) return second;
    return {
      ...second,
      container_side: first.container_side
        + (second.container_side - first.container_side) * progress,
      squares: second.squares.map((square, index) => ({
        ...square,
        x: first.squares[index].x + (square.x - first.squares[index].x) * progress,
        y: first.squares[index].y + (square.y - first.squares[index].y) * progress,
        theta: angleBetween(first.squares[index].theta, square.theta, progress),
      })),
    };
  }

  function animateEvent(index, done) {
    const target = trace.events[index];
    if (reduceMotion || target.phase === "angular-probe" || !displayedFrame) {
      renderEvent(index);
      playbackTimer = window.setTimeout(done, 520);
      return;
    }
    const startFrame = displayedFrame;
    const startTime = performance.now();
    const duration = target.phase === "fixed-angle-lp" ? 620 : 440;
    eventIndex = index;
    updateEventReadout(index);
    setPhase(target.phase, target.outcome);
    function tick(now) {
      const progress = Math.min(1, (now - startTime) / duration);
      renderFrame(interpolatedFrame(startFrame, target.frame, progress), target.phase, target.outcome);
      if (progress < 1) {
        tweenFrame = requestAnimationFrame(tick);
      } else {
        tweenFrame = null;
        renderEvent(index);
        playbackTimer = window.setTimeout(done, 260);
      }
    }
    tweenFrame = requestAnimationFrame(tick);
  }

  function playNext() {
    const nextIndex = playbackIndices.find((index) => index > eventIndex);
    if (!trace || nextIndex === undefined) {
      stopPlayback();
      announce("Quench trace reached its terminal event.");
      return;
    }
    animateEvent(nextIndex, playNext);
  }

  playTraceButton.addEventListener("click", () => {
    if (playbackTimer !== null || tweenFrame !== null) {
      stopPlayback();
      announce("Trace playback paused.");
      return;
    }
    if (reduceMotion) {
      renderEvent(Math.min(eventIndex + 1, trace.events.length - 1));
      announce("Reduced-motion mode advanced one retained event.");
      return;
    }
    if (eventIndex >= trace.events.length - 1) renderEvent(0);
    playTraceButton.textContent = "Pause";
    announce("Trace playback started.");
    playNext();
  });

  byId("previous-event-button").addEventListener("click", () => {
    stopPlayback();
    renderEvent(eventIndex - 1);
  });
  byId("next-event-button").addEventListener("click", () => {
    stopPlayback();
    renderEvent(eventIndex + 1);
  });
  timelineInput.addEventListener("input", () => {
    stopPlayback();
    renderEvent(Number(timelineInput.value));
  });

  function timelineItem(event, index) {
    const presentation = editor.phasePresentation(event);
    const item = document.createElement("li");
    item.dataset.variant = presentation.variant;
    item.dataset.eventIndex = String(index);
    item.classList.toggle("current", index === eventIndex);
    const button = document.createElement("button");
    button.type = "button";
    button.className = "timeline-event-button";
    const title = document.createElement("strong");
    title.textContent = `${index + 1}. ${presentation.label}`;
    const detail = document.createElement("span");
    detail.textContent = event.detail;
    button.append(title, detail);
    button.addEventListener("click", () => {
      stopPlayback();
      renderEvent(index);
    });
    item.append(button);
    return item;
  }

  function timelineGap(first, last) {
    const item = document.createElement("li");
    item.className = "timeline-gap";
    item.textContent = `${first + 1}–${last + 1} retained events omitted from this window`;
    return item;
  }

  function renderTimelineWindow(index) {
    timelineList.replaceChildren();
    const windowed = editor.timelineWindow(trace.events.length, index, 20);
    if (windowed.start > 0) timelineList.append(timelineGap(0, windowed.start - 1));
    for (let current = windowed.start; current < windowed.end; current += 1) {
      timelineList.append(timelineItem(trace.events[current], current));
    }
    if (windowed.end < trace.events.length) {
      timelineList.append(timelineGap(windowed.end, trace.events.length - 1));
    }
    const current = timelineList.querySelector(`[data-event-index="${index}"]`);
    current?.scrollIntoView({block: "nearest", inline: "nearest"});
  }

  function buildTimeline() {
    playbackIndices = editor.selectPlaybackIndices(trace.events, 160);
    timelineInput.max = String(trace.events.length - 1);
    const result = trace.result;
    byId("trace-summary").textContent = `${trace.events.length} retained events; autoplay samples ${playbackIndices.length}, preserving every accepted rotation, cell change, setup, and stop. Slider and step controls reach every event. Side ${result.side.toPrecision(9)}; ${result.reason}; ${result.converged ? "converged" : "not converged"}.`;
  }

  runButton.addEventListener("click", async () => {
    stopPlayback();
    const request = editor.releaseQuenchRequest(
      state,
      Number(byId("sweeps-input").value),
      Number(byId("budget-input").value),
    );
    runButton.disabled = true;
    runButton.textContent = "Quenching…";
    announce(`Released ${state.groups.length} temporary chunks; numerical quench running.`);
    try {
      const response = await fetch("/api/quench", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(request),
      });
      const text = await response.text();
      const body = JSON.parse(text);
      if (!response.ok) throw new Error(body.error?.message || "numerical request failed");
      trace = body;
      traceText = text;
      traceName = `quench-trace-n${trace.request.x.length}-seed${seedInput.value}.json`;
      eventIndex = 0;
      timelinePanel.hidden = false;
      downloadButton.disabled = false;
      buildTimeline();
      renderEvent(0);
      announce(`Quench returned ${trace.events.length} retained events; playback is paused.`);
    } catch (error) {
      // Clear before reporting. The download button names its file a quench trace, so
      // a rejected run must leave nothing behind for it to save.
      clearTraceView();
      announce(`Quench failed: ${error.message}`);
      renderSetup();
    } finally {
      runButton.disabled = false;
      runButton.textContent = "Release + run quench";
    }
  });

  downloadButton.addEventListener("click", () => {
    if (!traceText) return;
    const blob = new Blob([traceText], {type: "application/json"});
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = traceName;
    link.click();
    // Revoking in the same task can cancel the download in some browsers.
    window.setTimeout(() => URL.revokeObjectURL(url), 0);
    announce("Canonical quench trace downloaded.");
  });

  byId("return-setup-button").addEventListener("click", () => {
    stopPlayback();
    timelinePanel.hidden = true;
    renderSetup();
    announce("Returned to the unchanged editor setup; the downloaded trace remains independent.");
  });

  renderSetup();
})();
