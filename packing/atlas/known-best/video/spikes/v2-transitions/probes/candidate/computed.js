// One computed style property of the first element a selector matches.
// Takes {selector, property}.
(o) => getComputedStyle(document.querySelector(o.selector))[o.property];
