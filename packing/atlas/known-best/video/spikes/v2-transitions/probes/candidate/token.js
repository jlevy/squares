// A custom property of the document root, trimmed. Takes {name}.
(o) => getComputedStyle(document.documentElement).getPropertyValue(o.name).trim();
