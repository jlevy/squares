// How many elements a selector matches. Takes {selector}.
/** @param {{selector: string}} o */ (o) => document.querySelectorAll(o.selector).length;
