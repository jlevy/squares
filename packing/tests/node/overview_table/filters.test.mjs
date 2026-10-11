// The table script wired to a stand-in results table and its tools bar: a flat list of
// rows carrying the facets `overview_sections.result_facets` writes, under the controls
// `overview_sections.result_filters` writes, Significance starting at S4 and up (a
// stand-in level: the overview starts at S3) and Max age and Hide superseded wherever
// the page under test starts them. The stand-ins are only what the script reads, the
// day among them; the test reads what it then shows.
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import vm from "node:vm";

const SOURCE = readFileSync(
  new URL("../../../devtools/overview/table.js", import.meta.url),
  "utf8",
);

/** A control of the tools bar: what `data-filter` names, its `data-bound`, its value. */
class Control {
  /** @param {string} key @param {string | null} bound @param {string} value */
  constructor(key, bound, value) {
    this.key = key;
    this.bound = bound;
    this.value = value;
    this.type = "number";
  }

  /** @param {string} name */
  getAttribute(name) {
    return name === "data-filter" ? this.key : name === "data-bound" ? this.bound : null;
  }
}
class Select extends Control {}
class Input extends Control {}
/** A preset-only control's label: out of the bar, `hidden`, until its control filters. */
class Label {
  hidden = true;
}
/** A preset-only select (`data-preset`), inside its label. */
class Preset extends Select {
  label = new Label();

  closest() {
    return this.label;
  }
}
/** A checkbox: what it says is whether it is checked, never its value. */
class Checkbox extends Input {
  /** @param {string} key @param {boolean} checked */
  constructor(key, checked) {
    super(key, null, "on");
    this.type = "checkbox";
    this.checked = checked;
  }
}
class Table {}

/**
 * A stand-in row: a result's, with its facets.
 * @param {string} id
 * @param {Record<string, string>} facets
 * @param {boolean} [hidden] as the page writes it
 */
function row(id, facets, hidden = false) {
  return {
    id,
    hidden,
    dataset: facets,
    cells: [{ getAttribute: () => id }],
  };
}

/**
 * A `Date` whose now is noon on `today`, by the local clock, which is the one the script
 * reads the reader's day from.
 * @param {string} today an ISO date
 */
function clock(today) {
  const [year = 0, month = 1, day = 1] = today.split("-").map(Number);
  const now = new Date(year, month - 1, day, 12).getTime();
  return class extends Date {
    /** @param {number} [time] */
    constructor(time) {
      super(time ?? now);
    }
  };
}

/**
 * A page with a table of results, as the HTML has it: Significance at S4 and up, the
 * rows below it already hidden, Max age at `age`, empty for none, and Hide superseded
 * checked if `hide`. The reader opens it on `today`. Three rows are confirmed, one of
 * them superseded; of the other two, one is recorded and one is incomplete. Whether a
 * row is superseded is its `current`, and no status.
 * @param {{ search?: string, hash?: string, age?: string, hide?: boolean, today?: string }} [opened]
 */
