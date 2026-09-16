// The slideshow's player: the page script `build_candidate.py` inlines, byte for byte, into the
// candidate's `index.html`. It steps through the 324 packings on a virtual clock and publishes
// that clock as `window.atlasVideo`, which `probes/atlas-video.d.ts` declares.
//
// A classic script, not a module: the page runs it from an inline script element, and the
// `package.json` beside it says so, which is why its `"use strict"` directive stands.
// The JSDoc casts only tell the type checker what the markup `build_candidate.py` writes
// guarantees; none of them runs.
(() => {
  "use strict";
  var W = 1920,
    H = 1080;
  /**
   * The record `build_candidate.py` embeds as `#atlas-data`.
   * @type {{
   *   slides: {n: number, p: string, f: string, a: string, src?: string}[],
   *   first: number,
   *   palette: string[],
   *   timing: AtlasVideoTiming,
   *   settle: number,
   * }}
   */
  var data = JSON.parse(
    /** @type {HTMLElement} */ (document.getElementById("atlas-data")).textContent,
  );
  var slides = data.slides,
    first = data.first,
    count = slides.length;
  var timing = { dwell: data.timing.dwell, fade: data.timing.fade };
  var settleOn = true,
    settleAmount = data.settle;
  /** @type {{time: number, playing: boolean, stamp: number | null, raf: number, liveN: number, scrubbing: boolean}} */
  var state = { time: 0, playing: false, stamp: null, raf: 0, liveN: 0, scrubbing: false };

  var stage = /** @type {HTMLElement} */ (document.getElementById("stage"));
  var wrap = /** @type {HTMLElement} */ (document.getElementById("stage-wrap"));
  var live = /** @type {HTMLElement} */ (document.getElementById("live"));
  /** @type {HTMLElement[]} */
  var layerEls = [
    /** @type {HTMLElement} */ (document.getElementById("layer-a")),
    /** @type {HTMLElement} */ (document.getElementById("layer-b")),
  ];
  var layerN = [0, 0];
  var base = 0,
    top = 1;
  var factsHost = /** @type {HTMLElement} */ (document.getElementById("facts"));
  var factsN = 0;
  var barFill = /** @type {HTMLElement} */ (document.getElementById("progress-fill"));
  var barCursor = /** @type {HTMLElement} */ (document.getElementById("progress-cursor"));
  var proto = /** @type {HTMLTemplateElement} */ (document.getElementById("proto")).content;
  var gProto = /** @type {SVGGElement} */ (proto.querySelector("g"));
  var polyProto = /** @type {SVGPolygonElement} */ (proto.querySelector("polygon"));
  /** @type {Record<number, {squares: Node, facts: Node}>} */
  var built = {};

  function slot() {
    return timing.dwell + timing.fade;
  }
  function duration() {
    return count * slot();
  }
  /**
   * @param {number} v
   * @param {number} lo
   * @param {number} hi
   */
  function clamp(v, lo, hi) {
    return v < lo ? lo : v > hi ? hi : v;
  }
  /** @param {number} p */
  function smooth(p) {
    return p * p * (3 - 2 * p);
  }
  /** @param {number} p */
  function easeOut(p) {
    var q = 1 - p;
    return 1 - q * q * q;
  }

  /** @param {number} n */
  function ensure(n) {
    var c = built[n];
    if (c) {
      return c;
    }
    var slide = /** @type {(typeof slides)[number]} */ (slides[n - first]);
    var g = /** @type {SVGGElement} */ (gProto.cloneNode(false));
    g.setAttribute("data-n", String(n));
    var polys = slide.p.split(";");
    var i, el;
    for (i = 0; i < polys.length; i++) {
      el = /** @type {SVGPolygonElement} */ (polyProto.cloneNode(false));
      el.setAttribute("points", /** @type {string} */ (polys[i]));
      el.setAttribute(
        "fill",
        /** @type {string} */ (data.palette[parseInt(slide.f.charAt(i), 36)]),
      );
      g.appendChild(el);
    }
    var tpl = /** @type {HTMLTemplateElement} */ (document.getElementById(`facts-${n}`));
    c = {
      squares: g,
      facts: /** @type {Element} */ (tpl.content.firstElementChild).cloneNode(true),
    };
    built[n] = c;
    return c;
  }

  /** @param {Node} node */
  function clear(node) {
    while (node.firstChild) {
      node.removeChild(node.firstChild);
    }
  }

  /**
   * @param {number} index
   * @param {number} n
   */
  function load(index, n) {
    if (layerN[index] === n) {
      return;
    }
    var picHost = /** @type {Element} */ (
      /** @type {HTMLElement} */ (layerEls[index]).querySelector(".squares-host")
    );
    clear(picHost);
    if (n) {
      picHost.appendChild(ensure(n).squares);
    }
    layerN[index] = n;
  }

  /** @param {number} n */
  function loadFacts(n) {
    if (factsN === n) {
      return;
    }
    clear(factsHost);
    if (n) {
      factsHost.appendChild(ensure(n).facts);
    }
    factsN = n;
  }

  /** @param {number} t */
  function positionAt(t) {
    var s = slot(),
      D = timing.dwell,
      F = timing.fade;
    var k = Math.floor(t / s);
    if (k > count - 1) {
      k = count - 1;
    }
    if (k < 0) {
      k = 0;
    }
    var u = t - k * s;
    var p = 0;
    if (u >= D) {
      p = F > 0 ? clamp((u - D) / F, 0, 1) : 1;
    }
    // The panel cuts at the fade's midpoint: text is never half there, and the
    // panel always belongs to whichever picture the dissolve favours.
    var panel = p >= 0.5 ? (k + 1 < count ? first + k + 1 : 0) : first + k;
    // The bar advances one step of 323 across each fade and rests through each dwell.
    var bar = count > 1 ? clamp((k + p) / (count - 1), 0, 1) : 1;
    return {
      index: k,
      n: first + k,
      next: k + 1 < count ? first + k + 1 : 0,
      progress: p,
      within: u,
      panel: panel,
      bar: bar,
    };
  }

  /**
   * @param {number} t
   * @returns {AtlasVideoState}
   */
  function stateAt(t) {
    var pos = positionAt(t);
    return {
      time: t,
      n: pos.n,
      next: pos.next,
      progress: pos.progress,
      phase: pos.progress > 0 ? "fade" : "dwell",
      panel: pos.panel,
      bar: pos.bar,
    };
  }

  /** @param {number} t */
  function barAt(t) {
    return positionAt(t).bar;
  }

  function render() {
    var pos = positionAt(state.time);
    var nCur = pos.n,
      nNext = pos.next,
      p = pos.progress;
    var tmp;
    if (layerN[top] === nCur) {
      tmp = base;
      base = top;
      top = tmp;
    }
    load(base, nCur);
    load(top, nNext);
    var e = smooth(p);
    var baseEl = /** @type {HTMLElement} */ (layerEls[base]),
      topEl = /** @type {HTMLElement} */ (layerEls[top]);
    baseEl.style.zIndex = "1";
    topEl.style.zIndex = "2";
    // Always: a layer hidden while it was on top must show when a seek makes it the base.
    baseEl.style.visibility = "visible";
    if (nNext) {
      baseEl.style.opacity = "1";
      topEl.style.opacity = String(e);
      topEl.style.visibility = p > 0 ? "visible" : "hidden";
    } else {
      baseEl.style.opacity = String(1 - e);
      topEl.style.opacity = "0";
      topEl.style.visibility = "hidden";
    }
    var topPic = /** @type {HTMLElement} */ (topEl.querySelector(".pic"));
    topPic.style.transform =
      settleOn && nNext ? `scale(${1 - settleAmount * (1 - easeOut(p))})` : "";
    /** @type {HTMLElement} */ (baseEl.querySelector(".pic")).style.transform = "";
    loadFacts(pos.panel);
    var pct = `${(pos.bar * 100).toFixed(4)}%`;
    barFill.style.width = pct;
    barCursor.textContent = String(pos.panel || nCur);
    // The label rides above the fill's leading edge and is held inside the track at
    // either end, so it never runs into the 1 and the 324 beside the track.
    var trackW = barFill.parentNode
      ? /** @type {HTMLElement} */ (barFill.parentNode).offsetWidth || 0
      : 0;
    var half = (barCursor.offsetWidth || 0) / 2;
    barCursor.style.left =
      trackW > 0 ? `${clamp(pos.bar * trackW, half, trackW - half).toFixed(2)}px` : pct;
    var liveN = pos.panel || nCur;
    if (liveN !== state.liveN) {
      state.liveN = liveN;
      live.textContent = /** @type {(typeof slides)[number]} */ (slides[liveN - first]).a;
    }
    updateReadout(pos);
  }

  /** @param {number} t */
  function fmt(t) {
    var m = Math.floor(t / 60);
    var s = t - m * 60;
    var whole = Math.floor(s);
    var tenth = Math.floor((s - whole) * 10);
    return `${(m < 10 ? "0" : "") + m}:${whole < 10 ? "0" : ""}${whole}.${tenth}`;
  }

  var readout = /** @type {HTMLElement} */ (document.getElementById("readout"));
  var scrub = /** @type {HTMLInputElement} */ (document.getElementById("scrub"));
  var jump = /** @type {HTMLInputElement} */ (document.getElementById("jump"));
  var playBtn = /** @type {HTMLElement} */ (document.getElementById("btn-play"));
  var lengthEl = /** @type {HTMLElement} */ (document.getElementById("length"));

  /** @param {ReturnType<typeof positionAt>} pos */
  function updateReadout(pos) {
    var text = `n ${pos.n}`;
    if (pos.progress > 0) {
      text += pos.next ? ` → ${pos.next} (fade ${Math.round(pos.progress * 100)}%)` : " (fade out)";
    }
    text += ` · ${fmt(state.time)} / ${fmt(duration())}`;
    readout.textContent = text;
    if (!state.scrubbing) {
      scrub.value = String(state.time);
    }
    if (document.activeElement !== jump) {
      jump.value = String(pos.n);
    }
  }

  function syncTiming() {
    scrub.max = String(duration());
    lengthEl.textContent = `length ${fmt(duration())} at ${count} × (${timing.dwell.toFixed(2)} + ${timing.fade.toFixed(2)}) s`;
    /** @type {HTMLInputElement} */ (document.getElementById("dwell")).value = String(timing.dwell);
    /** @type {HTMLInputElement} */ (document.getElementById("fade")).value = String(timing.fade);
  }

  /** @param {number} stamp */
  function frame(stamp) {
    if (!state.playing) {
      return;
    }
    if (state.stamp !== null) {
      state.time += (stamp - state.stamp) / 1000;
    }
    state.stamp = stamp;
    if (state.time >= duration()) {
      state.time = duration();
      render();
      pause();
      return;
    }
    render();
    state.raf = requestAnimationFrame(frame);
  }

  function play() {
    if (state.playing) {
      return;
    }
    if (state.time >= duration()) {
      state.time = 0;
    }
    state.playing = true;
    state.stamp = null;
    playBtn.textContent = "Pause";
    state.raf = requestAnimationFrame(frame);
  }

  function pause() {
    if (state.raf) {
      cancelAnimationFrame(state.raf);
    }
    state.raf = 0;
    state.playing = false;
    state.stamp = null;
    playBtn.textContent = "Play";
  }

  /** @param {number} seconds */
  function seek(seconds) {
    state.time = clamp(Number(seconds) || 0, 0, duration());
    render();
    return stateAt(state.time);
  }

  /**
   * @param {number} index
   * @param {number} fps
   */
  function frameAt(index, fps) {
    return seek(index / fps);
  }

  /** @param {Partial<AtlasVideoTiming> | null} [options] */
  function setTiming(options) {
    var pos = positionAt(state.time);
    var frac =
      pos.progress > 0 ? 1 + pos.progress : timing.dwell > 0 ? pos.within / timing.dwell : 0;
    if (options && typeof options.dwell === "number" && options.dwell > 0) {
      timing.dwell = options.dwell;
    }
    if (options && typeof options.fade === "number" && options.fade >= 0) {
      timing.fade = options.fade;
    }
    var t =
      pos.index * slot() +
      (frac <= 1 ? frac * timing.dwell : timing.dwell + (frac - 1) * timing.fade);
    state.time = clamp(t, 0, duration());
    syncTiming();
    render();
    return { dwell: timing.dwell, fade: timing.fade, duration: duration() };
  }

  /** @param {boolean} on */
  function setSettle(on) {
    settleOn = !!on;
    /** @type {HTMLInputElement} */ (document.getElementById("settle")).checked = settleOn;
    render();
  }

  function fit() {
    var r = wrap.getBoundingClientRect();
    var k = Math.min(r.width / W, r.height / H);
    stage.style.transform = `scale(${k})`;
  }

  /** @param {boolean} on */
  function setCapture(on) {
    document.body.classList.toggle("capture", !!on);
    /** @type {HTMLInputElement} */ (document.getElementById("capture")).checked = !!on;
    fit();
  }

  /** @param {number} k */
  function goSlide(k) {
    k = clamp(k, 0, count - 1);
    seek(k * slot());
  }

  // ---- controls
  playBtn.addEventListener("click", () => {
    if (state.playing) {
      pause();
    } else {
      play();
    }
  });
  /** @type {HTMLElement} */ (document.getElementById("btn-prev")).addEventListener("click", () => {
    goSlide(positionAt(state.time).index - 1);
  });
  /** @type {HTMLElement} */ (document.getElementById("btn-next")).addEventListener("click", () => {
    goSlide(positionAt(state.time).index + 1);
  });
  scrub.addEventListener("input", () => {
    state.scrubbing = true;
    seek(Number(scrub.value));
  });
  scrub.addEventListener("change", () => {
    state.scrubbing = false;
    seek(Number(scrub.value));
  });
  jump.addEventListener("change", () => {
    goSlide(Math.round(Number(jump.value)) - first);
    jump.blur();
  });
  /** @type {HTMLElement} */ (document.getElementById("dwell")).addEventListener("change", (ev) => {
    setTiming({ dwell: Number(/** @type {HTMLInputElement} */ (ev.target).value) });
  });
  /** @type {HTMLElement} */ (document.getElementById("fade")).addEventListener("change", (ev) => {
    setTiming({ fade: Number(/** @type {HTMLInputElement} */ (ev.target).value) });
  });
  /** @type {HTMLElement} */ (document.getElementById("settle")).addEventListener(
    "change",
    (ev) => {
      setSettle(/** @type {HTMLInputElement} */ (ev.target).checked);
    },
  );
  /** @type {HTMLElement} */ (document.getElementById("capture")).addEventListener(
    "change",
    (ev) => {
      setCapture(/** @type {HTMLInputElement} */ (ev.target).checked);
    },
  );
  document.addEventListener("keydown", (ev) => {
    var tag = /** @type {Element | null} */ (ev.target)?.tagName;
    if (tag === "INPUT" || tag === "TEXTAREA" || tag === "BUTTON") {
      return;
    }
    if (ev.key === " ") {
      ev.preventDefault();
      if (state.playing) {
        pause();
      } else {
        play();
      }
    } else if (ev.key === "ArrowRight") {
      ev.preventDefault();
      goSlide(positionAt(state.time).index + 1);
    } else if (ev.key === "ArrowLeft") {
      ev.preventDefault();
      goSlide(positionAt(state.time).index - 1);
    } else if (ev.key === "Home") {
      ev.preventDefault();
      seek(0);
    } else if (ev.key === "End") {
      ev.preventDefault();
      goSlide(count - 1);
    }
  });
  window.addEventListener("resize", fit);

  window.atlasVideo = {
    seek: seek,
    frameAt: frameAt,
    duration: duration,
    play: play,
    pause: pause,
    setTiming: setTiming,
    stateAt: stateAt,
    barAt: barAt,
    setSettle: setSettle,
    setCapture: setCapture,
    timing: () => ({ dwell: timing.dwell, fade: timing.fade }),
    count: count,
    // A promise is always truthy, so asking whether the platform supplies one at all is the
    // same question as the truthiness test it replaces, without testing a promise as a boolean.
    ready: document.fonts?.ready != null ? document.fonts.ready : Promise.resolve(),
  };

  syncTiming();
  if (/[?&]capture=1/.test(window.location.search)) {
    setCapture(true);
  }
  fit();
  render();
})();
