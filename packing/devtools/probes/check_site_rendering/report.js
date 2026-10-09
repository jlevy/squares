// A single layout read after load and font settlement, followed by scroll sampling.
() => {
  const sampleStart = performance.now();
  /** @type {{supported: boolean, cls: number, lcpMs: number, longestTaskMs: number, blockingMs: number, shifts: number, readabilitySamples?: {startTime: number, durationMs: number}[]} | undefined} */
  const timing = Reflect.get(window, "siteRenderingMeasure");
  const math = [...document.querySelectorAll(".kpress-math, .tex, .tex-d")].filter(
    (element) => !element.parentElement?.closest(".kpress-math, .tex, .tex-d"),
  );
  /** @param {Element | null} element */
  const visible = (element) =>
    element instanceof HTMLElement &&
    element.getClientRects().length > 0 &&
    getComputedStyle(element).visibility !== "hidden";
  // Native collapsed sections may contain additional formulas. A hidden formula in
  // primary prose must fail rather than disappear from the no-JavaScript sample.
  const shown = math.filter((element) => {
    if (element.closest("[popover]:not(:popover-open)")) {
      return false;
    }
    const closed = element.closest("details:not([open])");
    if (closed && !element.closest("summary")) {
      return false;
    }
    // Only known optional controls/content may be absent initially. A generic
    // hidden ancestor is primary content and must remain in the readability sample.
    const held = element.closest(
      ".site-atlas-rest[data-atlas-rest][hidden], .site-table tbody tr[hidden], " +
        ".site-table-tools[hidden], .site-table-tools label[hidden], " +
        ".cert-figure[data-cert][hidden]",
    );
    // CSS may reveal a filtered row (including the no-script view) or certificate
    // while retaining its hidden attribute. Inspect that content when it has a box.
    return !held || visible(held);
  });
  const unreadable = shown.filter((element) => {
    if (element.getAttribute("data-site-native-math") === "frontier") {
      if (!visible(element) || !element.closest(".site-frontier td")) {
        return true;
      }
      const namespace = "http://www.w3.org/1998/Math/MathML";
      const roots = [...element.children].filter(
        (node) => node.namespaceURI === namespace && node.localName === "math",
      );
      const root = roots[0];
      if (roots.length !== 1 || !root || root.querySelector("merror")) {
        return true;
      }
      const box = root.getBoundingClientRect();
      if (box.width <= 0 || box.height <= 0 || getComputedStyle(root).visibility === "hidden") {
        return true;
      }
      // A visible host or empty math box does not prove mathematical text is drawn.
      return ![...root.querySelectorAll("mi, mn, mo, mtext, ms")].some((node) => {
        const token = node.getBoundingClientRect();
        return (
          node.namespaceURI === namespace &&
          (node.textContent ?? "").trim().length > 0 &&
          token.width > 0 &&
          token.height > 0 &&
          getComputedStyle(node).visibility !== "hidden"
        );
      });
    }
    const visual = [...element.querySelectorAll(".katex-html")].find(
      (node) => node.getClientRects().length && getComputedStyle(node).visibility !== "hidden",
    );
    return !visible(element) || !visual;
  });
  const article = [...document.querySelectorAll("article, main")].find(visible);
  const h1 = [...document.querySelectorAll("h1")].find(visible);
  const figures = [...document.querySelectorAll("main img, article img")];
  const report = {
    ...timing,
    // biome-ignore lint/nursery/useDomNodeTextContent: the gate measures rendered readable text, excluding hidden content.
    contentChars: (article instanceof HTMLElement ? article.innerText : "").trim().length ?? 0,
    // biome-ignore lint/nursery/useDomNodeTextContent: a hidden heading must not pass the reading contract.
    heading: h1 instanceof HTMLElement ? h1.innerText.trim() : "",
    shownMath: shown.length,
    unreadableMath: unreadable.length,
    unreservedImages: figures.filter(
      (image) => !image.hasAttribute("width") || !image.hasAttribute("height"),
    ).length,
    pending: document.querySelectorAll("[data-kpress-math-pending]").length,
  };
  // This identifies work performed by the checker without removing it from native
  // timing. An overlap can then be inspected instead of guessing from one scalar.
  const sample = { startTime: sampleStart, durationMs: performance.now() - sampleStart };
  const samples = timing?.readabilitySamples;
  if (samples && samples.length < 100) {
    samples.push(sample);
  }
  return report;
};
