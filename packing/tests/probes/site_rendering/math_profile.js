// Read the surrounding face and prepared glyph face without mutating the document.
/** @param {string} selector */
(selector) =>
  [...document.querySelectorAll(selector)].map((host) => ({
    profile: host.getAttribute("data-kpress-math-face"),
    surroundingFont: getComputedStyle(
      host.closest(".kpress-math")?.parentElement ?? host.parentElement ?? host,
    ).fontFamily,
    glyphFont: getComputedStyle(host.querySelector(".mathnormal, .mord") ?? host).fontFamily,
  }));
