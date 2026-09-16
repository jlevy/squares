// Diagnostic only: text-node ranges distinguish a moving operator baseline from its
// unchanged reserved box. DOM-order formula/token indices include hidden nodes, so
// identities do not shift merely because a print alternative becomes visible. FontFace
// status lists available faces; computed font-family is not proof of the selected face.
//
// A reference probe: the file returns the snapshot function, `(phase, selected)`, so
// `traced_settled` and `prepared_text_intervention` can be handed it as a handle, and
// `render_explainer_pdf.MATH_SNAPSHOT` applies it to evaluate it directly. `selected`, when
// given, collects each visible prepared Text node with its identity.
/**
 * @returns {(phase: string, selected?: SquaresSelectedText[] | null) => SquaresMathSnapshot}
 */
() =>
  (phase, selected = null) => {
    /** @param {DOMRect} r */
    const rect = (r) => ({ x: r.x, y: r.y, width: r.width, height: r.height });
    /** @param {Element} element */
    const visible = (element) =>
      element.checkVisibility({
        opacityProperty: true,
        visibilityProperty: true,
      });
    /** @param {HTMLElement} element */
    const metrics = (element) => {
      const style = getComputedStyle(element);
      return {
        class_name: element.className,
        rect: rect(element.getBoundingClientRect()),
        display: style.display,
        height: style.height,
        font_size: style.fontSize,
        line_height: style.lineHeight,
        vertical_align: style.verticalAlign,
        position: style.position,
        inline_style: element.style?.cssText || "",
      };
    };
    /** @type {SquaresMathSnapshot["tokens"]} */
    const tokens = [];
    /** @type {SquaresMathSnapshot["formulas"]} */
    const prepared = [];
    const limit = 10000;
    let truncated = false;
    const formulas = [
      .../** @type {NodeListOf<HTMLElement>} */ (
        document.querySelectorAll('[data-kpress-math-prepared="true"]')
      ),
    ];
    outer: for (const [formula, host] of formulas.entries()) {
      const html = host.querySelector(".katex-html");
      if (!html || !visible(html)) {
        continue;
      }
      const source = host.dataset.kpressMathSource || "";
      prepared.push({
        formula,
        source: source.slice(0, 4096),
        source_truncated: source.length > 4096,
        contexts: host.dataset.squaresMathContexts || "",
        host: metrics(host),
        boxes: [
          .../** @type {NodeListOf<HTMLElement>} */ (html.querySelectorAll(".squares-math-box")),
        ].map(metrics),
        bases: [.../** @type {NodeListOf<HTMLElement>} */ (html.querySelectorAll(".base"))].map(
          metrics,
        ),
        struts: [.../** @type {NodeListOf<HTMLElement>} */ (html.querySelectorAll(".strut"))].map(
          metrics,
        ),
      });
      const walker = document.createTreeWalker(html, NodeFilter.SHOW_TEXT);
      let token = -1;
      for (let node = walker.nextNode(); node; node = walker.nextNode()) {
        token++;
        const owner = node.parentElement;
        if (!(/** @type {string} */ (node.textContent).trim()) || !owner || !visible(owner)) {
          continue;
        }
        const range = document.createRange();
        range.selectNodeContents(node);
        const boxes = [...range.getClientRects()].filter((r) => r.width > 0 && r.height > 0);
        if (!boxes.length) {
          continue;
        }
        if (tokens.length === limit) {
          truncated = true;
          break outer;
        }
        const style = getComputedStyle(owner),
          path = [];
        for (
          let element = /** @type {Element | null} */ (owner);
          element && element !== host;
          element = element.parentElement
        ) {
          path.unshift(
            element.tagName.toLowerCase() +
              ":" +
              ([.../** @type {Element} */ (element.parentElement).children].indexOf(element) + 1),
          );
        }
        const identity = { formula, token, path: path.join("/") };
        if (selected !== null) {
          selected.push({ node: /** @type {Text} */ (node), ...identity });
        }
        const text = /** @type {string} */ (node.textContent);
        tokens.push({
          ...identity,
          text: text.slice(0, 512),
          text_truncated: text.length > 512,
          class_name: owner.className,
          element_rect: rect(owner.getBoundingClientRect()),
          text_rects: boxes.map(rect),
          font_family: style.fontFamily,
          font_size: style.fontSize,
          font_weight: style.fontWeight,
          font_style: style.fontStyle,
          line_height: style.lineHeight,
          vertical_align: style.verticalAlign,
          position: style.position,
          text_rendering: style.textRendering,
          font_kerning: style.fontKerning,
        });
      }
    }
    return {
      phase,
      time_ms: performance.now(),
      font_status: document.fonts.status,
      fonts: [...document.fonts].map((face) => ({
        family: face.family,
        style: face.style,
        weight: face.weight,
        stretch: face.stretch,
        status: face.status,
        unicode_range: face.unicodeRange,
      })),
      token_limit: limit,
      truncated,
      formulas: prepared,
      tokens,
    };
  };
