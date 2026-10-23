// The atlas view script's pure functions, run in a context with no document, as the
// table script's are: it publishes them on `globalThis.SiteAtlasView` and wires nothing
// until `atlas-grid.js` calls `mount`.
//
// They are the whole of the triangle's arithmetic: which row a case is in, how many
// tiles a line holds at a width, where each case then stands, and how a tile's first
// frame is worked out from where it was. The browser tests
// (`tests/test_site_atlas_views.py`) hold the page to the same shapes as laid out.
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import vm from "node:vm";

const SOURCE = readFileSync(
  new URL("../../../devtools/overview/atlas-view.js", import.meta.url),
  "utf8",
);

/** @returns {SiteAtlasViewApi} */
function load() {
  const context = vm.createContext({ URLSearchParams });
  vm.runInContext(SOURCE, context);
  return context.SiteAtlasView;
}

const atlas = load();

// The script's objects are of its own context, which `deepEqual` tells from this one's,
// so each is copied before it is compared.
/**
 * @param {number} n
 * @param {number} per
 * @returns {Omit<AtlasTrianglePlace, "gap" | "segmentLine" | "segmentColumn">}
 */
const place = (n, per) => {
  const {
    gap: _gap,
    segmentLine: _line,
    segmentColumn: _column,
    ...position
  } = atlas.place(n, per);
  return position;
};

/**
 * Cases 1 to `last` by line, each line the cases on it from the left with their columns.
 * @param {number} last
 * @param {number} per
 * @returns {{ n: number, column: number, row: number, opens: boolean }[][]}
 */
function lines(last, per) {
  /** @type {{ n: number, column: number, row: number, opens: boolean }[][]} */
  const found = [];
  for (let n = 1; n <= last; n += 1) {
    const at = atlas.place(n, per);
    const line = found[at.line - 1] ?? [];
    found[at.line - 1] = line;
    line.push({ n, column: at.column, row: at.row, opens: at.opens });
  }
  return found;
}

/**
 * How many tiles each line of row `k` holds.
 * @param {number} k
 * @param {number} per
 * @returns {number[]}
 */
function rowLines(k, per) {
  return lines(k * k, per)
    .filter((line) => line[0]?.row === k)
    .map((line) => line.length);
}

void test("row k holds the cases after (k - 1) squared, up to k squared", () => {
  /** @type {[number, number][]} */
  const known = [
    [1, 1],
    [2, 2],
    [4, 2],
    [5, 3],
    [9, 3],
    [10, 4],
    [100, 10],
    [101, 11],
    [324, 18],
  ];
  for (const [n, k] of known) {
    assert.equal(atlas.row(n), k, `n = ${n}`);
  }
  for (let n = 1; n <= 2000; n += 1) {
    const k = atlas.row(n);
    assert.ok((k - 1) * (k - 1) < n && n <= k * k, `n = ${n}`);
  }
});

void test("the longest row has 2k - 1 tiles: 19 of a hundred cases and 35 of 324", () => {
  assert.equal(atlas.widest(1), 1);
  assert.equal(atlas.widest(100), 19);
  assert.equal(atlas.widest(101), 21);
  assert.equal(atlas.widest(324), 35);
});

void test("a line budgets the shared cell minimum and the gaps between tiles", () => {
  assert.equal(atlas.perLine(1200, 108, 19, 8), 10);
  assert.equal(atlas.perLine(1200, 108, 35, 8), 10);
  assert.equal(atlas.perLine(944, 108, 35, 8), 8);
  assert.equal(atlas.perLine(688, 108, 35, 8), 6);
  assert.equal(atlas.perLine(358, 73.6, 19, 5.6), 4);
  // The final tile needs no gap after it: two 108px tiles fit in exactly 224px.
  assert.equal(atlas.perLine(224, 108, 19, 8), 2);
  assert.equal(atlas.perLine(223, 108, 19, 8), 1);
  assert.equal(atlas.perLine(2240, 108, 19, 8), 19);
  assert.equal(atlas.perLine(10, 108, 19, 8), 1);
  assert.equal(atlas.perLine(0, 108, 19, 8), 19);
  assert.equal(atlas.perLine(358, Number.NaN, 19, 8), 19);
});

