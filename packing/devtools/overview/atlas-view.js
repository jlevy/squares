// Input response: the atlas's two views, Grid and Triangle, and the move between them.
//
// The grid sets the cases in reading order, as many to a line as fit. The triangle sets
// them by the grid bound: row k holds the 2k - 1 cases n = (k - 1)^2 + 1 to k^2, the ones
// a square of side k is known to hold. Each row ends at its perfect square, whose
// packing is the k by k grid itself.
//
// Each row retains its non-grid and grid segments on one complete line, with half a
// drawing of extra space between them. All perfect-square endpoints share the right
// edge. A narrow screen pans the triangle without shrinking or breaking its rows.
// Every row reserves the same height and vertical gap. The first retained grid count
// comes from each row's markup, independent of derived drawing variants.
//
// One set of tiles serves both views. The view is an attribute of the atlas block,
// `data-atlas-view`, and the layout is the stylesheet's: in the triangle each tile
// takes its local segment column from custom properties this script writes.
// Viewport capacity follows from the block's width,
// the least cell the stylesheet allows (`--site-atlas-cell-min`) and the gaps. The
// stylesheet places and separates the segment containers. Placement properties change
// only when the answer changes, so changing the view is one attribute. Nothing here
// sizes a tile.
//
// The move is a FLIP: every tile's box is read, the layout is changed, every box is read
// again, and each tile is then animated from where it was to where it is with a
// transform alone, which the compositor runs without laying anything out. One read, one
// write, one read; a tile that neither starts nor ends in the window is not animated.
// The viewport height reveals added rows with the same timing. Page flow moves what
// follows it; changes without a height reveal move following elements with FLIP.
// The tokens `--site-atlas-move-duration` and `--site-atlas-move-easing` time it, and the
// duration is 0ms for a reader who asks for reduced motion, which switches at once.
//
// The view is in the address as `?atlas=grid`, so it can be linked; the triangle, the
// default, has no parameter. A query parameter and not a fragment: `forward.js` sends a
// fragment the overview does not have to the explainer.
//
// The tiles come in three sizes, Small, Medium and Large, chosen by a second strip of
// tabs beside the view tabs, in either view (think-ht8t). The size is an attribute of the
// block too, `data-atlas-size`, and the stylesheet scales a tile by it
// (`--site-atlas-scale`): both views use the same least cell and the same gaps. Small
// fits more tiles to a Grid line and Large fewer (`perLineAt`); Triangle keeps its
// complete rows at the same drawing size. A change of size is a change of layout like a
// change of view, moved the same way. Every explicit choice is preserved in the
// address, including `?size=small`; otherwise size follows the viewport.
//
// Scale, Row by default, changes only a drawing within its reserved tile. Row uses
// its actual enclosing side relative to the logical row's grid side k. Global uses
// the largest actual side among the shown cases. The address names the other choices
// as `?scale=fixed` or `?scale=global`.
//
// An untouched Triangle reached from the top of the page follows the scroll
// (think-apqd). The head bootstrap marks the root `data-site-atlas-follow` when the
// address names no fragment, size, Grid or embedding, and the stylesheet then paints
// Large. The triangle is laid out once, at Large, on a stage the height of the window
// that the browser pins (`position: sticky`) while an empty runway after it scrolls past.
// Each row takes one transform, its pan, its place and its zoom, so a frame lays out and
// draws no tile, and the page's own scroll is never touched. Laying the tiles out again
// restyles all of them (about 300 inherited custom properties each) and redraws every
// drawing, tens of milliseconds a frame; moving the page back under the reader fought
// the browser's own scrolling. The three sizes are points on the zoom, and the tabs
// show the nearest.
//
// The point of the triangle at the focus line, halfway down the window, passes it at the
// page's own speed. The zoom is one smooth curve of it, on a log scale from Large to
// Small or to where the case numbers would pass their least size, beginning where the
// row there first needs it and ending by the time the triangle's bottom reaches the
// stage's. The pan keeps the middle of the window a third of the way along that row
// (`--site-atlas-follow-across`) with its left end in view, rows read between rows on a
// monotone spline and each limit reached on a bend, so going down the top of the
// triangle slides off to the right and the left side, where each row's grid first
// breaks, stays in view. At the bottom the rows slow to a stop while the triangle slides
// to its left edge. All of it is a function of the scroll, the same going up as coming
// down. A sideways wheel or swipe pans it further while the page scrolls, and that
// eases away again back at the top. Nothing is written to the address. Pressing a size
// or view tab, or opening a tile by its fragment, ends the following for the page view
// and returns the triangle to its size's own layout.
//
// The pure functions are published on `globalThis.SiteAtlasView` for the Node tests and
// for `atlas-grid.js`, which places the tiles and calls `mount`.

