// The row popover script, run against a stand-in document: a table of two rows, each
// naming its popover, with a link and the native trigger in its cells. The stand-ins do
// what the platform does for a popover (`showPopover`, `hidePopover`, the `toggle`
// event, `:popover-open`) and for focus, so the test reads the script's own part:
// which presses open a row's popover, where focus goes, and what the row is told. A
// fourth row's body names a fuller one beside the page, which a stand-in `fetch` serves
// or refuses.
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import vm from "node:vm";

const SOURCE = readFileSync(
  new URL("../../../devtools/overview/row-popover.js", import.meta.url),
  "utf8",
);

const CASE_SOURCE = readFileSync(
  new URL("../../../devtools/overview/case-popover.js", import.meta.url),
  "utf8",
);

/** The script's own selectors, which is all the stand-in has to match. */
const COMPOUND = /^([a-z][a-z0-9]*)?((?:\[[^\]]+\]|\.[a-z-]+|:popover-open)*)$/;

/**
 * @typedef {object} Press what a test dispatches: a click or a key press
 * @property {number} [button]
 * @property {string} [key]
 * @property {boolean} [metaKey]
 * @property {boolean} [ctrlKey]
 * @property {boolean} [shiftKey]
 * @property {boolean} [altKey]
 * @property {string} [newState]
 */

/**
 * One page's stand-in classes and document, in a context of its own.
 * @param {string} [protocol] how the page was reached; `offline:` is `https:` with no
 *   network, so every fetch is refused
 */
