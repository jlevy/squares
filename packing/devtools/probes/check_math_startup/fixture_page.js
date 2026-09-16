// The startup fixture page's script: a small stand-in for KaTeX, kpress's math runtime and
// the host adapter, with the same public API and Figure 6 output contract as the published
// page. `mode` selects the control: `control`, `no-warmup`, `delayed`, `variants`,
// `wrong-active-variant`, `missing-math`, `missing-counters`, `late-target`, `width-change`
// or `missing-anchors`. Only these fixtures introduce delays or changed widths.
/** @param {{ mode: string }} o */
({ mode }) => {
  if (mode === "missing-anchors") {
    const paragraph = /** @type {HTMLElement} */ (document.getElementById("prose"));
    paragraph.replaceChildren(/** @type {Element} */ (paragraph.querySelector(".tex")));
  }
  if (mode === "missing-counters") {
    /** @type {SquaresMathStartupState} */ (globalThis.__mathStartup).counters.font_hooks = 0;
  }
  globalThis.katex = /** @type {SquaresKatex} */ (
    /** @type {unknown} */ ({
      /**
       * @param {string} source
       * @param {Element} node
       */
      render(source, node) {
        const katex = document.createElement("span");
        katex.className = "katex";
        const hidden = document.createElement("span");
        hidden.className = "katex-mathml";
        const annotation = document.createElement("annotation");
        annotation.setAttribute("encoding", "application/x-tex");
        annotation.textContent = source;
        hidden.append(annotation);
        katex.append(hidden);
        const html = document.createElement("span");
        html.className = "katex-html";
        html.textContent = source;
        katex.append(html);
        node.replaceChildren(katex);
      },
    })
  );
  const gate =
    mode === "delayed" || mode === "width-change"
      ? new Promise((resolve) => setTimeout(resolve, 300))
      : Promise.resolve();
  globalThis.kpressMathText = /** @type {KpressMathText} */ (
    /** @type {unknown} */ ({
      ready() {
        return gate;
      },
      /**
       * @param {string} source
       * @param {Element} node
       */
      render(source, node) {
        katex.render(source, node);
        return Promise.resolve();
      },
      complete() {
        delete document.documentElement.dataset.kpressMathPending;
      },
    })
  );
  const ready =
    mode === "no-warmup" ? gate : /** @type {KpressMathText} */ (kpressMathText).ready();
  /** @type {((value?: unknown) => void) | undefined} */
  let releaseLateTarget;
  const lateTarget =
    mode === "late-target"
      ? new Promise((resolve) => {
          releaseLateTarget = resolve;
        })
      : Promise.resolve();
  globalThis.squaresMath = /** @type {SquaresMathHost} */ (
    /** @type {unknown} */ ({ ready, settled: () => lateTarget })
  );
  void document.fonts.load("16px serif");
  void ready.then(async () => {
    for (const node of document.querySelectorAll(".tex")) {
      await /** @type {KpressMathText} */ (kpressMathText).render(
        /** @type {string} */ (node.textContent),
        node,
      );
    }
    for (const [key, source] of Object.entries({
      phi: "19.600^{\\circ}",
      theta: "15.000^{\\circ}",
      d: "4.600^{\\circ}",
      D: "0.1",
      B: "0.9",
      prod: "0.97",
    })) {
      if (mode === "missing-math" && key === "phi") {
        continue;
      }
      await /** @type {KpressMathText} */ (kpressMathText).render(
        source,
        /** @type {Element} */ (document.getElementById(`s-${key}-test`)),
      );
    }
    if (mode === "variants" || mode === "wrong-active-variant") {
      for (const math of document.querySelectorAll(".katex")) {
        const active = document.createElement("span"),
          dormant = document.createElement("span");
        active.className = dormant.className = "squares-math-variant";
        active.dataset.squaresMathContexts = "custom-serif";
        dormant.dataset.squaresMathContexts = "custom-sans system-serif system-sans";
        const copy = /** @type {Element} */ (math.cloneNode(true));
        /** @type {Element} */ (
          (mode === "variants" ? copy : math).querySelector("annotation")
        ).textContent = "wrong";
        dormant.append(copy);
        math.replaceWith(dormant, active);
        active.append(math);
      }
    }
    if (mode === "width-change") {
      /** @type {HTMLElement} */ (document.querySelector(".shift .tex")).style.width = "180px";
    }
    /** @type {KpressMathText} */ (kpressMathText).complete();
    document.documentElement.classList.add("math-ready");
    if (mode === "late-target") {
      const addAfterFirstReadiness = () => {
        if (
          /** @type {SquaresMathStartupState} */ (globalThis.__mathStartup).metrics
            .parameters_ready_ms == null
        ) {
          requestAnimationFrame(addAfterFirstReadiness);
          return;
        }
        const extra = document.createElement("dd");
        extra.id = "late-target";
        /** @type {Element} */ (document.querySelector(".panel .kv")).append(extra);
        void (
          /** @type {KpressMathText} */ (kpressMathText).render("0", extra).then(releaseLateTarget)
        );
      };
      requestAnimationFrame(addAfterFirstReadiness);
    }
  });
};