(() => {
  /** The query parameter that names the view. */
  const PARAM = "atlas";
  /** The query parameter that names the size. */
  const SIZE_PARAM = "size";
  /** The query parameter that names drawing scale within each tile. */
  const SCALE_PARAM = "scale";
  /** The sizes from the smallest. */
  /** @type {readonly AtlasSize[]} */
  const SIZES = ["small", "medium", "large"];
  /** How far down the window the focus line of a following triangle stands. */
  const FOCUS = 0.5;
  /** The share of the way to nothing the reader's own pan eases each frame once they
   * are back above the triangle. */
  const EASE = 0.2;
  /** How wide the bends of the pan are, as a share of the stage's width: where it leaves
   * the right edge, and where a row's left end comes to rest at the left. */
  const PAN_BEND = 0.25;

  /**
   * The triangle's row for case `n`: the k with (k - 1)^2 < n <= k^2.
   * @param {number} n
   * @returns {number}
   */
  function row(n) {
    let k = Math.max(1, Math.ceil(Math.sqrt(n)));
    while ((k - 1) * (k - 1) >= n && k > 1) {
      k -= 1;
    }
    while (k * k < n) {
      k += 1;
    }
    return k;
  }

  /**
   * How many tiles the longest row has when cases 1 to `last` show: row k has 2k - 1.
   * @param {number} last
   * @returns {number}
   */
  function widest(last) {
    return 2 * row(last) - 1;
  }

  /**
   * How many cells of width `least`, separated by `gap`, fit in `width`: at least one,
   * and no more than `most`, the longest row. The last cell needs no gap after it.
   * @param {number} width
   * @param {number} least
   * @param {number} most
   * @param {number} gap
   * @returns {number}
   */
  function perLine(width, least, most, gap = 0) {
    if (!(width > 0) || !(least > 0)) {
      return Math.max(1, most);
    }
    return Math.max(1, Math.min(most, Math.floor((width + gap) / (least + gap))));
  }

  /**
   * How many cells fit at `scale` times Medium's minimum width. Both views budget the
   * same width and gap, so Triangle pans its complete rows at Grid's readable size.
   * @param {number} width
   * @param {number} least
   * @param {number} most
   * @param {number} scale
   * @param {number} gap
   * @returns {number}
   */
  function perLineAt(width, least, most, scale, gap = 0) {
    return perLine(width, least * (scale > 0 ? scale : 1), most, gap);
  }

  /**
   * The width of one tile at `scale`, as the stylesheet works it out: as many cells of
   * the scaled least width as fit in `width`, sharing out what the gaps leave. Not a
   * number when the tokens are unreadable.
   * @param {number} width
   * @param {number} least
   * @param {number} scale
   * @param {number} gap
   * @returns {number}
   */
  function tileAt(width, least, scale, gap = 0) {
    const per = perLineAt(width, least, Number.POSITIVE_INFINITY, scale, gap);
    return Number.isFinite(per) ? (width - (per - 1) * gap) / per : Number.NaN;
  }

  /**
   * The lesser of `a` and `b`, rounded over a `bend` where they come within `bend` of
   * each other, so a curve that runs into a limit turns onto it without a corner. Never
   * more than the true lesser; the plain minimum where `bend` is 0.
   * @param {number} a
   * @param {number} b
   * @param {number} bend
   * @returns {number}
   */
  function smoothMin(a, b, bend) {
    if (!(bend > 0)) {
      return Math.min(a, b);
    }
    const near = Math.max(bend - Math.abs(a - b), 0) / bend;
    return Math.min(a, b) - (near * near * bend) / 4;
  }

  /**
   * The greater of `a` and `b`, rounded as `smoothMin` rounds the lesser.
   * @param {number} a
   * @param {number} b
   * @param {number} bend
   * @returns {number}
   */
  function smoothMax(a, b, bend) {
    return -smoothMin(-a, -b, bend);
  }

  /**
   * The value `through` of the way from `values[index]` to `values[index + 1]` on a
   * monotone cubic through all of them, so a quantity read row by row changes smoothly
   * from one row to the next without overshooting either. Ends hold their value.
   * @param {readonly number[]} values
   * @param {number} index
   * @param {number} through
   * @returns {number}
   */
  function curve(values, index, through) {
    /** @param {number} at */
    const value = (at) => values[Math.min(values.length - 1, Math.max(0, at))] ?? 0;
    const [before, here, next, after] = [-1, 0, 1, 2].map((step) => value(index + step));
    /** @param {number} a @param {number} b @param {number} c */
    const slope = (a, b, c) => {
      const left = b - a;
      const right = c - b;
      if (left * right <= 0) {
        return 0;
      }
      return (
        Math.sign(right) *
        Math.min(Math.abs(left + right) / 2, 3 * Math.min(Math.abs(left), Math.abs(right)))
      );
    };
    const t = through;
    return (
      (2 * t ** 3 - 3 * t ** 2 + 1) * (here ?? 0) +
      (t ** 3 - 2 * t ** 2 + t) * slope(before ?? 0, here ?? 0, next ?? 0) +
      (-2 * t ** 3 + 3 * t ** 2) * (next ?? 0) +
      (t ** 3 - t ** 2) * slope(here ?? 0, next ?? 0, after ?? 0)
    );
  }

  /**
   * The smootherstep of `t`, clamped to 0 and 1: no slope and no bend at either end.
   * @param {number} t
   * @returns {number}
   */
  function smootherstep(t) {
    const x = Math.min(1, Math.max(0, Number.isFinite(t) ? t : t > 0 ? 1 : 0));
    return x * x * x * (x * (6 * x - 15) + 10);
  }

  /**
   * How far a following triangle is zoomed with the point `point` of it at the focus
   * line: one smooth curve on a log scale, from the laid-out size, Large, at `from` to
   * `least` at `to`, starting and stopping without a jolt. Large before `from`.
   * @param {number} point
   * @param {number} from
   * @param {number} to
   * @param {number} least
   * @returns {number}
   */
  function zoomAt(point, from, to, least) {
    if (!(least > 0) || !(to > from)) {
      return 1;
    }
    return Math.exp(Math.log(least) * smootherstep((point - from) / (to - from)));
  }

  /**
   * How far along a road `distance` pixels have carried a traveller who, from the start,
   * slows smoothly to a stop over twice `bend`: the distance itself for a `bend` of 0,
   * and never more than `bend` past the start, where they come to rest.
   * @param {number} distance
   * @param {number} bend
   * @returns {number}
   */
  function settle(distance, bend) {
    if (!(bend > 0)) {
      return Math.max(0, distance);
    }
    const t = Math.min(1, Math.max(0, distance / (2 * bend)));
    // The integral of 1 - smootherstep, over twice the bend: half of it, the bend.
    return 2 * bend * (t - t ** 6 + 3 * t ** 5 - 2.5 * t ** 4);
  }

  /**
   * The point at the focus line after `scrolled` pixels of pinned scroll, read from the
   * journey's pairs `ys` and `us` and held at either end.
   * @param {readonly number[]} ys
   * @param {readonly number[]} us
   * @param {number} scrolled
   * @returns {number}
   */
  function journey(ys, us, scrolled) {
    if (ys.length === 0) {
      return 0;
    }
    let low = 0;
    let high = ys.length - 1;
    if (scrolled <= (ys[0] ?? 0)) {
      return us[0] ?? 0;
    }
    if (scrolled >= (ys[high] ?? 0)) {
      return us[high] ?? 0;
    }
    while (high - low > 1) {
      const middle = (low + high) >> 1;
      if ((ys[middle] ?? 0) <= scrolled) {
        low = middle;
      } else {
        high = middle;
      }
    }
    const y0 = ys[low] ?? 0;
    const y1 = ys[high] ?? y0;
    return between(us[low] ?? 0, us[high] ?? 0, y1 > y0 ? (scrolled - y0) / (y1 - y0) : 0);
  }

  /**
   * Where the left end of a row `width` wide stands from the left edge of a block `room`
   * wide when the middle of the block is `across` of the way along it: never left of
   * the edge, so a row too long for that keeps its left end in view, coming to rest
   * there on a `bend` of pixels.
   * @param {number} room
   * @param {number} width
   * @param {number} across
   * @param {number} [bend]
   * @returns {number}
   */
  function followLeft(room, width, across, bend = PAN_BEND) {
    return smoothMax(0, room / 2 - across * width, bend);
  }

  /**
   * The size whose tile in `tiles` is nearest to `tile`, by ratio: the one the size tabs
   * show while the zoom stands between sizes.
   * @param {number} tile
   * @param {Readonly<Record<AtlasSize, number>>} tiles
   * @returns {AtlasSize}
   */
  function nearestSize(tile, tiles) {
    /** @type {AtlasSize} */
    let best = "small";
    let distance = Number.POSITIVE_INFINITY;
    for (const each of SIZES) {
      const apart = Math.abs(Math.log(tile / tiles[each]));
      if (apart < distance) {
        best = each;
        distance = apart;
      }
    }
    return best;
  }

  /**
   * The value `through` of the way from `from` to `to`.
   * @param {number} from
   * @param {number} to
   * @param {number} through
   * @returns {number}
   */
  function between(from, to, through) {
    return from + (to - from) * through;
  }

  /**
   * Which of the lines whose tops are `tops`, from the top down, `at` falls on, and how
   * far it has gone toward the next, from 0 to 1: the first line above it and the last
   * below it, each with nothing gone.
   * @param {readonly number[]} tops
   * @param {number} at
   * @returns {{ index: number, through: number }}
   */
  function along(tops, at) {
    let index = 0;
    while (index + 1 < tops.length && (tops[index + 1] ?? at) <= at) {
      index += 1;
    }
    const top = tops[index];
    const next = tops[index + 1];
    if (top === undefined || next === undefined || !(next > top)) {
      return { index, through: 0 };
    }
    return { index, through: Math.min(1, Math.max(0, (at - top) / (next - top))) };
  }

  /**
   * The position of a right-to-left scroller, 0 at its start and negative down to
   * `-range`, that brings `left`, read with the scroller at `scrolled`, to `edge`: 0
   * while it already stands inside, leaving its start on a `bend` of pixels.
   * @param {number} left
   * @param {number} edge
   * @param {number} scrolled
   * @param {number} range
   * @param {number} [bend]
   * @returns {number}
   */
  function panTo(left, edge, scrolled, range, bend = 0) {
    return Math.min(0, Math.max(Math.min(0, -range), smoothMin(0, left + scrolled - edge, bend)));
  }

  /**
   * Where case `n` stands in a complete Triangle row, right aligned in `per`
   * canvas columns. Viewport capacity controls drawing scale separately. A smaller
   * canvas request still holds the entire row. Segments keep their local columns,
   * and mixed rows retain the extra horizontal separator before the grid suffix.
   * @param {number} n
   * @param {number} per
   * @param {AtlasGridStarts} starts first retained grid count by one-based row k
   * @returns {AtlasTrianglePlace}
   */
  function place(n, per, starts = {}) {
    const k = row(n);
    const count = 2 * k - 1;
    const columns = Math.max(count, Math.floor(per));
    const prefix = starts[k] === undefined ? count : starts[k] - (k - 1) ** 2 - 1;
    const at = n - (k - 1) ** 2;
    const inGrid = at > prefix;
    return {
      row: k,
      line: k,
      column: columns - count + at,
      opens: k > 1,
      gap: inGrid && prefix > 0,
      segmentLine: 1,
      segmentColumn: inGrid ? at - prefix : at,
    };
  }

  /**
   * The view a query string asks for: Grid when named, else the default Triangle.
   * @param {string} search
   * @returns {AtlasView}
   */
  function viewOf(search) {
    return new URLSearchParams(search).get(PARAM) === "grid" ? "grid" : "triangle";
  }

  /**
   * `search` with the view written into it: the parameter for Grid, none for the
   * default Triangle, and every other parameter kept in its place.
   * @param {string} search
   * @param {AtlasView} view
   * @returns {string}
   */
  function searchFor(search, view) {
    return searchWith(search, PARAM, view === "grid" ? "grid" : null);
  }

  /**
   * The size a word names: medium or large, else small.
   * @param {string | null | undefined} word
   * @returns {AtlasSize}
   */
  function asSize(word) {
    return word === "medium" || word === "large" ? word : "small";
  }

  /**
   * The size a query string asks for: medium or large when it says so, else small.
   * @param {string} search
   * @returns {AtlasSize}
   */
  function sizeOf(search) {
    return asSize(new URLSearchParams(search).get(SIZE_PARAM));
  }

  /**
   * `search` with an explicit size, including small so a wide-screen reload keeps
   * the reader's choice, and every other parameter kept in its place.
   * @param {string} search
   * @param {AtlasSize} size
   * @returns {string}
   */
  function searchForSize(search, size) {
    return searchWith(search, SIZE_PARAM, size);
  }

  /**
   * A drawing scale name: Fixed or Global when named, otherwise the default Row.
   * @param {string | null | undefined} word
   * @returns {AtlasScale}
   */
  function asScale(word) {
    return word === "fixed" || word === "global" ? word : "row";
  }

  /** @param {string} search @returns {AtlasScale} */
  function scaleOf(search) {
    return asScale(new URLSearchParams(search).get(SCALE_PARAM));
  }

  /** @param {string} search @param {AtlasScale} scale @returns {string} */
  function searchForScale(search, scale) {
    return searchWith(search, SCALE_PARAM, scale === "row" ? null : scale);
  }

  /**
   * Actual enclosing side relative to its logical row's k-by-k grid side, in either
   * layout. Responsive Grid lines do not change the mathematical row.
   * @param {number} n @param {number} side @returns {number}
   */
  function rowRatio(n, side) {
    return side / row(n);
  }

  /** @param {readonly number[]} sides @returns {number} */
  function largestSide(sides) {
    return Math.max(0, ...sides);
  }

  /**
   * `search` with parameter `name` set to `value`, or removed where `value` is null, and
   * every other parameter kept in its place.
   * @param {string} search
   * @param {string} name
   * @param {string | null} value
   * @returns {string}
   */
  function searchWith(search, name, value) {
    const params = new URLSearchParams(search);
    if (value === null) {
      params.delete(name);
    } else {
      params.set(name, value);
    }
    const text = params.toString();
    return text === "" ? "" : `?${text}`;
  }

  /**
   * The tab a key moves the focus to, from tab `from` of `count`: Right and Left to the
   * next and the previous, wrapping, and Home and End to the ends; -1 for any other key.
   * @param {string} key
   * @param {number} from
   * @param {number} count
   * @returns {number}
   */
  function stepTo(key, from, count) {
    if (count < 1 || from < 0 || from >= count) {
      return -1;
    }
    /** @type {Record<string, number>} */
    const to = {
      ArrowRight: (from + 1) % count,
      ArrowLeft: (from + count - 1) % count,
      Home: 0,
      End: count - 1,
    };
    return to[key] ?? -1;
  }

  /**
   * A length token in pixels: `1.5rem` at a root size of `rootPx`, or `24px`. Not a
   * number for anything else, which leaves a line as long as the longest row.
   * @param {string} text
   * @param {number} rootPx
   * @returns {number}
   */
  function lengthPx(text, rootPx) {
    const found = /^\s*(\d*\.?\d+)(rem|px)\s*$/.exec(text);
    if (found === null) {
      return Number.NaN;
    }
    return Number(found[1]) * (found[2] === "rem" ? rootPx : 1);
  }

  /**
   * A time token in milliseconds: `360ms` or `0.36s`. Anything else is 0, no move.
   * @param {string} text
   * @returns {number}
   */
  function milliseconds(text) {
    const found = /^\s*(\d*\.?\d+)(ms|s)\s*$/.exec(text);
    if (found === null) {
      return 0;
    }
    return Number(found[1]) * (found[2] === "s" ? 1000 : 1);
  }

  /**
   * The transform that sets a tile's drawing back where it was: `first` and `last` are
   * the drawing's box before and after the layout changed, and `holder` the tile's box
   * after. The tile is scaled about its own top left corner (its `transform-origin`), by
   * one factor both ways since a drawing is square, and moved so the drawing lands on
   * `first`.
   * @param {AtlasBox} first
   * @param {AtlasBox} last
   * @param {AtlasBox} holder
   * @returns {AtlasMove}
   */
  function moveFrom(first, last, holder) {
    const scale = last.width > 0 ? first.width / last.width : 1;
    return {
      x: first.left - holder.left - scale * (last.left - holder.left),
      y: first.top - holder.top - scale * (last.top - holder.top),
      scale,
    };
  }

  /**
   * Whether a move is too small to see: under half a pixel either way and under a
   * hundredth in size.
   * @param {AtlasMove} move
   * @returns {boolean}
   */
  function still(move) {
    return Math.abs(move.x) < 0.5 && Math.abs(move.y) < 0.5 && Math.abs(move.scale - 1) < 0.01;
  }

  /**
   * The buttons of a tablist, in order.
   * @param {HTMLElement} list
   * @returns {HTMLButtonElement[]}
   */
  function tabsOf(list) {
    return [...list.querySelectorAll('[role="tab"]')].filter(
      (tab) => tab instanceof HTMLButtonElement,
    );
  }

  /**
   * Make a tablist act: a press of a tab selects it, and the tabs are one stop in the
   * page's tab order, the arrow keys, Home and End moving between them and selecting the
   * tab the focus lands on at once, since showing a view or a size costs nothing.
   * @param {HTMLElement} list
   * @param {(tab: HTMLButtonElement) => void} select
   */
  function wire(list, select) {
    const buttons = tabsOf(list);
    list.addEventListener("click", (event) => {
      const tab = event.target instanceof Element ? event.target.closest('[role="tab"]') : null;
      if (tab instanceof HTMLButtonElement && list.contains(tab)) {
        select(tab);
      }
    });
    list.addEventListener("keydown", (event) => {
      const focused = document.activeElement;
      const from = focused instanceof HTMLButtonElement ? buttons.indexOf(focused) : -1;
      if (from < 0 || event.altKey || event.ctrlKey || event.metaKey) {
        return;
      }
      const next = buttons[stepTo(event.key, from, buttons.length)];
      if (next === undefined) {
        return;
      }
      event.preventDefault();
      next.focus();
      select(next);
    });
  }

  /**
   * Wire the view tabs and the size tabs of one atlas block. `cells` holds the tiles,
   * which `atlas-grid.js` places; `tabs` and `sizes` are the tablists the page ships.
   * @param {SiteAtlasParts} parts
   * @returns {SiteAtlasViews}
   */
  function mount({
    block,
    cells,
    tabs,
    sizes,
    scales = null,
    drawings = null,
    scoped = false,
    onDrawingChange,
  }) {
    const buttons = tabs === null ? [] : tabsOf(tabs);
    const sizeButtons = sizes === null ? [] : tabsOf(sizes);
    const scaleButtons = scales === null ? [] : tabsOf(scales);
    const drawingButtons = drawings === null ? [] : tabsOf(drawings);
    /** @type {Record<number, number>} */
    const starts = {};
    for (const tile of cells.querySelectorAll("[data-atlas-grid-from]")) {
      const n = Number(tile.getAttribute("data-atlas-n"));
      starts[row(n)] = n;
    }
    /** The tiles a line holds and the last case shown, as last arranged. */
    let arranged = "";
    /** The border-box width consumed by the latest arrangement. */
    let priorWidth = 0;
    /** @type {Animation[]} */
    let running = [];
    /** Whether the size and the pan follow the page's scroll, until the reader takes over. */
    let following = false;
    const sizeQuery = new URLSearchParams(location.search).get(SIZE_PARAM);
    const namedSize = sizeQuery === "small" || sizeQuery === "medium" || sizeQuery === "large";
    let explicitSize = namedSize || block.hasAttribute("data-atlas-size-explicit");
    // Keep this media query in step with site.css's first-paint default (think-mp47).
    const wideScreen = window.matchMedia("(min-width: 75rem)");
    /** @returns {AtlasSize} */
    const automaticSize = () => (wideScreen.matches ? "medium" : "small");

    /** @returns {AtlasView} */
    const view = () => (block.dataset.atlasView === "triangle" ? "triangle" : "grid");
    /** @returns {AtlasSize} */
    const size = () => asSize(block.dataset.atlasSize);
    /** @returns {AtlasScale} */
    const drawingScale = () => asScale(block.dataset.atlasScale);

    // Dedicated and homepage row containers share the same placement and FLIP.
    // Visibility is controlled by persistent wrappers or boundary cells, never clones.
    const shown = () =>
      [...cells.querySelectorAll(".site-atlas-cell")]
        .filter((tile) => tile instanceof HTMLElement)
        .filter((tile) => tile.closest("[hidden]") === null);

    // Write each tile's line and column for the tiles a line now holds. Only the
    // triangle reads them, but they are kept current in the grid too, so a change of
    // view writes nothing: a tile's properties are inherited by every line of its
    // drawing, and writing them restyles all of those. Nothing is written while
    // neither the tiles a line holds nor the last case shown has changed. The size's
    // scale is the stylesheet's (`--site-atlas-scale`), read as the tiles are arranged.
    const arrange = () => {
      const root = Number.parseFloat(getComputedStyle(document.documentElement).fontSize);
      const style = getComputedStyle(cells);
      const least = lengthPx(style.getPropertyValue("--site-atlas-cell-min"), root);
      const gap = lengthPx(style.getPropertyValue("--site-atlas-reference-gap"), root);
      const scale = Number.parseFloat(style.getPropertyValue("--site-atlas-scale"));
      const width = cells.getBoundingClientRect().width;
      priorWidth = width;
      const capacity = perLineAt(width, least, Number.POSITIVE_INFINITY, scale, gap);
      const tiles = shown();
      const last = Number(tiles.at(-1)?.dataset.atlasN);
      if (!(last >= 1)) {
        return;
      }
      const per = Number.isFinite(capacity) ? capacity : widest(last) + 1;
      const largest = largestSide(tiles.map((tile) => Number(tile.dataset.atlasSide)));
      const key = `${per}:${tiles.map((tile) => tile.dataset.atlasN).join(":")}:${largest}`;
      if (key === arranged) {
        return;
      }
      arranged = key;
      cells.style.setProperty("--site-atlas-per-line", String(per));
      cells.style.setProperty("--site-atlas-global-side", String(largest));
      for (const tile of tiles) {
        const at = place(Number(tile.dataset.atlasN), widest(last), starts);
        tile.style.setProperty("--site-atlas-line", String(at.segmentLine));
        tile.style.setProperty("--site-atlas-column", String(at.segmentColumn));
      }
    };

    // What stands after the tiles in the page's flow, which a change in their height
    // carries with it: the rest of the block, then every later sibling of the block and
    // of each of its ancestors.
    const followers = () => {
      /** @type {HTMLElement[]} */
      const found = [];
      /** @param {Element | null} from */
      const after = (from) => {
        for (let next = from; next !== null; next = next.nextElementSibling) {
          if (next instanceof HTMLElement) {
            found.push(next);
          }
        }
      };
      after(cells.nextElementSibling);
      for (
        let at = block;
        at.parentElement !== null && at !== document.body;
        at = at.parentElement
      ) {
        after(at.nextElementSibling);
      }
      return found;
    };

    /**
     * Every shown tile's box and its drawing's, and the box of each element after the
     * tiles, as laid out and transformed now.
     */
    const measure = () => {
      /** @type {Map<HTMLElement, { tile: DOMRect, drawing: AtlasBox }>} */
      const tiles = new Map();
      const visible = shown();
      const largest = largestSide(visible.map((tile) => Number(tile.dataset.atlasSide)));
      const mode = drawingScale();
      for (const tile of visible) {
        const drawing = tile.firstElementChild;
        if (drawing !== null) {
          const drawn = drawing.getBoundingClientRect();
          const side = Number(tile.dataset.atlasSide);
          const ratio =
            mode === "row"
              ? rowRatio(Number(tile.dataset.atlasN), side)
              : mode === "global"
                ? side / largest
                : 1;
          const width = drawn.width / ratio;
          const origin = getComputedStyle(drawing)
            .transformOrigin.split(" ")
            .map(Number.parseFloat);
          // FLIP moves the reserved slot, not the scaled square inside it. A scale
          // choice therefore never scales the tile's number or changes its position.
          tiles.set(tile, {
            tile: tile.getBoundingClientRect(),
            drawing: {
              left: drawn.left - (origin[0] ?? width / 2) * (1 - ratio),
              top: drawn.top - (origin[1] ?? width / 2) * (1 - ratio),
              width,
            },
          });
        }
      }
      /** @type {Map<HTMLElement, DOMRect>} */
      const rest = new Map();
      for (const follower of followers()) {
        rest.set(follower, follower.getBoundingClientRect());
      }
      return { tiles, rest, height: cells.getBoundingClientRect().height, scroll: window.scrollY };
    };

    const stop = () => {
      for (const animation of running) {
        animation.cancel();
      }
      running = [];
    };

    // Change the layout with `mutate` and move every tile from where it was to where it
    // is: one read of every box, the change, one read more, then one animation a tile,
    // on `transform` alone. A tile the change shows for the first time fades in, and
    // what follows the tiles moves with them. A move already under way is read where it
    // has got to and stopped, so a second change starts from what the reader sees. A
    // change that scrolls the page, as collapsing a long grid does, is not moved: the
    // window has jumped, and nothing is where the reader last saw it.
    /** @param {() => void} mutate */
    const change = (mutate) => {
      const style = getComputedStyle(block);
      const duration = milliseconds(style.getPropertyValue("--site-atlas-move-duration"));
      const easing = style.getPropertyValue("--site-atlas-move-easing").trim() || "ease-out";
      const before = duration > 0 ? measure() : null;
      stop();
      mutate();
      arrange();
      if (before === null) {
        return;
      }
      const now = measure();
      if (now.scroll !== before.scroll) {
        return;
      }
      const edge = window.innerHeight;
      /** @param {DOMRect} box */
      const inView = (box) => box.bottom > 0 && box.top < edge;
      /** @type {Keyframe[]} */
      const arrive = [{ opacity: 0 }, { opacity: 1 }];
      /** @type {KeyframeAnimationOptions} */
      const timing = { duration, easing };
      // What appears under the tiles, the triangle's key, waits until they have all but
      // landed, since they cross where it stands on their way: it is unseen through the
      // first three fifths of the move and fades in over the last two.
      /** @type {KeyframeAnimationOptions} */
      const late = { duration: duration * 0.4, delay: duration * 0.6, easing, fill: "backwards" };
      /** @type {[HTMLElement, Keyframe[], KeyframeAnimationOptions][]} */
      const moves = [];
      for (const [tile, last] of now.tiles) {
        const first = before.tiles.get(tile);
        if (first === undefined || first.tile.width === 0) {
          if (inView(last.tile)) {
            moves.push([tile, arrive, timing]);
          }
          continue;
        }
        if (!inView(first.tile) && !inView(last.tile)) {
          continue;
        }
        const move = moveFrom(first.drawing, last.drawing, last.tile);
        if (!still(move)) {
          moves.push([
            tile,
            [
              { transform: `translate(${move.x}px, ${move.y}px) scale(${move.scale})` },
              { transform: "translate(0px, 0px) scale(1)" },
            ],
            timing,
          ]);
        }
      }
      // The viewport reveals complete, already prepared rows as its height grows.
      // Flow carries following content with this animation, so it needs no second FLIP.
      const changesHeight = Math.abs(now.height - before.height) >= 0.5;
      if (changesHeight) {
        moves.push([
          cells,
          [
            { height: `${before.height}px`, overflowY: "hidden", alignContent: "start" },
            { height: `${now.height}px`, overflowY: "hidden", alignContent: "start" },
          ],
          timing,
        ]);
      }
      for (const [follower, last] of changesHeight ? [] : now.rest) {
        const first = before.rest.get(follower);
        if (last.height === 0 || first === undefined) {
          continue;
        }
        if (first.height === 0) {
          if (inView(last)) {
            moves.push([follower, arrive, late]);
          }
          continue;
        }
        const x = first.left - last.left;
        const y = first.top - last.top;
        if ((inView(first) || inView(last)) && !still({ x, y, scale: 1 })) {
          moves.push([
            follower,
            [{ transform: `translate(${x}px, ${y}px)` }, { transform: "translate(0px, 0px)" }],
            timing,
          ]);
        }
      }
      for (const [element, frames, options] of moves) {
        const animation = element.animate(frames, options);
        running.push(animation);
      }
      const batch = running;
      const done = () => {
        if (running === batch) {
          running = [];
        }
      };
      Promise.allSettled(batch.map((animation) => animation.finished)).then(done, done);
    };

    const labelPanel = () => {
      cells.setAttribute(
        "aria-labelledby",
        [...buttons, ...drawingButtons]
          .filter((tab) => tab.getAttribute("aria-selected") === "true")
          .map((tab) => tab.id)
          .join(" "),
      );
    };

    /** @param {AtlasView} current */
    const mark = (current) => {
      block.dataset.atlasView = current;
      if (!scoped) {
        document.documentElement.dataset.siteAtlasView = current;
      }
      for (const tab of buttons) {
        const on = tab.dataset.atlasTab === current;
        tab.setAttribute("aria-selected", String(on));
        tab.tabIndex = on ? 0 : -1;
      }
      labelPanel();
    };

    /** @param {AtlasSize} current */
    const showSize = (current) => {
      for (const tab of sizeButtons) {
        const on = tab.dataset.atlasSizeTab === current;
        tab.setAttribute("aria-selected", String(on));
        tab.tabIndex = on ? 0 : -1;
      }
    };

    /** @param {AtlasSize} current */
    const markSize = (current) => {
      block.dataset.atlasSize = current;
      block.toggleAttribute("data-atlas-size-explicit", explicitSize);
      if (!scoped) {
        if (explicitSize) {
          document.documentElement.dataset.siteAtlasSize = current;
        } else {
          delete document.documentElement.dataset.siteAtlasSize;
        }
      }
      showSize(current);
    };

    /** @param {AtlasScale} current */
    const markScale = (current) => {
      block.dataset.atlasScale = current;
      if (!scoped) {
        document.documentElement.dataset.siteAtlasScale = current;
      }
      for (const tab of scaleButtons) {
        const on = tab.dataset.atlasScaleTab === current;
        tab.setAttribute("aria-selected", String(on));
        tab.tabIndex = on ? 0 : -1;
      }
    };

    /** @param {string} search */
    const readdress = (search) => {
      history.replaceState(history.state, "", `${location.pathname}${search}${location.hash}`);
    };

    /** The empty box after the stage whose height is the scroll it stays pinned for. */
    const runway = document.createElement("div");
    runway.className = "site-atlas-runway";
    runway.setAttribute("aria-hidden", "true");
    // A size's own layout, which a chosen size and Grid always take: the stage, its
    // runway and the rows' transforms all go, and the scroller keeps the pan.
    const unzoom = () => {
      if (!block.hasAttribute("data-atlas-zoom")) {
        return;
      }
      delete block.dataset.atlasZoom;
      cells.style.removeProperty("height");
      runway.remove();
      for (const line of cells.querySelectorAll(".site-atlas-row")) {
        if (line instanceof HTMLElement) {
          line.style.removeProperty("transform");
        }
      }
      cells.scrollLeft = panned;
    };

    // The reader has chosen how the atlas stands: following ends for the page view. The
    // attribute stays to keep the stylesheet's first-paint defaults off the block.
    const quit = () => {
      if (following) {
        following = false;
        block.dataset.atlasFollow = "held";
      }
    };
    // A jump to a tile ends it at once, so the tile is found where its layout puts it.
    const hold = () => {
      quit();
      unzoom();
    };

    /** @param {AtlasView} next */
    const select = (next) => {
      if (next === view()) {
        return;
      }
      quit();
      change(() => {
        unzoom();
        mark(next);
      });
      if (!scoped) {
        readdress(searchFor(location.search, next));
      }
    };

    /** @param {AtlasSize} next */
    const selectSize = (next) => {
      explicitSize = true;
      quit();
      if (next === size() && !block.hasAttribute("data-atlas-zoom")) {
        markSize(next);
      } else {
        change(() => {
          unzoom();
          markSize(next);
        });
      }
      readdress(searchForSize(location.search, next));
    };

    /** @param {AtlasScale} next */
    const selectScale = (next) => {
      if (next === drawingScale()) {
        return;
      }
      change(() => markScale(next));
      if (!scoped) {
        readdress(searchForScale(location.search, next));
      }
    };

    /** Switch the existing images without persisting a mode.
     * @param {"regularized" | "original"} next */
    const selectDrawing = (next) => {
      if (next === block.dataset.atlasDrawing) {
        return;
      }
      change(() => {
        block.dataset.atlasDrawing = next;
        for (const image of cells.querySelectorAll("img[data-atlas-original-src]")) {
          const tile = image.closest(".site-atlas-cell");
          if (!(image instanceof HTMLImageElement) || !(tile instanceof HTMLElement)) {
            continue;
          }
          const original = next === "original";
          const source = original
            ? image.dataset.atlasOriginalSrc
            : image.dataset.atlasRegularizedSrc;
          const side = original
            ? image.dataset.atlasOriginalSide
            : image.dataset.atlasRegularizedSide;
          const credit = original
            ? image.dataset.atlasOriginalCredit
            : image.dataset.atlasRegularizedCredit;
          if (!source || !side || !credit) {
            continue;
          }
          image.src = source;
          image.alt = `${original ? "Original" : "Regularized"} packing of ${tile.dataset.atlasN} unit squares`;
          image.title = credit;
          delete image.dataset.atlasImageState;
          tile.dataset.atlasSide = side;
          tile.style.setProperty("--site-atlas-side", side);
          tile.toggleAttribute(
            "data-atlas-row-smaller",
            Number(side) < row(Number(tile.dataset.atlasN)),
          );
        }
        for (const tab of drawingButtons) {
          const on = tab.dataset.atlasDrawingTab === next;
          tab.setAttribute("aria-selected", String(on));
          tab.tabIndex = on ? 0 : -1;
        }
        labelPanel();
      });
      onDrawingChange?.();
    };

    if (tabs !== null) {
      cells.id = tabs.dataset.atlasPanel ?? "";
      cells.setAttribute("role", "tabpanel");
      wire(tabs, (tab) => select(tab.dataset.atlasTab === "triangle" ? "triangle" : "grid"));
    }
    mark(scoped ? view() : viewOf(location.search));
    following =
      document.documentElement.hasAttribute("data-site-atlas-follow") &&
      !explicitSize &&
      view() === "triangle";
    if (following) {
      // Both at once, so the triangle goes from its first paint to its zoomed drawing
      // in one restyle.
      block.dataset.atlasFollow = "scroll";
      block.dataset.atlasZoom = "";
    }
    markSize(
      namedSize ? asSize(sizeQuery) : explicitSize ? size() : following ? "large" : automaticSize(),
    );
    markScale(scoped ? drawingScale() : scaleOf(location.search));
    if (sizes !== null) {
      wire(sizes, (tab) => selectSize(asSize(tab.dataset.atlasSizeTab)));
    }
    // The font-ready getter can flush style. Read it after startup attributes are
    // settled, alongside arrangement reads and before any tile placement writes.
    const fontsReady = document.fonts.ready;
    arrange();
    // An untouched default follows the viewport without a transition. Explicit
    // query choices and even a click on the current automatic size stay fixed, and so
    // does a size that follows, or once followed, the scroll.
    wideScreen.addEventListener("change", () => {
      if (!explicitSize && !block.hasAttribute("data-atlas-follow")) {
        stop();
        markSize(automaticSize());
        arrange();
      }
    });

    if (scales !== null) {
      wire(scales, (tab) => selectScale(asScale(tab.dataset.atlasScaleTab)));
    }
    if (drawings !== null) {
      wire(drawings, (tab) =>
        selectDrawing(tab.dataset.atlasDrawingTab === "original" ? "original" : "regularized"),
      );
      drawings.hidden = false;
    }

    // The tiles a line holds follow the block's width. A resize is settled on the next
    // frame, at most once a frame, and placed without a move: the window is already
    // moving everything.
    if ("ResizeObserver" in window) {
      let waiting = false;
      new ResizeObserver((entries) => {
        const width =
          entries[0]?.borderBoxSize[0]?.inlineSize ?? cells.getBoundingClientRect().width;
        if (width === priorWidth) {
          return;
        }
        priorWidth = width;
        if (!waiting) {
          waiting = true;
          requestAnimationFrame(() => {
            waiting = false;
            arrange();
          });
        }
      }).observe(cells);
    }

    // The tiles of the three sizes at the block's width now, as `arrange` works them
    // out: Small's share of Large's bounds the zoom, and the nearest names the size the
    // tabs show.
    const presets = () => {
      const root = Number.parseFloat(getComputedStyle(document.documentElement).fontSize);
      const style = getComputedStyle(cells);
      const least = lengthPx(style.getPropertyValue("--site-atlas-cell-min"), root);
      const gap = lengthPx(style.getPropertyValue("--site-atlas-reference-gap"), root);
      const width = cells.getBoundingClientRect().width;
      /** @type {Record<AtlasSize, number>} */
      const tiles = { small: Number.NaN, medium: Number.NaN, large: Number.NaN };
      for (const each of SIZES) {
        const scale = Number.parseFloat(style.getPropertyValue(`--site-atlas-scale-${each}`));
        tiles[each] = tileAt(width, least, scale, gap);
      }
      return tiles;
    };

    // The triangle as laid out, before any zoom, and the journey the page's scroll takes
    // through it. `tops` and `spans` are each shown row's top below the box's and the
    // span of its tiles; `offset` is where the box stands below the block's top before
    // it is pinned. `ys` and `us` pair the scroll since the box was pinned with the
    // point of the triangle then at the focus line, up to `end`, where the triangle's
    // bottom reaches the stage's. The rows slow to a stop over `stop` either side of
    // `end`, while the triangle pans to its left edge, and the stage stays pinned for
    // the `runway` past `end` that this takes.
    let laid = {
      /** @type {HTMLElement[]} */
      rows: [],
      /** @type {number[]} */
      tops: [],
      /** @type {number[]} */
      spans: [],
      height: 0,
      offset: 0,
      stage: 0,
      focus: 0,
      /** @type {Record<AtlasSize, number>} */
      tiles: { small: Number.NaN, medium: Number.NaN, large: Number.NaN },
      least: 1,
      across: 1 / 3,
      from: Number.POSITIVE_INFINITY,
      to: Number.POSITIVE_INFINITY,
      /** @type {number[]} */
      ys: [],
      /** @type {number[]} */
      us: [],
      end: 0,
      stop: 0,
      runway: 0,
    };
    /** The span of the row at `point`, between rows on a monotone spline. */
    const spanAt = (/** @type {number} */ point) => {
      const at = along(laid.tops, point);
      return curve(laid.spans, at.index, at.through);
    };
    /** The zoom at `point`: one smooth curve from Large down to the least zoom. */
    const zoomOf = (/** @type {number} */ point) => zoomAt(point, laid.from, laid.to, laid.least);

    const lay = () => {
      for (const line of laid.rows) {
        line.style.removeProperty("transform");
      }
      const box = cells.getBoundingClientRect();
      /** @type {HTMLElement[]} */
      const rows = [];
      /** @type {number[]} */
      const tops = [];
      /** @type {number[]} */
      const spans = [];
      let height = 0;
      for (const line of cells.querySelectorAll(".site-atlas-row")) {
        if (!(line instanceof HTMLElement) || line.closest("[hidden]") !== null) {
          continue;
        }
        let left = Number.POSITIVE_INFINITY;
        let right = Number.NEGATIVE_INFINITY;
        for (const segment of line.querySelectorAll(".site-atlas-segment")) {
          const drawn = segment.getBoundingClientRect();
          if (drawn.width > 0) {
            left = Math.min(left, drawn.left);
            right = Math.max(right, drawn.right);
          }
        }
        if (left < right) {
          const drawn = line.getBoundingClientRect();
          rows.push(line);
          tops.push(drawn.top - box.top);
          spans.push(right - left);
          height = Math.max(height, drawn.bottom - box.top);
        }
      }
      const style = getComputedStyle(block);
      const across = Number.parseFloat(style.getPropertyValue("--site-atlas-follow-across"));
      const root = Number.parseFloat(getComputedStyle(document.documentElement).fontSize);
      const number = lengthPx(style.getPropertyValue("--site-atlas-follow-number"), root);
      const legible = lengthPx(style.getPropertyValue("--site-atlas-follow-number-least"), root);
      const tiles = presets();
      const controls = cells.previousElementSibling;
      const above =
        controls instanceof HTMLElement
          ? controls.getBoundingClientRect().bottom +
            Number.parseFloat(getComputedStyle(controls).marginBlockEnd || "0") -
            block.getBoundingClientRect().top
          : 0;
      laid = {
        ...laid,
        rows,
        tops,
        spans,
        height,
        offset: above,
        stage: window.innerHeight,
        focus: window.innerHeight * FOCUS,
        tiles,
        least: Math.min(1, Math.max(tiles.small / tiles.large, legible / number || 0)),
        across: across > 0 ? across : 1 / 3,
      };
      // The zoom runs from the first point where the row at the focus line would need
      // it, framed a third along with its left end in view, to the first point where it
      // would need the least zoom; past that, the triangle pans.
      const room = cells.clientWidth;
      const fits = (/** @type {number} */ point) => room / (2 * laid.across * spanAt(point));
      let from = Number.POSITIVE_INFINITY;
      let to = height;
      for (let point = 0; point <= height; point += 4) {
        const fit = fits(point);
        if (fit < 1 && !Number.isFinite(from)) {
          from = point;
        }
        if (fit <= laid.least) {
          to = point;
          break;
        }
      }
      // The zoom reaches its least by the time the triangle's bottom reaches the stage's,
      // however wide the window, so the slide along the left is always at that zoom.
      const last = height - (laid.stage - laid.focus) / laid.least;
      laid.from = Math.min(from, last - 1);
      laid.to = Math.max(Math.min(to, last), laid.from + 1);
      // While pinned, the point at the focus line moves at the page's own speed on the
      // screen: a pixel of scroll moves it a pixel divided by the zoom.
      /** @type {number[]} */
      const ys = [0];
      /** @type {number[]} */
      const us = [laid.focus];
      let point = laid.focus;
      let scrolled = 0;
      while (point < height && laid.focus + (height - point) * zoomOf(point) > laid.stage) {
        scrolled += zoomOf(point + 1) * 2;
        point += 2;
        ys.push(scrolled);
        us.push(point);
      }
      laid.ys = ys;
      laid.us = us;
      laid.end = scrolled;
      laid.stop = Math.min(laid.stage / 4, scrolled / 2);
      laid.runway = laid.stop + laid.stage / 3;
      cells.style.height = `${laid.stage}px`;
      // The stage stays pinned while this runway passes: content of the block after the
      // stage, since a sticky box keeps within its block's content.
      runway.style.blockSize = `${laid.end + laid.runway}px`;
      if (!runway.isConnected) {
        cells.after(runway);
      }
    };

    // One reading a frame, however many scrolls ask for it.
    let waiting = false;
    const schedule = () => {
      if (waiting) {
        return;
      }
      waiting = true;
      requestAnimationFrame(() => {
        waiting = false;
        follow();
      });
    };
    /** The last reading, which the browser tests read from the block. */
    const reading = { scrolled: 0, point: 0, line: 0, zoom: 1, pan: 0, nudge: 0, end: 0 };
    block.atlasFollow = reading;
    /** How far the reader has panned the triangle themselves, on top of the framing. */
    let nudge = 0;
    /** The pan last drawn, as a right-to-left scroller would read it: 0 at the right. */
    let panned = 0;
    // Draw the triangle for the page's scroll. Before the stage is pinned, the focus line
    // rises with the page; while pinned, the point at it comes from the journey; after,
    // everything holds its last reading and the page carries the stage away. Each row
    // takes one transform, its zoom about the focus line and the pan, so nothing is laid
    // out again and the page's own scroll is never touched.
    const follow = () => {
      if (!following || view() !== "triangle") {
        return;
      }
      if (laid.rows.length === 0) {
        lay();
      }
      if (laid.rows.length === 0) {
        return;
      }
      // A focused tile the browser scrolled into view moves the pan, not the box.
      if (cells.scrollTop !== 0) {
        cells.scrollTop = 0;
      }
      if (cells.scrollLeft !== 0) {
        nudge += cells.scrollLeft;
        cells.scrollLeft = 0;
      }
      const scrolled = -(block.getBoundingClientRect().top + laid.offset);
      // The rows come to rest smoothly: from `stop` before the end of the journey, the
      // scroll carries them less and less, and none past `stop` after it.
      const slowing = laid.end - laid.stop;
      const pinned =
        scrolled <= slowing
          ? Math.max(scrolled, 0)
          : slowing + settle(scrolled - slowing, laid.stop);
      const point = scrolled <= 0 ? laid.focus + scrolled : journey(laid.ys, laid.us, pinned);
      const line = laid.focus + Math.min(0, scrolled);
      const zoom = zoomOf(point);
      const room = cells.clientWidth;
      const width = spanAt(point) * zoom;
      const range = Math.max(0, (laid.spans.at(-1) ?? 0) * zoom - room);
      const bend = room * PAN_BEND;
      const framed = panTo(
        room - width,
        followLeft(room, width, laid.across, bend),
        0,
        range,
        bend,
      );
      // The pan to the left edge starts as the rows begin to slow and ends with the runway.
      const reach = smootherstep((scrolled - slowing) / (laid.runway + laid.stop));
      const auto = between(framed, -range, reach);
      // Back above the triangle, or at the page's top, the reader's own pan eases away.
      const above = (scrolled <= -laid.focus || window.scrollY <= 0) && nudge !== 0;
      if (above) {
        nudge = Math.abs(nudge) < 0.5 ? 0 : nudge * (1 - EASE);
      }
      nudge = Math.min(Math.max(nudge, -range - auto), -auto);
      panned = auto + nudge;
      laid.rows.forEach((row, index) => {
        const top = laid.tops[index] ?? 0;
        const moved = line + (top - point) * zoom - top;
        row.style.transform = `translate(${-panned}px, ${moved}px) scale(${zoom})`;
      });
      showSize(nearestSize(laid.tiles.large * zoom, laid.tiles));
      Object.assign(reading, { scrolled, point, line, zoom, pan: panned, nudge, end: laid.end });
      if (above && nudge !== 0) {
        schedule();
      }
    };
    if (following) {
      window.addEventListener("scroll", () => schedule(), { passive: true });
      // A new width or height, or the page's fonts, lay the triangle out anew.
      const relay = () => {
        if (following) {
          requestAnimationFrame(() => {
            lay();
            follow();
          });
        }
      };
      window.addEventListener("resize", relay);
      void fontsReady.then(relay);
      // A sideways turn of the wheel, a horizontal swipe on a trackpad, pans the triangle
      // while the page scrolls up and down, so a diagonal gesture moves both ways at
      // once. A finger dragged sideways does the same; up and down is the page's.
      const unit = (/** @type {WheelEvent} */ event) =>
        event.deltaMode === 1 ? 16 : event.deltaMode === 2 ? cells.clientWidth : 1;
      cells.addEventListener(
        "wheel",
        (event) => {
          if (following && event.deltaX !== 0) {
            nudge += event.deltaX * unit(event);
            schedule();
          }
        },
        { passive: true },
      );
      /** @type {number | null} */
      let touched = null;
      cells.addEventListener("pointerdown", (event) => {
        touched = event.pointerType === "touch" ? event.clientX : null;
      });
      cells.addEventListener("pointermove", (event) => {
        if (following && touched !== null && event.pointerType === "touch") {
          nudge += touched - event.clientX;
          touched = event.clientX;
          schedule();
        }
      });
      for (const kind of ["pointerup", "pointercancel"]) {
        cells.addEventListener(kind, () => {
          touched = null;
        });
      }
      cells.addEventListener("scroll", () => schedule(), { passive: true });
      schedule();
    }

    return { arrange, change, fontsReady, hold };
  }

  globalThis.SiteAtlasView = {
    row,
    widest,
    perLine,
    perLineAt,
    tileAt,
    smoothMin,
    smoothMax,
    curve,
    smootherstep,
    zoomAt,
    settle,
    journey,
    followLeft,
    nearestSize,
    between,
    along,
    panTo,
    place,
    viewOf,
    searchFor,
    sizeOf,
    searchForSize,
    scaleOf,
    searchForScale,
    rowRatio,
    largestSide,
    stepTo,
    lengthPx,
    milliseconds,
    moveFrom,
    still,
    mount,
  };
})();
