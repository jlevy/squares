// Combine the slot measurements from every saved-font context into one fragment per slot. A
// node every context measured identically is kept as it is; one that differs becomes one
// `.squares-math-variant` per distinct version, marked with the contexts that use it, so the
// publication's CSS selects the version the reader's saved preferences ask for.
/**
 * @param {{
 *   contexts: { name: string, fragments: SquaresPreparedFragment[] }[],
 *   attributeNames: string[],
 * }} o
 */
({ contexts, attributeNames }) => {
  /**
   * @param {HTMLElement} element
   * @returns {(HTMLElement | null | undefined)[]}
   */
  const actualNodes = (element) =>
    element.matches(".kpress-math")
      ? [element.querySelector(".kpress-math-render")]
      : element.id.startsWith("kval-")
        ? [.../** @type {NodeListOf<HTMLElement>} */ (element.querySelectorAll(".math-item"))]
        : [element];
  /** @param {Element} node */
  const attributes = (node) =>
    Object.fromEntries(
      attributeNames
        .filter((name) => node.hasAttribute(name))
        .map((name) => [name, node.getAttribute(name)]),
    );
  const first = /** @type {{ fragments: SquaresPreparedFragment[] }} */ (contexts[0]);
  return first.fragments.map((fragment, slot) => {
    const original = /** @type {HTMLElement} */ (
      document.querySelector(`[data-squares-math-key="${slot}"]`)
    );
    const copies = contexts.map((context) => {
      const measured = /** @type {SquaresPreparedFragment} */ (context.fragments[slot]);
      if (measured.key !== fragment.key) {
        throw new Error("math variant keys differ");
      }
      const copy = /** @type {HTMLElement} */ (original.cloneNode(false));
      for (const name of attributeNames) {
        copy.removeAttribute(name);
      }
      for (const [name, value] of Object.entries(measured.attributes)) {
        copy.setAttribute(name, value);
      }
      copy.innerHTML = measured.html;
      return copy;
    });
    const nodes = copies.map(actualNodes);
    const firstNodes = /** @type {(HTMLElement | null | undefined)[]} */ (nodes[0]);
    for (let index = 0; index < firstNodes.length; index++) {
      /** @type {Map<string, { node: HTMLElement, contexts: string[] }>} */
      const versions = new Map();
      contexts.forEach((context, offset) => {
        const node = /** @type {(HTMLElement | null | undefined)[]} */ (nodes[offset])[index];
        if (!node) {
          throw new Error("math variant nodes differ");
        }
        const signature = JSON.stringify([attributes(node), node.innerHTML]);
        const version = versions.get(signature) || { node, contexts: [] };
        version.contexts.push(context.name);
        versions.set(signature, version);
      });
      if (versions.size === 1) {
        continue;
      }
      const parent = /** @type {HTMLElement} */ (firstNodes[index]);
      const variants = [...versions.values()].map(({ node, contexts }) => {
        const variant = document.createElement("span");
        variant.className = "squares-math-variant";
        variant.dataset.squaresMathContexts = contexts.join(" ");
        for (const [name, value] of Object.entries(attributes(node))) {
          variant.setAttribute(name, /** @type {string} */ (value));
        }
        variant.innerHTML = node.innerHTML;
        return variant;
      });
      // The source stays on the original host target. Font/profile state belongs
      // to the selected child, so an inactive serif ancestor cannot override it.
      for (const name of [
        "data-kpress-math-face",
        "data-kpress-math-profile",
        "data-kpress-math-prepared",
      ]) {
        parent.removeAttribute(name);
      }
      parent.replaceChildren(...variants);
    }
    const combined = /** @type {HTMLElement} */ (copies[0]);
    return { key: fragment.key, html: combined.innerHTML, attributes: attributes(combined) };
  });
};
