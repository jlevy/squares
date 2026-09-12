// The text of every element a selector matches, in document order. Takes {selector}.
(o) => Array.from(document.querySelectorAll(o.selector)).map((e) => e.textContent);
