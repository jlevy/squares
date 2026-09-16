// The text of the first element a selector matches. Takes {selector}.
/** @param {{selector: string}} o */ (o) => document.querySelector(o.selector).textContent;