void test("each size fits as many scaled cells as the shared grid minimum allows", () => {
  assert.equal(atlas.perLineAt(1200, 108, 19, 0.667, 8), 15);
  assert.equal(atlas.perLineAt(1200, 108, 19, 1, 8), 10);
  assert.equal(atlas.perLineAt(1200, 108, 19, 1.5, 8), 7);
  assert.equal(atlas.perLineAt(358, 73.6, 19, 0.667, 5.6), 6);
  assert.equal(atlas.perLineAt(358, 73.6, 19, 1, 5.6), 4);
  assert.equal(atlas.perLineAt(358, 73.6, 19, 1.5, 5.6), 3);
  assert.equal(atlas.perLineAt(10, 108, 19, 1.5, 8), 1);
  assert.equal(atlas.perLineAt(4000, 108, Number.POSITIVE_INFINITY, 1, 8), 34);
  assert.equal(atlas.perLineAt(4200, 108, Number.POSITIVE_INFINITY, 1, 8), 36);
  assert.equal(atlas.perLineAt(1200, 108, 19, Number.NaN, 8), 10);
  for (let width = 300; width <= 2400; width += 7) {
    for (const most of [19, 35]) {
      const small = atlas.perLineAt(width, 108, most, 0.667, 8);
      const medium = atlas.perLineAt(width, 108, most, 1, 8);
      const large = atlas.perLineAt(width, 108, most, 1.5, 8);
      assert.ok(1 <= large && large <= medium && medium <= small && small <= most);
      for (const scale of [0.667, 1, 1.5]) {
        const per = atlas.perLineAt(width, 108, most, scale, 8);
        assert.ok(per * 108 * scale + (per - 1) * 8 <= width);
      }
    }
  }
});

void test("every complete row ends at the same rightmost canvas column", () => {
  for (const [last, columns] of /** @type {[number, number][]} */ ([
    [100, 19],
    [324, 35],
    [324, 40],
  ])) {
    for (let n = 1; n <= last; n += 1) {
      const k = atlas.row(n);
      assert.deepEqual(
        place(n, columns),
        { row: k, line: k, column: columns - (2 * k - 1) + n - (k - 1) ** 2, opens: k > 1 },
        String(n),
      );
    }
  }
});

void test("nineteen cases stay on one line even when the viewport holds eight", () => {
  assert.deepEqual(rowLines(10, 8), [19]);
  const found = lines(100, 19).filter((line) => line[0]?.row === 10);
  assert.equal(found.length, 1);
  assert.deepEqual(
    found[0]?.map(({ n, column }) => [n, column]),
    Array.from({ length: 19 }, (_, i) => [82 + i, i + 1]),
  );
});

void test("short rows use consecutive columns ending at the right edge", () => {
  assert.deepEqual(
    lines(16, 8)[2]?.map(({ n, column }) => [n, column]),
    [
      [5, 4],
      [6, 5],
      [7, 6],
      [8, 7],
      [9, 8],
    ],
  );
  assert.deepEqual(rowLines(4, 7), [7]);
  assert.equal(atlas.place(10, 7).column, 1);
});

void test("a canvas narrower than a row keeps the row complete", () => {
  assert.deepEqual(rowLines(5, 3), [9]);
  assert.deepEqual(place(17, 3), { row: 5, line: 5, column: 1, opens: true });
  assert.deepEqual(place(25, 3), { row: 5, line: 5, column: 9, opens: true });
});

void test("perfect squares occupy the common final column without wrapped lines", () => {
  for (let columns = 35; columns <= 40; columns += 1) {
    for (let k = 1; k <= 18; k += 1) {
      const square = atlas.place(k * k, columns);
      assert.equal(square.column, columns);
      assert.equal(square.line, k);
    }
  }
});

