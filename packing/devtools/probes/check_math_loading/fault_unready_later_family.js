// Negative control for `--self-test`, injected into the page's head: a formula whose second
// font family is the one that covers its glyph. The first family excludes ≥. A
// whole-family-list check can overlook the later required face in WebKit; the oracle must
// observe its actual load.
() => {
  document.addEventListener("DOMContentLoaded", () => {
    document.fonts.add(
      new FontFace("Math Range First", "url(data:font/woff2;base64,AA==)", {
        unicodeRange: "U+0041",
      }),
    );
    document.fonts.add(
      new FontFace("Math Range Late", "url(data:font/woff2;base64,AA==)", {
        unicodeRange: "U+2265",
      }),
    );
    const fault = document.createElement("div");
    fault.innerHTML =
      '<span class="katex" style="visibility:visible!important">' +
      `<span class="katex-html" style='font-family:"Math Range First","Math Range Late",serif'>` +
      "≥</span></span>";
    document.body.prepend(fault);
  });
};