function page(protocol = "https:") {
  class StandInElement {
    /**
     * @param {string} tag
     * @param {Record<string, string>} [attributes]
     * @param {StandInElement[]} [children]
     */
    constructor(tag, attributes = {}, children = []) {
      this.tag = tag;
      /** @type {Map<string, string>} */
      this.attributes = new Map(Object.entries(attributes));
      /** @type {StandInElement[]} */
      this.children = [];
      /** @type {StandInElement | null} */
      this.parentElement = null;
      /** @type {Map<string, ((event: object) => void)[]>} */
      this.listeners = new Map();
      this.tabIndex = tag === "a" || tag === "button" ? 0 : -1;
      this.open = false;
      /** @type {object | null} */
      this.sheet = null;
      /** @type {StandInElement | null} what a `<template>` holds, as its fragment */
      this.content = null;
      this.append(...children);
    }

    get id() {
      return this.attributes.get("id") ?? "";
    }

    /** @param {StandInElement[]} children */
    append(...children) {
      for (const child of children) {
        child.parentElement?.remove(child);
        child.parentElement = this;
        this.children.push(child);
      }
    }

    /** @param {StandInElement} [child] */
    remove(child) {
      if (child === undefined) {
        this.parentElement?.remove(this);
        this.parentElement = null;
      } else {
        this.children = this.children.filter((other) => other !== child);
      }
    }

    get href() {
      return new URL(this.getAttribute("href") || "", document.baseURI).href;
    }

    get target() {
      return this.getAttribute("target") || "";
    }

    scrollTo() {}

    /** @param {string} name */
    getAttribute(name) {
      return this.attributes.get(name) ?? null;
    }

    /** @param {string} name @param {string} value */
    setAttribute(name, value) {
      this.attributes.set(name, value);
    }

    /** @param {string} name */
    hasAttribute(name) {
      return this.attributes.has(name);
    }

    /** @param {string} name */
    removeAttribute(name) {
      this.attributes.delete(name);
    }

    /**
     * What a `<template>` is given to parse: one element holding the text.
     * @param {string} text
     */
    set innerHTML(text) {
      const isCase = text.includes('class="site-case"');
      const style = /<link data-site-math-styles href="([^"]+)"/.exec(text);
      const heading = /<h1 id="([^"]+)">/.exec(text);
      this.content = new StandInElement("fragment", {}, [
        ...(style
          ? [new StandInElement("link", { "data-site-math-styles": "", href: style[1] || "" })]
          : []),
        new StandInElement(
          "article",
          {
            class: isCase ? "site-case" : "site-result",
            ...(isCase ? { "data-case": "11" } : { "data-result-overview": "t-004" }),
            "data-text": text,
          },
          heading
            ? [
                new StandInElement("h1", { id: heading[1] || "" }),
                new StandInElement("a", { href: `#${heading[1] || ""}` }),
              ]
            : [],
        ),
      ]);
    }

    /** @param {StandInElement | null} fragment whose children become this element's */
    replaceChildren(fragment) {
      assert.ok(fragment !== null);
      for (const child of this.children) {
        child.parentElement = null;
      }
      this.children = [];
      this.append(...(fragment.tag === "fragment" ? fragment.children : [fragment]));
    }

    /** @param {string} selector */
    matches(selector) {
      return selector.split(",").some((part) => {
        const found = COMPOUND.exec(part.trim());
        assert.ok(found, `the stand-in does not read the selector ${part}`);
        const [, tag, rest = ""] = found;
        const conditions = rest.match(/\[[^\]]+\]|\.[a-z-]+|:popover-open/g) ?? [];
        return (
          (tag === undefined || tag === this.tag) &&
          conditions.every((condition) => {
            if (condition === ":popover-open") {
              return this.open;
            }
            if (condition.startsWith(".")) {
              return (this.attributes.get("class") ?? "").split(" ").includes(condition.slice(1));
            }
            const attribute = /^\[([a-z-]+)(?:([~]?=)"([^"]*)")?\]$/.exec(condition);
            assert.ok(attribute);
            const [, name = "", operator, value] = attribute;
            const actual = this.getAttribute(name);
            return operator === "="
              ? actual === value
              : operator === "~="
                ? (actual || "").split(" ").includes(value || "")
                : actual !== null;
          })
        );
      });
    }

    /** @param {string} selector @returns {StandInElement | null} */
    closest(selector) {
      /** @type {StandInElement | null} */
      let element = this;
      while (element !== null && !element.matches(selector)) {
        element = element.parentElement;
      }
      return element;
    }

    /** @param {unknown} other @returns {boolean} */
    contains(other) {
      return other === this || this.children.some((child) => child.contains(other));
    }

    /** @param {string} selector @returns {StandInElement[]} */
    querySelectorAll(selector) {
      return this.children.flatMap((child) => [
        ...(child.matches(selector) ? [child] : []),
        ...child.querySelectorAll(selector),
      ]);
    }

    /** @param {string} selector */
    querySelector(selector) {
      return this.querySelectorAll(selector)[0] ?? null;
    }

    /** @param {string} type @param {(event: object) => void} listener */
    addEventListener(type, listener) {
      this.listeners.set(type, [...(this.listeners.get(type) ?? []), listener]);
    }

    focus() {
      document.activeElement = this;
    }

    /** @param {StandInElement | null} fragment whose children take this element's place */
    replaceWith(fragment) {
      const parent = this.parentElement;
      assert.ok(parent !== null && fragment !== null);
      const placed = fragment.children;
      parent.children.splice(parent.children.indexOf(this), 1, ...placed);
      for (const child of placed) {
        child.parentElement = parent;
      }
      fragment.children = [];
      this.parentElement = null;
    }

    showPopover() {
      assert.ok(!this.open, "showPopover on an open popover throws in a browser");
      fire(this, "beforetoggle", { newState: "open" });
      this.open = true;
      fire(this, "toggle", { newState: "open" });
    }

    hidePopover() {
      this.open = false;
      /** @type {object | null} */
      this.sheet = null;
      fire(this, "toggle", { newState: "closed" });
    }
  }

  class StandInToggleEvent {
    /** @param {string} newState */
    constructor(newState) {
      this.newState = newState;
    }
  }

  const body = new StandInElement("body");
  const head = new StandInElement("head");
  /** @type {Map<string, ((event: object) => void)[]>} */
  const documentListeners = new Map();
  const document = {
    readyState: "complete",
    body,
    head,
    baseURI: "https://example.test/squares/index.html",
    /** @type {StandInElement | null} */
    activeElement: body,
    /**
     * What the reader has selected; a collapsed selection is none.
     * @type {{ isCollapsed: boolean, anchorNode: StandInElement | null }}
     */
    selection: { isCollapsed: true, anchorNode: null },
    getSelection: () => document.selection,
    /** @param {string} tag */
    createElement: (tag) => new StandInElement(tag),
    /** @param {string} id */
    getElementById: (id) =>
      [body, ...body.querySelectorAll("[id]")].find((element) => element.id === id) ?? null,
    /** @param {string} selector */
    querySelectorAll: (selector) => [
      ...head.querySelectorAll(selector),
      ...body.querySelectorAll(selector),
    ],
    /** @param {string} selector */
    querySelector: (selector) => body.querySelector(selector),
    /** @param {string} type @param {(event: object) => void} listener */
    addEventListener: (type, listener) =>
      documentListeners.set(type, [...(documentListeners.get(type) || []), listener]),
  };

  /**
   * Dispatch an event at `target`, bubbling to the body. Returns whether its default was
   * prevented, which for a click on a trigger is whether the platform's own opening ran.
   * @param {StandInElement} target
   * @param {string} type
   * @param {Press} [init]
   */
  function fire(target, type, init = {}) {
    const toggles = type === "toggle" || type === "beforetoggle";
    const kind = toggles ? new StandInToggleEvent(init.newState ?? "") : {};
    const event = Object.assign(kind, {
      button: 0,
      metaKey: false,
      ctrlKey: false,
      shiftKey: false,
      altKey: false,
      ...init,
      type,
      target,
      defaultPrevented: false,
      preventDefault() {
        this.defaultPrevented = true;
      },
    });
    // The toggle events do not bubble; a click and a key press do.
    /** @type {StandInElement[]} */
    const path = [];
    for (
      let element = /** @type {StandInElement | null} */ (target);
      element !== null;
      element = toggles ? null : element.parentElement
    ) {
      path.push(element);
    }
    for (const element of path) {
      for (const listener of element.listeners.get(type) ?? []) {
        listener(event);
      }
    }
    if (!toggles) {
      for (const listener of documentListeners.get(type) || []) {
        listener(event);
      }
    }
    return event.defaultPrevented;
  }

  /**
   * A row with detail and its popover, as `overview_sections.row_detail` writes them.
   * @param {string} key
   * @param {Record<string, string>} [more] further attributes of the row, such as `hidden`
   * @param {boolean} [deferred] whether the popover's body waits in a template
   * @param {string} [source] the fuller body the popover's body names, if it names one
   */
  function row(key, more = {}, deferred = false, source = "") {
    const target = `pop-${key}`;
    const trigger = new StandInElement("button", { class: "site-row-open", popovertarget: target });
    const link = new StandInElement("a", { href: `records/${key}` });
    const text = new StandInElement("td");
    const attributes = { id: key, "data-row-popover": target, ...more };
    const element = new StandInElement("tr", attributes, [
      new StandInElement("td", {}, [trigger]),
      text,
      new StandInElement("td", {}, [link]),
    ]);
    const close = new StandInElement("button", { class: "site-popover-close" });
    const detail = new StandInElement("a", { href: `detail/${key}` });
    const held = new StandInElement("template", { "data-row-pop-body": "" });
    held.content = new StandInElement("fragment", {}, [detail]);
    const body = new StandInElement(
      "div",
      { class: "site-row-pop-body", ...(source ? { "data-row-pop-src": source } : {}) },
      [deferred ? held : detail],
    );
    const title = new StandInElement("p", { class: "site-popover-value", id: `${target}-title` });
    const label = new StandInElement("span", { class: "site-card-label" });
    const popover = new StandInElement(
      "div",
      { id: target, class: "site-popover", "aria-labelledby": title.id },
      [close, label, title, body],
    );
    return { element, trigger, link, text, popover, close, body, held, detail };
  }

  const first = row("t-001");
  // The second row is one the filters hide at load, as a results table writes it, and
  // its popover's body is deferred.
  const second = row("t-002", { hidden: "" }, true);
  // A row naming a popover the page does not carry: its popover is never appended.
  const orphan = row("t-003");
  // A row whose popover holds a short body and names the fuller one beside the page.
  const fetched = row("t-004", {}, false, "result/t-004.html");
  const tbody = new StandInElement("tbody", {}, [
    first.element,
    second.element,
    orphan.element,
    fetched.element,
  ]);
  body.append(
    new StandInElement("table", {}, [tbody]),
    first.popover,
    second.popover,
    fetched.popover,
  );

  const caseBody = new StandInElement("div", { "data-case-body": "" });
  const caseAction = new StandInElement("a", { "data-case-open": "" });
  const caseClose = new StandInElement("button", { class: "site-popover-close" });
  const casePopover = new StandInElement("div", { "data-case-popover": "", id: "case-popover" }, [
    caseBody,
    caseAction,
    caseClose,
  ]);
  const caseLink = new StandInElement("a", { "data-case": "11", href: "cases/11.html" });
  body.append(casePopover, caseLink);

  /** What the site serves, by address; an address it lacks is a 404. */
  const served = new Map([
    ["result/t-004.html", "the whole overview of t-004"],
    [caseLink.href, '<article class="site-case">Case 11</article>'],
  ]);
  /** @type {Map<string, string>} */
  const responseURLs = new Map();
  /** @type {string[]} every address asked for, in order */
  const requests = [];
  /** @type {StandInElement[]} every root the math driver was asked to typeset */
  const typeset = [];
  /** @type {Promise<unknown>[]} */
  const pending = [];
  /** @param {string} address */
  const fetch = (address) => {
    requests.push(address);
    const text = served.get(address);
    const response =
      protocol === "offline:"
        ? Promise.reject(new TypeError("Failed to fetch"))
        : Promise.resolve({
            url: responseURLs.get(address) || new URL(address, document.baseURI).href,
            ok: text !== undefined,
            status: text === undefined ? 404 : 200,
            text: () => Promise.resolve(text ?? "Not found"),
          });
    pending.push(response.catch(() => undefined));
    return response;
  };
  /** Wait until every fetch so far, and what the script chained on it, has run. */
  const settled = async () => {
    await Promise.all(pending);
    await new Promise((resolve) => setImmediate(resolve));
  };

  const navigation = { protocol: protocol === "offline:" ? "https:" : protocol, href: "" };
  const context = vm.createContext({
    document,
    URL,
    fetch,
    location: navigation,
    siteMath: {
      /** @param {StandInElement} root */
      typeset: (root) => {
        typeset.push(root);
        return Promise.resolve();
      },
    },
    Element: StandInElement,
    HTMLElement: StandInElement,
    HTMLTemplateElement: StandInElement,
    HTMLAnchorElement: StandInElement,
    HTMLTableRowElement: StandInElement,
    HTMLLinkElement: StandInElement,
    ToggleEvent: StandInToggleEvent,
  });
  vm.runInContext(SOURCE, context);
  vm.runInContext(CASE_SOURCE, context);
  return {
    document,
    fire,
    first,
    second,
    orphan,
    fetched,
    tbody,
    served,
    responseURLs,
    navigation,
    caseBody,
    caseLink,
    casePopover,
    requests,
    typeset,
    settled,
  };
}