void test("retained grid suffixes stay beside their non-grid prefix with a separator", () => {
  const starts = Object.fromEntries(
    [1, 2, 6, 12, 20, 30, 42, 56, 72, 90, 111, 133, 157, 183, 212, 242, 274, 308].map((n) => [
      atlas.row(n),
      n,
    ]),
  );
  for (const columns of [35, 40]) {
    for (let k = 1; k <= 18; k += 1) {
      const first = (k - 1) ** 2 + 1;
      const boundary = starts[k];
      assert.ok(boundary !== undefined);
      for (let n = first; n <= k * k; n += 1) {
        const at = atlas.place(n, columns, starts);
        assert.equal(at.line, k);
        assert.equal(at.segmentLine, 1);
        assert.equal(at.segmentColumn, n - (n >= boundary ? boundary : first) + 1);
        assert.equal(at.gap, boundary > first && n >= boundary);
      }
      assert.equal(atlas.place(k * k, columns, starts).column, columns);
    }
  }
  // Row 8's six non-grid and nine grid cases share one physical line.
  assert.equal(atlas.place(56, 35, starts).line, atlas.place(55, 35, starts).line);
  assert.equal(atlas.place(56, 35, starts).segmentColumn, 1);
  assert.equal(atlas.place(56, 35, starts).gap, true);
  assert.equal(atlas.place(2, 35, starts).gap, false);
});

void test("cases read left to right and top to bottom, with one row per line", () => {
  for (const last of [100, 324]) {
    const columns = atlas.widest(last);
    const found = lines(last, columns);
    assert.equal(found.length, atlas.row(last));
    assert.deepEqual(
      found.flatMap((line) => line.map(({ n }) => n)),
      Array.from({ length: last }, (_, i) => i + 1),
    );
    for (const line of found) {
      assert.equal(new Set(line.map(({ row }) => row)).size, 1);
      assert.equal(new Set(line.map(({ column }) => column)).size, line.length);
      assert.equal(line.at(-1)?.column, columns);
    }
  }
});

void test("complete row counts are independent of viewport capacity", () => {
  for (let capacity = 1; capacity <= 40; capacity += 1) {
    for (let k = 1; k <= 18; k += 1) {
      assert.deepEqual(rowLines(k, capacity), [2 * k - 1]);
    }
  }
});

void test("every row after the first opens one ordinary physical line", () => {
  for (const line of lines(324, 35)) {
    const first = line[0];
    assert.ok(first !== undefined);
    assert.ok(line.every((tile) => tile.opens === first.row > 1));
  }
});

void test("the address defaults to Triangle and explicitly names Grid", () => {
  assert.equal(atlas.viewOf(""), "triangle");
  assert.equal(atlas.viewOf("?atlas=triangle"), "triangle");
  assert.equal(atlas.viewOf("?atlas=grid"), "grid");
  assert.equal(atlas.viewOf("?atlas=pyramid"), "triangle");
  assert.equal(atlas.viewOf("?s-min=4&atlas=triangle&age=180"), "triangle");
  assert.equal(atlas.viewOf("?s-min=4&atlas=grid&age=180"), "grid");
  assert.equal(atlas.searchFor("", "triangle"), "");
  assert.equal(atlas.searchFor("?atlas=triangle", "grid"), "?atlas=grid");
  assert.equal(atlas.searchFor("?atlas=grid", "triangle"), "");
});

void test("writing the view keeps every other parameter, and round-trips", () => {
  assert.equal(atlas.searchFor("?s-min=4&age=180", "grid"), "?s-min=4&age=180&atlas=grid");
  assert.equal(atlas.searchFor("?s-min=4&atlas=grid&age=180", "triangle"), "?s-min=4&age=180");
  assert.equal(
    atlas.searchFor("?atlas=triangle&project=evand-square-packing", "grid"),
    "?atlas=grid&project=evand-square-packing",
  );
  for (const search of ["", "?age=180", "?atlas=triangle", "?x=1&atlas=grid"]) {
    for (const view of /** @type {AtlasView[]} */ (["grid", "triangle"])) {
      assert.equal(atlas.viewOf(atlas.searchFor(search, view)), view);
    }
  }
});