function page({ search = "", hash = "", age = "", hide = false, today = "2026-10-01" } = {}) {
  const ours = { source: "ours", status: "confirmed", current: "true" };
  const superseded = { source: "others", status: "confirmed", current: "false" };
  const structure = { source: "others", status: "incomplete", current: "true" };
  const reported = { source: "others", status: "recorded", current: "true" };
  // The projects a row is attributed to, a space apart: none for this project's rows.
  const none = { project: "" };
  const beta = { project: "beta-two" };
  const alpha = { project: "alpha-one" };
  const both = { project: "alpha-one beta-two" };
  const rows = [
    row("t-001", { ...ours, ...none, v: "4", c: "5", s: "5", n: "11", date: "2026-09-04" }),
    row(
      "t-002",
      { ...ours, ...none, v: "3", c: "2", s: "3", n: "17 18", date: "2026-08-31" },
      true,
    ),
    row(
      "t-003",
      { ...structure, ...beta, v: "0", c: "0", s: "2", n: "18-21 26", date: "1979-01-01" },
      true,
    ),
    row(
      "t-004",
      { ...reported, ...alpha, v: "4", c: "3", s: "3", n: "1-100", date: "2026-09-27" },
      true,
    ),
    row("t-005", { ...superseded, ...both, v: "4", c: "4", s: "4", n: "45", date: "2026-09-27" }),
  ];
  const controls = {
    s: new Select("s", "min", "4"),
    v: new Select("v", "min", ""),
    c: new Select("c", "min", ""),
    status: new Select("status", null, ""),
    hide: new Checkbox("current", hide),
    source: new Select("source", null, ""),
    n: new Input("n", "covers", ""),
    age: new Input("date", "age", age),
    project: new Preset("project", "has", ""),
    exact: new Preset("s", null, ""),
  };
  const presets = [controls.project, controls.exact];
  const count = { textContent: "2 of 5 results", getAttribute: () => "results" };
  /** @type {Record<string, (() => void)[]>} */
  const listeners = { change: [], hashchange: [], click: [] };
  const tools = {
    classList: {
      /** @param {string} name */
      contains: (name) => name === "site-table-tools",
    },
    /** @param {string} selector */
    querySelectorAll: (selector) =>
      selector === "[data-preset]" ? presets : Object.values(controls),
    querySelector: () => count,
    removeAttribute: () => undefined,
    /** @param {string} type @param {() => void} listener */
    addEventListener: (type, listener) => listeners[type]?.push(listener),
  };
  /** @type {Record<string, string>} */
  const sortable = { "data-sort": "text" };
  const heading = {
    tabIndex: -1,
    /** @param {string} name */
    getAttribute: (name) => sortable[name] ?? null,
    /** @param {string} name @param {string} value */
    setAttribute: (name, value) => {
      sortable[name] = value;
    },
    /** @param {string} name */
    hasAttribute: (name) => name in sortable,
    /** @param {string} type @param {() => void} listener */
    addEventListener: (type, listener) => listeners[type]?.push(listener),
  };
  const body = {
    rows,
    /** @param {ReturnType<typeof row>[]} sorted */
    append(...sorted) {
      this.rows = sorted;
    },
  };
  const table = Object.assign(new Table(), {
    tBodies: [body],
    tHead: { rows: [{ cells: [heading] }] },
    hasAttribute: () => false,
    setAttribute: () => undefined,
    closest: () => ({ previousElementSibling: tools }),
  });
  const location = { search, hash };
  vm.runInContext(
    SOURCE,
    vm.createContext({
      URLSearchParams,
      decodeURIComponent,
      Date: clock(today),
      location,
      document: {
        readyState: "complete",
        querySelector: () => null,
        querySelectorAll: () => [table],
      },
      window: {
        /** @param {string} type @param {() => void} listener */
        addEventListener: (type, listener) => listeners[type]?.push(listener),
      },
      HTMLAnchorElement: Label,
      HTMLSelectElement: Select,
      HTMLInputElement: Input,
      HTMLTableElement: Table,
      HTMLElement: Label,
    }),
  );
  /** @param {keyof typeof listeners} type */
  const fire = (type) => {
    for (const listener of listeners[type] ?? []) {
      listener();
    }
  };
  return {
    controls,
    count,
    location,
    /** The ids of the rows showing, in the table's order; every row is a result's. */
    shown: () => ({
      rows: body.rows.filter((entry) => !entry.hidden).map((entry) => entry.id),
    }),
    /**
     * Change the controls, then tell the bar, as a reader's choice does.
     * @param {Partial<Record<Exclude<keyof typeof controls, "hide">, string>>} values
     */
    choose(values) {
      for (const [name, value] of Object.entries(values)) {
        controls[/** @type {Exclude<keyof typeof controls, "hide">} */ (name)].value = value;
      }
      fire("change");
    },
    /**
     * Check or clear Hide superseded, then tell the bar.
     * @param {boolean} checked
     */
    check(checked) {
      controls.hide.checked = checked;
      fire("change");
    },
    fire,
  };
}

void test("the bar's state in the HTML is the default: S4 and up, already filtered", () => {
  const results = page();
  assert.deepEqual(results.shown(), { rows: ["t-001", "t-005"] });
  assert.equal(results.count.textContent, "2 of 5 results");
});

void test("All shows every row, and the count is of every row", () => {
  const results = page();
  results.choose({ s: "" });
  assert.deepEqual(results.shown(), { rows: ["t-001", "t-002", "t-003", "t-004", "t-005"] });
  assert.equal(results.count.textContent, "5 results");
});

