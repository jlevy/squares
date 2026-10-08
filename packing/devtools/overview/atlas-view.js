// Input response: the atlas's two views, Grid and Triangle, and the move between them.
//
// The grid sets the cases in reading order, as many to a line as fit. The triangle sets
// them by the grid bound: row k holds the 2k - 1 cases n = (k - 1)^2 + 1 to k^2, the ones
// a square of side k is known to hold, and every row ends at the right edge, so the
// perfect squares 1, 4, 9, 16, ... run down it. Those are the cases whose packing is the
// k by k grid itself.
//
// A row wider than the page wraps, in reading order: every line but its last is full,
// from the left edge, and its last line holds the tiles left over, set from the right,
// so the row still ends at its k^2 on the right edge and the next row still starts a
// new line. So nineteen tiles at eight to a line are three lines of 8, 8 and 3, the 3
// ending at the square. Where every row fits, which is every desktop width, no row
// wraps and the same rule draws the plain triangle.
//
// One set of tiles serves both views. The view is an attribute of the atlas block,
// `data-atlas-view`, and the layout is the stylesheet's: in the triangle each tile takes
// its grid line and column from three custom properties this script writes, `place`'s
// answer for the tiles a line holds, which follows from the block's width and the least
// tile the stylesheet allows (`--site-atlas-tile-min`). They are a tile's only inline
// style, written when the tiles are placed and again only when that answer changes, so
// changing the view is one attribute. Nothing here sizes a tile.
//
// The move is a FLIP: every tile's box is read, the layout is changed, every box is read
// again, and each tile is then animated from where it was to where it is with a
// transform alone, which the compositor runs without laying anything out. One read, one
// write, one read; a tile that neither starts nor ends in the window is not animated.
// What follows the tiles on the page, which a change of their height carries up or down,
// moves the same way, so nothing jumps under the tiles while they travel.
// The tokens `--site-atlas-move-duration` and `--site-atlas-move-easing` time it, and the
// duration is 0ms for a reader who asks for reduced motion, which switches at once.
//
// The view is in the address as `?atlas=triangle`, so it can be linked; the grid, the
// default, has no parameter. A query parameter and not a fragment: `forward.js` sends a
// fragment the overview does not have to the explainer.
//
// The tiles come in three sizes, Small, Medium and Large, chosen by a second strip of
// tabs beside the view tabs, in either view (think-ht8t). The size is an attribute of the
// block too, `data-atlas-size`, and the stylesheet scales a tile by it
// (`--site-atlas-scale`): the grid's least cell, and in the triangle the most a tile may
// be and its share of a line, never under the least tile. Small keeps the tiles a line
// holds and draws each smaller; Large holds fewer, as many as tiles that much wider than
// Medium's leave room for (`perLineAt`), so where the triangle already filled the block
// its long rows wrap, by the one rule. A change of size is a change of layout like a
// change of view, moved the same way, and it is in the address as `?size=small` or
// `?size=large`; Medium, the default, has no parameter.
//
// The pure functions are published on `globalThis.SiteAtlasView` for the Node tests and
// for `atlas-grid.js`, which places the tiles and calls `mount`.