void test("a row with detail becomes one tab stop, collapsed, naming its popover", () => {
  const { first } = page();
  assert.equal(first.element.tabIndex, 0);
  assert.equal(first.trigger.tabIndex, -1);
  assert.equal(first.link.tabIndex, 0);
  assert.equal(first.element.getAttribute("aria-expanded"), "false");
  assert.equal(first.element.getAttribute("aria-controls"), "pop-t-001");
});

void test("a click anywhere on the row opens its popover and moves focus to the cross", () => {
  const { document, fire, first, second } = page();
  fire(first.text, "click");
  assert.ok(first.popover.open);
  assert.ok(!second.popover.open);
  assert.equal(document.activeElement, first.close);
  assert.equal(first.element.getAttribute("aria-expanded"), "true");
  assert.equal(second.element.getAttribute("aria-expanded"), "false");
});

void test("Enter and Space on the focused row open it, and no other key does", () => {
  for (const key of ["Enter", " "]) {
    const { fire, first } = page();
    assert.ok(fire(first.element, "keydown", { key }), "the key's own action is prevented");
    assert.ok(first.popover.open, key);
  }
  const { fire, first } = page();
  assert.ok(!fire(first.element, "keydown", { key: "ArrowDown" }));
  assert.ok(!fire(first.element, "keydown", { key: "Enter", ctrlKey: true }));
  assert.ok(!first.popover.open);
});

