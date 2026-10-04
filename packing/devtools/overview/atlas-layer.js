// The atlas's two drawings of a case, House and Regularized, and the swap between them.
//
// The house drawing is the record's own: the house renderer's picture of the witness the
// atlas keeps. The regularized drawing is a derived view (X-049, Exact Regularization):
// the record's exact frame with its nearly axis-aligned squares straightened and slid
// into exact contact, drawn by the same renderer at the same settings, so a square that
// only looked loose is shaded for the contacts it has. Only some cases have one; every
// other case keeps its house tile under both tabs.
//
// The regularized tiles arrive in a third `<template>`, each a whole tile with the
// layer's badge after its number. Choosing Regularized puts each one where its case's
// house tile stands, and House puts the house tiles back: the same place, with the place
// the triangle gave the tile (its one inline style) carried over, and the keyboard focus
// too where it was on a tile swapped, so nothing is laid out again and nothing moves.
// The swap is instant, so the two drawings can be compared by flicking between the tabs.
// A tile the grid has not placed yet, one of the rest before the expander is first
// pressed, is swapped when `atlas-grid.js` places it (`apply`).
//
// The drawing is in the address as `?layer=regularized`; house, the default, has no
// parameter, and every other parameter and the fragment keep their places, as the
// view's `?atlas=` does. It is read before any tile is placed, so a linked regularized
// atlas never shows a house tile first.
//
// The pure functions are published on `globalThis.SiteAtlasLayer` for the Node tests and
// for `atlas-grid.js`, which places the tiles and calls `mount`.

(() => {
  /** The query parameter that names the drawing. */
  const PARAM = "layer";
  /** The drawing a tile carries when it is not the house one. */
  const REGULARIZED = "regularized";

  /**
   * The drawing a query string asks for: the regularized when it says so, else house.
   * @param {string} search
   * @returns {AtlasLayer}
   */
  function layerOf(search) {
    return new URLSearchParams(search).get(PARAM) === REGULARIZED ? REGULARIZED : "house";
  }

  /**
   * `search` with the drawing written into it: the parameter for the regularized, none
   * for house, and every other parameter kept in its place.
   * @param {string} search
   * @param {AtlasLayer} layer
   * @returns {string}
   */
  function searchFor(search, layer) {
    const params = new URLSearchParams(search);
    if (layer === REGULARIZED) {
      params.set(PARAM, REGULARIZED);
    } else {
      params.delete(PARAM);
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
   * Wire the drawing tabs of one atlas block. `cells` holds the tiles, which
   * `atlas-grid.js` places; `tabs` is the tablist the page ships, and `template` holds
   * the regularized tiles.
   * @param {SiteAtlasLayerParts} parts
   * @returns {SiteAtlasLayers}
   */
  function mount({ block, cells, tabs, template }) {
    const buttons = [...tabs.querySelectorAll('[role="tab"]')].filter(
      (tab) => tab instanceof HTMLButtonElement,
    );
    /** @type {Map<number, HTMLElement> | null} */
    let drawn = null;
    /**
     * The house tiles set aside while their case's regularized tile stands in for them.
     * @type {Map<number, HTMLElement>}
     */
    const held = new Map();

    /** The regularized tiles by case, taken from their template the first time. */
    const regularized = () => {
      if (drawn === null) {
        drawn = new Map();
        const fragment = template.content.cloneNode(true);
        if (fragment instanceof DocumentFragment) {
          for (const tile of fragment.querySelectorAll(".site-atlas-cell")) {
            if (tile instanceof HTMLElement) {
              drawn.set(Number(tile.dataset.atlasN), tile);
            }
          }
        }
      }
      return drawn;
    };

    /** @returns {AtlasLayer} */
    const layer = () => (block.dataset.atlasLayer === REGULARIZED ? REGULARIZED : "house");

    /**
     * Put `to` where `from` stands, with its place in the triangle and the focus.
     * @param {HTMLElement} from
     * @param {HTMLElement} to
     */
    const swap = (from, to) => {
      to.style.cssText = from.style.cssText;
      const focused = document.activeElement === from;
      from.replaceWith(to);
      if (focused) {
        to.focus({ preventScroll: true });
      }
    };

    // Make every placed tile the drawing the block is in: each regularized tile in for
    // its house tile, or each house tile back. Placing it again is no change, so the
    // grid calls this whenever it places tiles.
    const apply = () => {
      if (layer() === REGULARIZED) {
        for (const [n, tile] of regularized()) {
          if (cells.contains(tile)) {
            continue;
          }
          const house = cells.querySelector(
            `.site-atlas-cell[data-atlas-n="${n}"]:not([data-atlas-layer])`,
          );
          if (house instanceof HTMLElement) {
            swap(house, tile);
            held.set(n, house);
          }
        }
        return;
      }
      for (const [n, house] of held) {
        const tile = regularized().get(n);
        if (tile !== undefined && cells.contains(tile)) {
          swap(tile, house);
        }
      }
      held.clear();
    };

    /** @param {AtlasLayer} current */
    const mark = (current) => {
      block.dataset.atlasLayer = current;
      for (const tab of buttons) {
        const on = tab.dataset.atlasLayerTab === current;
        tab.setAttribute("aria-selected", String(on));
        tab.tabIndex = on ? 0 : -1;
      }
    };

    /** @param {AtlasLayer} next */
    const select = (next) => {
      if (next === layer()) {
        return;
      }
      mark(next);
      apply();
      const address = `${location.pathname}${searchFor(location.search, next)}${location.hash}`;
      history.replaceState(history.state, "", address);
    };

    /** @param {HTMLButtonElement} tab */
    const named = (tab) => (tab.dataset.atlasLayerTab === REGULARIZED ? REGULARIZED : "house");

    mark(layerOf(location.search));

    tabs.addEventListener("click", (event) => {
      const tab = event.target instanceof Element ? event.target.closest('[role="tab"]') : null;
      if (tab instanceof HTMLButtonElement && tabs.contains(tab)) {
        select(named(tab));
      }
    });
    // The tabs are one stop in the page's tab order, as the view tabs are: the arrow
    // keys, Home and End move between them, and the tab focus lands on is selected.
    tabs.addEventListener("keydown", (event) => {
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
      select(named(next));
    });

    return { apply };
  }

  globalThis.SiteAtlasLayer = { layerOf, searchFor, stepTo, mount };
})();
