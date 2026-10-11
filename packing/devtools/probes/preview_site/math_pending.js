// How many math spans kpress has not yet typeset. It renders them progressively, near
// the viewport first, so a screenshot taken at load shows the untypeset fallback below.
// The frontier's explicit native MathML is already rendered without a KaTeX flag.
() =>
  [...document.querySelectorAll(".kpress-math:not([data-kpress-math-rendered])")].filter((host) => {
    const math = host.querySelector(":scope > math");
    return !(
      host.getAttribute("data-site-native-math") === "frontier" &&
      math?.namespaceURI === "http://www.w3.org/1998/Math/MathML" &&
      math.textContent?.trim() &&
      !math.querySelector("merror")
    );
  }).length;
