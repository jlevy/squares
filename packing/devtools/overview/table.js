// Sorting and filtering for the site's tables: the frontier atlas, the results table and
// the overview's recent results.
//
// A classic script, inlined into each page by `devtools.render_overview`. It enhances
// every `table.site-table` whose wrapper follows a `.site-table-tools` bar, directly or
// with a table of results' legend between them (`toolsBefore`); the table is complete in
// the HTML, so with scripting off every row is present and nothing is lost.
//
// Headings with `data-sort="num"` or `data-sort="text"` sort on click (a numeric sort
// reads each cell's `data-value`, else its text). Filters are the bar's controls, each
// naming a row attribute with `data-filter`; `data-bound` says how the control's value
// is held against the row's:
//   <select data-filter="status">                 row's data-status equals the value
//   <input type="checkbox" data-filter="open">     row's data-open is "true"
//   <input type="number" data-filter="n" data-bound="min|max">  row's data-n in range
//   <select data-filter="s" data-bound="min">     row's data-s at least the value
//   <input type="number" data-filter="date" data-bound="age">
//                                                 row's data-date, an ISO date, at most
//                                                 that many days before the reader's day
//   <input type="number" data-filter="n" data-bound="covers">
//                                                 row's data-n, a list of numbers and
//                                                 ranges ("27 28 31-32"), holds the value
//   <select data-filter="project" data-bound="has">
//                                                 row's data-project, a list of names a
//                                                 space apart, has the value among them
// An empty value passes every row, and filters compose: a row shows when it passes every
// one. A control's state in the HTML is its default, so a bar can start filtered, with
// the rows it hides already `hidden` and its count already written. An age is the one
// filter the page cannot settle when it is built: there its rows are hidden as of a day
// the build takes from the register, and here, on load, as of the reader's.
//
// One row is placed by more than the filters: the row the page's fragment names
// (`all-results.html#t-018`) always shows, so a link to a row never lands on nothing.
// A filtered table is one flat list, with no heading row among its rows.
//
// The bar's `.site-count` shows how many rows remain. A link can open the table
// filtered: each query parameter presets the control it names, `status=proved`,
// `recent=true`, `n-max=100` for a bound, `n=11` for a `covers` control, `age=180`
// for an age, or `project=evand-square-packing` for a `has` control, so a card can point
// at a filtered view. A control marked `data-preset` is for such links alone: its label
// is `hidden` in the HTML and shows only while the control filters, so a reader sees
// what narrows the table and can set it back.
// The pure functions are published
// on `globalThis.SiteTable` for the Node tests; nothing else leaves this file.