void test("each facet filters, and the filters compose", () => {
  const results = page();
  /** @param {Parameters<typeof results.choose>[0]} values */
  const rows = (values) => {
    results.choose({
      ...{ s: "", v: "", c: "", status: "", source: "", n: "", age: "" },
      ...values,
    });
    return results.shown().rows;
  };
  assert.deepEqual(rows({ s: "3" }), ["t-001", "t-002", "t-004", "t-005"]);
  assert.deepEqual(rows({ v: "4" }), ["t-001", "t-004", "t-005"]);
  assert.deepEqual(rows({ c: "4" }), ["t-001", "t-005"]);
  assert.deepEqual(rows({ status: "confirmed" }), ["t-001", "t-002", "t-005"]);
  assert.deepEqual(rows({ status: "incomplete" }), ["t-003"]);
  assert.deepEqual(rows({ status: "recorded" }), ["t-004"]);
  assert.deepEqual(rows({ source: "ours" }), ["t-001", "t-002"]);
  assert.deepEqual(rows({ n: "18" }), ["t-002", "t-003", "t-004"]);
  // On 1 October the rows are 27, 31, some 17,000, 4 and 4 days old.
  assert.deepEqual(rows({ age: "30" }), ["t-001", "t-004", "t-005"]);
  assert.deepEqual(rows({ age: "31" }), ["t-001", "t-002", "t-004", "t-005"]);
  assert.deepEqual(rows({ age: "4" }), ["t-004", "t-005"]);
  assert.deepEqual(rows({ age: "3" }), []);
  assert.deepEqual(rows({ age: "30", source: "ours" }), ["t-001"]);
  assert.deepEqual(rows({ s: "3", source: "others", v: "4" }), ["t-004", "t-005"]);
  assert.deepEqual(rows({ s: "3", source: "others", v: "4", n: "45" }), ["t-004", "t-005"]);
  assert.deepEqual(rows({ s: "3", source: "others", v: "4", n: "45", c: "4" }), ["t-005"]);
  assert.equal(results.count.textContent, "1 of 5 results");
  assert.deepEqual(rows({ s: "5", source: "others" }), []);
  assert.equal(results.count.textContent, "0 of 5 results");
});

void test("Hide superseded hides the superseded rows and no other, whatever their status", () => {
  // The overview's bar: the box checked in the HTML, and the row it hides with it.
  const recent = page({ hide: true });
  assert.deepEqual(recent.shown(), { rows: ["t-001"] });
  assert.equal(recent.count.textContent, "1 of 5 results");
  // Every row that is current stays, whatever its status: the confirmed ones that still
  // hold, the recorded one and the incomplete one.
  recent.choose({ s: "" });
  assert.deepEqual(recent.shown(), { rows: ["t-001", "t-002", "t-003", "t-004"] });
  assert.equal(recent.count.textContent, "4 of 5 results");
  // It composes with Status, which asks a different question: each status shows its
  // rows that are current, and superseded is no status.
  recent.choose({ status: "recorded" });
  assert.deepEqual(recent.shown().rows, ["t-004"]);
  recent.choose({ status: "incomplete" });
  assert.deepEqual(recent.shown().rows, ["t-003"]);
  recent.choose({ status: "confirmed" });
  assert.deepEqual(recent.shown(), { rows: ["t-001", "t-002"] });
  assert.equal(recent.count.textContent, "2 of 5 results");
  // Cleared, it passes every row, as an empty control does: the superseded one returns.
  recent.check(false);
  assert.deepEqual(recent.shown().rows, ["t-001", "t-002", "t-005"]);
  recent.choose({ status: "" });
  assert.equal(recent.count.textContent, "5 results");
  recent.check(true);
  assert.deepEqual(recent.shown().rows, ["t-001", "t-002", "t-003", "t-004"]);
  // The results page's bar starts with it clear, and it composes with the rest there.
  const every = page();
  every.choose({ s: "" });
  assert.equal(every.count.textContent, "5 results");
  every.check(true);
  every.choose({ source: "others" });
  assert.deepEqual(every.shown().rows, ["t-003", "t-004"]);
  // The row the address names shows though it is superseded.
  assert.deepEqual(page({ hide: true, hash: "#t-005" }).shown().rows, ["t-001", "t-005"]);
});

void test("the row the address names shows whatever the filters hide", () => {
  const results = page({ hash: "#t-003" });
  assert.deepEqual(results.shown(), { rows: ["t-001", "t-003", "t-005"] });
  assert.equal(results.count.textContent, "3 of 5 results");
  results.location.hash = "#t-002";
  results.fire("hashchange");
  assert.deepEqual(results.shown().rows, ["t-001", "t-002", "t-005"]);
  results.location.hash = "#%E0%A4%A";
  results.fire("hashchange");
  assert.deepEqual(results.shown().rows, ["t-001", "t-005"]);
});

void test("an age is measured from the reader's day, again on every load", () => {
  // As the overview's Recent Results open: a significance floor, S4 here, and no older
  // than 180 days. The HTML's
  // `hidden` rows and count are as of the day the page was built, and are settled here.
  const recent = page({ age: "180" });
  assert.deepEqual(recent.shown(), { rows: ["t-001", "t-005"] });
  assert.equal(recent.count.textContent, "2 of 5 results");
  // The same HTML, opened later: 4 March 2027 is 181 days after t-001, 158 after t-005.
  const later = page({ age: "180", today: "2027-03-04" });
  assert.deepEqual(later.shown(), { rows: ["t-005"] });
  assert.equal(later.count.textContent, "1 of 5 results");
  assert.deepEqual(page({ age: "180", today: "2027-03-03" }).shown().rows, ["t-001", "t-005"]);
  assert.deepEqual(page({ age: "180", today: "2028-01-01" }).shown(), { rows: [] });
  // Clearing the age brings them back, whatever the day.
  later.choose({ age: "" });
  assert.deepEqual(later.shown().rows, ["t-001", "t-005"]);
  // The row the address names shows however old it is.
  assert.deepEqual(page({ age: "180", today: "2028-01-01", hash: "#t-003" }).shown().rows, [
    "t-003",
  ]);
});

