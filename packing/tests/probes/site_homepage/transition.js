// Capture the synchronous input response, shared animation, and persistent nodes.
/** @param {{install: boolean, settle: boolean, rapid?: boolean, position?: boolean}} options */
async (options) => {
  const atlas =
    /** @type {typeof globalThis & {SiteAtlasView: {milliseconds(value: string): number, place(n: number, per: number): {line: number, column: number, opens: boolean}}}} */ (
      globalThis
    ).SiteAtlasView;
  const grid = document.querySelector("[data-atlas-preview]");
  const cells = grid?.querySelector(".site-atlas-cells");
  const toggle = document.querySelector("[data-homepage-atlas-toggle]");
  if (!(grid instanceof HTMLElement) || !(cells instanceof HTMLElement) || !toggle) {
    throw new Error("Missing homepage Atlas controls");
  }
  if (options.position) {
    toggle.scrollIntoView({ block: "center", behavior: "instant" });
  }
  if (options.install) {
    const links = [...cells.querySelectorAll(".site-atlas-cell")];
    const drawings = links.map((link) => link.firstElementChild);
    let beforeScroll = 0;
    /** @type {Map<HTMLElement, number[]>} */
    let beforeLayout = new Map();
    /** @param {HTMLElement} link */
    const geometry = (link) => [
      link.offsetLeft,
      link.offsetTop,
      link.offsetWidth,
      link.offsetHeight,
    ];
    toggle.addEventListener(
      "click",
      () => {
        beforeScroll = window.scrollY;
        beforeLayout = new Map(
          links.flatMap((link) => {
            const box = link.getBoundingClientRect();
            return link instanceof HTMLElement &&
              box.bottom > 0 &&
              box.top < window.innerHeight &&
              box.right > 0 &&
              box.left < window.innerWidth &&
              box.width > 0
              ? [[link, geometry(link)]]
              : [];
          }),
        );
      },
      true,
    );
    toggle.addEventListener("click", () => {
      const current = [...cells.querySelectorAll(".site-atlas-cell")];
      const count = current.filter((link) => link.getClientRects().length > 0).length;
      const history = JSON.parse(grid.dataset.testCounts ?? "[]");
      grid.dataset.testCounts = JSON.stringify([...history, count]);
      grid.dataset.testTransition = JSON.stringify({
        view: grid.dataset.atlasView,
        count,
        same_nodes: current.every(
          (link, i) => link === links[i] && link.firstElementChild === drawings[i],
        ),
        scroll_delta: window.scrollY - beforeScroll,
        layout_changed: [...beforeLayout].some(([link, before]) =>
          geometry(link).some((value, i) => Math.abs(value - (before[i] ?? value)) > 0.5),
        ),
        animations: current.flatMap((link) =>
          link
            .getAnimations()
            .filter(
              (animation) =>
                animation.effect instanceof KeyframeEffect &&
                animation.effect.getKeyframes().some((frame) => "transform" in frame),
            )
            .map((animation) => ({
              duration: animation.effect?.getTiming().duration,
              delay: animation.effect?.getTiming().delay,
              easing: animation.effect?.getTiming().easing,
              current_time: animation.currentTime,
            })),
        ),
      });
    });
  }
  if (options.rapid && toggle instanceof HTMLButtonElement) {
    toggle.click();
    toggle.click();
    toggle.click();
  }
  if (options.settle) {
    await Promise.allSettled(document.getAnimations().map((animation) => animation.finished));
  }
  const per = Number.parseInt(cells.style.getPropertyValue("--site-atlas-per-line"), 10);
  const style = getComputedStyle(grid);
  const shown = [...cells.querySelectorAll(".site-atlas-cell")].filter(
    (link) => link.getClientRects().length > 0,
  );
  return {
    input: JSON.parse(grid.dataset.testTransition ?? "null"),
    counts: JSON.parse(grid.dataset.testCounts ?? "[]"),
    duration: atlas.milliseconds(style.getPropertyValue("--site-atlas-move-duration")),
    easing: style.getPropertyValue("--site-atlas-move-easing").trim(),
    per_line: per,
    placement_errors: shown.flatMap((link) => {
      if (!(link instanceof HTMLElement)) {
        return [0];
      }
      const n = Number(link.dataset.atlasN);
      const at = atlas.place(n, per);
      return Number(link.style.getPropertyValue("--site-atlas-line")) === at.line &&
        Number(link.style.getPropertyValue("--site-atlas-column")) === at.column &&
        Number(link.style.getPropertyValue("--site-atlas-opens")) === Number(at.opens)
        ? []
        : [n];
    }),
    aspects: shown.map((link) => {
      const rect = link.firstElementChild?.getBoundingClientRect();
      return rect ? rect.width / rect.height : null;
    }),
    crop_errors: [11, 18, 291, 324].flatMap((n) => {
      const svg = cells.querySelector(`[data-case="${n}"] > svg`);
      if (!(svg instanceof SVGSVGElement) || svg.getClientRects().length === 0) {
        return [];
      }
      const view = svg.viewBox.baseVal;
      const errors = [...svg.querySelectorAll('text, [data-feature="evidence-badge"]')].flatMap(
        (mark) => {
          if (!(mark instanceof SVGGraphicsElement)) {
            return [`${n}: unexpected mark`];
          }
          const box = mark.getBBox();
          return box.x >= view.x &&
            box.y >= view.y &&
            box.x + box.width <= view.x + view.width &&
            box.y + box.height <= view.y + view.height
            ? []
            : [
                `${n}: ${mark.getAttribute("data-feature") ?? mark.localName} ${JSON.stringify({ x: box.x, y: box.y, width: box.width, height: box.height, view: { x: view.x, y: view.y, width: view.width, height: view.height } })}`,
              ];
        },
      );
      const outline = svg
        .querySelector('[data-feature="container-outline"]')
        ?.getBoundingClientRect();
      if (!outline || Math.abs(outline.width - outline.height) > 0.1) {
        errors.push(`${n}: outline ${outline?.width} x ${outline?.height}`);
      }
      return errors;
    }),
    address: location.href,
    root_view: document.documentElement.dataset.siteAtlasView ?? null,
    root_size: document.documentElement.dataset.siteAtlasSize ?? null,
    panel_id: cells.id,
    panel_role: cells.getAttribute("role"),
    toggle_in_view:
      toggle.getBoundingClientRect().top >= 0 &&
      toggle.getBoundingClientRect().bottom <= window.innerHeight,
  };
};
