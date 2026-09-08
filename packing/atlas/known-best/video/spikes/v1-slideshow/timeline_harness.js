// Runs the candidate's embedded script against a stub DOM and checks the timeline
// API without a browser: node timeline_harness.js index.html
'use strict';
const fs = require('fs');
const page = fs.readFileSync(process.argv[2], 'utf8');
const json = page
  .match(/<script id="atlas-data" type="application\/json">([\s\S]*?)<\/script>/)[1]
  .replace(/<\\\//g, '</');
const script = page.match(/<script>([\s\S]*?)<\/script>/)[1];
const data = JSON.parse(json);
const DWELL = data.timing.dwell, FADE = data.timing.fade, SLOT = DWELL + FADE, COUNT = data.slides.length;
const TOTAL = COUNT * SLOT;

function el(tag) {
  return {
    tagName: tag, children: [], style: {}, attrs: {}, textContent: '', value: '', checked: false, max: '',
    get firstChild() { return this.children[0] || null; },
    get firstElementChild() { return this.children[0] || null; },
    setAttribute(k, v) { this.attrs[k] = v; },
    getAttribute(k) { return this.attrs[k]; },
    appendChild(c) { this.children.push(c); return c; },
    removeChild(c) { this.children = this.children.filter((x) => x !== c); return c; },
    cloneNode() { const n = el(this.tagName); n.attrs = Object.assign({}, this.attrs); return n; },
    querySelector() { return el('div'); },
    addEventListener() {},
    blur() {},
    getBoundingClientRect() { return { width: 1920, height: 1080 }; },
    classList: { toggle() {} },
  };
}
function layer(id) {
  const node = el('div');
  node.id = id;
  node.parts = { '.squares-host': el('g'), '.pic': el('div') };
  node.querySelector = function (sel) { return this.parts[sel]; };
  return node;
}
const gProto = el('g'), polyProto = el('polygon');
const layers = { 'layer-a': layer('layer-a'), 'layer-b': layer('layer-b') };
const generic = {};
let polygonsBuilt = 0, factsBuilt = 0;
polyProto.cloneNode = function () { polygonsBuilt += 1; return el('polygon'); };
const document = {
  getElementById(id) {
    if (id === 'atlas-data') return { textContent: json };
    if (id === 'proto') return { content: { querySelector: (sel) => (sel === 'g' ? gProto : polyProto) } };
    if (id.startsWith('facts-')) {
      const facts = el('div'); facts.attrs.n = Number(id.slice(6));
      return { content: { get firstElementChild() { factsBuilt += 1; return facts; } } };
    }
    if (layers[id]) return layers[id];
    if (!generic[id]) generic[id] = el(id === 'scrub' || id === 'jump' ? 'input' : 'div');
    return generic[id];
  },
  body: { classList: { toggle() {} } },
  activeElement: null,
  addEventListener() {},
};
const window = { addEventListener() {}, location: { search: '' } };
let rafCalls = 0;
const requestAnimationFrame = () => { rafCalls += 1; return rafCalls; };
const cancelAnimationFrame = () => {};
new Function('document', 'window', 'requestAnimationFrame', 'cancelAnimationFrame', script)(
  document, window, requestAnimationFrame, cancelAnimationFrame
);
const api = window.atlasVideo;
const factsHost = generic.facts, barFill = generic['progress-fill'], barCursor = generic['progress-cursor'];

let failures = 0;
function check(label, ok, detail) {
  if (!ok) { failures += 1; console.log('FAIL', label, detail === undefined ? '' : JSON.stringify(detail)); }
  else console.log('ok  ', label);
}
function near(a, b, eps) { return Math.abs(a - b) <= (eps || 1e-9); }
function held(which) {
  const l = layers[which];
  const g = l.parts['.squares-host'].children[0];
  return { n: g ? Number(g.attrs['data-n']) : 0, z: l.style.zIndex, opacity: l.style.opacity, visibility: l.style.visibility };
}
function layersFor() {
  const a = held('layer-a'), b = held('layer-b');
  return { base: a.z === '1' ? a : b, top: a.z === '2' ? a : b };
}
function panelN() {
  const kids = factsHost.children;
  if (kids.length > 1) { failures += 1; console.log('FAIL panel holds', kids.length, 'slides at once'); }
  return kids.length ? kids[0].attrs.n : 0;
}
function fill() { return parseFloat(barFill.style.width); }

check('count is 324', api.count === 324);
check('default timing is 1.5 + 0.5', DWELL === 1.5 && FADE === 0.5, data.timing);
check('duration 324 x 2.0 = 648', near(api.duration(), 648, 1e-6), api.duration());
let s = api.frameAt(0, 30);
check('frame 0 is n=1 dwell', s.n === 1 && s.progress === 0 && s.phase === 'dwell', s);
check('  bar at 0, panel 1, cursor "1"', s.bar === 0 && fill() === 0 && panelN() === 1 && barCursor.textContent === '1', [s.bar, fill(), panelN(), barCursor.textContent]);
s = api.seek(DWELL + FADE / 2);
check('t at the first fade midpoint fades 1 -> 2 at 50%', s.n === 1 && s.next === 2 && near(s.progress, 0.5, 1e-9), s);
let L = layersFor(s);
check('  base holds 1 visible, top holds 2 at half opacity', L.base.n === 1 && L.base.visibility === 'visible' && L.top.n === 2 && L.top.visibility === 'visible' && near(Number(L.top.opacity), 0.5, 1e-9), L);
check('  panel already cut to 2 at the midpoint', s.panel === 2 && panelN() === 2, [s.panel, panelN()]);
s = api.seek(DWELL + FADE * 0.49);
check('  just before the midpoint the panel still holds 1', s.panel === 1 && panelN() === 1, [s.panel, panelN()]);
s = api.seek(SLOT);
check('t=slot is n=2 dwell', s.n === 2 && s.progress === 0, s);
L = layersFor(s);
check('  roles swapped: base holds 2 visible, top holds 3 hidden', L.base.n === 2 && L.base.visibility === 'visible' && L.top.n === 3 && L.top.visibility === 'hidden', L);
s = api.seek(146 * SLOT + 1.0);
check('t inside slide 147', s.n === 147 && s.next === 148 && s.progress === 0 && s.panel === 147, s);
check('  bar is 146/323 there', near(s.bar, 146 / 323, 1e-9) && near(fill(), 100 * 146 / 323, 1e-3), [s.bar, fill()]);
s = api.seek(TOTAL - FADE / 2);
check('last slide fades out', s.n === 324 && s.next === 0 && near(s.progress, 0.5, 1e-6), s);
L = layersFor(s);
check('  base 324 at half opacity, nothing on top', L.base.n === 324 && near(Number(L.base.opacity), 0.5, 1e-6) && L.top.n === 0, L);
check('  bar pinned at 1, cursor "324"', s.bar === 1 && barCursor.textContent === '324', [s.bar, barCursor.textContent]);
s = api.frameAt(Math.ceil(TOTAL * 30) - 1, 30);
check('last frame at 30 fps is n=324', s.n === 324, s);
s = api.seek(5.0); const again = api.seek(5.0);
check('seek is idempotent', JSON.stringify(s) === JSON.stringify(again));
s = api.seek(100.0); L = layersFor(s);
const before = { base: L.base.n, top: L.top.n, panel: panelN(), fill: fill() };
api.seek(5.0); api.seek(500.0); s = api.seek(100.0); L = layersFor(s);
check('layer, panel and bar depend only on time', before.base === L.base.n && before.top === L.top.n && before.panel === panelN() && before.fill === fill(), [before, L]);

// The bar never goes backwards, from the first frame to the last, and the base
// layer is visible at every dwell however the seeks arrive.
let last = -1, backwards = 0, hiddenBase = 0, steps = 0;
for (let t = 0; t <= TOTAL + 1e-9; t += 0.1) {
  api.seek(t);
  const w = fill();
  if (w < last - 1e-9) backwards += 1;
  last = w;
  const lay = layersFor();
  if (lay.base.visibility !== 'visible') hiddenBase += 1;
  steps += 1;
}
check('bar width is monotone over ' + steps + ' seeks', backwards === 0, backwards);
check('bar ends at 100%', near(last, 100, 1e-6), last);
check('base layer visible at every seek', hiddenBase === 0, hiddenBase);
// Dwell-to-dwell seeks in order, the way a frame-by-frame capture never arrives
// but a review scrub does: the base must show at each.
hiddenBase = 0;
for (let k = 0; k < COUNT; k++) { api.seek(k * SLOT + DWELL / 2); if (layersFor().base.visibility !== 'visible') hiddenBase += 1; }
check('base layer visible at every dwell when seeking dwell to dwell', hiddenBase === 0, hiddenBase);

s = api.seek(146 * SLOT + 1.0);
const t = api.setTiming({ dwell: 3, fade: 1 });
check('setTiming reports 324 x 4', near(t.duration, 1296, 1e-6), t);
s = api.stateAt(146 * 4 + 1.5);
check('setTiming kept the position inside slide 147', s.n === 147, s);
s = api.seek(146 * 4 + 1.5);
check('after retiming slide 147 is at 146*4', s.n === 147 && s.progress === 0, s);
api.setTiming({ dwell: DWELL, fade: FADE });
check('retimed back to 648', near(api.duration(), 648, 1e-6), api.duration());
check('barAt agrees with stateAt', near(api.barAt(146 * SLOT + DWELL + FADE / 4), api.stateAt(146 * SLOT + DWELL + FADE / 4).bar), api.barAt(146 * SLOT + DWELL + FADE / 4));
check('no rAF used outside play', rafCalls === 0, rafCalls);
api.play(); check('play requests a frame', rafCalls === 1, rafCalls); api.pause();
check('slides were built from the record on demand', polygonsBuilt > 0 && factsBuilt > 0, { polygonsBuilt, factsBuilt });
console.log(failures ? `${failures} failure(s)` : 'timeline harness: all checks passed');
process.exit(failures ? 1 : 0);