void test("a link can open the table on one project's results, at one significance", () => {
  // `project` names a `has` control: the row's list of projects has the name among
  // them. `s` names the exact-significance control, beside the `s-min` floor. Both are
  // preset-only: out of the bar until a link sets them, and out again once cleared.
  const closed = page({ search: "?s-min=" });
  assert.equal(closed.controls.project.label.hidden, true);
  assert.equal(closed.controls.exact.label.hidden, true);
  const alpha = page({ search: "?s-min=&project=alpha-one" });
  assert.equal(alpha.controls.project.value, "alpha-one");
  assert.deepEqual(alpha.shown().rows, ["t-004", "t-005"]);
  assert.equal(alpha.count.textContent, "2 of 5 results");
  assert.equal(alpha.controls.project.label.hidden, false);
  assert.equal(alpha.controls.exact.label.hidden, true);
  // A row attributed to two projects is each one's.
  assert.deepEqual(page({ search: "?s-min=&project=beta-two" }).shown().rows, ["t-003", "t-005"]);
  // A name is held whole: part of one matches no row.
  assert.deepEqual(page({ search: "?s-min=&project=alpha" }).shown().rows, []);
  // With `s`, only the rows at that level: S3 exactly, where `s-min=3` keeps S4 too.
  const exact = page({ search: "?s-min=&project=alpha-one&s=3" });
  assert.deepEqual(exact.shown().rows, ["t-004"]);
  assert.equal(exact.controls.exact.label.hidden, false);
  assert.deepEqual(page({ search: "?s-min=3&project=alpha-one" }).shown().rows.length, 2);
  // The page's own defaults still apply to a link that does not clear them.
  assert.deepEqual(page({ search: "?project=alpha-one" }).shown().rows, ["t-005"]);
  // Set back to all, each control passes every row and leaves the bar again.
  exact.choose({ project: "", exact: "" });
  assert.equal(exact.count.textContent, "5 results");
  assert.equal(exact.controls.project.label.hidden, true);
  assert.equal(exact.controls.exact.label.hidden, true);
});

void test("a link can open the table filtered, by each control's parameter", () => {
  const results = page({ search: "?s-min=3&n=17&age=40" });
  assert.equal(results.controls.s.value, "3");
  assert.equal(results.controls.n.value, "17");
  assert.equal(results.controls.age.value, "40");
  assert.deepEqual(results.shown().rows, ["t-002", "t-004"]);
  assert.deepEqual(page({ search: "?s-min=3&n=17&age=30" }).shown().rows, ["t-004"]);
  assert.deepEqual(page({ search: "?s-min=" }).shown().rows.length, 5);
  // An empty parameter clears a default the HTML sets.
  assert.deepEqual(page({ age: "3", search: "?s-min=" }).shown().rows, []);
  assert.deepEqual(page({ age: "3", search: "?s-min=&age=" }).shown().rows.length, 5);
  // A checkbox is preset by `true`, and cleared by anything else, the empty value too.
  const hidden = page({ search: "?s-min=&current=true" });
  assert.equal(hidden.controls.hide.checked, true);
  assert.deepEqual(hidden.shown().rows, ["t-001", "t-002", "t-003", "t-004"]);
  for (const search of ["?s-min=&current=false", "?s-min=&current="]) {
    const cleared = page({ hide: true, search });
    assert.equal(cleared.controls.hide.checked, false);
    assert.equal(cleared.shown().rows.length, 5);
  }
  assert.equal(page({ hide: true, search: "?s-min=" }).controls.hide.checked, true);
});

void test("a sort keeps the filters, and the table is one flat list either way", () => {
  const results = page();
  results.fire("click");
  assert.deepEqual(results.shown(), { rows: ["t-001", "t-005"] });
  results.fire("click");
  assert.deepEqual(results.shown(), { rows: ["t-005", "t-001"] });
  results.choose({ s: "" });
  assert.deepEqual(results.shown(), { rows: ["t-005", "t-004", "t-003", "t-002", "t-001"] });
  assert.equal(results.count.textContent, "5 results");
});
