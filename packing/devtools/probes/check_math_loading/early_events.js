// Early input, before fonts are released: moves every slider twice and fires the resize and
// print events the page listens to, then returns the frozen values each slider was left at.
// Playwright retains this snapshot outside the page, independently of boot resets.
/** @returns {ReadonlyArray<Readonly<{ id: string, value: string }>>} */
() => {
  const sliders = [
    .../** @type {NodeListOf<HTMLInputElement>} */ (
      document.querySelectorAll('input[type="range"]')
    ),
  ];
  const targets = sliders.map((slider, index) => {
    const min = Number(slider.min || 0),
      max = Number(slider.max || 100);
    const step = Number(slider.step) || 1;
    const steps = Math.floor((max - min) / step);
    let value = min + step * ((index + 1) % (steps + 1));
    if (value === Number(slider.value)) {
      value = value === max ? min : max;
    }
    if (value === Number(slider.value)) {
      throw new Error(`No distinct target for ${slider.id}`);
    }
    return Object.freeze({ id: slider.id, value: String(value) });
  });
  Object.freeze(targets);
  for (const [index, slider] of sliders.entries()) {
    const target = /** @type {{ id: string, value: string }} */ (targets[index]);
    slider.value = target.value === slider.max ? slider.min : slider.max;
    slider.dispatchEvent(new Event("input", { bubbles: true }));
    slider.value = target.value;
    slider.dispatchEvent(new Event("input", { bubbles: true }));
  }
  window.dispatchEvent(new Event("resize"));
  window.dispatchEvent(new Event("beforeprint"));
  window.dispatchEvent(new Event("afterprint"));
  return targets;
};
