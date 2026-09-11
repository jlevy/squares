// The drawn width of every visible square, which is the picture the owner is looking at
// rather than the `scale()` in its transform.
() =>
  Array.from(document.querySelectorAll("#squares g[data-identity]"))
    .filter((e) => e.style.display !== "none")
    .map((e) => e.firstElementChild.getBoundingClientRect().width);