void test("a link in the row stays a link: neither a click nor Enter on it opens the popover", () => {
  const { fire, first } = page();
  assert.ok(!fire(first.link, "click"), "the link's own navigation is left alone");
  assert.ok(!fire(first.link, "keydown", { key: "Enter" }));
  assert.ok(!first.popover.open);
});

void test("the native trigger opens through the row's one path, not twice", () => {
  const { document, fire, first } = page();
  // Left alone, the platform would toggle the popover after this click; preventing it
  // leaves the script's own opening, which also moves focus.
  assert.ok(fire(first.trigger, "click"));
  assert.ok(first.popover.open);
  assert.equal(document.activeElement, first.close);
});

void test("a modified click, another button, or a click ending a selection does not open", () => {
  const { document, fire, first } = page();
  fire(first.text, "click", { metaKey: true });
  fire(first.text, "click", { shiftKey: true });
  fire(first.text, "click", { button: 1 });
  document.selection = { isCollapsed: false, anchorNode: first.text };
  fire(first.text, "click");
  assert.ok(!first.popover.open);
  document.selection = { isCollapsed: true, anchorNode: null };
  fire(first.text, "click");
  assert.ok(first.popover.open);
});

void test("closing, as the cross and Escape do, collapses the row and returns focus to it", () => {
  const { document, fire, first } = page();
  fire(first.text, "click");
  first.popover.hidePopover();
  assert.equal(first.element.getAttribute("aria-expanded"), "false");
  assert.equal(document.activeElement, first.element);
});