void test("the address preserves an explicit size, including Small on a wide-screen reload", () => {
  assert.equal(atlas.sizeOf(""), "small");
  assert.equal(atlas.sizeOf("?size=small"), "small");
  assert.equal(atlas.sizeOf("?size=large"), "large");
  assert.equal(atlas.sizeOf("?size=medium"), "medium");
  assert.equal(atlas.sizeOf("?size=Large"), "small");
  assert.equal(atlas.sizeOf("?size=huge"), "small");
  assert.equal(atlas.sizeOf("?atlas=triangle&size=large&age=180"), "large");
  assert.equal(atlas.searchForSize("", "large"), "?size=large");
  assert.equal(atlas.searchForSize("?size=large", "medium"), "?size=medium");
  assert.equal(atlas.searchForSize("?size=large", "small"), "?size=small");
  assert.equal(atlas.searchForSize("?age=180", "small"), "?age=180&size=small");
  assert.equal(atlas.searchForSize("", "medium"), "?size=medium");
  for (const search of ["", "?age=180", "?size=small", "?x=1&size=medium"]) {
    for (const size of /** @type {AtlasSize[]} */ (["small", "medium", "large"])) {
      assert.equal(atlas.sizeOf(atlas.searchForSize(search, size)), size);
    }
  }
});

void test("the view and the size are two parameters that never overwrite each other", () => {
  let search = "?age=180";
  search = atlas.searchFor(search, "grid");
  search = atlas.searchForSize(search, "large");
  assert.equal(search, "?age=180&atlas=grid&size=large");
  assert.equal(atlas.viewOf(search), "grid");
  assert.equal(atlas.sizeOf(search), "large");
  search = atlas.searchFor(search, "triangle");
  assert.equal(search, "?age=180&size=large");
  assert.equal(atlas.sizeOf(search), "large");
  search = atlas.searchForSize(search, "medium");
  assert.equal(search, "?age=180&size=medium");
  assert.equal(atlas.viewOf(search), "triangle");
});

void test("the arrow keys wrap between the tabs, Home and End go to the ends", () => {
  for (const count of [2, 3]) {
    assert.equal(atlas.stepTo("ArrowRight", count - 1, count), 0);
    assert.equal(atlas.stepTo("ArrowLeft", 0, count), count - 1);
    assert.equal(atlas.stepTo("Home", count - 1, count), 0);
    assert.equal(atlas.stepTo("End", 0, count), count - 1);
  }
  assert.equal(atlas.stepTo("ArrowRight", 0, 3), 1);
  assert.equal(atlas.stepTo("ArrowLeft", 2, 3), 1);
  assert.equal(atlas.stepTo("ArrowDown", 0, 2), -1);
  assert.equal(atlas.stepTo("Enter", 0, 2), -1);
  assert.equal(atlas.stepTo("ArrowRight", -1, 2), -1);
  assert.equal(atlas.stepTo("ArrowRight", 0, 0), -1);
});

void test("a length token is read in rem or pixels, and nothing else", () => {
  assert.equal(atlas.lengthPx("1.625rem", 16), 26);
  assert.equal(atlas.lengthPx(" 2.5rem ", 16), 40);
  assert.equal(atlas.lengthPx("2.5rem", 20), 50);
  assert.equal(atlas.lengthPx("24px", 16), 24);
  assert.ok(Number.isNaN(atlas.lengthPx("", 16)));
  assert.ok(Number.isNaN(atlas.lengthPx("clamp(1rem, 2vw, 3rem)", 16)));
});

void test("a time token is read in milliseconds or seconds, and anything else is no move", () => {
  assert.equal(atlas.milliseconds("360ms"), 360);
  assert.equal(atlas.milliseconds(" 0.36s "), 360);
  assert.equal(atlas.milliseconds("0ms"), 0);
  assert.equal(atlas.milliseconds(""), 0);
  assert.equal(atlas.milliseconds("fast"), 0);
});