(() => {
  /**
   * The sort key of a cell: its `data-value`, else its visible text.
   * @param {Element | undefined} cell
   * @returns {string}
   */
  function cellKey(cell) {
    if (!cell) {
      return "";
    }
    const value = cell.getAttribute("data-value");
    return value ?? (cell.textContent ?? "").trim();
  }

  /**
   * Compare two sort keys; a key that is not a number sorts after every number.
   * @param {string} left
   * @param {string} right
   * @param {SiteTableSortType} type
   * @returns {number}
   */
  function compareKeys(left, right, type) {
    if (type === "num") {
      const a = Number.parseFloat(left);
      const b = Number.parseFloat(right);
      const aMissing = Number.isNaN(a);
      const bMissing = Number.isNaN(b);
      if (aMissing || bMissing) {
        return Number(aMissing) - Number(bMissing);
      }
      return a - b;
    }
    return left.localeCompare(right, undefined, { numeric: true, sensitivity: "base" });
  }

  /**
   * The order that sorts `keys`, stable, as indices into `keys`.
   * @param {readonly string[]} keys
   * @param {SiteTableSortType} type
   * @param {"ascending" | "descending"} direction
   * @returns {number[]}
   */
  function sortOrder(keys, type, direction) {
    const sign = direction === "ascending" ? 1 : -1;
    return keys
      .map((key, index) => ({ key, index }))
      .sort((a, b) => sign * compareKeys(a.key, b.key, type) || a.index - b.index)
      .map((entry) => entry.index);
  }

  /**
   * Whether a list of numbers and ranges, "27 28 31-32", holds `value`.
   * @param {string} list
   * @param {number} value
   * @returns {boolean}
   */
  function covers(list, value) {
    return list.split(/\s+/).some((entry) => {
      const [low = "", high = low] = entry.split("-");
      return entry !== "" && Number(low) <= value && value <= Number(high);
    });
  }

  /**
   * Whether a row with these attributes passes every active filter.
   * @param {Readonly<Record<string, string | undefined>>} row
   * @param {readonly SiteTableFilter[]} filters
   * @returns {boolean}
   */
  function rowMatches(row, filters) {
    return filters.every((filter) => {
      const actual = row[filter.key];
      switch (filter.kind) {
        case "equals":
          return filter.value === "" || actual === filter.value;
        case "flag":
          return filter.value !== "true" || actual === "true";
        case "min":
        case "max": {
          const bound = Number.parseFloat(filter.value);
          if (Number.isNaN(bound)) {
            return true;
          }
          const value = Number.parseFloat(actual ?? "");
          return filter.kind === "min" ? value >= bound : value <= bound;
        }
        case "since": {
          // ISO dates order as text, so no date is parsed.
          const value = actual ?? "";
          return filter.value === "" || (value !== "" && value >= filter.value);
        }
        case "covers": {
          const wanted = Number.parseFloat(filter.value);
          return Number.isNaN(wanted) || covers(actual ?? "", wanted);
        }
        case "has":
          return filter.value === "" || (actual ?? "").split(/\s+/).includes(filter.value);
        default:
          return true;
      }
    });
  }

  /**
   * The live count's words.
   * @param {number} shown
   * @param {number} total
   * @param {string} noun
   * @returns {string}
   */
  function countText(shown, total, noun) {
    return shown === total ? `${total} ${noun}` : `${shown} of ${total} ${noun}`;
  }

  /**
   * A day as an ISO date, by the clock of whoever is reading.
   * @param {Date} now
   * @returns {string}
   */
  function localDay(now) {
    const month = String(now.getMonth() + 1).padStart(2, "0");
    const day = String(now.getDate()).padStart(2, "0");
    return `${String(now.getFullYear()).padStart(4, "0")}-${month}-${day}`;
  }

  /**
   * The first day a row may be dated to be no older than `days` on `today`, both ISO
   * dates: 180 days on 2026-09-30 is 2026-04-03. Empty, which is no limit, when `days`
   * is not a number or reaches past the calendar.
   * @param {string} today
   * @param {string} days
   * @returns {string}
   */
  function ageCutoff(today, days) {
    const age = Number.parseFloat(days);
    const [year = Number.NaN, month = Number.NaN, day = Number.NaN] = today.split("-").map(Number);
    const time = Date.UTC(year, month - 1, day - Math.max(age, 0));
    if (Number.isNaN(time) || new Date(time).getUTCFullYear() < 1) {
      return "";
    }
    return new Date(time).toISOString().slice(0, 10);
  }

  /**
   * The query parameter that presets a filter control: its key, with its bound if it
   * is one end of a range, and `age` for an age, whatever it is the age of.
   * @param {string} key
   * @param {string | null} bound
   * @returns {string}
   */
  function controlParam(key, bound) {
    if (bound === "age") {
      return bound;
    }
    return bound && bound !== "covers" && bound !== "has" ? `${key}-${bound}` : key;
  }

  /**
   * Set a tools bar's controls from a page's query string.
   * @param {Element} tools
   * @param {URLSearchParams} params
   */
  function presetFilters(tools, params) {
    for (const control of tools.querySelectorAll("[data-filter]")) {
      const name = controlParam(
        control.getAttribute("data-filter") ?? "",
        control.getAttribute("data-bound"),
      );
      const value = params.get(name);
      if (value === null) {
        continue;
      }
      if (control instanceof HTMLInputElement && control.type === "checkbox") {
        control.checked = value === "true";
      } else if (control instanceof HTMLInputElement || control instanceof HTMLSelectElement) {
        control.value = value;
      }
    }
  }

  /**
   * What each `data-bound` makes of its control.
   * @type {Readonly<Record<string, SiteTableFilter["kind"]>>}
   */
  const BOUNDS = { min: "min", max: "max", covers: "covers", has: "has" };

  /**
   * Show each preset-only control's label while the control filters, and only then.
   * @param {Element} tools
   */
  function showPresets(tools) {
    for (const control of tools.querySelectorAll("[data-preset]")) {
      const label = control.closest("label");
      if (label instanceof HTMLElement && control instanceof HTMLSelectElement) {
        label.hidden = control.value === "";
      }
    }
  }

  /**
   * The id the page's fragment names: "" for none, or for one that does not decode.
   * @returns {string}
   */
  function fragmentTarget() {
    try {
      return decodeURIComponent(location.hash.slice(1));
    } catch {
      return "";
    }
  }

  /**
   * The filters a tools bar's controls currently express. An age becomes the day it
   * reaches back to from `today`, so a row is held to a date and never to a clock.
   * @param {Element} tools
   * @param {string} today an ISO date
   * @returns {SiteTableFilter[]}
   */
  function readFilters(tools, today) {
    /** @type {SiteTableFilter[]} */
    const filters = [];
    for (const control of tools.querySelectorAll("[data-filter]")) {
      const key = control.getAttribute("data-filter") ?? "";
      const bound = control.getAttribute("data-bound");
      if (control instanceof HTMLSelectElement && !bound) {
        filters.push({ key, kind: "equals", value: control.value });
      } else if (control instanceof HTMLInputElement && control.type === "checkbox") {
        filters.push({ key, kind: "flag", value: control.checked ? "true" : "false" });
      } else if (control instanceof HTMLInputElement && bound === "age") {
        filters.push({ key, kind: "since", value: ageCutoff(today, control.value) });
      } else if (control instanceof HTMLInputElement || control instanceof HTMLSelectElement) {
        filters.push({ key, kind: BOUNDS[bound ?? ""] ?? "min", value: control.value });
      }
    }
    return filters;
  }

  /**
   * A row's `data-*` attributes, by name without the prefix.
   * @param {HTMLTableRowElement} row
   * @returns {Record<string, string | undefined>}
   */
  function rowData(row) {
    return { ...row.dataset };
  }

  /**
   * Wire one table to its tools bar. Safe to call twice: a wired table is skipped.
   * @param {HTMLTableElement} table
   * @param {Element | null} tools
   */
  function enhance(table, tools) {
    if (table.hasAttribute("data-site-table-ready")) {
      return;
    }
    table.setAttribute("data-site-table-ready", "");
    const body = table.tBodies[0];
    if (!body) {
      return;
    }
    const count = tools?.querySelector(".site-count") ?? null;
    const noun = count?.getAttribute("data-noun") ?? "rows";

    const applyFilters = () => {
      if (!tools) {
        return;
      }
      showPresets(tools);
      const filters = readFilters(tools, localDay(new Date()));
      const target = fragmentTarget();
      const rows = Array.from(body.rows);
      const passes = rows.map(
        (row) => rowMatches(rowData(row), filters) || (row.id !== "" && row.id === target),
      );
      rows.forEach((row, index) => {
        row.hidden = passes[index] !== true;
      });
      if (count) {
        count.textContent = countText(passes.filter(Boolean).length, rows.length, noun);
      }
    };

    const headings = Array.from(table.tHead?.rows[0]?.cells ?? []);
    headings.forEach((heading, column) => {
      const type = heading.getAttribute("data-sort");
      if (type !== "num" && type !== "text") {
        return;
      }
      heading.tabIndex = 0;
      heading.setAttribute("aria-sort", "none");
      const sort = () => {
        const direction =
          heading.getAttribute("aria-sort") === "ascending" ? "descending" : "ascending";
        for (const other of headings) {
          if (other.hasAttribute("aria-sort")) {
            other.setAttribute("aria-sort", "none");
          }
        }
        heading.setAttribute("aria-sort", direction);
        const current = Array.from(body.rows);
        const keys = current.map((row) => cellKey(row.cells[column]));
        const order = sortOrder(keys, type, direction);
        body.append(...order.flatMap((index) => current[index] ?? []));
        applyFilters();
      };
      heading.addEventListener("click", sort);
      heading.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          sort();
        }
      });
    });

    if (tools) {
      tools.removeAttribute("hidden");
      tools.addEventListener("input", applyFilters);
      tools.addEventListener("change", applyFilters);
      window.addEventListener("hashchange", applyFilters);
      presetFilters(tools, new URLSearchParams(location.search));
      applyFilters();
    }
  }

  /**
   * The tools bar a table's wrapper follows: the element right before it. Null where
   * there is none.
   * @param {Element | null} wrap
   * @returns {Element | null}
   */
  function toolsBefore(wrap) {
    const before = wrap?.previousElementSibling ?? null;
    return before?.classList.contains("site-table-tools") ? before : null;
  }

  /** Enhance every site table on the page. */
  function init() {
    // The overview has a bounded recent set. Its complete-table link carries supported
    // filter query state, so a query selecting older results reaches the full dataset.
    const all = document.querySelector("a[data-all-results]");
    if (all instanceof HTMLAnchorElement) {
      const destination = all.href;
      const updateDestination = () => {
        const fragment = fragmentTarget();
        const retired = (() => {
          try {
            const aliases = JSON.parse(all.getAttribute("data-retired-results") ?? "{}");
            return /^t-\d+$/.test(fragment) &&
              Object.hasOwn(aliases, fragment) &&
              aliases[fragment] === `result/${fragment}.html`
              ? aliases[fragment]
              : null;
          } catch {
            return null;
          }
        })();
        const target = new URL(retired ?? destination, destination);
        const source = new URLSearchParams(location.search);
        for (const [key, value] of source) {
          if (
            [
              "status",
              "kind",
              "activity",
              "source",
              "project",
              "n",
              "n-min",
              "n-max",
              "s",
              "s-min",
              "s-max",
              "v",
              "v-min",
              "v-max",
              "c",
              "c-min",
              "c-max",
              "age",
              "age-max",
              "superseded",
              "current",
              "search",
            ].includes(key)
          ) {
            target.searchParams.set(key, value);
          }
        }
        const known = (all.getAttribute("data-result-ids") ?? "").split(/\s+/);
        target.hash = "";
        if (fragment && (retired || known.includes(fragment))) {
          target.hash = location.hash;
        }
        all.href = target.href;
      };
      updateDestination();
      window.addEventListener("hashchange", updateDestination);
    }
    for (const table of document.querySelectorAll("table.site-table")) {
      if (!(table instanceof HTMLTableElement)) {
        continue;
      }
      enhance(table, toolsBefore(table.closest(".site-table-wrap")));
    }
  }

  globalThis.SiteTable = {
    compareKeys,
    sortOrder,
    covers,
    rowMatches,
    countText,
    localDay,
    ageCutoff,
    controlParam,
    init,
  };

  if (typeof document === "undefined") {
    return;
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