void test("closing leaves focus where the reader has already moved it", () => {
  const { document, fire, first, second } = page();
  fire(first.text, "click");
  // A press on another row closes this popover by light dismiss, focus already there.
  second.element.focus();
  first.popover.hidePopover();
  assert.equal(document.activeElement, second.element);
  assert.equal(first.element.getAttribute("aria-expanded"), "false");
});

void test("a row moved by a sort still opens its own popover", () => {
  const { fire, first, second, tbody } = page();
  tbody.append(first.element);
  assert.deepEqual(
    tbody.children.map((element) => element.id),
    ["t-002", "t-003", "t-004", "t-001"],
  );
  fire(second.text, "click");
  assert.ok(second.popover.open);
  assert.ok(!first.popover.open);
  second.popover.hidePopover();
  fire(first.text, "click");
  assert.ok(first.popover.open);
});

void test("pressing a row whose popover is open does not open it again", () => {
  const { fire, first } = page();
  fire(first.text, "click");
  // `showPopover` on an open popover throws in a browser, and in the stand-in.
  fire(first.element, "keydown", { key: "Enter" });
  assert.ok(first.popover.open);
});

void test("a row whose popover is not on the page is left as the HTML has it", () => {
  const { document, fire, first, orphan } = page();
  assert.equal(document.getElementById("pop-t-001"), first.popover);
  assert.equal(document.getElementById("pop-t-003"), null);
  assert.ok(first.element.hasAttribute("data-row-ready"));
  assert.ok(!orphan.element.hasAttribute("data-row-ready"));
  assert.equal(orphan.element.tabIndex, -1);
  assert.equal(orphan.trigger.tabIndex, 0);
  assert.ok(!orphan.element.hasAttribute("aria-expanded"));
  assert.ok(!fire(orphan.text, "click"));
});

void test("a row the filters hide at load is wired all the same, for when they show it", () => {
  const { document, fire, second } = page();
  assert.ok(second.element.hasAttribute("hidden"));
  assert.equal(second.element.tabIndex, 0);
  assert.equal(second.trigger.tabIndex, -1);
  fire(second.text, "click");
  assert.ok(second.popover.open);
  assert.equal(document.activeElement, second.close);
});

void test("a body held in a template is placed when its popover first opens, and once", () => {
  const { fire, first, second } = page();
  assert.deepEqual(second.body.children, [second.held]);
  fire(second.text, "click");
  assert.deepEqual(second.body.children, [second.detail]);
  assert.equal(second.detail.parentElement, second.body);
  second.popover.hidePopover();
  fire(second.element, "keydown", { key: "Enter" });
  assert.deepEqual(second.body.children, [second.detail]);
  // A body written in place is left as it is.
  fire(first.text, "click");
  assert.deepEqual(first.body.children, [first.detail]);
});

void test("the platform's own opening places a deferred body too", () => {
  const { second } = page();
  // What the native trigger does when the script has not taken the click.
  second.popover.showPopover();
  assert.deepEqual(second.body.children, [second.detail]);
});

void test("a body that names a fuller one is replaced by it when the popover first opens", async () => {
  const { fire, fetched, requests, typeset, settled } = page();
  assert.deepEqual(fetched.body.children, [fetched.detail]);
  fire(fetched.text, "click");
  // The short body is what the popover shows until the fuller one lands.
  assert.ok(fetched.popover.open);
  assert.deepEqual(fetched.body.children, [fetched.detail]);
  assert.ok(fetched.body.hasAttribute("data-row-pop-loading"));
  await settled();
  assert.deepEqual(requests, ["result/t-004.html"]);
  assert.deepEqual(
    fetched.body.children.map((child) => child.getAttribute("data-text")),
    ["the whole overview of t-004"],
  );
  assert.ok(!fetched.body.hasAttribute("data-row-pop-src"));
  assert.ok(!fetched.body.hasAttribute("data-row-pop-loading"));
  // It landed in an open popover, so its math is typeset here.
  assert.deepEqual(typeset, [], "the fetched record already contains rendered math");
  fetched.popover.hidePopover();
  fire(fetched.text, "click");
  await settled();
  assert.deepEqual(requests, ["result/t-004.html"], "fetched once");
});