void test("a tile that has not moved has no transform to start from", () => {
  const drawing = { left: 104, top: 204, width: 92 };
  const holder = { left: 100, top: 200, width: 100 };
  const move = { ...atlas.moveFrom(drawing, drawing, holder) };
  assert.deepEqual(move, { x: 0, y: 0, scale: 1 });
  assert.ok(atlas.still(move));
  assert.ok(!atlas.still({ x: 0, y: 0.6, scale: 1 }));
  assert.ok(!atlas.still({ x: 0, y: 0, scale: 1.02 }));
});

void test("a move sets the drawing back on its old box, scaled about the tile's corner", () => {
  // In the grid the drawing was 100 pixels wide at (300, 500). In the triangle the tile
  // is at (700, 80) and its drawing, inset 3 pixels, is 50 wide.
  const first = { left: 300, top: 500, width: 100 };
  const last = { left: 703, top: 83, width: 50 };
  const holder = { left: 700, top: 80, width: 56 };
  const move = atlas.moveFrom(first, last, holder);
  assert.equal(move.scale, 2);
  // The drawing's corner is 3 pixels into the tile, 6 once scaled, so the tile's own
  // corner starts 6 pixels up and left of where the drawing was.
  assert.deepEqual([move.x, move.y], [300 - 700 - 6, 500 - 80 - 6]);
  const drawn = {
    left: holder.left + move.x + move.scale * (last.left - holder.left),
    top: holder.top + move.y + move.scale * (last.top - holder.top),
    width: move.scale * last.width,
  };
  assert.deepEqual(drawn, first);
});

void test("drawing scale URLs default to Row, preserve explicit Fixed, and retain layout and size", () => {
  for (const search of ["", "?scale=row", "?scale=unknown", "?scale=ROW"]) {
    assert.equal(atlas.scaleOf(search), "row");
  }
  assert.equal(atlas.scaleOf("?atlas=grid&scale=fixed&size=large"), "fixed");
  assert.equal(atlas.scaleOf("?scale=global"), "global");
  assert.equal(
    atlas.searchForScale("?x=1&atlas=grid&size=large", "row"),
    "?x=1&atlas=grid&size=large",
  );
  assert.equal(
    atlas.searchForScale("?x=1&scale=global&size=medium", "fixed"),
    "?x=1&scale=fixed&size=medium",
  );
  assert.equal(
    atlas.searchForSize("?scale=row&atlas=grid", "large"),
    "?scale=row&atlas=grid&size=large",
  );
  assert.equal(atlas.searchFor("?scale=global&size=large", "triangle"), "?scale=global&size=large");
});

void test("Row ratios use the actual enclosing side and the logical square-bound row", () => {
  // These are enclosing sides, not sqrt(n), lower bounds, or responsive grid lines.
  const five = 2 + Math.SQRT1_2;
  assert.equal(atlas.rowRatio(5, five), five / 3);
  assert.notEqual(atlas.rowRatio(5, five), Math.sqrt(5) / 3);
  assert.equal(atlas.rowRatio(25, 5), 1);
  assert.equal(atlas.rowRatio(36, 6), 1);
  assert.equal(atlas.rowRatio(18, 4 + Math.SQRT1_2), (4 + Math.SQRT1_2) / 5);
});

void test("Global reference is the largest actual side among this instance's shown cases", () => {
  // A subset can end between perfect squares; neither its count nor last n is a side.
  assert.equal(atlas.largestSide([2, 2.7071067811865475, 3.8]), 3.8);
  assert.equal(atlas.largestSide([6.1, 5.95, 6]), 6.1);
  assert.equal(atlas.largestSide([1, 10]), 10);
  assert.equal(atlas.largestSide([1, 10, 18]), 18);
});

