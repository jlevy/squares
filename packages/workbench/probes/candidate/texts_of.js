// The text of every element a selector matches, in document order. Takes {selector}.
/** @param {{selector: string}} o */ (o) =>
  Array.from(document.querySelectorAll(o.selector)).map((e) => e.textContent);
