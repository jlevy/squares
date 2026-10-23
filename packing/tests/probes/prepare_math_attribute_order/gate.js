// Pass one fixture formula through KPress's visibility gate as the runtime does: hide it
// through CSSOM, set its math data, show it again. With `readEarly`, the box's attribute list
// is read while it is hidden, as something in the page did in the race think-qa8b records,
// so Chromium writes the lazily kept `style` before the math data. Returns the live order.
/** @param {{ key: string, readEarly: boolean }} o */
({ key, readEarly }) => {
  const box = /** @type {HTMLElement | null} */ (
    document.querySelector(`[data-squares-math-key="${key}"] > .kpress-math-render`)
  );
  if (!box) {
    throw new Error(`no fixture formula ${key}`);
  }
  box.style.setProperty("visibility", "hidden", "important");
  box.dataset.kpressMathPending = "true";
  if (readEarly) {
    void box.attributes.length;
  }
  box.dataset.kpressMathSource = "n";
  box.dataset.kpressMathDisplay = "inline";
  box.style.removeProperty("visibility");
  delete box.dataset.kpressMathPending;
  return box.getAttributeNames();
};
