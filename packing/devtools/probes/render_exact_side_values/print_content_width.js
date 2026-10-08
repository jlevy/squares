// Letter's content box uses the publication layer's actual @page margin token.
() => {
  const box = document.createElement("div");
  box.style.cssText =
    "position:fixed;visibility:hidden;width:calc(8.5in - 2 * var(--kpress-print-page-margin));";
  document.body.append(box);
  try {
    return box.getBoundingClientRect().width;
  } finally {
    box.remove();
  }
};