void test("a press starts the fetch, and a body that lands before the popover opens waits for popover.js", async () => {
  const { fire, fetched, requests, typeset, settled } = page();
  fire(fetched.text, "pointerdown");
  assert.deepEqual(requests, ["result/t-004.html"]);
  // The click that follows the press finds the fetch under way and starts no other.
  await settled();
  assert.ok(!fetched.popover.open);
  assert.deepEqual(typeset, [], "a closed popover's math is left to its opening");
  fire(fetched.text, "click");
  await settled();
  assert.deepEqual(requests, ["result/t-004.html"]);
  assert.equal(fetched.body.children.length, 1);
  assert.equal(fetched.body.children[0]?.getAttribute("class"), "site-result");
});

void test("a body that cannot be fetched keeps its short form, and the next opening asks again", async () => {
  for (const reach of ["missing", "offline:"]) {
    const { fire, fetched, served, requests, typeset, settled } = page(
      reach === "offline:" ? reach : "https:",
    );
    served.clear();
    fire(fetched.text, "click");
    await settled();
    assert.deepEqual(fetched.body.children, [fetched.detail], reach);
    assert.equal(fetched.body.getAttribute("data-row-pop-src"), "result/t-004.html");
    assert.ok(!fetched.body.hasAttribute("data-row-pop-loading"));
    const fallback = fetched.popover.querySelector(".site-popover-value");
    assert.ok(fallback);
    assert.equal(fetched.popover.getAttribute("aria-labelledby"), fallback.id);
    assert.ok(fetched.popover.querySelector(".site-card-label"));
    assert.deepEqual(typeset, []);
    fetched.popover.hidePopover();
    fire(fetched.text, "click");
    await settled();
    assert.equal(requests.length, 2, reach);
  }
});

void test("the complete article title replaces outer titles and has a dialog-specific id", async () => {
  const { document, fire, fetched, served, settled } = page();
  served.set(
    "result/t-004.html",
    '<article class="site-result"><h1 id="t-004">T-004: Result</h1><a href="#t-004">Title</a></article>',
  );
  fire(fetched.text, "click");
  await settled();
  const heading = fetched.body.querySelector("h1");
  assert.ok(heading);
  assert.equal(fetched.popover.querySelector(".site-card-label"), null);
  assert.equal(fetched.popover.querySelector(".site-popover-value"), null);
  assert.equal(heading.id, "pop-t-004-record-title");
  assert.equal(fetched.popover.getAttribute("aria-labelledby"), heading.id);
  assert.equal(document.getElementById(heading.id), heading);
  assert.equal(document.getElementById("t-004"), fetched.element);
  assert.equal(fetched.body.querySelector("a")?.getAttribute("href"), `#${heading.id}`);
});

void test("a page read from a file fetches nothing and keeps the short body", async () => {
  const { fire, fetched, requests, settled } = page("file:");
  fire(fetched.text, "pointerdown");
  fire(fetched.text, "click");
  await settled();
  assert.deepEqual(requests, []);
  assert.deepEqual(fetched.body.children, [fetched.detail]);
  assert.ok(fetched.popover.open);
});

void test("a row whose body names nothing fetches nothing", async () => {
  const { fire, first, second, requests, settled } = page();
  fire(first.text, "pointerdown");
  fire(first.text, "click");
  fire(second.text, "click");
  await settled();
  assert.deepEqual(requests, []);
});

