// A custom property of the document root, trimmed. Takes {name}.
/** @param {{name: string}} o */ (o) =>
  getComputedStyle(document.documentElement).getPropertyValue(o.name).trim();