(() => {
  /** The query parameter that names the view. */
  const PARAM = "atlas";
  /** The query parameter that names the size. */
  const SIZE_PARAM = "size";

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
   * How many tiles a line holds: as many of the `least` width as `width` has room for,
   * at least one, and no more than `most`, the longest row, past which a line would only
   * have empty columns.
   * @param {number} width
   * @param {number} least
   * @param {number} most
   * @returns {number}
   */
  function perLine(width, least, most) {
    if (!(width > 0) || !(least > 0)) {
      return Math.max(1, most);
    }
    return Math.max(1, Math.min(most, Math.floor(width / least)));
  }

  /**
   * How many tiles a line holds at a size whose tile is `scale` times Medium's. At Medium
   * and below it is `perLine`'s answer: a smaller size draws the same tiles smaller. Above
   * it, a line holds as many tiles as have room at `scale` times the width a Medium tile
   * has, its share of the line and no more than `largest`, rounded to the nearest whole
   * tile, at least one and never more than at Medium. So a triangle that fills the block
   * at Medium wraps its long rows at Large, and one that a wide block leaves room around
   * grows into that room first.
   * @param {number} width
   * @param {number} least
   * @param {number} largest
   * @param {number} most
   * @param {number} scale
   * @returns {number}
   */
  function perLineAt(width, least, largest, most, scale) {
    const medium = perLine(width, least, most);
    if (!(scale > 1) || !(width > 0)) {
      return medium;
    }
    const tile = largest > 0 ? Math.min(largest, width / medium) : width / medium;
    return Math.max(1, Math.min(medium, Math.round(width / (scale * tile))));
  }

  /**
   * Where case `n` stands in the triangle when a line holds `per` tiles: its row k, its
   * line counted from the top of the triangle, its column counted from the left, and
   * whether its line opens a row after the first, which takes the space between rows.
   *
   * A row that fits is one line ending at the last column. A row that does not is
   * filled in reading order: every line but its last is full, from the first column,
   * and its last holds what is left over, ending at the last column, so every row ends
   * at its square on the right edge.
   * @param {number} n
   * @param {number} per
   * @returns {AtlasTrianglePlace}
   */
  function place(n, per) {
    const k = row(n);
    const columns = Math.max(1, Math.floor(per));
    let above = 0;
    for (let earlier = 1; earlier < k; earlier += 1) {
      above += Math.ceil((2 * earlier - 1) / columns);
    }
    const tiles = 2 * k - 1;
    const lines = Math.ceil(tiles / columns);
    const at = n - (k - 1) * (k - 1);
    const line = Math.ceil(at / columns);
    const within = at - (line - 1) * columns;
    // What the tile's line holds: a full line, or on the last line what is left over.
    const held = line === lines ? tiles - (lines - 1) * columns : columns;
    return {
      row: k,
      line: above + line,
      column: columns - held + within,
      opens: k > 1 && line === 1,
    };
  }

  /**
   * The view a query string asks for: the triangle when it says so, else the grid.
   * @param {string} search
   * @returns {AtlasView}
   */
  function viewOf(search) {
    return new URLSearchParams(search).get(PARAM) === "triangle" ? "triangle" : "grid";
  }

  /**
   * `search` with the view written into it: the parameter for the triangle, none for the
   * grid, and every other parameter kept in its place.
   * @param {string} search
   * @param {AtlasView} view
   * @returns {string}
   */
  function searchFor(search, view) {
    return searchWith(search, PARAM, view === "triangle" ? "triangle" : null);
  }

  /**
   * The size a word names: small or large, else medium.
   * @param {string | null | undefined} word
   * @returns {AtlasSize}
   */
  function asSize(word) {
    return word === "small" || word === "large" ? word : "medium";
  }

  /**
   * The size a query string asks for: small or large when it says so, else medium.
   * @param {string} search
   * @returns {AtlasSize}
   */
  function sizeOf(search) {
    return asSize(new URLSearchParams(search).get(SIZE_PARAM));
  }

  /**
   * `search` with the size written into it: the parameter for small and large, none for
   * medium, and every other parameter kept in its place.
   * @param {string} search
   * @param {AtlasSize} size
   * @returns {string}
   */
  function searchForSize(search, size) {
    return searchWith(search, SIZE_PARAM, size === "medium" ? null : size);
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
  function mount({ block, cells, tabs, sizes }) {
    const buttons = tabsOf(tabs);
    const sizeButtons = sizes === null ? [] : tabsOf(sizes);
    /** The tiles a line holds and the last case shown, as last arranged. */
    let arranged = "";
    /** @type {Animation[]} */
    let running = [];

    /** @returns {AtlasView} */
    const view = () => (block.dataset.atlasView === "triangle" ? "triangle" : "grid");
    /** @returns {AtlasSize} */
    const size = () => asSize(block.dataset.atlasSize);

    /** The tiles that show: the first hundred, and the rest once the grid is expanded. */
    const shown = () =>
      [
        ...cells.querySelectorAll(
          ":scope > .site-atlas-cell, :scope > :not([hidden]) > .site-atlas-cell",
        ),
      ].filter((tile) => tile instanceof HTMLElement);

    // Write each tile's line and column for the tiles a line now holds. Only the
    // triangle reads them, but they are kept current in the grid too, so a change of
    // view writes nothing: a tile's properties are inherited by every line of its
    // drawing, and writing them restyles all of those. Nothing is written while
    // neither the tiles a line holds nor the last case shown has changed. The size's
    // scale is the stylesheet's (`--site-atlas-scale`), read as the tiles are arranged.
    const arrange = () => {
      const tiles = shown();
      const last = Number(tiles.at(-1)?.dataset.atlasN);
      if (!(last >= 1)) {
        return;
      }
      const root = Number.parseFloat(getComputedStyle(document.documentElement).fontSize);
      const style = getComputedStyle(cells);
      const least = lengthPx(style.getPropertyValue("--site-atlas-tile-min"), root);
      const largest = lengthPx(style.getPropertyValue("--site-atlas-tile-max"), root);
      const scale = Number.parseFloat(style.getPropertyValue("--site-atlas-scale"));
      const width = cells.getBoundingClientRect().width;
      const per = perLineAt(width, least, largest, widest(last), scale);
      const key = `${per}:${last}`;
      if (key === arranged) {
        return;
      }
      arranged = key;
      cells.style.setProperty("--site-atlas-per-line", String(per));
      // A triangle some row of which wraps sets its rows further apart (site.css).
      cells.toggleAttribute("data-atlas-wrapped", per < widest(last));
      for (const tile of tiles) {
        const at = place(Number(tile.dataset.atlasN), per);
        tile.style.cssText =
          `--site-atlas-line: ${at.line}; --site-atlas-column: ${at.column}; ` +
          `--site-atlas-opens: ${at.opens ? 1 : 0};`;
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
      /** @type {Map<HTMLElement, { tile: DOMRect, drawing: DOMRect }>} */
      const tiles = new Map();
      for (const tile of shown()) {
        const drawing = tile.firstElementChild;
        if (drawing !== null) {
          tiles.set(tile, {
            tile: tile.getBoundingClientRect(),
            drawing: drawing.getBoundingClientRect(),
          });
        }
      }
      /** @type {Map<HTMLElement, DOMRect>} */
      const rest = new Map();
      for (const follower of followers()) {
        rest.set(follower, follower.getBoundingClientRect());
      }
      return { tiles, rest, scroll: window.scrollY };
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
      for (const [follower, last] of now.rest) {
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

    /** @param {AtlasView} current */
    const mark = (current) => {
      block.dataset.atlasView = current;
      document.documentElement.dataset.siteAtlasView = current;
      for (const tab of buttons) {
        const on = tab.dataset.atlasTab === current;
        tab.setAttribute("aria-selected", String(on));
        tab.tabIndex = on ? 0 : -1;
        if (on) {
          cells.setAttribute("aria-labelledby", tab.id);
        }
      }
    };

    /** @param {AtlasSize} current */
    const markSize = (current) => {
      block.dataset.atlasSize = current;
      document.documentElement.dataset.siteAtlasSize = current;
      for (const tab of sizeButtons) {
        const on = tab.dataset.atlasSizeTab === current;
        tab.setAttribute("aria-selected", String(on));
        tab.tabIndex = on ? 0 : -1;
      }
    };

    /** @param {string} search */
    const readdress = (search) => {
      history.replaceState(history.state, "", `${location.pathname}${search}${location.hash}`);
    };

    /** @param {AtlasView} next */
    const select = (next) => {
      if (next === view()) {
        return;
      }
      change(() => mark(next));
      readdress(searchFor(location.search, next));
    };

    /** @param {AtlasSize} next */
    const selectSize = (next) => {
      if (next === size()) {
        return;
      }
      change(() => markSize(next));
      readdress(searchForSize(location.search, next));
    };

    cells.id = tabs.dataset.atlasPanel ?? "";
    cells.setAttribute("role", "tabpanel");
    mark(document.documentElement.dataset.siteAtlasView === "triangle" ? "triangle" : "grid");
    markSize(asSize(document.documentElement.dataset.siteAtlasSize));

    wire(tabs, (tab) => select(tab.dataset.atlasTab === "triangle" ? "triangle" : "grid"));
    if (sizes !== null) {
      wire(sizes, (tab) => selectSize(asSize(tab.dataset.atlasSizeTab)));
    }

    // The tiles a line holds follow the block's width. A resize is settled on the next
    // frame, at most once a frame, and placed without a move: the window is already
    // moving everything.
    if ("ResizeObserver" in window) {
      let waiting = false;
      let priorWidth = cells.getBoundingClientRect().width;
      new ResizeObserver(() => {
        const width = cells.getBoundingClientRect().width;
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

    return { arrange, change };
  }

  globalThis.SiteAtlasView = {
    row,
    widest,
    perLine,
    perLineAt,
    place,
    viewOf,
    searchFor,
    sizeOf,
    searchForSize,
    stepTo,
    lengthPx,
    milliseconds,
    moveFrom,
    still,
    mount,
  };
})();