void test("case and result articles wait for one shared response-relative metric stylesheet", async () => {
  const { document, fire, fetched, served, caseBody, caseLink, casePopover, settled } = page();
  const marker = '<link data-site-math-styles href="../assets/css/site-math-profile.css">';
  served.set("result/t-004.html", `${marker}Result 4`);
  served.set(caseLink.href, `${marker}<article class="site-case">Case 11</article>`);
  assert.equal(document.head.children.length, 0, "nothing loads before input");
  fire(fetched.text, "pointerdown");
  fire(caseLink, "click");
  await settled();
  assert.equal(document.head.children.length, 1, "pending stylesheet shared across both scripts");
  const stylesheet = document.head.children[0];
  assert.ok(stylesheet);
  assert.equal(stylesheet.href, "https://example.test/squares/assets/css/site-math-profile.css");
  assert.deepEqual(fetched.body.children, [fetched.detail]);
  assert.equal(caseBody.children.length, 0);
  assert.equal(casePopover.open, false);
  stylesheet.sheet = {};
  fire(stylesheet, "load");
  await settled();
  assert.equal(fetched.body.children[0]?.getAttribute("class"), "site-result");
  assert.equal(caseBody.children[0]?.getAttribute("class"), "site-case");
  assert.equal(casePopover.open, true);
});

void test("a failed metric stylesheet preserves the row fallback and can be retried", async () => {
  const { document, fire, fetched, served, settled } = page();
  served.set(
    "result/t-004.html",
    '<link data-site-math-styles href="../assets/css/site-math-retry.css">Result',
  );
  fire(fetched.text, "pointerdown");
  await settled();
  const stylesheet = document.head.children[0];
  assert.ok(stylesheet);
  fire(stylesheet, "error");
  await settled();
  assert.deepEqual(fetched.body.children, [fetched.detail]);
  assert.equal(document.head.children.length, 0);
  fire(fetched.text, "pointerdown");
  await settled();
  assert.equal(document.head.children.length, 1);
  const retry = document.head.children[0];
  assert.ok(retry);
  fire(retry, "load");
  await settled();
  assert.equal(fetched.body.children[0]?.getAttribute("class"), "site-result");
});

void test("only this site's stylesheet namespace is accepted", async () => {
  for (const href of ["https://other.test/assets/css/math.css", "../unrelated/math.css"]) {
    const { document, fire, fetched, served, settled } = page();
    served.set("result/t-004.html", `<link data-site-math-styles href="${href}">Result`);
    fire(fetched.text, "pointerdown");
    await settled();
    assert.equal(document.head.children.length, 0);
    assert.deepEqual(fetched.body.children, [fetched.detail]);
    assert.ok(!fetched.body.hasAttribute("data-row-pop-loading"));
  }
});

void test("already loaded metric rules are reused without another request", async () => {
  const { document, fire, fetched, served, settled } = page();
  const link = document.createElement("link");
  link.setAttribute("href", "assets/css/site-math-existing.css");
  link.setAttribute("data-site-math-styles", "");
  link.sheet = {};
  document.head.append(link);
  served.set(
    "result/t-004.html",
    '<link data-site-math-styles href="../assets/css/site-math-existing.css">Result',
  );
  fire(fetched.text, "pointerdown");
  await settled();
  assert.equal(document.head.children.length, 1);
  assert.equal(fetched.body.children[0]?.getAttribute("class"), "site-result");
});

void test("a case stylesheet failure follows the ordinary case link and retries on a later input", async () => {
  const { document, fire, served, caseLink, caseBody, navigation, requests, settled } = page();
  served.set(
    caseLink.href,
    '<link data-site-math-styles href="../assets/css/site-math-case.css"><article class="site-case">Case 11</article>',
  );
  fire(caseLink, "click");
  await settled();
  const link = document.head.children[0];
  assert.ok(link);
  fire(link, "error");
  await settled();
  assert.equal(navigation.href, caseLink.href);
  assert.equal(caseBody.children.length, 0);
  fire(caseLink, "click");
  await settled();
  assert.equal(requests.length, 2);
  assert.equal(document.head.children.length, 1);
  const retry = document.head.children[0];
  assert.ok(retry);
  fire(retry, "load");
  await settled();
  assert.equal(caseBody.children[0]?.getAttribute("class"), "site-case");
});

void test("the canonical response address resolves its prepared stylesheet", async () => {
  const { document, fire, served, caseLink, responseURLs, caseBody, settled } = page();
  responseURLs.set(caseLink.href, "https://example.test/edition/cases/11.html");
  served.set(
    caseLink.href,
    '<link data-site-math-styles href="../assets/css/site-math-response.css"><article class="site-case">Case 11</article>',
  );
  fire(caseLink, "click");
  await settled();
  const link = document.head.children[0];
  assert.ok(link);
  assert.equal(link.href, "https://example.test/edition/assets/css/site-math-response.css");
  fire(link, "load");
  await settled();
  assert.equal(caseBody.children[0]?.getAttribute("class"), "site-case");
});
