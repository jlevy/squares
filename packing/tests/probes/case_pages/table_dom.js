// The native HTML parser restores optional table ends without changing any content.
/** @param {string} markup */
(markup) => new DOMParser().parseFromString(markup, "text/html").body.innerHTML;
