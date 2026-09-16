// The publication build's measurement. For every keyed math slot on the page, each
// unbreakable KaTeX `.base` is measured separately and wrapped in a fixed outer box that keeps
// its width, height and baseline in em; returns one fragment per slot for `prepared_html`.
//
// A reference probe: the file returns the slot measurement instead of being it, so that
// `page.evaluate_handle` can hand it to another probe. Evaluated through `applied`, it is
// called with the sorted math attribute names. The measurement of one base rides on it as
// `linearGeometry`, which the preparation-metrics control exercises on its own.
/** @returns {SquaresMeasureMath} */
() => {
  // One base's font size and width. Hinted advances are refused, and so is a width that does
  // not scale: a same-parent sample at 16 times the font size must agree within 1px.
  /** @param {HTMLElement} base */
  const linearGeometry = (base) => {
    const style = getComputedStyle(base);
    const fontSize = parseFloat(style.fontSize);
    const width = base.getBoundingClientRect().width;
    const native = document.documentElement.dataset.squaresNativeMathMetrics === "true";
    if (
      style.textRendering.toLowerCase() !== "geometricprecision" &&
      !(native && style.textRendering === "auto")
    ) {
      throw new Error(
        "math preparation requires geometricPrecision " +
          "or native linear metrics, got " +
          style.textRendering +
          ": " +
          base.textContent,
      );
    }
    const scale = 16;
    // A fresh same-parent sample keeps selector context and leaves the live
    // formula and its layout untouched.
    const probe = /** @type {HTMLElement} */ (base.cloneNode(true));
    probe.style.setProperty("font-size", `${fontSize * scale}px`, "important");
    probe.style.position = "absolute";
    probe.style.visibility = "hidden";
    base.after(probe);
    /** @type {number} */
    let linearWidth;
    /** @type {number} */
    let scaledFontSize;
    try {
      scaledFontSize = parseFloat(getComputedStyle(probe).fontSize);
      linearWidth = probe.getBoundingClientRect().width / scale;
    } finally {
      probe.remove();
    }
    if (!(fontSize > 0 && width > 0 && linearWidth > 0)) {
      throw new Error(`empty or hidden linear math geometry: ${base.textContent}`);
    }
    if (Math.abs(scaledFontSize - fontSize * scale) > 0.01) {
      throw new Error(
        "math scaling sample did not use the requested font size: " +
          scaledFontSize +
          "px instead of " +
          fontSize * scale +
          "px",
      );
    }
    if (Math.abs(width - linearWidth) > 1) {
      throw new Error(
        "math width does not scale linearly: " +
          width +
          "px at " +
          fontSize +
          "px versus " +
          linearWidth +
          "px normalized from " +
          scaledFontSize +
          "px: " +
          base.textContent,
      );
    }
    return { fontSize, width, linearWidth, textRendering: style.textRendering };
  };

  /** @param {string[]} attributeNames */
  const measureMath = (attributeNames) => {
    /** @param {number} value */
    const fixed = (value) => {
      if (!Number.isFinite(value)) {
        throw new Error("non-finite math geometry");
      }
      return `${Number(value.toFixed(8))}em`;
    };
    /** @type {SquaresPreparedFragment[]} */
    const result = [];
    for (const target of /** @type {NodeListOf<HTMLElement>} */ (
      document.querySelectorAll("[data-squares-math-key]")
    )) {
      const clone = /** @type {HTMLElement} */ (target.cloneNode(true));
      /**
       * @param {HTMLElement} element
       * @returns {(HTMLElement | null)[]}
       */
      const actualNodes = (element) =>
        element.matches(".kpress-math")
          ? [element.querySelector(".kpress-math-render")]
          : element.id.startsWith("kval-")
            ? [.../** @type {NodeListOf<HTMLElement>} */ (element.querySelectorAll(".math-item"))]
            : [element];
      const nodes = actualNodes(target),
        copies = actualNodes(clone);
      if (!nodes.length || nodes.length !== copies.length) {
        throw new Error(`missing initial parameter math: ${target.outerHTML.slice(0, 200)}`);
      }
      for (let index = 0; index < nodes.length; index++) {
        const node = nodes[index],
          copy = copies[index];
        if (
          !node ||
          !copy ||
          !node.querySelector(".katex") ||
          !node.hasAttribute("data-kpress-math-source")
        ) {
          throw new Error(`math did not finish preparing: ${target.outerHTML.slice(0, 200)}`);
        }
        const bases = [
          .../** @type {NodeListOf<HTMLElement>} */ (node.querySelectorAll(".katex-html > .base")),
        ];
        const clonedBases = [
          .../** @type {NodeListOf<HTMLElement>} */ (copy.querySelectorAll(".katex-html > .base")),
        ];
        if (!bases.length) {
          throw new Error("KaTeX emitted no measurable base");
        }
        for (let part = 0; part < bases.length; part++) {
          const base = /** @type {HTMLElement} */ (bases[part]),
            child = /** @type {HTMLElement} */ (clonedBases[part]);
          const measured = linearGeometry(base);
          const fontSize = measured.fontSize;
          const parentSize = parseFloat(
            getComputedStyle(/** @type {HTMLElement} */ (base.parentElement)).fontSize,
          );
          const marker = document.createElement("span");
          marker.style.cssText =
            "display:inline-block;width:0;height:0;padding:0;margin:0;" +
            "border:0;line-height:0;vertical-align:baseline;";
          base.append(marker);
          const rect = base.getBoundingClientRect();
          const baseline = marker.getBoundingClientRect().top;
          marker.remove();
          if (!(rect.width > 0 && rect.height > 0 && fontSize > 0 && parentSize > 0)) {
            throw new Error(`empty or hidden math geometry: ${node.textContent}`);
          }
          const box = document.createElement("span");
          box.className = "squares-math-box";
          box.style.cssText =
            "display:inline-block;position:relative;" +
            "font-size:" +
            fixed(fontSize / parentSize) +
            ";" +
            "width:" +
            fixed(rect.width / fontSize) +
            ";" +
            "height:" +
            fixed(rect.height / fontSize) +
            ";" +
            "vertical-align:" +
            fixed((baseline - rect.bottom) / fontSize) +
            ";";
          // The same em strut must anchor the actual glyphs and their reserved
          // box. A font's line strut rounds differently at print sizes; keep
          // its measured extent explicitly, including short punctuation bases.
          const strut = /** @type {HTMLElement | null} */ (child.querySelector(":scope > .strut"));
          if (!strut) {
            throw new Error("KaTeX emitted no baseline strut");
          }
          strut.style.height = fixed(rect.height / fontSize);
          strut.style.verticalAlign = fixed((baseline - rect.bottom) / fontSize);
          child.replaceWith(box);
          box.append(child);
          child.style.position = "absolute";
          child.style.left = "0";
          child.style.top = "0";
        }
        copy.dataset.kpressMathPrepared = "true";
        delete copy.dataset.squaresMathReady;
        delete copy.dataset.done;
      }
      clone.removeAttribute("data-squares-math-key");
      /** @type {Record<string, string>} */
      const attributes = {};
      for (const name of attributeNames) {
        if (clone.hasAttribute(name)) {
          attributes[name] = /** @type {string} */ (clone.getAttribute(name));
        }
      }
      result.push({
        key: Number(target.dataset.squaresMathKey),
        html: clone.innerHTML,
        attributes,
      });
    }
    return result;
  };

  return Object.assign(measureMath, { linearGeometry });
};
