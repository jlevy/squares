// Intercept the native copy event before its default OS clipboard write.
// The selection's text, DOM and exact formula sources remain observable.
/** @param {{selector: string, copy: boolean}} options */
(options) => {
  const host = document.querySelector(options.selector);
  const selection = window.getSelection();
  if (!host || !selection) {
    throw new Error("copy source or selection unavailable");
  }
  const range = document.createRange();
  range.selectNodeContents(host);
  const previous = Array.from({ length: selection.rangeCount }, (_, i) =>
    selection.getRangeAt(i).cloneRange(),
  );
  selection.removeAllRanges();
  selection.addRange(range);
  let intercepted = false;
  let text = "";
  let sourceHtml = "";
  const capture = () => {
    text = selection.toString();
    const cloned = document.createElement("div");
    cloned.append(range.cloneContents());
    sourceHtml = cloned.innerHTML;
  };
  /** @param {ClipboardEvent} event */
  const copy = (event) => {
    event.preventDefault();
    intercepted = true;
    capture();
  };
  if (options.copy) {
    document.addEventListener("copy", copy, { capture: true, once: true });
  }
  let succeeded = false;
  try {
    if (options.copy) {
      succeeded = document.execCommand("copy");
    } else {
      capture();
    }
  } finally {
    document.removeEventListener("copy", copy, true);
    selection.removeAllRanges();
    for (const original of previous) {
      selection.addRange(original);
    }
  }
  return {
    mode: options.copy ? "native-copy-intercepted" : "selection-only-nojs",
    intercepted,
    command_succeeded: succeeded,
    text,
    source_html: sourceHtml,
    mathml: [...host.querySelectorAll("math")].map((node) => node.outerHTML),
    semantic_styles: [
      ...document.querySelectorAll(".kpress-math-semantic, .kpress-math-semantic *"),
    ].map((node) => {
      const style = getComputedStyle(node);
      return {
        reset: style.counterReset,
        increment: style.counterIncrement,
        set: style.counterSet,
        before: getComputedStyle(node, "::before").content,
        after: getComputedStyle(node, "::after").content,
      };
    }),
  };
};
