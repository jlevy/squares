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

void test("the address names Medium and Large and says nothing for Small", () => {
  assert.equal(atlas.sizeOf(""), "small");
  assert.equal(atlas.sizeOf("?size=small"), "small");
  assert.equal(atlas.sizeOf("?size=large"), "large");
  assert.equal(atlas.sizeOf("?size=medium"), "medium");
  assert.equal(atlas.sizeOf("?size=Large"), "small");
  assert.equal(atlas.sizeOf("?size=huge"), "small");
  assert.equal(atlas.sizeOf("?atlas=triangle&size=large&age=180"), "large");
  assert.equal(atlas.searchForSize("", "large"), "?size=large");
  assert.equal(atlas.searchForSize("?size=large", "medium"), "?size=medium");
  assert.equal(atlas.searchForSize("?size=large", "small"), "");
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

void test("drawing scale URLs default to Fixed, validate values, and retain layout and size", () => {
  for (const search of ["", "?scale=fixed", "?scale=unknown", "?scale=ROW"]) {
    assert.equal(atlas.scaleOf(search), "fixed");
  }
  assert.equal(atlas.scaleOf("?atlas=grid&scale=row&size=large"), "row");
  assert.equal(atlas.scaleOf("?scale=global"), "global");
  assert.equal(
    atlas.searchForScale("?x=1&atlas=grid&size=large", "row"),
    "?x=1&atlas=grid&size=large&scale=row",
  );
  assert.equal(atlas.searchForScale("?x=1&scale=global&size=medium", "fixed"), "?x=1&size=medium");
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
