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
 * @returns {AtlasTrianglePlace}
 */
const place = (n, per) => ({ ...atlas.place(n, per) });

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

void test("where every row fits, row k is line k and starts at the first column", () => {
  for (const [last, per] of /** @type {[number, number][]} */ ([
    [100, 19],
    [324, 35],
  ])) {
    for (let n = 1; n <= last; n += 1) {
      const k = atlas.row(n);
      assert.deepEqual(
        place(n, per),
        { row: k, line: k, column: n - (k - 1) * (k - 1), opens: k > 1 },
        `n = ${n}`,
      );
    }
  }
});

void test("nineteen tiles at eight a line are lines of 8, 8 and 3, ending at the square", () => {
  assert.deepEqual(rowLines(10, 8), [8, 8, 3]);
  const row = lines(100, 8).filter((line) => line[0]?.row === 10);
  // The row reads from its first case at the left edge, two full lines.
  assert.deepEqual(row[0]?.[0], { n: 82, column: 1, row: 10, opens: true });
  assert.deepEqual(
    row[0]?.map(({ column }) => column),
    [1, 2, 3, 4, 5, 6, 7, 8],
  );
  assert.deepEqual(
    row[1]?.map(({ n, column }) => [n, column]),
    [
      [90, 1],
      [91, 2],
      [92, 3],
      [93, 4],
      [94, 5],
      [95, 6],
      [96, 7],
      [97, 8],
    ],
  );
  // The short last line also starts at the left edge.
  assert.deepEqual(
    row[2]?.map(({ n, column }) => [n, column]),
    [
      [98, 1],
      [99, 2],
      [100, 3],
    ],
  );
  assert.deepEqual(row[2]?.at(-1), { n: 100, column: 3, row: 10, opens: false });
});

void test("a row that fits is one line, set from the left", () => {
  // At eight a line rows 1 to 4 fit: 1, 3, 5 and 7 tiles.
  for (let k = 1; k <= 4; k += 1) {
    assert.deepEqual(rowLines(k, 8), [2 * k - 1]);
  }
  assert.deepEqual(
    lines(16, 8)[2]?.map(({ n, column }) => [n, column]),
    [
      [5, 1],
      [6, 2],
      [7, 3],
      [8, 4],
      [9, 5],
    ],
  );
  // A row exactly as long as a line is that line, full.
  assert.deepEqual(rowLines(4, 7), [7]);
  assert.equal(atlas.place(10, 7).column, 1);
});

void test("a row that is a whole number of lines has no short line", () => {
  // Row 5 has nine tiles: three lines of three, under the seven lines of rows 1 to 4.
  assert.deepEqual(rowLines(5, 3), [3, 3, 3]);
  assert.deepEqual(place(17, 3), { row: 5, line: 8, column: 1, opens: true });
  assert.deepEqual(place(25, 3), { row: 5, line: 10, column: 3, opens: false });
});

void test("every perfect square ends its row in the last occupied column, at any width", () => {
  for (let per = 1; per <= 40; per += 1) {
    for (let k = 1; k <= 18; k += 1) {
      assert.equal(
        atlas.place(k * k, per).column,
        ((2 * k - 2) % per) + 1,
        `${k} squared at ${per} a line`,
      );
    }
  }
});

void test("the cases read in order, left to right and top to bottom, one to a place", () => {
  for (const last of [100, 324]) {
    for (let per = 1; per <= 40; per += 1) {
      const found = lines(last, per);
      const reading = found.flatMap((line) => {
        const columns = line.map(({ column }) => column);
        // Left to right along the line, no column taken twice or past the last.
        assert.deepEqual(
          columns,
          [...columns].sort((a, b) => a - b),
        );
        assert.equal(new Set(columns).size, columns.length);
        assert.ok(columns.every((column) => column >= 1 && column <= per));
        return line.map(({ n }) => n);
      });
      assert.deepEqual(
        reading,
        Array.from({ length: last }, (_, index) => index + 1),
        `${last} cases at ${per} a line`,
      );
      // No line is empty, and none holds two rows.
      assert.ok(found.every((line) => new Set(line.map(({ row }) => row)).size === 1));
    }
  }
});

void test("every line starts at the left, including a wrapped row's short last line", () => {
  for (let per = 1; per <= 40; per += 1) {
    for (let k = 1; k <= 18; k += 1) {
      const sizes = rowLines(k, per);
      const tiles = 2 * k - 1;
      assert.equal(
        sizes.reduce((sum, size) => sum + size, 0),
        tiles,
      );
      assert.equal(sizes.length, Math.ceil(tiles / per));
      assert.ok(
        sizes.slice(0, -1).every((size) => size === per),
        `row ${k} at ${per}`,
      );
      assert.ok((sizes.at(-1) ?? 0) >= 1 && (sizes.at(-1) ?? 0) <= per);
    }
    // Every line fills consecutive columns from the first, including short lines.
    /** @type {Map<number, ReturnType<typeof lines>>} */
    const rows = new Map();
    for (const line of lines(324, per)) {
      const k = line[0]?.row ?? 0;
      rows.set(k, [...(rows.get(k) ?? []), line]);
    }
    for (const [k, found] of rows) {
      for (const line of found) {
        assert.equal(line[0]?.column, 1, `row ${k} at ${per}`);
        assert.equal(line.at(-1)?.column, line.length, `row ${k} at ${per}`);
      }
    }
  }
});

void test("the first line of each row after the first opens it, and no other line does", () => {
  for (const per of [8, 19, 26]) {
    for (const line of lines(324, per)) {
      const first = line[0];
      assert.ok(first !== undefined);
      const k = first.row;
      const opens = k > 1 && first.n === (k - 1) * (k - 1) + 1;
      assert.ok(
        line.every((tile) => tile.opens === opens),
        `the line of n = ${first.n}`,
      );
    }
  }
});

void test("the address defaults to Triangle and explicitly names Grid", () => {
  assert.equal(atlas.viewOf(""), "triangle");
  assert.equal(atlas.viewOf("?atlas=triangle"), "triangle");
  assert.equal(atlas.viewOf("?atlas=grid"), "grid");
  assert.equal(atlas.viewOf("?atlas=pyramid"), "triangle");
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

void test("the address names Small and Large and says nothing for Medium", () => {
  assert.equal(atlas.sizeOf(""), "medium");
  assert.equal(atlas.sizeOf("?size=small"), "small");
  assert.equal(atlas.sizeOf("?size=large"), "large");
  assert.equal(atlas.sizeOf("?size=medium"), "medium");
  assert.equal(atlas.sizeOf("?size=Large"), "medium");
  assert.equal(atlas.sizeOf("?size=huge"), "medium");
  assert.equal(atlas.sizeOf("?atlas=triangle&size=large&age=180"), "large");
  assert.equal(atlas.searchForSize("", "large"), "?size=large");
  assert.equal(atlas.searchForSize("?size=large", "medium"), "");
  assert.equal(atlas.searchForSize("?size=large", "small"), "?size=small");
  assert.equal(atlas.searchForSize("", "medium"), "");
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
  assert.equal(search, "?age=180");
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