// A triangle that follows the scroll (think-apqd) is drawn once at Large and zoomed as
// one picture; these are the arithmetic it reads each frame. The browser tests hold the
// page to the same behaviour as drawn.
void test("A size's tile is the stylesheet's: whole cells of the scaled least width", () => {
  // 1349px at 6.4rem cells and 0.5rem gaps, the dedicated Atlas on a 1440px window.
  assert.equal(atlas.tileAt(1349, 102.4, 1.5, 8), (1349 - 7 * 8) / 8);
  assert.equal(atlas.tileAt(1349, 102.4, 0.667, 8), (1349 - 16 * 8) / 17);
  assert.equal(atlas.tileAt(1349, 102.4, 1, 8), (1349 - 11 * 8) / 12);
  assert.ok(Number.isNaN(atlas.tileAt(1349, Number.NaN, 1, 8)));
});

void test("The framing keeps the middle a third along the row with its left end in view", () => {
  // The rule itself, with its bend taken out.
  assert.equal(atlas.followLeft(930, 600, 1 / 3, 0), 465 - 200);
  assert.equal(atlas.followLeft(930, 1500, 1 / 3, 0), 0);
  // Away from the edge the bend changes nothing, and near it the left end stays right of
  // where the rule puts it, so it never leaves view.
  assert.equal(atlas.followLeft(930, 600, 1 / 3), 465 - 200);
  for (let width = 800; width <= 4000; width += 7) {
    assert.ok(atlas.followLeft(930, width, 1 / 3) >= atlas.followLeft(930, width, 1 / 3, 0));
  }
});

/**
 * The largest jump in slope between neighbouring steps of `f` over [from, to].
 * @param {(x: number) => number} f
 * @param {number} from
 * @param {number} to
 */
function kink(f, from, to) {
  const steps = 4000;
  const h = (to - from) / steps;
  let worst = 0;
  for (let i = 1; i < steps; i += 1) {
    const x = from + i * h;
    worst = Math.max(worst, Math.abs((f(x + h) - f(x)) / h - (f(x) - f(x - h)) / h));
  }
  return worst;
}

void test("The zoom is one smooth curve from Large to the least zoom", () => {
  assert.equal(atlas.smootherstep(-1), 0);
  assert.equal(atlas.smootherstep(0.5), 0.5);
  assert.equal(atlas.smootherstep(2), 1);
  const zoom = (/** @type {number} */ point) => atlas.zoomAt(point, 1000, 3000, 0.45);
  assert.equal(zoom(0), 1);
  assert.equal(zoom(1000), 1);
  assert.equal(zoom(3000), 0.45);
  assert.equal(zoom(5000), 0.45);
  // It only ever shrinks, starts and stops with no slope, and has no corner anywhere.
  for (let point = 1000; point < 3000; point += 10) {
    assert.ok(zoom(point + 10) <= zoom(point));
  }
  assert.ok(Math.abs(zoom(1001) - zoom(1000)) < 1e-6);
  assert.ok(Math.abs(zoom(3000) - zoom(2999)) < 1e-6);
  assert.ok(kink(zoom, 0, 4000) < 1e-5);
  // A triangle that never needs to zoom stays at Large.
  assert.equal(atlas.zoomAt(500, Number.POSITIVE_INFINITY, Number.POSITIVE_INFINITY, 0.45), 1);
});

void test("The pan and the framing bend onto their limits without a corner", () => {
  /** @param {number} bend */
  const left = (bend) => (/** @type {number} */ width) => atlas.followLeft(930, width, 1 / 3, bend);
  assert.ok(kink(left(240), 1000, 2000) < kink(left(0), 1000, 2000) / 50);
  /** @param {number} bend */
  const pan = (bend) => (/** @type {number} */ x) => atlas.panTo(x, 0, 0, 5000, bend);
  assert.ok(kink(pan(240), -600, 600) < kink(pan(0), -600, 600) / 50);
  assert.equal(pan(240)(300), 0);
  assert.equal(pan(240)(-300), -300);
});

