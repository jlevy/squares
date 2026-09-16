// The distinct certificates the page's `.cert-figure`s carry, in document order.
/** @param {HTMLElement[]} els */
(els) => [...new Set(els.map((el) => el.dataset.cert))];
