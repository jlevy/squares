// One computed style property of the first element a selector matches.
// Takes {selector, property}.
/** @param {{selector: string, property: keyof CSSStyleDeclaration}} o */ (o) =>
  getComputedStyle(document.querySelector(o.selector))[o.property];