void test("The rows slow smoothly to a stop at the end of the triangle", () => {
  // Carried a pixel a pixel at first, they come to rest a bend past the start of the
  // slowing, twice the bend's scroll later, and stay there.
  assert.equal(atlas.settle(0, 100), 0);
  assert.equal(atlas.settle(200, 100), 100);
  assert.equal(atlas.settle(400, 100), 100);
  assert.equal(atlas.settle(50, 0), 50);
  assert.ok(Math.abs(atlas.settle(1, 100) - 1) < 1e-3);
  const carried = (/** @type {number} */ x) => atlas.settle(x, 100);
  for (let x = 0; x < 200; x += 2) {
    assert.ok(carried(x + 2) >= carried(x));
  }
  // Its speed falls from one to none without a corner.
  const joined = (/** @type {number} */ x) => (x < 0 ? x : carried(x));
  assert.ok(kink(joined, -100, 300) < 1e-3);
});

void test("The journey reads the point at the focus line from the pinned scroll", () => {
  const ys = [0, 10, 30, 60];
  const us = [500, 520, 540, 560];
  assert.equal(atlas.journey(ys, us, -5), 500);
  assert.equal(atlas.journey(ys, us, 5), 510);
  assert.equal(atlas.journey(ys, us, 20), 530);
  assert.equal(atlas.journey(ys, us, 45), 550);
  assert.equal(atlas.journey(ys, us, 99), 560);
  assert.equal(atlas.journey([], [], 5), 0);
});

void test("Row by row, the spline passes through every row and never overshoots", () => {
  // Row spans grow by two tiles a row, with the grid's extra space from the third.
  const spans = [100, 300, 560, 770, 980, 1190];
  for (let index = 0; index < spans.length - 1; index += 1) {
    assert.equal(atlas.curve(spans, index, 0), spans[index]);
    assert.equal(atlas.curve(spans, index, 1), spans[index + 1]);
    let prior = atlas.curve(spans, index, 0);
    for (let step = 1; step <= 20; step += 1) {
      const value = atlas.curve(spans, index, step / 20);
      assert.ok(value >= prior - 1e-9, `row ${index} step ${step}`);
      prior = value;
    }
  }
  // Its slope runs on across each row's start rather than turning there.
  const at = (/** @type {number} */ x) => atlas.curve(spans, Math.floor(x), x - Math.floor(x));
  const slope = (/** @type {number} */ x) => (at(x + 1e-6) - at(x - 1e-6)) / 2e-6;
  for (const row of [2, 3, 4]) {
    assert.ok(Math.abs(slope(row - 1e-4) - slope(row + 1e-4)) < 0.5, `row ${row}`);
  }
});

void test("A line falls on a row and a share of the way to the next", () => {
  const tops = [0, 100, 200];
  assert.deepEqual({ ...atlas.along(tops, -10) }, { index: 0, through: 0 });
  assert.deepEqual({ ...atlas.along(tops, 50) }, { index: 0, through: 0.5 });
  assert.deepEqual({ ...atlas.along(tops, 100) }, { index: 1, through: 0 });
  assert.deepEqual({ ...atlas.along(tops, 250) }, { index: 2, through: 0 });
  assert.deepEqual({ ...atlas.along([], 50) }, { index: 0, through: 0 });
  assert.equal(atlas.between(10, 20, 0.25), 12.5);
});

void test("A right-to-left scroller pans by what brings a row's left end to its place", () => {
  // Read 383px left of the edge with the scroller already 466px along.
  assert.equal(atlas.panTo(-343, 40, -466, 5584), -849);
  // Already inside: the start. Past the scroller's range: its end.
  assert.equal(atlas.panTo(200, 40, 0, 5584), 0);
  assert.equal(atlas.panTo(-9000, 40, 0, 5584), -5584);
  assert.equal(atlas.panTo(-9000, 40, 0, -3), 0);
});

void test("The tabs show the size whose tile is nearest the zoom, by ratio", () => {
  const tiles = { small: 72, medium: 105, large: 161 };
  assert.equal(atlas.nearestSize(72, tiles), "small");
  assert.equal(atlas.nearestSize(80, tiles), "small");
  assert.equal(atlas.nearestSize(95, tiles), "medium");
  assert.equal(atlas.nearestSize(140, tiles), "large");
});
