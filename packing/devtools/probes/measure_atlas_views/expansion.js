// Sample the actual Atlas viewport during expansion, including an interrupted move.
// The frames distinguish a height reveal from tiles fading in on an instant canvas.
(/** @type {{interrupt: boolean}} */ { interrupt }) => {
  const cells = document.querySelector(".site-atlas-cells");
  const toggle = document.querySelector("[data-atlas-toggle]");
  if (!(cells instanceof HTMLElement) || !(toggle instanceof HTMLButtonElement)) {
    return null;
  }
  const start = performance.now();
  /** @type {{elapsed: number, height: number}[]} */
  const samples = [{ elapsed: 0, height: cells.getBoundingClientRect().height }];
  toggle.click();
  const animation = cells.getAnimations().find((move) => move.effect instanceof KeyframeEffect);
  const timing = animation?.effect?.getComputedTiming();
  let interrupted = false;
  return new Promise((resolve) => {
    const sample = () => {
      const elapsed = performance.now() - start;
      samples.push({ elapsed, height: cells.getBoundingClientRect().height });
      if (interrupt && !interrupted && elapsed >= 100) {
        interrupted = true;
        toggle.click();
      }
      if (elapsed < 600) {
        requestAnimationFrame(sample);
      } else {
        const priorPan = cells.scrollLeft;
        cells.scrollLeft = -100;
        const pan = cells.scrollLeft;
        cells.scrollLeft = priorPan;
        resolve({
          viewport: {
            width: cells.clientWidth,
            canvas: cells.scrollWidth,
            overflowX: getComputedStyle(cells).overflowX,
            pan,
          },
          duration: timing?.duration ?? 0,
          easing: timing?.easing ?? null,
          samples,
          remaining: cells.getAnimations().length,
          inlineHeight: cells.style.height,
          expanded: toggle.getAttribute("aria-expanded"),
        });
      }
    };
    requestAnimationFrame(sample);
  });
};
