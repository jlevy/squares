// How many elements match this selector. o.selector is the selector.
/** @param {{selector: string}} o */ (o) => document.querySelectorAll(o.selector).length;
