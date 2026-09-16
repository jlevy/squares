// Negative control for `--self-test`, injected into the page's head: exposes KaTeX and
// semantic MathML before fonts are released. A failed face stays unavailable even if
// decoding finishes before the next sampled frame, which makes the missing-font control
// deterministic.
() => {
  document.addEventListener("DOMContentLoaded", () => {
    document.fonts.add(new FontFace("Math Unready Control", "url(data:font/woff2;base64,AA==)"));
    const fault = document.createElement("div");
    fault.innerHTML =
      '<span class="katex" style="visibility:visible!important">' +
      `<span class="katex-html" style='font-family:"Math Unready Control"'>x = 1</span></span>` +
      '<math class="kpress-math-semantic" style="visibility:visible!important">' +
      "<mi>y</mi><mo>=</mo><mn>2</mn></math>";
    document.body.prepend(fault);
  });
};
